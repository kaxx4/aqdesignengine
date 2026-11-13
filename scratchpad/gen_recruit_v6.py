"""AQ recruitment v6 (mix and match): the same one message ("A STUDENT [did a real thing] THIS."), pushed visually and made to feel handmade.

Owner feedback (2026-11-13): v5 was "too boring and basic", it needs to be "more visually pushing and feel more natural".
v5 was a template: logo, bar, line, pill. v6 puts the effort into the PHOTOGRAPH and the MATERIALS:
  * type that lives IN the scene: chalk written on the real blackboard, type tucked BEHIND people (real cut-outs),
    spray paint on the stall wall;
  * scrapbook materials: torn paper strips, tape, a taped print, hand-drawn marker circles and arrows;
  * film grain, a warm grade and a vignette on every photo, nothing perfectly aligned.
Same constants as the rest of the campaign: the logo, a department chip, one real fact, the URL. Brand craft is kept in
the paper strips (hard ink shadow) and the chips; cream/ink/lane colours only.

ADAPTATIONS (precedence ladder): chalk/spray/marker are built from SVG filters on brand type, not new fonts. Handwritten
annotations are set in Instrument Serif italic (the brand's voice face). Cut-outs are made with rembg (u2net_human_seg,
isnet-general-use) from real AQ photos and stored in engine/assets/img/cutouts/; the dark group shots segment badly so
they stay full photos.
"""
import os, sys, asyncio, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
core = K.core
W = 1080
INK, CREAM, PAPER = K.INK, K.CREAM, K.PAPER
M = 64
OUT = "out/recruit_nov2026/v6"
IMG = K.IMG

# ---------------------------------------------------------------- raster helpers
def cover_img(path, w, h, fx=.5, fy=.5, zoom=1.0, s=1.5, grade=True):
    """cover-crop any image (keeps alpha for cut-outs). Cut-outs were made from <=1500px thumbnails of the same photo, so a
    cut-out and its source crop identically as long as both use the same fx, fy, zoom."""
    im = Image.open(IMG + path)
    im = im.convert("RGBA") if path.endswith(".png") and "cutouts" in path else im.convert("RGB")
    tw, th = round(w * s), round(h * s)
    k = max(tw / im.width, th / im.height) * zoom
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = round((im.width - tw) * fx); y = round((im.height - th) * fy)
    im = im.crop((x, y, x + tw, y + th))
    if grade and im.mode == "RGB":
        im = ImageEnhance.Contrast(im).enhance(1.10); im = ImageEnhance.Color(im).enhance(1.12)
    return im

def clean_alpha(im, lo=90, gain=1.7):
    r, g, b, a = im.split()
    a = a.point(lambda v: 0 if v < lo else min(255, int((v - lo) * gain)))
    a = a.filter(ImageFilter.GaussianBlur(1.1))
    return Image.merge("RGBA", (r, g, b, a))

def jpg(im, q=88):
    return K.uri(im.convert("RGB"), "JPEG", q)

def png(im):
    return K.uri(im, "PNG")

# ---------------------------------------------------------------- svg filters + materials
DEFS = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="chalk" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="w"/>
 <feDisplacementMap in="SourceGraphic" in2="w" scale="7" result="d"/>
 <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="9" result="n"/>
 <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -2.6 1.95" result="m"/>
 <feComposite in="d" in2="m" operator="in" result="c"/>
 <feGaussianBlur in="c" stdDeviation="0.6"/></filter>
<filter id="spray" x="-10%" y="-20%" width="120%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="2" result="w"/>
 <feDisplacementMap in="SourceGraphic" in2="w" scale="9" result="d"/>
 <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="2" seed="5" result="n"/>
 <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -3.2 2.5" result="m"/>
 <feComposite in="d" in2="m" operator="in" result="c"/>
 <feGaussianBlur in="d" stdDeviation="9" result="halo"/>
 <feComponentTransfer in="halo" result="halo2"><feFuncA type="linear" slope=".5"/></feComponentTransfer>
 <feMerge><feMergeNode in="halo2"/><feMergeNode in="c"/></feMerge></filter>
