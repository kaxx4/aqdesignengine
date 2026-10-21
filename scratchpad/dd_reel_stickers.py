"""DISCO DIWALI reel covers, STICKERS + PHOTO ONLY (2026-10-21; user: "dont write disco diwali, i just want stickers and photo").

Fifteen 1080x1920 covers: one real event photo each (same crops as dd_reel_covers.py), lightly graded, and copper stickers as the only
foreground. No lockup, no hook, no badge, no text at all. Each cover has one large hero sticker and two small ones; four arrangements cycle
and every other block of four is mirrored so neighbours in the grid differ. Stickers: the copper mask, heart, star and diya (calendar and pin
are left out: they imply a date and a venue that covers do not state). Gold dust and film grain stay on as the format's texture.
Everything sits inside y 285..1635, the 4:5 profile-grid crop of a 1080x1920 cover (the 3:4 crop is wider).
CONSENT: many people in these photos look like minors and no consent record exists. Check before posting.

Outputs out/discodiwali/reels_stickers/reel_NN.png (+ sheet.png, grid_preview.png).   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_reel_stickers.py
"""
import asyncio, base64, importlib.util, io, math, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND = dd.B, dd.GROUND
W, H = 1080, 1920
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
LIB = os.path.join(ROOT, "engine", "assets", "img", "events", "unsorted-2026-10-07")
ASSET = os.path.join(ROOT, "engine", "assets", "disco_diwali")
STK = os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers")
# (photo, x-centre fraction of the 9:16 crop)
PHOTOS = [(f"{HALL}/04_pink-ceiling-chandelier-phone.jpg", .55), (f"{HALL}/05_boys-crowd-green-light.jpg", .50),
          (f"{HALL}/03_girls-dancing-yellow-top.jpg", .55), (f"{HALL}/01_dancers-silver-pillar-purple.jpg", .45),
          (f"{LIB}/06_three-friends-fairy-lights.jpg", .60), (f"{HALL}/06_blue-room-crowd-faces.jpg", .60),
          (f"{HALL}/07_pink-glare-girls-backs-phone.jpg", .45), (f"{HALL}/08_boy-on-shoulders-stage-lights-portrait.jpg", .55),
          (f"{HALL}/09_boy-on-shoulders-star-balloon.jpg", .42), (f"{LIB}/03_IMG_1451_red-drapes-entrance.jpg", .50),
          (f"{LIB}/10_disco-diwali-photo-booth.jpg", .55), (f"{LIB}/11_dance-green-light-portrait.jpg", .50),
          (f"{LIB}/13_IMG_1500_dance-pink-light-phone.jpg", .50), (f"{HALL}/02_crowd-teal-kurta-purple.jpg", .52),
          (f"{LIB}/02_IMG_7028_group-pink-balloons.jpg", .50)]
# sticker files and the aspect (h/w) of the VISIBLE art; the mask asset has transparent padding, handled in place()
FILES = {"mask": (os.path.join(ASSET, "mask_copper.png"), 920 / 1400), "heart": (os.path.join(STK, "copper_heart.png"), 1324 / 1496),
         "star": (os.path.join(STK, "copper_star.png"), 1.0), "diya": (os.path.join(STK, "copper_diya.png"), 1146 / 1870)}
# arrangements: (kind, visible width, centre x, centre y, rotation). First entry is the hero. Safe zone y 330..1590.
ARR = [[("mask", 640, 540, 930, -8), ("star", 230, 175, 520, 10), ("heart", 250, 900, 1370, -10)],
       [("heart", 540, 540, 900, 7), ("diya", 330, 215, 1380, -8), ("star", 220, 890, 500, 12)],
       [("star", 560, 540, 960, 0), ("mask", 400, 285, 520, -12), ("diya", 320, 850, 1400, 6)],
       [("diya", 660, 540, 980, -5), ("heart", 260, 880, 520, 9), ("star", 210, 190, 1380, -6)]]
SAFE_TOP, SAFE_BOT = 285, 1635
# Covers whose cycle arrangement would land on faces (found by looking at the sheet): literal arrangements, never mirrored. Hero goes to a
# ceiling or to clothing, smalls to dark or empty corners.
OVR = {2: [("heart", 440, 540, 545, 7), ("diya", 300, 870, 1420, -8), ("star", 200, 880, 1160, 12)],
       5: [("mask", 560, 540, 1400, -6), ("star", 230, 175, 520, 10), ("heart", 250, 900, 560, -10)],
       6: [("heart", 420, 540, 540, 7), ("diya", 300, 860, 1430, -8), ("star", 200, 880, 1190, 12)],
       8: [("diya", 540, 540, 500, -5), ("heart", 240, 200, 1420, 9), ("star", 210, 880, 1400, -6)],
       10: [("heart", 440, 540, 545, 7), ("diya", 330, 215, 1420, -8), ("star", 200, 540, 1480, 12)],
       11: [("star", 380, 540, 520, 0), ("mask", 280, 205, 560, -12), ("diya", 280, 910, 540, 6)],
       12: [("diya", 520, 540, 520, -5), ("heart", 260, 880, 1380, 9), ("star", 210, 190, 1380, -6)],
       14: [("heart", 420, 820, 600, -7), ("diya", 300, 190, 1420, 8), ("star", 210, 190, 520, -12)],
       15: [("star", 380, 540, 520, 0), ("mask", 300, 215, 560, -12), ("diya", 280, 900, 540, 6)]}

