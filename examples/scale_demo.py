"""
scale — Range Mapping
======================
The `scale` object linearly maps an input range to an output range.
  scale input_low input_high output_low output_high [exponential]

This patch maps a MIDI dial (0-127) to useful audio parameter ranges:
  - Frequency: 0-127 -> 100-2000 Hz
  - Volume: 0-127 -> 0.-1.
  - Filter Q: 0-127 -> 0.1-0.95

Usage in Max:
  1. Turn the dial (0-127)
  2. Watch each scale object map to a different range
  3. The oscillator frequency and filter respond in real time
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === SCALE: Range Mapping ===")[0]

# ============================================================
# INPUT: a single dial drives all three mappings
# ============================================================

patch.set_position(30, 70)
patch.place("comment MIDI-style input (0-127):")[0]

patch.set_position(30, 95)
dial = patch.place("dial")[0]

patch.set_position(30, 150)
input_num = patch.place("number")[0]

patch.connect(
    [dial.outs[0], input_num.ins[0]],
)

# ============================================================
# MAPPING 1: 0-127 -> 100-2000 (frequency)
# ============================================================

patch.set_position(30, 200)
patch.place("comment --- Frequency: 0-127 -> 100-2000 Hz ---")[0]

patch.set_position(30, 230)
scale_freq = patch.place("scale 0 127 100 2000")[0]

patch.set_position(30, 270)
freq_display = patch.place("flonum")[0]

patch.set_position(30, 310)
freq_sig = patch.place("sig~")[0]

patch.set_position(30, 350)
osc = patch.place("cycle~")[0]

patch.connect(
    [dial.outs[0], scale_freq.ins[0]],
    [scale_freq.outs[0], freq_display.ins[0]],
    [freq_display.outs[0], freq_sig.ins[0]],
    [freq_sig.outs[0], osc.ins[0]],
)

# ============================================================
# MAPPING 2: 0-127 -> 0. - 1. (volume)
# ============================================================

patch.set_position(250, 200)
patch.place("comment --- Volume: 0-127 -> 0.-1. ---")[0]

patch.set_position(250, 230)
scale_vol = patch.place("scale 0 127 0. 1.")[0]

patch.set_position(250, 270)
vol_display = patch.place("flonum")[0]

patch.set_position(250, 310)
vol_sig = patch.place("sig~")[0]

patch.connect(
    [dial.outs[0], scale_vol.ins[0]],
    [scale_vol.outs[0], vol_display.ins[0]],
    [vol_display.outs[0], vol_sig.ins[0]],
)

# ============================================================
# MAPPING 3: 0-127 -> 0.1 - 0.95 (filter resonance)
# ============================================================

patch.set_position(450, 200)
patch.place("comment --- Resonance: 0-127 -> 0.1-0.95 ---")[0]

patch.set_position(450, 230)
scale_q = patch.place("scale 0 127 0.1 0.95")[0]

patch.set_position(450, 270)
q_display = patch.place("flonum")[0]

patch.connect(
    [dial.outs[0], scale_q.ins[0]],
    [scale_q.outs[0], q_display.ins[0]],
)

# ============================================================
# AUDIO OUTPUT: osc -> filter -> volume -> dac
# ============================================================

patch.set_position(30, 400)
patch.place("comment --- Audio Output ---")[0]

patch.set_position(30, 430)
lores = patch.place("lores~ 1000 0.5")[0]

patch.set_position(30, 470)
vca = patch.place("*~")[0]

patch.set_position(30, 510)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(30, 550)
dac = patch.place("ezdac~")[0]

patch.connect(
    [osc.outs[0], lores.ins[0]],
    [q_display.outs[0], lores.ins[2]],
    [lores.outs[0], vca.ins[0]],
    [vol_sig.outs[0], vca.ins[1]],
    [vca.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 600)
patch.place("comment Turn on audio - move the dial - one knob controls freq/volume/resonance via scale")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/scale_demo.maxpat")
print("Saved: examples/scale_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
