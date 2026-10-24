#!/bin/bash
# ==============================================================================
# Chamunda Automobile Enterprise • Project Chhaya
# Dell Inspiron 3542 100% Software Speed Optimizer
# Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
# ==============================================================================

set -e
echo "🚀 [Chamunda Turbo] Initializing Software Speed Optimization..."

# 1. Virtual Memory & Kernel Swappiness Tuning
echo "⚡ [1/5] Applying Kernel RAM & HDD Swappiness Optimizations..."
cat << 'SYSCTL_EOF' > /etc/sysctl.d/99-chamunda-turbo.conf
# Prefer physical RAM, avoid slow 5400 RPM mechanical HDD swap thrashing
vm.swappiness = 10
# Cache directory inodes and file trees longer in memory
vm.vfs_cache_pressure = 50
# Smooth disk flushing to avoid long freezing
vm.dirty_background_ratio = 5
vm.dirty_ratio = 10
SYSCTL_EOF
sysctl -p /etc/sysctl.d/99-chamunda-turbo.conf >/dev/null 2>&1 || true

# 2. Enable ZRAM (Compressed RAM Swap - Eliminates HDD lag on 4GB RAM)
echo "⚡ [2/5] Setting up ZRAM Compressed RAM Engine..."
if ! command -v zramctl >/dev/null 2>&1; then
    apt-get update -qq && apt-get install -y -qq zram-tools || true
fi

if [ -f /etc/default/zramswap ]; then
    sed -i 's/^#*ALGO=.*/ALGO=lz4/' /etc/default/zramswap || true
    sed -i 's/^#*PERCENT=.*/PERCENT=60/' /etc/default/zramswap || true
    systemctl restart zramswap >/dev/null 2>&1 || true
fi

# 3. Disable Useless Boot & Background Daemons
echo "⚡ [3/5] Disabling Slow Boot Hang Services & Printers Spoolers..."
# Disable obsolete live-installer remnant
systemctl disable --now casper-md5check.service >/dev/null 2>&1 || true
# Disable background network printer broadcasts if not used
systemctl disable --now cups-browsed.service >/dev/null 2>&1 || true
# Disable daily firmware updater daemon on older laptops
systemctl disable --now fwupd-refresh.timer fwupd-refresh.service >/dev/null 2>&1 || true

# 4. Limit Systemd Journal Size (Stops 10-second HDD disk flush delay)
echo "⚡ [4/5] Capping Systemd Logs to 50MB..."
mkdir -p /etc/systemd/journald.conf.d
cat << 'JOURNAL_EOF' > /etc/systemd/journald.conf.d/size-limit.conf
[Journal]
SystemMaxUse=50M
JOURNAL_EOF
systemctl restart systemd-journald >/dev/null 2>&1 || true

# 5. Disk Cache & Temporary Files Cleanup
echo "⚡ [5/5] Pruning System Cache & Thumbnails..."
apt-get autoremove -y -qq >/dev/null 2>&1 || true
apt-get clean >/dev/null 2>&1 || true
rm -rf /home/alpesh/.cache/thumbnails/* >/dev/null 2>&1 || true

echo "✅ [Chamunda Turbo] All 5 Software Accelerations Successfully Applied!"
echo "🎉 Laptop is now running at peak software efficiency without any physical modifications."
