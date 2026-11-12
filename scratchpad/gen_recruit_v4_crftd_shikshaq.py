"""Recruitment campaign v4, Crftd + ShikshAQ lane pieces (4 pieces, feed 1080x1350).

  crftd_1     style 64b2248475fe76  halftone hero over a reversed word-mural, torn ribbon banner      lane crftd     T1
  crftd_2     style 2af2568a52cc92  sticker swarm landing in the gaps of a huge headline            lane crftd     T3
  shikshaq_1  style bf31ba49142543  signpost of colour-blocked labels + pattern-filled bubbles        lane shikshaq  T4
  shikshaq_2  style e7b32bd307aac4  centred workflow collage of overlapping cards, staged            lane shikshaq  T1

ADAPTATIONS (precedence ladder, CLAUDE.md section 2). Each is a hard brand rule beating a recipe, or a count that is a target.
  crftd_1   * recipe: one flat SATURATED ground. Brand: cream ground, accents as punctuation. Kept the MECHANISM (giant
              reversed word-mural bleeding off every edge, one halftone hero centred, torn ribbon carrying the headline)
              and set the mural in tomato ON cream rather than flooding the page in tomato.
            * hero is a REAL Crftd stall T-shirt photo (Novus), hand-cut with a polygon, then halftoned in PIL; the recipe's
              headphones/cassette is the reference's own subject.
            * colours: cream + tomato + ink + paper-white banner + lemon bolts = one more than the recipe's "exactly two plus
              paper"; lemon is the series-tab colour and the bolts are the recipe's own accent doodle.
  crftd_2   * dark ground is INK (a legitimate AQ ground), headline is cream not white, uppercase NeutralFace.
            * recipe: 8-9 badges. Made 9 (7 silhouettes). Sticker palette is the AQ accents.
            * the reference's tablet bezel is dropped; the poster is full-frame.
  shikshaq_1 * recipe: bubbles carry NO text. Mine each carry one cream label plate, because the piece has to say something
              true; the pattern still fills the bubble edge to edge around the plate.
            * recipe: exactly 5 sign colours and 3 bubble patterns. 5 and 3. The recipe's two cloud silhouettes kept.
  shikshaq_2 * the one QUIET style. Cards are typographic skeletons, NOT screenshots (real-assets-only rule: no fabricated UI).
            * pale field is a pale lemon panel on the cream page (ShikshAQ lane colour), not a new ground colour.
Companion art piece (CLAUDE.md standing rule) is OUTSTANDING: owned by the dispatching session, not built here.
"""
import os, sys, math, random, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

core, B, dd, shapes, tex = K.core, K.B, K.dd, K.shapes, K.tex
INK, CREAM, PAPER = K.INK, K.CREAM, K.PAPER
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = K.PINK, K.MINT, K.LEM, K.TOM, K.SKY, K.GRAPE, K.TEAL
W = 1080


def dood(kind, x, y, size, fill, rot=0, z=9, style="clean"):
    """K.doodle is broken in the shared kit (V.dood does not exist); same helper as CLAUDE.md section 6, via dd.stamp."""
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;z-index:{z}">'
            f'{dd.stamp(kind, fill, rot=rot, style=style)}</div>')


def nm(base, it):
    return base if it == 0 else f"{base}_v{it}"


def measure(items):
    return asyncio.run(B.measure_text(items))


def chrome(lane, H=1350, dark=False):
    """logo + series tab + lane chip, the campaign constants."""
    lg = K.logo_pill(dark=True) if dark else K.logo()
    return lg + K.series_tab() + K.lane_chip(lane)


