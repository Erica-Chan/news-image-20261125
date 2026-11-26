#!/usr/bin/env python3
"""Compose the news-image-20261125 entry poster (1024x1024 PNG).

Front-page broadsheet for Wednesday 25 November 2026: 54 stories across
10 regions. One banner top story, five large lead cards and ten medium
cards — each with its own code-drawn flat illustration (16 drawn scenes
in total) and a certainty badge — plus a world map with 16 numbered pins,
a by-the-numbers panel, a UTC timeline, 38 more one-line stories with
certainty dots, and a date-check box naming stories left out because they
happened on earlier days. Every story is dated 25 November 2026 (UTC)
and sourced; data lives in stories.json. All drawing is PIL:
deterministic, no network, no AI images. Run:
    python3 compose_poster.py   # writes entry.png next to this file
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
CREAM = (247, 243, 227)
PAPER = (252, 249, 238)
NAVY = (20, 38, 77)
NAVY2 = (12, 22, 48)
RED = (178, 44, 32)
GOLD = (232, 184, 74)
INK = (24, 28, 36)
GREY = (82, 88, 98)
CARD = (255, 255, 255)
LINE = (205, 198, 178)
SKY = (214, 230, 240)
SEA = (16, 42, 74)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size))


BADGE = {
    "CONFIRMED": (30, 125, 50),
    "OFFICIAL": (23, 90, 160),
    "REPORTED": (178, 106, 0),
    "CLAIM": (178, 60, 23),
    "PENDING": (91, 107, 124),
    "FORECAST": (106, 76, 160),
}


def wrap(draw, text, fnt, width, max_lines=None):
    """Greedy word wrap; optionally cap lines (last line gets an ellipsis)."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " …", font=fnt) > width:
            lines[-1] = lines[-1][:-1].rstrip()
        lines[-1] += " …"
    return lines


def badge(d, x, y, label, fnt):
    """Certainty badge; returns its width."""
    w = int(d.textlength(label, font=fnt)) + 12
    h = fnt.size + 8
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=BADGE[label])
    d.text((x + 6, y + 4), label, font=fnt, fill=(255, 255, 255))
    return w


def kicker(d, x, y, text, color=RED):
    d.text((x, y), text, font=font(SANS_B, 9), fill=color)
    return int(d.textlength(text, font=font(SANS_B, 9)))


# ---------------------------------------------------------------------------
# Flat vector illustrations. Each draws inside the box (x, y, w, h).
# ---------------------------------------------------------------------------

def ill_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 236, 244))
    cx, cy, r = x + w * 0.24, y + h * 0.52, h * 0.36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
              outline=NAVY, width=2)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=(255, 255, 255), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=2)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360,
          fill=(255, 255, 255), width=2)
    bars = [(0.50, 0.30, "15%"), (0.64, 0.48, "25%"), (0.78, 0.68, "35%")]
    for bx, bh, lab in bars:
        d.rectangle([x + w * bx, y + h * (0.92 - bh), x + w * (bx + 0.10),
                     y + h * 0.92], fill=RED)
        if w > 150:
            d.text((x + w * bx, y + h * (0.88 - bh)), lab,
                   font=font(SANS_B, 11), fill=RED)
    d.text((x + w * 0.52, y + h * 0.06), "SECTION 301",
           font=font(SANS_B, 12 if w > 150 else 9), fill=NAVY)


def ill_kospi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 245, 233))
    d.rectangle([x, y + h * 0.74, x + w, y + h], fill=(27, 94, 32))
    pts = [(0.06, 0.22), (0.22, 0.30), (0.38, 0.26), (0.54, 0.44),
           (0.70, 0.52), (0.86, 0.66), (0.97, 0.60)]
    for i in range(len(pts) - 1):
        d.line([x + w * pts[i][0], y + h * pts[i][1],
                x + w * pts[i + 1][0], y + h * pts[i + 1][1]],
               fill=RED, width=4)
    for px, py in pts:
        d.ellipse([x + w * px - 3, y + h * py - 3, x + w * px + 3,
                   y + h * py + 3], fill=(255, 255, 255),
                  outline=RED, width=2)
    s = h * 0.22
    cx, cy = x + w * 0.82, y + h * 0.22
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=NAVY,
                outline=GOLD, width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=GOLD)


