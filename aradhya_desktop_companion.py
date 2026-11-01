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
from gi.repository import Gtk, Gdk, GdkPixbuf, GLib
import cairo

SPRITES_DIR = BASE_DIR / "data" / "aradhya_pet" / "sprites"

# Voice greetings when clicked (BGMI Lobby Bot & Tactical Cyber Girl)
CLICK_GREETINGS = [
    "જય માતાજી અલ્પેશ સાહેબ! BGMI લોબીમાં આરાધ્યા આપની સાથે તૈયાર છે!",
    "વિનર વિનર ચિકન ડિનર! બોલો સાહેબ, કયું મિશન સ્ટાર્ટ કરવું છે?",
    "હા સાહેબ! લેવલ ૩ સાયબર પ્રોટેક્શન સમગ્ર લેપટોપ પર સક્રિય છે.",
    "બોલો અલ્પેશ સાહેબ! ડબલ-ક્લિક કરીને કમાન્ડ સેન્ટર લૉન્ચ કરો.",
    "આરાધ્યા આપની સર્વોચ્ચ એક્ઝિક્યુટિવ એજન્ટ છે, સાહેબ!"
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

        # Mouse Drag State
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.last_click_time = 0

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
            # Playing BGMI on smartphone in lobby!
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
            frames = ["dance_0", "dance_1"]
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
            # Switch to a random cute BGMI Lobby behavior
            choices = ["IDLE", "GAMING", "WAVING", "WALKING", "AIRDROP", "VICTORY"]
            weights = [30, 25, 15, 15, 8, 7]
            self.state = random.choices(choices, weights=weights)[0]
            self.target_state_duration = random.randint(6, 16)

            if self.state == "GAMING":
                self.say(random.choice(["BGMI લોબી મેચિંગ... 🎮", "ચિકન ડિનર કરીશું આજે! 🍗", "પ્લેઇંગ મોડ ઓન... 🕹️"]), duration=5)
            elif self.state == "WAVING":
                self.say("પ્રણામ અલ્પેશ સાહેબ! 👋", duration=4)
            elif self.state == "AIRDROP":
                self.say("એરડ્રોપ લૂંટ રેડી સાહેબ! 📦🔥", duration=4)
            elif self.state == "VICTORY":
                self.say("Winner Winner Chicken Dinner! 🏆", duration=4)
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
            # Check Double Click (within 350ms) -> Launch Terminal
            if now - self.last_click_time < 0.35:
                self.say("કમાન્ડ સેન્ટર લોન્ચિંગ... 🚀", duration=3, speak_aloud=False)
                self.launch_aradhya_terminal()
                self.last_click_time = 0
                return True

            self.last_click_time = now
            self.dragging = True
            self.drag_offset_x = int(event.x)
            self.drag_offset_y = int(event.y)

            # Trigger a cute reaction on single click
            self.state = "WAVING"
            greet = random.choice(CLICK_GREETINGS)
            self.say(greet, duration=5, speak_aloud=True)

        # Right Click (Button 3) -> Context Menu
        elif event.button == 3:
            self.show_context_menu(event)

        return True

    def on_button_release(self, widget, event):
        if event.button == 1:
            self.dragging = False
            self.state = "IDLE"
        return True

    def on_motion_notify(self, widget, event):
        if self.dragging:
            root_x, root_y = self.get_position()
            new_x = int(event.x_root - self.drag_offset_x)
            new_y = int(event.y_root - self.drag_offset_y)
            self.x = max(0, min(self.screen_width - self.pet_w, new_x))
            self.y = max(0, min(self.screen_height - self.pet_h, new_y))
            self.move(int(self.x), int(self.y))
        return True

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

        item_launch = Gtk.MenuItem(label="🚀 Launch Aradhya Console (ડબલ ક્લિક)")
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

def main():
    pet = AradhyaDesktopPet()
    Gtk.main()

if __name__ == "__main__":
    main()
