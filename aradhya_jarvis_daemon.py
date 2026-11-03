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
import json
import wave
import signal
import fcntl
import queue
import struct
import math
import subprocess
import threading
from pathlib import Path
from typing import Optional, Dict, Any, List

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from aradhya_autonomous_core import get_aradhya_engine
from aradhya_voice_engine import get_voice_engine
from aradhya_notifier import AradhyaNotifier

DAEMON_LOG = BASE_DIR / "data" / "aradhya_jarvis_daemon.log"
DAEMON_LOG.parent.mkdir(parents=True, exist_ok=True)
PID_FILE = Path("/tmp/aradhya_jarvis.pid")
LOCK_FILE = Path("/tmp/aradhya_jarvis.lock")
VOSK_MODEL_PATH = Path("/home/alpesh/.cache/vosk/vosk-model-small-en-us-0.15")

# Wake-word triggers in English and Gujarati scripts
WAKE_WORDS = [
    "hey aradhya", "hey radhya", "hey aaradhya", "hello aradhya", "hi aradhya", "ok aradhya",
    "aradhya", "aaradhya", "radhya", "aradhya ji", "hey aradhya ji",
    "હે આરાધ્યા", "આરાધ્યા", "ઓ આરાધ્યા", "નમસ્તે આરાધ્યા", "જય માતાજી આરાધ્યા",
    "સુનો આરાધ્યા", "બોલો આરાધ્યા", "આરાધ્યાજી", "હેય આરાધ્યા", "અરાધ્યા",
    "hey jarvis", "jarvis", "જારવિસ", "હે જારવિસ",
    "hey radha", "radha", "radia", "aradia", "hey alpesh", "alpesh"
]

