"""
Chamunda Automobile Parts & Service - Royal Enfield Custom Resto-Mod,
Vintage Cast-Iron (CI) Heavy Crank Rebirth & Performance Dyno Studio Engine.

Provides algorithmic Resto-Mod quotations, Bill of Materials (BOM) generation from 4,469 parts,
Stage-1 / Stage-2 Dyno Performance tuning estimates with RTO decibel compliance,
Vintage Cast-Iron (CI) Contact Breaker (CB) Point ignition diagnostics, and verifiable HTML blueprints.
"""

import os
import sys
import json
import time
import base64
import io
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import qrcode

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESTOMODS_DIR = DATA_DIR / "restomods"
RESTOMODS_DIR.mkdir(parents=True, exist_ok=True)

# Import inventory manager for 4,469 catalog matching
try:
    from inventory_engine import ChamundaInventoryManager
except ImportError:
    sys.path.insert(0, str(BASE_DIR))
    from inventory_engine import ChamundaInventoryManager


# 4 Iconic Royal Enfield Resto-Mod Archetypes
RESTOMOD_STYLES = {
    "bobber_solo": {
        "style_key": "bobber_solo",
        "name": "Classic Bobber Solo (સિંગલ સીટ બોબર)",
        "tagline": "Stripped-down, slammed posture with low center of gravity",
        "description": "Handcrafted chopped fenders, genuine sprung leather solo tractor seat, drag-bar or mini ape-hangers, short bottle vintage exhaust, floating side-mount license plate with LED stoplight, matte black engine accents with brass tank emblem.",
        "target_models": ["Classic 350", "Bullet 350", "Meteor 350", "Hunter 350"],
        "base_fabrication_cost": 34000,
        "base_paint_cost": 18000,
        "estimated_timeline_days": 14,
        "key_features": [
            "Handcrafted Chopped Steel Rear Fender",
            "Genuine Sprung Leather Solo Saddle",
            "Low-Slung Drag Handlebars (7/8 inch)",
            "Short Bottle Free-Flow Acoustic Silencer",
            "CNC Billet Aluminium Bar-End Mirrors",
            "Side-Mounted Curved License Plate Frame"
        ]
    },
    "cafe_racer": {
        "style_key": "cafe_racer",
        "name": "Urban Cafe Racer (અર્બન કેફે રેસર)",
        "tagline": "Aggressive track posture, clip-on steering, and aerodynamic cowl",
        "description": "Low-mounted CNC clip-on handlebars, aerodynamic rear seat cowl with diamond-stitched seat, rear-set footpeg rearward linkage, twin upswept megaphone cone exhausts, brushed metal knee pads, bar-end round convex mirrors.",
        "target_models": ["Continental GT 650", "Interceptor 650", "Hunter 350", "Classic 350"],
        "base_fabrication_cost": 42000,
        "base_paint_cost": 22000,
        "estimated_timeline_days": 18,
        "key_features": [
            "CNC Clip-on Adjustable Handlebars",
            "Handcrafted Cafe Cowl with Diamond Stitching",
            "Rear-set Aluminum Footpeg Control Links",
            "Twin Upswept Megaphone Brushed Stainless Exhausts",
            "Vintage Ribbed Tank Knee Grips",
            "Lightweight Billet Fork Stabilizer Brace"
        ]
    },
    "desert_scrambler": {
        "style_key": "desert_scrambler",
        "name": "Kutch Desert Scrambler (કચ્છ ડેઝર્ટ સ્ક્રેમ્બલર)",
        "tagline": "High ground clearance, dual-sport knobby tyres, and rally skid guard",
        "description": "Suspension preload lift with extended front fork gaiters, wide crossbar scrambler handlebar with braced clamps, high-mount upswept stainless exhaust with heat guard, heavy-gauge aluminium sump guard, knobby 50/50 terrain tyres, headlight rock cage.",
        "target_models": ["Himalayan 450", "Scram 411", "Hunter 350", "Classic 350"],
        "base_fabrication_cost": 38000,
        "base_paint_cost": 16000,
        "estimated_timeline_days": 12,
        "key_features": [
            "High-Rise Crossbar Enduro Handlebar",
            "4mm Aircraft-Grade Aluminum Sump Skid Plate",
            "High-Mount Upswept Stainless Steel Exhaust",
            "Heavy-Duty Ribbed Fork Rubber Gaiters",
            "Headlight Protective Metal Grill",
            "Block-Pattern Dual-Purpose All-Terrain Tyres"
        ]
    },
    "vintage_heritage_standard": {
        "style_key": "vintage_heritage_standard",
        "name": "Vintage Heritage Cast-Iron Standard (વિન્ટેજ હેરીટેજ સ્ટાન્ડર્ડ)",
        "tagline": "Original 1970-2000s authentic classic aesthetic with hand-drawn Madras pinstriping",
        "description": "Authentic showroom-grade restoration. Madras hand-drawn gold pinstripes over gloss black lacquer, heavy crank balanced flywheel, brass tank plaques, classic chrome crash guard with halogen auxiliary fog lamps, traditional long bottle muffler with iconic thumping acoustic baffle.",
        "target_models": ["Bullet 350 CI", "Bullet 500 CI", "Classic 350", "Electra 350"],
        "base_fabrication_cost": 46000,
        "base_paint_cost": 26000,
        "estimated_timeline_days": 21,
        "key_features": [
            "Authentic Hand-Drawn Gold Madras Pinstriping",
            "15kg Heavy Cast-Iron Crank Dynamic Balancing",
            "Solid Brass Vintage Royal Enfield Tank Emblems",
            "Heavy Gauge Chrome Engine Guard with Highway Pegs",
            "Long-Bottle Vintage Thump Muffler (Factory Baffle)",
            "Dual Split Touring Comfort Seats with Gel Inserts"
        ]
    }
}

