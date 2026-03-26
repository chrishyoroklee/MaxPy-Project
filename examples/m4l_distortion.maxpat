{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 8,
      "minor": 1,
      "revision": 11,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      34.0,
      87.0,
      1372.0,
      779.0
    ],
    "bglocked": 0,
    "openinpresentation": 1,
    "default_fontsize": 12.0,
    "default_fontface": 0,
    "default_fontname": "Arial",
    "gridonopen": 1,
    "gridsize": [
      15.0,
      15.0
    ],
    "gridsnaponopen": 1,
    "objectsnaponopen": 1,
    "statusbarvisible": 2,
    "toolbarvisible": 1,
    "lefttoolbarpinned": 0,
    "toptoolbarpinned": 0,
    "righttoolbarpinned": 0,
    "bottomtoolbarpinned": 0,
    "toolbars_unpinned_last_save": 0,
    "tallnewobj": 0,
    "boxanimatetime": 200,
    "enablehscroll": 1,
    "enablevscroll": 1,
    "devicewidth": 0.0,
    "description": "",
    "digest": "",
    "tags": "",
    "style": "",
    "subpatcher_template": "",
    "assistshowspatchername": 0,
    "boxes": [
      {
        "box": {
          "maxclass": "panel",
          "text": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            200.0,
            180.0,
            90.0
          ],
          "presentation": 1,
          "presentation_rect": [
            0.0,
            0.0,
            180.0,
            90.0
          ],
          "bgcolor": [
            0.18,
            0.06,
            0.04,
            1.0
          ],
          "mode": 0,
          "rounded": 0,
          "background": 1,
          "id": "obj-1"
        }
      },
      {
        "box": {
          "id": "obj-2",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            30,
            150.0,
            20.0
          ],
          "text": "comment === AUDIO INPUT ==="
        }
      },
      {
        "box": {
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "patching_rect": [
            30.0,
            65.0,
            46.0,
            22.0
          ],
          "text": "plugin~",
          "id": "obj-3"
        }
      },
      {
        "box": {
          "id": "obj-4",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            105,
            23.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            145,
            20.0,
            22.0
          ],
          "text": "*~ 0.5"
        }
      },
      {
        "box": {
          "id": "obj-6",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            200,
            150.0,
            20.0
          ],
          "text": "comment === DISTORTION ==="
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            235,
            20.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            235,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            275,
            65.0,
            22.0
          ],
          "text": "overdrive~ 2"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            315,
            42.0,
            22.0
          ],
          "text": "lores~ 3000 0.3"
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            315,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            380,
            150.0,
            20.0
          ],
          "text": "comment === MIX ==="
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            430.0,
            380,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            430.0,
            420,
            20.0,
            22.0
          ],
          "text": "-~ 1.0"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            420,
            20.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            420,
            20.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            460,
            23.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            510.0,
            200,
            150.0,
            20.0
          ],
          "text": "comment === CONTROLS ==="
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "drive",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            430.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            10.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.95,
            0.2,
            0.1,
            1.0
          ],
          "dialcolor": [
            0.35,
            0.1,
            0.05,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "needlecolor": [
            0.8,
            0.6,
            0.5,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Drive",
              "parameter_shortname": "Drive",
              "parameter_type": 0,
              "parameter_mmin": 1.0,
              "parameter_mmax": 50.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                5.0
              ],
              "parameter_unitstyle": 1,
              "parameter_exponent": 2.0
            }
          },
          "id": "obj-19"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "tone",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            500.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            65.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.95,
            0.2,
            0.1,
            1.0
          ],
          "dialcolor": [
            0.35,
            0.1,
            0.05,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "needlecolor": [
            0.8,
            0.6,
            0.5,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Tone",
              "parameter_shortname": "Tone",
              "parameter_type": 0,
              "parameter_mmin": 200.0,
              "parameter_mmax": 8000.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                3000.0
              ],
              "parameter_unitstyle": 1,
              "parameter_exponent": 2.0
            }
          },
          "id": "obj-20"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "mix",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            570.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            120.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.95,
            0.2,
            0.1,
            1.0
          ],
          "dialcolor": [
            0.35,
            0.1,
            0.05,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "needlecolor": [
            0.8,
            0.6,
            0.5,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Mix",
              "parameter_shortname": "Mix",
              "parameter_type": 0,
              "parameter_mmin": 0.0,
              "parameter_mmax": 1.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0.7
              ],
              "parameter_unitstyle": 1
            }
          },
          "id": "obj-21"
        }
      },
      {
        "box": {
          "id": "obj-22",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            510,
            150.0,
            20.0
          ],
          "text": "comment === OUTPUT ==="
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            545,
            34.0,
            22.0
          ],
          "text": "clip~ -1.0 1.0"
        }
      },
      {
        "box": {
          "id": "obj-24",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "patching_rect": [
            110.0,
            585,
            55.0,
            22.0
          ],
          "text": "plugout~"
        }
      },
      {
        "box": {
          "maxclass": "comment",
          "text": "Distortion",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            300.0,
            80.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            10.0,
            6.0,
            100.0,
            18.0
          ],
          "fontsize": 11.0,
          "fontface": 1,
          "textcolor": [
            1.0,
            0.9,
            0.8,
            1.0
          ],
          "id": "obj-25"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-4",
            0
          ],
          "source": [
            "obj-3",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-4",
            1
          ],
          "source": [
            "obj-3",
            1
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-5",
            0
          ],
          "source": [
            "obj-4",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "source": [
            "obj-5",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-16",
            0
          ],
          "source": [
            "obj-5",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-9",
            0
          ],
          "source": [
            "obj-7",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-7",
            1
          ],
          "source": [
            "obj-8",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-10",
            0
          ],
          "source": [
            "obj-9",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-15",
            0
          ],
          "source": [
            "obj-10",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-10",
            1
          ],
          "source": [
            "obj-11",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-14",
            0
          ],
          "source": [
            "obj-13",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-15",
            1
          ],
          "source": [
            "obj-13",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-16",
            1
          ],
          "source": [
            "obj-14",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-17",
            0
          ],
          "source": [
            "obj-15",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-17",
            1
          ],
          "source": [
            "obj-16",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-23",
            0
          ],
          "source": [
            "obj-17",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-8",
            0
          ],
          "source": [
            "obj-19",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-11",
            0
          ],
          "source": [
            "obj-20",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-13",
            0
          ],
          "source": [
            "obj-21",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-24",
            0
          ],
          "source": [
            "obj-23",
            0
          ],
          "midpoints": [
            null
          ]
        }
      },
      {
        "patchline": {
          "destination": [
            "obj-24",
            1
          ],
          "source": [
            "obj-23",
            0
          ],
          "midpoints": [
            null
          ]
        }
      }
    ],
    "dependency_cache": [],
    "autosave": 0
  }
}