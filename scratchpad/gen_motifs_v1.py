"""AQ session 10b — four motifs lifted from the new reference dump, built for the
first time. Content is real: workshop titles and counts from welfare_projects_rows.csv.

  A  STICKER SWARM       ref 2af2568a — badges of varied silhouette overlapping a
                         headline on an ink field, some behind the type, some in front
  B  STAGGERED BLEED     ref 62f8cc4d — pill rows offset like brickwork, bleeding off
                         BOTH edges so the field reads as endless
  C  DUOTONE PHOTO       a real AQ photo through tex.duotone (two plates, keeps faces)
  D  NOTCHED SLABS       ref 911d9ad8 — interlocking rounded blocks with a puzzle notch
"""
import asyncio, os, sys, csv, io, collections, importlib.util, math

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
lay = load("layout"); tex = load("tex"); sh = load("shapes")

ROWS = list(csv.DictReader(io.open(r"C:\Users\kanis\Downloads\welfare_projects_rows.csv",
                                   encoding="utf-8")))
OBJ = collections.Counter(r["objective"] for r in ROWS)
LOC = collections.Counter(r["location"].strip() for r in ROWS if r["location"].strip())
PARTNERS = len(LOC)
VOLS = sum(int(r["volunteers"]) for r in ROWS if (r["volunteers"] or "").strip().isdigit())

INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
PINK, MINT, LEMON, TOMATO, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/session10b"
os.makedirs(OUT, exist_ok=True)
W, H = core.SIZES["feed"]
M = 64


def sticker(kind, fill, size, label=None, rot=0, fs=13, lines=1, shadow=True):
    """One badge in the uniform AQ die-cut treatment: pale halo of its own fill,
    ink outline, hard offset. The uniformity is what makes nine unrelated colours
    read as one set (VISUAL_DNA §1)."""
    paths = {
        "scallop":   lambda: sh.scallop(lobes=13, r=45),
        "blob":      lambda: sh.blob(seed=7, lobes=8, r=44, wobble=.2),
        "burst":     lambda: sh.starburst(points=13, R=48, r=33),
        "gear":      lambda: sh.gear(teeth=11, R=46, r=36),
        "shield":    lambda: sh.shield(100, 100),
        "arch":      lambda: sh.arch(100, 100, 5),
        "capsule":   lambda: sh.capsule(100, 56),
        "tag":       lambda: sh.tag(100, 54, 15),
    }
    d = paths.get(kind, paths["scallop"])()
    inner = ""
    if label:
        fg = core.text_on(fill)
        ls = label.split("|")
        y0 = 50 - (len(ls) - 1) * (fs * 0.56)
        inner = "".join(sh.label(t, size=fs, y=y0 + i * fs * 1.12, fill=fg, weight=800)
                        for i, t in enumerate(ls))
    return sh.sticker(d, fill, size=size, rot=rot, inner=inner, shadow=shadow, detail="none")


def place(svg, x, y, size, z=10):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;'
            f'height:{size}px;z-index:{z}">{svg}</div>')


def footer(ground, right=""):
    c = INK if ground == CREAM else CREAM
    out = (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);'
           f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{c};z-index:40">'
           f'@ngo.aquaterra</span>')
    if right:
        out += (f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);'
                f'font-weight:700;font-size:15px;color:{c};opacity:.55;z-index:40">{right}</span>')
    return out


