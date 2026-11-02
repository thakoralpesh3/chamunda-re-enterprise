#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya Tactical Cyber Companion Sprite Generator
Author: Aradhya (CEO)
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)

Visual Identity:
- Tactical Cyber Robot Girl companion.
- Sleek Communication Headset with Glowing Neon Mic and Cat-Ear Antennae.
- Tactical Mecha Bodysuit with Hologram Armor Plates, Neon Cyan / Gold Trims.
- Golden Chamunda Royal Badge on chest reactor.
- Dynamic Action & Idle Behaviors:
  1. SMARTPHONE_MONITORING: Monitoring systems on a glowing mini smartphone in idle time.
  2. WAVING: Enthusiastic tactical salute & cute waving to Alpesh Sir!
  3. IDLE_BREATH: Floating & hovering with subtle thrusters, observing the desktop environment.
  4. WALKING: Tactical cute walk / patrol along screen edge.
  5. VICTORY_DANCE: Cute celebration victory dance with hologram hearts & sparkles!
  6. SECURE_PACKAGE: Holding a mini glowing secure delivery crate!
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw

SPRITES_DIR = Path("/home/alpesh/chamunda_re_enterprise/data/aradhya_pet/sprites")
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 140, 160

# Palette - Tactical Sci-Fi Meets Cute Anime
C_SKIN = (255, 236, 226, 255)
C_BLUSH = (255, 130, 160, 190)
C_HAIR_CYBER = (110, 210, 255, 255)        # Neon Aqua Cyan
C_HAIR_DARK = (55, 120, 210, 255)
C_HAIR_LIGHT = (215, 248, 255, 255)
C_EYE_NAVY = (20, 50, 140, 255)
C_EYE_CYAN = (0, 230, 255, 255)
C_EYE_WHITE = (255, 255, 255, 255)

# Tactical Gear Colors
C_ARMOR_DARK = (24, 28, 40, 255)           # Tactical Matte Carbon
C_ARMOR_GREY = (50, 60, 80, 255)           # Titanium Plates
C_NEON_CYAN = (0, 255, 240, 255)           # Cyber Glow
C_GOLD = (255, 210, 40, 255)               # Chamunda Gold
C_NEON_ORANGE = (255, 130, 30, 255)        # Energy accent
C_PHONE_BODY = (35, 40, 55, 255)
C_PHONE_SCREEN = (0, 255, 200, 255)
C_AIRDROP_RED = (235, 45, 65, 255)
C_AIRDROP_BLUE = (35, 95, 225, 255)

