#!/usr/bin/env bash
# Chamunda Automobile • 1-Click WhatsApp Pairing Wizard
echo "================================================================="
echo "📱 CHAMUNDA AUTOMOBILE • WHATSAPP BOT PAIRING WIZARD"
echo "================================================================="
echo "👉 Opening WhatsApp Web on your screen..."
echo "1. Open WhatsApp on your phone (+91 78747 19139)."
echo "2. Tap Menu (three dots) -> 'Linked Devices' -> 'Link a Device'."
echo "3. Scan the QR code appearing on your screen."
echo "================================================================="
cd /home/alpesh/chamunda_re_enterprise
export DISPLAY="${DISPLAY:-:0}"
python3 whatsapp_web_sender.py --pair
