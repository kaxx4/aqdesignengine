"""Self-test for engine/dispatch.py - the DISPATCH internal-roundup format.

Every assertion reproduces something that actually went wrong while issue no. 01
was built (2026-09-22/23), or a rule the person running the series asked for:

  * a spotlight slab + "act on this" stamp ranked one item over four (R3)
  * the WhatsApp text ran to 400 words; the review asked for headers only (R10)
  * the count burst read "THINGS 5" instead of "5 THINGS"
  * an equal row split sliced two-line bodies in half (R6) - the solver must now
    REFUSE an over-full brief by name rather than shrink type silently
  * a four-word mood line passed validation while telling nobody anything; the
    budget guards are what keep the copy honest in both directions
  * brief-level typos (unknown dept, a photo the bank does not have, em dashes)

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_dispatch.py
"""
import asyncio, importlib.util, os, re, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)


def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


D = _load("dispatch")
B = D.B
N = 0


def ok(cond, msg):
    global N
    assert cond, "FAILED: " + msg
    N += 1
    print(f"  ok {N}: {msg}")


def raises(fn, needle):
    try:
        fn()
    except D.BriefError as e:
        return needle in str(e)
    return False


def item(dept="events", chip="events", head="a thing happened",
         line="the events team did a specific thing this week and here is where it lives.", **kw):
    d = {"dept": dept, "chip": chip, "head": head, "line": line}
    d.update(kw)
    return d


def brief(items, **kw):
    b = {"issue": "07", "kicker": "this week at aq", "dateline": "1 oct 2026",
         "tagline": "what's / moving", "site": "ngoaquaterra.com", "items": items}
    b.update(kw)
    return b


GOOD = brief([item(), item("content", "magazine", "blogs is now bigger"),
              item("labs", "labs", "labs is wrapped"),
              item("ops", "website", "the site is coming"),
              item("welfare", "welfare", "a drive went out")], cover_photo="food")

# ---- 1-7: the brief is refused LOUDLY, with the field named -----------------
ok(D.validate_brief(GOOD) is GOOD, "a well-formed brief validates and is returned unchanged")
ok(raises(lambda: D.validate_brief(brief([item(dept="finance")])), "unknown department"),
   "an unknown department is refused - a new team's colour is decided once, on purpose")
ok(raises(lambda: D.validate_brief(brief([item()] * 7)), "Max is 6"),
   "seven items are refused (R2: past six rows nothing reads at thumbnail size)")
ok(raises(lambda: D.validate_brief(brief([item(photo="stock_smile")])), "Real AQ photos only"),
   "a photo the bank does not have is refused rather than rendering an empty <img>")
ok(raises(lambda: D.validate_brief(brief([item(line="word " * 29)])), "budget is 28"),
   "a 29-word poster line is refused by name (R4)")
ok(raises(lambda: D.validate_brief(brief([item(head="one two three four five six")])),
          "budget is 5"),
   "a six-word headline is refused (R4)")
ok(raises(lambda: D.validate_brief(brief([item(line="it moved — somewhere new")])),
          "em/en dash"),
   "an em dash in copy is refused (VOICE.md 1.1)")

# ---- 8-9: colour is semantic ------------------------------------------------
ok(D.accent("events") == D.core.accent_for("events") and D.accent("events") != D.accent("content"),
   "department colour comes from core.accent_for, never an index (R1)")
ok(D.PINK not in {D.accent(d) for d in D.DEPTS},
   "brand pink is owned by no department, so furniture can never read as one (R9)")

# ---- 10-12: the one serif accent word ---------------------------------------
lines = D._mast_lines("what's / moving")
ok(lines[-1][1] == "s" and lines[0][1] == "d",
   "a one-word last tagline line is set in the serif accent")
ok(all(tok == "d" for _, tok, _ in D._mast_lines("what's / on this week")),
   "a MULTI-word last line falls back to display - section 9 allows ONE accent word")
ok(all(tok == "d" for _, tok, _ in D._mast_lines("dispatch")),
   "a single-line tagline has no serif line to spend the allowance on")

# ---- 13-18: the text is headers (R10) ---------------------------------------
LONG = brief([item(line="the long sentence that belongs only on the poster.",
                   wa="the long whatsapp paragraph that should not appear by default."),
              item("labs", "labs", "labs is wrapped")])
wa = D.whatsapp_text(LONG)
ok("a thing happened" in wa and "labs is wrapped" in wa,
   "the WhatsApp text lists every item's headline")
ok("long sentence" not in wa and "long whatsapp paragraph" not in wa,
   "the default WhatsApp text carries NO body copy - headers only (R10)")
ok("long whatsapp paragraph" in D.whatsapp_text(dict(LONG, wa_mode="full")),
   'wa_mode="full" restores the long message for the issue that needs it')
ok(len(wa.split()) < 60, "a two-item headers message stays short (%d words)" % len(wa.split()))
ok("ngoaquaterra.com" in wa and "ngoacqua" not in wa,
   "the site in the text is the brief's, spelled right (issue 01 shipped a misheard one)")
ok(not re.search("[—–]", wa + D.ig_caption(LONG)),
   "neither generated text contains an em or en dash")


async def rendered():
    async with B.session():
        html, els, gate = await D.poster(GOOD)

        # ---- 19-22: every item is equal (R3) --------------------------------
        cards = re.findall(r'data-tag="r\d+card" style="([^"]+)"', html)
        ok(len(cards) == 5, "one card per item")

        def shape(style):          # strip what is SUPPOSED to vary: position + hue
            style = re.sub(r"top:\d+px;", "", style)
            style = re.sub(r"height:\d+px;", "", style)
            return re.sub(r"background:#[0-9A-Fa-f]{6};", "", style)
        ok(len({shape(c) for c in cards}) == 1,
           "every card has the identical craft treatment apart from its hue (R3)")
        ok("spotslab" not in html and "act on this" not in html.lower(),
           "no spotlight slab and no 'act on this' stamp survive in the poster")
        labels = gate["containers"]
        ok(all(("r%dcard" % k) in labels for k in range(5)),
           "each card is declared as a container for what is drawn on it")

        # ---- 23: no photo, no empty frame --------------------------------------
        bare, _, _ = await D.poster(dict(GOOD, cover_photo=None))
        ok('data-tag="photo"' not in bare and 'data-tag="burst"' not in bare,
           "an issue with no photo draws no empty frame and no orphaned burst")

        # ---- 24: the count burst reads number-first ---------------------------
        burst = html[html.index('data-tag="burst"'):]
        burst = burst[:burst.index("</svg>")]
        ok(burst.index(">5<") < burst.index(">THINGS<"),
           'the burst reads "5 THINGS", not "THINGS 5"')

        # ---- 25: the solver REFUSES, it does not shrink silently (R6) --------
        stuffed = brief([item(head="one two three four five", line=("word " * 28).strip())
                         for _ in range(6)])
        try:
            await D.poster(stuffed)
            refused = False
        except D.BriefError as e:
            refused = "CONTENT problem" in str(e)
        ok(refused, "six maximal items are refused by name rather than rendered unreadably")

asyncio.run(rendered())

print(f"\nALL {N} ASSERTIONS PASSED")
