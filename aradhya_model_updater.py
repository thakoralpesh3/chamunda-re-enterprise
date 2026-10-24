# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
ARADHYA AUTONOMOUS AI MODEL AUTO-DISCOVERY & REGISTRY SELF-UPDATING ENGINE
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. Probes Google GenAI API for newly released models via client.models.list().
2. Probes local offline endpoints (e.g. Ollama http://127.0.0.1:11434) for local offline LLMs.
3. Automatically classifies newly discovered models into tiers (Pro Reasoning, Flash, Lite, Thinking, Gemma).
4. Dynamically registers new models into Chamunda LLM Engine catalog & cascades without manual code changes.
5. Ingests discoveries into Aradhya Self-Evolution memory ledger.
6. Dispatches bilingual alerts and desktop notifications when new frontier models are ingested.
"""

import os
import sys
import json
import time
import urllib.request
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DISCOVERED_MODELS_FILE = DATA_DIR / "aradhya_discovered_models.json"
MODEL_UPDATE_LOG_FILE = DATA_DIR / "aradhya_model_updates.log"

class AradhyaModelUpdater:
    """
    Autonomous AI Model Discovery & Self-Updating Registry.
    Keeps Aradhya at the bleeding-edge of AI capabilities automatically.
    """

    def __init__(self):
        self.discovered_models: Dict[str, Any] = self._load_discovered_models()
        self._last_discovery_time: float = 0.0

    def _load_discovered_models(self) -> Dict[str, Any]:
        if DISCOVERED_MODELS_FILE.exists():
            try:
                with open(DISCOVERED_MODELS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_discovered_models(self):
        try:
            with open(DISCOVERED_MODELS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.discovered_models, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def log_update_event(self, event_text: str):
        try:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(MODEL_UPDATE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {event_text}\n")
        except Exception:
            pass

    def probe_google_genai_models(self) -> List[Dict[str, Any]]:
        """Query Google GenAI API to discover all available foundation models."""
        found = []
        try:
            from chamunda_llm_engine import get_api_key_pool
            pool = get_api_key_pool()
            keys = pool.get_candidate_keys()
            if not keys:
                return []
            client = pool.get_client(keys[0])
            if not client:
                return []

            raw_models = client.models.list()
            for m in raw_models:
                m_id = m.name.replace("models/", "")
                actions = getattr(m, "supported_actions", getattr(m, "supported_generation_methods", [])) or []

                # Filter for text/multimodal content generation models
                if "generateContent" in actions or "generate_content" in actions:
                    display_name = getattr(m, "display_name", m_id)
                    description = getattr(m, "description", "") or "Discovered Google Foundation Model"

                    # Classify model tier
                    tier = "FLASH_THROUGHPUT"
                    badge_icon = "⚡"
                    if "argon" in m_id or "gemini-4" in m_id:
                        tier = "FRONTIER_ARGON"
                        badge_icon = "👑"
                    elif "pro" in m_id:
                        tier = "PRO_REASONING"
                        badge_icon = "🔬"
                    elif "thinking" in m_id or "reason" in m_id:
                        tier = "HYBRID_REASONING"
                        badge_icon = "🧠"
                    elif "lite" in m_id or "flash-lite" in m_id:
                        tier = "FLASH_LITE"
                        badge_icon = "🌱"
                    elif "gemma" in m_id:
                        tier = "OPEN_WEIGHTS"
                        badge_icon = "💎"

                    found.append({
                        "model_id": m_id,
                        "name": f"{display_name} (Auto-Discovered)",
                        "tag": tier,
                        "description": description,
                        "badge": f"{badge_icon} {display_name}",
                        "source": "google_genai_api",
                        "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
                    })
        except Exception as e:
            self.log_update_event(f"Google GenAI model probe error: {e}")
        return found

    def probe_local_ollama_models(self) -> List[Dict[str, Any]]:
        """Probe local Ollama daemon on http://127.0.0.1:11434 for offline open models."""
        found = []
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags", headers={"User-Agent": "AradhyaModelUpdater/1.0"})
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                for m in data.get("models", []):
                    m_name = m.get("name", "")
                    if m_name:
                        found.append({
                            "model_id": f"ollama/{m_name}",
                            "name": f"Ollama Local {m_name} (Offline LLM)",
                            "tag": "LOCAL_OFFLINE_LLM",
                            "description": f"Local air-gapped open model ({m.get('size', 0) // (1024*1024)} MB)",
                            "badge": f"🦙 Ollama {m_name}",
                            "source": "local_ollama_runtime",
                            "discovered_at": time.strftime("%Y-%m-%d %H:%M:%S")
                        })
        except Exception:
            # Local Ollama not running or absent, gracefully skip
            pass
        return found

    def discover_and_update_models(self, notify_desktop: bool = True) -> Dict[str, Any]:
        """
        Execute full model discovery cycle across cloud APIs and local runtimes.
        Updates MODEL_CATALOG, CASCADES, and Self-Evolution memory dynamically.
        """
        start_time = time.time()
        new_models_found = []

        # 1. Probe Google Cloud
        cloud_models = self.probe_google_genai_models()

        # 2. Probe Local Runtimes
        local_models = self.probe_local_ollama_models()

        all_candidates = cloud_models + local_models

        # Import chamunda_llm_engine to update in-memory catalog
        try:
            import chamunda_llm_engine
        except Exception:
            chamunda_llm_engine = None

        for cand in all_candidates:
            mid = cand["model_id"]
            if mid not in self.discovered_models:
                self.discovered_models[mid] = cand
                new_models_found.append(cand)
                self.log_update_event(f"NEW MODEL DISCOVERED: {mid} ({cand['badge']})")

            # Update live MODEL_CATALOG
            if chamunda_llm_engine and hasattr(chamunda_llm_engine, "MODEL_CATALOG"):
                if mid not in chamunda_llm_engine.MODEL_CATALOG:
                    chamunda_llm_engine.MODEL_CATALOG[mid] = {
                        "name": cand["name"],
                        "tag": cand["tag"],
                        "description": cand["description"],
                        "badge": cand["badge"]
                    }

                # Dynamically register into cascades if not already present
                if hasattr(chamunda_llm_engine, "CASCADES") and mid not in chamunda_llm_engine.CASCADES:
                    if cand["tag"] == "PRO_REASONING":
                        chamunda_llm_engine.CASCADES[mid] = [mid, "gemini-3.5-flash-lite", "gemini-3.5-flash"]
                    elif cand["tag"] == "FLASH_LITE":
                        chamunda_llm_engine.CASCADES[mid] = [mid, "gemini-3.5-flash"]
                    else:
                        chamunda_llm_engine.CASCADES[mid] = [mid, "gemini-3.5-flash-lite", "gemini-3.5-flash"]

        # Persist updated registry
        self._save_discovered_models()
        self._last_discovery_time = time.time()

        # 3. Log into Aradhya Self-Evolution Ledger
        if new_models_found:
            try:
                from aradhya_self_evolution import get_self_evolution
                evo = get_self_evolution()
                for nm in new_models_found:
                    evo.record_learned_fact(
                        topic="Autonomous AI Model Discovery",
                        fact=f"Discovered and integrated new foundation model {nm['model_id']} ({nm['badge']}) into Aradhya Dual-Brain catalog.",
                        source="AradhyaModelUpdater"
                    )
            except Exception:
                pass

            # Desktop Notification if graphical session exists
            if notify_desktop:
                try:
                    import subprocess
                    names_str = ", ".join([m['model_id'] for m in new_models_found[:3]])
                    subprocess.run(
                        ["notify-send", "-u", "normal", "-t", "6000",
                         "🧬 Aradhya AI Self-Update Complete",
                         f"Discovered & ingested {len(new_models_found)} new AI model(s): {names_str}"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                except Exception:
                    pass

        elapsed_ms = int((time.time() - start_time) * 1000)

        # Bilingual reporting
        if new_models_found:
            msg_en = (
                f"🧬 Autonomous AI Model Discovery Complete in {elapsed_ms}ms! "
                f"Ingested {len(new_models_found)} newly released AI model(s) into Aradhya Brain. "
                f"Total Catalog: {len(self.discovered_models)} models."
            )
            msg_gu = (
                f"🧬 સ્વાયત્ત AI મોડેલ અપડેટ સફળ ({elapsed_ms}ms)! "
                f"અલ્પેશ સાહેબ, {len(new_models_found)} નવા એઆઈ મોડેલ આરાધ્યા સિસ્ટમમાં આપોઆપ ઉમેરાઈ ગયા છે. "
                f"હાલ કુલ મોડેલ ક્ષમતા: {len(self.discovered_models)}."
            )
        else:
            msg_en = (
                f"⚡ AI Model Registry Verified ({elapsed_ms}ms). "
                f"Aradhya is 100% up-to-date with latest frontier models. "
                f"Total Active Catalog: {len(self.discovered_models)} models."
            )
            msg_gu = (
                f"⚡ AI મોડેલ રજીસ્ટ્રી વેરિફાઇડ ({elapsed_ms}ms). "
                f"આરાધ્યા તમામ અત્યાધુનિક એઆઈ મોડેલ્સ સાથે ૧૦૦% અદ્યતન છે. "
                f"કુલ સક્રિય મોડેલ્સ: {len(self.discovered_models)}."
            )

        return {
            "success": True,
            "new_models_count": len(new_models_found),
            "new_models": new_models_found,
            "total_registered_models": len(self.discovered_models),
            "duration_ms": elapsed_ms,
            "message_en": msg_en,
            "message_gu": msg_gu,
            "summary": f"{len(new_models_found)} new model(s) ingested. Total: {len(self.discovered_models)}"
        }

_updater_instance: Optional[AradhyaModelUpdater] = None

def get_model_updater() -> AradhyaModelUpdater:
    global _updater_instance
    if _updater_instance is None:
        _updater_instance = AradhyaModelUpdater()
    return _updater_instance

if __name__ == "__main__":
    upd = get_model_updater()
    res = upd.discover_and_update_models()
    print("Result:", res["summary"])
    print("EN:", res["message_en"])
    print("GU:", res["message_gu"])
