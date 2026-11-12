"""AQ recruitment push, v2: CLOSE recreations of the user's five Pinterest references, built with real AQ photos.
(v1 softened the references into AQ-safe boxes and was rejected as boring; this follows the references.)

  r1_cast      ref 1  B&W photo + colour windows with track-name tabs + serif title lockup   (T3 FOMO)
  r2_blank     ref 2  fill-in-the-blank sentence with photo-crop thumbnails + cut-out photo   (T1 capability)
  r3_late      ref 3  posterised landscape + frosted card + highlight chip + stick figures   (T5 general)
  r4_haggling  ref 4  full-bleed photo, white headline, glass pills, glass dock/cards         (T4 learning)
  r5_site      ref 5  website-page layout, dithered photo strip, four colour blocks           (T2 recruit)

ADAPTATIONS, recorded per the precedence ladder (CLAUDE.md section 2):
  * USER DIRECTIVE overrides the usual 'one serif accent word' rule on r1 and r5, where the reference IS the serif
    headline. Everything else stays NeutralFace/Eina.
  * Fake assets swapped for real ones: no fake profile / case-study UI (r4), a real AQ fact card instead.
  * Pale ground is AQ cream, not the references' white/grey.
  * Posterise (r3) and dither (r5) are done offline in PIL on REAL AQ photos; nothing is stock.
  * White type on photo (r2? no, r3/r4) is sitting on scrimmed or posterised darks; contrast measured below.
"""
import asyncio, os, sys, importlib.util, io, base64
import numpy as np
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); shapes = load("shapes")
from PIL import Image, ImageOps, ImageFilter

W, H = 1080, 1350
INK = core.INK; CREAM = core.CREAM; A = core.ACCENTS
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = A
IMG = "engine/assets/img/"
URL = "ngoaquaterra.com/recruitment"
OUT = "out/recruit_nov2026/v2"
S = 1.5   # supersample the baked rasters

P_DESK = "events/summer-aq-turns-five/01_registration-desk.jpg"
P_FLOOR = "events/unsorted-2026-10-07/11_dance-green-light-portrait.jpg"
P_COURT = "events/summer-aq-turns-five/04_courtyard-crowd-garlands.jpg"
P_BLUE = "events/unsorted-2026-10-07/07_dance-blur-blue-light.jpg"
P_STALL = "events/welfare-feed-2026/01_sharbat-stall-volunteers.webp"   # local-only (teen volunteers); unused in the final set
P_JAR = "events/welfare-feed-2026/02_sharbat-jar-bottles.webp"
P_BOARD = "events/welfare-feed-2026/03_disha-volunteer-blackboard.webp"
P_DOG = "events/welfare-feed-2026/04_dog-biscuits-pat.webp"
P_STREET = "events/welfare-feed-2026/07_street-tree-dog.webp"
P_FACES = "events/disco-diwali-hall-2026-10-14/05_boys-crowd-green-light.jpg"
P_GROUP = "events/unsorted-2026-10-07/01_IMG_7180_group-aquaterra-banner.jpg"

# ------------------------------------------------------------------ raster prep (PIL)
def cover(rel, w, h, fx=.5, fy=.5, zoom=1.0, s=S):
    im = Image.open(IMG + rel).convert("RGB")
    tw, th = round(w * s), round(h * s)
    k = max(tw / im.width, th / im.height) * zoom
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x = round((im.width - tw) * fx); y = round((im.height - th) * fy)
    return im.crop((x, y, x + tw, y + th))

def uri(im, fmt="JPEG", q=88):
    b = io.BytesIO(); im.save(b, fmt, quality=q) if fmt == "JPEG" else im.save(b, fmt)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(b.getvalue()).decode()

def mono(im, contrast=1.0, cut=1):
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=cut)
    if contrast != 1.0:
        a = np.asarray(g, dtype=np.float32) / 255.0
        a = np.clip((a - .5) * contrast + .5, 0, 1)
        g = Image.fromarray((a * 255).astype("uint8"))
    return g.convert("RGB")

