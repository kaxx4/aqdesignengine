import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout"); sh = load("shapes")

W, H = core.SIZES["story"]          # 1080x1920 — story canvas, dark ground forced by brief
BG = "#0A0A0A"                       # ink page ground (dark)
OUTLINE = core.outline_of(BG)        # measured, not assumed -> "#F4EFE0" cream on this dark field
SHADOW = core.hard_shadow("lg", OUTLINE)

GRAPE  = core.accent_for("content")  # #7E5BFF -- department colour is semantic (content=grape), not a pick
TOMATO = core.ACCENTS[3]
LEMON  = core.ACCENTS[2]

# text colours: MEASURED per surface, never eyeballed
TXT_ON_GRAPE  = core.text_on(GRAPE)
TXT_ON_TOMATO = core.text_on(TOMATO)
TXT_ON_LEMON  = core.text_on(LEMON)
TXT_ON_BG     = core.text_on(BG)     # what wins directly on the ink page ground

elements = []   # (label, x, y, w, h) -- kept IN SYNC with every div drawn
color_pairs = []  # (label, fill, surface) for invisible_color_check
text_pairs = []   # (label, text_colour, surface_colour, size, bold) for text_contrast_check

# ---------------------------------------------------------------------------
# CARD FAN — mechanism drawn from STYLE 620d62f101b97c (design.py, --dept content
# --canvas story --ground dark --seed 14): a diagonal fan of 4 overlapping cards
# on black, pinned by one badge at a seam. Measured off compare.geometry(ref):
# coverage 0.568, centroid (0.508,0.501), margins L4/R4/T9/B3 pct -- built to those.
# ---------------------------------------------------------------------------
CARD_A = dict(x=64,  y=210, w=580, h=560)   # headline / hero stat -- grape, frontmost
CARD_B = dict(x=560, y=330, w=420, h=480)   # accent stat -- tomato, behind+right of A
CARD_C = dict(x=64,  y=650, w=500, h=560)   # photo 1 -- Sundarban education photo
CARD_D = dict(x=496, y=730, w=500, h=580)   # photo 2 -- food distribution photo

elements += [
    ("cardA", CARD_A["x"], CARD_A["y"], CARD_A["w"], CARD_A["h"]),
    ("cardB", CARD_B["x"], CARD_B["y"], CARD_B["w"], CARD_B["h"]),
    ("cardC", CARD_C["x"], CARD_C["y"], CARD_C["w"], CARD_C["h"]),
    ("cardD", CARD_D["x"], CARD_D["y"], CARD_D["w"], CARD_D["h"]),
]
color_pairs += [
    ("cardA_fill", GRAPE, BG),
    ("cardB_fill", TOMATO, BG),
]

# the whole fan is one intentional cascade group -- back to front: D, B, C, A
CASCADE = [ (CARD_D["x"],CARD_D["y"],CARD_D["w"],CARD_D["h"]),
            (CARD_B["x"],CARD_B["y"],CARD_B["w"],CARD_B["h"]),
            (CARD_C["x"],CARD_C["y"],CARD_C["w"],CARD_C["h"]),
            (CARD_A["x"],CARD_A["y"],CARD_A["w"],CARD_A["h"]) ]

# every pair of cards is a DECLARED, by-design overlap -- both the tuple-level
# collision_check AND the DOM-level audit.audit() key off THESE SAME LABEL
# STRINGS (audit tags each div data-tag=<label>), so one ignore set covers both.
IGNORE = {
    frozenset({"cardA","cardB"}), frozenset({"cardA","cardC"}),
    frozenset({"cardB","cardD"}), frozenset({"cardC","cardD"}),
    frozenset({"cardA","cardD"}),
    frozenset({"cardA","badge"}), frozenset({"cardB","badge"}),
    frozenset({"cardC","chip"}), frozenset({"cardD","chip"}),
    frozenset({"cardB","num558"}),   # num558 sits fully inside cardA, which laps
                                      # 84px into cardB's own bbox by design -- A is
                                      # drawn on top there, so nothing is actually hidden
}

def card_div(tag, spec, z, inner, extra=""):
    return (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{spec["x"]}px;'
            f'top:{spec["y"]}px;width:{spec["w"]}px;height:{spec["h"]}px;z-index:{z};'
            f'border:4px solid {OUTLINE};box-shadow:{SHADOW};border-radius:{core.RADII["inner"]}px;'
            f'overflow:hidden;{extra}">{inner}</div>')

