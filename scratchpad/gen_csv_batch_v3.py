"""AQ session 10 — batch v2. Every fix from the v1 looking gate, plus the rule
that made them fixable: MEASURE THE TEXT FIRST, then size the shape to it.

v1 → v2, by piece:
  01  the 470px hero measured 484px tall in a 367px line box, so the declared
      bbox under-reported by 117px and the collision check cleared a sticker
      onto the numeral. Stickers now placed against the MEASURED extent.
      The tomato sparkle sat on the headline (static gate caught it). The tape
      was cream-on-cream and read as a smudge, not an object. Dead bottom band.
  02  pill labels were sized from text while pills were sized from data, so
      "PLANTATION DRIVE" rendered as "PLANTAT". Labels now live in a fixed
      gutter column; bars can be any length without ever eating their label.
      The whole right half was dead.
  03  a 3-line headline measured 281px tall but was positioned in a 392px band
      starting at y=168, so it crossed the band edge into the body copy. The
      band is now sized FROM the measured headline. Dead bottom band.
"""
import asyncio, os, sys, csv, io, collections, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

core = load("core"); B = load("build"); dd = load("doodles")
lay = load("layout"); tex = load("tex")

CSV = r"C:\Users\kanis\Downloads\welfare_projects_rows.csv"
ROWS = list(csv.DictReader(io.open(CSV, encoding="utf-8")))
OBJ = collections.Counter(r["objective"] for r in ROWS)
LOC = collections.Counter(r["location"].strip() for r in ROWS if r["location"].strip())
YRS = sorted({(r["workshop_date"] or "")[:4] for r in ROWS if (r["workshop_date"] or "")[:4].isdigit()})
PATHER = LOC["Pather Sathi"] + LOC["Pather Saathi"]
VOLS = sum(int(r["volunteers"]) for r in ROWS if (r["volunteers"] or "").strip().isdigit())

INK, CREAM, PAPER = core.INK, core.CREAM, core.PAPER
MINT = core.accent_for("welfare")
PINK, LEMON, TOMATO, SKY, GRAPE = (core.ACCENTS[0], core.ACCENTS[2],
                                   core.ACCENTS[3], core.ACCENTS[4], core.ACCENTS[5])
OUT = "out/session10"
os.makedirs(OUT, exist_ok=True)

def doodle(kind, x, y, size, fill, rot=0, z=7, style="clean"):
    return (f'<div style="position:absolute;top:{y}px;left:{x}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp(kind, fill, rot=rot, style=style)}</div>')

def keyline_sticker(x, y, d, fill, label, rot=0, z=14, fs=17, ground=CREAM):
    fg = core.text_on(fill)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{d}px;height:{d}px;'
            f'border-radius:50%;background:{fill};transform:rotate({rot}deg);z-index:{z};'
            f'box-shadow:{core.keyline(ring_bg=ground)};display:flex;align-items:center;'
            f'justify-content:center;text-align:center;padding:12px;overflow:hidden">'
            f'<span style="font-family:var(--m);font-weight:700;font-size:{fs}px;line-height:1.08;'
            f'letter-spacing:.02em;color:{fg};text-transform:uppercase">{label}</span></div>')


