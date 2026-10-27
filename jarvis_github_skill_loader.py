# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
Jarvis Agent Online GitHub Skill Loader (જાર્વિસ ગિટહબ સ્કિલ લોડર)
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Features:
1. Online Skill Synchronization:
   - Syncs and verifies skills from https://github.com/thakoralpesh3/jarvis-agent
   - Dynamically imports and executes tools from /home/alpesh/jarvis-agent/tools
2. Offline Resilient Caching:
   - All tools are cached locally on disk.
   - When offline, execution runs 100% locally with zero internet dependency.
"""

import os
import sys
import time
import json
import logging
import subprocess
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional

JARVIS_DIR = Path("/home/alpesh/jarvis-agent")
TOOLS_DIR = JARVIS_DIR / "tools"
CORE_DIR = JARVIS_DIR / "core"
SKILL_CACHE_FILE = JARVIS_DIR / "memory" / "skills_catalog.json"

if str(JARVIS_DIR) not in sys.path:
    sys.path.insert(0, str(JARVIS_DIR))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [JarvisSkillLoader] %(message)s"
)
logger = logging.getLogger("JarvisSkillLoader")


class JarvisSkillLoader:
    """
    Manages loading and dynamic dispatch of Jarvis tools and skills.
    """

    def __init__(self):
        self.jarvis_dir = JARVIS_DIR
        self.tools_dir = TOOLS_DIR
        self.skills_catalog: Dict[str, Any] = {}
        self.last_sync_time = 0.0
        self.refresh_catalog()

    def sync_from_github(self) -> Dict[str, Any]:
        """
        Pulls latest commits from origin/main if internet is accessible.
        """
        if not self.jarvis_dir.exists():
            return {"success": False, "error": "jarvis-agent directory not found"}

        try:
            res = subprocess.run(
                ["git", "-C", str(self.jarvis_dir), "pull", "--ff-only", "origin", "main"],
                capture_output=True,
                text=True,
                timeout=10
            )
            self.last_sync_time = time.time()
            self.refresh_catalog()
            logger.info("GitHub Skill Sync completed: %s", res.stdout.strip())
            return {
                "success": res.returncode == 0,
                "output": res.stdout.strip() or res.stderr.strip(),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.warning("Could not sync Jarvis skills from GitHub (%s). Using local cache.", e)
            return {"success": False, "error": str(e), "using_local_cache": True}

    def refresh_catalog(self) -> Dict[str, Any]:
        """
        Scans tools directory and builds index of available functions.
        """
        catalog = {}
        if not self.tools_dir.exists():
            return catalog

        for py_file in self.tools_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            module_name = f"tools.{py_file.stem}"
            try:
                mod = importlib.import_module(module_name)
                funcs = [f for f in dir(mod) if callable(getattr(mod, f)) and not f.startswith("_")]
                catalog[py_file.stem] = {
                    "module": module_name,
                    "file": str(py_file),
                    "functions": funcs
                }
            except Exception as e:
                logger.debug("Could not inspect module %s: %s", module_name, e)

        self.skills_catalog = catalog
        try:
            SKILL_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            SKILL_CACHE_FILE.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
        except Exception:
            pass
        return catalog

    def execute_tool(self, module_stem: str, function_name: str, *args, **kwargs) -> Any:
        """
        Dynamically executes a tool function.
        """
        module_name = f"tools.{module_stem}"
        try:
            mod = importlib.import_module(module_name)
            func = getattr(mod, function_name)
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("Failed to execute %s.%s: %s", module_stem, function_name, e)
            return {"success": False, "error": str(e)}


_skill_loader: Optional[JarvisSkillLoader] = None

def get_jarvis_skill_loader() -> JarvisSkillLoader:
    global _skill_loader
    if _skill_loader is None:
        _skill_loader = JarvisSkillLoader()
    return _skill_loader


if __name__ == "__main__":
    loader = get_jarvis_skill_loader()
    print("Catalog modules loaded:", len(loader.skills_catalog))
    for mod, data in list(loader.skills_catalog.items())[:5]:
        print(f"  • {mod}: {len(data['functions'])} functions")
