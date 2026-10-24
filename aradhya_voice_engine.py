# -*- coding: utf-8 -*-
"""
Aradhya Voice & Speech Interaction Engine (આરાધ્યા - વૉઇસ & વાણી એન્જિન)
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Provides Dual-Mode Speech Synthesis (TTS) and Voice Recognition (STT):
1. Online Neural TTS:
   - Microsoft Edge Neural TTS (gu-IN-DhwaniNeural, en-IN-NeerjaExpressiveNeural, hi-IN-SwaraNeural)
   - Lifelike human voice output played via pygame.mixer through laptop speakers.
2. 100% Offline Local TTS:
   - Linux Speech Dispatcher (spd-say) with native Gujarati & English voices.
   - Zero internet required.
3. Voice Recording & Recognition (STT):
   - Captures microphone audio via arecord to WAV.
   - Transcribes via Google Gemini Multimodal Audio (gemini-3.5-flash) when online.
4. Project Chhaya Web Streaming:
   - Generates static MP3s accessible at /static/voice_cache/<hash>.mp3 for mobile browser playback.
"""

import os
import sys
import re
import time
import socket
import hashlib
import asyncio
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import pygame

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
VOICE_CACHE_DIR = DATA_DIR / "aradhya_voice_cache"
STATIC_VOICE_DIR = BASE_DIR / "static" / "voice_cache"
OFFLINE_VAULT_DIR = DATA_DIR / "aradhya_offline_voice_vault"

VOICE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATIC_VOICE_DIR.mkdir(parents=True, exist_ok=True)
OFFLINE_VAULT_DIR.mkdir(parents=True, exist_ok=True)

VOICE_MODELS = {
    "gu": "gu-IN-DhwaniNeural",            # Gujarati Female
    "gu-male": "gu-IN-NiranjanNeural",      # Gujarati Male
    "en": "en-IN-NeerjaExpressiveNeural",  # Indian English Female Expressive
    "en-male": "en-IN-PrabhatNeural",      # Indian English Male
    "hi": "hi-IN-SwaraNeural",             # Hindi Female
    "hi-male": "hi-IN-MadhurNeural"        # Hindi Male
}

