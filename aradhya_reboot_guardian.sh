#!/usr/bin/env bash
# ==============================================================================
# Aradhya Supreme Autonomous Executive AI • Hardware Power-On Reboot Guardian
# Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
# Executed via user crontab @reboot the moment laptop hardware powers on.
# ==============================================================================

export PATH="/home/alpesh/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
BASE_DIR="/home/alpesh/chamunda_re_enterprise"
LOG_FILE="$BASE_DIR/data/aradhya_reboot.log"
mkdir -p "$BASE_DIR/data"

echo "============================================================" >> "$LOG_FILE"
echo "🚀 [$(date '+%Y-%m-%d %H:%M:%S')] Laptop Hardware Power-On Detected" >> "$LOG_FILE"
echo "============================================================" >> "$LOG_FILE"

# 1. Clean up stale lock and temp files from previous sessions
rm -f /tmp/aradhya_desktop_boot_done /tmp/aradhya_startup.lock /tmp/chhaya_mirror.pid.stale /tmp/aradhya_user_dismissed

# 2. Ensure 'Software & Work' partition (/media/alpesh/Software & Work/Agents) is mounted
/home/alpesh/bin/ensure_software_work_mount.sh >> "$LOG_FILE" 2>&1 || true

# 3. Ensure systemd user environment and chamunda-chhaya.service are active
systemctl --user start chamunda-chhaya.service >> "$LOG_FILE" 2>&1 || true

# 4. Log active state
SVC_STATUS=$(systemctl --user is-active chamunda-chhaya.service 2>/dev/null || echo "unknown")
echo "ℹ️ [$(date '+%Y-%m-%d %H:%M:%S')] chamunda-chhaya.service status: $SVC_STATUS" >> "$LOG_FILE"

# 5. Trigger memory self-trimming
python3 -c "
import gc, ctypes
gc.collect()
try:
    ctypes.CDLL('libc.so.6').malloc_trim(0)
except Exception:
    pass
" >> "$LOG_FILE" 2>&1 || true

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] Hardware Reboot Guardian Initialized Successfully." >> "$LOG_FILE"
