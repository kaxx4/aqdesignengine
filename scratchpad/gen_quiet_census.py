"""QUIET CENSUS — companion art piece for the AQ 2026 workshop carousel batch.

Every value plotted is MEASURED from the 171 source photographs (out/companion/census.json):
each plate's unoccupied-field fraction — the share of its area whose local edge energy falls
below ONE threshold fixed across the whole corpus (the pooled 45th percentile, = 17.0).

That global threshold matters. The first pass thresholded each photo at its OWN 45th percentile,
which by construction returns ~0.46 for every plate: the chart was 171 identical bars, a
tautology dressed as data. Pooling first is what lets plates actually differ (0.241–0.744).
Nothing here is decorative data.

Colour is quantity: a bar is ink up to the archive mean and the register's accent above it, so
the coloured area IS the excess emptiness. Accent therefore occupies a small, earned fraction.
"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
F = r"C:\Users\kanis\.claude\skills\canvas-design\canvas-fonts"
OUT = "out/companion"

CREAM = (244, 239, 224)
INK = (10, 10, 10)
INK_S = (10, 10, 10, 70)          # hairline / soft rule
ACCENTS = {                        # AQ brand, one per register
    "pink": (255, 77, 140), "mint": (27, 138, 90), "lemon": (255, 199, 0),
    "tomato": (255, 77, 46), "sky": (61, 169, 252), "grape": (126, 91, 255),
    "teal": (14, 124, 134), "mintbright": (0, 229, 160),
}
# Blue-green biased (user direction, 2026-08-08). Was an even spread across the wheel; now the
# cool half carries the registers. Because colour here is a QUANTITY legend, the ramp still has
# to stay mutually distinguishable — teal / sky / mint / mintbright / grape read apart at bar
# width, and one warm rung (lemon) is kept so the coolness reads as chosen, not as a cast.
ORDER = ["teal", "sky", "mint", "mintbright", "grape", "teal", "lemon"]

W, H = 2400, 3000
M = 190                            # equal margins, strictly held
SS = 2                             # supersample factor for crisp edges


def font(name, size):
    return ImageFont.truetype(os.path.join(F, name), size)


def tracked(d, xy, text, fnt, fill, track=0, anchor_right=False):
    """Letter-spaced text. Returns total width."""
    x, y = xy
    widths = [d.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + track * max(0, len(text) - 1)
    if anchor_right:
        x -= total
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=fnt, fill=fill)
        x += w + track
    return total


def hairline(d, x0, x1, y, fill=INK, wpx=1):
    d.rectangle([x0, y, x1, y + wpx - 1], fill=fill)


# ── data ──────────────────────────────────────────────────────────────────────────
rows = json.load(open(f"{OUT}/census.json"))
groups = {}
for r in rows:
    groups.setdefault(r["slug"], []).append(r["free"])
# registers ordered by population — the archive's own unevenness, not alphabetised
regs = sorted(groups.items(), key=lambda kv: -len(kv[1]))
MEAN = float(np.mean([r["free"] for r in rows]))
N = len(rows)

LABEL = {
    "disha_grammar": "BUILD-A-SENTENCE", "learners_den_art": "LEARNER'S DEN",
    "menstrual_awareness": "AWARENESS SESSION", "mothers_day": "MOTHER'S DAY CARDS",
    "valentines_cards": "VALENTINE'S CARDS", "smile_notes_bhawanipore": "SMILE NOTES / BHAWANIPORE",
    "smile_notes_laketown": "SMILE NOTES / FOOTBRIDGE", "smile_notes_mba": "SMILE NOTES / LAKE TOWN",
    "teaching_english": "CONJUNCTIONS & VERBS", "teaching_internship": "TEACHING INTERNSHIP",
}

# ── canvas ────────────────────────────────────────────────────────────────────────
im = Image.new("RGB", (W * SS, H * SS), CREAM)
d = ImageDraw.Draw(im, "RGBA")


def S(v):
    return int(round(v * SS))


f_hero = font("Italiana-Regular.ttf", S(430))
f_mono = font("GeistMono-Regular.ttf", S(19))
f_mono_b = font("GeistMono-Bold.ttf", S(19))
f_tiny = font("GeistMono-Regular.ttf", S(15))
f_reg = font("GeistMono-Bold.ttf", S(21))
f_num = font("GeistMono-Regular.ttf", S(16))
f_ser = font("Gloock-Regular.ttf", S(34))

x0, x1 = S(M), S(W - M)

# ── header ────────────────────────────────────────────────────────────────────────
hairline(d, x0, x1, S(M), INK, S(2))
tracked(d, (x0, S(M + 26)), "QUIET CENSUS", f_mono_b, INK, track=S(7))
tracked(d, (x1, S(M + 26)), "AQUATERRA · WORKSHOP ARCHIVE · MMXXVI", f_mono, INK,
        track=S(2.4), anchor_right=True)

# ── hero: the finding ─────────────────────────────────────────────────────────────
hero = f"{MEAN:.4f}".lstrip("0")          # ".4598"
hy = S(M + 92)
hw = d.textlength(hero, font=f_hero)
d.text((x0 - S(10), hy), hero, font=f_hero, fill=INK)

# annotation block sits to the right of the numeral, never touching it
ax = x0 - S(10) + hw + S(78)
ay = hy + S(150)
tracked(d, (ax, ay), "MEAN UNOCCUPIED", f_mono_b, INK, track=S(3))
tracked(d, (ax, ay + S(30)), "FIELD FRACTION", f_mono_b, INK, track=S(3))
hairline(d, ax, ax + S(300), ay + S(74), INK, S(1))
tracked(d, (ax, ay + S(90)), f"N = {N} PLATES", f_mono, (10, 10, 10), track=S(2.6))
tracked(d, (ax, ay + S(118)), "10 REGISTERS", f_mono, (10, 10, 10), track=S(2.6))

# the unit, whispered, at the far right of the hero band
tracked(d, (x1, hy + S(300)), "OF FRAME AREA", f_tiny, (10, 10, 10), track=S(3),
        anchor_right=True)

hairline(d, x0, x1, S(M + 560), INK, S(2))

# ── registers ─────────────────────────────────────────────────────────────────────
TOP = M + 640
REG_H = 192
BAR_W, GAP = 21, 11
BAR_MAX = 104
LAB_W = 470                       # label gutter; bars begin after it
bx0 = M + LAB_W

for i, (slug, vals) in enumerate(regs):
    ry = TOP + i * REG_H
    base = ry + 138                            # bar baseline
    acc = ACCENTS[ORDER[i % len(ORDER)]]

    # register label + count, in the left gutter
    tracked(d, (S(M), S(ry + 108)), LABEL.get(slug, slug.upper()), f_reg, INK, track=S(2))
    tracked(d, (S(bx0 - 40), S(ry + 110)), f"{len(vals):02d}", f_num, (10, 10, 10),
            track=0, anchor_right=True)

    # baseline rule for this register
    hairline(d, S(bx0), S(bx0 + len(vals) * (BAR_W + GAP) - GAP), S(base + 3), INK, S(1))

    # the archive mean, carried as a datum line — spanning only this register's own plates,
    # so the rule never runs on into empty margin
    my = base - MEAN * BAR_MAX * 2
    reg_end = bx0 + len(vals) * (BAR_W + GAP) - GAP
    for xd in range(S(bx0), S(reg_end), S(9)):
        d.rectangle([xd, S(my), xd + S(4), S(my)], fill=(10, 10, 10, 105))

    for j, v in enumerate(sorted(vals, reverse=True)):
        bx = bx0 + j * (BAR_W + GAP)
        h = v * BAR_MAX * 2
        top = base - h
        mean_y = base - MEAN * BAR_MAX * 2
        if v <= MEAN:
            d.rectangle([S(bx), S(top), S(bx + BAR_W), S(base)], fill=INK)
        else:
            # ink to the mean, accent for the excess — colour IS the quantity
            d.rectangle([S(bx), S(mean_y), S(bx + BAR_W), S(base)], fill=INK)
            d.rectangle([S(bx), S(top), S(bx + BAR_W), S(mean_y)], fill=acc)
        # every fifth plate gets a coordinate tick
        if j % 5 == 0:
            d.rectangle([S(bx), S(base + 9), S(bx + 1), S(base + 17)], fill=(10, 10, 10, 150))
            tracked(d, (S(bx - 1), S(base + 24)), f"{j:02d}", f_tiny, (10, 10, 10, 170))

hairline(d, x0, x1, S(TOP + 10 * REG_H + 62), INK, S(2))

# ── legend / colophon ─────────────────────────────────────────────────────────────
ly = TOP + 10 * REG_H + 100
tracked(d, (S(M), S(ly)), "INK: FIELD TO ARCHIVE MEAN", f_tiny, INK, track=S(2.6))
d.rectangle([S(M), S(ly + 34), S(M + 46), S(ly + 46)], fill=INK)
tracked(d, (S(M + 380), S(ly)), "ACCENT: EXCESS ABOVE MEAN", f_tiny, INK, track=S(2.6))
for k, name in enumerate(ORDER):
    d.rectangle([S(M + 380 + k * 54), S(ly + 34), S(M + 380 + k * 54 + 46), S(ly + 46)],
                fill=ACCENTS[name])

d.text((S(W - M), S(ly - 8)), "PLATES SORTED WITHIN REGISTER BY", font=f_tiny,
       fill=(10, 10, 10, 190), anchor="ra")
d.text((S(W - M), S(ly + 22)), "DESCENDING UNOCCUPIED FRACTION", font=f_tiny,
       fill=(10, 10, 10, 190), anchor="ra")

# the epigraph sits in the gutter between the last register and the closing rule, centred on
# the bar field rather than the page, so it reads as part of the plate and not as a caption
d.text((S(M + LAB_W + (W - M - (M + LAB_W)) / 2), S(TOP + 10 * REG_H + 14)),
       "the empty part of a picture is the part worth counting",
       font=f_ser, fill=INK, anchor="ms")

im = im.resize((W, H), Image.LANCZOS)
os.makedirs(OUT, exist_ok=True)
im.save(f"{OUT}/QUIET_CENSUS.png", dpi=(300, 300))
im.convert("RGB").save(f"{OUT}/QUIET_CENSUS.pdf", "PDF", resolution=300)
print("wrote QUIET_CENSUS.png / .pdf   mean=%.4f  N=%d" % (MEAN, N))
