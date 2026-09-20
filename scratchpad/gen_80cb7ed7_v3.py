import asyncio, os, sys, importlib.util, math
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); sh = load("shapes")

W, H = core.SIZES["linkedin"]     # 1200x628 — the judged canvas for this reference (a poster, not a mockup)
A = core.ACCENTS                  # A[0..6]: pink,mint,lemon,tomato,sky,grape,teal
GRAPE = A[5]; TOMATO = A[3]; LEMON = A[2]; INK = core.INK
elements = []                     # (label, x, y, w, h) kept IN SYNC with every div's true bbox

# ---------------------------------------------------------------------------
# THE RIBBON — a single continuous thick wavy band, bleeding off the top and
# bottom edges (measured: compare.geometry reported content bbox y 0.000..0.999,
# i.e. the graphic touches BOTH edges — not a margin miss, the reference's own
# mechanism). No matching engine/shapes.py silhouette exists for a long flowing
# multi-bend ribbon, so it is built here as a stroked SVG polyline (fill:none,
# huge stroke-width, round caps/joins) sampled off a Catmull-Rom curve through
# 5 waypoints read off the reference (brain/RECREATION_AUDIT.md ## 80cb7ed71a8cc9
# step 1), scaled from the reference's 1199x675 px to this canvas's 1200x628.
SX, SY = W / 1199.0, H / 675.0
# Waypoints re-measured directly off the reference pixels (not eyeballed): scanned
# every 20th row for near-#536FD0 pixels and took each run's midpoint (v1's
# eyeballed 5-point path put the whole upper two-thirds ~150-250px too far right,
# which is exactly what compare.py's v1 critique caught: "REGION OVER-filled
# row1 col7" (ribbon touching the top edge too far right) + "REGION UNDER-filled
# row3 col6" and "row6 col8" (the reference's actual crest, which v1 never reached)).
# v3: denser waypoints, sampled directly off the same pixel scan every 20px of
# height (not just 9 hand-picked bends) — v2's coarser 9-point path still left
# three REGION under/over-fill misses (compare.py score 0.246): the crest/trough
# it drew were right in shape but off by ~1 grid cell in exactly where the curve
# sits, because 9 points under-constrains a Catmull-Rom through a shape this
# wiggly. y=460..660 (obscured by the flower/headline in the direct pixel scan)
# is extrapolated from the crop_bot visual read (RECREATION_AUDIT.md).
WAYPTS_SRC = [(681, -40), (643, 20), (654, 50), (695, 80), (881, 100), (902, 140),
              (931, 180), (1101, 220), (1106, 240), (1099, 260), (922, 300),
              (866, 340), (802, 380), (661, 400), (638, 420), (635, 440),
              (646, 460), (850, 500), (950, 540), (1080, 580), (1130, 620),
              (1150, 715)]
WAYPTS = [(x * SX, y * SY) for x, y in WAYPTS_SRC]   # first/last padded past the edge so the round cap itself bleeds, not just the centerline

def catmull_rom_path(pts):
    """Smooth cubic-bezier path through `pts` (Catmull-Rom, tension 1/6) — no
    helper for this exists in engine/*.py; a stroked wavy ribbon has no
    shapes.SILHOUETTES entry, so this is bespoke-script-local, not an engine change."""
    n = len(pts)
    d = f"M{pts[0][0]:.2f} {pts[0][1]:.2f}"
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += f" C{c1[0]:.2f} {c1[1]:.2f} {c2[0]:.2f} {c2[1]:.2f} {p2[0]:.2f} {p2[1]:.2f}"
    return d

RIBBON_SW = 108 * SX   # measured: ribbon width ~9% of the 1199px-wide source
ribbon_d = catmull_rom_path(WAYPTS)
# bbox of the sampled centerline (coarse: every 3px along each segment) + half stroke,
# so bounds_check/collision_check see the TRUE painted extent, not a guessed box.
def sample_bbox(pts, sw, n=400):
    # crude but sufficient: sample the cubic segments densely for min/max
    xs, ys = [], []
    segs = []
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0]-p0[0])/6.0, p1[1] + (p2[1]-p0[1])/6.0)
        c2 = (p2[0] - (p3[0]-p1[0])/6.0, p2[1] - (p3[1]-p1[1])/6.0)
        segs.append((p1, c1, c2, p2))
    for (p1, c1, c2, p2) in segs:
        for t in [i/n for i in range(n+1)]:
            mt = 1-t
            x = mt**3*p1[0] + 3*mt**2*t*c1[0] + 3*mt*t**2*c2[0] + t**3*p2[0]
            y = mt**3*p1[1] + 3*mt**2*t*c1[1] + 3*mt*t**2*c2[1] + t**3*p2[1]
            xs.append(x); ys.append(y)
    return min(xs)-sw/2, min(ys)-sw/2, max(xs)-min(xs)+sw, max(ys)-min(ys)+sw

