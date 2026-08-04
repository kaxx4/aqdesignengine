"""AQ FRIENDSHIP DAY CAROUSEL — 1080x1440, 8 slides.
Workflow B-style bespoke build (core+build+doodles+shapes+layout primitives directly).

THE SYSTEM (what makes 8 slides read as ONE post):
  1. every line slide ends in the SAME "WISH THEM" punch-box — same box, same ink border,
     same 10px hard shadow, same tilt. Only the accent rotates. That repetition IS the design.
  2. every illustration gets shapes.sticker()'s die-cut halo + ink outline, uniformly.
  3. dark ink bookends (cover + closer), cream middle — so the set has a rhythm, not 8 twins.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); sh = load("shapes"); lay = load("layout")

W, H = 1080, 1440                 # custom canvas — NOT core.SIZES["feed"] (1350)
M = 72
A = core.ACCENTS                  # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
INK = "#0A0A0A"; CREAM = "#F4EFE0"
OUT = "out/versions/friendship_day"

# ══════════════════════════════════════════════════════════════════════════════
# SHARED FURNITURE
# ══════════════════════════════════════════════════════════════════════════════
def logo(dark=False, x=M, y=64, h=52):
    """CLAUDE.md §9: real colored wordmark, top-left, NEVER white-inverted.
    On dark fields it sits in a cream pill (the brand rule) rather than a drop-shadow."""
    img = f'<img src="{core.LOGO}" style="height:{h}px;display:block">'
    if dark:
        return (f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:30;background:{CREAM};'
                f'border:4px solid {INK};border-radius:999px;padding:10px 22px;'
                f'box-shadow:6px 6px 0 rgba(0,0,0,.45)">{img}</div>')
    return f'<div style="position:absolute;top:{y}px;left:{x}px;z-index:30">{img}</div>'


def dots(active, n=8, dark=False, y=88):
    """Carousel position dots — ACTIVE dot takes this slide's accent (playbook rule)."""
    acc = SLIDE_ACCENT[active]
    idle = "rgba(255,255,255,.30)" if dark else "rgba(10,10,10,.20)"
    out = f'<div style="position:absolute;top:{y}px;right:{M}px;z-index:30;display:flex;gap:9px;align-items:center">'
    for i in range(n):
        if i == active:
            out += (f'<span style="width:13px;height:13px;border-radius:50%;background:{acc};'
                    f'border:3px solid {INK if not dark else CREAM}"></span>')
        else:
            out += f'<span style="width:9px;height:9px;border-radius:50%;background:{idle}"></span>'
    return out + "</div>"


def eyebrow(txt, acc, dark=False, y=None):
    y = y or 172
    fg = core.text_on(acc)
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;z-index:25;font-family:var(--m);'
            f'font-weight:700;font-size:15px;letter-spacing:.16em;text-transform:uppercase;'
            f'color:{fg};background:{acc};border:3px solid {INK};border-radius:999px;'
            f'padding:8px 18px;box-shadow:4px 4px 0 {INK};display:inline-block">{txt}</div>')


def footer(dark=False, extra=""):
    c = CREAM if dark else INK
    return (f'<div style="position:absolute;bottom:56px;left:{M}px;z-index:30;font-family:var(--m);'
            f'font-weight:700;font-size:16px;letter-spacing:.07em;color:{c}">@ngo.aquaterra'
            f'<span style="opacity:.55;font-weight:500"> {extra}</span></div>')


def punch(acc, x=None, y=0, rot=-2.2, fs=76, txt="wish them", right=None):
    """THE DRUMBEAT. Identical on all six line slides — only the accent moves.
    Uppercase NeutralFace in a hard-shadowed accent box. This is the whole system."""
    fg = core.text_on(acc)
    pos = f'left:{x}px;' if right is None else f'right:{right}px;'
    return (f'<div style="position:absolute;{pos}top:{y}px;z-index:26;display:inline-block;'
            f'background:{acc};color:{fg};border:7px solid {INK};box-shadow:12px 12px 0 {INK};'
            f'padding:12px 32px 16px;font-family:var(--d);font-weight:900;font-size:{fs}px;'
            f'line-height:1;text-transform:uppercase;letter-spacing:-.01em;white-space:nowrap;'
            f'transform:rotate({rot}deg)">{txt}</div>')


