#!/usr/bin/env python3
"""
Chamunda Automobile Parts & Service - Interactive Royal Enfield Executive AI Agent CLI.
Provides an interactive terminal console for Alpesh Sir (Chairman / CEO) with instant
access to 4,469 parts catalog, FFT sound diagnostics, service bays, predictive CRM,
and natural language conversation in Gujarati and English.
"""

import os
import sys
import time
import socket
import subprocess
from pathlib import Path

# Add paths
BASE_DIR = Path(__file__).resolve().parent
JARVIS_DIR = Path("/home/alpesh/jarvis-agent")

sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(JARVIS_DIR))

from inventory_engine import ChamundaInventoryManager
from service_engine import ChamundaServiceManager
from crm_engine import ChamundaCRMManager
from core.offline_commander import OfflineCommander
from config.settings import JarvisConfig, load_config
from tools.chamunda_ceo_tools import (
    chamunda_lookup_part,
    chamunda_search_parts_filtered,
    chamunda_diagnose_engine_sound,
    chamunda_get_predictive_service_reminders,
    chamunda_generate_wholesale_po,
    chamunda_launch_workshop_portal,
    chamunda_tune_engine_thump,
    chamunda_track_customer_service_status,
    chamunda_create_quick_counter_pos_sale,
    chamunda_inspect_preowned_bike,
    chamunda_evaluate_market_valuation,
    chamunda_audit_expedition_readiness,
    chamunda_build_carry_along_spares_kit,
    chamunda_highway_breakdown_sos_triage,
    chamunda_build_custom_restomod_quote,
    chamunda_calculate_performance_stage_tune,
    chamunda_diagnose_vintage_ci_bullet,
    chamunda_get_social_telemetry,
    chamunda_generate_social_campaign,
    chamunda_publish_social_post,
    chamunda_manage_social_inbox,
    chamunda_manage_google_business_reviews,
    chamunda_list_shop_subagents,
    chamunda_delegate_shop_task,
    chamunda_get_subagents_status,
    chamunda_execute_written_command,
    chamunda_heal_shop_subagent,
    chamunda_get_subagents_growth_telemetry,
    chamunda_process_bay_voice_command,
    chamunda_get_b2b_wholesale_overview,
    chamunda_create_b2b_wholesale_order,
    chamunda_manage_amc_membership,
    chamunda_run_obd_iot_scan,
    chamunda_kiosk_express_checkin,
    chamunda_get_predictive_supply_forecast,
    chamunda_generate_predictive_auto_po,
    chamunda_lookup_3d_engine_schematic,
    chamunda_run_borescope_inspection,
    chamunda_get_multibranch_overview,
    chamunda_transfer_branch_inventory,
)




