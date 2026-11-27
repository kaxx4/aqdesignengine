"""Self-test for engine/shikshaq.py: the Shikshaq design language as an engine format module.

Every assertion reproduces something that actually went wrong while the language was being learned
and built (2026-11-27), or a rule the site itself states:

  * the Node addon's copy of the tokens had DRIFTED from the site (old text ramp, old orange-deep);
    verify_tokens() must catch a drift, so the test also breaks a token on purpose
  * a page that was 425px wide in a 390px viewport (a scroller inside a grid cell, no min-width:0)
  * white-ish type on a pale card, an em dash, a 38px "button", a mascot landing on a headline
  * a numbered heading's ordinal reported as colliding with its line (a padded BLOCK is not text)
  * the site's own heavy-orange-on-bone payoff measures 2.42:1: it passes ONLY when declared
  * counts that disagree between surfaces (655 vs 661) are recorded, not silently picked

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_shikshaq.py
"""
import asyncio, datetime, importlib.util, os, subprocess, sys

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)


def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


sk = _load("shikshaq")
N = 0


def ok(cond, msg):
    global N
    assert cond, "FAILED: " + msg
    N += 1
    print(f"  ok {N}: {msg}")


# ── tokens: the language must equal the site, and the check must be able to FAIL ────────────
ok(sk.verify_tokens() == [], "every token recomputes from the vendored index.css / subject-palette.ts")
saved = sk.C["page"]
sk.C["page"] = "#FFFFFF"
drift = sk.verify_tokens()
sk.C["page"] = saved
ok(any(d.startswith("page:") for d in drift), "verify_tokens() NAMES a drifted token (a white page is caught)")
saved = sk.C["text2"]
sk.C["text2"] = "#7B736B"   # the pre-2026-11-06 ramp the Node addon still carried
ok(any(d.startswith("text2:") for d in sk.verify_tokens()), "the OLD warm text ramp is caught as drift")
sk.C["text2"] = saved
ok(sk.C["page"] == "#F9F5F1" and sk.C["card"] == "#FCFAF7", "ground is warm bone, not white")
ok(sk.contrast(sk.C["page"], sk.C["card"]) < 1.1, "page and card are ~1.0x apart: separation is by fill seam, not contrast")
ok(sk.contrast(sk.C["orange"], sk.C["ink"]) > 6.4, "ink on orange measures above 6.4:1")
ok(sk.contrast(sk.C["orange"], sk.C["white"]) < 2.6, "white on orange measures 2.5:1, which is why the site moved to ink")
ok(sk.text_on(sk.C["orange"]) == sk.C["ink"] and sk.text_on(sk.C["indigo"]) == sk.C["white"], "text_on() MEASURES: ink on orange, white on indigo")
ok(sk.MODES["teachers"]["on"] == sk.C["ink"] and sk.MODES["papers"]["on"] == sk.C["white"], "MODES carry the right text colour per mode")

# ── the subject generator is the site's, byte for byte ─────────────────────────────────────
WANT = {"maths": ("#FCECDE", "#F2A15A", "#604024", "#6F553E"), "science": ("#E3F7EC", "#34B268", "#24603D", "#3E6F53"),
        "english": ("#E5F5F5", "#46B9B9", "#246060", "#3E6F6F"), "commerce": ("#E2EAF8", "#4775D1", "#243860", "#3E4F6F"),
        "computer": ("#F0E4F6", "#9F53C6", "#4C2460", "#5F3E6F"), "hindi": ("#F9E2E2", "#D74242", "#602424", "#6F3E3E"),
        "history": ("#F7EFE3", "#C68B39", "#604724", "#6F5B3E"), "geography": ("#E4F6F0", "#39AC86", "#24604C", "#3E6F5F")}
for fam, want in WANT.items():
    p = sk.palette_from_seed(sk.SUBJECT_SEEDS[fam])
    ok((p["tint"], p["solid"], p["text"], p["meta"]) == want, f"palette {fam}: tint/solid/text/meta match the live site")
