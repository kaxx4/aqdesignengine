"""AQ FRIENDSHIP DAY CAROUSEL v2 — 1080x1440, 8 slides.

WHAT v1's LOOKING GATE CAUGHT (every fix below is a response to something seen, not guessed):
  1. INK BORDER ON INK FIELD = INVISIBLE. The punch box's `border:7px solid ink` +
     `box-shadow:12px 12px 0 ink` vanished completely on the dark cover/closer — the craft layer
     silently deleted itself. -> outline colour is now a per-slide token (CREAM on dark, INK on
     cream) threaded through punch/sticker/chip. GENERAL BUG -> encoded in layout.py (see §8).
  2. FAINT FIELDS READ AS STAINS. rings/hatch/checker at .13-.26 opacity looked like dirt and
     smeared straight through body copy (v1_06 "asked," sat on a checker smudge). -> deleted the
     whole faint-field vocabulary. Decoration is now SOLID, outlined, and deliberate.
  3. DEAD LEFT + DEAD BOTTOM-RIGHT on every line slide. -> fixed four-quadrant skeleton:
     Q1 giant outline numeral, Q2 art panel bleeding off the right edge, Q3 text+punch,
     Q4 pink sticker cluster. No quadrant is left to chance.
  4. BROKEN ILLUSTRATIONS: the 0.5x lens stacked on top of its own screen scene (unreadable
     pile); the "banana peel" read as a yellow eye; the closer's tag sticker was a lumpy slab.
     -> all three redrawn.
  5. Heart on v1_06 bled off-canvas and collided with the arch. -> all art now lives INSIDE the
     panel bounds.

PALETTE (user directive, mid-build): blues + greens LEAD, pink is the constant highlight.
  -> punch box + panel rotate through sky/teal/mint/mintbright; PINK is the em() swipe and at
     least one solid element on EVERY slide. Consistency of the pink is the through-line.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); sh = load("shapes"); lay = load("layout")

W, H = 1080, 1440
M = 72
A = core.ACCENTS
INK = "#0A0A0A"; CREAM = "#F4EFE0"
PINK = A[0]                      # the constant highlight — present on every slide
SKY = A[4]; MINT = A[1]; TEAL = A[6]; LEMON = A[2]; MBRIGHT = "#00E5A0"
OUT = "out/versions/friendship_day"

# PALETTE RULING (2026-08-03): mint #1B8A5A and sky #3DA9FC are the two PRIMARY carriers and
# alternate slide to slide. Teal and mint-bright demote to small doodle accents only; lemon is a
# minor pop; pink never takes a panel — it is the constant highlight on every slide.
SLIDE_ACCENT = [MINT, MINT, SKY, MINT, SKY, MINT, SKY, SKY]
DARK = {0, 7}                    # ink-based bookends
TOTAL = 8

def outline_of(dark):
    """THE v1 FIX: on an ink field, ink outlines are invisible. Outline colour is a slide token."""
    return CREAM if dark else INK


# ══════════════════════════════════════════════════════════════════════════════
# FURNITURE
# ══════════════════════════════════════════════════════════════════════════════
def logo(dark=False, x=M, y=64, h=52):
    img = f'<img src="{core.LOGO}" style="height:{h}px;display:block">'
    if dark:
        return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:30;background:{CREAM};'
                f'border-radius:999px;padding:10px 22px">{img}</div>')
    return f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:30">{img}</div>'


def dots(active, dark=False, y=90):
    acc = SLIDE_ACCENT[active]
    idle = "rgba(244,239,224,.28)" if dark else "rgba(10,10,10,.18)"
    ring = outline_of(dark)
    out = f'<div style="position:absolute;top:{y}px;right:{M}px;z-index:30;display:flex;gap:9px;align-items:center">'
    for i in range(TOTAL):
        if i == active:
            out += (f'<span style="width:14px;height:14px;border-radius:50%;background:{acc};'
                    f'border:3px solid {ring}"></span>')
        else:
            out += f'<span style="width:9px;height:9px;border-radius:50%;background:{idle}"></span>'
    return out + "</div>"


def chip(txt, acc, dark=False, y=176, x=M):
    o = outline_of(dark); fg = core.text_on(acc)
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:25;font-family:var(--m);'
            f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;'
            f'color:{fg};background:{acc};border:3px solid {o};border-radius:999px;'
            f'padding:8px 18px;box-shadow:5px 5px 0 {o};display:inline-block">{txt}</div>')


def footer(dark=False):
    c = CREAM if dark else INK
    return (f'<div style="position:absolute;bottom:56px;left:{M}px;z-index:30;font-family:var(--m);'
            f'font-weight:700;font-size:16px;letter-spacing:.07em;color:{c}">@ngo.aquaterra</div>')


def punch(acc, y, x=M - 4, rot=-2.2, fs=76, txt="wish them", dark=False):
    """THE DRUMBEAT — identical treatment on all 8 slides, outline colour flips on dark fields."""
    o = outline_of(dark); fg = core.text_on(acc)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:26;display:inline-block;'
            f'background:{acc};color:{fg};border:7px solid {o};box-shadow:13px 13px 0 {o};'
            f'padding:12px 32px 17px;font-family:var(--d);font-weight:900;font-size:{fs}px;'
            f'line-height:1;text-transform:uppercase;letter-spacing:-.015em;white-space:nowrap;'
            f'transform:rotate({rot}deg)">{txt}</div>')


def em(t):
    """PINK, always — the one constant highlight across the whole carousel."""
    return (f'<span style="background:linear-gradient(to top,{PINK}59 0,{PINK}59 40%,transparent 40%);'
            f'box-decoration-break:clone;-webkit-box-decoration-break:clone">{t}</span>')


def body(txt, y, dark=False, fs=54, maxw=880, x=M):
    c = CREAM if dark else INK
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{maxw}px;z-index:25;'
            f'font-family:var(--e);font-weight:400;font-size:{fs}px;line-height:1.26;'
            f'letter-spacing:-.018em;color:{c}">{txt}</div>')


def numeral(n, acc, y=300, x=56, fs=200, dark=False):
    """Giant outline numeral — fills the left column that was dead on every v1 line slide.
    v2 BUG: at fs=310 the second digit was swallowed by the art panel, so it read as a broken
    orphan glyph ("0" + a sliver) rather than a number. Sized to fit the 56..292 strip WHOLE."""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:4;font-family:var(--d);'
            f'font-weight:900;font-size:{fs}px;line-height:.78;letter-spacing:-.05em;'
            f'color:transparent;-webkit-text-stroke:8px {acc};opacity:.75">{n:02d}</div>')


def panel(x, y, w, h, acc, rot=-1.4, dark=False, z=8, radius=44):
    """The art card — a solid, outlined, hard-shadowed plate that bleeds off the right edge.
    Replaces v1's faint background washes: real colour mass instead of a stain."""
    o = outline_of(dark)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{acc};border:7px solid {o};border-radius:{radius}px;'
            f'box-shadow:14px 14px 0 {o};z-index:{z};transform:rotate({rot}deg)"></div>')


