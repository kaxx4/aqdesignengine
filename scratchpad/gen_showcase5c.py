"""SHOWCASE 5c — five more families, built DENSE.

CORRECTED LEARNING: showcase5b's low area readings were NOT mainly a texture artifact. After
denoising compare.py the ratios barely moved (0.39->0.42) — AQ output is genuinely UNDER-FILLED
against the corpus. The references are board-busy; AQ defaults airy. Everything here is built to
fill the frame: full-bleed fields, edge-cropped masses, and content pushed to all four margins.

 11 11e7d9a3ff  isometric keycaps -> extrude() fixed-direction slab shadows on graph paper
 12 1d518d2bc5  photo scatter     -> REAL AQ photos as rotated cards + label-to-item arrows
 13 2022ebef4f  card deck         -> same card duplicated 3x, decreasing scale, increasing rotation
 14 b2d4cc55d7  type sandwich     -> two headline bands clamping a cluster, cream reserved for type
 15 d252704dc5  quadrant patchwork-> hard field split + checkerboard + per-word sticker boxes
"""
import asyncio, os, sys, importlib.util, math
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
CREAM = "var(--bg)"
TON = core.text_on

def at(x, y, w, h, inner, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def logo(dark=False):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:40px;z-index:60;{sh}">'

def footer(light=False):
    c = "#FFFFFF" if light else "var(--ink)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:{c};z-index:60">@ngo.aquaterra</span>')

def eyebrow(txt, color="var(--ink)"):
    return (f'<span style="position:absolute;top:64px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:60">{txt}</span>')


# ── 11. ISOMETRIC KEYCAPS ─────────────────────────────────────────────────────
async def keycaps():
    grid = ('<svg style="position:absolute;inset:0;z-index:1" width="1080" height="1350" '
            'xmlns="http://www.w3.org/2000/svg">'
            + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1350" stroke="#9FC4D8" stroke-width="1.4"/>'
                      for x in range(0, 1081, 45))
            + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#9FC4D8" stroke-width="1.4"/>'
                      for y in range(0, 1351, 45)) + "</svg>")
    els = []
    word = "SHOW UP"
    xs = [70, 250, 430, 610, 790, 0, 250, 430, 610]
    k = 0
    for row, chunk in enumerate(["SHOW", "UP!"]):
        for i, ch in enumerate(chunk):
            x = 90 + i * 215 + (row * 120)
            y = 420 + row * 260
            acc = A[(k * 2) % 7]
            cap = S.extrude(S.capsule(100, 100), acc, depth=16, size=205, rot=0)
            els.append(at(x, y, 205, 205, cap, z=10 + k))
            els.append(at(x, y + 46, 205, 100,
                f'<div style="width:100%;text-align:center;font-family:var(--d);font-weight:900;'
                f'font-size:82px;color:{TON(acc)}">{ch}</div>', z=30 + k))
            k += 1
    # props scattered to the margins so the field fills (density learning)
    props = [(S.gear(9), A[3], 40, 190, 150, 8), (S.starburst(11), A[0], 880, 240, 160, -12),
             (S.blob(3, 8), A[1], 860, 980, 175, 0), (S.tag(100, 44), A[5], 60, 1010, 210, 6),
             (S.scallop(12), A[2], 470, 1060, 165, -8), (S.shield(), A[6], 900, 640, 130, 10)]
    for d, f, x, y, s, r in props:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=True, rot=r), z=40))
    inner = ('<div style="position:absolute;inset:0;background:#DCEAF2"></div>' + grid
             + "".join(els) + logo() + footer() + eyebrow("AQ · KEYS TO SHOWING UP"))
    return B.page(W, H, "#DCEAF2", inner, grain=True)


