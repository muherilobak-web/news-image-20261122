#!/usr/bin/env python3
"""Draw the news-image-20261122 front page: 'THE WORLD — Sunday 22 November 2026'.

Every picture on the page is drawn here from scratch with Pillow: flat shapes,
thick outlines, no gradients, no downloaded photos, no AI-generated image.
Run: python3 draw.py  ->  writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- palette (flat colours only) ----
PAPER = (247, 243, 234)
INK = (25, 25, 25)
RED = (185, 28, 28)
BLUE = (30, 58, 95)
GREEN = (31, 107, 74)
ORANGE = (217, 119, 6)
NIGHT = (46, 74, 107)
SEA = (38, 84, 130)
GREY = (120, 120, 120)
LIGHT_GREY = (170, 170, 170)
WHITE = (255, 255, 255)
BROWN = (139, 94, 60)
TAN = (210, 180, 140)
DARKGREEN = (46, 90, 60)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centre(d, cx, y, text, f, fill):
    """Draw text centred on cx, top edge at y."""
    d.text((cx, y), text, font=f, fill=fill, anchor="ma")


def wrap(f, text, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if f.getlength(trial) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def star(d, cx, cy, r_out, r_in, fill, points=8):
    """Flat burst star centred on (cx, cy)."""
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def smoke(d, x, y, r, fill=GREY):
    """A small column of three grey puffs rising from (x, y)."""
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    d.ellipse([x - r * 0.8, y - r * 2.2, x + r * 0.8, y - r * 0.6], fill=fill)
    d.ellipse([x - r * 0.6, y - r * 3.4, x + r * 0.6, y - r * 2.2], fill=fill)


def dish(d, cx, base_y, r, fill=INK):
    """A radar dish: stem + shallow tilted bowl, standing on base_y."""
    d.line([(cx, base_y), (cx, base_y - r - 2)], fill=fill, width=4)
    cy = base_y - r - 2
    # crescent bowl, tilted: wide shallow curve, thicker at the low side
    bowl = [(cx - r, cy - r * 0.55), (cx - r * 0.55, cy + r * 0.25),
            (cx, cy + r * 0.45), (cx + r * 0.55, cy + r * 0.25),
            (cx + r, cy - r * 0.75), (cx + r * 0.5, cy - r * 0.15),
            (cx, cy + r * 0.05), (cx - r * 0.5, cy - r * 0.15)]
    d.polygon(bowl, fill=fill)


def drone(d, cx, cy, size, fill, tilt=0):
    """Small fixed-wing drone silhouette: body diamond + wings + prop dot."""
    s = size
    body = [(cx - s, cy + tilt), (cx, cy - s * 0.35 + tilt),
            (cx + s, cy + tilt), (cx, cy + s * 0.35 + tilt)]
    d.polygon(body, fill=fill)
    d.line([(cx - s * 0.5, cy - s * 0.55 + tilt),
            (cx + s * 0.5, cy + s * 0.55 + tilt)], fill=fill, width=3)
    d.ellipse([cx - 3, cy - 3 + tilt, cx + 3, cy + 3 + tilt], fill=WHITE)


def truck(d, x, y, w, fill):
    """Simple military truck: body, cab, wheels."""
    d.rectangle([x, y, x + w, y + 22], fill=fill)
    d.rectangle([x + w - 26, y - 14, x + w, y], fill=fill)
    d.rectangle([x + w - 24, y - 12, x + w - 4, y - 2], fill=BLUE)
    for wx in (x + 10, x + w - 14):
        d.ellipse([wx - 7, y + 20, wx + 7, y + 34], fill=INK)
        d.ellipse([wx - 3, y + 24, wx + 3, y + 30], fill=LIGHT_GREY)


def cactus(d, x, y, h):
    """Flat cactus silhouette."""
    d.rectangle([x - 5, y - h, x + 5, y], fill=GREEN)
    d.rectangle([x - 16, y - h + 14, x - 5, y - h + 26], fill=GREEN)
    d.rectangle([x - 16, y - h + 26, x - 11, y - h + 44], fill=GREEN)
    d.rectangle([x + 5, y - h + 22, x + 16, y - h + 34], fill=GREEN)
    d.rectangle([x + 11, y - h + 34, x + 16, y - h + 52], fill=GREEN)


def waves(d, x0, x1, y, n, fill, amp=4, step=26):
    """A row of small wave humps across [x0, x1] at height y."""
    for i in range(n):
        x = x0 + i * step
        d.arc([x, y - amp, x + step, y + amp], 180, 360, fill=fill, width=3)


def build():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    # ---- outer frame: one object at 300px ----
    d.rectangle([12, 12, 1011, 1011], outline=INK, width=6)

    # ---- masthead ----
    centre(d, 512, 24, "THE WORLD", font(BOLD, 96), INK)
    # date with thin ink rules either side
    date_f = font(BOLD, 48)
    date_w = date_f.getlength("SUNDAY 22 NOVEMBER 2026")
    dx0 = 512 - date_w / 2
    dx1 = 512 + date_w / 2
    d.line([(34, 150), (dx0 - 18, 150)], fill=INK, width=3)
    d.line([(dx1 + 18, 150), (990, 150)], fill=INK, width=3)
    centre(d, 512, 126, "SUNDAY 22 NOVEMBER 2026", date_f, RED)
    centre(d, 512, 178, "Eight stories from a single day \u2014 "
           "every picture drawn for this page.", font(REG, 20), INK)

    # ---- lead headline ----
    centre(d, 512, 208, "GULF WAR WIDENS \u2014", font(BOLD, 42), INK)
    centre(d, 512, 254, "IRAN HITS FOUR US BASES", font(BOLD, 42), INK)

    # ---- lead panels ----
    lead_panel(d, 24, 488, "BAHRAIN", draw_bahrain,
               "Iran fires drones and missiles at four US bases in Bahrain; "
               "Manama says defences intercepted them.")
    lead_panel(d, 524, 476, "STRAIT OF HORMUZ", draw_hormuz,
               "Three tankers hit near the Strait of Hormuz; "
               "no casualties reported.")

    # ---- divider ----
    d.line([(24, 560), (1000, 560)], fill=INK, width=4)

    # ---- secondary grid: 3 x 2 ----
    grid_panel(d, 24, 570, (220, 230, 242), draw_drones,
               "IRAN CLAIMS TWO", "US DRONES DOWNED")
    grid_panel(d, 356, 570, (246, 222, 220), draw_cop31,
               "CLIMATE TALKS", "DEADLOCK AT COP31")
    grid_panel(d, 688, 570, (240, 230, 218), draw_peru,
               "QUAKE SHAKES PERU", "6.9, NONE REPORTED")
    grid_panel(d, 24, 766, (220, 233, 245), draw_mexico,
               "FBI MOST-WANTED", "SEIZED IN MEXICO")
    grid_panel(d, 356, 766, (226, 240, 223), draw_baltic,
               "DRONES HIT RUSSIAN", "SHIP IN THE BALTIC")
    grid_panel(d, 688, 766, (221, 240, 228), draw_apec,
               "TRUMP IN SHENZHEN", "XI, PUTIN TALKS DUE")

    # ---- footer ----
    centre(d, 512, 964, "Drawn for this page \u2014 no photographs. "
           "Sunday 22 November 2026.", font(REG, 18), INK)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("saved", out, img.size, os.path.getsize(out), "bytes")


def lead_panel(d, x, w, chip, draw_fn, caption):
    """Lead panel: y 302-548. Illustration 302-466, caption bar below."""
    y0, y1 = 302, 548
    d.rectangle([x, y0, x + w - 1, y1], outline=INK, width=3)
    draw_fn(d, x + 3, y0 + 3, x + w - 3, 466)
    d.line([(x, 466), (x + w - 1, 466)], fill=INK, width=3)
    # chip
    chip_f = font(BOLD, 18)
    cw = chip_f.getlength(chip) + 20
    d.rounded_rectangle([x + 12, y0 + 12, x + 12 + cw, y0 + 40],
                        radius=6, fill=WHITE, outline=INK, width=2)
    d.text((x + 22, y0 + 15), chip, font=chip_f, fill=INK)
    # caption, wrapped, centred, 22px regular
    cap_f = font(REG, 22)
    lines = wrap(cap_f, caption, w - 24)
    y = 466
    for line in lines:
        centre(d, x + w // 2, y, line, cap_f, INK)
        y += 25


def grid_panel(d, x, y, tint, draw_fn, line1, line2):
    """Grid panel 320x184: pale tint, 3px ink border, illustration on top,
    two-line bold headline below (25px, never below 24px)."""
    d.rectangle([x, y, x + 319, y + 183], fill=tint, outline=INK, width=3)
    draw_fn(d, x, y)
    hf = font(BOLD, 25)
    centre(d, x + 160, y + 122, line1, hf, INK)
    centre(d, x + 160, y + 151, line2, hf, INK)


# ================= lead illustrations =================

def draw_bahrain(d, x0, y0, x1, y1):
    """Night sky over a base: radar dishes, missile trails, orange glow."""
    d.rectangle([x0, y0, x1, y1], fill=NIGHT)
    # stars (fixed positions, no randomness)
    for sx, sy in [(x0 + 40, y0 + 22), (x0 + 120, y0 + 14), (x0 + 210, y0 + 30),
                   (x0 + 300, y0 + 16), (x0 + 380, y0 + 26), (x0 + 450, y0 + 12),
                   (x0 + 70, y0 + 52), (x0 + 340, y0 + 48)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # missile trails: three diagonal lines with burst stars at the top
    for (tx, ty, bx, by) in [(x0 + 90, y0 + 30, x0 + 40, y1 - 40),
                             (x0 + 250, y0 + 18, x0 + 210, y1 - 40),
                             (x0 + 400, y0 + 34, x0 + 350, y1 - 40)]:
        d.line([(bx, by), (tx, ty)], fill=ORANGE, width=4)
        d.line([(bx, by), (tx, ty)], fill=WHITE, width=2)
        star(d, tx, ty, 17, 7, ORANGE)
    # orange glow along the bottom
    d.rectangle([x0, y1 - 46, x1, y1 - 34], fill=ORANGE)
    # base silhouette with two radar dishes
    d.rectangle([x0, y1 - 34, x1, y1], fill=INK)
    d.rectangle([x0 + 60, y1 - 58, x0 + 150, y1 - 34], fill=INK)
    d.rectangle([x0 + 320, y1 - 52, x0 + 400, y1 - 34], fill=INK)
    dish(d, x0 + 105, y1 - 58, 22)
    dish(d, x0 + 360, y1 - 52, 18)
    # small grey smoke columns
    smoke(d, x0 + 190, y1 - 60, 7)
    smoke(d, x0 + 440, y1 - 56, 6)


def draw_hormuz(d, x0, y0, x1, y1):
    """Dark blue sea, two tankers, a mine, fire and smoke on the big one."""
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    waves(d, x0 + 8, x1 - 8, y0 + 130, 16, (140, 180, 210))
    waves(d, x0 + 8, x1 - 8, y0 + 148, 16, (110, 150, 190))
    # second, smaller tanker behind (upper left)
    tx, ty = x0 + 30, y0 + 52
    d.polygon([(tx, ty + 26), (tx + 150, ty + 26), (tx + 138, ty + 44),
               (tx + 8, ty + 44)], fill=(20, 48, 80))
    d.rectangle([tx + 96, ty + 6, tx + 122, ty + 26], fill=(20, 48, 80))
    d.rectangle([tx + 40, ty + 12, tx + 62, ty + 26], fill=(20, 48, 80))
    # big tanker (lower right)
    bx, by = x0 + 150, y0 + 78
    d.polygon([(bx, by + 34), (bx + 300, by + 34), (bx + 282, by + 62),
               (bx + 10, by + 62)], fill=INK)
    d.rectangle([bx + 210, by + 8, bx + 250, by + 34], fill=INK)
    d.rectangle([bx + 258, by + 14, bx + 268, by + 34], fill=RED)
    d.rectangle([bx + 60, by + 18, bx + 100, by + 34], fill=INK)
    d.rectangle([bx + 110, by + 22, bx + 150, by + 34], fill=INK)
    # fire burst + smoke on the deck
    star(d, bx + 130, by + 12, 20, 8, ORANGE)
    star(d, bx + 130, by + 12, 11, 5, (255, 200, 60))
    smoke(d, bx + 130, by - 6, 8)
    # round mine floating near the first tanker
    mx, my = bx - 42, by + 46
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=INK)
    for dx, dy in [(-14, 0), (14, 0), (0, -14), (0, 14),
                   (-10, -10), (10, -10), (-10, 10), (10, 10)]:
        d.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=3)


# ================= grid illustrations =================

def draw_drones(d, x, y):
    """Two falling drones trailing smoke over a sea strip, radar dish below."""
    # sea strip at the bottom of the illustration area
    d.rectangle([x + 3, y + 88, x + 316, y + 116], fill=SEA)
    waves(d, x + 12, x + 308, y + 100, 11, (140, 180, 210))
    # smoke trails from the falling drones
    d.line([(x + 110, y + 30), (x + 80, y + 62)], fill=GREY, width=3)
    d.line([(x + 215, y + 42), (x + 240, y + 70)], fill=GREY, width=3)
    drone(d, x + 112, y + 26, 20, INK, tilt=6)
    drone(d, x + 212, y + 38, 16, INK, tilt=-8)
    # radar dish on the sea strip
    dish(d, x + 160, y + 116, 16)


def draw_cop31(d, x, y):
    """Round table, small flags at the sides, cracked earth above,
    crossed oil drop at the top right."""
    cx = x + 160
    # cracked earth: brown circle with a jagged crack, above the table
    d.ellipse([cx - 28, y + 10, cx + 28, y + 66], fill=BROWN, outline=INK, width=3)
    d.line([(cx - 16, y + 18), (cx - 5, y + 34), (cx - 14, y + 44),
            (cx + 2, y + 56)], fill=INK, width=3)
    d.line([(cx + 6, y + 34), (cx + 18, y + 42)], fill=INK, width=3)
    # round table
    d.ellipse([x + 52, y + 80, x + 268, y + 112], fill=WHITE, outline=INK, width=3)
    d.rectangle([x + 152, y + 108, x + 168, y + 116], fill=INK)
    # small flags on poles at the sides of the table
    for fx, fc in [(x + 66, RED), (x + 232, GREEN)]:
        d.line([(fx, y + 44), (fx, y + 84)], fill=INK, width=3)
        d.polygon([(fx, y + 44), (fx + 22, y + 50), (fx, y + 58)], fill=fc)
    # crossed oil drop (red "no" symbol) at the top right
    ox, oy = x + 284, y + 30
    d.polygon([(ox, oy - 12), (ox + 9, oy + 6), (ox - 9, oy + 6)], fill=INK)
    d.ellipse([ox - 9, oy - 2, ox + 9, oy + 14], fill=INK)
    d.ellipse([ox - 16, oy - 16, ox + 16, oy + 16], outline=RED, width=4)
    d.line([(ox - 12, oy + 12), (ox + 12, oy - 12)], fill=RED, width=4)


def draw_peru(d, x, y):
    """Mountain ridge with a jagged crack, shaking buildings, wavy ground."""
    # mountains
    d.polygon([(x + 10, y + 100), (x + 120, y + 18), (x + 210, y + 100)],
              fill=BROWN, outline=INK)
    d.polygon([(x + 150, y + 100), (x + 240, y + 34), (x + 310, y + 100)],
              fill=(160, 110, 70), outline=INK)
    # snow caps
    d.polygon([(x + 104, y + 32), (x + 120, y + 18), (x + 136, y + 32),
               (x + 126, y + 40), (x + 114, y + 40)], fill=WHITE)
    # jagged crack down the big mountain
    d.line([(x + 120, y + 30), (x + 108, y + 52), (x + 126, y + 70),
            (x + 110, y + 92)], fill=INK, width=3)
    # wavy ground line
    d.line([(x + 6, y + 102), (x + 40, y + 96), (x + 74, y + 104),
            (x + 110, y + 97), (x + 146, y + 104), (x + 182, y + 97),
            (x + 218, y + 104), (x + 254, y + 97), (x + 314, y + 102)],
           fill=INK, width=3)
    # shaking buildings at the base
    for bx in (x + 60, x + 110, x + 210):
        d.polygon([(bx, y + 104), (bx + 4, y + 78), (bx + 30, y + 76),
                   (bx + 34, y + 104)], fill=WHITE, outline=INK, width=2)
        d.line([(bx - 10, y + 84), (bx - 4, y + 84)], fill=INK, width=2)
        d.line([(bx + 40, y + 90), (bx + 46, y + 90)], fill=INK, width=2)


def draw_mexico(d, x, y):
    """Desert road, cacti, a convoy of three military trucks, handcuffs."""
    # desert road band
    d.rectangle([x + 3, y + 78, x + 316, y + 116], fill=TAN)
    d.line([(x + 3, y + 78), (x + 316, y + 78)], fill=INK, width=2)
    d.line([(x + 3, y + 97), (x + 316, y + 97)], fill=INK, width=2)
    for dx in range(14, 310, 34):
        d.line([(x + dx, y + 97), (x + dx + 16, y + 97)], fill=WHITE, width=3)
    # cacti
    cactus(d, x + 34, y + 78, 34)
    cactus(d, x + 288, y + 78, 28)
    # convoy of three trucks on the road
    truck(d, x + 66, y + 66, 62, DARKGREEN)
    truck(d, x + 148, y + 66, 62, DARKGREEN)
    truck(d, x + 230, y + 66, 62, DARKGREEN)
    # handcuffs above the lead truck
    hx, hy = x + 261, y + 30
    d.ellipse([hx - 26, hy - 10, hx - 6, hy + 10], outline=INK, width=4)
    d.ellipse([hx + 6, hy - 10, hx + 26, hy + 10], outline=INK, width=4)
    d.line([(hx - 6, hy), (hx + 6, hy)], fill=INK, width=4)


def draw_baltic(d, x, y):
    """Grey sea, cargo ship with containers, two drones, a burst on deck."""
    d.rectangle([x + 3, y + 60, x + 316, y + 116], fill=(150, 160, 170))
    waves(d, x + 12, x + 308, y + 76, 11, WHITE)
    waves(d, x + 12, x + 308, y + 106, 11, (200, 205, 210))
    # cargo ship
    d.polygon([(x + 46, y + 78), (x + 274, y + 78), (x + 258, y + 104),
               (x + 62, y + 104)], fill=INK)
    # containers
    for i, cc in enumerate([RED, BLUE, GREEN, ORANGE]):
        d.rectangle([x + 66 + i * 34, y + 52, x + 96 + i * 34, y + 78],
                    fill=cc, outline=INK, width=2)
    d.rectangle([x + 216, y + 44, x + 240, y + 78], fill=WHITE, outline=INK, width=2)
    # drones above, burst on the deck
    drone(d, x + 90, y + 24, 15, INK, tilt=4)
    drone(d, x + 210, y + 16, 13, INK, tilt=-6)
    star(d, x + 150, y + 52, 14, 6, ORANGE)


def draw_apec(d, x, y):
    """Three flag poles with plain flags, a small globe below."""
    # flag poles
    for fx in (x + 70, x + 160, x + 250):
        d.line([(fx, y + 14), (fx, y + 84)], fill=INK, width=3)
    # flag 1: US flag — red-white stripes, blue canton with white stars
    fx0, fy0, fx1, fy1 = x + 70, y + 16, x + 112, y + 40
    for i in range(7):
        sy0 = fy0 + i * (fy1 - fy0) // 7
        sy1 = fy0 + (i + 1) * (fy1 - fy0) // 7
        d.rectangle([fx0, sy0, fx1, sy1], fill=RED if i % 2 == 0 else WHITE)
    canton_w = 18
    canton_h = (fy1 - fy0) * 4 // 7
    d.rectangle([fx0, fy0, fx0 + canton_w, fy0 + canton_h], fill=BLUE)
    for sx, sy in [(fx0 + 5, fy0 + 4), (fx0 + 12, fy0 + 4),
                   (fx0 + 5, fy0 + 10), (fx0 + 12, fy0 + 10)]:
        star(d, sx, sy, 2, 1, WHITE, points=5)
    d.rectangle([fx0, fy0, fx1, fy1], outline=INK, width=2)
    # flag 2: red with small white stars
    d.rectangle([x + 160, y + 16, x + 202, y + 40], fill=RED, outline=INK, width=2)
    for sx, sy in [(x + 170, y + 24), (x + 182, y + 20), (x + 192, y + 28),
                   (x + 174, y + 32), (x + 188, y + 34)]:
        star(d, sx, sy, 4, 2, WHITE, points=5)
    # flag 3: white-blue-red horizontal stripes
    d.rectangle([x + 250, y + 16, x + 292, y + 24], fill=WHITE, outline=INK, width=2)
    d.rectangle([x + 250, y + 24, x + 292, y + 32], fill=BLUE, outline=INK, width=2)
    d.rectangle([x + 250, y + 32, x + 292, y + 40], fill=RED, outline=INK, width=2)
    # globe below
    gx, gy = x + 160, y + 98
    d.ellipse([gx - 18, gy - 16, gx + 18, gy + 16], fill=(150, 190, 230),
              outline=INK, width=3)
    d.ellipse([gx - 12, gy - 8, gx + 2, gy + 4], fill=GREEN)
    d.ellipse([gx + 4, gy + 2, gx + 14, gy + 12], fill=GREEN)


if __name__ == "__main__":
    build()
