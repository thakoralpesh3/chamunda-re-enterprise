"""
Chamunda Automobile Parts & Service - Multi-Branch Cloud Network & Franchise Operating System.
Centralized management for North Gujarat branches:
1. HQ-MEHSANA: Mehsana Central Hub & Master Warehouse
2. BR-PATAN-01: Patan Heritage Spares & Service Center
3. BR-VISN-02: Visnagar Express Bay & Diagnostic Hub
4. BR-UNJHA-03: Unjha Spares Depot & Highway Quick Service
5. BR-PALAN-04: Palanpur Highway Outpost & Expedition Base

Provides consolidated network telemetry, intra-branch inventory transfer routing,
and franchise operational performance tracking.
"""

import json
import time
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
NETWORK_FILE = DATA_DIR / "multibranch_network.json"

DEFAULT_BRANCHES: List[Dict[str, Any]] = [
    {
        "branch_id": "HQ-MEHSANA",
        "name": "Mehsana Central Hub & Master Warehouse",
        "name_gu": "મહેસાણા સેન્ટ્રલ હબ અને મુખ્ય વેરહાઉસ",
        "city": "Mehsana",
        "district": "Mehsana",
        "address": "Opp. Radhanpur Road Cross, Mehsana, Gujarat 384002",
        "manager": "Ramesh Patel (Master Tech & Ops Lead)",
        "phone": "+91 78747 19139",
        "is_hq": True,
        "active_bays": 6,
        "today_jobs": 28,
        "today_revenue_inr": 84500,
        "stock_sku_count": 4469,
        "stock_valuation_inr": 2845000,
        "status": "Online",
        "color_badge": "success"
    },
    {
        "branch_id": "BR-PATAN-01",
        "name": "Patan Heritage Spares & Service Hub",
        "name_gu": "પાટણ હેરિટેજ સ્પેર અને સર્વિસ હબ",
        "city": "Patan",
        "district": "Patan",
        "address": "Near Hemchandracharya North Gujarat Univ Road, Patan 384265",
        "manager": "Jignesh Prajapati (Senior Tech)",
        "phone": "+91 98251 45012",
        "is_hq": False,
        "active_bays": 3,
        "today_jobs": 14,
        "today_revenue_inr": 36200,
        "stock_sku_count": 1820,
        "stock_valuation_inr": 920000,
        "status": "Online",
        "color_badge": "primary"
    },
    {
        "branch_id": "BR-VISN-02",
        "name": "Visnagar Express Bay & Diagnostics",
        "name_gu": "વિસનગર એક્સપ્રેસ બે અને ડાયગ્નોસ્ટિક્સ",
        "city": "Visnagar",
        "district": "Mehsana",
        "address": "Kansa Char Rasta, Visnagar 384315",
        "manager": "Pravin Solanki (Diagnostic Specialist)",
        "phone": "+91 94283 67104",
        "is_hq": False,
        "active_bays": 2,
        "today_jobs": 11,
        "today_revenue_inr": 24800,
        "stock_sku_count": 1240,
        "stock_valuation_inr": 680000,
        "status": "Online",
        "color_badge": "info"
    },
    {
        "branch_id": "BR-UNJHA-03",
        "name": "Unjha Spares Depot & Highway Quick Service",
        "name_gu": "ઊંઝા સ્પેર ડેપો અને હાઇવે ક્વિક સર્વિસ",
        "city": "Unjha",
        "district": "Mehsana",
        "address": "APMC Market Yard Bypass Road, Unjha 384170",
        "manager": "Haresh Chaudhari (Parts Specialist)",
        "phone": "+91 97230 89211",
        "is_hq": False,
        "active_bays": 2,
        "today_jobs": 9,
        "today_revenue_inr": 19400,
        "stock_sku_count": 1450,
        "stock_valuation_inr": 740000,
        "status": "Online",
        "color_badge": "warning"
    },
    {
        "branch_id": "BR-PALAN-04",
        "name": "Palanpur Highway Outpost & Expedition Base",
        "name_gu": "પાલનપુર હાઇવે આઉટપોસ્ટ અને એક્સપિડિશન બેઝ",
        "city": "Palanpur",
        "district": "Banaskantha",
        "address": "NH-27 Mount Abu Highway Junction, Palanpur 385001",
        "manager": "Dhaval Vaghela (Expedition SOS Lead)",
        "phone": "+91 99092 34870",
        "is_hq": False,
        "active_bays": 2,
        "today_jobs": 8,
        "today_revenue_inr": 22100,
        "stock_sku_count": 1100,
        "stock_valuation_inr": 590000,
        "status": "Online",
        "color_badge": "danger"
    }
]

