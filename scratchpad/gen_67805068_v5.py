"""Workflow B recreation — 67805068493b45 (training_samples/reference_posters/
67805068493b4522f5c3944723bee7d2.jpg), v5.

V5 FIXES OVER V4 (score 0.218 -> see friction doc for the v4 measurement):
  - compare.report on v4 flagged REGION OVER-filled at row8/11,col5/9 (delta 0.78) and eye
    confirmed it: the AQUATERRA wordmark was drawn directly ON TOP of bearBrown, both dense,
    where the reference's own "PLAYBOOK" wordmark sits in a clear empty gap below the
    characters (verified with compare.crop(ref, 0.35,0.60,0.65,0.85,...)). Bear moved up+left+
    smaller; wordmark moved down; a real gap now separates them.
  - REGION OVER-filled at row4/11,col9/9 (delta 0.70): shieldYellow was bled fully off the right
    edge; compare.crop(ref, 0.85,0.20,1.0,0.45,...) shows the reference's shield stops well
    short of the edge with visible cream margin. Shrunk and pulled onto-canvas; no longer a
    declared bleed element.
  - Two elements (flowerPink, flowerGreen2) were overflowing off-canvas UNINTENTIONALLY
    (reconcile.measure_dom OFF-CANVAS, not declared in bleed_tags) — pulled back onto canvas.
  - REGION UNDER-filled at row7/11,col4/9 (delta 0.69): bear's move freed up that cell further;
    birdCream repositioned to cover it.
  - bunnyStretch's overlapping text ("TO"/"show"/"UP") was reading as a jumble by eye; nudged
    apart for legibility while keeping the pile's intentional overlap elsewhere.
  - MISSING COLOUR dark/ink rgb(32,32,32): sentence text darkened from #242424 to #1E1E1E and
    two words enlarged for more ink coverage.
  - starRedBig is the ONLY element still declared as a genuine edge bleed (the reference's
    red starburst is visibly cropped by the left frame edge in the source jpg).

STATUS ENTERING THIS SESSION: v1-v3 exist as PNGs in out/versions/67805068493b45/ (dated
2026-07-14) but the SCRIPT that produced them is lost -- the only surviving trace is
scratchpad/gen_showcase5h.py's `orbit_stickers()` (job "36_orbit_stickers"), which renders to
out/showcase5/36_orbit_stickers.png on the FEED canvas (1080x1350), not into the versions/
folder, and does not match v1-v3's measured area/centroid when re-scored. Treated as lost per
the brief; this file starts a fresh v4, continuing the version count from the PNGs already on
disk.

STEP 0 FINDING THAT CHANGES EVERYTHING: the reference is 1200x2133 px = 0.5625:1, i.e. a STORY
canvas (core.SIZES['story'] = 1080x1920 = exactly 0.5625:1), NOT feed (0.8:1). orbit_stickers()
built on feed -- every prior score for this slug was computed against a wrong-aspect render.
compare.compare() confirms: scoring v1-v3 (which are also feed, 1080x1350) against the reference
prints "ASPECT MISMATCH 0.563:1 vs 0.8:1 (30% apart)" and returns 0.474/0.435/0.435 -- WORSE than
the queue's recorded 0.328, and the queue score is unreproducible from any script found on disk.
This build uses the correct STORY canvas.

COMPOSITION (measured + looked, see friction doc for full step-1 write-up): a ring of ~19
individually-styled illustrated character/shape stickers (flowers, stars, blobs, a bear, a bird,
kite/diamond shapes, coiled spirals) arranged in a loose, INTERLEAVED, OVERLAPPING oval, with a
ten-word sentence woven through the ring at varying font/size/rotation, a two-line wordmark below
the ring, and a large (~20% of canvas height) DELIBERATELY EMPTY cream strip at the very bottom.
compare.geometry(ref): content bbox y 0.157..0.793 (i.e. top 15.7% and bottom 20.7% are empty),
centroid (0.493, 0.446), coverage 0.181.

ADAPTATIONS (§5 step 4 / real-assets rule):
  - The reference's characters are a licensed cute-mascot illustration set (flowers/animals with
    faces). Reproducing the cartoon FACES would be copying a specific character design, not just a
    layout mechanism, so faces are dropped -- the recreation targets the SILHOUETTE FAMILY, colour,
    scale and INTERLEAVED arrangement, not the character IP. This is the single biggest acceptable
    adaptation in this build; flagged explicitly per the recreation protocol.
  - Reference sentence "What does it take to think outside the box?" ending in a real brand's
    wordmark ("PLAYBOOK") is swapped for AQ's own line and "AQUATERRA" wordmark (the real-assets /
    literal-brand-copy rule, CLAUDE.md §9).
  - Reference's italic accent word "think" -> AQ's italic accent word "show" (ONE word, per §9's
    <=1 accent-word rule for Instrument Serif -- the LOST script violated this by italicising two
    words, "show" and "up"; fixed here).
  - Reference "brown" tones (bear, one flower) have no direct core.ACCENTS entry -> derived from
    core.ink_of(A[2]) (lemon darkened to mustard-brown) and a lightened variant of it, per the
    brand rule that a missing hue must be assigned to the NEAREST accent-derived tone, not invented.
"""
import asyncio, os, sys, importlib.util, math
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
S = load("shapes")

