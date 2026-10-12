"""DISCO DIWALI 2-slide carousel from the user's inspo (2026-10-11): slide 1 = halftone duotone photo with a lowercase headline whose
parentheses hold inline photo thumbnails ("what's (photo) coming (photo) / to Disco Diwali (photo)"); slide 2 = halftone duotone ground
with a handle-style title and a 3x3 grid of "files" (photo tiles captioned with .jpg names) and a quote line.
TerraThon colours: slide 1 TT blue halftone, slide 2 orchid halftone, both on black. Real DD photos only (tiles are CROPS of the user's 3
photos, so file names describe what each crop shows). Teaser: no tickets, date, venue, price. Feed 1080x1350 + story 1080x1920 (arg: story).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_intern.py [story]  -> out/collaterals/dd_intern[_story]/
"""
import asyncio, base64, importlib.util, io, os, sys
import numpy as np
from PIL import Image, ImageOps
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(sp); sp.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
ORCHID, CTA_FILL, INK, WHITE = tt.ORCHID, tt.CTA_FILL, tt.INK, tt.WHITE
STORY = len(sys.argv) > 1 and sys.argv[1] == "story"
H = 1920 if STORY else 1350
FOOT = 270 if STORY else 0
P = {n: Image.open(f"engine/assets/terrathon/dd_photos/{n}.jpg").convert("RGB") for n in ("dance", "decor", "group")}


def b64(im, q=88):
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def crop(key, box, w=640):
    im = P[key].crop(box); return b64(im.resize((w, round(w * im.height / im.width)), Image.LANCZOS))


def halftone_bg(key, color, focus=(0.5, 0.5), cell=11, dot_gain=0.78, lift=1.0):
    """Duotone halftone: `color` ground, black dots that grow with the shadows (the inspo's newsprint look)."""
    im = ImageOps.autocontrast(P[key].convert("L"), cutoff=2)
    s = max(W / im.width, H / im.height); nw, nh = round(im.width * s), round(im.height * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = round((nw - W) * focus[0]); y0 = round((nh - H) * focus[1])
    L = np.asarray(im.crop((x0, y0, x0 + W, y0 + H)), dtype=np.float32) / 255.0
    L = np.power(L, lift)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    c, s_ = np.cos(np.pi / 4), np.sin(np.pi / 4)
    u = xx * c + yy * s_; v = -xx * s_ + yy * c
    cu = np.mod(u, cell) - cell / 2; cv = np.mod(v, cell) - cell / 2
    d = np.sqrt(cu * cu + cv * cv)
    r = cell * dot_gain * np.sqrt(np.clip(1 - L, 0, 1))
    a = np.clip(r - d + 0.6, 0, 1)[..., None]                 # 1 = black dot
    col = np.array([int(color[i:i + 2], 16) for i in (1, 3, 5)], dtype=np.float32)
    out = col * (1 - a)
    return b64(Image.fromarray(out.astype(np.uint8)), 90)


def footer(idx, total, els):
    ly = H - FOOT - 27 - 76
    f = (f'<div class="measure" data-tag="logo" style="position:absolute;left:27px;top:{ly}px;height:76px;padding:0 24px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;z-index:9"><img src="{core.LOGO}" style="height:40px"></div>')
    els.append(("logo", 27, ly, 330, 76))
    cw, ch = 150, 54; cx, cy = W - 27 - cw, H - FOOT - 27 - ch
    f += (f'<div class="measure" data-tag="idx" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:24px;color:{INK};z-index:9">{idx:02d} / {total:02d}</div>')
    els.append(("idx", cx, cy, cw, ch))
    return f


def thumb(src):
    return f'<span style="display:inline-block;width:1.7em;height:0.98em;vertical-align:-0.1em;margin:0 .05em;background:url({src}) center/cover no-repeat;border-radius:6px;box-shadow:0 0 0 3px {CTA_FILL}"></span>'


def slide1():
    els = []
    bg = halftone_bg("dance", "#0B66FF", focus=(0.55, 0.4), dot_gain=0.7, lift=0.55)
    t1, t2, t3 = crop("dance", (400, 300, 1000, 687)), crop("group", (400, 250, 1000, 637)), crop("decor", (980, 380, 1480, 703))
    FS = 88
    cy = 640 if not STORY else 900
    paren = lambda inner: f'<span style="font-weight:300">(</span>{inner}<span style="font-weight:300">)</span>'
    html = (f'<style>{tt.FONT_CSS}</style>'
            f'<img src="{bg}" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:0">'
            f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(0,0,0,.42) 0%,rgba(0,0,0,.18) 55%,rgba(0,0,0,.35) 100%);z-index:1"></div>'
            f'<div class="measure" data-tag="title" style="position:absolute;left:40px;width:{W - 80}px;top:{cy}px;text-align:center;font-family:var(--e);font-weight:500;font-size:{FS}px;line-height:1.14;letter-spacing:-0.035em;color:{WHITE};white-space:nowrap;z-index:6">'
            f'what’s {paren(thumb(t1))} coming {paren(thumb(t2))}<br>to Disco Diwali {paren(thumb(t3))}</div>'
            f'<div class="measure" data-tag="sub" style="position:absolute;left:200px;width:{W - 400}px;top:{cy + 2 * FS * 1.14 + 36}px;text-align:center;font-family:var(--e);font-weight:400;font-size:34px;color:{WHITE};z-index:6">a first look inside the folder</div>')
    els += [("title", 40, cy, W - 80, 2 * FS * 1.14), ("sub", 200, cy + 2 * FS * 1.14 + 36, W - 400, 40)]
    html += footer(1, 2, els)
    return B.page(W, H, "#000", html, grain=False), els


