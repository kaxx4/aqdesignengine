"""DISCO DIWALI reel covers (2026-10-21): fifteen 1080x1920 covers on one constant frame, one real event photo and one hook line each.

THE FRAME (constant across the series): full-bleed photo graded navy-dark, string lights, LIVE badge top left, a copper corner object top right
(the mask on four covers, a copper heart / star / diya on the rest: user, 2026-10-20, "different stickers instead of the mask again and again"),
the ball-free title lockup as the hero, the edition line tucked into its notch, then ONE hook line at a shared size. Everything that must read
sits inside Instagram's profile-grid crop. The grid shows the centre 3:4 of a reel cover (y 240..1680 here) and older grids the centre 4:5
(y 285..1635), so every element is declared inside y 285..1635; the top 200 and bottom 250 stay clear of the app UI.

Type is NeutralFace, white with a black border (launch-pack rule). No date, time, venue, price or lineup: none was supplied for covers, and the
hooks claim nothing but the event, the charity and the masks. VOICE.md section 9: no exclamation stacks, no countdown urgency.
Adaptation recorded: the title lockup is the ball-free file (as story_ref), so the cover reads at grid size without the ball's small detail.
CONSENT: many people in these photos look like minors and no consent record exists (engine/assets/img/events/README.md). Check before posting.

Outputs out/discodiwali/reels/reel_NN.png (+ sheet.png, grid_preview.png).   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_reel_covers.py
"""
import asyncio, base64, importlib.util, io, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND = dd.B, dd.GROUND
W, H = 1080, 1920
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
LIB = os.path.join(ROOT, "engine", "assets", "img", "events", "unsorted-2026-10-07")
STK = os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers")
EDITION = "Masquerade Sangeet"
# (photo path, x-centre fraction of the 9:16 crop, corner object, hook line 1, hook line 2)
COVERS = [
    (f"{HALL}/04_pink-ceiling-chandelier-phone.jpg", .55, "mask",  "DIWALI,", "BUT DISCO"),
    (f"{HALL}/05_boys-crowd-green-light.jpg",        .50, "heart", "WHO'S", "COMING?"),
    (f"{HALL}/03_girls-dancing-yellow-top.jpg",      .55, "star",  "DANCE FOR", "A REASON"),
    (f"{HALL}/01_dancers-silver-pillar-purple.jpg",  .45, "diya",  "MASKS ON.", "LIGHTS DOWN."),
    (f"{LIB}/06_three-friends-fairy-lights.jpg",     .60, "mask",  "TAG YOUR", "PLUS ONE"),
    (f"{HALL}/06_blue-room-crowd-faces.jpg",         .60, "heart", "DANCE FLOOR", "IS WAITING"),
    (f"{HALL}/07_pink-glare-girls-backs-phone.jpg",  .45, "star",  "SANGEET WITH", "A MASK ON"),
    (f"{HALL}/08_boy-on-shoulders-stage-lights-portrait.jpg", .55, "diya", "GOOD VIBES,", "GOOD CAUSE"),
    (f"{HALL}/09_boy-on-shoulders-star-balloon.jpg", .42, "mask",  "ALL FOR", "CHARITY"),
    (f"{LIB}/03_IMG_1451_red-drapes-entrance.jpg",   .50, "heart", "TICKET SALES", "OPEN SOON"),
    (f"{LIB}/10_disco-diwali-photo-booth.jpg",       .55, "star",  "PUT YOUR", "MASK ON"),
    (f"{LIB}/11_dance-green-light-portrait.jpg",     .50, "diya",  "SAVE THE", "NIGHT"),
    (f"{LIB}/13_IMG_1500_dance-pink-light-phone.jpg", .50, "mask", "MORE DETAILS", "TO FOLLOW"),
    (f"{HALL}/02_crowd-teal-kurta-purple.jpg",       .52, "heart", "SEE YOU", "ON THE FLOOR"),
    (f"{LIB}/02_IMG_7028_group-pink-balloons.jpg",   .50, "star",  "MASQUERADE", "MODE: ON"),
]
SAFE_TOP, SAFE_BOT = 285, 1635                  # the 4:5 grid crop of a 1080x1920 cover; the 3:4 crop (240..1680) is wider, so this is the stricter one
TITLE_T = .59                                    # title lockup scale, as story_ref (visible outline 38..1051 wide, 538 tall)
TITLE_Y = 660                                    # visible top of the lockup
HOOK_YS = (1338, 1462)                           # hook line centres

