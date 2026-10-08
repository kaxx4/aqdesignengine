"""REVER x DISCO DIWALI 2026: the 14-slide sponsorship deck, TerraThon look (Workflow C, bespoke build; user 2026-10-08).

Brief: "a disco diwali deck for location and food partner Rever", text supplied verbatim in rever_deck_text_1.md (copy is NOT edited here), then
"do a terrathon style where you generate fresh stickers and stuff".  So the deck is built in the TerraThon system (brain/TERRATHON.md): pure black ground with
white flecks, blue shuriken furniture that never rotates, white slabs with an orchid border and a small tilt, StretchPro / Sigmar One display type,
NeutralFace for labels and values, cream CTA pills, AQ logo bottom-left.  Every sticker is drawn fresh in scratchpad/rever_deck_stickers.py (the kit's die-cut
treatment); the disco ball, diya and ticket are the ones already drawn for the Disco Diwali ticket posters.

Adaptations (CLAUDE.md sec 2 rule 4), recorded:
  * 1920x1080 landscape (16:9), not a feed canvas: a deck is read on a screen / shared as PDF.  Margin M=96.
  * Palette is TerraThon's own (user ruling in TERRATHON.md sec 4), so Rever's crimson appears only inside Rever's real logo (transparent PNG cut from the file
    the user supplied, engine/assets/rever/rever_logo.png), never as a deck colour.
  * Instrument Serif is not used: TerraThon's voice is Sigmar One for the emphasis phrase of each heading (one per slide).
  * Body copy is Eina (readable at paragraph size); labels and values are NeutralFace 400 / 900, as in the kit.
  * Real assets only: the photos are Disco Diwali 2025 (faceless / backs-of-heads frames), the QR is the real @ngo.aquaterra code already in the repo.  No invented
    stats; every number on a slide is from the supplied text.  The 2026 funds-raised cell is blank in the source, so it reads "To come".
  * No Disco Diwali sticker carries text, so nothing in the kit can fall out of date.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_rever_deck.py [1 2 3 ...]     ->  out/rever_deck/slide_NN.png  (+ rever_disco_diwali_deck.pdf when all 14 are rendered)
"""
import asyncio, base64, importlib.util, io, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scratchpad"))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


tt = _load("tt_events", "scratchpad/tt_events.py")
stk = _load("rever_deck_stickers", "scratchpad/rever_deck_stickers.py")
core, B = tt.core, tt.B
lay = tt.load("layout")
from PIL import Image
import numpy as np

W, H, M = 1920, 1080, 96
TOTAL = 28
GROUND, ORCHID, HALO, SLAB, INK, WHITE, CTA = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL
GREEN, BLUE, GD = "#2FD284", "#0396FF", "#1B9A63"
OUT = os.path.join(ROOT, "out", "rever_deck")
P_DANCE = "engine/assets/terrathon/dd_photos/dance.jpg"
P_BLUE = "engine/assets/img/events/unsorted-2026-10-07/07_dance-blur-blue-light.jpg"
P_PURPLE = "engine/assets/img/events/unsorted-2026-10-07/08_cards-hall-crowd-purple.jpg"
P_CROWD = "engine/assets/img/events/unsorted-2026-10-07/12_dark-crowd-star-balloons.jpg"
P_GREEN = "engine/assets/img/events/unsorted-2026-10-07/05_cards-hall-dance-green-light.jpg"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


REVER = b64(os.path.join(ROOT, "engine/assets/rever/rever_logo.png"), "image/png")
QR = b64(os.path.join(ROOT, "engine/assets/terrathon/qr_instagram_ngo_aquaterra.svg"), "image/svg+xml")
_PH = {}


def photo_full(path, maxw, q=84):
    """Whole photo (aspect kept), resized so its long side is maxw, as a data URI."""
    k = (path, maxw, "full")
    if k not in _PH:
        im = Image.open(os.path.join(ROOT, path)).convert("RGB")
        r = maxw / max(im.size)
        if r < 1: im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
        _PH[k] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _PH[k]


def photo(path, size, focus=(.5, .5), q=82):
    """Square, centre-focused JPEG crop of one of the real Disco Diwali photos, as a data URI."""
    k = (path, size, focus)
    if k not in _PH:
        im = Image.open(os.path.join(ROOT, path)).convert("RGB")
        s = min(im.size); x0 = int((im.width - s) * focus[0]); y0 = int((im.height - s) * focus[1])
        im = im.crop((x0, y0, x0 + s, y0 + s)).resize((size, size), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=q)
        _PH[k] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _PH[k]


CSS = f"""<style>{tt.FONT_CSS}
.k{{font-family:var(--d);font-weight:400;text-transform:uppercase;letter-spacing:.03em}}
.v{{font-family:var(--d);font-weight:900}}
.b{{font-family:var(--e);font-weight:400}}
.sg{{font-family:SigmarOne;-webkit-text-stroke:.03em currentColor;letter-spacing:{tt.SG_LS}em}}
.st{{font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE}em currentColor;letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT}}}
.bul{{display:flex;gap:14px;align-items:flex-start}}
.bul i{{flex:none;width:15px;height:15px;border-radius:50%;background:{ORCHID};margin-top:.5em;border:2px solid {INK}}}
</style>"""


