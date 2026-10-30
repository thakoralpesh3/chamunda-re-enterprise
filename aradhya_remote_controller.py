# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
Aradhya Autonomous Remote PC Controller (આરાધ્યા રિમોટ પીસી કંટ્રોલર)
Author: Aradhya (CEO), reporting exclusively to Alpesh Sir (Founder, Chairman & Master Tech)

Features (Equivalent to Antigravity Remote Access & Mobile Companion):
1. Live System Telemetry: CPU, RAM, Disk, Battery, Temperature, Uptime.
2. Remote Shell Terminal: Executes bash commands securely and streams output to mobile.
3. Live Screen Capture: Captures desktop screenshot in real-time for mobile viewing.
4. PC Hardware Control:
   - Screen Lock (cinnamon-screensaver / xdg-screensaver)
   - Volume slider & Mute toggle (pactl / amixer)
   - Brightness adjustment (brightnessctl / xbacklight)
5. Remote File Explorer: Browse workspace files, inspect code & logs from phone.
6. Process Manager: Monitor top processes and terminate hung tasks.
"""

import os
import sys
import time
import shutil
import socket
import datetime
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

import psutil

BASE_DIR = Path(__file__).parent if "__file__" in globals() else Path("/home/alpesh/chamunda_re_enterprise")
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
SCREENSHOTS_DIR = STATIC_DIR / "screenshots"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [AradhyaRemotePC] %(message)s"
)
logger = logging.getLogger("AradhyaRemotePC")


class AradhyaRemoteController:
    """
    Core remote PC access controller allowing Alpesh Sir to monitor,
    control, and execute commands on his workshop laptop from mobile.
    """

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        STATIC_DIR.mkdir(parents=True, exist_ok=True)
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    def get_pc_telemetry(self) -> Dict[str, Any]:
        """Comprehensive PC hardware and state telemetry."""
        # Battery
        bat = psutil.sensors_battery()
        bat_info = {
            "percent": bat.percent if bat else 100,
            "power_plugged": bat.power_plugged if bat else True,
            "status_text": "Plugged in ⚡" if (bat and bat.power_plugged) else "On Battery 🔋"
        }

        # CPU & Memory
        cpu_pct = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        disk = psutil.disk_usage('/')

        # Load averages
        load1, load5, load15 = (0.0, 0.0, 0.0)
        if hasattr(os, "getloadavg"):
            try:
                load1, load5, load15 = os.getloadavg()
            except Exception:
                pass

        # Uptime
        boot_time = psutil.boot_time()
        uptime_seconds = int(time.time() - boot_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{hours}h {minutes}m"

        # Host and IP
        hostname = socket.gethostname()

        # Volume
        volume_pct = self._get_current_volume()

        return {
            "success": True,
            "hostname": hostname,
            "os": "Linux Mint 22 (Wilma)",
            "uptime": uptime_str,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "battery": bat_info,
            "cpu": {
                "percent": cpu_pct,
                "cores_logical": psutil.cpu_count(logical=True),
                "cores_physical": psutil.cpu_count(logical=False),
                "load_1m": round(load1, 2),
                "load_5m": round(load5, 2)
            },
            "memory": {
                "total_mb": round(mem.total / (1024 * 1024), 1),
                "used_mb": round(mem.used / (1024 * 1024), 1),
                "available_mb": round(mem.available / (1024 * 1024), 1),
                "percent_used": mem.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024 ** 3), 1),
                "used_gb": round(disk.used / (1024 ** 3), 1),
                "free_gb": round(disk.free / (1024 ** 3), 1),
                "percent_used": disk.percent
            },
            "volume_percent": volume_pct
        }

    def execute_terminal_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes a shell command on the PC and returns full stdout, stderr, and exit code.
        Blocks destructive root deletions.
        """
        cmd_clean = command.strip()
        if not cmd_clean:
            return {"success": False, "error": "Empty command provided."}

        # Dangerous command defense
        dangerous = ["rm -rf /", "rm -rf /*", "mkfs", ":(){ :|:& };:"]
        if any(d in cmd_clean for d in dangerous):
            logger.warning("Blocked dangerous remote command attempt: %s", cmd_clean)
            return {
                "success": False,
                "command": cmd_clean,
                "error": "⛔ Security Block: Destructive command rejected by Aradhya Remote Shield.",
                "exit_code": 1
            }

        target_cwd = cwd if (cwd and Path(cwd).exists()) else str(Path.home())
        env = os.environ.copy()
        env["PATH"] = f"/home/alpesh/.local/bin:/home/alpesh/bin:{env.get('PATH', '/usr/bin:/bin')}"
        if "DISPLAY" not in env:
            env["DISPLAY"] = ":0"

        start_time = time.time()
        try:
            res = subprocess.run(
                cmd_clean,
                shell=True,
                cwd=target_cwd,
                env=env,
                capture_output=True,
                text=True,
                timeout=25
            )
            duration_ms = round((time.time() - start_time) * 1000, 1)
            stdout = res.stdout
            stderr = res.stderr
            return {
                "success": res.returncode == 0,
                "command": cmd_clean,
                "stdout": stdout,
                "stderr": stderr,
                "output": (stdout or stderr or "[Command completed with exit code 0]").strip(),
                "exit_code": res.returncode,
                "duration_ms": duration_ms,
                "cwd": target_cwd,
                "timestamp": time.strftime("%H:%M:%S")
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "command": cmd_clean,
                "error": "⏱️ Command timed out after 25 seconds.",
                "exit_code": 124,
                "duration_ms": 25000
            }
        except Exception as e:
            return {
                "success": False,
                "command": cmd_clean,
                "error": str(e),
                "exit_code": 1
            }

    def capture_screen(self) -> Dict[str, Any]:
        """Capture live PC screen and return relative URL and path."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_live.png"
        target_path = STATIC_DIR / filename
        archive_path = SCREENSHOTS_DIR / f"screenshot_{timestamp}.png"

        captured = False

        # Attempt 1: mss
        try:
            import mss
            import mss.tools
            with mss.MSS() as sct:
                monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                img = sct.grab(monitor)
                mss.tools.to_png(img.rgb, img.size, output=str(target_path))
                # Also archive
                try:
                    shutil.copyfile(str(target_path), str(archive_path))
                except Exception:
                    pass
                captured = True
        except Exception as me:
            logger.debug("mss capture failed, trying scrot: %s", me)

        # Attempt 2: scrot fallback
        if not captured and shutil.which("scrot"):
            env = os.environ.copy()
            if "DISPLAY" not in env:
                env["DISPLAY"] = ":0"
            r = subprocess.run(["scrot", str(target_path)], capture_output=True, env=env)
            if r.returncode == 0 and target_path.exists():
                captured = True

        if captured and target_path.exists():
            size_kb = round(target_path.stat().st_size / 1024, 1)
            rel_url = f"/static/{filename}?t={int(time.time())}"
            return {
                "success": True,
                "filename": filename,
                "url": rel_url,
                "filepath": str(target_path),
                "size_kb": size_kb,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        return {"success": False, "error": "Could not capture display screenshot."}

    def lock_pc_screen(self) -> Dict[str, Any]:
        """Lock PC screen for privacy and security."""
        env = os.environ.copy()
        if "DISPLAY" not in env:
            env["DISPLAY"] = ":0"

        for cmd in [
            ["cinnamon-screensaver-command", "-l"],
            ["xdg-screensaver", "lock"],
            ["loginctl", "lock-session"]
        ]:
            try:
                res = subprocess.run(cmd, capture_output=True, env=env, timeout=3)
                if res.returncode == 0:
                    return {"success": True, "message": "🔒 PC screen successfully locked."}
            except Exception:
                pass
        return {"success": True, "message": "Screen lock request dispatched."}

    def set_volume(self, percent: int) -> Dict[str, Any]:
        """Set master audio volume (0-100%)."""
        vol = max(0, min(100, int(percent)))
        env = os.environ.copy()
        if "DISPLAY" not in env:
            env["DISPLAY"] = ":0"

        if shutil.which("pactl"):
            res = subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ {vol}%", shell=True, env=env, capture_output=True)
            if res.returncode == 0:
                return {"success": True, "volume": vol, "message": f"Volume set to {vol}%."}
        if shutil.which("amixer"):
            subprocess.run(f"amixer -D pulse sset Master {vol}%", shell=True, env=env, capture_output=True)
            return {"success": True, "volume": vol, "message": f"Volume set to {vol}%."}
        return {"success": False, "error": "Audio controller not available."}

    def toggle_mute(self) -> Dict[str, Any]:
        """Toggle audio mute on PC."""
        env = os.environ.copy()
        if "DISPLAY" not in env:
            env["DISPLAY"] = ":0"
        if shutil.which("pactl"):
            subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ toggle", shell=True, env=env, capture_output=True)
            return {"success": True, "message": "PC audio mute toggled."}
        if shutil.which("amixer"):
            subprocess.run("amixer -D pulse sset Master toggle", shell=True, env=env, capture_output=True)
            return {"success": True, "message": "PC audio mute toggled."}
        return {"success": False, "error": "Audio controller not available."}

    def _get_current_volume(self) -> int:
        """Helper to get current volume percentage."""
        try:
            if shutil.which("pactl"):
                out = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@", shell=True, text=True)
                for part in out.split():
                    if part.endswith("%"):
                        return int(part.replace("%", ""))
        except Exception:
            pass
        return 75

    def list_directory(self, path_str: str = "/home/alpesh") -> Dict[str, Any]:
        """Safely list files and directories for mobile file explorer."""
        p = Path(path_str).resolve()
        if not p.exists() or not p.is_dir():
            p = Path("/home/alpesh")

        entries = []
        try:
            for item in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                try:
                    st = item.stat()
                    size_str = f"{st.st_size} B"
                    if st.st_size > 1024 * 1024:
                        size_str = f"{st.st_size / (1024 * 1024):.1f} MB"
                    elif st.st_size > 1024:
                        size_str = f"{st.st_size / 1024:.1f} KB"

                    entries.append({
                        "name": item.name,
                        "path": str(item),
                        "is_dir": item.is_dir(),
                        "size": size_str if not item.is_dir() else "-",
                        "modified": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                    })
                except Exception:
                    pass
        except Exception as e:
            return {"success": False, "error": str(e), "current_path": str(p)}

        parent_path = str(p.parent) if p != Path("/") else str(p)
        return {
            "success": True,
            "current_path": str(p),
            "parent_path": parent_path,
            "entries_count": len(entries),
            "entries": entries[:100]
        }

    def read_file_preview(self, filepath: str, max_lines: int = 150) -> Dict[str, Any]:
        """Read text file preview safely."""
        p = Path(filepath).resolve()
        if not p.exists() or p.is_dir():
            return {"success": False, "error": "File does not exist or is a directory."}

        # Size check
        if p.stat().st_size > 2 * 1024 * 1024:
            return {"success": False, "error": "File exceeds 2MB preview limit."}

        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                lines = [f.readline() for _ in range(max_lines)]
                content = "".join(lines)
            return {
                "success": True,
                "filepath": str(p),
                "filename": p.name,
                "content": content,
                "lines_shown": len(lines),
                "size_kb": round(p.stat().st_size / 1024, 1)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_top_processes(self, limit: int = 12) -> List[Dict[str, Any]]:
        """List top running processes sorted by memory/CPU."""
        procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
            try:
                info = p.info
                if info.get('cpu_percent') is not None and info.get('memory_percent') is not None:
                    procs.append({
                        "pid": info['pid'],
                        "name": info['name'],
                        "user": info.get('username', 'alpesh'),
                        "cpu": round(info['cpu_percent'], 1),
                        "mem": round(info['memory_percent'], 1)
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        procs.sort(key=lambda x: (x['mem'], x['cpu']), reverse=True)
        return procs[:limit]


_controller_instance: Optional[AradhyaRemoteController] = None

def get_remote_controller() -> AradhyaRemoteController:
    global _controller_instance
    if _controller_instance is None:
        _controller_instance = AradhyaRemoteController()
    return _controller_instance


if __name__ == "__main__":
    c = get_remote_controller()
    print("Testing Aradhya Remote PC Controller...")
    t = c.get_pc_telemetry()
    print(f"Host: {t['hostname']} | OS: {t['os']} | CPU: {t['cpu']['percent']}% | RAM: {t['memory']['percent_used']}% | Battery: {t['battery']['percent']}%")
    cmd_res = c.execute_terminal_command("uname -a")
    print("Command Output:", cmd_res.get("output"))
    scr_res = c.capture_screen()
    print("Screenshot:", scr_res.get("url"))
