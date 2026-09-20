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
    try:
        os.remove(tmp)
    except OSError:
        pass

    print(f"\nALL {N} ASSERTIONS PASSED")


asyncio.run(main())
