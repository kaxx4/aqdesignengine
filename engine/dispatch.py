"""DISPATCH - the recurring internal-roundup format.

WHAT THIS IS. One person inside AQ (the internal community manager) collects what
every team is doing, drops it into a BRIEF, and gets back the same three artefacts
every single time:

    1. ONE WhatsApp promotional poster   (1080x1350)   <- always exactly one
    2. ONE WhatsApp message              (text)        <- always exactly one
    3. N Instagram stories               (1080x1920)   <- cover + one per item

The point of a SERIES is that the format does not get re-decided each issue. So
everything that could be re-decided is a rule here, and the only hand-input is the
brief's content. Same contract as the rest of the engine (CLAUDE.md section 1):
if an issue looks wrong, the fix goes in this file, not in one issue's output.

WHY A MODULE AND NOT A BESPOKE SCRIPT. A bespoke script is right for a one-off
(Workflow B/C). This runs every week, likely by a different person each time, so
the geometry, the colour semantics and the copy budgets have to survive an author
who has never read CLAUDE.md. Hence: the brief is validated (validate_brief) and
the layout is SOLVED from the content, never typed as constants.

THE ENCODED RULES
-----------------
R1  Department colour is semantic, never a rotation index. core.accent_for(dept).
R2  Max 6 items. A WhatsApp graphic is read at thumbnail size in a group chat;
    past 6 rows nothing is legible and people stop opening it.
R3  EVERY ITEM IS EQUAL. There is no spotlight row, no inverted slab, no "act on
    this" stamp. The format carried all three for one iteration and the person
    who will actually run this series asked for them out: a weekly roundup that
    ranks its own items teaches people to read one row and skip four, and
    whoever writes the brief then has to decide every week which team gets the
    big treatment. The hero is the masthead. The rows are an index.
R4  Copy budgets, from VOICE.md section 5 (the channel layer). The budget that
    binds is PER ITEM:
      chip <= 3 words   head <= 5 words   line <= 28 words
      story <= 70 words (the slide has room to explain)   wa <= 70 words
    (VOICE puts a feed POSTER's body at <= 14. This is not a feed poster - it is
    an internal digest whose whole job is to tell people what happened, and a
    four-word fragment does not do that. Early drafts were clipped to the point
    of being cryptic: "new spot, new vibe" over "both move somewhere new" told a
    reader nothing they did not already know. The rule is now: say the thing.)
R5  Accent type is sized through core.on_cream / on_dark / on_ground. No raw
    accent hex on small type (section 9: accents may shout, not whisper).
R6  Card heights, the masthead size and the story stack are all SOLVED from
    measured content, never typed as constants (bug catalog: "stacked plates
    spaced by a guessed constant clip their own text" - which is exactly what
    v1 of this file did, slicing two body lines in half).
R7  Every text-on-surface pair is declared to text_contrast_check. An opt-in
    check that nobody passes arguments to is worth nothing (session 10f ruling).
R8  NO FRAME MAY HAVE A DEAD HALF. The story slides are built around an
    always-present bottom band for this reason - see _story_item.
R9  THE CRAFT LAYER IS APPLIED EQUALLY. A reviewer's note on issue 01 was that
    the plain cream list read as flat ("make the design more eyecandy"), which
    the pixel critique had been saying on every render (sparse / flat_dominant).
    The answer is section 9's craft layer, not decoration: every item is a
    tinted card with a thick ink outline and a hard offset shadow, carrying a
    solid department-colour badge. Because every card gets the SAME treatment,
    the richness never turns back into a ranking (R3). Brand furniture that is
    not an item - the marker swipe, the count burst - is pink, the house shout,
    which no department owns, so it can never be misread as a department.
    One lemon sparkle is the piece's single hero-shine.
R10 THE TEXT IS HEADERS; THE GRAPHICS CARRY THE DETAIL. The same review asked for
    the WhatsApp text to be short - headers only - with the full sentences living
    on the poster for whoever wants to read them. whatsapp_text() defaults to
    that. brief["wa_mode"] = "full" restores the long version when an issue
    genuinely needs it.

THE PHOTO SLOT. An item may carry photo="food"|"edu"|"diwali"|"xmas" - the four
REAL AQ photographs in core.PHOTOS. The masthead photo card and the story bottom
band both read that field. Nothing here will invent a screenshot, a mockup or a
stock image (section 9, real-assets-only). A brief asking for a photo the bank
does not have raises, rather than quietly rendering an empty <img>.
"""

