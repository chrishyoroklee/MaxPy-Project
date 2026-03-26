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
            260.0,
            120.0
          ],
          "presentation": 1,
          "presentation_rect": [
            0.0,
            0.0,
            260.0,
            120.0
          ],
          "bgcolor": [
            0.08,
            0.05,
            0.02,
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
          "maxclass": "panel",
          "text": "panel",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            190.0,
            260.0,
            24.0
          ],
          "presentation": 1,
          "presentation_rect": [
            0.0,
            0.0,
            260.0,
            24.0
          ],
          "bgcolor": [
            0.35,
            0.22,
            0.08,
            1.0
          ],
          "mode": 0,
          "rounded": 0,
          "background": 1,
          "id": "obj-2"
        }
      },
      {
        "box": {
          "maxclass": "comment",
          "text": "FILTER",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            350.0,
            50.0,
            16.0
          ],
          "presentation": 1,
          "presentation_rect": [
            10.0,
            28.0,
            50.0,
            16.0
          ],
          "fontsize": 8.0,
          "fontface": 1,
          "textcolor": [
            0.6,
            0.45,
            0.25,
            1.0
          ],
          "id": "obj-3"
        }
      },
      {
        "box": {
          "maxclass": "comment",
          "text": "ENV",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            360.0,
            40.0,
            16.0
          ],
          "presentation": 1,
          "presentation_rect": [
            185.0,
            28.0,
            40.0,
            16.0
          ],
          "fontsize": 8.0,
          "fontface": 1,
          "textcolor": [
            0.6,
            0.45,
            0.25,
            1.0
          ],
          "id": "obj-4"
        }
      },
      {
        "box": {
          "id": "obj-5",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            30,
            150.0,
            20.0
          ],
          "text": "comment === MIDI INPUT ==="
        }
      },
      {
        "box": {
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 3,
          "outlettype": [
            "int",
            "int",
            "int"
          ],
          "patching_rect": [
            30.0,
            65.0,
            41.0,
            22.0
          ],
          "text": "notein",
          "id": "obj-6"
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            110.0,
            105,
            32.0,
            22.0
          ],
          "text": "mtof"
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
            110.0,
            145,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-9",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            200,
            150.0,
            20.0
          ],
          "text": "comment === OSCILLATORS ==="
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            235,
            37.0,
            22.0
          ],
          "text": "saw~"
        }
      },
      {
        "box": {
          "id": "obj-11",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            200,
            20.0,
            22.0
          ],
          "text": "*~ 0.5"
        }
      },
      {
        "box": {
          "id": "obj-12",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            235,
            43.0,
            22.0
          ],
          "text": "cycle~"
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            275,
            23.0,
            22.0
          ],
          "text": "+~"
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
            110.0,
            315,
            20.0,
            22.0
          ],
          "text": "*~ 0.5"
        }
      },
      {
        "box": {
          "id": "obj-15",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            370,
            150.0,
            20.0
          ],
          "text": "comment === FILTER ==="
        }
      },
      {
        "box": {
          "id": "obj-16",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            405,
            42.0,
            22.0
          ],
          "text": "lores~ 500 0.5"
        }
      },
      {
        "box": {
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            430.0,
            405,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-18",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            430.0,
            445,
            31.0,
            22.0
          ],
          "text": "sig~"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            370,
            20.0,
            22.0
          ],
          "text": "*~ 4"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            280.0,
            405,
            23.0,
            22.0
          ],
          "text": "+~"
        }
      },
      {
        "box": {
          "id": "obj-21",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            480.0,
            30,
            150.0,
            20.0
          ],
          "text": "comment === ENVELOPES ==="
        }
      },
      {
        "box": {
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "int"
          ],
          "patching_rect": [
            400.0,
            65.0,
            29.0,
            22.0
          ],
          "text": "> 0",
          "id": "obj-22"
        }
      },
      {
        "box": {
          "id": "obj-23",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 3,
          "outlettype": [
            "bang",
            "bang",
            ""
          ],
          "patching_rect": [
            480.0,
            105,
            40.0,
            22.0
          ],
          "text": "select 1 0"
        }
      },
      {
        "box": {
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            400.0,
            145.0,
            75.0,
            22.0
          ],
          "text": "0.9 5, 0.6 200",
          "id": "obj-24"
        }
      },
      {
        "box": {
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            520.0,
            145.0,
            45.0,
            22.0
          ],
          "text": "0. 150",
          "id": "obj-25"
        }
      },
      {
        "box": {
          "id": "obj-26",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "bang"
          ],
          "patching_rect": [
            480.0,
            185,
            34.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            400.0,
            240.0,
            70.0,
            22.0
          ],
          "text": "1. 5, 0. 400",
          "id": "obj-27"
        }
      },
      {
        "box": {
          "maxclass": "message",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            ""
          ],
          "patching_rect": [
            520.0,
            240.0,
            42.0,
            22.0
          ],
          "text": "0. 50",
          "id": "obj-28"
        }
      },
      {
        "box": {
          "id": "obj-29",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "bang"
          ],
          "patching_rect": [
            480.0,
            280,
            34.0,
            22.0
          ],
          "text": "line~"
        }
      },
      {
        "box": {
          "id": "obj-30",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            110.0,
            460,
            150.0,
            20.0
          ],
          "text": "comment === OUTPUT ==="
        }
      },
      {
        "box": {
          "id": "obj-31",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            495,
            20.0,
            22.0
          ],
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-32",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            535,
            34.0,
            22.0
          ],
          "text": "clip~ -1.0 1.0"
        }
      },
      {
        "box": {
          "id": "obj-33",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "patching_rect": [
            110.0,
            575,
            55.0,
            22.0
          ],
          "text": "plugout~"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "cutoff",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            600.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            15.0,
            46.0,
            50.0,
            56.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.85,
            0.55,
            0.15,
            1.0
          ],
          "dialcolor": [
            0.3,
            0.2,
            0.08,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "needlecolor": [
            0.7,
            0.55,
            0.35,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Cutoff",
              "parameter_shortname": "Cutoff",
              "parameter_type": 0,
              "parameter_mmin": 100.0,
              "parameter_mmax": 5000.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                500.0
              ],
              "parameter_unitstyle": 1,
              "parameter_exponent": 2.0
            }
          },
          "id": "obj-34"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "reso",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            670.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            95.0,
            46.0,
            50.0,
            56.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.85,
            0.55,
            0.15,
            1.0
          ],
          "dialcolor": [
            0.3,
            0.2,
            0.08,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "needlecolor": [
            0.7,
            0.55,
            0.35,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Reso",
              "parameter_shortname": "Reso",
              "parameter_type": 0,
              "parameter_mmin": 0.0,
              "parameter_mmax": 0.95,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0.5
              ],
              "parameter_unitstyle": 1
            }
          },
          "id": "obj-35"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "decay",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            740.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            190.0,
            46.0,
            50.0,
            56.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.85,
            0.55,
            0.15,
            1.0
          ],
          "dialcolor": [
            0.3,
            0.2,
            0.08,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "needlecolor": [
            0.7,
            0.55,
            0.35,
            1.0
          ],
          "textcolor": [
            1.0,
            0.9,
            0.7,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Decay",
              "parameter_shortname": "Decay",
              "parameter_type": 0,
              "parameter_mmin": 50.0,
              "parameter_mmax": 2000.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                400.0
              ],
              "parameter_unitstyle": 1,
              "parameter_exponent": 2.0
            }
          },
          "id": "obj-36"
        }
      },
      {
        "box": {
          "maxclass": "comment",
          "text": "BASS SYNTH",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            600.0,
            300.0,
            100.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            8.0,
            4.0,
            120.0,
            18.0
          ],
          "fontsize": 12.0,
          "fontface": 1,
          "textcolor": [
            0.95,
            0.75,
            0.35,
            1.0
          ],
          "id": "obj-37"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "destination": [
            "obj-7",
            0
          ],
          "source": [
            "obj-6",
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
            "obj-22",
            0
          ],
          "source": [
            "obj-6",
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
            "obj-8",
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
            "obj-10",
            0
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
            "obj-11",
            0
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
            "obj-13",
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
            "obj-12",
            0
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
            "obj-13",
            1
          ],
          "source": [
            "obj-12",
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
            "obj-16",
            0
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
            "obj-31",
            0
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
            "obj-20",
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
            "obj-16",
            2
          ],
          "source": [
            "obj-18",
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
            "obj-20",
            1
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
            "obj-16",
            1
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
            "obj-23",
            0
          ],
          "source": [
            "obj-22",
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
            "obj-27",
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
            "obj-25",
            0
          ],
          "source": [
            "obj-23",
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
            "obj-28",
            0
          ],
          "source": [
            "obj-23",
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
            "obj-26",
            0
          ],
          "source": [
            "obj-24",
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
            "obj-26",
            0
          ],
          "source": [
            "obj-25",
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
            "obj-31",
            1
          ],
          "source": [
            "obj-26",
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
            "obj-29",
            0
          ],
          "source": [
            "obj-27",
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
            "obj-29",
            0
          ],
          "source": [
            "obj-28",
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
            "obj-19",
            0
          ],
          "source": [
            "obj-29",
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
            "obj-32",
            0
          ],
          "source": [
            "obj-31",
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
            "obj-33",
            0
          ],
          "source": [
            "obj-32",
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
            "obj-33",
            1
          ],
          "source": [
            "obj-32",
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
            "obj-34",
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
            "obj-18",
            0
          ],
          "source": [
            "obj-35",
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