# Pre-rendered 100% Offline Real Girl Voice Vault Clips
VAULT_CLIPS = {
    "startup_online": {
        "text": "જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા. લેપટોપ સિસ્ટમ સફળતાપૂર્વક ઓનલાઇન થઈ ગઈ છે. તમામ કંટ્રોલ સક્રિય છે, અને હું આપના આદેશ માટે તૈયાર છું!",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["લેપટોપ સિસ્ટમ સફળતાપૂર્વક ઓનલાઇન થઈ ગઈ છે", "startup_online"]
    },
    "startup_offline": {
        "text": "જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા. લેપટોપ ઓફલાઇન એર-ગેપ્ડ ડિફેન્સ મોડમાં સક્રિય છે. ૧૦૦% ઓફલાઇન કંટ્રોલ સક્રિય છે, અને હું આપના આદેશ માટે તૈયાર છું!",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["ઓફલાઇન એર-ગેપ્ડ ડિફેન્સ મોડમાં સક્રિય છે", "startup_offline"]
    },
    "battery_good": {
        "text": "પ્રણામ અલ્પેશ સાહેબ! લેપટોપ બેટરી એકદમ સ્વસ્થ છે, અને પાવર મેનેજમેન્ટ ૧૦૦% ઓપ્ટિમાઇઝ્ડ છે.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["લેપટોપ બેટરી એકદમ સ્વસ્થ છે", "battery_good"]
    },
    "battery_low": {
        "text": "ચેતવણી અલ્પેશ સાહેબ! લેપટોપ બેટરી ઓછી થઈ રહી છે. કૃપા કરીને ચાર્જર કનેક્ટ કરો.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["બેટરી ઓછી", "battery_low", "ચાર્જર કનેક્ટ"]
    },
    "turbo_boost": {
        "text": "પ્રણામ અલ્પેશ સાહેબ! લેપટોપ ટર્બો બૂસ્ટ અને લેગ-બસ્ટર સફળતાપૂર્વક પૂર્ણ થઈ ગયું છે. સિસ્ટમ હવે એકદમ સ્મૂધ અને સુપરફાસ્ટ છે.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["ટર્બો બૂસ્ટ", "turbo_boost", "લેગ-બસ્ટર", "સુપરફાસ્ટ"]
    },
    "lockdown": {
        "text": "પ્રણામ અલ્પેશ સાહેબ! ઇમરજન્સી લોકડાઉન સક્રિય કરી દેવામાં આવ્યું છે. સ્ક્રીન લૉક થઈ ગઈ છે.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["ઇમરજન્સી લોકડાઉન સક્રિય", "lockdown", "સ્ક્રીન લૉક"]
    },
    "security_safe": {
        "text": "પ્રણામ અલ્પેશ સાહેબ! તમામ સુરક્ષા ચકાસણી પૂર્ણ થઈ છે. લેપટોપ સંપૂર્ણપણે સુરક્ષિત છે.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["તમામ સુરક્ષા ચકાસણી પૂર્ણ થઈ છે", "security_safe", "સંપૂર્ણપણે સુરક્ષિત"]
    },
    "acknowledged": {
        "text": "હા અલ્પેશ સાહેબ, આપનો આદેશ સ્વીકાર્યો છે અને હું તેના પર કામ કરી રહી છું.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["આદેશ સ્વીકાર્યો છે", "acknowledged", "કામ કરી રહી છું"]
    },
    "voice_mode_on": {
        "text": "જય માતાજી અલ્પેશ સાહેબ! વૉઇસ મોડ સક્રિય થઈ ગયો છે. હવે હું આપની સાથે બોલીને વાત કરીશ.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["વૉઇસ મોડ સક્રિય થઈ ગયો છે", "voice_mode_on", "બોલીને વાત કરીશ"]
    },
    "greeting": {
        "text": "જય માતાજી અલ્પેશ સાહેબ! આપનો દિવસ શુભ રહે. હું આપની શું સેવા કરી શકું?",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["આપનો દિવસ શુભ રહે", "greeting", "સેવા કરી શકું"]
    },
    "task_completed": {
        "text": "અલ્પેશ સાહેબ, આપનો ટાસ્ક સફળતાપૂર્વક પૂર્ણ થઈ ગયો છે.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["ટાસ્ક સફળતાપૂર્વક પૂર્ણ થઈ ગયો છે", "task_completed"]
    },
    "help": {
        "text": "હા અલ્પેશ સાહેબ, હું આપના સમગ્ર લેપટોપને નિયંત્રિત કરી શકું છું, ફાઇલો જોઈ શકું છું અને સિસ્ટમ કંટ્રોલ કરી શકું છું.",
        "voice": "gu-IN-DhwaniNeural",
        "keywords": ["સમગ્ર લેપટોપને નિયંત્રિત", "help", "સિસ્ટમ કંટ્રોલ"]
    }
}