def draw_aradhya_sprite(
    bob_y: int = 0,
    action: str = "idle",          # "idle", "phone", "wave", "walk", "dance", "airdrop"
    arm_left_mode: str = "default",
    arm_right_mode: str = "default",
    leg_phase: int = 0,            # 0=stand, 1=walk1, 2=walk2, 3=hover
    eye_state: str = "open",       # "open", "blink", "wink", "happy"
    mouth_state: str = "smile",    # "smile", "open", "cute_w"
    direction: int = 1,
    sub_frame: int = 0
) -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, 70 + bob_y

    # --- 1. Tactical Thrusters & Ground Shadow ---
    if leg_phase == 3 or action == "idle":
        # Hologram hover ring under boots
        glow_y = cy + 72
        d.ellipse([cx - 24, glow_y, cx + 24, glow_y + 8], fill=(0, 255, 240, 60))
        d.ellipse([cx - 14, glow_y + 1, cx + 14, glow_y + 5], fill=(255, 255, 255, 140))

    # --- 2. Cyber Back Hair (flowing twintails with neon clips) ---
    # Left hair tail
    d.polygon([(cx - 28, cy - 10), (cx - 48, cy + 25), (cx - 42, cy + 48), (cx - 26, cy + 30)], fill=C_HAIR_DARK)
    d.line([cx - 44, cy + 10, cx - 38, cy + 40], fill=C_NEON_CYAN, width=2)
    # Right hair tail
    d.polygon([(cx + 28, cy - 10), (cx + 48, cy + 25), (cx + 42, cy + 48), (cx + 26, cy + 30)], fill=C_HAIR_DARK)
    d.line([cx + 44, cy + 10, cx + 38, cy + 40], fill=C_NEON_CYAN, width=2)

    # --- 3. Legs & Cyber Tactical Boots ---
    leg_y = cy + 42
    if leg_phase == 0 or leg_phase == 3:  # Stand / Hover
        # Left Leg
        d.rounded_rectangle([cx - 18, leg_y, cx - 6, leg_y + 28], radius=4, fill=C_ARMOR_DARK)
        d.rounded_rectangle([cx - 19, leg_y + 14, cx - 5, leg_y + 28], radius=3, fill=C_ARMOR_GREY) # Boot
        d.line([cx - 18, leg_y + 18, cx - 6, leg_y + 18], fill=C_NEON_CYAN, width=2)
        d.ellipse([cx - 14, leg_y + 24, cx - 10, leg_y + 27], fill=C_GOLD)
        # Right Leg
        d.rounded_rectangle([cx + 6, leg_y, cx + 18, leg_y + 28], radius=4, fill=C_ARMOR_DARK)
        d.rounded_rectangle([cx + 5, leg_y + 14, cx + 19, leg_y + 28], radius=3, fill=C_ARMOR_GREY)
        d.line([cx + 6, leg_y + 18, cx + 18, leg_y + 18], fill=C_NEON_CYAN, width=2)
        d.ellipse([cx + 10, leg_y + 24, cx + 14, leg_y + 27], fill=C_GOLD)
    elif leg_phase == 1:  # Walk step A
        d.rounded_rectangle([cx - 20, leg_y - 2, cx - 8, leg_y + 24], radius=4, fill=C_ARMOR_DARK)
        d.rounded_rectangle([cx + 6, leg_y + 3, cx + 18, leg_y + 29], radius=4, fill=C_ARMOR_DARK)
        d.line([cx - 20, leg_y + 14, cx - 8, leg_y + 14], fill=C_NEON_CYAN, width=2)
        d.line([cx + 6, leg_y + 21, cx + 18, leg_y + 21], fill=C_NEON_CYAN, width=2)
    elif leg_phase == 2:  # Walk step B
        d.rounded_rectangle([cx - 18, leg_y + 3, cx - 6, leg_y + 29], radius=4, fill=C_ARMOR_DARK)
        d.rounded_rectangle([cx + 8, leg_y - 2, cx + 20, leg_y + 24], radius=4, fill=C_ARMOR_DARK)
        d.line([cx - 18, leg_y + 21, cx - 6, leg_y + 21], fill=C_NEON_CYAN, width=2)
        d.line([cx + 8, leg_y + 14, cx + 20, leg_y + 14], fill=C_NEON_CYAN, width=2)

    # --- 4. Tactical Bodysuit & Level 3 Armor Vest ---
    torso_rect = [cx - 22, cy + 10, cx + 22, cy + 44]
    d.rounded_rectangle(torso_rect, radius=7, fill=C_ARMOR_DARK)
    # Tactical chest plate
    d.rounded_rectangle([cx - 17, cy + 12, cx + 17, cy + 32], radius=5, fill=C_ARMOR_GREY)
    # Neon Holo Arc Reactor (Ray Buddy signature)
    d.ellipse([cx - 8, cy + 16, cx + 8, cy + 28], fill=C_NEON_CYAN)
    d.ellipse([cx - 4, cy + 19, cx + 4, cy + 25], fill=(255, 255, 255, 255))
    # Tactical utility belt & pouch
    d.rectangle([cx - 20, cy + 34, cx + 20, cy + 42], fill=(16, 20, 30, 255))
    d.rounded_rectangle([cx - 16, cy + 36, cx - 8, cy + 42], radius=2, fill=C_GOLD)      # Medkit / Ammo Pouch
    d.rounded_rectangle([cx + 8, cy + 36, cx + 16, cy + 42], radius=2, fill=C_NEON_CYAN) # Holo Battery
    d.ellipse([cx - 3, cy + 36, cx + 3, cy + 42], fill=C_NEON_ORANGE)

    # --- 5. Arms & Prop Hands based on Action ---
    if action == "phone":
        # Holding glowing cyber smartphone in both hands playing BGMI!
        d.polygon([(cx - 22, cy + 16), (cx - 12, cy + 28), (cx - 6, cy + 36), (cx - 20, cy + 30)], fill=C_ARMOR_GREY)
        d.polygon([(cx + 22, cy + 16), (cx + 12, cy + 28), (cx + 6, cy + 36), (cx + 20, cy + 30)], fill=C_ARMOR_GREY)
        # Phone Body
        phone_tilt = -1 if sub_frame % 2 == 0 else 1
        px, py = cx + phone_tilt, cy + 30
        d.rounded_rectangle([px - 16, py - 4, px + 16, py + 12], radius=3, fill=C_PHONE_BODY, outline=C_GOLD, width=1)
        d.rectangle([px - 14, py - 2, px + 14, py + 10], fill=C_PHONE_SCREEN)
        # Screen Mini Joystick & Action Buttons (playing BGMI)
        d.ellipse([px - 11, py + 1, px - 6, py + 6], fill=(0, 100, 255, 255))
        d.ellipse([px + 7, py + 2, px + 11, py + 6], fill=C_NEON_ORANGE)
        # Thumbs tapping
        d.ellipse([px - 14, py + 2, px - 10, py + 7], fill=C_SKIN)
        d.ellipse([px + 10, py + 2, px + 14, py + 7], fill=C_SKIN)
        # Screen glow beam
        d.polygon([(px - 12, py - 3), (px + 12, py - 3), (cx + 16, cy + 6), (cx - 16, cy + 6)], fill=(0, 255, 220, 40))

    elif action == "wave":
        # Left Arm Waving High (Saluting / Welcoming Alpesh Sir)
        wave_tilt = -4 if sub_frame % 2 == 0 else 4
        d.polygon([(cx - 22, cy + 16), (cx - 36 + wave_tilt, cy - 8), (cx - 44 + wave_tilt, cy - 4), (cx - 26, cy + 22)], fill=C_ARMOR_GREY)
        d.ellipse([cx - 48 + wave_tilt, cy - 14, cx - 34 + wave_tilt, cy - 2], fill=C_SKIN) # Hand
        # Hologram Wave Rings
        d.arc([cx - 54 + wave_tilt, cy - 20, cx - 28 + wave_tilt, cy + 4], start=180, end=300, fill=C_NEON_CYAN, width=2)
        # Right Arm on Hip / Rest
        d.rounded_rectangle([cx + 20, cy + 14, cx + 29, cy + 36], radius=4, fill=C_ARMOR_GREY)
        d.ellipse([cx + 19, cy + 34, cx + 30, cy + 42], fill=C_SKIN)

    elif action == "airdrop":
        # Holding Mini Glowing Airdrop Crate like a trophy!
        d.polygon([(cx - 22, cy + 16), (cx - 10, cy + 26), (cx - 6, cy + 36), (cx - 20, cy + 30)], fill=C_ARMOR_GREY)
        d.polygon([(cx + 22, cy + 16), (cx + 10, cy + 26), (cx + 6, cy + 36), (cx + 20, cy + 30)], fill=C_ARMOR_GREY)
        # Airdrop Crate (Red top, Blue bottom, iconic BGMI)
        ax, ay = cx, cy + 30
        d.rectangle([ax - 12, ay - 6, ax + 12, ay + 1], fill=C_AIRDROP_RED)    # Red Roof
        d.rectangle([ax - 12, ay + 1, ax + 12, ay + 12], fill=C_AIRDROP_BLUE) # Blue Box
        d.line([ax - 12, ay + 4, ax + 12, ay + 4], fill=C_GOLD, width=1)       # Crate Straps
        d.line([ax, ay - 6, ax, ay + 12], fill=C_GOLD, width=1)
        # Flare Smoke puff above crate
        d.ellipse([ax - 4, ay - 14, ax + 4, ay - 7], fill=(255, 60, 60, 180))
        d.ellipse([ax - 2, ay - 18, ax + 3, ay - 13], fill=(255, 120, 120, 120))

    elif action == "dance":
        # Victory Emote Dance (arms in happy diagonal victory pose)
        d.polygon([(cx - 22, cy + 16), (cx - 38, cy + 2), (cx - 44, cy + 8), (cx - 26, cy + 22)], fill=C_ARMOR_GREY)
        d.ellipse([cx - 48, cy + 2, cx - 36, cy + 14], fill=C_SKIN)
        d.polygon([(cx + 22, cy + 16), (cx + 38, cy - 8), (cx + 44, cy - 4), (cx + 26, cy + 20)], fill=C_ARMOR_GREY)
        d.ellipse([cx + 36, cy - 14, cx + 48, cy - 2], fill=C_SKIN)

    else:  # Default / Idle / Walk arms
        d.rounded_rectangle([cx - 29, cy + 14, cx - 20, cy + 36], radius=4, fill=C_ARMOR_GREY)
        d.ellipse([cx - 30, cy + 34, cx - 19, cy + 42], fill=C_SKIN)
        d.rounded_rectangle([cx + 20, cy + 14, cx + 29, cy + 36], radius=4, fill=C_ARMOR_GREY)
        d.ellipse([cx + 19, cy + 34, cx + 30, cy + 42], fill=C_SKIN)

    # --- 6. Tactical Gaming Headset with Glowing Robot Antennae ---
    ear_y = cy - 38
    # Left Cyber Antenna
    d.polygon([(cx - 34, ear_y + 10), (cx - 48, ear_y - 20), (cx - 22, ear_y - 4)], fill=C_ARMOR_DARK)
    d.polygon([(cx - 36, ear_y + 4), (cx - 46, ear_y - 14), (cx - 28, ear_y - 4)], fill=C_NEON_CYAN)
    # Right Cyber Antenna
    d.polygon([(cx + 34, ear_y + 10), (cx + 48, ear_y - 20), (cx + 22, ear_y - 4)], fill=C_ARMOR_DARK)
    d.polygon([(cx + 36, ear_y + 4), (cx + 46, ear_y - 14), (cx + 28, ear_y - 4)], fill=C_NEON_CYAN)

    # Pro Gaming Headset Band across head
    d.arc([cx - 36, cy - 42, cx + 36, cy - 12], start=190, end=350, fill=C_ARMOR_DARK, width=6)
    d.arc([cx - 34, cy - 40, cx + 34, cy - 14], start=195, end=345, fill=C_NEON_CYAN, width=2)
    # Earcups
    d.ellipse([cx - 40, cy - 24, cx - 30, cy - 6], fill=C_ARMOR_GREY)
    d.ellipse([cx - 38, cy - 21, cx - 32, cy - 9], fill=C_GOLD)
    d.ellipse([cx + 30, cy - 24, cx + 40, cy - 6], fill=C_ARMOR_GREY)
    d.ellipse([cx + 32, cy - 21, cx + 38, cy - 9], fill=C_GOLD)
    # Boom Microphone extending to mouth
    d.arc([cx + 8, cy - 12, cx + 34, cy + 10], start=30, end=130, fill=C_ARMOR_DARK, width=2)
    d.ellipse([cx + 9, cy + 6, cx + 15, cy + 12], fill=C_NEON_CYAN) # Glowing Mic tip

    # --- 7. Head & Anime Face ---
    head_box = [cx - 34, cy - 36, cx + 34, cy + 18]
    d.ellipse(head_box, fill=C_SKIN)

    # Cute Cheeks Blush
    d.ellipse([cx - 26, cy + 2, cx - 14, cy + 10], fill=C_BLUSH)
    d.ellipse([cx + 14, cy + 2, cx + 26, cy + 10], fill=C_BLUSH)

    # --- 8. Sparkly Anime Eyes ---
    lx, rx, eye_y = cx - 16, cx + 16, cy - 6
    if eye_state == "open":
        # Left Eye
        d.ellipse([lx - 9, eye_y - 11, lx + 9, eye_y + 9], fill=C_EYE_NAVY)
        d.ellipse([lx - 7, eye_y - 7, lx + 7, eye_y + 8], fill=C_EYE_CYAN)
        d.ellipse([lx - 5, eye_y - 8, lx + 1, eye_y - 3], fill=C_EYE_WHITE)
        d.ellipse([lx + 2, eye_y + 2, lx + 5, eye_y + 5], fill=C_EYE_WHITE)
        d.arc([lx - 10, eye_y - 14, lx + 10, eye_y - 6], start=200, end=340, fill=C_ARMOR_DARK, width=2)
        # Right Eye
        d.ellipse([rx - 9, eye_y - 11, rx + 9, eye_y + 9], fill=C_EYE_NAVY)
        d.ellipse([rx - 7, eye_y - 7, rx + 7, eye_y + 8], fill=C_EYE_CYAN)
        d.ellipse([rx - 5, eye_y - 8, rx + 1, eye_y - 3], fill=C_EYE_WHITE)
        d.ellipse([rx + 2, eye_y + 2, rx + 5, eye_y + 5], fill=C_EYE_WHITE)
        d.arc([rx - 10, eye_y - 14, rx + 10, eye_y - 6], start=200, end=340, fill=C_ARMOR_DARK, width=2)
    elif eye_state == "blink":
        d.arc([lx - 9, eye_y - 4, lx + 9, eye_y + 8], start=20, end=160, fill=C_ARMOR_DARK, width=3)
        d.arc([rx - 9, eye_y - 4, rx + 9, eye_y + 8], start=20, end=160, fill=C_ARMOR_DARK, width=3)
    elif eye_state == "wink":
        d.ellipse([lx - 9, eye_y - 11, lx + 9, eye_y + 9], fill=C_EYE_NAVY)
        d.ellipse([lx - 7, eye_y - 7, lx + 7, eye_y + 8], fill=C_EYE_CYAN)
        d.ellipse([lx - 5, eye_y - 8, lx + 1, eye_y - 3], fill=C_EYE_WHITE)
        d.arc([rx - 9, eye_y - 4, rx + 9, eye_y + 8], start=20, end=160, fill=C_ARMOR_DARK, width=3)
    elif eye_state == "happy":
        d.arc([lx - 9, eye_y - 8, lx + 9, eye_y + 6], start=190, end=350, fill=C_EYE_NAVY, width=3)
        d.arc([rx - 9, eye_y - 8, rx + 9, eye_y + 6], start=190, end=350, fill=C_EYE_NAVY, width=3)

    # --- 9. Mouth Expression ---
    mouth_y = cy + 6
    if mouth_state == "smile":
        d.arc([cx - 6, mouth_y - 2, cx + 6, mouth_y + 6], start=20, end=160, fill=C_ARMOR_DARK, width=2)
    elif mouth_state == "open":
        d.chord([cx - 7, mouth_y - 2, cx + 7, mouth_y + 8], start=0, end=180, fill=(255, 110, 130, 255), outline=C_ARMOR_DARK)
    elif mouth_state == "cute_w":
        d.arc([cx - 7, mouth_y - 2, cx - 1, mouth_y + 5], start=20, end=160, fill=C_ARMOR_DARK, width=2)
        d.arc([cx + 1, mouth_y - 2, cx + 7, mouth_y + 5], start=20, end=160, fill=C_ARMOR_DARK, width=2)

    # --- 10. Front Hair Bangs with Cyber Locks ---
    hair_top = [cx - 36, cy - 42, cx + 36, cy - 10]
    d.ellipse(hair_top, fill=C_HAIR_CYBER)
    # Bangs
    d.polygon([(cx - 36, cy - 24), (cx - 24, cy - 4), (cx - 18, cy - 18)], fill=C_HAIR_CYBER)
    d.polygon([(cx - 20, cy - 20), (cx - 8, cy - 2), (cx + 0, cy - 20)], fill=C_HAIR_LIGHT)
    d.polygon([(cx - 2, cy - 20), (cx + 14, cy - 3), (cx + 20, cy - 20)], fill=C_HAIR_CYBER)
    d.polygon([(cx + 18, cy - 20), (cx + 34, cy - 5), (cx + 38, cy - 24)], fill=C_HAIR_DARK)

    # Chamunda Gold Badge Pin on Hair
    d.polygon([(cx - 24, cy - 30), (cx - 28, cy - 24), (cx - 20, cy - 24)], fill=C_GOLD)

    return img