def photo169(path, fx):
    """Centre-crop to 9:16 around fx and resample to exactly 1080x1920, embedded at full canvas resolution."""
    im = Image.open(path).convert("RGB"); w, h = im.size
    cw, ch = (w, round(w * 16 / 9)) if w / h < 9 / 16 else (round(h * 9 / 16), h)
    x0 = min(max(round(fx * w - cw / 2), 0), w - cw); y0 = (h - ch) // 2
    im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, H), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

def png_uri(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

def build(photo, fx, corner, l1, l2, hook_px):
    P, E = [], []
    def img(uri, x, y, w, z, tag, extra="", h=None):
        P.append(f'<img data-tag="{tag}" src="{uri}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
                 f'{f"height:{h}px;" if h else ""}z-index:{z};{extra}">')
    P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
    P.append(f'<img data-tag="photo" src="{photo169(photo, fx)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1;'
             f'filter:contrast(1.08) saturate(1.0) brightness(1.0)">')
    # navy grade, heavier under the type so the hook reads on a bright frame
    P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(8,6,30,.42) 0%,rgba(8,6,30,.06) 24%,'
             'rgba(0,0,0,.05) 46%,rgba(0,0,0,.36) 66%,rgba(0,0,0,.50) 86%,rgba(0,0,0,.40) 100%)"></div>')
    img(dd.uri("string_lights.png"), 120, 215, 1000, 5, "lights"); E.append(("lights", 120, 215, 1000, 331))
    # corner object, top right, inside the grid crop; the lockup tucks over its bottom edge
    if corner == "mask":
        k = .40                                         # copper mask: visible outline starts 157,211 in the 1680x1278 asset, 1400 wide
        vx, vy = 476, 352
        img(dd.uri("mask_copper.png"), round(vx - 157 * k), round(vy - 211 * k), round(1680 * k), 6, "mask",
            "filter:drop-shadow(0 8px 26px rgba(0,0,0,.6));")
        E.append(("mask", vx, vy, round(1400 * k), round(920 * k)))
    else:
        f = os.path.join(STK, f"copper_{corner}.png"); sw, sh = Image.open(f).size
        w = {"heart": 300, "star": 310, "diya": 360}[corner]; h = round(w * sh / sw)
        x, y = 700, 350 if corner != "diya" else 380
        img(png_uri(f), x, y, w, 6, "sticker", "filter:drop-shadow(0 8px 22px rgba(0,0,0,.6));")
        E.append(("sticker", x, y, w, h))
    img(dd.uri("live_badge.png"), 45, 360, 264, 8, "badge"); E.append(("badge", 45, 360, 264, round(264 * 1005 / 1061)))
    # the hero: ball-free title lockup, placed from its measured visible outline
    t = TITLE_T
    img(dd.uri("title_lockup_noball.png"), round(38 - 265 * t), round(TITLE_Y - 401 * t), round(2000 * t), 9, "title")
    E.append(("title", 38, TITLE_Y, 1013, 538))
    dy = TITLE_Y - 480
    txt = ("position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);white-space:nowrap;line-height:1;color:#fff;font-family:var(--d);"
           "text-transform:uppercase;-webkit-text-stroke:{sw}px #000;paint-order:stroke fill;z-index:12;font-weight:{wt};font-size:{px}px")
    P.append(f'<div data-tag="sub1" style="{txt.format(cx=617, cy=938 + dy, sw=4, wt=700, px=40)}">{EDITION}</div>')
    P.append(f'<div data-tag="sub2" style="{txt.format(cx=617, cy=981 + dy, sw=4, wt=400, px=38)}">Edition</div>')
    E.append(("sub1", 357, 938 + dy - 23, 520, 46)); E.append(("sub2", 527, 981 + dy - 21, 180, 42))
    for lab, line, cy in (("hook1", l1, HOOK_YS[0]), ("hook2", l2, HOOK_YS[1])):
        P.append(f'<div data-tag="{lab}" style="{txt.format(cx=540, cy=cy, sw=7, wt=700, px=hook_px)}">{line}</div>')
    return P, E

