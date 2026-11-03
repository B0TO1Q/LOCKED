import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white
import math

W, H = 612, 792
OR = HexColor("#E8541A")
GR = HexColor("#BDBDBD")
LG = HexColor("#E4E4E4")
DK = HexColor("#222222")
CX = W / 2

PAGES = []  # (code, title, fn)


def target(code, title, sub):
    def deco(fn):
        PAGES.append((code, title, sub, fn))
        return fn
    return deco


def header(c, code, title, sub):
    c.setFillColor(OR)
    c.rect(0.5 * inch, 10.25 * inch, 0.12 * inch, 0.45 * inch, stroke=0, fill=1)
    c.setFillColor(DK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.75 * inch, 10.45 * inch, title.upper())
    c.setFont("Helvetica", 9)
    c.drawString(0.75 * inch, 10.27 * inch, sub)
    c.setFont("Helvetica-Bold", 10)
    c.drawRightString(8.0 * inch, 10.45 * inch, code)


def footer(c, code):
    y = 0.85 * inch
    c.setStrokeColor(DK)
    c.setLineWidth(0.5)
    c.setFillColor(DK)
    c.setFont("Helvetica", 7.5)
    fields = [("SHOOTER", 1.6), ("DATE", 1.0), ("DIST", 0.8), ("FIREARM / AMMO", 2.2)]
    x = 0.5 * inch
    for name, w in fields:
        c.drawString(x, y, name)
        tw = c.stringWidth(name, "Helvetica", 7.5) + 3
        c.line(x + tw, y - 1, x + w * inch, y - 1)
        x += w * inch + 0.15 * inch
    # scale bar
    bx, by = 0.5 * inch, 0.45 * inch
    c.setLineWidth(1)
    c.line(bx, by, bx + inch, by)
    for i in range(5):
        h = 4 if i % 2 == 0 else 2.5
        c.line(bx + i * inch / 4, by, bx + i * inch / 4, by + h)
    c.setFont("Helvetica", 6.5)
    c.drawString(bx + inch + 6, by, "= 1 inch. Print at 100% / Actual Size (no 'Fit to page'), then check this bar with a ruler.")
    c.drawRightString(8.0 * inch, by, code + "  |  LOCKED")


def rings(c, x, y, diams, black_from=None, nums=None, fill=black, lw=0.7):
    """diams largest->smallest in inches."""
    for i, d in enumerate(diams):
        r = d * inch / 2
        filled = black_from is not None and i >= black_from
        c.setFillColor(fill if filled else white)
        c.setStrokeColor(white if filled and i > black_from else DK)
        c.setLineWidth(lw)
        c.circle(x, y, r, stroke=1, fill=1)
    if nums:
        c.setFont("Helvetica-Bold", 7)
        for i, (d, n) in enumerate(zip(diams, nums)):
            if n is None or i + 1 >= len(diams):
                continue
            rmid = (d + diams[i + 1]) / 4 * inch
            filled = black_from is not None and i >= black_from
            c.setFillColor(white if filled else DK)
            for ang in (0, 180):
                a = math.radians(ang)
                c.drawCentredString(x + rmid * math.cos(a), y - 2.5, str(n))


def grid(c, x0, y0, w, h, step, color=GR, lw=0.4, major=None):
    c.setLineWidth(lw)
    n = int(round(w / step))
    for i in range(n + 1):
        xx = x0 + i * step
        c.setStrokeColor(DK if major and i % major == 0 else color)
        c.line(xx, y0, xx, y0 + h)
    m = int(round(h / step))
    for j in range(m + 1):
        yy = y0 + j * step
        c.setStrokeColor(DK if major and j % major == 0 else color)
        c.line(x0, yy, x0 + w, yy)


def diamond(c, x, y, s, col=OR):
    p = c.beginPath()
    p.moveTo(x, y + s); p.lineTo(x + s, y); p.lineTo(x, y - s); p.lineTo(x - s, y); p.close()
    c.setFillColor(col); c.setStrokeColor(DK); c.setLineWidth(0.6)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(white)
    c.rect(x - s * 0.18, y - s * 0.18, s * 0.36, s * 0.36, stroke=0, fill=1)


def label(c, x, y, txt, size=8, bold=False, col=DK, center=True):
    c.setFillColor(col)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    (c.drawCentredString if center else c.drawString)(x, y, txt)


# ---------------- targets ----------------

@target("T-01", "Five-Bull Sight-In", "General sight-in. Five 2.5 in. bulls on a 1 in. grid. Pistol 7-15 yd, rifle 25-50 yd.")
def t01(c):
    x0, y0 = 0.75 * inch, 1.5 * inch
    grid(c, x0, y0, 7 * inch, 8.5 * inch, inch)
    pts = [(2.25, 8.0), (6.25, 8.0), (4.25, 5.75), (2.25, 3.5), (6.25, 3.5)]
    for i, (x, y) in enumerate(pts):
        rings(c, x * inch, y * inch, [2.5, 1.85, 1.2, 0.6], black_from=2, fill=OR)
        c.setStrokeColor(DK); c.setLineWidth(0.5)
        c.line(x * inch - 1.35 * inch, y * inch, x * inch + 1.35 * inch, y * inch)
        c.line(x * inch, y * inch - 1.35 * inch, x * inch, y * inch + 1.35 * inch)
        label(c, x * inch - 1.3 * inch, y * inch + 1.3 * inch, str(i + 1), 11, True)


@target("T-02", "100-Yard Zero Grid", "1 in. squares. At 100 yd each square is about 1 MOA (1.047 in.). Center diamond for zero, corners for confirmation.")
def t02(c):
    x0, y0 = 0.75 * inch, 1.5 * inch
    w, h = 7 * inch, 8.5 * inch
    grid(c, x0, y0, w, h, 0.5 * inch, color=LG, lw=0.3)
    grid(c, x0, y0, w, h, inch, color=GR, lw=0.6)
    cx, cy = x0 + 3.5 * inch, y0 + 4.5 * inch
    c.setStrokeColor(DK); c.setLineWidth(1.2)
    c.line(x0, cy, x0 + w, cy); c.line(cx, y0, cx, y0 + h)
    c.setFont("Helvetica", 6)
    c.setFillColor(DK)
    for i in range(-3, 4):
        if i: c.drawCentredString(cx + i * inch, cy - 8, str(abs(i)))
    for j in range(-4, 5):
        if j: c.drawString(cx + 3, cy + j * inch - 2, str(abs(j)))
    diamond(c, cx, cy, 0.75 * inch)
    for dx, dy in [(-2.5, 3), (2.5, 3), (-2.5, -3), (2.5, -3)]:
        diamond(c, cx + dx * inch, cy + dy * inch, 0.4 * inch)


