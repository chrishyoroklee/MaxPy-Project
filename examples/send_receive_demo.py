"""
Send/Receive Modular Patch Demo
================================
Demonstrates Max's send and receive objects for "wireless" message routing.
The control section and audio section communicate entirely via named
send/receive pairs — no direct patch cords between them.

Send/receive pairs:
  - freq    : note frequency (from kslider -> mtof)
  - cutoff  : filter cutoff frequency
  - gate    : note on/off trigger (drives envelope)
  - volume  : master volume level

Usage in Max:
  1. Turn on ezdac~ (audio)
  2. Play notes on the kslider
  3. Adjust cutoff and volume controls
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# CONTROL SECTION (top) — sends values wirelessly
# ============================================================

patch.set_position(30, 30)
patch.place("comment === CONTROL SECTION (send) ===")[0]

# --- Pitch: kslider -> mtof -> send freq ---
patch.set_position(30, 70)
patch.place("comment Pitch")[0]

patch.set_position(30, 95)
kslider = patch.place("kslider")[0]

patch.set_position(30, 175)
mtof = patch.place("mtof")[0]

patch.set_position(30, 210)
freq_num = patch.place("flonum")[0]

patch.set_position(30, 245)
send_freq = patch.place("send freq")[0]

patch.connect(
    [kslider.outs[0], mtof.ins[0]],
    [mtof.outs[0], freq_num.ins[0]],
    [freq_num.outs[0], send_freq.ins[0]],
)

# --- Gate: kslider velocity -> envelope trigger -> send gate ---
patch.set_position(200, 95)
patch.place("comment Gate")[0]

patch.set_position(200, 175)
vel_toggle = patch.place("> 0")[0]

patch.set_position(200, 210)
sel = patch.place("select 1 0")[0]

patch.set_position(200, 245)
msg_attack = patch.place("message 1. 10")[0]

patch.set_position(320, 245)
msg_release = patch.place("message 0. 300")[0]

patch.set_position(200, 285)
send_gate = patch.place("send gate")[0]

patch.connect(
    [kslider.outs[1], vel_toggle.ins[0]],
    [vel_toggle.outs[0], sel.ins[0]],
    [sel.outs[0], msg_attack.ins[0]],
    [sel.outs[1], msg_release.ins[0]],
    [msg_attack.outs[0], send_gate.ins[0]],
    [msg_release.outs[0], send_gate.ins[0]],
)

# --- Cutoff control -> send cutoff ---
patch.set_position(400, 70)
patch.place("comment Filter Cutoff")[0]

patch.set_position(400, 95)
cutoff_num = patch.place("number")[0]

patch.set_position(400, 135)
send_cutoff = patch.place("send cutoff")[0]

# Loadbang -> default cutoff
patch.set_position(500, 30)
loadbang = patch.place("loadbang")[0]

patch.set_position(500, 70)
default_cutoff = patch.place("message 2000")[0]

patch.connect(
    [cutoff_num.outs[0], send_cutoff.ins[0]],
    [loadbang.outs[0], default_cutoff.ins[0]],
    [default_cutoff.outs[0], cutoff_num.ins[0]],
)

# --- Volume control -> send volume ---
patch.set_position(400, 180)
patch.place("comment Volume")[0]

patch.set_position(400, 205)
vol_dial = patch.place("dial")[0]

patch.set_position(400, 255)
vol_scale = patch.place("/ 127.")[0]

patch.set_position(400, 290)
send_volume = patch.place("send volume")[0]

# Default volume
patch.set_position(500, 180)
default_vol = patch.place("message 100")[0]

patch.connect(
    [vol_dial.outs[0], vol_scale.ins[0]],
    [vol_scale.outs[0], send_volume.ins[0]],
    [loadbang.outs[0], default_vol.ins[0]],
    [default_vol.outs[0], vol_dial.ins[0]],
)

# --- Divider ---
patch.set_position(30, 340)
patch.place("comment ─────────────── no patch cords cross this line ───────────────")[0]

# ============================================================
# AUDIO SECTION (bottom) — receives values wirelessly
# ============================================================

patch.set_position(30, 380)
patch.place("comment === AUDIO SECTION (receive) ===")[0]

# --- receive freq -> sig~ -> cycle~ ---
patch.set_position(30, 420)
recv_freq = patch.place("receive freq")[0]

patch.set_position(30, 455)
freq_sig = patch.place("sig~")[0]

patch.set_position(30, 490)
osc = patch.place("cycle~")[0]

patch.connect(
    [recv_freq.outs[0], freq_sig.ins[0]],
    [freq_sig.outs[0], osc.ins[0]],
)

# --- receive gate -> line~ (envelope) ---
patch.set_position(200, 420)
recv_gate = patch.place("receive gate")[0]

patch.set_position(200, 455)
line_env = patch.place("line~")[0]

patch.connect(
    [recv_gate.outs[0], line_env.ins[0]],
)

# --- receive cutoff -> lores~ ---
patch.set_position(350, 420)
recv_cutoff = patch.place("receive cutoff")[0]

patch.set_position(30, 530)
lores = patch.place("lores~ 2000 0.3")[0]

patch.connect(
    [osc.outs[0], lores.ins[0]],
    [recv_cutoff.outs[0], lores.ins[1]],
)

# --- Apply envelope ---
patch.set_position(30, 570)
env_vca = patch.place("*~")[0]

patch.connect(
    [lores.outs[0], env_vca.ins[0]],
    [line_env.outs[0], env_vca.ins[1]],
)

# --- receive volume -> master volume ---
patch.set_position(200, 530)
recv_volume = patch.place("receive volume")[0]

patch.set_position(200, 565)
vol_sig = patch.place("sig~")[0]

patch.set_position(30, 610)
master_vol = patch.place("*~")[0]

patch.connect(
    [recv_volume.outs[0], vol_sig.ins[0]],
    [env_vca.outs[0], master_vol.ins[0]],
    [vol_sig.outs[0], master_vol.ins[1]],
)

# --- Output: clip~ -> ezdac~ ---
patch.set_position(30, 650)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(30, 690)
dac = patch.place("ezdac~")[0]

patch.connect(
    [master_vol.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# Instructions
patch.set_position(30, 740)
patch.place("comment Play kslider - adjust cutoff and volume - all routing is wireless via send/receive")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/send_receive_demo.maxpat")
print("Saved: examples/send_receive_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
