# Max Patch Validity Rules

A formal ruleset for what makes a Max/MSP patch "legal" — meaning it generates, opens, and behaves correctly. Organized into six levels:

1. **Data Type & Message Rules** — atom types, coercion, message formatting
2. **Signal Rate Domain Rules** — audio vs control rate, bridging, hybrid inlets
3. **Object Validity Reference** — per-object specs (inlets, outlets, args, ranges)
4. **Graph Rules** — connection topology, type compatibility, feedback
5. **Execution Order & Scheduling Rules** — hot/cold inlets, threads, timing
6. **Patcher Lifecycle Rules** — initialization, loadbang, closing

These rules are NOT enforced by MaxPy (maxpylang). MaxPy will happily generate patches that violate every rule below. Enforcement is the programmer's responsibility.

---

## Level 1: Data Type & Message Rules

These rules govern the fundamental data types in Max and how they interact.

### 1.1 Atom Types

Max messages are composed of **atoms** — the smallest unit of data. Every atom is one of these types:

| Type | Description | Examples | Precision |
|------|------------|---------|-----------|
| `bang` | Trigger with no data | output of `button`, `loadbang`, `metro` | N/A |
| `int` | Integer number | `42`, `0`, `-7` | 32-bit signed (−2,147,483,648 to 2,147,483,647) |
| `float` | Floating-point number | `3.14`, `0.5`, `440.0` | 64-bit double precision |
| `symbol` | Text string (interned) | `freq`, `hello`, `set` | Interned — symbols are stored once and compared by pointer |

**Rule 1.1a: Every value in Max is one of these four atom types (plus signal).** There is no boolean, no null, no undefined. `toggle` outputs int 0 or 1. "True/false" is always int 0/non-zero.

**Rule 1.1b: Signal is a separate domain, not an atom type.** Audio signals are continuous streams of 64-bit floats processed at sample rate. They cannot be mixed with atom-based messages without explicit bridging (`sig~`, `snapshot~`).

### 1.2 List Rules

**Rule 1.2a: A list is an ordered sequence of atoms.** Lists are not a distinct type — they're a message containing multiple atoms.

**Rule 1.2b: Lists must start with int or float.** If the first element is a number, the message is a plain list. Examples: `60 100`, `440.0 0.5 1000`.

**Rule 1.2c: A symbol-prefixed sequence is a "message" (selector + arguments), not a list.** `set 42` is the selector `set` with argument `42`. `pitch 440 0.5` is the selector `pitch` with arguments `440` and `0.5`. Objects use the selector to decide which method to invoke.

### 1.3 Int vs Float Mode

**Rule 1.3a: A decimal point in arguments switches objects to float mode.** Many control objects operate in either int or float mode depending on their creation arguments:

| Arguments | Mode | Output Type | Behavior |
|-----------|------|-------------|----------|
| `scale 0 127 0 1` | Int mode | int | Output truncated to integer — always 0 or 1 |
| `scale 0 127 0. 1.` | Float mode | float | Output is continuous float 0.0–1.0 |
| `+ 5` | Int mode | int | Truncates float input to int before adding |
| `+ 5.` | Float mode | float | Promotes int input to float |
| `pack 0 0` | Int inlets | int | Float input truncated to int |
| `pack 0. 0.` | Float inlets | float | Int input promoted to float |

**Rule 1.3b: This applies to `scale`, `+`, `-`, `*`, `/`, `%`, `pack`, `unpack`, `expr`, and most math objects.** Forgetting the decimal point is one of the most common Max bugs. `scale 0 127 0 1` produces only 0 or 1, not a smooth 0.0–1.0 range.

### 1.4 Type Coercion Rules

When a value arrives at an inlet expecting a different type, Max applies silent coercion:

| From | To | Behavior |
|------|----|----------|
| `float` → `int` | Truncation toward zero | `3.7` → `3`, `-2.3` → `-2` (NOT rounded) |
| `int` → `float` | Promotion | `42` → `42.0` (lossless) |
| `symbol` → `int`/`float` | Ignored | The symbol is silently dropped — no output, no error |
| `bang` → `pack` | "Output current values" | `pack` outputs its stored values, treating bang as a trigger |
| `bang` → `number`/`flonum` | "Output current value" | Number boxes output their current value |
| `list` → single-value inlet | First element used | Rest of list is discarded silently |
| `int` → `bang`-expecting inlet | Treated as trigger | Most objects that respond to bang also respond to any message |

**Rule 1.4a: Float-to-int truncates, it does NOT round.** `3.9` becomes `3`, not `4`. This catches people who expect rounding.

**Rule 1.4b: Symbol-to-number is silently ignored.** No error, no warning, no output. The message simply vanishes.

### 1.5 Message Formatting

**Rule 1.5a: Dollar-sign substitution ($1–$9) inserts arguments.** In a `message` box, `$1` is replaced by the first element of the incoming message, `$2` by the second, etc.

```
message box text: "pitch $1 velocity $2"
incoming message: 60 100
output: pitch 60 velocity 100
```

**Rule 1.5b: `$1`–`$9` reference inlet arguments in message boxes; `#1`–`#9` reference patcher arguments.** Inside subpatchers/abstractions, `#1` etc. are replaced at load time with the arguments passed to the subpatcher.

**Rule 1.5c: Comma (`,`) sends sequential messages.** `1, 2, 3` in a message box sends three separate messages in sequence when triggered: first `1`, then `2`, then `3`.

**Rule 1.5d: Semicolon (`;`) routes to named objects.** `; target-name value` sends `value` to the object named `target-name` (a `receive` or named object). This is global routing — the target doesn't need to be connected by a patch cord.

### 1.6 Character Escaping

**Rule 1.6a: Backslash escapes special characters.** To include a literal comma, semicolon, or dollar sign in a message: `\,`, `\;`, `\$`.

**Rule 1.6b: Double quotes preserve spaces in symbols.** `"hello world"` is a single symbol, not two. Without quotes, `hello world` would be parsed as two atoms.

### 1.7 Named Data Types

Beyond atoms, Max has reference-based types passed by name, not by value:

| Type | Passed As | Created By | Accessed By |
|------|-----------|------------|-------------|
| Dictionary (`dict`) | Symbol (name) | `dict`, `dict.pack` | `dict.unpack`, `dict.get` |
| Array (`array`) | Symbol (name) | `array` | `array.get`, `array.set` |
| Buffer (`buffer~`) | Symbol (name) | `buffer~` | `cycle~`, `groove~`, `peek~`, `poke~` |
| Jitter matrix (`jit_matrix`) | Symbol (name) | `jit.matrix` | Any `jit.*` object |
| GL texture (`jit_gl_texture`) | Symbol (name) | `jit.gl.texture` | Any `jit.gl.*` object |

**Rule 1.7a: Named data is passed by reference.** Sending a buffer name to `cycle~` doesn't copy the audio — it tells `cycle~` where to look. Multiple objects sharing the same name share the same data.

**Rule 1.7b: Names must be unique per type within a session.** Two `buffer~ mybuf` objects in different patches share the same buffer. Use unique names or patcher-scoped naming conventions.

---

## Level 2: Signal Rate Domain Rules

These rules govern the two processing domains in Max and how to bridge between them.

### 2.1 Rate Domains

Every Max object operates at one of two rates:

