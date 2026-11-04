"""DISCO DIWALI "ZAAIRAH" food stall poster (copy of dd_pizzahut.py: vendor logo filling the circle, the vendor's own plate photo as the ground, new copper cloche sticker), feed (1080x1350, also the WhatsApp size) and story (1080x1920), 2026-10-24.
From the user's Paradox reference (circular photo, big red NANDU JEE, two-part tagline, JOIN NOW button, sponsor + logos): the MECHANISM is kept
(real photo in a circle, display headline, snarky tagline) and rebuilt on the Disco Diwali skeleton: diya ground, string lights, LIVE badge, copper diya sticker on the
circle's corner, the lockup (with ball) as the footer mark. Adaptations: the Realmark title-sponsor mark, the Paradox logo and the beach palms are NOT Disco Diwali's, so they
are dropped; the JOIN NOW / LIMITED SPOTS button becomes the story's LINK IN BIO pill (the feed, for WhatsApp, has none: nothing to link to). Copy is the user's own
reference copy: NANDU JEE / SERVING CHAOS AND CRAVINGS ('on the house' dropped 2026-10-24, user). No date, price or venue. Photo: user-supplied portrait, consent unconfirmed.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_nandu.py  -> out/discodiwali/nandu/{feed,story}.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "zaairah")
PHOTO = os.path.join(ROOT, "engine", "assets", "img", "events", "zaairah", "01_zaairah-logo.png")
import base64
BG = os.path.join(ROOT, "engine", "assets", "img", "events", "zaairah", "02_zaairah-pasta-plate.jpg")   # user-supplied Zaairah photo as the ground (2026-11-04)
LOGO = "data:image/png;base64," + base64.b64encode(open(PHOTO, "rb").read()).decode()
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_photo_bg as PB, dd_copper as CP   # noqa: E402  (photo ground and copper stickers, shared with the carousel posters)

def poster(H):
    story = H > 1350
    parts, els = [PB.photo_ground(dd, W, H, BG, "50% 50%", dim=.52)], []
    # LIVE badge, top left
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    # the circle photo
    d = 700 if story else 600
    cx, cy0 = (W - d) // 2, (320 if story else 150)
    parts.append(f'<div data-tag="circle" style="position:absolute;left:{cx}px;top:{cy0}px;width:{d}px;height:{d}px;border-radius:50%;overflow:hidden;border:8px solid {dd.GOLD};'
                 f'box-sizing:border-box;z-index:10;box-shadow:0 14px 40px rgba(0,0,0,.6)">'
                 f'<div style="position:absolute;inset:0;background:#000000"></div>'
                 f'<img src="{LOGO}" style="position:absolute;left:0;top:0;width:100%;height:100%;object-fit:contain"></div>')
    els.append(("circle", cx, cy0, d, d))
    # copper DHOL sticker (user, 2026-10-24: "a different sticker, not the mask") tucked on the circle's top-right; sticker() is square, rotation baked in
    ss = 300 if story else 280
    mx, my = 1040 - ss, (cy0 - 150 if story else 40)
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{mx}px;top:{my}px;z-index:12">{CP.cloche(ss, 8)}</div>'); els.append(("sticker", mx, my, ss, ss))
    # headline + tagline
    hy = cy0 + d + (28 if story else 26)
    hs = 165
    def line(tag, txt, top, size, weight, h, stroke=True):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE if stroke else "color:#fff;"}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("head", "Zaairah", hy, hs, 700, hs)
    t1 = hy + hs + 14
    line("tag1", "Food stall", t1, 50, 700, 54, stroke=False)
    y = t1 + 54 + (30 if story else 26)
    # footer lockup, with ball
    vw = 260 if story else 300
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(y - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, y, vw, vh)); bottom = y + vh
    # no LINK IN BIO pill (user, 2026-11-04)
    return "".join(parts), els, bottom

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "circle"),
                           page_bg="#000", collision_ignore=[("circle", "sticker"), ("circle", "head")],
                           text_pairs=[("head", "#fff", "#000", 165, True), ("tag", "#fff", "#000", 50, True)])
    print("zaairah done ->", OUT)
asyncio.run(main())
