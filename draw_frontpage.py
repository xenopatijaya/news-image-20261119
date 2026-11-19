#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026.

A newspaper front page: masthead with the date, two lead stories
(the Shenzhen trilateral and the GTA VI rollout), a world map with
eight flashpoints, and a grid of 40 short labelled stories across
six continents. Everything is drawn with PIL from scratch.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 683
PAPER = (253, 248, 236)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (24, 62, 120)
SEA = (214, 230, 240)
LAND = (232, 222, 198)
LAND_EDGE = (170, 158, 124)
GREY = (90, 90, 90)
RULE = (150, 140, 118)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_halo(draw, xy, s, fnt, fill, halo=(253, 248, 236)):
    x, y = xy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), s, font=fnt, fill=halo)
    draw.text((x, y), s, font=fnt, fill=fill)


# ---------------------------------------------------------------- map
# Rough lon/lat outlines (stylised, recognisable at small size).
NORTH_AMERICA = [(-168, 66), (-150, 70), (-130, 71), (-115, 73), (-100, 73),
                 (-90, 74), (-82, 73), (-76, 70), (-70, 62), (-60, 60),
                 (-55, 52), (-55, 47), (-65, 44), (-70, 42), (-75, 36),
                 (-80, 26), (-84, 30), (-90, 21), (-96, 17), (-90, 14),
                 (-84, 12), (-80, 8), (-83, 9), (-90, 14), (-97, 16),
                 (-104, 20), (-110, 23), (-114, 29), (-120, 34), (-125, 41),
                 (-124, 48), (-130, 55), (-140, 60), (-152, 58), (-162, 58),
                 (-168, 66)]
GREENLAND = [(-58, 64), (-48, 60), (-40, 63), (-32, 68), (-22, 70),
             (-25, 76), (-35, 80), (-50, 79), (-58, 76), (-60, 70)]
SOUTH_AMERICA = [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0),
                 (-44, -3), (-35, -8), (-38, -15), (-41, -23), (-48, -28),
                 (-53, -33), (-58, -38), (-65, -41), (-68, -50), (-70, -54),
                 (-73, -50), (-73, -40), (-72, -30), (-70, -18), (-76, -15),
                 (-81, -6), (-81, 0), (-80, 5), (-79, 9)]
AFRICA = [(-6, 35), (-10, 31), (-17, 15), (-17, 12), (-12, 8), (-8, 5),
          (-4, 5), (6, 4), (9, 4), (13, 0), (12, -5), (13, -12), (12, -18),
          (15, -27), (19, -34), (26, -34), (32, -28), (35, -22), (40, -15),
          (40, -10), (42, -4), (46, 0), (51, 11), (48, 11), (43, 12),
          (40, 15), (38, 18), (37, 22), (34, 28), (32, 31), (30, 31),
          (22, 33), (19, 32), (11, 34), (10, 37), (5, 37), (-6, 35)]
EURASIA = [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50),
           (3, 51), (8, 54), (8, 57), (10, 59), (5, 60), (5, 62), (12, 65),
           (18, 69), (25, 71), (30, 70), (35, 68), (42, 68), (50, 69),
           (60, 70), (68, 72), (78, 73), (88, 74), (98, 76), (108, 77),
           (118, 73), (128, 72), (138, 71), (148, 72), (158, 70), (168, 67),
           (178, 65), (178, 62), (170, 60), (162, 60), (158, 53), (150, 59),
           (142, 55), (140, 50), (135, 43), (130, 42), (127, 40), (122, 38),
           (120, 32), (118, 25), (110, 20), (108, 18), (105, 10), (100, 8),
           (98, 10), (94, 16), (92, 21), (88, 22), (86, 20), (80, 15),
           (77, 8), (75, 12), (72, 20), (66, 25), (62, 25), (58, 25),
           (56, 26), (52, 28), (50, 29), (48, 30), (44, 29), (40, 31),
           (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (18, 42),
           (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36),
           (-9, 37), (-10, 36)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (1, 52), (1, 51)]
