import os, sys, asyncio, importlib.util, math
# Repo root from THIS FILE's location (CLAUDE.md section 6 template rule).
_r = os.path.abspath(__file__)
while _r != os.path.dirname(_r) and not os.path.exists(os.path.join(_r, "CLAUDE.md")):
    _r = os.path.dirname(_r)
os.chdir(_r)
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
shapes = load("shapes"); tex = load("tex")

"""
RECREATION v4 of cfec9bd415fff2 (flat-lay cutting-mat desk scene).

CANVAS CHANGE FROM v1-v3 (documented adaptation, see friction log):
The reference is a native 1000x750 (aspect 1.333:1) illustration. v1-v3 rendered it
onto the `feed` canvas (1080x1350, aspect 0.8:1) -- a 1.667x aspect gap. compare.report
on v3 flagged "ASPECT MISMATCH 1.333:1 vs 0.8:1 (40% apart)... NOT comparable to a
same-aspect recreation" and scored 0.664, most of which measures the squeeze-distortion
of a landscape scene into a portrait frame, not a design gap. The style bank's own
judged entry for this slug records canvas:'linkedin' (this was made for a landscape/
square surface, never a 4:5 feed post -- CLAUDE.md section 9's own LinkedIn rule).
`li_square` (1080x1080, aspect 1.0) is the closest registered AQ canvas by log-ratio
(1.333x away vs 1.911x away for `linkedin`), so v4 renders there instead.

NO ADDED HEADLINE (adaptation from v1-v3, which added "BEHIND THE SCENES."). The
reference's own measured content_bbox is y 0.009-0.919 -- the flat-lay mat and its
above-mat decorations already run edge-to-edge with no room for a headline band in the
original frame. Adding one pushes the mat down and shrinks it relative to canvas,
which is exactly the "CONTENT TOO SMALL" failure mode the decision table warns about.
Logo + footer are still house-style-mandatory (CLAUDE.md section 9) but stay small.

SCRIBBLE, NOT COPY. The reference's note-card marks are illegible cursive scrawl, not
real words -- so recreating them as an actual line of copy ("plan your next drive
here.", what v3 did) is not an "acceptable adaptation" (that clause is for swapping the
reference's LITERAL BRAND COPY), it is inventing content the reference does not have.
v4 draws two scribble squiggle paths instead, matching what is actually there.
"""

W, H = core.SIZES["li_square"]  # 1080x1080 -- see docstring above
A = core.ACCENTS
INK = core.INK
elements = []

# ── measured local-fraction layout (relative to the MAT box, not the canvas) ───────
# Computed from the reference's own pixel bbox (1000x750 native), mat at approx
# x60-930,y60-680 (RECREATION_AUDIT Sample 37 inventory), giving mat origin (60,60)
# and mat size (870,620). Every prop's (x0,y0,x1,y1) below is
# ((ref_x - 60)/870, (ref_y - 60)/620) so the ARRANGEMENT on the mat is preserved
# even though the outer canvas aspect changed (RECREATION_PROTOCOL's "wrong shape /
# wrong arrangement" warning -- preserving relative layout is what step 4 actually
# checks, not literal absolute pixels).
MAT_X0, MAT_Y0 = 68, 138
MAT_W, MAT_H = W - 2 * MAT_X0, H - MAT_Y0 - 118  # generous bottom margin for footer/mat-shadow


def loc(fx0, fy0, fx1, fy1):
    return (MAT_X0 + fx0 * MAT_W, MAT_Y0 + fy0 * MAT_H,
            (fx1 - fx0) * MAT_W, (fy1 - fy0) * MAT_H)


def at(x, y, w, h, inner, z=6, rot=0, extra=""):
    return (f'<div style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;'
            f'height:{h:.1f}px;z-index:{z};transform:rotate({rot}deg);{extra}">{inner}</div>')