async def build():
    global elements, color_pairs, text_pairs
    # ---- measure every string BEFORE sizing anything around it ----
    items = [
        dict(text="558", font="d", size=250, weight=900, letter_spacing="-4px"),
        dict(text="WELFARE PROJECTS", font="d", size=44, weight=900, max_width=520),
        dict(text="logged since 2021", font="e", size=24, weight=600),
        dict(text="291", font="d", size=110, weight=900),
        dict(text="WORKSHOPS RUN", font="d", size=26, weight=900, max_width=260),
        dict(text="same span", font="e", size=19, weight=600),
        dict(text="126 return visits, one partner", font="e", size=22, weight=600, max_width=420),
        dict(text="COME SEE ONE", font="d", size=34, weight=900),
        dict(text="no pitch, promise", font="e", size=20, weight=600),
        dict(text="COUNTED", font="d", size=13, weight=800),   # box units, measured at 13px for fit_font
    ]
    M = await B.measure_text(items, W, H)
    (m558, mWELFARE, mlogged, m291, mWORK, msame, mchip, mCTA1, mCTA2, mCOUNTED) = M

    # ---- CARD A: hero numeral ----
    numA_h = m558["glyph_h"]; numA_w = m558["glyph_w"]
    a_inner = (
        f'<div style="position:absolute;left:32px;top:26px;font-family:var(--m);font-weight:700;'
        f'font-size:15px;letter-spacing:.12em;color:{TXT_ON_GRAPE};opacity:.72">FIELD LOG · COUNTED</div>'
        f'<div style="position:absolute;left:24px;top:{92}px;font-family:var(--d);font-weight:900;'
        f'font-size:250px;line-height:.78;letter-spacing:-4px;color:{TXT_ON_GRAPE}">558</div>'
        f'<div style="position:absolute;left:32px;top:{92+m558["h"]+6}px;width:520px;font-family:var(--d);'
        f'font-weight:900;font-size:44px;line-height:1.02;letter-spacing:.01em;color:{TXT_ON_GRAPE}">WELFARE PROJECTS</div>'
        f'<div style="position:absolute;left:32px;top:{92+m558["h"]+6+mWELFARE["h"]+10}px;font-family:var(--e);'
        f'font-weight:600;font-size:24px;color:{TXT_ON_GRAPE}">logged since 2021</div>'
    )
    # padded +8%: measure_text's canvas glyph metric ignores CSS letter-spacing/
    # line-height, so the DOM box reconcile.measure_dom sees runs a bit larger
    # than the pure glyph measurement -- pad rather than chase an exact match.
    elements.append(("num558", CARD_A["x"]+24, CARD_A["y"]+92, int(numA_w*1.08), int(numA_h*1.2)))
    text_pairs += [
        ("num558", TXT_ON_GRAPE, GRAPE, 250, True),
        ("WELFARE_PROJECTS", TXT_ON_GRAPE, GRAPE, 44, True),
        ("logged_since_2021", TXT_ON_GRAPE, GRAPE, 24, True),
    ]
    # contains: does the hero numeral + headline block actually fit inside card A?
    block_bottom = 92 + m558["h"] + 6 + mWELFARE["h"] + 10 + mlogged["h"]
    contains_pairs = [
        ("num558_in_cardA", (CARD_A["x"]+24, CARD_A["y"]+92, numA_w, numA_h),
         (CARD_A["x"], CARD_A["y"], CARD_A["w"], CARD_A["h"])),
        ("headline_block_in_cardA", (CARD_A["x"]+24, CARD_A["y"], 520, block_bottom+16),
         (CARD_A["x"], CARD_A["y"], CARD_A["w"], CARD_A["h"])),
    ]

    # ---- CARD B: secondary counted stat ----
    # cardA overlaps cardB's own left ~84px by design (the fan) -- content must
    # clear that zone, so B's inner padding starts well past it, not at B's own edge.
    BPAD = 128
    b_inner = (
        f'<div style="position:absolute;left:{BPAD}px;top:{28}px;font-family:var(--d);font-weight:900;'
        f'font-size:110px;line-height:.8;color:{TXT_ON_TOMATO}">291</div>'
        f'<div style="position:absolute;left:{BPAD}px;top:{28+m291["h"]+4}px;width:260px;font-family:var(--d);'
        f'font-weight:900;font-size:26px;line-height:1.05;color:{TXT_ON_TOMATO}">WORKSHOPS RUN</div>'
        f'<div style="position:absolute;left:{BPAD}px;top:{28+m291["h"]+4+mWORK["h"]+8}px;font-family:var(--e);'
        f'font-weight:600;font-size:19px;color:{TXT_ON_TOMATO}">same span</div>'
    )
    elements.append(("num291", CARD_B["x"]+BPAD, CARD_B["y"]+28, int(m291["glyph_w"]*1.08), int(m291["glyph_h"]*1.2)))
    text_pairs += [
        ("num291", TXT_ON_TOMATO, TOMATO, 110, True),
        ("WORKSHOPS_RUN", TXT_ON_TOMATO, TOMATO, 26, True),
        ("same_span", TXT_ON_TOMATO, TOMATO, 19, True),
    ]
    b_block_bottom = 28 + m291["h"] + 4 + mWORK["h"] + 8 + msame["h"]
    contains_pairs.append(
        ("stat_block_in_cardB", (CARD_B["x"]+BPAD, CARD_B["y"]+28, 260, b_block_bottom-28+16),
         (CARD_B["x"], CARD_B["y"], CARD_B["w"], CARD_B["h"])))

    # ---- CARD C / D: real AQ photos, tinted, cropped to feature faces not the
    # baked-in caption text each source jpeg already carries (real-assets-only rule) ----
    c_inner = (f'<img src="{core.PHOTOS["edu"]}" style="width:100%;height:100%;object-fit:cover;'
               f'object-position:50% 30%;filter:saturate(.9) contrast(1.08)">'
               f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,0) 55%,rgba(10,10,10,.75) 100%)"></div>')
    d_inner = (f'<img src="{core.PHOTOS["food"]}" style="width:100%;height:100%;object-fit:cover;'
               f'object-position:50% 22%;filter:saturate(.9) contrast(1.08)">'
               f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,0) 55%,rgba(10,10,10,.75) 100%)"></div>')

    # chip pinned at the bottom of the photo card (like the reference's "CLASSY NIGHTSS"
    # chip) -- carries the THIRD counted figure. Sits half on the photo, half below its
    # edge, so it is declared as an independent element (cardC/chip ignore pair above).
    chip_w, chip_h = mchip["ink_w"] + 40, mchip["h"] + 28
    chip_x, chip_y = CARD_C["x"] + 26, CARD_C["y"] + CARD_C["h"] - 34
    chip = (f'<div class="measure" data-tag="chip" style="position:absolute;left:{chip_x}px;top:{chip_y}px;'
            f'width:{chip_w}px;height:{chip_h}px;background:{LEMON};border:3px solid {OUTLINE};'
            f'box-shadow:{SHADOW};border-radius:999px;z-index:9;display:flex;align-items:center;'
            f'justify-content:center;font-family:var(--e);font-weight:600;font-size:22px;'
            f'color:{TXT_ON_LEMON};padding:0 20px;white-space:nowrap">126 return visits, one partner</div>')
    elements.append(("chip", chip_x, chip_y, chip_w, chip_h))
    color_pairs.append(("chip_fill", LEMON, BG))
    text_pairs.append(("chip_text", TXT_ON_LEMON, LEMON, 22, True))

    # ---- badge: scalloped sticker pinned at the A/B seam ----
    badge_size = 160
    badge_x, badge_y = CARD_A["x"]+CARD_A["w"]-56, CARD_A["y"]-20
    label_box, fits_counted = sh.fit_font(mCOUNTED["ink_w"], 13, "scallop", badge_size)
    if not fits_counted:
        print("!! badge label 'COUNTED' does not fit at this scallop size -- shorten or grow badge")
    badge_svg = sh.sticker(sh.scallop(lobes=12, r=42), fill=LEMON, size=badge_size,
                           outline=OUTLINE, shadow=True,
                           inner=sh.label("COUNTED", size=label_box, y=56, fill=TXT_ON_LEMON, weight=800))
    badge = (f'<div class="measure" data-tag="badge" style="position:absolute;left:{badge_x}px;'
             f'top:{badge_y}px;width:{badge_size}px;height:{badge_size}px;z-index:10">{badge_svg}</div>')
    elements.append(("badge", badge_x, badge_y, badge_size, badge_size))
    color_pairs.append(("badge_fill", LEMON, BG))

    # ---- floating doodle in the free gap under the fan ----
    dood_size = 108
    dood_x, dood_y = 150, 1340
    dood_col = core.on_dark(core.ACCENTS[0], 108, True)   # pink, checked against ink
    doodle = (f'<div class="measure" data-tag="doodle" style="position:absolute;left:{dood_x}px;'
              f'top:{dood_y}px;width:{dood_size}px;height:{dood_size}px;z-index:9">'
              f'{dd.stamp("heart", dood_col, rot=-8)}</div>')
    elements.append(("doodle", dood_x, dood_y, dood_size, dood_size))

    # ---- ellipse callout near the bottom (soft CTA, no urgency, real closure) ----
    ell_w, ell_h = 820, 210
    ell_x, ell_y = (W-ell_w)//2, 1460
    ellipse = (f'<div class="measure" data-tag="ellipse" style="position:absolute;left:{ell_x}px;'
               f'top:{ell_y}px;width:{ell_w}px;height:{ell_h}px;border-radius:50%;background:{GRAPE};'
               f'border:4px solid {OUTLINE};box-shadow:{SHADOW};z-index:9;display:flex;'
               f'flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px">'
               f'<div style="font-family:var(--d);font-weight:900;font-size:34px;color:{TXT_ON_GRAPE}">COME SEE ONE</div>'
               f'<div style="font-family:var(--e);font-weight:600;font-size:20px;color:{TXT_ON_GRAPE}">no pitch, promise</div>'
               f'</div>')
    elements.append(("ellipse", ell_x, ell_y, ell_w, ell_h))
    color_pairs.append(("ellipse_fill", GRAPE, BG))
    text_pairs += [("cta1", TXT_ON_GRAPE, GRAPE, 34, True), ("cta2", TXT_ON_GRAPE, GRAPE, 20, True)]

    # ---- header: logo pill (top-left, per CLAUDE.md sec.9 -- pill on dark ground) ----
    logo_pill = (f'<div class="measure" data-tag="logo" style="position:absolute;left:64px;top:56px;'
                 f'background:{core.CREAM};border-radius:999px;padding:10px 18px;z-index:20;'
                 f'display:flex;align-items:center"><img src="{core.LOGO}" style="height:26px;display:block"></div>')
    elements.append(("logo", 64, 56, 160, 46))
    kicker = (f'<div class="measure" data-tag="kicker" style="position:absolute;right:64px;top:66px;'
              f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.12em;'
              f'text-transform:uppercase;color:{LEMON};z-index:20">field log · kolkata</div>')
    elements.append(("kicker", W-64-260, 66, 260, 24))
    text_pairs.append(("kicker_text", core.on_dark(LEMON, 16), BG, 16, True))

    # ---- footer ----
    foot1 = (f'<div class="measure" data-tag="foot" style="position:absolute;left:64px;bottom:96px;'
             f'font-family:var(--m);font-weight:700;font-size:14px;letter-spacing:.08em;'
             f'text-transform:uppercase;color:#B9B4A6;z-index:20">student-run, kolkata-based</div>')
    elements.append(("foot1", 64, H-96-16, 400, 18))
    foot2 = (f'<span class="measure" data-tag="cta" style="position:absolute;bottom:{56}px;left:64px;'
             f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.08em;'
             f'color:{TXT_ON_BG};z-index:20">@ngo.aquaterra field notes</span>')
    elements.append(("foot2", 64, H-56-18, 320, 18))
    text_pairs.append(("foot2_text", TXT_ON_BG, BG, 15, True))

    inner = "".join([
        card_div("cardD", CARD_D, 6, d_inner),
        card_div("cardB", CARD_B, 7, b_inner, extra=f"background:{TOMATO}"),
        card_div("cardC", CARD_C, 8, c_inner),
        chip,
        card_div("cardA", CARD_A, 9, a_inner, extra=f"background:{GRAPE}"),
        badge, doodle, ellipse,
        logo_pill, kicker, foot1, foot2,
    ])
    html = B.page(W, H, BG, inner, grain=True)

    slug = "g4_558_welfare"
    outdir = f"out/session10g"
    os.makedirs(outdir, exist_ok=True)
    async with B.session():
        issues = await B.render(html, f"{outdir}/g4_v2.png", W, H,
                                elements=elements, color_pairs=color_pairs, page_bg=BG,
                                expect_hero=True, collision_ignore=IGNORE,
                                text_pairs=text_pairs, cascade_stacks=[CASCADE],
                                contains=contains_pairs, containers=["cardA","cardB"])
    print("RENDER ISSUES:", issues)

asyncio.run(build())
