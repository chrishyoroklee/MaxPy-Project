# Max Patch Validity Rules

A formal ruleset for what makes a Max/MSP patch "legal" — meaning it generates, opens, and behaves correctly. Organized into two levels: **Parameter rules** (within individual objects) and **Graph rules** (how objects connect to each other).

These rules are NOT enforced by MaxPy (maxpylang). MaxPy will happily generate patches that violate every rule below. Enforcement is the programmer's responsibility.

---

## Level 1: Parameter Rules (Within Objects)

These rules govern individual objects and their arguments/settings, independent of how they're connected.

### 1.1 Signal Rate Domain

Every Max object operates at one of two rates:

| Rate | Convention | Example Objects | Update Frequency |
|------|-----------|-----------------|-----------------|
| **Signal rate** (audio) | Name ends in `~` | `cycle~`, `lores~`, `*~`, `sig~`, `line~` | Every audio sample (~44,100/sec) |
| **Control rate** (message) | Name does NOT end in `~` | `metro`, `random`, `number`, `counter`, `scale` | Only when triggered by a message |

**Rule 1.1a: Object naming determines rate domain.** If an object name ends in `~`, it processes audio signals. If not, it processes messages. There is no ambiguity — the `~` suffix is the universal indicator.

**Rule 1.1b: Some `~` objects accept control-rate values on specific inlets.** This is the critical nuance. Many signal objects have "hybrid" inlets:
- `cycle~` inlet 0: accepts both signal (smooth frequency) and float/int (stepped frequency)
- `lores~` inlet 1 (cutoff): accepts both signal and float
- `lores~` inlet 2 (resonance): accepts both signal and float
- `*~` inlet 1: accepts both signal and float

The object will work either way, but **control-rate input produces stepped/quantized behavior** while signal-rate input produces smooth continuous behavior. For frequency and amplitude, stepped = audible artifacts (zipper noise, clicks).

### 1.2 Value Types

Max has distinct data types that objects expect on their inlets:

| Type | Description | Example |
|------|------------|---------|
| `bang` | Trigger with no data | output of `button`, `loadbang`, `metro` |
| `int` | Integer number | `42`, `0`, `-7` |
| `float` | Floating-point number | `3.14`, `0.5`, `440.0` |
| `symbol` | Text string | `freq`, `hello`, `set` |
| `list` | Ordered sequence | `60 100`, `pitch 440 0.5` |
| `signal` | Continuous audio stream | output of any `~` object |

**Rule 1.2a: Objects have expected types per inlet.** Each inlet of an object expects specific types. Sending the wrong type produces unexpected behavior:

| Situation | What Happens |
|-----------|-------------|
| `bang` into `pack` int inlet | `pack` outputs its current stored values (not an error, but semantically surprising) |
| `float` into `int`-expecting inlet | Truncated to integer silently |
| `int` into `float`-expecting inlet | Promoted to float (usually fine) |
| `symbol` into `number` box | Ignored silently |
| `list` into single-value inlet | First element used, rest discarded |

**Rule 1.2b: `message` box content determines output type.** The text inside a `message` box defines what type it outputs when banged:
- `message 440` → outputs int `440`
- `message 440.` → outputs float `440.0`
- `message 1. 10` → outputs list `1.0 10` (used by `line~` for ramp target + time)
- `message set 42` → outputs message `set 42` (the word "set" is a symbol prefix)

### 1.3 Parameter Ranges

Objects have valid parameter ranges. Exceeding them doesn't crash Max but produces broken audio or meaningless output.

**Rule 1.3a: Filter resonance must stay within stable range.**
- `lores~` resonance: safe range `0.0` to `~0.95`. Above ~1.0, the filter self-oscillates (produces its own tone). At 5.0, it's a screaming feedback loop.
- `reson~` resonance/Q: controls bandwidth. Very high Q (>100) produces ringing. Very low Q (<1) produces nearly no filtering.