def line_text(txt, y, dark=False, fs=54, maxw=880):
    c = CREAM if dark else INK
    return (f'<div style="position:absolute;top:{y}px;left:{M}px;width:{maxw}px;z-index:25;'
            f'font-family:var(--e);font-weight:400;font-size:{fs}px;line-height:1.26;'
            f'letter-spacing:-.015em;color:{c}">{txt}</div>')


def em(t, acc):
    """inline highlight — an underline swipe in the slide accent, behind the word"""
    return (f'<span style="background:linear-gradient(to top,{acc}66 0,{acc}66 38%,transparent 38%);'
            f'box-decoration-break:clone;-webkit-box-decoration-break:clone">{t}</span>')


def svgbox(inner, x, y, size, vb=400, rot=0, z=12, op=1.0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z};opacity:{op};transform:rotate({rot}deg)">'
            f'<svg viewBox="0 0 {vb} {vb}" width="{size}" height="{size}" style="overflow:visible" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg></div>')


def doodle(kind, x, y, size, fill, rot=0, z=10, op=1.0):
    fn = getattr(dd, kind)
    try: inner = fn(fill=fill, rot=rot, style="clean")
    except TypeError: inner = fn(rot=rot, style="clean")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z};opacity:{op}">{inner}</div>')


def stick(path_d, fill, x, y, size, rot=0, box=100, z=12, shadow=True, detail="inner"):
    """shapes.sticker() placed absolutely — the uniform die-cut treatment, applied to EVERY object."""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z}">'
            f'{sh.sticker(path_d, fill, size=size, rot=rot, box=box, shadow=shadow, detail=detail)}</div>')


# ── background fields (one per slide so no two line slides look alike) ─────────
def field_blob(x, y, size, acc, seed=3, op=.22, z=2):   # arg order matches field_rings
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z};opacity:{op}">'
            f'{sh.sticker(sh.blob(seed=seed, lobes=9, r=46, wobble=.14), acc, size=size, halo=False, detail="none")}</div>')

def field_checker(x, y, w, h, acc, cell=52, rot=0, op=.16, z=2):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z};opacity:{op};'
            f'transform:rotate({rot}deg);overflow:hidden">{sh.checker(w, h, cell=cell, c1=acc, c2=CREAM)}</div>')

def field_band(x, y, w, h, acc, rot=0, op=1.0, z=2, radius=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{acc};opacity:{op};z-index:{z};transform:rotate({rot}deg);'
            f'border-radius:{radius}px"></div>')

def field_rings(x, y, size, acc, n=3, z=2, op=.30):
    inner = "".join(f'<circle cx="200" cy="200" r="{60 + i*52}" fill="none" stroke="{acc}" stroke-width="14"/>'
                    for i in range(n))
    return svgbox(inner, x, y, size, z=z, op=op)

def field_hatch(x, y, w, h, acc, op=.20, z=2, rot=0):
    lines = "".join(f'<line x1="{i}" y1="0" x2="{i-h}" y2="{h}" stroke="{acc}" stroke-width="9"/>'
                    for i in range(0, int(w + h), 30))
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z};opacity:{op};'
            f'transform:rotate({rot}deg);overflow:hidden;width:{w}px;height:{h}px">'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'{lines}</svg></div>')


# ══════════════════════════════════════════════════════════════════════════════
# BESPOKE ILLUSTRATIONS — one per line, in a 0..400 viewBox.
# doodles.py has no camera/chai/door, so these are drawn here; each still wears the
# same ink outline + hard shadow language as sticker() so the set stays uniform.
# ══════════════════════════════════════════════════════════════════════════════
SWK = 10  # ink stroke weight in the 400-box

