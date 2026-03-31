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
            500.0,
            200.0,
            195.0,
            90.0
          ],
          "presentation": 1,
          "presentation_rect": [
            0.0,
            0.0,
            195.0,
            90.0
          ],
          "bgcolor": [
            0.12,
            0.12,
            0.14,
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
          "text": "comment === INPUT ==="
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
            330.0,
            30,
            150.0,
            20.0
          ],
          "text": "comment === DETECTOR ==="
        }
      },
      {
        "box": {
          "id": "obj-7",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            330.0,
            65,
            35.0,
            22.0
          ],
          "text": "abs~"
        }
      },
      {
        "box": {
          "id": "obj-8",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            330.0,
            105,
            40.0,
            22.0
          ],
          "text": "slide~ 10 100"
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
            330.0,
            145,
            23.0,
            22.0
          ],
          "text": "+~ 0.0001"
        }
      },
      {
        "box": {
          "id": "obj-10",
          "maxclass": "comment",
          "numinlets": 1,
          "numoutlets": 0,
          "patching_rect": [
            330.0,
            200,
            150.0,
            20.0
          ],
          "text": "comment === GAIN ==="
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
            480.0,
            200,
            31.0,
            22.0
          ],
          "text": "sig~"
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
            330.0,
            235,
            19.0,
            22.0
          ],
          "text": "/~"
        }
      },
      {
        "box": {
          "id": "obj-13",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            330.0,
            275,
            34.0,
            22.0
          ],
          "text": "clip~ 0.0 1.0"
        }
      },
      {
        "box": {
          "id": "obj-14",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            330.0,
            315,
            40.0,
            22.0
          ],
          "text": "slide~ 5 50"
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
            200,
            150.0,
            20.0
          ],
          "text": "comment === OUTPUT ==="
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
          "id": "obj-17",
          "maxclass": "newobj",
          "numinlets": 1,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            275,
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
          "text": "*~"
        }
      },
      {
        "box": {
          "id": "obj-19",
          "maxclass": "newobj",
          "numinlets": 3,
          "numoutlets": 1,
          "outlettype": [
            "signal"
          ],
          "patching_rect": [
            110.0,
            355,
            34.0,
            22.0
          ],
          "text": "clip~ -1.0 1.0"
        }
      },
      {
        "box": {
          "id": "obj-20",
          "maxclass": "newobj",
          "numinlets": 2,
          "numoutlets": 2,
          "outlettype": [
            "signal",
            "signal"
          ],
          "patching_rect": [
            110.0,
            395,
            55.0,
            22.0
          ],
          "text": "plugout~"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "threshold",
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
            10.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.7,
            0.72,
            0.78,
            1.0
          ],
          "dialcolor": [
            0.25,
            0.25,
            0.3,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            1.0,
            1.0,
            1.0
          ],
          "needlecolor": [
            0.6,
            0.6,
            0.65,
            1.0
          ],
          "textcolor": [
            0.85,
            0.85,
            0.9,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Threshold",
              "parameter_shortname": "Thresh",
              "parameter_type": 0,
              "parameter_mmin": 0.01,
              "parameter_mmax": 1.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                0.3
              ],
              "parameter_unitstyle": 1
            }
          },
          "id": "obj-21"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "speed",
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
            70.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.7,
            0.72,
            0.78,
            1.0
          ],
          "dialcolor": [
            0.25,
            0.25,
            0.3,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            1.0,
            1.0,
            1.0
          ],
          "needlecolor": [
            0.6,
            0.6,
            0.65,
            1.0
          ],
          "textcolor": [
            0.85,
            0.85,
            0.9,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Speed",
              "parameter_shortname": "Speed",
              "parameter_type": 0,
              "parameter_mmin": 1.0,
              "parameter_mmax": 100.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                20.0
              ],
              "parameter_unitstyle": 1
            }
          },
          "id": "obj-22"
        }
      },
      {
        "box": {
          "maxclass": "live.dial",
          "varname": "makeup",
          "text": "live.dial",
          "numinlets": 1,
          "numoutlets": 2,
          "outlettype": [
            "",
            "float"
          ],
          "patching_rect": [
            640.0,
            230.0,
            44.0,
            48.0
          ],
          "presentation": 1,
          "presentation_rect": [
            130.0,
            30.0,
            44.0,
            48.0
          ],
          "parameter_enable": 1,
          "activedialcolor": [
            0.7,
            0.72,
            0.78,
            1.0
          ],
          "dialcolor": [
            0.25,
            0.25,
            0.3,
            1.0
          ],
          "activeneedlecolor": [
            1.0,
            1.0,
            1.0,
            1.0
          ],
          "needlecolor": [
            0.6,
            0.6,
            0.65,
            1.0
          ],
          "textcolor": [
            0.85,
            0.85,
            0.9,
            1.0
          ],
          "saved_attribute_attributes": {
            "valueof": {
              "parameter_longname": "Makeup",
              "parameter_shortname": "Gain",
              "parameter_type": 0,
              "parameter_mmin": 1.0,
              "parameter_mmax": 10.0,
              "parameter_initial_enable": 1,
              "parameter_initial": [
                1.0
              ],
              "parameter_unitstyle": 1
            }
          },
          "id": "obj-23"
        }
      },
      {
        "box": {
          "maxclass": "comment",
          "text": "Compressor",
          "numinlets": 1,
          "numoutlets": 0,
          "outlettype": [],
          "patching_rect": [
            500.0,
            300.0,
            80.0,
            20.0
          ],
          "presentation": 1,
          "presentation_rect": [
            8.0,
            4.0,
            100.0,
            16.0
          ],
          "fontsize": 11.0,
          "fontface": 1,
          "textcolor": [
            0.85,
            0.85,
            0.9,
            1.0
          ],
          "id": "obj-24"
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
            "obj-9",
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
            "obj-12",
            1
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
            0
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
            "obj-18",
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
            "obj-18",
            1
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
            "obj-19",
            0
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
            "obj-11",
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
            "obj-17",
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
      }
    ],
    "dependency_cache": [],
    "autosave": 0
  }
}