**Rule 1.3b: Frequencies must be positive and below Nyquist.**
- Oscillator frequency (`cycle~`, `saw~`, etc.): must be > 0 and < sample_rate/2 (typically < 22050 Hz at 44.1kHz)
- Filter cutoff (`lores~` inlet 1): same constraint. Cutoff at 0 Hz = no signal passes. Cutoff above Nyquist = filter does nothing useful.
- Negative frequencies: `cycle~` handles them (phase reversal), but `saw~` and `rect~` may produce unexpected results.

**Rule 1.3c: Gain/amplitude should stay in -1.0 to 1.0 for output.**
- Individual voices can exceed this range internally, but the signal reaching `ezdac~` should be clipped to -1.0 to 1.0.
- Always use `clip~ -1. 1.` before `ezdac~` as a safety net.
- Multiple voices summed together will exceed 1.0 — scale by `*~ (1/N)` or use `clip~`.

**Rule 1.3d: Time values must be positive.**
- `metro` interval: milliseconds, must be > 0. Very small values (<1ms) flood the scheduler.
- `line~` ramp time: milliseconds. 0ms = instant jump. Negative = ignored.
- `delay` time: milliseconds, must be >= 0.
- `tapin~` buffer size: milliseconds, must be > 0, sets maximum delay time.

**Rule 1.3e: Object-specific argument requirements.**
- `clocker` requires a time interval argument (`clocker 1000`). Without it: maxpylang may create an unknown object with 0 inlets/outlets.
- `select` arguments define outlet count. `select 1 0` = 3 outlets (match 1, match 0, no match). Arguments must match expected input type.
- `scale` arguments: `scale inLow inHigh outLow outHigh [exp]`. If inLow == inHigh, division by zero.
- `buffer~` requires a name argument (`buffer~ mybuf`). Without it, the buffer has no name and can't be referenced.

### 1.4 File Path Rules

Some objects reference external files. The file must exist and be accessible at runtime.

**Rule 1.4a: `buffer~` file loading.**
- `buffer~ mybuf filename.wav` — the .wav file must be in Max's search path (same folder as the patch, or in File Preferences paths).
- If the file doesn't exist, `buffer~` creates an empty buffer (no crash, but no audio).

**Rule 1.4b: `bpatcher` file reference.**
- `bpatcher` loads another `.maxpat` file. The file must exist at the specified path.

**Rule 1.4c: `js` / `jsui` script files.**
- Reference a `.js` file that must be in the same folder as the patch or in Max's search path.

---

## Level 2: Graph Rules (Connections Between Objects)

These rules govern how objects connect to each other — the patch cord topology.

### 2.1 Rate Domain Matching

**Rule 2.1a: Signal-rate chains must be continuous.**
An audio signal path must be `~` objects all the way from source to `ezdac~`. If a non-`~` object appears in the middle of a signal chain, the audio stream is broken.

```
LEGAL:   cycle~ → lores~ → *~ → clip~ → ezdac~
ILLEGAL: cycle~ → scale → *~ → ezdac~
                   ^^^^^ control-rate object breaks the audio chain
```

**Rule 2.1b: Control-to-signal bridging requires `sig~`.**
When a control-rate value (from `number`, `scale`, `random`, etc.) needs to drive a signal-rate inlet smoothly, it must pass through `sig~` first.

```
LEGAL:   number → sig~ → cycle~ inlet 0    (smooth frequency changes)
WORKS BUT DEGRADED: number → cycle~ inlet 0 (stepped frequency, zipper noise)
```

The "works but degraded" case is technically accepted by Max — `cycle~` can receive floats on inlet 0. But the frequency only updates when a new message arrives, not sample-by-sample. For pitch, this produces audible stepping.

**Rule 2.1c: Signal-to-control bridging requires `snapshot~`.**
When you need to read an audio signal's current value as a control-rate number (e.g., for monitoring amplitude), use `snapshot~` (samples the signal at a specified interval) or `peakamp~` (reports peak amplitude over a window).

```
LEGAL:   *~ → peakamp~ 100 → snapshot~ 50 → number   (amplitude monitor)
ILLEGAL: *~ → number                                    (won't work — number ignores signals)
```

### 2.2 Outlet-to-Inlet Type Compatibility

**Rule 2.2a: Signal outlets connect to signal inlets.**
An outlet typed `"signal"` (in the maxpat JSON `outlettype`) should connect to an inlet that accepts signals.

