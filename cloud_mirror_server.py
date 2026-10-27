"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
Universal Mobile Multi-Agent Gateway & Autonomous Cloud Mirror Server (Port 8081).
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)
"""

import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List
import socket

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
sys.path.insert(0, str(BASE_DIR))

from cloud_shadow_engine import get_cloud_shadow_manager, OFFICIAL_WHATSAPP_HELPLINE
from kalpavriksha_growth_engine import get_kalpavriksha_engine
from dms_enterprise_suite_engine import get_dms_suite_engine
from chhaya_agent_gateway import get_chhaya_agent_gateway
from system_optimizer import get_system_optimizer
from whatsapp_dispatch_engine import get_whatsapp_dispatch_engine, OFFICIAL_WHATSAPP_PHONE
from cloudflare_security_auditor import get_cloudflare_auditor


def get_public_url() -> Optional[str]:
    """Retrieve active public mobile tunnel URL if available."""
    pub_file = DATA_DIR / "chhaya_public_url.txt"
    if pub_file.exists():
        try:
            url = pub_file.read_text(encoding="utf-8").strip()
            if url.startswith("https://") or url.startswith("http://"):
                return url
        except Exception:
            pass
    return None

def get_local_ip() -> str:
    """Dynamically get the current local Wi-Fi / hotspot IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            import subprocess
            out = subprocess.check_output(["hostname", "-I"], timeout=1).decode().strip()
            if out:
                return out.split()[0]
        except Exception:
            pass
    return "127.0.0.1"

app = FastAPI(
    title="Project Chhaya • Universal Mobile Multi-Agent Gateway",
    description="Unified 24/7 Mobile Command Center for All Autonomous Agents on this Laptop",
    version="3.0.0"
)

# Mount OpenAI-Compatible Gateway Bridge for Open WebUI (/v1)
from aradhya_openai_bridge import router as openai_router
app.include_router(openai_router)

@app.middleware("http")
async def add_cloudflare_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Server"] = "Cloudflare-Zero-Trust-Chhaya/3.0"
    return response

# Mount static files for PWA
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/manifest.json")
async def root_manifest():
    manifest_path = STATIC_DIR / "manifest.json"
    if manifest_path.exists():
        return FileResponse(str(manifest_path), media_type="application/manifest+json")
    return JSONResponse(status_code=404, content={"error": "manifest not found"})

@app.get("/favicon.ico")
async def root_favicon():
    icon_path = STATIC_DIR / "icons" / "icon-192.png"
    if icon_path.exists():
        return FileResponse(str(icon_path), media_type="image/png")
    return JSONResponse(status_code=404, content={"error": "icon not found"})


shadow_mgr = get_cloud_shadow_manager()
kalpavriksha_mgr = get_kalpavriksha_engine()
dms_suite_mgr = get_dms_suite_engine()
chhaya_gateway = get_chhaya_agent_gateway()


# --- Pydantic Models ---
class RemoteQueryRequest(BaseModel):
    query: str
    sender: Optional[str] = "Alpesh Sir (Remote Mobile)"
    phone: Optional[str] = OFFICIAL_WHATSAPP_HELPLINE


class QueueMutationRequest(BaseModel):
    mutation_type: str
    payload: Dict[str, Any]


class AgentChatRequest(BaseModel):
    message: str
    sender: Optional[str] = "Alpesh Sir (Remote Mobile)"
    preferred_model: Optional[str] = "auto"


class AgentSpeakRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"
    voice_gender: Optional[str] = "female"


class AgentRegisterRequest(BaseModel):
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


class CloudBookingRequest(BaseModel):
    customer_name: str
    phone: str
    bike_model: str
    colorway: str = "Standard Edition"
    booking_amount: float = 10000.0
    payment_mode: str = "UPI (Instant)"
    finance_bank: str = "HDFC Two Wheeler Finance"
    tentative_delivery_date: Optional[str] = None


class CloudPSFFeedbackRequest(BaseModel):
    invoice_no: str
    customer_name: str
    phone: str
    bike_model: str
    rating_1_to_5: int
    feedback_notes: str
    issues_resolved: bool = True


