# v6 (2026-11-03): v5 with sacks or crates on the pallet instead of the big bag (middle) and growing corn (right) instead of slurry and manure
"""Draft mod icon for Utilities & Waste Management: lightning bolt, slurry puddle with fumes, manure heap on a dark tile."""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

out = sys.argv[1]
S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# tile with a soft vertical gradient
tile = Image.new("RGBA", (S, S))
td = ImageDraw.Draw(tile)
for y in range(S):
    t = y / S
    td.line([(0, y), (S, y)], fill=(int(28 + 14 * t), int(40 + 10 * t), int(36 + 6 * t), 255))
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([8, 8, S - 8, S - 8], radius=56, fill=255)
img.paste(tile, (0, 0), mask)
d = ImageDraw.Draw(img)


def glow(shape_draw, color, blur=10):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    shape_draw(ImageDraw.Draw(layer), color)
    halo = layer.filter(ImageFilter.GaussianBlur(blur))
    img.alpha_composite(halo)
    img.alpha_composite(layer)


# lightning bolt (left)
def bolt(dr, c):
    dr.polygon([(150, 70), (82, 225), (138, 225), (104, 340), (196, 180), (140, 180), (176, 70)], fill=c)
glow(bolt, (255, 205, 40, 255))

# wooden pallet with a big bag on it (middle)
import math
def pallet(dr, c):
    dr.rectangle([196, 300, 330, 312], fill=c)                        # top boards
    for x in (198, 255, 312):                                         # blocks
        dr.rectangle([x, 312, x + 18, 326], fill=c)
    dr.rectangle([196, 326, 330, 336], fill=c)                        # bottom boards
glow(pallet, (176, 128, 70, 255), blur=6)
for x in (230, 263, 296):                                             # board gaps
    d.line([(x, 300), (x, 312)], fill=(120, 84, 44, 255), width=3)
# load on the pallet (v6): LOAD = "sacks" (burlap grain sacks, 3 + 2) or "crates" (wooden crates of potatoes)
LOAD = sys.argv[2] if len(sys.argv) > 2 else "sacks"
if LOAD == "sacks":
    def sacks(dr, c):
        for x0, y0 in [(200, 252), (243, 252), (286, 252), (221, 206), (264, 206)]:
            dr.rounded_rectangle([x0, y0, x0 + 42, y0 + 50], radius=16, fill=c)
    glow(sacks, (205, 170, 115, 255), blur=6)
    for x0, y0 in [(200, 252), (243, 252), (286, 252), (221, 206), (264, 206)]:
        d.rounded_rectangle([x0, y0, x0 + 42, y0 + 50], radius=16, outline=(140, 108, 66, 255), width=3)
        d.line([(x0 + 10, y0 + 8), (x0 + 32, y0 + 8)], fill=(140, 108, 66, 255), width=3)      # tied top
        d.line([(x0 + 8, y0 + 30), (x0 + 34, y0 + 30)], fill=(185, 150, 98, 255), width=2)     # weave
else:
    def crates(dr, c):
        for x0, y0 in [(202, 248), (266, 248), (234, 194)]:
            dr.rectangle([x0, y0, x0 + 60, y0 + 52], fill=c)
    glow(crates, (196, 150, 90, 255), blur=6)
    for x0, y0 in [(202, 248), (266, 248), (234, 194)]:
        for x, y in [(x0 + 12, y0 - 4), (x0 + 28, y0 - 7), (x0 + 44, y0 - 4), (x0 + 20, y0 - 1), (x0 + 38, y0 - 1)]:
            d.ellipse([x - 9, y - 7, x + 9, y + 7], fill=(196, 160, 100, 255), outline=(140, 105, 60, 255))  # potatoes
        d.rectangle([x0, y0, x0 + 60, y0 + 52], fill=(196, 150, 90, 255), outline=(120, 84, 44, 255), width=3)
        for y in (y0 + 17, y0 + 34):
            d.line([(x0, y), (x0 + 60, y)], fill=(120, 84, 44, 255), width=3)

# corn growing (right): three stalks with leaves and a cob
def corn(dr, c):
    for x0, top in [(372, 150), (412, 128), (450, 160)]:
        dr.line([(x0, 336), (x0, top)], fill=c, width=8)
        for i, y in enumerate(range(top + 40, 320, 42)):
            s = 1 if (i + x0 // 10) % 2 == 0 else -1
            dr.line([(x0, y), (x0 + s * 22, y - 18), (x0 + s * 34, y - 6)], fill=c, width=7, joint="curve")
        dr.line([(x0 - 8, top - 2), (x0, top - 22), (x0 + 8, top - 2)], fill=(200, 180, 90, 255), width=4)  # tassel
glow(corn, (110, 180, 60, 255), blur=8)
def cob(dr, c):
    dr.ellipse([400, 196, 426, 252], fill=c)
glow(cob, (250, 200, 50, 255), blur=6)
for y in range(204, 248, 8):
    d.line([(404, y), (422, y)], fill=(215, 160, 30, 255), width=2)
d.polygon([(398, 252), (413, 200), (404, 256)], fill=(90, 160, 50, 255))   # husk
d.polygon([(428, 252), (413, 200), (422, 256)], fill=(90, 160, 50, 255))
d.rectangle([340, 334, 476, 342], fill=(88, 62, 36, 255))             # soil

# title
font = ImageFont.truetype("arialbd.ttf", 62)
small = ImageFont.truetype("arialbd.ttf", 38)
for text, f, y in [("PLAYER", font, 362), ("TRADING+", font, 430)]:
    w = d.textlength(text, font=f)
    d.text(((S - w) / 2, y), text, font=f, fill=(245, 245, 240, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))

img.save(out)
