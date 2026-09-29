"""TerraThon / Wicket Wars (cricket), Workflow B recreation (converged at v4, score 0.039). Reference: the user-supplied 1620x2025 original.

Reference: training_samples/terrathon/wicket_wars_bio.png (4:5). Built on the feed
canvas 1080x1350 at scale S = 0.675, so every reference coordinate below is (ref px * S).

Adaptations (recorded per CLAUDE.md sec 2 rule 4):
  * Type is NeutralFace throughout (user ruling 2026-09-29): regular (400) for labels, bold (900)
    for values. That IS the reference's weight-pairing rule. The subtitle face is NeutralFace too.
  * Hero and star are the user's real sticker files (engine/assets/terrathon), aligned by alpha box.
    The hero's lower edge is hidden by the slab in the reference, so the cutout ends there.
  * The calendar glyph is DRAWN, with no date on it. The reference uses an emoji whose artwork
    reads "JUL 17" beside "3RD & 4TH OCTOBER".
  * Palette is TerraThon's own (user ruling), not core.ACCENTS.
"""
import asyncio, base64, json, os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core"); B = load("build")

W, H = core.SIZES["feed"]
S = W / 1600.0
ASSET = "engine/assets/terrathon"

# --- TerraThon tokens (sampled from the reference pixels) ---
GROUND = "#000000"
ORCHID = "#DE68F0"
CREAM_HALO = "#F3ECDE"
SLAB = "#F9F9F9"
INK = "#0A0A0A"
WHITE = "#F5F5F5"


def px(v):
    return round(v * S, 1)


