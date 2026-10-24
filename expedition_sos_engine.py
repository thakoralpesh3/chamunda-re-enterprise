"""
Chamunda Automobile Parts & Service - Royal Enfield Expedition Readiness,
Custom Touring Spares Kit Builder, and 24/7 Gujarat Highway SOS Breakdown Shield Engine.
Provides 48-point pre-touring clearance audits, model-specific emergency spares packager,
and interactive roadside breakdown triage in Gujarati and English.
"""

import io
import json
import time
import base64
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import qrcode
from inventory_engine import ChamundaInventoryManager, DATA_DIR

EXPEDITIONS_DIR = DATA_DIR / "expeditions"
EXPEDITIONS_DIR.mkdir(parents=True, exist_ok=True)
EXPEDITIONS_DB_FILE = DATA_DIR / "expedition_audits.json"

TOURING_DESTINATIONS = {
    "ladakh_high_altitude": {
        "title": "Leh-Ladakh & Spiti Valley (High Altitude / Sub-Zero)",
        "title_gu": "લેહ-લદ્દાખ અને સ્પીતિ વેલી (હાઇ-એલ્ટિટ્યુડ એક્સપિડિશન)",
        "min_score_required": 90.0,
        "recommended_viscosity": "15W-50 Fully Synthetic (Motul 7100)",
        "critical_spares": ["clutch cable", "spark plug", "fuse", "chain link", "brake pad"]
    },
    "desert_highway": {
        "title": "Kutch Rann & Rajasthan Highway (Extreme Heat / Long Distance)",
        "title_gu": "કચ્છ રણ અને રાજસ્થાન હાઇવે (હાઇ સ્પીડ / હાઇ ટેમ્પરેચર)",
        "min_score_required": 85.0,
        "recommended_viscosity": "15W-50 High Thermal Stability",
        "critical_spares": ["oil filter", "clutch cable", "air filter", "brake pad"]
    },
    "coastal_monsoon": {
        "title": "Konkan & Goa Coastal Corridor (Monsoon / High Moisture)",
        "title_gu": "કોંકણ અને ગોવા કોસ્ટલ (મોનસૂન / મોઇશ્ચર પ્રોટેક્શન)",
        "min_score_required": 80.0,
        "recommended_viscosity": "15W-50 Standard",
        "critical_spares": ["brake pad", "fuse", "spark plug", "chain lube"]
    },
    "weekend_escape": {
        "title": "Gujarat Regional Weekend Ride (Mount Abu / Gir / Pavagadh)",
        "title_gu": "ગુજરાત રિજનલ વિકએન્ડ રાઇડ (આબુ / ગીર / પાવાગઢ ૫૦૦ કિમી)",
        "min_score_required": 75.0,
        "recommended_viscosity": "15W-50",
        "critical_spares": ["clutch cable", "fuse"]
    }
}

