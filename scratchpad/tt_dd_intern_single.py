"""DISCO DIWALI single static post (feed 1080x1350) + single story (1080x1920, arg: story), companion to the 2-slide halftone carousel
(tt_dd_intern.py): halftone ground, lowercase headline with photo thumbnails inside parentheses, a grid of captioned .jpg "files", one quote line.
Feed = 3x2 files, story = 3x3. Teaser: no tickets, date, venue or price. Real DD photos only (crops).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_intern_single.py [story]  -> out/collaterals/dd_intern_single[_story].png
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("it", os.path.join(ROOT, "scratchpad", "tt_dd_intern.py"))
it = importlib.util.module_from_spec(sp); sp.loader.exec_module(it)
tt, core, B, W, H, STORY, FOOT = it.tt, it.core, it.B, it.W, it.H, it.STORY, it.FOOT
ORCHID, CTA_FILL, INK, WHITE = it.ORCHID, it.CTA_FILL, it.INK, it.WHITE
crop, thumb, halftone_bg = it.crop, it.thumb, it.halftone_bg
OY = 230 if STORY else 0

TILES = [("dance_floor.jpg", "dance", (400, 250, 1100, 761)), ("balloon_arch.jpg", "decor", (0, 250, 640, 717)), ("disco_blocks.jpg", "decor", (980, 380, 1480, 745)),
         ("full_fit.jpg", "group", (350, 230, 1000, 704)), ("red_curtain.jpg", "decor", (480, 350, 1000, 730)), ("cassette.jpg", "decor", (150, 740, 650, 1105)),
         ("hands_up.jpg", "dance", (420, 290, 900, 640)), ("chandeliers.jpg", "dance", (300, 0, 860, 409)), ("golden_hour.jpg", "group", (0, 0, 700, 511))]


def build():
    els = []
    bg = halftone_bg("dance", "#0B66FF", focus=(0.55, 0.4), dot_gain=0.7, lift=0.55)
    FS = 82
    t1, t2, t3 = crop("dance", (400, 300, 1000, 687)), crop("group", (400, 250, 1000, 637)), crop("decor", (980, 380, 1480, 703))
    paren = lambda inner: f'<span style="font-weight:300">(</span>{inner}<span style="font-weight:300">)</span>'
    ty = 105 + OY
    rows, TH, PITCH = (2, 320, 395) if STORY else (2, 245, 320)
    gy = ty + 2 * FS * 1.14 + 150
    TW = (W - 140 - 2 * 28) / 3
    html = (f'<style>{tt.FONT_CSS}</style><img src="{bg}" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:0">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.5) 0%,rgba(0,0,0,.2) 45%,rgba(0,0,0,.45) 100%);z-index:1"></div>'
            f'<div class="measure" data-tag="title" style="position:absolute;left:30px;width:{W - 60}px;top:{ty}px;text-align:center;font-family:var(--e);font-weight:500;font-size:{FS}px;line-height:1.14;letter-spacing:-0.035em;color:{WHITE};white-space:nowrap;z-index:6">'
            f'what’s {paren(thumb(t1))} coming {paren(thumb(t2))}<br>to Disco Diwali {paren(thumb(t3))}</div>'
            f'<div class="measure" data-tag="sub" style="position:absolute;left:200px;width:{W - 400}px;top:{ty + 2 * FS * 1.14 + 28}px;text-align:center;font-family:var(--e);font-weight:400;font-size:32px;color:{WHITE};z-index:6">a first look inside the folder</div>')
    els += [("title", 30, ty, W - 60, 2 * FS * 1.14), ("sub", 200, ty + 2 * FS * 1.14 + 28, W - 400, 38)]
    for i, (name, key, box) in enumerate(TILES[:rows * 3]):
        r, c = divmod(i, 3)
        x = 70 + c * (TW + 28); y = gy + r * PITCH
        html += (f'<div class="measure" data-tag="t{i}" style="position:absolute;left:{x}px;top:{y}px;width:{TW}px;height:{TH}px;box-sizing:border-box;border:5px solid {CTA_FILL};border-radius:10px;background:url({crop(key, box)}) center/cover no-repeat;z-index:6"></div>'
                 f'<div class="measure" data-tag="c{i}" style="position:absolute;left:{x}px;top:{y + TH + 10}px;width:{TW}px;font-family:var(--e);font-weight:500;font-size:22px;color:{WHITE};white-space:nowrap;z-index:6">• {name}</div>')
        els += [(f"t{i}", x, y, TW, TH), (f"c{i}", x, y + TH + 10, TW, 26)]
    qy = gy + rows * PITCH + 4
    html += (f'<div class="measure" data-tag="quote" style="position:absolute;left:140px;width:{W - 280}px;top:{qy}px;text-align:center;font-family:var(--e);font-weight:400;font-size:34px;letter-spacing:-0.02em;color:{WHITE};z-index:6">“good music, good people, good lights”</div>')
    els.append(("quote", 140, qy, W - 280, 42))
    ly = H - FOOT - 27 - 76
    html += (f'<div class="measure" data-tag="logo" style="position:absolute;left:27px;top:{ly}px;height:76px;padding:0 24px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;z-index:9"><img src="{core.LOGO}" style="height:40px"></div>')
    els.append(("logo", 27, ly, 330, 76))
    cw, ch = 330, 70; cx, cy = W - 27 - cw, H - FOOT - 27 - ch
    html += (f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:28px;color:{INK};z-index:9">STAY TUNED</div>')
    els.append(("cta", cx, cy, cw, ch))
    return B.page(W, H, "#000", html, grain=False), els


async def main():
    html, els = build()
    out = "out/collaterals/dd_intern_single" + ("_story" if STORY else "") + ".png"
    async with B.session():
        await B.render(html, out, W, H, elements=els, page_bg="#000", expect_hero=False, margin=12, crop_tags=tuple(f"t{i}" for i in range(9)))
    print("done", out)

asyncio.run(main())
