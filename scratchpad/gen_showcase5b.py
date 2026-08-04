"""SHOWCASE 5b — five MORE reference families, built on engine/shapes.py.
Applies the systematic finding from showcase5: compositions ran ~0.85x area and sat too high,
leaving dead bottom regions. Everything here is built BIGGER and LOWER from the first pass.

  6  64b2248475  ghost-type bleed   -> stroke-only headline overflowing all 4 edges, z=0
  7  487e800350  card grid board    -> rounded masonry on ink + ticker bar + seam-straddling stickers
  8  d375fd7dbc  annotated map      -> tilted title plate + two-plate labels + connector arcs
  9  eaad68d630  slab banners       -> alternating tilted title slabs + cropped hero + badges
 10  502e07d0eb  hero-less scatter  -> object pile, rotation jitter, silhouette alternation, NO focal
"""
import asyncio, os, sys, importlib.util, math
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS                    # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
CREAM = "var(--bg)"

def at(x, y, w, h, inner, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def logo(dark=False):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:40px;z-index:40;{sh}">'

def footer(light=False):
    c = "#FFFFFF" if light else "var(--ink)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:{c};z-index:40">@ngo.aquaterra</span>')

def eyebrow(txt, color="var(--ink)"):
    return (f'<span style="position:absolute;top:64px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:40">{txt}</span>')

def plate(txt, bg, fg, fs=30, pad="14px 26px", rot=0, shadow=True):
    sh = "box-shadow:7px 7px 0 var(--ink);" if shadow else ""
    return (f'<div style="display:inline-block;background:{bg};color:{fg};border:5px solid var(--ink);'
            f'border-radius:12px;padding:{pad};{sh}font-family:var(--d);font-weight:900;'
            f'font-size:{fs}px;letter-spacing:.01em;white-space:nowrap;transform:rotate({rot}deg)">{txt}</div>')


# ── 6. GHOST-TYPE BLEED ───────────────────────────────────────────────────────
async def ghost_type():
    """The 64b2248475 steal: re-set the headline at ~4x, STROKE ONLY, overflowing every edge,
    z=0. Free density + texture with zero new assets — and it is exactly the move bounds_check
    currently forbids, which is why this archetype was unreachable."""
    ghost = (f'<div style="position:absolute;top:-120px;left:-180px;width:1500px;'
             f'font-family:var(--d);font-weight:900;font-size:430px;line-height:.8;'
             f'text-transform:uppercase;color:transparent;'
             f'-webkit-text-stroke:6px rgba(255,255,255,.55);z-index:1">SHOW UP SHOW UP</div>')
    # hero object cluster, LOW and BIG (showcase5 learning)
    hero = []
    for d, f, x, y, s, r in [(S.scallop(16), A[2], 330, 560, 420, -5),
                             (S.gear(10), A[3], 640, 800, 250, 0),
                             (S.starburst(12), A[0], 190, 880, 210, 10),
                             (S.blob(9, 8), A[1], 720, 560, 190, 0)]:
        hero.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=True, rot=r,
                     inner=(S.label("EVERY", 17, 40) + S.label("SUNDAY", 17, 62)) if s > 400 else ""), z=12))
    band = (f'<div style="position:absolute;bottom:150px;left:0;right:0;background:var(--ink);'
            f'border-top:6px solid #FFF;border-bottom:6px solid #FFF;padding:26px 64px;'
            f'font-family:var(--d);font-weight:900;font-size:74px;line-height:.95;'
            f'text-transform:uppercase;color:#FFF;z-index:20">volunteer sundays</div>')
    inner = (f'<div style="position:absolute;inset:0;background:{A[5]}"></div>' + ghost
             + "".join(hero) + band + logo(True) + footer(True) + eyebrow("AQ · KOLKATA", "#FFFFFF"))
    return B.page(W, H, A[5], inner, grain=True)


