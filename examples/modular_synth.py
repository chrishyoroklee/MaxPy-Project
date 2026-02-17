"""
Modular Synth with Visual Keyboard (Organized Layout)
=====================================================
10 layers: keyboard pad, bass drone, mono synth, kick, snare, hi-hat,
sus4 chord, major chord, shimmer pad, dissonant cluster + delay.

All voices have individual volume sliders and feed a master mix bus.

Layout:
  Row 1: Transport
  Row 2: Keyboard Synth | Drums (Kick, Snare, Hi-hat) | Shimmer Pad
  Row 3: Bass Drone | Mono Synth | Dissonant Cluster + Delay
  Row 4: Chord Sus4 | Chord Major
  Row 5: Master Mix + Output
"""

import maxpylang as mp

patch = mp.MaxPatch()

# Column X positions
C1 = 30
C2 = 500
C3 = 950

# ================================================================
# TRANSPORT & MASTER CONTROLS
# ================================================================

patch.set_position(C1, 30)
patch.place("comment === TRANSPORT ===")[0]

patch.set_position(C1, 60)
loadbang = patch.place("loadbang")[0]

patch.set_position(C1, 95)
start_msg = patch.place("message 1")[0]

patch.set_position(C1, 130)
transport_metro = patch.place("metro 117")[0]

patch.set_position(C1, 165)
counter_16 = patch.place("counter 15")[0]

patch.connect(
    [loadbang.outs[0], start_msg.ins[0]],
    [start_msg.outs[0], transport_metro.ins[0]],
    [transport_metro.outs[0], counter_16.ins[0]],
)

# ================================================================
# SECTION 1: KEYBOARD PAD SYNTH (Column 1, y=220+)
# ================================================================

patch.set_position(C1, 220)
patch.place("comment === KEYBOARD PAD SYNTH ===")[0]

# --- Pitch path ---
patch.set_position(C1, 255)
keyboard = patch.place("kslider")[0]

patch.set_position(C1, 340)
mtof = patch.place("mtof")[0]

patch.set_position(C1, 375)
key_freq_sig = patch.place("sig~")[0]

patch.connect(
    [keyboard.outs[0], mtof.ins[0]],
    [mtof.outs[0], key_freq_sig.ins[0]],
)

# --- Detuned oscillators ---
patch.set_position(C1, 415)
patch.place("comment center")[0]
patch.set_position(C1 + 80, 415)
patch.place("comment -0.5%")[0]
patch.set_position(C1 + 160, 415)
patch.place("comment sub")[0]

patch.set_position(C1 + 80, 440)
key_detune_down = patch.place("*~ 0.995")[0]
patch.set_position(C1 + 160, 440)
key_sub_oct = patch.place("*~ 0.5")[0]

patch.set_position(C1, 480)
key_osc1 = patch.place("saw~")[0]
patch.set_position(C1 + 80, 480)
key_osc2 = patch.place("saw~")[0]
patch.set_position(C1 + 160, 480)
key_sub = patch.place("cycle~")[0]

patch.connect(
    [key_freq_sig.outs[0], key_osc1.ins[0]],
    [key_freq_sig.outs[0], key_detune_down.ins[0]],
    [key_freq_sig.outs[0], key_sub_oct.ins[0]],
    [key_detune_down.outs[0], key_osc2.ins[0]],
    [key_sub_oct.outs[0], key_sub.ins[0]],
)

# --- Mix oscillators ---
patch.set_position(C1, 520)
key_mix = patch.place("+~")[0]

patch.connect(
    [key_osc1.outs[0], key_mix.ins[0]],
    [key_osc2.outs[0], key_mix.ins[0]],
    [key_sub.outs[0], key_mix.ins[0]],
)

# --- Envelope (velocity gate) ---
patch.set_position(C1 + 250, 255)
patch.place("comment Envelope")[0]

patch.set_position(C1 + 250, 280)
key_vel_gate = patch.place("> 0")[0]

patch.set_position(C1 + 250, 315)
key_sel_env = patch.place("sel 0 1")[0]

patch.set_position(C1 + 250, 355)
key_release_msg = patch.place("message 0 800")[0]

patch.set_position(C1 + 370, 355)
key_attack_msg = patch.place("message 1 200")[0]

patch.set_position(C1 + 250, 395)
key_env = patch.place("line~")[0]

patch.connect(
    [keyboard.outs[1], key_vel_gate.ins[0]],
    [key_vel_gate.outs[0], key_sel_env.ins[0]],
    [key_sel_env.outs[0], key_release_msg.ins[0]],
    [key_sel_env.outs[1], key_attack_msg.ins[0]],
    [key_release_msg.outs[0], key_env.ins[0]],
    [key_attack_msg.outs[0], key_env.ins[0]],
)

# --- Apply envelope ---
patch.set_position(C1, 560)
key_shaped = patch.place("*~")[0]

patch.connect(
    [key_mix.outs[0], key_shaped.ins[0]],
    [key_env.outs[0], key_shaped.ins[1]],
)

# --- Filter with LFO modulation ---
patch.set_position(C1 + 150, 520)
key_filt_lfo = patch.place("cycle~ 0.3")[0]

patch.set_position(C1 + 150, 555)
key_filt_scale = patch.place("*~ 300")[0]