print("Rendering Tactical Cyber Companion Sprite Frames for Aradhya...")

# 1. IDLE / HOVER FRAMES (Floating / breathing companion)
draw_aradhya_sprite(bob_y=0, action="idle", leg_phase=3, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_0.png")
draw_aradhya_sprite(bob_y=1, action="idle", leg_phase=3, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_1.png")
draw_aradhya_sprite(bob_y=2, action="idle", leg_phase=3, eye_state="blink", mouth_state="smile").save(SPRITES_DIR / "idle_2.png")
draw_aradhya_sprite(bob_y=1, action="idle", leg_phase=3, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_3.png")

# 2. SMARTPHONE FRAMES (Inspecting system status on smartphone)
draw_aradhya_sprite(bob_y=0, action="phone", eye_state="happy", mouth_state="open", sub_frame=0).save(SPRITES_DIR / "game_0.png")
draw_aradhya_sprite(bob_y=1, action="phone", eye_state="open", mouth_state="cute_w", sub_frame=1).save(SPRITES_DIR / "game_1.png")
draw_aradhya_sprite(bob_y=0, action="phone", eye_state="wink", mouth_state="smile", sub_frame=2).save(SPRITES_DIR / "game_2.png")
draw_aradhya_sprite(bob_y=1, action="phone", eye_state="happy", mouth_state="open", sub_frame=3).save(SPRITES_DIR / "game_3.png")

# 3. WAVING FRAMES (Saluting / Greeting Alpesh Sir)
draw_aradhya_sprite(bob_y=0, action="wave", eye_state="happy", mouth_state="open", sub_frame=0).save(SPRITES_DIR / "wave_0.png")
draw_aradhya_sprite(bob_y=1, action="wave", eye_state="wink", mouth_state="smile", sub_frame=1).save(SPRITES_DIR / "wave_1.png")
draw_aradhya_sprite(bob_y=0, action="wave", eye_state="open", mouth_state="open", sub_frame=2).save(SPRITES_DIR / "wave_2.png")
draw_aradhya_sprite(bob_y=1, action="wave", eye_state="happy", mouth_state="smile", sub_frame=3).save(SPRITES_DIR / "wave_3.png")

# 4. WALKING FRAMES (Patrolling desktop edge)
draw_aradhya_sprite(bob_y=0, action="walk", leg_phase=1, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_0.png")
draw_aradhya_sprite(bob_y=1, action="walk", leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_1.png")
draw_aradhya_sprite(bob_y=0, action="walk", leg_phase=2, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_2.png")
draw_aradhya_sprite(bob_y=1, action="walk", leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_3.png")

# 5. SECURE PACKAGE
draw_aradhya_sprite(bob_y=0, action="airdrop", eye_state="happy", mouth_state="open").save(SPRITES_DIR / "airdrop_0.png")
draw_aradhya_sprite(bob_y=-2, action="airdrop", eye_state="wink", mouth_state="smile").save(SPRITES_DIR / "airdrop_1.png")

# 6. VICTORY DANCE / CHEER (Celebration)
draw_aradhya_sprite(bob_y=0, action="dance", eye_state="happy", mouth_state="open").save(SPRITES_DIR / "dance_0.png")
draw_aradhya_sprite(bob_y=-2, action="dance", eye_state="wink", mouth_state="smile").save(SPRITES_DIR / "dance_1.png")

print(f"✅ Successfully rendered 20 Cyber Companion Sprite Frames into {SPRITES_DIR}!")
