"""TerraThon x Disco Diwali: PINBOARD TEASER CAROUSEL (Workflow C bespoke build, TerraThon format).

Brief (user, 2026-10-10): "make a carousel teaser post for disco diwali using this idea [a Books & Moods
release-schedule pinboard: tilted polaroids, a string pulled taut between pushpins, dates in the captions,
tape, handwritten asides, doodles] using the terrathon branding".

MECHANISM (the part that must not be dropped): ONE orchid string that runs pin to pin ACROSS the whole
carousel. Each slide renders a window onto the same global polyline, so the string leaves slide N at the
exact y where it enters slide N+1. You follow the string by swiping, and it ends on the date polaroid.

Adaptations (CLAUDE.md sec 2 rule 4):
  * Reference is light grey paper; this is TerraThon's black ground, so polaroids are the slab white with the
    slab's orchid border, and the string/pins take the orchid (the reference's purple).
  * The reference's book covers are real photos of last edition (dd_photos) and kit-style stickers (disco ball,
    diya, ticket from tt_dd_tickets.py). Captions that were release dates become CLUE numbers; the LAST polaroid
    carries the date, as in the reference.
  * Handwriting is not in the TerraThon kit, so asides are NeutralFace 400 lowercase, rotated.
  * Copy is teaser-only: no venue, no price, no on-sale claim (none supplied / ticket stall ran at the Mini-Fete).
    Date is 10th November (user, 2026-10-01); year NOT printed (assumed 2026 elsewhere).
  * Title spelled DISCOO DIWAALI so StretchPro's doubled-letter ligatures fire (CLAUDE.md / TERRATHON.md sec 3.3).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_teaser.py
"""
import asyncio, base64, importlib.util, io, math, os, random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def _load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


dd = _load("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py"))
tt = dd.tt
core, B, W, H = tt.core, tt.B, tt.W, tt.H
GROUND, ORCHID, HALO, SLAB, INK, WHITE, CTA_FILL = dd.GROUND, dd.ORCHID, dd.HALO, dd.SLAB, dd.INK, dd.WHITE, dd.CTA_FILL
GREEN, BLUE, PURPLE = dd.GREEN, dd.BLUE, dd.PURPLE
N = 5

# ---- global string: pin positions in GLOBAL x (slide k spans k*W .. (k+1)*W) -----------------------------------
PHOTOS = {k: f"engine/assets/terrathon/dd_photos/{k}.jpg" for k in ("decor", "dance", "group")}


def photo_uri(key, maxw=900):
    im = Image.open(PHOTOS[key]).convert("RGB")
    im.thumbnail((maxw, maxw))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def rot_bbox(cx, cy, w, h, deg):
    a = math.radians(abs(deg)); bw = w * math.cos(a) + h * math.sin(a); bh = w * math.sin(a) + h * math.cos(a)
    return cx - bw / 2, cy - bh / 2, bw, bh


def polaroid(k, cx, cy, w, h, rot, inner_html, caption, tag, cap_px=36, z=3, pin=True):
    """A tilted polaroid. (cx, cy) is its centre in SLIDE coords. Returns (html, bbox, pin_global_xy)."""
    pad = 22; cap_h = 92
    px_, py_ = cx - w / 2, cy - h / 2
    card = (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{px_}px;top:{py_}px;width:{w}px;height:{h}px;z-index:{z};'
            f'transform:rotate({rot}deg);background:{SLAB};border:6px solid {ORCHID};border-radius:14px;box-sizing:border-box;'
            f'box-shadow:0 18px 0 -6px rgba(222,104,240,.0),0 16px 26px rgba(0,0,0,.55)">'
            f'<div style="position:absolute;left:{pad - 6}px;top:{pad - 6}px;width:{w - 2 * pad}px;height:{h - cap_h - pad + 6 - 6}px;overflow:hidden;'
            f'background:#111;border-radius:4px">{inner_html}</div>'
            f'<div style="position:absolute;left:0;right:0;bottom:12px;text-align:center;font-family:var(--d);font-weight:400;'
            f'font-size:{cap_px}px;line-height:1;color:{INK};white-space:nowrap">{caption}</div></div>')
    # pin sits at the top centre of the card, after rotation
    a = math.radians(rot); dy = -h / 2 + 30
    pcx, pcy = cx - dy * math.sin(a) * -1 * -1 * 0 + (-dy * -math.sin(a)) * 0, cy
    pcx = cx + (0 * math.cos(a) - dy * math.sin(a)); pcy = cy + (0 * math.sin(a) + dy * math.cos(a))
    return card, rot_bbox(cx, cy, w, h, rot), (k * W + pcx, pcy)