# ── 7. CARD GRID BOARD ────────────────────────────────────────────────────────
async def card_grid():
    """Highest-demand missing archetype (~5 refs). Rounded masonry on ink, one saturated fill per
    card, generous gutters, a full-width ticker bar divider, and one repeated brand glyph
    STRADDLING card seams to stitch the grid (the 4c6df2b479 steal)."""
    els = []
    cards = [  # x, y, w, h, accent, big text, small text
        (M, 300, 600, 330, A[4], "beach<br>cleanup", "diamond harbour"),
        (M + 620, 300, 332, 330, A[2], "12<br>drives", "this month"),
        (M, 650, 460, 300, A[0], "school<br>kits", "khidirpur"),
        (M + 480, 650, 472, 300, A[1], "medical<br>camp", "sunderbans"),
        (M, 1090, 952, 150, A[5], "dm to join", ""),
    ]
    for x, y, w, h, acc, big, small in cards:
        fg = core.text_on(acc)
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:34px;'
            f'padding:30px 34px;box-sizing:border-box;display:flex;flex-direction:column;'
            f'justify-content:space-between">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:{54 if h>200 else 40}px;'
            f'line-height:.92;text-transform:uppercase;color:{fg}">{big}</div>'
            f'<div style="font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.1em;'
            f'text-transform:uppercase;color:{fg};opacity:.8">{small}</div></div>', z=10))
    # ticker bar divider (the 487e800350 steal)
    words = " ★ ".join(["SHOW UP", "NO FEES", "RUN BY TEENAGERS", "SINCE 2021"])
    els.append(at(M, 985, 952, 78,
        f'<div style="width:100%;height:100%;background:{A[6]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center;font-family:var(--m);font-weight:700;'
        f'font-size:19px;letter-spacing:.12em;color:#FFF;overflow:hidden">{words}</div>', z=12))
    # seam-straddling stickers: stitch the grid instead of leaving it a tile set
    for x, y, s, acc, sh in [(600, 600, 110, A[3], S.starburst(9)),
                             (500, 940, 92, A[2], S.scallop(11)),
                             (955, 610, 86, A[0], S.blob(5, 7))]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s, halo=True), z=20, rot=-8))
    title = (f'<div style="position:absolute;top:150px;left:{M}px;font-family:var(--d);font-weight:900;'
             f'font-size:88px;line-height:.9;text-transform:uppercase;color:#FFF;z-index:20">'
             f'august board</div>')
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>' + title
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · PROGRAMMES", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


