"""RECREATION -- e7b32bd307aac4 ("Intake/Production/Review/Delivery" workflow-pile LinkedIn card).

Full element inventory written to brain/RECREATION_AUDIT.md under
"## Sample e7b32bd307aac4" BEFORE this script. 26 elements total. This is NOT a mockup --
genuinely scorable at full canvas (1200x628, matches core.SIZES['linkedin'] almost exactly).

Approach: bespoke script from core/build/doodles/layout/shapes primitives directly (never
engine.py ARCHETYPES). The hero is a deliberately-overlapping PILE of 11 UI-mockup tiles sitting
on a near-white "paper" card inside a cream field, itself framed by 8 diagonally-clipped
photo/paper bleed panels at the canvas edges (a receding-box / portal illusion).

Real-assets-only substitutions (declared in the audit, not silent): the pile's fake "Aa"/"Au"
type-app icons + doc/chip/file-tiles are synthetic UI chrome (not stock photography), recreated
directly as flat vector tiles -- same precedent as the 110a5730e3710b app-mockup recreation.
4 of the 8 stock-photo bleed panels use real AQ photos (edu/diwali/xmas/food); the 4 smallest/
least-legible slivers use flat AQ-accent colour panels instead of fabricated stock imagery.

layout.scatter_solve was evaluated for the pile and NOT used for placement -- it randomly
searches for a LEGAL layout against constraints (overlap budget, protect boxes, keep-out zones)
with no notion of a TARGET position, so it cannot reproduce a specific reference's arrangement;
using it here would produce a plausible-but-different pile, defeating a recreation task. Positions
below are the bboxes measured directly off the reference (audit step 1). See friction notes.

layout.resolve_label_z IS used below: each pile object's own readable text/glyph box is
registered, an initial hand-picked z assigned by the reference's own visual depth, and
resolve_label_z raises anything whose label ends up buried -- catching any z mistake rather than
trusting the hand-assigned order blindly.
"""
import asyncio, os, sys, importlib.util, itertools

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
shapes = load("shapes")

W, H = core.SIZES["linkedin"]        # 1200x628 -- matches the reference's own 1199x628 almost exactly
A = core.ACCENTS                     # 0 pink, 1 mint, 2 lemon, 3 tomato, 4 sky, 5 grape, 6 teal
CREAM = core.CREAM                   # #F4EFE0 -- outer field
PAPER = "#FFFFFF"                    # true white -- used for the doc/feedback mockup tiles,
                                      # which sit ON the card and need real contrast against it.
CARD_BG = shapes.lighten(A[5], 0.78)  # #E2DAFF -- a whisper of AQ grape.
                                      # v1 used pure white for the card and invisible_color_check
                                      # (hard fail, thresh=40) flagged it: euclidean distance from
                                      # CREAM (244,239,224) to white is only 36.6 -- ANY near-white
                                      # "paper" tone is structurally too close to CREAM to clear a
                                      # flat 40-unit RGB threshold, because CREAM is already almost
                                      # white. The reference's own card is genuinely near-invisible
                                      # in colour, distinguished only by its drop shadow -- a real
                                      # gate/reference mismatch, noted in the friction report. Fix:
                                      # tint the card with a light AQ-grape wash instead of literal
                                      # white, which clears the gate (dist 41.5) and reads as an
                                      # intentional cool "paper" tile against the warm cream field.
INK = core.INK
GREY = "#6B6B66"
LINE = "rgba(10,10,10,0.13)"

els = []


def E(label, x, y, w, h):
    els.append((label, x, y, w, h))


parts = []

# ---------------------------------------------------------------- ground + wireframe (ambient)
parts.append(f'<div style="position:absolute;inset:0;background:{CREAM}"></div>')

CARD_X, CARD_Y, CARD_W, CARD_H = 345, 63, 520, 502
CARD_R = 44