# --------------------------------------------------------------------------- crftd_1
def halftone_tee():
    """Hand-cut the Novus stall shirt, then screen it: ink dots by darkness, tomato dots by spray saturation."""
    src = Image.open(K.IMG + K.PH["tee_novus"]).convert("RGB")
    poly = [(353, 320), (453, 287), (613, 273), (800, 277), (907, 347), (1053, 507), (1000, 593), (933, 627), (816, 653),
            (813, 747), (800, 933), (800, 1333), (789, 1373), (533, 1413), (253, 1387), (287, 1200), (300, 933), (296, 693),
            (240, 696), (173, 593), (187, 547), (267, 400)]
    x0, y0, x1, y1 = 150, 255, 1075, 1440
    crop = src.crop((x0, y0, x1, y1))
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).polygon([(x - x0, y - y0) for x, y in poly], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(3)).point(lambda v: 255 if v > 128 else 0)
    S = 1.0
    w, h = crop.size
    g = np.asarray(ImageOps.autocontrast(ImageOps.grayscale(crop), cutoff=1), dtype=np.float32) / 255
    hsv = np.asarray(crop.convert("HSV"), dtype=np.float32) / 255
    sat = hsv[..., 1]
    # screen builder
    def screen(field, cell, angle, colour, gain=1.0):
        out = Image.new("L", (w * 2, h * 2), 0); d = ImageDraw.Draw(out)
        ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        n = int(max(w, h) * 2 / cell) + 4
        for i in range(-n, n):
            for j in range(-n, n):
                gx, gy = i * cell, j * cell
                px, py = gx * ca - gy * sa + w / 2, gx * sa + gy * ca + h / 2
                if not (0 <= px < w and 0 <= py < h): continue
                v = float(field[int(py), int(px)]) * gain
                r = cell * 0.78 * math.sqrt(min(1, max(0, v)))
                if r < .6: continue
                d.ellipse([(px - r) * 2, (py - r) * 2, (px + r) * 2, (py + r) * 2], fill=255)
        return out.resize((w, h), Image.LANCZOS)
    dark = np.clip((0.52 - g) * 1.7, 0, 1)
    spray = np.clip((sat - 0.16) * 2.6, 0, 1) * (g > 0.30)
    ink_dots = screen(dark, 9, 45, INK)
    tom_dots = screen(spray * (1 - dark * .6), 9, 15, TOM)
    base = Image.new("RGB", (w, h), PAPER)
    base.paste(Image.new("RGB", (w, h), K.hexrgb(TOM)), mask=tom_dots)
    base.paste(Image.new("RGB", (w, h), K.hexrgb(INK)), mask=ink_dots)
    # rim: paper-white halo outside the cut, then an ink keyline outside that
    big = Image.new("L", (w + 80, h + 80), 0); big.paste(mask, (40, 40))
    rim = big.filter(ImageFilter.MaxFilter(21)).point(lambda v: 255 if v > 100 else 0)
    keyl = rim.filter(ImageFilter.MaxFilter(7)).point(lambda v: 255 if v > 100 else 0)
    shad = ImageChops.offset(keyl, 14, 16)
    canvas = Image.new("RGBA", big.size, (0, 0, 0, 0))
    canvas.paste(Image.new("RGBA", big.size, K.hexrgb(INK) + (255,)), mask=shad)
    canvas.paste(Image.new("RGBA", big.size, K.hexrgb(INK) + (255,)), mask=keyl)
    canvas.paste(Image.new("RGBA", big.size, K.hexrgb(LEM) + (255,)), mask=rim)
    fill = Image.new("RGBA", big.size, (0, 0, 0, 0)); fill.paste(base.convert("RGBA"), (40, 40))
    sub = Image.new("RGBA", big.size, (0, 0, 0, 0)); sub.paste(fill, mask=big)
    canvas = Image.alpha_composite(canvas, sub)
    return canvas


