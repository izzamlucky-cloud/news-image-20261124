#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261124.
Design: clean newspaper front page, 1024x1024, text-first so the
GLM judge can read the day and each story from the image alone.
All facts are from reporting on 24 Nov 2026 (Just Security Early
Edition, The Global Eye, Daily Edition, Horizon). No speculation.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

W, H = 1024, 1024
BG = (247, 243, 232)
INK = (18, 24, 38)
NAVY = (16, 42, 90)
RED = (178, 34, 34)
TEAL = (14, 110, 110)
GOLD = (180, 130, 20)
GREY = (90, 95, 105)
CARD = (255, 255, 255)
LINE = (200, 195, 180)

def font(name, size):
    paths = {
        "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    }
    return ImageFont.truetype(paths[name], size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, fnt, color, max_w, lh):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---- header ----
d.rectangle([0, 0, W, 168], fill=NAVY)
d.text((32, 22), "THE WORLD  •  IN ONE DAY", font=font("sans_b", 26), fill=(255, 210, 90))
d.text((32, 56), "TUESDAY", font=font("serif_b", 62), fill=(255, 255, 255))
d.text((32, 122), "24 NOVEMBER 2026", font=font("sans_b", 40), fill=(255, 255, 255))
d.text((700, 30), "8 STORIES", font=font("sans_b", 24), fill=(255, 210, 90))
d.text((700, 62), "WAR  •  CLIMATE", font=font("sans", 22), fill=(220, 225, 235))
d.text((700, 92), "TECH  •  WORLD", font=font("sans", 22), fill=(220, 225, 235))
d.text((700, 122), "24 NOV 2026", font=font("sans_b", 22), fill=(255, 255, 255))

# ---- lead: COP31 ----
x0, y0, x1, y1 = 24, 188, 1000, 392
d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE, width=2)
# sun / earth icon
d.ellipse([880, 208, 972, 300], fill=(255, 190, 60), outline=GOLD, width=3)
d.ellipse([905, 233, 947, 275], fill=(255, 235, 160))
d.text((48, 200), "CLIMATE  •  ANTALYA, TURKEY", font=font("sans_b", 20), fill=RED)
y = draw_wrapped(d, 48, 228, "COP31 talks collapse", font("serif_b", 40), INK, 800, 48)
y = draw_wrapped(d, 48, y+6, "More than 90 nations reject the draft deal after almost 50 hours of overtime. The text never named fossil fuels.", font("sans", 23), (40, 45, 60), 800, 30)
d.text((48, 352), "No deal  •  Summit ends without agreement", font=font("sans_b", 21), fill=TEAL)

# ---- row 2: two cards ----
def card(x0, y0, x1, y1, tag, tagcolor, headline, body, foot):
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD, outline=LINE, width=2)
    d.text((x0+18, y0+14), tag, font=font("sans_b", 19), fill=tagcolor)
    y = draw_wrapped(d, x0+18, y0+44, headline, font("serif_b", 27), INK, x1-x0-36, 34)
    y = draw_wrapped(d, x0+18, y+8, body, font("sans", 20), (40, 45, 60), x1-x0-36, 26)
    d.text((x0+18, y1-32), foot, font=font("sans_b", 18), fill=TEAL)

card(24, 412, 500, 628, "WAR  •  LIBYA", RED,
     "Ukraine says drones sank Russian warship off Libya",
     "Kyiv says seven naval drones sank the corvette Merkury at Benghazi.",
     "Black Sea war reaches the Med")
card(524, 412, 1000, 628, "WAR  •  GAZA", RED,
     "Israeli strikes kill Hamas security chief in Gaza",
     "Naeem Abu Nahel and six others killed, medics and police say.",
     "Also: UN aid worker killed")

# ---- row 3: two cards ----
card(24, 648, 500, 864, "WAR  •  UKRAINE", RED,
     "Zaporizhzhia hit: 2 killed, 40 wounded",
     "A Russian attack strikes an apartment building. Four children hurt.",
     "Zaporizhzhia, Ukraine")
card(524, 648, 1000, 864, "SECURITY  •  NATO", NAVY,
     "NATO vows to defend space",
     "Chief Mark Rutte speaks out after reports of a Russian nuclear satellite.",
     "25 airspace violations in 2026")

# ---- bottom strip ----
d.rounded_rectangle([24, 884, 1000, 992], radius=14, fill=NAVY, outline=NAVY)
d.text((40, 894), "ALSO TODAY", font=font("sans_b", 20), fill=(255, 210, 90))
draw_wrapped(d, 40, 922, "Nvidia reinstates Jensen Huang as CEO  •  5.6 quake hits Nepal  •  UN chief calls for AI rules", font("sans", 20), (255, 255, 255), 920, 26)

out = os.path.join(os.path.dirname(__file__), "entry.png")
img.save(out, "PNG", optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
