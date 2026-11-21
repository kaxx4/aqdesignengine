"""AQ EVENTS TEAM recruitment stories for STARRY NIGHT, one per user photo, 1080x1920, AQ house style. Same design as scratchpad/aq_starry_recruit_photo.py (the DJ-decks story), generalised.

THE DESIGN IS FIXED, THE GROUND IS NOT: headline stack, sky chips/blocks, lemon serif 'starry', moon + stars, handle top right, a reserved clear 640x165 `linkzone` for Instagram's link sticker (NO pill, NO 'link in bio':
user, 2026-11-21). Per photo only the crop anchor, base scrim and lift change.
CONTRAST IS SOLVED, NOT TUNED: the layout is computed FIRST from measured type, then for every text box the lightest navy-black scrim that clears its WCAG floor with 1.55x headroom is solved against the REAL
photo pixels under that box (97th-percentile brightest pixel, the worst case for light type), plateaued over the box and eased out over 120px, and merged with the photo's own base scrim. Text colour is then picked
from cream/white/ink by measured ratio and printed as a receipt; lemon 'starry' is asserted too. A photo that cannot be made legible below alpha .9 stops the build instead of shipping.
Facts: Starry Night = the Christmas carnival fundraiser; edition, date, venue, roles, deadline, link NOT supplied and not printed.
Photos (consent unconfirmed: all three show guests, several apparent minors): A crowd under star lights (user, pasted), B photobooth strips 'Starry Night 2.0 / All for charity' (user, pasted), C crowd under net + star lights (user HEIC).
Run: PYTHONIOENCODING=utf-8 python scratchpad/aq_starry_recruit_photos.py [a|b|c ...]   -> out/aq_events/starry_recruit_{a,b,c}.png"""
import asyncio, base64, io, os, sys, importlib.util
import numpy as np
from PIL import Image
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
W, H = core.SIZES["story"]; M = 64
INK, CREAM = core.INK, core.CREAM
SKY = core.accent_for("events"); LEMON = core.ACCENTS[2]
EDGE = core.outline_of("#101010")
D = "engine/assets/img/events/starry-night-2026-11/"
SCRIM_RGB = np.array([6, 5, 24.])
# per-photo: file, crop anchor x (0..1), lift, base scrim stops (y, alpha), y of the lower block
PHOTOS = {
    "a": dict(file="crowd_star_lights.jpg", ax=.5, lift=1.35, base=[(0, .30), (1000, .22), (1920, .50)], ly=1105),
    "b": dict(file="photobooth_strips.jpg", ax=.5, lift=1.0, base=[(0, .40), (900, .28), (1920, .55)], ly=1105),
    "c": dict(file="photo_c.jpg", ax=.5, lift=1.0, base=[(0, .42), (900, .26), (1920, .60)], ly=1105),
}
HEADROOM = 1.55; PCT = 97
def lin(c): c = c / 255.0; return np.where(c <= .04045, c / 12.92, ((c + .055) / 1.055) ** 2.4)
def lum_arr(rgb): l = lin(rgb); return .2126 * l[..., 0] + .7152 * l[..., 1] + .0722 * l[..., 2]
def lum1(rgb): return float(lum_arr(np.array(rgb, float)))
def ratio1(a, b): la, lb = sorted((lum1(a), lum1(b)), reverse=True); return (la + .05) / (lb + .05)
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
CHOICES = {"cream": hexrgb(CREAM), "white": (255, 255, 255), "ink": hexrgb(INK)}
hexof = lambda n: {"cream": CREAM, "white": "#FFFFFF", "ink": INK}[n]

def load_photo(cfg):
    im = Image.open(D + cfg["file"]).convert("RGB"); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    left = round((im.width - W) * cfg["ax"]); top = (im.height - H) // 2
    return np.asarray(im.crop((left, top, left + W, top + H))).astype(float) * cfg["lift"]

def solve_scrim(arr, cfg, boxes):
    """boxes: (label, x, y, w, h, floor, colour_rgb). Returns the alpha profile (H,) and per-box solved alpha."""
    prof = np.interp(np.arange(H), [p[0] for p in cfg["base"]], [p[1] for p in cfg["base"]])
    solved = {}
    for label, x, y, w, h, floor, col in boxes:
        reg = arr[max(0, int(y)):int(y + h), max(0, int(x)):int(x + w)].reshape(-1, 3)[::5]
        need = floor * HEADROOM; lo, hi = 0.0, .9
        def ok(a):
            L = lum_arr(reg * (1 - a) + SCRIM_RGB * a); bg = np.percentile(L, PCT); lt = lum1(col)
            return (max(lt, bg) + .05) / (min(lt, bg) + .05) >= need
        if not ok(hi): raise SystemExit(f"{label}: cannot reach {need:.1f}:1 even at alpha .9 (photo too bright under the box)")
        for _ in range(14):
            mid = (lo + hi) / 2
            if ok(mid): hi = mid
            else: lo = mid
        a = round(hi + .02, 3); solved[label] = a
        ys = np.arange(H); y0, y1 = y - 30, y + h + 30
        ramp = np.clip(np.minimum((ys - (y0 - 120)) / 120, ((y1 + 120) - ys) / 120), 0, 1) * a
        prof = np.maximum(prof, np.where((ys >= y0) & (ys <= y1), a, ramp))
    return np.clip(prof, 0, .9), solved

