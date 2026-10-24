# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
ARADHYA UNIVERSAL POLYGLOT NLU & MULTILINGUAL ENGINE
Author: Aradhya (CEO), reporting to Alpesh Sir (Founder, Chairman & Master Tech)

Powers Aradhya with 100% Offline Universal Language Comprehension:
1. Script & Language Identification:
   - Indic Scripts: Gujarati, Devanagari (Hindi, Marathi), Tamil, Telugu, etc.
   - World Scripts: Latin (English, Spanish, French, German), Cyrillic, Arabic, CJK.
   - Transliterations: Hinglish (Hindi in Latin script) & Gujlish (Gujarati in Latin script).
2. Omnilingual Intent Normalization across 12+ Core Operational Domains.
3. Multilingual Response Generation with respectful Gujarati honorifics for Alpesh Sir.
"""

import re
import unicodedata
from typing import Dict, Any, List, Optional, Tuple


class AradhyaPolyglotNLU:
    """
    Universal Multilingual Comprehension & Intent Normalization Engine.
    Operates 100% locally with zero cloud dependencies.
    """

    # Unicode Range Signatures
    SCRIPT_RANGES = {
        "gujarati": (0x0A80, 0x0AFF),
        "devanagari": (0x0900, 0x097F),
        "tamil": (0x0B80, 0x0BFF),
        "telugu": (0x0C00, 0x0C7F),
        "arabic": (0x0600, 0x06FF),
        "cyrillic": (0x0400, 0x04FF),
        "cjk": (0x4E00, 0x9FFF),
    }

    # Transliteration Dialect Markers
    HINGLISH_MARKERS = {
        "karo", "kardo", "kijiye", "batao", "dikhao", "chaloo", "band", "kitna",
        "kitni", "hai", "mujhe", "mera", "meri", "chalao", "badhao", "ghatao",
        "hona", "chahiye", "karoge", "lelo", "bhejo", "khojo"
    }

    GUJLISH_MARKERS = {
        "karo", "karjo", "batavo", "aapjo", "aapo", "ketlu", "ketla", "ketli",
        "che", "vadharo", "ghatado", "chaloo", "paado", "sharu", "nathi",
        "tamne", "maru", "mari", "lejo", "moklo", "shodho"
    }

    # Multilingual Concept Dictionaries
    CONCEPT_SYNONYMS = {
        "BATTERY": [
            "battery", "batterie", "batería", "bateria", "akku", "batterij",
            "بنزين", "بطارية", "電池", "电池", "배터리",
            "બેટરી", "ચાર્જ", "ચાર્જિંગ", "પાવર",
            "बैटरी", "चार्ज", "चार्जिंग", "पावर", "ऊर्जा"
        ],
        "VOLUME": [
            "volume", "sound", "audio", "loudness", "volumen", "lautstärke", "son",
            "suono", "音量", "صوت", "볼륨",
            "અવાજ", "વોલ્યુમ", "સાઉન્ડ", "ધીમો", "મોટો",
            "आवाज", "ध्वनि", "वॉल्यूम", "धीमा", "तेज"
        ],
        "BRIGHTNESS": [
            "brightness", "screen light", "luminosité", "brillo", "helligkeit",
            "luminosità", "brilho", "亮度", "سطوع", "밝기",
            "બ્રાઇટનેસ", "તેજ", "સ્ક્રીન લાઈટ", "પ્રકાશ", "અજવાળું",
            "ब्राइटनेस", "चमक", "रोशनी", "स्क्रीन लाइट", "प्रकाश"
        ],
        "SCREENSHOT": [
            "screenshot", "screen capture", "screengrab", "snapshot", "printscreen",
            "bildschirmfoto", "capture d'écran", "captura de pantalla", "captura",
            "schermopname", "截屏", "截图", "لقطة شاشة", "스크린샷",
            "સ્ક્રીનશોટ", "ફોટો", "સ્ક્રીન કેપ્ચર",
            "स्क्रीनशॉट", "फोटो", "स्क्रीन कैप्चर"
        ],
        "TURBO_SPEED": [
            "turbo", "boost", "speed up", "lag", "sluggish", "slow", "faster", "clean ram",
            "free ram", "accélérer", "acelerar", "beschleunigen", "velocidad",
            "versnellen", "加速", "تسريع", "속도 향상",
            "ટર્બો", "સ્પીડ", "લેગ", "ધીમું", "કચરો સાફ", "ફાસ્ટ", "હેંગ", "ઝડપ",
            "टर्बो", "स्पीड", "लैग", "धीमा", "कचरा साफ", "फास्ट", "हैंग", "रफ्तार", "तेज"
        ],
        "SECURITY_AUDIT": [
            "security", "hacker", "hack", "threat", "audit", "cyber", "firewall", "ports",
            "vulnerability", "sécurité", "seguridad", "sicherheit", "sicurezza",
            "veiligheid", "安全", "أمان", "اختراق", "보안", "해커",
            "સુરક્ષા", "હેકર", "સિક્યુરિટી", "સેફ્ટી", "ઓડિટ", "પોર્ટ", "ફાયરવોલ",
            "सुरक्षा", "हैकर", "सिक्योरिटी", "सेफ्टी", "ऑडिट", "पोर्ट", "फायरवॉल", "खतरा"
        ],
        "LOCKDOWN": [
            "lockdown", "lock screen", "lock laptop", "lock pc", "secure laptop",
            "verrouiller", "bloquear", "sperren", "blocco", "vergrendelen",
            "锁定", "锁屏", "قفل", "잠금",
            "લોક", "લોક કરો", "સ્ક્રીન લોક", "તાળું",
            "लॉक", "लॉक करो", "स्क्रीन लॉक", "ताला"
        ],
        "SELF_GROWTH": [
            "learn", "evolve", "evolution", "growth", "synthesize", "create skill", "create tool",
            "apprendre", "aprender", "lernen", "imparare", "leren",
            "学习", "进化", "تعلم", "تطوير", "학습", "진화",
            "શીખો", "વિકાસ", "નવું શીખો", "નવી સ્કિલ", "સ્કિલ બનાવો", "ટૂલ બનાવો",
            "सीखो", "विकास", "नया सीखो", "नई स्किल", "स्किल बनाओ", "टूल बनाओ", "हुनर"
        ],
        "FILES": [
            "find", "search", "locate", "cat", "view file", "read file",
            "fichier", "archivo", "datei", "file", "document",
            "文件", "搜索", "بحث", "ملف", "파일", "검색",
            "શોધો", "ફાઇલ", "વાંચો", "ડોક્યુમેન્ટ",
            "खोजो", "ढूंढो", "फ़ाइल", "पढ़ो", "दस्तावेज़"
        ],
        "SHELL": [
            "run", "exec", "bash", "shell", "terminal", "command",
            "commande", "comando", "befehl", "opdracht",
            "命令", "运行", "أمر", "تشغيل", "실행", "명령어",
            "કમાન્ડ", "શેલ", "રન", "ચલાવો",
            "कमांड", "शेल", "रन", "चलाओ"
        ],
        "WEB_SEARCH": [
            "search web", "web search", "google", "duckduckgo", "internet search", "online search", "look up online",
            "recherche web", "buscar en la web", "websuche", "ricerca web", "网上搜索", "بحث في الويب", "웹 검색",
            "વેબ સર્ચ", "ઇન્ટરનેટ સર્ચ", "ઓનલાઇન શોધો", "વેબ પર શોધો", "ગુગલ",
            "वेब सर्च", "इंटरनेट सर्च", "ऑनलाइन खोजो", "વેબ પર શોધો", "गूगल"
        ],
        "CONNECTIVITY": [
            "ping", "connectivity", "internet status", "wifi status", "are you online", "online status", "connection",
            "connectivité", "conectividad", "verbindung", "connessione", "网络状态", "حالة الاتصال", "연결 상태",
            "ઇન્ટરનેટ સ્ટેટસ", "ઓનલાઇન છો", "નેટ કનેક્શન", "કનેક્ટિવિટી",
            "इंटरनेट स्टेटस", "ऑनलाइन हो", "नेट कनेक्शन", "कनेक्टिविटी"
        ],
        "AUTONOMOUS_MISSION": [
            "autonomous worker", "independent worker", "create chart", "generate chart", "plot chart",
            "plot sales", "make chart", "make graph", "solve mission", "solve task", "code interpreter",
            "analyze data", "csv analysis", "સ્વાયત્ત કાર્ય", "કામ કરો", "મિશન", "ચાર્ટ બનાવો",
            "ગ્રાફ બનાવો", "વિશ્લેષણ કરો", "કામ પૂરું કરો", "કોડ ઇન્ટરપ્રિટર", "ડેટા એનાલિસિસ"
        ],
        "HARDWARE_DIAGNOSTIC": [
            "camera", "webcam", "inbuilt camera", "mic", "microphone", "speaker",
            "caméra", "cámara", "kamera", "كاميرا", "相机", "카메라",
            "કેમેરા", "વેબકેમ", "માઇક", "માઇક્રોફોન", "અવાજ નથી", "સ્પીકર",
            "कैमरा", "वेबकैम", "माइक", "माइक खराब", "स्पीकर"
        ]
    }

    def __init__(self):
        pass

    # =========================================================================
    # 1. Script & Language Detector
    # =========================================================================

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Identify language script, family, and transliteration dialect.
        Returns: {code, name, script, is_transliteration}
        """
        clean = text.strip()
        if not clean:
            return {"code": "gu", "name": "Gujarati", "script": "gujarati", "is_transliteration": False}

        # Check Unicode Character Blocks
        counts = {k: 0 for k in self.SCRIPT_RANGES}
        latin_count = 0
        total_letters = 0

        for char in clean:
            code_pt = ord(char)
            matched = False
            for script_name, (start_pt, end_pt) in self.SCRIPT_RANGES.items():
                if start_pt <= code_pt <= end_pt:
                    counts[script_name] += 1
                    matched = True
                    break
            if not matched and ('a' <= char.lower() <= 'z'):
                latin_count += 1
            if char.isalpha():
                total_letters += 1

        # Evaluate Non-Latin Scripts First
        for script_name, count in counts.items():
            if count >= 2 or (total_letters > 0 and count / total_letters > 0.3):
                if script_name == "gujarati":
                    return {"code": "gu", "name": "Gujarati", "script": "gujarati", "is_transliteration": False}
                elif script_name == "devanagari":
                    # Distinguish Hindi vs Marathi if markers present
                    if any(w in clean.lower() for w in ["आहे", "करा", "सांगा", "माझे"]):
                        return {"code": "mr", "name": "Marathi", "script": "devanagari", "is_transliteration": False}
                    return {"code": "hi", "name": "Hindi", "script": "devanagari", "is_transliteration": False}
                elif script_name == "tamil":
                    return {"code": "ta", "name": "Tamil", "script": "tamil", "is_transliteration": False}
                elif script_name == "telugu":
                    return {"code": "te", "name": "Telugu", "script": "telugu", "is_transliteration": False}
                elif script_name == "arabic":
                    return {"code": "ar", "name": "Arabic", "script": "arabic", "is_transliteration": False}
                elif script_name == "cyrillic":
                    return {"code": "ru", "name": "Russian", "script": "cyrillic", "is_transliteration": False}
                elif script_name == "cjk":
                    return {"code": "zh", "name": "Chinese", "script": "cjk", "is_transliteration": False}

        # Evaluate Latin Script (English, Hinglish, Gujlish, French, Spanish, German)
        words = set(re.findall(r'[a-zA-Z]+', clean.lower()))

        # Check Gujlish Markers
        if len(words & self.GUJLISH_MARKERS) >= 1:
            return {"code": "gu-latn", "name": "Gujlish (Gujarati in English letters)", "script": "latin", "is_transliteration": True}

        # Check Hinglish Markers
        if len(words & self.HINGLISH_MARKERS) >= 1:
            return {"code": "hi-latn", "name": "Hinglish (Hindi in English letters)", "script": "latin", "is_transliteration": True}

        # Check European Languages
        if any(w in words for w in ["est", "le", "la", "de", "du", "pourquoi", "quel", "quelle", "batterie"]):
            return {"code": "fr", "name": "French", "script": "latin", "is_transliteration": False}
        if any(w in words for w in ["es", "el", "la", "por", "qué", "que", "pantalla", "batería", "sonido"]):
            return {"code": "es", "name": "Spanish", "script": "latin", "is_transliteration": False}
        if any(w in words for w in ["ist", "der", "die", "das", "lautstärke", "akku", "schnell", "bitte"]):
            return {"code": "de", "name": "German", "script": "latin", "is_transliteration": False}

        # Default to English
        return {"code": "en", "name": "English", "script": "latin", "is_transliteration": False}

    # =========================================================================
    # 2. Universal Concept & Intent Normalization
    # =========================================================================

    def normalize_intent(self, text: str) -> Dict[str, Any]:
        """
        Normalize raw multilingual input into a standard operational intent:
        Returns: {intent, confidence, detected_language, extracted_args}
        """
        clean = text.strip()
        lang_info = self.detect_language(clean)
        lower_text = clean.lower()

        matched_intent = "GENERAL_EXECUTIVE"
        matched_concept = None

        # Check all concept dictionaries
        for intent_name, keywords in self.CONCEPT_SYNONYMS.items():
            for kw in keywords:
                # Word boundary or substring check
                if kw in lower_text:
                    matched_intent = intent_name
                    matched_concept = kw
                    break
            if matched_concept:
                break

        # Specific Overrides for Nuances
        if matched_intent == "BATTERY":
            pass
        elif matched_intent == "VOLUME":
            if any(w in lower_text for w in ["mute", "unmute", "મ્યૂટ", "म्यूट"]):
                matched_intent = "VOLUME_MUTE"
            elif any(w in lower_text for w in ["up", "high", "louder", "vadharo", "badhao", "વધારો", "बढ़ाओ"]):
                matched_intent = "VOLUME_UP"
            elif any(w in lower_text for w in ["down", "low", "quieter", "ghatado", "ghatao", "ઘટાડો", "घटाओ"]):
                matched_intent = "VOLUME_DOWN"
        elif matched_intent == "BRIGHTNESS":
            if any(w in lower_text for w in ["up", "high", "vadharo", "badhao", "વધારો", "बढ़ाओ"]):
                matched_intent = "BRIGHTNESS_UP"
            elif any(w in lower_text for w in ["down", "low", "ghatado", "ghatao", "ઘટાડો", "घटाओ"]):
                matched_intent = "BRIGHTNESS_DOWN"

        return {
            "intent": matched_intent,
            "detected_language": lang_info,
            "raw_text": clean,
            "matched_keyword": matched_concept
        }

    # =========================================================================
    # 3. Multilingual Greeting & Response Formatter
    # =========================================================================

    def format_honorific_greeting(self, lang_code: str) -> str:
        """Provide respectful honorifics tailored to language family."""
        if lang_code in ("gu", "gu-latn"):
            return "જય માતાજી અલ્પેશ સાહેબ! હું આરાધ્યા (CEO & Supreme AI Orchestrator)."
        elif lang_code in ("hi", "hi-latn"):
            return "प्रणाम अल्पेश सर! मैं आराध्या (CEO & Supreme AI Orchestrator) उपस्थित हूँ।"
        elif lang_code == "mr":
            return "नमस्कार अल्पेश साहेब! मी आराध्या (CEO & Supreme AI Orchestrator) सज्ज आहे."
        elif lang_code == "ta":
            return "வணக்கம் அல்பேஷ் சார்! நான் ஆராத்யா (CEO & Supreme AI Orchestrator)."
        elif lang_code == "fr":
            return "Salutations respectueuses Monsieur Alpesh ! Ici Aradhya (CEO & Supreme AI Orchestrator)."
        elif lang_code == "es":
            return "¡Saludos respetuosos Señor Alpesh! Aradhya (CEO & Supreme AI Orchestrator) a sus órdenes."
        elif lang_code == "de":
            return "Herzliche Grüße Herr Alpesh! Aradhya (CEO & Supreme AI Orchestrator) meldet sich zum Dienst."
        elif lang_code == "ar":
            return "تحياتي سيدي ألبش! أنا أراديا (الرئيس التنفيذي والمنسق الأعلى للذكاء الاصطناعي)."
        elif lang_code == "ru":
            return "Приветствую, господин Альпеш! Арадхья (CEO & Supreme AI Orchestrator) готова к работе."
        elif lang_code == "zh":
            return "向您致敬，阿尔佩什先生！我是阿拉迪亚（CEO兼最高AI指挥官）。"
        else:
            return "Greetings Alpesh Sir! Aradhya (CEO & Supreme AI Orchestrator) standing by."


_polyglot_instance: Optional[AradhyaPolyglotNLU] = None

def get_polyglot_nlu() -> AradhyaPolyglotNLU:
    global _polyglot_instance
    if _polyglot_instance is None:
        _polyglot_instance = AradhyaPolyglotNLU()
    return _polyglot_instance