def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def posterise(im, palette, blur=7):
    """Gradient-map a photo into flat patches, the vector-landscape look of the 'You are not alone' reference."""
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2).filter(ImageFilter.MedianFilter(blur * 2 + 1)).filter(ImageFilter.GaussianBlur(2))
    a = np.asarray(g)
    idx = np.minimum((a.astype(np.int32) * len(palette)) // 256, len(palette) - 1)
    pal = np.array([hexrgb(c) for c in palette], dtype=np.uint8)
    return Image.fromarray(pal[idx])

def dither(im, light, dark=INK, cell=5):
    w, h = im.size
    g = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=2)
    g = g.resize((max(1, w // cell), max(1, h // cell)), Image.LANCZOS).convert("1")   # Floyd-Steinberg
    g = g.resize((w, h), Image.NEAREST).convert("L")
    a = np.asarray(g) > 127
    out = np.zeros((h, w, 3), dtype=np.uint8)
    out[a] = hexrgb(light); out[~a] = hexrgb(dark)
    return Image.fromarray(out)

# ------------------------------------------------------------------ html helpers
def box(x, y, w, h, style, inner="", z=3, extra="", cls=""):
    return (f'<div class="{cls}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{style}z-index:{z};{extra}">{inner}</div>')

def t(s, x, y, size, color=INK, font="e", weight=400, lh=None, w=None, z=8, extra="", italic=False, ls=0, tag="t", upper=False):
    wc = f"width:{w}px;" if w else "white-space:nowrap;"
    return (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;{wc}font-family:var(--{font});'
            f'font-weight:{weight};font-size:{size}px;line-height:{lh or round(size*1.2)}px;color:{color};letter-spacing:{ls}em;'
            f'{"font-style:italic;" if italic else ""}{"text-transform:uppercase;" if upper else ""}z-index:{z};{extra}">{s}</div>')

def img(uri_, x, y, w, h, z=1, extra=""):
    return f'<img src="{uri_}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};{extra}">'

def stick(kind, color, size, x, y, z=9):
    """Hand-drawn stick figure, as in the reference."""
    poses = {
        "run":  "M30 36 L30 82 M30 48 L10 64 M30 48 L54 40 M30 82 L14 112 M30 82 L56 104",
        "jump": "M30 36 L30 82 M30 46 L8 24 M30 46 L52 24 M30 82 L12 108 M30 82 L50 108",
        "wave": "M30 36 L30 82 M30 48 L8 58 M30 48 L54 22 M30 82 L18 112 M30 82 L44 112"}
    face = ""
    if kind == "jump":
        face = f'<circle cx="30" cy="20" r="15" fill="{color}" stroke="#0A0A0A" stroke-width="2.5"/><circle cx="25" cy="17" r="2" fill="#0A0A0A"/><circle cx="35" cy="17" r="2" fill="#0A0A0A"/><path d="M23 24 Q30 31 37 24" stroke="#0A0A0A" stroke-width="2.5" fill="none"/>'
    else:
        face = f'<circle cx="30" cy="20" r="15" fill="none" stroke="{color}" stroke-width="5"/><circle cx="25" cy="18" r="2" fill="{color}"/><circle cx="35" cy="18" r="2" fill="{color}"/><path d="M24 25 Q30 31 36 25" stroke="{color}" stroke-width="2.5" fill="none"/>'
    sc = "#FFC700" if kind == "jump" else color
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;z-index:{z}" width="{size}" height="{round(size*2)}" viewBox="0 0 60 120">'
            f'<path d="{poses[kind]}" stroke="{sc}" stroke-width="5" stroke-linecap="round" fill="none"/>{face}</svg>')

async def mw(items): return [m["text_w"] for m in await B.measure_text(items)]

def logo_pill(x=64, y=48, dark=False):
    if dark:
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;padding:10px 18px;background:{CREAM};border:3px solid #0A0A0A;'
                f'border-radius:999px;z-index:30;box-shadow:4px 4px 0 #0A0A0A"><img src="{core.LOGO}" style="height:28px;display:block"></div>')
    return B.logo(dark=False, x=x, y=y)

def page(inner, bg=CREAM): return B.page(W, H, bg, inner, grain=False)

# ================================================================= R1  the cast list (reference 1)
def r1():
    ph = cover(P_DESK, W, H, fy=.35)
    m = mono(ph, contrast=1.08)
    P = [img(uri(m), 0, 0, W, H, z=1)]
    # sky fade so the black title and paragraph read, as the reference's pale cloud does
    P.append(box(0, 0, W, 520, "background:linear-gradient(180deg,rgba(236,236,232,.96) 0%,rgba(236,236,232,.9) 52%,rgba(236,236,232,0) 100%);", z=2))
    # colour windows (multiply, so the photo shows through) + flush track tabs, as in the reference
    wins = [  # x, y, w, h, colour, tab text, tab side
        (70, 560, 250, 210, "#7E5BFF", "INTRO : we're students, apparently", "tr"),
        (400, 470, 230, 250, "#3DA9FC", "TRACK 02 : the last price (it was not)", "br"),
        (720, 440, 290, 300, "#FFC700", "SKIT : whose laptop is this", "tl"),
        (38, 940, 210, 250, "#FF4D2E", "THIS SEAT : yours", "tr"),
        (700, 860, 270, 330, "#FF4D8C", "OUTRO : someone find the wristbands", "bl"),
        (360, 980, 260, 220, "#1B8A5A", "TRACK 05 : who has the walkie-talkie", "tr"),
    ]
    for (x, y, w, h, c, label, side) in wins:
        P.append(box(x, y, w, h, f"background:{c};mix-blend-mode:multiply;opacity:.92;", z=6))
        lw = int(len(label) * 8.1 + 22); th = 26
        tx = x + w - lw if side in ("tr", "br") else x
        ty = y - th if side in ("tr", "tl") else y + h
        P.append(f'<div style="position:absolute;left:{tx}px;top:{ty}px;height:{th}px;padding:0 10px;background:{c};z-index:9;'
                 f'font-family:var(--e);font-weight:600;font-size:14.5px;line-height:{th}px;color:#0A0A0A;white-space:nowrap">{label}</div>')
    # paragraph, top left (reference: small justified block)
    P.append(t("Registration desk. four laptops, two walkie-talkies and a wristband situation. nobody in this photo has a boss, and the line still moved. applications are open at " + URL + ".",
               64, 120, 17, color="#0A0A0A", w=340, lh=27, tag="para"))
    # title lockup, top right, mixed sizes like the reference's hand-set serif
    X = 470
    P.append(t("&ldquo;", X - 8, 52, 120, font="s", color=INK, lh=110, tag="q"))
    P.append(t("Everyone", X + 70, 72, 74, font="s", lh=80, tag="a1"))
    P.append(t("in this photo", X + 40, 148, 92, font="s", lh=96, tag="a2"))
    P.append(t("is a", X + 10, 242, 70, font="s", lh=74, tag="a3"))
    P.append(t("student.", X + 100, 232, 150, font="s", italic=True, lh=150, tag="a4", z=9))
    P.append(t("by @ngo.aquaterra", X + 20, 376, 20, font="e", weight=600, tag="by"))
    P.append(logo_pill(64, 48))
    return "r1_cast", page("".join(P)), [("para", 64, 120, 340, 190), ("a4", X + 100, 232, 380, 150)]

# ================================================================= R2  fill-in-the-blank (reference 2)
def r2():
    PH_Y = 560; PH_H = H - PH_Y
    base = cover(P_FLOOR, W, PH_H, fy=.27, s=S)       # baked, so thumbnails are exact crops
    boxes = [(10, 60, 205, 190), (370, 170, 160, 240), (565, 6, 115, 190), (140, 585, 190, 190), (680, 560, 190, 215)]
    # the photo with the cut-out boxes punched out in the page grey, as the reference does
    punched = base.copy()
    from PIL import ImageDraw
    d = ImageDraw.Draw(punched)
    for (x, y, w, h) in boxes:
        d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=hexrgb(CREAM))
    P = [img(uri(punched), 0, PH_Y, W, PH_H, z=2)]
    def thumb(i, th=66):
        x, y, w, h = boxes[i]
        crop = base.crop((round(x * S), round(y * S), round((x + w) * S), round((y + h) * S)))
        tw = round(th * w / h)
        return (f'<img src="{uri(crop)}" style="display:inline-block;vertical-align:middle;height:{th}px;width:{tw}px;object-fit:cover;'
                f'margin:0 6px;border-radius:5px;border:2px solid #0A0A0A">'), tw
    th_ = [thumb(i)[0] for i in range(len(boxes))]
    body = (f'Some students built a ( {th_[0]} ) hall, hung ( {th_[1]} ) lights, lost an argument with a vendor over '
            f'( {th_[2]} ) balloons, and then danced on the result. ( {th_[3]} )<br>'
            f'Applications are open. Bring opinions about balloons. ( {th_[4]} )')
    P.append(f'<div style="position:absolute;left:56px;top:150px;width:968px;text-align:center;font-family:var(--e);font-weight:400;'
             f'font-size:31px;line-height:84px;color:#0A0A0A;z-index:8">{body}</div>')
    P.append(logo_pill(64, 46))
    return "r2_blank", page("".join(P)), []

