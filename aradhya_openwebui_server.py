# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
Open WebUI • Voice-First & Text Multi-Agent Conversational Server (Port 3000)
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. 100% Voice-First Call Mode by default with bidirectional continuous audio.
2. One-click instant toggle to text-based chat mode with full Markdown & tables.
3. Powered by Hermes Relay Agent (Auto online/offline fallback).
4. Direct integration with Aradhya Gateway (/v1) and Jarvis GitHub skills.
"""

import os
import sys
import json
import time
import socket
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from hermes_relay_agent import get_hermes_relay
from jarvis_github_skill_loader import get_jarvis_skill_loader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [OpenWebUI] %(message)s"
)
logger = logging.getLogger("OpenWebUI")

app = FastAPI(
    title="Open WebUI • Aradhya & Jarvis Voice-First Interface",
    description="Offline-First Voice & Text Multi-Agent Interface for Alpesh Sir",
    version="3.0.0"
)

# Gateway target
GATEWAY_URL = "http://127.0.0.1:8081/v1"


@app.get("/health")
async def health():
    relay = get_hermes_relay()
    online = relay.is_online()
    return {
        "status": "healthy",
        "online": online,
        "mode": "online-cloud" if online else "offline-airgapped",
        "gateway": GATEWAY_URL,
        "timestamp": time.time()
    }


@app.get("/api/models")
async def list_models():
    import urllib.request
    try:
        req = urllib.request.Request(f"{GATEWAY_URL}/models", headers={"User-Agent": "OpenWebUI-Local/3.0"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data
    except Exception as e:
        logger.warning("Could not reach gateway for models: %s", e)
        return {
            "object": "list",
            "data": [
                {"id": "aradhya-ceo", "name": "👑 Aradhya CEO (Royal Enfield Dealership & Technical Mastermind)"},
                {"id": "jarvis-commander", "name": "⚡ Jarvis Mark VII (Linux OS Control & Security)"},
                {"id": "hermes-relay", "name": "🕊️ Hermes Relay Agent (Smart Intent Router & Fallback)"},
                {"id": "aradhya-offline", "name": "📱 100% Offline Cognitive Core (AOCKRE v2.0 - Air-Gapped)"}
            ]
        }


@app.post("/api/chat/completions")
async def chat_completions(request: Request):
    body = await request.body()
    relay = get_hermes_relay()
    payload = json.loads(body.decode("utf-8"))
    stream = payload.get("stream", False)

    import urllib.request
    try:
        req = urllib.request.Request(
            f"{GATEWAY_URL}/chat/completions",
            data=body,
            headers={"Content-Type": "application/json", "User-Agent": "OpenWebUI-Local/3.0"}
        )
        if stream:
            resp = urllib.request.urlopen(req, timeout=30)
            def sse_stream():
                try:
                    for line in resp:
                        yield line
                finally:
                    resp.close()
            return StreamingResponse(sse_stream(), media_type="text/event-stream")
        else:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return JSONResponse(data)
    except Exception as e:
        logger.error("Error communicating with Aradhya Gateway (%s). Triggering emergency offline reply.", e)
        # Direct local fallback
        user_msg = payload.get("messages", [{}])[-1].get("content", "")
        fallback_res = relay.process_message(user_msg, preferred_model="aradhya-offline")
        reply_text = fallback_res.get("reply", "ક્ષમા કરશો સાહેબ, ઓફલાઇન પ્રક્રિયામાં સમસ્યા આવી છે.")
        return JSONResponse({
            "id": "chatcmpl-emergency-offline",
            "object": "chat.completion",
            "created": int(time.time()),
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": reply_text},
                "finish_reason": "stop"
            }]
        })


@app.post("/api/jarvis/sync")
async def sync_jarvis():
    """Syncs Jarvis skills from GitHub if online."""
    loader = get_jarvis_skill_loader()
    res = loader.sync_from_github()
    return JSONResponse(res)


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_openwebui():
    """Serves the complete Open WebUI Voice-First & Text Interface."""
    return HTMLResponse(content=INDEX_HTML)


INDEX_HTML = r"""<!DOCTYPE html>
<html lang="gu" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Open WebUI • Chamunda Automobile Enterprise (આરાધ્યા & જાર્વિસ)</title>
    <meta name="description" content="Open WebUI Voice-First Conversational Interface for Alpesh Sir">
    <meta name="theme-color" content="#0d1117">
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border: #30363d;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
            --accent-gold: #f59e0b;
            --accent-blue: #38bdf8;
            --accent-green: #10b981;
            --accent-red: #ef4444;
            --royal-red: #b91c1c;
            --radius-lg: 16px;
            --radius-md: 10px;
            --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans Gujarati", "Gujarati Sangam MN", sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            height: 100vh;
            width: 100vw;
            display: flex;
            overflow: hidden;
        }

        /* App Layout */
        #app-container {
            display: flex;
            width: 100%;
            height: 100%;
            position: relative;
        }

        /* Sidebar */
        aside.sidebar {
            width: 280px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            z-index: 20;
            transition: transform 0.3s ease;
        }

        @media (max-width: 768px) {
            aside.sidebar {
                position: absolute;
                top: 0;
                bottom: 0;
                left: 0;
                transform: translateX(-100%);
            }
            aside.sidebar.open {
                transform: translateX(0);
            }
        }

        .sidebar-header {
            padding: 18px 16px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand-badge {
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.05rem;
            letter-spacing: -0.2px;
        }

        .brand-logo {
            font-size: 1.4rem;
            filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.4));
        }

        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 16px 12px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .section-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-muted);
            padding: 0 8px;
            margin-bottom: 6px;
        }

        .model-list {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .model-btn {
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-main);
            padding: 10px 12px;
            border-radius: var(--radius-md);
            text-align: left;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 0.9rem;
            transition: all 0.2s;
        }

        .model-btn:hover {
            background: var(--bg-tertiary);
        }

        .model-btn.active {
            background: rgba(245, 158, 11, 0.12);
            border-color: rgba(245, 158, 11, 0.4);
            color: #fbbf24;
            font-weight: 600;
        }

        .sidebar-footer {
            padding: 14px 16px;
            border-top: 1px solid var(--border);
            font-size: 0.8rem;
            color: var(--text-muted);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 0.75rem;
            background: var(--bg-tertiary);
            width: fit-content;
        }

        .dot-green {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
            box-shadow: 0 0 6px var(--accent-green);
        }

        .dot-orange {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-gold);
            box-shadow: 0 0 6px var(--accent-gold);
        }

        /* Main View */
        main.main-viewport {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: var(--bg-primary);
            position: relative;
            height: 100%;
        }

        /* Top Bar */
        header.top-nav {
            height: 60px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            background: rgba(22, 27, 34, 0.85);
            backdrop-filter: blur(12px);
            z-index: 10;
        }

        .nav-left, .nav-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .icon-btn {
            background: transparent;
            border: 1px solid var(--border);
            color: var(--text-main);
            width: 38px;
            height: 38px;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            transition: all 0.2s;
        }

        .icon-btn:hover {
            background: var(--bg-tertiary);
            border-color: var(--text-muted);
        }

        .mode-toggle-btn {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #000;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 8px 16px;
            border-radius: var(--radius-md);
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
            transition: all 0.2s;
        }

        .mode-toggle-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(245, 158, 11, 0.4);
        }

        /* ========================================================================== */
        /* 1. VOICE CALL MODE (100% Full-Screen Voice)                                */
        /* ========================================================================== */
        #voice-call-mode {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, #1b2838 0%, #0d1117 80%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            padding: 40px 20px;
            z-index: 15;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }

        #voice-call-mode.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }

        .call-header {
            text-align: center;
            margin-top: 20px;
        }

        .call-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #fbbf24;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 6px;
        }

        .call-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
        }

        /* Glowing Pulsing Visualizer Orb */
        .call-visualizer-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            margin: auto 0;
        }

        .orb-pulse {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, #38bdf8 0%, #0284c7 50%, #0369a1 100%);
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.5), inset 0 0 30px rgba(255, 255, 255, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 4.5rem;
            color: #fff;
            position: relative;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            cursor: pointer;
        }

        .orb-pulse.listening {
            animation: pulse-ring 2s infinite ease-out;
            box-shadow: 0 0 80px rgba(16, 185, 129, 0.7), inset 0 0 40px rgba(255, 255, 255, 0.6);
            background: radial-gradient(circle, #34d399 0%, #059669 50%, #047857 100%);
        }

        .orb-pulse.speaking {
            animation: speaking-pulse 1.2s infinite alternate ease-in-out;
            box-shadow: 0 0 90px rgba(245, 158, 11, 0.8), inset 0 0 40px rgba(255, 255, 255, 0.6);
            background: radial-gradient(circle, #fbbf24 0%, #d97706 50%, #b45309 100%);
        }

        @keyframes pulse-ring {
            0% { transform: scale(0.96); box-shadow: 0 0 40px rgba(16, 185, 129, 0.5); }
            50% { transform: scale(1.08); box-shadow: 0 0 90px rgba(16, 185, 129, 0.9); }
            100% { transform: scale(0.96); box-shadow: 0 0 40px rgba(16, 185, 129, 0.5); }
        }

        @keyframes speaking-pulse {
            0% { transform: scale(1.0); box-shadow: 0 0 60px rgba(245, 158, 11, 0.6); }
            100% { transform: scale(1.15); box-shadow: 0 0 110px rgba(245, 158, 11, 1.0); }
        }

        .call-status-badge {
            margin-top: 32px;
            padding: 8px 20px;
            background: rgba(33, 38, 45, 0.8);
            border: 1px solid var(--border);
            border-radius: 999px;
            font-size: 0.95rem;
            color: #e2e8f0;
            display: flex;
            align-items: center;
            gap: 8px;
            backdrop-filter: blur(8px);
        }

        .live-transcript-box {
            max-width: 650px;
            width: 100%;
            min-height: 70px;
            max-height: 140px;
            overflow-y: auto;
            background: rgba(22, 27, 34, 0.6);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 16px 20px;
            text-align: center;
            font-size: 1.05rem;
            color: #cbd5e1;
            margin-top: 20px;
            backdrop-filter: blur(10px);
            line-height: 1.5;
        }

        .call-controls {
            display: flex;
            align-items: center;
            gap: 24px;
            margin-bottom: 20px;
        }

        .call-action-btn {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            transition: all 0.2s;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        }

        .call-action-btn.mute {
            background: var(--bg-tertiary);
            color: var(--text-main);
            border: 1px solid var(--border);
        }

        .call-action-btn.mute.active {
            background: var(--accent-red);
            color: #fff;
        }

        .call-action-btn.switch-text {
            background: #2563eb;
            color: #fff;
        }

        .call-action-btn:hover {
            transform: scale(1.08);
        }

        /* ========================================================================== */
        /* 2. TEXT CHAT MODE                                                         */
        /* ========================================================================== */
        #text-chat-mode {
            flex: 1;
            display: flex;
            flex-direction: column;
            height: calc(100% - 60px);
            position: relative;
        }

        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 24px 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            scroll-behavior: smooth;
        }

        .message-row {
            display: flex;
            gap: 14px;
            max-width: 860px;
            width: 100%;
            margin: 0 auto;
        }

        .message-row.user {
            flex-direction: row-reverse;
        }

        .avatar {
            width: 38px;
            height: 38px;
            border-radius: var(--radius-md);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
        }

        .message-row.assistant .avatar {
            background: rgba(245, 158, 11, 0.15);
            border-color: rgba(245, 158, 11, 0.3);
        }

        .message-bubble {
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            padding: 14px 18px;
            border-radius: var(--radius-lg);
            font-size: 0.98rem;
            line-height: 1.6;
            color: var(--text-main);
            max-width: 82%;
            word-wrap: break-word;
            box-shadow: var(--shadow);
        }

        .message-row.user .message-bubble {
            background: #1e3a8a;
            border-color: #2563eb;
            color: #ffffff;
            border-bottom-right-radius: 4px;
        }

        .message-row.assistant .message-bubble {
            border-bottom-left-radius: 4px;
        }

        /* Rich Markdown formatting in bubbles */
        .message-bubble pre {
            background: #090d13;
            padding: 12px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
            border: 1px solid var(--border);
            font-family: monospace;
            font-size: 0.88rem;
        }

        .message-bubble table {
            border-collapse: collapse;
            width: 100%;
            margin: 12px 0;
            font-size: 0.88rem;
        }

        .message-bubble th, .message-bubble td {
            border: 1px solid var(--border);
            padding: 8px 12px;
            text-align: left;
        }

        .message-bubble th {
            background: var(--bg-tertiary);
            color: #fbbf24;
        }

        .message-bubble blockquote {
            border-left: 3px solid #f59e0b;
            padding-left: 12px;
            color: #94a3b8;
            margin: 8px 0;
            font-style: italic;
        }

        /* Input Area */
        .chat-input-bar {
            padding: 16px 20px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            max-width: 860px;
            width: 100%;
            margin: 0 auto;
            border-radius: var(--radius-lg);
            margin-bottom: 16px;
            box-shadow: var(--shadow);
        }

        .chat-input-bar textarea {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            color: var(--text-main);
            font-size: 0.98rem;
            resize: none;
            max-height: 120px;
            min-height: 24px;
            line-height: 1.4;
        }

        .send-btn {
            background: #2563eb;
            color: #fff;
            border: none;
            width: 38px;
            height: 38px;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            transition: all 0.2s;
        }

        .send-btn:hover {
            background: #1d4ed8;
        }

        .mic-btn-input {
            background: transparent;
            border: 1px solid var(--border);
            color: #38bdf8;
            width: 38px;
            height: 38px;
            border-radius: var(--radius-md);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            transition: all 0.2s;
        }

        .mic-btn-input:hover {
            background: var(--bg-tertiary);
        }
    </style>
