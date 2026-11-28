"""STARRY NIGHT THROWBACK CAROUSEL, 6 slides 1080x1350, Disco Diwali branding, photos from the user's Drive folder `SN 24`.
Slide 1 is the tree poster (dd_starry_throwback.py). 2-5 are themed photo slides (the tree / together / under the lights / on the decks), 6 closes on the group shots.
Captions only describe the photo they sit under. Facts: Starry Night, Christmas carnival, December 2024. No venue, price, count. Index tag NN / 06 is true by construction.
Consent caveat: apparent minors, no consent record. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_starry_carousel.py"""
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_starry_throwback as st
dd, B, cp, W, H, GOLD, STROKE = st.dd, st.B, st.cp, st.W, st.H, st.GOLD, st.STROKE
OUT = os.path.join(st.ROOT, "out", "discodiwali", "starry_throwback")
N = 6


def frame(pi, x, y, w, h, rot, z, fx=50, fy=50, foot=46, pad=14):
    return (f'<div data-tag="frame" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#f1ead8;border:2px solid #000;box-sizing:border-box;'
            f'transform:rotate({rot}deg);box-shadow:6px 8px 0 rgba(0,0,0,.55);z-index:{z}">'
            f'<div data-tag="frame" style="position:absolute;left:{pad - 2}px;top:{pad - 2}px;width:{w - 2 * pad}px;height:{h - pad - foot}px;overflow:hidden;background:#000">'
            f'<img src="{st.photo_uri(pi, 1100)}" style="width:100%;height:100%;object-fit:cover;object-position:{fx}% {fy}%;filter:contrast(1.05) saturate(.95) brightness(1.08)"></div></div>')


def slide(idx, frames, kicker, title, tsize, ty=1168, extra=""):
    parts, els = [st.ground()] + frames, []
    parts.append(extra)
    def line(tag, txt, top, size, weight, h, ls="0"):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;letter-spacing:{ls};{STROKE}z-index:40">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    if title:
        line("kicker", kicker, ty - 50, 32, 400, 34, ".34em")
        line("title", title, ty, tsize, 700, tsize)
    parts.append(f'<div data-tag="idx" style="position:absolute;right:64px;top:64px;font-family:var(--d);font-weight:400;font-size:26px;letter-spacing:.2em;color:#f6dc9a;-webkit-text-stroke:4px #000;paint-order:stroke fill;z-index:40">{idx:02d} / {N:02d}</div>')
    els.append(("idx", W - 64 - 160, 64, 160, 28))
    return "".join(parts), els


import random
RED = "#d1352b"


def ptxt(tag, txt, top, size, weight=700, ls="0", left=0, w=W, h=None, anchor="center", els=None, extra=""):
    els.append((tag, left + 40, top, w - 80, h or size))
    return (f'<div data-tag="{tag}" style="position:absolute;left:{left}px;width:{w}px;top:{top}px;text-align:{anchor};font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1;'
            f'text-transform:uppercase;white-space:nowrap;letter-spacing:{ls};{STROKE}{extra}z-index:40">{txt}</div>')


def idx_tag(idx):
    return (f'<div data-tag="idx" style="position:absolute;right:64px;top:64px;font-family:var(--d);font-weight:400;font-size:26px;letter-spacing:.2em;color:#f6dc9a;'
            f'-webkit-text-stroke:4px #000;paint-order:stroke fill;z-index:40">{idx:02d} / {N:02d}</div>')


def photo_box(pi, x, y, w, h, fx=50, fy=50, clip="", z=14, rot=0, extra=""):
    return (f'<div data-tag="frame" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;overflow:hidden;background:#000;z-index:{z};transform:rotate({rot}deg);{clip}{extra}">'
            f'<img src="{st.photo_uri(pi, 1100)}" style="width:100%;height:100%;object-fit:cover;object-position:{fx}% {fy}%;filter:contrast(1.05) saturate(.95) brightness(1.08)"></div>')


def torn(w, h, top=False, bottom=False, seed=1):
    rnd = random.Random(seed); pts = []
    for x in range(0, w + 1, 14):
        pts.append((x, 6 + rnd.random() * 22 if top else 0))
    for x in range(w, -1, -14):
        pts.append((x, h - 6 - rnd.random() * 22 if bottom else h))
    return "clip-path:polygon(" + ",".join(f"{a}px {b:.0f}px" for a, b in pts) + ");"


