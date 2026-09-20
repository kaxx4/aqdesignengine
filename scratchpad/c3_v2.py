"""Workflow C -- bespoke fresh poster ("126 return visits to one partner in Kolkata"), ops dept,
LANDSCAPE canvas (linkedin, 1200x628). v2 -- fixes from the v1 looking-gate + gate-stack failures.

See scratchpad/c3_v1.py for the full style/measurement/re-proportioning writeup. v2 changes only:

WHAT WAS WRONG IN v1 (both the gate stack AND the eye caught real bugs):
  1. HIERARCHY BUG (eye only): "126" at 128px NeutralFace competed with the wordmark for hero
     status -- two heroes, and the number's tall bbox ate into the wordmark's vertical budget,
     causing the collision in (2). Fixed: all three columns now use comparable, modest value
     sizes (64/40/32px) -- the WORDMARK is the singular hero, matching the reference's own
     hierarchy (an unmissable full-width signature; the info columns are secondary, same scale
     as each other).
  2. REAL COLLISION (gate caught it): hero-num x wordmark overlapped 235x56px, and every sticker
     overlapped the wordmark AND the column text above it, because the wordmark's rendered size
     was wrong (see 3) and column 1 ran too tall. Fixed by (1) plus giving a real 40+px gap
     between the column block's lowest point and the wordmark's top before sizing either.
  3. MEASUREMENT GAP (gate caught it, cause diagnosed after): `build.measure_text()` has NO
     font-style parameter -- its own JS measurer builds `cx.font` from weight+size+family only
     (engine/build.py's canvas-measure block), so italic can never be requested through the
     public API. I measured "aquaterra" WITHOUT italic and scaled from that, but the actual
     element uses font-style:italic, and italic Instrument Serif is measurably WIDER per point
     size than its roman face. Result: predicted width 1120px, ACTUAL rendered width 1231px (+
     ~10%) -- reconcile.measure_dom's OVERSIZE warning ("real width 1231px vs 1120px box") is
     what surfaced this, and the wordmark bled 71px off the right edge of a 1200px canvas with
     NO static check flagging it (bounds_check trusted the declared-but-wrong bbox tuple --
     literally the catalogue's own "stale bbox hides real off-canvas" row, self-inflicted here
     because I fed it a bbox computed from a systematically wrong measurement, not a stale one).
     FIX: there is no italic-aware measurement primitve, so v2 calibrates directly off v1's own
     REAL rendered numbers (a true, if single, data point) rather than off measure_text: at
     font-size 335px the italic string actually painted 1231x355. Text width/height scale
     linearly with font-size for a fixed string (no wrapping, letter-spacing 0), so
       WORD_W_PER_PX = 1231/335 = 3.67463
       WORD_H_PER_PX = 355/335  = 1.05970
     solve the wanted font-size from these instead. This is a real workaround for a real API
     gap, not a guess -- but it is brittle (specific to this exact string+face) and worth fixing
     properly in build.measure_text() (add a `style` field) rather than re-deriving per script.
  4. FALSE-POSITIVE NOISE: `preflight`'s collision_check flagged the full-bleed "panel" rect
     against every element placed on it (everything "collides" with its own background). Fixed
     by not including background/panel rects in the `elements` list at all -- they were never a
     part of collision-check's intended input (a placed OBJECT), matching how the CLAUDE.md
     template's own worked example never adds page-spanning fills to `elements` either.
  5. INTENTIONAL OVERLAP: stickers glued onto the wordmark's strokes are BY DESIGN overlapping
     it (that is the whole reference mechanism) -- declared via `collision_ignore` instead of
     letting the gate flag five real-looking "collisions" that are actually the point.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/c3_v2.py
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
TARGET_WORD_W = 1080
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
    parts.append(f'<div class="measure" data-tag="wordmark" style="position:absolute;left:{word_x}px;'
                 f'top:{word_y}px;width:{word_w_final}px;font-family:var(--s);font-style:italic;'
                 f'font-weight:400;font-size:{word_size}px;line-height:.82;color:{CREAM};'
                 f'white-space:nowrap;z-index:6">aquaterra</div>')
    elements.append(("wordmark", word_x, word_y, word_w_final, word_h_final))

    # ---- stickers glued onto the wordmark's upper strokes (by-design overlap with it) ----
    stick_specs = [
        ("heart",     A[0], 70, 0.05, -14, -10),
        ("star",      A[2], 60, 0.26, -8,  12),
        ("thumbsup",  A[1], 76, 0.50, 6,   -8),
        ("burst",     A[4], 82, 0.72, -12, 6),
        ("spiral",    A[5], 56, 0.92, 10,  0),
    ]
    collision_ignore = set()
    for kind, col, size, frac, dy, rot in stick_specs:
        sx = word_x + word_w_final * frac
        sy = word_y + dy
        svg = dd.stamp(kind, col, rot=rot)
        parts.append(f'<div class="dood measure" data-tag="sticker-{kind}" style="position:absolute;left:{sx}px;'
                     f'top:{sy}px;width:{size}px;height:{size}px;z-index:12;'
                     f'filter:drop-shadow(3px 3px 0 {core.INK})">{svg}</div>')
        elements.append((f"sticker_{kind}", sx, sy, size, size))
        collision_ignore.add(frozenset({"wordmark", f"sticker_{kind}"}))

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
    await B.render(html, "out/session10f/c3_v2.png", W, H, elements=elements,
                   color_pairs=color_pairs, page_bg=CREAM, expect_hero=True,
                   collision_ignore=collision_ignore)
    print("done -> out/session10f/c3_v2.png")

asyncio.run(build_and_render())