async def build(key):
    cfg = PHOTOS[key]; arr = load_photo(cfg); els = []
    def box(label, x, y, w, h, html, z=10):
        els.append((label, round(x), round(y), round(w), round(h)))
        return f'<div data-tag="{label}" style="position:absolute;left:{round(x)}px;top:{round(y)}px;width:{round(w)}px;height:{round(h)}px;z-index:{z}">{html}</div>'
    async with B.session():
        probe = await B.measure_text([{"text": "EVENTS", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"}, {"text": "TEAM", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "NIGHT", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"}, {"text": "starry", "font": "s", "size": 100, "weight": 400}], W, H)
        ev100, team100, night100, star100 = (p["text_w"] for p in probe)
        ev_size = 100 * (W - 2 * M - 14) / ev100; night_size = 100 * 540 / night100; starry_size = 100 * 370 / star100
        sz = await B.measure_text([{"text": "JOIN THE", "font": "d", "size": 92, "weight": 900, "transform": "uppercase", "line_height": .9},
                                   {"text": "EVENTS", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "TEAM", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "NIGHT", "font": "d", "size": night_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "starry", "font": "s", "size": starry_size, "weight": 400, "line_height": .9}], W, H)
        join_h, ev_h, team_h, night_h, starry_h = (z["ink_h"] for z in sz); join_w = sz[0]["text_w"]; team_w = sz[2]["text_w"]; night_w = sz[3]["text_w"]
        # ---------- 1. LAYOUT FIRST (depends only on measured type) ----------
        y_join = 214; y_ev = y_join + join_h + 14; y_team = y_ev + ev_h + 30; bw, bh = team_w + 80, team_h + 44
        sx = M + bw + 36; y_sub = y_team + bh / 2 - 60
        ly = cfg["ly"]; y_night = ly + starry_h + 6; y_label = y_night + night_h + 26
        zx, zy, zw, zh = (W - 640) // 2, 1505, 640, 165
        assert y_label + 24 < zy, f"label ends {y_label + 24}, link zone starts {zy}"
        text_boxes = [("join", M, y_join, join_w, join_h, 3.0, CHOICES["cream"]), ("events", M, y_ev, W - 2 * M, ev_h, 3.0, CHOICES["cream"]),
                      ("sub", sx, y_sub, W - M - sx, 120, 4.5, CHOICES["cream"]), ("starry", M, ly, 380, starry_h, 3.0, hexrgb(LEMON)),
                      ("night", M, y_night, night_w, night_h, 3.0, CHOICES["cream"]), ("label", M, y_label, 470, 24, 4.5, CHOICES["cream"]),
                      ("handle", W - M - 215, 62, 215, 30, 4.5, CHOICES["cream"])]
        # ---------- 2. SOLVE THE SCRIM against the real photo pixels, then build the background ----------
        prof, solved = solve_scrim(arr, cfg, text_boxes)
        bg = arr * (1 - prof[:, None, None]) + SCRIM_RGB[None, None, :] * prof[:, None, None]
        bg_img = Image.fromarray(bg.clip(0, 255).astype("uint8")); buf = io.BytesIO(); bg_img.save(buf, "JPEG", quality=92)
        BG_URI = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
        receipt = []
        def pick(label, x, y, w, h, floor):
            reg = bg[max(0, int(y)):int(y + h), max(0, int(x)):int(x + w)].reshape(-1, 3)[::5]
            L = lum_arr(reg); bgc = tuple(int(v) for v in reg[np.argsort(L)[int(len(L) * PCT / 100) - 1]])
            for name in ("cream", "white", "ink"):
                if name == "ink": continue                        # on these dark grounds ink never wins; kept out so the receipt is about light type
                r = ratio1(CHOICES[name], bgc)
                if r >= floor: receipt.append((label, name, round(r, 2), floor, "#%02x%02x%02x" % bgc, solved.get(label))); return name, "#%02x%02x%02x" % bgc
            raise SystemExit(f"{label}: no light colour clears {floor}:1 over {bgc}")
        parts = [f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:34px;z-index:20;filter:drop-shadow(0 2px 6px rgba(0,0,0,.7))">']; els.append(("logo", M, 56, 160, 34))
        parts.append(box("eyebrow", M, 128, 290, 48, f'<div style="width:100%;height:100%;background:{SKY};border:3px solid {INK};border-radius:999px;box-shadow:4px 4px 0 {EDGE};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;color:{INK};white-space:nowrap">NOW RECRUITING</div>', z=12))
        jc, _ = pick("join", M, y_join, join_w, join_h, 3.0)
        parts.append(box("join", M, y_join, join_w + 10, join_h, f'<div style="font-family:var(--d);font-weight:900;font-size:92px;line-height:.9;text-transform:uppercase;color:{hexof(jc)};white-space:nowrap">JOIN THE</div>'))
        ec, _ = pick("events", M, y_ev, W - 2 * M, ev_h, 3.0)
        parts.append(box("events", M - 4, y_ev, W - 2 * M + 8, ev_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{hexof(ec)};text-shadow:7px 7px 0 {SKY};white-space:nowrap">EVENTS</div>'))
        parts.append(box("team", M, y_team, bw, bh, f'<div style="width:100%;height:100%;background:{SKY};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;box-shadow:9px 9px 0 {EDGE};box-sizing:border-box;'
                         f'display:flex;align-items:center;justify-content:center"><span style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{INK}">TEAM</span></div>', z=11))
        sc, _ = pick("sub", sx, y_sub, W - M - sx, 120, 4.5)
        parts.append(box("sub", sx, y_sub, W - M - sx, 120, f'<div style="font-family:var(--e);font-weight:600;font-size:34px;line-height:1.18;color:{hexof(sc)};text-shadow:0 2px 10px rgba(0,0,0,.55)">come run<br>the night<br>with us</div>'))
        parts.append(box("starry", M, ly, 560, starry_h, f'<div style="font-family:var(--s);font-style:italic;font-size:{starry_size:.0f}px;line-height:.9;color:{LEMON};white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.55)">starry</div>'))
        # lemon is a fixed colour, so assert it rather than pick it
        reg = bg[int(ly):int(ly + starry_h), M:M + 380].reshape(-1, 3)[::5]; lb = reg[np.argsort(lum_arr(reg))[int(len(reg) * PCT / 100) - 1]]
        rl = round(ratio1(hexrgb(LEMON), lb), 2); assert rl >= 3.0, f"starry lemon {rl}:1"; receipt.append(("starry", "lemon", rl, 3.0, "#%02x%02x%02x" % tuple(int(v) for v in lb), solved.get("starry")))
        nc, _ = pick("night", M, y_night, night_w, night_h, 3.0)
        parts.append(box("night", M - 4, y_night, 700, night_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{night_size:.0f}px;line-height:.86;text-transform:uppercase;color:{hexof(nc)};text-shadow:6px 6px 0 {SKY};white-space:nowrap">NIGHT</div>'))
        lc, _ = pick("label", M, y_label, 470, 24, 4.5)
        parts.append(box("label", M, y_label, 560, 24, f'<div style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.12em;color:{hexof(lc)};white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,.6)">THE CHRISTMAS CARNIVAL FUNDRAISER</div>'))
        ms = 150; mx, my = 800, ly - 4
        parts.append(box("moon", mx, my, ms, ms, f'<svg viewBox="0 0 100 100" width="{ms}" height="{ms}" style="display:block;overflow:visible"><defs><mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="68" cy="38" r="38" fill="#000"/></mask></defs>'
                         f'<circle cx="50" cy="50" r="46" fill="{LEMON}" stroke="{INK}" stroke-width="3.5" mask="url(#mm)" transform="rotate(-18 50 50)"/></svg>', z=15))
        for i, (kx, ky, ks, kr) in enumerate(((620, ly + 40, 62, -10), (940, ly + 190, 78, 12), (800, ly + 225, 48, 6))):
            parts.append(box(f"dd_star{i}", kx, ky, ks, ks, dd.stamp("star", LEMON, rot=kr, style="clean"), z=14))
        hc, _ = pick("handle", W - M - 215, 62, 215, 30, 4.5)
        parts.append(box("handle", W - M - 300, 62, 300, 30, f'<div style="font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.05em;color:{hexof(hc)};text-align:right;text-shadow:0 2px 8px rgba(0,0,0,.6)">@ngo.aquaterra</div>'))
        els.append(("linkzone", zx, zy, zw, zh))       # reserved clear for Instagram's link sticker; ends 250px above the bottom edge
        print(f"\n[{key}] TEXT-COLOUR RECEIPT (97th-pct backing pixel; scrim alpha solved per box)\n{'label':8} {'colour':6} {'ratio':>6} {'floor':>5} {'alpha':>6}  backing")
        for r in receipt: print(f"{r[0]:8} {r[1]:6} {r[2]:>6} {r[3]:>5} {str(r[5]):>6}  {r[4]}")
        inner = f'<img data-tag="plate" src="{BG_URI}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:0">' + "".join(parts)
        html = B.page(W, H, "#000", inner, grain=False)
        tp = [("eyebrow", INK, SKY, 18, True), ("team", INK, SKY, 200, True)] + [(r[0], {"cream": CREAM, "white": "#FFFFFF", "lemon": LEMON}[r[1]], r[4], 17 if r[0] == "label" else 34, r[0] != "sub") for r in receipt]
        os.makedirs("out/aq_events", exist_ok=True)
        await B.render(html, f"out/aq_events/starry_recruit_{key}.png", W, H, elements=els, text_pairs=tp, bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000",
                       collision_ignore=[("team", "events"), ("team", "sub"), ("starry", "moon")])

async def main():
    for k in (sys.argv[1:] or list(PHOTOS)): await build(k)
asyncio.run(main())
