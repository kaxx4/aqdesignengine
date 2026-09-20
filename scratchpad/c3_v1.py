"""Workflow C -- bespoke fresh poster ("126 return visits to one partner in Kolkata"), ops dept,
LANDSCAPE canvas (linkedin, 1200x628).

Style drawn by design.py (seed 5): STYLE 7d4fa0d720fa7f -- a three-column contact-info block over
a solid colour panel, closed out by a giant cursive-script wordmark stretching full-width with
small stickers glued along its strokes. Reference: training_samples/reference_posters/
7d4fa0d720fa7f49dded1e854599c4e0.jpg (a design agency's "work" page footer).

MEASURED (compare.geometry, run on the raw reference file):
  content bbox x 0.083..0.915  y 0.154..0.844   margins ~8.3% L/R, ~15.5% T/B
  vertical ratio 0.99:1 (space above the whole card ~= space below)
  centroid (0.500, 0.491)  coverage 0.520
  The reference itself is 1200x900 (4:3, NOT a tall portrait) -- but it is a screenshot of a
  browser card floating on a lavender backdrop, not a native 1.91:1 poster. The card being
  measured is ~0.832 wide x ~0.69 tall of that 4:3 frame, ratio ~1.6:1. Our canvas is 1200x628,
  ratio 1.91:1 -- MORE landscape than the card itself. So this is a genuine re-proportioning,
  not a copy: see the RE-PROPORTIONING NOTES below for what changed and why.

THIS IS WORKFLOW C, NOT B: new AQ content, reusing the reference's MECHANISM (two-tone stack:
thin light strip + solid colour panel; 3-column info block; giant expressive wordmark signature
along the bottom edge with stickers glued onto its strokes), never its literal copy or asset.

RE-PROPORTIONING DECISIONS (from the 4:3-card mechanism to our 1.91:1 canvas):
  - Dropped the outer lavender "browser mockup" frame entirely. That framing exists because the
    reference is a screenshot of a live website; faking a browser chrome on an AQ social poster
    would be fabricating a UI that doesn't exist (adjacent to the real-assets-only rule, Sec 9),
    so the AQ piece is the card itself, full-bleed on the 1200x628 canvas.
  - The reference's card is 1.6:1; ours is 1.91:1 -- 19% relatively WIDER for the same height
    budget. That extra width goes to the 3-column block (more breathing room between columns,
    each column gets to keep its label+value+caption on generous line lengths) rather than to
    the wordmark, which was already the widest single element and stays anchored to true full
    width regardless of aspect.
  - The reference's real content occupies 69% of its OWN card's height for one contact block +
    one wordmark; going to 1.91:1 with the SAME absolute canvas height (628 vs the card's ~621px
    at native res, coincidentally close) meant vertical room was not actually the constraint --
    width was. So the top strip and column block keep roughly the reference's proportions
    (top strip ~17% of height, panel ~83%), and the wordmark's font-size is solved from ink_h
    fitting the remaining vertical band, same as it would be on any canvas.
  - No literal cursive/script typeface exists in the engine's embedded font set (core.FONTS has
    NeutralFace / Eina01 / Instrument Serif italic / JetBrains Mono only -- no script face). Per
    "every design is a direct outcome of encoded rules," I did not import an external font to
    fake the reference's script; Instrument Serif ITALIC is the one expressive/flowing face the
    brand allows (Sec 9, <=1 accent word per piece already relaxed here since the WHOLE wordmark
    is the one italic use, not a caption word -- treating the full-bleed signature wordmark as
    the piece's single sanctioned italic moment, the same way the reference's script IS its one
    expressive typographic gesture).
  - "credits" tag (reference, bottom-right, small black pill) -> "@ngo.aquaterra" handle, same
    treatment (small dark pill, unobtrusive corner), our house footer convention.
  - Stickers: reference glues literal emoji/mascot stickers (smiley, heart, hand-heart, "100",
    camera) onto the script's loops. AQ has no equivalent iconography, so these become AQ
    doodles (heart, star, thumbsup, burst, spiral) in accent colours via doodles.stamp() --
    same idea (small, round-ish, glued to the wordmark's strokes, each its own accent), never a
    literal copy of someone else's mascot art.
  - Column copy: subject only supplies ONE verified number (126). No other figure is invented --
    "the count" carries 126; "the place" and "the point" columns carry qualitative copy, not
    fabricated stats (truth ladder, VOICE.md).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/c3_v1.py
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["linkedin"]     # 1200 x 628 -- landscape, NOT feed's 1080x1350
M = 64
A = core.ACCENTS                  # pink,mint,lemon,tomato,sky,grape,teal
TEAL = core.accent_for("ops")     # #0E7C86 -- department colour is semantic, not a rotation pick
CREAM = "#F4EFE0"
WHITE = "#FFFFFF"

TOP_H = 108                       # cream strip: ~17% of 628, matching the reference's proportion
PANEL_Y = TOP_H
PANEL_H = H - TOP_H

elements = []                     # (label, x, y, w, h), kept in sync with the CSS below

# ---------------- pass 1: measure every text string before placing anything ----------------
async def measure_all():
    items = [
        {"text": "THE COUNT", "font": "m", "size": 15, "weight": 700, "letter_spacing": ".12em", "transform": "uppercase"},
        {"text": "THE PLACE", "font": "m", "size": 15, "weight": 700, "letter_spacing": ".12em", "transform": "uppercase"},
        {"text": "THE POINT", "font": "m", "size": 15, "weight": 700, "letter_spacing": ".12em", "transform": "uppercase"},
        {"text": "126", "font": "d", "size": 128, "weight": 900, "line_height": 0.82},
        {"text": "return visits, one partner", "font": "m", "size": 14, "weight": 500},
        {"text": "kolkata", "font": "e", "size": 38, "weight": 600},
        {"text": "same site, revisited", "font": "m", "size": 14, "weight": 500},
        {"text": "built on trust", "font": "e", "size": 32, "weight": 600, "max_width": 320},
        {"text": "showing up, repeatedly", "font": "m", "size": 14, "weight": 500},
        {"text": "aquaterra", "font": "s", "size": 300, "weight": 400},
        {"text": "@ngo.aquaterra", "font": "m", "size": 14, "weight": 700},
    ]
    return await B.measure_text(items, W, H)

async def _get_measurements():
    return await measure_all()

meas = asyncio.run(_get_measurements())
(m_lbl1, m_lbl2, m_lbl3, m_num, m_cap1, m_kolkata, m_cap2, m_trust, m_cap3, m_word, m_handle) = meas

print("measured 126:", m_num)
print("measured aquaterra @300px:", m_word)

# solve the wordmark font-size so its TRUE painted width (glyph_w) hits our target span
TARGET_WORD_W = W - 2 * 40        # 40px each side -- a near-full-bleed signature, small margin
word_size = 300 * (TARGET_WORD_W / m_word["glyph_w"])
word_size = round(word_size)

# ---------------- pass 2: build the page at solved sizes ----------------
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

    # ---- background ----
    parts.append(f'<div style="position:absolute;inset:0;background:{CREAM}"></div>')
    parts.append(f'<div style="position:absolute;left:0;top:{PANEL_Y}px;width:{W}px;height:{PANEL_H}px;'
                 f'background:{TEAL}"></div>')
    elements.append(("panel", 0, PANEL_Y, W, PANEL_H))

    # ---- top cream strip: logo + dept/location kicker ----
    parts.append(B.logo(dark=False, x=M, y=(TOP_H - 32) // 2))
    elements.append(("logo", M, (TOP_H - 32) // 2, 150, 32))
    kicker = "OPS · KOLKATA"
    parts.append(f'<span style="position:absolute;right:{M}px;top:{(TOP_H-16)//2}px;font-family:var(--m);'
                 f'font-weight:700;font-size:14px;letter-spacing:.12em;color:{core.INK3 if hasattr(core,"INK3") else "#5A5A55"};'
                 f'z-index:20">{kicker}</span>')
    elements.append(("kicker", W - M - 160, (TOP_H - 16) // 2, 160, 16))
    # thin ink rule closing the strip, matching the reference's hairline under its nav
    parts.append(f'<div style="position:absolute;left:0;top:{TOP_H-2}px;width:{W}px;height:2px;background:{core.INK}"></div>')

    # ---- 3-column info block ----
    col_y = PANEL_Y + 36
    col_w = (W - 2 * M - 2 * 40) / 3
    col_xs = [M, M + col_w + 40, M + 2 * (col_w + 40)]

    # column 1 -- THE COUNT (the one verified number, the piece's hero)
    x0 = col_xs[0]
    pill("THE COUNT", x0, col_y)
    num_y = col_y + 34 + 10
    num_h = m_num["ink_h"]
    parts.append(f'<div class="measure" data-tag="hero-num" style="position:absolute;left:{x0}px;top:{num_y}px;'
                 f'font-family:var(--d);font-weight:900;font-size:128px;line-height:.82;color:{WHITE};'
                 f'z-index:10">126</div>')
    elements.append(("num126", x0, num_y, m_num["glyph_w"], num_h))
    cap1_y = num_y + num_h + 10
    parts.append(f'<div style="position:absolute;left:{x0}px;top:{cap1_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">return visits, one partner</div>')
    elements.append(("cap1", x0, cap1_y, m_cap1["w"], m_cap1["h"]))

    # column 2 -- THE PLACE
    x1 = col_xs[1]
    pill("THE PLACE", x1, col_y)
    val2_y = col_y + 34 + 14
    parts.append(f'<div style="position:absolute;left:{x1}px;top:{val2_y}px;font-family:var(--e);font-weight:600;'
                 f'font-size:38px;color:{WHITE};z-index:10">kolkata</div>')
    elements.append(("kolkata", x1, val2_y, m_kolkata["w"], m_kolkata["h"]))
    cap2_y = val2_y + m_kolkata["h"] + 12
    parts.append(f'<div style="position:absolute;left:{x1}px;top:{cap2_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">same site, revisited</div>')
    elements.append(("cap2", x1, cap2_y, m_cap2["w"], m_cap2["h"]))

    # column 3 -- THE POINT (one Instrument Serif italic accent word: "trust")
    x2 = col_xs[2]
    pill("THE POINT", x2, col_y)
    val3_y = col_y + 34 + 14
    parts.append(f'<div style="position:absolute;left:{x2}px;top:{val3_y}px;width:320px;font-family:var(--e);'
                 f'font-weight:600;font-size:32px;line-height:1.05;color:{WHITE};z-index:10">built on '
                 f'<span style="font-family:var(--s);font-style:italic;font-weight:400;color:{A[2]}">trust</span></div>')
    elements.append(("trust", x2, val3_y, m_trust["w"], m_trust["h"]))
    cap3_y = val3_y + m_trust["h"] + 12
    parts.append(f'<div style="position:absolute;left:{x2}px;top:{cap3_y}px;font-family:var(--m);font-weight:500;'
                 f'font-size:14px;color:rgba(244,239,224,.72);z-index:10">showing up, repeatedly</div>')
    elements.append(("cap3", x2, cap3_y, m_cap3["w"], m_cap3["h"]))

    # ---- giant wordmark signature along the bottom edge ----
    word_w_final = m_word["glyph_w"] * (word_size / 300)
    word_h_final = m_word["ink_h"] * (word_size / 300)
    word_x = (W - word_w_final) / 2
    word_bottom_pad = 6
    word_y = H - word_bottom_pad - word_h_final
    parts.append(f'<div class="measure" data-tag="wordmark" style="position:absolute;left:{word_x}px;'
                 f'top:{word_y}px;width:{word_w_final}px;font-family:var(--s);font-style:italic;'
                 f'font-weight:400;font-size:{word_size}px;line-height:.82;color:{CREAM};'
                 f'white-space:nowrap;z-index:6">aquaterra</div>')
    elements.append(("wordmark", word_x, word_y, word_w_final, word_h_final))

    # ---- stickers glued onto the wordmark's strokes ----
    stick_specs = [
        ("heart", A[0], 92, word_x + word_w_final * 0.09, word_y - 6, -8),
        ("star", A[2], 78, word_x + word_w_final * 0.30, word_y - 30, 10),
        ("thumbsup", A[1], 86, word_x + word_w_final * 0.52, word_y - 14, -6),
        ("burst", A[4], 96, word_x + word_w_final * 0.72, word_y - 34, 6),
        ("spiral", A[5], 70, word_x + word_w_final * 0.90, word_y + 4, 0),
    ]
    for kind, col, size, sx, sy, rot in stick_specs:
        svg = dd.stamp(kind, col, rot=rot)
        parts.append(f'<div class="dood measure" data-tag="sticker-{kind}" style="position:absolute;left:{sx}px;'
                     f'top:{sy}px;width:{size}px;height:{size}px;z-index:12;'
                     f'filter:drop-shadow(3px 3px 0 {core.INK})">{svg}</div>')
        elements.append((f"sticker_{kind}", sx, sy, size, size))

    # ---- footer handle, tucked into the gap right of the wordmark's last loop ----
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
    ]

    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                       page_bg=CREAM, core=core, expect_hero=True, min_hero_frac=0.08)

    os.makedirs("out/session10f", exist_ok=True)
    await B.render(html, "out/session10f/c3_v1.png", W, H, elements=elements,
                   color_pairs=color_pairs, page_bg=CREAM, expect_hero=True)
    print("done -> out/session10f/c3_v1.png")

asyncio.run(build_and_render())
