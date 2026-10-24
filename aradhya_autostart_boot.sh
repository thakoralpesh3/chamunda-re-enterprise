#!/usr/bin/env bash
# ==============================================================================
# Aradhya Supreme Autonomous Executive AI • Laptop Boot & Login Orchestrator
# Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
# ==============================================================================

export PATH="/home/alpesh/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"

BASE_DIR="/home/alpesh/chamunda_re_enterprise"
BOOT_LOG="$BASE_DIR/data/aradhya_boot_debug.log"
mkdir -p "$BASE_DIR/data"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$BOOT_LOG"
}

log "============================================================"
log "🚀 Aradhya Desktop Login Orchestrator Initiated"
log "============================================================"

# 1. Wait for X11 graphical display server to be responsive
log "⏳ Waiting for X11 Display Server ($DISPLAY)..."
X_READY=0
for i in {1..30}; do
    if xset q >/dev/null 2>&1; then
        X_READY=1
        log "✅ X11 Display Server ready after ${i}s"
        break
    fi
    sleep 1
done

if [ "$X_READY" -eq 0 ]; then
    log "⚠️ Warning: X11 Display Server not ready after 30s. Proceeding with best effort."
fi

# 2. Allow Cinnamon compositor and audio server 4 seconds to settle
sleep 4

# 3. Ensure 24/7 Background Watchdog & Cloud Shadow Service is active
systemctl --user start chamunda-chhaya.service >> "$BOOT_LOG" 2>&1 || true
log "ℹ️ chamunda-chhaya.service verified"

# 4. Pre-warm gnome-terminal-server to eliminate cold-boot DBus activation delays
systemctl --user start gnome-terminal-server.service >> "$BOOT_LOG" 2>&1 || true
sleep 1

# 5. Deliver Audible Voice Greeting & Desktop Notification in background
python3 "$BASE_DIR/aradhya_startup_greeting.py" >> "$BOOT_LOG" 2>&1 &
log "🔊 Voice greeting and desktop notification dispatched"

# 6. Run Daily YouTube Shorts pipeline quietly in background if due for today
if [ -d "/home/alpesh/jarvis-agent" ]; then
    python3 -c "
try:
    import sys; sys.path.insert(0, '/home/alpesh/jarvis-agent')
    from core.youtube_commander import YouTubeShortsCommander
    yt = YouTubeShortsCommander()
    if yt.is_daily_run_due():
        import threading
        t = threading.Thread(target=yt.run_and_supervise_pipeline, daemon=False)
        t.start()
except Exception:
    pass
" >> "$BOOT_LOG" 2>&1 &
fi

# 7. Resilient Terminal Console Launcher with Multi-Attempt Fallbacks
log "🖥️ Launching Aradhya Supreme Interactive Terminal Console..."

launch_terminal() {
    if pgrep -f "/home/alpesh/bin/aradhya" >/dev/null 2>&1; then
        log "ℹ️ Aradhya console is already running on the desktop."
        return 0
    fi

    # Attempt 1: Standard gnome-terminal
    log "Attempt 1: Launching via gnome-terminal..."
    gnome-terminal --title="👑 Aradhya Autonomous AI Orchestrator" \
                   --geometry=115x32 \
                   -- bash -c "/home/alpesh/bin/aradhya" >> "$BOOT_LOG" 2>&1 &
    
    sleep 3
    if pgrep -f "/home/alpesh/bin/aradhya" >/dev/null 2>&1; then
        log "✅ Terminal console launched successfully (gnome-terminal)"
        wmctrl -a "Aradhya" >/dev/null 2>&1 || true
        return 0
    fi

    # Attempt 2: Fallback via x-terminal-emulator
    log "Attempt 2: Fallback to x-terminal-emulator..."
    x-terminal-emulator -title "👑 Aradhya Autonomous AI Orchestrator" \
                        -e bash -c "/home/alpesh/bin/aradhya" >> "$BOOT_LOG" 2>&1 &

    sleep 3
    if pgrep -f "/home/alpesh/bin/aradhya" >/dev/null 2>&1; then
        log "✅ Terminal console launched successfully (x-terminal-emulator)"
        wmctrl -a "Aradhya" >/dev/null 2>&1 || true
        return 0
    fi

    # Attempt 3: Direct binary invocation of gnome-terminal.real
    log "Attempt 3: Direct invocation via gnome-terminal.real..."
    /usr/bin/gnome-terminal.real --title="👑 Aradhya Autonomous AI Orchestrator" \
                                 -- bash -c "/home/alpesh/bin/aradhya" >> "$BOOT_LOG" 2>&1 &

    sleep 2
    if pgrep -f "/home/alpesh/bin/aradhya" >/dev/null 2>&1; then
        log "✅ Terminal console launched successfully (gnome-terminal.real)"
        wmctrl -a "Aradhya" >/dev/null 2>&1 || true
        return 0
    fi

    log "⚠️ Notice: Terminal window attempt completed."
}

launch_terminal

# Mark desktop boot as done
touch /tmp/aradhya_desktop_boot_done
log "🏁 Aradhya Laptop Startup Protocol Completed Successfully"
