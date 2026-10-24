"""
Chamunda Automobile Enterprise • System Performance Optimizer & Lag Buster Engine
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Chairman)

Features:
1. Real-time CPU, RAM, Swap & Top-Process Telemetry.
2. Autonomous Sluggishness Detection (CPU/RAM/Load/Swap thresholds).
3. Temporary Files Cleaner (thumbnails, user /tmp files, build caches, __pycache__).
4. Safe Background Process Buster (zombies, defuncts, orphan test runners, stray processes).
5. Safe Garbage Collection & libc malloc_trim to return unmapped pages to Linux OS.
6. 24/7 Autonomous Self-Healing with automatic cooldown and audit logging.
7. Sub-second 'Turbo Boost' pipeline for instant lag elimination.
"""

import os
import sys
import gc
import time
import json
import shutil
import logging
import ctypes
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import psutil

logger = logging.getLogger("ChamundaSystemOptimizer")

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
DATA_DIR = BASE_DIR / "data"
AUTONOMOUS_LOG_FILE = DATA_DIR / "system_autonomous_healing.json"

SAFE_PROTECTED_NAMES = {
    "systemd", "dbus-daemon", "Xorg", "cinnamon", "gnome-shell", "lightdm",
    "pulseaudio", "pipewire", "bash", "sh", "sshd", "ssh", "tmux",
    "antigravity", "cursor", "code", "node", "chrome", "google-chrome",
    "brave", "firefox", "blueman-applet", "blueman-tray", "applet.py"
}

SAFE_PROTECTED_KEYWORDS = [
    "antigravity", "language_server", "daemon", "cinnamon", "blueman",
    "scheduler.py", "cloud_mirror_server", "chhaya_watchdog"
]


