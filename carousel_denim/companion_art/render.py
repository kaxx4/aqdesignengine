import random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

random.seed(42)

FONT_DIR = "/root/.claude/skills/synced/canvas-design/canvas-fonts"
mono = lambda s, bold=False: ImageFont.truetype(f"{FONT_DIR}/{'IBMPlexMono-Bold' if bold else 'IBMPlexMono-Regular'}.ttf", s)
serif = lambda s: ImageFont.truetype(f"{FONT_DIR}/YoungSerif-Regular.ttf", s)

W, H = 2000, 2500
CREAM = (238, 231, 214)
INDIGO_DARK = (26, 34, 58)
INDIGO_MID = (52, 68, 110)
INDIGO_PALE = (140, 156, 190)
RUST = (150, 92, 58)
INK = (18, 18, 22)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img, "RGBA")

# subtle paper grain
grain = Image.effect_noise((W, H), 22).convert("L")
grain = grain.point(lambda p: 128 + (p - 128) * 0.10)
img = Image.composite(Image.new("RGB", (W, H), (255, 255, 255)), img, grain.point(lambda p: max(0, p - 118)))
d = ImageDraw.Draw(img, "RGBA")

M = 130

# ledger ruling — faint horizontal register lines across the whole page
for y in range(M, H - M, 34):
    d.line([(M, y), (W - M, y)], fill=(120, 110, 90, 35), width=1)

# outer frame, hairline
d.rectangle([M - 40, M - 40, W - M + 40, H - M + 40], outline=(40, 36, 30, 200), width=2)

# ---- dominant seam-form: a single stitched seam running the full height ----
seam_x = 430
pts = []
seam_bottom = H - M - 180
for t in range(0, 101):
    ty = M - 20 + (seam_bottom - (M - 20)) * t / 100
    tx = seam_x + 38 * math.sin(t / 9.0) + 14 * math.sin(t / 3.3)
    pts.append((tx, ty))

# woven fiber field behind the seam (cross-hatch, dense repetition)
for i in range(0, 260):
    x0 = M + random.uniform(0, 640)
    y0 = M + random.uniform(0, H - 2 * M)
    length = random.uniform(18, 46)
    angle = random.choice([28, -28, 90, 0]) + random.uniform(-4, 4)
    rad = math.radians(angle)
    x1 = x0 + length * math.cos(rad)
    y1 = y0 + length * math.sin(rad)
    tone = random.choice([INDIGO_PALE, INDIGO_MID, INDIGO_DARK])
    alpha = random.randint(28, 70)
    d.line([(x0, y0), (x1, y1)], fill=tone + (alpha,), width=1)

# the seam itself: double stitched line, ink shadow offset
for ox, oy, col, w in [(6, 6, (0, 0, 0, 60), 10), (0, 0, INDIGO_DARK + (255,), 9)]:
    d.line([(px + ox, py + oy) for px, py in pts], fill=col, width=w, joint="curve")
# stitch ticks along the seam
for i in range(0, len(pts) - 1, 3):
    x0, y0 = pts[i]
    dx = pts[min(i + 1, len(pts) - 1)][0] - x0
    dy = pts[min(i + 1, len(pts) - 1)][1] - y0
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n, dx / n
    d.line([(x0 - nx * 9, y0 - ny * 9), (x0 + nx * 9, y0 + ny * 9)], fill=CREAM + (255,), width=3)
    d.line([(x0 - nx * 9, y0 - ny * 9), (x0 + nx * 9, y0 + ny * 9)], fill=(255, 255, 255, 90), width=1)

# rivets — small rust circles at three points along the seam
for i in (14, 52, 88):
    rx, ry = pts[i]
    rx += 46
    d.ellipse([rx - 13, ry - 13, rx + 13, ry + 13], fill=RUST + (255,), outline=INK + (255,), width=3)
    d.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=INDIGO_DARK + (255,))

# ---- specimen register: grid of small studies, right two-thirds ----
grid_x0, grid_y0 = 760, 300
cell_w, cell_h = 260, 260
gap = 26
cols, rows = 4, 6

fade_tones = [
    (18, 24, 46), (30, 40, 72), (46, 58, 98), (66, 80, 122),
    (92, 106, 148), (120, 134, 172), (150, 162, 192), (178, 188, 210),
]

