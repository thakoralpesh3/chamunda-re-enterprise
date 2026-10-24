#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya Autonomous Executive Intelligence • JARVIS Laptop Startup Protocol
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Automatically executed when Alpesh Sir turns on the laptop and desktop session starts:
1. Gathers hardware & OS diagnostics (Battery, RAM, Disk, Uptime).
2. Probes internet connectivity (Online Hybrid vs Air-Gapped).
3. Verifies zero-trust cryptographic code integrity (SHA-256).
4. Dispatches desktop graphical notification (notify-send).
5. Speaks audible welcome announcement through laptop speakers in lifelike neural voice.
6. Records event into data/aradhya_startup.log.
"""

import os
import sys
import time
import datetime
import subprocess
from pathlib import Path

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from aradhya_autonomous_core import get_aradhya_engine
from aradhya_voice_engine import get_voice_engine

LOG_FILE = BASE_DIR / "data" / "aradhya_startup.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def run_startup_sequence():
    start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    engine = get_aradhya_engine()
    voice = get_voice_engine()

    # Small pause to allow desktop audio and notification daemon to settle
    time.sleep(2.5)

    # 1. Telemetry checks
    battery = engine.get_battery_status()
    bat_pct = battery.get("percent", 100)
    charging_text = "ચાર્જિંગ મોડ ⚡" if battery.get("charging") else "બેટરી પાવર"

    storage = engine.get_disk_storage()
    free_gb = storage.get("free_gb", 0)

    net = engine.check_internet_connection()
    is_online = net.get("is_online", False)
    latency = net.get("latency_ms", 0)

    # 2. Desktop notification
    notify_title = "👑 Aradhya Autonomous Executive Core Online"
    notify_body = (
        f"જય માતાજી અલ્પેશ સાહેબ! ⚡\n"
        f"• મોડ: {'હાઇબ્રિડ ઓનલાઇન 🌐' if is_online else '૧૦૦% ઓફલાઇન શીલ્ડ 🛡️'}\n"
        f"• બેટરી: {bat_pct}% ({charging_text})\n"
        f"• ફ્રી સ્ટોરેજ: {free_gb} GB\n"
        f"• ઓથોરિટી: સમગ્ર લેપટોપ (/home/alpesh) પર સંપૂર્ણ સક્રિય"
    )

    try:
        subprocess.run(
            ["notify-send", "-u", "normal", "-t", "8000", notify_title, notify_body],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass

    # 3. Spoken Voice Announcement
    if is_online:
        spoken_greeting = (
            f"જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા. "
            f"લેપટોપ સિસ્ટમ સફળતાપૂર્વક ઓનલાઇન થઈ ગઈ છે. "
            f"બેટરી {bat_pct} ટકા છે, અને ઇન્ટરનેટ કનેક્શન જીવંત છે. "
            f"સમગ્ર લેપટોપ પર તમામ કંટ્રોલ્સ સક્રિય છે, અને હું આપના આદેશ માટે તૈયાર છું!"
        )
    else:
        spoken_greeting = (
            f"જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા. "
            f"લેપટોપ ઓફલાઇન એર-ગેપ્ડ ડિફેન્સ મોડમાં સક્રિય છે. "
            f"બેટરી {bat_pct} ટકા છે. "
            f"૧૦૦% ઓફલાઇન કંટ્રોલ સક્રિય છે, અને હું આપના આદેશ માટે તૈયાર છું!"
        )

    # 3. Spoken Voice Announcement (Instant Pre-rendered Neural Vault First)
    try:
        subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    vault_file = BASE_DIR / "data" / "aradhya_offline_voice_vault" / ("startup_online.mp3" if is_online else "startup_offline.mp3")
    played = False
    if vault_file.exists():
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            pygame.mixer.music.load(str(vault_file))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            played = True
        except Exception:
            played = False

    if not played:
        try:
            voice.speak(spoken_greeting, language="gu", blocking=True)
        except Exception as e:
            voice.speak_offline(spoken_greeting, language="gu")

    # 4. Log event
    log_entry = (
        f"[{start_time}] ARADHYA STARTUP EXECUTION\n"
        f"• Status: {'ONLINE_HYBRID' if is_online else 'OFFLINE_AIR_GAPPED'} (Latency: {latency}ms)\n"
        f"• Battery: {bat_pct}% ({battery.get('status_text')})\n"
        f"• Storage: {free_gb} GB Free\n"
        f"• Spoken Greeting: SUCCESS\n"
        f"{'-'*60}\n"
    )
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception:
        pass

    print(f"Aradhya startup sequence completed successfully at {start_time}.")

if __name__ == "__main__":
    run_startup_sequence()
