#!/usr/bin/env python3
# Copyright (C) 2026 The nasgorOS Project
# SPDX-License-Identifier: Apache-2.0
"""Generate the Android boot ZIP and optional previews from the editable SVG.

Usage: generate.py <font.ttf> <output.zip> [--preview-dir DIRECTORY]
Dependencies: see requirements.txt. Release font: AOSP's Rubik-Medium.ttf (OFL).
"""

import argparse
import io
import math
from pathlib import Path
import zipfile

import cairosvg
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1080, 30
INTRO_FRAMES, LOOP_FRAMES, FADE_FRAMES = 36, 72, 12
SCALE = 2  # Supersampling keeps text, curves, and the tiny loader crisp.
BG = (0, 0, 0)
CREAM = (255, 245, 225)
ORANGE = (244, 151, 72)
# A fixed crop avoids allocating 1080x1080 GPU textures for every frame.
TRIM = (290, 200, 790, 820)
SOURCE = Path(__file__).resolve().parent


def clamp(value):
    return max(0.0, min(1.0, value))


def smooth(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def ease_out(value):
    return 1 - (1 - clamp(value)) ** 3


def blend(color, alpha):
    return tuple(round(c * clamp(alpha)) for c in color)


class Renderer:
    def __init__(self, font_path):
        self.font = ImageFont.truetype(str(font_path), 76 * SCALE)
        self.logo = Image.open(io.BytesIO(cairosvg.svg2png(
            url=str(SOURCE / "logo.svg"), output_width=400 * SCALE,
            output_height=320 * SCALE))).convert("RGBA")
        self.black = Image.new("RGB", (WIDTH, HEIGHT), BG)

    def point(self, x, y):
        return ((x - TRIM[0]) * SCALE, (y - TRIM[1]) * SCALE)

    def box(self, left, top, right, bottom):
        return (*self.point(left, top), *self.point(right, bottom))

    def frame(self, phase=0.0, reveal=1.0):
        canvas = Image.new("RGBA", ((TRIM[2] - TRIM[0]) * SCALE,
                                     (TRIM[3] - TRIM[1]) * SCALE), (*BG, 255))
        draw = ImageDraw.Draw(canvas)
        logo_t = ease_out(reveal / 0.62)
        text_t = smooth((reveal - 0.24) / 0.52)
        loading_t = smooth((reveal - 0.58) / 0.42)
        bob = 2.5 * math.sin(phase * math.tau) * loading_t

        # Intro: gently settle the plate upward into place.
        size = 0.88 + 0.12 * logo_t
        logo = self.logo.resize((round(400 * SCALE * size),
                                 round(320 * SCALE * size)), Image.Resampling.LANCZOS)
        if logo_t < 1:
            logo.putalpha(logo.getchannel("A").point(lambda a: round(a * logo_t)))
        position = self.point(540 - 200 * size,
                              272 + 160 * (1 - size) + 22 * (1 - logo_t) + bob)
        canvas.alpha_composite(logo, tuple(round(v) for v in position))

        # Three wisps rise independently. Opacity is zero at the wrap point.
        for index, x in enumerate((502, 540, 578)):
            life = (phase + index / 3) % 1.0
            alpha = math.sin(math.pi * life) ** 1.8 * 0.43 * loading_t
            points = []
            for step in range(41):
                t = step / 40
                points.append(self.point(
                    x + 6 * math.sin(t * math.tau - life * math.pi),
                    333 - 47 * life - 45 * t + bob))
            draw.line(points, fill=(*blend(CREAM, alpha), 255),
                      width=3 * SCALE, joint="curve")

        # Exact requested wordmark: lowercase, with a real space before os.
        label = "nasgor os"
        x = 540 - draw.textlength(label, font=self.font) / SCALE / 2
        y = 635 + 18 * (1 - text_t)
        draw.text(self.point(x, y), "nasgor ", font=self.font, anchor="lt",
                  fill=(*blend(CREAM, text_t), 255))
        prefix = draw.textlength("nasgor ", font=self.font) / SCALE
        draw.text(self.point(x + prefix, y), "os", font=self.font, anchor="lt",
                  fill=(*blend(ORANGE, text_t), 255))

        # Indeterminate capsule: all terms are periodic, with no reset flash.
        track = self.box(440, 773, 640, 779)
        draw.rounded_rectangle(track, radius=3 * SCALE,
                               fill=(*blend((48, 39, 30), loading_t), 255))
        wave = math.sin(math.tau * phase)
        length = 42 + 26 * (1 - wave * wave)
        center = 540 - (100 - length / 2) * math.cos(math.tau * phase)
        left, right = center - length / 2, center + length / 2
        mask = Image.new("L", canvas.size)
        ImageDraw.Draw(mask).rounded_rectangle(self.box(left, 773, right, 779),
                                               radius=3 * SCALE, fill=255)
        gradient = Image.new("RGBA", canvas.size)
        gd = ImageDraw.Draw(gradient)
        x0, y0, x1, y1 = map(round, self.box(left, 773, right, 779))
        for xx in range(x0, x1 + 1):
            t = (xx - x0) / max(1, x1 - x0)
            color = (round(239 + 16 * t), round(119 + 79 * t), round(59 + 43 * t))
            gd.line((xx, y0, xx, y1), fill=(*blend(color, loading_t), 255))
        canvas.paste(gradient, (0, 0), mask)

        cropped = canvas.convert("RGB").resize(
            (TRIM[2] - TRIM[0], TRIM[3] - TRIM[1]), Image.Resampling.LANCZOS)
        frame = self.black.copy()
        frame.paste(cropped, TRIM[:2])
        return frame


def png_bytes(image):
    output = io.BytesIO()
    # Truecolor avoids per-frame palette shifts in the steam and gradients.
    image.save(output, "PNG", optimize=True)
    return output.getvalue()


def store_file(archive, name, data):
    # Stable metadata makes rebuilding with the same inputs reproducible.
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def write_archive(renderer, output):
    description = (f"{WIDTH} {HEIGHT} {FPS}\n"
                   "c 1 0 part0 #000000\n"
                   f"f 0 0 part1 {FADE_FRAMES} #000000\n")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        store_file(archive, "desc.txt", description)
        for name, count in (("part0", INTRO_FRAMES), ("part1", LOOP_FRAMES)):
            for i in range(count):
                frame = (renderer.frame(reveal=i / (count - 1)) if name == "part0"
                         else renderer.frame(phase=i / count))
                store_file(archive, f"{name}/{i:03d}.png", png_bytes(frame.crop(TRIM)))
            trim = f"{TRIM[2] - TRIM[0]}x{TRIM[3] - TRIM[1]}+{TRIM[0]}+{TRIM[1]}\n"
            store_file(archive, f"{name}/trim.txt", trim * count)
            print(f"{name}: {count} frames", flush=True)


def read_preview_frames(archive_path):
    """Reconstruct the shipped PNGs so previews show the actual ZIP artwork."""
    parts = {}
    with zipfile.ZipFile(archive_path) as archive:
        for part in ("part0", "part1"):
            parts[part] = []
            for name in sorted(archive.namelist()):
                if name.startswith(part + "/") and name.endswith(".png"):
                    canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
                    with Image.open(io.BytesIO(archive.read(name))) as cropped:
                        canvas.paste(cropped, TRIM[:2])
                    parts[part].append(canvas)
    return parts


def write_previews(archive_path, directory):
    directory.mkdir(parents=True, exist_ok=True)
    parts = read_preview_frames(archive_path)
    poster = parts["part1"][LOOP_FRAMES // 8]
    poster.save(directory / "preview.png")
    phone = Image.new("RGB", (1080, 2340), BG)
    phone.paste(poster, (0, (2340 - HEIGHT) // 2))
    phone.resize((540, 1170), Image.Resampling.LANCZOS).save(directory / "preview-phone.png")

    # 15 fps with alternating GIF delays to match the 30 fps ZIP duration.
    sequence = parts["part0"][::2] + parts["part1"][::2] * 2
    black = Image.new("RGB", (WIDTH, HEIGHT), BG)
    for i in range(0, FADE_FRAMES, 2):
        sequence.append(Image.blend(parts["part1"][i], black, (i + 1) / FADE_FRAMES))
    sequence.append(black)
    # One shared palette prevents GIF flicker on a stationary logo.
    palette = poster.resize((540, 540)).quantize(colors=255)
    frames = [frame.resize((540, 540), Image.Resampling.LANCZOS).quantize(
        palette=palette, dither=Image.Dither.NONE) for frame in sequence]
    durations = [60 if i % 3 == 0 else 70 for i in range(len(frames))]
    durations[-1] = 700
    frames[0].save(directory / "preview.gif", save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=False, disposal=2)
    (directory / "preview.html").write_text('''<!doctype html>
<html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>nasgor os · Boot animation</title>
<style>
  *{box-sizing:border-box}body{margin:0;min-height:100svh;background:#11110f;color:#fff5e1;
  font:15px system-ui,sans-serif;display:grid;place-items:center;padding:32px 20px}
  main{text-align:center}h1{font-size:20px;font-weight:500;letter-spacing:-.5px;margin:0 0 10px}
  p{color:#a4a098;font-size:13px;margin:0 0 24px}a{color:#f49748;text-underline-offset:4px}
  .screen{width:min(340px,78vw);aspect-ratio:1080/2340;background:#000;border-radius:32px;
  overflow:hidden;display:grid;place-items:center;box-shadow:0 0 0 1px #33332d,0 24px 80px #0006}
  img{display:block;width:100%}footer{margin-top:24px;color:#a4a098;font-size:12px;line-height:1.8}
  @media(prefers-reduced-motion:reduce){.motion{display:none}}
  @media(prefers-reduced-motion:no-preference){.still{display:none}}
</style>
<main><h1>nasgor os</h1><p>Sepiring semangat untuk awal yang baru.</p>
<div class="screen"><img class="motion" src="preview.gif" alt="Logo nasi goreng, uap bergerak, dan loading oranye">
<img class="still" src="preview.png" alt="Logo nasi goreng dan tulisan nasgor os"></div>
<footer>Pratinjau boot animation · <a href="../bootanimation.zip" download>Unduh ZIP</a><br>
Di perangkat, loading berulang sampai boot selesai.</footer></main></html>
''', encoding="utf-8")
    print(f"Previews: {directory}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("font", type=Path, help="Rubik-Medium.ttf from external/google-fonts/rubik")
    parser.add_argument("output", type=Path, help="destination bootanimation.zip")
    parser.add_argument("--preview-dir", type=Path, help="also write GIF, PNG, and HTML previews")
    args = parser.parse_args()
    if not args.font.is_file():
        parser.error(f"font does not exist: {args.font}")
    write_archive(Renderer(args.font), args.output)
    print(f"ZIP: {args.output} ({args.output.stat().st_size / 1024 / 1024:.2f} MiB)")
    if args.preview_dir:
        write_previews(args.output, args.preview_dir)


if __name__ == "__main__":
    main()