@target("T-03", "25 m Metric Zero", "1 cm squares. At 25 m each square = 0.4 mil (about 1.4 MOA). Move impacts to the center circle.")
def t03(c):
    cm = inch / 2.54
    n = 17
    x0 = CX - n * cm / 2
    y0 = 5.75 * inch - 11 * cm
    grid(c, x0, y0, n * cm, 22 * cm, cm, color=GR, lw=0.4, major=5)
    cx, cy = CX, y0 + 11 * cm
    c.setStrokeColor(DK); c.setLineWidth(1.2)
    c.line(x0, cy, x0 + n * cm, cy); c.line(cx, y0, cx, y0 + 22 * cm)
    c.setFillColor(OR); c.setStrokeColor(DK)
    c.circle(cx, cy, 2 * cm, stroke=1, fill=0)
    c.setLineWidth(0.6)
    c.circle(cx, cy, 1 * cm, stroke=1, fill=1)
    label(c, cx, y0 - 14, "Major lines every 5 cm. Aim at center; group should land inside the 4 cm circle.", 7.5)


@target("T-04", "MOA Dot Ladder", "Dot sizes in true MOA at 100 yd. Rows: 2, 1.5, 1 and 0.5 MOA. Shoot each row smaller as you tighten up.")
def t04(c):
    sizes = [2, 1.5, 1, 0.5]
    for r, moa in enumerate(sizes):
        y = (8.7 - r * 2.2) * inch
        label(c, 0.75 * inch, y - 3, f"{moa} MOA", 9, True, center=False)
        for k in range(3):
            x = (2.6 + k * 2.2) * inch
            d = moa * 1.047 * inch
            c.setFillColor(OR if k % 2 == 0 else DK); c.setStrokeColor(DK)
            c.circle(x, y, d / 2, stroke=0, fill=1)
            c.setStrokeColor(GR); c.setLineWidth(0.4)
            c.line(x - 0.6 * inch, y, x - d / 2 - 3, y); c.line(x + d / 2 + 3, y, x + 0.6 * inch, y)
            c.line(x, y - 0.6 * inch, x, y - d / 2 - 3); c.line(x, y + d / 2 + 3, x, y + 0.6 * inch)
    label(c, CX, 1.55 * inch, "At 200 yd each dot doubles in angular difficulty (2 MOA dot = 1 MOA test).", 7.5)


@target("T-05", "Precision Bullseye", "Slow-fire scoring target. Rings 10 to 5 plus X ring. Score each shot by the highest ring it touches.")
def t05(c):
    diams = [7.5, 6.25, 5.0, 3.75, 2.5, 1.25, 0.6]
    rings(c, CX, 5.9 * inch, diams, black_from=3, nums=[5, 6, 7, 8, 9, 10], lw=0.8)
    label(c, CX, 5.9 * inch - 2.5, "X", 7, True, col=white)
    # score box
    y = 1.55 * inch
    c.setStrokeColor(DK); c.setLineWidth(0.6)
    for i in range(11):
        c.rect((0.75 + i * 0.64) * inch, y, 0.64 * inch, 0.35 * inch)
        label(c, (0.75 + i * 0.64 + 0.32) * inch, y + 0.38 * inch, str(i + 1) if i < 10 else "TOTAL", 6.5)


@target("T-06", "Rimfire 12-Bull", "Ten 1.5 in. record bulls plus two sighters. Built for 50 ft / 25 yd rimfire and air rifle practice.")
def t06(c):
    k = 0
    for r in range(4):
        for col in range(3):
            x = (2.0 + col * 2.25) * inch
            y = (8.75 - r * 2.2) * inch
            sighter = r == 0 and col in (0, 2)
            rings(c, x, y, [1.5, 1.1, 0.7, 0.3], black_from=1, fill=OR if sighter else black)
            if sighter:
                txt = "SIGHTER"
            else:
                k += 1; txt = str(k)
            label(c, x, y - 1.0 * inch, txt, 8, True)


@target("T-07", "Ten-Dot Drill", "2 in. and 1 in. dots. Run each numbered string in order. Any miss on a string means you rerun it.")
def t07(c):
    drills = [
        (2, "5 shots, slow fire"),
        (2, "Draw, 1 shot. x5"),
        (1, "5 shots, slow fire"),
        (1, "Draw, 1 shot. x5"),
        (2, "Draw, 2 shots. x3"),
        (2, "Strong hand only, 5"),
        (2, "Weak hand only, 5"),
        (1, "1 shot each on 8 then 9, x4"),
        (1, None),
        (2, "Reload drill: 1, reload, 1. x2"),
    ]
    pos = [(1.6, 8.6), (4.25, 8.6), (6.9, 8.6),
           (1.6, 6.35), (4.25, 6.35), (6.9, 6.35),
           (1.6, 4.1), (3.35, 4.1), (5.15, 4.1),
           (6.9, 4.1)]
    for i, ((d, txt), (x, y)) in enumerate(zip(drills, pos)):
        c.setFillColor(OR if d == 2 else DK); c.setStrokeColor(DK); c.setLineWidth(0.6)
        c.circle(x * inch, y * inch, d * inch / 2, stroke=1, fill=0 if d == 2 else 1)
        if d == 2:
            c.setFillColor(OR); c.circle(x * inch, y * inch, 0.15 * inch, stroke=0, fill=1)
        label(c, x * inch - 1.1 * inch, y * inch + 0.85 * inch, str(i + 1), 12, True, center=False)
    # instructions box
    c.setStrokeColor(DK); c.setLineWidth(0.6)
    c.rect(0.75 * inch, 1.4 * inch, 7 * inch, 1.5 * inch)
    c.setFont("Helvetica-Bold", 8); c.setFillColor(DK)
    c.drawString(0.9 * inch, 2.7 * inch, "STRINGS (start at 3 yd, back up once you run it clean)")
    c.setFont("Helvetica", 7.5)
    for i, (d, txt) in enumerate(drills):
        if txt is None:
            txt = "(see 8)"
        col, row = divmod(i, 5)
        c.drawString((0.9 + col * 3.5) * inch, (2.45 - row * 0.2) * inch, f"{i+1}.  {txt}")


