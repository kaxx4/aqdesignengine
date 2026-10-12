"""DISCO DIWALI "missing pieces" carousel (user inspo, 2026-10-12): a photo cut as a jigsaw with clusters of pieces missing; the holes show
white paper with small lowercase lines of copy; a few loose pieces lie around the board. TerraThon dress: black ground, white board with an
orchid keyline (so the holes read as white), pieces carry a cream die-cut edge when loose. 3 slides, feed 1080x1350 + story 1080x1920 (arg: story).
1 dance photo, six holes + the DISCO DIWALI name in StretchPro / 2 decor photo, four holes / 3 group photo, one hole "you're the missing piece".
Teaser: no tickets, date, venue, price. Real DD photos only. Jigsaw outlines are generated (shared edge knobs, so neighbours interlock).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_puzzle.py [story]  -> out/collaterals/dd_puzzle[_story]/
"""
import asyncio, base64, importlib.util, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(sp); sp.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
ORCHID, CTA_FILL, INK, WHITE, SLAB = tt.ORCHID, tt.CTA_FILL, tt.INK, tt.WHITE, tt.SLAB
STORY = len(sys.argv) > 1 and sys.argv[1] == "story"
H = 1920 if STORY else 1350
FOOT = 270 if STORY else 0
COLS, ROWS = 9, (9 if not STORY else 10)
BX, BW = 70, 940
PW = BW / COLS
PH = PW * (1.0 if not STORY else 1.02)
BH = PH * ROWS
BY = 205 if not STORY else 440
PHOTO = {n: "data:image/jpeg;base64," + base64.b64encode(open(f"engine/assets/terrathon/dd_photos/{n}.jpg", "rb").read()).decode() for n in ("dance", "decor", "group")}
PSIZE = {"dance": (1500, 1000), "decor": (1500, 1125), "group": (1500, 1000)}


def knob_pts(L, sign, seed):
    """Canonical knob along an edge of length L (from 0 to L), bulging by `sign` (+1/-1) perpendicular. Returns (u,v) points."""
    rnd = random.Random(seed); sh = rnd.uniform(-0.03, 0.03)
    cu, cv, r = 0.5 + sh, 0.145, 0.088
    pts = [(0.0, 0.0), (0.36 + sh, 0.0), (0.40 + sh, 0.012), (0.43 + sh, 0.045), (cu + r * math.cos(math.radians(250)), cv + r * math.sin(math.radians(250)))]
    for a in range(250, -71, -10):
        pts.append((cu + r * math.cos(math.radians(a)), cv + r * math.sin(math.radians(a))))
    pts += [(0.57 + sh, 0.045), (0.60 + sh, 0.012), (0.64 + sh, 0.0), (1.0, 0.0)]
    return [(u * L, v * L * sign) for u, v in pts]


# edges[(r,c,'h')] = horizontal edge ABOVE piece (r,c) ; edges[(r,c,'v')] = vertical edge LEFT of piece (r,c)
EDGE = {}
rr = random.Random(7)
for r in range(ROWS + 1):
    for c in range(COLS + 1):
        EDGE[(r, c, 'h')] = rr.choice((-1, 1)); EDGE[(r, c, 'v')] = rr.choice((-1, 1))


def piece_poly(r, c):
    x0, y0 = c * PW, r * PH
    pts = []
    def add(seq):
        for p in seq:
            if not pts or abs(pts[-1][0] - p[0]) + abs(pts[-1][1] - p[1]) > 0.01: pts.append(p)
    # top: left->right
    if r == 0: add([(x0, y0), (x0 + PW, y0)])
    else: add([(x0 + u, y0 + v) for u, v in knob_pts(PW, EDGE[(r, c, 'h')], r * 100 + c)])
    # right: top->bottom (edge left of piece (r,c+1))
    if c == COLS - 1: add([(x0 + PW, y0), (x0 + PW, y0 + PH)])
    else: add([(x0 + PW + v, y0 + u) for u, v in knob_pts(PH, EDGE[(r, c + 1, 'v')], r * 100 + c + 1 + 5000)])
    # bottom: right->left (edge above piece (r+1,c), reversed)
    if r == ROWS - 1: add([(x0 + PW, y0 + PH), (x0, y0 + PH)])
    else: add([(x0 + u, y0 + PH + v) for u, v in reversed(knob_pts(PW, EDGE[(r + 1, c, 'h')], (r + 1) * 100 + c))])
    # left: bottom->top
    if c == 0: add([(x0, y0 + PH), (x0, y0)])
    else: add([(x0 + v, y0 + u) for u, v in reversed(knob_pts(PH, EDGE[(r, c, 'v')], r * 100 + c + 5000))])
    return pts


def path(pts): return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