patch.set_position(C1 + 150, 590)
key_filt_base = patch.place("+~ 800")[0]

patch.set_position(C1, 600)
key_lpf = patch.place("svf~ 800 0.6")[0]

patch.connect(
    [key_filt_lfo.outs[0], key_filt_scale.ins[0]],
    [key_filt_scale.outs[0], key_filt_base.ins[0]],
    [key_shaped.outs[0], key_lpf.ins[0]],
    [key_filt_base.outs[0], key_lpf.ins[1]],
)

# --- FX: Tremolo ---
patch.set_position(C1, 650)
patch.place("comment Tremolo")[0]

patch.set_position(C1, 675)
trem_dial = patch.place("dial")[0]

patch.set_position(C1, 725)
trem_scale = patch.place("/ 12.")[0]

patch.set_position(C1, 760)
trem_sig = patch.place("sig~")[0]

patch.set_position(C1, 795)
trem_osc = patch.place("cycle~")[0]

patch.set_position(C1, 835)
trem_depth = patch.place("*~ 0.25")[0]

patch.set_position(C1, 870)
trem_offset = patch.place("+~ 0.75")[0]

patch.connect(
    [trem_dial.outs[0], trem_scale.ins[0]],
    [trem_scale.outs[0], trem_sig.ins[0]],
    [trem_sig.outs[0], trem_osc.ins[0]],
    [trem_osc.outs[0], trem_depth.ins[0]],
    [trem_depth.outs[0], trem_offset.ins[0]],
)

# --- FX: Phaser ---
patch.set_position(C1 + 150, 650)
patch.place("comment Phaser")[0]

patch.set_position(C1 + 150, 675)
phaser_dial = patch.place("dial")[0]

patch.set_position(C1 + 150, 725)
phaser_rate = patch.place("/ 20.")[0]

patch.set_position(C1 + 150, 760)
phaser_lfo = patch.place("cycle~")[0]

patch.set_position(C1 + 150, 795)
phaser_depth = patch.place("*~ 5")[0]

patch.set_position(C1 + 150, 830)
phaser_offset = patch.place("+~ 10")[0]

patch.set_position(C1 + 150, 870)
phaser_tapin = patch.place("tapin~ 200")[0]

patch.set_position(C1 + 150, 905)
phaser_tapout = patch.place("tapout~")[0]

patch.connect(
    [phaser_dial.outs[0], phaser_rate.ins[0]],
    [phaser_rate.outs[0], phaser_lfo.ins[0]],
    [phaser_lfo.outs[0], phaser_depth.ins[0]],
    [phaser_depth.outs[0], phaser_offset.ins[0]],
    [phaser_offset.outs[0], phaser_tapout.ins[0]],
    [key_lpf.outs[0], phaser_tapin.ins[0]],
    [phaser_tapin.outs[0], phaser_tapout.ins[0]],
)

# --- Mix phaser + tremolo ---
patch.set_position(C1, 910)
phaser_mix = patch.place("+~")[0]

patch.set_position(C1, 945)
trem_amp = patch.place("*~")[0]

patch.connect(
    [key_lpf.outs[0], phaser_mix.ins[0]],
    [phaser_tapout.outs[0], phaser_mix.ins[0]],
    [phaser_mix.outs[0], trem_amp.ins[0]],
    [trem_offset.outs[0], trem_amp.ins[1]],
)

# --- Keyboard volume ---
patch.set_position(C1 + 300, 650)
patch.place("comment KEY VOL")[0]

patch.set_position(C1 + 300, 675)
key_slider = patch.place("slider")[0]

patch.set_position(C1 + 300, 725)
key_vol_scale = patch.place("/ 127.")[0]

patch.set_position(C1 + 300, 760)
key_vol_sig = patch.place("sig~")[0]

patch.set_position(C1, 985)
key_vol = patch.place("*~")[0]

patch.connect(
    [key_slider.outs[0], key_vol_scale.ins[0]],
    [key_vol_scale.outs[0], key_vol_sig.ins[0]],
    [trem_amp.outs[0], key_vol.ins[0]],
    [key_vol_sig.outs[0], key_vol.ins[1]],
)

# Init keyboard controls
patch.set_position(C1 + 300, 800)
key_init_lb = patch.place("loadbang")[0]

patch.set_position(C1 + 300, 835)
key_init_msg = patch.place("message 80")[0]

patch.set_position(C1 + 300, 870)
fx_init_msg = patch.place("message 0")[0]

patch.set_position(C1 + 300, 905)
fx_trem_init = patch.place("message 10")[0]

patch.connect(
    [key_init_lb.outs[0], key_init_msg.ins[0]],
    [key_init_msg.outs[0], key_slider.ins[0]],
    [key_init_lb.outs[0], fx_init_msg.ins[0]],
    [fx_init_msg.outs[0], phaser_dial.ins[0]],
    [key_init_lb.outs[0], fx_trem_init.ins[0]],
    [fx_trem_init.outs[0], trem_dial.ins[0]],
)

# ================================================================
# SECTION 2: DRUMS (Column 2, y=220+)
# ================================================================

# --- Trigger selectors ---
patch.set_position(C2, 220)
patch.place("comment === DRUMS (FIBONACCI PATTERN) ===")[0]