# ================================================================= R3  posterised landscape + frosted card (reference 3)
def r3(story=False):
    TB, ys = (330, 230) if story else (150, 0)
    pal = ["#0d2413", "#17391c", "#245a24", "#3f7a2a", "#7a9a35", "#b9b04a", "#e6dca0"]
    bg = posterise(cover(P_STREET, W, H - TB, fy=.45, zoom=1.0), pal, blur=5)
    dog = posterise(cover(P_DOG, 480, 360, fy=.5), ["#0d2413","#143018","#1d4524","#276028","#3a7a2c","#5b8f31","#86a038","#b0ab45","#d3c673","#ece3ad"], blur=1)
    P = [img(uri(bg, "PNG"), 0, TB, W, H - TB, z=1)]
    # pale top band + italic caption
    P.append(box(0, 0, W, TB, f"background:{CREAM};", z=2))
    P.append(t("Doing nothing over winter break is more common than you think.", 0, 66 + (196 if story else 0), 31, font="s", italic=True, w=W, lh=40, extra="text-align:center;", tag="cap"))
    P.append(logo_pill(64, 24 + (182 if story else 0)))
    # frosted card
    cx, cy, cw, ch = 64, 330 + ys, 560, 700
    P.append(box(cx, cy, cw, ch, "background:rgba(244,239,224,.62);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border:3px solid rgba(255,255,255,.8);", z=4))
    P.append(img(uri(dog, "PNG"), cx + 26, cy + 58, cw - 52, 410, z=5, extra="border:3px solid #fff;object-fit:cover;"))
    P.append(t("You are not", cx + 28, cy + 505, 34, color="#0A0A0A", font="e", weight=400, tag="n1"))
    P.append(f'<div style="position:absolute;left:{cx+28}px;top:{cy+550}px;padding:4px 18px 8px;background:{SKY};z-index:6;'
             f'font-family:var(--e);font-weight:600;font-size:70px;line-height:80px;color:#0A0A0A">late.</div>')
    P.append(box(560, TB, 520, H - TB, 'background:linear-gradient(90deg,rgba(6,22,10,0),rgba(6,22,10,.5) 35%,rgba(6,22,10,.55));', z=3))
    P.append(box(0, H - (340 if story else 170), W, 340 if story else 170, 'background:linear-gradient(180deg,rgba(6,22,10,0),rgba(6,22,10,.72));', z=3))
    # right column
    rx, rw = 656, 360
    P.append(t("Nobody started anything on 1st January at 9am sharp. Most good ideas begin on a random Tuesday, right after someone says what if we just did it.",
               rx, 360 + ys, 25, font="s", italic=True, color="#fff", w=rw, lh=34, extra="text-align:right;", tag="p1"))
    P.append(f'<div style="position:absolute;left:{1016-292}px;top:{640+ys}px;padding:5px 12px;background:{SKY};z-index:8;font-family:var(--m);font-weight:700;'
             f'font-size:15px;color:#0A0A0A">{URL}</div>')
    P.append(stick("run", "#fff", 96, 690, 700 + ys)); P.append(stick("jump", "#fff", 96, 800, 692 + ys)); P.append(stick("wave", "#fff", 96, 905, 700 + ys))
    P.append(t("We are students who feed dogs, throw fests and lose arguments to vendors. Come be late with us.",
               rx, 960 + ys, 25, font="s", italic=True, color="#fff", w=rw, lh=34, extra="text-align:right;", tag="p2"))
    P.append(t("Applications are open. Nobody is checking your timing.", 0, 1500 if story else 1262, 28, font="s", italic=True, color="#fff", w=W, lh=36, extra="text-align:center;", tag="cap2"))
    return "r3_late" + ("_story" if story else ""), page("".join(P)), [("p1", rx, 360 + ys, rw, 210), ("p2", rx, 960 + ys, rw, 150)]