def ill_shenzhou(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 46))
    for sx, sy in [(0.12, 0.18), (0.30, 0.10), (0.55, 0.22), (0.80, 0.12),
                   (0.92, 0.30), (0.45, 0.08), (0.68, 0.32)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 2, y + h * sy + 2],
                  fill=(255, 255, 255))
    # station: central module + panels
    d.rectangle([x + w * 0.52, y + h * 0.42, x + w * 0.94, y + h * 0.58],
                fill=(200, 205, 215), outline=NAVY, width=1)
    d.rectangle([x + w * 0.52, y + h * 0.30, x + w * 0.64, y + h * 0.70],
                fill=(40, 90, 160))
    d.rectangle([x + w * 0.82, y + h * 0.30, x + w * 0.94, y + h * 0.70],
                fill=(40, 90, 160))
    # rocket rising on the left
    rx = x + w * 0.22
    d.polygon([(rx, y + h * 0.12), (rx - h * 0.10, y + h * 0.34),
               (rx + h * 0.10, y + h * 0.34)], fill=(255, 255, 255))
    d.rectangle([rx - h * 0.10, y + h * 0.34, rx + h * 0.10, y + h * 0.62],
                fill=(255, 255, 255))
    d.rectangle([rx - h * 0.10, y + h * 0.34, rx + h * 0.10, y + h * 0.40],
                fill=RED)
    d.polygon([(rx - h * 0.05, y + h * 0.62), (rx + h * 0.05, y + h * 0.62),
               (rx + h * 0.14, y + h * 0.82), (rx, y + h * 0.74),
               (rx - h * 0.14, y + h * 0.82)], fill=(255, 150, 40))


def ill_cairo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 160))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(90, 82, 96))
    d.line([x, y + h * 0.83, x + w, y + h * 0.83], fill=(255, 255, 255),
           width=2)
    # tanker truck
    tx, ty = x + w * 0.30, y + h * 0.52
    d.rectangle([tx, ty, tx + w * 0.42, ty + h * 0.14], fill=(210, 210, 210),
                outline=NAVY, width=1)
    d.rectangle([tx + w * 0.42, ty - h * 0.04, tx + w * 0.54,
                 ty + h * 0.14], fill=RED)
    d.ellipse([tx + w * 0.08, ty + h * 0.14, tx + w * 0.16, ty + h * 0.22],
              fill=INK)
    d.ellipse([tx + w * 0.36, ty + h * 0.14, tx + w * 0.44, ty + h * 0.22],
              fill=INK)
    # flame
    fx, fy = tx + w * 0.21, ty - h * 0.02
    d.polygon([(fx, fy - h * 0.34), (fx - w * 0.07, fy),
               (fx + w * 0.07, fy)], fill=(255, 120, 20))
    d.polygon([(fx, fy - h * 0.20), (fx - w * 0.035, fy),
               (fx + w * 0.035, fy)], fill=(255, 220, 60))
    # smoke
    for i, (sx, sy, sr) in enumerate([(0.62, 0.30, 0.05), (0.68, 0.20, 0.07),
                                      (0.76, 0.12, 0.09)]):
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)], fill=(120, 120, 120))


def ill_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 225))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(30, 90, 140))
    for i in range(5):
        d.arc([x + w * (0.05 + i * 0.2), y + h * 0.66,
               x + w * (0.20 + i * 0.2), y + h * 0.80], 0, 180,
              fill=(255, 255, 255), width=2)
    # tanker
    tx, ty = x + w * 0.22, y + h * 0.44
    d.rectangle([tx, ty, tx + w * 0.44, ty + h * 0.18], fill=(120, 30, 30))
    d.rectangle([tx + w * 0.34, ty - h * 0.12, tx + w * 0.42, ty],
                fill=(200, 200, 200))
    # naval mine, spiked
    mx, my, mr = x + w * 0.78, y + h * 0.52, h * 0.09
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        d.line([mx, my, mx + (mr + 5) * math.cos(a),
                my + (mr + 5) * math.sin(a)], fill=INK, width=2)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    # explosion burst
    bx, by = x + w * 0.55, y + h * 0.30
    for dx, dy, rr in [(0, 0, 0.10), (-0.08, 0.04, 0.06), (0.08, -0.03, 0.07),
                       (0.02, 0.07, 0.05)]:
        ex, ey = bx + w * dx, by + h * dy
        d.ellipse([ex - h * rr, ey - h * rr, ex + h * rr, ey + h * rr],
                  fill=(255, 140, 20))