patch.set_position(C2, 255)
kick_trigger = patch.place("sel 0 1 2 3 5 8 13")[0]

patch.set_position(C2, 290)
snare_trigger = patch.place("sel 3 5 8 13")[0]

patch.set_position(C2, 325)
hh_trigger = patch.place("sel 0 1 2 3 5 8 10 13 15")[0]

patch.connect(
    [counter_16.outs[0], kick_trigger.ins[0]],
    [counter_16.outs[0], snare_trigger.ins[0]],
    [counter_16.outs[0], hh_trigger.ins[0]],
)

# --- KICK ---
patch.set_position(C2, 375)
patch.place("comment --- KICK ---")[0]

patch.set_position(C2, 400)
kick_btn = patch.place("button")[0]

patch.set_position(C2, 435)
kick_freq_msg = patch.place("message 150, 50 150")[0]

patch.set_position(C2 + 140, 435)
kick_env_msg = patch.place("message 1, 0 150")[0]

patch.set_position(C2, 475)
kick_freq_line = patch.place("line~")[0]

patch.set_position(C2 + 140, 475)
kick_line = patch.place("line~")[0]

patch.set_position(C2, 515)
kick_osc = patch.place("cycle~")[0]

patch.set_position(C2, 555)
kick_shaped = patch.place("*~")[0]

patch.set_position(C2, 595)
kick_drive = patch.place("*~ 4.0")[0]

patch.set_position(C2, 635)
kick_sat = patch.place("tanh~")[0]

for i in range(7):
    patch.connect([kick_trigger.outs[i], kick_btn.ins[0]])

patch.connect(
    [kick_btn.outs[0], kick_freq_msg.ins[0]],
    [kick_btn.outs[0], kick_env_msg.ins[0]],
    [kick_freq_msg.outs[0], kick_freq_line.ins[0]],
    [kick_env_msg.outs[0], kick_line.ins[0]],
    [kick_freq_line.outs[0], kick_osc.ins[0]],
    [kick_osc.outs[0], kick_shaped.ins[0]],
    [kick_line.outs[0], kick_shaped.ins[1]],
    [kick_shaped.outs[0], kick_drive.ins[0]],
    [kick_drive.outs[0], kick_sat.ins[0]],
)

# Kick volume
patch.set_position(C2 + 140, 555)
patch.place("comment KICK VOL")[0]

patch.set_position(C2 + 140, 580)
kick_slider = patch.place("slider")[0]

patch.set_position(C2 + 140, 630)
kick_vol_scale = patch.place("/ 127.")[0]

patch.set_position(C2 + 140, 665)
kick_vol_sig = patch.place("sig~")[0]

patch.set_position(C2, 675)
kick_vol = patch.place("*~")[0]

patch.connect(
    [kick_slider.outs[0], kick_vol_scale.ins[0]],
    [kick_vol_scale.outs[0], kick_vol_sig.ins[0]],
    [kick_sat.outs[0], kick_vol.ins[0]],
    [kick_vol_sig.outs[0], kick_vol.ins[1]],
)

patch.set_position(C2 + 140, 705)
kick_init_lb = patch.place("loadbang")[0]
patch.set_position(C2 + 140, 740)
kick_init_msg = patch.place("message 100")[0]
patch.connect(
    [kick_init_lb.outs[0], kick_init_msg.ins[0]],
    [kick_init_msg.outs[0], kick_slider.ins[0]],
)

# --- SNARE ---
patch.set_position(C2 + 280, 375)
patch.place("comment --- SNARE ---")[0]

patch.set_position(C2 + 280, 400)
snare_btn = patch.place("button")[0]

patch.set_position(C2 + 280, 435)
snare_noise = patch.place("noise~")[0]

patch.set_position(C2 + 280 + 100, 435)
snare_env_msg = patch.place("message 1, 0 100")[0]

patch.set_position(C2 + 280, 475)
snare_filter = patch.place("svf~ 200 1.5")[0]

patch.set_position(C2 + 280 + 100, 475)
snare_line = patch.place("line~")[0]

patch.set_position(C2 + 280, 515)
snare_shaped = patch.place("*~")[0]

for i in range(4):
    patch.connect([snare_trigger.outs[i], snare_btn.ins[0]])

patch.connect(
    [snare_btn.outs[0], snare_env_msg.ins[0]],
    [snare_noise.outs[0], snare_filter.ins[0]],
    [snare_env_msg.outs[0], snare_line.ins[0]],
    [snare_filter.outs[2], snare_shaped.ins[0]],
    [snare_line.outs[0], snare_shaped.ins[1]],
)

# Snare volume
patch.set_position(C2 + 280 + 100, 515)
patch.place("comment SNR VOL")[0]
patch.set_position(C2 + 280 + 100, 540)
snare_slider = patch.place("slider")[0]
patch.set_position(C2 + 280 + 100, 590)
snare_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C2 + 280 + 100, 625)
snare_vol_sig = patch.place("sig~")[0]
patch.set_position(C2 + 280, 555)
snare_vol = patch.place("*~")[0]

patch.connect(
    [snare_slider.outs[0], snare_vol_scale.ins[0]],
    [snare_vol_scale.outs[0], snare_vol_sig.ins[0]],
    [snare_shaped.outs[0], snare_vol.ins[0]],
    [snare_vol_sig.outs[0], snare_vol.ins[1]],
)

