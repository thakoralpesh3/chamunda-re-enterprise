# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
Aradhya Autonomous Multi-Channel Notification Engine (આરાધ્યા નોટિફાયર)
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Channels Supported:
1. Telegram Bot API (Direct 24/7 push notifications to Alpesh Sir's phone)
2. Linux Desktop GUI Banner (/usr/bin/notify-send)
3. Notification History Log (data/notifications_history.json)
"""

import os
import sys
import json
import time
import urllib.request
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path(__file__).parent if "__file__" in globals() else Path("/home/alpesh/chamunda_re_enterprise")
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = DATA_DIR / "bot_notification_config.json"
HISTORY_FILE = DATA_DIR / "notifications_history.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [AradhyaNotifier] %(message)s"
)
logger = logging.getLogger("AradhyaNotifier")


class AradhyaNotifier:
    """
    Unified notification hub to alert Alpesh Sir immediately when tasks are done
    or if any system issue occurs on the laptop or cloud.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        default_cfg = {
            "authorized_user": "Alpesh Sir (Founder, Chairman & Master Tech)",
            "github_username": "thakoralpesh3",
            "channels": {
                "telegram": {
                    "enabled": True,
                    "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
                    "chat_id": os.getenv("TELEGRAM_CHAT_ID", "") or os.getenv("ALPESH_TELEGRAM_CHAT_ID", ""),
                    "bot_username": "@AradhyaCeoBot"
                },
                "desktop_banner": {
                    "enabled": True
                },
                "whatsapp": {
                    "enabled": True,
                    "target_phone": "917874719139",
                    "callmebot_api_key": os.getenv("CALLMEBOT_API_KEY", ""),
                    "custom_webhook_url": os.getenv("WHATSAPP_WEBHOOK_URL", "")
                }
            },
            "notification_preferences": {
                "work_done": True,
                "system_issues": True,
                "task_failures": True,
                "startup_sync": True,
                "threat_neutralized": True
            }
        }
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    # Environment variable override if config is blank
                    t_cfg = cfg.get("channels", {}).get("telegram", {})
                    if not t_cfg.get("bot_token"):
                        t_cfg["bot_token"] = os.getenv("TELEGRAM_BOT_TOKEN", "")
                    if not t_cfg.get("chat_id"):
                        t_cfg["chat_id"] = os.getenv("TELEGRAM_CHAT_ID", "") or os.getenv("ALPESH_TELEGRAM_CHAT_ID", "")

                    wa_cfg = cfg.setdefault("channels", {}).setdefault("whatsapp", {})
                    if not wa_cfg.get("target_phone"):
                        wa_cfg["target_phone"] = "917874719139"
                    if not wa_cfg.get("callmebot_api_key"):
                        wa_cfg["callmebot_api_key"] = os.getenv("CALLMEBOT_API_KEY", "")
                    if not wa_cfg.get("custom_webhook_url"):
                        wa_cfg["custom_webhook_url"] = os.getenv("WHATSAPP_WEBHOOK_URL", "")
                    return cfg
            except Exception as e:
                logger.debug("Config load error: %s", e)
        return default_cfg

    def send_notification(
        self,
        title: str,
        message: str,
        category: str = "INFO",
        details: Optional[str] = None,
        solution: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Broadcast notification across configured channels (WhatsApp, Telegram, Desktop Banner).
        Categories: WORK_DONE, ISSUE, WARNING, CRITICAL, TASK_FAILURE, STARTUP_SYNC, INFO.
        Always includes actionable solution for issues, task failures, and warnings.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        record = {
            "id": f"NOTIF-{int(time.time())}",
            "timestamp": timestamp,
            "title": title,
            "message": message,
            "category": category,
            "details": details or "",
            "solution": solution or "",
            "dispatched_channels": []
        }

        # 1. Desktop Notification (/usr/bin/notify-send)
        if self.config.get("channels", {}).get("desktop_banner", {}).get("enabled", True):
            dt_ok = self._send_desktop_notification(title, message, category, solution=solution)
            if dt_ok:
                record["dispatched_channels"].append("desktop_banner")

        # 2. Telegram Bot Notification
        tg_cfg = self.config.get("channels", {}).get("telegram", {})
        if tg_cfg.get("enabled", True):
            token = tg_cfg.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN", "")
            chat_id = tg_cfg.get("chat_id") or os.getenv("TELEGRAM_CHAT_ID", "") or os.getenv("ALPESH_TELEGRAM_CHAT_ID", "")
            if token and chat_id:
                tg_ok = self._send_telegram(token, chat_id, title, message, category, details, solution=solution)
                if tg_ok:
                    record["dispatched_channels"].append("telegram")
            else:
                logger.debug("Telegram credentials not set; skipping mobile push.")

        # 3. WhatsApp Notification (CallMeBot API / Custom Webhook / Headless Browser / wa.me link)
        wa_cfg = self.config.get("channels", {}).get("whatsapp", {})
        if wa_cfg.get("enabled", True):
            # Prioritize task failures, critical errors, and system warnings for WhatsApp dispatch
            if category in ["TASK_FAILURE", "CRITICAL", "ISSUE", "WARNING", "ERROR"] or self.config.get("notification_preferences", {}).get("notify_all_to_whatsapp", False):
                wa_ok = self._send_whatsapp(title, message, category, details, solution=solution)
                if wa_ok:
                    record["dispatched_channels"].append("whatsapp")

        # 4. Append to History
        self._record_history(record)
        logger.info("📢 Dispatched [%s] '%s' via: %s", category, title, ", ".join(record["dispatched_channels"]) or "log only")
        return record

    def notify_work_done(self, task_name: str, details: str = "", agent: str = "Aradhya CEO", solution: str = "") -> Dict[str, Any]:
        """Specific helper for completed work."""
        title = f"✅ કામ પૂર્ણ (Work Done): {task_name}"
        msg = f"જય માતાજી અલ્પેશ સાહેબ! {agent} દ્વારા આપનું સોંપેલું કામ સફળતાપૂર્વક પૂર્ણ થઈ ગયું છે."
        return self.send_notification(title=title, message=msg, category="WORK_DONE", details=details, solution=solution)

    def notify_issue(self, issue_title: str, error_details: str = "", severity: str = "WARNING", solution: str = "") -> Dict[str, Any]:
        """Specific helper for system issues or alerts with clear solution."""
        prefix = "🚨 ગંભીર ખામી (Critical Alert)" if severity == "CRITICAL" else "⚠️ સિસ્ટમ સૂચના (System Alert)"
        title = f"{prefix}: {issue_title}"
        msg = f"ધ્યાન આપો અલ્પેશ સાહેબ! સિસ્ટમમાં સમસ્યા જણાઈ છે:\n{error_details}"
        return self.send_notification(title=title, message=msg, category=severity, details=error_details, solution=solution)

    def notify_startup_sync(self, synced_repos_count: int, details: str = "", solution: str = "") -> Dict[str, Any]:
        """Specific helper for laptop startup sync."""
        title = "💻 લેપટોપ શરૂ થયું • GitHub Auto-Sync પૂર્ણ"
        msg = (
            f"જય માતાજી અલ્પેશ સાહેબ! લેપટોપ શરૂ થતાં GitHub પરથી {synced_repos_count} "
            f"રિપોઝીટરીઝ 100% ઓટો-સિન્ક થઈ ગઈ છે. તમામ એજન્ટ્સ અને સર્વિસીસ સક્રિય છે."
        )
        return self.send_notification(title=title, message=msg, category="STARTUP_SYNC", details=details, solution=solution)

    def notify_task_failure(
        self,
        task_name: str,
        error_details: str = "",
        solution: str = "",
        agent: str = "Aradhya CEO"
    ) -> Dict[str, Any]:
        """
        High-priority notification explicitly dispatched to WhatsApp (and all channels)
        when Aradhya Agent is unable to perform an assigned task or mission.
        """
        title = f"🚨 કાર્ય પૂર્ણ ન થઈ શક્યું (Task Incomplete): {task_name}"
        msg = (
            f"ધ્યાન આપો અલ્પેશ સાહેબ! {agent} આપનું સોંપેલું કાર્ય પૂર્ણ કરવામાં અસમર્થ રહી છે:\n"
            f"• કાર્ય: {task_name}\n"
            f"• વિગત/ભૂલ: {error_details[:300] if error_details else 'Execution halted or retries exhausted.'}"
        )
        sol = solution or "કૃપા કરીને ટર્મિનલમાં `aradhya` ચલાવી વિગતવાર સ્થિતિ તપાસો અથવા કમાન્ડ રી-ટ્રાય કરો."
        return self.send_notification(
            title=title,
            message=msg,
            category="TASK_FAILURE",
            details=error_details,
            solution=sol
        )

    def _send_desktop_notification(self, title: str, message: str, category: str, solution: Optional[str] = None) -> bool:
        """Invokes Linux Mint desktop notification with solution."""
        urgency = "critical" if category in ["CRITICAL", "ISSUE", "WARNING"] else "normal"
        full_text = f"{message}"
        if solution:
            full_text += f"\n\n💡 ઉકેલ (Solution):\n{solution}"
        try:
            cmd = [
                "/usr/bin/notify-send",
                "-a", "Aradhya CEO",
                "-u", urgency,
                "-t", "10000",
                title,
                full_text
            ]
            res = subprocess.run(cmd, capture_output=True, timeout=3)
            return res.returncode == 0
        except Exception as e:
            logger.debug("Desktop notify-send error: %s", e)
            return False

    def _send_telegram(
        self,
        token: str,
        chat_id: str | int,
        title: str,
        message: str,
        category: str,
        details: Optional[str],
        solution: Optional[str] = None
    ) -> bool:
        """Sends formatted message via Telegram Bot API with solution block."""
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        icon_map = {
            "WORK_DONE": "✅",
            "CRITICAL": "🚨",
            "WARNING": "⚠️",
            "ISSUE": "⚠️",
            "STARTUP_SYNC": "💻",
            "INFO": "👑"
        }
        icon = icon_map.get(category, "👑")

        text = (
            f"*{icon} Chamunda RE Enterprise • Project Chhaya*\n"
            f"*Authority: Alpesh Sir (Chairman)*\n\n"
            f"*{title}*\n"
            f"{message}\n"
        )
        if details:
            text += f"\n```\n{details[:500]}\n```"
        if solution:
            text += f"\n\n💡 *ઉકેલ / સમાધાન (Solution):*\n`{solution}`"

        text += f"\n\n_Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}_"

        try:
            payload = json.dumps({
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown"
            }).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "AradhyaNotifier/1.0"}
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
                return bool(data.get("ok"))
        except Exception as e:
            logger.warning("Telegram dispatch failed: %s", e)
            return False

    def _send_whatsapp(
        self,
        title: str,
        message: str,
        category: str,
        details: Optional[str],
        solution: Optional[str] = None
    ) -> bool:
        """Sends formatted alert via WhatsAppDispatchEngine directly to Alpesh Sir's WhatsApp."""
        try:
            from whatsapp_dispatch_engine import get_whatsapp_dispatch_engine, OFFICIAL_WHATSAPP_INTL
            wa_engine = get_whatsapp_dispatch_engine()
            wa_cfg = self.config.get("channels", {}).get("whatsapp", {})
            target_phone = wa_cfg.get("target_phone") or OFFICIAL_WHATSAPP_INTL

            if category == "TASK_FAILURE":
                clean_title = re.sub(r'^🚨\s*(?:કાર્ય પૂર્ણ ન થઈ શક્યું|Task Incomplete|Task Failed)\s*:\s*', '', title).strip()
                res = wa_engine.send_task_failure_alert(
                    task_name=clean_title or title,
                    error_details=details or message,
                    solution=solution or "",
                    agent="Aradhya CEO",
                    recipient=target_phone
                )
            else:
                res = wa_engine.send_custom_alert(
                    title=title,
                    message=message,
                    recipient=target_phone,
                    category=category,
                    details=details or "",
                    solution=solution or ""
                )
            return bool(res and res.get("status") in [
                "SENT_VIA_CALLMEBOT",
                "SENT_VIA_WEBHOOK",
                "DISPATCHING_VIA_WHATSAPP_WEB",
                "QUEUED_AND_READY"
            ])
        except Exception as e:
            logger.warning("WhatsApp dispatch attempt failed: %s", e)
            return False

    def _record_history(self, record: Dict[str, Any]):
        """Persists notification record into history file."""
        try:
            history = []
            if HISTORY_FILE.exists():
                try:
                    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []
            history.insert(0, record)
            history = history[:100]  # Keep last 100
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.debug("Failed to record notification history: %s", e)

    def get_recent_notifications(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent notification records."""
        if not HISTORY_FILE.exists():
            return []
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                return history[:limit]
        except Exception:
            return []


_notifier_instance: Optional[AradhyaNotifier] = None

def get_aradhya_notifier() -> AradhyaNotifier:
    global _notifier_instance
    if _notifier_instance is None:
        _notifier_instance = AradhyaNotifier()
    return _notifier_instance


if __name__ == "__main__":
    n = get_aradhya_notifier()
    print("Testing Aradhya Notifier...")
    res = n.notify_work_done("GST Invoice Generation Batch", details="Processed 45 DMS job cards for Classic 350.")
    print("Result:", res)