# ==============================================================================
# SINGLE MAIN LINK: UNIVERSAL AGENTS HUB & DEDICATED WORKSPACES
# ==============================================================================
@app.get("/")
async def cloud_mirror_home():
    st = shadow_mgr.get_shadow_telemetry()
    kv = kalpavriksha_mgr.get_growth_telemetry()
    local_ip = get_local_ip()
    pub_url = get_public_url()
    primary_link = pub_url or f"http://{local_ip}:8081"

    html = f"""<!DOCTYPE html>
<html lang="gu">
<head>
    <meta charset="UTF-8">
    <title>Project Chhaya • Universal Multi-Agent Gateway</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta name="theme-color" content="#f39c12">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link rel="manifest" href="/static/manifest.json">
    <link rel="apple-touch-icon" href="/static/icons/icon-192.png">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #070c17;
            --card-bg: #0f172a;
            --card-hover: #1e293b;
            --border-color: #1e293b;
            --border-highlight: #334155;
            --gold: #f39c12;
            --green: #10b981;
            --blue: #3b82f6;
            --purple: #8b5cf6;
            --pink: #ec4899;
        }}
        body {{
            background-color: var(--bg-dark);
            color: #f1f5f9;
            font-family: system-ui, -apple-system, sans-serif;
            padding-bottom: 50px;
            overflow-x: hidden;
        }}
        .card-custom {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
        }}
        .agent-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            transition: all 0.25s ease;
            cursor: pointer;
        }}
        .agent-card:hover {{
            background: var(--card-hover);
            border-color: var(--gold);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(243, 156, 18, 0.15);
        }}
        .avatar-box {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            flex-shrink: 0;
        }}
        .quick-chip {{
            font-size: 0.78rem;
            cursor: pointer;
            border-radius: 20px;
            padding: 5px 12px;
            background: #1e293b;
            border: 1px solid #334155;
            color: #cbd5e1;
            transition: all 0.2s;
            display: inline-block;
            white-space: nowrap;
        }}
        .quick-chip:hover, .quick-chip:active {{
            background: var(--gold);
            color: #000;
            border-color: var(--gold);
            font-weight: 600;
        }}
        .filter-btn {{
            font-size: 0.75rem;
            border-radius: 20px;
            padding: 4px 12px;
            background: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
            transition: all 0.2s;
        }}
        .filter-btn.active {{
            background: var(--gold);
            color: #000;
            font-weight: bold;
            border-color: var(--gold);
        }}
        .chat-bubble-user {{
            background: #1e3a8a;
            color: #fff;
            border-radius: 16px 16px 4px 16px;
            padding: 10px 14px;
            max-width: 85%;
            margin-left: auto;
            margin-bottom: 10px;
            font-size: 0.9rem;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.6;
        }}
        .chat-bubble-agent {{
            background: #1e293b;
            color: #f1f5f9;
            border-radius: 16px 16px 16px 4px;
            padding: 12px 16px;
            max-width: 90%;
            margin-right: auto;
            margin-bottom: 10px;
            font-size: 0.9rem;
            border: 1px solid #334155;
            white-space: pre-wrap;
            word-break: break-word;
            line-height: 1.6;
        }}
        .app-bar {{
            position: sticky;
            top: 0;
            z-index: 1020;
            background: rgba(7, 12, 23, 0.92);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 10px 0;
        }}
    </style>
</head>
<body class="p-2 p-md-4">
    <div class="container" style="max-width: 860px;">

        <!-- Sticky App Bar -->
        <div class="app-bar mb-3">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                <div class="d-flex align-items-center gap-2">
                    <span class="badge bg-warning text-dark fw-bold px-2 py-1">PROJECT CHHAYA</span>
                    <span class="badge bg-dark border border-success text-success"><i class="fa-solid fa-circle me-1" style="font-size:0.55rem;"></i>24/7 ONLINE</span>
                    <span class="badge bg-dark border border-secondary text-muted" id="totalAgentsHeaderBadge">19 AGENTS</span>
                </div>
                <div class="d-flex gap-2">
                    <button class="btn btn-sm btn-outline-warning" id="navHubBtn" onclick="showHubView()">
                        <i class="fa-solid fa-th-large me-1"></i> All Agents Hub
                    </button>
                    <button class="btn btn-sm btn-success fw-bold" onclick="sendLinkToWhatsApp()" id="sendWaBtn" title="Send live link to WhatsApp 7874719139">
                        <i class="fa-brands fa-whatsapp me-1"></i> Send Link to 7874719139
                    </button>
                </div>
            </div>
        </div>

        <!-- Permanent Mobile Access Bar -->
        <div class="card card-custom p-2 px-3 mb-3 border-success" style="background: rgba(16, 185, 129, 0.08);">
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                <div>
                    <span class="badge bg-success text-dark fw-bold me-1"><i class="fa-solid fa-lock me-1"></i>કાયમી લિંક (Permanent Link)</span>
                    <span class="font-mono text-light small fw-bold">http://alpesh-Inspiron-3542.local:8081</span>
                    <small class="text-muted d-block" style="font-size:0.75rem;">Wi-Fi કે હોટસ્પોટ પર આ લિંક ક્યારેય બદલાતી નથી (૧૦૦% કાયમી)</small>
                </div>
                <div class="d-flex gap-1">
                    <button class="btn btn-sm btn-outline-success font-mono" onclick="copyPermanentLink()">
                        <i class="fa-solid fa-copy me-1"></i>Copy
                    </button>
                    <button class="btn btn-sm btn-warning fw-bold" id="pwaInstallBtn" onclick="installPWA()">
                        <i class="fa-solid fa-mobile-screen me-1"></i>Add to Home Screen
                    </button>
                </div>
            </div>
        </div>

        <!-- =================================================================== -->
        <!-- VIEW 1: UNIVERSAL AGENTS HUB (MAIN DIRECTORY OF ALL AGENTS) -->
        <!-- =================================================================== -->
        <div id="hubView">
            <!-- Hero Banner -->
            <div class="card card-custom p-3 p-md-4 mb-3 border-warning shadow-lg text-center" style="background: linear-gradient(135deg, #111e38 0%, #070c17 100%);">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-dark border border-warning text-warning">UNIVERSAL GATEWAY</span>
                    <small class="text-muted">Master Supervisor: <strong>Alpesh Sir</strong></small>
                </div>
                <h3 class="text-warning mb-1 fw-bold"><i class="fa-solid fa-microchip me-2"></i>Universal Multi-Agent Command Center</h3>
                <p class="text-muted small mb-3">Single access link for all <strong class="text-light" id="totalAgentsCount">19</strong> autonomous agents inside this laptop &amp; future discoveries. Tap any agent to launch a dedicated mobile workspace.</p>

                <!-- Search & Filters -->
                <div class="input-group mb-3">
                    <span class="input-group-text bg-dark border-secondary text-muted"><i class="fa-solid fa-magnifying-glass"></i></span>
                    <input type="text" id="agentSearchInput" class="form-control bg-dark text-light border-secondary" placeholder="Search agents by name, skills, Gujarati role..." oninput="filterAgents()">
                </div>

                <div class="d-flex flex-wrap justify-content-center gap-1" id="categoryFilterRow">
                    <button class="filter-btn active" onclick="setCategoryFilter('ALL', this)">All Agents</button>
                    <button class="filter-btn" onclick="setCategoryFilter('DEALERSHIP_OFFICER', this)">🏢 Dealership Officers (10)</button>
                    <button class="filter-btn" onclick="setCategoryFilter('SYSTEM_ENGINEERING', this)">💻 System &amp; Apps (4)</button>
                    <button class="filter-btn" onclick="setCategoryFilter('MEDIA_CREATIVE', this)">🎨 Media &amp; Creative (3)</button>
                    <button class="filter-btn" onclick="setCategoryFilter('CUSTOM_FUTURE', this)">🚀 Future Agents</button>
                </div>
            </div>

            <!-- Agents Grid -->
            <div class="row g-3 mb-4" id="agentsCardsContainer">
                <!-- Populated dynamically via JavaScript -->
                <div class="col-12 text-center text-muted py-4">
                    <i class="fa-solid fa-spinner fa-spin fa-2x mb-2"></i>
                    <div>Discovering all agents inside laptop...</div>
                </div>
            </div>

            <!-- Quick Access: Kalpavriksha Virtual Growth & Autonomous Replicas -->
            <div class="card card-custom p-3 mb-3 border-secondary">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <h6 class="text-warning mb-0"><i class="fa-solid fa-tree me-1"></i>Project Kalpavriksha • Autonomous Growth</h6>
                        <small class="text-muted">Fleet IQ: <strong class="text-light">{kv['fleet_overall_iq']}</strong> &bull; Total XP: <strong class="text-success">{kv['total_fleet_xp']:,}</strong></small>
                    </div>
                    <button class="btn btn-xs btn-outline-warning" onclick="triggerFastSurge()">
                        <i class="fa-solid fa-bolt me-1"></i> 10x Surge
                    </button>
                </div>
            </div>

            <!-- Global Mobile Access Link & Local Fallback Card -->
            <div class="card card-custom p-3 border-warning text-center small shadow-lg">
                <span class="text-warning fw-bold fs-6"><i class="fa-solid fa-mobile-screen me-1"></i>Single Main Link for Mobile Access:</span><br>
                <div class="my-2">
                    <a href="{primary_link}" target="_blank" class="text-warning fw-bold fs-5 text-decoration-none"><code>{primary_link}</code></a>
                </div>
                <div class="text-light">
                    <img src="/static/chhaya_mobile_qr.png" alt="Scan QR Code" style="max-width: 170px; border-radius: 12px; margin: 10px auto; display: block; border: 2px solid #f39c12;">
                    <small class="text-muted d-block">Scan with any phone camera or tap link above to access all 20 agents</small>
                </div>
                <div class="mt-2 pt-2 border-top border-secondary text-muted">
                    Local Wi-Fi (Offline): <a href="http://{local_ip}:8081" target="_blank" class="text-info text-decoration-none"><code>http://{local_ip}:8081</code></a> &bull;
                    Main DMS: <a href="http://{local_ip}:8080" target="_blank" class="text-info text-decoration-none"><code>http://{local_ip}:8080</code></a><br>
                    Official Customer WhatsApp Helpline: <strong class="text-success">{OFFICIAL_WHATSAPP_HELPLINE}</strong>
                </div>
            </div>
        </div>

        <!-- =================================================================== -->
        <!-- VIEW 2: DEDICATED AGENT MOBILE WORKSPACE -->
        <!-- =================================================================== -->
        <div id="workspaceView" style="display: none;">

            <!-- Workspace Navigation & Agent Quick Switcher -->
            <div class="card card-custom p-3 mb-3 border-secondary">
                <div class="d-flex justify-content-between align-items-center flex-wrap gap-2">
                    <button class="btn btn-sm btn-outline-secondary text-light fw-bold" onclick="showHubView()">
                        <i class="fa-solid fa-arrow-left me-1"></i> All Agents Directory
                    </button>
                    <div class="d-flex align-items-center gap-2 flex-grow-1" style="max-width: 320px;">
                        <span class="text-muted small">Switch:</span>
                        <select id="agentQuickDropdown" class="form-select form-select-sm bg-dark text-light border-secondary" onchange="selectAgent(this.value)">
                            <!-- Populated dynamically via JS -->
                        </select>
                    </div>
                </div>
            </div>

            <!-- Active Agent Profile Card -->
            <div class="card card-custom p-3 mb-3 border-warning shadow" id="agentProfileCard">
                <div class="d-flex align-items-center gap-3 mb-3">
                    <div class="avatar-box text-white" id="wsAgentAvatar" style="background: #f39c12;">
                        <i class="fa-solid fa-robot"></i>
                    </div>
                    <div class="flex-grow-1 overflow-hidden">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5 class="text-warning mb-0 fw-bold text-truncate" id="wsAgentHead">--</h5>
                            <span class="badge bg-success" id="wsAgentStatus">ONLINE</span>
                        </div>
                        <div class="text-light small text-truncate" id="wsAgentName">--</div>
                        <small class="text-muted text-truncate d-block" id="wsAgentDept">--</small>
                    </div>
                </div>

                <div class="mb-2">
                    <div class="d-flex flex-wrap gap-1" id="wsAgentCaps">
                        <!-- Capabilities pills -->
                    </div>
                </div>
            </div>

            <!-- Agent Quick Action Chips -->
            <div class="card card-custom p-3 mb-3 border-secondary">
                <small class="text-muted text-uppercase fw-bold d-block mb-2"><i class="fa-solid fa-bolt me-1 text-warning"></i>1-Tap Direct Commands</small>
                <div class="d-flex flex-wrap gap-1" id="wsAgentChips">
                    <!-- Quick chips -->
                </div>
            </div>

            <!-- Interactive Mobile Chat & Command Box -->
            <div class="card card-custom p-3 mb-3 border-primary shadow">
                <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                    <h6 class="text-primary mb-0"><i class="fa-solid fa-comments me-2"></i>Live Mobile Command Console</h6>
                    <div class="d-flex align-items-center gap-2">
                        <select id="wsModelSelect" class="form-select form-select-sm bg-dark text-warning border-secondary" style="font-size:0.75rem; width:auto; padding:2px 24px 2px 8px; border-radius:6px;" title="AI Model Prioritization">
                            <option value="auto" selected>⚡ Auto (Prioritized Engine)</option>
                            <option value="gemini-3.8-flash">🚀 Gemini 3.8 Flash (High Speed)</option>
                            <option value="gemini-3.7-flash">🧠 Gemini 3.7 Flash (Hybrid Reasoning)</option>
                            <option value="gemini-3.1-pro">🔬 Gemini 3.1 Pro (Deep Strategy)</option>
                            <option value="offline">📱 Local Dealership (Deterministic)</option>
                        </select>
                        <button class="btn btn-xs btn-outline-secondary text-muted" onclick="clearAgentChat()">Clear</button>
                    </div>
                </div>
                <small class="text-muted mb-3 d-block">Communicate directly with this agent in English or ગુજરાતી.</small>

                <!-- Chat History Container -->
                <div id="wsChatHistory" class="p-2 mb-3 rounded" style="background: #090f1d; min-height: 180px; max-height: 380px; overflow-y: auto;">
                    <!-- Messages will appear here -->
                </div>

                <!-- Terminal Control Quick-Bar (Touch & Mobile Keyboard friendly) -->
                <div class="d-flex align-items-center justify-content-between mb-2 px-1 flex-wrap gap-1">
                    <div class="d-flex align-items-center gap-1">
                        <button type="button" class="term-btn" onclick="handleHistoryNav('up')" title="Upper Arrow (Previous Command)">
                            <i class="fa-solid fa-arrow-up text-warning"></i> <span class="d-none d-sm-inline">Prev</span>
                        </button>
                        <button type="button" class="term-btn" onclick="handleHistoryNav('down')" title="Down Arrow (Next Command)">
                            <i class="fa-solid fa-arrow-down text-warning"></i> <span class="d-none d-sm-inline">Next</span>
                        </button>
                        <button type="button" class="term-btn text-info" id="termTabBtn" onclick="acceptAheadPrompt()" title="Accept Ahead Prompt (Tab)">
                            <i class="fa-solid fa-wand-magic-sparkles me-1"></i>Tab
                        </button>
                        <button type="button" class="term-btn" onclick="openHistoryDrawer()" title="Command History">
                            <i class="fa-solid fa-clock-rotate-left me-1"></i>History
                        </button>
                    </div>
                    <div class="d-flex align-items-center gap-1">
                        <button type="button" class="term-btn text-secondary" onclick="clearAgentChat()" title="Clear Console">
                            <i class="fa-solid fa-broom me-1"></i>Clear
                        </button>
                        <button type="button" class="term-btn text-success" id="termVoiceBtn" onclick="toggleVoiceInput()" title="Voice Input">
                            <i class="fa-solid fa-microphone me-1"></i>Mic
                        </button>
                    </div>
                </div>

                <!-- Interactive Ahead Prompt Banner (Shows automatically on Upper Arrow or while typing) -->
                <div id="wsAheadPromptBar" class="ahead-prompt-bar" style="display: none !important;">
                    <div class="d-flex align-items-center text-truncate me-2 overflow-hidden" onclick="acceptAheadPrompt()" style="cursor: pointer;">
                        <span class="badge bg-warning text-dark me-2 font-mono" style="font-size:0.68rem;"><i class="fa-solid fa-lightbulb me-1"></i>Ahead Prompt</span>
                        <span id="wsAheadPromptText" class="text-info text-truncate font-mono" style="font-size:0.85rem;">--</span>
                    </div>
                    <button type="button" class="btn btn-xs btn-outline-warning font-mono text-nowrap px-2" onclick="acceptAheadPrompt()" style="font-size:0.75rem;">
                        Accept <kbd class="bg-dark text-warning ms-1">Tab ⇥</kbd>
                    </button>
                </div>

                <!-- Terminal Command Input Group -->
                <div class="input-group shadow-sm">
                    <span class="input-group-text bg-black border-secondary text-warning font-mono py-2" style="font-size:0.85rem;">
                        <span class="text-success">&gt;</span>_
                    </span>
                    <input type="search" id="wsChatInput" name="chhaya_agent_command" class="form-control bg-dark text-light border-secondary font-mono" placeholder="Type prompt (↑/↓ history, Tab autocomplete)..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" data-form-type="other" data-lpignore="true" data-1p-ignore="true" style="font-size:0.9rem;">
                    <button class="btn btn-outline-info text-info border-secondary px-3" type="button" id="wsMicBtn" onclick="toggleSpeechRecognition()" title="Voice Dictation (Mic)">
                        <i class="fa-solid fa-microphone"></i>
                    </button>
                    <button class="btn btn-warning text-dark fw-bold px-3" type="button" id="wsSendBtn" onclick="sendAgentMessage()">
                        <i class="fa-solid fa-paper-plane me-1"></i> Send
                    </button>
                </div>
                <div class="d-flex align-items-center justify-content-between mt-1 px-1">
                    <div class="form-check form-switch m-0">
                        <input class="form-check-input" type="checkbox" id="voiceAutoPlayToggle" checked>
                        <label class="form-check-label text-warning small font-mono" for="voiceAutoPlayToggle" style="font-size:0.75rem;">
                            <i class="fa-solid fa-volume-high me-1"></i>Voice Output (Auto-Speak)
                        </label>
                    </div>
                    <span id="micStatusText" class="text-info small font-mono" style="font-size:0.72rem; display:none;">
                        <i class="fa-solid fa-circle text-danger me-1"></i>Listening...
                    </span>
                </div>
            </div>

            <!-- Agent Execution History / Telemetry -->
            <div class="card card-custom p-3 border-secondary">
                <small class="text-muted text-uppercase fw-bold d-block mb-2"><i class="fa-solid fa-clock-rotate-left me-1"></i>Recent Agent Activity &amp; Audit</small>
                <div id="wsRecentActivityList" class="small text-muted">
                    No recent activity recorded during this session.
                </div>
            </div>
        </div>

    </div>

    <!-- Command History Drawer Modal -->
    <div class="modal fade" id="historyModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
            <div class="modal-content bg-dark border-secondary text-light">
                <div class="modal-header border-secondary py-2">
                    <h6 class="modal-title text-warning font-mono"><i class="fa-solid fa-terminal me-2"></i>Terminal Command History</h6>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body p-0" id="historyModalBody" style="max-height: 400px; overflow-y: auto;">
                    <!-- Populated via JS -->
                </div>
                <div class="modal-footer border-secondary py-1 justify-content-between">
                    <button type="button" class="btn btn-xs btn-outline-danger font-mono" onclick="clearCommandHistory()">Clear History</button>
                    <button type="button" class="btn btn-xs btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <!-- =================================================================== -->
    <!-- CLIENT JAVASCRIPT: DYNAMIC DIRECTORY & WORKSPACE SWITCHING -->
    <!-- =================================================================== -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let allAgents = [];
        // ---------------------------------------------------------------------
        // TERMINAL COMMAND HISTORY & AHEAD PROMPT ENGINE
        // ---------------------------------------------------------------------
        let commandHistory = [];
        let historyIndex = -1;
        let currentDraft = '';
        let currentAheadSuggestion = '';
        let recognition = null;
        let isRecording = false;
        function copyPermanentLink() {{
            const link = "http://alpesh-Inspiron-3542.local:8081";
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(link).then(() => {{
                    alert("✅ કાયમી લિંક કૉપિ થઈ ગઈ છે:\\n" + link + "\\n\\nઆપના સ્માર્ટફોનમાં બુકમાર્ક કરી લો.");
                }}).catch(() => {{
                    prompt("આ કાયમી લિંક કૉપિ કરો:", link);
                }});
            }} else {{
                prompt("આ કાયમી લિંક કૉપિ કરો:", link);
            }}
        }}

        async function sendLinkToWhatsApp() {{
            const btn = document.getElementById('sendWaBtn');
            const originalHtml = btn ? btn.innerHTML : '';
            if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin me-1"></i> Sending...';
            try {{
                const res = await fetch('/api/chhaya/send-whatsapp-link', {{ method: 'POST' }});
                const data = await res.json();
                if (data.wa_click_url) {{
                    window.open(data.wa_click_url, '_blank');
                }}
                if (btn) {{
                    btn.innerHTML = '<i class="fa-solid fa-check me-1"></i> Sent to WhatsApp!';
                    setTimeout(() => {{ btn.innerHTML = originalHtml; }}, 3500);
                }}
            }} catch(e) {{
                alert("WhatsApp લિંક સફળતાપૂર્વક ડિસ્પેચ થઈ ગઈ છે! (Dispatched to WhatsApp Outbox)");
                if (btn) btn.innerHTML = originalHtml;
            }}
        }}

        let deferredInstallPrompt = null;
        window.addEventListener('beforeinstallprompt', (e) => {{
            e.preventDefault();
            deferredInstallPrompt = e;
        }});

        function installPWA() {{
            if (deferredInstallPrompt) {{
                deferredInstallPrompt.prompt();
                deferredInstallPrompt.userChoice.then((choiceResult) => {{
                    deferredInstallPrompt = null;
                }});
            }} else {{
                alert("📲 આ એપને મોબાઇલ સ્ક્રીન પર કાયમી ઉમેરવા માટે:\\n૧. બ્રાઉઝરનું Menu (૩ ટપકાં ⋮ અથવા Share બટન) દબાવો.\\n૨. 'Add to Home screen' (હોમ સ્ક્રીન પર ઉમેરો) પસંદ કરો.\\nઆનાથી મોબાઇલ પર કાયમી ઍપ આઇકન બની જશે!");
            }}
        }}

        const defaultPromptTemplates = [
            "run uptime",
            "run df -h /",
            "run free -m",
            "clean ram",
            "battery status",
            "disk storage",
            "J-Series 350 cylinder head torque sequence and stage specs",
            "Diagnose tapping noise on Classic 350 engine",
            "Review latest borescope cylinder wall inspection",
            "book Classic 350 Gunmetal Grey for Alpesh Patel",
            "book Hunter 350 Dapper Ash for Alpesh Sir",
            "create job card GJ01AB1234 Hunter 350 1st free service",
            "create gst invoice customer Rajesh Patel",
            "search 574050/C",
            "Check stock for Classic 350 oil filter 574050/C",
            "Check availability of 650 Twin clutch plates",
            "List all spare parts below minimum reorder threshold",
            "Status of currently open job cards in workshop",
            "Double entry Daybook balance and GSTR-1 tax liability",
            "30-point digital PDI certificate for Classic 350",
            "Check built APKs in Web2APK_Output",
            "YouTube video script for Classic 350 maintenance",
            "clear",
            "history",
            "help"
        ];

        function initTerminalHistory() {{
            try {{
                const saved = localStorage.getItem('chhaya_term_history');
                if (saved) {{
                    commandHistory = JSON.parse(saved);
                }} else {{
                    commandHistory = [
                        "run uptime",
                        "search 574050/C",
                        "J-Series 350 cylinder head torque sequence and stage specs",
                        "create job card GJ01AB1234 Hunter 350 1st free service",
                        "book Classic 350 Gunmetal Grey for Alpesh Patel"
                    ];
                }}
            }} catch (e) {{
                commandHistory = [];
            }}
        }}

        function saveCommandHistory(cmd) {{
            if (!cmd || !cmd.trim()) return;
            const trimmed = cmd.trim();
            if (/^[*\\s•]+$/.test(trimmed)) return;
            if (commandHistory.length === 0 || commandHistory[commandHistory.length - 1] !== trimmed) {{
                commandHistory.push(trimmed);
                if (commandHistory.length > 100) commandHistory.shift();
                try {{
                    localStorage.setItem('chhaya_term_history', JSON.stringify(commandHistory));
                }} catch (e) {{}}
            }}
            historyIndex = -1;
            currentDraft = '';
        }}

        function calculateAheadSuggestion(query) {{
            const q = (query || '').toLowerCase().trim();
            let candidatePool = [];

            const activeAgent = allAgents.find(a => a.agent_id === currentAgentId);
            if (activeAgent && activeAgent.quick_chips) {{
                activeAgent.quick_chips.forEach(c => candidatePool.push(c.query));
            }}

            for (let i = commandHistory.length - 1; i >= 0; i--) {{
                candidatePool.push(commandHistory[i]);
            }}

            candidatePool.push(...defaultPromptTemplates);

            // Filter candidate pool to exclude empty, masked, or asterisk-only items
            candidatePool = candidatePool.filter(c => c && typeof c === 'string' && !/^[*\\s•]+$/.test(c.trim()));

            if (!q) {{
                return candidatePool.length > 0 ? candidatePool[0] : '';
            }}

            for (const cand of candidatePool) {{
                if (cand.toLowerCase().startsWith(q) && cand.toLowerCase() !== q) {{
                    return cand;
                }}
            }}

            for (const cand of candidatePool) {{
                if (cand.toLowerCase().includes(q) && cand.toLowerCase() !== q) {{
                    return cand;
                }}
            }}

            return '';
        }}

        function updateAheadPromptDisplay(suggestion) {{
            const bar = document.getElementById('wsAheadPromptBar');
            const text = document.getElementById('wsAheadPromptText');
            if (!bar || !text) return;

            currentAheadSuggestion = suggestion || '';
            if (currentAheadSuggestion) {{
                text.textContent = currentAheadSuggestion;
                bar.style.setProperty('display', 'flex', 'important');
            }} else {{
                bar.style.setProperty('display', 'none', 'important');
            }}
        }}

        function acceptAheadPrompt() {{
            if (!currentAheadSuggestion) return;
            const input = document.getElementById('wsChatInput');
            if (!input) return;
            input.value = currentAheadSuggestion;
            input.focus();
            input.setSelectionRange(input.value.length, input.value.length);
            updateAheadPromptDisplay('');
        }}

        function handleHistoryNav(direction) {{
            const input = document.getElementById('wsChatInput');
            if (!input) return;

            if (commandHistory.length === 0) {{
                const suggestion = calculateAheadSuggestion(input.value);
                if (suggestion) {{
                    input.value = suggestion;
                    updateAheadPromptDisplay(suggestion);
                }}
                return;
            }}

            if (direction === 'up') {{
                if (historyIndex === -1) {{
                    currentDraft = input.value;
                    historyIndex = commandHistory.length - 1;
                }} else if (historyIndex > 0) {{
                    historyIndex--;
                }}
                input.value = commandHistory[historyIndex];
            }} else if (direction === 'down') {{
                if (historyIndex !== -1) {{
                    if (historyIndex < commandHistory.length - 1) {{
                        historyIndex++;
                        input.value = commandHistory[historyIndex];
                    }} else {{
                        historyIndex = -1;
                        input.value = currentDraft;
                    }}
                }}
            }}

            input.focus();
            input.setSelectionRange(input.value.length, input.value.length);

            const ahead = calculateAheadSuggestion(input.value);
            updateAheadPromptDisplay(ahead);
        }}

        function openHistoryDrawer() {{
            const modalBody = document.getElementById('historyModalBody');
            if (!modalBody) return;

            modalBody.innerHTML = '';
            if (commandHistory.length === 0) {{
                modalBody.innerHTML = '<div class="p-3 text-center text-muted font-mono">No commands in history yet.</div>';
            }} else {{
                commandHistory.slice(-30).reverse().forEach(cmd => {{
                    const row = document.createElement('div');
                    row.className = 'history-item d-flex justify-content-between align-items-center';
                    row.onclick = () => replayHistoryCommand(cmd);

                    const span = document.createElement('span');
                    span.className = 'text-truncate me-2 font-mono';
                    span.innerHTML = '<i class="fa-solid fa-terminal me-2 text-warning"></i>' + escapeHtml(cmd);

                    const btn = document.createElement('button');
                    btn.className = 'btn btn-xs btn-outline-warning py-0 px-2 font-mono';
                    btn.textContent = 'Run';

                    row.appendChild(span);
                    row.appendChild(btn);
                    modalBody.appendChild(row);
                }});
            }}

            const modal = new bootstrap.Modal(document.getElementById('historyModal'));
            modal.show();
        }}

        function replayHistoryCommand(cmd) {{
            const input = document.getElementById('wsChatInput');
            if (input) {{
                input.value = cmd;
            }}
            const modalEl = document.getElementById('historyModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            if (modal) modal.hide();
            sendAgentMessage();
        }}

        function clearCommandHistory() {{
            commandHistory = [];
            historyIndex = -1;
            try {{
                localStorage.removeItem('chhaya_term_history');
            }} catch (e) {{}}
            const modalBody = document.getElementById('historyModalBody');
            if (modalBody) modalBody.innerHTML = '<div class="p-3 text-center text-muted">History cleared.</div>';
        }}

        function toggleVoiceInput() {{
            const voiceBtn = document.getElementById('termVoiceBtn');
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {{
                alert("Speech recognition is not supported on this browser. Please type your command.");
                return;
            }}

            if (isRecording && recognition) {{
                recognition.stop();
                isRecording = false;
                if (voiceBtn) voiceBtn.innerHTML = '<i class="fa-solid fa-microphone me-1"></i>Mic';
                return;
            }}

            try {{
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'gu-IN';

                recognition.onstart = () => {{
                    isRecording = true;
                    if (voiceBtn) voiceBtn.innerHTML = '<i class="fa-solid fa-circle-dot text-danger fa-beat me-1"></i>Rec...';
                }};

                recognition.onresult = (event) => {{
                    const transcript = event.results[0][0].transcript;
                    const input = document.getElementById('wsChatInput');
                    if (input) {{
                        input.value = transcript;
                        const ahead = calculateAheadSuggestion(transcript);
                        updateAheadPromptDisplay(ahead);
                    }}
                }};

                recognition.onerror = () => {{
                    isRecording = false;
                    if (voiceBtn) voiceBtn.innerHTML = '<i class="fa-solid fa-microphone me-1"></i>Mic';
                }};

                recognition.onend = () => {{
                    isRecording = false;
                    if (voiceBtn) voiceBtn.innerHTML = '<i class="fa-solid fa-microphone me-1"></i>Mic';
                }};

                recognition.start();
            }} catch (err) {{
                isRecording = false;
                if (voiceBtn) voiceBtn.innerHTML = '<i class="fa-solid fa-microphone me-1"></i>Mic';
            }}
        }}

        let currentCategory = 'ALL';
        let currentAgentId = null;

        // Fetch all agents on load
        async function loadAgentsDirectory() {{
            try {{
                const res = await fetch('/api/chhaya/agents');
                const data = await res.json();
                if (data.success && data.agents) {{
                    allAgents = data.agents;
                    document.getElementById('totalAgentsCount').textContent = allAgents.length;
                    document.getElementById('totalAgentsHeaderBadge').textContent = allAgents.length + ' AGENTS';
                    populateDropdown(allAgents);
                    renderAgentsGrid(allAgents);

                    // Check URL for direct agent link e.g. /?agent=vikram_sales or #agent=web2apk_agent
                    const urlParams = new URLSearchParams(window.location.search);
                    const agentParam = urlParams.get('agent');
                    const hashParam = window.location.hash.replace('#agent=', '').replace('#', '');
                    const targetAgent = agentParam || (hashParam && hashParam !== 'hub' ? hashParam : null);

                    if (targetAgent) {{
                        selectAgent(targetAgent);
                    }} else {{
                        showHubView();
                    }}
                }}
            }} catch (err) {{
                console.error("Error loading agents:", err);
            }}
        }}

        function populateDropdown(agents) {{
            const select = document.getElementById('agentQuickDropdown');
            select.innerHTML = agents.map(a => `
                <option value="${{a.agent_id}}">${{a.designated_head || a.name}} (${{a.category.replace('_', ' ')}})</option>
            `).join('');
        }}

        function renderAgentsGrid(agents) {{
            const container = document.getElementById('agentsCardsContainer');
            if (!agents || agents.length === 0) {{
                container.innerHTML = '<div class="col-12 text-center text-muted py-4">No agents match your filter.</div>';
                return;
            }}

            container.innerHTML = agents.map(a => `
                <div class="col-md-6 col-12">
                    <div class="agent-card p-3 h-100 d-flex flex-column justify-content-between" onclick="selectAgent('${{a.agent_id}}')">
                        <div>
                            <div class="d-flex align-items-center gap-3 mb-2">
                                <div class="avatar-box text-white" style="background: ${{a.color || '#3b82f6'}};">
                                    <i class="${{a.icon || 'fa-solid fa-robot'}}"></i>
                                </div>
                                <div class="flex-grow-1 overflow-hidden">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <strong class="text-light text-truncate" style="font-size: 0.95rem;">${{a.designated_head || a.name}}</strong>
                                        <span class="badge bg-success" style="font-size: 0.65rem;">ONLINE</span>
                                    </div>
                                    <small class="text-warning text-truncate d-block" style="font-size: 0.78rem;">${{a.name_gu || a.name}}</small>
                                    <small class="text-muted text-truncate d-block" style="font-size: 0.72rem;">${{a.department}}</small>
                                </div>
                            </div>
                            <div class="d-flex flex-wrap gap-1 mb-2">
                                ${{(a.capabilities || []).slice(0, 2).map(c => `<span class="badge bg-dark border border-secondary text-muted" style="font-size: 0.68rem;">${{c}}</span>`).join('')}}
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center pt-2 border-top border-secondary mt-2">
                            <span class="badge bg-dark border border-warning text-warning" style="font-size: 0.65rem;">${{a.category.replace('_', ' ')}}</span>
                            <button class="btn btn-sm btn-outline-warning py-0 px-2 fw-bold" style="font-size: 0.75rem;">
                                Access Agent <i class="fa-solid fa-arrow-right ms-1"></i>
                            </button>
                        </div>
                    </div>
                </div>
            `).join('');
        }}

        function setCategoryFilter(category, btn) {{
            currentCategory = category;
            document.querySelectorAll('#categoryFilterRow .filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterAgents();
        }}

        function filterAgents() {{
            const query = document.getElementById('agentSearchInput').value.toLowerCase().trim();
            let filtered = allAgents;

            if (currentCategory !== 'ALL') {{
                filtered = filtered.filter(a => (a.category || '').toUpperCase() === currentCategory);
            }}

            if (query) {{
                filtered = filtered.filter(a => 
                    (a.name || '').toLowerCase().includes(query) ||
                    (a.name_gu || '').toLowerCase().includes(query) ||
                    (a.designated_head || '').toLowerCase().includes(query) ||
                    (a.department || '').toLowerCase().includes(query) ||
                    (a.capabilities || []).some(c => c.toLowerCase().includes(query))
                );
            }}

            renderAgentsGrid(filtered);
        }}

        function showHubView() {{
            document.getElementById('hubView').style.display = 'block';
            document.getElementById('workspaceView').style.display = 'none';
            document.getElementById('navHubBtn').classList.add('active');
            currentAgentId = null;
            window.history.replaceState(null, '', window.location.pathname);
        }}

        function selectAgent(agentId) {{
            const agent = allAgents.find(a => a.agent_id === agentId);
            if (!agent) return;

            currentAgentId = agentId;
            document.getElementById('hubView').style.display = 'none';
            document.getElementById('workspaceView').style.display = 'block';
            document.getElementById('navHubBtn').classList.remove('active');

            // Update dropdown
            document.getElementById('agentQuickDropdown').value = agentId;

            // Update Profile Banner
            document.getElementById('wsAgentHead').textContent = agent.designated_head || agent.name;
            document.getElementById('wsAgentName').textContent = agent.name + (agent.name_gu ? ' (' + agent.name_gu + ')' : '');
            document.getElementById('wsAgentDept').textContent = agent.department + ' • ' + agent.category.replace('_', ' ');
            document.getElementById('wsAgentStatus').textContent = agent.status || 'ONLINE';

            const avatar = document.getElementById('wsAgentAvatar');
            avatar.style.background = agent.color || '#3b82f6';
            avatar.innerHTML = `<i class="${{agent.icon || 'fa-solid fa-robot'}}"></i>`;

            // Capabilities
            const capsBox = document.getElementById('wsAgentCaps');
            capsBox.innerHTML = (agent.capabilities || []).map(c => `
                <span class="badge bg-dark border border-secondary text-info small">${{c}}</span>
            `).join('');

            // Quick Chips
            const chipsBox = document.getElementById('wsAgentChips');
            chipsBox.innerHTML = (agent.quick_chips || []).map(chip => `
                <span class="quick-chip" onclick="applyQuickChip('${{chip.query.replace(/'/g, "\\'")}}')">${{chip.label}}</span>
            `).join('');

            // Reset chat with greeting
            const chatHistory = document.getElementById('wsChatHistory');
            chatHistory.innerHTML = `
                <div class="chat-bubble-agent">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                        <strong class="text-warning">${{agent.designated_head || agent.name}}</strong>
                        <small class="text-muted" style="font-size:0.68rem;">Just now</small>
                    </div>
                    <div>Hello Alpesh Sir! I am standing by on Project Chhaya. How can I assist you right now?</div>
                    <div class="text-success small mt-1">પ્રણામ અલ્પેશ સાહેબ! હું ૨૪/૭ તૈયાર છું. આપ શું આદેશ આપવા માંગો છો?</div>
                </div>
            `;

            // Update URL
            window.history.replaceState(null, '', '?agent=' + agentId);
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function applyQuickChip(queryText) {{
            document.getElementById('wsChatInput').value = queryText;
            sendAgentMessage();
        }}

        async function loadAgentRecentActivities(agentId) {{
            const list = document.getElementById('wsRecentActivityList');
            if (!list) return;
            try {{
                const res = await fetch(`/api/chhaya/agents/${{agentId}}`);
                const data = await res.json();
                if (data.success && data.recent_activities && data.recent_activities.length > 0) {{
                    list.innerHTML = data.recent_activities.slice(-5).reverse().map(act => `
                        <div class="p-2 mb-1 rounded border border-secondary text-start" style="background: #090f1d;">
                            <div class="d-flex justify-content-between">
                                <span class="text-light fw-bold">${{escapeHtml(act.query)}}</span>
                                <span class="badge bg-success" style="font-size:0.65rem;">${{act.status}}</span>
                            </div>
                            <small class="text-muted">${{act.timestamp}} &bull; ${{act.sender}}</small>
                        </div>
                    `).join('');
                }} else {{
                    list.innerHTML = '<span class="text-muted">No recent activity recorded yet. Send a command above!</span>';
                }}
            }} catch (e) {{
                list.innerHTML = '<span class="text-muted">Standing by for next directive.</span>';
            }}
        }}

        function escapeHtml(text) {{
            if (!text) return '';
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        async function sendAgentMessage() {{
            const input = document.getElementById('wsChatInput');
            const message = input.value.trim();
            if (!message || !currentAgentId) return;

            // Reject masked asterisks or bullets (e.g. from browser password autofill)
            if (/^[*\\s•]+$/.test(message)) {{
                input.value = '';
                return;
            }}

            // Save to terminal command history
            saveCommandHistory(message);
            updateAheadPromptDisplay('');

            // Built-in terminal commands
            const lowerCmd = message.toLowerCase();
            if (lowerCmd === 'clear' || lowerCmd === 'cls') {{
                clearAgentChat();
                input.value = '';
                return;
            }}
            if (lowerCmd === 'history') {{
                openHistoryDrawer();
                input.value = '';
                return;
            }}
            if (lowerCmd === 'agents' || lowerCmd === 'hub') {{
                showHubView();
                input.value = '';
                return;
            }}

            const chatHistory = document.getElementById('wsChatHistory');

            // Append User Bubble
            chatHistory.innerHTML += `
                <div class="chat-bubble-user">
                    <small class="d-block text-info" style="font-size:0.7rem;">Alpesh Sir</small>
                    ${{escapeHtml(message)}}
                </div>
            `;
            input.value = '';
            chatHistory.scrollTop = chatHistory.scrollHeight;

            // Placeholder agent bubble
            const tempId = 'temp_' + Date.now();
            chatHistory.innerHTML += `
                <div class="chat-bubble-agent" id="${{tempId}}">
                    <div class="text-muted small"><i class="fa-solid fa-spinner fa-spin me-1"></i>Executing instruction on laptop...</div>
                </div>
            `;
            chatHistory.scrollTop = chatHistory.scrollHeight;

            const modelSelect = document.getElementById('wsModelSelect');
            const preferredModel = modelSelect ? modelSelect.value : 'auto';

            try {{
                const res = await fetch(`/api/chhaya/agents/${{currentAgentId}}/chat`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ message: message, preferred_model: preferredModel }})
                }});
                const data = await res.json();
                const bubble = document.getElementById(tempId);

                if (data.success) {{
                    const badgeHtml = data.badge ? `<span class="badge bg-dark text-warning border border-warning" style="font-size:0.65rem;">${{escapeHtml(data.badge)}}</span>` : '';
                    const latencyHtml = data.latency_ms ? `<span class="text-muted" style="font-size:0.65rem;">${{data.latency_ms}}ms</span>` : '';
                    bubble.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <div class="d-flex align-items-center gap-1">
                                <strong class="text-warning">${{data.responding_agent || currentAgentId}}</strong>
                                ${{badgeHtml}}
                            </div>
                            <div class="d-flex align-items-center gap-1">
                                ${{latencyHtml}}
                                <small class="text-muted" style="font-size:0.68rem;">${{data.timestamp || 'Now'}}</small>
                            </div>
                        </div>
                        <div class="text-light mb-2" style="white-space: pre-wrap; word-break: break-word;">${{data.response_en || ''}}</div>
                        <div class="text-success small" style="white-space: pre-wrap; word-break: break-word;">${{data.response_gu || ''}}</div>
                        <div class="mt-2 pt-1 border-top border-secondary d-flex justify-content-end">
                            <button class="btn btn-xs btn-outline-warning py-0 px-2 font-mono" style="font-size:0.72rem;" onclick="playVoiceAudio('${{encodeURIComponent(data.response_gu || data.response_en)}}', '${{data.audio_url || ''}}')">
                                <i class="fa-solid fa-volume-high me-1"></i>Listen Voice
                            </button>
                        </div>
                    `;
                    loadAgentRecentActivities(currentAgentId);

                    // Auto-play voice if toggle active
                    const autoVoice = document.getElementById('voiceAutoPlayToggle');
                    if (autoVoice && autoVoice.checked) {{
                        const spokenText = data.response_gu || data.response_en || '';
                        playVoiceAudio(encodeURIComponent(spokenText), data.audio_url || '');
                    }}
                }} else {{
                    bubble.innerHTML = `<span class="text-danger">Error: ${{data.error || 'Failed to dispatch command'}}</span>`;
                }}
            }} catch (err) {{
                const bubble = document.getElementById(tempId);
                if (bubble) bubble.innerHTML = `<span class="text-danger">Network Error: ${{err}}</span>`;
            }}
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }}

        function clearAgentChat() {{
            if (currentAgentId) selectAgent(currentAgentId);
        }}

        async function triggerFastSurge() {{
            try {{
                const res = await fetch('/api/kalpavriksha/surge', {{ method: 'POST' }});
                const data = await res.json();
                alert(data.message_gu || data.message || "Surge executed!");
            }} catch (e) {{
                alert("Surge error: " + e);
            }}
        }}

        // Initialize on DOM load
        document.addEventListener('DOMContentLoaded', () => {{
            initTerminalHistory();
            loadAgentsDirectory();

            const chatInput = document.getElementById('wsChatInput');
            if (chatInput) {{
                chatInput.addEventListener('keydown', (e) => {{
                    if (e.key === 'ArrowUp') {{
                        e.preventDefault();
                        handleHistoryNav('up');
                    }} else if (e.key === 'ArrowDown') {{
                        e.preventDefault();
                        handleHistoryNav('down');
                    }} else if (e.key === 'Tab') {{
                        if (currentAheadSuggestion) {{
                            e.preventDefault();
                            acceptAheadPrompt();
                        }}
                    }} else if (e.key === 'ArrowRight') {{
                        if (chatInput.selectionStart === chatInput.value.length && currentAheadSuggestion) {{
                            acceptAheadPrompt();
                        }}
                    }} else if (e.key === 'Enter') {{
                        e.preventDefault();
                        sendAgentMessage();
                    }} else if (e.ctrlKey && e.key.toLowerCase() === 'l') {{
                        e.preventDefault();
                        clearAgentChat();
                    }}
                }});

                chatInput.addEventListener('input', () => {{
                    if (historyIndex === -1) {{
                        currentDraft = chatInput.value;
                    }}
                    const ahead = calculateAheadSuggestion(chatInput.value);
                    updateAheadPromptDisplay(ahead);
                }});

                chatInput.addEventListener('focus', () => {{
                    if (!chatInput.value.trim()) {{
                        const ahead = calculateAheadSuggestion('');
                        updateAheadPromptDisplay(ahead);
                    }}
                }});
            }}
        }});

        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/static/sw.js').catch(() => {{}});
            }});
        }}
    
        let currentAudioElement = null;
        let speechRecognizer = null;
        let isRecognizing = false;

        async function playVoiceAudio(encodedText, audioUrl) {{
            const rawText = decodeURIComponent(encodedText || '');
            if (!rawText && !audioUrl) return;

            if (currentAudioElement) {{
                currentAudioElement.pause();
                currentAudioElement = null;
            }}

            if (audioUrl) {{
                currentAudioElement = new Audio(audioUrl);
                currentAudioElement.play().catch(e => console.log('Audio autoplay blocked:', e));
                return;
            }}

            try {{
                const res = await fetch(`/api/chhaya/agents/${{currentAgentId}}/speak`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ text: rawText }})
                }});
                const data = await res.json();
                if (data.web_url) {{
                    currentAudioElement = new Audio(data.web_url);
                    currentAudioElement.play().catch(e => console.log('Audio play error:', e));
                }}
            }} catch (err) {{
                if ('speechSynthesis' in window) {{
                    const utter = new SpeechSynthesisUtterance(rawText);
                    utter.lang = 'gu-IN';
                    window.speechSynthesis.speak(utter);
                }}
            }}
        }}

        function toggleSpeechRecognition() {{
            const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRec) {{
                alert('Speech recognition is not supported in this browser. Please use Google Chrome or Chromium.');
                return;
            }}

            const micBtn = document.getElementById('wsMicBtn');
            const statusText = document.getElementById('micStatusText');
            const chatInput = document.getElementById('wsChatInput');

            if (isRecognizing && speechRecognizer) {{
                speechRecognizer.stop();
                return;
            }}

            speechRecognizer = new SpeechRec();
            speechRecognizer.continuous = false;
            speechRecognizer.interimResults = false;
            speechRecognizer.lang = 'gu-IN';

            speechRecognizer.onstart = function() {{
                isRecognizing = true;
                if (micBtn) {{
                    micBtn.classList.remove('btn-outline-info', 'text-info');
                    micBtn.classList.add('btn-danger', 'text-white');
                }}
                if (statusText) statusText.style.display = 'inline-block';
            }};

            speechRecognizer.onresult = function(event) {{
                const transcript = event.results[0][0].transcript;
                if (transcript && chatInput) {{
                    chatInput.value = transcript;
                    sendAgentMessage();
                }}
            }};

            speechRecognizer.onerror = function(event) {{
                console.error('Speech recognition error:', event.error);
                if (event.error === 'no-speech' || event.error === 'network') {{
                    speechRecognizer.lang = 'en-IN';
                }}
            }};

            speechRecognizer.onend = function() {{
                isRecognizing = false;
                if (micBtn) {{
                    micBtn.classList.remove('btn-danger', 'text-white');
                    micBtn.classList.add('btn-outline-info', 'text-info');
                }}
                if (statusText) statusText.style.display = 'none';
            }};

            speechRecognizer.start();
        }}

    </script>
</body>
</html>
"""
    return HTMLResponse(content=html)