# Custom Paint Schemes
CUSTOM_PAINT_THEMES = {
    "british_racing_green": {"name": "British Racing Green Gloss", "cost": 18000, "finish": "Deep High-Gloss Lacquer"},
    "desert_storm_matte": {"name": "Kutch Desert Storm Tan", "cost": 16000, "finish": "Matte Military Texture"},
    "gunmetal_grey_metallic": {"name": "Gunmetal Grey Metallic Flake", "cost": 20000, "finish": "Multi-Coat Metallic Pearl"},
    "royal_maroon_pinstripe": {"name": "Royal Maroon & Hand Gold Pinstripes", "cost": 24000, "finish": "Heritage Madras Handcraft"},
    "chamunda_gold_emerald": {"name": "Chamunda Signature Gold & Emerald", "cost": 28000, "finish": "Limited CEO Custom Edition"}
}

# Performance Tuning Stages
PERFORMANCE_STAGES = {
    "stage_0": {
        "stage_key": "stage_0",
        "name": "Stock Factory OEM Spec",
        "components": ["Factory Standard Exhaust", "Paper OEM Air Filter", "Standard Spark Plug"],
        "bhp_gain": 0.0,
        "torque_gain_nm": 0.0,
        "cost": 0,
        "rto_decibel": 78.5,
        "rto_compliant": True,
        "description": "Pure factory baseline performance with zero mechanical alterations."
    },
    "stage_1": {
        "stage_key": "stage_1",
        "name": "Stage-1 Street Bolt-On Performance",
        "components": [
            "BMC / DNA High-Flow Reusable Air Filter",
            "Free-Flow Slip-on Acoustic Muffler with dB Killer",
            "NGK Laser Iridium IX High-Ignition Spark Plug",
            "Performance Throttle Cam Pulley"
        ],
        "bhp_gain": 3.4,
        "torque_gain_nm": 4.2,
        "cost": 14500,
        "rto_decibel": 82.8,
        "rto_compliant": True,
        "description": "Crisp low-end response, immediate roll-on acceleration, and authentic rumble within RTO <85 dB legal limits."
    },
    "stage_2": {
        "stage_key": "stage_2",
        "name": "Stage-2 Sport Cam & FuelX Piggyback ECU Remap",
        "components": [
            "All Stage-1 Bolt-On Components",
            "FuelX Pro / Powertronic Piggyback ECU Micro-Controller",
            "High-Lift Fast-Ramp Performance Camshaft",
            "Upsized Fuel Injector Nozzle (+15% CC flow)"
        ],
        "bhp_gain": 7.2,
        "torque_gain_nm": 8.6,
        "cost": 36500,
        "rto_decibel": 84.6,
        "rto_compliant": True,
        "description": "Extensive mid-range punch, broadened torque band, and elevated redline performance calibrated on dyno."
    }
}

# Vintage Cast-Iron (CI) Specifications & Diagnostic Rules
VINTAGE_CI_SPECS = {
    "engine_types": ["Standard 350 CI (1970-2009)", "Standard 500 CI (1990-2009)", "Machismo 350 CI", "Electra 4-Speed CI"],
    "cb_point_gap": "0.35 mm to 0.40 mm (0.014 - 0.016 in)",
    "ignition_timing": "0.8 mm (1/32 in) BTDC fully retarded; 32° BTDC fully advanced",
    "pushrod_tappet": "Free rotation with thumb & forefinger; zero vertical/axial play when engine cold",
    "carburetor_jetting": "Mikcarb VM24 (350): Main Jet 110, Pilot 25; Mikcarb VM28 (500): Main 125, Pilot 27.5; Air Screw 1.5 turns out",
    "gearbox": "Albion 4-speed: EP-90 Gear Oil (approx 450 ml); clutch pushrod ball bearing 1/4 inch",
    "flywheel_crank": "15 kg Heavy Twin Flywheels (Left & Right Cast-Iron Bobweights)"
}