def ill_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.rectangle([x, y + h * 0.78, x + w, y + h], fill=(150, 140, 120))
    # pediment + columns
    px, py = x + w * 0.14, y + h * 0.16
    d.polygon([(px, py + h * 0.22), (px + w * 0.72, py + h * 0.22),
               (px + w * 0.36, py)], fill=(120, 110, 95))
    for i in range(4):
        cx = px + w * (0.08 + i * 0.17)
        d.rectangle([cx, py + h * 0.24, cx + w * 0.07, y + h * 0.78],
                    fill=(250, 248, 240), outline=(120, 110, 95), width=1)
    d.rectangle([px - w * 0.02, y + h * 0.76, px + w * 0.76, y + h * 0.80],
                fill=(120, 110, 95))
    # scales of justice
    sx, sy = x + w * 0.86, y + h * 0.34
    d.line([sx, sy - h * 0.18, sx, sy + h * 0.30], fill=GOLD, width=3)
    d.line([sx - w * 0.07, sy - h * 0.14, sx + w * 0.07, sy - h * 0.14],
           fill=GOLD, width=3)
    for sgn in (-1, 1):
        ex = sx + sgn * w * 0.07
        d.line([ex, sy - h * 0.14, ex, sy - h * 0.04], fill=GOLD, width=2)
        d.polygon([(ex - w * 0.035, sy - h * 0.02), (ex + w * 0.035, sy - h * 0.02),
                   (ex, sy + h * 0.06)], fill=GOLD)


def ill_wage(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 236, 248))
    # factory
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.62, y + h * 0.86],
                fill=(90, 110, 140))
    d.rectangle([x + w * 0.52, y + h * 0.20, x + w * 0.60, y + h * 0.86],
                fill=(70, 90, 120))
    for i in range(3):
        d.rectangle([x + w * (0.14 + i * 0.15), y + h * 0.54,
                     x + w * (0.22 + i * 0.15), y + h * 0.66],
                    fill=(255, 240, 150))
    # rising arrow with 36%
    pts = [(0.66, 0.72), (0.74, 0.58), (0.80, 0.62), (0.92, 0.38)]
    for i in range(len(pts) - 1):
        d.line([x + w * pts[i][0], y + h * pts[i][1],
                x + w * pts[i + 1][0], y + h * pts[i + 1][1]],
               fill=(30, 125, 50), width=4)
    d.polygon([(x + w * 0.92, y + h * 0.38), (x + w * 0.86, y + h * 0.38),
               (x + w * 0.92, y + h * 0.30)], fill=(30, 125, 50))
    if w > 120:
        d.text((x + w * 0.64, y + h * 0.10), "+36%",
               font=font(SANS_B, 13), fill=(30, 125, 50))


def ill_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 38, 77))
    cx, cy, s = x + w * 0.5, y + h * 0.5, h * 0.30
    d.rectangle([cx - s, cy - s, cx + s, cy + s], fill=(40, 60, 110),
                outline=GOLD, width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=GOLD)
    for k in (-1, 0, 1):
        d.line([cx + k * s * 0.55, cy - s - 5, cx + k * s * 0.55, cy - s],
               fill=GOLD, width=2)
        d.line([cx + k * s * 0.55, cy + s, cx + k * s * 0.55, cy + s + 5],
               fill=GOLD, width=2)
        d.line([cx - s - 5, cy + k * s * 0.55, cx - s, cy + k * s * 0.55],
               fill=GOLD, width=2)
        d.line([cx + s, cy + k * s * 0.55, cx + s + 5, cy + k * s * 0.55],
               fill=GOLD, width=2)


