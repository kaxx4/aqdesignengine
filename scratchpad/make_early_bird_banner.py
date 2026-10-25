"""Builds engine/assets/disco_diwali/early_bird_sold_out_banner.png (2026-10-22) from the user's diagonal SOLD OUT band (RGB on white).
1. the band is cut out by two fitted edge lines (angle -16.3, 738px thick), anti-aliased;
2. the old SOLD OUT lettering is removed by REPLACING each text pixel with a real band pixel from the same columns (so the grain, which
   gets coarser toward the left, is the band's own);
3. the new lettering EARLY BIRD / SOLD OUT and a small NEXT PHASE OPENS SOON are set in NeutralFace in the same off-white speckle.
Usage: python scratchpad/make_early_bird_banner.py <user banner jpg> [LINE1 LINE2 OUTFILE]   (defaults: EARLY BIRD / SOLD OUT / early_bird_sold_out_banner.png)"""
import glob, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1]; L1 = sys.argv[2] if len(sys.argv) > 2 else "EARLY BIRD"; L2 = sys.argv[3] if len(sys.argv) > 3 else "SOLD OUT"
OUT = os.path.join(ROOT, "engine/assets/disco_diwali", sys.argv[4] if len(sys.argv) > 4 else "early_bird_sold_out_banner.png")
im = np.asarray(Image.open(SRC).convert("RGB")).astype(np.uint8); H, W, _ = im.shape
PT, PB = (-0.29255, 679.39), (-0.29239, 1447.89)                 # fitted top / bottom edge: y = m x + c
yy, xx = np.mgrid[0:H, 0:W]
top, bot = PT[0] * xx + PT[1], PB[0] * xx + PB[1]
inb = (yy > top + 2) & (yy < bot - 2)
txt = inb & (im.astype(int).min(axis=2) > 150)      # near-WHITE only: pink grain specks (G up to ~140) are band, not lettering
txt = np.asarray(Image.fromarray((txt * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))) > 0   # grow over the anti-aliased rim
txt &= inb
rng = random.Random(7); out = im.copy()
for x0 in range(0, W, 8):
    cols = slice(x0, min(x0 + 8, W)); m = txt[:, cols]; n = int(m.sum())
    if n == 0: continue
    lo, hi = max(x0 - 28, 0), min(x0 + 36, W)               # a +-28 column window: a bigger pool, so no strip is tinted by its own luck
    sel = inb[:, lo:hi] & ~txt[:, lo:hi]; pool = im[:, lo:hi][sel]
    if len(pool) == 0: continue
    picks = pool[np.array([rng.randrange(len(pool)) for _ in range(n)])]
    sub = out[:, cols]; sub[m] = picks; out[:, cols] = sub
# --- lengthen the band: E px of fresh band each side (grain sampled from the end 28 columns), so a smaller scale still bleeds off both canvas edges
E = 400; W2 = W + 2 * E
big = np.full((H, W2, 3), 255, np.uint8); big[:, E:E + W] = out
yy2, xx2 = np.mgrid[0:H, 0:W2]
top2, bot2 = PT[0] * (xx2 - E) + PT[1], PB[0] * (xx2 - E) + PB[1]
band2 = (yy2 > top2 - 2) & (yy2 < bot2 + 2)           # a hair wider than the alpha edge: no white fringe
for lo, hi, src in ((0, E, slice(0, 28)), (E + W, W2, slice(W - 28, W))):
    m = band2[:, lo:hi]; n = int(m.sum()); sel = inb[:, src]; pool = im[:, src][sel]
    idx = np.array([rng.randrange(len(pool)) for _ in range(n)]); sub = big[:, lo:hi]; sub[m] = pool[idx]; big[:, lo:hi] = sub
out = big; W = W2; yy, xx = yy2, xx2; top, bot = top2, bot2
# --- new lettering, drawn UNROTATED on a strip then rotated to the band's angle -------------------------------------------
ang = np.degrees(np.arctan(PT[0]))                                # -16.3 (rises to the right)
S = 2; LW, LH = W // 1 * S, 900 * S
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
bold = [f for f in fonts if "Bold" in f or "900" in f or "Black" in f] or fonts
reg = [f for f in fonts if "Regular" in f] or fonts
def fit(fontpath, text, target_w):
    size = 100
    while True:
        f = ImageFont.truetype(fontpath, size * S); w = f.getlength(text)
        if w >= target_w * S or size > 600: return f
        size += 4
lay = Image.new("L", (LW, LH), 0); d = ImageDraw.Draw(lay)
f1 = fit(bold[-1], max((L1, L2), key=len), 1380)
l2 = L2; f2 = ImageFont.truetype(bold[-1], f1.size)
f3 = fit(reg[-1], "NEXT PHASE OPENS SOON", 620)
def centered(txt_, f, cy):
    w = f.getlength(txt_); bb = f.getbbox(txt_); h = bb[3] - bb[1]
    d.text(((LW - w) / 2 - bb[0] * 0, cy - bb[1] - h / 2), txt_, font=f, fill=255)
    return h
h1 = f1.getbbox(L1)[3] - f1.getbbox(L1)[1]
gap = 46 * S; h3 = f3.getbbox("NEXT PHASE OPENS SOON")[3] - f3.getbbox("NEXT PHASE OPENS SOON")[1]
total = h1 * 2 + gap + 62 * S + h3; y0 = LH / 2 - total / 2
centered(L1, f1, y0 + h1 / 2); centered(l2, f2, y0 + h1 + gap + h1 / 2)
centered("NEXT PHASE OPENS SOON", f3, y0 + h1 * 2 + gap + 62 * S + h3 / 2)
lay = lay.resize((LW // S, LH // S), Image.LANCZOS)
# speckle: off-white with darker grey flecks like the original lettering
rs = np.random.default_rng(3); n = rs.random((LH // S, LW // S))
fleck = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))).astype(float)
fleck = (fleck - fleck.min()) / (fleck.max() - fleck.min())
shade = 238 - 38 * (fleck > .56)                                  # 238 off-white, 200 flecks
txt_rgb = np.stack([shade, shade, shade], -1).astype(np.uint8)
ink = Image.fromarray(np.dstack([txt_rgb, np.asarray(lay)]), "RGBA")
cx = W / 2; cy = (PT[0] * (cx - E) + PT[1] + PB[0] * (cx - E) + PB[1]) / 2
ink = ink.rotate(-ang, resample=Image.BICUBIC, expand=True)       # PIL rotates counter-clockwise for positive angles
base = Image.fromarray(out).convert("RGBA")
base.alpha_composite(ink, (int(cx - ink.width / 2), int(cy - ink.height / 2)))
# --- cut the band out of the white (anti-aliased) -------------------------------------------------------------------------
a = np.clip(np.minimum(yy - top, bot - yy) + .5, 0, 1)
arr = np.asarray(base).copy(); arr[..., 3] = (a * 255).astype(np.uint8)
res = Image.fromarray(arr, "RGBA"); res.save(OUT); print("wrote", OUT, res.size)
prev = Image.new("RGB", res.size, (30, 30, 30)); prev.paste(res, mask=res.split()[3]); prev.save("/tmp/claude-0/-home-user-aqdesignengine/e1203e37-3b2e-5065-b181-a5fb91ea7d41/scratchpad/banner_preview.png")
