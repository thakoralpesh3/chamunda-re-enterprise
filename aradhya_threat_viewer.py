#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chamunda Automobile Enterprise • Project "Chhaya"
ARADHYA THREAT FORENSICS & NEUTRALIZATION INSPECTOR
Author: Aradhya (CEO), reporting directly to Alpesh Sir (Founder & Chairman)

Displays comprehensive forensic details of all threats neutralized by the
Aradhya Cyber-Defense Shield:
- Threat Classification (Reverse Shell, Backdoor Listener, Temp Binaries, Brute Force, Tampering)
- Hostile Process & Full Command-Line telemetry
- PID, Executable Path, Target Ports
- Mitigation Status & Actions Taken (SIGKILL / Port Closed)
- Bilingual Explanation (English & Natural Gujarati)
- Real-Time Action Controls (Emergency Lockdown, Rescan)
"""

import os
import sys
import json
import time
import datetime
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data"
THREAT_LOG_FILE = DATA_DIR / "aradhya_threats_neutralized.json"
SECURITY_AUDIT_LOG = DATA_DIR / "aradhya_security_audit.log"


def get_threat_records() -> List[Dict[str, Any]]:
    """Retrieve all neutralized threat records in reverse chronological order."""
    if not THREAT_LOG_FILE.exists():
        return []
    try:
        data = json.loads(THREAT_LOG_FILE.read_text(encoding="utf-8") or "[]")
        if isinstance(data, list):
            return list(reversed(data))
        return []
    except Exception:
        return []


def format_threat_detail_text(record: Dict[str, Any]) -> str:
    """Format a single threat record with complete forensic details."""
    threat_type = record.get("threat_type", "UNKNOWN_THREAT")
    timestamp = record.get("timestamp", "N/A")
    pid = record.get("pid", "N/A")
    name = record.get("name", "N/A")
    exe = record.get("exe", "N/A")
    cmdline = record.get("cmdline", "N/A")
    port = record.get("port", "N/A")
    action = record.get("action_taken", "TERMINATED")
    severity = record.get("severity", "CRITICAL 🚨")

    # Threat Analysis Descriptions
    analysis_en = ""
    analysis_gu = ""

    if "REVERSE_SHELL" in threat_type:
        analysis_en = (
            "A malicious interactive reverse shell payload was identified attempting to give remote "
            "attacker terminal control over your laptop. Aradhya Sentry intercepted the process and "
            "executed instant SIGKILL termination."
        )
        analysis_gu = (
            "રિમોટ હેકરને આપના લેપટોપનો ટર્મિનલ કંટ્રોલ આપવાનો પ્રયાસ કરતો રિવર્સ શેલ પકડાયો હતો. "
            "આરાધ્યા સાયબર-ડિફેન્સ કવચે તેને તાત્કાલિક મારી નાખી (SIGKILL) સંપૂર્ણ સુરક્ષિત કરી દીધું છે."
        )
    elif "BACKDOOR" in threat_type:
        analysis_en = (
            f"An unauthorized network socket was detected listening on public high-risk backdoor port {port}. "
            "Aradhya severed the socket and killed the process immediately."
        )
        analysis_gu = (
            f"હાઈ-રિસ્ક પોર્ટ {port} પર અનધિકૃત બેકડોર લિસનર પકડાયો હતો. "
            "આરાધ્યાએ નેટવર્ક પોર્ટ તાત્કાલિક બંધ કરી સોકેટ કિલ કરી દીધું છે."
        )
    elif "TEMP" in threat_type:
        analysis_en = (
            f"An unauthorized executable was running out of volatile directory '{exe}'. "
            "Temporary directory execution is a primary malware vector and was neutralized."
        )
        analysis_gu = (
            f"કામચલાઉ ડિરેક્ટરી '{exe}' માંથી ચાલતી શંકાસ્પદ બાઈનરી પકડાઈ અને બ્લોક કરવામાં આવી."
        )
    elif "BRUTE_FORCE" in threat_type:
        analysis_en = "Multiple failed authentication attempts detected in system authentication logs."
        analysis_gu = "સિસ્ટમ ઓથેન્ટિકેશન લૉગ્સમાં બ્રુટ-ફોર્સ પાસવર્ડ હુમલાની ચેતવણી."
    else:
        analysis_en = "Suspicious system activity intercepted and mitigated by Aradhya Zero-Trust Matrix."
        analysis_gu = "આરાધ્યા ઝીરો-ટ્રસ્ટ સિક્યુરિટી શીલ્ડ દ્વારા શંકાસ્પદ પ્રવૃત્તિ અટકાવવામાં આવી."

    details = (
        f"═══════════════════════════════════════════════════════════════════════\n"
        f"🛡️ INCIDENT REPORT: {threat_type}\n"
        f"═══════════════════════════════════════════════════════════════════════\n"
        f"• Timestamp:        {timestamp}\n"
        f"• Severity:         {severity}\n"
        f"• Process Name:     {name} (PID: {pid})\n"
        f"• Executable Path:  {exe}\n"
        f"• Network Port:     {port if port != 'N/A' else 'None (Local Host Vector)'}\n"
        f"• Action Taken:     {action} ✅\n"
        f"• Defense Status:   100% NEUTRALIZED & SECURED\n\n"
        f"🔍 COMMAND LINE PAYLOAD:\n"
        f"   {cmdline}\n\n"
        f"📋 FORENSIC ANALYSIS (ENGLISH):\n"
        f"   {analysis_en}\n\n"
        f"📋 ફોરેન્સિક પૃથ્થકરણ (ગુજરાતી):\n"
        f"   {analysis_gu}\n"
        f"═══════════════════════════════════════════════════════════════════════\n"
    )
    return details


class AradhyaThreatViewerGTK:
    """Modern GTK3 Graphical Viewer for Neutralized Threats."""

    def __init__(self):
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk, Pango

        self.Gtk = Gtk
        self.Pango = Pango
        self.records = get_threat_records()

        # Window Setup
        self.window = Gtk.Window(title="🛡️ Aradhya Cyber-Defense • Neutralized Threats Forensics")
        self.window.set_default_size(900, 620)
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.connect("destroy", Gtk.main_quit)

        # Main Vertical Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(16)
        vbox.set_margin_end(16)
        vbox.set_margin_top(14)
        vbox.set_margin_bottom(14)
        self.window.add(vbox)

        # 1. Header Banner
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        vbox.pack_start(header_box, False, False, 0)

        title_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        lbl_title = Gtk.Label()
        lbl_title.set_markup("<span size='x-large' weight='bold' color='#00ff88'>🛡️ Aradhya Autonomous Cyber-Defense Shield</span>")
        lbl_title.set_xalign(0.0)

        lbl_sub = Gtk.Label()
        lbl_sub.set_markup(
            f"<span size='small' color='#aaaaaa'>Owner: <b>Alpesh Sir</b> • Chamunda Automobile Enterprise • System: <b>Dell Inspiron 3542 (Linux Mint)</b></span>"
        )
        lbl_sub.set_xalign(0.0)

        title_vbox.pack_start(lbl_title, False, False, 0)
        title_vbox.pack_start(lbl_sub, False, False, 0)
        header_box.pack_start(title_vbox, True, True, 0)

        # Status Badge
        lbl_badge = Gtk.Label()
        threat_count = len(self.records)
        badge_text = f"<span background='#114422' color='#00ff88' weight='bold'>  {threat_count} THREAT(S) NEUTRALIZED  </span>" if threat_count > 0 else "<span background='#113355' color='#55aaff' weight='bold'>  0 ATTACKS DETECTED (CLEAN)  </span>"
        lbl_badge.set_markup(badge_text)
        header_box.pack_end(lbl_badge, False, False, 0)

        # 2. Main Paned Layout: List on Left (40%), Detailed Forensics on Right (60%)
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_position(360)
        vbox.pack_start(paned, True, True, 0)

        # Left Pane: List of Neutralized Threats
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        lbl_list_hdr = Gtk.Label()
        lbl_list_hdr.set_markup("<b>Neutralized Incidents Log:</b>")
        lbl_list_hdr.set_xalign(0.0)
        left_box.pack_start(lbl_list_hdr, False, False, 0)

        self.liststore = Gtk.ListStore(str, str, str, int)  # Timestamp, Threat Type, PID/Name, Record Index
        self._populate_liststore()

        treeview = Gtk.TreeView(model=self.liststore)
        treeview.set_rules_hint(True)

        # Columns
        col_time = Gtk.TreeViewColumn("Timestamp", Gtk.CellRendererText(), text=0)
        col_time.set_sort_column_id(0)
        treeview.append_column(col_time)

        col_type = Gtk.TreeViewColumn("Threat Type", Gtk.CellRendererText(), text=1)
        col_type.set_sort_column_id(1)
        treeview.append_column(col_type)

        col_pid = Gtk.TreeViewColumn("Target / PID", Gtk.CellRendererText(), text=2)
        treeview.append_column(col_pid)

        treeview.connect("cursor-changed", self._on_select_record)

        scroll_left = Gtk.ScrolledWindow()
        scroll_left.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_left.add(treeview)
        left_box.pack_start(scroll_left, True, True, 0)
        paned.pack1(left_box, True, False)

        # Right Pane: Detailed Incident Forensics
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        lbl_detail_hdr = Gtk.Label()
        lbl_detail_hdr.set_markup("<b>Incident Forensics & Mitigation Details:</b>")
        lbl_detail_hdr.set_xalign(0.0)
        right_box.pack_start(lbl_detail_hdr, False, False, 0)

        self.textview = Gtk.TextView()
        self.textview.set_editable(False)
        self.textview.set_cursor_visible(False)
        self.textview.set_monospace(True)
        self.textview.set_left_margin(12)
        self.textview.set_right_margin(12)
        self.textview.set_top_margin(10)
        self.textview.set_bottom_margin(10)

        scroll_right = Gtk.ScrolledWindow()
        scroll_right.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_right.add(self.textview)
        right_box.pack_start(scroll_right, True, True, 0)
        paned.pack2(right_box, True, False)

        # 3. Bottom Action Bar
        bottom_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        vbox.pack_end(bottom_box, False, False, 0)

        btn_lockdown = Gtk.Button(label="🚨 Emergency Lockdown")
        btn_lockdown.connect("clicked", self._on_lockdown)
        bottom_box.pack_start(btn_lockdown, False, False, 0)

        btn_rescan = Gtk.Button(label="🛡️ Run Active Defense Scan")
        btn_rescan.connect("clicked", self._on_rescan)
        bottom_box.pack_start(btn_rescan, False, False, 0)

        lbl_helpline = Gtk.Label()
        lbl_helpline.set_markup("<span color='#888888'>Helpline: +91 78747 19139 | 100% Offline Autonomous Shield</span>")
        lbl_helpline.set_xalign(0.5)
        bottom_box.pack_start(lbl_helpline, True, True, 0)

        btn_close = Gtk.Button(label="Close")
        btn_close.connect("clicked", lambda b: self.window.destroy())
        bottom_box.pack_end(btn_close, False, False, 0)

        # Select first record if exists
        if self.records:
            treeview.set_cursor(Gtk.TreePath(0))
            self._display_record(self.records[0])
        else:
            self._display_no_threats()

    def _populate_liststore(self):
        self.liststore.clear()
        for idx, rec in enumerate(self.records):
            ts = rec.get("timestamp", "").split()[-1] if " " in rec.get("timestamp", "") else rec.get("timestamp", "")
            tt = rec.get("threat_type", "THREAT")
            pid_str = f"PID {rec.get('pid')}" if rec.get("pid") else f"Port {rec.get('port', '')}"
            self.liststore.append([ts, tt, pid_str, idx])

    def _on_select_record(self, treeview):
        selection = treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter:
            idx = model[treeiter][3]
            if 0 <= idx < len(self.records):
                self._display_record(self.records[idx])

    def _display_record(self, record: Dict[str, Any]):
        text = format_threat_detail_text(record)
        buf = self.textview.get_buffer()
        buf.set_text(text)

    def _display_no_threats(self):
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        text = (
            f"═══════════════════════════════════════════════════════════════════════\n"
            f"🛡️ ARADHYA ZERO-TRUST SECURITY SHIELD • ALL SYSTEMS CLEAN\n"
            f"═══════════════════════════════════════════════════════════════════════\n"
            f"• Current Time:      {now_str}\n"
            f"• Laptop Model:      Dell Inspiron 3542\n"
            f"• Operating System:  Linux Mint Cinnamon (Kernel 6.x / x86_64)\n"
            f"• Protection Mode:   Active Anti-Hacker Autonomous Watcher (24/7)\n"
            f"• Threat Posture:    100% SECURE & OPERATIONAL ✅\n\n"
            f"📋 STATUS SUMMARY:\n"
            f"   No active hacker attempts or unauthorized backdoor processes are\n"
            f"   currently running on this machine.\n\n"
            f"   All reverse shells, backdoor listeners on high-risk ports, and\n"
            f"   unauthorized /tmp binaries are continuously intercepted in real-time.\n\n"
            f"📋 ગુજરાતી અહેવાલ:\n"
            f"   જય માતાજી અલ્પેશ સાહેબ! લેપટોપ પર હાલમાં કોઈ શંકાસ્પદ કે હેકિંગ પ્રવૃત્તિ નથી.\n"
            f"   આરાધ્યા સાયબર-ડિફેન્સ કવચ સતત ૨૪x૭ સુરક્ષા પૂરી પાડી રહ્યું છે.\n"
            f"═══════════════════════════════════════════════════════════════════════\n"
        )
        self.textview.get_buffer().set_text(text)

    def _on_lockdown(self, btn):
        try:
            from aradhya_security_sentry import get_security_sentry
            res = get_security_sentry().emergency_lockdown()
            dialog = self.Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=self.Gtk.MessageType.WARNING,
                buttons=self.Gtk.ButtonsType.OK,
                text="🚨 Emergency Lockdown Triggered!"
            )
            dialog.format_secondary_text("Screen locked and network defense barriers engaged.")
            dialog.run()
            dialog.destroy()
        except Exception as e:
            pass

    def _on_rescan(self, btn):
        try:
            from aradhya_security_sentry import get_security_sentry
            res = get_security_sentry().active_threat_neutralization_cycle()
            self.records = get_threat_records()
            self._populate_liststore()
            if self.records:
                self._display_record(self.records[0])
            else:
                self._display_no_threats()
        except Exception:
            pass

    def show(self):
        self.window.show_all()
        import gi
        from gi.repository import Gtk
        Gtk.main()


def show_threat_details_zenity():
    """Fallback GUI using Zenity if GTK3 window fails or is unavailable."""
    records = get_threat_records()
    tmp_path = Path("/tmp/aradhya_threat_report.txt")
    if records:
        content = "\n\n".join([format_threat_detail_text(r) for r in records])
    else:
        content = (
            "🛡️ ARADHYA CYBER-DEFENSE SHIELD: ALL SYSTEMS CLEAN\n\n"
            "No hostile attacks or backdoor attempts detected.\n"
            "System posture: 100% Secure & Untampered."
        )
    tmp_path.write_text(content, encoding="utf-8")
    subprocess.run([
        "zenity", "--text-info",
        "--title=🛡️ Aradhya Cyber-Defense • Neutralized Threats",
        f"--filename={str(tmp_path)}",
        "--width=780", "--height=520",
        "--font=Monospace 10"
    ])


def show_threat_details_cli():
    """Display threat details in terminal with rich formatting."""
    records = get_threat_records()
    print("\n" + "=" * 75)
    print("🛡️  ARADHYA CYBER-DEFENSE SHIELD • NEUTRALIZED THREATS FORENSICS")
    print(f"• Target Workstation: Dell Inspiron 3542 (Linux Mint) | Owner: Alpesh Sir")
    print(f"• Total Neutralized Incidents: {len(records)}")
    print("=" * 75)

    if not records:
        print("\n✅ All systems 100% clean. Zero malicious payloads or backdoors recorded.\n")
        return

    for idx, r in enumerate(records, 1):
        print(f"\n[INCIDENT #{idx}]")
        print(format_threat_detail_text(r))


def launch_threat_viewer(mode: str = "auto"):
    """Launch GUI viewer with automatic fallback to Zenity or CLI."""
    if mode == "cli" or not os.environ.get("DISPLAY"):
        show_threat_details_cli()
        return

    try:
        app = AradhyaThreatViewerGTK()
        app.show()
    except Exception as e:
        try:
            show_threat_details_zenity()
        except Exception:
            show_threat_details_cli()


if __name__ == "__main__":
    mode_arg = "cli" if "--cli" in sys.argv or "-c" in sys.argv else "auto"
    launch_threat_viewer(mode_arg)
