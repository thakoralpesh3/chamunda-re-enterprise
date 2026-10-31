# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
Aradhya Autonomous Remote PC Access Router & Mobile Companion Web App
Author: Aradhya (CEO), reporting exclusively to Alpesh Sir (Founder, Chairman & Master Tech)

Provides Antigravity-Style Remote PC Access from any Smartphone or Tablet:
1. /remote - Dedicated Touch-Friendly Remote PC Mobile Web App
2. Interactive Web Terminal with bash execution
3. Live PC Screen Capture & Screenshot Viewer
4. Hardware Controls: Screen Lock, Volume, Mute, Turbo Boost, Battery
5. Remote Workspace File Explorer & Code Viewer
6. Top Processes & Task Manager
"""

import os
import sys
import time
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path("/home/alpesh/chamunda_re_enterprise")
sys.path.insert(0, str(BASE_DIR))

from aradhya_remote_controller import get_remote_controller

router = APIRouter(tags=["Remote PC Access"])


# -----------------------------------------------------------------------------
# Request Models
# -----------------------------------------------------------------------------

class RemoteCommandRequest(BaseModel):
    command: str
    cwd: Optional[str] = "/home/alpesh"

class RemoteVolumeRequest(BaseModel):
    volume: Optional[int] = None
    mute_toggle: Optional[bool] = False

class RemoteFileRequest(BaseModel):
    path: Optional[str] = "/home/alpesh"

class RemoteKillRequest(BaseModel):
    pid: int

class RemoteTaskRequest(BaseModel):
    directive: str
    preferred_model: Optional[str] = "auto"
    max_steps: Optional[int] = 8


# -----------------------------------------------------------------------------
# REST API Endpoints
# -----------------------------------------------------------------------------

@router.post("/api/remote/task")
async def api_remote_task(req: RemoteTaskRequest):
    """
    Execute an autonomous multi-step mission like Antigravity.
    Executes Python scripts, shell commands, code verification, self-healing,
    and returns deliverable artifacts and step telemetry.
    """
    from aradhya_autonomous_core import get_aradhya_engine
    core = get_aradhya_engine()
    res = await asyncio.to_thread(
        core.execute_mission,
        mission_directive=req.directive,
        preferred_model=req.preferred_model or "auto",
        max_steps=req.max_steps or 8
    )
    return JSONResponse(content=res)


@router.get("/api/remote/status")
async def api_remote_status():
    """Retrieve full live hardware & OS telemetry."""
    ctrl = get_remote_controller()
    telemetry = await asyncio.to_thread(ctrl.get_pc_telemetry)
    return JSONResponse(content=telemetry)


@router.post("/api/remote/terminal")
async def api_remote_terminal(req: RemoteCommandRequest):
    """Execute a shell command on the PC and return terminal stdout/stderr."""
    ctrl = get_remote_controller()
    res = await asyncio.to_thread(ctrl.execute_terminal_command, req.command, req.cwd)
    return JSONResponse(content=res)


@router.get("/api/remote/screenshot")
@router.post("/api/remote/screenshot")
async def api_remote_screenshot():
    """Capture live PC screen and return relative image URL."""
    ctrl = get_remote_controller()
    res = await asyncio.to_thread(ctrl.capture_screen)
    return JSONResponse(content=res)


@router.post("/api/remote/lock")
async def api_remote_lock():
    """Lock the laptop display for privacy & security."""
    ctrl = get_remote_controller()
    res = await asyncio.to_thread(ctrl.lock_pc_screen)
    return JSONResponse(content=res)


@router.post("/api/remote/volume")
async def api_remote_volume(req: RemoteVolumeRequest):
    """Adjust master volume or toggle mute."""
    ctrl = get_remote_controller()
    if req.mute_toggle:
        res = await asyncio.to_thread(ctrl.toggle_mute)
    elif req.volume is not None:
        res = await asyncio.to_thread(ctrl.set_volume, req.volume)
    else:
        res = {"success": True, "volume": ctrl._get_current_volume()}
    return JSONResponse(content=res)


@router.post("/api/remote/files")
async def api_remote_files(req: RemoteFileRequest):
    """List directory contents for remote file explorer."""
    ctrl = get_remote_controller()
    res = await asyncio.to_thread(ctrl.list_directory, req.path or "/home/alpesh")
    return JSONResponse(content=res)


@router.post("/api/remote/file-view")
async def api_remote_file_view(req: RemoteFileRequest):
    """Read text file preview safely."""
    ctrl = get_remote_controller()
    res = await asyncio.to_thread(ctrl.read_file_preview, req.path or "/home/alpesh")
    return JSONResponse(content=res)


@router.get("/api/remote/processes")
async def api_remote_processes(limit: int = 15):
    """List top running processes."""
    ctrl = get_remote_controller()
    procs = await asyncio.to_thread(ctrl.get_top_processes, limit)
    return JSONResponse(content={"success": True, "processes": procs})


# -----------------------------------------------------------------------------
# Mobile Web Companion HTML UI (/remote)
# -----------------------------------------------------------------------------

@router.get("/remote", response_class=HTMLResponse)
async def remote_pc_dashboard():
    """Render the touch-friendly Remote PC Companion App."""
    html_content = """<!DOCTYPE html>
