#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya Real-Time Jarvis Daemon (આરાધ્યા - રિયલ-ટાઇમ જારવિસ ડેમન)
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
Author: Aradhya (CEO)

Functions:
1. Real-time background wake-word listening ("Hey Aradhya", "હે આરાધ્યા", "Aradhya", "આરાધ્યા").
2. Instant spoken acknowledgment in Gujarati ("હા અલ્પેશ સાહેબ, બોલો! હું સાંભળી રહી છું.").
3. Automatic command recording & transcription via Google Gemini 3.5 audio model.
4. Autonomous task execution via AradhyaAutonomousEngine (Antigravity-level parity).
5. Voice output of results in natural Gujarati.
6. Instant multi-channel task completion dispatch to WhatsApp (+91 78747 19139) and Desktop notification banner.
"""

import os
import sys
import time
import re
import wave
import signal
import struct
import math
import subprocess
import threading
from pathlib import Path

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from aradhya_autonomous_core import get_aradhya_engine
from aradhya_voice_engine import get_voice_engine
from aradhya_notifier import AradhyaNotifier

DAEMON_LOG = BASE_DIR / "data" / "aradhya_jarvis_daemon.log"
DAEMON_LOG.parent.mkdir(parents=True, exist_ok=True)
PID_FILE = Path("/tmp/aradhya_jarvis.pid")

# Wake-word triggers in English and Gujarati scripts
WAKE_WORDS = [
    "hey aradhya", "hey radhya", "hey aaradhya", "hello aradhya", "hi aradhya",
    "aradhya", "aaradhya", "radhya", "aradhya ji",
    "હે આરાધ્યા", "આરાધ્યા", "ઓ આરાધ્યા", "નમસ્તે આરાધ્યા", "જય માતાજી આરાધ્યા"
]

def log(msg: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [JarvisDaemon] {msg}"
    print(formatted, flush=True)
    try:
        with open(DAEMON_LOG, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

class AradhyaJarvisDaemon:
    def __init__(self):
        self.engine = get_aradhya_engine()
        self.voice = get_voice_engine()
        self.notifier = AradhyaNotifier()
        self.running = True
        self.is_processing = False
        self._lock = threading.Lock()
        
        # Audio parameters
        self.sample_rate = 16000
        self.channels = 1
        self.chunk_duration = 3  # seconds per listening frame
        self.energy_threshold = 400  # RMS threshold for voice activity detection

    def calculate_rms(self, wav_path: Path) -> float:
        """Calculate Root Mean Square (audio energy level) of WAV file."""
        try:
            with wave.open(str(wav_path), 'rb') as wf:
                n_frames = wf.getnframes()
                if n_frames == 0:
                    return 0.0
                raw_data = wf.readframes(n_frames)
                total_samples = len(raw_data) // 2
                if total_samples == 0:
                    return 0.0
                fmt = f"<{total_samples}h"
                samples = struct.unpack(fmt, raw_data)
                sum_sq = sum(s ** 2 for s in samples)
                return math.sqrt(sum_sq / total_samples)
        except Exception as e:
            return 0.0

    def record_chunk(self, wav_path: Path, duration: int = 3) -> bool:
        """Capture microphone audio chunk using arecord."""
        cmd = [
            "arecord",
            "-d", str(duration),
            "-f", "S16_LE",
            "-r", str(self.sample_rate),
            "-c", str(self.channels),
            "-t", "wav",
            str(wav_path)
        ]
        try:
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=duration + 2)
            return res.returncode == 0 and wav_path.exists() and wav_path.stat().st_size > 500
        except Exception:
            return False

    def check_wake_word(self, text: str) -> bool:
        """Check if transcribed speech matches any wake phrase."""
        if not text:
            return False
        clean = text.lower().strip()
        for ww in WAKE_WORDS:
            if ww in clean:
                return True
        return False

    def extract_command(self, text: str) -> str:
        """Extract user's command following the wake word."""
        clean = text.strip()
        for ww in sorted(WAKE_WORDS, key=len, reverse=True):
            pattern = re.compile(re.escape(ww), re.IGNORECASE)
            if pattern.search(clean):
                parts = pattern.split(clean, maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    cmd = parts[1].strip(" ,:.-!?")
                    if len(cmd) > 1:
                        return cmd
        return ""

    def speak_acknowledgement(self):
        """Immediately acknowledge in Gujarati using offline vault or voice synthesis."""
        ack_file = BASE_DIR / "data" / "aradhya_offline_voice_vault" / "hey_aradhya_ack.mp3"
        if ack_file.exists():
            try:
                self.voice._play_audio_file(ack_file, blocking=True)
                return
            except Exception:
                pass
        self.voice.speak("હા અલ્પેશ સાહેબ, બોલો! હું સાંભળી રહી છું.", language="gu", blocking=True)

    def speak_task_done(self):
        """Play task completion voice notification."""
        done_file = BASE_DIR / "data" / "aradhya_offline_voice_vault" / "task_done.mp3"
        if done_file.exists():
            try:
                self.voice._play_audio_file(done_file, blocking=True)
                return
            except Exception:
                pass
        self.voice.speak("અલ્પેશ સાહેબ, આપનો આદેશ સફળતાપૂર્વક પૂર્ણ થઈ ગયો છે અને મેં આપને વ્હોટ્સએપ પર પણ જાણ કરી દીધી છે.", language="gu", blocking=True)

    def handle_wake_interaction(self, initial_transcription: str):
        """Full interaction flow: Wake -> Acknowledge -> Command -> Execute -> Speak & WhatsApp Notify."""
        with self._lock:
            self.is_processing = True

        try:
            log("⚡ Wake Word Detected! Acknowledging Alpesh Sir...")
            self.speak_acknowledgement()

            # Check if command was spoken in the same utterance as the wake word
            command = self.extract_command(initial_transcription)

            if not command:
                log("🎙️ Listening for Alpesh Sir's direct command (6s)...")
                cmd_wav = Path("/tmp/aradhya_jarvis_cmd.wav")
                if self.record_chunk(cmd_wav, duration=6):
                    trans_res = self.voice.transcribe_audio(cmd_wav)
                    if trans_res.get("success"):
                        command = trans_res.get("transcribed_text", "").strip()

            if not command:
                log("⚠️ No actionable command captured. Returning to standby.")
                self.voice.speak("અલ્પેશ સાહેબ, આપનો અવાજ સ્પષ્ટ ન મળ્યો. આપ ફરીથી 'Hey Aradhya' કહી શકો છો.", language="gu", blocking=False)
                return

            log(f"🎯 Executing Command from Alpesh Sir: \"{command}\"")

            # Execute command using Aradhya's Autonomous Engine
            res = self.engine.process_command(command, sender="jarvis_voice", speak_response=False)
            resp_gu = res.get("response_gu", "")
            resp_en = res.get("response_en", "")

            # Speak result back in Gujarati
            log("🔊 Speaking response in Gujarati...")
            self.voice.speak(resp_gu or resp_en, language="gu", blocking=True)

            # Play completion notification & dispatch WhatsApp report
            self.speak_task_done()
            log("📱 Dispatching Task Completion Notification to WhatsApp and Desktop...")
            
            summary_details = f"Command: {command}\n\nOutcome (Gujarati):\n{resp_gu[:400]}"
            self.notifier.notify_work_done(
                task_name=command,
                details=summary_details,
                solution="કાર્ય ૧૦૦% સફળતાપૂર્વક પૂર્ણ થયેલ છે. કોઈ વધુ આદેશ હોય તો 'Hey Aradhya' બોલો."
            )
            log("✅ Real-Time Jarvis Task Completed & WhatsApp Notification Dispatched!")

        except Exception as e:
            log(f"❌ Error during Jarvis command execution: {e}")
            self.notifier.notify_task_failure(
                task_name=command or "Voice Command",
                error_details=str(e),
                solution="ટર્મિનલમાં 'aradhya' રન કરી વિગતવાર સ્ટેટસ ચકાસો."
            )
        finally:
            with self._lock:
                self.is_processing = False

    def run(self):
        log("👑 Aradhya Real-Time Jarvis Wake-Word Daemon Initiated.")
        log(f"👂 Listening continuously for wake words: {', '.join(WAKE_WORDS[:4])}...")
        
        # Write PID file
        try:
            PID_FILE.write_text(str(os.getpid()))
        except Exception:
            pass

        chunk_path = Path("/tmp/aradhya_wake_chunk.wav")

        while self.running:
            if self.is_processing:
                time.sleep(0.5)
                continue

            # Record a sliding 3-second audio chunk
            rec_ok = self.record_chunk(chunk_path, duration=self.chunk_duration)
            if not rec_ok:
                time.sleep(0.2)
                continue

            # Quick Energy / VAD check
            rms = self.calculate_rms(chunk_path)
            if rms < self.energy_threshold:
                # Silence or ambient noise, continue listening
                time.sleep(0.1)
                continue

            # Audio has speech energy -> transcribe
            trans = self.voice.transcribe_audio(chunk_path)
            if not trans.get("success"):
                time.sleep(0.2)
                continue

            text = trans.get("transcribed_text", "").strip()
            log(f"Audio detected (RMS {int(rms)}): \"{text}\"")

            if self.check_wake_word(text):
                self.handle_wake_interaction(text)

            time.sleep(0.1)

    def stop(self):
        self.running = False
        if PID_FILE.exists():
            try:
                PID_FILE.unlink()
            except Exception:
                pass
        log("Aradhya Real-Time Jarvis Daemon Stopped.")

def main():
    daemon = AradhyaJarvisDaemon()

    def _sig_handler(sig, frame):
        daemon.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    daemon.run()

if __name__ == "__main__":
    main()
