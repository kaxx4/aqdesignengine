"""STARRY NIGHTS reel covers (1080x1920), Workflow C bespoke build, real photos.
Two covers, one grammar: ink night ground, cream NeutralFace STARRY, one Instrument Serif italic accent word
("nights", sky), a lemon constellation, one mono sticker that describes THIS photo, logo top-left, handle top-right.
Everything that matters sits inside the 4:5 grid crop (y 285..1635) because Instagram shows a reel cover as 4:5 in the profile grid.
Cover A (crowd): full-bleed photo, title low over a dark scrim.  Cover B (tree): photo as a tilted card on the ink ground, title above, overlapping its top edge.
ADAPTATIONS (precedence ladder, section 2): hero accent is SKY (events dept, core.accent_for) not the lemon of the fairy lights; lemon is the small star colour only.
The crowd photo is 1920x1280, so a 9:16 crop is upscaled 1.5x; grain is left on to carry it.
No date, venue or count appears: none was supplied (real-assets-only, section 9).
Run: PYTHONIOENCODING=utf-8 python scratchpad/starry_reel_covers.py"""
import asyncio, base64, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); ED = os.path.join(ROOT, "engine"); sys.path.insert(0, ED)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ED, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
W, H = 1080, 1920; M = 64
SKY = core.accent_for("events"); LEMON = core.ACCENTS[2]; INK = core.INK; CREAM = core.CREAM
OUT = os.path.join(ROOT, "out", "starry_night")
def jpg(p): return "data:image/jpeg;base64," + base64.b64encode(open(os.path.join(ROOT, p), "rb").read()).decode()
def star(kind, x, y, s, col, rot=0, z=12):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;z-index:{z};filter:drop-shadow(0 3px 6px rgba(0,0,0,.55))">{dd.stamp(kind, col, rot=rot)}</div>')
def constellation(pts, z=12):
    """pts: [(cx, cy, size, kind)] joined by a dashed cream line, drawn under the stars."""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    d = " ".join(f"{p[0]},{p[1]}" for p in pts)
    html = (f'<svg style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:{z - 1};filter:drop-shadow(0 2px 4px rgba(0,0,0,.6))" viewBox="0 0 {W} {H}">'
            f'<polyline points="{d}" fill="none" stroke="{CREAM}" stroke-width="3" stroke-dasharray="3 12" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    els = []
    for i, (cx, cy, s, k) in enumerate(pts):
        html += star(k, round(cx - s / 2), round(cy - s / 2), s, LEMON, rot=(i * 17) % 40 - 20, z=z)
        els.append((f"star{i}", round(cx - s / 2), round(cy - s / 2), s, s))
    return html, els
def chip(tag, txt, x, y, rot, bg, w, h=64, z=30):
    fg = core.text_on(bg)
    return (f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;'
            f'background:{bg};color:{fg};border:3px solid {INK};border-radius:999px;box-shadow:5px 5px 0 {INK};transform:rotate({rot}deg);'
            f'font-family:var(--m);font-weight:700;font-size:22px;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;z-index:{z}">{txt}</div>')
def furniture():
    lg = B.logo(dark=True, x=M, y=304)
    hd = (f'<span data-tag="handle" style="position:absolute;right:{M}px;top:310px;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.08em;color:#fff;'
          f'text-shadow:0 2px 8px rgba(0,0,0,.7);z-index:20">@ngo.aquaterra</span>')
    return lg + hd, [("logo", M, 304, 190, 36), ("handle", W - M - 230, 308, 230, 26)]

async def sizes():
    r = await B.measure_text([dict(text="STARRY", font="d", size=100, weight=900),
                              dict(text="nights", font="s", size=100, style="italic")])
    return r
def title(top, s1, g1, g2, rot=-3, z=25):
    """STARRY (cream, display) + nights (serif italic, sky) overlapping its base. s1 = STARRY font px, measured glyph box g1=(w,h) at 100px."""
    tw = round(g1["text_w"] * s1 / 100); th = round(g1["glyph_h"] * s1 / 100)
    s2 = round(s1 * 0.92); nw = round(g2["text_w"] * s2 / 100)
    nx = W - M - nw - 10
    ny = top + th - round(s2 * 0.30)
    h = (f'<div data-tag="t1" style="position:absolute;left:{M}px;top:{top}px;font-family:var(--d);font-weight:900;font-size:{s1}px;line-height:1;text-transform:uppercase;white-space:nowrap;color:{CREAM};'
         f'text-shadow:0 6px 0 {INK};z-index:{z}">STARRY</div>'
         f'<div data-tag="t2" style="position:absolute;left:{nx}px;top:{ny}px;font-family:var(--s);font-style:italic;font-size:{s2}px;line-height:1;white-space:nowrap;color:{core.on_dark(SKY, s2)};'
         f'transform:rotate({rot}deg);text-shadow:0 5px 0 {INK};z-index:{z + 1}">nights</div>')
    return h, [("t1", M, top, tw, th), ("t2",) + tuple(lay.rotated_bbox(nx, ny + round(s2 * .12), nw, round(s2 * .62), rot))], ny + s2

def cover_a(g1, g2):
    s1 = min(380, int(952 / (g1["text_w"] / 100))); 
    fx, els = furniture()
    top = 1170
    t, te, bottom = title(top, s1, g1, g2)
    con, ce = constellation([(560, 440, 40, "sparkle"), (690, 520, 64, "star"), (790, 430, 34, "sparkle"), (905, 560, 52, "sparkle"), (980, 450, 30, "star")])
    inner = (f'<img src="{jpg("training_samples/starry_night/crowd_dance.jpg")}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:70% 50%;filter:brightness(.92) saturate(1.1) contrast(1.05)">'
             f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.78) 0%,rgba(10,10,10,0) 24%,rgba(10,10,10,0) 44%,rgba(10,10,10,.93) 78%,rgba(10,10,10,.97) 100%);z-index:3"></div>'
             + fx + con + t + chip("chip", "Hands up", 80, top + 20 - 92, -6, SKY, 230) )
    els += ce + te + [("chip", 80, top - 72, 230, 64)]
    return inner, els, "#0A0A0A"