def ill_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 139, 67))
    d.line([x, y + h * 0.5, x + w, y + h * 0.5], fill=(255, 255, 255),
           width=2)
    d.ellipse([x + w * 0.42, y + h * 0.28, x + w * 0.58, y + h * 0.72],
              outline=(255, 255, 255), width=2)
    cx, cy, r = x + w * 0.72, y + h * 0.42, h * 0.26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
              outline=INK, width=1)
    d.polygon([(cx, cy - r * 0.4), (cx + r * 0.38, cy - r * 0.12),
               (cx + r * 0.24, cy + r * 0.32), (cx - r * 0.24, cy + r * 0.32),
               (cx - r * 0.38, cy - r * 0.12)], fill=INK)
    # goal posts
    d.rectangle([x + w * 0.06, y + h * 0.14, x + w * 0.24, y + h * 0.30],
                outline=(255, 255, 255), width=2)


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 210))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(140, 130, 110))
    for bx, bw, bh in [(0.06, 0.18, 0.34), (0.28, 0.15, 0.46),
                       (0.47, 0.20, 0.30), (0.70, 0.16, 0.40)]:
        d.rectangle([x + w * bx, y + h * (0.72 - bh), x + w * (bx + bw),
                     y + h * 0.72], fill=(100, 92, 84))
        for wy in (0.72 - bh + 0.08, 0.72 - bh + 0.20):
            d.rectangle([x + w * (bx + 0.03), y + h * wy,
                         x + w * (bx + 0.08), y + h * (wy + 0.06)],
                        fill=(255, 240, 150))
    for sx, sy, sr in [(0.55, 0.30, 0.06), (0.62, 0.20, 0.08),
                       (0.70, 0.12, 0.09)]:
        d.ellipse([x + w * (sx - sr), y + h * (sy - sr),
                   x + w * (sx + sr), y + h * (sy + sr)], fill=(110, 110, 110))


def ill_odesa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 50, 70))
    d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.60, y + h * 0.86],
                fill=(70, 80, 100))
    for r in range(3):
        for c in range(3):
            d.rectangle([x + w * (0.18 + c * 0.13), y + h * (0.38 + r * 0.16),
                         x + w * (0.24 + c * 0.13), y + h * (0.44 + r * 0.16)],
                        fill=(255, 220, 100))
    fx, fy = x + w * 0.78, y + h * 0.72
    d.polygon([(fx, fy - h * 0.42), (fx - w * 0.09, fy),
               (fx + w * 0.09, fy)], fill=(255, 120, 20))
    d.polygon([(fx, fy - h * 0.26), (fx - w * 0.045, fy),
               (fx + w * 0.045, fy)], fill=(255, 220, 60))


def ill_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    cx, cy = x + w * 0.5, y + h * 0.55
    d.ellipse([cx - w * 0.10, cy - h * 0.14, cx + w * 0.10, cy + h * 0.14],
              fill=(60, 70, 85))
    d.ellipse([cx - w * 0.03, cy - h * 0.05, cx + w * 0.03, cy + h * 0.05],
              fill=RED)
    for sx, sy in [(-0.32, -0.28), (0.32, -0.28), (-0.32, 0.28), (0.32, 0.28)]:
        rx, ry = cx + w * sx, cy + h * sy
        d.line([cx, cy, rx, ry], fill=(60, 70, 85), width=2)
        d.ellipse([rx - w * 0.11, ry - 2, rx + w * 0.11, ry + 2],
                  fill=(120, 130, 145))
        d.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=(60, 70, 85))


