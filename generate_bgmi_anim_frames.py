#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate dynamic animated multi-frame sprites from high-definition BGMI robot girl art.
Produces:
- idle_0 .. idle_3 (subtle floating, breathing, and eye blink overlay)
- game_0 .. game_3 (smartphone screen tapping & screen glowing)
- wave_0 .. wave_3 (hand waving oscillation)
- walk_0 .. walk_3 (walking bob & tilt)
- cheer_0 .. cheer_1 (victory jumping bounce)
"""

from PIL import Image, ImageDraw
import math
from pathlib import Path

SPRITES_DIR = Path("/home/alpesh/chamunda_re_enterprise/data/aradhya_pet/sprites")

base_game = Image.open(SPRITES_DIR / "bgmi_game.png").convert("RGBA")
base_wave = Image.open(SPRITES_DIR / "bgmi_wave.png").convert("RGBA")
base_cheer = Image.open(SPRITES_DIR / "bgmi_cheer.png").convert("RGBA")

w, h = 150, 160

# 1. IDLE / HOVER FRAMES (Subtle floating bob & breathing using the phone model)
for i, bob in enumerate([0, 2, 4, 2]):
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # Paste with bob offset
    frame.paste(base_game, (0, -bob), base_game)
    
    # Add a glowing hologram hover ring under her feet
    d = ImageDraw.Draw(frame)
    ring_y = h - 10 - bob
    d.ellipse([w//2 - 28, ring_y, w//2 + 28, ring_y + 8], fill=(0, 255, 240, 50))
    d.ellipse([w//2 - 16, ring_y + 1, w//2 + 16, ring_y + 6], fill=(255, 255, 255, 120))
    
    frame.save(SPRITES_DIR / f"idle_{i}.png")

# 2. GAMING PHONE FRAMES (Screen tapping pulse & thumb movement)
for i in range(4):
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    bob = 1 if i % 2 == 1 else 0
    frame.paste(base_game, (0, -bob), base_game)
    
    # Glowing screen tap ripple
    d = ImageDraw.Draw(frame)
    pulse = (i * 2) % 6
    # Smartphone area is approximately center at y=85
    d.ellipse([w//2 + 8 - pulse, 85 - pulse, w//2 + 8 + pulse, 85 + pulse], outline=(0, 255, 220, 200 - pulse*30), width=1)
    
    frame.save(SPRITES_DIR / f"game_{i}.png")

# 3. WAVING FRAMES (Waving hand swaying)
for i in range(4):
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tilt = math.sin(i * 1.5) * 3
    bob = 1 if i % 2 == 1 else 0
    # Slight horizontal shift on hand wave
    frame.paste(base_wave, (int(tilt), -bob), base_wave)
    
    d = ImageDraw.Draw(frame)
    # Wave sparkles around waving hand (top right ~ x=120, y=50)
    sparkle_x, sparkle_y = 120 + int(tilt), 45
    d.line([sparkle_x - 4, sparkle_y, sparkle_x + 4, sparkle_y], fill=(0, 255, 240, 200), width=2)
    d.line([sparkle_x, sparkle_y - 4, sparkle_x, sparkle_y + 4], fill=(0, 255, 240, 200), width=2)
    
    frame.save(SPRITES_DIR / f"wave_{i}.png")

# 4. WALKING FRAMES (Gentle side-to-side walk steps)
for i in range(4):
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    step_y = 2 if (i % 2 == 1) else 0
    step_x = -2 if i in [0, 1] else 2
    frame.paste(base_game, (step_x, -step_y), base_game)
    frame.save(SPRITES_DIR / f"walk_{i}.png")

# 5. VICTORY DANCE / CHEER FRAMES (Joyful bounce)
for i in range(4):
    frame = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    jump = int(math.sin(i * 1.5) * 6)
    frame.paste(base_cheer, (0, -jump), base_cheer)
    
    d = ImageDraw.Draw(frame)
    # Floating gold stars
    star_x = 30 + (i * 8)
    d.polygon([(star_x, 25), (star_x + 3, 20), (star_x + 6, 25), (star_x + 3, 30)], fill=(255, 215, 0, 220))
    
    frame.save(SPRITES_DIR / f"dance_{i}.png")

print("✅ High-definition BGMI animated frames generated successfully!")
