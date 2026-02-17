"""
Warm Synth (Organized Layout)
==============================
3 detuned saw oscillators through a low-pass filter with
velocity envelope and volume knob.

  kslider -> mtof -> sig~ -> 3x saw~ (center, -1Hz, +1Hz)
  velocity -> gate -> line~ envelope
  mix -> lores~ -> envelope VCA -> volume -> ezdac~

Usage in Max:
  1. Turn on ezdac~
  2. Turn up the volume dial
  3. Play notes on the kslider
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# KEYBOARD INPUT
# ============================================================

patch.set_position(30, 30)
patch.place("comment === KEYBOARD INPUT ===")[0]

# Pitch path: kslider -> mtof -> sig~
patch.set_position(30, 65)
patch.place("comment Pitch")[0]

patch.set_position(30, 90)
kslider = patch.place("kslider")[0]

patch.set_position(30, 170)
mtof = patch.place("mtof")[0]

patch.set_position(30, 205)
freq_sig = patch.place("sig~")[0]

patch.connect(
    [kslider.outs[0], mtof.ins[0]],
    [mtof.outs[0], freq_sig.ins[0]],
)

# ============================================================
# ENVELOPE (velocity -> gate -> line~)
# ============================================================

patch.set_position(250, 30)
patch.place("comment === ENVELOPE ===")[0]

patch.set_position(250, 65)
patch.place("comment Velocity gate")[0]

patch.set_position(250, 90)
vel_toggle = patch.place("> 0")[0]

patch.set_position(250, 125)
sel = patch.place("select 1 0")[0]

patch.set_position(250, 165)
msg_attack = patch.place("message 1. 10")[0]

patch.set_position(370, 165)
msg_release = patch.place("message 0. 300")[0]

patch.set_position(250, 205)
line_env = patch.place("line~")[0]

patch.connect(
    [kslider.outs[1], vel_toggle.ins[0]],
    [vel_toggle.outs[0], sel.ins[0]],
    [sel.outs[0], msg_attack.ins[0]],
    [sel.outs[1], msg_release.ins[0]],
    [msg_attack.outs[0], line_env.ins[0]],
    [msg_release.outs[0], line_env.ins[0]],
)

# ============================================================
# 3 DETUNED SAW OSCILLATORS
# ============================================================

patch.set_position(30, 260)
patch.place("comment === 3 DETUNED SAW OSCILLATORS ===")[0]

# Detune offsets
patch.set_position(30, 295)
patch.place("comment center")[0]

patch.set_position(130, 295)
patch.place("comment -1 Hz")[0]

patch.set_position(230, 295)
patch.place("comment +1 Hz")[0]

patch.set_position(130, 320)
detune_down = patch.place("-~ 1")[0]

patch.set_position(230, 320)
detune_up = patch.place("+~ 1")[0]

# Three oscillators side by side
patch.set_position(30, 360)
osc1 = patch.place("saw~")[0]

patch.set_position(130, 360)
osc2 = patch.place("saw~")[0]

patch.set_position(230, 360)
osc3 = patch.place("saw~")[0]

patch.connect(
    # Frequency -> center osc directly, detuned via +~/−~
    [freq_sig.outs[0], osc1.ins[0]],
    [freq_sig.outs[0], detune_down.ins[0]],
    [freq_sig.outs[0], detune_up.ins[0]],
    [detune_down.outs[0], osc2.ins[0]],
    [detune_up.outs[0], osc3.ins[0]],
)

# ============================================================
# MIX + FILTER
# ============================================================

patch.set_position(30, 415)
patch.place("comment === MIX + FILTER ===")[0]

patch.set_position(30, 445)
mix_gain = patch.place("*~ 0.33")[0]

patch.set_position(30, 485)
lpf = patch.place("lores~ 800 0.3")[0]

patch.connect(
    [osc1.outs[0], mix_gain.ins[0]],
    [osc2.outs[0], mix_gain.ins[0]],
    [osc3.outs[0], mix_gain.ins[0]],
    [mix_gain.outs[0], lpf.ins[0]],
)

# ============================================================
# ENVELOPE VCA + MASTER VOLUME + OUTPUT
# ============================================================

patch.set_position(30, 540)
patch.place("comment === OUTPUT ===")[0]

# Envelope VCA
patch.set_position(30, 570)
env_apply = patch.place("*~")[0]

# Volume control (to the right)
patch.set_position(200, 540)
patch.place("comment Volume")[0]

patch.set_position(200, 565)
vol_knob = patch.place("dial")[0]

patch.set_position(200, 615)
vol_scale = patch.place("/ 127.")[0]

patch.set_position(200, 650)
vol_sig = patch.place("sig~")[0]

# Master volume
patch.set_position(30, 650)
master_vol = patch.place("*~")[0]

# Safety + DAC
patch.set_position(30, 690)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(30, 730)
dac = patch.place("ezdac~")[0]

patch.connect(
    # Filter -> envelope VCA
    [lpf.outs[0], env_apply.ins[0]],
    [line_env.outs[0], env_apply.ins[1]],
    # Volume knob -> scale -> sig~
    [vol_knob.outs[0], vol_scale.ins[0]],
    [vol_scale.outs[0], vol_sig.ins[0]],
    # Envelope VCA -> master volume
    [env_apply.outs[0], master_vol.ins[0]],
    [vol_sig.outs[0], master_vol.ins[1]],
    # Master -> clip -> DAC stereo
    [master_vol.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 780)
patch.place("comment Turn on ezdac~ - turn up volume dial - play notes on kslider")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/warm_synth.maxpat")
print("Saved: examples/warm_synth.maxpat")
print(f"Total objects: {patch.num_objs}")