def photo169(path, fx):
    im = Image.open(path).convert("RGB"); w, h = im.size
    cw, ch = (w, round(w * 16 / 9)) if w / h < 9 / 16 else (round(h * 9 / 16), h)
    x0 = min(max(round(fx * w - cw / 2), 0), w - cw); y0 = (h - ch) // 2
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

_u = {}
def uri(path):
    if path not in _u:
        _u[path] = "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
    return _u[path]

def place(kind, vw, cx, cy, rot):
    """Return (html, declared box) for a sticker of visible width vw centred on cx,cy. The mask asset carries padding around its art
    (art spans x157..1557, y211..1131 of 1680x1278), so it is sized from the art, not the file."""
    path, asp = FILES[kind]
    vh = vw * asp
    if kind == "mask":
        k = vw / 1400
        iw, ih = 1680 * k, 1278 * k
        left = cx - (157 + 700) * k; top = cy - (211 + 460) * k
    else:
        iw, ih = vw, vh; left, top = cx - vw / 2, cy - vh / 2
    html = (f'<img data-tag="sticker" src="{uri(path)}" style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{iw:.0f}px;height:{ih:.0f}px;'
            f'z-index:6;transform:rotate({rot}deg);filter:drop-shadow(0 12px 30px rgba(0,0,0,.55))">')
    r = math.radians(abs(rot)); bw = vw * math.cos(r) + vh * math.sin(r); bh = vw * math.sin(r) + vh * math.cos(r)   # rotated footprint
    return html, (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))

def build(i, photo, fx):
    arr = OVR.get(i) or ARR[(i - 1) % 4]; mirror = i not in OVR and ((i - 1) // 4) % 2 == 1
    P, E = [f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
            f'<img data-tag="photo" src="{photo169(photo, fx)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1;'
            f'filter:contrast(1.08) saturate(1.05) brightness(1.0)">',
            '<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(8,6,30,.30) 0%,rgba(8,6,30,0) 22%,'
            'rgba(0,0,0,0) 70%,rgba(0,0,0,.34) 100%)"></div>'], []
    for n, (kind, vw, cx, cy, rot) in enumerate(arr):
        if mirror:
            cx, rot = W - cx, -rot
        html, box = place(kind, vw, cx, cy, rot)
        P.append(html); E.append((f"s{n}_{kind}",) + box)
    P.append(f'<img src="{dd.uri("sparkles.png")}" data-tag="sparkles" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:14;mix-blend-mode:screen;object-fit:cover">')
    P.append(f'<img src="{dd.uri("grain.png")}" data-tag="grain" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:15;mix-blend-mode:screen;object-fit:cover;opacity:.9">')
    return P, E

async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "reels_stickers"); os.makedirs(out, exist_ok=True)
    async with B.session():
        for i, (photo, fx) in enumerate(PHOTOS, 1):
            P, E = build(i, photo, fx)
            for lab, x, y, w, h in E:
                assert x >= 0 and x + w <= W and y >= SAFE_TOP and y + h <= SAFE_BOT, f"cover {i}: {lab} leaves the safe zone ({x},{y},{w},{h})"
            html = B.page(W, H, GROUND, "".join(P), grain=False)
            await B.render(html, os.path.join(out, f"reel_{i:02d}.png"), W, H, elements=E,
                           bleed_tags=("plate", "sparkles", "grain", "photo"), crop_tags=("plate", "sparkles", "grain", "photo"), page_bg=GROUND)
    ims = [Image.open(os.path.join(out, f"reel_{i:02d}.png")).convert("RGB") for i in range(1, len(PHOTOS) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 3 + 20), (40, 40, 40)); gp = Image.new("RGB", (360 * 5 + 40, 480 * 3 + 20), (20, 20, 20))
    for i, im in enumerate(ims):
        s = im.width / W
        sh.paste(im.resize((324, 576), Image.LANCZOS), ((i % 5) * 334, (i // 5) * 586))
        gp.paste(im.crop((0, round(240 * s), im.width, round(1680 * s))).resize((360, 480), Image.LANCZOS), ((i % 5) * 370, (i // 5) * 490))
    sh.save(os.path.join(out, "sheet.png")); gp.save(os.path.join(out, "grid_preview.png"))
    print("sticker reel covers done ->", out)
asyncio.run(main())
