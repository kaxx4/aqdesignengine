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

print(f"\nALL {N} ASSERTIONS PASSED")
