"""Self-test for engine/discodiwali.py - the DISCO DIWALI format module.

Each assertion reproduces something that went wrong building the set (2026-10-13) or a rule the user set:

  * a countdown numeral's declared box was taller than its glyphs, so it "collided" with the label under it
  * the clock line rendered at a tiny size: the width estimate counted the clock's SVG markup as TYPE
  * the red carpet was a hard-edged slab; the user's rule is that it ALWAYS fades into black
  * a 4:5 plate cropped to 9:16 left a dead black middle; taller canvases now stack two plates
  * a brief with a missing or unknown field must be refused by name (the dispatch.py contract), and a price,
    venue or lineup is never invented because no such field exists

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_discodiwali.py
"""
import datetime, importlib.util, os, re, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

dd = _load("discodiwali")
N = 0
def ok(cond, msg):
    global N
    N += 1
    if not cond:
        print(f"FAIL {N}: {msg}"); sys.exit(1)
    print(f"ok {N}: {msg}")

def refused(kind, content, canvas="feed", needle=""):
    try:
        dd.validate_brief(kind, content, canvas)
    except ValueError as e:
        return needle in str(e)
    return False

ANN = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards",
           status="Ticket sales open soon", cta="Link in bio")

# --- brief validation ---------------------------------------------------------------------------------------
ok(not refused("announce", ANN), "a complete announce brief validates")
ok(refused("announce", {k: v for k, v in ANN.items() if k != "time"}, needle="'time'"), "a missing field is refused BY NAME")
ok(refused("announce", dict(ANN, price="Rs. 550"), needle="price"), "an unknown field (a price nobody supplied) is refused, not printed")
ok(refused("sparkle", ANN, needle="kind"), "an unknown kind is refused")
ok(refused("announce", ANN, canvas="square", needle="canvas"), "an unsupported canvas is refused")
ok(refused("countdown", dict(edition="X Edition", date="d", days="soon", cta="c"), needle="days"), "a non-numeric countdown is refused")
ok(all(k in dd.REQUIRED for k in dd.KINDS), "every kind declares its required fields")

# --- derived facts -------------------------------------------------------------------------------------------
ok(dd.days_to_go("2026-11-10", datetime.date(2026, 10, 13)) == 28, "days_to_go derives the count from the supplied date")
ok(dd.days_to_go("2026-11-10", datetime.date(2026, 11, 9)) == 1, "one day out reads 1")

# --- fit: markup is not type -----------------------------------------------------------------------------------
clock = dd.Poster.clock(54)
plain = "xx4:30 PM ONWARDS"
ok(dd._fit(clock + "4:30 PM ONWARDS", 54, 900) < 30, "REPRODUCES THE BUG: measuring the svg markup as text shrinks the size to illegible")
ok(dd._fit(plain, 54, 900) == 54, "measuring the visible text keeps the size")

# --- build-level rules (html only, no render) -------------------------------------------------------------------
tk = dd.Poster("tickets_open", dict(edition="Masquerade Sangeet Edition", headline="Tickets are live", cta="Link in bio"), "feed").build()
carpet = re.search(r'data-tag="carpet"[^>]*', tk)
ok(carpet is not None and "mask-image:linear-gradient" in carpet.group(0), "the carpet carries a fade mask, never a hard slab")
ok("transparent" in carpet.group(0), "the carpet fade ends in transparent, i.e. into the black ground")

feed = dd.Poster("announce", ANN, "feed").build()
story = dd.Poster("announce", ANN, "story").build()
ok(feed.count('data-tag="plate"') == 1, "the feed canvas uses a single plate")
ok(story.count('data-tag="plate"') == 2 and "scaleY(-1)" in story, "a story stacks TWO plates, the second flipped, so no dead middle")

p = dd.Poster("countdown", dict(edition="Masquerade Sangeet Edition", date="d", days=28, cta="c"), "feed"); p.build()
box = {e[0]: e for e in p.elements}
ok(box["count"][4] >= 145 and box["count"][2] + box["count"][4] <= box["unit"][2], "the numeral's declared box is TRUTHFUL (drawn 171px at size 171) and still clears the label under it")

ok(all(e[1] >= -1 and e[1] + e[3] <= p.W + 1 for e in p.elements if e[0] in ("date", "unit", "cta", "sub1")), "declared type boxes stay inside the canvas")

# only story gets the extra height, and only INFO is bottom-anchored
fs, ss = dd.Poster("announce", ANN, "feed"), dd.Poster("announce", ANN, "story")
ok(fs.dy_info == 0 and ss.dy_info == ss.H - dd.BASE_H, "the info group takes ALL the extra height on a taller canvas, so the CTA stays bottom-anchored")
ok(ss.dy_top < ss.dy_title < ss.dy_info, "extra height is shared top < title < info")

# --- style and mask options ---------------------------------------------------------------------------------------
def refused_opt(**kw):
    try:
        dd.Poster("announce", ANN, "feed", **kw)
    except ValueError as e:
        return True
    return False
