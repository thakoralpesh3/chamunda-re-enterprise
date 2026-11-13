# -*- coding: utf-8 -*-
"""
Aradhya • OpenJarvis Modular AI Framework Bridge
Integrates Aradhya Autonomous Core with https://github.com/open-jarvis/OpenJarvis
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

OPENJARVIS_DIR = Path("/home/alpesh/OpenJarvis")
OPENJARVIS_SRC = OPENJARVIS_DIR / "src"

if OPENJARVIS_SRC.exists() and str(OPENJARVIS_SRC) not in sys.path:
    sys.path.insert(0, str(OPENJARVIS_SRC))

logger = logging.getLogger("AradhyaOpenJarvisBridge")


class AradhyaOpenJarvisBridge:
    """
    Bridge connecting Aradhya with OpenJarvis tools, registry, and execution pipeline.
    """

    def __init__(self):
        self.available = False
        self.registry = None
        self._init_openjarvis()

    def _init_openjarvis(self) -> None:
        if not OPENJARVIS_SRC.exists():
            return
        try:
            import openjarvis.tools
            from openjarvis.core.registry import ToolRegistry
            self.registry = ToolRegistry
            self.available = True
            logger.info("OpenJarvis ToolRegistry loaded successfully (%d tools available).", len(self.registry.keys()))
        except Exception as e:
            logger.warning("Could not initialize OpenJarvis registry: %s", e)
            self.available = False

    def list_tools(self) -> List[str]:
        """List all registered OpenJarvis tools."""
        if not self.available or not self.registry:
            return []
        return list(self.registry.keys())

    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute an OpenJarvis tool by name with arguments.
        """
        if not self.available or not self.registry:
            return {
                "success": False,
                "error": "OpenJarvis is not available on this system."
            }

        tool_cls = self.registry.get(tool_name)
        if not tool_cls:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found in OpenJarvis registry."
            }

        try:
            tool_instance = tool_cls()
            result = tool_instance.execute(**kwargs)
            return {
                "success": getattr(result, "success", True),
                "content": getattr(result, "content", str(result)),
                "tool_name": getattr(result, "tool_name", tool_name),
                "cost_usd": getattr(result, "cost_usd", 0.0),
                "latency_seconds": getattr(result, "latency_seconds", 0.0)
            }
        except Exception as e:
            logger.exception("Error executing OpenJarvis tool '%s': %s", tool_name, e)
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }


_bridge_instance: Optional[AradhyaOpenJarvisBridge] = None


def get_openjarvis_bridge() -> AradhyaOpenJarvisBridge:
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = AradhyaOpenJarvisBridge()
    return _bridge_instance
