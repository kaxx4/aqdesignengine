"""Workflow B bespoke recreation — 114f2b19c46119 ("You're doing awesome!" onboarding note).
MOCKUP reference: crop the left phone's screen only (compare.crop), score against the crop.
See brain/RECREATION_AUDIT.md '## 114f2b19c46119' for the full step-1 inventory + measurements.
"""
import asyncio, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")
shapes = load("shapes"); tex = load("tex")

W, H = core.SIZES["story"]     # 1080x1920 — chosen to match the phone-screen crop's aspect
                                 # (0.500) far more closely than feed (0.8) or square (1.0);
                                 # see the aspect-gap math in RECREATION_AUDIT.md.
M = 64
A = core.ACCENTS
INK = core.INK
GROUND = "#F1F1F1"    # the reference's own app-UI grey — NOT AQ cream. Declared adaptation:
                       # this piece recreates a PHONE SCREEN, and the grey is representationally
                       # load-bearing (it says "this is an app", cream would say "this is a
                       # poster page"). See precedence-ladder note in the audit entry.
TAN = "#D9CDA6"        # the clip's cream/tan tone — a neutral, not one of the 7 ACCENTS,
                       # matching CLAUDE.md's own description of "AQ's tan doodle tone".

elements = []

def back_arrow():
    return (f'<div style="position:absolute;left:{64}px;top:{78}px;width:48px;height:48px;z-index:6">'
            f'<svg viewBox="0 0 40 50" width="100%" height="100%">'
            f'<path d="M28 8 L10 25 L28 42" fill="none" stroke="{INK}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg></div>')

def progress_bar():
    track_x, track_y, track_w, track_h = 160, 98, 856, 12
    fill_w = int(track_w * 0.12)
    html = (f'<div style="position:absolute;left:{track_x}px;top:{track_y}px;width:{track_w}px;'
            f'height:{track_h}px;background:#D8D8D8;border-radius:999px;z-index:5"></div>'
            f'<div style="position:absolute;left:{track_x}px;top:{track_y}px;width:{fill_w}px;'
            f'height:{track_h}px;background:{A[3]};border-radius:999px;z-index:6"></div>')
    elements.append(("progress_track", track_x, track_y, track_w, track_h))
    return html

def clip_svg():
    # bespoke flat icon — no binder-clip primitive exists in doodles.py/shapes.py.
    return (f'<svg viewBox="0 0 120 100" width="100%" height="100%">'
            f'<path d="M38 58 L50 18 Q60 6 70 18 L82 58 Z" fill="{TAN}" stroke="{INK}" '
            f'stroke-width="4" stroke-linejoin="round"/>'
            f'<rect x="8" y="52" width="104" height="30" rx="8" fill="{TAN}" stroke="{INK}" stroke-width="4"/>'
            f'<line x1="22" y1="62" x2="98" y2="62" stroke="{INK}" stroke-width="2.5" opacity="0.55"/>'
            f'<line x1="22" y1="72" x2="98" y2="72" stroke="{INK}" stroke-width="2.5" opacity="0.55"/>'
            f'<circle cx="60" cy="24" r="5" fill="{INK}"/></svg>')

def flame_svg():
    outline = core.ink_of(A[3])
    outer = "#FF7A2E"
    inner = A[2]
    return (f'<svg viewBox="0 0 100 140" width="100%" height="100%">'
            f'<path d="M50 6 C22 42 12 72 27 102 C19 86 24 64 39 54 '
            f'C33 80 47 96 57 100 C74 90 78 68 66 54 '
            f'C82 64 87 84 76 102 C92 70 80 38 50 6 Z" '
            f'fill="{outer}" stroke="{outline}" stroke-width="5" stroke-linejoin="round"/>'
            f'<path d="M50 46 C38 64 35 80 45 94 C41 84 47 76 50 80 '
            f'C53 71 59 63 55 51 C61 59 64 69 59 80 C69 72 68 58 50 46 Z" '
            f'fill="{inner}"/></svg>')

