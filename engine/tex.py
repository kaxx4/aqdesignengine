# ════════════════════════════════════════════════════════════════════════════
# AQ ENGINE — tex: the texture vocabulary
# ════════════════════════════════════════════════════════════════════════════
# Texture is part of an element's CONSTRUCTION, not a layer smeared over the
# finished piece. Every function here returns either a CSS `background` fragment
# you put INSIDE a shape's own style, or a complete element that is itself the
# textured thing. None of them are page-wide overlays.
#
# THE ONE RULE THAT GOVERNS THIS FILE — learned the hard way on `friendship_day`:
#   Decoration is SOLID. A faint (~.13-.26 alpha) hatch/ring/checker spread
#   across a field does not read as texture, it reads as DIRT, and it smears
#   through any body copy sitting on it. If you want a texture to be seen, give
#   it real contrast and let it live inside a shape with an edge. If it has to
#   be whispered to be tolerable, it does not belong in the piece.
#   layout.wash_scan() now enforces this; see §10 of CLAUDE.md.
#
# The legitimate places texture goes, in priority order:
#   1. INSIDE a photo        — halftone / duotone / riso. Always allowed.
#   2. INSIDE a solid slab   — as a full-contrast pattern, edge-to-edge in that
#                              slab, never bleeding under unrelated body copy.
#   3. ON the page ground    — grain / fibre only, and only at the ground level.
#   4. As a physical object  — tape, torn edge, curled corner. Solid, outlined.

import hashlib

INK   = "#0A0A0A"
CREAM = "#F4EFE0"

def _uid(*parts):
    return "t" + hashlib.md5("|".join(str(p) for p in parts).encode()).hexdigest()[:8]

def _esc(svg):
    """Inline an SVG into a css url() — the characters that actually break it."""
    return (svg.replace("#", "%23").replace("<", "%3C").replace(">", "%3E")
               .replace('"', "'").replace("\n", "").replace("  ", " "))

# ── 3. PAGE GROUND ──────────────────────────────────────────────────────────

def grain(opacity=0.06, freq=0.8, octaves=2, size=240):
    """Fractal-noise grain. The parameterised form of core.GRAIN, which was a
    frozen string — so every piece in the corpus carried IDENTICAL grain and
    nothing could be dialled per piece. Returns a `background-image:` fragment;
    pair with `mix-blend-mode:multiply` on an ::after or a stacked div."""
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}'>"
           f"<filter id='n'><feTurbulence baseFrequency='{freq}' numOctaves='{octaves}'/></filter>"
           f"<rect width='100%' height='100%' filter='url(%23n)' opacity='{opacity}'/></svg>")
    return f'background-image:url("data:image/svg+xml,{_esc(svg)}")'

def paper_fibre(opacity=0.05, color=INK):
    """Directional fibre — a laid-paper stock rather than TV static. Reads as
    the cream having a grain direction. Ground level only."""
    return (f"background-image:"
            f"repeating-linear-gradient(97deg,{color}00 0 3px,{color}{_a(opacity)} 3px 4px),"
            f"repeating-linear-gradient(4deg,{color}00 0 7px,{color}{_a(opacity*0.6)} 7px 8px)")

def _a(opacity):
    """0..1 -> two-digit hex alpha suffix."""
    return f"{max(0, min(255, round(opacity * 255))):02x}"

# ── 1. INSIDE A PHOTO ───────────────────────────────────────────────────────

def halftone(color=INK, size=6, opacity=0.5, angle=0):
    """A real dot screen. HOUSE RULE: halftone belongs on PHOTOS and on shaded
    panels — never scattered across a flat brand colour, where it just muddies
    the hue. Returns a background fragment to stack over an image."""
    rot = f"transform:rotate({angle}deg);" if angle else ""
    return (f"background-image:radial-gradient({color}{_a(opacity)} 1.1px,transparent 1.5px);"
            f"background-size:{size}px {size}px;{rot}")

def duotone(src, shadow="#0A0A0A", highlight="#FF4D8C", size_css="width:100%;height:100%",
            screen=True, screen_size=5, radius="0", extra=""):
    """Two-plate riso photo: the image's darks become `shadow`, its lights
    become `highlight`. Implemented as grayscale + a highlight plate under a
    multiply shadow plate, which keeps real photographic detail instead of the
    flat posterise you get from a single tint wash.

    This replaced riso_photo_wrap's single-tint-at-.55 approach, which pushed
    every photo toward one muddy mid-tone and lost the faces."""
    scr = (f'<div style="position:absolute;inset:0;{halftone(shadow, screen_size, 0.33)}'
           f'mix-blend-mode:multiply"></div>') if screen else ""
    return (f'<div style="position:relative;overflow:hidden;{size_css};border-radius:{radius};{extra}">'
            f'<div style="position:absolute;inset:0;background:{highlight}"></div>'
            f'<img src="{src}" style="position:absolute;inset:0;width:100%;height:100%;'
            f'object-fit:cover;filter:grayscale(1) contrast(1.25) brightness(1.08);'
            f'mix-blend-mode:multiply">'
            f'<div style="position:absolute;inset:0;background:{shadow};mix-blend-mode:lighten;'
            f'opacity:.18"></div>{scr}</div>')

