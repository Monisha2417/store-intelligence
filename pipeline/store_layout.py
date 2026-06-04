"""
store_layout.py
Generates store_layout.json files for Store 1 and Store 2
based on the floor plan images (Store_1_-_layout.png, store_2_-_layout.png).

How zone coordinates work
─────────────────────────
All polygons use NORMALISED coordinates: values between 0.0 and 1.0
where (0.0, 0.0) is the TOP-LEFT corner of the camera frame
and   (1.0, 1.0) is the BOTTOM-RIGHT corner.

To read coordinates off the layout image:
  x = (distance from left edge) / (total image width)
  y = (distance from top edge)  / (total image height)

Store 1 image dimensions  : ~1528 x 796  px  (landscape, entrance left)
Store 2 image dimensions  : ~960  x 1200 px  (portrait, entrance bottom-centre)

Each zone polygon is a list of [x, y] corner points going clockwise.
"""

import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ─────────────────────────────────────────────────────────────────────────────
# STORE 1
# Layout: landscape rectangle, entrance on the LEFT (existing glass door)
#
#  ┌──────────────────────────────────────────────────────────────┐
#  │ [SALM][TFS][  ][  ][MINIMALIS][AQUALOGI][FOXTAL][JC]  CASH  │
#  │                                                    COUNTER  │
#  │ [FRAGRANCE]        F.O.H        [MAKEUP UNIT]      ACCES    │
#  │ [NAIL UNIT]                                                  │
#  │ [FAC][FAC][MARS+NYBAE][MENS][  ][LOREAL][BEAUT]             │
#  └──────────────────────────────────────────────────────────────┘
#  ↑ entrance (left, existing glass)
#
# Camera assignments (assumed, adjust to match your actual camera positions):
#   CAM_ENTRY_01  — faces the left glass door (captures entry/exit crossing)
#   CAM_FLOOR_01  — overhead/angled, covers back wall (top) + centre floor
#   CAM_FLOOR_02  — covers bottom wall brands
#   CAM_BILLING_01— faces cash counter (right side)
# ─────────────────────────────────────────────────────────────────────────────