def board_svg(key, focus, holes, loose, uid):
    """Return (svg_html_for_board, [loose svg parts], hole boxes). Image fills the board with object-fit cover at `focus`."""
    iw, ih = PSIZE[key]; s = max(BW / iw, BH / ih); w, h = iw * s, ih * s
    ox = -(w - BW) * focus[0]; oy = -(h - BH) * focus[1]
    missing = set(); boxes = []
    for (r0, c0, rs, cs, txt, fs) in holes:
        for r in range(r0, r0 + rs):
            for c in range(c0, c0 + cs): missing.add((r, c))
        boxes.append((c0 * PW, r0 * PH, cs * PW, rs * PH, txt, fs))
    defs, body = "", ""
    img = f'<image href="{PHOTO[key]}" x="{ox:.1f}" y="{oy:.1f}" width="{w:.1f}" height="{h:.1f}" preserveAspectRatio="none"/>'
    for r in range(ROWS):
        for c in range(COLS):
            if (r, c) in missing: continue
            defs += f'<clipPath id="{uid}p{r}_{c}"><path d="{path(piece_poly(r, c))}"/></clipPath>'
            body += f'<g clip-path="url(#{uid}p{r}_{c})">{img}</g><path d="{path(piece_poly(r, c))}" fill="none" stroke="rgba(0,0,0,.42)" stroke-width="1.6"/><path d="{path(piece_poly(r, c))}" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="0.8" transform="translate(.8,.8)"/>'
    loose_svgs = []
    for k, (r, c, dx, dy, rot) in enumerate(loose):
        poly = piece_poly(r, c); cx, cy = c * PW + PW / 2, r * PH + PH / 2
        loose_svgs.append((f'<clipPath id="{uid}l{k}"><path d="{path(poly)}"/></clipPath>'
                           f'<g transform="translate({dx - cx:.1f},{dy - cy:.1f}) rotate({rot},{cx:.1f},{cy:.1f})">'
                           f'<path d="{path(poly)}" fill="{CTA_FILL}" stroke="{CTA_FILL}" stroke-width="9" stroke-linejoin="round"/>'
                           f'<g clip-path="url(#{uid}l{k})">{img}</g><path d="{path(poly)}" fill="none" stroke="rgba(0,0,0,.4)" stroke-width="1.6"/></g>', (dx, dy)))
    return defs, body, loose_svgs, boxes


SLIDES = {
    "1": ("dance", (0.55, 0.5), [(1, 0, 2, 3, "the lights", 30), (0, 5, 2, 4, None, 0), (3, 3, 2, 2, "the dance floor", 30), (5, 0, 2, 2, "your people", 30), (5, 6, 2, 3, "the music", 30), (7, 3, 1, 3, "what to wear?", 28)],
          [(1, 1, 110, 105, -12), (3, 4, 335, 100, 8), (1, 6, 560, 105, -6), (6, 7, 765, 100, -9), (0, 7, 965, 105, 14)], "disco"),
    "2": ("decor", (0.3, 0.55), [(1, 1, 2, 3, "balls", 34), (1, 5, 2, 3, "blocks", 34), (5, 1, 2, 3, "a cassette", 34), (5, 5, 2, 3, "one night", 34)],
          [(1, 2, 140, 105, 12), (2, 6, 400, 100, -10), (5, 2, 680, 105, 9), (6, 6, 930, 105, -16)], None),
    "3": ("group", (0.45, 0.4), [(3, 3, 3, 3, "you're the missing piece", 38)], [(4, 4, 700, 105, 12), (5, 3, 260, 105, -8)], None),
}


def hole_text(boxes, tag_prefix, els):
    out = ""
    for i, (x, y, w, h, txt, fs) in enumerate(boxes):
        X, Y = BX + x, BY + y
        if txt is None:   # the name
            out += (f'<div class="measure" data-tag="{tag_prefix}name" style="position:absolute;left:{X}px;top:{Y}px;width:{w}px;height:{h}px;display:flex;align-items:center;justify-content:center;z-index:6;text-align:center;'
                    f'font-family:StretchPro;font-size:{w * 0.19:.0f}px;line-height:.95;color:{INK};-webkit-text-stroke:{w * .19 * tt.ST_STROKE:.1f}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT}">DISCO<br>DIWALI</div>')
            els.append((f"{tag_prefix}name", X + 10, Y + 10, w - 20, h - 20))
        else:
            out += (f'<div class="measure" data-tag="{tag_prefix}h{i}" style="position:absolute;left:{X + 14}px;top:{Y}px;width:{w - 28}px;height:{h}px;display:flex;align-items:center;justify-content:center;text-align:center;z-index:6;'
                    f'font-family:var(--e);font-weight:500;font-size:{fs}px;line-height:1.1;letter-spacing:-0.02em;color:{INK}">{txt}</div>')
            els.append((f"{tag_prefix}h{i}", X + 14, Y + h * .3, w - 28, h * .4))
    return out