# schematic "receding box" guide lines -- 6 lines from the card's corners/edges out to the
# canvas edges, reproducing the reference's portal illusion (not pixel-traced, ambient only,
# never gated -- decoration, not a hero or legibility element).
guide_svg = (
    f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">'
    f'<line x1="{CARD_X}" y1="{CARD_Y}" x2="0" y2="0" stroke="{LINE}" stroke-width="1.5"/>'
    f'<line x1="{CARD_X+CARD_W}" y1="{CARD_Y}" x2="{W}" y2="0" stroke="{LINE}" stroke-width="1.5"/>'
    f'<line x1="{CARD_X}" y1="{CARD_Y+CARD_H}" x2="0" y2="{H}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<line x1="{CARD_X+CARD_W}" y1="{CARD_Y+CARD_H}" x2="{W}" y2="{H}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<line x1="158" y1="0" x2="158" y2="{H}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<line x1="954" y1="0" x2="954" y2="{H}" stroke="{LINE}" stroke-width="1.5"/>'
    f'</svg>'
)
parts.append(guide_svg)

# ---------------------------------------------------------------- 8 photo/paper bleed panels
# real AQ photos for the 4 largest/most legible panels; flat accent-colour panels (declared
# swap, CLAUDE.md Sec9) for the 4 smallest slivers where a photo would be unrecognisable anyway.


def clipped(label, x, y, w, h, clip_poly, fill=None, photo=None, z=1):
    bg = f'url({photo}) center/cover' if photo else fill
    parts.append(
        f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
        f'clip-path:polygon({clip_poly});background:{bg};z-index:{z}"></div>'
    )
    E(label, x, y, w, h)


# 3. TL seats sliver -- flat dark teal panel (swap: stock theater-seat photo too small to read)
clipped("bleed_tl_seats", 240, 0, 216, 44, "0% 0%, 100% 0%, 55% 100%, 20% 100%",
        fill="#16352B", z=1)
# 4. L-mid person -- real AQ photo (xmas)
clipped("bleed_lmid_person", 240, 157, 60, 176, "40% 0%, 100% 10%, 100% 100%, 0% 90%",
        photo=core.PHOTOS["xmas"], z=1)
# 5. BL book-pages corner -- flat pale-sky panel (swap: stock photo with foreign-language type)
clipped("bleed_bl_pages", 0, 333, 156, 295, "0% 0%, 100% 32%, 100% 100%, 0% 100%",
        fill=shapes.lighten(A[4], 0.72), z=1)
# 6. TR daisy kite -- flat denim-blue panel (swap: small stock still-life kite)
clipped("bleed_tr_kite", 894, 0, 60, 157, "40% 0%, 100% 0%, 60% 100%, 0% 100%",
        fill="#4A5C86", z=1)
# 7. TR tulip corner -- real AQ photo (diwali) -- loudest single colour patch, kept photographic
clipped("bleed_tr_tulip", 954, 0, 246, 188, "22% 0%, 100% 0%, 100% 100%, 0% 42%",
        photo=core.PHOTOS["diwali"], z=1)
# 8. R-mid buttercup -- real AQ photo (edu), largest bleed panel
clipped("bleed_rmid_flowers", 1002, 302, 198, 257, "35% 0%, 100% 0%, 100% 100%, 0% 100%",
        photo=core.PHOTOS["edu"], z=1)
# 10. bottom-mid chair -- flat tomato panel (swap: small stock furniture photo)
clipped("bleed_bmid_chair", 576, 590, 144, 38, "25% 0%, 75% 0%, 90% 100%, 10% 100%",
        fill=A[3], z=1)

# 9. BR swing tag -- a paper/text card (not a photo), rotated, own real AQ copy (never the
#    reference's literal garment-care words -- RECREATION_PROTOCOL rule 4)
# v1 tracked this element with a hand-padded box that overflowed the canvas
# (1006,466,196,166 -> right/bottom edge past 1200x628). CLAUDE.md Sec10 names this exact
# bug ("Rotated element's real footprint is bigger than its CSS size") and its fix
# (layout.rotated_bbox) -- used here instead of guessing a pad.
TAG_X, TAG_Y, TAG_W, TAG_H, TAG_DEG = 1000, 462, 160, 140, -9
TAG_BOX = lay.rotated_bbox(TAG_X, TAG_Y, TAG_W, TAG_H, TAG_DEG)
parts.append(
    f'<div style="position:absolute;left:{TAG_X}px;top:{TAG_Y}px;width:{TAG_W}px;height:{TAG_H}px;'
    f'transform:rotate({TAG_DEG}deg);background:{A[1]};border-radius:10px;'
    f'box-shadow:3px 4px 0 {INK};z-index:2"></div>'
)
E("bleed_br_tag_bg", *TAG_BOX)
parts.append(
    f'<div style="position:absolute;left:{TAG_X+14}px;top:{TAG_Y+28}px;width:{TAG_W-28}px;'
    f'transform:rotate({TAG_DEG}deg);font-family:var(--d);font-weight:900;font-size:24px;line-height:1.0;'
    f'color:{INK};text-transform:uppercase;z-index:3">Thank<br>you</div>'
)
E("bleed_br_tag_text", TAG_X + 8, TAG_Y + 18, TAG_W - 16, 74)