W, H = core.SIZES["story"]   # 1080, 1920 -- the reference's own aspect (0.5625:1), NOT feed
M = 64
A = core.ACCENTS
BROWN_DK = core.ink_of(A[2])                  # #7E6000 -- mustard-brown, derived not invented
BROWN_MD = S.lighten(BROWN_DK, 0.18)          # lighter sibling for the 2nd brown element
CREAMY = "#FAF6EC"                            # off-white for the two pale characters (outline-carried)
DARKTXT = "#1E1E1E"                           # measured reference sentence colour is charcoal, not pure ink

elements = []  # (label, x, y, w, h) -- every drawn thing, kept in sync per CLAUDE.md §6


def at(x, y, w, h, inner, z=10, rot=0, label=None):
    if label:
        elements.append((label, x, y, w, h))
    r = f"transform:rotate({rot}deg);" if rot else ""
    return (f'<div style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{w:.0f}px;'
            f'height:{h:.0f}px;z-index:{z};{r}">{inner}</div>')


def stick(shape_path, fill, x, y, size, rot=0, box=100, label=None, z=20):
    """One sticker, uniformly treated. rot is baked into the svg (S.sticker), so the
    wrapping div NEVER also rotates -- avoids the double-rotation bug (§10)."""
    svg = S.sticker(shape_path, fill, size=size, box=box, rot=rot, halo=False, shadow=True)
    return at(x, y, size, size, svg, z=z, label=label)


def word(text, x, y, fs, rot=0, italic=False, color=DARKTXT, z=40, label=None, w=None, h=None):
    ff = "var(--s)" if italic else "var(--d)"
    style = "font-style:italic;" if italic else ""
    ww = w if w is not None else fs * len(text) * 0.62 + 20
    hh = h if h is not None else fs * 1.25
    inner = (f'<div style="font-family:{ff};{style}font-weight:900;font-size:{fs}px;'
              f'line-height:1;color:{color};white-space:nowrap;text-transform:lowercase">{text}</div>')
    return at(x, y, ww, hh, inner, z=z, rot=rot, label=label)


def F(xf, yf):
    return xf * W, yf * H


