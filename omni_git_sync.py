#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
OMNI-AGENT AUTONOMOUS GIT CLOUD AUTO-SYNC ENGINE
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Master Tech)

Features:
1. Monitors ALL 9 autonomous agent repositories across this laptop:
   - Chamunda RE Enterprise (Aradhya CEO & Dealership Suite)
   - Jarvis Mark VII Agent
   - Web2APK Android Packager
   - Web2IPA Apple iOS Packager
   - APK TV Converter Agent
   - PublisheR AI (Book Publishing Agent)
   - KidsPlay AI Studio (Games Engine)
   - YouTube Production Agent
   - MicroCorp AI Enterprise
2. Automatically detects changes made by Antigravity or local agents.
3. Stages, commits with descriptive metadata, and pushes to GitHub origin main.
4. Seamlessly callable as a 24/7 background watchdog task or CLI (`aradhya-sync --all`).
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [OmniGitSync] %(message)s"
)
logger = logging.getLogger("OmniGitSync")


def get_git_executable() -> str:
    for candidate in [
        "/home/alpesh/.local/bin/git",
        "/usr/bin/git",
        "/usr/local/bin/git",
        "/bin/git"
    ]:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return candidate
    import shutil
    return shutil.which("git") or "git"


REGISTERED_AGENTS: List[Dict[str, Any]] = [
    {
        "id": "chamunda_re_enterprise",
        "name": "Chamunda RE Enterprise (Aradhya CEO)",
        "path": Path("/home/alpesh/chamunda_re_enterprise"),
        "remote": "thakoralpesh3/chamunda-re-enterprise"
    },
    {
        "id": "jarvis_agent",
        "name": "Jarvis Mark VII System Assistant",
        "path": Path("/home/alpesh/jarvis-agent"),
        "remote": "thakoralpesh3/jarvis-agent"
    },
    {
        "id": "web_to_apk_agent",
        "name": "Web2APK Autonomous Android Packager",
        "path": Path("/home/alpesh/web-to-apk-agent"),
        "remote": "thakoralpesh3/web-to-apk-agent"
    },
    {
        "id": "web_to_ipa_agent",
        "name": "Web2IPA Autonomous iOS Packager",
        "path": Path("/home/alpesh/web-to-ipa-agent"),
        "remote": "thakoralpesh3/web-to-ipa-agent"
    },
    {
        "id": "apk_tv_converter_agent",
        "name": "APK TV Converter Agent",
        "path": Path("/home/alpesh/apk-tv-converter-agent"),
        "remote": "thakoralpesh3/apk-tv-converter-agent"
    },
    {
        "id": "book_publishing_agent",
        "name": "PublisheR AI Book Publishing Agent",
        "path": Path("/home/alpesh/book-publishing-agent"),
        "remote": "thakoralpesh3/book-publishing-agent"
    },
    {
        "id": "kids_game_studio",
        "name": "KidsPlay AI Studio",
        "path": Path("/home/alpesh/kids-game-studio"),
        "remote": "thakoralpesh3/kidsplay-ai-studio"
    },
    {
        "id": "youtube_agent",
        "name": "YouTube Production & Growth Agent",
        "path": Path("/home/alpesh/youtube-agent"),
        "remote": "thakoralpesh3/youtube-agent"
    },
    {
        "id": "microcorp_agent",
        "name": "MicroCorp AI Autonomous Enterprise",
        "path": Path("/media/alpesh/Software & Work/Agents/microcorp-agent"),
        "remote": "thakoralpesh3/microcorp-agent"
    }
]


