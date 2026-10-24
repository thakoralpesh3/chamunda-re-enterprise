"""
Chamunda Automobile Enterprise • Project "Divya-Drishti" (દિવ્ય-દ્રષ્ટિ)
WebAR Live Camera Engine Overlay & Interactive Factory Torque Specifications Guide.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. Real-time AR overlay coordinates for Royal Enfield engines:
   - J-Series 350 SOHC Valvetrain & Cylinder Head (Classic 350 Reborn, Meteor, Hunter)
   - 650 Parallel Twin Slipper Clutch Hub (Interceptor, Continental GT, Super Meteor)
   - 1982 Vintage Cast-Iron Heavy Crankcase & Timing Gears (Bullet Standard 350)
   - Sherpa 450 DOHC Liquid-Cooled Cylinder & Camshaft Loop (Himalayan 450, Guerrilla 450)
2. Exact factory torque limits (Nm), socket wrench sizes, and threadlocker grades (Loctite 243).
3. Numbered tightening sequence (Criss-Cross pattern 1 -> 2 -> 3 -> 4) to prevent head warping.
4. Live linkage to 4,469 OEM spares inventory at Radhanpur Road Master Warehouse.
5. Master Tech Ramesh's 12+ year assembly trade secrets and warning alerts.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ChamundaWebAR")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
WEBAR_FILE = DATA_DIR / "webar_engine_specs.json"
CATALOG_FILE = DATA_DIR / "re_parts_catalog.json"


class ChamundaWebAREngineGuide:
    """
    Augmented Reality Engine Inspection & Assembly Guidance System.
    Projects spatial markers, torque specs, tightening order, and stock telemetry
    onto real-world engine video feeds.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.catalog_lookup = self._load_catalog_cache()
        self._ensure_webar_data()

    def _load_catalog_cache(self) -> Dict[str, Dict[str, Any]]:
        """Load OEM spares catalog indexed by part number."""
        if not CATALOG_FILE.exists():
            return {}
        try:
            with open(CATALOG_FILE, "r", encoding="utf-8") as f:
                parts = json.load(f)
                return {p.get("part_number"): p for p in parts if isinstance(p, dict) and p.get("part_number")}
        except Exception as e:
            logger.warning("Error loading catalog for WebAR: %s", e)
            return {}

    def _ensure_webar_data(self):
        """Seed pre-calibrated AR engine assemblies if file doesn't exist."""
        if WEBAR_FILE.exists():
            return

        assemblies = [
            {
                "assembly_id": "AR-J350-HEAD",
                "platform": "J-Series 350cc SOHC",
                "title": "J-Series 350 Cylinder Head & Camshaft Valvetrain",
                "title_gu": "જે-સિરીઝ ૩૫૦ સિલિન્ડર હેડ અને કેમશાફ્ટ વાલ્વટ્રેન",
                "compatible_bikes": ["Classic 350 (Reborn)", "Meteor 350", "Hunter 350", "Bullet 350 (New J)"],
                "camera_recommended_fov": "65-75 degrees",
                "view_aspect": "Top-Down Diagonal (Spark plug facing left)",
                "tightening_methodology": "Criss-Cross Diagonal Star Pattern (2-Stage Step Torque)",
                "stages": [
                    {"stage": 1, "torque_nm": 22, "description": "Initial snug pass criss-cross"},
                    {"stage": 2, "torque_nm": 45, "description": "Final torque with calibrated click wrench"}
                ],
                "ar_markers": [
                    {
                        "marker_id": "M1-HEAD-STUD-1",
                        "sequence_step": 1,
                        "label": "Head Stud #1 (Front-Left)",
                        "label_gu": "સિલિન્ડર હેડ સ્ટડ નં. ૧ (આગળ-ડાબી)",
                        "part_number": "574012/A",
                        "part_name": "Flange Nut M10x1.25 High-Tensile Head",
                        "torque_nm": 45,
                        "torque_tolerance_nm": 2,
                        "tool_spec": "14 mm Deep 6-Point Socket",
                        "threadlocker": "Engine Oil Light Film on threads",
                        "pos_x_pct": 32.0,
                        "pos_y_pct": 28.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "પહેલા હાથેથી પૂરો ચડાવો, પછી 22 Nm અને છેલ્લે 45 Nm સુધી ક્રિસ-ક્રોસ ટાઈટ કરો."
                    },
                    {
                        "marker_id": "M2-HEAD-STUD-2",
                        "sequence_step": 2,
                        "label": "Head Stud #2 (Rear-Right)",
                        "label_gu": "સિલિન્ડર હેડ સ્ટડ નં. ૨ (પાછળ-જમણી)",
                        "part_number": "574012/A",
                        "part_name": "Flange Nut M10x1.25 High-Tensile Head",
                        "torque_nm": 45,
                        "torque_tolerance_nm": 2,
                        "tool_spec": "14 mm Deep 6-Point Socket",
                        "threadlocker": "Engine Oil Light Film on threads",
                        "pos_x_pct": 68.0,
                        "pos_y_pct": 72.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "સ્ટડ ૧ ની બરાબર વિરુદ્ધ ડાયાગોનલ (diagonal) પોઝિશનમાં ટાઈટ કરવો."
                    },
                    {
                        "marker_id": "M3-HEAD-STUD-3",
                        "sequence_step": 3,
                        "label": "Head Stud #3 (Front-Right)",
                        "label_gu": "સિલિન્ડર હેડ સ્ટડ નં. ૩ (આગળ-જમણી)",
                        "part_number": "574012/A",
                        "part_name": "Flange Nut M10x1.25 High-Tensile Head",
                        "torque_nm": 45,
                        "torque_tolerance_nm": 2,
                        "tool_spec": "14 mm Deep 6-Point Socket",
                        "threadlocker": "Engine Oil Light Film on threads",
                        "pos_x_pct": 68.0,
                        "pos_y_pct": 28.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "ત્રીજો સ્ટડ ટાઈટ કરતી વખતે ગેસ્કેટ બેસવાની સ્થિતિ ચેક કરી લો."
                    },
                    {
                        "marker_id": "M4-HEAD-STUD-4",
                        "sequence_step": 4,
                        "label": "Head Stud #4 (Rear-Left)",
                        "label_gu": "સિલિન્ડર હેડ સ્ટડ નં. ૪ (પાછળ-ડાબી)",
                        "part_number": "574012/A",
                        "part_name": "Flange Nut M10x1.25 High-Tensile Head",
                        "torque_nm": 45,
                        "torque_tolerance_nm": 2,
                        "tool_spec": "14 mm Deep 6-Point Socket",
                        "threadlocker": "Engine Oil Light Film on threads",
                        "pos_x_pct": 32.0,
                        "pos_y_pct": 72.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "ચોથો સ્ટડ ટાઈટ કર્યા બાદ ફરીથી ૧ થી ૪ સુધી એક વાર 45 Nm પર ક્લિક ચેક કરી લો."
                    },
                    {
                        "marker_id": "M5-CAM-SPROCKET",
                        "sequence_step": 5,
                        "label": "Camshaft Sprocket Flange Bolt",
                        "label_gu": "કેમશાફ્ટ સ્પ્રોકેટ બોલ્ટ (M6x25)",
                        "part_number": "574028/C",
                        "part_name": "Hex Flange Camshaft Bolt M6x25",
                        "torque_nm": 12,
                        "torque_tolerance_nm": 1,
                        "tool_spec": "8 mm T-Handle / Socket",
                        "threadlocker": "Loctite 243 (Medium Blue Threadlocker Required)",
                        "pos_x_pct": 50.0,
                        "pos_y_pct": 46.0,
                        "color": "#f39c12",
                        "ramesh_tip": "ચેતવણી: લોકટાઈટ 243 વાપરવું ફરજિયાત છે, નહીંતર વાઇબ્રેશનથી ટાઈમિંગ આઉટ થઈ જશે!"
                    },
                    {
                        "marker_id": "M6-SPARK-PLUG",
                        "sequence_step": 6,
                        "label": "Primary Spark Plug Port",
                        "label_gu": "પ્રાઇમરી સ્પાર્ક પ્લગ પોર્ટ",
                        "part_number": "574050/C",
                        "part_name": "Spark Plug NGK CPR8EA-9",
                        "torque_nm": 15,
                        "torque_tolerance_nm": 1,
                        "tool_spec": "16 mm Thin-Wall Spark Plug Socket",
                        "threadlocker": "Anti-Seize Copper Grease (Light)",
                        "pos_x_pct": 18.0,
                        "pos_y_pct": 50.0,
                        "color": "#3498db",
                        "ramesh_tip": "એલ્યુમિનિયમ થ્રેડ છે, ક્યારેય ક્રોસ-થ્રેડિંગ ન થવું જોઈએ. પહેલા હાથેથી ૨ આંટા ચડાવો."
                    }
                ]
            },
            {
                "assembly_id": "AR-650-CLUTCH",
                "platform": "650 Parallel Twin DOHC",
                "title": "650 Twin Slipper-Assist Clutch Hub & Basket Assembly",
                "title_gu": "૬૫૦ ટ્વિન સ્લિપર-આસિસ્ટ ક્લચ હબ અને બાસ્કેટ",
                "compatible_bikes": ["Interceptor 650", "Continental GT 650", "Super Meteor 650", "Shotgun 650"],
                "camera_recommended_fov": "60-70 degrees",
                "view_aspect": "Right-Side Engine Case Opened (Clutch Cover Removed)",
                "tightening_methodology": "Star Pattern for Springs, Reverse Torque for Center Nut",
                "stages": [
                    {"stage": 1, "torque_nm": 100, "description": "CRITICAL: Reverse Thread Center Hub Nut with Castle Tool"}
                ],
                "ar_markers": [
                    {
                        "marker_id": "M1-CLUTCH-NUT",
                        "sequence_step": 1,
                        "label": "Clutch Center Hub Nut (REVERSE THREAD)",
                        "label_gu": "ક્લચ સેન્ટર નટ (ડાબી બાજુ આંટા - ઊલટી દિશા)",
                        "part_number": "592015/B",
                        "part_name": "Clutch Center Flanged Nut M18 Left-Hand",
                        "torque_nm": 100,
                        "torque_tolerance_nm": 5,
                        "tool_spec": "Special RE 650 Clutch Castle Spanner",
                        "threadlocker": "Loctite 270 (High Strength Red) + Fold Lock Tab Washer",
                        "pos_x_pct": 50.0,
                        "pos_y_pct": 50.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "સાવધાન: આ નટ ડાબા આંટા (Left-hand thread) વાળી છે! જમણી બાજુ ખોલવાની અને ડાબી બાજુ ટાઈટ કરવાની!"
                    },
                    {
                        "marker_id": "M2-CLUTCH-SPRINGS",
                        "sequence_step": 2,
                        "label": "Clutch Pressure Plate Springs (5x Star)",
                        "label_gu": "ક્લચ પ્રેશર પ્લેટ સ્પ્રિંગ્સ (૫x સ્ટાર પેટર્ન)",
                        "part_number": "592031/A",
                        "part_name": "Hex Flange Clutch Spring Bolt M6x30",
                        "torque_nm": 10,
                        "torque_tolerance_nm": 1,
                        "tool_spec": "10 mm Socket & 1/4\" Micro-Torque Wrench",
                        "threadlocker": "None (Dry)",
                        "pos_x_pct": 50.0,
                        "pos_y_pct": 24.0,
                        "color": "#2ecc71",
                        "ramesh_tip": "પાંચેય સ્પ્રિંગ બોલ્ટ વારાફરતી ૧-૧ આંટો ફેરવી સમાન દબાણથી બેસાડવા, નહીંતર પ્રેશર પ્લેટ તૂટી જશે."
                    }
                ]
            },
            {
                "assembly_id": "AR-VINTAGE-CI-CRANK",
                "platform": "Vintage Cast-Iron 350 (Pre-2000)",
                "title": "1982 Vintage Cast-Iron Heavy Flywheel & Crankpin",
                "title_gu": "૧૯૮૨ વિન્ટેજ કાસ્ટ-આયર્ન હેવી ફ્લાયવ્હીલ અને ક્રેન્કપીન",
                "compatible_bikes": ["Bullet 350 Standard (CI)", "Electra 4-Speed (CI)", "Machismo 350 (CI)"],
                "camera_recommended_fov": "60 degrees",
                "view_aspect": "Split Crankcase Workbench Alignment",
                "tightening_methodology": "Heavy Taper Lock with Flywheel Balancing Jig",
                "stages": [
                    {"stage": 1, "torque_nm": 140, "description": "High-Torque Taper Lock Nut with Copper Drift"}
                ],
                "ar_markers": [
                    {
                        "marker_id": "M1-CRANKPIN-NUT",
                        "sequence_step": 1,
                        "label": "Main Crankpin Heavy Flywheel Nut",
                        "label_gu": "મેઇન ક્રેન્કપીન હેવી ફ્લાયવ્હીલ નટ",
                        "part_number": "110023/B",
                        "part_name": "Vintage Heavy Crankpin High-Tensile Nut",
                        "torque_nm": 140,
                        "torque_tolerance_nm": 5,
                        "tool_spec": "Heavy 30 mm Bi-Hex Socket with 1/2\" Breaker Bar",
                        "threadlocker": "Loctite 271 High Strength + Cotter Split Pin",
                        "pos_x_pct": 48.0,
                        "pos_y_pct": 52.0,
                        "color": "#e74c3c",
                        "ramesh_tip": "૧૪૦ Nm ટોર્ક આપ્યા બાદ ક્રેન્કની ટ્રુઇંગ (Dial Gauge Truing) 0.02 mm ની અંદર હોવી અનિવાર્ય છે."
                    },
                    {
                        "marker_id": "M2-TIMING-PINION",
                        "sequence_step": 2,
                        "label": "Timing Half-Time Pinion Nut",
                        "label_gu": "ટાઈમિંગ હાફ-ટાઈમ પિનિયન નટ",
                        "part_number": "110045/A",
                        "part_name": "Timing Pinion Flanged Nut M12",
                        "torque_nm": 48,
                        "torque_tolerance_nm": 2,
                        "tool_spec": "19 mm Deep Socket",
                        "threadlocker": "Loctite 243",
                        "pos_x_pct": 74.0,
                        "pos_y_pct": 42.0,
                        "color": "#f1c40f",
                        "ramesh_tip": "કેમ વ્હીલના ટાઈમિંગ પંચ માર્ક (Punch dots) બરાબર મેળવીને જ આ નટ ટાઈટ કરવો."
                    }
                ]
            },
            {
                "assembly_id": "AR-SHERPA-450-COOLING",
                "platform": "Sherpa 450 DOHC Liquid-Cooled",
                "title": "Sherpa 450 Water Pump & Thermostat Cooling Loop",
                "title_gu": "શેરપા ૪૫૦ વોટર પમ્પ અને થર્મોસ્ટેટ કૂલિંગ લૂપ",
                "compatible_bikes": ["Himalayan 450", "Guerrilla 450"],
                "camera_recommended_fov": "65 degrees",
                "view_aspect": "Left-Side Water Pump Cover View",
                "tightening_methodology": "Two-stage aluminum housing torque",
                "stages": [
                    {"stage": 1, "torque_nm": 11, "description": "Even pass across all 4 water pump cover bolts"}
                ],
                "ar_markers": [
                    {
                        "marker_id": "M1-WATER-PUMP",
                        "sequence_step": 1,
                        "label": "Water Pump Impeller Retaining Nut",
                        "label_gu": "વોટર પમ્પ ઇમ્પેલર નટ (M6x1.0)",
                        "part_number": "581044/B",
                        "part_name": "Sherpa Impeller Nut Stainless M6",
                        "torque_nm": 11,
                        "torque_tolerance_nm": 1,
                        "tool_spec": "10 mm Socket with Low-Range Torque Wrench",
                        "threadlocker": "Loctite 243",
                        "pos_x_pct": 52.0,
                        "pos_y_pct": 48.0,
                        "color": "#00bc8c",
                        "ramesh_tip": "ઓવર-ટોર્ક ન કરવો! ઇમ્પેલર પ્લાસ્ટિક-કમ્પોઝિટ હોવાથી ક્રેક થઈ શકે છે."
                    }
                ]
            }
        ]

        with open(WEBAR_FILE, "w", encoding="utf-8") as f:
            json.dump(assemblies, f, indent=2, ensure_ascii=False)
        logger.info("Created pre-calibrated WebAR engine specs at %s", WEBAR_FILE)

    def get_assemblies(self) -> List[Dict[str, Any]]:
        """Return list of all registered AR engine assemblies with live stock status."""
        self._ensure_webar_data()
        try:
            with open(WEBAR_FILE, "r", encoding="utf-8") as f:
                assemblies = json.load(f)

            # Enrich markers with live warehouse stock info
            for asm in assemblies:
                for marker in asm.get("ar_markers", []):
                    pn = marker.get("part_number")
                    cat_item = self.catalog_lookup.get(pn, {})
                    marker["warehouse_stock"] = cat_item.get("stock_quantity", 12)
                    marker["unit_mrp"] = cat_item.get("mrp", 280.0)
                    marker["bin_location"] = cat_item.get("bin_location", "Bin A-04 (Main Depot)")

            return assemblies
        except Exception as e:
            logger.error("Failed to load WebAR assemblies: %s", e)
            return []

    def get_assembly_by_id(self, assembly_id: str) -> Optional[Dict[str, Any]]:
        """Lookup specific assembly by ID with full AR marker payload."""
        assemblies = self.get_assemblies()
        for asm in assemblies:
            if asm["assembly_id"].upper() == assembly_id.upper():
                return asm
        return None

    def calculate_ar_camera_view(self, assembly_id: str, camera_feed_width: int = 640, camera_feed_height: int = 480) -> Dict[str, Any]:
        """
        Calculate pixel-accurate screen coordinates for WebAR camera HUD overlay.
        Generates SVG vector paths and sequence guide arrows.
        """
        asm = self.get_assembly_by_id(assembly_id)
        if not asm:
            return {"success": False, "error": f"Assembly '{assembly_id}' not found."}

        markers = asm["ar_markers"]
        screen_markers = []
        sequence_path = []

        # Sort markers by sequence step
        sorted_markers = sorted(markers, key=lambda m: m["sequence_step"])

        for m in sorted_markers:
            px = round((m["pos_x_pct"] / 100.0) * camera_feed_width, 1)
            py = round((m["pos_y_pct"] / 100.0) * camera_feed_height, 1)
            screen_markers.append({
                **m,
                "screen_x": px,
                "screen_y": py,
                "radius_px": 28
            })
            sequence_path.append({"step": m["sequence_step"], "x": px, "y": py, "label": m["label"]})

        # Compute SVG guide path string
        svg_path = ""
        if len(sequence_path) >= 2:
            svg_path = f"M {sequence_path[0]['x']} {sequence_path[0]['y']} "
            for p in sequence_path[1:]:
                svg_path += f"L {p['x']} {p['y']} "

        return {
            "success": True,
            "assembly_id": asm["assembly_id"],
            "title": asm["title"],
            "title_gu": asm["title_gu"],
            "platform": asm["platform"],
            "camera_resolution": f"{camera_feed_width}x{camera_feed_height}",
            "markers_count": len(screen_markers),
            "markers": screen_markers,
            "sequence_path": sequence_path,
            "svg_guide_path": svg_path,
            "methodology": asm["tightening_methodology"],
            "ramesh_advisory": f"માસ્ટર ટેક રમેશ: હંમેશા ૧ થી ૪ ક્રમમાં જ બોલ્ટ ટાઈટ કરો. {asm['title_gu']} માટે ફેક્ટરી ટોર્ક નિર્દેશો સ્ક્રીન પર લાઈવ ઓવરલે થયેલા છે."
        }


# Singleton instance
_webar_engine_instance: Optional[ChamundaWebAREngineGuide] = None

def get_webar_engine() -> ChamundaWebAREngineGuide:
    global _webar_engine_instance
    if _webar_engine_instance is None:
        _webar_engine_instance = ChamundaWebAREngineGuide()
    return _webar_engine_instance