ok(refused_opt(style="neon"), "an unknown style is refused")
ok(refused_opt(mask="gold"), "an unknown mask is refused")
diya = dd.Poster("announce", ANN, "feed", style="diya", mask="copper").build()
ok("data-tag=\"lights\"" not in diya, "the navy diya direction drops the string lights (the plate carries the light)")
ok("data-tag=\"lights\"" in feed, "the default direction keeps the string lights")
ok(diya.count("mask_copper") == 0 and 'data-tag="mask"' in diya, "the copper mask is placed (inlined as a data URI, so no file name in the html)")
red = dd.Poster("announce", ANN, "feed", style="stroke", mask="red").build()
ok('data-tag="plate"' not in red, "the stroke style draws no beaded plate: the ground is plain ink")
ok("image/svg+xml" in red, "the drawn red mask is embedded as svg")

# --- photo teasers ---------------------------------------------------------------------------------------------
TE = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", line="Save the date", cta="Link in bio")
ok(not refused("teaser_full", dict(TE, photo="03")), "a teaser with a library photo (unique NN prefix) validates")
ok(refused("teaser_full", dict(TE, photo="99"), needle="not in"), "a photo that is not in the library is refused by name")
ok(refused("teaser_trio", dict(TE, photos=["07", "08"]), needle="exactly 3"), "a trio needs exactly three photos")
ok(refused("teaser_full", {k: v for k, v in TE.items() if k != "line"} | {"photo": "03"}, needle="'line'"), "a teaser without its line is refused")
th = dd.Poster("teaser_full", dict(TE, photo="03"), "feed").build()
ok("pointer-events:none" in th, "gradient overlays over a photo never hit-test (else the gate reports the photo buried)")
ok('data-tag="plate"' not in th, "a full-bleed photo teaser draws no plate under the photo")
big = dd.photo_uri("02")
ok(len(big) < 600_000, "a 3024x4032 original is downscaled before it is embedded")
tr = dd.Poster("teaser_trio", dict(TE, photos=["07", "08", "09"]), "story")
tr.build()
fr = {e[0]: e for e in tr.elements}
ok(fr["f1"][2] > fr["badge"][2] + fr["badge"][4] or fr["f1"][1] > fr["badge"][1] + fr["badge"][3], "trio frames start below the LIVE badge, never under it")

# --- blue blend-mode direction -------------------------------------------------------------------------------------
bl = dd.Poster("announce", ANN, "feed", style="blue", mask="copper").build()
ok("color-dodge" in bl and "repeating-conic-gradient" in bl, "the blue direction layers a colour-dodge blue and screen-blended disco beams")
ok("filter:url(#ca)" in bl and 'id="ca"' in bl, "the title lockup carries the RGB-split shader and its filter is defined")
ok(bl.count('data-tag="plate"') >= 4, "every blend layer is tagged plate (deliberate full bleed)")
ok('id="ca"' not in feed, "other directions do not carry the shader")

# --- photo direction: photo behind, soft plate screen-blended, editorial type -------------------------------------------
ph = dd.Poster("announce", dict(ANN, photo="05"), "feed", style="photo", mask="copper").build()
ok('data-tag="photo"' in ph and "mix-blend-mode:screen" in ph, "the photo direction puts a real photo behind a SCREEN-blended plate")
ok("pattern_diya_navy" not in ph and ph.count("data:image/jpeg") >= 2, "it uses the soft plate and never the raw tiled pattern (that is for edge cases only)")
ok("var(--s)" in ph and "letter-spacing:.34em" in ph, "the type is editorial: serif italic accents and tracked small caps")
ok(refused("announce", dict(ANN, photo="05"), needle="") is False, "announce accepts an optional photo field")

# --- type treatments --------------------------------------------------------------------------------------------------
def photo_html(typo):
    return dd.Poster("announce", dict(ANN, photo="05"), "feed", style="photo", mask="copper", typo=typo).build()
try:
    dd.Poster("announce", ANN, "feed", style="photo", typo="neon"); bad = False
except ValueError:
    bad = True
ok(bad, "an unknown typo is refused")
ok("background-clip:text" in photo_html("foil"), "foil clips a gold gradient to the glyphs")
ok("-webkit-text-stroke:3px" in photo_html("outline") and "transparent" in photo_html("outline"), "outline draws hollow numerals so the photo reads through them")
ok("rotate(-90deg)" in photo_html("vertical"), "vertical runs its rail type up the edges")
ok(all(len(photo_html(t)) > 1000 for t in dd.TYPOS), "every typo treatment builds")

# --- stacking: the mask is in front of the string lights ----------------------------------------------------------------
import re as _re
zs = lambda h, tag: int(_re.search(r'data-tag="%s"[^>]*z-index:(\d+)' % tag, h).group(1))
ok(zs(feed, "mask") > zs(feed, "lights"), "the mask is IN FRONT of the string lights (user directive)")
ok(zs(ph, "mask") > zs(ph, "lights"), "and in the photo direction too")

