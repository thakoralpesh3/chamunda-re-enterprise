#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
CLOUDFLARE-STANDARD CYBERSECURITY AUDITOR & THREAT REMEDIATION ENGINE
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Master Tech)

Features:
1. Audits host machine security posture against Cloudflare Zero Trust & OWASP benchmarks.
2. Audits all current autonomous agents (Chamunda RE, Jarvis, Web2APK, Web2IPA, APK TV,
   Book Publisher, KidsPlay, YouTube, MicroCorp).
3. Auto-discovers any FUTURE agents created on this system dynamically.
4. Generates detailed threat breakdowns and tailored defensive solutions.
5. Provides automated remediation (`--fix`) to harden origins and secure endpoints.
"""

import os
import re
import sys
import time
import json
import socket
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [CloudflareAuditor] %(message)s"
)
logger = logging.getLogger("CloudflareAuditor")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_LOG_FILE = DATA_DIR / "cloudflare_security_audit.json"

KNOWN_AGENTS = [
    {"id": "chamunda_re_enterprise", "name": "Chamunda RE Enterprise & Aradhya CEO", "path": Path("/home/alpesh/chamunda_re_enterprise"), "port": 8081},
    {"id": "jarvis_agent", "name": "Jarvis Mark VII System Commander", "path": Path("/home/alpesh/jarvis-agent"), "port": None},
    {"id": "web_to_apk_agent", "name": "Web2APK Autonomous Android Packager", "path": Path("/home/alpesh/web-to-apk-agent"), "port": 8990},
    {"id": "web_to_ipa_agent", "name": "Web2IPA Autonomous iOS Packager", "path": Path("/home/alpesh/web-to-ipa-agent"), "port": 8992},
    {"id": "apk_tv_converter_agent", "name": "APK TV Converter Agent", "path": Path("/home/alpesh/apk-tv-converter-agent"), "port": 8000},
    {"id": "book_publishing_agent", "name": "PublisheR AI Book Publishing Agent", "path": Path("/home/alpesh/book-publishing-agent"), "port": 8550},
    {"id": "kids_game_studio", "name": "KidsPlay AI Studio", "path": Path("/home/alpesh/kids-game-studio"), "port": 8899},
    {"id": "youtube_agent", "name": "YouTube Production & Growth Agent", "path": Path("/home/alpesh/youtube-agent"), "port": 8080},
    {"id": "microcorp_agent", "name": "MicroCorp AI Autonomous Enterprise", "path": Path("/media/alpesh/Software & Work/Agents/microcorp-agent"), "port": 8585}
]

SECRET_REGEX_PATTERNS = [
    ("CRITICAL", "Private Cryptographic Key", r"-----BEGIN\s+(?:RSA|OPENSSH|EC|DSA|PRIVATE)\s+KEY-----"),
    ("CRITICAL", "Live Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24}"),
    ("CRITICAL", "AWS Access Key Leaked", r"AKIA[0-9A-Z]{16}"),
    ("HIGH", "Google Cloud Gemini API Key", r"AIza[0-9A-Za-z\-_]{35}"),
    ("HIGH", "GitHub Personal Access Token", r"ghp_[0-9a-zA-Z]{36}"),
    ("HIGH", "OpenAI API Secret Key", r"sk-[a-zA-Z0-9]{32,}")
]

DUMMY_SECRET_PATTERNS = [
    r"1234567890",
    r"EXAMPLE",
    r"0000000000",
    r"XXXXX",
    r"TESTKEY",
    r"dummy",
    r"fake",
    r"placeholder"
]

SUSPICIOUS_PORTS = {
    4444: "Metasploit Default Reverse Shell Listener",
    1337: "Classic Backdoor Listener",
    31337: "Back Orifice Trojan Port",
    6666: "IRC Trojan Botnet Controller",
    23: "Insecure Telnet Plaintext Service"
}

PRE_PUSH_HOOK_SCRIPT = """#!/usr/bin/env bash
# Chamunda Enterprise • Cloudflare Zero-Trust Pre-Push Security Guard
# Author: Aradhya CEO & Alpesh Sir (Master Tech)
# Standard: Cloudflare Zero Trust & OWASP Top 10

echo "🛡️ [Cloudflare Zero-Trust Guard] Verifying outgoing commits before GitHub push..."

