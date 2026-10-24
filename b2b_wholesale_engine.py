"""
Chamunda Automobile Parts & Service - B2B Wholesale Genuine Spares Distribution Engine.
Serves 200+ local two-wheeler garages across North Gujarat:
Mehsana, Patan, Unjha, Visnagar, Kadi, Siddhpur, Vadnagar, Kheralu, Chanasma.

Features:
- 4 Partner Tiers: Bronze (12%), Silver (16%), Gold (20%), Platinum Hub (25% off MRP)
- 4,469 Genuine Royal Enfield OEM SKUs wholesale inventory lookup
- Bulk PO & WhatsApp Requisition (+91 78747 19139)
- Dynamic NPCI UPI QR & Credit Ledger Tracking (7/15/30 days credit)
- Daily Express Delivery Van Logistics & Route Planning
"""

import io
import json
import time
import base64
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
import qrcode

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
GARAGES_FILE = DATA_DIR / "b2b_garages.json"
ORDERS_FILE = DATA_DIR / "b2b_wholesale_orders.json"
PARTS_FILE = DATA_DIR / "re_parts_catalog.json"

# Tier Configuration
TIER_DISCOUNTS = {
    "Bronze": {"discount_pct": 12.0, "min_monthly_inr": 15000, "credit_days": 0, "badge": "secondary"},
    "Silver": {"discount_pct": 16.0, "min_monthly_inr": 35000, "credit_days": 7, "badge": "info"},
    "Gold": {"discount_pct": 20.0, "min_monthly_inr": 75000, "credit_days": 15, "badge": "warning"},
    "Platinum": {"discount_pct": 25.0, "min_monthly_inr": 150000, "credit_days": 30, "badge": "danger"}
}

# Initial Garages across North Gujarat
DEFAULT_GARAGES: List[Dict[str, Any]] = [
    {
        "garage_id": "GAR-PATAN-001",
        "name": "Siddheshwar Bullet Works",
        "owner_name": "Bharatbhai Prajapati",
        "phone": "+91 98251 11223",
        "city": "Patan",
        "address": "Opp. Old Ganj Bazaar, Patan-Chanasma Highway, Patan",
        "tier": "Gold",
        "gstin": "24ABCPP1234F1Z8",
        "credit_limit_inr": 100000,
        "outstanding_balance_inr": 24500,
        "monthly_orders_count": 8,
        "joined_date": "2025-11-10",
        "preferred_route": "Route 1: North Highway Corridor"
    },
    {
        "garage_id": "GAR-UNJHA-002",
        "name": "Umiya Two-Wheeler Care",
        "owner_name": "Hareshbhai Patel",
        "phone": "+91 94280 22334",
        "city": "Unjha",
        "address": "Near APMC Market Gate 2, Unjha",
        "tier": "Silver",
        "gstin": "24AABCU5678G1Z2",
        "credit_limit_inr": 50000,
        "outstanding_balance_inr": 12000,
        "monthly_orders_count": 5,
        "joined_date": "2026-01-15",
        "preferred_route": "Route 1: North Highway Corridor"
    },
    {
        "garage_id": "GAR-VISN-003",
        "name": "Mahadev RE Clinic",
        "owner_name": "Dineshbhai Rabari",
        "phone": "+91 97230 33445",
        "city": "Visnagar",
        "address": "Station Road, Near ITI Circle, Visnagar",
        "tier": "Platinum",
        "gstin": "24ABCMR9012H1Z5",
        "credit_limit_inr": 250000,
        "outstanding_balance_inr": 48200,
        "monthly_orders_count": 14,
        "joined_date": "2025-08-20",
        "preferred_route": "Route 2: East Industrial Loop"
    },
    {
        "garage_id": "GAR-KADI-004",
        "name": "Maruti Auto Service & Spares",
        "owner_name": "Pravinbhai Vaghela",
        "phone": "+91 98980 44556",
        "city": "Kadi",
        "address": "Chhatral-Kadi GIDC Road, Kadi",
        "tier": "Gold",
        "gstin": "24AABCM3456J1Z1",
        "credit_limit_inr": 120000,
        "outstanding_balance_inr": 18500,
        "monthly_orders_count": 9,
        "joined_date": "2025-10-05",
        "preferred_route": "Route 3: South GIDC Express"
    },
    {
        "garage_id": "GAR-SIDD-005",
        "name": "Rudra Bullet Point",
        "owner_name": "Kamleshbhai Rawal",
        "phone": "+91 94090 55667",
        "city": "Siddhpur",
        "address": "Bindu Sarovar Road, Siddhpur",
        "tier": "Bronze",
        "gstin": "24AACCR7890K1Z9",
        "credit_limit_inr": 20000,
        "outstanding_balance_inr": 3400,
        "monthly_orders_count": 3,
        "joined_date": "2026-03-01",
        "preferred_route": "Route 1: North Highway Corridor"
    }
]