patch.set_position(C2 + 280 + 100, 665)
snare_init_lb = patch.place("loadbang")[0]
patch.set_position(C2 + 280 + 100, 700)
snare_init_msg = patch.place("message 90")[0]
patch.connect(
    [snare_init_lb.outs[0], snare_init_msg.ins[0]],
    [snare_init_msg.outs[0], snare_slider.ins[0]],
)

# --- HI-HAT ---
patch.set_position(C2 + 280, 600)
patch.place("comment --- HI-HAT ---")[0]

patch.set_position(C2 + 280, 625)
hh_btn = patch.place("button")[0]

patch.set_position(C2 + 280, 660)
hh_noise = patch.place("noise~")[0]

patch.set_position(C2 + 280 + 100, 735)
hh_env_msg = patch.place("message 1, 0 40")[0]

patch.set_position(C2 + 280, 700)
hh_filter = patch.place("svf~ 8000 0.7")[0]

patch.set_position(C2 + 280 + 100, 770)
hh_line = patch.place("line~")[0]

patch.set_position(C2 + 280, 740)
hh_shaped = patch.place("*~")[0]

for i in range(9):
    patch.connect([hh_trigger.outs[i], hh_btn.ins[0]])

patch.connect(
    [hh_btn.outs[0], hh_env_msg.ins[0]],
    [hh_noise.outs[0], hh_filter.ins[0]],
    [hh_env_msg.outs[0], hh_line.ins[0]],
    [hh_filter.outs[1], hh_shaped.ins[0]],
    [hh_line.outs[0], hh_shaped.ins[1]],
)

# Hi-hat volume
patch.set_position(C2 + 280 + 100, 810)
patch.place("comment HH VOL")[0]
patch.set_position(C2 + 280 + 100, 835)
hh_slider = patch.place("slider")[0]
patch.set_position(C2 + 280 + 100, 885)
hh_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C2 + 280 + 100, 920)
hh_vol_sig = patch.place("sig~")[0]
patch.set_position(C2 + 280, 780)
hh_vol = patch.place("*~")[0]

patch.connect(
    [hh_slider.outs[0], hh_vol_scale.ins[0]],
    [hh_vol_scale.outs[0], hh_vol_sig.ins[0]],
    [hh_shaped.outs[0], hh_vol.ins[0]],
    [hh_vol_sig.outs[0], hh_vol.ins[1]],
)

patch.set_position(C2 + 280 + 100, 960)
hh_init_lb = patch.place("loadbang")[0]
patch.set_position(C2 + 280 + 100, 995)
hh_init_msg = patch.place("message 70")[0]
patch.connect(
    [hh_init_lb.outs[0], hh_init_msg.ins[0]],
    [hh_init_msg.outs[0], hh_slider.ins[0]],
)

# ================================================================
# SECTION 3: SHIMMER PAD (Column 3, y=220+)
# ================================================================

patch.set_position(C3, 220)
patch.place("comment === SHIMMER PAD (E5,A5,B5) ===")[0]

# Oscillators
patch.set_position(C3, 260)
patch.place("comment E5")[0]
patch.set_position(C3 + 100, 260)
patch.place("comment A5")[0]
patch.set_position(C3 + 200, 260)
patch.place("comment B5")[0]

patch.set_position(C3, 285)
shimmer_e5 = patch.place("cycle~ 659")[0]
patch.set_position(C3 + 100, 285)
shimmer_a5 = patch.place("cycle~ 880")[0]
patch.set_position(C3 + 200, 285)
shimmer_b5 = patch.place("cycle~ 988")[0]

# LFOs (different rates for movement)
patch.set_position(C3, 325)
shimmer_lfo1 = patch.place("cycle~ 0.15")[0]
patch.set_position(C3 + 100, 325)
shimmer_lfo2 = patch.place("cycle~ 0.23")[0]
patch.set_position(C3 + 200, 325)
shimmer_lfo3 = patch.place("cycle~ 0.19")[0]

# Scale LFOs to 0.5-1 range
patch.set_position(C3, 365)
shimmer_lfo1_scale = patch.place("*~ 0.25")[0]
patch.set_position(C3 + 100, 365)
shimmer_lfo2_scale = patch.place("*~ 0.25")[0]
patch.set_position(C3 + 200, 365)
shimmer_lfo3_scale = patch.place("*~ 0.25")[0]

patch.set_position(C3, 400)
shimmer_lfo1_off = patch.place("+~ 0.75")[0]
patch.set_position(C3 + 100, 400)
shimmer_lfo2_off = patch.place("+~ 0.75")[0]
patch.set_position(C3 + 200, 400)
shimmer_lfo3_off = patch.place("+~ 0.75")[0]

patch.connect(
    [shimmer_lfo1.outs[0], shimmer_lfo1_scale.ins[0]],
    [shimmer_lfo1_scale.outs[0], shimmer_lfo1_off.ins[0]],
    [shimmer_lfo2.outs[0], shimmer_lfo2_scale.ins[0]],
    [shimmer_lfo2_scale.outs[0], shimmer_lfo2_off.ins[0]],
    [shimmer_lfo3.outs[0], shimmer_lfo3_scale.ins[0]],
    [shimmer_lfo3_scale.outs[0], shimmer_lfo3_off.ins[0]],
)