class Slide:
    def __init__(s, n, seed=None, specks_on=True):
        s.n, s.parts, s.els, s.tp, s.conts = n, [], [], [], []
        rnd = random.Random(seed or n * 17)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>'
                         for _ in range(420))
        s.parts += [CSS] + ([f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>'] if specks_on else [])

    def add(s, html): s.parts.append(html)
    def el(s, label, x, y, w, h): s.els.append((label, x, y, w, h))
    def text_pair(s, label, fg, bg, size, bold=True): s.tp.append((label, fg, bg, size, bold))

    # ---- furniture -------------------------------------------------------------
    def stars(s, pts, size=96):
        im, src = tt.crop_to_alpha("shuriken.png")
        for i, (x, y) in enumerate(pts):
            s.add(f'<img class="measure" data-tag="star{i}" src="{src}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:9">')
            s.el(f"star{i}", x, y, size, size)

    def sticker(s, label, built, x, y, rot=0, z=9):
        svg, w, h = built
        s.add(f'<div class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;z-index:{z};transform:rotate({rot}deg)">{svg}</div>')
        b = lay.rotated_bbox(x, y, w, h, rot) if rot else (x, y, w, h)
        s.el(label, *(tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])))

    def photo_circle(s, label, path, x, y, d, focus=(.5, .5), cap=True, ring=14, rot=0):
        """Real Disco Diwali 2025 photo in an orchid-ringed circle (the kit's photo treatment), optional small caption under it."""
        s.add(f'<img class="measure" data-tag="{label}" src="{photo(path, int(d * 1.5), focus)}" style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
              f'border-radius:50%;border:{ring}px solid {ORCHID};object-fit:cover;z-index:8;transform:rotate({rot}deg)">')
        s.el(label, x, y, d, d)
        if cap:
            s.add(f'<div class="measure k" data-tag="{label}_cap" style="position:absolute;left:{x}px;top:{y + d + 8}px;width:{d}px;text-align:center;font-size:18px;color:{WHITE};z-index:6;white-space:nowrap">Disco Diwali 2025</div>')
            s.el(label + "_cap", x, y + d + 8, d, 20)

    def cord(s, x, y0, y1):
        s.add(f'<div style="position:absolute;left:{x}px;top:{y0}px;width:4px;height:{y1 - y0}px;background:{HALO};z-index:3"></div>')

    def ball(s, label, w, x, y, rot=0, cord_from=None):
        svg, h = tt_ball(w)
        if cord_from is not None:
            s.cord(x + w / 2 - 2, cord_from, y + w * 100 / 500 + 6)
        s.sticker(label, (svg, w, h), x, y, rot, 6)

    def slab(s, label, x, y, w, h, inner, rot=0, fill=SLAB, border=10, radius=34, z=8, pad="30px 36px", extra="", tilt=False):
        rot = rot if tilt else 0
        s.add(f'<div class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);background:{fill};'
              f'border:{border}px solid {ORCHID};border-radius:{radius}px;z-index:{z};padding:{pad};color:{INK};overflow:hidden;{extra}">{inner}</div>')
        s.el(label, x - 2, y - 2, w + 4, h + 4); s.conts.append(label)

    def panel(s, label, x, y, w, h, inner, rot=0, z=8, pad="28px 34px"):
        """Dark card with an orchid border (the slab's night-mode twin), for text that sits on the black ground."""
        s.add(f'<div class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);background:#0B0B0D;'
              f'border:5px solid {ORCHID};border-radius:30px;z-index:{z};padding:{pad};color:{WHITE};overflow:hidden">{inner}</div>')
        s.el(label, x - 2, y - 2, w + 4, h + 4); s.conts.append(label)

    def pill(s, label, x, y, text, size=34, w=None, align="left", z=12):
        """Cream CTA pill with an orchid border (the kit's footer pill)."""
        s.add(f'<div class="measure v" data-tag="{label}" style="position:absolute;{align}:{x}px;top:{y}px;{"width:%dpx;" % w if w else ""}height:{size * 2.1:.0f}px;border:8px solid {ORCHID};border-radius:999px;'
              f'background:{CTA};display:flex;align-items:center;justify-content:center;padding:0 {size * .9:.0f}px;font-size:{size}px;color:{INK};white-space:nowrap;z-index:{z}">{text}</div>')

    def photo_rect(s, label, path, x, y, w, h, focus="50% 50%", cap="Disco Diwali 2025", ring=8, radius=30, z=8, maxw=1400):
        """Real Disco Diwali 2025 photo in an orchid-bordered rounded rectangle, with a small cream caption chip."""
        s.add(f'<div class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border:{ring}px solid {ORCHID};border-radius:{radius}px;'
              f'background:url({photo_full(path, maxw)}) {focus}/cover;z-index:{z}"></div>')
        s.el(label, x, y, w, h)
        if cap:
            s.add(f'<div class="measure v" data-tag="{label}_cap" style="position:absolute;left:{x + 22}px;top:{y + h - 62}px;height:42px;padding:0 20px;border-radius:999px;background:{CTA};'
                  f'border:4px solid {ORCHID};display:flex;align-items:center;font-size:19px;color:{INK};z-index:{z + 1};white-space:nowrap">{cap.upper()}</div>')
            s.el(label + "_cap", x + 22, y + h - 62, 260, 42)

    def chrome(s, kicker=None):
        """AQ logo bottom-left; Rever's pill + the slide count bottom-right; kicker top-left."""
        s.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{M}px;top:{H - 100}px;height:50px;z-index:9">')
        s.el("logo", M, H - 100, 296, 50)
        rw = 214
        s.add(f'<div class="measure" data-tag="rever_pill" style="position:absolute;left:{W - M - rw}px;top:{H - 108}px;width:{rw}px;height:66px;border:6px solid {ORCHID};border-radius:999px;'
              f'background:#fff;display:flex;align-items:center;justify-content:center;z-index:12"><img src="{REVER}" style="height:36px"></div>')
        s.el("rever_pill", W - M - rw, H - 108, rw, 66)
        s.add(f'<div class="measure k" data-tag="count" style="position:absolute;right:{M + rw + 16}px;top:{H - 96}px;font-size:24px;line-height:1;color:{WHITE};z-index:9;white-space:nowrap;background:rgba(0,0,0,.62);padding:8px 16px;border-radius:999px">{s.n:02d} / {TOTAL}</div>')
        s.el("count", W - M - rw - 24 - 96, H - 90, 96, 26)
        if kicker:
            s.add(f'<div class="measure k" data-tag="kicker" style="position:absolute;left:{M}px;top:56px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">{kicker}</div>')
            s.el("kicker", M, 56, 760, 30)
            s.text_pair("kicker", WHITE, GROUND, 26, False)

    async def heading(s, x, y, w, white, orchid=None, ws=80, os_=62, gap=0, label="h1", wl=None):
        """White NeutralFace headline + (optional) Sigmar One orchid emphasis line. Returns the y below the block."""
        items = [dict(text=white.upper().replace("\n", " "), font="d", size=ws, weight=900, max_width=w)]
        if orchid: items.append(dict(text=orchid, font="SigmarOne", size=os_, weight=400, letter_spacing=f"{tt.SG_LS}em", max_width=w))
        m = await B.measure_text(items, W, H, extra_css=tt.FONT_CSS)
        hw = (wl or m[0]["lines"]) * ws * .98
        s.add(f'<div class="measure v" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{ws}px;line-height:.98;color:{WHITE};z-index:6">{white.upper().replace("\n", "<br>")}</div>')
        s.el(label, x, y, min(w, m[0]["text_w"]), hw); s.text_pair(label, WHITE, GROUND, ws, True)
        bottom = y + hw
        if orchid:
            ho = m[1]["lines"] * os_ * 1.08; y2 = bottom + gap
            s.add(f'<div class="measure sg" data-tag="{label}o" style="position:absolute;left:{x}px;top:{y2}px;width:{w}px;font-size:{os_}px;line-height:1.08;color:{ORCHID};z-index:6">{orchid}</div>')
            s.el(label + "o", x, y2, min(w, m[1]["text_w"]), ho); s.text_pair(label + "o", ORCHID, GROUND, os_, True)
            bottom = y2 + ho
        return bottom

    async def render(s, out, ignore_extra=()):
        html = B.page(W, H, GROUND, "".join(s.parts), grain=False)
        txt = re.sub(r"<style>.*?</style>|<svg.*?</svg>|<img[^>]*>", " ", "".join(s.parts), flags=re.S)
        txt = re.sub(r"<br\s*/?>", " ", txt); txt = re.sub(r"</(div|p|span)>", "\n", txt); txt = re.sub(r"<[^>]+>", "", txt)
        import html as _h
        lines = [" ".join(_h.unescape(l).split()) for l in txt.split("\n")]
        os.makedirs(f"{OUT}/text", exist_ok=True)
        open(f"{OUT}/text/{os.path.basename(out)[:-4]}.txt", "w").write("\n".join(l for l in lines if l))
        names = [e[0] for e in s.els]
        deco = [n for n in names if n.startswith(("st_", "star", "ph_"))]
        ign = set()
        for a in deco:
            for b in names:
                if b != a and (b in s.conts or b.startswith(("st_", "star", "ph_"))): ign.add((a, b))
        ign |= set(ignore_extra)
        await B.render(html, out, W, H, elements=s.els, text_pairs=s.tp, containers=tuple(s.conts), page_bg=GROUND,
                       collision_ignore=ign, margin=24)
        return html


def tt_ball(w):
    svg, h = stk.disco_ball(w)
    return svg, h


def bullets(items, size=23, gap=14, color=INK):
    return "".join(f'<div class="bul b" style="font-size:{size}px;line-height:1.28;color:{color};margin-bottom:{gap}px"><i></i><span>{t}</span></div>' for t in items)


def numdot(n, d=54, fs=28, fill=ORCHID):
    return (f'<div class="v" style="flex:none;width:{d}px;height:{d}px;border-radius:50%;background:{fill};border:3px solid {INK};display:flex;align-items:center;justify-content:center;'
            f'font-size:{fs}px;color:{INK}">{n}</div>')


def label(txt, size=22, color=INK, extra=""):
    return f'<div class="k" style="font-size:{size}px;color:{color};line-height:1.1;{extra}">{txt}</div>'


# =============================================================================== slides
U = "engine/assets/img/events/unsorted-2026-10-07/"
D = "engine/assets/terrathon/dd_photos/"
PH = dict(blue=U + "07_dance-blur-blue-light.jpg", arrivals=U + "03_IMG_1451_red-drapes-entrance.jpg", green=U + "05_cards-hall-dance-green-light.jpg",
          greenp=U + "11_dance-green-light-portrait.jpg", friends=U + "06_three-friends-fairy-lights.jpg", booth=U + "10_disco-diwali-photo-booth.jpg",
          phone=U + "13_IMG_1500_dance-pink-light-phone.jpg", purple=U + "08_cards-hall-crowd-purple.jpg", wall=D + "decor.jpg", dance=D + "dance.jpg",
          group=D + "group.jpg", courtyard=U + "09_night-courtyard-string-lights-crowd.jpg", banner=U + "01_IMG_7180_group-aquaterra-banner.jpg",
          pink=U + "02_IMG_7028_group-pink-balloons.jpg", crowd=U + "12_dark-crowd-star-balloons.jpg")


