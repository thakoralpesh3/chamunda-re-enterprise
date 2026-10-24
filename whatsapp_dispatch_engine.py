"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
Autonomous WhatsApp Dispatch Engine & Real-Time Alert Gateway.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Master Tech)
Official Target WhatsApp: +91 78747 19139
"""

import os
import sys
import time
import json
import logging
import urllib.parse
import urllib.request
import subprocess
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [WhatsAppDispatch] %(message)s"
)
logger = logging.getLogger("WhatsAppDispatch")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTBOX_FILE = DATA_DIR / "whatsapp_outbox.json"
CONFIG_FILE = DATA_DIR / "whatsapp_config.json"

OFFICIAL_WHATSAPP_PHONE = "+91 78747 19139"
OFFICIAL_WHATSAPP_RAW = "7874719139"
OFFICIAL_WHATSAPP_INTL = "917874719139"
DEFAULT_MDNS_URL = "http://alpesh-Inspiron-3542.local:8081"


class WhatsAppDispatchEngine:
    """
    Autonomous engine that broadcasts live link updates and critical alerts
    directly to Alpesh Sir's WhatsApp (+91 78747 19139).
    """

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.outbox_file = data_dir / "whatsapp_outbox.json"
        self.config_file = data_dir / "whatsapp_config.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_outbox()
        self._ensure_config()

    def _ensure_outbox(self):
        if not self.outbox_file.exists():
            try:
                self.outbox_file.write_text("[]", encoding="utf-8")
            except Exception as e:
                logger.error("Failed to initialize outbox file: %s", e)

    def _ensure_config(self):
        if not self.config_file.exists():
            default_cfg = {
                "target_phone": OFFICIAL_WHATSAPP_INTL,
                "callmebot_api_key": "",
                "custom_webhook_url": ""
            }
            try:
                self.config_file.write_text(json.dumps(default_cfg, indent=2), encoding="utf-8")
            except Exception as e:
                logger.error("Failed to initialize config file: %s", e)

    def get_config(self) -> Dict[str, Any]:
        """Read active config from file and environment."""
        cfg = {
            "target_phone": OFFICIAL_WHATSAPP_INTL,
            "callmebot_api_key": os.environ.get("CALLMEBOT_API_KEY", "").strip(),
            "custom_webhook_url": os.environ.get("WHATSAPP_WEBHOOK_URL", "").strip()
        }
        if self.config_file.exists():
            try:
                disk_cfg = json.loads(self.config_file.read_text(encoding="utf-8") or "{}")
                if disk_cfg.get("callmebot_api_key"):
                    cfg["callmebot_api_key"] = disk_cfg["callmebot_api_key"].strip()
                if disk_cfg.get("custom_webhook_url"):
                    cfg["custom_webhook_url"] = disk_cfg["custom_webhook_url"].strip()
                if disk_cfg.get("target_phone"):
                    cfg["target_phone"] = disk_cfg["target_phone"].strip()
            except Exception:
                pass
        return cfg

    def set_config(self, callmebot_api_key: Optional[str] = None, webhook_url: Optional[str] = None) -> Dict[str, Any]:
        """Update config file with new API key or webhook."""
        cfg = self.get_config()
        if callmebot_api_key is not None:
            cfg["callmebot_api_key"] = callmebot_api_key.strip()
        if webhook_url is not None:
            cfg["custom_webhook_url"] = webhook_url.strip()
        try:
            self.config_file.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error("Failed to write config file: %s", e)
        return cfg

    def format_link_notification(
        self,
        public_url: str,
        mdns_url: str = DEFAULT_MDNS_URL,
        reason: str = "લાઈવ લિંક અપડેટ (Live Link Active)",
        permanent_cloud_url: str = ""
    ) -> str:
        """Format a clear, professional bilingual WhatsApp dispatch message."""
        timestamp = time.strftime("%d-%m-%Y %I:%M %p")
        lines = [
            "🏍️ *CHAMUNDA AUTOMOBILE • PROJECT CHHAYA* 🏍️",
            "જય માતાજી અલ્પેશ સાહેબ (Alpesh Sir),",
            "",
            "આપના લેપટોપના તમામ ૨૦ એજન્ટ્સ (Agents) માટે લાઈવ લિંક તૈયાર છે:",
            f"📅 *સમય:* {timestamp}",
            f"🔔 *કારણ:* {reason}",
            ""
        ]

        if permanent_cloud_url:
            lines.extend([
                "☁️ *૨૪/૭ કાયમી ક્લાઉડ લિંક (લેપટોપ બંધ હોય ત્યારે પણ ચાલુ રહેશે):*",
                f"{permanent_cloud_url}",
                ""
            ])

        lines.extend([
            "🌐 *લાઈવ મોબાઈલ લિંક (Online Direct Link):*",
            f"{public_url}",
            "",
            "🏠 *કાયમી લોકલ લિંક (Wi-Fi Permanent Link):*",
            f"{mdns_url}",
            "",
            "⚡ *સક્રિય એજન્ટ્સ:* Aradhya (CEO), Bhairav (Parts), Ramesh (Service), Restomod & Dyno Studio, Kalpavriksha (Growth Engine).",
            "",
            "💡 *ટિપ:* મોબાઈલમાં લિંક ખોલી 'Add to Home Screen' કરવાથી એપ તરીકે સેવ થઈ જશે (ઓફલાઇન પણ ખુલશે).",
            "",
            "— *Aradhya (CEO)*, Chamunda Automobile",
            f"Helpline: {OFFICIAL_WHATSAPP_PHONE}"
        ])
        return "\n".join(lines)

    def generate_click_to_chat_url(self, text: str, recipient: str = OFFICIAL_WHATSAPP_INTL) -> str:
        """Generate official WhatsApp Click-to-Chat URI (wa.me scheme)."""
        clean_phone = "".join(c for c in recipient if c.isdigit())
        encoded_text = urllib.parse.quote(text)
        return f"https://wa.me/{clean_phone}?text={encoded_text}"

    def send_link_update(
        self,
        public_url: str,
        recipient: str = OFFICIAL_WHATSAPP_INTL,
        trigger_reason: str = "AUTOMATIC_TUNNEL_SYNC",
        mdns_url: str = DEFAULT_MDNS_URL,
        permanent_cloud_url: str = ""
    ) -> Dict[str, Any]:
        """
        Dispatch the active link to WhatsApp.
        1. Formats bilingual alert.
        2. Generates 1-click wa.me URL.
        3. Attempts CallMeBot API if apikey configured.
        4. Attempts Webhook if configured.
        5. Emits system notification on laptop.
        6. Logs in outbox.
        """
        clean_phone = "".join(c for c in recipient if c.isdigit())
        if not clean_phone:
            clean_phone = OFFICIAL_WHATSAPP_INTL

        message = self.format_link_notification(public_url, mdns_url=mdns_url, permanent_cloud_url=permanent_cloud_url)
        wa_click_url = self.generate_click_to_chat_url(message, clean_phone)

        record = {
            "dispatch_id": f"WA-CHHAYA-{int(time.time())}",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "recipient_raw": clean_phone,
            "recipient_formatted": OFFICIAL_WHATSAPP_PHONE if clean_phone.endswith(OFFICIAL_WHATSAPP_RAW) else f"+{clean_phone}",
            "public_url": public_url,
            "permanent_cloud_url": permanent_cloud_url,
            "mdns_url": mdns_url,
            "trigger_reason": trigger_reason,
            "message": message,
            "wa_click_url": wa_click_url,
            "status": "QUEUED_AND_READY",
            "channels_attempted": []
        }

        # Load configuration
        cfg = self.get_config()

        # Channel 1: CallMeBot API (if apikey available)
        callmebot_key = cfg.get("callmebot_api_key", "").strip()
        if callmebot_key:
            try:
                cm_url = (
                    f"https://api.callmebot.com/whatsapp.php?"
                    f"phone=+{clean_phone}&text={urllib.parse.quote(message)}&apikey={callmebot_key}"
                )
                req = urllib.request.Request(cm_url, headers={"User-Agent": "ChamundaChhaya/1.0"})
                with urllib.request.urlopen(req, timeout=8.0) as resp:
                    resp_body = resp.read().decode("utf-8", errors="ignore")
                    record["channels_attempted"].append({
                        "channel": "CallMeBot_API",
                        "success": True,
                        "response": resp_body[:100]
                    })
                    record["status"] = "SENT_VIA_CALLMEBOT"
                    logger.info("WhatsApp dispatched via CallMeBot API to %s", clean_phone)
            except Exception as e:
                logger.warning("CallMeBot dispatch error: %s", e)
                record["channels_attempted"].append({
                    "channel": "CallMeBot_API",
                    "success": False,
                    "error": str(e)
                })

        # Channel 2: Custom Webhook (if webhook available)
        webhook_url = cfg.get("custom_webhook_url", "").strip()
        if webhook_url:
            try:
                payload = json.dumps({
                    "phone": clean_phone,
                    "message": message,
                    "public_url": public_url,
                    "mdns_url": mdns_url,
                    "timestamp": record["timestamp"]
                }).encode("utf-8")
                req = urllib.request.Request(
                    webhook_url,
                    data=payload,
                    headers={"Content-Type": "application/json", "User-Agent": "ChamundaChhaya/1.0"}
                )
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    record["channels_attempted"].append({
                        "channel": "Custom_Webhook",
                        "success": True,
                        "code": resp.getcode()
                    })
                    record["status"] = "SENT_VIA_WEBHOOK"
                    logger.info("WhatsApp dispatched via Webhook to %s", clean_phone)
            except Exception as e:
                logger.warning("Webhook dispatch error: %s", e)
                record["channels_attempted"].append({
                    "channel": "Custom_Webhook",
                    "success": False,
                    "error": str(e)
                })

        # Channel 3: Autonomous WhatsApp Web Headless Dispatcher
        try:
            from whatsapp_web_sender import get_whatsapp_web_sender
            web_sender = get_whatsapp_web_sender()
            session_info = web_sender.get_session_info()
            if session_info.get("paired", False):
                dispatch_id = record["dispatch_id"]

                def _do_web_dispatch():
                    try:
                        web_res = web_sender.send_message(clean_phone, message, headless=True)
                        logger.info("WhatsApp Web automated dispatch result: %s", web_res)
                        self._update_outbox_channel_result(dispatch_id, "WhatsApp_Web_Headless", web_res)
                        if web_res.get("success"):
                            subprocess.Popen(
                                [
                                    "notify-send",
                                    "-a", "Project Chhaya",
                                    "-i", str(BASE_DIR / "static" / "icons" / "icon-192.png"),
                                    "✅ Chhaya Link Delivered to WhatsApp",
                                    f"Delivered to: +{clean_phone}\nLink: {public_url}"
                                ],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL
                            )
                        else:
                            st = web_res.get('status', 'ERROR')
                            logger.warning("WhatsApp Web automated dispatch unsuccessful: %s (%s)", st, web_res.get('details', ''))
                            if st == "QR_PAIRING_REQUIRED":
                                subprocess.Popen(
                                    [
                                        "notify-send",
                                        "-u", "critical",
                                        "-a", "Project Chhaya",
                                        "-i", str(BASE_DIR / "static" / "icons" / "icon-192.png"),
                                        "📱 WhatsApp Pairing Required",
                                        "Please scan the QR code to re-link WhatsApp Web."
                                    ],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL
                                )
                    except Exception as we:
                        logger.warning("WhatsApp Web thread error: %s", we)
                        self._update_outbox_channel_result(dispatch_id, "WhatsApp_Web_Headless", {"success": False, "error": str(we)})

                t = threading.Thread(target=_do_web_dispatch, daemon=True)
                t.start()
                record["channels_attempted"].append({
                    "channel": "WhatsApp_Web_Headless",
                    "success": True,
                    "status": "DISPATCH_STARTED"
                })
                record["status"] = "DISPATCHING_VIA_WHATSAPP_WEB"
            else:
                record["channels_attempted"].append({
                    "channel": "WhatsApp_Web_Headless",
                    "success": False,
                    "status": "NOT_YET_PAIRED",
                    "details": "Run 'python3 whatsapp_web_sender.py --pair' to link WhatsApp Web on screen."
                })
        except Exception as e:
            logger.warning("WhatsApp Web sender integration error: %s", e)

        # Channel 4: Desktop UI Notification on Laptop (In-progress alert)
        try:
            subprocess.Popen(
                [
                    "notify-send",
                    "-a", "Project Chhaya",
                    "-i", str(BASE_DIR / "static" / "icons" / "icon-192.png"),
                    "🚀 Dispatching Chhaya Link to WhatsApp...",
                    f"Recipient: {OFFICIAL_WHATSAPP_PHONE}\nLink: {public_url}"
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            record["channels_attempted"].append({
                "channel": "Desktop_Notification",
                "success": True
            })
        except Exception:
            pass

        # Channel 4: Click-to-Chat Ready URL (Always guaranteed functional)
        record["channels_attempted"].append({
            "channel": "WhatsApp_Click_To_Chat",
            "success": True,
            "url": wa_click_url
        })

        # Save to outbox
        self._record_in_outbox(record)
        logger.info(
            "✅ [WhatsApp Alert] Link dispatched for %s | Status: %s | URL: %s",
            OFFICIAL_WHATSAPP_PHONE, record["status"], public_url
        )
        return record

    def _record_in_outbox(self, record: Dict[str, Any]):
        """Append record to outbox, capping at 100 entries."""
        try:
            outbox = []
            if self.outbox_file.exists():
                try:
                    outbox = json.loads(self.outbox_file.read_text(encoding="utf-8") or "[]")
                except Exception:
                    outbox = []
            outbox.insert(0, record)
            outbox = outbox[:100]
            self.outbox_file.write_text(json.dumps(outbox, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error("Error writing outbox: %s", e)

    def _update_outbox_channel_result(self, dispatch_id: str, channel_name: str, result: Dict[str, Any]):
        """Update an existing outbox entry once background dispatch finishes."""
        try:
            if not self.outbox_file.exists():
                return
            outbox = json.loads(self.outbox_file.read_text(encoding="utf-8") or "[]")
            for entry in outbox:
                if entry.get("dispatch_id") == dispatch_id:
                    if result.get("success"):
                        entry["status"] = "DELIVERED_VIA_WHATSAPP_WEB"
                    else:
                        entry["status"] = "WHATSAPP_WEB_FAILED"
                    for ch in entry.get("channels_attempted", []):
                        if ch.get("channel") == channel_name:
                            ch["success"] = result.get("success", False)
                            ch["final_result"] = result
                            break
                    break
            self.outbox_file.write_text(json.dumps(outbox, indent=2, ensure_ascii=False), encoding="utf-8")
            logger.info("Updated outbox record %s status: %s", dispatch_id, result.get("status", "COMPLETED"))
        except Exception as e:
            logger.error("Error updating outbox record %s: %s", dispatch_id, e)

    def get_latest_outbox(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent outbox records."""
        try:
            if self.outbox_file.exists():
                outbox = json.loads(self.outbox_file.read_text(encoding="utf-8") or "[]")
                return outbox[:limit]
        except Exception:
            pass
        return []


_whatsapp_engine: Optional[WhatsAppDispatchEngine] = None


def get_whatsapp_dispatch_engine() -> WhatsAppDispatchEngine:
    global _whatsapp_engine
    if _whatsapp_engine is None:
        _whatsapp_engine = WhatsAppDispatchEngine()
    return _whatsapp_engine


if __name__ == "__main__":
    eng = get_whatsapp_dispatch_engine()
    test_res = eng.send_link_update(
        "http://alpesh-Inspiron-3542.local:8081",
        trigger_reason="MANUAL_CLI_TEST"
    )
    print("Test dispatch result:")
    print(json.dumps(test_res, indent=2, ensure_ascii=False))