</head>
<body>
    <div id="app-container">
        <!-- Sidebar -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="brand-badge">
                    <span class="brand-logo">👑</span>
                    <span>Aradhya & Jarvis</span>
                </div>
                <button class="icon-btn" onclick="toggleSidebar()" title="Close Sidebar">✕</button>
            </div>

            <div class="sidebar-content">
                <div class="section-label">Select Model / Agent</div>
                <div class="model-list">
                    <button class="model-btn active" data-model="aradhya-ceo" onclick="selectModel('aradhya-ceo')">
                        <span>👑</span>
                        <div>
                            <div>Aradhya CEO</div>
                            <small style="color:var(--text-muted);font-size:0.75rem;">Royal Enfield & Dealership</small>
                        </div>
                    </button>
                    <button class="model-btn" data-model="jarvis-commander" onclick="selectModel('jarvis-commander')">
                        <span>⚡</span>
                        <div>
                            <div>Jarvis Mark VII</div>
                            <small style="color:var(--text-muted);font-size:0.75rem;">OS Control & Security</small>
                        </div>
                    </button>
                    <button class="model-btn" data-model="hermes-relay" onclick="selectModel('hermes-relay')">
                        <span>🕊️</span>
                        <div>
                            <div>Hermes Relay</div>
                            <small style="color:var(--text-muted);font-size:0.75rem;">Smart Router & Fallback</small>
                        </div>
                    </button>
                    <button class="model-btn" data-model="aradhya-offline" onclick="selectModel('aradhya-offline')">
                        <span>📱</span>
                        <div>
                            <div>100% Offline Core</div>
                            <small style="color:var(--text-muted);font-size:0.75rem;">AOCKRE v2.0 Air-Gapped</small>
                        </div>
                    </button>
                </div>

                <div class="section-label" style="margin-top:20px;">GitHub Skill Loader</div>
                <button class="model-btn" onclick="syncJarvisSkills()" style="border:1px dashed var(--border);">
                    <span>🔄</span>
                    <div>
                        <div>Sync GitHub Skills</div>
                        <small style="color:var(--text-muted);font-size:0.75rem;">thakoralpesh3/jarvis-agent</small>
                    </div>
                </button>
            </div>

            <div class="sidebar-footer">
                <div class="status-pill" id="network-status-pill">
                    <span class="dot-green" id="network-dot"></span>
                    <span id="network-text">Checking network...</span>
                </div>
                <div style="font-size:0.75rem;">Authority: Alpesh Sir (Chairman)</div>
            </div>
        </aside>

        <!-- Main Viewport -->
        <main class="main-viewport">
            <!-- Top Navigation -->
            <header class="top-nav">
                <div class="nav-left">
                    <button class="icon-btn" onclick="toggleSidebar()" title="Toggle Sidebar">☰</button>
                    <span id="current-model-badge" style="font-weight:600;font-size:0.95rem;color:#fbbf24;">👑 Aradhya CEO</span>
                </div>
                <div class="nav-right">
                    <button class="mode-toggle-btn" id="mode-toggle-btn" onclick="toggleMode()">
                        <span>💬 Switch to Text Mode</span>
                    </button>
                </div>
            </header>

            <!-- =============================================================== -->
            <!-- 1. VOICE CALL MODE (DEFAULT)                                   -->
            <!-- =============================================================== -->
            <section id="voice-call-mode">
                <div class="call-header">
                    <div class="call-title">
                        <span>🎙️</span>
                        <span>100% Hands-Free Voice Mode</span>
                    </div>
                    <div class="call-subtitle">Speak freely in Gujarati or English • Aradhya is listening</div>
                </div>

                <div class="call-visualizer-container">
                    <div class="orb-pulse listening" id="call-orb" onclick="toggleListening()">
                        <span>🎙️</span>
                    </div>
                    <div class="call-status-badge">
                        <span class="dot-green" id="call-dot"></span>
                        <span id="call-status-label">Listening for Alpesh Sir...</span>
                    </div>
                    <div class="live-transcript-box" id="call-transcript">
                        "જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા છું. આપનો શો આદેશ છે?"
                    </div>
                </div>

                <div class="call-controls">
                    <button class="call-action-btn mute" id="call-mute-btn" onclick="toggleMute()" title="Mute/Unmute Mic">
                        <span id="mute-icon">🎤</span>
                    </button>
                    <button class="call-action-btn switch-text" onclick="setMode('text')" title="Switch to Text Mode">
                        <span>💬</span>
                    </button>
                </div>
            </section>

            <!-- =============================================================== -->
            <!-- 2. TEXT CHAT MODE                                              -->
            <!-- =============================================================== -->
            <section id="text-chat-mode" style="display:none;">
                <div class="messages-container" id="messages-container">
                    <!-- Default Greeting Message -->
                    <div class="message-row assistant">
                        <div class="avatar">👑</div>
                        <div class="message-bubble">
                            <strong>જય માતાજી અલ્પેશ સાહેબ!</strong><br><br>
                            આરાધ્યા (CEO, Chamunda Automobile Enterprise) અને જાર્વિસ (Mark VII) આપની સેવામાં હાજર છે.<br>
                            - <strong>૧૦૦% ઓફલાઇન મોડ</strong>: ઇન્ટરનેટ વગર રોયલ એનફીલ્ડ સ્પેસિફિકેશન્સ અને લેપટોપ કંટ્રોલ.<br>
                            - <strong>ઓનલાઇન મોડ</strong>: ગિટહબ સ્કિલ્સ અને ક્લાઉડ મલ્ટી-કી રોટેશન.<br>
                            - ગમે ત્યારે ઉપર આપેલા <strong>🎙️ Call Mode</strong> બટન પર ક્લિક કરીને વોઈસ મોડમાં જઈ શકો છો!
                        </div>
                    </div>
                </div>

                <div class="chat-input-bar">
                    <button class="mic-btn-input" onclick="setMode('voice')" title="Start Voice Call Mode">🎙️</button>
                    <textarea id="chat-textarea" placeholder="આદેશ આપો, અલ્પેશ સાહેબ... (Ask Royal Enfield specs, laptop control, etc.)" rows="1" onkeydown="handleTextKey(event)"></textarea>
                    <button class="send-btn" onclick="sendTextMessage()" title="Send Message">➤</button>
                </div>
            </section>
        </main>
    </div>

    <!-- Script Logic -->
    <script>
        // State
        let currentMode = "voice"; // "voice" or "text"
        let activeModel = "aradhya-ceo";
        let isListening = false;
        let isSpeaking = false;
        let isMuted = false;
        let recognition = null;
        let synthesis = window.speechSynthesis;
        let currentUtterance = null;

        // Elements
        const voiceCallSection = document.getElementById("voice-call-mode");
        const textChatSection = document.getElementById("text-chat-mode");
        const modeToggleBtn = document.getElementById("mode-toggle-btn");
        const callOrb = document.getElementById("call-orb");
        const callStatusLabel = document.getElementById("call-status-label");
        const callTranscript = document.getElementById("call-transcript");
        const callDot = document.getElementById("call-dot");
        const callMuteBtn = document.getElementById("call-mute-btn");
        const messagesContainer = document.getElementById("messages-container");
        const chatTextarea = document.getElementById("chat-textarea");
        const currentModelBadge = document.getElementById("current-model-badge");
        const networkStatusPill = document.getElementById("network-status-pill");
        const networkDot = document.getElementById("network-dot");
        const networkText = document.getElementById("network-text");

        // Initialize Speech Recognition
        function initSpeechRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                console.warn("Web Speech API not supported in this browser. Falling back to audio recording.");
                return;
            }

            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = "gu-IN"; // Default to Gujarati (also recognizes English commands)

            recognition.onstart = () => {
                isListening = true;
                callOrb.className = "orb-pulse listening";
                callStatusLabel.textContent = "Listening for Alpesh Sir...";
                callDot.className = "dot-green";
            };

            recognition.onresult = (event) => {
                let interim = "";
                let finalTranscript = "";
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interim += event.results[i][0].transcript;
                    }
                }
                const textToShow = finalTranscript || interim;
                if (textToShow) {
                    callTranscript.textContent = `"${textToShow}"`;
                }

                if (finalTranscript.trim()) {
                    handleUserSpokenText(finalTranscript.trim());
                }
            };

            recognition.onerror = (event) => {
                console.warn("Speech recognition error:", event.error);
                if (event.error !== "no-speech" && !isSpeaking && !isMuted && currentMode === "voice") {
                    setTimeout(startListening, 1000);
                }
            };

            recognition.onend = () => {
                isListening = false;
                if (!isSpeaking && !isMuted && currentMode === "voice") {
                    startListening();
                }
            };
        }

        function startListening() {
            if (isMuted || isSpeaking || currentMode !== "voice") return;
            try {
                if (recognition) {
                    recognition.start();
                }
            } catch (e) {
                // Ignore already running errors
            }
        }

        function stopListening() {
            if (recognition) {
                try { recognition.stop(); } catch(e){}
            }
            isListening = false;
        }

        // Handle User Spoken Text in Voice Call Mode
        async function handleUserSpokenText(text) {
            stopListening();
            callStatusLabel.textContent = "Aradhya is processing...";
            callOrb.className = "orb-pulse";

            // Add user message to text chat log for history
            appendMessage("user", text);

            try {
                const response = await fetch("/api/chat/completions", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        model: activeModel,
                        messages: [{ role: "user", content: text }],
                        stream: false
                    })
                });

                const data = await response.json();
                const reply = data.choices?.[0]?.message?.content || "જી સાહેબ, આપનો સંદેશ મળ્યો છે.";

                // Display reply in Call Mode transcript box and log in text chat
                callTranscript.innerHTML = `<span style="color:#fbbf24;">👑 Aradhya:</span> ${reply.substring(0, 250)}...`;
                appendMessage("assistant", reply);

                // Speak reply aloud in Aradhya's voice
                speakReplyAloud(reply);
            } catch (err) {
                console.error("Chat error:", err);
                const errReply = "ક્ષમા કરશો અલ્પેશ સાહેબ, સર્વર કનેક્શનમાં વિલંબ થયો છે.";
                callTranscript.textContent = errReply;
                speakReplyAloud(errReply);
            }
        }

        // Text-to-Speech
        function speakReplyAloud(text) {
            if (!synthesis) {
                setTimeout(startListening, 1500);
                return;
            }

            synthesis.cancel();
            isSpeaking = true;
            callOrb.className = "orb-pulse speaking";
            callStatusLabel.textContent = "Aradhya speaking...";

            // Clean text for speech synthesis
            const cleanText = text.replace(/[*_#`~>\[\]\(\)]/g, " ").replace(/\s+/g, " ").trim();
            const utterance = new SpeechSynthesisUtterance(cleanText);

            // Voice selection: prioritize Gujarati/Indian female voice
            const voices = synthesis.getVoices();
            const guVoice = voices.find(v => v.lang.includes("gu") || v.lang.includes("hi") || v.name.includes("Dhwani") || v.name.includes("Kalpana"));
            if (guVoice) utterance.voice = guVoice;
            utterance.rate = 1.0;
            utterance.pitch = 1.05;

            utterance.onend = () => {
                isSpeaking = false;
                callOrb.className = "orb-pulse listening";
                callStatusLabel.textContent = "Listening for Alpesh Sir...";
                if (currentMode === "voice" && !isMuted) {
                    setTimeout(startListening, 600);
                }
            };

            utterance.onerror = () => {
                isSpeaking = false;
                if (currentMode === "voice" && !isMuted) {
                    setTimeout(startListening, 800);
                }
            };

            synthesis.speak(utterance);
        }

        // Mode Switching (Voice <-> Text)
        function toggleMode() {
            setMode(currentMode === "voice" ? "text" : "voice");
        }

        function setMode(mode) {
            currentMode = mode;
            if (mode === "voice") {
                voiceCallSection.style.display = "flex";
                voiceCallSection.classList.remove("hidden");
                textChatSection.style.display = "none";
                modeToggleBtn.innerHTML = "<span>💬 Switch to Text Mode</span>";
                startListening();
            } else {
                stopListening();
                if (synthesis) synthesis.cancel();
                isSpeaking = false;
                voiceCallSection.style.display = "none";
                voiceCallSection.classList.add("hidden");
                textChatSection.style.display = "flex";
                modeToggleBtn.innerHTML = "<span>🎙️ Switch to Voice Mode</span>";
                chatTextarea.focus();
            }
        }

        function toggleMute() {
            isMuted = !isMuted;
            if (isMuted) {
                stopListening();
                callMuteBtn.classList.add("active");
                callStatusLabel.textContent = "Microphone Muted";
                callDot.className = "dot-orange";
            } else {
                callMuteBtn.classList.remove("active");
                startListening();
            }
        }

        function toggleListening() {
            if (isSpeaking) {
                synthesis.cancel();
                isSpeaking = false;
                startListening();
            } else if (isListening) {
                stopListening();
            } else {
                startListening();
            }
        }

        // Text Chat Messaging
        async function sendTextMessage() {
            const text = chatTextarea.value.trim();
            if (!text) return;

            chatTextarea.value = "";
            appendMessage("user", text);

            try {
                const response = await fetch("/api/chat/completions", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        model: activeModel,
                        messages: [{ role: "user", content: text }],
                        stream: false
                    })
                });

                const data = await response.json();
                const reply = data.choices?.[0]?.message?.content || "આદેશ સફળતાપૂર્વક ચલાવાયો છે.";
                appendMessage("assistant", reply);
            } catch (err) {
                appendMessage("assistant", "⚠️ ભૂલ: Aradhya Gateway સાથે જોડાણ થઈ શક્યું નથી.");
            }
        }

        function appendMessage(role, text) {
            const row = document.createElement("div");
            row.className = `message-row ${role}`;

            const avatar = document.createElement("div");
            avatar.className = "avatar";
            avatar.textContent = role === "user" ? "👤" : (activeModel.includes("jarvis") ? "⚡" : "👑");

            const bubble = document.createElement("div");
            bubble.className = "message-bubble";
            bubble.innerHTML = formatMarkdown(text);

            row.appendChild(avatar);
            row.appendChild(bubble);
            messagesContainer.appendChild(row);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }

        function formatMarkdown(text) {
            let html = text
                .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
                .replace(/```([\s\S]*?)```/g, "<pre><code>$1</code></pre>")
                .replace(/`([^`]+)`/g, "<code style='background:#1e293b;padding:2px 6px;border-radius:4px;'>$1</code>")
                .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                .replace(/\*(.*?)\*/g, "<em>$1</em>")
                .replace(/\n/g, "<br>");
            return html;
        }

        function handleTextKey(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendTextMessage();
            }
        }

        function selectModel(modelId) {
            activeModel = modelId;
            document.querySelectorAll(".model-btn").forEach(btn => {
                btn.classList.toggle("active", btn.getAttribute("data-model") === modelId);
            });
            const nameMap = {
                "aradhya-ceo": "👑 Aradhya CEO",
                "jarvis-commander": "⚡ Jarvis Mark VII",
                "hermes-relay": "🕊️ Hermes Relay",
                "aradhya-offline": "📱 100% Offline Core"
            };
            currentModelBadge.textContent = nameMap[modelId] || modelId;
        }

        function toggleSidebar() {
            document.getElementById("sidebar").classList.toggle("open");
        }

        async function syncJarvisSkills() {
            networkText.textContent = "Syncing skills from GitHub...";
            try {
                const res = await fetch("/api/jarvis/sync", { method: "POST" });
                const data = await res.json();
                alert(data.success ? "✅ Jarvis skills synced from GitHub!" : "ℹ️ Using local cached skills: " + (data.error || "offline"));
            } catch (e) {
                alert("ℹ️ Using local cached skills (offline mode active).");
            }
            checkNetworkHealth();
        }

        async function checkNetworkHealth() {
            try {
                const res = await fetch("/health");
                const data = await res.json();
                if (data.online) {
                    networkDot.className = "dot-green";
                    networkText.textContent = "Online • Cloud & GitHub Active";
                } else {
                    networkDot.className = "dot-orange";
                    networkText.textContent = "100% Offline • Air-Gapped Core Active";
                }
            } catch (e) {
                networkDot.className = "dot-orange";
                networkText.textContent = "Offline Mode";
            }
        }

        // Initialize on Load
        window.addEventListener("DOMContentLoaded", () => {
            initSpeechRecognition();
            checkNetworkHealth();
            setInterval(checkNetworkHealth, 10000);

            // Greet Alpesh Sir automatically on load in Call Mode
            setTimeout(() => {
                if (currentMode === "voice") {
                    startListening();
                }
            }, 1000);
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    host = os.environ.get("HOST", "0.0.0.0")
    logger.info("Starting Open WebUI on http://%s:%s (Voice-First & Text)", host, port)
    uvicorn.run(app, host=host, port=port, log_level="warning")
