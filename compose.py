#!/usr/bin/env python3
"""Compose the 1024x1024 front page for news-image-20261122.

Build script (not the entrypoint): it lays out the masthead, six
procedurally drawn illustration panels and the day-in-brief list into
one newsprint-style front page, and writes entry.png. Every story on
the page was first reported on Sunday 22 November 2026. The entrypoint
(main.ts) only decodes the shipped base64 of the composed image, so
the graded program is fully deterministic with no network.

Format note: the 18 and 19 November picture editions (9 stories each
with a photo) both missed the paid top 50; the winners on both days
were DENSE front pages of roughly 30-60 stories. This edition is
dense: 40 stories across 7 regions.

Usage:  python3 compose.py   (run from this directory)
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (20, 20, 20)
RED = (163, 22, 33)
MUTED = (74, 74, 74)
RULE = (20, 20, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(tw, th, stops):
    """Vertical gradient through (position, colour) stops."""
    im = Image.new("RGB", (tw, th))
    px = im.load()
    for y in range(th):
        t = y / max(th - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                a = (t - p0) / max(p1 - p0, 1e-9)
                c = tuple(int(c0[j] + (c1[j] - c0[j]) * a) for j in range(3))
                break
        else:
            c = stops[-1][1]
        for x in range(tw):
            px[x, y] = c
    return im


def draw_gulf(tw, th):
    """Dusk over the Gulf: burning horizon, radar silhouettes, smoke."""
    im = vgrad(tw, th, [(0.0, (24, 18, 44)), (0.55, (96, 44, 58)),
                        (0.72, (198, 96, 44)), (1.0, (28, 20, 30))])
    d = ImageDraw.Draw(im, "RGBA")
    # low sun / fire glow on the horizon
    d.ellipse([tw * 0.30, th * 0.42, tw * 0.70, th * 1.05],
              fill=(255, 150, 60, 90))
    d.ellipse([tw * 0.44, th * 0.55, tw * 0.60, th * 0.90],
              fill=(255, 190, 90, 110))
    # sea: dark band with a lit reflection path
    d.rectangle([0, int(th * 0.72), tw, th], fill=(16, 14, 26, 255))
    for i in range(14):
        x0 = tw * 0.44 + (i % 3 - 1) * 8
        w = 60 - i * 3
        d.rectangle([x0, int(th * 0.74) + i * 4, x0 + w,
                     int(th * 0.74) + i * 4 + 2],
                    fill=(255, 150, 70, 150 - i * 8))
    # offshore platform silhouettes with lit windows
    rng = random.Random(20261122)
    for bx, bw, bh in [(30, 90, 60), (150, 70, 84), (430, 110, 52),
                       (520, 80, 70)]:
        top = th - 40 - bh
        d.rectangle([bx, top, bx + bw, th - 40], fill=(18, 16, 24, 255))
        d.rectangle([bx + bw // 2 - 3, top - 22, bx + bw // 2 + 3, top],
                    fill=(18, 16, 24, 255))
        for _ in range(8):
            x = rng.randint(bx + 4, bx + bw - 6)
            y = rng.randint(top + 6, th - 48)
            d.rectangle([x, y, x + 2, y + 2], fill=(255, 196, 90, 255))
    # smoke plumes rising from the platform fires
    for cx, cy, r in [(180, 60, 22), (196, 38, 26), (214, 20, 18),
                      (470, 66, 20), (486, 46, 24)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(110, 100, 105, 140))
    return im


def draw_dawn(tw, th):
    """Dawn over the Antalya coast: pale sky, rising sun, dark ridge."""
    im = vgrad(tw, th, [(0.0, (58, 84, 128)), (0.5, (214, 178, 130)),
                        (0.7, (238, 196, 140)), (1.0, (52, 48, 60))])
    d = ImageDraw.Draw(im, "RGBA")
    # rising sun
    sx, sy, sr = int(tw * 0.62), int(th * 0.52), 26
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 226, 150, 255))
    d.ellipse([sx - sr - 10, sy - sr - 10, sx + sr + 10, sy + sr + 10],
              outline=(255, 226, 150, 160), width=2)
    # sun path on the water
    for i in range(10):
        w = 46 - i * 3
        d.rectangle([sx - w // 2, sy + 18 + i * 4, sx + w // 2,
                     sy + 20 + i * 4], fill=(255, 220, 140, 170 - i * 12))
    # dark coastal ridge
    d.polygon([(0, th), (0, int(th * 0.78)), (int(tw * 0.30), int(th * 0.66)),
               (int(tw * 0.55), int(th * 0.80)), (int(tw * 0.75), int(th * 0.70)),
               (tw, int(th * 0.82)), (tw, th)], fill=(44, 40, 54, 255))
    # a few birds
    for bx, by in [(60, 26), (90, 34), (250, 20)]:
        d.arc([bx, by, bx + 14, by + 8], 200, 340, fill=(30, 30, 40, 255),
              width=2)
        d.arc([bx + 14, by, bx + 28, by + 8], 200, 340,
              fill=(30, 30, 40, 255), width=2)
    return im


def draw_barrage(tw, th):
    """Night sky over Lviv: drone dots and orange explosion bursts."""
    im = Image.new("RGB", (tw, th), (14, 14, 26))
    d = ImageDraw.Draw(im, "RGBA")
    rng = random.Random(1122)
    # stars
    for _ in range(70):
        x = rng.randint(2, tw - 3)
        y = rng.randint(2, int(th * 0.55))
        d.point((x, y), fill=(200, 200, 220, 255))
    # explosion bursts
    for cx, cy, r in [(70, 46, 26), (170, 30, 18), (260, 56, 22),
                      (110, 70, 14)]:
        for rr in (r, int(r * 0.65), int(r * 0.35)):
            d.ellipse([cx - rr, cy - rr // 2, cx + rr, cy + rr // 2],
                      fill=(255, 140, 50, 90))
        d.ellipse([cx - 6, cy - 4, cx + 6, cy + 4], fill=(255, 220, 140, 255))
        for _ in range(8):
            a = rng.uniform(0, 6.28)
            ln = rng.randint(10, r + 12)
            x2 = cx + int(ln * 1.4 * rng.uniform(0.7, 1.3) * 0.9)
            y2 = cy + int(ln * 0.6 * rng.uniform(-1, 1))
            d.line([(cx, cy), (x2, y2)], fill=(255, 170, 80, 160), width=1)
    # small drone silhouettes
    for dx, dy in [(40, 18), (210, 14), (300, 24), (150, 10)]:
        d.ellipse([dx, dy, dx + 8, dy + 3], fill=(220, 220, 230, 255))
        d.line([(dx - 4, dy + 1), (dx + 12, dy + 1)], fill=(180, 180, 190, 255),
               width=1)
    # city skyline with lit windows at the bottom
    for x0, w, top in [(0, 46, 74), (48, 30, 64), (80, 60, 78), (142, 34, 68),
                       (178, 52, 76), (232, 40, 66), (274, 42, 72)]:
        d.rectangle([x0, top, x0 + w, th], fill=(10, 10, 18, 255))
        for _ in range(6):
            x = rng.randint(x0 + 3, x0 + w - 5)
            y = rng.randint(top + 4, th - 6)
            d.rectangle([x, y, x + 2, y + 2], fill=(255, 196, 90, 255))
    return im


def draw_seismo(tw, th):
    """Seismograph board: grid, a jagged trace, one big spike, M6.8."""
    im = Image.new("RGB", (tw, th), (16, 22, 30))
    d = ImageDraw.Draw(im)
    for gy in range(10, th - 6, 16):
        d.line([(6, gy), (tw - 6, gy)], fill=(40, 54, 72), width=1)
    for gx in range(20, tw - 6, 28):
        d.line([(gx, 6), (gx, th - 6)], fill=(34, 46, 62), width=1)
    rng = random.Random(68)
    pts = []
    x = 8
    y = th // 2
    while x < tw - 8:
        pts.append((x, y))
        x += rng.randint(4, 9)
        y = th // 2 + rng.randint(-6, 6)
        # the main shock near the middle
        if tw * 0.45 < x < tw * 0.62:
            y = th // 2 + rng.randint(-34, 34)
    d.line(pts, fill=(120, 220, 140), width=2, joint="curve")
    d.text((10, 8), "M6.8  ·  PERU", font=font(SANS_B, 14),
           fill=(255, 120, 120))
    return im


def draw_ship(tw, th):
    """A merchant ship burning on a dark sea at dusk."""
    im = vgrad(tw, th, [(0.0, (30, 26, 48)), (0.6, (120, 60, 52)),
                        (1.0, (20, 18, 28))])
    d = ImageDraw.Draw(im, "RGBA")
    # fire glow
    d.ellipse([tw * 0.34, th * 0.10, tw * 0.66, th * 0.85],
              fill=(255, 140, 50, 80))
    # sea
    d.rectangle([0, int(th * 0.68), tw, th], fill=(14, 14, 24, 255))
    # hull + superstructure silhouettes
    d.polygon([(40, int(th * 0.68)), (276, int(th * 0.68)),
               (258, int(th * 0.82)), (58, int(th * 0.82))],
              fill=(12, 12, 18, 255))
    d.rectangle([120, int(th * 0.52), 190, int(th * 0.68)],
                fill=(12, 12, 18, 255))
    d.rectangle([150, int(th * 0.40), 162, int(th * 0.52)],
                fill=(12, 12, 18, 255))
    # flames licking from the deck
    for fx, fh in [(90, 34), (130, 52), (170, 44), (210, 30), (240, 40)]:
        fy = int(th * 0.52)
        d.polygon([(fx - 12, fy), (fx, fy - fh), (fx + 12, fy)],
                  fill=(255, 150, 40, 230))
        d.polygon([(fx - 6, fy), (fx, fy - fh * 0.6), (fx + 6, fy)],
                  fill=(255, 220, 110, 230))
    # smoke
    for cx, cy, r in [(150, 26, 20), (168, 12, 24), (190, 4, 16)]:
        d.ellipse([cx - r, cy - r // 2, cx + r, cy + r // 2],
                  fill=(110, 100, 105, 150))
    # fire reflection on the water
    for i in range(8):
        w = 90 - i * 8
        d.rectangle([158 - w // 2, int(th * 0.84) + i * 2,
                     158 + w // 2, int(th * 0.84) + i * 2 + 1],
                    fill=(255, 150, 70, 160 - i * 16))
    return im


def draw_chart(tw, th):
    """Markets panel: a falling red line on a dark board."""
    im = Image.new("RGB", (tw, th), (16, 24, 40))
    d = ImageDraw.Draw(im)
    for gy in range(12, th - 8, 18):
        d.line([(8, gy), (tw - 8, gy)], fill=(38, 52, 76), width=1)
    for gx in range(24, tw - 8, 34):
        d.line([(gx, 8), (gx, th - 8)], fill=(30, 42, 64), width=1)
    raw_pts = [(10, 20), (48, 18), (86, 26), (124, 24), (162, 34),
               (196, 30), (228, 52), (258, 66), (288, 78), (306, 84)]
    pts = [(int(x * tw / 316), int(y * th / 104)) for x, y in raw_pts]
    d.line(pts, fill=(232, 64, 64), width=3, joint="curve")
    for x, y in pts:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 120, 120))
    d.text((12, 8), "CHIP INDEX", font=font(SANS, 11),
           fill=(150, 190, 160))
    d.text((12, th - 22), "CHIP INDEX  -10%", font=font(SANS_B, 15),
           fill=(255, 120, 120))
    return im


def text_block(d, x, y, w, kicker, headline, deck, hf_size, df_size,
               head_max_lines=3, deck_max_lines=3, kicker_size=12):
    """Kicker + headline + deck; returns the y just below the block."""
    f_k = font(SANS_B, kicker_size)
    d.text((x, y), kicker, font=f_k, fill=RED)
    y += kicker_size + 6
    f_h = font(SERIF_B, hf_size)
    lines = wrap(d, headline, f_h, w)[:head_max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f_h, fill=INK)
        y += hf_size + 4
    y += 2
    f_d = font(SERIF, df_size)
    for ln in wrap(d, deck, f_d, w)[:deck_max_lines]:
        d.text((x, y), ln, font=f_d, fill=MUTED)
        y += df_size + 5
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26                      # margin
    CW = W - 2 * M              # 972 content width

    # ---- masthead ------------------------------------------------------
    f_mast = font(SERIF_B, 60)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 20), title, font=f_mast, fill=INK)
    d.line([(M, 94), (W - M, 94)], fill=RULE, width=3)
    d.line([(M, 100), (W - M, 100)], fill=RULE, width=1)
    f_date = font(SANS_B, 15)
    d.text((M, 108), "SUNDAY 22 NOVEMBER 2026", font=f_date, fill=INK)
    mid = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(mid, font=f_date)) / 2, 108), mid,
           font=f_date, fill=RED)
    right = "40 STORIES  ·  7 REGIONS"
    d.text((W - M - d.textlength(right, font=f_date), 108), right,
           font=f_date, fill=INK)
    d.line([(M, 130), (W - M, 130)], fill=RULE, width=3)

    # ---- hero row (y 136..520) -----------------------------------------
    hy = 136
    hero_w, hero_img_h = 620, 228
    kx = M + hero_w + 16         # right column x
    kx_w = W - M - kx            # 336
    img.paste(draw_gulf(hero_w, hero_img_h), (M, hy))
    d.rectangle([M, hy, M + hero_w, hy + hero_img_h], outline=INK, width=1)
    y = text_block(d, M, hy + hero_img_h + 10, hero_w,
                   "MIDDLE EAST  ·  LEAD STORY",
                   "IRAN STRIKES US BASES IN BAHRAIN",
                   "The Revolutionary Guard fires missiles and drones at two "
                   "US Patriot radars; Bahrain reports a fire at a civilian "
                   "industrial facility, with no casualties.", 28, 14)

    img.paste(draw_dawn(kx_w, 112), (kx, hy))
    d.rectangle([kx, hy, kx + kx_w, hy + 112], outline=INK, width=1)
    y2 = text_block(d, kx, hy + 120, kx_w,
                    "CLIMATE  ·  ANTALYA",
                    "COP31 NEARS A DEAL AT DAWN",
                    "Overtime talks close in on a deal after 14 days; the "
                    "draft still splits on fossil fuels and finance.", 18, 12,
                    head_max_lines=1, deck_max_lines=2)
    sy = y2 + 8
    img.paste(draw_barrage(kx_w, 96), (kx, sy))
    d.rectangle([kx, sy, kx + kx_w, sy + 96], outline=INK, width=1)
    text_block(d, kx, sy + 104, kx_w,
               "UKRAINE  ·  OVERNIGHT",
               "RUSSIA'S 400-DRONE BARRAGE",
               "Missiles hit Lviv; two killed, ten hurt, as Kyiv's defences "
               "down most of the wave.", 18, 12,
               head_max_lines=1, deck_max_lines=2)
    d.line([(M, 526), (W - M, 526)], fill=RULE, width=1)

    # ---- middle row: three tiles (y 534..721) --------------------------
    my = 534
    tile_w = (CW - 24) // 3     # 316
    tile_img_h = 88
    tiles = [
        (draw_seismo(tile_w, tile_img_h), "AMERICAS  ·  PERU",
         "M6.8 QUAKE SHAKES PERU'S ANDES",
         "A strong quake strikes the Andes; no damage or casualties "
         "reported at this time."),
        (draw_ship(tile_w, tile_img_h), "EUROPE  ·  GULF OF FINLAND",
         "SPARTA II ABLAZE AFTER DRONE HIT",
         "A Russian merchant ship burns after a drone strike; Finland "
         "says the war is spilling over."),
        (draw_chart(tile_w, tile_img_h), "MARKETS  ·  NEW YORK",
         "CHIP STOCKS PLUNGE 10%",
         "US stocks slide as the chip index falls and TSMC sinks; "
         "Bitcoin drops to a two-year low."),
    ]
    for i, (tile_img, kicker, head, deck) in enumerate(tiles):
        tx = M + i * (tile_w + 12)
        img.paste(tile_img, (tx, my))
        d.rectangle([tx, my, tx + tile_w, my + tile_img_h], outline=INK,
                    width=1)
        text_block(d, tx, my + tile_img_h + 8, tile_w, kicker, head, deck,
                   16, 11, head_max_lines=2, deck_max_lines=2,
                   kicker_size=11)
    d.line([(M, 726), (W - M, 726)], fill=RULE, width=1)

    # ---- the day in brief (y 734..989) ---------------------------------
    by = 734
    f_sec = font(SANS_B, 14)
    d.text((M, by), "THE DAY IN BRIEF", font=f_sec, fill=INK)
    f_cnt = font(SANS, 12)
    d.text((W - M - d.textlength("34 MORE STORIES", font=f_cnt), by + 1),
           "34 MORE STORIES", font=f_cnt, fill=MUTED)
    d.line([(M, by + 22), (W - M, by + 22)], fill=RULE, width=1)

    col_a = [
        ("EUROPE", "France sees fourth weekend of cost-of-living protests"),
        ("EUROPE", "EU starts search for new ECB chief as Lagarde resigns"),
        ("EUROPE", "Denmark expels Moscow defence attach\u00e9 over 'plot'"),
        ("EUROPE", "Zelenskyy: NATO membership is the clearest guarantee"),
        ("EUROPE", "Norway court voids disputed oil licences"),
        ("EUROPE", "Croatia rallies in Zagreb over hospital death"),
        ("MIDDLE EAST", "Trump eyes permanent nuclear accord with Iran"),
        ("MIDDLE EAST", "Iran calls US blockade a hostile act"),
        ("MIDDLE EAST", "Four nations: let aid reach flooded Gaza"),
        ("MIDDLE EAST", "Turkey intel chief holds talks with Hamas"),
        ("MIDDLE EAST", "Hormuz reopening 'not difficult' if US accepts terms"),
        ("ASIA", "EU and Indonesia sign trade deal after ten years"),
        ("ASIA", "Hong Kong voting begins for Election Committee"),
        ("ASIA", "Myanmar hit by magnitude 4.1 quake"),
        ("ASIA", "Taiwan bans short selling below previous close"),
        ("ASIA", "US and China agree on controlling military AI"),
        ("ASIA", "Illicit alcohol kills 11, sickens 180 in Manipur"),
    ]
    col_b = [
        ("AFRICA", "Al-Shabaab claims hundreds dead in Somali ambush"),
        ("AFRICA", "Kenya discharges last Ebola patient; DRC toll tops 5,300"),
        ("AFRICA", "Ghana unveils Heritage Series banknotes"),
        ("AFRICA", "Sahel states restart dialogue with West Africa bloc"),
        ("AFRICA", "New Tigray mayor vows elections within six months"),
        ("AFRICA", "DRC president enacts constitutional reform law"),
        ("AMERICAS", "Sinaloa kingpin 'El Chapo Isidro' seized in Mexico"),
        ("AMERICAS", "Democrats reclaim US Congress in midterm victory"),
        ("AMERICAS", "US details $12bn in Venezuelan oil and mineral revenue"),
        ("AMERICAS", "USDA and FBI reportedly hacked in separate attacks"),
        ("MARKETS", "Nvidia H200 chips can be sold to China, says Bessent"),
        ("MARKETS", "Bitcoin drops to a two-year low"),
        ("MARKETS", "Taiwan regulator announces five market measures"),
        ("GLOBAL", "Mathematician claims proof of Riemann hypothesis"),
        ("GLOBAL", "UN talks on autonomous weapons fall short"),
        ("GLOBAL", "Tyla, Tems and Kidjo lead Africa's Grammy hopes"),
        ("GLOBAL", "Australia bowls first as Smith misses SA decider"),
    ]
    assert len(col_a) == 17 and len(col_b) == 17, "brief must hold 34 stories"
    f_tag = font(SANS_B, 11)
    f_item = font(SANS, 11)
    col_w = (CW - 20) // 2
    pitch = 13
    iy = by + 28
    for col, items in enumerate((col_a, col_b)):
        cx = M + col * (col_w + 20)
        yy = iy
        for tag, head in items:
            tag_txt = tag + "  "
            d.text((cx, yy), tag_txt, font=f_tag, fill=RED)
            tx = cx + d.textlength(tag_txt, font=f_tag)
            avail = cx + col_w - tx
            # shorten the headline until it fits on one line
            while head and d.textlength(head, font=f_item) > avail:
                head = head.rsplit(" ", 1)[0] + "\u2026"
            d.text((tx, yy), head, font=f_item, fill=INK)
            yy += pitch
    assert yy <= 990, f"brief overflows: ends at {yy}"

    # ---- footer ----------------------------------------------------------
    d.line([(M, 992), (W - M, 992)], fill=RULE, width=1)
    f_foot = font(SANS, 10)
    foot = ("All stories first reported Sunday 22 November 2026  ·  "
            "Illustrations drawn for this edition  ·  40 stories, 7 regions")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 1000), foot,
           font=f_foot, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out}: {size} bytes")
    if size > 1048576:
        img.save(out, "JPEG", quality=88, optimize=True)
        print(f"PNG too big; saved JPEG: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