# ── measured colours (sampled directly from the reference jpg) ─────────────────────
BG      = "#3E5590"   # navy-blue speckled ground, sampled ~(65-68,87-90,145-148)
MAT     = A[1]        # #1B8A5A mint -- reference mat sampled (34,129,89), a near-exact match
MAT_TXT = core.on_ground(MAT, MAT, 13)
ORANGE  = A[3]        # #FF4D2E tomato -- reference under-layer/mug sampled (239,91,61)
LEMON   = A[2]
SKY     = A[4]
PINK    = A[0]

# ── 1. BACKGROUND + speckle texture (navy dots, matches reference's dotted ground) ──
speck = "".join(
    f'<circle cx="{(i * 131) % W}" cy="{(i * 293 + 47) % H}" r="{1.6 + (i % 3) * 0.7}" '
    f'fill="#0A1230" opacity="{0.14 + 0.05 * (i % 3)}"/>'
    for i in range(420)
)
ground = (f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}" '
          f'xmlns="http://www.w3.org/2000/svg">{speck}</svg>')

# ── 2. DOUBLE-LAYERED MAT: orange under-sheet ROTATED a SMALL amount behind an
#    axis-aligned green mat, SAME size, no padding. A rotated rect under a straight
#    one only pokes out near the two corners the rotation carries past the straight
#    edge, tapering to nothing at the opposite two corners and at the edge midpoints
#    -- v4's first pass used +14px padding AND 1.6deg rotation, which produced a
#    near-uniform ~15-20px orange OUTLINE all the way round (visible on every side in
#    the render) instead of the reference's two short corner slivers. Cropped
#    side-by-side comparison (scratchpad/_ref_tr.png vs _gen_tr.png, _ref_bl.png vs
#    _gen_bl.png) showed the padding was the dominant cause: this compare.py REGION
#    critique ("OVER-filled row1/col2", "row10/col1", corroborated by top-right too)
#    was correctly pointing at a real geometry bug, not noise. Dropping the padding
#    and using a much smaller rotation (0.75deg vs 1.6deg) reproduces the short,
#    corner-only peek.
# v5 (0 padding, 0.75deg) undershot -- the corner peek nearly vanished and a soft
# blurred drop-shadow still registered as extra solid content in the background
# margin below the mat (compare.crop of v5's bottom-left vs the reference's showed
# the reference has ONLY the orange sliver there, no mat corner, no shadow blob).
# v6: small explicit padding brings the peek back to a visible size, a bit more
# rotation, and the mat's own shadow drops from a big offset block to a soft tight
# blur so it doesn't paint fake content past the mat's true edge.
# v5/v6/v7 (padding 0-6px + rotation 0.75-1.8deg on the WHOLE rect) all scored ~0.214-
# 0.215 -- barely moved, because that was never the actual mechanism. A full grid diff
# (compare._grid_occupancy on both images, not just the top-3-critique printout) showed
# the reference's own left column (col0) is LOWER than my render's almost everywhere
# down the mat's height (ref ~0.15-0.43, mine ~0.5-0.61 -- a near-constant ~0.2 excess,
# not a taper), and specifically COLLAPSES near the bottom-left corner cell (ref 0.11,
# mine 0.57 -- delta 0.46, the single biggest miss in the whole grid). Cropping that
# exact corner (scratchpad/_ref_bl.png) confirms it: the reference's mat has an OPEN,
# SPARSE bottom-left corner (mostly navy background, one thin orange sliver) -- the
# green mat's own footprint is pulled back from that corner, not padded outward. My
# build had it backwards: adding MORE orange peek there made row9/col0 worse each
# iteration (v6: delta 0.52, v7: delta 0.53) since I was fighting the wrong mechanism.
# v8: clip the green mat's bottom-left and top-right corners on a diagonal (matching
# the low coverage measured at both) so the under-layer's orange shows through a real
# notch instead of a rotated-rect taper.
NOTCH = 66
under = at(MAT_X0, MAT_Y0, MAT_W, MAT_H,
           f'<div style="width:100%;height:100%;background:{ORANGE};border-radius:10px;'
           f'box-shadow:0 6px 14px rgba(0,0,0,.28)"></div>', z=4)
