"""
FFT Spectrogram — Color Jitter Matrix Visualization with Effects Rack
=====================================================================
Loads a WAV file, runs it through 5 real-time audio effects, then
performs a 512-point FFT and writes each frame's bin magnitudes into
a scrolling 512x256 Jitter matrix with a heat map color scheme
(black → red → yellow → white).

Effects Rack (inserted between sfplay~ and fft~):
  1. Filter Cutoff  — lores~ lowpass sweep (100 Hz – 15 kHz)
  2. Resonance      — lores~ resonance boost (0 – 0.95)
  3. Drive           — gain + tanh~ soft saturation (1x – 20x)
  4. Tremolo         — cycle~ LFO amplitude modulation (0 – 20 Hz)
  5. Delay Feedback  — tapin~/tapout~ 250ms echo (0 – 0.8 feedback)

Uses 4 jit.poke~ objects writing to separate ARGB planes:
  Red   = clip(mag * 3, 0, 1)         — appears first (low energy)
  Green = clip(mag * 3 - 1, 0, 1)     — appears second (mid energy)
  Blue  = clip(mag * 3 - 2, 0, 1)     — appears last  (high energy)
  Alpha = 1.0 constant                — fully opaque

Usage in Max:
  1. Turn on ezdac~ (enables DSP)
  2. Click 'open' to load a WAV file
  3. Click the toggle to start playback
  4. Turn the 5 effect dials to alter the sound
  5. Adjust the Gain flonum to control brightness (try 0.5–5.0)
  6. Resize jit.pwindow to see the full spectrogram
"""

import maxpylang as mp

patch = mp.MaxPatch()

# ============================================================
# JITTER MATRIX — MUST BE CREATED FIRST
# ============================================================
# 4-plane float32 for ARGB color. Named "fft_viz" so all
# jit.poke~ objects share the same matrix.

patch.set_position(30, 1380)
matrix = patch.place("jit.matrix fft_viz 4 float32 512 256")[0]

# ============================================================
# AUDIO INPUT
# ============================================================

patch.set_position(30, 30)
patch.place("comment === FFT SPECTROGRAM — COLOR HEAT MAP WITH EFFECTS ===")[0]

patch.set_position(30, 65)
patch.place("comment --- Audio Input ---")[0]

patch.set_position(30, 95)
open_msg = patch.place("message open")[0]

patch.set_position(120, 95)
play_toggle = patch.place("toggle")[0]

patch.set_position(30, 135)
sfplay = patch.place("sfplay~ 1")[0]

patch.connect(
    [open_msg.outs[0], sfplay.ins[0]],
    [play_toggle.outs[0], sfplay.ins[0]],
)

# ============================================================
# EFFECTS RACK — 5 dial-controlled audio effects
# ============================================================
# Each column: loadbang → message (default) → dial → scale → sig~
# The sig~ outputs feed the DSP chain below.

patch.set_position(30, 180)
patch.place("comment === Effects Rack ===")[0]

# --- Column labels ---
patch.set_position(30, 205)
patch.place("comment Filter Cutoff")[0]

patch.set_position(150, 205)
patch.place("comment Resonance")[0]

patch.set_position(270, 205)
patch.place("comment Drive")[0]

patch.set_position(390, 205)
patch.place("comment Tremolo")[0]

patch.set_position(510, 205)
patch.place("comment Delay FB")[0]

# --- Loadbangs for defaults ---
patch.set_position(30, 235)
lb_filt = patch.place("loadbang")[0]

patch.set_position(150, 235)
lb_res = patch.place("loadbang")[0]

patch.set_position(270, 235)
lb_drive = patch.place("loadbang")[0]

patch.set_position(390, 235)
lb_trem = patch.place("loadbang")[0]

patch.set_position(510, 235)
lb_delay = patch.place("loadbang")[0]

# --- Default value messages ---
patch.set_position(30, 265)
def_filt = patch.place("message 127")[0]    # fully open (15 kHz)

patch.set_position(150, 265)
def_res = patch.place("message 0")[0]       # no resonance

patch.set_position(270, 265)
def_drive = patch.place("message 0")[0]     # clean (gain 1.0)

patch.set_position(390, 265)
def_trem = patch.place("message 0")[0]      # no tremolo (0 Hz)

patch.set_position(510, 265)
def_delay = patch.place("message 0")[0]     # no feedback

# --- Dials (0–127) ---
patch.set_position(30, 295)
dial_filt = patch.place("dial")[0]

