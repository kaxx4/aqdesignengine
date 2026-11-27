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
    line("kicker", kicker, ty - 50, 32, 400, 34, ".34em")
    line("title", title, ty, tsize, 700, tsize)
    parts.append(f'<div data-tag="idx" style="position:absolute;right:64px;top:64px;font-family:var(--d);font-weight:400;font-size:26px;letter-spacing:.2em;color:#f6dc9a;-webkit-text-stroke:4px #000;paint-order:stroke fill;z-index:40">{idx:02d} / {N:02d}</div>')
    els.append(("idx", W - 64 - 160, 64, 160, 28))
    return "".join(parts), els


def slides():
    s = []
    s.append(slide(2, [frame(2, 80, 190, 560, 720, -4, 12, 50, 40), frame(11, 540, 470, 450, 580, 5, 13, 50, 55)], "Starry Night", "The tree", 130))
    s.append(slide(3, [frame(7, 80, 130, 400, 470, -4, 12, 50, 45), frame(14, 590, 150, 400, 470, 4, 13, 50, 45),
                       frame(8, 100, 630, 400, 420, 3, 14, 50, 55), frame(9, 580, 650, 400, 420, -3, 15, 50, 40)], "Starry Night", "Together", 110, 1176))
    s.append(slide(4, [frame(12, 70, 170, 460, 610, -3, 12, 50, 50), frame(10, 560, 250, 450, 540, 4, 13, 50, 50), frame(15, 330, 670, 420, 380, -2, 14, 50, 50)],
                   "Starry Night", "Under the lights", 90))
    s.append(slide(5, [frame(3, 60, 170, 500, 660, -4, 12, 50, 35), frame(4, 580, 190, 430, 400, 5, 13, 50, 50), frame(5, 560, 620, 400, 480, -3, 14, 50, 40)],
                   "Starry Night", "On the decks", 100))
    ss = 150
    star = f'<div data-tag="star" style="position:absolute;left:{(W - ss) // 2}px;top:40px;z-index:40">{cp.star(ss, 0)}</div>'
    s.append(slide(6, [frame(0, 70, 230, 560, 520, -3, 12, 50, 50), frame(1, 520, 330, 480, 640, 4, 13, 50, 50)], "Throwback", "Starry Night", 114, 1100, star))
    return s


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els = st.poster()
    jobs = [(inner, els, "slide_01.png")] + [(i, e, f"slide_{k + 2:02d}.png") for k, (i, e) in enumerate(slides())]
    async with B.session():
        for inner, els, name in jobs:
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, name), W, H, elements=els, bleed_tags=("plate",), crop_tags=("plate", "frame"), page_bg="#000", collision_ignore=[])
    print("done")
asyncio.run(main())
