"""DISCO DIWALI thank-you-to-all-the-stalls poster, feed (1080x1350) and story (1080x1920), 2026-11-20.
Five user-supplied stall photos (engine/assets/img/events/stalls-2026-11/) as a BRICK of tilted gold-edged print frames (the teaser_trio mechanism, five frames in two rows,
the second row sitting in the gaps of the first) under a THANK YOU headline. Diya ground, LIVE badge, copper diya sticker, lockup as footer mark. No pill, no link.
Copy: THANK YOU / TO ALL OUR STALLS. Only the three READABLE stall names could be printed and none is: the photos carry the names on their own signs (Meet Cute, Nandu Jee, Mad Over
Donuts); the jewellery and patches stalls have no readable name, so no name is invented. No date, price or venue. Photos: user-supplied, consent unconfirmed (Nandu Jee shows two vendors' faces).
Row 1 (overlapped from below) holds the photos whose bottoms matter least; row 2 sits on top and holds Meet Cute (its sign is at the bottom) and the donut sign (a zoomed crop on the sign).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_thanks_stalls.py -> out/discodiwali/thanks_stalls/{feed,story}.png"""
import asyncio, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B; W = 1080
import dd_copper as CP
OUT = os.path.join(ROOT, "out", "discodiwali", "thanks_stalls")
IMG = os.path.join(ROOT, "engine", "assets", "img", "events", "stalls-2026-11")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GOLD = "#D9B25F"


def rot_box(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return (round(cx - bw / 2), round(cy - bh / 2), round(bw), round(bh))


def ground(H):
    plate = lambda top, extra="": (f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{top}px;width:{W}px;height:1350px;object-fit:cover;z-index:1;{extra}">')
    p = '<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>' + plate(0)
    if H > 1350:
        p += plate(H - 1350, "transform:scaleY(-1);-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);")
    return p + (f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
                f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
                f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def poster(H):
    story = H > 1350
    parts, els = [ground(H)], []
    bx, by, bw = 40, (210 if story else 40), 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    ss = 160 if not story else 190
    sx, sy = 1040 - ss, (50 if not story else 215)
    parts.append(f'<div data-tag="sticker" style="position:absolute;left:{sx}px;top:{sy}px;z-index:12">{CP.diya(ss, 8)}</div>'); els.append(("sticker", sx, sy, ss, ss))

    def line(tag, txt, top, fsize, weight, h):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    if story:
        hs, hy = 150, 430
        line("head1", "Thank you", hy, hs, 700, hs)
        sub_y = hy + hs + 8
        fw, step, row1_y, row2_dy = 300, 330, sub_y + 90, 320
    else:
        hs, hy = 150, 205
        line("head1", "Thank you", hy, hs, 700, hs)
        sub_y = hy + hs + 8
        fw, step, row1_y, row2_dy = 290, 320, sub_y + 80, 300
    line("sub", "to all our stalls", sub_y, 44, 400, 46)
    fh = round(fw * 4 / 3); pad = 10; iw = fw - 2 * pad; ih = fh - 2 * pad
    x0 = (W - (fw + 2 * step)) // 2
    # (file, row, col, tilt, extra img css). row 2 sits on top of row 1; the donut photo is a zoomed crop on the sign (the sign's centre is ~ (.50W, .66H) of the photo)
    zoom = f"position:absolute;width:{round(iw * 1.4)}px;height:{round(ih * 1.4)}px;left:{round(iw / 2 - .50 * iw * 1.4)}px;top:{round(ih / 2 - .66 * ih * 1.4)}px;"
    frames = [("nandu_jee", 0, 0, -5, ""), ("jewellery", 0, 1, 3, ""), ("patches", 0, 2, -3, ""),
              ("meet_cute", 1, 0, 4, ""), ("mad_over_donuts", 1, 1, -4, zoom)]
    labels = []
    for i, (f, row, col, tilt, extra) in enumerate(frames):
        x = x0 + col * step + (step // 2 if row else 0)
        if row == 1: x = x0 + step // 2 + col * step
        y = row1_y + row * row2_dy
        img_css = (extra or "width:100%;height:100%;object-fit:cover;") + "display:block;"
        parts.append(f'<div data-tag="frame" style="position:absolute;left:{x}px;top:{y}px;width:{fw}px;height:{fh}px;box-sizing:border-box;background:#F4EFE0;border:4px solid {GOLD};border-radius:10px;'
                     f'box-shadow:10px 12px 0 rgba(0,0,0,.65);transform:rotate({tilt}deg);z-index:{10 + row * 3 + col}">'
                     f'<div data-tag="frame" style="position:absolute;left:{pad - 4}px;top:{pad - 4}px;width:{iw}px;height:{ih}px;overflow:hidden">'
                     f'<img src="{dd.photo_uri(os.path.join(IMG, f + ".jpg"), 900)}" style="{img_css}filter:brightness(1.12) contrast(1.05)"></div></div>')
        lab = f"frame{i}"; labels.append(lab); els.append((lab,) + rot_box(x + fw / 2, y + fh / 2, fw, fh, tilt))
    vw = 300 if story else 190
    t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2
    last = max(e[2] + e[4] for e in els if e[0].startswith("frame"))
    vy = (last + 44) if story else H - 40 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els, vy + vh, labels


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            inner, els, bottom, labels = poster(H)
            print(f"[{name}] last element ends at y={bottom} of {H}")
            ign = [(a, b) for i, a in enumerate(labels) for b in labels[i + 1:]]
            tp = [("headline", "#fff", "#1a1020", 150, True), ("sub", "#fff", "#1a1020", 44, False)]
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate", "frame"),
                           page_bg="#000", collision_ignore=ign, text_pairs=tp)
    print("done ->", OUT)
asyncio.run(main())
