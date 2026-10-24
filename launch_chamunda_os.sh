#!/usr/bin/env bash
# ==============================================================================
# Chamunda Automobile Parts & Service - Executive OS & AI Agent Launcher
# ==============================================================================

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

export PYTHONPATH="/home/alpesh/jarvis-agent:$DIR:$PYTHONPATH"
export PYTHONUNBUFFERED="1"

echo "======================================================================"
echo "🏍️  CHAMUNDA AUTOMOBILE PARTS & SERVICE • ROYAL ENFIELD ENTERPRISE AI"
echo "======================================================================"
echo "Checking executive web portal status on port 8080..."

# Check if port 8080 is already active
if ! python3 -c "import socket; s=socket.socket(); s.settimeout(0.5); exit(0 if s.connect_ex(('127.0.0.1', 8080))==0 else 1)" 2>/dev/null; then
    echo "Starting FastAPI Web Portal in background..."
    mkdir -p "$DIR/data"
    nohup python3 -m uvicorn app:app --host 0.0.0.0 --port 8080 > "$DIR/data/portal.log" 2>&1 &
    sleep 1.2
fi

echo "Opening Web Portal in default browser..."
(
    sleep 0.8
    xdg-open "http://127.0.0.1:8080" >/dev/null 2>&1 || sensible-browser "http://127.0.0.1:8080" >/dev/null 2>&1 || true
) &

# Launch interactive executive AI Agent console in foreground
exec python3 "$DIR/chamunda_agent_cli.py"
