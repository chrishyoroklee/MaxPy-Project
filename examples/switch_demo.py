"""
switch — Input Selector
========================
The `switch` object routes one of N inputs to a single output based on
an index.  Inlet 0 selects which input (1-N) passes through; 0 = off.

Default switch (no args) has 2 data inlets:
  inlet 0: selector (0=off, 1 or 2)
  inlet 1: input 1
  inlet 2: input 2
  outlet 0: selected input

This patch switches between 2 oscillator waveforms:
  1 = sine (cycle~), 2 = saw (saw~)

Usage in Max:
  1. Turn on ezdac~
  2. Type 1 or 2 into the number box to select a waveform
  3. Type 0 to mute (no input selected)
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# TITLE
# ============================================================

patch.set_position(30, 30)
patch.place("comment === SWITCH: Input Selector ===")[0]

# ============================================================
# FREQUENCY INPUT
# ============================================================

patch.set_position(30, 70)
patch.place("comment Frequency (Hz):")[0]

patch.set_position(30, 95)
freq_num = patch.place("number")[0]

# Loadbang default freq
patch.set_position(170, 70)
loadbang = patch.place("loadbang")[0]

patch.set_position(170, 95)
default_freq = patch.place("message 440")[0]

patch.set_position(30, 135)
freq_sig = patch.place("sig~")[0]

patch.connect(
    [loadbang.outs[0], default_freq.ins[0]],
    [default_freq.outs[0], freq_num.ins[0]],
    [freq_num.outs[0], freq_sig.ins[0]],
)

# ============================================================
# TWO OSCILLATORS
# ============================================================

patch.set_position(30, 180)
patch.place("comment 1: sine")[0]

patch.set_position(160, 180)
patch.place("comment 2: saw")[0]

patch.set_position(30, 205)
osc_sine = patch.place("cycle~")[0]

patch.set_position(160, 205)
osc_saw = patch.place("saw~")[0]

patch.connect(
    [freq_sig.outs[0], osc_sine.ins[0]],
    [freq_sig.outs[0], osc_saw.ins[0]],
)

# ============================================================
# SWITCH: select which oscillator passes through
# ============================================================

patch.set_position(30, 260)
patch.place("comment Select waveform (0=off, 1=sine, 2=saw):")[0]

patch.set_position(30, 285)
selector = patch.place("number")[0]

patch.set_position(30, 325)
switch = patch.place("switch")[0]

patch.connect(
    [selector.outs[0], switch.ins[0]],
    [osc_sine.outs[0], switch.ins[1]],
    [osc_saw.outs[0], switch.ins[2]],
)

# Default to sine
patch.set_position(170, 285)
default_sel = patch.place("message 1")[0]

patch.connect(
    [loadbang.outs[0], default_sel.ins[0]],
    [default_sel.outs[0], selector.ins[0]],
)

# ============================================================
# OUTPUT: switch -> volume -> clip -> dac
# ============================================================

patch.set_position(30, 380)
patch.place("comment Volume:")[0]

patch.set_position(30, 405)
vol_dial = patch.place("dial")[0]

patch.set_position(30, 455)
vol_scale = patch.place("/ 127.")[0]

patch.set_position(30, 490)
vol_sig = patch.place("sig~")[0]

patch.set_position(30, 530)
vca = patch.place("*~")[0]

patch.set_position(30, 570)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(30, 610)
dac = patch.place("ezdac~")[0]

# Default volume
patch.set_position(170, 405)
default_vol = patch.place("message 80")[0]

patch.connect(
    [loadbang.outs[0], default_vol.ins[0]],
    [default_vol.outs[0], vol_dial.ins[0]],
    [vol_dial.outs[0], vol_scale.ins[0]],
    [vol_scale.outs[0], vol_sig.ins[0]],
    [switch.outs[0], vca.ins[0]],
    [vol_sig.outs[0], vca.ins[1]],
    [vca.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 660)
patch.place("comment Turn on audio - type 1 or 2 to switch waveforms - 0 to mute")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/switch_demo.maxpat")
print("Saved: examples/switch_demo.maxpat")
print(f"Total objects: {patch.num_objs}")
