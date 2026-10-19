"""DISCO DIWALI WhatsApp poster (1080x1350): THE REVEAL IS TOMORROW. Built from the carousel cover (scratchpad/dd_cover.py): the lockup with its ball, the LIVE badge, the three
fanned cards (the ALL FOR CHARITY slide as is, the date and location slides BLURRED behind "?"), the edition line. The cover's SWIPE pill is dropped (nothing to swipe on WhatsApp)
and the cards are slightly bigger. NO date and NO location are printed or shown: they are what tomorrow reveals. "Tomorrow" is the user's own statement; no calendar date is
asserted. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_reveal.py"""
import asyncio, base64, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "wa_reveal")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


SLIDES = [("sample_outputs/disco_diwali_charity/feed.jpg", -9, False), ("sample_outputs/disco_diwali_date/feed.jpg", 0, True), ("sample_outputs/disco_diwali_location/feed.jpg", 9, True)]
CW, CH = 350, 437                                            # card size, 4:5


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


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
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:40px;width:150px;z-index:20">'); els.append(("badge", 40, 40, 150, round(150 * 1005 / 1061)))
    # lockup with ball, top centre, visible box 265..1982 x 320..1311, drawn 560 wide
    vw = 560; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2 + 40; vy = 40
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    def line(tag, txt, top, size, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    hy = vy + vh + 28
    line("h1", "The reveal is", hy, 100, 700, 96)
    line("h2", "tomorrow.", hy + 96, 142, 700, 138)
    # fan of the three slides: the charity slide is shown as is; the date and location slides are BLURRED behind a big "?" so they tease without revealing
    cy = hy + 96 + 138 + 40 + CH // 2 + 20
    xs = (285, 540, 795)
    z = (11, 12, 13)
    for (path, deg, hidden), cx, zi in zip(SLIDES, xs, z):
        dy = 14 if deg == 0 else 0
        img_style = "width:100%;height:100%;object-fit:cover;display:block;" + ("filter:blur(22px) brightness(.55) saturate(1.2);transform:scale(1.15);" if hidden else "")
        q = (f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:210px;line-height:1;{STROKE}">?</div>' if hidden else "")
        parts.append(f'<div data-tag="card{zi}" style="position:absolute;left:{cx - CW // 2}px;top:{cy - CH // 2 + dy}px;width:{CW}px;height:{CH}px;transform:rotate({deg}deg);z-index:{zi};'
                     f'border:6px solid #fff;border-radius:22px;overflow:hidden;box-sizing:border-box;box-shadow:0 22px 48px rgba(0,0,0,.65)">'
                     f'<img src="{jpg(path)}" style="{img_style}">{q}</div>')
        els.append((f"card{zi}",) + rot_box(cx, cy + dy, CW, CH, deg))
    ey = cy + CH // 2 + 48
    line("edition", "Masquerade Sangeet Edition", ey, 36, 400, 38)
    sy = ey + 38
    parts.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
                 f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
    return "".join(parts), els, ey + 38


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, bottom = build()
    print(f"[wa_reveal] last element ends at y={bottom} of {H}")
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "poster.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card11", "card12", "card13"),
                       page_bg="#000", collision_ignore=[("card11", "card12"), ("card12", "card13"), ("title", "badge"), ("h2", "card12"), ("h2", "card11"), ("h2", "card13")])
    print("wa reveal done ->", OUT)
asyncio.run(main())