# Delivery Routes across North Gujarat
DELIVERY_ROUTES: List[Dict[str, Any]] = [
    {
        "route_id": "ROUTE-1",
        "name": "Route 1: North Highway Corridor",
        "coverage": ["Mehsana (Hub)", "Unjha", "Siddhpur", "Patan"],
        "departure_time": "10:30 AM Daily",
        "vehicle": "Chamunda Spares Patrol Van (GJ-02-AT-5555)",
        "driver_name": "Mukeshbhai Parmar",
        "driver_phone": "+91 98254 99112",
        "estimated_turnaround_hours": 4.5,
        "status": "Scheduled for Morning Dispatch"
    },
    {
        "route_id": "ROUTE-2",
        "name": "Route 2: East Industrial Loop",
        "coverage": ["Mehsana (Hub)", "Visnagar", "Vadnagar", "Kheralu"],
        "departure_time": "02:00 PM Daily",
        "vehicle": "Chamunda Express Utility Van (GJ-02-BX-8888)",
        "driver_name": "Rakeshbhai Vankar",
        "driver_phone": "+91 94285 77221",
        "estimated_turnaround_hours": 4.0,
        "status": "Scheduled for Afternoon Dispatch"
    },
    {
        "route_id": "ROUTE-3",
        "name": "Route 3: South GIDC Express",
        "coverage": ["Mehsana (Hub)", "Kadi", "Kalol Highway", "Chanasma"],
        "departure_time": "11:30 AM Daily",
        "vehicle": "Chamunda Logistics Cargo Van (GJ-02-CZ-3333)",
        "driver_name": "Sureshbhai Desai",
        "driver_phone": "+91 97231 66332",
        "estimated_turnaround_hours": 3.5,
        "status": "Scheduled for Mid-Day Dispatch"
    }
]

# Initial Wholesale Orders
DEFAULT_ORDERS: List[Dict[str, Any]] = [
    {
        "order_id": "B2B-20260912-001",
        "garage_id": "GAR-VISN-003",
        "garage_name": "Mahadev RE Clinic",
        "city": "Visnagar",
        "tier": "Platinum",
        "discount_pct": 25.0,
        "items": [
            {"part_number": "574050/C", "name": "Genuine Oil Filter Element", "quantity": 20, "mrp": 210, "unit_rate": 157.5, "total_rate": 3150},
            {"part_number": "147008/A", "name": "OEM Pleated Air Filter Element", "quantity": 10, "mrp": 380, "unit_rate": 285.0, "total_rate": 2850},
            {"part_number": "592188/B", "name": "Bybre Front Disc Brake Pads", "quantity": 5, "mrp": 680, "unit_rate": 510.0, "total_rate": 2550}
        ],
        "mrp_total_inr": 11400.0,
        "discount_amount_inr": 2850.0,
        "subtotal_inr": 8550.0,
        "gst_amount_inr": 1539.0,
        "net_payable_inr": 10089.0,
        "payment_mode": "Credit (30 Days)",
        "order_status": "Packed & Ready for Route 2 Dispatch",
        "delivery_route": "Route 2: East Industrial Loop",
        "created_at": "2026-09-12 11:30 AM",
        "tracking_code": "CHAM-B2B-TRK-9901"
    }
]