ok(sk.subject_family("Physics,Chemistry,Biology") == "science", "a comma combo resolves on its FIRST member")
ok(sk.subject_family("Computer Science") == "computer", "'Computer Science' is computer, not science (keyword order)")
ok(sk.subject_family("Accounts") == "commerce" and sk.subject_family("Mathematics") == "maths", "aliases resolve (Accounts, Mathematics)")
ok(sk.subject_family("History & Civics") == "history", "ampersand is normalised ('History & Civics')")
ok(sk.subject_family("Drawing & Painting") is None and sk.subject_palette("Drawing & Painting") == sk.FALLBACK_PALETTE, "an unknown subject gets the neutral fallback, never a guess")
# The spec table marks science "dark: yes" but the SITE'S CODE measures: white on science green is 2.72:1, ink is 6.05.
# A hand-typed white tile for Chemistry (done in the first demo build) is therefore wrong; the generator is right.
ok(sk.palette_from_seed(sk.SUBJECT_SEEDS["science"])["badge"] == sk.C["ink"], "badge text on science green is INK (white measures 2.72:1), whatever the spec's dark flag says")
ok(sk.palette_from_seed(sk.SUBJECT_SEEDS["maths"])["badge"] == sk.C["ink"], "badge text on maths orange is ink (white would be 2.1:1)")
ok(sk.palette_from_seed(sk.SUBJECT_SEEDS["commerce"])["badge"] == sk.C["white"], "commerce blue takes white: ink measures only 3.72:1, the failure the site's comment records")
ok(sk.palette_from_key("ICSE Maths X") == sk.palette_from_key("ICSE Maths X"), "palette_from_key is stable across calls")
ok(sk.palette_from_key("") == sk.FALLBACK_PALETTE, "palette_from_key of nothing is the fallback")

# ── facts + copy gate ───────────────────────────────────────────────────────────────────────
F = sk.FACTS
ok(F["teachers"] == 157 and F["papers"] == 655 and F["commission"] == 0, "facts carry the figures read off the live data")
ok(len(F["known_inconsistencies"]) >= 1 and "661" in F["known_inconsistencies"][0], "the 655-vs-661 disagreement between surfaces is RECORDED")
e, _ = sk.copy_gate(["655 board papers.", "Free to read."]); ok(e == [], "a number that IS a fact passes")
e, _ = sk.copy_gate(["700 board papers."]); ok(any("does not trace" in x for x in e), "an invented number fails")
e, _ = sk.copy_gate(["Class 10 Maths", "ICSE 2026"]); ok(e == [], "a class numeral in context and a year pass")
e, _ = sk.copy_gate(["Free to read — always"]); ok(any("dash" in x for x in e), "an em dash fails (site rule)")
e, _ = sk.copy_gate(["Free – always"]); ok(any("dash" in x for x in e), "an en dash fails too")
e, _ = sk.copy_gate(["Trusted by thousands of parents"]); ok(len(e) >= 1, "unsourced social proof fails")
e, _ = sk.copy_gate(["The best teacher in Kolkata"]); ok(any("superlative" in x for x in e), "an unprovable superlative fails")
_, w = sk.copy_gate(["ok"], today=datetime.date(2027, 3, 1)); ok(any("days old" in x for x in w), "facts older than 14 days WARN")
_, w = sk.copy_gate(["ok"], today=datetime.date(2026, 11, 28)); ok(w == [], "fresh facts do not warn")

# ── builders refuse what the language forbids ───────────────────────────────────────────────
def raises(fn):
    try:
        fn()
    except sk.ShikshaqError:
        return True
    return False

ok(raises(lambda: sk.sticker("x", tilt=15)), "a sticker tilted beyond 9 degrees is refused")
ok(raises(lambda: sk.blob("angry")), "an unknown blob mood is refused")
ok(raises(lambda: sk.doc("x", kind="poster")), "a poster doc without W and H is refused")
ok("<circle" in sk.blob("great") and "<path d=\"M8 92" in sk.blob("meh"), "blob 'great' is a circle, the others are arches")
ok(set(sk.BLOB_USE) == {"rough", "meh", "fine", "good", "great"}, "every blob mood has a documented use")
ok("filter:brightness(0) invert(1)" in sk.logo(True) and "filter" not in sk.logo(False), "the logo inverts to white on dark and is never recoloured otherwise")
ok(sk.PILLAR_MODE["papers"] == "papers" and sk.PILLAR_MODE["teachers"] == "teachers", "mode is semantic per pillar, not a rotation")

# ── assets are vendored, so the engine never reaches into the Shikshaq repo ─────────────────
for rel in ("fonts/archivo-latin.woff2", "fonts/geist-latin.woff2", "logo.svg", "source/index.css",
            "source/tailwind.config.ts", "source/subject-palette.ts", "source/button.tsx", "source/chip.tsx"):
    ok(os.path.exists(os.path.join(sk.ASSETS, rel)), f"vendored: {rel}")