JAPAN = [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
         (141, 41), (142, 43), (144, 44), (142, 42), (140, 38), (137, 35),
         (133, 34), (131, 33)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (120, -34), (126, -32),
             (130, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
             (113, -22)]
NEW_ZEALAND = [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
               (175, -40), (172, -43), (168, -46)]
INDONESIA = [(95, 5), (100, 0), (105, -6), (110, -7), (115, -8), (120, -9),
             (125, -9), (130, -4), (135, -3), (140, -8), (135, -8),
             (130, -5), (125, -2), (120, -1), (115, -3), (110, -6),
             (105, -5), (100, -2), (95, 5)]


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    # Crop the poles: latitude 80..-60 fills the strip, so the
    # continents read instead of sitting as a thin band.
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (80.0 - lat) / 140.0 * h
    return (x, y)


def draw_map(draw, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    for poly in (NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA,
                 EURASIA, BRITAIN, JAPAN, AUSTRALIA, NEW_ZEALAND,
                 INDONESIA):
        pts = [lonlat_to_xy(lon, lat, x0, y0, w, h) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # markers: (lon, lat, label, label offset, anchor)
    marks = [
        (114, 22, "SHENZHEN", (-4, -26), "top"),
        (4, 52, "THE HAGUE", (-78, -8), "left"),
        (31, 50, "KYIV", (8, -22), "top"),
        (56, 27, "GULF", (8, 2), "right"),
        (34, 31, "GAZA", (8, 8), "right"),
        (-77, 39, "WASHINGTON", (-8, 16), "bottom"),
        (139, 36, "TOKYO", (8, -8), "right"),
        (149, -35, "CANBERRA", (-52, 6), "bottom"),
    ]
    fnt = font(SANS_B, 11)
    for lon, lat, label, off, _anchor in marks:
        mx, my = lonlat_to_xy(lon, lat, x0, y0, w, h)
        draw.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(255, 255, 255))
        lx, ly = mx + off[0], my + off[1]
        text_halo(draw, (lx, ly), label, fnt, INK)


# ---------------------------------------------------------------- grid
GRID = [
    ("EUROPE", "EU proposes \u20ac45bn Ukraine loan for 2027"),
    ("EUROPE", "Kyiv downs 120+ drones overnight; Kerch strikes go on"),
    ("EUROPE", "UN: 372+ civilians killed in Ukraine during October"),
    ("EUROPE", "Germany & Norway fund new air-defence package for Kyiv"),
    ("EUROPE", "Merz ties EU budget to all members funding Ukraine"),
    ("EUROPE", "Coalition of the Willing meets in Berlin on guarantees"),
    ("EUROPE", "UK pledges \u00a3240m in missiles for Ukraine's air defence"),
    ("EUROPE", "EU plans \u20ac14.4bn drone and ammo buys for Ukraine in 2027"),
    ("MIDEAST", "Iran hits US base in Kuwait and sites in Bahrain again"),
    ("MIDEAST", "US jets strike missile site on Iran's Qeshm Island"),
    ("MIDEAST", "ADNOC tanker hit in Hormuz Strait: 1 missing, 11 hurt"),
    ("MIDEAST", "Israeli troops enter central Gaza after evacuation order"),
    ("MIDEAST", "Saudi Arabia: danger passes in three southern cities"),
    ("MIDEAST", "US forces in Gulf up to 60,000 troops, 3 carriers"),
    ("MIDEAST", "War-risk cover hits $64m per tanker transit"),
    ("MIDEAST", "Iraq jails 6 French nationals for life for joining ISIL"),
    ("ASIA", "India & Japan review defence ties in Tokyo"),
    ("ASIA", "Cyclone Akvan nears India's coast, Machilipatnam to Puri"),
    ("ASIA", "Australia sanctions Israeli settlers over West Bank"),
    ("ASIA", "APEC Shenzhen, day 2: leaders' meetings continue"),
    ("ASIA", "Trump and Putin hold bilateral talks today, first since Alaska"),
    ("ASIA", "Kremlin: Putin\u2013Trump may discuss Kostiantynivka mission"),
    ("ASIA", "New START expired in Feb; no US\u2013Russia nuclear limits"),
    ("ASIA", "Rockstar promotes GTA VI in China, unapproved for sale"),
    ("AMERICAS", "Fed minutes: most officials expect further rate rises"),
    ("AMERICAS", "US proposes stricter work-based green-card rules"),
    ("AMERICAS", "Hegseth makes first Venezuela visit since Maduro arrest"),
    ("AMERICAS", "Senators warn AI cyber threats outpace US defences"),
    ("AMERICAS", "NSA probes outage of its internal comms network"),
    ("AMERICAS", "Deutsche Bank handled $582m in Epstein-linked deals (FT)"),
    ("AMERICAS", "Trump: reports of Washington bombing plot taken seriously"),
    ("AMERICAS", "Peltola's Alaska win seals Democrats' 56\u201344 Senate edge"),
    ("AFRICA", "Sudan: UN confirms 2,230+ civilian deaths, 1,630 by drone"),
    ("AFRICA", "Somalia accuses UAE of building secret military base"),
    ("AFRICA", "South Africa's Gaza genocide case still pending at ICJ"),
    ("AFRICA", "The Gambia brought Rohingya case for 57 Muslim states"),
    ("WORLD", "ICJ rules today: did Myanmar commit genocide of Rohingya?"),
    ("SCIENCE", "Voyager 1 crosses one light-day from Earth"),
    ("TECH", "Nvidia chief Kress promises early raises, more shares"),
    ("MARKETS", "Take-Two shares jump 6.5% as GTA VI scores 99"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    f_mast = font(SERIF, 62)
    d.text((W // 2, 4), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    d.rectangle([12, 72, W - 12, 76], fill=INK)
    # date ribbon
    d.rectangle([12, 80, W - 12, 104], fill=RED)
    f_date = font(SANS_B, 19)
    d.text((W // 2, 82), "THURSDAY  19  NOVEMBER  2026", font=f_date,
           fill=(255, 255, 255), anchor="ma")
    f_sub = font(SANS_B, 11)
    d.text((12, 108), "42 STORIES  \u2022  SIX CONTINENTS  \u2022  ONE FRONT PAGE",
           font=f_sub, fill=GREY)
    d.text((W - 12, 108), "THE DAY'S NEWS, IN ONE IMAGE", font=f_sub,
           fill=GREY, anchor="ra")

    # ---- lead row
    ly, lh = 126, 104
    d.rectangle([12, ly, 506, ly + lh], outline=INK, width=2)
    d.rectangle([518, ly, W - 12, ly + lh], outline=INK, width=2)
    f_kick = font(SANS_B, 11)
    f_lead = font(SERIF, 27)
    f_sub2 = font(SANS, 13)

    # lead 1: trilateral
    d.text((24, ly + 5), "DIPLOMACY  \u2022  SHENZHEN", font=f_kick, fill=RED)
    d.text((24, ly + 21), "XI, TRUMP & PUTIN", font=f_lead, fill=INK)
    d.text((24, ly + 51), "MEET TODAY", font=f_lead, fill=INK)
    d.text((24, ly + 84),
           "First three-way summit: nuclear arms, Iran, Ukraine on the table.",
           font=f_sub2, fill=INK)
    # three leader discs, top right
    for i, (letter, col) in enumerate((("X", RED), ("T", BLUE), ("P", (34, 120, 60)))):
        cx = 420 + i * 30
        cy = ly + 20
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=col,
                  outline=(255, 255, 255), width=2)
        d.text((cx, cy - 10), letter, font=font(SANS_B, 16),
               fill=(255, 255, 255), anchor="ma")

    # lead 2: GTA VI
    d.text((530, ly + 5), "CULTURE  \u2022  GAMES", font=f_kick, fill=RED)
    d.text((530, ly + 21), "GTA VI GOES LIVE", font=f_lead, fill=INK)
    d.text((530, ly + 51), "WORLDWIDE TODAY", font=f_lead, fill=INK)
    d.text((530, ly + 84),
           "Midnight rollout in NZ; Metacritic 99, 17m pre-sold.",
           font=f_sub2, fill=INK)
    d.rounded_rectangle([880, ly + 12, 1000, ly + 92], radius=8, fill=BLUE)
    d.text((940, ly + 14), "99", font=font(SANS_B, 40),
           fill=(255, 255, 255), anchor="ma")
    d.text((940, ly + 58), "METACRITIC", font=font(SANS_B, 10),
           fill=(255, 255, 255), anchor="ma")

    # ---- map strip
    my, mh = 238, 98
    d.text((12, my), "THE WORLD TODAY \u2014 EIGHT FLASHPOINTS",
           font=font(SANS_B, 12), fill=INK)
    d.text((W - 12, my), "SHENZHEN \u2022 THE HAGUE \u2022 KYIV \u2022 GULF",
           font=font(SANS, 11), fill=GREY, anchor="ra")
    draw_map(d, 12, my + 16, W - 24, mh - 16)

    # ---- grid of 40 stories
    gy = 344
    d.rectangle([12, gy - 4, W - 12, gy - 4], fill=INK)
    cols, rows = 5, 8
    cw = (W - 24 - (cols - 1) * 6) // cols
    rh = 37
    f_tag = font(SANS_B, 9)
    for idx, (tag, head) in enumerate(GRID):
        r, c = divmod(idx, cols)
        x = 12 + c * (cw + 6)
        y = gy + r * rh
        if c > 0:
            d.line([x - 3, y + 2, x - 3, y + rh - 4], fill=(210, 200, 175))
        d.text((x, y), tag, font=f_tag, fill=RED)
        f_head = font(SANS_B, 12)
        lines = wrap(d, head, f_head, cw)
        if len(lines) > 2:
            f_head = font(SANS_B, 11)
            lines = wrap(d, head, f_head, cw)[:2]
        yy = y + 11
        for ln in lines[:2]:
            d.text((x, yy), ln, font=f_head, fill=INK)
            yy += 13

    # ---- footer
    fy = gy + rows * rh + 6
    d.rectangle([12, fy, W - 12, fy], fill=INK)
    d.text((W // 2, fy + 5),
           "All 42 stories were reported on Thursday 19 November 2026.",
           font=font(SANS_B, 12), fill=INK, anchor="ma")
    d.text((W // 2, fy + 21),
           "make.fun  \u2022  news-image-20261119  \u2022  The World \u2014 one day, one front page.",
           font=font(SANS, 10), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