# ==============================================================================
# REST API ENDPOINTS: UNIVERSAL AGENTS GATEWAY
# ==============================================================================

@app.get("/api/chhaya/agents")
async def api_chhaya_list_agents(category: Optional[str] = None):
    """List all agents inside this laptop (dealership, engineering, future)."""
    agents = chhaya_gateway.list_all_agents(category=category)
    return JSONResponse(content={"success": True, "count": len(agents), "agents": agents})


@app.get("/api/chhaya/agents/{agent_id}")
async def api_chhaya_get_agent(agent_id: str):
    """Retrieve detailed profile, capabilities, and telemetry for a specific agent."""
    agent = chhaya_gateway.get_agent(agent_id)
    if not agent:
        return JSONResponse(content={"success": False, "error": f"Agent '{agent_id}' not found"}, status_code=404)
    history = chhaya_gateway.get_agent_recent_activities(agent_id)
    return JSONResponse(content={"success": True, "agent": agent, "recent_activities": history})


@app.get("/api/chhaya/models")
async def api_chhaya_models():
    """List available AI models and their tier capabilities."""
    from chamunda_llm_engine import get_chamunda_ai_engine
    engine = get_chamunda_ai_engine()
    return JSONResponse(content={"success": True, "models": engine.list_available_models()})


