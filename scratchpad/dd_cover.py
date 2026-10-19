"""DISCO DIWALI carousel cover (feed 1080x1350), v3 "hype, no reveals": the lockup with its ball, the copper mask, the LIVE badge, IT'S HAPPENING., the edition line
and a SWIPE FOR THE REVEAL pill. Carousel: slide 2 ALL FOR CHARITY, slide 3 the date reveal, slide 4 the location reveal. The cover must NOT show the date or the
location (user, 2026-10-19: the fanned-slides version leaked both), so it carries neither as text nor as a picture of the later slides.
Copy: IT'S HAPPENING is the user's brief ("fun, hype") expressed as copy, a claim of nothing but the event existing. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_cover.py"""
import asyncio, base64, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "cover")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


def jpg(path):
    return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, path), "rb").read()).decode()


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


def build():
    parts, els = [], []
    parts.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>'
                 f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'
                 f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">')
    # copper mask, visible box 343..1035 x 60..512 (the poster_ref placement lifted 48px to make room for the headline)
    k = .4925; my = 60
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(343 - 157 * k)}px;top:{round(my - 211 * k)}px;width:{round(1680 * k)}px;z-index:6;'
                 f'filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">'); els.append(("mask", 343, my, 692, 452))
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:30px;top:74px;width:267px;z-index:8">'); els.append(("badge", 30, 74, 267, 248))
    # lockup WITH its ball, visible box 265..1982 x 320..1311 of the 2000x1382 asset, drawn 860 wide
    vw = 860; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = 465
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    def line(tag, txt, top, size, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    hy = vy + vh + 44
    line("headline", "It&rsquo;s happening.", hy, 104, 700, 100)
    ey = hy + 118
    line("edition", "Masquerade Sangeet Edition", ey, 36, 400, 38)
    sy = ey + 56
    sw, sh = 700, 78
    parts.append(f'<div data-tag="swipe" style="position:absolute;left:{(W - sw) // 2}px;top:{sy}px;width:{sw}px;height:{sh}px;border:2px solid rgba(214,170,90,.85);border-radius:39px;background:rgba(0,0,0,.4);'
                 f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:36px;white-space:nowrap;text-transform:uppercase;letter-spacing:2px;{STROKE}z-index:20">Swipe for the reveal &rarr;</div>')
    els.append(("swipe", (W - sw) // 2, sy, sw, sh))
    parts.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
                 f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return "".join(parts), els, sy + sh


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, bottom = build()
    print(f"[cover] last element ends at y={bottom} of {H}")
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "cover.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                       page_bg="#000", collision_ignore=[("mask", "title"), ("badge", "title"), ("mask", "badge")])
    print("cover done ->", OUT)
asyncio.run(main())