| Rate | Convention | Example Objects | Update Frequency |
|------|-----------|-----------------|-----------------|
| **Signal rate** (audio) | Name ends in `~` | `cycle~`, `lores~`, `*~`, `sig~`, `line~` | Every audio sample (~44,100/sec) |
| **Control rate** (message) | Name does NOT end in `~` | `metro`, `random`, `number`, `counter`, `scale` | Only when triggered by a message |

**Rule 2.1a: Object naming determines rate domain.** If an object name ends in `~`, it processes audio signals. If not, it processes messages. The `~` suffix is the universal indicator — no exceptions.

### 2.2 Hybrid Inlets

**Rule 2.2a: Some `~` objects accept control-rate values on specific inlets.** These "hybrid" inlets accept both signals and float/int messages:

| Object | Inlet | Accepts Signal? | Accepts Float/Int? | Notes |
|--------|-------|----------------|-------------------|-------|
| `cycle~` | 0 (frequency) | Yes | Yes | Float = stepped frequency, signal = smooth |
| `cycle~` | 1 (phase offset) | Yes | Yes | 0.0–1.0 range |
| `lores~` | 1 (cutoff) | Yes | Yes | Hz value |
| `lores~` | 2 (resonance) | Yes | Yes | 0.0–1.0 range |
| `svf~` | 1 (center freq) | Yes | Yes | Hz value |
| `svf~` | 2 (Q) | Yes | Yes | 0.01–1.0 range |
| `*~` | 0, 1 | Yes | Yes | Float sets constant multiplier |
| `+~` | 0, 1 | Yes | Yes | Float sets constant addend |
| `-~` | 0, 1 | Yes | Yes | Float sets constant subtrahend |

**Rule 2.2b: Control-rate input to hybrid inlets produces stepped/quantized behavior.** The value only updates when a new message arrives — not sample-by-sample. For frequency and amplitude, stepped updates cause audible artifacts (zipper noise, clicks).

### 2.3 sig~ Bridging (Control → Signal)

**Rule 2.3a: Control-to-signal bridging requires `sig~`.** When a control-rate value needs to drive a signal-rate inlet smoothly, pass it through `sig~` first.

```
LEGAL:   number → sig~ → cycle~ inlet 0    (smooth frequency changes)
WORKS BUT DEGRADED: number → cycle~ inlet 0 (stepped frequency, zipper noise)
```

**Rule 2.3b: `sig~` outputs a constant signal with no smoothing.** It immediately jumps to the new value — there is no interpolation. For ramped transitions, use `line~` instead.

**Rule 2.3c: With SIAI enabled, `sig~` is sample-accurate.** When Scheduler in Audio Interrupt is on, `sig~` updates at the exact sample boundary of the triggering event.

### 2.4 snapshot~ Bridging (Signal → Control)

**Rule 2.4a: Signal-to-control bridging requires `snapshot~`.** Control-rate objects (like `number`) cannot receive signals directly — they ignore them silently.

```
LEGAL:   *~ → snapshot~ 50 → number    (samples signal every 50ms)
ILLEGAL: *~ → number                    (won't work — number ignores signals)
```

**Rule 2.4b: `snapshot~` has two modes.** With an interval argument (e.g., `snapshot~ 50`), it auto-samples at that interval. With interval 0, it only samples when banged.

**Rule 2.4c: `peakamp~` is an alternative for amplitude monitoring.** It reports the peak absolute amplitude over a window, useful for level meters.

### 2.5 Signal Arithmetic

**Rule 2.5a: Multiple signals into one inlet are summed.** If two signal cords connect to the same signal inlet, the signals are added together before the object processes them.

**Rule 2.5b: Control messages into signal inlets are stepped/quantized.** The value is held constant until the next message arrives. No interpolation between values.

---

## Level 3: Object Validity Reference

Per-object specifications for objects used in our examples and common Max objects. Each entry documents arguments, inlets, outlets, parameter ranges, and common mistakes.

### 3.1 Oscillators & Generators

#### `cycle~` — Cosine/Wavetable Oscillator

| Property | Details |
|----------|---------|
| **Arguments** | `cycle~ [freq] [buffer-name] [sample-offset]` — all optional |
| **Defaults** | Freq: 0 Hz. Uses internal 16,384-sample cosine wavetable if no buffer |
| **Inlets** | 2: (0) frequency — signal or float, Hz; (1) phase offset — signal or float, 0.0–1.0 |
| **Outlets** | 1: signal output (−1.0 to 1.0 for default cosine) |
| **Hot inlets** | 0 |
| **Phase range** | 0.0 to 1.0 (wraps). 0.5 = half cycle offset |
| **Messages** | `set <buffer-name>` — switch wavetable. `setall <buffer-name>` — set and reset phase |
| **Buffer mode** | When referencing a `buffer~`, reads it as a single-cycle wavetable |
| **Common mistakes** | Sending MIDI note numbers instead of Hz (use `mtof` first). Forgetting freq arg = silent (0 Hz) |

#### `saw~` — Antialiased Sawtooth Oscillator

| Property | Details |
|----------|---------|
| **Arguments** | `saw~ [freq]` — optional, default 0 Hz |
| **Inlets** | 2: (0) frequency — signal or float, Hz; (1) sync — signal, resets phase on positive zero-crossing |
| **Outlets** | 1: signal output (−1.0 to 1.0, antialiased) |
| **Hot inlets** | 0 |
| **Notes** | Antialiased (band-limited). Output is bipolar. Default 0 Hz = silence |
| **Common mistakes** | Negative frequencies may produce unexpected results (unlike `cycle~`) |

#### `noise~` — White Noise Generator

| Property | Details |
|----------|---------|
| **Arguments** | None |
| **Inlets** | 0 |
| **Outlets** | 1: signal output (uniform random, −1.0 to 1.0) |
| **Notes** | No inputs, no arguments. Pure uniform white noise. New random value every sample |

### 3.2 Filters

#### `lores~` — Resonant Lowpass Filter

| Property | Details |
|----------|---------|
| **Arguments** | `lores~ [cutoff-Hz] [resonance]` — both optional |
| **Inlets** | 3: (0) signal input; (1) cutoff frequency — signal or float, Hz; (2) resonance — signal or float |
| **Outlets** | 1: filtered signal output |
| **Hot inlets** | 0 |
| **Cutoff range** | 0 Hz (nothing passes) to Nyquist (sr/2, ~22050 Hz). Values beyond Nyquist: filter does nothing useful |
| **Resonance range** | 0.0 (no resonance) to 1.0 (self-oscillation). Safe range: 0.0–0.95. Above ~1.0: self-oscillation, potentially very loud |
| **Messages** | `clear` — reset filter state (use after blowup/NaN recovery) |
| **Common mistakes** | Resonance > 1.0 causes runaway feedback. Always `clear` after changing parameters drastically. Not clipping output before `ezdac~` |

#### `svf~` — State Variable Filter

| Property | Details |
|----------|---------|
| **Arguments** | `svf~ [center-freq] [Q]` — both optional |
| **Inlets** | 3: (0) signal input; (1) center frequency — signal or float, Hz; (2) Q — signal or float |
| **Outlets** | 4: (0) lowpass; (1) highpass; (2) bandpass; (3) notch |
| **Hot inlets** | 0 |
| **Q range** | 0.01 to 1.0. Modes: Hz, linear (0–1), radians |
| **Messages** | `clear` — reset filter state for blowup recovery |
| **Common mistakes** | Confusing the four outlets. Q outside valid range causes instability |

