#!/usr/bin/env python3
"""
Chamunda Automobile Parts & Service - Royal Enfield Live Sound Diagnostic CLI Tool.
Analyzes motorcycle engine acoustics, detects mechanical faults, and recommends genuine OEM parts.

Usage:
    python3 diagnose_sound_cli.py --model "Hunter 350" --record 5
    python3 diagnose_sound_cli.py --model "Classic 350" --file /path/to/engine.wav
    python3 diagnose_sound_cli.py --model "Continental GT 650" --simulate chain
    python3 diagnose_sound_cli.py --model "Himalayan 450" --simulate healthy --json
"""

import sys
import json
import argparse
from pathlib import Path

# Ensure chamunda_re_enterprise is in path
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from acoustic_sound_diagnostic import ChamundaSoundDiagnosticEngine, FAULT_PROFILES


SIMULATION_MAP = {
    "tappet": "tappet_valve_noise",
    "chain": "timing_chain_slack",
    "timing": "timing_chain_slack",
    "clutch": "clutch_primary_whine",
    "piston": "piston_slap_knock",
    "exhaust": "exhaust_leak_turbulence",
    "healthy": None,
    "none": None
}


def print_banner():
    print("=" * 78)
    print("🏍️  CHAMUNDA AUTOMOBILE • ROYAL ENFIELD LIVE SOUND DIAGNOSTIC AI")
    print("    Fast Fourier Transform (FFT) Harmonics & 4,469 Parts Catalog Engine")
    print("=" * 78)


def format_report_terminal(rep: dict):
    print(f"\n📋 DIAGNOSTIC REPORT: {rep['diagnostic_id']}")
    print(f"⏰ Timestamp: {rep['timestamp']} | Source: {rep['audio_source']}")
    print(f"🏍️  Motorcycle: {rep['bike_model']}")
    print(f"📊 Telemetry: Idle Rhythm {rep['dominant_freq_hz']} Hz | Sound Level: {rep['estimated_db']} dB | Sample: {rep['duration_sec']}s")
    print("-" * 78)

    # Health score banner
    score = rep['health_score']
    if score >= 90:
        badge = f"\033[92m● HEALTH SCORE: {score}/100 [{rep['health_status']}]\033[0m"
    elif score >= 70:
        badge = f"\033[93m● HEALTH SCORE: {score}/100 [{rep['health_status']}]\033[0m"
    else:
        badge = f"\033[91m● HEALTH SCORE: {score}/100 [{rep['health_status']}]\033[0m"
    print(f"\n{badge}")
    print(f"📝 સારાંશ (Gujarati): {rep['summary_gu']}\n")

    anomalies = rep.get("anomalies_detected", [])
    if not anomalies:
        print("✅ NO MECHANICAL ANOMALIES DETECTED.")
        print("   All harmonic frequencies (tappets, cam chain, clutch, exhaust) are within factory tolerances.")
        print("=" * 78 + "\n")
        return

    print("⚠️  MECHANICAL ANOMALIES IDENTIFIED:")
    for idx, anom in enumerate(anomalies, 1):
        print(f"  {idx}. [{anom['fault_id']}] {anom['title']} ({anom['title_gu']})")
        print(f"     • Severity: {anom['severity']} | Confidence: {anom['confidence_pct']}%")
        print(f"     • Root Cause: {anom['root_cause']}")
        print(f"     • Action: {anom['recommended_action']}")

    recs = rep.get("parts_recommendations", [])
    if recs:
        print("\n🔧 RECOMMENDED GENUINE OEM SPARE PARTS (from 4,469 Parts Catalog):")
        print("-" * 78)
        print(f"{'OEM Part Number':<18} | {'Part Description':<28} | {'MRP (₹)':<8} | {'Stock':<6} | {'Bin':<8}")
        print("-" * 78)
        for r in recs:
            for p in r.get("matched_oem_parts", []):
                p_no = str(p.get("part_number", "N/A"))[:18]
                p_name = str(p.get("name", "N/A"))[:28]
                p_mrp = f"₹{p.get('mrp', 0)}"
                p_stock = f"{p.get('stock', 0)} Pcs"
                p_bin = str(p.get("bin_location", "A-01"))[:8]
                print(f"{p_no:<18} | {p_name:<28} | {p_mrp:<8} | {p_stock:<6} | {p_bin:<8}")
        print("-" * 78)

    print("=" * 78 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Royal Enfield Live Sound Diagnostic CLI Tool")
    parser.add_argument("--model", type=str, default="Classic 350", help="Motorcycle model (e.g. 'Hunter 350', 'Classic 350', 'Interceptor 650', 'Himalayan 450')")
    parser.add_argument("--file", type=str, default=None, help="Path to input audio WAV file")
    parser.add_argument("--record", type=int, default=None, help="Record audio live from microphone for N seconds (e.g. 5)")
    parser.add_argument("--simulate", type=str, default=None, choices=["tappet", "chain", "clutch", "piston", "exhaust", "healthy"], help="Simulate calibrated anomaly wave")
    parser.add_argument("--json", action="store_true", help="Output raw JSON data")

    args = parser.parse_args()

    engine = ChamundaSoundDiagnosticEngine()

    sim_anomaly = SIMULATION_MAP.get(args.simulate) if args.simulate else None
    rec_sec = args.record if args.record is not None else 5

    if not args.json:
        print_banner()
        if args.record:
            print(f"🎙️  Listening to {args.model} engine idle sound for {rec_sec} seconds...")
        elif args.file:
            print(f"📂 Analyzing audio file: {args.file} for {args.model}...")
        elif args.simulate:
            print(f"🧪 Running calibrated simulation for [{args.simulate}] on {args.model}...")
        else:
            print(f"🎙️  Starting 5-second acoustic analysis for {args.model}...")

    rep = engine.diagnose_engine_sound(
        bike_model=args.model,
        audio_path=args.file,
        record_seconds=rec_sec,
        inject_simulation=sim_anomaly
    )

    if args.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False))
    else:
        format_report_terminal(rep)


if __name__ == "__main__":
    main()
