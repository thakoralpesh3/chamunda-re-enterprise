# -*- coding: utf-8 -*-
"""
Aradhya • OpenJarvis API Server Daemon
Runs OpenJarvis OpenAI-compatible API server bound to 127.0.0.1:8000
with Aradhya's multi-key pool, security guardrails, and tool matrix.
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)
"""

import os
import sys
import logging
from pathlib import Path

BASE_DIR = Path(__file__).parent
OPENJARVIS_SRC = Path("/home/alpesh/OpenJarvis/src")

if str(OPENJARVIS_SRC) not in sys.path:
    sys.path.insert(0, str(OPENJARVIS_SRC))
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure Gemini API key is populated from Chamunda pool if not already set in environment
if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
    try:
        from chamunda_llm_engine import get_api_key_pool
        pool = get_api_key_pool()
        keys = pool.get_candidate_keys()
        if keys:
            os.environ["GEMINI_API_KEY"] = keys[0]
            os.environ["GOOGLE_API_KEY"] = keys[0]
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [AradhyaOpenJarvisServer] %(message)s"
)
logger = logging.getLogger("AradhyaOpenJarvisServer")


def start_server(host: str = "127.0.0.1", port: int = 8000):
    logger.info("Starting OpenJarvis server for Aradhya on http://%s:%d ...", host, port)
    from openjarvis.core.config import load_config
    from openjarvis.server.daemon import run_server
    from openjarvis.server.app import create_app
    from openjarvis.engine import get_engine
    from openjarvis.core.events import EventBus
    from openjarvis.security import setup_security

    config = load_config()
    bus = EventBus(record_history=False)
    resolved = get_engine(config, "cloud", model=config.intelligence.default_model)
    if not resolved:
        resolved = get_engine(config, None, model=None)

    engine_name, engine = resolved if resolved else ("nim", None)
    sec = setup_security(config, engine, bus)

    app = create_app(
        sec.engine if sec else engine,
        config.intelligence.default_model or "gemini-3.5-flash-lite",
        agent=None,
        bus=bus,
        engine_name=engine_name,
        agent_name="simple",
        config=config,
        capability_policy=sec.capability_policy if sec else None,
        rate_limiter=sec.rate_limiter if sec else None,
        audit_logger=sec.audit_logger if sec else None,
        api_key="",
        cors_origins=["*"]
    )

    logger.info("OpenJarvis FastAPI app constructed successfully. Starting daemon on %s:%d", host, port)
    run_server(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    start_server()