# ── 8. ANNOTATED MAP ──────────────────────────────────────────────────────────
async def annotated_map():
    """d375fd7dbc steal: every data point is a TWO-PLATE stack — white plate = name, inverted
    ink plate = value — rotated together and slightly overlapped, so a list reads as a
    label-maker artifact. Plus connector arcs from each origin to the destination pin."""
    els = []
    pts = [("HOWRAH", "2h 10m", 120, 430, -6), ("SALT LAKE", "2h 40m", 560, 360, 4),
           ("BEHALA", "2h 25m", 130, 700, 3), ("BARASAT", "3h 05m", 620, 640, -4),
           ("GARIA", "1h 55m", 300, 940, 5)]
    for name, val, x, y, r in pts:
        els.append(at(x, y, 300, 130,
            plate(name, "#FFFFFF", "#0A0A0A", 30, "12px 22px", 0)
            + f'<div style="height:8px"></div>'
            + plate(val, "#0A0A0A", "#FFFFFF", 24, "9px 18px", 0), z=14, rot=r))
        els.append(at(x + 240, y - 26, 54, 54,
                      S.sticker(S.starburst(8), A[2], size=54, halo=False), z=15))
    # destination pin, low-right (bigger + lower per showcase5 learning)
    els.append(at(700, 1010, 190, 190, S.sticker(S.starburst(12), A[3], size=190, halo=True,
                  inner=S.label("CAMP", 15, 56, fill="#FFFFFF")), z=16, rot=-8))
    arcs = ('<svg style="position:absolute;left:0;top:0;width:1080px;height:1350px;z-index:8" '
            'xmlns="http://www.w3.org/2000/svg">')
    for _, _, x, y, _ in pts:
        arcs += (f'<path d="M{x+150} {y+70} Q{(x+790)/2} {(y+1105)/2 - 90} 790 1105" fill="none" '
                 f'stroke="#FFFFFF" stroke-width="3" stroke-dasharray="3 10" opacity=".65"/>')
    arcs += "</svg>"
    title = at(150, 200, 660, 130,
               plate("OTW TO SUNDERBANS", "#FFFFFF", "#0A0A0A", 46, "20px 34px"), z=20, rot=-3)
    inner = (f'<div style="position:absolute;inset:0;background:{A[4]}"></div>' + arcs
             + title + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · ROUTES", "#FFFFFF"))
    return B.page(W, H, A[4], inner, grain=True)


# ── 9. SLAB BANNERS ───────────────────────────────────────────────────────────
async def slab_banners():
    """eaad68d630 steal: a stacked title gets ONE slab per line in alternating accents, each
    tilted the opposite way (+3/-3) with a hard ink shadow — reads as a nailed-up sign."""
    els = []
    # LOOKING GATE FIX: slabs were spaced 130px while each is ~130px tall, so each one clipped the
    # text of the slab above it. Space by slab HEIGHT + a real gap, never a guessed constant.
    for i, (txt, acc, x, y, fs) in enumerate([("THE", A[1], 110, 290, 92),
                                              ("SHOW-UP", A[3], 150, 460, 92),
                                              ("SERIES", A[5], 210, 630, 92)]):
        fg = core.text_on(acc)
        els.append(at(x, y, 760, 150, plate(txt, acc, fg, fs, "18px 40px"), z=20 + i, rot=(-3 if i % 2 else 3)))
    # cropped hero object, bleeding off the bottom edge (intentional off-frame)
    els.append(at(560, 830, 520, 520, S.sticker(S.gear(12), A[6], size=520, halo=True), z=12, rot=-10))
    # speech bubble + badge
    # LOOKING GATE FIX: this bubble was A[2] — the SAME colour as the page field — so it read as
    # an empty outline. layout.invisible_color_check exists for exactly this, but it is opt-in and
    # this script never passed color_pairs, so it silently did not run. Use the cream instead.
    els.append(at(110, 830, 330, 150,
        f'<div style="width:100%;height:100%;background:{CREAM};border:5px solid var(--ink);'
        f'border-radius:34px;box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;'
        f'justify-content:center;font-family:var(--e);font-weight:700;font-size:27px;'
        f'color:var(--ink);text-align:center">every friday.<br>real stories.</div>', z=18, rot=-2))
    els.append(at(120, 1030, 210, 210, S.sticker(S.scallop(13), A[0], size=210, halo=True,
                  inner=S.label("EP", 16, 44, fill="#FFFFFF") + S.label("01", 22, 70, fill="#FFFFFF")),
                  z=18, rot=8))
    inner = (f'<div style="position:absolute;inset:0;background:{A[2]};opacity:1"></div>'
             f'<div style="position:absolute;inset:0;background:{A[2]}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · PODCAST"))
    return B.page(W, H, A[2], inner, grain=True)


# ── 10. HERO-LESS SCATTER ─────────────────────────────────────────────────────
async def heroless_scatter():
    """502e07d0eb: deliberately NO dominant element — a scan pattern, not a reading axis.
    dominance_check would reject this layout outright (VISUAL_DNA §6), which is precisely why
    the archetype was unreachable. Rotation jitter +-18 deg and never two same silhouettes adjacent."""
    els = []
    fams = [S.shield(), S.tag(100, 44), S.arch(), S.capsule(100, 40), S.starburst(9),
            S.scallop(12), S.blob(2, 7), S.gear(8), S.wave_banner(100, 44, 1.5, 7)]
    labels = ["WELFARE", "CLIMATE", "EDU", "ANIMALS", "HEALTH", "FOOD", "TREES", "BOOKS", "DOGS"]
    # loose 3-col jitter grid, filling the frame (no focal, even weight)
    k = 0
    for r in range(4):
        for c in range(3):
            if k >= 11:
                break
            x = 90 + c * 320 + (40 if r % 2 else -20)
            y = 250 + r * 250 + (30 if c % 2 else 0)
            s = 200 + (40 if (r + c) % 3 == 0 else 0)
            d = fams[k % len(fams)]
            acc = A[(k * 3) % 7]
            fg = core.text_on(acc)
            els.append(at(x, y, s, s, S.sticker(d, acc, size=s, halo=True,
                          rot=((k * 37) % 36) - 18,
                          inner=S.label(labels[k % len(labels)], 11, 54, fill=fg)), z=10 + k))
            k += 1
    inner = ('<div style="position:absolute;inset:0;background:#EDEAE3"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · EVERY LANE"))
    return B.page(W, H, "#EDEAE3", inner, grain=True)


JOBS = [("06_ghost_type", ghost_type), ("07_card_grid", card_grid),
        ("08_annotated_map", annotated_map), ("09_slab_banners", slab_banners),
        ("10_heroless_scatter", heroless_scatter)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
