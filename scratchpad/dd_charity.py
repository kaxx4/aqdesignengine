"""DISCO DIWALI ALL FOR CHARITY poster, feed (1080x1350) and story (1080x1920), rebuilt to MATCH the carousel's date and location posters.

Shared skeleton (same numbers as scratchpad/dd_date_reveal.py and dd_location_reveal.py): diya ground with string lights, a small LIVE badge top left, a headline
block, a big white rounded card tilted -5 degrees with the copper mask lying across its top-right corner, the DISCO DIWALI lockup (with its ball) as a footer mark,
no pill, no link. Here the headline is ALL FOR CHARITY, the line under it is the edition, and the card holds the LIVE badge art (ALL FOR CHARITY / LIVE / AQUATERRA)
large, as the visual. Facts: only "All for charity" (the badge) and "Masquerade Sangeet Edition". No date, venue, price or figure (the cover and slides own the rest).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_charity.py"""
import asyncio, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "charity")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
CARD_W, CARD_H, TILT = 880, 520, -5


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


def ground(H):
    plate = lambda top, extra="": (f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{top}px;width:{W}px;height:1350px;'
                                   f'object-fit:cover;z-index:1;{extra}">')
    p = '<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>' + plate(0)
    if H > 1350:
        p += plate(H - 1350, "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
    p += (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
          f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
          f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return p


def poster(H):
    story = H > 1350
    parts, els = [ground(H)], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    size = 112 if story else 92
    hy = 430 if story else 205
    def line(tag, txt, top, fsize, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 70, top, 940, h))
    line("head1", "All for", hy, size, 700, size)
    line("head2", "charity", hy + round(size * .96), size, 700, size)
    sy = hy + round(size * .96) * 2 + 20
    line("sub", "Masquerade Sangeet Edition", sy, 38, 400, 40)
    # the card: white, tilted, holding the LIVE badge art large and centred
    ctop = 800 if story else 520
    cleft = (W - CARD_W) // 2
    bw2 = 460; bh2 = round(bw2 * 1005 / 1061)                # the badge art is semi-transparent over black: on a white card it washes to grey, so it sits on an OPAQUE black tile
    inner = (f'<div style="position:absolute;left:{(CARD_W - bw2) // 2}px;top:{(CARD_H - bh2) // 2}px;width:{bw2}px;height:{bh2}px;background:#0a0a0a;border-radius:44px;overflow:hidden">'
             f'<img src="{dd.uri("live_badge.png")}" style="width:{bw2}px;display:block"></div>')
    parts.append(f'<div data-tag="card" style="position:absolute;left:{cleft}px;top:{ctop}px;width:{CARD_W}px;height:{CARD_H}px;border-radius:30px;overflow:hidden;background:#fff;z-index:10;'
                 f'transform:rotate({TILT}deg);box-shadow:0 36px 70px rgba(0,0,0,.6),0 0 0 3px rgba(255,255,255,.55)">{inner}</div>')
    els.append(("card",) + rot_box(cleft + CARD_W / 2, ctop + CARD_H / 2, CARD_W, CARD_H, TILT))
    mw = 330; mx, my = 730, ctop - 62
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{mx}px;top:{my}px;width:{mw}px;z-index:12;transform:rotate(10deg);'
                 f'filter:drop-shadow(0 12px 26px rgba(0,0,0,.65))">'); els.append(("mask", mx + 30, my + 40, 276, 196))
    vw = 400 if story else 330
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    vy = 1420 if story else H - 64 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card"),
                           page_bg="#000", collision_ignore=[("mask", "card"), ("card", "badge")])
    print("charity done ->", OUT)
asyncio.run(main())