async def piece_one():
    """126 — the number that means we kept coming back."""
    W, H = core.SIZES["feed"]; M = 64
    HERO_FS = 430
    m = await B.measure_text([
        {"text": str(PATHER), "font": "d", "size": HERO_FS, "weight": 900,
         "line_height": 0.78, "letter_spacing": "-.045em"},
        {"text": "TIMES WE<br>CAME BACK.", "font": "d", "size": 92, "weight": 900,
         "line_height": 0.92, "max_width": 780},
        {"text": "CAME BACK.", "font": "d", "size": 92, "weight": 900},  # true widest line
    ])
    # h = layout box (flow the next element off it); ink_h = what the glyphs
    # actually paint (size the collision bbox off THAT). v2 used h for both and
    # the sticker landed 50px into the headline.
    hero_w, hero_h, hero_ink = m[0]["w"], m[0]["h"], m[0]["ink_h"]
    title_h, title_ink = m[1]["h"], m[1]["ink_h"]
    title_w = m[2]["w"]                             # the real text width, not max_width

    els, parts = [], []
    parts.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.05)}"></div>')
    parts.append(B.logo())
    parts.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{core.on_cream(MINT,15)};'
                 f'z-index:20">WELFARE</span>')

    ey = 168
    parts.append(f'<div class="measure" data-tag="eyebrow" style="position:absolute;top:{ey}px;left:{M}px;'
                 f'font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.16em;'
                 f'color:{INK};z-index:6">ONE PARTNER &nbsp;/&nbsp; {YRS[0]}&ndash;{YRS[-1]}</div>')
    els.append(("eyebrow", M, ey, 560, 26))

    hero_y = 208
    parts.append(f'<div style="position:absolute;top:{hero_y}px;left:{M-12}px;font-family:var(--d);'
                 f'font-weight:900;font-size:{HERO_FS}px;line-height:.78;letter-spacing:-.045em;'
                 f'color:{core.on_cream(MINT, HERO_FS)};z-index:5">{PATHER}</div>')
    els.append(("hero", M - 12, hero_y, hero_w, hero_ink))   # PAINTED extent

    ty = hero_y + hero_ink + 10                     # clear the glyphs, not the line box
    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{ty}px;left:{M}px;'
                 f'width:780px;font-family:var(--d);font-weight:900;font-size:92px;line-height:.92;'
                 f'letter-spacing:-.02em;color:{INK};z-index:6">TIMES WE<br>CAME BACK.</div>')
    els.append(("title", M, ty, title_w, title_ink))

    # stickers go where the MEASURED hero is not. hero right edge + a real gap.
    sx = M - 12 + hero_w + 26
    parts.append(keyline_sticker(sx, hero_y + 44, 168, LEMON, "ALL<br>WELFARE", rot=-9))
    els.append(("stk1", sx, hero_y + 44, 168, 168))
    parts.append(keyline_sticker(sx + 6, hero_y + 240, 150, PINK,
                                 f"{OBJ['Workshop']}<br>WORK&shy;SHOPS", rot=7, fs=15))
    els.append(("stk2", sx + 6, hero_y + 240, 150, 150))
    # the sparkle sat ON the headline in v1; park it beside the headline instead
    parts.append(doodle("sparkle", M + title_w + 34, ty + 30, 96, TOMATO, rot=-14, z=13))
    els.append(("dd1", M + title_w + 34, ty + 30, 96, 96))
    # tape was cream on cream — an object you cannot see is not craft
    parts.append(tex.tape(sx + 128, hero_y + 8, 128, 40, rot=-7, z=30, color="#E4D7A8"))

    sy = ty + title_ink + 26
    parts.append(f'<div style="position:absolute;left:{M}px;top:{sy}px;width:{W-2*M}px;height:176px;'
                 f'background-color:{MINT};{tex.crosshatch(color=INK, step=13, width=2, opacity=0.14)};'
                 f'border:4px solid {INK};border-radius:{core.RADII["outer"]}px;'
                 f'box-shadow:{core.hard_shadow("xl")};z-index:8;overflow:hidden">'
                 f'<div style="padding:26px 34px">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:60px;line-height:1;'
                 f'color:{core.text_on(MINT)}">PATHER SATHI</div>'
                 f'<div style="font-family:var(--e);font-size:25px;margin-top:8px;'
                 f'color:{core.text_on(MINT)};opacity:.92">kolkata &middot; every visit logged</div>'
                 f'</div></div>')
    els.append(("slab", M, sy, W - 2 * M, 176))

    row = [("WORKSHOPS", OBJ["Workshop"]), ("DRIVES", OBJ["Distribution Drive"]),
           ("DOG FEEDS", OBJ["Feeding Dogs"]), ("PLANTATIONS", OBJ["Plantation Drive"])]
    by = sy + 176 + 22
    bw = (W - 2 * M - 3 * 14) / 4
    ch = H - 118 - by                                    # fill to the footer: no dead band
    for i, (lab, n) in enumerate(row):
        x = M + i * (bw + 14)
        parts.append(f'<div style="position:absolute;left:{x}px;top:{by}px;width:{bw}px;height:{ch}px;'
                     f'background:{PAPER};border:3px solid {INK};border-radius:{core.RADII["inner"]}px;'
                     f'box-shadow:{core.hard_shadow("lg")};z-index:8;overflow:hidden;'
                     f'display:flex;flex-direction:column;align-items:center;justify-content:center">'
                     f'<div style="font-family:var(--d);font-weight:900;font-size:62px;line-height:1;'
                     f'color:{INK}">{n}</div>'
                     f'<div style="font-family:var(--m);font-weight:700;font-size:13px;margin-top:10px;'
                     f'letter-spacing:.09em;color:{core.on_cream(MINT,13)};text-align:center">{lab}</div>'
                     f'</div>')
        els.append((f"cell{i}", x, by, bw, ch))

    parts.append(f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{INK};z-index:20">'
                 f'@ngo.aquaterra</span>')
    parts.append(f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{INK};opacity:.55;z-index:20">'
                 f'{len(ROWS)} LOGGED PROJECTS</span>')

    return B.page(W, H, CREAM, "".join(parts), grain=False), f"{OUT}/01_pather_sathi.png", W, H, els, CREAM


