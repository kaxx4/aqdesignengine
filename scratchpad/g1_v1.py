"""Workflow C -- bespoke FRESH poster (no reference), brief:
"126 return visits to one partner in Kolkata", dept welfare (mint, core.accent_for).

Style drawn from brain/STYLE_BANK.json:
  PYTHONIOENCODING=utf-8 python design.py "126 return visits to one partner in Kolkata" --dept welfare --seed 31
  -> STYLE 62f8cc4d3c6135: "staggered rows of pills bleeding off BOTH edges, brick-offset
     per row" (hero: pile). Reference is 1.536:1 landscape; feed is 0.8:1 (taller) so the
     brief itself says: re-solve for the frame, stack more rows rather than stretching.
     Recipe explicitly allows "one rotated ink slab over the field partway down, with a
     keyline ring so it reads as laid over the pills" -- that slab carries the hero number.

CONTENT (truth ladder, VOICE.md sec2): "126 return visits" and "Pather Sathi" are COUNTED,
off welfare_projects_rows.csv per brain/DECISIONS.md SESSION 10 sec10 ("126 returns to one
partner, two spellings of Pather Sathi merged") and out/CSV_IMAGE_FILL/welfare_projects_rows_FILLED.csv
(real rows: Pather Sathi / Pather Saathi, Kolkata). No invented number appears anywhere below.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/g1_v1.py
"""
import asyncio, os, sys, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); sh = load("shapes")

W, H = core.SIZES["feed"]              # 1080 x 1350 -- feed is the default, portrait
M = 64
ACCENT = core.accent_for("welfare")    # #1B8A5A mint -- department colour is semantic, not a rotation
INK = core.INK

WORDS = ["PATHER SATHI", "KOLKATA", "RETURN VISIT", "WELFARE", "AQUATERRA",
         "SUNDAY SCHOOL", "VOLUNTEERS", "WORKSHOP", "SATURDAYS"]
CALLOUT = "PATHER SATHI"               # the one partner -- gets the mint fill + dot


def clip(x, y, w, h):
    """Visible-on-canvas portion of a bbox that is allowed to bleed off-edge by
    design. The .p container is overflow:hidden, so the TRUE visible extent of a
    bleeding pill *is* this clipped rect -- bounds_check/collision_check should
    see what actually shows, not the full CSS box that intentionally continues
    past the frame."""
    x2, y2 = min(x + w, W), min(y + h, H)
    x0, y0 = max(x, 0), max(y, 0)
    return (x0, y0, max(0, x2 - x0), max(0, y2 - y0))