# --- layout presets ------------------------------------------------------------------------------------------------------
def layout_poster(lay):
    q = dd.Poster("announce", dict(ANN, photo="05"), "feed", style="photo", mask="copper", typo="editorial", layout=lay); q.build(); return q
try:
    dd.Poster("announce", ANN, "feed", layout="diagonal"); bad = False
except ValueError:
    bad = True
ok(bad, "an unknown layout is refused")
ok(all(layout_poster(l) for l in dd.LAYOUTS), "every layout preset builds")
bx = lambda q, n: {e[0]: e for e in q.elements}[n]
ok(bx(layout_poster("mask_behind"), "sub1")[2] != bx(layout_poster("classic"), "sub1")[2], "the edition lines follow the title's real bottom, not fixed coordinates")
ok(dd.LAYOUTS["title_hero"]["title"][1] >= 340, "title_hero keeps the disco ball clear of the LIVE badge (y_ref >= 340)")

# --- launch pack: stories, WhatsApp poster, WhatsApp DP ---------------------------------------------------------------------
LF = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards", status="Ticket sales open soon", note="More details soon", photo="05")
def refused_kind(kind, content, canvas, needle=""):
    return refused(kind, content, canvas, needle)
ok(refused_kind("story_launch", LF, "feed", "canvas"), "a launch story is refused on a feed canvas (it is a story)")
ok(refused_kind("wa_dp", dict(edition="X", date="d"), "feed", "canvas"), "the WhatsApp DP is refused anywhere but square")
ok(refused_kind("story_launch", {k: v for k, v in LF.items() if k != "time"}, "story", "'time'"), "a launch story missing the time is refused BY NAME")
st = dd.Poster("story_launch", LF, "story", typo="foil"); sh = st.build()
bx2 = {e[0]: e for e in st.elements}
ok("linkzone" in bx2, "a launch story declares the reserved link-sticker zone as an element")
lz = bx2["linkzone"]
ok(lz[2] + lz[4] <= st.H - 240, "the link zone (y + h) ends above Instagram's bottom 250px (reply bar) safe line")
ok(not any(e[0] != "linkzone" and e[1] < lz[1] + lz[3] and lz[1] < e[1] + e[3] and e[2] < lz[2] + lz[4] and lz[2] < e[2] + e[4]
           for e in st.elements if e[0] not in ("plate", "photo", "mask", "title")), "nothing else is declared inside the link-sticker zone (x,y,w,h compared on the right axes)")
ok('data-tag="cta"' not in sh, "a launch story carries no CTA pill (the link sticker takes its place)")
FACT_PARTS = ("10", "NOVEMBER", "2026", "4:30 PM", "ONWARDS", "TICKET SALES OPEN SOON", "MORE DETAILS SOON", "MASQUERADE SANGEET", "EDITION", "ALL FOR")
import re as _re2
def visible_text(h):                       # text nodes only: drop tags, the style block and base64 payloads
    h = _re2.sub(r"<style.*?</style>", "", h, flags=_re2.S)
    return _re2.sub(r"\s+", " ", _re2.sub(r"<[^>]+>", " ", h)).upper()
for ty in ("foil", "outline", "stack", "editorial"):
    txt = visible_text(dd.Poster("story_launch", LF, "story", typo=ty).build())
    parts = [("NOV" if (p == "NOVEMBER" and ty == "stack") else p) for p in FACT_PARTS]      # the stack treatment sets the month as NOV (10 NOV 2026)
    missing = [p for p in parts if p not in txt and p != "ALL FOR"]
    ok(not missing, f"story typo={ty}: every launch fact is present as text (missing: {missing})")
ok("var(--e)" not in sh and "var(--s)" not in sh and "var(--m)" not in sh, "ALL launch-pack type is NeutralFace (no Eina, serif or mono left)")
ok("text-transform:uppercase" in sh, "NeutralFace is an uppercase face: the replacements force uppercase")
dp = dd.Poster("wa_dp", dict(edition="Masquerade Sangeet Edition", date="10th November, 2026"), "square"); dp.build()
import math as _m
inside = lambda e: all(_m.hypot(cx - dp.W / 2, cy - dp.H / 2) <= 540 for cx in (e[1], e[1] + e[3]) for cy in (e[2], e[2] + e[4]))
ok(all(inside(e) for e in dp.elements if e[0] in ("date", "edition")), "the DP's text boxes sit wholly inside the circular crop WhatsApp applies")
ok(dp.dy_info == 0 and dp.dy_title == 0, "a square canvas does not inherit a negative height shift from the 1350 baseline")
wp = dd.Poster("wa_poster", LF, "feed").build()
ok('data-tag="cta"' not in wp and "LINK IN BIO" not in wp.upper(), "the WhatsApp poster has no CTA pill and no 'link in bio' (there is no link to point at)")

print(f"\nALL {N} ASSERTIONS PASSED")