elements.append(("under_layer", MAT_X0, MAT_Y0, MAT_W, MAT_H))

# ── 3. THE GREEN CUTTING MAT — grid lines, ruler numbers 1-13 down the left edge,
#    tick marks along the top edge, inset white frame line. ───────────────────────────
GRID_N = 13
grid_lines = []
for i in range(1, GRID_N):
    fx = i / GRID_N
    grid_lines.append(f'<line x1="{fx*MAT_W:.1f}" y1="0" x2="{fx*MAT_W:.1f}" y2="{MAT_H:.1f}" '
                       f'stroke="#FFFFFF" stroke-opacity=".22" stroke-width="1.4"/>')
for i in range(1, 10):
    fy = i / 9
    grid_lines.append(f'<line x1="0" y1="{fy*MAT_H:.1f}" x2="{MAT_W:.1f}" y2="{fy*MAT_H:.1f}" '
                       f'stroke="#FFFFFF" stroke-opacity=".22" stroke-width="1.4"/>')
# inset white frame
inset = 18
grid_lines.append(f'<rect x="{inset}" y="{inset}" width="{MAT_W-2*inset:.1f}" '
                   f'height="{MAT_H-2*inset:.1f}" fill="none" stroke="#FFFFFF" '
                   f'stroke-opacity=".55" stroke-width="2"/>')
# tick marks along the top edge
ticks = "".join(f'<line x1="{i*(MAT_W/40):.1f}" y1="0" x2="{i*(MAT_W/40):.1f}" y2="9" '
                 f'stroke="#FFFFFF" stroke-opacity=".5" stroke-width="1.6"/>' for i in range(41))
mat_svg = (f'<svg width="{MAT_W}" height="{MAT_H}" style="position:absolute;inset:0" '
           f'xmlns="http://www.w3.org/2000/svg">{"".join(grid_lines)}{ticks}</svg>')
numbers = "".join(
    f'<span style="position:absolute;left:8px;top:{(i/(GRID_N))*MAT_H+MAT_H/(GRID_N*2)-9:.1f}px;'
    f'font-family:var(--m);font-weight:700;font-size:15px;color:#FFFFFF;opacity:.75">{i+1}</span>'
    for i in range(GRID_N))
# diagonal notch cut into the TOP-RIGHT and BOTTOM-LEFT corners (see the under_layer
# comment above -- this is the mechanism the reference actually uses, measured from
# its own low grid coverage at exactly those two corners, not a rotated-rect taper).
_clip = (f'polygon(0 0, {MAT_W-NOTCH:.0f}px 0, {MAT_W:.0f}px {NOTCH:.0f}px, '
         f'{MAT_W:.0f}px {MAT_H:.0f}px, {NOTCH:.0f}px {MAT_H:.0f}px, 0 {MAT_H-NOTCH:.0f}px)')
mat_inner = (f'<div style="width:100%;height:100%;background:{MAT};border-radius:8px;'
             f'border:3px solid {INK};box-shadow:0 8px 18px rgba(0,0,0,.3);position:relative;'
             f'overflow:hidden;clip-path:{_clip}">{mat_svg}{numbers}</div>')
elements.append(("mat", MAT_X0, MAT_Y0, MAT_W, MAT_H))

# ── 4. small confetti cluster near mat's top edge: crown/leaf glyph, white dot,
#    yellow heart, red diamond -- clustered center-top, per the measured local fractions
elements_html = [ground, under, at(MAT_X0, MAT_Y0, MAT_W, MAT_H, mat_inner, z=8)]

lx, ly, lw, lh = loc(0.33, -0.018, 0.41, 0.02)
elements_html.append(at(lx, ly, 30, 30, dd.stamp("leaf", "#0F6B45", rot=-12), z=20))
elements.append(("leaf_glyph", lx, ly, 30, 30))