# ── 12. PHOTO SCATTER + LABEL ARROWS ──────────────────────────────────────────
async def photo_scatter():
    """Real AQ photos (core.PHOTOS) as rotated cards — satisfies the real-assets rule — with
    handwritten-style labels bound to each card by a curved arrow (the 1d518d2bc5 steal)."""
    els = []
    cards = [("food", 90, 380, 400, 330, -5, A[3]), ("edu", 560, 300, 420, 350, 4, A[4]),
             ("diwali", 130, 780, 380, 320, 6, A[2]), ("xmas", 590, 760, 400, 340, -4, A[1])]
    for key, x, y, w, h, r, acc in cards:
        img = core.PHOTOS.get(key, "")
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:#fff;border:6px solid var(--ink);'
            f'box-shadow:10px 10px 0 var(--ink);padding:14px 14px 46px 14px;box-sizing:border-box">'
            f'<img src="{img}" style="width:100%;height:100%;object-fit:cover;display:block">'
            f'</div>', z=12, rot=r))
        els.append(at(x + w - 90, y - 34, 88, 88,
                      S.sticker(S.scallop(11), acc, size=88, halo=True), z=20, rot=r * 2))
    title = (f'<div style="position:absolute;top:150px;left:{M}px;font-family:var(--d);font-weight:900;'
             f'font-size:84px;line-height:.9;text-transform:uppercase;color:var(--ink);z-index:30">'
             f'what a year</div>')
    arrows = ('<svg style="position:absolute;inset:0;z-index:28" width="1080" height="1350" '
              'xmlns="http://www.w3.org/2000/svg">'
              '<path d="M520 300 C560 340 545 380 505 392" fill="none" stroke="#0A0A0A" '
              'stroke-width="6" stroke-linecap="round"/>'
              '<path d="M534 360 L500 396 L540 404" fill="none" stroke="#0A0A0A" stroke-width="6" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    band = (f'<div style="position:absolute;bottom:120px;left:0;right:0;background:var(--ink);'
            f'padding:24px 64px;font-family:var(--d);font-weight:900;font-size:52px;'
            f'text-transform:uppercase;color:#fff;z-index:40">4 programmes. 1,200 of us.</div>')
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + title + "".join(els) + arrows + band + logo() + footer(True) + eyebrow("AQ · RECAP"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 13. CARD DECK (repetition as composition) ─────────────────────────────────
async def card_deck():
    """2022ebef4f steal: duplicate the SAME card 3x at decreasing scale and increasing rotation,
    offset down-left, so one message becomes a stacked deck. Repetition IS the composition."""
    els = []
    for i, (sc, rot, dx, dy) in enumerate([(1.0, -3, 0, 0), (0.92, 6, -46, 40), (0.84, 13, -92, 82)]):
        w, h = int(620 * sc), int(520 * sc)
        z = 20 - i * 3
        els.append(at(300 + dx, 400 + dy, w, h,
            f'<div style="width:100%;height:100%;background:#FFF;border:6px solid var(--ink);'
            f'box-shadow:12px 12px 0 rgba(0,0,0,.45);display:flex;flex-direction:column;'
            f'align-items:center;justify-content:center;gap:10px">'
            f'<div style="font-family:var(--m);font-weight:700;font-size:{int(20*sc)}px;'
            f'letter-spacing:.18em">SATURDAY</div>'
            f'<div style="font-family:var(--d);font-weight:900;font-size:{int(96*sc)}px;'
            f'line-height:.9;text-transform:uppercase;text-align:center">clean<br>up</div>'
            f'<div style="font-family:var(--e);font-weight:600;font-size:{int(24*sc)}px;'
            f'opacity:.7">diamond harbour · 7am</div></div>', z=z, rot=rot))
    props = [(S.starburst(11), A[2], 760, 300, 200, 12), (S.gear(9), A[4], 820, 900, 185, 0),
             (S.blob(7, 8), A[1], 90, 300, 190, 0), (S.tag(100, 44), A[5], 60, 980, 240, -7),
             (S.scallop(13), A[6], 680, 1080, 170, 9), (S.shield(), A[2], 120, 640, 140, 6)]
    for d, f, x, y, s, r in props:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=True, rot=r), z=30))
    inner = (f'<div style="position:absolute;inset:0;background:{A[3]}"></div>' + "".join(els)
             + logo(True) + footer(True) + eyebrow("AQ · EVERY SATURDAY", "#FFFFFF"))
    return B.page(W, H, A[3], inner, grain=True)


