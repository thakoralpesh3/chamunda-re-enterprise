import os, sys
os.environ['MPLBACKEND'] = 'Agg'
try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    pass

import os, sys, json, datetime

print("🚀 [Aradhya Worker] Initializing Dealership GST Invoicing Engine...")
# Directive: generate GST invoice for service and parts

def generate_full_gst_bill():
    parts = [
        {"name": "Motul 7100 15W-50 4T (2.5L)", "hsn": "2710", "qty": 1, "unit_rate": 2250.0, "gst_rate": 0.28},
        {"name": "OEM J-Series Oil Filter Cartridge", "hsn": "8714", "qty": 1, "unit_rate": 140.0, "gst_rate": 0.28},
        {"name": "Front Disc Brake Pad Kit (Brembo/ByBre)", "hsn": "8714", "qty": 1, "unit_rate": 650.0, "gst_rate": 0.28},
        {"name": "NGK Iridium Spark Plug", "hsn": "8511", "qty": 1, "unit_rate": 750.0, "gst_rate": 0.28}
    ]
    labor_tasks = [
        {"name": "Periodic Paid Service & 30-Point Inspection", "sac": "9987", "rate": 650.0, "gst_rate": 0.18},
        {"name": "Valvetrain Tappet Clearance Calibration", "sac": "9987", "rate": 350.0, "gst_rate": 0.18},
        {"name": "Hydraulic Brake Bleeding (DOT 4)", "sac": "9987", "rate": 250.0, "gst_rate": 0.18}
    ]

    parts_taxable = sum(p["qty"] * p["unit_rate"] for p in parts)
    parts_gst = parts_taxable * 0.28
    labor_taxable = sum(l["rate"] for l in labor_tasks)
    labor_gst = labor_taxable * 0.18

    grand_total = parts_taxable + parts_gst + labor_taxable + labor_gst

    out_file = "/home/alpesh/chamunda_re_enterprise/data/missions/tax_invoice_summary.json"
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    
    invoice = {
        "dealership": "Chamunda Automobile Parts & Service",
        "founder": "Alpesh Sir (Master Automobile Engineer)",
        "helpline": "+91 78747 19139",
        "invoice_no": f"CH-INV-{int(datetime.datetime.now().timestamp())}",
        "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
        "parts_taxable": parts_taxable,
        "parts_gst_28pct": parts_gst,
        "labor_taxable": labor_taxable,
        "labor_gst_18pct": labor_gst,
        "grand_total": round(grand_total, 2)
    }

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(invoice, f, indent=2, ensure_ascii=False)

    print("=" * 60)
    print("🧾 CHAMUNDA AUTOMOBILE GST TAX INVOICE")
    print("=" * 60)
    print(f"• Parts Taxable:   ₹{parts_taxable:,.2f} | 28% GST: ₹{parts_gst:,.2f}")
    print(f"• Labor Taxable:   ₹{labor_taxable:,.2f} | 18% GST: ₹{labor_gst:,.2f}")
    print(f"• Grand Total:     ₹{grand_total:,.2f} (CGST 50% / SGST 50%)")
    print(f"✅ Invoice saved to: {out_file}")

generate_full_gst_bill()