# ---------------------------------------------------------------- 11. central card ("paper ground")
parts.append(
    f'<div style="position:absolute;left:{CARD_X}px;top:{CARD_Y}px;width:{CARD_W}px;height:{CARD_H}px;'
    f'border-radius:{CARD_R}px;background:{CARD_BG};box-shadow:0 18px 40px rgba(10,10,10,.14);'
    f'z-index:4"></div>'
)
E("card_bg", CARD_X, CARD_Y, CARD_W, CARD_H)

# ---------------------------------------------------------------- 12-15. step list (zig-zag)


def step(label_text, sup, x, y):
    parts.append(
        f'<span class="measure" data-tag="step_{sup}" style="position:absolute;left:{x}px;top:{y}px;'
        f'font-family:var(--m);font-weight:700;font-size:17px;color:{INK};z-index:20">'
        f'&bull; {label_text.upper()}<sup style="font-size:10px">{sup}</sup></span>'
    )


step("Intake", "01", 372, 90)
E("step_intake", 372, 90, 110, 22)
step("Production", "02", 452, 148)
E("step_production", 452, 148, 155, 22)
step("Review", "03", 372, 380)
E("step_review", 372, 380, 115, 22)
step("Delivery", "04", 760, 380)
E("step_delivery", 760, 380, 100, 22)

# ---------------------------------------------------------------- 16-26. the pile (11 objects)
# every pair inside the pile overlaps BY DESIGN -- collision_check is the wrong question here
# (CLAUDE.md Sec10 "resolve_label_z" row); ignored via collision_ignore below, and
# resolve_label_z is used instead to guarantee no object's own LABEL is buried.

PILE_KEYS = ["qcard", "docard", "forreview", "bookphoto", "ribbed", "autile", "aatile",
             "approved", "sticky", "feedback", "jpgtile", "mp4tile"]
PILE_BOX = {}    # key -> (x, y, w, h) full object footprint
LABEL_BOX = {}   # key -> (x, y, w, h) the READABLE part only (what resolve_label_z protects)
INIT_Z = {}      # key -> hand-picked initial z, matching the reference's visual depth order

# 19. beige "Q" lorem card -- deepest element in the stack
QX, QY, QW, QH = 492, 198, 110, 207
PILE_BOX["qcard"] = (QX, QY, QW, QH)
LABEL_BOX["qcard"] = (QX, QY, 45, QH)   # only a left sliver of text ever stays visible
INIT_Z["qcard"] = 1

# 21. green ribbed rect -- anchors the bottom of the pile, mostly behind the book photo
# (narrower than v1's 220px -- that width pushed into the "Delivery" label's column and
# forced an unwanted choice between shrinking the pile or the text; the reference's own
# pile reads about this width relative to the card)
RX, RY, RW, RH = 575, 350, 165, 140
PILE_BOX["ribbed"] = (RX, RY, RW, RH)
LABEL_BOX["ribbed"] = (RX, RY + RH - 25, RW, 25)   # the bit that peeks out below the book photo
INIT_Z["ribbed"] = 2

# 20. blue book photo
BX, BY, BW, BH = 575, 175, 165, 290
PILE_BOX["bookphoto"] = (BX, BY, BW, BH)
LABEL_BOX["bookphoto"] = (BX, BY, BW, 40)   # top strip stays clear of everything in front
INIT_Z["bookphoto"] = 3

# 17. white doc card "01 Campaign"
DX, DY, DW, DH = 360, 160, 70, 80
PILE_BOX["docard"] = (DX, DY, DW, DH)
LABEL_BOX["docard"] = (DX + 4, DY + 4, DW - 8, 16)   # its own label line, top of the card
INIT_Z["docard"] = 4