def is_port_in_use(port: int = 8080) -> bool:
    """Check if TCP port is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def ensure_portal_running() -> str:
    """Ensure FastAPI portal is running in background; start if needed."""
    if is_port_in_use(8080):
        return "🟢 Online (Active on http://127.0.0.1:8080)"

    portal_script = BASE_DIR / "app.py"
    log_dir = BASE_DIR / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "portal.log"

    with open(log_file, "a", encoding="utf-8") as out:
        subprocess.Popen(
            ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"],
            cwd=str(BASE_DIR),
            stdout=out,
            stderr=out,
            start_new_session=True
        )

    # Wait up to 3 seconds for port to open
    for _ in range(15):
        time.sleep(0.2)
        if is_port_in_use(8080):
            return "🟢 Started (Active on http://127.0.0.1:8080)"

    return "🟡 Starting in background..."


def print_banner(portal_status: str, valuation: dict, crm_data: dict):
    print("\033[1;33m" + "=" * 80 + "\033[0m")
    print("\033[1;32m  👑 CHAMUNDA AUTOMOBILE PARTS & SERVICE • ROYAL ENFIELD AI AGENT\033[0m")
    print("\033[1;37m     Executive AI Assistant for Alpesh Sir • Chief Executive Officer (CEO)\033[0m")
    print("\033[1;33m" + "=" * 80 + "\033[0m")
    print(f"  🌐 Workshop Web Portal : {portal_status}")
    print(f"  📦 Genuine OEM SKUs    : \033[1;36m{valuation['total_distinct_skus']:,} Parts\033[0m ({valuation['total_units_in_stock']:,} Pcs in Stock)")
    print(f"  💰 Retail Valuation    : \033[1;32m₹{valuation['mrp_valuation_inr']:,}\033[0m (Wholesale: ₹{valuation['cost_valuation_inr']:,})")
    print(f"  📅 Predictive CRM      : \033[1;31m{crm_data['due_now_count']} Due Now\033[0m | \033[1;33m{crm_data['upcoming_count']} Upcoming\033[0m | {crm_data['total_fleet_tracked']} Fleet Tracked")
    print("\033[1;33m" + "-" * 80 + "\033[0m")
    print("  \033[1;37mQuick Commands:\033[0m")
    print("    [1] 🔍 Search 4,469 Parts Catalog      [4] 📅 Predictive CRM Reminders")
    print("    [2] 🎙️ Live Engine Sound Diagnostic   [5] 📦 Generate Wholesale Stock PO")
    print("    [3] 📋 Service Bay & QR Invoicing      [6] 🌐 Open Web Portal in Browser")
    print("    [7] 🏍️ Iconic Thump Tuner & Directives [8] 💬 24/7 Customer Bot (+91 78747 19139)")
    print("    [9] 🛒 Counter POS & Dynamic UPI QR    [10] 🛡️ Pre-Owned RE Inspection")
    print("    [11] 🏔️ Expedition Audit & Highway SOS  [12] 🏍️ Resto-Mod & Vintage CI Studio")
    print("    [13] 📱 360° Social & Brand Hub        [14] 👥 Executive Sub-Agents")
    print("    [15] 🎙️ Hands-Free Bay Voice Terminal  [16] 📦 B2B Wholesale Spares Hub")
    print("    [17] 🏍️ Riders Club & AMC Pass Manager  [18] 🔌 Live OBD-II IoT ECU Scanner")
    print("    [19] 🖥️ Workshop Smart Lounge Kiosk    [20] 📈 AI Predictive Supply Chain")
    print("    [21] 🧩 3D Engine Schematics & Torque  [22] 🔬 AI Borescope Cylinder Endoscopy")
    print("    [23] 🏢 Multi-Branch Cloud Network     [24] 🚀 System Optimizer & Lag Buster")
    print("    [25] 👁️ WebAR Live Engine Camera Guide [26] 🌙 24/7 Night Highway Emergency Locker")
    print("    [27] ☁️ Cloud Shadow & Offline Mirror  [0] 🚪 Exit Console")
    print("\033[1;33m" + "-" * 80 + "\033[0m")
    print("  💡 \033[3mType any query or instruction in Gujarati or English below.\033[0m\n")


def interactive_loop():
    inv_mgr = ChamundaInventoryManager()
    crm_mgr = ChamundaCRMManager()
    commander = OfflineCommander(config=JarvisConfig(language="gu"))

    portal_status = ensure_portal_running()
    valuation = inv_mgr.get_total_inventory_valuation()
    crm_data = crm_mgr.get_predictive_service_reminders()

    print_banner(portal_status, valuation, crm_data)

    while True:
        try:
            prompt = input("\033[1;32mChamunda AI [Alpesh Sir] > \033[0m").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n\033[1;33mજી સાહેબ, ચામુંડા AI એજન્ટ કન્સોલ પૂર્ણ થયું છે. શુભ દિવસ!\033[0m")
            break

        if not prompt:
            continue

        low = prompt.lower()

        if low in ["0", "exit", "quit", "q", "bye"]:
            print("\n\033[1;33mજી સાહેબ, ચામુંડા AI એજન્ટ કન્સોલ પૂર્ણ થયું છે. શુભ દિવસ!\033[0m")
            break

        if low in ["help", "/help", "?"]:
            print("\n\033[1;36m=== 📖 CHAMUNDA AI COMMAND GUIDE ===\033[0m")
            print("  - Search Parts: '1' or type 'Hunter 350 brake pad', '574050/C', 'oil filter under 500'")
            print("  - Sound Diagnostic: '2' or type 'engine sound test', 'tappet noise Classic 350'")
            print("  - Job Cards & QR Bill: '3' or type 'complete job card JOB-20260908-001'")
            print("  - Service CRM: '4' or type 'સર્વિસ રિમાઇન્ડર બતાવો', 'show service reminders'")
            print("  - Wholesale PO: '5' or type 'પીઓ બનાવો', 'generate wholesale purchase order'")
            print("  - Open Web Portal: '6' or type 'open portal', 'web dashboard'")
            print("  - Pre-Owned Inspection: '10' or type '100 point inspection', 'preowned valuation Classic 350'\n")
            continue

        if low == "1":
            q = input("Enter part name, OEM number, or bike model: ").strip()
            print("\n" + chamunda_lookup_part(q) + "\n")
            continue

        if low == "2":
            print("\nSelect engine sound profile to test:")
            print("  [1] Tappet / Valve Clatter (2.5k - 4.5k Hz)")
            print("  [2] Timing Chain Slack Rattle (1.6k - 2.2k Hz)")
            print("  [3] Clutch / Primary Whine (950 - 1.4k Hz)")
            print("  [4] Piston Slap Knock (450 - 750 Hz)")
            print("  [5] Healthy Showroom Engine (Optimal Thump)")
            choice = input("Option [1-5]: ").strip()
            map_c = {"1": "tappet", "2": "chain", "3": "clutch", "4": "piston", "5": "healthy"}
            sim = map_c.get(choice, "tappet")
            print("\n" + chamunda_diagnose_engine_sound(bike_model="Classic 350", simulate_fault=sim) + "\n")
            continue

        if low == "3":
            res = commander.execute_offline_turn("complete job card")
            print("\n" + res + "\n")
            continue

        if low == "4":
            print("\n" + chamunda_get_predictive_service_reminders() + "\n")
            continue

        if low == "5":
            print("\n" + chamunda_generate_wholesale_po() + "\n")
            continue

        if low == "6":
            ensure_portal_running()
            subprocess.run(["xdg-open", "http://127.0.0.1:8080"], check=False)
            print("\n\033[1;32mWeb portal opened in browser: http://127.0.0.1:8080\033[0m\n")
            continue

        if low == "7":
            print("\nSelect engine thump profile to analyze:")
            print("  [1] Iconic Cast-Iron Heavy Rhythm Chug (ઓથેન્ટિક ડુગ-ડુગ)")
            print("  [2] BS6 J-Series Showroom Balanced Thump (શોરૂમ સ્મૂથ)")
            print("  [3] Classic & Meteor 350 Highway Bass Rumble (હાઇવે રમ્બલ)")
            print("  [4] Himalayan 450 Highland Throaty Growl (શેરપા ગ્રોલ)")
            print("  [5] Interceptor 650 Twin 270° Crossplane Roar (ટ્વિન રોઅર)")
            p_c = input("Option [1-5, default 1]: ").strip()
            map_p = {"1": "deep_vintage_chug", "2": "factory_oem_clean", "3": "cruiser_bass_rumble", "4": "sherpa_highland_growl", "5": "twin_270_crossplane_roar"}
            profile_choice = map_p.get(p_c, "deep_vintage_chug")
            print("\n" + chamunda_tune_engine_thump(bike_model="Classic 350", profile=profile_choice) + "\n")
            continue

        if low == "8":
            print("\n📲 24/7 WhatsApp AI Customer Bot & Live Tracker (+91 78747 19139 | https://wa.me/917874719139)")
            reg_q = input("Enter bike registration no or job card ID [default GJ-01-AB-1234]: ").strip() or "GJ-01-AB-1234"
            print("\n" + chamunda_track_customer_service_status(identifier=reg_q) + "\n")
            continue

        if low == "9":
            part_sku_input = input("Enter part number or SKU (e.g. 574050/C, RAM00008/B) [default 574050/C]: ").strip() or "574050/C"
            c_name = input("Customer Name [default Counter Customer]: ").strip() or "Counter Customer"
            print("\n" + chamunda_create_quick_counter_pos_sale(part_skus=part_sku_input, customer_name=c_name) + "\n")
            continue

        if low in ["10", "[10]"]:
            print("\nSelect Pre-Owned Service:")
            print("  [1] 🛡️ 100-Point Digital Quality Inspection & Shield Certificate")
            print("  [2] 💰 AI Gujarat Fair Market Valuation Calculator")
            sub_c = input("Option [1-2, default 1]: ").strip() or "1"
            if sub_c == "2":
                m_model = input("RE Model [default Classic 350]: ").strip() or "Classic 350"
                m_year = input("Manufacturing Year [default 2022]: ").strip() or "2022"
                m_km = input("Odometer KM [default 18000]: ").strip() or "18000"
                print("\n" + chamunda_evaluate_market_valuation(
                    bike_model=m_model,
                    manufacturing_year=int(m_year),
                    odometer_km=int(m_km)
                ) + "\n")
            else:
                m_model = input("RE Model [default Classic 350]: ").strip() or "Classic 350"
                m_reg = input("Registration No [default GJ-01-RE-2022]: ").strip() or "GJ-01-RE-2022"
                m_owner = input("Owner Name [default Ramesh Patel]: ").strip() or "Ramesh Patel"
                m_year = input("Manufacturing Year [default 2022]: ").strip() or "2022"
                m_km = input("Odometer KM [default 18500]: ").strip() or "18500"
                print("\n" + chamunda_inspect_preowned_bike(
                    customer_name=m_owner,
                    phone="+91 98250 12345",
                    bike_model=m_model,
                    registration_no=m_reg,
                    manufacturing_year=int(m_year),
                    odometer_km=int(m_km)
                ) + "\n")
            continue

        if low in ["11", "[11]"]:
            print("\nSelect Expedition & Touring SOS Service:")
            print("  [1] 🏔️ 48-Point Expedition Pre-Touring Audit & QR Passport")
            print("  [2] 🎒 Build Carry-Along Backup Spares Kit (From 4,469 Parts)")
            print("  [3] 🚨 24/7 Gujarat Highway Breakdown SOS Roadside Triage")
            sub_c = input("Option [1-3, default 1]: ").strip() or "1"
            if sub_c == "2":
                m_model = input("RE Model [default Himalayan 450]: ").strip() or "Himalayan 450"
                print("Destinations: [1] Ladakh / High Altitude, [2] Coastal Highway, [3] Desert Run, [4] Monsoon Western Ghats, [5] Interstate Expressway")
                dest_in = input("Destination [1-5, default 1]: ").strip() or "1"
                dest_map = {"1": "ladakh_high_altitude", "2": "coastal_highway", "3": "desert_run", "4": "monsoon_western_ghats", "5": "interstate_expressway"}
                print("\n" + chamunda_build_carry_along_spares_kit(
                    bike_model=m_model,
                    destination_key=dest_map.get(dest_in, "ladakh_high_altitude")
                ) + "\n")
            elif sub_c == "3":
                symptom = input("Describe breakdown symptom (e.g. clutch wire snap, engine overheating, puncture) [default clutch wire snap on highway]: ").strip() or "clutch wire snap on highway"
                print("\n" + chamunda_highway_breakdown_sos_triage(symptom_query=symptom) + "\n")
            else:
                r_name = input("Rider Name [default Alpesh Patel]: ").strip() or "Alpesh Patel"
                r_phone = input("Phone [default +91 98250 54321]: ").strip() or "+91 98250 54321"
                m_model = input("RE Model [default Himalayan 450]: ").strip() or "Himalayan 450"
                m_reg = input("Registration No [default GJ-01-RE-2024]: ").strip() or "GJ-01-RE-2024"
                print("Destinations: [1] Ladakh / High Altitude, [2] Coastal Highway, [3] Desert Run, [4] Monsoon Western Ghats, [5] Interstate Expressway")
                dest_in = input("Destination [1-5, default 1]: ").strip() or "1"
                dest_map = {"1": "ladakh_high_altitude", "2": "coastal_highway", "3": "desert_run", "4": "monsoon_western_ghats", "5": "interstate_expressway"}
                p_km = input("Planned KM [default 3500]: ").strip() or "3500"
                print("\n" + chamunda_audit_expedition_readiness(
                    rider_name=r_name,
                    phone=r_phone,
                    bike_model=m_model,
                    registration_no=m_reg,
                    destination_key=dest_map.get(dest_in, "ladakh_high_altitude"),
                    planned_km=int(p_km)
                ) + "\n")
            continue

        if low in ["12", "[12]"]:
            print("\nSelect Custom Resto-Mod & Vintage Studio Service:")
            print("  [1] 🏍️ Bespoke Resto-Mod Build Quote & Locked BOM Blueprint")
            print("  [2] ⚡ Dyno Performance Tuning & Noise Check (<85 dB)")
            print("  [3] ⚙️ Vintage Cast-Iron (CI) Heavy Crank Rebirth & Tappet Matrix")
            sub_c = input("Option [1-3, default 1]: ").strip() or "1"
            if sub_c == "2":
                m_model = input("RE Model Platform [default Classic 350 Reborn]: ").strip() or "Classic 350 Reborn"
                stg = input("Tuning Stage ([1] Stage-1 Street Thump, [2] Stage-2 Dyno Sprint) [default 1]: ").strip() or "1"
                stg_key = "stage_2_dyno_sprint" if stg == "2" else "stage_1_street_thump"
                print("\n" + chamunda_calculate_performance_stage_tune(bike_model=m_model, stage_key=stg_key) + "\n")
            elif sub_c == "3":
                symptom = input("Describe vintage CI symptom (e.g. cb point gap misfire, pushrod tappet clatter, albion 4 speed slip) [default cb point gap misfire]: ").strip() or "cb point gap misfire"
                print("\n" + chamunda_diagnose_vintage_ci_bullet(symptom_query=symptom) + "\n")
            else:
                c_name = input("Rider Name [default Kishorbhai Parmar]: ").strip() or "Kishorbhai Parmar"
                c_phone = input("Phone [default +91 98250 44551]: ").strip() or "+91 98250 44551"
                m_model = input("RE Model Platform [default Bullet 350 Cast-Iron CI]: ").strip() or "Bullet 350 Cast-Iron CI"
                m_reg = input("Registration No [default GJ-01-AB-1982]: ").strip() or "GJ-01-AB-1982"
                print("Styles: [1] Bobber Solo, [2] Cafe Racer, [3] Desert Scrambler, [4] Vintage Heritage")
                style_in = input("Style [1-4, default 1]: ").strip() or "1"
                style_map = {"1": "bobber_solo", "2": "cafe_racer", "3": "desert_scrambler", "4": "vintage_heritage_standard"}
                print("\n" + chamunda_build_custom_restomod_quote(
                    customer_name=c_name,
                    phone=c_phone,
                    bike_model=m_model,
                    registration_no=m_reg,
                    style_key=style_map.get(style_in, "bobber_solo"),
                    paint_theme_key="matte_phantom_black",
                    performance_stage_key="stage_1_street_thump",
                    include_vintage_ci_package=True,
                    custom_notes="Configured via Chamunda CLI Console"
                ) + "\n")
            continue

        if low in ["13", "[13]"]:
            print("\nSelect 360° Social & Brand Action:")
            print("  [1] 📊 View All Channels Live Telemetry & Metrics")
            print("  [2] 🚀 Generate & Publish Multi-Platform Campaign (WhatsApp, IG, FB, GBP, YT)")
            print("  [3] 📥 View Unified Social Inbox & Customer Queries")
            print("  [4] ⭐ Google Business Profile 4.9★ Reviews & Auto-Replies")
            sub_c = input("Option [1-4, default 1]: ").strip() or "1"
            if sub_c == "1":
                print("\n" + chamunda_get_social_telemetry() + "\n")
            elif sub_c == "2":
                top_in = input("Enter Campaign Topic [default Classic 350 Cold Start Tappet Noise Fix]: ").strip() or "Classic 350 Cold Start Tappet Noise Fix"
                print("\n" + chamunda_generate_social_campaign(topic=top_in) + "\n")
                pub_q = input("Publish to all channels now? (y/n) [default y]: ").strip().lower() or "y"
                if pub_q in ["y", "yes"]:
                    print("\n" + chamunda_publish_social_post(topic=top_in, channels="all") + "\n")
            elif sub_c == "3":
                ch_filter = input("Filter channel ('all', 'whatsapp', 'instagram', 'facebook', 'youtube') [default all]: ").strip() or "all"
                print("\n" + chamunda_manage_social_inbox(channel=ch_filter) + "\n")
            elif sub_c == "4":
                print("\n" + chamunda_manage_google_business_reviews() + "\n")
            continue

        if low in ["14", "[14]"]:
            print("\nSelect Executive Sub-Agent Action:")
            print("  [1] 📋 List All 5 Departmental Sub-Agents & Leads")
            print("  [2] 👑 View CEO Executive Dashboard & Delegation History")
            print("  [3] ✍️ Issue Written Command (ગુજરાતી અથવા English લેખિત આદેશ આપો)")
            print("  [4] 🎯 Delegate Specific Directive to Sub-Agent")
            print("  [5] 🧠 View Sub-Agent Growth & Self-Healing Matrix (લેવલ, XP અને સ્વાયત્ત ઉકેલો)")
            print("  [6] ⚡ Run Autonomous Incident Diagnostic & Self-Healing (સમસ્યાનું નિવારણ કરો)")
            sub_c = input("Option [1-6, default 5]: ").strip() or "5"
            if sub_c == "1":
                print("\n" + chamunda_list_shop_subagents() + "\n")
            elif sub_c == "2":
                print("\n" + chamunda_get_subagents_status() + "\n")
            elif sub_c == "3":
                w_cmd = input("Enter Written Command (English or ગુજરાતી): ").strip()
                if w_cmd:
                    print("\n" + chamunda_execute_written_command(command=w_cmd, sender="Alpesh Sir (Founder & Chairman)") + "\n")
                else:
                    print("\n[!] No command entered.\n")
            elif sub_c == "4":
                print("Target Sub-Agents: [1] bay_chief, [2] parts_specialist, [3] customer_receptionist, [4] social_growth_manager, [5] accounts_controller")
                a_c = input("Select Sub-Agent [1-5, default 1]: ").strip() or "1"
                a_map = {
                    "1": "bay_chief",
                    "2": "parts_specialist",
                    "3": "customer_receptionist",
                    "4": "social_growth_manager",
                    "5": "accounts_controller"
                }
                target_agent = a_map.get(a_c, "bay_chief")
                task_in = input("Enter Directive / Instructions: ").strip() or "Perform routine department inspection"
                print("\n" + chamunda_delegate_shop_task(agent_name=target_agent, task=task_in) + "\n")
            elif sub_c == "5":
                print("\n" + chamunda_get_subagents_growth_telemetry() + "\n")
            elif sub_c == "6":
                print("Select Department: [1] bay_chief (Ramesh), [2] parts_specialist (Jayesh), [3] customer_receptionist (Priya), [4] social_growth_manager (Kabir), [5] accounts_controller (Hasmukh)")
                a_c = input("Select Agent [1-5, default 1]: ").strip() or "1"
                a_map = {
                    "1": "bay_chief",
                    "2": "parts_specialist",
                    "3": "customer_receptionist",
                    "4": "social_growth_manager",
                    "5": "accounts_controller"
                }
                target_agent = a_map.get(a_c, "bay_chief")
                issue_in = input("Describe Issue / Defect to Heal [Enter for auto-preset]: ").strip()
                if not issue_in:
                    issue_in = "Operational execution roadblock or technical defect"
                print("\n" + chamunda_heal_shop_subagent(agent_name=target_agent, issue=issue_in) + "\n")
            continue

        if low in ["15", "[15]"]:
            print("\n🎙️ Chamunda Hands-Free Workshop Bay Voice Terminal:")
            print("  Speak or type natural command (e.g. 'આરાધ્યા GJ-02-BQ-1234 માં લિક્વી મોલી 15W-50 અને ઓઇલ ફિલ્ટર નાખી દીધા છે')")
            v_input = input("Voice Command [default simulation]: ").strip()
            if not v_input:
                v_input = "આરાધ્યા, ગાડી નંબર GJ-02-BQ-1234 માં લિક્વી મોલી 15W-50 એન્જિન ઓઇલ અને નવું ઓઇલ ફિલ્ટર નાખી દીધું છે, બિલમાં એડ કરી દો."
            m_name = input("Mechanic Name [default Master Tech Ramesh]: ").strip() or "Master Tech Ramesh"
            print("\n" + chamunda_process_bay_voice_command(spoken_text=v_input, mechanic_name=m_name) + "\n")
            continue

        if low in ["16", "[16]"]:
            print("\n📦 Chamunda B2B Wholesale Spares Network:")
            print("  [1] 📋 View North Gujarat Partner Garages & Routes")
            print("  [2] 🚚 Dispatch Quick Wholesale Order (Patan / Visnagar)")
            sub_b2b = input("Option [1-2, default 1]: ").strip() or "1"
            if sub_b2b == "1":
                print("\n" + chamunda_get_b2b_wholesale_overview() + "\n")
            elif sub_b2b == "2":
                gid_in = input("Partner Garage ID [default GAR-PATAN-001]: ").strip() or "GAR-PATAN-001"
                parts_json = '[{"part_number": "574050/C", "name": "Genuine Oil Filter Element", "quantity": 10, "mrp": 210}, {"part_number": "147008/A", "name": "OEM Air Filter", "quantity": 5, "mrp": 380}]'
                print("\n" + chamunda_create_b2b_wholesale_order(garage_id=gid_in, items_json=parts_json, payment_mode="Credit (15 Days)") + "\n")
            continue

        if low in ["17", "[17]"]:
            print("\n🏍️ Chamunda Royal Riders Club (CRRC) & AMC Manager:")
            print("  [1] 🛡️ View AMC Membership Plans (Silver / Gold / Platinum)")
            print("  [2] 👥 View Active Club Members & Thump Points")
            print("  [3] 📝 Enroll New Rider into AMC Pass")
            sub_club = input("Option [1-3, default 1]: ").strip() or "1"
            if sub_club == "1":
                print("\n" + chamunda_manage_amc_membership(action="list_plans") + "\n")
            elif sub_club == "2":
                print("\n" + chamunda_manage_amc_membership(action="overview") + "\n")
            elif sub_club == "3":
                r_name = input("Rider Name [default Alpesh Sir]: ").strip() or "Alpesh Sir"
                r_phone = input("Phone [default +91 78747 19139]: ").strip() or "+91 78747 19139"
                r_bike = input("Bike Model [default Bullet 350 Standard]: ").strip() or "Bullet 350 Standard"
                r_reg = input("Registration No [default GJ-02-BQ-1234]: ").strip() or "GJ-02-BQ-1234"
                print("Plans: [1] AMC-SILVER (₹3,999), [2] AMC-GOLD (₹7,499), [3] AMC-PLATINUM (₹11,999)")
                p_c = input("Plan [1-3, default 3]: ").strip() or "3"
                p_map = {"1": "AMC-SILVER", "2": "AMC-GOLD", "3": "AMC-PLATINUM"}
                print("\n" + chamunda_manage_amc_membership(action="enroll", name=r_name, phone=r_phone, bike_model=r_bike, registration_no=r_reg, plan_id=p_map.get(p_c, "AMC-PLATINUM")) + "\n")
            continue

        if low in ["18", "[18]"]:
            print("\n🔌 Chamunda OBD-II Live IoT ECU Scanner:")
            b_in = input("Bike Model [default Classic 350 (Reborn)]: ").strip() or "Classic 350 (Reborn)"
            r_in = input("Registration No [default GJ-02-BQ-1234]: ").strip() or "GJ-02-BQ-1234"
            print("Simulate DTC: [1] P0505 (Idle Stepper Motor), [2] P0130 (O2 Sensor), [3] P0115 (Temp Sensor), [4] P0300 (Misfire), [5] Optimal (Zero DTCs)")
            dtc_c = input("Option [1-5, default 1]: ").strip() or "1"
            dtc_map = {"1": "P0505", "2": "P0130", "3": "P0115", "4": "P0300", "5": "HEALTHY"}
            print("\n" + chamunda_run_obd_iot_scan(bike_model=b_in, registration_no=r_in, simulate_dtc=dtc_map.get(dtc_c, "P0505")) + "\n")
            continue

        if low in ["19", "[19]"]:
            print("\n🖥️ Workshop Smart Lounge Kiosk Express Check-In:")
            r_reg = input("Registration No [default GJ-02-BQ-1234]: ").strip() or "GJ-02-BQ-1234"
            r_name = input("Rider Name [default Alpesh Sir]: ").strip() or "Alpesh Sir"
            r_phone = input("Phone [default +91 78747 19139]: ").strip() or "+91 78747 19139"
            r_bike = input("Bike Model [default Classic 350 Reborn]: ").strip() or "Classic 350 Reborn"
            r_issues = input("Issues [default Periodic 10,000 km Service, Tappet Sound Check]: ").strip() or "Periodic 10,000 km Service, Tappet Sound Check"
            print("\n" + chamunda_kiosk_express_checkin(registration_no=r_reg, customer_name=r_name, phone=r_phone, bike_model=r_bike, issues_csv=r_issues) + "\n")
            continue

        if low in ["20", "[20]"]:
            print("\n📈 Chamunda AI Predictive Supply Chain & Auto-Reordering:")
            print("  [1] 📊 View Festival Demand Velocity Forecast (Diwali / Dhanteras 2.5x)")
            print("  [2] 📦 Auto-Generate Replenishment Wholesale PO for Supplier")
            sub_sc = input("Option [1-2, default 1]: ").strip() or "1"
            if sub_sc == "1":
                print("\n" + chamunda_get_predictive_supply_forecast(season_key="diwali_dhanteras_rush") + "\n")
            elif sub_sc == "2":
                print("\n" + chamunda_generate_predictive_auto_po(season_key="diwali_dhanteras_rush") + "\n")
            continue

        if low in ["21", "[21]"]:
            print("\n🧩 Chamunda 3D Interactive Exploded Engine Schematics:")
            print("  [1] J-Series 350 SOHC Cylinder Head & Valvetrain (Classic/Hunter/Meteor)")
            print("  [2] 650 Parallel-Twin Slipper & Assist Clutch (Interceptor/GT 650)")
            print("  [3] Vintage 1982 Cast-Iron Bullet 350 Heavy Crankshaft & Flywheels")
            print("  [4] Sherpa 450 Liquid-Cooled Water Pump & Thermal Loop (Himalayan 450)")
            a_c = input("Option [1-4, default 1]: ").strip() or "1"
            a_map = {"1": "ASM-J350-HEAD", "2": "ASM-650-CLUTCH", "3": "ASM-CI350-CRANK", "4": "ASM-SHERPA-COOLING"}
            print("\n" + chamunda_lookup_3d_engine_schematic(assembly_id=a_map.get(a_c, "ASM-J350-HEAD")) + "\n")
            continue

        if low in ["22", "[22]"]:
            print("\n🔬 Chamunda Non-Invasive AI Borescope Endoscopic Scanner:")
            b_model = input("Bike Model [default Classic 350 (Reborn)]: ").strip() or "Classic 350 (Reborn)"
            b_reg = input("Registration No [default GJ-02-BQ-1234]: ").strip() or "GJ-02-BQ-1234"
            b_km = input("Odometer KM [default 15000]: ").strip() or "15000"
            print("Select Inspection Scenario:")
            print("  [1] Heavy Carbon Crust (0.95-1.15 mm encrustation, knock risk)")
            print("  [2] Moderate Carbon Layer (0.45 mm soot, minor valve glazing)")
            print("  [3] Pristine Showroom Spec (0.12 mm, intact factory crosshatch)")
            print("  [4] Cylinder Bore Score Scratches & Pitted Valve Lip")
            s_c = input("Option [1-4, default 1]: ").strip() or "1"
            s_map = {"1": "heavy_carbon_crust", "2": "moderate_carbon", "3": "pristine_showroom", "4": "bore_score_damage"}
            print("\n" + chamunda_run_borescope_inspection(bike_model=b_model, registration_no=b_reg, odometer_km=int(b_km), scenario=s_map.get(s_c, "heavy_carbon_crust")) + "\n")
            continue

        if low in ["23", "[23]"]:
            print("\n🏢 Chamunda Multi-Branch Cloud Franchise Network:")
            print("  [1] 📊 View Consolidated Network Telemetry & Branches")
            print("  [2] 🚚 Dispatch Intra-Branch Spares Transfer")
            b_c = input("Option [1-2, default 1]: ").strip() or "1"
            if b_c == "1":
                print("\n" + chamunda_get_multibranch_overview() + "\n")
            elif b_c == "2":
                f_b = input("From Branch [default HQ-MEHSANA]: ").strip() or "HQ-MEHSANA"
                t_b = input("To Branch [default BR-PATAN-01]: ").strip() or "BR-PATAN-01"
                p_n = input("OEM Part Number [default 574012/A]: ").strip() or "574012/A"
                qty = input("Quantity [default 2]: ").strip() or "2"
                notes = input("Transfer Notes [default Urgent service bay dispatch]: ").strip() or "Urgent service bay dispatch"
                print("\n" + chamunda_transfer_branch_inventory(from_branch=f_b, to_branch=t_b, part_number=p_n, quantity=int(qty), notes=notes) + "\n")
            continue

        if low in ["24", "[24]", "turbo", "lag", "boost", "ઝડપી", "લેગ", "optimizer"]:
            print("\n🚀 Chamunda Laptop System Optimizer & Lag Buster:")
            print("  [1] ⚡ Quick Turbo Boost (Reclaim RAM & Terminate Stale Tasks)")
            print("  [2] 💻 Real-Time System Resources Telemetry")
            print("  [3] 🔥 Aggressive Deep Memory Cleanup")
            opt_c = input("Option [1-3, default 1]: ").strip() or "1"
            from system_optimizer import get_system_optimizer
            optimizer = get_system_optimizer()
            if opt_c == "1":
                res = optimizer.optimize_laptop_performance(aggressive=False)
                print("\n" + res["message_gu"])
                print(res["message_en"] + "\n")
            elif opt_c == "2":
                m = optimizer.get_system_metrics()
                print(f"\nStatus: {m['status']} ({m['status_gu']})")
                print(f"CPU: {m['cpu_percent']}% | RAM: {m['memory']['percent_used']}% (Used: {m['memory']['used_mb']}MB / Free: {m['memory']['free_mb']}MB)")
                print(f"Top processes: {', '.join([p['name'] + ' (' + str(p['memory_mb']) + 'MB)' for p in m['top_processes'][:4]])}\n")
            elif opt_c == "3":
                res = optimizer.optimize_laptop_performance(aggressive=True)
                print("\n" + res["message_gu"])
                print(res["message_en"] + "\n")
            continue

        if low in ["25", "[25]", "webar", "ar camera", "દિવ્ય દ્રષ્ટિ"]:
            print("\n👁️ Chamunda WebAR Live Camera Engine Overlay:")
            print("  [1] J-Series 350 SOHC Cylinder Head & Camshaft (45 Nm)")
            print("  [2] 650 Parallel Twin Slipper Clutch Hub (100 Nm Reverse)")
            print("  [3] 1982 Vintage Cast-Iron Heavy Crankcase (140 Nm)")
            print("  [4] Sherpa 450 Liquid-Cooled Loop & Water Pump (11 Nm)")
            ar_c = input("Option [1-4, default 1]: ").strip() or "1"
            ar_map = {"1": "AR-J350-HEAD", "2": "AR-650-CLUTCH", "3": "AR-VINTAGE-CI-CRANK", "4": "AR-SHERPA-450-COOLING"}
            from webar_engine_guide import get_webar_engine
            w_eng = get_webar_engine()
            w_view = w_eng.calculate_ar_camera_view(ar_map.get(ar_c, "AR-J350-HEAD"))
            print(f"\n{w_view['title']} ({w_view['platform']}):")
            print(f"Methodology: {w_view['methodology']}")
            for m in w_view['markers']:
                print(f"  Step #{m['sequence_step']}: {m['label']} -> {m['torque_nm']} Nm ({m['tool_spec']}) | Stock: {m.get('warehouse_stock')} pcs")
            print(f"Ramesh Advisory: {w_view['ramesh_advisory']}\n")
            continue

        if low in ["26", "[26]", "locker", "night locker", "emergency", "રાત્રિ સંરક્ષક"]:
            print("\n🌙 24/7 Automated Highway Emergency Spares Locker:")
            print("  [1] 📊 Inspect Exterior Locker Bay Status & Temperature")
            print("  [2] 📦 Reserve Emergency Breakdown Part & Generate OTP")
            print("  [3] 🔑 Test Solenoid Relay Unlock (Enter OTP)")
            lk_c = input("Option [1-3, default 1]: ").strip() or "1"
            from night_locker_engine import get_night_locker_manager
            l_mgr = get_night_locker_manager()
            if lk_c == "1":
                lst = l_mgr.get_locker_status()
                print(f"\nStation: {lst['locker_station']} ({lst['telemetry']['system_status']})")
                print(f"Available Bays: {lst['available_compartments_count']}/{lst['total_compartments']} | Temp: {lst['telemetry']['ambient_temp_c']}°C | Battery: {lst['telemetry']['backup_battery_pct']}%")
                for c in lst['compartments']:
                    print(f"  [{c['box_id']}] {c['item_name']} - ₹{c['price_inr']} ({c['units_inside']} pcs) -> {c['status']}")
                print(f"WhatsApp Helpline: {lst['support_whatsapp']}\n")
            elif lk_c == "2":
                box = input("Enter Box ID [default BOX-01]: ").strip() or "BOX-01"
                cname = input("Customer / Rider Name [default Touring Rider]: ").strip() or "Touring Rider"
                cphone = input("Phone [default +91 98250 12345]: ").strip() or "+91 98250 12345"
                creg = input("Vehicle Reg [default GJ-02-BQ-1234]: ").strip() or "GJ-02-BQ-1234"
                rres = l_mgr.reserve_compartment(box_id=box, customer_name=cname, phone=cphone, vehicle_reg=creg)
                print("\n" + rres.get("message_gu", str(rres)) + "\n")
            elif lk_c == "3":
                rid = input("Reservation ID: ").strip()
                rotp = input("6-Digit Unlock OTP: ").strip()
                ures = l_mgr.verify_and_unlock(reservation_id=rid, otp_code=rotp)
                print("\n" + ures.get("message_gu", str(ures)) + "\n")
            continue

        if low in ["27", "[27]", "chhaya", "cloud shadow", "offline mirror", "છાયા"]:
            print("\n☁️ Chamunda Cloud Shadow & Offline Mirror (Project Chhaya):")
            print("  [1] 📊 View Cloud Mirror Telemetry & Replicas Status")
            print("  [2] 🔄 Trigger Instant Local-to-Cloud Snapshot Sync")
            print("  [3] 📱 Simulate Remote Offline Query (WhatsApp Simulation)")
            print("  [4] ⚡ Reconcile Offline Queued Mutations")
            c_c = input("Option [1-4, default 1]: ").strip() or "1"
            from cloud_shadow_engine import get_cloud_shadow_manager
            c_mgr = get_cloud_shadow_manager()
            if c_c == "1":
                c_st = c_mgr.get_shadow_telemetry()
                print(f"\nCluster: {c_st['cluster_name']} ({c_st['system_mode']}) | Region: {c_st['cloud_region']}")
                print(f"Parts Mirrored: {c_st['snapshot_data'].get('total_parts_skus')} | Value: ₹{c_st['snapshot_data'].get('inventory_valuation_inr'):,}")
                print(f"Active Replicas: {len(c_st['cloud_replicas'])} agents | Queued Events: {c_st['queued_mutations_count']}")
                print(f"WhatsApp Helpline: {c_st['whatsapp_helpline']}\n")
            elif c_c == "2":
                s_res = c_mgr.generate_state_snapshot()
                print(f"\n✅ {s_res['message']} (Timestamp: {s_res['timestamp']})\n")
            elif c_c == "3":
                q_text = input("Enter remote inquiry (e.g. 'Classic 350 clutch plate stock'): ").strip() or "Classic 350 clutch plate stock"
                q_res = c_mgr.process_remote_offline_query(query_text=q_text)
                print(f"\nResponding: {q_res['responding_agent']} ({q_res['assigned_role']})")
                print(f"English: {q_res['response_en']}")
                print(f"ગુજરાતી: {q_res['response_gu']}\n")
            elif c_c == "4":
                r_res = c_mgr.reconcile_sync()
                print(f"\n✅ {r_res['message_gu']}\n")
            continue

        # Free natural language command routed to Aradhya OfflineCommander
        response = commander.execute_offline_turn(prompt)
        print("\n" + response + "\n")


if __name__ == "__main__":
    interactive_loop()