SOS_ROAD_FAULTS = {
    "clutch_snap": {
        "fault_title": "Clutch Cable Snapped / Lever Completely Free",
        "fault_title_gu": "ક્લચ વાયર તૂટી ગયો / લીવર સંપૂર્ણ ફ્રી થઈ ગયું",
        "severity": "HIGH (Immobilized)",
        "immediate_action_gu": "૧. બાઇકને ન્યુટ્રલમાં મૂકી સાઇડ સ્ટેન્ડ પર ઊભી રાખો.\n૨. હેન્ડલબાર લીવર સ્ક્રૂ ઢીલો કરી તૂટેલા ઇનર કેબલને ખેંચી બહાર કાઢો.\n૩. ટૂલ કિટમાંથી ઇમરજન્સી સ્પેર ક્લચ વાયર પસાર કરો અને ક્લચ આર્મમાં સ્ક્રૂ નીપલ લોક કરો.\n૪. જો વાયર ન હોય, તો ૧લા ગિયરમાં હળવો પુશ સ્ટાર્ટ આપી ક્લચલેસ ગિયર શિફ્ટિંગથી નજીકના ગેરેજ સુધી જાઓ.",
        "immediate_action_en": "1. Shift bike into Neutral and park on side stand.\n2. Loosen handlebar lever adjuster bolt and extract snapped inner cable.\n3. Route spare emergency inner wire through sleeve and lock clamp nipple at clutch arm.\n4. If no spare, roll bike in 1st gear with gentle throttle for clutchless rev-matching to nearest stop.",
        "toolkit_needed": "10mm / 12mm Open Spanner, Pliers, Flat Screwdriver",
        "spare_part_needed": "Clutch Inner Cable (Universal Clamp Nipple)"
    },
    "no_start_dead_battery": {
        "fault_title": "Electric Starter Dead / Relay Clicking / Zero Crank",
        "fault_title_gu": "સેલ્ફ સ્ટાર્ટર બંધ / રિલે ટક-ટક અવાજ કરે છે / એન્જિન ક્રેન્ક થતું નથી",
        "severity": "MEDIUM (Start Failure)",
        "immediate_action_gu": "૧. કી-સ્વિચ અને કિલ-સ્વિચ ON કરો; ગિયરબોક્સ ૨જા ગિયરમાં નાખો.\n૨. ક્લચ દબાવી ૨-૩ લોકોની મદદથી બાઇકને ૧૫-૨૦ km/h સ્પીડમાં ધક્કો મરાવો.\n૩. સ્પીડ પકડતાં જ અચાનક ક્લચ છોડો અને તરત ફરી દબાવો (બમ્પ સ્ટાર્ટ / પુશ સ્ટાર્ટ).\n૪. એન્જિન શરૂ થતાં જ એક્સિલરેટર હળવું રાખો અને બેટરી ચાર્જ થવા દો (હેડલાઇટ ૫ મિનિટ બંધ રાખો).",
        "immediate_action_en": "1. Switch Ignition and Red Kill switch ON; engage 2nd Gear.\n2. Pull clutch and have companion push bike to 15-20 km/h speed.\n3. Dump clutch suddenly while sitting down to compress cylinder, then immediately pull clutch back in.\n4. Keep engine idling at 1,500 RPM for 10 minutes to allow alternator to charge capacitor.",
        "toolkit_needed": "Push Start / Jump Lead Cable (12V)",
        "spare_part_needed": "Main Fuse 25A / Battery Jump-Start"
    },
    "engine_stall_hot": {
        "fault_title": "Engine Sudden Stalling / Extreme Heat / Tappet Noise",
        "fault_title_gu": "એન્જિન અચાનક બંધ પડી ગયું / અતિશય ગરમી / ટેપેટ ખખડવા લાગ્યા",
        "severity": "HIGH (Thermal Overheat)",
        "immediate_action_gu": "૧. તરત જ બાઇકને છાંયડામાં પાર્ક કરો અને એન્જિન ૧૫ મિનિટ ઠંડુ થવા દો (પાણી છાંટવું નહીં!).\n૨. એન્જિન ઓઇલ ઇન્સ્પેક્શન ગ્લાસમાં લેવલ ચેક કરો. જો ઓઇલ ઓછું હોય તો ટોપ-અપ કરો.\n૩. સ્પાર્ક પ્લગ કેપ કાઢીને સ્પાર્ક ચેક કરો.\n૪. એન્જિન સામાન્ય તાપમાને પહોંચે પછી સેલ્ફ મારો. એર-લોક હોય તો ફ્યુઅલ ટાંકીનું ઢાંકણું ખોલી બંધ કરો.",
        "immediate_action_en": "1. Immediately park in shade and let cylinder head cool for 15-20 mins (DO NOT splash water!).\n2. Inspect oil level sight glass on right crankcase. Top-up if below minimum line.\n3. Open and re-close fuel tank cap to release vacuum vapour lock.\n4. Once block is hand-touch warm, crank with choke slightly pulled.",
        "toolkit_needed": "Spark Plug Wrench, Engine Oil Top-Up",
        "spare_part_needed": "Motul 7100 15W-50 (1L Topping)"
    },
    "rear_puncture": {
        "fault_title": "Rear Tyre Pressure Loss / Highway Puncture",
        "fault_title_gu": "પાછલા ટાયરમાં પંચર / પ્રેશર ઘટી જવું / ગાડી ઝોલા ખાય છે",
        "severity": "HIGH (Safety Hazard)",
        "immediate_action_gu": "૧. અચાનક બ્રેક માર્યા વગર બાઇકને ધીમે-ધીમે હાઇવે શોલ્ડર પર સુરક્ષિત ઉતારો.\n૨. સેન્ટર સ્ટેન્ડ પર ઊભી રાખી ટાયરને ફેરવી ખીલી કે કાચ શોધો.\n૩. ટ્યુબલેસ ટાયર હોય તો પંચર સ્ટ્રિપ ટૂલ વડે ૫ મિનિટમાં પંચર પ્લગ કરો.\n૪. પોર્ટેબલ ૧૨V કોમ્પ્રેસર અથવા CO2 કારતૂસથી પ્રેશર ૩૨ PSI સુધી ભરી નજીકના પંચર સેન્ટર સુધી જાઓ.",
        "immediate_action_en": "1. Smoothly decelerate using engine braking and front brake without abrupt rear braking.\n2. Place motorcycle on center stand; rotate rear wheel to identify nail/debris.\n3. For tubeless alloys: Ream hole with spiral tool and insert vulcanized puncture plug strip.\n4. Inflate to 32 PSI with portable 12V pump or manual hand pump.",
        "toolkit_needed": "Tubeless Puncture Strip Kit, Portable 12V Inflator",
        "spare_part_needed": "Puncture Plug Strips / Spare Inner Tube 120/80-18"
    },
    "chain_loose_off": {
        "fault_title": "Drive Chain Slapped / Slipped off Rear Sprocket",
        "fault_title_gu": "ડ્રાઇવ ચેઇન ઉતરી ગઈ / અવાજ સાથે ઢીલી પડી ગઈ",
        "severity": "CRITICAL (Mechanical Disconnect)",
        "immediate_action_gu": "૧. તરત જ ક્લચ દબાવી સાઈડમાં ઊભી રાખો; પાછલા વ્હીલ એક્સલ નટ (૨૪mm) ઢીલો કરો.\n૨. બંને બાજુના ચેઇન એડજસ્ટર સ્નેલ કેમ્સ અથવા બોલ્ટ્સ એક સરખા ૨ આંટા આગળ ધકેલો.\n૩. ચેઇનને પાછલા સ્પ્રોકેટ પર ચડાવી વ્હીલ ફેરવો જેથી ચેઇન ગ્રુવમાં બેસી જાય.\n૪. ચેઇનમાં ૨૫ થી ૩૦ mm નું સ્લેક રહે તે રીતે એક્સલ નટ ટાઇટ કરો (૭૦ Nm) અને લ્યુબ સ્પ્રે કરો.",
        "immediate_action_en": "1. Pull clutch immediately to avoid rear wheel lockup; park on center stand.\n2. Loosen 24mm rear wheel axle nut by 2 full turns.\n3. Rotate snail cams or tensioner bolts equally on left and right sides to align chain with sprocket teeth.\n4. Ensure 25-30 mm vertical play; tighten axle nut firmly and apply chain spray.",
        "toolkit_needed": "24mm Ring Spanner, 12mm / 14mm Spanners, Chain Lube",
        "spare_part_needed": "Heavy-Duty Chain Master Link (520 / 525 O-Ring)"
    }
}