# Apply LFOs
patch.set_position(C3, 440)
shimmer_mod1 = patch.place("*~")[0]
patch.set_position(C3 + 100, 440)
shimmer_mod2 = patch.place("*~")[0]
patch.set_position(C3 + 200, 440)
shimmer_mod3 = patch.place("*~")[0]

patch.connect(
    [shimmer_e5.outs[0], shimmer_mod1.ins[0]],
    [shimmer_lfo1_off.outs[0], shimmer_mod1.ins[1]],
    [shimmer_a5.outs[0], shimmer_mod2.ins[0]],
    [shimmer_lfo2_off.outs[0], shimmer_mod2.ins[1]],
    [shimmer_b5.outs[0], shimmer_mod3.ins[0]],
    [shimmer_lfo3_off.outs[0], shimmer_mod3.ins[1]],
)

# Mix + HP filter
patch.set_position(C3, 480)
shimmer_mix = patch.place("+~")[0]

patch.set_position(C3, 520)
shimmer_hpf = patch.place("svf~ 600 0.3")[0]

patch.connect(
    [shimmer_mod1.outs[0], shimmer_mix.ins[0]],
    [shimmer_mod2.outs[0], shimmer_mix.ins[0]],
    [shimmer_mod3.outs[0], shimmer_mix.ins[0]],
    [shimmer_mix.outs[0], shimmer_hpf.ins[0]],
)

# Shimmer volume
patch.set_position(C3 + 150, 480)
patch.place("comment SHIMMER VOL")[0]
patch.set_position(C3 + 150, 505)
shimmer_slider = patch.place("slider")[0]
patch.set_position(C3 + 150, 555)
shimmer_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C3 + 150, 590)
shimmer_vol_sig = patch.place("sig~")[0]

patch.set_position(C3, 560)
shimmer_vol = patch.place("*~")[0]

patch.connect(
    [shimmer_slider.outs[0], shimmer_vol_scale.ins[0]],
    [shimmer_vol_scale.outs[0], shimmer_vol_sig.ins[0]],
    [shimmer_hpf.outs[1], shimmer_vol.ins[0]],
    [shimmer_vol_sig.outs[0], shimmer_vol.ins[1]],
)

patch.set_position(C3 + 150, 630)
shimmer_init_lb = patch.place("loadbang")[0]
patch.set_position(C3 + 150, 665)
shimmer_init_msg = patch.place("message 60")[0]
patch.connect(
    [shimmer_init_lb.outs[0], shimmer_init_msg.ins[0]],
    [shimmer_init_msg.outs[0], shimmer_slider.ins[0]],
)

# ================================================================
# SECTION 4: BASS DRONE (Column 1, y=1050+)
# ================================================================

patch.set_position(C1, 1050)
patch.place("comment === BASS DRONE (55Hz) ===")[0]

patch.set_position(C1, 1085)
drone1 = patch.place("saw~ 55")[0]
patch.set_position(C1 + 90, 1085)
drone2 = patch.place("saw~ 54.7")[0]
patch.set_position(C1 + 180, 1085)
drone3 = patch.place("saw~ 55.3")[0]
patch.set_position(C1 + 270, 1085)
drone_sub = patch.place("cycle~ 27.5")[0]

patch.set_position(C1, 1125)
drone_mix = patch.place("+~")[0]

patch.connect(
    [drone1.outs[0], drone_mix.ins[0]],
    [drone2.outs[0], drone_mix.ins[0]],
    [drone3.outs[0], drone_mix.ins[0]],
    [drone_sub.outs[0], drone_mix.ins[0]],
)

# Filter LFO
patch.set_position(C1 + 150, 1125)
drone_lfo = patch.place("cycle~ 0.1")[0]
patch.set_position(C1 + 150, 1160)
drone_lfo_scale = patch.place("*~ 100")[0]
patch.set_position(C1 + 150, 1195)
drone_lfo_offset = patch.place("+~ 250")[0]

patch.set_position(C1, 1165)
drone_lpf = patch.place("svf~ 250 0.5")[0]

patch.connect(
    [drone_lfo.outs[0], drone_lfo_scale.ins[0]],
    [drone_lfo_scale.outs[0], drone_lfo_offset.ins[0]],
    [drone_mix.outs[0], drone_lpf.ins[0]],
    [drone_lfo_offset.outs[0], drone_lpf.ins[1]],
)

# Drone volume
patch.set_position(C1 + 300, 1050)
patch.place("comment DRONE VOL")[0]
patch.set_position(C1 + 300, 1075)
drone_slider = patch.place("slider")[0]
patch.set_position(C1 + 300, 1125)
drone_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C1 + 300, 1160)
drone_vol_sig = patch.place("sig~")[0]

patch.set_position(C1, 1205)
drone_vol = patch.place("*~")[0]

patch.connect(
    [drone_slider.outs[0], drone_vol_scale.ins[0]],
    [drone_vol_scale.outs[0], drone_vol_sig.ins[0]],
    [drone_lpf.outs[0], drone_vol.ins[0]],
    [drone_vol_sig.outs[0], drone_vol.ins[1]],
)

