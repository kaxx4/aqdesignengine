"""STARRY NIGHT THROWBACK poster in the DISCO DIWALI branding, feed (1080x1350).

Brief (user, 2026-11-27): "make a throwback post for Starry Night, use disco diwali branding, use the inspos". Photos: the user's Drive folder
`SN 24` (18 frames, Starry Night Christmas carnival, December 2024). Inspo mechanism taken: the first inspo, a Christmas TREE built out of tilted print frames
with a star on top and the title underneath. Other inspos contributed the Christmas mood only (envelope / gift frame / arc text were not used: one mechanism per piece).

Branding borrowed from the Disco Diwali format: navy-and-gold diya ground fading to black, string lights, gold dust + film grain (screen blend), NeutralFace white type with a black
stroke, the red-copper metal sticker (dd_copper.star) as the tree-top star. NOT used on purpose: the DISCO DIWALI lockup, the mask and the LIVE badge: they name another event and
LIVE would be false on a throwback.
Adaptations: the inspo's colour confetti stars become gold only (format palette: silver, gold, copper); the inspo's cut-out figures are not built (no cut-outs supplied).
Facts printed: only "Starry Night", "Throwback", "Christmas carnival", "December 2024" (brain/AQ_FACTS.md). No venue, price or count.
Consent caveat: the frames show apparent minors and there is no consent record. Check before posting.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_starry_throwback.py"""
import asyncio, base64, io, importlib.util, math, os, random, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_copper as cp
B = dd.B
W, H = 1080, 1350
SRC = os.environ.get("SN_SRC", "/tmp/claude-0/-home-user-aqdesignengine/d97c83e4-e42c-5d0c-953f-a1bebdeb468c/scratchpad/starry/sn24/src_images")
OUT = os.path.join(ROOT, "out", "discodiwali", "starry_throwback")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GOLD = "#e8c46a"

# (photo index, focus x%, focus y%) from the top of the tree down; looked at on the contact sheet, faces and the tree kept in the frame
ROWS = [
    [(11, 50, 50)],
    [(13, 50, 50), (2, 50, 40)],
    [(7, 50, 45), (8, 50, 55), (14, 50, 45)],
    [(15, 50, 55), (12, 50, 70), (3, 50, 35), (9, 50, 40)],
    [(0, 50, 50), (1, 50, 50), (6, 62, 50), (16, 50, 45), (5, 50, 35)],
]
FW, FH, PAD, FOOT = 200, 246, 12, 40        # print frame, photo inset, polaroid foot
STEP_X, STEP_Y, TOP = 176, 142, 176


def photo_uri(i):
    im = Image.open(os.path.join(SRC, f"{i:02d}.jpg")).convert("RGB"); im.thumbnail((620, 620))
    b = io.BytesIO(); im.save(b, "JPEG", quality=84)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def ground():
    plate = (f'<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>'
             f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:1350px;object-fit:cover;z-index:1">')
    return plate + (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
                    f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
                    f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def sparkle(x, y, s, o=1):
    return (f'<svg data-tag="spark" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;z-index:8;opacity:{o}" viewBox="-50 -50 100 100">'
            f'<path d="M0-48 C4-12 12-4 48 0 C12 4 4 12 0 48 C-4 12 -12 4 -48 0 C-12-4 -4-12 0-48Z" fill="{GOLD}"/></svg>')


def tree():
    rnd = random.Random(24)
    frames, z = [], 10
    for r, row in enumerate(ROWS):
        n = len(row)
        for k, (pi, fx, fy) in enumerate(row):
            cx = W / 2 + (k - (n - 1) / 2) * STEP_X + rnd.uniform(-7, 7)
            y = TOP + r * STEP_Y + rnd.uniform(-6, 6)
            rot = rnd.uniform(-6.5, 6.5)
            z += 1
            frames.append(
                f'<div data-tag="frame" style="position:absolute;left:{round(cx - FW / 2)}px;top:{round(y)}px;width:{FW}px;height:{FH}px;background:#f1ead8;'
                f'border:2px solid #000;box-sizing:border-box;transform:rotate({rot:.1f}deg);box-shadow:5px 6px 0 rgba(0,0,0,.55);z-index:{z}">'
                f'<div data-tag="frame" style="position:absolute;left:{PAD - 2}px;top:{PAD - 2}px;width:{FW - 2 * PAD}px;height:{FH - PAD - FOOT}px;overflow:hidden;background:#000">'
                f'<img src="{photo_uri(pi)}" style="width:100%;height:100%;object-fit:cover;object-position:{fx}% {fy}%;filter:contrast(1.05) saturate(.95) brightness(1.06)"></div></div>')
    x0 = W / 2 - (STEP_X * 2 + FW / 2) - 14
    return "".join(frames), (round(x0), TOP - 14, round(2 * (W / 2 - x0)), (len(ROWS) - 1) * STEP_Y + FH + 28)


def poster():
    parts, els = [ground()], []
    t_html, tb = tree()
    parts.append(t_html); els.append(("tree", *tb))
    ss = 150                                                      # tree-top star: the red-copper metal sticker, as on the other posters
    sx, sy = (W - ss) // 2, TOP - 128
    parts.append(f'<div data-tag="star" style="position:absolute;left:{sx}px;top:{sy}px;z-index:40">{cp.star(ss, 0)}</div>'); els.append(("star", sx, sy, ss, ss))
    # gold sparkles in the empty navy corners (sizes varied, none touching the tree or type)
    for (x, y, s, o) in [(70, 190, 46, 1), (140, 330, 26, .9), (60, 520, 20, .8), (940, 210, 40, 1), (900, 400, 24, .9), (990, 560, 30, .85),
                         (200, 90, 22, .8), (850, 90, 26, .8), (36, 760, 34, .9), (1000, 830, 24, .9)]:
        parts.append(sparkle(x, y, s, o))
    # type: THROWBACK small over a huge STARRY NIGHT, then the edition line; all NeutralFace, white with a black stroke
    def line(tag, txt, top, size, weight, h, extra="", z=20):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                     f'line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:{z}">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    ty = 1042
    line("kicker", "Throwback", ty, 40, 400, 42, f"letter-spacing:.34em;")
    line("title", "Starry Night", ty + 50, 114, 700, 118)
    line("sub", "Christmas carnival &middot; December 2024", ty + 50 + 128, 36, 400, 38, "letter-spacing:.06em;")
    parts.append(f'<div data-tag="gold" style="position:absolute;left:{W // 2 - 90}px;top:{ty + 50 + 128 + 56}px;width:180px;height:4px;background:{GOLD};z-index:20"></div>')
    els.append(("gold", W // 2 - 90, ty + 50 + 128 + 56, 180, 4))
    return "".join(parts), els


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els = poster()
    out = os.path.join(OUT, "feed.png")
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), out, W, H, elements=els, containers=("tree",), bleed_tags=("plate",), crop_tags=("plate", "frame"),
                       page_bg="#000", collision_ignore=[])
    print("done ->", out)
asyncio.run(main())