def build(name):
    key, focus, holes, loose, kind = SLIDES[name]
    els = []
    sc = 1.0 if not STORY else 1.0
    loose_scaled = []
    for (r, c, dx, dy, rot) in loose:
        # loose centre in canvas coords -> board-local coords
        loose_scaled.append((r, c, dx - BX, (dy if not STORY else dy + 225) - BY, rot))
    defs, body, loose_svgs, boxes = board_svg(key, focus, holes, loose_scaled, f"s{name}")
    html = f'<style>{tt.FONT_CSS}</style><div style="position:absolute;inset:0;background:#000"></div>'
    specks = ""
    rnd = random.Random(int(name) * 11)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(480))
    # cool ground: deep indigo base, coloured glow orbs (orchid / blue / mint), disco light rays from the top, 4-point sparkles
    glow = (f'<div style="position:absolute;inset:0;background:'
            f'radial-gradient(ellipse 70% 38% at 12% 8%,rgba(222,104,240,.55),transparent 70%),'
            f'radial-gradient(ellipse 65% 40% at 92% 14%,rgba(3,150,255,.5),transparent 70%),'
            f'radial-gradient(ellipse 80% 40% at 50% 104%,rgba(222,104,240,.45),transparent 70%),'
            f'radial-gradient(ellipse 50% 30% at 4% 70%,rgba(47,210,132,.28),transparent 70%),'
            f'radial-gradient(ellipse 50% 30% at 98% 60%,rgba(3,150,255,.3),transparent 70%),#09051a;z-index:0"></div>')
    rays = (f'<div style="position:absolute;inset:0;z-index:1;background:repeating-conic-gradient(from -90deg at 50% -6%,rgba(255,255,255,.075) 0deg 5deg,transparent 5deg 15deg);'
            f'-webkit-mask-image:radial-gradient(ellipse 90% 70% at 50% 0%,#000 0%,transparent 75%);mask-image:radial-gradient(ellipse 90% 70% at 50% 0%,#000 0%,transparent 75%)"></div>')
    def spark(cx, cy, r, op):
        k = r * .22
        return (f'<path d="M{cx},{cy - r} Q{cx + k},{cy - k} {cx + r},{cy} Q{cx + k},{cy + k} {cx},{cy + r} Q{cx - k},{cy + k} {cx - r},{cy} Q{cx - k},{cy - k} {cx},{cy - r}Z" fill="#fff" opacity="{op}"/>')
    sp_ = "".join(spark(rnd.uniform(0, W), rnd.uniform(0, H), rnd.choice([7, 9, 12, 16, 22]), rnd.uniform(.35, .9)) for _ in range(34))
    html += glow + rays + f'<svg style="position:absolute;inset:0;z-index:2" width="{W}" height="{H}">{specks}{sp_}</svg>'
    # board slab (white, orchid keyline) behind the puzzle: holes show it
    html += (f'<div class="measure" data-tag="board" style="position:absolute;left:{BX - 14}px;top:{BY - 14}px;width:{BW + 28}px;height:{BH + 28}px;box-sizing:border-box;background:{SLAB};border:8px solid {ORCHID};border-radius:22px;z-index:3"></div>')
    els.append(("board", BX - 14, BY - 14, BW + 28, BH + 28))
    html += f'<svg class="measure" data-tag="puzzle" style="position:absolute;left:{BX}px;top:{BY}px;z-index:4" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" overflow="visible"><defs>{defs}</defs>{body}</svg>'
    els.append(("puzzle", BX, BY, BW, BH))
    for k, (svg, (dx, dy)) in enumerate(loose_svgs):
        gx, gy = BX + dx, BY + dy
        S = PW * 1.75
        html += (f'<svg class="measure" data-tag="loose{k}" style="position:absolute;left:{gx - S / 2:.1f}px;top:{gy - S / 2:.1f}px;z-index:7;filter:drop-shadow(0 4px 0 rgba(0,0,0,.55))" width="{S:.0f}" height="{S:.0f}" '
                 f'viewBox="{dx - S / 2:.1f} {dy - S / 2:.1f} {S:.0f} {S:.0f}" overflow="visible"><defs></defs>{svg}</svg>')
        els.append((f"loose{k}", gx - PW * .62, gy - PW * .62, PW * 1.24, PW * 1.24))
    html += hole_text(boxes, f"s{name}", els)
    # footer
    ly = H - FOOT - 27 - 76
    html += (f'<div class="measure" data-tag="logo" style="position:absolute;left:27px;top:{ly}px;height:76px;padding:0 24px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;z-index:9"><img src="{core.LOGO}" style="height:40px"></div>')
    els.append(("logo", 27, ly, 330, 76))
    cw, ch = 150, 54; cx, cy = W - 27 - cw, H - FOOT - 27 - ch
    html += (f'<div class="measure" data-tag="idx" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:900;font-size:24px;color:{INK};z-index:9">{int(name):02d} / 03</div>')
    els.append(("idx", cx, cy, cw, ch))
    return B.page(W, H, "#000", html, grain=False), els


async def main():
    outdir = "out/collaterals/dd_puzzle" + ("_story" if STORY else ""); os.makedirs(outdir, exist_ok=True)
    async with B.session():
        for name in SLIDES:
            html, els = build(name)
            ign = {(a[0], b[0]) for a in els for b in els if a[0] != b[0] and (a[0] in ("board", "puzzle") or b[0] in ("board", "puzzle"))}
            await B.render(html, f"{outdir}/dd_puzzle_{name}.png", W, H, elements=els, page_bg="#000", expect_hero=False, margin=12, collision_ignore=ign, containers=("board",))
            print("done", name)

asyncio.run(main())