patch.set_position(C1 + 300, 1200)
drone_init_lb = patch.place("loadbang")[0]
patch.set_position(C1 + 300, 1235)
drone_init_msg = patch.place("message 70")[0]
patch.connect(
    [drone_init_lb.outs[0], drone_init_msg.ins[0]],
    [drone_init_msg.outs[0], drone_slider.ins[0]],
)

# ================================================================
# SECTION 5: MONO SYNTH (Column 2, y=1050+)
# ================================================================

patch.set_position(C2, 1050)
patch.place("comment === MONO SYNTH (440Hz) ===")[0]

patch.set_position(C2, 1085)
synth_osc = patch.place("saw~ 440")[0]

patch.set_position(C2, 1125)
synth_sel = patch.place("sel 2 5 7 10 13 15")[0]

patch.set_position(C2, 1165)
synth_env_msg = patch.place("message 1 3, 0.3 30, 0 50")[0]

patch.set_position(C2, 1205)
synth_env = patch.place("line~")[0]

patch.set_position(C2, 1245)
synth_shaped = patch.place("*~")[0]

patch.set_position(C2, 1285)
synth_lpf = patch.place("svf~ 1200 0.4")[0]

patch.connect(
    [counter_16.outs[0], synth_sel.ins[0]],
)
for i in range(6):
    patch.connect([synth_sel.outs[i], synth_env_msg.ins[0]])
patch.connect(
    [synth_env_msg.outs[0], synth_env.ins[0]],
    [synth_osc.outs[0], synth_shaped.ins[0]],
    [synth_env.outs[0], synth_shaped.ins[1]],
    [synth_shaped.outs[0], synth_lpf.ins[0]],
)

# Synth volume
patch.set_position(C2 + 200, 1050)
patch.place("comment SYNTH VOL")[0]
patch.set_position(C2 + 200, 1075)
synth_slider = patch.place("slider")[0]
patch.set_position(C2 + 200, 1125)
synth_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C2 + 200, 1160)
synth_vol_sig = patch.place("sig~")[0]

patch.set_position(C2, 1325)
synth_vol = patch.place("*~")[0]

patch.connect(
    [synth_slider.outs[0], synth_vol_scale.ins[0]],
    [synth_vol_scale.outs[0], synth_vol_sig.ins[0]],
    [synth_lpf.outs[0], synth_vol.ins[0]],
    [synth_vol_sig.outs[0], synth_vol.ins[1]],
)

patch.set_position(C2 + 200, 1200)
synth_init_lb = patch.place("loadbang")[0]
patch.set_position(C2 + 200, 1235)
synth_init_msg = patch.place("message 100")[0]
patch.connect(
    [synth_init_lb.outs[0], synth_init_msg.ins[0]],
    [synth_init_msg.outs[0], synth_slider.ins[0]],
)

# ================================================================
# SECTION 6: DISSONANT CLUSTER + DELAY (Column 3, y=750+)
# ================================================================

patch.set_position(C3, 750)
patch.place("comment === DISSONANT CLUSTER + DELAY ===")[0]

patch.set_position(C3, 785)
patch.place("comment A4")[0]
patch.set_position(C3 + 90, 785)
patch.place("comment Bb4")[0]
patch.set_position(C3 + 180, 785)
patch.place("comment D#5")[0]

patch.set_position(C3, 810)
diss_a4 = patch.place("saw~ 440")[0]
patch.set_position(C3 + 90, 810)
diss_bb4 = patch.place("saw~ 466")[0]
patch.set_position(C3 + 180, 810)
diss_ds5 = patch.place("saw~ 622")[0]

patch.set_position(C3, 850)
diss_scale1 = patch.place("*~ 0.3")[0]
patch.set_position(C3 + 90, 850)
diss_scale2 = patch.place("*~ 0.3")[0]
patch.set_position(C3 + 180, 850)
diss_scale3 = patch.place("*~ 0.3")[0]

patch.set_position(C3, 890)
diss_mix = patch.place("+~")[0]

patch.connect(
    [diss_a4.outs[0], diss_scale1.ins[0]],
    [diss_bb4.outs[0], diss_scale2.ins[0]],
    [diss_ds5.outs[0], diss_scale3.ins[0]],
    [diss_scale1.outs[0], diss_mix.ins[0]],
    [diss_scale2.outs[0], diss_mix.ins[0]],
    [diss_scale3.outs[0], diss_mix.ins[0]],
)

# LFO swell
patch.set_position(C3 + 150, 890)
diss_lfo = patch.place("cycle~ 0.08")[0]
patch.set_position(C3 + 150, 925)
diss_lfo_scale = patch.place("*~ 0.5")[0]
patch.set_position(C3 + 150, 960)
diss_lfo_off = patch.place("+~ 0.5")[0]

patch.set_position(C3, 930)
diss_shaped = patch.place("*~")[0]

patch.set_position(C3, 970)
diss_lpf = patch.place("svf~ 1200 0.4")[0]

patch.connect(
    [diss_lfo.outs[0], diss_lfo_scale.ins[0]],
    [diss_lfo_scale.outs[0], diss_lfo_off.ins[0]],
    [diss_mix.outs[0], diss_shaped.ins[0]],
    [diss_lfo_off.outs[0], diss_shaped.ins[1]],
    [diss_shaped.outs[0], diss_lpf.ins[0]],
)