async def main():
    elements = []          # (label, x, y, w, h) -- CLIPPED/visible bboxes, gate input
    color_pairs = []       # (label, fill, surface)
    parts = []             # html fragments, in z-order

    # ---------------------------------------------------------------- measure
    pill_font = dict(font="e", weight=700, size=24, transform="none")
    to_measure = [dict(text=w, **pill_font) for w in WORDS]
    to_measure += [
        dict(text="PATHER SATHI · KOLKATA", font="m", weight=700, size=17, letter_spacing="0.08em"),
        dict(text="126", font="d", weight=900, size=280),
        dict(text="RETURN VISITS", font="d", weight=900, size=46, letter_spacing="0.01em"),
        dict(text="counted across AquaTerra's welfare log, 2021–2026", font="m", weight=500, size=14),
    ]
    m = await B.measure_text(to_measure, W, H)
    word_w = {WORDS[i]: m[i]["text_w"] for i in range(len(WORDS))}
    slab_eyebrow_m, num_m, sub_m, qual_m = m[len(WORDS):]

    # ---------------------------------------------------------------- header
    parts.append(B.logo())
    eyebrow_y = 60
    parts.append(
        f'<div style="position:absolute;top:{eyebrow_y}px;right:{M}px;font-family:var(--m);'
        f'font-weight:700;font-size:15px;letter-spacing:.1em;text-transform:uppercase;'
        f'color:var(--ink3);z-index:20">WELFARE · KOLKATA</div>'
    )
    elements.append(("logo", M, 56, 150, 32))
    elements.append(("eyebrow_tr", W - M - 220, eyebrow_y, 220, 20))

    # ---------------------------------------------------------------- pill field
    # Rows bleed off BOTH left and right edges (the mechanism, per the drawn style's
    # recipe) -- brick-offset row to row. Feed is much taller than the 1.536:1
    # reference, so roughly double the row count rather than stretching pill size.
    PILL_H = 58
    GAP_X = 16
    ROW_PITCH = 82
    row_top = 168
    row_bottom = 1258
    n_rows = 1 + (row_bottom - row_top) // ROW_PITCH   # ~14 rows

    pill_labels = []   # (label, x, y, w, h, word, is_callout)
    for r in range(n_rows):
        y = row_top + r * ROW_PITCH
        offset = -90 if r % 2 == 0 else -170          # brick offset alternates row to row
        x = offset
        wi = r % len(WORDS)                            # rotate the word list per row
        col = 0
        while x < W + 140:
            word = WORDS[(wi + col) % len(WORDS)]
            pw = word_w[word] + 52                      # + horizontal pad (26px each side)
            label = f"pill_{r}_{col}"
            pill_labels.append((label, x, y, pw, PILL_H, word, word == CALLOUT))
            x += pw + GAP_X
            col += 1

    for label, x, y, w, h, word, callout in pill_labels:
        fill = ACCENT if callout else "var(--bg2)"
        fg = core.text_on(ACCENT) if callout else INK
        dot = (f'<span style="width:11px;height:11px;border-radius:50%;background:{INK if callout else ACCENT};'
               f'display:inline-block;margin-right:9px;flex:none"></span>') if callout else ""
        parts.append(
            f'<div style="position:absolute;top:{round(y)}px;left:{round(x)}px;width:{round(w)}px;'
            f'height:{h}px;background:{fill};border:3px solid var(--ink);border-radius:999px;'
            f'box-shadow:{core.hard_shadow("sm")};display:flex;align-items:center;justify-content:center;'
            f'font-family:var(--e);font-weight:700;font-size:24px;color:{fg};white-space:nowrap;z-index:6">'
            f'{dot}{word}</div>'
        )
        cx, cy, cw, ch = clip(x, y, w, h)
        if cw > 0 and ch > 0:
            elements.append((label, cx, cy, cw, ch))
        color_pairs.append((label, fill, "var(--bg)"))

    # ---------------------------------------------------------------- the ink slab (hero)
    SLAB_W, SLAB_H = 860, 430
    slab_x = (W - SLAB_W) / 2
    slab_y = 560
    ROT = -3
    slab_label = "slab"
    parts.append(
        f'<div style="position:absolute;top:{slab_y}px;left:{slab_x}px;width:{SLAB_W}px;height:{SLAB_H}px;'
        f'background:var(--ink);border-radius:32px;transform:rotate({ROT}deg);'
        f'box-shadow:{core.keyline(ring_bg="var(--bg)")}, {core.hard_shadow("xl")};z-index:15">'
        # eyebrow
        f'<div style="position:absolute;top:44px;left:56px;font-family:var(--m);font-weight:700;'
        f'font-size:17px;letter-spacing:.08em;color:{core.on_dark(ACCENT, 17)};text-transform:uppercase">'
        f'PATHER SATHI · KOLKATA</div>'
        # hero numeral
        f'<div style="position:absolute;top:76px;left:52px;font-family:var(--d);font-weight:900;'
        f'font-size:280px;line-height:.78;color:{core.on_dark(ACCENT, 280)}">126</div>'
        # subhead
        f'<div style="position:absolute;top:322px;left:56px;font-family:var(--d);font-weight:900;'
        f'font-size:46px;letter-spacing:.01em;color:var(--bg)">RETURN VISITS</div>'
        # qualifier
        f'<div style="position:absolute;bottom:34px;left:56px;font-family:var(--m);font-weight:500;'
        f'font-size:14px;color:var(--ink3);opacity:.9">counted across AquaTerra’s welfare log, 2021–2026</div>'
        f'</div>'
    )
    # rotated footprint for the gate -- the slab is rotated, so its ACTUAL bbox is
    # larger than its own W/H (layout.rotated_bbox, CLAUDE.md sec10).
    rx, ry, rw, rh = lay.rotated_bbox(slab_x, slab_y, SLAB_W, SLAB_H, ROT)
    elements.append((slab_label, rx, ry, rw, rh))
    color_pairs.append((slab_label, "var(--ink)", "var(--bg)"))

    # Slab deliberately lies OVER the pill field (the drawn style's own recipe: "pin
    # one rotated ink slab over the field ... so it reads as laid over the pills").
    # Declare that as an intentional overlap for every pill it actually touches,
    # derived from real geometry -- not a blanket ignore of the whole class.
    collision_ignore = set()
    for label, x, y, w, h, word, callout in pill_labels:
        cx, cy, cw, ch = clip(x, y, w, h)
        if cw <= 0 or ch <= 0:
            continue
        ox = min(cx + cw, rx + rw) - max(cx, rx)
        oy = min(cy + ch, ry + rh) - max(cy, ry)
        if ox > 0 and oy > 0:
            collision_ignore.add(frozenset({label, slab_label}))

    # ---------------------------------------------------------------- footer
    parts.append(
        f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
        f'font-size:13px;color:var(--ink);z-index:20">@ngo.aquaterra</span>'
    )
    elements.append(("footer", M, H - 70, 300, 20))

    inner = "".join(parts)
    html = B.page(W, H, "var(--bg)", inner, grain=True)

    os.makedirs("out/session10g", exist_ok=True)
    out_png = "out/session10g/g1_v1.png"
    async with B.session():
        await B.render(
            html, out_png, W, H,
            elements=elements,
            color_pairs=color_pairs,
            page_bg="var(--bg)",
            expect_hero=True,
            collision_ignore=collision_ignore,
        )
    print("done ->", out_png)


asyncio.run(main())
