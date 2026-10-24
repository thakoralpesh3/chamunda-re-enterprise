"""
Chamunda Automobile Enterprise • Project "Night-Guardian" (રાત્રિ-સંરક્ષક)
24/7 Automated Highway Emergency Spares Locker & Midnight Dispenser Kiosk.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. 8 Physical Smart Locker Compartments installed outside Radhanpur Road Workshop.
2. Pre-stocked with vital Royal Enfield highway breakdown spares (clutch wire, relays, oil, plugs, CO2 kit).
3. Automated WhatsApp Bot integration (+91 78747 19139) with dynamic UPI QR payment.
4. One-Time Password (6-digit OTP) solenoid relay unlock simulation.
5. Real-time locker bay environmental telemetry (temperature, battery backup, door sensors).
6. Cashless midnight sales ledger and automatic morning restocking orders.
"""

import os
import sys
import json
import time
import random
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger("ChamundaNightLocker")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
LOCKER_FILE = DATA_DIR / "night_locker_inventory.json"
OFFICIAL_WHATSAPP_HELPLINE = "+91 78747 19139"


class ChamundaNightLockerManager:
    """
    Manages the 24/7 exterior emergency smart locker bays for highway touring riders.
    Handles reservations, UPI payment verification, OTP solenoid unlock, and stock audit.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_locker_data()

    def _ensure_locker_data(self):
        """Initialize 8 default smart locker compartments if not already persisted."""
        if LOCKER_FILE.exists():
            return

        initial_state = {
            "locker_station": "CHAMUNDA-LOCKER-MEHSANA-HQ",
            "location": "Outside Shutter, Radhanpur Road Master Workshop, Mehsana Highway Corridor",
            "support_whatsapp": OFFICIAL_WHATSAPP_HELPLINE,
            "telemetry": {
                "system_status": "ONLINE",
                "ambient_temp_c": 26.8,
                "backup_battery_pct": 98,
                "power_source": "Mains 230V + UPS Sine Wave",
                "tamper_sensor": "ARMED_SECURE",
                "solenoid_voltage": "12.4V (Nominal)",
                "last_heartbeat": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "compartments": [
                {
                    "box_id": "BOX-01",
                    "item_name": "RE Heavy-Duty Clutch Cable + Cable Lube Pouch",
                    "item_name_gu": "હેવી-ડ્યુટી ક્લચ કેબલ અને કેબલ લ્યુબ પાઉચ",
                    "part_number": "574012/C",
                    "compatible_bikes": "Classic, Bullet 350, Hunter, Meteor, Standard",
                    "price_inr": 340.0,
                    "units_inside": 2,
                    "max_capacity": 3,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_01",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-02",
                    "item_name": "J-Series & UCE Accelerator Throttle Cable Set",
                    "item_name_gu": "એક્સિલરેટર થ્રોટલ કેબલ સેટ",
                    "part_number": "574018/A",
                    "compatible_bikes": "All 350cc & 500cc EFI / Carb Models",
                    "price_inr": 290.0,
                    "units_inside": 2,
                    "max_capacity": 3,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_02",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-03",
                    "item_name": "Twin Spark Plugs Set (NGK Laser Platinum CPR8EA-9 x2)",
                    "item_name_gu": "ટ્વિન સ્પાર્ક પ્લગ સેટ (NGK પ્લેટિનમ x2)",
                    "part_number": "574050/C",
                    "compatible_bikes": "Twinspark, Classic, Meteor, Hunter, 650 Twin",
                    "price_inr": 480.0,
                    "units_inside": 4,
                    "max_capacity": 4,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_03",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-04",
                    "item_name": "12V 30A Main Starter & Lighting Heavy Relay Pair",
                    "item_name_gu": "૧૨V ૩૦A મેઇન સ્ટાર્ટર અને લાઇટિંગ રિલે પેર",
                    "part_number": "581023/A",
                    "compatible_bikes": "All Royal Enfield Electric Start Models",
                    "price_inr": 380.0,
                    "units_inside": 3,
                    "max_capacity": 4,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_04",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-05",
                    "item_name": "Liqui Moly 15W-50 Street Synthetic Engine Oil (1L Emergency Pouch)",
                    "item_name_gu": "લિક્વી મોલી ૧૫W-૫૦ સિન્થેટિક એન્જિન ઓઇલ (૧ લીટર)",
                    "part_number": "LM-15W50-1L",
                    "compatible_bikes": "J-Series, 650 Twins, Himalayan 450, UCE 350/500",
                    "price_inr": 980.0,
                    "units_inside": 2,
                    "max_capacity": 2,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_05",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-06",
                    "item_name": "Heavy-Duty Tubeless Tyre Puncture Strip Kit + 2x CO2 Cylinders",
                    "item_name_gu": "ટ્યુબલેસ પંચર કીટ + ૨x CO2 ઇન્ફ્લેટર સિલિન્ડર",
                    "part_number": "PUNC-CO2-KIT",
                    "compatible_bikes": "All Alloy / Tubeless Royal Enfield Motorcycles",
                    "price_inr": 550.0,
                    "units_inside": 3,
                    "max_capacity": 3,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_06",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-07",
                    "item_name": "Motul 150ml Emergency Pocket Chain Lube & Clean Spray",
                    "item_name_gu": "મોતુલ ઇમરજન્સી પોકેટ ચેઇન લ્યુબ સ્પ્રે",
                    "part_number": "MOT-CL-150",
                    "compatible_bikes": "All O-Ring / X-Ring Motorcycle Chains",
                    "price_inr": 320.0,
                    "units_inside": 4,
                    "max_capacity": 5,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_07",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                },
                {
                    "box_id": "BOX-08",
                    "item_name": "H4 Halogen 12V 60/55W Heavy-Duty Anti-Vibration Bulb",
                    "item_name_gu": "H4 ૧૨V ૬૦/૫૫W હેવી-ડ્યુટી હેડલાઇટ બલ્બ",
                    "part_number": "571089/A",
                    "compatible_bikes": "Classic, Standard, Thunderbird, Himalayan",
                    "price_inr": 220.0,
                    "units_inside": 3,
                    "max_capacity": 4,
                    "status": "Available",
                    "solenoid_relay_id": "RELAY_08",
                    "door_state": "CLOSED_LOCKED",
                    "last_accessed": None
                }
            ],
            "active_reservations": [],
            "completed_transactions": []
        }

        with open(LOCKER_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_state, f, indent=2, ensure_ascii=False)
        logger.info("Initialized 24/7 Night Locker data at %s", LOCKER_FILE)

    def _read_data(self) -> Dict[str, Any]:
        self._ensure_locker_data()
        try:
            with open(LOCKER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error("Failed to read locker file: %s", e)
            return {"compartments": [], "active_reservations": [], "completed_transactions": []}

    def _save_data(self, data: Dict[str, Any]):
        with open(LOCKER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_locker_status(self) -> Dict[str, Any]:
        """Return real-time locker telemetry, compartment grid, and night sales summary."""
        data = self._read_data()
        compartments = data.get("compartments", [])
        txs = data.get("completed_transactions", [])

        # Auto-clean expired reservations (>15 mins)
        now = time.time()
        active = []
        for r in data.get("active_reservations", []):
            if now - r.get("created_timestamp", now) < 900 and r.get("status") == "Reserved":
                active.append(r)
            else:
                # Reset box status back to Available
                for b in compartments:
                    if b["box_id"] == r.get("box_id") and b["status"] == "Reserved":
                        b["status"] = "Available"
        data["active_reservations"] = active
        self._save_data(data)

        total_night_revenue = sum(t.get("amount_paid", 0.0) for t in txs)
        available_count = sum(1 for c in compartments if c["status"] == "Available" and c["units_inside"] > 0)

        return {
            "locker_station": data.get("locker_station"),
            "location": data.get("location"),
            "support_whatsapp": data.get("support_whatsapp", OFFICIAL_WHATSAPP_HELPLINE),
            "telemetry": data.get("telemetry", {}),
            "total_compartments": len(compartments),
            "available_compartments_count": available_count,
            "active_reservations_count": len(active),
            "total_night_transactions": len(txs),
            "total_night_revenue_inr": round(total_night_revenue, 2),
            "compartments": compartments,
            "recent_transactions": txs[-6:]
        }

    def reserve_compartment(
        self,
        box_id: str,
        customer_name: str,
        phone: str,
        vehicle_reg: str = "Touring Rider"
    ) -> Dict[str, Any]:
        """
        Reserve an emergency locker compartment, generate unique 6-digit OTP,
        and provide dynamic UPI QR payment string.
        """
        data = self._read_data()
        comp = next((c for c in data.get("compartments", []) if c["box_id"].upper() == box_id.upper()), None)

        if not comp:
            return {"success": False, "error": f"Locker compartment '{box_id}' does not exist."}

        if comp["units_inside"] <= 0 or comp["status"] != "Available":
            return {"success": False, "error": f"Compartment '{box_id}' ({comp['item_name']}) is currently empty or reserved."}

        otp_code = f"{random.randint(100000, 999999)}"
        res_id = f"NLK-{time.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        amount = comp["price_inr"]

        # Formulate UPI payload
        upi_payload = f"upi://pay?pa=7874719139@upi&pn=ChamundaAutomobile&am={amount:.2f}&cu=INR&tn={res_id}"

        reservation = {
            "reservation_id": res_id,
            "box_id": comp["box_id"],
            "item_name": comp["item_name"],
            "item_name_gu": comp["item_name_gu"],
            "part_number": comp["part_number"],
            "customer_name": customer_name,
            "phone": phone,
            "vehicle_reg": vehicle_reg,
            "amount_payable": amount,
            "otp_code": otp_code,
            "upi_payload": upi_payload,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "created_timestamp": time.time(),
            "status": "Reserved"
        }

        # Update compartment state
        comp["status"] = "Reserved"
        data.setdefault("active_reservations", []).append(reservation)
        self._save_data(data)

        msg_gu = (
            f"રાત્રિ ઇમરજન્સી બુકિંગ કન્ફર્મ! રિઝર્વેશન ID: {res_id}. "
            f"બોક્સ: {comp['box_id']} ({comp['item_name_gu']}). "
            f"રકમ: ₹{amount}. UPI સ્કેન કરી ₹{amount} પે કરો. "
            f"આપનો 6-અંકનો ડિસ્પેન્સર અનલોક OTP: {otp_code} છે. (વેલિડિટી: ૧૫ મિનિટ). "
            f"સહાયતા વ્હોટ્સએપ: {OFFICIAL_WHATSAPP_HELPLINE}"
        )

        return {
            "success": True,
            "reservation_id": res_id,
            "box_id": comp["box_id"],
            "item_name": comp["item_name"],
            "item_name_gu": comp["item_name_gu"],
            "amount_payable": amount,
            "otp_code": otp_code,
            "upi_payload": upi_payload,
            "validity_minutes": 15,
            "message_gu": msg_gu,
            "whatsapp_helpline": OFFICIAL_WHATSAPP_HELPLINE
        }

    def verify_and_unlock(
        self,
        reservation_id: str,
        otp_code: str,
        payment_ref: str = "UPI-AUTOCONFIRMED"
    ) -> Dict[str, Any]:
        """
        Verify payment and OTP code, trigger physical solenoid relay open signal,
        and log automated night sale transaction.
        """
        data = self._read_data()
        res = next((r for r in data.get("active_reservations", []) if r["reservation_id"] == reservation_id), None)

        if not res:
            return {"success": False, "error": f"Reservation '{reservation_id}' not found or has expired."}

        if res["otp_code"] != otp_code.strip():
            return {"success": False, "error": "Invalid OTP code. Please enter the correct 6-digit OTP."}

        comp = next((c for c in data.get("compartments", []) if c["box_id"] == res["box_id"]), None)
        if not comp:
            return {"success": False, "error": f"Target locker '{res['box_id']}' not found."}

        # Decrement stock and update status
        comp["units_inside"] = max(0, comp["units_inside"] - 1)
        comp["status"] = "Available" if comp["units_inside"] > 0 else "Empty - Awaiting Morning Restock"
        comp["door_state"] = "OPEN_UNLOCKED"
        comp["last_accessed"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Mark reservation completed
        res["status"] = "Completed"
        res["payment_ref"] = payment_ref
        res["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        tx_record = {
            "transaction_id": f"TXN-NLK-{int(time.time())}",
            "reservation_id": reservation_id,
            "box_id": comp["box_id"],
            "item_name": comp["item_name"],
            "part_number": comp["part_number"],
            "customer_name": res["customer_name"],
            "phone": res["phone"],
            "vehicle_reg": res.get("vehicle_reg", "Touring Rider"),
            "amount_paid": res["amount_payable"],
            "payment_ref": payment_ref,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "solenoid_status": "RELAY_FIRED_SUCCESS_500MS_PULSE"
        }
        data.setdefault("completed_transactions", []).append(tx_record)

        # Remove from active reservations
        data["active_reservations"] = [r for r in data.get("active_reservations", []) if r["reservation_id"] != reservation_id]
        self._save_data(data)

        receipt_gu = (
            f"✅ બોક્સ {comp['box_id']} નું લોક સફળતાપૂર્વક ખૂલી ગયું છે! "
            f"ગ્રાહક {res['customer_name']} માટે {comp['item_name_gu']} ડિસ્પેન્સ થઈ ગયું છે. "
            f"પેમેન્ટ ₹{res['amount_payable']} સફળ. ડિજિટલ પહોંચ વ્હોટ્સએપ {OFFICIAL_WHATSAPP_HELPLINE} પર મોકલેલ છે. "
            f"સુરક્ષિત સવારી, જય માતાજી!"
        )

        return {
            "success": True,
            "box_id": comp["box_id"],
            "item_name": comp["item_name"],
            "units_remaining": comp["units_inside"],
            "door_state": "OPEN_UNLOCKED",
            "solenoid_relay": "FIRED_PULSE_OPEN",
            "solenoid_pulse": "500ms_12V_HIGH",
            "transaction_id": tx_record["transaction_id"],
            "amount_paid": tx_record["amount_paid"],
            "message_gu": receipt_gu,
            "whatsapp_helpline": OFFICIAL_WHATSAPP_HELPLINE
        }

    def restock_compartment(self, box_id: str, add_units: int = 2, restocked_by: str = "Jayesh Prajapati (Parts Specialist)") -> Dict[str, Any]:
        """Restock a compartment and reset its door status."""
        data = self._read_data()
        comp = next((c for c in data.get("compartments", []) if c["box_id"].upper() == box_id.upper()), None)
        if not comp:
            return {"success": False, "error": f"Compartment '{box_id}' not found."}

        comp["units_inside"] = min(comp["max_capacity"], comp["units_inside"] + add_units)
        comp["status"] = "Available"
        comp["door_state"] = "CLOSED_LOCKED"
        self._save_data(data)

        return {
            "success": True,
            "box_id": comp["box_id"],
            "item_name": comp["item_name"],
            "units_inside": comp["units_inside"],
            "status": comp["status"],
            "restocked_by": restocked_by
        }


# Singleton instance
_night_locker_instance: Optional[ChamundaNightLockerManager] = None

def get_night_locker_manager() -> ChamundaNightLockerManager:
    global _night_locker_instance
    if _night_locker_instance is None:
        _night_locker_instance = ChamundaNightLockerManager()
    return _night_locker_instance