# 18. pink "For review" chip
FX, FY, FW, FH = 400, 300, 92, 28
PILE_BOX["forreview"] = (FX, FY, FW, FH)
LABEL_BOX["forreview"] = (FX, FY, FW, FH)   # the whole chip IS the label
INIT_Z["forreview"] = 5

# 23. lime "Au" tile -- overlaps Aa's lower-left corner + book photo top
UX, UY, UW, UH = 605, 185, 105, 105
PILE_BOX["autile"] = (UX, UY, UW, UH)
LABEL_BOX["autile"] = (UX + UW * 0.30, UY + UH * 0.30, UW * 0.40, UH * 0.40)
INIT_Z["autile"] = 7

# 22. frosted grey "Aa" tile
GX, GY, GW, GH = 660, 95, 140, 170
PILE_BOX["aatile"] = (GX, GY, GW, GH)
LABEL_BOX["aatile"] = (GX + 20, GY + 40, GW - 40, GH - 80)
INIT_Z["aatile"] = 6

# 24. green "Approved" chip
PX, PY, PW, PH = 545, 352, 100, 28
PILE_BOX["approved"] = (PX, PY, PW, PH)
LABEL_BOX["approved"] = (PX, PY, PW, PH)
INIT_Z["approved"] = 8

# 16. sticky-note stack
SX, SY, SW, SH = 635, 68, 60, 50
PILE_BOX["sticky"] = (SX, SY, SW, SH)
LABEL_BOX["sticky"] = (SX, SY, SW, SH)   # small icon glyph, whole tile
INIT_Z["sticky"] = 9

# 25. feedback comment card
CX2, CY2, CW2, CH2 = 400, 430, 150, 95
PILE_BOX["feedback"] = (CX2, CY2, CW2, CH2)
LABEL_BOX["feedback"] = (CX2 + 12, CY2 + 10, CW2 - 24, CH2 - 20)
INIT_Z["feedback"] = 10

# 26a/b. .jpg / .mp4 file tiles. v1 put BOTH labels at the bottom of their tile and let mp4
# (in front, lower-right) sit almost exactly over jpg's bottom strip -- render's own DOM scan
# reported the ".jpg" span genuinely buried (opaque div covering it at 6/9 sample points), a
# real miss (audit item 26 requires the pair to be distinctly readable). Fix: jpg's own label
# lives at the TOP of its tile, clear of the overlap, which only ever eats its lower half.
JX, JY, JW, JH = 770, 415, 68, 88
PILE_BOX["jpgtile"] = (JX, JY, JW, JH)
LABEL_BOX["jpgtile"] = (JX, JY, JW, 26)
INIT_Z["jpgtile"] = 11

MX, MY, MW, MH = 800, 452, 68, 88
PILE_BOX["mp4tile"] = (MX, MY, MW, MH)
LABEL_BOX["mp4tile"] = (MX, MY + MH - 26, MW, 26)
INIT_Z["mp4tile"] = 12

# --- resolve_label_z: raise anything whose own label ends up buried by the hand-picked order ---
rz_items = [(k, LABEL_BOX[k], INIT_Z[k]) for k in PILE_KEYS]
NEW_Z, UNRESOLVED = lay.resolve_label_z(rz_items, min_visible=0.80)
print("resolve_label_z ->", NEW_Z)
print("resolve_label_z unresolved:", UNRESOLVED)
Z = {k: 10 + NEW_Z[k] for k in PILE_KEYS}   # lift the whole pile above ground/card (z>=4)

# ---- draw the pile, in ascending z order, using the (possibly-raised) resolved z ----
draw_order = sorted(PILE_KEYS, key=lambda k: Z[k])

