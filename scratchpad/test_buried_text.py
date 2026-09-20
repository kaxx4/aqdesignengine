"""Self-test for reconcile.measure_dom's `buried_text` — type that is painted,
laid out, correctly coloured, inside its box, on the canvas, and still invisible
because something opaque is in front of it.

THE BUG (session 10f, agent c1's v1). A body-copy paragraph had no z-index. A
sibling background rectangle had `z-index:1`. In CSS any explicit z-index on a
positioned element paints above `z-index:auto` REGARDLESS of DOM order, so the
opaque rectangle buried the whole paragraph. preflight printed CLEAN, render()'s
auto-gates printed CLEAN, and Playwright's own is_visible() and bounding_box()
both reported it present — because by every DOM measure it WAS present. Only
reading the rendered PNG caught it.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_buried_text.py
"""
import asyncio, importlib.util, os, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)


def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


rec = _load("reconcile")
N = 0


def ok(cond, msg):
    global N
    assert cond, "FAILED: " + msg
    N += 1
    print(f"  ok {N}: {msg}")


W, H = 1080, 1350


def page(inner):
    return ("<!DOCTYPE html><html><head><meta charset='utf-8'></head><body "
            "style='margin:0'><div class='p' style='position:relative;width:%dpx;"
            "height:%dpx;overflow:hidden;background:#F4EFE0'>%s</div></body></html>"
            % (W, H, inner))


# THE EXACT SHAPE OF THE BUG: copy first in DOM order with NO z-index, an opaque
# sibling rectangle after it WITH z-index:1. DOM order says the rect is on top
# anyway — but this stays a faithful reproduction of what c1_v1 actually wrote.
BURIED = page(
    "<div data-tag='copy' style='position:absolute;left:80px;top:400px;width:600px;"
    "height:200px;font:700 28px sans-serif;color:#0A0A0A'>since 2021, one number "
    "keeps climbing</div>"
    "<div data-tag='panel' style='position:absolute;left:60px;top:380px;width:700px;"
    "height:260px;background:#EDE7D4;z-index:1'></div>")

# The same two elements with the copy correctly raised above the panel.
FIXED = page(
    "<div data-tag='copy' style='position:absolute;left:80px;top:400px;width:600px;"
    "height:200px;font:700 28px sans-serif;color:#0A0A0A;z-index:2'>since 2021, one "
    "number keeps climbing</div>"
    "<div data-tag='panel' style='position:absolute;left:60px;top:380px;width:700px;"
    "height:260px;background:#EDE7D4;z-index:1'></div>")

# A decorative div with no text of its own, deliberately behind a card. Must NOT
# fire — things are allowed to sit behind other things; words are not.
DECOR = page(
    "<div data-tag='blob' style='position:absolute;left:100px;top:200px;width:300px;"
    "height:300px;background:#FF4D8C'></div>"
    "<div data-tag='card' style='position:absolute;left:80px;top:180px;width:360px;"
    "height:360px;background:#FFFFFF;z-index:1'></div>")

# Ordinary nested copy: a label inside its own card. The card is on top of the
# page but the label is inside it, so elementFromPoint returns the label.
NESTED = page(
    "<div data-tag='card' style='position:absolute;left:80px;top:180px;width:400px;"
    "height:300px;background:#FFFFFF;z-index:1'>"
    "<div data-tag='label' style='position:absolute;left:24px;top:24px;"
    "font:700 30px sans-serif;color:#0A0A0A'>Classroom notes</div></div>")


