"""AQ session 10b — motifs v2. Every fix from the v1 looking gate.

v1 -> v2:
  A  sticker labels ran out of their silhouettes (the box-units trap: label(size=13)
     inside a 206px badge renders at 27px). Now fitted via shapes.fit_font, which
     returns BOX units and reports when a label simply cannot fit — two of them
     couldn't, and are split across lines rather than shrunk to nothing.
     The swarm also sat in two tidy bands ABOVE and BELOW the headline, which is
     not the motif: the badges have to land ON the type, some in front, some behind.
     Dead bottom third.
  B  the ink slab covered two whole rows and its edges clashed with the pills it
     half-hid. The rows now run the FULL canvas (that endlessness is the motif) and
     the slab is deliberately pinned: rotated, hard-shadowed, reading as on top.
  C  "FIELD PROGRAM" clipped its burst; "AWAY." and "route." were orphans.
  D  each slab's right 55% was dead, and the notch read as a floating dot rather
     than an interlock.
"""
import asyncio, os, sys, csv, io, collections, importlib.util

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
REF = 40          # the px size every sticker label is measured at


def path_for(kind):
    return {
        "scallop": lambda: sh.scallop(lobes=13, r=45),
        "blob":    lambda: sh.blob(seed=7, lobes=8, r=44, wobble=.2),
        "burst":   lambda: sh.starburst(points=13, R=48, r=33),
        "gear":    lambda: sh.gear(teeth=11, R=46, r=36),
        "shield":  lambda: sh.shield(100, 100),
        "arch":    lambda: sh.arch(100, 100, 5),
        "capsule": lambda: sh.capsule(100, 56),
        "tag":     lambda: sh.tag(100, 54, 15),
    }.get(kind, lambda: sh.scallop(lobes=13, r=45))()


def badge(kind, fill, size, lines, widths, rot=0, shadow=True):
    """A sticker whose label is FITTED to its silhouette, never assumed.
    `widths` are the measured px widths of each line at REF px."""
    box, fits = sh.fit_font(max(widths), REF, kind, size, min_box=6.0, max_box=14.0)
    if not fits:
        print(f"    ! label {lines!r} cannot fit a {kind} at {size}px — widen or re-split")
    fg = core.text_on(fill)
    y0 = 50 - (len(lines) - 1) * (box * 0.58)
    inner = "".join(sh.label(t, size=box, y=y0 + i * box * 1.16, fill=fg, weight=800)
                    for i, t in enumerate(lines))
    return sh.sticker(path_for(kind), fill, size=size, rot=rot, inner=inner,
                      shadow=shadow, detail="none")


def place(svg, x, y, size, z=10):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;'
            f'height:{size}px;z-index:{z}">{svg}</div>')


def footer(ground, right=""):
    c = INK if ground == CREAM else CREAM
    out = (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);'
           f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{c};z-index:60">'
           f'@ngo.aquaterra</span>')
    if right:
        out += (f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);'
                f'font-weight:700;font-size:15px;color:{c};opacity:.55;z-index:60">{right}</span>')
    return out