# ================================================================= R4  CREATIE-style hero (reference 4)
async def r4(story=False):
    ts, ms, bs = (170, (H - 1350) // 2, H - 1350 - 258) if story else (0, 0, 0)
    ph = cover(P_BLUE, W, H, fx=.45, fy=.5)
    P = [img(uri(ph), 0, 0, W, H, z=1)]
    P.append(box(0, 0, W, H, "background:linear-gradient(180deg,rgba(6,12,40,.35),rgba(6,12,40,.18) 45%,rgba(6,12,40,.55));", z=2))
    lines = ["SCHOOL TEACHES", "ALGEBRA. WE", "TEACH HAGGLING."]
    ws = await mw([dict(text=s_, font="d", size=sz, weight=900) for s_ in lines for sz in (150,)])
    size = int(150 * min(1.0, 940 / max(ws)))
    step = round(size * .95)
    y0 = 470 + ms
    for i, s_ in enumerate(lines):
        P.append(t(s_, 0, y0 + i * step, size, color="#fff", font="d", weight=900, w=W, lh=step, extra="text-align:center;", tag=f"h{i}", upper=True))
    def glass(x, y, w, h, inner="", r=24, a=.34):
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;background:rgba(255,255,255,{a});'
                f'backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:2px solid rgba(255,255,255,.55);z-index:12;'
                f'box-shadow:0 8px 30px rgba(0,0,0,.18)">{inner}</div>')
    def pill(x, y, label, col, rot=0, icon="sparkle"):
        wpx = int(len(label) * 16 + 98)
        ic = (f'<div style="position:absolute;left:10px;top:10px;width:44px;height:44px;border-radius:50%;background:{col};z-index:2;'
              f'display:flex;align-items:center;justify-content:center"><div style="position:relative;width:26px;height:26px">{dd.stamp(icon, "#fff")}</div></div>')
        return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{wpx}px;height:64px;border-radius:18px;background:rgba(255,255,255,.8);'
                f'border:2px solid rgba(255,255,255,.9);z-index:14;transform:rotate({rot}deg);box-shadow:0 6px 18px rgba(0,0,0,.25);'
                f'font-family:var(--e);font-weight:600;font-size:25px;line-height:64px;color:#0A0A0A;padding-left:66px">{ic}{label}</div>')
    P.append(pill(760, y0 - 70, "Vendors", SKY, rot=-4, icon="sparkle"))
    P.append(pill(850, y0 + step * 1 + 6, "Sponsors", PINK, rot=3, icon="heart"))
    P.append(pill(110, y0 + step * 2 + 78, "Budgets", GRAPE, rot=-3, icon="star"))
    # top-left fact card (the reference's profile card, with a real AQ fact instead of a fake person)
    card = (f'<div style="position:absolute;left:22px;top:20px;width:12px;height:12px;border-radius:50%;background:#2ecc71"></div>'
            f'<div style="position:absolute;left:44px;top:12px;font-family:var(--e);font-size:17px;color:#0A0A0A">Applications open</div>'
            f'<div style="position:absolute;left:22px;top:42px;font-family:var(--e);font-weight:600;font-size:23px;color:#0A0A0A">AQUATERRA, KOLKATA</div>'
            f'<div style="position:absolute;left:22px;top:78px;width:330px;font-family:var(--e);font-size:17px;line-height:24px;color:#222">student-run since 2021. events, welfare, startups, a magazine.</div>')
    P.append(glass(64, 150 + ts, 380, 140, card, r=26, a=.5))
    P.append(logo_pill(425, 44 + ts, dark=True))
    # squiggles, as in the reference
    P.append(f'<div style="position:absolute;left:880px;top:{210+ts}px;width:120px;height:120px;z-index:10">{dd.stamp("spiral", "#FFC700", rot=20)}</div>')
    P.append(f'<div style="position:absolute;left:910px;top:{330+ts}px;width:110px;height:60px;z-index:10">{dd.stamp("zigzag", "#3DA9FC")}</div>')
    P.append(f'<div style="position:absolute;left:150px;top:{960+ms}px;width:74px;height:74px;z-index:10">{dd.stamp("zigzag", "#FF4D8C", rot=-20)}</div>')
    # caption bottom-left
    P.append(t("&mdash; no donations. we throw parties and sell clothes, and that pays for everything.",
               64, 1160 + bs, 24, color="#fff", font="e", weight=600, w=290, lh=33, tag="capt"))
    # dock (the reference's app dock) in department colours
    dock_icons = "".join(
        f'<div style="width:66px;height:66px;border-radius:18px;background:{c};display:flex;align-items:center;justify-content:center;border:2px solid rgba(255,255,255,.7)">'
        f'<div style="position:relative;width:40px;height:40px">{dd.stamp(k, "#0A0A0A")}</div></div>' for c, k in [(LEM, "star"), (SKY, "burst"), (MINT, "leaf"), (PINK, "speech")])
    P.append(glass(372, 1176 + bs, 328, 98, f'<div style="display:flex;gap:12px;padding:14px 16px">{dock_icons}</div>', r=28, a=.3))
    # stacked card, bottom right (the reference's case-study card)
    for k in (2, 1):
        P.append(glass(730 + k * 10, 1176 + bs - k * 12, 290, 112, "", r=18, a=.22))
    P.append(glass(730, 1176 + bs, 290, 112, (f'<div style="position:absolute;left:18px;top:12px;font-family:var(--m);font-size:13px;font-weight:700;color:#222">RECRUITMENT &nbsp; 2026</div>'
                                         f'<div style="position:absolute;left:18px;top:36px;font-family:var(--e);font-weight:600;font-size:24px;color:#0A0A0A">Open now</div>'
                                         f'<div style="position:absolute;left:18px;top:72px;font-family:var(--m);font-weight:700;font-size:14px;color:#0A0A0A">{URL} &rarr;</div>'), r=18, a=.62))
    return "r4_haggling" + ("_story" if story else ""), page("".join(P), bg="#0b1030"), [("h0", 70, y0, 940, size), ("h1", 70, y0 + step, 940, size), ("h2", 70, y0 + 2 * step, 940, size)]