for k in draw_order:
    z = Z[k]
    if k == "qcard":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:#C9A67B;border-radius:14px;z-index:{z}"></div>')
        parts.append(f'<div style="position:absolute;left:{x+14}px;top:{y+14}px;font-family:var(--d);'
                     f'font-weight:900;font-size:24px;color:{INK};z-index:{z+1}">Q</div>')
        lines = ["Mus u", "pellentesque", "lacus", "Diam imper", "sociis", "eget t",
                 "aenean", "phare", "fugiat risus", "nam et duis. Nu"]
        for i, ln in enumerate(lines):
            parts.append(f'<div style="position:absolute;left:{x+14}px;top:{y+52+i*15}px;'
                         f'font-family:var(--e);font-weight:400;font-size:11px;color:{GREY};'
                         f'z-index:{z+1}">{ln}</div>')
        E("q_card_visible", x, y, w, h)
    elif k == "ribbed":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:repeating-linear-gradient(125deg,{A[1]} 0px,{A[1]} 6px,'
                     f'{A[6]} 6px,{A[6]} 12px);z-index:{z}"></div>')
    elif k == "bookphoto":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:url({core.PHOTOS["food"]}) center/cover;border-radius:6px;'
                     f'box-shadow:0 8px 18px rgba(10,10,10,.25);z-index:{z}"></div>')
    elif k == "docard":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:{PAPER};border-radius:6px;box-shadow:0 6px 14px rgba(10,10,10,.18);'
                     f'clip-path:polygon(0 0,80% 0,100% 20%,100% 100%,0 100%);z-index:{z}"></div>')
        parts.append(f'<div style="position:absolute;left:{x+6}px;top:{y+6}px;font-family:var(--m);'
                     f'font-weight:700;font-size:8px;color:{INK};z-index:{z+1}">01 CAMPAIGN</div>')
        for i in range(4):
            parts.append(f'<div style="position:absolute;left:{x+6}px;top:{y+22+i*11}px;width:{w-16}px;'
                         f'height:3px;background:#D8D6CC;z-index:{z+1}"></div>')
    elif k == "forreview":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div class="measure" data-tag="for_review" style="position:absolute;left:{x}px;'
                     f'top:{y}px;width:{w}px;height:{h}px;border-radius:999px;'
                     f'background:{shapes.lighten(A[0], 0.78)};display:flex;align-items:center;'
                     f'justify-content:center;z-index:{z}"><span style="font-family:var(--e);'
                     f'font-weight:700;font-size:14px;color:{INK}">For review</span></div>')
    elif k == "autile":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'transform:rotate(-6deg);background:{shapes.lighten(A[2], 0.35)};border-radius:18px;'
                     f'box-shadow:0 8px 16px rgba(10,10,10,.2);display:flex;align-items:center;'
                     f'justify-content:center;z-index:{z}"><span style="font-family:var(--s);'
                     f'font-style:italic;font-size:44px;color:{INK}">Au</span></div>')
    elif k == "aatile":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:rgba(150,152,140,.72);border-radius:22px;'
                     f'box-shadow:0 10px 22px rgba(10,10,10,.2);display:flex;align-items:center;'
                     f'justify-content:center;z-index:{z}"><span style="font-family:var(--d);'
                     f'font-weight:900;font-size:60px;color:#FFFFFF">Aa</span></div>')
    elif k == "approved":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div class="measure" data-tag="approved" style="position:absolute;left:{x}px;'
                     f'top:{y}px;width:{w}px;height:{h}px;border-radius:999px;background:{A[1]};'
                     f'display:flex;align-items:center;justify-content:center;z-index:{z}">'
                     f'<span style="font-family:var(--e);font-weight:700;font-size:14px;'
                     f'color:#FFFFFF">Approved</span></div>')
    elif k == "sticky":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x+8}px;top:{y+10}px;width:{w-14}px;'
                     f'height:{h-14}px;background:#D8CBB0;border-radius:8px;z-index:{z-2}"></div>')
        parts.append(f'<div style="position:absolute;left:{x+4}px;top:{y+5}px;width:{w-14}px;'
                     f'height:{h-16}px;background:#1F4B3A;border-radius:8px;z-index:{z-1}"></div>')
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w-14}px;'
                     f'height:{h-18}px;background:{A[2]};border-radius:8px;box-shadow:0 4px 10px '
                     f'rgba(10,10,10,.2);z-index:{z}"></div>')
        parts.append(f'<div style="position:absolute;left:{x+w-14}px;top:{y-2}px;width:22px;'
                     f'height:22px;z-index:{z+1}">{dd.stamp("sparkle", INK, style="clean")}</div>')
    elif k == "feedback":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'background:{PAPER};border-radius:14px;box-shadow:0 8px 18px rgba(10,10,10,.18);'
                     f'z-index:{z}"></div>')
        parts.append(f'<div class="measure" data-tag="feedback_text" style="position:absolute;'
                     f'left:{x+12}px;top:{y+10}px;width:{w-24}px;font-family:var(--e);z-index:{z+1}">'
                     f'<span style="font-weight:700;font-size:13px;color:{INK}">Feedback</span>'
                     f'<span style="font-weight:400;font-size:11px;color:{GREY}"> &middot; 2h ago</span>'
                     f'<div style="font-weight:400;font-size:11px;color:{GREY};line-height:1.35;'
                     f'margin-top:4px">I like the simplicity of having a pure visual here, do we '
                     f'want to introduce a fun line?</div></div>')
    elif k == "jpgtile":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'transform:rotate(-6deg);background:{shapes.lighten(A[4], 0.55)};'
                     f'border-radius:12px;box-shadow:0 6px 14px rgba(10,10,10,.2);z-index:{z}">'
                     f'<span style="position:absolute;top:8px;left:0;width:100%;text-align:center;'
                     f'font-family:var(--m);font-weight:700;font-size:11px;color:{INK}">.jpg</span></div>')
    elif k == "mp4tile":
        x, y, w, h = PILE_BOX[k]
        parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                     f'transform:rotate(6deg);background:{shapes.lighten(A[0], 0.6)};'
                     f'border-radius:12px;box-shadow:0 6px 14px rgba(10,10,10,.2);z-index:{z}">'
                     f'<span style="position:absolute;bottom:8px;left:0;width:100%;text-align:center;'
                     f'font-family:var(--m);font-weight:700;font-size:11px;color:{INK}">.mp4</span></div>')
    E(k, *PILE_BOX[k])