async def piece_two():
    """The ledger. Labels live in their own gutter, so a short bar can never eat one."""
    W, H = core.SIZES["feed"]; M = 64
    order = OBJ.most_common(6)
    labels = [k.upper() for k, _ in order]
    m = await B.measure_text(
        [{"text": l, "font": "m", "size": 19, "weight": 700, "letter_spacing": ".05em"} for l in labels]
        + [{"text": "EVERY<br>SINGLE<br>ONE.", "font": "d", "size": 124, "weight": 900,
            "line_height": 0.86, "max_width": 660}])
    GUT = max(x["w"] for x in m[:-1]) + 26        # the label column, sized to the LONGEST label
    title_h = m[-1]["h"]

    OL = core.outline_of(INK)                     # cream, or the craft layer deletes itself
    els, parts = [], []
    parts.append(f'<div style="position:absolute;inset:0;background:{INK}"></div>')
    parts.append(B.logo(dark=True))
    parts.append(f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.14em;color:{CREAM};opacity:.6;'
                 f'z-index:20">THE LEDGER</span>')

    ty = 160
    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{ty}px;left:{M}px;'
                 f'width:660px;font-family:var(--d);font-weight:900;font-size:124px;line-height:.86;'
                 f'letter-spacing:-.03em;color:{CREAM};z-index:6">EVERY<br>SINGLE<br>ONE.</div>')
    els.append(("title", M, ty, 660, title_h))

    # v1 left the whole right half dead. A big outlined numeral anchors it.
    parts.append(f'<div style="position:absolute;top:{ty+8}px;right:{M}px;font-family:var(--d);'
                 f'font-weight:900;font-size:196px;line-height:.82;letter-spacing:-.04em;'
                 f'color:transparent;-webkit-text-stroke:3px {MINT};z-index:5">{len(ROWS)}</div>')
    parts.append(f'<div style="position:absolute;top:{ty+184}px;right:{M+6}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;letter-spacing:.16em;color:{MINT};z-index:6">'
                 f'PROJECTS</div>')

    by = ty + title_h + 40
    parts.append(f'<div style="position:absolute;top:{by}px;left:{M}px;width:840px;font-family:var(--e);'
                 f'font-size:26px;line-height:1.45;color:{CREAM};opacity:.78;z-index:6">'
                 f'logged one at a time between {YRS[0]} and {YRS[-1]}. no rounding up.</div>')
    els.append(("body", M, by, 840, 42))

    top = order[0][1]
    hues = [MINT, SKY, LEMON, PINK, TOMATO, GRAPE]
    ry, rh, gap = by + 84, 78, 16
    track = W - M - (M + GUT) - 96                 # room left for the count at the end
    for i, (lab, n) in enumerate(order):
        y = ry + i * (rh + gap)
        bx = M + GUT
        bw = max(58, int(track * n / top))
        c = hues[i % len(hues)]
        parts.append(f'<div style="position:absolute;left:{M}px;top:{y+rh/2-11}px;width:{GUT-20}px;'
                     f'font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.05em;'
                     f'color:{CREAM};opacity:.9;z-index:9;white-space:nowrap">{lab.upper()}</div>')
        parts.append(f'<div style="position:absolute;left:{bx}px;top:{y}px;width:{bw}px;height:{rh}px;'
                     f'background-color:{c};border:3px solid {OL};border-radius:{core.RADII["pill"]}px;'
                     f'box-shadow:{core.hard_shadow("lg", OL)};z-index:8"></div>')
        parts.append(f'<div style="position:absolute;left:{bx+bw+20}px;top:{y+14}px;font-family:var(--d);'
                     f'font-weight:900;font-size:46px;line-height:1;color:{CREAM};z-index:9">{n}</div>')
        els.append((f"bar{i}", M, y, GUT + bw + 100, rh))

    parts.append(f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:16px;letter-spacing:.06em;color:{CREAM};z-index:20">'
                 f'@ngo.aquaterra</span>')
    parts.append(f'<span style="position:absolute;bottom:52px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{CREAM};opacity:.55;z-index:20">'
                 f'{VOLS:,} VOLUNTEER TURNOUTS</span>')

    return B.page(W, H, INK, "".join(parts), grain=False), f"{OUT}/02_ledger.png", W, H, els, INK