@target("T-08", "Reduced Silhouette", "Generic torso and head with scoring zones. Reduced size: shooting it at 10 yd looks like a full-size target at about 30 yd.")
def t08(c):
    cx = CX
    base = 1.6 * inch
    # body
    p = c.beginPath()
    bw, bh = 5.6 * inch, 5.8 * inch
    p.roundRect(cx - bw / 2, base, bw, bh, 0.9 * inch)
    c.setFillColor(HexColor("#D9C8A9")); c.setStrokeColor(DK); c.setLineWidth(1)
    c.drawPath(p, stroke=1, fill=1)
    # neck + head
    c.rect(cx - 0.6 * inch, base + bh - 0.1 * inch, 1.2 * inch, 0.5 * inch, stroke=0, fill=1)
    c.roundRect(cx - 1.05 * inch, base + bh + 0.35 * inch, 2.1 * inch, 2.1 * inch, 0.7 * inch, stroke=1, fill=1)
    c.setDash(3, 2); c.setLineWidth(0.8)
    # A zones
    c.rect(cx - 1.0 * inch, base + 2.4 * inch, 2.0 * inch, 2.9 * inch, stroke=1, fill=0)
    c.rect(cx - 0.6 * inch, base + bh + 0.6 * inch, 1.2 * inch, 0.8 * inch, stroke=1, fill=0)
    # C zone
    c.rect(cx - 1.9 * inch, base + 1.2 * inch, 3.8 * inch, 4.4 * inch, stroke=1, fill=0)
    c.setDash()
    label(c, cx, base + 3.8 * inch, "A", 16, True)
    label(c, cx, base + bh + 0.92 * inch, "A", 10, True)
    label(c, cx - 1.55 * inch, base + 1.45 * inch, "C", 12, True)
    label(c, cx - 2.4 * inch, base + 0.35 * inch, "D", 12, True)


@target("T-09", "Shapes & Numbers", "Call-out drill. A partner calls a shape, a color, or a number and you engage only that target. Builds target ID under time.")
def t09(c):
    items = [
        ("circle", OR, "1"), ("square", DK, "2"), ("triangle", OR, "3"),
        ("triangle", DK, "4"), ("circle", DK, "5"), ("square", OR, "6"),
        ("square", OR, "7"), ("triangle", DK, "8"), ("circle", OR, "9"),
    ]
    s = 1.0 * inch
    for i, (shape, col, n) in enumerate(items):
        r, k = divmod(i, 3)
        x = (1.85 + k * 2.4) * inch
        y = (8.3 - r * 2.55) * inch
        c.setFillColor(col); c.setStrokeColor(DK); c.setLineWidth(0.8)
        if shape == "circle":
            c.circle(x, y, s, stroke=1, fill=1)
        elif shape == "square":
            c.rect(x - s * 0.9, y - s * 0.9, s * 1.8, s * 1.8, stroke=1, fill=1)
        else:
            p = c.beginPath(); p.moveTo(x, y + s); p.lineTo(x + s * 1.05, y - s * 0.8); p.lineTo(x - s * 1.05, y - s * 0.8); p.close()
            c.drawPath(p, stroke=1, fill=1)
        c.setFillColor(white); c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(x, y - (18 if shape == "triangle" else 11), n)


@target("T-10", "Tic-Tac-Toe", "Two shooters, one target. Hit a square to claim it with your color of marker. First to three in a row wins.")
def t10(c):
    s = 2.2 * inch
    x0 = CX - 1.5 * s
    y0 = 2.35 * inch
    c.setStrokeColor(DK); c.setLineWidth(3)
    for i in (1, 2):
        c.line(x0 + i * s, y0, x0 + i * s, y0 + 3 * s)
        c.line(x0, y0 + i * s, x0 + 3 * s, y0 + i * s)
    for r in range(3):
        for k in range(3):
            x = x0 + k * s + s / 2; y = y0 + r * s + s / 2
            c.setFillColor(OR); c.setStrokeColor(DK); c.setLineWidth(0.6)
            c.circle(x, y, 0.55 * inch, stroke=1, fill=1)
            c.setFillColor(white); c.circle(x, y, 0.12 * inch, stroke=0, fill=1)
    label(c, CX, 1.6 * inch, "Tip: use colored target pasters or a marker to claim squares between strings.", 7.5)


@target("T-11", "Plate Rack", "Two racks of six 1 in. plates plus a stop plate. At 10 yd each plate matches a 4 in. steel plate at 40 yd.")
def t11(c):
    for row, y in enumerate((8.2, 5.6)):
        c.setFillColor(GR); c.rect(0.9 * inch, (y - 1.35) * inch, 6.7 * inch, 0.18 * inch, stroke=0, fill=1)
        for k in range(6):
            x = (1.35 + k * 1.16) * inch
            c.setFillColor(GR); c.rect(x - 0.06 * inch, (y - 1.2) * inch, 0.12 * inch, 0.2 * inch, stroke=0, fill=1)
            c.setFillColor(OR if row == 0 else DK); c.setStrokeColor(DK)
            c.circle(x, (y - 0.15) * inch, 0.5 * inch, stroke=1, fill=1)
            label(c, x, (y - 0.15) * inch - 4, str(row * 6 + k + 1), 10, True, col=white)
    # stop plate
    c.setFillColor(OR); c.setStrokeColor(DK)
    c.rect(CX - 0.9 * inch, 1.6 * inch, 1.8 * inch, 1.8 * inch, stroke=1, fill=1)
    label(c, CX, 2.45 * inch, "STOP", 14, True, col=white)
    label(c, CX, 3.75 * inch, "Clear a rack left to right, then hit STOP. Log your time.", 8)


@target("T-12", "Error Diagnosis", "For a right-handed handgun shooter (mirror it if left-handed). Fire 10 slow shots at the center, then read where they cluster.")
def t12(c):
    cy = 5.9 * inch
    R = 3.4 * inch
    labels = [
        (90, "Anticipating recoil", "pushing / breaking wrist up"),
        (45, "Heeling", "palm pushing in anticipation"),
        (0, "Thumbing", "too little trigger finger"),
        (-45, "Tightening grip", "squeezing whole hand"),
        (-90, "Breaking wrist down", "pushing forward / flinch"),
        (-135, "Jerking trigger", "slapping or jerking"),
        (180, "Too much finger", "trigger in the joint"),
        (135, "Wrist break up", "drifting high left"),
    ]
    c.setStrokeColor(GR); c.setLineWidth(0.6)
    c.circle(CX, cy, R, stroke=1, fill=0)
    for a in range(-158, 202, 45):
        rad = math.radians(a + 0.5)
        c.line(CX + 1.0 * inch * math.cos(rad), cy + 1.0 * inch * math.sin(rad), CX + R * math.cos(rad), cy + R * math.sin(rad))
    for ang, t1, t2 in labels:
        rad = math.radians(ang)
        x = CX + 2.3 * inch * math.cos(rad); y = cy + 2.3 * inch * math.sin(rad)
        label(c, x, y + 2, t1, 8, True)
        label(c, x, y - 8, t2, 6.5)
    rings(c, CX, cy, [2.0, 1.4, 0.8], black_from=1, fill=OR)


@target("T-13", "Load Development", "Ten 1 in. diamonds for a ladder or OCW test. Write the charge and seating depth under each.")
def t13(c):
    for i in range(10):
        r, k = divmod(i, 5)
        x = (1.15 + k * 1.55) * inch
        y = (7.9 - r * 3.4) * inch
        c.setStrokeColor(LG); c.setLineWidth(0.4)
        grid(c, x - 0.7 * inch, y - 0.7 * inch, 1.4 * inch, 1.4 * inch, 0.25 * inch, color=LG)
        diamond(c, x, y, 0.5 * inch, OR if i % 2 == 0 else DK)
        label(c, x, y + 0.9 * inch, f"LOAD {i+1}", 8, True)
        c.setStrokeColor(DK); c.setLineWidth(0.5)
        for j, f in enumerate(("CHG", "OAL", "VEL")):
            yy = y - (1.05 + j * 0.3) * inch
            label(c, x - 0.65 * inch, yy, f, 6.5, center=False)
            c.line(x - 0.35 * inch, yy - 1, x + 0.65 * inch, yy - 1)


