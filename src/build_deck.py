"""Pick a Card: a full 54-card deck (52 + 2 Jokers) at true size, in four shuffled layouts.

Writes, for each shuffle A-D:
  deck/Pick_a_Card_Poster_X.pdf  - one 24 x 36 in. poster (print shop)
  deck/Pick_a_Card_Home_X.pdf    - nine US Letter sheets that tape into a 3 x 3 board
"""
import os
import random
import sys

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cards import draw_card, full_deck, CARD_W, CARD_H, DK, OR, star

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "deck")
GR = HexColor("#BDBDBD")
SHUFFLES = {"A": 1101, "B": 2202, "C": 3303, "D": 4404}


def shuffled(seed):
    d = full_deck()
    random.Random(seed).shuffle(d)
    return d


def scale_bar(c, x, y, size=6.5):
    c.setStrokeColor(DK); c.setLineWidth(1)
    c.line(x, y, x + inch, y)
    for i in range(5):
        c.line(x + i * inch / 4, y, x + i * inch / 4, y + (4 if i % 2 == 0 else 2.5))
    c.setFillColor(DK); c.setFont("Helvetica", size)
    c.drawString(x + inch + 6, y, "= 1 inch. Print at 100% / Actual Size. Each card should measure 2.5 x 3.5 in.")