### 3.3 Envelopes & Ramps

#### `line~` — Signal Ramp Generator

| Property | Details |
|----------|---------|
| **Arguments** | `line~ [initial-value]` — optional, default 0.0 |
| **Inlets** | 2: (0) target-time pairs or value; (1) time in ms (sets ramp time for next target) |
| **Outlets** | 2–3: (0) signal output; (1) bang when ramp completes; (2) optional: 1 while ramping, 0 when idle |
| **Hot inlets** | 0 |
| **Pair format** | `target time` — ramp to `target` over `time` ms. Example: `1. 10` = ramp to 1.0 in 10ms |
| **Compound ramps** | Up to 128 target-time pairs in one message: `0. 0 1. 1000 0. 1000` (jump to 0, ramp to 1 over 1s, ramp back to 0 over 1s) |
| **Messages** | `pause` — freeze ramp. `resume` — continue. `stop` — halt and stay at current value |
| **Common mistakes** | Sending plain number without time (instant jump, no ramp). Forgetting decimal point (int mode). Not waiting for completion bang before starting next ramp |

### 3.4 Amplitude & Math (Signal Rate)

#### `*~` — Signal Multiply

| Property | Details |
|----------|---------|
| **Arguments** | `*~ [constant]` — optional float, default 0.0 |
| **Inlets** | 2: (0) signal or float; (1) signal or float |
| **Outlets** | 1: signal (product) |
| **Unconnected inlet** | 0.0 — multiplying by zero = silence |
| **Common mistakes** | Leaving inlet 1 unconnected = multiplying by 0 = silence. Use `*~ 1.` if passthrough is intended |

#### `+~` — Signal Add

| Property | Details |
|----------|---------|
| **Arguments** | `+~ [constant]` — optional float, default 0.0 |
| **Inlets** | 2: (0) signal or float; (1) signal or float |
| **Outlets** | 1: signal (sum) |
| **Unconnected inlet** | 0.0 — adding zero = passthrough |

#### `-~` — Signal Subtract

| Property | Details |
|----------|---------|
| **Arguments** | `-~ [constant]` — optional float, default 0.0 |
| **Inlets** | 2: (0) signal or float; (1) signal or float |
| **Outlets** | 1: signal (difference: inlet 0 − inlet 1) |
| **Unconnected inlet** | 0.0 — subtracting zero = passthrough |

#### `clip~` — Signal Clamp

| Property | Details |
|----------|---------|
| **Arguments** | `clip~ [min] [max]` — optional, default both 0.0 |
| **Inlets** | 3: (0) signal input; (1) minimum — float; (2) maximum — float |
| **Outlets** | 1: clamped signal |
| **Modes** | Default: values outside range are clamped to min/max |
| **Common mistakes** | Forgetting to set min/max (both default 0.0 = constant zero output). Always use `clip~ -1. 1.` before `ezdac~` |

#### `tanh~` — Hyperbolic Tangent (Soft Saturation)

| Property | Details |
|----------|---------|
| **Arguments** | None |
| **Inlets** | 1: signal input |
| **Outlets** | 1: signal output (−1.0 to 1.0, soft-clipped) |
| **Notes** | Soft saturation curve. Input near 0 passes through linearly; large input asymptotically approaches ±1.0. Good for gentle distortion/warmth |

### 3.5 Delay

#### `tapin~` — Delay Line Input

| Property | Details |
|----------|---------|
| **Arguments** | `tapin~ [max-delay-ms]` — required for useful operation, default 100ms |
| **Inlets** | 2: (0) signal input; (1) messages (`clear`, `freeze`) |
| **Outlets** | 1: **must connect to `tapout~` left inlet** — this is memory sharing, not a signal |
| **Messages** | `clear` — zero the delay buffer. `freeze` — stop writing new input (loop current buffer) |
| **Critical rule** | The outlet of `tapin~` MUST connect to the left inlet of `tapout~`. This connection shares the delay memory — it is not a normal signal connection |
| **Common mistakes** | Connecting `tapin~` outlet to anything other than `tapout~`. Resizing (changing max delay) clears the buffer and causes clicks |

#### `tapout~` — Delay Line Output

| Property | Details |
|----------|---------|
| **Arguments** | `tapout~ [delay-ms] [delay-ms] ...` — one outlet per delay time argument |
| **Inlets** | 1: **must receive from `tapin~` outlet** (memory sharing) |
| **Outlets** | N: one signal outlet per delay time argument |
| **Notes** | Multiple `tapout~` objects can share a single `tapin~`. Delay times can exceed `tapin~` max (wraps/clips) |
| **Common mistakes** | Not connecting to a `tapin~` (no output). Delay time > tapin~ buffer size |

### 3.6 Output

#### `ezdac~` — Audio Output (Easy DAC)

| Property | Details |
|----------|---------|
| **Arguments** | `ezdac~ [ch1] [ch2]` — optional channel assignment, default 1 2 |
| **Inlets** | 2: (0) left channel signal; (1) right channel signal |
| **Outlets** | 0 |
| **Signal range** | Input must be −1.0 to 1.0. Signals outside this range clip and may damage speakers |
| **Messages** | `startwindow` — start audio for this patcher only. `start` / `stop` — global audio. `set [ch1] [ch2]` — remap output channels (requires audio restart) |
| **Common mistakes** | Not using `clip~ -1. 1.` before `ezdac~`. Forgetting to turn audio on (click the speaker icon or send `startwindow`) |

### 3.7 Control Objects

#### `metro` — Metronome (Periodic Bang Generator)

| Property | Details |
|----------|---------|
| **Arguments** | `metro [interval-ms]` — optional, default 5ms |
| **Inlets** | 2: (0) on/off (non-zero = start, 0 = stop) + bang to fire immediately; (1) interval in ms |
| **Outlets** | 1: bang at each interval |
| **Behavior** | Bangs immediately on start, then at interval. Supports time formats (ms, Hz, ticks, bars.beats.units) |
| **Attributes** | `active` — query running state. `autostart` — start automatically |
| **Common mistakes** | Very small intervals (<1ms) flood the scheduler and can hang Max. Default 5ms is very fast — usually want 100+ ms |

#### `counter` — Counter

| Property | Details |
|----------|---------|
| **Arguments** | `counter [direction] [min] [max]` — direction: 0=up, 1=down, 2=updown |
| **Inlets** | 5: (0) bang to count; (1) direction; (2) set to min; (3) set to max; (4) set current value |
| **Outlets** | 4: (0) count value; (1) carry bang (reached max going up); (2) carry bang (reached min going down); (3) current count on underflow/overflow |
| **Hot inlets** | 0 |
| **Common mistakes** | Confusing the 5 inlets. Not setting min/max (defaults to 0 to max-int) |

#### `random` — Random Number Generator

| Property | Details |
|----------|---------|
| **Arguments** | `random [range]` — int arg: output 0 to (range−1). Float arg: output 0.0 to range inclusive |
| **Inlets** | 2: (0) bang to generate; (1) range |
| **Outlets** | 1: random value |
| **No argument** | Always outputs 0 |
| **Messages** | `seed [value]` — set seed for reproducible sequences |
| **Common mistakes** | Int arg `random 10` = range 0–9, NOT 0–10. Float arg `random 10.` = range 0.0–10.0. No arg = always 0 |