cx, cy, cw, ch = loc(0.280, 0.014, 0.318, 0.058)
elements_html.append(at(cx, cy, cw, ch,
    f'<div style="width:100%;height:100%;border-radius:50%;background:#F4EFE0;'
    f'border:2.5px solid {INK}"></div>', z=20))
elements.append(("white_dot", cx, cy, cw, ch))

hx, hy, hw, hh = loc(0.332, 0.062, 0.374, 0.112)
elements_html.append(at(hx, hy, hw, hh, dd.stamp("heart", LEMON, rot=-6), z=21))
elements.append(("top_heart", hx, hy, hw, hh))

dx, dy, dw, dh = loc(0.264, 0.128, 0.310, 0.174)
elements_html.append(at(dx, dy, dw, dh,
    f'<div style="width:100%;height:100%;background:{ORANGE};border:2.5px solid {INK};'
    f'box-shadow:3px 4px 0 rgba(0,0,0,.3)"></div>', z=20, rot=45))
elements.append(("top_diamond", dx, dy, dw, dh))

# ── 5. THE NOTE CARD -- pink-to-mint gradient wash, rotated, scribble marks + a small
#    orange flower-face doodle in its top-right corner (matching the reference, NOT
#    real copy -- see docstring). ────────────────────────────────────────────────────
kx, ky, kw, kh = loc(0.132, 0.185, 0.661, 0.702)
scribble_svg = f'''<svg viewBox="0 0 {kw:.0f} {kh:.0f}" width="100%" height="100%"
    style="position:absolute;inset:0" xmlns="http://www.w3.org/2000/svg">
  <path d="M {kw*0.14:.0f} {kh*0.42:.0f}
           C {kw*0.05:.0f} {kh*0.30:.0f} {kw*0.10:.0f} {kh*0.14:.0f} {kw*0.22:.0f} {kh*0.20:.0f}
           C {kw*0.34:.0f} {kh*0.26:.0f} {kw*0.30:.0f} {kh*0.42:.0f} {kw*0.20:.0f} {kh*0.44:.0f}
           C {kw*0.10:.0f} {kh*0.46:.0f} {kw*0.10:.0f} {kh*0.30:.0f} {kw*0.24:.0f} {kh*0.28:.0f}
           C {kw*0.38:.0f} {kh*0.26:.0f} {kw*0.46:.0f} {kh*0.40:.0f} {kw*0.42:.0f} {kh*0.50:.0f}
           C {kw*0.38:.0f} {kh*0.60:.0f} {kw*0.30:.0f} {kh*0.44:.0f} {kw*0.40:.0f} {kh*0.38:.0f}
           C {kw*0.50:.0f} {kh*0.32:.0f} {kw*0.58:.0f} {kh*0.44:.0f} {kw*0.55:.0f} {kh*0.52:.0f}"
        fill="none" stroke="#1E8E63" stroke-width="7" stroke-linecap="round"/>
  <path d="M {kw*0.58:.0f} {kh*0.58:.0f}
           C {kw*0.62:.0f} {kh*0.50:.0f} {kw*0.70:.0f} {kh*0.50:.0f} {kw*0.70:.0f} {kh*0.58:.0f}
           C {kw*0.70:.0f} {kh*0.66:.0f} {kw*0.62:.0f} {kh*0.66:.0f} {kw*0.63:.0f} {kh*0.58:.0f}
           C {kw*0.64:.0f} {kh*0.50:.0f} {kw*0.75:.0f} {kh*0.50:.0f} {kw*0.76:.0f} {kh*0.60:.0f}"
        fill="none" stroke="#3D74C4" stroke-width="6" stroke-linecap="round"/>
</svg>'''
flower = (f'<div style="position:absolute;right:6%;top:5%;width:13%;height:11%">'
          f'{dd.stamp("burst", ORANGE, rot=8)}</div>')