# ════════════════════════════════════════════════════════════════════════════
# A — STICKER SWARM (badges ON the type)
# ════════════════════════════════════════════════════════════════════════════
async def piece_a():
    # every label that cannot fit on one line is split HERE, not shrunk to 5pt
    SW_ = [
        ("scallop", LEMON,  196, ["ALL", "WELFARE"],   -11, 34,  238),
        ("burst",   PINK,   196, ["291", "WORK", "SHOPS"], 9, 33, 742),
        ("capsule", MINT,   244, ["PATHER SATHI"],       7, 12,  452),
        ("gear",    GRAPE,  158, ["EK", "TARA"],       -14, 33,  892),
        ("tag",     TOMATO, 214, ["DOG FEEDS"],          6, 22,  102),
        ("blob",    SKY,    166, ["SUNDAR", "BANS"],    -7, 34,  700),
        ("arch",    LEMON,  164, ["26", "DRIVES"],      -8, 33,  876),
        ("shield",  MINT,   152, ["DISHA"],             11, 22,  330),
        ("blob",    PINK,   144, ["SINCE", "2021"],     -9, 33,   66),
        ("scallop", SKY,    150, ["KOLKATA"],            8, 22,  548),
    ]
    flat = [(i, t) for i, (_, _, _, ls, _, _, _) in enumerate(SW_) for t in ls]
    mm = await B.measure_text([{"text": t, "font": "d", "size": REF, "weight": 800}
                               for _, t in flat])
    wmap = {}
    for (i, t), r in zip(flat, mm):
        wmap.setdefault(i, []).append(r["w"])

    m = await B.measure_text([{"text": "WE JUST<br>KEEP<br>SHOWING UP.", "font": "d",
                               "size": 152, "weight": 900, "line_height": .86,
                               "max_width": W - 2 * M}])
    head_h = m[0]["h"]

    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')
    P.append(B.logo(dark=True))
    P.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{CREAM};opacity:.55;'
             f'z-index:60">{PARTNERS} PARTNER ORGS</span>')

    hy = 352
    P.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{hy}px;left:{M}px;'
             f'width:{W-2*M}px;font-family:var(--d);font-weight:900;font-size:152px;'
             f'line-height:.86;letter-spacing:-.03em;color:{CREAM};z-index:20">'
             f'WE JUST<br>KEEP<br>SHOWING UP.</div>')
    els.append(("title", M, hy, W - 2 * M, head_h))

    # y positions RELATIVE to the headline: the badges must land on it. z 12 sits
    # behind the type, z 28 in front — interleaving is what makes a pile read as
    # depth instead of a border.
    ys = [hy - 118, hy - 92, hy + 118, hy + 96, hy + 252, hy + 226,
          hy + 300, hy + 374, hy + 402, hy + 352]
    zs = [12, 28, 12, 28, 12, 28, 12, 28, 28, 12]
    for (kind, fill, size, lines, rot, _fs, x), y, z in zip(SW_, ys, zs):
        P.append(place(badge(kind, fill, size, lines, wmap[SW_.index((kind, fill, size, lines, rot, _fs, x))], rot),
                       x, y, size, z))
        els.append((f"stk{x}", *lay.rotated_bbox(x, y, size, size, rot)))

    by = hy + head_h + 66
    P.append(f'<div style="position:absolute;top:{by}px;left:{M}px;width:790px;'
             f'font-family:var(--e);font-size:29px;line-height:1.45;color:{CREAM};opacity:.74;'
             f'z-index:40">{len(ROWS)} logged welfare projects across {PARTNERS} partner '
             f'organisations. the same rooms, again and again.</div>')

    # v1's bottom third was dead. A measured strip of the real counts closes it.
    strip = [("558", "PROJECTS"), ("291", "WORKSHOPS"), ("126", "RETURNS"), (f"{PARTNERS}", "PARTNERS")]
    sy = H - 250
    cw = (W - 2 * M - 3 * 16) / 4
    for i, (n, lab) in enumerate(strip):
        x = M + i * (cw + 16)
        P.append(f'<div style="position:absolute;left:{x}px;top:{sy}px;width:{cw}px;height:120px;'
                 f'border:3px solid {CREAM};border-radius:{core.RADII["inner"]}px;z-index:40;'
                 f'overflow:hidden;display:flex;flex-direction:column;align-items:center;'
                 f'justify-content:center">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:50px;line-height:1;'
                 f'color:{CREAM}">{n}</div>'
                 f'<div style="font-family:var(--m);font-weight:700;font-size:12px;margin-top:8px;'
                 f'letter-spacing:.12em;color:{CREAM};opacity:.7">{lab}</div></div>')
        els.append((f"cell{i}", x, sy, cw, 120))

    P.append(footer(INK, f"{VOLS:,} VOLUNTEER TURNOUTS"))
    return B.page(W, H, INK, "".join(P), grain=False), f"{OUT}/A_sticker_swarm.png", els, INK