# ════════════════════════════════════════════════════════════════════════════
# A — STICKER SWARM
# ════════════════════════════════════════════════════════════════════════════
async def piece_a():
    m = await B.measure_text([
        {"text": "WE JUST<br>KEEP<br>SHOWING UP.", "font": "d", "size": 150, "weight": 900,
         "line_height": 0.86, "max_width": W - 2 * M},
    ])
    head_h = m[0]["h"]
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')
    P.append(B.logo(dark=True))
    P.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{CREAM};opacity:.55;'
             f'z-index:40">{PARTNERS} PARTNER ORGS</span>')

    hy = 430
    P.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{hy}px;left:{M}px;'
             f'width:{W-2*M}px;font-family:var(--d);font-weight:900;font-size:150px;'
             f'line-height:.86;letter-spacing:-.03em;color:{CREAM};z-index:20">'
             f'WE JUST<br>KEEP<br>SHOWING UP.</div>')
    els.append(("title", M, hy, W - 2 * M, head_h))

    # The swarm. Half sit BEHIND the type (z<20) and half in FRONT (z>20) — that
    # interleaving is what makes the pile read as depth rather than a border.
    swarm = [
        ("scallop", LEMON,  190, "ALL|WELFARE",              -11, 15, 12, 268),
        ("burst",   PINK,   168, f"{OBJ['Workshop']}|WORKSHOPS",  9, 14, 12, 690),
        ("blob",    SKY,    158, "SUNDARBANS",               -6, 13, 12, 470),
        ("capsule", MINT,   206, "PATHER SATHI",              7, 13, 26, 122),
        ("gear",    GRAPE,  146, "EK TARA",                 -14, 13, 30, 856),
        ("tag",     TOMATO, 196, "DOG FEEDS",                 6, 13, 26, 640),
        ("arch",    LEMON,  150, f"{OBJ['Plantation Drive']}|DRIVES", -8, 13, 30, 900),
        ("shield",  MINT,   142, "DISHA",                    11, 13, 26, 300),
        ("blob",    PINK,   132, "SINCE|2021",               -9, 12, 30, 62),
        ("scallop", SKY,    138, "KOLKATA",                   8, 12, 30, 812),
    ]
    ys = [252, 236, 300, 286, 262, 806, 820, 852, 880, 866]
    for (kind, fill, size, lab, rot, fs, z, x), y in zip(swarm, ys):
        P.append(place(sticker(kind, fill, size, lab, rot, fs), x, y, size, z))
        els.append((f"stk_{lab[:6]}", *lay.rotated_bbox(x, y, size, size, rot)))

    P.append(f'<div style="position:absolute;top:{hy+head_h+34}px;left:{M}px;width:760px;'
             f'font-family:var(--e);font-size:28px;line-height:1.45;color:{CREAM};opacity:.72;'
             f'z-index:20">{len(ROWS)} logged welfare projects across {PARTNERS} partner '
             f'organisations. the same rooms, again and again.</div>')
    P.append(footer(INK, f"{VOLS:,} VOLUNTEER TURNOUTS"))
    return B.page(W, H, INK, "".join(P), grain=False), f"{OUT}/A_sticker_swarm.png", els, INK