rx, ry, rw, rh = sample_bbox(WAYPTS, RIBBON_SW)
elements.append(("ribbon", rx, ry, rw, rh))
ribbon = (f'<svg data-tag="ribbon" style="position:absolute;top:0;left:0;z-index:5" width="{W}" height="{H}" '
          f'viewBox="0 0 {W} {H}"><path d="{ribbon_d}" fill="none" stroke="{GRAPE}" '
          f'stroke-width="{RIBBON_SW:.1f}" stroke-linecap="round" stroke-linejoin="round"/></svg>')

# ---------------------------------------------------------------------------
# RED SPARKLE (with face) — measured bbox in source ~(490..730, 30..230),
# centered ~(610,130) diameter ~240px. Deliberately FLAT (no ink outline/halo):
# the reference's own sparkle characters carry no stroke at all, and running
# them through shapes.sticker() would invent a craft-layer detail the
# reference does not have — the "REGION OVER-filled" failure mode applied to
# treatment instead of geometry (see RECREATION_AUDIT.md).
star_cx, star_cy = 610 * SX, 130 * SY
star_size = 230 * SX
star_path = sh.starburst(points=8, R=48, r=25)
star_x, star_y = star_cx - star_size/2, star_cy - star_size/2
elements.append(("star", star_x, star_y, star_size, star_size))
star = (f'<svg data-tag="star" style="position:absolute;top:{star_y:.1f}px;left:{star_x:.1f}px;'  # noqa: intentional occlusion of ribbon, see COLLISION_IGNORE
        f'z-index:8" width="{star_size:.1f}" height="{star_size:.1f}" viewBox="0 0 100 100" '
        f'transform="rotate(-6deg)"><path d="{star_path}" fill="{TOMATO}"/>'
        f'<path d="M40 44 Q44 38 48 44" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
        f'<path d="M56 44 Q60 38 64 44" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
        f'<path d="M42 56 Q52 66 64 55" fill="none" stroke="{INK}" stroke-width="3.4" stroke-linecap="round"/>'
        f'</svg>')

# ---------------------------------------------------------------------------
# YELLOW FLOWER — measured bbox in source ~(980..1160, 420..630), centered
# ~(1070,525) diameter ~200px. Rounder petals than the star (r/R closer to 1)
# to keep the "flower" register the reference itself distinguishes it by.
flower_cx, flower_cy = 1070 * SX, 525 * SY
flower_size = 210 * SX
flower_path = sh.starburst(points=9, R=46, r=34)
flower_x, flower_y = flower_cx - flower_size/2, flower_cy - flower_size/2
elements.append(("flower", flower_x, flower_y, flower_size, flower_size))
flower = (f'<svg data-tag="flower" style="position:absolute;top:{flower_y:.1f}px;left:{flower_x:.1f}px;'
          f'z-index:8" width="{flower_size:.1f}" height="{flower_size:.1f}" viewBox="0 0 100 100">'
          f'<path d="{flower_path}" fill="{LEMON}"/></svg>')

# ---------------------------------------------------------------------------
# HEADLINE + SUBHEAD — measured first (CLAUDE.md §6: "measure text before you
# size anything around it"). Reference headline block spans y-fraction
# 0.378..0.859 of a 675-tall source (three tight lines); subhead is tiny
# (~0.027 of source height) directly under it.
HEAD_X = 88
LINES = ["A WORLD", "OF PURE", "IMAGINATION."]
SUBHEAD = "aprender inglês fazendo arte."

async def build():
    items = [{"text": t, "font": "d", "size": 92, "weight": 900, "transform": "uppercase",
              "letter_spacing": "-1px"} for t in LINES]
    items.append({"text": SUBHEAD, "font": "m", "size": 19, "weight": 700})
    m = await B.measure_text(items, W, H)
    return m

