"""AQ ENGINE — shapes: parametric die-cut silhouettes + the uniform sticker treatment.

WHY THIS EXISTS (the single biggest recreation-fidelity bug)
`doodles.py` is 20 FIXED stamps, each one flat path in a 120x120 box. So every distinctive
reference silhouette collapses to the nearest stamp:
    reference scalloped badge  -> a plain blob
    reference wavy banner      -> a rounded rectangle
    reference OK-hand          -> a donut
    reference gear             -> square teeth
Measured on c42f94a09f vs its recreation: detail ratio 0.51-0.58x the reference (engine/compare.py).
A sticker is recognised by its OUTLINE. Substituting the silhouette destroys recognition even when
colour and position are right — which is exactly why recreations "stray" while metrics look fine.

Two fixes live here:
  1. PARAMETRIC silhouettes — generated to fit any w/h, so the shape family is matched, not approximated.
  2. sticker() — the uniform treatment (pale die-cut halo + ink outline + optional hard shadow) that
     VISUAL_DNA.md §1 found as the top steal in 5 of 6 reference batches. It is what makes a pile of
     unrelated colours read as ONE set, and it was entirely absent from AQ output.

All builders return an SVG path `d` string in a 0..100 x 0..100 box unless noted; `svg()` scales.
Designed to be callable by a weak model: pick a family name, pass w/h and fill. No judgement needed.
"""
import math

INK = "#0A0A0A"
SW = 6                      # ink outline weight at 100-box scale
HALO = 26                   # die-cut halo weight at 100-box scale