def ill_pope(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
    d.rectangle([x + w * 0.18, y + h * 0.58, x + w * 0.82, y + h * 0.86],
                fill=(200, 185, 150))
    d.pieslice([x + w * 0.32, y + h * 0.16, x + w * 0.68, y + h * 0.62],
               180, 360, fill=(150, 120, 80))
    d.rectangle([x + w * 0.47, y + h * 0.08, x + w * 0.53, y + h * 0.20],
                fill=GOLD)
    d.rectangle([x + w * 0.43, y + h * 0.12, x + w * 0.57, y + h * 0.16],
                fill=GOLD)
    for i in range(3):
        d.rectangle([x + w * (0.26 + i * 0.24), y + h * 0.64,
                     x + w * (0.32 + i * 0.24), y + h * 0.86],
                    fill=(90, 75, 55))


def ill_island(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 190, 220))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(30, 120, 170))
    d.pieslice([x + w * 0.14, y + h * 0.52, x + w * 0.86, y + h * 0.90],
               180, 360, fill=(240, 220, 140))
    tx, ty = x + w * 0.52, y + h * 0.52
    d.line([tx, ty, tx, ty - h * 0.30], fill=(110, 80, 40), width=3)
    for dx, dy in [(-0.12, -0.34), (-0.05, -0.40), (0.06, -0.38),
                   (0.12, -0.32)]:
        d.line([tx, ty - h * 0.30, tx + w * dx, ty + h * dy],
               fill=(40, 140, 70), width=3)
    d.ellipse([tx - 3, ty - h * 0.28, tx + 3, ty - h * 0.22],
              fill=(120, 90, 40))
    d.ellipse([tx + 6, ty - h * 0.26, tx + 12, ty - h * 0.20],
              fill=(120, 90, 40))


def ill_gdp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 245, 233))
    bars = [(0.12, 0.24), (0.30, 0.34), (0.48, 0.30), (0.66, 0.52),
            (0.82, 0.66)]
    for bx, bh in bars:
        d.rectangle([x + w * bx, y + h * (0.88 - bh), x + w * (bx + 0.12),
                     y + h * 0.88], fill=(30, 125, 50))
    d.line([x + w * 0.10, y + h * 0.20, x + w * 0.90, y + h * 0.14],
           fill=(30, 125, 50), width=3)
    if w > 120:
        d.text((x + w * 0.60, y + h * 0.04), "4.3%",
               font=font(SANS_B, 13), fill=(30, 125, 50))


def ill_refinery(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 200, 130))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(90, 80, 70))
    for tx in (0.10, 0.34, 0.58):
        d.ellipse([x + w * tx, y + h * 0.48, x + w * (tx + 0.18),
                   y + h * 0.70], fill=(200, 200, 205), outline=NAVY, width=1)
    # flare stack
    fx = x + w * 0.86
    d.rectangle([fx - 2, y + h * 0.30, fx + 2, y + h * 0.70], fill=INK)
    d.polygon([(fx, y + h * 0.06), (fx - w * 0.05, y + h * 0.30),
               (fx + w * 0.05, y + h * 0.30)], fill=(255, 140, 20))
    d.polygon([(fx, y + h * 0.14), (fx - w * 0.025, y + h * 0.30),
               (fx + w * 0.025, y + h * 0.30)], fill=(255, 220, 60))


SCENES = {
    "tariffs": ill_tariffs, "kospi": ill_kospi, "shenzhou": ill_shenzhou,
    "cairo": ill_cairo, "hormuz": ill_hormuz, "court": ill_court,
    "wage": ill_wage, "chip": ill_chip, "football": ill_football,
    "gaza": ill_gaza, "odesa": ill_odesa, "drone": ill_drone,
    "pope": ill_pope, "island": ill_island, "gdp": ill_gdp,
    "refinery": ill_refinery,
}