# ---------------------------------------------------------------- footer wordmark (real, never inverted)
parts.append(f'<div style="position:absolute;left:{CARD_X}px;top:{CARD_Y+CARD_H-38}px;'
             f'width:150px;height:22px;z-index:20"><img src="{core.LOGO}" style="height:20px;'
             f'display:block"></div>')
E("logo", CARD_X, CARD_Y + CARD_H - 38, 150, 22)

html = B.page(W, H, CREAM, "".join(parts), grain=False)

color_pairs = [
    ("card_bg", CARD_BG, CREAM),
    ("bleed_tl_seats", "#16352B", CREAM),
    ("bleed_tr_kite", "#4A5C86", CREAM),
    ("bleed_bmid_chair", A[3], CREAM),
    ("bleed_br_tag_bg", A[1], CREAM),
]

# every pair of pile objects overlaps by design -- ignore collision_check between them, and
# between the tag's own bg/text pair, and between qcard and its own printed text lines.
PILE_PAIRS = set(itertools.combinations(PILE_KEYS, 2))
CONTAINMENT_IGNORE = PILE_PAIRS | {
    ("q_card_visible", "qcard"), ("bleed_br_tag_bg", "bleed_br_tag_text"),
    ("card_bg", "logo"),
    # deliberate overlap: the swing tag sits IN FRONT of the buttercup photo bleed, same as
    # the reference (audit item 9 overlapping item 8).
    ("bleed_rmid_flowers", "bleed_br_tag_bg"), ("bleed_rmid_flowers", "bleed_br_tag_text"),
}
for k in PILE_KEYS:
    CONTAINMENT_IGNORE.add(("card_bg", k))
    CONTAINMENT_IGNORE.add(("q_card_visible", k))
# every pile object is NESTED inside the card visually (drawn on top of it) -- so are the
# step labels; card_bg containing them is by design, not a collision.
for lbl in ("step_intake", "step_production", "step_review", "step_delivery", "q_card_visible"):
    CONTAINMENT_IGNORE.add(("card_bg", lbl))

pf = lay.preflight(W, H, els, html=html, color_pairs=color_pairs, page_bg=CREAM, core=core,
                   expect_hero=True, collision_ignore=frozenset(CONTAINMENT_IGNORE))
print("PREFLIGHT CLEAN:", pf["clean"])
if not pf["clean"]:
    print({k: v for k, v in pf.items() if k != "clean" and v})


async def main():
    slug = "e7b32bd307aac4"
    outdir = f"out/versions/{slug}"
    os.makedirs(outdir, exist_ok=True)
    async with B.session():
        await B.render(html, f"{outdir}/v2.png", W, H, elements=els, color_pairs=color_pairs,
                        page_bg=CREAM, expect_hero=True, collision_ignore=frozenset(CONTAINMENT_IGNORE))
    print("done ->", f"{outdir}/v2.png")

asyncio.run(main())
