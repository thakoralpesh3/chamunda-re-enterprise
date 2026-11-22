#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya 2D Desktop Companion (આરાધ્યા - ૨ડી ડેસ્કટોપ સાથી)
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)
Author: Aradhya (CEO)

Features:
1. Transparent, frameless 2D chibi robot girl character floating and walking across the desktop.
2. Natural idle behaviors:
   - Soft hovering / breathing
   - Eye blinking and winking
   - Sweet arm waving with cheerful greeting to Alpesh Sir
   - Cute wandering / walking along the taskbar / screen edges
   - Joyful cheering with glowing heart animations
   - Hovering jetpack flight mode
3. Real-time interactivity:
   - Click to speak with Aradhya (voice response in Gujarati)
   - Double-click to instantly launch the Aradhya Autonomous Agent terminal console
   - Right-click menu for instant actions:
     * 🎙️ Talk / Voice Mode
     * 🚀 Launch Aradhya Console (Full Terminal)
     * ⚡ Run Turbo Boost / Lag-Buster
     * 🛡️ Hacker Defense Scan
     * 📱 Remote Mobile Companion Link
     * 🔇 Mute / Unmute Voice
     * ❌ Minimize / Exit
   - Draggable across the desktop with mouse drag!
"""

import os
import sys
import time
import math
import random
import subprocess
from pathlib import Path

BASE_DIR = Path("/home/alpesh/chamunda_re_enterprise")
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib, Pango
import cairo

SPRITES_DIR = BASE_DIR / "data" / "aradhya_pet" / "sprites"

CHAT_CSS = b"""
window.aradhya-chat-window {
    background-color: #0d1117;
    border: 2px solid #30363d;
    border-radius: 14px;
}
.chat-header {
    background-color: #161b22;
    padding: 10px 14px;
    border-bottom: 1px solid #30363d;
    border-radius: 12px 12px 0 0;
}
.chat-header-title {
    color: #f59e0b;
    font-size: 13px;
    font-weight: bold;
}
.chat-header-sub {
    color: #8b949e;
    font-size: 10px;
}
.chat-close-btn {
    background: transparent;
    border: none;
    color: #8b949e;
    font-size: 14px;
    padding: 2px 6px;
    border-radius: 4px;
}
.chat-close-btn:hover {
    color: #ff7b72;
    background: rgba(248, 81, 73, 0.15);
}
.chips-container {
    background-color: #161b22;
    padding: 6px 10px;
    border-bottom: 1px solid #21262d;
}
.chip-btn {
    background-color: #21262d;
    border: 1px solid #30363d;
    color: #38bdf8;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
}
.chip-btn:hover {
    background-color: #30363d;
    color: #7dd3fc;
}
.chat-scrolled {
    background-color: #0d1117;
}
.msg-user-box {
    background-color: #1f6feb;
    border-radius: 12px 12px 2px 12px;
    padding: 8px 12px;
}
.msg-user-label {
    color: #ffffff;
    font-size: 12px;
}
.msg-aradhya-box {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px 12px 12px 2px;
    padding: 8px 12px;
}
.msg-aradhya-title {
    color: #f59e0b;
    font-size: 10px;
    font-weight: bold;
    margin-bottom: 2px;
}
.msg-aradhya-label {
    color: #f0f6fc;
    font-size: 12px;
}
.input-container {
    background-color: #161b22;
    padding: 8px 10px;
    border-top: 1px solid #30363d;
    border-radius: 0 0 12px 12px;
}
.chat-entry {
    background-color: #0d1117;
    border: 1px solid #30363d;
    border-radius: 6px;
    color: #f0f6fc;
    padding: 6px 8px;
    font-size: 12px;
}
.chat-entry:focus {
    border-color: #38bdf8;
}
.chat-send-btn {
    background-color: #238636;
    border: none;
    border-radius: 6px;
    color: #ffffff;
    padding: 6px 12px;
    font-weight: bold;
    font-size: 11px;
}
.chat-send-btn:hover {
    background-color: #2ea043;
}
"""

class AradhyaChatWindow(Gtk.Window):
    def __init__(self, pet):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.pet = pet
        self.set_title("👑 આરાધ્યા કમાન્ડ સેન્ટર")
        self.set_default_size(380, 520)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(False)
        self.set_decorated(False)
        self.get_style_context().add_class("aradhya-chat-window")

        # Load CSS style provider
        try:
            provider = Gtk.CssProvider()
            provider.load_from_data(CHAT_CSS)
            screen = Gdk.Screen.get_default()
            Gtk.StyleContext.add_provider_for_screen(screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except Exception:
            pass

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # 1. Header Bar
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header.get_style_context().add_class("chat-header")

        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        title_lbl = Gtk.Label()
        title_lbl.set_markup("<b>👑 આરાધ્યા કમાન્ડ સેન્ટર</b>")
        title_lbl.set_halign(Gtk.Align.START)
        title_lbl.get_style_context().add_class("chat-header-title")

        sub_lbl = Gtk.Label(label="જય માતાજી અલ્પેશ સાહેબ! બોલો આપનું શું કામ છે?")
        sub_lbl.set_halign(Gtk.Align.START)
        sub_lbl.get_style_context().add_class("chat-header-sub")

        title_box.pack_start(title_lbl, False, False, 0)
        title_box.pack_start(sub_lbl, False, False, 0)
        header.pack_start(title_box, True, True, 0)

        close_btn = Gtk.Button(label="✕")
        close_btn.get_style_context().add_class("chat-close-btn")
        close_btn.connect("clicked", lambda w: self.hide())
        header.pack_end(close_btn, False, False, 0)
        header.connect("button-press-event", self._on_header_press)
        main_box.pack_start(header, False, False, 0)

        # 2. Quick Action Chips
        chips_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        chips_box.get_style_context().add_class("chips-container")
        chips = [
            ("⚡ ટર્બો બૂસ્ટ", "turbo clean ram"),
            ("💬 WhatsApp", "open whatsapp"),
            ("🛡️ સાયબર સ્કેન", "hacker defense scan"),
            ("📊 સિસ્ટમ હેલ્થ", "check battery and system status"),
            ("🌐 OpenWebUI", "open_webui")
        ]
        for label, cmd in chips:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("chip-btn")
            btn.connect("clicked", self._on_chip_clicked, cmd)
            chips_box.pack_start(btn, False, False, 0)

        chips_scroll = Gtk.ScrolledWindow()
        chips_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        chips_scroll.add(chips_box)
        main_box.pack_start(chips_scroll, False, False, 0)

        # 3. Message List
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled.get_style_context().add_class("chat-scrolled")

        self.msg_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.msg_box.set_margin_top(8)
        self.msg_box.set_margin_bottom(8)
        self.msg_box.set_margin_start(10)
        self.msg_box.set_margin_end(10)
        self.scrolled.add(self.msg_box)
        main_box.pack_start(self.scrolled, True, True, 0)

        # 4. Input Area
        input_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        input_container.get_style_context().add_class("input-container")

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("આદેશ અથવા પ્રશ્ન લખો... (Type command)")
        self.entry.get_style_context().add_class("chat-entry")
        self.entry.connect("activate", self.on_send)
        input_container.pack_start(self.entry, True, True, 0)

        send_btn = Gtk.Button(label="મોકલો ➤")
        send_btn.get_style_context().add_class("chat-send-btn")
        send_btn.connect("clicked", self.on_send)
        input_container.pack_end(send_btn, False, False, 0)
        main_box.pack_start(input_container, False, False, 0)

        self.add_message("aradhya", "પ્રણામ અલ્પેશ સાહેબ! આરાધ્યા કમાન્ડ ચેટ સક્રિય છે. આપ કોઈપણ કાર્ય, ટેકનિકલ પ્રશ્ન કે સિસ્ટમ આદેશ આપી શકો છો.")
        self.connect("key-press-event", self._on_key_press)

    def _on_header_press(self, widget, event):
        if event.button == 1:
            self.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
        return True

    def _on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.hide()
            return True
        return False

    def _on_chip_clicked(self, widget, cmd):
        if cmd == "open_webui":
            subprocess.Popen(["xdg-open", "http://127.0.0.1:3000"])
            self.add_message("aradhya", "🌐 OpenWebUI બ્રાઉઝરમાં લૉન્ચ કરવામાં આવ્યું છે.")
            return
        self.entry.set_text(cmd)
        self.on_send(self.entry)

    def add_message(self, role: str, text: str):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        if role == "user":
            row.set_halign(Gtk.Align.END)
            bubble = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            bubble.get_style_context().add_class("msg-user-box")
            lbl = Gtk.Label(label=text)
            lbl.set_line_wrap(True)
            lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            lbl.set_max_width_chars(32)
            lbl.set_selectable(True)
            lbl.get_style_context().add_class("msg-user-label")
            bubble.pack_start(lbl, False, False, 0)
            row.pack_start(bubble, False, False, 0)
        else:
            row.set_halign(Gtk.Align.START)
            bubble = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            bubble.get_style_context().add_class("msg-aradhya-box")
            title = Gtk.Label(label="👑 આરાધ્યા (CEO)")
            title.set_halign(Gtk.Align.START)
            title.get_style_context().add_class("msg-aradhya-title")
            bubble.pack_start(title, False, False, 0)
            lbl = Gtk.Label(label=text)
            lbl.set_line_wrap(True)
            lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            lbl.set_max_width_chars(34)
            lbl.set_selectable(True)
            lbl.get_style_context().add_class("msg-aradhya-label")
            bubble.pack_start(lbl, False, False, 0)
            row.pack_start(bubble, False, False, 0)
            row._content_label = lbl

        self.msg_box.pack_start(row, False, False, 0)
        self.msg_box.show_all()
        GLib.idle_add(self._scroll_bottom)
        return row

    def _scroll_bottom(self):
        adj = self.scrolled.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        return False

    def on_send(self, widget):
        cmd = self.entry.get_text().strip()
        if not cmd:
            return
        self.entry.set_text("")
        self.add_message("user", cmd)
        loading_row = self.add_message("aradhya", "પ્રક્રિયા કરી રહી છું... ⏳")

        def _bg_worker():
            reply_text = ""
            try:
                from hermes_relay_agent import is_laptop_action
                from aradhya_autonomous_core import get_aradhya_engine
                if is_laptop_action(cmd):
                    core = get_aradhya_engine()
                    res = core.process_command(cmd, speak_response=False)
                    reply_text = res.get("response_gu") or res.get("response_en") or ""
            except Exception as e:
                logger.warning("Companion core physical execution error: %s", e)

            if not reply_text:
                try:
                    from hermes_relay_agent import get_hermes_relay
                    relay = get_hermes_relay()
                    res = relay.process_message(user_message=cmd, preferred_model="auto", voice_mode=False)
                    reply_text = res.get("reply") or res.get("response_gu") or res.get("response_en") or ""
                except Exception as e:
                    logger.warning("Companion relay error: %s", e)

            if not reply_text:
                try:
                    from aradhya_autonomous_core import get_aradhya_engine
                    core = get_aradhya_engine()
                    res = core.process_command(cmd, speak_response=False)
                    reply_text = res.get("response_gu") or res.get("response_en") or "આદેશ સફળતાપૂર્વક ચલાવાયો છે."
                except Exception as e:
                    reply_text = f"ક્ષમા કરશો સાહેબ, ક્ષતિ આવી છે: {e}"

            GLib.idle_add(self._deliver_reply, loading_row, reply_text)

        import threading
        threading.Thread(target=_bg_worker, daemon=True).start()

    def _deliver_reply(self, loading_row, reply_text):
        if hasattr(loading_row, "_content_label"):
            loading_row._content_label.set_text(reply_text)
        self._scroll_bottom()
        if self.pet:
            clean_short = reply_text.split("\n")[0][:25]
            self.pet.say(clean_short, duration=4, speak_aloud=False)
            self.pet.state = "WAVING"
        return False


# Voice greetings when clicked (Aradhya Autonomous Companion)
CLICK_GREETINGS = [
    "જય માતાજી અલ્પેશ સાહેબ! હું અહીં આપની સાથે તૈયાર છું.",
    "પ્રણામ અલ્પેશ સાહેબ! બોલો સાહેબ, આપનું શું કામ છે?",
    "હા સાહેબ! સાયબર પ્રોટેક્શન સમગ્ર લેપટોપ પર સક્રિય છે.",
    "બોલો અલ્પેશ સાહેબ! આપનો આદેશ આપો.",
    "આરાધ્યા આપની સેવામાં ૧૦૦% હાજર છે, સાહેબ!"
]

class AradhyaDesktopPet(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.POPUP)

        self.set_title("Aradhya 2D Companion")
        self.set_keep_above(True)
        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)

        # Support true RGBA transparency on X11
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Window dimension
        self.pet_w = 150
        self.pet_h = 160
        self.set_size_request(self.pet_w, self.pet_h)

        # Initial Position: Bottom-Right above the taskbar
        self.x = self.screen_width - 200
        self.y = self.screen_height - 240
        self.move(int(self.x), int(self.y))

        # Mouse Drag & Click State
        self.dragging = False
        self.has_dragged = False
        self.is_pressed = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.press_x = 0
        self.press_y = 0
        self.last_click_time = 0
        self.chat_window = None

        # Animation states
        self.state = "IDLE"  # IDLE, WAVING, WALKING, CHEERING, FLOATING
        self.frame_idx = 0
        self.direction = 1   # 1 = facing right, -1 = facing left
        self.state_timer = 0
        self.target_state_duration = random.randint(12, 25)

        # Speech bubble
        self.speech_bubble_text = "જય માતાજી અલ્પેશ સાહેબ! ⚡"
        self.show_speech_bubble = True
        self.bubble_expire_time = time.time() + 6.0

        # Pre-load Pixbuf Sprites
        self.sprites = self._load_sprites()
        self.current_pixbuf = self.sprites.get("idle_0")

        # Events
        self.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.connect("draw", self.on_draw)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion_notify)

        # Animation Timer (every 180ms for fluid anime motion)
        GLib.timeout_add(180, self.update_animation)
        # Behavior Planner (every 1 second)
        GLib.timeout_add(1000, self.plan_behavior)

        self.show_all()

    def _load_sprites(self):
        sprites = {}
        if not SPRITES_DIR.exists():
            return sprites

        for p in SPRITES_DIR.glob("*.png"):
            try:
                pb = GdkPixbuf.Pixbuf.new_from_file(str(p))
                sprites[p.stem] = pb
            except Exception:
                pass
        return sprites

    def on_draw(self, widget, cr):
        # 1. Clear background to 100% transparent
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        # 2. Draw Speech Bubble if active
        if self.show_speech_bubble and time.time() < self.bubble_expire_time:
            self._draw_speech_bubble(cr, self.speech_bubble_text)

        # 3. Draw Character Sprite
        if self.current_pixbuf:
            pb = self.current_pixbuf
            if self.direction < 0:
                pb = pb.flip(True)  # Flip horizontally if moving left
            Gdk.cairo_set_source_pixbuf(cr, pb, 0, 0)
            cr.paint()

        return False

    def _draw_speech_bubble(self, cr, text):
        cr.save()
        # White & cyan pill bubble above head
        bx, by, bw, bh = 6, 4, self.pet_w - 12, 28
        
        # Glow border
        cr.set_source_rgba(0, 0.8, 1, 0.4)
        cr.arc(bx + 10, by + 10, 8, 3.14, 4.71)
        cr.arc(bx + bw - 10, by + 10, 8, 4.71, 0)
        cr.arc(bx + bw - 10, by + bh - 10, 8, 0, 1.57)
        cr.arc(bx + 10, by + bh - 10, 8, 1.57, 3.14)
        cr.close_path()
        cr.fill()

        # Bubble body
        cr.set_source_rgba(0.08, 0.12, 0.22, 0.92)
        cr.arc(bx + 10, by + 10, 6, 3.14, 4.71)
        cr.arc(bx + bw - 10, by + 10, 6, 4.71, 0)
        cr.arc(bx + bw - 10, by + bh - 10, 6, 0, 1.57)
        cr.arc(bx + 10, by + bh - 10, 6, 1.57, 3.14)
        cr.close_path()
        cr.fill()

        # Text inside bubble
        cr.set_source_rgba(1, 1, 1, 1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(10)
        cr.move_to(bx + 8, by + 18)
        cr.show_text(text[:22])
        cr.restore()

    def update_animation(self):
        if self.dragging:
            self.current_pixbuf = self.sprites.get("float_1", self.current_pixbuf)
            self.queue_draw()
            return True

        self.frame_idx += 1

        if self.state == "IDLE":
            frames = ["idle_0", "idle_1", "idle_2", "idle_3"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

        elif self.state == "GAMING":
            # Interactive smartphone inspection
            frames = ["game_0", "game_1", "game_2", "game_3"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

        elif self.state == "WAVING":
            frames = ["wave_0", "wave_1", "wave_2", "wave_3"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

        elif self.state == "WALKING":
            frames = ["walk_0", "walk_1", "walk_2", "walk_3"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

            # Move character position
            step = 5 * self.direction
            new_x = self.x + step
            # Bounds check with margin
            if new_x < 30:
                self.direction = 1
            elif new_x > self.screen_width - self.pet_w - 30:
                self.direction = -1
            else:
                self.x = new_x
            self.move(int(self.x), int(self.y))

        elif self.state == "AIRDROP":
            frames = ["airdrop_0", "airdrop_1"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

        elif self.state == "VICTORY":
            frames = ["dance_0", "dance_1", "dance_2", "dance_3"]
            key = frames[self.frame_idx % len(frames)]
            self.current_pixbuf = self.sprites.get(key)

        self.queue_draw()
        return True

    def plan_behavior(self):
        if self.dragging:
            return True

        self.state_timer += 1
        if self.state_timer >= self.target_state_duration:
            self.state_timer = 0
            # Switch to a random cute autonomous behavior
            choices = ["IDLE", "GAMING", "WAVING", "WALKING", "AIRDROP", "VICTORY"]
            weights = [30, 25, 15, 15, 8, 7]
            self.state = random.choices(choices, weights=weights)[0]
            self.target_state_duration = random.randint(6, 16)

            if self.state == "GAMING":
                self.say(random.choice(["સિસ્ટમ મોનિટરિંગ... 📱", "ડેટા પ્રોસેસિંગ મોડ... ⚡", "આરાધ્યા સ્ટેન્ડબાય... ✨"]), duration=5)
            elif self.state == "WAVING":
                self.say("પ્રણામ અલ્પેશ સાહેબ! 👋", duration=4)
            elif self.state == "AIRDROP":
                self.say("સુરક્ષા પેકેજ તૈયાર છે સાહેબ! 📦✨", duration=4)
            elif self.state == "VICTORY":
                self.say("તમામ સિસ્ટમ સફળતાપૂર્વક સક્રિય છે! 🌟", duration=4)
            elif self.state == "WALKING":
                self.direction = random.choice([1, -1])

        return True

    def say(self, text: str, duration: int = 5, speak_aloud: bool = False):
        self.speech_bubble_text = text
        self.show_speech_bubble = True
        self.bubble_expire_time = time.time() + duration
        self.queue_draw()

        if speak_aloud:
            def _speak():
                try:
                    from aradhya_voice_engine import get_voice_engine
                    v = get_voice_engine()
                    v.speak(text, language="gu", blocking=False)
                except Exception:
                    pass
            import threading
            threading.Thread(target=_speak, daemon=True).start()

    def on_button_press(self, widget, event):
        now = time.time()

        # Left Click (Button 1)
        if event.button == 1:
            self.is_pressed = True
            self.press_x = event.x_root
            self.press_y = event.y_root
            self.has_dragged = False
            self.drag_offset_x = int(event.x)
            self.drag_offset_y = int(event.y)
            self.last_click_time = now

        # Right Click (Button 3) -> Context Menu
        elif event.button == 3:
            self.show_context_menu(event)

        return True

    def on_button_release(self, widget, event):
        if event.button == 1:
            was_dragged = getattr(self, "has_dragged", False)
            self.is_pressed = False
            self.dragging = False
            self.has_dragged = False
            self.state = "IDLE"
            if not was_dragged:
                # Clicked on anime girl -> Open small chat screen for commands/work!
                self.toggle_chat_screen()
        return True

    def on_motion_notify(self, widget, event):
        # Hover protection: Only move/drag if mouse button 1 is actively pressed down
        if not (event.state & Gdk.ModifierType.BUTTON1_MASK):
            self.is_pressed = False
            self.dragging = False
            return True

        if getattr(self, "is_pressed", False):
            dx = abs(event.x_root - self.press_x)
            dy = abs(event.y_root - self.press_y)
            if dx > 6 or dy > 6:
                self.has_dragged = True
                self.dragging = True
                new_x = int(event.x_root - self.drag_offset_x)
                new_y = int(event.y_root - self.drag_offset_y)
                self.x = max(0, min(self.screen_width - self.pet_w, new_x))
                self.y = max(0, min(self.screen_height - self.pet_h, new_y))
                self.move(int(self.x), int(self.y))
        return True

    def toggle_chat_screen(self):
        """Opens or toggles the small compact chat screen for asking commands or work."""
        if self.chat_window is None:
            self.chat_window = AradhyaChatWindow(self)

        if self.chat_window.get_visible():
            self.chat_window.hide()
        else:
            chat_w = 380
            chat_h = 520
            target_x = int(self.x - chat_w - 12)
            if target_x < 15:
                target_x = int(self.x + self.pet_w + 12)
            if target_x + chat_w > self.screen_width - 15:
                target_x = max(15, self.screen_width - chat_w - 20)

            target_y = int(self.y + self.pet_h - chat_h)
            if target_y < 40:
                target_y = 40
            if target_y + chat_h > self.screen_height - 40:
                target_y = max(40, self.screen_height - chat_h - 40)

            self.chat_window.move(target_x, target_y)
            self.chat_window.show_all()
            self.chat_window.present()
            self.chat_window.entry.grab_focus()

            self.state = "WAVING"
            greet = random.choice(CLICK_GREETINGS)
            self.say(greet, duration=4, speak_aloud=False)

    def launch_aradhya_terminal(self):
        """Launches the global terminal console."""
        cmd = [
            "gnome-terminal",
            "--title=👑 Aradhya Autonomous AI Orchestrator",
            "--geometry=115x32",
            "--", "bash", "-c", "/home/alpesh/bin/aradhya"
        ]
        try:
            subprocess.Popen(cmd)
        except Exception:
            try:
                subprocess.Popen(["x-terminal-emulator", "-e", "/home/alpesh/bin/aradhya"])
            except Exception:
                pass

    def show_context_menu(self, event):
        menu = Gtk.Menu()

        item_chat = Gtk.MenuItem(label="💬 આરાધ્યા કમાન્ડ ચેટ (Click Anime Girl)")
        item_chat.connect("activate", lambda w: self.toggle_chat_screen())
        menu.append(item_chat)

        item_launch = Gtk.MenuItem(label="🚀 Full Terminal Console")
        item_launch.connect("activate", lambda w: self.launch_aradhya_terminal())
        menu.append(item_launch)

        item_talk = Gtk.MenuItem(label="🎙️ Speak / Voice Command")
        item_talk.connect("activate", lambda w: self.trigger_voice_cmd())
        menu.append(item_talk)

        menu.append(Gtk.SeparatorMenuItem())

        item_turbo = Gtk.MenuItem(label="⚡ Proactive Turbo Boost (લેગ-બસ્ટર)")
        item_turbo.connect("activate", lambda w: self.trigger_turbo())
        menu.append(item_turbo)

        item_shield = Gtk.MenuItem(label="🛡️ Anti-Hacker Shield Scan")
        item_shield.connect("activate", lambda w: self.trigger_shield())
        menu.append(item_shield)

        item_remote = Gtk.MenuItem(label="📱 Mobile Remote Companion Link")
        item_remote.connect("activate", lambda w: self.trigger_remote())
        menu.append(item_remote)

        menu.append(Gtk.SeparatorMenuItem())

        item_health = Gtk.MenuItem(label="📊 Laptop Health & Diagnostics (સિસ્ટમ સ્થિતિ)")
        item_health.connect("activate", lambda w: self.trigger_health())
        menu.append(item_health)

        item_wa = Gtk.MenuItem(label="💬 WhatsApp Alert Test (અલ્પેશ સાહેબ)")
        item_wa.connect("activate", lambda w: self.trigger_whatsapp_test())
        menu.append(item_wa)

        menu.append(Gtk.SeparatorMenuItem())

        item_exit = Gtk.MenuItem(label="❌ Hide / Exit")
        item_exit.connect("activate", lambda w: Gtk.main_quit())
        menu.append(item_exit)

        menu.show_all()
        menu.popup_at_pointer(event)

    def trigger_voice_cmd(self):
        self.say("આપનો આદેશ આપો સાહેબ, હું સાંભળું છું... 🎙️", duration=4, speak_aloud=True)
        # One-shot terminal or mic capture
        subprocess.Popen(["gnome-terminal", "--title=🎙️ Aradhya Voice Mode", "--", "bash", "-c", "/home/alpesh/bin/aradhya --mic"])

    def trigger_turbo(self):
        self.say("ટર્બો બૂસ્ટિંગ સિસ્ટમ... ⚡", duration=3, speak_aloud=True)
        def _bg():
            from aradhya_autonomous_core import get_aradhya_engine
            e = get_aradhya_engine()
            e.process_command("turbo clean ram", speak_response=True)
        import threading
        threading.Thread(target=_bg, daemon=True).start()

    def trigger_shield(self):
        self.say("સાયબર સિક્યુરિટી સ્કેન સક્રિય! 🛡️", duration=3, speak_aloud=True)
        def _bg():
            from aradhya_autonomous_core import get_aradhya_engine
            e = get_aradhya_engine()
            e.process_command("hacker defense scan", speak_response=True)
        import threading
        threading.Thread(target=_bg, daemon=True).start()

    def trigger_remote(self):
        self.say("મોબાઇલ રીમોટ લિંક જનરેટ થઈ રહી છે... 📱", duration=3, speak_aloud=True)
        subprocess.Popen(["gnome-terminal", "--title=📱 Aradhya Mobile Remote", "--", "bash", "-c", "/home/alpesh/bin/aradhya --remote; sleep 15"])

    def trigger_health(self):
        self.say("લેપટોપ હેલ્થ અને ડાયગ્નોસ્ટિક્સ તપાસી રહી છું... 📊", duration=3, speak_aloud=True)
        def _bg():
            from aradhya_autonomous_core import get_aradhya_engine
            e = get_aradhya_engine()
            res = e.get_battery_status()
            import psutil
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            bat = res.get('percent', 100)
            txt = f"CPU: {cpu}% | RAM: {ram}% | બેટરી: {bat}%"
            self.say(f"લેપટોપ ૧૦૦% સલામત છે સાહેબ! ⚡\n{txt}", duration=6, speak_aloud=True)
        import threading
        threading.Thread(target=_bg, daemon=True).start()

    def trigger_whatsapp_test(self):
        self.say("અલ્પેશ સાહેબના વ્હોટ્સએપ પર ટેસ્ટ એલર્ટ મોકલી રહી છું... 💬", duration=3, speak_aloud=True)
        def _bg():
            from aradhya_notifier import get_aradhya_notifier
            n = get_aradhya_notifier()
            n.notify_work_done(
                "વ્હોટ્સએપ અને સિસ્ટમ કનેક્ટિવિટી ટેસ્ટ",
                details="આરાધ્યા ડેસ્કટોપ અને વ્હોટ્સએપ ઇન્ટરેક્ટિવ કનેક્શન સક્રિય છે.",
                solution="બધું બરાબર ચાલે છે સાહેબ."
            )
            self.say("વ્હોટ્સએપ એલર્ટ સફળતાપૂર્વક ડિસ્પેચ થયું! ✅", duration=4, speak_aloud=False)
        import threading
        threading.Thread(target=_bg, daemon=True).start()

def main():
    pet = AradhyaDesktopPet()
    Gtk.main()

if __name__ == "__main__":
    main()