VINTAGE_CI_FAULTS = {
    "point_pitted_misfire": {
        "fault_key": "point_pitted_misfire",
        "fault_title": "CB Point Pitting / High RPM Hesitation & Backfiring",
        "fault_title_gu": "CB પોઇન્ટ બળી જવો / હાઇ સ્પીડમાં મિસફાયરિંગ અને ઝટકા મારવા",
        "severity": "HIGH (Ignition Failure)",
        "immediate_action_gu": "૧. એન્જિનના જમણા કવર પરથી CB પોઇન્ટ કેપ ખોલો. ૨. પોઇન્ટના ફેસ પર બળી ગયેલા ખાડા કે ઓઇલ ચેક કરો. ૩. ૪૦૦ નંબરના એમરી પેપરથી પોઇન્ટ ફેસ સાફ કરો. ૪. કેમ લોબ ટોપ પર હોય ત્યારે ફીલર ગેજથી ગેપ બરાબર ૦.૩૫ mm સેટ કરો. ૫. જો સ્પાર્ક પીળો થતો હોય તો કન્ડેન્સર (0.22 uF) બદલો.",
        "immediate_action_en": "1. Remove contact breaker cover on right crankcase. 2. Inspect tungsten contact faces for gray pitting or oil contamination. 3. Clean contacts with 400-grit emery paper and solvent. 4. Set gap to exactly 0.35 mm using feeler gauge at maximum cam opening. 5. Inspect condenser; replace with 0.22 uF unit if arc is yellow.",
        "toolkit_needed": "Feeler Gauge 0.35mm, Small Screwdriver, 400-Grit Emery Paper",
        "spare_parts_needed": ["Royal Enfield Genuine CB Point Set", "Ignition Condenser 0.22 uF"]
    },
    "kickback_timing": {
        "fault_key": "kickback_timing",
        "fault_title": "Violent Kickback / Hard Starting / Advanced Timing Shock",
        "fault_title_gu": "કિક પાછી મારવી (વાયલેન્ટ કિકબેક) / સ્ટાર્ટિંગમાં જોખમ",
        "severity": "HIGH (Mechanical & Physical Hazard)",
        "immediate_action_gu": "૧. કિક પાછી મારવાનું કારણ ટાઇમિંગ વધુ પડતો એડવાન્સ હોવો છે. ૨. ડિસ્ટ્રીબ્યુટર બેઝપ્લેટના બંને સ્ક્રૂ ઢીલા કરો. ૩. બેઝપ્લેટને ક્લોકવાઇઝ હળવી ફેરવી ટાઇમિંગ રિટાર્ડ કરો (0.8 mm BTDC). ૪. કિક મારતા પહેલા ડીકમ્પ્રેશન લીવર દબાવી સિલિન્ડરનું પ્રેશર રિલીઝ કરી એમ્પિયર મીટર સેન્ટર પર લાવો.",
        "immediate_action_en": "1. Severe kickback occurs when ignition fires too far before Top Dead Center. 2. Loosen distributor baseplate screws. 3. Rotate plate slightly clockwise to retard advance. 4. Depress decompressor lever to clear ammeter past center before applying smooth kick stroke.",
        "toolkit_needed": "Flat Screwdriver, Ring Spanner 10mm, Timing Mark Scale",
        "spare_parts_needed": ["Decompressor Valve Kit", "Heavy Duty Kickstart Ratchet Pawl"]
    },
    "albion_gear_slip": {
        "fault_key": "albion_gear_slip",
        "fault_title": "Albion 4-Speed Gear Slipping / 2nd Gear False Neutral",
        "fault_title_gu": "એલ્બિયન ૪-સ્પીડ ગિયર સ્લિપ થવો / ૨જા ગિયરમાં ફોલ્સ ન્યુટ્રલ",
        "severity": "MEDIUM (Transmission Wear)",
        "immediate_action_gu": "૧. એલ્બિયન ૪-સ્પીડ ગિયરબોક્સમાં સિલેક્ટર પોલનું માઇક્રો-શિમ એડજસ્ટમેન્ટ જરૂરી છે. ૨. ન્યુટ્રલ ફાઇન્ડર લીવરનો પ્લે ચેક કરો. ૩. જૂનું ઓઇલ કાઢી નવું EP-90 ગિયર ઓઇલ ભરો. ૪. ક્લચ વાયરનો ફ્રી-પ્લે ૨-૩ mm સેટ કરો જેથી ૧લા અને ૨જા ગિયર વચ્ચે ક્લચ ડ્રેગ ન થાય.",
        "immediate_action_en": "1. Albion 4-speed transmission requires precise shimming on selector ratchet pawl. 2. Inspect external neutral-finder lever linkage for slop. 3. Drain and refill with EP-90 extreme pressure oil. 4. Adjust clutch cable free-play to 2-3 mm to prevent gear dog rounding.",
        "toolkit_needed": "12mm/14mm Box Spanner, Selector Shims, EP-90 Oil",
        "spare_parts_needed": ["Albion Gearbox Selector Ratchet Pawl", "EP-90 Extreme Pressure Gear Lubricant"]
    },
    "pushrod_tappet_noise": {
        "fault_key": "pushrod_tappet_noise",
        "fault_title": "Excessive Pushrod Clatter / Cold Tappet Valve Rattle",
        "fault_title_gu": "પુશરોડ ટેપેટનો વધુ પડતો અવાજ / ખખડવું",
        "severity": "MEDIUM (Acoustic & Wear Issue)",
        "immediate_action_gu": "૧. કાસ્ટ-આયર્ન એન્જિન ગરમ થતાં ફેલાય છે, તેથી ઠંડા એન્જિને ચોક્કસ સેટિંગ કરો. ૨. સિલિન્ડર બેરલ પરથી ટેપેટ વિન્ડો ખોલો. ૩. એન્જિનને કોમ્પ્રેશન સ્ટ્રોકના TDC પર લાવો. ૪. લોકનટ ઢીલો કરી પુશરોડને આંગળીથી ફરે તેવો ફ્રી સેટ કરો (ઉપર-નીચે પ્લે ન હોવો જોઈએ). ૫. સ્પેનર વડે લોકનટ ટાઈટ કરો.",
        "immediate_action_en": "1. Cast-iron cylinder blocks expand when hot; cold setting must be zero lash. 2. Remove side tappet inspection window. 3. Rotate engine to TDC on compression stroke. 4. Adjust pushrod threaded adjuster so it spins freely between fingers with zero vertical end-play. 5. Lock jam nut firmly.",
        "toolkit_needed": "Open Spanners 11mm & 12mm, Tappet Cover Key",
        "spare_parts_needed": ["Hardened Steel Pushrod Pair", "Tappet Inspection Cork Gaskets"]
    },
    "duckbill_breather_leak": {
        "fault_key": "duckbill_breather_leak",
        "fault_title": "Oil Puking from Engine Breather Pipe (Wet Sumping)",
        "fault_title_gu": "એન્જિન બ્રીધર પાઇપમાંથી ઓઇલ બહાર ફેંકવું (વેટ-સમ્પિંગ)",
        "severity": "MEDIUM (Oil Loss / Drainage Issue)",
        "immediate_action_gu": "૧. લાંબા સમય પછી ગાડી ચાલુ કરતાં ઓઇલ સમ્પમાં ભરાઈ જવાથી બ્રીધરમાંથી ઓઇલ નીકળે છે. ૨. સ્વિંગઆર્મ નીચે બ્રીધર પાઇપનું રબર ડકબિલ વાલ્વ સાફ કરો. ૩. એન્જિન શરૂ કરતાં પહેલા સમ્પ બોલ્ટથી વધારાનું ઓઇલ કાઢી લો. ૪. ઓઇલ પંપ ચેક વાલ્વ સ્પ્રિંગ અને બોલ સાફ કરો.",
        "immediate_action_en": "1. Oil drains past check valve during long storage (wet sumping). 2. Clean rubber duckbill slit valve located under swingarm pivot. 3. Drain excess crankcase oil from front magnetic drain plug before running. 4. Inspect oil pump non-return valve ball and seat.",
        "toolkit_needed": "19mm Sump Plug Socket, Pliers, Solvent Spray",
        "spare_parts_needed": ["Rubber Duckbill Breather Valve", "Oil Pump Non-Return Ball & Spring Set"]
    }
}