def torn_ribbon(w, h, seed=3):
    rnd = random.Random(seed)
    def edge(y0, flip):
        pts = []; x = 0
        while x <= w:
            pts.append((x, y0 + rnd.uniform(-9, 9) * flip)); x += rnd.uniform(14, 34)
        pts.append((w, y0 + rnd.uniform(-9, 9) * flip)); return pts
    top = edge(22, 1)
    bot = edge(h - 22, 1)[::-1]
    # swallowtail ends, as in the reference ribbon
    pts = top + [(w - 4, h * .5)] + bot + [(4, h * .5)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    return (f'<svg width="{w+24}" height="{h+24}" viewBox="-6 -6 {w+24} {h+24}" style="overflow:visible">'
            f'<path d="{d}" transform="translate(9,10)" fill="{INK}"/>'
            f'<path d="{d}" fill="{PAPER}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></svg>')


def crftd_1(it=1):
    H = 1350
    els = []; h = []
    # mural: CRFTD, giant, reversed (it is the object the hero covers), bleeding off all four edges
    fs = 420
    m = measure([dict(text="CRFTD", font="d", size=fs, weight=900)])[0]["text_w"]
    rows = [(-70, 170), (-250, 508), (-20, 846)]
    for i, (dx, y) in enumerate(rows):
        h.append(f'<div style="position:absolute;left:{dx}px;top:{y}px;white-space:nowrap;font-family:var(--d);font-weight:900;font-size:{fs}px;'
                 f'line-height:{fs*.8:.0f}px;color:{TOM};letter-spacing:-.01em;z-index:1;text-transform:uppercase">CRFTD</div>')
    # a cream cap so the header reads clean on the first 150px
    h.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:172px;background:{CREAM};z-index:2"></div>')
    h.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:172px;z-index:2;border-bottom:5px solid {INK}"></div>')
    # hero
    hero = halftone_tee()
    hw = 640; hh = round(hw * hero.height / hero.width)
    hx = (W - hw) // 2 - 6; hy = 150
    h.append(K.img(K.uri(hero, "PNG"), hx, hy, hw, hh, z=6))
    els.append(("hero", hx, hy, hw, hh))
    # bolts around it, lemon with ink outline via stamp style
    for k, (bx, by, bs, rot) in enumerate([(70, 300, 190, -20), (850, 230, 170, 25), (800, 640, 140, -10), (95, 640, 130, 15)]):
        h.append(dood("lightning", bx, by, bs, LEM, rot, z=8)); els.append((f"bolt{k}", bx, by, bs, bs))
    # torn ribbon, headline INSIDE the rotated wrapper so ribbon and type turn together
    rw, rh = 980, 236
    line = lambda txt, y: (f'<div class="measure" data-tag="rib" style="position:absolute;left:70px;width:{rw-140}px;top:{y}px;text-align:center;white-space:nowrap;'
                           f'font-family:var(--d);font-weight:900;font-size:64px;line-height:70px;color:{INK};text-transform:uppercase">{txt}</div>')
    h.append(f'<div style="position:absolute;left:{(W-rw)//2-12}px;top:872px;width:{rw}px;height:{rh}px;z-index:12;transform:rotate(-2.2deg)">'
             f'{torn_ribbon(rw, rh)}{line("EVERY RUPEE OF PROFIT", 46)}{line("FUNDS A WELFARE DRIVE", 122)}</div>')
    els.append(("ribbon", 40, 860, rw, rh + 40))
    h.append(K.t("crftd (formerly roots) school-fest stalls. novus alone logged 300 walk-ins.", 64, 1134, 17, color=INK, font="m", weight=700,
                 z=14, tag="note", extra=f"background:{CREAM};padding:6px 10px;border:3px solid {INK};"))
    els.append(("note", 64, 1130, 700, 40))
    h.append(chrome("crftd")); h.append(K.url_pill())
    els += [("logo", 64, 48, 200, 40), ("tab", 760, 58, 256, 40), ("lane", 64, 116, 100, 38), ("url", 64, 1188, 952, 84)]
    html = K.page("".join(h))
    tp = [("ribbon head", INK, PAPER, 64, True), ("note", INK, CREAM, 17, True)]
    return K.render(nm("crftd_1", it), html, H, elements=els, text_pairs=tp, containers=("ribbon",), bleed_tags=("t",),
                    collision_ignore=[("hero", "bolt0"), ("hero", "bolt1"), ("hero", "bolt2"), ("hero", "bolt3"), ("hero", "ribbon"),
                                  ("hero", "note")])


# --------------------------------------------------------------------------- crftd_2
SHAPE_WH = {"capsule": (100, 40), "tag": (100, 44), "wave_banner": (100, 44)}   # silhouettes that are NOT square inside their square svg
PAD = 26 / 152.0                                                               # halo margin as a fraction of the svg size


def badge(kind, fill, S, lines, cx, cy, rot=0, label_id="b", z=14, boost=1.2):
    """A die-cut sticker positioned by its VISIBLE centre (cx, cy), label fitted to the silhouette (shapes.fit_font).
    shapes.sticker draws a SQUARE svg with the shape in the top-left of it for wide silhouettes, so a plain x,y would misplace it."""
    sw_, sh_ = SHAPE_WH.get(kind, (100, 100))
    path = shapes.SILHOUETTES[kind]()
    ms = measure([dict(text=l, font="d", size=40, weight=800) for l in lines])
    longest = max(range(len(lines)), key=lambda i: ms[i]["text_w"])
    bx, fits = shapes.fit_font(ms[longest]["text_w"], 40, kind, S * boost)
    n = len(lines); step = bx * 1.1; mid = sh_ / 2
    inner = "".join(shapes.label(l, size=bx, y=mid + (i - (n - 1) / 2) * step + bx * .34, fill=core.text_on(fill)) for i, l in enumerate(lines))
    svg = shapes.sticker(path, fill, size=S, rot=rot, inner=inner, detail="none")
    x = cx - S * (PAD + .658 * sw_ / 200); y = cy - S * (PAD + .658 * sh_ / 200)
    vw, vh = .658 * S * sw_ / 100, .658 * S * sh_ / 100
    box = (label_id, int(cx - vw / 2), int(cy - vh / 2), int(vw), int(vh))
    return (f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{S}px;height:{S}px;z-index:{z}">{svg}</div>'), box, fits


def crftd_2(it=1):
    H = 1350
    h = [f'<div style="position:absolute;inset:0;background:{INK}"></div>']
    els = []
    m = measure([dict(text="300", font="d", size=100, weight=900), dict(text="WALK-INS.", font="d", size=100, weight=900)])
    fs1 = int(936 / (m[0]["text_w"] / 100)); fs2 = int(840 / (m[1]["text_w"] / 100))
    y1 = 196; y2 = y1 + int(fs1 * .80) - 6
    for txt, fs, y, tag, mi in (("300", fs1, y1, "h1", 0), ("WALK-INS.", fs2, y2, "h2", 1)):
        w_ = m[mi]["text_w"] / 100 * fs
        h.append(K.t(txt, int((W - w_) / 2), y, fs, color=CREAM, font="d", weight=900, lh=int(fs * .8), z=5, tag=tag, upper=True))
        els.append((tag, int((W - w_) / 2), y + int(fs * .08), int(w_), int(fs * .66)))
    print("fs", fs1, fs2, "y", y1, y2)
    specs = [   # kind, fill, S, label lines, visible centre x, y, rot, id
        ("scallop", LEM, 330, ["NOVUS", "300"], 150, 300, -8, "novus"),
        ("starburst", PINK, 340, ["RUN BY", "STUDENTS"], 925, 285, 9, "students"),
        ("gear", TOM, 330, ["CONFLUENCE", "300 & 250"], 70, 660, -6, "confl"),
        ("tag", SKY, 340, ["CONCORD", "200 & 250"], 945, 735, 6, "concord"),
        ("blob", MINT, 330, ["CRFTD", "EX-ROOTS"], 215, 810, 6, "blob"),
        ("shield", GRAPE, 330, ["MORPHEUS", "300 & 350"], 480, 800, -5, "morph"),
        ("arch", LEM, 330, ["SCHOOL", "FEST STALLS"], 750, 825, 5, "fests"),
        ("capsule", PAPER, 660, ["EVERY RUPEE OF PROFIT", "FUNDS A WELFARE DRIVE"], 520, 1008, -2, "profit"),
        ("scallop", SKY, 300, ["ZERO", "DONATIONS"], 960, 950, 8, "zero"),
    ]
    for k, f, sz, ls, cx, cy, rot, lid in specs:
        b, e, fits = badge(k, f, sz, ls, cx, cy, rot, lid, z=12 if k == 'capsule' else 14, boost=1.35 if k == 'capsule' else 1.2)
        h.append(b); els.append(e)
        if not fits: print("LABEL DOES NOT FIT", lid)
    names = [e[0] for e in els]
    ign = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    h.append(K.t("walk-in counts as logged for crftd school-fest stalls (platform). the profit line is from the site.",
                 64, 1162, 15, color=CREAM, font="m", weight=700, z=14, tag="note", w=952, lh=22))
    els.append(("note", 64, 1162, 800, 22))
    h.append(chrome("crftd", dark=True)); h.append(K.url_pill(bg=LEM, fg=INK))
    els += [("logo", 64, 48, 200, 40), ("tab", 760, 58, 256, 40), ("lane", 64, 116, 100, 38), ("url", 64, 1188, 952, 84)]
    html = K.page("".join(h), bg=INK)
    tp = [("h1", CREAM, INK, 400, True), ("h2", CREAM, INK, 200, True), ("note", CREAM, INK, 15, True)]
    return K.render(nm("crftd_2", it), html, H, elements=els, text_pairs=tp, collision_ignore=ign)


# --------------------------------------------------------------------------- shikshaq_1
def bubble_svg(w, h, bg, pattern, uid, tail=True):
    """A speech-bubble rectangle filled edge to edge with a two-colour pattern, ink outline, hard shadow, tail bottom-left."""
    r = 26
    path = f"M{r},0 H{w-r} Q{w},0 {w},{r} V{h-r} Q{w},{h} {w-r},{h} H{70} L{40},{h+44} L{44},{h} H{r} Q0,{h} 0,{h-r} V{r} Q0,0 {r},0 Z"
    rnd = random.Random(uid)
    pat = ""
    if pattern == "stripes":                      # diagonal bands in the second colour
        for i in range(-6, 14):
            pat += f'<path d="M{i*58},{h+10} L{i*58+h+10},0" stroke="{pattern_col[uid]}" stroke-width="22"/>'
    elif pattern == "curves":                     # intersecting curves
        for k in range(5):
            y0 = rnd.uniform(0, h); y1 = rnd.uniform(0, h)
            pat += (f'<path d="M-10,{y0:.0f} C{w*.3:.0f},{rnd.uniform(-40,h+40):.0f} {w*.6:.0f},{rnd.uniform(-40,h+40):.0f} {w+10},{y1:.0f}" '
                    f'stroke="{pattern_col[uid]}" stroke-width="9" fill="none" stroke-linecap="round"/>')
        for k in range(3):
            x0 = rnd.uniform(.1, .9) * w
            pat += (f'<path d="M{x0:.0f},-10 C{x0+rnd.uniform(-90,90):.0f},{h*.35:.0f} {x0+rnd.uniform(-90,90):.0f},{h*.7:.0f} {x0+rnd.uniform(-50,50):.0f},{h+10}" '
                    f'stroke="{pattern_col[uid]}" stroke-width="9" fill="none" stroke-linecap="round"/>')
    else:                                         # rough brush strokes
        for k in range(7):
            x0 = k * w / 6.0 - 40
            pts = []
            for t_ in range(0, 9):
                pts.append((x0 + t_ * 16 + rnd.uniform(-6, 6), h + 20 - t_ * (h + 40) / 8.0 + rnd.uniform(-4, 4)))
            left = " L".join(f"{x:.0f},{y:.0f}" for x, y in pts)
            right = " L".join(f"{x+26+rnd.uniform(-8,8):.0f},{y+rnd.uniform(-5,5):.0f}" for x, y in pts[::-1])
            pat += f'<path d="M{left} L{right} Z" fill="{pattern_col[uid]}"/>'
    return (f'<svg width="{w+16}" height="{h+60}" viewBox="-4 -4 {w+16} {h+60}" style="overflow:visible">'
            f'<defs><clipPath id="bc{uid}"><path d="{path}"/></clipPath></defs>'
            f'<path d="{path}" transform="translate(8,9)" fill="{INK}"/>'
            f'<g clip-path="url(#bc{uid})"><rect x="-5" y="-5" width="{w+10}" height="{h+60}" fill="{bg}"/>{pat}</g>'
            f'<path d="{path}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></svg>')


pattern_col = {1: SKY, 2: PINK, 3: LEM}


def cloud(x, y, w, z=3):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:{z}" width="{w}" height="{w*.4:.0f}" viewBox="0 0 100 40">'
            f'<path d="M4,36 Q0,28 10,25 Q10,12 24,14 Q30,2 44,8 Q56,0 64,12 Q80,8 84,22 Q100,24 96,36 Z" fill="{INK}"/></svg>')


def shikshaq_1(it=1):
    H = 1350
    h = []; els = []
    # headline
    lines = ["ASKING AROUND IS NOT", "A SEARCH ENGINE."]
    m = measure([dict(text=l, font="d", size=100, weight=900) for l in lines])
    fs = int(952 / (max(x["text_w"] for x in m) / 100))
    for i, l in enumerate(lines):
        h.append(K.t(l, 64, 176 + i * int(fs * .94), fs, color=INK, font="d", weight=900, lh=int(fs * .94), z=6, tag=f"h{i}", upper=True))
        els.append((f"h{i}", 64, 176 + i * int(fs * .94) + 6, int(m[i]["text_w"] / 100 * fs), int(fs * .8)))
    yb = 176 + 2 * int(fs * .94) + 14
    h.append(K.t("tutor search took 11 days. after shikshaq launched, under 48 hours.", 64, yb, 29, color=INK, font="e", weight=500, w=952, lh=36, z=6, tag="sub"))
    els.append(("sub", 64, yb, 952, 38))
    # signpost
    PX = 290; top = 412
    h.append(f'<div style="position:absolute;left:{PX-14}px;top:{top+18}px;width:28px;height:{1068-top-18}px;background:{INK};z-index:2"></div>')
    h.append(f'<div style="position:absolute;left:{PX-22}px;top:{top}px;width:44px;height:44px;border-radius:50%;background:{INK};z-index:2"></div>')
    h.append(f'<div style="position:absolute;left:{PX-120}px;top:1052px;width:240px;height:34px;border-radius:50%;background:{INK};z-index:1"></div>')
    h.append(cloud(80, 408, 130)); h.append(cloud(405, 398, 120))
    els += [("pole", PX - 14, top, 28, 640), ("base", PX - 120, 1052, 240, 34), ("cloud1", 80, 408, 130, 52), ("cloud2", 405, 398, 120, 48)]
    signs = [("KOLKATA", LEM, "leaf", -2.5), ("ZERO COMMISSION", SKY, "cross", 2), ("FREE TO USE", TOM, "heart", -1.5),
             ("DIRECT CONTACT", MINT, "speech", 2.5), ("RUN BY STUDENTS", GRAPE, "star", -2)]
    ms = measure([dict(text=t_, font="d", size=34, weight=900) for t_, *_ in signs])
    for i, ((txt, col, ic, rot), mm) in enumerate(zip(signs, ms)):
        wpx = int(mm["text_w"] + 120); y = top + 58 + i * 114
        wpx = min(wpx, 520)
        sx = max(64, min(PX - wpx // 2 + (-20 if i % 2 == 0 else 14), 546 - wpx))
        tc = core.text_on(col)
        h.append(f'<div style="position:absolute;left:{sx}px;top:{y}px;width:{wpx}px;height:90px;border-radius:24px;background:{col};border:4px solid {INK};'
                 f'box-shadow:6px 7px 0 {INK};transform:rotate({rot}deg);z-index:8"></div>')
        h.append(f'<div style="position:absolute;left:{sx+16}px;top:{y+19}px;width:50px;height:50px;z-index:9;transform:rotate({rot}deg)">{dd.stamp(ic, tc, rot=0)}</div>')
        h.append(K.t(txt, sx + 76, y + 25, 34, color=tc, font="d", weight=900, lh=40, z=9, tag=f"sign{i}", upper=True,
                     extra=f"transform:rotate({rot}deg);transform-origin:{-60}px 20px;"))
        els.append((f"sign{i}", sx, y, wpx, 90))
    # bubbles
    bub = [(456, 172, GRAPE, "stripes", 1, ["11 DAYS", "asking around for a tutor"], 436),
           (420, 160, MINT, "curves", 2, ["UNDER 48 HOURS", "on shikshaq, after launch"], 676),
           (372, 150, TOM, "brush", 3, ["50+ VERIFIED", "profiles at launch"], 896)]
    for bw, bh, bg, pat, uid, (big, small), by in bub:
        bx = 560
        h.append(f'<div style="position:absolute;left:{bx}px;top:{by}px;z-index:4">{bubble_svg(bw, bh, bg, pat, uid)}</div>')
        mmx = measure([dict(text=big, font="d", size=36, weight=900), dict(text=small, font="m", size=15, weight=700)])
        pw = int(max(mmx[0]["text_w"], mmx[1]["text_w"]) + 40); ph = 88
        px = bx + (bw - pw) // 2; py = by + (bh - ph) // 2
        h.append(f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;background:{CREAM};border:4px solid {INK};border-radius:16px;z-index:9;box-shadow:5px 5px 0 {INK}"></div>')
        h.append(K.t(big, px + 20, py + 10, 36, color=INK, font="d", weight=900, lh=42, z=10, tag=f"bb{uid}", upper=True))
        h.append(K.t(small, px + 20, py + 56, 14, color=INK, font="m", weight=700, z=10, tag=f"bs{uid}"))
        els += [(f"bub{uid}", bx, by, bw, bh + 40), (f"plate{uid}", px, py, pw, ph)]
    h.append(K.t("shikshaq launch research, scoped. made by aquaterra, an ngo whose team are students.", 64, 1148, 14, color="var(--ink3)", font="m", weight=700, z=6, tag="note"))
    els.append(("note", 64, 1148, 800, 20))
    h.append(chrome("shikshaq")); h.append(K.url_pill())
    els += [("logo", 64, 48, 200, 40), ("tab", 760, 58, 256, 40), ("lane", 64, 116, 120, 38), ("url", 64, 1188, 952, 84)]
    names = [e[0] for e in els]
    ign = [(a, b) for a in names for b in names if a < b and (a.startswith(("bub", "plate", "sign", "pole", "cloud", "base")) and b.startswith(("bub", "plate", "sign", "pole", "cloud", "base")))]
    html = K.page("".join(h))
    tp = [("h0", INK, CREAM, fs, True), ("sub", INK, CREAM, 29, False), ("note", core.INK3 if hasattr(core, "INK3") else INK, CREAM, 14, True)]
    return K.render(nm("shikshaq_1", it), html, H, elements=els, text_pairs=tp, collision_ignore=ign)


if __name__ == "__main__":
    which = sys.argv[1]; it = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    globals()[which](it)
