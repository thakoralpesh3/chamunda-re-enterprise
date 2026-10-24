#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Parts & Service • Autonomous GST Invoice Generator
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
GST Rules: Spare Parts @ 28% GST (HSN 8714), Service Labor @ 18% GST (SAC 9987).
"""
import sys
import json
import datetime

def calculate_invoice(customer_name: str, bike_model: str, parts: list, labor_charges: float):
    parts_subtotal = sum(p.get("qty", 1) * p.get("unit_price", 0.0) for p in parts)
    cgst_parts = parts_subtotal * 0.14
    sgst_parts = parts_subtotal * 0.14
    total_parts = parts_subtotal + cgst_parts + sgst_parts

    cgst_labor = labor_charges * 0.09
    sgst_labor = labor_charges * 0.09
    total_labor = labor_charges + cgst_labor + sgst_labor

    grand_total = total_parts + total_labor

    invoice = {
        "dealership": "Chamunda Automobile Parts & Service",
        "helpline": "+91 78747 19139",
        "date": datetime.datetime.now().strftime("%d-%m-%Y %I:%M %p"),
        "customer": customer_name,
        "motorcycle": bike_model,
        "parts_summary": {
            "subtotal": round(parts_subtotal, 2),
            "cgst_14pct": round(cgst_parts, 2),
            "sgst_14pct": round(sgst_parts, 2),
            "total_parts_with_gst": round(total_parts, 2)
        },
        "labor_summary": {
            "labor_base": round(labor_charges, 2),
            "cgst_9pct": round(cgst_labor, 2),
            "sgst_9pct": round(sgst_labor, 2),
            "total_labor_with_gst": round(total_labor, 2)
        },
        "grand_total": round(grand_total, 2)
    }
    return invoice

if __name__ == "__main__":
    demo_parts = [
        {"name": "Motul 7100 15W-50 2.5L", "qty": 1, "unit_price": 2250.0},
        {"name": "OEM J-Series Oil Filter", "qty": 1, "unit_price": 140.0},
        {"name": "OEM Front Brake Pads", "qty": 1, "unit_price": 550.0}
    ]
    res = calculate_invoice("Alpesh Sir VIP Fleet", "Classic 350 Reborn", demo_parts, 650.0)
    print(json.dumps(res, indent=2, ensure_ascii=False))