patch.set_position(150, 295)
dial_res = patch.place("dial")[0]

patch.set_position(270, 295)
dial_drive = patch.place("dial")[0]

patch.set_position(390, 295)
dial_trem = patch.place("dial")[0]

patch.set_position(510, 295)
dial_delay = patch.place("dial")[0]

# --- Scale objects (map 0–127 to parameter ranges) ---
patch.set_position(30, 345)
scale_filt = patch.place("scale 0 127 100. 15000.")[0]

patch.set_position(150, 345)
scale_res = patch.place("scale 0 127 0. 0.95")[0]

patch.set_position(270, 345)
scale_drive = patch.place("scale 0 127 1. 20.")[0]

patch.set_position(390, 345)
scale_trem = patch.place("scale 0 127 0. 20.")[0]

patch.set_position(510, 345)
scale_delay = patch.place("scale 0 127 0. 0.8")[0]

# --- sig~ objects (control → signal bridge) ---
# Initial values match defaults so audio passes through even before loadbang
patch.set_position(30, 385)
sig_filt = patch.place("sig~ 15000.")[0]   # filter wide open

patch.set_position(150, 385)
sig_res = patch.place("sig~")[0]            # resonance 0 (default)

patch.set_position(270, 385)
sig_drive = patch.place("sig~ 1.")[0]       # unity gain

patch.set_position(390, 385)
sig_trem = patch.place("sig~")[0]            # 0 Hz LFO (default)

patch.set_position(510, 385)
sig_delay = patch.place("sig~")[0]           # no feedback (default)

# Wire all 5 knob columns
patch.connect(
    # Filter cutoff
    [lb_filt.outs[0], def_filt.ins[0]],
    [def_filt.outs[0], dial_filt.ins[0]],
    [dial_filt.outs[0], scale_filt.ins[0]],
    [scale_filt.outs[0], sig_filt.ins[0]],
    # Resonance
    [lb_res.outs[0], def_res.ins[0]],
    [def_res.outs[0], dial_res.ins[0]],
    [dial_res.outs[0], scale_res.ins[0]],
    [scale_res.outs[0], sig_res.ins[0]],
    # Drive
    [lb_drive.outs[0], def_drive.ins[0]],
    [def_drive.outs[0], dial_drive.ins[0]],
    [dial_drive.outs[0], scale_drive.ins[0]],
    [scale_drive.outs[0], sig_drive.ins[0]],
    # Tremolo
    [lb_trem.outs[0], def_trem.ins[0]],
    [def_trem.outs[0], dial_trem.ins[0]],
    [dial_trem.outs[0], scale_trem.ins[0]],
    [scale_trem.outs[0], sig_trem.ins[0]],
    # Delay feedback
    [lb_delay.outs[0], def_delay.ins[0]],
    [def_delay.outs[0], dial_delay.ins[0]],
    [dial_delay.outs[0], scale_delay.ins[0]],
    [scale_delay.outs[0], sig_delay.ins[0]],
)

# ============================================================
# EFFECTS DSP CHAIN
# ============================================================
# Signal flow: sfplay~ → lores~ → *~ drive → tanh~ → *~ tremolo
#              → +~ (delay mix) → tapin~/tapout~ feedback loop
# Output taken from +~ feeds both FFT analysis and audio output.

patch.set_position(30, 425)
patch.place("comment --- Effects DSP Chain ---")[0]

# 1. Low-pass filter
patch.set_position(30, 455)
lores = patch.place("lores~")[0]

# 2. Drive gain
patch.set_position(30, 495)
drive_mul = patch.place("*~")[0]

# 3. Soft saturation
patch.set_position(30, 535)
saturate = patch.place("tanh~")[0]

# 4. Tremolo — LFO sub-chain (at x=390, near tremolo knob)
patch.set_position(390, 425)
lfo = patch.place("cycle~")[0]

patch.set_position(390, 465)
lfo_scale = patch.place("*~ 0.5")[0]

patch.set_position(390, 505)
lfo_offset = patch.place("+~ 0.5")[0]

# Tremolo multiply (audio × LFO)
patch.set_position(30, 575)
trem_mul = patch.place("*~")[0]

# 5. Delay with feedback
patch.set_position(30, 615)
delay_mix = patch.place("+~")[0]

patch.set_position(30, 655)
tapin = patch.place("tapin~ 1000")[0]

patch.set_position(30, 690)
tapout = patch.place("tapout~ 250")[0]

