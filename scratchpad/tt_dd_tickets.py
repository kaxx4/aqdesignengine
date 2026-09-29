"""TerraThon x Disco Diwali: TICKETS AT THE CARNIVAL, Rs. 550 (Workflow C bespoke build, TerraThon format).

Brief (user, 2026-09-29): "disco diwali ticket sales at 550rs promotion for carnival at terrathon",
then "nice graphic icons stickers less text". The first message said 55rs, a follow-up said 550rs; built
at Rs. 550, flagged to the user as an assumption.

Same visual system as tt_minifete.py (black ground, four shuriken, tilted white slab with orchid border,
AQ logo + cream CTA pill) but the mechanism is STICKERS-FIRST: the hero is a hung DISCO BALL, with a DIYA
(Diwali) and a TICKET, all drawn here in the kit's die-cut treatment (cream halo, flat fills, rough edge).
The only big type is the price. Text budget: 2 header lines, price, one tag, one info row, CTA.

Adaptations (CLAUDE.md sec 2 rule 4):
  * The disco ball, diya and ticket are NOT in the supplied kit, so they are drawn as SVG with an feMorphology
    halo + turbulence-displaced edge that imitates the kit's hand-cut die-cut (sec 3 rule 5 says stickers are
    assets because sticker() cannot do the rough edge; this filter approximates it. Swap in real files if supplied).
  * No fabricated barcode / QR on the ticket (real-assets rule): the ticket carries a star and a perforation.
  * Palette stays TerraThon's own (blue / green / orchid / cream on black), not core.ACCENTS.
  * Disco Diwali's own date and venue were NOT supplied, so they are not printed. The date/venue row is the
    CARNIVAL's (3rd and 4th Oct, Turf XL, New Alipore), where the tickets are sold.
  * NeutralFace 900/400, no stretched glyphs; StretchPro only for the price numerals if it carries digits.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_tickets.py
"""
import asyncio, importlib.util, math, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, px, S, W, H = tt.core, tt.B, tt.px, tt.S, tt.W, tt.H
GROUND, ORCHID, HALO, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB
INK, WHITE, CTA_FILL = tt.INK, tt.WHITE, tt.CTA_FILL
BLUE, GREEN, PURPLE, NAVY = "#0396FF", "#2FD284", "#D468E8", "#0A3D8F"

CAP, BOX = 0.81, -0.02
CONTENT = dict(head=("LIMITED TICKETS ON SALE", "DISCO DIWALI"), price="RS. 550", tag="AT THE CARNIVAL",
               date="3RD & 4TH OCT", venue="TURF XL", cta="DD TICKET STALL")


def die_filter(fid, seed, halo=13, rough=9):
    """The kit's die-cut: cream halo grown from the artwork's alpha, edge roughened by turbulence."""
    return (f'<filter id="{fid}" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">'
            f'<feMorphology in="SourceAlpha" operator="dilate" radius="{halo}" result="d"/>'
            f'<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="{seed}" result="n"/>'
            f'<feDisplacementMap in="d" in2="n" scale="{rough}" result="dh"/>'
            f'<feFlood flood-color="{HALO}"/><feComposite in2="dh" operator="in" result="cream"/>'
            f'<feDisplacementMap in="SourceGraphic" in2="n" scale="3.5" result="art"/>'
            f'<feMerge><feMergeNode in="cream"/><feMergeNode in="art"/></feMerge></filter>')


def star4(cx, cy, r, fill, rot=0, inner=.34):
    pts = []
    for i in range(8):
        a = math.radians(rot + i * 45 - 90); rr = r if i % 2 == 0 else r * inner
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def disco_ball(size, fid="dbf"):
    """Hung mirror ball: a spherical tile grid (lat/lon quads), palette-cycled, with a string and a highlight."""
    R, cx, cy = 200, 250, 330
    rnd = random.Random(11)
    tiles = ""
    n_lon, n_lat = 12, 9
    for j in range(n_lat):
        la0 = math.radians(-90 + j * 180 / n_lat + 1.6); la1 = math.radians(-90 + (j + 1) * 180 / n_lat - 1.6)
        for i in range(n_lon):
            lo0 = math.radians(-90 + i * 180 / n_lon + 1.6); lo1 = math.radians(-90 + (i + 1) * 180 / n_lon - 1.6)
            quad = [(la0, lo0), (la0, lo1), (la1, lo1), (la1, lo0)]
            P = [(cx + R * math.cos(la) * math.sin(lo), cy + R * math.sin(la)) for la, lo in quad]
            # tiles facing the light (upper-left) are brighter; the rest cycle the kit palette
            lit = (lo0 + lo1) / 2 < math.radians(-20) and (la0 + la1) / 2 < math.radians(10)
            col = rnd.choices([BLUE, GREEN, PURPLE, HALO, NAVY], weights=[5, 3, 3, 4, 0] if lit else [8, 3, 2, 1, 0])[0]
            tiles += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in P)}" fill="{col}"/>'
    art = (f'<rect x="228" y="118" width="44" height="26" rx="6" fill="{PURPLE}"/>'
           f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{NAVY}"/>'
           f'<clipPath id="bc"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath><g clip-path="url(#bc)">{tiles}</g>'
           f'<path d="M{cx - 150},{cy - 96} A180,180 0 0 1 {cx - 40},{cy - 176}" stroke="{WHITE}" stroke-width="14" fill="none" stroke-linecap="round" opacity=".9"/>')
    h = size * 460 / 500
    return (f'<svg width="{size}" height="{h}" viewBox="0 100 500 460" overflow="visible"><defs>{die_filter(fid, 4)}</defs>'
            f'<rect x="246" y="96" width="8" height="40" fill="{HALO}"/><g filter="url(#{fid})">{art}</g></svg>'), h