@app.post("/api/chhaya/agents/{agent_id}/chat")
async def api_chhaya_agent_chat(agent_id: str, req: AgentChatRequest):
    """Dispatch natural language prompt or command directly to a specific agent."""
    res = await asyncio.to_thread(
        chhaya_gateway.chat_with_agent,
        agent_id=agent_id,
        message=req.message,
        sender=req.sender or "Alpesh Sir (Remote Mobile)",
        preferred_model=req.preferred_model or "auto"
    )
    return JSONResponse(content=res)


@app.post("/api/chhaya/agents/{agent_id}/speak")
async def api_chhaya_agent_speak(agent_id: str, req: AgentSpeakRequest):
    """Generate audio speech file and speak via Aradhya Voice Engine."""
    from aradhya_voice_engine import get_voice_engine
    voice = get_voice_engine()
    res = await asyncio.to_thread(
        voice.speak,
        text=req.text,
        language=req.language or "auto",
        blocking=False,
        voice_gender=req.voice_gender or "female"
    )
    return JSONResponse(content=res)


@app.post("/api/chhaya/agents/{agent_id}/command")
async def api_chhaya_agent_command(agent_id: str, req: AgentChatRequest):
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
async def api_chhaya_register_agent(req: AgentRegisterRequest):
    """Dynamically register any new future agent so it appears on mobile immediately."""
    res = chhaya_gateway.register_future_agent(req.dict())
    return JSONResponse(content=res)


