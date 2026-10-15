#!/usr/bin/env python3
"""Rebuild locally created art, keeping imported refindTTT files intact."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source"
ICONS = ROOT / "icons"
ICONS.mkdir(exist_ok=True)

im = Image.open(SRC / "original-clean-background-1672x941.png").convert("RGB")
im.resize((3840, 2160), Image.Resampling.LANCZOS).save(
    ROOT / "background.png", format="PNG", compress_level=7
)

custom = {
    "glossy_neon_terminal_icon.png": "os_shell.png",
    "neon_frosted_six_tooth_gear.png": "os_rescue.png",
}
for original, filename in custom.items():
    im = Image.open(SRC / ("original-" + original)).convert("RGBA")
    im.putalpha(im.getchannel("A").point(lambda v: 0 if v <= 2 else v))
    im.resize((256, 256), Image.Resampling.LANCZOS).save(
        ICONS / filename, format="PNG", optimize=True
    )
print("Rebuilt background and custom Shell/Rescue icons; refindTTT assets preserved")
