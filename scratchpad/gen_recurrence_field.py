"""RECURRENCE FIELD — plate 01. Companion art piece to the AQ Friendship Day carousel.

THE CONCEPT (the quiet reference): six registers of independent readings, each internally varied
in the cool blue-green family. Exactly one warm mark per register, always at the same index — so
the six pink marks align into a vertical column that is invisible in any single register and
undeniable across all of them. That column IS the carousel's repeated "WISH THEM" punch-box,
abstracted to its logic: variation across, constant down. Anyone who has seen the carousel feels
it; everyone else sees a plate from a discipline that does not exist.
"""
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle, Circle

FD = r"C:\Users\kanis\.claude\skills\canvas-design\canvas-fonts"
def F(name, size):
    return fm.FontProperties(fname=os.path.join(FD, name), size=size)

MONO   = lambda s: F("GeistMono-Regular.ttf", s)
MONOB  = lambda s: F("GeistMono-Bold.ttf", s)
SERIFI = lambda s: F("InstrumentSerif-Italic.ttf", s)

CREAM = "#F4EFE0"; INK = "#0A0A0A"
PINK  = "#FF4D8C"                                   # the invariant
FIELD = ["#3DA9FC", "#0E7C86", "#1B8A5A", "#00E5A0"]  # the variables

W, H = 1080, 1440
M = 96
OUT = "out/versions/friendship_day"

# ── registers ────────────────────────────────────────────────────────────────
N_REG, N_BAR = 6, 52
BAR_X0, BAR_X1 = 186, W - M                          # 186 .. 984
STEP = (BAR_X1 - BAR_X0) / (N_BAR - 1)
BASE0, SPACING = 372, 126                            # baseline of register I, then down
INVAR = 41                                           # the index every register shares
BW = 6.4                                             # bar width

# each register draws from its own 2-colour slice of the family, so registers read as
# tonally distinct observations rather than one repeated row
SLICES = [[0, 1], [1, 2], [0, 3], [2, 3], [1, 3], [0, 2]]
LABELS = ["R·I", "R·II", "R·III", "R·IV", "R·V", "R·VI"]