# ── colour helpers ─────────────────────────────────────────────────────────────
def lighten(hex_color, amt=0.55):
    """Tint toward white — the die-cut halo colour is a tint of the element's OWN fill,
    which is what keeps 9 unrelated sticker colours reading as one set."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * amt); g = int(g + (255 - g) * amt); b = int(b + (255 - b) * amt)
    return f"#{r:02X}{g:02X}{b:02X}"


# ── parametric silhouettes (the vocabulary that was missing) ───────────────────
def scallop(lobes=12, r=46):
    """Wavy die-cut badge edge — the 'YOU GOT THIS!' shape. Bumps ride OUTWARD along a circle."""
    cx = cy = 50
    pts = [(cx + r * math.cos(2 * math.pi * i / lobes - math.pi / 2),
            cy + r * math.sin(2 * math.pi * i / lobes - math.pi / 2)) for i in range(lobes)]
    chord = 2 * r * math.sin(math.pi / lobes)
    rad = chord / 2 * 1.08
    d = f"M{pts[0][0]:.2f} {pts[0][1]:.2f}"
    for i in range(1, lobes + 1):
        x, y = pts[i % lobes]
        d += f" A{rad:.2f} {rad:.2f} 0 0 1 {x:.2f} {y:.2f}"
    return d + " Z"


def arch(w=100, h=100, pad=6):
    """Tombstone/arch plate — the 'UPLIFT EACH OTHER' shape."""
    x0, x1 = pad, w - pad
    y1 = h - pad
    r = (x1 - x0) / 2
    yt = pad + r
    return (f"M{x0:.2f} {y1:.2f} L{x0:.2f} {yt:.2f} "
            f"A{r:.2f} {r:.2f} 0 0 1 {x1:.2f} {yt:.2f} L{x1:.2f} {y1:.2f} Z")


def wave_banner(w=100, h=44, waves=1.5, amp=7):
    """Ribbon whose top and bottom edges undulate — the 'PRESENTATION' banner."""
    steps = 40
    top = []
    for i in range(steps + 1):
        t = i / steps
        x = t * w
        y = amp + amp * math.sin(t * waves * 2 * math.pi)
        top.append((x, y))
    bot = [(x, y + (h - 2 * amp)) for x, y in reversed(top)]
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in top)
    d += " L" + " L".join(f"{x:.2f} {y:.2f}" for x, y in bot)
    return d + " Z"


def blob(seed=1, lobes=7, r=44, wobble=0.18):
    """Organic rounded blob — smooth, NOT a polygon. Uses quadratic beziers through midpoints."""
    import random
    rnd = random.Random(seed)
    cx = cy = 50
    pts = []
    for i in range(lobes):
        a = 2 * math.pi * i / lobes
        rr = r * (1 + rnd.uniform(-wobble, wobble))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = ""
    for i in range(lobes):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % lobes]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        if i == 0:
            d += f"M{mx:.2f} {my:.2f}"
        nx, ny = pts[(i + 1) % lobes]
        mx2, my2 = (nx + pts[(i + 2) % lobes][0]) / 2, (ny + pts[(i + 2) % lobes][1]) / 2
        d += f" Q{nx:.2f} {ny:.2f} {mx2:.2f} {my2:.2f}"
    return d + " Z"


def starburst(points=10, R=48, r=30):
    """Spiky badge — sharper than doodles.burst, parametric point count."""
    cx = cy = 50
    p = []
    for i in range(points * 2):
        a = -math.pi / 2 + i * math.pi / points
        rad = R if i % 2 == 0 else r
        p.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in p) + " Z"


def gear(teeth=8, R=46, r=34):
    """Gear with flat-topped trapezoidal teeth and arced valleys (the reference form).
    doodles.py has square nubs; the first version here produced pointed spikes because the
    tooth top had no flat span — the two flank points met at a single angle."""
    cx = cy = 50
    step = 2 * math.pi / teeth
    def P(ang, rad):
        return (cx + rad * math.cos(ang), cy + rad * math.sin(ang))
    d = ""
    for i in range(teeth):
        a0 = i * step                 # valley start
        aA = a0 + step * 0.18         # flank up
        aB = a0 + step * 0.40         # tooth top ends (flat span aA..aB)
        aC = a0 + step * 0.58         # flank down
        p0, pA, pB, pC = P(a0, r), P(aA, R), P(aB, R), P(aC, r)
        pN = P(a0 + step, r)
        if i == 0:
            d += f"M{p0[0]:.2f} {p0[1]:.2f}"
        d += (f" L{pA[0]:.2f} {pA[1]:.2f}"
              f" A{R:.2f} {R:.2f} 0 0 1 {pB[0]:.2f} {pB[1]:.2f}"
              f" L{pC[0]:.2f} {pC[1]:.2f}"
              f" A{r:.2f} {r:.2f} 0 0 1 {pN[0]:.2f} {pN[1]:.2f}")
    return d + " Z"


def capsule(w=100, h=40):
    r = h / 2
    return (f"M{r:.2f} 0 L{w-r:.2f} 0 A{r:.2f} {r:.2f} 0 0 1 {w-r:.2f} {h:.2f} "
            f"L{r:.2f} {h:.2f} A{r:.2f} {r:.2f} 0 0 1 {r:.2f} 0 Z")


def shield(w=100, h=100):
    return (f"M8 10 L{w-8:.2f} 10 L{w-8:.2f} {h*0.55:.2f} "
            f"Q{w-8:.2f} {h-10:.2f} {w/2:.2f} {h-6:.2f} "
            f"Q8 {h-10:.2f} 8 {h*0.55:.2f} Z")


def tag(w=100, h=44, notch=14):
    return (f"M0 {h/2:.2f} L{notch:.2f} 0 L{w-6:.2f} 0 A6 6 0 0 1 {w:.2f} 6 "
            f"L{w:.2f} {h-6:.2f} A6 6 0 0 1 {w-6:.2f} {h:.2f} L{notch:.2f} {h:.2f} Z")


SILHOUETTES = {"scallop": scallop, "arch": arch, "wave_banner": wave_banner, "blob": blob,
               "starburst": starburst, "gear": gear, "capsule": capsule, "shield": shield,
               "tag": tag}


# ── interior detail (what lifts detail_ratio out of the 'flat blob' zone) ──────
def motion_lines(x, y, n=3, length=14, gap=7, rot=-20, color=INK, w=4):
    """Short speed ticks — the marks beside the reference's OK-hand. Cheap, high detail-per-pixel."""
    out = []
    for i in range(n):
        yy = y + i * gap
        out.append(f'<line x1="{x}" y1="{yy}" x2="{x+length}" y2="{yy}" stroke="{color}" '
                   f'stroke-width="{w}" stroke-linecap="round" transform="rotate({rot} {x} {yy})"/>')
    return "".join(out)


def hatch(x, y, w, h, step=8, color=INK, sw=2.5, angle=45):
    """Diagonal hatching inside a region — adds internal linework without new silhouettes."""
    lines = []
    n = int((w + h) / step)
    for i in range(n):
        o = i * step
        lines.append(f'<line x1="{x+o}" y1="{y}" x2="{x+o-h}" y2="{y+h}" stroke="{color}" '
                     f'stroke-width="{sw}" stroke-linecap="round"/>')
    return (f'<g clip-path="url(#clip{int(x)}{int(y)})"><clipPath id="clip{int(x)}{int(y)}">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>{"".join(lines)}</g>')


