"""AQ session 10 — real posts from welfare_projects_rows.csv, batch v1.

Every number here is COUNTED off the CSV (VOICE.md truth ladder), with its
qualifier attached. Nothing is estimated and nothing is invented.

Exercises the session-10 engine work end to end:
  core.accent_for()  — welfare is mint BY RULE, not by rotation index
  core.text_on()     — measured, so accents carry ink not the old failing white
  core.on_cream()    — accents shout at display size, whisper as the dark partner
  core.keyline()     — the site's stuck-on sticker double-ring
  tex.*              — texture INSIDE slabs, at full contrast
  B.session()        — one browser for the whole batch
"""
import asyncio, os, sys, csv, re, io, collections, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = load("core"); B = load("build"); dd = load("doodles")
lay = load("layout"); tex = load("tex"); sh = load("shapes")

CSV = r"C:\Users\kanis\Downloads\welfare_projects_rows.csv"
ROWS = list(csv.DictReader(io.open(CSV, encoding="utf-8")))
OBJ = collections.Counter(r["objective"] for r in ROWS)
LOC = collections.Counter(r["location"].strip() for r in ROWS if r["location"].strip())
YRS = sorted({(r["workshop_date"] or "")[:4] for r in ROWS if (r["workshop_date"] or "")[:4].isdigit()})
PATHER = LOC["Pather Sathi"] + LOC["Pather Saathi"]          # same partner, two spellings
VOLS = sum(int(r["volunteers"]) for r in ROWS if (r["volunteers"] or "").strip().isdigit())

INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
MINT = core.accent_for("welfare")           # #1B8A5A — by rule
LEMON, PINK, SKY, TOMATO = core.ACCENTS[2], core.ACCENTS[0], core.ACCENTS[4], core.ACCENTS[3]
OUT = "out/session10"
os.makedirs(OUT, exist_ok=True)

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

def keyline_sticker(x, y, d, fill, label, rot=0, z=14, fs=17, ground=CREAM):
    """A round keyline sticker: paper ring then ink ring, so it reads STUCK ON.
    Text colour is measured off its own fill, never assumed."""
    fg = core.text_on(fill)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
            f'border-radius:50%;background:{fill};transform:rotate({rot}deg);z-index:{z};'
            f'box-shadow:{core.keyline(ring_bg=ground)};display:flex;align-items:center;'
            f'justify-content:center;text-align:center;padding:10px">'
            f'<span style="font-family:var(--m);font-weight:700;font-size:{fs}px;line-height:1.05;'
            f'letter-spacing:.02em;color:{fg};text-transform:uppercase">{label}</span></div>')

def footer(ground=CREAM, y=None, W=1080, H=1350):
    c = INK if ground == CREAM else PAPER
    return (f'<span style="position:absolute;bottom:{y or 54}px;left:64px;font-family:var(--m);'
            f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{c};z-index:20">'
            f'@ngo.aquaterra</span>')

