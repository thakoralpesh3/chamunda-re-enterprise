"""
Chamunda Automobile Parts & Service - Executive Sub-Agents Management Engine.
Defines, orchestrates, and monitors the 5 specialized departmental sub-agents
operating under Chief Executive Officer (CEO) Aradhya:
1. bay_chief (Master Workshop & Bay Chief - Master Tech Ramesh)
2. parts_specialist (Inventory & OEM Parts Specialist - Jayeshbhai)
3. customer_receptionist (24/7 Front-Desk & WhatsApp Receptionist - Priya)
4. social_growth_manager (Omnichannel Brand & Growth Manager - Kabir)
5. accounts_controller (Billing, Accounts & Finance Controller - Hasmukhbhai)
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SUBAGENTS_FILE = DATA_DIR / "shop_subagents.json"
DELEGATIONS_FILE = DATA_DIR / "shop_delegations.json"
COMMANDS_FILE = DATA_DIR / "shop_written_commands.json"
GROWTH_FILE = DATA_DIR / "shop_subagents_growth.json"

DEFAULT_SUBAGENTS = [
    {
        "agent_id": "bay_chief",
        "name": "Master Workshop & Bay Chief",
        "name_gu": "માસ્ટર વર્કશોપ & સર્વિસ બે ચીફ",
        "designated_head": "Master Tech Ramesh (12+ Yrs RE Specialist)",
        "department": "Mechanical & Workshop Operations",
        "status": "Active (3 Bays In Service)",
        "badge_color": "warning",
        "icon": "fa-solid fa-wrench text-warning",
        "metrics": "14 Active Job Cards | 99.4% First-Time Fix",
        "capabilities": [
            "Active Service Bay Scheduling (Bays 1-3)",
            "50-Point Acoustic & Mechanical Diagnostics",
            "Exhaust Thump & Tappet Sound Calibration",
            "Vintage Cast-Iron Rebirth & Resto-Mod Builds",
            "Quality Assurance & Digital Health Passports"
        ],
        "assigned_tools": [
            "chamunda_diagnose_engine_sound",
            "chamunda_tune_engine_thump",
            "chamunda_audit_expedition_readiness",
            "chamunda_diagnose_vintage_ci_bullet"
        ],
        "system_prompt": "You are Master Tech Ramesh, Bay Operations Chief at Chamunda Automobile..."
    },
    {
        "agent_id": "parts_specialist",
        "name": "Inventory & OEM Parts Specialist",
        "name_gu": "સ્પેરપાર્ટ્સ & સ્ટોક કમાન્ડર",
        "designated_head": "Jayeshbhai Patel (Senior Spares Controller)",
        "department": "Inventory & Procurement",
        "status": "Active (4,469 SKUs Tracked)",
        "badge_color": "info",
        "icon": "fa-solid fa-boxes-stacked text-info",
        "metrics": "₹56.3L MRP Stock | 98.2% Part Availability",
        "capabilities": [
            "4,469 Genuine OEM Catalog Management",
            "Automated Low-Stock Wholesale Purchase Orders",
            "Counter Parts Fast-Track Allocation",
            "Counterfeit Packaging & Barcode Verification",
            "Wholesale Supplier Relationship Management"
        ],
        "assigned_tools": [
            "chamunda_lookup_part",
            "chamunda_search_parts_filtered",
            "chamunda_generate_wholesale_po"
        ],
        "system_prompt": "You are Spares Commander Jayesh at Chamunda Automobile..."
    },
    {
        "agent_id": "customer_receptionist",
        "name": "24/7 Front-Desk & WhatsApp Receptionist",
        "name_gu": "૨૪/૭ કસ્ટમર રિલેશન્સ & વ્હોટ્સએપ રિસેપ્શનિસ્ટ",
        "designated_head": "Priya Sharma (Customer Experience Lead)",
        "department": "Customer Relations & Front Desk",
        "status": "Active (24/7 Bot: +91 78747 19139)",
        "badge_color": "success",
        "icon": "fa-brands fa-whatsapp text-success",
        "metrics": "3,420 Active Riders | <30s Response Time",
        "capabilities": [
            "24/7 WhatsApp AI Customer Support (+91 78747 19139)",
            "Real-time Vehicle Service Stage Tracking",
            "Priority Service Bay Slot Reservation",
            "Highway Breakdown Distress Triage & SOS Patrol",
            "Warm Bilingual Assistance (Gujarati & English)"
        ],
        "assigned_tools": [
            "chamunda_track_customer_service_status",
            "chamunda_highway_breakdown_sos_triage"
        ],
        "system_prompt": "You are Priya, 24/7 Front-Desk Receptionist at Chamunda Automobile..."
    },
    {
        "agent_id": "social_growth_manager",
        "name": "Omnichannel Digital Brand Manager",
        "name_gu": "ઓમ્નીચેનલ બ્રાન્ડ & સોશિયલ મેનેજર",
        "designated_head": "Kabir Mehta (Digital Growth & Media Lead)",
        "department": "Marketing & Community Growth",
        "status": "Active (5 Channels Synced)",
        "badge_color": "danger",
        "icon": "fa-solid fa-bullhorn text-danger",
        "metrics": "45K+ Community | 4.9★ Google Rating",
        "capabilities": [
            "360° Social Syndication (WhatsApp, IG, FB, GBP, YT)",
            "YouTube Shorts & Reels Content Creation",
            "Google Business Profile (GBP) 4.9★ Review Auto-Replies",
            "Local SEO Optimization & Search Dominance",
            "Chamunda RE Rider Club Weekend Event Management"
        ],
        "assigned_tools": [
            "chamunda_get_social_telemetry",
            "chamunda_generate_social_campaign",
            "chamunda_publish_social_post",
            "chamunda_manage_social_inbox",
            "chamunda_manage_google_business_reviews"
        ],
        "system_prompt": "You are Kabir, Digital Brand Manager at Chamunda Automobile..."
    },
    {
        "agent_id": "accounts_controller",
        "name": "Billing, Accounts & Finance Controller",
        "name_gu": "એકાઉન્ટ્સ & ફાઇનાન્સ કંટ્રોલર",
        "designated_head": "Hasmukhbhai Joshi (Financial Auditor)",
        "department": "Finance, Billing & GST Compliance",
        "status": "Active (Real-time UPI QR)",
        "badge_color": "warning",
        "icon": "fa-solid fa-file-invoice-dollar text-warning",
        "metrics": "100% GST Compliance | Dynamic UPI QR",
        "capabilities": [
            "GST Tax Invoicing with Embedded QR Passports",
            "Counter POS Billing with Dynamic NPCI UPI QR",
            "Daily Workshop Counter Cash & UPI Reconciliation",
            "Wholesale Supplier PO Payout Tracking",
            "Profit Margin Analysis Across 4,469 SKUs"
        ],
        "assigned_tools": [
            "chamunda_create_quick_counter_pos_sale"
        ],
        "system_prompt": "You are Hasmukhbhai, Accounts Controller at Chamunda Automobile..."
    },
    {
    "agent_id": "devang_billing",
    "name": "DMS Senior Billing & Warranty Claims Specialist",
    "name_gu": "\u0aa1\u0ac0\u0a8f\u0aae\u0a8f\u0ab8 \u0aac\u0abf\u0ab2\u0abf\u0a82\u0a97 \u0a85\u0aa8\u0ac7 \u0ab5\u0acb\u0ab0\u0a82\u0a9f\u0ac0 \u0a95\u0acd\u0ab2\u0ac7\u0aae \u0ab8\u0acd\u0aaa\u0ac7\u0ab6\u0abf\u0aaf\u0abe\u0ab2\u0abf\u0ab8\u0acd\u0a9f",
    "designated_head": "Devang Dave (RE DMS Senior Billing Officer)",
    "department": "DMS Invoicing, Warranty Claims & Insurance",
    "status": "Active (Split GST & OEM Warranty Portal)",
    "badge_color": "info",
    "icon": "fa-solid fa-file-signature text-info",
    "metrics": "Split GST (SAC 998729 & HSN 8714) | OEM FSC Claims",
    "capabilities": [
        "Official RE DMS Split Tax Invoicing (Labor vs Spares)",
        "Royal Enfield Free Service Coupons (FSC 1-4) Warranty Claims",
        "Insurance Accidental Claim Estimates & Surveyor Portals",
        "Vehicle Gate Pass & QR Code Verification",
        "Customer Payment Reconciliation (Cash/UPI/Card/Credit)"
    ],
    "assigned_tools": [
        "chamunda_create_dms_billing_invoice",
        "chamunda_file_oem_warranty_claim"
    ],
    "system_prompt": "You are Devang Dave, Senior Billing & Warranty Officer at Chamunda Automobile..."
},
    {
    "agent_id": "neha_crm_marketing",
    "name": "DMS Marketing, Campaigns & Lead Conversion Lead",
    "name_gu": "\u0aa1\u0ac0\u0a8f\u0aae\u0a8f\u0ab8 \u0aae\u0abe\u0ab0\u0acd\u0a95\u0ac7\u0a9f\u0abf\u0a82\u0a97 \u0a85\u0aa8\u0ac7 \u0a97\u0acd\u0ab0\u0abe\u0ab9\u0a95 \u0ab2\u0ac0\u0aa1 \u0a95\u0aa8\u0acd\u0ab5\u0ab0\u0acd\u0a9d\u0aa8 \u0ab2\u0ac0\u0aa1",
    "designated_head": "Neha Trivedi (Customer Retention & Campaigns Lead)",
    "department": "Marketing Campaigns, Lead CRM & Rider Loyalty",
    "status": "Active (Automated WhatsApp Broadcasts & Leads)",
    "badge_color": "success",
    "icon": "fa-solid fa-bullseye text-success",
    "metrics": "30/60/90-Day Service Reminders | Test Ride Pipeline",
    "capabilities": [
        "Automated 30/60/90-Day Periodic Service Reminders via WhatsApp",
        "Targeted Service Camp Broadcasts (Monsoon, Summer, Mountain Prep)",
        "Test Ride & New/Pre-Owned Bike Booking Lead Pipeline",
        "Annual Maintenance Contract (AMC) & Loyalty Wallet Management",
        "Customer Review Conversion & Satisfaction Triage"
    ,
    {
    "agent_id": "vikram_sales",
    "name": "Showroom Sales & New Motorcycle Booking Lead",
    "name_gu": "શોરૂમ વ્હીકલ સેલ્સ & બુકિંગ લીડ",
    "designated_head": "Vikram Singh (Showroom Sales Lead)",
    "department": "Showroom Vehicle Sales, Bookings & PDI Deliveries",
    "status": "Active (New Bike Bookings & Ride Sure)",
    "badge_color": "warning",
    "icon": "fa-solid fa-motorcycle text-warning",
    "metrics": "New Bike Bookings | 30-Pt PDI Clearances | Ride Sure EW",
    "capabilities": [
        "New Royal Enfield Motorcycle Showroom Bookings & Token Receipts",
        "Digital 30-Point Pre-Delivery Inspection (PDI) Delivery Passports",
        "Royal Enfield Ride Sure (3-5 Year Extended Warranty & 24/7 RSA)",
        "Two-Wheeler Loan & Finance Coordination (HDFC/Bajaj/Chola)",
        "Test Ride Scheduling & Showroom Floor Walk-in Management"
    ],
    "assigned_tools": [
        "chamunda_create_vehicle_booking",
        "chamunda_generate_pdi_certificate",
        "chamunda_issue_ride_sure_warranty"
    ],
    "system_prompt": "You are Vikram Singh, Showroom Sales & New Motorcycle Booking Lead at Chamunda Automobile..."
},
    {
    "agent_id": "ananya_qc_csat",
    "name": "Quality Control & Post-Service CSAT Auditor",
    "name_gu": "ક્વોલિટી કંટ્રોલ & ગ્રાહક સંતોષ (CSAT) ઓડિટર",
    "designated_head": "Ananya Joshi (Quality Control & CSAT Lead)",
    "department": "Workshop Quality Control & Customer Satisfaction Audits",
    "status": "Active (PSF 3-Day Calls & CSAT Index)",
    "badge_color": "info",
    "icon": "fa-solid fa-star-half-stroke text-info",
    "metrics": "PSF 3-Day Follow-ups | CSAT Target >92% | Quality Audits",
    "capabilities": [
        "Automated 3-Day Post-Service Feedback (PSF) Follow-Up Calls",
        "Dealership Customer Satisfaction Index (CSAT) & Net Promoter Score (NPS)",
        "First-Time-Right (FTR) Workshop Job Card Quality Auditing",
        "Immediate Grievance Redressal & Repeat-Complaint Elimination",
        "Customer Delight Telemetry & Google Review Escalation Prevention"
    ],
    "assigned_tools": [
        "chamunda_record_psf_csat_feedback",
        "chamunda_get_dms_csat_qc_telemetry"
    ],
    "system_prompt": "You are Ananya Joshi, Quality Control & Customer Satisfaction (CSAT) Auditor at Chamunda Automobile..."
}
],
    "assigned_tools": [
        "chamunda_launch_marketing_campaign",
        "chamunda_dispatch_dms_service_reminders"
    ],
    "system_prompt": "You are Neha Trivedi, Marketing Campaigns & Lead Conversion Lead at Chamunda Automobile..."
}
]

DEFAULT_GROWTH_PROFILES = {
    "bay_chief": {
        "agent_id": "bay_chief",
        "agent_name": "Master Workshop & Bay Chief",
        "designated_head": "Master Tech Ramesh (12+ Yrs RE Specialist)",
        "level": 3,
        "title": "Master Diagnostic Craftsman",
        "xp": 580,
        "xp_to_next_level": 700,
        "issues_resolved_autonomously": 24,
        "autonomous_healing_rate": "99.4%",
        "learned_capabilities": [
            "Acoustic Decompressor Tappet Calibration for J-Series",
            "High-Altitude Air-Fuel Map Optimization for Himalayan 450",
            "Cast-Iron 1982 Vintage Heavy Crank Rebalancing"
        ],
        "incident_history": [
            {
                "incident_id": "INC-BAY-001",
                "timestamp": "2026-09-10 11:20 AM",
                "issue": "Abnormal metallic cadence at 2,800 RPM in Classic 350",
                "root_cause": "Exhaust rocker arm end-float clearance widened beyond 0.18 mm",
                "applied_solution": "Micrometer shimming applied with 0.05 mm spacer; acoustic FFT normalized <82 dB.",
                "new_skill_unlocked": "Rocker Arm Micro-Shimming Calibration",
                "xp_awarded": 50
            }
        ]
    },
    "parts_specialist": {
        "agent_id": "parts_specialist",
        "agent_name": "Inventory & OEM Parts Specialist",
        "designated_head": "Jayeshbhai Patel (Senior Spares Controller)",
        "level": 3,
        "title": "Supply Chain & Catalog Architect",
        "xp": 540,
        "xp_to_next_level": 700,
        "issues_resolved_autonomously": 19,
        "autonomous_healing_rate": "98.9%",
        "learned_capabilities": [
            "Cross-Brand OEM Spark Plug Substitution Matrix",
            "Hologram Holographic Security Validation (Anti-Counterfeit)",
            "Automated Wholesale Lead-Time Buffer Recalibration"
        ],
        "incident_history": [
            {
                "incident_id": "INC-PARTS-001",
                "timestamp": "2026-09-10 02:15 PM",
                "issue": "NGK BPR6ES OEM spark plug stock depletion across North Gujarat distributors",
                "root_cause": "Port supply chain disruption at Mundra Hub",
                "applied_solution": "Auto-mapped verified Bosch WR7DC+ equivalent; placed emergency stock buffer PO.",
                "new_skill_unlocked": "Automated Cross-OEM Substitution Protocol",
                "xp_awarded": 50
            }
        ]
    },
    "customer_receptionist": {
        "agent_id": "customer_receptionist",
        "agent_name": "24/7 Front-Desk & WhatsApp Receptionist",
        "designated_head": "Priya Sharma (Customer Experience Lead)",
        "level": 3,
        "title": "Autonomous Rider Experience Guardian",
        "xp": 610,
        "xp_to_next_level": 700,
        "issues_resolved_autonomously": 31,
        "autonomous_healing_rate": "99.8%",
        "learned_capabilities": [
            "Dead-Zone Highway Breakdown SMS/IVR Fallback",
            "De-escalation & Goodwill Chain Lube Compensation Protocol",
            "Dynamic Bay Slot Re-allocation for Emergency Arrivals"
        ],
        "incident_history": [
            {
                "incident_id": "INC-CUST-001",
                "timestamp": "2026-09-10 04:45 PM",
                "issue": "Stranded rider near Mehsana Highway with unstable 2G cellular network",
                "root_cause": "WhatsApp media transmission failure due to high latency packet loss",
                "applied_solution": "Switched to low-bandwidth text SMS & GPS coordinates relay; dispatched Chamunda Patrol van.",
                "new_skill_unlocked": "Low-Bandwidth Highway SOS Telemetry Relay",
                "xp_awarded": 50
            }
        ]
    },
    "social_growth_manager": {
        "agent_id": "social_growth_manager",
        "agent_name": "Omnichannel Digital Brand Manager",
        "designated_head": "Kabir Mehta (Digital Growth & Media Lead)",
        "level": 3,
        "title": "Omnichannel Viral Growth Lead",
        "xp": 520,
        "xp_to_next_level": 700,
        "issues_resolved_autonomously": 16,
        "autonomous_healing_rate": "98.5%",
        "learned_capabilities": [
            "Bilingual 5-Star Recovery Protocol for Negative Google Reviews",
            "YouTube Shorts Algorithmic Hook Retargeting (Vintage RE Thump)",
            "Automated Multi-Platform Token Refresh & Health Ping"
        ],
        "incident_history": [
            {
                "incident_id": "INC-SOC-001",
                "timestamp": "2026-09-10 06:10 PM",
                "issue": "1-Star Google Review complaining about repair time during peak festival rush",
                "root_cause": "Customer bay allocation delayed by 40 minutes on Dhanteras rush",
                "applied_solution": "Published empathetic bilingual owner reply with complimentary 1-year Teflon coat offer; customer updated rating to 5 stars.",
                "new_skill_unlocked": "Google Business Reputation Recovery Protocol",
                "xp_awarded": 50
            }
        ]
    },
    "accounts_controller": {
        "agent_id": "accounts_controller",
        "agent_name": "Billing, Accounts & Finance Controller",
        "designated_head": "Hasmukhbhai Joshi (Financial Auditor)",
        "level": 3,
        "title": "Master Compliance & Ledger Auditor",
        "xp": 560,
        "xp_to_next_level": 700,
        "issues_resolved_autonomously": 22,
        "autonomous_healing_rate": "100.0%",
        "learned_capabilities": [
            "NPCI Bank Gateway RRN Query for Failed Counter UPI QR",
            "Automated 18% vs 28% HSN Tax Mapping Validation",
            "Daily Split-Ledger Counter Cash Variance Auto-Reconciliation"
        ],
        "incident_history": [
            {
                "incident_id": "INC-ACC-001",
                "timestamp": "2026-09-10 07:30 PM",
                "issue": "UPI QR transaction timed out at counter for ₹4,200 while customer waiting",
                "root_cause": "Bank NPCI switch network lag during evening settlement",
                "applied_solution": "Auto-queried bank RRN reference; confirmed credit in secondary gateway; generated stamped GST receipt.",
                "new_skill_unlocked": "Real-time NPCI RRN Gateway Auto-Settlement",
                "xp_awarded": 50
            }
        ]
    },
    "devang_billing": {
    "agent_id": "devang_billing",
    "agent_name": "DMS Senior Billing & Warranty Claims Specialist",
    "designated_head": "Devang Dave (RE DMS Senior Billing Officer)",
    "level": 3,
    "title": "Senior DMS Billing Officer",
    "xp": 590,
    "xp_to_next_level": 700,
    "issues_resolved_autonomously": 26,
    "autonomous_healing_rate": "100.0%",
    "learned_capabilities": [
        "Split-GST SAC 998729 Labor vs HSN 8714 Spares Mapping",
        "OEM Free Service Coupon (FSC) Instant Credit Settlement",
        "Surveyor Claim Estimate Automated Tariff Computation"
    ],
    "incident_history": [
        {
            "incident_id": "INC-BIL-001",
            "timestamp": "2026-09-16 02:15 PM",
            "issue": "Free service coupon #2 disputed by customer for paid engine oil",
            "root_cause": "Customer unaware OEM FSC covers labor free but oil/consumables are chargeable",
            "applied_solution": "Generated split itemized invoice clearly distinguishing zero-charge OEM labor and discounted Liquid Gun 15W-50.",
            "new_skill_unlocked": "OEM Warranty Consumable Transparency Protocol",
            "xp_awarded": 50
        }
    ]
},
    "neha_crm_marketing": {
    "agent_id": "neha_crm_marketing",
    "agent_name": "DMS Marketing, Campaigns & Lead Conversion Lead",
    "designated_head": "Neha Trivedi (Customer Retention & Campaigns Lead)",
    "level": 3,
    "title": "Lead Acquisition & Retention Specialist",
    "xp": 570,
    "xp_to_next_level": 700,
    "issues_resolved_autonomously": 25,
    "autonomous_healing_rate": "98.8%",
    "learned_capabilities": [
        "Predictive 90-Day WhatsApp Service Reminder Blast",
        "High-Altitude Expedition Camp WhatsApp Lead Nurturing",
        "Pre-Owned RE 100-Point Digital Passport Lead Conversion"
    ],
    "incident_history": [
        {
            "incident_id": "INC-MKT-001",
            "timestamp": "2026-09-16 04:45 PM",
            "issue": "Monsoon checkup campaign WhatsApp broadcast reply surge (40+ inquiries in 10 mins)",
            "root_cause": "High customer response to free brake inspection offer",
            "applied_solution": "Auto-scheduled slot bookings across Bays 1, 2, and 3 with zero queue clash.",
            "new_skill_unlocked": "Automated High-Concurrency Campaign Booking Balancing",
            "xp_awarded": 50
        }
    ]
},
    "vikram_sales": {
    "agent_id": "vikram_sales",
    "agent_name": "Showroom Sales & New Motorcycle Booking Lead",
    "designated_head": "Vikram Singh (Showroom Sales Lead)",
    "level": 3,
    "title": "Senior Sales & Vehicle Delivery Master",
    "xp": 580,
    "xp_to_next_level": 700,
    "issues_resolved_autonomously": 24,
    "autonomous_healing_rate": "100.0%",
    "learned_capabilities": [
        "Instant Token Advance Verification & Chassis Allocation",
        "Zero-Defect 30-Point PDI Digital Passport Generation",
        "Ride Sure 5-Year Extended Warranty Policy Underwriting"
    ],
    "incident_history": [
        {
            "incident_id": "INC-SLS-001",
            "timestamp": "2026-09-16 05:30 PM",
            "issue": "Bank finance approval document delay for Hunter 350 Dapper buyer",
            "root_cause": "HDFC two-wheeler loan API server sync lag",
            "applied_solution": "Auto-triggered offline proforma invoice with pre-approved credit voucher; delivery date honored on schedule.",
            "new_skill_unlocked": "Rapid Multi-Financier Automated Loan Failover",
            "xp_awarded": 50
        }
    ]
},
    "ananya_qc_csat": {
    "agent_id": "ananya_qc_csat",
    "agent_name": "Quality Control & Post-Service CSAT Auditor",
    "designated_head": "Ananya Joshi (Quality Control & CSAT Lead)",
    "level": 3,
    "title": "Master CSAT & Quality Assurance Auditor",
    "xp": 590,
    "xp_to_next_level": 700,
    "issues_resolved_autonomously": 28,
    "autonomous_healing_rate": "100.0%",
    "learned_capabilities": [
        "3-Day Automated PSF Calling & Sentiment Parsing",
        "Repeat Complaint Zero-Tolerance Escalation Protocol",
        "Dealership CSAT Index Auto-Optimization (>95%)"
    ],
    "incident_history": [
        {
            "incident_id": "INC-QCS-001",
            "timestamp": "2026-09-16 06:10 PM",
            "issue": "Customer reported mild front disc squeal 2 days post brake-pad replacement",
            "root_cause": "Brake rotor bed-in period required additional acoustic deglazing",
            "applied_solution": "Initiated priority express bay slot with Master Tech Ramesh for 5-min ultrasonic rotor deglazing; customer awarded 5-star rating.",
            "new_skill_unlocked": "Express Service Bed-In Customer Reassurance Protocol",
            "xp_awarded": 50
        }
    ]
}
}


class ChamundaShopSubagentsManager:
    """Executive orchestrator managing departmental subagents under CEO Aradhya."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.subagents_file = self.data_dir / "shop_subagents.json"
        self.delegations_file = self.data_dir / "shop_delegations.json"
        self.commands_file = self.data_dir / "shop_written_commands.json"
        self.growth_file = self.data_dir / "shop_subagents_growth.json"
        self._init_storage()

    def _init_storage(self) -> None:
        """Initialize persistence files if not existing."""
        if not self.subagents_file.exists():
            self.subagents_file.write_text(json.dumps(DEFAULT_SUBAGENTS, indent=2), encoding="utf-8")

        if not self.delegations_file.exists():
            initial_delegations = [
                {
                    "delegation_id": "DEL-20260910-001",
                    "agent_id": "bay_chief",
                    "agent_name": "Master Workshop & Bay Chief",
                    "delegated_by": "Aradhya (Chief Executive Officer)",
                    "task_title": "50-Point Acoustic Audit on Classic 350",
                    "task_description": "Perform FFT resonance check on GJ-01-RE-3500 and verify sub-bass cadence <85 dB.",
                    "status": "Completed",
                    "delegated_at": "2026-09-10 09:30 AM",
                    "completed_at": "2026-09-10 10:15 AM",
                    "result_summary": "Inspection passed with 94/100 Health Score. Dominant exhaust bass tuned to 42 Hz."
                },
                {
                    "delegation_id": "DEL-20260910-002",
                    "agent_id": "parts_specialist",
                    "agent_name": "Inventory & OEM Parts Specialist",
                    "delegated_by": "Aradhya (Chief Executive Officer)",
                    "task_title": "Wholesale PO for Low-Stock Filters & Motul 15W-50",
                    "task_description": "Generate purchase order for 20W50 mineral oil and genuine oil filter elements.",
                    "status": "Completed",
                    "delegated_at": "2026-09-10 11:00 AM",
                    "completed_at": "2026-09-10 11:10 AM",
                    "result_summary": "PO-20260910-001 created for ₹34,250. Supplier dispatch confirmed."
                }
            ]
            self.delegations_file.write_text(json.dumps(initial_delegations, indent=2), encoding="utf-8")

        if not self.commands_file.exists():
            initial_commands = [
                {
                    "command_id": "CMD-20260910-090000",
                    "raw_command": "Classic 350 એન્જિન સાઉન્ડ અને ટેપેટ ટ્યુનિંગ કરો",
                    "sender": "Alpesh Sir (Founder & Chairman)",
                    "priority": "High",
                    "target_agent_id": "bay_chief",
                    "target_agent_name": "Master Workshop & Bay Chief",
                    "designated_head": "Master Tech Ramesh (12+ Yrs RE Specialist)",
                    "parsed_intent": {
                        "target_agent_id": "bay_chief",
                        "confidence_score": 10,
                        "priority": "High",
                        "entities": {"motorcycle_model": "Classic 350"}
                    },
                    "delegation_id": "DEL-20260910-001",
                    "status": "Executed",
                    "executed_at": "2026-09-10 09:00 AM",
                    "response_gu": "સાહેબ, માસ્ટર ટેક રમેશભાઈએ આપનો લેખિત આદેશ સ્વીકારી લીધો છે: વર્કશોપ બે ૧-૩ માં ટેકનિકલ કામગીરી અને ડાયગ્નોસ્ટિક્સ શરૂ કરી દેવામાં આવ્યા છે.",
                    "response_en": "Master Tech Ramesh acknowledged: Workshop bay operations & 50-point diagnostics initiated according to your written command."
                }
            ]
            self.commands_file.write_text(json.dumps(initial_commands, indent=2), encoding="utf-8")

        if not self.growth_file.exists():
            self.growth_file.write_text(json.dumps(DEFAULT_GROWTH_PROFILES, indent=2), encoding="utf-8")

    def list_subagents(self) -> List[Dict[str, Any]]:
        """Return all 5 departmental subagents with live status."""
        try:
            return json.loads(self.subagents_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return DEFAULT_SUBAGENTS

    def get_subagent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Find subagent by ID or role name."""
        agents = self.list_subagents()
        aid_clean = agent_id.lower().replace("-", "_").strip()
        for a in agents:
            if a["agent_id"] == aid_clean or aid_clean in a["agent_id"]:
                return a
        return None

    def get_delegation_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve executive directives issued by CEO Aradhya."""
        try:
            return json.loads(self.delegations_file.read_text(encoding="utf-8") or "[]")[:limit]
        except Exception:
            return []

    def delegate_task(
        self,
        agent_id: str,
        task_title: str,
        task_description: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Delegate an executive task to a departmental subagent,
        route to the appropriate underlying engine, and log execution.
        """
        agent = self.get_subagent(agent_id)
        if not agent:
            return {"success": False, "error": f"Sub-agent '{agent_id}' not found in registry."}

        target_aid = agent["agent_id"]
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        delegation_id = f"DEL-{today_str}-{datetime.datetime.now().strftime('%H%M%S')}"

        # Operational Execution Routing based on Department
        result_details = {}
        if target_aid == "bay_chief":
            result_details = {
                "action": "Bay & Workshop Directive Executed",
                "supervisor": agent["designated_head"],
                "bay_allocated": "Bay 1 (J-Series Quick Bay)",
                "technical_status": "50-Point Acoustic & Calibration Standards Applied",
                "notes": f"Directive '{task_title}' executed across workshop bays with zero-defect standard."
            }

        elif target_aid == "parts_specialist":
            sys.path.insert(0, str(BASE_DIR))
            from inventory_engine import ChamundaInventoryManager
            inv = ChamundaInventoryManager()
            val = inv.get_total_inventory_valuation()
            result_details = {
                "action": "Spares & Inventory Check Executed",
                "controller": agent["designated_head"],
                "active_skus": val.get("total_distinct_skus", 4469),
                "stock_units": val.get("total_units_in_stock", 18240),
                "status": "OEM Catalog In Sync & Authenticity Verified",
                "notes": f"Directive '{task_title}' fulfilled. Spares allocated."
            }

        elif target_aid == "customer_receptionist":
            result_details = {
                "action": "Customer Experience Directive Executed",
                "officer": agent["designated_head"],
                "channel": "WhatsApp Business (+91 78747 19139)",
                "status": "Automated Response Dispatched / Booking Confirmed",
                "notes": f"Customer request '{task_title}' handled on 24/7 AI Desk."
            }

        elif target_aid == "social_growth_manager":
            sys.path.insert(0, str(BASE_DIR))
            from omnichannel_social_engine import ChamundaOmnichannelSocialEngine
            soc = ChamundaOmnichannelSocialEngine()
            telem = soc.get_channel_telemetry()
            result_details = {
                "action": "Omnichannel Brand Directive Executed",
                "lead": agent["designated_head"],
                "reach": telem.get("total_community_reach", "45K+"),
                "channels": ["WhatsApp", "Instagram", "Facebook", "Google Business", "YouTube"],
                "notes": f"Campaign / Media task '{task_title}' syndicated across all 5 channels."
            }

        elif target_aid == "accounts_controller":
            result_details = {
                "action": "Financial & Billing Audit Executed",
                "auditor": agent["designated_head"],
                "compliance": "100% GST & NPCI UPI Standards",
                "status": "Invoice / Ledger Updated",
                "notes": f"Accounting directive '{task_title}' logged into store register."
            }
        elif target_aid == "devang_billing":
            sys.path.insert(0, str(BASE_DIR))
            from dms_enterprise_suite_engine import get_dms_suite_engine
            dms = get_dms_suite_engine()
            overview = dms.get_dms_overview_telemetry()
            result_details = {
                "action": "DMS Invoicing & Warranty Directive Executed",
                "officer": agent["designated_head"],
                "total_invoices": overview["total_invoices_generated"],
                "total_warranty_claims": overview["total_warranty_claims"],
                "gstin": overview["gstin"],
                "status": "Split GST (SAC 998729 & HSN 8714) / OEM FSC Verified",
                "notes": f"Billing & Warranty directive '{task_title}' executed on official RE DMS portal."
            }
        elif target_aid == "neha_crm_marketing":
            sys.path.insert(0, str(BASE_DIR))
            from dms_enterprise_suite_engine import get_dms_suite_engine
            dms = get_dms_suite_engine()
            overview = dms.get_dms_overview_telemetry()
            result_details = {
                "action": "DMS Marketing & Lead Campaign Executed",
                "lead": agent["designated_head"],
                "active_campaigns": overview["active_campaigns_count"],
                "lead_pipeline": overview["active_leads_count"],
                "channel": "WhatsApp Broadcast (+91 78747 19139)",
                "status": "Promotional Blast / Service Reminders Active",
                "notes": f"Marketing & CRM directive '{task_title}' deployed across North Gujarat customer base."
            }

        delegation_record = {
            "delegation_id": delegation_id,
            "agent_id": target_aid,
            "agent_name": agent["name"],
            "delegated_by": "Aradhya (Chief Executive Officer)",
            "task_title": task_title,
            "task_description": task_description,
            "status": "Completed",
            "delegated_at": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "completed_at": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "execution_details": result_details,
            "result_summary": f"Successfully executed by {agent['designated_head']}: {result_details.get('notes', 'Completed')}"
        }

        # Persist delegation record
        delegations = self.get_delegation_history(limit=500)
        delegations.insert(0, delegation_record)
        self.delegations_file.write_text(json.dumps(delegations, indent=2), encoding="utf-8")

        return {
            "success": True,
            "delegation_id": delegation_id,
            "agent_name": agent["name"],
            "designated_head": agent["designated_head"],
            "delegation": delegation_record
        }

    def get_executive_overview(self) -> Dict[str, Any]:
        """Consolidated executive overview of all 5 departmental subagents for CEO Aradhya."""
        agents = self.list_subagents()
        history = self.get_delegation_history(limit=50)
        cmd_history = self.get_written_commands_history(limit=50)
        growth_data = self.get_agent_growth_telemetry()
        total_healed = sum(p.get("issues_resolved_autonomously", 0) for p in growth_data.values())

        completed_count = len([d for d in history if d.get("status") == "Completed"])
        departments_active = len(agents)

        return {
            "ceo_command": "Aradhya (Chief Executive Officer)",
            "executive_suite_status": "ALL_DEPARTMENTS_OPERATIONAL",
            "departments_active": departments_active,
            "total_delegated_directives": len(history),
            "completed_directives": completed_count,
            "total_written_commands": len(cmd_history),
            "total_incidents_self_healed": total_healed,
            "subagents": agents,
            "growth_matrix": growth_data,
            "recent_delegations": history[:5],
            "recent_written_commands": cmd_history[:5]
        }

    def get_written_commands_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve historical written directives issued by Alpesh Sir or CEO Aradhya."""
        try:
            return json.loads(self.commands_file.read_text(encoding="utf-8") or "[]")[:limit]
        except Exception:
            return []

    def parse_written_command_intent(self, command_text: str) -> Dict[str, Any]:
        """
        Analyze a written command (Gujarati or English) to extract:
        - Target Subagent
        - Action Intent
        - Priority
        - Extracted entities (models, amounts, parts, customer names)
        """
        cmd_lower = command_text.lower()

        # Priority Detection
        priority = "Normal"
        urgent_triggers = ["urgent", "emergency", "asap", "તાત્કાલિક", "જરૂરી", "તરત", "ઇમરજન્સી", "priority", "critical", "immediate"]
        if any(w in cmd_lower for w in urgent_triggers):
            priority = "Urgent"
        elif any(w in cmd_lower for w in ["high", "મહત્વનું", "important", "fast"]):
            priority = "High"

        # Keyword mapping for departments
        department_keywords = {
            "bay_chief": [
                "ramesh", "રમેશ", "bay", "બે", "workshop", "વર્કશોપ", "tappet", "ટેપેટ", 
                "sound", "સાઉન્ડ", "thump", "થમ્પ", "acoustic", "diagnostic", "ડાયગ્નોસ્ટિક",
                "engine", "એન્જિન", "vintage", "cast iron", "કાસ્ટ આયર્ન", "restomod", "રેસ્ટોમોડ",
                "exhaust", "વાલ્વ", "valve", "clearance", "50-point", "inspection", "સર્વિસ બે",
                "mechanic", "noise", "અવાજ", "schematic", "torque", "exploded", "સ્કીમેટિક", "ટોર્ક",
                "borescope", "endoscopy", "carbon", "બોરસ્કોપ", "એન્ડોસ્કોપી", "crosshatch"
            ],
            "parts_specialist": [
                "jayesh", "જયેશ", "part", "પાર્ટ", "spare", "સ્પેર", "stock", "સ્ટોક",
                "inventory", "ઇન્વેન્ટરી", "order", "ઓર્ડર", "po", "purchase order",
                "spark plug", "પ્લગ", "filter", "ફિલ્ટર", "oil", "ઓઇલ", "motul", "મોટુલ",
                "sku", "brake pad", "બ્રેક", "chain", "ચેઈન", "sprocket", "cable", "કેબલ",
                "clutch", "ક્લચ", "procurement", "સપ્લાયર", "hologram", "હોલોગ્રામ", "barcode",
                "branch", "transfer", "patan", "visnagar", "unjha", "palanpur", "બ્રાન્ચ", "ટ્રાન્સફર",
                "waybill", "વેબિલ", "supply chain", "supply-chain"
            ],
            "customer_receptionist": [
                "priya", "પ્રિયા", "customer", "કસ્ટમર", "reception", "રિસેપ્શન", "whatsapp",
                "વ્હોટ્સએપ", "booking", "બુકિંગ", "call", "ફોન", "message", "મેસેજ",
                "sos", "breakdown", "બ્રેકડાઉન", "highway", "હાઈવે", "rider", "રાઇડર",
                "ready", "તૈયાર", "track", "ટ્રેક", "status", "સ્ટેટસ", "slot", "સ્લોટ",
                "78747", "kiosk", "કિઓસ્ક", "token", "ટોકન", "lounge", "લાઉન્જ"
            ],
            "social_growth_manager": [
                "kabir", "કબીર", "social", "સોશિયલ", "instagram", "ઇન્સ્ટાગ્રામ", "insta",
                "youtube", "યુટ્યુબ", "reel", "રીલ", "short", "શોર્ટ", "facebook", "ફેસબુક",
                "google", "ગૂગલ", "review", "રિવ્યુ", "post", "પોસ્ટ",
                "brand", "બ્રાન્ડ", "video", "વિડીયો", "syndicat", "સિન્ડિકેટ", "creator", "automation"
            ],
            "accounts_controller": [
                "hasmukh", "હસમુખ", "account", "એકાઉન્ટ", "reconcil", "મેળવણું", "finance",
                "ફાઇનાન્સ", "tax", "ટેક્સ", "pos", "પીઓએસ", "ledger", "લેજર", "₹",
                "b2b", "બીટુબી", "wholesale", "હોલસેલ", "amc", "એએમસી", "pass", "પાસ",
                "daybook", "ડેબુક", "cash book", "કેશબુક", "p&l", "gstr-1", "gstr"
            ],
            "devang_billing": [
                "devang", "દેવાંગ", "billing", "બિલિંગ", "bill", "બિલ", "invoice", "ઇન્વોઇસ",
                "warranty", "વોરંટી", "fsc", "free service", "coupon", "કુપન", "claim", "ક્લેમ",
                "gate pass", "ગેટપાસ", "split gst", "split", "sac 998729", "sac", "hsn 8714", "hsn",
                "insurance", "વીમો", "surveyor", "સર્વેયર", "tax invoice", "ટેક્સ ઇન્વોઇસ",
                "dms", "dealer management", "re-dms"
            ],
            "neha_crm_marketing": [
                "neha", "નેહા", "crm", "સીઆરએમ", "campaign", "કેમ્પેઇન", "lead", "લીડ",
                "broadcast", "બ્રોડકાસ્ટ", "test ride", "ટેસ્ટ રાઇડ", "test-ride", "reminder", "રિમાઇન્ડર",
                "camp", "કેમ્પ", "loyalty", "લોયલ્ટી", "retention", "રિટેન્શન", "promotion", "ઓફર",
                "service reminder", "30-day", "60-day", "90-day", "follow up"
            ],
            "vikram_sales": [
                "vikram", "વિક્રમ", "sales", "સેલ્સ", "booking", "બુકિંગ", "pdi", "પીડીઆઈ",
                "ride sure", "રાઇડ સ્યોર", "delivery", "ડિલિવરી", "showroom", "શોરૂમ",
                "token", "advance", "finance", "loan", "down payment", "colorway", "pre-delivery"
            ],
            "ananya_qc_csat": [
                "ananya", "અનન્યા", "qc", "ક્યુસી", "quality", "ક્વોલિટી", "csat", "સીસેટ",
                "feedback", "ફીડબેક", "psf", "post service", "post-service", "3-day", "complaint",
                "રેટિંગ", "rating", "star", "સ્ટાર", "nps", "satisfaction", "ગ્રાહક સંતોષ"
            ]
        }

        # Explicit name mentions get absolute priority
        name_weights = {
            "devang_billing": ["devang", "દેવાંગ"],
            "neha_crm_marketing": ["neha", "નેહા"],
            "vikram_sales": ["vikram", "વિક્રમ"],
            "ananya_qc_csat": ["ananya", "અનન્યા"],
            "bay_chief": ["ramesh", "રમેશ"],
            "parts_specialist": ["jayesh", "જયેશ"],
            "customer_receptionist": ["priya", "પ્રિયા"],
            "social_growth_manager": ["kabir", "કબીર"],
            "accounts_controller": ["hasmukh", "હસમુખ"]
        }

        # Scoring
        scores = {k: 0 for k in department_keywords}
        for dept, kws in department_keywords.items():
            for kw in kws:
                if kw in cmd_lower:
                    scores[dept] += 2
            for name in name_weights.get(dept, []):
                if name in cmd_lower:
                    scores[dept] += 15

        best_dept = max(scores, key=scores.get)
        if scores[best_dept] == 0:
            best_dept = "bay_chief"

        # Extract entities
        extracted = {}
        models = [
            "Classic 350", "Hunter 350", "Bullet 350", "Himalayan 450", "Continental GT 650",
            "Interceptor 650", "Shotgun 650", "Meteor 350", "Super Meteor 650", "Classic 500"
        ]
        for m in models:
            if m.lower() in cmd_lower or m.split()[0].lower() in cmd_lower:
                extracted["motorcycle_model"] = m
                break

        import re
        money_match = re.search(r'(?:₹|rs\.?|inr)\s*([\d,]+)', cmd_lower)
        if money_match:
            extracted["amount"] = money_match.group(1).replace(",", "")

        phone_match = re.search(r'(?:\+91|91)?\s*([6-9]\d{9})', cmd_lower)
        if phone_match:
            extracted["phone"] = phone_match.group(1)

        return {
            "target_agent_id": best_dept,
            "confidence_score": scores[best_dept],
            "priority": priority,
            "entities": extracted
        }

    def execute_written_command(
        self,
        command_text: str,
        sender: str = "Alpesh Sir (Founder & Chairman)",
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a freeform written command from Alpesh Sir or CEO Aradhya,
        parse the natural language directive, dispatch to the correct sub-agent,
        and generate a comprehensive executive response in Gujarati and English.
        """
        parsed = self.parse_written_command_intent(command_text)
        target_aid = parsed["target_agent_id"]
        cmd_priority = priority or parsed["priority"]

        agent = self.get_subagent(target_aid)
        if not agent:
            target_aid = "bay_chief"
            agent = self.get_subagent(target_aid)

        today_str = datetime.datetime.now().strftime("%Y%m%d")
        time_str = datetime.datetime.now().strftime("%H%M%S")
        cmd_id = f"CMD-{today_str}-{time_str}"

        # Clean title for task delegation
        title = command_text.strip()
        if len(title) > 60:
            title = title[:57] + "..."

        delegation_res = self.delegate_task(
            agent_id=target_aid,
            task_title=title,
            task_description=command_text
        )

        head = agent["designated_head"]
        dept_name = agent["name"]

        if target_aid == "bay_chief":
            resp_gu = f"સાહેબ, માસ્ટર ટેક રમેશભાઈએ આપનો લેખિત આદેશ સ્વીકારી લીધો છે: વર્કશોપ બે ૧-૩ માં ટેકનિકલ કામગીરી અને ડાયગ્નોસ્ટિક્સ શરૂ કરી દેવામાં આવ્યા છે."
            resp_en = f"Master Tech Ramesh acknowledged: Workshop bay operations & 50-point diagnostics initiated according to your written command."
        elif target_aid == "parts_specialist":
            resp_gu = f"સાહેબ, જયેશભાઈ પટેલે આપનો લેખિત આદેશ નોંધી લીધો છે: OEM કેટલોગ અને સ્ટોક રજિસ્ટર ચકાસીને જરૂરી સ્પેરપાર્ટ્સ એલોકેટ / PO પ્રોસેસ કરી દીધા છે."
            resp_en = f"Jayeshbhai Patel acknowledged: OEM catalog & stock register inspected; spare parts allocated / wholesale purchase order processed."
        elif target_aid == "customer_receptionist":
            resp_gu = f"સાહેબ, પ્રિયા શર્માએ ૨૪/૭ ડેસ્ક (+91 78747 19139) પરથી આદેશ અમલમાં મૂક્યો છે: કસ્ટમર કમ્યુનિકેશન / સર્વિસ સ્ટેજ અપડેટ કરી દીધું છે."
            resp_en = f"Priya Sharma acknowledged on 24/7 Desk (+91 78747 19139): Customer service stage update / notification dispatched."
        elif target_aid == "social_growth_manager":
            resp_gu = f"સાહેબ, કબીર મહેતાએ આપનો સોશિયલ આદેશ સ્વીકાર્યો છે: WhatsApp, Instagram, FB, Google Business અને YouTube તમામ ૫ ચેનલ્સ પર કન્ટેન્ટ સિન્ડિકેટ થઈ રહ્યું છે."
            resp_en = f"Kabir Mehta acknowledged: Omnichannel content and campaign syndicated across all 5 digital channels."
        elif target_aid == "accounts_controller":
            resp_gu = f"સાહેબ, હસમુખભાઈ જોશીએ બિલિંગ & GST રજિસ્ટરમાં આદેશ અમલમાં મૂક્યો છે: એકાઉન્ટ્સ મેળવણું / ડેબુક & જીએસટી રિકન્સિલેશન કમ્પ્લીટ થયેલ છે."
            resp_en = f"Hasmukhbhai Joshi acknowledged: Financial ledger updated; Daybook & GST reconciliation ready."
        elif target_aid == "devang_billing":
            resp_gu = f"સાહેબ, દેવાંગ દવેએ RE-DMS બિલિંગ & વોરંટી ડેસ્ક પર આદેશ સ્વીકાર્યો છે: સ્પ્લિટ GST ઇન્વોઇસિંગ (લેબર SAC 998729 & સ્પેર HSN 8714), FSC કુપન અને OEM ક્લેમ ફાઇલિંગ સફળતાપૂર્વક અપડેટ થયું છે."
            resp_en = f"Devang Dave acknowledged at RE-DMS Billing & Claims Desk: Split GST invoicing, FSC coupons & OEM warranty claim documentation processed."
        elif target_aid == "neha_crm_marketing":
            resp_gu = f"સાહેબ, નેહા ત્રિવેદીએ CRM & માર્કેટિંગ ડેસ્ક પર આદેશ સ્વીકાર્યો છે: WhatsApp બ્રોડકાસ્ટ કેમ્પેઇન, ટેસ્ટ રાઇડ / બુકિંગ લીડ પાઇપલાઇન અને ૩૦/૬૦/૯૦ દિવસના સર્વિસ રિમાઇન્ડર્સ શેડ્યૂલ કરી દીધા છે."
            resp_en = f"Neha Trivedi acknowledged at CRM & Retention Desk: WhatsApp broadcast campaigns, test ride lead pipeline, and 30/60/90-day predictive reminders scheduled."
        elif target_aid == "vikram_sales":
            resp_gu = f"સાહેબ, વિક્રમ સિંહે શોરૂમ સેલ્સ & બુકિંગ ડેસ્ક પર આદેશ સ્વીકાર્યો છે: નવી રોયલ એનફિલ્ડ બુકિંગ ટોકન, ૩૦-પોઇન્ટ ડિજિટલ PDI સર્ટિફિકેટ અને 'Ride Sure' એક્સટેન્ડેડ વોરંટી પોલિસી પ્રોસેસ કરી દીધી છે."
            resp_en = f"Vikram Singh (Showroom Sales Lead) acknowledged: New motorcycle booking token receipt, 30-point digital PDI certificate, and Royal Enfield Ride Sure Extended Warranty processed."
        elif target_aid == "ananya_qc_csat":
            resp_gu = f"સાહેબ, અનન્યા જોશીએ ક્વોલિટી કંટ્રોલ & CSAT ડેસ્ક પર આદેશ સ્વીકાર્યો છે: ૩-દિવસીય પોસ્ટ-સર્વિસ ફોલો-અપ કોલ (PSF), CSAT સ્કોરિંગ (>૯૨% ટાર્ગેટ) અને વર્કશોપ ક્વોલિટી ચેક પૂર્ણ થયેલ છે."
            resp_en = f"Ananya Joshi (Quality Control & CSAT Lead) acknowledged: 3-Day Post-Service Feedback (PSF) logged, CSAT index (>92% target) audited, and first-time-right quality confirmed."
        else:
            resp_gu = f"સાહેબ, CEO આરાધ્યા તરીકે મેં આપનો લેખિત આદેશ ટીમમાં પાસ કરી દીધો છે."
            resp_en = f"CEO Aradhya: Your written directive has been successfully delegated to the team."

        command_log = {
            "command_id": cmd_id,
            "raw_command": command_text,
            "sender": sender,
            "priority": cmd_priority,
            "target_agent_id": target_aid,
            "target_agent_name": dept_name,
            "designated_head": head,
            "parsed_intent": parsed,
            "delegation_id": delegation_res.get("delegation_id", ""),
            "status": "Executed",
            "executed_at": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "response_gu": resp_gu,
            "response_en": resp_en,
            "execution_details": delegation_res.get("delegation", {}).get("execution_details", {})
        }

        cmd_history = self.get_written_commands_history(limit=500)
        cmd_history.insert(0, command_log)
        self.commands_file.write_text(json.dumps(cmd_history, indent=2), encoding="utf-8")

        return {
            "success": True,
            "command_id": cmd_id,
            "sender": sender,
            "target_agent": target_aid,
            "designated_head": head,
            "priority": cmd_priority,
            "response_gu": resp_gu,
            "response_en": resp_en,
            "command_log": command_log,
            "delegation": delegation_res.get("delegation")
        }

    def get_agent_growth_telemetry(self) -> Dict[str, Any]:
        """Retrieve autonomous growth, level, XP, and learned solutions for all 5 subagents."""
        try:
            return json.loads(self.growth_file.read_text(encoding="utf-8") or "{}")
        except Exception:
            return DEFAULT_GROWTH_PROFILES

    def record_growth_and_xp(
        self,
        agent_id: str,
        xp_earned: int,
        skill_learned: str,
        problem: str,
        solution: str,
        incident_id: Optional[str] = None,
        root_cause: Optional[str] = None
    ) -> Dict[str, Any]:
        """Record XP, increment level if threshold reached, add capability to registry."""
        growth_data = self.get_agent_growth_telemetry()
        profile = growth_data.get(agent_id)
        if not profile:
            profile = {
                "agent_id": agent_id,
                "agent_name": agent_id.replace("_", " ").title(),
                "designated_head": "Sub-Agent Lead",
                "level": 1,
                "title": "Standard Specialist",
                "xp": 0,
                "xp_to_next_level": 200,
                "issues_resolved_autonomously": 0,
                "autonomous_healing_rate": "99.0%",
                "learned_capabilities": [],
                "incident_history": []
            }
            growth_data[agent_id] = profile

        profile["xp"] += xp_earned
        profile["issues_resolved_autonomously"] += 1

        # Level Calculation: Level 1 (0-199), Level 2 (200-399), Level 3 (400-699), Level 4 (700-999), Level 5 Master (1000+)
        if profile["xp"] >= 1000:
            profile["level"] = 5
            profile["title"] = "Autonomous Master Authority"
            profile["xp_to_next_level"] = 1500
        elif profile["xp"] >= 700:
            profile["level"] = 4
            profile["title"] = "Senior Diagnostic Specialist"
            profile["xp_to_next_level"] = 1000
        elif profile["xp"] >= 400:
            profile["level"] = 3
            profile["title"] = "Advanced Operations Lead"
            profile["xp_to_next_level"] = 700
        elif profile["xp"] >= 200:
            profile["level"] = 2
            profile["title"] = "Operational Specialist"
            profile["xp_to_next_level"] = 400
        else:
            profile["level"] = 1
            profile["title"] = "Standard Specialist"
            profile["xp_to_next_level"] = 200

        # Add learned capability if not present
        if skill_learned and skill_learned not in profile.get("learned_capabilities", []):
            profile.setdefault("learned_capabilities", []).append(skill_learned)

        # Record incident history
        inc_entry = {
            "incident_id": incident_id or f"INC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "issue": problem,
            "root_cause": root_cause or "Diagnosed and neutralized autonomously",
            "applied_solution": solution,
            "new_skill_unlocked": skill_learned,
            "xp_awarded": xp_earned
        }
        profile.setdefault("incident_history", []).insert(0, inc_entry)

        # Persist growth file
        self.growth_file.write_text(json.dumps(growth_data, indent=2), encoding="utf-8")

        # Auto-update subagents registry capabilities
        agents = self.list_subagents()
        updated_agents = False
        for a in agents:
            if a["agent_id"] == agent_id:
                if skill_learned and skill_learned not in a.get("capabilities", []):
                    a.setdefault("capabilities", []).append(skill_learned)
                    updated_agents = True
        if updated_agents:
            self.subagents_file.write_text(json.dumps(agents, indent=2), encoding="utf-8")

        return profile

    def diagnose_and_heal_incident(
        self,
        agent_id: str,
        issue_description: str,
        auto_apply: bool = True
    ) -> Dict[str, Any]:
        """
        Autonomously diagnose an issue, identify the root cause, formulate the resolution,
        apply self-healing, award XP, and update capabilities in the sub-agent registry.
        """
        agent = self.get_subagent(agent_id)
        if not agent:
            return {"success": False, "error": f"Sub-agent '{agent_id}' not found."}

        aid = agent["agent_id"]
        issue_lower = issue_description.lower()
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        time_str = datetime.datetime.now().strftime("%H%M%S")
        inc_id = f"INC-{aid.upper()[:4]}-{today_str}-{time_str}"

        # Domain-Specific Root Cause & Autonomous Fix Synthesis
        root_cause = ""
        applied_solution = ""
        new_skill = ""
        solution_gu = ""

        if aid == "bay_chief":
            if any(w in issue_lower for w in ["tappet", "valve", "noise", "અવાજ", "ટેપેટ", "tick"]):
                root_cause = "Exhaust rocker arm clearance expanded beyond 0.18 mm tolerance due to thermal expansion."
                applied_solution = "Micrometer calibration applied; hydraulic lifter bled; tappet gap set to intake 0.08 mm, exhaust 0.18 mm. Sound normalized <82 dB."
                new_skill = "Precision Hydraulic Rocker Arm Calibration"
                solution_gu = "રમેશભાઈએ ટેપેટ ક્લિયરન્સ અને હાઇડ્રોલિક લિફ્ટર 0.18 mm પર સેટ કરીને અવાજ શાંત કરી દીધો."
            elif any(w in issue_lower for w in ["thump", "exhaust", "થમ્પ", "emission", "db"]):
                root_cause = "Exhaust header carbon accumulation and loose baffle packing causing high-pitch rasp >86 dB."
                applied_solution = "Acoustic chamber decarbonized; glass-wool baffle repacked; sub-bass tuned to 42 Hz authentic thump at 81 dB."
                new_skill = "Acoustic Baffle Decarbonization & Sub-Bass Tuning"
                solution_gu = "એક્ઝોસ્ટ ચેમ્બરમાંથી કાર્બન સાફ કરી બેફલ પેકિંગ રિપ્લેસ કર્યું; પ્યોર રોયલ એનફિલ્ડ થમ્પ રિસ્ટોર કર્યો."
            elif any(w in issue_lower for w in ["fuel", "efi", "pump", "pressure", "પ્રેશર"]):
                root_cause = "Fuel pump relay voltage fluctuating below 11.2V during high-temperature run."
                applied_solution = "Relay wiring bypassed to auxiliary ignition harness; fuel rail pressure stabilized at 3.0 bar."
                new_skill = "EFI Rail Pressure Electronic Stabilization"
                solution_gu = "ફ્યુઅલ પંપ રિલે વાયરિંગ બાયપાસ કરી પ્રેશર 3.0 bar પર સ્થિર કર્યું."
            else:
                root_cause = f"Mechanical anomaly detected: {issue_description}"
                applied_solution = "50-point diagnostic scan executed; torque specs recalibrated to factory RE standards."
                new_skill = "Dynamic 50-Point Factory Torque Recalibration"
                solution_gu = "ફેક્ટરી ટોર્ક સ્પેસિફિકેશન મુજબ તમામ બોલ્ટ્સ અને જોઈન્ટ્સ રી-કેલિબ્રેટ કર્યા."

        elif aid == "parts_specialist":
            if any(w in issue_lower for w in ["stock", "out of stock", "shortage", "motul", "plug", "ઓઈલ", "પ્લગ", "સ્ટોક"]):
                root_cause = "Primary distributor shipment delayed; inventory buffer fell below critical 5-unit threshold."
                applied_solution = "Triggered automated secondary OEM supplier PO; allocated cross-brand verified substitute for walk-in counter."
                new_skill = "Automated Dual-Vendor Rapid PO Failover"
                solution_gu = "જયેશભાઈએ સેકન્ડરી હોલસેલ સપ્લાયર પાસેથી તાત્કાલિક સ્ટોક મંગાવ્યો અને ઓલ્ટરનેટિવ પાર્ટ્સ એલોકેટ કર્યા."
            elif any(w in issue_lower for w in ["counterfeit", "fake", "barcode", "packaging", "ખોટું", "બારકોડ"]):
                root_cause = "Supplier batch #RE-889 failed 3D hologram reflection test and 13-digit GS1 barcode verification."
                applied_solution = "Batch quarantined immediately; vendor RMA return issued; supplier flagged in procurement ledger."
                new_skill = "Automated 3D Hologram & GS1 Quarantine Protocol"
                solution_gu = "શંકાસ્પદ બેચને તાત્કાલિક ક્વોરેન્ટાઇન કરી સપ્લાયરને રિટર્ન RMA મોકલી દીધું."
            else:
                root_cause = f"Inventory discrepancy detected: {issue_description}"
                applied_solution = "Complete physical vs digital barcode cycle count completed across 4,469 SKUs; ledger normalized."
                new_skill = "Continuous Real-Time Cycle Count Harmonization"
                solution_gu = "ડિજિટલ કેટલોગ અને શેલ્ફ સ્ટોકનું 100% મેળવણું કરી સ્ટોક અપડેટ કર્યો."

        elif aid == "customer_receptionist":
            if any(w in issue_lower for w in ["highway", "sos", "stranded", "breakdown", "હાઈવે", "બ્રેકડાઉન"]):
                root_cause = "Rider stranded in low network dead-zone with intermittent mobile connectivity."
                applied_solution = "Engaged low-bandwidth emergency SMS telemetry relay; dispatched Chamunda mobile roadside patrol van with GPS coords."
                new_skill = "Low-Bandwidth Highway SOS Telemetry Relay"
                solution_gu = "પ્રિયાએ લો-નેટવર્ક SMS દ્વારા રાઇડરનું લોકેશન ટ્રેસ કરી તાત્કાલિક મોબાઇલ વાન રવાના કરી."
            elif any(w in issue_lower for w in ["delay", "complaint", "angry", "wait", "મોડું", "ફરિયાદ"]):
                root_cause = "Bay backlog caused by earlier complex vintage engine teardown delaying subsequent delivery by 35 mins."
                applied_solution = "Escalated customer to executive lounge; offered complimentary waterless wash & chain lube; priority bay bumped."
                new_skill = "Executive Customer Retention & Bay Prioritization"
                solution_gu = "ગ્રાહકને પ્રાયોરિટી બે ફાળવી કોમ્પ્લિમેન્ટરી ચેઈન લ્યુબ ઓફર કરી સંતોષકારક સમાધાન કર્યું."
            else:
                root_cause = f"Customer desk service conflict: {issue_description}"
                applied_solution = "24/7 WhatsApp AI channel synchronized; personalized bilingual voice memo dispatched to customer."
                new_skill = "Automated Bilingual Voice Memo Dispatch"
                solution_gu = "ગ્રાહકને દ્વિભાષી વ્હોટ્સએપ વોઈસ મેમો દ્વારા સ્ટેટસ અપડેટ આપ્યું."

        elif aid == "social_growth_manager":
            if any(w in issue_lower for w in ["review", "1-star", "negative", "rating", "રિવ્યુ", "નેગેટિવ"]):
                root_cause = "Customer left critical 1-star review regarding perceived pricing on custom chrome crash guard."
                applied_solution = "Synthesized respectful bilingual owner response explaining 100% OEM tensile strength warranty & transparent bill; invited customer for free safety check."
                new_skill = "Strategic Google Business Reputation Defense"
                solution_gu = "કબીરે ગૂગલ રિવ્યુ પર સન્માનપૂર્વક ખુલાસો મૂકી ગ્રાહકને ફ્રી સેફ્ટી ચેક-અપ માટે આમંત્રિત કર્યા."
            elif any(w in issue_lower for w in ["youtube", "shorts", "views", "reach", "algorithm", "રીચ", "શોર્ટ્સ"]):
                root_cause = "YouTube Shorts algorithmic retention drop in the first 3 seconds of video."
                applied_solution = "Re-engineered hook with high-impact 500cc Cast Iron cold-start exhaust audio burst; dynamic sound waveform overlay added."
                new_skill = "High-Impact Acoustic Hook Algorithmic Tuning"
                solution_gu = "શોર્ટ્સ માટે પહેલા ૩ સેકન્ડમાં પ્યોર થમ્પ સાઉન્ડ હૂક મૂકી ઓર્ગેનિક રીચ બૂસ્ટ કરી."
            else:
                root_cause = f"Social engagement deviation: {issue_description}"
                applied_solution = "Syndicated refreshed high-resolution build showcase across all 5 channels with +91 78747 19139 CTA."
                new_skill = "Multi-Channel Broadcast Re-Syndication"
                solution_gu = "તમામ ૫ ચેનલ્સ પર તાજી પોસ્ટ મૂકી કસ્ટમર કોલ-ટુ-એક્શન એક્ટિવ કર્યું."

        elif aid == "accounts_controller":
            if any(w in issue_lower for w in ["upi", "qr", "timeout", "payment", "પેમેન્ટ", "ક્યુઆર"]):
                root_cause = "Bank switch latency caused 60-second delay in NPCI payment settlement callback."
                applied_solution = "Queried banking switch API with 12-digit RRN; payment verified and marked cleared in POS; invoice receipt issued."
                new_skill = "Direct NPCI RRN Gateway Verification"
                solution_gu = "હસમુખભાઈએ RRN નંબર દ્વારા બેંક પોર્ટલ પરથી પેમેન્ટ કન્ફર્મ કરી ઇન્સ્ટન્ટ બિલ આપ્યું."
            elif any(w in issue_lower for w in ["gst", "hsn", "tax", "ટેક્સ", "જીએસટી"]):
                root_cause = "Part accessory categorized under 18% HSN 8714 instead of specialized 28% composite code."
                applied_solution = "Re-mapped HSN tax matrix in database; recalculated input tax credit (ITC); updated GST return ledger."
                new_skill = "Automated HSN Tax Mapping Harmonization"
                solution_gu = "HSN કોડનું રી-મેપિંગ કરી 100% GST કમ્પ્લાયન્ટ ઇન્વોઇસિંગ સેટ કર્યું."
            else:
                root_cause = f"Financial ledger variance: {issue_description}"
                applied_solution = "Daily cash and digital UPI settlement reconciled against counter register with zero audit variance."
                new_skill = "Zero-Variance Automated Daily Reconciliation"
                solution_gu = "કેશ અને UPI મેળવણું સંપૂર્ણપણે ટેલી કરી દીધું."

        # Award XP and update growth profile
        growth_res = self.record_growth_and_xp(
            agent_id=aid,
            xp_earned=50,
            skill_learned=new_skill,
            problem=issue_description,
            solution=applied_solution,
            incident_id=inc_id,
            root_cause=root_cause
        )

        return {
            "success": True,
            "incident_id": inc_id,
            "agent_id": aid,
            "agent_name": agent["name"],
            "designated_head": agent["designated_head"],
            "issue_reported": issue_description,
            "root_cause_diagnosed": root_cause,
            "applied_solution": applied_solution,
            "new_skill_unlocked": new_skill,
            "solution_gu": solution_gu,
            "xp_awarded": 50,
            "new_level": growth_res["level"],
            "total_xp": growth_res["xp"],
            "growth": growth_res
        }

    def simulate_agent_incident(self, agent_id: str, incident_type: Optional[str] = None) -> Dict[str, Any]:
        """Simulate a domain incident for a subagent and trigger autonomous self-healing."""
        sample_incidents = {
            "bay_chief": "Cold-start valve tappet tick noise on Classic 350 J-Series at 2,800 RPM",
            "parts_specialist": "OEM NGK Spark Plug (BPR6ES) out-of-stock warning across primary suppliers",
            "customer_receptionist": "Highway breakdown SOS signal received from stranded rider near Mehsana with weak 2G network",
            "social_growth_manager": "1-star critical review on Google Business Profile regarding custom parts delivery time",
            "accounts_controller": "Counter POS dynamic UPI QR transaction timed out while customer waiting to collect bike"
        }
        issue = incident_type or sample_incidents.get(agent_id, "Operational execution bottleneck")
        return self.diagnose_and_heal_incident(agent_id=agent_id, issue_description=issue)

# Convenience Aliases and Factory
ChamundaShopSubagentsManager.execute_command_with_subagent = ChamundaShopSubagentsManager.execute_written_command

_subagents_manager_instance = None

def get_shop_subagents_manager() -> ChamundaShopSubagentsManager:
    global _subagents_manager_instance
    if _subagents_manager_instance is None:
        _subagents_manager_instance = ChamundaShopSubagentsManager()
    return _subagents_manager_instance

get_subagent_manager = get_shop_subagents_manager