class AradhyaVoiceEngine:
    """
    JARVIS / EDITH / FRIDAY Style Speech Interaction Engine for Aradhya.
    Operates seamlessly both online (neural TTS) and offline (spd-say).
    """

    def __init__(self):
        self._pygame_initialized = False
        self._init_pygame_mixer()
        self._is_speaking = False
        self._speak_lock = threading.Lock()

    def _init_pygame_mixer(self):
        """Initialize pygame mixer for audio playback."""
        if not self._pygame_initialized:
            try:
                pygame.mixer.init()
                self._pygame_initialized = True
            except Exception as e:
                pass

    def check_internet(self) -> bool:
        """Fast socket probe (0.25s) to verify active internet connectivity."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.25)
            s.connect(("1.1.1.1", 53))
            s.close()
            return True
        except Exception:
            return False

    def clean_text_for_speech(self, text: str) -> str:
        """
        Strip markdown formatting, emojis, shell blocks, and URLs so speech is natural.
        """
        if not text:
            return ""

        # Remove code blocks
        clean = re.sub(r'```[\s\S]*?```', '', text)
        # Remove inline backticks
        clean = re.sub(r'`([^`]+)`', r'\1', clean)
        # Remove URLs
        clean = re.sub(r'https?://\S+', '', clean)
        # Remove markdown headers and bullets
        clean = re.sub(r'^[#*•\->\s]+', '', clean, flags=re.MULTILINE)
        # Remove bold/italic markers
        clean = re.sub(r'[*_~]', '', clean)
        # Remove excessive punctuation or symbols
        clean = re.sub(r'[-─═━┌┐└┘├┤│]{2,}', '', clean)
        # Clean extra whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()

        # Limit spoken text to first 300 words for voice clarity
        words = clean.split()
        if len(words) > 300:
            clean = " ".join(words[:300]) + "..."

        return clean

    def detect_speech_language(self, text: str) -> str:
        """Determine whether text is primarily Gujarati, Hindi, or English."""
        gu_chars = len(re.findall(r'[઀-૿]', text))
        hi_chars = len(re.findall(r'[ऀ-ॿ]', text))

        if gu_chars > 3:
            return "gu"
        elif hi_chars > 3:
            return "hi"
        return "en"

    def _play_audio_file(self, file_path: Path, blocking: bool = False):
        """Play audio file via pygame mixer."""
        def _worker():
            with self._speak_lock:
                self._is_speaking = True
                try:
                    self._init_pygame_mixer()
                    pygame.mixer.music.load(str(file_path))
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                except Exception as e:
                    pass
                finally:
                    self._is_speaking = False

        if blocking:
            _worker()
        else:
            t = threading.Thread(target=_worker, daemon=True)
            t.start()

    def speak_offline(self, clean_text: str, language: str = "gu") -> Dict[str, Any]:
        """
        100% Offline Speech Synthesis using Linux Speech Dispatcher (spd-say)
        with feminine acoustic prosody.
        Works with zero internet connection.
        """
        lang_code = "gu" if language.startswith("gu") else ("hi" if language.startswith("hi") else "en")
        try:
            # Escape text for shell
            safe_text = clean_text.replace('"', '\\"').replace('$', r'\$')
            cmd = ["spd-say", "-l", lang_code, "-t", "female1", "-p", "22", "-R", "18", "-r", "-8", safe_text]
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {
                "success": True,
                "mode": "OFFLINE_SPD_SAY",
                "engine": "Speech Dispatcher (Feminine Acoustics, 100% Offline)",
                "language": lang_code,
                "text": clean_text[:100]
            }
        except Exception as e:
            return {
                "success": False,
                "mode": "OFFLINE_SPD_SAY",
                "error": str(e)
            }

    async def _generate_edge_tts(self, text: str, voice: str, output_path: Path, pitch: str = "+3Hz", rate: str = "+0%"):
        """Internal async call to edge_tts with fine-tuned natural feminine pitch & rate."""
        import edge_tts
        comm = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate)
        await comm.save(str(output_path))

    def find_vault_clip(self, text: str) -> Optional[Tuple[str, Path]]:
        """
        Check if text corresponds to a pre-rendered offline neural voice vault clip.
        Returns (clip_name, mp3_path) if found.
        """
        text_clean = text.strip()
        text_lower = text_clean.lower()
        norm_key = re.sub(r'[\s_\-]+', '', text_lower)

        # 1. Direct clip key name match (e.g. "startup_offline", "battery_good")
        for name in VAULT_CLIPS:
            if norm_key == re.sub(r'[\s_\-]+', '', name.lower()):
                vault_file = OFFLINE_VAULT_DIR / f"{name}.mp3"
                if vault_file.exists():
                    return name, vault_file

        # 2. Text or keyword match
        for name, data in VAULT_CLIPS.items():
            vault_file = OFFLINE_VAULT_DIR / f"{name}.mp3"
            if not vault_file.exists():
                continue

            # Exact or substring match
            if data["text"] in text_clean or text_clean in data["text"]:
                return name, vault_file

            # Keyword match
            for kw in data.get("keywords", []):
                if kw.lower() in text_lower:
                    return name, vault_file
        return None

    def pre_render_offline_vault(self, force: bool = False) -> Dict[str, Any]:
        """
        Pre-render high-definition female neural MP3 clips for the Offline Voice Vault.
        Renders clips using gu-IN-DhwaniNeural with feminine pitch tuning.
        """
        rendered = []
        errors = []
        for name, data in VAULT_CLIPS.items():
            out_file = OFFLINE_VAULT_DIR / f"{name}.mp3"
            if out_file.exists() and not force:
                rendered.append(name)
                continue

            try:
                asyncio.run(self._generate_edge_tts(data["text"], data["voice"], out_file, pitch="+3Hz", rate="+0%"))
                rendered.append(name)
            except Exception as e:
                errors.append({"clip": name, "error": str(e)})

        return {
            "success": len(errors) == 0,
            "vault_dir": str(OFFLINE_VAULT_DIR),
            "rendered_count": len(rendered),
            "rendered": rendered,
            "errors": errors
        }

    def speak(
        self,
        text: str,
        language: str = "auto",
        blocking: bool = False,
        force_offline: bool = False,
        voice_gender: str = "female"
    ) -> Dict[str, Any]:
        """
        Master speech method for Real Girl Voice interaction.
        If online: Uses ultra-realistic neural TTS (edge_tts) played via pygame.mixer.
        If offline: Plays from pre-rendered Neural Voice Vault or local neural cache,
                    falling back to feminine-tuned Speech Dispatcher (spd-say).
        """
        clean = self.clean_text_for_speech(text)
        if not clean:
            return {"success": False, "error": "No speakable text provided."}

        lang = self.detect_speech_language(clean) if language == "auto" else language
        vault_match = self.find_vault_clip(clean)
        is_online = self.check_internet() and not force_offline

        if is_online:
            voice_key = f"{lang}-male" if voice_gender == "male" else lang
            voice_name = VOICE_MODELS.get(voice_key, VOICE_MODELS.get(lang, "gu-IN-DhwaniNeural"))

            # Hash text and voice for cache key
            cache_key = hashlib.md5(f"{voice_name}:{clean}".encode("utf-8")).hexdigest()
            cache_file = VOICE_CACHE_DIR / f"{cache_key}.mp3"
            static_file = STATIC_VOICE_DIR / f"{cache_key}.mp3"

            if not cache_file.exists():
                try:
                    asyncio.run(self._generate_edge_tts(clean, voice_name, cache_file, pitch="+3Hz", rate="+0%"))
                    # Copy to static dir for mobile web streaming
                    if cache_file.exists():
                        import shutil
                        shutil.copy2(cache_file, static_file)
                except Exception as e:
                    # Fall back instantly to offline vault or spd-say if online generation fails
                    if vault_match:
                        clip_name, vault_file = vault_match
                        self._play_audio_file(vault_file, blocking=blocking)
                        return {
                            "success": True,
                            "mode": "OFFLINE_NEURAL_VAULT",
                            "engine": f"Pre-Rendered Neural Vault ({clip_name})",
                            "voice": "gu-IN-DhwaniNeural (Offline Real Girl Voice)",
                            "audio_file": str(vault_file),
                            "language": lang,
                            "text": clean[:100]
                        }
                    return self.speak_offline(clean, language=lang)

            if cache_file.exists():
                self._play_audio_file(cache_file, blocking=blocking)
                return {
                    "success": True,
                    "mode": "ONLINE_NEURAL_EDGE",
                    "engine": f"Neural TTS ({voice_name})",
                    "voice": voice_name,
                    "audio_file": str(cache_file),
                    "web_url": f"/static/voice_cache/{cache_key}.mp3",
                    "language": lang,
                    "text": clean[:100]
                }

        # 100% OFFLINE EXECUTION:
        # Check 1: Has this exact prompt already been generated and cached locally?
        for voice_candidate in [VOICE_MODELS.get(lang, "gu-IN-DhwaniNeural"), "gu-IN-DhwaniNeural"]:
            cached_key = hashlib.md5(f"{voice_candidate}:{clean}".encode("utf-8")).hexdigest()
            cached_mp3 = VOICE_CACHE_DIR / f"{cached_key}.mp3"
            if cached_mp3.exists():
                self._play_audio_file(cached_mp3, blocking=blocking)
                return {
                    "success": True,
                    "mode": "OFFLINE_LOCAL_CACHE",
                    "engine": f"Local Neural Audio Cache ({voice_candidate})",
                    "voice": f"{voice_candidate} (Offline Cached Real Girl Voice)",
                    "audio_file": str(cached_mp3),
                    "language": lang,
                    "text": clean[:100]
                }

        # Check 2: Pre-rendered neural voice vault clip (Real Girl Voice guaranteed offline)
        if vault_match:
            clip_name, vault_file = vault_match
            self._play_audio_file(vault_file, blocking=blocking)
            return {
                "success": True,
                "mode": "OFFLINE_NEURAL_VAULT",
                "engine": f"Pre-Rendered Neural Vault ({clip_name})",
                "voice": "gu-IN-DhwaniNeural (Offline Real Girl Voice)",
                "audio_file": str(vault_file),
                "language": lang,
                "text": clean[:100]
            }

        # Check 3: Dynamic speech dispatcher with feminine prosody
        return self.speak_offline(clean, language=lang)

    def stop_speaking(self):
        """Immediately stop any playing speech."""
        try:
            if self._pygame_initialized:
                pygame.mixer.music.stop()
            subprocess.run(["spd-say", "--cancel"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def record_microphone(self, output_wav: Path, duration_seconds: int = 5) -> Dict[str, Any]:
        """
        Record audio from laptop microphone via ALSA arecord.
        """
        output_wav.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "arecord",
            "-d", str(duration_seconds),
            "-f", "cd",
            "-t", "wav",
            str(output_wav)
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=duration_seconds + 3)
            if output_wav.exists() and output_wav.stat().st_size > 1000:
                return {
                    "success": True,
                    "wav_file": str(output_wav),
                    "size_bytes": output_wav.stat().st_size,
                    "duration_seconds": duration_seconds
                }
            return {
                "success": False,
                "error": f"Recording failed or empty file. Stderr: {r.stderr}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def transcribe_audio(self, wav_file: Path) -> Dict[str, Any]:
        """
        Transcribe recorded audio file.
        Uses Google Gemini Multimodal Audio (gemini-3.5-flash) when online.
        """
        if not wav_file.exists():
            return {"success": False, "error": "Audio file does not exist."}

        if not self.check_internet():
            return {
                "success": False,
                "error": "Offline Mode: Gemini audio transcription requires internet connectivity."
            }

        try:
            from google import genai
            from google.genai import types
            from chamunda_llm_engine import get_api_key_pool

            pool = get_api_key_pool()
            candidate_keys = pool.get_candidate_keys()
            if not candidate_keys:
                return {"success": False, "error": "No API keys configured."}

            audio_bytes = wav_file.read_bytes()
            prompt = """
