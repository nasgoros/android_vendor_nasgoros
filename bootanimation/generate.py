#!/usr/bin/env python3
#
# Copyright (C) 2026 The nasgorOS Project
#
# SPDX-License-Identifier: Apache-2.0
#
# Generates bootanimation.zip for NasgorOS.
# Requires Pillow. Usage: generate.py <font.ttf> <output.zip>
# The font used for releases is Rubik Bold (OFL) from external/google-fonts/rubik.

import io
import math
import sys
import zipfile

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 600, 30

CHILI = (229, 72, 43)       # logo + "OS"
CREAM = (255, 247, 237)     # "Nasgor" + logo letter
EGG = (245, 179, 1)         # loading dots
BG = (0, 0, 0)

LOGO = 150                  # logo square size
GAP = 40                    # space between logo and text
TEXT_SIZE = 118

INTRO_FRAMES = 40           # part0: logo pops in, text slides in
LOOP_FRAMES = 60            # part1: loading dots, loops until boot completes
OUTRO_FRAMES = 15           # part2: fade out


def ease_out(t):
    return 1 - (1 - t) ** 3


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def blend(color, alpha):
    return tuple(int(c * alpha) for c in color)


class Renderer:
    def __init__(self, font_path):
        self.font = ImageFont.truetype(font_path, TEXT_SIZE)
        self.logo_font = ImageFont.truetype(font_path, int(LOGO * 0.72))
        draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        self.w_nasgor = draw.textlength("Nasgor", font=self.font)
        self.w_os = draw.textlength("OS", font=self.font)
        group = LOGO + GAP + self.w_nasgor + self.w_os
        self.x0 = (WIDTH - group) / 2
        self.cy = HEIGHT / 2 - 30

    def frame(self, logo_scale=1.0, logo_alpha=1.0, text_alpha=1.0,
              text_offset=0.0, dots=None, fade=1.0):
        img = Image.new("RGB", (WIDTH, HEIGHT), BG)
        d = ImageDraw.Draw(img)

        # Logo: rounded square with a lowercase "n"
        size = LOGO * logo_scale
        cx = self.x0 + LOGO / 2
        box = (cx - size / 2, self.cy - size / 2, cx + size / 2, self.cy + size / 2)
        if size > 2:
            d.rounded_rectangle(box, radius=size * 0.26,
                                fill=blend(CHILI, logo_alpha * fade))
            letter = ImageFont.truetype(self.logo_font.path, max(1, int(size * 0.72)))
            d.text((cx, self.cy + size * 0.02), "n", font=letter, anchor="mm",
                   fill=blend(CREAM, logo_alpha * fade))

        # Wordmark: "Nasgor" + "OS"
        a = text_alpha * fade
        if a > 0:
            tx = self.x0 + LOGO + GAP + text_offset
            d.text((tx, self.cy), "Nasgor", font=self.font, anchor="lm", fill=blend(CREAM, a))
            d.text((tx + self.w_nasgor, self.cy), "OS", font=self.font, anchor="lm",
                   fill=blend(CHILI, a))

        # Loading dots under the wordmark
        if dots is not None:
            for i, level in enumerate(dots):
                r = 9 + 4 * level
                x = WIDTH / 2 + (i - 1) * 46
                y = self.cy + LOGO / 2 + 95
                d.ellipse((x - r, y - r, x + r, y + r),
                          fill=blend(EGG, (0.35 + 0.65 * level) * fade))
        return img


def png_bytes(img):
    buf = io.BytesIO()
    img.quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(buf, "PNG", optimize=True)
    return buf.getvalue()


def dot_levels(t):
    # Three dots pulse one after another; t in [0, 1)
    return [0.5 + 0.5 * math.sin(2 * math.pi * (t - i / 3)) for i in range(3)]


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: generate.py <font.ttf> <output.zip>")
    r = Renderer(sys.argv[1])
    parts = {"part0": [], "part1": [], "part2": []}

    for i in range(INTRO_FRAMES):
        t = i / (INTRO_FRAMES - 1)
        logo_t = ease_out(clamp(t / 0.45))
        text_t = ease_out(clamp((t - 0.35) / 0.65))
        parts["part0"].append(r.frame(
            logo_scale=0.55 + 0.45 * logo_t, logo_alpha=logo_t,
            text_alpha=text_t, text_offset=40 * (1 - text_t)))

    for i in range(LOOP_FRAMES):
        parts["part1"].append(r.frame(dots=dot_levels(i / LOOP_FRAMES)))

    for i in range(OUTRO_FRAMES):
        fade = 1 - ease_out((i + 1) / OUTRO_FRAMES)
        parts["part2"].append(r.frame(dots=dot_levels(0), fade=fade))

    desc = (f"{WIDTH} {HEIGHT} {FPS}\n"
            "c 1 0 part0\n"
            "c 0 0 part1\n"
            "c 1 0 part2\n")

    # bootanimation.zip must be stored without compression
    with zipfile.ZipFile(sys.argv[2], "w", zipfile.ZIP_STORED) as z:
        z.writestr("desc.txt", desc)
        for name, frames in parts.items():
            for n, img in enumerate(frames):
                z.writestr(f"{name}/{n:03d}.png", png_bytes(img))


if __name__ == "__main__":
    main()