def photo_ink(src, size_css="width:100%;height:100%", contrast=1.35, radius="0", extra=""):
    """High-contrast black-ink photo — the newsprint/zine treatment. One colour,
    maximum bite. Use when a photo must sit beside flat brand colour without
    competing with it."""
    return (f'<div style="position:relative;overflow:hidden;{size_css};border-radius:{radius};{extra}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;'
            f'filter:grayscale(1) contrast({contrast}) brightness(1.02)">'
            f'<div style="position:absolute;inset:0;{halftone(INK, 5, 0.28)}'
            f'mix-blend-mode:multiply"></div></div>')

# ── 2. INSIDE A SOLID SLAB ──────────────────────────────────────────────────
# All of these are FULL-CONTRAST by default. The opacity arguments exist so a
# caller can tune within a slab, not so they can be whispered to .15 across the
# whole page — wash_scan() will catch that.

def stripes(color=INK, bg=None, width=10, gap=10, angle=45, opacity=1.0):
    """Hard diagonal bars. The classic AQ caution-tape / awning field."""
    base = f"background-color:{bg};" if bg else ""
    return (f"{base}background-image:repeating-linear-gradient({angle}deg,"
            f"{color}{_a(opacity)} 0 {width}px,transparent {width}px {width+gap}px)")

def crosshatch(color=INK, step=9, width=2, opacity=1.0):
    """Two hatch angles crossing — engraving shade. Solid lines, not a wash."""
    a = _a(opacity)
    return (f"background-image:"
            f"repeating-linear-gradient(45deg,{color}{a} 0 {width}px,transparent {width}px {step}px),"
            f"repeating-linear-gradient(-45deg,{color}{a} 0 {width}px,transparent {width}px {step}px)")

def dot_grid(color=INK, size=18, dot=3, opacity=1.0):
    """Regular dot lattice — graph-paper/pegboard. Reads as structure."""
    return (f"background-image:radial-gradient({color}{_a(opacity)} {dot/2}px,transparent {dot/2+0.6}px);"
            f"background-size:{size}px {size}px")

def grid_lines(color=INK, step=40, width=2, opacity=1.0):
    """Ruled grid — the engineering/ledger field."""
    a = _a(opacity)
    return (f"background-image:"
            f"repeating-linear-gradient(0deg,{color}{a} 0 {width}px,transparent {width}px {step}px),"
            f"repeating-linear-gradient(90deg,{color}{a} 0 {width}px,transparent {width}px {step}px)")

def checkerboard(c1=INK, c2=CREAM, cell=28):
    """Hard checker. Solid by construction — there is no faint version."""
    return (f"background-color:{c2};background-image:"
            f"linear-gradient(45deg,{c1} 25%,transparent 25%,transparent 75%,{c1} 75%),"
            f"linear-gradient(45deg,{c1} 25%,transparent 25%,transparent 75%,{c1} 75%);"
            f"background-size:{cell*2}px {cell*2}px;"
            f"background-position:0 0,{cell}px {cell}px")

def rays(color=INK, n=12, opacity=1.0, from_="50% 50%"):
    """Sunburst wedges radiating from a point. A field, not a doodle."""
    step = 360 / n
    stops = []
    for i in range(n):
        a0, a1 = i * step, i * step + step / 2
        stops.append(f"{color}{_a(opacity)} {a0}deg {a1}deg")
        stops.append(f"transparent {a1}deg {a0+step}deg")
    return f"background-image:conic-gradient(from 0deg at {from_},{','.join(stops)})"

def concentric(color=INK, step=26, width=6, opacity=1.0, at="50% 50%"):
    """Ripple rings — the AquaTerra water motif as a field."""
    a = _a(opacity)
    return (f"background-image:repeating-radial-gradient(circle at {at},"
            f"{color}{a} 0 {width}px,transparent {width}px {step}px)")

# ── riso misregistration ────────────────────────────────────────────────────

def riso_offset(inner_html, dx=6, dy=6, plate="#FF4D8C", opacity=0.9):
    """The riso signature: a second colour plate printed slightly off-register.
    Wraps any markup and prints a displaced, single-colour ghost of it behind
    the original. This is SOLID colour offset — it is texture you can see from
    across a room, which is the whole point. Pass the same markup you're about
    to place; the ghost inherits its silhouette."""
    uid = _uid(inner_html[:120], dx, dy, plate)
    return (f'<div style="position:relative" data-riso="{uid}">'
            f'<div style="position:absolute;left:{dx}px;top:{dy}px;'
            f'filter:brightness(0) saturate(100%);opacity:{opacity};'
            f'mix-blend-mode:multiply;background:{plate};'
            f'-webkit-mask-image:none">{inner_html}</div>'
            f'<div style="position:relative">{inner_html}</div></div>')

# ── 4. PHYSICAL OBJECTS ─────────────────────────────────────────────────────

