"""AQ ENGINE — core: brand tokens, embedded fonts, shared render helpers.
This is the single source for CSS tokens + fonts. build.py imports from here.
Nothing here is 'enforced per piece' — these are the raw materials only.
"""
import base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
def _b64(path, mime):
    with open(os.path.join(HERE, path), "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

# ---- real assets (never fake these) ----
LOGO   = _b64("assets/logo.png", "image/png")                       # real colored wordmark
PHOTOS = {
    "food":     _b64("assets/img/food-distribution.jpeg", "image/jpeg"),
    "edu":      _b64("assets/img/education-sundarban.jpeg", "image/jpeg"),
    "diwali":   _b64("assets/img/fundraising-diwali.jpeg", "image/jpeg"),
    "xmas":     _b64("assets/img/christmas-khidirpur.jpeg", "image/jpeg"),
}

# ---- embedded font-face block ----
FONTS = f"""
@font-face{{font-family:'NeutralFace';src:url('{_b64("assets/fonts/NeutralFace-Bold.otf","font/otf")}') format('opentype');font-weight:700 900}}
@font-face{{font-family:'NeutralFace';src:url('{_b64("assets/fonts/NeutralFace.otf","font/otf")}') format('opentype');font-weight:400}}
@font-face{{font-family:'Eina01';src:url('{_b64("assets/fonts/Eina01-Regular.ttf","font/ttf")}') format('truetype');font-weight:400}}
@font-face{{font-family:'Eina01';src:url('{_b64("assets/fonts/Eina02-SemiBold.ttf","font/ttf")}') format('truetype');font-weight:600}}
@font-face{{font-family:'Instrument Serif';src:url('{_b64("assets/fonts/InstrumentSerif-Italic.ttf","font/ttf")}') format('truetype');font-style:italic}}
@font-face{{font-family:'Instrument Serif';src:url('{_b64("assets/fonts/InstrumentSerif-Regular.ttf","font/ttf")}') format('truetype')}}
@font-face{{font-family:'JetBrains Mono';src:url('{_b64("assets/fonts/JetBrainsMono-Bold.ttf","font/ttf")}') format('truetype');font-weight:700}}
@font-face{{font-family:'JetBrains Mono';src:url('{_b64("assets/fonts/JetBrainsMono-Medium.ttf","font/ttf")}') format('truetype');font-weight:500}}
"""

# ---- brand tokens (the LAW — do not invent colors) ----
ROOT = """:root{
--bg:#F4EFE0;--bg2:#EDE6D0;--ink:#0A0A0A;--ink2:#1A1A18;--ink3:#5A5A55;
--pink:#FF4D8C;--mint:#1B8A5A;--lemon:#FFC700;--tomato:#FF4D2E;--sky:#3DA9FC;--grape:#7E5BFF;--teal:#0E7C86;--mintbright:#00E5A0;
--d:'NeutralFace',sans-serif;--e:'Eina01',sans-serif;--s:'Instrument Serif',serif;--m:'JetBrains Mono',monospace}"""

# 7 accents for free rotation (pink is default shout; teal is the 7th, canon)
ACCENTS = ["#FF4D8C","#1B8A5A","#FFC700","#FF4D2E","#3DA9FC","#7E5BFF","#0E7C86"]
# ink text required on these light accents; white text on the rest
INK_ON = {"#FFC700","#3DA9FC","#00E5A0"}

GRAIN = ("background-image:url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
         "width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.8' numOctaves='2'/%3E%3C/filter%3E"
         "%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.06'/%3E%3C/svg%3E\")")

# ---- canvas sizes ----
SIZES = {
    "feed":     (1080, 1350),   # Instagram portrait — the default
    "story":    (1080, 1920),   # IG/FB story
    "square":   (1080, 1080),   # IG square
    # LinkedIn, added session 10. LI crops portrait hard in-feed, so AQ's
    # LinkedIn art is landscape or square, never 4:5.
    "linkedin": (1200,  628),   # LI link/feed landscape (1.91:1)
    "li_square":(1200, 1200),   # LI square — the one that survives mobile best
}

# ════════════════════════════════════════════════════════════════════════════
# CONTRAST — measured, never guessed  (session 10)
# ════════════════════════════════════════════════════════════════════════════
# History: text_on() used to read a hand-kept INK_ON set and returned WHITE for
# pink/mint/tomato/grape. Measured against WCAG, that was wrong on all four —
# white on pink #FF4D8C is 3.14:1, which FAILS AA for normal text, while ink on
# the same pink is 6.31:1. The live site (frontend/src/styles/tokens.css) had
# already resolved this ("--on-pink: var(--ink) — the display hue PASSES"); the
# poster engine never got the memo and had been shipping the failing pairing.
# The fix is not a corrected lookup table (tables drift) — it is to MEASURE.

def _rel_lum(hex_color):
    """WCAG 2.x relative luminance of an #RRGGBB string."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def contrast(a, b):
    """WCAG contrast ratio between two #RRGGBB colors. 1.0 … 21.0"""
    l1, l2 = sorted((_rel_lum(a), _rel_lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

AA_NORMAL = 4.5   # body/label text — the floor that matters for posters
AA_LARGE  = 3.0   # >=24px bold display type

def text_on(fill_hex, large=False):
    """Correct text colour for type placed ON `fill_hex`, DECIDED BY MEASUREMENT.

    Returns whichever of ink / paper-white scores higher contrast, so it is
    right for any colour — including ones not in ACCENTS. `large=True` only
    relaxes the reporting floor, never the choice."""
    if not isinstance(fill_hex, str) or not fill_hex.startswith("#"):
        return INK                      # unknown/gradient/var() -> safest default
    ci, cw = contrast(INK, fill_hex), contrast(PAPER, fill_hex)
    return INK if ci >= cw else PAPER

def text_on_passes(fill_hex, large=False):
    """True when the BEST available text colour on `fill_hex` clears the AA floor.
    Some brand fills simply cannot carry small type — this reports that honestly
    instead of returning a colour and pretending it is legible."""
    if not isinstance(fill_hex, str) or not fill_hex.startswith("#"):
        return True
    best = max(contrast(INK, fill_hex), contrast(PAPER, fill_hex))
    return best >= (AA_LARGE if large else AA_NORMAL)

INK   = "#0A0A0A"
PAPER = "#FFFFFF"
CREAM = "#F4EFE0"

# ── Accent ink variants ──────────────────────────────────────────────────────
# MEASURED FACT: not one of the seven accents clears 4.5:1 as TEXT on the cream
# page ground (best is teal at 4.30, worst is lemon at 1.36). So accent-coloured
# small type on cream is ALWAYS illegible — a defect the engine had no guard for.
# These darkened partners all clear 4.5:1 on both cream and white; they are the
# only accent values allowed for type sitting on the page. Values carried over
# from the live site's tokens.css so poster and web stay one system.
ACCENT_INK = {
    "#FF4D8C": "#C4185C",   # pink   -> 5.03:1 on cream
    "#1B8A5A": "#146F47",   # mint   -> 5.38:1
    "#FFC700": "#7E6000",   # lemon  -> 5.13:1
    "#FF4D2E": "#C6300F",   # tomato -> 4.77:1
    "#3DA9FC": "#0B6BB8",   # sky    -> 4.80:1
    "#7E5BFF": "#6B44E8",   # grape  -> 5.05:1
    "#0E7C86": "#0E6E77",   # teal   -> 5.20:1
}

def _chan(hex_color):
    """(r,g,b) 0-255 from an #RGB or #RRGGBB string."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(a_hex, b_hex, t):
    """Blend a toward b by t (0..1) in sRGB. Hue-preserving enough for a tint ladder."""
    a, b = _chan(a_hex), _chan(b_hex)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lit_of(accent_hex, ground=None, floor=AA_NORMAL):
    """The LIGHTENED partner of an accent, for type on a DARK ground.

    The mirror of ink_of(). Computed, not tabulated, for the same reason contrast()
    is computed: a hand-kept table drifts, and this one would need an entry per
    (accent, ground) pair. Walks the accent toward PAPER in 5% steps and returns the
    FIRST tint that clears the floor — the smallest change that does the job, so the
    hue stays recognisably the department's colour.

    Returns the accent unchanged when it already passes, or when no tint can pass
    (a caller that needs to know should ask contrast() directly).
    """
    ground = ground or INK
    if not isinstance(accent_hex, str) or not accent_hex.startswith("#"):
        return accent_hex
    if contrast(accent_hex, ground) >= floor:
        return accent_hex
    for i in range(1, 21):
        cand = _mix(accent_hex, PAPER, i * 0.05)
        if contrast(cand, ground) >= floor:
            return cand
    return accent_hex


def on_ground(accent_hex, ground, size_px=16, bold=True):
    """The accent value that is ACTUALLY LEGIBLE as type on ANY ground.

    THE BUG THIS FIXES. on_cream() took a `ground=` argument — which invites exactly
    the call `on_cream(accent, 16, ground=INK)` for a dark-ground poster — but its
    only fallback was ink_of(), which DARKENS. On a dark ground that walks the wrong
    way, fails again, and hits the final `else INK` branch: the function returned
    #0A0A0A ON #0A0A0A, contrast 1.00:1, invisible. It was the catalog's oldest
    failure class ("drawn but invisible") emitted by the helper built to prevent it.

    So the direction of the fix is now chosen by MEASURING the ground rather than
    assumed to be "darker": darken on a light ground, lighten on a dark one. And the
    last-resort value is the neutral that actually WINS on that ground (text_on), not
    a hardcoded INK.
    """
    if not isinstance(accent_hex, str) or not accent_hex.startswith("#"):
        return accent_hex
    ground = ground or CREAM
    if not isinstance(ground, str) or not ground.startswith("#"):
        return accent_hex               # var()/gradient — never guess (same as text_on)
    floor = AA_LARGE if (bool(bold) and size_px >= 24) else AA_NORMAL
    if contrast(accent_hex, ground) >= floor:
        return accent_hex               # accents may shout
    # Which way is there room to move? Ask the ground, don't assume.
    partner = lit_of(accent_hex, ground, floor) if contrast(PAPER, ground) > contrast(INK, ground) \
        else ink_of(accent_hex)
    if contrast(partner, ground) >= floor:
        return partner
    return text_on(ground)              # the neutral that WINS here, never a fixed INK


def on_cream(accent_hex, size_px=16, bold=True, ground=None):
    """The accent value that is ACTUALLY LEGIBLE as type on the page ground.

    WCAG splits at "large text" (>=24px bold, or >=18.66px bold): the floor drops
    from 4.5:1 to 3.0:1. That split matters here, because it is the difference
    between the two true statements:
      * a 500px mint numeral on cream is 3.78:1 -> PASSES as display type, and a
        giant ink numeral would throw away the department colour for nothing;
      * a 20px mint label on the same cream is the SAME 3.78:1 and FAILS, which
        is the defect ink_of() exists to fix.
    So the rule is not "accents never touch the page" — it is "accents may shout
    but may not whisper". Returns the raw accent when it clears its own floor at
    that size, otherwise the darkened partner.

    Kept as the named entry point for the common case — the page ground is cream far
    more often than anything else, and `on_cream(a, 20)` reads better at a call site
    than `on_ground(a, CREAM, 20)`. It now DELEGATES, so the dark-ground branch cannot
    diverge from it again.
    """
    return on_ground(accent_hex, ground or CREAM, size_px=size_px, bold=bold)


def on_dark(accent_hex, size_px=16, bold=True, ground=None):
    """Type on the INK ground — the other half of the poster corpus.

    Named because a third of the style bank is dark-ground and every one of those
    builds needs this decision. Measured facts on #0A0A0A: teal is 4.00:1 and FAILS
    small type (so it gets tinted); mint and grape sit at 4.55:1 and just pass.
    """
    return on_ground(accent_hex, ground or INK, size_px=size_px, bold=bold)

def ink_of(accent_hex):
    """The legible partner of an accent, for TYPE ON THE PAGE GROUND.
    Falls back to the accent itself for non-palette colours (never invents one)."""
    return ACCENT_INK.get(accent_hex, accent_hex)

# ── Department semantics ─────────────────────────────────────────────────────
# The site assigns a FIXED hue per department (tokens.css --c-events/--c-welfare
# /--c-labs/--c-ops/--c-content). The poster engine used to rotate accents by an
# arbitrary index, so a welfare post could come out grape and an events post
# pink — visually fine, but it broke the one colour-code the audience is being
# taught everywhere else. A poster about a welfare workshop is MINT. Full stop.
DEPT = {
    "welfare": "#1B8A5A",   # mint   — site --c-welfare
    "events":  "#3DA9FC",   # sky    — site --c-events
    "labs":    "#FFC700",   # lemon  — site --c-labs
    "ops":     "#0E7C86",   # teal   — site --c-ops (see DRIFT note below)
    "content": "#7E5BFF",   # grape  — site --c-content
}
# DRIFT, recorded not silently reconciled: the site's --c-ops/--teal is #12909C,
# the engine's canon teal is #0E7C86. Changing ACCENTS[6] would restyle all 44
# recreations, so the engine keeps its own teal and maps ops onto it. Worth a
# deliberate decision later — see brain/DECISIONS.md.
DEPT_SITE_TEAL = "#12909C"

def accent_for(dept, fallback="#FF4D8C"):
    """Accent a piece MUST use, given its department. Unknown dept -> fallback."""
    return DEPT.get((dept or "").strip().lower(), fallback)

# ── Craft scales — one system with the site ──────────────────────────────────
# Both were previously ad-hoc per bespoke script, which is why offsets ranged
# 3-14px across the corpus with no intent behind the differences.
RADII   = {"tight": 14, "inner": 22, "outer": 32, "pill": 999}
# Concentric: an outer 32 box with 10px padding wants a 22 inner; 22 with 8 -> 14.
def radius_inside(outer_r, pad):
    """The child radius that stays concentric inside `outer_r` at `pad` inset."""
    return max(0, outer_r - pad)

SHADOWS = {"sm": 1.5, "base": 2, "lg": 3, "xl": 4, "pressed": 1}
def hard_shadow(size="base", color=INK):
    """The house hard-offset shadow. NEVER mix with a blur on the same element."""
    px = SHADOWS.get(size, 2)
    return f"{px}px {px}px 0 0 {color}"

def keyline(ring_bg=CREAM, ink=INK, gap=2, ring=2):
    """The sticker double-ring: a ground-coloured gap, then an ink ring, so the
    sticker reads as STUCK ON the surface rather than cut out of it. Site rule 4.
    `ring_bg` must be the colour of whatever the sticker actually sits on."""
    return f"0 0 0 {gap}px {ring_bg}, 0 0 0 {gap + ring}px {ink}"

def outline_of(surface_hex):
    """Outline colour for craft (ink lines / hard shadows) ON a given surface.
    On a dark/ink field an ink outline is invisible — that whole-craft-layer-
    vanishes bug (friendship_day) is why this is a function, not a constant."""
    if not isinstance(surface_hex, str) or not surface_hex.startswith("#"):
        return INK
    return INK if _rel_lum(surface_hex) > 0.22 else CREAM