@target("T-14", "Transitions", "Three head boxes spread wide. Draw, one shot each left to right, then right to left. Push speed, keep hits in the box.")
def t14(c):
    for i, x in enumerate((1.4, 4.25, 7.1)):
        for row, y in enumerate((7.6, 4.0)):
            c.setFillColor(white); c.setStrokeColor(DK); c.setLineWidth(1)
            c.rect((x - 0.85) * inch, (y - 1.15) * inch, 1.7 * inch, 2.3 * inch, stroke=1, fill=1)
            c.setFillColor(OR if row == 0 else DK)
            c.rect((x - 0.5) * inch, (y - 0.4) * inch, 1.0 * inch, 0.8 * inch, stroke=0, fill=1)
            label(c, x * inch, (y + 1.3) * inch, f"{row*3+i+1}", 12, True)
    label(c, CX, 1.75 * inch, "Top row: 1-2-3, 3-2-1.   Bottom row: two shots each, 4-5-6.", 8)


@target("T-15", "Half-Inch Grid", "Blank 1/2 in. grid with a center cross. Use it for anything: group measuring, custom drills, or a backer.")
def t15(c):
    x0, y0 = 0.75 * inch, 1.5 * inch
    grid(c, x0, y0, 7 * inch, 8.5 * inch, 0.5 * inch, color=GR, lw=0.4, major=2)
    c.setStrokeColor(OR); c.setLineWidth(1.5)
    cx, cy = x0 + 3.5 * inch, y0 + 4.25 * inch
    c.line(cx, y0, cx, y0 + 8.5 * inch); c.line(x0, cy, x0 + 7 * inch, cy)
    c.setFillColor(OR); c.circle(cx, cy, 0.25 * inch, stroke=0, fill=1)


@target("T-16", "Range Log", "Record each group. Measure center-to-center (largest spread minus one bullet diameter).")
def t16(c):
    cols = [("#", 0.4), ("Date", 0.9), ("Firearm", 1.3), ("Ammo / Load", 1.4), ("Dist", 0.6), ("Shots", 0.6), ("Group", 0.7), ("Notes", 1.1)]
    x0, y = 0.75 * inch, 9.8 * inch
    rh = 0.33 * inch
    c.setStrokeColor(DK); c.setLineWidth(0.5)
    x = x0
    c.setFillColor(OR)
    c.rect(x0, y - rh, 7 * inch, rh, stroke=0, fill=1)
    for name, w in cols:
        label(c, x + 4, y - rh + 7, name.upper(), 7.5, True, col=white, center=False)
        x += w * inch
    for r in range(22):
        yy = y - rh * (r + 2)
        if r % 2 == 0:
            c.setFillColor(HexColor("#F4F4F4")); c.rect(x0, yy, 7 * inch, rh, stroke=0, fill=1)
        label(c, x0 + 0.2 * inch, yy + 7, str(r + 1), 7, center=True)
    x = x0
    for name, w in cols:
        c.line(x, y, x, y - rh * 23); x += w * inch
    c.line(x, y, x, y - rh * 23)
    for r in range(24):
        c.line(x0, y - rh * r, x0 + 7 * inch, y - rh * r)


# ---------------- shooter tools ----------------
def table(c, x0, ytop, cols, nrows, rh, rowlabels=None, size=7.5):
    """cols: list of (name, width_in). Draws header + nrows rows. Returns bottom y."""
    tw = sum(w for _, w in cols) * inch
    c.setFillColor(OR); c.rect(x0, ytop - rh, tw, rh, stroke=0, fill=1)
    x = x0
    for name, w in cols:
        label(c, x + w * inch / 2, ytop - rh + rh / 2 - 2.5, name.upper(), size, True, col=white)
        x += w * inch
    for r in range(nrows):
        yy = ytop - rh * (r + 2)
        if r % 2 == 0:
            c.setFillColor(HexColor("#F4F4F4")); c.rect(x0, yy, tw, rh, stroke=0, fill=1)
        if rowlabels:
            label(c, x0 + cols[0][1] * inch / 2, yy + rh / 2 - 3, str(rowlabels[r]), size + 0.5, True)
    c.setStrokeColor(DK); c.setLineWidth(0.5)
    bot = ytop - rh * (nrows + 1)
    x = x0
    for _, w in cols:
        c.line(x, ytop, x, bot); x += w * inch
    c.line(x, ytop, x, bot)
    for r in range(nrows + 2):
        c.line(x0, ytop - rh * r, x0 + tw, ytop - rh * r)
    return bot


def field_line(c, x, y, name, w, size=7):
    c.setFillColor(DK); c.setFont("Helvetica-Bold", size)
    c.drawString(x, y, name)
    tw = c.stringWidth(name, "Helvetica-Bold", size) + 3
    c.setStrokeColor(DK); c.setLineWidth(0.5)
    c.line(x + tw, y - 1.5, x + w, y - 1.5)


def checkbox(c, x, y, txt, size=8):
    c.setStrokeColor(DK); c.setLineWidth(0.7)
    c.rect(x, y - 1, 8, 8, stroke=1, fill=0)
    c.setFillColor(DK); c.setFont("Helvetica", size)
    c.drawString(x + 13, y, txt)


@target("T-17", "Pocket DOPE Cards", "Four 3.5 x 4.25 in. cards. Cut on the dashed lines, fill in your come-ups, and tape one to the stock or keep it in a sleeve.")
def t17(c):
    cw, ch = 3.5 * inch, 4.25 * inch
    xs = [0.6 * inch, 4.4 * inch]
    ys = [5.65 * inch, 1.2 * inch]
    for yb in ys:
        for xb in xs:
            c.setStrokeColor(GR); c.setLineWidth(0.6); c.setDash(4, 3)
            c.rect(xb, yb, cw, ch, stroke=1, fill=0); c.setDash()
            p = 0.12 * inch
            x0, top = xb + p, yb + ch - p
            iw = cw - 2 * p
            c.setFillColor(DK); c.rect(x0, top - 0.28 * inch, iw, 0.28 * inch, stroke=0, fill=1)
            label(c, x0 + 5, top - 0.2 * inch, "DOPE", 10, True, col=OR, center=False)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 6.5)
            c.drawRightString(x0 + iw - 5, top - 0.19 * inch, "UNITS:   MOA   /   MIL")
            fy = top - 0.48 * inch
            field_line(c, x0, fy, "RIFLE", iw * 0.58, 6.5)
            field_line(c, x0 + iw * 0.62, fy, "ZERO", iw * 0.38, 6.5)
            field_line(c, x0, fy - 0.2 * inch, "LOAD", iw * 0.58, 6.5)
            field_line(c, x0 + iw * 0.62, fy - 0.2 * inch, "MV", iw * 0.38, 6.5)
            cols = [("YDS", 0.55), ("ELEV", 0.68), ("5 MPH", 0.68), ("10 MPH", 0.68), ("NOTE", 0.67)]
            table(c, x0, fy - 0.33 * inch, cols, 10, 0.26 * inch, rowlabels=list(range(100, 1100, 100)), size=6.5)


