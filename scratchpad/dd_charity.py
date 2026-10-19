"""DISCO DIWALI ALL FOR CHARITY poster, feed (1080x1350) and story (1080x1920), matching the carousel's date and location posters WITHOUT their cards.

Same skeleton minus the card (user, 2026-10-19: "no cards in this slide"): diya ground with string lights, a small LIVE badge top left, the ALL FOR CHARITY headline with the
edition line under it, the copper mask large and centred as the hero, the DISCO DIWALI lockup (with its ball) as a footer mark, no pill, no link.
Facts: only "All for charity" and "Masquerade Sangeet Edition". Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_charity.py"""
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
    # no card (user, 2026-10-19: "no cards in this slide"): the copper mask is the hero, large and centred under the headline
    ctop = 850 if story else 545                              # top of the mask's visible box
    k = .498                                                  # visible width 1405k = 700, visible height 923k = 460 (asset 157..1562 x 211..1134)
    mw = round(1680 * k); mx = (W - round(1405 * k)) // 2 - round(157 * k); my = ctop - round(211 * k)
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{mx}px;top:{my}px;width:{mw}px;z-index:12;'
                 f'filter:drop-shadow(0 14px 32px rgba(0,0,0,.7))">'); els.append(("mask", (W - round(1405 * k)) // 2, ctop, round(1405 * k), round(923 * k)))
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
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", collision_ignore=[])
    print("charity done ->", OUT)
asyncio.run(main())