def tape(x, y, w=150, h=44, rot=-6, color="#F2E9C9", z=30, opacity=0.92):
    """A strip of masking tape. Torn ends via clip-path, a hairline edge so it
    reads as a physical object, and it is deliberately opaque — see-through
    tape is the faint-wash bug wearing a costume."""
    clip = ("polygon(0% 12%,4% 0%,10% 9%,17% 1%,24% 10%,32% 2%,40% 11%,48% 3%,56% 12%,"
            "64% 4%,72% 12%,80% 3%,88% 11%,95% 2%,100% 10%,100% 90%,95% 99%,88% 89%,"
            "80% 98%,72% 88%,64% 97%,56% 88%,48% 98%,40% 89%,32% 98%,24% 90%,17% 99%,"
            "10% 91%,4% 100%,0% 88%)")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{color};opacity:{opacity};transform:rotate({rot}deg);'
            f'clip-path:{clip};z-index:{z};'
            f'box-shadow:inset 0 0 0 1px rgba(10,10,10,.10)"></div>')

TORN_TOP = ("polygon(0% 6%,6% 0%,13% 7%,21% 1%,29% 8%,37% 2%,45% 8%,53% 1%,61% 7%,"
            "69% 2%,77% 8%,85% 1%,92% 7%,100% 2%,100% 100%,0% 100%)")
TORN_BOTTOM = ("polygon(0% 0%,100% 0%,100% 94%,92% 100%,85% 93%,77% 99%,69% 92%,61% 98%,"
               "53% 92%,45% 99%,37% 93%,29% 98%,21% 92%,13% 99%,6% 93%,0% 98%)")

def torn(edge="top"):
    """Torn-paper edge as a clip-path fragment. `edge` in top|bottom."""
    return f"clip-path:{TORN_TOP if edge == 'top' else TORN_BOTTOM}"

def cutpaper(x, y, w, h, col, rot=0, z=3, shadow=14, radius="0", texture=None,
             outline=None):
    """A flat cut-paper shape: solid fill, an optional in-fill texture, a hard
    flat drop (never a blur), and an optional ink edge.

    `texture` takes any background fragment from this module — that is the
    supported way to get a textured field: inside a shape with an edge, not
    loose on the page."""
    tex = f"{texture};" if texture else ""
    edge = f"box-shadow:{shadow}px {shadow}px 0 rgba(10,10,10,.22),inset 0 0 0 3px {outline};" \
        if outline else f"box-shadow:{shadow}px {shadow}px 0 rgba(10,10,10,.22);"
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{w}px;height:{h}px;'
            f'background-color:{col};{tex}border-radius:{radius};'
            f'transform:rotate({rot}deg);z-index:{z};{edge}"></div>')

# ── legacy shims ────────────────────────────────────────────────────────────
# Kept because 44 recreations import them. halftone_fill returning a FLAT fill
# is not a bug — it is the standing house ruling that flat brand colour stays
# flat — but the name lies, so it is documented here rather than left to be
# rediscovered. New work should call the named function it actually wants.

def halftone_fill(base, dot=INK, size=9, dot_op=0.06, angle=0):
    """DEPRECATED NAME, CORRECT BEHAVIOUR: returns a FLAT fill. House rule is no
    halftone on solid brand colour. For a genuinely textured slab use
    cutpaper(..., texture=crosshatch()) or one of the field functions."""
    return f"background-color:{base};"

def halftone_gradient(base, dot=INK, size_from=6, size_to=16):
    """Graduated halftone for shaded panels."""
    return (f"background-color:{base};"
            f"background-image:radial-gradient({dot} 30%, transparent 32%);"
            f"background-size:{size_from}px {size_from}px;")

def riso_photo(src, tint="#1B3A8A", mix="multiply", contrast=1.15):
    """Legacy: style-body string for a grayscale photo."""
    return f"width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast({contrast});"

def riso_photo_wrap(src, tint, size_css, extra=""):
    """Legacy single-tint riso. Prefer duotone(), which keeps the faces."""
    return (f'<div style="position:relative;{size_css};overflow:hidden;{extra}">'
            f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;'
            f'filter:grayscale(1) contrast(1.2) brightness(1.05)">'
            f'<div style="position:absolute;inset:0;background:{tint};'
            f'mix-blend-mode:multiply;opacity:.55"></div>'
            f'<div style="position:absolute;inset:0;'
            f'background-image:radial-gradient(#00000055 1.2px,transparent 1.6px);'
            f'background-size:5px 5px;mix-blend-mode:multiply;opacity:.4"></div></div>')

# What a caller can ask for by name, for the director/archetype layer.
FIELDS = {
    "stripes": stripes, "crosshatch": crosshatch, "dot_grid": dot_grid,
    "grid_lines": grid_lines, "checkerboard": checkerboard, "rays": rays,
    "concentric": concentric,
}

def field(name, **kw):
    """Look up a field texture by name. Unknown name -> no texture (never a
    guess), so a typo degrades to a flat slab instead of a surprise pattern."""
    fn = FIELDS.get(name)
    return fn(**kw) if fn else ""