# ════════════════════════════════════════════════════════════════════════════
# B — STAGGERED BLEED ROWS
# ════════════════════════════════════════════════════════════════════════════
async def piece_b():
    titles = ["Roots in Mud", "Beyond the Stars", "Echoes of Joy", "One for All",
              "Speak Skillfully", "Life in a Bottle", "Hands at Work", "Green Hour",
              "Smiles Shared", "Heal The Earth", "Bottled Greens", "Act It Out",
              "Planet First", "Sentence Secrets", "Fun Fiesta", "Roots Rise",
              "Green Christmas", "World Health Day", "Cookie Pass On", "Mini-Fete"]
    FS = 34
    m = await B.measure_text([{"text": t, "font": "e", "size": FS, "weight": 600} for t in titles])
    widths = [x["w"] for x in m]

    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')

    hues = [MINT, SKY, LEMON, PINK, TOMATO, GRAPE, TEAL]
    PAD, DOT, GAP, RH, RGAP = 30, 22, 22, 78, 18
    rows_y, offsets = [], [-150, -60, -240, -110, -300, -40, -190, -90]
    y = 250
    idx = 0
    ri = 0
    while y < H - 190 and idx < len(titles):
        x = offsets[ri % len(offsets)]
        while x < W + 40 and idx < len(titles):
            tw = widths[idx]
            pw = PAD + DOT + 14 + tw + PAD
            c = hues[idx % len(hues)]
            # each pill is a NESTED structure: the label lives inside the pill, so the
            # browser enforces the fit and measure_dom reports any clip for free.
            P.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;width:{pw}px;height:{RH}px;'
                f'background:{PAPER};border:3px solid {INK};border-radius:999px;'
                f'box-shadow:{core.hard_shadow("lg")};z-index:6;overflow:hidden;'
                f'display:flex;align-items:center;padding:0 {PAD}px;gap:14px">'
                f'<span style="flex:0 0 {DOT}px;width:{DOT}px;height:{DOT}px;border-radius:50%;'
                f'background:{c};border:2px solid {INK}"></span>'
                f'<span style="font-family:var(--e);font-weight:600;font-size:{FS}px;'
                f'color:{INK};white-space:nowrap">{titles[idx]}</span></div>')
            els.append((f"pill{idx}", x, y, pw, RH))
            x += pw + GAP
            idx += 1
        y += RH + RGAP
        ri += 1

    # the headline sits ON the field as an ink slab — rule 3: ink is an accent, never the page
    m2 = await B.measure_text([{"text": "TWENTY OF<br>THE 291.", "font": "d", "size": 118,
                                "weight": 900, "line_height": .88, "max_width": 700}])
    bh = m2[0]["h"] + 76
    by = int(H * 0.40)
    P.append(f'<div style="position:absolute;left:{M}px;top:{by}px;width:{W-2*M}px;height:{bh}px;'
             f'background-color:{INK};border-radius:{core.RADII["outer"]}px;'
             f'box-shadow:{core.hard_shadow("xl")};z-index:18;overflow:hidden;padding:38px 42px">'
             f'<div style="font-family:var(--d);font-weight:900;font-size:118px;line-height:.88;'
             f'letter-spacing:-.03em;color:{CREAM}">TWENTY OF<br>THE 291.</div></div>')
    els.append(("band", M, by, W - 2 * M, bh))
    P.append(f'<div style="position:absolute;left:{M+8}px;top:{by+bh+16}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{core.on_cream(MINT,15)};'
             f'z-index:20">EVERY WORKSHOP WE RAN HAS A NAME</div>')

    P.append(B.logo())
    P.append(footer(CREAM, "WORKSHOPS 2021-2026"))
    return B.page(W, H, CREAM, "".join(P), grain=False), f"{OUT}/B_bleed_rows.png", els, CREAM


# ════════════════════════════════════════════════════════════════════════════
# C — DUOTONE PHOTO
# ════════════════════════════════════════════════════════════════════════════
async def piece_c():
    m = await B.measure_text([{"text": "THE CLASSROOM<br>IS A BOAT RIDE<br>AWAY.", "font": "d",
                               "size": 92, "weight": 900, "line_height": .9, "max_width": 880}])
    hh = m[0]["h"]
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')

    # two-plate riso: darks -> ink, lights -> mint. Keeps photographic detail, unlike
    # the old single-tint wrap which pushed everything to one muddy mid-tone.
    PX, PY, PW, PH = M, 196, W - 2 * M, 620
    P.append(f'<div style="position:absolute;left:{PX}px;top:{PY}px;width:{PW}px;height:{PH}px;'
             f'border:5px solid {INK};border-radius:{core.RADII["outer"]}px;overflow:hidden;'
             f'box-shadow:{core.hard_shadow("xl")};z-index:6">'
             + tex.duotone(core.PHOTOS["edu"], shadow=INK, highlight=MINT,
                           size_css=f"width:{PW}px;height:{PH}px", screen=True, screen_size=6)
             + '</div>')
    els.append(("photo", PX, PY, PW, PH))

    P.append(B.logo(dark=True))
    P.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{core.on_cream(MINT,15)};'
             f'z-index:40">EDUCATION &middot; SUNDARBANS</span>')

    stk = sticker("burst", LEMON, 188, "FIELD|PROGRAM", rot=-12, fs=14)
    sx, sy = W - M - 150, PY + PH - 110
    P.append(place(stk, sx, sy, 188, 22))
    els.append(("stk", *lay.rotated_bbox(sx, sy, 188, 188, -12)))

    ty = PY + PH + 46
    P.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{ty}px;left:{M}px;'
             f'width:880px;font-family:var(--d);font-weight:900;font-size:92px;line-height:.9;'
             f'letter-spacing:-.025em;color:{INK};z-index:10">'
             f'THE CLASSROOM<br>IS A BOAT RIDE<br>AWAY.</div>')
    els.append(("title", M, ty, 880, hh))

    P.append(f'<div style="position:absolute;top:{ty+hh+26}px;left:{M}px;width:820px;'
             f'font-family:var(--e);font-size:26px;line-height:1.45;color:{INK};opacity:.78;'
             f'z-index:10">ten sundarbans relief runs logged. the delta does not have '
             f'a bus route.</div>')
    P.append(footer(CREAM, "SUNDARBANS RELIEF \u00b7 10 RUNS"))
    return B.page(W, H, CREAM, "".join(P), grain=False), f"{OUT}/C_duotone_photo.png", els, CREAM


