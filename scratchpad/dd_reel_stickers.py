"""DISCO DIWALI reel covers, STICKERS + PHOTO ONLY (2026-10-21; user: "dont write disco diwali, i just want stickers and photo").

Fifteen 1080x1920 covers: one real event photo each (same crops as dd_reel_covers.py), lightly graded, and copper stickers as the only
foreground, ONE IN EACH OF THE FOUR CORNERS of the grid-safe frame (user: "place them on the 4 corners", not scattered), rotating by one step per cover; the corners are the EXTREME canvas corners.
No lockup, hook, badge or text. Stickers: the copper mask, heart, star and diya (calendar and pin
are left out: they imply a date and a venue that covers do not state). Gold dust and film grain stay on as the format's texture.
Stickers sit on the extreme canvas corners, outside the profile-grid crop.
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
# SET 2 (2026-10-21, "create 5 more"): the five remaining stills, numbered 16..20 so the corner rotation continues. Run with SET=2.
PHOTOS2 = [(f"{LIB}/05_cards-hall-dance-green-light.jpg", .50), (f"{LIB}/07_dance-blur-blue-light.jpg", .50),
           (f"{LIB}/08_cards-hall-crowd-purple.jpg", .50), (f"{LIB}/09_night-courtyard-string-lights-crowd.jpg", .50),
           (f"{LIB}/01_IMG_7180_group-aquaterra-banner.jpg", .50)]
SET2 = os.environ.get("SET") == "2"
START = 16 if SET2 else 1
if SET2:
    PHOTOS = PHOTOS2
# sticker files and the aspect (h/w) of the VISIBLE art; the mask asset has transparent padding, handled in place()
FILES = {"mask": (os.path.join(ASSET, "mask_copper.png"), 920 / 1400), "heart": (os.path.join(STK, "copper_heart.png"), 1324 / 1496),
         "star": (os.path.join(STK, "copper_star.png"), 1.0), "diya": (os.path.join(STK, "copper_diya.png"), 1146 / 1870)}
# EXTREME CORNERS (user, 2026-10-21: "i want the stickers to be on the extreme corners"): one sticker hugging each corner of the CANVAS, 26px
# from both edges, one of each kind per cover, rotating by one corner per cover. This puts them OUTSIDE Instagram's profile-grid crop (3:4 centre,
# y 240..1680), so the grid thumbnail shows the photo alone; the full reel cover shows all four. The user chose this knowingly.
CORNERS = [(0, 0, -8), (1, 0, 8), (0, 1, 7), (1, 1, -7)]       # TL, TR, BL, BR: right?, bottom?, tilt
MARGIN = 26
KINDS = ["mask", "heart", "star", "diya"]
WIDTH = {"mask": 440, "heart": 340, "star": 330, "diya": 400}
SAFE_TOP, SAFE_BOT = 285, 1635

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
    arr = []
    for c, (right, bottom, rot) in enumerate(CORNERS):
        kind = KINDS[(c + i) % 4]; vw = WIDTH[kind]; vh = vw * FILES[kind][1]
        r = math.radians(abs(rot)); bw = vw * math.cos(r) + vh * math.sin(r); bh = vw * math.sin(r) + vh * math.cos(r)   # rotated footprint
        cx = W - MARGIN - bw / 2 if right else MARGIN + bw / 2
        cy = H - MARGIN - bh / 2 if bottom else MARGIN + bh / 2
        arr.append((kind, vw, round(cx), round(cy), rot))
    P, E = [f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
            f'<img data-tag="photo" src="{photo169(photo, fx)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1;'
            f'filter:contrast(1.08) saturate(1.05) brightness(1.0)">',
            '<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(8,6,30,.30) 0%,rgba(8,6,30,0) 22%,'
            'rgba(0,0,0,0) 70%,rgba(0,0,0,.34) 100%)"></div>'], []
    for n, (kind, vw, cx, cy, rot) in enumerate(arr):
        html, box = place(kind, vw, cx, cy, rot)
        P.append(html); E.append((f"s{n}_{kind}",) + box)
    P.append(f'<img src="{dd.uri("sparkles.png")}" data-tag="sparkles" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:14;mix-blend-mode:screen;object-fit:cover">')
    P.append(f'<img src="{dd.uri("grain.png")}" data-tag="grain" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:15;mix-blend-mode:screen;object-fit:cover;opacity:.9">')
    return P, E

async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "reels_stickers_2" if SET2 else "reels_stickers"); os.makedirs(out, exist_ok=True)
    async with B.session():
        for i, (photo, fx) in enumerate(PHOTOS, START):
            P, E = build(i, photo, fx)
            for lab, x, y, w, h in E:
                assert x >= 0 and x + w <= W and y >= 0 and y + h <= H, f"cover {i}: {lab} leaves the canvas ({x},{y},{w},{h})"
            html = B.page(W, H, GROUND, "".join(P), grain=False)
            await B.render(html, os.path.join(out, f"reel_{i:02d}.png"), W, H, elements=E,
                           bleed_tags=("plate", "sparkles", "grain", "photo", "sticker"), crop_tags=("plate", "sparkles", "grain", "photo"), page_bg=GROUND)
    ims = [Image.open(os.path.join(out, f"reel_{i:02d}.png")).convert("RGB") for i in range(START, START + len(PHOTOS))]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 3 + 20), (40, 40, 40)); gp = Image.new("RGB", (360 * 5 + 40, 480 * 3 + 20), (20, 20, 20))
    for i, im in enumerate(ims):
        s = im.width / W
        sh.paste(im.resize((324, 576), Image.LANCZOS), ((i % 5) * 334, (i // 5) * 586))
        gp.paste(im.crop((0, round(240 * s), im.width, round(1680 * s))).resize((360, 480), Image.LANCZOS), ((i % 5) * 370, (i // 5) * 490))
    sh.save(os.path.join(out, "sheet.png")); gp.save(os.path.join(out, "grid_preview.png"))
    print("sticker reel covers done ->", out)
asyncio.run(main())
