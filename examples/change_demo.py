"""
change — Filter Duplicate Values
=================================
The `change` object only passes a value through if it differs from the
previous one.  This patch uses a metro + random to generate numbers,
then shows how `change` filters out the repeats.

  metro 300 -> random 5 -> change -> number (only new values appear)
                       |
                       +-> number (all values, including repeats)

Usage in Max:
  1. Click the toggle to start the metro
  2. Watch the "before" number box show every value (with repeats)
  3. Watch the "after" number box show only when the value changes
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === CHANGE: Filter Duplicate Values ===")[0]

# ============================================================
# CLOCK: toggle -> metro -> random 5
# ============================================================

patch.set_position(30, 70)
patch.place("comment Start/Stop")[0]

patch.set_position(30, 95)
toggle = patch.place("toggle")[0]

patch.set_position(30, 130)
metro = patch.place("metro 300")[0]

patch.set_position(30, 170)
rng = patch.place("random 5")[0]

patch.connect(
    [toggle.outs[0], metro.ins[0]],
    [metro.outs[0], rng.ins[0]],
)

# ============================================================
# BEFORE CHANGE: shows all values (with repeats)
# ============================================================

patch.set_position(200, 170)
patch.place("comment Before change")[0]

patch.set_position(200, 195)
before_num = patch.place("number")[0]

patch.connect(
    [rng.outs[0], before_num.ins[0]],
)

# ============================================================
# AFTER CHANGE: only passes new values
# ============================================================

patch.set_position(30, 220)
change = patch.place("change")[0]

patch.set_position(30, 260)
patch.place("comment After change")[0]

patch.set_position(30, 285)
after_num = patch.place("number")[0]

patch.connect(
    [rng.outs[0], change.ins[0]],
    [change.outs[0], after_num.ins[0]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 340)
patch.place("comment Click toggle to start - compare the two number boxes")[0]

patch.set_position(30, 370)
patch.place("comment random 5 produces 0-4 so repeats are frequent - change filters them out")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/change_demo.maxpat")
print("Saved: examples/change_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