def pin_html(x, y, z=6, size=40):
    return (f'<div class="measure" data-tag="pin" style="position:absolute;left:{x - size / 2}px;top:{y - size / 2}px;width:{size}px;height:{size}px;'
            f'border-radius:50%;z-index:{z};background:radial-gradient(circle at 34% 30%,#FFE3FF 0 9%,#F08CFF 24%,{ORCHID} 52%,#8B2FA3 100%);'
            f'box-shadow:0 8px 10px rgba(0,0,0,.55),inset 0 -4px 6px rgba(80,0,100,.45)"></div>')


def tape(x, y, w, h, rot, z=7):
    """A strip of cream masking tape with torn ends, holding a polaroid corner down."""
    return (f'<div class="measure" data-tag="tape" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z};transform:rotate({rot}deg);'
            f'background:linear-gradient(180deg,rgba(243,236,222,.96),rgba(228,219,200,.96));'
            f'clip-path:polygon(0 8%,4% 0,8% 10%,12% 0,100% 0,96% 22%,100% 40%,96% 62%,100% 100%,10% 100%,6% 88%,3% 100%,0 80%,3% 55%,0 32%)"></div>')


def note(x, y, text, rot=-4, size=40, z=6, w=None, tag="note", align="left"):
    ws = f"width:{w}px;" if w else "white-space:nowrap;"
    return (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;{ws}z-index:{z};transform:rotate({rot}deg);'
            f'font-family:var(--d);font-weight:400;font-size:{size}px;line-height:1.12;color:{WHITE};text-align:{align}">{text}</div>')


