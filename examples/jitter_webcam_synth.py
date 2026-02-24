"""
Jitter Webcam Synth Trigger
============================
Uses webcam brightness in 3 horizontal zones (Left / Center / Right)
to trigger and control three different synthesizers:

  LEFT ZONE   → Synth A: Kick Drum
                  Brightness spike triggers a 150→50Hz percussive hit

  CENTER ZONE → Synth B: Drone Pad
                  Brightness maps to pitch (55–440 Hz) and amplitude

  RIGHT ZONE  → Synth C: Shimmer Pad
                  Brightness gates 3 LFO-modulated sine oscillators

Layout: 5 columns, top-to-bottom signal flow.
Follows MAX_PATCH_VALIDITY_RULES and PATCH_LAYOUT_GUIDE.

Usage in Max:
  1. Turn on ezdac~ (audio output)
  2. Toggle starts webcam metro at 33ms (~30fps)
  3. Wave/move in front of camera to trigger synths
  4. Brightness numbers show live zone values (0–255)

Note: Webcam device is set to 0. If no video, try device 1 in jit.grab.
"""

import maxpylang as mp

patch = mp.MaxPatch()


# ============================================================
# SECTION 1: JITTER WEBCAM INPUT  (Column 1, x=30)
# ============================================================

patch.set_position(30, 30)
patch.place("comment === JITTER WEBCAM INPUT ===")[0]

# Toggle starts/stops the metro (and thus camera capture)
patch.set_position(30, 65)
cam_toggle = patch.place("toggle")[0]

patch.set_position(100, 65)
patch.place("comment Webcam ON/OFF")[0]

# Metro drives frame capture at ~30fps
patch.set_position(30, 100)
cam_metro = patch.place("metro 33")[0]

# Open camera on loadbang (device 0 = built-in/first camera)
patch.set_position(240, 65)
lb_cam = patch.place("loadbang")[0]

patch.set_position(240, 100)
cam_open = patch.place("message open 0")[0]

# Webcam grab: device 0, char type, 4 planes (ARGB), 320x240
patch.set_position(30, 140)
cam_grab = patch.place("jit.grab 0 char 4 320 240")[0]

# Convert ARGB -> 1-plane luminance (grayscale) for zone analysis
patch.set_position(30, 180)
cam_luma = patch.place("jit.rgb2luma")[0]

# Video preview inline in patch window
patch.set_position(30, 220)
cam_preview = patch.place("jit.pwindow")[0]

patch.connect(
    [cam_toggle.outs[0], cam_metro.ins[0]],
    [lb_cam.outs[0], cam_open.ins[0]],
    [cam_open.outs[0], cam_grab.ins[0]],   # "open 0" initializes device
    [cam_metro.outs[0], cam_grab.ins[0]],   # bang captures each frame
    [cam_grab.outs[0], cam_luma.ins[0]],
    [cam_luma.outs[0], cam_preview.ins[0]],
)


# ============================================================
# SECTION 2: ZONE ANALYSIS  (Column 1, below preview, x=30)
# Split 320x240 luma frame into Left / Center / Right thirds
# Use jit.stats (outlet 1 = stats list) + zl nth 2 (= mean)
# ============================================================

patch.set_position(30, 430)
patch.place("comment === ZONE ANALYSIS (L / C / R) ===")[0]

# Zone labels
patch.set_position(30, 465)
patch.place("comment LEFT")[0]

patch.set_position(175, 465)
patch.place("comment CENTER")[0]

patch.set_position(320, 465)
patch.place("comment RIGHT")[0]

# Submatrix objects crop the luma frame into horizontal thirds
# 320 / 3 = 107 | 107 | 106
patch.set_position(30, 485)
zone_left = patch.place("jit.submatrix @dim 107 240 @offset 0 0")[0]

patch.set_position(175, 485)
zone_center = patch.place("jit.submatrix @dim 107 240 @offset 107 0")[0]

patch.set_position(320, 485)
zone_right = patch.place("jit.submatrix @dim 106 240 @offset 214 0")[0]

# Feed luma matrix to all three zones
patch.connect(
    [cam_luma.outs[0], zone_left.ins[0]],
    [cam_luma.outs[0], zone_center.ins[0]],
    [cam_luma.outs[0], zone_right.ins[0]],
)