<html lang="gu">
<head>
    <meta charset="UTF-8">
    <title>Aradhya Remote PC • Antigravity Mobile Access</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <meta name="theme-color" content="#0d1117">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-color: #090d16;
            --card-bg: #111827;
            --border-color: #1f2937;
            --cyan-accent: #06b6d4;
            --gold-accent: #f59e0b;
            --green-accent: #10b981;
            --red-accent: #ef4444;
        }
        body {
            background-color: var(--bg-color);
            color: #f3f4f6;
            font-family: system-ui, -apple-system, sans-serif;
            padding-bottom: 70px;
            user-select: none;
        }
        .header-bar {
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 12px 16px;
        }
        .nav-tabs .nav-link {
            color: #9ca3af;
            border: none;
            border-bottom: 2px solid transparent;
            font-size: 0.88rem;
            font-weight: 600;
            padding: 8px 12px;
        }
        .nav-tabs .nav-link.active {
            color: var(--cyan-accent);
            background: transparent;
            border-bottom: 2px solid var(--cyan-accent);
        }
        .card-custom {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
        }
        .telemetry-chip {
            background: #1f2937;
            border-radius: 8px;
            padding: 8px 12px;
            border: 1px solid #374151;
        }
        /* Web Terminal Styles */
        .terminal-window {
            background: #030712;
            border: 1px solid #1f2937;
            border-radius: 10px;
            font-family: monospace;
            padding: 12px;
            height: 380px;
            overflow-y: auto;
            color: #a7f3d0;
            font-size: 0.85rem;
            white-space: pre-wrap;
            word-break: break-all;
        }
        .terminal-prompt {
            color: var(--cyan-accent);
            font-weight: bold;
        }
        .quick-cmd-btn {
            background: #1f2937;
            border: 1px solid #374151;
            color: #e5e7eb;
            font-size: 0.78rem;
            border-radius: 16px;
            padding: 4px 10px;
            white-space: nowrap;
        }
        .quick-cmd-btn:hover, .quick-cmd-btn:active {
            background: var(--cyan-accent);
            color: #000;
        }
        /* Screen Viewer */
        .screen-preview-img {
            width: 100%;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        /* File Explorer Item */
        .file-item {
            padding: 8px 10px;
            border-bottom: 1px solid #1f2937;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .file-item:hover, .file-item:active {
            background: #1f2937;
        }
    </style>
</head>
<body>

    <!-- Header Bar -->
    <div class="header-bar d-flex justify-content-between align-items-center">
        <div>
            <div class="d-flex align-items-center gap-2">
                <span class="badge bg-info text-dark fw-bold">ARADHYA REMOTE</span>
                <span class="badge bg-dark border border-success text-success"><i class="fa-solid fa-circle me-1" style="font-size:0.5rem;"></i>PC CONNECTED</span>
            </div>
            <small class="text-muted d-block" id="hostTitle" style="font-size:0.75rem;">Connecting to workshop laptop...</small>
        </div>
        <div class="d-flex gap-2">
            <button class="btn btn-sm btn-outline-danger" onclick="lockPC()" title="Lock Screen">
                <i class="fa-solid fa-lock"></i>
            </button>
            <a href="/" class="btn btn-sm btn-outline-warning" title="Return to Hub">
                <i class="fa-solid fa-home"></i>
            </a>
        </div>
    </div>

    <div class="container-fluid px-3 pt-2">

        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs mb-3" id="remoteTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="term-tab" data-bs-toggle="tab" data-bs-target="#tab-terminal" type="button">
                    <i class="fa-solid fa-terminal me-1"></i>Terminal
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="tasks-tab" data-bs-toggle="tab" data-bs-target="#tab-tasks" type="button">
                    <i class="fa-solid fa-wand-magic-sparkles me-1 text-warning"></i>Autonomous Tasks
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="screen-tab" data-bs-toggle="tab" data-bs-target="#tab-screen" type="button" onclick="refreshScreenshot()">
                    <i class="fa-solid fa-desktop me-1"></i>Screen
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="hardware-tab" data-bs-toggle="tab" data-bs-target="#tab-hardware" type="button" onclick="refreshHardware()">
                    <i class="fa-solid fa-sliders me-1"></i>Controls
                </button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="files-tab" data-bs-toggle="tab" data-bs-target="#tab-files" type="button" onclick="loadFiles()">
                    <i class="fa-solid fa-folder me-1"></i>Files
                </button>
            </li>
        </ul>

        <!-- TAB 1: TERMINAL -->
        <div class="tab-content" id="remoteTabContent">
            <div class="tab-pane fade show active" id="tab-terminal" role="tabpanel">
                <div class="card card-custom p-2 mb-2">
                    <!-- Quick Commands -->
                    <div class="d-flex gap-1 overflow-auto pb-2 mb-1">
                        <button class="quick-cmd-btn" onclick="sendQuickCommand('git status')">git status</button>
                        <button class="quick-cmd-btn" onclick="sendQuickCommand('df -h /')">df -h</button>
                        <button class="quick-cmd-btn" onclick="sendQuickCommand('free -m')">free -m</button>
                        <button class="quick-cmd-btn" onclick="sendQuickCommand('uptime')">uptime</button>
                        <button class="quick-cmd-btn" onclick="sendQuickCommand('systemctl --user status chamunda-chhaya.service --no-pager')">chhaya status</button>
                        <button class="quick-cmd-btn" onclick="clearTerminal()">clear</button>
                    </div>

                    <!-- Terminal Output Window -->
                    <div class="terminal-window" id="terminalOutput">
[Aradhya Remote Shell v1.0]
Host: alpesh-Inspiron-3542 (Linux Mint)
Type commands below or use quick chips above.
                    </div>

                    <!-- Input Box -->
                    <div class="input-group mt-2">
                        <span class="input-group-text bg-dark border-secondary text-info font-mono">$</span>
                        <input type="text" id="terminalInput" class="form-control bg-dark text-light border-secondary font-mono" placeholder="Enter shell command (e.g. ls -la)..." onkeydown="if(event.key==='Enter') executeCommand()">
                        <button class="btn btn-info fw-bold" onclick="executeCommand()">
                            <i class="fa-solid fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- TAB: AUTONOMOUS TASKS (ANTIGRAVITY PARITY) -->
            <div class="tab-pane fade" id="tab-tasks" role="tabpanel">
                <div class="card card-custom p-3 mb-3 border-warning">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="text-warning mb-0 fw-bold">
                            <i class="fa-solid fa-wand-magic-sparkles me-2"></i>Antigravity Autonomous Task Engine
                        </h6>
                        <span class="badge bg-warning text-dark font-mono">Plan • Act • Verify</span>
                    </div>
                    <p class="text-muted small mb-2">
                        Give Aradhya a high-level task directive from your phone. She writes code, executes tools, tests herself, auto-fixes bugs, and produces verified deliverables.
                    </p>

                    <!-- Quick Task Directives -->
                    <div class="d-flex gap-1 overflow-auto pb-2 mb-2">
                        <button class="quick-cmd-btn" onclick="setTaskDirective('Analyze battery drain and top 5 RAM consumers, then optimize laptop')">⚡ System Diagnostic</button>
                        <button class="quick-cmd-btn" onclick="setTaskDirective('Audit disk space in /home/alpesh and list top 10 largest files')">📂 Storage Audit</button>
                        <button class="quick-cmd-btn" onclick="setTaskDirective('Check all active git repositories status and uncommitted changes')">🌿 Git Scan</button>
                        <button class="quick-cmd-btn" onclick="setTaskDirective('Create a monthly Royal Enfield sales performance chart and export PNG')">📊 Sales Chart</button>
                    </div>

                    <!-- Task Input Group -->
                    <div class="mb-2">
                        <textarea id="taskDirectiveInput" class="form-control bg-dark text-light border-secondary font-mono" rows="2" placeholder="Describe task to complete autonomously (e.g., 'Check database health, clean RAM, and summarize in Gujarati')..."></textarea>
                    </div>

                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center gap-2">
                            <span class="text-muted small">Model:</span>
                            <select id="taskModelSelect" class="form-select form-select-sm bg-dark text-light border-secondary" style="width: auto;">
                                <option value="auto" selected>Auto (Hybrid Gemini + Local)</option>
                                <option value="gemini-4-argon">Gemini 4 Argon (Frontier)</option>
                                <option value="gemini-3.5-flash">Gemini 3.5 Flash</option>
                                <option value="offline">100% Offline Cognitive Matrix</option>
                            </select>
                        </div>
                        <button class="btn btn-warning fw-bold text-dark px-3" id="launchTaskBtn" onclick="launchAutonomousTask()">
                            <i class="fa-solid fa-rocket me-1"></i> Execute Task
                        </button>
                    </div>
                </div>

                <!-- Live Task Execution Telemetry Box -->
                <div class="card card-custom p-3 border-secondary" id="taskTelemetryCard" style="display:none;">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="text-info font-mono small fw-bold" id="taskStatusBadge">
                            <i class="fa-solid fa-spinner fa-spin me-1"></i> EXECUTING AUTONOMOUS WORKER...
                        </span>
                        <span class="badge bg-secondary font-mono" id="taskTimeElapsed">0s</span>
                    </div>

                    <div class="terminal-window mb-2" id="taskExecutionConsole" style="height: 220px; font-size: 0.82rem;">
Initializing Autonomous Agent Environment...
                    </div>

                    <div id="taskDeliverablesBox" class="mt-2" style="display:none;">
                        <h6 class="text-success small fw-bold"><i class="fa-solid fa-folder-check me-1"></i>Artifacts & Deliverables Created:</h6>
                        <ul id="taskArtifactsList" class="small text-light mb-2 ps-3 font-mono"></ul>
                    </div>

                    <div id="taskSummaryBox" class="mt-2 p-2 rounded bg-dark border border-secondary" style="display:none;">
                        <h6 class="text-warning small fw-bold mb-1"><i class="fa-solid fa-file-lines me-1"></i>Executive Resolution:</h6>
                        <div id="taskSummaryGu" class="small text-info mb-1"></div>
                        <div id="taskSummaryEn" class="small text-light"></div>
                    </div>
                </div>
            </div>

            <!-- TAB 2: SCREEN VIEWER -->
            <div class="tab-pane fade" id="tab-screen" role="tabpanel">
                <div class="card card-custom p-3 text-center mb-2">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0 text-info"><i class="fa-solid fa-eye me-1"></i>Live PC Screen</h6>
                        <button class="btn btn-sm btn-outline-info" onclick="refreshScreenshot()">
                            <i class="fa-solid fa-rotate me-1"></i>Capture Now
                        </button>
                    </div>
                    <div id="screenContainer">
                        <img src="/static/screenshot_live.png" id="screenImg" class="screen-preview-img" alt="PC Screen" onclick="openFullImage()">
                    </div>
                    <small class="text-muted d-block mt-2" id="screenMeta" style="font-size:0.75rem;">Tap image to view full screen.</small>
                </div>
            </div>

            <!-- TAB 3: CONTROLS & HARDWARE -->
            <div class="tab-pane fade" id="tab-hardware" role="tabpanel">
                <!-- Telemetry Row -->
                <div class="row g-2 mb-3">
                    <div class="col-6 col-md-3">
                        <div class="telemetry-chip text-center">
                            <small class="text-muted d-block">CPU</small>
                            <span class="fw-bold text-info fs-5" id="cpuStat">--%</span>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="telemetry-chip text-center">
                            <small class="text-muted d-block">RAM</small>
                            <span class="fw-bold text-warning fs-5" id="ramStat">--%</span>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="telemetry-chip text-center">
                            <small class="text-muted d-block">Battery</small>
                            <span class="fw-bold text-success fs-5" id="batStat">--%</span>
                        </div>
                    </div>
                    <div class="col-6 col-md-3">
                        <div class="telemetry-chip text-center">
                            <small class="text-muted d-block">Disk Usage</small>
                            <span class="fw-bold text-light fs-5" id="diskStat">--%</span>
                        </div>
                    </div>
                </div>

                <!-- Hardware Control Actions -->
                <div class="card card-custom p-3 mb-3">
                    <h6 class="text-warning mb-3"><i class="fa-solid fa-sliders me-1"></i>Hardware Controls</h6>

                    <!-- Volume Control -->
                    <div class="mb-3">
                        <label class="form-label text-muted small d-flex justify-content-between">
                            <span>Speaker Volume</span>
                            <span id="volLabel">75%</span>
                        </label>
                        <div class="d-flex align-items-center gap-2">
                            <button class="btn btn-sm btn-outline-secondary" onclick="toggleMute()">
                                <i class="fa-solid fa-volume-xmark" id="muteIcon"></i>
                            </button>
                            <input type="range" class="form-range" id="volumeSlider" min="0" max="100" value="75" onchange="setVolume(this.value)">
                        </div>
                    </div>

                    <!-- Action Buttons -->
                    <div class="d-grid gap-2">
                        <button class="btn btn-outline-danger fw-bold" onclick="lockPC()">
                            <i class="fa-solid fa-lock me-1"></i> Lock PC Screen Immediately
                        </button>
                        <button class="btn btn-outline-warning fw-bold" onclick="runTurboBoost()">
                            <i class="fa-solid fa-bolt me-1"></i> Speed Boost & Clean RAM
                        </button>
                    </div>
                </div>

                <!-- Running Processes -->
                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="text-info mb-0"><i class="fa-solid fa-microchip me-1"></i>Top Processes</h6>
                        <button class="btn btn-sm btn-outline-secondary" onclick="loadProcesses()"><i class="fa-solid fa-rotate"></i></button>
                    </div>
                    <div id="processList" class="small" style="max-height: 200px; overflow-y:auto;">
                        Loading processes...
                    </div>
                </div>
            </div>

            <!-- TAB 4: FILE EXPLORER -->
            <div class="tab-pane fade" id="tab-files" role="tabpanel">
                <div class="card card-custom p-3">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="text-info mb-0 text-truncate" id="currentDirLabel" style="max-width: 70%;">/home/alpesh</h6>
                        <button class="btn btn-sm btn-outline-secondary" onclick="navigateParent()">
                            <i class="fa-solid fa-level-up-alt me-1"></i>Up
                        </button>
                    </div>
                    <div id="fileExplorerList" style="max-height: 450px; overflow-y:auto;">
                        Loading directory...
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- File View Modal -->
    <div class="modal fade" id="fileModal" tabindex="-1">
        <div class="modal-dialog modal-dialog-scrollable modal-lg">
            <div class="modal-content bg-dark text-light border-secondary">
                <div class="modal-header border-secondary">
                    <h6 class="modal-title text-info" id="fileModalTitle">File Preview</h6>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body font-mono small" style="background:#030712; max-height: 400px; overflow:auto;">
                    <pre id="fileModalContent" class="m-0 text-light" style="white-space: pre-wrap;"></pre>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentPath = "/home/alpesh";
        let parentPath = "/home";

        async function fetchStatus() {
            try {
                const res = await fetch('/api/remote/status');
                const data = await res.json();
                if (data.success) {
                    document.getElementById('hostTitle').innerText = `${data.hostname} • ${data.os} • Uptime: ${data.uptime}`;
                    document.getElementById('cpuStat').innerText = `${data.cpu.percent}%`;
                    document.getElementById('ramStat').innerText = `${data.memory.percent_used}%`;
                    document.getElementById('batStat').innerText = `${data.battery.percent}% ${data.battery.power_plugged ? '⚡' : ''}`;
                    document.getElementById('diskStat').innerText = `${data.disk.percent_used}%`;
                }
            } catch(e) {
                console.error(e);
            }
        }

        async function executeCommand() {
            const input = document.getElementById('terminalInput');
            const cmd = input.value.trim();
            if (!cmd) return;
            input.value = '';

            const term = document.getElementById('terminalOutput');
            term.innerHTML += `\\n<span class="terminal-prompt">$ ${cmd}</span>\\n`;
            term.scrollTop = term.scrollHeight;

            try {
                const res = await fetch('/api/remote/terminal', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command: cmd, cwd: currentPath})
                });
                const data = await res.json();
                term.innerHTML += escapeHtml(data.output) + '\\n';
                term.scrollTop = term.scrollHeight;
            } catch(e) {
                term.innerHTML += `<span class="text-danger">Error: ${e}</span>\\n`;
            }
        }

        function sendQuickCommand(cmd) {
            document.getElementById('terminalInput').value = cmd;
            executeCommand();
        }

        function clearTerminal() {
            document.getElementById('terminalOutput').innerHTML = '[Terminal Cleared]\\n';
        }

        async function refreshScreenshot() {
            const meta = document.getElementById('screenMeta');
            meta.innerText = 'Capturing live desktop...';
            try {
                const res = await fetch('/api/remote/screenshot');
                const data = await res.json();
                if (data.success) {
                    document.getElementById('screenImg').src = data.url;
                    meta.innerText = `Captured: ${data.timestamp} (${data.size_kb} KB)`;
                } else {
                    meta.innerText = 'Failed to capture screenshot.';
                }
            } catch(e) {
                meta.innerText = 'Screenshot error: ' + e;
            }
        }

        function openFullImage() {
            const img = document.getElementById('screenImg');
            window.open(img.src, '_blank');
        }

        async function lockPC() {
            if (!confirm('Lock laptop screen now?')) return;
            try {
                const res = await fetch('/api/remote/lock', {method: 'POST'});
                const data = await res.json();
                alert(data.message || 'Screen locked.');
            } catch(e) {
                alert('Error locking PC: ' + e);
            }
        }

        async function setVolume(val) {
            document.getElementById('volLabel').innerText = val + '%';
            try {
                await fetch('/api/remote/volume', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({volume: parseInt(val)})
                });
            } catch(e) {}
        }

        async function toggleMute() {
            try {
                await fetch('/api/remote/volume', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({mute_toggle: true})
                });
            } catch(e) {}
        }

        async function runTurboBoost() {
            try {
                const res = await fetch('/api/system/turbo-boost', {method: 'POST'});
                const data = await res.json();
                alert('⚡ Turbo Boost complete! Freed RAM: ' + (data.freed_memory_mb || 0).toFixed(1) + ' MB');
                fetchStatus();
            } catch(e) {
                alert('Turbo boost failed: ' + e);
            }
        }

        async function loadFiles(path = currentPath) {
            const container = document.getElementById('fileExplorerList');
            container.innerHTML = '<div class="text-muted p-2">Loading directory...</div>';
            try {
                const res = await fetch('/api/remote/files', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({path: path})
                });
                const data = await res.json();
                if (data.success) {
                    currentPath = data.current_path;
                    parentPath = data.parent_path;
                    document.getElementById('currentDirLabel').innerText = currentPath;
                    let html = '';
                    data.entries.forEach(item => {
                        const icon = item.is_dir ? 'fa-solid fa-folder text-warning' : 'fa-solid fa-file-code text-info';
                        const action = item.is_dir ? `loadFiles('${escapeHtml(item.path)}')` : `viewFile('${escapeHtml(item.path)}')`;
                        html += `
                            <div class="file-item" onclick="${action}">
                                <div class="d-flex align-items-center gap-2 text-truncate">
                                    <i class="${icon}"></i>
                                    <span class="text-truncate">${escapeHtml(item.name)}</span>
                                </div>
                                <small class="text-muted font-mono" style="font-size:0.75rem;">${item.size}</small>
                            </div>
                        `;
                    });
                    container.innerHTML = html || '<div class="text-muted p-2">Directory is empty.</div>';
                }
            } catch(e) {
                container.innerHTML = `<div class="text-danger p-2">Error: ${e}</div>`;
            }
        }

        function navigateParent() {
            if (parentPath && parentPath !== currentPath) {
                loadFiles(parentPath);
            }
        }

        async function viewFile(path) {
            try {
                const res = await fetch('/api/remote/file-view', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({path: path})
                });
                const data = await res.json();
                if (data.success) {
                    document.getElementById('fileModalTitle').innerText = data.filename + ` (${data.size_kb} KB)`;
                    document.getElementById('fileModalContent').innerText = data.content;
                    new bootstrap.Modal(document.getElementById('fileModal')).show();
                } else {
                    alert(data.error || 'Could not view file.');
                }
            } catch(e) {
                alert('File view error: ' + e);
            }
        }

        async function loadProcesses() {
            const list = document.getElementById('processList');
            list.innerHTML = 'Refreshing...';
            try {
                const res = await fetch('/api/remote/processes');
                const data = await res.json();
                let html = '<table class="table table-dark table-sm m-0"><thead><tr><th>PID</th><th>Name</th><th>CPU%</th><th>RAM%</th></tr></thead><tbody>';
                data.processes.forEach(p => {
                    html += `<tr><td>${p.pid}</td><td>${escapeHtml(p.name)}</td><td>${p.cpu}%</td><td>${p.mem}%</td></tr>`;
                });
                html += '</tbody></table>';
                list.innerHTML = html;
            } catch(e) {
                list.innerHTML = 'Error loading processes.';
            }
        }

        function refreshHardware() {
            fetchStatus();
            loadProcesses();
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Initialize on load
        fetchStatus();
        setInterval(fetchStatus, 8000);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)
