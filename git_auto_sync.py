#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
AUTONOMOUS GIT CLOUD AUTO-SYNC ENGINE
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder & Master Tech)

Features:
1. Detects code/config/template changes made by Antigravity or local autonomous agents.
2. Automatically commits with timestamped descriptive message.
3. Pushes securely to GitHub (thakoralpesh3/chamunda-re-enterprise) via HTTPS / GitHub CLI credentials.
4. Seamlessly callable as a daemon, standalone CLI (`aradhya-sync`), or from chhaya_watchdog.
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [GitAutoSync] %(message)s"
)
logger = logging.getLogger("GitAutoSync")

BASE_DIR = Path(__file__).parent


class GitAutoSyncEngine:
    """Manages autonomous Git commit & push pipeline to GitHub."""

    def __init__(self, repo_dir: Path = BASE_DIR):
        self.repo_dir = repo_dir
        self.last_sync_time = 0.0

    def is_git_repo(self) -> bool:
        return (self.repo_dir / ".git").exists()

    def get_status(self) -> Dict[str, Any]:
        """Check whether working directory has uncommitted or untracked changes."""
        if not self.is_git_repo():
            return {"is_repo": False, "dirty": False, "files": []}

        try:
            res = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=str(self.repo_dir),
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
            logger.error("Git status check error: %s", e)
            return {"is_repo": True, "dirty": False, "error": str(e), "files": []}

    def sync_changes(self, reason: str = "Antigravity Updates") -> Tuple[bool, str]:
        """
        Stage all valid changes, commit, and push to origin.
        """
        if not self.is_git_repo():
            return False, "Directory is not a git repository"

        status = self.get_status()
        if not status.get("dirty"):
            return True, "Working directory clean; no changes to sync."

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"🤖 Auto-Sync: {reason} [{timestamp}]"

        try:
            # 1. Stage changes (respects .gitignore)
            subprocess.run(["git", "add", "."], cwd=str(self.repo_dir), check=True, timeout=15)

            # 2. Check if staged changes exist
            diff_check = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=str(self.repo_dir)
            )
            if diff_check.returncode == 0:
                return True, "No staged modifications to commit."

            # 3. Commit
            commit_res = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(self.repo_dir),
                capture_output=True,
                text=True,
                timeout=15
            )
            if commit_res.returncode != 0:
                logger.warning("Commit failed: %s", commit_res.stderr)
                return False, f"Commit failed: {commit_res.stderr.strip()}"

            logger.info("✅ Committed changes: %s", commit_msg)

            # 4. Push to remote origin main
            push_res = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(self.repo_dir),
                capture_output=True,
                text=True,
                timeout=40
            )
            if push_res.returncode == 0:
                self.last_sync_time = time.time()
                logger.info("🚀 Successfully pushed updates to GitHub origin/main!")
                return True, f"Synchronized successfully with GitHub at {timestamp}"
            else:
                logger.warning("Git push warning: %s", push_res.stderr)
                return False, f"Push error: {push_res.stderr.strip()}"

        except Exception as e:
            logger.error("Auto-sync error: %s", e)
            return False, str(e)


_sync_engine = None

def get_git_sync_engine() -> GitAutoSyncEngine:
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = GitAutoSyncEngine()
    return _sync_engine


if __name__ == "__main__":
    engine = get_git_sync_engine()
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        logger.info("Starting Autonomous Git Auto-Sync Daemon (Interval: 120s)...")
        while True:
            try:
                engine.sync_changes(reason="Scheduled Watchdog Sync")
            except Exception as e:
                logger.error("Daemon cycle error: %s", e)
            time.sleep(120)
    else:
        success, msg = engine.sync_changes(reason="Manual Sync Trigger")
        print(f"[{'SUCCESS' if success else 'FAILED'}] {msg}")
