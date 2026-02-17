"""
route — Message Router
=======================
The `route` object matches the first element of incoming messages and
sends the remainder out the corresponding outlet.  Unmatched messages
go out the rightmost outlet.

  route pitch velocity cc
    outlet 0: messages starting with "pitch" (remainder passed through)
    outlet 1: messages starting with "velocity"
    outlet 2: messages starting with "cc"
    outlet 3: everything else (unmatched)

This patch simulates a simple MIDI-like message stream and uses route
to split it into separate parameter paths.

Usage in Max:
  1. Click the message boxes to send tagged messages
  2. route splits them to the correct number box
  3. Unmatched messages appear in the "other" display
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === ROUTE: Message Router ===")[0]

# ============================================================
# INPUT MESSAGES: simulate tagged messages
# ============================================================

patch.set_position(30, 70)
patch.place("comment Click a message to send it into route:")[0]

patch.set_position(30, 100)
msg_pitch = patch.place("message pitch 60")[0]

patch.set_position(170, 100)
msg_vel = patch.place("message velocity 100")[0]

patch.set_position(330, 100)
msg_cc = patch.place("message cc 74 64")[0]

patch.set_position(480, 100)
msg_other = patch.place("message unknown hello")[0]

# ============================================================
# ROUTE: split by first element
# ============================================================

patch.set_position(30, 160)
route = patch.place("route pitch velocity cc")[0]

patch.connect(
    [msg_pitch.outs[0], route.ins[0]],
    [msg_vel.outs[0], route.ins[0]],
    [msg_cc.outs[0], route.ins[0]],
    [msg_other.outs[0], route.ins[0]],
)

# ============================================================
# OUTPUTS: one number box per route outlet
# ============================================================

# Pitch outlet
patch.set_position(30, 220)
patch.place("comment pitch")[0]

patch.set_position(30, 245)
pitch_num = patch.place("number")[0]

# Velocity outlet
patch.set_position(170, 220)
patch.place("comment velocity")[0]

patch.set_position(170, 245)
vel_num = patch.place("number")[0]

# CC outlet
patch.set_position(310, 220)
patch.place("comment cc")[0]

patch.set_position(310, 245)
cc_num = patch.place("number")[0]

# Unmatched outlet
patch.set_position(450, 220)
patch.place("comment other (unmatched)")[0]

patch.set_position(450, 245)
other_display = patch.place("number")[0]

patch.connect(
    [route.outs[0], pitch_num.ins[0]],
    [route.outs[1], vel_num.ins[0]],
    [route.outs[2], cc_num.ins[0]],
    [route.outs[3], other_display.ins[0]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 310)
patch.place("comment route strips the first word and sends the rest out the matching outlet")[0]

patch.set_position(30, 340)
patch.place("comment 'pitch 60' -> outlet 0 outputs 60 -- 'cc 74 64' -> outlet 2 outputs '74 64'")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/route_demo.maxpat")
print("Saved: examples/route_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
