"""Workflow C -- bespoke FRESH poster, v4 (final). See g1_v1.py for the full brief/style/
content writeup -- unchanged. v3 fixed the dead void inside the hero slab (860->680 wide,
fitted to the numeral's measured 514px). v4's ONLY change: CLAUDE.md sec9's craft layer
("thick ink outlines * hard-offset ink shadows * ONE HERO-SHINE per piece") was the one
listed craft element this build was missing -- outlines and hard shadows were present from
v1, but nothing gave the hero card a glint. Added one soft diagonal highlight across the
slab's top-left, low-alpha white, behind all text in z-order so it never touches legibility.

v3's changelog, still true here:

  1. REAL BUG, missed by every hard-fail check: the footer ("@ngo.aquaterra") visually
     collided with the bottom pill row -- text rendered struck through by the pill's ink
     border. collision_check's own min_overlap=12 threshold saw oy=12 (not >12, a graze)
     because the footer's declared bbox (guessed, not measured) undersold its real
     position relative to the last row. Fix: measure the footer text for real, and stop
     the pill field noticeably higher so there is honest clearance, not a threshold graze.
  2. invisible_colors (HARD FAIL, correctly caught in v1): pill fill var(--bg2) v.
     page var(--bg) measured 19.6 RGB-distance, under the 40 threshold -- i.e. the pill
     would be invisible if not for its ink border, which the check cannot see. Rather
     than fight a gate that is right about the FILL in isolation, picked a fill the gate
     agrees is a real second surface: #D9CFAF (measured dist 64.5).
  3. Contrast NOT hard-gated in v1 because I never passed text_pairs: the qualifier line
     used var(--ink3) (#5A5A55) on the ink slab -- contrast 2.86:1, fails AA_NORMAL (4.5)
     outright, and it read as a weak grey smear on the render. Fixed to a colour actually
     picked by measurement (#8B8880, 5.59:1) and now DECLARED via text_pairs so a future
     edit can't silently reintroduce the failure.
  4. Recipe says "each [pill] carrying a small accent dot" -- v1 only gave dots to the
     callout pill. Added a small mint dot to every third pill for rhythm, closer to the
     drawn style's own recipe.
  5. Added contains_check for the two headline strings inside the slab (hard-fail: content
     must fit the shape it's declared to belong to, CLAUDE.md sec7a).
  6. Discovered while building v1: build.render()'s "runs the full preflight for free"
     claim is only true for the elements/color/hero/text checks. Its OWN internal
     preflight call is hardcoded `html=None` (engine/build.py render(), the
     `layout.preflight(W, H, elements, html=None, ...)` line) so invisible_craft_scan,
     wash_scan, double_rotation_scan, antipattern_scan and img_src_check NEVER run
     through render() no matter what you pass it -- despite CLAUDE.md sec7a listing
     several of them as "in preflight" with no caveat that preflight-via-render doesn't
     carry html. Per the brief ("use the full gate stack" / "pass gate config through
     render() rather than calling preflight separately"), this version keeps using
     render()'s built-in path for everything render CAN do, and calls the handful of
     plain layout.* functions that render() drops directly (not through a second
     preflight() call) to still get their coverage.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/g1_v2.py
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
ACCENT = core.accent_for("welfare")    # #1B8A5A mint -- department colour is semantic
INK = core.INK
PILL_FILL = "#D9CFAF"                  # a real second surface (measured dist 64.5 from --bg)
QUAL_COLOR = "#8B8880"                 # measured 5.59:1 on ink -- clears AA_NORMAL

WORDS = ["PATHER SATHI", "KOLKATA", "RETURN VISIT", "WELFARE", "AQUATERRA",
         "SUNDAY SCHOOL", "VOLUNTEERS", "WORKSHOP", "SATURDAYS"]
CALLOUT = "PATHER SATHI"               # the one partner -- gets the mint fill + ink dot


def clip(x, y, w, h):
    """Visible-on-canvas portion of a bbox that is allowed to bleed off-edge by design
    (the .p container is overflow:hidden). bounds_check/collision_check see the TRUE
    visible extent, not the full CSS box that intentionally continues past the frame."""
    x2, y2 = min(x + w, W), min(y + h, H)
    x0, y0 = max(x, 0), max(y, 0)
    return (x0, y0, max(0, x2 - x0), max(0, y2 - y0))


async def main():
    elements = []
    color_pairs = []
    text_pairs = []
    contains = []
    parts = []

    # ---------------------------------------------------------------- measure
    pill_font = dict(font="e", weight=700, size=24, transform="none")
    to_measure = [dict(text=w, **pill_font) for w in WORDS]
    to_measure += [
        dict(text="PATHER SATHI · KOLKATA", font="m", weight=700, size=17, letter_spacing="0.08em"),
        dict(text="126", font="d", weight=900, size=280),
        dict(text="RETURN VISITS", font="d", weight=900, size=46, letter_spacing="0.01em"),
        dict(text="counted across AquaTerra's welfare log, 2021–2026", font="m", weight=500, size=14),
        dict(text="@ngo.aquaterra", font="m", weight=700, size=13),
    ]
    m = await B.measure_text(to_measure, W, H)
    word_w = {WORDS[i]: m[i]["text_w"] for i in range(len(WORDS))}
    slab_eyebrow_m, num_m, sub_m, qual_m, footer_m = m[len(WORDS):]

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

    # ---------------------------------------------------------------- footer (measured, placed FIRST
    # so the pill field below can be sized to leave it honest clearance, not a guess)
    FOOTER_H = footer_m["ink_h"]
    footer_y = H - 52 - FOOTER_H
    footer_bottom = H - 52
    parts.append(
        f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
        f'font-size:13px;color:var(--ink);z-index:20">@ngo.aquaterra</span>'
    )
    elements.append(("footer", M, footer_y, footer_m["text_w"], FOOTER_H))

    # ---------------------------------------------------------------- pill field
    # Rows bleed off BOTH left and right edges (the mechanism named in the drawn
    # style's recipe) -- brick-offset row to row. Feed is much taller than the
    # style's 1.536:1 reference, so roughly double the row count rather than
    # stretching pill size -- but stop with REAL clearance above the footer,
    # not a guessed constant (that guess is exactly what broke v1).
    PILL_H = 58
    GAP_X = 16
    ROW_PITCH = 82
    row_top = 168
    FOOTER_CLEARANCE = 46
    row_bottom_limit = footer_y - FOOTER_CLEARANCE - PILL_H
    n_rows = 1 + max(0, (row_bottom_limit - row_top) // ROW_PITCH)

    pill_labels = []   # (label, x, y, w, h, word, is_callout, dotted)
    for r in range(n_rows):
        y = row_top + r * ROW_PITCH
        offset = -90 if r % 2 == 0 else -170
        x = offset
        wi = r % len(WORDS)
        col = 0
        while x < W + 140:
            word = WORDS[(wi + col) % len(WORDS)]
            pw = word_w[word] + 52
            label = f"pill_{r}_{col}"
            callout = word == CALLOUT
            dotted = (not callout) and (col % 3 == 0)
            pill_labels.append((label, x, y, pw, PILL_H, word, callout, dotted))
            x += pw + GAP_X
            col += 1

    for label, x, y, w, h, word, callout, dotted in pill_labels:
        fill = ACCENT if callout else PILL_FILL
        fg = core.text_on(ACCENT) if callout else INK
        dot = ""
        if callout:
            dot = (f'<span style="width:11px;height:11px;border-radius:50%;background:{INK};'
                   f'display:inline-block;margin-right:9px;flex:none"></span>')
        elif dotted:
            dot = (f'<span style="width:9px;height:9px;border-radius:50%;background:{ACCENT};'
                   f'display:inline-block;margin-right:8px;flex:none"></span>')
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
        if callout:
            text_pairs.append((label + "_text", fg, fill, 24, True))

    # ---------------------------------------------------------------- the ink slab (hero)
    SLAB_W, SLAB_H = 680, 430   # measured to the numeral's 514px width (was 860, a dead void)
    slab_x = (W - SLAB_W) / 2
    slab_y = 560
    ROT = -3
    slab_label = "slab"
    PAD = 56
    num_color = core.on_dark(ACCENT, 280)
    eyebrow_color = core.on_dark(ACCENT, 17)
    parts.append(
        f'<div style="position:absolute;top:{slab_y}px;left:{slab_x}px;width:{SLAB_W}px;height:{SLAB_H}px;'
        f'background:var(--ink);border-radius:32px;transform:rotate({ROT}deg);'
        f'box-shadow:{core.keyline(ring_bg="var(--bg)")}, {core.hard_shadow("xl")};z-index:15;'
        f'overflow:hidden">'
        # one hero-shine (CLAUDE.md sec9 craft layer) -- a soft diagonal highlight, low-alpha,
        # painted FIRST so every text div after it in DOM order sits on top and stays legible.
        f'<div style="position:absolute;inset:-20% -20%;'
        f'background:linear-gradient(120deg, rgba(255,255,255,.16) 0%, rgba(255,255,255,0) 42%);'
        f'pointer-events:none"></div>'
        f'<div style="position:absolute;top:44px;left:{PAD}px;font-family:var(--m);font-weight:700;'
        f'font-size:17px;letter-spacing:.08em;color:{eyebrow_color};text-transform:uppercase">'
        f'PATHER SATHI · KOLKATA</div>'
        f'<div style="position:absolute;top:76px;left:{PAD - 4}px;font-family:var(--d);font-weight:900;'
        f'font-size:280px;line-height:.78;color:{num_color}">126</div>'
        f'<div style="position:absolute;top:322px;left:{PAD}px;font-family:var(--d);font-weight:900;'
        f'font-size:46px;letter-spacing:.01em;color:var(--bg)">RETURN VISITS</div>'
        f'<div style="position:absolute;bottom:34px;left:{PAD}px;font-family:var(--m);font-weight:500;'
        f'font-size:14px;color:{QUAL_COLOR}">counted across AquaTerra’s welfare log, 2021–2026</div>'
        f'</div>'
    )
    rx, ry, rw, rh = lay.rotated_bbox(slab_x, slab_y, SLAB_W, SLAB_H, ROT)
    elements.append((slab_label, rx, ry, rw, rh))
    color_pairs.append((slab_label, "var(--ink)", "var(--bg)"))
    text_pairs.append(("slab_eyebrow", eyebrow_color, "var(--ink)", 17, True))
    text_pairs.append(("slab_numeral", num_color, "var(--ink)", 280, True))
    text_pairs.append(("slab_subhead", "var(--bg)", "var(--ink)", 46, True))
    text_pairs.append(("slab_qualifier", QUAL_COLOR, "var(--ink)", 14, True))

    # Content must fit the slab it is declared to sit inside (CLAUDE.md sec7a
    # contains_check, HARD FAIL). Un-rotated local coordinates: the slab establishes
    # its own containing block for these children, so their box IS relative to it.
    inner_w = SLAB_W - PAD - (PAD - 4)
    contains.append(("numeral_in_slab", (0, 0, num_m["ink_w"], num_m["ink_h"]), (0, 0, inner_w, SLAB_H)))
    contains.append(("subhead_in_slab", (0, 0, sub_m["ink_w"], sub_m["ink_h"]), (0, 0, inner_w, SLAB_H)))

    # Slab deliberately lies OVER the pill field (the drawn style's own recipe: "pin
    # one rotated ink slab over the field ... so it reads as laid over the pills").
    # Declare that as intentional for every pill it actually, geometrically touches --
    # not a blanket ignore of the whole collision class.
    collision_ignore = set()
    for label, x, y, w, h, word, callout, dotted in pill_labels:
        cx, cy, cw, ch = clip(x, y, w, h)
        if cw <= 0 or ch <= 0:
            continue
        ox = min(cx + cw, rx + rw) - max(cx, rx)
        oy = min(cy + ch, ry + rh) - max(cy, ry)
        if ox > 0 and oy > 0:
            collision_ignore.add(frozenset({label, slab_label}))

    inner = "".join(parts)
    html = B.page(W, H, "var(--bg)", inner, grain=True)

    # ---------------------------------------------------------------- the checks render()
    # does NOT run (its internal preflight call hardcodes html=None -- see docstring
    # above). Called directly, not via a second preflight(), per the brief.
    craft_issues = lay.invisible_craft_scan(html, "var(--bg)", core)
    wash_issues = lay.wash_scan(html, W, H)
    rot_issues = lay.double_rotation_scan(html)
    img_issues = lay.img_src_check(html)
    anti_issues = lay.antipattern_scan(html)
    for name_, issues in [("invisible_craft_scan", craft_issues), ("wash_scan", wash_issues),
                          ("double_rotation_scan", rot_issues), ("img_src_check", img_issues),
                          ("antipattern_scan", anti_issues)]:
        print(f"[manual-gate] {name_}: {'CLEAN' if not issues else issues}")

    os.makedirs("out/session10g", exist_ok=True)
    out_png = "out/session10g/g1_v4.png"
    async with B.session():
        await B.render(
            html, out_png, W, H,
            elements=elements,
            color_pairs=color_pairs,
            page_bg="var(--bg)",
            expect_hero=True,
            collision_ignore=collision_ignore,
            text_pairs=text_pairs,
            contains=contains,
        )
    print("done ->", out_png)


asyncio.run(main())