| Source outlet type | Valid destination inlet types |
|-------------------|------------------------------|
| `signal` | Signal inlets on `~` objects, or hybrid inlets |
| `""` (empty = any message) | Message inlets on any object |
| `bang` | Message inlets that respond to bang |
| `int` | Message inlets that accept int |
| `float` | Message inlets that accept float |
| `list` | Message inlets that accept list |

**Rule 2.2b: Multiple message types can feed the same inlet.**
Most Max inlets accept multiple types. A `number` box inlet accepts int, float, and bang (bang causes it to output its current value). This flexibility means type errors are rarely hard failures — they're semantic mismatches that produce wrong behavior rather than crashes.

**Rule 2.2c: Multiple cords into one inlet are summed (signals) or last-wins (messages).**
- **Signal inlets:** Multiple signal cords into one inlet are summed. `osc1~ → *~ inlet 0` + `osc2~ → *~ inlet 0` = the two signals are added before multiplication.
- **Message inlets:** Only the most recently arrived message is used. If two `metro` objects both send to the same `number` box, whichever fires last overwrites the other.

### 2.3 Graph Connectivity

**Rule 2.3a: Every audio chain must reach `ezdac~` (or `dac~`).**
An audio processing chain that doesn't connect to an output object produces no sound. The DSP still runs (wasting CPU) but the result goes nowhere. This is the most common structural bug in Max patches.

```
LEGAL:   cycle~ → lores~ → *~ → ezdac~        (sound comes out)
ILLEGAL: cycle~ → lores~ → *~                   (orphaned — silent, wastes CPU)
```

**Rule 2.3b: No required inlets should be unconnected (in audio chains).**
Signal objects with unconnected signal inlets receive 0.0 on that inlet. For most objects this means silence:
- `*~` with unconnected inlet 1 → multiplies by 0 → silence
- `+~` with unconnected inlet 1 → adds 0 → signal passes through unchanged
- `lores~` with unconnected inlet 0 → no input signal → silence

**Rule 2.3c: Feedback loops require `tapin~/tapout~` or explicit delay.**
Direct feedback in signal chains (output of A feeds back to input of A) creates an infinite loop at the DSP level. Max handles this with single-sample delay in some cases, but explicit feedback should use:
- `tapin~` / `tapout~` for audio feedback (delay-based)
- `delay` for message feedback (time-delayed)

```
LEGAL:   tapin~ → tapout~ → *~ 0.7 → tapin~    (feedback delay with decay)
RISKY:   lores~ → *~ → lores~                    (Max may handle with 1-sample delay, but behavior is unpredictable)
```

### 2.4 Execution Order

**Rule 2.4a: Right-to-left, depth-first evaluation.**
When a single outlet connects to multiple inlets, Max sends messages **right to left** (rightmost connection first). This ordering is invisible in the patch visually but determines which inlet gets set first.

This matters when two inlets of the same object receive from the same source:
```
number → [right inlet of +] AND [left inlet of +]
```
The right inlet is set first, THEN the left inlet triggers computation. This is usually correct. But if the order were reversed, the left inlet would trigger `+` with the OLD right-inlet value.

**Rule 2.4b: Use `trigger` to make execution order explicit.**
When order matters, don't rely on invisible connection ordering. Use `trigger` (alias `t`) to explicitly fire outputs right-to-left:

```
number → trigger f b → outlet 0 (float, fires second) → left inlet of *
                     → outlet 1 (bang, fires first)  → message 10 → right inlet of *
```

This guarantees the multiplier is set before the value arrives.

**Rule 2.4c: Hot vs. cold inlets.**
In most Max objects, only the **leftmost inlet** (inlet 0) is "hot" — meaning receiving a message on it triggers the object to compute and output. Other inlets are "cold" — they store the value silently until the hot inlet fires.

```
+ object:  inlet 0 (hot) — receiving a number triggers addition and output
           inlet 1 (cold) — receiving a number stores it, no output yet
```

This means: **always set cold inlets before sending to the hot inlet.** `trigger` enforces this.

### 2.5 Semantic Correctness

Beyond type and rate matching, connections must make semantic sense for the patch to work as intended.

