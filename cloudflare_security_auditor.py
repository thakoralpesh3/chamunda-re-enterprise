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

PRE_PUSH_HOOK_SCRIPT = r"""#!/usr/bin/env bash
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
                parts = line.strip().split(None, 2)
                if len(parts) >= 3:
                    cmd_binary = parts[2].split()[0]
                    for volatile in ["/tmp/", "/dev/shm/", "/var/tmp/"]:
                        if cmd_binary.startswith(volatile) and "python" not in cmd_binary and "cloudflared" not in cmd_binary:
                            findings.append({
                                "severity": "CRITICAL",
                                "category": "HOST_INTEGRITY",
                                "title": f"Volatile Execution Detected from {volatile}",
                                "details": f"Suspicious binary executing from volatile memory: {cmd_binary}",
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
            "samples", "browser_profiles", "downloads", "tmp", "videos", "music",
            "examples", "agency_agents", "docs", "templates"
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

    def audit_github_posture(self, agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audit GitHub Cloud Security Posture across all repositories:
        1. Pre-Push Secret Guard Hook (.git/hooks/pre-push)
        2. Git remote URL credentials / token leaks in .git/config
        3. GitHub Actions CI/CD workflow security (permissions, unpinned actions)
        4. Dependabot supply chain security configuration
        5. Public repository safeguard
        """
        findings = []
        repo_statuses = []

        for agent in agents:
            p = Path(agent["path"])
            name = agent["name"]
            git_dir = p / ".git"
            if not git_dir.exists():
                continue

            repo_findings = []

            # A. Remote URL Token Leak Check
            cfg_path = git_dir / "config"
            remote_url = ""
            if cfg_path.exists():
                try:
                    cfg_text = cfg_path.read_text(encoding="utf-8", errors="ignore")
                    for line in cfg_text.splitlines():
                        if "url =" in line:
                            remote_url = line.split("=", 1)[1].strip()
                            if "@github.com" in remote_url and ("ghp_" in remote_url or "github_pat_" in remote_url or ":" in remote_url.split("@")[0].replace("https://", "")):
                                f_item = {
                                    "severity": "CRITICAL",
                                    "category": "GITHUB_CREDENTIAL_LEAK",
                                    "title": f"Plaintext Token in Git Remote: {name}",
                                    "repo": name,
                                    "details": "Personal Access Token or password is hardcoded directly inside .git/config remote URL.",
                                    "remediation": "Sanitize .git/config URL and store GitHub token in system keychain or SSH credentials."
                                }
                                findings.append(f_item)
                                repo_findings.append(f_item)
                except Exception:
                    pass

            # B. Pre-Push Secret Guard Hook Check
            pre_push_hook = git_dir / "hooks" / "pre-push"
            has_pre_push = pre_push_hook.exists() and os.access(pre_push_hook, os.X_OK)
            if not has_pre_push:
                f_item = {
                    "severity": "HIGH",
                    "category": "GITHUB_PUSH_PROTECTION",
                    "title": f"Missing Pre-Push Secret Hook: {name}",
                    "repo": name,
                    "details": f"Repository {name} lacks an active pre-push secret blocking hook. Pushes to public GitHub can accidentally leak credentials.",
                    "remediation": "Install executable .git/hooks/pre-push script to intercept secret leaks prior to git push."
                }
                findings.append(f_item)
                repo_findings.append(f_item)

            # C. GitHub Actions Workflows Security Check
            workflows_dir = p / ".github" / "workflows"
            if workflows_dir.exists():
                for wf_file in workflows_dir.glob("*.yml"):
                    try:
                        wf_content = wf_file.read_text(encoding="utf-8", errors="ignore")
                        if "pull_request" in wf_content and "permissions:" not in wf_content:
                            f_item = {
                                "severity": "MEDIUM",
                                "category": "GITHUB_ACTIONS_HARDENING",
                                "title": f"Unrestricted GitHub Actions Permissions in {wf_file.name} ({name})",
                                "repo": name,
                                "file": str(wf_file.relative_to(p)),
                                "details": f"Workflow {wf_file.name} executes on pull_request without explicit 'permissions: contents: read' least-privilege block.",
                                "remediation": "Add 'permissions: contents: read' to restrict default write permissions for workflow GITHUB_TOKEN."
                            }
                            findings.append(f_item)
                            repo_findings.append(f_item)
                    except Exception:
                        pass

            # D. Dependabot Supply Chain Check
            dependabot_file = p / ".github" / "dependabot.yml"
            if not dependabot_file.exists():
                f_item = {
                    "severity": "LOW",
                    "category": "GITHUB_SUPPLY_CHAIN",
                    "title": f"Dependabot Not Configured: {name}",
                    "repo": name,
                    "details": f"Repository {name} does not have .github/dependabot.yml for automated dependency vulnerability patching.",
                    "remediation": "Add .github/dependabot.yml to enable weekly dependency audits."
                }
                findings.append(f_item)
                repo_findings.append(f_item)

            repo_statuses.append({
                "agent_id": agent["id"],
                "name": name,
                "remote_url": remote_url,
                "has_pre_push_hook": has_pre_push,
                "has_dependabot": dependabot_file.exists(),
                "findings_count": len(repo_findings),
                "findings": repo_findings
            })

        return {
            "status": "PASS" if len(findings) == 0 else ("FAIL" if any(f["severity"] == "CRITICAL" for f in findings) else "WARNING"),
            "total_repositories_audited": len(repo_statuses),
            "findings_count": len(findings),
            "findings": findings,
            "repositories": repo_statuses
        }

    def run_full_security_audit(self) -> Dict[str, Any]:
        """Perform system-wide Cloudflare cybersecurity audit."""
        start_time = time.time()
        agents = self.discover_all_agents()
        host_audit = self.audit_host_system()
        github_audit = self.audit_github_posture(agents)

        agent_audits = []
        all_threats = list(host_audit.get("findings", []))
        all_threats.extend(github_audit.get("findings", []))

        for agent in agents:
            res = self.audit_agent(agent)
            agent_audits.append(res)
            all_threats.extend(res.get("findings", []))

        # Calculate Cloudflare Security Score (0-100)
        crit_count = sum(1 for t in all_threats if t.get("severity") == "CRITICAL")
        high_count = sum(1 for t in all_threats if t.get("severity") == "HIGH")
        med_count = sum(1 for t in all_threats if t.get("severity") == "MEDIUM")
        low_count = sum(1 for t in all_threats if t.get("severity") == "LOW")

        deductions = (crit_count * 20) + min(35, high_count * 5) + min(25, med_count * 3) + min(15, low_count * 1)
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
            "github_cloud_audit": github_audit,
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
            elif "Pre-Push" in title or cat == "GITHUB_PUSH_PROTECTION":
                sol_id = "SOL-GH-PREPUSH-HOOK"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Cloudflare Pre-Push Secret Guard Hook Enforcement",
                        "solution_gu": "પબ્લિક ગીટહબ પર પુશ કરતાં પહેલાં ક્રેડેન્શિયલ્સ આપોઆપ બ્લોક કરવા પ્રી-પુશ હૂક ઇન્સ્ટોલ કરો.",
                        "action_required": "Install executable .git/hooks/pre-push script across all repositories to intercept secrets.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            elif "Dependabot" in title or cat == "GITHUB_SUPPLY_CHAIN":
                sol_id = "SOL-GH-DEPENDABOT"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "GitHub Dependabot Supply Chain Vulnerability Patching",
                        "solution_gu": "સપ્લાય ચેઇન સુરક્ષા માટે .github/dependabot.yml કોન્ફિગર કરો.",
                        "action_required": "Deploy .github/dependabot.yml to enable weekly automated vulnerability monitoring.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            elif "Permissions" in title or cat == "GITHUB_ACTIONS_HARDENING":
                sol_id = "SOL-GH-WORKFLOW-HARDEN"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "GitHub Actions Least-Privilege Permission Boundary",
                        "solution_gu": "વર્કફ્લોમાં 'permissions: contents: read' ઉમેરી અનધિકૃત રાઇટ એક્સેસ રોકો.",
                        "action_required": "Inject permissions: contents: read into all GitHub Actions workflow files.",
                        "affected_items": [],
                        "can_autofix": True
                    }
                solutions_map[sol_id]["affected_items"].append(title)
            elif "Plaintext Token" in title or cat == "GITHUB_CREDENTIAL_LEAK":
                sol_id = "SOL-GH-CREDENTIAL-VAULT"
                if sol_id not in solutions_map:
                    solutions_map[sol_id] = {
                        "id": sol_id,
                        "severity": sev,
                        "title": "Sanitize Git Config Remote Credentials",
                        "solution_gu": ".git/config માંથી પ્લેનટેક્સ્ટ ટોકન હટાવીને SSH અથવા ક્રેડેન્શિયલ કીચેન વાપરો.",
                        "action_required": "Remove token from git remote URL and authenticate using gh auth or SSH.",
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
        """Automatically execute safe defensive mitigations across Laptop, GitHub & Agents."""
        report = self.run_full_security_audit()
        agents = self.discover_all_agents()
        remediated_actions = []

        # 1. Auto-install Pre-Push Secret Guard Hook in all git repos
        for agent in agents:
            p = Path(agent["path"])
            git_hooks = p / ".git" / "hooks"
            if git_hooks.exists():
                hook_file = git_hooks / "pre-push"
                try:
                    hook_file.write_text(PRE_PUSH_HOOK_SCRIPT, encoding="utf-8")
                    hook_file.chmod(0o755)
                    remediated_actions.append(f"Installed Pre-Push Secret Guard Hook in {agent['name']}")
                except Exception as e:
                    logger.debug("Failed installing pre-push hook in %s: %s", agent['name'], e)

        # 2. Auto-provision .github/dependabot.yml in all repos
        for agent in agents:
            p = Path(agent["path"])
            gh_dir = p / ".github"
            if p.exists() and (p / ".git").exists():
                gh_dir.mkdir(parents=True, exist_ok=True)
                dep_file = gh_dir / "dependabot.yml"
                if not dep_file.exists():
                    try:
                        dep_file.write_text(DEPENDABOT_TEMPLATE, encoding="utf-8")
                        remediated_actions.append(f"Deployed Dependabot config in {agent['name']}")
                    except Exception as e:
                        logger.debug("Failed writing dependabot in %s: %s", agent['name'], e)

        # 3. Auto-harden .gitignore in all repos
        for agent in agents:
            agent_path = Path(agent["path"])
            if agent_path.exists():
                gi = agent_path / ".gitignore"
                existing = gi.read_text(encoding="utf-8", errors="ignore") if gi.exists() else ""
                needed = [".env", ".venv", "__pycache__/", "*.pyc", "*.key", "*.token", "*.pem"]
                to_add = [n for n in needed if n not in existing]
                if to_add:
                    try:
                        with gi.open("a", encoding="utf-8") as f:
                            f.write("\n# Cloudflare Security Auditor Hardening\n" + "\n".join(to_add) + "\n")
                        remediated_actions.append(f"Hardened .gitignore in {agent['name']}")
                    except Exception as e:
                        logger.debug("Failed updating .gitignore in %s: %s", agent['name'], e)

        # 4. Auto-harden GitHub Actions permissions (permissions: contents: read)
        for agent in agents:
            p = Path(agent["path"])
            wf_dir = p / ".github" / "workflows"
            if wf_dir.exists():
                for wf in wf_dir.glob("*.yml"):
                    try:
                        content = wf.read_text(encoding="utf-8")
                        if "permissions:" not in content and "jobs:" in content:
                            new_content = content.replace("jobs:\n", "permissions:\n  contents: read\n\njobs:\n", 1)
                            wf.write_text(new_content, encoding="utf-8")
                            remediated_actions.append(f"Injected least-privilege permissions in {agent['name']} ({wf.name})")
                    except Exception as e:
                        logger.debug("Failed updating workflow in %s: %s", agent['name'], e)

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
        print("🛡️ Executing Autonomous Cloudflare Security Remediation across Laptop, GitHub & Agents...")
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
    
    # GitHub Repositories Posture Card
    gh_rep = rep.get("github_cloud_audit", {})
    if gh_rep:
        print("-" * 76)
        print("GITHUB CLOUD REPOSITORIES SECURITY POSTURE:")
        gh_status_color = "\033[32mPASS\033[0m" if gh_rep.get("status") == "PASS" else ("\033[31mFAIL\033[0m" if gh_rep.get("status") == "FAIL" else "\033[33mWARNING\033[0m")
        secured_prepush = sum(1 for r in gh_rep.get("repositories", []) if r.get("has_pre_push_hook"))
        secured_dep = sum(1 for r in gh_rep.get("repositories", []) if r.get("has_dependabot"))
        total_r = gh_rep.get("total_repositories_audited", 0)
        print(f"  • Overall Posture: {gh_status_color} ({gh_rep.get('findings_count', 0)} finding(s) across {total_r} repos)")
        print(f"  • Pre-Push Secret Guard Hook: {secured_prepush}/{total_r} Repos Protected")
        print(f"  • Dependabot Supply Chain Patching: {secured_dep}/{total_r} Repos Configured")

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