async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})

        async def measure(html):
            await pg.set_content(html, wait_until="load")
            return await rec.measure_dom(pg, W, H)

        r = await measure(BURIED)
        buried = r["buried_text"]
        ok(any(t[0] == "copy" for t in buried),
           "the c1_v1 shape is caught: copy with no z-index under a z-index:1 panel")
        rowc = [t for t in buried if t[0] == "copy"][0]
        ok("since 2021" in rowc[1],
           "...and the report quotes the text that is actually lost")
        ok(rowc[2] == "panel",
           "...and names WHAT is on top of it, which is the thing you have to move")

        # every other check must stay quiet — this is a NEW class, not a re-report
        ok(r["clipped"] == [] and r["spilling"] == [] and r["off_canvas"] == [],
           "no other check fires: it is not clipped, not spilling, not off-canvas")

        r = await measure(FIXED)
        ok(r["buried_text"] == [],
           "raising the copy above the panel clears it — the fix is verified, not assumed")

        r = await measure(DECOR)
        ok(r["buried_text"] == [],
           "a TEXTLESS decorative div behind a card does not fire (depth is legal)")

        r = await measure(NESTED)
        ok(r["buried_text"] == [],
           "a label nested inside its own card does not fire (hit-test sees a descendant)")

        # ── THE FALSE POSITIVE THIS CHECK SHIPPED WITH (agent c2, c2_v5) ────
        # v1 used elementFromPoint, which reports GEOMETRIC stacking, not visual
        # coverage. A headline at the house's tight line-height HIT-TESTS ABOVE
        # its own border box: the box below started at y=168 and the browser
        # returned it for a point at y=141. So a small centred label 27px higher
        # was reported buried under a headline that is fully transparent there.
        # Both flagged strings were plainly visible in the PNG.
        #
        # Opacity is the discriminator, and it is the ONLY one that separates
        # this from agent c1's real bug — there the occluder was an opaque
        # cream rectangle. Now the whole stack is walked and only an opaque
        # element counts as blocking.
        TIGHT = page(
            "<div data-tag='kicker' style='position:absolute;top:126px;left:0;right:0;"
            "text-align:center;font:700 22px sans-serif;color:#0A0A0A;z-index:70'>"
            "WELCOME TO THE</div>"
            "<div data-tag='headline' style='position:absolute;top:168px;left:40px;"
            "width:1000px;font:900 130px sans-serif;line-height:.78;color:#0A0A0A'>"
            "MONSOON READING CAMP</div>")
        r = await measure(TIGHT)
        ok(not any(t[0] == "kicker" for t in r["buried_text"]),
           "a kicker above a tight-line-height headline is NOT buried (the c2_v5 "
           "false positive: the headline hit-tests above its box but is transparent)")

        # PARTIAL BURIAL (session 10f, g2_v6). The check required EVERY sampled point
        # to be covered, so a plate whose label had its bottom half sliced off by an
        # overlapping sibling passed with 2 of 5 points clear — and shipped, with
        # "SINCE 2021" cut through the middle of its letters. You cannot read the top
        # half of a word.
        HALF = page(
            "<div data-tag='label' style='position:absolute;left:100px;top:200px;"
            "width:500px;height:100px;font:900 64px sans-serif;color:#0A0A0A'>"
            "SINCE 2021</div>"
            "<div data-tag='plate' style='position:absolute;left:60px;top:248px;"
            "width:700px;height:400px;background:#FFC700;z-index:5'></div>")
        r = await measure(HALF)
        ok(any(t[0] == "label" for t in r["buried_text"]),
           "a label with its bottom half covered by a plate IS reported (g2_v6)")

        # the AQ move this must NOT flag: a sticker tucked over a headline's corner
        TUCK = page(
            "<div data-tag='head' style='position:absolute;left:100px;top:200px;"
            "width:800px;height:200px;font:900 90px sans-serif;color:#0A0A0A'>"
            "SHOWING UP</div>"
            "<div data-tag='badge' style='position:absolute;left:820px;top:180px;"
            "width:140px;height:140px;border-radius:50%;background:#FF4D8C;"
            "z-index:5'></div>")
        r = await measure(TUCK)
        ok(not any(t[0] == "head" for t in r["buried_text"]),
           "...while a sticker tucked over one corner is a deliberate tuck, not a cut")

        # ...and a TRANSPARENT box genuinely on top must not bury anything either
        GLASS = page(
            "<div data-tag='copy' style='position:absolute;left:80px;top:400px;"
            "width:600px;height:200px;font:700 28px sans-serif;color:#0A0A0A'>"
            "still perfectly readable</div>"
            "<div data-tag='glass' style='position:absolute;left:60px;top:380px;"
            "width:700px;height:260px;background:rgba(0,0,0,0);z-index:9'></div>")
        r = await measure(GLASS)
        ok(r["buried_text"] == [],
           "a fully transparent overlay does not bury the text under it")

        # but a MOSTLY-opaque one does — this is the line the check draws
        SCRIM = page(
            "<div data-tag='copy' style='position:absolute;left:80px;top:400px;"
            "width:600px;height:200px;font:700 28px sans-serif;color:#0A0A0A'>"
            "swallowed by the scrim</div>"
            "<div data-tag='scrim' style='position:absolute;left:60px;top:380px;"
            "width:700px;height:260px;background:rgba(10,10,10,0.97);z-index:9'></div>")
        r = await measure(SCRIM)
        ok(any(t[0] == "copy" for t in r["buried_text"]),
           "...while a 0.97-alpha scrim over the same copy IS reported")

        await b.close()

    # ── THE TWO OVERLAP CHECKERS MUST COOPERATE (session 10f, agent c3) ──────
    # layout.collision_check takes collision_ignore for by-design overlaps. But
    # build.render ALSO auto-runs audit.py's DOM overlap check, which had its own
    # closed SKIP_PAIRS vocabulary baked into that file and reachable by no caller.
    # So a script could silence one report and the other kept printing the same five
    # overlaps on every render. The only thing that actually worked was DOM
    # parent/child nesting, found by reading engine source after the documented
    # parameter appeared to do nothing. A gate nobody can silence is a gate everybody
    # learns to scroll past.
    B = _load("build")
    inner = ('<div class="measure" data-tag="word" style="position:absolute;left:120px;'
             'top:400px;width:700px;height:200px;background:#1B8A5A"></div>'
             '<div class="measure" data-tag="sticker" style="position:absolute;left:300px;'
             'top:450px;width:160px;height:160px;background:#FF4D8C"></div>')
    html2 = B.page(W, H, "var(--bg)", inner, grain=False)
    els = [("word", 120, 400, 700, 200), ("sticker", 300, 450, 160, 160)]
    tmp = os.path.join(os.environ.get("TEMP", "."), "_aq_overlap.png")

    import io as _io, contextlib as _ctx
    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        await B.render(html2, tmp, W, H, elements=els)
    undeclared = buf.getvalue()
    ok("OVERLAP word x sticker" in undeclared,
       "an undeclared overlap is reported by the DOM audit (it is a real report)")

    buf = _io.StringIO()
    with _ctx.redirect_stdout(buf):
        await B.render(html2, tmp, W, H, elements=els,
                       collision_ignore={("word", "sticker")})
    declared = buf.getvalue()
    ok("OVERLAP word x sticker" not in declared,
       "ONE collision_ignore declaration now silences the DOM audit too")
    ok("ISSUES" not in declared and "CLEAN" in declared,
       "...and the render reports clean rather than contradicting its own preflight")
    # ── INVISIBLE FILL, MEASURED (session 10f, agents c3 and g3) ────────────
    # layout.same_as_bg_scan compares every declared background against the PAGE
    # ground and called itself zero-false-positive. It is not: a cream badge on a
    # full-bleed teal panel is plainly visible and got "FILL SAME AS PAGE BG" on
    # EVERY render. Two independent agents reported it, which makes it a spec
    # defect — a static scan cannot know what is behind an element, and most AQ
    # posters layer. The browser knows exactly.
    from playwright.async_api import async_playwright as _apw
    async with _apw() as p2:
        b2 = await p2.chromium.launch()
        pg2 = await b2.new_page(viewport={"width": W, "height": H})

        async def fills(inner):
            await pg2.set_content(page(inner), wait_until="load")
            return (await rec.measure_dom(pg2, W, H))["invisible_fill"]

        visible = await fills(
            "<div data-tag='panel' style='position:absolute;inset:0;"
            "background:#0E7C86'></div>"
            "<div data-tag='badge' style='position:absolute;left:100px;top:300px;"
            "width:300px;height:120px;background:#F4EFE0'></div>")
        ok(not any(t[0] == "badge" for t in visible),
           "a cream badge on a full-bleed TEAL panel is NOT flagged (the c3/g3 false positive)")

        gone = await fills(
            "<div data-tag='badge' style='position:absolute;left:100px;top:300px;"
            "width:300px;height:120px;background:#F4EFE0'></div>")
        ok(any(t[0] == "badge" for t in gone),
           "...while a cream badge on the CREAM page still IS — the real bug survives")
        _row = [t for t in gone if t[0] == "badge"][0]
        ok(_row[3] and _row[4] < 18,
           "...and the report names what is painted behind it, with the measured distance")

        # a translucent fill is a deliberate tint, not an invisible shape
        tinted = await fills(
            "<div data-tag='wash' style='position:absolute;left:100px;top:300px;"
            "width:300px;height:120px;background:rgba(244,239,224,0.4)'></div>")
        ok(not any(t[0] == "wash" for t in tinted),
           "a translucent fill over the same colour is a tint, not a vanished shape")

        await b2.close()

    # ── render() MUST ACTUALLY PASS THE HTML TO PREFLIGHT (agent g1) ─────────
    # It hardcoded html=None, so css_var_check, img_src_check, invisible_craft_scan,
    # wash_scan and double_rotation_scan never ran through the documented convenience
    # path no matter what the caller passed — while §6 claimed this one call was the
    # whole gate. Found by reading build.py after the agent's own manual scans caught
    # things render() had just reported clean.
    buf3 = _io.StringIO()
    with _ctx.redirect_stdout(buf3):
        await B.render(
            B.page(W, H, "var(--bg)",
                   '<div data-tag="a" style="position:absolute;left:100px;top:200px;'
                   'width:200px;height:100px;color:var(--typo)">x</div>', grain=False),
            tmp, W, H, elements=[("a", 100, 200, 200, 100)])
    ok("--typo" in buf3.getvalue(),
       "an undefined css var reaches preflight THROUGH render (html is no longer None)")
    ok(buf3.getvalue().count("--typo") == 1,
       "...and is reported exactly once, not by two checkers at once")
    try:
        os.remove(tmp)
    except OSError:
        pass

    try:
        os.remove(tmp)
    except OSError:
        pass

    print(f"\nALL {N} ASSERTIONS PASSED")


asyncio.run(main())
