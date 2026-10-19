"""DISCO DIWALI carousel cover (feed 1080x1350) for the three-slide set: ALL FOR CHARITY, the date reveal, the location reveal.

The cover is the brand moment: the DISCO DIWALI lockup WITH its ball as the hero, the copper mask top right, the LIVE badge top left, the edition line and a
swipe cue, on the approved diya ground with string lights. It repeats no date, time or venue (slides 2 and 3 own those) and carries no link pill.
Positions follow the measured poster_ref remake (badge 30..297 x 122..370, copper mask 343..1035 x 108..560, title 35..1071 wide).
Facts: only "Masquerade Sangeet Edition" and ALL FOR CHARITY (the badge). The swipe cue is navigation, not a claim.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_cover.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "cover")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


def build():
    parts, els = [], []
    parts.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>'
                 f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'
                 f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">')
    # copper mask, visible box 343..1035 x 108..560
    k = .4925
    parts.append(f'<img data-tag="mask" src="{dd.uri("mask_copper.png")}" style="position:absolute;left:{round(343 - 157 * k)}px;top:{round(108 - 211 * k)}px;width:{round(1680 * k)}px;z-index:6;'
                 f'filter:drop-shadow(0 8px 26px rgba(0,0,0,.6))">'); els.append(("mask", 343, 108, 692, 452))
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:30px;top:122px;width:267px;z-index:8">'); els.append(("badge", 30, 122, 267, 248))
    # lockup WITH its ball, visible box 265..1982 x 320..1311 of the 2000x1382 asset, drawn 1036 wide
    vw = 1036; t = vw / 1717; vh = round(991 * t); vx = 22; vy = 500
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    def line(tag, txt, top, size, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 90, top, 900, h))
    y = vy + vh + 26
    line("edition", "Masquerade Sangeet Edition", y, 44, 400, 46)
    sy = y + 96
    sw, sh = 330, 80
    parts.append(f'<div data-tag="swipe" style="position:absolute;left:{(W - sw) // 2}px;top:{sy}px;width:{sw}px;height:{sh}px;border:2px solid rgba(214,170,90,.7);border-radius:22px;background:rgba(0,0,0,.28);'
                 f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:40px;text-transform:uppercase;{STROKE}z-index:20">Swipe &rarr;</div>')
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