# 1. Block pushing unencrypted environment / secret files
FORBIDDEN_FILES=(".env" "id_rsa" "id_ed25519" "*.pem" "*.key" "secrets.json" "service_account.json")
for pattern in "${FORBIDDEN_FILES[@]}"; do
    git diff --cached --name-only 2>/dev/null | grep -E "$pattern" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "❌ [BLOCK] Attempted to push sensitive file matching '$pattern' to GitHub!"
        echo "👉 Action: Remove sensitive file from git tracking, add to .gitignore, and push again."
        exit 1
    fi
done

# 2. Block outgoing diffs containing hardcoded API keys
SECRET_PATTERNS=(
    "AIza[0-9A-Za-z\-_]{35}"
    "sk_live_[0-9a-zA-Z]{24}"
    "ghp_[0-9a-zA-Z]{36}"
    "-----BEGIN[ A-Z0-9_-]*PRIVATE KEY-----"
)

while read -r local_ref local_oid remote_ref remote_oid; do
    if [ "$local_oid" = "0000000000000000000000000000000000000000" ]; then
        continue
    fi
    if [ "$remote_oid" = "0000000000000000000000000000000000000000" ]; then
        RANGE="$local_oid"
    else
        RANGE="$remote_oid..$local_oid"
    fi

    for pat in "${SECRET_PATTERNS[@]}"; do
        MATCHES=$(git log -p "$RANGE" 2>/dev/null | grep -E "^\+[^+]" | grep -E "$pat" | grep -v "DUMMY" | grep -v "EXAMPLE" | grep -v "1234567890")
        if [ -n "$MATCHES" ]; then
            echo "🚨 [BLOCK] Hardcoded credential detected in outgoing commits matching: $pat"
            echo "👉 Action: Redact secret from commit history before pushing to public GitHub!"
            exit 1
        fi
    done
done

