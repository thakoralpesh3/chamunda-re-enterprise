"""
Chamunda Automobile Parts & Service - Royal Enfield Smart Job Card & Diagnostic Engine.
Handles motorcycle check-in, repair estimation, mechanic assignment, and expert RE fault diagnostics.
"""

import sys
import json
import time
import uuid
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


DATA_DIR = Path(__file__).parent / "data"
JOBCARDS_FILE = DATA_DIR / "job_cards.json"


RE_EXPERT_DIAGNOSTICS = {
    "tappet_noise": {
        "symptom": "Rattling / ticking metal sound from cylinder head on cold/hot idle",
        "models": ["Classic 350", "Hunter 350", "Meteor 350", "UCE 350/500", "650 Twins"],
        "root_cause": "Excessive valve clearance or auto-decompressor spring tension drop.",
        "recommended_action": "Set valve clearance (Inlet: 0.08mm, Exhaust: 0.18mm with feeler gauge when engine is stone cold). Replace head gasket O-ring.",
        "estimated_labor_inr": 450,
        "parts_needed": ["Cylinder Head Cover O-Ring", "Rocker Gasket"],
        "turnaround_time": "1.5 hours"
    },
    "wobble_at_high_speed": {
        "symptom": "Handlebar vibration / wobble at 70-90 km/h or on deceleration",
        "models": ["Classic 350", "Bullet 350", "Himalayan 411/450", "Interceptor 650"],
        "root_cause": "Conical steering cone set play, front tyre uneven wear/pressure, or rim spoke truing required.",
        "recommended_action": "Inspect & tighten T-stem bearing cone set; true front spoke wheel with dial indicator; set tyre pressure to 32 PSI.",
        "estimated_labor_inr": 600,
        "parts_needed": ["Steering Cone Set (SKF/Genuine)", "Fork Oil 10W"],
        "turnaround_time": "2 hours"
    },
    "cold_start_stalling": {
        "symptom": "Engine starts but cuts off immediately within 5 seconds when cold",
        "models": ["Hunter 350", "Meteor 350", "Classic 350 Reborn", "Himalayan 450"],
        "root_cause": "Carbon buildup on Stepper Motor / Idle Air Control Valve (IACV) or fouled spark plug.",
        "recommended_action": "Remove throttle body, ultrasonic clean IACV valve with throttle cleaner spray, check ECU firmware version, reset TPS calibration.",
        "estimated_labor_inr": 500,
        "parts_needed": ["Throttle Body Spray Cleaner", "NGK Spark Plug"],
        "turnaround_time": "1 hour"
    },
    "clutch_slippage": {
        "symptom": "Engine RPM rises on throttle but motorcycle does not accelerate proportionally in 4th/5th gear",
        "models": ["Interceptor 650", "Continental GT 650", "Classic 350/500 UCE"],
        "root_cause": "Worn friction plates, glazed steel clutch plates, or wrong non-JASO MA2 engine oil used.",
        "recommended_action": "Replace friction clutch plate pack, inspect slipper assist springs, flush and refill with Motul 7100 15W-50 JASO MA2.",
        "estimated_labor_inr": 750,
        "parts_needed": ["Complete Clutch Plate Set", "Clutch Cover Gasket", "Motul 15W-50 2.5L"],
        "turnaround_time": "3 hours"
    },
    "battery_drain": {
        "symptom": "Self-starter clicks or fails in morning after standing overnight",
        "models": ["All Royal Enfield EFI Models"],
        "root_cause": "Parasitic drain from aftermarket accessories (fog lights / mobile charger), faulty starter relay, or stator coil charging drop.",
        "recommended_action": "Multimeter check: idle charging voltage must be 14.2V - 14.6V at 2500 RPM. Clean relay terminal rust, install relay-isolated harness.",
        "estimated_labor_inr": 350,
        "parts_needed": ["Starter Solenoid Relay", "Exide 14Ah Battery (if cell dead)"],
        "turnaround_time": "45 mins"
    }
}