async def piece_three():
    """LinkedIn square. The band is sized FROM the headline, not guessed around it."""
    W, H = core.SIZES["li_square"]; M = 78
    HFS, TOP = 96, 158
    m = await B.measure_text([
        {"text": "CONSISTENCY IS<br>THE WHOLE PROGRAM.", "font": "d", "size": HFS,
         "weight": 900, "line_height": 0.92, "max_width": W - 2 * M},
        {"text": (f"Between {YRS[0]} and {YRS[-1]} we logged {len(ROWS)} welfare projects "
                  f"&mdash; {OBJ['Workshop']} classroom workshops, and {PATHER} return visits "
                  f"to one partner in Kolkata."), "font": "e", "size": 30, "weight": 400,
         "line_height": 1.5, "max_width": W - 2 * M - 40},
    ])
    head_h, body_h = m[0]["h"], m[1]["h"]
    BAND = TOP + head_h + 46                       # the band CONTAINS the headline, by construction

    els, parts = [], []
    parts.append(f'<div style="position:absolute;inset:0;background:{CREAM};{tex.paper_fibre(0.045)}"></div>')
    parts.append(f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{BAND}px;'
                 f'background-color:{MINT};{tex.stripes(color=INK, width=3, gap=26, angle=-40, opacity=0.13)};'
                 f'border-bottom:5px solid {INK};z-index:2"></div>')
    parts.append(B.logo(dark=True, x=M, y=62))
    parts.append(f'<span style="position:absolute;top:70px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:16px;letter-spacing:.14em;color:{core.text_on(MINT)};'
                 f'opacity:.8;z-index:20">AQUATERRA &middot; WELFARE</span>')
    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;top:{TOP}px;left:{M}px;'
                 f'width:{W-2*M}px;font-family:var(--d);font-weight:900;font-size:{HFS}px;'
                 f'line-height:.92;letter-spacing:-.025em;color:{core.text_on(MINT)};z-index:6">'
                 f'CONSISTENCY IS<br>THE WHOLE PROGRAM.</div>')
    els.append(("title", M, TOP, W - 2 * M, head_h))

    byy = BAND + 44
    parts.append(f'<div style="position:absolute;top:{byy}px;left:{M}px;width:{W-2*M-40}px;'
                 f'font-family:var(--e);font-size:30px;line-height:1.5;color:{INK};z-index:6">'
                 f'Between {YRS[0]} and {YRS[-1]} we logged <b>{len(ROWS)} welfare projects</b> &mdash; '
                 f'{OBJ["Workshop"]} classroom workshops, and {PATHER} return visits to one partner '
                 f'in Kolkata.</div>')
    els.append(("body", M, byy, W - 2 * M - 40, body_h))

    kick = byy + body_h + 26
    parts.append(f'<div style="position:absolute;top:{kick}px;left:{M}px;width:{W-2*M}px;'
                 f'font-family:var(--s);font-style:italic;font-size:44px;color:{core.on_cream(MINT,44)};'
                 f'z-index:6">The number that matters is how many times we went back.</div>')
    els.append(("kicker", M, kick, W - 2 * M, 56))

    stats = [(f"{len(ROWS)}", "PROJECTS LOGGED"), (f"{VOLS:,}", "VOLUNTEER TURNOUTS"),
             (f"{PATHER}", "RETURNS, ONE PARTNER")]
    cy = kick + 104
    ch = H - 118 - cy                              # fill to the footer: no dead band
    cw = (W - 2 * M - 2 * 20) / 3
    for i, (n, lab) in enumerate(stats):
        x = M + i * (cw + 20)
        parts.append(f'<div style="position:absolute;left:{x}px;top:{cy}px;width:{cw}px;height:{ch}px;'
                     f'background:{PAPER};border:4px solid {INK};border-radius:{core.RADII["outer"]}px;'
                     f'box-shadow:{core.hard_shadow("xl")};z-index:8;overflow:hidden;display:flex;'
                     f'flex-direction:column;align-items:center;justify-content:center;padding:14px">'
                     f'<div style="font-family:var(--d);font-weight:900;font-size:90px;line-height:1;'
                     f'color:{core.on_cream(MINT,90)}">{n}</div>'
                     f'<div style="font-family:var(--m);font-weight:700;font-size:15px;margin-top:14px;'
                     f'letter-spacing:.08em;line-height:1.3;text-align:center;color:{INK}">{lab}</div>'
                     f'</div>')
        els.append((f"stat{i}", x, cy, cw, ch))

    parts.append(f'<span style="position:absolute;bottom:56px;left:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:17px;letter-spacing:.06em;color:{INK};z-index:20">'
                 f'ngoaquaterra.com</span>')
    parts.append(f'<span style="position:absolute;bottom:56px;right:{M}px;font-family:var(--m);'
                 f'font-weight:700;font-size:15px;color:{INK};opacity:.55;z-index:20">'
                 f'SOURCE: AQ WELFARE PROJECT LOG</span>')

    return B.page(W, H, CREAM, "".join(parts), grain=False), f"{OUT}/03_linkedin.png", W, H, els, CREAM


async def main():
    print(f"CSV {len(ROWS)} rows | Pather Sathi {PATHER} | workshops {OBJ['Workshop']} | "
          f"turnouts {VOLS} | {YRS[0]}-{YRS[-1]}\n")
    async with B.session():
        for maker in (piece_one, piece_two, piece_three):
            html, out, W, H, els, bg = await maker()
            lay.preflight(W, H, els, html=html, page_bg=bg, core=core)
            await B.render(html, out, W, H, elements=els)
            print(f"  -> {out}\n")

asyncio.run(main())