def cover_b(g1, g2):
    s1 = min(380, int(952 / (g1["text_w"] / 100)))
    fx, els = furniture()
    top = 420
    t, te, bottom = title(top, s1, g1, g2, rot=-3)
    cw, ch = 800, 980; cx, cy = 540, 1110
    ol = core.outline_of(INK)
    card = (f'<div data-tag="card" style="position:absolute;left:{cx - cw // 2}px;top:{cy - ch // 2}px;width:{cw}px;height:{ch}px;border:6px solid {ol};border-radius:36px;overflow:hidden;'
            f'box-shadow:16px 16px 0 {SKY};transform:rotate(2.5deg);z-index:10">'
            f'<img src="{jpg("training_samples/starry_night/tree_gifts.jpg")}" style="width:100%;height:100%;object-fit:cover;object-position:46% 62%;filter:brightness(1.12) saturate(1.1)"></div>')
    con, ce = constellation([(78, 800, 44, "star"), (62, 930, 28, "sparkle"), (84, 1070, 36, "sparkle")], z=12)
    con2, ce2 = constellation([(985, 840, 34, "sparkle"), (1010, 960, 54, "star"), (990, 1080, 30, "sparkle")], z=12)
    con3, ce3 = constellation([(160, 1760, 40, "sparkle"), (330, 1820, 28, "sparkle"), (560, 1770, 52, "star"), (790, 1830, 30, "sparkle"), (940, 1750, 38, "sparkle")], z=12)
    con4, ce4 = constellation([(120, 130, 34, "sparkle"), (300, 200, 26, "sparkle"), (700, 120, 46, "star"), (900, 210, 30, "sparkle")], z=12)
    bx = lay.rotated_bbox(cx - cw // 2, cy - ch // 2, cw, ch, 2.5)
    inner = (f'<div style="position:absolute;inset:0;background:{INK}"></div>' + fx + card + con + con2 + con3 + con4 + t
             + chip("chip", "Fairy lights on", 120, 1560, -5, LEMON, 330))
    els += [("card",) + tuple(bx)] + te + ce + ce2 + ce3 + ce4 + [("chip", 120, 1560, 330, 64)]
    return inner, els, INK

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        g1, g2 = await sizes()
        print("STARRY@100:", g1["text_w"], g1["glyph_h"], " nights@100:", g2["text_w"])
        for name, fn, ground in (("cover_a_crowd", cover_a, INK), ("cover_b_tree", cover_b, INK)):
            inner, els, _ = fn(g1, g2)
            await B.render(B.page(W, H, ground, inner, grain=True), os.path.join(OUT, name + ".png"), W, H, elements=els,
                           containers=("card",), page_bg=ground, bleed_tags=("photo",),
                           collision_ignore=[("t1", "t2"), ("t2", "card"), ("t1", "card"), ("chip", "card"), ("chip", "t1"), ("chip", "t2")])
asyncio.run(main())