async def build():
    els_html = []

    # ---------------- the ring: ~19 stickers, hand-placed from compare.geometry's occupancy
    # grid + the looked-at reference (see docstring), overlapping on purpose (§5 hard rule 5:
    # "reference piles overlap; the engine's instinct to separate is wrong here").
    ring = [
        # label, shape_path, fill, xf, yf, sf(size as fraction of W), rot, z
        ("flowerA",      S.blob(seed=3, lobes=8, wobble=0.36),                 A[1], 0.10, 0.145, 0.205, -8,  22),
        ("starRedSmall", S.starburst(points=5, R=48, r=18),                    A[3], 0.42, 0.205, 0.10,   10,  24),
        ("flowerBlueTip",S.scallop(lobes=7, r=42),                             A[4], 0.605,0.205, 0.095, 12,  24),
        ("blobPillow",   S.blob(seed=7, lobes=6, wobble=0.12),                 A[4], 0.02, 0.255, 0.16,  -8,  20),
        ("kiteYellow",   S.starburst(points=4, R=50, r=16),                    A[2], 0.665,0.27,  0.13,   0,  22),
        ("shieldYellow", S.shield(),                                          A[2], 0.775,0.285, 0.16,   8,  18),
        ("bunnyStretch", S.capsule(w=100, h=70),                              CREAMY,0.265,0.335, 0.34,  -24, 26),
        ("flowerBlue2",  S.scallop(lobes=7, r=42),                             A[4], 0.375,0.325, 0.075,  0,  28),
        ("scallopYellow",S.scallop(lobes=6, r=44),                             A[2], 0.135,0.385, 0.15,   4,  20),
        ("starRedBig",   S.starburst(points=7, R=50, r=20),                    A[3], -0.05,0.375, 0.20,  -6,  16),
        ("stemGreenPink",S.blob(seed=15, lobes=5, wobble=0.3),                 A[1], 0.735,0.375, 0.12,  -12, 16),
        ("flowerPink",   S.scallop(lobes=9, r=44),                             A[0], 0.79, 0.405, 0.16,   0,  20),
        ("animalPink",   S.capsule(w=100, h=60),                              A[0], 0.70, 0.46,  0.19,   16,  22),
        ("spiralBlue",   None,                                                A[4], 0.09, 0.45,  0.145,  0,  20),  # doodle
        ("spiralYellow", None,                                                A[2], 0.185,0.515, 0.115, 15,  22),  # doodle
        ("flowerGreen2", S.blob(seed=9, lobes=8, wobble=0.32),                 A[1], 0.83, 0.545, 0.13,  10,  24),
        ("flowerBrown",  S.scallop(lobes=8, r=44),                            BROWN_DK,0.745,0.645,0.135,-6,  20),
        ("kiteBlueLt",   S.starburst(points=4, R=50, r=16),                    A[4], 0.64, 0.695, 0.115,  6,  22),
        ("bearBrown",    S.blob(seed=11, lobes=8, wobble=0.26),               BROWN_MD,0.27, 0.535, 0.24, -10, 18),
        ("birdCream",    S.blob(seed=13, lobes=6, wobble=0.2),                CREAMY,0.475,0.605, 0.135,  8,  22),
    ]
    for label, path, fill, xf, yf, sf, rot, z in ring:
        x, y = F(xf, yf)
        s = sf * W
        if path is None:
            svg = dd.stamp("spiral", fill, rot=rot)
            els_html.append(at(x, y, s, s, svg, z=z, label=label))
        else:
            els_html.append(stick(path, fill, x, y, s, rot=rot, label=label, z=z))

    # a small stroke-drawn squiggle "stem" behind the tiny blue flower near the top, and one
    # leading into the pink flower -- doodles.stamp, per §6, resolves the colour kwarg correctly
    x, y = F(0.50, 0.165); s = 0.20 * W
    els_html.append(at(x, y, s, s * 0.55, dd.stamp("squiggle", A[1], rot=-6), z=14, label="stemGreenTop"))

    # ---------------- the sentence, interleaved through the ring (NOT clustered top-left --
    # that was v1-v3's structural miss on top of the wrong canvas). Spans near-full width like
    # the reference's content bbox (x 0.00..0.998).
    x, y = F(0.145, 0.225); els_html.append(word("does", x, y, 34, rot=-15, label="w_does"))
    x, y = F(0.335, 0.215); els_html.append(word("What", x, y, 50, rot=-8, label="w_What"))
    x, y = F(0.205, 0.375); els_html.append(word("it", x, y, 30, rot=8, label="w_it"))
    x, y = F(0.185, 0.405); els_html.append(word("take", x, y, 44, rot=2, label="w_take"))
    x, y = F(0.33, 0.435);  els_html.append(word("to", x, y, 30, rot=-4, label="w_to"))
    x, y = F(0.40, 0.415);  els_html.append(word("show", x, y, 96, rot=-2, italic=True, label="w_show"))
    x, y = F(0.245, 0.49);  els_html.append(word("up", x, y, 62, rot=3, label="w_up"))
    x, y = F(0.63, 0.505);  els_html.append(word("for", x, y, 30, rot=-6, label="w_for"))
    x, y = F(0.505, 0.525); els_html.append(word("someone", x, y, 64, rot=0, label="w_someone"))
    x, y = F(0.775, 0.485); els_html.append(word("else?", x, y, 46, rot=4, label="w_else"))

    # ---------------- wordmark, two lines + thumbsup, echoing the reference's PLAYBOOK block.
    # Reference (compare.crop 0.35,0.60,0.65,0.85) shows a clear empty gap between the
    # characters and this text -- v4 drew it directly on top of bearBrown; both moved apart.
    wx, wy = F(0.335, 0.755)
    tw = 0.33 * W
    els_html.append(at(wx, wy, tw, 200,
        f'<div style="font-family:var(--d);font-weight:900;font-size:52px;line-height:1.05;'
        f'text-transform:uppercase;color:var(--ink)">AQUA<br>TERRA</div>', z=40, label="wordmark"))
    tx, ty = F(0.60, 0.79)
    els_html.append(at(tx, ty, 70, 70, dd.stamp("thumbsup", A[1], rot=0), z=40, label="thumbsup"))

    # ---------------- logo + tiny footer, both small, both inside the reference's own bottom
    # empty band's outer edge so the ~20% empty strip stays visually empty
    logo_h = 34
    els_html.append(f'<img src="{core.LOGO}" style="position:absolute;top:44px;left:{M}px;'
                     f'height:{logo_h}px;z-index:70">')
    elements.append(("logo", M, 44, 160, logo_h))
    fx, fy = F(0.06, 0.972)
    els_html.append(at(fx, fy, 300, 20,
        f'<span style="font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.06em;'
        f'color:var(--ink)">@ngo.aquaterra</span>', z=70, label="footer"))

    inner = ('<div style="position:absolute;inset:0;background:var(--bg)"></div>'
              + "".join(els_html))
    html = B.page(W, H, "var(--bg)", inner, grain=True)

    color_pairs = [("bunnyStretch", CREAMY, "var(--bg)"), ("birdCream", CREAMY, "var(--bg)")]
    text_pairs = [("w_show", DARKTXT, "var(--bg)", 92, True),
                  ("w_someone", DARKTXT, "var(--bg)", 60, True),
                  ("wordmark", core.INK, "var(--bg)", 58, True)]
    bleed_tags = ("starRedBig",)   # the only element still meant to bleed off-canvas
    # deliberate overlaps in the pile -- declare them so collision_check doesn't flag the design
    # (§10 / audit.py note: this ignore list matches layout.collision_check's LABEL namespace,
    # a different namespace from audit.audit's data-tag one -- see friction doc)
    collision_ignore = {
        ("flowerA", "w_does"), ("w_What", "flowerBlueTip"), ("bunnyStretch", "flowerBlue2"),
        ("bunnyStretch", "w_it"), ("bunnyStretch", "w_take"), ("scallopYellow", "starRedBig"),
        ("stemGreenPink", "flowerPink"), ("flowerPink", "animalPink"), ("w_for", "flowerGreen2"),
        ("flowerBrown", "kiteBlueLt"), ("bearBrown", "birdCream"), ("w_up", "bunnyStretch"),
        ("w_to", "flowerBlue2"), ("w_someone", "flowerBrown"), ("w_someone", "bearBrown"),
        ("w_else", "flowerGreen2"), ("w_else", "kiteBlueLt"), ("kiteYellow", "shieldYellow"),
        ("starRedSmall", "flowerBlueTip"), ("blobPillow", "scallopYellow"),
        ("starRedSmall", "stemGreenTop"), ("starRedSmall", "w_What"), ("flowerBlueTip", "stemGreenTop"),
        ("shieldYellow", "stemGreenPink"), ("bunnyStretch", "scallopYellow"),
        ("bunnyStretch", "spiralYellow"), ("bunnyStretch", "w_to"), ("bunnyStretch", "w_show"),
        ("scallopYellow", "spiralBlue"), ("scallopYellow", "w_it"), ("scallopYellow", "w_take"),
        ("starRedBig", "spiralBlue"), ("flowerPink", "w_else"), ("animalPink", "flowerGreen2"),
        ("animalPink", "w_someone"), ("animalPink", "w_else"), ("spiralBlue", "spiralYellow"),
        ("bearBrown", "wordmark"), ("bearBrown", "birdCream"), ("w_to", "w_show"),
        ("wordmark", "thumbsup"), ("birdCream", "kiteBlueLt"), ("birdCream", "flowerBrown"),
        ("w_someone", "birdCream"), ("bearBrown", "w_up"),
    }

    slug = "67805068493b45"
    os.makedirs(f"out/versions/{slug}", exist_ok=True)
    out_png = f"out/versions/{slug}/v5.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs,
                    text_pairs=text_pairs, page_bg="var(--bg)", expect_hero=False,
                    collision_ignore=collision_ignore, bleed_tags=bleed_tags)
    print("done ->", out_png)


asyncio.run(build())