# ════════════════════════════════════════════════════════════════════════════
# PIECE 1 — "119": the number that means we kept coming back
# ════════════════════════════════════════════════════════════════════════════
def piece_one():
    W, H = core.SIZES["feed"]; M = 64
    els = []
    parts = [f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>']

    parts.append(B.logo())
    parts.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{core.on_cream(MINT, 15)};'
                 f'z-index:20">WELFARE</span>')

    # eyebrow
    parts.append(f'<div class="measure" data-tag="eyebrow" style="position:absolute;top:172px;left:{M}px;'
                 f'font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.16em;'
                 f'color:{INK};z-index:6">ONE PARTNER &nbsp;/&nbsp; {YRS[0]}&ndash;{YRS[-1]}</div>')
    els.append(("eyebrow", M, 172, 560, 26))

    # THE HERO — mint at display size clears the large-text floor, so it keeps the dept hue
    parts.append(f'<div style="position:absolute;top:210px;left:{M-14}px;font-family:var(--d);'
                 f'font-weight:900;font-size:470px;line-height:.78;letter-spacing:-.045em;'
                 f'color:{core.on_cream(MINT, 470)};z-index:5">{PATHER}</div>')
    els.append(("hero", M - 14, 230, 700, 360))

    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:600px;left:{M}px;'
                 f'width:760px;font-family:var(--d);font-weight:900;font-size:96px;line-height:.92;'
                 f'letter-spacing:-.02em;color:{INK};z-index:6">TIMES WE<br>CAME BACK.</div>')
    els.append(("title", M, 600, 760, 185))

    # the mint slab, textured INSIDE its own edge — never a wash on the page
    sy = 812
    parts.append(f'<div style="position:absolute;left:{M}px;top:{sy}px;width:{W-2*M}px;height:150px;'
                 f'background-color:{MINT};{tex.crosshatch(color=INK, step=13, width=2, opacity=0.14)};'
                 f'border:4px solid {INK};border-radius:{core.RADII["outer"]}px;'
                 f'box-shadow:{core.hard_shadow("xl")};z-index:8"></div>')
    els.append(("slab", M, sy, W - 2 * M, 150))
    parts.append(f'<div style="position:absolute;left:{M+34}px;top:{sy+30}px;width:{W-2*M-68}px;'
                 f'font-family:var(--d);font-weight:900;font-size:60px;line-height:1;'
                 f'color:{core.text_on(MINT)};z-index:9">PATHER SATHI</div>')
    parts.append(f'<div style="position:absolute;left:{M+36}px;top:{sy+100}px;font-family:var(--e);'
                 f'font-size:25px;color:{core.text_on(MINT)};opacity:.92;z-index:9">'
                 f'kolkata &middot; every visit logged</div>')

    # the breakdown — real counts, each with its qualifier
    row = [("WORKSHOPS", OBJ["Workshop"]), ("DRIVES", OBJ["Distribution Drive"]),
           ("DOG FEEDS", OBJ["Feeding Dogs"]), ("PLANTATIONS", OBJ["Plantation Drive"])]
    bx, by, bw = M, 1010, (W - 2 * M - 3 * 14) / 4
    for i, (lab, n) in enumerate(row):
        x = bx + i * (bw + 14)
        parts.append(f'<div style="position:absolute;left:{x}px;top:{by}px;width:{bw}px;height:132px;'
                     f'background:{PAPER};border:3px solid {INK};border-radius:{core.RADII["inner"]}px;'
                     f'box-shadow:{core.hard_shadow("lg")};z-index:8"></div>')
        parts.append(f'<div style="position:absolute;left:{x}px;top:{by+18}px;width:{bw}px;'
                     f'text-align:center;font-family:var(--d);font-weight:900;font-size:60px;'
                     f'color:{INK};z-index:9">{n}</div>')
        parts.append(f'<div style="position:absolute;left:{x}px;top:{by+92}px;width:{bw}px;'
                     f'text-align:center;font-family:var(--m);font-weight:700;font-size:13px;'
                     f'letter-spacing:.09em;color:{core.on_cream(MINT, 13)};z-index:9">{lab}</div>')
        els.append((f"cell{i}", x, by, bw, 132))

    # sticker swarm, keyline-ringed so they read as stuck onto the paper
    parts.append(keyline_sticker(762, 236, 176, LEMON, "ALL<br>WELFARE", rot=-9))
    els.append(("stk1", 762, 236, 176, 176))
    parts.append(keyline_sticker(838, 430, 146, PINK, f"{OBJ['Workshop']}<br>WORK&shy;SHOPS", rot=7, fs=15))
    els.append(("stk2", 838, 430, 146, 146))
    parts.append(doodle("sparkle", 700, 596, 92, TOMATO, rot=-14, z=13))
    els.append(("dd1", 700, 596, 92, 92))
    parts.append(tex.tape(636, 176, 132, 40, rot=-7, z=30))

    parts.append(footer())
    parts.append(f'<span style="position:absolute;bottom:54px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{INK};opacity:.55;z-index:20">'
                 f'{len(ROWS)} LOGGED PROJECTS</span>')

    html = B.page(W, H, CREAM, "".join(parts), grain=False)
    return html, f"{OUT}/01_pather_sathi.png", W, H, els


