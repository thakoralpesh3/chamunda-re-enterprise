"""
Chamunda Automobile Parts & Service - Royal Riders Club (CRRC) & AMC Engine.
Fosters the North Gujarat Royal Enfield rider community with:
- 3 Annual Maintenance Contract (AMC) Tiers: Silver Thump, Gold Tourer, Platinum Vintage & Twin
- Verified Thump Club Loyalty Points (Earn 1 Thump Point per ₹10 spent)
- Scheduled Heritage Expeditions (Polo Forest, Nadabet Border, Kutch Salt Rann) with Chamunda SOS Escort
"""

import json
import time
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
MEMBERS_FILE = DATA_DIR / "riders_club_members.json"
EXPEDITIONS_FILE = DATA_DIR / "riders_expeditions.json"

AMC_PLANS = [
    {
        "plan_id": "AMC-SILVER",
        "name": "Silver Thump Pass",
        "name_gu": "સિલ્વર થમ્પ પાસ",
        "annual_fee_inr": 3999,
        "services_included": 3,
        "chain_lube_sessions": 6,
        "parts_discount_pct": 5.0,
        "health_passports_included": 1,
        "features": [
            "3 Comprehensive Periodic Services (Labor Free)",
            "6 High-Pressure Foam Wash & Chain Lube Sessions",
            "5% Flat Discount on Genuine OEM Spare Parts",
            "1 Free Acoustic Thump AI Health Passport with QR Card",
            "WhatsApp Priority Service Booking"
        ],
        "badge_color": "secondary",
        "recommended_for": "Daily Commuters & City Cruisers (Classic 350, Hunter 350)"
    },
    {
        "plan_id": "AMC-GOLD",
        "name": "Gold Tourer Pass",
        "name_gu": "ગોલ્ડ ટૂરર પાસ",
        "annual_fee_inr": 7499,
        "services_included": 4,
        "chain_lube_sessions": 999,  # Unlimited
        "parts_discount_pct": 10.0,
        "health_passports_included": 2,
        "features": [
            "4 Complete Periodic Services (Zero Labor Charges)",
            "Unlimited Foam Wash & Motul Chain Lube & Tightening",
            "10% Flat Discount on All RE Parts & Touring Accessories",
            "24/7 Highway Breakdown SOS Towing & Patrol (50 km Mehsana Radius)",
            "1 Complimentary Full 3M Teflon Anti-Rust Coating",
            "2 Digital Acoustic Thump Health Passports"
        ],
        "badge_color": "warning",
        "recommended_for": "Highway Tourers & Highway Enthusiasts (Himalayan 450, Meteor 350)"
    },
    {
        "plan_id": "AMC-PLATINUM",
        "name": "Platinum Vintage & Twin Pass",
        "name_gu": "પ્લેટિનમ વિન્ટેજ & ટ્વિન પાસ",
        "annual_fee_inr": 11999,
        "services_included": 5,
        "chain_lube_sessions": 999,
        "parts_discount_pct": 15.0,
        "health_passports_included": 4,
        "features": [
            "5 Bespoke Services with Dedicated Master Tech Ramesh Hand-tuning",
            "Unlimited Foam Wash, Ceramic Detailing & Chain Maintenance",
            "15% Flat Discount on All Genuine Parts, Restomods & Custom Paint",
            "Free Doorstep Bike Pick-up & Drop anywhere in Mehsana District",
            "VIP Express Priority Bay 1 Scheduling (Zero Waiting Time)",
            "1 Free Ticket to Annual Chamunda Heritage Expedition (Polo / Kutch)",
            "Unlimited Digital Health Passports & QR Keychains"
        ],
        "badge_color": "danger",
        "recommended_for": "Twin Cylinder & Vintage Cast-Iron Owners (Interceptor 650, 1982 CI Bullet)"
    }
]

DEFAULT_MEMBERS: List[Dict[str, Any]] = [
    {
        "member_id": "CRRC-2026-001",
        "name": "Hardikbhai Patel",
        "phone": "+91 98250 11999",
        "bike_model": "Interceptor 650 (Mark 2 Chrome)",
        "registration_no": "GJ-02-BQ-1234",
        "tier": "Platinum Vintage & Twin Pass",
        "plan_id": "AMC-PLATINUM",
        "membership_status": "Active",
        "valid_until": "2027-04-15",
        "thump_points": 2450,
        "services_used": 1,
        "services_remaining": 4,
        "joined_date": "2026-04-15"
    },
    {
        "member_id": "CRRC-2026-002",
        "name": "Chiragbhai Shah",
        "phone": "+91 94281 33221",
        "bike_model": "Himalayan 450 (Kamet White)",
        "registration_no": "GJ-02-CD-5678",
        "tier": "Gold Tourer Pass",
        "plan_id": "AMC-GOLD",
        "membership_status": "Active",
        "valid_until": "2027-02-10",
        "thump_points": 1800,
        "services_used": 2,
        "services_remaining": 2,
        "joined_date": "2026-02-10"
    },
    {
        "member_id": "CRRC-2026-003",
        "name": "Yogeshbhai Dave",
        "phone": "+91 97235 88776",
        "bike_model": "Classic 350 Reborn (Halcyon Green)",
        "registration_no": "GJ-02-EF-9012",
        "tier": "Silver Thump Pass",
        "plan_id": "AMC-SILVER",
        "membership_status": "Active",
        "valid_until": "2026-12-31",
        "thump_points": 950,
        "services_used": 1,
        "services_remaining": 2,
        "joined_date": "2026-01-01"
    }
]