def slide2():
    els = []
    bg = halftone_bg("decor", "#C23AD6", focus=(0.5, 0.45))
    TITLE_Y, GRID_Y, TH, PITCH, QY = (95, 290, 215, 262, 1110) if not STORY else (250, 410, 250, 300, 1330)
    tiles = [("dance_floor.jpg", "dance", (400, 250, 1100, 761)), ("chandeliers.jpg", "dance", (300, 0, 860, 409)), ("hands_up.jpg", "dance", (420, 290, 900, 640)),
             ("balloon_arch.jpg", "decor", (0, 250, 640, 717)), ("red_curtain.jpg", "decor", (480, 350, 1000, 730)), ("disco_blocks.jpg", "decor", (980, 380, 1480, 745)),
             ("full_fit.jpg", "group", (350, 230, 1000, 704)), ("golden_hour.jpg", "group", (0, 0, 700, 511)), ("cassette.jpg", "decor", (150, 740, 650, 1105))]
    html = (f'<style>{tt.FONT_CSS}</style>'
            f'<img src="{bg}" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:0">'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.4) 0%,rgba(0,0,0,.1) 40%,rgba(0,0,0,.3) 100%);z-index:1"></div>'
            f'<div class="measure" data-tag="handle" style="position:absolute;left:64px;top:{TITLE_Y}px;font-family:var(--e);font-weight:400;font-size:104px;letter-spacing:-0.04em;line-height:1;color:{WHITE};z-index:6">disco_diwali_</div>')
    els.append(("handle", 64, TITLE_Y, 680, 104))
    TW = (W - 140 - 2 * 28) / 3
    for i, (name, key, box) in enumerate(tiles):
        r, c = divmod(i, 3)
        x = 70 + c * (TW + 28); y = GRID_Y + r * PITCH
        html += (f'<div class="measure" data-tag="t{i}" style="position:absolute;left:{x}px;top:{y}px;width:{TW}px;height:{TH}px;box-sizing:border-box;border:5px solid {CTA_FILL};border-radius:10px;background:url({crop(key, box)}) center/cover no-repeat;z-index:6"></div>'
                 f'<div class="measure" data-tag="c{i}" style="position:absolute;left:{x}px;top:{y + TH + 10}px;width:{TW}px;font-family:var(--e);font-weight:500;font-size:22px;color:{WHITE};white-space:nowrap;z-index:6">• {name}</div>')
        els += [(f"t{i}", x, y, TW, TH), (f"c{i}", x, y + TH + 10, TW, 26)]
    html += (f'<div class="measure" data-tag="quote" style="position:absolute;left:140px;width:{W - 280}px;top:{QY}px;text-align:center;font-family:var(--e);font-weight:400;font-size:36px;letter-spacing:-0.02em;color:{WHITE};z-index:6">“good music, good people, good lights”</div>')
    els.append(("quote", 140, QY, W - 280, 44))
    html += footer(2, 2, els)
    return B.page(W, H, "#000", html, grain=False), els


async def main():
    outdir = "out/collaterals/dd_intern" + ("_story" if STORY else ""); os.makedirs(outdir, exist_ok=True)
    async with B.session():
        for n, fn in (("1", slide1), ("2", slide2)):
            html, els = fn()
            out = f"{outdir}/dd_intern_{n}.png"
            await B.render(html, out, W, H, elements=els, page_bg="#000", expect_hero=False, margin=12, crop_tags=("t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"))
            print("done", out)

if __name__ == "__main__":
    asyncio.run(main())
