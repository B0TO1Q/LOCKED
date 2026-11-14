"""Playing-card drawing for LOCKED. Original, simple card faces at true poker size (2.5 x 3.5 in)."""
import math
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white

DK = HexColor("#222222")
OR = HexColor("#E8541A")
CARD_W, CARD_H = 2.5 * inch, 3.5 * inch

RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS = ["S", "H", "D", "C"]
SUIT_NAME = {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}
RANK_NAME = {"A": "ace", "J": "jack", "Q": "queen", "K": "king"}


def suit_color(s):
    return OR if s in ("H", "D") else DK


def _fill(c, p, col):
    c.setFillColor(col)
    c.drawPath(p, stroke=0, fill=1)


def spade(c, x, y, s, col=DK):
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * s)
    p.curveTo(x + 0.15 * s, y + 0.25 * s, x + 0.5 * s, y + 0.1 * s, x + 0.45 * s, y - 0.15 * s)
    p.curveTo(x + 0.4 * s, y - 0.36 * s, x + 0.14 * s, y - 0.36 * s, x + 0.04 * s, y - 0.2 * s)
    p.lineTo(x + 0.13 * s, y - 0.5 * s)
    p.lineTo(x - 0.13 * s, y - 0.5 * s)
    p.lineTo(x - 0.04 * s, y - 0.2 * s)
    p.curveTo(x - 0.14 * s, y - 0.36 * s, x - 0.4 * s, y - 0.36 * s, x - 0.45 * s, y - 0.15 * s)
    p.curveTo(x - 0.5 * s, y + 0.1 * s, x - 0.15 * s, y + 0.25 * s, x, y + 0.5 * s)
    p.close()
    _fill(c, p, col)


def heart(c, x, y, s, col=OR):
    p = c.beginPath()
    p.moveTo(x, y - 0.5 * s)
    p.curveTo(x + 0.12 * s, y - 0.3 * s, x + 0.5 * s, y - 0.08 * s, x + 0.48 * s, y + 0.2 * s)
    p.curveTo(x + 0.46 * s, y + 0.52 * s, x + 0.08 * s, y + 0.56 * s, x, y + 0.28 * s)
    p.curveTo(x - 0.08 * s, y + 0.56 * s, x - 0.46 * s, y + 0.52 * s, x - 0.48 * s, y + 0.2 * s)
    p.curveTo(x - 0.5 * s, y - 0.08 * s, x - 0.12 * s, y - 0.3 * s, x, y - 0.5 * s)
    p.close()
    _fill(c, p, col)


def diamond(c, x, y, s, col=OR):
    p = c.beginPath()
    p.moveTo(x, y + 0.5 * s); p.lineTo(x + 0.36 * s, y); p.lineTo(x, y - 0.5 * s); p.lineTo(x - 0.36 * s, y)
    p.close()
    _fill(c, p, col)


def club(c, x, y, s, col=DK):
    c.setFillColor(col)
    r = 0.2 * s
    c.circle(x, y + 0.24 * s, r, stroke=0, fill=1)
    c.circle(x - 0.22 * s, y - 0.06 * s, r, stroke=0, fill=1)
    c.circle(x + 0.22 * s, y - 0.06 * s, r, stroke=0, fill=1)
    c.circle(x, y + 0.02 * s, 0.1 * s, stroke=0, fill=1)
    p = c.beginPath()
    p.moveTo(x - 0.03 * s, y); p.lineTo(x + 0.03 * s, y)
    p.lineTo(x + 0.13 * s, y - 0.5 * s); p.lineTo(x - 0.13 * s, y - 0.5 * s)
    p.close()
    _fill(c, p, col)


def star(c, x, y, s, col=OR):
    p = c.beginPath()
    for i in range(10):
        r = 0.5 * s if i % 2 == 0 else 0.2 * s
        a = math.radians(90 + i * 36)
        (p.moveTo if i == 0 else p.lineTo)(x + r * math.cos(a), y + r * math.sin(a))
    p.close()
    _fill(c, p, col)


PIP = {"S": spade, "H": heart, "D": diamond, "C": club}


def _corner(c, x, y, rank, suit, flip):
    c.saveState()
    c.translate(x, y)
    if flip:
        c.rotate(180)
    col = OR if suit == "J" else suit_color(suit)
    c.setFillColor(col)
    if suit == "J":
        c.setFont("Helvetica-Bold", 13)
        for i, ch in enumerate("JOKER"):
            c.drawCentredString(0, -15 - i * 13, ch)
    else:
        c.setFont("Helvetica-Bold", 30 if rank != "10" else 26)
        c.drawCentredString(0, -30, rank)
        PIP[suit](c, 0, -48, 20, col)
    c.restoreState()


def draw_card(c, x, y, rank, suit):
    """Bottom-left at x,y. suit 'J' with rank '' draws a Joker."""
    w, h = CARD_W, CARD_H
    c.setFillColor(white); c.setStrokeColor(DK); c.setLineWidth(1.2)
    c.roundRect(x, y, w, h, 0.13 * inch, stroke=1, fill=1)
    cx, cy = x + w / 2, y + h / 2
    _corner(c, x + 0.27 * inch, y + h - 0.06 * inch, rank, suit, False)
    _corner(c, x + w - 0.27 * inch, y + 0.06 * inch, rank, suit, True)
    if suit == "J":
        star(c, cx, cy, 1.5 * inch, OR)
        dot = white
    else:
        col = suit_color(suit)
        if rank in ("J", "Q", "K"):
            c.setStrokeColor(col); c.setLineWidth(1.5)
            c.roundRect(x + 0.55 * inch, y + 0.62 * inch, w - 1.1 * inch, h - 1.24 * inch, 0.08 * inch, stroke=1, fill=0)
        PIP[suit](c, cx, cy, 1.25 * inch, col)
        dot = white
    # center aim dot: exact card center
    c.setFillColor(dot); c.circle(cx, cy, 0.075 * inch, stroke=0, fill=1)
    c.setFillColor(DK if suit != "J" else white); c.circle(cx, cy, 0.022 * inch, stroke=0, fill=1)


def full_deck():
    deck = [(r, s) for s in SUITS for r in RANKS]
    deck += [("", "J"), ("", "J")]
    return deck
