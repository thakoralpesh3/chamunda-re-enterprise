#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aradhya 2D Chibi Robot Girl Sprite Sheet & Animation Generator
Author: Aradhya (CEO)
Dedicated to: Alpesh Sir (Founder, Chairman & Master Tech)

Draws beautiful, high-definition 2D anime-style chibi robot girl sprites with:
- Cybernetic glowing cat/antenna robot ears
- Soft lilac/cyan futuristic hair
- Sparkly anime eyes (open, blink, happy wink)
- Cute robot maid/tech bodysuit with glowing teal arc-reactor chest badge
- Smooth multi-frame animations:
  1. IDLE (breathing, soft floating hover, eye blinks)
  2. WAVING (arm waving greeting Alpesh Sir with cute smile)
  3. WALKING (cute walking steps across the screen bottom)
  4. CUTE_HEART / SPARKLE (holding glowing heart / cheering)
  5. FLOATING / JETPACK (flying with gentle thruster flame)
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw

SPRITES_DIR = Path("/home/alpesh/chamunda_re_enterprise/data/aradhya_pet/sprites")
SPRITES_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 140, 160

# Palette
C_SKIN = (255, 235, 225, 255)
C_BLUSH = (255, 140, 160, 180)
C_HAIR_BASE = (130, 200, 255, 255)       # Cyber Cyan
C_HAIR_SHADOW = (90, 150, 230, 255)
C_HAIR_HIGHLIGHT = (210, 245, 255, 255)
C_EYE_OUTER = (30, 80, 180, 255)
C_EYE_CORE = (0, 210, 255, 255)
C_EYE_WHITE = (255, 255, 255, 255)
C_SUIT_DARK = (28, 34, 48, 255)          # Sleek titanium tech suit
C_SUIT_WHITE = (240, 245, 255, 255)
C_TEAL_GLOW = (0, 255, 230, 255)         # Aradhya Cyan Glow
C_GOLD_ACCENT = (255, 215, 0, 255)       # Royal Gold
C_EAR_INNER = (255, 120, 160, 255)

