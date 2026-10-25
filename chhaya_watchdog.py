"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
24/7 Autonomous Watchdog & Resilient Cloud Mirror Supervisor.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. 24/7 Process Supervision: Keeps cloud_mirror_server.py running continuously on port 8081.
2. Auto-Restart on Crash: Detects process exit or HTTP failure and restarts within 3 seconds.
3. Heartbeat Telemetry: Writes continuous heartbeats to cloud_shadow_state.json every 15 seconds.
4. Memory Self-Trimming: Periodically invokes Python gc.collect() and C malloc_trim(0) to stay lean (<45MB).
5. 24/7 Public Mobile Access: Supervised SSH reverse tunnel (localhost.run over Port 22) for 100% reliable HTTPS on any mobile network.
6. Dynamic QR Code Generation: Encodes the live public HTTPS link for 1-tap camera access from any phone.
"""

import os
import sys
import time
import json
import socket
import signal
import ctypes
import re
import urllib.request
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [ChhayaWatchdog] %(message)s"
)
logger = logging.getLogger("ChhayaWatchdog")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
BRAIN_DIR = Path("/home/alpesh/.gemini/antigravity/brain/c2f8252a-5273-4c4e-ae3c-b25c4e717e70")
STATE_FILE = DATA_DIR / "cloud_shadow_state.json"
PID_FILE = DATA_DIR / "chhaya_mirror.pid"
TUNNEL_URL_FILE = DATA_DIR / "chhaya_public_url.txt"
TUNNEL_LOG_FILE = DATA_DIR / "chhaya_tunnel.log"
WATCHDOG_LOG = DATA_DIR / "chhaya_watchdog.log"
CF_CONFIG_FILE = DATA_DIR / "cloudflare_config.json"


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def get_local_lan_ip() -> str:
    """Detect local active LAN/Wi-Fi/Hotspot IP address dynamically."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        if not ip.startswith("127."):
            return ip
    except Exception:
        pass
    return "127.0.0.1"


def trim_process_memory():
    """Trigger Python garbage collection and Linux malloc_trim to keep memory lean."""
    try:
        import gc
        gc.collect()
        libc = ctypes.CDLL("libc.so.6")
        libc.malloc_trim(0)
    except Exception:
        pass


