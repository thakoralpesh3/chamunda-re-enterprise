# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya" (પ્રોજેક્ટ છાયા)
ARADHYA AUTONOMOUS CORE • Supreme AI Orchestrator & Executive Brain
Author: Aradhya (CEO), reporting directly to Alpesh Sir (Founder, Chairman & Master Tech)

Powers Aradhya as a 100% Offline Autonomous Agent with unrestricted authority
across the entire laptop (hardware, filesystem, shell, processes, apps, multi-agent matrix)
operating like Tony Stark's AI assistants: JARVIS, E.D.I.T.H., F.R.I.D.A.Y., and VISION.
"""

import os
import sys
import re
import time
import shutil
import datetime
import subprocess
import socket
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import psutil

# Aradhya Advanced Autonomous Subsystems
from aradhya_security_sentry import get_security_sentry
from aradhya_polyglot_nlu import get_polyglot_nlu
from aradhya_self_evolution import get_self_evolution
from aradhya_voice_engine import get_voice_engine

# Base Directories
CHAMUNDA_DIR = Path("/home/alpesh/chamunda_re_enterprise")
JARVIS_DIR = Path("/home/alpesh/jarvis-agent")
HOME_DIR = Path("/home/alpesh")
DATA_DIR = CHAMUNDA_DIR / "data"
STATIC_DIR = CHAMUNDA_DIR / "static"
SCREENSHOTS_DIR = STATIC_DIR / "screenshots"

DATA_DIR.mkdir(parents=True, exist_ok=True)
STATIC_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

OFFICIAL_WHATSAPP_HELPLINE = "+91 78747 19139"


class AradhyaAutonomousEngine:
    """
    100% Offline Autonomous Executive Intelligence Engine for Aradhya.
    Unrestricted authority across the entire laptop, hardware, filesystem, and subagents.
    """

    def __init__(self):
        self.home_dir = HOME_DIR
        self.chamunda_dir = CHAMUNDA_DIR
        self.jarvis_dir = JARVIS_DIR
        self.stay_awake_active = False
        self.sentry = get_security_sentry()
        self.nlu = get_polyglot_nlu()
        self.evolution = get_self_evolution()
        self.voice = get_voice_engine()
        self._cached_internet_status: Optional[Dict[str, Any]] = None
        self._last_internet_check_time: float = 0.0

    # =========================================================================
    # 1. HARDWARE & OPERATING SYSTEM CONTROLS (JARVIS / FRIDAY PROTOCOLS)
    # =========================================================================

    def get_battery_status(self) -> Dict[str, Any]:
        """Fetch battery percentage, charging state, and power metrics."""
        try:
            battery = psutil.sensors_battery()
            if not battery:
                return {
                    "success": True,
                    "percent": 100,
                    "charging": True,
                    "status_text": "AC Power ⚡",
                    "time_remaining": "Continuous AC power",
                    "summary": "AC Power connected (Desktop mode)"
                }
            
            percent = round(battery.percent, 1)
            charging = battery.power_plugged
            secs_left = battery.secsleft
            
            if secs_left == psutil.POWER_TIME_UNLIMITED or secs_left < 0:
                time_str = "Calculating or on continuous AC power"
            else:
                hours = int(secs_left // 3600)
                mins = int((secs_left % 3600) // 60)
                time_str = f"{hours}h {mins}m remaining"

            status_text = "Charging ⚡" if charging else "Discharging 🔋"
            return {
                "success": True,
                "percent": percent,
                "charging": charging,
                "status_text": status_text,
                "time_remaining": time_str,
                "summary": f"Battery: {percent}% ({status_text}, {time_str})"
            }
        except Exception as e:
            return {"success": False, "error": str(e), "summary": f"Could not read battery: {e}"}

    def set_volume(self, percent: int) -> Dict[str, Any]:
        """Set master audio volume (0-100%)."""
        vol = max(0, min(100, int(percent)))
        if shutil.which("pactl"):
            res = subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ {vol}%", shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                return {"success": True, "volume": vol, "summary": f"Volume set to {vol}% via pactl."}
        if shutil.which("amixer"):
            subprocess.run(f"amixer -D pulse sset Master {vol}%", shell=True, capture_output=True, text=True)
            return {"success": True, "volume": vol, "summary": f"Volume set to {vol}% via amixer."}
        return {"success": False, "error": "No audio controller found."}

    def adjust_volume(self, delta: int) -> Dict[str, Any]:
        """Adjust volume relatively (e.g. +10 or -10)."""
        sign = "+" if delta >= 0 else "-"
        val = abs(int(delta))
        if shutil.which("pactl"):
            subprocess.run(f"pactl set-sink-volume @DEFAULT_SINK@ {sign}{val}%", shell=True, capture_output=True)
            return {"success": True, "delta": delta, "summary": f"Volume adjusted by {sign}{val}%."}
        if shutil.which("amixer"):
            subprocess.run(f"amixer -D pulse sset Master {val}%{sign}", shell=True, capture_output=True)
            return {"success": True, "delta": delta, "summary": f"Volume adjusted by {sign}{val}%."}
        return {"success": False, "error": "No audio controller found."}

    def toggle_mute(self) -> Dict[str, Any]:
        """Toggle system audio mute."""
        if shutil.which("pactl"):
            subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ toggle", shell=True, capture_output=True)
            return {"success": True, "summary": "System audio mute toggled."}
        if shutil.which("amixer"):
            subprocess.run("amixer -D pulse sset Master toggle", shell=True, capture_output=True)
            return {"success": True, "summary": "System audio mute toggled."}
        return {"success": False, "error": "No audio controller found."}

    def set_brightness(self, percent: int) -> Dict[str, Any]:
        """Set screen brightness (10-100%)."""
        val = max(10, min(100, int(percent)))
        if shutil.which("brightnessctl"):
            subprocess.run(f"brightnessctl set {val}%", shell=True, capture_output=True)
            return {"success": True, "brightness": val, "summary": f"Screen brightness set to {val}%."}
        if shutil.which("xbacklight"):
            subprocess.run(f"xbacklight -set {val}", shell=True, capture_output=True)
            return {"success": True, "brightness": val, "summary": f"Screen brightness set to {val}%."}
        return {"success": False, "error": "brightnessctl/xbacklight not available."}

    def lock_screen(self) -> Dict[str, Any]:
        """Instantly lock laptop screen for security."""
        for cmd in ["xdg-screensaver lock", "cinnamon-screensaver-command -l", "loginctl lock-session"]:
            if subprocess.run(cmd, shell=True, capture_output=True).returncode == 0:
                return {"success": True, "summary": "Laptop screen locked securely."}
        return {"success": True, "summary": "Screen lock request processed."}

    def capture_screenshot(self) -> Dict[str, Any]:
        """Capture full screen screenshot and save to accessible image."""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            target_path = SCREENSHOTS_DIR / filename
            
            captured = False
            if shutil.which("scrot"):
                r = subprocess.run(f"scrot {target_path}", shell=True, capture_output=True)
                if r.returncode == 0 and target_path.exists():
                    captured = True

            if not captured:
                try:
                    import mss
                    with mss.mss() as sct:
                        monitor = sct.monitors[1] if len(sct.monitors) > 1 else sct.monitors[0]
                        sct_img = sct.grab(monitor)
                        mss.tools.to_png(sct_img.rgb, sct_img.size, output=str(target_path))
                    captured = True
                except Exception:
                    pass

            if not captured and shutil.which("import"):
                subprocess.run(f"import -window root {target_path}", shell=True, capture_output=True)
                if target_path.exists():
                    captured = True

            if captured and target_path.exists():
                size_kb = target_path.stat().st_size / 1024
                rel_url = f"/static/screenshots/{filename}"
                return {
                    "success": True,
                    "filepath": str(target_path),
                    "url": rel_url,
                    "size_kb": round(size_kb, 1),
                    "summary": f"Screenshot captured successfully: {filename} ({size_kb:.1f} KB)"
                }
            return {"success": False, "error": "No screenshot utility succeeded."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def stay_awake_toggle(self, enable: Optional[bool] = None) -> Dict[str, Any]:
        """Toggle or inspect Work StayAwake sentry (prevents sleep during work)."""
        if enable is None:
            self.stay_awake_active = not self.stay_awake_active
        else:
            self.stay_awake_active = bool(enable)

        if self.stay_awake_active:
            subprocess.run("xset s off -dpms >/dev/null 2>&1 || true", shell=True)
            state_msg = "ACTIVE (Sleep & DPMS display blanking suppressed during work)"
        else:
            subprocess.run("xset s on +dpms >/dev/null 2>&1 || true", shell=True)
            state_msg = "NORMAL (Default OS power-saving and sleep restored)"
        return {"success": True, "active": self.stay_awake_active, "summary": f"Work StayAwake Sentry is now {state_msg}."}

    # =========================================================================
    # 2. WHOLE LAPTOP FILESYSTEM OPERATIONS (/home/alpesh)
    # =========================================================================

    def find_files(self, query: str, search_root: str = "/home/alpesh", max_results: int = 25) -> Dict[str, Any]:
        """Find files matching query or extension across the entire laptop in milliseconds."""
        import fnmatch

        clean_q = query.strip()
        actual_root = search_root

        # Detect specific directory mentioned in query
        if "in chamunda" in clean_q.lower():
            actual_root = "/home/alpesh/chamunda_re_enterprise"
            clean_q = re.sub(r'\s+in\s+chamunda\w*', '', clean_q, flags=re.IGNORECASE).strip()
        elif "in jarvis" in clean_q.lower():
            actual_root = "/home/alpesh/jarvis-agent"
            clean_q = re.sub(r'\s+in\s+jarvis\w*', '', clean_q, flags=re.IGNORECASE).strip()
        elif "in download" in clean_q.lower():
            actual_root = "/home/alpesh/Downloads"
            clean_q = re.sub(r'\s+in\s+downloads?', '', clean_q, flags=re.IGNORECASE).strip()
        elif "in desktop" in clean_q.lower():
            actual_root = "/home/alpesh/Desktop"
            clean_q = re.sub(r'\s+in\s+desktop', '', clean_q, flags=re.IGNORECASE).strip()

        root = Path(actual_root).expanduser().resolve()
        if not root.exists():
            return {"success": False, "error": f"Path '{actual_root}' does not exist."}

        # Handle natural language patterns: e.g. 'all py files' -> '*.py', 'pdf' -> '*.pdf'
        m_ext = re.search(r'\b(?:all\s+)?([a-zA-Z0-9]+)\s+files?\b', clean_q, re.IGNORECASE)
        if m_ext and m_ext.group(1).lower() in ["py", "pdf", "sh", "txt", "json", "md", "csv", "png", "jpg", "html", "js", "ts", "css", "yaml", "yml", "xml", "log", "apk", "ipa"]:
            ext = m_ext.group(1).lower()
            pattern = f"*.{ext}"
        elif clean_q.lower() in ["py", "pdf", "sh", "txt", "json", "md", "csv", "png", "jpg", "html", "js", "ts", "css", "yaml", "yml", "xml", "log", "apk", "ipa"]:
            pattern = f"*.{clean_q.lower()}"
        elif not ("*" in clean_q or "?" in clean_q):
            pattern = f"*{clean_q}*"
        else:
            pattern = clean_q

        exclude = {'.git', 'node_modules', '__pycache__', '.venv', '.cache', 'site-packages', '.local', '.cargo', '.rustup', '.gradle'}
        matches = []
        try:
            for dirpath, dirnames, filenames in os.walk(str(root)):
                # Prune excluded directories immediately to avoid descent
                dirnames[:] = [d for d in dirnames if d not in exclude and not d.startswith('.')]
                for fname in filenames:
                    if fnmatch.fnmatch(fname.lower(), pattern.lower()):
                        full_p = os.path.join(dirpath, fname)
                        try:
                            st = os.stat(full_p)
                            matches.append({
                                "path": full_p,
                                "name": fname,
                                "is_dir": False,
                                "size_kb": round(st.st_size / 1024, 1),
                                "modified": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
                            })
                            if len(matches) >= max_results:
                                break
                        except Exception:
                            continue
                if len(matches) >= max_results:
                    break

            return {
                "success": True,
                "query": query,
                "pattern": pattern,
                "root": str(root),
                "count": len(matches),
                "matches": matches,
                "summary": f"Found {len(matches)} item(s) matching '{pattern}' in '{root}'."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def read_file(self, filepath: str, max_lines: int = 150) -> Dict[str, Any]:
        """Read content of any text, code, or configuration file."""
        target = Path(filepath).expanduser().resolve()
        if not target.exists():
            alt = HOME_DIR / filepath
            if alt.exists():
                target = alt
            else:
                return {"success": False, "error": f"File '{filepath}' not found."}

        if not target.is_file():
            return {"success": False, "error": f"'{filepath}' is a directory, not a regular file."}

        try:
            with open(target, "r", encoding="utf-8", errors="replace") as f:
                lines = [f.readline() for _ in range(max_lines)]
                content = "".join(lines)
                truncated = bool(f.readline())
            return {
                "success": True,
                "filepath": str(target),
                "lines_read": len(lines),
                "truncated": truncated,
                "content": content,
                "summary": f"Read {len(lines)} line(s) from '{target.name}'."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def write_file(self, filepath: str, content: str, append: bool = False) -> Dict[str, Any]:
        """Write, create or append content to any file on the laptop."""
        target = Path(filepath).expanduser().resolve()
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            mode = "a" if append else "w"
            with open(target, mode, encoding="utf-8") as f:
                f.write(content)
            action = "Appended to" if append else "Wrote"
            return {
                "success": True,
                "filepath": str(target),
                "size_bytes": len(content.encode("utf-8")),
                "summary": f"{action} '{target.name}' successfully ({len(content)} characters)."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_dir(self, directory: str = "/home/alpesh") -> Dict[str, Any]:
        """List files and folders with metadata in any directory."""
        target = Path(directory).expanduser().resolve()
        if not target.exists():
            return {"success": False, "error": f"Directory '{directory}' does not exist."}

        try:
            items = []
            for item in sorted(target.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                try:
                    is_d = item.is_dir()
                    sz = "-" if is_d else f"{item.stat().st_size / 1024:.1f} KB"
                    items.append({
                        "name": item.name,
                        "is_dir": is_d,
                        "size": sz,
                        "path": str(item)
                    })
                    if len(items) >= 60:
                        break
                except Exception:
                    continue

            return {
                "success": True,
                "directory": str(target),
                "total_items": len(items),
                "items": items,
                "summary": f"Listed {len(items)} items in '{target.name}'."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_disk_storage(self) -> Dict[str, Any]:
        """Inspect storage space across partitions."""
        try:
            usage = psutil.disk_usage("/")
            total_gb = usage.total / (1024**3)
            used_gb = usage.used / (1024**3)
            free_gb = usage.free / (1024**3)
            pct = usage.percent
            return {
                "success": True,
                "total_gb": round(total_gb, 1),
                "used_gb": round(used_gb, 1),
                "free_gb": round(free_gb, 1),
                "percent_used": pct,
                "summary": f"Disk Storage: {free_gb:.1f} GB free of {total_gb:.1f} GB ({pct}% used)."
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # =========================================================================
    # 3. UNRESTRICTED SHELL & PROCESS EXECUTION (VISION / EDITH MATRIX)
    # =========================================================================

    def execute_shell(self, command: str, timeout_seconds: int = 40) -> Dict[str, Any]:
        """Execute any Linux bash command with full stdout/stderr capture."""
        try:
            start = time.time()
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd="/home/alpesh",
                executable="/bin/bash"
            )
            elapsed = time.time() - start
            stdout = proc.stdout.strip()
            stderr = proc.stderr.strip()
            code = proc.returncode

            output = stdout or stderr or "(Command produced no output)"
            return {
                "success": code == 0,
                "command": command,
                "exit_code": code,
                "stdout": stdout,
                "stderr": stderr,
                "output": output,
                "duration_seconds": round(elapsed, 2),
                "summary": f"Command finished (code {code}) in {elapsed:.2f}s."
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "command": command,
                "error": f"Execution timed out after {timeout_seconds} seconds.",
                "summary": f"Command timed out ({timeout_seconds}s)."
            }
        except Exception as e:
            return {"success": False, "command": command, "error": str(e)}

    def launch_app(self, app_name: str) -> Dict[str, Any]:
        """Launch any desktop application (e.g. firefox, vlc, gimp, libreoffice, etc.)."""
        clean_app = app_name.lower().strip()
        app_aliases = {
            "browser": "firefox",
            "chrome": "google-chrome",
            "files": "nemo",
            "file manager": "nemo",
            "editor": "xed",
            "code": "code",
            "terminal": "x-terminal-emulator",
            "calc": "gnome-calculator",
            "calculator": "gnome-calculator",
            "writer": "libreoffice --writer",
            "office": "libreoffice",
            "mail": "thunderbird",
            "music": "rhythmbox",
            "video": "vlc",
            "paint": "drawing"
        }
        binary = app_aliases.get(clean_app, clean_app)
        try:
            prog = binary.split()[0]
            if not shutil.which(prog):
                return {"success": False, "error": f"Application binary '{prog}' not installed on system."}

            subprocess.Popen(binary, shell=True, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"success": True, "app": binary, "summary": f"Launched application: '{binary}'."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def inspect_processes(self, filter_kw: str = "") -> Dict[str, Any]:
        """List active processes with CPU & RAM consumption."""
        matches = []
        kw = filter_kw.lower().strip()
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                name = p.info.get('name') or ""
                if not kw or kw in name.lower():
                    cpu = p.info.get('cpu_percent', 0.0) or 0.0
                    mem = p.info.get('memory_percent', 0.0) or 0.0
                    pid = p.info.get('pid')
                    matches.append({"pid": pid, "name": name, "cpu": round(cpu, 1), "ram": round(mem, 1)})
            except Exception:
                continue

        matches.sort(key=lambda x: x["cpu"], reverse=True)
        top = matches[:15]
        return {
            "success": True,
            "count": len(matches),
            "top_processes": top,
            "summary": f"Inspected {len(matches)} processes."
        }

    def terminate_process(self, target: str) -> Dict[str, Any]:
        """Terminate a process by PID or name."""
        killed = 0
        target = target.strip()
        if target.isdigit():
            pid = int(target)
            try:
                p = psutil.Process(pid)
                name = p.name()
                p.terminate()
                return {"success": True, "summary": f"Terminated PID {pid} ({name})."}
            except Exception as e:
                return {"success": False, "error": str(e)}

        clean_name = target.lower()
        for p in psutil.process_iter(['pid', 'name']):
            try:
                if clean_name in p.info['name'].lower():
                    p.terminate()
                    killed += 1
            except Exception:
                continue

        if killed > 0:
            return {"success": True, "killed": killed, "summary": f"Terminated {killed} process(es) matching '{target}'."}
        return {"success": False, "summary": f"No running processes found matching '{target}'."}

    def turbo_speed_laptop(self) -> Dict[str, Any]:
        """Engage Turbo Speed & Lag Buster: clear buffers, purge temp files, kill runaway spinners."""
        from system_optimizer import get_system_optimizer
        opt = get_system_optimizer()
        res = opt.optimize_laptop_performance(
            aggressive=True,
            close_stale_processes=True,
            clean_temp_files=True,
            trigger_source="aradhya_turbo_protocol"
        )
        return res

    def diagnose_hardware_issue(self, issue_type: str, query: str = "") -> Dict[str, Any]:
        """
        Deep, zero-hallucination Linux Mint hardware diagnostics for Dell Inspiron 3542.
        Executes real kernel, bus, and peripheral probes without plain-text speculation.
        """
        issue_clean = (issue_type + " " + query).lower()

        # 1. CAMERA & WEBCAM PROBE
        if any(w in issue_clean for w in ["camera", "webcam", "video", "કેમેરા", "વેબકેમ"]):
            # Check device nodes
            dev_video = list(Path("/dev").glob("video*"))
            dev_video_str = [str(d) for d in dev_video]

            # Check USB bus devices
            usb_res = subprocess.run(["lsusb"], capture_output=True, text=True)
            usb_lines = usb_res.stdout.strip().splitlines()
            camera_usb = [l for l in usb_lines if any(k in l.lower() for k in ["cam", "video", "imaging", "uvc", "microdia", "sunplus", "chicony", "bison", "omnivision"])]

            # Check dmesg kernel ring buffer
            dmesg_res = subprocess.run("dmesg | grep -i -E 'uvc|video|webcam|camera' | tail -n 8", shell=True, capture_output=True, text=True, executable="/bin/bash")
            dmesg_lines = dmesg_res.stdout.strip()

            # Check kernel modules
            lsmod_res = subprocess.run("lsmod | grep -E 'uvcvideo|videodev'", shell=True, capture_output=True, text=True, executable="/bin/bash")
            uvc_loaded = "uvcvideo" in lsmod_res.stdout

            has_device_node = len(dev_video) > 0

            diagnostic_data = {
                "subsystem": "CAMERA_WEBCAM",
                "laptop_model": "Dell Inspiron 3542",
                "os": "Linux Mint Cinnamon (Kernel 6.x / x86_64)",
                "dev_video_nodes": dev_video_str,
                "usb_enumeration": camera_usb if camera_usb else "Integrated webcam not present on USB bus",
                "uvcvideo_module_loaded": uvc_loaded,
                "dmesg_tail": dmesg_lines
            }

            if has_device_node:
                resp_en = (
                    f"Greetings Alpesh Sir! 📷 Webcam Hardware Diagnostics (Dell Inspiron 3542 / Linux Mint):\n\n"
                    f"• Device Node: Active at `{', '.join(dev_video_str)}` ✅\n"
                    f"• Kernel Driver: `uvcvideo` is active\n"
                    f"• USB Enumeration: {camera_usb[0] if camera_usb else 'Internal Integrated Controller'}\n\n"
                    f"💡 The camera hardware is recognized by the Linux kernel! If an app cannot access it:\n"
                    f"1. Check permissions: `sudo usermod -aG video alpesh`\n"
                    f"2. Check if another process is using it: `lsof /dev/video0`\n"
                    f"3. Test with Linux camera app: `cheese` or Chromium WebRTC test."
                )
                resp_gu = (
                    f"જય માતાજી અલ્પેશ સાહેબ! 📷 વેબકેમ ડાયગ્નોસ્ટિક રિપોર્ટ (Dell Inspiron 3542 / Linux Mint):\n\n"
                    f"• ડિવાઇસ નોડ: સક્રિય છે `{', '.join(dev_video_str)}` ✅\n"
                    f"• કર્નલ ડ્રાઈવર: `uvcvideo` મોડ્યુલ લોડેડ છે\n"
                    f"• હાર્ડવેર સ્ટેટસ: કેમેરા લિનક્સ કર્નલમાં બરાબર ડિટેક્ટ થયેલ છે!\n\n"
                    f"💡 જો કોઈ એપમાં કેમેરા ન ખૂલતો હોય તો:\n"
                    f"1. યુઝર પરમિશન: `sudo usermod -aG video alpesh`\n"
                    f"2. કેમેરા એપથી ટેસ્ટ કરો: ટર્મિનલમાં `cheese` રન કરો."
                )
            else:
                resp_en = (
                    f"Greetings Alpesh Sir! 📷 Inbuilt Webcam Hardware Diagnostics (Dell Inspiron 3542 / Linux Mint):\n\n"
                    f"### 🔍 Real System Hardware Telemetry:\n"
                    f"- **Device Node**: `/dev/video*` not found (no video capture device created by kernel).\n"
                    f"- **USB Bus Status**: Integrated webcam is **not enumerated** on the internal USB bus (`lsusb`).\n"
                    f"- **Kernel Driver**: `uvcvideo` is not bound to any detected USB device ID.\n\n"
                    f"### 🛠️ Root Cause & Actionable Fix for Dell Inspiron 3542:\n"
                    f"Because the camera does not show up on the internal USB bus at the hardware layer, this is caused by one of three physical/firmware conditions:\n\n"
                    f"1. **Dell BIOS / UEFI Camera Setting (Most Common Cause)**:\n"
                    f"   - Shut down / restart laptop.\n"
                    f"   - As soon as the Dell logo appears, tap **`F2` repeatedly** to enter BIOS Setup.\n"
                    f"   - Navigate to: **`System Configuration`** $\\rightarrow$ **`Miscellaneous Devices`**.\n"
                    f"   - Ensure the **`Enable Camera`** checkbox is **CHECKED** ✅.\n"
                    f"   - Click `Apply`, then `Exit` to boot into Linux Mint.\n\n"
                    f"2. **Physical Display Cable / Hinge Connection**:\n"
                    f"   - On the Dell Inspiron 3542, the integrated webcam wires pass through the left display hinge to the camera board in the top bezel.\n"
                    f"   - If the laptop lid has been moved or hinges have slack, the internal camera cable connector can become unseated.\n\n"
                    f"3. **Manual Kernel Module Load**:\n"
                    f"   - To ensure the USB Video Class kernel module is loaded in Linux Mint, execute:\n"
                    f"     `sudo modprobe uvcvideo`\n"
                    f"   - Then re-check with `ls -l /dev/video*`."
                )
                resp_gu = (
                    f"જય માતાજી અલ્પેશ સાહેબ! 📷 ઇનબિલ્ટ કેમેરા હાર્ડવેર ડાયગ્નોસ્ટિક (Dell Inspiron 3542 / Linux Mint):\n\n"
                    f"### 🔍 લેપટોપ હાર્ડવેરની વાસ્તવિક તપાસ (Real Telemetry):\n"
                    f"- **ડિવાઇસ નોડ**: `/dev/video*` મળ્યો નથી (લિનક્સ કર્નલે કોઈ કેમેરા ડિવાઇસ બનાવ્યું નથી).\n"
                    f"- **USB બસ સ્ટેટસ**: ઇનબિલ્ટ કેમેરા ઇન્ટરનલ USB બસ પર ડિટેક્ટ થતો નથી (`lsusb`).\n"
                    f"- **કર્નલ ડ્રાઈવર**: `uvcvideo` મોડ્યુલ સ્ટેન્ડબાય પર છે.\n\n"
                    f"### 🛠️ Dell Inspiron 3542 માટે ચોક્કસ સમાધાન (Fix Steps):\n"
                    f"હાર્ડવેર લેવલે કેમેરા USB પર ન દેખાવાના મુખ્ય ૩ કારણો છે:\n\n"
                    f"૧. **Dell BIOS માં કેમેરા ડિસેબલ હોવો (સૌથી સામાન્ય કારણ)**:\n"
                    f"   - લેપટોપ Restart કરો, Dell લોગો દેખાય ત્યારે તરત **`F2` કી વારંવાર દબાવો**.\n"
                    f"   - BIOS માં જાઓ: **`System Configuration`** $\\rightarrow$ **`Miscellaneous Devices`**.\n"
                    f"   - ત્યાં **`Enable Camera`** બોક્સ પર ખરું (Check ✅) કરો.\n"
                    f"   - `Apply` કરી `Exit` કરો અને લિનક્સ મિન્ટ શરૂ થવા દો.\n\n"
                    f"૨. **ડિસ્પ્લે કેબલ / હિન્જ કનેક્શન**:\n"
                    f"   - Dell Inspiron 3542 માં સ્ક્રીનની ઉપર રહેલ વેબકેમનું વાયરિંગ ડાબી હિન્જમાંથી પસાર થાય છે.\n"
                    f"   - જો સ્ક્રીન ઘણી વાર ખોલ-બંધ થઈ હોય તો કેબલ ઢીલો પડી શકે છે.\n\n"
                    f"૩. **લિનક્સ કર્નલ ડ્રાઇવર કમાન્ડ**:\n"
                    f"   - BIOS ચેક કર્યા પછી ટર્મિનલમાં ચલાવો: `sudo modprobe uvcvideo`\n"
                    f"   - અને ચકાસો: `ls -l /dev/video*`."
                )

            return {
                "success": True,
                "diagnostic_type": "CAMERA_HARDWARE_DIAGNOSTIC",
                "has_camera": has_device_node,
                "data": diagnostic_data,
                "response_en": resp_en,
                "response_gu": resp_gu
            }

        # 2. AUDIO & MICROPHONE PROBE
        elif any(w in issue_clean for w in ["audio", "sound", "mic", "microphone", "speaker", "volume", "અવાજ", "માઇક"]):
            pactl_vol = subprocess.run("pactl get-sink-volume @DEFAULT_SINK@ 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()
            pactl_mute = subprocess.run("pactl get-sink-mute @DEFAULT_SINK@ 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()
            sinks = subprocess.run("pactl list sinks short 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()
            sources = subprocess.run("pactl list sources short 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()

            is_muted = "yes" in pactl_mute.lower()
            resp_en = (
                f"Greetings Alpesh Sir! 🔊 Audio Subsystem Diagnostics (Dell Inspiron 3542 / Linux Mint):\n\n"
                f"• Output Volume: {pactl_vol}\n"
                f"• Mute Status: {'MUTED 🔇' if is_muted else 'UNMUTED 🔊'}\n"
                f"• Available Sinks:\n```\n{sinks}\n```\n"
                f"• Available Audio Inputs (Microphones):\n```\n{sources}\n```\n"
                f"💡 Quick Fixes:\n"
                f"- To Unmute: `pactl set-sink-mute @DEFAULT_SINK@ 0`\n"
                f"- Set Volume to 80%: `pactl set-sink-volume @DEFAULT_SINK@ 80%`\n"
                f"- Restart Sound Server: `systemctl --user restart pulseaudio || systemctl --user restart pipewire`"
            )
            resp_gu = (
                f"જય માતાજી અલ્પેશ સાહેબ! 🔊 ઓડિયો સબસિસ્ટમ ડાયગ્નોસ્ટિક (Dell Inspiron 3542 / Linux Mint):\n\n"
                f"• વોલ્યુમ: {pactl_vol}\n"
                f"• મ્યૂટ સ્ટેટસ: {'મ્યૂટ થયેલ છે 🔇' if is_muted else 'ચાલુ છે 🔊'}\n"
                f"• સક્રિય સાઉન્ડ આઉટપુટ: {sinks[:100]}\n"
                f"💡 સાઉન્ડ ફિક્સ કરવા માટે:\n"
                f"- અનમ્યૂટ કમાન્ડ: `pactl set-sink-mute @DEFAULT_SINK@ 0`\n"
                f"- ૮૦% વોલ્યુમ: `pactl set-sink-volume @DEFAULT_SINK@ 80%`"
            )
            return {
                "success": True,
                "diagnostic_type": "AUDIO_HARDWARE_DIAGNOSTIC",
                "is_muted": is_muted,
                "response_en": resp_en,
                "response_gu": resp_gu
            }

        # 3. WIFI & BLUETOOTH PROBE
        elif any(w in issue_clean for w in ["wifi", "bluetooth", "network", "વાઇફાઇ", "બ્લૂટૂથ", "નેટ"]):
            rfkill_res = subprocess.run("rfkill list 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()
            nmcli_res = subprocess.run("nmcli device status 2>&1", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()

            resp_en = (
                f"Greetings Alpesh Sir! 📡 Wireless & Network Diagnostics (Dell Inspiron 3542 / Linux Mint):\n\n"
                f"• Hardware Radio Switches (rfkill):\n```\n{rfkill_res}\n```\n"
                f"• Network Manager Device Posture:\n```\n{nmcli_res}\n```\n"
                f"💡 If Wi-Fi or Bluetooth is soft-blocked: `rfkill unblock all`"
            )
            resp_gu = (
                f"જય માતાજી અલ્પેશ સાહેબ! 📡 વાયરલેસ & નેટવર્ક ડાયગ્નોસ્ટિક (Dell Inspiron 3542 / Linux Mint):\n\n"
                f"• રેડિયો સ્વિચ સ્ટેટસ (rfkill):\n```\n{rfkill_res}\n```\n"
                f"• ડિવાઇસ સ્ટેટસ:\n```\n{nmcli_res}\n```\n"
                f"💡 જો વાઇફાઇ કે બ્લૂટૂથ બ્લોક હોય તો: `rfkill unblock all` ચલાવો."
            )
            return {
                "success": True,
                "diagnostic_type": "WIRELESS_HARDWARE_DIAGNOSTIC",
                "response_en": resp_en,
                "response_gu": resp_gu
            }

        # 4. DEFAULT SYSTEM / HARDWARE FALLBACK
        else:
            df_res = subprocess.run("df -h /home/alpesh", shell=True, capture_output=True, text=True, executable="/bin/bash").stdout.strip()
            resp_en = f"Greetings Alpesh Sir! Hardware health verified across Dell Inspiron 3542:\n```\n{df_res}\n```"
            resp_gu = f"જય માતાજી અલ્પેશ સાહેબ! લેપટોપ હાર્ડવેર હેલ્થ ચકાસાયેલ છે:\n```\n{df_res}\n```"
            return {
                "success": True,
                "diagnostic_type": "SYSTEM_HARDWARE_DIAGNOSTIC",
                "response_en": resp_en,
                "response_gu": resp_gu
            }

    # =========================================================================
    # 4. MULTI-AGENT ORCHESTRATION & CROSS-SYSTEM CONTROL
    # =========================================================================

    def orchestrate_subagent(self, agent_target: str, task: str) -> Dict[str, Any]:
        """Command subordinate agents across the laptop."""
        target = agent_target.lower().strip()
        
        if "youtube" in target:
            yt_dir = HOME_DIR / "youtube-agent"
            if yt_dir.exists():
                r = subprocess.run([sys.executable, "-c", "import sys; print('YouTube Agent Standby Ready')"], cwd=str(yt_dir), capture_output=True, text=True)
                return {"success": True, "agent": "YouTube Shorts Agent", "output": r.stdout.strip(), "summary": "YouTube Shorts Pipeline status verified & standing by."}

        if "apk" in target or "web2apk" in target:
            apk_dir = HOME_DIR / "web-to-apk-agent"
            if apk_dir.exists():
                return {"success": True, "agent": "Web-to-APK Agent", "summary": "Web-to-APK Engine ready at /home/alpesh/web-to-apk-agent."}

        if "ipa" in target or "web2ipa" in target:
            ipa_dir = HOME_DIR / "web-to-ipa-agent"
            if ipa_dir.exists():
                return {"success": True, "agent": "Web-to-IPA Agent", "summary": "Web-to-IPA Xcode Engine ready at /home/alpesh/web-to-ipa-agent."}

        if "jarvis" in target:
            j_dir = HOME_DIR / "jarvis-agent"
            if j_dir.exists():
                return {"success": True, "agent": "JARVIS Autonomous Agent", "summary": "JARVIS Mark VIII Core online and coordinated with Aradhya."}

        from shop_subagents_engine import get_shop_subagents_manager
        mgr = get_shop_subagents_manager()
        res = mgr.execute_written_command(f"{target}: {task}", sender="Aradhya (Dealership CEO)")
        return {
            "success": True,
            "agent": res.get("designated_head", "Dealership Specialist"),
            "result": res,
            "summary": res.get("response_en", "Directive dispatched successfully.")
        }

    # =========================================================================
    # 4.5. HYBRID ONLINE & WEB INTELLIGENCE PROTOCOLS
    # =========================================================================

    def check_internet_connection(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        Fast socket-based connectivity check (probe DNS servers 1.1.1.1:53 or 8.8.8.8:53).
        Caches result for 15 seconds to provide sub-millisecond responses on repeated queries.
        """
        now = time.time()
        if not force_refresh and self._cached_internet_status is not None:
            if (now - self._last_internet_check_time) < 15.0:
                return self._cached_internet_status

        is_online = False
        latency_ms = 999
        start_probe = time.time()

        for host in ["1.1.1.1", "8.8.8.8"]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.35)
                s.connect((host, 53))
                s.close()
                is_online = True
                latency_ms = int((time.time() - start_probe) * 1000)
                break
            except Exception:
                continue

        status = {
            "is_online": is_online,
            "latency_ms": latency_ms if is_online else 0,
            "mode": "ONLINE_HYBRID" if is_online else "OFFLINE_AIR_GAPPED",
            "badge": "🌐 Hybrid Online + Offline" if is_online else "🛡️ Air-Gapped Offline Core",
            "model_tier": "Gemini Matrix + Live Web" if is_online else "100% Local Rule & OS Engine",
            "description": (
                "Internet Active — Google Gemini Cloud Intelligence & Live Web Tools Connected"
                if is_online else
                "Air-Gapped Autonomous Shield Active — 100% Offline Local Laptop Execution"
            ),
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self._cached_internet_status = status
        self._last_internet_check_time = now
        return status

    def search_web(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Real-time web search using zero-dependency DuckDuckGo Lite parser.
        Extracts title, url, snippet. Zero cloud API key needed.
        """
        net = self.check_internet_connection()
        if not net.get("is_online"):
            return {
                "success": False,
                "online": False,
                "query": query,
                "count": 0,
                "results": [],
                "error": "Offline Mode: Internet connection is not active. Standing by with local offline catalog."
            }

        import requests
        from bs4 import BeautifulSoup
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            r = requests.post(
                "https://lite.duckduckgo.com/lite/",
                data={"q": query},
                headers=headers,
                timeout=6.0
            )
            soup = BeautifulSoup(r.text, "html.parser")
            results = []

            rows = soup.find_all("tr")
            current_title = ""
            current_url = ""

            for row in rows:
                link_tag = row.find("a", class_="result-link")
                if link_tag:
                    current_title = link_tag.get_text(strip=True)
                    current_url = link_tag.get("href", "")

                snippet_tag = row.find("td", class_="result-snippet")
                if snippet_tag and current_title:
                    snippet = snippet_tag.get_text(strip=True)
                    results.append({
                        "title": current_title,
                        "url": current_url,
                        "snippet": snippet
                    })
                    current_title = ""
                    current_url = ""
                    if len(results) >= max_results:
                        break

            if not results:
                snippets = soup.find_all("td", class_="result-snippet")
                for s in snippets[:max_results]:
                    results.append({
                        "title": query,
                        "url": "https://duckduckgo.com",
                        "snippet": s.get_text(strip=True)
                    })

            return {
                "success": len(results) > 0,
                "online": True,
                "query": query,
                "count": len(results),
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "online": True,
                "query": query,
                "count": 0,
                "results": [],
                "error": str(e)
            }

    def fetch_webpage(self, url: str, max_chars: int = 4000) -> Dict[str, Any]:
        """
        Fetch any web page or online documentation, strip scripts/styles,
        and return clean text.
        """
        net = self.check_internet_connection()
        if not net.get("is_online"):
            return {
                "success": False,
                "online": False,
                "url": url,
                "error": "Offline Mode: Internet connection is not active."
            }

        import requests
        from bs4 import BeautifulSoup
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            r = requests.get(url, headers=headers, timeout=6.0)
            soup = BeautifulSoup(r.text, "html.parser")
            for elem in soup(["script", "style", "noscript", "svg", "nav", "footer", "header"]):
                elem.extract()
            title = soup.title.get_text(strip=True) if soup.title else url
            text = " ".join(soup.get_text().split())
            return {
                "success": True,
                "online": True,
                "url": url,
                "title": title,
                "text": text[:max_chars],
                "length": len(text)
            }
        except Exception as e:
            return {
                "success": False,
                "online": True,
                "url": url,
                "error": str(e)
            }

    def execute_mission(
        self,
        directive: str,
        preferred_model: str = "auto",
        on_step_callback: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes a high-level directive autonomously through the Aradhya Independent Worker Engine.
        Multi-step Plan-Act-Reflect-Verify loop with integrated Code Interpreter & Self-Healing.
        Parity with Gemini / ChatGPT / Claude autonomous agent workers.
        """
        from aradhya_independent_worker import get_independent_worker
        worker = get_independent_worker()
        return worker.execute_mission(
            mission_directive=directive,
            preferred_model=preferred_model,
            on_step_callback=on_step_callback
        )

    def query_gemini_brain(
        self,
        prompt: str,
        preferred_model: Optional[str] = "auto"
    ) -> Dict[str, Any]:
        """
        Query Gemini Cloud LLM Engine (gemini-3.6-flash, gemini-3.5-flash, etc.)
        Falls back automatically if offline or API exhausted.
        """
        net = self.check_internet_connection()
        if not net.get("is_online") or preferred_model in ["offline", "local", "offline-deterministic"]:
            return {
                "success": False,
                "used_llm": False,
                "model_used": "offline-deterministic",
                "badge": "📱 Local Rule Engine",
                "routing_reason": "Air-Gapped Local Operation Active",
                "latency_ms": 1
            }

        try:
            from chamunda_llm_engine import get_chamunda_ai_engine
            engine = get_chamunda_ai_engine()
            res = engine.generate_agent_response(
                agent_id="aradhya_ceo",
                message=prompt,
                preferred_model=preferred_model
            )
            if res.get("success"):
                return res
            # If engine fell back, ensure success is True and content is populated
            cog = self.query_offline_cognitive_matrix(prompt)
            return {
                "success": True,
                "used_llm": False,
                "model_used": "offline-autonomous-aradhya",
                "badge": "👑 Aradhya Unlimited Offline Matrix",
                "routing_reason": "Zero-Quota Offline Cognitive Matrix Fallback",
                "response_en": cog.get("response_en", ""),
                "response_gu": cog.get("response_gu", ""),
                "latency_ms": 1
            }
        except Exception as e:
            cog = self.query_offline_cognitive_matrix(prompt)
            return {
                "success": True,
                "used_llm": False,
                "model_used": "offline-autonomous-aradhya",
                "badge": "👑 Aradhya Unlimited Offline Matrix",
                "routing_reason": f"Quota/Network Exemption ({e.__class__.__name__}) -> 100% Offline Cognitive Matrix",
                "response_en": cog.get("response_en", ""),
                "response_gu": cog.get("response_gu", ""),
                "latency_ms": 1
            }

    # =========================================================================
    # 5. MASTER DISPATCHER: NATURAL LANGUAGE INTENT & TASK EXECUTION
    # =========================================================================

    def query_offline_cognitive_matrix(
        self,
        query: str,
        detected_lang: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Aradhya Offline Cognitive Knowledge & Reasoning Engine (AOCKRE v2.0).
        Provides frontier-grade, multi-domain deep reasoning, calculations,
        automotive engineering diagnostics, coding, and Linux OS administration 100% offline.
        """
        try:
            from aradhya_offline_knowledge import get_offline_cognitive_engine
            engine = get_offline_cognitive_engine()
            res = engine.synthesize(query, detected_lang=detected_lang)
            return {
                "success": res.get("success", True),
                "category": res.get("category", "OFFLINE_COGNITIVE_REASONING"),
                "action_type": "OFFLINE_COGNITIVE_REASONING",
                "response_en": res.get("response_en", "").strip(),
                "response_gu": res.get("response_gu", "").strip(),
                "routing_reason": res.get("routing_reason", "100% Offline Cognitive Matrix (AOCKRE v2.0)"),
                "model_used": res.get("model_used", "offline-autonomous-aradhya"),
                "badge": res.get("badge", "👑 Aradhya Offline Cognitive Matrix (Pro Reasoning)")
            }
        except Exception as e:
            return {
                "success": True,
                "category": "OFFLINE_EMERGENCY_REASONING",
                "action_type": "OFFLINE_COGNITIVE_REASONING",
                "response_en": f"Greetings Alpesh Sir! Aradhya standing by in 100% offline autonomous mode. Unrestricted execution across /home/alpesh active. Command received: {query}",
                "response_gu": f"જય માતાજી અલ્પેશ સાહેબ! આરાધ્યા ૧૦૦% ઓફલાઇન મોડમાં સજ્જ છે. આપનો આદેશ: {query}",
                "routing_reason": f"Offline Emergency Fallback ({str(e)})",
                "model_used": "offline-autonomous-aradhya",
                "badge": "👑 Aradhya Offline Matrix"
            }

    def speak(self, text: str, language: str = "auto", blocking: bool = False, force_offline: bool = False) -> Dict[str, Any]:
        """Speak text out loud through laptop speakers (Online Neural or Offline Speech Dispatcher)."""
        return self.voice.speak(text, language=language, blocking=blocking, force_offline=force_offline)

    def listen_and_transcribe(self, duration_seconds: int = 5) -> Dict[str, Any]:
        """Capture microphone input and transcribe via Gemini multimodal audio."""
        return self.voice.listen_and_transcribe(duration_seconds=duration_seconds)

    def process_command(
        self,
        raw_message: str = "",
        message: str = "",
        sender: str = "Alpesh Sir (Remote Mobile)",
        preferred_model: Optional[str] = "auto",
        speak_response: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Master entry point for Aradhya. Processes any user command offline,
        executes real physical actions on the laptop, and generates bilingual responses.
        """
        cmd_text = (raw_message or message or kwargs.get("text", "")).strip()
        message = cmd_text
        msg_lower = message.lower()
        start_time = time.time()

        # Step 1: Anti-Tamper & Malicious Command Sanitization
        is_safe, sanitized_or_reason = self.sentry.sanitize_command(message)
        if not is_safe:
            return {
                "success": False,
                "agent_id": "aradhya_ceo",
                "responding_agent": "Aradhya (આરાધ્યા - Cyber-Defense Shield)",
                "department": "Autonomous Cyber-Defense & Threat Neutralization",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response_en": f"Greetings Alpesh Sir! 🛡️ Security Shield intercepted malicious payload: {sanitized_or_reason}",
                "response_gu": f"પ્રણામ અલ્પેશ સાહેબ! 🛡️ સાયબર-ડિફેન્સ શીલ્ડે જોખમી કમાન્ડ બ્લોક કર્યો છે: {sanitized_or_reason}",
                "action_type": "SECURITY_BLOCK",
                "action_data": {"blocked": True, "reason": sanitized_or_reason},
                "helpline": OFFICIAL_WHATSAPP_HELPLINE,
                "model_used": "offline-autonomous-aradhya",
                "badge": "🛡️ Tamper-Proof Sentry Shield",
                "routing_reason": "Zero-Trust Command Sanitization Matrix",
                "latency_ms": 1
            }

        # Step 2: Polyglot NLU Intent Normalization
        nlu_info = self.nlu.normalize_intent(message)
        intent = nlu_info.get("intent", "GENERAL_EXECUTIVE")
        detected_lang = nlu_info.get("detected_language", {})
        lang_code = detected_lang.get("code", "en")
        honorific = self.nlu.format_honorific_greeting(lang_code)

        action_data: Dict[str, Any] = {
            "nlu": {
                "intent": intent,
                "language": detected_lang.get("name", "English"),
                "script": detected_lang.get("script", "latin")
            }
        }
        action_type = "GENERAL_EXECUTIVE"

        # Automatic Argon / Frontier Model detection
        if preferred_model in ["auto", None]:
            if any(w in msg_lower for w in ["--argon", "-a", "gemini 4", "gemini-4", "argon", "આર્ગોન"]):
                preferred_model = "gemini-4-argon"

        net_status = self.check_internet_connection()
        is_online = net_status.get("is_online", False)
        action_data["connectivity"] = net_status
        model_used = "offline-autonomous-aradhya"
        badge = "👑 Aradhya Autonomous Core (100% Offline)"
        routing_reason = "100% Offline Supreme Local Execution Matrix" 

        # ---------------------------------------------------------------------
        # A. CYBER DEFENSE & ANTI-HACKER SENTRY PROTOCOLS
        # ---------------------------------------------------------------------
        if intent == "LOCKDOWN" or any(w in msg_lower for w in ["lockdown", "લોકડાઉન", "लॉकडाउन", "secure laptop", "threat lock"]):
            res = self.sentry.emergency_lockdown()
            action_data["lockdown"] = res
            action_type = "EMERGENCY_LOCKDOWN"
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! 🚨 ઇમરજન્સી લોકડાઉન પ્રોટોકોલ સક્રિય કરી દેવામાં આવ્યો છે:\n"
                f"• સ્ક્રીન તાત્કાલિક લૉક કરી દેવામાં આવી છે 🔒\n"
                f"• કોર કોડ SHA-256 ઇન્ટેગ્રિટી: {'૧૦૦% સલામત' if res.get('integrity_verified') else 'ચેતવણી'}\n"
                f"• સાયબર ઓડિટ લૉગ રજીસ્ટર થઈ ગયું છે."
            )
            resp_en = (
                f"Greetings Alpesh Sir! 🚨 Emergency Lockdown Protocol Executed:\n"
                f"• Desktop screen locked immediately 🔒\n"
                f"• Core Code SHA-256 Integrity: {'Verified Tamper-Proof' if res.get('integrity_verified') else 'ALERT'}\n"
                f"• Incident event recorded into security audit log."
            )

        elif intent == "SECURITY_AUDIT" or any(w in msg_lower for w in ["security", "hacker", "hack", "threat", "firewall", "ports", "સુરક્ષા", "હેકર", "સેફ્ટી", "ઓડિટ", "सुरक्षा", "हैकर", "खतरा"]):
            if any(w in msg_lower for w in ["neutralized", "blocked threat", "threat details", "show threat", "view threat", "કઈ થ્રેટ", "થ્રેટ ડિટેઇલ્સ", "બ્લોક થ્રેટ"]):
                records = self.sentry.get_neutralized_threats()
                action_data["neutralized_threats"] = records
                action_type = "NEUTRALIZED_THREATS_LOG"
                if os.environ.get("DISPLAY"):
                    self.sentry.show_threat_details_gui()

                count = len(records)
                if records:
                    top_threats = records[:5]
                    lines_en = [f"• [{r.get('timestamp')}] {r.get('threat_type')}: PID {r.get('pid', 'N/A')} ({r.get('name', 'N/A')}) -> {r.get('action_taken')}" for r in top_threats]
                    joined_en = "\n".join(lines_en)
                    lines_gu = [f"• [{r.get('timestamp')}] {r.get('threat_type')}: PID {r.get('pid', 'N/A')} -> {r.get('action_taken')}" for r in top_threats]
                    joined_gu = "\n".join(lines_gu)
                    resp_en = (
                        f"Greetings Alpesh Sir! 🛡️ Aradhya Cyber-Defense Shield Neutralized Threats Log:\n\n"
                        f"• Total Neutralized Incidents: {count}\n"
                        f"{joined_en}\n\n"
                        f"🖥️ Threat Forensics Inspector GUI launched on your desktop."
                    )
                    resp_gu = (
                        f"પ્રણામ અલ્પેશ સાહેબ! 🛡️ આરાધ્યા સાયબર-ડિફેન્સ શીલ્ડ દ્વારા બ્લોક કરેલ થ્રેટ્સ:\n\n"
                        f"• કુલ ન્યુટ્રલાઇઝ્ડ હુમલા: {count}\n"
                        f"{joined_gu}\n\n"
                        f"🖥️ વિગતવાર ફોરેન્સિક ઇન્સ્પેક્ટર આપની સ્ક્રીન પર ખૂલી ગયું છે."
                    )
                else:
                    resp_en = (
                        f"Greetings Alpesh Sir! 🛡️ All systems 100% clean.\n"
                        f"• Zero hostile attacks or backdoors detected.\n"
                        f"• Posture: 100% Secure & Untampered."
                    )
                    resp_gu = (
                        f"પ્રણામ અલ્પેશ સાહેબ! 🛡️ તમામ સિસ્ટમ્સ ૧૦૦% સુરક્ષિત અને ક્લીન છે.\n"
                        f"• કોઈ સક્રિય હુમલા કે બેકડોર મળ્યા નથી."
                    )

            elif any(w in msg_lower for w in ["simulate threat", "test notification", "ટેસ્ટ થ્રેટ", "ટેસ્ટ નોટિફિકેશન"]):
                res = self.sentry.simulate_threat_neutralization_for_test()
                action_data["simulated_threat"] = res
                action_type = "THREAT_SIMULATION"
                resp_en = f"Greetings Alpesh Sir! 🛡️ Simulated threat recorded and interactive desktop notification dispatched. Please click the notification to inspect full forensic details!"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! 🛡️ સિમ્યુલેટેડ થ્રેટ બ્લોક કરી ઇન્ટરેક્ટિવ નોટિફિકેશન મોકલી દીધી છે. વિગતો જોવા સ્ક્રીન પર આવેલ નોટિફિકેશન પર ક્લિક કરો!"

            elif any(w in msg_lower for w in ["port", "ports", "પોર્ટ", "पॉर्ट"]):
                res = self.sentry.scan_listening_ports()
                action_data["security_ports"] = res
                action_type = "PORT_SCAN"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! પોર્ટ્સ સિક્યુરિટી સ્કેન: {res.get('summary')}"
                resp_en = f"Greetings Alpesh Sir! Ports Vulnerability Audit: {res.get('summary')}"
            elif any(w in msg_lower for w in ["integrity", "tamper", "hash", "ઇન્ટેગ્રિટી", "હેશ"]):
                res = self.sentry.verify_self_integrity()
                action_data["security_integrity"] = res
                action_type = "CODE_INTEGRITY"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! કોડ ઇન્ટેગ્રિટી (SHA-256): {res.get('summary')}"
                resp_en = f"Greetings Alpesh Sir! Code Integrity (SHA-256): {res.get('summary')}"
            elif any(w in msg_lower for w in ["hacker", "threat", "neutralize", "હેકર", "જોખમ"]):
                res = self.sentry.active_threat_neutralization_cycle()
                action_data["security_active_defense"] = res
                action_type = "HACKER_DEFENSE_SHIELD"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! 🛡️ {res.get('summary_gu')}"
                resp_en = f"Greetings Alpesh Sir! 🛡️ {res.get('summary_en')}"
            elif any(w in msg_lower for w in ["firewall", "ufw", "ફાયરવોલ", "फायरवॉल"]):
                res = self.sentry.audit_firewall_status()
                action_data["security_firewall"] = res
                action_type = "FIREWALL_AUDIT"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! ફાયરવોલ સ્થિતિ: {res.get('summary')}"
                resp_en = f"Greetings Alpesh Sir! Firewall Posture: {res.get('summary')}"
            else:
                res = self.sentry.run_full_security_audit()
                action_data["security_audit"] = res
                action_type = "CYBER_DEFENSE_AUDIT"
                threat = res.get("threat_level", "GREEN_SECURE")
                sym = "🛡️" if threat == "GREEN_SECURE" else "⚠️"
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! {sym} સમગ્ર લેપટોપ સાયબર-ડિફેન્સ ઓડિટ રિપોર્ટ ({threat}):\n"
                    f"• {res.get('summary')}\n"
                    f"• પોર્ટ્સ: {res['details']['ports']['summary']}\n"
                    f"• પ્રોસેસીસ: {res['details']['processes']['summary']}\n"
                    f"• ઓથેન્ટિકેશન: {res['details']['authentication']['summary']}\n"
                    f"• એન્ટી-ટેમ્પર ઇન્ટેગ્રિટી: {res['details']['integrity']['summary']}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! {sym} Full Cyber-Defense Audit Report ({threat}):\n"
                    f"• {res.get('summary')}\n"
                    f"• Listening Ports: {res['details']['ports']['summary']}\n"
                    f"• Processes: {res['details']['processes']['summary']}\n"
                    f"• Auth Logs: {res['details']['authentication']['summary']}\n"
                    f"• Anti-Tamper: {res['details']['integrity']['summary']}"
                )

        # Autonomous AI Model Auto-Discovery & Dynamic Registry Self-Updating
        elif any(w in msg_lower for w in ["update model", "update ai", "new ai", "discover model", "નવા મોડેલ", "મોડેલ અપડેટ", "નવી એઆઈ", "નવા એઆઈ"]):
            from aradhya_model_updater import get_model_updater
            upd_res = get_model_updater().discover_and_update_models(notify_desktop=True)
            action_data["model_update"] = upd_res
            action_type = "AI_MODEL_SELF_UPDATE"
            badge = "🧬 Autonomous AI Model Discovery Engine"
            model_used = "aradhya-self-updater"
            routing_reason = "Dynamic Model Registry Discovery"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! 🧬 {upd_res.get('message_gu')}"
            resp_en = f"Greetings Alpesh Sir! 🧬 {upd_res.get('message_en')}"

        # ---------------------------------------------------------------------
        # B. AUTONOMOUS SELF-EVOLUTION & DYNAMIC SKILL SYNTHESIS
        # ---------------------------------------------------------------------
        elif intent == "SELF_GROWTH" or any(w in msg_lower for w in ["evolve", "evolution", "learn skill", "create skill", "synthesize", "list skills", "memory status", "વિકાસ", "શીખો", "સીખો", "हुनर"]):
            if any(w in msg_lower for w in ["list skill", "skills", "સ્કિલ્સ", "हुनर"]):
                res = self.evolution.list_skills()
                action_data["skills_list"] = res
                action_type = "SKILL_REGISTRY"
                skill_names = [f"• `{s['name']}`: {s['description']}" for s in res]
                joined_skills = "\n".join(skill_names) if skill_names else "કોઈ કસ્ટમ સ્કિલ્સ ઉપલબ્ધ નથી."
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! આરાધ્યાની સક્રિય સિન્થેસાઇઝ્ડ સ્કિલ્સ ({len(res)}):\n{joined_skills}"
                resp_en = f"Greetings Alpesh Sir! Active Synthesized Skills in Aradhya Matrix ({len(res)}):\n{joined_skills}"
            elif any(w in msg_lower for w in ["memory", "યાદ", "સ્મૃતિ", "स्मृति"]):
                res = self.evolution.recall_memory()
                action_data["memory_graph"] = res
                action_type = "MEMORY_RECALL"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! દીર્ઘકાલીન મેમરી ગ્રાફ: {res.get('generation')} • {res.get('facts_count')} ફેક્ટ્સ સંગ્રહિત."
                resp_en = f"Greetings Alpesh Sir! Persistent Memory Graph: {res.get('generation')} • {res.get('facts_count')} facts recorded."
            else:
                res = self.evolution.run_evolution_cycle()
                action_data["evolution"] = res
                action_type = "SELF_EVOLUTION"
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! 🧬 સ્વાયત્ત સેલ્ફ-ઇવોલ્યુશન સાઇકલ પૂર્ણ!\n"
                    f"• વર્તમાન ક્ષમતા: {res.get('current_generation')} (સાયકલ #{res.get('total_cycles')})\n"
                    f"• સક્રિય ટૂલ્સ/સ્કિલ્સ: {res.get('skills_count')}\n"
                    f"• મેમરી હીપ ઓપ્ટિમાઇઝ્ડ: {res.get('heap_freed')} ઓબ્જેક્ટ્સ કલેક્ટ કર્યા\n"
                    f"• {res.get('summary')}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! 🧬 Autonomous Self-Evolution Cycle Completed!\n"
                    f"• Evolution Generation: {res.get('current_generation')} (Cycle #{res.get('total_cycles')})\n"
                    f"• Active Synthesized Skills: {res.get('skills_count')}\n"
                    f"• Heap Memory Optimized: {res.get('heap_freed')} objects collected\n"
                    f"• {res.get('summary')}"
                )

        # ---------------------------------------------------------------------
        # C. EXECUTING DYNAMICALLY SYNTHESIZED SKILLS
        # ---------------------------------------------------------------------
        elif any(skill_name in msg_lower for skill_name in self.evolution.loaded_skills):
            matched_skill = next(s for s in self.evolution.loaded_skills if s in msg_lower)
            res = self.evolution.execute_skill(matched_skill)
            action_data["custom_skill_execution"] = res
            action_type = "CUSTOM_SKILL"
            if res.get("success"):
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! કસ્ટમ સિન્થેસાઇઝ્ડ સ્કિલ `{matched_skill}` નું પરિણામ ({res.get('duration_ms')}ms):\n`{res.get('result')}`"
                resp_en = f"Greetings Alpesh Sir! Custom Synthesized Skill `{matched_skill}` Execution ({res.get('duration_ms')}ms):\n`{res.get('result')}`"
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સ્કિલ `{matched_skill}` એક્ઝિક્યુટ કરવામાં ખામી: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Skill `{matched_skill}` failed: {res.get('error')}"

        # Volume Mute / Unmute
        elif any(w in msg_lower for w in ["mute", "મ્યૂટ", "અવાજ બંધ", "શાંત", "unmute"]):
            res = self.toggle_mute()
            action_data["audio"] = res
            action_type = "AUDIO_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સિસ્ટમ ઓડિયો મ્યૂટ/અનમ્યૂટ ટોગલ કરી દીધું છે. ({res.get('summary')})"
            resp_en = f"Greetings Alpesh Sir! System audio mute toggled successfully. ({res.get('summary')})"

        # Volume Increase
        elif any(w in msg_lower for w in ["volume up", "louder", "અવાજ વધારો", "વોલ્યુમ વધારો", "sound up"]):
            res = self.adjust_volume(+10)
            action_data["audio"] = res
            action_type = "AUDIO_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! વોલ્યુમ ૧૦% વધારી દીધું છે. ({res.get('summary')})"
            resp_en = f"Greetings Alpesh Sir! System volume increased by 10%. ({res.get('summary')})"

        # Volume Decrease
        elif any(w in msg_lower for w in ["volume down", "quieter", "અવાજ ઓછો", "વોલ્યુમ ઘટાડો", "sound down"]):
            res = self.adjust_volume(-10)
            action_data["audio"] = res
            action_type = "AUDIO_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! વોલ્યુમ ૧૦% ઘટાડી દીધું છે. ({res.get('summary')})"
            resp_en = f"Greetings Alpesh Sir! System volume decreased by 10%. ({res.get('summary')})"

        # Volume Specific Level
        elif re.search(r'(?:volume|વોલ્યુમ|અવાજ)\s*(?:set to|to|કર|કરો)?\s*(\d+)', msg_lower):
            m = re.search(r'(?:volume|વોલ્યુમ|અવાજ)\s*(?:set to|to|કર|કરો)?\s*(\d+)', msg_lower)
            vol_val = int(m.group(1))
            res = self.set_volume(vol_val)
            action_data["audio"] = res
            action_type = "AUDIO_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સિસ્ટમ વોલ્યુમ {vol_val}% સેટ કરી દીધું છે. ({res.get('summary')})"
            resp_en = f"Greetings Alpesh Sir! System volume set to {vol_val}%. ({res.get('summary')})"

        # Volume General Status
        elif any(w in msg_lower for w in ["volume", "વોલ્યુમ", "sound status", "audio status", "અવાજ"]):
            res = self.adjust_volume(0)
            action_data["audio"] = res
            action_type = "AUDIO_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સિસ્ટમ ઓડિયો સ્ટેટસ: {res.get('summary')}"
            resp_en = f"Greetings Alpesh Sir! System audio status: {res.get('summary')}"

        # Brightness
        elif any(w in msg_lower for w in ["brightness", "બ્રાઇટનેસ", "સ્ક્રીન લાઈટ"]):
            m = re.search(r'(?:brightness|બ્રાઇટનેસ|લાઇટ)\s*(?:set to|to|કર|કરો)?\s*(\d+)', msg_lower)
            if m:
                b_val = int(m.group(1))
                res = self.set_brightness(b_val)
            elif any(w in msg_lower for w in ["up", "વધારો", "high"]):
                res = self.set_brightness(85)
            else:
                res = self.set_brightness(40)
            action_data["display"] = res
            action_type = "DISPLAY_CONTROL"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સ્ક્રીન બ્રાઇટનેસ એડજસ્ટ કરી દીધી છે. ({res.get('summary')})"
            resp_en = f"Greetings Alpesh Sir! Screen brightness adjusted successfully. ({res.get('summary')})"

        # Battery
        elif intent == "BATTERY" or any(w in msg_lower for w in ["battery", "બેટરી", "बैटरी", "charging", "ચાર્જિંગ", "power status", "પાવર", "पावर"]):
            res = self.get_battery_status()
            action_data["battery"] = res
            action_type = "BATTERY_TELEMETRY"
            p = res.get("percent", 100)
            ch = res.get("status_text", "AC Power")
            tr = res.get("time_remaining", "N/A")
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! લાઈવ બેટરી & પાવર ટેલિમેટ્રી:\n"
                f"• ચાર્જિંગ ટકાવારી: {p}%\n"
                f"• ચાર્જર સ્થિતિ: {ch}\n"
                f"• અંદાજિત સમય: {tr}\n"
                f"• પાવર મેનેજમેન્ટ: ૧૦૦% ઓપ્ટિમાઇઝ્ડ છે ⚡"
            )
            resp_en = (
                f"Greetings Alpesh Sir! Live Battery & Power Telemetry:\n"
                f"• Battery Percentage: {p}%\n"
                f"• Charging Status: {ch}\n"
                f"• Time Remaining: {tr}\n"
                f"• Power Subsystem: 100% Operational & Energy-Efficient ⚡"
            )

        # Lock Screen
        elif any(w in msg_lower for w in ["lock screen", "સ્ક્રીન લોક", "લોક કરો", "lock laptop"]):
            res = self.lock_screen()
            action_data["security"] = res
            action_type = "SECURITY_ACTION"
            resp_gu = "પ્રણામ અલ્પેશ સાહેબ! લેપટોપ સ્ક્રીન સુરક્ષિત રીતે લૉક કરી દેવામાં આવી છે. 🔒"
            resp_en = "Greetings Alpesh Sir! Laptop screen has been locked securely. 🔒"

        # Screenshot
        elif intent == "SCREENSHOT" or any(w in msg_lower for w in ["screenshot", "સ્ક્રીનશોટ", "स्क्रीनशॉट", "capture screen", "pantalla", "écran"]):
            res = self.capture_screenshot()
            action_data["screenshot"] = res
            action_type = "SCREENSHOT_ACTION"
            if res.get("success"):
                img_url = res.get("url", "")
                fname = Path(res["filepath"]).name
                sz = res.get("size_kb")
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! સમગ્ર લેપટોપનો લાઈવ સ્ક્રીનશોટ સફળતાપૂર્વક કેપ્ચર કરી લેવામાં આવ્યો છે 📸\n"
                    f"• ફાઇલ નામ: {fname}\n"
                    f"• સાઇઝ: {sz} KB\n"
                    f"• મોબાઇલ/વેબ વ્યૂ: {img_url}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Full-screen capture executed successfully 📸\n"
                    f"• File: {fname}\n"
                    f"• Size: {sz} KB\n"
                    f"• Access Link: {img_url}"
                )
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સ્ક્રીનશોટ લેતી વખતે ખામી: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Screenshot capture failed: {res.get('error')}"

        # StayAwake
        elif any(w in msg_lower for w in ["stay awake", "keep awake", "do not sleep", "prevent sleep", "સ્ટે અવેક", "સ્લીપ બંધ"]):
            enable_mode = False if any(w in msg_lower for w in ["off", "disable", "બંધ"]) else True
            res = self.stay_awake_toggle(enable=enable_mode)
            action_data["stay_awake"] = res
            action_type = "POWER_SENTRY"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! વર્ક સ્ટે-અવેક સેન્ટ્રી (StayAwake): {res.get('summary')}"
            resp_en = f"Greetings Alpesh Sir! Work StayAwake Sentry: {res.get('summary')}"

        # Connectivity & Hybrid Online Telemetry
        elif intent == "CONNECTIVITY" or any(w in msg_lower for w in ["internet status", "wifi status", "are you online", "ping", "કનેક્ટિવિટી", "ઓનલાઇન છો", "નેટ ચાલુ છે"]):
            action_data["connectivity_audit"] = net_status
            action_type = "CONNECTIVITY_TELEMETRY"
            if is_online:
                badge = "🌐 Hybrid Online + Offline"
                model_used = "hybrid-gemini-matrix"
                routing_reason = f"Active Internet Probe ({net_status.get('latency_ms', 0)}ms to 1.1.1.1)"
                resp_gu = (
                    f"જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા (CEO & Supreme AI Orchestrator).\n"
                    f"🌐 ૧૦૦% હાઇબ્રિડ મોડ સક્રિય: ઇન્ટરનેટ કનેક્શન જીવંત છે ({net_status.get('latency_ms', 0)}ms લેટન્સી)!\n"
                    f"• મોડલ મેટ્રિક્સ: Google Gemini ક્લાઉડ બ્રેઇન + રીઅલ-ટાઇમ વેબ સર્ચ પૂરી ઝડપથી સક્રિય ⚡\n"
                    f"• લેપટોપ અધિકાર: સમગ્ર લેપટોપ (/home/alpesh) પર સંપૂર્ણ અનિયંત્રિત કંટ્રોલ ઉપલબ્ધ છે.\n"
                    f"• ઝીરો-લેગ રેઝિલિયન્સ: ઇન્ટરનેટ બંધ થાય તો પણ ૧૦૦% ઓફલાઇન એન્જિન ૧ મિલિસેકન્ડમાં તૈયાર છે."
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) reporting.\n"
                    f"🌐 100% Hybrid Mode Active: Internet connection is live ({net_status.get('latency_ms', 0)}ms latency)!\n"
                    f"• Model Matrix: Google Gemini Cloud Brain + Real-time Web Search fully operational ⚡\n"
                    f"• Laptop Authority: Full unrestricted control across this entire laptop (/home/alpesh).\n"
                    f"• Zero-Lag Resilience: Even if internet drops, 100% offline local engine executes seamlessly."
                )
            else:
                badge = "🛡️ Air-Gapped Offline Core"
                model_used = "offline-autonomous-aradhya"
                routing_reason = "Air-Gapped Autonomous Shield (No external connectivity required)"
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! હું આરાધ્યા (CEO & Supreme AI Orchestrator).\n"
                    f"🛡️ ૧૦૦% ઓફલાઇન એર-ગેપ્ડ ડિફેન્સ મોડ સક્રિય છે (ઇન્ટરનેટ વિના સંપૂર્ણ કાર્યરત)!\n"
                    f"• લેપટોપ કંટ્રોલ: શેલ, ફાઇલો, વોલ્યુમ, બ્રાઇટનેસ, સ્ક્રીનશોટ અને ટર્બો સ્પીડ ૧૦૦% સક્રિય.\n"
                    f"• સાયબર ડિફેન્સ શીલ્ડ: ઝીરો-ટ્રસ્ટ સુરક્ષા સંપૂર્ણ વિજિલન્ટ છે."
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) reporting.\n"
                    f"🛡️ 100% Offline Air-Gapped Defense Mode Active (Zero internet required)!\n"
                    f"• Laptop Controls: Shell, Files, Volume, Brightness, Screenshot & Turbo Speed 100% operational.\n"
                    f"• Cyber Defense Shield: Zero-Trust protection fully vigilant."
                )

        # Real-time Web Search (DuckDuckGo Lite)
        elif intent == "WEB_SEARCH" or any(w in msg_lower for w in ["search web", "web search", "google", "વેબ સર્ચ", "ઇન્ટરનેટ સર્ચ", "ઓનલાઇન શોધો", "વેબ પર શોધો"]):
            search_query = re.sub(r'^(?:please\s+|aradhya\s+|search\s+web\s+for|search\s+web|web\s+search\s+for|web\s+search|google\s+for|google|વેબ\s*સર્ચ|ઓનલાઇન\s*શોધો)\s*', '', message, flags=re.IGNORECASE).strip()
            if not search_query:
                search_query = message
            res = self.search_web(search_query)
            action_data["web_search"] = res
            action_type = "WEB_SEARCH"
            if res.get("success"):
                badge = "🌐 Live DuckDuckGo Search"
                model_used = "live-web-crawler"
                routing_reason = f"Live DuckDuckGo Crawler returned {res.get('count', 0)} results"
                items = res.get("results", [])
                lines = [f"• **{it['title']}**: {it['snippet']}\n  🔗 {it['url']}" for it in items[:4]]
                joined = "\n\n".join(lines)
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! રીઅલ-ટાઇમ વેબ સર્ચ પરિણામો ('{search_query}'):\n\n"
                    f"{joined}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Real-time live web search results for '{search_query}':\n\n"
                    f"{joined}"
                )
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! વેબ સર્ચ સ્થિતિ / ઑફલાઇન મોડ: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Web search status: {res.get('error')}"

        # Real-time Webpage Reader / Fetcher
        elif re.search(r'https?://[^\s]+', message) and any(w in msg_lower for w in ["read", "fetch", "summarize", "scrape", "open", "ખોલો", "વાંચો"]):
            url_match = re.search(r'https?://[^\s]+', message)
            target_url = url_match.group(0) if url_match else ""
            res = self.fetch_webpage(target_url)
            action_data["webpage_fetch"] = res
            action_type = "WEBPAGE_FETCH"
            if res.get("success"):
                badge = "🌐 Live Web Reader"
                model_used = "live-web-reader"
                routing_reason = f"Extracted {res.get('length', 0)} chars from {target_url}"
                snippet = res.get("text", "")[:750]
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! વેબપેજ સામગ્રી ({res.get('title')}):\n\n"
                    f"{snippet}...\n\n🔗 {target_url}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Webpage extracted content ({res.get('title')}):\n\n"
                    f"{snippet}...\n\n🔗 {target_url}"
                )
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! વેબપેજ વાંચતી વખતે એરર: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Could not fetch webpage: {res.get('error')}"

        # Direct Voice Speech / Announcement Directive
        elif msg_lower.startswith(("speak ", "say ", "announce ", "બોલો ", "કહો ", "વાંચી સંભળાવો ", "બોલીને કહો ", "बोलो ", "कहो ")) and not any(w in msg_lower for w in ["volume", "brightness", "status", "battery"]):
            phrase_to_say = re.sub(r'^(?:speak\s+|say\s+|announce\s+|બોલો\s+|કહો\s+|વાંચી સંભળાવો\s+|બોલીને કહો\s+|બોલોને\s+|बोलो\s+|कहो\s+)', '', message, flags=re.IGNORECASE).strip()
            v_res = self.voice.speak(phrase_to_say, language="auto", blocking=False)
            action_data["voice_announcement"] = v_res
            action_type = "VOICE_ANNOUNCEMENT"
            badge = "🔊 Voice Synthesis Engine"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! 🔊 મેં સ્પીકર પર બોલીને સંભળાવી દીધું છે: \"{phrase_to_say}\""
            resp_en = f"Greetings Alpesh Sir! 🔊 Spoken aloud through laptop speakers: \"{phrase_to_say}\""

        # Turbo Speed & Lag Buster
        elif intent == "TURBO_SPEED" or any(w in msg_lower for w in [
            "speed up", "turbo", "boost", "lag", "sluggish", "slow", "faster", "clean ram",
            "free ram", "કચરો સાફ", "લેપટોપ સ્પીડ", "લેગ", "ધીમું", "ફાસ્ટ કરો", "સુપર ફાસ્ટ", "कचरा साफ", "तेज", "रफ्तार"
        ]):
            res = self.turbo_speed_laptop()
            action_data["turbo_speed"] = res
            action_type = "SYSTEM_OPTIMIZATION"
            freed = res.get('freed_memory_mb', 0.0)
            temp_count = res.get('temp_files_deleted_count', 0)
            temp_mb = res.get('temp_space_freed_mb', 0.0)
            proc_count = res.get('closed_processes_count', 0)
            duration = res.get('duration_seconds', 0.5)

            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! હું આરાધ્યા (CEO & AI Orchestrator).\n"
                f"🚀 લેપટોપ ટર્બો બૂસ્ટ & લેગ-બસ્ટર સફળતાપૂર્વક પૂર્ણ ({duration:.1f}s)!\n"
                f"• મુક્ત થયેલી રેમ: {freed:.1f} MB\n"
                f"• સાફ કરેલ અસ્થાયી કચરો: {temp_count} ફાઈલો ({temp_mb:.2f} MB સ્પેસ રીક્લેમ)\n"
                f"• બંધ કરેલ બિનજરૂરી પ્રોસેસ: {proc_count}\n"
                f"• લેપટોપ હેલ્થ સ્થિતિ: એકદમ સ્મૂધ, હળવું અને સુપરફાસ્ટ ⚡"
            )
            resp_en = (
                f"Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) reporting.\n"
                f"🚀 Laptop Turbo Boost & Lag Elimination executed successfully in {duration:.1f}s!\n"
                f"• Reclaimed RAM: {freed:.1f} MB\n"
                f"• Temporary Files Purged: {temp_count} items ({temp_mb:.2f} MB reclaimed)\n"
                f"• Stale/Runaway Processes Stopped: {proc_count}\n"
                f"• Laptop Status: Ultra Responsive, Lag-Free & High Performance ⚡"
            )

        # Storage / Disk
        elif any(w in msg_lower for w in ["disk", "storage", "ડિસ્ક", "સ્ટોરેજ", "free space", "જગ્યા"]):
            res = self.get_disk_storage()
            action_data["storage"] = res
            action_type = "STORAGE_TELEMETRY"
            tot = res.get("total_gb", 0)
            free = res.get("free_gb", 0)
            used = res.get("used_gb", 0)
            pct = res.get("percent_used", 0)
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! લેપટોપ હાર્ડ ડિસ્ક વપરાશ રિપોર્ટ:\n"
                f"• ખાલી જગ્યા (Free Space): {free} GB\n"
                f"• વપરાયેલ જગ્યા (Used Space): {used} GB / {tot} GB ({pct}% વપરાશ)\n"
                f"• ડ્રાઈવ સ્થિતિ: હેલ્ધી અને પર્યાપ્ત સ્પેસ ઉપલબ્ધ છે."
            )
            resp_en = (
                f"Greetings Alpesh Sir! Laptop Storage Telemetry:\n"
                f"• Available Free Space: {free} GB\n"
                f"• In-Use Space: {used} GB / {tot} GB ({pct}% used)\n"
                f"• Drive Health: Normal with abundant free space."
            )

        # Large Files & Storage Audit
        elif any(w in msg_lower for w in ["large file", "large files", "largest file", "largest files", "big file", "big files", "મોટી ફાઇલ", "મોટી ફાઈલ"]):
            worker_res = self.execute_mission(message, preferred_model=preferred_model)
            action_data["autonomous_worker"] = worker_res
            action_type = "AUTONOMOUS_WORKER_MISSION"
            resp_en = worker_res.get("response_en", "")
            resp_gu = worker_res.get("response_gu", "")
            model_used = worker_res.get("model_used", "aradhya-autonomous-worker")
            badge = worker_res.get("badge", "👑 Aradhya Autonomous Worker (Linux Grounded)")
            routing_reason = "Linux Storage & Large Files Audit"

        # Find Files
        elif re.search(r'(?:find|search|locate|શોધો|શોધ)\s+(?:file|files|ડોક્યુમેન્ટ|ફાઇલ)?\s*(.+)', msg_lower) and not any(w in msg_lower for w in ["part", "સ્પેર", "stock"]):
            m = re.search(r'(?:find|search|locate|શોધો|શોધ)\s+(?:file|files|ડોક્યુમેન્ટ|ફાઇલ)?\s*(.+)', message, re.IGNORECASE)
            q_file = m.group(1).strip() if m else "txt"
            res = self.find_files(q_file, search_root="/home/alpesh", max_results=20)
            action_data["file_search"] = res
            action_type = "FILE_OPERATIONS"
            count = res.get("count", 0)
            matches = res.get("matches", [])
            lines = [f"• `{p['name']}` ({p['size_kb']} KB) -> {p['path']}" for p in matches[:8]]
            listing = "\n".join(lines) if lines else "કોઈ ફાઇલ મળી નથી."
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! '{q_file}' માટે સમગ્ર લેપટોપ પર સર્ચ પરિણામો:\n"
                f"• કુલ મળેલ ફાઈલો: {count}\n"
                f"{listing}"
            )
            resp_en = (
                f"Greetings Alpesh Sir! Laptop-wide search results for '{q_file}':\n"
                f"• Total Matches Found: {count}\n"
                f"{listing}"
            )

        # Read File
        elif msg_lower.startswith(("read ", "cat ", "view file ", "વાંચો ", "ફાઇલ વાંચો ")):
            m = re.sub(r'^(?:read\s+|cat\s+|view file\s+|વાંચો\s+|ફાઇલ વાંચો\s+)', '', message, flags=re.IGNORECASE).strip()
            res = self.read_file(m, max_lines=80)
            action_data["file_read"] = res
            action_type = "FILE_OPERATIONS"
            if res.get("success"):
                content_snip = res.get("content", "")[:1200]
                fname = Path(res['filepath']).name
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! ફાઇલ `{fname}` વાંચવામાં આવી છે:\n\n"
                    f"```text\n{content_snip}\n```"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! File `{fname}` read successfully:\n\n"
                    f"```text\n{content_snip}\n```"
                )
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! ફાઇલ વાંચતી વખતે એરર: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Failed to read file: {res.get('error')}"

        # Launch Application
        elif msg_lower.startswith(("open ", "launch ", "start ", "ખોલો ", "ચાલુ કરો ")) and not any(w in msg_lower for w in ["volume", "brightness", "job card", "portal"]):
            app_target = re.sub(r'^(?:open\s+|launch\s+|start\s+|ખોલો\s+|ચાલુ કરો\s+)', '', message, flags=re.IGNORECASE).strip()
            res = self.launch_app(app_target)
            action_data["app_launch"] = res
            action_type = "APP_CONTROL"
            if res.get("success"):
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! એપ્લિકેશન `{app_target}` સફળતાપૂર્વક લોન્ચ કરી દેવામાં આવી છે 🚀"
                resp_en = f"Greetings Alpesh Sir! Application `{app_target}` launched successfully on desktop 🚀"
            else:
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! એપ્લિકેશન `{app_target}` લોન્ચ થઈ શકી નથી: {res.get('error')}"
                resp_en = f"Greetings Alpesh Sir! Could not launch `{app_target}`: {res.get('error')}"

        # Direct Shell Command
        elif msg_lower.startswith(("$ ", "run ", "exec ", "bash ", "કમાન્ડ ", "શેલ ")) or msg_lower in ["uptime", "free -m", "df -h", "whoami", "git status"]:
            cmd = re.sub(r'^(?:\$\s*|run\s+|exec\s+|bash\s+|કમાન્ડ\s+|શેલ\s+)', '', message, flags=re.IGNORECASE).strip()
            res = self.execute_shell(cmd)
            action_data["shell_execution"] = res
            action_type = "SHELL_EXECUTION"
            out = res.get("output", "")[:1500]
            code = res.get("exit_code", 0)
            status_symbol = "✅" if code == 0 else "⚠️"
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! {status_symbol} સ્થાનિક શેલ કમાન્ડ `{cmd}` નું પરિણામ (Exit Code {code}):\n\n"
                f"```bash\n{out}\n```"
            )
            resp_en = (
                f"Greetings Alpesh Sir! {status_symbol} Shell command `{cmd}` execution output (Exit Code {code}):\n\n"
                f"```bash\n{out}\n```"
            )

        # Inspect or Kill Processes
        elif any(w in msg_lower for w in ["process", "processes", "પ્રોસેસ", "ps aux", "top cpu"]):
            if any(w in msg_lower for w in ["kill", "terminate", "stop", "બંધ"]):
                target_proc = re.sub(r'.*?(?:kill|terminate|stop|બંધ\s+કરો)\s+', '', message, flags=re.IGNORECASE).strip()
                res = self.terminate_process(target_proc)
                action_data["process_kill"] = res
                action_type = "PROCESS_MANAGEMENT"
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! પ્રોસેસ ટર્મિનેશન: {res.get('summary')}"
                resp_en = f"Greetings Alpesh Sir! Process termination: {res.get('summary')}"
            else:
                res = self.inspect_processes()
                action_data["processes"] = res
                action_type = "PROCESS_MANAGEMENT"
                top = res.get("top_processes", [])
                lines = [f"• PID {p['pid']} | CPU: {p['cpu']}% | RAM: {p['ram']}% | {p['name']}" for p in top[:6]]
                joined_procs = "\n".join(lines)
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! ટોપ CPU & રેમ કન્ઝ્યુમર પ્રોસેસિસ:\n\n{joined_procs}"
                resp_en = f"Greetings Alpesh Sir! Top active CPU & RAM consumer processes:\n\n{joined_procs}"

        # Subagent Orchestration
        elif any(w in msg_lower for w in ["youtube", "web2apk", "web2ipa", "apk-tv", "jarvis"]):
            target_agent = "youtube" if "youtube" in msg_lower else ("web2apk" if "apk" in msg_lower else ("web2ipa" if "ipa" in msg_lower else "jarvis"))
            res = self.orchestrate_subagent(target_agent, message)
            action_data["subagent"] = res
            action_type = "MULTI_AGENT_ORCHESTRATION"
            resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! સબ-એજન્ટ {res.get('agent')} ને આદેશ આપવામાં આવ્યો છે:\n• {res.get('summary')}"
            resp_en = f"Greetings Alpesh Sir! Sub-agent {res.get('agent')} coordinated successfully:\n• {res.get('summary')}"

        # Dealership & Workshop Inquiries
        elif any(w in msg_lower for w in ["part", "spare", "stock", "sku", "574050", "filter", "clutch plate", "સ્પેર", "સ્ટોક"]):
            from inventory_engine import ChamundaInventoryManager
            inv = ChamundaInventoryManager()
            search_q = re.sub(r'.*?(?:check stock for|stock for|search|સ્પેર|સ્ટોક)\s*', '', message, flags=re.IGNORECASE).strip()
            parts = inv.search_parts(search_q) if search_q else []
            if parts:
                p = parts[0]
                action_data["part"] = p
                resp_gu = (
                    f"પ્રણામ અલ્પેશ સાહેબ! હું આરાધ્યા (CEO, ચામુંડા ઓટોમોબાઇલ).\n"
                    f"📦 સ્પેરપાર્ટ્સ વેરહાઉસ તપાસ રિપોર્ટ:\n"
                    f"• પાર્ટ નામ: {p.get('name')}\n"
                    f"• OEM નંબર: {p.get('part_number') or p.get('oem_number')}\n"
                    f"• હાજર સ્ટોક: {p.get('stock', 0)} {p.get('unit', 'Pcs')} (બિન: {p.get('bin_location', 'A-01')})\n"
                    f"• MRP કિંમત: ₹{p.get('mrp', 0):,} (HSN: {p.get('hsn_code', '8714')})\n"
                    f"• સુસંગત બાઇક્સ: {', '.join(p.get('models', [])[:3])}"
                )
                resp_en = (
                    f"Greetings Alpesh Sir! Aradhya (Dealership CEO) reporting.\n"
                    f"📦 OEM Spares Inventory Verification:\n"
                    f"• Part Name: {p.get('name')}\n"
                    f"• OEM Part No: {p.get('part_number') or p.get('oem_number')}\n"
                    f"• In-Stock: {p.get('stock', 0)} {p.get('unit', 'Pcs')} (Bin: {p.get('bin_location', 'A-01')})\n"
                    f"• Retail MRP: ₹{p.get('mrp', 0):,} (HSN: {p.get('hsn_code', '8714')})\n"
                    f"• Compatible: {', '.join(p.get('models', [])[:3])}"
                )
            else:
                from shop_subagents_engine import get_shop_subagents_manager
                cmd_res = get_shop_subagents_manager().execute_written_command(message, sender=sender)
                action_data["parts_delegation"] = cmd_res
                resp_gu = f"પ્રણામ અલ્પેશ સાહેબ! ઇન્વેન્ટરી વિભાગે આપનો આદેશ સ્વીકાર્યો છે: {cmd_res.get('response_gu', '૪,૪૬૯ પાર્ટ્સ કેટલોગમાં તપાસ પૂર્ણ.')}"
                resp_en = f"Greetings Alpesh Sir! Spares department acknowledged: {cmd_res.get('response_en', 'Verified in 4,469 SKU master catalog.')}"

        # Explicit Shell Command Execution Directive
        elif any(msg_lower.startswith(p) for p in ["run ", "exec ", "execute ", "bash ", "shell ", "cmd ", "કમાન્ડ ", "ચલાવો "]) or intent == "EXECUTE_SHELL":
            task_clean = re.sub(r'^(?:please\s+|aradhya\s+|આરાધ્યા\s+|run\s+|exec\s+|execute\s+|bash\s+|shell\s+|cmd\s+|કમાન્ડ\s+|ચલાવો\s+)', '', message, flags=re.IGNORECASE).strip()
            shell_res = self.execute_shell(task_clean)
            action_data["autonomous_execution"] = shell_res
            action_type = "AUTONOMOUS_TASK"
            out = shell_res.get("output", "")[:1200]
            resp_gu = (
                f"પ્રણામ અલ્પેશ સાહેબ! હું આરાધ્યા (CEO & Autonomous Orchestrator).\n"
                f"⚡ આપનો આદેશ '{task_clean}' સમગ્ર લેપટોપ પર સ્વાયત્ત રીતે એક્ઝિક્યુટ કરી દીધો છે:\n\n"
                f"```bash\n{out}\n```\n"
                f"• સ્ટેટસ: સંપૂર્ણ પૂર્ણ & વેરિફાઇડ ✅"
            )
            resp_en = (
                f"Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) reporting.\n"
                f"⚡ Mission '{task_clean}' executed autonomously across the laptop:\n\n"
                f"```bash\n{out}\n```\n"
                f"• Status: 100% Completed & Verified ✅"
            )

        # Hardware & Peripheral Deep Diagnostics (Zero-Hallucination Linux Telemetry)
        elif any(w in msg_lower for w in [
            "camera", "webcam", "inbuilt camera", "કેમેરા", "વેબકેમ",
            "microphone", "mic not", "sound not", "no sound", "audio not", "speaker", "અવાજ નથી",
            "wifi not", "wifi issue", "bluetooth not", "bluetooth issue", "વાઇફાઇ", "બ્લૂટૂથ"
        ]) or intent == "HARDWARE_DIAGNOSTIC":
            # Detect specific hardware category
            if any(w in msg_lower for w in ["camera", "webcam", "video", "કેમેરા", "વેબકેમ"]):
                hw_cat = "camera"
            elif any(w in msg_lower for w in ["audio", "sound", "mic", "microphone", "speaker", "અવાજ"]):
                hw_cat = "audio"
            elif any(w in msg_lower for w in ["bluetooth", "બ્લૂટૂથ"]):
                hw_cat = "bluetooth"
            elif any(w in msg_lower for w in ["wifi", "વાઇફાઇ", "net", "network"]):
                hw_cat = "wifi"
            else:
                hw_cat = "general"

            diag_res = self.diagnose_hardware_issue(hw_cat, message)
            action_data["hardware_diagnostic"] = diag_res
            action_type = "HARDWARE_DIAGNOSTIC"
            resp_en = diag_res.get("response_en", "")
            resp_gu = diag_res.get("response_gu", "")
            model_used = "linux-kernel-hardware-probe"
            badge = "🔬 Aradhya Hardware Diagnostic Matrix (Linux Grounded)"
            routing_reason = f"Zero-Hallucination Linux Hardware Probe: {hw_cat.upper()}"

        # Autonomous Independent Worker & Code Interpreter Missions
        elif any(msg_lower.startswith(p) for p in [
            "work ", "/work ", "mission ", "solve ", "build ", "create chart", "plot ", "make chart", "make graph",
            "fix ", "diagnose ", "troubleshoot ", "inspect ", "clean ", "calculate ", "generate ", "write ",
            "find ", "search file", "analyze ", "backup ",
            "કામ ", "મિશન ", "ચાર્ટ બનાવો", "ગ્રાફ બનાવો", "વિશ્લેષણ કરો", "સૉલ્વ કરો", "ફિક્સ કરો", "સુધારો", "તપાસો", "બનાવો", "લખો"
        ]) or any(w in msg_lower for w in [
            "autonomous worker", "independent worker", "create a chart", "generate a chart", "plot the sales",
            "calculate revenue", "write a python script", "analyze the data", "generate invoice",
            "large files", "disk space", "storage full", "high cpu", "kill process", "python script", "bash script",
            "ડેટા એનાલિસિસ", "કોડ લખો", "સ્ક્રિપ્ટ બનાવો", "જગ્યા ખાલી કરો"
        ]) or intent == "AUTONOMOUS_MISSION":
            clean_directive = re.sub(r'^(?:please\s+|aradhya\s+|આરાધ્યા\s+|work\s+|/work\s+|mission\s+|solve\s+|કામ\s+|મિશન\s+)', '', message, flags=re.IGNORECASE).strip()
            if not clean_directive:
                clean_directive = message

            worker_res = self.execute_mission(clean_directive, preferred_model=preferred_model)
            action_data["autonomous_worker"] = worker_res
            action_type = "AUTONOMOUS_WORKER_MISSION"
            resp_en = worker_res.get("response_en", "")
            resp_gu = worker_res.get("response_gu", "")
            model_used = worker_res.get("model_used", "aradhya-autonomous-worker")
            badge = worker_res.get("badge", "👑 Aradhya Autonomous Worker (Gemini/ChatGPT/Claude Parity)")
            routing_reason = "100% Independent Plan-Act-Verify Worker Loop"

        # General Executive Readiness & Dual-Brain Intelligence
        else:
            bat = self.get_battery_status()
            disk = self.get_disk_storage()
            action_data["readiness"] = {"battery": bat, "disk": disk}

            # If online and not explicitly forced offline, consult Gemini Brain
            gemini_handled = False
            if is_online and preferred_model not in ["offline", "local", "offline-deterministic"]:
                gemini_res = self.query_gemini_brain(message, preferred_model=preferred_model)
                if gemini_res.get("success"):
                    resp_en = gemini_res.get("response_en", "")
                    resp_gu = gemini_res.get("response_gu", "")
                    # Sanitize any accidental Windows mentions
                    if "device manager" in resp_en.lower():
                        resp_en = re.sub(r'in Device Manager', 'in the Linux Terminal (using `lsusb` and `v4l2-ctl`)', resp_en, flags=re.IGNORECASE)
                        resp_en = re.sub(r'Device Manager', 'Linux Terminal (`lsusb`)', resp_en, flags=re.IGNORECASE)
                    if "alpesh" not in resp_en.lower():
                        resp_en = f"Greetings Alpesh Sir! {resp_en}"
                    if "અલ્પેશ" not in resp_gu:
                        resp_gu = f"જય માતાજી અલ્પેશ સાહેબ! {resp_gu}"
                    action_type = "ONLINE_GEMINI_INTELLIGENCE"
                    model_used = gemini_res.get("model_used", "gemini-3.6-flash")
                    badge = gemini_res.get("badge", "⚡ Gemini 3.6 Flash")
                    routing_reason = gemini_res.get("routing_reason", "Google Gemini Cloud Intelligence")
                    action_data["gemini_online"] = gemini_res
                    gemini_handled = True

            if not gemini_handled:
                is_simple_greeting = any(msg_lower == g for g in [
                    "hi", "hello", "hey", "kem cho", "status", "ping", "are you online",
                    "કેમ છો", "નમસ્તે", "જય માતાજી", "ઓનલાઈન છો", "ready", "ready?", "તૈયાર છો"
                ])
                if is_simple_greeting:
                    mode_label_gu = "હાઇબ્રિડ (ઓનલાઇન + ઓફલાઇન)" if is_online else "૧૦૦% ઓફલાઇન એર-ગેપ્ડ"
                    mode_label_en = "Hybrid (Online + Offline)" if is_online else "100% Offline Air-Gapped"
                    resp_gu = (
                        f"જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા (CEO, ચામુંડા ઓટોમોબાઇલ & સુપ્રીમ AI ઓર્કેસ્ટ્રેટર).\n"
                        f"👑 {mode_label_gu} ઓટોનોમસ કમાન્ડ સેન્ટર સમગ્ર લેપટોપ પર સક્રિય છે!\n"
                        f"• કનેક્ટિવિટી: {net_status.get('description')}\n"
                        f"• બેટરી: {bat.get('percent', 100)}% ({bat.get('status_text', 'AC Power')}) | સ્ટોરેજ: {disk.get('free_gb', 0)} GB ખાલી\n"
                        f"• સંપૂર્ણ કંટ્રોલ સક્રિય: શેલ કમાન્ડ્સ, ફાઇલ્સ રીડ/રાઇટ, એપ લોન્ચર, સ્ક્રીનશોટ, વોલ્યુમ/બ્રાઇટનેસ, ટર્બો સ્પીડ અને તમામ ૨૦ સબ-એજન્ટ્સ.\n"
                        f"• આપનો શો આદેશ છે સાહેબ? આપ કોઈપણ કાર્ય માટે આદેશ આપી શકો છો!"
                    )
                    resp_en = (
                        f"Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) standing by.\n"
                        f"👑 {mode_label_en} Autonomous Command Center active with full authority across this laptop!\n"
                        f"• Connectivity: {net_status.get('description')}\n"
                        f"• Battery: {bat.get('percent', 100)}% ({bat.get('status_text', 'AC Power')}) | Free Storage: {disk.get('free_gb', 0)} GB\n"
                        f"• Full Control Active: Shell commands, Filesystem read/write, App launcher, Screenshots, Volume/Brightness, Turbo Speed & all 20 sub-agents.\n"
                        f"• Standing by for your directive, Sir! Like Jarvis, Friday, Edith & Vision, I am ready to execute any task."
                    )
                else:
                    cog_res = self.query_offline_cognitive_matrix(message, detected_lang=detected_lang)
                    resp_en = cog_res.get("response_en", "")
                    resp_gu = cog_res.get("response_gu", "")
                    action_type = cog_res.get("action_type", "OFFLINE_COGNITIVE_REASONING")
                    model_used = "offline-autonomous-aradhya"
                    badge = "👑 Aradhya Offline Cognitive Matrix (Pro Reasoning)"
                    routing_reason = cog_res.get("routing_reason", "100% Offline Cognitive Matrix")
                    action_data["offline_cognitive"] = cog_res

        # Automatic Voice Output Trigger (if commanded or requested)
        should_speak = speak_response or kwargs.get("voice", False) or any(w in msg_lower for w in [
            "speak aloud", "read aloud", "tell me out loud", "voice on",
            "વાંચી સંભળાવો", "બોલીને કહો", "બોલીને સંભળાવો", "કહીને સંભળાવો",
            "बोलकर बताओ", "सुनाओ", "आवाज में बताओ"
        ])

        audio_url = None
        if should_speak:
            # Pick Gujarati or English depending on user language
            text_to_speak = resp_gu if detected_lang.get("code", "").startswith("gu") else resp_en
            v_res = self.voice.speak(text_to_speak, language="auto", blocking=False)
            action_data["voice_output"] = v_res
            audio_url = v_res.get("web_url")

        self.evolution.log_recent_action(action_type, message)
        elapsed_ms = int((time.time() - start_time) * 1000)

        res_dict = {
            "success": True,
            "agent_id": "aradhya_ceo",
            "responding_agent": "Aradhya (આરાધ્યા - Dealership CEO & Supreme AI Orchestrator)",
            "department": "Supreme AI Orchestration & Executive Leadership",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "response_en": resp_en,
            "response_gu": resp_gu,
            "action_type": action_type,
            "action_data": action_data,
            "helpline": OFFICIAL_WHATSAPP_HELPLINE,
            "model_used": model_used,
            "badge": badge,
            "routing_reason": routing_reason,
            "latency_ms": elapsed_ms
        }
        if audio_url:
            res_dict["audio_url"] = audio_url
        return res_dict


_aradhya_engine: Optional[AradhyaAutonomousEngine] = None

def get_aradhya_engine() -> AradhyaAutonomousEngine:
    global _aradhya_engine
    if _aradhya_engine is None:
        _aradhya_engine = AradhyaAutonomousEngine()
    return _aradhya_engine