#### `delay` — Single Bang Delay

| Property | Details |
|----------|---------|
| **Arguments** | `delay [time-ms]` — optional |
| **Inlets** | 2: (0) bang to start delay; (1) delay time in ms |
| **Outlets** | 1: bang after delay |
| **Critical rule** | Only delays ONE bang at a time. A new bang cancels and replaces any pending delayed bang |
| **Messages** | `stop` — cancel pending bang |
| **Common mistakes** | Expecting multiple pending bangs (use `pipe` for that). Sending int/float instead of bang |

#### `pipe` — Multi-Message Delay

| Property | Details |
|----------|---------|
| **Arguments** | `pipe [types...] [delay-ms]` — types define inlet/outlet count and types |
| **Inlets** | N+1: one per data type + rightmost for delay time |
| **Outlets** | N: one per data type |
| **Behavior** | Unlike `delay`, supports multiple pending messages simultaneously |
| **Messages** | `flush` — immediately output all pending messages. `clear` — discard all pending |
| **Common mistakes** | Confusing with `delay` (which only holds one bang). Forgetting that rightmost inlet sets delay time |

### 3.8 Logic & Routing

#### `trigger` (alias `t`) — Ordered Multi-Output

| Property | Details |
|----------|---------|
| **Arguments** | `t [type-specs...]` — one outlet per arg. Types: `b`=bang, `i`=int, `f`=float, `l`=list, `s`=symbol, or constant values |
| **Inlets** | 1: any message |
| **Outlets** | N: one per argument, fires **right to left** |
| **Hot inlets** | 0 |
| **Type conversion** | Non-numeric input → 0 for `i`/`f` outlets. Any input → bang for `b` outlets |
| **Common mistakes** | Forgetting right-to-left order. Using `t` with only one outlet (pointless) |

#### `select` (alias `sel`) — Match and Route

| Property | Details |
|----------|---------|
| **Arguments** | `sel [values...]` — one outlet per match value + reject outlet |
| **Inlets** | 1–2: (0) value to test; (1) optional — set match value (only with single-arg `sel`) |
| **Outlets** | N+1: one bang outlet per match value + rightmost passes non-matching values |
| **Float matching** | OFF by default. Requires `matchfloat 1` attribute to match float values |
| **Duplicate args** | Only the leftmost matching outlet fires |
| **Common mistakes** | Expecting float matching to work without `matchfloat 1`. Forgetting the reject (rightmost) outlet exists |

#### `route` — Selector-Based Router

| Property | Details |
|----------|---------|
| **Arguments** | `route [selectors...]` — one outlet per selector + unmatched outlet |
| **Inlets** | 1: incoming message |
| **Outlets** | N+1: one per selector + rightmost passes unmatched messages intact |
| **Critical rule** | `route` STRIPS the first element (selector) on match. `pitch 440` → outlet outputs `440` (not `pitch 440`) |
| **Single-element match** | If the matched message has only the selector and nothing else, outputs bang |
| **Common mistakes** | Expecting the full message on output (selector is stripped). Confusing with `select` (which outputs bang, not the remainder) |

#### `gate` — Output Selector

| Property | Details |
|----------|---------|
| **Arguments** | `gate [num-outlets]` — default 1 |
| **Inlets** | 2: (0) selector — int selects which outlet (1-indexed); (1) input to route |
| **Outlets** | N: one per argument value |
| **Selector values** | 0 = closed (nothing passes). Negative = leftmost outlet. Exceeds range = rightmost |
| **Messages** | `next` — cycle to next outlet |
| **Common mistakes** | 1-indexed (not 0-indexed). Inlet 0 is selector, inlet 1 is data — reversed from what you might expect |

#### `switch` — Input Selector

| Property | Details |
|----------|---------|
| **Arguments** | `switch [num-inlets]` — default 1 |
| **Inlets** | N+1: (0) selector — int selects which inlet to pass; (1..N) inputs |
| **Outlets** | 1: selected input passes through |
| **Selector values** | 0 = closed. Negative → absolute value. `next` cycles inlets |
| **Common mistakes** | Confusing with `gate` (which is output selector). Inlet 0 is selector, not data |

#### `change` — Duplicate Filter

| Property | Details |
|----------|---------|
| **Arguments** | `change [initial-value]` — optional |
| **Inlets** | 1: value to filter |
| **Outlets** | 3: (0) value, only when different from previous; (1) bang on 0→nonzero transition; (2) bang on nonzero→0 transition |
| **Modes** | Default: output on any change. `+` mode: only output increases. `-` mode: only output decreases |
| **Common mistakes** | Expecting it to filter lists (only works on single values). Forgetting the transition outlets (1 and 2) |

#### `send` / `receive` (aliases `s` / `r`) — Wireless Routing

| Property | Details |
|----------|---------|
| **Arguments** | `send [name]` / `receive [name]` — required name argument |
| **send inlets** | 1: any message to broadcast |
| **send outlets** | 0 |
| **receive inlets** | 0 |
| **receive outlets** | 1: received message |
| **Critical rule** | Multiple `receive` objects with the same name: all fire, but in non-deterministic order |
| **Scoping** | `---` prefix for Max for Live unique scoping (e.g., `s ---myvar`) |
| **Common mistakes** | Relying on order when multiple `receive` objects share a name. Name typos cause silent failure |

#### `value` (alias `v`) — Global Named Storage

| Property | Details |
|----------|---------|
| **Arguments** | `value [name]` — required name argument |
| **Inlets** | 1: bang to read, any message to write |
| **Outlets** | 1: stored value (on bang or after write) |
| **Scope** | Global — shared across ALL open patches in the session |
| **Uninitialized** | Outputs empty (no value) until first write |
| **Common mistakes** | Forgetting global scope — modifying in one patch affects all others. Name collisions between unrelated patches |

### 3.9 Data Objects

#### `pack` — Build Lists

| Property | Details |
|----------|---------|
| **Arguments** | `pack [type-defaults...]` — one inlet per arg. `0`=int, `0.`=float, `symbol`=symbol |
| **Inlets** | N: one per argument. Inlet 0 is hot, rest are cold |
| **Outlets** | 1: list output |
| **Hot inlets** | 0 only |
| **Messages** | `set [values...]` — store values without triggering output |
| **Common mistakes** | Forgetting only inlet 0 is hot — setting cold inlets doesn't produce output. Int args = int inlets (truncate floats) |

#### `scale` — Range Mapping

| Property | Details |
|----------|---------|
| **Arguments** | `scale [inLow] [inHigh] [outLow] [outHigh] [exp]` — exp optional (default 1.0 = linear) |
| **Inlets** | 6: (0) input value — hot; (1) inLow; (2) inHigh; (3) outLow; (4) outHigh; (5) exponent |
| **Outlets** | 1: mapped value |
| **Hot inlets** | 0 |
| **Int vs float** | All-int args = int mode (truncates output). Any float arg = float mode |
| **Input range** | Input is NOT clipped to inLow–inHigh. Out-of-range input produces out-of-range output |
| **Common mistakes** | `scale 0 127 0 1` (int mode) outputs only 0 or 1. Use `scale 0 127 0. 1.` for float output. `inLow == inHigh` = division by zero |

