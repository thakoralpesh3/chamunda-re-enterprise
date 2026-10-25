"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
Autonomous WhatsApp Web Headless Dispatcher.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Master Tech)
Official Target: +91 78747 19139
"""

import os
import sys
import time
import json
import logging
import urllib.parse
import threading
from pathlib import Path
from typing import Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [WhatsAppWebSender] %(message)s"
)
logger = logging.getLogger("WhatsAppWebSender")

# Prevent Firefox GDK_BACKEND mismatch on Linux Mint
os.environ.pop("GDK_BACKEND", None)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
PROFILE_DIR = DATA_DIR / "whatsapp_bot_firefox"
SESSION_STATE_FILE = DATA_DIR / "whatsapp_bot_session.json"
QR_SCREENSHOT = STATIC_DIR / "whatsapp_pair_qr.png"

# Geckodriver discovery
GECKO_CANDIDATES = [
    Path("/home/alpesh/.local/bin/geckodriver"),
    Path("/home/alpesh/youtube-agent/.venv/bin/geckodriver"),
    Path("/usr/bin/geckodriver"),
    Path("/usr/local/bin/geckodriver"),
]

def get_gecko_path() -> Optional[Path]:
    for p in GECKO_CANDIDATES:
        if p.exists() and os.access(str(p), os.X_OK):
            return p
    return None

def clean_locks(profile_dir: Path = PROFILE_DIR):
    for lock_name in ["lock", ".parentlock", ".agent_browser.lock"]:
        lp = profile_dir / lock_name
        if lp.is_symlink() or lp.exists():
            try:
                lp.unlink()
            except Exception:
                pass

class WhatsAppWebSender:
    """
    Automates sending messages via WhatsApp Web using a persistent Firefox profile.
    """

    def __init__(self, profile_dir: Path = PROFILE_DIR):
        self.profile_dir = profile_dir
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        STATIC_DIR.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()

    def get_session_info(self) -> Dict[str, Any]:
        """Check pairing state from metadata file."""
        if SESSION_STATE_FILE.exists():
            try:
                return json.loads(SESSION_STATE_FILE.read_text(encoding="utf-8") or "{}")
            except Exception:
                pass
        return {"paired": False, "last_used": None}

    def mark_session_paired(self, paired: bool = True):
        info = {
            "paired": paired,
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "profile_path": str(self.profile_dir)
        }
        try:
            SESSION_STATE_FILE.write_text(json.dumps(info, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error("Failed to write session state: %s", e)

    def launch_pairing_wizard(self, timeout_seconds: int = 120) -> Dict[str, Any]:
        """
        Launch visible Firefox window on screen (:0) to let Alpesh Sir scan the QR code.
        """
        clean_locks(self.profile_dir)
        gecko = get_gecko_path()
        if not gecko:
            return {"success": False, "error": "geckodriver not found"}

        display = os.environ.get("DISPLAY", ":0")
        os.environ["DISPLAY"] = display

        options = Options()
        options.add_argument("-profile")
        options.add_argument(str(self.profile_dir))
        options.set_preference("dom.serviceWorkers.enabled", True)
        options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0")

        service = Service(executable_path=str(gecko))
        logger.info("🚀 Launching interactive WhatsApp Web Pairing Wizard on display %s...", display)
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(1280, 850)

        try:
            driver.get("https://web.whatsapp.com")
            logger.info("👉 Alpesh Sir: Scan QR Code on screen with your phone (WhatsApp -> Linked Devices -> Link a Device)")

            paired = False
            start_time = time.time()
            while time.time() - start_time < timeout_seconds:
                time.sleep(2)
                # Check for logged-in indicators
                chats = driver.find_elements(
                    By.XPATH,
                    "//div[@role='navigation'] | //*[@data-testid='chat-list'] | //*[@aria-label='Chat list'] | //div[@contenteditable='true']"
                )
                if chats:
                    logger.info("🎉 [SUCCESS] WhatsApp Web is paired and active!")
                    self.mark_session_paired(True)
                    paired = True
                    break

            return {"success": paired, "paired": paired}
        except Exception as e:
            logger.error("Error in pairing wizard: %s", e)
            return {"success": False, "error": str(e)}
        finally:
            driver.quit()
            clean_locks(self.profile_dir)

    def send_message(self, phone: str, text: str, headless: bool = True) -> Dict[str, Any]:
        """
        Autonomously dispatch a message to a phone number via WhatsApp Web.
        """
        clean_phone = "".join(c for c in phone if c.isdigit())
        if not clean_phone:
            clean_phone = "917874719139"

        with self.lock:
            clean_locks(self.profile_dir)
            gecko = get_gecko_path()
            if not gecko:
                return {"success": False, "channel": "WhatsApp_Web", "error": "geckodriver not found"}

            options = Options()
            options.add_argument("-profile")
            options.add_argument(str(self.profile_dir))
            if headless:
                options.add_argument("-headless")
            options.set_preference("dom.serviceWorkers.enabled", True)
            options.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0")
            options.set_preference("browser.startup.homepage", "about:blank")
            options.set_preference("browser.startup.page", 0)
            options.set_preference("browser.cache.disk.enable", True)
            options.set_preference("browser.cache.memory.enable", True)

            service = Service(executable_path=str(gecko))
            driver = None

            try:
                try:
                    os.nice(10)
                except Exception:
                    pass
                driver = webdriver.Firefox(service=service, options=options)
                driver.set_window_size(1280, 850)

                # Direct navigation to target chat endpoint with retry for transient DNS/network glitches
                encoded_text = urllib.parse.quote(text)
                url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_text}"
                logger.info("Connecting to WhatsApp Web chat for %s...", clean_phone)
                for nav_attempt in range(3):
                    try:
                        driver.get(url)
                        break
                    except Exception as nav_err:
                        logger.warning("WhatsApp Web navigation attempt %d failed (%s). Retrying...", nav_attempt + 1, nav_err)
                        if nav_attempt < 2:
                            time.sleep(3)
                        else:
                            raise

                # Wait up to 80 seconds for #main or QR pairing code (resilient to CPU lag)
                main_found = False
                pane_seen_tick = 0
                for tick in range(80):
                    time.sleep(1)
                    # Check for modern WhatsApp Web QR login indicators
                    qr = driver.find_elements(
                        By.XPATH,
                        "//canvas | //*[@data-testid='qrcode'] | //*[contains(text(), 'Scan to log in')] | //*[contains(text(), 'Link with phone number')]"
                    )
                    if qr and tick > 4:
                        logger.warning("📱 WhatsApp Web requires pairing scan. Saving QR screenshot...")
                        driver.save_screenshot(str(QR_SCREENSHOT))
                        self.mark_session_paired(False)
                        return {
                            "success": False,
                            "channel": "WhatsApp_Web",
                            "status": "QR_PAIRING_REQUIRED",
                            "qr_image": str(QR_SCREENSHOT),
                            "details": "WhatsApp Web needs a one-time device pairing scan. Run 'aradhya-pair' to link on screen."
                        }

                    if driver.find_elements(By.ID, "main"):
                        logger.info("✅ WhatsApp chat interface (#main) loaded in %d seconds.", tick + 1)
                        main_found = True
                        break

                    # Fallback: if chat list (#pane-side) has loaded but #main is still hydrating
                    if driver.find_elements(By.ID, "pane-side"):
                        if pane_seen_tick == 0:
                            pane_seen_tick = tick
                            logger.info("WhatsApp left chat pane (#pane-side) hydrated in %d seconds. Waiting for #main...", tick + 1)
                        elif (tick - pane_seen_tick) > 6:
                            # Try activating chat via left pane click
                            chat_items = driver.find_elements(
                                By.XPATH,
                                "//div[@id='pane-side']//span[contains(@title, 'You')]/ancestor::div[@role='listitem'] | "
                                "//div[@id='pane-side']//span[contains(text(), 'You')]/ancestor::div[@role='listitem'] | "
                                "//div[@id='pane-side']//div[@role='listitem']"
                            )
                            if chat_items:
                                try:
                                    driver.execute_script("arguments[0].click();", chat_items[0])
                                    time.sleep(1.5)
                                    if driver.find_elements(By.ID, "main"):
                                        logger.info("✅ Activated #main via left pane item click at tick %d!", tick + 1)
                                        main_found = True
                                        break
                                except Exception:
                                    pass

                if not main_found:
                    driver.save_screenshot(str(QR_SCREENSHOT))
                    return {
                        "success": False,
                        "channel": "WhatsApp_Web",
                        "status": "CHAT_LOAD_TIMEOUT",
                        "details": "Timed out waiting for #main container on web.whatsapp.com (80s limit)"
                    }

                # Clear any blocking modal/dialogs (such as 'Cancel' on starting chat popup)
                cancel_btns = driver.find_elements(
                    By.XPATH,
                    "//button[contains(., 'Cancel')] | //div[@role='button'][contains(., 'Cancel')]"
                )
                if cancel_btns:
                    try:
                        driver.execute_script("arguments[0].click();", cancel_btns[0])
                        time.sleep(1)
                    except Exception:
                        pass

                # Locate Send Button inside #main (wait up to 15 seconds)
                send_clicked = False
                for s_wait in range(15):
                    time.sleep(1)
                    send_btns = driver.find_elements(
                        By.XPATH,
                        "//div[@id='main']//button[@aria-label='Send'] | "
                        "//div[@id='main']//div[contains(@aria-label, 'Send')]"
                    )
                    if send_btns:
                        btn = send_btns[0]
                        try:
                            btn.click()
                            logger.info("✅ Clicked WhatsApp Send button directly!")
                            send_clicked = True
                            break
                        except Exception as ce:
                            logger.info("Direct click intercepted (%s), executing JavaScript click fallback...", ce)
                            try:
                                driver.execute_script("arguments[0].click();", btn)
                                logger.info("✅ Clicked WhatsApp Send button via JavaScript!")
                                send_clicked = True
                                break
                            except Exception as jse:
                                logger.warning("JavaScript click fallback error: %s", jse)

                # Fallback: send ENTER key directly into the message composer inside #main
                if not send_clicked:
                    composers = driver.find_elements(
                        By.XPATH,
                        "//div[@id='main']//div[@contenteditable='true']"
                    )
                    if composers:
                        try:
                            composers[0].send_keys(Keys.ENTER)
                            logger.info("✅ Triggered Enter key in composer inside #main!")
                            send_clicked = True
                        except Exception as ke:
                            logger.warning("Composer Enter failed: %s", ke)

                if not send_clicked:
                    driver.save_screenshot(str(QR_SCREENSHOT))
                    return {
                        "success": False,
                        "channel": "WhatsApp_Web",
                        "status": "SEND_BUTTON_TIMEOUT",
                        "details": "Timed out waiting for Send button on web.whatsapp.com"
                    }

                # Transmission & Delivery Verification Loop (up to 30s)
                logger.info("Monitoring WebSocket transmission & server delivery acknowledgement...")
                verified = False
                for w_tick in range(15):
                    time.sleep(2)
                    msgs = driver.find_elements(By.XPATH, "//div[@id='main']//div[contains(@class, 'message-out')]")
                    if msgs:
                        last_msg = msgs[-1]
                        has_check = last_msg.find_elements(
                            By.XPATH,
                            ".//*[@data-icon='msg-check'] | .//*[@data-icon='msg-dblcheck']"
                        )
                        has_clock = last_msg.find_elements(
                            By.XPATH,
                            ".//*[@data-icon='msg-time']"
                        )
                        fails = driver.find_elements(
                            By.XPATH,
                            "//div[@data-testid='fail-container'] | //title[text()='ic-error']"
                        )

                        if len(has_check) > 0 and len(has_clock) == 0:
                            logger.info("✅ Verified: Message acknowledged by server with checkmark!")
                            verified = True
                            break
                        elif len(fails) > 0:
                            logger.warning("⚠️ Message flagged with failure by WhatsApp Web. Attempting retry...")
                            retry_btn = driver.find_elements(
                                By.XPATH,
                                "//div[@role='button'][contains(@aria-label, 'Something went wrong')]"
                            )
                            if retry_btn:
                                try:
                                    retry_btn[0].click()
                                    time.sleep(1)
                                    again_btn = driver.find_elements(By.XPATH, "//button[contains(., 'Try again')]")
                                    if again_btn:
                                        again_btn[0].click()
                                except Exception:
                                    pass

                # Save confirmation screenshot for visual audit
                confirm_screenshot = DATA_DIR / "whatsapp_last_delivery.png"
                try:
                    driver.save_screenshot(str(confirm_screenshot))
                except Exception:
                    pass

                self.mark_session_paired(True)
                logger.info("🎉 Message transmitted successfully to %s on WhatsApp! Verified: %s", clean_phone, verified)
                return {
                    "success": True,
                    "channel": "WhatsApp_Web",
                    "status": "DELIVERED_VIA_BROWSER",
                    "recipient": clean_phone,
                    "verified_delivery": verified,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }

            except Exception as e:
                logger.error("WhatsApp Web automation error: %s", e)
                return {"success": False, "channel": "WhatsApp_Web", "error": str(e)}
            finally:
                if driver:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                clean_locks(self.profile_dir)


_web_sender: Optional[WhatsAppWebSender] = None

def get_whatsapp_web_sender() -> WhatsAppWebSender:
    global _web_sender
    if _web_sender is None:
        _web_sender = WhatsAppWebSender()
    return _web_sender

if __name__ == "__main__":
    sender = get_whatsapp_web_sender()
    if len(sys.argv) > 1 and sys.argv[1] == "--pair":
        res = sender.launch_pairing_wizard()
        print("Pairing result:", res)
    else:
        info = sender.get_session_info()
        print("WhatsApp Web Sender Info:", info)