patch.set_position(150, 690)
fb_mul = patch.place("*~")[0]

# Wire the effects DSP chain
patch.connect(
    # sfplay~ → lores~ (audio input)
    [sfplay.outs[0], lores.ins[0]],
    # Control signals → lores~
    [sig_filt.outs[0], lores.ins[1]],
    [sig_res.outs[0], lores.ins[2]],
    # lores~ → drive *~
    [lores.outs[0], drive_mul.ins[0]],
    [sig_drive.outs[0], drive_mul.ins[1]],
    # drive → tanh~ (saturation)
    [drive_mul.outs[0], saturate.ins[0]],
    # LFO sub-chain: sig_trem → cycle~ → scale → offset
    [sig_trem.outs[0], lfo.ins[0]],
    [lfo.outs[0], lfo_scale.ins[0]],
    [lfo_scale.outs[0], lfo_offset.ins[0]],
    # tanh~ → tremolo *~ (audio × LFO)
    [saturate.outs[0], trem_mul.ins[0]],
    [lfo_offset.outs[0], trem_mul.ins[1]],
    # tremolo → delay mix (+~ inlet 0)
    [trem_mul.outs[0], delay_mix.ins[0]],
    # Delay feedback loop
    [delay_mix.outs[0], tapin.ins[0]],
    [tapin.outs[0], tapout.ins[0]],
    [tapout.outs[0], fb_mul.ins[0]],
    [sig_delay.outs[0], fb_mul.ins[1]],
    [fb_mul.outs[0], delay_mix.ins[1]],
)

# ============================================================
# FFT ANALYSIS (512-point)
# ============================================================

patch.set_position(30, 730)
patch.place("comment --- FFT Analysis ---")[0]

patch.set_position(30, 760)
fft = patch.place("fft~ 512")[0]

patch.set_position(30, 800)
cartopol = patch.place("cartopol~")[0]

patch.connect(
    [delay_mix.outs[0], fft.ins[0]],
    [fft.outs[0], cartopol.ins[0]],
    [fft.outs[1], cartopol.ins[1]],
)

# ============================================================
# MAGNITUDE SCALING
# ============================================================

patch.set_position(30, 855)
patch.place("comment --- Gain ---")[0]

patch.set_position(30, 885)
gain_num = patch.place("flonum")[0]

patch.set_position(30, 925)
gain_sig = patch.place("sig~")[0]

patch.set_position(30, 965)
scale_mag = patch.place("*~")[0]

# Default gain
patch.set_position(130, 855)
lb_gain = patch.place("loadbang")[0]

patch.set_position(130, 885)
gain_def = patch.place("message 1.")[0]

patch.connect(
    [lb_gain.outs[0], gain_def.ins[0]],
    [gain_def.outs[0], gain_num.ins[0]],
    [gain_num.outs[0], gain_sig.ins[0]],
    [gain_sig.outs[0], scale_mag.ins[1]],
    [cartopol.outs[0], scale_mag.ins[0]],
)

# ============================================================
# COLOR MAPPING: heat map (black → red → yellow → white)
# ============================================================

patch.set_position(30, 1020)
patch.place("comment --- Color Map: black → red → yellow → white ---")[0]

# Triple the magnitude for the 3-segment color ramp
patch.set_position(30, 1050)
mag3 = patch.place("*~ 3.")[0]

patch.connect(
    [scale_mag.outs[0], mag3.ins[0]],
)

# --- Red = clip(mag*3, 0, 1) ---
patch.set_position(30, 1085)
patch.place("comment Red")[0]

patch.set_position(30, 1110)
r_clip = patch.place("clip~ 0. 1.")[0]

patch.connect(
    [mag3.outs[0], r_clip.ins[0]],
)

# --- Green = clip(mag*3 - 1, 0, 1) ---
patch.set_position(170, 1085)
patch.place("comment Green")[0]

patch.set_position(170, 1110)
g_sub = patch.place("+~ -1.")[0]

patch.set_position(170, 1150)
g_clip = patch.place("clip~ 0. 1.")[0]

patch.connect(
    [mag3.outs[0], g_sub.ins[0]],
    [g_sub.outs[0], g_clip.ins[0]],
)

# --- Blue = clip(mag*3 - 2, 0, 1) ---
patch.set_position(310, 1085)
patch.place("comment Blue")[0]

patch.set_position(310, 1110)
b_sub = patch.place("+~ -2.")[0]