m = asyncio.run(build())
head_m = m[:3]; sub_m = m[3]

LINE_GAP = 4    # tight leading (nearly touching, matching the reference) while
                # staying clear of collision_check's 12px graze threshold — ink_h
                # (105) already overflows the flow box (h=92) by 13px per line,
                # which alone reads as "tight"; LINE_GAP only needs to add flow space.
head_boxes = []
cur_y = 0
for i, hm in enumerate(head_m):
    head_boxes.append((cur_y, hm))
    cur_y += hm["h"] + LINE_GAP
head_block_h = cur_y - LINE_GAP

# Placed OFF the star's measured bottom edge, not centered blindly — a centered
# guess put "A WORLD" 43px into the star's bbox on the first pass (real collision,
# caught by layout.preflight, not by eye). The reference itself has the headline
# start just clear of the sparkle above it.
STAR_GAP = 4
top_y = star_y + star_size + STAR_GAP

headline_html = ""
for i, (rel_y, hm) in enumerate(head_boxes):
    yy = top_y + rel_y
    headline_html += (f'<div class="measure" data-tag="headline_l{i+1}" style="position:absolute;top:{yy:.1f}px;left:{HEAD_X}px;'
                      f'font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:92px;'
                      f'letter-spacing:-1px;line-height:1;color:{INK};z-index:12;white-space:nowrap">{LINES[i]}</div>')
    elements.append((f"headline_l{i+1}", HEAD_X, yy, hm["text_w"], hm["ink_h"]))

SUB_GAP = 14
sub_y = top_y + head_block_h + SUB_GAP
subhead_html = (f'<div class="measure" data-tag="subhead" style="position:absolute;top:{sub_y:.1f}px;left:{HEAD_X}px;'
               f'font-family:var(--m);font-weight:700;font-size:19px;color:{INK};z-index:12">{SUBHEAD}</div>')
elements.append(("subhead", HEAD_X, sub_y, sub_m["text_w"], sub_m["ink_h"]))

# ---------------------------------------------------------------------------
# ASSEMBLE + GATE
# No explicit background div: B.page() already paints `.p{background:var(--bg)}`,
# and a redundant full-inset div with the identical fill tripped reconcile's
# invisible_fill scan on the first pass ("its background ... is the same as the
# 'p' painted directly behind it") — technically true and technically harmless,
# but a real duplicate element rather than a bug, so it is simply not added.
inner = ribbon + star + flower + headline_html + subhead_html
html = B.page(W, H, "var(--bg)", inner, grain=False)

color_pairs = [
    ("ribbon", GRAPE, "var(--bg)"),
    ("star", TOMATO, "var(--bg)"),
    ("flower", LEMON, "var(--bg)"),
    ("headline_l1", INK, "var(--bg)"),
    ("headline_l2", INK, "var(--bg)"),
    ("headline_l3", INK, "var(--bg)"),
    ("subhead", INK, "var(--bg)"),
]

# Two intentional-occlusion pairs, matching the reference exactly:
#  - star/flower sit IN FRONT of the ribbon (the reference's own z-order), so
#    their bboxes overlapping the ribbon's bbox is the mechanism, not a bug.
#  - "IMAGINATION." (headline_l3) is long enough to run onto the ribbon, same
#    as the reference's own "...ION." sitting on the blue band, still legible.
COLLISION_IGNORE = frozenset({frozenset({"ribbon", "star"}),
                              frozenset({"ribbon", "flower"}),
                              frozenset({"headline_l3", "ribbon"}),
                              frozenset({"headline_l2", "ribbon"})})

pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                   page_bg="var(--bg)", core=core, expect_hero=True, min_hero_frac=0.12,
                   collision_ignore=COLLISION_IGNORE, bleed_tags=("ribbon",))
print("PREFLIGHT CLEAN:", pf["clean"])

SLUG = "80cb7ed71a8cc9"

async def main():
    os.makedirs(f"out/versions/{SLUG}", exist_ok=True)
    await B.render(html, f"out/versions/{SLUG}/v3.png", W, H, elements=elements,
                   color_pairs=color_pairs, page_bg="var(--bg)", expect_hero=True,
                   collision_ignore=COLLISION_IGNORE, bleed_tags=("ribbon",))
    print("done -> out/versions/%s/v3.png" % SLUG)

asyncio.run(main())