@target("T-18", "Full DOPE Sheet", "One rifle, 50 yd steps out to 1000. Record conditions at the top so you know what the data was shot in.")
def t18(c):
    x0 = 0.75 * inch
    y = 9.95 * inch
    for row in [[("RIFLE", 2.4), ("SCOPE", 2.2), ("UNITS  MOA / MIL", 2.4)],
                [("CARTRIDGE", 2.4), ("BULLET / WT", 2.2), ("MUZZLE VEL", 2.4)],
                [("ZERO RANGE", 1.6), ("SIGHT HEIGHT", 1.7), ("TWIST", 1.5), ("BC (G1/G7)", 2.2)],
                [("TEMP", 1.6), ("PRESSURE", 1.7), ("ALTITUDE / DA", 1.5), ("DATE", 2.2)]]:
        x = x0
        for name, w in row:
            field_line(c, x, y, name, w * inch - 10, 7.5)
            x += w * inch
        y -= 0.3 * inch
    cols = [("RANGE", 0.8), ("ELEV", 0.9), ("WIND 5", 0.85), ("WIND 10", 0.85), ("WIND 15", 0.85), ("LEAD", 0.75), ("CONFIRMED / NOTES", 2.0)]
    table(c, x0, y - 0.05 * inch, cols, 19, 0.315 * inch, rowlabels=list(range(100, 1050, 50)))


@target("T-19", "Angular Reference", "How big a MOA, a mil and one click are at each distance, plus range-estimation and conversion formulas.")
def t19(c):
    dists = [25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000]
    cols = [("YARDS", 1.0), ("1 MOA (IN)", 1.2), ("1/4 MOA CLICK", 1.2), ("1 MIL (IN)", 1.2), ("0.1 MIL CLICK", 1.2), ("1 MIL (CM)", 1.2)]
    x0, ytop, rh = 0.75 * inch, 9.95 * inch, 0.3 * inch
    table(c, x0, ytop, cols, len(dists), rh, rowlabels=dists)
    for r, d in enumerate(dists):
        moa = 1.047 * d / 100
        mil = 3.6 * d / 100
        vals = [f"{moa:.2f}", f"{moa/4:.2f}", f"{mil:.2f}", f"{mil/10:.2f}", f"{d*0.9144/10:.1f}"]
        yy = ytop - rh * (r + 2) + rh / 2 - 3
        x = x0 + 1.0 * inch
        c.setFont("Helvetica", 8); c.setFillColor(DK)
        for v in vals:
            c.drawCentredString(x + 0.6 * inch, yy, v); x += 1.2 * inch
    # formulas
    by = 2.75 * inch
    c.setFillColor(DK); c.rect(x0, 1.3 * inch, 7 * inch, by - 1.3 * inch + 0.25 * inch, stroke=0, fill=1)
    label(c, x0 + 10, by + 0.05 * inch, "FORMULAS", 9, True, col=OR, center=False)
    lines = [
        ("Range (yd) =", "target size (in) x 27.78  /  size in mils"),
        ("Range (m) =", "target size (m) x 1000  /  size in mils"),
        ("Range (yd) =", "target size (in) x 95.5  /  size in MOA"),
        ("Mils to MOA:", "mils x 3.438        MOA to mils:  MOA / 3.438"),
        ("Inches to MOA:", "inches / (1.047 x yards / 100)"),
    ]
    for i, (a, b) in enumerate(lines):
        yy = by - 0.25 * inch - i * 0.22 * inch
        label(c, x0 + 10, yy, a, 8.5, True, col=white, center=False)
        label(c, x0 + 1.25 * inch, yy, b, 8.5, col=white, center=False)
    label(c, CX, 1.4 * inch - 1, "Reference sizes: deer chest about 18 in. | IPSC target 18 x 30 in. | human head about 6 x 9 in.", 7, col=HexColor("#BBBBBB"))


@target("T-20", "Wind Card", "Wind value by clock direction, field cues for estimating speed, and a blank hold table for your load.")
def t20(c):
    cx, cy, R = 2.65 * inch, 7.45 * inch, 1.75 * inch
    vals = {12: 0, 6: 0, 1: .5, 5: .5, 7: .5, 11: .5, 2: .87, 4: .87, 8: .87, 10: .87, 3: 1, 9: 1}
    for h in range(1, 13):
        ang = 90 - h * 30
        v = vals[h]
        col = OR if v == 1 else (HexColor("#F3A27F") if v > .8 else (HexColor("#FAD8C8") if v > 0 else white))
        c.setFillColor(col); c.setStrokeColor(DK); c.setLineWidth(0.6)
        c.wedge(cx - R, cy - R, cx + R, cy + R, ang - 15, 30, stroke=1, fill=1)
        rad = math.radians(ang)
        tx, ty = cx + R * 0.72 * math.cos(rad), cy + R * 0.72 * math.sin(rad)
        label(c, tx, ty + 1, str(h), 9, True)
        txt = {0: "none", .5: "half", .87: "~full", 1: "FULL"}[v]
        label(c, tx, ty - 8, txt, 6)
    c.setFillColor(white); c.circle(cx, cy, 0.35 * inch, stroke=1, fill=1)
    label(c, cx, cy - 3, "YOU", 7, True)
    p = c.beginPath(); p.moveTo(cx, cy + R + 14); p.lineTo(cx - 6, cy + R + 4); p.lineTo(cx + 6, cy + R + 4); p.close()
    c.setFillColor(DK); c.drawPath(p, stroke=0, fill=1)
    label(c, cx, cy + R + 18, "TARGET", 7, True)
    # speed cues
    x0, y = 4.9 * inch, 9.0 * inch
    label(c, x0, y + 0.1 * inch, "ESTIMATING SPEED", 9, True, col=OR, center=False)
    cues = [("0-3 mph", "Barely felt. Smoke drifts."), ("3-5 mph", "Felt lightly on your face."),
            ("5-8 mph", "Leaves and small twigs move steadily."), ("8-12 mph", "Raises dust and loose paper."),
            ("12-15 mph", "Small trees begin to sway."), ("15+ mph", "Large branches move. Hard to hold.")]
    for i, (a, b) in enumerate(cues):
        yy = y - 0.2 * inch - i * 0.38 * inch
        label(c, x0, yy, a, 8, True, center=False)
        label(c, x0, yy - 10, b, 7, center=False)
    label(c, x0, y - 2.5 * inch, "Hold = full-value hold x clock value.", 7.5, True, center=False)
    label(c, x0, y - 2.5 * inch - 11, "Example: 10 mph from 1 o'clock = half the 10 mph hold.", 7, center=False)
    cols = [("RANGE", 1.0), ("5 MPH", 1.2), ("10 MPH", 1.2), ("15 MPH", 1.2), ("20 MPH", 1.2), ("NOTES", 1.2)]
    table(c, 0.75 * inch, 5.2 * inch, cols, 10, 0.32 * inch, rowlabels=list(range(100, 1100, 100)))
    label(c, CX, 1.35 * inch, "Values are full-value holds (wind from 3 or 9 o'clock) in your scope's units.", 7.5)


