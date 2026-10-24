"""
Chamunda Automobile Parts & Service - Royal Enfield Executive Web Portal & Enterprise OS.
Interactive workshop dashboard featuring live FFT sound diagnostics, 4,469 parts dynamic search,
active service bay tracking, one-click QR invoicing, and customer mobile passport verification.
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Add current directory to path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, "/home/alpesh/jarvis-agent")

from inventory_engine import ChamundaInventoryManager
from service_engine import ChamundaServiceManager
from billing_engine import ChamundaBillingManager
from acoustic_health_passport import ChamundaHealthPassportGenerator, PASSPORTS_DIR
from acoustic_sound_diagnostic import ChamundaSoundDiagnosticEngine
from crm_engine import ChamundaCRMManager
from core.wholesale_po_engine import WholesalePOEngine, PO_DIR
from customer_bot_engine import ChamundaCustomerBot
from thump_tuner_engine import ChamundaThumpTuner, THUMP_PRESETS
from counter_pos_engine import ChamundaCounterPOS, POS_RECEIPTS_DIR
from used_bike_inspection_engine import ChamundaPreOwnedManager, INSPECTIONS_DIR
from expedition_sos_engine import ChamundaExpeditionManager, EXPEDITIONS_DIR, TOURING_DESTINATIONS, SOS_ROAD_FAULTS
from restomod_studio_engine import ChamundaRestoModStudio, RESTOMODS_DIR, RESTOMOD_STYLES, CUSTOM_PAINT_THEMES, PERFORMANCE_STAGES, VINTAGE_CI_SPECS, VINTAGE_CI_FAULTS
from omnichannel_social_engine import ChamundaOmnichannelSocialEngine
from shop_subagents_engine import ChamundaShopSubagentsManager
from bay_voice_engine import get_bay_voice_engine
from b2b_wholesale_engine import get_b2b_wholesale_manager
from riders_club_engine import get_riders_club_manager
from obd_diagnostics_engine import get_obd_diagnostics_engine
from smart_kiosk_engine import get_smart_kiosk_engine
from predictive_supply_chain_engine import get_predictive_supply_chain_manager
from schematics_3d_engine import get_schematics_3d_engine
from borescope_inspection_engine import get_borescope_engine
from multibranch_hub_engine import get_multibranch_engine
from system_optimizer import get_system_optimizer
from webar_engine_guide import get_webar_engine
from night_locker_engine import get_night_locker_manager
from cloud_shadow_engine import get_cloud_shadow_manager
from kalpavriksha_growth_engine import get_kalpavriksha_engine
from dms_enterprise_suite_engine import get_dms_suite_engine
from chhaya_agent_gateway import get_chhaya_agent_gateway

app = FastAPI(
    title="Chamunda AI • Royal Enfield Specialist Workshop Portal",
    description="Live Sound Diagnostics, 4,469 Genuine Parts Catalog, QR Passports, and Predictive CRM",
    version="2.3.0"
)

# Mount static files for PWA manifest, service worker and mobile assets
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Initialize engines
inv_mgr = ChamundaInventoryManager()
srv_mgr = ChamundaServiceManager()
bill_mgr = ChamundaBillingManager()
passport_gen = ChamundaHealthPassportGenerator()
sound_eng = ChamundaSoundDiagnosticEngine()
crm_mgr = ChamundaCRMManager()
po_eng = WholesalePOEngine()
bot_eng = ChamundaCustomerBot()
thump_eng = ChamundaThumpTuner()
pos_eng = ChamundaCounterPOS()
preowned_mgr = ChamundaPreOwnedManager()
expedition_mgr = ChamundaExpeditionManager()
restomod_mgr = ChamundaRestoModStudio()
social_eng = ChamundaOmnichannelSocialEngine()
subagents_mgr = ChamundaShopSubagentsManager()
bay_voice_eng = get_bay_voice_engine()
b2b_mgr = get_b2b_wholesale_manager()
riders_club_mgr = get_riders_club_manager()
obd_eng = get_obd_diagnostics_engine()
kiosk_eng = get_smart_kiosk_engine()
supply_chain_mgr = get_predictive_supply_chain_manager()
schematics_eng = get_schematics_3d_engine()
borescope_eng = get_borescope_engine()
multibranch_eng = get_multibranch_engine()
system_optimizer_eng = get_system_optimizer()
webar_eng = get_webar_engine()
night_locker_mgr = get_night_locker_manager()
cloud_shadow_mgr = get_cloud_shadow_manager()
kalpavriksha_mgr = get_kalpavriksha_engine()
dms_suite_eng = get_dms_suite_engine()
chhaya_gateway = get_chhaya_agent_gateway()


# --- Pydantic Models ---
class JobCardCreateRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    odometer_km: int
    customer_issues: str
    service_type: str = "General Service & Diagnostics"
    mechanic: str = "Master Tech Alpesh (Chamunda Automobile)"


class AddPartToJobRequest(BaseModel):
    job_card_id: str
    part_name: str
    qty: int = 1
    price: float


class CompleteJobRequest(BaseModel):
    job_card_id: str
    technician: str = "Master Tech Alpesh (Chamunda Automobile)"
    service_notes: str = "Standard 50-Point Master Service & Valve Calibration"


class MarkReminderSentRequest(BaseModel):
    registration_no: str


class GeneratePORequest(BaseModel):
    supplier_name: str = "Royal Enfield OEM Genuine Spares Dist."


class SoundDiagnoseRequest(BaseModel):
    bike_model: str = "Hunter 350"
    record_seconds: int = 5
    simulate_fault: Optional[str] = None


class DiagnosticRequest(BaseModel):
    symptom: str


class BotChatRequest(BaseModel):
    message: str
    phone: Optional[str] = None


class BotBookRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    preferred_date: str = "Tomorrow 10:00 AM"
    customer_issues: str = "Periodic Service & Sound Check"


class JobCardUpdateStageRequest(BaseModel):
    job_card_id: str
    stage_name: str


class ThumpAnalyzeRequest(BaseModel):
    bike_model: str = "Classic 350"
    preset_key: str = "deep_vintage_chug"


class POSScanRequest(BaseModel):
    code_or_query: str


class POSCheckoutRequest(BaseModel):
    items: List[Dict[str, Any]]
    customer_name: str = "Counter Walk-in Customer"
    phone: str = ""
    payment_mode: str = "UPI"
    discount_amount: float = 0.0
    notes: str = ""


class PreOwnedValuationRequest(BaseModel):
    bike_model: str = "Classic 350"
    manufacturing_year: int = 2022
    odometer_km: int = 18000
    condition_score: float = 85.0
    model: Optional[str] = None
    year: Optional[int] = None


class PreOwnedInspectionRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: Optional[str] = None
    model: Optional[str] = None
    registration_no: str
    manufacturing_year: Optional[int] = None
    year: Optional[int] = None
    odometer_km: int = 15000
    checklist_overrides: Optional[Dict[str, Any]] = None
    inspector_name: str = "Master Tech Alpesh (Chamunda Automobile)"


class ExpeditionAuditRequest(BaseModel):
    rider_name: str
    phone: str
    bike_model: str
    registration_no: str
    destination_key: str = "ladakh_high_altitude"
    planned_km: int = 3500
    domain_scores: Optional[Dict[str, int]] = None
    inspector_name: str = "Master Tech Alpesh (Chamunda Automobile)"


class ExpeditionSparesKitRequest(BaseModel):
    bike_model: str = "Classic 350"
    destination_key: str = "ladakh_high_altitude"


class HighwaySOSTriageRequest(BaseModel):
    symptom_query: str


class RestoModQuoteRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    base_style: Optional[str] = "bobber_solo"
    style_key: Optional[str] = None
    custom_paint: Optional[str] = "british_racing_green"
    paint_theme_key: Optional[str] = None
    stage_tune: Optional[str] = "stage_1"
    performance_stage_key: Optional[str] = None
    include_vintage_ci_package: bool = False
    custom_notes: str = ""
    inspector_name: str = "Master Tech Alpesh (Chamunda Automobile)"


class PerformanceTuneRequest(BaseModel):
    bike_model: str = "Hunter 350"
    stage: Optional[str] = "stage_1"
    stage_key: Optional[str] = None


class VintageCIDiagnosticRequest(BaseModel):
    symptom_query: str
    engine_cc: int = 350


class SocialCampaignGenerateRequest(BaseModel):
    topic: str = "Classic 350 Cold Start Tappet Noise Fix"
    campaign_type: str = "Workshop Master Tip"
    custom_notes: str = ""


class SocialPublishRequest(BaseModel):
    campaign_id: Optional[str] = None
    topic: str = "Classic 350 Care"
    campaign_type: str = "Workshop Master Tip"
    channels: Optional[List[str]] = None
    channels_data: Optional[Dict[str, Any]] = None


class SocialInboxReplyRequest(BaseModel):
    item_id: str
    reply_text: str


class GoogleReviewReplyRequest(BaseModel):
    review_id: str
    reply_text: str
    reply_text_gu: Optional[str] = None


class TaskDelegationRequest(BaseModel):
    agent_id: str
    task_title: str
    task_description: str
    parameters: Optional[Dict[str, Any]] = None


class WrittenCommandRequest(BaseModel):
    command: str
    sender: Optional[str] = "Alpesh Sir (Founder & Chairman)"
    priority: Optional[str] = "Normal"


class AgentHealRequest(BaseModel):
    agent_id: str
    issue: str


class SimulateIncidentRequest(BaseModel):
    agent_id: str
    incident_type: Optional[str] = None


class BayVoiceProcessRequest(BaseModel):
    spoken_text: str
    mechanic_name: Optional[str] = "Master Tech Ramesh"
    bay_id: Optional[str] = "Bay 1 (J-Series Platform)"


class B2BGarageRegisterRequest(BaseModel):
    name: str
    owner_name: str
    phone: str
    city: str
    address: str
    tier: Optional[str] = "Bronze"
    gstin: Optional[str] = ""


class B2BOrderCreateRequest(BaseModel):
    garage_id: str
    items: List[Dict[str, Any]]
    payment_mode: Optional[str] = "Credit"
    notes: Optional[str] = ""


class ClubEnrollRequest(BaseModel):
    name: str
    phone: str
    bike_model: str
    registration_no: str
    plan_id: Optional[str] = "AMC-GOLD"


class ClubExpeditionRegisterRequest(BaseModel):
    expedition_id: str
    rider_name: str
    phone: str
    bike_model: str


class OBDScanRequest(BaseModel):
    bike_model: str = "Classic 350 (Reborn)"
    registration_no: str = "GJ-02-BQ-1234"
    simulate_dtc: Optional[str] = "P0505"


class KioskCheckinRequest(BaseModel):
    registration_no: str
    customer_name: str
    phone: str
    bike_model: str
    selected_issues: List[str]
    odometer_km: Optional[int] = 15000


class AutoPOGenerateRequest(BaseModel):
    season_key: Optional[str] = "diwali_dhanteras_rush"
    supplier_name: Optional[str] = "Royal Enfield Central Spares Distribution Depot"


class BorescopeInspectRequest(BaseModel):
    bike_model: str = "Classic 350 (Reborn)"
    registration_no: str = "GJ-02-BQ-1234"
    odometer_km: int = 15000
    scenario: str = "heavy_carbon_crust"


class BranchTransferRequest(BaseModel):
    from_branch: str = "HQ-MEHSANA"
    to_branch: str = "BR-PATAN-01"
    part_number: str = "574012/A"
    quantity: int = 1
    requested_by: str = "Branch Lead"
    part_name: Optional[str] = None
    unit_mrp: Optional[float] = 0.0
    notes: Optional[str] = ""


class SystemOptimizeRequest(BaseModel):
    mode: str = "safe"


class LockerReserveRequest(BaseModel):
    box_id: str = "BOX-01"
    customer_name: str = "Touring Rider"
    phone: str = "+91 98250 12345"
    vehicle_reg: Optional[str] = "GJ-02-BQ-1234"


class LockerUnlockRequest(BaseModel):
    reservation_id: str
    otp_code: str
    payment_ref: Optional[str] = "UPI-AUTOCONFIRMED"


class CloudShadowQueryRequest(BaseModel):
    query: str
    sender: Optional[str] = "Alpesh Sir (Remote Mobile)"
    phone: Optional[str] = "+91 78747 19139"


class CloudShadowSyncRequest(BaseModel):
    mode: Optional[str] = "full"


# --- HTML Dashboard Template ---
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    valuation = inv_mgr.get_total_inventory_valuation()
    low_stock = inv_mgr.get_low_stock_alerts()
    job_cards = srv_mgr.get_all_job_cards()
    crm_data = crm_mgr.get_predictive_service_reminders()
    po_files = sorted(list(PO_DIR.glob("*.html")), key=lambda x: x.stat().st_mtime, reverse=True)[:10]
    recent_inspections = preowned_mgr.get_all_inspections(limit=10)
    recent_expeditions = expedition_mgr.get_all_expeditions(limit=10)
    recent_restomods = restomod_mgr.get_all_restomods(limit=10)

    inspection_rows_html = ""
    for ins in recent_inspections:
        badge_cls = "bg-warning text-dark" if "PLATINUM" in ins.get("certification_tier", "") else ("bg-success text-light" if "GOLD" in ins.get("certification_tier", "") else "bg-info text-dark")
        inspection_rows_html += f"""
        <tr>
            <td><strong>{ins.get('cert_id')}</strong><br><small class='text-muted'>{ins.get('timestamp', '')[:10]}</small></td>
            <td><strong>{ins.get('bike_model')}</strong><br><small class='text-warning'><code>{ins.get('registration_no')}</code></small></td>
            <td><strong>{ins.get('customer_name')}</strong><br><small class='text-muted'>{ins.get('phone')}</small></td>
            <td><span class='badge bg-dark border border-warning text-warning fs-6'>{ins.get('total_score')}/100</span></td>
            <td><span class='badge {badge_cls}'>{ins.get('certification_tier')}</span></td>
            <td><strong>₹{ins.get('fair_market_valuation', {}).get('fair_market_value_inr', 0):,}</strong></td>
            <td>
                <a href='/certification/{ins.get('cert_id')}' target='_blank' class='btn btn-sm btn-outline-warning'>
                    <i class='fa-solid fa-certificate me-1'></i> View Shield
                </a>
            </td>
        </tr>
        """
    if not inspection_rows_html:
        inspection_rows_html = "<tr><td colspan='7' class='text-center text-muted py-3'>No inspections conducted yet. Use the form to issue first certificate.</td></tr>"

    expedition_rows_html = ""
    for exp in recent_expeditions:
        badge_cls = "bg-warning text-dark" if "LADAKH" in exp.get("clearance_tier", "") else ("bg-success text-light" if "HIGHWAY" in exp.get("clearance_tier", "") else "bg-info text-dark")
        expedition_rows_html += f"""
        <tr>
            <td><strong>{exp.get('exp_id')}</strong><br><small class='text-muted'>{exp.get('timestamp', '')[:10]}</small></td>
            <td><strong>{exp.get('bike_model')}</strong><br><small class='text-warning'><code>{exp.get('registration_no')}</code></small></td>
            <td><strong>{exp.get('rider_name')}</strong><br><small class='text-muted'>{exp.get('phone')}</small></td>
            <td><small class='text-info'>{exp.get('destination_title', '')[:25]}...</small><br><span class='text-muted'>~{exp.get('planned_km', 0):,} KM</span></td>
            <td><span class='badge bg-dark border border-warning text-warning fs-6'>{exp.get('total_score')}/100</span></td>
            <td><span class='badge {badge_cls}'>{exp.get('clearance_tier')}</span></td>
            <td>
                <a href='/expedition/{exp.get('exp_id')}' target='_blank' class='btn btn-sm btn-outline-warning'>
                    <i class='fa-solid fa-compass me-1'></i> Passport
                </a>
            </td>
        </tr>
        """
    if not expedition_rows_html:
        expedition_rows_html = "<tr><td colspan='7' class='text-center text-muted py-3'>No expedition audits recorded yet. Conduct pre-tour clearance using the form below.</td></tr>"

    restomod_rows_html = ""
    for rm in recent_restomods:
        restomod_rows_html += f"""
        <tr>
            <td><strong>{rm.get('resto_id')}</strong><br><small class='text-muted'>{rm.get('timestamp', '')[:10]}</small></td>
            <td><strong>{rm.get('bike_model')}</strong><br><small class='text-warning'><code>{rm.get('registration_no')}</code></small></td>
            <td><strong>{rm.get('customer_name')}</strong><br><small class='text-muted'>{rm.get('phone')}</small></td>
            <td><span class='badge bg-dark border border-warning text-warning'>{rm.get('style_name')}</span></td>
            <td><span class='badge bg-secondary'>{rm.get('paint_name')}</span></td>
            <td><strong class='text-warning'>₹{rm.get('grand_total', 0):,.2f}</strong><br><small class='text-muted'>{rm.get('timeline_days')} Days</small></td>
            <td>
                <a href='/restomod/{rm.get('resto_id')}' target='_blank' class='btn btn-sm btn-outline-warning'>
                    <i class='fa-solid fa-file-invoice me-1'></i> Blueprint
                </a>
            </td>
        </tr>
        """
    if not restomod_rows_html:
        restomod_rows_html = "<tr><td colspan='7' class='text-center text-muted py-3'>No custom resto-mod builds configured yet. Use the Studio to design your first build.</td></tr>"

    due_rows_html = ""
    for c in crm_data.get("due_now_customers", []):
        sent_badge = f"<span class='badge bg-success'><i class='fa-solid fa-check'></i> Sent {c['last_sent'][:10]}</span>" if c.get("last_sent") else "<span class='badge bg-secondary'>Pending</span>"
        gu_enc = c["whatsapp_gujarati"].replace("'", "\\'").replace('"', '&quot;').replace("\n", "\\n")
        en_enc = c["whatsapp_english"].replace("'", "\\'").replace('"', '&quot;').replace("\n", "\\n")
        name_esc = c["customer_name"].replace("'", "\\'")
        reg_esc = c["registration_no"].replace("'", "\\'")
        model_esc = c["bike_model"].replace("'", "\\'")
        due_rows_html += f"""
        <tr>
            <td><strong>{c['customer_name']}</strong><br><small class='text-muted'>{c['phone']}</small></td>
            <td><strong>{c['bike_model']}</strong><br><small class='text-warning'><code>{c['registration_no']}</code></small></td>
            <td><span class='badge bg-danger'>{c['days_elapsed']} Days Ago</span><br><small class='text-muted'>{c['last_service_date']}</small></td>
            <td><strong>~{c['projected_odometer_km']:,} KM</strong><br><small class='text-muted'>Base: {c['base_odometer_km']:,} KM</small></td>
            <td><span class='badge bg-dark border border-warning text-warning'>{c['health_score']}/100</span></td>
            <td>{sent_badge}</td>
            <td>
                <button class='btn btn-danger btn-sm' onclick='openWhatsAppModal(\"{name_esc}\", \"{c['phone']}\", \"{reg_esc}\", \"{model_esc}\", {c['days_elapsed']}, {c['projected_odometer_km']}, {c['health_score']}, \"{gu_enc}\", \"{en_enc}\")'>
                    <i class='fa-brands fa-whatsapp me-1'></i> Send Reminder
                </button>
            </td>
        </tr>
        """

    upcoming_rows_html = ""
    for c in crm_data.get("upcoming_customers", []):
        gu_enc = c["whatsapp_gujarati"].replace("'", "\\'").replace('"', '&quot;').replace("\n", "\\n")
        en_enc = c["whatsapp_english"].replace("'", "\\'").replace('"', '&quot;').replace("\n", "\\n")
        name_esc = c["customer_name"].replace("'", "\\'")
        reg_esc = c["registration_no"].replace("'", "\\'")
        model_esc = c["bike_model"].replace("'", "\\'")
        upcoming_rows_html += f"""
        <tr>
            <td><strong>{c['customer_name']}</strong><br><small class='text-muted'>{c['phone']}</small></td>
            <td><strong>{c['bike_model']}</strong><br><small class='text-warning'><code>{c['registration_no']}</code></small></td>
            <td><span class='badge bg-warning text-dark'>{c['days_elapsed']} Days Ago</span><br><small class='text-muted'>{c['last_service_date']}</small></td>
            <td><strong>~{c['projected_odometer_km']:,} KM</strong></td>
            <td><span class='badge bg-dark border border-secondary text-light'>{c['health_score']}/100</span></td>
            <td>
                <button class='btn btn-outline-warning btn-sm' onclick='openWhatsAppModal(\"{name_esc}\", \"{c['phone']}\", \"{reg_esc}\", \"{model_esc}\", {c['days_elapsed']}, {c['projected_odometer_km']}, {c['health_score']}, \"{gu_enc}\", \"{en_enc}\")'>
                    <i class='fa-brands fa-whatsapp me-1'></i> Preemptive Msg
                </button>
            </td>
        </tr>
        """

    po_rows_html = ""
    for pf in po_files:
        po_num = pf.stem
        po_rows_html += f"""
        <tr>
            <td><code>{po_num}</code></td>
            <td>Official Wholesale Replenishment PO</td>
            <td><a href='/po/{po_num}' target='_blank' class='btn btn-outline-warning btn-sm'><i class='fa-solid fa-eye me-1'></i> View PO</a></td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chamunda AI • Royal Enfield Specialist OS</title>
    <!-- PWA & Mobile Web App Manifest -->
    <link rel="manifest" href="/static/manifest.json">
    <meta name="theme-color" content="#f39c12">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Chamunda RE">
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
    <script>
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/static/sw.js')
                    .then(reg => console.log('PWA Service Worker registered:', reg.scope))
                    .catch(err => console.log('PWA Service Worker failed:', err));
            }});
        }}
    </script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --gold: #D4AF37;
            --gold-bright: #F5D76E;
            --dark-green: #0d2b22;
            --forest-green: #1b4d3e;
            --dark-bg: #091713;
            --card-bg: #11221c;
            --card-border: #1d382e;
            --text-light: #e6edf3;
            --text-dim: #8b949e;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            background-color: var(--dark-bg);
            color: var(--text-light);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            min-height: 100vh;
        }}
        .navbar-custom {{
            background: linear-gradient(135deg, #071712, #123328);
            border-bottom: 2px solid var(--gold);
            padding: 12px 24px;
        }}
        .brand-title {{
            color: var(--gold);
            font-weight: 800;
            letter-spacing: 1.5px;
            font-size: 20px;
        }}
        .nav-tabs .nav-link {{
            color: var(--text-dim);
            font-weight: 600;
            border: none;
            padding: 12px 18px;
            transition: all 0.2s;
        }}
        .nav-tabs .nav-link:hover {{
            color: var(--gold-bright);
        }}
        .nav-tabs .nav-link.active {{
            color: #000;
            background-color: var(--gold);
            border-radius: 6px 6px 0 0;
            font-weight: 700;
        }}
        .card-custom {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.3);
        }}
        .metric-val {{
            font-size: 26px;
            font-weight: 800;
            color: var(--gold);
        }}
        .btn-gold {{
            background: linear-gradient(135deg, var(--gold), var(--gold-bright));
            color: #000;
            font-weight: 700;
            border: none;
            transition: all 0.2s;
        }}
        .btn-gold:hover {{
            background: linear-gradient(135deg, var(--gold-bright), #fff);
            color: #000;
            transform: translateY(-1px);
        }}
        .waveform-canvas {{
            width: 100%;
            height: 90px;
            background: #060e0b;
            border-radius: 8px;
            border: 1px solid var(--card-border);
        }}
        .badge-status {{
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 700;
            border-radius: 4px;
        }}
        .table-custom {{
            color: var(--text-light);
            background: transparent;
        }}
        .table-custom th {{
            background: #0c1c16;
            color: var(--gold);
            font-size: 12px;
            text-transform: uppercase;
            border-color: var(--card-border);
        }}
        .table-custom td {{
            border-color: var(--card-border);
            vertical-align: middle;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="/">
                <span class="fs-4 me-2">👑</span>
                <div>
                    <div class="brand-title">CHAMUNDA AUTOMOBILE</div>
                    <small style="font-size: 10px; color: var(--gold-bright); letter-spacing: 1px;">PARTS & SERVICE • ROYAL ENFIELD SPECIALISTS</small>
                </div>
            </a>
            <div class="d-flex align-items-center gap-3">
                <button class="btn btn-warning btn-sm fw-bold px-3 py-2 shadow-sm" onclick="openPOSModal()">
                    <i class="fa-solid fa-cash-register me-1"></i> Quick Counter POS (Dynamic UPI QR)
                </button>
                <span class="badge bg-dark border border-warning text-warning px-3 py-2">
                    <i class="fa-solid fa-microchip me-1"></i> Aradhya AI Active
                </span>
                <span class="badge bg-success px-3 py-2">
                    <i class="fa-solid fa-signal me-1"></i> Workshop Node Online
                </span>
            </div>
        </div>
    </nav>

    <div class="container-fluid px-4 py-4">
        <!-- Alpesh Sir Omni-Control Center & Live Command Strip -->
        <div class="card card-custom p-3 mb-4 border border-warning shadow-lg" style="background: linear-gradient(135deg, rgba(20,25,22,0.95), rgba(35,28,12,0.95));">
            <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                <div class="d-flex align-items-center gap-2">
                    <span class="fs-4">👑</span>
                    <div>
                        <strong class="text-warning fs-6">Alpesh Sir • Supreme Omni-Control Center (ઓમ્ની કંટ્રોલ ટર્મિનલ)</strong>
                        <small class="text-muted d-block">Issue written commands to all 5 shop sub-agents, workshop bays, cloud branches &amp; diagnostic engines</small>
                    </div>
                </div>
                <div class="d-flex align-items-center gap-2">
                    <span class="badge bg-gold text-dark fw-bold px-2 py-1"><i class="fa-solid fa-crown me-1"></i> Chairman &amp; Master Tech</span>
                    <span class="badge bg-dark border border-warning text-warning px-2 py-1"><i class="fa-solid fa-robot me-1"></i> CEO Aradhya Online</span>
                </div>
            </div>

            <!-- Input bar with priority and execute button -->
            <div class="row g-2 align-items-center">
                <div class="col-md-8">
                    <div class="input-group">
                        <span class="input-group-text bg-black text-warning border-secondary"><i class="fa-solid fa-terminal"></i></span>
                        <input type="text" id="globalOmniCommandInput" class="form-control bg-black text-light border-secondary" placeholder="Type any directive in Gujarati or English (e.g. 'રમેશભાઈ, બે 1 માં ટેપેટ ટ્યુનિંગ કરો', 'જયેશભાઈ, ઓઇલ ફિલ્ટર સ્ટોક બતાવો', 'પાટણ બ્રાન્ચ માટે 2x કેમશાફ્ટ ટ્રાન્સફર કરો')..." onkeydown="if(event.key==='Enter') submitGlobalOmniCommand()">
                    </div>
                </div>
                <div class="col-md-2">
                    <select id="globalOmniPriority" class="form-select bg-black text-warning border-secondary">
                        <option value="Normal">Normal Priority</option>
                        <option value="High" selected>High Priority</option>
                        <option value="Urgent">⚡ Urgent Priority</option>
                    </select>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-warning w-100 fw-bold" id="btnGlobalOmniSubmit" onclick="submitGlobalOmniCommand()">
                        <i class="fa-solid fa-paper-plane me-1"></i> Execute
                    </button>
                </div>
            </div>

            <!-- 1-Click Quick Subsystem Jump Controls -->
            <div class="d-flex flex-wrap gap-2 mt-2 align-items-center pt-2 border-top border-secondary">
                <small class="text-muted"><i class="fa-solid fa-sliders text-warning me-1"></i> Quick Control Jumps:</small>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="setAndRunGlobalCommand('રમેશભાઈ, વર્કશોપ બે અને ટેપેટ સાઉન્ડ સ્ટેટસ બતાવો', 'High')">
                    🛠️ Bay Chief (Ramesh)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="setAndRunGlobalCommand('જયેશભાઈ, 4,469 પાર્ટ્સમાંથી લો-સ્ટોક ફિલ્ટર કરો અને PO તૈયાર કરો', 'Urgent')">
                    📦 Parts Specialist (Jayesh)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="setAndRunGlobalCommand('પ્રિયા, આજના પેન્ડિંગ કસ્ટમર વ્હોટ્સએપ રીમાઇન્ડર્સ મોકલો (+91 78747 19139)', 'High')">
                    💬 Receptionist (Priya)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="setAndRunGlobalCommand('કબીર, 5 સોશિયલ ચેનલ્સ અને ગૂગલ રિવ્યુઝ સિન્ડિકેટ કરો', 'Normal')">
                    📱 Social Growth (Kabir)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="setAndRunGlobalCommand('હસમુખભાઈ, આજનું જીએસટી સેલ્સ લેજર અને કાઉન્ટર કેશ મેળવો', 'High')">
                    🧾 Accounts (Hasmukh)
                </button>
                <button class="btn btn-xs btn-outline-info py-1 px-2 small" onclick="document.getElementById('obd-tab').click()">
                    🔌 OBD-II Scanner
                </button>
                <button class="btn btn-xs btn-outline-info py-1 px-2 small" onclick="document.getElementById('schematics-tab').click()">
                    🧩 3D Schematics
                </button>
                <button class="btn btn-xs btn-outline-danger py-1 px-2 small" onclick="document.getElementById('borescope-tab').click()">
                    🔬 Borescope
                </button>
                <button class="btn btn-xs btn-outline-success py-1 px-2 small" onclick="document.getElementById('multibranch-tab').click()">
                    🏢 5 Branches Hub
                </button>
                <button class="btn btn-xs btn-outline-info py-1 px-2 small" onclick="document.getElementById('webar-tab').click()">
                    👁️ WebAR Guide
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="document.getElementById('night-locker-tab').click()">
                    🌙 24/7 Night Locker
                </button>
                <button class="btn btn-xs btn-outline-primary py-1 px-2 small" onclick="document.getElementById('cloud-shadow-tab').click()">
                    ☁️ Cloud Shadow (Offline)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small" onclick="document.getElementById('kalpavriksha-tab').click()">
                    🌳 Kalpavriksha (Growth)
                </button>
                <button class="btn btn-xs btn-outline-warning py-1 px-2 small fw-bold" onclick="document.getElementById('dms-tab').click()">
                    🏢 RE-DMS Suite
                </button>
                <button class="btn btn-xs btn-primary py-1 px-2 small fw-bold" onclick="triggerCloudShadowSync()" title="Force immediate local-to-cloud snapshot sync">
                    🔄 Cloud Sync
                </button>
                <button class="btn btn-xs btn-danger py-1 px-2 small fw-bold" onclick="triggerTurboBoost()" title="Clean background processes, trim memory & eliminate lag">
                    🚀 Turbo Boost (Fix Lag)
                </button>
            </div>

            <!-- Execution Result Alert Box -->
            <div id="globalOmniResultBox" class="mt-3 p-3 bg-black rounded border border-warning text-light" style="display: none;">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <strong class="text-warning" id="globalOmniResultTitle">Directive Executed</strong>
                    <span class="badge bg-warning text-dark fw-bold" id="globalOmniResultAgent"></span>
                </div>
                <div class="small text-light mb-1" id="globalOmniResultSummary"></div>
                <div class="small text-warning" id="globalOmniResultGu"></div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs border-0 mb-4" id="portalTabs" role="tablist">
            <li class="nav-item">
                <button class="nav-link active" id="overview-tab" data-bs-toggle="tab" data-bs-target="#overview" type="button">
                    <i class="fa-solid fa-chart-pie me-2"></i>Executive Overview
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="diagnostics-tab" data-bs-toggle="tab" data-bs-target="#sound-bay" type="button">
                    <i class="fa-solid fa-wave-square me-2"></i>Live Sound Diagnostic Bay &amp; Thump Tuner
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="parts-tab" data-bs-toggle="tab" data-bs-target="#parts-catalog" type="button">
                    <i class="fa-solid fa-boxes-stacked me-2"></i>4,469 Parts Dynamic Filter
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="service-tab" data-bs-toggle="tab" data-bs-target="#service-bays" type="button">
                    <i class="fa-solid fa-motorcycle me-2"></i>Service Bays & QR Invoicing
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="intake-tab" data-bs-toggle="tab" data-bs-target="#bike-intake" type="button">
                    <i class="fa-solid fa-plus-circle me-2"></i>New Bike Intake
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="crm-tab" data-bs-toggle="tab" data-bs-target="#crm-reminders" type="button">
                    <i class="fa-solid fa-clock-rotate-left me-2"></i>Smart Reminders & CRM
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="bot-tab" data-bs-toggle="tab" data-bs-target="#customer-bot" type="button">
                    <i class="fa-solid fa-comments me-2"></i>24/7 WhatsApp Bot & Live Tracker
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="preowned-tab" data-bs-toggle="tab" data-bs-target="#preowned-inspection" type="button">
                    <i class="fa-solid fa-shield-halved me-2"></i>Certified Pre-Owned Inspection
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="expedition-tab" data-bs-toggle="tab" data-bs-target="#expedition-sos" type="button">
                    <i class="fa-solid fa-compass me-2"></i>Expedition Readiness &amp; Highway SOS
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="restomod-tab" data-bs-toggle="tab" data-bs-target="#custom-studio" type="button">
                    <i class="fa-solid fa-screwdriver-wrench me-2"></i>Custom Resto-Mod &amp; Vintage CI Studio
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="social-tab" data-bs-toggle="tab" data-bs-target="#omnichannel-social" type="button">
                    <i class="fa-solid fa-share-nodes me-2"></i>360° Social &amp; Brand Hub
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="agents-tab" data-bs-toggle="tab" data-bs-target="#shop-subagents" type="button">
                    <i class="fa-solid fa-users-gear me-2"></i>Executive Sub-Agents
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="bay-voice-tab" data-bs-toggle="tab" data-bs-target="#bay-voice" type="button">
                    <i class="fa-solid fa-microphone-lines me-2 text-warning"></i>🎙️ Hands-Free Bay Voice
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="b2b-wholesale-tab" data-bs-toggle="tab" data-bs-target="#b2b-wholesale" type="button">
                    <i class="fa-solid fa-boxes-packing me-2 text-info"></i>📦 B2B Spares Wholesale
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="riders-club-tab" data-bs-toggle="tab" data-bs-target="#riders-club" type="button">
                    <i class="fa-solid fa-motorcycle me-2 text-danger"></i>🏍️ Riders Club &amp; AMC
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="obd-tab" data-bs-toggle="tab" data-bs-target="#obd-scanner" type="button">
                    <i class="fa-solid fa-microchip me-2 text-info"></i>🔌 OBD-II IoT Scanner
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="kiosk-tab" data-bs-toggle="tab" data-bs-target="#smart-kiosk" type="button">
                    <i class="fa-solid fa-desktop me-2 text-warning"></i>🖥️ Smart Lounge Kiosk
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="supply-chain-tab" data-bs-toggle="tab" data-bs-target="#supply-chain" type="button">
                    <i class="fa-solid fa-chart-line me-2 text-success"></i>📈 Predictive Supply Chain
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="schematics-tab" data-bs-toggle="tab" data-bs-target="#engine-schematics" type="button">
                    <i class="fa-solid fa-cubes-stacked me-2 text-warning"></i>🧩 3D Schematics &amp; Torque
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="borescope-tab" data-bs-toggle="tab" data-bs-target="#borescope-inspection" type="button">
                    <i class="fa-solid fa-microscope me-2 text-danger"></i>🔬 AI Borescope Endoscopy
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="multibranch-tab" data-bs-toggle="tab" data-bs-target="#multibranch-hub" type="button">
                    <i class="fa-solid fa-network-wired me-2 text-info"></i>🏢 Multi-Branch Cloud Hub
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="webar-tab" data-bs-toggle="tab" data-bs-target="#webar-guide" type="button">
                    <i class="fa-solid fa-eye me-2 text-warning"></i>👁️ WebAR Engine Guide
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="night-locker-tab" data-bs-toggle="tab" data-bs-target="#night-locker" type="button">
                    <i class="fa-solid fa-moon me-2 text-info"></i>🌙 24/7 Night Highway Locker
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="cloud-shadow-tab" data-bs-toggle="tab" data-bs-target="#cloud-shadow" type="button">
                    <i class="fa-solid fa-cloud me-2 text-primary"></i>☁️ Cloud Shadow (Offline Mirror)
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="kalpavriksha-tab" data-bs-toggle="tab" data-bs-target="#kalpavriksha" type="button">
                    <i class="fa-solid fa-tree me-2 text-warning"></i>🌳 Kalpavriksha (Virtual Growth &amp; Mastery)
                </button>
            </li>
            <li class="nav-item">
                <button class="nav-link" id="dms-tab" data-bs-toggle="tab" data-bs-target="#dms" type="button">
                    <i class="fa-solid fa-building me-2 text-warning"></i>🏢 RE-DMS Suite (Billing • Daybook • CRM)
                </button>
            </li>
        </ul>

        <div class="tab-content" id="portalTabContent">
            <!-- ============================================================= -->
            <!-- TAB 1: EXECUTIVE OVERVIEW -->
            <!-- ============================================================= -->
            <div class="tab-pane fade show active" id="overview" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3">
                            <small class="text-muted text-uppercase fw-bold">Genuine OEM SKUs</small>
                            <div class="metric-val">{valuation['total_distinct_skus']:,}</div>
                            <small class="text-success"><i class="fa-solid fa-check"></i> Authentic spares.royalenfield.com</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3">
                            <small class="text-muted text-muted text-uppercase fw-bold">Total Units in Stock</small>
                            <div class="metric-val">{valuation['total_units_in_stock']:,} Pcs</div>
                            <small class="text-light opacity-75">Wholesale: ₹{valuation['cost_valuation_inr']:,}</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3">
                            <small class="text-muted text-uppercase fw-bold">Retail Inventory Valuation (MRP)</small>
                            <div class="metric-val">₹{valuation['mrp_valuation_inr']:,}</div>
                            <small class="text-warning">Gross Margin: ₹{valuation['expected_gross_profit_inr']:,}</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3">
                            <small class="text-muted text-uppercase fw-bold">Active Service Job Cards</small>
                            <div class="metric-val">{len(job_cards)} Bikes</div>
                            <small class="text-info"><i class="fa-solid fa-wrench"></i> In Service & Delivery Flow</small>
                        </div>
                    </div>
                </div>

                <div class="row g-4">
                    <div class="col-md-8">
                        <div class="card card-custom p-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="text-warning mb-0"><i class="fa-solid fa-bell me-2"></i>Critical Low-Stock Reorder Alerts</h5>
                                <span class="badge bg-danger">{len(low_stock)} Items Below Threshold</span>
                            </div>
                            <div class="table-responsive" style="max-height: 380px;">
                                <table class="table table-custom">
                                    <thead>
                                        <tr>
                                            <th>Part Number</th>
                                            <th>Description</th>
                                            <th>Category</th>
                                            <th>Stock</th>
                                            <th>Min</th>
                                            <th>Bin</th>
                                            <th>MRP</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {"".join(f'''<tr>
                                            <td><code>{p.get("part_number", p.get("oem_number"))}</code></td>
                                            <td><strong>{p.get("name")}</strong></td>
                                            <td><small>{p.get("category")}</small></td>
                                            <td class="text-danger fw-bold">{p.get("stock", 0)}</td>
                                            <td>{p.get("min_threshold", 5)}</td>
                                            <td><code>{p.get("bin_location", "A-01")}</code></td>
                                            <td>₹{p.get("mrp", 0)}</td>
                                        </tr>''' for p in low_stock[:15])}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card card-custom p-4 h-100">
                            <h5 class="text-warning mb-3"><i class="fa-solid fa-lightbulb me-2"></i>Executive AI Directives</h5>
                            <div class="p-3 mb-3" style="background: #0a1b15; border-left: 4px solid var(--gold); border-radius: 4px;">
                                <strong>🎙️ Acoustic Health Passport Adoption:</strong>
                                <p class="small text-muted mb-0">Attach verifiable QR certificates on 100% of Hunter 350 & Classic 350 deliveries to build customer trust.</p>
                            </div>
                            <div class="p-3 mb-3" style="background: #0a1b15; border-left: 4px solid #10b981; border-radius: 4px;">
                                <strong>⚡ Fast-Moving Parts Optimization:</strong>
                                <p class="small text-muted mb-0">Brake pads and Motul 7100 15W-50 inventory turning every 6 days. Automated reorder suggested.</p>
                            </div>
                            <div class="p-3" style="background: #0a1b15; border-left: 4px solid #3b82f6; border-radius: 4px;">
                                <strong>📱 Customer WhatsApp Auto-Dispatch:</strong>
                                <p class="small text-muted mb-0">One-click bilingual broadcast ready for every completed job card.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 2: LIVE SOUND DIAGNOSTIC BAY -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="sound-bay" role="tabpanel">
                <div class="card card-custom p-4">
                    <div class="row align-items-center mb-3">
                        <div class="col-md-8">
                            <h4 class="text-warning mb-1"><i class="fa-solid fa-microphone-lines me-2"></i>Live Engine Sound Diagnostic Bay</h4>
                            <p class="text-muted small mb-0">Fast Fourier Transform (FFT) Harmonics Spectrum Analyzer for Tappets, Timing Chains, Clutch & Exhaust</p>
                        </div>
                        <div class="col-md-4 text-end">
                            <span class="badge bg-dark border border-warning text-warning p-2">
                                <i class="fa-solid fa-shield-halved"></i> 100% Factory Tolerance Verified
                            </span>
                        </div>
                    </div>

                    <!-- Controls & Visualizer -->
                    <div class="row g-3 mb-4">
                        <div class="col-md-3">
                            <label class="form-label text-muted small">Select Motorcycle Model</label>
                            <select id="diagModel" class="form-select bg-dark text-light border-secondary">
                                <option value="Hunter 350">Hunter 350 (J-Series)</option>
                                <option value="Classic 350">Classic 350 Reborn</option>
                                <option value="Meteor 350">Meteor 350</option>
                                <option value="Bullet 350">Bullet 350</option>
                                <option value="Himalayan 450">Himalayan 450 (Sherpa)</option>
                                <option value="Interceptor 650">Interceptor 650 (Twin)</option>
                                <option value="Continental GT 650">Continental GT 650</option>
                            </select>
                        </div>
                        <div class="col-md-9 d-flex align-items-end gap-2 flex-wrap">
                            <button class="btn btn-gold px-4 py-2" id="btnLiveListen" onclick="startLiveListening()">
                                <i class="fa-solid fa-microphone me-1"></i> Start 5s Live Mic Listening
                            </button>
                            <div class="btn-group">
                                <button type="button" class="btn btn-outline-warning dropdown-toggle" data-bs-toggle="dropdown">
                                    <i class="fa-solid fa-vial me-1"></i> Simulate Test Profile
                                </button>
                                <ul class="dropdown-menu dropdown-menu-dark">
                                    <li><a class="dropdown-item" href="javascript:void(0)" onclick="runSimulatedSound('tappet')">⚠️ Tappet / Valve Clearance Clatter</a></li>
                                    <li><a class="dropdown-item" href="javascript:void(0)" onclick="runSimulatedSound('chain')">⚠️ Cam Timing Chain Slack Rattle</a></li>
                                    <li><a class="dropdown-item" href="javascript:void(0)" onclick="runSimulatedSound('clutch')">⚠️ Primary Drive / Clutch Whine</a></li>
                                    <li><a class="dropdown-item" href="javascript:void(0)" onclick="runSimulatedSound('piston')">⚠️ Piston Skirt Play Knock</a></li>
                                    <li><a class="dropdown-item" href="javascript:void(0)" onclick="runSimulatedSound('exhaust')">⚠️ Exhaust Flange Leak Turbulence</a></li>
                                    <li><hr class="dropdown-divider"></li>
                                    <li><a class="dropdown-item text-success" href="javascript:void(0)" onclick="runSimulatedSound('healthy')">✅ Healthy Engine (Showroom Mint)</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Waveform Animation -->
                    <div class="mb-4">
                        <div class="d-flex justify-content-between text-muted small mb-1">
                            <span><i class="fa-solid fa-wave-square me-1"></i> Real-Time Acoustic Waveform Spectrum</span>
                            <span id="audioStatusText">Standing by for audio stream...</span>
                        </div>
                        <canvas id="waveformCanvas" class="waveform-canvas"></canvas>
                    </div>

                    <!-- Results Container -->
                    <div id="diagResultsContainer" class="d-none">
                        <div class="row g-3">
                            <!-- Telemetry & Health Score -->
                            <div class="col-md-4">
                                <div class="card bg-dark border-secondary p-3 h-100">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span class="text-muted small">Diagnostic ID</span>
                                        <code id="repDiagId" class="text-warning"></code>
                                    </div>
                                    <div class="text-center my-3">
                                        <div id="repHealthScore" style="font-size: 42px; font-weight: 800;"></div>
                                        <div id="repHealthStatus" class="fw-bold mt-1"></div>
                                    </div>
                                    <hr class="border-secondary my-2">
                                    <div class="d-flex justify-content-between small text-muted">
                                        <span>Idle Rhythm:</span>
                                        <strong id="repRhythm" class="text-light"></strong>
                                    </div>
                                    <div class="d-flex justify-content-between small text-muted mt-1">
                                        <span>Sound Level:</span>
                                        <strong id="repDb" class="text-light"></strong>
                                    </div>
                                    <div class="d-flex justify-content-between small text-muted mt-1">
                                        <span>Audio Source:</span>
                                        <strong id="repSource" class="text-light"></strong>
                                    </div>
                                </div>
                            </div>

                            <!-- Anomalies & Gujarati Summary -->
                            <div class="col-md-8">
                                <div class="card bg-dark border-secondary p-3 h-100">
                                    <h6 class="text-warning mb-2"><i class="fa-solid fa-clipboard-list me-2"></i>Acoustic Analysis & Recommendations</h6>
                                    <div class="p-2 mb-3 rounded" style="background: #0c1c16; border-left: 3px solid var(--gold);">
                                        <strong class="text-warning">સારાંશ (Gujarati):</strong>
                                        <div id="repSummaryGu" class="small mt-1 text-light"></div>
                                    </div>
                                    <div id="repAnomaliesList"></div>
                                </div>
                            </div>

                            <!-- Recommended Parts -->
                            <div class="col-12 mt-3">
                                <div class="card bg-dark border-secondary p-3">
                                    <h6 class="text-warning mb-3">
                                        <i class="fa-solid fa-wrench me-2"></i>Auto-Matched Genuine OEM Parts from 4,469 Catalog
                                    </h6>
                                    <div id="repMatchedParts"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ROYAL ENFIELD ICONIC THUMP TUNER & ACOUSTIC CALIBRATOR -->
                    <div class="card bg-black border-warning mt-4 p-4 shadow">
                        <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                            <div>
                                <h5 class="text-warning mb-1">
                                    <i class="fa-solid fa-compact-disc me-2"></i>Royal Enfield Authentic Thump Tuner &amp; Acoustic Resonance Calibrator
                                </h5>
                                <small class="text-muted">ઓથેન્ટિક ડુગ-ડુગ થમ્પ વિશ્લેષણ • Sub-bass FFT Harmonics (30 - 250 Hz) • RTO Decibel Compliance (&lt;85 dB) • Valve Clearance Directives</small>
                            </div>
                            <span class="badge bg-warning text-dark px-3 py-2 fw-bold">
                                <i class="fa-solid fa-crown me-1"></i> Heritage Sound Engineering
                            </span>
                        </div>

                        <div class="row g-3 align-items-end mb-3">
                            <div class="col-md-4">
                                <label class="form-label text-muted small fw-bold">Target Acoustic Thump Profile</label>
                                <select id="thumpProfileSelect" class="form-select bg-dark text-light border-secondary">
                                    <option value="deep_vintage_chug">Iconic Cast-Iron Heavy Rhythm Chug (ઓથેન્ટિક ડુગ-ડુગ)</option>
                                    <option value="factory_oem_clean">BS6 J-Series Showroom Balanced Thump (શોરૂમ સ્મૂથ)</option>
                                    <option value="cruiser_bass_rumble">Classic &amp; Meteor 350 Highway Bass Rumble (હાઇવે રમ્બલ)</option>
                                    <option value="sherpa_highland_growl">Himalayan 450 Highland Throaty Growl (શેરપા ગ્રોલ)</option>
                                    <option value="twin_270_crossplane_roar">Interceptor 650 Twin 270° Crossplane Roar (ટ્વિન રોઅર)</option>
                                </select>
                            </div>
                            <div class="col-md-3">
                                <label class="form-label text-muted small fw-bold">Motorcycle Model</label>
                                <select id="thumpModelSelect" class="form-select bg-dark text-light border-secondary">
                                    <option value="Classic 350">Classic 350 Reborn</option>
                                    <option value="Bullet 350">Bullet 350 (Cast Iron / UCE / J-Series)</option>
                                    <option value="Hunter 350">Hunter 350</option>
                                    <option value="Meteor 350">Meteor 350</option>
                                    <option value="Himalayan 450">Himalayan 450 (Sherpa)</option>
                                    <option value="Interceptor 650">Interceptor 650 Twin</option>
                                </select>
                            </div>
                            <div class="col-md-5">
                                <button class="btn btn-gold px-4 py-2 w-100 fw-bold" onclick="runThumpAnalysis()">
                                    <i class="fa-solid fa-sliders me-2"></i> Calibrate &amp; Measure Iconic Thump
                                </button>
                            </div>
                        </div>

                        <!-- Thump Analysis Results Display -->
                        <div id="thumpResultsBox" class="p-3 rounded mt-2 border border-secondary" style="background: #091a14; display: none;">
                            <div class="row g-3">
                                <div class="col-md-3 text-center border-end border-secondary">
                                    <small class="text-muted text-uppercase fw-bold">Thump Score</small>
                                    <div id="thumpScoreVal" style="font-size: 38px; font-weight: 800; color: var(--gold);">--</div>
                                    <div id="thumpRatingBadge" class="badge bg-warning text-dark mt-1"></div>
                                </div>
                                <div class="col-md-3 text-center border-end border-secondary">
                                    <small class="text-muted text-uppercase fw-bold">Dominant Sub-Bass</small>
                                    <div id="thumpHzVal" style="font-size: 32px; font-weight: 700; color: #10b981;">-- Hz</div>
                                    <small class="text-muted">Resonance Band (30-90Hz)</small>
                                </div>
                                <div class="col-md-3 text-center border-end border-secondary">
                                    <small class="text-muted text-uppercase fw-bold">Cadence Idle Rhythm</small>
                                    <div id="thumpRpmVal" style="font-size: 32px; font-weight: 700; color: #60a5fa;">-- RPM</div>
                                    <small class="text-muted">Exhaust Stroke Pulse</small>
                                </div>
                                <div class="col-md-3 text-center">
                                    <small class="text-muted text-uppercase fw-bold">Sound Level &amp; Legal</small>
                                    <div id="thumpDbVal" style="font-size: 32px; font-weight: 700; color: #f59e0b;">-- dB</div>
                                    <span id="thumpLegalBadge" class="badge bg-success">RTO Legal (&lt;85 dB)</span>
                                </div>

                                <div class="col-12 mt-2">
                                    <div class="p-2 rounded bg-dark border-start border-warning border-3">
                                        <strong class="text-warning"><i class="fa-solid fa-circle-info me-1"></i> ગુજરાતી તારણ:</strong>
                                        <span id="thumpSummaryGu" class="ms-2 text-light small"></span>
                                    </div>
                                </div>

                                <div class="col-12 mt-2">
                                    <h6 class="text-warning mb-2"><i class="fa-solid fa-wrench me-1"></i> Master Mechanic Step-by-Step Directives:</h6>
                                    <div id="thumpDirectivesList" class="small text-light"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 3: 4,469 PARTS DYNAMIC FILTER -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="parts-catalog" role="tabpanel">
                <div class="card card-custom p-4">
                    <div class="row g-3 mb-3">
                        <div class="col-md-4">
                            <label class="form-label text-muted small">Search by Name / SKU / Keyword</label>
                            <input type="text" id="filterQuery" class="form-control bg-dark text-light border-secondary" placeholder="e.g. brake pad, RAM00012, oil filter...">
                        </div>
                        <div class="col-md-2">
                            <label class="form-label text-muted small">Bike Model</label>
                            <select id="filterModel" class="form-select bg-dark text-light border-secondary">
                                <option value="">All RE Models</option>
                                <option value="Hunter 350">Hunter 350</option>
                                <option value="Classic 350">Classic 350</option>
                                <option value="Meteor 350">Meteor 350</option>
                                <option value="Bullet 350">Bullet 350</option>
                                <option value="Himalayan 450">Himalayan 450</option>
                                <option value="Interceptor 650">Interceptor 650</option>
                                <option value="Continental GT 650">Continental GT 650</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label text-muted small">Category</label>
                            <select id="filterCategory" class="form-select bg-dark text-light border-secondary">
                                <option value="">All Categories</option>
                                <option value="Periodic Service">Periodic Service</option>
                                <option value="Braking System">Braking System</option>
                                <option value="Engine & Transmission">Engine & Transmission</option>
                                <option value="Electrical & Ignition">Electrical & Ignition</option>
                                <option value="Suspension">Suspension & Steering</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <label class="form-label text-muted small">Stock Status</label>
                            <select id="filterStockStatus" class="form-select bg-dark text-light border-secondary">
                                <option value="all">All Inventory</option>
                                <option value="in_stock">In Stock Only</option>
                                <option value="low_stock">Low Stock (≤5)</option>
                                <option value="out_of_stock">Out of Stock</option>
                            </select>
                        </div>
                        <div class="col-md-2 d-flex align-items-end">
                            <button class="btn btn-gold w-100" onclick="applyPartsFilter()">
                                <i class="fa-solid fa-filter me-1"></i> Filter Parts
                            </button>
                        </div>
                    </div>

                    <div class="table-responsive" style="max-height: 520px;">
                        <table class="table table-custom table-hover" id="filteredPartsTable">
                            <thead>
                                <tr>
                                    <th>OEM Part No</th>
                                    <th>Part Description</th>
                                    <th>Category</th>
                                    <th>MRP</th>
                                    <th>Cost</th>
                                    <th>Stock</th>
                                    <th>Bin</th>
                                    <th>Compatible Models</th>
                                </tr>
                            </thead>
                            <tbody id="partsTableBody">
                                <tr>
                                    <td colspan="8" class="text-center py-4 text-muted">
                                        <i class="fa-solid fa-spinner fa-spin me-2"></i> Loading parts catalog...
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 4: SERVICE BAYS & QR INVOICING -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="service-bays" role="tabpanel">
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-warning mb-0"><i class="fa-solid fa-list-check me-2"></i>Active Job Cards & One-Click QR Invoicing</h5>
                        <button class="btn btn-sm btn-outline-warning" onclick="location.reload()">
                            <i class="fa-solid fa-rotate me-1"></i> Refresh Bay Status
                        </button>
                    </div>

                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>Job Card ID</th>
                                    <th>Customer</th>
                                    <th>Bike Model</th>
                                    <th>Registration</th>
                                    <th>Stage &amp; Progress</th>
                                    <th>Status</th>
                                    <th>Est. Total</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {"".join(f'''<tr>
                                    <td><code>{c["job_card_id"]}</code></td>
                                    <td><strong>{c["customer_name"]}</strong><br><small class="text-muted">{c.get("phone", "")}</small></td>
                                    <td><span class="badge bg-dark border border-warning text-warning">{c["bike_model"]}</span></td>
                                    <td><strong>{c["registration_no"]}</strong><br><small class="text-muted">{c.get("odometer_km", 0):,} KM</small></td>
                                    <td>
                                        <span class="badge bg-info text-dark fw-bold mb-1">
                                            {c.get("current_stage") or (c["status"] == "Completed" and "Ready for Delivery" or "Service Bay Work")}
                                        </span>
                                        <div class="dropdown">
                                            <button class="btn btn-outline-secondary btn-sm dropdown-toggle py-0" style="font-size: 11px;" type="button" data-bs-toggle="dropdown">
                                                Update Stage
                                            </button>
                                            <ul class="dropdown-menu dropdown-menu-dark">
                                                <li><a class="dropdown-item small" href="javascript:void(0)" onclick="updateJobStage('{c["job_card_id"]}', 'Vehicle Intake & Check-in')">📥 1. Vehicle Intake</a></li>
                                                <li><a class="dropdown-item small" href="javascript:void(0)" onclick="updateJobStage('{c["job_card_id"]}', '50-Point Inspection & Tappet Check')">🔍 2. 50-Pt Inspection</a></li>
                                                <li><a class="dropdown-item small" href="javascript:void(0)" onclick="updateJobStage('{c["job_card_id"]}', 'Service Bay Work & Part Replacement')">⚙️ 3. Bay Engine Work</a></li>
                                                <li><a class="dropdown-item small" href="javascript:void(0)" onclick="updateJobStage('{c["job_card_id"]}', 'Foam Wash, Polishing & Detailing')">✨ 4. Foam Wash & Polish</a></li>
                                                <li><a class="dropdown-item small" href="javascript:void(0)" onclick="updateJobStage('{c["job_card_id"]}', 'Final Quality Audit & Ready for Delivery')">🏁 5. Ready for Delivery</a></li>
                                            </ul>
                                        </div>
                                    </td>
                                    <td>
                                        <span class="badge {c["status"] == "Completed" and "bg-success" or "bg-warning text-dark"}">
                                            {c["status"]}
                                        </span>
                                    </td>
                                    <td class="fw-bold text-warning">₹{c.get("total_amount", 500):,}</td>
                                    <td>
                                        <div class="btn-group btn-group-sm">
                                            <button class="btn btn-gold" onclick="completeAndBillJob('{c["job_card_id"]}')" title="Complete job and issue QR Tax Invoice">
                                                <i class="fa-solid fa-receipt me-1"></i> Complete & Bill
                                            </button>
                                            {f'<a href="/passport/{c.get("passport_id")}" target="_blank" class="btn btn-outline-warning" title="View Health Passport"><i class="fa-solid fa-certificate"></i> Passport</a>' if c.get("passport_id") else ''}
                                            {f'<a href="/invoice/{c.get("invoice_no")}" target="_blank" class="btn btn-outline-light" title="View Tax Invoice"><i class="fa-solid fa-file-invoice"></i> Invoice</a>' if c.get("invoice_no") else ''}
                                        </div>
                                    </td>
                                </tr>''' for c in job_cards)}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 5: NEW BIKE INTAKE -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="bike-intake" role="tabpanel">
                <div class="card card-custom p-4">
                    <h5 class="text-warning mb-3"><i class="fa-solid fa-clipboard-check me-2"></i>New Motorcycle Intake & Job Card Generation</h5>
                    <form id="jobCardForm" onsubmit="submitJobCard(event)">
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label">Customer Name</label>
                                <input type="text" id="custName" class="form-control bg-dark text-light border-secondary" required placeholder="e.g. Vikram Sharma">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Phone Number</label>
                                <input type="text" id="custPhone" class="form-control bg-dark text-light border-secondary" required placeholder="e.g. +91 98980 00000">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Royal Enfield Model</label>
                                <select id="bikeModel" class="form-select bg-dark text-light border-secondary">
                                    <option>Hunter 350</option>
                                    <option>Classic 350 Reborn</option>
                                    <option>Meteor 350</option>
                                    <option>Bullet 350 (New J-Series)</option>
                                    <option>Himalayan 450 (Sherpa)</option>
                                    <option>Continental GT 650</option>
                                    <option>Interceptor 650</option>
                                    <option>Super Meteor 650</option>
                                </select>
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Registration Number</label>
                                <input type="text" id="regNo" class="form-control bg-dark text-light border-secondary" required placeholder="GJ-01-RE-2026">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Odometer (KM)</label>
                                <input type="number" id="odoKm" class="form-control bg-dark text-light border-secondary" required placeholder="8500">
                            </div>
                            <div class="col-12">
                                <label class="form-label">Customer Complaints / Desired Service</label>
                                <textarea id="issues" class="form-control bg-dark text-light border-secondary" rows="3" placeholder="e.g. Periodic service, engine oil replacement, tappet ticking sound check, front brake squeal"></textarea>
                            </div>
                            <div class="col-12">
                                <button type="submit" class="btn btn-gold px-4 py-2">
                                    <i class="fa-solid fa-check-circle me-1"></i> Create Digital Job Card & Auto-Diagnose
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 6: SMART REMINDERS & PREDICTIVE CRM -->
        <!-- ============================================================= -->
        <div class="tab-pane fade" id="crm-reminders" role="tabpanel">
            <div class="row g-3 mb-4">
                <div class="col-md-3">
                    <div class="card card-custom p-3 border-danger">
                        <small class="text-danger text-uppercase fw-bold"><i class="fa-solid fa-triangle-exclamation me-1"></i> Due Now (Urgent)</small>
                        <div class="metric-val text-danger">{crm_data['due_now_count']} Bikes</div>
                        <small class="text-light opacity-75">≥80 Days or ≥2,800 KM</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card card-custom p-3 border-warning">
                        <small class="text-warning text-uppercase fw-bold"><i class="fa-solid fa-calendar-day me-1"></i> Upcoming Due</small>
                        <div class="metric-val text-warning">{crm_data['upcoming_count']} Bikes</div>
                        <small class="text-light opacity-75">55 - 79 Days (Next 30D)</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card card-custom p-3 border-success">
                        <small class="text-success text-uppercase fw-bold"><i class="fa-solid fa-shield-halved me-1"></i> Healthy / Recent</small>
                        <div class="metric-val text-success">{crm_data['recent_count']} Bikes</div>
                        <small class="text-light opacity-75">&lt;55 Days (Optimal Interval)</small>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card card-custom p-3 border-info">
                        <small class="text-info text-uppercase fw-bold"><i class="fa-solid fa-motorcycle me-1"></i> Total Fleet Monitored</small>
                        <div class="metric-val text-info">{crm_data['total_fleet_tracked']} Bikes</div>
                        <small class="text-light opacity-75">Algorithmic Mileage Tracking</small>
                    </div>
                </div>
            </div>

            <!-- Action Bar -->
            <div class="card card-custom p-3 mb-4">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <div>
                        <h5 class="text-warning mb-1"><i class="fa-solid fa-robot me-2"></i>Predictive Service CRM & WhatsApp Automation</h5>
                        <small class="text-muted">Calculates daily running (~32 km/day), detects overdue services, and crafts personalized bilingual reminders.</small>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-gold px-3 py-2 fw-bold" onclick="generateWholesalePO()">
                            <i class="fa-solid fa-boxes-packing me-1"></i> 1-Click Wholesale Stock PO
                        </button>
                    </div>
                </div>
            </div>

            <!-- URGENT: DUE NOW -->
            <div class="card card-custom p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-danger mb-0"><i class="fa-solid fa-circle-exclamation me-2"></i>Urgent: Service Due Now (Elapsed ≥80 Days / ≥2,800 KM)</h5>
                    <span class="badge bg-danger">{crm_data['due_now_count']} Actionable Customers</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-custom">
                        <thead>
                            <tr>
                                <th>Customer &amp; Phone</th>
                                <th>Motorcycle &amp; Reg No</th>
                                <th>Days Elapsed</th>
                                <th>Estimated Odo</th>
                                <th>Health Score</th>
                                <th>Reminder Status</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {due_rows_html if due_rows_html else '<tr><td colspan="7" class="text-center text-muted py-3">No motorcycles currently overdue.</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- UPCOMING FORECAST -->
            <div class="card card-custom p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-warning mb-0"><i class="fa-solid fa-clock me-2"></i>Upcoming Service Forecast (55 to 79 Days)</h5>
                    <span class="badge bg-warning text-dark">{crm_data['upcoming_count']} Upcoming</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-custom">
                        <thead>
                            <tr>
                                <th>Customer &amp; Phone</th>
                                <th>Motorcycle &amp; Reg No</th>
                                <th>Days Elapsed</th>
                                <th>Estimated Odo</th>
                                <th>Health Score</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {upcoming_rows_html if upcoming_rows_html else '<tr><td colspan="6" class="text-center text-muted py-3">No motorcycles in upcoming 30-day forecast.</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- WHOLESALE PO ARCHIVE -->
            <div class="card card-custom p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-info mb-0"><i class="fa-solid fa-file-invoice me-2"></i>Wholesale Stock Replenishment Orders</h5>
                    <span class="badge bg-info">{len(po_files)} Generated Orders</span>
                </div>
                <div class="table-responsive" style="max-height: 250px;">
                    <table class="table table-custom">
                        <thead>
                            <tr>
                                <th>PO Number</th>
                                <th>Vendor &amp; Scope</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            {po_rows_html if po_rows_html else '<tr><td colspan="3" class="text-center text-muted py-3">No purchase orders generated yet. Click \"1-Click Wholesale Stock PO\" above to generate.</td></tr>'}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 7: 24/7 CUSTOMER WHATSAPP BOT & LIVE JOB CARD TRACKER -->
        <!-- ============================================================= -->
        <div class="tab-pane fade" id="customer-bot" role="tabpanel">
            <div class="row g-4">
                <!-- Left: Customer Self-Service Job Tracker -->
                <div class="col-lg-6">
                    <div class="card card-custom p-4 h-100">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h5 class="text-warning mb-1">
                                    <i class="fa-solid fa-route me-2"></i>Live Service Stage &amp; Job Card Tracker
                                </h5>
                                <small class="text-muted">ગ્રાહક સેલ્ફ-સર્વિસ લાઈવ ટ્રેકર • ૫-સ્ટેજ પ્રોગ્રેસ બાર • WhatsApp સ્ટેટસ</small>
                            </div>
                            <span class="badge bg-success px-3 py-2"><i class="fa-solid fa-satellite-dish me-1"></i> Live Bay Telemetry</span>
                        </div>

                        <div class="input-group mb-3">
                            <span class="input-group-text bg-dark border-secondary text-warning"><i class="fa-solid fa-motorcycle"></i></span>
                            <input type="text" id="trackInput" class="form-control bg-dark text-light border-secondary" placeholder="Enter Reg No (e.g. GJ-01-AB-1234) or Phone...">
                            <button class="btn btn-gold fw-bold px-4" onclick="trackServiceLive()">
                                <i class="fa-solid fa-magnifying-glass me-1"></i> Track Now
                            </button>
                        </div>

                        <!-- Live Tracker Result -->
                        <div id="trackerResultBox" class="p-3 rounded border border-secondary" style="background: #091a14; display: none;">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <div>
                                    <h6 class="text-warning mb-0" id="trCustName">Customer</h6>
                                    <small class="text-light" id="trBikeInfo"></small>
                                </div>
                                <span class="badge bg-warning text-dark fs-6" id="trProgressBadge">0%</span>
                            </div>

                            <!-- Progress Bar -->
                            <div class="progress mb-3" style="height: 10px; background: #1a3328;">
                                <div id="trProgressBar" class="progress-bar progress-bar-striped progress-bar-animated bg-warning" role="progressbar" style="width: 0%"></div>
                            </div>

                            <!-- Stepper Visualizer -->
                            <div class="row text-center g-1 mb-3" style="font-size: 11px;">
                                <div class="col">
                                    <div class="p-2 rounded border border-secondary" id="step0">
                                        <div>📥</div>
                                        <strong>Intake</strong>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="p-2 rounded border border-secondary" id="step1">
                                        <div>🔍</div>
                                        <strong>50-Pt Check</strong>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="p-2 rounded border border-secondary" id="step2">
                                        <div>⚙️</div>
                                        <strong>Engine Bay</strong>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="p-2 rounded border border-secondary" id="step3">
                                        <div>✨</div>
                                        <strong>Wash &amp; Polish</strong>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="p-2 rounded border border-secondary" id="step4">
                                        <div>🏁</div>
                                        <strong>Ready</strong>
                                    </div>
                                </div>
                            </div>

                            <div class="row g-2 small mb-3">
                                <div class="col-6">
                                    <div class="p-2 bg-dark rounded border border-secondary">
                                        <span class="text-muted">Assigned Tech:</span><br>
                                        <strong class="text-light" id="trMechanic">Master Tech Alpesh</strong>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="p-2 bg-dark rounded border border-secondary">
                                        <span class="text-muted">Est. Delivery:</span><br>
                                        <strong class="text-warning" id="trDelivery">Today 05:30 PM</strong>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="p-2 bg-dark rounded border border-secondary">
                                        <span class="text-muted">Est. Billing:</span>
                                        <strong class="text-warning ms-1" id="trBill">₹0</strong>
                                    </div>
                                </div>
                            </div>

                            <div class="p-2 rounded bg-dark border-start border-warning border-3 mb-2">
                                <small class="text-light" id="trMessageGu"></small>
                            </div>

                            <button class="btn btn-outline-success btn-sm w-100" onclick="copyTrackerWhatsAppMsg()">
                                <i class="fa-brands fa-whatsapp me-1"></i> Copy WhatsApp Status Update Message
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Right: 24/7 WhatsApp Chat Simulator & Online Slot Booking -->
                <div class="col-lg-6">
                    <div class="card card-custom p-4 h-100">
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h5 class="text-warning mb-1">
                                    <i class="fa-brands fa-whatsapp text-success me-2"></i>24/7 WhatsApp AI Customer Advisor
                                </h5>
                                <small class="text-muted">Bilingual Gujarati &amp; English • Instant Quotes • Advance Slot Booking</small>
                            </div>
                            <div class="d-flex gap-2 align-items-center">
                                <a href="https://wa.me/917874719139?text=Hi%20Chamunda%20AI" target="_blank" class="badge bg-success text-decoration-none px-3 py-2 fs-6">
                                    <i class="fa-brands fa-whatsapp me-1"></i> WhatsApp: +91 78747 19139
                                </a>
                                <span class="badge bg-dark border border-warning text-warning px-3 py-2"><i class="fa-solid fa-bolt me-1"></i> 24/7 Active</span>
                            </div>
                        </div>

                        <!-- Chat Simulator Window -->
                        <div class="p-3 rounded border border-secondary mb-3" style="background: #081711; height: 320px; overflow-y: auto;" id="chatWindow">
                            <div class="d-flex mb-3">
                                <div class="p-2 rounded bg-dark border border-secondary text-light small" style="max-width: 85%;">
                                    <strong class="text-warning">👑 Chamunda AI Advisor:</strong><br>
                                    નમસ્તે! 🏍️ ચામુંડા ઓટોમોબાઇલ 24/7 WhatsApp AI આસિસ્ટન્ટ (+91 78747 19139) માં આપનું સ્વાગત છે. હું આપને સર્વિસ ટ્રેકિંગ, ૨૪/૭ બુકિંગ અને સ્પેરપાર્ટ્સની વિગતોમાં મદદ કરી શકું છું.
                                </div>
                            </div>
                        </div>

                        <div class="mb-3 d-flex justify-content-between align-items-center">
                            <a href="https://wa.me/917874719139?text=Hi%20Chamunda%20AI" target="_blank" class="btn btn-sm btn-outline-success">
                                <i class="fa-brands fa-whatsapp me-1"></i> Open WhatsApp Web (+91 78747 19139)
                            </a>
                            <small class="text-muted">Official Bot: +91 78747 19139</small>
                        </div>

                        <!-- Quick Suggestion Chips -->
                        <div class="d-flex gap-2 flex-wrap mb-3">
                            <button class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="sendQuickChat('મારી બાઇક ક્યાં પહોંચી? GJ-01-AB-1234')">🔍 Track GJ-01-AB-1234</button>
                            <button class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="sendQuickChat('Hunter 350 brake pad ભાવ શું છે?')">📦 Hunter 350 Brake Pad</button>
                            <button class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="sendQuickChat('કાલે સર્વિસ માટે બુકિંગ કરવું છે Classic 350')">📅 Book Service Slot</button>
                            <button class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="sendQuickChat('વર્કશોપનું સરનામું અને સમય')">📍 Location &amp; Timings</button>
                        </div>

                        <!-- Chat Input -->
                        <div class="input-group">
                            <input type="text" id="chatInput" class="form-control bg-dark text-light border-secondary" placeholder="Type customer message or query..." onkeydown="if(event.key==='Enter') sendChatMessage()">
                            <button class="btn btn-gold px-4" onclick="sendChatMessage()">
                                <i class="fa-solid fa-paper-plane me-1"></i> Send
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 8: CERTIFIED PRE-OWNED RE 100-POINT INSPECTION & VALUATION -->
        <!-- ============================================================= -->
        <div class="tab-pane fade" id="preowned-inspection" role="tabpanel">
            <!-- Header Banner -->
            <div class="card card-custom p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
                    <div>
                        <h4 class="text-warning mb-1">
                            <i class="fa-solid fa-shield-halved text-warning me-2"></i>Chamunda Certified Pre-Owned Royal Enfield &amp; 100-Point Shield Engine
                        </h4>
                        <p class="text-muted mb-0 small">
                            ચામુંડા સર્ટીફાઇડ સેકન્ડ-હેન્ડ રોયલ એનફિલ્ડ ઇન્સ્પેક્શન • AI ગુજરાત ફેર માર્કેટ વેલ્યુએશન • ડિજિટલ QR વોરંટી સર્ટિફિકેટ
                        </p>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-warning btn-sm" onclick="quickFillInspectionDemo()">
                            <i class="fa-solid fa-wand-magic-sparkles me-1"></i> Demo Fill (Classic 350)
                        </button>
                        <span class="badge bg-dark border border-warning text-warning px-3 py-2">
                            <i class="fa-solid fa-certificate me-1"></i> 100-Point Matrix Active
                        </span>
                    </div>
                </div>
            </div>

            <div class="row g-4 mb-4">
                <!-- Left Column: 100-Point Inspection Form -->
                <div class="col-lg-7">
                    <div class="card card-custom p-4">
                        <h5 class="text-warning mb-3">
                            <i class="fa-solid fa-clipboard-check me-2"></i>Conduct 100-Point Digital Quality Inspection
                        </h5>

                        <!-- Bike & Owner Details -->
                        <div class="row g-2 mb-3">
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Bike Model:</label>
                                <select class="form-select form-select-sm bg-dark text-light border-secondary" id="inspBikeModel" onchange="syncPreownedModel()">
                                    <option value="Classic 350" selected>Classic 350</option>
                                    <option value="Classic 350 (Reborn)">Classic 350 (Reborn)</option>
                                    <option value="Bullet 350">Bullet 350</option>
                                    <option value="Bullet 350 (New)">Bullet 350 (New)</option>
                                    <option value="Hunter 350">Hunter 350</option>
                                    <option value="Meteor 350">Meteor 350</option>
                                    <option value="Himalayan 450">Himalayan 450</option>
                                    <option value="Himalayan 411">Himalayan 411</option>
                                    <option value="Scram 411">Scram 411</option>
                                    <option value="Guerrilla 450">Guerrilla 450</option>
                                    <option value="Interceptor 650">Interceptor 650</option>
                                    <option value="Continental GT 650">Continental GT 650</option>
                                    <option value="Super Meteor 650">Super Meteor 650</option>
                                    <option value="Shotgun 650">Shotgun 650</option>
                                    <option value="Standard 350 (UCE)">Standard 350 (UCE)</option>
                                    <option value="Thunderbird 350">Thunderbird 350</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Registration Number:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary text-uppercase" id="inspRegNo" placeholder="GJ-01-RE-2022">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label small text-muted">Mfg Year:</label>
                                <input type="number" class="form-control form-control-sm bg-dark text-light border-secondary" id="inspYear" value="2022" min="1995" max="2026" onchange="calcLiveScore()">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label small text-muted">Odometer (KM):</label>
                                <input type="number" class="form-control form-control-sm bg-dark text-light border-secondary" id="inspOdo" value="18500" onchange="calcLiveScore()">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label small text-muted">Owner Name:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary" id="inspOwner" placeholder="e.g. Ramesh Patel">
                            </div>
                            <div class="col-md-3">
                                <label class="form-label small text-muted">Phone Number:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary" id="inspPhone" placeholder="+91 98250 12345">
                            </div>
                        </div>

                        <!-- 6 Domain Point Sliders -->
                        <div class="card bg-black border-secondary p-3 mb-3">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="text-warning fw-bold small"><i class="fa-solid fa-sliders me-1"></i> 6 Mechanical &amp; Electrical Domain Scores</span>
                                <span class="badge bg-gold text-dark fw-bold fs-6" id="liveScoreBadge">93 / 100 • PLATINUM</span>
                            </div>

                            <div class="row g-3 small">
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">1. Engine &amp; Clutch (Max 25):</span>
                                        <strong class="text-warning" id="lbl_engine">23</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_engine" min="10" max="25" value="23" oninput="document.getElementById('lbl_engine').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Compression, Valve Lash, Timing Chain, Clutch Plates</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">2. Chassis &amp; Suspension (Max 20):</span>
                                        <strong class="text-warning" id="lbl_chassis">19</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_chassis" min="8" max="20" value="19" oninput="document.getElementById('lbl_chassis').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Frame True, Headstock Bearings, Fork Seals, Swingarm</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">3. Acoustic Thump &amp; NVH (Max 15):</span>
                                        <strong class="text-warning" id="lbl_acoustic">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_acoustic" min="5" max="15" value="14" oninput="document.getElementById('lbl_acoustic').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Exhaust Bass Cadence (30-90Hz), Mechanical Clatter</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">4. Brakes &amp; Dual ABS (Max 15):</span>
                                        <strong class="text-warning" id="lbl_brakes">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_brakes" min="5" max="15" value="14" oninput="document.getElementById('lbl_brakes').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Rotor Thickness, ByBre Calipers, DOT4 Purity, ABS Sensors</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">5. Electricals &amp; ECU (Max 15):</span>
                                        <strong class="text-warning" id="lbl_electrical">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_electrical" min="5" max="15" value="14" oninput="document.getElementById('lbl_electrical').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">100A Battery Load Test, Stator Coil 14.2V, Zero DTCs</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">6. Aesthetics &amp; Odo Audit (Max 10):</span>
                                        <strong class="text-warning" id="lbl_aesthetics">9</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_aesthetics" min="3" max="10" value="9" oninput="document.getElementById('lbl_aesthetics').innerText=this.value; calcLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">OEM Clearcoat, Chrome Luster, Wear-vs-Odo Tamper Check</small>
                                </div>
                            </div>
                        </div>

                        <button class="btn btn-gold w-100 py-2 fw-bold" onclick="submit100PointInspection()">
                            <i class="fa-solid fa-shield-halved me-2"></i>Issue Chamunda Certified Pre-Owned Certificate &amp; QR
                        </button>
                    </div>
                </div>

                <!-- Right Column: AI Fair Market Valuation & Quick Calculator -->
                <div class="col-lg-5">
                    <div class="card card-custom p-4 mb-4">
                        <h5 class="text-warning mb-2">
                            <i class="fa-solid fa-calculator me-2"></i>AI Gujarat Fair Market Valuation
                        </h5>
                        <small class="text-muted d-block mb-3">
                            Algorithm calibrated for Royal Enfield demand in Ahmedabad, Rajkot, Surat &amp; Vadodara markets.
                        </small>

                        <div class="row g-2 mb-3">
                            <div class="col-7">
                                <label class="form-label small text-muted">Selected Model:</label>
                                <input type="text" id="valModelDisplay" class="form-control form-control-sm bg-dark text-light border-secondary" readonly value="Classic 350">
                            </div>
                            <div class="col-5">
                                <label class="form-label small text-muted">Year:</label>
                                <input type="number" id="valYearDisplay" class="form-control form-control-sm bg-dark text-light border-secondary" value="2022" onchange="runLiveValuation()">
                            </div>
                            <div class="col-6">
                                <label class="form-label small text-muted">Odometer (KM):</label>
                                <input type="number" id="valOdoDisplay" class="form-control form-control-sm bg-dark text-light border-secondary" value="18500" onchange="runLiveValuation()">
                            </div>
                            <div class="col-6">
                                <label class="form-label small text-muted">Condition Score:</label>
                                <input type="number" id="valScoreDisplay" class="form-control form-control-sm bg-dark text-light border-secondary" value="93" onchange="runLiveValuation()">
                            </div>
                        </div>

                        <button class="btn btn-outline-warning btn-sm w-100 mb-3 fw-bold" onclick="runLiveValuation()">
                            <i class="fa-solid fa-bolt me-1"></i> Calculate Fair Valuation
                        </button>

                        <!-- Valuation Output Box -->
                        <div class="p-3 bg-black rounded border border-warning" id="valuationResultCard">
                            <div class="text-center mb-2">
                                <small class="text-muted text-uppercase fw-bold">Fair Market Valuation (સરેરાશ બજાર ભાવ)</small>
                                <div class="display-6 fw-bold text-warning" id="resFairVal">₹1,82,300</div>
                            </div>
                            <hr class="border-secondary my-2">
                            <div class="row g-2 text-center small">
                                <div class="col-6">
                                    <span class="text-muted">Workshop Buying Target:</span><br>
                                    <strong class="text-success" id="resBuyerPrice">₹1,75,000</strong>
                                </div>
                                <div class="col-6">
                                    <span class="text-muted">Direct Asking Price:</span><br>
                                    <strong class="text-info" id="resSellerPrice">₹1,91,400</strong>
                                </div>
                                <div class="col-12 mt-2">
                                    <div class="p-1 rounded bg-dark border border-secondary" style="font-size: 11px;">
                                        <span class="text-muted">Gujarat Market Demand:</span>
                                        <strong class="text-warning ms-1" id="resMarketDemand">HIGH (Strong Resale Value)</strong>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Inspections Table -->
            <div class="card card-custom p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h5 class="text-warning mb-0"><i class="fa-solid fa-certificate me-2"></i>Chamunda Certified Pre-Owned Vehicle Registry</h5>
                        <small class="text-muted">Recently verified motorcycles with active QR Shield certificates</small>
                    </div>
                    <span class="badge bg-dark border border-warning text-warning">{len(recent_inspections)} Certified Units</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-custom table-hover align-middle">
                        <thead>
                            <tr>
                                <th>Certificate ID</th>
                                <th>Bike &amp; Reg No</th>
                                <th>Owner</th>
                                <th>Quality Score</th>
                                <th>Shield Grade</th>
                                <th>Fair Valuation</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="preownedRegistryBody">
                            {inspection_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- ============================================================= -->
        <!-- TAB 9: EXPEDITION READINESS, SPARES KIT & HIGHWAY SOS -->
        <!-- ============================================================= -->
        <div class="tab-pane fade" id="expedition-sos" role="tabpanel">
            <!-- Header Banner -->
            <div class="card card-custom p-4 mb-4">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
                    <div>
                        <h4 class="text-warning mb-1">
                            <i class="fa-solid fa-compass text-warning me-2"></i>Chamunda Royal Enfield Expedition Readiness &amp; Highway SOS Breakdown Shield
                        </h4>
                        <p class="text-muted mb-0 small">
                            ૪૮-પોઇન્ટ એક્સપિડિશન પ્રી-ટુર ક્લિયરન્સ ઓડિટ • મોડેલ-સ્પેસિફિક ટ્રિપ સ્પેર કીટ બિલ્ડર • ૨૪/૭ ગુજરાત હાઇવે બ્રેકડાઉન SOS સપોર્ટ
                        </p>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-warning btn-sm" onclick="quickFillExpeditionDemo()">
                            <i class="fa-solid fa-mountain me-1"></i> Demo Fill (Himalayan 450 • Ladakh)
                        </button>
                        <span class="badge bg-dark border border-warning text-warning px-3 py-2">
                            <i class="fa-solid fa-shield-halved me-1"></i> Expedition Shield Active
                        </span>
                    </div>
                </div>
            </div>

            <div class="row g-4 mb-4">
                <!-- Left: 48-Point Expedition Pre-Touring Audit Form -->
                <div class="col-lg-7">
                    <div class="card card-custom p-4">
                        <h5 class="text-warning mb-3">
                            <i class="fa-solid fa-list-check me-2"></i>48-Point Expedition Pre-Touring Readiness Audit
                        </h5>

                        <div class="row g-2 mb-3">
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Bike Model:</label>
                                <select class="form-select form-select-sm bg-dark text-light border-secondary" id="expBikeModel" onchange="syncExpeditionModel()">
                                    <option value="Himalayan 450" selected>Himalayan 450 (Sherpa 450)</option>
                                    <option value="Himalayan 411">Himalayan 411 / Scram 411</option>
                                    <option value="Classic 350">Classic 350 (Reborn / J-Series)</option>
                                    <option value="Bullet 350">Bullet 350</option>
                                    <option value="Hunter 350">Hunter 350</option>
                                    <option value="Meteor 350">Meteor 350 Supernova</option>
                                    <option value="Interceptor 650">Interceptor 650 Twin</option>
                                    <option value="Continental GT 650">Continental GT 650</option>
                                    <option value="Super Meteor 650">Super Meteor 650 Cruiser</option>
                                    <option value="Shotgun 650">Shotgun 650</option>
                                    <option value="Guerrilla 450">Guerrilla 450</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Registration Number:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary text-uppercase" id="expRegNo" placeholder="GJ-01-EX-4500">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Tour Destination &amp; Route:</label>
                                <select class="form-select form-select-sm bg-dark text-light border-secondary" id="expDestination" onchange="updateExpeditionKit()">
                                    <option value="ladakh_high_altitude" selected>Leh-Ladakh &amp; Spiti (High Altitude / Sub-Zero)</option>
                                    <option value="desert_highway">Kutch Rann &amp; Rajasthan (Heat / High Speed)</option>
                                    <option value="coastal_monsoon">Konkan &amp; Goa (Monsoon / Coastal Moisture)</option>
                                    <option value="weekend_escape">Gujarat Regional Weekend (Abu / Gir 500 KM)</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Planned Distance (KM):</label>
                                <input type="number" class="form-control form-control-sm bg-dark text-light border-secondary" id="expPlannedKm" value="3800">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Rider / Owner Name:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary" id="expRider" placeholder="e.g. Alpesh Patel">
                            </div>
                            <div class="col-md-6">
                                <label class="form-label small text-muted">Phone Number:</label>
                                <input type="text" class="form-control form-control-sm bg-dark text-light border-secondary" id="expPhone" placeholder="+91 98250 12345">
                            </div>
                        </div>

                        <!-- 6 Touring Domains Sliders -->
                        <div class="card bg-black border-secondary p-3 mb-3">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="text-warning fw-bold small"><i class="fa-solid fa-sliders me-1"></i> 6 Touring Endurance Domain Scores</span>
                                <span class="badge bg-gold text-dark fw-bold fs-6" id="expLiveScoreBadge">94 / 100 • LADAKH READY</span>
                            </div>

                            <div class="row g-3 small">
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">1. High-Altitude Fluids (Max 20):</span>
                                        <strong class="text-warning" id="lbl_exp_fluids">19</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_fluids" min="8" max="20" value="19" oninput="document.getElementById('lbl_exp_fluids').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Motul 7100 15W-50, DOT4 Boiling Point, Fork Dampening</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">2. Drive Chain &amp; Sprockets (Max 15):</span>
                                        <strong class="text-warning" id="lbl_exp_chain">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_chain" min="5" max="15" value="14" oninput="document.getElementById('lbl_exp_chain').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">28mm Slack, Sprocket Tooth Profile, Master Clip Locked</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">3. Mountain Braking Reserve (Max 15):</span>
                                        <strong class="text-warning" id="lbl_exp_brakes">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_brakes" min="5" max="15" value="14" oninput="document.getElementById('lbl_exp_brakes').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">ByBre Pads >3.5mm, Dual ABS Sensor Line Armoring</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">4. Electrical &amp; Aux Lighting (Max 15):</span>
                                        <strong class="text-warning" id="lbl_exp_electrical">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_electrical" min="5" max="15" value="14" oninput="document.getElementById('lbl_exp_electrical').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">14.2V Alternator Charge with Fog Lamps, 100A CCA Reserve</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">5. Panniers &amp; Luggage Balance (Max 20):</span>
                                        <strong class="text-warning" id="lbl_exp_chassis">19</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_chassis" min="8" max="20" value="19" oninput="document.getElementById('lbl_exp_chassis').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Rack Mount Bolt Torque 28Nm, Rear Gas Preload Click 5</small>
                                </div>
                                <div class="col-md-6">
                                    <div class="d-flex justify-content-between">
                                        <span class="text-light">6. Tyres &amp; Highway Heat (Max 15):</span>
                                        <strong class="text-warning" id="lbl_exp_tyres">14</strong>
                                    </div>
                                    <input type="range" class="form-range" id="pts_exp_tyres" min="5" max="15" value="14" oninput="document.getElementById('lbl_exp_tyres').innerText=this.value; calcExpLiveScore();">
                                    <small class="text-muted d-block" style="font-size: 11px;">Tread >3.5mm, Rim Trueness, High-Pressure Brass Caps</small>
                                </div>
                            </div>
                        </div>

                        <button class="btn btn-gold w-100 py-2 fw-bold" onclick="submitExpeditionAudit()">
                            <i class="fa-solid fa-compass me-2"></i>Issue Expedition Clearance Passport &amp; QR
                        </button>
                    </div>
                </div>

                <!-- Right: Carry-Along Custom Spares Pack Generator -->
                <div class="col-lg-5">
                    <div class="card card-custom p-4 mb-4">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h5 class="text-warning mb-0">
                                <i class="fa-solid fa-boxes-packing me-2"></i>Custom Carry-Along Spares Kit
                            </h5>
                            <button class="btn btn-outline-warning btn-sm" onclick="updateExpeditionKit()">
                                <i class="fa-solid fa-rotate me-1"></i> Refresh
                            </button>
                        </div>
                        <small class="text-muted d-block mb-3">
                            4,469 Genuine Parts Catalog માંથી પસંદ કરેલી ઇમરજન્સી હાઇવે બેકઅપ કીટ.
                        </small>

                        <div id="sparesKitLoading" style="display: none;" class="text-center py-3 text-muted">
                            <div class="spinner-border text-warning spinner-border-sm me-2"></div> Auto-packaging OEM parts...
                        </div>

                        <div id="sparesKitContent">
                            <!-- Injected by JavaScript updateExpeditionKit() -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- Full Width: 24/7 Gujarat Highway Breakdown SOS Triage Terminal -->
            <div class="card card-custom p-4 mb-4 border-danger">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                    <div>
                        <h5 class="text-danger mb-1">
                            <i class="fa-solid fa-triangle-exclamation me-2"></i>24/7 Gujarat Highway Breakdown SOS Roadside Triage Terminal
                        </h5>
                        <small class="text-muted">
                            NH-48, NH-27, રાજકોટ, સુરત અથવા ઉદયપુર હાઇવે પર અટવાયેલા રાઇડર્સ માટે ૩૦-સેકન્ડ ઇમરજન્સી ટેકનિકલ ગાઇડન્સ.
                        </small>
                    </div>
                    <a href="tel:+919825012345" class="btn btn-danger btn-sm fw-bold">
                        <i class="fa-solid fa-phone-volume me-1"></i> SOS Hotline: +91 98250 12345
                    </a>
                </div>

                <!-- Quick Problem Chips -->
                <div class="d-flex gap-2 flex-wrap mb-3">
                    <button class="btn btn-sm btn-outline-danger" onclick="runSOSTriage('clutch')">🔴 Snapped Clutch Wire / Free Lever</button>
                    <button class="btn btn-sm btn-outline-warning" onclick="runSOSTriage('start')">⚡ Electric Starter Dead / Click Sound</button>
                    <button class="btn btn-sm btn-outline-info" onclick="runSOSTriage('heat')">🔥 Engine Overheated / Sudden Stall</button>
                    <button class="btn btn-sm btn-outline-light" onclick="runSOSTriage('puncture')">🛑 Rear Tyre Puncture / Low Pressure</button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="runSOSTriage('chain')">⛓️ Drive Chain Slapped / Slipped</button>
                </div>

                <div class="input-group mb-3">
                    <input type="text" id="sosQueryInput" class="form-control bg-dark text-light border-secondary" placeholder="Describe breakdown issue (e.g. ગાડી ચાલુ નથી થતી, ક્લચ વાયર તૂટી ગયો)..." onkeydown="if(event.key==='Enter') runSOSTriageFromInput()">
                    <button class="btn btn-danger px-4 fw-bold" onclick="runSOSTriageFromInput()">
                        <i class="fa-solid fa-bolt me-1"></i> Instant Roadside Triage
                    </button>
                </div>

                <!-- Roadside Fix Result Box -->
                <div id="sosResultBox" class="p-3 bg-black rounded border border-danger" style="display: none;">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="text-warning mb-0" id="sosFaultTitle">Clutch Cable Snapped</h6>
                        <span class="badge bg-danger" id="sosSeverity">HIGH</span>
                    </div>
                    <div class="row g-3 small">
                        <div class="col-md-6">
                            <div class="p-2 bg-dark rounded border border-secondary mb-2">
                                <strong class="text-success"><i class="fa-solid fa-wrench me-1"></i> ગુજરાતી રોડસાઇડ ગાઇડ:</strong>
                                <p class="text-light mb-0 mt-1" id="sosActionGu" style="white-space: pre-line; font-size: 12px;"></p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-2 bg-dark rounded border border-secondary mb-2">
                                <strong class="text-info"><i class="fa-solid fa-wrench me-1"></i> English Action Steps:</strong>
                                <p class="text-light mb-0 mt-1" id="sosActionEn" style="white-space: pre-line; font-size: 12px;"></p>
                            </div>
                        </div>
                        <div class="col-12">
                            <div class="d-flex gap-3 text-muted" style="font-size: 11px;">
                                <div><strong>🛠️ Toolkit Needed:</strong> <span id="sosToolkit" class="text-light"></span></div>
                                <div><strong>📦 Spare Part:</strong> <span id="sosSpare" class="text-warning"></span></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Expedition Clearance Passports Table -->
            <div class="card card-custom p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h5 class="text-warning mb-0"><i class="fa-solid fa-passport me-2"></i>Chamunda Expedition Clearance Passports Registry</h5>
                        <small class="text-muted">Riders cleared for high-altitude and long-distance touring</small>
                    </div>
                    <span class="badge bg-dark border border-warning text-warning">{len(recent_expeditions)} Active Passports</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-custom table-hover align-middle">
                        <thead>
                            <tr>
                                <th>Passport ID</th>
                                <th>Bike &amp; Reg No</th>
                                <th>Rider</th>
                                <th>Destination &amp; KM</th>
                                <th>Readiness Score</th>
                                <th>Clearance Grade</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="expeditionRegistryBody">
                            {expedition_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

            <!-- ============================================================= -->
            <!-- TAB 10: CUSTOM RESTO-MOD & VINTAGE CI STUDIO -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="custom-studio" role="tabpanel">
                <!-- Header Banner -->
                <div class="card card-custom p-4 mb-4 border border-warning" style="background: linear-gradient(135deg, rgba(212,175,55,0.12) 0%, rgba(17,17,17,0.95) 100%);">
                    <div class="row align-items-center">
                        <div class="col-lg-8">
                            <div class="d-flex align-items-center gap-3 mb-2">
                                <span class="badge bg-warning text-dark fs-6 px-3 py-2 fw-bold">
                                    <i class="fa-solid fa-crown me-1"></i> Bespoke Custom &amp; Vintage Engineering
                                </span>
                                <span class="badge bg-dark border border-warning text-warning px-3 py-2">
                                    <i class="fa-solid fa-bolt me-1"></i> Heavy Crank Rebirth &amp; Dyno Tuner
                                </span>
                            </div>
                            <h3 class="text-warning fw-bold mb-1">
                                🏍️ Chamunda Royal Enfield Custom Resto-Mod, Dyno Tuning &amp; Vintage CI Rebirth Studio
                            </h3>
                            <p class="text-light mb-0" style="font-size: 0.95rem;">
                                ચામુંડા કસ્ટમ રેસ્ટો-મોડ સ્ટુડિયો: હેવી ક્રેન્ક વિન્ટેજ કાસ્ટ-આયર્ન (1970-2009) રિબર્થ, બોબર/કેફે રેસર/સ્ક્રેમ્બલર બિલ્ડ્સ, સ્ટેજ 1 &amp; 2 ડાયનો ટ્યુનિંગ (&lt;85 dB RTO લિગલ), અને 4,469 જેન્યુઈન પાર્ટ્સમાંથી ઓટોમેટેડ BOM બ્લુપ્રિન્ટ.
                            </p>
                        </div>
                        <div class="col-lg-4 text-end mt-3 mt-lg-0">
                            <button class="btn btn-outline-warning btn-sm me-2" onclick="quickFillRestoDemo()">
                                <i class="fa-solid fa-wand-magic-sparkles me-1"></i> Demo Build (CI Bobber 350)
                            </button>
                            <a href="#restoRegistryCard" class="btn btn-gold btn-sm">
                                <i class="fa-solid fa-list-check me-1"></i> View Blueprints
                            </a>
                        </div>
                    </div>
                </div>

                <div class="row g-4">
                    <!-- Column 1 & 2: Custom Resto-Mod Builder Form & Live BOM Preview -->
                    <div class="col-lg-8">
                        <div class="card card-custom p-4 mb-4">
                            <h5 class="text-warning mb-3">
                                <i class="fa-solid fa-sliders me-2"></i>Configure Bespoke Resto-Mod Build
                            </h5>
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <label class="form-label text-warning small fw-bold">Rider / Customer Name</label>
                                    <input type="text" id="restoCustomer" class="form-control bg-dark text-light border-secondary" value="Kishorbhai Parmar" placeholder="Enter customer name">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-warning small fw-bold">Contact Phone (WhatsApp)</label>
                                    <input type="text" id="restoPhone" class="form-control bg-dark text-light border-secondary" value="+91 98250 44551" placeholder="+91 98...">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-warning small fw-bold">Royal Enfield Model Platform</label>
                                    <select id="restoModel" class="form-select bg-dark text-light border-secondary" onchange="updateRestoPreview()">
                                        <option value="Bullet 350 Cast-Iron CI" selected>Bullet 350 Cast-Iron CI (Heavy Crank Vintage)</option>
                                        <option value="Electra 350 CI">Electra 350 CI (4-Speed Right Shift)</option>
                                        <option value="Classic 350 Reborn">Classic 350 Reborn (J-Series 2021+)</option>
                                        <option value="Bullet 350">Bullet 350 Next-Gen (J-Series)</option>
                                        <option value="Hunter 350">Hunter 350 Roadster</option>
                                        <option value="Meteor 350">Meteor 350 Cruiser</option>
                                        <option value="Himalayan 450">Himalayan 450 Sherpa Liquid-Cooled</option>
                                        <option value="Interceptor 650">Interceptor 650 Twin</option>
                                        <option value="Continental GT 650">Continental GT 650 Cafe Racer</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label text-warning small fw-bold">Vehicle Registration No.</label>
                                    <input type="text" id="restoRegNo" class="form-control bg-dark text-light border-secondary text-uppercase" value="GJ-01-AB-1982" placeholder="e.g. GJ-01-AB-1234">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label text-warning small fw-bold">Resto-Mod Style Archetype</label>
                                    <select id="restoStyle" class="form-select bg-dark text-light border-secondary" onchange="updateRestoPreview()">
                                        <option value="bobber_solo" selected>Bobber Solo (ચોપડ ફેન્ડર &amp; સિંગલ સ્પ્રંગ સીટ)</option>
                                        <option value="cafe_racer">Cafe Racer (ક્લિપ-ઓન હેન્ડલ &amp; કાઉલ સીટ)</option>
                                        <option value="desert_scrambler">Desert Scrambler (હાઇ એક્ઝોસ્ટ &amp; નોબી ટાયર)</option>
                                        <option value="vintage_heritage_standard">Vintage Heritage Standard (ઓરિજિનલ વિન્ટેજ)</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label text-warning small fw-bold">Custom Paint &amp; Finish</label>
                                    <select id="restoPaint" class="form-select bg-dark text-light border-secondary" onchange="updateRestoPreview()">
                                        <option value="british_racing_green_gold">British Racing Green with 24K Gold Pinstripes</option>
                                        <option value="matte_phantom_black" selected>Matte Phantom Black Ceramic Coat</option>
                                        <option value="desert_sand_patina">Desert Sand Matte Military Patina</option>
                                        <option value="candy_royal_maroon">Candy Royal Maroon with Chrome Flakes</option>
                                        <option value="vintage_gunmetal_silver">Vintage Gunmetal Brushed Silver</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label text-warning small fw-bold">Performance Dyno Stage</label>
                                    <select id="restoStage" class="form-select bg-dark text-light border-secondary" onchange="updateRestoPreview()">
                                        <option value="stage_0_stock">Stage 0 - Factory Stock Calibration</option>
                                        <option value="stage_1_street_thump" selected>Stage 1 - Street Thump &amp; Free-Flow Intake (+15% HP)</option>
                                        <option value="stage_2_dyno_sprint">Stage 2 - Dyno Sprint High-Cam (+30% HP / +28% TQ)</option>
                                    </select>
                                </div>
                                <div class="col-12">
                                    <div class="form-check form-switch p-3 bg-black rounded border border-warning">
                                        <input class="form-check-input ms-0 me-3" type="checkbox" id="restoIncludeVintage" checked onchange="updateRestoPreview()">
                                        <label class="form-check-label text-warning fw-bold" for="restoIncludeVintage">
                                            <i class="fa-solid fa-wrench me-1"></i> Include Vintage Cast-Iron (CI) Heavy Crank Rebirth Package (₹12,500)
                                        </label>
                                        <small class="d-block text-muted ms-4">Includes CB point calibration, pushrod tappet zero-lash set, Mikcarb jetting, Albion 4-speed shimming, and de-carbonizing.</small>
                                    </div>
                                </div>
                                <div class="col-12">
                                    <label class="form-label text-warning small fw-bold">Custom Fabrications &amp; Rider Directives</label>
                                    <textarea id="restoNotes" class="form-control bg-dark text-light border-secondary" rows="2" placeholder="e.g. Springer front fork suspension, handcrafted tan leather single seat, custom brass tank emblems, barcode laser etching"></textarea>
                                </div>
                            </div>

                            <!-- Live Cost & Spec Estimate Strip -->
                            <div class="mt-4 p-3 bg-black rounded border border-secondary">
                                <div class="row text-center g-2">
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Style Labor</small>
                                        <strong class="text-light" id="previewLabor">₹38,000</strong>
                                    </div>
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Custom Paint</small>
                                        <strong class="text-light" id="previewPaint">₹15,000</strong>
                                    </div>
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Dyno Tune</small>
                                        <strong class="text-light" id="previewTune">₹14,500</strong>
                                    </div>
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Vintage Rebirth</small>
                                        <strong class="text-light" id="previewVintage">₹12,500</strong>
                                    </div>
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Spares BOM (Est)</small>
                                        <strong class="text-light" id="previewBOM">₹24,500</strong>
                                    </div>
                                    <div class="col-6 col-md-2">
                                        <small class="text-muted text-uppercase d-block">Est. Grand Total</small>
                                        <strong class="text-warning fs-5" id="previewGrand">₹1,04,500</strong>
                                    </div>
                                </div>
                                <div class="mt-2 text-center text-muted small">
                                    <i class="fa-solid fa-clock me-1 text-warning"></i> Estimated Turnaround Time: <strong class="text-warning" id="previewDays">33</strong> Working Days
                                </div>
                            </div>

                            <div class="mt-4 d-flex justify-content-between align-items-center">
                                <span class="text-muted small"><i class="fa-solid fa-qrcode me-1 text-warning"></i> Generates Verifiable QR Blueprint &amp; locks Bill of Materials</span>
                                <button type="button" class="btn btn-gold px-4 py-2" onclick="generateRestoBlueprint()">
                                    <i class="fa-solid fa-hammer me-2"></i>Generate Digital Blueprint &amp; Lock BOM
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Column 3: Dyno Calibration Bench & Quick Actions -->
                    <div class="col-lg-4">
                        <!-- Dyno Tuner Box -->
                        <div class="card card-custom p-3 mb-4">
                            <h6 class="text-warning mb-3">
                                <i class="fa-solid fa-gauge-high me-2"></i>Performance Dyno Calibrator
                            </h6>
                            <div class="mb-2">
                                <label class="text-muted small fw-bold">Platform</label>
                                <select id="dynoModelSelect" class="form-select form-select-sm bg-dark text-light border-secondary">
                                    <option value="Bullet 350 Cast-Iron CI">Bullet 350 Cast-Iron CI</option>
                                    <option value="Classic 350 Reborn" selected>Classic 350 Reborn</option>
                                    <option value="Himalayan 450">Himalayan 450</option>
                                    <option value="Interceptor 650">Interceptor 650</option>
                                    <option value="Continental GT 650">Continental GT 650</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="text-muted small fw-bold">Target Dyno Stage</label>
                                <select id="dynoStageSelect" class="form-select form-select-sm bg-dark text-light border-secondary">
                                    <option value="stage_1_street_thump">Stage 1: Street Thump (+15% HP)</option>
                                    <option value="stage_2_dyno_sprint" selected>Stage 2: Dyno Sprint High-Cam (+30% HP)</option>
                                </select>
                            </div>
                            <button class="btn btn-outline-warning btn-sm w-100 mb-3" onclick="runDynoAnalysis()">
                                <i class="fa-solid fa-chart-line me-1"></i> Simulate Dyno Pull &amp; Noise Check
                            </button>

                            <!-- Dyno Output Display -->
                            <div id="dynoResultBox" class="p-3 bg-black rounded border border-secondary" style="display: none;">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <strong class="text-warning small" id="dynoStageTitle">Stage 2 Dyno Sprint</strong>
                                    <span id="dynoRtoBadge" class="badge bg-success small">RTO Legal &lt;85 dB</span>
                                </div>
                                <div class="row text-center g-2 mb-2">
                                    <div class="col-6">
                                        <small class="text-muted d-block">Power</small>
                                        <strong class="text-success" id="dynoHpChange">20.2 &rarr; 27.4 HP</strong>
                                    </div>
                                    <div class="col-6">
                                        <small class="text-muted d-block">Torque</small>
                                        <strong class="text-success" id="dynoTqChange">27.0 &rarr; 34.6 Nm</strong>
                                    </div>
                                </div>
                                <div class="small text-muted mb-1">Top Speed Gain: <strong class="text-light" id="dynoSpeed">+15-20 km/h</strong></div>
                                <div class="small text-muted mb-1">Thump Profile: <strong class="text-warning" id="dynoThump">Deep Bass Baritone</strong></div>
                                <div class="small text-muted">Sound dB: <strong class="text-light" id="dynoDb">84.2 dB</strong> (Legal Limit 85 dB)</div>
                            </div>
                        </div>

                        <!-- Vintage CI Quick Rebirth Matrix -->
                        <div class="card card-custom p-3">
                            <h6 class="text-warning mb-2">
                                <i class="fa-solid fa-gears me-2"></i>Vintage CI (1970-2009) Rebirth Matrix
                            </h6>
                            <p class="text-muted small mb-2">Instant diagnostic tolerance check for heavy crank Cast-Iron engines.</p>
                            
                            <div class="d-flex flex-wrap gap-1 mb-3">
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('points burnt misfire')">CB Points</button>
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('tappet ticking noise')">Pushrods</button>
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('black smoke mikcarb jetting')">Mikcarb</button>
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('heavy crank backfire timing')">Timing</button>
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('albion 4 speed slip')">Albion Box</button>
                                <button class="btn btn-sm btn-outline-secondary py-0 px-2" onclick="quickVintageSymptom('wet sumping crankcase oil')">Wet Sump</button>
                            </div>

                            <div class="input-group input-group-sm mb-2">
                                <input type="text" id="vintageQueryInput" class="form-control bg-dark text-light border-secondary" placeholder="e.g. tappet clatter, cb point gap...">
                                <button class="btn btn-warning" onclick="diagnoseVintageBullet()">
                                    <i class="fa-solid fa-magnifying-glass"></i>
                                </button>
                            </div>

                            <!-- Vintage Diagnosis Output -->
                            <div id="vintageResultBox" class="p-3 bg-black rounded border border-warning" style="display: none;">
                                <div class="fw-bold text-warning small mb-1" id="vintageFaultTitle">CB Point Burn &amp; Ignition Misfire</div>
                                <div class="text-light small mb-2" id="vintageRootCause"></div>
                                <div class="p-2 bg-dark rounded border border-secondary mb-2">
                                    <small class="text-warning d-block fw-bold">Factory Spec &amp; Tolerance:</small>
                                    <code class="text-light" id="vintageTolerance">0.35 mm - 0.40 mm gap</code>
                                </div>
                                <div class="small text-muted mb-1">
                                    <strong class="text-success">ગુજરાતી માર્ગદર્શિકા:</strong> <span id="vintageActionGu"></span>
                                </div>
                                <div class="small text-muted">
                                    <strong class="text-info">Directive:</strong> <span id="vintageActionEn"></span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Master Blueprint Registry -->
                <div class="card card-custom p-4 mt-4" id="restoRegistryCard">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-warning mb-0">
                            <i class="fa-solid fa-clipboard-check me-2"></i>Master Registry of Resto-Mod Blueprints &amp; Build Orders
                        </h5>
                        <span class="badge bg-secondary">Archived &amp; Verifiable via QR Code</span>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-warning small text-uppercase">
                                    <th>Blueprint ID</th>
                                    <th>Model Platform</th>
                                    <th>Customer / Phone</th>
                                    <th>Resto Style</th>
                                    <th>Paint Theme</th>
                                    <th>Grand Total &amp; Timeline</th>
                                    <th>Digital Blueprint</th>
                                </tr>
                            </thead>
                            <tbody id="restoRegistryBody">
                                {restomod_rows_html}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 11: 360° OMNICHANNEL SOCIAL & BRAND MANAGEMENT HUB -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="omnichannel-social" role="tabpanel">
                <!-- Channel Telemetry Bar -->
                <div class="card card-custom p-4 mb-4">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-3 mb-3">
                        <div>
                            <h4 class="text-warning mb-1">
                                <i class="fa-solid fa-share-nodes text-warning me-2"></i>360° Omnichannel Social Media &amp; Brand Presence Hub
                            </h4>
                            <p class="text-muted mb-0 small">
                                Autonomous brand syndication &amp; customer interaction across WhatsApp (+91 78747 19139), Instagram, Facebook, Google Business Profile &amp; YouTube.
                            </p>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-outline-warning btn-sm" onclick="loadSocialTelemetry()">
                                <i class="fa-solid fa-rotate me-1"></i> Refresh Channels
                            </button>
                            <span class="badge bg-dark border border-success text-success px-3 py-2 fs-6">
                                <i class="fa-solid fa-circle-check me-1"></i> All 5 Channels Synced
                            </span>
                        </div>
                    </div>

                    <!-- Channel Badges Row -->
                    <div class="row g-3 text-center">
                        <div class="col-md">
                            <div class="p-3 bg-dark rounded border border-success h-100">
                                <i class="fa-brands fa-whatsapp text-success fs-3 mb-2"></i>
                                <h6 class="text-light mb-1">WhatsApp Business</h6>
                                <a href="https://wa.me/917874719139" target="_blank" class="badge bg-success text-decoration-none mb-1">+91 78747 19139</a>
                                <small class="text-muted d-block">24/7 AI Bot Active</small>
                                <span class="badge bg-dark border border-secondary text-warning mt-2">3,420 Riders</span>
                            </div>
                        </div>
                        <div class="col-md">
                            <div class="p-3 bg-dark rounded border border-danger h-100">
                                <i class="fa-brands fa-instagram text-danger fs-3 mb-2"></i>
                                <h6 class="text-light mb-1">Instagram Business</h6>
                                <code class="text-danger">@chamunda_automobile_re</code>
                                <small class="text-muted d-block mt-1">Reels &amp; DM Auto-Reply</small>
                                <span class="badge bg-dark border border-secondary text-warning mt-2">18.6K Followers</span>
                            </div>
                        </div>
                        <div class="col-md">
                            <div class="p-3 bg-dark rounded border border-primary h-100">
                                <i class="fa-brands fa-facebook text-primary fs-3 mb-2"></i>
                                <h6 class="text-light mb-1">Facebook Page &amp; Club</h6>
                                <code class="text-primary">fb.com/chamundaautomobile</code>
                                <small class="text-muted d-block mt-1">RE Club Community</small>
                                <span class="badge bg-dark border border-secondary text-warning mt-2">12.8K Followers</span>
                            </div>
                        </div>
                        <div class="col-md">
                            <div class="p-3 bg-dark rounded border border-warning h-100">
                                <i class="fa-brands fa-google text-warning fs-3 mb-2"></i>
                                <h6 class="text-light mb-1">Google Business (GBP)</h6>
                                <span class="badge bg-warning text-dark fw-bold mb-1">4.9 ★★★★★</span>
                                <small class="text-muted d-block">842 Local Reviews</small>
                                <span class="badge bg-dark border border-secondary text-warning mt-2">Local SEO Dominance</span>
                            </div>
                        </div>
                        <div class="col-md">
                            <div class="p-3 bg-dark rounded border border-danger h-100">
                                <i class="fa-brands fa-youtube text-danger fs-3 mb-2"></i>
                                <h6 class="text-light mb-1">YouTube Channel</h6>
                                <code class="text-danger">@ChamundaAutomobileRE</code>
                                <small class="text-muted d-block mt-1">Shorts AI Commander</small>
                                <span class="badge bg-dark border border-secondary text-warning mt-2">9.4K Subscribers</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Studio & Campaigns -->
                <div class="row g-4 mb-4">
                    <!-- Left: Multi-Channel Post Studio -->
                    <div class="col-lg-5">
                        <div class="card card-custom p-4 h-100">
                            <h5 class="text-warning mb-3">
                                <i class="fa-solid fa-wand-magic-sparkles me-2"></i>AI 360° Campaign Studio
                            </h5>
                            <p class="text-muted small mb-3">
                                Generate native copies formatted uniquely for WhatsApp, Instagram, Facebook, Google Business, and YouTube with a single click.
                            </p>

                            <!-- Presets Chips -->
                            <label class="form-label text-warning small fw-bold">Quick Topic Templates</label>
                            <div class="d-flex flex-wrap gap-2 mb-3">
                                <button type="button" class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="setSocialTopic('Classic 350 Cold Start Tappet Noise Fix &amp; Calibration')">Classic 350 Tappets</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="setSocialTopic('Monsoon 48-Point Waterproofing &amp; Chain Lube Package')">Monsoon Care</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="setSocialTopic('1994 Standard 350 Vintage Cast-Iron Restoration &amp; Signature Thump')">Vintage CI Rebuild</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary py-0" style="font-size: 11px;" onclick="setSocialTopic('Himalayan 450 Pre-Ladakh Expedition Inspection &amp; Spares Kit')">Himalayan Ladakh</button>
                            </div>

                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Campaign Topic / Royal Enfield Focus</label>
                                <input type="text" id="socialTopicInput" class="form-control bg-dark text-light border-secondary" value="Classic 350 Cold Start Tappet Noise Fix &amp; Calibration">
                            </div>

                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Campaign Category</label>
                                <select id="socialTypeSelect" class="form-select bg-dark text-light border-secondary">
                                    <option value="Workshop Master Tip">Workshop Master Tip (Mechanical Education)</option>
                                    <option value="Service Awareness">Service Awareness &amp; Seasonal Packages</option>
                                    <option value="Resto-Mod Showcase">Resto-Mod &amp; Vintage CI Rebuild Showcase</option>
                                    <option value="Spares Alert">Genuine vs Duplicate Spares Warning</option>
                                    <option value="Rider Club Event">Chamunda RE Rider Club Weekend Tour</option>
                                </select>
                            </div>

                            <button type="button" class="btn btn-gold w-100 fw-bold py-2 mb-3" onclick="generateSocialCampaign()">
                                <i class="fa-solid fa-bolt me-1"></i> Generate Native Multi-Channel Copies
                            </button>

                            <div class="alert alert-dark border-secondary small mb-0">
                                <i class="fa-solid fa-circle-info text-warning me-2"></i>
                                All generated copies automatically embed the official 24/7 WhatsApp AI Bot link (<strong>+91 78747 19139</strong>) and workshop helpline.
                            </div>
                        </div>
                    </div>

                    <!-- Right: Visual Multi-Platform Previewer -->
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="text-warning mb-0">
                                    <i class="fa-solid fa-eye me-2"></i>Live Multi-Platform Previews
                                </h5>
                                <button class="btn btn-success btn-sm px-3 fw-bold" onclick="publishSocialCampaign()">
                                    <i class="fa-solid fa-paper-plane me-1"></i> Publish to All 5 Channels
                                </button>
                            </div>

                            <!-- Channel Tabs -->
                            <ul class="nav nav-pills mb-3" id="socialPreviewTabs" role="tablist">
                                <li class="nav-item">
                                    <button class="nav-link active py-1 px-3 btn-sm" data-bs-toggle="pill" data-bs-target="#prevWhatsApp">
                                        <i class="fa-brands fa-whatsapp text-success me-1"></i> WhatsApp
                                    </button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 px-3 btn-sm" data-bs-toggle="pill" data-bs-target="#prevInstagram">
                                        <i class="fa-brands fa-instagram text-danger me-1"></i> Instagram
                                    </button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 px-3 btn-sm" data-bs-toggle="pill" data-bs-target="#prevFacebook">
                                        <i class="fa-brands fa-facebook text-primary me-1"></i> Facebook
                                    </button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 px-3 btn-sm" data-bs-toggle="pill" data-bs-target="#prevGoogle">
                                        <i class="fa-brands fa-google text-warning me-1"></i> Google (GBP)
                                    </button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 px-3 btn-sm" data-bs-toggle="pill" data-bs-target="#prevYouTube">
                                        <i class="fa-brands fa-youtube text-danger me-1"></i> YouTube
                                    </button>
                                </li>
                            </ul>

                            <div class="tab-content flex-fill">
                                <!-- WhatsApp Preview -->
                                <div class="tab-pane fade show active" id="prevWhatsApp">
                                    <div class="p-3 bg-black rounded border border-success" style="font-family: monospace; white-space: pre-wrap; font-size: 12px;" id="prevWaText">
Click 'Generate Native Multi-Channel Copies' to preview WhatsApp broadcast copy...
                                    </div>
                                </div>

                                <!-- Instagram Preview -->
                                <div class="tab-pane fade" id="prevInstagram">
                                    <div class="p-3 bg-black rounded border border-danger" style="font-size: 13px;">
                                        <div class="mb-2 text-warning fw-bold"><i class="fa-brands fa-instagram me-1"></i> @chamunda_automobile_re • Reels &amp; Post Caption</div>
                                        <div id="prevIgText" style="white-space: pre-wrap;">
Click 'Generate Native Multi-Channel Copies' to preview Instagram caption &amp; hashtags...
                                        </div>
                                    </div>
                                </div>

                                <!-- Facebook Preview -->
                                <div class="tab-pane fade" id="prevFacebook">
                                    <div class="p-3 bg-black rounded border border-primary" style="font-size: 13px;" id="prevFbText">
Click 'Generate Native Multi-Channel Copies' to preview Facebook page update...
                                    </div>
                                </div>

                                <!-- Google Business Preview -->
                                <div class="tab-pane fade" id="prevGoogle">
                                    <div class="p-3 bg-black rounded border border-warning" style="font-size: 13px;">
                                        <div class="d-flex justify-content-between mb-2">
                                            <span class="badge bg-warning text-dark">Google Search &amp; Maps Post</span>
                                            <span class="text-success small"><i class="fa-solid fa-location-dot me-1"></i> Ahmedabad &amp; Gandhinagar</span>
                                        </div>
                                        <div id="prevGbpText" style="white-space: pre-wrap;">
Click 'Generate Native Multi-Channel Copies' to preview Google Local SEO update...
                                        </div>
                                        <div class="mt-3 pt-2 border-top border-secondary d-flex gap-2">
                                            <a href="tel:+919825012345" class="btn btn-sm btn-primary py-1"><i class="fa-solid fa-phone me-1"></i> Call Now (+91 98250 12345)</a>
                                            <a href="https://wa.me/917874719139" target="_blank" class="btn btn-sm btn-success py-1"><i class="fa-brands fa-whatsapp me-1"></i> WhatsApp Booking</a>
                                        </div>
                                    </div>
                                </div>

                                <!-- YouTube Preview -->
                                <div class="tab-pane fade" id="prevYouTube">
                                    <div class="p-3 bg-black rounded border border-danger" style="font-size: 13px;">
                                        <h6 class="text-light mb-1" id="prevYtTitle">YouTube Video / Short Title</h6>
                                        <small class="text-warning d-block mb-2" id="prevYtHook"></small>
                                        <div class="p-2 bg-dark rounded border border-secondary mb-2" style="max-height: 180px; overflow-y: auto; font-family: monospace; font-size: 11px; white-space: pre-wrap;" id="prevYtDesc">
Description &amp; Timestamps...
                                        </div>
                                        <div class="small text-muted mb-1" id="prevYtTags">Tags: </div>
                                        <div class="small text-info" id="prevYtComment">Pinned Comment: </div>
                                    </div>
                                </div>
                            </div>

                            <div id="publishStatusAlert" class="mt-3 alert alert-success small py-2" style="display: none;"></div>
                        </div>
                    </div>
                </div>

                <!-- Unified Inbox & Google Reviews -->
                <div class="row g-4">
                    <!-- Left: Unified Social Inbox -->
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="text-warning mb-0">
                                    <i class="fa-solid fa-inbox me-2"></i>Unified Omnichannel Social Inbox
                                </h5>
                                <div class="d-flex gap-1">
                                    <button class="btn btn-outline-secondary btn-sm py-0 px-2" onclick="loadSocialInbox('all')">All</button>
                                    <button class="btn btn-outline-success btn-sm py-0 px-2" onclick="loadSocialInbox('whatsapp')">WA</button>
                                    <button class="btn btn-outline-danger btn-sm py-0 px-2" onclick="loadSocialInbox('instagram')">IG</button>
                                    <button class="btn btn-outline-primary btn-sm py-0 px-2" onclick="loadSocialInbox('facebook')">FB</button>
                                    <button class="btn btn-outline-danger btn-sm py-0 px-2" onclick="loadSocialInbox('youtube')">YT</button>
                                </div>
                            </div>

                            <div class="table-responsive" style="max-height: 420px; overflow-y: auto;">
                                <table class="table table-dark table-hover mb-0 align-middle">
                                    <thead>
                                        <tr class="text-warning small text-uppercase">
                                           <th>Channel</th>
                                           <th>Sender</th>
                                           <th>Customer Message</th>
                                           <th>Status</th>
                                           <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="socialInboxBody">
                                        <!-- Loaded dynamically -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Google Business Reviews Manager -->
                    <div class="col-lg-5">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-warning mb-0">
                                        <i class="fa-brands fa-google text-warning me-2"></i>Google Business 4.9★ Reviews
                                    </h5>
                                    <small class="text-muted">AI Gujarati &amp; English Owner Auto-Responder</small>
                                </div>
                                <span class="badge bg-warning text-dark fw-bold">842 Reviews</span>
                            </div>

                            <div id="googleReviewsContainer" style="max-height: 420px; overflow-y: auto;">
                                <!-- Loaded dynamically -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 12: EXECUTIVE TEAM & SHOP SUB-AGENTS (UNDER CEO ARADHYA) -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="shop-subagents" role="tabpanel">
                <!-- CEO Executive Suite Header Banner -->
                <div class="card card-custom p-4 mb-4">
                    <div class="d-flex justify-content-between align-items-center flex-wrap gap-3">
                        <div>
                            <div class="d-flex align-items-center gap-2 mb-1">
                                <h4 class="text-warning mb-0">
                                    <i class="fa-solid fa-users-gear text-warning me-2"></i>Chamunda Executive Suite &amp; Departmental Sub-Agents
                                </h4>
                                <span class="badge bg-gold text-dark fw-bold px-3 py-1">CEO Command Mode</span>
                            </div>
                            <p class="text-muted mb-0 small">
                                Supreme Commander: <strong>Aradhya (Chief Executive Officer)</strong> • Founder &amp; Master Tech: <strong>Alpesh Sir</strong>
                            </p>
                        </div>
                        <div class="d-flex gap-2 align-items-center">
                            <button class="btn btn-outline-warning btn-sm" onclick="loadSubagentsOverview()">
                                <i class="fa-solid fa-rotate me-1"></i> Refresh Department Telemetry
                            </button>
                            <span class="badge bg-dark border border-warning text-warning px-3 py-2 fs-6">
                                <i class="fa-solid fa-circle-check text-success me-1"></i> 5 Departments Active
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Executive Written Command Terminal (લેખિત આદેશ કન્સોલ) -->
                <div class="card card-custom p-4 mb-4 border border-warning" style="background: linear-gradient(135deg, rgba(26,26,26,0.95), rgba(40,30,15,0.95));">
                    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                        <div class="d-flex align-items-center gap-2">
                            <span class="fs-4">✍️</span>
                            <div>
                                <h5 class="text-warning mb-0">Executive Written Command Terminal / લેખિત આદેશ કન્સોલ</h5>
                                <small class="text-muted">Type any written command in English or Gujarati — CEO Aradhya will parse, route, and execute via the right Sub-Agent</small>
                            </div>
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            <span class="badge bg-gold text-dark fw-bold px-3 py-1"><i class="fa-solid fa-bolt me-1"></i> NLP Command Router</span>
                        </div>
                    </div>

                    <!-- Quick Preset Suggestion Chips -->
                    <div class="mb-3">
                        <small class="text-muted d-block mb-2"><i class="fa-solid fa-lightbulb text-warning me-1"></i> Quick Directives (Click to insert):</small>
                        <div class="d-flex flex-wrap gap-2">
                            <button class="btn btn-sm btn-outline-secondary text-start" onclick="setWrittenCommand('રમેશભાઈ, Classic 350 એન્જિન સાઉન્ડ અને વાલ્વ ટેપેટ ટ્યુનિંગ કરો', 'High')">
                                🛠️ રમેશ: Classic 350 સાઉન્ડ &amp; ટેપેટ ટ્યુનિંગ
                            </button>
                            <button class="btn btn-sm btn-outline-secondary text-start" onclick="setWrittenCommand('જયેશભાઈ, 50 NGK Spark Plugs અને 20 કેન Motul 15W50 નો હોલસેલ PO બનાવો', 'Urgent')">
                                📦 જયેશ: NGK Plugs &amp; Motul 15W50 PO
                            </button>
                            <button class="btn btn-sm btn-outline-secondary text-start" onclick="setWrittenCommand('પ્રિયા, રાઇડર રાહુલને વ્હોટ્સએપ પર સર્વિસ રેડી નોટિફિકેશન મોકલો (+91 78747 19139)', 'Normal')">
                                💬 પ્રિયા: વ્હોટ્સએપ સર્વિસ અપડેટ (+91 78747 19139)
                            </button>
                            <button class="btn btn-sm btn-outline-secondary text-start" onclick="setWrittenCommand('કબીર, હિમાલયન 450 રિસ્ટો-મોડ વિડીયો તમામ 5 સોશિયલ ચેનલ્સ પર પબ્લિશ કરો', 'Normal')">
                                📱 કબીર: હિમાલયન 450 રીલ 5 ચેનલ્સ પર સિન્ડિકેટ
                            </button>
                            <button class="btn btn-sm btn-outline-secondary text-start" onclick="setWrittenCommand('હસમુખભાઈ, ₹4,850 નું GST ટેક્સ ઇન્વોઇસ અને Dynamic UPI QR તૈયાર કરો', 'High')">
                                🧾 હસમુખ: GST ઇન્વોઇસ &amp; UPI QR
                            </button>
                        </div>
                    </div>

                    <!-- Written Command Input Form -->
                    <div class="row g-2 mb-3">
                        <div class="col-md-7">
                            <div class="form-floating">
                                <textarea class="form-control bg-dark text-white border-secondary" placeholder="Type command..." id="writtenCommandText" style="height: 90px;"></textarea>
                                <label for="writtenCommandText" class="text-muted">Type Written Command (English, ગુજરાતી, or mixed)...</label>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="d-flex flex-column gap-2">
                                <div>
                                    <label class="form-label small text-muted mb-1">Commander / Sender</label>
                                    <select class="form-select form-select-sm bg-dark text-white border-secondary" id="writtenCommandSender">
                                        <option value="Alpesh Sir (Founder &amp; Chairman)">Alpesh Sir (Founder &amp; Master Tech)</option>
                                        <option value="Aradhya (Chief Executive Officer)">Aradhya (CEO)</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="form-label small text-muted mb-1">Priority</label>
                                    <select class="form-select form-select-sm bg-dark text-white border-secondary" id="writtenCommandPriority">
                                        <option value="Normal">Normal Priority</option>
                                        <option value="High">High Priority</option>
                                        <option value="Urgent">Urgent / Emergency (તાત્કાલિક)</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-2 d-flex align-items-end">
                            <button class="btn btn-warning w-100 py-3 fw-bold" id="btnExecuteWrittenCommand" onclick="submitWrittenCommand()">
                                <i class="fa-solid fa-paper-plane me-1"></i> Execute Directive<br><small class="fw-normal">આદેશ આપો</small>
                            </button>
                        </div>
                    </div>

                    <!-- Live Execution Feedback Box -->
                    <div id="writtenCommandResultBox" style="display: none;" class="p-3 rounded bg-dark border border-warning">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge bg-warning text-dark fw-bold" id="wcrTargetBadge"><i class="fa-solid fa-user-check me-1"></i> Routed Sub-Agent</span>
                            <span class="badge bg-success" id="wcrStatusBadge">Executed</span>
                        </div>
                        <h6 class="text-white mb-1" id="wcrHeadTitle">Master Tech Ramesh</h6>
                        <div class="alert alert-warning text-dark small py-2 mb-2" id="wcrGuText"></div>
                        <p class="small text-muted mb-0" id="wcrEnText"></p>
                    </div>
                </div>

                <!-- Autonomous Sub-Agent Growth & Self-Healing Matrix (સ્વાયત્ત ગ્રોથ & સેલ્ફ-હીલિંગ મેટ્રિક્સ) -->
                <div class="card card-custom p-4 mb-4 border border-success" style="background: linear-gradient(135deg, rgba(20,35,25,0.95), rgba(15,25,35,0.95));">
                    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
                        <div class="d-flex align-items-center gap-2">
                            <span class="fs-4">🧠</span>
                            <div>
                                <h5 class="text-success mb-0">Autonomous Sub-Agent Growth &amp; Self-Healing Engine</h5>
                                <small class="text-muted">Sub-agents auto-diagnose issues, apply self-healing solutions, and evolve capabilities with persistent XP &amp; Leveling</small>
                            </div>
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            <span class="badge bg-success text-dark fw-bold px-3 py-1"><i class="fa-solid fa-shield-virus me-1"></i> Auto-Update &amp; Healing Active</span>
                        </div>
                    </div>

                    <!-- Growth Profiles Overview Grid (Dynamic via JS) -->
                    <div class="row g-3 mb-3" id="subagentGrowthGrid">
                        <!-- Loaded dynamically from /api/agents/growth -->
                    </div>

                    <!-- Autonomous Incident Simulation & Diagnostic Workbench -->
                    <div class="p-3 bg-dark rounded border border-secondary mt-2">
                        <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                            <h6 class="text-warning mb-0"><i class="fa-solid fa-microchip text-warning me-2"></i>Autonomous Incident Diagnostic &amp; Self-Healing Workbench</h6>
                            <span class="small text-muted">Test how sub-agents formulate &amp; apply solutions themselves</span>
                        </div>

                        <!-- Quick Preset Incident Buttons -->
                        <div class="mb-3">
                            <small class="text-muted d-block mb-1">Simulate Real-World Departmental Roadblocks (Click to trigger):</small>
                            <div class="d-flex flex-wrap gap-2">
                                <button class="btn btn-sm btn-outline-warning" onclick="triggerIncidentSimulation('bay_chief', 'Cold-start valve tappet tick noise on Classic 350 J-Series at 2,800 RPM')">
                                    🛠️ રમેશ: J-Series ટેપેટ અવાજ &amp; વાલ્વ હીલિંગ
                                </button>
                                <button class="btn btn-sm btn-outline-info" onclick="triggerIncidentSimulation('parts_specialist', 'OEM NGK Spark Plug (BPR6ES) out-of-stock across primary distributors')">
                                    📦 જયેશ: NGK પ્લગ સ્ટોક શોર્ટેજ &amp; સબસ્ટીટ્યુટ PO
                                </button>
                                <button class="btn btn-sm btn-outline-success" onclick="triggerIncidentSimulation('customer_receptionist', 'Highway breakdown SOS signal received from stranded rider near Mehsana with weak 2G network')">
                                    💬 પ્રિયા: હાઈવે બ્રેકડાઉન SOS લો-બેન્ડવિડ્થ રિલે
                                </button>
                                <button class="btn btn-sm btn-outline-danger" onclick="triggerIncidentSimulation('social_growth_manager', '1-star critical review on Google Business Profile regarding custom parts delivery time')">
                                    📱 કબીર: ગૂગલ નેગેટિવ રિવ્યુ 5-સ્ટાર રિકવરી
                                </button>
                                <button class="btn btn-sm btn-outline-warning" onclick="triggerIncidentSimulation('accounts_controller', 'Counter POS dynamic UPI QR transaction timed out while customer waiting to collect bike')">
                                    🧾 હસમુખ: UPI QR ટાઈમઆઉટ &amp; NPCI RRN વેરિફિકેશન
                                </button>
                            </div>
                        </div>

                        <!-- Custom Incident Input Form -->
                        <div class="row g-2">
                            <div class="col-md-3">
                                <select class="form-select form-select-sm bg-dark text-white border-secondary" id="healSelectAgent">
                                    <option value="bay_chief">🛠️ Master Tech Ramesh (Workshop)</option>
                                    <option value="parts_specialist">📦 Jayeshbhai (Inventory)</option>
                                    <option value="customer_receptionist">💬 Priya (24/7 Front-Desk)</option>
                                    <option value="social_growth_manager">📱 Kabir (Omnichannel Social)</option>
                                    <option value="accounts_controller">🧾 Hasmukhbhai (Billing &amp; GST)</option>
                                </select>
                            </div>
                            <div class="col-md-7">
                                <input type="text" class="form-control form-control-sm bg-dark text-white border-secondary" id="healIssueText" placeholder="Describe issue or defect to diagnose (English or ગુજરાતી)...">
                            </div>
                            <div class="col-md-2">
                                <button class="btn btn-success btn-sm w-100 fw-bold" id="btnTriggerHeal" onclick="submitCustomHeal()">
                                    <i class="fa-solid fa-wrench me-1"></i> Auto-Heal &amp; Grow
                                </button>
                            </div>
                        </div>

                        <!-- Incident Healing Result Feedback Card -->
                        <div id="healResultCard" style="display: none;" class="mt-3 p-3 rounded bg-black border border-success">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="badge bg-success text-dark fw-bold" id="healAgentBadge">Autonomous Fix Applied</span>
                                <span class="badge bg-gold text-dark" id="healXpBadge">+50 XP Earned</span>
                            </div>
                            <h6 class="text-white mb-1" id="healTitle">Incident Neutralized</h6>
                            <p class="small text-muted mb-1"><strong>Root Cause:</strong> <span id="healRootCause"></span></p>
                            <div class="alert alert-success text-dark small py-2 mb-2" id="healAppliedFix"></div>
                            <div class="p-2 rounded bg-dark border border-secondary small text-light mb-1">
                                <strong class="text-warning"><i class="fa-solid fa-star me-1"></i> New Skill Auto-Unlocked &amp; Added to Registry:</strong>
                                <span id="healSkillUnlocked" class="text-info fw-bold"></span>
                            </div>
                            <small class="text-muted" id="healGuText"></small>
                        </div>
                    </div>
                </div>

                <!-- 5 Department Cards Grid -->
                <div class="row g-3 mb-4" id="subagentCardsRow">
                    <!-- 1. Bay Chief -->
                    <div class="col-lg-4 col-md-6">
                        <div class="card card-custom p-3 h-100 border-warning">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <span class="fs-4">🛠️</span>
                                    <div>
                                        <h6 class="text-warning mb-0">Master Workshop &amp; Bay Chief</h6>
                                        <small class="text-muted">માસ્ટર વર્કશોપ &amp; સર્વિસ બે ચીફ</small>
                                    </div>
                                </div>
                                <span class="badge bg-warning text-dark">Active</span>
                            </div>
                            <p class="small text-light mb-2"><strong>Lead:</strong> Master Tech Ramesh (12+ Yrs RE Spec)</p>
                            <div class="small text-muted mb-2">
                                <i class="fa-solid fa-gauge-high me-1 text-warning"></i> 14 Active Job Cards | 99.4% First-Time Fix
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary small mb-3">
                                <strong class="text-warning d-block mb-1">Key Responsibilities:</strong>
                                • 50-Pt Acoustic &amp; Tappet Sound Diagnostics<br>
                                • Service Bay 1-3 Allocation &amp; QC Audit<br>
                                • Vintage Cast-Iron &amp; Resto-Mod Builds
                            </div>
                            <button class="btn btn-sm btn-outline-warning w-100 mt-auto" onclick="openDelegateModal('bay_chief', 'Master Workshop & Bay Chief')">
                                <i class="fa-solid fa-paper-plane me-1"></i> Delegate Directive
                            </button>
                        </div>
                    </div>

                    <!-- 2. Parts Specialist -->
                    <div class="col-lg-4 col-md-6">
                        <div class="card card-custom p-3 h-100 border-info">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <span class="fs-4">📦</span>
                                    <div>
                                        <h6 class="text-info mb-0">Inventory &amp; OEM Parts Specialist</h6>
                                        <small class="text-muted">સ્પેરપાર્ટ્સ &amp; સ્ટોક કમાન્ડર</small>
                                    </div>
                                </div>
                                <span class="badge bg-info text-dark">Active</span>
                            </div>
                            <p class="small text-light mb-2"><strong>Lead:</strong> Jayeshbhai Patel (Senior Spares Controller)</p>
                            <div class="small text-muted mb-2">
                                <i class="fa-solid fa-boxes-stacked me-1 text-info"></i> ₹56.3L MRP Stock | 98.2% Availability
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary small mb-3">
                                <strong class="text-info d-block mb-1">Key Responsibilities:</strong>
                                • 4,469 Genuine Royal Enfield OEM SKUs<br>
                                • Low-Stock Wholesale Purchase Orders<br>
                                • Counterfeit Hologram &amp; Barcode Audit
                            </div>
                            <button class="btn btn-sm btn-outline-info w-100 mt-auto" onclick="openDelegateModal('parts_specialist', 'Inventory & OEM Parts Specialist')">
                                <i class="fa-solid fa-paper-plane me-1"></i> Delegate Directive
                            </button>
                        </div>
                    </div>

                    <!-- 3. Customer Receptionist -->
                    <div class="col-lg-4 col-md-6">
                        <div class="card card-custom p-3 h-100 border-success">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <span class="fs-4">💬</span>
                                    <div>
                                        <h6 class="text-success mb-0">24/7 Front-Desk &amp; WhatsApp Bot</h6>
                                        <small class="text-muted">૨૪/૭ કસ્ટમર રિલેશન્સ &amp; વ્હોટ્સએપ</small>
                                    </div>
                                </div>
                                <span class="badge bg-success">24/7 Active</span>
                            </div>
                            <p class="small text-light mb-2"><strong>Lead:</strong> Priya Sharma (Customer Experience Lead)</p>
                            <div class="small text-muted mb-2">
                                <i class="fa-brands fa-whatsapp me-1 text-success"></i> +91 78747 19139 | 3,420 Riders
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary small mb-3">
                                <strong class="text-success d-block mb-1">Key Responsibilities:</strong>
                                • Live Vehicle Service Job Card Tracking<br>
                                • Priority Advance Bay Booking Reservation<br>
                                • Highway Breakdown Emergency SOS Triage
                            </div>
                            <button class="btn btn-sm btn-outline-success w-100 mt-auto" onclick="openDelegateModal('customer_receptionist', '24/7 Front-Desk & WhatsApp Receptionist')">
                                <i class="fa-solid fa-paper-plane me-1"></i> Delegate Directive
                            </button>
                        </div>
                    </div>

                    <!-- 4. Social Growth Manager -->
                    <div class="col-lg-6 col-md-6">
                        <div class="card card-custom p-3 h-100 border-danger">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <span class="fs-4">🚀</span>
                                    <div>
                                        <h6 class="text-danger mb-0">Omnichannel Digital Brand Manager</h6>
                                        <small class="text-muted">ઓમ્નીચેનલ બ્રાન્ડ &amp; સોશિયલ મેનેજર</small>
                                    </div>
                                </div>
                                <span class="badge bg-danger">Active</span>
                            </div>
                            <p class="small text-light mb-2"><strong>Lead:</strong> Kabir Mehta (Digital Media Lead)</p>
                            <div class="small text-muted mb-2">
                                <i class="fa-solid fa-chart-line me-1 text-danger"></i> 45,162+ Community | 4.9★ Google Rating
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary small mb-3">
                                <strong class="text-danger d-block mb-1">Key Responsibilities:</strong>
                                • 360° Syndication (WhatsApp, Instagram, FB, GBP, YouTube)<br>
                                • YouTube Shorts &amp; Reels Video Content Creation<br>
                                • Google Business Profile 4.9★ AI Review Auto-Replies
                            </div>
                            <button class="btn btn-sm btn-outline-danger w-100 mt-auto" onclick="openDelegateModal('social_growth_manager', 'Omnichannel Digital Brand Manager')">
                                <i class="fa-solid fa-paper-plane me-1"></i> Delegate Directive
                            </button>
                        </div>
                    </div>

                    <!-- 5. Accounts Controller -->
                    <div class="col-lg-6 col-md-12">
                        <div class="card card-custom p-3 h-100 border-warning">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div class="d-flex align-items-center gap-2">
                                    <span class="fs-4">💰</span>
                                    <div>
                                        <h6 class="text-warning mb-0">Billing &amp; Finance Accounts Controller</h6>
                                        <small class="text-muted">એકાઉન્ટ્સ &amp; ફાઇનાન્સ કંટ્રોલર</small>
                                    </div>
                                </div>
                                <span class="badge bg-warning text-dark">Active</span>
                            </div>
                            <p class="small text-light mb-2"><strong>Lead:</strong> Hasmukhbhai Joshi (Senior Financial Auditor)</p>
                            <div class="small text-muted mb-2">
                                <i class="fa-solid fa-qrcode me-1 text-warning"></i> 100% GST Compliance | Dynamic NPCI UPI QR
                            </div>
                            <div class="p-2 bg-dark rounded border border-secondary small mb-3">
                                <strong class="text-warning d-block mb-1">Key Responsibilities:</strong>
                                • Official GST Tax Invoicing &amp; Digital QR Passports<br>
                                • Fast-Track Counter POS Billing &amp; Instant UPI QR<br>
                                • Daily Cash/UPI Reconciliation &amp; Vendor Ledgers
                            </div>
                            <button class="btn btn-sm btn-outline-warning w-100 mt-auto" onclick="openDelegateModal('accounts_controller', 'Billing & Finance Accounts Controller')">
                                <i class="fa-solid fa-paper-plane me-1"></i> Delegate Directive
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Executive Directive Audit Trail -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-warning mb-0">
                                <i class="fa-solid fa-list-check me-2"></i>Executive Directive Log &amp; Delegation History
                            </h5>
                            <small class="text-muted">Directives issued by CEO Aradhya across workshop departments</small>
                        </div>
                        <span class="badge bg-secondary">Real-Time Audit Trail</span>
                    </div>

                    <div class="table-responsive" style="max-height: 420px; overflow-y: auto;">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-warning small text-uppercase">
                                    <th>Directive ID</th>
                                    <th>Department / Sub-Agent</th>
                                    <th>Task Title &amp; Scope</th>
                                    <th>Status</th>
                                    <th>Delegated At</th>
                                    <th>Result Summary</th>
                                </tr>
                            </thead>
                            <tbody id="delegationLogBody">
                                <!-- Loaded dynamically -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Modal for Subagent Task Delegation -->
            <div class="modal fade" id="delegateModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content bg-dark text-light border-warning">
                        <div class="modal-header border-secondary">
                            <h5 class="modal-title text-warning">
                                <i class="fa-solid fa-bullhorn me-2"></i>Issue Executive Directive from CEO Aradhya
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <input type="hidden" id="modalAgentId">
                            <div class="mb-3">
                                <label class="form-label text-muted small">Target Department / Sub-Agent</label>
                                <input type="text" id="modalAgentName" class="form-control bg-dark text-warning border-secondary" readonly>
                            </div>
                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Directive Title</label>
                                <input type="text" id="modalTaskTitle" class="form-control bg-dark text-light border-secondary" placeholder="e.g. Inspect Classic 350 Cold Start Tappet Sound">
                            </div>
                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Detailed Instructions / Scope</label>
                                <textarea id="modalTaskDesc" class="form-control bg-dark text-light border-secondary" rows="4" placeholder="Enter specific instructions, bike models, or execution parameters..."></textarea>
                            </div>
                            <div id="modalDelegationAlert" class="alert alert-info small py-2" style="display: none;"></div>
                        </div>
                        <div class="modal-footer border-secondary">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-gold fw-bold px-4" onclick="submitTaskDelegation()">
                                <i class="fa-solid fa-paper-plane me-1"></i> Dispatch Directive
                            </button>
                        </div>
                    </div>
                </div>
            </div>

    </div>

            <!-- ============================================================= -->
            <!-- TAB 13: 🎙️ HANDS-FREE BAY VOICE TERMINAL -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="bay-voice" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Voice Control Status</small>
                            <div class="fs-4 text-warning fw-bold"><i class="fa-solid fa-microphone me-2"></i>Active Hands-Free</div>
                            <small class="text-success"><i class="fa-solid fa-wifi"></i> Bluetooth Bay Headset Paired</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Active Service Bays</small>
                            <div class="fs-4 text-info fw-bold">3 Bays Monitored</div>
                            <small class="text-light">Bay 1 (J-Series), Bay 2 (Twins), Bay 3 (UCE)</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Multi-Agent Sync</small>
                            <div class="fs-4 text-success fw-bold">4 AI Agents</div>
                            <small class="text-muted">Bay Chief • Spares • Accounts • Reception</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">Official WhatsApp Relay</small>
                            <div class="fs-4 text-danger fw-bold">+91 78747 19139</div>
                            <small class="text-muted">Instant rider stage alerts</small>
                        </div>
                    </div>
                </div>

                <!-- Voice Input Studio & Simulation Console -->
                <div class="card card-custom p-4 mb-4 border-warning">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-warning mb-0">
                                <i class="fa-solid fa-headset me-2"></i>Mechanic Hands-Free Voice-to-Action Console
                            </h5>
                            <small class="text-muted">Designed for grease-handed mechanics: Speak or simulate natural Gujarati/English workshop commands</small>
                        </div>
                        <span class="badge bg-warning text-dark px-3 py-2 fw-bold">
                            <i class="fa-solid fa-signal me-1"></i> Live Audio Stream
                        </span>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-8">
                            <label class="form-label text-light fw-bold">Spoken Audio Command (Speech-to-Text Transcription)</label>
                            <div class="input-group">
                                <span class="input-group-text bg-dark border-secondary text-warning">
                                    <i class="fa-solid fa-microphone"></i>
                                </span>
                                <input type="text" id="bayVoiceInput" class="form-control bg-dark text-light border-secondary"
                                       placeholder="e.g. આરાધ્યા, ગાડી નંબર GJ-02-BQ-1234 માં લિક્વી મોલી 15W-50 એન્જિન ઓઇલ અને નવું ઓઇલ ફિલ્ટર નાખી દીધું છે, બિલમાં એડ કરી દો">
                                <button class="btn btn-warning fw-bold px-4" type="button" onclick="submitBayVoiceCommand()">
                                    <i class="fa-solid fa-bolt me-1"></i> Execute Action
                                </button>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label text-light fw-bold">Bay &amp; Mechanic</label>
                            <select id="bayMechanicSelect" class="form-select bg-dark text-light border-secondary">
                                <option value="Master Tech Ramesh" selected>Master Tech Ramesh (Bay 1 • J-Series)</option>
                                <option value="Tech Kiritbhai">Tech Kiritbhai (Bay 2 • 650 Twins)</option>
                                <option value="Tech Nareshbhai">Tech Nareshbhai (Bay 3 • UCE &amp; CI Rebuild)</option>
                            </select>
                        </div>
                    </div>

                    <!-- Quick Voice Prompt Chips -->
                    <div class="d-flex flex-wrap gap-2 mb-3">
                        <span class="text-muted small align-self-center me-1">Quick Gujarati Voice Presets:</span>
                        <button class="btn btn-sm btn-outline-secondary" onclick="setVoicePrompt('આરાધ્યા, ગાડી નંબર GJ-02-BQ-1234 માં લિક્વી મોલી 15W-50 એન્જિન ઓઇલ અને નવું ઓઇલ ફિલ્ટર નાખી દીધું છે, બિલમાં એડ કરી દો.')">
                            🛢️ ઓઇલ &amp; ફિલ્ટર (GJ-02-BQ-1234)
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="setVoicePrompt('આરાધ્યા, Hunter 350 GJ-02-CD-5678 માં નવા ફ્રન્ટ બ્રેક પેડ નાખી દીધા છે અને ટેપેટ સાઉન્ડ 0.18mm પર સેટ કરી દીધો છે.')">
                            🛑 બ્રેક પેડ &amp; ટેપેટ (GJ-02-CD-5678)
                        </button>
                        <button class="btn btn-sm btn-outline-secondary" onclick="setVoicePrompt('આરાધ્યા, Classic 350 GJ-02-EF-9012 માં હાઇ-પ્રેશર ફોમ વોશ અને ચેઇન લ્યુબ પૂરું થઈ ગયું છે, ડિલિવરી માટે તૈયાર છે.')">
                            🧼 ફોમ વોશ &amp; રેડી (GJ-02-EF-9012)
                        </button>
                    </div>

                    <!-- Voice Response Feedback Box -->
                    <div id="voiceFeedbackBox" class="p-3 bg-dark rounded border border-warning" style="display: none;">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="text-warning mb-0"><i class="fa-solid fa-volume-high me-2"></i>Synthesized Audio Headset Feedback</h6>
                            <span id="voiceLogIdBadge" class="badge bg-warning text-dark"></span>
                        </div>
                        <div class="row g-2">
                            <div class="col-md-6">
                                <div class="p-2 bg-black rounded border border-secondary">
                                    <small class="text-muted d-block fw-bold">🔊 Audio Response (ગુજરાતી):</small>
                                    <span id="voiceGuFeedback" class="text-light"></span>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="p-2 bg-black rounded border border-secondary">
                                    <small class="text-muted d-block fw-bold">🔊 Audio Response (English):</small>
                                    <span id="voiceEnFeedback" class="text-light"></span>
                                </div>
                            </div>
                        </div>
                        <div class="mt-3 p-2 bg-black rounded border border-secondary small" id="voiceSyncReport"></div>
                    </div>
                </div>

                <!-- Voice Execution Audit Trail -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-warning mb-0"><i class="fa-solid fa-list me-2"></i>Hands-Free Bay Voice Execution History</h5>
                        <button class="btn btn-sm btn-outline-warning" onclick="loadBayVoiceLogs()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-warning small text-uppercase">
                                    <th>Log ID</th>
                                    <th>Timestamp</th>
                                    <th>Mechanic &amp; Bay</th>
                                    <th>Vehicle Reg</th>
                                    <th>Spoken Command</th>
                                    <th>Action &amp; Spares</th>
                                    <th>Bill Impact</th>
                                </tr>
                            </thead>
                            <tbody id="voiceLogsTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading bay voice logs...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 14: 📦 B2B WHOLESALE SPARES NETWORK -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="b2b-wholesale" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Partner Garages</small>
                            <div class="fs-4 text-info fw-bold" id="b2bGaragesCount">5 Garages</div>
                            <small class="text-muted">Across North Gujarat</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">B2B Wholesale Revenue</small>
                            <div class="fs-4 text-success fw-bold" id="b2bRevenueVal">₹12,071.40</div>
                            <small class="text-success"><i class="fa-solid fa-arrow-trend-up"></i> Tiered Wholesale Margins</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Delivery Van Routes</small>
                            <div class="fs-4 text-warning fw-bold">3 Daily Express Routes</div>
                            <small class="text-light">Highway, Industrial &amp; GIDC</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">WhatsApp B2B PO Line</small>
                            <div class="fs-4 text-danger fw-bold">+91 78747 19139</div>
                            <small class="text-muted">Instant PO Quoting</small>
                        </div>
                    </div>
                </div>

                <!-- North Gujarat Partner Garages Directory -->
                <div class="card card-custom p-4 mb-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-info mb-0">
                                <i class="fa-solid fa-warehouse me-2"></i>North Gujarat B2B Partner Garages &amp; Wholesalers
                            </h5>
                            <small class="text-muted">Authorized local garages supplied with 100% genuine Royal Enfield OEM spares</small>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-info" onclick="loadB2BGarages()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                            <button class="btn btn-sm btn-info fw-bold" data-bs-toggle="modal" data-bs-target="#registerGarageModal">
                                <i class="fa-solid fa-plus me-1"></i> Register Partner Garage
                            </button>
                        </div>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-info small text-uppercase">
                                    <th>Garage ID</th>
                                    <th>Garage &amp; Owner</th>
                                    <th>City &amp; Address</th>
                                    <th>Wholesale Tier</th>
                                    <th>Margin</th>
                                    <th>Credit / Outstanding</th>
                                    <th>Preferred Route</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody id="b2bGaragesTableBody">
                                <tr><td colspan="8" class="text-center text-muted py-3">Loading partner garages...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Daily Express Van Delivery Logistics & Routes -->
                <div class="card card-custom p-4 mb-4">
                    <h5 class="text-warning mb-3"><i class="fa-solid fa-truck-fast me-2"></i>Chamunda Spares Daily Delivery Routes</h5>
                    <div class="row g-3" id="b2bRoutesGrid">
                        <!-- Route cards populated by JS -->
                    </div>
                </div>

                <!-- Wholesale Orders & Dispatch Log -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-info mb-0"><i class="fa-solid fa-file-invoice-dollar me-2"></i>Recent B2B Wholesale Invoices &amp; Dispatches</h5>
                        <button class="btn btn-sm btn-outline-info" onclick="loadB2BOrders()"><i class="fa-solid fa-rotate me-1"></i> Refresh Orders</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-info small text-uppercase">
                                    <th>Order ID</th>
                                    <th>Garage</th>
                                    <th>City</th>
                                    <th>Items Ordered</th>
                                    <th>MRP Total</th>
                                    <th>Discount</th>
                                    <th>Net Payable</th>
                                    <th>Status &amp; Route</th>
                                </tr>
                            </thead>
                            <tbody id="b2bOrdersTableBody">
                                <tr><td colspan="8" class="text-center text-muted py-3">Loading wholesale orders...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 15: 🏍️ RIDERS CLUB & AMC PASS MANAGER -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="riders-club" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">Club Members</small>
                            <div class="fs-4 text-danger fw-bold" id="clubMembersCount">4 Members</div>
                            <small class="text-muted">Active AMC Riders</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Annual AMC Revenue</small>
                            <div class="fs-4 text-warning fw-bold" id="clubAmsRev">₹35,496</div>
                            <small class="text-success"><i class="fa-solid fa-shield-halved"></i> Guaranteed Recurring Revenue</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Thump Points Pool</small>
                            <div class="fs-4 text-info fw-bold" id="clubPointsPool">5,700 Pts</div>
                            <small class="text-muted">1 Pt per ₹10 spent</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Upcoming Expeditions</small>
                            <div class="fs-4 text-success fw-bold">2 Rides</div>
                            <small class="text-light">Polo Forest &amp; Nadabet Border</small>
                        </div>
                    </div>
                </div>

                <!-- 3 AMC Plans Cards -->
                <div class="card card-custom p-4 mb-4">
                    <h5 class="text-warning mb-3"><i class="fa-solid fa-id-card-clip me-2"></i>Chamunda Royal Riders Club • AMC Pass Tiers</h5>
                    <div class="row g-3">
                        <div class="col-md-4">
                            <div class="card card-custom p-3 h-100 border-secondary">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h6 class="text-light mb-0">Silver Thump Pass</h6>
                                    <span class="badge bg-secondary">₹3,999/yr</span>
                                </div>
                                <small class="text-muted d-block mb-2">Daily Commuters (Classic 350, Hunter 350)</small>
                                <ul class="small text-light ps-3 mb-3">
                                    <li>3 Periodic Services (Zero Labor)</li>
                                    <li>6 Foam Wash &amp; Chain Lube Sessions</li>
                                    <li>5% Flat Discount on Genuine OEM Parts</li>
                                    <li>1 Acoustic Thump AI Health Passport</li>
                                </ul>
                                <button class="btn btn-sm btn-outline-light w-100 mt-auto" onclick="openClubEnrollModal('AMC-SILVER')">Enroll in Silver</button>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card card-custom p-3 h-100 border-warning">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h6 class="text-warning mb-0">Gold Tourer Pass</h6>
                                    <span class="badge bg-warning text-dark fw-bold">₹7,499/yr</span>
                                </div>
                                <small class="text-muted d-block mb-2">Highway Tourers (Himalayan 450, Meteor 350)</small>
                                <ul class="small text-light ps-3 mb-3">
                                    <li>4 Complete Periodic Services (Zero Labor)</li>
                                    <li>Unlimited Wash &amp; Motul Chain Lube</li>
                                    <li>10% Flat Discount on RE Parts &amp; Touring Gear</li>
                                    <li>24/7 Highway SOS Breakdown Patrol (50 km)</li>
                                    <li>1 Free 3M Teflon Anti-Rust Coating</li>
                                </ul>
                                <button class="btn btn-sm btn-warning w-100 fw-bold mt-auto" onclick="openClubEnrollModal('AMC-GOLD')">Enroll in Gold</button>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card card-custom p-3 h-100 border-danger">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <h6 class="text-danger mb-0">Platinum Vintage &amp; Twin</h6>
                                    <span class="badge bg-danger">₹11,999/yr</span>
                                </div>
                                <small class="text-muted d-block mb-2">650 Twins &amp; Vintage Cast-Iron Bullets</small>
                                <ul class="small text-light ps-3 mb-3">
                                    <li>5 Bespoke Services with Master Tech Ramesh</li>
                                    <li>Unlimited Wash, Detailing &amp; Chain Care</li>
                                    <li>15% Flat Discount on All Parts &amp; Restomods</li>
                                    <li>Free Doorstep Pick &amp; Drop in Mehsana</li>
                                    <li>VIP Priority Bay 1 Scheduling</li>
                                    <li>1 Free Ticket to Annual Heritage Expedition</li>
                                </ul>
                                <button class="btn btn-sm btn-danger w-100 fw-bold mt-auto" onclick="openClubEnrollModal('AMC-PLATINUM')">Enroll in Platinum</button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Active Members Registry & Expeditions Grid -->
                <div class="row g-3">
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="text-warning mb-0"><i class="fa-solid fa-users me-2"></i>Active Club Members</h5>
                                <button class="btn btn-sm btn-outline-warning" onclick="loadClubOverview()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                            </div>
                            <div class="table-responsive">
                                <table class="table table-dark table-hover mb-0 align-middle">
                                    <thead>
                                        <tr class="text-warning small text-uppercase">
                                            <th>Member ID</th>
                                            <th>Rider</th>
                                            <th>Bike Model</th>
                                            <th>Plan Tier</th>
                                            <th>Services Left</th>
                                            <th>Thump Pts</th>
                                        </tr>
                                    </thead>
                                    <tbody id="clubMembersTableBody">
                                        <tr><td colspan="6" class="text-center text-muted py-3">Loading members...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-5">
                        <div class="card card-custom p-4 h-100">
                            <h5 class="text-danger mb-3"><i class="fa-solid fa-map-location-dot me-2"></i>Heritage Touring Expeditions</h5>
                            <div id="clubExpeditionsList">
                                <!-- Populated by JS -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 16: 🔌 OBD-II LIVE IOT SCANNER -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="obd-scanner" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">OBD-II Connection</small>
                            <div class="fs-4 text-info fw-bold"><i class="fa-solid fa-bluetooth me-2"></i>Paired &amp; Live</div>
                            <small class="text-success"><i class="fa-solid fa-check-circle"></i> ISO 15765 CAN Bus Active</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Battery Charging Voltage</small>
                            <div class="fs-4 text-warning fw-bold" id="obdBatteryVal">14.3 V</div>
                            <small class="text-light">Target: 14.2V - 14.5V Healthy</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Engine Idle RPM</small>
                            <div class="fs-4 text-success fw-bold" id="obdRpmVal">1,080 RPM</div>
                            <small class="text-muted">J-Series Sweet Spot (1,050 - 1,120)</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">ECU Diagnostic Health</small>
                            <div class="fs-4 text-danger fw-bold" id="obdHealthStatus">Warning (1 DTC)</div>
                            <small class="text-muted">Master Tech Ramesh Guided Fix</small>
                        </div>
                    </div>
                </div>

                <!-- Live Diagnostic Workbench & DTC Simulator -->
                <div class="card card-custom p-4 mb-4 border-info">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-info mb-0">
                                <i class="fa-solid fa-microchip me-2"></i>Live Royal Enfield ECU Telemetry &amp; DTC Scanner
                            </h5>
                            <small class="text-muted">Real-time CAN bus telemetry stream across J-Series, 650 Twins, and Sherpa 450 platforms</small>
                        </div>
                        <span class="badge bg-info text-dark px-3 py-2 fw-bold">
                            <i class="fa-solid fa-satellite-dish me-1"></i> Bluetooth OBD Dongle
                        </span>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-4">
                            <label class="form-label text-light fw-bold small">Royal Enfield Model Platform</label>
                            <select id="obdBikeModel" class="form-select bg-dark text-light border-secondary">
                                <option value="Classic 350 (Reborn)" selected>Classic 350 (Reborn - J-Series)</option>
                                <option value="Hunter 350">Hunter 350 (J-Series Agile)</option>
                                <option value="Meteor 350">Meteor 350 (J-Series Cruiser)</option>
                                <option value="Interceptor 650">Interceptor 650 (Parallel Twin)</option>
                                <option value="Continental GT 650">Continental GT 650 (Parallel Twin)</option>
                                <option value="Himalayan 450">Himalayan 450 (Sherpa Liquid-Cooled)</option>
                            </select>
                        </div>
                        <div class="col-md-4">
                            <label class="form-label text-light fw-bold small">Vehicle Registration No</label>
                            <input type="text" id="obdRegNo" class="form-control bg-dark text-light border-secondary" value="GJ-02-BQ-1234">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label text-light fw-bold small">Diagnostic Simulation Scenario</label>
                            <div class="input-group">
                                <select id="obdSimulateDtc" class="form-select bg-dark text-light border-secondary">
                                    <option value="P0505" selected>P0505: Idle Air Control / Stepper Carbon</option>
                                    <option value="P0130">P0130: Oxygen (O2) Lambda Sensor Circuit</option>
                                    <option value="P0115">P0115: Engine Temperature Sensor Open</option>
                                    <option value="P0300">P0300: Ignition Misfire / Fouled Plug</option>
                                    <option value="P0562">P0562: System Low Voltage (&lt;11.8V)</option>
                                    <option value="P0105">P0105: MAP Sensor Vacuum Leak</option>
                                    <option value="HEALTHY">Optimal (Zero DTCs Showroom Tune)</option>
                                </select>
                                <button class="btn btn-info fw-bold" onclick="runOBDScan()">
                                    <i class="fa-solid fa-play me-1"></i> Scan ECU
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Telemetry Gauges Row -->
                    <div class="row g-2 mb-3">
                        <div class="col-md-2 col-6">
                            <div class="p-2 bg-dark rounded border border-secondary text-center">
                                <small class="text-muted d-block">Throttle (TPS)</small>
                                <span class="fs-5 text-warning fw-bold" id="obdTpsVal">0.0%</span>
                            </div>
                        </div>
                        <div class="col-md-2 col-6">
                            <div class="p-2 bg-dark rounded border border-secondary text-center">
                                <small class="text-muted d-block">Engine Temp</small>
                                <span class="fs-5 text-danger fw-bold" id="obdTempVal">92°C</span>
                            </div>
                        </div>
                        <div class="col-md-2 col-6">
                            <div class="p-2 bg-dark rounded border border-secondary text-center">
                                <small class="text-muted d-block">O2 Sensor</small>
                                <span class="fs-5 text-info fw-bold" id="obdO2Val">0.68 V</span>
                            </div>
                        </div>
                        <div class="col-md-2 col-6">
                            <div class="p-2 bg-dark rounded border border-secondary text-center">
                                <small class="text-muted d-block">Manifold MAP</small>
                                <span class="fs-5 text-success fw-bold" id="obdMapVal">42 kPa</span>
                            </div>
                        </div>
                        <div class="col-md-4 col-12">
                            <div class="p-2 bg-dark rounded border border-secondary">
                                <small class="text-muted d-block">ECU Identification:</small>
                                <span class="small text-light fw-bold" id="obdEcuId">RE-BOSCH-MSE6.0-J1 (FW: v1.4.2-2026)</span>
                            </div>
                        </div>
                    </div>

                    <!-- DTC Result & Guided Fix Card -->
                    <div id="obdResultCard" class="p-3 bg-dark rounded border border-info" style="display: none;">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="text-info mb-0" id="obdResultTitle">DTC Diagnosis Result</h6>
                            <span id="obdScanIdBadge" class="badge bg-info text-dark"></span>
                        </div>
                        <div id="obdDtcList" class="mb-3"></div>
                        <div class="p-2 bg-black rounded border border-secondary small mb-2" id="obdDiagnosisGu"></div>
                        <div class="small text-muted" id="obdDiagnosisEn"></div>
                    </div>
                </div>

                <!-- Recent OBD Scans Table -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-info mb-0"><i class="fa-solid fa-clock-rotate-left me-2"></i>Recent ECU Diagnostic Scans</h5>
                        <button class="btn btn-sm btn-outline-info" onclick="loadRecentOBDScans()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-info small text-uppercase">
                                    <th>Scan ID</th>
                                    <th>Timestamp</th>
                                    <th>Motorcycle &amp; Reg</th>
                                    <th>Platform &amp; ECU</th>
                                    <th>Battery / RPM</th>
                                    <th>Health &amp; DTCs</th>
                                </tr>
                            </thead>
                            <tbody id="obdScansTableBody">
                                <tr><td colspan="6" class="text-center text-muted py-3">Loading scans...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 17: 🖥️ SMART LOUNGE SELF-CHECK-IN KIOSK -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="smart-kiosk" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Lounge Kiosk Terminal</small>
                            <div class="fs-4 text-warning fw-bold"><i class="fa-solid fa-display me-2"></i>Touchscreen Live</div>
                            <small class="text-success"><i class="fa-solid fa-check"></i> 24/7 Self-Service Intake</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Active Tokens in Queue</small>
                            <div class="fs-4 text-info fw-bold" id="kioskTokensCount">3 Tokens</div>
                            <small class="text-muted">Average turnaround: 45 mins</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Automated Job Cards</small>
                            <div class="fs-4 text-success fw-bold">100% Synced</div>
                            <small class="text-muted">Direct to Master Tech Ramesh</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">WhatsApp Digital Slip</small>
                            <div class="fs-4 text-danger fw-bold">+91 78747 19139</div>
                            <small class="text-muted">Instant token confirmation</small>
                        </div>
                    </div>
                </div>

                <!-- Kiosk Interactive Self-Check-In Panel -->
                <div class="card card-custom p-4 mb-4 border-warning">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-warning mb-0">
                                <i class="fa-solid fa-ticket me-2"></i>Rider Self-Service Express Check-In Console
                            </h5>
                            <small class="text-muted">Welcome screen: Enter vehicle registration to retrieve service history, health passport, and issue queue token</small>
                        </div>
                        <span class="badge bg-warning text-dark fw-bold px-3 py-2">Touch Kiosk Mode</span>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <label class="form-label text-light fw-bold">1. Enter Vehicle Registration Number</label>
                            <div class="input-group">
                                <input type="text" id="kioskRegInput" class="form-control bg-dark text-warning border-secondary fs-5 text-uppercase fw-bold"
                                       placeholder="GJ-02-BQ-1234" value="GJ-02-BQ-1234">
                                <button class="btn btn-warning fw-bold px-4" onclick="lookupKioskVehicle()">
                                    <i class="fa-solid fa-magnifying-glass me-1"></i> Lookup Rider
                                </button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-light fw-bold">Rider Identification</label>
                            <div class="p-2 bg-dark rounded border border-secondary d-flex justify-content-between align-items-center">
                                <div>
                                    <strong class="text-light d-block" id="kioskRiderName">Alpesh Sir</strong>
                                    <small class="text-muted" id="kioskRiderPhone">+91 78747 19139</small>
                                </div>
                                <span class="badge bg-success" id="kioskPassportBadge"><i class="fa-solid fa-certificate me-1"></i> Health Passport 94%</span>
                            </div>
                        </div>
                    </div>

                    <!-- Issues Selection Checklist -->
                    <div class="mb-3">
                        <label class="form-label text-light fw-bold small">2. Select Service Symptoms &amp; Directives (Touch to Select)</label>
                        <div class="d-flex flex-wrap gap-2" id="kioskIssuesChecklist">
                            <div class="form-check form-check-inline bg-dark p-2 rounded border border-secondary text-light">
                                <input class="form-check-input ms-1" type="checkbox" id="chkPeriodic" value="Periodic 10,000 km Service" checked>
                                <label class="form-check-label ms-2" for="chkPeriodic">🛠️ Periodic Service</label>
                            </div>
                            <div class="form-check form-check-inline bg-dark p-2 rounded border border-secondary text-light">
                                <input class="form-check-input ms-1" type="checkbox" id="chkOil" value="Engine Oil &amp; Filter Change" checked>
                                <label class="form-check-label ms-2" for="chkOil">🛢️ Oil &amp; Filter</label>
                            </div>
                            <div class="form-check form-check-inline bg-dark p-2 rounded border border-secondary text-light">
                                <input class="form-check-input ms-1" type="checkbox" id="chkTappet" value="50-Pt Acoustic Tappet Sound Calibration">
                                <label class="form-check-label ms-2" for="chkTappet">🔊 Tappet Sound Check</label>
                            </div>
                            <div class="form-check form-check-inline bg-dark p-2 rounded border border-secondary text-light">
                                <input class="form-check-input ms-1" type="checkbox" id="chkBrake" value="Brake Pad Inspection / Replacement">
                                <label class="form-check-label ms-2" for="chkBrake">🛑 Brake Inspection</label>
                            </div>
                            <div class="form-check form-check-inline bg-dark p-2 rounded border border-secondary text-light">
                                <input class="form-check-input ms-1" type="checkbox" id="chkChain" value="High-Pressure Wash &amp; Chain Polishing" checked>
                                <label class="form-check-label ms-2" for="chkChain">🧼 Foam Wash &amp; Lube</label>
                            </div>
                        </div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <span class="small text-muted">Estimated service turnaround: ~45 Minutes in Bay 1</span>
                        <button class="btn btn-warning fw-bold px-4 py-2 fs-6" onclick="submitKioskCheckin()">
                            <i class="fa-solid fa-print me-2"></i> Generate Token &amp; Start Service
                        </button>
                    </div>

                    <!-- Token Confirmation Modal Box -->
                    <div id="kioskTokenGeneratedAlert" class="mt-3 p-3 bg-dark rounded border border-warning" style="display: none;">
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h5 class="text-warning mb-0"><i class="fa-solid fa-circle-check me-2 text-success"></i>Service Token Confirmed!</h5>
                            <span class="badge bg-warning text-dark fs-6" id="kioskTokenIdDisplay"></span>
                        </div>
                        <p class="small text-light mb-2" id="kioskTokenDetails"></p>
                        <div class="p-2 bg-black rounded border border-secondary small text-success">
                            <i class="fa-brands fa-whatsapp me-1"></i> WhatsApp Digital Token slip dispatched to rider via <strong>+91 78747 19139</strong>.
                        </div>
                    </div>
                </div>

                <!-- Recent Tokens Queue Table -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-warning mb-0"><i class="fa-solid fa-list-ol me-2"></i>Active Workshop Queue &amp; Bay Slots</h5>
                        <button class="btn btn-sm btn-outline-warning" onclick="loadKioskTokens()"><i class="fa-solid fa-rotate me-1"></i> Refresh Queue</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-warning small text-uppercase">
                                    <th>Token ID</th>
                                    <th>Timestamp</th>
                                    <th>Rider</th>
                                    <th>Motorcycle</th>
                                    <th>Assigned Bay</th>
                                    <th>Lead Tech</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="kioskTokensTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading queue tokens...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 18: 📈 PREDICTIVE SUPPLY CHAIN & AUTO-PO -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="supply-chain" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Total Catalog SKUs</small>
                            <div class="fs-4 text-success fw-bold">4,469 SKUs</div>
                            <small class="text-light">90,474 Units Stocked</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">Critical Shortage SKUs</small>
                            <div class="fs-4 text-danger fw-bold" id="supplyCriticalCount">2 SKUs</div>
                            <small class="text-danger">&lt;2 Days Runway Remaining</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Demand Multiplier</small>
                            <div class="fs-4 text-warning fw-bold" id="supplyMultiplier">2.5x Festive Rush</div>
                            <small class="text-muted">Dhanteras / Diwali Mode</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Auto-Generated POs</small>
                            <div class="fs-4 text-info fw-bold" id="supplyPoCount">1 PO Dispatched</div>
                            <small class="text-muted">₹148,850 Replenishment</small>
                        </div>
                    </div>
                </div>

                <!-- Forecasting & Auto-PO Workbench -->
                <div class="card card-custom p-4 mb-4 border-success">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-success mb-0">
                                <i class="fa-solid fa-chart-line me-2"></i>AI Festival Demand Forecaster &amp; Auto-PO Generator
                            </h5>
                            <small class="text-muted">Predictive inventory replenishment for Jayeshbhai Patel to guarantee zero stockouts during rush season</small>
                        </div>
                        <div class="d-flex gap-2">
                            <select id="seasonProfileSelect" class="form-select form-select-sm bg-dark text-success border-success fw-bold" onchange="loadSupplyChainForecast()">
                                <option value="diwali_dhanteras_rush" selected>Diwali &amp; Dhanteras Festive Rush (2.5x Demand)</option>
                                <option value="monsoon_touring_season">Monsoon &amp; Ladakh Touring Season (1.8x Demand)</option>
                                <option value="routine_baseline">Routine Monthly Baseline (1.0x Demand)</option>
                            </select>
                            <button class="btn btn-sm btn-success fw-bold px-3 text-nowrap" onclick="submitGenerateAutoPO()">
                                <i class="fa-solid fa-cart-arrow-down me-1"></i> Auto-Generate PO
                            </button>
                        </div>
                    </div>

                    <div id="autoPoAlert" class="alert alert-success small py-2 mb-3" style="display: none;"></div>

                    <!-- At Risk Items Table -->
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-success small text-uppercase">
                                    <th>Part Number</th>
                                    <th>Part Name &amp; Category</th>
                                    <th>Current Stock</th>
                                    <th>Daily Burn Rate</th>
                                    <th>Runway Days</th>
                                    <th>Suggested Reorder</th>
                                    <th>Stockout Urgency</th>
                                </tr>
                            </thead>
                            <tbody id="supplyAtRiskTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading inventory forecast...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Auto-Generated PO History -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-success mb-0"><i class="fa-solid fa-file-invoice me-2"></i>Automated Purchase Orders Dispatched to Depot</h5>
                        <button class="btn btn-sm btn-outline-success" onclick="loadAutoPOs()"><i class="fa-solid fa-rotate me-1"></i> Refresh POs</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-success small text-uppercase">
                                    <th>PO Number</th>
                                    <th>Timestamp</th>
                                    <th>Supplier Depot</th>
                                    <th>Season Scenario</th>
                                    <th>Units Ordered</th>
                                    <th>Total Valuation</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="supplyPosTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading auto POs...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 19: 🧩 3D INTERACTIVE EXPLODED ENGINE SCHEMATICS -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="engine-schematics" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Active Engine Platform</small>
                            <div class="fs-4 text-warning fw-bold" id="schematicPlatformTitle">J-Series 350 SOHC</div>
                            <small class="text-light">Classic, Hunter &amp; Meteor 350</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Assembly Components</small>
                            <div class="fs-4 text-info fw-bold" id="schematicComponentCount">5 Critical Items</div>
                            <small class="text-info">OEM Genuine Catalog Linked</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Critical Factory Torque</small>
                            <div class="fs-4 text-success fw-bold" id="schematicTopTorque">45 Nm (Head Studs)</div>
                            <small class="text-muted">Factory Service Manual Standard</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-primary">
                            <small class="text-muted text-uppercase fw-bold">Stock Availability</small>
                            <div class="fs-4 text-primary fw-bold" id="schematicStockStatus">In Stock (Bin C-04)</div>
                            <small class="text-muted">Radhanpur Rd Master Warehouse</small>
                        </div>
                    </div>
                </div>

                <!-- Platform Assembly Selector Pills -->
                <div class="card card-custom p-3 mb-4 border-warning">
                    <div class="d-flex flex-wrap gap-2 align-items-center justify-content-between">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-warning active" id="btnAsmJ350" onclick="loadSchematicAssembly('ASM-J350-HEAD')">
                                <i class="fa-solid fa-gears me-1"></i> J-Series 350 SOHC Valvetrain
                            </button>
                            <button type="button" class="btn btn-outline-warning" id="btnAsm650" onclick="loadSchematicAssembly('ASM-650-CLUTCH')">
                                <i class="fa-solid fa-circle-nodes me-1"></i> 650 Twin Slipper Clutch
                            </button>
                            <button type="button" class="btn btn-outline-warning" id="btnAsmCI" onclick="loadSchematicAssembly('ASM-CI350-CRANK')">
                                <i class="fa-solid fa-weight-hanging me-1"></i> 1982 Cast-Iron Heavy Crank
                            </button>
                            <button type="button" class="btn btn-outline-warning" id="btnAsmSherpa" onclick="loadSchematicAssembly('ASM-SHERPA-COOLING')">
                                <i class="fa-solid fa-droplet me-1"></i> Sherpa 450 Liquid Cooling
                            </button>
                        </div>
                        <span class="badge bg-black border border-warning text-warning p-2">
                            <i class="fa-solid fa-screwdriver-wrench me-1"></i> Master Tech Ramesh Torque Guide
                        </span>
                    </div>
                </div>

                <!-- 3D Interactive Exploded Diagram Viewport -->
                <div class="card card-custom p-4 mb-4 border-warning">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-warning mb-0" id="schematicDisplayTitle">
                                <i class="fa-solid fa-layer-group me-2"></i>J-Series 350 SOHC Cylinder Head &amp; Valvetrain
                            </h5>
                            <small class="text-muted" id="schematicDisplaySub">Interactive 3D Exploded View &bull; Click components to highlight torque &amp; warehouse bin</small>
                        </div>
                        <span class="badge bg-dark border border-warning text-warning fs-6" id="schematicIdBadge">ASM-J350-HEAD</span>
                    </div>

                    <!-- Visual Exploded Representation Container -->
                    <div class="p-4 bg-black rounded border border-secondary text-center position-relative mb-4" id="schematicViewport" style="min-height: 240px; background: radial-gradient(circle, #1a1e24 0%, #0d0e12 100%);">
                        <div id="schematicVisualCallouts" class="d-flex flex-wrap justify-content-around align-items-center py-4 gap-3">
                            <!-- Populated dynamically by loadSchematicAssembly -->
                        </div>
                    </div>

                    <!-- Technical Specs Grid -->
                    <div class="row g-3 mb-4" id="schematicSpecsContainer">
                        <!-- Populated dynamically -->
                    </div>

                    <!-- Components & Torque Specifications Table -->
                    <h6 class="text-warning text-uppercase small fw-bold mb-2"><i class="fa-solid fa-list-check me-2"></i>Bill of Materials &amp; Factory Torque Specifications</h6>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-warning small text-uppercase">
                                    <th>Item #</th>
                                    <th>OEM Part No</th>
                                    <th>Component Name</th>
                                    <th>Category</th>
                                    <th>Stock &amp; Bin</th>
                                    <th>Factory Torque (Nm)</th>
                                    <th>Master Tech Ramesh Advice</th>
                                </tr>
                            </thead>
                            <tbody id="schematicComponentsTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading schematic components...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 20: 🔬 NON-INVASIVE AI BORESCOPE CYLINDER ENDOSCOPY -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="borescope-inspection" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">Combustion Health Score</small>
                            <div class="fs-4 text-danger fw-bold" id="borescopeScoreCard">64 / 100</div>
                            <small class="text-warning" id="borescopeGradeBadge">Grade C (De-Carb Due)</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Piston Crown Carbon</small>
                            <div class="fs-4 text-warning fw-bold" id="borescopeCarbonCard">0.95 mm Layer</div>
                            <small class="text-muted">Dense Baked Encrustation</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Honing Crosshatch</small>
                            <div class="fs-4 text-success fw-bold" id="borescopeHoneCard">76% Retention</div>
                            <small class="text-muted">Zero Wall Score Scratches</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Treatment Cost</small>
                            <div class="fs-4 text-info fw-bold" id="borescopeCostCard">₹1,450</div>
                            <small class="text-muted">Chemical Soak (No Teardown)</small>
                        </div>
                    </div>
                </div>

                <!-- Borescope Diagnostic Scanner Workbench -->
                <div class="card card-custom p-4 mb-4 border-danger">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-danger mb-0"><i class="fa-solid fa-microscope me-2"></i>Optical Endoscopic Combustion Chamber Inspection</h5>
                            <small class="text-muted">Non-invasive inspection through 14 mm spark plug hole with high-definition digital borescope</small>
                        </div>
                        <span class="badge bg-danger text-light fs-6">Live Optical Probe</span>
                    </div>

                    <div class="row g-3 mb-3">
                        <div class="col-md-3">
                            <label class="form-label text-light small fw-bold">Motorcycle Platform</label>
                            <select id="boreBikeModel" class="form-select bg-dark text-light border-secondary">
                                <option value="Classic 350 (Reborn)" selected>Classic 350 (Reborn)</option>
                                <option value="Hunter 350">Hunter 350</option>
                                <option value="Bullet 350 Standard">Bullet 350 Standard</option>
                                <option value="Meteor 350">Meteor 350</option>
                                <option value="Himalayan 450 (Sherpa)">Himalayan 450 (Sherpa)</option>
                                <option value="Interceptor 650 Twin">Interceptor 650 Twin</option>
                                <option value="Vintage 1982 Cast-Iron 350">Vintage 1982 Cast-Iron 350</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label text-light small fw-bold">Registration Number</label>
                            <input type="text" id="boreRegNo" class="form-control bg-dark text-light border-secondary" value="GJ-02-BQ-1234">
                        </div>
                        <div class="col-md-2">
                            <label class="form-label text-light small fw-bold">Odometer KM</label>
                            <input type="number" id="boreOdoKm" class="form-control bg-dark text-light border-secondary" value="16400">
                        </div>
                        <div class="col-md-4">
                            <label class="form-label text-light small fw-bold">Endoscopic Scenario</label>
                            <select id="boreScenario" class="form-select bg-dark text-light border-secondary">
                                <option value="heavy_carbon_crust" selected>Heavy Carbon Crust (0.95 mm, baked knock risk)</option>
                                <option value="moderate_carbon">Moderate Carbon Film (0.45 mm, minor valve glaze)</option>
                                <option value="pristine_showroom">Pristine Showroom Spec (0.12 mm, perfect hone)</option>
                                <option value="bore_score_damage">Cylinder Wall Scored &amp; Exhaust Valve Leak</option>
                            </select>
                        </div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <span class="small text-muted"><i class="fa-solid fa-circle-info me-1 text-info"></i> Zero teardown needed. Preserves factory engine cylinder head seal.</span>
                        <button class="btn btn-danger fw-bold px-4 py-2" id="btnRunBorescope" onclick="runBorescopeInspection()">
                            <i class="fa-solid fa-video me-2"></i> Run Borescope Optical Scan
                        </button>
                    </div>

                    <!-- Endoscopic Inspection Detailed Output -->
                    <div id="borescopeResultCard" class="mt-4 p-4 bg-dark rounded border border-danger" style="display: none;">
                        <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom border-secondary">
                            <div>
                                <h5 class="text-danger mb-0" id="boreResTitle"><i class="fa-solid fa-clipboard-check me-2"></i>Inspection Report</h5>
                                <small class="text-muted" id="boreResMeta"></small>
                            </div>
                            <span class="badge bg-danger fs-6" id="boreResGradeBadge"></span>
                        </div>

                        <div class="row g-3 mb-3">
                            <div class="col-md-4">
                                <div class="p-3 bg-black rounded border border-secondary">
                                    <h6 class="text-warning small text-uppercase mb-2"><i class="fa-solid fa-fire me-1"></i> Piston Crown Encrustation</h6>
                                    <div class="fs-5 text-light fw-bold" id="boreResCarbonThickness"></div>
                                    <small class="text-muted d-block" id="boreResCarbonDensity"></small>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-warning" id="boreResCarbonProgress" role="progressbar" style="width: 60%;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="p-3 bg-black rounded border border-secondary">
                                    <h6 class="text-success small text-uppercase mb-2"><i class="fa-solid fa-arrows-split-up-and-left me-1"></i> Cylinder Wall Honing</h6>
                                    <div class="fs-5 text-light fw-bold" id="boreResHonePct"></div>
                                    <small class="text-muted d-block" id="boreResGlaze"></small>
                                    <div class="progress mt-2" style="height: 6px;">
                                        <div class="progress-bar bg-success" id="boreResHoneProgress" role="progressbar" style="width: 80%;"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="p-3 bg-black rounded border border-secondary">
                                    <h6 class="text-info small text-uppercase mb-2"><i class="fa-solid fa-ring me-1"></i> Valve Sealing Margins</h6>
                                    <div class="small text-light" id="boreResIntakeValve"></div>
                                    <div class="small text-warning" id="boreResExhaustValve"></div>
                                    <small class="text-muted d-block mt-1" id="boreResValveStatus"></small>
                                </div>
                            </div>
                        </div>

                        <div class="p-3 bg-black rounded border border-warning mb-3">
                            <div class="d-flex justify-content-between align-items-center mb-1">
                                <h6 class="text-warning mb-0"><i class="fa-solid fa-prescription-bottle-medical me-2"></i>Prescribed Non-Invasive Treatment</h6>
                                <span class="badge bg-warning text-dark fw-bold fs-6" id="boreResCost"></span>
                            </div>
                            <p class="small text-light mb-0" id="boreResTreatment"></p>
                        </div>

                        <div class="p-3 bg-black rounded border border-secondary mb-3">
                            <h6 class="text-info small text-uppercase mb-1"><i class="fa-solid fa-user-gear me-2"></i>Master Tech Ramesh Mechanical Verdict</h6>
                            <p class="small text-warning mb-1" id="boreResVerdictGu"></p>
                            <p class="small text-muted mb-0" id="boreResVerdictEn"></p>
                        </div>

                        <div class="p-2 bg-black rounded border border-success small text-success">
                            <i class="fa-brands fa-whatsapp me-1"></i> WhatsApp Inspection Report &amp; De-carb quotation dispatched to customer via <strong>+91 78747 19139</strong>.
                        </div>
                    </div>
                </div>

                <!-- Recent Borescope Inspections Table -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-danger mb-0"><i class="fa-solid fa-clock-rotate-left me-2"></i>Recent Endoscopic Inspections</h5>
                        <button class="btn btn-sm btn-outline-danger" onclick="loadBorescopeHistory()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-danger small text-uppercase">
                                    <th>Inspection ID</th>
                                    <th>Timestamp</th>
                                    <th>Motorcycle</th>
                                    <th>Reg No</th>
                                    <th>Odometer</th>
                                    <th>Health Score</th>
                                    <th>Grade</th>
                                    <th>Piston Carbon</th>
                                </tr>
                            </thead>
                            <tbody id="borescopeHistoryTableBody">
                                <tr><td colspan="8" class="text-center text-muted py-3">Loading borescope history...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 21: 🏢 MULTI-BRANCH CLOUD NETWORK & FRANCHISE OS -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="multibranch-hub" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Consolidated Revenue Today</small>
                            <div class="fs-4 text-info fw-bold" id="mbNetworkRevenue">₹187,000</div>
                            <small class="text-success"><i class="fa-solid fa-arrow-trend-up"></i> North Gujarat Network</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Active Service Bays</small>
                            <div class="fs-4 text-success fw-bold" id="mbActiveBays">15 Bays Active</div>
                            <small class="text-light">Mehsana, Patan, Visnagar, Unjha, Palanpur</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Network Jobs Handled</small>
                            <div class="fs-4 text-warning fw-bold" id="mbTodayJobs">70 Motorcycles</div>
                            <small class="text-muted">Today's Total Throughput</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-primary">
                            <small class="text-muted text-uppercase fw-bold">Network Spares Valuation</small>
                            <div class="fs-4 text-primary fw-bold" id="mbInventoryValuation">₹5,775,000</div>
                            <small class="text-muted">Unified OEM Parts Catalog</small>
                        </div>
                    </div>
                </div>

                <!-- 5 North Gujarat Branches Status Cards -->
                <div class="card card-custom p-4 mb-4 border-info">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h5 class="text-info mb-0"><i class="fa-solid fa-map-location-dot me-2"></i>North Gujarat Franchise Branch Network</h5>
                            <small class="text-muted">Real-time telemetry and operational heartbeat across 5 strategic locations</small>
                        </div>
                        <button class="btn btn-sm btn-outline-info" onclick="loadMultiBranchOverview()"><i class="fa-solid fa-rotate me-1"></i> Sync Cloud</button>
                    </div>
                    <div class="row g-3" id="mbBranchesGrid">
                        <!-- Populated dynamically by loadMultiBranchOverview -->
                    </div>
                </div>

                <!-- Intra-Branch Stock Transfer Requisition Workbench -->
                <div class="card card-custom p-4 mb-4 border-warning">
                    <h5 class="text-warning mb-3"><i class="fa-solid fa-truck-ramp-box me-2"></i>Intra-Branch Spares Requisition &amp; Transfer Dispatcher</h5>
                    <div class="row g-3 mb-3">
                        <div class="col-md-3">
                            <label class="form-label text-light small fw-bold">Origin / Source Branch</label>
                            <select id="mbFromBranch" class="form-select bg-dark text-light border-secondary">
                                <option value="HQ-MEHSANA" selected>HQ-MEHSANA (Radhanpur Rd Central Warehouse)</option>
                                <option value="BR-PATAN-01">BR-PATAN-01 (Patan Heritage Hub)</option>
                                <option value="BR-VISN-02">BR-VISN-02 (Visnagar Express Bay)</option>
                                <option value="BR-UNJHA-03">BR-UNJHA-03 (Unjha Spares Depot)</option>
                                <option value="BR-PALAN-04">BR-PALAN-04 (Palanpur Highway Outpost)</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label text-light small fw-bold">Destination Branch</label>
                            <select id="mbToBranch" class="form-select bg-dark text-light border-secondary">
                                <option value="BR-PATAN-01" selected>BR-PATAN-01 (Patan Heritage Hub)</option>
                                <option value="BR-VISN-02">BR-VISN-02 (Visnagar Express Bay)</option>
                                <option value="BR-UNJHA-03">BR-UNJHA-03 (Unjha Spares Depot)</option>
                                <option value="BR-PALAN-04">BR-PALAN-04 (Palanpur Highway Outpost)</option>
                                <option value="HQ-MEHSANA">HQ-MEHSANA (Central Warehouse Return)</option>
                            </select>
                        </div>
                        <div class="col-md-3">
                            <label class="form-label text-light small fw-bold">OEM Part Number</label>
                            <input type="text" id="mbPartNumber" class="form-control bg-dark text-light border-secondary" value="574012/A">
                        </div>
                        <div class="col-md-1">
                            <label class="form-label text-light small fw-bold">Qty</label>
                            <input type="number" id="mbQuantity" class="form-control bg-dark text-light border-secondary" value="2" min="1">
                        </div>
                        <div class="col-md-2">
                            <label class="form-label text-light small fw-bold">Requested By</label>
                            <input type="text" id="mbRequestedBy" class="form-control bg-dark text-light border-secondary" value="Branch Lead">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Transfer Reason / Job Card Ref</label>
                        <input type="text" id="mbTransferNotes" class="form-control bg-dark text-light border-secondary" value="Urgent express delivery for Classic Reborn engine rebuild.">
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <span class="small text-muted"><i class="fa-solid fa-barcode me-1 text-warning"></i> Generates intra-branch transfer waybill with digital tracking ID.</span>
                        <button class="btn btn-warning fw-bold px-4 py-2" id="btnDispatchTransfer" onclick="submitBranchTransfer()">
                            <i class="fa-solid fa-paper-plane me-2"></i> Dispatch Stock Transfer
                        </button>
                    </div>

                    <div id="mbTransferAlert" class="mt-3 p-3 bg-dark rounded border border-warning" style="display:none;"></div>
                </div>

                <!-- Recent Transfers Log Table -->
                <div class="card card-custom p-4">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="text-info mb-0"><i class="fa-solid fa-dolly me-2"></i>Intra-Branch Transit &amp; Waybill Log</h5>
                        <button class="btn btn-sm btn-outline-info" onclick="loadMultiBranchOverview()"><i class="fa-solid fa-rotate me-1"></i> Refresh Log</button>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover mb-0 align-middle">
                            <thead>
                                <tr class="text-info small text-uppercase">
                                    <th>Transfer ID</th>
                                    <th>Timestamp</th>
                                    <th>Route</th>
                                    <th>Part Number &amp; Name</th>
                                    <th>Quantity</th>
                                    <th>Valuation</th>
                                    <th>Status</th>
                                    <th>Requested By</th>
                                </tr>
                            </thead>
                            <tbody id="mbTransfersTableBody">
                                <tr><td colspan="8" class="text-center text-muted py-3">Loading transfers...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 22: 👁️ WEBAR LIVE CAMERA ENGINE OVERLAY & TORQUE GUIDE -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="webar-guide" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">AR Optical Tracking Engine</small>
                            <div class="fs-4 text-warning fw-bold">Divya-Drishti 4K</div>
                            <small class="text-success"><i class="fa-solid fa-satellite-dish"></i> Spatial HUD Active</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Pre-Calibrated Engines</small>
                            <div class="fs-4 text-info fw-bold" id="arTotalEnginesCount">4 Platforms</div>
                            <small class="text-muted">J350, 650 Twin, CI 350, Sherpa 450</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Torque Tolerance Range</small>
                            <div class="fs-4 text-success fw-bold">± 1.0 ~ 2.0 Nm</div>
                            <small class="text-muted">Factory Click-Type Precision</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-danger">
                            <small class="text-muted text-uppercase fw-bold">Warehouse Spares Link</small>
                            <div class="fs-4 text-danger fw-bold">4,469 SKUs</div>
                            <small class="text-muted">Live Stock &amp; Bin Tracking</small>
                        </div>
                    </div>
                </div>

                <div class="row g-4">
                    <!-- Left: Camera Viewport & AR HUD Overlay -->
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 border-warning mb-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-warning mb-0"><i class="fa-solid fa-video me-2"></i>WebAR Spatial Viewport HUD</h5>
                                    <small class="text-muted">Real-time overlay of tightening sequences, torque markers, and socket guides</small>
                                </div>
                                <div class="d-flex gap-2">
                                    <select id="webarAssemblySelect" class="form-select form-select-sm bg-dark text-warning border-warning" style="width: auto;" onchange="selectWebARAssembly(this.value)">
                                        <option value="AR-J350-HEAD" selected>J-Series 350 Cylinder Head (Classic Reborn)</option>
                                        <option value="AR-650-CLUTCH">650 Twin Slipper Clutch Hub (Interceptor/GT)</option>
                                        <option value="AR-VINTAGE-CI-CRANK">1982 Vintage Cast-Iron 350 Crankcase (Bullet)</option>
                                        <option value="AR-SHERPA-450-COOLING">Sherpa 450 Liquid-Cooled Loop (Himalayan 450)</option>
                                    </select>
                                    <button class="btn btn-sm btn-outline-warning" onclick="startWebARCamera()"><i class="fa-solid fa-camera me-1"></i> AR Camera</button>
                                </div>
                            </div>

                            <!-- Interactive AR Canvas Container -->
                            <div class="position-relative bg-black rounded border border-secondary text-center p-2" style="min-height: 380px; overflow: hidden;" id="arViewportContainer">
                                <div class="position-absolute top-0 start-0 m-3 text-start z-3">
                                    <span class="badge bg-danger"><i class="fa-solid fa-circle-dot fa-fade me-1"></i> AR HUD LIVE</span>
                                    <span class="badge bg-dark border border-warning text-warning ms-1" id="arActiveEngineBadge">J-Series 350 SOHC</span>
                                </div>
                                <div class="position-absolute top-0 end-0 m-3 text-end z-3">
                                    <small class="text-light bg-dark px-2 py-1 rounded border border-secondary" id="arResolutionBadge">640 x 480 px</small>
                                </div>

                                <!-- Simulated AR Camera View with Visual Grid and Markers -->
                                <div id="arCameraStage" class="position-relative w-100 h-100 d-flex flex-column justify-content-center align-items-center" style="min-height: 360px; background: radial-gradient(circle, #1a252f 0%, #0c1017 100%);">
                                    <svg id="arSvgOverlay" class="position-absolute top-0 start-0 w-100 h-100" style="pointer-events: none;"></svg>
                                    <div id="arMarkersLayer" class="position-absolute top-0 start-0 w-100 h-100">
                                        <!-- Dynamically injected AR markers -->
                                    </div>
                                    <div class="text-center p-4" id="arPlaceholderMessage">
                                        <i class="fa-solid fa-crosshairs text-warning fs-1 mb-3 opacity-50"></i>
                                        <h6 class="text-light" id="arAssemblyTitleDisplay">J-Series 350 Cylinder Head &amp; Camshaft Valvetrain</h6>
                                        <p class="text-muted small mb-0" id="arAssemblyMethodology">Criss-Cross Diagonal Star Pattern (2-Stage Step Torque)</p>
                                    </div>
                                </div>

                                <div class="position-absolute bottom-0 start-0 end-0 p-2 bg-dark bg-opacity-75 border-top border-secondary text-start small d-flex justify-content-between align-items-center z-3">
                                    <span class="text-warning" id="arRameshAdvisoryText"><i class="fa-solid fa-user-ninja me-1"></i> <strong>માસ્ટર ટેક રમેશ:</strong> ૧ થી ૪ ક્રમમાં જ બોલ્ટ ટાઈટ કરો. 22 Nm ➔ 45 Nm.</span>
                                    <button class="btn btn-xs btn-outline-info" onclick="dispatchArSpecToWhatsApp()"><i class="fa-brands fa-whatsapp me-1"></i> WhatsApp Specs</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Bolt Sequence, Factory Torque & Warehouse Stock Linkage -->
                    <div class="col-lg-5">
                        <div class="card card-custom p-4 border-info mb-4">
                            <h5 class="text-info mb-3"><i class="fa-solid fa-list-ol me-2"></i>Torque Specs &amp; Tightening Step Matrix</h5>
                            <div class="table-responsive" style="max-height: 380px; overflow-y: auto;">
                                <table class="table table-dark table-hover align-middle small mb-0">
                                    <thead>
                                        <tr class="text-secondary">
                                            <th>#</th>
                                            <th>Marker / Bolt</th>
                                            <th>Torque</th>
                                            <th>Socket / Chemical</th>
                                            <th>Live Stock</th>
                                        </tr>
                                    </thead>
                                    <tbody id="arSequenceTableBody">
                                        <tr><td colspan="5" class="text-center text-muted py-3">Loading AR torque specs...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div class="card card-custom p-3 border-secondary" id="arSelectedMarkerCard">
                            <h6 class="text-warning mb-2"><i class="fa-solid fa-circle-info me-2"></i>Selected Bolt Guidance &amp; Spares Bin</h6>
                            <div id="arSelectedMarkerContent" class="small text-muted">
                                Click on any AR marker circle above to view exact socket sizes, Loctite grades, and workshop bin location.
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 23: 🌙 24/7 NIGHT HIGHWAY EMERGENCY SPARES LOCKER -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="night-locker" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">Highway Locker Station</small>
                            <div class="fs-4 text-info fw-bold">CHAMUNDA-HQ-01</div>
                            <small class="text-success"><i class="fa-solid fa-bolt me-1"></i> Radhanpur Road Corridor</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">Smart Lockers Status</small>
                            <div class="fs-4 text-success fw-bold" id="nlkAvailableCount">8 Bays Ready</div>
                            <small class="text-muted" id="nlkTelemetryStatus">Online • Temp: 26.8°C • UPS: 98%</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Midnight Sales Revenue</small>
                            <div class="fs-4 text-warning fw-bold" id="nlkTotalRevenue">₹0.00</div>
                            <small class="text-muted" id="nlkTotalTxns">0 Cashless Transactions</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-primary">
                            <small class="text-muted text-uppercase fw-bold">Emergency WhatsApp Bot</small>
                            <div class="fs-4 text-primary fw-bold">+91 78747 19139</div>
                            <small class="text-muted">Instant Dynamic UPI &amp; OTP</small>
                        </div>
                    </div>
                </div>

                <div class="row g-4 mb-4">
                    <!-- Left: 8 Physical Smart Locker Compartments Grid -->
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 border-info">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-info mb-0"><i class="fa-solid fa-boxes-stacked me-2"></i>Exterior Smart Locker Compartment Bays</h5>
                                    <small class="text-muted">High-security solenoid lock compartments outside Radhanpur Road workshop</small>
                                </div>
                                <button class="btn btn-sm btn-outline-info" onclick="loadNightLockerStatus()"><i class="fa-solid fa-rotate me-1"></i> Refresh Bays</button>
                            </div>
                            <div class="row g-3" id="nlkCompartmentsGrid">
                                <!-- Populated dynamically by loadNightLockerStatus -->
                            </div>
                        </div>
                    </div>

                    <!-- Right: Instant Reserve & Solenoid Unlock Terminal -->
                    <div class="col-lg-5">
                        <!-- Step 1: Emergency Reserve Panel -->
                        <div class="card card-custom p-4 border-warning mb-4">
                            <h5 class="text-warning mb-3"><i class="fa-solid fa-cart-plus me-2"></i>Midnight Emergency Spares Dispatch</h5>
                            <div class="row g-2 mb-2">
                                <div class="col-6">
                                    <label class="form-label text-light small fw-bold">Select Locker Bay</label>
                                    <select id="nlkReserveBoxSelect" class="form-select bg-dark text-light border-secondary">
                                        <option value="BOX-01">BOX-01: HD Clutch Cable (₹340)</option>
                                        <option value="BOX-02">BOX-02: Throttle Cable Set (₹290)</option>
                                        <option value="BOX-03">BOX-03: Twin Spark Plugs NGK (₹480)</option>
                                        <option value="BOX-04">BOX-04: Starter &amp; Headlamp Relay (₹380)</option>
                                        <option value="BOX-05">BOX-05: Liqui Moly 15W-50 Oil 1L (₹850)</option>
                                        <option value="BOX-06">BOX-06: Heavy Tube 3.50-19 (₹420)</option>
                                        <option value="BOX-07">BOX-07: CO2 Quick Inflator Kit (₹650)</option>
                                        <option value="BOX-08">BOX-08: Master Link 530 O-Ring (₹220)</option>
                                    </select>
                                </div>
                                <div class="col-6">
                                    <label class="form-label text-light small fw-bold">Rider Phone</label>
                                    <input type="text" id="nlkReservePhone" class="form-control bg-dark text-light border-secondary" value="+91 98250 12345">
                                </div>
                            </div>
                            <div class="row g-2 mb-3">
                                <div class="col-6">
                                    <label class="form-label text-light small fw-bold">Customer Name</label>
                                    <input type="text" id="nlkReserveName" class="form-control bg-dark text-light border-secondary" value="Highway Rider">
                                </div>
                                <div class="col-6">
                                    <label class="form-label text-light small fw-bold">Vehicle Reg No</label>
                                    <input type="text" id="nlkReserveReg" class="form-control bg-dark text-light border-secondary" value="GJ-02-BQ-1234">
                                </div>
                            </div>
                            <button class="btn btn-warning fw-bold w-100" id="btnReserveLocker" onclick="submitLockerReservation()">
                                <i class="fa-solid fa-qrcode me-2"></i> Reserve Bay &amp; Generate Dynamic UPI QR
                            </button>
                            <div id="nlkReserveResultAlert" class="mt-3" style="display:none;"></div>
                        </div>

                        <!-- Step 2: Solenoid Relay OTP Unlock Terminal -->
                        <div class="card card-custom p-4 border-success">
                            <h5 class="text-success mb-3"><i class="fa-solid fa-lock-open me-2"></i>Physical 12V Solenoid Unlock Terminal</h5>
                            <div class="row g-2 mb-2">
                                <div class="col-7">
                                    <label class="form-label text-light small fw-bold">Reservation Reference ID</label>
                                    <input type="text" id="nlkUnlockResId" class="form-control bg-dark text-success border-secondary" placeholder="NLK-20260914-XXXX">
                                </div>
                                <div class="col-5">
                                    <label class="form-label text-light small fw-bold">6-Digit Secret OTP</label>
                                    <input type="text" id="nlkUnlockOtp" class="form-control bg-dark text-center text-warning fw-bold fs-5 border-warning" placeholder="654321" maxlength="6">
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">UPI / Cashless Reference</label>
                                <input type="text" id="nlkUnlockPaymentRef" class="form-control bg-dark text-light border-secondary" value="UPI-AUTOCONFIRMED-INSTANT">
                            </div>
                            <button class="btn btn-success fw-bold w-100" id="btnUnlockLocker" onclick="submitLockerUnlock()">
                                <i class="fa-solid fa-key me-2"></i> Trigger 500ms Solenoid Relay Unlock
                            </button>
                            <div id="nlkUnlockResultAlert" class="mt-3" style="display:none;"></div>
                        </div>
                    </div>
                </div>

                <!-- Midnight Highway Spares Audit Log -->
                <div class="card card-custom p-4 border-secondary">
                    <h5 class="text-secondary mb-3"><i class="fa-solid fa-receipt me-2"></i>Midnight Highway Dispenser Ledger &amp; Restock Audit</h5>
                    <div class="table-responsive">
                        <table class="table table-dark table-hover align-middle small mb-0">
                            <thead>
                                <tr class="text-secondary">
                                    <th>Transaction ID</th>
                                    <th>Locker Box</th>
                                    <th>Spares Description</th>
                                    <th>Rider / Vehicle</th>
                                    <th>Amount Paid</th>
                                    <th>Timestamp</th>
                                    <th>Solenoid Relay State</th>
                                </tr>
                            </thead>
                            <tbody id="nlkLedgerTableBody">
                                <tr><td colspan="7" class="text-center text-muted py-3">Loading night dispenser ledger...</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 24: ☁️ CLOUD SHADOW & OFFLINE AGENT MIRROR (PROJECT CHHAYA) -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="cloud-shadow" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-primary">
                            <small class="text-muted text-uppercase fw-bold">Cloud Shadow Cluster</small>
                            <div class="fs-4 text-primary fw-bold" id="cshClusterName">CHAMUNDA-CLOUD-HQ</div>
                            <small class="text-success"><i class="fa-solid fa-satellite-dish me-1"></i> <span id="cshClusterRegion">asia-south1</span></small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success">
                            <small class="text-muted text-uppercase fw-bold">System Sync Mode</small>
                            <div class="fs-4 text-success fw-bold" id="cshSystemMode">ONLINE_MASTER</div>
                            <small class="text-muted" id="cshLastHeartbeat">Heartbeat: Live</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning">
                            <small class="text-muted text-uppercase fw-bold">Mirrored Enterprise SKUs</small>
                            <div class="fs-4 text-warning fw-bold" id="cshMirroredSkus">4,469 SKUs</div>
                            <small class="text-muted" id="cshMirroredValuation">₹5,775,000 Spares Valuation</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info">
                            <small class="text-muted text-uppercase fw-bold">WhatsApp Standby Bot</small>
                            <div class="fs-4 text-info fw-bold">+91 78747 19139</div>
                            <small class="text-muted"><span id="cshQueuedEvents">0</span> Queued Offline Mutations</small>
                        </div>
                    </div>
                </div>

                <div class="row g-4 mb-4">
                    <!-- Left: 6 Autonomous Cloud Replica Agents -->
                    <div class="col-lg-7">
                        <div class="card card-custom p-4 border-primary mb-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-primary mb-0"><i class="fa-solid fa-robot me-2"></i>Autonomous Cloud Replica Agents (24/7 Standby Fleet)</h5>
                                    <small class="text-muted">These replicas guard operations, answer WhatsApp leads, and process queries when laptop is offline</small>
                                </div>
                                <div class="d-flex gap-2">
                                    <button class="btn btn-sm btn-outline-primary" onclick="loadCloudShadowStatus()"><i class="fa-solid fa-rotate me-1"></i> Refresh</button>
                                    <button class="btn btn-sm btn-primary" onclick="triggerCloudShadowSync()"><i class="fa-solid fa-cloud-arrow-up me-1"></i> Push Snapshot</button>
                                </div>
                            </div>

                            <div class="row g-3" id="cshReplicasGrid">
                                <!-- Populated dynamically by loadCloudShadowStatus -->
                            </div>
                        </div>

                        <!-- Queued Offline Mutations & Reconnection Ledger -->
                        <div class="card card-custom p-4 border-secondary">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="text-secondary mb-0"><i class="fa-solid fa-clock-rotate-left me-2"></i>Queued Offline Events &amp; Sync Ledger</h5>
                                <button class="btn btn-sm btn-outline-success" onclick="reconcileCloudShadow()"><i class="fa-solid fa-arrows-rotate me-1"></i> Reconcile Mutations</button>
                            </div>
                            <div class="table-responsive">
                                <table class="table table-dark table-hover align-middle small mb-0">
                                    <thead>
                                        <tr class="text-secondary">
                                            <th>Sync / Event ID</th>
                                            <th>Timestamp</th>
                                            <th>Mutations Applied</th>
                                            <th>Status</th>
                                            <th>Resolution Note</th>
                                        </tr>
                                    </thead>
                                    <tbody id="cshSyncHistoryTableBody">
                                        <tr><td colspan="5" class="text-center text-muted py-3">Loading cloud sync ledger...</td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Right: Offline Remote Query Simulator -->
                    <div class="col-lg-5">
                        <div class="card card-custom p-4 border-warning mb-4 shadow-lg">
                            <h5 class="text-warning mb-2"><i class="fa-solid fa-mobile-screen-button me-2"></i>Offline Remote Query Simulator (WhatsApp / Mobile)</h5>
                            <small class="text-muted d-block mb-3">
                                Test asking questions to Aradhya, Ramesh, Jayesh, Priya, or Hasmukh <strong>as if this physical laptop were closed and sleeping</strong>.
                            </small>

                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Sender / Channel</label>
                                <div class="input-group input-group-sm">
                                    <span class="input-group-text bg-dark text-warning border-secondary"><i class="fa-brands fa-whatsapp"></i></span>
                                    <input type="text" id="cshSimSender" class="form-control bg-dark text-light border-secondary" value="Alpesh Sir (Remote Mobile: +91 78747 19139)">
                                </div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label text-light small fw-bold">Preset Test Inquiries</label>
                                <div class="d-flex flex-wrap gap-1 mb-2">
                                    <button class="btn btn-xs btn-outline-warning" onclick="setOfflineQueryPreset('Classic 350 clutch plate stock and price check karo')">📦 Jayesh (Stock)</button>
                                    <button class="btn btn-xs btn-outline-warning" onclick="setOfflineQueryPreset('J-Series 350 cylinder head factory tightening torque sequence')">🛠️ Ramesh (Torque)</button>
                                    <button class="btn btn-xs btn-outline-warning" onclick="setOfflineQueryPreset('આજનું કુલ કેશલેસ યુપીઆઈ કલેક્શન કેટલું થયું?')">🧾 Hasmukh (Accounts)</button>
                                    <button class="btn btn-xs btn-outline-warning" onclick="setOfflineQueryPreset('વર્કશોપમાં સર્વિસ બાઇક્સ અને જોબ કાર્ડ સ્ટેટસ શું છે?')">💬 Priya (Job Status)</button>
                                    <button class="btn btn-xs btn-outline-warning" onclick="setOfflineQueryPreset('લેટેસ્ટ યુટ્યુબ શોર્ટ્સ અને રાઇડર્સ ક્લબનું અપડેટ આપો')">📱 Kabir (Social)</button>
                                </div>
                                <textarea id="cshSimQueryInput" class="form-control bg-dark text-light border-warning" rows="3" placeholder="Enter inquiry in Gujarati or English..."></textarea>
                            </div>

                            <button class="btn btn-warning fw-bold w-100" id="btnRunOfflineSim" onclick="submitOfflineSimulationQuery()">
                                <i class="fa-solid fa-paper-plane me-2"></i> Query Cloud Shadow Replica
                            </button>

                            <!-- Response Card -->
                            <div id="cshSimResultBox" class="mt-3 p-3 bg-black rounded border border-success text-light" style="display:none;">
                                <div class="d-flex justify-content-between align-items-center mb-2">
                                    <span class="badge bg-success" id="cshSimAgentBadge">Cloud Replica</span>
                                    <span class="badge bg-dark border border-secondary text-muted" id="cshSimEnvBadge">STANDBY MIRROR</span>
                                </div>
                                <div class="mb-2 small" id="cshSimEn"></div>
                                <div class="p-2 bg-dark rounded border border-warning text-warning small" id="cshSimGu"></div>
                            </div>
                        </div>

                        <!-- 24/7 Cloud Hosting Guide -->
                        <div class="card card-custom p-3 border-info">
                            <h6 class="text-info mb-2"><i class="fa-solid fa-cloud-arrow-up me-2"></i>Zero-Cost Cloud Deployment Ready</h6>
                            <p class="small text-muted mb-2">
                                Standalone microservice package generated in <code>chamunda_re_enterprise/build_cloud_shadow</code>.
                                Ready for free 24/7 deployment on Render, Fly.io, or Google Cloud Run.
                            </p>
                            <div class="d-flex justify-content-between align-items-center">
                                <span class="badge bg-dark border border-info text-info">Dockerfile &amp; Procfile Ready</span>
                                <button class="btn btn-xs btn-outline-info" onclick="alert('Execute ./deploy_cloud_shadow.sh to package standalone cloud container.')">View Deploy Docs</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- ============================================================= -->
            <!-- TAB 25: PROJECT KALPAVRIKSHA (AUTONOMOUS VIRTUAL GROWTH & MASTERY) -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="kalpavriksha" role="tabpanel">
                <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom border-secondary">
                    <div>
                        <h4 class="text-warning mb-1"><i class="fa-solid fa-tree me-2"></i>Project "Kalpavriksha" • Autonomous Virtual Growth &amp; Self-Evolution Engine</h4>
                        <p class="text-muted small mb-0">પ્રોજેક્ટ કલ્પવૃક્ષ — Continuous synthetic mechanical simulations, agent XP advancement, and factory manual deep-indexing. <strong>100% OFFLINE CAPABLE.</strong></p>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-warning btn-sm fw-bold" onclick="triggerKalpavrikshaSimulation()">
                            <i class="fa-solid fa-play me-1"></i> Run 1-Click Synthetic Simulation
                        </button>
                        <button class="btn btn-primary btn-sm fw-bold" onclick="triggerKalpavrikshaSurge()">
                            <i class="fa-solid fa-bolt-lightning me-1"></i> 10x Fast Growth Surge
                        </button>
                        <button class="btn btn-outline-info btn-sm" onclick="loadKalpavrikshaStatus()">
                            <i class="fa-solid fa-rotate me-1"></i> Refresh Telemetry
                        </button>
                    </div>
                </div>

                <!-- KPI Cards -->
                <div class="row g-3 mb-4">
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-warning text-center h-100">
                            <span class="text-muted small text-uppercase">Fleet Overall IQ</span>
                            <h2 class="text-warning my-1" id="kvFleetIQ">184</h2>
                            <small class="text-success"><i class="fa-solid fa-brain me-1"></i>Self-Improving Daily</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-success text-center h-100">
                            <span class="text-muted small text-uppercase">Fleet Total Experience</span>
                            <h2 class="text-success my-1" id="kvTotalXP">93,100 XP</h2>
                            <small class="text-muted">Combined Mastery Pool</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-info text-center h-100">
                            <span class="text-muted small text-uppercase">Simulations Executed</span>
                            <h2 class="text-info my-1" id="kvSimsCount">48</h2>
                            <small class="text-info"><i class="fa-solid fa-check-double me-1"></i>Fault Scenarios Solved</small>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card card-custom p-3 border-primary text-center h-100">
                            <span class="text-muted small text-uppercase">Offline Engine Status</span>
                            <h2 class="text-light my-1"><span class="badge bg-success">100% LOCAL</span></h2>
                            <small class="text-muted">Zero Cloud/Internet Reliance</small>
                        </div>
                    </div>
                </div>

                <!-- Live Simulation Execution Result Banner -->
                <div id="kvSimResultCard" class="card card-custom p-3 mb-4 border-warning" style="display:none; background: #1a2216;">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="text-warning mb-0"><i class="fa-solid fa-bolt me-2"></i><span id="kvResultTitle">Simulation Executed</span></h6>
                        <span class="badge bg-warning text-dark fw-bold" id="kvResultXP">+500 XP Awarded</span>
                    </div>
                    <div class="row g-2 small">
                        <div class="col-md-6">
                            <span class="text-muted">Bike Model:</span> <strong class="text-light" id="kvResultBike">--</strong><br>
                            <span class="text-muted">Reported Symptom:</span> <span class="text-info" id="kvResultSymptom">--</span>
                        </div>
                        <div class="col-md-6">
                            <span class="text-muted">Responding Agent:</span> <strong class="text-warning" id="kvResultAgent">--</strong><br>
                            <span class="text-muted">Diagnosis:</span> <span class="text-light" id="kvResultDiagnosis">--</span>
                        </div>
                        <div class="col-12 mt-2 p-2 bg-dark rounded border border-secondary">
                            <span class="text-warning fw-bold"><i class="fa-solid fa-wrench me-1"></i>Prescribed Resolution:</span> <span class="text-light" id="kvResultPrescription">--</span><br>
                            <span class="text-success fw-bold"><i class="fa-solid fa-language me-1"></i>ગુજરાતી નિવારણ:</span> <span class="text-light" id="kvResultGujarati">--</span>
                        </div>
                    </div>
                </div>

                <!-- Sub-Agents Mastery Grid -->
                <div class="card card-custom p-3 mb-4">
                    <h5 class="text-warning mb-3"><i class="fa-solid fa-users-gear me-2"></i>Autonomous Sub-Agents Mastery Progression</h5>
                    <div class="row g-3" id="kvAgentsGrid">
                        <!-- Populated via JS -->
                    </div>
                </div>

                <!-- Technical Manuals Ingestion & Indexed Specs -->
                <div class="row g-3 mb-4">
                    <div class="col-md-7">
                        <div class="card card-custom p-3 h-100">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="text-info mb-0"><i class="fa-solid fa-book-bookmark me-2"></i>Locally Indexed Technical Specifications</h6>
                                <span class="badge bg-dark border border-info text-info" id="kvSpecsCount">3 Specs</span>
                            </div>
                            <p class="small text-muted mb-2">Factory torque sequences, clearance tolerances, and Master Tech Ramesh's trade secrets stored locally in <code>data/kalpavriksha_knowledge.json</code>.</p>
                            <div class="table-responsive">
                                <table class="table table-dark table-sm table-hover align-middle mb-0">
                                    <thead>
                                        <tr class="text-muted small">
                                            <th>Spec ID</th>
                                            <th>Engine Family</th>
                                            <th>Category</th>
                                            <th>Key Spec / Ramesh Secret</th>
                                        </tr>
                                    </thead>
                                    <tbody id="kvSpecsTableBody">
                                        <!-- Populated via JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-5">
                        <div class="card card-custom p-3 h-100 border-secondary">
                            <h6 class="text-warning mb-2"><i class="fa-solid fa-file-import me-2"></i>Ingest New Technical Spec</h6>
                            <p class="small text-muted mb-2">Deep-index new workshop specifications directly into the agent's offline local memory.</p>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Engine Family</label>
                                <input type="text" id="kvIngestFamily" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Himalayan 450 Sherpa DOHC">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Category</label>
                                <input type="text" id="kvIngestCategory" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Cooling Loop / Valvetrain">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Target Components</label>
                                <input type="text" id="kvIngestComponents" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Water Pump Impeller Nut">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Torque Sequence</label>
                                <input type="text" id="kvIngestTorque" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. 11 Nm with Loctite 243">
                            </div>
                            <div class="mb-2">
                                <label class="form-label small text-muted mb-1">Clearances / Tolerance</label>
                                <input type="text" id="kvIngestClearances" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Rotor runout &lt; 0.05 mm">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small text-muted mb-1">Master Tech Secret / Note</label>
                                <input type="text" id="kvIngestSecret" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Bleed air bubble via radiator cap bleed screw">
                            </div>
                            <button class="btn btn-warning btn-sm w-100 fw-bold" onclick="ingestKalpavrikshaSpec()">
                                <i class="fa-solid fa-plus me-1"></i> Ingest into Local Disk
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Simulation Audit Log -->
                <div class="card card-custom p-3">
                    <h6 class="text-light mb-2"><i class="fa-solid fa-clock-rotate-left me-2"></i>Recent Autonomous Practice Scenarios</h6>
                    <div class="table-responsive">
                        <table class="table table-dark table-sm table-hover align-middle mb-0">
                            <thead>
                                <tr class="text-muted small">
                                    <th>Timestamp</th>
                                    <th>Simulation ID</th>
                                    <th>Bike Model</th>
                                    <th>Responding Agent</th>
                                    <th>XP Gained</th>
                                    <th>Diagnosis &amp; Solution</th>
                                </tr>
                            </thead>
                            <tbody id="kvRecentSimsTableBody">
                                <!-- Populated via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>




            <!-- ============================================================= -->
            <!-- TAB 26: ROYAL ENFIELD DEALER MANAGEMENT SYSTEM (RE-DMS SUITE) -->
            <!-- ============================================================= -->
            <div class="tab-pane fade" id="dms" role="tabpanel">
                <!-- Dealership Banner -->
                <div class="p-4 mb-4 rounded-3 border border-warning" style="background: linear-gradient(135deg, #1c1505 0%, #0d0e12 100%);">
                    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3">
                        <div>
                            <div class="d-flex align-items-center gap-2 mb-1">
                                <span class="badge bg-warning text-dark fw-bold px-2 py-1">OFFICIAL RE DEALER SUITE</span>
                                <span class="badge bg-dark border border-secondary text-muted">GSTIN: 24AAPCC4469R1Z8</span>
                                <span class="badge bg-success text-light"><i class="fa-brands fa-whatsapp me-1"></i>+91 78747 19139</span>
                            </div>
                            <h3 class="fw-bold text-light mb-1">🏢 Chamunda Royal Enfield Dealer Management System (RE-DMS)</h3>
                            <p class="text-muted small mb-0">Unified Dealership Platform: Split GST Invoicing (SAC 998729 vs HSN 8714), OEM FSC Warranty Claims, Double-Entry Daybook Ledger &amp; Predictive WhatsApp CRM.</p>
                        </div>
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-warning" onclick="loadDMSOverview()">
                                <i class="fa-solid fa-rotate me-1"></i>Refresh Portal
                            </button>
                            <button class="btn btn-sm btn-warning text-dark fw-bold" onclick="dispatchDMSServiceReminders()">
                                <i class="fa-brands fa-whatsapp me-1"></i>Dispatch 90-Day Reminders
                            </button>
                        </div>
                    </div>
                </div>

                <!-- KPI Metric Cards (6-Pillar OEM Dashboard) -->
                <div class="row g-3 mb-4">
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-warning h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">Invoices Generated</small>
                            <div class="metric-val text-warning fs-4" id="dmsTotalInvoices">0</div>
                            <small class="text-muted" style="font-size:0.7rem;">Turnover: <strong class="text-light" id="dmsGrossRevenue">₹0</strong></small>
                        </div>
                    </div>
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-info h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">OEM Warranty Claims</small>
                            <div class="metric-val text-info fs-4" id="dmsTotalClaims">0</div>
                            <small class="text-success" style="font-size:0.7rem;"><i class="fa-solid fa-check-double"></i> Approved CNs</small>
                        </div>
                    </div>
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-success h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">Daybook Net Cash</small>
                            <div class="metric-val text-success fs-4" id="dmsNetCash">₹0</div>
                            <small class="text-muted" style="font-size:0.7rem;">AR: <strong class="text-light" id="dmsReceivables">₹0</strong></small>
                        </div>
                    </div>
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-primary h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">Marketing &amp; Leads</small>
                            <div class="metric-val text-primary fs-4" id="dmsActiveCampaigns">0</div>
                            <small class="text-muted" style="font-size:0.7rem;">Leads: <strong class="text-light" id="dmsActiveLeads">0</strong></small>
                        </div>
                    </div>
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-warning h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">Showroom Bookings</small>
                            <div class="metric-val text-warning fs-4" id="dmsTotalBookings">0</div>
                            <small class="text-muted" style="font-size:0.7rem;">Advance: <strong class="text-light" id="dmsTotalAdvance">₹0</strong></small>
                        </div>
                    </div>
                    <div class="col-md-2 col-6">
                        <div class="card card-custom p-3 border-danger h-100">
                            <small class="text-muted text-uppercase fw-bold" style="font-size:0.7rem;">CSAT Quality Index</small>
                            <div class="metric-val text-danger fs-4" id="dmsCSATScore">100%</div>
                            <small class="text-muted" style="font-size:0.7rem;">Avg: <strong class="text-warning" id="dmsAvgRating">5.0 ⭐</strong></small>
                        </div>
                    </div>
                </div>

                <!-- 4 Main Workstation Panes -->
                <div class="row g-4 mb-4">
                    <!-- Pane A: Billing & Gate Pass Desk (Devang Dave) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-warning">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-warning mb-0"><i class="fa-solid fa-file-invoice-dollar me-2"></i>Split-GST Billing &amp; Gate Pass</h5>
                                    <small class="text-muted">Officer: <strong>Devang Dave</strong> | SAC 998729 (Labor) &amp; HSN 8714 (Spares)</small>
                                </div>
                                <span class="badge bg-dark border border-warning text-warning">Devang Dave Desk</span>
                            </div>

                            <div class="row g-2 mb-2">
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Customer Name</label>
                                    <input type="text" id="dmsCustName" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Ramesh Patel">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Mobile (+91)</label>
                                    <input type="text" id="dmsCustPhone" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. +91 98250 12345">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Motorcycle Model</label>
                                    <select id="dmsBikeModel" class="form-select form-select-sm bg-dark text-light border-secondary">
                                        <option value="Classic 350 (Reborn)">Classic 350 (Reborn)</option>
                                        <option value="Hunter 350 Dapper">Hunter 350 Dapper</option>
                                        <option value="Bullet 350 Standard">Bullet 350 Standard</option>
                                        <option value="Meteor 350 Fireball">Meteor 350 Fireball</option>
                                        <option value="Himalayan 450 Sherpa">Himalayan 450 Sherpa</option>
                                        <option value="Interceptor 650 Twin">Interceptor 650 Twin</option>
                                        <option value="Continental GT 650">Continental GT 650</option>
                                        <option value="Super Meteor 650">Super Meteor 650</option>
                                        <option value="Shotgun 650">Shotgun 650</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Registration No</label>
                                    <input type="text" id="dmsRegNo" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. GJ-02-CD-5678">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small text-muted mb-1">Spares (HSN 8714)</label>
                                    <input type="number" id="dmsPartsSubtotal" class="form-control form-control-sm bg-dark text-light border-secondary" value="1935">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small text-muted mb-1">Labor (SAC 998729)</label>
                                    <input type="number" id="dmsLaborSubtotal" class="form-control form-control-sm bg-dark text-light border-secondary" value="900">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label small text-muted mb-1">Payment Mode</label>
                                    <select id="dmsPaymentMode" class="form-select form-select-sm bg-dark text-light border-secondary">
                                        <option value="UPI (Instant)">UPI (Instant)</option>
                                        <option value="Cash Counter">Cash Counter</option>
                                        <option value="HDFC POS Card">HDFC POS Card</option>
                                        <option value="B2B Ledger Credit">B2B Ledger Credit</option>
                                    </select>
                                </div>
                            </div>

                            <button class="btn btn-warning text-dark w-100 fw-bold mb-3" onclick="createDMSInvoice()">
                                <i class="fa-solid fa-receipt me-2"></i>Generate Split GST Invoice &amp; Gate Pass
                            </button>

                            <div id="dmsInvoiceResultBox" class="p-3 bg-black rounded border border-warning text-light" style="display: none;">
                                <!-- Live Invoice Output -->
                            </div>
                        </div>
                    </div>

                    <!-- Pane B: OEM Warranty & Claims Desk (Devang Dave) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-info">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-info mb-0"><i class="fa-solid fa-shield-halved me-2"></i>OEM Warranty &amp; FSC Claims</h5>
                                    <small class="text-muted">Direct Royal Enfield India Warranty &amp; Coupon Settlement Portal</small>
                                </div>
                                <span class="badge bg-dark border border-info text-info">OEM Claims Desk</span>
                            </div>

                            <div class="row g-2 mb-2">
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Coupon / Claim Type</label>
                                    <select id="dmsCouponType" class="form-select form-select-sm bg-dark text-light border-secondary">
                                        <option value="1st Free Service Coupon (500 km)">1st Free Service Coupon (500 km)</option>
                                        <option value="2nd Free Service Coupon (5000 km)">2nd Free Service Coupon (5000 km)</option>
                                        <option value="3rd Free Service Coupon (10000 km)">3rd Free Service Coupon (10000 km)</option>
                                        <option value="4th Free Service Coupon (15000 km)">4th Free Service Coupon (15000 km)</option>
                                        <option value="Electrical Sensor / ECU Defect Claim">Electrical Sensor / ECU Defect Claim</option>
                                        <option value="Engine Tappet / Valvetrain Warranty">Engine Tappet / Valvetrain Warranty</option>
                                        <option value="Fuel Pump / Injector Replacement">Fuel Pump / Injector Replacement</option>
                                    </select>
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Chassis / VIN Number</label>
                                    <input type="text" id="dmsChassisNo" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. ME3J350NR99842">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Engine Number</label>
                                    <input type="text" id="dmsEngineNo" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. J350-2024-8812">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Claim Value (INR)</label>
                                    <input type="number" id="dmsClaimAmount" class="form-control form-control-sm bg-dark text-light border-secondary" value="1450">
                                </div>
                                <div class="col-12">
                                    <label class="form-label small text-muted mb-1">Defective Component Description</label>
                                    <input type="text" id="dmsDefectDesc" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. OEM Engine Oil, Oil Filter Element &amp; 50-Point Periodic Free Service Coupon">
                                </div>
                            </div>

                            <button class="btn btn-info text-dark w-100 fw-bold mb-3" onclick="fileDMSWarrantyClaim()">
                                <i class="fa-solid fa-cloud-arrow-up me-2"></i>File OEM Warranty Claim to Royal Enfield India
                            </button>

                            <div id="dmsClaimResultBox" class="p-3 bg-black rounded border border-info text-light" style="display: none;">
                                <!-- Live Claim Output -->
                            </div>
                        </div>
                    </div>

                    <!-- Pane C: Dealership Daybook & Financial Ledger (Hasmukhbhai Joshi) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-success">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-success mb-0"><i class="fa-solid fa-book-journal-whills me-2"></i>Dealership Daybook &amp; GSTR-1</h5>
                                    <small class="text-muted">Controller: <strong>Hasmukhbhai Joshi</strong> | Double-entry Cash/Bank Audit</small>
                                </div>
                                <span class="badge bg-dark border border-success text-success">Hasmukhbhai Desk</span>
                            </div>

                            <div class="row g-2 mb-3">
                                <div class="col-6">
                                    <div class="p-2 bg-dark rounded border border-secondary">
                                        <small class="text-muted d-block">B2B Partner Receivables</small>
                                        <strong class="text-warning" id="dmsARSum">₹44,750.00</strong>
                                        <small class="text-muted d-block">Siddhpur, Patan, Unjha</small>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="p-2 bg-dark rounded border border-secondary">
                                        <small class="text-muted d-block">RE Distributorship Payables</small>
                                        <strong class="text-danger" id="dmsAPSum">₹130,700.00</strong>
                                        <small class="text-muted d-block">Ahmedabad Spares Hub</small>
                                    </div>
                                </div>
                            </div>

                            <h6 class="text-light small fw-bold mb-2">Recent Daybook Inflows &amp; Outflows</h6>
                            <div class="table-responsive">
                                <table class="table table-dark table-sm table-hover align-middle mb-0">
                                    <thead>
                                        <tr class="text-muted small">
                                            <th>Timestamp</th>
                                            <th>Type</th>
                                            <th>Particulars / Ledger</th>
                                            <th>Amount</th>
                                        </tr>
                                    </thead>
                                    <tbody id="dmsDaybookTableBody">
                                        <!-- Populated via JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Pane D: Marketing Campaigns & Predictive Reminders (Neha Trivedi) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-primary">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-primary mb-0"><i class="fa-solid fa-bullhorn me-2"></i>Marketing &amp; Retention CRM</h5>
                                    <small class="text-muted">Lead: <strong>Neha Trivedi</strong> | WhatsApp Broadcasts &amp; Test Rides</small>
                                </div>
                                <span class="badge bg-dark border border-primary text-primary">Neha Trivedi Desk</span>
                            </div>

                            <div class="row g-2 mb-2">
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Campaign Name</label>
                                    <input type="text" id="dmsCampName" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Royal Enfield Summer Ride Utsav">
                                </div>
                                <div class="col-md-6">
                                    <label class="form-label small text-muted mb-1">Target Audience</label>
                                    <input type="text" id="dmsCampAudience" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Classic &amp; Hunter Owners (North Gujarat)">
                                </div>
                                <div class="col-12">
                                    <label class="form-label small text-muted mb-1">Offer Title &amp; Details</label>
                                    <input type="text" id="dmsCampOffer" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Complimentary Brake Bleed &amp; 15% Off Synthetic Engine Oil">
                                </div>
                            </div>

                            <div class="d-flex gap-2 mb-3">
                                <button class="btn btn-primary btn-sm flex-grow-1 fw-bold" onclick="createDMSCampaign()">
                                    <i class="fa-solid fa-paper-plane me-1"></i>Launch WhatsApp Broadcast
                                </button>
                                <button class="btn btn-outline-success btn-sm fw-bold" onclick="dispatchDMSServiceReminders()">
                                    <i class="fa-brands fa-whatsapp me-1"></i>Send 30/60/90D Reminders
                                </button>
                            </div>

                            <h6 class="text-light small fw-bold mb-2">Live Test Ride &amp; New Bike Lead Pipeline</h6>
                            <div class="table-responsive">
                                <table class="table table-dark table-sm table-hover align-middle mb-0">
                                    <thead>
                                        <tr class="text-muted small">
                                            <th>Customer</th>
                                            <th>Bike Interest</th>
                                            <th>Source</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody id="dmsLeadsTableBody">
                                        <!-- Populated via JS -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>

                    <!-- Pane E: Showroom Sales, Vehicle Bookings & 30-Point PDI Desk (Vikram Singh) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-warning">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-warning mb-0"><i class="fa-solid fa-motorcycle me-2"></i>Showroom Sales, Booking &amp; PDI Desk</h5>
                                    <small class="text-muted">Lead: <strong>Vikram Singh</strong> | Advance Booking Tokens, Digital PDI &amp; Delivery Passports</small>
                                </div>
                                <span class="badge bg-dark border border-warning text-warning">Vikram Singh Desk</span>
                            </div>

                            <ul class="nav nav-pills nav-fill mb-3" id="pills-sales-tab" role="tablist">
                                <li class="nav-item">
                                    <button class="nav-link active py-1 small" id="pills-booking-tab" data-bs-toggle="pill" data-bs-target="#pills-booking" type="button">1. Bike Booking Token</button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 small" id="pills-pdi-tab" data-bs-toggle="pill" data-bs-target="#pills-pdi" type="button">2. 30-Pt Digital PDI</button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 small" id="pills-ridesure-tab" data-bs-toggle="pill" data-bs-target="#pills-ridesure" type="button">3. Ride Sure &amp; RSA</button>
                                </li>
                            </ul>

                            <div class="tab-content">
                                <!-- Subtab 1: Booking Token -->
                                <div class="tab-pane fade show active" id="pills-booking">
                                    <div class="row g-2 mb-2">
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Customer Name</label>
                                            <input type="text" id="dmsBkCustName" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Chirag Patel">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Mobile (+91)</label>
                                            <input type="text" id="dmsBkCustPhone" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. +91 98250 44556">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Royal Enfield Model</label>
                                            <select id="dmsBkModel" class="form-select form-select-sm bg-dark text-light border-secondary">
                                                <option value="Classic 350 (Reborn)">Classic 350 (Reborn)</option>
                                                <option value="Hunter 350 Dapper">Hunter 350 Dapper</option>
                                                <option value="Himalayan 450 Sherpa">Himalayan 450 Sherpa</option>
                                                <option value="Continental GT 650 Twin">Continental GT 650 Twin</option>
                                                <option value="Interceptor 650 Twin">Interceptor 650 Twin</option>
                                                <option value="Bullet 350 Standard">Bullet 350 Standard</option>
                                                <option value="Meteor 350 Supernova">Meteor 350 Supernova</option>
                                                <option value="Super Meteor 650 Celestial">Super Meteor 650 Celestial</option>
                                                <option value="Shotgun 650 Custom">Shotgun 650 Custom</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Color / Edition</label>
                                            <input type="text" id="dmsBkColor" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Halcyon Black / Kamet White">
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Booking Token (₹)</label>
                                            <input type="number" id="dmsBkAmount" class="form-control form-control-sm bg-dark text-light border-secondary" value="10000">
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Finance Partner</label>
                                            <select id="dmsBkFinance" class="form-select form-select-sm bg-dark text-light border-secondary">
                                                <option value="HDFC Two Wheeler Finance">HDFC Bank (8.9% ROI)</option>
                                                <option value="Bajaj Auto Finance">Bajaj Auto Finance</option>
                                                <option value="Cholamandalam Investment">Cholamandalam Finance</option>
                                                <option value="Full Cash / Direct Bank Transfer">Full Cash (No Hypothecation)</option>
                                            </select>
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Tentative Delivery</label>
                                            <input type="date" id="dmsBkDeliveryDate" class="form-control form-control-sm bg-dark text-light border-secondary">
                                        </div>
                                    </div>
                                    <button class="btn btn-warning text-dark w-100 fw-bold btn-sm mb-2" onclick="createDMSBooking()">
                                        <i class="fa-solid fa-receipt me-1"></i>Confirm Booking &amp; Issue Token Receipt
                                    </button>
                                    <div id="dmsBookingResultBox" class="p-2 bg-black rounded border border-warning text-light small" style="display: none;"></div>
                                </div>

                                <!-- Subtab 2: Digital PDI Certificate -->
                                <div class="tab-pane fade" id="pills-pdi">
                                    <div class="row g-2 mb-2">
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Chassis / VIN (17 Digits)</label>
                                            <input type="text" id="dmsPDIChassis" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="ME3J350NR7892104">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Engine Number</label>
                                            <input type="text" id="dmsPDIEngine" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="J350-2026-9921">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Motorcycle Model</label>
                                            <input type="text" id="dmsPDIModel" class="form-control form-control-sm bg-dark text-light border-secondary" value="Classic 350 (Reborn)">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Customer Name</label>
                                            <input type="text" id="dmsPDICustomer" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="Alpesh Sir">
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Battery Voltage (V)</label>
                                            <input type="number" step="0.1" id="dmsPDIBattery" class="form-control form-control-sm bg-dark text-light border-secondary" value="12.8">
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Idle RPM</label>
                                            <input type="number" id="dmsPDIRPM" class="form-control form-control-sm bg-dark text-light border-secondary" value="1050">
                                        </div>
                                        <div class="col-md-4">
                                            <label class="form-label small text-muted mb-1">Tyre Pressure</label>
                                            <input type="text" id="dmsPDIPressure" class="form-control form-control-sm bg-dark text-light border-secondary" value="Front: 32 / Rear: 36 PSI">
                                        </div>
                                    </div>
                                    <div class="form-check form-switch mb-2">
                                        <input class="form-check-input" type="checkbox" id="dmsPDIToolkit" checked>
                                        <label class="form-check-label small text-light" for="dmsPDIToolkit">Tool Kit, First Aid Kit &amp; Owner's Passport Verified</label>
                                    </div>
                                    <button class="btn btn-outline-warning w-100 fw-bold btn-sm mb-2" onclick="generateDMSPDI()">
                                        <i class="fa-solid fa-clipboard-check me-1"></i>Generate 30-Pt Delivery Passport &amp; PDI Certificate
                                    </button>
                                    <div id="dmsPDIResultBox" class="p-2 bg-black rounded border border-warning text-light small" style="display: none;"></div>
                                </div>

                                <!-- Subtab 3: Ride Sure Extended Warranty & RSA -->
                                <div class="tab-pane fade" id="pills-ridesure">
                                    <div class="row g-2 mb-2">
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Customer Name</label>
                                            <input type="text" id="dmsRSCustName" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Ramesh Patel">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Mobile (+91)</label>
                                            <input type="text" id="dmsRSCustPhone" class="form-control form-control-sm bg-dark text-light border-secondary" value="+91 78747 19139">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Registration / VIN</label>
                                            <input type="text" id="dmsRSReg" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="GJ-02-RE-2026">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Warranty Coverage Plan</label>
                                            <select id="dmsRSPlan" class="form-select form-select-sm bg-dark text-light border-secondary">
                                                <option value="4">4 Years (2+2) + 24/7 Roadside Assistance (₹3,850)</option>
                                                <option value="5">5 Years (2+3) + 24/7 Roadside Assistance (₹4,950)</option>
                                                <option value="3">3 Years (2+1) Roadside Assistance Core (₹2,650)</option>
                                            </select>
                                        </div>
                                    </div>
                                    <button class="btn btn-warning text-dark w-100 fw-bold btn-sm mb-2" onclick="issueDMSRideSure()">
                                        <i class="fa-solid fa-shield me-1"></i>Issue Royal Enfield Ride Sure Policy
                                    </button>
                                    <div id="dmsRideSureResultBox" class="p-2 bg-black rounded border border-warning text-light small" style="display: none;"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Pane F: Accidental Insurance Surveyor & 3-Day PSF CSAT Desk (Devang Dave & Ananya Joshi) -->
                    <div class="col-lg-6">
                        <div class="card card-custom p-3 h-100 border-info">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div>
                                    <h5 class="text-info mb-0"><i class="fa-solid fa-scale-balanced me-2"></i>Insurance Surveyor &amp; PSF CSAT Desk</h5>
                                    <small class="text-muted">Officers: <strong>Devang Dave</strong> (Insurance Claims) &amp; <strong>Ananya Joshi</strong> (CSAT &amp; PSF)</small>
                                </div>
                                <span class="badge bg-dark border border-info text-info">Ananya &amp; Devang Desk</span>
                            </div>

                            <ul class="nav nav-pills nav-fill mb-3" id="pills-audit-tab" role="tablist">
                                <li class="nav-item">
                                    <button class="nav-link active py-1 small" id="pills-psf-tab" data-bs-toggle="pill" data-bs-target="#pills-psf" type="button">1. 3-Day PSF &amp; CSAT Audit</button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 small" id="pills-insurance-tab" data-bs-toggle="pill" data-bs-target="#pills-insurance" type="button">2. Cashless Insurance Claim</button>
                                </li>
                            </ul>

                            <div class="tab-content">
                                <!-- Subtab 1: Post-Service Feedback & CSAT Audit (Ananya Joshi) -->
                                <div class="tab-pane fade show active" id="pills-psf">
                                    <div class="row g-2 mb-2">
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Tax Invoice / Job Card No</label>
                                            <input type="text" id="dmsPSFInvNo" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. INV-RE-2026-001">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Customer Mobile</label>
                                            <input type="text" id="dmsPSFPhone" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="+91 98250 12345">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Customer Name</label>
                                            <input type="text" id="dmsPSFCustName" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="Alpesh Sir">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Star Rating (1 to 5)</label>
                                            <select id="dmsPSFRating" class="form-select form-select-sm bg-dark text-warning border-secondary fw-bold">
                                                <option value="5">⭐⭐⭐⭐⭐ 5 Stars (Delighted - Benchmark)</option>
                                                <option value="4">⭐⭐⭐⭐ 4 Stars (Satisfied)</option>
                                                <option value="3">⭐⭐⭐ 3 Stars (Neutral / Tappet Noise Query)</option>
                                                <option value="2">⭐⭐ 2 Stars (Dissatisfied - Bay Recall Required)</option>
                                                <option value="1">⭐ 1 Star (Critical Complaint - Escalated to Aradhya CEO)</option>
                                            </select>
                                        </div>
                                        <div class="col-12">
                                            <label class="form-label small text-muted mb-1">Customer Voice &amp; PSF Notes</label>
                                            <input type="text" id="dmsPSFNotes" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. Engine feels remarkably smooth, brake feel restored to perfection.">
                                        </div>
                                    </div>
                                    <div class="form-check form-switch mb-2">
                                        <input class="form-check-input" type="checkbox" id="dmsPSFResolved" checked>
                                        <label class="form-check-label small text-light" for="dmsPSFResolved">First Time Right (FTR) - All reported complaints verified 100% resolved</label>
                                    </div>
                                    <button class="btn btn-info text-dark w-100 fw-bold btn-sm mb-2" onclick="recordDMSPSFFeedback()">
                                        <i class="fa-solid fa-star me-1"></i>Record 3-Day PSF &amp; Audit CSAT Score
                                    </button>
                                    <div id="dmsPSFResultBox" class="p-2 bg-black rounded border border-info text-light small" style="display: none;"></div>
                                </div>

                                <!-- Subtab 2: Accidental Insurance Claim Estimate (Devang Dave) -->
                                <div class="tab-pane fade" id="pills-insurance">
                                    <div class="row g-2 mb-2">
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Insurance Company</label>
                                            <select id="dmsInsCo" class="form-select form-select-sm bg-dark text-light border-secondary">
                                                <option value="ICICI Lombard General Insurance">ICICI Lombard General Insurance</option>
                                                <option value="Go Digit General Insurance">Go Digit General Insurance</option>
                                                <option value="HDFC ERGO General Insurance">HDFC ERGO General Insurance</option>
                                                <option value="The Oriental Insurance Co. Ltd">The Oriental Insurance Co. Ltd</option>
                                                <option value="The New India Assurance Co. Ltd">The New India Assurance Co. Ltd</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Deputed Surveyor Name</label>
                                            <input type="text" id="dmsInsSurveyor" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="e.g. M. K. Trivedi (IRDAI Surveyor)">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Damaged Spares Estimate (₹)</label>
                                            <input type="number" id="dmsInsParts" class="form-control form-control-sm bg-dark text-light border-secondary" value="14200">
                                        </div>
                                        <div class="col-md-6">
                                            <label class="form-label small text-muted mb-1">Labor &amp; Paint Estimate (₹)</label>
                                            <input type="number" id="dmsInsLabor" class="form-control form-control-sm bg-dark text-light border-secondary" value="4800">
                                        </div>
                                    </div>
                                    <button class="btn btn-outline-info w-100 fw-bold btn-sm mb-2" onclick="createDMSInsuranceEstimate()">
                                        <i class="fa-solid fa-calculator me-1"></i>Compute Cashless Surveyor Estimate &amp; DO Split
                                    </button>
                                    <div id="dmsInsuranceResultBox" class="p-2 bg-black rounded border border-info text-light small" style="display: none;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 10-Officer Dealership Fleet Roster -->
                <div class="card card-custom p-3 border-secondary">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div>
                            <h6 class="text-light mb-0"><i class="fa-solid fa-users-gear me-2 text-warning"></i>Royal Enfield Dealership Autonomous Officers Fleet (10 Active Officers)</h6>
                            <small class="text-muted">100% Offline Multi-Agent Cluster • Supervised by Alpesh Sir &amp; Aradhya CEO</small>
                        </div>
                        <span class="badge bg-warning text-dark fw-bold">10 Autonomous Officers</span>
                    </div>
                    <div class="row g-2" id="dmsFleetRosterRow">
                        <!-- Populated via JS -->
                    </div>
                </div>
            </div>

    <!-- Modal for B2B Wholesale Quick Order -->
    <div class="modal fade" id="b2bOrderModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-info">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-info"><i class="fa-solid fa-boxes-packing me-2"></i>Dispatch B2B Wholesale Spares Order</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <input type="hidden" id="b2bModalGarageId">
                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <label class="form-label text-muted small">Partner Garage</label>
                            <input type="text" id="b2bModalGarageName" class="form-control bg-dark text-info border-secondary" readonly>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-muted small">Wholesale Tier &amp; Margin</label>
                            <input type="text" id="b2bModalTier" class="form-control bg-dark text-light border-secondary" readonly>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light fw-bold small">Select Genuine Royal Enfield OEM Spares Package</label>
                        <select id="b2bSparesPackageSelect" class="form-select bg-dark text-light border-secondary">
                            <option value="routine_service_pack">Periodic Service Pack: 20x Oil Filter (574050/C), 10x Air Filter (147008/A)</option>
                            <option value="braking_pack">Braking Overhaul Pack: 10x Front Brake Pads (592188/B), 5x Rear Brake Pads</option>
                            <option value="clutch_ignition_pack">Clutch &amp; Ignition: 5x Clutch Plate Sets (586119/D), 10x NGK Spark Plugs</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light fw-bold small">Payment Terms</label>
                        <select id="b2bPaymentModeSelect" class="form-select bg-dark text-light border-secondary">
                            <option value="Credit (Based on Tier)">Credit (Tier-based 7 / 15 / 30 Days)</option>
                            <option value="UPI / Instant (2% Cash Discount)">UPI / Instant (2% Additional Cash Discount)</option>
                            <option value="Cash on Delivery">Cash on Delivery (COD)</option>
                        </select>
                    </div>
                    <div id="b2bOrderAlert" class="alert alert-info small py-2" style="display:none;"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-info fw-bold" onclick="submitB2BOrder()"><i class="fa-solid fa-paper-plane me-1"></i> Dispatch Order</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Partner Garage Registration -->
    <div class="modal fade" id="registerGarageModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content bg-dark text-light border-info">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-info"><i class="fa-solid fa-building me-2"></i>Register North Gujarat Partner Garage</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Garage Name</label>
                        <input type="text" id="regGName" class="form-control bg-dark text-light border-secondary" placeholder="e.g. Somnath RE Workshop">
                    </div>
                    <div class="row g-2 mb-3">
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">Owner Name</label>
                            <input type="text" id="regGOwner" class="form-control bg-dark text-light border-secondary" placeholder="e.g. Jagdishbhai Patel">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">Phone Number</label>
                            <input type="text" id="regGPhone" class="form-control bg-dark text-light border-secondary" placeholder="+91 98250 XXXXX">
                        </div>
                    </div>
                    <div class="row g-2 mb-3">
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">City / Town</label>
                            <select id="regGCity" class="form-select bg-dark text-light border-secondary">
                                <option value="Patan">Patan</option>
                                <option value="Unjha">Unjha</option>
                                <option value="Visnagar">Visnagar</option>
                                <option value="Kadi">Kadi</option>
                                <option value="Siddhpur">Siddhpur</option>
                                <option value="Vadnagar">Vadnagar</option>
                                <option value="Kheralu">Kheralu</option>
                                <option value="Chanasma">Chanasma</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">Partner Tier</label>
                            <select id="regGTier" class="form-select bg-dark text-light border-secondary">
                                <option value="Bronze">Bronze (12% off)</option>
                                <option value="Silver">Silver (16% off)</option>
                                <option value="Gold" selected>Gold (20% off)</option>
                                <option value="Platinum">Platinum Hub (25% off)</option>
                            </select>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Full Address</label>
                        <input type="text" id="regGAddress" class="form-control bg-dark text-light border-secondary" placeholder="Highway Road, Opp Bus Station...">
                    </div>
                    <div id="regGAlert" class="alert alert-info small py-2" style="display:none;"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-info fw-bold" onclick="submitRegisterGarage()">Save Partner Garage</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Club AMC Enrollment -->
    <div class="modal fade" id="clubEnrollModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content bg-dark text-light border-danger">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-danger"><i class="fa-solid fa-shield-halved me-2"></i>Enroll Rider into AMC Pass</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Select AMC Tier</label>
                        <select id="enrollPlanId" class="form-select bg-dark text-light border-secondary">
                            <option value="AMC-SILVER">Silver Thump Pass (₹3,999/yr)</option>
                            <option value="AMC-GOLD" selected>Gold Tourer Pass (₹7,499/yr)</option>
                            <option value="AMC-PLATINUM">Platinum Vintage &amp; Twin (₹11,999/yr)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Rider Full Name</label>
                        <input type="text" id="enrollName" class="form-control bg-dark text-light border-secondary" placeholder="e.g. Alpesh Sir">
                    </div>
                    <div class="row g-2 mb-3">
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">Phone Number</label>
                            <input type="text" id="enrollPhone" class="form-control bg-dark text-light border-secondary" placeholder="+91 78747 19139">
                        </div>
                        <div class="col-md-6">
                            <label class="form-label text-light small fw-bold">Registration No</label>
                            <input type="text" id="enrollReg" class="form-control bg-dark text-light border-secondary" placeholder="GJ-02-BQ-1234">
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label text-light small fw-bold">Bike Model Platform</label>
                        <input type="text" id="enrollBike" class="form-control bg-dark text-light border-secondary" placeholder="e.g. Classic 350 Reborn / Interceptor 650">
                    </div>
                    <div id="enrollAlert" class="alert alert-info small py-2" style="display:none;"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger fw-bold" onclick="submitClubEnroll()">Activate AMC Pass</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Complete & Bill Result -->
    <div class="modal fade" id="billModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-solid fa-certificate me-2"></i>Job Card Completed & QR Invoice Issued</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="billModalContent"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for WhatsApp Reminder Dispatch -->
    <div class="modal fade" id="whatsappModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-brands fa-whatsapp text-success me-2"></i>Automated WhatsApp Service Reminder</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label text-warning small fw-bold">Customer &amp; Vehicle Details</label>
                            <div class="p-3 bg-black rounded border border-secondary mb-3">
                                <h6 class="text-warning mb-1" id="waCustName"></h6>
                                <p class="mb-1 text-light"><i class="fa-solid fa-motorcycle me-1 text-warning"></i> <span id="waBikeModel"></span> (<code id="waRegNo" class="text-warning"></code>)</p>
                                <p class="mb-1 text-light"><i class="fa-solid fa-phone me-1 text-success"></i> <span id="waPhone"></span></p>
                                <small class="text-muted d-block mt-2">Days Elapsed: <strong id="waDays" class="text-danger"></strong> | Est Odo: <strong id="waOdo" class="text-warning"></strong> KM | Health: <strong id="waHealth" class="text-success"></strong>/100</small>
                            </div>
                            <div class="d-flex gap-2">
                                <button type="button" class="btn btn-success flex-fill" onclick="dispatchToWhatsAppWeb()">
                                    <i class="fa-brands fa-whatsapp me-1"></i> Open WhatsApp Web
                                </button>
                                <button type="button" class="btn btn-outline-info" onclick="markCurrentReminderSent()">
                                    <i class="fa-solid fa-check-double me-1"></i> Mark as Sent
                                </button>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <ul class="nav nav-pills mb-2" id="waLangTabs" role="tablist">
                                <li class="nav-item">
                                    <button class="nav-link active py-1 px-3 btn-sm" id="waGuTab" data-bs-toggle="pill" data-bs-target="#waGuContent" type="button">Gujarati (ગુજરાતી)</button>
                                </li>
                                <li class="nav-item">
                                    <button class="nav-link py-1 px-3 btn-sm" id="waEnTab" data-bs-toggle="pill" data-bs-target="#waEnContent" type="button">English</button>
                                </li>
                            </ul>
                            <div class="tab-content">
                                <div class="tab-pane fade show active" id="waGuContent">
                                    <textarea id="waTextGu" class="form-control bg-dark text-light border-secondary" rows="10" readonly></textarea>
                                </div>
                                <div class="tab-pane fade" id="waEnContent">
                                    <textarea id="waTextEn" class="form-control bg-dark text-light border-secondary" rows="10" readonly></textarea>
                                </div>
                            </div>
                            <button type="button" class="btn btn-outline-warning btn-sm mt-2 w-100" onclick="copyCurrentWhatsAppText()">
                                <i class="fa-regular fa-copy me-1"></i> Copy Current Message to Clipboard
                            </button>
                        </div>
                    </div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Wholesale PO Generation Result -->
    <div class="modal fade" id="poModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-solid fa-boxes-packing me-2"></i>Wholesale Purchase Order Generated</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="poModalBody">
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Quick Countertop POS & Dynamic UPI QR -->
    <div class="modal fade" id="posModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <div>
                        <h5 class="modal-title text-warning mb-0">
                            <i class="fa-solid fa-cash-register me-2"></i>Quick Countertop POS • Barcode Scanner &amp; Dynamic UPI QR
                        </h5>
                        <small class="text-muted">ઝડપી કાઉન્ટર પાર્ટ્સ વેચાણ • ઇન્વેન્ટરી સ્ટોક ઓટો-ડિડક્શન • PhonePe/GPay ડાયનેમિક UPI QR</small>
                    </div>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div class="row g-3">
                        <!-- Left: Barcode Scanner & Cart -->
                        <div class="col-lg-7">
                            <div class="card bg-black border-secondary p-3 mb-3">
                                <label class="form-label text-warning small fw-bold">
                                    <i class="fa-solid fa-barcode me-1"></i> Scan Barcode / Enter Part No or SKU:
                                </label>
                                <div class="input-group mb-2">
                                    <input type="text" id="posScanInput" class="form-control bg-dark text-light border-secondary" placeholder="Scan barcode or type e.g. 574050/C, RAM00008/B..." onkeydown="if(event.key==='Enter') posScanAndAdd()">
                                    <button class="btn btn-gold fw-bold px-3" onclick="posScanAndAdd()">
                                        <i class="fa-solid fa-plus me-1"></i> Add Part
                                    </button>
                                </div>
                                <div class="d-flex gap-1 flex-wrap">
                                    <button class="btn btn-outline-secondary btn-sm py-0" style="font-size: 11px;" onclick="posQuickAdd('574050/C')">+ Oil Filter Element (574050/C)</button>
                                    <button class="btn btn-outline-secondary btn-sm py-0" style="font-size: 11px;" onclick="posQuickAdd('RAM00008/B')">+ Air Filter J-Series (RAM00008/B)</button>
                                    <button class="btn btn-outline-secondary btn-sm py-0" style="font-size: 11px;" onclick="posQuickAdd('KXA00215')">+ Sherpa 450 Filter (KXA00215)</button>
                                    <button class="btn btn-outline-secondary btn-sm py-0" style="font-size: 11px;" onclick="posQuickAdd('1017011/A')">+ 650 Twin Air Filter (1017011/A)</button>
                                </div>
                            </div>

                            <div class="table-responsive" style="max-height: 280px;">
                                <table class="table table-custom table-sm">
                                    <thead>
                                        <tr>
                                            <th>Part Description</th>
                                            <th>OEM / SKU</th>
                                            <th style="width: 70px;">Qty</th>
                                            <th>Rate</th>
                                            <th>Total</th>
                                            <th>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody id="posCartBody">
                                        <tr>
                                            <td colspan="6" class="text-center py-4 text-muted">Cart is empty. Scan barcode or click quick parts above.</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Right: Checkout & Dynamic UPI QR -->
                        <div class="col-lg-5">
                            <div class="card bg-black border-warning p-3 h-100">
                                <h6 class="text-warning mb-3"><i class="fa-solid fa-receipt me-1"></i> Counter Checkout Summary</h6>
                                
                                <div class="mb-2">
                                    <label class="form-label text-muted small">Customer Name:</label>
                                    <input type="text" id="posCustName" class="form-control form-control-sm bg-dark text-light border-secondary" value="Walk-in Counter Customer">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label text-muted small">Phone Number:</label>
                                    <input type="text" id="posCustPhone" class="form-control form-control-sm bg-dark text-light border-secondary" placeholder="+91 98250 XXXXX">
                                </div>

                                <div class="p-2 bg-dark rounded border border-secondary mb-3">
                                    <div class="d-flex justify-content-between small text-muted">
                                        <span>Items Subtotal:</span>
                                        <strong id="posSubtotal" class="text-light">₹0.00</strong>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-center small text-muted mt-1">
                                        <span>Discount (₹):</span>
                                        <input type="number" id="posDiscount" class="form-control form-control-sm bg-black text-light border-secondary text-end py-0" style="width: 80px;" value="0" onchange="posRecalcTotals()">
                                    </div>
                                    <hr class="border-secondary my-2">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span class="fw-bold text-warning">NET PAYABLE:</span>
                                        <strong id="posNetTotal" style="font-size: 24px; color: var(--gold);">₹0.00</strong>
                                    </div>
                                    <small class="text-muted d-block text-end" style="font-size: 10px;">(Includes 18% GST)</small>
                                </div>

                                <button class="btn btn-gold w-100 py-2 fw-bold mb-3" onclick="posExecuteCheckout()">
                                    <i class="fa-solid fa-qrcode me-1"></i> Instant Checkout &amp; Generate UPI QR
                                </button>

                                <!-- Instant UPI QR Container -->
                                <div id="posCheckoutResultBox" class="p-3 bg-dark rounded border border-warning text-center" style="display: none;">
                                    <span class="badge bg-success mb-2"><i class="fa-solid fa-check me-1"></i> Stock Deducted &amp; QR Generated</span>
                                    <div class="small text-warning fw-bold" id="posReceiptNo">POS-0000</div>
                                    <div class="my-2">
                                        <img id="posQrImage" src="" style="width: 140px; height: 140px; border-radius: 6px; border: 2px solid var(--gold);" alt="Dynamic UPI QR">
                                    </div>
                                    <div class="small text-light" style="font-size: 11px;">UPI ID: <code>chamunda.re@okicici</code></div>
                                    <div class="small text-muted" style="font-size: 10px;">GPay • PhonePe • Paytm • BHIM</div>
                                    <div class="d-flex gap-2 mt-3">
                                        <button class="btn btn-outline-warning btn-sm flex-fill" id="posPrintSlipBtn" onclick="posPrintCurrentReceipt()">
                                            <i class="fa-solid fa-print me-1"></i> Print 80mm Slip
                                        </button>
                                        <button class="btn btn-outline-success btn-sm flex-fill" onclick="posCopyWhatsAppReceipt()">
                                            <i class="fa-brands fa-whatsapp me-1"></i> WhatsApp
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Pre-Owned Certificate Result -->
    <div class="modal fade" id="preownedModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-solid fa-shield-halved me-2"></i>Chamunda Pre-Owned Inspection &amp; Shield Certificate</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="preownedModalContent"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-gold" onclick="printPreownedCert()"><i class="fa-solid fa-print me-1"></i> Print / Open Certificate</button>
                    <button type="button" class="btn btn-outline-success" onclick="copyPreownedWhatsApp()"><i class="fa-brands fa-whatsapp me-1"></i> Copy WhatsApp Report</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Expedition Clearance Passport Result -->
    <div class="modal fade" id="expeditionModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-solid fa-compass me-2"></i>Chamunda Expedition Clearance Passport</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="expeditionModalContent"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-gold" onclick="printExpeditionPassport()"><i class="fa-solid fa-print me-1"></i> Print / Open Passport</button>
                    <button type="button" class="btn btn-outline-success" onclick="copyExpeditionWhatsApp()"><i class="fa-brands fa-whatsapp me-1"></i> Copy WhatsApp Broadcast</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal for Custom Resto-Mod Blueprint Result -->
    <div class="modal fade" id="restomodModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content bg-dark text-light border-warning">
                <div class="modal-header border-secondary">
                    <h5 class="modal-title text-warning"><i class="fa-solid fa-screwdriver-wrench me-2"></i>Chamunda Custom Resto-Mod Blueprint &amp; Specification</h5>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="restomodModalContent"></div>
                </div>
                <div class="modal-footer border-secondary">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    <button type="button" class="btn btn-gold" onclick="printRestomodBlueprint()"><i class="fa-solid fa-print me-1"></i> Print / Open Blueprint</button>
                    <button type="button" class="btn btn-outline-success" onclick="copyRestomodWhatsApp()"><i class="fa-brands fa-whatsapp me-1"></i> Copy WhatsApp Specification</button>
                </div>
            </div>
        </div>
    </div>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Initial parts load
        document.addEventListener("DOMContentLoaded", function() {{
            applyPartsFilter();
            initWaveformCanvas();
            if (typeof updateExpeditionKit === 'function') {{
                updateExpeditionKit();
            }}
            if (typeof updateRestoPreview === 'function') {{
                updateRestoPreview();
            }}
        }});

        // --- Waveform Canvas Animation ---
        let canvas, ctx, animId, isAnimating = false;
        function initWaveformCanvas() {{
            canvas = document.getElementById('waveformCanvas');
            if(!canvas) return;
            ctx = canvas.getContext('2d');
            canvas.width = canvas.parentElement.clientWidth;
            drawIdleWave();
        }}

        function drawIdleWave() {{
            if(!ctx) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.strokeStyle = '#1b4d3e';
            ctx.lineWidth = 2;
            ctx.beginPath();
            let sliceWidth = canvas.width / 100;
            let x = 0;
            for (let i = 0; i < 100; i++) {{
                let y = (canvas.height / 2) + Math.sin(i * 0.15) * 5;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
                x += sliceWidth;
            }}
            ctx.stroke();
        }}

        function startWaveAnimation() {{
            isAnimating = true;
            let step = 0;
            function animate() {{
                if(!isAnimating) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = '#D4AF37';
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                let sliceWidth = canvas.width / 120;
                let x = 0;
                for (let i = 0; i < 120; i++) {{
                    let y = (canvas.height / 2) + Math.sin((i * 0.2) + step) * 24 * Math.cos(i * 0.05);
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                    x += sliceWidth;
                }}
                ctx.stroke();
                step += 0.18;
                animId = requestAnimationFrame(animate);
            }}
            animate();
        }}

        function stopWaveAnimation() {{
            isAnimating = false;
            cancelAnimationFrame(animId);
            drawIdleWave();
        }}

        // --- Sound Diagnostics ---
        async function startLiveListening() {{
            let model = document.getElementById('diagModel').value;
            let btn = document.getElementById('btnLiveListen');
            let statusText = document.getElementById('audioStatusText');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Listening to engine (5s)...';
            statusText.innerText = '🎙️ Recording & analyzing engine sound stream...';
            startWaveAnimation();

            try {{
                let res = await fetch('/api/sound-diagnose', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{bike_model: model, record_seconds: 5}})
                }});
                let data = await res.json();
                renderDiagResult(data);
                statusText.innerText = '✅ Analysis complete!';
            }} catch(err) {{
                alert('Audio analysis error: ' + err);
                statusText.innerText = 'Error capturing sound';
            }} finally {{
                stopWaveAnimation();
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-microphone me-1"></i> Start 5s Live Mic Listening';
            }}
        }}

        async function runSimulatedSound(faultKey) {{
            let model = document.getElementById('diagModel').value;
            let statusText = document.getElementById('audioStatusText');
            statusText.innerText = '🧪 Running calibrated acoustic simulation for [' + faultKey + ']...';
            startWaveAnimation();

            try {{
                let res = await fetch('/api/sound-diagnose', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{bike_model: model, simulate_fault: faultKey}})
                }});
                let data = await res.json();
                renderDiagResult(data);
                statusText.innerText = '✅ Simulation analysis complete!';
            }} catch(err) {{
                alert('Simulation error: ' + err);
            }} finally {{
                stopWaveAnimation();
            }}
        }}

        function renderDiagResult(data) {{
            let c = document.getElementById('diagResultsContainer');
            c.classList.remove('d-none');
            document.getElementById('repDiagId').innerText = data.diagnostic_id;
            
            let scDiv = document.getElementById('repHealthScore');
            scDiv.innerText = data.health_score + ' / 100';
            scDiv.style.color = data.status_color;

            let stDiv = document.getElementById('repHealthStatus');
            stDiv.innerText = data.health_status;
            stDiv.style.color = data.status_color;

            document.getElementById('repRhythm').innerText = data.dominant_freq_hz + ' Hz';
            document.getElementById('repDb').innerText = data.estimated_db + ' dB';
            document.getElementById('repSource').innerText = data.audio_source;
            document.getElementById('repSummaryGu').innerText = data.summary_gu;

            // Anomalies list
            let aList = document.getElementById('repAnomaliesList');
            if (!data.anomalies_detected || data.anomalies_detected.length === 0) {{
                aList.innerHTML = '<div class="alert alert-success py-2 mb-0"><i class="fa-solid fa-circle-check me-2"></i>No mechanical anomalies detected. Factory tolerances optimal.</div>';
            }} else {{
                let items = data.anomalies_detected.map(a => `
                    <div class="mb-2 p-2 rounded" style="background: #182820; border-left: 3px solid #ef4444;">
                        <div class="d-flex justify-content-between">
                            <strong>${{a.title}} (${{a.title_gu}})</strong>
                            <span class="badge bg-danger">${{a.severity}} (${{a.confidence_pct}}%)</span>
                        </div>
                        <small class="text-muted d-block mt-1">Root Cause: ${{a.root_cause}}</small>
                        <small class="text-warning d-block">Action: ${{a.recommended_action}}</small>
                    </div>
                `).join('');
                aList.innerHTML = items;
            }}

            // Matched Parts
            let pDiv = document.getElementById('repMatchedParts');
            let allParts = [];
            if (data.parts_recommendations) {{
                data.parts_recommendations.forEach(r => {{
                    if (r.matched_oem_parts) {{
                        r.matched_oem_parts.forEach(p => allParts.push(p));
                    }}
                }});
            }}

            if (allParts.length === 0) {{
                pDiv.innerHTML = '<p class="text-muted small">No specific replacement parts required.</p>';
            }} else {{
                let pRows = allParts.map(p => `
                    <tr>
                        <td><code>${{p.part_number}}</code></td>
                        <td><strong>${{p.name}}</strong></td>
                        <td class="text-warning">₹${{p.mrp}}</td>
                        <td><span class="badge bg-dark border border-secondary">${{p.stock}} Pcs</span></td>
                        <td><code>${{p.bin_location}}</code></td>
                        <td>
                            <button class="btn btn-sm btn-outline-warning" onclick="promptAddPartToActiveJob('${{p.name}}', ${{p.mrp}})">
                                <i class="fa-solid fa-plus"></i> Allocate to Job
                            </button>
                        </td>
                    </tr>
                `).join('');
                pDiv.innerHTML = `
                    <div class="table-responsive">
                        <table class="table table-custom table-sm">
                            <thead>
                                <tr>
                                    <th>OEM Part No</th>
                                    <th>Part Description</th>
                                    <th>MRP</th>
                                    <th>Stock</th>
                                    <th>Bin</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>${{pRows}}</tbody>
                        </table>
                    </div>
                `;
            }}
        }}

        // --- Parts Filtering ---
        async function applyPartsFilter() {{
            let q = document.getElementById('filterQuery').value;
            let m = document.getElementById('filterModel').value;
            let c = document.getElementById('filterCategory').value;
            let s = document.getElementById('filterStockStatus').value;

            let params = new URLSearchParams();
            if (q) params.append('query', q);
            if (m) params.append('model', m);
            if (c) params.append('category', c);
            if (s) params.append('stock_status', s);
            params.append('limit', 50);

            let res = await fetch('/api/parts/filter?' + params.toString());
            let parts = await res.json();

            let tbody = document.getElementById('partsTableBody');
            if (parts.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="8" class="text-center py-4 text-muted">No spare parts found matching criteria.</td></tr>';
                return;
            }}

            tbody.innerHTML = parts.map(p => {{
                let models = (p.models || []).slice(0, 2).join(', ');
                let stockBadge = p.stock > 0 ? `<span class="text-success fw-bold">${{p.stock}}</span>` : `<span class="text-danger">Out</span>`;
                return `<tr>
                    <td><code>${{p.part_number || p.oem_number}}</code></td>
                    <td><strong>${{p.name}}</strong></td>
                    <td><small>${{p.category}}</small></td>
                    <td class="text-warning fw-bold">₹${{p.mrp}}</td>
                    <td class="text-muted">₹${{p.cost_price}}</td>
                    <td>${{stockBadge}}</td>
                    <td><code>${{p.bin_location || 'A-01'}}</code></td>
                    <td><small class="text-muted">${{models}}</small></td>
                </tr>`;
            }}).join('');
        }}

        // --- Job Card Creation ---
        async function submitJobCard(e) {{
            e.preventDefault();
            let payload = {{
                customer_name: document.getElementById('custName').value,
                phone: document.getElementById('custPhone').value,
                bike_model: document.getElementById('bikeModel').value,
                registration_no: document.getElementById('regNo').value,
                odometer_km: parseInt(document.getElementById('odoKm').value),
                customer_issues: document.getElementById('issues').value
            }};
            let res = await fetch('/api/jobcard', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(payload)
            }});
            if (res.ok) {{
                alert("Job Card Created Successfully!");
                location.reload();
            }}
        }}

        // --- Complete Job and Bill with QR ---
        async function completeAndBillJob(jobId) {{
            if (!confirm("Complete Job Card " + jobId + " and issue official QR Health Passport Tax Invoice?")) return;
            let res = await fetch('/api/jobcard/complete-and-bill', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{job_card_id: jobId}})
            }});
            let data = await res.json();
            if (res.ok) {{
                let modalHtml = `
                    <div class="row g-3">
                        <div class="col-md-7">
                            <h6 class="text-warning mb-1">Invoice: ${{data.invoice_no}}</h6>
                            <p class="mb-1"><strong>Customer:</strong> ${{data.customer_name}} (${{data.bike_model}} - ${{data.registration_no}})</p>
                            <p class="mb-2"><strong>Grand Total:</strong> <span class="text-warning fw-bold">₹${{data.grand_total}}</span> (Subtotal: ₹${{data.subtotal}} + GST: ₹${{data.gst_amount}})</p>
                            <div class="p-2 mb-2 rounded bg-dark border border-warning">
                                <small class="text-warning fw-bold">Digital Acoustic Health Passport:</small><br>
                                <code>${{data.passport_id}}</code> (Score: <strong>${{data.health_score}}/100</strong>)
                            </div>
                            <div class="d-flex gap-2 mt-3">
                                <a href="/invoice/${{data.invoice_no}}" target="_blank" class="btn btn-gold btn-sm"><i class="fa-solid fa-print me-1"></i> Print Tax Invoice</a>
                                <a href="/passport/${{data.passport_id}}" target="_blank" class="btn btn-outline-warning btn-sm"><i class="fa-solid fa-certificate me-1"></i> View Passport</a>
                            </div>
                        </div>
                        <div class="col-md-5 text-center">
                            <img src="${{data.qr_code_base64}}" style="width: 130px; height: 130px; border-radius: 8px; border: 2px solid var(--gold);" alt="Passport QR" />
                            <div class="small text-warning fw-bold mt-1">VERIFIED QR CODE</div>
                            <small class="text-muted d-block" style="font-size: 10px;">Scan to view mobile certificate</small>
                        </div>
                        <div class="col-12 mt-2">
                            <label class="form-label text-warning small fw-bold">WhatsApp Dispatch Copy (Gujarati):</label>
                            <textarea class="form-control bg-dark text-light border-secondary small" rows="3" readonly>${{data.whatsapp_gujarati}}</textarea>
                        </div>
                    </div>
                `;
                document.getElementById('billModalContent').innerHTML = modalHtml;
                new bootstrap.Modal(document.getElementById('billModal')).show();
            }} else {{
                alert("Error completing job: " + (data.error || "Unknown error"));
            }}
        }}

        function promptAddPartToActiveJob(partName, price) {{
            let jobId = prompt("Enter Active Job Card ID (e.g. JOB-20260908-001) to allocate '" + partName + "' (₹" + price + "):");
            if (!jobId) return;
            fetch('/api/jobcard/add-part', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{job_card_id: jobId.trim(), part_name: partName, qty: 1, price: price}})
            }}).then(res => res.json()).then(data => {{
                if (data.success) {{
                    alert("Part allocated successfully to " + jobId + "!");
                }} else {{
                    alert("Failed to allocate part: " + (data.error || "Job card not found"));
                }}
            }});
        }}

        // --- Predictive CRM & WhatsApp Dispatch ---
        let currentWaModalData = {{}};

        function openWhatsAppModal(name, phone, regNo, model, days, odo, health, guText, enText) {{
            currentWaModalData = {{
                name: name,
                phone: phone,
                regNo: regNo,
                model: model,
                days: days,
                odo: odo,
                health: health,
                guText: guText,
                enText: enText
            }};
            document.getElementById('waCustName').innerText = name;
            document.getElementById('waBikeModel').innerText = model;
            document.getElementById('waRegNo').innerText = regNo;
            document.getElementById('waPhone').innerText = phone;
            document.getElementById('waDays').innerText = days + ' Days';
            document.getElementById('waOdo').innerText = odo.toLocaleString();
            document.getElementById('waHealth').innerText = health;
            document.getElementById('waTextGu').value = guText;
            document.getElementById('waTextEn').value = enText;

            new bootstrap.Modal(document.getElementById('whatsappModal')).show();
        }}

        function copyCurrentWhatsAppText() {{
            let guActive = document.getElementById('waGuTab').classList.contains('active');
            let text = guActive ? document.getElementById('waTextGu').value : document.getElementById('waTextEn').value;
            navigator.clipboard.writeText(text);
            alert("WhatsApp reminder text copied to clipboard!");
        }}

        function dispatchToWhatsAppWeb() {{
            let phoneClean = currentWaModalData.phone.replace(/[^0-9]/g, '');
            if (!phoneClean.startsWith('91') && phoneClean.length === 10) {{
                phoneClean = '91' + phoneClean;
            }}
            let guActive = document.getElementById('waGuTab').classList.contains('active');
            let text = guActive ? document.getElementById('waTextGu').value : document.getElementById('waTextEn').value;
            let url = 'https://web.whatsapp.com/send?phone=' + phoneClean + '&text=' + encodeURIComponent(text);
            window.open(url, '_blank');
            markCurrentReminderSent();
        }}

        async function markCurrentReminderSent() {{
            if (!currentWaModalData.regNo) return;
            try {{
                let res = await fetch('/api/crm/mark-sent', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{registration_no: currentWaModalData.regNo}})
                }});
                if (res.ok) {{
                    alert("Reminder marked as dispatched for " + currentWaModalData.regNo);
                }}
            }} catch (err) {{
                console.error(err);
            }}
        }}

        async function generateWholesalePO() {{
            let vendor = prompt("Enter Supplier/Vendor Name for Wholesale PO:", "Royal Enfield OEM Genuine Spares Dist.");
            if (!vendor) return;

            let res = await fetch('/api/po/generate', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{supplier_name: vendor}})
            }});
            let data = await res.json();
            if (res.ok) {{
                let bodyHtml = `
                    <div class="alert alert-success py-2">
                        <i class="fa-solid fa-check-circle me-2"></i>Purchase Order <strong>${{data.po_number}}</strong> generated successfully!
                    </div>
                    <div class="row g-3 mb-3">
                        <div class="col-md-6">
                            <div class="p-3 bg-black rounded border border-warning">
                                <small class="text-muted">Total Reorder SKUs</small>
                                <h4 class="text-warning mb-0">${{data.items.length}} Items</h4>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="p-3 bg-black rounded border border-warning">
                                <small class="text-muted">Total Outlay (Wholesale)</small>
                                <h4 class="text-warning mb-0">₹${{data.total_outlay_inr.toLocaleString()}}</h4>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex gap-2">
                        <a href="/po/${{data.po_number}}" target="_blank" class="btn btn-gold btn-sm"><i class="fa-solid fa-print me-1"></i> Open & Print Formal PO</a>
                    </div>
                `;
                document.getElementById('poModalBody').innerHTML = bodyHtml;
                new bootstrap.Modal(document.getElementById('poModal')).show();
            }} else {{
                alert("Failed to generate PO: " + (data.error || "Unknown error"));
            }}
        }}

        // --- Trinity Innovation 1: Thump Tuner JS ---
        async function runThumpAnalysis() {{
            let model = document.getElementById('thumpModelSelect').value;
            let profile = document.getElementById('thumpProfileSelect').value;
            let res = await fetch('/api/thump/analyze', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{bike_model: model, preset_key: profile}})
            }});
            let data = await res.json();
            if (res.ok) {{
                document.getElementById('thumpResultsBox').style.display = 'block';
                document.getElementById('thumpScoreVal').innerText = data.thump_score + '/100';
                document.getElementById('thumpRatingBadge').innerText = data.rating;
                document.getElementById('thumpRatingBadge').style.backgroundColor = data.badge_color;
                document.getElementById('thumpHzVal').innerText = data.dominant_bass_hz + ' Hz';
                document.getElementById('thumpRpmVal').innerText = data.idle_cadence_bpm + ' RPM';
                document.getElementById('thumpDbVal').innerText = data.estimated_db + ' dB';
                document.getElementById('thumpLegalBadge').className = data.rto_legal_compliant ? 'badge bg-success' : 'badge bg-danger';
                document.getElementById('thumpLegalBadge').innerText = data.rto_legal_compliant ? 'RTO Legal (<85 dB)' : 'Exceeds Legal Limit';
                document.getElementById('thumpSummaryGu').innerText = data.summary_gu;

                let dirHtml = data.mechanic_directives.map(d => `<div class="mb-1 text-light">${{d}}</div>`).join('');
                document.getElementById('thumpDirectivesList').innerHTML = dirHtml;
            }} else {{
                alert("Failed to analyze thump: " + (data.error || "Unknown error"));
            }}
        }}

        // --- Trinity Innovation 2: Stage Update & Customer Bot JS ---
        async function updateJobStage(jobId, stageName) {{
            let res = await fetch('/api/jobcard/update-stage', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{job_card_id: jobId, stage_name: stageName}})
            }});
            let data = await res.json();
            if (res.ok && data.success) {{
                alert(`Stage updated to: "${{stageName}}" for ${{jobId}}`);
                location.reload();
            }} else {{
                alert("Error updating stage: " + (data.error || "Failed"));
            }}
        }}

        let activeTrackWhatsAppMsg = "";
        async function trackServiceLive() {{
            let q = document.getElementById('trackInput').value.trim();
            if (!q) {{
                alert("Please enter a bike registration number or phone number!");
                return;
            }}
            let res = await fetch('/api/bot/track/' + encodeURIComponent(q));
            let data = await res.json();
            if (res.ok && data.found) {{
                document.getElementById('trackerResultBox').style.display = 'block';
                document.getElementById('trCustName').innerText = data.customer_name + ' • ' + data.job_card_id;
                document.getElementById('trBikeInfo').innerText = data.bike_model + ' (' + data.registration_no + ')';
                document.getElementById('trProgressBadge').innerText = data.progress_pct + '%';
                document.getElementById('trProgressBar').style.width = data.progress_pct + '%';
                document.getElementById('trMechanic').innerText = data.mechanic_assigned || 'Master Tech Alpesh';
                document.getElementById('trDelivery').innerText = data.estimated_delivery || 'Today 05:30 PM';
                document.getElementById('trBill').innerText = '₹' + (data.estimated_total_inr || 0).toLocaleString();
                document.getElementById('trMessageGu').innerText = data.message_gu;
                activeTrackWhatsAppMsg = data.message_gu;

                // Highlight active step
                for (let i = 0; i < 5; i++) {{
                    let stepEl = document.getElementById('step' + i);
                    if (stepEl) {{
                        if (i < data.stage_index) {{
                            stepEl.className = 'p-2 rounded border border-success bg-dark text-success';
                        }} else if (i === data.stage_index) {{
                            stepEl.className = 'p-2 rounded border border-warning bg-black text-warning fw-bold shadow';
                        }} else {{
                            stepEl.className = 'p-2 rounded border border-secondary text-muted';
                        }}
                    }}
                }}
            }} else {{
                alert(data.message || "No active job card found for: " + q);
            }}
        }}

        function copyTrackerWhatsAppMsg() {{
            if (!activeTrackWhatsAppMsg) return;
            navigator.clipboard.writeText(activeTrackWhatsAppMsg);
            alert("WhatsApp status update copied to clipboard!");
        }}

        function sendQuickChat(txt) {{
            document.getElementById('chatInput').value = txt;
            sendChatMessage();
        }}

        async function sendChatMessage() {{
            let input = document.getElementById('chatInput');
            let txt = input.value.trim();
            if (!txt) return;

            let cWin = document.getElementById('chatWindow');
            cWin.innerHTML += `
                <div class="d-flex justify-content-end mb-2">
                    <div class="p-2 rounded bg-success text-white small" style="max-width: 85%;">
                        ${{txt}}
                    </div>
                </div>
            `;
            input.value = '';
            cWin.scrollTop = cWin.scrollHeight;

            let res = await fetch('/api/bot/chat', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{message: txt}})
            }});
            let data = await res.json();
            if (res.ok) {{
                let reply = (data.reply || data.reply_gu || data.reply_en || "").replace(/\\n/g, '<br>');
                cWin.innerHTML += `
                    <div class="d-flex mb-2">
                        <div class="p-2 rounded bg-dark border border-secondary text-light small" style="max-width: 85%;">
                            <strong class="text-warning">👑 Chamunda AI:</strong><br>
                            ${{reply}}
                        </div>
                    </div>
                `;
            }} else {{
                cWin.innerHTML += `
                    <div class="d-flex mb-2">
                        <div class="p-2 rounded bg-danger text-white small">
                            Bot error. Please try again.
                        </div>
                    </div>
                `;
            }}
            cWin.scrollTop = cWin.scrollHeight;
        }}

        // --- Trinity Innovation 3: Countertop POS & Dynamic UPI QR JS ---
        let posCart = [];
        let currentPosSaleData = null;

        function openPOSModal() {{
            new bootstrap.Modal(document.getElementById('posModal')).show();
        }}

        async function posScanAndAdd() {{
            let code = document.getElementById('posScanInput').value.trim();
            if (!code) return;
            await posProcessPartCode(code);
            document.getElementById('posScanInput').value = '';
        }}

        async function posQuickAdd(code) {{
            await posProcessPartCode(code);
        }}

        async function posProcessPartCode(code) {{
            let res = await fetch('/api/pos/scan', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{code_or_query: code}})
            }});
            let data = await res.json();
            if (res.ok && data.found) {{
                let part = data.part;
                let existing = posCart.find(item => item.part_id === part.part_id);
                if (existing) {{
                    existing.qty += 1;
                }} else {{
                    posCart.push({{
                        part_id: part.part_id,
                        name: part.name,
                        part_number: part.part_number || part.oem_number,
                        price: parseFloat(part.mrp || 0),
                        qty: 1
                    }});
                }}
                renderPOSCart();
            }} else {{
                alert("Part not found in 4,469 catalog for query: " + code);
            }}
        }}

        function renderPOSCart() {{
            let tbody = document.getElementById('posCartBody');
            if (posCart.length === 0) {{
                tbody.innerHTML = '<tr><td colspan="6" class="text-center py-4 text-muted">Cart is empty. Scan barcode or click quick parts above.</td></tr>';
                posRecalcTotals();
                return;
            }}

            tbody.innerHTML = posCart.map((item, idx) => `
                <tr>
                    <td><strong>${{item.name}}</strong></td>
                    <td><code>${{item.part_number}}</code></td>
                    <td>
                        <input type="number" min="1" class="form-control form-control-sm bg-dark text-light border-secondary text-center py-0" style="width: 55px;" value="${{item.qty}}" onchange="posUpdateQty(${{idx}}, this.value)">
                    </td>
                    <td>₹${{item.price.toFixed(2)}}</td>
                    <td class="text-warning fw-bold">₹${{(item.price * item.qty).toFixed(2)}}</td>
                    <td>
                        <button class="btn btn-outline-danger btn-sm py-0" onclick="posRemoveItem(${{idx}})">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `).join('');

            posRecalcTotals();
        }}

        function posUpdateQty(idx, val) {{
            let q = parseInt(val) || 1;
            posCart[idx].qty = Math.max(1, q);
            renderPOSCart();
        }}

        function posRemoveItem(idx) {{
            posCart.splice(idx, 1);
            renderPOSCart();
        }}

        function posRecalcTotals() {{
            let subtotal = posCart.reduce((sum, itm) => sum + (itm.price * itm.qty), 0);
            let discount = parseFloat(document.getElementById('posDiscount').value) || 0;
            let net = Math.max(0, subtotal - discount);

            document.getElementById('posSubtotal').innerText = '₹' + subtotal.toFixed(2);
            document.getElementById('posNetTotal').innerText = '₹' + net.toFixed(2);
        }}

        async function posExecuteCheckout() {{
            if (posCart.length === 0) {{
                alert("Please add at least one spare part to the cart before checkout!");
                return;
            }}
            let discount = parseFloat(document.getElementById('posDiscount').value) || 0;
            let custName = document.getElementById('posCustName').value.trim() || 'Walk-in Counter Customer';
            let custPhone = document.getElementById('posCustPhone').value.trim();

            let payload = {{
                items: posCart,
                customer_name: custName,
                phone: custPhone,
                payment_mode: "UPI",
                discount_amount: discount
            }};

            let res = await fetch('/api/pos/checkout', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(payload)
            }});
            let data = await res.json();
            if (res.ok && data.receipt_no) {{
                currentPosSaleData = data;
                document.getElementById('posCheckoutResultBox').style.display = 'block';
                document.getElementById('posReceiptNo').innerText = 'RECEIPT: ' + data.receipt_no + ' • ₹' + data.net_amount.toFixed(2);
                document.getElementById('posQrImage').src = data.qr_code_base64;
                posCart = [];
                renderPOSCart();
                alert(`POS Sale Completed! Receipt #${{data.receipt_no}} issued. Dynamic UPI QR generated.`);
            }} else {{
                alert("Checkout failed: " + (data.error || "Unknown error"));
            }}
        }}

        function posPrintCurrentReceipt() {{
            if (!currentPosSaleData || !currentPosSaleData.receipt_no) return;
            window.open('/pos/receipt/' + currentPosSaleData.receipt_no, '_blank');
        }}

        function posCopyWhatsAppReceipt() {{
            if (!currentPosSaleData) return;
            let msg = currentPosSaleData.whatsapp_message_gu || currentPosSaleData.whatsapp_message_en;
            navigator.clipboard.writeText(msg);
            alert("POS Receipt WhatsApp text copied to clipboard!");
        }}

        // --- Pre-Owned RE Inspection & Valuation Functions ---
        let currentCertData = null;

        function syncPreownedModel() {{
            let sel = document.getElementById('inspBikeModel').value;
            document.getElementById('valModelDisplay').value = sel;
            runLiveValuation();
        }}

        function calcLiveScore() {{
            let e = parseInt(document.getElementById('pts_engine').value) || 0;
            let c = parseInt(document.getElementById('pts_chassis').value) || 0;
            let a = parseInt(document.getElementById('pts_acoustic').value) || 0;
            let b = parseInt(document.getElementById('pts_brakes').value) || 0;
            let el = parseInt(document.getElementById('pts_electrical').value) || 0;
            let ae = parseInt(document.getElementById('pts_aesthetics').value) || 0;
            let total = e + c + a + b + el + ae;

            let tier = "REPAIR REQUIRED";
            let cls = "bg-danger";
            if (total >= 90) {{ tier = "PLATINUM CERTIFIED"; cls = "bg-warning text-dark"; }}
            else if (total >= 80) {{ tier = "GOLD CERTIFIED"; cls = "bg-success text-light"; }}
            else if (total >= 70) {{ tier = "SILVER CERTIFIED"; cls = "bg-info text-dark"; }}

            let badge = document.getElementById('liveScoreBadge');
            badge.className = `badge ${{cls}} fw-bold fs-6`;
            badge.innerText = `${{total}} / 100 • ${{tier}}`;

            document.getElementById('valScoreDisplay').value = total;
            document.getElementById('valYearDisplay').value = document.getElementById('inspYear').value;
            document.getElementById('valOdoDisplay').value = document.getElementById('inspOdo').value;
        }}

        async function runLiveValuation() {{
            let model = document.getElementById('valModelDisplay').value || 'Classic 350';
            let year = parseInt(document.getElementById('valYearDisplay').value) || 2022;
            let odo = parseInt(document.getElementById('valOdoDisplay').value) || 18500;
            let score = parseFloat(document.getElementById('valScoreDisplay').value) || 85.0;

            try {{
                let res = await fetch('/api/preowned/valuation', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        bike_model: model,
                        manufacturing_year: year,
                        odometer_km: odo,
                        condition_score: score
                    }})
                }});
                let data = await res.json();
                if (res.ok) {{
                    document.getElementById('resFairVal').innerText = '₹' + data.fair_market_value_inr.toLocaleString('en-IN');
                    document.getElementById('resBuyerPrice').innerText = '₹' + data.recommended_buyer_price_inr.toLocaleString('en-IN');
                    document.getElementById('resSellerPrice').innerText = '₹' + data.recommended_seller_asking_inr.toLocaleString('en-IN');
                    document.getElementById('resMarketDemand').innerText = data.gujarat_market_demand;
                }}
            }} catch (err) {{
                console.error("Valuation error:", err);
            }}
        }}

        function quickFillInspectionDemo() {{
            document.getElementById('inspBikeModel').value = 'Classic 350';
            document.getElementById('inspRegNo').value = 'GJ-01-RE-2022';
            document.getElementById('inspYear').value = 2022;
            document.getElementById('inspOdo').value = 18500;
            document.getElementById('inspOwner').value = 'Ramesh Patel';
            document.getElementById('inspPhone').value = '+91 98250 12345';
            document.getElementById('pts_engine').value = 23;
            document.getElementById('pts_chassis').value = 19;
            document.getElementById('pts_acoustic').value = 14;
            document.getElementById('pts_brakes').value = 14;
            document.getElementById('pts_electrical').value = 14;
            document.getElementById('pts_aesthetics').value = 9;
            document.getElementById('lbl_engine').innerText = '23';
            document.getElementById('lbl_chassis').innerText = '19';
            document.getElementById('lbl_acoustic').innerText = '14';
            document.getElementById('lbl_brakes').innerText = '14';
            document.getElementById('lbl_electrical').innerText = '14';
            document.getElementById('lbl_aesthetics').innerText = '9';
            syncPreownedModel();
            calcLiveScore();
        }}

        async function submit100PointInspection() {{
            let model = document.getElementById('inspBikeModel').value;
            let reg = document.getElementById('inspRegNo').value.trim();
            let year = parseInt(document.getElementById('inspYear').value) || 2022;
            let odo = parseInt(document.getElementById('inspOdo').value) || 15000;
            let owner = document.getElementById('inspOwner').value.trim() || 'Owner / Seller';
            let phone = document.getElementById('inspPhone').value.trim() || '+91 98000 00000';

            if (!reg) {{
                alert("Please enter bike registration number (e.g. GJ-01-RE-2022)");
                return;
            }}

            let overrides = {{
                engine_pts: parseInt(document.getElementById('pts_engine').value) || 23,
                chassis_pts: parseInt(document.getElementById('pts_chassis').value) || 19,
                acoustic_pts: parseInt(document.getElementById('pts_acoustic').value) || 14,
                brakes_pts: parseInt(document.getElementById('pts_brakes').value) || 14,
                electrical_pts: parseInt(document.getElementById('pts_electrical').value) || 14,
                aesthetics_pts: parseInt(document.getElementById('pts_aesthetics').value) || 9
            }};

            let payload = {{
                customer_name: owner,
                phone: phone,
                bike_model: model,
                registration_no: reg,
                manufacturing_year: year,
                odometer_km: odo,
                checklist_overrides: overrides
            }};

            try {{
                let res = await fetch('/api/preowned/inspect', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(payload)
                }});
                let data = await res.json();
                if (res.ok && data.cert_id) {{
                    currentCertData = data;
                    renderPreownedModal(data);
                    let modal = new bootstrap.Modal(document.getElementById('preownedModal'));
                    modal.show();
                }} else {{
                    alert("Inspection failed: " + (data.error || "Unknown error"));
                }}
            }} catch (err) {{
                alert("Network error submitting inspection: " + err);
            }}
        }}

        function renderPreownedModal(data) {{
            let content = `
                <div class="p-3 bg-black rounded border border-warning text-center mb-3">
                    <span class="badge bg-gold text-dark fs-6 mb-2">${{data.certification_tier}}</span>
                    <h3 class="text-warning mb-1">${{data.bike_model}} • ${{data.registration_no}}</h3>
                    <div class="display-5 text-light fw-bold mb-2">${{data.total_score}} <span class="fs-4 text-muted">/ 100</span></div>
                    <div class="text-success fw-bold">${{data.warranty_shield}}</div>
                </div>
                <div class="row g-2 mb-3">
                    <div class="col-6">
                        <div class="p-2 bg-dark rounded border border-secondary">
                            <span class="text-muted small">Fair Market Valuation:</span><br>
                            <strong class="text-warning fs-5">₹${{data.fair_market_valuation.fair_market_value_inr.toLocaleString('en-IN')}}</strong>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="p-2 bg-dark rounded border border-secondary text-center">
                            <img src="${{data.qr_code_base64}}" style="width: 70px; height: 70px; border-radius: 4px;" alt="QR">
                            <div class="text-muted" style="font-size: 10px;">Scannable Online Shield</div>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('preownedModalContent').innerHTML = content;
        }}

        function printPreownedCert() {{
            if (!currentCertData || !currentCertData.cert_id) return;
            window.open('/certification/' + currentCertData.cert_id, '_blank');
        }}

        function copyPreownedWhatsApp() {{
            if (!currentCertData) return;
            let msg = currentCertData.whatsapp_message_gu || currentCertData.whatsapp_message_en;
            navigator.clipboard.writeText(msg);
            alert("Chamunda Certified Pre-Owned WhatsApp report copied to clipboard!");
        }}

        // --- Expedition Readiness & Highway SOS Functions ---
        let currentExpData = null;

        function syncExpeditionModel() {{
            updateExpeditionKit();
        }}

        function calcExpLiveScore() {{
            let f = parseInt(document.getElementById('pts_exp_fluids').value) || 0;
            let ch = parseInt(document.getElementById('pts_exp_chain').value) || 0;
            let b = parseInt(document.getElementById('pts_exp_brakes').value) || 0;
            let el = parseInt(document.getElementById('pts_exp_electrical').value) || 0;
            let c = parseInt(document.getElementById('pts_exp_chassis').value) || 0;
            let t = parseInt(document.getElementById('pts_exp_tyres').value) || 0;
            let total = f + ch + b + el + c + t;

            let tier = "EXPEDITION REJECTED";
            let cls = "bg-danger";
            if (total >= 90) {{ tier = "EXPEDITION CERTIFIED (LADAKH READY)"; cls = "bg-warning text-dark"; }}
            else if (total >= 80) {{ tier = "HIGHWAY TOURING READY"; cls = "bg-success text-light"; }}
            else if (total >= 70) {{ tier = "SHORT RUN APPROVED"; cls = "bg-info text-dark"; }}

            let badge = document.getElementById('expLiveScoreBadge');
            badge.className = `badge ${{cls}} fw-bold fs-6`;
            badge.innerText = `${{total}} / 100 • ${{tier}}`;
        }}

        function quickFillExpeditionDemo() {{
            document.getElementById('expBikeModel').value = 'Himalayan 450';
            document.getElementById('expRegNo').value = 'GJ-01-EX-4500';
            document.getElementById('expDestination').value = 'ladakh_high_altitude';
            document.getElementById('expPlannedKm').value = '3800';
            document.getElementById('expRider').value = 'Alpesh Patel';
            document.getElementById('expPhone').value = '+91 98250 12345';
            document.getElementById('pts_exp_fluids').value = 19;
            document.getElementById('pts_exp_chain').value = 14;
            document.getElementById('pts_exp_brakes').value = 14;
            document.getElementById('pts_exp_electrical').value = 14;
            document.getElementById('pts_exp_chassis').value = 19;
            document.getElementById('pts_exp_tyres').value = 14;
            document.getElementById('lbl_exp_fluids').innerText = '19';
            document.getElementById('lbl_exp_chain').innerText = '14';
            document.getElementById('lbl_exp_brakes').innerText = '14';
            document.getElementById('lbl_exp_electrical').innerText = '14';
            document.getElementById('lbl_exp_chassis').innerText = '19';
            document.getElementById('lbl_exp_tyres').innerText = '14';
            calcExpLiveScore();
            updateExpeditionKit();
        }}

        async function updateExpeditionKit() {{
            let model = document.getElementById('expBikeModel').value || 'Himalayan 450';
            let dest = document.getElementById('expDestination').value || 'ladakh_high_altitude';

            try {{
                let res = await fetch('/api/expedition/spares-kit', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{
                        bike_model: model,
                        destination_key: dest
                    }})
                }});
                let data = await res.json();
                if (res.ok) {{
                    let itemsHtml = data.items.map(it => `
                        <div class="p-2 bg-dark rounded border border-secondary mb-2 d-flex justify-content-between align-items-center">
                            <div>
                                <strong class="text-light" style="font-size: 13px;">${{it.name}}</strong><br>
                                <small class="text-muted"><code>${{it.part_number}}</code> • ${{it.role}}</small>
                            </div>
                            <div class="text-end">
                                <span class="text-warning fw-bold">₹${{it.mrp}}</span>
                            </div>
                        </div>
                    `).join('');

                    document.getElementById('sparesKitContent').innerHTML = `
                        <div class="p-2 bg-black rounded border border-warning mb-3">
                            <div class="d-flex justify-content-between text-muted small">
                                <span>Essential Spares:</span>
                                <strong class="text-light">${{data.total_parts_count}} Items</strong>
                            </div>
                            <div class="d-flex justify-content-between align-items-center mt-1">
                                <span class="text-warning fw-bold">TOTAL KIT COST:</span>
                                <strong class="text-warning fs-5">₹${{data.total_kit_mrp.toLocaleString('en-IN')}}</strong>
                            </div>
                        </div>
                        <div style="max-height: 250px; overflow-y: auto;">
                            ${{itemsHtml}}
                        </div>
                    `;
                }}
            }} catch (err) {{
                console.error("Kit load error:", err);
            }}
        }}

        async function submitExpeditionAudit() {{
            let model = document.getElementById('expBikeModel').value;
            let reg = document.getElementById('expRegNo').value.trim();
            let dest = document.getElementById('expDestination').value;
            let km = parseInt(document.getElementById('expPlannedKm').value) || 3000;
            let rider = document.getElementById('expRider').value.trim() || 'Rider';
            let phone = document.getElementById('expPhone').value.trim() || '+91 98250 12345';

            if (!reg) {{
                alert("Please enter motorcycle registration number (e.g. GJ-01-EX-4500)");
                return;
            }}

            let scores = {{
                fluids_pts: parseInt(document.getElementById('pts_exp_fluids').value) || 19,
                chain_pts: parseInt(document.getElementById('pts_exp_chain').value) || 14,
                brakes_pts: parseInt(document.getElementById('pts_exp_brakes').value) || 14,
                electrical_pts: parseInt(document.getElementById('pts_exp_electrical').value) || 14,
                chassis_pts: parseInt(document.getElementById('pts_exp_chassis').value) || 19,
                tyres_pts: parseInt(document.getElementById('pts_exp_tyres').value) || 14
            }};

            let payload = {{
                rider_name: rider,
                phone: phone,
                bike_model: model,
                registration_no: reg,
                destination_key: dest,
                planned_km: km,
                domain_scores: scores
            }};

            try {{
                let res = await fetch('/api/expedition/audit', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify(payload)
                }});
                let data = await res.json();
                if (res.ok && data.exp_id) {{
                    currentExpData = data;
                    renderExpeditionModal(data);
                    let modal = new bootstrap.Modal(document.getElementById('expeditionModal'));
                    modal.show();
                }} else {{
                    alert("Audit failed: " + (data.error || "Unknown error"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        function renderExpeditionModal(data) {{
            let content = `
                <div class="p-3 bg-black rounded border border-warning text-center mb-3">
                    <span class="badge bg-gold text-dark fs-6 mb-2">${{data.clearance_tier}}</span>
                    <h3 class="text-warning mb-1">${{data.bike_model}} • ${{data.registration_no}}</h3>
                    <div class="display-5 text-light fw-bold mb-1">${{data.total_score}} <span class="fs-4 text-muted">/ 100</span></div>
                    <div class="text-info">${{data.destination_title}} (~${{data.planned_km.toLocaleString('en-IN')}} KM)</div>
                    <small class="text-muted mt-2 d-block">${{data.directive}}</small>
                </div>
                <div class="row g-2 mb-3">
                    <div class="col-6">
                        <div class="p-2 bg-dark rounded border border-secondary">
                            <span class="text-muted small">Carry-Along Spares:</span><br>
                            <strong class="text-warning">${{data.spares_kit.total_parts_count}} Items • ₹${{data.spares_kit.total_kit_mrp.toLocaleString('en-IN')}}</strong>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="p-2 bg-dark rounded border border-secondary text-center">
                            <img src="${{data.qr_code_base64}}" style="width: 70px; height: 70px; border-radius: 4px;" alt="QR">
                            <div class="text-muted" style="font-size: 10px;">Verifiable Clearance QR</div>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('expeditionModalContent').innerHTML = content;
        }}

        function printExpeditionPassport() {{
            if (!currentExpData || !currentExpData.exp_id) return;
            window.open('/expedition/' + currentExpData.exp_id, '_blank');
        }}

        function copyExpeditionWhatsApp() {{
            if (!currentExpData) return;
            let msg = currentExpData.whatsapp_message_gu || currentExpData.whatsapp_message_en;
            navigator.clipboard.writeText(msg);
            alert("Chamunda Expedition Clearance WhatsApp broadcast copied to clipboard!");
        }}

        async function runSOSTriage(symptomKey) {{
            document.getElementById('sosQueryInput').value = symptomKey;
            await executeSOSTriage(symptomKey);
        }}

        async function runSOSTriageFromInput() {{
            let q = document.getElementById('sosQueryInput').value.trim();
            if (!q) return;
            await executeSOSTriage(q);
        }}

        async function executeSOSTriage(query) {{
            try {{
                let res = await fetch('/api/expedition/sos-triage', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{ symptom_query: query }})
                }});
                let data = await res.json();
                if (res.ok) {{
                    document.getElementById('sosResultBox').style.display = 'block';
                    document.getElementById('sosFaultTitle').innerText = data.fault_title + ' (' + data.fault_title_gu + ')';
                    document.getElementById('sosSeverity').innerText = data.severity;
                    document.getElementById('sosActionGu').innerText = data.immediate_action_gu;
                    document.getElementById('sosActionEn').innerText = data.immediate_action_en;
                    document.getElementById('sosToolkit').innerText = data.toolkit_needed;
                    document.getElementById('sosSpare').innerText = data.spare_part_needed;
                }}
            }} catch (err) {{
                console.error("SOS triage error:", err);
            }}
        }}

        // --- Tab 10: Custom Resto-Mod & Vintage CI Studio Scripts ---
        let currentRestoBlueprint = null;

        function quickFillRestoDemo() {{
            document.getElementById('restoCustomer').value = "Kishorbhai Parmar";
            document.getElementById('restoPhone').value = "+91 98250 44551";
            document.getElementById('restoModel').value = "Bullet 350 Cast-Iron CI";
            document.getElementById('restoRegNo').value = "GJ-01-AB-1982";
            document.getElementById('restoStyle').value = "bobber_solo";
            document.getElementById('restoPaint').value = "matte_phantom_black";
            document.getElementById('restoStage').value = "stage_1_street_thump";
            document.getElementById('restoIncludeVintage').checked = true;
            document.getElementById('restoNotes').value = "Solo sprung saddle, matte black custom megaphone exhaust, brass tank badges, heavy crank tuning & de-carbonize.";
            updateRestoPreview();
        }}

        function updateRestoPreview() {{
            const styleRates = {{
                "bobber_solo": {{ labor: 38000, days: 21, bom: 24500 }},
                "cafe_racer": {{ labor: 45000, days: 28, bom: 28000 }},
                "desert_scrambler": {{ labor: 42000, days: 25, bom: 26000 }},
                "vintage_heritage_standard": {{ labor: 35000, days: 21, bom: 22000 }}
            }};
            const paintRates = {{
                "british_racing_green_gold": 18500,
                "matte_phantom_black": 15000,
                "desert_sand_patina": 16500,
                "candy_royal_maroon": 19500,
                "vintage_gunmetal_silver": 17500
            }};
            const stageRates = {{
                "stage_0_stock": {{ cost: 0, days: 0 }},
                "stage_1_street_thump": {{ cost: 14500, days: 5 }},
                "stage_2_dyno_sprint": {{ cost: 29500, days: 10 }}
            }};

            const sKey = document.getElementById('restoStyle').value;
            const pKey = document.getElementById('restoPaint').value;
            const stKey = document.getElementById('restoStage').value;
            const incVintage = document.getElementById('restoIncludeVintage').checked;

            const labor = (styleRates[sKey] || styleRates["bobber_solo"]).labor;
            const baseDays = (styleRates[sKey] || styleRates["bobber_solo"]).days;
            const estBom = (styleRates[sKey] || styleRates["bobber_solo"]).bom;
            const paint = paintRates[pKey] || 15000;
            const stage = (stageRates[stKey] || stageRates["stage_1_street_thump"]).cost;
            const stageDays = (stageRates[stKey] || stageRates["stage_1_street_thump"]).days;
            const vintage = incVintage ? 12500 : 0;
            const vintageDays = incVintage ? 7 : 0;

            const grand = labor + paint + stage + vintage + estBom;
            const totalDays = baseDays + stageDays + vintageDays;

            document.getElementById('previewLabor').innerText = '₹' + labor.toLocaleString('en-IN');
            document.getElementById('previewPaint').innerText = '₹' + paint.toLocaleString('en-IN');
            document.getElementById('previewTune').innerText = '₹' + stage.toLocaleString('en-IN');
            document.getElementById('previewVintage').innerText = '₹' + vintage.toLocaleString('en-IN');
            document.getElementById('previewBOM').innerText = '₹' + estBom.toLocaleString('en-IN');
            document.getElementById('previewGrand').innerText = '₹' + grand.toLocaleString('en-IN');
            document.getElementById('previewDays').innerText = totalDays;
        }}

        async function generateRestoBlueprint() {{
            const customer = document.getElementById('restoCustomer').value.trim();
            const phone = document.getElementById('restoPhone').value.trim();
            const model = document.getElementById('restoModel').value;
            const regNo = document.getElementById('restoRegNo').value.trim();
            const style = document.getElementById('restoStyle').value;
            const paint = document.getElementById('restoPaint').value;
            const stage = document.getElementById('restoStage').value;
            const incVintage = document.getElementById('restoIncludeVintage').checked;
            const notes = document.getElementById('restoNotes').value.trim();

            if (!customer || !phone || !regNo) {{
                alert("Please fill in Customer Name, WhatsApp Phone, and Vehicle Registration Number.");
                return;
            }}

            try {{
                const res = await fetch('/api/restomod/quote', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        customer_name: customer,
                        phone: phone,
                        bike_model: model,
                        registration_no: regNo,
                        style_key: style,
                        paint_theme_key: paint,
                        performance_stage_key: stage,
                        include_vintage_ci_package: incVintage,
                        custom_notes: notes
                    }})
                }});
                const data = await res.json();
                if (!res.ok) {{
                    alert("Failed to generate blueprint: " + (data.error || "Unknown error"));
                    return;
                }}

                currentRestoBlueprint = data;

                // Render Modal Content
                let bomHtml = '';
                if (data.bom_parts && data.bom_parts.length > 0) {{
                    bomHtml = '<div class="table-responsive my-3">' +
                        '<table class="table table-sm table-dark table-bordered mb-0">' +
                        '<thead>' +
                        '<tr class="text-warning"><th>SKU</th><th>Part Description</th><th>Category</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>' +
                        '</thead><tbody>' +
                        data.bom_parts.map(p => '<tr><td><code>' + p.sku + '</code></td><td>' + p.name + '</td><td><span class="badge bg-secondary">' + p.category + '</span></td><td>' + p.quantity + '</td><td>₹' + p.unit_price.toLocaleString('en-IN') + '</td><td class="text-warning">₹' + p.total_price.toLocaleString('en-IN') + '</td></tr>').join('') +
                        '</tbody></table></div>';
                }}

                let modalHtml = '<div class="text-center pb-3 border-bottom border-secondary mb-3">' +
                    '<span class="badge bg-warning text-dark px-3 py-1 fw-bold fs-6 mb-2">CHAMUNDA BESPOKE RESTO-MOD BLUEPRINT</span>' +
                    '<h4 class="text-warning fw-bold mb-1">' + data.resto_id + '</h4>' +
                    '<p class="text-muted small mb-2">Authenticated on Chamunda Engine • Timestamp: ' + data.timestamp + '</p>' +
                    '<img src="data:image/png;base64,' + data.qr_code_base64 + '" alt="Blueprint QR" style="width: 120px; height: 120px; border: 2px solid #d4af37; border-radius: 8px;" class="p-1 bg-white mb-2">' +
                    '<div class="small text-muted">Scan QR to verify authentic Chamunda Build Certificate online</div></div>' +
                    '<div class="row g-3 mb-3">' +
                    '<div class="col-md-6"><div class="p-3 bg-black rounded border border-secondary">' +
                    '<small class="text-muted d-block text-uppercase fw-bold">Client &amp; Platform</small>' +
                    '<strong class="text-warning">' + data.customer_name + '</strong> (' + data.phone + ')<br>' +
                    '<span class="text-light">' + data.bike_model + '</span> • <code class="text-warning">' + data.registration_no + '</code>' +
                    '</div></div>' +
                    '<div class="col-md-6"><div class="p-3 bg-black rounded border border-secondary">' +
                    '<small class="text-muted d-block text-uppercase fw-bold">Styling &amp; Finish</small>' +
                    '<strong class="text-warning">' + data.style_name + '</strong><br>' +
                    '<span class="text-light">' + data.paint_name + '</span>' +
                    '</div></div></div>' +
                    '<div class="p-3 bg-black rounded border border-warning mb-3">' +
                    '<div class="row text-center g-2">' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Style Labor</small><strong class="text-light">₹' + data.cost_breakdown.style_labor.toLocaleString('en-IN') + '</strong></div>' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Paint Theme</small><strong class="text-light">₹' + data.cost_breakdown.paint_finish.toLocaleString('en-IN') + '</strong></div>' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Dyno Tune</small><strong class="text-light">₹' + data.cost_breakdown.performance_tuning.toLocaleString('en-IN') + '</strong></div>' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Vintage CI</small><strong class="text-light">₹' + data.cost_breakdown.vintage_ci_package.toLocaleString('en-IN') + '</strong></div>' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Parts BOM</small><strong class="text-light">₹' + data.cost_breakdown.bom_spares.toLocaleString('en-IN') + '</strong></div>' +
                    '<div class="col-4 col-md-2"><small class="text-muted d-block">Grand Total</small><strong class="text-warning fs-5">₹' + data.grand_total.toLocaleString('en-IN') + '</strong></div>' +
                    '</div><div class="text-center mt-2 text-muted small">Turnaround Timeline: <strong class="text-warning">' + data.timeline_days + ' Working Days</strong></div></div>' +
                    '<h6 class="text-warning mb-2"><i class="fa-solid fa-boxes-stacked me-2"></i>Locked Bill of Materials (BOM) Spares:</h6>' +
                    bomHtml +
                    '<div class="p-3 bg-black rounded border border-secondary mt-3">' +
                    '<div class="d-flex justify-content-between align-items-center mb-1">' +
                    '<strong class="text-warning small"><i class="fa-solid fa-gauge-high me-1"></i> Dyno Performance Calibration</strong>' +
                    '<span class="badge bg-success">' + (data.performance_specs.rto_legal_noise ? 'RTO Legal &lt;85 dB' : 'Track Only') + '</span></div>' +
                    '<div class="small text-muted">Power Gain: <span class="text-light">' + data.performance_specs.hp_gain + '</span> | Torque Gain: <span class="text-light">' + data.performance_specs.torque_gain + '</span></div>' +
                    '<div class="small text-muted">Thump Profile: <span class="text-warning">' + data.performance_specs.exhaust_note_db + '</span></div></div>';

                document.getElementById('restomodModalContent').innerHTML = modalHtml;

                // Add to registry table
                const tbody = document.getElementById('restoRegistryBody');
                if (tbody) {{
                    const newRow = '<tr>' +
                        '<td><strong>' + data.resto_id + '</strong><br><small class="text-muted">Just Now</small></td>' +
                        '<td><strong>' + data.bike_model + '</strong><br><small class="text-warning"><code>' + data.registration_no + '</code></small></td>' +
                        '<td><strong>' + data.customer_name + '</strong><br><small class="text-muted">' + data.phone + '</small></td>' +
                        '<td><span class="badge bg-dark border border-warning text-warning">' + data.style_name + '</span></td>' +
                        '<td><span class="badge bg-secondary">' + data.paint_name + '</span></td>' +
                        '<td><strong class="text-warning">₹' + data.grand_total.toLocaleString('en-IN') + '</strong><br><small class="text-muted">' + data.timeline_days + ' Days</small></td>' +
                        '<td><a href="/restomod/' + data.resto_id + '" target="_blank" class="btn btn-sm btn-outline-warning"><i class="fa-solid fa-file-invoice me-1"></i> Blueprint</a></td>' +
                        '</tr>';
                    tbody.innerHTML = newRow + tbody.innerHTML;
                }}

                const modal = new bootstrap.Modal(document.getElementById('restomodModal'));
                modal.show();

            }} catch (err) {{
                console.error("RestoMod quote error:", err);
                alert("Failed to connect to Resto-Mod Studio server.");
            }}
        }}

        async function runDynoAnalysis() {{
            const model = document.getElementById('dynoModelSelect').value;
            const stage = document.getElementById('dynoStageSelect').value;

            try {{
                const res = await fetch('/api/restomod/performance-tune', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ bike_model: model, stage_key: stage }})
                }});
                const data = await res.json();
                if (res.ok) {{
                    document.getElementById('dynoResultBox').style.display = 'block';
                    document.getElementById('dynoStageTitle').innerText = data.stage_name;
                    document.getElementById('dynoHpChange').innerText = data.stock_hp + ' -> ' + data.tuned_hp + ' HP (+' + data.hp_gain + ')';
                    document.getElementById('dynoTqChange').innerText = data.stock_torque_nm + ' -> ' + data.tuned_torque_nm + ' Nm (+' + data.torque_gain + ')';
                    document.getElementById('dynoSpeed').innerText = data.top_speed_gain;
                    document.getElementById('dynoThump').innerText = data.thump_profile;
                    document.getElementById('dynoDb').innerText = data.exhaust_decibel + ' dB';
                    const badge = document.getElementById('dynoRtoBadge');
                    if (data.rto_legal) {{
                        badge.className = 'badge bg-success small';
                        badge.innerText = 'RTO Legal (<85 dB)';
                    }} else {{
                        badge.className = 'badge bg-danger small';
                        badge.innerText = 'Exceeds RTO Limit';
                    }}
                }}
            }} catch (err) {{
                console.error("Dyno error:", err);
            }}
        }}

        function quickVintageSymptom(txt) {{
            document.getElementById('vintageQueryInput').value = txt;
            diagnoseVintageBullet();
        }}

        async function diagnoseVintageBullet() {{
            const q = document.getElementById('vintageQueryInput').value.trim();
            if (!q) return;

            try {{
                const res = await fetch('/api/restomod/vintage-ci-diagnose', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ symptom_query: q }})
                }});
                const data = await res.json();
                if (res.ok) {{
                    document.getElementById('vintageResultBox').style.display = 'block';
                    document.getElementById('vintageFaultTitle').innerText = data.fault_name + ' (' + data.fault_name_gu + ')';
                    document.getElementById('vintageRootCause').innerText = data.root_cause;
                    document.getElementById('vintageTolerance').innerText = data.factory_tolerance_specs;
                    document.getElementById('vintageActionGu').innerText = data.mechanic_directive_gu;
                    document.getElementById('vintageActionEn').innerText = data.mechanic_directive_en;
                }}
            }} catch (err) {{
                console.error("Vintage CI diagnose error:", err);
            }}
        }}

        function printRestomodBlueprint() {{
            if (currentRestoBlueprint && currentRestoBlueprint.resto_id) {{
                window.open('/restomod/' + currentRestoBlueprint.resto_id, '_blank');
            }}
        }}

        function copyRestomodWhatsApp() {{
            if (!currentRestoBlueprint) return;
            const b = currentRestoBlueprint;
            const text = "*CHAMUNDA AUTOMOBILES - CUSTOM RESTO-MOD SPECIFICATION* 🏍️\n" +
                "*Blueprint ID:* " + b.resto_id + "\n" +
                "*Rider:* " + b.customer_name + " (" + b.registration_no + ")\n" +
                "*Model Platform:* " + b.bike_model + "\n" +
                "*Style:* " + b.style_name + "\n" +
                "*Custom Paint:* " + b.paint_name + "\n" +
                "*Dyno Tune:* " + b.performance_stage + " (" + b.performance_specs.hp_gain + ")\n" +
                "*Turnaround Timeline:* " + b.timeline_days + " Working Days\n" +
                "*Total Build Estimate:* ₹" + b.grand_total.toLocaleString('en-IN') + "\n\n" +
                "*Verify Online Blueprint:* http://127.0.0.1:8080/restomod/" + b.resto_id + "\n" +
                "_Chamunda Royal Enfield Specialist, Ahmedabad_";

            navigator.clipboard.writeText(text).then(() => {{
                alert("Resto-Mod build specification copied to clipboard! Ready to paste into WhatsApp.");
            }}).catch(err => {{
                console.error("Clipboard error:", err);
                prompt("Copy Resto-Mod specification:", text);
            }});
        }}

        // ==========================================
        // TAB 11: 360° OMNICHANNEL SOCIAL & BRAND HUB
        // ==========================================
        let currentSocialCampaign = null;

        function setSocialTopic(t) {{
            document.getElementById('socialTopicInput').value = t;
        }}

        async function loadSocialTelemetry() {{
            try {{
                const res = await fetch('/api/social/telemetry');
                const data = await res.json();
                console.log("Social Telemetry:", data);
            }} catch (err) {{
                console.error("Failed to load telemetry:", err);
            }}
            loadSocialInbox('all');
            loadGoogleReviews();
        }}

        async function generateSocialCampaign() {{
            const topic = document.getElementById('socialTopicInput').value;
            const ctype = document.getElementById('socialTypeSelect').value;

            try {{
                const res = await fetch('/api/social/campaign/generate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ topic: topic, campaign_type: ctype }})
                }});
                const data = await res.json();
                currentSocialCampaign = data;

                const ch = data.channels_data;
                document.getElementById('prevWaText').innerText = ch.whatsapp ? ch.whatsapp.content : '';
                document.getElementById('prevIgText').innerText = ch.instagram ? (ch.instagram.caption) : '';
                document.getElementById('prevFbText').innerText = ch.facebook ? ch.facebook.content : '';
                document.getElementById('prevGbpText').innerText = ch.google_business ? ch.google_business.content : '';

                if (ch.youtube) {{
                    document.getElementById('prevYtTitle').innerText = ch.youtube.title || '';
                    document.getElementById('prevYtHook').innerText = 'Hook: ' + (ch.youtube.script_hook || '');
                    document.getElementById('prevYtDesc').innerText = ch.youtube.description || '';
                    document.getElementById('prevYtTags').innerText = 'Tags: ' + (ch.youtube.tags ? ch.youtube.tags.join(', ') : '');
                    document.getElementById('prevYtComment').innerText = 'Pinned Comment: ' + (ch.youtube.pinned_comment || '');
                }}

                const alertBox = document.getElementById('publishStatusAlert');
                alertBox.style.display = 'block';
                alertBox.className = 'mt-3 alert alert-info small py-2';
                alertBox.innerHTML = '<i class="fa-solid fa-check me-1"></i> Native copies generated for WhatsApp (+91 78747 19139), Instagram, Facebook, Google Business, and YouTube!';
            }} catch (err) {{
                console.error("Campaign generation error:", err);
                alert("Failed to generate campaign.");
            }}
        }}

        async function publishSocialCampaign() {{
            if (!currentSocialCampaign) {{
                await generateSocialCampaign();
            }}
            if (!currentSocialCampaign) return;

            try {{
                const res = await fetch('/api/social/publish', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        campaign_id: currentSocialCampaign.campaign_id,
                        topic: currentSocialCampaign.topic,
                        campaign_type: currentSocialCampaign.campaign_type,
                        channels_data: currentSocialCampaign.channels_data
                    }})
                }});
                const data = await res.json();
                const alertBox = document.getElementById('publishStatusAlert');
                alertBox.style.display = 'block';
                alertBox.className = 'mt-3 alert alert-success small py-2';
                alertBox.innerHTML = '<i class="fa-solid fa-circle-check me-1"></i> ' + data.message + ' (Post ID: ' + data.post_id + ')';
            }} catch (err) {{
                console.error("Publish error:", err);
                alert("Failed to publish campaign.");
            }}
        }}

        async function loadSocialInbox(channel) {{
            try {{
                const url = '/api/social/inbox' + (channel && channel !== 'all' ? '?channel=' + channel : '');
                const res = await fetch(url);
                const items = await res.json();
                const tbody = document.getElementById('socialInboxBody');
                if (!tbody) return;

                if (!items || items.length === 0) {{
                    tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No messages in this channel view.</td></tr>';
                    return;
                }}

                tbody.innerHTML = items.map(item => {{
                    let badgeClass = 'bg-secondary';
                    let icon = 'fa-solid fa-message';
                    if (item.channel === 'whatsapp') {{ badgeClass = 'bg-success'; icon = 'fa-brands fa-whatsapp'; }}
                    else if (item.channel === 'instagram') {{ badgeClass = 'bg-danger'; icon = 'fa-brands fa-instagram'; }}
                    else if (item.channel === 'facebook') {{ badgeClass = 'bg-primary'; icon = 'fa-brands fa-facebook'; }}
                    else if (item.channel === 'youtube') {{ badgeClass = 'bg-danger'; icon = 'fa-brands fa-youtube'; }}

                    return '<tr>' +
                        '<td><span class="badge ' + badgeClass + '"><i class="' + icon + ' me-1"></i>' + item.channel.toUpperCase() + '</span></td>' +
                        '<td><strong>' + item.sender_name + '</strong><br><small class="text-muted">' + item.sender_contact + '</small></td>' +
                        '<td><div class="small text-light">' + item.message + '</div>' +
                        (item.ai_draft_reply ? '<div class="small text-warning mt-1"><em>AI Draft: ' + item.ai_draft_reply.substring(0, 75) + '...</em></div>' : '') +
                        '</td>' +
                        '<td><span class="badge ' + (item.reply_sent ? 'bg-success' : 'bg-warning text-dark') + '">' + item.status + '</span></td>' +
                        '<td><button class="btn btn-sm btn-outline-warning" onclick="sendInboxReply(\'' + item.item_id + '\')"><i class="fa-solid fa-reply me-1"></i> Reply</button></td>' +
                        '</tr>';
                }}).join('');
            }} catch (err) {{
                console.error("Inbox load error:", err);
            }}
        }}

        async function sendInboxReply(itemId) {{
            const reply = prompt("Enter AI response to send to customer:", "નમસ્તે! ચામુંડા ઓટોમોબાઇલ પાર્ટ્સ એન્ડ સર્વિસમાં આપનું સ્વાગત છે. વધુ વિગત માટે WhatsApp: +91 78747 19139 પર સંપર્ક કરો.");
            if (!reply) return;

            try {{
                const res = await fetch('/api/social/inbox/reply', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ item_id: itemId, reply_text: reply }})
                }});
                const data = await res.json();
                if (data.success) {{
                    alert(data.message);
                    loadSocialInbox('all');
                }}
            }} catch (err) {{
                console.error("Reply dispatch error:", err);
            }}
        }}

        async function loadGoogleReviews() {{
            try {{
                const res = await fetch('/api/social/reviews');
                const reviews = await res.json();
                const container = document.getElementById('googleReviewsContainer');
                if (!container) return;

                if (!reviews || reviews.length === 0) {{
                    container.innerHTML = '<p class="text-muted small">No reviews loaded.</p>';
                    return;
                }}

                container.innerHTML = reviews.map(r => {{
                    return '<div class="p-3 bg-dark rounded border border-secondary mb-3">' +
                        '<div class="d-flex justify-content-between align-items-center mb-1">' +
                        '<strong class="text-warning">' + r.customer_name + '</strong>' +
                        '<span class="text-warning">' + '★'.repeat(r.rating) + '</span>' +
                        '</div>' +
                        '<p class="small text-light mb-2">"' + r.comment + '"</p>' +
                        (r.owner_reply ? '<div class="p-2 bg-black rounded border border-warning small text-muted mb-2"><strong class="text-warning">Owner Response:</strong><br>' + r.owner_reply + '</div>' : '') +
                        '<div class="d-flex justify-content-between align-items-center">' +
                        '<small class="text-muted">' + r.time_ago + ' • ' + r.status + '</small>' +
                        '<button class="btn btn-sm btn-outline-warning py-0 px-2" onclick="sendGoogleReviewReply(\'' + r.review_id + '\')"><i class="fa-solid fa-pen-to-square me-1"></i> Edit Reply</button>' +
                        '</div>' +
                        '</div>';
                }}).join('');
            }} catch (err) {{
                console.error("Reviews load error:", err);
            }}
        }}

        async function sendGoogleReviewReply(reviewId) {{
            const reply = prompt("Enter official Google Business Profile owner reply:", "Thank you for trusting Chamunda Automobile! We take pride in delivering the authentic Royal Enfield thump and 100% genuine spares. - Alpesh Sir & Team");
            if (!reply) return;

            try {{
                const res = await fetch('/api/social/reviews/reply', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ review_id: reviewId, reply_text: reply }})
                }});
                const data = await res.json();
                if (data.success) {{
                    alert(data.message);
                    loadGoogleReviews();
                }}
            }} catch (err) {{
                console.error("Review reply error:", err);
            }}
        }}

        // Auto load social data on initial render
        document.addEventListener('DOMContentLoaded', () => {{
            setTimeout(() => {{
                loadSocialInbox('all');
                loadGoogleReviews();
            }}, 1000);
        }});

        // ==========================================
        // TAB 12: EXECUTIVE TEAM & SHOP SUB-AGENTS
        // ==========================================
        async function loadSubagentsOverview() {{
            try {{
                const res = await fetch('/api/agents/history');
                const history = await res.json();
                const tbody = document.getElementById('delegationLogBody');
                if (tbody && history && history.length > 0) {{
                    tbody.innerHTML = history.map(d => {{
                        return '<tr>' +
                            '<td><code>' + d.delegation_id + '</code></td>' +
                            '<td><strong class="text-warning">' + d.agent_name + '</strong></td>' +
                            '<td><strong>' + d.task_title + '</strong><br><small class="text-muted">' + (d.task_description || '').substring(0, 80) + '...</small></td>' +
                            '<td><span class="badge bg-success">' + d.status + '</span></td>' +
                            '<td><small class="text-muted">' + d.delegated_at + '</small></td>' +
                            '<td><small class="text-light">' + (d.result_summary || 'Executed') + '</small></td>' +
                            '</tr>';
                    }}).join('');
                }}
            }} catch (err) {{
                console.error("Subagent overview error:", err);
            }}
        }}

        function setWrittenCommand(text, priority) {{
            document.getElementById('writtenCommandText').value = text;
            if (priority) {{
                document.getElementById('writtenCommandPriority').value = priority;
            }}
            document.getElementById('writtenCommandText').focus();
        }}

        async function submitWrittenCommand() {{
            const cmd = document.getElementById('writtenCommandText').value.trim();
            if (!cmd) {{
                alert("Please enter a written command.");
                return;
            }}

            const sender = document.getElementById('writtenCommandSender').value;
            const priority = document.getElementById('writtenCommandPriority').value;
            const btn = document.getElementById('btnExecuteWrittenCommand');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Processing...';

            try {{
                const res = await fetch('/api/agents/command', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        command: cmd,
                        sender: sender,
                        priority: priority
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const box = document.getElementById('writtenCommandResultBox');
                    box.style.display = 'block';
                    document.getElementById('wcrTargetBadge').textContent = data.target_agent.toUpperCase() + ' (' + data.priority + ')';
                    document.getElementById('wcrHeadTitle').textContent = data.designated_head;
                    document.getElementById('wcrGuText').innerHTML = '<i class="fa-solid fa-check-circle me-1"></i> ' + data.response_gu;
                    document.getElementById('wcrEnText').textContent = data.response_en;

                    document.getElementById('writtenCommandText').value = '';
                    loadSubagentsOverview();
                }} else {{
                    alert("Error: " + (data.error || "Failed to execute directive"));
                }}
            }} catch (err) {{
                console.error("Written command error:", err);
                alert("Failed to submit written command.");
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane me-1"></i> Execute Directive<br><small class="fw-normal">આદેશ આપો</small>';
            }}
        }}

        function openDelegateModal(agentId, agentName) {{
            document.getElementById('modalAgentId').value = agentId;
            document.getElementById('modalAgentName').value = agentName;
            
            // Suggest default task title based on agent
            let defaultTitle = "Execute Department Routine Check";
            let defaultDesc = "Verify operational standards and report status to CEO Aradhya.";
            if (agentId === 'bay_chief') {{
                defaultTitle = "Perform 50-Point Acoustic Audit & Tappet Check";
                defaultDesc = "Inspect Classic 350 engine sound, measure exhaust dB (<85 dB limit), and prepare Health Passport.";
            }} else if (agentId === 'parts_specialist') {{
                defaultTitle = "Audit Low-Stock Spares & Generate Purchase Order";
                defaultDesc = "Scan inventory for filters, gaskets, and Motul 15W-50 oil below reorder threshold.";
            }} else if (agentId === 'customer_receptionist') {{
                defaultTitle = "Broadcast Service Reminders on WhatsApp";
                defaultDesc = "Send upcoming maintenance reminders via official WhatsApp bot (+91 78747 19139).";
            }} else if (agentId === 'social_growth_manager') {{
                defaultTitle = "Syndicate Thump Tuning Reel & Google Review Reply";
                defaultDesc = "Publish workshop video to YouTube Shorts & Instagram, and auto-reply to new 5-star reviews.";
            }} else if (agentId === 'accounts_controller') {{
                defaultTitle = "Reconcile Daily Counter Cash & UPI Payments";
                defaultDesc = "Verify GST invoice totals and counter POS transactions against bank settlement.";
            }}

            document.getElementById('modalTaskTitle').value = defaultTitle;
            document.getElementById('modalTaskDesc').value = defaultDesc;
            document.getElementById('modalDelegationAlert').style.display = 'none';

            const modal = new bootstrap.Modal(document.getElementById('delegateModal'));
            modal.show();
        }}

        async function submitTaskDelegation() {{
            const agentId = document.getElementById('modalAgentId').value;
            const title = document.getElementById('modalTaskTitle').value;
            const desc = document.getElementById('modalTaskDesc').value;

            try {{
                const res = await fetch('/api/agents/delegate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        agent_id: agentId,
                        task_title: title,
                        task_description: desc
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const alertBox = document.getElementById('modalDelegationAlert');
                    alertBox.style.display = 'block';
                    alertBox.className = 'alert alert-success small py-2';
                    alertBox.innerHTML = '<i class="fa-solid fa-check-double me-1"></i> Directive dispatched to ' + data.designated_head + '! ID: ' + data.delegation_id;
                    setTimeout(() => {{
                        bootstrap.Modal.getInstance(document.getElementById('delegateModal')).hide();
                        loadSubagentsOverview();
                    }}, 1500);
                }}
            }} catch (err) {{
                console.error("Task delegation error:", err);
                alert("Failed to delegate task.");
            }}
        }}

        async function loadAgentGrowthMatrix() {{
            try {{
                const res = await fetch('/api/agents/growth');
                const growthData = await res.json();
                const container = document.getElementById('subagentGrowthGrid');
                if (!container) return;

                const profiles = Object.values(growthData);
                container.innerHTML = profiles.map(p => {{
                    const xpPct = Math.min(100, Math.round((p.xp / (p.xp_to_next_level || 700)) * 100));
                    const skills = (p.learned_capabilities || []).slice(0, 2).map(s => '<span class="badge bg-secondary me-1 mb-1 small">' + s + '</span>').join('');
                    return '<div class="col-md-4 col-sm-6">' +
                        '<div class="p-3 bg-dark rounded border border-secondary h-100">' +
                            '<div class="d-flex justify-content-between align-items-start mb-2">' +
                                '<div>' +
                                    '<strong class="text-white d-block">' + p.agent_name + '</strong>' +
                                    '<small class="text-warning">' + p.designated_head + '</small>' +
                                '</div>' +
                                '<span class="badge bg-warning text-dark fw-bold">Level ' + p.level + '</span>' +
                            '</div>' +
                            '<div class="d-flex justify-content-between small text-muted mb-1">' +
                                '<span>XP: ' + p.xp + ' / ' + (p.xp_to_next_level || 700) + '</span>' +
                                '<span>' + xpPct + '%</span>' +
                            '</div>' +
                            '<div class="progress mb-2" style="height: 6px;">' +
                                '<div class="progress-bar bg-success progress-bar-striped progress-bar-animated" style="width: ' + xpPct + '%;"></div>' +
                            '</div>' +
                            '<div class="d-flex justify-content-between small text-muted mb-2">' +
                                '<span><i class="fa-solid fa-shield-halved text-success me-1"></i> ' + p.issues_resolved_autonomously + ' Healed</span>' +
                                '<span class="text-success fw-bold">' + (p.autonomous_healing_rate || '99.4%') + ' Fix Rate</span>' +
                            '</div>' +
                            '<div class="border-top border-secondary pt-2 mt-2">' +
                                '<small class="text-muted d-block mb-1">Learned Capabilities:</small>' +
                                '<div>' + (skills || '<span class="text-muted small">Standard baseline</span>') + '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';
                }}).join('');
            }} catch (err) {{
                console.error("Growth load error:", err);
            }}
        }}

        async function triggerIncidentSimulation(agentId, incidentType) {{
            const btn = document.getElementById('btnTriggerHeal');
            if (btn) {{
                btn.disabled = true;
                btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Diagnosing & Healing...';
            }}
            try {{
                const res = await fetch('/api/agents/simulate-incident', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ agent_id: agentId, incident_type: incidentType }})
                }});
                const data = await res.json();
                if (data.success) {{
                    displayHealResult(data);
                    loadAgentGrowthMatrix();
                    loadSubagentsOverview();
                }} else {{
                    alert("Heal error: " + (data.error || "Failed to self-heal incident"));
                }}
            }} catch (err) {{
                console.error("Simulate incident error:", err);
            }} finally {{
                if (btn) {{
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fa-solid fa-wrench me-1"></i> Auto-Heal &amp; Grow';
                }}
            }}
        }}

        async function submitCustomHeal() {{
            const agentId = document.getElementById('healSelectAgent').value;
            const issue = document.getElementById('healIssueText').value.trim();
            if (!issue) {{
                alert("Please describe the issue or defect to diagnose.");
                return;
            }}
            const btn = document.getElementById('btnTriggerHeal');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Diagnosing & Healing...';
            try {{
                const res = await fetch('/api/agents/heal', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ agent_id: agentId, issue: issue }})
                }});
                const data = await res.json();
                if (data.success) {{
                    displayHealResult(data);
                    document.getElementById('healIssueText').value = '';
                    loadAgentGrowthMatrix();
                    loadSubagentsOverview();
                }} else {{
                    alert("Heal error: " + (data.error || "Failed to self-heal incident"));
                }}
            }} catch (err) {{
                console.error("Custom heal error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-wrench me-1"></i> Auto-Heal &amp; Grow';
            }}
        }}

        function displayHealResult(data) {{
            const card = document.getElementById('healResultCard');
            card.style.display = 'block';
            document.getElementById('healAgentBadge').textContent = data.agent_name + ' • Level ' + data.new_level;
            document.getElementById('healXpBadge').textContent = '+' + data.xp_awarded + ' XP (Total: ' + data.total_xp + ' XP)';
            document.getElementById('healTitle').textContent = data.designated_head + ' Neutralized Incident: ' + data.incident_id;
            document.getElementById('healRootCause').textContent = data.root_cause_diagnosed;
            document.getElementById('healAppliedFix').innerHTML = '<i class="fa-solid fa-check-double me-1 text-success"></i> <strong>Fix Applied:</strong> ' + data.applied_solution;
            document.getElementById('healSkillUnlocked').textContent = data.new_skill_unlocked;
            document.getElementById('healGuText').innerHTML = '<strong>ગુજરાતી સારાંશ:</strong> ' + data.solution_gu;
        }}

        // --- Project Trinetra JS: 3D Schematics, Borescope & Multi-Branch Hub ---
        let currentSchematicData = null;

        async function loadSchematicAssembly(assemblyId) {{
            const buttons = ['btnAsmJ350', 'btnAsm650', 'btnAsmCI', 'btnAsmSherpa'];
            buttons.forEach(b => {{
                const el = document.getElementById(b);
                if (el) el.classList.remove('active');
            }});
            if (assemblyId === 'ASM-J350-HEAD' && document.getElementById('btnAsmJ350')) document.getElementById('btnAsmJ350').classList.add('active');
            if (assemblyId === 'ASM-650-CLUTCH' && document.getElementById('btnAsm650')) document.getElementById('btnAsm650').classList.add('active');
            if (assemblyId === 'ASM-CI350-CRANK' && document.getElementById('btnAsmCI')) document.getElementById('btnAsmCI').classList.add('active');
            if (assemblyId === 'ASM-SHERPA-COOLING' && document.getElementById('btnAsmSherpa')) document.getElementById('btnAsmSherpa').classList.add('active');

            try {{
                const res = await fetch('/api/schematics/assembly/' + assemblyId);
                const data = await res.json();
                if (!data || !data.assembly_id) return;
                currentSchematicData = data;

                document.getElementById('schematicPlatformTitle').textContent = data.platform.split('(')[0].trim();
                document.getElementById('schematicComponentCount').textContent = data.components.length + ' Critical Items';
                document.getElementById('schematicTopTorque').textContent = (data.components[0] ? data.components[0].torque_nm : 'Factory Spec');
                document.getElementById('schematicStockStatus').textContent = (data.components[0] ? data.components[0].stock + ' Pcs (' + data.components[0].bin + ')' : 'In Stock');
                document.getElementById('schematicDisplayTitle').innerHTML = '<i class="' + data.icon + ' me-2"></i>' + data.title;
                document.getElementById('schematicDisplaySub').textContent = data.title_gu + ' • ' + data.platform;
                document.getElementById('schematicIdBadge').textContent = data.assembly_id;

                // Visual Callouts
                const calloutsContainer = document.getElementById('schematicVisualCallouts');
                let calloutsHtml = '';
                data.components.forEach((c, idx) => {{
                    calloutsHtml += `
                    <div class="p-3 bg-dark rounded border border-warning text-center" style="min-width: 170px; max-width: 220px; box-shadow: 0 0 10px rgba(255,193,7,0.15);">
                        <span class="badge bg-warning text-dark fw-bold mb-2">#${{c.item_no}} OEM ${{c.part_number}}</span>
                        <div class="small fw-bold text-light mb-1">${{c.name}}</div>
                        <div class="badge bg-black border border-warning text-warning small mb-1">${{c.torque_nm}}</div>
                        <div class="text-muted" style="font-size: 0.75rem;"><i class="fa-solid fa-boxes-stacked me-1"></i>${{c.bin}} (${{c.stock}} pcs)</div>
                    </div>`;
                }});
                calloutsContainer.innerHTML = calloutsHtml;

                // Key Specs
                const specsContainer = document.getElementById('schematicSpecsContainer');
                let specsHtml = '';
                for (const [k, v] of Object.entries(data.key_specifications || {{}})) {{
                    const label = k.replace(/_/g, ' ').toUpperCase();
                    specsHtml += `
                    <div class="col-md-3">
                        <div class="p-2 bg-black rounded border border-secondary">
                            <small class="text-muted d-block" style="font-size: 0.7rem;">${{label}}</small>
                            <span class="small fw-bold text-light">${{v}}</span>
                        </div>
                    </div>`;
                }}
                specsContainer.innerHTML = specsHtml;

                // Table
                const tbody = document.getElementById('schematicComponentsTableBody');
                let rowsHtml = '';
                data.components.forEach(c => {{
                    rowsHtml += `
                    <tr>
                        <td><span class="badge bg-warning text-dark fw-bold">#${{c.item_no}}</span></td>
                        <td><code class="text-warning fw-bold">${{c.part_number}}</code></td>
                        <td><strong>${{c.name}}</strong><br><small class="text-muted">${{c.name_gu || ''}}</small></td>
                        <td><span class="badge bg-secondary">${{c.category}}</span></td>
                        <td><strong>${{c.stock}} pcs</strong><br><small class="text-info"><i class="fa-solid fa-location-dot me-1"></i>${{c.bin}}</small></td>
                        <td><span class="badge bg-dark border border-warning text-warning fw-bold fs-6">${{c.torque_nm}}</span></td>
                        <td><small class="text-light"><i class="fa-solid fa-user-gear me-1 text-warning"></i>${{c.master_tech_advice}}</small></td>
                    </tr>`;
                }});
                tbody.innerHTML = rowsHtml;
            }} catch (err) {{
                console.error("Error loading schematic:", err);
            }}
        }}

        async function runBorescopeInspection() {{
            const btn = document.getElementById('btnRunBorescope');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Capturing Optical Endoscopy...';

            const payload = {{
                bike_model: document.getElementById('boreBikeModel').value,
                registration_no: document.getElementById('boreRegNo').value.trim() || 'GJ-02-BQ-1234',
                odometer_km: parseInt(document.getElementById('boreOdoKm').value) || 15000,
                scenario: document.getElementById('boreScenario').value
            }};

            try {{
                const res = await fetch('/api/borescope/inspect', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                const data = await res.json();
                if (data && data.inspection_id) {{
                    document.getElementById('borescopeResultCard').style.display = 'block';
                    document.getElementById('borescopeScoreCard').textContent = data.combustion_health_score + ' / 100';
                    document.getElementById('borescopeGradeBadge').textContent = data.chamber_grade;
                    document.getElementById('borescopeCarbonCard').textContent = data.piston_crown.carbon_crust_thickness_mm + ' mm Layer';
                    document.getElementById('borescopeHoneCard').textContent = data.cylinder_wall.honing_crosshatch_retention_pct + '% Retention';
                    document.getElementById('borescopeCostCard').textContent = '₹' + data.cost_estimate_inr.toLocaleString();

                    document.getElementById('boreResTitle').innerHTML = '<i class="fa-solid fa-clipboard-check me-2"></i>' + data.inspection_id + ' • ' + data.bike_model + ' (' + data.registration_no + ')';
                    document.getElementById('boreResMeta').textContent = data.timestamp + ' • ' + data.odometer_km.toLocaleString() + ' KM • Score: ' + data.combustion_health_score + '/100';
                    document.getElementById('boreResGradeBadge').textContent = data.chamber_grade;

                    document.getElementById('boreResCarbonThickness').textContent = data.piston_crown.carbon_crust_thickness_mm + ' mm Thickness';
                    document.getElementById('boreResCarbonDensity').textContent = data.piston_crown.carbon_density + ' (' + data.piston_crown.status + ')';
                    const carbPct = Math.min(100, Math.round((data.piston_crown.carbon_crust_thickness_mm / 1.5) * 100));
                    document.getElementById('boreResCarbonProgress').style.width = carbPct + '%';

                    document.getElementById('boreResHonePct').textContent = data.cylinder_wall.honing_crosshatch_retention_pct + '% Crosshatch Intact';
                    document.getElementById('boreResGlaze').textContent = data.cylinder_wall.thrust_face_glazing + (data.cylinder_wall.micro_scratch_detected ? ' [SCORING DETECTED]' : '');
                    document.getElementById('boreResHoneProgress').style.width = data.cylinder_wall.honing_crosshatch_retention_pct + '%';

                    document.getElementById('boreResIntakeValve').textContent = 'Intake: ' + data.valve_seals.intake_valve_carbon_deposit;
                    document.getElementById('boreResExhaustValve').textContent = 'Exhaust: ' + data.valve_seals.exhaust_valve_carbon_deposit;
                    document.getElementById('boreResValveStatus').textContent = 'Status: ' + data.valve_seals.status;

                    document.getElementById('boreResCost').textContent = 'Estimate: ₹' + data.cost_estimate_inr.toLocaleString();
                    document.getElementById('boreResTreatment').textContent = data.prescribed_treatment;
                    document.getElementById('boreResVerdictGu').textContent = data.master_tech_verdict_gu;
                    document.getElementById('boreResVerdictEn').textContent = data.master_tech_verdict_en;

                    loadBorescopeHistory();
                }}
            }} catch (err) {{
                console.error("Borescope scan error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-video me-2"></i> Run Borescope Optical Scan';
            }}
        }}

        async function loadBorescopeHistory() {{
            try {{
                const res = await fetch('/api/borescope/inspections');
                const list = await res.json();
                const tbody = document.getElementById('borescopeHistoryTableBody');
                if (!list || list.length === 0) {{
                    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-3">No borescope inspections recorded yet.</td></tr>';
                    return;
                }}
                let rowsHtml = '';
                list.slice(0, 10).forEach(item => {{
                    rowsHtml += `
                    <tr>
                        <td><strong>${{item.inspection_id}}</strong></td>
                        <td><small class="text-muted">${{item.timestamp}}</small></td>
                        <td>${{item.bike_model}}</td>
                        <td><code class="text-warning">${{item.registration_no}}</code></td>
                        <td>${{item.odometer_km.toLocaleString()}} KM</td>
                        <td><span class="badge bg-dark border border-danger text-danger fs-6">${{item.combustion_health_score}}/100</span></td>
                        <td><span class="badge bg-danger">${{item.chamber_grade.split('(')[0]}}</span></td>
                        <td><small class="text-warning">${{item.piston_crown.carbon_crust_thickness_mm}} mm</small></td>
                    </tr>`;
                }});
                tbody.innerHTML = rowsHtml;
            }} catch (err) {{
                console.error("Error loading borescope history:", err);
            }}
        }}

        async function loadMultiBranchOverview() {{
            try {{
                const res = await fetch('/api/branches/overview');
                const data = await res.json();
                if (!data || !data.branches) return;

                document.getElementById('mbNetworkRevenue').textContent = '₹' + data.total_revenue_today_inr.toLocaleString();
                document.getElementById('mbActiveBays').textContent = data.total_active_bays + ' Bays Active';
                document.getElementById('mbTodayJobs').textContent = data.total_jobs_today + ' Motorcycles';
                document.getElementById('mbInventoryValuation').textContent = '₹' + data.total_inventory_valuation_inr.toLocaleString();

                // Branch Cards Grid
                const grid = document.getElementById('mbBranchesGrid');
                let cardsHtml = '';
                data.branches.forEach(b => {{
                    cardsHtml += `
                    <div class="col-md-4">
                        <div class="card card-custom p-3 border-${{b.color_badge || 'info'}} h-100">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="badge bg-${{b.color_badge || 'info'}} text-light fw-bold">${{b.branch_id}}</span>
                                <span class="badge bg-success"><i class="fa-solid fa-circle-dot me-1"></i>${{b.status}}</span>
                            </div>
                            <h6 class="text-light fw-bold mb-1">${{b.name}}</h6>
                            <small class="text-muted d-block mb-2">${{b.name_gu || ''}}</small>
                            <div class="small text-muted mb-2"><i class="fa-solid fa-location-dot me-1 text-warning"></i>${{b.address}}</div>
                            <div class="small text-light mb-1"><i class="fa-solid fa-user-tie me-1 text-info"></i><strong>${{b.manager}}</strong> (${{b.phone}})</div>
                            <hr class="border-secondary my-2">
                            <div class="d-flex justify-content-between text-muted small">
                                <span>Bays: <strong class="text-light">${{b.active_bays}}</strong></span>
                                <span>Jobs Today: <strong class="text-warning">${{b.today_jobs}}</strong></span>
                                <span>Valuation: <strong class="text-success">₹${{(b.stock_valuation_inr || 0).toLocaleString()}}</strong></span>
                            </div>
                        </div>
                    </div>`;
                }});
                grid.innerHTML = cardsHtml;

                // Transfers Table
                const tbody = document.getElementById('mbTransfersTableBody');
                if (!data.recent_transfers || data.recent_transfers.length === 0) {{
                    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-3">No transfers logged yet.</td></tr>';
                    return;
                }}
                let tRows = '';
                data.recent_transfers.forEach(t => {{
                    tRows += `
                    <tr>
                        <td><strong>${{t.transfer_id}}</strong></td>
                        <td><small class="text-muted">${{t.timestamp}}</small></td>
                        <td><span class="badge bg-dark border text-light">${{t.from_branch}}</span> ➔ <span class="badge bg-dark border text-warning">${{t.to_branch}}</span></td>
                        <td><code>${{t.part_number}}</code><br><small class="text-muted">${{t.part_name || ''}}</small></td>
                        <td><strong>${{t.quantity}} pcs</strong></td>
                        <td>₹${{t.total_value_inr.toLocaleString()}}</td>
                        <td><span class="badge bg-${{t.status === 'Delivered' ? 'success' : 'warning text-dark'}}">${{t.status}}</span></td>
                        <td><small class="text-light">${{t.requested_by}}</small></td>
                    </tr>`;
                }});
                tbody.innerHTML = tRows;
            }} catch (err) {{
                console.error("Error loading branch overview:", err);
            }}
        }}

        async function submitBranchTransfer() {{
            const btn = document.getElementById('btnDispatchTransfer');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Routing Transfer...';

            const payload = {{
                from_branch: document.getElementById('mbFromBranch').value,
                to_branch: document.getElementById('mbToBranch').value,
                part_number: document.getElementById('mbPartNumber').value.trim() || '574012/A',
                quantity: parseInt(document.getElementById('mbQuantity').value) || 1,
                requested_by: document.getElementById('mbRequestedBy').value.trim() || 'Branch Lead',
                notes: document.getElementById('mbTransferNotes').value.trim()
            }};

            try {{
                const res = await fetch('/api/branches/transfer-stock', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});
                const data = await res.json();
                const alertEl = document.getElementById('mbTransferAlert');
                alertEl.style.display = 'block';
                if (data.success) {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-success text-success';
                    alertEl.innerHTML = '<i class="fa-solid fa-circle-check me-2"></i>' + data.message + '<br><small class="text-muted">' + (data.message_gu || '') + '</small><br><small class="text-info"><i class="fa-brands fa-whatsapp me-1"></i>Waybill alert dispatched via <strong>+91 78747 19139</strong>.</small>';
                    loadMultiBranchOverview();
                loadWebARAssemblies();
                loadNightLockerStatus();
                }} else {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-danger text-danger';
                    alertEl.textContent = 'Transfer Error: ' + (data.error || 'Failed to dispatch transfer');
                }}
            }} catch (err) {{
                console.error("Branch transfer error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane me-2"></i> Dispatch Stock Transfer';
            }}
        }}

        async function submitGlobalOmniCommand() {{
            const input = document.getElementById('globalOmniCommandInput');
            const cmd = input.value.trim();
            if (!cmd) return;
            const priority = document.getElementById('globalOmniPriority').value;
            const btn = document.getElementById('btnGlobalOmniSubmit');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Executing...';

            try {{
                const res = await fetch('/api/agents/command', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        command: cmd,
                        sender: 'Alpesh Sir (Founder, Chairman & Master Tech)',
                        priority: priority
                    }})
                }});
                const data = await res.json();
                const box = document.getElementById('globalOmniResultBox');
                box.style.display = 'block';
                if (data.success) {{
                    document.getElementById('globalOmniResultTitle').innerHTML = '<i class="fa-solid fa-circle-check text-success me-1"></i> Directive ' + data.command_id + ' Successfully Executed';
                    document.getElementById('globalOmniResultAgent').textContent = (data.designated_head || 'Agent') + ' (' + (data.assigned_department || '') + ')';
                    document.getElementById('globalOmniResultSummary').textContent = data.result_summary;
                    document.getElementById('globalOmniResultGu').innerHTML = '<strong>ગુજરાતી પુષ્ટિ:</strong> ' + data.response_gu;
                    input.value = '';
                }} else {{
                    document.getElementById('globalOmniResultTitle').innerHTML = '<i class="fa-solid fa-triangle-exclamation text-danger me-1"></i> Execution Failed';
                    document.getElementById('globalOmniResultAgent').textContent = 'Error';
                    document.getElementById('globalOmniResultSummary').textContent = data.error || 'Failed to parse directive';
                    document.getElementById('globalOmniResultGu').textContent = '';
                }}
            }} catch (err) {{
                console.error("Omni-command error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane me-1"></i> Execute';
            }}
        }}

        function setAndRunGlobalCommand(cmdText, priority) {{
            document.getElementById('globalOmniCommandInput').value = cmdText;
            document.getElementById('globalOmniPriority').value = priority;
            submitGlobalOmniCommand();
        }}

        async function triggerTurboBoost() {{
            const box = document.getElementById('globalOmniResultBox');
            box.style.display = 'block';
            document.getElementById('globalOmniResultTitle').innerHTML = '<i class="fa-solid fa-spinner fa-spin text-warning me-1"></i> Running Turbo Boost Optimization...';
            document.getElementById('globalOmniResultAgent').textContent = 'System Optimizer';
            document.getElementById('globalOmniResultSummary').textContent = 'Pruning zombie tasks, trimming memory via malloc_trim, and purging caches...';
            document.getElementById('globalOmniResultGu').textContent = 'કૃપા કરીને રાહ જુઓ, લેપટોપને ઝડપી બનાવવામાં આવી રહ્યું છે...';

            try {{
                const res = await fetch('/api/system/optimize', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ mode: 'safe' }})
                }});
                const data = await res.json();
                if (data.success) {{
                    document.getElementById('globalOmniResultTitle').innerHTML = '<i class="fa-solid fa-circle-check text-success me-1"></i> 🚀 Turbo Boost Optimization Complete!';
                    document.getElementById('globalOmniResultAgent').textContent = 'Freed ' + data.freed_memory_mb + ' MB RAM';
                    document.getElementById('globalOmniResultSummary').textContent = data.message_en;
                    document.getElementById('globalOmniResultGu').innerHTML = '<strong>ગુજરાતી અહેવાલ:</strong> ' + data.message_gu;
                }} else {{
                    document.getElementById('globalOmniResultTitle').innerHTML = '<i class="fa-solid fa-circle-exclamation text-danger me-1"></i> Optimization Warning';
                    document.getElementById('globalOmniResultSummary').textContent = data.error || 'Optimization finished with notes.';
                }}
            }} catch (err) {{
                console.error("Turbo boost error:", err);
                document.getElementById('globalOmniResultSummary').textContent = 'Turbo Boost network error: ' + err.message;
            }}
        }}


        // =========================================================================
        // PROJECT DIVYA-DRISHTI: WEBAR CAMERA ENGINE GUIDE
        // =========================================================================
        let currentWebARData = null;

        async function loadWebARAssemblies() {{
            try {{
                const res = await fetch('/api/webar/assemblies');
                const assemblies = await res.json();
                if (assemblies && assemblies.length > 0) {{
                    document.getElementById('arTotalEnginesCount').textContent = assemblies.length + ' Platforms';
                    const selectEl = document.getElementById('webarAssemblySelect');
                    selectEl.innerHTML = '';
                    assemblies.forEach(asm => {{
                        const opt = document.createElement('option');
                        opt.value = asm.assembly_id;
                        opt.textContent = asm.title + ' (' + asm.platform + ')';
                        selectEl.appendChild(opt);
                    }});
                    selectWebARAssembly(assemblies[0].assembly_id);
                }}
            }} catch (err) {{
                console.error("Failed to load WebAR assemblies:", err);
            }}
        }}

        async function selectWebARAssembly(asmId) {{
            try {{
                const res = await fetch('/api/webar/overlay/' + encodeURIComponent(asmId));
                const data = await res.json();
                if (data.success) {{
                    currentWebARData = data;
                    renderWebAROverlay(data);
                }}
            }} catch (err) {{
                console.error("Failed to fetch WebAR overlay for " + asmId, err);
            }}
        }}

        function renderWebAROverlay(data) {{
            document.getElementById('arActiveEngineBadge').textContent = data.platform;
            document.getElementById('arResolutionBadge').textContent = data.camera_resolution;
            document.getElementById('arAssemblyTitleDisplay').textContent = data.title;
            document.getElementById('arAssemblyMethodology').textContent = data.methodology;
            document.getElementById('arRameshAdvisoryText').innerHTML = '<i class="fa-solid fa-user-ninja me-1"></i> <strong>માસ્ટર ટેક રમેશ:</strong> ' + data.ramesh_advisory;

            // Render SVG criss-cross guide line
            const svgEl = document.getElementById('arSvgOverlay');
            if (data.svg_guide_path) {{
                svgEl.innerHTML = '<path d="' + data.svg_guide_path + '" fill="none" stroke="#f39c12" stroke-width="3" stroke-dasharray="6,6" opacity="0.8"/>';
            }} else {{
                svgEl.innerHTML = '';
            }}

            // Render AR interactive markers
            const markersLayer = document.getElementById('arMarkersLayer');
            markersLayer.innerHTML = '';
            const tableBody = document.getElementById('arSequenceTableBody');
            tableBody.innerHTML = '';

            data.markers.forEach(m => {{
                // Overlay Pin
                const pin = document.createElement('div');
                pin.className = 'position-absolute d-flex flex-column align-items-center justify-content-center cursor-pointer';
                pin.style.left = (m.pos_x_pct) + '%';
                pin.style.top = (m.pos_y_pct) + '%';
                pin.style.transform = 'translate(-50%, -50%)';
                pin.style.zIndex = '5';
                pin.style.cursor = 'pointer';
                pin.onclick = () => showMarkerDetails(m);

                pin.innerHTML = '<div class="badge rounded-pill shadow-lg border border-light" style="background-color: ' + (m.color || '#e74c3c') + '; width: 34px; height: 34px; line-height: 26px; font-weight: bold; font-size: 14px;">' + m.sequence_step + '</div>' +
                                '<span class="badge bg-dark bg-opacity-75 border border-secondary text-warning mt-1 px-1" style="font-size: 10px;">' + m.torque_nm + ' Nm</span>';
                markersLayer.appendChild(pin);

                // Table Row
                const tr = document.createElement('tr');
                tr.className = 'cursor-pointer';
                tr.onclick = () => showMarkerDetails(m);
                tr.innerHTML = '<td><span class="badge" style="background-color:' + (m.color || '#e74c3c') + '">' + m.sequence_step + '</span></td>' +
                               '<td><strong>' + m.label + '</strong><br><small class="text-muted">' + (m.label_gu || '') + '</small></td>' +
                               '<td><span class="text-warning fw-bold">' + m.torque_nm + ' Nm</span><br><small class="text-muted">±' + m.torque_tolerance_nm + ' Nm</small></td>' +
                               '<td><span class="text-info">' + m.tool_spec + '</span><br><small class="text-muted">' + m.threadlocker + '</small></td>' +
                               '<td><span class="badge ' + (m.warehouse_stock > 3 ? 'bg-success' : 'bg-danger') + '">' + m.warehouse_stock + ' in stock</span><br><small class="text-light">₹' + m.unit_mrp + '</small></td>';
                tableBody.appendChild(tr);
            }});

            if (data.markers.length > 0) {{
                showMarkerDetails(data.markers[0]);
            }}
        }}

        function showMarkerDetails(marker) {{
            const card = document.getElementById('arSelectedMarkerContent');
            card.innerHTML = '<div class="d-flex justify-content-between align-items-center mb-2">' +
                '<span class="badge bg-warning text-dark fs-6">Step ' + marker.sequence_step + ': ' + marker.label + '</span>' +
                '<span class="badge bg-dark border border-secondary text-info">' + marker.part_number + '</span>' +
                '</div>' +
                '<p class="text-light mb-1"><strong>ગુજરાતી નામ:</strong> ' + (marker.label_gu || marker.label) + '</p>' +
                '<div class="row g-2 mb-2">' +
                '<div class="col-6"><span class="text-muted">Target Torque:</span> <strong class="text-warning">' + marker.torque_nm + ' Nm (±' + marker.torque_tolerance_nm + ')</strong></div>' +
                '<div class="col-6"><span class="text-muted">Required Tool:</span> <strong class="text-info">' + marker.tool_spec + '</strong></div>' +
                '<div class="col-6"><span class="text-muted">Threadlocker:</span> <strong class="text-light">' + marker.threadlocker + '</strong></div>' +
                '<div class="col-6"><span class="text-muted">Warehouse Bin:</span> <strong class="text-success">' + (marker.bin_location || 'Bin A-04') + ' (' + marker.warehouse_stock + ' pcs)</strong></div>' +
                '</div>' +
                '<div class="p-2 bg-dark rounded border border-warning text-warning small">' +
                '<i class="fa-solid fa-lightbulb me-1"></i> <strong>માસ્ટર રમેશ ટિપ:</strong> ' + (marker.ramesh_tip || 'હંમેશા નિર્ધારિત ટોર્ક પ્રમાણે જ સ્પેનર વાપરો.') +
                '</div>';
        }}

        function startWebARCamera() {{
            const stage = document.getElementById('arCameraStage');
            stage.style.background = 'radial-gradient(circle, #2c3e50 0%, #1a1a2e 100%)';
            const msg = document.getElementById('arPlaceholderMessage');
            msg.innerHTML = '<i class="fa-solid fa-satellite-dish text-success fs-1 mb-3 fa-beat"></i>' +
                            '<h6 class="text-light">Optical AR Camera Overlay Active</h6>' +
                            '<p class="text-success small mb-0">60 FPS Hardware-Accelerated Tracking &bull; Aligned to Royal Enfield Cylinder Head</p>';
        }}

        function dispatchArSpecToWhatsApp() {{
            if (!currentWebARData) return;
            const text = encodeURIComponent("દિવ્ય-દ્રષ્ટિ એન્જિન ટોર્ક ગાઈડ: " + currentWebARData.title + " (" + currentWebARData.platform + "). સહાયતા: +91 78747 19139.");
            window.open('https://api.whatsapp.com/send?phone=917874719139&text=' + text, '_blank');
        }}

        // =========================================================================
        // PROJECT NIGHT-GUARDIAN: 24/7 HIGHWAY EMERGENCY SPARES LOCKER
        // =========================================================================
        async function loadNightLockerStatus() {{
            try {{
                const res = await fetch('/api/locker/status');
                const data = await res.json();

                document.getElementById('nlkAvailableCount').textContent = data.available_compartments_count + ' / ' + data.total_compartments + ' Ready';
                document.getElementById('nlkTotalRevenue').textContent = '₹' + data.total_night_revenue_inr.toLocaleString();
                document.getElementById('nlkTotalTxns').textContent = data.total_night_transactions + ' Cashless Transactions';
                if (data.telemetry) {{
                    document.getElementById('nlkTelemetryStatus').textContent = data.telemetry.system_status + ' • Temp: ' + data.telemetry.ambient_temp_c + '°C • UPS: ' + data.telemetry.backup_battery_pct + '%';
                }}

                // Render Compartments Grid
                const grid = document.getElementById('nlkCompartmentsGrid');
                grid.innerHTML = '';
                (data.compartments || []).forEach(comp => {{
                    const isAvail = comp.status === 'Available' && comp.units_inside > 0;
                    const borderCls = isAvail ? 'border-success' : 'border-danger opacity-75';
                    const badgeCls = isAvail ? 'bg-success' : 'bg-danger';

                    const col = document.createElement('div');
                    col.className = 'col-md-6';
                    col.innerHTML = '<div class="card card-custom p-3 ' + borderCls + ' h-100">' +
                                    '<div class="d-flex justify-content-between align-items-center mb-2">' +
                                    '<span class="badge bg-dark border border-secondary text-info fw-bold">' + comp.box_id + '</span>' +
                                    '<span class="badge ' + badgeCls + '">' + comp.status + ' (' + comp.units_inside + '/' + comp.max_capacity + ')</span>' +
                                    '</div>' +
                                    '<h6 class="text-light mb-1">' + comp.item_name + '</h6>' +
                                    '<small class="text-warning d-block mb-1">' + comp.item_name_gu + '</small>' +
                                    '<small class="text-muted d-block mb-2">OEM SKU: <code>' + comp.part_number + '</code> | ' + comp.compatible_bikes + '</small>' +
                                    '<div class="d-flex justify-content-between align-items-center mt-auto">' +
                                    '<span class="fs-5 text-success fw-bold">₹' + comp.price_inr + '</span>' +
                                    '<button class="btn btn-sm btn-outline-warning" ' + (!isAvail ? 'disabled' : '') + ' onclick="selectLockerForReserve(\'' + comp.box_id + '\')">' +
                                    '<i class="fa-solid fa-cart-shopping me-1"></i> Reserve Bay</button>' +
                                    '</div>' +
                                    '</div>';
                    grid.appendChild(col);
                }});

                // Render Ledger
                const ledgerBody = document.getElementById('nlkLedgerTableBody');
                ledgerBody.innerHTML = '';
                if (!data.recent_transactions || data.recent_transactions.length === 0) {{
                    ledgerBody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-3">No midnight dispenser sales recorded yet. All lockers securely armed.</td></tr>';
                }} else {{
                    data.recent_transactions.forEach(t => {{
                        const tr = document.createElement('tr');
                        tr.innerHTML = '<td><strong>' + t.transaction_id + '</strong><br><small class="text-muted">' + t.reservation_id + '</small></td>' +
                                       '<td><span class="badge bg-dark border border-info text-info">' + t.box_id + '</span></td>' +
                                       '<td>' + t.item_name + '<br><small class="text-muted"><code>' + t.part_number + '</code></small></td>' +
                                       '<td><strong>' + t.customer_name + '</strong><br><small class="text-warning">' + t.vehicle_reg + '</small></td>' +
                                       '<td><span class="text-success fw-bold">₹' + t.amount_paid + '</span><br><small class="text-muted">' + t.payment_ref + '</small></td>' +
                                       '<td><small class="text-muted">' + t.timestamp + '</small></td>' +
                                       '<td><span class="badge bg-success"><i class="fa-solid fa-check me-1"></i> ' + t.solenoid_status + '</span></td>';
                        ledgerBody.appendChild(tr);
                    }});
                }}
            }} catch (err) {{
                console.error("Failed to load night locker status:", err);
            }}
        }}

        function selectLockerForReserve(boxId) {{
            document.getElementById('nlkReserveBoxSelect').value = boxId;
            document.getElementById('btnReserveLocker').scrollIntoView({{ behavior: 'smooth' }});
        }}

        async function submitLockerReservation() {{
            const boxId = document.getElementById('nlkReserveBoxSelect').value;
            const phone = document.getElementById('nlkReservePhone').value.trim();
            const name = document.getElementById('nlkReserveName').value.trim();
            const reg = document.getElementById('nlkReserveReg').value.trim();
            const btn = document.getElementById('btnReserveLocker');
            const alertEl = document.getElementById('nlkReserveResultAlert');

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Generating UPI QR & OTP...';
            alertEl.style.display = 'none';

            try {{
                const res = await fetch('/api/locker/reserve', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        box_id: boxId,
                        customer_name: name,
                        phone: phone,
                        vehicle_reg: reg
                    }})
                }});
                const data = await res.json();
                alertEl.style.display = 'block';
                if (data.success) {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-success text-light';
                    alertEl.innerHTML = '<h6 class="text-success mb-2"><i class="fa-solid fa-circle-check me-2"></i>Emergency Bay Reserved!</h6>' +
                                        '<div class="mb-2"><strong>Reservation ID:</strong> <code>' + data.reservation_id + '</code> | <strong>Bay:</strong> ' + data.box_id + '</div>' +
                                        '<div class="mb-2"><strong>Item:</strong> ' + data.item_name + ' (' + data.item_name_gu + ') - <span class="text-warning fw-bold">₹' + data.amount_payable + '</span></div>' +
                                        '<div class="p-2 bg-black rounded border border-warning mb-2 text-center">' +
                                        '<div class="small text-muted mb-1">Your 6-Digit Locker Solenoid OTP (Valid 15 Mins):</div>' +
                                        '<div class="fs-2 text-warning fw-bold letter-spacing-2">' + data.otp_code + '</div>' +
                                        '</div>' +
                                        '<div class="small text-info mb-2"><i class="fa-solid fa-qrcode me-1"></i> UPI Payload: <code>' + data.upi_payload + '</code></div>' +
                                        '<div class="small text-muted"><i class="fa-brands fa-whatsapp me-1 text-success"></i> Helpline: <strong>+91 78747 19139</strong></div>';

                    // Auto populate unlock fields
                    document.getElementById('nlkUnlockResId').value = data.reservation_id;
                    document.getElementById('nlkUnlockOtp').value = data.otp_code;
                    loadNightLockerStatus();
                }} else {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-danger text-danger';
                    alertEl.textContent = 'Reservation Error: ' + (data.error || 'Failed to reserve bay');
                }}
            }} catch (err) {{
                console.error("Locker reservation error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-qrcode me-2"></i> Reserve Bay &amp; Generate Dynamic UPI QR';
            }}
        }}

        async function submitLockerUnlock() {{
            const resId = document.getElementById('nlkUnlockResId').value.trim();
            const otp = document.getElementById('nlkUnlockOtp').value.trim();
            const paymentRef = document.getElementById('nlkUnlockPaymentRef').value.trim();
            const btn = document.getElementById('btnUnlockLocker');
            const alertEl = document.getElementById('nlkUnlockResultAlert');

            if (!resId || !otp) {{
                alert("Please enter both Reservation ID and 6-Digit OTP.");
                return;
            }}

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Firing Solenoid Relay...';
            alertEl.style.display = 'none';

            try {{
                const res = await fetch('/api/locker/unlock', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        reservation_id: resId,
                        otp_code: otp,
                        payment_ref: paymentRef
                    }})
                }});
                const data = await res.json();
                alertEl.style.display = 'block';
                if (data.success) {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-success text-light';
                    alertEl.innerHTML = '<h6 class="text-success mb-2"><i class="fa-solid fa-unlock me-2"></i>DOOR OPENED! Solenoid Relay Fired</h6>' +
                                        '<div class="mb-1 text-light"><strong>Locker ' + data.box_id + ' Unlocked:</strong> ' + data.item_name + '</div>' +
                                        '<div class="small text-muted mb-2">Txn ID: ' + data.transaction_id + ' | Pulse: ' + data.solenoid_pulse + '</div>' +
                                        '<div class="p-2 bg-success bg-opacity-25 border border-success rounded text-success small">' +
                                        '<i class="fa-solid fa-circle-check me-1"></i> ' + data.message_gu +
                                        '</div>';
                    loadNightLockerStatus();
                }} else {{
                    alertEl.className = 'mt-3 p-3 bg-dark rounded border border-danger text-danger';
                    alertEl.textContent = 'Unlock Error: ' + (data.error || 'Failed to unlock locker');
                }}
            }} catch (err) {{
                console.error("Locker unlock error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-key me-2"></i> Trigger 500ms Solenoid Relay Unlock';
            }}
        }}


        // =========================================================================
        // PROJECT CHHAYA: CLOUD SHADOW MIRRORING & OFFLINE AGENT ACCESS
        // =========================================================================
        async function loadCloudShadowStatus() {{
            try {{
                const res = await fetch('/api/cloud-shadow/status');
                const data = await res.json();

                document.getElementById('cshClusterName').textContent = data.cluster_name;
                document.getElementById('cshClusterRegion').textContent = data.cloud_region;
                document.getElementById('cshSystemMode').textContent = data.system_mode;
                document.getElementById('cshLastHeartbeat').textContent = 'Heartbeat: ' + data.last_heartbeat;
                if (data.snapshot_data) {{
                    document.getElementById('cshMirroredSkus').textContent = (data.snapshot_data.total_parts_skus || 4469).toLocaleString() + ' SKUs';
                    document.getElementById('cshMirroredValuation').textContent = '₹' + (data.snapshot_data.inventory_valuation_inr || 5775000).toLocaleString() + ' Spares Valuation';
                }}
                document.getElementById('cshQueuedEvents').textContent = data.queued_mutations_count;

                // Render Replicas Grid
                const grid = document.getElementById('cshReplicasGrid');
                grid.innerHTML = '';
                const replicas = data.cloud_replicas || {{}};
                for (const [key, r] of Object.entries(replicas)) {{
                    const col = document.createElement('div');
                    col.className = 'col-md-6';
                    col.innerHTML = '<div class="card card-custom p-3 border-secondary h-100">' +
                                    '<div class="d-flex justify-content-between align-items-center mb-1">' +
                                    '<strong class="text-light">' + r.name + '</strong>' +
                                    '<span class="badge bg-success">' + r.status + '</span>' +
                                    '</div>' +
                                    '<small class="text-warning d-block mb-1">' + r.role + '</small>' +
                                    '<small class="text-muted d-block">' + r.capabilities + '</small>' +
                                    '</div>';
                    grid.appendChild(col);
                }}

                // Render Sync History
                const histBody = document.getElementById('cshSyncHistoryTableBody');
                histBody.innerHTML = '';
                const history = data.sync_history || [];
                if (history.length === 0) {{
                    histBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted py-3">No sync transactions recorded yet.</td></tr>';
                }} else {{
                    history.forEach(h => {{
                        const tr = document.createElement('tr');
                        tr.innerHTML = '<td><code>' + h.sync_id + '</code></td>' +
                                       '<td>' + h.timestamp + '</td>' +
                                       '<td><span class="badge bg-info">' + h.mutations_applied + ' events</span></td>' +
                                       '<td><span class="badge bg-success">' + h.status + '</span></td>' +
                                       '<td><small class="text-light">' + (h.message_gu || 'Sync Complete') + '</small></td>';
                        histBody.appendChild(tr);
                    }});
                }}
            }} catch (err) {{
                console.error("Failed to load cloud shadow status:", err);
            }}
        }}

        async function triggerCloudShadowSync() {{
            try {{
                const res = await fetch('/api/cloud-shadow/sync', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ mode: 'full' }})
                }});
                const data = await res.json();
                if (data.success) {{
                    alert("☁️ Cloud Shadow Snapshot Synced Successfully!\nTimestamp: " + data.timestamp);
                    loadCloudShadowStatus();
                }}
            }} catch (err) {{
                console.error("Failed to sync cloud shadow:", err);
            }}
        }}

        function setOfflineQueryPreset(text) {{
            document.getElementById('cshSimQueryInput').value = text;
        }}

        async function submitOfflineSimulationQuery() {{
            const query = document.getElementById('cshSimQueryInput').value.trim();
            if (!query) return;

            const sender = document.getElementById('cshSimSender').value.trim();
            const btn = document.getElementById('btnRunOfflineSim');
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-2"></i> Querying Cloud Shadow Replica...';

            try {{
                const res = await fetch('/api/cloud-shadow/query', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        query: query,
                        sender: sender,
                        phone: '+91 78747 19139'
                    }})
                }});
                const data = await res.json();
                const box = document.getElementById('cshSimResultBox');
                box.style.display = 'block';

                document.getElementById('cshSimAgentBadge').textContent = data.responding_agent + ' (' + data.assigned_role + ')';
                document.getElementById('cshSimEnvBadge').textContent = data.execution_environment;
                document.getElementById('cshSimEn').innerHTML = '<strong>English:</strong> ' + data.response_en;
                document.getElementById('cshSimGu').innerHTML = '<strong>ગુજરાતી:</strong> ' + data.response_gu;
                loadCloudShadowStatus();
            }} catch (err) {{
                console.error("Offline query simulation error:", err);
            }} finally {{
                btn.disabled = false;
                btn.innerHTML = '<i class="fa-solid fa-paper-plane me-2"></i> Query Cloud Shadow Replica';
            }}
        }}

        async function reconcileCloudShadow() {{
            try {{
                const res = await fetch('/api/cloud-shadow/reconcile', {{ method: 'POST' }});
                const data = await res.json();
                alert(data.message_gu || data.message_en);
                loadCloudShadowStatus();
            }} catch (err) {{
                console.error("Reconcile error:", err);
            }}
        }}

        // =========================================================================
        // PROJECT KALPAVRIKSHA: AUTONOMOUS VIRTUAL GROWTH & MASTERY
        // =========================================================================
        async function loadKalpavrikshaStatus() {{
            try {{
                const res = await fetch('/api/kalpavriksha/status');
                const data = await res.json();

                document.getElementById('kvFleetIQ').textContent = data.fleet_overall_iq || 184;
                document.getElementById('kvTotalXP').textContent = (data.total_fleet_xp || 0).toLocaleString() + ' XP';
                document.getElementById('kvSimsCount').textContent = data.total_simulations_executed || 0;
                document.getElementById('kvSpecsCount').textContent = (data.knowledge_specs_count || 0) + ' Specs';

                // Render Agents Grid
                const grid = document.getElementById('kvAgentsGrid');
                grid.innerHTML = '';
                const agents = data.agents || {{}};
                for (const [key, a] of Object.entries(agents)) {{
                    const col = document.createElement('div');
                    col.className = 'col-md-4';
                    const skillsList = (a.unlocked_skills || []).map(s => `<li>${{s}}</li>`).join('');
                    col.innerHTML = `
                        <div class="card card-custom p-3 border-secondary h-100">
                            <div class="d-flex justify-content-between align-items-center mb-1">
                                <strong class="text-light">${{a.agent_name}}</strong>
                                <span class="badge bg-warning text-dark fw-bold">Level ${{a.level}}</span>
                            </div>
                            <small class="text-info d-block mb-2">${{a.department}} • <em>${{a.rank}}</em></small>
                            <div class="progress mb-2" style="height: 6px; background-color: #222;">
                                <div class="progress-bar bg-warning" role="progressbar" style="width: ${{(a.total_xp % 1000) / 10}}%"></div>
                            </div>
                            <div class="d-flex justify-content-between small text-muted mb-2">
                                <span>${{a.total_xp.toLocaleString()}} Total XP</span>
                                <span>${{a.simulations_passed || 0}} Sims Passed</span>
                            </div>
                            <div class="small">
                                <span class="text-warning fw-bold">Unlocked Capabilities:</span>
                                <ul class="text-muted ps-3 mb-0" style="font-size: 0.8rem;">
                                    ${{skillsList}}
                                </ul>
                            </div>
                        </div>
                    `;
                    grid.appendChild(col);
                }}

                // Render Recent Sims
                const simTable = document.getElementById('kvRecentSimsTableBody');
                simTable.innerHTML = '';
                const recent = data.recent_simulations || [];
                if (recent.length === 0) {{
                    simTable.innerHTML = '<tr><td colspan="6" class="text-center text-muted py-3">No simulation logs yet. Click \'Run 1-Click Synthetic Simulation\' to start practicing!</td></tr>';
                }} else {{
                    recent.slice().reverse().forEach(s => {{
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td><small class="text-muted">${{s.timestamp}}</small></td>
                            <td><code>${{s.sim_id}}</code></td>
                            <td><strong class="text-light">${{s.bike_model}}</strong></td>
                            <td><span class="badge bg-dark border border-secondary text-warning">${{s.responding_agent}}</span></td>
                            <td><span class="badge bg-success">+${{s.xp_awarded}} XP</span></td>
                            <td class="small"><span class="text-info">${{s.diagnosis}}</span><br><span class="text-muted">${{s.solution_gu}}</span></td>
                        `;
                        simTable.appendChild(tr);
                    }});
                }}

                // Render Indexed Specs
                const specsTable = document.getElementById('kvSpecsTableBody');
                if (specsTable) {{
                    specsTable.innerHTML = '';
                    const specs = data.technical_specs || [];
                    if (specs.length === 0) {{
                        specsTable.innerHTML = '<tr><td colspan="4" class="text-center text-muted py-2">No specs indexed yet.</td></tr>';
                    }} else {{
                        specs.forEach(sp => {{
                            const tr = document.createElement('tr');
                            tr.innerHTML = `
                                <td><code>${{sp.spec_id}}</code></td>
                                <td><strong class="text-light">${{sp.engine_family}}</strong></td>
                                <td><span class="badge bg-dark border border-secondary text-info">${{sp.category}}</span></td>
                                <td class="small">
                                    <span class="text-warning">${{sp.torque_sequence}}</span><br>
                                    <small class="text-muted"><em>Ramesh Note:</em> ${{sp.ramesh_secret || '--'}}</small>
                                </td>
                            `;
                            specsTable.appendChild(tr);
                        }});
                    }}
                }}
            }} catch (err) {{
                console.error("Failed to load Kalpavriksha status:", err);
            }}
        }}

        async function triggerKalpavrikshaSimulation() {{
            try {{
                const res = await fetch('/api/kalpavriksha/simulate', {{ method: 'POST' }});
                const data = await res.json();
                if (data.success) {{
                    document.getElementById('kvSimResultCard').style.display = 'block';
                    document.getElementById('kvResultTitle').textContent = `Simulation Completed: ${{data.simulation_id}}`;
                    document.getElementById('kvResultXP').textContent = `+${{data.xp_awarded}} XP Awarded (${{data.responding_agent}} -> Level ${{data.agent_current_level}})`;
                    document.getElementById('kvResultBike').textContent = data.bike_model;
                    document.getElementById('kvResultSymptom').textContent = data.symptom;
                    document.getElementById('kvResultAgent').textContent = data.responding_agent;
                    document.getElementById('kvResultDiagnosis').textContent = data.diagnosis;
                    document.getElementById('kvResultPrescription').textContent = data.solution_prescribed;
                    document.getElementById('kvResultGujarati').textContent = data.solution_gu;

                    // Reload telemetry
                    loadKalpavrikshaStatus();
                loadDMSOverview();
                }} else {{
                    alert("Simulation failed: " + (data.error || "Unknown error"));
                }}
            }} catch (err) {{
                alert("Network error executing simulation: " + err);
            }}
        }}

        async function triggerKalpavrikshaSurge() {{
            try {{
                const res = await fetch('/api/kalpavriksha/surge', {{ method: 'POST' }});
                const data = await res.json();
                if (data.success) {{
                    alert(data.message_gu || data.message);
                    loadKalpavrikshaStatus();
                }} else {{
                    alert("Surge error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error triggering surge: " + err);
            }}
        }}

        async function ingestKalpavrikshaSpec() {{
            const family = document.getElementById('kvIngestFamily').value.trim();
            const category = document.getElementById('kvIngestCategory').value.trim();
            const components = document.getElementById('kvIngestComponents').value.trim();
            const torque = document.getElementById('kvIngestTorque').value.trim();
            const clearances = document.getElementById('kvIngestClearances').value.trim();
            const secret = document.getElementById('kvIngestSecret').value.trim();

            if (!family || !category || !torque) {{
                alert("Please fill in at least Engine Family, Category, and Torque Sequence.");
                return;
            }}

            try {{
                const res = await fetch('/api/kalpavriksha/ingest-spec', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        engine_family: family,
                        category: category,
                        target_components: components,
                        torque_sequence: torque,
                        clearances: clearances,
                        ramesh_secret: secret
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    alert("Specification successfully indexed into local disk memory!");
                    document.getElementById('kvIngestFamily').value = '';
                    document.getElementById('kvIngestCategory').value = '';
                    document.getElementById('kvIngestComponents').value = '';
                    document.getElementById('kvIngestTorque').value = '';
                    document.getElementById('kvIngestClearances').value = '';
                    document.getElementById('kvIngestSecret').value = '';
                    loadKalpavrikshaStatus();
                }} else {{
                    alert("Ingestion error: " + (data.error || "Unknown error"));
                }}
            }} catch (err) {{
                alert("Error ingesting spec: " + err);
            }}
        }}

        // =========================================================================
        // RE-DMS SUITE JAVASCRIPT HANDLERS (FULL 360-DEGREE DEALERSHIP SUITE)
        // =========================================================================
        async function loadDMSOverview() {{
            try {{
                const res = await fetch('/api/dms/overview');
                const data = await res.json();
                if (!data.success) return;

                const o = data.overview;
                document.getElementById('dmsTotalInvoices').innerText = o.total_invoices_generated || 0;
                document.getElementById('dmsTotalClaims').innerText = o.total_warranty_claims || 0;
                document.getElementById('dmsActiveCampaigns').innerText = o.active_campaigns_count || 0;
                document.getElementById('dmsActiveLeads').innerText = o.active_leads_count || 0;

                // Accounting summary
                if (o.accounting_summary) {{
                    const acc = o.accounting_summary;
                    const pnl = acc.pnl_summary || {{}};
                    document.getElementById('dmsGrossRevenue').innerText = '₹' + Math.round(Number(pnl.total_revenue || 0)).toLocaleString();
                    document.getElementById('dmsNetCash').innerText = '₹' + Math.round(Number(acc.net_cash_inflow || 0)).toLocaleString();
                    document.getElementById('dmsReceivables').innerText = '₹' + Math.round(Number(acc.total_ar_outstanding || 0)).toLocaleString();
                    if (document.getElementById('dmsARSum')) {{
                        document.getElementById('dmsARSum').innerText = '₹' + Math.round(Number(acc.total_ar_outstanding || 0)).toLocaleString();
                    }}
                    if (document.getElementById('dmsAPSum')) {{
                        document.getElementById('dmsAPSum').innerText = '₹' + Math.round(Number(acc.total_ap_due || 0)).toLocaleString();
                    }}

                    // Populate Daybook Table
                    const dbTbody = document.getElementById('dmsDaybookTableBody');
                    if (dbTbody && acc.daybook_entries) {{
                        dbTbody.innerHTML = acc.daybook_entries.map(e => `
                            <tr>
                                <td class="text-muted small">${{e.timestamp || '-'}}</td>
                                <td><span class="badge ${{e.type === 'CREDIT' ? 'bg-success' : 'bg-danger'}}">${{e.type}}</span></td>
                                <td><strong class="text-light">${{e.ledger}}</strong></td>
                                <td class="fw-bold ${{e.type === 'CREDIT' ? 'text-success' : 'text-danger'}}">₹${{Number(e.amount).toLocaleString()}}</td>
                            </tr>
                        `).join('');
                    }}
                }}

                // Showroom summary
                if (o.showroom_summary) {{
                    const sh = o.showroom_summary;
                    document.getElementById('dmsTotalBookings').innerText = sh.total_bookings_count || 0;
                    document.getElementById('dmsTotalAdvance').innerText = '₹' + Math.round(Number(sh.total_booking_advance_inr || 0)).toLocaleString();
                }}

                // CSAT summary
                if (o.csat_summary) {{
                    const cs = o.csat_summary;
                    document.getElementById('dmsCSATScore').innerText = (cs.dealership_csat_percentage || 100).toFixed(1) + '%';
                    document.getElementById('dmsAvgRating').innerText = (cs.average_rating_out_of_5 || 5.0).toFixed(1) + ' ⭐';
                }}

                // Populate Leads Table
                const leadsTbody = document.getElementById('dmsLeadsTableBody');
                if (leadsTbody && o.leads) {{
                    leadsTbody.innerHTML = o.leads.map(l => `
                        <tr>
                            <td><strong class="text-light">${{l.customer_name}}</strong><br><small class="text-muted">${{l.phone}}</small></td>
                            <td class="text-warning">${{l.interest}}</td>
                            <td><small class="text-muted">${{l.source}}</small></td>
                            <td><span class="badge bg-primary">${{l.status}}</span></td>
                        </tr>
                    `).join('');
                }}

                // Populate 10-Member Fleet Roster
                const rosterRow = document.getElementById('dmsFleetRosterRow');
                if (rosterRow && data.fleet) {{
                    rosterRow.innerHTML = data.fleet.map(sa => `
                        <div class="col-md-2 col-6 mb-2">
                            <div class="p-2 bg-dark rounded border border-secondary h-100 shadow-sm">
                                <div class="d-flex justify-content-between align-items-center mb-1">
                                    <strong class="text-warning" style="font-size: 0.75rem;">${{sa.designated_head || sa.name}}</strong>
                                    <span class="badge bg-secondary" style="font-size: 0.6rem;">${{sa.agent_id}}</span>
                                </div>
                                <small class="text-light d-block fw-bold" style="font-size: 0.72rem;">${{sa.name}}</small>
                                <small class="text-muted d-block" style="font-size: 0.68rem;">${{sa.department || sa.role || 'Officer'}}</small>
                                <div class="mt-1">
                                    <span class="badge bg-dark border border-success text-success" style="font-size: 0.6rem;">● Active 24/7</span>
                                </div>
                            </div>
                        </div>
                    `).join('');
                }}
            }} catch (err) {{
                console.error("Error loading DMS overview:", err);
            }}
        }}

        async function createDMSInvoice() {{
            const name = document.getElementById('dmsCustName').value.trim() || 'Valued RE Customer';
            const phone = document.getElementById('dmsCustPhone').value.trim() || '+91 98250 12345';
            const model = document.getElementById('dmsBikeModel').value;
            const reg = document.getElementById('dmsRegNo').value.trim() || 'GJ-02-RE-2026';
            const parts = parseFloat(document.getElementById('dmsPartsSubtotal').value) || 1935.0;
            const labor = parseFloat(document.getElementById('dmsLaborSubtotal').value) || 900.0;
            const mode = document.getElementById('dmsPaymentMode').value;

            try {{
                const res = await fetch('/api/dms/invoice', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        customer_name: name,
                        phone: phone,
                        bike_model: model,
                        registration_no: reg,
                        parts_items: [{{ part_no: 'RE-OEM-PART', name: 'Genuine RE Spares (HSN 8714)', hsn: '8714', qty: 1, rate: parts, amount: parts }}],
                        labor_items: [{{ sac: '998729', description: 'Periodic Paid Service & 50-Pt Check', amount: labor }}],
                        payment_mode: mode
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const inv = data.invoice;
                    const box = document.getElementById('dmsInvoiceResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="text-warning mb-0"><i class="fa-solid fa-check-circle me-1"></i>Split-GST Tax Invoice Generated</h6>
                            <span class="badge bg-warning text-dark fw-bold">${{inv.invoice_no}}</span>
                        </div>
                        <div class="row g-2 mb-2 small">
                            <div class="col-6">Customer: <strong>${{inv.customer_name}}</strong></div>
                            <div class="col-6 text-end">Reg: <strong>${{inv.registration_no}}</strong></div>
                            <div class="col-6">Spares HSN 8714: <strong>₹${{inv.parts_subtotal}}</strong></div>
                            <div class="col-6 text-end">Labor SAC 998729: <strong>₹${{inv.labor_subtotal}}</strong></div>
                            <div class="col-6">CGST (9%) + SGST (9%): <strong>₹${{inv.cgst_amount + inv.sgst_amount}}</strong></div>
                            <div class="col-6 text-end text-success fw-bold">Total: ₹${{inv.grand_total}}</div>
                        </div>
                        <div class="p-2 bg-dark rounded border border-secondary text-center mb-2">
                            <small class="text-muted d-block">GATE PASS CODE</small>
                            <span class="badge bg-success fs-6">${{inv.gate_pass_code}}</span>
                        </div>
                        <div class="text-center">
                            <img src="${{inv.qr_code_uri}}" alt="UPI QR" style="max-height: 120px;" class="rounded border border-warning mb-2">
                            <div class="small text-muted">Scan with any UPI app to settle instantly.</div>
                        </div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("Error: " + (data.error || "Failed to generate invoice"));
                }}
            }} catch (err) {{
                alert("Error creating DMS invoice: " + err);
            }}
        }}

        async function fileDMSWarrantyClaim() {{
            const coupon = document.getElementById('dmsCouponType').value;
            const chassis = document.getElementById('dmsChassisNo').value.trim() || 'ME3J350NR' + Math.floor(10000 + Math.random() * 90000);
            const engine = document.getElementById('dmsEngineNo').value.trim() || 'J350-2026-' + Math.floor(1000 + Math.random() * 9000);
            const amt = parseFloat(document.getElementById('dmsClaimAmount').value) || 1450.0;
            const defect = document.getElementById('dmsDefectDesc').value.trim() || 'Free Service Coupon & Oil Element Replacement';

            try {{
                const res = await fetch('/api/dms/warranty-claim', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        coupon_type: coupon,
                        chassis_no: chassis,
                        engine_no: engine,
                        bike_model: 'Classic 350 (Reborn)',
                        customer_name: 'Workshop Warranty Customer',
                        phone: '+91 78747 19139',
                        kilometers: 500,
                        defective_components: defect,
                        claim_amount: amt
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const clm = data.claim;
                    const box = document.getElementById('dmsClaimResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <h6 class="text-info mb-0"><i class="fa-solid fa-check-circle me-1"></i>OEM Claim Filed &amp; Credit Approved</h6>
                            <span class="badge bg-info text-dark fw-bold">${{clm.claim_id}}</span>
                        </div>
                        <div class="small text-muted mb-1">Coupon: <strong class="text-light">${{clm.coupon_type}}</strong></div>
                        <div class="small text-muted mb-1">VIN: <code>${{clm.chassis_no}}</code> | Engine: <code>${{clm.engine_no}}</code></div>
                        <div class="small text-success fw-bold mb-2">Reimbursement Credit Note: ${{clm.re_credit_note_no}} (₹${{clm.claim_amount}})</div>
                        <small class="text-muted d-block">${{data.message_gu || ''}}</small>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("Error: " + (data.error || "Failed filing claim"));
                }}
            }} catch (err) {{
                alert("Error filing claim: " + err);
            }}
        }}

        async function createDMSCampaign() {{
            const name = document.getElementById('dmsCampName').value.trim() || 'Royal Enfield Seasonal Service Utsav';
            const aud = document.getElementById('dmsCampAudience').value.trim() || 'North Gujarat Royal Enfield Riders';
            const offer = document.getElementById('dmsCampOffer').value.trim() || 'Free 50-Point Inspection & 15% Off Labor';

            try {{
                const res = await fetch('/api/dms/campaign', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        name: name,
                        target_audience: aud,
                        offer_title: offer,
                        offer_details: offer
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    alert("WhatsApp Broadcast Campaign launched successfully! (+91 78747 19139)");
                    loadDMSOverview();
                }} else {{
                    alert("Error: " + (data.error || "Failed creating campaign"));
                }}
            }} catch (err) {{
                alert("Error launching campaign: " + err);
            }}
        }}

        async function dispatchDMSServiceReminders() {{
            try {{
                const res = await fetch('/api/dms/service-reminders', {{ method: 'POST' }});
                const data = await res.json();
                if (data.success) {{
                    alert("30/60/90-day periodic service reminders dispatched via WhatsApp (+91 78747 19139) to " + data.reminders_count + " riders!");
                    loadDMSOverview();
                }} else {{
                    alert("Error: " + (data.error || "Failed sending reminders"));
                }}
            }} catch (err) {{
                alert("Error dispatching reminders: " + err);
            }}
        }}

        async function createDMSBooking() {{
            const name = document.getElementById('dmsBkCustName').value.trim() || 'Valued RE Buyer';
            const phone = document.getElementById('dmsBkCustPhone').value.trim() || '+91 98250 44556';
            const model = document.getElementById('dmsBkModel').value;
            const color = document.getElementById('dmsBkColor').value.trim() || 'Standard Edition';
            const amount = parseFloat(document.getElementById('dmsBkAmount').value) || 10000.0;
            const finance = document.getElementById('dmsBkFinance').value;
            const date = document.getElementById('dmsBkDeliveryDate').value || '2026-10-01';

            try {{
                const res = await fetch('/api/dms/booking', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        customer_name: name,
                        phone: phone,
                        bike_model: model,
                        colorway: color,
                        booking_amount: amount,
                        payment_mode: 'UPI (Instant)',
                        finance_bank: finance,
                        tentative_delivery_date: date
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const bk = data.booking;
                    const box = document.getElementById('dmsBookingResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong class="text-warning"><i class="fa-solid fa-receipt me-1"></i>Booking Confirmed: ${{bk.booking_id}}</strong>
                            <span class="badge bg-warning text-dark">${{bk.token_receipt_no}}</span>
                        </div>
                        <div class="text-light small">Customer: <strong>${{bk.customer_name}}</strong> (${{bk.phone}})</div>
                        <div class="text-muted small">Model: <span class="text-warning">${{bk.bike_model}}</span> (${{bk.colorway}})</div>
                        <div class="text-success small fw-bold">Advance Paid: ₹${{bk.booking_amount.toLocaleString()}} | Finance: ${{bk.finance_bank}}</div>
                        <div class="text-info small">Sales Officer: ${{bk.sales_manager}}</div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("Booking error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        async function generateDMSPDI() {{
            const chassis = document.getElementById('dmsPDIChassis').value.trim() || 'ME3J350NR' + Math.floor(100000 + Math.random() * 900000);
            const engine = document.getElementById('dmsPDIEngine').value.trim() || 'J350-' + Math.floor(10000 + Math.random() * 90000);
            const model = document.getElementById('dmsPDIModel').value.trim() || 'Classic 350 (Reborn)';
            const customer = document.getElementById('dmsPDICustomer').value.trim() || 'Alpesh Sir';
            const battery = parseFloat(document.getElementById('dmsPDIBattery').value) || 12.8;
            const rpm = parseInt(document.getElementById('dmsPDIRPM').value) || 1050;
            const psi = document.getElementById('dmsPDIPressure').value.trim() || 'Front: 32 / Rear: 36 PSI';
            const toolkit = document.getElementById('dmsPDIToolkit').checked;

            try {{
                const res = await fetch('/api/dms/pdi', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        chassis_no: chassis,
                        engine_no: engine,
                        bike_model: model,
                        customer_name: customer,
                        battery_voltage: battery,
                        idle_rpm: rpm,
                        tire_pressure_psi: psi,
                        toolkit_handed_over: toolkit
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const pdi = data.pdi_certificate;
                    const box = document.getElementById('dmsPDIResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong class="text-success"><i class="fa-solid fa-certificate me-1"></i>PDI Certificate: ${{pdi.pdi_id}}</strong>
                            <span class="badge bg-success">${{pdi.pdi_clearance}}</span>
                        </div>
                        <div class="text-light small">VIN: <code>${{pdi.chassis_no}}</code> | Engine: <code>${{pdi.engine_no}}</code></div>
                        <div class="text-muted small">Battery: ${{pdi.battery_voltage}}V | RPM: ${{pdi.idle_rpm}} | Tyre: ${{pdi.tire_pressure}}</div>
                        <div class="text-info small">Inspector: ${{pdi.inspector}}</div>
                        <div class="text-success small fw-bold">Status: ${{pdi.status}}</div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("PDI error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        async function issueDMSRideSure() {{
            const name = document.getElementById('dmsRSCustName').value.trim() || 'Valued RE Rider';
            const phone = document.getElementById('dmsRSCustPhone').value.trim() || '+91 78747 19139';
            const reg = document.getElementById('dmsRSReg').value.trim() || 'GJ-02-RE-2026';
            const years = parseInt(document.getElementById('dmsRSPlan').value) || 4;

            try {{
                const res = await fetch('/api/dms/ride-sure', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        customer_name: name,
                        phone: phone,
                        bike_model: 'Royal Enfield Motorcycle',
                        registration_no: reg,
                        chassis_no: 'VIN-' + Math.floor(100000 + Math.random() * 900000),
                        coverage_years: years
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const rs = data.policy;
                    const box = document.getElementById('dmsRideSureResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong class="text-warning"><i class="fa-solid fa-shield-check me-1"></i>Policy Issued: ${{rs.policy_no}}</strong>
                            <span class="badge bg-warning text-dark">${{rs.coverage_years}} Years Coverage</span>
                        </div>
                        <div class="text-light small">Customer: ${{rs.customer_name}} (${{rs.registration_no}})</div>
                        <div class="text-muted small">Plan: ${{rs.plan_type}}</div>
                        <div class="text-success small fw-bold">24/7 Roadside Helpline: ${{rs.emergency_helpline}}</div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("Ride Sure error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        async function recordDMSPSFFeedback() {{
            const inv = document.getElementById('dmsPSFInvNo').value.trim() || 'INV-RE-2026-001';
            const phone = document.getElementById('dmsPSFPhone').value.trim() || '+91 98250 12345';
            const name = document.getElementById('dmsPSFCustName').value.trim() || 'Alpesh Sir';
            const rating = parseInt(document.getElementById('dmsPSFRating').value) || 5;
            const notes = document.getElementById('dmsPSFNotes').value.trim() || 'Service carried out with exceptional precision and clean handover.';
            const resolved = document.getElementById('dmsPSFResolved').checked;

            try {{
                const res = await fetch('/api/dms/psf-feedback', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        invoice_no: inv,
                        customer_name: name,
                        phone: phone,
                        bike_model: 'Classic 350',
                        rating_1_to_5: rating,
                        feedback_notes: notes,
                        issues_resolved: resolved
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const psf = data.feedback;
                    const box = document.getElementById('dmsPSFResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong class="text-info"><i class="fa-solid fa-star me-1"></i>PSF Audited: ${{psf.psf_id}}</strong>
                            <span class="badge bg-info text-dark">${{'⭐'.repeat(psf.rating)}} (${{psf.csat_status}})</span>
                        </div>
                        <div class="text-light small">Customer: ${{psf.customer_name}} | FTR: ${{psf.issues_resolved ? '<span class="text-success">PASSED</span>' : '<span class="text-danger">RECALL</span>'}}</div>
                        <div class="text-muted small">Auditor: ${{psf.auditor}}</div>
                        <div class="text-info small">Feedback: "${{psf.feedback_notes}}"</div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("PSF error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        async function createDMSInsuranceEstimate() {{
            const co = document.getElementById('dmsInsCo').value;
            const surveyor = document.getElementById('dmsInsSurveyor').value.trim() || 'M. K. Trivedi (IRDAI Surveyor)';
            const parts = parseFloat(document.getElementById('dmsInsParts').value) || 14200.0;
            const labor = parseFloat(document.getElementById('dmsInsLabor').value) || 4800.0;

            try {{
                const res = await fetch('/api/dms/insurance-estimate', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        customer_name: 'Workshop Insurance Customer',
                        phone: '+91 78747 19139',
                        bike_model: 'Classic 350',
                        registration_no: 'GJ-02-RE-8899',
                        insurance_company: co,
                        surveyor_name: surveyor,
                        parts_estimate: parts,
                        labor_estimate: labor
                    }})
                }});
                const data = await res.json();
                if (data.success) {{
                    const est = data.insurance_estimate;
                    const box = document.getElementById('dmsInsuranceResultBox');
                    box.style.display = 'block';
                    box.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <strong class="text-info"><i class="fa-solid fa-calculator me-1"></i>Estimate: ${{est.claim_id}}</strong>
                            <span class="badge bg-info text-dark">${{est.insurance_company}}</span>
                        </div>
                        <div class="text-light small">Surveyor: ${{est.surveyor_name}}</div>
                        <div class="row g-1 small mb-1">
                            <div class="col-6">Net Parts: ₹${{est.net_parts_approved.toLocaleString()}}</div>
                            <div class="col-6 text-end">Net Labor: ₹${{est.labor_estimate.toLocaleString()}}</div>
                            <div class="col-6 text-success fw-bold">Cashless Insurer Liability: ₹${{est.net_insurer_liability.toLocaleString()}}</div>
                            <div class="col-6 text-end text-warning">Customer Share: ₹${{est.customer_payable_excess.toLocaleString()}}</div>
                        </div>
                        <div class="text-muted small">Delivery Order: <span class="badge bg-dark border border-info text-info">${{est.delivery_order_status}}</span></div>
                    `;
                    loadDMSOverview();
                }} else {{
                    alert("Insurance error: " + (data.error || "Failed"));
                }}
            }} catch (err) {{
                alert("Network error: " + err);
            }}
        }}

        // Auto load subagents & Project Trinetra on load
        document.addEventListener('DOMContentLoaded', () => {{
            setTimeout(() => {{
                loadSubagentsOverview();
                loadAgentGrowthMatrix();
                loadSchematicAssembly('ASM-J350-HEAD');
                loadBorescopeHistory();
                loadMultiBranchOverview();
                loadKalpavrikshaStatus();
                loadDMSOverview();
            }}, 1500);
        }});

    </script>
</body>
</html>
"""
    return HTMLResponse(content=html)


# --- REST API Endpoints ---
@app.post("/api/sound-diagnose")
async def api_sound_diagnose(req: SoundDiagnoseRequest):
    """Run live Fast Fourier Transform sound diagnosis or calibrated simulation."""
    sim_map = {
        "tappet": "tappet_valve_noise",
        "chain": "timing_chain_slack",
        "timing": "timing_chain_slack",
        "clutch": "clutch_primary_whine",
        "piston": "piston_slap_knock",
        "exhaust": "exhaust_leak_turbulence",
        "healthy": None
    }
    sim_key = sim_map.get(req.simulate_fault, req.simulate_fault) if req.simulate_fault else None

    rep = sound_eng.diagnose_engine_sound(
        bike_model=req.bike_model,
        record_seconds=req.record_seconds,
        inject_simulation=sim_key
    )
    return JSONResponse(content=rep)


@app.get("/api/parts/filter")
async def api_filter_parts(
    query: str = "",
    model: str = "",
    category: str = "",
    stock_status: str = "all",
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 50
):
    """Dynamic multi-parameter filter querying Chamunda's 4,469 genuine parts catalog."""
    parts = inv_mgr.filter_parts(
        query=query,
        model=model,
        category=category,
        stock_status=stock_status,
        min_price=min_price,
        max_price=max_price,
        limit=limit
    )
    return JSONResponse(content=parts)


@app.post("/api/jobcard")
async def api_create_jobcard(req: JobCardCreateRequest):
    """Intake motorcycle into service bay."""
    job = srv_mgr.create_job_card(
        customer_name=req.customer_name,
        phone=req.phone,
        bike_model=req.bike_model,
        registration_no=req.registration_no,
        odometer_km=req.odometer_km,
        customer_issues=req.customer_issues,
        service_type=req.service_type,
        mechanic_assigned=req.mechanic
    )
    return JSONResponse(content=job)


@app.post("/api/jobcard/add-part")
async def api_add_part(req: AddPartToJobRequest):
    """Allocate spare part to an open job card."""
    ok = srv_mgr.add_parts_to_job(req.job_card_id, req.part_name, req.qty, req.price)
    if ok:
        return JSONResponse(content={"success": True, "job_card_id": req.job_card_id})
    return JSONResponse(status_code=404, content={"success": False, "error": f"Job card {req.job_card_id} not found."})


@app.post("/api/jobcard/complete-and-bill")
async def api_complete_and_bill(req: CompleteJobRequest):
    """One-click completion, Digital Acoustic Health Passport creation, and QR Tax Invoice generation."""
    try:
        res = srv_mgr.complete_job_and_generate_invoice(
            job_card_id=req.job_card_id,
            technician=req.technician,
            service_notes=req.service_notes
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/passport/{passport_id}", response_class=HTMLResponse)
async def view_customer_passport(passport_id: str):
    """Dedicated mobile-friendly endpoint for customer QR code verification scanning."""
    p_file = PASSPORTS_DIR / f"{passport_id}.html"
    if p_file.exists():
        return HTMLResponse(content=p_file.read_text(encoding="utf-8"))
    
    # Try finding passport by partial ID or in database
    db_file = BASE_DIR / "data" / "health_passports.json"
    if db_file.exists():
        try:
            records = json.loads(db_file.read_text(encoding="utf-8"))
            for r in records:
                if r.get("passport_id") == passport_id and Path(r.get("html_path", "")).exists():
                    return HTMLResponse(content=Path(r["html_path"]).read_text(encoding="utf-8"))
        except Exception:
            pass

    return HTMLResponse(
        content=f"""<h2 style='color:#c5a059; font-family:sans-serif; text-align:center; margin-top:50px;'>
        🏍️ Chamunda Automobile • Passport ID [{passport_id}] Not Found</h2>
        <p style='text-align:center; font-family:sans-serif;'>Please contact Chamunda Automobile workshop support.</p>""",
        status_code=404
    )


@app.get("/invoice/{invoice_no}", response_class=HTMLResponse)
async def view_tax_invoice(invoice_no: str):
    """Official GST Tax Invoice viewer with embedded QR code."""
    inv_dir = BASE_DIR / "data" / "invoices"
    inv_file = inv_dir / f"{invoice_no}.html"
    if inv_file.exists():
        return HTMLResponse(content=inv_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>Invoice {invoice_no} not found</h2>", status_code=404)


@app.post("/api/diagnose")
async def api_diagnose_text(req: DiagnosticRequest):
    return srv_mgr.diagnose_fault(req.symptom)


@app.get("/api/crm/reminders")
async def api_get_crm_reminders():
    """Returns predictive maintenance CRM projections and categorized fleets."""
    return JSONResponse(content=crm_mgr.get_predictive_service_reminders())


@app.post("/api/crm/mark-sent")
async def api_mark_reminder_sent(req: MarkReminderSentRequest):
    """Marks that a WhatsApp service reminder was sent to the customer."""
    res = crm_mgr.mark_reminder_sent(req.registration_no)
    return JSONResponse(content=res)


@app.post("/api/po/generate")
async def api_generate_po(req: GeneratePORequest):
    """Generates an official wholesale purchase order for low-stock spare parts."""
    res = po_eng.generate_low_stock_purchase_order(supplier_name=req.supplier_name)
    return JSONResponse(content=res)


@app.get("/po/{po_number}", response_class=HTMLResponse)
async def view_purchase_order(po_number: str):
    """View official wholesale purchase order HTML."""
    po_file = PO_DIR / f"{po_number}.html"
    if po_file.exists():
        return HTMLResponse(content=po_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>Purchase Order {po_number} not found</h2>", status_code=404)


# =====================================================================
# TRINITY INNOVATIONS REST ENDPOINTS
# =====================================================================

# 1. Thump Tuner Endpoints
@app.post("/api/thump/analyze")
async def api_thump_analyze(req: ThumpAnalyzeRequest):
    """Analyze exhaust acoustic thump, calculate thump score and mechanic directives."""
    try:
        res = thump_eng.analyze_exhaust_thump(bike_model=req.bike_model, preset_key=req.preset_key)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/api/thump/presets")
async def api_thump_presets():
    """Get all configured Royal Enfield acoustic thump profiles."""
    return JSONResponse(content=THUMP_PRESETS)


# 2. Customer Bot & Job Stage Endpoints
@app.get("/api/bot/info")
async def api_bot_info():
    """Get official 24/7 WhatsApp AI Customer Bot contact info and link."""
    return JSONResponse(content=bot_eng.get_bot_contact_info())


@app.post("/api/bot/chat")
async def api_bot_chat(req: BotChatRequest):
    """Bilingual conversational agent response for customer queries."""
    try:
        res = bot_eng.process_customer_message(user_msg=req.message, phone=req.phone)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/api/bot/track/{identifier}")
async def api_bot_track(identifier: str):
    """Track motorcycle service progress and stage."""
    res = bot_eng.track_service_status(identifier)
    return JSONResponse(content=res)


@app.post("/api/bot/book")
async def api_bot_book(req: BotBookRequest):
    """Book advance service slot."""
    res = bot_eng.book_service_slot(
        customer_name=req.customer_name,
        phone=req.phone,
        bike_model=req.bike_model,
        registration_no=req.registration_no,
        preferred_date=req.preferred_date,
        customer_issues=req.customer_issues
    )
    return JSONResponse(content=res)


@app.post("/api/jobcard/update-stage")
async def api_update_jobcard_stage(req: JobCardUpdateStageRequest):
    """Update active job card service stage."""
    job_file = BASE_DIR / "data" / "job_cards.json"
    if not job_file.exists():
        return JSONResponse(status_code=404, content={"success": False, "error": "Job cards not found"})
    try:
        jobs = json.loads(job_file.read_text(encoding="utf-8"))
        for j in jobs:
            if j.get("job_card_id") == req.job_card_id:
                j["current_stage"] = req.stage_name
                job_file.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")
                return JSONResponse(content={"success": True, "job_card_id": req.job_card_id, "current_stage": req.stage_name})
        return JSONResponse(status_code=404, content={"success": False, "error": f"Job card {req.job_card_id} not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


# 3. Smart POS & Dynamic UPI QR Endpoints
@app.post("/api/pos/scan")
async def api_pos_scan(req: POSScanRequest):
    """Instant barcode or part number lookup."""
    part = pos_eng.scan_or_lookup_part(req.code_or_query)
    if part:
        return JSONResponse(content={"found": True, "part": part})
    return JSONResponse(content={"found": False, "part": None})


@app.post("/api/pos/checkout")
async def api_pos_checkout(req: POSCheckoutRequest):
    """Execute over-the-counter POS sale, deduct inventory, generate dynamic UPI QR and thermal slip."""
    try:
        res = pos_eng.create_counter_sale(
            cart_items=req.items,
            customer_name=req.customer_name,
            phone=req.phone,
            payment_mode=req.payment_mode,
            discount_amount=req.discount_amount,
            notes=req.notes
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/pos/receipt/{receipt_no}", response_class=HTMLResponse)
async def view_pos_receipt(receipt_no: str):
    """View printable 80mm POS thermal receipt."""
    slip_file = POS_RECEIPTS_DIR / f"{receipt_no}.html"
    if slip_file.exists():
        return HTMLResponse(content=slip_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>POS Receipt {receipt_no} not found</h2>", status_code=404)


@app.get("/api/pos/history")
async def api_pos_history(limit: int = 50):
    """Get recent POS sales history."""
    return JSONResponse(content=pos_eng.get_sales_history(limit=limit))


# --- Certified Pre-Owned Inspection & Valuation Endpoints ---
@app.post("/api/preowned/valuation")
async def api_preowned_valuation(req: PreOwnedValuationRequest):
    """AI algorithmic valuation for Royal Enfield pre-owned motorcycle."""
    model = req.bike_model or req.model or "Classic 350"
    year = req.manufacturing_year or req.year or 2022
    val = preowned_mgr.calculate_fair_market_valuation(
        bike_model=model,
        manufacturing_year=year,
        odometer_km=req.odometer_km,
        condition_score=req.condition_score
    )
    return JSONResponse(content=val)


@app.post("/api/preowned/inspect")
async def api_preowned_inspect(req: PreOwnedInspectionRequest):
    """Execute 100-point inspection and generate verifiable Chamunda Shield Certificate."""
    model = req.bike_model or req.model or "Classic 350"
    year = req.manufacturing_year or req.year or 2022
    try:
        report = preowned_mgr.conduct_100_point_inspection(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=model,
            registration_no=req.registration_no,
            manufacturing_year=year,
            odometer_km=req.odometer_km,
            checklist_overrides=req.checklist_overrides,
            inspector_name=req.inspector_name
        )
        return JSONResponse(content=report)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.get("/api/preowned/report/{cert_id}")
async def api_preowned_report(cert_id: str):
    """Retrieve full inspection JSON data by Certificate ID."""
    rec = preowned_mgr.get_inspection_record(cert_id)
    if rec:
        return JSONResponse(content=rec)
    return JSONResponse(status_code=404, content={"error": f"Certificate {cert_id} not found"})


@app.get("/certification/{cert_id}", response_class=HTMLResponse)
async def view_preowned_certificate(cert_id: str):
    """View verifiable Chamunda Certified Pre-Owned HTML Certificate."""
    cert_file = INSPECTIONS_DIR / f"{cert_id}.html"
    if cert_file.exists():
        return HTMLResponse(content=cert_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>Chamunda Pre-Owned Certificate {cert_id} not found</h2>", status_code=404)


@app.get("/api/preowned/recent")
async def api_preowned_recent(limit: int = 50):
    """Get list of recent certified pre-owned inspections."""
    return JSONResponse(content=preowned_mgr.get_all_inspections(limit=limit))


# --- Chamunda Royal Enfield Expedition Readiness & Highway SOS Endpoints ---
@app.post("/api/expedition/audit")
async def api_expedition_audit(req: ExpeditionAuditRequest):
    """Execute 48-Point Expedition Pre-Touring Audit and generate QR Clearance Passport."""
    try:
        report = expedition_mgr.conduct_expedition_audit(
            rider_name=req.rider_name,
            phone=req.phone,
            bike_model=req.bike_model,
            registration_no=req.registration_no,
            destination_key=req.destination_key,
            planned_km=req.planned_km,
            domain_scores=req.domain_scores,
            inspector_name=req.inspector_name
        )
        return JSONResponse(content=report)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/api/expedition/spares-kit")
async def api_expedition_spares_kit(req: ExpeditionSparesKitRequest):
    """Build model & route specific carry-along backup spares kit from 4,469 parts catalog."""
    kit = expedition_mgr.build_carry_along_spares_kit(
        bike_model=req.bike_model,
        destination_key=req.destination_key
    )
    return JSONResponse(content=kit)


@app.post("/api/expedition/sos-triage")
async def api_expedition_sos_triage(req: HighwaySOSTriageRequest):
    """24/7 Highway Breakdown SOS roadside diagnostic triage and immediate directives."""
    res = expedition_mgr.highway_sos_triage(req.symptom_query)
    return JSONResponse(content=res)


@app.get("/api/expedition/passport/{exp_id}")
async def api_expedition_passport(exp_id: str):
    """Retrieve expedition audit record and verification data by Expedition ID."""
    rec = expedition_mgr.get_expedition_passport(exp_id)
    if rec:
        return JSONResponse(content=rec)
    return JSONResponse(status_code=404, content={"error": f"Expedition Passport {exp_id} not found"})


@app.get("/expedition/{exp_id}", response_class=HTMLResponse)
async def view_expedition_passport(exp_id: str):
    """View verifiable Chamunda Expedition Clearance Passport HTML."""
    exp_file = EXPEDITIONS_DIR / f"{exp_id}.html"
    if exp_file.exists():
        return HTMLResponse(content=exp_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>Chamunda Expedition Passport {exp_id} not found</h2>", status_code=404)


@app.get("/api/expedition/recent")
async def api_expedition_recent(limit: int = 50):
    """Get list of recent expedition readiness audits."""
    return JSONResponse(content=expedition_mgr.get_all_expeditions(limit=limit))



# --- Chamunda Royal Enfield Custom Resto-Mod & Vintage CI Endpoints ---
@app.post("/api/restomod/quote")
async def api_restomod_quote(req: RestoModQuoteRequest):
    """Generate bespoke Resto-Mod quote, BOM, Dyno tune, and digital QR blueprint."""
    try:
        quote = restomod_mgr.generate_restomod_quote(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            registration_no=req.registration_no,
            style_key=req.style_key or req.base_style or "bobber_solo",
            paint_theme_key=req.paint_theme_key or req.custom_paint or "british_racing_green",
            performance_stage_key=req.performance_stage_key or req.stage_tune or "stage_1",
            include_vintage_ci_package=req.include_vintage_ci_package,
            custom_notes=req.custom_notes
        )
        return JSONResponse(content=quote)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@app.post("/api/restomod/performance-tune")
async def api_restomod_performance_tune(req: PerformanceTuneRequest):
    """Calculate Stage 1 or Stage 2 Dyno performance calibration, HP/Torque gains & RTO dB check."""
    stg = req.stage_key or req.stage or "stage_1"
    res = restomod_mgr.calculate_performance_stage(req.bike_model, stg)
    return JSONResponse(content=res)


@app.post("/api/restomod/vintage-ci-diagnose")
async def api_restomod_vintage_ci_diagnose(req: VintageCIDiagnosticRequest):
    """Diagnose Vintage Cast-Iron (CI) Bullet (1970-2009) engine, CB point, tappet, or gearbox faults."""
    res = restomod_mgr.diagnose_vintage_ci_bullet(req.symptom_query)
    return JSONResponse(content=res)


@app.get("/api/restomod/blueprint/{resto_id}")
async def api_restomod_blueprint(resto_id: str):
    """Retrieve full Resto-Mod blueprint and BOM JSON data by Blueprint ID."""
    rec = restomod_mgr.get_restomod_blueprint(resto_id)
    if rec:
        return JSONResponse(content=rec)
    return JSONResponse(status_code=404, content={"error": f"Blueprint {resto_id} not found"})


@app.get("/restomod/{resto_id}", response_class=HTMLResponse)
async def view_restomod_blueprint(resto_id: str):
    """View verifiable Chamunda Custom Resto-Mod Blueprint HTML."""
    resto_file = RESTOMODS_DIR / f"{resto_id}.html"
    if resto_file.exists():
        return HTMLResponse(content=resto_file.read_text(encoding="utf-8"))
    return HTMLResponse(content=f"<h2>Chamunda Resto-Mod Blueprint {resto_id} not found</h2>", status_code=404)


@app.get("/api/restomod/recent")
async def api_restomod_recent(limit: int = 50):
    """Get list of recent custom resto-mod builds."""
    return JSONResponse(content=restomod_mgr.get_all_restomods(limit=limit))


# =====================================================================
# 360° OMNICHANNEL SOCIAL & BRAND MANAGEMENT REST ENDPOINTS
# =====================================================================

@app.get("/api/social/telemetry")
async def api_social_telemetry():
    """Get real-time social channels telemetry and engagement metrics."""
    return JSONResponse(content=social_eng.get_channel_telemetry())


@app.get("/api/social/channels")
async def api_social_channels():
    """Get list of configured social media channels."""
    return JSONResponse(content=social_eng.get_channels_info())


@app.post("/api/social/campaign/generate")
async def api_social_campaign_generate(req: SocialCampaignGenerateRequest):
    """Generate tailored, native content copies for WhatsApp, Instagram, Facebook, Google Business, and YouTube."""
    campaign = social_eng.generate_multi_platform_campaign(
        topic=req.topic,
        campaign_type=req.campaign_type,
        custom_notes=req.custom_notes
    )
    return JSONResponse(content=campaign)


@app.post("/api/social/publish")
async def api_social_publish(req: SocialPublishRequest):
    """Publish a campaign across designated or all social platforms."""
    campaign_data = {
        "campaign_id": req.campaign_id,
        "topic": req.topic,
        "campaign_type": req.campaign_type,
        "channels_data": req.channels_data or {}
    }
    res = social_eng.publish_to_channels(campaign_data=campaign_data, target_channels=req.channels)
    return JSONResponse(content=res)


@app.get("/api/social/inbox")
async def api_social_inbox(channel: Optional[str] = Query(None)):
    """Get unified omnichannel incoming social inbox messages."""
    items = social_eng.get_social_inbox(filter_channel=channel)
    return JSONResponse(content=items)


@app.post("/api/social/inbox/reply")
async def api_social_inbox_reply(req: SocialInboxReplyRequest):
    """Send response to an incoming social inbox message."""
    res = social_eng.reply_to_inbox_item(item_id=req.item_id, reply_text=req.reply_text)
    return JSONResponse(content=res)


@app.get("/api/social/reviews")
async def api_social_reviews(sentiment: Optional[str] = Query(None)):
    """Get Google Business Profile customer reviews."""
    reviews = social_eng.get_google_reviews(filter_sentiment=sentiment)
    return JSONResponse(content=reviews)


@app.post("/api/social/reviews/reply")
async def api_social_reviews_reply(req: GoogleReviewReplyRequest):
    """Publish owner reply to a Google Business Profile customer review."""
    res = social_eng.reply_to_google_review(
        review_id=req.review_id,
        reply_text=req.reply_text,
        reply_text_gu=req.reply_text_gu
    )
    return JSONResponse(content=res)


@app.get("/api/social/calendar")
async def api_social_calendar():
    """Get weekly content publishing calendar."""
    return JSONResponse(content=social_eng.get_content_calendar())


# =====================================================================
# EXECUTIVE SUB-AGENTS REST ENDPOINTS (UNDER CEO ARADHYA)
# =====================================================================

@app.get("/api/agents/list")
async def api_agents_list():
    """List all 5 departmental subagents under CEO Aradhya."""
    return JSONResponse(content=subagents_mgr.list_subagents())


@app.get("/api/agents/overview")
async def api_agents_overview():
    """Get consolidated executive overview of all departmental subagents."""
    return JSONResponse(content=subagents_mgr.get_executive_overview())


@app.post("/api/agents/delegate")
async def api_agents_delegate(req: TaskDelegationRequest):
    """Delegate an executive directive to a specific departmental subagent."""
    res = subagents_mgr.delegate_task(
        agent_id=req.agent_id,
        task_title=req.task_title,
        task_description=req.task_description,
        parameters=req.parameters
    )
    return JSONResponse(content=res)


@app.get("/api/agents/history")
async def api_agents_history(limit: int = 50):
    """Retrieve executive directives delegation history."""
    return JSONResponse(content=subagents_mgr.get_delegation_history(limit=limit))


@app.post("/api/agents/command")
async def api_agents_command(req: WrittenCommandRequest):
    """Execute a freeform written command from Alpesh Sir or CEO Aradhya."""
    cmd_lower = req.command.lower()
    if any(w in cmd_lower for w in ["lag", "lagging", "turbo", "boost", "speed up", "make laptop faster", "ઝડપી", "લેગ", "સ્પિડ", "clean ram", "free ram"]):
        opt_res = system_optimizer_eng.optimize_laptop_performance(aggressive=False)
        return JSONResponse(content={
            "success": True,
            "command_id": f"CMD-SYS-{int(time.time())}",
            "sender": req.sender or "Alpesh Sir",
            "target_agent": "system_optimizer",
            "designated_head": "System Optimizer & Lag Buster",
            "assigned_department": "Infrastructure & Performance",
            "priority": req.priority or "High",
            "response_gu": opt_res["message_gu"],
            "response_en": opt_res["message_en"],
            "result_summary": f"Freed {opt_res['freed_memory_mb']} MB RAM. Closed {opt_res['closed_processes_count']} stale processes.",
            "optimization_details": opt_res
        })

    res = subagents_mgr.execute_written_command(
        command_text=req.command,
        sender=req.sender or "Alpesh Sir (Founder & Chairman)",
        priority=req.priority or "Normal"
    )
    return JSONResponse(content=res)


@app.get("/api/agents/commands/history")
async def api_agents_commands_history(limit: int = 50):
    """Retrieve written command execution history."""
    return JSONResponse(content=subagents_mgr.get_written_commands_history(limit=limit))


@app.get("/api/agents/growth")
async def api_agents_growth():
    """Retrieve autonomous growth matrix, levels, and XP for all sub-agents."""
    return JSONResponse(content=subagents_mgr.get_agent_growth_telemetry())


@app.post("/api/agents/heal")
async def api_agents_heal(req: AgentHealRequest):
    """Trigger autonomous diagnostic and self-healing for an issue."""
    res = subagents_mgr.diagnose_and_heal_incident(
        agent_id=req.agent_id,
        issue_description=req.issue,
        auto_apply=True
    )
    return JSONResponse(content=res)


@app.post("/api/agents/simulate-incident")
async def api_agents_simulate_incident(req: SimulateIncidentRequest):
    """Simulate a domain incident and execute autonomous self-healing."""
    res = subagents_mgr.simulate_agent_incident(
        agent_id=req.agent_id,
        incident_type=req.incident_type
    )
    return JSONResponse(content=res)


# --- Project Garjana: Bay Voice, B2B Wholesale & Riders Club REST APIs ---
@app.post("/api/voice/process")
async def api_voice_process(req: BayVoiceProcessRequest):
    """Process hands-free workshop spoken voice command and coordinate across subagents."""
    res = bay_voice_eng.process_voice_action(
        spoken_text=req.spoken_text,
        mechanic_name=req.mechanic_name or "Master Tech Ramesh",
        bay_id=req.bay_id or "Bay 1 (J-Series Platform)"
    )
    return JSONResponse(content=res)


@app.get("/api/voice/logs")
async def api_voice_logs():
    """Get recent bay voice commands history."""
    return JSONResponse(content=bay_voice_eng.get_voice_logs())


@app.get("/api/b2b/overview")
async def api_b2b_overview():
    """Get B2B wholesale network overview, partner garages, routes, and metrics."""
    return JSONResponse(content=b2b_mgr.get_overview())


@app.get("/api/b2b/garages")
async def api_b2b_garages():
    """List all registered North Gujarat partner garages."""
    return JSONResponse(content=b2b_mgr.get_garages())


@app.post("/api/b2b/garages/register")
async def api_b2b_register_garage(req: B2BGarageRegisterRequest):
    """Register a new partner garage in North Gujarat."""
    garage = b2b_mgr.register_garage(
        name=req.name,
        owner_name=req.owner_name,
        phone=req.phone,
        city=req.city,
        address=req.address,
        tier=req.tier or "Bronze",
        gstin=req.gstin or ""
    )
    return JSONResponse(content=garage)


@app.post("/api/b2b/orders/create")
async def api_b2b_create_order(req: B2BOrderCreateRequest):
    """Create wholesale parts order for a partner garage."""
    order = b2b_mgr.create_order(
        garage_id=req.garage_id,
        items=req.items,
        payment_mode=req.payment_mode or "Credit",
        notes=req.notes or ""
    )
    return JSONResponse(content=order)


@app.get("/api/b2b/orders")
async def api_b2b_orders():
    """Get wholesale order history."""
    return JSONResponse(content=b2b_mgr.get_orders())


@app.get("/api/b2b/routes")
async def api_b2b_routes():
    """Get daily van delivery routes."""
    return JSONResponse(content=b2b_mgr.get_delivery_routes())


@app.get("/api/club/overview")
async def api_club_overview():
    """Get Chamunda Royal Riders Club overview and metrics."""
    return JSONResponse(content=riders_club_mgr.get_overview())


@app.get("/api/club/amc/plans")
async def api_club_plans():
    """Get AMC membership plans."""
    return JSONResponse(content=riders_club_mgr.get_amc_plans())


@app.get("/api/club/members")
async def api_club_members():
    """List active club members."""
    return JSONResponse(content=riders_club_mgr.get_members())


@app.post("/api/club/members/enroll")
async def api_club_enroll(req: ClubEnrollRequest):
    """Enroll a rider into AMC pass."""
    member = riders_club_mgr.enroll_member(
        name=req.name,
        phone=req.phone,
        bike_model=req.bike_model,
        registration_no=req.registration_no,
        plan_id=req.plan_id or "AMC-GOLD"
    )
    return JSONResponse(content=member)


@app.get("/api/club/expeditions")
async def api_club_expeditions():
    """Get upcoming club expeditions."""
    return JSONResponse(content=riders_club_mgr.get_expeditions())


@app.post("/api/club/expeditions/register")
async def api_club_register_expedition(req: ClubExpeditionRegisterRequest):
    """Register rider for an upcoming expedition."""
    res = riders_club_mgr.register_for_expedition(
        expedition_id=req.expedition_id,
        rider_name=req.rider_name,
        phone=req.phone,
        bike_model=req.bike_model
    )
    return JSONResponse(content=res)


# --- Project Spandan & Drishti: OBD-II, Smart Kiosk & Predictive Supply Chain APIs ---
@app.post("/api/obd/scan")
async def api_obd_scan(req: OBDScanRequest):
    """Run live OBD-II diagnostic scan on Royal Enfield motorcycle."""
    res = obd_eng.run_obd_scan(
        bike_model=req.bike_model,
        registration_no=req.registration_no,
        simulate_dtc=req.simulate_dtc
    )
    return JSONResponse(content=res)


@app.get("/api/obd/telemetry/{bike_model}")
async def api_obd_telemetry(bike_model: str):
    """Get live streaming telemetry simulation for a bike platform."""
    return JSONResponse(content=obd_eng.generate_live_telemetry(bike_model=bike_model))


@app.get("/api/obd/scans")
async def api_obd_scans():
    """Get recent OBD-II diagnostic scans."""
    return JSONResponse(content=obd_eng.get_recent_scans())


@app.get("/api/kiosk/lookup/{registration_no}")
async def api_kiosk_lookup(registration_no: str):
    """Lookup vehicle history, past job cards, and health passport at lounge kiosk."""
    return JSONResponse(content=kiosk_eng.lookup_vehicle(registration_no=registration_no))


@app.post("/api/kiosk/checkin")
async def api_kiosk_checkin(req: KioskCheckinRequest):
    """Process customer self-service kiosk check-in and issue queue token."""
    token = kiosk_eng.process_checkin(
        registration_no=req.registration_no,
        customer_name=req.customer_name,
        phone=req.phone,
        bike_model=req.bike_model,
        selected_issues=req.selected_issues,
        odometer_km=req.odometer_km or 15000
    )
    return JSONResponse(content=token)


@app.get("/api/kiosk/tokens")
async def api_kiosk_tokens():
    """Get list of active lounge queue tokens."""
    return JSONResponse(content=kiosk_eng.get_tokens())


@app.get("/api/supply-chain/forecast")
async def api_supply_chain_forecast(season: str = "diwali_dhanteras_rush"):
    """Get inventory forecast and velocity analysis under selected seasonal rush."""
    return JSONResponse(content=supply_chain_mgr.get_critical_parts_forecast(season_key=season))


@app.post("/api/supply-chain/auto-po/generate")
async def api_supply_chain_auto_po(req: AutoPOGenerateRequest):
    """Auto-generate wholesale replenishment purchase order for parts nearing stockout."""
    po = supply_chain_mgr.generate_auto_replenishment_po(
        season_key=req.season_key or "diwali_dhanteras_rush",
        supplier_name=req.supplier_name or "Royal Enfield Central Spares Distribution Depot"
    )
    return JSONResponse(content=po)


@app.get("/api/supply-chain/pos")
async def api_supply_chain_pos():
    """Get list of auto-generated purchase orders."""
    return JSONResponse(content=supply_chain_mgr.get_auto_pos())


# --- Project Trinetra: 3D Schematics, AI Borescope & Multi-Branch Hub APIs ---
@app.get("/api/schematics/assemblies")
async def api_schematics_assemblies():
    """Get all 3D interactive exploded engine assemblies and torque specifications."""
    return JSONResponse(content=schematics_eng.get_assemblies())


@app.get("/api/schematics/assembly/{assembly_id}")
async def api_schematic_assembly(assembly_id: str):
    """Get detailed 3D exploded view, BOM components, and torque specs for an assembly."""
    assembly = schematics_eng.get_assembly_by_id(assembly_id)
    if not assembly:
        return JSONResponse(content={"error": f"Assembly {assembly_id} not found"}, status_code=404)
    return JSONResponse(content=assembly)


@app.post("/api/borescope/inspect")
async def api_borescope_inspect(req: BorescopeInspectRequest):
    """Run non-invasive AI borescope optical endoscopy and combustion health diagnosis."""
    res = borescope_eng.inspect_combustion_chamber(
        bike_model=req.bike_model,
        registration_no=req.registration_no,
        odometer_km=req.odometer_km,
        scenario=req.scenario
    )
    return JSONResponse(content=res)


@app.get("/api/borescope/inspections")
async def api_borescope_inspections():
    """Get recent borescope endoscopic inspections."""
    return JSONResponse(content=borescope_eng.get_inspections())


@app.get("/api/branches/overview")
async def api_branches_overview():
    """Get consolidated North Gujarat multi-branch cloud franchise telemetry and transit ledger."""
    return JSONResponse(content=multibranch_eng.get_branches_overview())


@app.get("/api/branches/list")
async def api_branches_list():
    """List all registered franchise branches."""
    return JSONResponse(content=multibranch_eng.get_branches())


@app.post("/api/branches/transfer-stock")
async def api_branches_transfer(req: BranchTransferRequest):
    """Dispatch an intra-branch stock transfer across North Gujarat branches."""
    try:
        res = multibranch_eng.transfer_stock(
            from_branch=req.from_branch,
            to_branch=req.to_branch,
            part_number=req.part_number,
            quantity=req.quantity,
            requested_by=req.requested_by,
            part_name=req.part_name,
            unit_mrp=req.unit_mrp or 0.0,
            notes=req.notes or ""
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)


@app.get("/api/system/resources")
async def api_system_resources():
    """Get real-time CPU, RAM, load averages, and top processes to monitor system performance."""
    return JSONResponse(content=system_optimizer_eng.get_system_metrics())


@app.post("/api/system/optimize")
async def api_system_optimize(req: Optional[SystemOptimizeRequest] = None):
    """Execute high-speed Turbo Boost to terminate stale processes, trim memory, and purge caches."""
    try:
        mode = req.mode if req else "safe"
        res = system_optimizer_eng.optimize_laptop_performance(aggressive=(mode == "aggressive"))
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)




@app.get("/api/webar/assemblies")
async def api_webar_assemblies():
    """Get all pre-calibrated WebAR engine assemblies with live stock status."""
    return JSONResponse(content=webar_eng.get_assemblies())


@app.get("/api/webar/overlay/{assembly_id}")
async def api_webar_overlay(assembly_id: str, width: int = 640, height: int = 480):
    """Calculate pixel-accurate screen markers and SVG tightening paths for WebAR camera HUD."""
    res = webar_eng.calculate_ar_camera_view(assembly_id, camera_feed_width=width, camera_feed_height=height)
    return JSONResponse(content=res)


@app.get("/api/locker/status")
async def api_locker_status():
    """Get real-time 24/7 smart emergency locker telemetry, box statuses, and sales log."""
    return JSONResponse(content=night_locker_mgr.get_locker_status())


@app.post("/api/locker/reserve")
async def api_locker_reserve(req: LockerReserveRequest):
    """Reserve an emergency locker compartment, generate dynamic UPI payment, and 6-digit OTP."""
    try:
        res = night_locker_mgr.reserve_compartment(
            box_id=req.box_id,
            customer_name=req.customer_name,
            phone=req.phone,
            vehicle_reg=req.vehicle_reg or "Touring Rider"
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)


@app.post("/api/locker/unlock")
async def api_locker_unlock(req: LockerUnlockRequest):
    """Verify OTP and trigger physical 12V solenoid relay unlock for emergency spare dispenser."""
    try:
        res = night_locker_mgr.verify_and_unlock(
            reservation_id=req.reservation_id,
            otp_code=req.otp_code,
            payment_ref=req.payment_ref or "UPI-AUTOCONFIRMED"
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)




@app.get("/api/cloud-shadow/status")
async def api_cloud_shadow_status():
    """Get real-time cloud shadow status, replicas, and sync health."""
    return JSONResponse(content=cloud_shadow_mgr.get_shadow_telemetry())


@app.post("/api/cloud-shadow/sync")
async def api_cloud_shadow_sync(req: Optional[CloudShadowSyncRequest] = None):
    """Trigger instant local-to-cloud state snapshot synchronization."""
    try:
        res = cloud_shadow_mgr.generate_state_snapshot()
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/cloud-shadow/query")
async def api_cloud_shadow_query(req: CloudShadowQueryRequest):
    """Process natural language query via Cloud Shadow replica agents as if laptop is offline."""
    try:
        res = cloud_shadow_mgr.process_remote_offline_query(
            query_text=req.query,
            sender=req.sender or "Alpesh Sir (Remote Mobile)",
            phone=req.phone or "+91 78747 19139"
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)


@app.post("/api/cloud-shadow/reconcile")
async def api_cloud_shadow_reconcile():
    """Reconcile queued offline mutations upon laptop reconnection."""
    try:
        res = cloud_shadow_mgr.reconcile_sync()
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)



class KalpavrikshaIngestRequest(BaseModel):
    engine_family: str
    category: str
    target_components: str = ""
    torque_sequence: str = ""
    clearances: str = ""
    ramesh_secret: str = ""


@app.get("/api/kalpavriksha/status")
async def api_kalpavriksha_status():
    """Return Project Kalpavriksha fleet mastery, XP, and offline specs."""
    try:
        return JSONResponse(content=kalpavriksha_mgr.get_growth_telemetry())
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/kalpavriksha/simulate")
async def api_kalpavriksha_simulate():
    """Execute an autonomous Royal Enfield synthetic diagnostic scenario."""
    try:
        res = kalpavriksha_mgr.run_synthetic_diagnostic_simulation()
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/kalpavriksha/surge")
async def api_kalpavriksha_surge():
    """Execute a 10x deep-learning mastery surge across the fleet."""
    try:
        res = kalpavriksha_mgr.run_mastery_surge(count=10)
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/kalpavriksha/ingest-spec")
async def api_kalpavriksha_ingest_spec(req: KalpavrikshaIngestRequest):
    """Ingest a factory torque/clearance spec into local disk memory."""
    try:
        res = kalpavriksha_mgr.ingest_technical_manual_spec(
            engine_family=req.engine_family,
            category=req.category,
            target_components=req.target_components,
            torque_sequence=req.torque_sequence,
            clearances=req.clearances,
            ramesh_secret=req.ramesh_secret
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)



# ==============================================================================
# RE-DMS SUITE REST API ENDPOINTS
# ==============================================================================

class DMSInvoiceRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    odometer_km: int = 4500
    parts_items: Optional[List[Dict[str, Any]]] = None
    labor_items: Optional[List[Dict[str, Any]]] = None
    discount_amount: float = 0.0
    payment_mode: str = "UPI (Instant)"
    warranty_type: str = "None"


class DMSWarrantyClaimRequest(BaseModel):
    coupon_type: str
    chassis_no: str
    engine_no: str
    bike_model: str
    customer_name: str
    phone: str
    kilometers: int
    defective_components: str
    claim_amount: float


class DMSCampaignRequest(BaseModel):
    name: str
    target_audience: str
    offer_title: str
    offer_details: str
    channels: Optional[List[str]] = None


@app.get("/api/dms/overview")
async def api_dms_overview():
    """Return RE-DMS dashboard overview telemetry and 10-officer dealership fleet roster."""
    try:
        overview = dms_suite_eng.get_dms_overview_telemetry()
        # Ensure Aradhya CEO + 9 autonomous subagents = 10 total dealership officers
        ceo_officer = {
            "agent_id": "aradhya_ceo",
            "name": "Aradhya (Dealership CEO)",
            "designated_head": "Aradhya (આરાધ્યા)",
            "department": "Executive Dealership Operations & AI Orchestration",
            "role": "Chief Executive Officer & Commander",
            "status": "ONLINE"
        }
        fleet = [ceo_officer] + subagents_mgr.list_subagents()
        return JSONResponse(content={
            "success": True,
            "overview": overview,
            "fleet": fleet
        })
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/invoice")
async def api_dms_invoice(req: DMSInvoiceRequest):
    """Generate a Split-GST Dealership Tax Invoice with Dynamic UPI QR & Gate Pass."""
    try:
        res = dms_suite_eng.create_split_gst_invoice(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            registration_no=req.registration_no,
            odometer_km=req.odometer_km,
            parts_items=req.parts_items,
            labor_items=req.labor_items,
            discount_amount=req.discount_amount,
            payment_mode=req.payment_mode,
            warranty_type=req.warranty_type
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/warranty-claim")
async def api_dms_warranty_claim(req: DMSWarrantyClaimRequest):
    """File an OEM Warranty or FSC Coupon claim to Royal Enfield India."""
    try:
        res = dms_suite_eng.file_oem_warranty_claim(
            coupon_type=req.coupon_type,
            chassis_no=req.chassis_no,
            engine_no=req.engine_no,
            bike_model=req.bike_model,
            customer_name=req.customer_name,
            phone=req.phone,
            kilometers=req.kilometers,
            defective_components=req.defective_components,
            claim_amount=req.claim_amount
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.get("/api/dms/daybook")
async def api_dms_daybook():
    """Return double-entry Daybook, Accounts Receivable/Payable and P&L."""
    try:
        res = dms_suite_eng.get_dms_accounting_daybook()
        return JSONResponse(content={"success": True, "accounting": res})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/campaign")
async def api_dms_campaign(req: DMSCampaignRequest):
    """Launch a targeted marketing campaign."""
    try:
        res = dms_suite_eng.create_marketing_campaign(
            name=req.name,
            target_audience=req.target_audience,
            offer_title=req.offer_title,
            offer_details=req.offer_details,
            channels=req.channels
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.get("/api/dms/leads")
async def api_dms_leads():
    """Return lead pipeline for test rides and bike bookings."""
    try:
        leads = dms_suite_eng.get_lead_pipeline()
        return JSONResponse(content={"success": True, "leads": leads})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/service-reminders")
async def api_dms_service_reminders():
    """Dispatch automated 30/60/90-day WhatsApp service reminders."""
    try:
        res = dms_suite_eng.dispatch_service_reminder_broadcast()
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)



class DMSBookingRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    colorway: str = "Standard Edition"
    booking_amount: float = 10000.0
    payment_mode: str = "UPI (Instant)"
    finance_bank: str = "HDFC Two Wheeler Finance"
    tentative_delivery_date: Optional[str] = None


class DMSPDIRequest(BaseModel):
    chassis_no: str
    engine_no: str
    bike_model: str
    customer_name: str
    inspector_name: str = "Master Tech Ramesh & Vikram Singh"
    battery_voltage: float = 12.8
    tire_pressure_psi: str = "Front: 32 PSI / Rear: 36 PSI"
    idle_rpm: int = 1050
    toolkit_handed_over: bool = True


class DMSRideSureRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    chassis_no: str
    coverage_years: int = 4
    plan_type: str = "Ride Sure Premium (Extended Warranty + 24/7 Roadside Assistance)"
    premium_amount: float = 3850.0


class DMSInsuranceEstimateRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    registration_no: str
    insurance_company: str
    surveyor_name: str
    parts_estimate: float
    labor_estimate: float
    salvage_deduction: float = 250.0
    compulsory_deductible: float = 100.0


class DMSPSFFeedbackRequest(BaseModel):
    invoice_no: str
    customer_name: str
    phone: str
    bike_model: str
    rating_1_to_5: int
    feedback_notes: str
    issues_resolved: bool = True


@app.post("/api/dms/booking")
async def api_dms_booking(req: DMSBookingRequest):
    """Create new motorcycle showroom booking with advance token receipt."""
    try:
        res = dms_suite_eng.create_vehicle_booking(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            colorway=req.colorway,
            booking_amount=req.booking_amount,
            payment_mode=req.payment_mode,
            finance_bank=req.finance_bank,
            tentative_delivery_date=req.tentative_delivery_date
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/pdi")
async def api_dms_pdi(req: DMSPDIRequest):
    """Generate digital 30-Point Pre-Delivery Inspection certificate."""
    try:
        res = dms_suite_eng.generate_pdi_inspection(
            chassis_no=req.chassis_no,
            engine_no=req.engine_no,
            bike_model=req.bike_model,
            customer_name=req.customer_name,
            inspector_name=req.inspector_name,
            battery_voltage=req.battery_voltage,
            tire_pressure_psi=req.tire_pressure_psi,
            idle_rpm=req.idle_rpm,
            toolkit_handed_over=req.toolkit_handed_over
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/ride-sure")
async def api_dms_ride_sure(req: DMSRideSureRequest):
    """Issue Royal Enfield Ride Sure extended warranty policy and 24/7 RSA."""
    try:
        res = dms_suite_eng.issue_ride_sure_warranty(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            registration_no=req.registration_no,
            chassis_no=req.chassis_no,
            coverage_years=req.coverage_years,
            plan_type=req.plan_type,
            premium_amount=req.premium_amount
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/insurance-estimate")
async def api_dms_insurance_estimate(req: DMSInsuranceEstimateRequest):
    """Generate accidental surveyor repair estimate with cashless DO computation."""
    try:
        res = dms_suite_eng.create_insurance_claim_estimate(
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            registration_no=req.registration_no,
            insurance_company=req.insurance_company,
            surveyor_name=req.surveyor_name,
            parts_estimate=req.parts_estimate,
            labor_estimate=req.labor_estimate,
            salvage_deduction=req.salvage_deduction,
            compulsory_deductible=req.compulsory_deductible
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/dms/psf-feedback")
async def api_dms_psf_feedback(req: DMSPSFFeedbackRequest):
    """Log post-service 3-day customer feedback and compute CSAT & FTR."""
    try:
        res = dms_suite_eng.record_post_service_feedback(
            invoice_no=req.invoice_no,
            customer_name=req.customer_name,
            phone=req.phone,
            bike_model=req.bike_model,
            rating_1_to_5=req.rating_1_to_5,
            feedback_notes=req.feedback_notes,
            issues_resolved=req.issues_resolved
        )
        return JSONResponse(content=res)
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.get("/api/dms/csat-telemetry")
async def api_dms_csat_telemetry():
    """Return workshop CSAT and PSF quality control telemetry."""
    try:
        res = dms_suite_eng.get_csat_and_qc_telemetry()
        return JSONResponse(content={"success": True, "csat": res})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.get("/api/dms/showroom-telemetry")
async def api_dms_showroom_telemetry():
    """Return showroom new vehicle sales and PDI telemetry."""
    try:
        res = dms_suite_eng.get_showroom_sales_telemetry()
        return JSONResponse(content={"success": True, "showroom": res})
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)



# ==============================================================================
# PROJECT CHHAYA: UNIVERSAL MULTI-AGENT GATEWAY REST API
# ==============================================================================

class ChhayaAgentChatRequest(BaseModel):
    message: str
    sender: Optional[str] = "Alpesh Sir (Remote Mobile)"
    preferred_model: Optional[str] = "auto"


class ChhayaAgentRegisterRequest(BaseModel):
    agent_id: str
    name: str
    name_gu: Optional[str] = None
    designated_head: Optional[str] = None
    department: Optional[str] = "Custom Future Agent"
    category: Optional[str] = "CUSTOM_FUTURE"
    icon: Optional[str] = "fa-solid fa-microchip"
    color: Optional[str] = "#0984e3"
    capabilities: Optional[List[str]] = None
    quick_chips: Optional[List[Dict[str, str]]] = None


@app.get("/api/chhaya/models")
async def api_app_chhaya_models():
    """List available AI models and their tier capabilities."""
    from chamunda_llm_engine import get_chamunda_ai_engine
    engine = get_chamunda_ai_engine()
    return JSONResponse(content={"success": True, "models": engine.list_available_models()})


@app.get("/api/chhaya/agents")
async def api_app_chhaya_list_agents(category: Optional[str] = None):
    """List all agents inside this laptop (dealership, engineering, future)."""
    agents = chhaya_gateway.list_all_agents(category=category)
    return JSONResponse(content={"success": True, "count": len(agents), "agents": agents})


@app.get("/api/chhaya/agents/{agent_id}")
async def api_app_chhaya_get_agent(agent_id: str):
    """Retrieve detailed profile, capabilities, and telemetry for a specific agent."""
    agent = chhaya_gateway.get_agent(agent_id)
    if not agent:
        return JSONResponse(content={"success": False, "error": f"Agent '{agent_id}' not found"}, status_code=404)
    history = chhaya_gateway.get_agent_recent_activities(agent_id)
    return JSONResponse(content={"success": True, "agent": agent, "recent_activities": history})


@app.post("/api/chhaya/agents/{agent_id}/chat")
async def api_app_chhaya_agent_chat(agent_id: str, req: ChhayaAgentChatRequest):
    """Dispatch natural language prompt or command directly to a specific agent."""
    res = await asyncio.to_thread(
        chhaya_gateway.chat_with_agent,
        agent_id=agent_id,
        message=req.message,
        sender=req.sender or "Alpesh Sir (Remote Mobile)",
        preferred_model=req.preferred_model or "auto"
    )
    return JSONResponse(content=res)


@app.post("/api/chhaya/agents/{agent_id}/command")
async def api_app_chhaya_agent_command(agent_id: str, req: ChhayaAgentChatRequest):
    """Execute a structured command on a specific agent."""
    res = await asyncio.to_thread(
        chhaya_gateway.chat_with_agent,
        agent_id=agent_id,
        message=req.message,
        sender=req.sender or "Alpesh Sir (Remote Mobile)",
        preferred_model=req.preferred_model or "auto"
    )
    return JSONResponse(content=res)


@app.post("/api/chhaya/agents/register")
async def api_app_chhaya_register_agent(req: ChhayaAgentRegisterRequest):
    """Dynamically register any new future agent so it appears on mobile immediately."""
    res = chhaya_gateway.register_future_agent(req.dict())
    return JSONResponse(content=res)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)