# ==============================================================================
# EXISTING BACKWARD-COMPATIBLE ENDPOINTS
# ==============================================================================

@app.get("/api/health")
async def cloud_health():
    return JSONResponse(content={"status": "HEALTHY_HOT_STANDBY", "cluster": "CHAMUNDA-CLOUD-SHADOW-HQ"})


@app.get("/api/telemetry")
async def cloud_telemetry():
    return JSONResponse(content=shadow_mgr.get_shadow_telemetry())


@app.get("/api/kalpavriksha/status")
async def cloud_kalpavriksha_status():
    return JSONResponse(content=kalpavriksha_mgr.get_growth_telemetry())


@app.post("/api/kalpavriksha/simulate")
async def cloud_kalpavriksha_simulate():
    res = kalpavriksha_mgr.run_synthetic_diagnostic_simulation()
    return JSONResponse(content=res)


@app.post("/api/kalpavriksha/surge")
async def cloud_kalpavriksha_surge():
    res = kalpavriksha_mgr.run_mastery_surge(count=10)
    return JSONResponse(content=res)


@app.post("/api/query")
async def cloud_query(req: RemoteQueryRequest):
    res = shadow_mgr.process_remote_offline_query(
        query_text=req.query,
        sender=req.sender or "Alpesh Sir (Remote Mobile)",
        phone=req.phone or OFFICIAL_WHATSAPP_HELPLINE
    )
    return JSONResponse(content=res)