@target("T-21", "Round Count Log", "Track rounds, cleaning, parts and malfunctions for one firearm. Helps you replace springs and barrels on schedule.")
def t21(c):
    x0, y = 0.75 * inch, 9.95 * inch
    for row in [[("FIREARM", 3.0), ("SERIAL / ID", 2.2), ("START COUNT", 1.8)],
                [("BARREL / PARTS INSTALLED", 4.2), ("DATE", 2.8)]]:
        x = x0
        for name, w in row:
            field_line(c, x, y, name, w * inch - 10, 7.5)
            x += w * inch
        y -= 0.3 * inch
    cols = [("DATE", 0.85), ("ROUNDS", 0.75), ("TOTAL", 0.8), ("AMMO", 1.15), ("CLEANED", 0.7), ("MALFUNCTIONS", 1.25), ("PARTS / NOTES", 1.5)]
    table(c, x0, y - 0.05 * inch, cols, 22, 0.315 * inch)


@target("T-22", "Range Day Checklist", "Run through this before you leave the house. Laminate it and check boxes with a dry-erase marker.")
def t22(c):
    groups = [
        ("SAFETY", ["Eye protection", "Ear protection (plus spares)", "Tourniquet and trauma kit", "Range rules / membership card", "Hat with brim", "Phone charged"]),
        ("FIREARMS", ["Firearms unloaded and cased", "Magazines (counted)", "Optics zeroed / batteries checked", "Cleaning rod or bore snake", "Lube", "Holster and belt"]),
        ("AMMO", ["Ammo for each caliber", "Correct load for DOPE", "Ammo can / range bag", "Brass bag or bucket"]),
        ("TARGETS & SETUP", ["Printed targets", "Stapler, tape or clips", "Target pasters / markers", "Cardboard backers", "Target stand"]),
        ("GEAR", ["Shot timer", "Spotting scope or binoculars", "Rest, bags or bipod", "Rangefinder", "Wind meter", "Shooting mat"]),
        ("DATA", ["DOPE card", "Range log and pen", "Chronograph", "Multitool / torque driver", "Spare batteries", "Water and snacks"]),
    ]
    for gi, (name, items) in enumerate(groups):
        col, row = gi % 2, gi // 2
        x = (0.85 + col * 3.6) * inch
        y = (9.75 - row * 2.75) * inch
        c.setFillColor(OR); c.rect(x - 0.1 * inch, y - 2, 3.3 * inch, 0.22 * inch, stroke=0, fill=1)
        label(c, x, y + 3, name, 9, True, col=white, center=False)
        for i, it in enumerate(items):
            checkbox(c, x, y - 0.3 * inch - i * 0.32 * inch, it, 9)


# ---------------- field kit ----------------
@target("T-23", "36-Yard Zero", "Grid squares are 1 MOA at 36 yd (0.377 in.). A common carbine zero distance. Confirm at your far distance afterward.")
def t23(c):
    s = 0.377 * inch
    nx, ny = 17, 21
    x0 = CX - nx * s / 2
    cy = 5.85 * inch
    y0 = cy - ny * s / 2
    grid(c, x0, y0, nx * s, ny * s, s, color=GR, lw=0.4, major=None)
    c.setStrokeColor(DK); c.setLineWidth(1.2)
    c.line(x0, cy, x0 + nx * s, cy); c.line(CX, y0, CX, y0 + ny * s)
    # tick numbers every 2 MOA
    c.setFont("Helvetica", 5.5); c.setFillColor(DK)
    for i in range(-8, 9, 2):
        if i: c.drawCentredString(CX + i * s, cy - 7, str(abs(i)))
    for j in range(-10, 11, 2):
        if j: c.drawString(CX + 2, cy + j * s - 2, str(abs(j)))
    c.setFillColor(OR); c.setStrokeColor(DK); c.setLineWidth(0.6)
    c.circle(CX, cy, 2 * s, stroke=1, fill=1)
    c.setFillColor(white); c.circle(CX, cy, 0.5 * s, stroke=0, fill=1)
    label(c, CX, y0 - 14, "Numbers = MOA from center at 36 yd. Center dot = 4 MOA. Zero distance depends on your optic and ammo; confirm it on paper at range.", 7)


@target("T-24", "Data Book Page", "One page per string. Plot where you called each shot and where it hit. The gap between the two shows what to fix.")
def t24(c):
    x0, y = 0.75 * inch, 9.95 * inch
    rows = [[("DATE", 1.6), ("TIME", 1.2), ("RANGE / LANE", 2.0), ("DISTANCE", 2.2)],
            [("RIFLE / OPTIC", 3.0), ("AMMO / LOT", 2.0), ("POSITION", 2.0)],
            [("LIGHT", 1.6), ("TEMP", 1.2), ("WIND DIR / SPEED", 2.0), ("MIRAGE", 2.2)],
            [("ELEV SET", 1.6), ("WIND SET", 1.2), ("ZERO / BDC MARK", 2.0), ("SHOOTER", 2.2)]]
    for row in rows:
        x = x0
        for name, w in row:
            field_line(c, x, y, name, w * inch - 10, 7.5)
            x += w * inch
        y -= 0.3 * inch
    # two plots
    for k, ttl in enumerate(("CALLED", "ACTUAL HIT")):
        px = (2.25 + k * 4.0) * inch
        py = 6.55 * inch
        r = 1.45 * inch
        label(c, px, py + r + 8, ttl, 9, True, col=OR)
        for d in (2.9, 2.0, 1.1):
            c.setStrokeColor(DK if d < 2.5 else GR); c.setLineWidth(0.6)
            c.circle(px, py, d * inch / 2, stroke=1, fill=0)
        c.setFillColor(DK); c.circle(px, py, 0.25 * inch, stroke=0, fill=1)
        c.setStrokeColor(GR); c.setLineWidth(0.4)
        c.line(px - r, py, px + r, py); c.line(px, py - r, px, py + r)
        label(c, px, py - r - 12, "Number each shot", 6.5)
    cols = [("SHOT", 0.6), ("CALL", 1.0), ("ELEV", 0.9), ("WIND", 0.9), ("HIT?", 0.7), ("REMARKS", 2.9)]
    bot = table(c, x0, 4.75 * inch, cols, 10, 0.25 * inch, rowlabels=list(range(1, 11)), size=7)
    field_line(c, x0, bot - 0.25 * inch, "CORRECTIONS FOR NEXT STRING", 7 * inch, 7.5)
    c.setStrokeColor(DK); c.line(x0, bot - 0.5 * inch, x0 + 7 * inch, bot - 0.5 * inch)


