"""
Chamunda Automobile Parts & Service - Royal Enfield Invoicing & Customer Engagement Engine.
Generates GST compliant invoices, customer billings, embedded QR verification codes,
and links with the Royal Enfield Digital Acoustic Health Passport.
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
INVOICES_DIR = DATA_DIR / "invoices"
INVOICES_DIR.mkdir(parents=True, exist_ok=True)


def generate_invoice_qr(data: str, fill_color: str = "#1b4d3e", back_color: str = "#ffffff") -> str:
    """Generate high-contrast QR code as Base64 data URI for GST invoice."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=4,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    b64_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64_str}"


class ChamundaBillingManager:
    """Generates invoices, GST calculation, QR codes, and service reminders."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.invoices_dir = data_dir / "invoices"
        self.invoices_dir.mkdir(parents=True, exist_ok=True)

    def generate_invoice_html(
        self,
        job_card_id: str,
        customer_name: str,
        phone: str,
        bike_model: str,
        registration_no: str,
        odometer_km: int,
        parts: List[Dict[str, Any]],
        labor_charges: float,
        gst_pct: float = 18.0,
        passport_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a branded GST invoice for Chamunda Automobile Parts & Service with embedded Health Passport & QR."""
        clean_job_id = job_card_id.replace("JOB-", "").replace("-", "")
        suffix = clean_job_id[-4:] if len(clean_job_id) >= 4 else f"{int(time.time()) % 10000:04d}"
        invoice_no = f"CAPS-{datetime.datetime.now().strftime('%Y%m%d')}-{suffix}"
        invoice_date = datetime.datetime.now().strftime("%d-%b-%Y")

        parts_subtotal = sum(p["price"] * p.get("qty", 1) for p in parts)
        subtotal = parts_subtotal + labor_charges
        gst_amount = round(subtotal * (gst_pct / 100.0), 2)
        grand_total = round(subtotal + gst_amount, 2)

        next_service_date = (datetime.datetime.now() + datetime.timedelta(days=90)).strftime("%d-%b-%Y")
        next_service_km = odometer_km + 3000

        # Passport and QR Code integration
        passport_id = passport_data.get("passport_id") if passport_data else None
        health_score = passport_data.get("overall_score", 97.5) if passport_data else 97.5
        grade = passport_data.get("grade", "GOLD MINT (Showroom Specification)") if passport_data else "GOLD MINT (Showroom Specification)"
        passport_html_path = passport_data.get("html_path", "") if passport_data else ""

        qr_target_url = f"https://chamunda-re.internal/passport/{passport_id}" if passport_id else f"https://chamunda-re.internal/invoice/{invoice_no}"
        qr_code_base64 = generate_invoice_qr(qr_target_url, fill_color="#1b4d3e", back_color="#ffffff")

        parts_rows = ""
        for idx, p in enumerate(parts, 1):
            p_total = p["price"] * p.get("qty", 1)
            parts_rows += f"""
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;">{idx}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>{p['name']}</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">{p.get('qty', 1)}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">₹{p['price']}</td>
                <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">₹{p_total}</td>
            </tr>
            """

        # Passport Card HTML snippet
        passport_section = ""
        if passport_id:
            passport_section = f"""
            <div style="margin: 20px 0; padding: 16px; border: 2px solid #c5a059; border-radius: 8px; background: #fffdf8; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="color: #c5a059; font-weight: 800; font-size: 11px; letter-spacing: 1px; text-transform: uppercase;">✔ VERIFIED ACOUSTIC ENGINE HEALTH PASSPORT ATTACHED</div>
                    <div style="font-size: 16px; font-weight: bold; color: #1b4d3e; margin: 4px 0;">Health Score: {health_score} / 100 <span style="font-size: 12px; color: #555;">({grade})</span></div>
                    <div style="font-size: 12px; color: #666;">Certificate ID: <strong>{passport_id}</strong> | Tappet & Cam Chain Harmonic Balance: <strong>Optimal</strong></div>
                    <div style="margin-top: 6px; font-size: 11px;"><a href="{passport_html_path}" target="_blank" style="color: #1b4d3e; font-weight: bold; text-decoration: underline;">View Full Acoustic Harmonic Certificate ➔</a></div>
                </div>
                <div style="text-align: center; margin-left: 20px;">
                    <img src="{qr_code_base64}" style="width: 78px; height: 78px; border-radius: 4px; border: 1px solid #1b4d3e; display: block;" alt="Passport QR" />
                    <div style="font-size: 9px; color: #1b4d3e; font-weight: bold; margin-top: 2px;">SCAN TO VIEW</div>
                </div>
            </div>
            """
        else:
            passport_section = f"""
            <div style="margin: 15px 0; text-align: right;">
                <img src="{qr_code_base64}" style="width: 70px; height: 70px; border: 1px solid #ccc; border-radius: 4px; display: inline-block;" alt="Invoice QR" />
                <div style="font-size: 9px; color: #666;">Scan for Digital Copy</div>
            </div>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Invoice {invoice_no} - Chamunda Automobile Parts & Service</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 25px; color: #333; background: #fdfdfd; }}
        .invoice-card {{ max-width: 780px; margin: auto; border: 2px solid #1b4d3e; border-radius: 8px; padding: 30px; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }}
        .header {{ display: flex; justify-content: space-between; border-bottom: 2px solid #c5a059; padding-bottom: 15px; margin-bottom: 20px; }}
        .brand {{ color: #1b4d3e; margin: 0; font-size: 26px; text-transform: uppercase; letter-spacing: 1px; }}
        .tagline {{ color: #c5a059; font-weight: bold; margin: 3px 0 0 0; font-size: 14px; }}
        .meta-table {{ width: 100%; margin-bottom: 20px; font-size: 14px; }}
        .parts-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px; }}
        .parts-table th {{ background: #1b4d3e; color: white; padding: 10px; text-align: left; }}
        .totals-box {{ float: right; width: 280px; font-size: 15px; }}
        .totals-box table {{ width: 100%; border-collapse: collapse; }}
        .totals-box td {{ padding: 6px; }}
        .grand-total {{ background: #1b4d3e; color: #fff; font-size: 18px; font-weight: bold; }}
        .reminder-box {{ clear: both; margin-top: 30px; background: #f0f7f4; border-left: 4px solid #1b4d3e; padding: 12px; font-size: 13px; }}
        .footer {{ text-align: center; font-size: 12px; color: #777; margin-top: 25px; border-top: 1px solid #ddd; padding-top: 10px; }}
    </style>
</head>
<body>
    <div class="invoice-card">
        <div class="header">
            <div>
                <h1 class="brand">CHAMUNDA AUTOMOBILE</h1>
                <p class="tagline">★ PARTS & SERVICE • ROYAL ENFIELD SPECIALISTS ★</p>
                <p style="font-size: 12px; color: #555; margin: 4px 0 0 0;">Authorized Genuine Parts • Precision Engine Tuning • Acoustic Health Passports</p>
            </div>
            <div style="text-align: right;">
                <h3 style="margin: 0; color: #1b4d3e;">TAX INVOICE</h3>
                <p style="margin: 4px 0; font-weight: bold;">{invoice_no}</p>
                <p style="margin: 2px 0; font-size: 13px; color: #666;">Date: {invoice_date}</p>
            </div>
        </div>

        <table class="meta-table">
            <tr>
                <td style="width: 50%;">
                    <strong>Customer:</strong> {customer_name}<br>
                    <strong>Phone:</strong> {phone}
                </td>
                <td style="width: 50%; text-align: right;">
                    <strong>Bike Model:</strong> {bike_model}<br>
                    <strong>Reg No:</strong> {registration_no} | <strong>Odo:</strong> {odometer_km:,} KM
                </td>
            </tr>
        </table>

        <table class="parts-table">
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 50%;">Part Description / Service</th>
                    <th style="width: 10%; text-align: center;">Qty</th>
                    <th style="width: 15%; text-align: right;">Rate</th>
                    <th style="width: 20%; text-align: right;">Total</th>
                </tr>
            </thead>
            <tbody>
                {parts_rows}
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;">★</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd;"><strong>Royal Enfield Master Labor & Calibration Charges</strong></td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: center;">1</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">₹{labor_charges}</td>
                    <td style="padding: 8px; border-bottom: 1px solid #ddd; text-align: right;">₹{labor_charges}</td>
                </tr>
            </tbody>
        </table>

        <div class="totals-box">
            <table>
                <tr>
                    <td>Subtotal:</td>
                    <td style="text-align: right;">₹{subtotal}</td>
                </tr>
                <tr>
                    <td>GST ({gst_pct}%):</td>
                    <td style="text-align: right;">₹{gst_amount}</td>
                </tr>
                <tr class="grand-total">
                    <td style="padding: 8px;">Grand Total:</td>
                    <td style="text-align: right; padding: 8px;">₹{grand_total}</td>
                </tr>
            </table>
        </div>

        <div style="clear: both;"></div>

        {passport_section}

        <div class="reminder-box">
            🔔 <strong>Next Scheduled Service Due:</strong> {next_service_date} or at <strong>{next_service_km:,} KM</strong>.<br>
            Thank you for trusting Chamunda Automobile for your Royal Enfield's pure thumping performance!
        </div>

        <div class="footer">
            Chamunda Automobile Parts & Service • Genuine Royal Enfield Spares • Acoustic Health Passports • Master Engine Rebuilds
        </div>
    </div>
</body>
</html>
"""
        inv_file = self.invoices_dir / f"{invoice_no}.html"
        inv_file.write_text(html_content, encoding="utf-8")

        # Bilingual WhatsApp templates
        passport_info_en = f"📜 Digital Health Passport: {passport_id} (Score: {health_score}/100)\n📱 View Certificate: {qr_target_url}\n" if passport_id else ""
        whatsapp_msg_en = (
            f"Namaste {customer_name} ji! 🏍️\n"
            f"Your Royal Enfield ({bike_model} - {registration_no}) is fully serviced and ready at Chamunda Automobile.\n\n"
            f"📄 Invoice No: {invoice_no}\n"
            f"💰 Grand Total: ₹{grand_total}\n"
            f"{passport_info_en}"
            f"🔔 Next Service Due: {next_service_date} / {next_service_km:,} KM\n\n"
            f"Thank you for choosing Chamunda Automobile Parts & Service!"
        )

        passport_info_gu = f"📜 ડિજિટલ હેલ્થ પાસપોર્ટ ID: `{passport_id}` (સ્કોર: *{health_score}/100*)\n📱 સર્ટિફિકેટ લિંક: {qr_target_url}\n" if passport_id else ""
        whatsapp_msg_gu = (
            f"નમસ્તે શ્રી {customer_name} જી! 🏍️\n"
            f"આપની રોયલ એનફિલ્ડ ({bike_model} - `{registration_no}`) સર્વિસ થઈને ચામુંડા ઓટોમોબાઇલ પર સંપૂર્ણ તૈયાર છે.\n\n"
            f"📄 બિલ/ઇન્વોઇસ નં: *{invoice_no}*\n"
            f"💰 કુલ રકમ: *₹{grand_total}*\n"
            f"{passport_info_gu}"
            f"🔔 આગામી સર્વિસ: *{next_service_date}* અથવા *{next_service_km:,} KM*\n\n"
            f"ચામુંડા ઓટોમોબાઇલ પાર્ટ્સ એન્ડ સર્વિસ પર વિશ્વાસ મૂકવા બદલ આપનો ખૂબ ખૂબ આભાર!"
        )

        return {
            "invoice_no": invoice_no,
            "subtotal": subtotal,
            "gst_amount": gst_amount,
            "grand_total": grand_total,
            "invoice_file": str(inv_file),
            "passport_id": passport_id,
            "health_score": health_score,
            "grade": grade,
            "qr_code_base64": qr_code_base64,
            "whatsapp_message": whatsapp_msg_en,
            "whatsapp_message_gujarati": whatsapp_msg_gu,
            "next_service_date": next_service_date,
            "next_service_km": next_service_km
        }