# jit.3m: outlet 0 = min, outlet 1 = max, outlet 2 = mean (per plane)
# For our 1-plane luma matrix, each outlet outputs a single float
patch.set_position(30, 525)
m3_left = patch.place("jit.3m")[0]

patch.set_position(175, 525)
m3_center = patch.place("jit.3m")[0]

patch.set_position(320, 525)
m3_right = patch.place("jit.3m")[0]

patch.connect(
    [zone_left.outs[0], m3_left.ins[0]],
    [zone_center.outs[0], m3_center.ins[0]],
    [zone_right.outs[0], m3_right.ins[0]],
)

# Display live zone mean brightness (outlet 2 = mean, 0-255)
patch.set_position(30, 565)
num_left = patch.place("number")[0]

patch.set_position(175, 565)
num_center = patch.place("number")[0]

patch.set_position(320, 565)
num_right = patch.place("number")[0]

patch.connect(
    [m3_left.outs[2], num_left.ins[0]],
    [m3_center.outs[2], num_center.ins[0]],
    [m3_right.outs[2], num_right.ins[0]],
)

# Send control-rate brightness values wirelessly to synth columns
# (avoids long diagonal cords per PATCH_LAYOUT_GUIDE Rule 7)
patch.set_position(30, 605)
send_left = patch.place("send zone1")[0]

patch.set_position(175, 605)
send_center = patch.place("send zone2")[0]

patch.set_position(320, 605)
send_right = patch.place("send zone3")[0]

patch.connect(
    [num_left.outs[0], send_left.ins[0]],
    [num_center.outs[0], send_center.ins[0]],
    [num_right.outs[0], send_right.ins[0]],
)


# ============================================================
# SECTION 3: SYNTH A - KICK DRUM  (Column 2, x=550)
# Triggered by LEFT zone brightness crossing a threshold
# Sound: 150Hz -> 50Hz sine sweep with fast decay envelope
# ============================================================

patch.set_position(550, 30)
patch.place("comment === SYNTH A: KICK DRUM ===")[0]

patch.set_position(550, 55)
patch.place("comment LEFT ZONE: spike triggers hit")[0]

# Receive left zone brightness (0-255 control-rate number)
patch.set_position(550, 85)
recv_left = patch.place("receive zone1")[0]

# Threshold: output 1 when brightness > 80, else 0
patch.set_position(550, 120)
kick_thresh = patch.place("> 80")[0]

# Edge detection: only fire when value changes (rising edge = 0->1)
patch.set_position(550, 155)
kick_change = patch.place("change")[0]

# sel 1: only pass bang when rising edge detected (value = 1)
patch.set_position(550, 190)
kick_sel = patch.place("sel 1")[0]

# Visual trigger indicator
patch.set_position(550, 225)
kick_btn = patch.place("button")[0]

patch.connect(
    [recv_left.outs[0], kick_thresh.ins[0]],
    [kick_thresh.outs[0], kick_change.ins[0]],
    [kick_change.outs[0], kick_sel.ins[0]],
    [kick_sel.outs[0], kick_btn.ins[0]],
)

# trigger b b: right outlet fires first (set env), left fires second (set freq)
# This ensures the envelope is armed before the oscillator freq is set
# (Rule 2.4b: use trigger to make execution order explicit)
patch.set_position(550, 265)
kick_trig = patch.place("trigger b b")[0]

# Freq sweep: jump to 150Hz, glide down to 50Hz over 150ms
# line~ format: "target, target time" (Rule 2.5b)
patch.set_position(550, 305)
kick_freq_msg = patch.place("message 150, 50 150")[0]

patch.set_position(550, 345)
kick_freq_line = patch.place("line~")[0]

# Envelope: 1.0 -> 0.0 over 150ms
patch.set_position(700, 305)
kick_env_msg = patch.place("message 1, 0 150")[0]

patch.set_position(700, 345)
kick_env_line = patch.place("line~")[0]

# Sine oscillator — frequency driven by line~ (signal-rate, smooth)
patch.set_position(550, 385)
kick_osc = patch.place("cycle~")[0]

# Apply envelope (VCA)
patch.set_position(550, 425)
kick_shaped = patch.place("*~")[0]

# Gain stage (Rule 1.3c: keep below 1.0 internally)
patch.set_position(550, 465)
kick_gain = patch.place("*~ 0.8")[0]