# Delay
patch.set_position(C3, 1010)
diss_tapin = patch.place("tapin~ 1000")[0]

patch.set_position(C3, 1050)
diss_tapout1 = patch.place("tapout~ 333")[0]
patch.set_position(C3 + 120, 1050)
diss_tapout2 = patch.place("tapout~ 666")[0]

patch.set_position(C3, 1090)
diss_delay1_scale = patch.place("*~ 0.4")[0]
patch.set_position(C3 + 120, 1090)
diss_delay2_scale = patch.place("*~ 0.25")[0]

patch.set_position(C3, 1130)
diss_delay_mix = patch.place("+~")[0]

patch.connect(
    [diss_lpf.outs[0], diss_tapin.ins[0]],
    [diss_tapin.outs[0], diss_tapout1.ins[0]],
    [diss_tapin.outs[0], diss_tapout2.ins[0]],
    [diss_tapout1.outs[0], diss_delay1_scale.ins[0]],
    [diss_tapout2.outs[0], diss_delay2_scale.ins[0]],
    [diss_lpf.outs[0], diss_delay_mix.ins[0]],
    [diss_delay1_scale.outs[0], diss_delay_mix.ins[0]],
    [diss_delay2_scale.outs[0], diss_delay_mix.ins[0]],
)

# Dissonance volume
patch.set_position(C3 + 200, 1050)
patch.place("comment DISS VOL")[0]
patch.set_position(C3 + 200, 1075)
diss_slider = patch.place("slider")[0]
patch.set_position(C3 + 200, 1125)
diss_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C3 + 200, 1160)
diss_vol_sig = patch.place("sig~")[0]

patch.set_position(C3, 1170)
diss_vol = patch.place("*~")[0]

patch.connect(
    [diss_slider.outs[0], diss_vol_scale.ins[0]],
    [diss_vol_scale.outs[0], diss_vol_sig.ins[0]],
    [diss_delay_mix.outs[0], diss_vol.ins[0]],
    [diss_vol_sig.outs[0], diss_vol.ins[1]],
)

patch.set_position(C3 + 200, 1200)
diss_init_lb = patch.place("loadbang")[0]
patch.set_position(C3 + 200, 1235)
diss_init_msg = patch.place("message 50")[0]
patch.connect(
    [diss_init_lb.outs[0], diss_init_msg.ins[0]],
    [diss_init_msg.outs[0], diss_slider.ins[0]],
)

# ================================================================
# SECTION 7: CHORD SUS4 (Column 1, y=1300+)
# ================================================================

patch.set_position(C1, 1300)
patch.place("comment === CHORD SUS4 (A,D,E) ===")[0]

patch.set_position(C1, 1335)
sus4_a = patch.place("saw~ 880")[0]
patch.set_position(C1 + 90, 1335)
sus4_d = patch.place("saw~ 1175")[0]
patch.set_position(C1 + 180, 1335)
sus4_e = patch.place("saw~ 1319")[0]

patch.set_position(C1, 1375)
sus4_mix = patch.place("+~")[0]

patch.connect(
    [sus4_a.outs[0], sus4_mix.ins[0]],
    [sus4_d.outs[0], sus4_mix.ins[0]],
    [sus4_e.outs[0], sus4_mix.ins[0]],
)

patch.set_position(C1, 1415)
sus4_sel = patch.place("sel 0 3 6 8 11 14")[0]

patch.set_position(C1, 1455)
sus4_env_msg = patch.place("message 1 2, 0.5 20, 0 40")[0]

patch.set_position(C1, 1495)
sus4_env = patch.place("line~")[0]

patch.set_position(C1, 1535)
sus4_shaped = patch.place("*~")[0]

patch.set_position(C1, 1575)
sus4_hpf = patch.place("svf~ 400 0.3")[0]

patch.set_position(C1, 1615)
sus4_lpf = patch.place("svf~ 3000 0.4")[0]

patch.connect([counter_16.outs[0], sus4_sel.ins[0]])
for i in range(6):
    patch.connect([sus4_sel.outs[i], sus4_env_msg.ins[0]])
patch.connect(
    [sus4_env_msg.outs[0], sus4_env.ins[0]],
    [sus4_mix.outs[0], sus4_shaped.ins[0]],
    [sus4_env.outs[0], sus4_shaped.ins[1]],
    [sus4_shaped.outs[0], sus4_hpf.ins[0]],
    [sus4_hpf.outs[1], sus4_lpf.ins[0]],
)

# Sus4 volume
patch.set_position(C1 + 280, 1300)
patch.place("comment SUS4 VOL")[0]
patch.set_position(C1 + 280, 1325)
sus4_slider = patch.place("slider")[0]
patch.set_position(C1 + 280, 1375)
sus4_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C1 + 280, 1410)
sus4_vol_sig = patch.place("sig~")[0]

patch.set_position(C1, 1655)
sus4_vol = patch.place("*~")[0]

patch.connect(
    [sus4_slider.outs[0], sus4_vol_scale.ins[0]],
    [sus4_vol_scale.outs[0], sus4_vol_sig.ins[0]],
    [sus4_lpf.outs[0], sus4_vol.ins[0]],
    [sus4_vol_sig.outs[0], sus4_vol.ins[1]],
)