# ════════════════════════════════════════════════════════════════════════════
# D — NOTCHED INTERLOCKING SLABS
# ════════════════════════════════════════════════════════════════════════════
async def piece_d():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')
    P.append(B.logo())
    P.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{INK};opacity:.5;'
             f'z-index:40">THE SHAPE OF THE WORK</span>')

    blocks = [
        (MINT,   f"{OBJ['Workshop']}",            "CLASSROOM WORKSHOPS", 268, tex.crosshatch(INK, 14, 2, .13)),
        (SKY,    f"{OBJ['Distribution Drive']}",  "DISTRIBUTION DRIVES", 208, tex.stripes(INK, None, 3, 22, -40, .14)),
        (LEMON,  f"{OBJ['Feeding Dogs']}",        "DOG FEEDING RUNS",    176, tex.dot_grid(INK, 20, 3, .16)),
        (TOMATO, f"{OBJ['Plantation Drive']}",    "PLANTATION DRIVES",   164, tex.concentric(INK, 22, 4, .12)),
    ]
    NOTCH = 56
    y = 210
    for i, (c, n, lab, bh, texture) in enumerate(blocks):
        # the notch: a cream half-disc biting the slab's bottom edge, and the NEXT
        # slab carries the matching tab, so the stack visibly interlocks.
        notch_x = M + 150 + (i % 2) * 380
        P.append(f'<div style="position:absolute;left:{M}px;top:{y}px;width:{W-2*M}px;height:{bh}px;'
                 f'background-color:{c};{texture};border:4px solid {INK};'
                 f'border-radius:{core.RADII["outer"]}px;box-shadow:{core.hard_shadow("xl")};'
                 f'z-index:{6+i};overflow:hidden;display:flex;align-items:center;'
                 f'padding:0 40px;gap:34px">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:{int(bh*0.56)}px;'
                 f'line-height:1;color:{core.text_on(c)}">{n}</div>'
                 f'<div style="font-family:var(--m);font-weight:700;font-size:19px;'
                 f'letter-spacing:.12em;line-height:1.4;color:{core.text_on(c)};opacity:.92">'
                 f'{lab.replace(" ", "<br>", 1)}</div></div>')
        els.append((f"slab{i}", M, y, W - 2 * M, bh))
        if i < len(blocks) - 1:
            P.append(f'<div style="position:absolute;left:{notch_x}px;top:{y+bh-NOTCH/2}px;'
                     f'width:{NOTCH}px;height:{NOTCH}px;border-radius:50%;background:{CREAM};'
                     f'border:4px solid {INK};z-index:{6+i+20}"></div>')
        y += bh + 16

    P.append(f'<div style="position:absolute;left:{M}px;top:{y+14}px;width:{W-2*M}px;'
             f'font-family:var(--e);font-size:26px;line-height:1.4;color:{INK};opacity:.8;'
             f'z-index:10">{len(ROWS)} projects. four shapes. the proportions are the '
             f'programme, not the pitch.</div>')
    P.append(footer(CREAM, f"{PARTNERS} PARTNER ORGS"))
    return B.page(W, H, CREAM, "".join(P), grain=False), f"{OUT}/D_notched_slabs.png", els, CREAM


async def main():
    print(f"CSV {len(ROWS)} rows | {PARTNERS} partners | {VOLS:,} turnouts\n")
    async with B.session():
        for maker in (piece_a, piece_b, piece_c, piece_d):
            html, out, els, bg = await maker()
            lay.preflight(W, H, els, html=html, page_bg=bg, core=core)
            await B.render(html, out, W, H, elements=els)
            print(f"  -> {out}\n")

asyncio.run(main())