# ════════════════════════════════════════════════════════════════════════════
# PIECE 2 — the ledger: 558 projects, typed
# ════════════════════════════════════════════════════════════════════════════
def piece_two():
    W, H = core.SIZES["feed"]; M = 64
    els = []
    parts = [f'<div style="position:absolute;inset:0;background:{INK}"></div>']
    # on an ink field the craft outline must FLIP to cream or it deletes itself
    OL = core.outline_of(INK)

    parts.append(B.logo(dark=True))
    parts.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{CREAM};opacity:.6;'
                 f'z-index:20">THE LEDGER</span>')

    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:168px;left:{M}px;'
                 f'width:900px;font-family:var(--d);font-weight:900;font-size:128px;line-height:.86;'
                 f'letter-spacing:-.03em;color:{CREAM};z-index:6">EVERY<br>SINGLE<br>ONE.</div>')
    els.append(("title", M, 168, 900, 340))

    parts.append(f'<div style="position:absolute;top:524px;left:{M}px;width:820px;font-family:var(--e);'
                 f'font-size:27px;line-height:1.45;color:{CREAM};opacity:.78;z-index:6">'
                 f'{len(ROWS)} welfare projects, logged one at a time between '
                 f'{YRS[0]} and {YRS[-1]}. no rounding up.</div>')
    els.append(("body", M, 524, 820, 92))

    # the ledger rows — a real bar chart off real counts
    order = OBJ.most_common(6)
    top = order[0][1]
    hues = [MINT, SKY, LEMON, PINK, TOMATO, core.ACCENTS[5]]
    ry, rh, gap = 660, 74, 14
    for i, (lab, n) in enumerate(order):
        y = ry + i * (rh + gap)
        wfull = W - 2 * M - 210
        bw = max(120, int(wfull * n / top))
        c = hues[i % len(hues)]
        parts.append(f'<div style="position:absolute;left:{M}px;top:{y}px;width:{bw}px;height:{rh}px;'
                     f'background-color:{c};border:3px solid {OL};border-radius:{core.RADII["pill"]}px;'
                     f'box-shadow:{core.hard_shadow("lg", OL)};z-index:8"></div>')
        parts.append(f'<div style="position:absolute;left:{M+26}px;top:{y+22}px;font-family:var(--m);'
                     f'font-weight:700;font-size:20px;letter-spacing:.06em;color:{core.text_on(c)};'
                     f'z-index:9;text-transform:uppercase">{lab}</div>')
        parts.append(f'<div style="position:absolute;left:{M+bw+22}px;top:{y+14}px;font-family:var(--d);'
                     f'font-weight:900;font-size:46px;color:{CREAM};z-index:9">{n}</div>')
        els.append((f"bar{i}", M, y, bw + 120, rh))

    parts.append(footer(ground=INK))
    parts.append(f'<span style="position:absolute;bottom:54px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{CREAM};opacity:.55;z-index:20">'
                 f'{VOLS:,} VOLUNTEER TURNOUTS</span>')

    html = B.page(W, H, INK, "".join(parts), grain=False)
    return html, f"{OUT}/02_ledger.png", W, H, els


