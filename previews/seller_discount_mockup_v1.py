"""Mock-up v1: the seller's discount where it is missing now (2026-11-02).
A = "Sell to them" (selling into another farm's standing buy order): amount + discount in one box.
B = "Request an invoice": the buyer's form has no discount any more; the seller sets it when approving.
python -I seller_discount_mockup_v1.py <outDir>"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

F = "C:/Windows/Fonts/"
def font(sz, bold=False):
    return ImageFont.truetype(F + ("segoeuib.ttf" if bold else "segoeui.ttf"), sz)

W, H = 2000, 1125
BG = (36, 37, 35); CARD = (28, 29, 27); BAR = (8, 8, 8); TILE = (40, 44, 34)
GREEN = (134, 177, 17); GREEN_L = (166, 200, 60); TINT = (50, 60, 28)
WHITE = (235, 235, 235); GREY = (170, 170, 165); DIM = (110, 112, 105); LINE = (62, 64, 58); EDGE = (46, 48, 43)
ORANGE = (230, 170, 60)

def spaced(d, xy, text, fnt, fill, spacing=3):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill, anchor="lm")
        x += d.textlength(c, font=fnt) + spacing

def drop(d, cx, cy, c, s=1.0):
    d.polygon([(cx, cy - 16 * s), (cx - 11 * s, cy + 2 * s), (cx + 11 * s, cy + 2 * s)], fill=c)
    d.ellipse([cx - 11 * s, cy - 8 * s, cx + 11 * s, cy + 14 * s], fill=c)

def heap(d, cx, cy, c):
    d.pieslice([cx - 17, cy - 8, cx + 17, cy + 26], 180, 360, fill=c)

def dialog(d, x0, y0, x1, y1, title, sub, icon=drop):
    d.rounded_rectangle([x0, y0, x1, y1], 10, fill=BG, outline=EDGE, width=2)
    d.rounded_rectangle([x0 + 20, y0 + 20, x0 + 80, y0 + 80], 8, fill=GREEN)
    icon(d, x0 + 50, y0 + 48, WHITE)
    spaced(d, (x0 + 100, y0 + 34), "UWM CO-OP", font(17, True), GREEN_L, 1)
    d.text((x0 + 100, y0 + 64), title, font=font(30, True), fill=WHITE, anchor="lm")
    if sub:
        d.text((x1 - 24, y0 + 50), sub, font=font(18), fill=GREY, anchor="rm")
    d.line([x0 + 20, y0 + 100, x1 - 20, y0 + 100], fill=LINE, width=2)

def label(d, x, y, text):
    spaced(d, (x, y), text.upper(), font(15, True), GREY, 2)

def field(d, x0, y, w, text, active=True, new=False, hint=None):
    col = GREEN if new else (WHITE if active else LINE)
    d.rounded_rectangle([x0, y, x0 + w, y + 46], 6, fill=CARD if active else BG, outline=col, width=2)
    d.text((x0 + w / 2, y + 23), text, font=font(22, active), fill=WHITE if active else DIM, anchor="mm")
    if active:
        d.text((x0 + w - 18, y + 23), "✎", font=ImageFont.truetype(F + "seguisym.ttf", 16), fill=GREY, anchor="mm")
    if new:
        d.rounded_rectangle([x0 + w - 56, y - 14, x0 + w + 8, y + 10], 12, fill=GREEN)
        d.text((x0 + w - 24, y - 2), "NEW", font=font(14, True), fill=BAR, anchor="mm")
    if hint:
        d.text((x0, y + 64), hint, font=font(16), fill=GREY, anchor="lm")

def row(d, x0, x1, y, left, right, col=WHITE, bold=False):
    d.text((x0, y), left, font=font(20, bold), fill=GREY if not bold else WHITE, anchor="lm")
    d.text((x1, y), right, font=font(22 if bold else 20, True), fill=col, anchor="rm")

def buttons(d, x1, y, items):
    x = x1
    for key, text in reversed(items):
        f = font(22, True)
        tw = d.textlength(text, font=f)
        d.text((x, y), text, font=f, fill=WHITE, anchor="rm")
        x -= tw + 14
        kw = d.textlength(key, font=font(20, True)) + 26
        d.rounded_rectangle([x - kw, y - 20, x, y + 20], 5, fill=TINT)
        d.text((x - kw / 2, y), key, font=font(20, True), fill=GREEN_L, anchor="mm")
        x -= kw + 34

def caption(d, text):
    d.rectangle([0, 0, W, 64], fill=BAR)
    d.text((40, 32), text, font=font(24, True), fill=GREEN_L, anchor="lm")

def sell_to_them(path):
    img = Image.new("RGB", (W, H), (22, 23, 21)); d = ImageDraw.Draw(img)
    caption(d, "A  -  SELL TO THEM: you sell into Farm B's standing buy order")
    x0, y0, x1, y1 = 520, 140, 1480, 1000
    dialog(d, x0, y0, x1, y1, "Sell to a buy order", "SO-007  -  Farm B")
    # the order
    d.rounded_rectangle([x0 + 30, y0 + 125, x1 - 30, y0 + 215], 8, fill=CARD, outline=EDGE, width=2)
    d.rounded_rectangle([x0 + 48, y0 + 140, x0 + 108, y0 + 200], 8, fill=TILE)
    drop(d, x0 + 78, y0 + 168, GREEN_L)
    d.text((x0 + 128, y0 + 152), "Slurry  -  Farm B wants 500,000 l", font=font(24, True), fill=WHITE, anchor="lm")
    d.text((x0 + 128, y0 + 186), "Buyer's money is held for the whole order  -  You have 1,857,979 l", font=font(17), fill=GREY, anchor="lm")
    d.text((x1 - 50, y0 + 170), "$ 30 / 1,000 l", font=font(24, True), fill=GREEN_L, anchor="rm")
    # inputs
    fy = y0 + 270
    label(d, x0 + 30, fy, "Amount in liters")
    field(d, x0 + 30, fy + 22, 430, "200000")
    label(d, x0 + 500, fy, "Discount %")
    field(d, x0 + 500, fy + 22, 430, "10", new=True, hint="Optional. Leave empty for the full price.")
    # totals
    ty = y0 + 440
    d.rounded_rectangle([x0 + 30, ty, x1 - 30, ty + 300], 8, fill=CARD, outline=EDGE, width=2)
    row(d, x0 + 60, x1 - 60, ty + 40, "200,000 l at $ 30 / 1,000 l", "$ 6,000")
    row(d, x0 + 60, x1 - 60, ty + 85, "Your discount 10 %", "- $ 600", ORANGE)
    d.line([x0 + 60, ty + 120, x1 - 60, ty + 120], fill=LINE, width=2)
    label(d, x0 + 60, ty + 160, "You receive")
    d.text((x1 - 60, ty + 165), "$ 5,400", font=font(48, True), fill=GREEN_L, anchor="rm")
    d.text((x0 + 60, ty + 240), "Farm B gets the $ 600 back from the money held for the order.", font=font(18), fill=GREY, anchor="lm")
    d.text((x0 + 60, ty + 268), "Farm B is told: \"... sold you 200,000 l Slurry, 10 % off\".", font=font(18), fill=GREY, anchor="lm")
    d.rectangle([x0, y1 - 70, x1, y1], fill=BAR)
    buttons(d, x1 - 30, y1 - 35, [("ENTER", "SELL"), ("ESC", "CANCEL")])
    img.save(path)

def request(path):
    img = Image.new("RGB", (W, H), (22, 23, 21)); d = ImageDraw.Draw(img)
    caption(d, "B  -  REQUEST AN INVOICE: the buyer asks, the SELLER sets the discount when approving")
    # left: the buyer's form line (discount box off)
    x0, y0, x1, y1 = 40, 140, 960, 760
    dialog(d, x0, y0, x1, y1, "Request an invoice", "Buyer: Farm B", heap)
    spaced(d, (x0 + 30, y0 + 135), "1  THE BUYER FILLS IN THE FORM", font(17, True), GREEN_L, 2)
    fy = y0 + 200
    for i, (name, val, on) in enumerate([("Price per 1,000 l", "32", True), ("Amount in liters", "100000", True),
                                        ("Discount %", "Seller sets it", False), ("Repeat", "Once", True)]):
        cx = x0 + 30 + (i % 2) * 450
        cy = fy + (i // 2) * 130
        label(d, cx, cy, name)
        field(d, cx, cy + 22, 410, val, active=on)
    d.text((x0 + 30, fy + 300), "The discount box is greyed out: the buyer can't give themselves a discount.", font=font(18), fill=GREY, anchor="lm")
    d.rectangle([x0, y1 - 70, x1, y1], fill=BAR)
    buttons(d, x1 - 30, y1 - 35, [("ENTER", "SEND REQUEST"), ("ESC", "CANCEL")])

    # right: the seller approves, with the discount
    x0, y0, x1, y1 = 1000, 140, 1960, 1000
    dialog(d, x0, y0, x1, y1, "Approve a request", "From Farm B", heap)
    spaced(d, (x0 + 30, y0 + 135), "2  THE SELLER APPROVES (YOU)", font(17, True), GREEN_L, 2)
    d.rounded_rectangle([x0 + 30, y0 + 165, x1 - 30, y0 + 255], 8, fill=CARD, outline=EDGE, width=2)
    d.rounded_rectangle([x0 + 48, y0 + 180, x0 + 108, y0 + 240], 8, fill=TILE)
    heap(d, x0 + 78, y0 + 205, GREEN_L)
    d.text((x0 + 128, y0 + 192), "Manure  -  100,000 l, once", font=font(24, True), fill=WHITE, anchor="lm")
    d.text((x0 + 128, y0 + 226), "Pickup: Community Depot  -  Manure pit", font=font(17), fill=GREY, anchor="lm")
    d.text((x1 - 50, y0 + 210), "$ 32 / 1,000 l", font=font(24, True), fill=GREEN_L, anchor="rm")
    fy = y0 + 300
    label(d, x0 + 30, fy, "Discount %")
    field(d, x0 + 30, fy + 22, 430, "5", new=True, hint="Optional. Leave empty for the full price.")
    ty = y0 + 440
    d.rounded_rectangle([x0 + 30, ty, x1 - 30, ty + 250], 8, fill=CARD, outline=EDGE, width=2)
    row(d, x0 + 60, x1 - 60, ty + 40, "100,000 l at $ 32 / 1,000 l", "$ 3,200")
    row(d, x0 + 60, x1 - 60, ty + 85, "Your discount 5 %", "- $ 160", ORANGE)
    d.line([x0 + 60, ty + 120, x1 - 60, ty + 120], fill=LINE, width=2)
    label(d, x0 + 60, ty + 160, "Farm B pays you")
    d.text((x1 - 60, ty + 165), "$ 3,040", font=font(48, True), fill=GREEN_L, anchor="rm")
    d.text((x0 + 30, ty + 290), "Farm B is told the request was approved, with \"5 % off\".", font=font(18), fill=GREY, anchor="lm")
    d.rectangle([x0, y1 - 70, x1, y1], fill=BAR)
    buttons(d, x1 - 30, y1 - 35, [("ENTER", "APPROVE"), ("C", "DECLINE"), ("ESC", "BACK")])
    img.save(path)

if __name__ == "__main__":
    out = sys.argv[1]
    sell_to_them(os.path.join(out, "seller_discount_v1_sell_to_them.png"))
    request(os.path.join(out, "seller_discount_v1_request.png"))