patch.set_position(310, 1150)
b_clip = patch.place("clip~ 0. 1.")[0]

patch.connect(
    [mag3.outs[0], b_sub.ins[0]],
    [b_sub.outs[0], b_clip.ins[0]],
)

# --- Alpha = constant 1.0 (fully opaque) ---
patch.set_position(450, 1085)
patch.place("comment Alpha")[0]

patch.set_position(450, 1110)
alpha_sig = patch.place("sig~ 1.")[0]

# ============================================================
# ROW COUNTER (scrolling y position)
# ============================================================

patch.set_position(450, 1180)
patch.place("comment --- Row Counter ---")[0]

patch.set_position(450, 1210)
lb_y = patch.place("loadbang")[0]

patch.set_position(450, 1245)
metro_y = patch.place("metro 6")[0]

patch.set_position(450, 1280)
counter_y = patch.place("counter 0 255")[0]

patch.set_position(450, 1315)
y_sig = patch.place("sig~")[0]

patch.connect(
    [lb_y.outs[0], metro_y.ins[0]],
    [metro_y.outs[0], counter_y.ins[0]],
    [counter_y.outs[0], y_sig.ins[0]],
)

# ============================================================
# 4x JIT.POKE~ — one per ARGB plane
# ============================================================

patch.set_position(30, 1200)
patch.place("comment --- jit.poke~ per color plane (value, x=bin, y=row) ---")[0]

# Alpha (plane 0)
patch.set_position(450, 1350)
poke_a = patch.place("jit.poke~ fft_viz 2 @plane 0")[0]

# Red (plane 1)
patch.set_position(30, 1240)
poke_r = patch.place("jit.poke~ fft_viz 2 @plane 1")[0]

# Green (plane 2)
patch.set_position(170, 1240)
poke_g = patch.place("jit.poke~ fft_viz 2 @plane 2")[0]

# Blue (plane 3)
patch.set_position(310, 1240)
poke_b = patch.place("jit.poke~ fft_viz 2 @plane 3")[0]

# Connect color values to poke inlets (inlet 0 = value)
patch.connect(
    [r_clip.outs[0], poke_r.ins[0]],
    [g_clip.outs[0], poke_g.ins[0]],
    [b_clip.outs[0], poke_b.ins[0]],
    [alpha_sig.outs[0], poke_a.ins[0]],
)

# Connect x position (fft~ sync) to all poke inlet 1
patch.connect(
    [fft.outs[2], poke_r.ins[1]],
    [fft.outs[2], poke_g.ins[1]],
    [fft.outs[2], poke_b.ins[1]],
    [fft.outs[2], poke_a.ins[1]],
)

# Connect y position (counter) to all poke inlet 2
patch.connect(
    [y_sig.outs[0], poke_r.ins[2]],
    [y_sig.outs[0], poke_g.ins[2]],
    [y_sig.outs[0], poke_b.ins[2]],
    [y_sig.outs[0], poke_a.ins[2]],
)

# ============================================================
# JITTER MATRIX DISPLAY
# ============================================================

patch.set_position(30, 1330)
patch.place("comment --- Jitter Display (512 x 256, ARGB) ---")[0]

# Display refresh (~30 fps)
patch.set_position(250, 1355)
lb_disp = patch.place("loadbang")[0]

patch.set_position(250, 1390)
metro_disp = patch.place("metro 33")[0]

# Visual output
patch.set_position(30, 1430)
pwindow = patch.place("jit.pwindow")[0]

patch.connect(
    [lb_disp.outs[0], metro_disp.ins[0]],
    [metro_disp.outs[0], matrix.ins[0]],
    [matrix.outs[0], pwindow.ins[0]],
)

# ============================================================
# AUDIO OUTPUT
# ============================================================

patch.set_position(30, 1500)
patch.place("comment --- Audio Output ---")[0]

patch.set_position(30, 1530)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(30, 1570)
dac = patch.place("ezdac~")[0]

patch.connect(
    [delay_mix.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# ============================================================
# INSTRUCTIONS
# ============================================================

patch.set_position(30, 1620)
patch.place("comment Turn on ezdac~ → 'open' WAV → toggle play → turn effect dials → adjust Gain (0.5–5.0) → resize jit.pwindow")[0]

# ============================================================
# SAVE
# ============================================================

patch.save("examples/fft_jitter_viz.maxpat")
print("Saved: examples/fft_jitter_viz.maxpat")
print(f"Total objects: {patch.num_objs}")