def envelope_slide():
    els, parts = [], [st.ground()]
    TEX = f"background:url({dd.uri('copper_texture.jpg')}) center/cover;"
    top_y, ap, bot = 760, 900, 1270
    # back, open top flap, photos, front panels, seal
    parts.append(f'<div data-tag="frame" style="position:absolute;left:90px;top:{top_y}px;width:900px;height:{bot - top_y}px;{TEX}filter:brightness(.45);z-index:9"></div>')
    parts.append(f'<div data-tag="frame" style="position:absolute;left:90px;top:{top_y - 190}px;width:900px;height:190px;{TEX}filter:brightness(.38);clip-path:polygon(0 100%,100% 100%,50% 0);z-index:9"></div>')
    for (pi, x, y, w, h, rot, z, fx, fy) in [(2, 70, 200, 380, 470, -9, 12, 50, 40), (8, 340, 110, 400, 490, 3, 13, 50, 55), (15, 640, 200, 380, 470, 8, 12, 50, 55), (7, 190, 400, 360, 440, -4, 14, 50, 45), (12, 560, 420, 340, 420, 5, 14, 50, 55)]:
        parts.append(frame(pi, x, y, w, h, rot, z, fx, fy))
    for tag, poly in (("l", "0 0,50% 140px,0 100%"), ("r", "100% 0,50% 140px,100% 100%"), ("b", "0 100%,50% 140px,100% 100%")):
        parts.append(f'<div data-tag="frame" style="position:absolute;left:90px;top:{top_y}px;width:900px;height:{bot - top_y}px;{TEX}filter:brightness(.5) saturate(.75);clip-path:polygon({poly});z-index:20"></div>')
    parts.append(f'<svg data-tag="frame" style="position:absolute;left:90px;top:{top_y}px;width:900px;height:{bot - top_y}px;z-index:21" viewBox="0 0 900 {bot - top_y}"><path d="M0 0L450 140L0 {bot - top_y}M900 0L450 140L900 {bot - top_y}M0 {bot - top_y}L450 140L900 {bot - top_y}" fill="none" stroke="#e8c46a" stroke-opacity=".75" stroke-width="3"/></svg>')
    parts.append(f'<div data-tag="seal" style="position:absolute;left:{540 - 52}px;top:{ap - 52}px;width:104px;height:104px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#d9453a,#8e1c1c 70%);border:3px solid #000;box-shadow:5px 6px 0 rgba(0,0,0,.55);z-index:26">'
                 f'<div style="position:absolute;inset:0">{st.sparkle(26, 26, 52)}</div></div>')
    parts.append(ptxt("kicker", "Throwback", 1034, 34, 700, ".34em", els=els))
    parts.append(ptxt("title", "Starry Night", 1086, 104, 700, els=els))
    parts.append(f'<div data-tag="star" style="position:absolute;left:14px;top:690px;z-index:40">{cp.star(150, -14)}</div>')
    parts.append(f'<div data-tag="star" style="position:absolute;left:870px;top:1150px;z-index:40">{cp.star(140, 12)}</div>')
    parts.append(idx_tag(2))
    return "".join(parts), els


def gift_slide():
    els, parts = [], [st.ground()]
    parts.append('<svg width="0" height="0" style="position:absolute"><filter id="rough" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="7"/>'
                 '<feDisplacementMap in="SourceGraphic" scale="11"/></filter></svg>')
    X0, X1, Y0, Y1, XM, YM = 96, 984, 400, 1236, 540, 818
    cells = [(12, X0, Y0, XM - X0, YM - Y0, 50, 55), (11, XM, Y0, X1 - XM, YM - Y0, 50, 50), (15, X0, YM, XM - X0, Y1 - YM, 50, 50), (9, XM, YM, X1 - XM, Y1 - YM, 40, 40)]
    for pi, x, y, w, h, fx, fy in cells:
        parts.append(photo_box(pi, x, y, w, h, fx, fy, z=12))
    sw = 22
    parts.append(f'<svg data-tag="frame" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:20;filter:url(#rough)" viewBox="0 0 {W} {H}" fill="none" stroke="{RED}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
                 f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}"/><path d="M{XM} {Y0}V{Y1}M{X0} {YM}H{X1}"/>'
                 f'<path d="M{XM} {Y0}C{XM - 60} {Y0 - 40} {XM - 190} {Y0 - 110} {XM - 190} {Y0 - 40}C{XM - 190} {Y0 + 10} {XM - 80} {Y0 - 6} {XM} {Y0}"/>'
                 f'<path d="M{XM} {Y0}C{XM + 60} {Y0 - 40} {XM + 190} {Y0 - 110} {XM + 190} {Y0 - 40}C{XM + 190} {Y0 + 10} {XM + 80} {Y0 - 6} {XM} {Y0}"/>'
                 f'<path d="M{XM - 10} {Y0 - 8}L{XM - 70} {Y0 + 60}M{XM + 10} {Y0 - 8}L{XM + 70} {Y0 + 60}"/></svg>')
    parts.append(ptxt("title", "Merry Christmas", 130, 84, 700, els=els))
    parts.append(f'<div data-tag="star" style="position:absolute;left:30px;top:236px;z-index:40">{cp.star(110, -10)}</div>')
    parts.append(f'<div data-tag="star" style="position:absolute;left:920px;top:1210px;z-index:41">{cp.star(110, 10)}</div>')
    parts.append(ptxt("sub", "Starry Night &middot; Christmas carnival", 1270, 30, 400, ".1em", els=els))
    parts.append(idx_tag(3))
    return "".join(parts), els