# Signal-rate wireless send to master mix
patch.set_position(550, 505)
kick_send = patch.place("send~ kick_out")[0]

patch.connect(
    [kick_btn.outs[0], kick_trig.ins[0]],
    [kick_trig.outs[1], kick_env_msg.ins[0]],    # right fires first (env armed)
    [kick_env_msg.outs[0], kick_env_line.ins[0]],
    [kick_trig.outs[0], kick_freq_msg.ins[0]],    # left fires second (freq set)
    [kick_freq_msg.outs[0], kick_freq_line.ins[0]],
    [kick_freq_line.outs[0], kick_osc.ins[0]],
    [kick_osc.outs[0], kick_shaped.ins[0]],
    [kick_env_line.outs[0], kick_shaped.ins[1]],
    [kick_shaped.outs[0], kick_gain.ins[0]],
    [kick_gain.outs[0], kick_send.ins[0]],
)


# ============================================================
# SECTION 4: SYNTH B - DRONE PAD  (Column 3, x=850)
# CENTER zone brightness -> pitch (55-440 Hz) and amplitude
# Sound: warm detuned saw pair through low-pass filter
# ============================================================

patch.set_position(850, 30)
patch.place("comment === SYNTH B: DRONE PAD ===")[0]

patch.set_position(850, 55)
patch.place("comment CENTER ZONE: pitch and amplitude")[0]

# Receive center zone brightness
patch.set_position(850, 85)
recv_center = patch.place("receive zone2")[0]

# --- PITCH PATH ---

# Map brightness (0-255) -> frequency (55-440 Hz, bass to mid range)
patch.set_position(850, 120)
pad_pitch_scale = patch.place("scale 0 255 55 440")[0]

# Control -> signal bridge (Rule 2.1b: use sig~ for control->signal)
patch.set_position(850, 160)
pad_pitch_sig = patch.place("sig~")[0]

# Primary saw oscillator (frequency from sig~)
patch.set_position(850, 200)
pad_osc1 = patch.place("saw~")[0]

# Second oscillator slightly detuned for warmth (+0.6%)
patch.set_position(990, 160)
pad_detune = patch.place("*~ 1.006")[0]

patch.set_position(990, 200)
pad_osc2 = patch.place("saw~")[0]

# Mix the two oscillators
patch.set_position(850, 240)
pad_mix = patch.place("+~")[0]

# Warm low-pass filter (Rule 1.3a: resonance 0.3 is safe, well below 0.95)
patch.set_position(850, 280)
pad_filt = patch.place("lores~ 500 0.3")[0]

# --- AMPLITUDE PATH ---

# Normalize brightness (0-255 -> 0.0-1.0) for amplitude gate
patch.set_position(1110, 120)
pad_amp_norm = patch.place("/ 255.")[0]

# Control -> signal bridge for amplitude (Rule 2.1b)
patch.set_position(1110, 160)
pad_amp_sig = patch.place("sig~")[0]

# Apply amplitude gate: filtered signal x brightness level
patch.set_position(850, 320)
pad_gate = patch.place("*~")[0]

# Scale gain
patch.set_position(850, 360)
pad_gain = patch.place("*~ 0.5")[0]

# Signal-rate wireless send to master
patch.set_position(850, 400)
pad_send = patch.place("send~ pad_out")[0]

patch.connect(
    # Pitch path
    [recv_center.outs[0], pad_pitch_scale.ins[0]],
    [pad_pitch_scale.outs[0], pad_pitch_sig.ins[0]],
    [pad_pitch_sig.outs[0], pad_osc1.ins[0]],
    [pad_pitch_sig.outs[0], pad_detune.ins[0]],
    [pad_detune.outs[0], pad_osc2.ins[0]],
    [pad_osc1.outs[0], pad_mix.ins[0]],
    [pad_osc2.outs[0], pad_mix.ins[1]],
    [pad_mix.outs[0], pad_filt.ins[0]],
    # Amplitude path
    [recv_center.outs[0], pad_amp_norm.ins[0]],
    [pad_amp_norm.outs[0], pad_amp_sig.ins[0]],
    # Gate: filtered signal x brightness amplitude
    [pad_filt.outs[0], pad_gate.ins[0]],
    [pad_amp_sig.outs[0], pad_gate.ins[1]],
    [pad_gate.outs[0], pad_gain.ins[0]],
    [pad_gain.outs[0], pad_send.ins[0]],
)


