"""Workflow B recreation — reference f25de42e61b5c9a4e34e7745cd556090.jpg, SCREEN 4 ONLY
("£5 off your groceries" promo-code modal, the 4th of 4 phone mockups in the reference).

Composition description (written before any code, per CLAUDE.md §5 step 1):
  - Full-bleed pastel green field (the whole "screen" is one flat colour, no cream visible).
  - Top-right: a small ink "X" close icon.
  - Center: the dominant hero graphic — a large ink-outlined rectangle/frame (transparent,
    background shows through) housing the headline+subhead, OVERLAPPED on its right side by
    a large SOLID ink "A-frame sign leg" wedge shape that splays into two feet near the bottom
    (a sandwich-board-sign silhouette). This is the single largest, dominant element.
  - Inside the outline frame: giant headline ("£5"), bold ink, top-left of the frame.
  - Below the headline, inside the same frame: a 2-line bold subhead ("off your" / "groceries").
  - Below the whole sign group, centered, same column width: a small mono label
    ("Use promo code:").
  - Below that: a white rounded box with the promo code, bold, centered ("WZY2021").
  - Below that: a pale-pink rounded box, same width, "Copy code" bold centered (a CTA).
  - Below that: 3 lines of small centered fine print (terms).
  - No logo/nav visible (it's an in-app modal) — per established precedent (sample "yearbook
    rework" style pieces with no source logo), we ADD the AQ logo top-left and the
    @ngo.aquaterra footer handle anyway, since AQ branding is standing-on for every poster
    regardless of what the reference had.

Acceptable adaptations (per §5 step 4):
  - Literal "weezy" grocery-delivery copy -> AQ referral-code mechanic for a real AQ
    program (Shikshaq), since AQ is an NGO, not a grocery app — content swap, same mechanism.
  - Reference's saturated pastel green (~#A8D5A2, not an AQ token) -> shapes.lighten(AQ mint,
    0.55), i.e. a tint DERIVED from the brand's own mint accent, so the field is on-brand
    while visually reading the same family of colour as the reference.
  - Exact A-frame silhouette (a slightly perspective double-sign) -> simplified to one outline
    rectangle + one solid wedge-with-feet — the "giant sign housing type, overlapped by a solid
    dark accent shape" mechanism is preserved; the exact perspective doubling is not.

NOTE ON BRAND RULES IN TENSION: core.py's ACCENTS are meant to "punctuate ~30% of the piece,
never flood the field" (CLAUDE.md §9), but this reference's flat pastel field covers ~100% of
the canvas. This is not a bug in the recreation - the WHOLE MECHANISM being recreated is a
flooded-color app screen - so preview.critique's flat_dominant flag is EXPECTED to fire here,
the same way giant_type's dark base is a declared exemption in ARCHETYPE_PROFILES. There is no
per-archetype exemption mechanism available to a bespoke Workflow B script (that's an
engine.py/ARCHETYPE_PROFILES concept, engine.py is explicitly off-limits for Workflow B), so
this is flagged in the run output and accepted by eye rather than suppressed.
"""
import asyncio, os, sys, importlib.util

# CLAUDE.md's own bespoke-script template hardcodes
# C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE, which does not exist on this
# machine (the repo actually lives at C:\Users\kanis\Desktop\Code\AquaTerra\AQ_CODEBASE - see
# report). Using the same self-locating chdir already adopted by newer scripts in scratchpad/
# (e.g. gen_motifs_v6.py) instead of copy-pasting the stale absolute path from the manual.
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = load("core")
B = load("build")
dd = load("doodles")
lay = load("layout")
sh = load("shapes")

W, H = core.SIZES["feed"]
M = 64
A = core.ACCENTS  # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
INK = core.INK

elements = []  # (label, x, y, w, h) kept IN SYNC with every element's real CSS box


def snap(v):
    return round(v / 8) * 8