def arc_slide():
    els, parts = [], [st.ground()]
    cw, ch = 400, 440
    for pi, x, y, top_t, bot_t, seed, fx, fy in [(6, 120, 150, False, True, 3, 62, 50), (16, 560, 150, False, True, 5, 50, 45), (1, 120, 650, True, False, 8, 50, 40), (8, 560, 650, True, False, 11, 50, 55)]:
        parts.append(photo_box(pi, x, y, cw, ch, fx, fy, clip=torn(cw, ch, top_t, bot_t, seed), z=12, extra="filter:drop-shadow(0 0 0 #000);"))
    path = "M 30 905 C 260 690 430 650 640 690 C 860 735 980 560 1000 150"
    parts.append(f'<svg data-tag="arc" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:30" viewBox="0 0 {W} {H}"><defs><path id="ap" d="{path}"/></defs>'
                 f'<text font-family="NeutralFace,var(--d)" font-weight="700" font-size="46" letter-spacing="14" fill="#fff" stroke="#000" stroke-width="7" paint-order="stroke fill" style="font-family:var(--d)">'
                 f'<textPath href="#ap" startOffset="3%">YOU HAD TO BE THERE</textPath></text></svg>')
    els.append(("arc", 30, 150, 980, 760))
    parts.append(ptxt("title", "@ngo.aquaterra", 1170, 34, 400, ".12em", left=300, w=480, els=els))
    parts.append(f'<div data-tag="star" style="position:absolute;left:52px;top:1090px;z-index:40">{cp.star(170, -8)}</div>')
    parts.append(f'<svg data-tag="arrow" style="position:absolute;left:760px;top:1140px;width:200px;height:90px;z-index:40" viewBox="0 0 200 90" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-dasharray="3 12"><path d="M8 52C50 30 100 70 168 46"/></svg>')
    parts.append(f'<svg data-tag="arrowhead" style="position:absolute;left:900px;top:1160px;width:60px;height:60px;z-index:40" viewBox="0 0 60 60"><path d="M6 8L50 28L14 52Z" fill="{GOLD}" transform="rotate(-8 30 30)"/></svg>')
    parts.append(idx_tag(4))
    return "".join(parts), els


def slides():
    out = [envelope_slide(), gift_slide(), arc_slide()]
    out.append(slide(5, [frame(3, 60, 170, 500, 660, -4, 12, 50, 35), frame(4, 580, 190, 430, 400, 5, 13, 50, 50), frame(5, 560, 620, 400, 480, -3, 14, 50, 40)],
                     "Starry Night", "On the decks", 100))
    ss = 150
    star = f'<div data-tag="star" style="position:absolute;left:{(W - ss) // 2}px;top:40px;z-index:40">{cp.star(ss, 0)}</div>'
    out.append(slide(6, [frame(0, 70, 230, 560, 520, -3, 12, 50, 50), frame(1, 520, 330, 480, 640, 4, 13, 50, 50)], "Throwback", "Starry Night", 114, 1100, star))
    return out


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els = st.poster()
    jobs = [(inner, els, "slide_01.png")] + [(i, e, f"slide_{k + 2:02d}.png") for k, (i, e) in enumerate(slides())]
    async with B.session():
        for inner, els, name in jobs:
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, name), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "frame"), page_bg="#000", collision_ignore=[])
    print("done")
asyncio.run(main())