import os, sys, importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def _load(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(_HERE, name + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


core = _load("core")
B = _load("build")
dd = _load("doodles")
tex = _load("tex")
lay = _load("layout")
shapes = _load("shapes")

M = B.M                       # 64 - one margin constant, read, never retyped
W_FEED, H_FEED = core.SIZES["feed"]
W_STORY, H_STORY = core.SIZES["story"]

# -- R1: the department vocabulary -------------------------------------------
# The KEY is what the community manager types. accent_for() owns the colour.
# A department that is not here is a real error: a new team needs a colour
# decision made once, on purpose, not silently defaulted to pink.
DEPTS = {
    "events":  "events",
    "welfare": "welfare",
    "labs":    "labs",
    "ops":     "ops",
    "content": "content",
}

MAX_ITEMS = 6                                     # R2
HEAD_WORDS, LINE_WORDS, CHIP_WORDS = 5, 28, 3     # R4
STORY_WORDS = 70                                  # R4, the story's longer body
WA_WORDS = 70                                     # R4, per item, wa_mode="full" only

# -- R9: brand furniture (never an item's colour) ----------------------------
PINK = core.ACCENTS[0]        # the house shout: swipe + count burst
LEMON = core.ACCENTS[2]       # the single hero-shine

# -- R6/R9: the poster's card solver -----------------------------------------
# v1 split the row region EQUALLY between items; two-line bodies were sliced by
# the next row. So every card is MEASURED at a candidate type size, the stack is
# summed, and the sizes step down until it fits. If even the smallest pair does
# not fit, that is a CONTENT problem and the brief is told so by name.
CARD_SIZES = ((34, 19), (32, 18), (30, 18), (30, 17), (28, 17), (26, 16))
CARD_PAD = (14, 14)           # (top, bottom) inside a card
CARD_GAP_MIN = 16             # must clear the hard shadow, with air to spare
CARD_BORDER, CARD_SHADOW = 3, 6
CARD_TINT = 0.80              # shapes.lighten amount for a card's pastel fill
BADGE = 60                    # the department numeral disc
CHIP_H, CHIP_GAP, HEAD_GAP = 26, 8, 10
BODY_LH = 1.36
MAST_GUTTER = 40              # air between the wordmark column and the photo
MAST_RANGE = (84, 104)        # the display line may scale between these only
SERIF_SCALE = 1.22            # the accent word runs larger: the serif is narrow
BURST = 128                   # the count burst on the photo's corner

# -- R8: the story's zones ---------------------------------------------------
# A 1080x1920 frame is nearly half as tall again as the poster, and the first
# version simply stacked the poster's content at the top of it: the lower 55%
# of every story rendered as empty ground. The band is what stops that, and it
# is ALWAYS present - it carries the photo when the item has one and a flat
# department plate when it does not, so neither case can leave a dead half.
STORY_TOP = 260               # below the logo / index row
STORY_BAND_Y, STORY_BAND_H = 1400, 360
STORY_NUM_SIZES = (380, 330, 280, 230)   # stepped down until the block fits
STORY_HEAD, STORY_BODY = 88, 29
STORY_CARD_PAD = 34
STORY_STICKER = (270, 150)    # (preferred, smallest) department burst size


class BriefError(ValueError):
    """The brief is wrong. Raised loudly so a bad issue never renders."""


def accent(dept):
    if dept not in DEPTS:
        raise BriefError(
            "unknown department %r. known: %s. Adding one is a colour decision - "
            "put it in dispatch.DEPTS and core.accent_for, do not improvise it "
            "in a brief." % (dept, sorted(DEPTS)))
    return core.accent_for(DEPTS[dept])


def tint_of(acc):
    return shapes.lighten(acc, CARD_TINT)


def _words(s):
    return len(s.replace("\n", " ").split())


def validate_brief(brief):
    """Every rule that can be checked before a single pixel is drawn.

    Returns the brief unchanged so it can be used inline. Raises BriefError with
    the exact field named - this is read by someone who is not a designer.
    """
    items = brief.get("items") or []
    if not items:
        raise BriefError("brief has no items.")
    if len(items) > MAX_ITEMS:
        raise BriefError(
            "%d items. Max is %d (R2) - a WhatsApp graphic is read at thumbnail "
            "size. Split into two issues, or drop the weakest."
            % (len(items), MAX_ITEMS))

    for n, it in enumerate(items, 1):
        for field in ("dept", "chip", "head", "line"):
            if not it.get(field):
                raise BriefError("item %d is missing %r." % (n, field))
        accent(it["dept"])                                          # raises if unknown
        budgets = [("chip", CHIP_WORDS), ("head", HEAD_WORDS), ("line", LINE_WORDS)]
        if it.get("story"):
            budgets.append(("story", STORY_WORDS))
        if it.get("wa"):
            budgets.append(("wa", WA_WORDS))
        for field, budget in budgets:
            if _words(it[field]) > budget:
                raise BriefError(
                    "item %d %r is %d words, budget is %d (R4). Cut it: %r"
                    % (n, field, _words(it[field]), budget, it[field]))
        if it.get("photo") and it["photo"] not in core.PHOTOS:
            raise BriefError(
                "item %d asks for photo %r. Real AQ photos only: %s. Never "
                "fabricate imagery (section 9)."
                % (n, it["photo"], sorted(core.PHOTOS)))
        # VOICE.md section 1 craft invariants, enforced on COPY strings only.
        for field in ("chip", "head", "line", "story", "wa"):
            if it.get(field) and ("—" in it[field] or "–" in it[field]):
                raise BriefError(
                    "item %d %r contains an em/en dash. VOICE.md section 1.1: "
                    "full stop or comma." % (n, field))
    return brief


def story_text(it):
    """The story's body: the long form if the brief wrote one, else the WhatsApp
    line, else the poster line. Stories are the one surface in this format with
    room to actually explain something."""
    return it.get("story") or it.get("wa") or it["line"]


def _mast_lines(tagline):
    """Split the tagline into masthead lines and decide each one's face.

    THE ONE ACCENT WORD. Section 9 allows Instrument Serif italic for at most one
    word per piece. So the LAST line of the tagline is set in the serif - but only
    if it IS one word. A multi-word last line would spend the allowance on a
    phrase, and falls back to the display face instead of breaking the rule.
    Returns [(text, token, scale)] where token is 'd' (display) or 's' (serif)."""
    segs = [w.strip() for w in tagline.split("/") if w.strip()]
    serif_last = len(segs) >= 2 and len(segs[-1].split()) == 1
    out = []
    for k, t in enumerate(segs):
        if serif_last and k == len(segs) - 1:
            out.append((t.lower(), "s", SERIF_SCALE))
        else:
            out.append((t.upper(), "d", 1.0))
    return out


def _mt(text, tok, size, max_width=None, lh=0.9):
    d = {"text": text, "font": tok, "size": size,
         "weight": 900 if tok == "d" else 400,
         "letter_spacing": "-.02em" if tok == "d" else "0", "line_height": lh}
    if max_width:
        d["max_width"] = max_width
    return d


def _burst_svg(lines, fill, size, rot, measured):
    """A die-cut starburst carrying 1-2 lines of label, each FITTED to the burst's
    waist (shapes.fit_font returns BOX units - the unit trap is its whole point).
    `measured` is [(text, px_width_at_20px)], from build.measure_text."""
    fg = core.text_on(fill)
    if len(lines) == 1:
        box, _ = shapes.fit_font(measured[0][1], 20, "burst", size, max_box=24)
        inner = shapes.label(lines[0], size=box, y=50 + box * 0.36, fill=fg)
    else:
        # BIG line first, small line under it: "5 / THINGS" reads as "5 things".
        # The first build put the small word on top and read "things 5".
        b0, _ = shapes.fit_font(measured[0][1], 20, "burst", size, max_box=30)
        b1, _ = shapes.fit_font(measured[1][1], 20, "burst", size, max_box=13)
        inner = (shapes.label(lines[0], size=b0, y=50, fill=fg)
                 + shapes.label(lines[1], size=b1, y=50 + b1 * 1.25, fill=fg))
    return shapes.sticker(shapes.starburst(12, 48, 37), fill, size=size,
                          shadow=True, rot=rot, inner=inner, detail="none")


# ============================================================================
# 1. THE WHATSAPP POSTER
# ============================================================================

async def poster(brief):
    """Build the one WhatsApp promotional poster.

    Returns (html, elements, gate_kwargs) - the caller renders it, so a batch can
    hold one browser open (build.session()).
    """
    validate_brief(brief)
    items = brief["items"]
    n = len(items)
    inner, els = [], []
    text_pairs, color_pairs = [], []
    BG = core.CREAM
    inner.append('<div style="position:absolute;inset:0;background:var(--bg);z-index:0"></div>')

    inner.append(B.logo(y=56))
    els.append(("logo", M, 56, 190, 32))

    issue = brief.get("issue", "01")
    tagline = brief.get("tagline", "what's / moving")
    dateline = brief.get("dateline", "")
    kicker = brief.get("kicker", "this week at aq")

    inner.append(
        f'<span class="measure" data-tag="stamp" style="position:absolute;top:60px;right:{M}px;'
        f'font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.14em;'
        f'text-transform:uppercase;color:var(--ink3);z-index:20">{kicker} &middot; no. {issue}</span>')
    els.append(("stamp", 620, 58, 396, 24))
    text_pairs.append(("stamp", "#5A5A55", BG, 15, True))

    # -- the photo card, PLACED FIRST: the masthead is sized to the room it leaves.
    # Rotation is why its position is computed: a tilted card's real footprint is
    # wider than its CSS width, and placing it flush by CSS breached the margin.
    photo_bottom, photo_left = 0, W_FEED - M
    photo_key = brief.get("cover_photo") or next(
        (it.get("photo") for it in items if it.get("photo")), None)
    burst_box = None
    if photo_key:
        if photo_key not in core.PHOTOS:
            raise BriefError("cover_photo %r is not a real AQ photo." % photo_key)
        ps, rot, py = 198, -4, 130
        _, _, bw, bh = lay.rotated_bbox(0, 0, ps, ps, rot)
        over = (bw - ps) / 2.0
        px = int(W_FEED - M - ps - over)
        inner.append(
            f'<div class="measure" data-tag="photo" style="position:absolute;top:{py}px;left:{px}px;'
            f'width:{ps}px;height:{ps}px;transform:rotate({rot}deg);z-index:9;'
            f'border:5px solid var(--ink);box-shadow:10px 10px 0 var(--ink);overflow:hidden">'
            f'{tex.photo_ink(core.PHOTOS[photo_key], "width:100%;height:100%")}</div>')
        els.append(("photo", px - over, py - over, bw, bh))
        inner.append(tex.tape(px + 56, py - 22, w=120, h=36, rot=-7, z=14))
        photo_bottom, photo_left = py + ps + over, px - over

        # THE COUNT BURST. Brand furniture (R9): pink, never a department's hue.
        # It sits on the photo's lower-left corner, pinning the photo to the page
        # the way tape does, and carries the item count so the number can never
        # disagree with the rows under it.
        cm = await B.measure_text([_mt(str(n), "d", 20, lh=1), _mt("THINGS", "d", 20, lh=1)],
                                  W_FEED, H_FEED)
        brot = -10
        # It straddles the photo's LEFT edge rather than hanging off its bottom
        # corner: the first placement dropped 60px below the photo and pushed the
        # whole card stack down until the solver refused to fit five items.
        bx = int(photo_left - BURST * 0.52)
        by = int(photo_bottom - BURST * 0.96)
        burst = _burst_svg([str(n), "THINGS"], PINK, BURST, brot,
                           [(str(n), cm[0]["text_w"] * 2.2), ("THINGS", cm[1]["text_w"])])
        inner.append(f'<div class="measure" data-tag="burst" style="position:absolute;'
                     f'top:{by}px;left:{bx}px;width:{BURST}px;height:{BURST}px;z-index:15">'
                     f'{burst}</div>')
        burst_box = lay.rotated_bbox(bx, by, BURST, BURST, brot)
        els.append(("burst", *burst_box))
        color_pairs.append(("burst", PINK, BG, True))

    # -- the masthead. The display line is SIZED TO ITS COLUMN (measured once at a
    # reference size, then scaled), and the last word of the tagline is the one
    # serif accent section 9 allows (_mast_lines).
    lines = _mast_lines(tagline)
    col_right = (burst_box[0] if burst_box else photo_left) - MAST_GUTTER
    avail = col_right - M
    REF = 100
    ref = await B.measure_text([_mt(t, tok, REF * sc) for t, tok, sc in lines], W_FEED, H_FEED)
    widest = max((m["text_w"] or m["w"]) for m in ref) or 1
    MAST = int(max(MAST_RANGE[0], min(MAST_RANGE[1], REF * avail / widest)))
    ms = await B.measure_text([_mt(t, tok, MAST * sc) for t, tok, sc in lines], W_FEED, H_FEED)

    y = 128
    mast_tags = []
    last_bottom = y
    for k, ((t, tok, sc), m) in enumerate(zip(lines, ms)):
        tag = "mast%d" % k
        mast_tags.append(tag)
        size = int(MAST * sc)
        gw = m["glyph_w"] or m["text_w"]
        gh = m["glyph_h"] or m["ink_h"]
        if tok == "s":
            # the marker swipe: pink, behind the lower half of the accent word
            sw_y = int(y + size * 0.50)
            inner.append(
                f'<div data-tag="swipe" style="position:absolute;top:{sw_y}px;left:{M - 10}px;'
                f'width:{gw + 30}px;height:{int(size * 0.30)}px;background:{PINK};'
                f'transform:rotate(-1.5deg);border-radius:6px;z-index:7"></div>')
            els.append(("swipe", M - 10, sw_y, gw + 30, int(size * 0.30)))
            text_pairs.append((tag, core.INK, PINK, size, True))
            font = "font-family:var(--s);font-style:italic;font-weight:400;letter-spacing:0"
        else:
            text_pairs.append((tag, core.INK, BG, size, True))
            font = "font-family:var(--d);font-weight:900;letter-spacing:-.02em"
        inner.append(
            f'<div class="measure" data-tag="{tag}" style="position:absolute;top:{y}px;left:{M}px;'
            f'{font};font-size:{size}px;line-height:.9;color:var(--ink);'
            f'white-space:nowrap;z-index:8">{t}</div>')
        els.append((tag, M, y, gw, max(m["ink_h"], m["h"])))
        if k == 0:
            # the single hero-shine (section 9), off the first line's last glyph
            sp = 64
            sx, sy = int(M + gw + 14), int(y - 10)
            if sx + sp < col_right:
                inner.append(f'<div style="position:absolute;top:{sy}px;left:{sx}px;'
                             f'width:{sp}px;height:{sp}px;z-index:9">'
                             f'{dd.stamp("sparkle", LEMON, rot=12)}</div>')
                els.append(("spark", sx, sy, sp, sp))
        last_bottom = y + gh
        y += int(size * 0.9)
    mast_bottom = last_bottom + 14

    # the dateline closes the masthead
    date_y = int(mast_bottom + 18)
    if dateline:
        inner.append(
            f'<div class="measure" data-tag="dateline" style="position:absolute;top:{date_y}px;'
            f'left:{M}px;font-family:var(--m);font-weight:700;font-size:18px;'
            f'letter-spacing:.16em;text-transform:uppercase;color:var(--ink3);z-index:9">'
            f'week of {dateline}</div>')
        els.append(("dateline", M, date_y, 520, 26))
        text_pairs.append(("dateline", "#5A5A55", BG, 18, True))

    # -- the cards. R6: the region is measured, the stack is SOLVED. -----------
    foot_top = 1262
    burst_bottom = (burst_box[1] + burst_box[3]) if burst_box else 0
    top = int(max(date_y + 26 + 34, photo_bottom + 26, burst_bottom + 18))
    specs = await _plan_cards(items, foot_top - top - CARD_SHADOW)

    ry = top
    card_tags = []
    for i, it in enumerate(items):
        card_tags.append(_card(inner, els, text_pairs, color_pairs, it, i,
                               accent(it["dept"]), ry, specs[i], BG))
        ry += specs[i]["h"]

    # -- footer band ---------------------------------------------------------
    inner.append(
        f'<div style="position:absolute;top:{foot_top}px;left:0;width:{W_FEED}px;'
        f'height:{H_FEED - foot_top}px;background:var(--ink);z-index:6"></div>')
    els.append(("footband", 0, foot_top, W_FEED, H_FEED - foot_top))
    color_pairs.append(("footband", core.INK, BG, True))

    inner.append(
        f'<span class="measure" data-tag="handle" style="position:absolute;bottom:34px;left:{M}px;'
        f'font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.08em;'
        f'color:{core.PAPER};z-index:20">{brief.get("handle", "@ngo.aquaterra")}</span>')
    els.append(("handle", M, H_FEED - 58, 240, 24))
    text_pairs.append(("handle", core.PAPER, core.INK, 17, True))

    site = brief.get("site", "")
    if site:
        site_col = core.on_dark(PINK, 17)
        inner.append(
            f'<span class="measure" data-tag="site" style="position:absolute;bottom:34px;'
            f'right:{M}px;font-family:var(--m);font-weight:700;font-size:17px;'
            f'letter-spacing:.08em;color:{site_col};z-index:20">{site}</span>')
        els.append(("site", 700, H_FEED - 58, 316, 24))
        text_pairs.append(("site", site_col, core.INK, 17, True))

    html = B.page(W_FEED, H_FEED, "var(--bg)", "".join(inner), grain=False)

    # THE IGNORE PAIRS, each one a deliberate overlap and not a hidden bug:
    #  * consecutive wordmark lines: line-height .9 reserves an em box the caps
    #    never paint, so the DECLARED boxes (the overflow extent measure_dom checks)
    #    overlap by reserved air while the ink does not touch;
    #  * the swipe sits under the accent word - that is what a marker swipe is;
    #  * the burst pins the photo's corner - that is what it is for.
    ignore = [(a, b) for a, b in zip(mast_tags, mast_tags[1:])]
    ignore += [("swipe", t) for t in mast_tags]
    ignore += [("burst", "photo")]
    #  * a card HOLDS its badge, chip, headline and line. `containers` tells
    #    layout.collision_check that; audit.py's DOM check only reads pairs.
    ignore += [(c, c[:-4] + part) for c in card_tags
               for part in ("badge", "chip", "head", "line")]
    gate = dict(color_pairs=color_pairs, text_pairs=text_pairs,
                containers=tuple(card_tags) + ("footband",), page_bg="var(--bg)",
                bleed_tags=("footband", "handle", "site"), expect_hero=False,
                collision_ignore=ignore)
    return html, els, gate


# -- R6, the card solver ------------------------------------------------------

def _card_geometry():
    """Where a card's badge and text column sit, and how wide the text may be.
    One function so the MEASURE pass and the DRAW pass cannot disagree."""
    bx = M + 20
    cx = bx + BADGE + 22
    return bx, cx, (W_FEED - M - 28) - cx


async def _plan_cards(items, region):
    """Measure every card, then pick the largest type pair whose stack fits."""
    _, _, tw = _card_geometry()
    for hsize, bsize in CARD_SIZES:
        specs = []
        for it in items:
            m = await B.measure_text([
                _mt(it["head"].upper(), "d", hsize, max_width=tw, lh=1.02),
                {"text": it["line"], "font": "e", "size": bsize, "weight": 500,
                 "line_height": BODY_LH, "max_width": tw},
            ], W_FEED, H_FEED)
            pt, pb = CARD_PAD
            text_h = CHIP_H + CHIP_GAP + m[0]["ink_h"] + HEAD_GAP + m[1]["ink_h"]
            specs.append({"hsize": hsize, "bsize": bsize, "tw": tw, "pad_top": pt,
                          "head_h": m[0]["ink_h"], "line_h": m[1]["ink_h"],
                          "content": pt + max(BADGE, text_h) + pb})
        total = sum(s["content"] for s in specs)
        if total + CARD_GAP_MIN * len(items) <= region:
            gap = (region - total) // len(items)
            for s in specs:
                s["h"], s["gap"] = s["content"] + gap, gap
            return specs
    raise BriefError(
        "the %d items do not fit the poster even at the smallest type in "
        "CARD_SIZES. This is a CONTENT problem, not a layout one: shorten the "
        "longest `line`, or move an item to the next issue. The engine will not "
        "ship a body size nobody can read on a phone." % len(items))


def _card(inner, els, tp, cp, it, i, acc, y, spec, page_bg):
    """One item: a tinted card with the house craft layer (R9), identical for
    every item (R3). Returns the card's tag so the gate can treat it as a
    container for everything drawn on it."""
    tag = "r%d" % i
    tint = tint_of(acc)
    h = spec["content"]
    cw = W_FEED - 2 * M
    inner.append(
        f'<div class="measure" data-tag="{tag}card" style="position:absolute;top:{y}px;left:{M}px;'
        f'width:{cw}px;height:{h}px;background:{tint};border:{CARD_BORDER}px solid var(--ink);'
        f'border-radius:{core.RADII["inner"]}px;box-shadow:{CARD_SHADOW}px {CARD_SHADOW}px 0 var(--ink);'
        f'z-index:5"></div>')
    els.append((tag + "card", M, y, cw + CARD_SHADOW, h + CARD_SHADOW))
    cp.append((tag + "card", tint, page_bg, True))           # edged: outline + shadow

    bx, cx, tw = _card_geometry()
    by = y + spec["pad_top"]
    num_fg = core.text_on(acc)
    inner.append(
        f'<div class="measure" data-tag="{tag}badge" style="position:absolute;top:{by}px;left:{bx}px;'
        f'width:{BADGE}px;height:{BADGE}px;border-radius:50%;background:{acc};'
        f'border:3px solid var(--ink);box-shadow:3px 3px 0 var(--ink);display:flex;'
        f'align-items:center;justify-content:center;font-family:var(--d);font-weight:900;'
        f'font-size:24px;letter-spacing:-.02em;color:{num_fg};z-index:9">{i + 1:02d}</div>')
    els.append((tag + "badge", bx, by, BADGE + 3, BADGE + 3))
    tp.append((tag + "badge", num_fg, acc, 24, True))
    cp.append((tag + "badge", acc, tint, True))

    chip_fg = core.on_ground(acc, tint, 13)
    inner.append(
        f'<div class="measure" data-tag="{tag}chip" style="position:absolute;top:{by}px;left:{cx}px;'
        f'font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.16em;'
        f'text-transform:uppercase;color:{chip_fg};z-index:9">{it["chip"]}</div>')
    els.append((tag + "chip", cx, by, 320, CHIP_H - 6))
    tp.append((tag + "chip", chip_fg, tint, 13, True))

    hy = by + CHIP_H + CHIP_GAP - 8
    inner.append(
        f'<div class="measure" data-tag="{tag}head" style="position:absolute;top:{hy}px;left:{cx}px;'
        f'width:{tw}px;font-family:var(--d);font-weight:900;font-size:{spec["hsize"]}px;'
        f'line-height:1.02;letter-spacing:-.01em;color:var(--ink);z-index:9">'
        f'{it["head"].upper()}</div>')
    els.append((tag + "head", cx, hy, tw, spec["head_h"]))
    tp.append((tag + "head", core.INK, tint, spec["hsize"], True))

    ly = hy + spec["head_h"] + HEAD_GAP
    inner.append(
        f'<div class="measure" data-tag="{tag}line" style="position:absolute;top:{ly}px;left:{cx}px;'
        f'width:{tw}px;font-family:var(--e);font-weight:500;font-size:{spec["bsize"]}px;'
        f'line-height:{BODY_LH};color:#2E2E2B;z-index:9">{it["line"]}</div>')
    els.append((tag + "line", cx, ly, tw, spec["line_h"]))
    tp.append((tag + "line", "#2E2E2B", tint, spec["bsize"], False))
    return tag + "card"


# ============================================================================
# 2. THE INSTAGRAM STORIES
# ============================================================================

async def stories(brief):
    """Returns [(name, html, elements, gate_kwargs), ...] - cover first."""
    validate_brief(brief)
    out = [await _story_cover(brief)]
    n = len(brief["items"])
    for i, it in enumerate(brief["items"]):
        out.append(await _story_item(brief, it, i, n))
    return out


def _story_frame(dark, index_tag):
    """The furniture every story slide shares: ground, logo, index tag."""
    bg = "var(--ink)" if dark else "var(--bg)"
    inner = ['<div style="position:absolute;inset:0;background:%s;z-index:0"></div>' % bg]
    inner.append(B.logo(dark=dark, y=76))
    els = [("logo", M, 76, 190, 32)]
    col = "#8A867A" if dark else "var(--ink3)"
    inner.append(
        f'<span class="measure" data-tag="idx" style="position:absolute;top:80px;right:{M}px;'
        f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.16em;'
        f'text-transform:uppercase;color:{col};z-index:20">{index_tag}</span>')
    els.append(("idx", 700, 78, 316, 26))
    return inner, els


def _story_footer(inner, els, tp, brief, dark, cta):
    ground = core.INK if dark else core.CREAM
    col = core.PAPER if dark else core.INK
    sub = "#8A867A" if dark else "#5A5A55"
    inner.append(
        f'<span class="measure" data-tag="cta" style="position:absolute;bottom:106px;left:{M}px;'
        f'font-family:var(--e);font-weight:500;font-size:22px;color:{sub};z-index:20">{cta}</span>')
    els.append(("cta", M, H_STORY - 140, 760, 30))
    tp.append(("cta", sub, ground, 22, False))

    line = brief.get("handle", "@ngo.aquaterra")
    if brief.get("site"):
        line += "   &middot;   " + brief["site"]
    inner.append(
        f'<span class="measure" data-tag="handle" style="position:absolute;bottom:58px;left:{M}px;'
        f'font-family:var(--m);font-weight:700;font-size:21px;letter-spacing:.08em;color:{col};'
        f'z-index:20">{line}</span>')
    els.append(("handle", M, H_STORY - 90, 760, 28))
    tp.append(("handle", col, ground, 21, True))


async def _story_cover(brief):
    """The contents page. Every item, stacked, with its department disc.

    This slide exists so the set has a first frame that says what the set IS.
    Without it story 1 reads as a standalone announcement and the rest look like
    unrelated posts that happened to go up together.
    """
    issue = brief.get("issue", "01")
    items = brief["items"]
    inner, els = _story_frame(True, brief.get("kicker", "this week at aq"))
    tp, cp = [], []
    tp.append(("idx", "#8A867A", core.INK, 16, True))

    # the issue burst, top right: brand furniture, pink (R9)
    CB, crot = 230, 8
    nm = await B.measure_text([_mt(issue, "d", 20, lh=1), _mt("ISSUE", "d", 20, lh=1)],
                              W_STORY, H_STORY)
    burst = _burst_svg([issue, "ISSUE"], PINK, CB, crot,
                       [(issue, nm[0]["text_w"] * 1.4), ("ISSUE", nm[1]["text_w"])])
    _, _, bw, _ = lay.rotated_bbox(0, 0, CB, CB, crot)
    bxo = (bw - CB) / 2.0
    bx, by = int(W_STORY - M - CB - bxo), 190
    inner.append(f'<div class="measure" data-tag="burst" style="position:absolute;top:{by}px;'
                 f'left:{bx}px;width:{CB}px;height:{CB}px;z-index:12">{burst}</div>')
    els.append(("burst", *lay.rotated_bbox(bx, by, CB, CB, crot)))
    cp.append(("burst", PINK, core.INK, True))

    lines = _mast_lines(brief.get("tagline", "what's / moving"))
    CT = 132
    ms = await B.measure_text([_mt(t, tok, CT * sc, lh=0.92) for t, tok, sc in lines],
                              W_STORY, H_STORY)
    y = 330
    ct = []
    for k, ((t, tok, sc), m) in enumerate(zip(lines, ms)):
        tag = "ctitle%d" % k
        ct.append(tag)
        size = int(CT * sc)
        font = ("font-family:var(--s);font-style:italic;font-weight:400"
                if tok == "s" else "font-family:var(--d);font-weight:900;letter-spacing:-.02em")
        colr = PINK if tok == "s" else core.PAPER
        inner.append(
            f'<div class="measure" data-tag="{tag}" style="position:absolute;top:{y}px;left:{M}px;'
            f'{font};font-size:{size}px;line-height:.92;color:{colr};white-space:nowrap;'
            f'z-index:9">{t}</div>')
        els.append((tag, M, y, m["glyph_w"] or m["text_w"], max(m["ink_h"], m["h"])))
        tp.append((tag, colr, core.INK, size, True))
        y += int(size * 0.92)

    sub = "week of %s" % brief["dateline"] if brief.get("dateline") else "no. %s" % issue
    inner.append(
        f'<div class="measure" data-tag="csub" style="position:absolute;top:{y + 30}px;left:{M}px;'
        f'font-family:var(--m);font-weight:700;font-size:26px;letter-spacing:.16em;'
        f'text-transform:uppercase;color:#B9B4A6;z-index:9">{sub}</div>')
    els.append(("csub", M, y + 30, 700, 36))
    tp.append(("csub", "#B9B4A6", core.INK, 26, True))

    # the index: one CARD per item, the same craft layer as the poster (R9), so the
    # cover no longer reads as a plain text list on black. On an INK ground the
    # ink outline would vanish (bug catalog: "ink outline + hard shadow on an ink
    # field"), so the edge is outline_of(INK) and the hard shadow takes the
    # department colour - which is where the cover's colour comes from. Every card
    # is identical apart from its hue (R3). The step is DIVIDED out of the room and
    # the block centred in it (R8), so three items and six both fit the frame.
    iy = y + 140
    avail = (H_STORY - 270) - iy
    step = max(96, avail // max(len(items), 1))
    ch = min(124, step - 34)                     # card height, leaves room for shadow
    block = (len(items) - 1) * step + ch
    iy += max(0, (avail - block) // 2)
    edge = core.outline_of(core.INK)
    cw = W_STORY - 2 * M - 10                    # minus the shadow's reach
    card_tags = []
    for i, it in enumerate(items):
        acc = accent(it["dept"])
        tint = tint_of(acc)
        fg = core.text_on(acc)
        tag = "ixcard%d" % i
        card_tags.append(tag)
        inner.append(
            f'<div class="measure" data-tag="{tag}" style="position:absolute;top:{iy}px;left:{M}px;'
            f'width:{cw}px;height:{ch}px;background:{tint};border:{CARD_BORDER}px solid {edge};'
            f'border-radius:{core.RADII["inner"]}px;box-shadow:10px 10px 0 {acc};z-index:8"></div>')
        els.append((tag, M, iy, cw + 10, ch + 10))
        cp.append((tag, tint, core.INK, True))
        d = 64
        dy = iy + (ch - d) // 2
        inner.append(
            f'<div class="measure" data-tag="sw{i}" style="position:absolute;top:{dy}px;left:{M + 22}px;'
            f'width:{d}px;height:{d}px;border-radius:50%;background:{acc};'
            f'border:3px solid var(--ink);display:flex;align-items:center;justify-content:center;'
            f'font-family:var(--d);font-weight:900;font-size:24px;color:{fg};z-index:9">'
            f'{i + 1:02d}</div>')
        els.append(("sw%d" % i, M + 22, dy, d, d))
        tp.append(("sw%d" % i, fg, acc, 24, True))
        chip_fg = core.on_ground(acc, tint, 15)
        tx = M + 22 + d + 26
        tw = M + cw - 26 - tx
        inner.append(
            f'<div class="measure" data-tag="ixchip{i}" style="position:absolute;top:{iy + 20}px;'
            f'left:{tx}px;font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.16em;'
            f'text-transform:uppercase;color:{chip_fg};z-index:9">{it["chip"]}</div>')
        els.append(("ixchip%d" % i, tx, iy + 20, 320, 20))
        tp.append(("ixchip%d" % i, chip_fg, tint, 15, True))
        inner.append(
            f'<div class="measure" data-tag="ix{i}" style="position:absolute;top:{iy + 46}px;'
            f'left:{tx}px;width:{tw}px;font-family:var(--d);font-weight:900;font-size:44px;'
            f'letter-spacing:-.01em;line-height:1.05;color:var(--ink);white-space:nowrap;'
            f'z-index:9">{it["head"].upper()}</div>')
        els.append(("ix%d" % i, tx, iy + 46, tw, 48))
        tp.append(("ix%d" % i, core.INK, tint, 44, True))
        iy += step

    _story_footer(inner, els, tp, brief, True,
                  brief.get("story_cta", "swipe for all of it."))
    html = B.page(W_STORY, H_STORY, "var(--ink)", "".join(inner), grain=False)
    ignore = [(a, b) for a, b in zip(ct, ct[1:])]                        # em-box air
    ignore += [("ixcard%d" % k, part % k) for k in range(len(items))
               for part in ("sw%d", "ixchip%d", "ix%d")]                  # card holds these
    gate = dict(color_pairs=cp, text_pairs=tp, page_bg="var(--ink)", expect_hero=False,
                containers=tuple(card_tags), collision_ignore=ignore)
    return ("s00_cover", html, els, gate)


async def _story_item(brief, it, i, n):
    """One item, told at length, with the same craft layer as the poster (R9).

    R8, AND WHY THIS IS NOT THE POSTER ROW SCALED UP. The first version stacked
    the poster's content from the top of a 1920px frame and left the lower 55%
    empty. The content block is CENTRED in its region, a band is ALWAYS painted
    across the lower third, and the numeral's empty right-hand side - the dead
    quadrant the pixel critique kept naming - now carries the department burst.
    """
    acc = accent(it["dept"])
    ground = core.CREAM
    tint = tint_of(acc)
    inner, els = _story_frame(False, "%02d / %02d" % (i + 1, n))
    tp, cp = [], []
    tp.append(("idx", "#5A5A55", ground, 16, True))

    hw = W_STORY - 2 * M
    body_w = hw - 2 * STORY_CARD_PAD - 2 * CARD_BORDER
    G1, G2 = 46, 40
    region_h = (STORY_BAND_Y - 44) - STORY_TOP

    # THE NUMERAL IS SOLVED, NOT SET: it is the most compressible thing on the
    # slide, so it gives way until the whole stack (numeral, head, body card)
    # fits - exactly as the poster's card solver steps its type down.
    for num_size in STORY_NUM_SIZES:
        nm, hm, bm = await B.measure_text([
            _mt("%02d" % (i + 1), "d", num_size, lh=0.86),
            _mt(it["head"].upper(), "d", STORY_HEAD, max_width=hw, lh=0.98),
            {"text": story_text(it), "font": "e", "size": STORY_BODY, "weight": 500,
             "line_height": 1.42, "max_width": body_w},
        ], W_STORY, H_STORY)
        num_ink = nm["glyph_h"] or nm["h"]
        card_h = bm["ink_h"] + 2 * STORY_CARD_PAD + 2 * CARD_BORDER
        block = num_ink + G1 + hm["ink_h"] + G2 + card_h + CARD_SHADOW
        if block <= region_h:
            break
    else:
        raise BriefError(
            "item %d's story copy does not fit the slide even with the numeral at "
            "its smallest. Shorten `story` (budget %d words) - the slide will not "
            "run its text under the band." % (i + 1, STORY_WORDS))

    y = STORY_TOP + max(0, (region_h - block) // 2)

    num_col = core.on_cream(acc, num_size)
    inner.append(
        f'<div class="measure" data-tag="num" style="position:absolute;top:{y}px;left:{M}px;'
        f'font-family:var(--d);font-weight:900;font-size:{num_size}px;line-height:.86;'
        f'color:{num_col};z-index:9">{i + 1:02d}</div>')
    num_w = nm["text_w"] or nm["w"]
    els.append(("num", M, y, num_w, max(nm["h"], nm["ink_h"])))
    tp.append(("num", num_col, ground, num_size, True))

    # the department burst, in the numeral's empty right-hand side. Sized to the
    # room that is actually there, and dropped rather than squeezed below a floor.
    srot = 8
    room = (W_STORY - M) - (M + num_w) - 40
    S = int(min(STORY_STICKER[0], room / 1.08))
    if S >= STORY_STICKER[1]:
        _, _, sbw, _ = lay.rotated_bbox(0, 0, S, S, srot)
        so = (sbw - S) / 2.0
        sx = int(W_STORY - M - S - so)
        sy = int(y + num_ink / 2 - S / 2)
        cm = await B.measure_text([_mt(it["chip"].upper(), "d", 20, lh=1)], W_STORY, H_STORY)
        stk = _burst_svg([it["chip"].upper()], acc, S, srot, [(it["chip"], cm[0]["text_w"])])
        inner.append(f'<div class="measure" data-tag="dept" style="position:absolute;top:{sy}px;'
                     f'left:{sx}px;width:{S}px;height:{S}px;z-index:12">{stk}</div>')
        els.append(("dept", *lay.rotated_bbox(sx, sy, S, S, srot)))
        cp.append(("dept", acc, ground, True))

    hy = y + num_ink + G1
    inner.append(
        f'<div class="measure" data-tag="head" style="position:absolute;top:{hy}px;left:{M}px;'
        f'width:{hw}px;font-family:var(--d);font-weight:900;font-size:{STORY_HEAD}px;'
        f'line-height:.98;letter-spacing:-.015em;color:var(--ink);z-index:9">'
        f'{it["head"].upper()}</div>')
    els.append(("head", M, hy, hw, hm["ink_h"]))
    tp.append(("head", core.INK, ground, STORY_HEAD, True))

    # the body card: same craft layer as the poster's cards. The text is NESTED
    # in it, so the browser - not a tuple - enforces that it stays inside.
    ky = hy + hm["ink_h"] + G2
    inner.append(
        f'<div class="measure" data-tag="card" style="position:absolute;top:{ky}px;left:{M}px;'
        f'width:{hw}px;height:{card_h}px;background:{tint};border:{CARD_BORDER}px solid var(--ink);'
        f'border-radius:{core.RADII["outer"]}px;box-shadow:8px 8px 0 var(--ink);'
        f'padding:{STORY_CARD_PAD}px;z-index:8">'
        f'<div class="measure" data-tag="line" style="font-family:var(--e);font-weight:500;'
        f'font-size:{STORY_BODY}px;line-height:1.42;color:#2E2E2B">{story_text(it)}</div></div>')
    els.append(("card", M, ky, hw + 8, card_h + 8))
    cp.append(("card", tint, ground, True))
    tp.append(("line", "#2E2E2B", tint, STORY_BODY, False))

    # -- the band (R8). Full bleed, always painted. --------------------------
    if it.get("photo"):
        # the crop window favours the upper frame: centring a letterbox on a
        # portrait photograph lands on the torso (the first render of this slide
        # was a headless body holding a parcel). Faces sit high.
        inner.append(
            f'<div class="measure" data-tag="band" style="position:absolute;top:{STORY_BAND_Y}px;'
            f'left:0;width:{W_STORY}px;height:{STORY_BAND_H}px;z-index:7;overflow:hidden;'
            f'border-top:{CARD_BORDER}px solid var(--ink);border-bottom:{CARD_BORDER}px solid var(--ink)">'
            f'{tex.photo_ink(core.PHOTOS[it["photo"]], "width:100%;height:100%", focus="50% 22%")}'
            f'</div>')
    else:
        plate = core.lit_of(acc)
        on_plate = core.text_on(plate)
        inner.append(
            f'<div class="measure" data-tag="band" style="position:absolute;top:{STORY_BAND_Y}px;'
            f'left:0;width:{W_STORY}px;height:{STORY_BAND_H}px;background:{plate};z-index:7;'
            f'border-top:{CARD_BORDER}px solid var(--ink);border-bottom:{CARD_BORDER}px solid var(--ink);'
            f'display:flex;align-items:center;padding-left:{M}px">'
            f'<span class="measure" data-tag="plate" style="font-family:var(--d);font-weight:900;'
            f'font-size:72px;line-height:.94;letter-spacing:-.02em;color:{on_plate}">'
            f'{brief.get("kicker", "this week at aq").upper()}<br>no. {brief.get("issue", "01")}'
            f'</span></div>')
        els.append(("plate", M, STORY_BAND_Y + 104, W_STORY - 2 * M, 150))
        cp.append(("band", plate, ground, True))
        tp.append(("plate", on_plate, plate, 72, True))
    els.append(("band", 0, STORY_BAND_Y, W_STORY, STORY_BAND_H))

    _story_footer(inner, els, tp, brief, False,
                  it.get("cta") or brief.get("story_cta", "more in the group."))
    html = B.page(W_STORY, H_STORY, "var(--bg)", "".join(inner), grain=False)
    gate = dict(color_pairs=cp, text_pairs=tp, page_bg="var(--bg)", expect_hero=False,
                containers=("band", "card"), bleed_tags=("band",),
                # the numeral's declared box (its overflow extent) reserves a
                # descender digits never paint; the headline sits in that air,
                # 46px clear of the ink.
                collision_ignore=[("num", "head")])
    return ("s%02d_%s" % (i + 1, it["dept"]), html, els, gate)


# ============================================================================
# 3. THE TEXT
# ============================================================================
# WHAT THIS OWNS AND WHAT IT DOES NOT. It owns STRUCTURE: the header, the
# numbering, the sign-off, the handle, the link. It does NOT write sentences:
# VOICE.md is a specification and engine/copy.py does not exist yet, so a
# generator here that invented phrasing would be inventing a voice.
#
# R10: the default is HEADERS ONLY. The poster carries the sentences; the text is
# the table of contents that makes someone open it.


def whatsapp_text(brief):
    """The ONE WhatsApp message that goes out with the poster.

    WhatsApp markup: *bold*, _italic_. No em dashes (VOICE.md 1.1), no emoji
    (1.2), lowercase body (1.4), soft close with an exit (1.12).
    brief["wa_mode"]: "headers" (default, R10) or "full".
    """
    validate_brief(brief)
    items = brief["items"]
    issue = brief.get("issue", "01")
    kicker = brief.get("kicker", "this week at aq")
    full = brief.get("wa_mode", "headers") == "full"

    out = ["*%s · no. %s*" % (kicker.upper(), issue)]
    if brief.get("dateline"):
        out.append("_week of %s_" % brief["dateline"])
    out.append("")

    for i, it in enumerate(items, 1):
        if full:
            out.append("*%d. %s*" % (i, it["head"].lower()))
            out.append(it.get("wa") or it["line"])
            out.append("")
        else:
            out.append("%d. *%s* · _%s_" % (i, it["head"].lower(), it["chip"].lower()))
    if not full:
        out.append("")

    out.append(brief.get("wa_signoff",
                         "the detail on each one is in the poster. if your team did "
                         "something that isn't here, reply and it goes in no. %s."
                         % _next_issue(issue)))
    tail = brief.get("handle", "@ngo.aquaterra")
    if brief.get("site"):
        tail += "  ·  " + brief["site"]
    out.append(tail)
    return "\n".join(out).rstrip() + "\n"


def ig_caption(brief):
    """The caption for the story set / the feed crosspost. Headers, like the
    WhatsApp text (R10): the stories are where the detail lives."""
    validate_brief(brief)
    items = brief["items"]
    issue = brief.get("issue", "01")
    kicker = brief.get("kicker", "this week at aq")

    out = ["%s, no. %s." % (kicker, issue), ""]
    for it in items:
        out.append("· %s: %s" % (it["chip"].lower(), it["head"].lower()))
    out.append("")
    out.append(brief.get("ig_signoff", "the detail on each one is in the stories."))
    if brief.get("site"):
        out.append(brief["site"])
    out.append("")
    out.append(" ".join(brief.get("tags", ["#aquaterra", "#kolkata", "#studentrun"])))
    return "\n".join(out).rstrip() + "\n"


def _next_issue(issue):
    try:
        return "%02d" % (int(issue) + 1)
    except (TypeError, ValueError):
        return "the next one"