class OmniGitSyncEngine:
    def __init__(self):
        self.git_bin = get_git_executable()
        self.env = os.environ.copy()
        self.env["PATH"] = f"/home/alpesh/.local/bin:/home/alpesh/bin:{self.env.get('PATH', '/usr/bin:/bin')}"
        self.agents = REGISTERED_AGENTS

    def is_git_repo(self, repo_dir: Path) -> bool:
        return repo_dir.exists() and (repo_dir / ".git").exists()

    def get_repo_status(self, repo_dir: Path) -> Dict[str, Any]:
        if not self.is_git_repo(repo_dir):
            return {"is_repo": False, "dirty": False, "files": []}

        try:
            res = subprocess.run(
                [self.git_bin, "status", "--porcelain"],
                cwd=str(repo_dir),
                env=self.env,
                capture_output=True,
                text=True,
                timeout=10
            )
            lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
            return {
                "is_repo": True,
                "dirty": len(lines) > 0,
                "changed_count": len(lines),
                "files": lines[:10]
            }
        except Exception as e:
            logger.error("Git status error on %s: %s", repo_dir, e)
            return {"is_repo": True, "dirty": False, "error": str(e), "files": []}

    def sync_repo(self, agent: Dict[str, Any], reason: str = "Antigravity Updates") -> Tuple[bool, str]:
        repo_dir = agent["path"]
        name = agent["name"]

        if not self.is_git_repo(repo_dir):
            return False, f"Directory {repo_dir} is not a git repo or inaccessible."

        # Clear stale index.lock if present
        lock_file = repo_dir / ".git" / "index.lock"
        if lock_file.exists():
            try:
                if (time.time() - lock_file.stat().st_mtime) > 5.0:
                    lock_file.unlink(missing_ok=True)
            except Exception:
                pass

        status = self.get_repo_status(repo_dir)
        if not status.get("dirty"):
            return True, f"{name}: Clean; no changes to sync."

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"🤖 Auto-Sync: {reason} in {name} [{timestamp}]"

        try:
            # 1. Stage changes
            subprocess.run(
                [self.git_bin, "add", "."],
                cwd=str(repo_dir),
                env=self.env,
                check=True,
                timeout=20
            )

            # 2. Check if staged changes exist
            diff_check = subprocess.run(
                [self.git_bin, "diff", "--cached", "--quiet"],
                cwd=str(repo_dir),
                env=self.env
            )
            if diff_check.returncode == 0:
                return True, f"{name}: No staged modifications."

            # 3. Commit
            commit_res = subprocess.run(
                [self.git_bin, "commit", "-m", commit_msg],
                cwd=str(repo_dir),
                env=self.env,
                capture_output=True,
                text=True,
                timeout=20
            )
            if commit_res.returncode != 0:
                logger.warning("Commit failed for %s: %s", name, commit_res.stderr)
                return False, f"Commit error: {commit_res.stderr.strip()}"

            logger.info("✅ [%s] Committed: %s", name, commit_msg)

            # 4. Push to remote
            push_res = subprocess.run(
                [self.git_bin, "push", "origin", "main"],
                cwd=str(repo_dir),
                env=self.env,
                capture_output=True,
                text=True,
                timeout=60
            )
            if push_res.returncode == 0:
                logger.info("🚀 [%s] Successfully pushed updates to GitHub origin/main!", name)
                return True, f"Successfully pushed {name} updates at {timestamp}"
            else:
                logger.warning("Push warning for %s: %s", name, push_res.stderr)
                return False, f"Push error: {push_res.stderr.strip()}"

        except Exception as e:
            logger.error("Auto-sync error for %s: %s", name, e)
            return False, str(e)

    def sync_all(self, reason: str = "Omni-Agent Auto-Sync") -> Dict[str, Any]:
        results = {}
        synced_count = 0
        for agent in self.agents:
            if not agent["path"].exists():
                continue
            synced, msg = self.sync_repo(agent, reason=reason)
            results[agent["id"]] = {"synced": synced, "message": msg}
            if synced and "Clean" not in msg and "No staged" not in msg:
                synced_count += 1
        return {"total_checked": len(self.agents), "synced_count": synced_count, "results": results}


_engine = None

def get_omni_sync_engine() -> OmniGitSyncEngine:
    global _engine
    if _engine is None:
        _engine = OmniGitSyncEngine()
    return _engine


if __name__ == "__main__":
    engine = get_omni_sync_engine()
    
    # Check if --all or specific directory
    if len(sys.argv) > 1 and sys.argv[1] in ["--all", "-a"]:
        print("🌐 Running Omni-Agent Cloud Auto-Sync across all 9 agent repositories...")
        res = engine.sync_all(reason="Manual Omni-Sync Trigger")
        print(f"✅ Sync complete: {res['synced_count']} repository(ies) pushed to GitHub.")
        for agent_id, data in res["results"].items():
            if "Clean" not in data["message"] and "No staged" not in data["message"]:
                print(f"  - {agent_id}: {data['message']}")
    else:
        # Detect current directory
        cwd = Path.cwd().resolve()
        matched = False
        for agent in engine.agents:
            try:
                if cwd == agent["path"].resolve() or cwd.is_relative_to(agent["path"].resolve()):
                    print(f"🤖 Synchronizing active agent repository: {agent['name']}...")
                    ok, msg = engine.sync_repo(agent, reason="Active Directory Sync Trigger")
                    if ok:
                        print(f"✅ {msg}")
                    else:
                        print(f"❌ {msg}")
                    matched = True
                    break
            except Exception:
                pass
        if not matched:
            print("🌐 Synchronizing ALL 9 agent repositories...")
            res = engine.sync_all(reason="Omni-Sync Trigger")
            print(f"✅ Sync complete: {res['synced_count']} repository(ies) updated.")