async def main():
    slug = "114f2b19c46119"
    outdir = f"out/versions/{slug}"
    os.makedirs(outdir, exist_ok=True)

    # NOTE: no separate full-bleed ground div — page() already paints `.p`'s own
    # background to GROUND; a second identical div on top of it tripped
    # reconcile.measure_dom's invisible_fill check (distance 0.0, correctly).
    parts = []
    parts.append(back_arrow())
    elements.append(("back_arrow", 64, 78, 48, 48))
    parts.append(progress_bar())

    # star — tucked behind the note's top-left corner (lower z than the note).
    # x pushed in from the edge: at rot=-18 a 210px square's rotated footprint is
    # 210*(|cos18|+|sin18|) ~= 265px, i.e. ~27px larger on every side than its
    # declared box — flush against x=10 put the ROTATED bbox 17px off-canvas
    # (reconcile.measure_dom caught it: 'OFF-CANVAS dood: box (-17,273)-(247,537)').
    star_x, star_y, star_s = 45, 300, 210
    parts.append(f'<div style="position:absolute;left:{star_x}px;top:{star_y}px;width:{star_s}px;'
                 f'height:{star_s}px;z-index:5">{dd.stamp("star", A[2], rot=-18)}</div>')
    elements.append(("star", star_x, star_y, star_s, star_s))

    # clip — centered, gripping the note's top edge (higher z than the note, note
    # visually hangs FROM it)
    clip_x, clip_y, clip_w, clip_h = 390, 185, 300, 250
    parts.append(f'<div style="position:absolute;left:{clip_x}px;top:{clip_y}px;width:{clip_w}px;'
                 f'height:{clip_h}px;z-index:8">{clip_svg()}</div>')
    elements.append(("clip", clip_x, clip_y, clip_w, clip_h))

    # note card — rotated rounded rect, ink outline + soft shadow (craft layer; a
    # HARD offset shadow per core.hard_shadow() reads wrong here — a phone-UI card
    # elevation is the mechanism worth keeping, so it stays soft, per the precedence
    # ladder's "the mechanism is the part you may not drop")
    card_x, card_y, card_w, card_h = 76, 340, 900, 1130
    card_html = (f'<div style="position:absolute;left:{card_x}px;top:{card_y}px;width:{card_w}px;'
                f'height:{card_h}px;transform:rotate(-4deg);transform-origin:center;'
                f'background:#FFFFFF;border-radius:18px;border:3px solid {INK};'
                f'box-shadow:0 26px 50px rgba(10,10,10,0.22);z-index:6"></div>')
    parts.append(card_html)
    elements.append(("note_card", card_x, card_y, card_w, card_h))

    # body copy — ONE italic Instrument-Serif accent word (house rule, section 9), the
    # rest in Eina. Sits INSIDE the card's rotated frame; approximated here with the
    # card's own rotation applied to the text block too, so the text tilts WITH the paper.
    text_x, text_y, text_w = card_x + 90, card_y + 170, card_w - 180
    body = (f'you’re doing <span style="font-family:var(--s);font-style:italic">amazing</span>! '
            f'let’s take shikshaq’s reading circle to the next level — soon these '
            f'kids will be reading like pros!')
    text_html = (f'<div style="position:absolute;left:{card_x}px;top:{card_y}px;width:{card_w}px;'
                f'height:{card_h}px;transform:rotate(-4deg);transform-origin:center;z-index:7">'
                f'<div style="position:absolute;left:90px;top:170px;width:{text_w}px;'
                f'font-family:var(--e);font-weight:600;font-size:44px;line-height:1.28;'
                f'color:{INK}">{body}</div></div>')
    parts.append(text_html)
    elements.append(("note_text", text_x, text_y, text_w, 620))

    # fire sticker — overlaps the note's lower-right area and hangs off its BOTTOM edge
    # into the grey ground (corrected from the step-1 guess of "past its right edge" —
    # measured off the gridded crop, it is the bottom that breaks past, see audit note)
    fire_x, fire_y, fire_w, fire_h = 560, 1190, 320, 460
    parts.append(f'<div style="position:absolute;left:{fire_x}px;top:{fire_y}px;width:{fire_w}px;'
                 f'height:{fire_h}px;z-index:9">{flame_svg()}</div>')
    elements.append(("fire", fire_x, fire_y, fire_w, fire_h))

    inner = "".join(parts)
    html = B.page(W, H, GROUND, inner, grain=False)

    color_pairs = [("note_card", "#FFFFFF", GROUND, True)]   # edged=True: ink outline + shadow
    text_pairs = [("note_text", INK, "#FFFFFF", 44, False)]

    # star/clip/fire deliberately PARTIALLY overlap note_card (peeking behind/gripping/
    # hanging off it, per the step-1 inventory) — not full containment, so `containers`
    # doesn't apply; declared via collision_ignore instead. note_text truly sits fully
    # inside note_card, so that one goes in `containers`.
    collision_ignore = {frozenset({"star", "note_card"}), frozenset({"clip", "note_card"}),
                        frozenset({"fire", "note_card"})}

    out_png = f"{outdir}/v1.png"
    await B.render(html, out_png, W, H, elements=elements, color_pairs=color_pairs,
                   text_pairs=text_pairs, page_bg=GROUND, expect_hero=False,
                   collision_ignore=collision_ignore, containers=("note_card",))
    print("rendered", out_png)

asyncio.run(main())
