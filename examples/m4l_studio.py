"""
Max for Live Studio (Audio Effect)
===================================
An embedded web browser that loads MaxPyLang Studio inside Ableton Live.

  - jweb loads https://maxpy-studio.vercel.app/?embedded=true
  - Audio passes through transparently (plugin~ → plugout~)
  - User describes a plugin in the chat, downloads the .amxd

Usage in Ableton Live:
  1. Drag the .amxd onto any audio track
  2. Enter your API key in the compact UI
  3. Describe a plugin, click generate
  4. Download the generated .amxd and drag it onto a track
"""

import json
import maxpylang as mp
from maxpylang.maxobject import MaxObject

patch = mp.MaxPatch()


# -- Helper: place objects from raw dicts ------------------------------------
def place_raw(obj_dict, x, y):
    """Create a MaxObject from a raw dict and place it at (x, y)."""
    obj = MaxObject(obj_dict, from_dict=True)
    patch.set_position(x, y)
    patch.place_obj(obj, position=[float(x), float(y)])
    return obj


# ============================================================
# JWEB (embedded browser — fills the device view)
# ============================================================

jweb_browser = place_raw({
    "box": {
        "maxclass": "jweb",
        "text": "jweb",
        "numinlets": 1,
        "numoutlets": 1,
        "outlettype": [""],
        "patching_rect": [30.0, 30.0, 400.0, 300.0],
        "presentation": 1,
        "presentation_rect": [0.0, 0.0, 400.0, 300.0],
        "url": "https://maxpy-studio.vercel.app/?embedded=true",
        "rendermode": 0,
        "disablefind": 1
    }
}, 30, 30)

# ============================================================
# NODE SCRIPT (receives base64 from jweb, saves .amxd to Desktop)
# ============================================================

node_save = place_raw({
    "box": {
        "maxclass": "newobj",
        "text": "node.script save_device.js",
        "numinlets": 1,
        "numoutlets": 2,
        "outlettype": ["", ""],
        "patching_rect": [500.0, 30.0, 160.0, 22.0]
    }
}, 500, 30)

# jweb outlet → node.script inlet
patch.connect([jweb_browser.outs[0], node_save.ins[0]])

# ============================================================
# TRANSPARENT AUDIO PASSTHROUGH (off-screen in presentation)
# ============================================================

plugin = place_raw({
    "box": {
        "maxclass": "newobj",
        "numinlets": 2,
        "numoutlets": 2,
        "outlettype": ["signal", "signal"],
        "patching_rect": [700.0, 30.0, 46.0, 22.0],
        "text": "plugin~"
    }
}, 700, 30)

plugout = place_raw({
    "box": {
        "maxclass": "newobj",
        "numinlets": 2,
        "numoutlets": 0,
        "outlettype": [],
        "patching_rect": [700.0, 70.0, 52.0, 22.0],
        "text": "plugout~"
    }
}, 700, 70)

patch.connect(
    [plugin.outs[0], plugout.ins[0]],
    [plugin.outs[1], plugout.ins[1]],
)

# ============================================================
# SAVE (enable presentation mode, set device width)
# ============================================================

patcher_json = patch.get_json()
patcher_json["patcher"]["openinpresentation"] = 1
patcher_json["patcher"]["devicewidth"] = 400.0

with open("examples/m4l_studio.maxpat", "w") as f:
    json.dump(patcher_json, f, indent=2)
print("Saved: examples/m4l_studio.maxpat")

from amxd import save_amxd
save_amxd(patcher_json, "examples/m4l_studio.amxd", device_type="audio_effect")
print("Saved: examples/m4l_studio.amxd")

print(f"Total objects: {patch.num_objs}")
