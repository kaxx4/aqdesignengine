"""Workflow C -- bespoke fresh poster ("126 return visits to one partner in Kolkata"), ops dept,
LANDSCAPE canvas (linkedin, 1200x628). v3 -- v2 looked genuinely good (see friction notes); this
version only cleans up two gate-stack complaints v2 left printing, it does not change the design:

  1. audit.py's DOM overlap check (auto-run inside B.render, separate from layout.preflight's
     tuple-based collision_check) flagged all 5 sticker x wordmark overlaps as ISSUES, even
     though I'd already declared them intentional via `collision_ignore` -- that parameter only
     threads into layout.preflight's check, not into audit.py's own SKIP_PAIRS whitelist, and
     that whitelist is a fixed vocabulary of literal `data-tag` strings baked into audit.py
     (word/word, stk/stk, sign/sign, ...) that a bespoke script cannot add to or parametrize.
     The one thing that DOES suppress an audit.py overlap regardless of tag: parent/child DOM
     nesting is skipped outright (`if nest[i]==j or nest[j]==i: continue`). So v3 nests the
     sticker divs INSIDE the wordmark div as real DOM children instead of positioning them as
     page-level siblings at absolute coordinates -- which is also more architecturally honest
     (they are visually part of the wordmark signature, not independent objects), and it is the
     same "prefer nesting" fix CLAUDE.md Sec 7a recommends for contains_check.
  2. audit.py's own margin check uses a HARDCODED M=64 (module-level constant, not derived from
     the canvas or from build.py's own M) and flagged the wordmark's right edge by a mere 1px
     (r1140 vs the aW-M+3=1139 threshold) and left edge by 1px (x60 vs M-3=61). Not a visible
     margin problem at all -- purely a threshold graze -- but rather than lean on a hair's-width
     coincidence, v3 tightens the wordmark's target width from 1080 to 1050px so it clears the
     threshold with an honest ~5px of headroom on each side.

See scratchpad/c3_v1.py and c3_v2.py for the full style/measurement/re-proportioning writeup and
the v1->v2 fix list (hierarchy, the real collision, the italic measurement gap, false-positive
collision noise, and declaring the sticker/wordmark overlap as intentional).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/c3_v3.py
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["linkedin"]     # 1200 x 628
M = 64
A = core.ACCENTS
TEAL = core.accent_for("ops")
CREAM = "#F4EFE0"
WHITE = "#FFFFFF"

TOP_H = 108
PANEL_Y = TOP_H
PANEL_H = H - TOP_H

# empirical italic calibration -- see docstring point 3. NOT a general constant; specific to
# Instrument Serif italic rendering "aquaterra" (measured off v1's real reconcile output).
WORD_W_PER_PX = 1231 / 335
WORD_H_PER_PX = 355 / 335

elements = []   # (label, x, y, w, h) -- placed OBJECTS only, never full-bleed background fills

async def measure_all():
    items = [
        {"text": "126", "font": "d", "size": 64, "weight": 900, "line_height": 0.9},
        {"text": "return visits, one partner", "font": "m", "size": 14, "weight": 500},
        {"text": "kolkata", "font": "e", "size": 40, "weight": 600},
        {"text": "same site, revisited", "font": "m", "size": 14, "weight": 500},
        {"text": "built on trust", "font": "e", "size": 32, "weight": 600, "max_width": 300, "line_height": 1.15},
        {"text": "showing up, repeatedly", "font": "m", "size": 14, "weight": 500},
        {"text": "@ngo.aquaterra", "font": "m", "size": 14, "weight": 700},
    ]
    return await B.measure_text(items, W, H)

meas = asyncio.run(measure_all())
(m_num, m_cap1, m_kolkata, m_cap2, m_trust, m_cap3, m_handle) = meas
for name, m in zip(["126", "cap1", "kolkata", "cap2", "trust", "cap3", "handle"], meas):
    print(f"  {name:8} w={m['w']:4} h={m['h']:4} ink_h={m['ink_h']:4} glyph_w={m['glyph_w']} lines={m['lines']}")

# ---- solve wordmark size from the empirical calibration, targeting a safe width ----
TARGET_WORD_W = 1050
word_size = round(TARGET_WORD_W / WORD_W_PER_PX)
word_w_final = word_size * WORD_W_PER_PX
word_h_final = word_size * WORD_H_PER_PX
print(f"  wordmark  font-size={word_size} -> predicted {word_w_final:.0f}x{word_h_final:.0f}")

async def build_and_render():
    global elements
    parts = []

    def pill(text, x, y, w=None):
        w = w or (len(text) * 9 + 40)
        parts.append(
            f'<div class="measure" data-tag="pill" style="position:absolute;left:{x}px;top:{y}px;'
            f'background:{CREAM};color:{core.INK};font-family:var(--m);font-weight:700;font-size:13px;'
            f'letter-spacing:.12em;padding:8px 16px;border-radius:999px;border:3px solid {core.INK};'
            f'box-shadow:{core.hard_shadow("sm")};z-index:10;white-space:nowrap">{text}</div>')
        elements.append((f"pill:{text}", x, y, w, 34))

    # ---- background: page() already paints CREAM for `.p`; only the teal panel is drawn ----
    parts.append(f'<div style="position:absolute;left:0;top:{PANEL_Y}px;width:{W}px;height:{PANEL_H}px;'
                 f'background:{TEAL}"></div>')

    # ---- top cream strip: logo + dept/location kicker ----
    parts.append(B.logo(dark=False, x=M, y=(TOP_H - 32) // 2))
    elements.append(("logo", M, (TOP_H - 32) // 2, 150, 32))
    kicker = "OPS · KOLKATA"
    parts.append(f'<span style="position:absolute;right:{M}px;top:{(TOP_H-16)//2}px;font-family:var(--m);'
                 f'font-weight:700;font-size:14px;letter-spacing:.12em;color:var(--ink3);'
                 f'z-index:20">{kicker}</span>')
    elements.append(("kicker", W - M - 160, (TOP_H - 16) // 2, 160, 16))
    parts.append(f'<div style="position:absolute;left:0;top:{TOP_H-2}px;width:{W}px;height:2px;background:{core.INK}"></div>')

    # ---- 3-column info block (modest, equal scale -- the wordmark is the one hero) ----
    col_y = PANEL_Y + 28
    col_w = (W - 2 * M - 2 * 40) / 3
    col_xs = [M, M + col_w + 40, M + 2 * (col_w + 40)]
    col_bottoms = []

    # column 1 -- THE COUNT
    x0 = col_xs[0]
    pill("THE COUNT", x0, col_y)
    num_y = col_y + 34 + 10
    parts.append(f'<div class="measure" data-tag="hero-num" style="position:absolute;left:{x0}px;top:{num_y}px;'
                 f'font-family:var(--d);font-weight:900;font-size:64px;line-height:.9;color:{WHITE};'
                 f'z-index:10">126</div>')
    elements.append(("num126", x0, num_y, m_num["glyph_w"], m_num["ink_h"]))
    cap1_y = num_y + m_num["ink_h"] + 10
    parts.append(f'<div style="position:absolute;left:{x0}px;top:{cap1_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">return visits, one partner</div>')
    elements.append(("cap1", x0, cap1_y, m_cap1["w"], m_cap1["h"]))
    col_bottoms.append(cap1_y + m_cap1["h"])

    # column 2 -- THE PLACE
    x1 = col_xs[1]
    pill("THE PLACE", x1, col_y)
    val2_y = col_y + 34 + 10
    parts.append(f'<div style="position:absolute;left:{x1}px;top:{val2_y}px;font-family:var(--e);font-weight:600;'
                 f'font-size:40px;color:{WHITE};z-index:10">kolkata</div>')
    elements.append(("kolkata", x1, val2_y, m_kolkata["w"], m_kolkata["h"]))
    cap2_y = val2_y + m_kolkata["h"] + 10
    parts.append(f'<div style="position:absolute;left:{x1}px;top:{cap2_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">same site, revisited</div>')
    elements.append(("cap2", x1, cap2_y, m_cap2["w"], m_cap2["h"]))
    col_bottoms.append(cap2_y + m_cap2["h"])

    # column 3 -- THE POINT (one Instrument Serif italic accent word: "trust")
    x2 = col_xs[2]
    pill("THE POINT", x2, col_y)
    val3_y = col_y + 34 + 10
    parts.append(f'<div style="position:absolute;left:{x2}px;top:{val3_y}px;width:300px;font-family:var(--e);'
                 f'font-weight:600;font-size:32px;line-height:1.15;color:{WHITE};z-index:10">built on '
                 f'<span style="font-family:var(--s);font-style:italic;font-weight:400;color:{A[2]}">trust</span></div>')
    elements.append(("trust", x2, val3_y, m_trust["w"], m_trust["h"]))
    cap3_y = val3_y + m_trust["h"] + 10
    parts.append(f'<div style="position:absolute;left:{x2}px;top:{cap3_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">showing up, repeatedly</div>')
    elements.append(("cap3", x2, cap3_y, m_cap3["w"], m_cap3["h"]))
    col_bottoms.append(cap3_y + m_cap3["h"])

    col_block_bottom = max(col_bottoms)
    print(f"  column block bottom = {col_block_bottom:.0f}")

    # ---- giant wordmark signature along the bottom edge ----
    word_x = (W - word_w_final) / 2
    word_y = H - 6 - word_h_final
    gap_to_columns = word_y - col_block_bottom
    print(f"  wordmark top={word_y:.0f}  gap above columns={gap_to_columns:.0f}")
    elements.append(("wordmark", word_x, word_y, word_w_final, word_h_final))

    # ---- stickers glued onto the wordmark's upper strokes ----
    # NESTED as real DOM children of the wordmark div (not page-level siblings at absolute
    # page coordinates) so audit.py's parent/child skip applies -- see docstring point 1.
    # `elements` still records each sticker's true PAGE-space bbox for the tuple-world
    # checks (bounds/collision/reconcile), which don't care about DOM nesting, only geometry.
    stick_specs = [
        ("heart",     A[0], 70, 0.05, -14, -10),
        ("star",      A[2], 60, 0.26, -8,  12),
        ("thumbsup",  A[1], 76, 0.50, 6,   -8),
        ("burst",     A[4], 82, 0.72, -12, 6),
        ("spiral",    A[5], 56, 0.92, 10,  0),
    ]
    sticker_children = []
    collision_ignore = set()
    for kind, col, size, frac, dy, rot in stick_specs:
        sx_rel = word_w_final * frac      # relative to the wordmark div's own box
        sy_rel = dy
        sx_page = word_x + sx_rel
        sy_page = word_y + sy_rel
        svg = dd.stamp(kind, col, rot=rot)
        sticker_children.append(
            f'<div class="dood measure" data-tag="sticker-{kind}" style="position:absolute;'
            f'left:{sx_rel}px;top:{sy_rel}px;width:{size}px;height:{size}px;z-index:12;'
            f'filter:drop-shadow(3px 3px 0 {core.INK})">{svg}</div>')
        elements.append((f"sticker_{kind}", sx_page, sy_page, size, size))
        collision_ignore.add(frozenset({"wordmark", f"sticker_{kind}"}))

    parts.append(f'<div class="measure" data-tag="wordmark" style="position:absolute;left:{word_x}px;'
                 f'top:{word_y}px;width:{word_w_final}px;font-family:var(--s);'
                 f'font-style:italic;font-weight:400;font-size:{word_size}px;line-height:.82;color:{CREAM};'
                 f'white-space:nowrap;z-index:6">aquaterra'
                 + "".join(sticker_children) + '</div>')

    # ---- footer handle, top-right of the panel (clear of the column block) ----
    handle_w = m_handle["w"] + 24
    handle_x = W - M - handle_w
    handle_y = TOP_H + 14
    parts.append(f'<div style="position:absolute;left:{handle_x}px;top:{handle_y}px;background:{core.INK};'
                 f'color:{CREAM};font-family:var(--m);font-weight:700;font-size:14px;padding:6px 12px;'
                 f'border-radius:999px;z-index:20;white-space:nowrap">@ngo.aquaterra</div>')
    elements.append(("handle", handle_x, handle_y, handle_w, 28))

    inner = "".join(parts)
    html = B.page(W, H, CREAM, inner, grain=False)

    color_pairs = [
        ("panel", TEAL, CREAM),
        ("num126", WHITE, TEAL),
        ("kolkata", WHITE, TEAL),
        ("wordmark", CREAM, TEAL),
        ("trust", A[2], TEAL),
    ]

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                       page_bg=CREAM, core=core, expect_hero=True, min_hero_frac=0.08,
                       collision_ignore=collision_ignore)

    os.makedirs("out/session10f", exist_ok=True)
    await B.render(html, "out/session10f/c3_v3.png", W, H, elements=elements,
                   color_pairs=color_pairs, page_bg=CREAM, expect_hero=True,
                   collision_ignore=collision_ignore)
    print("done -> out/session10f/c3_v3.png")

asyncio.run(build_and_render())