STORE_1 = {
    "store_id": "STORE_1",
    "name": "Apex Retail Store 1",
    "open_hours": {"open": "10:00", "close": "21:00"},
    "staff_uniform": {
        "dominant_hue_range": [100, 130],   # blue-ish uniform — adjust if different
        "saturation_min": 80
    },

    # ── Camera definitions ────────────────────────────────────────────────────
    # Each camera has its own coordinate space (0,0 = top-left of THAT camera's frame).
    # Polygons are normalised to that camera's frame.
    "cameras": {

        # Entry camera — left side glass door
        # Frame imagined as a vertical slice covering the door threshold.
        # Person walking IN moves from top of frame → bottom (outside→inside).
        "CAM_ENTRY_01": {
            "type": "entry",
            "description": "Left glass entrance door. Inbound = top→bottom.",
            "zones": {
                "ENTRY": {
                    "polygon": [[0.0, 0.0], [1.0, 0.0], [1.0, 0.50], [0.0, 0.50]],
                    "normalised": True,
                    "note": "Upper half of frame = outside / approaching"
                },
                "EXIT": {
                    "polygon": [[0.0, 0.50], [1.0, 0.50], [1.0, 1.0], [0.0, 1.0]],
                    "normalised": True,
                    "note": "Lower half = inside / leaving"
                }
            }
        },

        # Floor camera 1 — back wall (top of layout) + centre floor
        # Covers: Salm, TFS, blank×2, Minimalis, Aqualogi, Foxtal, JC (back wall)
        #         Fragrance/Nail kiosk (centre-left)
        #         Makeup Unit (centre)
        "CAM_FLOOR_01": {
            "type": "floor",
            "description": "Back wall brands + centre FOH area.",
            "zones": {

                # Back wall — left cluster: Salm, TFS
                # In layout: leftmost ~30% of back wall
                "BACK_WALL_LEFT": {
                    "polygon": [[0.0, 0.0], [0.30, 0.0], [0.30, 0.22], [0.0, 0.22]],
                    "normalised": True,
                    "brands": ["SALM", "TFS"]
                },

                # Back wall — centre cluster: two unlabelled + Minimalis + Aqualogi
                "BACK_WALL_CENTRE": {
                    "polygon": [[0.30, 0.0], [0.65, 0.0], [0.65, 0.22], [0.30, 0.22]],
                    "normalised": True,
                    "brands": ["MINIMALIS", "AQUALOGI"]
                },

                # Back wall — right cluster: Foxtal, JC
                "BACK_WALL_RIGHT": {
                    "polygon": [[0.65, 0.0], [0.85, 0.0], [0.85, 0.22], [0.65, 0.22]],
                    "normalised": True,
                    "brands": ["FOXTAL", "JC"]
                },

                # Fragrance + Nail Unit kiosk — centre-left of floor
                "FRAGRANCE_NAIL": {
                    "polygon": [[0.27, 0.25], [0.40, 0.25], [0.40, 0.72], [0.27, 0.72]],
                    "normalised": True,
                    "brands": ["FRAGRANCE", "NAIL_UNIT"]
                },

                # Makeup Unit — centre of floor (the two-seat makeup table)
                "MAKEUP_UNIT": {
                    "polygon": [[0.47, 0.25], [0.70, 0.25], [0.70, 0.80], [0.47, 0.80]],
                    "normalised": True,
                    "brands": ["MAKEUP_UNIT"]
                },

                # Open floor / aisle between kiosk and makeup unit
                "FOH_AISLE": {
                    "polygon": [[0.40, 0.25], [0.47, 0.25], [0.47, 0.80], [0.40, 0.80]],
                    "normalised": True,
                    "note": "Narrow aisle — mostly transit, low dwell expected"
                }
            }
        },

        # Floor camera 2 — bottom wall brands
        # Covers: Backlit area, Fac, Mars+Nybae, Mens, Lo'real, Beaut
        "CAM_FLOOR_02": {
            "type": "floor",
            "description": "Bottom wall — mass-market brand shelves.",
            "zones": {

                "FACE_CARE": {
                    "polygon": [[0.08, 0.70], [0.32, 0.70], [0.32, 1.0], [0.08, 1.0]],
                    "normalised": True,
                    "brands": ["FAC"]
                },

                "MARS_NYBAE": {
                    "polygon": [[0.32, 0.70], [0.50, 0.70], [0.50, 1.0], [0.32, 1.0]],
                    "normalised": True,
                    "brands": ["MARS_PLUS", "NYBAE"]
                },

                "MENS": {
                    "polygon": [[0.50, 0.70], [0.63, 0.70], [0.63, 1.0], [0.50, 1.0]],
                    "normalised": True,
                    "brands": ["MENS"]
                },

                "LOREAL": {
                    "polygon": [[0.63, 0.70], [0.80, 0.70], [0.80, 1.0], [0.63, 1.0]],
                    "normalised": True,
                    "brands": ["LOREAL"]
                },

                "BEAUTY": {
                    "polygon": [[0.80, 0.70], [0.95, 0.70], [0.95, 1.0], [0.80, 1.0]],
                    "normalised": True,
                    "brands": ["BEAUT"]
                }
            }
        },

        # Billing camera — right side, covers cash counter + accessories
        # Cash counter is the tall unit top-right in the layout.
        # Accessories (cyan box) is below it.
        "CAM_BILLING_01": {
            "type": "billing",
            "description": "Right side: cash counter + accessories zone.",
            "zones": {

                "BILLING": {
                    "polygon": [[0.0, 0.0], [1.0, 0.0], [1.0, 0.55], [0.0, 0.55]],
                    "normalised": True,
                    "note": "Active billing area — person at counter"
                },

                "BILLING_QUEUE": {
                    "polygon": [[0.0, 0.55], [1.0, 0.55], [1.0, 1.0], [0.0, 1.0]],
                    "normalised": True,
                    "note": "Queue buildup zone behind the counter"
                },

                "ACCESSORIES": {
                    "polygon": [[0.60, 0.65], [1.0, 0.65], [1.0, 1.0], [0.60, 1.0]],
                    "normalised": True,
                    "brands": ["ACCES"],
                    "note": "Cyan box bottom-right in layout"
                }
            }
        }
    },

    # ── Master zone catalogue (used by API for metrics + heatmap) ─────────────
    "zones": {
        "ENTRY":             {"label": "Entry",              "sku_zone": None},
        "EXIT":              {"label": "Exit",               "sku_zone": None},
        "BACK_WALL_LEFT":    {"label": "Salm / TFS",         "sku_zone": "HAIRCARE"},
        "BACK_WALL_CENTRE":  {"label": "Minimalis / Aqualogi","sku_zone": "SKINCARE"},
        "BACK_WALL_RIGHT":   {"label": "Foxtal / JC",        "sku_zone": "SKINCARE"},
        "FRAGRANCE_NAIL":    {"label": "Fragrance & Nail",   "sku_zone": "FRAGRANCE"},
        "MAKEUP_UNIT":       {"label": "Makeup Unit",        "sku_zone": "MAKEUP"},
        "FOH_AISLE":         {"label": "FOH Aisle",          "sku_zone": None},
        "FACE_CARE":         {"label": "Face Care (Fac)",    "sku_zone": "FACE"},
        "MARS_NYBAE":        {"label": "Mars+ / Nybae",      "sku_zone": "COLOUR"},
        "MENS":              {"label": "Mens",               "sku_zone": "MENS"},
        "LOREAL":            {"label": "Lo'real",            "sku_zone": "HAIRCARE"},
        "BEAUTY":            {"label": "Beauty",             "sku_zone": "COLOUR"},
        "BILLING":           {"label": "Cash Counter",       "sku_zone": None},
        "BILLING_QUEUE":     {"label": "Billing Queue",      "sku_zone": None},
        "ACCESSORIES":       {"label": "Accessories",        "sku_zone": "ACCESSORIES"}
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# STORE 2
# Layout: portrait/square, entrance at BOTTOM CENTRE (clearly marked)
#
#  ┌──────────────────────────────────────┐
#  │         B.O.H (back of house)        │  ← excluded from all metrics
#  ├──[W7][W8][W9][W10]──CASH──[W11][W12]─┤  ← top wall + billing
#  │[W6]                            [W15] │
#  │[W5]   GONDOLA-2    F.O.H       [W16] │
#  │[W4]                  [MAKEUP]  [W17] │
#  │[W3]   GONDOLA-1                [W18] │
#  │[W2]                                  │
#  │[W1]          ENTRANCE          [W14] │
#  └──────────────────────────────────────┘
#              ↑ ENTRANCE (bottom centre)
#
# Camera assignments:
#   CAM_ENTRY_01   — faces bottom entrance (inbound = bottom→top of frame)
#   CAM_FLOOR_01   — left wall units + gondolas
#   CAM_FLOOR_02   — right wall units + makeup units
#   CAM_FLOOR_03   — top wall (wall units 7-12)
#   CAM_BILLING_01 — cash counter (top centre)
# ─────────────────────────────────────────────────────────────────────────────

STORE_2 = {
    "store_id": "STORE_2",
    "name": "Apex Retail Store 2",
    "open_hours": {"open": "10:00", "close": "21:00"},
    "staff_uniform": {
        "dominant_hue_range": [100, 130],
        "saturation_min": 80
    },

    "cameras": {

        # Entry camera — bottom centre glazing
        # Person walking IN moves from bottom of frame → top (street→store).
        "CAM_ENTRY_01": {
            "type": "entry",
            "description": "Bottom centre glazing — main entrance. Inbound = bottom→top.",
            "zones": {
                "ENTRY": {
                    "polygon": [[0.0, 0.55], [1.0, 0.55], [1.0, 1.0], [0.0, 1.0]],
                    "normalised": True,
                    "note": "Lower half = outside / approaching the door"
                },
                "EXIT": {
                    "polygon": [[0.0, 0.0], [1.0, 0.0], [1.0, 0.55], [0.0, 0.55]],
                    "normalised": True,
                    "note": "Upper half = inside / leaving"
                }
            }
        },

        # Floor camera 1 — left wall (Wall Units 1-6) + Gondola 1 & 2
        "CAM_FLOOR_01": {
            "type": "floor",
            "description": "Left wall units and centre gondolas.",
            "zones": {

                # Wall Units 1-2 (lower left in layout)
                "LEFT_WALL_LOWER": {
                    "polygon": [[0.0, 0.62], [0.16, 0.62], [0.16, 1.0], [0.0, 1.0]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_1", "WALL_UNIT_2"]
                },

                # Wall Units 3-6 (upper left)
                "LEFT_WALL_UPPER": {
                    "polygon": [[0.0, 0.18], [0.16, 0.18], [0.16, 0.62], [0.0, 0.62]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_3", "WALL_UNIT_4", "WALL_UNIT_5", "WALL_UNIT_6"]
                },

                # MK Gondola 1 — lower centre-left (angled in layout)
                "GONDOLA_1": {
                    "polygon": [[0.16, 0.65], [0.46, 0.65], [0.46, 0.95], [0.16, 0.95]],
                    "normalised": True,
                    "fixtures": ["MK_GONDOLA_1"]
                },

                # MK Gondola 2 — upper centre-left
                "GONDOLA_2": {
                    "polygon": [[0.18, 0.33], [0.46, 0.33], [0.46, 0.65], [0.18, 0.65]],
                    "normalised": True,
                    "fixtures": ["MK_GONDOLA_2"]
                }
            }
        },

        # Floor camera 2 — right wall (Wall Units 13-18) + Makeup Units cluster
        "CAM_FLOOR_02": {
            "type": "floor",
            "description": "Makeup units cluster + right wall.",
            "zones": {

                # Makeup Units — centre-right cluster (4 units with chairs)
                "MAKEUP_UNITS": {
                    "polygon": [[0.52, 0.45], [0.80, 0.45], [0.80, 0.82], [0.52, 0.82]],
                    "normalised": True,
                    "fixtures": ["MAKEUP_UNIT_1", "MAKEUP_UNIT_2", "MAKEUP_UNIT_3", "MAKEUP_UNIT_4"]
                },

                # Wall Units 13-14 (lower right)
                "RIGHT_WALL_LOWER": {
                    "polygon": [[0.83, 0.60], [1.0, 0.60], [1.0, 1.0], [0.83, 1.0]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_13", "WALL_UNIT_14"]
                },

                # Wall Units 15-18 (upper right)
                "RIGHT_WALL_UPPER": {
                    "polygon": [[0.83, 0.18], [1.0, 0.18], [1.0, 0.60], [0.83, 0.60]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_15", "WALL_UNIT_16", "WALL_UNIT_17", "WALL_UNIT_18"]
                },

                # Open FOH centre — general floor traffic
                "FOH_CENTRE": {
                    "polygon": [[0.16, 0.33], [0.52, 0.33], [0.52, 0.82], [0.16, 0.82]],
                    "normalised": True,
                    "note": "General floor circulation area"
                }
            }
        },

        # Floor camera 3 — top wall (Wall Units 7-12)
        "CAM_FLOOR_03": {
            "type": "floor",
            "description": "Top wall — Wall Units 7 to 12 (left of cash counter + right).",
            "zones": {

                # Wall Units 7-10 — left of cash counter
                "TOP_WALL_LEFT": {
                    "polygon": [[0.0, 0.0], [0.44, 0.0], [0.44, 0.28], [0.0, 0.28]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_7", "WALL_UNIT_8", "WALL_UNIT_9", "WALL_UNIT_10"]
                },

                # Wall Units 11-12 — right of cash counter
                "TOP_WALL_RIGHT": {
                    "polygon": [[0.56, 0.0], [1.0, 0.0], [1.0, 0.28], [0.56, 0.28]],
                    "normalised": True,
                    "fixtures": ["WALL_UNIT_11", "WALL_UNIT_12"]
                }
            }
        },

        # Billing camera — top centre, cash counter
        "CAM_BILLING_01": {
            "type": "billing",
            "description": "Cash counter — top centre of store.",
            "zones": {
                "BILLING": {
                    "polygon": [[0.0, 0.0], [1.0, 0.0], [1.0, 0.50], [0.0, 0.50]],
                    "normalised": True,
                    "note": "Active counter area"
                },
                "BILLING_QUEUE": {
                    "polygon": [[0.0, 0.50], [1.0, 0.50], [1.0, 1.0], [0.0, 1.0]],
                    "normalised": True,
                    "note": "Queue depth tracking zone"
                }
            }
        }
    },

    # ── Excluded zones (B.O.H — not customer-facing) ──────────────────────────
    "excluded_zones": {
        "BOH": {
            "description": "Back of House — top-right section. Staff only. Excluded from all customer metrics.",
            "polygon": [[0.48, 0.0], [1.0, 0.0], [1.0, 0.42], [0.48, 0.42]],
            "normalised": True
        }
    },

    # ── Master zone catalogue ─────────────────────────────────────────────────
    "zones": {
        "ENTRY":             {"label": "Entrance",           "sku_zone": None},
        "EXIT":              {"label": "Exit",               "sku_zone": None},
        "LEFT_WALL_LOWER":   {"label": "Left Wall Lower",    "sku_zone": "SKINCARE"},
        "LEFT_WALL_UPPER":   {"label": "Left Wall Upper",    "sku_zone": "SKINCARE"},
        "GONDOLA_1":         {"label": "MK Gondola 1",       "sku_zone": "MAKEUP"},
        "GONDOLA_2":         {"label": "MK Gondola 2",       "sku_zone": "MAKEUP"},
        "MAKEUP_UNITS":      {"label": "Makeup Units",       "sku_zone": "MAKEUP"},
        "RIGHT_WALL_LOWER":  {"label": "Right Wall Lower",   "sku_zone": "HAIRCARE"},
        "RIGHT_WALL_UPPER":  {"label": "Right Wall Upper",   "sku_zone": "HAIRCARE"},
        "FOH_CENTRE":        {"label": "Floor Centre",       "sku_zone": None},
        "TOP_WALL_LEFT":     {"label": "Top Wall Left",      "sku_zone": "FRAGRANCE"},
        "TOP_WALL_RIGHT":    {"label": "Top Wall Right",     "sku_zone": "FRAGRANCE"},
        "BILLING":           {"label": "Cash Counter",       "sku_zone": None},
        "BILLING_QUEUE":     {"label": "Billing Queue",      "sku_zone": None}
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# Write JSON files
# ─────────────────────────────────────────────────────────────────────────────

def write(data: dict, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Written: {path}")
    print(f"  Stores  : {data['store_id']}")
    print(f"  Cameras : {list(data['cameras'].keys())}")
    total_zones = sum(len(cam['zones']) for cam in data['cameras'].values())
    print(f"  Zones   : {total_zones} across all cameras")
    print(f"  Master  : {len(data['zones'])} zone entries")
    print()


if __name__ == "__main__":
    print("=" * 55)
    print("  Store Layout Generator")
    print("  Source: Store_1_-_layout.png, store_2_-_layout.png")
    print("=" * 55)
    print()

    write(STORE_1, "store_layout.json")        # default layout used by pipeline
    write(STORE_2, "store_2_layout.json")

    print("Done. Pass the right file to detect.py with --layout:")
    print("  Store 1:  --layout data/store_layout.json")
    print("  Store 2:  --layout data/store_2_layout.json")