def ddt_ticket(w): svg, h = stk.ticket(w); return svg, w, h
def ddt_diya(w): svg, h = stk.diya(w); return svg, w, h
def ddt_spark(sz, fill, fid): return stk.spark(sz, fill, fid)


def cap_chip(s, label_, x, y, text, size=28, z=12, shadow=True):
    """Cream caption pill with an orchid border: the kit's CTA pill, used for photo captions."""
    s.add(f'<div class="measure v" data-tag="{label_}" style="position:absolute;left:{x}px;top:{y}px;height:{size * 2.1:.0f}px;border:6px solid {ORCHID};border-radius:999px;background:{CTA};'
          f'display:flex;align-items:center;padding:0 {size * .9:.0f}px;font-size:{size}px;color:{INK};white-space:nowrap;z-index:{z}">{text.upper()}</div>')


# ---------------------------------------------------------------- photo slides
async def photo_full_slide(n, key, title, caption, focus="50% 50%", label_="DISCO DIWALI 2025", stickers=(), tsize=112):
    """Full-bleed real photo, a two-line title bottom-left and a caption pill under it (the 'title image slide')."""
    s = Slide(n, specks_on=False)
    s.add(f'<div style="position:absolute;inset:0;background:url({photo_full(PH[key], 2000)}) {focus}/cover;z-index:0"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,.94) 0%,rgba(0,0,0,.74) 26%,rgba(0,0,0,0) 60%)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 20%)"></div>')
    s.add(f'<div class="measure k" data-tag="eyebrow" style="position:absolute;left:{M}px;top:56px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap;letter-spacing:.08em">{label_}</div>')
    s.el("eyebrow", M, 56, 420, 28); s.text_pair("eyebrow", WHITE, GROUND, 26, False)
    lines = title.split("\n")
    th = len(lines) * tsize * .96
    ty = 846 - th
    s.add(f'<div class="measure v" data-tag="title" style="position:absolute;left:{M}px;top:{ty}px;font-size:{tsize}px;line-height:.96;color:{WHITE};z-index:6;white-space:nowrap;text-shadow:0 4px 24px rgba(0,0,0,.5)">{"<br>".join(l.upper() for l in lines)}</div>')
    s.el("title", M, ty, 1500, th); s.text_pair("title", WHITE, GROUND, tsize, True)
    cap_chip(s, "cap", M, 872, caption, 28)
    s.el("cap", M, 872, 1300, 59)
    for i, (built, x, y, rot) in enumerate(stickers):
        s.sticker(f"st_{i}", built, x, y, rot, 9)
    s.chrome()
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def photo_split_slide(n, key, title, caption, focus="50% 50%", label_="DISCO DIWALI 2025", stickers=(), tsize=100):
    """Portrait photo as a full-height right panel; title, caption and a sticker on the black left."""
    s = Slide(n)
    s.add(f'<div class="measure" data-tag="ph_panel" style="position:absolute;left:1000px;top:0;width:920px;height:{H}px;background:url({photo_full(PH[key], 1600)}) {focus}/cover;border-left:10px solid {ORCHID};z-index:3"></div>')
    s.el("ph_panel", 1000, 0, 920, H)
    s.add(f'<div class="measure k" data-tag="eyebrow" style="position:absolute;left:{M}px;top:56px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap;letter-spacing:.08em">{label_}</div>')
    s.el("eyebrow", M, 56, 420, 28); s.text_pair("eyebrow", WHITE, GROUND, 26, False)
    lines = title.split("\n")
    mm = await B.measure_text([dict(text=l.upper(), font="d", size=100, weight=900) for l in lines], W, H)
    tsize = min(tsize, 100 * 850 / max(r["text_w"] for r in mm))
    th = len(lines) * tsize * .96
    ty = 330
    s.add(f'<div class="measure v" data-tag="title" style="position:absolute;left:{M}px;top:{ty}px;font-size:{tsize}px;line-height:.96;color:{WHITE};z-index:6;white-space:nowrap">{"<br>".join(l.upper() for l in lines)}</div>')
    s.el("title", M, ty, 860, th); s.text_pair("title", WHITE, GROUND, tsize, True)
    s.slab("capcard", M, ty + th + 36, 760, 150, f'<div class="v" style="font-size:30px;line-height:1.15;color:{INK};text-transform:uppercase;display:flex;align-items:center;height:100%">{caption}</div>', pad="14px 34px", border=8)
    s.text_pair("capcard", INK, SLAB, 30, True)
    for i, (built, x, y, rot) in enumerate(stickers):
        s.sticker(f"st_{i}", built, x, y, rot, 9)
    s.chrome()
    await s.render(f"{OUT}/slide_{n:02d}.png")


def P(key, *a, **k):
    f = photo_split_slide if k.pop("split", False) else photo_full_slide
    async def run(n): await f(n, key, *a, **k)
    return run


# ---------------------------------------------------------------- cover
async def s_cover(n):
    s = Slide(n, specks_on=False)
    s.add(f'<div style="position:absolute;inset:0;background:url({photo_full(PH["wall"], 1500)}) 62% 38%/cover;z-index:0;filter:brightness(1.25) saturate(1.1)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.93) 28%,rgba(0,0,0,.5) 52%,rgba(0,0,0,.08) 100%)"></div>')
    s.add('<div style="position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(0,0,0,.9) 0%,rgba(0,0,0,0) 28%)"></div>')
    s.add(f'<div class="measure k" data-tag="eyebrow" style="position:absolute;left:{M}px;top:64px;font-size:26px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap;letter-spacing:.08em">A PARTNERSHIP PROPOSAL FOR REVER</div>')
    s.el("eyebrow", M, 64, 620, 28); s.text_pair("eyebrow", WHITE, GROUND, 26, False)
    s.add(f'<div class="measure k" data-tag="t1" style="position:absolute;left:{M}px;top:136px;font-size:96px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">REVER x</div>')
    s.el("t1", M, 142, 444, 84); s.text_pair("t1", WHITE, GROUND, 96, False)
    s.add(f'<div class="measure v" data-tag="year" style="position:absolute;left:{M + 484}px;top:140px;height:84px;border:8px solid {ORCHID};border-radius:999px;background:{SLAB};'
          f'display:flex;align-items:center;padding:0 34px;font-size:50px;color:{INK};z-index:6">2026</div>')
    s.el("year", M + 484, 140, 215, 84)
    s.add(f'<div class="measure v" data-tag="t2" style="position:absolute;left:{M}px;top:242px;font-size:196px;line-height:.9;color:{WHITE};z-index:6;white-space:nowrap">DISCO<br>DIWALI</div>')
    s.el("t2", M, 252, 720, 360); s.text_pair("t2", WHITE, GROUND, 196, True)
    s.add(f'<div class="measure sg" data-tag="sub" style="position:absolute;left:{M}px;top:648px;width:860px;font-size:50px;line-height:1.1;color:{ORCHID};z-index:6">'
          f'A masquerade evening, hosted at Rever Skydeck.</div>')
    s.el("sub", M, 648, 860, 110); s.text_pair("sub", ORCHID, GROUND, 50, True)
    inner = (f'<div style="display:flex;align-items:center;gap:36px;height:100%"><img src="{REVER}" style="height:70px;flex:none">'
             f'<div style="width:5px;align-self:stretch;background:{ORCHID};border-radius:3px"></div>'
             f'<div class="v" style="font-size:38px;line-height:1.05;color:{INK}">EXCLUSIVE FOOD AND<br>LOCATION PARTNER</div></div>')
    s.slab("slab", M, 800, 960, 140, inner, rot=-1.0, pad="10px 38px", radius=44, tilt=True)
    s.text_pair("slab", INK, SLAB, 38, True)
    s.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{M}px;top:{H - 90}px;height:50px;z-index:9">'); s.el("logo", M, H - 90, 296, 50)
    s.pill("cta", M, H - 112, "TEAM AQUATERRA, EST. 2021&nbsp;&nbsp;|&nbsp;&nbsp;10 NOVEMBER 2026", 28, align="right")
    s.el("cta", W - M - 700, H - 112, 700, 59); s.text_pair("cta", INK, CTA, 28, True)
    s.cord(1488, 0, 76); s.ball("st_ball", 340, 1318, 70, 0)
    s.sticker("st_mask", stk.mask(width=820, seed=3), 1040, 290, -7)
    s.sticker("st_sp1", (ddt_spark(70, GREEN, "c1"), 70, 70), 1010, 230, 0, 7)
    s.sticker("st_sp2", (ddt_spark(56, ORCHID, "c2"), 56, 56), 1130, 120, 0, 7)
    s.stars([(1760, 80)], 90)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- the partnership