<filter id="marker" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="7" result="w"/>
 <feDisplacementMap in="SourceGraphic" in2="w" scale="5"/></filter>
</defs></svg>"""

def grain(op=.55):
    return (f'<div style="position:absolute;inset:0;{core.GRAIN};mix-blend-mode:multiply;opacity:{op};pointer-events:none;z-index:95"></div>')

def vignette(a=.45):
    return (f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,{a}) 100%);z-index:90;pointer-events:none"></div>')

def jag(w, h, seed, amp=7, step=26, sides="tb"):
    """polygon() points for a torn-paper rectangle (jagged top and bottom edges, slightly ragged ends)."""
    rnd = random.Random(seed); pts = []
    nx = max(2, int(w / step))
    for i in range(nx + 1):
        pts.append((w * i / nx, rnd.uniform(0, amp) if "t" in sides else 0))
    pts.append((w - rnd.uniform(0, amp * .6), h * .5))
    for i in range(nx, -1, -1):
        pts.append((w * i / nx, h - (rnd.uniform(0, amp) if "b" in sides else 0)))
    pts.append((rnd.uniform(0, amp * .6), h * .5))
    return "polygon(" + ",".join(f"{x:.1f}px {y:.1f}px" for x, y in pts) + ")"

def strip(text_html, x, y, w, h, bg, fg, rot=-2, seed=1, size=100, z=40, tag="strip", extra="", padx=26, ls=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);filter:drop-shadow(5px 6px 0 rgba(10,10,10,.85));z-index:{z}">'
            f'<div style="width:100%;height:100%;background:{bg};clip-path:{jag(w, h, seed)};"></div>'
            f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{padx}px;top:0;height:{h}px;line-height:{h}px;white-space:nowrap;font-family:var(--d);font-weight:900;'
            f'font-size:{size}px;letter-spacing:{ls}em;text-transform:uppercase;color:{fg};{extra}">{text_html}</div></div>')

def tape(x, y, w=170, h=52, rot=-6, color="#F2E4B3", seed=3, z=60):
    rnd = random.Random(seed)
    pts = [(0, rnd.uniform(0, 8)), (w * .5, rnd.uniform(0, 4)), (w, rnd.uniform(0, 8)), (w - rnd.uniform(2, 8), h * .5), (w, h - rnd.uniform(0, 8)), (w * .5, h - rnd.uniform(0, 4)), (0, h - rnd.uniform(0, 8)), (rnd.uniform(2, 8), h * .5)]
    cp = "polygon(" + ",".join(f"{a:.1f}px {b:.1f}px" for a, b in pts) + ")"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);background:{color};opacity:.88;clip-path:{cp};z-index:{z};'
            f'box-shadow:none"></div>')

def marker_path(d, color="#FF4D2E", sw=9, z=70):
    return (f'<svg style="position:absolute;inset:0;z-index:{z};pointer-events:none" width="{W}" height="2000" viewBox="0 0 {W} 2000">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" filter="url(#marker)"/></svg>')

def scribble_ellipse(cx, cy, rx, ry, seed=1, turns=1.12):
    rnd = random.Random(seed); pts = []
    n = 70; ph = rnd.uniform(0, 6.28)
    for i in range(n + 1):
        t = ph + 2 * math.pi * turns * i / n
        k = 1 + .045 * math.sin(3 * t + seed) + rnd.uniform(-.012, .012) + .05 * i / n
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def scribble_arrow(x0, y0, x1, y1, bend=60, seed=2):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2 - bend
    a = math.atan2(y1 - my, x1 - mx)
    h1 = (x1 - 34 * math.cos(a - .5), y1 - 34 * math.sin(a - .5)); h2 = (x1 - 34 * math.cos(a + .5), y1 - 34 * math.sin(a + .5))
    return f"M{x0},{y0} Q{mx},{my} {x1},{y1} M{h1[0]:.1f},{h1[1]:.1f} L{x1},{y1} L{h2[0]:.1f},{h2[1]:.1f}"

def note(text, x, y, size=50, color="#FFFFFF", rot=-4, w=None, z=75, shadow=True):
    sh = "text-shadow:0 2px 14px rgba(0,0,0,.7);" if shadow else ""
    wc = f"width:{w}px;" if w else "white-space:nowrap;"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{wc}transform:rotate({rot}deg);font-family:var(--s);font-style:italic;font-size:{size}px;line-height:{round(size*1.05)}px;'
            f'color:{color};{sh}z-index:{z}">{text}</div>')

def chip(dept, x_right=W - M, y=56):
    lab, col = K.LANE[dept]
    w = int(len(lab) * 15 * .66 + 36)
    return K.t(lab, x_right - w, y, 15, color=core.text_on(col), font="m", weight=700, ls=.06, upper=True, tag="lane", z=96,
               extra=f"background:{col};border:3px solid #0A0A0A;box-shadow:4px 4px 0 #0A0A0A;padding:6px 12px;")

def fact_tape(text, x, y, w=None, rot=-1.2, z=80):
    wd = f"width:{w}px;" if w else "white-space:nowrap;"
    return (f'<div class="measure" data-tag="fact" style="position:absolute;left:{x}px;top:{y}px;{wd}transform:rotate({rot}deg);background:#F6EFD8;color:#0A0A0A;font-family:var(--m);font-weight:700;font-size:21px;'
            f'line-height:30px;padding:10px 18px;box-shadow:4px 5px 0 rgba(10,10,10,.85);z-index:{z}">{text}</div>')

def url_pill(y, x=M):
    s = K.URL; w = int(len(s) * 15.6 + 80)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:60px;border-radius:999px;background:{INK};z-index:96"></div>'
            + K.t(s, x + 36, y + 17, 23, color=K.LEM, font="m", weight=700, ls=.02, z=97, upper=False, tag="url"))

async def fit(lines, maxw, cap=300):
    ws = await K.mw([dict(text=s, font="d", size=200, weight=900) for s in lines])
    return min(cap, int(200 * maxw / max(ws))), ws

def big_type(lines, x, y, size, color, z, step=.9, filt=None, extra="", align="left", boxw=None):
    out = []
    for i, ln in enumerate(lines):
        al = f"width:{boxw}px;text-align:{align};" if boxw else ""
        out.append(f'<div class="measure" data-tag="bt{i}" style="position:absolute;left:{x}px;top:{y + round(i*size*step)}px;{al}white-space:nowrap;font-family:var(--d);font-weight:900;font-size:{size}px;'
                   f'line-height:{round(size*step)}px;color:{color};text-transform:uppercase;z-index:{z};{("filter:url(#"+filt+");") if filt else ""}{extra}">{ln}</div>')
    return "".join(out)

def img_layer(src, w, h, z, extra=""):
    return f'<img src="{src}" style="position:absolute;left:0;top:0;width:{w}px;height:{h}px;z-index:{z};{extra}">'

async def done(name, parts, H, bg="#111"):
    html = K.page(DEFS + "".join(parts) + grain(), H, bg=bg)
    await K._render(name, html, H, None, None)
    print("rendered", name)

def safe(H, story): return 200 if story else 0
def bottom(H, story): return 250 if story else 0

# ================================================================= shared mix-and-match pieces (from the owner's inspo)
def blob_svg(x, y, size, color, seed=3, stroke=INK, sw=5, rot=0, z=6, lobes=8, wob=.2):
    d = K.shapes.blob(seed, lobes=lobes, r=46, wobble=wob)
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg);z-index:{z};overflow:visible" width="{size}" height="{size}" viewBox="0 0 100 100">'
            f'<path d="{d}" fill="{INK}" transform="translate(3.2,3.8)"/><path d="{d}" fill="{color}" stroke="{stroke}" stroke-width="{sw/ size*100:.2f}" stroke-linejoin="round"/></svg>')

def halftone_over(w, h, z=3, op=.12, size=6):
    return (f'<div style="position:absolute;inset:0;width:{w}px;height:{h}px;background-image:radial-gradient(#0A0A0A 1.2px,transparent 1.7px);background-size:{size}px {size}px;'
            f'mix-blend-mode:multiply;opacity:{op};z-index:{z};pointer-events:none"></div>')

def misreg(src, w, h, dx=8, dy=6, color_filter="sepia(1) saturate(6) hue-rotate(290deg)", op=.28, z=2):
    return (f'<img src="{src}" style="position:absolute;left:{dx}px;top:{dy}px;width:{w}px;height:{h}px;filter:{color_filter};mix-blend-mode:multiply;opacity:{op};z-index:{z}">')

def window(x, y, w, h, c, label, side="tr", z=30, blend="multiply", op=.9):
    lw = int(len(label) * 8.1 + 22); th = 26
    tx = x + w - lw if side in ("tr", "br") else x
    ty = y - th if side in ("tr", "tl") else y + h
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{c};mix-blend-mode:{blend};opacity:{op};z-index:{z}"></div>'
            f'<div style="position:absolute;left:{tx}px;top:{ty}px;height:{th}px;padding:0 10px;background:{c};z-index:{z+1};font-family:var(--e);font-weight:600;font-size:14.5px;line-height:{th}px;color:#0A0A0A;white-space:nowrap">{label}</div>')

def glass_pill(x, y, label, col, rot=0, icon="sparkle", z=85):
    wpx = int(len(label) * 16 + 98)
    ic = (f'<div style="position:absolute;left:10px;top:10px;width:44px;height:44px;border-radius:50%;background:{col};display:flex;align-items:center;justify-content:center">'
          f'<div style="position:relative;width:26px;height:26px">{K.dd.stamp(icon, "#fff")}</div></div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wpx}px;height:64px;border-radius:18px;background:rgba(255,255,255,.84);border:2px solid rgba(255,255,255,.9);'
            f'z-index:{z};transform:rotate({rot}deg);box-shadow:0 6px 18px rgba(0,0,0,.3);font-family:var(--e);font-weight:600;font-size:25px;line-height:64px;color:#0A0A0A;padding-left:66px">{ic}{label}</div>')

def bubble(text, x, y, rot=-3, size=30, z=86, tail="left", w=None):
    t_ = ('<div style="position:absolute;left:36px;bottom:-22px;width:30px;height:30px;background:#fff;border-right:4px solid #0A0A0A;border-bottom:4px solid #0A0A0A;transform:rotate(45deg) skew(8deg,8deg)"></div>' if tail == "left" else
          '<div style="position:absolute;right:36px;bottom:-22px;width:30px;height:30px;background:#fff;border-right:4px solid #0A0A0A;border-bottom:4px solid #0A0A0A;transform:rotate(45deg) skew(8deg,8deg)"></div>')
    wd = f"width:{w}px;" if w else "white-space:nowrap;"
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;{wd}transform:rotate({rot}deg);background:#fff;border:4px solid #0A0A0A;border-radius:30px;padding:12px 24px;'
            f'font-family:var(--e);font-weight:600;font-size:{size}px;line-height:{round(size*1.2)}px;color:#0A0A0A;box-shadow:6px 7px 0 #0A0A0A;z-index:{z}">{text}{t_}</div>')

def alpha_bbox(im, thr=128):
    a = np.asarray(im.split()[3]) > thr
    ys, xs = np.where(a)
    return (xs.min() / 1.5, ys.min() / 1.5, xs.max() / 1.5, ys.max() / 1.5)

async def chrome(P, dept, top, base, fact=None, fx=M, fw=None, frot=-1.5):
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip(dept, y=56 + top))
    if fact: P.append(fact_tape(fact, fx, base - 190, w=fw, rot=frot))
    P.append(url_pill(base - 100))

# ================================================================= 1. TEACH: chalk on the real board + behind people + cast windows
async def teach(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/10_teaching-abc-board.jpg", W, H, fy=.35)
    cut = clean_alpha(cover_img("cutouts/teach.png", W, H, fy=.35, grade=False), lo=110)
    bx0, by0, bx1, by1 = alpha_bbox(cut); bw, bh = bx1 - bx0, by1 - by0
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 7, 5, op=.18, z=2),
         f'<div style="position:absolute;inset:0;background:rgba(8,18,12,.42);z-index:3"></div>', halftone_over(W, H, 4, .07), vignette(.5)]
    lines = ["A STUDENT", "TAUGHT", "THIS."]
    size, ws = await fit(lines, W - 2 * M + 60, cap=330)
    y0 = 120 + top
    P.append(big_type(lines, M - 20, y0, size, "#F4F1E6", 10, step=.88, filt="chalk"))
    P.append(img_layer(png(cut), W, H, 20))
    P.append(window(int(bx0), int(by0 + bh * .04), int(bw * .36), int(bh * .62), K.TOM, "A STUDENT : the teacher", "tr", blend="overlay", op=1))
    P.append(window(int(bx0 + bw * .42), int(by0 + bh * .3), int(bw * .56), int(bh * .62), K.LEM, "THE CLASS : eyes on the board", "tl", blend="overlay", op=1))
    await chrome(P, "welfare", top, base, "about 70% of our welfare work is teaching.")
    P.append(tape(M + 30, base - 206, 120, 40, -8))
    await done("b1_teach" + ("_story" if story else ""), P, H)

# ================================================================= 2. EVENTS: hero + blob + bleed type + cut-out depth + glass pills
async def events(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    src = "events/summer-aq-turns-five/07_group-portrait-pink-light.jpg"
    bg = cover_img(src, W, H, fy=.55)
    cut = clean_alpha(cover_img("cutouts/five_group.png", W, H, fy=.55, grade=False), lo=100)
    bx0, by0, bx1, by1 = alpha_bbox(cut)
    P = [img_layer(jpg(bg), W, H, 1), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(40,10,60,.6),rgba(40,10,60,.15) 50%,rgba(20,5,30,.65));z-index:2"></div>', halftone_over(W, H, 3, .07), vignette(.35)]
    bsz = int(max(bx1 - bx0, by1 - by0) * 1.25)
    P.append(blob_svg(int((bx0 + bx1) / 2 - bsz / 2), int((by0 + by1) / 2 - bsz / 2) + 20, bsz, K.LEM, seed=5, sw=6, z=8, rot=12))
    lines = ["STUDENTS", "THREW", "THIS."]
    size, ws = await fit(lines, W - 2 * M + 60, cap=360)
    size = int(size * 1.18)                     # bleed: let the canvas edge cut the type
    y0 = 140 + top
    P.append(big_type(lines, -34, y0, size, K.SKY, 12, step=.86, extra="-webkit-text-stroke:5px #0A0A0A;paint-order:stroke fill;text-shadow:11px 11px 0 #0A0A0A;"))
    P.append(img_layer(png(cut), W, H, 20))
    P.append(glass_pill(740, int(by0) + 40, "DJ", K.GRAPE, -5, "star")); P.append(glass_pill(60, int(by0 + (by1 - by0) * .55), "Vendors", K.SKY, 4, "sparkle"))
    P.append(glass_pill(720, int(by0 + (by1 - by0) * .7), "Sponsors", K.PINK, -3, "heart"))
    await chrome(P, "events", top, base, "disco diwali 2.0: 550 registrations, 10+ small businesses.", fw=600)
    P.append(tape(W - 300, base - 200, 130, 42, 7, seed=8))
    await done("b2_events" + ("_story" if story else ""), P, H)

# ================================================================= 3. DOGS: riso halftone + sticker strips + marker + speech tags
async def dogs(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/08_dog-drive-bhowanipur.jpg", W, H, fy=.5)
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 9, 7, op=.3, z=2),
         f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.3),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 45%,rgba(0,0,0,.6));z-index:3"></div>', halftone_over(W, H, 4, .09, 5), vignette(.4)]
    t1, t2, t3 = "A STUDENT", "FED THESE", "DOGS."
    ws = await K.mw([dict(text=t, font="d", size=150, weight=900) for t in (t1, t2, t3)])
    sy = 128 + top
    P.append(strip(t1, M - 14, sy, int(ws[0] + 60), 150, "#F6EFD8", INK, -2.5, 3, 150, tag="s1"))
    P.append(strip(t2, M + 60, sy + 140, int(ws[1] + 60), 150, K.MINT, INK, 1.5, 5, 150, tag="s2", z=41))
    P.append(strip(t3, M + 6, sy + 280, int(ws[2] + 60), 150, K.LEM, INK, -1, 9, 150, tag="s3", z=42))
    ccy = H * (.64 if not story else .62) + (0 if not story else 40)
    P.append(marker_path(scribble_ellipse(560, ccy, 400, 235, seed=4), "#FFC700", 10))
    P.append(bubble("edition 53", 640, ccy + 215, -4, 42))
    P.append(bubble("first run january 2022", 70, ccy + 235, 3, 26, tail="right"))
    await chrome(P, "welfare", top, base)
    P.append(tape(M + 470, sy - 14, 130, 40, -5, seed=11))
    await done("b3_dogs" + ("_story" if story else ""), P, H)

# ================================================================= 4. CRFTD: giant serif + spray + riso + sticker tags
async def crftd(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/12_roots-stall-novus-tee.jpg", W, H, fy=.3)
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 8, 6, op=.22, z=2),
         f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.4),rgba(0,0,0,.05) 35%,rgba(0,0,0,.1) 55%,rgba(0,0,0,.68));z-index:3"></div>', halftone_over(W, H, 4, .08, 5), vignette(.35)]
    lines = ["a student", "sprayed", "this."]
    ws = await K.mw([dict(text=l, font="s", size=220, weight=400, style="normal") for l in lines])
    size = int(220 * min(1.0, (W - 2 * M + 40) / max(ws)))
    stepp = int(size * .84)
    y0 = base - 260 - stepp * 3 + 40
    for i, ln in enumerate(lines):
        col = "#FFFFFF" if i != 1 else "rgba(255,255,255,0)"
        P.append(f'<div class="measure" data-tag="sf{i}" style="position:absolute;left:{M-6}px;top:{y0 + i*stepp}px;white-space:nowrap;font-family:var(--s);font-size:{size}px;line-height:{stepp}px;color:{col};z-index:30;'
                 f'text-shadow:0 4px 28px rgba(0,0,0,.5)">{ln}</div>')
    # the verb is SPRAYED on top, in tomato
    P.append(f'<div style="position:absolute;left:{M-6}px;top:{y0 + stepp}px;white-space:nowrap;font-family:var(--s);font-style:italic;font-size:{size}px;line-height:{stepp}px;color:{K.TOM};z-index:31;filter:url(#spray)">sprayed</div>')
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("crftd", y=56 + top))
    P.append(strip("SCHOOL FESTS", M - 10, 140 + top, 420, 76, "#F6EFD8", INK, -2.5, 31, 40, tag="t1", padx=18))
    P.append(strip("300 WALK-INS AT NOVUS", M + 60, 140 + top + 70, 620, 76, K.LEM, INK, 1.5, 33, 40, tag="t2", padx=18))
    P.append(fact_tape("crftd, formerly roots. every rupee of profit funds a welfare drive.", M, base - 190, w=640, rot=-1.5))
    P.append(url_pill(base - 100))
    await done("b4_crftd" + ("_story" if story else ""), P, H)

# ================================================================= 5. SUNDARBANS: cast windows + giant serif + sunset
async def sundarbans(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/09_sundarbans-sunset-group.png", W, H, fy=.55)
    bg = ImageEnhance.Brightness(K.mono(bg, contrast=1.15)).enhance(1.25)
    P = [img_layer(jpg(bg), W, H, 1), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.75),rgba(10,10,10,.25) 36%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55));z-index:2"></div>', vignette(.4)]
    lines = ["students ran this", "health camp."]
    ws = await K.mw([dict(text=l, font="s", size=220, weight=400, style="normal") for l in lines])
    size = int(220 * min(1.0, (W - 2 * M + 30) / max(ws))); stepp = int(size * .9)
    y0 = 128 + top
    for i, ln in enumerate(lines):
        it = "font-style:italic;" if i == 1 else ""
        P.append(f'<div class="measure" data-tag="sg{i}" style="position:absolute;left:{M-6}px;top:{y0 + i*stepp}px;white-space:nowrap;font-family:var(--s);{it}font-size:{size}px;line-height:{stepp}px;color:#FFF3E0;z-index:30;text-shadow:0 3px 24px rgba(0,0,0,.7)">{ln}</div>')
    off = 0 if not story else 150
    P.append(window(120, 770 + off, 330, 280, K.MINT, "120+ CHECKUPS", "tl", 40))
    P.append(window(470, 560 + off, 300, 300, K.LEM, "SUNDERBANS 8.0", "br", 40))
    P.append(window(730, 700 + off, 270, 280, K.PINK, "DECEMBER 2025", "tl", 40))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("welfare", y=56 + top))
    P.append(url_pill(base - 100))
    await done("b5_sundarbans" + ("_story" if story else ""), P, H)

# ================================================================= 6. COLLABS: taped print + blob + sticker strips
async def collabs(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{K.PINK};z-index:0"></div>']
    P.append(blob_svg(-120, 120 + top, 760, K.LEM, seed=9, sw=6, z=2, rot=20))
    P.append(blob_svg(520, base - 780, 640, K.SKY, seed=4, sw=6, z=2, rot=-10))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("collabs", y=56 + top))
    pw, ph = 880, int(880 * .72); px, py = (W - pw) // 2, 150 + top
    pic = cover_img("events/welfare-feed-2026/15_emami-science-city-lineup.png", pw, ph, fy=.5, fx=.5)
    P.append(f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw+36}px;height:{ph+36+70}px;transform:rotate(-2.2deg);background:#FBF8EE;box-shadow:10px 12px 0 rgba(10,10,10,.85);z-index:10;padding:18px">'
             f'<img src="{jpg(pic)}" style="width:{pw}px;height:{ph}px;object-fit:cover;display:block"></div>')
    P.append(note("science city", px + 40, py + ph + 14, 54, INK, -3.5, shadow=False, z=30))
    P.append(tape(px + 60, py - 22, 170, 52, -8, seed=2)); P.append(tape(px + pw - 150, py - 18, 170, 52, 6, seed=5))
    t1, t2 = "STUDENTS HOSTED", "30 KIDS"
    sz = 84; ws = await K.mw([dict(text=t, font="d", size=sz, weight=900) for t in (t1, t2)])
    sy = py + ph + 130
    P.append(strip(t1, M - 14, sy, int(ws[0] + 60), 104, "#F6EFD8", INK, -1.8, 21, sz, tag="c1", z=40))
    P.append(strip(t2, M + 120, sy + 98, int(ws[1] + 60), 104, K.LEM, INK, 1.6, 23, sz, tag="c2", z=41))
    P.append(marker_path(scribble_arrow(900, sy + 205, 760, sy + 150, bend=40), INK, 8))
    P.append(note("300 kits", 810, sy + 100, 46, "#FFFFFF", -5))
    P.append(fact_tape("with vishwajagriti and emami, at science city.", M, sy + 230, rot=-1))
    P.append(url_pill(base - 100))
    await done("b6_collabs" + ("_story" if story else ""), P, H, bg=K.PINK)

JOBS = {"teach": teach, "events": events, "dogs": dogs, "crftd": crftd, "sundarbans": sundarbans, "collabs": collabs}
STORY = {"teach", "dogs", "crftd", "sundarbans"}

async def main(only, stories=True):
    async with K.B.session():
        for k, fn in JOBS.items():
            if only and k not in only: continue
            await fn(False)
            if stories and k in STORY: await fn(True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    args = [a for a in sys.argv[1:] if a != "--feed"]
    asyncio.run(main(set(args) or None, stories="--feed" not in sys.argv))