**Rule 2.5a: Oscillator frequency inlets expect frequency values (Hz).**
Sending a MIDI note number (0-127) directly to `cycle~` inlet 0 produces the wrong pitch. MIDI 60 becomes 60 Hz (a low B-flat), not middle C (261.6 Hz). The conversion chain is:
```
kslider → mtof → sig~ → cycle~     (MIDI note → Hz → signal → oscillator)
```

**Rule 2.5b: `line~` expects ramp-formatted messages.**
`line~` does NOT accept plain numbers. It expects pairs: `target time` meaning "ramp to `target` over `time` milliseconds."
```
LEGAL:   message "1. 10"  → line~     (ramp to 1.0 over 10ms)
LEGAL:   message "0. 300" → line~     (ramp to 0.0 over 300ms)
BROKEN:  number 1         → line~     (jumps to 1 instantly, no ramp — technically works but defeats the purpose)
```

**Rule 2.5c: `select` arguments must match incoming value domain.**
`select 1 0` expects integers and fires outlet 0 when it receives 1, outlet 1 when it receives 0. If you send it floats or symbols, it will never match (silent failure — nothing comes out).

**Rule 2.5d: `pack` inlet types are defined by arguments.**
`pack 0 0` creates two int inlets. `pack 0. 0.` creates two float inlets. `pack 0 hello` creates an int inlet and a symbol inlet. Sending the wrong type to an inlet coerces silently (float→int truncates, bang→"output current values").

**Rule 2.5e: `route` strips the first element.**
`route pitch velocity cc` matches the first word and outputs the **remainder**. So `pitch 440` enters, and `440` exits outlet 0 (the word "pitch" is consumed). If you expect the full message including the prefix, use `select` instead.

---

## Summary: Violation Categories

| Category | What Can Go Wrong | Severity | Max Behavior |
|----------|-------------------|----------|-------------|
| **Signal rate** | Control-rate value driving signal inlet without `sig~` | Medium | Works but with audible stepping/zipper noise |
| **Signal rate** | Signal chain broken by control-rate object | High | Audio stream stops at that point |
| **Value type** | Wrong type into inlet (bang where int expected) | Low-Medium | Silent coercion or ignored, semantically wrong |
| **Parameter range** | Filter resonance too high | High | Self-oscillation, feedback, dangerously loud |
| **Parameter range** | Frequency at 0 or negative | Medium | Silence or unexpected behavior |
| **Parameter range** | Gain > 1.0 at output | Medium-High | Clipping, distortion, potential speaker damage |
| **Connectivity** | Audio chain doesn't reach `ezdac~` | High | Complete silence, wasted CPU |
| **Connectivity** | Hot inlet never triggered | High | Object never fires — dead path |
| **Execution order** | Cold inlet set after hot inlet | Medium | Uses stale value, wrong computation |
| **Semantic** | MIDI note sent as frequency | Medium | Wrong pitch (off by a lot) |
| **Semantic** | Plain number sent to `line~` | Low | Instant jump instead of smooth ramp |
| **File path** | Referenced file doesn't exist | Medium | Empty buffer / missing subpatch, silent failure |

---

## What MaxPy (maxpylang) Does and Does NOT Enforce

| Rule | MaxPy Enforces? | Notes |
|------|----------------|-------|
| Object name recognition | Partial | Warns about unknown objects but still generates them |
| Inlet/outlet count | Yes | Refuses to connect to non-existent inlets |
| Signal rate matching | **No** | Allows control→signal connections without `sig~` |
| Value type matching | **No** | Allows any outlet→inlet connection regardless of type |
| Parameter ranges | **No** | Accepts `lores~ 800 5.0` without warning |
| Graph connectivity | **No** | No reachability analysis — orphaned subgraphs are silent |
| Execution order | **No** | No hot/cold inlet awareness |
| Semantic correctness | **No** | No domain knowledge (MIDI vs Hz, ramp format, etc.) |

**Bottom line:** MaxPy is a structural generation tool. It ensures objects exist and connections reference valid inlets/outlets. Everything else — rate matching, type safety, parameter validity, graph completeness, semantic correctness — is the programmer's responsibility.
