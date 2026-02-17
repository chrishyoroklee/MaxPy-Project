"""
value — Named Global Variable
==============================
The `value` object stores a single value accessible by name from
anywhere in the patch.  One section writes to it, another reads from it.

  Writer: number box -> value my_param  (stores whatever you type)
  Reader: bang -> value my_param        (bang recalls the stored value)

Usage in Max:
  1. Type a number into the Writer number box — it stores into "my_param"
  2. Click the bang in the Reader section — it outputs the stored value
  3. Notice no patch cord connects the two sections
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === VALUE: Named Global Variable ===")[0]

# ============================================================
# WRITER SECTION: number -> value my_param
# ============================================================

patch.set_position(30, 70)
patch.place("comment --- Writer ---")[0]

patch.set_position(30, 95)
patch.place("comment Type a number to store:")[0]

patch.set_position(30, 120)
writer_num = patch.place("number")[0]

patch.set_position(30, 160)
val_write = patch.place("value my_param")[0]

patch.connect(
    [writer_num.outs[0], val_write.ins[0]],
)

# ============================================================
# READER SECTION: bang -> value my_param -> number
# ============================================================

patch.set_position(250, 70)
patch.place("comment --- Reader ---")[0]

patch.set_position(250, 95)
patch.place("comment Bang to recall stored value:")[0]

patch.set_position(250, 120)
reader_bang = patch.place("button")[0]

patch.set_position(250, 160)
val_read = patch.place("value my_param")[0]

patch.set_position(250, 200)
reader_num = patch.place("number")[0]

patch.connect(
    [reader_bang.outs[0], val_read.ins[0]],
    [val_read.outs[0], reader_num.ins[0]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 260)
patch.place("comment Both 'value my_param' objects share the same storage - no patch cord needed")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/value_demo.maxpat")
print("Saved: examples/value_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