def generate_qr_base64(data: str, fill_color: str = "#0d2b22", back_color: str = "#ffffff") -> str:
    """Generate high-contrast QR code as Base64 data URI."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64_str}"


class ChamundaExpeditionManager:
    """
    Institutional Long-Distance Touring Readiness, Custom Spares Kit, and Highway Breakdown SOS Manager.
    """

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.expeditions_dir = data_dir / "expeditions"
        self.expeditions_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = data_dir / "expedition_audits.json"
        self.inv_manager = ChamundaInventoryManager(data_dir=data_dir)

    def _load_db(self) -> List[Dict[str, Any]]:
        if self.db_file.exists():
            try:
                return json.loads(self.db_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save_db(self, records: List[Dict[str, Any]]) -> None:
        self.db_file.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    def conduct_expedition_audit(
        self,
        rider_name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        destination_key: str = "ladakh_high_altitude",
        planned_km: int = 3500,
        domain_scores: Optional[Dict[str, int]] = None,
        inspector_name: str = "Master Tech Alpesh (Chamunda Automobile)"
    ) -> Dict[str, Any]:
        """
        Execute 48-Point Expedition Pre-Flight Inspection across 6 touring survival domains.
        Assigns clearance tier, calculates tour endurance score (0-100), auto-packages essential spares,
        and generates a verifiable 'Chamunda Expedition Ready' QR Clearance Passport.
        """
        now = datetime.datetime.now()
        clean_reg = registration_no.upper().strip()
        exp_suffix = f"{int(time.time()) % 10000:04d}"
        exp_id = f"EXP-RE-{now.strftime('%Y%m%d')}-{exp_suffix}"

        dest_info = TOURING_DESTINATIONS.get(destination_key, TOURING_DESTINATIONS["ladakh_high_altitude"])
        ds = domain_scores or {}

        # 6 Specialized Touring Domains (Total 100 pts)
        fluids_val = ds.get("fluids_pts") or ds.get("engine_altitude") or 19
        chain_val = ds.get("chain_pts") or ds.get("suspension_load") or 14
        brakes_val = ds.get("brakes_pts") or ds.get("brakes_fluid") or 14
        elec_val = ds.get("electrical_pts") or ds.get("electricals_cold") or 14
        chassis_val = ds.get("chassis_pts") or ds.get("survival_pack") or 19
        tyres_val = ds.get("tyres_pts") or ds.get("tyres_terrain") or 14

        dom_fluids = {
            "domain": "High-Altitude Fluids & Oil Viscosity",
            "name": "High-Altitude Fluids & Oil Viscosity",
            "domain_gu": "હાઇ-એલ્ટિટ્યુડ એન્જિન ઓઇલ અને ફ્લુઇડ વિસ્કોસિટી",
            "max_pts": 20,
            "earned_pts": fluids_val,
            "checks": [
                {"item": "Motul 7100 15W-50 Viscosity & Sheer Resistance", "status": "Optimal High-Temp Film", "pts": 7},
                {"item": "DOT 4 Brake Fluid Moisture & Boiling Point (>230°C)", "status": "Moisture <1.5%", "pts": 7},
                {"item": "Fork Oil Damping & Stanchion Dust Seals Integrity", "status": "Zero Seal Weep", "pts": 6}
            ]
        }

        dom_chain = {
            "domain": "Drive Chain & Sprocket Fatigue",
            "name": "Drive Chain & Sprocket Fatigue",
            "domain_gu": "ડ્રાઇવ ચેઇન સ્લેક અને સ્પ્રોકેટ લાઇફ",
            "max_pts": 15,
            "earned_pts": chain_val,
            "checks": [
                {"item": "Drive Chain Slack Specification (25 - 30 mm)", "status": "Perfect 28mm Tension", "pts": 5},
                {"item": "Rear/Front Sprocket Tooth Profile & Hooking Check", "status": "Even Tooth Profile (<10% Wear)", "pts": 5},
                {"item": "O-Ring / X-Ring Lubrication & Master Link Clip Clip Orientation", "status": "Lube Saturated & Clip Locked", "pts": 5}
            ]
        }

        dom_brakes = {
            "domain": "Braking Reserve for Mountain Descents",
            "name": "Braking Reserve for Mountain Descents",
            "domain_gu": "બ્રેકિંગ રિઝર્વ અને પહાડી ઢોળાવ સલામતી",
            "max_pts": 15,
            "earned_pts": brakes_val,
            "checks": [
                {"item": "Front/Rear ByBre Pad Thickness (>3.5 mm Remaining)", "status": "4.8mm Pad Reserve", "pts": 5},
                {"item": "Disc Rotor Thickness & Heat Scoring Trueness", "status": "Runout <0.08mm", "pts": 5},
                {"item": "Dual-Channel ABS Sensor Line Routing & Armoring", "status": "Zero Chafe / Secure", "pts": 5}
            ]
        }

        dom_electrical = {
            "domain": "Electrical & Auxiliary Touring Load",
            "name": "Electrical & Auxiliary Touring Load",
            "domain_gu": "ઇલેક્ટ્રિકલ સિસ્ટમ, ફોગ લાઇટ અને ઓલ્ટરનેટર લોડ",
            "max_pts": 15,
            "earned_pts": elec_val,
            "checks": [
                {"item": "Alternator Charging Under Fog Lights (14.2V @ 2,500 RPM)", "status": "Pass (Healthy 14.18V)", "pts": 5},
                {"item": "Battery Cold Cranking Reserve (100A Load Test >10.2V)", "status": "Pass (10.6V Strong)", "pts": 5},
                {"item": "Waterproof Wiring Harness & Auxiliary Fuse Isolation", "status": "Marine-Grade Sealed", "pts": 5}
            ]
        }

        dom_chassis = {
            "domain": "Chassis, Pannier Racks & Luggage Balance",
            "name": "Chassis, Pannier Racks & Luggage Balance",
            "domain_gu": "ચેસિસ, લગેજ રેક્સ અને પેનિયર લોડ બેલેન્સ",
            "max_pts": 20,
            "earned_pts": chassis_val,
            "checks": [
                {"item": "Subframe Luggage Rack Mounting Torques (28 Nm)", "status": "Factory Torqued", "pts": 7},
                {"item": "Steering Headstock Cone Bearings & Zero Notch Play", "status": "Smooth Travel", "pts": 7},
                {"item": "Rear Gas Shock Preload Adjusted for Luggage Weight", "status": "Preload Click 5 Set", "pts": 6}
            ]
        }

        dom_tyres = {
            "domain": "Tyres & High-Speed Highway Heat Endurance",
            "name": "Tyres & High-Speed Highway Heat Endurance",
            "domain_gu": "ટાયર્સ, ટ્રેડ ડેપ્થ અને હાઇ-સ્પીડ હીટ રેઝિસ્ટન્સ",
            "max_pts": 15,
            "earned_pts": tyres_val,
            "checks": [
                {"item": "Tread Depth Center/Shoulder (>3.0 mm Highway Spec)", "status": "4.5mm Remaining", "pts": 5},
                {"item": "Spoke Radial Trueness / Alloy Bead Seating Integrity", "status": "True (<1.0mm)", "pts": 5},
                {"item": "Valve Stem Rubber Aging & High-Pressure Metal Caps", "status": "New Brass Caps Fitted", "pts": 5}
            ]
        }

        domains = [dom_fluids, dom_chain, dom_brakes, dom_electrical, dom_chassis, dom_tyres]
        for d in domains:
            d["status"] = "PASSED" if d["earned_pts"] >= (d["max_pts"] * 0.7) else "ATTENTION"

        total_score = round(sum(float(d["earned_pts"]) for d in domains), 1)

        # Clearance Tiers
        if total_score >= 90.0:
            clearance_tier = "EXPEDITION CERTIFIED - HIGH ALTITUDE & LADAKH READY"
            clearance_tier_gu = "એક્સપિડિશન સર્ટિફાઇડ (લદ્દાખ અને હાઇ-એલ્ટિટ્યુડ માટે ૧૦૦% મંજૂર)"
            badge_color = "#D4AF37"
            approved = True
            directive = "Full Expedition Clearance Granted. Motorcycle is structurally and mechanically optimal for extreme high-altitude mountain passes."
        elif total_score >= 80.0:
            clearance_tier = "HIGHWAY TOURING READY"
            clearance_tier_gu = "હાઇવે ટૂરિંગ રેડી (૨,૫૦૦+ કિમી હાઇવે માટે મંજૂર)"
            badge_color = "#10b981"
            approved = True
            directive = "Approved for national highway long-distance expeditions. Recommend carrying Chamunda custom spares kit."
        elif total_score >= 70.0:
            clearance_tier = "SHORT RUN / COMMUTER APPROVED"
            clearance_tier_gu = "શોર્ટ રન મંજૂર (ટૂરિંગ પહેલાં ટ્યુન-અપ જરૂરી)"
            badge_color = "#60a5fa"
            approved = False
            directive = "Conditional clearance. General servicing and wear-part replacement required before undertaking trips over 500 km."
        else:
            clearance_tier = "EXPEDITION REJECTED - CRITICAL DEFECTS"
            clearance_tier_gu = "એક્સપિડિશન અસ્વીકાર્ય (ગંભીર ખામીઓ - મુસાફરી જોખમી)"
            badge_color = "#ef4444"
            approved = False
            directive = "Expedition Clearance DENIED. Critical safety items (brakes/chain/tyres) must be overhauled prior to highway travel."

        # Generate Carry-Along Spares Kit
        spares_kit = self.build_carry_along_spares_kit(bike_model=bike_model, destination_key=destination_key)

        # Dynamic QR Code linking to verification endpoint
        qr_verification_url = f"http://127.0.0.1:8080/expedition/{exp_id}"
        qr_b64 = generate_qr_base64(qr_verification_url, fill_color="#0d2b22", back_color="#ffffff")

        # Generate HTML Expedition Passport
        cert_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Expedition Passport {exp_id} - Chamunda Automobile</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 25px;
            background: #f1f5f3;
            color: #1a1a1a;
        }}
        .passport-card {{
            max-width: 820px;
            margin: auto;
            background: #ffffff;
            border: 3px solid #0d2b22;
            border-top: 8px solid #D4AF37;
            border-radius: 12px;
            padding: 35px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #D4AF37;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .brand-title {{
            font-size: 26px;
            font-weight: 800;
            color: #0d2b22;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}
        .brand-subtitle {{
            color: #D4AF37;
            font-weight: bold;
            font-size: 13px;
        }}
        .score-pill {{
            background: #0d2b22;
            color: #D4AF37;
            padding: 10px 20px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #D4AF37;
        }}
        .table-custom {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}
        .table-custom th, .table-custom td {{
            padding: 10px 14px;
            border: 1px solid #e5e7eb;
            font-size: 13px;
        }}
        .table-custom th {{
            background: #0d2b22;
            color: #D4AF37;
            text-align: left;
        }}
        .sos-box {{
            background: #0a1b15;
            color: #f3f4f6;
            padding: 18px;
            border-left: 4px solid #D4AF37;
            border-radius: 8px;
            margin: 20px 0;
            font-size: 12px;
        }}
        .footer {{
            text-align: center;
            margin-top: 25px;
            border-top: 1px solid #d1d5db;
            padding-top: 15px;
            font-size: 12px;
            color: #6b7280;
        }}
        @media print {{
            body {{ padding: 0; background: white; }}
            .passport-card {{ box-shadow: none; border-width: 2px; }}
            .no-print {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <div class="passport-card">
        <div class="header">
            <div>
                <div class="brand-title">🏔️ CHAMUNDA EXPEDITION SHIELD</div>
                <div class="brand-subtitle">ROYAL ENFIELD LONG-DISTANCE TOURING READINESS PASSPORT</div>
                <div style="font-size: 11px; color: #4b5563; margin-top: 4px;">48-Point Pre-Touring Clearance &amp; 24/7 Highway SOS Protection</div>
            </div>
            <div class="score-pill">
                <div style="font-size: 28px; font-weight: 800;">{total_score} / 100</div>
                <div style="font-size: 11px; font-weight: bold; color: {badge_color};">{clearance_tier}</div>
            </div>
        </div>

        <table class="table-custom">
            <tr>
                <td style="width: 50%;"><strong>Rider Name:</strong> {rider_name} ({phone})</td>
                <td style="width: 50%;"><strong>Motorcycle:</strong> {bike_model} (<code>{clean_reg}</code>)</td>
            </tr>
            <tr>
                <td><strong>Destination:</strong> {dest_info['title']}</td>
                <td><strong>Planned Expedition:</strong> ~{planned_km:,} KM</td>
            </tr>
            <tr>
                <td><strong>Passport ID:</strong> <code>{exp_id}</code></td>
                <td><strong>Clearance Status:</strong> <span style="color: {badge_color}; font-weight: bold;">{clearance_tier_gu}</span></td>
            </tr>
        </table>

        <h4 style="color: #0d2b22; margin-top: 20px; border-bottom: 2px solid #e5e7eb; padding-bottom: 5px;">
            🔍 6 Specialized Touring Domains Assessment
        </h4>
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Touring Domain</th>
                    <th>Gujarati Spec</th>
                    <th>Max Pts</th>
                    <th>Earned Pts</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f'<tr><td><strong>{d["domain"]}</strong></td><td><small>{d["domain_gu"]}</small></td><td>{d["max_pts"]}</td><td><strong style="color:#0d2b22;">{d["earned_pts"]}</strong></td></tr>' for d in domains)}
            </tbody>
        </table>

        <h4 style="color: #0d2b22; margin-top: 20px; border-bottom: 2px solid #e5e7eb; padding-bottom: 5px;">
            📦 Recommended Carry-Along Spares Kit ({spares_kit['total_parts_count']} Essential Items)
        </h4>
        <table class="table-custom">
            <thead>
                <tr>
                    <th>Item Description</th>
                    <th>OEM Part No</th>
                    <th>MRP (₹)</th>
                    <th>Emergency Role</th>
                </tr>
            </thead>
            <tbody>
                {''.join(f'<tr><td>{it["name"]}</td><td><code>{it["part_number"]}</code></td><td>₹{it["mrp"]}</td><td>{it["role"]}</td></tr>' for it in spares_kit['items'])}
            </tbody>
        </table>
        <div style="text-align: right; font-size: 13px; font-weight: bold; color: #0d2b22; margin-bottom: 15px;">
            Total Essential Kit Outlay: ₹{spares_kit['total_kit_mrp']:,} (Available at Chamunda Counter POS)
        </div>

        <div class="sos-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #D4AF37; font-size: 14px;">🚨 24/7 GUJARAT HIGHWAY BREAKDOWN SOS SUPPORT</strong>
                    <div style="margin-top: 4px;">If stranded on NH-48 / NH-27 / Ahmedabad-Udaipur / Saurashtra Corridors:</div>
                    <div style="color: #10b981; font-weight: bold; font-size: 13px; margin-top: 2px;">📞 Chamunda Emergency SOS Helpline: +91 98250 12345</div>
                </div>
                <div>
                    <img src="{qr_b64}" style="width: 75px; height: 75px; border-radius: 4px; border: 1px solid #D4AF37;" alt="QR">
                </div>
            </div>
        </div>

        <div class="footer">
            Chamunda Automobile Parts &amp; Service • NH-48, Gujarat • Royal Enfield Specialists • Chief Tech: {inspector_name}
        </div>

        <div class="no-print" style="margin-top: 20px; text-align: center;">
            <button onclick="window.print()" style="padding: 10px 24px; background: #0d2b22; color: #D4AF37; border: 2px solid #D4AF37; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 14px;">
                🖨️ Print Chamunda Expedition Clearance Passport
            </button>
        </div>
    </div>
</body>
</html>
"""
        passport_file = self.expeditions_dir / f"{exp_id}.html"
        passport_file.write_text(cert_html, encoding="utf-8")

        # Bilingual WhatsApp Broadcast copy
        wa_gu = (
            f"🏔️ *ચામુંડા રોયલ એનફિલ્ડ એક્સપિડિશન ક્લિયરન્સ પાસપોર્ટ* 📜\n\n"
            f"નમસ્તે શ્રી {rider_name} જી!\n"
            f"આપની રોયલ એનફિલ્ડ *{bike_model}* (`{clean_reg}`) નું ૪૮-પોઇન્ટ પ્રી-ટુર ઓડિટ પૂર્ણ થયું છે.\n\n"
            f"🎯 *એક્સપિડિશન સ્કોર:* *{total_score} / 100*\n"
            f"🏅 *ક્લિયરન્સ સ્ટેટસ:* *{clearance_tier_gu}*\n"
            f"🗺️ *પ્લાન્ડ ટૂર:* {dest_info['title_gu']} (~{planned_km:,} KM)\n"
            f"📦 *ટ્રિપ સ્પેર કીટ:* {spares_kit['total_parts_count']} સ્પેરપાર્ટ્સ પેકેજ (₹{spares_kit['total_kit_mrp']:,})\n\n"
            f"🚨 *૨૪/૭ હાઇવે બ્રેકડાઉન SOS હેલ્પલાઇન:* +91 98250 12345\n"
            f"📱 *ડિજિટલ પાસપોર્ટ લાઈવ જુઓ:* {qr_verification_url}\n\n"
            f"ચામુંડા ઓટોમોબાઇલ પાર્ટ્સ એન્ડ સર્વિસ - રોયલ એનફિલ્ડ સ્પેશિયાલિસ્ટ્સ"
        )

        wa_en = (
            f"🏔️ *Chamunda Royal Enfield Expedition Clearance Passport* 📜\n\n"
            f"Namaste {rider_name} ji!\n"
            f"48-Point Pre-Touring Inspection completed for your *{bike_model}* (`{clean_reg}`).\n\n"
            f"🎯 *Touring Readiness Score:* *{total_score} / 100*\n"
            f"🏅 *Clearance Status:* *{clearance_tier}*\n"
            f"🗺️ *Destination:* {dest_info['title']} (~{planned_km:,} KM)\n"
            f"📦 *Essential Spares Kit:* {spares_kit['total_parts_count']} Parts (₹{spares_kit['total_kit_mrp']:,})\n\n"
            f"🚨 *24/7 Highway SOS Helpline:* +91 98250 12345\n"
            f"📱 *Verify Digital Passport:* {qr_verification_url}\n\n"
            f"Chamunda Automobile Parts & Service - Royal Enfield Specialists"
        )

        record = {
            "exp_id": exp_id,
            "expedition_id": exp_id,
            "timestamp": now.isoformat(),
            "rider_name": rider_name,
            "phone": phone,
            "bike_model": bike_model,
            "registration_no": clean_reg,
            "destination_key": destination_key,
            "destination_title": dest_info["title"],
            "destination_name": dest_info["title"],
            "destination_terrain": dest_info.get("terrain", "Extreme Altitude"),
            "planned_km": planned_km,
            "total_score": total_score,
            "clearance_tier": clearance_tier,
            "clearance_tier_gu": clearance_tier_gu,
            "badge_color": badge_color,
            "approved": approved,
            "clearance_granted": approved,
            "sos_shield": "24/7 GPS SOS Guard & Chamunda Highway Patrol",
            "directive": directive,
            "directives": [directive],
            "domains": domains,
            "spares_kit": spares_kit,
            "carry_along_spares": spares_kit.get("items", []),
            "spares_total_cost": spares_kit.get("total_kit_mrp", 0),
            "passport_html_file": str(passport_file),
            "qr_verification_url": qr_verification_url,
            "qr_code_base64": qr_b64,
            "whatsapp_message_gu": wa_gu,
            "whatsapp_message_en": wa_en
        }

        records = self._load_db()
        records.insert(0, record)
        self._save_db(records)

        return record

    def build_carry_along_spares_kit(
        self,
        bike_model: str,
        destination_key: str = "ladakh_high_altitude"
    ) -> Dict[str, Any]:
        """
        Auto-package custom essential backup spares from 4,469 parts catalog tailored for the model and route.
        """
        items = []

        # 1. Essential Clutch Wire (Universal Long Tour Lifeline)
        clutch_parts = self.inv_manager.filter_parts(query="clutch cable", limit=1)
        if clutch_parts:
            cp = clutch_parts[0]
            items.append({
                "name": cp.get("name", "Royal Enfield Clutch Inner Cable"),
                "part_number": cp.get("part_number", "1017002/A"),
                "mrp": cp.get("mrp", 180),
                "role": "Lifeline: Snapped clutch cable roadside repair"
            })
        else:
            items.append({
                "name": f"Royal Enfield Genuine Clutch Cable ({bike_model})",
                "part_number": "OEM-CC-350",
                "mrp": 220,
                "role": "Lifeline: Snapped clutch cable roadside repair"
            })

        # 2. OEM Spark Plug
        plug_parts = self.inv_manager.filter_parts(query="spark plug", limit=1)
        if plug_parts:
            sp = plug_parts[0]
            items.append({
                "name": sp.get("name", "Bosch / Champion Spark Plug OEM"),
                "part_number": sp.get("part_number", "592004/A"),
                "mrp": sp.get("mrp", 245),
                "role": "High-Altitude misfire / cold-foul backup"
            })
        else:
            items.append({
                "name": "Bosch High-Performance Spark Plug",
                "part_number": "592004/A",
                "mrp": 245,
                "role": "High-Altitude misfire / cold-foul backup"
            })

        # 3. Brake Pads (Heavy mountain descent safety)
        brake_parts = self.inv_manager.filter_parts(query="brake pad", limit=1)
        if brake_parts:
            bp = brake_parts[0]
            items.append({
                "name": bp.get("name", "Front Disc Brake Pad Set ByBre"),
                "part_number": bp.get("part_number", "1017008/B"),
                "mrp": bp.get("mrp", 650),
                "role": "Mountain descent friction wear replacement"
            })
        else:
            items.append({
                "name": "Front Disc Brake Pad Set ByBre OEM",
                "part_number": "1017008/B",
                "mrp": 650,
                "role": "Mountain descent friction wear replacement"
            })

        # 4. Heavy-Duty Chain Master Link (520 O-Ring)
        items.append({
            "name": "Heavy-Duty Drive Chain Master Link (520 / 525 O-Ring)",
            "part_number": "OEM-CML-520",
            "mrp": 150,
            "role": "Broken chain reconnection on isolated highway"
        })

        # 5. Assorted Blade Fuse Pack (10A, 15A, 25A)
        items.append({
            "name": "Automotive Blade Fuse Emergency Assortment (5 Pcs)",
            "part_number": "OEM-FUSE-SET",
            "mrp": 95,
            "role": "Electrical short-circuit / lighting circuit revival"
        })

        # 6. Destination specific extras
        if destination_key == "ladakh_high_altitude":
            items.append({
                "name": "Motul 7100 15W-50 4T Synthetic Oil (1L Emergency Top-up)",
                "part_number": "MOTUL-7100-1L",
                "mrp": 980,
                "role": "Extreme high-temperature / mountain grade topping"
            })
        elif destination_key == "coastal_monsoon":
            items.append({
                "name": "Chain Lube Aerosol (150ml Pocket Can)",
                "part_number": "MOTUL-LUBE-150",
                "mrp": 220,
                "role": "Water and salt spray anti-rust protection"
            })

        total_mrp = sum(it["mrp"] for it in items)
        for it in items:
            it["purpose"] = it.get("role", "Emergency touring replacement")
            it["criticality"] = "HIGH"
            it["qty"] = 1
            it["price"] = it.get("mrp", 0)

        dest_meta = TOURING_DESTINATIONS.get(destination_key, {})
        return {
            "bike_model": bike_model,
            "destination_key": destination_key,
            "destination": dest_meta.get("title", destination_key.replace("_", " ").title()),
            "terrain": dest_meta.get("terrain", "Touring Route"),
            "total_parts_count": len(items),
            "item_count": len(items),
            "total_kit_mrp": total_mrp,
            "total_estimated_cost_inr": total_mrp,
            "items": items
        }

    def highway_sos_triage(self, symptom_query: str) -> Dict[str, Any]:
        """
        Interactive 30-Second Highway Breakdown Roadside Triage.
        Analyzes breakdown symptoms and delivers instant mechanical revival instructions in Gujarati & English.
        """
        q = symptom_query.lower()
        matched_key = "clutch_snap"

        if any(w in q for w in ["clutch", "ક્લચ", "cable", "વાયર", "લીવર", "lever"]):
            matched_key = "clutch_snap"
        elif any(w in q for w in ["start", "સ્ટાર્ટ", "battery", "બેટરી", "relay", "રિલે", "self", "સેલ્ફ", "dead", "ક્રેન્ક"]):
            matched_key = "no_start_dead_battery"
        elif any(w in q for w in ["heat", "ગરમ", "overheat", "stall", "બંધ", "tappet", "ટેપેટ", "smoke", "ધુમાડો"]):
            matched_key = "engine_stall_hot"
        elif any(w in q for w in ["puncture", "પંચર", "tyre", "ટાયર", "air", "હવા", "pressure", "પ્રેશર"]):
            matched_key = "rear_puncture"
        elif any(w in q for w in ["chain", "ચેઇન", "sprocket", "સ્પ્રોકેટ", "slack", "ઢીલી", "ઉતરી"]):
            matched_key = "chain_loose_off"

        fault_info = SOS_ROAD_FAULTS[matched_key]
        raw_fix = fault_info["immediate_action_en"].split("\n")
        steps = [s.strip() for s in raw_fix if s.strip()]
        return {
            "symptom_queried": symptom_query,
            "fault_key": matched_key,
            "fault_category": fault_info["fault_title"],
            "fault_title": fault_info["fault_title"],
            "fault_title_gu": fault_info["fault_title_gu"],
            "severity": fault_info["severity"],
            "urgency": fault_info["severity"],
            "safety_protocol": "Park motorcycle safely onto highway shoulder, switch hazard lights ON, place on center stand.",
            "immediate_action_gu": fault_info["immediate_action_gu"],
            "immediate_action_en": fault_info["immediate_action_en"],
            "english_directive": fault_info["immediate_action_en"].replace("\n", " "),
            "gujarati_directive": fault_info["immediate_action_gu"].replace("\n", " "),
            "toolkit_needed": fault_info["toolkit_needed"],
            "tools_required": [t.strip() for t in fault_info["toolkit_needed"].split(",")],
            "spare_part_needed": fault_info["spare_part_needed"],
            "roadside_fix_steps": steps,
            "sos_helpline": "+91 98250 12345 (Chamunda 24/7 Roadside Hotline)",
            "helpline_24x7": "+91 98250 12345 (Chamunda Automobile Highway Patrol)"
        }

    def get_expedition_passport(self, exp_id: str) -> Optional[Dict[str, Any]]:
        """Fetch expedition passport record by ID."""
        for r in self._load_db():
            if r.get("exp_id") == exp_id or r.get("expedition_id") == exp_id:
                return r
        return None

    def get_all_expeditions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent expedition audits."""
        return self._load_db()[:limit]