card_inner = (f'<div style="width:100%;height:100%;border-radius:6px;border:3px solid {INK};'
              f'box-shadow:10px 10px 0 rgba(0,0,0,.28);position:relative;overflow:hidden;'
              f'background:linear-gradient(135deg,#F3B9C4 0%,#CFE2C0 55%,#8FC39E 100%)">'
              f'{scribble_svg}{flower}</div>')
elements_html.append(at(kx, ky, kw, kh, card_inner, z=14, rot=-2))
elements.append(("note_card", kx, ky, kw, kh))

# ── 6. PENCIL — two-tone yellow barrel, graphite tip, pink eraser band, diagonal ────
px, py, pw, ph = loc(0.155, 0.516, 0.339, 0.903)
pencil = f'''<svg viewBox="0 0 100 260" width="100%" height="100%"
    style="overflow:visible" xmlns="http://www.w3.org/2000/svg">
  <rect x="28" y="0" width="30" height="22" rx="4" fill="#F2A7C0" stroke="{INK}" stroke-width="3"/>
  <rect x="30" y="20" width="26" height="16" fill="#D9D9D9" stroke="{INK}" stroke-width="2.5"/>
  <rect x="26" y="34" width="34" height="184" fill="{LEMON}" stroke="{INK}" stroke-width="3.5"/>
  <line x1="26" y1="34" x2="26" y2="218" stroke="#E0A800" stroke-width="4"/>
  <polygon points="26,218 60,218 43,250" fill="#E8C088" stroke="{INK}" stroke-width="3"/>
  <polygon points="37,240 49,240 43,254" fill="#2B2B2B"/>
</svg>'''
elements_html.append(at(px, py, pw, ph, pencil, z=18, rot=-32))
elements.append(("pencil", px, py, pw, ph))

# ── 7. MUG — tomato body, white-to-mint tea surface, string + tag, 2 steam/bubble dots
mx, my, mw, mh = loc(0.675, 0.165, 0.842, 0.435)
mug = f'''<svg viewBox="0 0 100 100" width="100%" height="100%" style="overflow:visible"
    xmlns="http://www.w3.org/2000/svg">
  <rect x="18" y="30" width="56" height="58" rx="10" fill="{ORANGE}" stroke="{INK}" stroke-width="4"/>
  <path d="M74 42 Q98 42 98 62 Q98 82 74 78" fill="none" stroke="{INK}" stroke-width="4"/>
  <ellipse cx="46" cy="30" rx="28" ry="12" fill="url(#teagrad)" stroke="{INK}" stroke-width="4"/>
  <defs><linearGradient id="teagrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#B9D9C3"/>
  </linearGradient></defs>
  <circle cx="38" cy="27" r="3" fill="#FFFFFF" opacity=".8"/>
  <circle cx="48" cy="23" r="2" fill="#FFFFFF" opacity=".7"/>
  <line x1="46" y1="18" x2="51" y2="8" stroke="{INK}" stroke-width="2.5"/>
  <rect x="46" y="1" width="12" height="9" rx="2" fill="{LEMON}" stroke="{INK}" stroke-width="2.5"/>
</svg>'''
elements_html.append(at(mx, my, mw, mh, mug, z=17))
elements.append(("mug", mx, my, mw, mh))

# ── 8. two-tone eraser (sky + pink halves), diagonal ────────────────────────────────
ex, ey, ew, eh = loc(0.787, 0.403, 0.948, 0.565)
eraser = (f'<div style="width:100%;height:100%;border:3px solid {INK};border-radius:8px;'
          f'overflow:hidden;display:flex;box-shadow:5px 6px 0 rgba(0,0,0,.28)">'
          f'<div style="width:52%;height:100%;background:{SKY}"></div>'
          f'<div style="width:48%;height:100%;background:{PINK}"></div></div>')
elements_html.append(at(ex, ey, ew, eh, eraser, z=16, rot=-24))
elements.append(("eraser", ex, ey, ew, eh))