def generate_qr_base64(data: str, fill_color: str = "#0d2b22", back_color: str = "#ffffff") -> str:
    """Generate high-contrast PNG QR code as base64 data URI."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64_str}"


class ChamundaRestoModStudio:
    """
    Core engine managing Royal Enfield Custom Resto-Mod builds, Bill of Materials (BOM),
    Stage-1/2 performance tuning, and vintage Cast-Iron (CI) diagnostics.
    """

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.restomods_dir = data_dir / "restomods"
        self.restomods_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.restomods_dir / "restomods_db.json"
        self.inv_manager = ChamundaInventoryManager()

    def _load_db(self) -> List[Dict[str, Any]]:
        if self.db_file.exists():
            try:
                return json.loads(self.db_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save_db(self, records: List[Dict[str, Any]]) -> None:
        self.db_file.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    def build_restomod_quote(
        self,
        customer_name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        base_style: str = "bobber_solo",
        custom_paint: str = "british_racing_green",
        stage_tune: str = "stage_1",
        inspector_name: str = "Master Tech Alpesh (Chamunda Automobile)"
    ) -> Dict[str, Any]:
        """
        Generate a complete Resto-Mod architectural build blueprint, Bill of Materials (BOM)
        from 4,469 parts, timeline, dyno power projection, and verifiable digital certificate.
        """
        now = datetime.datetime.now()
        clean_reg = registration_no.upper().strip()
        resto_suffix = f"{int(time.time()) % 10000:04d}"
        resto_id = f"RESTO-RE-{now.strftime('%Y%m%d')}-{resto_suffix}"

        style_info = RESTOMOD_STYLES.get(base_style, RESTOMOD_STYLES["bobber_solo"])
        paint_info = CUSTOM_PAINT_THEMES.get(custom_paint, CUSTOM_PAINT_THEMES["british_racing_green"])
        tune_info = PERFORMANCE_STAGES.get(stage_tune, PERFORMANCE_STAGES["stage_1"])

        # 1. Match genuine components from 4,469 parts catalog
        bom_items = []

        # Exhaust matching
        exhaust_matches = self.inv_manager.filter_parts(query="exhaust", limit=1)
        if not exhaust_matches:
            exhaust_matches = self.inv_manager.filter_parts(query="silencer", limit=1)
        if exhaust_matches:
            em = exhaust_matches[0]
            bom_items.append({
                "category": "Acoustic Exhaust",
                "name": em.get("name", "Royal Enfield Free-Flow Acoustic Silencer"),
                "part_number": em.get("part_number", em.get("oem_number", "OEM-EXH-01")),
                "mrp": float(em.get("mrp", 4200)),
                "qty": 1,
                "notes": "Tuned acoustic chamber with removable baffle"
            })
        else:
            bom_items.append({
                "category": "Acoustic Exhaust",
                "name": "Chamunda Custom Acoustic Megaphone Exhaust",
                "part_number": "CHAM-EXH-MEGA",
                "mrp": 4850.0,
                "qty": 1,
                "notes": "Hand-rolled stainless steel with baffle"
            })

        # Air filter & Intake matching
        air_matches = self.inv_manager.filter_parts(query="air filter", limit=1)
        if air_matches:
            am = air_matches[0]
            bom_items.append({
                "category": "Air Intake & Fuel",
                "name": am.get("name", "High-Flow Conical Air Intake"),
                "part_number": am.get("part_number", am.get("oem_number", "OEM-AF-01")),
                "mrp": float(am.get("mrp", 2200)),
                "qty": 1,
                "notes": "High CFM cotton gauze high-performance filter"
            })

        # Spark Plug
        spark_matches = self.inv_manager.filter_parts(query="spark plug", limit=1)
        if spark_matches:
            sm = spark_matches[0]
            bom_items.append({
                "category": "Ignition Electrical",
                "name": sm.get("name", "Laser Iridium Extreme Ignition Plug"),
                "part_number": sm.get("part_number", sm.get("oem_number", "OEM-PLUG-IRID")),
                "mrp": float(sm.get("mrp", 750)),
                "qty": 2 if "650" in bike_model or "TWIN" in bike_model.upper() else 1,
                "notes": "Fine-wire iridium tip for cold starting and throttle crispness"
            })

        # Custom Handlebars & Controls
        bom_items.append({
            "category": "Chassis & Ergonomics",
            "name": f"Handcrafted {style_info['name'].split('(')[0].strip()} Handlebar Assembly",
            "part_number": "CHAM-HBAR-CUSTOM",
            "mrp": 3800.0,
            "qty": 1,
            "notes": "Heavy-wall seamless mild steel with powdercoat finish"
        })

        # Custom Seating
        bom_items.append({
            "category": "Upholstery & Saddle",
            "name": f"Chamunda Hand-Stitched Saddle ({style_info['name'].split('(')[0].strip()})",
            "part_number": "CHAM-SEAT-LEATHER",
            "mrp": 6200.0,
            "qty": 1,
            "notes": "High-density molded foam with genuine oil-pull leather"
        })

        # Lighting & Electronics
        bom_items.append({
            "category": "LED Lighting",
            "name": "Cast-Aluminium Vintage Projector LED Headlamp & Micro Indicators",
            "part_number": "CHAM-LED-VINTAGE",
            "mrp": 4500.0,
            "qty": 1,
            "notes": "IP67 waterproof warm-white retro light pattern"
        })

        # Financial Calculations
        parts_total = sum(it["mrp"] * it["qty"] for it in bom_items)
        fab_cost = float(style_info["base_fabrication_cost"])
        paint_cost = float(paint_info["cost"])
        tune_cost = float(tune_info["cost"])
        dyno_labor_cost = 8500.0
        vintage_cost = 12500.0 if ("vintage" in base_style or "vintage" in custom_paint) else 0.0

        grand_total = parts_total + fab_cost + paint_cost + tune_cost + dyno_labor_cost + vintage_cost
        timeline_days = style_info["estimated_timeline_days"] + (4 if stage_tune == "stage_2" else 0)

        # Dynamic QR Code linking to online blueprint
        qr_url = f"http://127.0.0.1:8080/restomod/{resto_id}"
        qr_b64 = generate_qr_base64(qr_url, fill_color="#0d2b22", back_color="#ffffff")

        # Generate HTML Blueprint Document
        blueprint_file = self.restomods_dir / f"{resto_id}.html"
        html_markup = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Resto-Mod Blueprint {resto_id} - Chamunda Automobile</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 30px;
            background: #091713;
            color: #e6edf3;
        }}
        .blueprint-card {{
            max-width: 900px;
            margin: auto;
            background: #11221c;
            border: 2px solid #D4AF37;
            border-top: 8px solid #D4AF37;
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #1d382e;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .brand-title {{
            font-size: 24px;
            font-weight: 800;
            color: #D4AF37;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }}
        .brand-sub {{
            color: #9ca3af;
            font-size: 13px;
            margin-top: 4px;
        }}
        .badge-style {{
            background: #0d2b22;
            color: #D4AF37;
            border: 1px solid #D4AF37;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        }}
        .table-custom {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .table-custom th, .table-custom td {{
            padding: 10px 14px;
            border: 1px solid #1d382e;
            font-size: 13px;
        }}
        .table-custom th {{
            background: #0d2b22;
            color: #D4AF37;
            text-align: left;
        }}
        .spec-box {{
            background: #071712;
            border: 1px solid #1d382e;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .total-box {{
            background: #071712;
            border: 2px solid #D4AF37;
            border-radius: 8px;
            padding: 20px;
            margin-top: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .footer {{
            text-align: center;
            margin-top: 25px;
            padding-top: 15px;
            border-top: 1px solid #1d382e;
            font-size: 12px;
            color: #8b949e;
        }}
        @media print {{
            body {{ background: white; color: black; padding: 0; }}
            .blueprint-card {{ border: 1px solid #000; box-shadow: none; background: white; color: black; }}
            .table-custom th {{ background: #eee !important; color: black !important; }}
            .table-custom td {{ border-color: #ccc; }}
            .spec-box, .total-box {{ background: #fafafa; border-color: #000; color: black; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="blueprint-card">
        <div class="header">
            <div>
                <div class="brand-title">👑 CHAMUNDA RESTO-MOD &amp; PERFORMANCE STUDIO</div>
                <div class="brand-sub">ROYAL ENFIELD BESPOKE ARCHITECTURE &amp; DYNO BLUEPRINT</div>
            </div>
            <div class="badge-style">
                {style_info['name']}
            </div>
        </div>

        <div class="spec-box">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                <div><strong>Client Name:</strong> {customer_name} ({phone})</div>
                <div><strong>Motorcycle:</strong> {bike_model} (<code>{clean_reg}</code>)</div>
                <div><strong>Paint Scheme:</strong> {paint_info['name']} ({paint_info['finish']})</div>
                <div><strong>Performance Tune:</strong> {tune_info['name']} (+{tune_info['bhp_gain']} BHP / +{tune_info['torque_gain_nm']} Nm)</div>
                <div><strong>Estimated Build Duration:</strong> {timeline_days} Working Days</div>
                <div><strong>Blueprint ID:</strong> <code>{resto_id}</code></div>
            </div>
        </div>

        <h4 style="color: #D4AF37; margin-bottom: 8px;">📦 Bill of Materials (BOM) &amp; Component Outlay</h4>
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Component &amp; Specification</th>
                    <th>Part Number</th>
                    <th>Qty</th>
                    <th>MRP (₹)</th>
                </tr>
            </thead>
            <tbody>
"""
        for it in bom_items:
            html_markup += f"""
                <tr>
                    <td><strong style="color: #F5D76E;">{it['category']}</strong></td>
                    <td>{it['name']}<br><small style="color: #8b949e;">{it['notes']}</small></td>
                    <td><code>{it['part_number']}</code></td>
                    <td>{it['qty']}</td>
                    <td>₹{it['mrp']:,.2f}</td>
                </tr>
            """

        html_markup += f"""
            </tbody>
        </table>

        <h4 style="color: #D4AF37; margin-bottom: 8px;">🔨 Labor, Paint &amp; Fabrication Breakdown</h4>
        <table class="table-custom">
            <tr>
                <td><strong>Chassis Modification &amp; Metal Fabrication</strong></td>
                <td style="text-align: right;">₹{fab_cost:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Custom Paint &amp; Surface Treatment ({paint_info['name']})</strong></td>
                <td style="text-align: right;">₹{paint_cost:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Dyno Tuning &amp; Electronics ({tune_info['name']})</strong></td>
                <td style="text-align: right;">₹{tune_cost:,.2f}</td>
            </tr>
            <tr>
                <td><strong>Master Assembly, Tappet Balancing &amp; Road Trial Labor</strong></td>
                <td style="text-align: right;">₹{dyno_labor_cost:,.2f}</td>
            </tr>
        </table>

        <div class="total-box">
            <div>
                <div style="font-size: 13px; color: #8b949e;">TOTAL ALL-INCLUSIVE ESTIMATED INVESTMENT</div>
                <div style="font-size: 26px; font-weight: 800; color: #D4AF37;">₹{grand_total:,.2f}</div>
                <div style="font-size: 12px; color: #10b981;">✓ 6-Month Chamunda Resto Warranty &amp; Dyno Pass Included</div>
            </div>
            <div style="text-align: right;">
                <img src="{qr_b64}" style="width: 80px; height: 80px; border-radius: 4px; border: 1px solid #D4AF37;" alt="QR">
            </div>
        </div>

        <div class="footer">
            Chamunda Automobile Parts &amp; Service • NH-48, Gujarat • Royal Enfield Specialists • Chief Builder: {inspector_name}
        </div>

        <div class="no-print" style="margin-top: 20px; text-align: center;">
            <button onclick="window.print()" style="padding: 10px 24px; background: #0d2b22; color: #D4AF37; border: 2px solid #D4AF37; border-radius: 6px; font-weight: bold; cursor: pointer;">
                🖨️ Print Resto-Mod Blueprint &amp; Quote
            </button>
        </div>
    </div>
</body>
</html>
"""
        blueprint_file.write_text(html_markup, encoding="utf-8")

        # Bilingual WhatsApp messages
        wa_gu = f"""👑 *ચામુંડા રોયલ એનફિલ્ડ કસ્ટમ રેસ્ટો-મોડ બ્લુપ્રિન્ટ*
નમસ્તે {customer_name},
આપના {bike_model} ({clean_reg}) માટે કસ્ટમ {style_info['name']} બ્લુપ્રિન્ટ તૈયાર છે:
🎨 *પેઇન્ટ:* {paint_info['name']}
⚡ *પરફોર્મન્સ:* {tune_info['name']} (+{tune_info['bhp_gain']} BHP)
⏱️ *સમયગાળો:* {timeline_days} દિવસ
💰 *કુલ એસ્ટીમેટ:* ₹{grand_total:,.2f}
📱 *ડિજિટલ બ્લુપ્રિન્ટ જુઓ:* {qr_url}

ચામુંડા ઓટોમોબાઇલ - રોયલ એનફિલ્ડ સ્પેશિયાલિસ્ટ્સ"""

        wa_en = f"""👑 *Chamunda Royal Enfield Custom Resto-Mod Blueprint*
Dear {customer_name},
Custom {style_info['name'].split('(')[0].strip()} blueprint for your {bike_model} ({clean_reg}) is ready:
🎨 *Paint:* {paint_info['name']}
⚡ *Performance:* {tune_info['name']} (+{tune_info['bhp_gain']} BHP)
⏱️ *Timeline:* {timeline_days} Working Days
💰 *Total Investment:* ₹{grand_total:,.2f}
📱 *View Blueprint:* {qr_url}

Chamunda Automobile - Royal Enfield Specialists"""

        # Format bom_parts list
        bom_parts = [
            {
                "sku": itm.get("part_number", "OEM-RE-PART"),
                "name": itm.get("name", "Royal Enfield Component"),
                "category": itm.get("category", "General"),
                "quantity": 1,
                "unit_price": itm.get("price", 0),
                "total_price": itm.get("price", 0),
                "notes": itm.get("notes", "")
            }
            for itm in bom_items
        ]

        cost_breakdown = {
            "style_labor": fab_cost,
            "paint_finish": paint_cost,
            "performance_tuning": tune_cost + dyno_labor_cost,
            "vintage_ci_package": vintage_cost,
            "bom_spares": parts_total
        }

        perf_specs = {
            "hp_gain": f"+{tune_info['bhp_gain']} HP",
            "torque_gain": f"+{tune_info['torque_gain_nm']} Nm",
            "top_speed_gain": "+15-20 km/h" if tune_info["bhp_gain"] > 4 else "+8-12 km/h",
            "accel_improvement": "-1.5s (0-60 km/h)" if tune_info["bhp_gain"] > 4 else "-0.7s (0-60 km/h)",
            "exhaust_note_db": f"{tune_info['rto_decibel']} dB",
            "rto_legal_noise": tune_info["rto_compliant"]
        }

        record = {
            "resto_id": resto_id,
            "blueprint_id": resto_id,
            "timestamp": now.isoformat(),
            "customer_name": customer_name,
            "phone": phone,
            "bike_model": bike_model,
            "registration_no": clean_reg,
            "base_style": base_style,
            "style_name": style_info["name"],
            "style_name_gu": style_info["name"].split("(")[-1].replace(")", "") if "(" in style_info["name"] else style_info["name"],
            "custom_paint": custom_paint,
            "paint_name": paint_info["name"],
            "stage_tune": stage_tune,
            "performance_stage": tune_info["name"],
            "tune_name": tune_info["name"],
            "bhp_gain": tune_info["bhp_gain"],
            "torque_gain_nm": tune_info["torque_gain_nm"],
            "rto_compliant": tune_info["rto_compliant"],
            "timeline_days": timeline_days,
            "parts_total": parts_total,
            "fabrication_cost": fab_cost,
            "paint_cost": paint_cost,
            "tune_cost": tune_cost,
            "cost_breakdown": cost_breakdown,
            "performance_specs": perf_specs,
            "grand_total": grand_total,
            "bom_items": bom_items,
            "bom_parts": bom_parts,
            "blueprint_html_file": str(blueprint_file),
            "blueprint_html_path": str(blueprint_file),
            "qr_code_base64": qr_b64,
            "whatsapp_message_gu": wa_gu,
            "whatsapp_message_en": wa_en
        }

        records = self._load_db()
        records.insert(0, record)
        self._save_db(records)

        return record

    def calculate_performance_stage_tune(self, bike_model: str, stage: str = "stage_1") -> Dict[str, Any]:
        """
        Calculates dyno horsepower and torque improvements for Stage-1 or Stage-2 tuning.
        Evaluates RTO legal decibel noise compliance (<85 dB limit).
        """
        tune_data = PERFORMANCE_STAGES.get(stage, PERFORMANCE_STAGES["stage_1"])

        # Baseline specs by engine family
        base_hp = 20.2
        base_torque = 27.0
        if "650" in bike_model:
            base_hp = 47.0
            base_torque = 52.0
        elif "450" in bike_model:
            base_hp = 40.0
            base_torque = 40.0
        elif "411" in bike_model:
            base_hp = 24.3
            base_torque = 32.0
        elif "500" in bike_model:
            base_hp = 27.2
            base_torque = 41.3

        hp_gain = tune_data["bhp_gain"]
        torque_gain = tune_data["torque_gain_nm"]
        final_hp = round(base_hp + hp_gain, 1)
        final_torque = round(base_torque + torque_gain, 1)

        return {
            "bike_model": bike_model,
            "stage_key": stage,
            "stage_name": tune_data["name"],
            "baseline_hp": base_hp,
            "baseline_torque_nm": base_torque,
            "hp_gain": hp_gain,
            "torque_gain_nm": torque_gain,
            "projected_hp": final_hp,
            "projected_torque_nm": final_torque,
            "estimated_cost_inr": tune_data["cost"],
            "acoustic_db": tune_data["rto_decibel"],
            "rto_legal_compliant": tune_data["rto_compliant"],
            "components": tune_data["components"],
            "tuning_summary_en": f"{tune_data['name']} yields +{hp_gain} BHP (Total: {final_hp} BHP) and +{torque_gain} Nm torque (Total: {final_torque} Nm). RTO sound: {tune_data['rto_decibel']} dB ({'Legal' if tune_data['rto_compliant'] else 'Exceeds Limit'}).",
            "tuning_summary_gu": f"{tune_data['name']} થી +{hp_gain} BHP (કુલ: {final_hp} BHP) અને +{torque_gain} Nm ટોર્ક (કુલ: {final_torque} Nm) મળે છે. સાઉન્ડ લેવલ {tune_data['rto_decibel']} dB છે (RTO માન્ય)."
        }

    def diagnose_vintage_ci_bullet(self, symptom_query: str, engine_cc: int = 350) -> Dict[str, Any]:
        """
        Expert mechanical diagnostic guidance for classic Cast-Iron (CI) Bullets (1970-2009).
        Delivers Contact Breaker (CB) point timing directives, Albion 4-speed shimming,
        pushrod tappet setting, and decompressor tuning in Gujarati & English.
        """
        q = symptom_query.lower()
        matched_key = "point_pitted_misfire"

        if any(w in q for w in ["kickback", "કિક", "પાછી", "advance", "timing", "ટાંઇમિંગ"]):
            matched_key = "kickback_timing"
        elif any(w in q for w in ["gear", "ગિયર", "albion", "એલ્બિયન", "slip", "સ્લિપ", "neutral", "ન્યુટ્રલ"]):
            matched_key = "albion_gear_slip"
        elif any(w in q for w in ["tappet", "ટેપેટ", "pushrod", "પુશરોડ", "clatter", "અવાજ"]):
            matched_key = "pushrod_tappet_noise"
        elif any(w in q for w in ["duckbill", "બ્રીધર", "breather", "leak", "sump", "ઓઇલ", "ફેંકવું"]):
            matched_key = "duckbill_breather_leak"
        elif any(w in q for w in ["point", "પોઇન્ટ", "cb", "misfire", "મિસફાયર", "ઝટકા", "spark"]):
            matched_key = "point_pitted_misfire"

        fault = VINTAGE_CI_FAULTS[matched_key]
        parts_list = [
            {
                "part_name": sp,
                "part_number": "RE-CI-" + "".join([c[0] for c in sp.split() if c]).upper() + "-OEM",
                "approx_mrp": 450,
                "function": "Original factory calibration replacement"
            }
            for sp in fault["spare_parts_needed"]
        ]
        return {
            "symptom_queried": symptom_query,
            "engine_cc": engine_cc,
            "fault_key": matched_key,
            "fault_name": fault["fault_title"],
            "fault_name_gu": fault["fault_title_gu"],
            "fault_title": fault["fault_title"],
            "fault_title_gu": fault["fault_title_gu"],
            "severity": fault["severity"],
            "root_cause": fault.get("description", fault["fault_title"]),
            "factory_tolerance_specs": f"CB Gap: {VINTAGE_CI_SPECS['cb_point_gap']} | Timing: {VINTAGE_CI_SPECS['ignition_timing']} | Tappet: {VINTAGE_CI_SPECS['pushrod_tappet']}",
            "immediate_action_en": fault["immediate_action_en"],
            "immediate_action_gu": fault["immediate_action_gu"],
            "mechanic_directive_en": fault["immediate_action_en"],
            "mechanic_directive_gu": fault["immediate_action_gu"],
            "toolkit_needed": fault["toolkit_needed"],
            "spare_parts_needed": fault["spare_parts_needed"],
            "parts_needed": parts_list,
            "factory_specs": VINTAGE_CI_SPECS,
            "master_tech": "Master Tech Alpesh (Chamunda Automobile Vintage CI Specialist)"
        }

    def get_restomod_blueprint(self, resto_id: str) -> Optional[Dict[str, Any]]:
        """Fetch custom resto-mod record by ID."""
        for r in self._load_db():
            if r.get("resto_id") == resto_id or r.get("blueprint_id") == resto_id:
                return r
        return None

    def get_all_restomods(self, limit: int = 50) -> List[Dict[str, Any]]:
        """List all past custom resto-mod quotes and builds."""
        records = self._load_db()
        return records[:limit]
    def generate_restomod_quote(
        self,
        customer_name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        style_key: str = "bobber_solo",
        paint_theme_key: str = "british_racing_green",
        performance_stage_key: str = "stage_1",
        include_vintage_ci_package: bool = False,
        custom_notes: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Universal alias for build_restomod_quote with flexible style, paint, and stage key resolution.
        """
        # Map paint themes if needed
        paint_map = {
            "british_racing_green_gold": "british_racing_green",
            "matte_phantom_black": "gunmetal_grey_metallic",
            "desert_sand_patina": "desert_storm_matte",
            "candy_royal_maroon": "royal_maroon_pinstripe",
            "vintage_gunmetal_silver": "gunmetal_grey_metallic"
        }
        resolved_paint = paint_map.get(paint_theme_key, paint_theme_key)
        if resolved_paint not in CUSTOM_PAINT_THEMES:
            resolved_paint = "british_racing_green"

        # Map stages
        stage_map = {
            "stage_0_stock": "stage_0",
            "stage_1_street_thump": "stage_1",
            "stage_2_dyno_sprint": "stage_2"
        }
        resolved_stage = stage_map.get(performance_stage_key, performance_stage_key)
        if resolved_stage not in PERFORMANCE_STAGES:
            resolved_stage = "stage_1"

        resolved_style = style_key if style_key in RESTOMOD_STYLES else "bobber_solo"

        rec = self.build_restomod_quote(
            customer_name=customer_name,
            phone=phone,
            bike_model=bike_model,
            registration_no=registration_no,
            base_style=resolved_style,
            custom_paint=resolved_paint,
            stage_tune=resolved_stage
        )

        if include_vintage_ci_package:
            rec["cost_breakdown"]["vintage_ci_package"] = 12500
            rec["grand_total"] += 12500
            rec["timeline_days"] += 7
            rec["cost_breakdown"]["style_labor"] = rec["fabrication_cost"]

        return rec

    def calculate_performance_stage(self, bike_model: str, stage_key: str = "stage_1") -> Dict[str, Any]:
        """
        Universal alias for calculate_performance_stage_tune with dyno metrics adapter.
        """
        stage_map = {
            "stage_0_stock": "stage_0",
            "stage_1_street_thump": "stage_1",
            "stage_2_dyno_sprint": "stage_2"
        }
        resolved_stage = stage_map.get(stage_key, stage_key)
        if resolved_stage not in PERFORMANCE_STAGES:
            resolved_stage = "stage_1"

        res = self.calculate_performance_stage_tune(bike_model=bike_model, stage=resolved_stage)

        res["stage_cost"] = res["estimated_cost_inr"]
        res["stage_name_gu"] = "સ્ટેજ-૧ સ્ટ્રીટ બોલ્ટ-ઓન" if resolved_stage == "stage_1" else ("સ્ટેજ-૨ સ્પોર્ટ કેમ & ECU રિમેપ" if resolved_stage == "stage_2" else "સ્ટોક ફેક્ટરી સ્પેક")
        res["extra_days"] = 5 if resolved_stage == "stage_1" else 10
        res["stock_hp"] = res["baseline_hp"]
        res["tuned_hp"] = res["projected_hp"]
        res["hp_gain"] = f"{res.get('hp_gain', 3.4)} HP"
        res["stock_torque_nm"] = res["baseline_torque_nm"]
        res["tuned_torque_nm"] = res["projected_torque_nm"]
        res["torque_gain"] = f"{res.get('torque_gain_nm', 4.2)} Nm"
        res["top_speed_gain"] = "+10-15 km/h" if resolved_stage == "stage_1" else "+20-25 km/h"
        res["accel_drop"] = "-0.8s" if resolved_stage == "stage_1" else "-1.5s"
        res["exhaust_decibel"] = res["acoustic_db"]
        res["rto_legal"] = res["rto_legal_compliant"]
        res["thump_profile"] = "Deep Bass Rumble" if resolved_stage == "stage_1" else "Crisp High-Compression Throaty Thump"
        res["required_spares"] = [
            {"part_name": c, "oem_sku": f"RE-TUN-{idx:03d}", "est_price": 2500, "purpose": "Performance calibration"}
            for idx, c in enumerate(res["components"], 1)
        ]
        return res