def generate_b2b_qr(upi_uri: str) -> str:
    """Generate base64 encoded QR code for dynamic NPCI B2B instant settlement."""
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0d6efd", back_color="#ffffff")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


class ChamundaB2BWholesaleManager:
    """Enterprise wholesale management, tiered pricing, bulk PO processing, and dispatch routes."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.garages_file = self.data_dir / "b2b_garages.json"
        self.orders_file = self.data_dir / "b2b_wholesale_orders.json"
        self._init_storage()

    def _init_storage(self) -> None:
        if not self.garages_file.exists():
            self.garages_file.write_text(json.dumps(DEFAULT_GARAGES, indent=2, ensure_ascii=False), encoding="utf-8")
        if not self.orders_file.exists():
            self.orders_file.write_text(json.dumps(DEFAULT_ORDERS, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_garages(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.garages_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def _save_garages(self, garages: List[Dict[str, Any]]) -> None:
        self.garages_file.write_text(json.dumps(garages, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_orders(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.orders_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def _save_orders(self, orders: List[Dict[str, Any]]) -> None:
        self.orders_file.write_text(json.dumps(orders, indent=2, ensure_ascii=False), encoding="utf-8")

    def register_garage(
        self,
        name: str,
        owner_name: str,
        phone: str,
        city: str,
        address: str,
        tier: str = "Bronze",
        gstin: str = ""
    ) -> Dict[str, Any]:
        """Register a new partner garage in North Gujarat."""
        garages = self.get_garages()
        clean_city = city.strip().upper()[:4]
        gid = f"GAR-{clean_city}-{len(garages) + 1:03d}"
        tier_info = TIER_DISCOUNTS.get(tier, TIER_DISCOUNTS["Bronze"])

        # Determine route based on city
        preferred_route = "Route 1: North Highway Corridor"
        if city.lower() in ["visnagar", "vadnagar", "kheralu"]:
            preferred_route = "Route 2: East Industrial Loop"
        elif city.lower() in ["kadi", "kalol", "chanasma"]:
            preferred_route = "Route 3: South GIDC Express"

        new_garage = {
            "garage_id": gid,
            "name": name.strip(),
            "owner_name": owner_name.strip(),
            "phone": phone.strip(),
            "city": city.strip(),
            "address": address.strip(),
            "tier": tier,
            "gstin": gstin.strip() or f"24{clean_city}9999Z",
            "credit_limit_inr": tier_info["min_monthly_inr"] * 2,
            "outstanding_balance_inr": 0.0,
            "monthly_orders_count": 0,
            "joined_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "preferred_route": preferred_route
        }

        garages.append(new_garage)
        self._save_garages(garages)
        return new_garage

    def calculate_order_pricing(self, garage_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate line items, bulk margin discounts, and GST."""
        garages = {g["garage_id"]: g for g in self.get_garages()}
        garage = garages.get(garage_id, {
            "name": "Walk-in B2B Garage", "tier": "Bronze", "city": "Mehsana", "preferred_route": "Route 1: North Highway Corridor"
        })

        tier = garage.get("tier", "Bronze")
        tier_cfg = TIER_DISCOUNTS.get(tier, TIER_DISCOUNTS["Bronze"])
        discount_pct = tier_cfg["discount_pct"]

        processed_items = []
        mrp_total = 0.0
        discounted_subtotal = 0.0

        for item in items:
            mrp = float(item.get("mrp", 200))
            qty = int(item.get("quantity", 1))
            unit_rate = round(mrp * (1 - (discount_pct / 100.0)), 2)
            item_total = round(unit_rate * qty, 2)
            mrp_total += mrp * qty
            discounted_subtotal += item_total

            processed_items.append({
                "part_number": item.get("part_number", "OEM-RE-PART"),
                "name": item.get("name", "Royal Enfield Genuine Part"),
                "quantity": qty,
                "mrp": mrp,
                "unit_rate": unit_rate,
                "total_rate": item_total
            })

        discount_amount = round(mrp_total - discounted_subtotal, 2)
        gst_amount = round(discounted_subtotal * 0.18, 2)
        net_payable = round(discounted_subtotal + gst_amount, 2)

        return {
            "garage": garage,
            "tier": tier,
            "discount_pct": discount_pct,
            "items": processed_items,
            "mrp_total_inr": mrp_total,
            "discount_amount_inr": discount_amount,
            "subtotal_inr": discounted_subtotal,
            "gst_amount_inr": gst_amount,
            "net_payable_inr": net_payable
        }

    def create_order(
        self,
        garage_id: str,
        items: List[Dict[str, Any]],
        payment_mode: str = "Credit",
        notes: str = ""
    ) -> Dict[str, Any]:
        """Create a new wholesale B2B order, compute discounts, generate QR code, and assign delivery route."""
        calc = self.calculate_order_pricing(garage_id, items)
        garage = calc["garage"]
        now = datetime.datetime.now()
        order_id = f"B2B-{now.strftime('%Y%m%d')}-{int(time.time()) % 10000:04d}"
        tracking_code = f"CHAM-B2B-TRK-{int(time.time()) % 9000 + 1000}"

        # Generate Dynamic UPI QR for instantaneous settlement
        upi_string = f"upi://pay?pa=chamundaauto@okhdfcbank&pn=Chamunda+Automobile+Spares&am={calc['net_payable_inr']:.2f}&cu=INR&tn={order_id}"
        qr_code_b64 = generate_b2b_qr(upi_string)

        order = {
            "order_id": order_id,
            "garage_id": garage_id,
            "garage_name": garage.get("name", "Unknown Garage"),
            "city": garage.get("city", "Mehsana"),
            "tier": calc["tier"],
            "discount_pct": calc["discount_pct"],
            "items": calc["items"],
            "mrp_total_inr": calc["mrp_total_inr"],
            "discount_amount_inr": calc["discount_amount_inr"],
            "subtotal_inr": calc["subtotal_inr"],
            "gst_amount_inr": calc["gst_amount_inr"],
            "net_payable_inr": calc["net_payable_inr"],
            "payment_mode": payment_mode,
            "order_status": "Dispatched to Warehouse Bay for Packing",
            "delivery_route": garage.get("preferred_route", "Route 1: North Highway Corridor"),
            "created_at": now.strftime("%Y-%m-%d %I:%M %p"),
            "tracking_code": tracking_code,
            "qr_code_b64": qr_code_b64,
            "notes": notes
        }

        orders = self.get_orders()
        orders.insert(0, order)
        self._save_orders(orders)

        # Update garage balance & count
        garages = self.get_garages()
        for g in garages:
            if g["garage_id"] == garage_id:
                g["monthly_orders_count"] = g.get("monthly_orders_count", 0) + 1
                if payment_mode.startswith("Credit"):
                    g["outstanding_balance_inr"] = round(g.get("outstanding_balance_inr", 0.0) + calc["net_payable_inr"], 2)
        self._save_garages(garages)

        return order

    def get_delivery_routes(self) -> List[Dict[str, Any]]:
        return DELIVERY_ROUTES

    def get_overview(self) -> Dict[str, Any]:
        garages = self.get_garages()
        orders = self.get_orders()

        total_wholesale_revenue = sum(o.get("net_payable_inr", 0) for o in orders)
        total_outstanding = sum(g.get("outstanding_balance_inr", 0) for g in garages)
        active_routes_count = len(DELIVERY_ROUTES)

        return {
            "partner_garages_count": len(garages),
            "total_orders_count": len(orders),
            "total_wholesale_revenue_inr": total_wholesale_revenue,
            "total_outstanding_inr": total_outstanding,
            "active_routes_count": active_routes_count,
            "garages": garages,
            "routes": DELIVERY_ROUTES,
            "recent_orders": orders[:10]
        }


# Global singleton instance
_b2b_wholesale_manager: Optional[ChamundaB2BWholesaleManager] = None


def get_b2b_wholesale_manager() -> ChamundaB2BWholesaleManager:
    global _b2b_wholesale_manager
    if _b2b_wholesale_manager is None:
        _b2b_wholesale_manager = ChamundaB2BWholesaleManager()
    return _b2b_wholesale_manager