class ChamundaServiceManager:
    """Manages service workflow, bike diagnostics, and digital job cards."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.jobcards_file = self.data_dir / "job_cards.json"
        self._initialize_jobcards()

    def _initialize_jobcards(self) -> None:
        if not self.jobcards_file.exists():
            self.jobcards_file.write_text("[]", encoding="utf-8")

    def get_all_job_cards(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.jobcards_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def create_job_card(
        self,
        customer_name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        odometer_km: int,
        customer_issues: str,
        service_type: str = "General Service & Diagnostics",
        mechanic_assigned: str = "Workshop Technician"
    ) -> Dict[str, Any]:
        """Create and persist a new customer job card."""
        job_cards = self.get_all_job_cards()
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        job_card_id = f"JOB-{today_str}-{len(job_cards) + 1:03d}"

        # Automatic diagnostic recommendation based on customer issues
        diag = self.diagnose_fault(customer_issues)

        new_card = {
            "job_card_id": job_card_id,
            "customer_name": customer_name,
            "phone": phone,
            "bike_model": bike_model,
            "registration_no": registration_no.upper().strip(),
            "odometer_km": odometer_km,
            "service_type": service_type,
            "customer_issues": customer_issues,
            "diagnostic_recommendation": diag.get("recommended_action", "Standard multipoint inspection"),
            "mechanic_assigned": mechanic_assigned,
            "parts_allocated": [],
            "labor_charges": diag.get("estimated_labor_inr", 500),
            "status": "In Service Bay",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "estimated_delivery": (datetime.datetime.now() + datetime.timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
            "total_amount": diag.get("estimated_labor_inr", 500)
        }

        job_cards.insert(0, new_card)
        self.jobcards_file.write_text(json.dumps(job_cards, indent=2), encoding="utf-8")
        return new_card

    def update_job_card_status(self, job_card_id: str, new_status: str) -> bool:
        """Update job card status (e.g. 'In Service Bay', 'Quality Check', 'Ready for Delivery', 'Completed')."""
        job_cards = self.get_all_job_cards()
        found = False
        for card in job_cards:
            if card["job_card_id"] == job_card_id:
                card["status"] = new_status
                if new_status == "Completed":
                    card["completed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                found = True
                break
        if found:
            self.jobcards_file.write_text(json.dumps(job_cards, indent=2), encoding="utf-8")
        return found

    def add_parts_to_job(self, job_card_id: str, part_name: str, qty: int, price: float) -> bool:
        """Add spare part to an open job card."""
        job_cards = self.get_all_job_cards()
        found = False
        for card in job_cards:
            if card["job_card_id"] == job_card_id:
                card.setdefault("parts_allocated", []).append({
                    "name": part_name,
                    "qty": qty,
                    "price": price
                })
                parts_sum = sum(p["qty"] * p["price"] for p in card["parts_allocated"])
                card["total_amount"] = parts_sum + card.get("labor_charges", 500)
                found = True
                break
        if found:
            self.jobcards_file.write_text(json.dumps(job_cards, indent=2), encoding="utf-8")
        return found

    def complete_job_and_generate_invoice(
        self,
        job_card_id: str,
        technician: str = "Master Tech Alpesh (Chamunda Automobile)",
        service_notes: str = "Standard 50-Point Master Service & Valve Calibration",
        audio_path: Optional[str] = None,
        gst_pct: float = 18.0
    ) -> Dict[str, Any]:
        """
        Complete the job card, generate the Digital Acoustic Health Passport,
        and generate a GST invoice with embedded verifiable QR code.
        """
        job_cards = self.get_all_job_cards()
        target_card = None
        for card in job_cards:
            if card["job_card_id"] == job_card_id:
                target_card = card
                break

        if not target_card:
            raise ValueError(f"Job Card {job_card_id} not found.")

        # Import modules dynamically to avoid circular imports
        sys.path.insert(0, str(Path(__file__).parent))
        from acoustic_health_passport import ChamundaHealthPassportGenerator
        from billing_engine import ChamundaBillingManager

        passport_gen = ChamundaHealthPassportGenerator()
        passport_record = passport_gen.generate_health_passport(
            customer_name=target_card["customer_name"],
            phone=target_card["phone"],
            bike_model=target_card["bike_model"],
            registration_no=target_card["registration_no"],
            odometer_km=target_card.get("odometer_km", 10000),
            service_notes=service_notes,
            technician=technician,
            audio_path=audio_path
        )

        billing_mgr = ChamundaBillingManager()
        invoice_record = billing_mgr.generate_invoice_html(
            job_card_id=job_card_id,
            customer_name=target_card["customer_name"],
            phone=target_card["phone"],
            bike_model=target_card["bike_model"],
            registration_no=target_card["registration_no"],
            odometer_km=target_card.get("odometer_km", 10000),
            parts=target_card.get("parts_allocated", []),
            labor_charges=target_card.get("labor_charges", 500.0),
            gst_pct=gst_pct,
            passport_data=passport_record
        )

        # Update card status and attach invoice/passport
        target_card["status"] = "Completed"
        target_card["completed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        target_card["invoice_no"] = invoice_record["invoice_no"]
        target_card["invoice_file"] = invoice_record["invoice_file"]
        target_card["passport_id"] = passport_record["passport_id"]
        target_card["passport_file"] = passport_record["html_path"]
        target_card["health_score"] = passport_record["overall_score"]
        target_card["grand_total"] = invoice_record["grand_total"]

        self.jobcards_file.write_text(json.dumps(job_cards, indent=2), encoding="utf-8")

        return {
            "job_card_id": job_card_id,
            "status": "Completed",
            "customer_name": target_card["customer_name"],
            "bike_model": target_card["bike_model"],
            "registration_no": target_card["registration_no"],
            "invoice_no": invoice_record["invoice_no"],
            "invoice_file": invoice_record["invoice_file"],
            "grand_total": invoice_record["grand_total"],
            "subtotal": invoice_record["subtotal"],
            "gst_amount": invoice_record["gst_amount"],
            "passport_id": passport_record["passport_id"],
            "passport_file": passport_record["html_path"],
            "health_score": passport_record["overall_score"],
            "grade": passport_record["grade"],
            "qr_code_base64": invoice_record["qr_code_base64"],
            "whatsapp_gujarati": invoice_record["whatsapp_message_gujarati"],
            "whatsapp_english": invoice_record["whatsapp_message"],
            "next_service_date": invoice_record["next_service_date"],
            "next_service_km": invoice_record["next_service_km"]
        }

    def diagnose_fault(self, issue_description: str) -> Dict[str, Any]:
        """Match customer reported symptoms against Royal Enfield expert diagnostic rules."""
        desc_lower = issue_description.lower()

        if any(k in desc_lower for k in ["tappet", "tick", "ticking", "valve", "clatter"]):
            return RE_EXPERT_DIAGNOSTICS["tappet_noise"]
        elif any(k in desc_lower for k in ["wobble", "vibrate", "vibration", "handle", "handlebar", "cone", "fork"]):
            return RE_EXPERT_DIAGNOSTICS["wobble_at_high_speed"]
        elif any(k in desc_lower for k in ["stall", "stalling", "cut off", "start problem", "cold start", "idle"]):
            return RE_EXPERT_DIAGNOSTICS["cold_start_stalling"]
        elif any(k in desc_lower for k in ["clutch", "slip", "slipping", "pickup", "acceleration"]):
            return RE_EXPERT_DIAGNOSTICS["clutch_slippage"]
        elif any(k in desc_lower for k in ["battery", "drain", "self", "starter", "dead", "relay", "click"]):
            return RE_EXPERT_DIAGNOSTICS["battery_drain"]

        return {
            "symptom": issue_description,
            "root_cause": "General wear or routine maintenance required.",
            "recommended_action": "Perform 24-point Royal Enfield periodic service inspection and test ride.",
            "estimated_labor_inr": 500,
            "parts_needed": ["Motul 15W-50 4T Engine Oil", "Genuine Oil Filter"],
            "turnaround_time": "2 hours"
        }