# ── THE UNIFIER ────────────────────────────────────────────────────────────────
_UID = [0]


def _next_uid():
    _UID[0] += 1
    return _UID[0]


def interior(path_d, kind="inner", box=100, color=INK, fill=None, uid=None):
    """Interior linework for a silhouette — the fix for the persistent `DETAIL TOO LOW` critique.

    compare.py measures DETAIL as edge energy per unit of content. Reference stickers carry
    internal structure (die-cut inner lines, keyboard keys, knuckle creases, halftone screens);
    AQ shapes were flat fills with a single outline, so they measured 0.48-0.76x the reference
    across every showcase batch. Interior marks raise edge-per-pixel WITHOUT adding new objects,
    which is the only way to close that gap without also breaking the density measurements.

    kinds:
      inner  — a concentric inset outline (the die-cut sticker's second line). Works on ANY
               silhouette because it is just the same path scaled about its centre.
      dots   — halftone screen clipped to the shape
      hatch  — diagonal rule fill clipped to the shape
      both   — inner + dots
    """
    u = uid if uid is not None else _next_uid()
    c = box / 2
    out = []
    if kind in ("inner", "both"):
        out.append(f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="2.6" '
                   f'opacity=".55" stroke-linejoin="round" '
                   f'transform="translate({c},{c}) scale(0.78) translate({-c},{-c})"/>')
    if kind in ("dots", "hatch", "both"):
        marks = []
        if kind in ("dots", "both"):
            step = 11
            for r in range(0, int(box) + step, step):
                for cc in range(0, int(box) + step, step):
                    off = (step // 2) if (r // step) % 2 else 0
                    marks.append(f'<circle cx="{cc+off}" cy="{r}" r="1.9" fill="{color}" opacity=".38"/>')
        else:
            for i in range(-int(box), int(box) * 2, 9):
                marks.append(f'<line x1="{i}" y1="0" x2="{i - box}" y2="{box}" stroke="{color}" '
                             f'stroke-width="2" opacity=".34" stroke-linecap="round"/>')
        out.append(f'<clipPath id="ip{u}"><path d="{path_d}"/></clipPath>'
                   f'<g clip-path="url(#ip{u})">{"".join(marks)}</g>')
    return "".join(out)


def sticker(path_d, fill, size=120, halo=True, shadow=False, rot=0, box=100,
            inner="", outline=INK, sw=SW, halo_amt=0.55, halo_w=HALO, detail="inner"):
    """Wrap a silhouette in the uniform AQ sticker treatment.

    Drawing order IS the treatment:
      1. the same path stroked fat in a TINT of its own fill  -> the die-cut halo
      2. optional hard ink offset shadow
      3. the path itself, filled, with the ink outline
      4. any interior detail (`inner` raw SVG, in the same 0..box coords)

    This is the rule that makes a dense pile of unrelated colours read as one set
    (VISUAL_DNA.md §1). Apply it to EVERY object in a piece, uniformly — the uniformity is
    the point, not the outline.
    """
    halo_col = lighten(fill, halo_amt)
    parts = []
    if shadow:
        parts.append(f'<path d="{path_d}" fill="{outline}" transform="translate(4,5)"/>')
    if halo:
        parts.append(f'<path d="{path_d}" fill="{halo_col}" stroke="{halo_col}" '
                     f'stroke-width="{halo_w}" stroke-linejoin="round" stroke-linecap="round"/>')
    parts.append(f'<path d="{path_d}" fill="{fill}" stroke="{outline}" stroke-width="{sw}" '
                 f'stroke-linejoin="round"/>')
    # interior linework runs BY DEFAULT (detail="inner"). Flat fills were the cause of the
    # persistent DETAIL TOO LOW critique; making detail opt-OUT rather than opt-in means every
    # object carries reference-grade structure without the caller having to remember.
    if detail and detail != "none":
        parts.append(interior(path_d, detail, box=box, color=outline))
    if inner:
        parts.append(inner)
    pad = halo_w if halo else sw
    vb = f"{-pad} {-pad} {box + 2*pad} {box + 2*pad}"
    return (f'<svg viewBox="{vb}" width="{size}" height="{size}" '
            f'style="transform:rotate({rot}deg);overflow:visible" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(parts)}</svg>')


def text_on_arc(text, r=34, size=13, fill="#FFFFFF", box=100, start="0%", weight=800, uid=None):
    """Text following a circular path — the reference's 'GO TEAM! GO TEAM!' ring.
    Uses a real SVG textPath so the text CANNOT clip off the ring the way a rotated div does
    (that clipping was a visible defect in the c42f94 v2 recreation).

    startOffset MUST be a percentage string. Passing a bare number means USER UNITS: the first
    version passed 180 against a ~188px circumference, so the whole string was pushed to the very
    end of the path and rendered as one visible glyph. Percentages are circumference-relative and
    stay correct at any radius.
    """
    cx = cy = box / 2
    pid = f"arc{uid if uid is not None else abs(hash(text)) % 100000}"
    d = (f"M{cx-r:.2f} {cy:.2f} A{r:.2f} {r:.2f} 0 1 1 {cx+r:.2f} {cy:.2f} "
         f"A{r:.2f} {r:.2f} 0 1 1 {cx-r:.2f} {cy:.2f}")
    if isinstance(start, (int, float)):
        start = f"{start}%"
    return (f'<defs><path id="{pid}" d="{d}" fill="none"/></defs>'
            f'<text font-weight="{weight}" font-size="{size}" fill="{fill}" letter-spacing="1">'
            f'<textPath href="#{pid}" xlink:href="#{pid}" startOffset="{start}">{text}</textPath>'
            f'</text>')


def word_boxes(words, accents, fs=76, gap=14, tilt=3, x=0, y=0, text_on=None):
    """VISUAL_DNA §4 — the biggest structural gap: the engine sets TEXT BLOCKS, the references
    design individual WORDS. Boxes each word in its own tightly-hugging accent rectangle, each
    tilted alternately and horizontally staggered. The MISREGISTRATION is the whole effect
    (seen in d252704dc5, d375fd7dbc, eaad68d630).
    Returns absolutely-positioned HTML; caller supplies x,y as the block origin."""
    out, cy = [], y
    for i, w in enumerate(words):
        acc = accents[i % len(accents)]
        fg = text_on(acc) if text_on else "#FFFFFF"
        rot = tilt if i % 2 == 0 else -tilt
        off = x + (i % 3) * 26            # stagger, so boxes never stack flush
        out.append(
            f'<div style="position:absolute;left:{off}px;top:{cy}px;display:inline-block;'
            f'background:{acc};color:{fg};border:5px solid {INK};padding:10px 26px;'
            f'box-shadow:8px 8px 0 {INK};font-family:var(--d),sans-serif;font-weight:900;'
            f'font-size:{fs}px;line-height:1;text-transform:uppercase;white-space:nowrap;'
            f'transform:rotate({rot}deg);z-index:{20+i}">{w}</div>')
        cy += fs + gap + 18
    return "".join(out)


def checker(w, h, cell=44, c1="#0A0A0A", c2="#FFFFFF", opacity=1.0):
    """Procedural checkerboard field fill — a pattern primitive the engine lacked entirely
    (quadrant_patchwork, d252704dc5). Cheap density that is a FIELD, not scattered objects."""
    rects = []
    for r in range(int(h // cell) + 1):
        for c in range(int(w // cell) + 1):
            if (r + c) % 2 == 0:
                rects.append(f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="{c2}"/>')
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="opacity:{opacity}" '
            f'xmlns="http://www.w3.org/2000/svg"><rect width="{w}" height="{h}" fill="{c1}"/>'
            f'{"".join(rects)}</svg>')


def extrude(path_d, fill, depth=14, size=120, box=100, shade="#0A0A0A", rot=0):
    """Fixed-direction extruded slab shadow — the move that makes a flat SVG scatter read as a
    coherent 3D set (11e7d9a3ff keycaps; top steal of batch 1). Same offset for EVERY object."""
    layers = "".join(f'<path d="{path_d}" fill="{shade}" transform="translate({i},{i})"/>'
                     for i in range(depth, 0, -1))
    return (f'<svg viewBox="-8 -8 {box+depth+16} {box+depth+16}" width="{size}" height="{size}" '
            f'style="transform:rotate({rot}deg);overflow:visible" xmlns="http://www.w3.org/2000/svg">'
            f'{layers}<path d="{path_d}" fill="{fill}" stroke="{INK}" stroke-width="{SW}" '
            f'stroke-linejoin="round"/></svg>')


def label(text, size=13, y=52, box=100, fill=INK, weight=800, anchor="middle"):
    return (f'<text x="{box/2}" y="{y}" text-anchor="{anchor}" font-family="var(--d), sans-serif" '
            f'font-weight="{weight}" font-size="{size}" fill="{fill}">{text}</text>')