@target("T-25", "Metric DOPE Cards", "Four cut-out cards ranged in meters (100-1000 m) for mil-based optics. Same layout as the yard cards.")
def t25(c):
    cw, ch = 3.5 * inch, 4.25 * inch
    for yb in (5.65 * inch, 1.2 * inch):
        for xb in (0.6 * inch, 4.4 * inch):
            c.setStrokeColor(GR); c.setLineWidth(0.6); c.setDash(4, 3)
            c.rect(xb, yb, cw, ch, stroke=1, fill=0); c.setDash()
            p = 0.12 * inch
            x0, top = xb + p, yb + ch - p
            iw = cw - 2 * p
            c.setFillColor(DK); c.rect(x0, top - 0.28 * inch, iw, 0.28 * inch, stroke=0, fill=1)
            label(c, x0 + 5, top - 0.2 * inch, "DOPE  (METERS)", 10, True, col=OR, center=False)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 6.5)
            c.drawRightString(x0 + iw - 5, top - 0.19 * inch, "UNITS:  MIL / MOA")
            fy = top - 0.48 * inch
            field_line(c, x0, fy, "RIFLE", iw * 0.58, 6.5)
            field_line(c, x0 + iw * 0.62, fy, "ZERO", iw * 0.38, 6.5)
            field_line(c, x0, fy - 0.2 * inch, "LOAD", iw * 0.58, 6.5)
            field_line(c, x0 + iw * 0.62, fy - 0.2 * inch, "MV", iw * 0.38, 6.5)
            cols = [("M", 0.55), ("ELEV", 0.68), ("5 MPH", 0.68), ("10 MPH", 0.68), ("NOTE", 0.67)]
            table(c, x0, fy - 0.33 * inch, cols, 10, 0.26 * inch, rowlabels=list(range(100, 1100, 100)), size=6.5)


@target("T-26", "Range Card", "Sketch your sector from your position: left and right limits, reference points and their ranges. Fill in the table to match.")
def t26(c):
    x0, y = 0.75 * inch, 9.95 * inch
    for row in [[("POSITION", 2.6), ("WEAPON / OPTIC", 2.4), ("DATE / TIME", 2.0)]]:
        x = x0
        for name, w in row:
            field_line(c, x, y, name, w * inch - 10, 7.5); x += w * inch
    cx, cy = CX, 4.55 * inch
    rings_m = [100, 200, 300, 400, 500]
    rmax = 3.9 * inch
    c.setLineWidth(0.6)
    for i, m in enumerate(rings_m):
        r = rmax * (i + 1) / len(rings_m)
        c.setStrokeColor(GR if i < 4 else DK)
        c.arc(cx - r, cy - r, cx + r, cy + r, 30, 120)
        c.setFillColor(DK); c.setFont("Helvetica", 6.5)
        c.drawCentredString(cx + 4, cy + r + 2, f"{m} m")
    c.setStrokeColor(GR); c.setDash(2, 3)
    for a in range(30, 151, 20):
        rad = math.radians(a)
        c.line(cx, cy, cx + rmax * math.cos(rad), cy + rmax * math.sin(rad))
    c.setDash()
    c.setFillColor(OR); c.setStrokeColor(DK)
    p = c.beginPath(); p.moveTo(cx, cy + 10); p.lineTo(cx + 9, cy - 6); p.lineTo(cx - 9, cy - 6); p.close()
    c.drawPath(p, stroke=1, fill=1)
    label(c, cx, cy - 16, "YOUR POSITION", 7, True)
    # north box
    bx, by = 7.0 * inch, 8.95 * inch
    c.setStrokeColor(DK); c.rect(bx, by, 0.75 * inch, 0.75 * inch, stroke=1, fill=0)
    label(c, bx + 0.375 * inch, by + 0.8 * inch, "DRAW N", 6.5, True)
    label(c, 0.75 * inch, 9.45 * inch, "Mark left limit (L), right limit (R), and number each reference point (TRP 1, 2, 3...).", 7.5, center=False)
    label(c, 0.75 * inch, 9.3 * inch, "Change the ring labels if your sector is shorter or longer.", 7.5, center=False)
    cols = [("TRP", 0.5), ("DESCRIPTION", 2.4), ("RANGE", 0.9), ("AZIMUTH", 0.9), ("ELEV / HOLD", 1.1), ("NOTES", 1.2)]
    table(c, x0, 4.15 * inch, cols, 8, 0.28 * inch, rowlabels=["L", "R", 1, 2, 3, 4, 5, 6])


@target("T-27", "Range Estimation", "Mil-relation table in meters. Measure the target in mils through your reticle, find its row, and read the range.")
def t27(c):
    mils = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5]
    objs = [("Head (height)", 0.25), ("Shoulder width", 0.5), ("Torso, waist to head", 0.9), ("Standing person", 1.8),
            ("Door height", 2.0), ("Car height", 1.5), ("Car length", 4.5), ("Truck / van height", 3.0), ("Fence post (std. 1.2 m)", 1.2)]
    cols = [("OBJECT", 1.75), ("SIZE (M)", 0.75)] + [(f"{m} MIL", 0.5625) for m in mils]
    x0, ytop, rh = 0.75 * inch, 9.95 * inch, 0.34 * inch
    table(c, x0, ytop, cols, len(objs), rh, size=7)
    for r, (name, sz) in enumerate(objs):
        yy = ytop - rh * (r + 2) + rh / 2 - 3
        label(c, x0 + 5, yy, name, 7.5, True, center=False)
        label(c, x0 + 1.75 * inch + 0.375 * inch, yy, f"{sz:g}", 7.5)
        x = x0 + 2.5 * inch
        for m in mils:
            rng = sz * 1000 / m
            txt = f"{rng:,.0f}" if rng < 2000 else "—"
            label(c, x + 0.28 * inch, yy, txt, 7.5)
            x += 0.5625 * inch
    y = ytop - rh * (len(objs) + 1) - 0.45 * inch
    c.setFillColor(DK); c.rect(x0, y - 2.2 * inch, 7 * inch, 2.35 * inch, stroke=0, fill=1)
    label(c, x0 + 10, y - 0.05 * inch, "FORMULAS & METHODS", 9, True, col=OR, center=False)
    lines = [
        ("Mil-relation:", "range (m) = size (m) x 1000 / mils"),
        ("In yards:", "range (yd) = size (yd) x 1000 / mils"),
        ("100 m units:", "picture a 100 m field and count how many fit to the target"),
        ("Bracketing:", "estimate the nearest and farthest it could be, then average"),
        ("Looks closer:", "bright light, looking across water or a valley, large targets"),
        ("Looks farther:", "poor light, looking over smooth ground, small or partly hidden targets"),
    ]
    for i, (a, b) in enumerate(lines):
        yy = y - 0.35 * inch - i * 0.28 * inch
        label(c, x0 + 10, yy, a, 8.5, True, col=white, center=False)
        label(c, x0 + 1.35 * inch, yy, b, 8.5, col=white, center=False)
    label(c, CX, y - 2.45 * inch, "Ranges over 2,000 m are left blank. Sizes are averages; real targets vary.", 7)