async def s_brief(n):
    s = Slide(n); s.chrome("THE PARTNERSHIP IN BRIEF")
    s.stars([(1760, 40)], 80)
    y = await s.heading(M, 110, 880, "One evening.\n400+ guests.", "Hosted entirely at Rever Skydeck.", 76, 54, wl=2)
    s.add(f'<div class="measure b" data-tag="body" style="position:absolute;left:{M}px;top:{y + 30}px;width:840px;font-size:28px;line-height:1.38;color:{WHITE};z-index:6">'
          f'Disco Diwali is one of Kolkata\'s largest student evenings. This year it is a masquerade, hosting an estimated 400+ guests at Rever Skydeck. '
          f'Headlining the night, we are flying in a DJ from Mumbai who made his debut with Blunt Entertainment.</div>')
    s.el("body", M, y + 30, 840, 190); s.text_pair("body", WHITE, GROUND, 28, False)
    s.photo_rect("ph_a", PH["dance"], M, 650, 780, 280, "50% 55%")
    s.sticker("st_record", stk.record(width=210), M + 650, 770, -6, 11)
    s.add(f'<div class="measure k" data-tag="lab" style="position:absolute;left:1040px;top:122px;font-size:24px;line-height:1;color:{ORCHID};z-index:6;white-space:nowrap">WHAT THE PARTNERSHIP OFFERS REVER</div>')
    s.el("lab", 1040, 122, 620, 26); s.text_pair("lab", ORCHID, GROUND, 24, False)
    tiles = [("Rever Skydeck as the sole venue for the evening", stk.pin(100)), ("Exclusive food rights, with a menu curated for the event", stk.cloche(120)),
             ("An introduction to a young audience, at an event Rever hosts", stk.heart(100)), ("Rever's name across our content, our team and the event itself", stk.shirt(104))]
    for i, (t, st) in enumerate(tiles):
        inner = (f'<div style="display:flex;align-items:center;gap:26px;height:100%"><div style="flex:none;width:120px;display:flex;justify-content:center">{st[0]}</div>'
                 f'<div class="v" style="font-size:30px;line-height:1.12;color:{INK}">{t.upper()}</div></div>')
        s.slab(f"tile{i}", 1040, 170 + i * 190, 768, 170, inner, pad="12px 30px")
    s.text_pair("tile0", INK, SLAB, 30, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_location(n):
    s = Slide(n); s.chrome("LOCATION PARTNER, AND MORE")
    s.stars([(1760, 40)], 80)
    y = await s.heading(M, 110, 1000, "More than a venue.", "The only kitchen of the night.", 76, 54)
    body = ("Rever comes in as our Location Partner, and we will make sure Rever is also the Exclusive Food Partner. No outside vendors and no competing stalls: Rever's menu is the only food menu at the event.",
            "We would love to build a special event menu with your team. Rever's kitchen decides what goes on it, and a short, tight menu keeps service fast for 400+ guests and quality consistent. Every guest gets a first taste of Rever.")
    s.add(f'<div class="measure b" data-tag="body" style="position:absolute;left:{M}px;top:{y + 36}px;width:900px;font-size:30px;line-height:1.38;color:{WHITE};z-index:6">'
          f'<p style="margin:0 0 20px">{body[0]}</p><p style="margin:0">{body[1]}</p></div>')
    s.el("body", M, y + 36, 900, 440); s.text_pair("body", WHITE, GROUND, 30, False)
    s.sticker("st_cloche", stk.cloche(width=520), 1180, 80, 5)
    s.sticker("st_pin", stk.pin(width=210), 1100, 470, -6)
    s.sticker("st_sp", (ddt_spark(64, GREEN, "c4"), 64, 64), 1480, 340, 0, 7)
    m = await B.measure_text([dict(text="ONE VENUE. ONE KITCHEN. ONE MENU,", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], W, H, extra_css=tt.FONT_CSS)
    fs = min(70, 100 * 1500 / m[0]["text_w"])
    inner = (f'<div class="st" style="font-size:{fs:.0f}px;line-height:1;color:{INK};white-space:nowrap;margin-top:6px">ONE VENUE. ONE KITCHEN. ONE MENU,</div>'
             f'<div class="sg" style="font-size:48px;line-height:1.1;color:{INK};margin-top:10px">and it is Rever\'s.</div>')
    s.slab("slab", M, 730, 1728, 226, inner, rot=-1.0, pad="22px 48px", tilt=True)
    s.text_pair("slab", INK, SLAB, 48, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- visibility, in two parts
def head_icon(title, icon, size=44, h=110):
    return (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:22px;height:{h}px"><div class="v" style="font-size:{size}px;line-height:1;color:{INK};text-transform:uppercase">{title}</div>'
            f'<div style="flex:none">{icon[0]}</div></div>')


async def s_vis1(n):
    s = Slide(n); s.chrome("YOUR BRAND, FRONT AND CENTRE  (1 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 900, "Visibility,", "in detail.", 76, 56, gap=4)
    cards = [("Visibility", ["Rever logo on all event deliverables: posters, posts, tickets, the ticket page and WhatsApp broadcasts", "Rever logo on all AquaTerra core team shirts",
                             "“Exclusive Food and Location Partner” billing everywhere", "On-ground branding at the venue and stage mentions on the night"], stk.shirt(140)),
             ("Reputation", ["Rever's Google reviews QR code displayed at the event, so guests can choose to leave their own honest review", "Our team does not write, buy or solicit reviews for Rever"], stk.review(170))]
    for i, (t, items, st) in enumerate(cards):
        s.slab(f"slab{i}", M + i * 888, 300, 840, 640, head_icon(t, st) + bullets(items, 30, 24), pad="34px 44px")
    s.text_pair("slab0", INK, SLAB, 30, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_vis2(n):
    s = Slide(n); s.chrome("YOUR BRAND, FRONT AND CENTRE  (2 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1200, "Promotion and content,", "in detail.", 76, 56, gap=4)
    cards = [("Promotion", ["Rever promoted on Instagram and across our WhatsApp community for close to a month", "Business card promotion for Rever", "A thank-you post after the event"], stk.megaphone(170)),
             ("Content", ["5 to 10 planned reels, plus regular casual content", "Our event photos and videos are free for Rever to use in its own marketing. Images of anyone under 18 are used only with guardian consent on file"], stk.phone(110))]
    for i, (t, items, st) in enumerate(cards):
        s.slab(f"slab{i}", M + i * 888, 300, 840, 480, head_icon(t, st) + bullets(items, 29, 22), pad="34px 44px")
    s.text_pair("slab0", INK, SLAB, 29, False)
    inner = (f'<div style="display:flex;gap:44px;align-items:center;height:100%"><div class="v" style="flex:none;font-size:34px;line-height:1.05;color:{ORCHID}">OUR<br>STANDARD</div>'
             f'<div class="b" style="font-size:27px;line-height:1.36;color:{WHITE}">This list is a baseline, not a ceiling. We aim to overachieve on every deliverable we commit to a sponsor. '
             f'We have done that for our partners in the past, and Rever will be no different.</div></div>')
    s.panel("standard", M, 812, 1728, 140, inner, pad="12px 44px")
    s.text_pair("standard", WHITE, "#0B0B0D", 27, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- audience, in two parts
async def s_aud1(n):
    s = Slide(n); s.chrome("AUDIENCE AND DEMOGRAPHICS  (1 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1600, "Who is in the room.", "A young crowd, introduced to Rever early.", 76, 56, gap=4)
    m = await B.measure_text([dict(text="16-19", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], W, H, extra_css=tt.FONT_CSS)
    fs = 100 * 480 / m[0]["text_w"]
    inner = (label("Age band, roughly", 28, INK, "margin-bottom:12px") + f'<div class="st" style="font-size:{fs:.0f}px;line-height:1.05;color:{INK};white-space:nowrap">16-19</div>')
    s.slab("age", M, 300, 620, 300, inner, rot=-1.0, pad="36px 44px", tilt=True)
    s.text_pair("age", INK, SLAB, 28, False)
    rows = [("Segment", "Senior high school students and college first-years from across Kolkata"),
            ("Group behaviour", "Arrive in friend groups, return for birthdays, celebrations and weekend plans"),
            ("Discovery", "Instagram-first, heavily influenced by peers and event content")]
    inner = "".join(f'<div style="margin-bottom:22px">{label(k, 24, ORCHID)}<div class="b" style="font-size:31px;line-height:1.22;color:{WHITE};margin-top:6px">{v}</div></div>' for k, v in rows)
    s.add(f'<div class="measure" data-tag="rows" style="position:absolute;left:{M + 700}px;top:290px;width:1020px;z-index:6">{inner}</div>')
    s.el("rows", M + 700, 290, 1020, 330); s.text_pair("rows", WHITE, GROUND, 31, False)
    s.photo_rect("ph_a", PH["group"], M, 650, 1728, 290, "50% 32%", cap="Disco Diwali 2025")
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_aud2(n):
    s = Slide(n); s.chrome("AUDIENCE AND DEMOGRAPHICS  (2 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1500, "The time slot.", "A young audience, introduced to Rever at the hours it is building.", 76, 52, gap=4)
    seg = lambda flex, bg, txt: (f'<div class="v" style="flex:{flex};background:{bg};border:4px solid {INK};border-radius:20px;display:flex;align-items:center;justify-content:center;text-align:center;'
                                 f'padding:10px 18px;font-size:34px;line-height:1.12;color:{INK}">{txt}</div>')
    bar = f'<div style="display:flex;gap:12px;height:230px;margin:16px 0 40px">{seg(3, "#E4DFD0", "AFTER SCHOOL, COLLEGE AND TUITION")}{seg(1.7, ORCHID, "5 TO 6 PM")}{seg(3, GREEN, "REVER&rsquo;S ESTABLISHED LATE-NIGHT TRADE")}</div>'
    inner = (label("The time slot", 28, INK) + bar +
             f'<div class="b" style="font-size:32px;line-height:1.4;color:{INK};max-width:1500px">This audience is free and looking for somewhere to go between 5 and 6 PM, after school, college and tuition hours. '
             f'That early evening window sits before Rever\'s established late-night trade, and it is exactly the window this audience fills.</div>')
    s.slab("slot", M, 340, 1728, 590, inner, pad="36px 48px")
    s.text_pair("slot", INK, SLAB, 30, False)
    s.sticker("st_clock", stk.clock(width=200), 1650, 205, 8, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- touchpoints
async def s_touch(n):
    s = Slide(n); s.chrome("BRAND TOUCHPOINTS")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1500, "Every point where a guest", "meets Rever.", 76, 56)
    cols = [("Before the event (after sign-off)", ["Rever tagged as venue on every ticket, post and story", "Reels shot at Rever Skydeck, published as collab posts",
                                "Callouts across our WhatsApp community and broadcast lists", "Rever featured on the ticket page and confirmation messages"], 500, stk.phone(78)),
            ("At the event", ["Branded banners and standees at entry, stage and food counters", "Rever branding on photo booth backdrops", "Stage mentions from our hosts and the DJ set",
                              "Rever's menu as the only menu, with branded menu boards", "Reviews QR code displayed at high-traffic points"], 650, stk.camera(112)),
            ("After the event", ["Promotion cards for guests, offering a return incentive on terms Rever sets (optional)", "Thank-you post and event recap featuring Rever",
                                 "Photo and video assets handed over for Rever's own use"], 500, stk.heart(96))]
    x = M
    for i, (t, items, w, st) in enumerate(cols):
        head = (f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;height:88px"><div class="v" style="font-size:32px;line-height:1;color:{INK};text-transform:uppercase">{t}</div>'
                f'<div style="flex:none">{st[0]}</div></div>')
        s.slab(f"slab{i}", x, 296, w, 548, head + bullets(items, 25, 16), pad="28px 32px")
        s.text_pair(f"slab{i}", INK, SLAB, 25, False)
        x += w + 24
    s.pill("callout", M, 868, "REVER STAYS IN VIEW FROM THE FIRST POSTER TO THE LAST STORY.", 34, align="left")
    s.el("callout", M, 868, 1250, 72); s.text_pair("callout", INK, CTA, 34, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- track record, in two parts (+ mosaic)
async def s_hist1(n):
    s = Slide(n); s.chrome("EVENT HISTORY AND TRACK RECORD  (1 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 96, 1500, "Five years of events that fill rooms", "and fund real work.", 66, 54)
    th = lambda t: f'<div class="k" style="font-size:21px;color:{INK};padding-bottom:10px;border-bottom:4px solid {ORCHID}">{t}</div>'
    td = lambda t: f'<div class="v" style="font-size:25px;line-height:1.15;color:{INK};padding:16px 0 10px">{t}</div>'
    cols = "grid-template-columns:260px 1fr 200px 150px;column-gap:18px"
    tab = (f'<div style="display:grid;{cols}">{th("Edition")}{th("Venue")}{th("Footfall")}{th("Funds raised")}'
           f'{td("DISCO DIWALI 2025")}{td("60 CHOWRINGHEE, WITH DJ AMAY")}{td("500+")}{td("RS. 4.3 LAKH")}'
           f'{td("DISCO DIWALI 2026")}{td("REVER SKYDECK, MASQUERADE")}{td("Up to 400+<br>(venue capacity)")}{td("TO COME")}</div>')
    s.slab("table", M, 290, 1080, 372, label("Disco Diwali, edition by edition", 26, INK, "margin-bottom:14px") + tab, pad="28px 36px")
    s.text_pair("table", INK, SLAB, 25, True)
    inner = f'<div class="sg" style="font-size:40px;line-height:1.1;color:{INK}">2025 filled the room and raised Rs. 4.3 lakh. 2026 is built around Rever Skydeck.</div>'
    s.slab("callout", M, 700, 1080, 240, inner, rot=-1.0, fill=ORCHID, border=12, pad="30px 44px", tilt=True)
    s.text_pair("callout", INK, ORCHID, 44, True)
    s.add(f'<div class="measure k" data-tag="lab" style="position:absolute;left:1240px;top:290px;font-size:24px;line-height:1;color:{ORCHID};z-index:6;white-space:nowrap">ACROSS THE AQ EVENTS PORTFOLIO</div>')
    s.el("lab", 1240, 290, 560, 26); s.text_pair("lab", ORCHID, GROUND, 24, False)
    stats = [("650+", "GUESTS AT STARRY NIGHT 2025"), ("400+", "GUESTS AT PARADOX"), ("1.11M+", "IMPRESSIONS ACROSS OUR LAST FEW EVENTS"), ("1,800+", "MEMBERS IN OUR WHATSAPP COMMUNITY")]
    m = await B.measure_text([dict(text=v, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT) for v, _ in stats], W, H, extra_css=tt.FONT_CSS)
    vfs = min(56, min(100 * 190 / r["text_w"] for r in m))
    for i, (v, l) in enumerate(stats):
        inner = (f'<div class="st" style="font-size:{vfs:.0f}px;line-height:1;color:{WHITE};margin-bottom:14px">{v}</div>'
                 f'<div class="k" style="font-size:19px;line-height:1.15;color:{ORCHID}">{l}</div>')
        s.panel(f"stat{i}", 1240 + (i % 2) * 296, 336 + (i // 2) * 290, 272, 262, inner, pad="30px 26px")
    s.text_pair("stat0", WHITE, "#0B0B0D", 56, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_hist2(n):
    s = Slide(n); s.chrome("EVENT HISTORY AND TRACK RECORD  (2 OF 2)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 96, 1500, "Who runs it.", None, 76)
    inner = (f'<div class="b" style="font-size:29px;line-height:1.4;color:{INK}">'
             'Team AquaTerra is a student-run, registered NGO, active since 2021, 80G certified and Darpan registered. Our student community spans 25+ schools across Kolkata. '
             'Net proceeds fund welfare work across the city.</div>')
    s.slab("who", M, 230, 860, 400, inner, pad="36px 40px")
    s.text_pair("who", INK, SLAB, 27, False)
    yrs = [("2021", 52), ("2022", 64), ("2023", 80), ("2024", 92), ("2025", 112)]
    bars = "".join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:8px"><div class="v" style="font-size:32px;color:{WHITE}">{v}</div>'
                   f'<div style="width:100%;height:{v * 1.7:.0f}px;background:{GREEN if y == "2025" else ORCHID};border:3px solid {HALO};border-radius:14px 14px 4px 4px"></div>'
                   f'<div class="k" style="font-size:21px;color:{WHITE}">{y}</div></div>' for y, v in yrs)
    inner = label("Projects completed per year", 25, ORCHID, "margin-bottom:8px") + f'<div style="display:flex;gap:20px;align-items:flex-end;height:300px">{bars}</div>'
    s.panel("chart", 1000, 230, 824, 412, inner, pad="26px 38px")
    s.text_pair("chart", WHITE, "#0B0B0D", 32, True)
    wi = [("1,600+", "doctor check-ups in the Sundarbans"), ("3,000+", "dogs fed"), ("5,000+", "saplings planted"), ("2.5 tons", "of clothes collected"), ("4,000+", "children reached through workshops")]
    cells = "".join(f'<div><div class="v" style="font-size:44px;color:{GREEN};line-height:1">{v}</div><div class="b" style="font-size:24px;line-height:1.22;color:{WHITE};margin-top:8px">{t}</div></div>' for v, t in wi)
    inner = label("Welfare impact", 25, ORCHID, "margin-bottom:16px") + f'<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:24px">{cells}</div>'
    s.panel("welfare", M, 670, 1728, 262, inner, pad="28px 40px")
    s.text_pair("welfare", WHITE, "#0B0B0D", 24, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_mosaic(n):
    s = Slide(n); s.chrome("DISCO DIWALI 2025, IN PHOTOS")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1500, "The people who", "make the night.", 76, 56, gap=2)
    s.photo_rect("ph_a", PH["green"], M, 290, 860, 640, "50% 50%", cap="Dancing under the hanging cards")
    s.photo_rect("ph_b", PH["banner"], 1000, 290, 808, 300, "50% 40%", cap="Friends posing at an AquaTerra evening")
    s.photo_rect("ph_c", PH["crowd"], 1000, 620, 808, 310, "50% 45%", cap="Hands up in the crowd")
    s.sticker("st_mask", stk.mask(width=230, plume=False, seed=6), 1660, 190, 9, 11)
    s.sticker("st_sp", (ddt_spark(64, GREEN, "c5"), 64, 64), 940, 250, 0, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- the masquerade, content, timeline
async def s_masq(n):
    s = Slide(n); s.chrome("THE MASQUERADE")
    s.stars([(1760, 40), (40, 600)], 80)
    y = await s.heading(M, 110, 900, "A first for", "Kolkata's student scene.", 76, 56)
    s.add(f'<div class="measure b" data-tag="body" style="position:absolute;left:{M}px;top:{y + 30}px;width:840px;font-size:30px;line-height:1.38;color:{WHITE};z-index:6">'
          f'A masquerade has not been done here before. Guests mask up once they are through the door, the room glows, and every photo is shareable.</div>')
    s.el("body", M, y + 30, 840, 130); s.text_pair("body", WHITE, GROUND, 30, False)
    rows = ["Every guest has a reason to dress up and post", "The theme suits the Skydeck setting", "Curated photo booths around the venue put Rever's space in every shared photo", "It is new, so Rever is part of the first story"]
    inner = label("Why it works for Rever", 26, INK, "margin-bottom:16px")
    inner += "".join(f'<div style="display:flex;gap:20px;align-items:center;margin-bottom:16px">{numdot(i + 1, 48, 25)}<div class="v" style="font-size:27px;line-height:1.12;color:{INK}">{t.upper()}</div></div>' for i, t in enumerate(rows))
    s.slab("why", M, 540, 880, 420, inner, pad="28px 36px")
    s.text_pair("why", INK, SLAB, 27, True)
    s.sticker("st_mask1", stk.mask(width=780, seed=3), 1060, 70, -6)
    s.sticker("st_mask2", stk.mask(width=420, main=GREEN, dark=GD, accent=ORCHID, seed=7, flip=True), 1440, 470, 12, 10)
    s.add(f'<img class="measure" data-tag="ph_photo" src="{photo(PH["group"], 640, (.5, .4))}" '
          f'style="position:absolute;left:1020px;top:480px;width:430px;height:430px;border-radius:50%;border:14px solid {ORCHID};object-fit:cover;z-index:8">')
    s.el("ph_photo", 1020, 480, 430, 430)
    s.pill("cap", 1190, 910, "DISCO DIWALI 2025", 26, align="left")
    s.el("cap", 1190, 910, 400, 55); s.text_pair("cap", INK, CTA, 26, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_content(n):
    s = Slide(n); s.chrome("CONTENT BUILT AROUND REVER")
    s.stars([(1790, 500), (24, 650)], 90)
    await s.heading(M, 104, 1150, "5 to 10 reels.", "Rever's space in every frame.", 76, 56)
    p1 = "Our team shoots the campaign at Rever Skydeck in advance and builds it around your decor. Event reels go out as collab posts, so they also appear on Rever's profile and reach your followers."
    p2 = "We will also produce dedicated reels promoting Rever on its own, with no Disco Diwali branding, for Rever to post on its page. These serve as standalone content for Rever well beyond the event."
    for i, p in enumerate((p1, p2)):
        s.add(f'<div class="measure b" data-tag="p{i}" style="position:absolute;left:{M + i * 880}px;top:360px;width:830px;font-size:28px;line-height:1.38;color:{WHITE};z-index:6">{p}</div>')
        s.el(f"p{i}", M + i * 880, 360, 830, 130); s.text_pair(f"p{i}", WHITE, GROUND, 28, False)
    hl = ["A venue reveal reel opens the campaign", "Masquerade styling matched to Rever's look", "The event menu featured on camera", "Standalone Rever reels for your page", "A reach and views summary after the event"]
    cw = (1728 - 4 * 24) / 5
    for i, t in enumerate(hl):
        inner = (f'<div style="display:flex;flex-direction:column;gap:22px;height:100%">{numdot(i + 1, 64, 34)}<div class="v" style="font-size:26px;line-height:1.1;color:{INK}">{t.upper()}</div></div>')
        s.slab(f"hl{i}", M + i * (cw + 24), 634, cw, 300, inner, pad="28px 26px")
    s.text_pair("hl0", INK, SLAB, 26, True)
    s.add(f'<div class="measure k" data-tag="hlab" style="position:absolute;left:{M}px;top:592px;font-size:24px;color:{ORCHID};z-index:6">HIGHLIGHTS</div>'); s.el("hlab", M, 592, 200, 26)
    s.photo_circle("ph_a", PH["purple"], 1560, 30, 290, (.4, .6), cap=False)
    s.sticker("st_phone", stk.phone(width=170), 1500, 165, -8)
    s.sticker("st_camera", stk.camera(width=240), 1250, 90, -8)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_timeline(n):
    s = Slide(n); s.chrome("CAMPAIGN AND EVENT TIMELINE")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1200, "From sign-off", "to the last song.", 76, 56)
    ph = [("Partnership sign-off", "On agreement", "Menu, deliverables and dates locked"),
          ("Content shoots at Rever", "Multiple days, scheduled with Rever", "Reels and campaign content shot at Rever Skydeck"),
          ("Venue reveal", "Within two weeks of sign-off", "Reveal reel launches the campaign, Rever tagged as venue"),
          ("Ticket sales and promotion", "Through to event day", "Collab reels, standalone Rever reels, WhatsApp community callouts"),
          ("Event day", "10 November 2026", "Disco Diwali 2026 at Rever Skydeck"),
          ("Post-event", "The following week", "Thank-you post, recap, reach summary, asset handover")]
    cols = "grid-template-columns:430px 380px 1fr;column-gap:28px;align-items:center"
    hd = lambda t: f'<div class="k" style="font-size:22px;color:{INK}">{t}</div>'
    grid = f'<div style="display:grid;{cols}">{hd("Phase")}{hd("Timing")}{hd("What happens")}</div>'
    for a, b, c in ph:
        hot = a == "Event day"
        bg = f"background:{ORCHID};" if hot else ""
        grid += (f'<div style="display:grid;{cols};border-top:4px solid {ORCHID};{bg}padding:11px 14px;margin:{"0 -14px" if hot else "0"};border-radius:{16 if hot else 0}px">'
                 f'<div class="v" style="font-size:28px;line-height:1.1;color:{INK}">{a.upper()}</div><div class="b" style="font-size:25px;line-height:1.2;color:{INK}">{b}</div>'
                 f'<div class="b" style="font-size:25px;line-height:1.25;color:{INK}">{c}</div></div>')
    s.slab("tl", M, 280, 1728, 560, label("Campaign timeline", 28, INK, "margin-bottom:10px") + grid, pad="26px 44px")
    s.text_pair("tl", INK, SLAB, 25, False)
    s.pill("callout", M, 868, "THE SOONER WE SIGN OFF, THE MORE OF THE MONTH WE CAN PROMOTE.", 32, align="left")
    s.el("callout", M, 868, 1300, 67); s.text_pair("callout", INK, CTA, 32, True)
    s.sticker("st_clock", stk.clock(width=190), 1620, 70, 8)
    s.sticker("st_record", stk.record(width=230), 1360, 56, -6)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_run(n):
    s = Slide(n); s.chrome("CAMPAIGN AND EVENT TIMELINE  (RUN OF SHOW)")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 900, "Run of show,", "10 November.", 76, 56, gap=4)
    ros = [("9:00 AM", "Setup begins: decor, sound, stage and photo booths"), ("5:00 PM", "Gates open (kitchen live: times set with Rever)"), ("7:00 PM", "DJ set begins"), ("8:00 PM", "Entry closes"), ("9:00 PM", "DJ set ends, guided exit")]
    inner = "".join(f'<div style="display:flex;gap:34px;align-items:center;padding:18px 0;border-top:3px solid #2A2A2E"><div class="v" style="flex:none;width:270px;font-size:54px;line-height:1;color:{ORCHID}">{t}</div>'
                    f'<div class="b" style="font-size:31px;line-height:1.25;color:{WHITE}">{a}</div></div>' for t, a in ros)
    s.add(f'<div class="measure" data-tag="ros" style="position:absolute;left:{M}px;top:310px;width:1000px;z-index:6">{inner}</div>')
    s.el("ros", M, 310, 1000, 560); s.text_pair("ros", WHITE, GROUND, 31, False)
    s.pill("callout", M, 868, "KITCHEN TIMES: SET WITH REVER.", 28, align="left")
    s.el("callout", M, 868, 640, 59); s.text_pair("callout", INK, CTA, 28, True)
    s.photo_rect("ph_a", PH["crowd"], 1180, 230, 628, 690, "50% 50%", cap="The hall, Disco Diwali 2025")
    s.sticker("st_record", stk.record(width=240), 1500, 640, -6, 11)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- a well-run night, in two parts
async def s_crowd(n):
    s = Slide(n); s.chrome("A WELL-RUN NIGHT")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1700, "We run the door and the floor.", "Rever runs the kitchen.", 70, 56)
    cards = [("Entry", "QR ticket check-in and ID verification at the door. Guests show ID first, then the masks go on.", ddt_ticket(150)),
             ("Security", "We bring in bouncers for security at the door.", stk.shield(130)),
             ("Age and alcohol", "Rever sets the age and alcohol rules, in writing, as part of the agreement. We confirm them before anything is announced publicly.", stk.badge(104)),
             ("Photos and consent", "Images of anyone under 18 are used only with guardian consent on file, and Rever approves each image before it goes out.", stk.camera(130))]
    for i, (t, d, st) in enumerate(cards):
        x, y = M + (i % 2) * 888, 300 + (i // 2) * 290
        inner = (f'<div style="display:flex;gap:24px;height:100%"><div style="flex:1"><div class="v" style="font-size:36px;line-height:1.05;color:{INK};margin-bottom:14px;text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.33;color:{INK}">{d}</div></div>'
                 f'<div style="flex:none;width:140px;display:flex;justify-content:center;padding-top:4px">{st[0]}</div></div>')
        s.slab(f"card{i}", x, y, 840, 262, inner, pad="28px 34px")
    s.text_pair("card0", INK, SLAB, 27, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_ask(n):
    s = Slide(n); s.chrome("THE ASKS")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1200, "What we ask of Rever.", "Every ask is open to discussion.", 76, 56)
    ask = [("The venue on 10 November", "Access to Rever Skydeck from the morning, for setup, decor, sound and stage, through to the close of the event", stk.pin(110)),
           ("Food and service", "As Exclusive Food Partner, an event menu designed by Rever and service for 400+ guests, with prices set by Rever and agreed up front", stk.cloche(130)),
           ("A named contact", "One person at Rever we coordinate with", stk.badge(96)),
           ("Promotion cards (optional)", "A return incentive for guests, if Rever would like to include one", ddt_ticket(150))]
    for i, (t, d, st) in enumerate(ask):
        x, y = M + (i % 2) * 888, 310 + (i // 2) * 320
        inner = (f'<div style="display:flex;gap:24px;height:100%"><div style="flex:1"><div class="v" style="font-size:34px;line-height:1.05;color:{INK};margin-bottom:14px;text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.35;color:{INK}">{d}</div></div>'
                 f'<div style="flex:none;width:150px;display:flex;justify-content:center;padding-top:6px">{st[0]}</div></div>')
        s.slab(f"card{i}", x, y, 840, 292, inner, pad="32px 36px")
    s.text_pair("card0", INK, SLAB, 27, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_why(n):
    s = Slide(n); s.chrome("WHY REVER")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1400, "We looked at many venues.", "Rever stood out.", 76, 56)
    rs = [("The food.", "Great food sits at the heart of a good evening, and Rever's is what we want our guests to taste."),
          ("The kitchen.", "One kitchen running one curated menu means consistent quality and short lines."),
          ("A menu that gets people talking.", "Food that gets people talking, posting and coming back."),
          ("A shared goal.", "If Rever wants to build with a younger audience, this is a first introduction, on Rever's terms.")]
    cw, gap = 411, 28
    for i, (t, d) in enumerate(rs):
        inner = (f'<div class="st" style="font-size:150px;line-height:.9;color:{INK};margin-bottom:16px">{i + 1}</div>'
                 f'<div class="v" style="font-size:31px;line-height:1.05;color:{INK};text-transform:uppercase;margin-bottom:14px">{t}</div>'
                 f'<div class="b" style="font-size:27px;line-height:1.34;color:{INK}">{d}</div>')
        s.slab(f"r{i}", M + i * (cw + gap), 320, cw, 490, inner, pad="26px 30px")
    s.text_pair("r0", INK, SLAB, 27, False)
    s.pill("close", M, 846, "WE LOOK FORWARD TO THIS BEING THE FIRST OF MANY EVENINGS TOGETHER.", 38, align="left", w=1728)
    s.el("close", M, 846, 1728, 80); s.text_pair("close", INK, CTA, 38, True)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_exchange(n):
    s = Slide(n); s.chrome("THE EXCHANGE")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1200, "What we both bring.", None, 76)
    items = ["Rever Skydeck on 10 November", "The event menu and service", "One named contact"]
    inner = (label("Rever brings", 30, INK, "margin-bottom:22px") + "".join(
        f'<div style="display:flex;gap:18px;align-items:center;margin-bottom:26px">{numdot(i + 1, 50, 26, WHITE)}<div class="v" style="font-size:31px;line-height:1.1;color:{INK}">{t.upper()}</div></div>' for i, t in enumerate(items)))
    s.slab("brings", M, 250, 480, 540, inner, rot=-1.0, fill=ORCHID, border=12, pad="34px 34px", tilt=True)
    s.text_pair("brings", INK, ORCHID, 31, True)
    rec = [("Exclusivity", "Sole venue and sole food partner for the evening"), ("Audience", "Reach to 400+ guests, mostly high school and first-year college students"),
           ("Visibility", "Logo on all deliverables and core team shirts, on-ground branding, stage mentions"), ("Reputation", "A Google reviews QR code at the event, guests choose whether to post"),
           ("Promotion", "Close to a month across Instagram and our WhatsApp community, business card promotion"),
           ("Content", "5 to 10 planned reels, standalone Rever reels, our photos and videos for Rever to use; under-18s only with guardian consent"), ("Flexibility", "Every element is open to discussion and can be expanded")]
    inner = label("Rever receives", 30, INK, "margin-bottom:10px")
    inner += "".join(f'<div style="display:flex;gap:22px;align-items:center;padding:11px 0;border-top:3px solid {ORCHID}"><div class="v" style="flex:none;width:215px;font-size:26px;color:{INK};text-transform:uppercase">{a}</div>'
                     f'<div class="b" style="font-size:25px;line-height:1.25;color:{INK}">{b}</div></div>' for a, b in rec)
    s.slab("receives", 620, 236, 1204, 604, inner, pad="26px 36px")
    s.text_pair("receives", INK, SLAB, 25, False)
    s.pill("callout", M, 866, "EACH SIDE BRINGS SOMETHING REAL. THE TERMS ARE AGREED IN WRITING.", 32, align="left")
    s.el("callout", M, 866, 1350, 68); s.text_pair("callout", INK, CTA, 32, True)
    s.sticker("st_cloche", stk.cloche(width=180), 270, 640, -6)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_terms(n):
    s = Slide(n); s.chrome("TERMS")
    s.stars([(1760, 40)], 80)
    await s.heading(M, 104, 1500, "Terms to agree together.", "In writing, before anything is announced.", 76, 54)
    items = [("The venue", "Rever sets the terms for the venue on 10 November, including setup from the morning"),
             ("Food and prices", "Rever designs the menu and sets the prices. Pre-order with the ticket, or pay on the night: Rever's call"),
             ("Guest cap and covers", "A guest cap and a minimum number of paid covers, so neither side carries the risk alone"),
             ("Costs", "Who covers decor, sound, stage, banners and menu boards, settled up front"),
             ("Approvals", "Rever approves every post, reel, banner, ticket and broadcast that carries its name before it goes out"),
             ("Money", "Any fee, revenue share and ticket price on one page, with tax treatment confirmed. We share our registration documents"),
             ("Promotion cards", "Optional: a return incentive on terms Rever sets"),
             ("Timing", "The sooner we sign off, the more of the month we can use for promotion")]
    cw = 840
    for i, (t, d) in enumerate(items):
        x, y = M + (i % 2) * 888, 290 + (i // 2) * 164
        inner = (f'<div style="display:flex;gap:22px;align-items:center;height:100%">{numdot(i + 1, 56, 28)}<div><div class="v" style="font-size:30px;line-height:1.05;color:{INK};text-transform:uppercase">{t}</div>'
                 f'<div class="b" style="font-size:24px;line-height:1.26;color:{INK};margin-top:6px">{d}</div></div></div>')
        s.slab(f"term{i}", x, y, cw, 148, inner, pad="10px 28px", border=8)
    s.text_pair("term0", INK, SLAB, 24, False)
    await s.render(f"{OUT}/slide_{n:02d}.png")


async def s_next(n):
    s = Slide(n); s.chrome("NEXT STEPS")
    s.stars([(1760, 560)], 90)
    await s.heading(M, 104, 1180, "Let's make this Diwali", "happen at Rever.", 76, 64)
    steps = ["A short meeting to align on the menu and deliverables", "A one-page agreement", "Campaign launch"]
    sx = M
    for i, (t, sw) in enumerate(zip(steps, (440, 300, 300))):
        inner = f'<div style="display:flex;flex-direction:column;gap:14px">{numdot(i + 1, 56, 30)}<div class="v" style="font-size:28px;line-height:1.1;color:{INK}">{t.upper()}</div></div>'
        s.slab(f"step{i}", sx, 330, sw, 250, inner, rot=(-1.2, .9, -.8)[i], pad="22px 26px", tilt=False)
        sx += sw + 20
    s.text_pair("step0", INK, SLAB, 28, True)
    inner = (label("Contact", 24, INK, "margin-bottom:8px") + f'<div class="v" style="font-size:54px;line-height:1.1;color:{INK}">PRATYAKSH SINGHANIA</div>'
             f'<div class="k" style="font-size:30px;color:{INK};margin:8px 0 18px">Team AquaTerra&nbsp;&nbsp;|&nbsp;&nbsp;+91 98305 54654</div>'
             f'<div class="b" style="font-size:30px;line-height:1.35;color:{INK}">Instagram: <b>@ngo.aquaterra</b> | <b>@aquaterra.live</b><br>ngoaquaterra.com</div>')
    s.slab("contact", M, 616, 1060, 316, inner, pad="26px 40px")
    s.text_pair("contact", INK, SLAB, 30, False)
    s.add(f'<div class="measure" data-tag="rever_logo" style="position:absolute;left:1290px;top:96px;width:440px;height:440px;border-radius:50%;background:#fff;border:16px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8">'
          f'<img src="{REVER}" style="width:320px"></div>')
    s.el("rever_logo", 1290, 96, 440, 440)
    s.add(f'<div class="measure" data-tag="qr" style="position:absolute;left:1350px;top:590px;width:320px;height:320px;border-radius:36px;background:#fff;border:14px solid {ORCHID};display:flex;align-items:center;justify-content:center;z-index:8;transform:rotate(3deg)">'
          f'<img src="{QR}" style="width:250px;height:250px"></div>')
    s.el("qr", 1350, 590, 320, 320)
    s.add(f'<div class="measure k" data-tag="qrcap" style="position:absolute;left:1330px;top:922px;width:360px;text-align:center;font-size:21px;color:{WHITE};z-index:9">SCAN FOR @NGO.AQUATERRA</div>'); s.el("qrcap", 1330, 922, 360, 24); s.text_pair("qrcap", WHITE, GROUND, 21, False)
    s.cord(1830, 0, 280); s.ball("st_ball", 150, 1755, 270, 0)
    s.sticker("st_mask", stk.mask(width=210, plume=False, seed=5), 1690, 700, -10)
    s.sticker("st_diya", ddt_diya(150), 1236, 790, 6, 10)
    s.sticker("st_sp", (ddt_spark(60, GREEN, "c14"), 60, 60), 1270, 560, 0, 7)
    await s.render(f"{OUT}/slide_{n:02d}.png")


# ---------------------------------------------------------------- the running order
ORDER = [
    s_cover,
    P("blue", "This is\nthe energy.", "Crowd at Disco Diwali 2025 when the DJ entered", "50% 40%", stickers=[(stk.mask(width=260, plume=False, seed=2), 1560, 110, 8)]),
    s_brief,
    s_location,
    P("arrivals", "The entrance\nis the first photo.", "Guests arriving on the red carpet at Disco Diwali 2025", "50% 55%", split=True, tsize=92,
      stickers=[(stk.camera(width=250), 640, 790, -8)]),
    s_vis1,
    s_vis2,
    P("greenp", "A dance floor\nthat does not sit.", "Dance floor at Disco Diwali 2025", "50% 38%", split=True, tsize=92,
      stickers=[(stk.record(width=240), 680, 800, 6)]),
    s_aud1,
    s_aud2,
    P("friends", "Friend groups,\nfront and centre.", "Friends at an AquaTerra evening", "50% 100%", label_="AQUATERRA EVENTS", tsize=104),
    s_touch,
    s_hist1,
    s_hist2,
    s_mosaic,
    s_masq,
    s_content,
    s_timeline,
    s_run,
    s_crowd,
    s_ask,
    s_why,
    s_exchange,
    s_terms,
    s_next,
]
TOTAL = len(ORDER)


async def main(which):
    global TOTAL
    TOTAL = len(ORDER)
    os.makedirs(OUT, exist_ok=True)
    async with B.session(scale=1):
        for i in which:
            await ORDER[i - 1](i)
            print("slide", i, "done")
    if len(which) == TOTAL:
        pages = [Image.open(f"{OUT}/slide_{n:02d}.png").convert("RGB") for n in range(1, TOTAL + 1)]
        pages[0].save(f"{OUT}/rever_disco_diwali_deck.pdf", save_all=True, append_images=pages[1:], resolution=96, quality=92)
        print("pdf written", TOTAL, "pages")


if __name__ == "__main__":
    which = [int(a) for a in sys.argv[1:]] or list(range(1, len(ORDER) + 1))
    asyncio.run(main(which))