# ════════════════════════════════════════════════════════════════════════════
# B — STAGGERED BLEED ROWS (full field)
# ════════════════════════════════════════════════════════════════════════════
async def piece_b():
    titles = ["Roots in Mud", "Beyond the Stars", "Echoes of Joy", "One for All",
              "Speak Skillfully", "Life in a Bottle", "Hands at Work", "Green Hour",
              "Smiles Shared", "Heal The Earth", "Bottled Greens", "Act It Out",
              "Planet First", "Sentence Secrets", "Fun Fiesta", "Roots Rise",
              "Green Christmas", "World Health Day", "Cookie Pass On", "Mini-Fete",
              "Valentine's Cards", "Pot Painting", "Menstrual Awareness", "Gender Equality",
              "Space Education", "Public Speaking", "Earth Day", "Art Workshop"]
    FS = 33
    m = await B.measure_text([{"text": t, "font": "e", "size": FS, "weight": 600} for t in titles])
    widths = [x["w"] for x in m]

    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')
    hues = [MINT, SKY, LEMON, PINK, TOMATO, GRAPE, TEAL]
    PAD, DOT, GAP, RH, RGAP = 28, 20, 20, 74, 16
    offsets = [-150, -60, -250, -110, -310, -40, -200, -90, -180, -20, -260, -130]

    # the field runs the WHOLE canvas — that endlessness IS the motif. v1 stopped
    # two thirds down and the bottom read as an accident.
    y, idx, ri = 132, 0, 0
    while y < H - 80:
        x = offsets[ri % len(offsets)]
        while x < W + 40:
            t, tw = titles[idx % len(titles)], widths[idx % len(widths)]
            pw = PAD + DOT + 13 + tw + PAD
            c = hues[idx % len(hues)]
            P.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;width:{pw}px;height:{RH}px;'
                f'background:{PAPER};border:3px solid {INK};border-radius:999px;'
                f'box-shadow:{core.hard_shadow("base")};z-index:6;overflow:hidden;'
                f'display:flex;align-items:center;padding:0 {PAD}px;gap:13px">'
                f'<span style="flex:0 0 {DOT}px;width:{DOT}px;height:{DOT}px;border-radius:50%;'
                f'background:{c};border:2px solid {INK}"></span>'
                f'<span style="font-family:var(--e);font-weight:600;font-size:{FS}px;'
                f'color:{INK};white-space:nowrap">{t}</span></div>')
            x += pw + GAP
            idx += 1
        y += RH + RGAP
        ri += 1

    # the slab is PINNED on top: rotated, heavy shadow, cream keyline ring so it
    # reads as an object laid over the field rather than a hole punched in it.
    m2 = await B.measure_text([{"text": "TWENTY-EIGHT<br>OF THE 291.", "font": "d", "size": 104,
                                "weight": 900, "line_height": .88, "max_width": 780}])
    bw, bh = 852, m2[0]["h"] + 118
    bx, by = (W - bw) / 2, (H - bh) / 2 - 10
    P.append(f'<div style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;'
             f'background-color:{INK};border-radius:{core.RADII["outer"]}px;'
             f'transform:rotate(-2.2deg);z-index:30;overflow:hidden;padding:44px 46px;'
             f'box-shadow:{core.hard_shadow("xl")},{core.keyline(ring_bg=CREAM, gap=9, ring=3)}">'
             f'<div style="font-family:var(--d);font-weight:900;font-size:104px;line-height:.88;'
             f'letter-spacing:-.03em;color:{CREAM}">TWENTY-EIGHT<br>OF THE 291.</div>'
             f'<div style="font-family:var(--m);font-weight:700;font-size:15px;margin-top:22px;'
             f'letter-spacing:.14em;color:{LEMON}">EVERY WORKSHOP WE RAN HAS A NAME</div></div>')
    els.append(("band", *lay.rotated_bbox(bx, by, bw, bh, -2.2)))

    P.append(B.logo())
    P.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:118px;'
             f'background:linear-gradient(180deg,{CREAM} 34%,transparent);z-index:50"></div>')
    P.append(f'<div style="position:absolute;left:0;bottom:0;width:{W}px;height:132px;'
             f'background:linear-gradient(0deg,{CREAM} 46%,transparent);z-index:50"></div>')
    P.append(footer(CREAM, "WORKSHOPS 2021-2026"))
    return B.page(W, H, CREAM, "".join(P), grain=False), f"{OUT}/B_bleed_rows.png", els, CREAM


# ════════════════════════════════════════════════════════════════════════════
# C — DUOTONE PHOTO
# ════════════════════════════════════════════════════════════════════════════
async def piece_c():
    lines = ["FIELD", "PROGRAM"]
    lm = await B.measure_text([{"text": t, "font": "d", "size": REF, "weight": 800} for t in lines])
    m = await B.measure_text([{"text": "THE CLASSROOM IS<br>A BOAT RIDE AWAY.", "font": "d",
                               "size": 94, "weight": 900, "line_height": .9, "max_width": 900}])
    hh = m[0]["h"]

    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')
    PX, PY, PW, PH = M, 188, W - 2 * M, 640
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
             f'z-index:60">EDUCATION &middot; SUNDARBANS</span>')

    ssz = 196
    sx, sy = W - M - 158, PY + PH - 116
    P.append(place(badge("burst", LEMON, ssz, lines, [x["w"] for x in lm], rot=-12), sx, sy, ssz, 22))
    els.append(("stk", *lay.rotated_bbox(sx, sy, ssz, ssz, -12)))

    ty = PY + PH + 52
    P.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{ty}px;left:{M}px;'
             f'width:900px;font-family:var(--d);font-weight:900;font-size:94px;line-height:.9;'
             f'letter-spacing:-.025em;color:{INK};z-index:10">'
             f'THE CLASSROOM IS<br>A BOAT RIDE AWAY.</div>')
    els.append(("title", M, ty, 900, hh))
    P.append(f'<div style="position:absolute;top:{ty+hh+30}px;left:{M}px;width:900px;'
             f'font-family:var(--e);font-size:27px;line-height:1.45;color:{INK};opacity:.78;'
             f'z-index:10">ten sundarbans relief runs logged. the delta has no bus route.</div>')
    P.append(footer(CREAM, "SUNDARBANS RELIEF \u00b7 10 RUNS"))
    return B.page(W, H, CREAM, "".join(P), grain=False), f"{OUT}/C_duotone_photo.png", els, CREAM