def draw_chibi_aradhya(
    bob_y: int = 0,
    arm_left_pose: str = "down",   # "down", "wave_up", "wave_mid", "heart"
    arm_right_pose: str = "down",  # "down", "heart"
    leg_phase: int = 0,            # 0=standing, 1=walk_left, 2=walk_right, 3=floating
    eye_state: str = "open",       # "open", "blink", "wink", "happy"
    mouth_state: str = "smile",    # "smile", "open", "cute_w"
    show_heart: bool = False,
    thruster_glow: bool = False
) -> Image.Image:
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, 70 + bob_y

    # --- 1. Thruster Glow if floating ---
    if thruster_glow:
        flame_y = cy + 62
        d.ellipse([cx - 16, flame_y, cx + 16, flame_y + 14], fill=(0, 220, 255, 120))
        d.ellipse([cx - 8, flame_y + 2, cx + 8, flame_y + 18], fill=(255, 255, 255, 220))

    # --- 2. Cyber Ribbon / Back Hair (Bangs behind body) ---
    back_hair_pts = [
        (cx - 38, cy - 10), (cx - 45, cy + 35), (cx - 28, cy + 45),
        (cx + 28, cy + 45), (cx + 45, cy + 35), (cx + 38, cy - 10)
    ]
    d.polygon(back_hair_pts, fill=C_HAIR_SHADOW)

    # --- 3. Legs / Boots ---
    leg_y = cy + 42
    if leg_phase == 0:  # Standing
        d.rounded_rectangle([cx - 18, leg_y, cx - 6, leg_y + 30], radius=4, fill=C_SUIT_DARK)
        d.rounded_rectangle([cx + 6, leg_y, cx + 18, leg_y + 30], radius=4, fill=C_SUIT_DARK)
        # Boot neon rings
        d.line([cx - 18, leg_y + 18, cx - 6, leg_y + 18], fill=C_TEAL_GLOW, width=2)
        d.line([cx + 6, leg_y + 18, cx + 18, leg_y + 18], fill=C_TEAL_GLOW, width=2)
    elif leg_phase == 1:  # Walk A
        d.rounded_rectangle([cx - 20, leg_y - 3, cx - 8, leg_y + 26], radius=4, fill=C_SUIT_DARK)
        d.rounded_rectangle([cx + 6, leg_y + 2, cx + 18, leg_y + 31], radius=4, fill=C_SUIT_DARK)
        d.line([cx - 20, leg_y + 14, cx - 8, leg_y + 14], fill=C_TEAL_GLOW, width=2)
        d.line([cx + 6, leg_y + 20, cx + 18, leg_y + 20], fill=C_TEAL_GLOW, width=2)
    elif leg_phase == 2:  # Walk B
        d.rounded_rectangle([cx - 18, leg_y + 2, cx - 6, leg_y + 31], radius=4, fill=C_SUIT_DARK)
        d.rounded_rectangle([cx + 8, leg_y - 3, cx + 20, leg_y + 26], radius=4, fill=C_SUIT_DARK)
        d.line([cx - 18, leg_y + 20, cx - 6, leg_y + 20], fill=C_TEAL_GLOW, width=2)
        d.line([cx + 8, leg_y + 14, cx + 20, leg_y + 14], fill=C_TEAL_GLOW, width=2)
    elif leg_phase == 3:  # Floating knees bent
        d.rounded_rectangle([cx - 16, leg_y, cx - 6, leg_y + 22], radius=4, fill=C_SUIT_DARK)
        d.rounded_rectangle([cx + 6, leg_y + 2, cx + 16, leg_y + 24], radius=4, fill=C_SUIT_DARK)
        d.line([cx - 16, leg_y + 14, cx - 6, leg_y + 14], fill=C_TEAL_GLOW, width=2)
        d.line([cx + 6, leg_y + 16, cx + 16, leg_y + 16], fill=C_TEAL_GLOW, width=2)

    # --- 4. Bodysuit / Torso ---
    torso_rect = [cx - 22, cy + 10, cx + 22, cy + 44]
    d.rounded_rectangle(torso_rect, radius=8, fill=C_SUIT_WHITE)
    # Tech corset / belt
    d.rectangle([cx - 20, cy + 28, cx + 20, cy + 42], fill=C_SUIT_DARK)
    # Golden belt buckle
    d.rounded_rectangle([cx - 6, cy + 32, cx + 6, cy + 38], radius=2, fill=C_GOLD_ACCENT)
    # Glowing Arc-Reactor Core
    d.ellipse([cx - 8, cy + 16, cx + 8, cy + 30], fill=C_TEAL_GLOW)
    d.ellipse([cx - 4, cy + 20, cx + 4, cy + 26], fill=(255, 255, 255, 255))

    # --- 5. Arms ---
    # Left Arm (Viewer's left)
    if arm_left_pose == "down":
        d.rounded_rectangle([cx - 30, cy + 14, cx - 20, cy + 38], radius=4, fill=C_SUIT_WHITE)
        d.ellipse([cx - 31, cy + 36, cx - 19, cy + 44], fill=C_SKIN)  # Hand
    elif arm_left_pose == "wave_up":
        # Waving high
        d.polygon([(cx - 22, cy + 16), (cx - 38, cy - 8), (cx - 46, cy - 4), (cx - 28, cy + 20)], fill=C_SUIT_WHITE)
        d.ellipse([cx - 48, cy - 14, cx - 34, cy + 0], fill=C_SKIN)   # Waving hand
    elif arm_left_pose == "wave_mid":
        # Waving mid
        d.polygon([(cx - 22, cy + 16), (cx - 42, cy + 2), (cx - 46, cy + 8), (cx - 28, cy + 20)], fill=C_SUIT_WHITE)
        d.ellipse([cx - 48, cy + 2, cx - 36, cy + 14], fill=C_SKIN)
    elif arm_left_pose == "heart":
        d.polygon([(cx - 22, cy + 16), (cx - 10, cy + 20), (cx - 12, cy + 28), (cx - 26, cy + 24)], fill=C_SUIT_WHITE)
        d.ellipse([cx - 12, cy + 20, cx - 2, cy + 30], fill=C_SKIN)

    # Right Arm (Viewer's right)
    if arm_right_pose == "down":
        d.rounded_rectangle([cx + 20, cy + 14, cx + 30, cy + 38], radius=4, fill=C_SUIT_WHITE)
        d.ellipse([cx + 19, cy + 36, cx + 31, cy + 44], fill=C_SKIN)
    elif arm_right_pose == "heart":
        d.polygon([(cx + 22, cy + 16), (cx + 10, cy + 20), (cx + 12, cy + 28), (cx + 26, cy + 24)], fill=C_SUIT_WHITE)
        d.ellipse([cx + 2, cy + 20, cx + 12, cy + 30], fill=C_SKIN)

    # --- 6. Cute Robot Ears (Mecha Cat Ears) ---
    ear_y = cy - 38
    # Left Ear
    d.polygon([(cx - 36, ear_y + 12), (cx - 48, ear_y - 18), (cx - 22, ear_y - 2)], fill=C_SUIT_DARK)
    d.polygon([(cx - 38, ear_y + 6), (cx - 46, ear_y - 12), (cx - 28, ear_y - 2)], fill=C_TEAL_GLOW)
    # Right Ear
    d.polygon([(cx + 36, ear_y + 12), (cx + 48, ear_y - 18), (cx + 22, ear_y - 2)], fill=C_SUIT_DARK)
    d.polygon([(cx + 38, ear_y + 6), (cx + 48, ear_y - 12), (cx + 28, ear_y - 2)], fill=C_TEAL_GLOW)

    # Glowing Antenna Rod on Right Ear
    d.line([cx + 44, ear_y - 16, cx + 52, ear_y - 26], fill=C_GOLD_ACCENT, width=2)
    d.ellipse([cx + 50, ear_y - 30, cx + 56, ear_y - 24], fill=C_TEAL_GLOW)

    # --- 7. Head & Face ---
    head_box = [cx - 34, cy - 36, cx + 34, cy + 18]
    d.ellipse(head_box, fill=C_SKIN)

    # Cheeks Blush
    d.ellipse([cx - 26, cy + 2, cx - 14, cy + 10], fill=C_BLUSH)
    d.ellipse([cx + 14, cy + 2, cx + 26, cy + 10], fill=C_BLUSH)

    # --- 8. Eyes ---
    lx, rx, eye_y = cx - 16, cx + 16, cy - 6
    if eye_state == "open":
        # Left Eye
        d.ellipse([lx - 9, eye_y - 11, lx + 9, eye_y + 9], fill=C_EYE_OUTER)
        d.ellipse([lx - 7, eye_y - 8, lx + 7, eye_y + 7], fill=C_EYE_CORE)
        d.ellipse([lx - 5, eye_y - 8, lx + 0, eye_y - 3], fill=C_EYE_WHITE)  # Big gleam
        d.ellipse([lx + 2, eye_y + 1, lx + 5, eye_y + 4], fill=C_EYE_WHITE)  # Small gleam
        d.arc([lx - 10, eye_y - 14, lx + 10, eye_y - 6], start=200, end=340, fill=C_SUIT_DARK, width=2)

        # Right Eye
        d.ellipse([rx - 9, eye_y - 11, rx + 9, eye_y + 9], fill=C_EYE_OUTER)
        d.ellipse([rx - 7, eye_y - 8, rx + 7, eye_y + 7], fill=C_EYE_CORE)
        d.ellipse([rx - 5, eye_y - 8, rx + 0, eye_y - 3], fill=C_EYE_WHITE)
        d.ellipse([rx + 2, eye_y + 1, rx + 5, eye_y + 4], fill=C_EYE_WHITE)
        d.arc([rx - 10, eye_y - 14, rx + 10, eye_y - 6], start=200, end=340, fill=C_SUIT_DARK, width=2)
    elif eye_state == "blink":
        # Closed line
        d.arc([lx - 9, eye_y - 4, lx + 9, eye_y + 8], start=20, end=160, fill=C_SUIT_DARK, width=3)
        d.arc([rx - 9, eye_y - 4, rx + 9, eye_y + 8], start=20, end=160, fill=C_SUIT_DARK, width=3)
    elif eye_state == "wink":
        # Left open, right closed winking
        d.ellipse([lx - 9, eye_y - 11, lx + 9, eye_y + 9], fill=C_EYE_OUTER)
        d.ellipse([lx - 7, eye_y - 8, lx + 7, eye_y + 7], fill=C_EYE_CORE)
        d.ellipse([lx - 5, eye_y - 8, lx + 0, eye_y - 3], fill=C_EYE_WHITE)
        d.arc([rx - 9, eye_y - 4, rx + 9, eye_y + 8], start=20, end=160, fill=C_SUIT_DARK, width=3)
    elif eye_state == "happy":
        # Both happy curved eyes (^_^)
        d.arc([lx - 9, eye_y - 8, lx + 9, eye_y + 6], start=190, end=350, fill=C_EYE_OUTER, width=3)
        d.arc([rx - 9, eye_y - 8, rx + 9, eye_y + 6], start=190, end=350, fill=C_EYE_OUTER, width=3)

    # --- 9. Mouth ---
    mouth_y = cy + 6
    if mouth_state == "smile":
        d.arc([cx - 6, mouth_y - 2, cx + 6, mouth_y + 6], start=20, end=160, fill=C_SUIT_DARK, width=2)
    elif mouth_state == "open":
        d.chord([cx - 7, mouth_y - 2, cx + 7, mouth_y + 9], start=0, end=180, fill=(255, 120, 140, 255), outline=C_SUIT_DARK)
    elif mouth_state == "cute_w":
        d.arc([cx - 7, mouth_y - 2, cx - 1, mouth_y + 5], start=20, end=160, fill=C_SUIT_DARK, width=2)
        d.arc([cx + 1, mouth_y - 2, cx + 7, mouth_y + 5], start=20, end=160, fill=C_SUIT_DARK, width=2)

    # --- 10. Front Hair & Bangs ---
    hair_top = [cx - 36, cy - 42, cx + 36, cy - 10]
    d.ellipse(hair_top, fill=C_HAIR_BASE)
    # Bangs locks
    d.polygon([(cx - 36, cy - 24), (cx - 24, cy - 4), (cx - 18, cy - 18)], fill=C_HAIR_BASE)
    d.polygon([(cx - 20, cy - 20), (cx - 8, cy - 2), (cx + 0, cy - 20)], fill=C_HAIR_HIGHLIGHT)
    d.polygon([(cx - 2, cy - 20), (cx + 14, cy - 3), (cx + 20, cy - 20)], fill=C_HAIR_BASE)
    d.polygon([(cx + 18, cy - 20), (cx + 34, cy - 5), (cx + 38, cy - 24)], fill=C_HAIR_SHADOW)

    # Headband with Chamunda Gold Star
    d.arc([cx - 34, cy - 38, cx + 34, cy - 14], start=190, end=350, fill=C_SUIT_DARK, width=4)
    d.line([cx - 30, cy - 26, cx + 30, cy - 26], fill=C_TEAL_GLOW, width=1)
    d.ellipse([cx - 5, cy - 32, cx + 5, cy - 22], fill=C_GOLD_ACCENT)

    # --- 11. Heart Effect if Cheer ---
    if show_heart:
        hx, hy = cx, cy + 24
        d.polygon([(hx - 12, hy - 4), (hx - 16, hy - 14), (hx - 4, hy - 18),
                   (hx, hy - 12), (hx + 4, hy - 18), (hx + 16, hy - 14),
                   (hx + 12, hy - 4), (hx, hy + 6)], fill=(255, 70, 130, 255))
        d.ellipse([hx - 4, hy - 10, hx + 4, hy - 2], fill=(255, 200, 230, 255))

    return img