# ================================================================= R5  website-page layout (reference 5)
def r5():
    P = []
    # nav
    P.append(B.logo(dark=False, x=48, y=26))
    for i, s_ in enumerate(["Teams +", "Drives", "Magazine", "Shikshaq"]):
        P.append(t(s_, 330 + i * 130, 30, 19, font="e", weight=400, tag=f"nav{i}"))
    P.append(f'<div style="position:absolute;right:0;top:0;width:190px;height:78px;background:#0A0A0A;z-index:8;color:#fff;font-family:var(--e);font-weight:600;font-size:20px;line-height:78px;text-align:center">Apply now &rarr;</div>')
    # headline: serif, last phrase italic (the reference's mechanism)
    P.append(f'<div style="position:absolute;left:48px;top:112px;width:620px;font-family:var(--s);font-size:100px;line-height:96px;letter-spacing:-.02em;color:#0A0A0A;z-index:8">'
             f'Fests, drives and startups, run by people <i>still doing homework.</i></div>')
    P.append(t("Real vendors, real drives, real deadlines. Come to one drive first, decide after.", 700, 262, 20, color="#555", w=316, lh=30, tag="sub"))
    P.append(f'<div style="position:absolute;left:700px;top:382px;width:170px;height:56px;background:#0A0A0A;z-index:8;color:#fff;font-family:var(--e);font-weight:600;font-size:19px;line-height:56px;text-align:center">Apply now &rarr;</div>')
    P.append(t("Read the magazine", 888, 396, 16, tag="lnk"))
    # strip: dithered photos + flat colour tiles
    sy, sh, tw = 566, 168, 164
    def tile(i, kind, **kw):
        x = 48 + i * tw
        if kind == "dither":
            im = dither(cover(kw["rel"], tw, sh, fy=kw.get("fy", .4), fx=kw.get("fx", .5), s=1.6), kw["light"], cell=5)
            return img(uri(im, "PNG"), x, sy, tw, sh, z=5)
        if kind == "block":
            return (f'<div style="position:absolute;left:{x}px;top:{sy}px;width:{tw}px;height:{sh}px;background:{kw["col"]};z-index:5">'
                    f'<div style="position:absolute;left:14px;top:12px;font-family:var(--e);font-size:13px;color:#0A0A0A">{kw["top"]}</div>'
                    f'<div style="position:absolute;left:14px;bottom:34px;font-family:var(--s);font-size:27px;line-height:28px;color:#0A0A0A">{kw["name"]}</div>'
                    f'<div style="position:absolute;left:14px;bottom:12px;font-family:var(--e);font-size:12px;color:#0A0A0A">{kw["sub"]}</div></div>')
        return (f'<div style="position:absolute;left:{x}px;top:{sy}px;width:{tw}px;height:{sh}px;background:#0A0A0A;z-index:5">'
                f'<div style="position:absolute;left:{tw//2-46}px;top:{sh//2-46}px;width:92px;height:92px">{shapes.brush_asterisk() if False else dd.stamp("burst", PINK)}</div></div>')
    P += [tile(0, "dither", rel=P_FACES, light="#FF5A1F"), tile(1, "block", col="#4A73FF", top="Welfare · summer", name="Sharbat drive", sub="4.5 L handed out"),
          tile(2, "glyph"), tile(3, "dither", rel=P_DESK, light="#4A73FF", fy=.6), tile(4, "block", col="#FF8AD6", top="Events · Nov 2026", name="Disco Diwali", sub="Masquerade Sangeet"),
          tile(5, "dither", rel=P_JAR, light="#7FE3A4", fy=.4)]
    # section title
    P.append(f'<div style="position:absolute;left:48px;top:770px;width:520px;font-family:var(--s);font-size:62px;line-height:62px;letter-spacing:-.02em;z-index:8">Four ways in, one form.</div>')
    P.append(t("Pick the team that sounds like your kind of chaos.", 700, 790, 19, color="#555", w=326, lh=26, tag="s2"))
    # four colour blocks
    blocks = [("#4A73FF", "01 · events", "Events", "Fests, sports days and a dance floor built from nothing.", "circle"),
              ("#FF5A1F", "02 · welfare", "Welfare", "Sharbat in summer, biscuits for strays, a Sunday class for 65+ kids.", "half"),
              ("#FF8AD6", "03 · startups", "Startups", "Crftd sells the clothes. ShikshAQ finds the tutor. Students run both.", "dots"),
              ("#7FE3A4", "04 · magazine", "Magazine", "Written and published by students. Nobody makes you write about your summer.", "star")]
    bx, by, bw, bh = 48, 866, 240, 330
    for i, (col, top, name, desc, icon) in enumerate(blocks):
        x = bx + i * (bw + 8)
        ic = {"circle": '<circle cx="20" cy="20" r="20" fill="#0A0A0A"/>',
              "half": '<path d="M0 20a20 20 0 0 1 40 0z" fill="#0A0A0A"/><path d="M0 24a20 20 0 0 0 40 0z" fill="#0A0A0A"/>',
              "dots": '<circle cx="10" cy="10" r="9" fill="#0A0A0A"/><circle cx="30" cy="10" r="9" fill="#0A0A0A"/><circle cx="10" cy="30" r="9" fill="#0A0A0A"/><circle cx="30" cy="30" r="9" fill="#0A0A0A"/>',
              "star": '<g stroke="#0A0A0A" stroke-width="4" stroke-linecap="round"><path d="M20 2v36M2 20h36M7 7l26 26M33 7L7 33"/></g>'}[icon]
        P.append(f'<div style="position:absolute;left:{x}px;top:{by}px;width:{bw}px;height:{bh}px;background:{col};z-index:5">'
                 f'<div style="position:absolute;left:16px;top:16px;font-family:var(--e);font-size:13px;color:#0A0A0A">{top}</div>'
                 f'<svg style="position:absolute;right:16px;top:14px" width="40" height="40" viewBox="0 0 40 40">{ic}</svg>'
                 f'<div style="position:absolute;left:16px;bottom:96px;font-family:var(--s);font-size:40px;line-height:40px;color:#0A0A0A">{name}</div>'
                 f'<div style="position:absolute;left:16px;bottom:16px;width:{bw-32}px;font-family:var(--e);font-size:14px;line-height:20px;color:#0A0A0A">{desc}</div></div>')
    # black "how it works" band, numerals running off the bottom like the reference
    P.append(f'<div style="position:absolute;left:0;top:1222px;width:{W}px;height:{H-1222}px;background:#0A0A0A;z-index:4"></div>')
    P.append(f'<div style="position:absolute;left:48px;top:1240px;font-family:var(--s);font-size:44px;line-height:44px;color:#fff;z-index:8">Come in.</div>')
    P.append(t("Apply and you are in the community. Join a team when you find yours.", 620, 1244, 15, color="#bbb", w=396, lh=22, tag="how"))
    for i, (c, n) in enumerate([("#3DA9FC", "Events"), ("#1B8A5A", "Welfare"), ("#FF4D2E", "Crftd"), ("#FFC700", "ShikshAQ")]):
        P.append(f'<div style="position:absolute;left:{48+i*248}px;top:{1300}px;font-family:var(--s);font-size:80px;line-height:80px;color:{c};z-index:8">{n}</div>')
    return "r5_site", page("".join(P)), [("sub", 700, 262, 316, 90)]

async def main():
    global H
    os.makedirs(OUT, exist_ok=True)
    jobs = [("r1", r1, {}, 1350), ("r2", r2, {}, 1350), ("r3", r3, {}, 1350), ("r4", r4, {}, 1350), ("r5", r5, {}, 1350),
            ("r3s", r3, {"story": True}, 1920), ("r4s", r4, {"story": True}, 1920)]
    async with B.session():
        for key, fn, kw, hh in jobs:
            if len(sys.argv) > 1 and key not in sys.argv[1:]: continue
            H = hh
            res = fn(**kw)
            if asyncio.iscoroutine(res): res = await res
            name, html, els = res
            await B.render(html, f"{OUT}/{name}.png", W, H, elements=els or None, page_bg="var(--bg)")
            print("rendered", name)
        H = 1350
if __name__ == "__main__":
    asyncio.run(main())