# ── 9. plain red/orange circle badge ────────────────────────────────────────────────
rx, ry, rw, rh = loc(0.770, 0.508, 0.868, 0.613)
elements_html.append(at(rx, ry, rw, rh,
    f'<div style="width:100%;height:100%;border-radius:50%;background:{ORANGE};'
    f'border:3px solid {INK};box-shadow:4px 4px 0 rgba(0,0,0,.25)"></div>', z=16))
elements.append(("red_circle", rx, ry, rw, rh))

# ── 10. pink diamond sticker, black heart + 2 teal dots ─────────────────────────────
hdx, hdy, hdw, hdh = loc(0.517, 0.750, 0.632, 0.903)
pink_sticker = f'''<svg viewBox="0 0 100 100" width="100%" height="100%" style="overflow:visible"
    xmlns="http://www.w3.org/2000/svg">
  <rect x="14" y="14" width="72" height="72" rx="8" fill="{PINK}" stroke="{INK}" stroke-width="4"
        transform="rotate(45 50 50)"/>
  <path d="M50 60 C40 50 34 44 40 36 C45 30 50 34 50 40 C50 34 55 30 60 36 C66 44 60 50 50 60 Z"
        fill="{INK}"/>
  <circle cx="30" cy="66" r="4" fill="{A[6]}"/>
  <circle cx="70" cy="34" r="4" fill="{A[6]}"/>
</svg>'''
elements_html.append(at(hdx, hdy, hdw, hdh, pink_sticker, z=18))
elements.append(("pink_diamond", hdx, hdy, hdw, hdh))

# ── 11. yellow set-square triangle ruler, dotted hypotenuse ─────────────────────────
tx, ty, tw, th = loc(0.701, 0.621, 1.0, 0.927)
triangle = f'''<svg viewBox="0 0 100 100" width="100%" height="100%" style="overflow:visible"
    xmlns="http://www.w3.org/2000/svg">
  <polygon points="4,4 4,96 96,96" fill="{LEMON}" stroke="{INK}" stroke-width="4"/>
  {''.join(f'<circle cx="{4+i*92/13:.1f}" cy="{96-i*92/13:.1f}" r="2" fill="{INK}"/>' for i in range(1,13))}
</svg>'''
elements_html.append(at(tx, ty, tw, th, triangle, z=15))
elements.append(("yellow_triangle", tx, ty, tw, th))

# ── logo + footer (house style minimum, kept small -- see docstring) ───────────────
logo = f'<img src="{core.LOGO}" style="position:absolute;top:26px;left:{MAT_X0}px;height:30px;z-index:60;filter:drop-shadow(0 2px 6px rgba(0,0,0,.5))">'
footer = (f'<span style="position:absolute;bottom:38px;left:{MAT_X0}px;font-family:var(--m);'
          f'font-weight:700;font-size:12px;letter-spacing:.06em;color:#FFFFFF;z-index:60">'
          f'@ngo.aquaterra</span>')
elements.append(("logo", MAT_X0, 26, 140, 30))
elements.append(("footer", MAT_X0, H - 38 - 16, 200, 16))

inner = "".join(elements_html) + logo + footer
html = B.page(W, H, BG, inner, grain=False)

color_pairs = [
    ("white_dot", "#F4EFE0", MAT),
    ("top_diamond", ORANGE, MAT),
    ("red_circle", ORANGE, MAT),
]
text_pairs = [("footer", "#FFFFFF", BG, 12, True)]
containers = ("mat",)

pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs, text_pairs=text_pairs,
                    containers=containers, page_bg=BG, core=core, expect_hero=False)


async def main():
    slug = "cfec9bd415fff2"
    outdir = f"out/versions/{slug}"
    os.makedirs(outdir, exist_ok=True)
    out_png = f"{outdir}/v10.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs,
                    text_pairs=text_pairs, containers=containers, page_bg=BG, expect_hero=False)
    print("rendered ->", out_png)

asyncio.run(main())