# ── 14. TYPE SANDWICH ─────────────────────────────────────────────────────────
async def type_sandwich():
    """b2d4cc55d7: two cut-paper headline bands clamp a dense central cluster on a FLOODED
    saturated field. Guard rail that makes flooding survivable: ONE colour reserved exclusively
    for type (cream here) and forbidden in every illustration fill."""
    TYPE_ONLY = "#F4EFE0"
    top = (f'<div style="position:absolute;top:170px;left:0;right:0;text-align:center;'
           f'font-family:var(--d);font-weight:900;font-size:150px;line-height:.86;'
           f'text-transform:uppercase;color:{TYPE_ONLY};z-index:30">and all</div>')
    bot = (f'<div style="position:absolute;bottom:170px;left:0;right:0;text-align:center;'
           f'font-family:var(--d);font-weight:900;font-size:150px;line-height:.86;'
           f'text-transform:uppercase;color:{TYPE_ONLY};z-index:30">that work</div>')
    els = []
    cluster = [(S.gear(11), A[2], 300, 500, 300, -6), (S.scallop(14), A[0], 560, 470, 260, 8),
               (S.starburst(12), A[3], 190, 720, 230, 12), (S.blob(4, 8), A[1], 700, 690, 250, 0),
               (S.tag(100, 44), A[5], 430, 760, 280, -5), (S.shield(), A[6], 760, 470, 170, 10),
               (S.capsule(100, 40), A[2], 130, 560, 210, -14), (S.arch(), A[0], 620, 860, 190, 4)]
    for d, f, x, y, s, r in cluster:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=True, rot=r), z=20))
    inner = (f'<div style="position:absolute;inset:0;background:{A[4]}"></div>' + top + bot
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · 2026", TYPE_ONLY))
    return B.page(W, H, A[4], inner, grain=True)


# ── 15. QUADRANT PATCHWORK ────────────────────────────────────────────────────
async def patchwork():
    """d252704dc5: canvas split into hard-edged fields (ink / cream / checkerboard) with type
    straddling the seams, plus per-WORD tilted sticker boxes (shapes.word_boxes)."""
    fields = (f'<div style="position:absolute;top:0;left:0;right:0;height:640px;background:#0A0A0A;z-index:1"></div>'
              f'<div style="position:absolute;top:640px;left:0;width:520px;height:710px;z-index:1">'
              f'{S.checker(520, 710, 52, A[0], A[3])}</div>'
              f'<div style="position:absolute;top:640px;left:520px;right:0;height:710px;'
              f'background:{CREAM};z-index:1"></div>')
    serif = (f'<div style="position:absolute;top:120px;left:{M}px;font-family:var(--s);font-style:italic;'
             f'font-size:56px;color:{CREAM};z-index:20">the volunteer series</div>')
    words = S.word_boxes(["IT'S NOT", "YOU. IT'S", "THE SYSTEM"], [A[4], A[2], A[5]],
                         fs=72, x=90, y=250, text_on=TON)
    big = (f'<div style="position:absolute;bottom:120px;right:{M}px;width:470px;font-family:var(--s);'
           f'font-style:italic;font-size:70px;line-height:.95;color:var(--ink);z-index:22;'
           f'text-align:right">so we built<br>a way in.</div>')
    els = [at(120, 700, 200, 200, S.sticker(S.starburst(12), A[2], size=200, halo=True,
              inner=S.label("EP 02", 15, 56)), z=30, rot=-9),
           at(330, 940, 165, 165, S.sticker(S.scallop(13), A[6], size=165, halo=True), z=30, rot=7),
           at(600, 660, 150, 150, S.sticker(S.gear(9), A[3], size=150, halo=True), z=30)]
    inner = (fields + serif + f'<div style="position:absolute;inset:0;z-index:20">{words}</div>'
             + "".join(els) + big + logo(True) + footer(True) + eyebrow("AQ · SERIES", CREAM))
    return B.page(W, H, CREAM, inner, grain=True)


JOBS = [("11_keycaps", keycaps), ("12_photo_scatter", photo_scatter),
        ("13_card_deck", card_deck), ("14_type_sandwich", type_sandwich),
        ("15_patchwork", patchwork)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