def diya(size, fid="dyf"):
    """Diwali lamp: a bowl, a wick and a flame, with light sparks."""
    art = (f'<path d="M30,150 Q30,250 150,262 Q270,250 270,150 Z" fill="{PURPLE}"/>'
           f'<path d="M20,146 Q150,200 280,146 Q150,120 20,146 Z" fill="{GREEN}"/>'
           f'<path d="M62,196 Q150,236 238,196" stroke="{HALO}" stroke-width="9" fill="none" stroke-linecap="round"/>'
           f'<path d="M150,132 C96,92 122,44 150,14 C178,44 204,92 150,132 Z" fill="{GREEN}"/>'
           f'<path d="M150,120 C128,100 138,76 150,58 C162,76 172,100 150,120 Z" fill="{HALO}"/>'
           + star4(52, 70, 20, GREEN, 0))
    return (f'<svg width="{size}" height="{size * 280 / 300}" viewBox="0 0 300 280" overflow="visible"><defs>{die_filter(fid, 9, 11, 8)}</defs>'
            f'<g filter="url(#{fid})">{art}</g></svg>'), size * 280 / 300


def spark(size, fill, fid, seed=5):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" overflow="visible"><defs>{die_filter(fid, seed, 5, 5)}</defs>'
            f'<g filter="url(#{fid})">{star4(50, 50, 44, fill, 0, .3)}</g></svg>')


def ticket(size, fid="tkf"):
    """Admit-one stub, textless: notched sides, a perforation, a shuriken star."""
    art = (f'<mask id="tkm"><rect x="10" y="20" width="380" height="200" rx="26" fill="#fff"/>'
           f'<circle cx="10" cy="120" r="30" fill="#000"/><circle cx="390" cy="120" r="30" fill="#000"/></mask>'
           f'<g mask="url(#tkm)"><rect x="10" y="20" width="380" height="200" fill="{GREEN}"/>'
           f'<rect x="280" y="20" width="110" height="200" fill="{PURPLE}"/></g>'
           f'<line x1="280" y1="38" x2="280" y2="202" stroke="{HALO}" stroke-width="7" stroke-dasharray="4 14" stroke-linecap="round"/>'
           + star4(148, 120, 70, HALO, 0, .38) + f'<circle cx="148" cy="120" r="12" fill="{GREEN}"/>'
           + star4(335, 120, 34, HALO, 0, .38))
    return (f'<svg width="{size}" height="{size * 240 / 400}" viewBox="0 0 400 240" overflow="visible"><defs>{die_filter(fid, 21, 12, 9)}</defs>'
            f'<g filter="url(#{fid})">{art}</g></svg>'), size * 240 / 400