def b64(name):
    with open(f"{ASSET}/{name}", "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


elements = []


def el(label, x, y, w, h):
    elements.append((label, x, y, w, h))


import numpy as _np
from PIL import Image as _Im


def sticker_img(name, label, x0, y0, tw, z, rot=0):
    """Place a REAL sticker so its visible (alpha) box lands at ref (x0,y0) with width tw (ref px, 1600 space).
    The PNG is cropped to its alpha box first, so the element the browser draws IS the box we declare."""
    import io
    im = _Im.open(f"{ASSET}/{name}").convert("RGBA")
    al = _np.array(im)[..., 3]
    ys, xs = _np.where(al > 20)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    buf = io.BytesIO(); im.save(buf, "PNG")
    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    k = tw / im.width
    x, y, w, h = px(x0), px(y0), px(tw), px(im.height * k)
    el(label, x, y, w, h)
    return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{h}px;z-index:{z}">')


def star(x0, y0, label, z=5):
    return sticker_img("shuriken.png", label, x0, y0, 150, z)


# ---------- speckle ground (white flecks on black, like the reference) ----------
import random
rnd = random.Random(7)
specks = "".join(
    f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
    f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
ground = (f'<div style="position:absolute;inset:0;background:{GROUND}"></div>'
          f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>')

# ---------- header: prize block ----------
CX = px(800)
hdr = (
    f'<div class="measure" data-tag="pp_label" style="position:absolute;left:{px(420)}px;width:{px(760)}px;top:{px(104)}px;text-align:center;'
    f'font-family:var(--d);font-weight:400;font-size:{px(113.5)}px;line-height:1;color:{WHITE};z-index:6">PRIZE POOL:</div>'
    f'<div class="measure" data-tag="pp_value" style="position:absolute;left:{px(420)}px;width:{px(760)}px;top:{px(212)}px;text-align:center;'
    f'font-family:var(--d);font-weight:900;font-size:{px(113.5)}px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">'
    f'<span style="font-family:\'Noto Color Emoji\';font-weight:400;font-size:{px(84)}px;vertical-align:.02em;margin-right:{px(12)}px">💸</span>RS. 7,500</div>'
    f'<div class="measure" data-tag="winner" style="position:absolute;left:{px(420)}px;width:{px(760)}px;top:{px(338)}px;text-align:center;'
    f'font-family:var(--d);font-weight:400;font-size:{px(50)}px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">'
    f'WINNER<span style="font-family:\'Noto Color Emoji\';font-size:{px(40)}px">🥇</span>: <b style="font-weight:900">RS.4,500</b></div>'
    f'<div class="measure" data-tag="runners" style="position:absolute;left:{px(420)}px;width:{px(760)}px;top:{px(392)}px;text-align:center;'
    f'font-family:var(--d);font-weight:400;font-size:{px(50)}px;line-height:1;color:{WHITE};z-index:6;white-space:nowrap">'
    f'RUNNERS UP<span style="font-family:\'Noto Color Emoji\';font-size:{px(40)}px">🥈</span>: <b style="font-weight:900">RS.3,000</b></div>'
)
el("pp_label", px(420), px(104), px(760), px(103))
el("pp_value", px(420), px(212), px(760), px(103))
el("winner", px(420), px(338), px(760), px(50))
el("runners", px(420), px(392), px(760), px(50))

# ---------- TERRATHON pill (top right) ----------
pill_x, pill_y, pill_w, pill_h = px(1198), px(78), px(377), px(120)
el("fest_pill", pill_x, pill_y, pill_w, pill_h)
fest = (f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{pill_x}px;top:{pill_y}px;width:{pill_w}px;height:{pill_h}px;'
        f'border:{px(9)}px solid {ORCHID};border-radius:999px;background:#fff;display:flex;align-items:center;justify-content:center;z-index:7;'
        f'font-family:var(--d);font-weight:900;font-size:{px(46)}px;color:{INK}">TERRATHON</div>')

# ---------- hero + stars ----------
hero = sticker_img("cricket_set.png", "hero", 432, 484, 747, 3)
stars = (star(1346, 257, "star_tr") + star(163, 484, "star_ul") + star(1343, 813, "star_rm") + star(28, 1010, "star_ll", z=9))

# ---------- slab (white, orchid border, tilted -1.25deg) with title ----------
SL_X, SL_Y, SL_W, SL_H, SL_ROT = px(70), px(1095), px(1472), px(506), -1.25
el("slab", SL_X - px(6), SL_Y - px(10), SL_W + px(12), SL_H + px(20))
BORDER = px(28)
slab = (
    f'<div class="measure" data-tag="slab" style="position:absolute;left:{SL_X}px;top:{SL_Y}px;width:{SL_W}px;height:{SL_H}px;'
    f'transform:rotate({SL_ROT}deg);transform-origin:50% 50%;background:{SLAB};border:{BORDER}px solid {ORCHID};'
    f'border-radius:{px(70)}px;z-index:8">'
    # title: plain NeutralFace Bold, NO stretched glyphs (user ruling 2026-09-29)
    f'<div style="position:absolute;left:{px(30)}px;top:{px(48)}px;font-family:var(--d);font-weight:900;color:{INK};'
    f'font-size:{px(156)}px;line-height:.9;white-space:nowrap;letter-spacing:-.01em">'
    f'<div>WICKET</div><div>WARS</div></div>'
    f'<div style="position:absolute;left:{px(34)}px;top:{px(350)}px;font-family:var(--d);font-weight:900;color:{INK};'
    f'font-size:{px(88)}px;line-height:1;white-space:nowrap">A CRICKET TOURNAMENT</div>'
    f'</div>'
)

# ---------- info block ----------
LB = f'font-family:var(--d);font-weight:400;font-size:{px(49)}px;line-height:1;color:{WHITE};white-space:nowrap'
cal = (f'<svg class="measure" data-tag="cal" style="position:absolute;left:{px(250)}px;top:{px(1648)}px;z-index:6" '
       f'width="{px(84)}" height="{px(84)}" viewBox="0 0 84 84"><rect x="6" y="14" width="72" height="64" rx="10" fill="{CREAM_HALO}"/>'
       f'<rect x="6" y="14" width="72" height="20" rx="8" fill="{ORCHID}"/>'
       f'<rect x="20" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/><rect x="56" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/>'
       f'<rect x="18" y="44" width="14" height="12" rx="3" fill="{INK}"/><rect x="38" y="44" width="14" height="12" rx="3" fill="{INK}"/>'
       f'<rect x="58" y="44" width="10" height="12" rx="3" fill="{INK}"/></svg>')
el("cal", px(250), px(1648), px(84), px(84))
pin = (f'<span class="measure" data-tag="pin" style="position:absolute;left:{px(1088)}px;top:{px(1646)}px;font-family:\'Noto Color Emoji\';'
       f'font-size:{px(62)}px;line-height:1;z-index:6">📍</span>')
el("pin", px(1085), px(1642), px(80), px(90))
info = (
    f'<div class="measure" data-tag="date" style="position:absolute;left:{px(340)}px;top:{px(1671)}px;{LB}">3RD &amp; 4TH OCTOBER, 2026</div>'
    f'<div class="measure" data-tag="venue" style="position:absolute;left:{px(1150)}px;top:{px(1671)}px;{LB}">TURF XL</div>'
    f'<div class="measure" data-tag="fee1" style="position:absolute;left:{px(400)}px;width:{px(800)}px;text-align:center;top:{px(1751)}px;{LB}">'
    f'PARTICIPATION FEE <b style="font-weight:900">RS. 2,100</b></div>'
    f'<div class="measure" data-tag="fee2" style="position:absolute;left:{px(400)}px;width:{px(800)}px;text-align:center;top:{px(1803)}px;{LB}">'
    f'FOR A <b style="font-weight:900">TEAM OF 8</b></div>'
)
el("date", px(342), px(1680), px(675), px(45)); el("venue", px(1150), px(1680), px(210), px(45))
el("fee1", px(400), px(1751), px(800), px(52)); el("fee2", px(400), px(1803), px(800), px(52))

# ---------- footer: logo + CTA pill ----------
lg_x, lg_y, lg_h = px(40), px(1888), px(83)
logo = f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{lg_x}px;top:{lg_y}px;height:{lg_h}px;z-index:9">'
el("logo", lg_x, lg_y, px(475), lg_h)
cta_x, cta_y, cta_w, cta_h = px(1068), px(1880), px(500), px(100)
el("cta", cta_x, cta_y, cta_w, cta_h)
cta = (f'<div class="measure" data-tag="cta" style="position:absolute;left:{cta_x}px;top:{cta_y}px;width:{cta_w}px;height:{cta_h}px;'
       f'border:{px(9)}px solid {ORCHID};border-radius:999px;background:#F5EEE1;display:flex;align-items:center;justify-content:center;z-index:9;'
       f'font-family:var(--d);font-weight:900;font-size:{px(44)}px;color:{INK}">LINK IN THE BIO</div>')

inner = ground + hdr + fest + hero + stars + slab + cal + pin + info + logo + cta
html = B.page(W, H, GROUND, inner, grain=False)

text_pairs = [("prize", WHITE, GROUND, 96, True), ("info", WHITE, GROUND, 40, False),
              ("title", INK, SLAB, 100, True), ("cta", INK, "#F5EEE1", 34, True), ("pill", INK, "#FFFFFF", 36, True)]


async def main():
    slug = "terrathon_wicket_wars"
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    out = f"out/versions/{slug}/v4.png"
    await B.render(html, out, W, H, elements=elements, text_pairs=text_pairs,
                   containers=("slab",), page_bg=GROUND, expect_hero=True,
                   collision_ignore={("hero", "slab"), ("star_ll", "slab")}, margin=12)
    print("done", out)

asyncio.run(main())