# ============================================================
# SECTION 5: SYNTH C - SHIMMER PAD  (Column 4, x=1200)
# RIGHT zone brightness -> amplitude gate on shimmer oscillators
# Sound: 3 LFO-modulated sine waves at E5, A5, B5 (659, 880, 988 Hz)
# ============================================================

patch.set_position(1200, 30)
patch.place("comment === SYNTH C: SHIMMER PAD ===")[0]

patch.set_position(1200, 55)
patch.place("comment RIGHT ZONE: amplitude gate")[0]

# Receive right zone brightness
patch.set_position(1200, 85)
recv_right = patch.place("receive zone3")[0]

# Normalize brightness -> amplitude (0-255 -> 0.0-1.0)
patch.set_position(1200, 120)
shim_amp_norm = patch.place("/ 255.")[0]

# Control -> signal bridge (Rule 2.1b)
patch.set_position(1200, 160)
shim_amp_sig = patch.place("sig~")[0]

# Three shimmer oscillators: E5, A5, B5 upper harmony
patch.set_position(1200, 200)
shim_e5 = patch.place("cycle~ 659")[0]

patch.set_position(1315, 200)
shim_a5 = patch.place("cycle~ 880")[0]

patch.set_position(1430, 200)
shim_b5 = patch.place("cycle~ 988")[0]

# Slow LFOs at different rates for natural shimmer movement
patch.set_position(1200, 240)
shim_lfo1 = patch.place("cycle~ 0.17")[0]

patch.set_position(1315, 240)
shim_lfo2 = patch.place("cycle~ 0.23")[0]

patch.set_position(1430, 240)
shim_lfo3 = patch.place("cycle~ 0.13")[0]

# Scale LFOs to 0.7-1.0 range (oscillators always slightly present)
# LFO output is -1 to 1, so: *0.15 -> -0.15..0.15, +0.85 -> 0.70..1.00
patch.set_position(1200, 280)
shim_ls1 = patch.place("*~ 0.15")[0]

patch.set_position(1200, 315)
shim_lo1 = patch.place("+~ 0.85")[0]

patch.set_position(1315, 280)
shim_ls2 = patch.place("*~ 0.15")[0]

patch.set_position(1315, 315)
shim_lo2 = patch.place("+~ 0.85")[0]

patch.set_position(1430, 280)
shim_ls3 = patch.place("*~ 0.15")[0]

patch.set_position(1430, 315)
shim_lo3 = patch.place("+~ 0.85")[0]

# Modulate oscillator amplitude with LFO
patch.set_position(1200, 355)
shim_mod1 = patch.place("*~")[0]

patch.set_position(1315, 355)
shim_mod2 = patch.place("*~")[0]

patch.set_position(1430, 355)
shim_mod3 = patch.place("*~")[0]

# Sum all three shimmer voices
patch.set_position(1200, 395)
shim_sum1 = patch.place("+~")[0]

patch.set_position(1200, 435)
shim_sum2 = patch.place("+~")[0]

# Scale down for 3 voices (Rule 1.3c: keep gain in range)
patch.set_position(1200, 475)
shim_scale = patch.place("*~ 0.33")[0]

# Apply brightness as amplitude gate (right zone light = shimmer on)
patch.set_position(1200, 515)
shim_gate = patch.place("*~")[0]

# Signal-rate wireless send to master
patch.set_position(1200, 555)
shim_send = patch.place("send~ shimmer_out")[0]