async def build(c, out, canvas="feed"):
    story = canvas == "story"; Hc = 1920 if story else H
    dy = 260 if story else 0            # story: everything drops as one block below IG's top UI zone
    els = []

    def el(label, x, y, w, h):
        els.append((label, x, y + dy, w, h))

    def shuriken(label, x0, y0, z, k=tt.NATIVE):
        im, src = tt.crop_to_alpha("shuriken.png")
        w, h = px(im.width * k), px(im.height * k)
        el(label, px(x0), px(y0), w, h)
        return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{px(x0)}px;top:{px(y0) + dy}px;'
                f'width:{w}px;height:{h}px;z-index:{z}">')

    # ---- measure type ----
    m = await B.measure_text([
        dict(text=c["head"][0], font="d", size=px(96), weight=400),
        dict(text=c["head"][1], font="d", size=px(120), weight=900),
        dict(text=c["price"], font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text=c["tag"], font="SigmarOne", size=px(72), weight=400, letter_spacing=f"{tt.SG_LS}em"),
        dict(text=c["date"], font="d", size=px(50), weight=400),
        dict(text=c["venue"], font="d", size=px(50), weight=400),
        dict(text=c["cta"], font="d", size=px(44), weight=900),
    ], extra_css=tt.FONT_CSS)
    tw = [r["text_w"] for r in m]
    price_px = 100 * px(1180) / tw[2]
    tag_px = px(72) * min(1.0, px(1000) / tw[3])
    h1_px = px(96) * min(1.0, 690 / tw[0]); h1_w = tw[0] * h1_px / px(96)
    h2_px = px(120) * min(1.0, px(1230) / tw[1])

    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, Hc):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * Hc / H)))
    ground = (f'<div style="position:absolute;inset:0;background:{GROUND}"></div>'
              f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{Hc}">{specks}</svg>')

    # ---- header (two lines, centred) ----
    HB = f'position:absolute;left:0;width:{W}px;text-align:center;color:{WHITE};z-index:6;white-space:nowrap;line-height:1;font-family:var(--d)'
    hdr = (f'<div class="measure" data-tag="h1" style="{HB};top:{px(70) + dy}px;font-weight:400;font-size:{h1_px}px">{c["head"][0]}</div>'
           f'<div class="measure" data-tag="h2" style="{HB};top:{px(170) + dy}px;font-weight:900;font-size:{h2_px}px">{c["head"][1]}</div>')
    el("h1", (W - h1_w) / 2, px(78), h1_w, h1_px * CAP); el("h2", (W - tw[1] * h2_px / px(120)) / 2, px(180), tw[1] * h2_px / px(120), px(CAP * 120))
    hdr = hdr.replace(f'left:0;width:{W}px;text-align:center', f'left:{(W - h1_w) / 2}px;width:{h1_w + 4}px;text-align:center', 1)
    hw2 = tw[1] * h2_px / px(120)
    hdr = hdr.replace(f'left:0;width:{W}px;text-align:center', f'left:{(W - hw2) / 2}px;width:{hw2 + 4}px;text-align:center', 1)

    # ---- stickers ----
    ball_w = 625
    ball, ball_h = disco_ball(ball_w)
    bx, by = (W - ball_w) / 2, 72 + 100 * ball_w / 500
    dsz = 300; dya, dya_h = diya(dsz); dx0, dy0 = 132, 548
    tsz = 360; tk, tk_h = ticket(tsz)
    tx0, ty0 = 668, 470
    box = lambda x, y, svg, z, rot=0, tag="": (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + dy}px;z-index:{z};'
                                              f'transform:rotate({rot}deg)">{svg}</div>')
    sp = [("sp1", 88, 320, 74, GREEN), ("sp2", 930, 330, 64, PURPLE), ("sp3", 60, 452, 46, HALO)]
    sparks = "".join(box(x, y, spark(sz, col, "sp" + str(i)), 6, 0, t) for i, (t, x, y, sz, col) in enumerate(sp))
    for t, x, y, sz, _ in sp: el(t, x, y, sz, sz)
    stickers = sparks + box(bx, by, ball, 4, 0, "ball") + box(dx0, dy0, dya, 10, -8, "diya") + box(tx0, ty0, tk, 7, 12, "ticket")
    el("ball", bx, by, ball_w, ball_h); el("diya", dx0 - 18, dy0 - 23, 337, 326); el("ticket", tx0 - 19, ty0 - 38, 398, 293)
    stars = (shuriken("star_tl", 62, 78, 5) + shuriken("star_tr", 1402, 256, 5) + shuriken("star_ml", 20, 988, 5)
             + shuriken("star_br", 1458, 1506, 9, k=tt.NATIVE * 0.9))

    # ---- slab: price + tag ----
    SX, SY, SW, SH = px(78), px(1114), px(1467), px(520)
    el("slab", SX - px(6), SY - px(12), SW + px(12), SH + px(24))
    def tier(txt, size_px, top_ref, fam, wt=400):
        sg = fam == "SigmarOne"
        stroke, ls = (tt.SG_STROKE, tt.SG_LS) if sg else (tt.ST_STROKE, tt.ST_LS)
        feat = "normal" if sg else tt.ST_FEAT
        return (f'<div style="position:absolute;left:0;width:100%;text-align:center;top:{px(top_ref - 1114 - 28) - BOX * size_px}px;font-family:{fam};'
                f'font-weight:{wt};color:{INK};-webkit-text-stroke:{stroke * size_px}px {INK};letter-spacing:{ls}em;font-feature-settings:{feat};'
                f'font-size:{size_px}px;line-height:1;white-space:nowrap">{txt}</div>')
    slab = (f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{SY + dy}px;width:{SW}px;height:{SH}px;'
            f'transform:rotate(-1.3deg);background:{SLAB};border:{px(28)}px solid {ORCHID};border-radius:{px(70)}px;z-index:8">'
            + tier(c["price"], price_px, 1228, "StretchPro") + tier(c["tag"], tag_px, 1470, "SigmarOne") + "</div>")

    # ---- info row: calendar, date, pin, venue ----
    FS = px(50); cal_w, gap, grp = px(84), px(10), px(60)
    total = cal_w + gap + tw[4] + grp + px(60) + gap + tw[5]
    x = (W - total) / 2
    LBL = f'font-family:var(--d);font-weight:400;font-size:{FS}px;line-height:1;color:{WHITE};white-space:nowrap'
    ry = 1691 - BOX * 50 + 8
    cal = (f'<svg class="measure" data-tag="cal" style="position:absolute;left:{x}px;top:{px(1682) + dy + 6}px;z-index:6" width="{cal_w}" height="{px(84)}" viewBox="0 0 84 84">'
           f'<rect x="6" y="14" width="72" height="64" rx="10" fill="{HALO}"/><rect x="6" y="14" width="72" height="20" rx="8" fill="{ORCHID}"/>'
           f'<rect x="20" y="4" width="8" height="18" rx="4" fill="{HALO}"/><rect x="56" y="4" width="8" height="18" rx="4" fill="{HALO}"/>'
           f'<rect x="18" y="44" width="14" height="12" rx="3" fill="{INK}"/><rect x="38" y="44" width="14" height="12" rx="3" fill="{INK}"/>'
           f'<rect x="58" y="44" width="10" height="12" rx="3" fill="{INK}"/></svg>')
    el("cal", x, px(1682) + 6, cal_w, px(84))
    dxp = x + cal_w + gap
    pinx = dxp + tw[4] + grp
    pin = (f'<svg class="measure" data-tag="pin" style="position:absolute;left:{pinx}px;top:{px(1682) + dy + 6}px;z-index:6" width="{px(60)}" height="{px(84)}" viewBox="0 0 60 84">'
           f'<path d="M30 6 C14 6 6 18 6 30 C6 50 30 78 30 78 C30 78 54 50 54 30 C54 18 46 6 30 6 Z" fill="{GREEN}"/><circle cx="30" cy="30" r="10" fill="{INK}"/></svg>')
    el("pin", pinx, px(1682) + 6, px(60), px(84))
    vx = pinx + px(60) + gap
    info = (cal + pin + f'<div class="measure" data-tag="date" style="position:absolute;left:{dxp}px;top:{px(ry) + dy}px;{LBL}">{c["date"].replace("&", "&amp;")}</div>'
            f'<div class="measure" data-tag="venue" style="position:absolute;left:{vx}px;top:{px(ry) + dy}px;{LBL}">{c["venue"]}</div>')
    el("date", dxp, px(1691) + 8, tw[4], px(CAP * 50)); el("venue", vx, px(1691) + 8, tw[5], px(CAP * 50))

    # ---- footer ----
    lh = px(83)
    logo = f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{px(40)}px;top:{px(1888) + dy + (60 if story else 0)}px;height:{lh}px;z-index:9">'
    el("logo", px(40), px(1888) + (60 if story else 0), px(475), lh)
    cw, ch = tw[6] + px(120), px(100)
    cx, cy = W - cw - px(32), px(1880) + (60 if story else 0)
    el("cta", cx, cy, cw, ch)
    cta = (f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy + dy}px;width:{cw}px;height:{ch}px;border:{px(9)}px solid {ORCHID};'
           f'border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;'
           f'font-size:{px(44)}px;color:{INK}">{c["cta"]}</div>')

    html = B.page(W, Hc, GROUND, f'<style>{tt.FONT_CSS}</style>' + ground + hdr + stickers + stars + slab + info + logo + cta, grain=False)
    text_pairs = [("h", WHITE, GROUND, 96, True), ("info", WHITE, GROUND, 40, False), ("price", INK, SLAB, 100, True), ("cta", INK, CTA_FILL, 34, True)]
    await B.render(html, out, W, Hc, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=True,
                   collision_ignore={("diya", "slab"), ("ball", "diya"), ("ball", "ticket"), ("ticket", "slab"), ("star_ml", "slab"), ("star_br", "slab"),
                                     ("ball", "slab"), ("diya", "star_ml"), ("diya", "ball"), ("ticket", "star_tr")}, margin=12, bleed_tags=("star_br",))


async def main():
    os.makedirs("out/versions/terrathon_dd_tickets", exist_ok=True)
    out = f"out/versions/terrathon_dd_tickets/v{os.environ.get('TT_V', '1')}.png"
    async with B.session():
        await build(CONTENT, out)
    print("done", out)

if __name__ == "__main__":
    asyncio.run(main())
