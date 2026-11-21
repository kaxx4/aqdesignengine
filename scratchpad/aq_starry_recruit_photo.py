"""AQ EVENTS TEAM recruitment story for STARRY NIGHT, photo ground (user photo: DJ decks, hands only, no faces), 1080x1920, AQ house style.

Workflow C build, photo variant of scratchpad/aq_starry_recruit.py (same copy, same facts). The ground is the user's photograph, not cream: the user asked for it, and AQ's real-photo
pieces (CAROUSEL_PLAYBOOK) are dark-scrimmed photos with bare logo, accent chips and hard-shadowed type. Adaptations: palette is the photo + scrim, events sky (core.accent_for('events')) for chips/blocks,
lemon for the moon and stars (cream ground rule does not apply on a photo ground). Craft outline/shadow colour is core.outline_of(surface), not ink (an ink shadow vanishes on this ground).
TEXT COLOUR IS MEASURED, NOT ASSUMED (user: 'texts according to the contrast of the background picture'): the scrimmed background is rebuilt in numpy exactly as the CSS paints it, each text box is sampled at its
BRIGHTEST 95th-percentile pixel (worst case for light type), and the type colour is picked from cream/white/ink by measured WCAG ratio; the table is printed and asserted. No facts beyond the earlier poster:
Starry Night = the Christmas carnival fundraiser. Edition, date, venue, roles, deadline, link are NOT supplied; The CTA slot reads LINK HERE (user, 2026-11-21): it is an empty pill sized for an Instagram link sticker, to be covered with the form link when posted.
Run: PYTHONIOENCODING=utf-8 python scratchpad/aq_starry_recruit_photo.py"""
import asyncio, base64, io, os, sys, importlib.util
import numpy as np
from PIL import Image
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = core.SIZES["story"]; M = 64
INK, CREAM = core.INK, core.CREAM
SKY = core.accent_for("events"); LEMON = core.ACCENTS[2]
EDGE = core.outline_of("#101010")                  # the craft outline colour on this dark ground (cream)
PHOTO = "engine/assets/img/events/starry-night-2026-11/dj_decks.jpg"
SCRIM = [(0, .68), (480, .50), (760, .26), (1010, .08), (1230, .40), (1500, .64), (1920, .84)]   # (y, alpha) of a navy-black scrim, heaviest where type sits
SCRIM_RGB = (6, 5, 24)