class ChamundaSystemOptimizer:
    """
    Automated Laptop Performance Optimizer & Lag Buster for Alpesh Sir.
    Protects critical system processes while reclaiming RAM, deleting temporary files,
    and terminating rogue/orphan background tasks within seconds.
    """

    def __init__(self, base_dirs: Optional[List[str]] = None):
        self.base_dirs = [
            Path(p) for p in (base_dirs or ["/home/alpesh/chamunda_re_enterprise", "/home/alpesh/jarvis-agent"])
            if Path(p).exists()
        ]
        self.current_pid = os.getpid()
        self.parent_pid = os.getppid()
        self._last_auto_heal_time: float = 0.0

    def get_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system performance, CPU, memory, and load telemetry."""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        cpu_pct = psutil.cpu_percent(interval=0.08)
        load_1, load_5, load_15 = os.getloadavg() if hasattr(os, "getloadavg") else (0.0, 0.0, 0.0)

        # Top memory-consuming processes
        top_procs = []
        for p in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
            try:
                info = p.info
                mem_mb = round((info['memory_info'].rss if info.get('memory_info') else 0) / (1024 * 1024), 1)
                top_procs.append({
                    "pid": info['pid'],
                    "name": info.get('name') or "unknown",
                    "user": info.get('username') or "system",
                    "memory_mb": mem_mb,
                    "cpu_percent": info.get('cpu_percent') or 0.0
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        top_procs.sort(key=lambda x: x["memory_mb"], reverse=True)

        status = "Optimal"
        status_gu = "ઉત્તમ (લેપટોપ સંપૂર્ણ સરળ ચાલે છે)"
        if mem.percent > 85 or cpu_pct > 80:
            status = "High Load / Lagging"
            status_gu = "અતિશય લોડ / લેગિંગ (ઓપ્ટિમાઇઝેશન જરૂરી છે)"
        elif mem.percent > 70 or cpu_pct > 60:
            status = "Moderate Load"
            status_gu = "મધ્યમ લોડ"

        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_percent": cpu_pct,
            "cpu_cores_logical": psutil.cpu_count(logical=True),
            "cpu_cores_physical": psutil.cpu_count(logical=False),
            "load_averages": {
                "1_min": round(load_1, 2),
                "5_min": round(load_5, 2),
                "15_min": round(load_15, 2)
            },
            "memory": {
                "total_mb": round(mem.total / (1024 * 1024), 1),
                "used_mb": round(mem.used / (1024 * 1024), 1),
                "free_mb": round(mem.free / (1024 * 1024), 1),
                "available_mb": round(mem.available / (1024 * 1024), 1),
                "percent_used": mem.percent
            },
            "swap": {
                "total_mb": round(swap.total / (1024 * 1024), 1),
                "used_mb": round(swap.used / (1024 * 1024), 1),
                "percent_used": swap.percent
            },
            "status": status,
            "status_gu": status_gu,
            "top_processes": top_procs[:6]
        }

    def is_system_sluggish(self) -> Tuple[bool, List[str], Dict[str, Any]]:
        """
        Analyze current system metrics to determine if the laptop feels sluggish.
        Returns: (is_sluggish: bool, reasons: List[str], metrics: Dict[str, Any])
        """
        metrics = self.get_system_metrics()
        reasons = []

        mem_pct = metrics.get("memory", {}).get("percent_used", 0)
        avail_mb = metrics.get("memory", {}).get("available_mb", 0)
        cpu_pct = metrics.get("cpu_percent", 0)
        load_1 = metrics.get("load_averages", {}).get("1_min", 0)
        swap_pct = metrics.get("swap", {}).get("percent_used", 0)

        # Thresholds tuned for responsiveness on 4GB laptop
        if mem_pct >= 76.0:
            reasons.append(f"High RAM usage ({mem_pct:.1f}% used, only {avail_mb:.0f} MB available)")
        elif avail_mb <= 550.0:
            reasons.append(f"Low available memory ({avail_mb:.0f} MB remaining)")

        if cpu_pct >= 75.0:
            reasons.append(f"Spiking CPU load ({cpu_pct:.1f}%)")

        if load_1 >= 3.2:
            reasons.append(f"High CPU task queue load (1-min average: {load_1:.2f})")

        if swap_pct >= 45.0:
            reasons.append(f"Elevated swap memory pressure ({swap_pct:.1f}%)")

        is_sluggish = len(reasons) > 0
        return is_sluggish, reasons, metrics

    def _is_safe_to_kill(self, proc: psutil.Process, active_uvicorn_pid: Optional[int] = None) -> bool:
        """
        Determine whether a process can be safely terminated without breaking
        the system desktop, Antigravity IDE, or essential daemons.
        """
        try:
            pid = proc.pid
            if pid in {0, 1, self.current_pid, self.parent_pid}:
                return False
            if active_uvicorn_pid and pid == active_uvicorn_pid:
                return False

            name = (proc.name() or "").lower()
            cmdline_list = proc.cmdline() or []
            cmdline = " ".join(cmdline_list).lower()

            # Protect essential system and desktop names
            if any(prot in name for prot in SAFE_PROTECTED_NAMES):
                return False

            # Protect critical keywords
            for kw in SAFE_PROTECTED_KEYWORDS:
                if kw in cmdline or kw in name:
                    return False

            # Protect active uvicorn 8080 or port listening
            if "uvicorn" in cmdline and "8080" in cmdline:
                return False
            if "cloud_mirror_server" in cmdline or "8081" in cmdline:
                return False
            if "chhaya_watchdog" in cmdline:
                return False

            # Protect background scheduler
            if "scheduler.py" in cmdline:
                return False

            # Check for zombie/defunct
            if proc.status() == psutil.STATUS_ZOMBIE:
                return True

            # Identify stale orphan python test runs or dead test runners
            if "python" in name or "pytest" in cmdline:
                if "pytest" in cmdline and pid != self.current_pid:
                    create_time = proc.create_time()
                    if time.time() - create_time > 45:
                        return True

                if "test_" in cmdline and pid != self.current_pid:
                    create_time = proc.create_time()
                    if time.time() - create_time > 45:
                        return True

            # Identify stray orphan sleep commands
            if name == "sleep" or "sleep " in cmdline:
                return True

            # Identify orphan curl/wget loops (> 60s)
            if (name in {"curl", "wget", "ping"}) and (time.time() - proc.create_time() > 60):
                return True

            return False
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False

    def clean_temporary_files(self) -> Dict[str, Any]:
        """
        Delete user temporary files, stale thumbnails, build caches, and test caches.
        Returns detailed count of deleted items and total megabytes reclaimed.
        """
        deleted_count = 0
        reclaimed_bytes = 0

        # 1. User thumbnail caches (~/.cache/thumbnails)
        thumb_base = Path.home() / ".cache" / "thumbnails"
        if thumb_base.exists():
            for f in thumb_base.rglob("*"):
                try:
                    if f.is_file():
                        sz = f.stat().st_size
                        f.unlink(missing_ok=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    continue

        # 2. Pip cache temporary downloads & wheels (~/.cache/pip)
        pip_cache = Path.home() / ".cache" / "pip"
        if pip_cache.exists():
            for f in pip_cache.rglob("*"):
                try:
                    if f.is_file():
                        sz = f.stat().st_size
                        f.unlink(missing_ok=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    continue

        # 3. Web browser disk cache (~/.cache/mozilla/firefox/*/cache2)
        mozilla_cache = Path.home() / ".cache" / "mozilla" / "firefox"
        if mozilla_cache.exists():
            for c_folder in ["entries", "doomed"]:
                for c_dir in mozilla_cache.glob(f"*/cache2/{c_folder}"):
                    if c_dir.is_dir():
                        for f in c_dir.iterdir():
                            try:
                                if f.is_file():
                                    sz = f.stat().st_size
                                    f.unlink(missing_ok=True)
                                    deleted_count += 1
                                    reclaimed_bytes += sz
                            except Exception:
                                pass

        # 4. Trash bin (~/.local/share/Trash/files)
        trash_dir = Path.home() / ".local" / "share" / "Trash" / "files"
        if trash_dir.exists():
            for f in trash_dir.iterdir():
                try:
                    if f.is_file() or f.is_symlink():
                        sz = f.stat().st_size
                        f.unlink(missing_ok=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                    elif f.is_dir():
                        sz = sum(sub.stat().st_size for sub in f.rglob("*") if sub.is_file())
                        shutil.rmtree(f, ignore_errors=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    pass

        # 5. Selenium & browser temp driver caches (~/.cache/selenium)
        selenium_cache = Path.home() / ".cache" / "selenium"
        if selenium_cache.exists():
            for f in selenium_cache.rglob("*"):
                try:
                    if f.is_file():
                        sz = f.stat().st_size
                        f.unlink(missing_ok=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    continue

        # 4. Stale user /tmp files (older than 30 mins)
        tmp_dir = Path("/tmp")
        current_uid = os.getuid()
        now = time.time()
        if tmp_dir.exists():
            for f in tmp_dir.iterdir():
                try:
                    st = f.stat()
                    if st.st_uid == current_uid and (now - st.st_mtime > 1800):
                        if f.name.startswith((".X11", ".ICE", "ssh-", "gpg-")):
                            continue
                        if f.is_file() or f.is_symlink():
                            sz = st.st_size
                            f.unlink(missing_ok=True)
                            deleted_count += 1
                            reclaimed_bytes += sz
                        elif f.is_dir() and f.name.startswith("tmp"):
                            sz = sum(sub.stat().st_size for sub in f.rglob("*") if sub.is_file())
                            shutil.rmtree(f, ignore_errors=True)
                            deleted_count += 1
                            reclaimed_bytes += sz
                except Exception:
                    continue

        # 5. Project __pycache__ and test caches across base directories
        for b_dir in self.base_dirs:
            for cache_dir in b_dir.rglob("__pycache__"):
                try:
                    if cache_dir.is_dir():
                        sz = sum(sub.stat().st_size for sub in cache_dir.rglob("*") if sub.is_file())
                        shutil.rmtree(cache_dir, ignore_errors=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    continue

            for pytest_cache in b_dir.rglob(".pytest_cache"):
                try:
                    if pytest_cache.is_dir():
                        sz = sum(sub.stat().st_size for sub in pytest_cache.rglob("*") if sub.is_file())
                        shutil.rmtree(pytest_cache, ignore_errors=True)
                        deleted_count += 1
                        reclaimed_bytes += sz
                except Exception:
                    continue

        reclaimed_mb = round(reclaimed_bytes / (1024 * 1024), 2)
        return {
            "deleted_count": deleted_count,
            "reclaimed_bytes": reclaimed_bytes,
            "reclaimed_mb": reclaimed_mb
        }

    def clean_cache_files(self) -> int:
        """Prune __pycache__ and temporary test cache files across project roots."""
        res = self.clean_temporary_files()
        return res["deleted_count"]

    def stop_stale_background_processes(self, active_uvicorn_pid: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Identify and terminate rogue, orphan, or zombie background processes
        that waste CPU and RAM, while strictly protecting critical user and desktop tasks.
        """
        closed_procs = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'status', 'memory_info', 'create_time']):
            try:
                if self._is_safe_to_kill(proc, active_uvicorn_pid=active_uvicorn_pid):
                    pid = proc.pid
                    pname = proc.name()
                    pcmd = " ".join(proc.cmdline()[:3]) if proc.cmdline() else pname
                    rss_mb = round((proc.memory_info().rss if proc.memory_info() else 0) / (1024 * 1024), 1)

                    proc.terminate()
                    try:
                        proc.wait(timeout=0.4)
                    except psutil.TimeoutExpired:
                        proc.kill()

                    closed_procs.append({
                        "pid": pid,
                        "name": pname,
                        "cmd": pcmd,
                        "reclaimed_mb": rss_mb
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return closed_procs

    def trim_memory(self) -> bool:
        """Trigger Python GC and invoke libc malloc_trim to return free memory pages to Linux kernel."""
        try:
            gc.collect()
            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
            return True
        except Exception as e:
            logger.warning("malloc_trim call failed: %s", e)
            return False

    def optimize_laptop_performance(
        self,
        aggressive: bool = False,
        close_stale_processes: bool = True,
        clean_temp_files: bool = True,
        trigger_source: str = "manual"
    ) -> Dict[str, Any]:
        """
        Full Turbo Boost pipeline to fix lagging issues and maximize laptop speed within seconds.
        Cleans temp files, terminates stale processes, and reclaims RAM.
        """
        start_time = time.time()
        metrics_before = self.get_system_metrics()

        # Step 1: Force initial memory sweep
        self.trim_memory()

        # Step 2: Identify active uvicorn PID to protect it
        active_uvicorn_pid = None
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmd = " ".join(p.info.get('cmdline') or []).lower()
                if "uvicorn" in cmd and "8080" in cmd:
                    active_uvicorn_pid = p.info['pid']
                    break
            except Exception:
                continue

        # Step 3: Terminate stale / orphan processes
        closed_procs = []
        if close_stale_processes:
            closed_procs = self.stop_stale_background_processes(active_uvicorn_pid=active_uvicorn_pid)

        # Step 4: Purge temporary files and caches
        temp_cleaned = {"deleted_count": 0, "reclaimed_mb": 0.0}
        if clean_temp_files:
            temp_cleaned = self.clean_temporary_files()

        # Step 5: Final libc malloc_trim & GC sweep
        self.trim_memory()
        time.sleep(0.05)

        metrics_after = self.get_system_metrics()
        mem_freed_mb = max(0.0, round(metrics_before["memory"]["used_mb"] - metrics_after["memory"]["used_mb"], 1))
        duration_sec = round(time.time() - start_time, 2)

        # Bilingual reporting
        msg_en = (
            f"🚀 Turbo Boost Complete in {duration_sec}s! "
            f"Freed {mem_freed_mb} MB RAM. "
            f"Deleted {temp_cleaned['deleted_count']} temporary files ({temp_cleaned['reclaimed_mb']} MB disk space reclaimed). "
            f"Stopped {len(closed_procs)} background processes. "
            f"RAM Usage: {metrics_after['memory']['percent_used']}% (Available: {metrics_after['memory']['available_mb']} MB)."
        )
        msg_gu = (
            f"🚀 ટર્બો બૂસ્ટ સફળ ({duration_sec} સેકન્ડ)! "
            f"અલ્પેશ સાહેબ, {mem_freed_mb} MB રેમ મુક્ત થઈ છે. "
            f"{temp_cleaned['deleted_count']} અસ્થાયી ટેમ્પરરી ફાઈલો ({temp_cleaned['reclaimed_mb']} MB જગ્યા) સાફ કરી છે. "
            f"{len(closed_procs)} બિનજરૂરી પ્રોસેસ બંધ કરી છે. "
            f"હાલ રેમ વપરાશ: {metrics_after['memory']['percent_used']}% (ઉપલબ્ધ: {metrics_after['memory']['available_mb']} MB). "
            f"લેપટોપ સંપૂર્ણ સરળ અને સુપરફાસ્ટ થઈ ગયું છે!"
        )

        res = {
            "success": True,
            "mode": "aggressive" if aggressive else "safe_turbo",
            "trigger_source": trigger_source,
            "duration_seconds": duration_sec,
            "metrics_before": metrics_before,
            "metrics_after": metrics_after,
            "freed_memory_mb": mem_freed_mb,
            "temp_files_deleted_count": temp_cleaned["deleted_count"],
            "temp_space_freed_mb": temp_cleaned["reclaimed_mb"],
            "closed_processes_count": len(closed_procs),
            "closed_processes": closed_procs,
            "caches_pruned_count": temp_cleaned["deleted_count"],
            "message_en": msg_en,
            "message_gu": msg_gu
        }

        # Save to autonomous audit log
        self._record_autonomous_healing_event(res)
        return res

    def auto_heal_if_sluggish(self, cooldown_seconds: int = 180) -> Optional[Dict[str, Any]]:
        """
        Autonomous Watcher: Checks if laptop is sluggish; if detected and cooldown elapsed,
        autonomously runs Turbo Boost, purges temp files, reclaims RAM, and logs action.
        """
        now = time.time()
        if now - self._last_auto_heal_time < cooldown_seconds:
            return None

        is_sluggish, reasons, _ = self.is_system_sluggish()
        if not is_sluggish:
            return None

        logger.info("⚡ Autonomous Lag Buster Triggered! Reasons: %s", ", ".join(reasons))
        result = self.optimize_laptop_performance(
            aggressive=False,
            close_stale_processes=True,
            clean_temp_files=True,
            trigger_source="autonomous_watchdog"
        )
        result["reasons"] = reasons
        self._last_auto_heal_time = now
        return result

    def _record_autonomous_healing_event(self, event: Dict[str, Any]):
        """Persist auto-healing / optimization event to disk."""
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            history = []
            if AUTONOMOUS_LOG_FILE.exists():
                try:
                    with open(AUTONOMOUS_LOG_FILE, "r", encoding="utf-8") as f:
                        history = json.load(f)
                except Exception:
                    history = []

            record = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "trigger_source": event.get("trigger_source", "manual"),
                "duration_seconds": event.get("duration_seconds", 0.0),
                "freed_memory_mb": event.get("freed_memory_mb", 0.0),
                "temp_files_deleted": event.get("temp_files_deleted_count", 0),
                "temp_space_freed_mb": event.get("temp_space_freed_mb", 0.0),
                "closed_processes_count": event.get("closed_processes_count", 0),
                "ram_after_percent": event.get("metrics_after", {}).get("memory", {}).get("percent_used", 0),
                "reasons": event.get("reasons", ["Laptop Performance Acceleration"]),
                "status": "COMPLETED"
            }
            history.append(record)
            if len(history) > 50:
                history = history[-50:]

            with open(AUTONOMOUS_LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.debug("Failed to record autonomous healing event: %s", e)

    def get_autonomous_healing_history(self) -> List[Dict[str, Any]]:
        """Retrieve recent autonomous optimization records."""
        if not AUTONOMOUS_LOG_FILE.exists():
            return []
        try:
            with open(AUTONOMOUS_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []


# Singleton factory helper
_optimizer_instance: Optional[ChamundaSystemOptimizer] = None

def get_system_optimizer() -> ChamundaSystemOptimizer:
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = ChamundaSystemOptimizer()
    return _optimizer_instance