print("Generating Aradhya Sprite Frames...")

# 1. IDLE FRAMES (Soft Breathing, Hovering, Blink)
draw_chibi_aradhya(bob_y=0, leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_0.png")
draw_chibi_aradhya(bob_y=1, leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_1.png")
draw_chibi_aradhya(bob_y=2, leg_phase=0, eye_state="blink", mouth_state="smile").save(SPRITES_DIR / "idle_2.png")
draw_chibi_aradhya(bob_y=1, leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "idle_3.png")

# 2. WAVING FRAMES (Waving to Alpesh Sir)
draw_chibi_aradhya(bob_y=0, arm_left_pose="wave_up", eye_state="happy", mouth_state="open").save(SPRITES_DIR / "wave_0.png")
draw_chibi_aradhya(bob_y=1, arm_left_pose="wave_mid", eye_state="wink", mouth_state="smile").save(SPRITES_DIR / "wave_1.png")
draw_chibi_aradhya(bob_y=0, arm_left_pose="wave_up", eye_state="open", mouth_state="open").save(SPRITES_DIR / "wave_2.png")
draw_chibi_aradhya(bob_y=1, arm_left_pose="wave_mid", eye_state="happy", mouth_state="smile").save(SPRITES_DIR / "wave_3.png")

# 3. WALKING FRAMES (Walking along the screen)
draw_chibi_aradhya(bob_y=0, leg_phase=1, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_0.png")
draw_chibi_aradhya(bob_y=1, leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_1.png")
draw_chibi_aradhya(bob_y=0, leg_phase=2, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_2.png")
draw_chibi_aradhya(bob_y=1, leg_phase=0, eye_state="open", mouth_state="smile").save(SPRITES_DIR / "walk_3.png")

# 4. CUTE CHEER / HEART FRAMES
draw_chibi_aradhya(bob_y=0, arm_left_pose="heart", arm_right_pose="heart", eye_state="happy", mouth_state="open", show_heart=True).save(SPRITES_DIR / "cheer_0.png")
draw_chibi_aradhya(bob_y=-2, arm_left_pose="heart", arm_right_pose="heart", eye_state="wink", mouth_state="smile", show_heart=True).save(SPRITES_DIR / "cheer_1.png")

# 5. FLOATING / HOVER FRAMES (Jetpack flight)
draw_chibi_aradhya(bob_y=-4, leg_phase=3, eye_state="open", mouth_state="open", thruster_glow=True).save(SPRITES_DIR / "float_0.png")
draw_chibi_aradhya(bob_y=-6, leg_phase=3, eye_state="happy", mouth_state="smile", thruster_glow=True).save(SPRITES_DIR / "float_1.png")
draw_chibi_aradhya(bob_y=-2, leg_phase=3, eye_state="open", mouth_state="smile", thruster_glow=True).save(SPRITES_DIR / "float_2.png")

print(f"✅ Successfully rendered 16 sprite frames into {SPRITES_DIR}!")