# Coarse equirectangular continents (lon, lat) — recognisable, not exact.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 73), (-65, 60), (-55, 52), (-60, 46), (-70, 42), (-75, 35),
     (-80, 26), (-85, 20), (-90, 15), (-95, 16), (-100, 20), (-105, 23),
     (-110, 28), (-115, 32), (-120, 38), (-125, 45), (-130, 55),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 10), (-60, 5), (-50, 0), (-45, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-73, -40), (-72, -25), (-70, -18), (-78, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 20), (43, 12), (48, 10), (51, 12), (45, 0),
     (40, -10), (35, -20), (32, -28), (25, -33), (18, -35), (15, -25),
     (12, -15), (9, 0), (8, 4), (-8, 5), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (-5, 58), (5, 60), (10, 62),
     (18, 68), (25, 71), (35, 68), (45, 68), (55, 70), (65, 72), (75, 73),
     (90, 75), (110, 76), (130, 72), (150, 70), (170, 67), (178, 65),
     (170, 60), (160, 55), (155, 50), (142, 45), (140, 40), (135, 35),
     (130, 32), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (85, 20), (80, 10), (77, 8), (75, 15), (72, 20),
     (65, 25), (60, 25), (55, 26), (50, 28), (48, 30), (45, 28), (40, 30),
     (35, 36), (30, 36), (25, 38), (20, 40), (15, 44), (10, 44),
     (5, 43), (0, 40), (-5, 36), (-10, 37)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (150, -25), (146, -20), (142, -15), (140, -12),
     (136, -12), (132, -12), (128, -14), (124, -15), (120, -18),
     (116, -20)],
    [(-55, 60), (-45, 60), (-40, 65), (-30, 68), (-22, 70), (-25, 75),
     (-35, 78), (-50, 76), (-58, 70), (-60, 65)],
    [(43, -12), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22),
     (43, -16)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 52)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (141, 40), (138, 35), (134, 33)],
]

# Pin offsets (px) where two pinned stories share a city.
PIN_DX = {1: (-9, 6), 8: (9, -6), 10: (8, 2), 15: (9, -2), 4: (-7, -4)}