def svgbox(inner, x, y, size, vb=400, rot=0, z=14):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z};transform:rotate({rot}deg)">'
            f'<svg viewBox="0 0 {vb} {vb}" width="{size}" height="{size}" style="overflow:visible" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg></div>')


def doodle(kind, x, y, size, fill, rot=0, z=16):
    # v4 BUG: this used `try: fn(fill=..) except TypeError: fn(rot=rot)`, which SILENTLY dropped
    # the colour for the 5 stroke-drawn doodles (ring/arrow/squiggle/zigzag/spiral) — a pink arrow
    # rendered tomato. dd.stamp() resolves the right kwarg by introspection. Never call the PACK
    # entries by hand again.
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot)}</div>')


def stick(path_d, fill, x, y, size, rot=0, box=100, z=16, dark=False, detail="inner"):
    o = outline_of(dark)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z}">'
            f'{sh.sticker(path_d, fill, size=size, rot=rot, box=box, shadow=True, outline=o, detail=detail)}</div>')


# ══════════════════════════════════════════════════════════════════════════════
# ILLUSTRATIONS — 0..400 viewBox. Drawn ON the accent panel, so fills are cream/pink/lemon
# for contrast against the blue-green plate.
# ══════════════════════════════════════════════════════════════════════════════
SWK = 10
def _sh(d, dx=8, dy=10):
    return f'<path d="{d}" fill="{INK}" transform="translate({dx},{dy})"/>'


