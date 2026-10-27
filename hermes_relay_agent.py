# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
Hermes Multi-Agent Relay & Intent Dispatcher (હર્મિસ રિલે એજન્ટ)
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)
"""

import os
import sys
import time
import json
import socket
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Generator

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
JARVIS_DIR = Path("/home/alpesh/jarvis-agent")
DATA_DIR = BASE_DIR / "data"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(JARVIS_DIR) not in sys.path:
    sys.path.insert(0, str(JARVIS_DIR))

# Import Aradhya Offline Cognitive Knowledge Engine
from aradhya_offline_knowledge import get_offline_cognitive_engine

try:
    from chamunda_llm_engine import get_llm_engine
except ImportError:
    get_llm_engine = None

# Import Jarvis Offline Commander
try:
    from core.offline_commander import OfflineAutonomousCommander
    jarvis_offline_commander = OfflineAutonomousCommander()
except Exception:
    jarvis_offline_commander = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [HermesRelay] %(message)s"
)
logger = logging.getLogger("HermesRelay")


class HermesRelayAgent:
    """
    Intelligent message relay, agent dispatcher, and online/offline bridge.
    """

    def __init__(self):
        self.last_online_check = 0.0
        self.cached_online_status = True
        self.check_interval = 5.0
        self.offline_engine = get_offline_cognitive_engine()

    def is_online(self, force_refresh: bool = False) -> bool:
        """Microsecond socket probe to verify real internet connectivity."""
        now = time.time()
        if not force_refresh and (now - self.last_online_check < self.check_interval):
            return self.cached_online_status

        self.last_online_check = now
        for host in ["8.8.8.8", "1.1.1.1"]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.8)
                s.connect((host, 53))
                s.close()
                self.cached_online_status = True
                return True
            except (socket.timeout, OSError):
                continue

        self.cached_online_status = False
        return False

    def classify_intent(self, text: str) -> str:
        """Classify user prompt into aradhya, jarvis, or relay."""
        t = text.lower()

        jarvis_keywords = [
            "battery", "brightness", "volume", "sound", "mute", "unmute",
            "screen", "lock screen", "lag", "hang", "sluggish", "turbo",
            "optimize laptop", "kill process", "running process", "disk usage",
            "security audit", "hacker", "firewall", "backdoor", "stay awake",
            "reboot", "shutdown", "laptop", "cpu", "ram", "memory", "storage",
            "reverse engineer", "reverse engineering", "decompile", "disassemble",
            "rea", "apk decompil", "binary audit", "jadx", "ghidra",
            "strix", "penetration test", "pentest", "owasp", "appsec",
            "vulnerability scan", "security test", "idor", "xss", "ssrf", "sql injection",
            "લેપટોપ", "બેટરી", "સ્ક્રીન", "અવાજ", "હેંગ", "વાયરસ", "સિક્યોરિટી", "રિવર્સ એન્જિનિયરિંગ", "ડીકમ્પાઈલ"
        ]
        for kw in jarvis_keywords:
            if kw in t:
                return "jarvis"

        aradhya_keywords = [
            "royal enfield", "classic", "bullet", "meteor", "hunter", "interceptor",
            "continental", "himalayan", "guerrilla", "shotgun", "bear 650",
            "engine oil", "tappet", "torque", "spark plug", "chain slack",
            "fork oil", "tyre pressure", "service", "booking", "inventory",
            "spare part", "part number", "price", "on road", "emi", "invoice",
            "dms", "chhaya", "dealership", "showroom", "workshop",
            "રોયલ એનફીલ્ડ", "ક્લાસિક", "બુલેટ", "સર્વિસ", "ઓઇલ", "પાર્ટ્સ", "કિંમત"
        ]
        for kw in aradhya_keywords:
            if kw in t:
                return "aradhya"

        return "relay"

    def process_message(
        self,
        user_message: str,
        preferred_model: str = "auto",
        voice_mode: bool = False
    ) -> Dict[str, Any]:
        """Processes user message with automatic offline fallback."""
        online = self.is_online()
        intent = self.classify_intent(user_message)
        logger.info("Hermes dispatching query [Online=%s, Intent=%s]: '%s'", online, intent, user_message[:60])

        if not online or preferred_model == "aradhya-offline":
            return self._execute_offline(user_message, intent, voice_mode)

        try:
            return self._execute_online(user_message, intent, preferred_model, voice_mode)
        except Exception as e:
            logger.warning("Online execution error (%s). Falling back to Offline Mode...", e)
            res = self._execute_offline(user_message, intent, voice_mode)
            res["fallback_triggered"] = True
            res["fallback_reason"] = str(e)
            return res

    def _execute_online(
        self,
        user_message: str,
        intent: str,
        preferred_model: str,
        voice_mode: bool
    ) -> Dict[str, Any]:
        if intent == "jarvis" and jarvis_offline_commander:
            jarvis_res = jarvis_offline_commander.execute_offline_command(user_message)
            if jarvis_res.get("recognized"):
                reply_text = jarvis_res.get("feedback_message", "Command executed successfully.")
                if voice_mode and "voice_message" in jarvis_res:
                    reply_text = jarvis_res["voice_message"]
                return {
                    "agent": "jarvis-commander",
                    "mode": "online-local-hybrid",
                    "model": "jarvis-mark7",
                    "reply": reply_text,
                    "voice_ready": self._clean_for_voice(reply_text),
                    "action_executed": jarvis_res.get("action_executed")
                }

        if get_llm_engine:
            llm = get_llm_engine()
            target_model = "gemini-3.5-flash" if preferred_model in ["auto", "aradhya-ceo", "hermes-relay"] else preferred_model

            system_instruction = (
                "You are Aradhya (આરાધ્યા), the Chief Executive Officer (CEO) of Chamunda Automobile Enterprise "
                "(Royal Enfield Dealership & Workshop) in Gujarat. You report directly to Alpesh Sir (Founder & Chairman). "
                "Respond with deep technical Royal Enfield expertise, automotive leadership, and utmost respect ('જય માતાજી અલ્પેશ સાહેબ!'). "
                "Support both Gujarati and English naturally."
            )
            if voice_mode:
                system_instruction += " Keep responses concise, clear, and phonetically smooth for real-time text-to-speech voice playback."

            ai_res = llm.generate_ai_response(
                prompt=user_message,
                model_name=target_model,
                system_prompt=system_instruction
            )
            reply = ai_res.get("reply", "")
            if reply:
                return {
                    "agent": "aradhya-ceo" if intent == "aradhya" else "hermes-relay",
                    "mode": "online",
                    "model": ai_res.get("model_used", target_model),
                    "reply": reply,
                    "voice_ready": self._clean_for_voice(reply)
                }

        raise RuntimeError("Online LLM response was empty.")

    def _execute_offline(
        self,
        user_message: str,
        intent: str,
        voice_mode: bool
    ) -> Dict[str, Any]:
        """100% Offline Air-Gapped Execution using AOCKRE v2.0 & Jarvis."""
        if intent == "jarvis" and jarvis_offline_commander:
            jarvis_res = jarvis_offline_commander.execute_offline_command(user_message)
            if jarvis_res.get("recognized"):
                reply_text = jarvis_res.get("feedback_message", "ઓફલાઇન આદેશ સફળતાપૂર્વક ચલાવાયો છે.")
                if voice_mode and "voice_message" in jarvis_res:
                    reply_text = jarvis_res["voice_message"]
                return {
                    "agent": "jarvis-commander",
                    "mode": "offline",
                    "model": "jarvis-offline-core",
                    "reply": f"⚡ [ઓફલાઇન મોડ] {reply_text}",
                    "voice_ready": self._clean_for_voice(reply_text),
                    "action_executed": jarvis_res.get("action_executed")
                }

        low_msg = user_message.lower()
        if any(k in low_msg for k in ["reverse engineer", "rea", "decompile", "disassemble", "apk decompil", "રિવર્સ એન્જિનિયરિંગ"]):
            reply_text = (
                "⚡ [REA • Reverse Engineer Anything] સક્રિય છે, અલ્પેશ સાહેબ!\\n"
                "- સમર્થિત ટાર્ગેટ્સ: Android APK/AAR (Jadx/Fernflower), Native ELF/PE Binaries, Electron Apps, Managed .NET, અને Firmware.\\n"
                "- ક્ષમતાઓ: Decompilation, Call Graph Tracing, API Endpoint Extraction, અને AgentEnv Bundle Generation.\\n"
                "- મોડ: ૧૦૦% ઓફલાઇન એર-ગેપ્ડ એક્ઝિક્યુશન ઉપલબ્ધ."
            )
            return {
                "agent": "jarvis-commander",
                "mode": "offline",
                "model": "rea-reverse-engine",
                "reply": f"⚡ [ઓફલાઇન મોડ] {reply_text}",
                "voice_ready": self._clean_for_voice(reply_text)
            }

        if any(k in low_msg for k in ["strix", "penetration test", "pentest", "owasp", "appsec", "vulnerability scan", "પેનટેસ્ટ", "સિક્યોરિટી"]):
            reply_text = (
                "🛡️ [Strix • Autonomous Security Agent] સક્રિય છે, અલ્પેશ સાહેબ!\\n"
                "- ઓડિટ મોડ્સ: Web App Pentesting, API Security (REST/GraphQL), OWASP Top 10, Codebase Vulnerability Discovery, અને CI/CD Gates.\\n"
                "- વર્કફ્લો: ડાયનેમિક એક્સ્પ્લોઇટેશન પ્રૂફ-ઓફ-કન્સેપ્ટ (PoC) + ઓટોમેટેડ PR ફિક્સ જનરેશન.\\n"
                "- સ્કેનર: OSS Local Sandbox & Strix Cloud સપોર્ટેડ."
            )
            return {
                "agent": "jarvis-commander",
                "mode": "offline",
                "model": "strix-security-core",
                "reply": f"⚡ [ઓફલાઇન મોડ] {reply_text}",
                "voice_ready": self._clean_for_voice(reply_text)
            }

        synth_res = self.offline_engine.synthesize(user_message)
        has_gujarati = any('\u0A80' <= c <= '\u0AFF' for c in user_message)
        reply = synth_res.get("response_gu") if has_gujarati else synth_res.get("response_en")
        if not reply:
            reply = synth_res.get("response_en") or synth_res.get("response_gu") or ""

        if not reply:
            reply = (
                "જય માતાજી અલ્પેશ સાહેબ! હાલમાં ઇન્ટરનેટ ઉપલબ્ધ નથી, પરંતુ આરાધ્યા ઓફલાઇન સિસ્ટમ સક્રિય છે. "
                "રોયલ એનફીલ્ડના તમામ પ્લેટફોર્મ્સ (J-Series 350, 650 Twins, Sherpa 450), ટોર્ક સ્પેસિફિકેશન, "
                "સ્પેરપાર્ટ્સ, સર્વિસ શિડ્યુલ અને લેપટોપ કંટ્રોલ ઉપલબ્ધ છે. હું આપને શું મદદ કરી શકું?"
            )

        formatted_reply = f"📱 [૧૦૦% ઓફલાઇન મોડ] {reply}"

        return {
            "agent": "aradhya-offline",
            "mode": "offline",
            "model": "aradhya-cognitive-core-v2",
            "reply": formatted_reply,
            "voice_ready": self._clean_for_voice(reply),
            "category": synth_res.get("category")
        }

    def _clean_for_voice(self, text: str) -> str:
        import re
        t = re.sub(r"```[\s\S]*?```", "", text)
        t = re.sub(r"`([^`]+)`", r"\1", t)
        t = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", t)
        t = re.sub(r"[#*_\-~>]", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t


_hermes_relay: Optional[HermesRelayAgent] = None

def get_hermes_relay() -> HermesRelayAgent:
    global _hermes_relay
    if _hermes_relay is None:
        _hermes_relay = HermesRelayAgent()
    return _hermes_relay


if __name__ == "__main__":
    relay = get_hermes_relay()
    print("Testing Hermes Relay Agent...")
    print("Online status:", relay.is_online())
    test_queries = [
        "What is the oil capacity and tappet clearance of Royal Enfield Classic 350?",
        "Check laptop battery status",
        "જય માતાજી આરાધ્યા, J-Series 350 ની વિગતો આપો"
    ]
    for q in test_queries:
        res = relay.process_message(q)
        print(f"\n--- Query: {q} ---")
        print(f"Agent: {res['agent']} | Mode: {res['mode']} | Model: {res['model']}")
        print(f"Reply Preview: {res['reply'][:150]}...")