# ---- the background, built once in PIL and used for BOTH the render and the contrast measurement --------------------------------------------------------
im = Image.open(PHOTO).convert("RGB"); s = max(W / im.width, H / im.height)
im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
left = (im.width - W) // 2; im = im.crop((left, 0, left + W, H))
arr = np.asarray(im).astype(float) * 1.18     # the source is dark: lift it before the scrim
ys = np.arange(H); alpha = np.interp(ys, [p[0] for p in SCRIM], [p[1] for p in SCRIM])[:, None, None]
bg = arr * (1 - alpha) + np.array(SCRIM_RGB)[None, None, :] * alpha
bg_img = Image.fromarray(bg.clip(0, 255).astype("uint8"))
buf = io.BytesIO(); bg_img.save(buf, "JPEG", quality=92); BG_URI = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
lin = lambda c: ((c / 255) / 12.92) if c / 255 <= .04045 else (((c / 255 + .055) / 1.055) ** 2.4)
def lum(rgb): r, g, b = (lin(v) for v in rgb); return .2126 * r + .7152 * g + .0722 * b
def ratio(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
hexrgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
def surface(x, y, w, h, light_text=True):
    """The worst-case backing colour under a text box: the 95th-percentile-brightest pixel for light type, the 5th-percentile-darkest for dark type."""
    x, y, w, h = max(0, int(x)), max(0, int(y)), int(w), int(h)
    reg = bg[y:y + h, x:x + w].reshape(-1, 3); L = np.array([lum(p) for p in reg[::7]])
    idx = np.argsort(L)[int(len(L) * (.95 if light_text else .05))]; return tuple(int(v) for v in reg[::7][idx])
CHOICES = {"cream": hexrgb(CREAM), "white": (255, 255, 255), "ink": hexrgb(INK)}
receipt = []
def pick(label, x, y, w, h, size, bold=True, prefer=("cream", "white", "ink")):
    floor = 3.0 if (size >= 24 and bold) or size >= 36 else 4.5
    for name in prefer:
        bgc = surface(x, y, w, h, light_text=(name != "ink"))
        r = ratio(CHOICES[name], bgc)
        if r >= floor:
            receipt.append((label, name, round(r, 2), floor, "#%02x%02x%02x" % bgc)); return name, "#%02x%02x%02x" % bgc
    raise SystemExit(f"NO TEXT COLOUR CLEARS {floor}:1 for {label} at ({x},{y},{w},{h}); deepen the scrim there")

els = []
def box(label, x, y, w, h, html, z=10):
    els.append((label, round(x), round(y), round(w), round(h)))
    return f'<div data-tag="{label}" style="position:absolute;left:{round(x)}px;top:{round(y)}px;width:{round(w)}px;height:{round(h)}px;z-index:{z}">{html}</div>'

async def main():
    async with B.session():
        probe = await B.measure_text([{"text": "EVENTS", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "TEAM", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "NIGHT", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                      {"text": "starry", "font": "s", "size": 100, "weight": 400}], W, H)
        ev100, team100, night100, star100 = (p["text_w"] for p in probe)
        ev_size = 100 * (W - 2 * M - 14) / ev100; night_size = 100 * 540 / night100; starry_size = 100 * 370 / star100
        sz = await B.measure_text([{"text": "JOIN THE", "font": "d", "size": 92, "weight": 900, "transform": "uppercase", "line_height": .9},
                                   {"text": "EVENTS", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "TEAM", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "NIGHT", "font": "d", "size": night_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "starry", "font": "s", "size": starry_size, "weight": 400, "line_height": .9}], W, H)
        join_h, ev_h, team_h, night_h, starry_h = (z["ink_h"] for z in sz); join_w = sz[0]["text_w"]; team_w = sz[2]["text_w"]
        parts = []
        parts.append(f'<img src="{core.LOGO}" style="position:absolute;top:56px;left:{M}px;height:34px;z-index:20;filter:drop-shadow(0 2px 6px rgba(0,0,0,.7))">'); els.append(("logo", M, 56, 160, 34))
        parts.append(box("eyebrow", M, 128, 290, 48, f'<div style="width:100%;height:100%;background:{SKY};border:3px solid {INK};border-radius:999px;box-shadow:4px 4px 0 {EDGE};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;color:{INK};white-space:nowrap">NOW RECRUITING</div>', z=12))
        y = 214
        jc, _ = pick("join", M, y, join_w, join_h, 92)
        hexof = lambda n: {"cream": CREAM, "white": "#FFFFFF", "ink": INK}[n]
        parts.append(box("join", M, y, join_w + 10, join_h, f'<div style="font-family:var(--d);font-weight:900;font-size:92px;line-height:.9;text-transform:uppercase;color:{hexof(jc)};white-space:nowrap">JOIN THE</div>'))
        y += join_h + 14
        ec, _ = pick("events", M, y, W - 2 * M, ev_h, int(ev_size))
        parts.append(box("events", M - 4, y, W - 2 * M + 8, ev_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{hexof(ec)};text-shadow:7px 7px 0 {SKY};white-space:nowrap">EVENTS</div>'))
        y += ev_h + 30
        bw, bh = team_w + 80, team_h + 44
        parts.append(box("team", M, y, bw, bh, f'<div style="width:100%;height:100%;background:{SKY};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;box-shadow:9px 9px 0 {EDGE};box-sizing:border-box;'
                         f'display:flex;align-items:center;justify-content:center"><span style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{INK}">TEAM</span></div>', z=11))
        sx = M + bw + 36; sub_y = y + bh / 2 - 60
        subc, _ = pick("sub", sx, sub_y, W - M - sx, 120, 34, bold=False)
        parts.append(box("sub", sx, sub_y, W - M - sx, 120, f'<div style="font-family:var(--e);font-weight:600;font-size:34px;line-height:1.18;color:{hexof(subc)};text-shadow:0 2px 10px rgba(0,0,0,.55)">come run<br>the night<br>with us</div>'))
        y_team_end = y + bh
        # ---- lower block: the photo is the hero in between (hands on the decks, y ~ 760-1180) ----
        ly = 1140
        parts.append(box("starry", M, ly, 560, starry_h, f'<div style="font-family:var(--s);font-style:italic;font-size:{starry_size:.0f}px;line-height:.9;color:{LEMON};white-space:nowrap;text-shadow:0 3px 14px rgba(0,0,0,.55)">starry</div>'))
        nc, _ = pick("night", M, ly + starry_h + 6, 700, night_h, int(night_size))
        parts.append(box("night", M - 4, ly + starry_h + 6, 700, night_h, f'<div style="font-family:var(--d);font-weight:900;font-size:{night_size:.0f}px;line-height:.86;text-transform:uppercase;color:{hexof(nc)};text-shadow:6px 6px 0 {SKY};white-space:nowrap">NIGHT</div>'))
        ey = ly + starry_h + 6 + night_h + 26
        lc, _ = pick("label", M, ey, 560, 24, 17)
        parts.append(box("label", M, ey, 560, 24, f'<div style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.12em;color:{hexof(lc)};white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,.6)">THE CHRISTMAS CARNIVAL FUNDRAISER</div>'))
        # moon + stars, lemon, in the clear space right of 'starry' (measured: dark scrim, no type)
        ms = 150; mx, my = 800, ly - 4
        parts.append(box("moon", mx, my, ms, ms, f'<svg viewBox="0 0 100 100" width="{ms}" height="{ms}" style="display:block;overflow:visible"><defs><mask id="mm"><rect width="100" height="100" fill="#fff"/><circle cx="68" cy="38" r="38" fill="#000"/></mask></defs>'
                         f'<circle cx="50" cy="50" r="46" fill="{LEMON}" stroke="{INK}" stroke-width="3.5" mask="url(#mm)" transform="rotate(-18 50 50)"/></svg>', z=15))
        for i, (kx, ky, ks, kr) in enumerate(((620, ly + 40, 62, -10), (940, ly + 190, 78, 12), (800, ly + 225, 48, 6))):
            parts.append(box(f"dd_star{i}", kx, ky, ks, ks, dd.stamp("star", LEMON, rot=kr, style="clean"), z=14))
        # LINK SLOT (user, 2026-11-21: 'write link here so we can post the link of the form'): a pill the size of an Instagram link sticker, left clear for it. Ends above the reply bar (y~1670).
        cy0 = ey + 24 + 44; lw, lh = 600, 96
        parts.append(box("linkzone", M, cy0, lw, lh, f'<div style="width:100%;height:100%;background:{SKY};border:4px solid {INK};border-radius:999px;box-shadow:6px 6px 0 {EDGE};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:30px;letter-spacing:.12em;color:{INK}">LINK HERE</div>', z=12))
        # the handle moves to the top-right kicker slot so nothing else sits in the link zone
        hc, _ = pick("handle", W - M - 300, 62, 300, 30, 20)
        parts.append(box("handle", W - M - 300, 62, 300, 30, f'<div style="font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.05em;color:{hexof(hc)};text-align:right;text-shadow:0 2px 8px rgba(0,0,0,.6)">@ngo.aquaterra</div>'))
        print("heights: starry", starry_h, "night", night_h, "team_end", y_team_end, "ly", ly)
        print(f"\nTEXT-COLOUR RECEIPT (95th-pct backing pixel under each box)\n{'label':8} {'colour':6} {'ratio':>6} {'floor':>5}  backing")
        for r in receipt: print(f"{r[0]:8} {r[1]:6} {r[2]:>6} {r[3]:>5}  {r[4]}")
        print("LINK slot ends at y =", cy0 + lh, "(reply bar starts ~1670)")
        inner = f'<img data-tag="plate" src="{BG_URI}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:0">' + "".join(parts)
        html = B.page(W, H, "#000", inner, grain=False)
        tp = [("eyebrow", INK, SKY, 18, True), ("team", INK, SKY, 200, True), ("linkzone", INK, SKY, 30, True)]
        for r in receipt:
            tp.append((r[0], {"cream": CREAM, "white": "#FFFFFF", "ink": INK}[r[1]], r[4], 17 if r[0] == "label" else 34, r[0] != "sub"))
        os.makedirs("out/aq_events", exist_ok=True)
        await B.render(html, "out/aq_events/starry_recruit_photo_story.png", W, H, elements=els, text_pairs=tp, bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000",
                       collision_ignore=[("team", "events"), ("team", "sub"), ("starry", "moon")])
asyncio.run(main())
