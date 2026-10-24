"""
Chamunda Automobile Parts & Service - Smart Barcode Scanner & Instant Dynamic UPI QR Countertop POS Engine.
Enables rapid over-the-counter spare parts checkout, camera/barcode lookup, automatic stock deduction,
dynamic UPI QR generation (PhonePe/Google Pay/Paytm), and 80mm thermal receipt generation.
"""

import io
import json
import time
import base64
import urllib.parse
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import qrcode
from inventory_engine import ChamundaInventoryManager, DATA_DIR


POS_RECEIPTS_DIR = DATA_DIR / "pos_receipts"
POS_RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
POS_SALES_FILE = DATA_DIR / "pos_sales.json"


def generate_qr_base64(data: str, fill_color: str = "#1b4d3e", back_color: str = "#ffffff") -> str:
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


class ChamundaCounterPOS:
    """
    Smart Over-The-Counter POS Engine with barcode parsing, instant UPI QR payments,
    and automatic real-time inventory reconciliation.
    """

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.receipts_dir = data_dir / "pos_receipts"
        self.receipts_dir.mkdir(parents=True, exist_ok=True)
        self.sales_file = data_dir / "pos_sales.json"
        self.inventory_manager = ChamundaInventoryManager(data_dir=data_dir)
        self.merchant_vpa = "chamunda.re@okicici"
        self.merchant_name = "Chamunda Automobile"

    def _load_sales(self) -> List[Dict[str, Any]]:
        if self.sales_file.exists():
            try:
                return json.loads(self.sales_file.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _save_sales(self, sales: List[Dict[str, Any]]) -> None:
        self.sales_file.write_text(json.dumps(sales, indent=2, ensure_ascii=False), encoding="utf-8")

    def scan_or_lookup_part(self, code_or_query: str) -> Optional[Dict[str, Any]]:
        """
        Lookup part by Barcode, Part Number, OEM Number, Part ID, or Name.
        Matches exact identifiers first, then falls back to prefix/substring.
        """
        query = str(code_or_query).strip()
        if not query:
            return None

        all_parts = self.inventory_manager.get_all_parts()
        query_upper = query.upper()
        query_lower = query.lower()

        # 1. Exact match on part_id, part_number, oem_number
        for p in all_parts:
            p_id = str(p.get("part_id", "")).upper()
            p_no = str(p.get("part_number", "")).upper()
            oem = str(p.get("oem_number", "")).upper()
            if query_upper in (p_id, p_no, oem):
                return p

        # 2. Case-insensitive exact match or substring in part number / OEM
        for p in all_parts:
            p_no = str(p.get("part_number", "")).upper()
            oem = str(p.get("oem_number", "")).upper()
            if query_upper in p_no or query_upper in oem:
                return p

        # 3. Name or model match
        for p in all_parts:
            name = str(p.get("name", "")).lower()
            if query_lower in name:
                return p

        return None

    def search_counter_parts(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search parts for POS interface auto-complete dropdown."""
        query = str(query).strip().lower()
        if not query:
            return self.inventory_manager.get_all_parts()[:limit]

        results = []
        for p in self.inventory_manager.get_all_parts():
            p_id = str(p.get("part_id", "")).lower()
            p_no = str(p.get("part_number", "")).lower()
            name = str(p.get("name", "")).lower()
            models = " ".join(p.get("models", [])).lower()
            if query in p_id or query in p_no or query in name or query in models:
                results.append(p)
                if len(results) >= limit:
                    break
        return results

    def generate_upi_payment_link(self, amount: float, receipt_no: str) -> Dict[str, str]:
        """
        Generates standard NPCI UPI Intent URI and QR code image for Google Pay, PhonePe, Paytm.
        """
        am_str = f"{amount:.2f}"
        encoded_pn = urllib.parse.quote_plus(self.merchant_name)
        encoded_tn = urllib.parse.quote_plus(f"Payment for {receipt_no}")

        upi_uri = f"upi://pay?pa={self.merchant_vpa}&pn={encoded_pn}&am={am_str}&cu=INR&tn={encoded_tn}"
        qr_b64 = generate_qr_base64(upi_uri, fill_color="#0a4d2e", back_color="#ffffff")

        return {
            "upi_uri": upi_uri,
            "qr_code_base64": qr_b64,
            "merchant_vpa": self.merchant_vpa,
            "merchant_name": self.merchant_name,
            "amount": amount
        }

    def create_counter_sale(
        self,
        cart_items: List[Dict[str, Any]],
        customer_name: str = "Counter Walk-in Customer",
        phone: str = "",
        payment_mode: str = "UPI",
        discount_amount: float = 0.0,
        notes: str = ""
    ) -> Dict[str, Any]:
        """
        Execute POS counter sale:
        1. Resolve each part and deduct stock.
        2. Calculate subtotal, GST breakdown, discount, and final amount.
        3. Generate dynamic UPI QR Code.
        4. Produce printable 80mm thermal receipt HTML.
        5. Persist sale to pos_sales.json.
        """
        if not cart_items:
            raise ValueError("Cart is empty. Please add parts before checkout.")

        now = datetime.datetime.now()
        receipt_suffix = f"{int(time.time()) % 10000:04d}"
        receipt_no = f"POS-{now.strftime('%Y%m%d')}-{receipt_suffix}"
        sale_date_str = now.strftime("%d-%b-%Y %I:%M %p")

        resolved_items = []
        subtotal = 0.0

        for item in cart_items:
            code = item.get("part_id") or item.get("part_number") or item.get("query")
            qty = max(1, int(item.get("qty", 1)))
            part = self.scan_or_lookup_part(str(code))

            if part:
                unit_price = float(item.get("price") or part.get("mrp", 0))
                line_total = unit_price * qty
                subtotal += line_total

                # Deduct stock immediately
                p_id = part.get("part_id")
                updated_part = self.inventory_manager.update_stock(p_id, -qty)
                current_remaining = updated_part.get("stock", 0) if updated_part else max(0, part.get("stock", 0) - qty)

                resolved_items.append({
                    "part_id": p_id,
                    "name": part.get("name", "Unknown Part"),
                    "part_number": part.get("part_number", ""),
                    "category": part.get("category", ""),
                    "unit_price": unit_price,
                    "qty": qty,
                    "line_total": line_total,
                    "remaining_stock": current_remaining
                })
            else:
                # Custom ad-hoc item or unlisted part
                name = item.get("name", f"Item ({code})")
                unit_price = float(item.get("price", 0.0))
                line_total = unit_price * qty
                subtotal += line_total
                resolved_items.append({
                    "part_id": str(code),
                    "name": name,
                    "part_number": str(code),
                    "category": "Over-The-Counter Custom",
                    "unit_price": unit_price,
                    "qty": qty,
                    "line_total": line_total,
                    "remaining_stock": None
                })

        discount = max(0.0, float(discount_amount))
        net_amount = max(0.0, subtotal - discount)
        # Assuming MRP includes GST 18% or standard Indian retail pricing
        gst_included = round(net_amount * 18 / 118, 2)

        # Dynamic UPI QR
        upi_data = self.generate_upi_payment_link(amount=net_amount, receipt_no=receipt_no)

        # Generate 80mm Thermal Receipt HTML
        items_rows_html = ""
        for itm in resolved_items:
            items_rows_html += f"""
            <tr>
                <td style="padding: 4px 0; font-weight: 600;">{itm['name']}<br><span style="font-size: 10px; color: #555;">P/N: {itm['part_number']}</span></td>
                <td style="text-align: center; vertical-align: top; padding: 4px 0;">{itm['qty']}</td>
                <td style="text-align: right; vertical-align: top; padding: 4px 0;">₹{itm['unit_price']:.2f}</td>
                <td style="text-align: right; vertical-align: top; padding: 4px 0; font-weight: 600;">₹{itm['line_total']:.2f}</td>
            </tr>
            """

        receipt_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Thermal Receipt - {receipt_no}</title>
    <style>
        @page {{ size: 80mm auto; margin: 0; }}
        body {{
            font-family: 'Courier New', Courier, monospace;
            width: 76mm;
            margin: auto;
            padding: 8px;
            color: #000;
            background: #fff;
            font-size: 12px;
            line-height: 1.25;
        }}
        .center {{ text-align: center; }}
        .bold {{ font-weight: bold; }}
        .hr {{ border-top: 1px dashed #000; margin: 6px 0; }}
        .header {{ margin-bottom: 6px; }}
        .title {{ font-size: 15px; font-weight: bold; letter-spacing: 0.5px; }}
        .subtitle {{ font-size: 10px; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
        .totals td {{ padding: 2px 0; }}
        .qr-section {{ text-align: center; margin: 8px 0; }}
        .qr-img {{ width: 140px; height: 140px; margin: 4px auto; display: block; }}
        .footer {{ font-size: 10px; text-align: center; margin-top: 8px; }}
        @media print {{
            .no-print {{ display: none !important; }}
            body {{ width: 100%; padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="header center">
        <div class="title">CHAMUNDA AUTOMOBILE</div>
        <div class="subtitle">PARTS & SERVICE • ROYAL ENFIELD SPECIALISTS</div>
        <div class="subtitle">NH-48, Gujarat | Mo: +91 98250 XXXXX</div>
        <div class="subtitle">GSTIN: 24AAAPC1234F1Z5</div>
    </div>
    
    <div class="hr"></div>
    <div>
        <div><strong>RECEIPT NO:</strong> {receipt_no}</div>
        <div><strong>DATE:</strong> {sale_date_str}</div>
        <div><strong>CUSTOMER:</strong> {customer_name}</div>
        {f'<div><strong>PHONE:</strong> {phone}</div>' if phone else ''}
        <div><strong>PAY MODE:</strong> {payment_mode}</div>
    </div>
    <div class="hr"></div>

    <table>
        <thead>
            <tr style="border-bottom: 1px solid #000;">
                <th style="text-align: left; padding-bottom: 4px;">Item / P/N</th>
                <th style="text-align: center; padding-bottom: 4px;">Qty</th>
                <th style="text-align: right; padding-bottom: 4px;">Rate</th>
                <th style="text-align: right; padding-bottom: 4px;">Amt</th>
            </tr>
        </thead>
        <tbody>
            {items_rows_html}
        </tbody>
    </table>

    <div class="hr"></div>
    <table class="totals">
        <tr>
            <td>Items Total:</td>
            <td style="text-align: right;">₹{subtotal:.2f}</td>
        </tr>
        {f'<tr><td>Discount:</td><td style="text-align: right;">-₹{discount:.2f}</td></tr>' if discount > 0 else ''}
        <tr style="font-size: 14px; font-weight: bold; border-top: 1px dashed #000; border-bottom: 1px dashed #000;">
            <td style="padding: 4px 0;">NET PAYABLE:</td>
            <td style="text-align: right; padding: 4px 0;">₹{net_amount:.2f}</td>
        </tr>
        <tr style="font-size: 9px; color: #444;">
            <td>(Incl. GST @ 18%):</td>
            <td style="text-align: right;">₹{gst_included:.2f}</td>
        </tr>
    </table>

    <div class="qr-section">
        <div class="bold" style="font-size: 11px;">SCAN TO PAY VIA UPI</div>
        <img src="{upi_data['qr_code_base64']}" class="qr-img" alt="UPI QR">
        <div style="font-size: 9px;">UPI ID: {self.merchant_vpa}</div>
        <div style="font-size: 9px; color: #555;">GPay • PhonePe • Paytm • BHIM</div>
    </div>

    <div class="hr"></div>
    <div class="footer">
        <div>★ 100% Genuine Royal Enfield Spares ★</div>
        <div>Goods once sold can be exchanged within 7 days in original packaging.</div>
        <div style="margin-top: 4px; font-weight: bold;">THANK YOU! RIDE SAFE! 🏍️</div>
    </div>

    <div class="no-print" style="margin-top: 20px; text-align: center;">
        <button onclick="window.print()" style="padding: 8px 16px; background: #0a4d2e; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">
            🖨️ Print 80mm POS Thermal Slip
        </button>
    </div>
</body>
</html>
"""
        receipt_file = self.receipts_dir / f"{receipt_no}.html"
        receipt_file.write_text(receipt_html, encoding="utf-8")

        # Bilingual WhatsApp copy
        items_summary_en = "\n".join([f"• {itm['name']} (x{itm['qty']}) - ₹{itm['line_total']:.2f}" for itm in resolved_items])
        whatsapp_en = (
            f"Namaste {customer_name}! 🏍️\n"
            f"Thank you for shopping genuine Royal Enfield spares at Chamunda Automobile Parts & Service.\n\n"
            f"🧾 POS Receipt: {receipt_no}\n"
            f"📦 Items Purchased:\n{items_summary_en}\n"
            f"💰 Total Paid: ₹{net_amount:.2f} ({payment_mode})\n\n"
            f"Keep your ride pure and thumping! Safe riding! 🏍️💨"
        )

        items_summary_gu = "\n".join([f"• {itm['name']} (જથ્થો: {itm['qty']}) - ₹{itm['line_total']:.2f}" for itm in resolved_items])
        whatsapp_gu = (
            f"નમસ્તે શ્રી {customer_name}! 🏍️\n"
            f"ચામુંડા ઓટોમોબાઇલ પાર્ટ્સ એન્ડ સર્વિસમાંથી રોયલ એનફિલ્ડ જેન્યુઇન પાર્ટ્સ ખરીદવા બદલ આભાર.\n\n"
            f"🧾 POS રસીદ નં: *{receipt_no}*\n"
            f"📦 ખરીદેલ પાર્ટ્સ:\n{items_summary_gu}\n"
            f"💰 કુલ ચૂકવેલ રકમ: *₹{net_amount:.2f}* ({payment_mode})\n\n"
            f"આપની સવારી રોયલ એનફિલ્ડ સાથે સલામત અને આનંદદાયક રહે! 🏍️💨"
        )

        sale_record = {
            "receipt_no": receipt_no,
            "timestamp": now.isoformat(),
            "customer_name": customer_name,
            "phone": phone,
            "payment_mode": payment_mode,
            "items_count": len(resolved_items),
            "subtotal": subtotal,
            "discount": discount,
            "net_amount": net_amount,
            "gst_included": gst_included,
            "items": resolved_items,
            "notes": notes,
            "receipt_file": str(receipt_file),
            "upi_uri": upi_data["upi_uri"],
            "qr_code_base64": upi_data["qr_code_base64"],
            "whatsapp_message_en": whatsapp_en,
            "whatsapp_message_gu": whatsapp_gu
        }

        sales = self._load_sales()
        sales.insert(0, sale_record)
        self._save_sales(sales)

        return sale_record

    def get_sales_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return recent POS counter transactions."""
        return self._load_sales()[:limit]

    def get_receipt(self, receipt_no: str) -> Optional[Dict[str, Any]]:
        """Find a sale by receipt number."""
        for s in self._load_sales():
            if s.get("receipt_no") == receipt_no:
                return s
        return None