@target("T-28", "Fundamentals Card", "Safety rules, the marksmanship fundamentals, position checkpoints and immediate action for a stoppage. Laminate for the range bag.")
def t28(c):
    blocks = [
        ("FOUR SAFETY RULES", [
            "1. Treat every firearm as loaded.",
            "2. Never point the muzzle at anything you are not willing to destroy.",
            "3. Keep your finger off the trigger until your sights are on target.",
            "4. Be sure of your target and what is beyond it."]),
        ("FUNDAMENTALS", [
            "Position: stable, bone support, natural point of aim on the target.",
            "Aim: front sight or reticle sharp, sight alignment held.",
            "Breath: settle and fire in the natural pause after you exhale.",
            "Trigger: smooth press straight back. Do not slap or jerk.",
            "Follow-through: hold the trigger back, then call the shot."]),
        ("POSITION CHECKPOINTS", [
            "Prone: body angled behind the rifle, support elbow under the gun.",
            "Sitting: elbows in front of or on the knees, not bone on bone.",
            "Kneeling: support elbow forward of the knee, weight on the heel.",
            "Standing: feet shoulder width, support arm under the handguard.",
            "NPA check: close eyes, breathe, open. Move your body, not your arms."]),
        ("IMMEDIATE ACTION (CARBINE)", [
            "Tap: firmly seat the magazine.",
            "Rack: pull the charging handle fully back and release.",
            "Assess: check the target and your situation.",
            "Still down? Lock the bolt back, strip the magazine,",
            "clear the chamber and reload. Squib suspected: stop and inspect."]),
        ("CALLING THE SHOT", [
            "Note exactly where the reticle was when the shot broke.",
            "Call good on target = hit expected. Call it off = fix your fundamentals.",
            "Good call but bad hit = adjust the optic, wind or elevation."]),
    ]
    x0, y = 0.75 * inch, 9.85 * inch
    for title, lines in blocks:
        c.setFillColor(OR); c.rect(x0, y - 4, 7 * inch, 0.24 * inch, stroke=0, fill=1)
        label(c, x0 + 8, y + 2, title, 9, True, col=white, center=False)
        y -= 0.3 * inch
        for ln in lines:
            label(c, x0 + 8, y - 2, ln, 9, center=False)
            y -= 0.21 * inch
        y -= 0.2 * inch


@target("T-29", "Dry-Fire Log", "Daily dry practice tracker. Unload, move all ammo out of the room, verify empty, and pick a safe backstop before every session.")
def t29(c):
    cols = [("DATE", 0.9), ("MIN", 0.6), ("DRILL", 1.9), ("REPS", 0.6), ("PAR TIME", 0.8), ("BEST", 0.7), ("NOTES", 1.5)]
    table(c, 0.75 * inch, 9.95 * inch, cols, 24, 0.31 * inch)
    label(c, CX, 1.55 * inch, "Ideas: draw to first shot, reloads, trigger press on a dot, transitions, position changes, malfunction clears.", 7.5)


# ---------------- build ----------------
SECTIONS = [("TARGETS", 0, 16), ("SHOOTER TOOLS", 16, 22), ("FIELD KIT", 22, 99)]


def cover(c):
    c.setFillColor(DK); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(OR); c.circle(W - 1.5 * inch, H - 1.45 * inch, 0.85 * inch, stroke=0, fill=1)
    c.setFillColor(DK); c.circle(W - 1.5 * inch, H - 1.45 * inch, 0.55 * inch, stroke=0, fill=1)
    c.setFillColor(OR); c.circle(W - 1.5 * inch, H - 1.45 * inch, 0.24 * inch, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("Helvetica-Bold", 56)
    c.drawString(0.7 * inch, 9.5 * inch, "LOCKED")
    c.setFont("Helvetica", 11)
    c.drawString(0.75 * inch, 9.12 * inch, f"Targets, data and field tools  |  {len(PAGES)} pages  |  US Letter, true scale")
    colx = [0.75 * inch, 4.4 * inch]
    layout = [(0, SECTIONS[0]), (1, SECTIONS[1]), (1, SECTIONS[2])]
    ys = [8.3 * inch, 8.3 * inch]
    rh = 0.36 * inch
    for col, (name, a0, a1) in layout:
        x = colx[col]; y = ys[col]
        c.setFillColor(OR); c.setFont("Helvetica-Bold", 9)
        c.drawString(x, y, name)
        c.setStrokeColor(OR); c.setLineWidth(0.8); c.line(x, y - 5, x + 3.35 * inch, y - 5)
        y -= rh
        for i in range(a0, min(a1, len(PAGES))):
            code, title, sub, _ = PAGES[i]
            c.setFillColor(OR); c.setFont("Helvetica-Bold", 9); c.drawString(x, y, code)
            c.setFillColor(white); c.setFont("Helvetica-Bold", 10); c.drawString(x + 0.55 * inch, y, title)
            c.setFillColor(HexColor("#AAAAAA")); c.setFont("Helvetica", 9); c.drawRightString(x + 3.35 * inch, y, str(i + 2))
            c.linkRect("", f"p{i}", (x - 4, y - 8, x + 3.4 * inch, y + 12), relative=0)
            y -= rh
        ys[col] = y - 0.2 * inch
    c.setFont("Helvetica", 8); c.setFillColor(HexColor("#AAAAAA"))
    c.drawString(0.75 * inch, 0.9 * inch, "To print one target, print just its page number. Always print at 100% / Actual Size so the scales stay true.")
    c.drawString(0.75 * inch, 0.72 * inch, "Tap any row to jump to that page. Laminate the cards and checklists for field use.")
    c.showPage()


c = canvas.Canvas(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "LOCKED.pdf"), pagesize=(W, H))
c.setTitle("LOCKED - Targets, Data and Field Tools")
cover(c)
for i, (code, title, sub, fn) in enumerate(PAGES):
    c.bookmarkPage(f"p{i}")
    c.addOutlineEntry(f"{code} {title}", f"p{i}")
    header(c, code, title, sub)
    fn(c)
    footer(c, code)
    c.showPage()
c.save()
print(len(PAGES))