patch.set_position(C1 + 280, 1450)
sus4_init_lb = patch.place("loadbang")[0]
patch.set_position(C1 + 280, 1485)
sus4_init_msg = patch.place("message 80")[0]
patch.connect(
    [sus4_init_lb.outs[0], sus4_init_msg.ins[0]],
    [sus4_init_msg.outs[0], sus4_slider.ins[0]],
)

# ================================================================
# SECTION 8: CHORD MAJOR (Column 2, y=1400+)
# ================================================================

patch.set_position(C2, 1400)
patch.place("comment === CHORD MAJOR (A,C#,E) ===")[0]

patch.set_position(C2, 1435)
maj_a = patch.place("saw~ 880")[0]
patch.set_position(C2 + 90, 1435)
maj_cs = patch.place("saw~ 1109")[0]
patch.set_position(C2 + 180, 1435)
maj_e = patch.place("saw~ 1319")[0]

patch.set_position(C2, 1475)
maj_mix = patch.place("+~")[0]

patch.connect(
    [maj_a.outs[0], maj_mix.ins[0]],
    [maj_cs.outs[0], maj_mix.ins[0]],
    [maj_e.outs[0], maj_mix.ins[0]],
)

patch.set_position(C2, 1515)
maj_sel = patch.place("sel 2 5 9 12 14")[0]

patch.set_position(C2, 1555)
maj_env_msg = patch.place("message 1 2, 0.5 20, 0 40")[0]

patch.set_position(C2, 1595)
maj_env = patch.place("line~")[0]

patch.set_position(C2, 1635)
maj_shaped = patch.place("*~")[0]

patch.set_position(C2, 1675)
maj_hpf = patch.place("svf~ 400 0.3")[0]

patch.set_position(C2, 1715)
maj_lpf = patch.place("svf~ 3000 0.4")[0]

patch.connect([counter_16.outs[0], maj_sel.ins[0]])
for i in range(5):
    patch.connect([maj_sel.outs[i], maj_env_msg.ins[0]])
patch.connect(
    [maj_env_msg.outs[0], maj_env.ins[0]],
    [maj_mix.outs[0], maj_shaped.ins[0]],
    [maj_env.outs[0], maj_shaped.ins[1]],
    [maj_shaped.outs[0], maj_hpf.ins[0]],
    [maj_hpf.outs[1], maj_lpf.ins[0]],
)

# Major volume
patch.set_position(C2 + 280, 1400)
patch.place("comment MAJ VOL")[0]
patch.set_position(C2 + 280, 1425)
maj_slider = patch.place("slider")[0]
patch.set_position(C2 + 280, 1475)
maj_vol_scale = patch.place("/ 127.")[0]
patch.set_position(C2 + 280, 1510)
maj_vol_sig = patch.place("sig~")[0]

patch.set_position(C2, 1755)
maj_vol = patch.place("*~")[0]

patch.connect(
    [maj_slider.outs[0], maj_vol_scale.ins[0]],
    [maj_vol_scale.outs[0], maj_vol_sig.ins[0]],
    [maj_lpf.outs[0], maj_vol.ins[0]],
    [maj_vol_sig.outs[0], maj_vol.ins[1]],
)

patch.set_position(C2 + 280, 1550)
maj_init_lb = patch.place("loadbang")[0]
patch.set_position(C2 + 280, 1585)
maj_init_msg = patch.place("message 60")[0]
patch.connect(
    [maj_init_lb.outs[0], maj_init_msg.ins[0]],
    [maj_init_msg.outs[0], maj_slider.ins[0]],
)

# ================================================================
# MASTER MIX + OUTPUT
# ================================================================

patch.set_position(C2, 1850)
patch.place("comment === MASTER MIX ===")[0]

patch.set_position(C2, 1885)
master = patch.place("+~")[0]

patch.set_position(C2, 1925)
master_lim = patch.place("*~ 0.5")[0]

patch.set_position(C2, 1965)
clip = patch.place("clip~ -1. 1.")[0]

patch.set_position(C2, 2005)
dac = patch.place("ezdac~")[0]

# All 10 voices into master bus
patch.connect(
    [key_vol.outs[0], master.ins[0]],
    [kick_vol.outs[0], master.ins[0]],
    [snare_vol.outs[0], master.ins[0]],
    [hh_vol.outs[0], master.ins[0]],
    [shimmer_vol.outs[0], master.ins[0]],
    [drone_vol.outs[0], master.ins[0]],
    [synth_vol.outs[0], master.ins[0]],
    [diss_vol.outs[0], master.ins[0]],
    [sus4_vol.outs[0], master.ins[0]],
    [maj_vol.outs[0], master.ins[0]],
    [master.outs[0], master_lim.ins[0]],
    [master_lim.outs[0], clip.ins[0]],
    [clip.outs[0], dac.ins[0]],
    [clip.outs[0], dac.ins[1]],
)

# Instructions
patch.set_position(C2, 2050)
patch.place("comment Turn on ezdac~ - use sliders to mix 10 layers - play kslider for pad synth")[0]

# ================================================================
# SAVE
# ================================================================

patch.save("examples/modular_synth.maxpat")
print("Saved: examples/modular_synth.maxpat")
print(f"Total objects: {patch.num_objs}")