def _sh(d, dx=9, dy=11):   # hard offset ink shadow, same vector on every object
    return f'<path d="{d}" fill="{INK}" transform="translate({dx},{dy})"/>'

def art_zerofive(acc=A[4], acc2=A[0]):
    """0.5x drive pics — a phone held wide, huge ultrawide lens, tiny scene inside, 0.5x badge."""
    body = "M96 34 H304 A26 26 0 0 1 330 60 V344 A26 26 0 0 1 304 370 H96 A26 26 0 0 1 70 344 V60 A26 26 0 0 1 96 34 Z"
    screen = "M96 74 H304 V330 H96 Z"
    return (
        f'{_sh(body)}'
        f'<path d="{body}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="{screen}" fill="{acc}" stroke="{INK}" stroke-width="{SWK}"/>'
        # tiny landscape inside the screen — hills + sun + road (the "drive")
        f'<path d="M96 260 Q150 200 200 250 Q250 296 304 244 V330 H96 Z" fill="{sh.lighten(acc,.45)}" stroke="{INK}" stroke-width="7"/>'
        f'<circle cx="252" cy="150" r="30" fill="{A[2]}" stroke="{INK}" stroke-width="7"/>'
        f'<path d="M96 330 L200 288 L304 330" fill="none" stroke="{INK}" stroke-width="7" stroke-dasharray="16 14" stroke-linecap="round"/>'
        # ultrawide lens barrel
        f'<circle cx="200" cy="212" r="74" fill="none" stroke="{INK}" stroke-width="{SWK}"/>'
        f'<circle cx="200" cy="212" r="52" fill="{INK}" opacity=".82"/>'
        f'<circle cx="200" cy="212" r="34" fill="{acc2}" stroke="{INK}" stroke-width="7"/>'
        f'<circle cx="186" cy="198" r="10" fill="{CREAM}" opacity=".92"/>'
        # 0.5x badge, tilted
        f'<g transform="rotate(-9 316 320)">'
        f'<rect x="252" y="292" width="128" height="56" rx="28" fill="{INK}" transform="translate(8,9)"/>'
        f'<rect x="252" y="292" width="128" height="56" rx="28" fill="{A[2]}" stroke="{INK}" stroke-width="8"/>'
        f'<text x="316" y="331" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="30" fill="{INK}">0.5&#215;</text></g>'
        # shutter sparks
        f'<path d="M42 96 L74 118 M40 160 L76 158 M60 46 L84 76" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    )

def art_chai(acc=A[2], acc2=A[3]):
    """40km for a chai — cutting-chai glass, steam, and a dashed road looping behind it."""
    glass = "M132 158 L268 158 L246 348 A16 16 0 0 1 230 362 L170 362 A16 16 0 0 1 154 348 Z"
    tea   = "M146 214 L254 214 L238 330 A10 10 0 0 1 228 340 L172 340 A10 10 0 0 1 162 330 Z"
    return (
        # road arc behind
        f'<path d="M24 330 Q200 236 376 330" fill="none" stroke="{INK}" stroke-width="12" opacity=".28"/>'
        f'<path d="M24 330 Q200 236 376 330" fill="none" stroke="{acc2}" stroke-width="7" '
        f'stroke-dasharray="20 20" stroke-linecap="round"/>'
        f'{_sh(glass)}'
        f'<path d="{glass}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="{tea}" fill="{acc}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
        f'<ellipse cx="200" cy="214" rx="54" ry="13" fill="{sh.lighten(acc,.4)}" stroke="{INK}" stroke-width="6"/>'
        f'<path d="M132 158 L268 158" stroke="{INK}" stroke-width="{SWK}" stroke-linecap="round"/>'
        # steam
        f'<path d="M164 130 Q148 100 168 74 Q186 50 172 24" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        f'<path d="M212 132 Q196 100 216 76 Q234 52 220 28" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" opacity=".7"/>'
        f'<path d="M256 138 Q244 112 260 92" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" opacity=".45"/>'
        # 40 KM tag
        f'<g transform="rotate(8 76 268)">'
        f'<rect x="12" y="240" width="128" height="54" rx="27" fill="{INK}" transform="translate(8,9)"/>'
        f'<rect x="12" y="240" width="128" height="54" rx="27" fill="{acc2}" stroke="{INK}" stroke-width="8"/>'
        f'<text x="76" y="277" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        f'font-weight="700" font-size="28" fill="#FFFFFF">40 KM</text></g>'
    )

def art_reel(acc=A[0], acc2=A[4]):
    """bullied into a reel — phone shooting vertical video, REC dot, and eyes watching."""
    body = "M118 20 H282 A24 24 0 0 1 306 44 V356 A24 24 0 0 1 282 380 H118 A24 24 0 0 1 94 356 V44 A24 24 0 0 1 118 20 Z"
    play = "M176 168 L246 208 L176 248 Z"
    return (
        f'{_sh(body)}'
        f'<path d="{body}" fill="{acc}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="M118 62 H282 V338 H118 Z" fill="{INK}" opacity=".88"/>'
        f'<circle cx="200" cy="208" r="66" fill="{CREAM}" stroke="{INK}" stroke-width="8" opacity=".14"/>'
        f'{_sh(play, 6, 7)}'
        f'<path d="{play}" fill="{A[2]}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        # REC
        f'<circle cx="146" cy="94" r="13" fill="{A[3]}" stroke="{INK}" stroke-width="6"/>'
        f'<text x="170" y="104" font-family="JetBrains Mono, monospace" font-weight="700" '
        f'font-size="22" fill="{CREAM}">REC</text>'
        # timeline ticks along the bottom of the screen
        + "".join(f'<rect x="{132 + i*17}" y="{300 - (i%3)*14}" width="9" height="{22 + (i%3)*14}" '
                  f'rx="4" fill="{acc2}" stroke="{INK}" stroke-width="4"/>' for i in range(9)) +
        # eyes watching from the sides
        f'<g><circle cx="44" cy="132" r="30" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="52" cy="134" r="12" fill="{INK}"/></g>'
        f'<g><circle cx="358" cy="196" r="26" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="350" cy="198" r="10" fill="{INK}"/></g>'
        f'<g><circle cx="58" cy="290" r="22" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        f'<circle cx="64" cy="292" r="9" fill="{INK}"/></g>'
    )

def art_ha(acc=A[3], acc2=A[2]):
    """laughed first, asked second — a HA! starburst over a banana peel."""
    burst = sh.starburst(points=13, R=48, r=33)
    peel  = "M120 330 Q200 286 288 322 Q246 366 186 366 Q142 366 120 330 Z"
    return (
        # the laugh
        f'<g transform="translate(56,14) scale(2.4)">'
        f'<path d="{burst}" fill="{INK}" transform="translate(4,5)"/>'
        f'<path d="{burst}" fill="{sh.lighten(acc,.55)}" stroke="{sh.lighten(acc,.55)}" stroke-width="18" stroke-linejoin="round"/>'
        f'<path d="{burst}" fill="{acc}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></g>'
        f'<text x="200" y="188" text-anchor="middle" font-family="NeutralFace, sans-serif" '
        f'font-weight="900" font-size="84" fill="{CREAM}">HA!</text>'
        # the peel
        f'{_sh(peel)}'
        f'<path d="{peel}" fill="{acc2}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="M186 328 Q200 300 236 292 M186 328 Q176 300 148 296" fill="none" stroke="{INK}" '
        f'stroke-width="8" stroke-linecap="round"/>'
        # small trailing has
        f'<text x="330" y="106" font-family="NeutralFace, sans-serif" font-weight="900" '
        f'font-size="40" fill="{INK}" transform="rotate(12 330 106)">ha</text>'
        f'<text x="26" y="252" font-family="NeutralFace, sans-serif" font-weight="900" '
        f'font-size="30" fill="{INK}" transform="rotate(-14 26 252)">ha</text>'
        f'<path d="M296 232 L330 244 M304 268 L338 268" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    )

def art_door(acc=A[1], acc2=A[0]):
    """showed up unasked — an open arch doorway with light spilling and a figure stepping through."""
    frame = sh.arch(w=400, h=400, pad=8)          # parametric arch, scaled to the 400 box
    leaf  = "M212 96 A94 94 0 0 1 306 190 V376 H212 Z"
    return (
        f'{_sh(frame)}'
        f'<path d="{frame}" fill="{acc}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        f'<path d="M94 392 V190 A106 106 0 0 1 306 190 V392 Z" fill="{CREAM}" stroke="{INK}" stroke-width="8"/>'
        # light spill
        f'<path d="M94 392 L152 168 L232 168 L212 392 Z" fill="{A[2]}" opacity=".55"/>'
        # the door leaf, swung open
        f'<path d="{leaf}" fill="{sh.lighten(acc,.35)}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        f'<circle cx="228" cy="248" r="10" fill="{INK}"/>'
        # the friend, mid-step
        f'<circle cx="150" cy="224" r="32" fill="{acc2}" stroke="{INK}" stroke-width="8"/>'
        f'<path d="M150 262 Q186 268 186 320 L186 372 M150 262 Q114 268 114 320 L114 372" '
        f'fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
        f'<path d="M118 268 L118 330 L184 330 L184 268 Q150 254 118 268 Z" fill="{acc2}" '
        f'stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
        # a heart above, unprompted
        f'<g transform="translate(268,22) scale(.86)">'
        f'{dd.heart(fill=A[0])}</g>'
    )

def art_silence(acc=A[5], acc2=A[6]):
    """comfortable silence — two blobs on a ledge under one quiet '...' bubble."""
    b1 = sh.blob(seed=4, lobes=8, r=44, wobble=.13)
    b2 = sh.blob(seed=9, lobes=8, r=44, wobble=.16)
    bubble = ("M108 34 H292 A30 30 0 0 1 322 64 V148 A30 30 0 0 1 292 178 H210 L168 216 L178 178 "
              "H108 A30 30 0 0 1 78 148 V64 A30 30 0 0 1 108 34 Z")
    return (
        f'{_sh(bubble)}'
        f'<path d="{bubble}" fill="{CREAM}" stroke="{INK}" stroke-width="{SWK}" stroke-linejoin="round"/>'
        + "".join(f'<circle cx="{152 + i*48}" cy="108" r="17" fill="{acc}" stroke="{INK}" stroke-width="7"/>'
                  for i in range(3)) +
        # the ledge
        f'<rect x="26" y="352" width="348" height="20" rx="10" fill="{INK}"/>'
        f'<rect x="26" y="344" width="348" height="20" rx="10" fill="{acc2}" stroke="{INK}" stroke-width="7"/>'
        # the two of them, sitting, not talking
        f'<g transform="translate(28,206) scale(1.5)">'
        f'<path d="{b1}" fill="{INK}" transform="translate(3,4)"/>'
        f'<path d="{b1}" fill="{acc}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<circle cx="36" cy="44" r="5" fill="{INK}"/><circle cx="64" cy="44" r="5" fill="{INK}"/>'
        f'<path d="M36 66 Q50 76 64 66" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
        f'<g transform="translate(196,206) scale(1.5)">'
        f'<path d="{b2}" fill="{INK}" transform="translate(3,4)"/>'
        f'<path d="{b2}" fill="{A[2]}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
        f'<circle cx="36" cy="44" r="5" fill="{INK}"/><circle cx="64" cy="44" r="5" fill="{INK}"/>'
        f'<path d="M36 68 Q50 76 64 68" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/></g>'
        # quiet marks
        f'<path d="M356 246 L372 262 M348 288 L370 288" stroke="{INK}" stroke-width="8" stroke-linecap="round" opacity=".5"/>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# THE SLIDES
# ══════════════════════════════════════════════════════════════════════════════
SLIDE_ACCENT = [A[0], A[4], A[2], A[0], A[3], A[1], A[5], A[6]]
TOTAL = 8

def slide_cover():
    """01 — dark ink base, giant type. The bookend."""
    acc = SLIDE_ACCENT[0]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{INK};z-index:0"></div>'
    deco = (field_rings(-120, 760, 720, acc, n=4, op=.22)
            + field_hatch(660, 940, 520, 520, A[2], op=.16, rot=-8)
            + field_blob(700, 120, 460, A[4], seed=6, op=.14))
    els += [("rings", 0, 800, 560, 560), ("hatch", 700, 960, 380, 420)]

    eb = eyebrow("friendship day &middot; 02.08.26", acc, dark=True, y=176)
    els.append(("eyebrow", M, 176, 380, 48))

    # giant stacked type — three lines, the third boxed
    t1 = (f'<div style="position:absolute;top:296px;left:{M}px;z-index:24;font-family:var(--d);'
          f'font-weight:900;font-size:150px;line-height:.88;letter-spacing:-.035em;color:{CREAM};'
          f'text-transform:uppercase">SIX<br>REASONS<br>TO</div>')
    els.append(("giant", M, 296, 700, 400))
    t2 = punch(acc, x=M - 6, y=716, rot=-2.6, fs=132, txt="wish them")
    els.append(("punchbox", M - 6, 716, 860, 190))

    sub = (f'<div style="position:absolute;top:962px;left:{M}px;width:820px;z-index:24;'
           f'font-family:var(--e);font-weight:400;font-size:40px;line-height:1.3;'
           f'letter-spacing:-.01em;color:rgba(244,239,224,.82)">there are more than six. '
           f'these are just the ones we could <span style="font-family:var(--s);font-style:italic;'
           f'color:{A[2]}">prove</span>.</div>')
    els.append(("sub", M, 962, 820, 120))

    swipe = (f'<div style="position:absolute;bottom:56px;right:{M}px;z-index:30;font-family:var(--m);'
             f'font-weight:700;font-size:16px;letter-spacing:.14em;text-transform:uppercase;'
             f'color:{CREAM};display:flex;align-items:center;gap:10px">swipe'
             f'<span style="display:inline-block;width:34px;height:3px;background:{acc}"></span>&rarr;</div>')
    els.append(("swipe", 820, H - 84, 190, 30))

    # sticker scatter — uniform die-cut treatment, varied silhouettes
    scat = (stick(sh.scallop(lobes=13, r=45), A[2], 792, 236, 190, rot=-12)
            + stick(sh.starburst(points=11), A[3], 668, 1128, 150, rot=8)
            + stick(sh.blob(seed=2), A[4], 856, 1216, 168, rot=-6)
            + doodle("sparkle", 596, 214, 92, A[0], rot=14, z=13)
            + doodle("heart", 44, 1148, 104, A[0], rot=-12, z=13))
    els += [("sc1", 792, 236, 190, 190), ("sc2", 668, 1128, 150, 150),
            ("sc3", 856, 1216, 168, 168), ("d1", 596, 214, 92, 92), ("d2", 44, 1148, 104, 104)]

    inner = bg + deco + logo(dark=True) + dots(0, TOTAL, dark=True) + eb + t1 + t2 + sub + scat + swipe
    return inner, els, True


def slide_line(i, txt_html, art_fn, art_xy, art_size, punch_y, text_y, field, extras="", art_rot=0):
    """02–07 — the six reasons. Same skeleton, different field geometry + illustration."""
    acc = SLIDE_ACCENT[i]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{CREAM};z-index:0"></div>'
    eb = eyebrow(f"reason {i:02d} &middot; of 06", acc, y=176)
    els.append(("eyebrow", M, 176, 320, 48))

    ax, ay = art_xy
    art = svgbox(art_fn(), ax, ay, art_size, rot=art_rot, z=14)
    els.append((f"art{i}", ax, ay, art_size, art_size))

    txt = line_text(txt_html, text_y)
    els.append((f"line{i}", M, text_y, 880, 150))

    p = punch(acc, x=M - 4, y=punch_y)
    els.append((f"punch{i}", M - 4, punch_y, 560, 130))

    inner = bg + field + logo() + dots(i, TOTAL) + eb + art + txt + p + extras + footer()
    return inner, els, False


def slide_closer():
    """08 — dark bookend + the CTA. Tag-them ask lives here, once, unmissable."""
    acc = SLIDE_ACCENT[7]; els = []
    bg = f'<div style="position:absolute;inset:0;background:{INK};z-index:0"></div>'
    deco = (field_checker(0, 1108, 1160, 340, A[2], cell=58, op=.13, rot=-3)
            + field_rings(700, -140, 640, acc, n=4, op=.26)
            + field_blob(-160, 900, 520, acc, seed=8, op=.13))
    els += [("chk", 0, 1140, 1080, 300), ("rings", 760, 0, 320, 400)]

    eb = eyebrow("that's the whole post", acc, dark=True, y=176)
    els.append(("eyebrow", M, 176, 400, 48))

    t1 = (f'<div style="position:absolute;top:300px;left:{M}px;width:880px;z-index:24;'
          f'font-family:var(--e);font-weight:400;font-size:56px;line-height:1.2;'
          f'letter-spacing:-.02em;color:rgba(244,239,224,.9)">you don\'t need '
          f'<span style="font-family:var(--s);font-style:italic;color:{A[2]}">a</span> reason.</div>')
    els.append(("t1", M, 300, 880, 80))

    t2 = (f'<div style="position:absolute;top:400px;left:{M}px;z-index:24;font-family:var(--d);'
          f'font-weight:900;font-size:124px;line-height:.9;letter-spacing:-.035em;color:{CREAM};'
          f'text-transform:uppercase">YOU HAVE<br>A HUNDRED.</div>')
    els.append(("t2", M, 400, 800, 240))

    t3 = punch(acc, x=M - 6, y=700, rot=-2.2, fs=92, txt="go wish them")
    els.append(("punch", M - 6, 700, 700, 150))

    t4 = (f'<div style="position:absolute;top:892px;left:{M}px;width:860px;z-index:24;'
          f'font-family:var(--e);font-weight:400;font-size:42px;line-height:1.28;'
          f'letter-spacing:-.01em;color:rgba(244,239,224,.86)">and '
          f'{em("tag them below", A[0])} &mdash; they&rsquo;ll pretend to be annoyed.</div>')
    els.append(("t4", M, 892, 860, 120))

    sign = (f'<div style="position:absolute;top:1044px;left:{M}px;z-index:24;font-family:var(--m);'
            f'font-weight:500;font-size:19px;letter-spacing:.05em;line-height:1.6;'
            f'color:rgba(244,239,224,.62)">happy friendship day,<br>'
            f'<span style="font-weight:700;color:{CREAM}">from all of us at aquaterra</span></div>')
    els.append(("sign", M, 1044, 520, 90))

    scat = (stick(sh.scallop(lobes=14, r=45), A[0], 792, 452, 200, rot=10)
            + stick(sh.tag(w=100, h=44), A[2], 812, 968, 176, rot=-8, box=100)
            + doodle("paw", 664, 1176, 112, A[0], rot=-10, z=15)
            + doodle("sparkle", 880, 1236, 88, A[2], rot=18, z=15))
    els += [("sc1", 792, 452, 200, 200), ("sc2", 812, 968, 176, 100),
            ("p1", 664, 1176, 112, 112), ("p2", 880, 1236, 88, 88)]

    inner = bg + deco + logo(dark=True) + dots(7, TOTAL, dark=True) + eb + t1 + t2 + t3 + t4 + sign + scat + footer(dark=True)
    return inner, els, True


# ── the six line slides, each with its own field geometry so none repeat ──────
def build_lines():
    S = []
    # 02 — 0.5x drives — sky
    acc = SLIDE_ACCENT[1]
    S.append(slide_line(
        1,
        f'if you&rsquo;ve only gone for drives to take {em("embarrassing 0.5x pics", acc)},',
        lambda: art_zerofive(acc, A[0]), (486, 268), 520, 1096, 900,
        field_band(-60, 232, 700, 620, acc, rot=-6, op=.20, radius=48)
        + field_rings(-190, 700, 560, A[0], n=3, op=.22),
        extras=doodle("zigzag", 92, 706, 150, acc, rot=6, z=13)))

    # 03 — 40km chai — lemon
    acc = SLIDE_ACCENT[2]
    S.append(slide_line(
        2,
        f'if you&rsquo;ve driven {em("40km for a chai", acc)} and called it a plan,',
        lambda: art_chai(acc, A[3]), (72, 288), 540, 1108, 908,
        field_checker(560, 236, 560, 560, acc, cell=56, op=.20, rot=5)
        + field_band(0, 856, 1080, 26, A[3], op=.6),
        extras=doodle("arrow", 690, 792, 160, A[3], rot=-8, z=13)))

    # 04 — reels — pink
    acc = SLIDE_ACCENT[3]
    S.append(slide_line(
        3,
        f'if you&rsquo;ve {em("bullied them into making a reel", acc)} in public,',
        lambda: art_reel(acc, A[4]), (500, 250), 530, 1096, 900,
        field_blob(-120, 250, 700, acc, seed=5, op=.20)
        + field_hatch(64, 620, 420, 300, A[4], op=.22, rot=-4),
        extras=doodle("lightning", 92, 262, 118, A[2], rot=-12, z=13)))

    # 05 — laughed first — tomato
    acc = SLIDE_ACCENT[4]
    S.append(slide_line(
        4,
        f'if you {em("laughed first", acc)} and asked if they were okay second,',
        lambda: art_ha(acc, A[2]), (96, 244), 560, 1112, 912,
        field_rings(560, 226, 620, acc, n=4, op=.24)
        + field_band(636, 830, 400, 22, A[2], rot=4, op=.85),
        extras=doodle("speech", 700, 686, 140, A[4], rot=10, z=13)))

    # 06 — showed up — mint
    acc = SLIDE_ACCENT[5]
    S.append(slide_line(
        5,
        f'if they&rsquo;ve {em("shown up without being asked", acc)},',
        lambda: art_door(acc, A[0]), (492, 254), 520, 1052, 892,
        field_band(-40, 236, 640, 600, A[2], rot=5, op=.26, radius=40)
        + field_checker(48, 690, 420, 300, acc, cell=48, op=.18, rot=-3),
        extras=doodle("star", 108, 274, 110, A[2], rot=12, z=13)))

    # 07 — silence — grape
    acc = SLIDE_ACCENT[6]
    S.append(slide_line(
        6,
        f'if you&rsquo;ve {em("sat in silence together", acc)} and it wasn&rsquo;t awkward,',
        lambda: art_silence(acc, A[6]), (86, 258), 560, 1112, 912,
        field_blob(560, 224, 620, acc, seed=7, op=.20)
        + field_hatch(620, 760, 440, 300, acc, op=.20, rot=6),
        extras=doodle("dots", 706, 690, 128, A[2], rot=0, z=13)))
    return S


# ══════════════════════════════════════════════════════════════════════════════
async def main():
    os.makedirs(OUT, exist_ok=True)
    slides = [slide_cover()] + build_lines() + [slide_closer()]
    for idx, (inner, els, dark) in enumerate(slides, start=1):
        bg = INK if dark else CREAM
        html = B.page(W, H, bg, inner, grain=True)
        pf = lay.preflight(W, H, els, html=html, page_bg=bg, core=core, expect_hero=False)
        path = f"{OUT}/v1_{idx:02d}.png"
        await B.render(html, path, W, H)
        print(f"  -> {path}  preflight_clean={pf.get('clean')}")
    print("DONE — 8 slides @ 1080x1440")

asyncio.run(main())