# ---------------------------------------------------------------------------
# the "sandwich-board A-frame sign" silhouette: wide flat top, straight sides
# down to a bottom notch that splits it into two feet with a gap between them.
# Returns an SVG path `d` string in the element's own 0..w x 0..h box.
# ---------------------------------------------------------------------------
def sign_leg_path(w, h, top_in=0.14, notch_y=0.78, foot_in=0.24):
    top_l, top_r = top_in * w, (1 - top_in) * w
    foot_l, foot_r = foot_in * w, (1 - foot_in) * w
    notch_l, notch_r = (foot_in + 0.08) * w, (1 - foot_in - 0.08) * w
    ny = notch_y * h
    pts = [(top_l, 0), (top_r, 0), (w, h), (foot_r, h), (notch_r, ny),
           (notch_l, ny), (foot_l, h), (0, h)]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"


def svg_shape(path_d, w, h, fill="none", stroke="none", sw=0):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg"><path d="{path_d}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/></svg>')


async def main():
    # -- measure the two real headline strings first (never guess text geometry) --
    HERO_TXT = "AQ"
    SUB_L1, SUB_L2 = "unlock a", "free seat"
    sign_x, sign_w = 110, 520          # outline sign frame
    pad = 40
    text_max_w = sign_w - 2 * pad      # 440, kept clear of the leg — see v1->v2 note below

    # NOTE (found the hard way): passing max_width here does NOT give you the true
    # painted text width back as ink_w when the string is a single unbreakable
    # "word" (no space) narrower than that box — a block div's getBoundingClientRect
    # is the CSS box you gave it, so ink_w = max(box_width, scrollWidth) just
    # reports the box back (440px) rather than "AQ"'s real ~340px of ink. That
    # silently made hero's collision bbox 100px too wide against sign_leg. Omitting
    # max_width measures with white-space:nowrap instead, which is the box's TRUE
    # natural size — the right call for a short hero word that must never wrap.
    sizes = await B.measure_text([
        dict(text=HERO_TXT, font="d", size=280, weight=900, line_height=0.82,
             transform="uppercase"),
        dict(text=SUB_L1, font="e", size=58, weight=600, line_height=1.0),
        dict(text=SUB_L2, font="e", size=58, weight=600, line_height=1.0),
    ], W, H)
    hero_m, l1_m, l2_m = sizes

    bg_field = sh.lighten(A[1], 0.55)  # pastel tint OF the brand mint, not a foreign colour
    outline_col = INK
    cta_bg = sh.lighten(A[0], 0.68)    # pale pink tint of the brand pink, for the CTA plate

    # ---- logo (top-left, standing brand rule; reference had none, we keep our own) ----
    logo_html = B.logo(dark=False, x=M, y=52)
    elements.append(("logo", M, 52, 170, 32))

    # ---- close X (top-right) ----
    x_size = 56
    x_x, x_y = W - M - x_size, 48
    close_html = (f'<div class="measure" data-tag="closex" style="position:absolute;'
                  f'top:{x_y}px;left:{x_x}px;width:{x_size}px;height:{x_size}px;z-index:20">'
                  f'{dd.stamp("cross", INK, rot=0)}</div>')
    elements.append(("closex", x_x, x_y, x_size, x_size))

    # ---- the hero sign group ----
    # v1->v2: sign_outline's bottom (910) reached past the leg's notch start (~794),
    # so the outline's border traced a stray floating rectangle INSIDE the leg's
    # bottom gap where the leg's fill is cut away (visible in B_v2.png, bottom-right
    # of the sign). Keeping the outline's bottom well above the notch means the only
    # place the two shapes overlap is the leg's SOLID upper trapezoid, where an ink
    # border on an ink fill is simply invisible, as intended.
    sign_y, sign_h = 260, 500
    outline_html = (f'<div class="measure" data-tag="sign_outline" style="position:absolute;'
                    f'top:{sign_y}px;left:{sign_x}px;width:{sign_w}px;height:{sign_h}px;'
                    f'border:5px solid {outline_col};box-sizing:border-box;z-index:6"></div>')
    elements.append(("sign_outline", sign_x, sign_y, sign_w, sign_h))

    # v1->v2: shifted 40px right so the headline's glyphs (measured ink_w, not the
    # wider layout box) clear the leg's own sloped left edge instead of the "Q"
    # tail vanishing into the black shape (B_v2.png).
    leg_x, leg_y, leg_w, leg_h = 560, 232, 440, 720
    leg_path = sign_leg_path(leg_w, leg_h)
    leg_html = (f'<div class="measure" data-tag="sign_leg" style="position:absolute;'
                f'top:{leg_y}px;left:{leg_x}px;width:{leg_w}px;height:{leg_h}px;z-index:5">'
                f'{svg_shape(leg_path, leg_w, leg_h, fill=outline_col)}</div>')
    elements.append(("sign_leg", leg_x, leg_y, leg_w, leg_h))

    # headline "AQ" — top-left inside the outline frame. white-space:nowrap so the
    # rendered box matches the nowrap measurement above exactly (no forced width).
    hero_x, hero_y = sign_x + pad, sign_y + 46
    hero_html = (f'<div class="measure" data-tag="hero" style="position:absolute;'
                 f'top:{hero_y}px;left:{hero_x}px;white-space:nowrap;'
                 f'font-family:var(--d);font-weight:900;font-size:280px;line-height:.82;'
                 f'text-transform:uppercase;color:{INK};z-index:8">{HERO_TXT}</div>')
    elements.append(("hero", hero_x, hero_y, hero_m["ink_w"], hero_m["ink_h"]))

    # sub flows off hero's LAYOUT box (`h`) per measure_text's own guidance, but hero's
    # COLLISION box (above) intentionally uses the bigger `ink_h` as a safety margin —
    # "AQ" has no descenders so ink_h (294) overstates its real footprint (h=230) by
    # 64px. Rather than quietly shrinking that safety margin back down (defeating the
    # reason ink_h exists), close the gap by flowing off ink_h too: honest, if a little
    # more open than the reference's tighter spacing.
    sub_x = sign_x + pad
    sub_y = hero_y + hero_m["ink_h"] + 8
    sub_html = (f'<div class="measure" data-tag="sub" style="position:absolute;top:{sub_y}px;'
                f'left:{sub_x}px;white-space:nowrap;font-family:var(--e);font-weight:600;'
                f'font-size:58px;line-height:1.05;color:{INK};z-index:8">{SUB_L1}<br>{SUB_L2}</div>')
    sub_h = l1_m["h"] + l2_m["h"]
    elements.append(("sub", sub_x, sub_y, max(l1_m["ink_w"], l2_m["ink_w"]), sub_h))

    # ---- promo block, centered under the sign group, shared column ----
    # v1->v2: widened/re-centered to span the full sign+leg group (110-1000) instead
    # of just the outline's width, and the whole vertical stack was compressed —
    # v1's fine print ended at y~1300 while the footer (bottom:56px fixed by
    # build.cta) starts at H-56-20=1274, an overlap the preflight collision check
    # already caught as ('fine','footer',344,20) but v1 shipped without reading it.
    col_x, col_w = 110, 890

    label_y = 970
    label_html = (f'<div class="measure" data-tag="lbl" style="position:absolute;top:{label_y}px;'
                  f'left:{col_x}px;width:{col_w}px;text-align:center;font-family:var(--m);'
                  f'font-weight:700;font-size:22px;letter-spacing:.04em;color:{INK};z-index:9">'
                  f'Use referral code:</div>')
    elements.append(("lbl", col_x, label_y, col_w, 28))

    code_y, code_h = 1010, 72
    code_html = (f'<div class="measure" data-tag="codebox" style="position:absolute;'
                 f'top:{code_y}px;left:{col_x}px;width:{col_w}px;height:{code_h}px;'
                 f'background:#FFFFFF;border:4px solid {INK};box-shadow:{core.hard_shadow("base")};'
                 f'display:flex;align-items:center;justify-content:center;z-index:9">'
                 f'<span style="font-family:var(--m);font-weight:700;font-size:30px;'
                 f'letter-spacing:.06em;color:{INK}">AQFRIEND</span></div>')
    elements.append(("codebox", col_x, code_y, col_w, code_h))

    cta_y, cta_h = code_y + code_h + 14, 72
    cta_html = (f'<div class="measure" data-tag="cta" style="position:absolute;top:{cta_y}px;'
                f'left:{col_x}px;width:{col_w}px;height:{cta_h}px;background:{cta_bg};'
                f'border:4px solid {INK};display:flex;align-items:center;justify-content:center;'
                f'z-index:9"><span style="font-family:var(--e);font-weight:600;font-size:26px;'
                f'color:{INK}">copy code</span></div>')
    elements.append(("cta", col_x, cta_y, col_w, cta_h))

    fine_y = cta_y + cta_h + 26
    fine_html = (f'<div class="measure" data-tag="fine" style="position:absolute;top:{fine_y}px;'
                 f'left:{col_x}px;width:{col_w}px;text-align:center;font-family:var(--e);'
                 f'font-weight:400;font-size:19px;line-height:1.4;color:var(--ink3);z-index:9">'
                 f'Share your code with a friend to open a seat<br>in an upcoming aquaterra '
                 f'workshop.</div>')
    elements.append(("fine", col_x, fine_y, col_w, 54))

    footer_html = B.cta("· recreation training run")
    elements.append(("footer", M, H - 70, 420, 20))

    inner = "".join([
        f'<div style="position:absolute;inset:0;background:{bg_field}"></div>',
        logo_html, close_html, outline_html, leg_html, hero_html, sub_html,
        label_html, code_html, cta_html, fine_html, footer_html,
    ])
    html = B.page(W, H, bg_field, inner, grain=False)

    # v1->v2: dropped the ("field", bg_field, bg_field) pair — that was comparing the
    # page background to itself, which invisible_color_check correctly (if uselessly)
    # flagged as a 0-delta "invisible" match every time. color_pairs is for ELEMENTS
    # sitting ON the page bg, not the bg itself.
    color_pairs = [
        ("sign_leg", outline_col, bg_field),
        ("hero_text", INK, bg_field),
        ("codebox", "#FFFFFF", bg_field),
        ("cta", cta_bg, bg_field),
    ]

    # v1->v2: sign_outline/hero/sub overlapping sign_outline/sign_leg are BY DESIGN
    # (the frame houses the headline; the frame and the leg are meant to overlap the
    # way the reference's two sign layers do) — ignored the same way audit.py's own
    # SKIP_PAIRS ignores "sign x sign". Any OTHER collision still fails clean.
    # NOTE (found the hard way): collision_check's ignore_pairs must be a set of
    # frozenset({label_a, label_b}) — an ORDERED tuple like ("sign_outline","sign_leg")
    # never matches (frozenset({a,b}) == a 2-tuple is always False) and fails SILENTLY,
    # no error, the collision just keeps reporting. layout.preflight's own docstring
    # doesn't restate this; only collision_check's docstring several hundred lines
    # away spells out the required shape.
    ignore = {
        frozenset({"sign_outline", "sign_leg"}),
        frozenset({"sign_outline", "hero"}),
        frozenset({"sign_outline", "sub"}),
    }
    pf = lay.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                       page_bg=bg_field, core=core, expect_hero=True,
                       collision_ignore=ignore)

    out_dir = "out/sonnet_test"
    os.makedirs(out_dir, exist_ok=True)
    out_png = os.path.join(out_dir, "B_v2.png")
    await B.render(html, out_png, W, H, elements=[e[1:] for e in elements],
                   color_pairs=color_pairs, page_bg=bg_field, expect_hero=True)
    print("done ->", out_png)
    return pf


if __name__ == "__main__":
    asyncio.run(main())