def squiggle(x, y, w, col, z=5, sw=7, rot=0, tag="squig"):
    """A hand-drawn loop-de-loop, like the reference's black scribble."""
    d = "M4,60 C30,10 70,10 60,50 C50,86 20,60 46,32 C72,4 110,30 100,56 C92,78 70,64 92,40 C112,18 150,40 150,60 C150,72 138,76 130,66"
    return (f'<svg class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;z-index:{z};transform:rotate({rot}deg)" width="{w}" height="{w * .55}" viewBox="0 0 160 90" overflow="visible">'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def hearts(x, y, s, col, z=5):
    h = lambda cx, cy, r: (f'<path transform="translate({cx},{cy}) scale({r})" d="M0,6 C-10,-2 -12,-12 -5,-13 C-2,-13 0,-10 0,-8 C0,-10 2,-13 5,-13 C12,-12 10,-2 0,6Z" fill="{col}"/>')
    return (f'<svg class="measure" data-tag="hearts" style="position:absolute;left:{x}px;top:{y}px;z-index:{z}" width="{s}" height="{s * .8}" viewBox="0 0 60 48" overflow="visible">'
            f'{h(18, 22, 1.5)}{h(44, 30, 1.0)}</svg>')


def shuriken(label, x, y, z=5, k=tt.NATIVE * 0.67):
    im, src = tt.crop_to_alpha("shuriken.png")
    w, h = round(im.width * k), round(im.height * k)
    return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'), (label, x, y, w, h)


async def build_all(outdir):
    # ---- measure type once ----
    m = await B.measure_text([
        dict(text="DISCOO DIWAALI", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text="10TH NOVEMBER", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text="10TH", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text="THE STRING ENDS HERE", font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em"),
        dict(text="CLUES INSIDE", font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em"),
        dict(text="SWIPE", font="d", size=40, weight=900),
        dict(text="FOLLOW @NGO.AQUATERRA", font="d", size=40, weight=900),
    ], extra_css=tt.FONT_CSS)
    tw = [r["text_w"] for r in m]
    fit = lambda i, target, base=100: base * target / tw[i]
    print("TW", tw); title_px = 63; nov_px = 63; tenth_px = fit(2, 330)
    sub1_px = min(86, fit(4, 520)); sub2_px = min(86, fit(3, 640))
    cta_w = {"SWIPE": tw[5] * .8 + 70, "FOLLOW": tw[6] * .8 + 70}

    # ---- pins (global) decided with the polaroids ----
    slides_els = [[] for _ in range(N)]
    parts = [[] for _ in range(N)]
    pins = []

    def add(k, label, html, bbox=None):
        parts[k].append(html)
        if bbox is not None:
            slides_els[k].append((label, *bbox))

    # sticker helpers
    box = lambda x, y, svg, z, rot=0, tag="": (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;z-index:{z};transform:rotate({rot}deg)">{svg}</div>')

    # ================= S1 COVER =================
    k = 0
    decor = f'<div style="position:absolute;inset:0;background:url({photo_uri("decor")}) 36% 50%/cover"></div>'
    c, bb, p = polaroid(k, 300, 520, 480, 590, -6, decor, "clue 00: this one", "pol0", 40)
    add(k, "pol0", c, bb); pins.append(p)
    ball, bh = dd.disco_ball(380, "dbf1")
    add(k, "ball", box(660, 200, ball, 4, 0, "ball"), (660, 200, 380, bh))
    sp, spb = dd.spark(70, GREEN, "spk1", 3), None
    add(k, "sp1", box(560, 330, sp, 6, 0, "sp1"), (560, 330, 70, 70))
    add(k, "note0", note(600, 660, "pin it.<br>string it.<br>feel it.", -5, 46, w=300, tag="note0"), (600, 660, 300, 150))

    # ================= S2 CLUE 01: the floor =================
    k = 1
    dance = f'<div style="position:absolute;inset:0;background:url({photo_uri("dance")}) 52% 50%/cover"></div>'
    c, bb, p = polaroid(k, 620, 640, 600, 700, 5, dance, "clue 01", "pol1", 44)
    add(k, "pol1", c, bb); pins.append(p)
    add(k, "note1", note(60, 1000, "somebody<br>was not ready<br>for this", -5, 42, w=300, tag="note1"), (60, 1000, 300, 170))
    sp = dd.spark(90, PURPLE, "spk2", 8)
    add(k, "sp2", box(930, 330, sp, 6, 0, "sp2"), (930, 330, 90, 90))
    add(k, "hearts2", hearts(780, 1050, 120, WHITE), (780, 1050, 120, 96))

    # ================= S3 CLUE 02: diya + ticket =================
    k = 2
    dya, dh = dd.diya(380, "dyf3")
    plate = (f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,#2a0f33 0,#0b0612 70%)"></div>'
             f'<div style="position:absolute;left:{(556 - 380) / 2 - 10}px;top:{(558 - dh) / 2 + 6}px">{dya}</div>')
    c, bb, p = polaroid(k, 460, 660, 600, 700, -4, plate, "clue 02", "pol2", 44)
    add(k, "pol2", c, bb); pins.append(p)
    tk, tkh = dd.ticket(360, "tkf3")
    add(k, "ticket3", box(600, 900, tk, 8, 10, "ticket3"), (590, 880, 400, 300))
    add(k, "tape3", tape(660, 350, 150, 50, 38), (660, 340, 150, 130))
    add(k, "note3", note(790, 640, "full<br>sparkle,<br>zero<br>chill", 6, 44, w=260, tag="note3"), (790, 640, 260, 220))

    # ================= S3b CLUE 03: the crew =================
    k = 3
    group = f'<div style="position:absolute;inset:0;background:url({photo_uri("group")}) 62% 50%/cover"></div>'
    c, bb, p = polaroid(k, 600, 640, 600, 700, 4, group, "clue 03", "pol3", 44)
    add(k, "pol3", c, bb); pins.append(p)
    add(k, "note4", note(60, 1000, "your crew<br>is already<br>typing...", -5, 44, w=330, tag="note4"), (60, 1000, 330, 190))
    sp = dd.spark(80, HALO, "spk4", 14)
    add(k, "sp4", box(940, 1000, sp, 6, 0, "sp4"), (940, 1000, 80, 80))
    add(k, "squig4", squiggle(480, 1060, 190, ORCHID, tag="squig4"), (480, 1060, 190, 104))

    # ================= S5 REVEAL: the date =================
    k = 4
    ball2, b2h = dd.disco_ball(440, "dbf5")
    plate5 = (f'<div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 36%,#2a0f33 0,#0b0612 72%)"></div>'
              f'<div style="position:absolute;left:{(540 - 440) / 2 - 2}px;top:{(450 - b2h) / 2 + 52}px;overflow:hidden">{ball2}</div>')
    c, bb, p = polaroid(k, 540, 560, 540, 640, -4, plate5, "save the date", "pol4", 46)
    add(k, "pol4", c, bb); pins.append(p)

    # ---- the string: global polyline through the pins ----
    pts = pins
    for kk in range(N):
        x0 = kk * W
        d = "M" + " L".join(f"{x - x0:.1f},{y:.1f}" for x, y in pts)
        parts[kk].append(f'<svg class="measure" data-tag="string" style="position:absolute;left:0;top:0;z-index:4;overflow:visible" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                         f'<path d="{d}" fill="none" stroke="{ORCHID}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
        for gx, gy in pts:
            if x0 - 40 <= gx <= x0 + W + 40:
                parts[kk].append(pin_html(gx - x0, gy))

    # ---- shared chrome per slide: header, logo, CTA, stars ----
    HB = f'position:absolute;left:64px;white-space:nowrap;line-height:1;font-family:var(--d);color:{WHITE};z-index:9'
    headers = [
        ("SWIPE TO CONNECT", "THE DOTS", 400),
        ("CLUE 01", "DANCING SHOES ON", 400),
        ("CLUE 02", "DIYAS MEET DISCO", 400),
        ("CLUE 03", "BRING YOUR CREW", 400),
        ("CLUE 04: THE DATE", "STRING ENDS HERE", 400),
    ]
    star_pos = [[(960, 40), (960, 770)], [(30, 380), (960, 1110)], [(960, 330), (24, 1090)], [(960, 380), (830, 1150)], [(70, 400), (950, 520)]]

    for k in range(N):
        a, b2, _ = headers[k]
        a_px, b_px = 52, (74 if k == 4 else 86)
        mm_w = {}
        parts[k].append(f'<div class="measure" data-tag="h1" style="{HB};top:56px;font-weight:400;font-size:{a_px}px">{a}</div>'
                        f'<div class="measure" data-tag="h2" style="{HB};top:{56 + a_px + 10}px;font-weight:900;font-size:{b_px}px">{b2}</div>')
        slides_els[k] += [("h1", 64, 56, 520, a_px * .8), ("h2", 64, 56 + a_px + 10, 900, b_px * .8)]
        for i, (sx, sy) in enumerate(star_pos[k]):
            html, e = shuriken(f"star{i}", sx, sy)
            parts[k].append(html); slides_els[k].append(e)

    # ---- S1 slab (title) ----
    sx, sy, sw, sh = 78, 905, 924, 250
    slab = (f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;transform:rotate(-1.3deg);'
            f'background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;box-sizing:border-box">'
            f'<div style="position:absolute;left:0;width:100%;text-align:center;top:34px;font-family:StretchPro;color:{INK};'
            f'-webkit-text-stroke:{tt.ST_STROKE * title_px}px {INK};letter-spacing:-0.02em;font-feature-settings:{tt.ST_FEAT};font-size:{title_px}px;line-height:1;white-space:nowrap">DISCOO DIWALI</div>'
            f'<div style="position:absolute;left:0;width:100%;text-align:center;top:{34 + title_px * .86 + 26}px;font-family:SigmarOne;color:{INK};'
            f'-webkit-text-stroke:{tt.SG_STROKE * sub1_px}px {INK};letter-spacing:{tt.SG_LS}em;font-size:{sub1_px}px;line-height:1;white-space:nowrap">CLUES INSIDE</div></div>')
    parts[0].append(slab); slides_els[0].append(("slab", sx - 6, sy - 10, sw + 12, sh + 20))

    # ---- S5 slab (date) ----
    sx, sy, sw, sh = 78, 965, 924, 215
    d10 = (f'<div style="position:absolute;left:0;width:100%;text-align:center;top:22px;font-family:StretchPro;color:{INK};'
           f'-webkit-text-stroke:{tt.ST_STROKE * nov_px}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{nov_px}px;line-height:1;white-space:nowrap">10TH NOVEMBER</div>')
    # one line "10TH NOVEMBER" fitted to the slab; measured width of the two words ~ tw[2]+tw[1] plus a space
    parts[4].append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;transform:rotate(-1.3deg);'
                    f'background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;box-sizing:border-box">__DATE__'
                    f'<div style="position:absolute;left:0;width:100%;text-align:center;top:__SUBTOP__px;font-family:SigmarOne;color:{INK};'
                    f'-webkit-text-stroke:{tt.SG_STROKE * sub2_px}px {INK};letter-spacing:{tt.SG_LS}em;font-size:{sub2_px}px;line-height:1;white-space:nowrap">DISCO DIWALI</div></div>')
    slides_els[4].append(("slab", sx - 6, sy - 10, sw + 12, sh + 20))
    s5_date = d10
    s5_sub = 22 + nov_px * .86 + 22

    # ---- footer ----
    for k in range(N):
        parts[k].append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:1252px;height:56px;z-index:9">')
        slides_els[k].append(("logo", 27, 1252, 320, 56))
        lab = "FOLLOW @NGO.AQUATERRA" if k == N - 1 else "SWIPE"
        cw = cta_w["FOLLOW" if k == N - 1 else "SWIPE"] * (40 / 40)
        ch = 68
        cx = W - cw - 22
        parts[k].append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:1244px;width:{cw}px;height:{ch}px;border:6px solid {ORCHID};border-radius:999px;'
                        f'background:{CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:30px;color:{INK};'
                        f'white-space:nowrap">{lab}{" &rsaquo;" if k < N - 1 else ""}</div>')
        slides_els[k].append(("cta", cx, 1244, cw, ch))

    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    ground = (f'<div style="position:absolute;inset:0;background:{GROUND}"></div><svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>')

    os.makedirs(outdir, exist_ok=True)
    text_pairs = [("h", WHITE, GROUND, 52, False), ("note", WHITE, GROUND, 40, False), ("cap", INK, SLAB, 36, False), ("cta", INK, CTA_FILL, 30, True)]
    for k in range(N):
        body = "".join(parts[k]).replace("__DATE__", s5_date).replace("__SUBTOP__", f"{s5_sub:.1f}")
        html = B.page(W, H, GROUND, f"<style>{tt.FONT_CSS}</style>" + ground + body, grain=False)
        els = slides_els[k]
        await B.render(html, f"{outdir}/dd_teaser_{k + 1:02d}.png", W, H, elements=els, text_pairs=text_pairs, containers=("slab",),
                       page_bg=GROUND, expect_hero=False, margin=12,
                       bleed_tags=("string", "pin", "ball", "ticket3", "tape", "star0", "star1"),
                       collision_ignore={("pol0", "ball"), ("pol0", "note0"), ("ball", "note0"),
                                         ("ticket3", "pol2"), ("tape3", "pol2"), ("note3", "pol2"), ("tape3", "note3"), ("ticket3", "slab"),
                                         ("note1", "pol1"), ("hearts2", "pol1"), ("sp2", "pol1"),
                                         ("note4", "pol3"), ("sp4", "pol3"), ("squig4", "pol3"), ("pol4", "slab"),
                                         ("pol0", "slab"), ("star0", "h2"), ("star1", "pol3")})
        print("slide", k + 1, "ok")


async def main():
    async with B.session():
        await build_all(os.environ.get("TT_OUT", "out/versions/terrathon_dd_teaser"))
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
