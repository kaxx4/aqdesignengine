"""DISCO DIWALI "NANDU JEE" point poster, feed (1080x1350, also the WhatsApp size) and story (1080x1920), 2026-10-24.
From the user's Paradox reference (circular photo, big red NANDU JEE, two-part tagline, JOIN NOW button, sponsor + logos): the MECHANISM is kept
(real photo in a circle, display headline, snarky tagline) and rebuilt on the Disco Diwali skeleton: diya ground, string lights, LIVE badge, copper mask tucked on the
circle's corner, the lockup (with ball) as the footer mark. Adaptations: the Realmark title-sponsor mark, the Paradox logo and the beach palms are NOT Disco Diwali's, so they
are dropped; the JOIN NOW / LIMITED SPOTS button becomes the story's LINK IN BIO pill (the feed, for WhatsApp, has none: nothing to link to). Copy is the user's own
reference copy: NANDU JEE / SERVING CHAOS AND CRAVINGS (ON THE HOUSE). No date, price or venue. Photo: user-supplied portrait, consent unconfirmed.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_nandu.py  -> out/discodiwali/nandu/{feed,story}.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "nandu")
PHOTO = os.path.join(ROOT, "engine", "assets", "img", "events", "nandu-jee", "01_nandu-jee-googly-eyes.jpg")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_charity_ground as G          # noqa: E402  (diya ground, shared with the charity poster)

def poster(H):
    story = H > 1350
    parts, els = [G.ground_diya(W, H)], []
    # LIVE badge, top left
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # the circle photo
    d = 680 if story else 560
    cx, cy0 = (W - d) // 2, (300 if story else 130)
    parts.append(f'<div data-tag="circle" style="position:absolute;left:{cx}px;top:{cy0}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:8px solid {dd.GOLD};'
                 f'box-sizing:border-box;z-index:10;box-shadow:0 14px 40px rgba(0,0,0,.6)">'
                 f'<img src="{dd.photo_uri(PHOTO)}" style="width:100%;height:100%;object-fit:cover;object-position:50% 38%;filter:contrast(1.06) saturate(1.05)"></div>')
    els.append(("circle", cx, cy0, d, d))
    # copper mask tucked on the circle's top-right corner (visible outline = 1403x878 native at scale k)
    k = .30 if story else .28
    mvw, mvh = round(1403 * k), round(878 * k)
    mx, my = 1040 - mvw, (cy0 - 120 if story else 60)
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(mx - 157 * k)}px;top:{round(my - 211 * k)}px;width:{round(1680 * k)}px;'
                 f'z-index:12;filter:drop-shadow(0 8px 22px rgba(0,0,0,.6))">'); els.append(("mask", mx, my, mvw, mvh))
    # headline + tagline
    hy = cy0 + d + (28 if story else 26)
    hs = 150
    def line(tag, txt, top, size, weight, h, stroke=True):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else "color:#fff;"}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("head", "Nandu Jee", hy, hs, 700, hs)
    t1 = hy + hs + 14
    line("tag1", "Serving chaos and cravings", t1, 50, 700, 54, stroke=False)
    line("tag2", "(on the house)", t1 + 58, 50, 400, 54, stroke=False)
    y = t1 + 58 + 54 + (26 if story else 22)
    # footer lockup, with ball
    vw = 260 if story else 300
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, y, vw, vh)); bottom = y + vh
    if story:                                           # link pill where the link sticker goes; clear of Instagram's reply bar (1670+)
        py = bottom + 22
        parts.append(f'<div data-tag="linkpill" style="position:absolute;left:342px;top:{py}px;width:382px;height:82px;border-radius:22px;border:2px solid rgba(222,180,100,.6);'
                     f'background:rgba(236,200,150,.22);z-index:12;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:44px;line-height:1;'
                     f'text-transform:uppercase;color:#fff">Link in bio</div>'); els.append(("linkpill", 342, py, 382, 82)); bottom = py + 82
    return "".join(parts), els, bottom

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "circle"),
                           page_bg="#000", collision_ignore=[("circle", "mask"), ("circle", "head")],
                           text_pairs=[("head", "#fff", "#000", 150, True), ("tag", "#fff", "#000", 50, True)])
    print("nandu done ->", OUT)
asyncio.run(main())