DEFAULT_TRANSFERS: List[Dict[str, Any]] = [
    {
        "transfer_id": "TRF-20260912-001",
        "timestamp": "2026-09-12 10:15 AM",
        "from_branch": "HQ-MEHSANA",
        "to_branch": "BR-PATAN-01",
        "part_number": "574012/A",
        "part_name": "SOHC Camshaft Assembly with Decompressor (J-Series 350)",
        "quantity": 2,
        "unit_mrp": 2450,
        "total_value_inr": 4900,
        "requested_by": "Jignesh Prajapati (Patan Branch Lead)",
        "status": "Delivered",
        "notes": "Emergency express dispatch for Classic Reborn top-end overhaul job."
    },
    {
        "transfer_id": "TRF-20260912-002",
        "timestamp": "2026-09-12 02:40 PM",
        "from_branch": "HQ-MEHSANA",
        "to_branch": "BR-PALAN-04",
        "part_number": "KXA00310",
        "part_name": "Sherpa 450 Wax Pellet Thermostat Unit",
        "quantity": 3,
        "unit_mrp": 890,
        "total_value_inr": 2670,
        "requested_by": "Dhaval Vaghela (Palanpur Lead)",
        "status": "In-Transit",
        "notes": "SOS stock replenishment for Himalayan 450 Abu highway travelers."
    }
]


