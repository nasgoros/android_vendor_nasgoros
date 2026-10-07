#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
"""Export the boot-animation plate as the ROM's PNG logo and About resource.

Uses CairoSVG from bootanimation/requirements.txt. No Android compilation.
"""
import argparse
from pathlib import Path
import xml.etree.ElementTree as ET

import cairosvg


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "bootanimation" / "logo.svg"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)


def render(viewbox, width, height, background=None):
    """Render directly from the editable SVG, without altering a raster logo."""
    root = ET.parse(SOURCE).getroot()
    root.set("viewBox", viewbox)
    root.set("width", str(width))
    root.set("height", str(height))
    return cairosvg.svg2png(
        bytestring=ET.tostring(root),
        output_width=width,
        output_height=height,
        background_color=background,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-copy", type=Path,
                        help="also save the square transparent master at this path")
    parser.add_argument("--avatar-copy", type=Path,
                        help="also save the dark square avatar at this path")
    parser.add_argument("--settings-res", type=Path,
                        help="Settings res/ directory for the compact About PNG")
    args = parser.parse_args()

    master = render("0 0 400 400", 1024, 1024)
    (HERE / "proyek.png").write_bytes(master)
    (HERE / "nasgor-os-logo-transparent.png").write_bytes(master)
    avatar = render("0 0 400 400", 1024, 1024, "#111821")
    (HERE / "nasgor-os-avatar-dark.png").write_bytes(avatar)
    # Crop only transparent space for the 128dp x 80dp About ImageView.
    about = render("0 68 400 250", 512, 320)
    (HERE / "nasgor-about-mark.png").write_bytes(about)
    if args.project_copy:
        args.project_copy.parent.mkdir(parents=True, exist_ok=True)
        args.project_copy.write_bytes(master)
    if args.avatar_copy:
        args.avatar_copy.parent.mkdir(parents=True, exist_ok=True)
        args.avatar_copy.write_bytes(avatar)
    if args.settings_res:
        output = args.settings_res / "drawable-nodpi" / "nasgor_about_mark.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(about)
    print("Exported plate logo: transparent/avatar 1024x1024, About 512x320")


if __name__ == "__main__":
    main()