async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "reels"); os.makedirs(out, exist_ok=True)
    lines = [l for c in COVERS for l in (c[3], c[4])]
    # ONE hook size for the whole series: the largest at which the widest line still fits 960px (measured, not guessed)
    probe = await B.measure_text([dict(text=l, font="d", size=100, weight=700) for l in lines], W=W, H=H)
    widest = max(p["glyph_w"] for p in probe)
    hook_px = int(100 * 960 / widest) // 2 * 2
    print("hook size", hook_px, "widest line at 100px", round(widest))
    # measured line height of the hook for honest boxes
    hm = await B.measure_text([dict(text="HG", font="d", size=hook_px, weight=700)], W=W, H=H)
    hh = max(round(hm[0]["glyph_h"]), 114)   # drawn height incl. the 7px border (reconcile reported 114)
    async with B.session():
        for i, (photo, fx, corner, l1, l2) in enumerate(COVERS, 1):
            P, E = build(photo, fx, corner, l1, l2, hook_px)
            ws = await B.measure_text([dict(text=l1, font="d", size=hook_px, weight=700), dict(text=l2, font="d", size=hook_px, weight=700)], W=W, H=H)
            for lab, m, cy in (("hook1", ws[0], HOOK_YS[0]), ("hook2", ws[1], HOOK_YS[1])):
                E.append((lab, round(540 - m["glyph_w"] / 2), round(cy - hh / 2), round(m["glyph_w"]), hh))
            P.append(f'<img src="{dd.uri("sparkles.png")}" data-tag="sparkles" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:14;mix-blend-mode:screen;object-fit:cover">')
            P.append(f'<img src="{dd.uri("grain.png")}" data-tag="grain" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:15;mix-blend-mode:screen;object-fit:cover;opacity:.9">')
            for lab, x, y, w, h in E:                          # the grid-crop rule, asserted for every element that must read
                if lab not in ("lights",):
                    assert y >= SAFE_TOP - 1 and y + h <= SAFE_BOT + 1, f"cover {i}: {lab} leaves the grid-safe zone ({y}..{y + h})"
            html = B.page(W, H, GROUND, "".join(P), grain=False)
            html = dd.Poster.neutralise(html)
            ignore = [("title", "sub1"), ("title", "sub2"), ("title", "mask"), ("title", "sticker"), ("mask", "badge"), ("badge", "title"),
                      ("lights", "mask"), ("lights", "sticker"), ("lights", "badge"), ("lights", "title"), ("sub2", "hook1"), ("title", "hook1"), ("badge", "sticker")]
            names = {e[0] for e in E}
            await B.render(html, os.path.join(out, f"reel_{i:02d}.png"), W, H, elements=E,
                           collision_ignore=[p for p in ignore if p[0] in names and p[1] in names],
                           text_pairs=[("hook1", "#fff", "#000", hook_px, True), ("hook2", "#fff", "#000", hook_px, True)],
                           bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain", "photo"), crop_tags=("plate", "sparkles", "grain", "photo"),
                           page_bg=GROUND)
    ims = [Image.open(os.path.join(out, f"reel_{i:02d}.png")).convert("RGB") for i in range(1, len(COVERS) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 3 + 20), (40, 40, 40))
    gp = Image.new("RGB", (360 * 5 + 40, 480 * 3 + 20), (20, 20, 20))
    for i, im in enumerate(ims):
        sh.paste(im.resize((324, 576), Image.LANCZOS), ((i % 5) * 334, (i // 5) * 586))
        s = im.width / W; gp.paste(im.crop((0, round(240 * s), im.width, round(1680 * s))).resize((360, 480), Image.LANCZOS), ((i % 5) * 370, (i // 5) * 490))   # the 3:4 profile-grid crop
    sh.save(os.path.join(out, "sheet.png")); gp.save(os.path.join(out, "grid_preview.png"))
    print("reel covers done ->", out)
asyncio.run(main())