# ---------------- poster, 24 x 36 in. ----------------
def poster(letter, seed):
    W, H = 24 * inch, 36 * inch
    path = os.path.join(OUT, f"Pick_a_Card_Poster_{letter}.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(f"LOCKED - Pick a Card - Poster, Shuffle {letter}")

    # title band
    c.setFillColor(DK); c.rect(0, H - 5.4 * inch, W, 5.4 * inch, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 120)
    c.drawString(1.125 * inch, H - 2.55 * inch, "PICK A CARD")
    c.setFillColor(OR); c.setFont("Helvetica-Bold", 30)
    c.drawRightString(W - 1.125 * inch, H - 1.25 * inch, f"SHUFFLE {letter}")
    c.setFillColor(HexColor("#AAAAAA")); c.setFont("Helvetica-Bold", 20)
    c.drawRightString(W - 1.125 * inch, H - 1.7 * inch, "LOCKED")
    rules = [
        "1.  Someone flips a card from a real deck and calls it out: \"seven of hearts.\"",
        "2.  Everyone fires one shot at that card. Closest to the white center dot wins the round.",
        "3.  Miss the card and you are out for that round. First to 5 round wins takes the game.",
        "4.  Flip a Joker and everyone shoots a Joker.",
    ]
    c.setFillColor(white); c.setFont("Helvetica", 22)
    for i, r in enumerate(rules):
        c.drawString(1.125 * inch, H - 3.35 * inch - i * 0.42 * inch, r)

    # card grid: 8 x 7 = 56 slots, two in the middle row are the no-score tile
    cols, rows = 8, 7
    gx, gy = 0.25 * inch, 0.3 * inch
    gw = cols * CARD_W + (cols - 1) * gx
    x0 = (W - gw) / 2
    top = H - 5.85 * inch
    tile = {(3, 3), (3, 4)}
    deck = iter(shuffled(seed))
    for r in range(rows):
        for k in range(cols):
            x = x0 + k * (CARD_W + gx)
            y = top - (r + 1) * CARD_H - r * gy
            if (r, k) in tile:
                if k == 3:
                    tw = 2 * CARD_W + gx
                    c.setFillColor(DK); c.roundRect(x, y, tw, CARD_H, 0.13 * inch, stroke=0, fill=1)
                    star(c, x + tw / 2, y + CARD_H * 0.62, 1.1 * inch, OR)
                    c.setFillColor(white); c.setFont("Helvetica-Bold", 30)
                    c.drawCentredString(x + tw / 2, y + 0.95 * inch, "PICK A CARD")
                    c.setFont("Helvetica-Bold", 14); c.setFillColor(HexColor("#AAAAAA"))
                    c.drawCentredString(x + tw / 2, y + 0.55 * inch, f"SHUFFLE {letter}  ·  NO SCORE")
                continue
            rank, suit = next(deck)
            draw_card(c, x, y, rank, suit)

    # scoreboard
    sb_top = top - rows * CARD_H - (rows - 1) * gy - 0.45 * inch
    c.setFillColor(DK); c.setFont("Helvetica-Bold", 18)
    c.drawString(x0, sb_top, "SCOREBOARD")
    c.setFont("Helvetica", 12); c.setFillColor(HexColor("#666666"))
    c.drawString(x0 + 1.75 * inch, sb_top, "Tally round wins. First to 5.")
    rh = 0.42 * inch
    for half in range(2):
        tx = x0 + half * (gw / 2 + 0.15 * inch)
        tw = gw / 2 - 0.15 * inch
        for i in range(4):
            yy = sb_top - 0.25 * inch - (i + 1) * rh
            c.setStrokeColor(DK); c.setLineWidth(0.8)
            c.rect(tx, yy, tw, rh, stroke=1, fill=0)
            c.line(tx + 3.4 * inch, yy, tx + 3.4 * inch, yy + rh)
            for t in range(1, 5):
                xx = tx + 3.4 * inch + t * (tw - 3.4 * inch) / 5
                c.setStrokeColor(GR); c.line(xx, yy, xx, yy + rh)
            c.setFillColor(HexColor("#999999")); c.setFont("Helvetica", 9)
            c.drawString(tx + 6, yy + rh - 12, "NAME")
    scale_bar(c, x0, 0.55 * inch, 10)
    c.setFillColor(DK); c.setFont("Helvetica-Bold", 10)
    c.drawRightString(x0 + gw, 0.55 * inch, f"LOCKED  ·  PICK A CARD  ·  SHUFFLE {letter}  ·  24 x 36 in.")
    c.showPage(); c.save()


# ---------------- home: nine Letter sheets, 3 x 3 board ----------------
def mini_map(c, x, y, idx):
    s = 0.16 * inch
    for i in range(9):
        r, k = divmod(i, 3)
        c.setFillColor(OR if i == idx else white); c.setStrokeColor(DK); c.setLineWidth(0.6)
        c.rect(x + k * (s + 2), y - (r + 1) * (s + 2), s, s, stroke=1, fill=1)


def home(letter, seed):
    W, H = 8.5 * inch, 11 * inch
    path = os.path.join(OUT, f"Pick_a_Card_Home_{letter}.pdf")
    c = canvas.Canvas(path, pagesize=(W, H))
    c.setTitle(f"LOCKED - Pick a Card - Home sheets, Shuffle {letter}")
    deck = shuffled(seed)
    gx, gy = 0.15 * inch, 0.3 * inch
    gw = 3 * CARD_W + 2 * gx
    x0 = (W - gw) / 2
    top = 9.55 * inch
    for sheet in range(9):
        # header
        c.setFillColor(OR); c.rect(x0, 10.2 * inch, 0.1 * inch, 0.42 * inch, stroke=0, fill=1)
        c.setFillColor(DK); c.setFont("Helvetica-Bold", 18)
        c.drawString(x0 + 0.22 * inch, 10.4 * inch, "PICK A CARD")
        c.setFont("Helvetica", 8.5)
        c.drawString(x0 + 0.22 * inch, 10.22 * inch, f"Shuffle {letter}  ·  Sheet {sheet + 1} of 9  ·  Tape into a 3 x 3 board (about 25 x 32 in.) or hang the sheets in a row.")
        mini_map(c, x0 + gw - 0.55 * inch, 10.68 * inch, sheet)
        c.setFont("Helvetica-Bold", 7); c.drawRightString(x0 + gw - 0.6 * inch, 10.5 * inch, f"SHEET {sheet + 1}")
        for i in range(6):
            r, k = divmod(i, 3)
            rank, suit = deck[sheet * 6 + i]
            draw_card(c, x0 + k * (CARD_W + gx), top - (r + 1) * CARD_H - r * gy, rank, suit)
        c.setFillColor(DK); c.setFont("Helvetica", 8)
        c.drawString(x0, 1.75 * inch, "Rules: flip a card from a real deck and call it. Everyone fires one shot at that card. Closest to the white center dot")
        c.drawString(x0, 1.6 * inch, "wins the round. Miss the card and you are out for that round. First to 5 round wins takes the game. Joker = shoot a Joker.")
        scale_bar(c, x0, 0.6 * inch)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawRightString(x0 + gw, 0.6 * inch, f"LOCKED  ·  SHUFFLE {letter}  ·  {sheet + 1}/9")
        c.showPage()
    c.save()


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for L, seed in SHUFFLES.items():
        poster(L, seed)
        home(L, seed)
    print("deck written:", sorted(os.listdir(OUT)))
