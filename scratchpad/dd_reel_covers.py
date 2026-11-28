"""DISCO DIWALI reel covers (1080x1920) from two supplied event photos, on the format's own skeleton (discodiwali.py primitives):
ink ground, string lights, gold dust + film grain, LIVE badge top left, the DISCO DIWALI lockup (with ball) as the hero, the supplied edition line,
and the user's copper STICKERS (sample_outputs/disco_diwali_stickers/). No date, time, venue, price or lineup (none shown on any cover, per the carousel rule).
Cover A: crowd photo sunk into ink under the lockup (photo pushed down so the raised hands clear the title), copper heart + star low.
Cover B: tree photo in a tilted gold-edged card under the lockup, copper diya + star on its corners.
Everything that matters sits inside the 4:5 grid crop (y 285..1635); the top 200px stays clear of Instagram's profile bar.
CONSENT: the crowd photo shows apparent minors and there is no consent record (brain/DISCO_DIWALI.md). Check before posting.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_reel_covers.py"""
import asyncio, base64, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; W, H = 1080, 1920
OUT = os.path.join(ROOT, "out", "discodiwali", "reel_covers")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GOLD = "rgba(214,170,90,.95)"
from PIL import Image
def sticker_uri(name, w):
    im = Image.open(os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers", name)).convert("RGBA")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS); b = io.BytesIO(); im.save(b, "PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode(), im.size
def photo(path, maxw=1800):
    return dd.photo_uri(os.path.join(ROOT, path), maxw)
def stick(tag, name, x, y, w, z=26):
    u, (sw, sh) = sticker_uri(name, 700)
    h = round(sh * w / sw)
    return (f'<img data-tag="{tag}" src="{u}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;z-index:{z};filter:drop-shadow(0 12px 18px rgba(0,0,0,.6))">', (tag, x, y, w, h))
def common():
    parts, els = [], []
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:245px;width:150px;z-index:20">'); els.append(("badge", 40, 245, 150, 142))
    vw = 700; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2 + 40; vy = 250
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    ey = vy + vh + 26
    parts.append(f'<div data-tag="edition" style="position:absolute;left:0;width:{W}px;top:{ey}px;text-align:center;font-family:var(--d);font-weight:700;font-size:38px;line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">Masquerade Sangeet Edition</div>')
    els.append(("edition", 150, ey, 780, 40))
    return parts, els, ey + 40
def overlays():
    return (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
            f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:40;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:41;mix-blend-mode:screen;opacity:.35;pointer-events:none">')
def cover_a():
    parts, els, bottom = common()
    shift = 330                                                 # photo pushed down so the raised hands clear the title
    ph = (f'<div data-tag="plate" style="position:absolute;inset:0;background:#000;z-index:0"></div>'
          f'<img data-tag="plate" src="{photo("training_samples/reel_cover_photos/crowd_dance.jpg")}" style="position:absolute;left:0;top:{shift}px;width:{W}px;height:{H - shift}px;object-fit:cover;object-position:70% 50%;z-index:1;'
          f'filter:contrast(1.08) saturate(1.05) brightness(.95);-webkit-mask-image:linear-gradient(180deg,transparent 0%,#000 26%);mask-image:linear-gradient(180deg,transparent 0%,#000 26%)">'
          f'<div data-tag="plate" style="position:absolute;inset:0;z-index:2;pointer-events:none;background:linear-gradient(180deg,rgba(6,5,24,.55) 0%,rgba(6,5,24,.30) 45%,rgba(6,5,24,.25) 70%,rgba(0,0,0,.88) 100%)"></div>')
    s1, e1 = stick("heart", "copper_heart.png", 40, 1330, 330)
    s2, e2 = stick("star", "copper_star.png", 770, 1340, 270)
    return ph + "".join(parts) + s1 + s2 + overlays(), els + [e1, e2]
def cover_b():
    parts, els, bottom = common()
    cw, ch = 640, 780; cx, cy = 540, 1215
    card = (f'<div data-tag="card" style="position:absolute;left:{cx - cw // 2}px;top:{cy - ch // 2}px;width:{cw}px;height:{ch}px;border:6px solid {GOLD};border-radius:28px;overflow:hidden;'
            f'box-shadow:0 22px 48px rgba(0,0,0,.7);transform:rotate(2deg);z-index:10">'
            f'<img src="{photo("training_samples/reel_cover_photos/tree_gifts.jpg")}" style="width:100%;height:100%;object-fit:cover;object-position:46% 62%;filter:brightness(1.1) saturate(1.05)"></div>')
    s1, e1 = stick("diya", "copper_diya.png", 150, 1520, 300)
    s2, e2 = stick("star", "copper_star.png", 730, 790, 240)
    ground = ('<div data-tag="plate" style="position:absolute;inset:0;background:#000;z-index:0"></div>'
              f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:1350px;object-fit:cover;z-index:1;opacity:.9">'
              f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - 1350}px;width:{W}px;height:1350px;object-fit:cover;z-index:1;opacity:.9;transform:scaleY(-1);'
              f'-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%)">')
    bx = dd.B.lay.rotated_bbox(cx - cw // 2, cy - ch // 2, cw, ch, 2) if hasattr(dd.B, "lay") else (cx - cw // 2 - 12, cy - ch // 2 - 12, cw + 24, ch + 24)
    return ground + "".join(parts) + card + s1 + s2 + overlays(), els + [("card",) + tuple(bx), e1, e2]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, fn in (("cover_a_crowd", cover_a), ("cover_b_tree", cover_b)):
            inner, els = fn()
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, name + ".png"), W, H, elements=els, containers=("card",), bleed_tags=("plate", "lights"), crop_tags=("plate",),
                           page_bg="#000", collision_ignore=[("title", "badge"), ("heart", "star"), ("card", "diya"), ("card", "star"), ("card", "edition"), ("title", "star")])
    print("done ->", OUT)
asyncio.run(main())
