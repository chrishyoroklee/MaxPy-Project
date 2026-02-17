"""
trigger — Right-to-Left Output with Type Conversion
=====================================================
The `trigger` (alias: t) object takes one input and fires multiple
outputs right-to-left, converting types as specified.

  trigger b f i  ->  outlet 2 (bang), outlet 1 (float), outlet 0 (int)
                     fires right-to-left: bang first, then float, then int

This patch shows the classic use: ensuring the right inlet of an
arithmetic object is set BEFORE the left inlet triggers computation.

  number -> trigger b f -> right outlet bangs a message
                        -> left outlet sends float to multiply

Usage in Max:
  1. Type a number into the input
  2. trigger ensures the multiplier is set before the value arrives
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === TRIGGER: Right-to-Left Execution Order ===")[0]

# ============================================================
# EXAMPLE 1: trigger b i — bang + integer output
# ============================================================

patch.set_position(30, 70)
patch.place("comment --- Example 1: Type Conversion ---")[0]

patch.set_position(30, 95)
patch.place("comment Input a float:")[0]

patch.set_position(30, 120)
input_float = patch.place("flonum")[0]

patch.set_position(30, 160)
trig1 = patch.place("trigger b i f")[0]

# bang output
patch.set_position(30, 210)
patch.place("comment bang")[0]

patch.set_position(30, 235)
bang_display = patch.place("button")[0]

# int output
patch.set_position(140, 210)
patch.place("comment int")[0]

patch.set_position(140, 235)
int_display = patch.place("number")[0]

# float output
patch.set_position(250, 210)
patch.place("comment float")[0]

patch.set_position(250, 235)
float_display = patch.place("flonum")[0]

patch.connect(
    [input_float.outs[0], trig1.ins[0]],
    [trig1.outs[0], bang_display.ins[0]],
    [trig1.outs[1], int_display.ins[0]],
    [trig1.outs[2], float_display.ins[0]],
)

# ============================================================
# EXAMPLE 2: Classic use — set right inlet before left
# ============================================================

patch.set_position(30, 300)
patch.place("comment --- Example 2: Correct Execution Order ---")[0]

patch.set_position(30, 330)
patch.place("comment Without trigger: right inlet might not be set yet")[0]

patch.set_position(30, 355)
patch.place("comment With trigger: right fires first then left")[0]

patch.set_position(30, 390)
input_val = patch.place("number")[0]

patch.set_position(30, 430)
trig2 = patch.place("trigger f b")[0]

# Right outlet (bang) -> message with multiplier
patch.set_position(170, 430)
mult_msg = patch.place("message 10")[0]

# Multiply
patch.set_position(30, 480)
multiply = patch.place("* 10")[0]

patch.set_position(30, 520)
patch.place("comment Result (input x 10):")[0]

patch.set_position(30, 545)
result = patch.place("number")[0]

patch.connect(
    [input_val.outs[0], trig2.ins[0]],
    [trig2.outs[0], multiply.ins[0]],
    [trig2.outs[1], mult_msg.ins[0]],
    [mult_msg.outs[0], multiply.ins[1]],
    [multiply.outs[0], result.ins[0]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 600)
patch.place("comment trigger fires outlets RIGHT to LEFT - guaranteeing execution order")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/trigger_demo.maxpat")
print("Saved: examples/trigger_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