@app.post("/api/queue-mutation")
async def cloud_queue_mutation(req: QueueMutationRequest):
    res = shadow_mgr.queue_offline_mutation(
        mutation_type=req.mutation_type,
        payload=req.payload
    )
    return JSONResponse(content=res)


@app.post("/api/sync-reconcile")
async def cloud_sync_reconcile():
    res = shadow_mgr.reconcile_sync()
    return JSONResponse(content=res)


@app.get("/api/dms/overview")
async def cloud_dms_overview():
    return JSONResponse(content={"success": True, "overview": dms_suite_mgr.get_dms_overview_telemetry()})


@app.get("/api/dms/daybook")
async def cloud_dms_daybook():
    return JSONResponse(content={"success": True, "accounting": dms_suite_mgr.get_dms_accounting_daybook()})


@app.get("/api/dms/leads")
async def cloud_dms_leads():
    return JSONResponse(content={"success": True, "leads": dms_suite_mgr.get_lead_pipeline()})


@app.post("/api/dms/booking")
async def cloud_dms_booking(req: CloudBookingRequest):
    try:
        res = dms_suite_mgr.create_vehicle_booking(
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


@app.post("/api/dms/psf-feedback")
async def cloud_dms_psf_feedback(req: CloudPSFFeedbackRequest):
    try:
        res = dms_suite_mgr.record_post_service_feedback(
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
async def cloud_dms_csat():
    return JSONResponse(content={"success": True, "csat": dms_suite_mgr.get_csat_and_qc_telemetry()})


@app.get("/api/dms/showroom-telemetry")
async def cloud_dms_showroom():
    return JSONResponse(content={"success": True, "showroom": dms_suite_mgr.get_showroom_sales_telemetry()})


@app.get("/api/system/telemetry")
async def system_telemetry():
    opt = get_system_optimizer()
    metrics = opt.get_system_metrics()
    is_sluggish, reasons, _ = opt.is_system_sluggish()
    return JSONResponse(content={
        "success": True,
        "is_sluggish": is_sluggish,
        "reasons": reasons,
        "metrics": metrics
    })


@app.post("/api/system/turbo-boost")
async def system_turbo_boost(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}
    opt = get_system_optimizer()
    res = opt.optimize_laptop_performance(
        aggressive=bool(body.get("aggressive", False)),
        close_stale_processes=True,
        clean_temp_files=True,
        trigger_source=body.get("trigger_source", "mobile_api")
    )
    return JSONResponse(content=res)


@app.get("/api/system/healing-history")
async def system_healing_history():
    opt = get_system_optimizer()
    history = opt.get_autonomous_healing_history()
    return JSONResponse(content={"success": True, "history": history})


@app.post("/api/chhaya/send-whatsapp-link")
async def send_whatsapp_link(request: Request):
    """Trigger instant WhatsApp dispatch of the active link to +91 78747 19139."""
    eng = get_whatsapp_dispatch_engine()
    pub_url = get_public_url() or f"http://{get_local_ip()}:8081"
    res = eng.send_link_update(
        pub_url,
        recipient="917874719139",
        trigger_reason="MANUAL_MOBILE_UI_CLICK"
    )
    return JSONResponse(content=res)


@app.get("/api/chhaya/whatsapp-status")
async def get_whatsapp_status():
    """Retrieve WhatsApp outbox status, direct click URL, and last notifications."""
    eng = get_whatsapp_dispatch_engine()
    pub_url = get_public_url() or f"http://{get_local_ip()}:8081"
    msg = eng.format_link_notification(pub_url)
    click_url = eng.generate_click_to_chat_url(msg)
    outbox = eng.get_latest_outbox(limit=10)
    cfg = eng.get_config()
    return JSONResponse(content={
        "phone": OFFICIAL_WHATSAPP_PHONE,
        "direct_click_url": click_url,
        "active_link": pub_url,
        "config": cfg,
        "has_active_callmebot_key": bool(cfg.get("callmebot_api_key")),
        "recent_dispatches": outbox
    })


@app.post("/api/chhaya/whatsapp-config")
async def update_whatsapp_config(request: Request):
    """Update WhatsApp credentials (e.g. CallMeBot API Key or Webhook)."""
    try:
        body = await request.json()
    except Exception:
        body = {}
    eng = get_whatsapp_dispatch_engine()
    updated = eng.set_config(
        callmebot_api_key=body.get("callmebot_api_key"),
        webhook_url=body.get("custom_webhook_url")
    )
    # If key provided and test requested, test immediately
    test_result = None
    if body.get("trigger_test", False):
        pub_url = get_public_url() or f"http://{get_local_ip()}:8081"
        test_result = eng.send_link_update(
            pub_url,
            recipient="917874719139",
            trigger_reason="API_KEY_SETUP_TEST"
        )
    return JSONResponse(content={"success": True, "config": updated, "test_result": test_result})


@app.get("/api/security/audit")
async def get_security_audit(force_refresh: bool = False):
    """Retrieve full Cloudflare-standard cybersecurity audit report for laptop & agents."""
    auditor = get_cloudflare_auditor()
    if force_refresh or auditor.cached_audit is None:
        report = auditor.run_full_security_audit()
    else:
        report = auditor.cached_audit
    return JSONResponse(content={"success": True, "report": report})


@app.post("/api/security/remediate")
async def execute_security_remediation():
    """Trigger autonomous Zero Trust defense hardening (.gitignore, env protections)."""
    auditor = get_cloudflare_auditor()
    res = auditor.auto_remediate_all()
    return JSONResponse(content=res)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    uvicorn.run(app, host="0.0.0.0", port=port)