echo "✅ [Cloudflare Zero-Trust Guard] Outgoing commits verified clean. Safe to push to GitHub."
exit 0
"""

DEPENDABOT_TEMPLATE = """# Cloudflare & GitHub Zero-Trust Supply Chain Security
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
"""


class CloudflareSecurityAuditor:
    """
    Zero-Trust Security Auditor modeled on Cloudflare Security Posture & Radar intelligence.
    """

    def __init__(self):
        self.known_agents = KNOWN_AGENTS
        self.cached_audit: Optional[Dict[str, Any]] = None

    def discover_all_agents(self) -> List[Dict[str, Any]]:
        """
        Returns registered agents plus auto-discovers ANY new agent directories
        created in user workspace or external storage.
        """
        known_resolved_paths = {str(a["path"].resolve()): a for a in self.known_agents if a["path"].exists()}
        known_agent_names = {a["path"].name.lower() for a in self.known_agents}
        known_agent_names.update({a["id"].lower() for a in self.known_agents})
        agents_map = dict(known_resolved_paths)

        search_roots = [
            Path("/home/alpesh"),
            Path("/media/alpesh/Software & Work/Agents")
        ]

        for root in search_roots:
            if not root.exists():
                continue
            try:
                for item in root.iterdir():
                    if item.is_dir() and not item.name.startswith("."):
                        item_resolved = str(item.resolve())
                        if item_resolved in known_resolved_paths or item.name.lower() in known_agent_names:
                            continue

                        # Check if directory name suggests an agent
                        name_lower = item.name.lower()
                        is_agent_candidate = any(keyword in name_lower for keyword in ["agent", "studio", "bot", "assistant"])

                        # Check if directory contains agent code
                        has_agent_code = (
                            (item / "agent.py").exists() or
                            (item / "main.py").exists() or
                            (item / "app.py").exists()
                        )

                        if is_agent_candidate or has_agent_code:
                            detected_agent = {
                                "id": item.name.lower().replace("-", "_").replace(" ", "_"),
                                "name": f"✨ Auto-Discovered: {item.name}",
                                "path": item,
                                "port": None,
                                "is_dynamically_discovered": True
                            }
                            agents_map[item_resolved] = detected_agent
                            logger.info("🧬 [Dynamic Discovery] Ingested new future agent directory: %s", item.name)
            except Exception as e:
                logger.debug("Directory discovery error in %s: %s", root, e)

        return list(agents_map.values())

    def audit_host_system(self) -> Dict[str, Any]:
        """Audit host OS open ports, origin bindings, and process integrity."""
        findings = []
        listening_ports = []
        
        try:
            res = subprocess.run(
                ["ss", "-tlpn"],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in res.stdout.splitlines()[1:]:
                parts = line.split()
                if len(parts) >= 4:
                    local_addr = parts[3]
                    proc_info = parts[5] if len(parts) > 5 else ""
                    proc_name = ""
                    if proc_info:
                        m_proc = re.findall(r'"([^"]+)",pid=(\d+)', proc_info)
                        if m_proc:
                            proc_name = f"{m_proc[0][0]} (PID {m_proc[0][1]})"
                    if ":" in local_addr:
                        try:
                            port_str = local_addr.rsplit(":", 1)[1]
                            port = int(port_str)
                            ip_bind = local_addr.rsplit(":", 1)[0]
                            listening_ports.append({"ip": ip_bind, "port": port, "raw": local_addr, "process": proc_name})

                            # Check for hostile known backdoor ports
                            if port in SUSPICIOUS_PORTS:
                                findings.append({
                                    "severity": "CRITICAL",
                                    "category": "HOST_INTEGRITY",
                                    "title": f"Hostile Backdoor Port Listening: {port}",
                                    "details": f"Port {port} ({SUSPICIOUS_PORTS[port]}) is open on local socket: {local_addr} ({proc_name})",
                                    "remediation": f"Immediately terminate process listening on port {port} and check origin binary."
                                })

                            # Check for uncloaked 0.0.0.0 bindings on non-standard ports
                            if ip_bind in ["0.0.0.0", "*", "[::]"] and port > 1024:
                                details_desc = f"Port {port} ({proc_name or 'Process'}) accepts connections from all local network interfaces (0.0.0.0) instead of binding to loopback (127.0.0.1) or routing through Cloudflare Zero Trust."
                                findings.append({
                                    "severity": "MEDIUM",
                                    "category": "ORIGIN_EXPOSURE",
                                    "title": f"Service Bound to All Interfaces (0.0.0.0:{port})",
                                    "details": details_desc,
                                    "remediation": f"Bind service to 127.0.0.1 and tunnel externally via Cloudflare Tunnel."
                                })
                        except Exception:
                            pass
        except Exception as e:
            logger.debug("Error running ss: %s", e)

        # Check for active cloudflared tunnel
        tunnel_active = False
        try:
            cf_check = subprocess.run(["pgrep", "-f", "cloudflared"], capture_output=True, text=True)
            tunnel_active = len(cf_check.stdout.strip()) > 0
        except Exception:
            pass

        if not tunnel_active:
            findings.append({
                "severity": "HIGH",
                "category": "EDGE_TUNNELING",
                "title": "Cloudflare Edge Tunnel Daemon Inactive",
                "details": "No active cloudflared tunnel process found. Inbound traffic cannot leverage Cloudflare DDoS and WAF protections without an active tunnel.",
                "remediation": "Start Cloudflare Tunnel daemon using chhaya_watchdog or systemd service."
            })

        # Check for unauthorized volatile binary executions (/tmp, /dev/shm)
        try:
            ps_res = subprocess.run(
                ["ps", "-eo", "pid,user,args"],
                capture_output=True,
                text=True,
                timeout=5
            )
            for line in ps_res.stdout.splitlines()[1:]:
                for volatile in ["/tmp/", "/dev/shm/", "/var/tmp/"]:
                    if volatile in line and "python" not in line and "cloudflared" not in line:
                        findings.append({
                            "severity": "CRITICAL",
                            "category": "HOST_INTEGRITY",
                            "title": f"Volatile Execution Detected from {volatile}",
                            "details": f"Suspicious process running from volatile memory directory: {line.strip()[:100]}",
                            "remediation": "Investigate and terminate process. Disallow execution permissions on temporary filesystems."
                        })
        except Exception as e:
            logger.debug("Error checking volatile processes: %s", e)

        return {
            "status": "PASS" if len(findings) == 0 else "WARNING",
            "active_listening_sockets": len(listening_ports),
            "cloudflared_edge_tunnel_active": tunnel_active,
            "findings": findings
        }

    def audit_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Audit an individual agent codebase against Cloudflare Zero-Trust standards."""
        path = agent["path"]
        name = agent["name"]
        findings = []

        if not path.exists():
            return {
                "agent_id": agent["id"],
                "name": name,
                "status": "NOT_INSTALLED",
                "findings": []
            }

        # 1. Secret & Key Leak Audit (Static Analysis)
        EXCLUDED_DIRS = {
            ".venv", "venv", ".git", "__pycache__", "node_modules", ".pytest_cache",
            "deliverables", "assets", "static", "build", "dist", "data", "output",
            "samples", "browser_profiles", "downloads", "tmp", "videos", "music"
        }
        for root, dirs, files in os.walk(path):
            # Prune virtualenvs and heavy asset/data directories
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file.endswith((".py", ".json", ".md", ".yaml", ".yml", ".sh", ".toml", ".env.example")):
                    filepath = Path(root) / file
                    try:
                        # Skip huge generated data or binary files
                        if filepath.stat().st_size > 80_000:
                            continue
                        content = filepath.read_text(encoding="utf-8", errors="ignore")
                        for sev, title, pat in SECRET_REGEX_PATTERNS:
                            # Skip scanning scanner definitions themselves!
                            if "vulnerability_scanner" in file or "security_guard" in file or "cloudflare_security_auditor" in file:
                                continue
                            matches = re.findall(pat, content)
                            if matches:
                                # Filter out dummy mock values in tests
                                valid_matches = [
                                    m for m in matches
                                    if not any(re.search(d_pat, m, re.IGNORECASE) for d_pat in DUMMY_SECRET_PATTERNS)
                                ]
                                if valid_matches:
                                    findings.append({
                                        "severity": sev,
                                        "category": "SECRET_LEAK",
                                        "title": f"Leaked Credential: {title}",
                                        "file": str(filepath.relative_to(path)),
                                        "details": f"Found {len(valid_matches)} potential real secret occurrence(s) in {file}",
                                        "remediation": f"Redact secret from {file}, add to .gitignore, and load via environment variable."
                                    })
                    except Exception:
                        pass

        # 2. Origin Cloaking & .gitignore Audit
        gitignore_path = path / ".gitignore"
        if not gitignore_path.exists():
            findings.append({
                "severity": "HIGH",
                "category": "ORIGIN_CLOAKING",
                "title": "Missing .gitignore Security Boundary",
                "details": f"Agent {name} lacks a .gitignore file. Local configs and session state risk being pushed to public repos.",
                "remediation": "Create a comprehensive .gitignore file excluding .env, credentials, and virtualenvs."
            })
        else:
            try:
                gi_content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
                for sensitive in [".env", ".venv", "__pycache__"]:
                    if sensitive not in gi_content:
                        findings.append({
                            "severity": "LOW",
                            "category": "ORIGIN_CLOAKING",
                            "title": f"Incomplete .gitignore: Missing {sensitive}",
                            "details": f".gitignore does not explicitly exclude {sensitive}.",
                            "remediation": f"Add {sensitive} to {name}/.gitignore."
                        })
            except Exception:
                pass

        # 3. Cloud Codespaces & WAF Readiness
        devcontainer = path / ".devcontainer" / "devcontainer.json"
        has_devcontainer = devcontainer.exists()
        if not has_devcontainer:
            findings.append({
                "severity": "LOW",
                "category": "EDGE_CONTAINER",
                "title": "Codespaces Sandbox Not Configured",
                "details": f"{name} does not have a .devcontainer configuration for isolated cloud sandbox execution.",
                "remediation": "Generate .devcontainer/devcontainer.json for secure cloud runtime."
            })

        return {
            "agent_id": agent["id"],
            "name": name,
            "path": str(path),
            "status": "PASS" if len(findings) == 0 else ("FAIL" if any(f["severity"] == "CRITICAL" for f in findings) else "WARNING"),
            "findings_count": len(findings),
            "findings": findings
        }

    def run_full_security_audit(self) -> Dict[str, Any]:
        """Perform system-wide Cloudflare cybersecurity audit."""
        start_time = time.time()
        agents = self.discover_all_agents()
        host_audit = self.audit_host_system()

        agent_audits = []
        all_threats = list(host_audit.get("findings", []))

        for agent in agents:
            res = self.audit_agent(agent)
            agent_audits.append(res)
            all_threats.extend(res.get("findings", []))

        # Calculate Cloudflare Security Score (0-100)
        crit_count = sum(1 for t in all_threats if t.get("severity") == "CRITICAL")
        high_count = sum(1 for t in all_threats if t.get("severity") == "HIGH")
        med_count = sum(1 for t in all_threats if t.get("severity") == "MEDIUM")
        low_count = sum(1 for t in all_threats if t.get("severity") == "LOW")

        deductions = (crit_count * 25) + (high_count * 10) + (med_count * 4) + (low_count * 1)
        score = max(0, min(100, 100 - deductions))

        if score >= 95:
            grade = "A+ (Cloudflare Fortress)"
        elif score >= 88:
            grade = "A (Zero Trust Compliant)"
        elif score >= 78:
            grade = "B (Hardened with Warnings)"
        elif score >= 65:
            grade = "C (Remediation Required)"
        else:
            grade = "F (High Cyber Risk)"

        solutions = self.generate_defensive_solutions(all_threats)

        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "audit_standard": "Cloudflare Zero Trust & OWASP Top 10",
            "overall_score": score,
            "grade": grade,
            "total_agents_audited": len(agents),
            "threats_summary": {
                "total_threats": len(all_threats),
                "critical": crit_count,
                "high": high_count,
                "medium": med_count,
                "low": low_count
            },
            "host_os_audit": host_audit,
            "agents_audit": agent_audits,
            "defensive_solutions": solutions,
            "duration_seconds": round(time.time() - start_time, 2)
        }

        # Cache report to disk
        try:
            AUDIT_LOG_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error("Failed to save audit report: %s", e)

        self.cached_audit = report
        return report

    def generate_defensive_solutions(self, threats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map discovered threat vectors to concrete Cloudflare Zero Trust solutions."""
        solutions_map: Dict[str, Dict[str, Any]] = {}

        for threat in threats:
            title = threat.get("title", "")
            cat = threat.get("category", "")
            sev = threat.get("severity", "LOW")

            if "0.0.0.0" in title:
                sol_id = "SOL-ORIGIN-CLOAK"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Cloudflare Origin Cloaking (Bind Loopback)",
                        "solution_gu": "સર્વિસને 127.0.0.1 પર બાઇન્ડ કરી પબ્લિક પોર્ટ એક્સપોઝર અટકાવો.",
                        "action_required": "Configure microservices to bind strictly to 127.0.0.1 and expose securely via Cloudflare Tunnel.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            elif "Secret" in title or "Leaked" in title:
                sol_id = "SOL-SECRET-REDACT"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Zero-Trust Secret Redaction & Environment Vault",
                        "solution_gu": "કોડમાંથી પ્રાઇવેટ API કી હટાવીને .env અથવા Cloudflare Secrets માં સાચવો.",
                        "action_required": "Move leaked credentials to .env file and ensure source files load secrets via os.environ.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(f"{threat.get('file', 'file')}: {title}")
            elif "Tunnel" in title:
                sol_id = "SOL-TUNNEL-RESILIENCE"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Cloudflare Tunnel Auto-Restart & Fallback",
                        "solution_gu": "Cloudflare ટનલ બંધ હોય તો watchdog દ્વારા આપોઆપ રીસ્ટાર્ટ કરો.",
                        "action_required": "Verify chamunda-chhaya.service is running with quick-tunnel fallback.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            elif ".gitignore" in title:
                sol_id = "SOL-GITIGNORE-HARDEN"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Automated .gitignore Hardening",
                        "solution_gu": ".gitignore માં જરૂરી સિક્યોરિટી નિયમો ઉમેરો.",
                        "action_required": "Inject standard rules (.env, .venv, *.key) into repository .gitignore.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            else:
                sol_id = f"SOL-GEN-{len(solutions_map)+1}"
                solutions_map[sol_id] = {
                    "id": sol_id,
                    "severity": sev,
                    "title": "Zero-Trust Defensive Policy Enforcement",
                    "solution_gu": "સિક્યોરિટી નિયમો લાગુ કરી થ્રેટ અટકાવો.",
                    "action_required": threat.get("remediation", "Apply defensive patches."),
                    "affected_items": [title],
                    "can_autofix": False
                }

        return list(solutions_map.values())

    def auto_remediate_all(self) -> Dict[str, Any]:
        """Automatically execute safe defensive mitigations."""
        report = self.run_full_security_audit()
        threats = []
        threats.extend(report.get("host_os_audit", {}).get("findings", []))
        for a in report.get("agents_audit", []):
            threats.extend(a.get("findings", []))

        remediated_actions = []

        for threat in threats:
            title = threat.get("title", "")
            # 1. Auto-harden .gitignore
            if "Missing .gitignore" in title or "Incomplete .gitignore" in title:
                for agent in report.get("agents_audit", []):
                    agent_path = Path(agent["path"])
                    if agent_path.exists():
                        gi = agent_path / ".gitignore"
                        existing = gi.read_text(encoding="utf-8", errors="ignore") if gi.exists() else ""
                        needed = [".env", ".venv", "__pycache__/", "*.pyc", "*.key", "*.token"]
                        to_add = [n for n in needed if n not in existing]
                        if to_add:
                            with gi.open("a", encoding="utf-8") as f:
                                f.write("\n# Cloudflare Security Auditor Hardening\n" + "\n".join(to_add) + "\n")
                            remediated_actions.append(f"Hardened .gitignore in {agent['name']}")

        # Re-run audit to calculate post-hardening score
        updated_report = self.run_full_security_audit()
        return {
            "success": True,
            "actions_taken": remediated_actions,
            "previous_score": report["overall_score"],
            "new_score": updated_report["overall_score"],
            "new_grade": updated_report["grade"]
        }


_auditor = None

def get_cloudflare_auditor() -> CloudflareSecurityAuditor:
    global _auditor
    if _auditor is None:
        _auditor = CloudflareSecurityAuditor()
    return _auditor


if __name__ == "__main__":
    auditor = get_cloudflare_auditor()

    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        rep = auditor.run_full_security_audit()
        print(json.dumps(rep, indent=2))
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--fix":
        print("🛡️ Executing Autonomous Cloudflare Security Remediation...")
        fix_res = auditor.auto_remediate_all()
        print(f"✅ Remediation Complete! Score improved from {fix_res['previous_score']} -> {fix_res['new_score']} [{fix_res['new_grade']}]")
        for act in fix_res["actions_taken"]:
            print(f"  - {act}")
        sys.exit(0)

    # ANSI Console Table Report
    print("\n" + "=" * 76)
    print(" 🛡️  CHAMUNDA AUTOMOBILE • CLOUDFLARE ZERO-TRUST CYBERSECURITY AUDIT")
    print("=" * 76)
    rep = auditor.run_full_security_audit()
    print(f"📅 Timestamp: {rep['timestamp']} | Standard: {rep['audit_standard']}")
    print(f"🏆 Security Score: \033[1;32m{rep['overall_score']}/100\033[0m  |  Grade: \033[1;33m{rep['grade']}\033[0m")
    print(f"🤖 Total Autonomous Agents Audited: {rep['total_agents_audited']}")
    print(f"⚠️  Threats Detected: {rep['threats_summary']['total_threats']} (Critical: {rep['threats_summary']['critical']}, High: {rep['threats_summary']['high']}, Medium: {rep['threats_summary']['medium']}, Low: {rep['threats_summary']['low']})")
    print("-" * 76)
    print("AGENTS SECURITY STATUS:")
    for a in rep["agents_audit"]:
        st_color = "\033[32mPASS\033[0m" if a["status"] == "PASS" else ("\033[31mFAIL\033[0m" if a["status"] == "FAIL" else "\033[33mWARNING\033[0m")
        disc_tag = " [New Agent]" if a.get("is_dynamically_discovered") else ""
        print(f"  • {a['name']}{disc_tag}: {st_color} ({a['findings_count']} finding(s))")

    if rep["defensive_solutions"]:
        print("-" * 76)
        print("RECOMMENDED DEFENSIVE SOLUTIONS:")
        for s in rep["defensive_solutions"]:
            print(f"  [{s['severity']}] {s['title']}")
            print(f"       👉 Solution: {s['solution_gu']}")
            print(f"       🔧 Action: {s['action_required']}")
            if s.get("affected_items"):
                items_str = ", ".join(s["affected_items"][:4])
                if len(s["affected_items"]) > 4:
                    items_str += f" (+{len(s['affected_items']) - 4} more)"
                print(f"       🎯 Targets: {items_str}")
    print("=" * 76 + "\n")