patch.connect(
    # LFO processing chains
    [shim_lfo1.outs[0], shim_ls1.ins[0]],
    [shim_ls1.outs[0], shim_lo1.ins[0]],
    [shim_lfo2.outs[0], shim_ls2.ins[0]],
    [shim_ls2.outs[0], shim_lo2.ins[0]],
    [shim_lfo3.outs[0], shim_ls3.ins[0]],
    [shim_ls3.outs[0], shim_lo3.ins[0]],
    # Oscillator x LFO amplitude modulation
    [shim_e5.outs[0], shim_mod1.ins[0]],
    [shim_lo1.outs[0], shim_mod1.ins[1]],
    [shim_a5.outs[0], shim_mod2.ins[0]],
    [shim_lo2.outs[0], shim_mod2.ins[1]],
    [shim_b5.outs[0], shim_mod3.ins[0]],
    [shim_lo3.outs[0], shim_mod3.ins[1]],
    # Mix voices
    [shim_mod1.outs[0], shim_sum1.ins[0]],
    [shim_mod2.outs[0], shim_sum1.ins[1]],
    [shim_sum1.outs[0], shim_sum2.ins[0]],
    [shim_mod3.outs[0], shim_sum2.ins[1]],
    [shim_sum2.outs[0], shim_scale.ins[0]],
    # Brightness amplitude gate
    [recv_right.outs[0], shim_amp_norm.ins[0]],
    [shim_amp_norm.outs[0], shim_amp_sig.ins[0]],
    [shim_scale.outs[0], shim_gate.ins[0]],
    [shim_amp_sig.outs[0], shim_gate.ins[1]],
    [shim_gate.outs[0], shim_send.ins[0]],
)


# ============================================================
# SECTION 6: MASTER MIX + OUTPUT  (Column 5, x=1700)
# All three voices received via send~/receive~ and summed
# ============================================================

patch.set_position(1700, 30)
patch.place("comment === MASTER MIX ===")[0]

# Receive signal-rate audio from all synths
patch.set_position(1700, 65)
recv_kick = patch.place("receive~ kick_out")[0]

patch.set_position(1700, 100)
recv_pad = patch.place("receive~ pad_out")[0]

patch.set_position(1700, 135)
recv_shimmer = patch.place("receive~ shimmer_out")[0]

# Sum kick + pad
patch.set_position(1700, 175)
sum1 = patch.place("+~")[0]

# Sum (kick+pad) + shimmer
patch.set_position(1700, 215)
sum2 = patch.place("+~")[0]

# Scale master down (3 voices, prevent summed clipping)
patch.set_position(1700, 255)
master_scale = patch.place("*~ 0.35")[0]

# Safety hard clipper before output (Rule 1.3c)
patch.set_position(1700, 295)
master_clip = patch.place("clip~ -1. 1.")[0]

# Stereo output (left and right channels)
patch.set_position(1700, 335)
dac = patch.place("ezdac~")[0]

# Instructions
patch.set_position(1700, 380)
patch.place("comment Turn on ezdac~ then toggle webcam")[0]

patch.set_position(1700, 410)
patch.place("comment L: kick on brightness spike | C: pad pitch+vol | R: shimmer vol")[0]

patch.connect(
    [recv_kick.outs[0], sum1.ins[0]],
    [recv_pad.outs[0], sum1.ins[1]],
    [sum1.outs[0], sum2.ins[0]],
    [recv_shimmer.outs[0], sum2.ins[1]],
    [sum2.outs[0], master_scale.ins[0]],
    [master_scale.outs[0], master_clip.ins[0]],
    [master_clip.outs[0], dac.ins[0]],
    [master_clip.outs[0], dac.ins[1]],  # stereo (same mono signal both channels)
)


# ============================================================
# SAVE
# ============================================================

patch.save("jitter_webcam_synth.maxpat")
print("Saved: jitter_webcam_synth.maxpat")
print(f"Total objects: {patch.num_objs}")
print("""
HOW IT WORKS:
  Webcam (320x240) is split into 3 horizontal zones:
    LEFT   (x 0-106)  : brightness spike -> triggers kick drum hit
    CENTER (x 107-213): brightness -> pitch (55-440Hz) and amplitude of drone pad
    RIGHT  (x 214-319): brightness -> amplitude gate on shimmer pad (E5/A5/B5)

SYNTHS:
  Kick:    cycle~ with 150->50Hz freq sweep + fast decay envelope
  Drone:   detuned saw~ pair through lores~ low-pass filter
  Shimmer: 3x cycle~ at E5/A5/B5 with slow LFO modulation

LAYOUT (5 columns):
  x=30    JITTER INPUT + ZONE ANALYSIS
  x=550   SYNTH A: KICK (left zone)
  x=850   SYNTH B: DRONE PAD (center zone)
  x=1200  SYNTH C: SHIMMER (right zone)
  x=1700  MASTER MIX
""")