ok(os.path.exists("brain/shikshaq_source/DESIGN_SYSTEM.md") and os.path.exists("brain/shikshaq_source/VISUAL_LANGUAGE.md"), "the site's design docs are vendored")
ok(len([f for f in os.listdir("training_samples/shikshaq") if f.endswith(".jpg")]) >= 30, "reference screens are vendored (training_samples/shikshaq)")
ok("font-stretch:62% 125%" in sk.font_css() and "base64," in sk.font_css(), "fonts are EMBEDDED with the Archivo width axis, no network")

# ── the GATE: each fixture is a bug that really shipped, run through a real browser ─────────
def page(body, extra=""):
    return sk.doc(body, kind="page", extra_css=extra)

def poster(body, W=1080, H=600):
    return sk.doc(body, kind="poster", W=W, H=H)

async def gate_tests():
    out = {}
    async with sk.session() as s:
        async def g(key, html, W, H, kind):
            r = await s.render(html, f"out/shikshaq/_test_{key}.png", W, H, kind=kind, name=f"test:{key}")
            out[key] = r
        # a clean poster
        await g("clean", poster('<div style="padding:60px"><h1 style="font-size:90px">Free to read.</h1><p style="font-size:30px">655 papers</p></div>'), 1080, 600, "poster")
        # S9: 425px page. A scroller inside a grid cell without min-width:0 forces the column open.
        chips = "".join(f'<span class="chip" data-tap style="flex:none">Chip number {i}</span>' for i in range(12))
        grid = '<div style="display:grid;grid-template-columns:1fr"><div><div style="display:flex;gap:8px;overflow:auto">%s</div></div></div>' % chips
        await g("overflow", page(grid), 390, 844, "page")
        await g("overflow_fixed", page(grid.replace("<div><div style", '<div style="min-width:0"><div style', 1)), 390, 844, "page")
        # S6: white-ish type on a pale lavender card (1.4:1)
        await g("lowcontrast", page('<section class="panel lav"><div class="wrap"><p style="color:#fff;font-size:20px">Nobody can read this</p></div></section>'), 390, 844, "page")
        # S8: a dash in visible text
        await g("dash", page('<section class="panel bone"><div class="wrap"><p>Free to read — always</p></div></section>'), 390, 844, "page")
        # 44px targets
        await g("tap", page('<section class="panel bone"><div class="wrap"><span class="count" data-tap>38px chip</span></div></section>'), 390, 844, "page")
        # art on text
        await g("art", poster('<div style="padding:60px;position:relative"><h1 style="font-size:90px;position:relative">Read it today.</h1>'
                              '<div style="position:absolute;left:200px;top:40px">%s</div></div>' % sk.mascot("orange", cls="", size=180)), 1080, 600, "poster")
        # S10 seams: two indigo panels touching; and orange-indigo-orange (two seams)
        ind = '<section class="panel ind" data-fill="indigo"><div class="wrap"><p>One</p></div></section>'
        org = '<section class="panel org" data-fill="orange"><div class="wrap"><p>Two</p></div></section>'
        await g("samehue", page(ind + ind), 390, 844, "page")
        await g("twoseams", page(org + ind + org), 390, 844, "page")
        await g("oneseam", page(ind + org), 390, 844, "page")
        # text sliced by an overflow:hidden parent, and the declared crop
        sliced = '<div style="width:300px;height:30px;overflow:hidden"><p style="margin-top:14px;font-size:40px;white-space:nowrap">Sliced headline</p></div>'
        await g("clipped", page('<div class="wrap">%s</div>' % sliced), 390, 844, "page")
        await g("cropped", page('<div class="wrap">%s</div>' % sliced.replace('<p ', '<p data-crop ')), 390, 844, "page")
        # the site's heavy orange on bone: undeclared fails, declared at display size is INFO, declared small still fails
        big = '<section class="panel bone"><div class="wrap"><h1 style="font-size:66px;font-weight:800;color:var(--orange)"%s>Read it today.</h1></div></section>'
        await g("accent_undeclared", page(big % ""), 390, 844, "page")
        await g("accent_declared", page(big % " data-accent-display"), 390, 844, "page")
        small = '<section class="panel bone"><div class="wrap"><p style="font-size:20px;font-weight:800;color:var(--orange)" data-accent-display>Small orange</p></div></section>'
        await g("accent_small", page(small), 390, 844, "page")
        # no fonts: a bare document that never embeds Archivo/Geist
        await g("nofont", "<!doctype html><body><p style='font-size:30px'>hello</p></body>", 390, 400, "page")
        # the padded-block ordinal must NOT read as a collision with its own line
        await g("numbered", page('<section class="panel bone"><div class="wrap">%s</div></section>' % sk.numbered_heading("02", "Or go straight", "to the subject")), 390, 844, "page")
        # the two worked examples must come out clean at both sizes
        ex = _load_example("shik_landing_example")
        a, b = await ex.main()
        out["landing_m"], out["landing_d"] = a, b
    return out

