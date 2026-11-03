# v5 (2026-11-03): v4 with a pallet + big bag (middle) and growing corn (right) instead of slurry and manure
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
def bag(dr, c):
    dr.rounded_rectangle([206, 190, 320, 302], radius=18, fill=c)
glow(bag, (236, 232, 218, 255), blur=8)
d.rounded_rectangle([206, 190, 320, 302], radius=18, outline=(190, 186, 170, 255), width=3)
for x in (220, 306):                                                  # lifting loops
    d.arc([x - 14, 168, x + 14, 204], 180, 360, fill=(70, 120, 200, 255), width=7)
d.rectangle([226, 228, 300, 262], fill=(70, 120, 200, 255))           # label
for i, y in enumerate((236, 246, 254)):
    d.line([(234, y), (292 - i * 12, y)], fill=(235, 240, 250, 255), width=3)

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