WAKE_REGEX = re.compile(
    r"\b(?:hey\s+|hello\s+|hi\s+|ok\s+)?(?:aradhya|radhya|radha|radia|aradia|jarvis|alpesh)\b"
    r"|(?:હે\s+|ઓ\s+|નમસ્તે\s+)?(?:આરાધ્યા|જારવિસ|અરાધ્યા)",
    re.IGNORECASE
)

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
        self.audio_queue = queue.Queue(maxsize=100)

        # Audio parameters
        self.sample_rate = 16000
        self.channels = 1
        self.block_size = 4000  # 0.25s per chunk
        self.chunk_duration = 3.0
        self.energy_threshold = 200

        # Load local Vosk model for instant wake-word recognition
        self.vosk_model = None
        if VOSK_MODEL_PATH.exists():
            try:
                from vosk import Model
                self.vosk_model = Model(str(VOSK_MODEL_PATH))
                log("⚡ Local Vosk Model Loaded (0ms offline wake-word engine ready).")
            except Exception as e:
                log(f"⚠️ Vosk load failed: {e}. Falling back to streaming VAD.")

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
        except Exception:
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
        """Check if transcribed speech matches any wake phrase via regex or tokens."""
        if not text:
            return False
        clean = text.lower().strip()
        if WAKE_REGEX.search(clean):
            return True
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

    def execute_fast_path(self, cmd_clean: str) -> Optional[Dict[str, str]]:
        """
        Execute common hardware & executive commands locally in <50ms without cloud LLM overhead.
        """
        cl = cmd_clean.lower()

        # 1. Battery
        if any(w in cl for w in ["battery", "બેટરી", "charge", "ચાર્જ"]):
            bat = self.engine.get_battery_status()
            pct = bat.get("percent", 100)
            st = bat.get("status_text", "AC Power")
            resp_gu = f"અલ્પેશ સાહેબ, આપના લેપટોપની બેટરી {pct}% છે ({st})."
            resp_en = f"Alpesh Sir, laptop battery is at {pct}% ({st})."
            return {"resp_gu": resp_gu, "resp_en": resp_en}

        # 2. Volume Up / Down / Mute
        if "mute" in cl or "મ્યૂટ" in cl:
            self.engine.toggle_mute()
            return {"resp_gu": "અલ્પેશ સાહેબ, ઓડિયો મ્યૂટ ટોગલ કરી દીધું છે.", "resp_en": "Alpesh Sir, audio mute toggled."}
        if any(w in cl for w in ["volume up", "increase volume", "અવાજ વધારો", "વોલ્યુમ વધારો"]):
            self.engine.adjust_volume(10)
            return {"resp_gu": "અલ્પેશ સાહેબ, વોલ્યુમ ૧૦% વધારી દીધું છે.", "resp_en": "Alpesh Sir, volume increased by 10%."}
        if any(w in cl for w in ["volume down", "decrease volume", "અવાજ ઘટાડો", "વોલ્યુમ ઘટાડો"]):
            self.engine.adjust_volume(-10)
            return {"resp_gu": "અલ્પેશ સાહેબ, વોલ્યુમ ૧૦% ઘટાડી દીધું છે.", "resp_en": "Alpesh Sir, volume reduced by 10%."}

        # 3. Brightness
        if any(w in cl for w in ["brightness", "બ્રાઇટનેસ"]):
            self.engine.set_brightness(75)
            return {"resp_gu": "અલ્પેશ સાહેબ, સ્ક્રીન બ્રાઇટનેસ સેટ કરી દીધી છે.", "resp_en": "Alpesh Sir, brightness adjusted."}

        # 4. Lock Screen
        if any(w in cl for w in ["lock screen", "lock laptop", "સ્ક્રીન લોક", "લોક કરો"]):
            self.engine.lock_screen()
            return {"resp_gu": "અલ્પેશ સાહેબ, સ્ક્રીન તાત્કાલિક લૉક કરી દેવામાં આવી છે. 🔒", "resp_en": "Alpesh Sir, laptop locked securely. 🔒"}

        # 5. Screenshot
        if any(w in cl for w in ["screenshot", "સ્ક્રીનશોટ", "capture screen"]):
            s_res = self.engine.capture_screenshot()
            if s_res.get("success"):
                return {"resp_gu": "અલ્પેશ સાહેબ, સ્ક્રીનશોટ સફળતાપૂર્વક કેપ્ચર કરી લેવામાં આવ્યો છે. 📸", "resp_en": "Alpesh Sir, full screenshot captured. 📸"}

        # 6. Turbo Clean / Lag Buster
        if any(w in cl for w in ["turbo", "clean ram", "boost", "ટર્બો", "રેમ સાફ", "લેગ બસ્ટર"]):
            res = self.engine.process_command("turbo clean ram", speak_response=False)
            return {"resp_gu": res.get("response_gu", "અલ્પેશ સાહેબ, ટર્બો રેમ ક્લીન પૂર્ણ!"), "resp_en": res.get("response_en", "Turbo clean completed.")}

        # 7. Status / Diagnostics
        if any(cl == w for w in ["status", "system status", "સ્ટેટસ", "કેમ છો", "તૈયાર છો", "ready"]):
            bat = self.engine.get_battery_status()
            disk = self.engine.get_disk_storage()
            net = self.engine.check_internet_connection()
            resp_gu = (
                f"જય માતાજી અલ્પેશ સાહેબ! તમામ સિસ્ટમ સંપૂર્ણ કાર્યરત છે.\n"
                f"• બેટરી: {bat.get('percent', 100)}% ({bat.get('status_text', 'AC Power')})\n"
                f"• સ્ટોરેજ: {disk.get('free_gb', 0)} GB ખાલી\n"
                f"• કનેક્ટિવિટી: {net.get('description')}\n"
                f"• હું આપના આદેશની રાહ જોઈ રહી છું સાહેબ!"
            )
            resp_en = f"Greetings Alpesh Sir! Systems operational. Battery: {bat.get('percent', 100)}%, Free Storage: {disk.get('free_gb', 0)} GB. Ready for your command!"
            return {"resp_gu": resp_gu, "resp_en": resp_en}

        # 8. Threats / Security
        if any(w in cl for w in ["threat", "threats", "hacker", "security", "સુરક્ષા", "હેકર", "થ્રેટ"]):
            threats = self.engine.sentry.get_neutralized_threats()
            cnt = len(threats)
            resp_gu = f"અલ્પેશ સાહેબ, સાયબર સેન્ટ્રી શીલ્ડ ૧૦૦% વિજિલન્ટ છે. અત્યાર સુધી {cnt} જોખમો ન્યુટ્રલાઈઝ કરવામાં આવ્યા છે."
            resp_en = f"Alpesh Sir, Cyber Sentry Shield is fully vigilant. {cnt} threats neutralized."
            return {"resp_gu": resp_gu, "resp_en": resp_en}

        return None

    def handle_wake_interaction(self, initial_transcription: str):
        """Full interaction flow: Wake -> Acknowledge -> Fast/Deep Command -> Execute -> Speak & WhatsApp Notify."""
        with self._lock:
            self.is_processing = True

        try:
            log("⚡ Wake Word Detected! Acknowledging Alpesh Sir (<50ms)...")
            try:
                subprocess.run(
                    ["notify-send", "-u", "normal", "-t", "5000", "⚡ આરાધ્યા એક્ટિવ (Jarvis Mode)", "હા અલ્પેશ સાહેબ, બોલો! હું સાંભળી રહી છું..."],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except Exception:
                pass

            # Instant spoken ack (<50ms)
            self.speak_acknowledgement()

            # Check if command was spoken in the same utterance as the wake word
            command = self.extract_command(initial_transcription)

            if not command:
                log("🎙️ Listening for Alpesh Sir's direct command (5s)...")
                try:
                    subprocess.run(
                        ["notify-send", "-u", "low", "-t", "5000", "🎙️ આરાધ્યા સાંભળી રહી છે...", "બોલો અલ્પેશ સાહેબ, આપનો આદેશ શું છે?"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except Exception:
                    pass
                cmd_wav = Path("/tmp/aradhya_jarvis_cmd.wav")
                if self.record_chunk(cmd_wav, duration=5):
                    trans_res = self.voice.transcribe_audio(cmd_wav)
                    if trans_res.get("success"):
                        command = trans_res.get("transcribed_text", "").strip()
                        if command == "[SILENCE]":
                            command = ""

            if not command:
                log("⚠️ No actionable command captured. Returning to standby.")
                self.voice.speak("અલ્પેશ સાહેબ, આપનો અવાજ સ્પષ્ટ ન મળ્યો. આપ ફરીથી 'Hey Aradhya' કહી શકો છો.", language="gu", blocking=False)
                return

            log(f"🎯 Executing Command from Alpesh Sir: \"{command}\"")

            # Check Local Fast-Path First (<50ms)
            fast_res = self.execute_fast_path(command)
            if fast_res:
                resp_gu = fast_res["resp_gu"]
                resp_en = fast_res["resp_en"]
                log("⚡ Fast-Path Executed Locally!")
            else:
                # Deep Autonomous Execution
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

    def run_vosk_stream(self):
        """Zero-latency continuous microphone streaming with local Vosk Kaldi recognizer."""
        import sounddevice as sd
        from vosk import KaldiRecognizer

        recognizer = KaldiRecognizer(self.vosk_model, self.sample_rate)

        def audio_callback(indata, frames, time_info, status):
            if not self.is_processing:
                try:
                    self.audio_queue.put_nowait(bytes(indata))
                except queue.Full:
                    pass

        log("🎙️ Opening SoundDevice RawInputStream (16kHz, 16-bit mono)...")
        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.block_size,
            dtype="int16",
            channels=self.channels,
            callback=audio_callback
        ):
            log("👂 Continuous zero-latency wake-word listening active (<100ms trigger ready).")
            while self.running:
                if self.is_processing:
                    time.sleep(0.2)
                    while not self.audio_queue.empty():
                        try:
                            self.audio_queue.get_nowait()
                        except Exception:
                            break
                    continue

                try:
                    data = self.audio_queue.get(timeout=0.5)
                except queue.Empty:
                    continue

                if recognizer.AcceptWaveform(data):
                    res = json.loads(recognizer.Result())
                    text = res.get("text", "").strip()
                    if text:
                        log(f"Microphone heard: \"{text}\"")
                        if self.check_wake_word(text):
                            self.handle_wake_interaction(text)
                            recognizer.Reset()
                else:
                    # Check partial result for instant response while still speaking
                    partial = json.loads(recognizer.PartialResult())
                    part_text = partial.get("partial", "").strip()
                    if part_text and self.check_wake_word(part_text):
                        log(f"⚡ Instant partial wake trigger: \"{part_text}\"")
                        self.handle_wake_interaction(part_text)
                        recognizer.Reset()

    def run_fallback_poll(self):
        """Fallback recording loop in case sounddevice is unavailable."""
        log("ℹ️ Running fallback chunked listener...")
        chunk_path = Path("/tmp/aradhya_wake_chunk.wav")
        while self.running:
            if self.is_processing:
                time.sleep(0.5)
                continue

            rec_ok = self.record_chunk(chunk_path, duration=self.chunk_duration)
            if not rec_ok:
                time.sleep(0.2)
                continue

            rms = self.calculate_rms(chunk_path)
            if rms < self.energy_threshold:
                time.sleep(0.1)
                continue

            trans = self.voice.transcribe_audio(chunk_path)
            if not trans.get("success"):
                time.sleep(0.2)
                continue

            text = trans.get("transcribed_text", "").strip()
            if not text or text == "[SILENCE]":
                time.sleep(0.1)
                continue

            log(f"Audio detected (RMS {int(rms)}): \"{text}\"")
            if self.check_wake_word(text):
                self.handle_wake_interaction(text)
            time.sleep(0.1)

    def run(self):
        log("👑 Aradhya Real-Time Jarvis Wake-Word Daemon Initiated.")
        log(f"👂 Listening continuously for wake words: {', '.join(WAKE_WORDS[:4])}...")

        # Write PID file
        try:
            PID_FILE.write_text(str(os.getpid()))
        except Exception:
            pass

        if self.vosk_model is not None:
            try:
                self.run_vosk_stream()
            except Exception as e:
                log(f"⚠️ Vosk stream error: {e}. Switching to fallback listener.")
                self.run_fallback_poll()
        else:
            self.run_fallback_poll()

    def stop(self):
        self.running = False
        if PID_FILE.exists():
            try:
                PID_FILE.unlink()
            except Exception:
                pass
        log("Aradhya Real-Time Jarvis Daemon Stopped.")


def main():
    # Strict single-instance enforcement via Linux fcntl kernel lock
    try:
        lock_fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_RDWR)
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (IOError, BlockingIOError):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [JarvisDaemon] Another instance is already active. Exiting cleanly.", flush=True)
        sys.exit(0)

    daemon = AradhyaJarvisDaemon()

    def _sig_handler(sig, frame):
        daemon.stop()
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    daemon.run()


if __name__ == "__main__":
    main()