# ════════════════════════════════════════════════════════════════════════════
# D — NOTCHED SLABS
# ════════════════════════════════════════════════════════════════════════════
async def piece_d():
    els, P = [], []
    P.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')
    P.append(B.logo())
    P.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
             f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{INK};opacity:.5;'
             f'z-index:60">THE SHAPE OF THE WORK</span>')

    total = sum(OBJ[k] for k in ("Workshop", "Distribution Drive", "Feeding Dogs", "Plantation Drive"))
    blocks = [
        (MINT,   OBJ["Workshop"],           "CLASSROOM<br>WORKSHOPS", tex.crosshatch(INK, 14, 2, .13)),
        (SKY,    OBJ["Distribution Drive"], "DISTRIBUTION<br>DRIVES", tex.stripes(INK, None, 3, 22, -40, .14)),
        (LEMON,  OBJ["Feeding Dogs"],       "DOG FEEDING<br>RUNS",    tex.dot_grid(INK, 20, 3, .16)),
        (TOMATO, OBJ["Plantation Drive"],   "PLANTATION<br>DRIVES",   tex.grid_lines(INK, 34, 2, .13)),
    ]
    NOTCH = 64
    y = 206
    for i, (c, n, lab, texture) in enumerate(blocks):
        bh = int(150 + 150 * (n / blocks[0][1]) ** 0.55)
        fg = core.text_on(c)
        # v1 left the right 55% of every slab empty. A right-aligned share bar,
        # drawn from the same count, fills it with information rather than filler.
        share = n / total
        P.append(f'<div style="position:absolute;left:{M}px;top:{y}px;width:{W-2*M}px;height:{bh}px;'
                 f'background-color:{c};{texture};border:4px solid {INK};'
                 f'border-radius:{core.RADII["outer"]}px;box-shadow:{core.hard_shadow("xl")};'
                 f'z-index:{6+i};overflow:hidden;display:flex;align-items:center;'
                 f'padding:0 38px;gap:30px">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:{int(bh*0.52)}px;'
                 f'line-height:1;color:{fg}">{n}</div>'
                 f'<div style="flex:1;font-family:var(--m);font-weight:700;font-size:18px;'
                 f'letter-spacing:.12em;line-height:1.45;color:{fg};opacity:.92">{lab}</div>'
                 f'<div style="flex:0 0 210px;text-align:right">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:42px;line-height:1;'
                 f'color:{fg}">{share*100:.0f}%</div>'
                 f'<div style="height:12px;margin-top:10px;border:2px solid {fg};border-radius:999px;'
                 f'overflow:hidden"><div style="width:{share*100:.0f}%;height:100%;'
                 f'background:{fg}"></div></div>'
                 f'<div style="font-family:var(--m);font-weight:700;font-size:11px;margin-top:8px;'
                 f'letter-spacing:.14em;color:{fg};opacity:.8">OF ALL LOGGED WORK</div>'
                 f'</div></div>')
        els.append((f"slab{i}", M, y, W - 2 * M, bh))
        if i < len(blocks) - 1:
            # a real interlock: the tab belongs to the slab ABOVE and bites into the
            # one below, so the two visibly key together instead of a dot floating
            # on the seam.
            nx = M + 140 + (i % 2) * 420
            P.append(f'<div style="position:absolute;left:{nx}px;top:{y+bh-NOTCH/2+2}px;'
                     f'width:{NOTCH}px;height:{NOTCH}px;border-radius:50%;background-color:{c};'
                     f'{texture};border:4px solid {INK};z-index:{6+i};'
                     f'box-shadow:0 5px 0 -1px rgba(10,10,10,.25)"></div>')
        y += bh + 14

    P.append(f'<div style="position:absolute;left:{M}px;top:{y+18}px;width:{W-2*M}px;'
             f'font-family:var(--e);font-size:26px;line-height:1.45;color:{INK};opacity:.8;'
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