def _load_example(name):
    s = importlib.util.spec_from_file_location(name, os.path.join("scratchpad", name + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

R = asyncio.run(gate_tests())
has = lambda r, k: any(k in m for m in r.hard)
ok(R["clean"].clean, "a plain, correct poster reports CLEAN")
ok(has(R["overflow"], "OVERFLOW-X") and "min-width:0" in " ".join(R["overflow"].hard), "S9: the 425px-page bug is caught and the message names the fix")
ok(R["overflow_fixed"].clean, "S9: the same page with min-width:0 on the grid cell is CLEAN")
ok(has(R["lowcontrast"], "CONTRAST"), "S6: near-white type on the lavender card fails on measured contrast")
ok(has(R["dash"], "DASH"), "S8: an em dash in visible text is a hard failure")
ok(has(R["tap"], "TAP-TARGET"), "a 38px element declared interactive fails the 44px floor")
ok(has(R["art"], "ART-ON-TEXT"), "a mascot landing on a headline is caught (art is not text, so text-vs-text missed it)")
ok(has(R["samehue"], "SAME-HUE"), "S10: two indigo panels touching is a hard failure")
ok(has(R["twoseams"], "SATURATED-SEAMS"), "S10: two orange/indigo seams is a hard failure")
ok(R["oneseam"].clean and any("one orange/indigo seam" in m for m in R["oneseam"].info), "S10: ONE seam (the live home's) is allowed and reported")
ok(has(R["clipped"], "CLIPPED"), "text sliced by an overflow:hidden parent is caught")
ok(R["cropped"].clean, "the same slice declared with data-crop is a deliberate crop")
ok(has(R["accent_undeclared"], "CONTRAST"), "heavy orange on bone FAILS when it is not declared")
ok(R["accent_declared"].clean and any("ACCENT-DISPLAY" in m for m in R["accent_declared"].info), "declared at display size it passes, and is REPORTED every time")
ok(has(R["accent_small"], "CONTRAST"), "the accent-display exception does not stretch down to 20px type")
ok(has(R["nofont"], "FONT-FALLBACK"), "a document that never embeds Archivo/Geist fails (every word would be in a fallback face)")
ok(R["numbered"].clean and not any("COLLISION" in m for m in R["numbered"].hard), "a numbered heading's ordinal does not collide with its own line (glyph boxes, not block boxes)")
ok(R["landing_m"].clean and R["landing_d"].clean, "the landing-page worked example is CLEAN at 390 and 1280")

# ── the poster example and the scaffolds must run clean, as shipped ─────────────────────────
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return r.returncode, r.stdout + r.stderr

rc, outp = run([sys.executable, "scratchpad/shik_poster_example.py"])
ok(rc == 0 and outp.strip().endswith("CLEAN"), "the poster worked example runs and reports CLEAN")
for kind in ("poster", "page"):
    rc, outp = run([sys.executable, "engine/shikshaq.py", "scaffold", kind, "_selftest_" + kind])
    ok(rc == 0 and os.path.exists(f"scratchpad/shik__selftest_{kind}.py"), f"scaffold {kind} writes a starter")
    rc, outp = run([sys.executable, f"scratchpad/shik__selftest_{kind}.py"])
    ok(rc == 0 and "HARD" not in outp.replace("0 HARD", ""), f"the scaffolded {kind} runs and passes its own gate as shipped")
    os.remove(f"scratchpad/shik__selftest_{kind}.py")
rc, outp = run([sys.executable, "engine/shikshaq.py", "selftest"])
ok(rc == 0, "the CLI selftest agrees with the module")

print(f"\nALL {N} ASSERTIONS PASSED")