class Chhaya247Watchdog:
    """
    Supervises the 24/7 Cloud Shadow Standby Mirror Server on port 8081,
    the SSH Reverse Tunnel (localhost.run) for mobile access, and dynamic QR generation.
    """

    def __init__(self, port: int = 8081):
        self.port = port
        self.server_proc: Optional[subprocess.Popen] = None
        self.tunnel_proc: Optional[subprocess.Popen] = None
        self.running = True
        self.last_tunnel_url = ""
        self.tunnel_fail_count = 0
        self._last_dispatch_time = 0.0
        self._min_dispatch_interval = 60.0  # Minimum 60 seconds debounce between automated WhatsApp link updates
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        STATIC_DIR.mkdir(parents=True, exist_ok=True)

    def get_cf_config(self) -> Dict[str, Any]:
        """Read persistent Cloudflare Zero Trust / Cloud Mirror config."""
        if CF_CONFIG_FILE.exists():
            try:
                return json.loads(CF_CONFIG_FILE.read_text(encoding="utf-8") or "{}")
            except Exception:
                pass
        return {}

    def generate_qr_code(self, target_url: str):
        """Generate high-contrast mobile QR code pointing to target_url."""
        try:
            import qrcode
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(target_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#e53935", back_color="#0a0e17")
            img.save(str(STATIC_DIR / "chhaya_mobile_qr.png"))
            if BRAIN_DIR.exists():
                img.save(str(BRAIN_DIR / "chhaya_mobile_qr.png"))
            logger.info("📱 Mobile QR code generated for %s", target_url)
        except Exception as e:
            logger.warning("Could not generate QR code: %s", e)

    def start_mirror_server(self) -> bool:
        """Launch cloud_mirror_server.py as a managed subprocess."""
        if is_port_in_use(self.port):
            logger.info("Port %d is already in use. Checking if healthy...", self.port)
            if self.check_health():
                logger.info("Existing server on port %d is healthy.", self.port)
                return True
            else:
                logger.warning("Port %d is unresponsive. Freeing port...", self.port)
                os.system(f"fuser -k {self.port}/tcp >/dev/null 2>&1 || true")
                time.sleep(1)

        server_script = BASE_DIR / "cloud_mirror_server.py"
        env = os.environ.copy()
        env["PORT"] = str(self.port)

        logger.info("Starting Cloud Mirror Server on port %d...", self.port)
        log_out = open(DATA_DIR / "chhaya_mirror_server.log", "a", encoding="utf-8")

        self.server_proc = subprocess.Popen(
            [sys.executable, str(server_script)],
            cwd=str(BASE_DIR),
            env=env,
            stdout=log_out,
            stderr=log_out,
            start_new_session=True
        )

        with open(PID_FILE, "w") as f:
            f.write(str(self.server_proc.pid))

        # Wait up to 5 seconds for health
        for _ in range(10):
            time.sleep(0.5)
            if self.check_health():
                logger.info("✅ Cloud Mirror Server is healthy on http://127.0.0.1:%d (PID: %d)", self.port, self.server_proc.pid)
                return True

        logger.error("Failed to verify Cloud Mirror Server health on port %d", self.port)
        return False

    def check_health(self) -> bool:
        """Ping /api/health endpoint with generous timeout for high CPU loads."""
        try:
            url = f"http://127.0.0.1:{self.port}/api/health"
            req = urllib.request.Request(url, headers={"User-Agent": "ChhayaWatchdog/1.0"})
            with urllib.request.urlopen(req, timeout=15.0) as resp:
                data = json.loads(resp.read().decode())
                return data.get("status") == "HEALTHY_HOT_STANDBY"
        except Exception:
            return False

    def sync_tunnel_url(self) -> Optional[str]:
        """Parse active HTTPS URL from TUNNEL_LOG_FILE or permanent Cloudflare config, notify WhatsApp 7874719139 with debouncing, and regenerate QR code."""
        cf_cfg = self.get_cf_config()
        pub_url = None

        # 1. If permanent custom domain configured in Cloudflare Zero Trust
        if cf_cfg.get("permanent_domain"):
            pub_url = cf_cfg["permanent_domain"].strip()
        elif TUNNEL_LOG_FILE.exists():
            try:
                with open(TUNNEL_LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                matches = re.findall(r"https://[a-zA-Z0-9-]+\.(?:trycloudflare\.com|lhr\.life)", content)
                if matches:
                    valid_urls = [
                        m.strip() for m in matches
                        if not any(x in m for x in ["api.trycloudflare.com", "pkg.cloudflare.com", "developers.cloudflare.com"])
                    ]
                    if valid_urls:
                        pub_url = valid_urls[-1].strip()
            except Exception as e:
                logger.debug("Tunnel URL read error: %s", e)

        if not pub_url:
            return None

        try:
            current_url = ""
            if TUNNEL_URL_FILE.exists():
                try:
                    current_url = TUNNEL_URL_FILE.read_text(encoding="utf-8").strip()
                except Exception:
                    pass

            now = time.time()
            time_since_last_dispatch = now - self._last_dispatch_time
            should_dispatch = False
            trigger_reason = "TUNNEL_URL_CHANGED"

            if pub_url != current_url or pub_url != self.last_tunnel_url:
                TUNNEL_URL_FILE.write_text(pub_url, encoding="utf-8")
                self.last_tunnel_url = pub_url
                logger.info("🌐 Mobile Public URL updated: %s", pub_url)
                self.generate_qr_code(pub_url)

                # Only dispatch if first boot or debounced past minimum interval
                if self._last_dispatch_time == 0 or time_since_last_dispatch >= self._min_dispatch_interval:
                    should_dispatch = True
                else:
                    logger.info("⏳ WhatsApp dispatch debounced (%ds elapsed < %ds min interval). Link saved to disk.", int(time_since_last_dispatch), int(self._min_dispatch_interval))

            if should_dispatch:
                self._last_dispatch_time = now
                try:
                    from whatsapp_dispatch_engine import get_whatsapp_dispatch_engine
                    active_lan_ip = get_local_lan_ip()
                    get_whatsapp_dispatch_engine().send_link_update(
                        pub_url,
                        recipient="917874719139",
                        trigger_reason=trigger_reason,
                        mdns_url=f"http://alpesh-Inspiron-3542.local:{self.port}",
                        lan_url=f"http://{active_lan_ip}:{self.port}",
                        permanent_cloud_url=cf_cfg.get("permanent_cloud_url", "https://github.com/thakoralpesh3/chamunda-re-enterprise")
                    )
                except Exception as we:
                    logger.error("WhatsApp dispatch trigger error: %s", we)
            return pub_url
        except Exception as e:
            logger.debug("Tunnel URL sync error: %s", e)
        return None

    def stop_public_tunnel(self):
        """Cleanly terminate running tunnel process for this watchdog port."""
        if self.tunnel_proc:
            try:
                logger.info("Terminating public tunnel process (PID: %d)...", self.tunnel_proc.pid)
                self.tunnel_proc.terminate()
                try:
                    self.tunnel_proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.tunnel_proc.kill()
                    self.tunnel_proc.wait(timeout=2)
            except Exception as e:
                logger.debug("Error terminating tunnel_proc: %s", e)
            self.tunnel_proc = None

        # Clean up any orphan cloudflared process listening on this port specifically
        try:
            subprocess.run(["pkill", "-f", f"cloudflared.*{self.port}"], check=False)
        except Exception:
            pass

    def restart_public_tunnel(self, reason: str = "health_check_failed"):
        """Auto-heal dropped/stale public tunnel by terminating and relaunching."""
        logger.warning("🔄 Auto-healing public tunnel (Reason: %s)...", reason)
        self.stop_public_tunnel()
        time.sleep(1)
        self.tunnel_fail_count = 0
        self.start_public_tunnel()

    def start_public_tunnel(self):
        """Start Cloudflare Tunnel (Named Zero Trust or Quick Tunnel) or fallback SSH reverse tunnel."""
        if self.tunnel_proc and self.tunnel_proc.poll() is None:
            self.sync_tunnel_url()
            return  # Tunnel is already running stably

        cloudflared_bin = BASE_DIR / "bin" / "cloudflared"
        tunnel_log = open(TUNNEL_LOG_FILE, "w", encoding="utf-8", buffering=1)
        cf_cfg = self.get_cf_config()

        if cloudflared_bin.exists() and os.access(str(cloudflared_bin), os.X_OK):
            if cf_cfg.get("tunnel_token"):
                logger.info("Starting Cloudflare Zero Trust Named Tunnel using persistent token for permanent link...")
                cmd = [
                    str(cloudflared_bin),
                    "tunnel",
                    "run",
                    "--token", cf_cfg["tunnel_token"].strip()
                ]
            else:
                logger.info("Starting Cloudflare Quick Tunnel for mobile access on port %d...", self.port)
                cmd = [
                    str(cloudflared_bin),
                    "tunnel",
                    "--protocol", "http2",
                    "--edge-ip-version", "4",
                    "--url", f"http://127.0.0.1:{self.port}"
                ]
        else:
            logger.info("Starting SSH reverse tunnel (localhost.run) for mobile access on port %d...", self.port)
            cmd = [
                "stdbuf", "-oL", "-eL",
                "ssh", "-T",
                "-o", "StrictHostKeyChecking=no",
                "-o", "ServerAliveInterval=30",
                "-o", "ServerAliveCountMax=3",
                "-o", "ExitOnForwardFailure=yes",
                "-R", f"80:localhost:{self.port}",
                "nokey@localhost.run"
            ]

        self.tunnel_proc = subprocess.Popen(
            cmd,
            cwd=str(BASE_DIR),
            stdout=tunnel_log,
            stderr=tunnel_log,
            start_new_session=True
        )

        for _ in range(35):
            time.sleep(0.5)
            url = self.sync_tunnel_url()
            if url:
                logger.info("✅ Global Mobile Access URL is live: %s", url)
                break

    def check_tunnel_health(self) -> bool:
        """Probe public tunnel endpoint to ensure it has not gone stale."""
        if not self.last_tunnel_url or not any(d in self.last_tunnel_url for d in ["trycloudflare.com", "lhr.life"]):
            return False

        # Fast detection: Check if tunnel log has edge revocation errors
        if TUNNEL_LOG_FILE.exists():
            try:
                size = TUNNEL_LOG_FILE.stat().st_size
                with open(TUNNEL_LOG_FILE, "rb") as f:
                    f.seek(max(0, size - 8192))
                    tail_content = f.read().decode("utf-8", errors="ignore")
                    if "Unauthorized: Tunnel not found" in tail_content:
                        logger.warning("⚠️ Cloudflare quick tunnel dropped by edge: 'Unauthorized: Tunnel not found'")
                        return False
            except Exception as e:
                logger.debug("Log probe error: %s", e)

        try:
            req = urllib.request.Request(
                f"{self.last_tunnel_url}/api/health",
                headers={"User-Agent": "ChhayaTunnelProbe/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                data = json.loads(resp.read().decode())
                return data.get("status") == "HEALTHY_HOT_STANDBY"
        except Exception:
            return False

    def update_heartbeat_in_state(self):
        """Update last heartbeat timestamp in state file."""
        if not STATE_FILE.exists():
            return
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
            state["last_heartbeat"] = time.strftime("%Y-%m-%d %H:%M:%S")
            state["watchdog_status"] = "24_7_SUPERVISED_ACTIVE"
            state["local_ip"] = get_local_lan_ip()
            state["local_mobile_url"] = f"http://{get_local_lan_ip()}:{self.port}"
            state["permanent_mdns_url"] = f"http://alpesh-Inspiron-3542.local:{self.port}"
            state["public_tunnel_url"] = self.last_tunnel_url or "Initializing..."
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.debug("Error writing heartbeat: %s", e)

    def run_supervision_loop(self):
        """Infinite 24/7 supervision loop."""
        logger.info("🛡️ Starting Chhaya 24/7 Autonomous Supervision Loop (Port: %d)...", self.port)
        self.start_mirror_server()
        self.start_public_tunnel()

        # If no public url yet, generate offline QR code initially
        if not self.last_tunnel_url:
            self.generate_qr_code(f"http://alpesh-Inspiron-3542.local:{self.port}")

        iteration = 0
        server_fail_count = 0
        while self.running:
            time.sleep(5)
            iteration += 1

            # 1. Server Health check with process liveness verification
            is_healthy = self.check_health()
            if not is_healthy:
                proc_dead = (self.server_proc is not None and self.server_proc.poll() is not None)
                server_fail_count += 1
                logger.warning("⚠️ Cloud Mirror Server health check failed (%d/12, proc_dead=%s)...", server_fail_count, proc_dead)
                if server_fail_count >= 12 or (proc_dead and server_fail_count >= 3):
                    logger.warning("⚠️ Cloud Mirror Server is truly crashed! Auto-restarting immediately...")
                    server_fail_count = 0
                    self.start_mirror_server()
            else:
                server_fail_count = 0
                self.update_heartbeat_in_state()

            # 2. Check and sync public tunnel URL continuously
            self.sync_tunnel_url()

            # 3. Active tunnel process check & Autonomous Auto-Healing
            if iteration % 6 == 0:
                tunnel_alive = (self.tunnel_proc and self.tunnel_proc.poll() is None)
                if not tunnel_alive:
                    logger.info("Tunnel process has terminated. Relaunching tunnel...")
                    self.tunnel_fail_count = 0
                    self.start_public_tunnel()
                elif self.last_tunnel_url:
                    is_tunnel_healthy = self.check_tunnel_health()
                    if is_tunnel_healthy:
                        self.tunnel_fail_count = 0
                    else:
                        # If edge revocation was logged, fast-track to 3 failures immediately
                        revoked = False
                        if TUNNEL_LOG_FILE.exists():
                            try:
                                with open(TUNNEL_LOG_FILE, "rb") as f:
                                    f.seek(max(0, TUNNEL_LOG_FILE.stat().st_size - 4096))
                                    if b"Unauthorized: Tunnel not found" in f.read():
                                        revoked = True
                            except Exception:
                                pass
                        if revoked:
                            self.tunnel_fail_count = 3
                        else:
                            self.tunnel_fail_count += 1

                        logger.warning("⚠️ Public tunnel health check failed (%d/3)...", self.tunnel_fail_count)
                        if self.tunnel_fail_count >= 3:
                            logger.error("❌ Public tunnel is DEAD (consecutive failures / edge revoked). Auto-restarting fresh tunnel...")
                            self.restart_public_tunnel(reason="probe_failed_or_revoked")

            # 4. Trim memory every 2 minutes
            if iteration % 24 == 0:
                trim_process_memory()

            # 5. Autonomous Laptop Sluggishness Watcher & Auto-Healer (Runs every 15s)
            if iteration % 3 == 0:
                try:
                    from system_optimizer import get_system_optimizer
                    heal_res = get_system_optimizer().auto_heal_if_sluggish(cooldown_seconds=180)
                    if heal_res:
                        logger.info(
                            "⚡ [Autonomous Healer] Laptop lag eliminated in %.2fs! Reasons: %s | Freed RAM: %.1f MB | Temp files pruned: %d",
                            heal_res.get("duration_seconds", 0.0),
                            ", ".join(heal_res.get("reasons", [])),
                            heal_res.get("freed_memory_mb", 0.0),
                            heal_res.get("temp_files_deleted_count", 0)
                        )
                except Exception as e:
                    logger.debug("Auto-heal check error: %s", e)

            # 6. Active Anti-Hacker Autonomous Watcher & Threat Neutralization (Runs every 30s)
            if iteration % 6 == 0:
                try:
                    from aradhya_security_sentry import get_security_sentry
                    sec_res = get_security_sentry().active_threat_neutralization_cycle()
                    if sec_res.get("neutralized_count", 0) > 0:
                        logger.warning(
                            "🛡️ [Anti-Hacker Shield] NEUTRALIZED %d threat(s)! Status: %s",
                            sec_res["neutralized_count"], sec_res["status"]
                        )
                except Exception as e:
                    logger.debug("Anti-hacker sentry check error: %s", e)

            # 7. Autonomous AI Model Auto-Discovery & Self-Updating (Runs on startup & every 1 hour)
            if iteration == 1 or iteration % 720 == 0:
                try:
                    from aradhya_model_updater import get_model_updater
                    upd_res = get_model_updater().discover_and_update_models(notify_desktop=False)
                    if upd_res.get("new_models_count", 0) > 0:
                        logger.info(
                            "🧬 [Autonomous Model Discovery] Ingested %d new AI models into catalog! Total: %d",
                            upd_res["new_models_count"], upd_res["total_registered_models"]
                        )
                except Exception as e:
                    logger.debug("Model updater auto-discovery error: %s", e)

            # 8. Omni-Agent Autonomous Git Cloud Auto-Sync to GitHub (Runs every 60s)
            if iteration % 12 == 0:
                try:
                    from omni_git_sync import get_omni_sync_engine
                    sync_summary = get_omni_sync_engine().sync_all(reason="Autonomous Watchdog Auto-Sync")
                    if sync_summary.get("synced_count", 0) > 0:
                        logger.info(
                            "☁️ [Omni-Agent Cloud Auto-Sync] Pushed updates for %d agent repository(ies) to GitHub!",
                            sync_summary["synced_count"]
                        )
                except Exception as ge:
                    logger.debug("Omni-agent git auto-sync error: %s", ge)




def get_watchdog_status() -> Dict[str, Any]:
    """Retrieve current 24/7 watchdog and server status."""
    port = 8081
    healthy = False
    try:
        url = f"http://127.0.0.1:{port}/api/health"
        req = urllib.request.Request(url, headers={"User-Agent": "ChhayaWatchdog/1.0"})
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            data = json.loads(resp.read().decode())
            healthy = (data.get("status") == "HEALTHY_HOT_STANDBY")
    except Exception:
        healthy = False

    lan_ip = get_local_lan_ip()
    pub_url = None
    if TUNNEL_URL_FILE.exists():
        try:
            pub_url = TUNNEL_URL_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            pass

    return {
        "status": "ONLINE_24_7" if healthy else "OFFLINE",
        "port": port,
        "is_healthy": healthy,
        "local_ip": lan_ip,
        "public_mobile_url": pub_url or "Initializing...",
        "local_wifi_url": f"http://{lan_ip}:{port}",
        "last_check": time.strftime("%Y-%m-%d %H:%M:%S")
    }


if __name__ == "__main__":
    wd = Chhaya247Watchdog()
    try:
        wd.run_supervision_loop()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Watchdog shutting down cleanly.")