### 3.10 Conversion Objects

#### `mtof` — MIDI Note to Frequency

| Property | Details |
|----------|---------|
| **Arguments** | None (or `mtof [base-freq]` to set A4 tuning) |
| **Inlets** | 1: MIDI note number (int or float) |
| **Outlets** | 1: frequency in Hz (float) |
| **Formula** | Equal temperament: `freq = base * 2^((note - 69) / 12)`, base default 440 Hz |
| **Common mistakes** | Forgetting to use this before sending MIDI to oscillators. MIDI 60 ≠ 60 Hz (it's 261.6 Hz) |

#### `sig~` — Constant Signal Generator

| Property | Details |
|----------|---------|
| **Arguments** | `sig~ [value]` — optional initial value, default 0.0 |
| **Inlets** | 1: float/int to convert to signal |
| **Outlets** | 1: constant signal at the input value |
| **No smoothing** | Value jumps instantly. Use `line~` for ramped transitions |
| **SIAI** | With Scheduler in Audio Interrupt enabled, updates are sample-accurate |

#### `snapshot~` — Signal to Float Sampler

| Property | Details |
|----------|---------|
| **Arguments** | `snapshot~ [interval-ms]` — 0 = bang-only mode |
| **Inlets** | 1: signal input (also accepts bang to sample immediately) |
| **Outlets** | 1: float value |
| **Modes** | Non-zero interval: auto-samples at that rate. Zero interval: only samples when banged |

### 3.11 UI Objects

| Object | Inlets | Outlets | Output Type | Default Range | Notes |
|--------|--------|---------|-------------|---------------|-------|
| `number` | 1 | 1 | int | Full int range | Truncates float input |
| `flonum` | 1 | 1 | float | Full float range | Displays/outputs floats |
| `button` | 1 | 1 | bang | N/A | Any input → bang out |
| `toggle` | 1 | 1 | int (0 or 1) | 0–1 | Non-zero input → 1. Bang toggles |
| `dial` | 1 | 1 | int | 0–127 | Circular knob |
| `slider` | 1 | 1 | int | 0–127 | Vertical or horizontal fader |
| `kslider` | 1 | 2 | int | 0–127 each | (0) pitch, (1) velocity. Key-up = velocity 0 |
| `message` | 1 | 1 | varies | N/A | Content determines type. Click or bang to output |
| `comment` | 0 | 0 | N/A | N/A | Display only — no inlets, no outlets |
| `loadbang` | 0 | 1 | bang | N/A | Fires once when patch loads (after connections established) |

### 3.12 Math Objects (Control Rate)

| Object | Arguments | Inlets | Outlets | Int/Float Mode | Notes |
|--------|-----------|--------|---------|----------------|-------|
| `+` | `+ [value]` | 2 | 1 | Arg type determines | Hot inlet 0, cold inlet 1 |
| `-` | `- [value]` | 2 | 1 | Arg type determines | inlet 0 − inlet 1 |
| `*` | `* [value]` | 2 | 1 | Arg type determines | Hot inlet 0, cold inlet 1 |
| `/` | `/ [value]` | 2 | 1 | Arg type determines | inlet 0 / inlet 1. Division by zero → 0 |
| `%` | `% [value]` | 2 | 1 | Int only | Modulo. `% 0` → 0 |
| `>` | `> [value]` | 2 | 1 | Int (0 or 1) | Comparison. Also `<`, `>=`, `<=`, `==`, `!=` |

**Critical: use decimal point for float output.** `/ 127` = int division (output always 0 for inputs 0–126). `/ 127.` = float division (output 0.0–1.0).

### 3.13 FFT & Spectral Objects

#### `fft~` — Fast Fourier Transform

| Property | Details |
|----------|---------|
| **Arguments** | `fft~ [size] [hop] [options]` |
| **Inlets** | 2: (0) signal (real); (1) signal (imaginary, usually 0) |
| **Outlets** | 3: (0) real part; (1) imaginary part; (2) sync signal (bang per frame) |
| **Notes** | Size must be power of 2. Used with `cartopol~`, `poltocar~` for magnitude/phase processing |

#### `cartopol~` — Cartesian to Polar Conversion

| Property | Details |
|----------|---------|
| **Arguments** | None |
| **Inlets** | 2: (0) real; (1) imaginary |
| **Outlets** | 2: (0) magnitude; (1) phase |
| **Notes** | Typically placed after `fft~` for spectral magnitude/phase manipulation |

### 3.14 Jitter Objects (Matrix/Visual)

#### `jit.matrix` — Named Matrix Data

| Property | Details |
|----------|---------|
| **Arguments** | `jit.matrix [name] [planes] [type] [dim1] [dim2]` |
| **Notes** | Named data container for video/matrix processing. Passed by reference name |

#### `jit.poke~` — Audio-Rate Matrix Writer

| Property | Details |
|----------|---------|
| **Arguments** | `jit.poke~ [matrix-name] [plane]` |
| **Inlets** | 3: (0) signal (value); (1) signal (x position); (2) signal (y position, if 2D) |
| **Notes** | Writes audio signals directly into Jitter matrix cells at audio rate |

#### `jit.pwindow` — Matrix Display Window

| Property | Details |
|----------|---------|
| **Arguments** | None (size set via attributes) |
| **Inlets** | 1: jit_matrix name |
| **Notes** | Displays matrix content in a small embedded window |

### 3.15 File Playback

#### `sfplay~` — Sound File Player

| Property | Details |
|----------|---------|
| **Arguments** | `sfplay~ [channels]` — number of output channels, default 1 |
| **Inlets** | 1: messages (`open`, `1`/`0` for play/stop, `preload`, `loop`) |
| **Outlets** | N+1: (0..N-1) signal outputs per channel; (N) bang on file end |
| **Messages** | `open` — open file dialog. `1` — play. `0` — stop. `loop 1` — enable looping. `preload [cue] [file]` — load to cue point |

---

## Level 4: Graph Rules (Connections Between Objects)

These rules govern how objects connect to each other — the patch cord topology.

### 4.1 Signal Chain Continuity

**Rule 4.1a: Signal-rate chains must be continuous.** An audio signal path must be `~` objects all the way from source to `ezdac~`. If a non-`~` object appears in the middle of a signal chain, the audio stream is broken.

```
LEGAL:   cycle~ → lores~ → *~ → clip~ → ezdac~
ILLEGAL: cycle~ → scale → *~ → ezdac~
                   ^^^^^ control-rate object breaks the audio chain
```

**Rule 4.1b: No control objects in audio chains.** Even if a control object accepts number input and produces number output, inserting it between two `~` objects breaks the signal stream. The signal becomes a single float, losing continuous audio.

### 4.2 Outlet-to-Inlet Type Compatibility

**Rule 4.2a: Signal outlets connect to signal inlets.**

| Source outlet type | Valid destination inlet types |
|-------------------|------------------------------|
| `signal` | Signal inlets on `~` objects, or hybrid inlets |
| `""` (empty = any message) | Message inlets on any object |
| `bang` | Message inlets that respond to bang |
| `int` / `float` / `list` | Message inlets that accept the respective type |

**Rule 4.2b: Multiple message types can feed the same inlet.** Most inlets accept multiple types. A `number` box inlet accepts int, float, and bang. Type errors are semantic mismatches (wrong behavior), not hard failures.

**Rule 4.2c: Multiple cords into one inlet — summing vs last-wins.**
- **Signal inlets:** Multiple signal cords summed. `osc1~ + osc2~ → same inlet = sum`.
- **Message inlets:** Last-arrived message wins. If two sources fire simultaneously, right-to-left execution order determines "last."

### 4.3 Graph Connectivity

**Rule 4.3a: Every audio chain must reach `ezdac~` (or `dac~`).** Orphaned audio chains produce no sound but the DSP still runs, wasting CPU silently.

```
LEGAL:   cycle~ → lores~ → *~ → ezdac~        (sound comes out)
ILLEGAL: cycle~ → lores~ → *~                   (orphaned — silent, wastes CPU)
```

**Rule 4.3b: Unconnected signal inlets receive 0.0.**
- `*~` with unconnected inlet 1 → multiplies by 0 → silence
- `+~` with unconnected inlet 1 → adds 0 → passthrough
- `lores~` with unconnected inlet 0 → no input → silence

### 4.4 Feedback Loops

**Rule 4.4a: Signal feedback requires `tapin~`/`tapout~`.** Direct signal-rate feedback loops cause Max to report an error and disable DSP.

```
LEGAL:   tapin~ → tapout~ → *~ 0.7 → +~ → tapin~    (feedback delay with decay)
ILLEGAL: lores~ outlet → lores~ inlet                   (direct loop — DSP error)
```

**Rule 4.4b: Message feedback requires `delay` or `deferlow`.** Direct message loops cause stack overflow. Max disables the offending connection. Break the loop with `delay`, `pipe`, or `deferlow`.

**Rule 4.4c: `tapin~` outlet → `tapout~` inlet is special.** This connection shares delay buffer memory — it is not a standard signal connection. Do not route `tapin~` output to any other object.

### 4.5 Patch Cord Types

Max has six patch cord types, distinguished visually and functionally:

| Cord Type | Appearance | Carries |
|-----------|-----------|---------|
| Event (message) | Thin gray | int, float, bang, symbol, list |
| Signal (audio) | Thick yellow-green striped | Continuous audio stream |
| MC (multichannel) | Thick multi-colored striped | Multiple audio channels in one cord |
| Jitter matrix | Thick green-yellow | Matrix name reference |
| GL texture | Thick green | Texture name reference |
| GL geometry | Thick purple | Geometry name reference |

**Rule 4.5a: Cord type is determined by the outlet type.** You cannot force a cord type — it's automatic based on what the outlet produces.

### 4.6 Multiple Connections

**Rule 4.6a: Any outlet can connect to multiple inlets.** Fan-out is always allowed.

**Rule 4.6b: Any inlet can receive from multiple outlets.** For signals, they sum. For messages, last-wins.

**Rule 4.6c: Cords can be disabled without deleting.** In Max, Cmd/Ctrl-click on a cord disables it (grayed out). MaxPy does not support disabled cords.

---

## Level 5: Execution Order & Scheduling Rules

These rules govern when and in what order objects fire — the temporal behavior of a patch.

### 5.1 Hot vs Cold Inlets

**Rule 5.1a: Only inlet 0 (leftmost) is "hot" — it triggers computation.** Other inlets are "cold" — they store values silently until the hot inlet fires.

```
+ object:  inlet 0 (hot) — receiving a number triggers addition and output
           inlet 1 (cold) — receiving a number stores it, no output yet
```

**Rule 5.1b: Always set cold inlets BEFORE sending to the hot inlet.** If the hot inlet fires before cold inlets are updated, the object uses stale values. Use `trigger` to enforce this order.

**Rule 5.1c: Exceptions exist.** Some objects have multiple hot inlets or non-standard behavior:
- `gate` inlet 0 (selector) can trigger rerouting
- `select` inlet 0 triggers matching
- Most `~` objects process continuously (hot/cold is a control-rate concept)

### 5.2 Right-to-Left, Depth-First Evaluation

**Rule 5.2a: When one outlet connects to multiple inlets, messages fire right to left.** The rightmost connection receives the message first.

**Rule 5.2b: Evaluation is depth-first.** Each path is followed to its terminal before the next connection from the same outlet fires. This means a message travels all the way down a chain before sibling branches execute.

```
outlet → A (rightmost, fires 1st) → A's chain completes fully
       → B (middle, fires 2nd) → B's chain completes fully
       → C (leftmost, fires 3rd) → C's chain completes fully
```

**Rule 5.2c: This ordering is determined by connection creation order, NOT visual position.** In MaxPy, the order you list connections in `patch.connect()` determines firing order. In Max's GUI, the order you draw cords determines it. Visual left/right positioning is unreliable.

### 5.3 trigger for Explicit Ordering

**Rule 5.3a: Use `trigger` (`t`) to guarantee firing order.** `trigger` outputs right-to-left from its outlet list, making order explicit and readable.

```
number → t f b → outlet 0 (float, fires second) → left inlet of *
               → outlet 1 (bang, fires first)  → message 10 → right inlet of *
```

This guarantees the multiplier (cold inlet) is set before the value arrives at the hot inlet.

**Rule 5.3b: Every fan-out to the same object should use `trigger`.** If one value needs to reach both the hot and cold inlets of a single object, always use `trigger` — never rely on implicit ordering.

### 5.4 Scheduler Threads

Max has two execution threads:

| Thread | Priority | Handles | Timing |
|--------|----------|---------|--------|
| **High-priority** | Timing-critical | `metro`, `delay`, MIDI input, `clocker`, `timepoint` | Precise scheduling |
| **Low-priority** | Background | UI updates, file I/O, `print`, drawing, `jit.window` refresh | When CPU available |

**Rule 5.4a: High-priority operations should be fast.** Expensive computation in the high-priority thread delays all timing-critical events (MIDI, audio sync, metro ticks).

**Rule 5.4b: UI-bound operations always run low-priority.** Number boxes, sliders, `jit.pwindow`, `print` — these update on the low-priority thread regardless of what triggered them.

### 5.5 Overdrive

**Rule 5.5a: Overdrive enables parallel high/low priority threads.** When Overdrive is ON (default in most setups), the high-priority scheduler runs on its own thread, separate from the UI.

**Rule 5.5b: Disable Overdrive for debugging.** With Overdrive OFF, everything runs on one thread, making execution order deterministic and easier to trace.

**Rule 5.5c: Enable Overdrive for MIDI and audio performance.** Without it, UI operations can delay MIDI and timing events.

### 5.6 Scheduler in Audio Interrupt (SIAI)

**Rule 5.6a: SIAI couples the scheduler to the audio processing thread.** When enabled, scheduled events (`metro`, `delay`, etc.) execute at sample-accurate timing within the audio callback.

**Rule 5.6b: SIAI improves event-to-audio synchronization.** `sig~` updates become sample-accurate. Envelope triggers align precisely with audio.

**Rule 5.6c: SIAI makes expensive scheduler operations cause audio dropouts.** Any slow operation in the scheduler path now blocks audio processing. Use `deferlow` for heavy computation.

### 5.7 defer and deferlow

**Rule 5.7a: `defer` moves execution to the front of the low-priority queue.** The deferred message may execute before previously queued low-priority events — potentially reordering messages.

**Rule 5.7b: `deferlow` moves execution to the back of the low-priority queue.** Always defers, preserves order with respect to other low-priority events. Preferred for thread-safety.

**Rule 5.7c: Use `deferlow` to break feedback loops.** Inserting `deferlow` in a message loop breaks the immediate recursion by deferring execution to the next low-priority pass.

### 5.8 Stack Overflow

**Rule 5.8a: Infinite message loops cause stack overflow.** If object A triggers B which triggers A (directly or through a chain), Max detects the recursion and disables the offending connections.

**Rule 5.8b: Fix message loops with `delay`, `pipe`, or `deferlow`.** Any object that introduces a time break or thread change prevents stack overflow.

### 5.9 Event Backlog

**Rule 5.9a: High-frequency generators feeding low-priority consumers cause queue overflow.** Example: `metro 1` (1000 bangs/sec) feeding a `print` object floods the low-priority queue.

**Rule 5.9b: Use `speedlim` or `qlim` to throttle.** `speedlim 50` limits throughput to one message per 50ms. `qlim 50` similar but only outputs the most recent value.

### 5.10 Automatic Priority Demotion

Certain operations always run on the low-priority thread regardless of what triggers them:

- `buffer~` file loading (`read` message)
- All drawing/rendering operations
- File I/O (`filein`, `text`, `coll` file operations)
- Dialog boxes (`opendialog`, `savedialog`)
- `print` output

**Rule 5.10a: Do not expect synchronous completion of demoted operations.** After sending `read` to `buffer~`, the buffer is not immediately loaded — wait for the completion bang/callback.

---

## Level 6: Patcher Lifecycle Rules

These rules govern the order of events when a patch loads, initializes, and closes.

### 6.1 Initialization Phases

When a Max patch loads, initialization proceeds in this order:

| Phase | What Happens | Notes |
|-------|-------------|-------|
| 1. Object creation | All objects instantiated with their arguments | No connections yet |
| 2. Patchcord connection | All patch cords established | Objects can now route to each other |
| 3. Parameter initialization | `@`-attribute parameters set to saved values | Attribute order not guaranteed |
| 4. `pattr` restoration | `pattr`/`autopattr` restores saved state | After parameters |
| 5. `loadbang` / `loadmess` | `loadbang` sends bang; `loadmess` sends its stored message | After connections — safe for inter-object messaging |
| 6. `live.thisdevice` | Max for Live: sends bang when device is fully loaded | After loadbang |
| 7. Window activation | Patcher window becomes active | UI now visible |
| 8. `patcherargs` | `patcherargs` in subpatchers outputs abstraction arguments | Deferred — may arrive after loadbang |
| 9. DSP start | `dspstate~` reports 1; audio processing begins | Only if audio is on |

### 6.2 Critical Ordering Constraints

**Rule 6.2a: Messages during object creation cannot route correctly.** Connections don't exist yet in Phase 1. Any object that tries to send a message at creation time will fail silently.

**Rule 6.2b: `loadbang` fires after connections are established (Phase 5).** This means `loadbang` → `message` → target object works correctly — the connections exist.

**Rule 6.2c: `patcherargs` output is deferred.** It may arrive after `loadbang` has already fired. Do not rely on `patcherargs` values being available during `loadbang`-triggered initialization chains.

### 6.3 Subpatcher Ordering

**Rule 6.3a: Subpatchers initialize before their parents within each phase.** Child objects are created before parent-level objects. Child `loadbang` fires before parent `loadbang`.

**Rule 6.3b: Sibling subpatcher order is NOT guaranteed.** If a parent patch contains two subpatchers A and B, the order of their `loadbang` execution is undefined.

**Rule 6.3c: `bpatcher` follows the same rules as subpatchers.** Embedded patchers initialize their contents before the parent continues.

### 6.4 Closing & Cleanup

**Rule 6.4a: `closebang` fires when the patcher window closes.** Use for cleanup that should happen when the window is dismissed (but the patch may still be in memory).

**Rule 6.4b: `freebang` fires when the patch is deallocated.** This happens when the patch is truly removed from memory — later than `closebang`. Use for final resource cleanup.

**Rule 6.4c: Children close before parents.** Subpatcher `closebang`/`freebang` fires before the parent patcher's.

### 6.5 loadbang Reliability

**Rule 6.5a: `loadbang` is the standard way to set initial state.** It fires once, after connections are formed, before the user interacts. Use it to send default values to number boxes, set initial toggle states, start metros, etc.

**Rule 6.5b: `loadbang` does NOT fire when a patch is loaded into `poly~`.** Use `thispoly~` or `loadmess` for poly~ voice initialization.

**Rule 6.5c: `loadmess` fires at the same time as `loadbang` but sends a specific message.** `loadmess 440` sends `440` on load — equivalent to `loadbang → message 440` but in one object.

---

## Summary Tables

### Object Quick-Reference Table

| Object | Inlets | Outlets | Hot Inlets | Args Required? | Signal Rate? |
|--------|--------|---------|------------|---------------|-------------|
| `cycle~` | 2 | 1 | 0 | No (default 0 Hz) | Yes |
| `saw~` | 2 | 1 | 0 | No (default 0 Hz) | Yes |
| `noise~` | 0 | 1 | — | No | Yes |
| `lores~` | 3 | 1 | 0 | No | Yes |
| `svf~` | 3 | 4 | 0 | No | Yes |
| `line~` | 2 | 2–3 | 0 | No | Yes |
| `*~` | 2 | 1 | — | No (default 0) | Yes |
| `+~` | 2 | 1 | — | No (default 0) | Yes |
| `-~` | 2 | 1 | — | No (default 0) | Yes |
| `clip~` | 3 | 1 | — | No (default 0, 0) | Yes |
| `tanh~` | 1 | 1 | — | No | Yes |
| `tapin~` | 2 | 1 | — | Practical (default 100ms) | Yes |
| `tapout~` | 1 | N | — | Yes (delay times) | Yes |
| `ezdac~` | 2 | 0 | — | No | Yes |
| `fft~` | 2 | 3 | — | Practical (size) | Yes |
| `cartopol~` | 2 | 2 | — | No | Yes |
| `sig~` | 1 | 1 | 0 | No | Yes |
| `snapshot~` | 1 | 1 | 0 | Practical (interval) | Hybrid |
| `sfplay~` | 1 | N+1 | 0 | Practical (channels) | Yes |
| `jit.poke~` | 3 | 0 | — | Yes (matrix, plane) | Yes |
| `metro` | 2 | 1 | 0 | Practical (interval) | No |
| `counter` | 5 | 4 | 0 | No | No |
| `random` | 2 | 1 | 0 | Practical (range) | No |
| `delay` | 2 | 1 | 0 | No | No |
| `pipe` | N+1 | N | 0 | Yes (types + time) | No |
| `trigger` / `t` | 1 | N | 0 | Yes (type specs) | No |
| `select` / `sel` | 1–2 | N+1 | 0 | Yes (match values) | No |
| `route` | 1 | N+1 | 0 | Yes (selectors) | No |
| `gate` | 2 | N | 0 | Practical (num outlets) | No |
| `switch` | N+1 | 1 | 0 | Practical (num inlets) | No |
| `change` | 1 | 3 | 0 | No | No |
| `send` / `s` | 1 | 0 | 0 | Yes (name) | No |
| `receive` / `r` | 0 | 1 | — | Yes (name) | No |
| `value` / `v` | 1 | 1 | 0 | Yes (name) | No |
| `pack` | N | 1 | 0 | Yes (type defaults) | No |
| `scale` | 6 | 1 | 0 | Practical (ranges) | No |
| `mtof` | 1 | 1 | 0 | No | No |
| `number` | 1 | 1 | 0 | No | No |
| `flonum` | 1 | 1 | 0 | No | No |
| `button` | 1 | 1 | 0 | No | No |
| `toggle` | 1 | 1 | 0 | No | No |
| `dial` | 1 | 1 | 0 | No | No |
| `slider` | 1 | 1 | 0 | No | No |
| `kslider` | 1 | 2 | 0 | No | No |
| `message` | 1 | 1 | 0 | Practical (content) | No |
| `comment` | 0 | 0 | — | No | No |
| `loadbang` | 0 | 1 | — | No | No |
| `+` / `-` / `*` / `/` | 2 | 1 | 0 | No | No |
| `>` / `<` / `==` | 2 | 1 | 0 | No | No |
| `jit.matrix` | 1 | 1 | 0 | Yes (name, specs) | No |
| `jit.pwindow` | 1 | 0 | 0 | No | No |

### Common Conversion Chains

| From | To | Chain | Notes |
|------|-----|-------|-------|
| MIDI note | Hz | `mtof` | Equal temperament. A4=440 |
| Hz | MIDI note | `ftom` | Inverse of mtof |
| Linear amplitude | dB | `atodb` | 1.0 → 0 dB |
| dB | Linear amplitude | `dbtoa` | 0 dB → 1.0 |
| Control int/float | Signal | `sig~` | No smoothing — instant jump |
| Control int/float | Signal (smooth) | `line~` | Needs target-time pair (e.g., `0.5 10`) |
| Signal | Control float | `snapshot~` | Needs interval or bang |
| 0–127 | 0.0–1.0 | `/ 127.` | Note the decimal point (float mode) |
| 0–127 | Custom range | `scale 0 127 outLow. outHigh.` | Note decimal points |
| MIDI note | Oscillator freq | `mtof → sig~ → cycle~` (or `saw~`, etc.) | Full MIDI-to-sound chain |
| MIDI note | Oscillator freq (stepped) | `mtof → cycle~` | Works but stepped (zipper noise) |
| Keyboard velocity | Envelope gate | `kslider outlet 1 → > 0 → select 1 0 → messages → line~` | Velocity > 0 = note on |

### Violation Severity Matrix

| Category | Violation | Severity | Max Behavior |
|----------|-----------|----------|-------------|
| **Data type** | Float into int-expecting inlet | Low | Silent truncation |
| **Data type** | Symbol into number inlet | Low | Silently ignored — no output |
| **Data type** | All-int args for float-range output | Medium | Output truncated — `scale 0 127 0 1` always outputs 0 or 1 |
| **Signal rate** | Control value into signal inlet (no `sig~`) | Medium | Works but stepped — zipper noise |
| **Signal rate** | Signal chain broken by control object | High | Audio stream stops at that point |
| **Signal rate** | Signal outlet to control-only inlet | Medium | Silently ignored — control object gets nothing |
| **Object args** | Missing required argument | Medium-High | Object may have 0 inlets/outlets or wrong behavior |
| **Object args** | Wrong argument type | Medium | Silent coercion or unexpected configuration |
| **Parameter range** | Filter resonance > 1.0 | High | Self-oscillation, feedback, dangerously loud |
| **Parameter range** | Frequency at 0 or negative | Medium | Silence or unexpected behavior |
| **Parameter range** | Gain > 1.0 at `ezdac~` | Medium-High | Clipping, distortion, potential speaker damage |
| **Parameter range** | `metro` interval < 1ms | High | Scheduler flood — can hang Max |
| **Connectivity** | Audio chain doesn't reach `ezdac~` | High | Complete silence, wasted CPU |
| **Connectivity** | Hot inlet never triggered | High | Object never fires — dead path |
| **Connectivity** | `*~` inlet 1 unconnected | High | Multiplies by 0 — silence |
| **Connectivity** | `tapin~` outlet not connected to `tapout~` | High | No delay output; memory sharing broken |
| **Feedback** | Direct signal feedback loop | Critical | Max error + DSP disabled |
| **Feedback** | Direct message feedback loop | Critical | Stack overflow — connection disabled |
| **Execution order** | Cold inlet set after hot inlet | Medium | Uses stale value — wrong computation |
| **Execution order** | No `trigger` for fan-out to same object | Medium | Implicit ordering — fragile, may break |
| **Scheduling** | Expensive ops in high-priority thread | Medium | Timing jitter, delayed MIDI/metro |
| **Scheduling** | Expensive ops with SIAI enabled | High | Audio dropouts (buffer underrun) |
| **Scheduling** | High-frequency source → slow consumer | Medium | Queue overflow, UI freeze |
| **Lifecycle** | Depending on `patcherargs` during `loadbang` | Medium | Values not yet available — uses uninitialized state |
| **Lifecycle** | Messages during object creation (Phase 1) | High | Connections don't exist — messages lost |
| **Semantic** | MIDI note sent as frequency | Medium | Wrong pitch (off by a lot — MIDI 60 ≠ 60 Hz) |
| **Semantic** | Plain number sent to `line~` | Low | Instant jump instead of smooth ramp |
| **Semantic** | `select` with float input (no `matchfloat 1`) | Medium | Never matches — silent failure |
| **Semantic** | `route` output assumed to include selector | Medium | Selector is stripped — output is remainder only |
| **File path** | Referenced file doesn't exist | Medium | Empty buffer / missing subpatch — silent failure |

---

## What MaxPy (maxpylang) Does and Does NOT Enforce

| Rule | MaxPy Enforces? | Notes |
|------|----------------|-------|
| Object name recognition | Partial | Warns about unknown objects but still generates them |
| Inlet/outlet count | Yes | Refuses to connect to non-existent inlets |
| Signal rate matching | **No** | Allows control→signal connections without `sig~` |
| Value type matching | **No** | Allows any outlet→inlet connection regardless of type |
| Int vs float mode | **No** | No awareness of decimal-point argument significance |
| Parameter ranges | **No** | Accepts `lores~ 800 5.0` without warning |
| Graph connectivity | **No** | No reachability analysis — orphaned subgraphs are silent |
| Feedback detection | **No** | Allows direct loops that will crash DSP |
| Execution order | **No** | No hot/cold inlet awareness |
| Scheduling rules | **No** | No thread-safety or priority analysis |
| Lifecycle ordering | **No** | No initialization-phase awareness |
| Semantic correctness | **No** | No domain knowledge (MIDI vs Hz, ramp format, etc.) |

**Bottom line:** MaxPy is a structural generation tool. It ensures objects exist and connections reference valid inlets/outlets. Everything else — rate matching, type safety, parameter validity, graph completeness, execution order, scheduling, lifecycle, and semantic correctness — is the programmer's responsibility. This document is the reference for getting it right.