# ════════════════════════════════════════════════════════════════════════════
# PIECE 3 — LinkedIn square: the same truth, institutional register
# ════════════════════════════════════════════════════════════════════════════
def piece_three():
    W, H = core.SIZES["li_square"]; M = 78
    els = []
    parts = [f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.045)}"></div>']

    # a mint field across the top third, textured inside its own edge
    parts.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:392px;'
                 f'background-color:{MINT};{tex.stripes(color=INK, width=3, gap=26, angle=-40, opacity=0.13)};'
                 f'border-bottom:5px solid {INK};z-index:2"></div>')

    parts.append(B.logo(dark=True, x=M, y=62))
    parts.append(f'<span style="position:absolute;top:70px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:16px;letter-spacing:.14em;color:{core.text_on(MINT)};'
                 f'opacity:.8;z-index:20">AQUATERRA &middot; WELFARE</span>')

    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:168px;left:{M}px;'
                 f'width:{W-2*M}px;font-family:var(--d);font-weight:900;font-size:104px;line-height:.9;'
                 f'letter-spacing:-.025em;color:{core.text_on(MINT)};z-index:6">'
                 f'CONSISTENCY IS<br>THE WHOLE PROGRAM.</div>')
    els.append(("title", M, 168, W - 2 * M, 200))

    parts.append(f'<div style="position:absolute;top:452px;left:{M}px;width:{W-2*M-40}px;'
                 f'font-family:var(--e);font-size:31px;line-height:1.5;color:{INK};z-index:6">'
                 f'Between {YRS[0]} and {YRS[-1]} we logged <b>{len(ROWS)} welfare projects</b> &mdash; '
                 f'{OBJ["Workshop"]} of them classroom workshops, and {PATHER} of them return visits '
                 f'to a single partner in Kolkata. The number that matters is not how many '
                 f'children we met once. It is how many times we went back.</div>')
    els.append(("body", M, 452, W - 2 * M - 40, 230))

    stats = [(f"{len(ROWS)}", "PROJECTS LOGGED"), (f"{VOLS:,}", "VOLUNTEER TURNOUTS"),
             (f"{PATHER}", "RETURNS, ONE PARTNER")]
    cy, cw = 748, (W - 2 * M - 2 * 20) / 3
    for i, (n, lab) in enumerate(stats):
        x = M + i * (cw + 20)
        parts.append(f'<div style="position:absolute;left:{x}px;top:{cy}px;width:{cw}px;height:212px;'
                     f'background:{PAPER};border:4px solid {INK};border-radius:{core.RADII["outer"]}px;'
                     f'box-shadow:{core.hard_shadow("xl")};z-index:8"></div>')
        parts.append(f'<div style="position:absolute;left:{x}px;top:{cy+34}px;width:{cw}px;'
                     f'text-align:center;font-family:var(--d);font-weight:900;font-size:86px;'
                     f'line-height:1;color:{core.on_cream(MINT, 86)};z-index:9">{n}</div>')
        parts.append(f'<div style="position:absolute;left:{x+16}px;top:{cy+142}px;width:{cw-32}px;'
                     f'text-align:center;font-family:var(--m);font-weight:700;font-size:15px;'
                     f'letter-spacing:.08em;line-height:1.3;color:{INK};z-index:9">{lab}</div>')
        els.append((f"stat{i}", x, cy, cw, 212))

    parts.append(f'<span style="position:absolute;bottom:58px;left:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:17px;letter-spacing:.06em;color:{INK};z-index:20">'
                 f'ngoaquaterra.com</span>')
    parts.append(f'<span style="position:absolute;bottom:58px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{INK};opacity:.55;z-index:20">'
                 f'SOURCE: AQ WELFARE PROJECT LOG</span>')

    html = B.page(W, H, CREAM, "".join(parts), grain=False)
    return html, f"{OUT}/03_linkedin.png", W, H, els


async def main():
    print(f"CSV: {len(ROWS)} rows | Pather Sathi {PATHER} | workshops {OBJ['Workshop']} | "
          f"volunteer turnouts {VOLS} | years {YRS[0]}-{YRS[-1]}\n")
    jobs = [piece_one(), piece_two(), piece_three()]
    for html, out, W, H, els in jobs:
        pf = lay.preflight(W, H, els, html=html, page_bg=CREAM if "02_" not in out else INK,
                           core=core)
    async with B.session():
        for html, out, W, H, els in jobs:
            await B.render(html, out, W, H)
            print(f"  -> {out}")

asyncio.run(main())