DEFAULT_EXPEDITIONS: List[Dict[str, Any]] = [
    {
        "expedition_id": "EXP-POLO-2026",
        "title": "Polo Forest Monsoon Thump & Heritage Ride",
        "title_gu": "પોળો ફોરેસ્ટ મોનસૂન થમ્પ રાઇડ",
        "date": "2026-10-04",
        "distance_km": 185,
        "route": "Mehsana Hub -> Idar -> Polo Forest Sanctuary -> Harnav River -> Return",
        "escort_vehicle": "Chamunda Expedition SOS Patrol Van (Tools, Spares & Medical Box)",
        "lead_rider": "Master Tech Ramesh (RE Veteran)",
        "max_riders": 35,
        "registered_riders_count": 22,
        "status": "Registration Open",
        "participation_fee_inr": 850,
        "amc_platinum_free": True
    },
    {
        "expedition_id": "EXP-NADABET-2026",
        "title": "Nadabet Indo-Pak Border Seema Darshan Run",
        "title_gu": "નડાબેટ ભારત-પાક સીમા દર્શન રાઇડ",
        "date": "2026-11-15",
        "distance_km": 310,
        "route": "Mehsana Hub -> Radhanpur -> Suigam -> Nadabet T-Junction -> Zero Point",
        "escort_vehicle": "Chamunda Expedition SOS Patrol Van (Twin Fuel Cans & High-Altitude Kit)",
        "lead_rider": "Master Tech Ramesh",
        "max_riders": 25,
        "registered_riders_count": 18,
        "status": "Registration Open",
        "participation_fee_inr": 1500,
        "amc_platinum_free": True
    }
]


class ChamundaRidersClubManager:
    """Manages Royal Riders Club, AMC plans, memberships, and heritage touring expeditions."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.members_file = self.data_dir / "riders_club_members.json"
        self.expeditions_file = self.data_dir / "riders_expeditions.json"
        self._init_storage()

    def _init_storage(self) -> None:
        if not self.members_file.exists():
            self.members_file.write_text(json.dumps(DEFAULT_MEMBERS, indent=2, ensure_ascii=False), encoding="utf-8")
        if not self.expeditions_file.exists():
            self.expeditions_file.write_text(json.dumps(DEFAULT_EXPEDITIONS, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_amc_plans(self) -> List[Dict[str, Any]]:
        return AMC_PLANS

    def get_members(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.members_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def _save_members(self, members: List[Dict[str, Any]]) -> None:
        self.members_file.write_text(json.dumps(members, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_expeditions(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.expeditions_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def _save_expeditions(self, expeditions: List[Dict[str, Any]]) -> None:
        self.expeditions_file.write_text(json.dumps(expeditions, indent=2, ensure_ascii=False), encoding="utf-8")

    def enroll_member(
        self,
        name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        plan_id: str = "AMC-GOLD"
    ) -> Dict[str, Any]:
        """Enroll a rider into an AMC plan."""
        members = self.get_members()
        plan = next((p for p in AMC_PLANS if p["plan_id"] == plan_id), AMC_PLANS[1])

        now = datetime.datetime.now()
        valid_until = (now + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        member_id = f"CRRC-{now.year}-{len(members) + 1:03d}"

        new_member = {
            "member_id": member_id,
            "name": name.strip(),
            "phone": phone.strip(),
            "bike_model": bike_model.strip(),
            "registration_no": registration_no.upper().strip(),
            "tier": plan["name"],
            "plan_id": plan["plan_id"],
            "membership_status": "Active",
            "valid_until": valid_until,
            "thump_points": 500,  # 500 Welcome Thump points
            "services_used": 0,
            "services_remaining": plan["services_included"],
            "joined_date": now.strftime("%Y-%m-%d")
        }

        members.insert(0, new_member)
        self._save_members(members)
        return new_member

    def register_for_expedition(self, expedition_id: str, rider_name: str, phone: str, bike_model: str) -> Dict[str, Any]:
        """Register a rider for a club expedition."""
        expeditions = self.get_expeditions()
        exp = next((e for e in expeditions if e["expedition_id"] == expedition_id), None)
        if not exp:
            return {"success": False, "message": "Expedition not found"}

        if exp["registered_riders_count"] >= exp["max_riders"]:
            return {"success": False, "message": "Expedition is fully booked"}

        exp["registered_riders_count"] += 1
        self._save_expeditions(expeditions)

        return {
            "success": True,
            "expedition_title": exp["title"],
            "rider_name": rider_name,
            "bike_model": bike_model,
            "date": exp["date"],
            "escort_assigned": exp["escort_vehicle"],
            "total_riders": exp["registered_riders_count"]
        }

    def get_overview(self) -> Dict[str, Any]:
        members = self.get_members()
        expeditions = self.get_expeditions()
        plans = self.get_amc_plans()

        total_members = len(members)
        total_thump_points = sum(m.get("thump_points", 0) for m in members)
        active_amc_revenue = sum(
            next((p["annual_fee_inr"] for p in plans if p["plan_id"] == m.get("plan_id")), 3999)
            for m in members
        )

        return {
            "total_club_members": total_members,
            "total_thump_points_circulating": total_thump_points,
            "annual_amc_revenue_inr": active_amc_revenue,
            "upcoming_expeditions_count": len(expeditions),
            "members": members,
            "plans": plans,
            "expeditions": expeditions
        }


# Global singleton instance
_riders_club_manager: Optional[ChamundaRidersClubManager] = None


def get_riders_club_manager() -> ChamundaRidersClubManager:
    global _riders_club_manager
    if _riders_club_manager is None:
        _riders_club_manager = ChamundaRidersClubManager()
    return _riders_club_manager