idx = 1
for r in range(rows):
    for c in range(cols):
        x0 = grid_x0 + c * (cell_w + gap)
        y0 = grid_y0 + r * (cell_h + gap)
        x1, y1 = x0 + cell_w, y0 + cell_h
        tone = fade_tones[(r * cols + c) % len(fade_tones)]
        d.rectangle([x0, y0, x1, y1], outline=(40, 36, 30, 160), width=1)
        # each cell: a small weave study, alternating motif
        motif = idx % 4
        cx, cy = x0 + cell_w / 2, y0 + cell_h / 2
        if motif == 0:
            # cross-hatch swatch
            for k in range(-6, 7):
                off = k * 18
                d.line([(x0 + 14, cy + off), (x1 - 14, cy + off - 40)], fill=tone + (200,), width=2)
            for k in range(-6, 7):
                off = k * 18
                d.line([(x0 + 14, cy + off - 40), (x1 - 14, cy + off)], fill=tone + (110,), width=1)
        elif motif == 1:
            # frayed edge study — jagged bottom line
            fx = x0 + 20
            fy = cy
            fray = [(fx, fy)]
            while fx < x1 - 20:
                fx += random.uniform(6, 14)
                fy += random.uniform(-16, 16)
                fray.append((fx, fy))
            d.line(fray, fill=tone + (230,), width=3, joint="curve")
            for (fx2, fy2) in fray[::3]:
                d.line([(fx2, fy2), (fx2, fy2 + random.uniform(10, 26))], fill=tone + (150,), width=1)
        elif motif == 2:
            # stitch-density study — parallel ticks
            for k in range(10):
                sx = x0 + 24 + k * ((cell_w - 48) / 9)
                d.line([(sx, y0 + 30), (sx, y1 - 30)], fill=tone + (200,), width=2 if k % 3 else 4)
        else:
            # fiber circle — a single dyed fiber cross-section
            rr = cell_w * 0.28
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=tone + (255,), width=4)
            for a in range(0, 360, 24):
                rad = math.radians(a)
                d.line([(cx, cy), (cx + rr * math.cos(rad), cy + rr * math.sin(rad))],
                       fill=tone + (60,), width=1)
        # specimen label
        label = f"FIG.{idx:02d}  IX-{fade_tones.index(tone)+1}"
        d.text((x0 + 10, y1 - 30), label, font=mono(14), fill=(40, 36, 30, 220))
        idx += 1

# ---- header block ----
d.text((M, 56), "SEAM LEDGER", font=serif(64), fill=INK + (255,))
d.text((M, 132), "an index of continuance — cat. no. AQ / DENIM-UPCYCLE / 14.08.2026",
       font=mono(20), fill=(70, 64, 54, 255))

# right-aligned register note
note = "SPECIMEN REGISTER — 24 STUDIES\nINDIGO GRADIENT, IX-1 THROUGH IX-8\nRECORDED BY HAND"
ty = 56
for line in note.split("\n"):
    w = d.textlength(line, font=mono(16))
    d.text((W - M - w, ty), line, font=mono(16), fill=(70, 64, 54, 255))
    ty += 24

# ---- footer: measurement ledger strip ----
fy = H - M + 10
d.line([(M, fy), (W - M, fy)], fill=(40, 36, 30, 200), width=2)
ledger_items = [
    "SEAM RUN — 2.31m", "STITCH DENSITY — 6/cm", "RIVET CT. — 3",
    "DYE FADE — 62% recovered", "THREAD — undyed cotton, 40wt",
]
lx = M
for item in ledger_items:
    d.text((lx, fy + 18), item, font=mono(15), fill=(60, 54, 44, 230))
    lx += d.textlength(item, font=mono(15)) + 60

# small caption near seam base
d.text((M, H - M - 60), "nothing discarded is empty —\nthe record continues, folded into a new form.",
       font=serif(26), fill=INDIGO_DARK + (255,))

img = img.filter(ImageFilter.GaussianBlur(0.3))
img.save("/home/user/aqdesignengine/carousel_denim/companion_art/seam_ledger.png", "PNG")
print("saved", img.size)