def art_zerofive():
    """0.5x drive pics. v1 BUG: a lens ring was stacked on top of the screen scene, so the phone,
    the lens and the landscape all fought in the same 150px. Now: the screen simply IS the
    ultrawide photo (two friends stretched to the edges, the way 0.5x actually distorts), and the
    camera is a small notch dot where a camera really sits."""
    b = "M112 26 H288 A28 28 0 0 1 316 54 V346 A28 28 0 0 1 288 374 H112 A28 28 0 0 1 84 346 V54 A28 28 0 0 1 112 26 Z"
    scr = "M112 78 H288 V322 H112 Z"
    return (
        f'{_sh(b)}'
        f'<path d="{b}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<circle cx="200" cy="52" r="7" fill="{INK}"/>'
        f'<path d="{scr}" fill="{SKY}" stroke="{INK}" stroke-width="{SWK}"/>'
        # ultrawide horizon — bowed, because 0.5x bends it
        f'<path d="M112 244 Q200 202 288 244 V322 H112 Z" fill="{MINT}" stroke="{INK}" stroke-width="7"/>'
        f'<circle cx="256" cy="132" r="26" fill="{LEMON}" stroke="{INK}" stroke-width="7"/>'
        # the two of them, stretched wide at the frame edges (the whole joke of 0.5x)
        f'<g><ellipse cx="152" cy="212" rx="34" ry="30" fill="{PINK}" stroke="{INK}" stroke-width="7"/>'
        f'<path d="M120 300 Q120 246 152 246 Q184 246 184 300 Z" fill="{PINK}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<circle cx="141" cy="208" r="4.5" fill="{INK}"/><circle cx="163" cy="208" r="4.5" fill="{INK}"/>'
        f'<path d="M142 224 Q152 233 162 224" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
        f'<g><ellipse cx="250" cy="216" rx="30" ry="27" fill="{CREAM}" stroke="{INK}" stroke-width="7"/>'
        f'<path d="M222 300 Q222 250 250 250 Q278 250 278 300 Z" fill="{CREAM}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<circle cx="240" cy="213" r="4.5" fill="{INK}"/><circle cx="260" cy="213" r="4.5" fill="{INK}"/>'
        f'<path d="M240 228 Q250 236 260 228" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
        # 0.5x badge
        f'<g transform="rotate(-8 318 336)">'
        f'<rect x="254" y="308" width="128" height="56" rx="28" fill="{INK}" transform="translate(7,8)"/>'
        f'<rect x="254" y="308" width="128" height="56" rx="28" fill="{PINK}" stroke="{INK}" stroke-width="8"/>'
        f'<text x="318" y="347" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="30" fill="#FFFFFF">0.5&#215;</text></g>'
        f'<path d="M42 118 L72 136 M38 178 L70 174" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    )


def art_chai():
    """40km for a chai — cutting-chai glass + a dashed road looping behind it."""
    g = "M134 162 L266 162 L245 348 A16 16 0 0 1 229 362 L171 362 A16 16 0 0 1 155 348 Z"
    t = "M148 216 L252 216 L237 330 A10 10 0 0 1 227 340 L173 340 A10 10 0 0 1 163 330 Z"
    return (
        f'<path d="M20 334 Q200 238 380 334" fill="none" stroke="{INK}" stroke-width="13"/>'
        f'<path d="M20 334 Q200 238 380 334" fill="none" stroke="{PINK}" stroke-width="7" '
        f'stroke-dasharray="20 20" stroke-linecap="round"/>'
        f'{_sh(g)}'
        f'<path d="{g}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="{t}" fill="{LEMON}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<ellipse cx="200" cy="216" rx="52" ry="13" fill="{sh.lighten(LEMON,.4)}" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M134 162 L266 162" stroke="{INK}" stroke-width="{SWK}" stroke-linecap="round"/>'
        f'<path d="M166 134 Q150 104 170 78 Q188 54 174 28" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M214 136 Q198 104 218 80 Q236 56 222 32" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round" opacity=".75"/>'
        f'<path d="M256 142 Q244 116 260 96" fill="none" stroke="{CREAM}" stroke-width="10" stroke-linecap="round" opacity=".5"/>'
        f'<g transform="rotate(8 66 300)">'
        f'<rect x="2" y="272" width="128" height="54" rx="27" fill="{INK}" transform="translate(7,8)"/>'
        f'<rect x="2" y="272" width="128" height="54" rx="27" fill="{PINK}" stroke="{INK}" stroke-width="8"/>'
        f'<text x="66" y="309" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="28" fill="#FFFFFF">40 KM</text></g>'
    )


def art_reel():
    """bullied into a reel — vertical video, REC dot, and three eyes watching in public."""
    b = "M124 22 H276 A24 24 0 0 1 300 46 V354 A24 24 0 0 1 276 378 H124 A24 24 0 0 1 100 354 V46 A24 24 0 0 1 124 22 Z"
    play = "M180 168 L248 208 L180 248 Z"
    return (
        f'{_sh(b)}'
        f'<path d="{b}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="M124 64 H276 V336 H124 Z" fill="{INK}"/>'
        f'<circle cx="200" cy="208" r="64" fill="{CREAM}" opacity=".12"/>'
        f'{_sh(play, 6, 7)}'
        f'<path d="{play}" fill="{PINK}" stroke="{CREAM}" stroke-width="8" stroke-linejoin="round"/>'
        f'<circle cx="152" cy="96" r="12" fill="{PINK}" stroke="{CREAM}" stroke-width="5"/>'
        f'<text x="174" y="105" font-family="JetBrains Mono, monospace" font-weight="700" '
        f'font-size="21" fill="{CREAM}">REC</text>'
        + "".join(f'<rect x="{138 + i*17}" y="{302 - (i%3)*13}" width="9" height="{20 + (i%3)*13}" '
                  f'rx="4" fill="{SKY}" stroke="{INK}" stroke-width="3"/>' for i in range(8)) +
        f'<g><circle cx="46" cy="140" r="30" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="55" cy="142" r="12" fill="{INK}"/></g>'
        f'<g><circle cx="356" cy="200" r="26" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="347" cy="202" r="10" fill="{INK}"/></g>'
        f'<g><circle cx="58" cy="292" r="22" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="65" cy="294" r="9" fill="{INK}"/></g>'
    )


def art_ha():
    """laughed first, asked second. v1 BUG: the 'banana peel' read as a yellow eye — nobody would
    decode it. Replaced with the actual joke: a HUGE laugh, and a much smaller, later, apologetic
    'u ok?' bubble trailing behind it. The size difference IS the punchline."""
    burst = sh.starburst(points=13, R=48, r=32)
    bub = ("M236 268 H370 A24 24 0 0 1 394 292 V344 A24 24 0 0 1 370 368 H302 L268 396 L276 368 "
           "H236 A24 24 0 0 1 212 344 V292 A24 24 0 0 1 236 268 Z")
    # v2 BUG: the burst was scaled about the origin (translate(10,4) scale(2.15)) which put its
    # centre at ~(117,111), but "HA!" was hard-coded at x=228 — so the word sat OUTSIDE its own
    # burst. Centre is now derived: scale(2.6) about a translate that lands the 0..100 box centre
    # on (196,150), and the text is placed at that same point.
    S, CX, CY = 2.6, 196, 150
    tx, ty = S * 50, S * 50
    return (
        f'<g transform="translate({CX - tx},{CY - ty}) scale({S})">'
        f'<path d="{burst}" fill="{INK}" transform="translate(4,5)"/>'
        f'<path d="{burst}" fill="{CREAM}" stroke="{CREAM}" stroke-width="18" stroke-linejoin="round"/>'
        f'<path d="{burst}" fill="{CREAM}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>'
        f'<text x="{CX}" y="{CY + 34}" text-anchor="middle" font-family="NeutralFace, sans-serif" '
        f'font-weight="900" font-size="102" fill="{INK}">HA!</text>'
        # the late, much smaller apology — the SIZE GAP is the punchline
        f'{_sh(bub, 6, 7)}'
        f'<path d="{bub}" fill="{PINK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<text x="303" y="334" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="34" fill="#FFFFFF">u ok?</text>'
        f'<text x="30" y="316" font-family="NeutralFace, sans-serif" font-weight="900" '
        f'font-size="40" fill="{INK}" transform="rotate(-14 30 316)">ha</text>'
        f'<text x="86" y="382" font-family="NeutralFace, sans-serif" font-weight="900" '
        f'font-size="30" fill="{INK}" transform="rotate(8 86 382)">ha</text>'
    )


def art_door():
    """showed up unasked — an open arch doorway, warm light spilling, a friend mid-step."""
    frame = sh.arch(w=376, h=386, pad=10)
    leaf = "M206 104 A92 92 0 0 1 298 196 V370 H206 Z"
    return (
        f'<g transform="translate(12,6)">'
        f'{_sh(frame)}'
        f'<path d="{frame}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="M50 372 V186 A98 98 0 0 1 246 186 V372 Z" fill="{INK}"/>'
        f'<path d="M50 372 L108 176 L186 176 L166 372 Z" fill="{LEMON}" opacity=".92"/>'
        f'<path d="{leaf}" fill="{SKY}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<circle cx="222" cy="248" r="9" fill="{CREAM}"/>'
        # the friend, mid-step. v2 read as "person sitting on a chair" because the torso was a
        # flat-topped rounded rect with two stick legs under it — now a shouldered torso.
        f'<circle cx="122" cy="220" r="31" fill="{PINK}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="113" cy="217" r="4.5" fill="{INK}"/><circle cx="133" cy="217" r="4.5" fill="{INK}"/>'
        f'<path d="M112 234 Q122 243 132 234" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M122 254 Q158 258 158 306 L158 330 L86 330 L86 306 Q86 258 122 254 Z" '
        f'fill="{PINK}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<path d="M100 330 L88 372 M144 330 L160 372" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
        f'</g>'
        # v2 BUG: this was `dd.heart()` nested inside the art <svg>. A nested <svg> with no
        # width/height resolves to 100% of the PARENT viewBox (400), not its own 120 box — so
        # scale(.72) produced a 288-unit heart that bled off the panel AND off the canvas.
        # Inline path, explicit coordinates, no nesting.
        f'<g transform="translate(300,26) scale(.62)">'
        f'<path d="M60 104 C20 76 12 52 12 38 C12 22 24 14 36 14 C46 14 55 20 60 30 '
        f'C65 20 74 14 84 14 C96 14 108 22 108 38 C108 52 100 76 60 104 Z" '
        f'fill="{PINK}" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/></g>'
    )


def art_silence():
    """comfortable silence — two of them on a ledge under ONE quiet '...' bubble."""
    b1 = sh.blob(seed=4, lobes=8, r=44, wobble=.13)
    b2 = sh.blob(seed=9, lobes=8, r=44, wobble=.16)
    bub = ("M116 22 H300 A30 30 0 0 1 330 52 V142 A30 30 0 0 1 300 172 H216 L176 208 L184 172 "
           "H116 A30 30 0 0 1 86 142 V52 A30 30 0 0 1 116 22 Z")
    return (
        f'{_sh(bub)}'
        f'<path d="{bub}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        + "".join(f'<circle cx="{160 + i*48}" cy="98" r="17" fill="{PINK}" stroke="{INK}" stroke-width="7"/>'
                  for i in range(3)) +
        f'<rect x="22" y="342" width="356" height="22" rx="11" fill="{INK}"/>'
        f'<rect x="22" y="332" width="356" height="22" rx="11" fill="{MINT}" stroke="{INK}" stroke-width="7"/>'
        f'<g transform="translate(38,198) scale(1.42)">'
        f'<path d="{b1}" fill="{INK}" transform="translate(3,4)"/>'
        f'<path d="{b1}" fill="{PINK}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<circle cx="36" cy="44" r="5" fill="{INK}"/><circle cx="64" cy="44" r="5" fill="{INK}"/>'
        f'<path d="M36 66 Q50 74 64 66" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
        f'<g transform="translate(202,198) scale(1.42)">'
        f'<path d="{b2}" fill="{INK}" transform="translate(3,4)"/>'
        f'<path d="{b2}" fill="{CREAM}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<circle cx="36" cy="44" r="5" fill="{INK}"/><circle cx="64" cy="44" r="5" fill="{INK}"/>'
        f'<path d="M36 68 Q50 74 64 68" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# SLIDES
# ══════════════════════════════════════════════════════════════════════════════
def slide_cover():
    acc = SLIDE_ACCENT[0]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{INK};z-index:0"></div>'

    # solid, outlined decoration — no faint washes
    # v2 left the bottom band (y>1100) nearly empty — a real dead zone. Cluster enlarged and
    # pulled up so the closing third carries weight instead of trailing off.
    deco = (stick(sh.blob(seed=6, lobes=9), SKY, 736, 210, 296, rot=-8, dark=True, detail="dots")
            + stick(sh.scallop(lobes=14, r=45), PINK, 846, 388, 190, rot=12, dark=True)
            + stick(sh.starburst(points=11), MINT, 672, 1128, 190, rot=-6, dark=True)
            + stick(sh.capsule(w=100, h=42), SKY, 132, 1156, 200, rot=7, dark=True, box=100)
            + doodle("sparkle", 604, 274, 84, PINK, rot=16)
            + doodle("heart", 388, 1216, 116, PINK, rot=-12)
            + doodle("plus", 900, 1258, 92, MINT, rot=14))
    els += [("bl", 736, 210, 296, 296), ("sc", 846, 388, 190, 190),
            ("st", 672, 1128, 190, 190), ("cap", 132, 1156, 200, 90),
            ("d1", 604, 274, 84, 84), ("d2", 388, 1216, 116, 116), ("d3", 900, 1258, 92, 92)]

    eb = chip("friendship day &middot; 02.08.26", PINK, dark=True, y=176)
    els.append(("chip", M, 176, 400, 48))

    t1 = (f'<div style="position:absolute;top:322px;left:{M}px;z-index:24;font-family:var(--d);'
          f'font-weight:900;font-size:138px;line-height:.87;letter-spacing:-.04em;color:{CREAM};'
          f'text-transform:uppercase">SIX<br>REASONS<br>TO</div>')
    els.append(("giant", M, 322, 660, 370))
    t2 = punch(acc, 716, x=M - 6, rot=-2.4, fs=112, dark=True)
    els.append(("punch", M - 6, 716, 780, 170))

    sub = (f'<div style="position:absolute;top:952px;left:{M}px;width:800px;z-index:24;'
           f'font-family:var(--e);font-weight:400;font-size:40px;line-height:1.3;'
           f'letter-spacing:-.015em;color:rgba(244,239,224,.84)">there are more than six. these are '
           f'just the ones we could <span style="font-family:var(--s);font-style:italic;'
           f'color:{PINK}">prove</span>.</div>')
    els.append(("sub", M, 952, 800, 120))

    sw = (f'<div style="position:absolute;bottom:56px;right:{M}px;z-index:30;font-family:var(--m);'
          f'font-weight:700;font-size:16px;letter-spacing:.14em;text-transform:uppercase;'
          f'color:{CREAM};display:flex;align-items:center;gap:10px">swipe'
          f'<span style="display:inline-block;width:34px;height:3px;background:{PINK}"></span>&rarr;</div>')
    els.append(("swipe", 830, H - 82, 180, 28))

    return bg + deco + logo(True) + dots(0, True) + eb + t1 + t2 + sub + sw, els, True


def slide_line(i, txt, art_fn, pink_cluster, panel_acc=None, art_dx=0, art_dy=0):
    """The fixed four-quadrant skeleton — Q1 numeral, Q2 art panel (bleeds right),
    Q3 text+punch, Q4 pink cluster. Nothing is left to land where it may."""
    acc = panel_acc or SLIDE_ACCENT[i]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{CREAM};z-index:0"></div>'

    num = numeral(i, acc)
    els.append(("num", 52, 286, 330, 250))

    PX, PY, PW, PH = 292, 262, 788, 616          # right edge == canvas edge: a clean bleed
    pnl = panel(PX, PY, PW, PH, acc)
    els.append(("panel", PX, PY, PW - 8, PH))

    art = svgbox(art_fn(), PX + 118 + art_dx, PY + 46 + art_dy, 530, z=15)
    els.append(("art", PX + 130, PY + 58, 500, 500))

    tx = body(txt, 920)
    els.append(("body", M, 920, 880, 150))

    p = punch(acc, 1128)
    els.append(("punch", M - 4, 1128, 560, 132))

    return (bg + num + pnl + art + logo() + dots(i) + chip(f"reason {i:02d} &middot; of 06", PINK, y=176)
            + tx + p + pink_cluster + footer()), els, False


def slide_closer():
    acc = SLIDE_ACCENT[7]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{INK};z-index:0"></div>'

    deco = (stick(sh.blob(seed=8, lobes=9), MINT, 748, 232, 290, rot=10, dark=True, detail="dots")
            + stick(sh.scallop(lobes=14, r=45), PINK, 690, 1150, 208, rot=-9, dark=True)
            + doodle("paw", 912, 1214, 112, PINK, rot=-8)
            + doodle("sparkle", 604, 1052, 76, SKY, rot=18))
    els += [("bl", 748, 232, 290, 290), ("sc", 690, 1150, 208, 208),
            ("pw", 912, 1214, 112, 112), ("sp", 604, 1052, 76, 76)]

    eb = chip("that's the whole post", PINK, dark=True, y=176)
    els.append(("chip", M, 176, 420, 48))

    t1 = (f'<div style="position:absolute;top:322px;left:{M}px;width:620px;z-index:24;'
          f'font-family:var(--e);font-weight:400;font-size:54px;line-height:1.2;'
          f'letter-spacing:-.02em;color:rgba(244,239,224,.9)">you don\'t need '
          f'<span style="font-family:var(--s);font-style:italic;color:{PINK}">a</span> reason.</div>')
    els.append(("t1", M, 322, 620, 76))

    t2 = (f'<div style="position:absolute;top:418px;left:{M}px;z-index:24;font-family:var(--d);'
          f'font-weight:900;font-size:118px;line-height:.9;letter-spacing:-.04em;color:{CREAM};'
          f'text-transform:uppercase">YOU HAVE<br>A HUNDRED.</div>')
    els.append(("t2", M, 418, 700, 230))

    t3 = punch(acc, 700, x=M - 6, rot=-2.2, fs=88, txt="go wish them", dark=True)
    els.append(("punch", M - 6, 700, 640, 145))

    t4 = (f'<div style="position:absolute;top:892px;left:{M}px;width:560px;z-index:24;'
          f'font-family:var(--e);font-weight:400;font-size:42px;line-height:1.28;'
          f'letter-spacing:-.015em;color:rgba(244,239,224,.88)">and {em("tag them below")} '
          f'&mdash; they&rsquo;ll pretend to be annoyed.</div>')
    els.append(("t4", M, 892, 560, 170))

    sign = (f'<div style="position:absolute;top:1104px;left:{M}px;z-index:24;font-family:var(--m);'
            f'font-weight:500;font-size:19px;letter-spacing:.05em;line-height:1.65;'
            f'color:rgba(244,239,224,.6)">happy friendship day,<br>'
            f'<span style="font-weight:700;color:{CREAM}">from all of us at aquaterra</span></div>')
    els.append(("sign", M, 1104, 520, 92))

    return bg + deco + logo(True) + dots(7, True) + eb + t1 + t2 + t3 + t4 + sign + footer(True), els, True


# ── the six ───────────────────────────────────────────────────────────────────
def build_lines():
    S = []
    S.append(slide_line(1, f'if you&rsquo;ve only gone for drives to take {em("embarrassing 0.5x pics")},',
        art_zerofive,
        doodle("zigzag", 742, 1216, 152, PINK, rot=6) + doodle("star", 936, 1104, 84, SKY, rot=-14),
))

    S.append(slide_line(2, f'if you&rsquo;ve driven {em("40km for a chai")} and called it a plan,',
        art_chai,
        doodle("arrow", 740, 1196, 156, PINK, rot=-6) + doodle("circle", 950, 1108, 78, MINT),
))

    S.append(slide_line(3, f'if you&rsquo;ve {em("bullied them into making a reel")} in public,',
        art_reel,
        doodle("lightning", 764, 1188, 132, PINK, rot=-10) + doodle("dots", 932, 1112, 92, SKY),
))

    S.append(slide_line(4, f'if you {em("laughed first")} and asked if they were okay second,',
        art_ha,
        doodle("speech", 748, 1194, 136, PINK, rot=8) + doodle("plus", 946, 1108, 78, MINT, rot=12),
))

    S.append(slide_line(5, f'if they&rsquo;ve {em("shown up without being asked")},',
        art_door,
        doodle("heart", 754, 1192, 138, PINK, rot=-10) + doodle("sparkle", 946, 1104, 82, SKY, rot=16),
))

    S.append(slide_line(6, f'if you&rsquo;ve {em("sat in silence together")} and it wasn&rsquo;t awkward,',
        art_silence,
        doodle("spiral", 748, 1190, 140, PINK, rot=0) + doodle("ring", 944, 1108, 82, MINT),
))
    return S


async def main():
    os.makedirs(OUT, exist_ok=True)
    for idx, (inner, els, dark) in enumerate([slide_cover()] + build_lines() + [slide_closer()], 1):
        bg = INK if dark else CREAM
        html = B.page(W, H, bg, inner, grain=True)
        pf = lay.preflight(W, H, els, html=html, page_bg=bg, core=core, expect_hero=False)
        path = f"{OUT}/v5_{idx:02d}.png"
        await B.render(html, path, W, H)
        print(f"  -> {path}  clean={pf.get('clean')}")
    print("DONE — v5, 8 slides @ 1080x1440")

asyncio.run(main())
