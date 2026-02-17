# Patch Layout Guide: How to Generate Visually Organized Max Patches with MaxPy

MaxPy can produce clean, readable patches — or a tangled mess of overlapping objects and spaghetti cords. The difference comes down to a few layout rules.

---

## The Problem

When you use `patch.place()` without setting positions, MaxPy places objects using its default grid layout. Objects stack sequentially, and patch cords fly in every direction to reach their destinations. The result looks like this in Max:

- Objects pile up in a column or cluster in one corner
- Patch cords cross over each other and over unrelated objects
- You can't tell which section of the patch does what
- It's hard to trace a signal path visually

This is what happened in the early experiments (`warm_synth.py`, `drum_machine.py`) — the patches worked, but they were visually unreadable.

---

## The Fix: Manual Positioning with `set_position`

The single most important rule:

**Call `patch.set_position(x, y)` before every `patch.place()` call.**

```python
# Bad — objects land wherever MaxPy's grid puts them
osc = patch.place("cycle~")[0]
filter = patch.place("lores~")[0]
dac = patch.place("ezdac~")[0]

# Good — objects are placed exactly where you want them
patch.set_position(30, 200)
osc = patch.place("cycle~")[0]

patch.set_position(30, 240)
filter = patch.place("lores~")[0]

patch.set_position(30, 280)
dac = patch.place("ezdac~")[0]
```

`set_position(x, y)` sets the pixel coordinates for the next placed object. `x` is horizontal (left to right), `y` is vertical (top to bottom). These map directly to the `patching_rect` in the `.maxpat` JSON file.

---

## Layout Rules

### Rule 1: Top-to-bottom signal flow

Max patches read top to bottom. Inputs at the top, processing in the middle, outputs at the bottom. Match this with increasing `y` values.

```python
# Input
patch.set_position(30, 100)
input_obj = patch.place("kslider")[0]

# Processing
patch.set_position(30, 200)
filter_obj = patch.place("lores~")[0]

# Output
patch.set_position(30, 300)
dac = patch.place("ezdac~")[0]
```

### Rule 2: Use consistent vertical spacing

Pick a vertical step size and stick to it. 35-40px between objects in the same chain works well. Use larger gaps (60-80px) between logical sections.

```python
Y_STEP = 40        # within a chain
SECTION_GAP = 80   # between sections

# Chain 1
patch.set_position(30, 100)         # object A
patch.set_position(30, 100 + Y_STEP)   # object B (140)
patch.set_position(30, 100 + 2*Y_STEP) # object C (180)

# Chain 2 (new section)
patch.set_position(30, 180 + SECTION_GAP)  # object D (260)
```

### Rule 3: Parallel chains go side by side

When objects feed into different paths (e.g., multiple oscillators, separate parameter controls), place them at the same `y` but different `x` values.

```python
# Three oscillators at the same vertical level
patch.set_position(30, 200)
osc1 = patch.place("cycle~")[0]

patch.set_position(160, 200)
osc2 = patch.place("saw~")[0]

patch.set_position(290, 200)
osc3 = patch.place("rect~")[0]
```

Good column spacing is 130-170px depending on object width.

### Rule 4: Labels go directly above their objects

Place `comment` labels 20-25px above the object they describe, at the same `x` position.

```python
patch.set_position(30, 70)
patch.place("comment Filter Cutoff")[0]

patch.set_position(30, 95)
cutoff_num = patch.place("number")[0]
```

### Rule 5: Section headers mark logical boundaries

Use wide `comment` objects as visual dividers between patch sections. Give them a recognizable format.

```python
patch.set_position(30, 30)
patch.place("comment === CONTROL SECTION ===")[0]

# ... control objects ...

patch.set_position(30, 340)
patch.place("comment === AUDIO SECTION ===")[0]

# ... audio objects ...
```

### Rule 6: Defaults and loadbang go to the right

`loadbang` → `message` chains that set default values should sit to the right of the objects they initialize. This keeps them out of the main signal flow but visually associated.

```python
# Main object (left)
patch.set_position(30, 95)
freq_num = patch.place("number")[0]

# Default initializer (right)
patch.set_position(170, 70)
loadbang = patch.place("loadbang")[0]

patch.set_position(170, 95)
default_freq = patch.place("message 440")[0]
```

### Rule 7: Keep connected objects close together

The shorter the patch cord, the easier it is to read. If object A connects to object B, they should be adjacent — either vertically (A above B) or horizontally (A left of B, same `y`).

When you must connect distant objects, that's a sign you might want `send`/`receive` for wireless routing instead.

### Rule 8: Group connections by section

Instead of scattering `patch.connect()` calls throughout the code, group connections at the end of each logical section. This makes the code easier to read and matches how you'd think about wiring in Max.

```python
# Place all objects in section
patch.set_position(30, 100)
osc = patch.place("cycle~")[0]

patch.set_position(30, 140)
filter = patch.place("lores~")[0]

patch.set_position(30, 180)
vca = patch.place("*~")[0]

# Connect the section
patch.connect(
    [osc.outs[0], filter.ins[0]],
    [filter.outs[0], vca.ins[0]],
)
```

---

## Typical Patch Layout Template

Here's a standard layout skeleton that produces clean patches:

```
y=30    Section header comment
y=70    Label comments
y=95    Input objects (kslider, number, toggle)
y=135   Conversion objects (mtof, sig~)
y=175   Processing objects (cycle~, saw~)
y=220   Section header comment
y=250   More processing (lores~, *~)
y=300   Section header comment
y=330   Output controls (dial, volume)
y=380   Safety (clip~)
y=420   Output (ezdac~)
y=470   Instructions comment
```

With parallel columns:
```
x=30    Main signal path
x=170   Secondary controls / defaults
x=300   Third column if needed
x=450   Fourth column if needed
```

---

## Before and After

### Before (no positioning — `warm_synth.py`)
- All objects placed by MaxPy's auto-grid
- Objects clustered together with no logical grouping
- Patch cords cross and overlap
- Impossible to tell what section does what at a glance

### After (manual positioning — `effects_chain.py`, `examples/*.py`)
- Objects flow top to bottom matching signal flow
- Clear sections with header comments
- Labels directly above their objects
- Parallel controls in columns
- Defaults/loadbang pushed to the right
- Patch cords are short and mostly vertical (straight down)

---

## Common Mistakes

1. **Forgetting `set_position` for some objects** — One misplaced object creates a long diagonal cord that crosses everything. Be consistent: every `place()` gets a `set_position()`.

2. **Too tight spacing** — Objects overlap and cords become invisible. Use at least 35px vertical and 130px horizontal between objects.

3. **Too wide spacing** — If columns are 500px apart, cords become long horizontal lines. Keep related objects within 200px of each other.

4. **Mixing signal flow direction** — If most of your patch flows top-to-bottom but one connection goes bottom-to-top, it creates a confusing backward cord. Reorganize so everything flows downward, or use `send`/`receive` for feedback paths.

5. **Not grouping connections** — Scattered `patch.connect()` calls make it hard to verify wiring. Group them by section.
