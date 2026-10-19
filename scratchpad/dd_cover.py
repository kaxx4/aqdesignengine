"""DISCO DIWALI carousel cover (feed 1080x1350), v4: the user LIKED the fanned-cards cover (v2) but the date and location must stay hidden, so the same
composition is kept and the date and location cards are BLURRED behind a big "?". IT'S HAPPENING. over three fanned cards: the ALL FOR CHARITY slide as is (nothing to hide), the
date slide and the location slide blurred (blur 22px, darkened, scaled up so no edge text survives) with a "?" on each. Edition line and a SWIPE FOR THE REVEAL pill. The
cover reveals neither the date nor the place: the blur is checked by eye at full size. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_cover.py"""
import asyncio, base64, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "cover")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"


SLIDES = [("sample_outputs/disco_diwali_captcha/slide_4.jpg", -9, False), ("sample_outputs/disco_diwali_date/feed.jpg", 0, True), ("sample_outputs/disco_diwali_location/feed.jpg", 9, True)]
CW, CH = 330, 412                                            # card size, 4:5


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
    line("h1", "It&rsquo;s", hy, 104, 700, 100)
    line("h2", "happening.", hy + 98, 150, 700, 146)
    # fan of the three slides: the charity slide is shown as is; the date and location slides are BLURRED behind a big "?" so they tease without revealing
    cy = hy + 98 + 146 + 36 + CH // 2 + 20
    xs = (300, 540, 780)
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
    sy = ey + 62
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
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, "cover.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "card11", "card12", "card13"),
                       page_bg="#000", collision_ignore=[("card11", "card12"), ("card12", "card13"), ("title", "badge"), ("h2", "card12"), ("h2", "card11"), ("h2", "card13")])
    print("cover done ->", OUT)
asyncio.run(main())