Listen to this audio command from Alpesh Sir.
Transcribe the user's spoken words verbatim.
The language is likely Gujarati, Hindi, or Indian English.
Return ONLY the transcribed text. Do not add explanations or quotes.
"""
            models_to_try = ["gemini-3.5-flash-lite", "gemini-3.5-flash"]
            last_e = None

            for key in candidate_keys:
                client = pool.get_client(key)
                if not client:
                    continue

                for model_candidate in models_to_try:
                    if pool.is_model_on_cooldown(key, model_candidate):
                        continue
                    try:
                        response = client.models.generate_content(
                            model=model_candidate,
                            contents=[
                                types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                                prompt
                            ]
                        )
                        text = (response.text or "").strip()
                        if text:
                            return {
                                "success": True,
                                "transcribed_text": text,
                                "model_used": model_candidate
                            }
                    except Exception as e:
                        last_e = e
                        err_s = str(e)
                        if "429" in err_s or "RESOURCE_EXHAUSTED" in err_s or "quota" in err_s.lower():
                            pool.mark_model_exhausted(key, model_candidate, cooldown_seconds=3600)
                        continue

            return {"success": False, "error": f"Audio transcription limit reached: {last_e}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def listen_and_transcribe(self, duration_seconds: int = 5) -> Dict[str, Any]:
        """
        Convenience workflow: Listen to microphone for N seconds and transcribe.
        """
        tmp_wav = Path("/tmp/aradhya_mic_input.wav")
        rec = self.record_microphone(tmp_wav, duration_seconds=duration_seconds)
        if not rec.get("success"):
            return rec

        return self.transcribe_audio(tmp_wav)


_voice_engine: Optional[AradhyaVoiceEngine] = None

def get_voice_engine() -> AradhyaVoiceEngine:
    global _voice_engine
    if _voice_engine is None:
        _voice_engine = AradhyaVoiceEngine()
    return _voice_engine