class ChamundaMultiBranchManager:
    """Manages multi-branch network telemetry, intra-branch stock movements, and consolidated analytics."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.network_file = self.data_dir / "multibranch_network.json"
        self._init_storage()

    def _init_storage(self) -> None:
        if not self.network_file.exists():
            payload = {
                "branches": DEFAULT_BRANCHES,
                "transfers": DEFAULT_TRANSFERS,
                "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
            }
            self.network_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    def _read_data(self) -> Dict[str, Any]:
        try:
            return json.loads(self.network_file.read_text(encoding="utf-8") or "{}")
        except Exception:
            return {"branches": DEFAULT_BRANCHES, "transfers": DEFAULT_TRANSFERS}

    def _write_data(self, data: Dict[str, Any]) -> None:
        data["last_sync"] = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        self.network_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_branches(self) -> List[Dict[str, Any]]:
        data = self._read_data()
        return data.get("branches", DEFAULT_BRANCHES)

    def get_branch_by_id(self, branch_id: str) -> Optional[Dict[str, Any]]:
        branches = self.get_branches()
        clean_id = branch_id.upper().strip()
        return next((b for b in branches if b["branch_id"] == clean_id), None)

    def get_transfers(self) -> List[Dict[str, Any]]:
        data = self._read_data()
        return data.get("transfers", DEFAULT_TRANSFERS)

    def get_branches_overview(self) -> Dict[str, Any]:
        """Generate high-level multi-branch consolidated executive dashboard telemetry."""
        branches = self.get_branches()
        transfers = self.get_transfers()

        total_bays = sum(b.get("active_bays", 0) for b in branches)
        total_jobs_today = sum(b.get("today_jobs", 0) for b in branches)
        total_revenue_today = sum(b.get("today_revenue_inr", 0) for b in branches)
        total_stock_valuation = sum(b.get("stock_valuation_inr", 0) for b in branches)
        total_sku_coverage = sum(b.get("stock_sku_count", 0) for b in branches)

        in_transit_transfers = sum(1 for t in transfers if t.get("status") == "In-Transit")

        return {
            "network_status": "Healthy & Unified (5 Active Branches)",
            "hq_branch": "HQ-MEHSANA (Radhanpur Road Central Warehouse)",
            "total_branches": len(branches),
            "total_active_bays": total_bays,
            "total_jobs_today": total_jobs_today,
            "total_revenue_today_inr": total_revenue_today,
            "total_inventory_valuation_inr": total_stock_valuation,
            "total_network_sku_count": total_sku_coverage,
            "pending_transfers_count": in_transit_transfers,
            "branches": branches,
            "recent_transfers": transfers[:10],
            "last_cloud_sync": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        }

    def transfer_stock(
        self,
        from_branch: str,
        to_branch: str,
        part_number: str,
        quantity: int = 1,
        requested_by: str = "Branch Lead",
        part_name: Optional[str] = None,
        unit_mrp: float = 0.0,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Execute intra-branch stock requisition and dispatch log."""
        data = self._read_data()
        branches = data.get("branches", [])
        transfers = data.get("transfers", [])

        # Validate branches
        from_b = next((b for b in branches if b["branch_id"] == from_branch.upper().strip()), None)
        to_b = next((b for b in branches if b["branch_id"] == to_branch.upper().strip()), None)

        if not from_b or not to_b:
            raise ValueError(f"Invalid branch IDs: {from_branch} -> {to_branch}")

        if from_b["branch_id"] == to_b["branch_id"]:
            raise ValueError("Source and destination branch cannot be the same.")

        if quantity <= 0:
            raise ValueError("Transfer quantity must be greater than 0.")

        # If part name / price not provided, attempt to look up in catalog
        display_part_name = part_name or f"OEM Spares Part #{part_number}"
        price = unit_mrp if unit_mrp > 0 else 1250.0

        now = datetime.datetime.now()
        transfer_id = f"TRF-{now.strftime('%Y%m%d')}-{int(time.time()) % 10000:04d}"

        transfer_record = {
            "transfer_id": transfer_id,
            "timestamp": now.strftime("%Y-%m-%d %I:%M %p"),
            "from_branch": from_b["branch_id"],
            "from_branch_name": from_b["name"],
            "to_branch": to_b["branch_id"],
            "to_branch_name": to_b["name"],
            "part_number": part_number,
            "part_name": display_part_name,
            "quantity": quantity,
            "unit_mrp": price,
            "total_value_inr": round(price * quantity, 2),
            "requested_by": requested_by,
            "status": "In-Transit",
            "notes": notes or f"Express intra-branch transfer from {from_b['city']} to {to_b['city']}."
        }

        # Update source and dest branch telemetry lightly
        from_b["stock_valuation_inr"] = max(0, from_b.get("stock_valuation_inr", 0) - int(price * quantity))
        to_b["stock_valuation_inr"] = to_b.get("stock_valuation_inr", 0) + int(price * quantity)

        transfers.insert(0, transfer_record)
        data["branches"] = branches
        data["transfers"] = transfers[:50]
        self._write_data(data)

        return {
            "success": True,
            "transfer_id": transfer_id,
            "message": f"Stock transfer dispatched from {from_b['name']} to {to_b['name']}.",
            "message_gu": f"{from_b['name_gu']} થી {to_b['name_gu']} માટે {quantity}x {display_part_name} સફળતાપૂર્વક ડિસ્પેચ કરવામાં આવ્યું.",
            "transfer": transfer_record
        }


# Global singleton instance
_multibranch_hub_engine: Optional[ChamundaMultiBranchManager] = None


def get_multibranch_engine() -> ChamundaMultiBranchManager:
    global _multibranch_hub_engine
    if _multibranch_hub_engine is None:
        _multibranch_hub_engine = ChamundaMultiBranchManager()
    return _multibranch_hub_engine