def main():
    data = json.load(open(os.path.join(HERE, "stories.json")))
    stories = sorted(data["stories"], key=lambda s: s["n"])
    leads = [s for s in stories if s["kind"] == "lead"]
    mediums = [s for s in stories if s["kind"] == "medium"]
    alsos = [s for s in stories if s["kind"] == "also"]

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=PAPER)
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=2)

    # --- masthead ---------------------------------------------------------
    title = "THE WORLD IN ONE DAY"
    tf = font(SERIF_B, 34)
    d.text(((W - d.textlength(title, font=tf)) / 2, 12), title,
           font=tf, fill=NAVY2)
    d.line([14, 52, W - 14, 52], fill=NAVY, width=2)
    d.text((14, 56), "WEDNESDAY, 25 NOVEMBER 2026",
           font=font(SANS_B, 11), fill=NAVY)
    right = "54 STORIES  ·  10 REGIONS  ·  16 DRAWN SCENES"
    d.text((W - 14 - d.textlength(right, font=font(SANS_B, 11)), 56),
           right, font=font(SANS_B, 11), fill=RED)

    # --- banner top story (lead 1) ----------------------------------------
    bx, by, bw, bh = 14, 74, 996, 112
    d.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    s = leads[0]
    scene_w = 300
    SCENES[s["scene"]](d, bx + bw - scene_w, by, scene_w, bh)
    d.rectangle([bx + bw - scene_w, by, bx + bw - scene_w + 2, by + bh],
                fill=GOLD)
    tx = bx + 12
    d.text((tx, by + 7), "TOP STORY — TRADE WAR",
           font=font(SANS_B, 10), fill=GOLD)
    badge(d, bx + bw - scene_w - 92, by + 6, s["certainty"],
          font(SANS_B, 8))
    hl = wrap(d, s["headline"], font(SERIF_B, 21), bw - scene_w - 24,
              max_lines=2)
    yy = by + 20
    for line in hl:
        d.text((tx, yy), line, font=font(SERIF_B, 21), fill=(255, 255, 255))
        yy += 24
    bl = wrap(d, s["body"], font(SANS, 11), bw - scene_w - 24, max_lines=2)
    for line in bl:
        d.text((tx, yy), line, font=font(SANS, 11), fill=(225, 230, 240))
        yy += 14
    d.text((tx, by + bh - 14), f"1 · {s['place']}  —  {s['source']}",
           font=font(SANS, 9), fill=(200, 205, 220))

    # --- lead cards -------------------------------------------------------
    def lead_card(s, cx, cy, cw, ch):
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD,
                    outline=LINE, width=1)
        sh = 48
        SCENES[s["scene"]](d, cx, cy, cw, sh)
        d.rectangle([cx, cy + sh, cx + cw, cy + sh + 2], fill=RED)
        d.text((cx + 8, cy + 52), f"{s['n']} · {s['place']}",
               font=font(SANS_B, 8), fill=RED)
        hl = wrap(d, s["headline"], font(SERIF_B, 12.5), cw - 16,
                  max_lines=2)
        yy = cy + 64
        for line in hl:
            d.text((cx + 8, yy), line, font=font(SERIF_B, 12.5), fill=INK)
            yy += 14
        bl = wrap(d, s["body"], font(SANS, 9), cw - 16, max_lines=2)
        yy = cy + 94
        for line in bl:
            d.text((cx + 8, yy), line, font=font(SANS, 9), fill=GREY)
            yy += 11
        d.text((cx + 8, cy + ch - 10), s["source"],
               font=font(SANS, 8), fill=GREY)
        badge(d, cx + cw - 62, cy + ch - 14, s["certainty"],
              font(SANS_B, 7))

    col_w, gap = 326, 9
    xs = [14, 14 + col_w + gap, 14 + 2 * (col_w + gap)]
    lead_card(leads[1], xs[0], 192, col_w, 130)
    lead_card(leads[2], xs[1], 192, col_w, 130)
    lead_card(leads[3], xs[2], 192, col_w, 130)
    lead_card(leads[4], xs[0], 328, col_w, 130)
    lead_card(leads[5], xs[1], 328, col_w, 130)

    # --- by-the-numbers panel (third slot, row 2) -------------------------
    nx, ny, nw, nh = xs[2], 328, col_w, 130
    d.rectangle([nx, ny, nx + nw, ny + nh], fill=NAVY)
    d.text((nx + 10, ny + 7), "BY THE NUMBERS",
           font=font(SANS_B, 10), fill=GOLD)
    nums = data["numbers"]
    for i, (big, label) in enumerate(nums):
        cx = nx + 10 + (i % 2) * (nw // 2)
        cy = ny + 25 + (i // 2) * 35
        d.text((cx, cy), big, font=font(SANS_B, 14), fill=(255, 255, 255))
        ll = wrap(d, label, font(SANS, 8), nw // 2 - 14, max_lines=2)
        yy = cy + 16
        for line in ll:
            d.text((cx, yy), line, font=font(SANS, 8),
                   fill=(200, 205, 220))
            yy += 9

    # --- world map with numbered pins -------------------------------------
    mx, my, mw, mh = 14, 464, 996, 88
    d.rectangle([mx, my, mx + mw, my + mh], fill=SKY, outline=LINE, width=1)
    d.text((mx + 8, my + 4), "THE WORLD AT A GLANCE — 16 PINNED STORIES",
           font=font(SANS_B, 9), fill=NAVY)

    def proj(lon, lat):
        return (mx + (lon + 170) / 360 * mw,
                my + 14 + (75 - lat) / 130 * (mh - 18))

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=(196, 204, 186), outline=(150, 160, 140))
    pinned = [s for s in stories if s["kind"] in ("lead", "medium")]
    for s in pinned:
        px, py = proj(s["lon"], s["lat"])
        dx, dy = PIN_DX.get(s["n"], (0, 0))
        px, py = px + dx, py + dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(255, 255, 255), width=1)
        num = str(s["n"])
        fnt = font(SANS_B, 8 if len(num) < 2 else 7)
        d.text((px - d.textlength(num, font=fnt) / 2, py - 5), num,
               font=fnt, fill=(255, 255, 255))

    # --- medium cards (10, two columns x five rows) -----------------------
    d.text((14, 558), "MORE OF THE DAY — TEN STORIES WITH A SCENE EACH",
           font=font(SANS_B, 10), fill=NAVY)
    d.line([14, 572, W - 14, 572], fill=NAVY, width=1)
    mcol_w = 494
    mxs = [14, 14 + mcol_w + 8]
    for i, s in enumerate(mediums):
        col, row = i % 2, i // 2
        cx = mxs[col]
        cy = 576 + row * 28
        chip_w = 44
        SCENES[s["scene"]](d, cx, cy, chip_w, 26)
        d.rectangle([cx, cy, cx + chip_w, cy + 26], outline=LINE, width=1)
        tx = cx + chip_w + 6
        tw = mcol_w - chip_w - 6
        hl = wrap(d, f"{s['n']}. {s['headline']}", font(SANS_B, 10.5),
                  tw - 72, max_lines=1)
        d.text((tx, cy), hl[0], font=font(SANS_B, 10.5), fill=INK)
        hw = d.textlength(hl[0], font=font(SANS_B, 10.5))
        badge(d, tx + hw + 8, cy, s["certainty"], font(SANS_B, 7))
        bl = wrap(d, f"{s['body']} — {s['source']}", font(SANS, 9), tw,
                  max_lines=1)
        d.text((tx, cy + 13), bl[0], font=font(SANS, 9), fill=GREY)

    # --- also-today list (38 one-liners, three columns) -------------------
    ay = 722
    d.text((14, ay), "ALSO TODAY — 38 MORE STORIES",
           font=font(SANS_B, 10), fill=NAVY)
    d.line([14, ay + 16, W - 14, ay + 16], fill=NAVY, width=1)
    acol_w = 326
    axs = [14, 14 + acol_w + gap, 14 + 2 * (acol_w + gap)]
    per_col = 13
    for i, s in enumerate(alsos):
        col, row = i // per_col, i % per_col
        cx = axs[col]
        cy = ay + 22 + row * 12
        dot = BADGE[s["certainty"]]
        d.ellipse([cx, cy + 2, cx + 6, cy + 8], fill=dot)
        fnt = font(SANS, 9.5)
        txt = f"{s['n']}. {s['headline']}"
        if d.textlength(txt, font=fnt) > acol_w - 10:
            fnt = font(SANS, 9)
        d.text((cx + 9, cy), txt, font=fnt, fill=INK)

    # --- UTC timeline ------------------------------------------------------
    ty = 906
    d.rectangle([14, ty, W - 14, ty + 34], fill=(232, 236, 242))
    d.text((22, ty + 4), "UTC TIMELINE", font=font(SANS_B, 9), fill=NAVY)
    d.text((22, ty + 18), "25 NOV 2026", font=font(SANS, 8), fill=GREY)
    tl = data["timeline"]
    slot = (W - 28 - 110) / len(tl)
    for i, (t, ev) in enumerate(tl):
        cx = 14 + 110 + i * slot + 4
        d.text((cx, ty + 3), t, font=font(SANS_B, 9.5), fill=RED)
        el = wrap(d, ev, font(SANS, 8), slot - 8, max_lines=2)
        yy = ty + 15
        for line in el:
            d.text((cx, yy), line, font=font(SANS, 8), fill=INK)
            yy += 9

    # --- date check --------------------------------------------------------
    dy = 946
    d.rectangle([14, dy, W - 14, dy + 38], outline=LINE, width=1)
    d.text((22, dy + 3), "DATE CHECK", font=font(SANS_B, 9), fill=RED)
    dl = wrap(d, data["date_check"], font(SANS, 8.5), W - 28 - 16,
              max_lines=2)
    yy = dy + 15
    for line in dl:
        d.text((22, yy), line, font=font(SANS, 8.5), fill=GREY)
        yy += 11

    # --- footer ------------------------------------------------------------
    d.text((14, 990), "All stories dated Wednesday 25 November 2026 (UTC) · "
           "Sources as credited · Drawn in code — no photographs, no AI images",
           font=font(SANS, 8.5), fill=GREY)
    d.text((14, 1003), "Certainty:  CONFIRMED = multiple major outlets  ·  "
           "REPORTED = single source or claim reported today",
           font=font(SANS, 8.5), fill=GREY)

    img.save(os.path.join(HERE, "entry.png"), format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