fig = plt.figure(figsize=(W / 150, H / 150), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.axis("off")
ax.add_patch(Rectangle((0, 0), W, H, facecolor=CREAM, edgecolor="none", zorder=0))

# ── the column of coincidence, drawn UNDER everything ────────────────────────
# REFINEMENT PASS: at alpha .34 this rule fused the six invariant marks into one continuous
# pink stripe — the alignment was ANNOUNCED, not discovered, which is precisely what the
# philosophy forbids. Dropped to a whisper: it guides the eye once the eye is already looking.
inv_x = BAR_X0 + INVAR * STEP
ax.plot([inv_x, inv_x], [300, BASE0 + (N_REG - 1) * SPACING + 40],
        color=PINK, lw=0.7, alpha=0.11, zorder=1, solid_capstyle="butt")

rng = np.random.default_rng(20260802)
for r in range(N_REG):
    yb = BASE0 + r * SPACING
    pal = [FIELD[i] for i in SLICES[r]]
    # baseline — the instrument rule
    ax.plot([BAR_X0 - 14, BAR_X1 + 8], [yb, yb], color=INK, lw=1.1, alpha=0.85, zorder=3)
    # register label, left column, clear of the bars
    ax.text(M, yb + 1, LABELS[r], fontproperties=MONOB(7.4), color=INK,
            ha="left", va="center", zorder=4)
    hts = rng.integers(9, 84, N_BAR)
    for i in range(N_BAR):
        x = BAR_X0 + i * STEP
        if i == INVAR:
            # the invariant runs taller AND heavier — so that once found it is unmistakable,
            # which is what lets the connecting rule stay almost invisible
            h, w = 100, BW * 1.45
            ax.add_patch(Rectangle((x - w / 2, yb - h), w, h,
                                   facecolor=PINK, edgecolor="none", zorder=6))
            ax.add_patch(Circle((x, yb - h - 8), 4.8, facecolor=PINK,
                                edgecolor=CREAM, lw=1.1, zorder=7))
        else:
            h = float(hts[i])
            ax.add_patch(Rectangle((x - BW / 2, yb - h), BW, h,
                                   facecolor=pal[i % len(pal)], edgecolor="none",
                                   alpha=0.93, zorder=5))
    # tick marks every 8th index — the instrument's own scale
    for i in range(0, N_BAR, 8):
        x = BAR_X0 + i * STEP
        ax.plot([x, x], [yb + 3, yb + 8], color=INK, lw=0.7, alpha=0.4, zorder=4)

# ── header ───────────────────────────────────────────────────────────────────
ax.text(M, 138, "RECURRENCE FIELD", fontproperties=MONOB(14.5), color=INK,
        ha="left", va="baseline", zorder=8)
ax.plot([M, M + 168], [156, 156], color=PINK, lw=2.2, zorder=8, solid_capstyle="butt")
ax.text(M, 186, "PLATE 01  ·  SIX REGISTERS, ONE INVARIANT",
        fontproperties=MONO(6.6), color=INK, alpha=0.55, ha="left", va="baseline", zorder=8)
ax.text(W - M, 138, "AQ / 02.08.26", fontproperties=MONO(6.6), color=INK,
        alpha=0.55, ha="right", va="baseline", zorder=8)
ax.text(W - M, 186, "OBS. 0.5× / 40KM / REEL / LAUGH / DOOR / SILENCE",
        fontproperties=MONO(5.4), color=INK, alpha=0.38, ha="right", va="baseline", zorder=8)
ax.plot([M, W - M], [232, 232], color=INK, lw=0.8, alpha=0.5, zorder=8)

# REFINEMENT: the per-register readout was identical on all six rows — pure redundancy, which
# the philosophy explicitly forbids. Stated ONCE, under the final baseline, as an axis note.
last_y = BASE0 + (N_REG - 1) * SPACING
ax.text(BAR_X1, last_y + 26, f"n = {N_BAR} readings per register",
        fontproperties=MONO(5.8), color=INK, alpha=0.4, ha="right", va="center", zorder=4)

# ── footer: the one permitted departure ──────────────────────────────────────
fy = last_y + 112
ax.plot([M, W - M], [fy, fy], color=INK, lw=0.8, alpha=0.5, zorder=8)
ax.text(M, fy + 62, "the constant is not the sentiment.",
        fontproperties=SERIFI(25), color=INK, ha="left", va="baseline", zorder=8)
ax.text(M, fy + 100, "it is the return.",
        fontproperties=SERIFI(25), color=PINK, ha="left", va="baseline", zorder=8)

# REFINEMENT: the legend's three swatches were near-identical blues, so the key failed to key
# anything. Each now states its own kind — the field as its actual four-colour set, the
# invariant as the single heavy mark, the reading as an ink hairline (a direction, not a colour).
ly = fy + 154
rows = [("field", "FIELD  —  variable, cool register"),
        ("inv",   "INVARIANT  —  fixed index, every register, without exception"),
        ("rule",  "READING  —  vertical coincidence is legible only across all six")]
for i, (kind, txt) in enumerate(rows):
    y = ly + i * 22
    if kind == "field":
        for j, c in enumerate(FIELD):
            ax.add_patch(Rectangle((M + j * 6.0, y - 6.5), 4.2, 7,
                                   facecolor=c, edgecolor="none", alpha=0.93, zorder=8))
    elif kind == "inv":
        ax.add_patch(Rectangle((M, y - 8.5), 6.1, 9, facecolor=PINK, edgecolor="none", zorder=8))
    else:
        ax.plot([M, M + 22], [y - 3, y - 3], color=INK, lw=0.8, alpha=0.5, zorder=8)
    ax.text(M + 40, y, txt, fontproperties=MONO(6.0), color=INK, alpha=0.62,
            ha="left", va="baseline", zorder=8)

ax.text(W - M, ly + 44, f"FIG. 1  ·  INVARIANT AT n = {INVAR + 1:02d} / {N_BAR}",
        fontproperties=MONO(6.0), color=INK, alpha=0.5, ha="right", va="baseline", zorder=8)

# ── grain: the ground is handled paper, never flat ───────────────────────────
g = np.random.default_rng(7).normal(0.5, 0.5, (300, 225))
ax.imshow(g, extent=[0, W, H, 0], cmap="gray", alpha=0.035, aspect="auto",
          zorder=9, interpolation="bilinear")

os.makedirs(OUT, exist_ok=True)
fig.savefig(f"{OUT}/RECURRENCE_FIELD.pdf", facecolor=CREAM)
fig.savefig(f"{OUT}/RECURRENCE_FIELD.png", facecolor=CREAM, dpi=220)
print("wrote RECURRENCE_FIELD.pdf + .png")
