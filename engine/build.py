"""AQ ENGINE — build: the generator.

A piece is a SPEC (a dict): canvas + a list of bands + optional per-piece feature flags.
NOTHING is enforced. Dividers, doodles, fillers, framing, background geometry are all
OPTIONAL and chosen per piece. Variety = different choices, including leaving things OUT.
(See ENGINE.md for the decision menu and DECISIONS.md for standing rulings.)

Pipeline:  spec -> html_from_spec() -> render_and_audit()  (audit is the gate)
"""
import asyncio, importlib.util, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(HERE, name+".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = _load("core"); rhythm = _load("rhythm"); dd = _load("doodles"); audit = _load("audit")
layout = _load("layout"); reconcile = _load("reconcile")

M = 64; COLS = 6; GUT = 20
def _colw(W): return (W-2*M - GUT*(COLS-1))/COLS
def colspan(W,n): return n*_colw(W)+(n-1)*GUT

# ---------- optional element helpers (used only when a spec asks for them) ----------
def logo(dark=False, x=M, y=56):
    sh = "filter:drop-shadow(0 2px 8px rgba(0,0,0,.6));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:{rhythm.snap(y)}px;left:{x}px;height:32px;z-index:20;{sh}">'

def eyebrow(txt, color, y):
    return (f'<div class="measure" data-tag="eyebrow" style="position:absolute;top:{rhythm.snap(y)}px;left:{M}px;'
            f'font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;text-transform:uppercase;'
            f'color:{color};z-index:6;display:flex;align-items:center;gap:10px">'
            f'<span style="width:12px;height:12px;border-radius:50%;background:{color}"></span>{txt}</div>')

def kicker_tr(txt, color="var(--ink3)"):
    return (f'<span style="position:absolute;top:{rhythm.snap(62)}px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:{color};z-index:20">{txt}</span>')

def cta(txt, dark=False):
    c = "#fff" if dark else "var(--ink3)"
    return (f'<span style="position:absolute;bottom:{rhythm.snap(56)}px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:15px;letter-spacing:.08em;color:{c};z-index:20">@ngo.aquaterra {txt}</span>')

def chip(t,bg,fg="#0A0A0A",rot=0):
    return (f'<span class="measure" data-tag="chip" style="display:inline-block;background:{bg};color:{fg};'
            f'font-family:var(--e);font-weight:600;font-size:21px;padding:11px 20px;border-radius:999px;'
            f'border:3px solid var(--ink);box-shadow:4px 4px 0 var(--ink);transform:rotate({rot}deg);white-space:nowrap">{t}</span>')

def rule(W,y,color,opacity=.3):   # OPTIONAL divider — use only when the piece wants it
    return f'<div style="position:absolute;top:{rhythm.snap(y)}px;left:{M}px;width:{colspan(W,6)}px;height:3px;background:{color};opacity:{opacity};z-index:3"></div>'

def doodle(fn,y,x,size,**kw):     # OPTIONAL — place only in measured free zones
    return f'<div class="dood measure" data-tag="doodle" style="position:absolute;top:{rhythm.snap(y)}px;left:{round(x)}px;width:{size}px;height:{size}px">{fn(**kw)}</div>'

def bggeo(shapes):                # OPTIONAL faint background geometry (z-index 1)
    out=""
    for kind,x,y,d,col,op in shapes:
        if kind=="circle": out+=f'<div style="position:absolute;top:{y}px;left:{x}px;width:{d}px;height:{d}px;border-radius:50%;background:{col};opacity:{op};z-index:1"></div>'
        elif kind=="ring": out+=f'<div style="position:absolute;top:{y}px;left:{x}px;width:{d}px;height:{d}px;border-radius:50%;border:14px solid {col};opacity:{op};z-index:1"></div>'
        elif kind=="square": out+=f'<div style="position:absolute;top:{y}px;left:{x}px;width:{d}px;height:{d}px;background:{col};opacity:{op};z-index:1;transform:rotate(12deg)"></div>'
    return out

# ---------- the frame ----------
def page(W,H,bg,inner,grain=True):
    g = f'.p::after{{content:"";position:absolute;inset:0;{core.GRAIN};mix-blend-mode:multiply;pointer-events:none;z-index:2}}' if grain else ''
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{core.FONTS}{core.ROOT}'
            f'*{{margin:0;box-sizing:border-box}}.dood{{position:absolute;z-index:4}}'
            f'.p{{width:{W}px;height:{H}px;background:{bg};position:relative;overflow:hidden;font-family:var(--e)}}{g}</style></head>'
            f'<body><div class="p">{inner}</div></body></html>')

# ════════════════════════════════════════════════════════════════════════════
# RENDER SESSION — one browser, many posters  (session 10)
# ════════════════════════════════════════════════════════════════════════════
# Measured before this existed: 16.81s PER POSTER. The browser work is only
# ~1.1s of that. The rest was structural waste, all of it repeated per render:
#   * audit.audit() cold-started its OWN chromium, then render started a second
#   * 1200ms + 1500ms of blind wait_for_timeout() "for fonts"
#   * 1.3 MB of base64 @font-face re-parsed from scratch every document
# A session keeps one browser and one page per viewport alive, so a batch pays
# the cold start ONCE and each extra poster costs about a second. Nothing about
# a piece's appearance changes — this is purely how many times we boot chromium.
#
# Use it whenever you render more than one thing:
#     async with B.session():
#         for spec in specs:
#             await B.render(spec.html, spec.out, W, H)
# render() still works standalone; with no session open it opens a private one
# for that single call, so every existing bespoke script keeps working unchanged.

class RenderSession:
    def __init__(self, scale=2):
        self.scale = scale
        self._pw = None; self._browser = None; self._pages = {}

    async def start(self):
        from playwright.async_api import async_playwright
        self._pw = await async_playwright().start()
        self._browser = await self._pw.chromium.launch()
        return self

    async def page(self, W, H):
        """One reused page per (viewport, scale). Reusing the page is what keeps
        the embedded fonts in the renderer's cache between posters."""
        key = (W, H, self.scale)
        if key not in self._pages:
            self._pages[key] = await self._browser.new_page(
                viewport={"width": W, "height": H}, device_scale_factor=self.scale)
        return self._pages[key]

    async def close(self):
        try:
            if self._browser: await self._browser.close()
        finally:
            if self._pw: await self._pw.stop()
            self._pw = None; self._browser = None; self._pages = {}

_SESSION = None

class session:
    """`async with B.session():` — hold one browser open across many renders."""
    def __init__(self, scale=2): self.scale = scale; self._owned = False
    async def __aenter__(self):
        global _SESSION
        if _SESSION is None:
            _SESSION = await RenderSession(self.scale).start(); self._owned = True
        return _SESSION
    async def __aexit__(self, *exc):
        global _SESSION
        if self._owned and _SESSION is not None:
            await _SESSION.close(); _SESSION = None
        return False

# Deterministic readiness, replacing the two blind sleeps. We wait for the thing
# we actually care about — fonts parsed, images decoded, two frames painted —
# rather than guessing 1500ms and hoping it was enough on a slow machine (or
# burning 1400ms of it on a fast one).
_SETTLE_JS = """async () => {
  await document.fonts.ready;
  await Promise.all([...document.images]
    .filter(i => !i.complete)
    .map(i => new Promise(r => { i.onload = i.onerror = r; })));
  await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
}"""

async def _settle(pg):
    await pg.evaluate(_SETTLE_JS)

# ---------- render + audit gate ----------
async def render(html, out_png, W, H, elements=None, color_pairs=None, page_bg=None,
                 expect_hero=False, collision_ignore=frozenset(), containers=(),
                 text_pairs=None, cascade_stacks=None, reading_order=None,
                 contains=None, occlusion=None, bleed_tags=None, crop_tags=(),
                 auto_nudge=False):
    """Render + gate. Always: playwright screenshot + audit.py (DOM) + css_var_check (auto,
    zero false positives). OPTIONAL: pass `elements` (and optionally color_pairs/page_bg/
    expect_hero) and render also runs the full layout.preflight static gate for free — the
    session-8 hardening, so a build gets bounds+collision+invisible-color+hero checks at
    render time without a separate call. Backward-compatible: omit them and nothing changes."""
    name = os.path.basename(out_png)
    # Auto-run ONLY zero-false-positive HTML checks on every render: an undefined css var is
    # unambiguously an invisible-element bug (sample 32). The rotate+overflow+bottom blank-card
    # gotcha is NOT auto-run — it can't be told apart from a normal full-width footer without
    # nesting analysis, so it's a manual diagnostic (layout.antipattern_scan).
    # css_var_check runs here ONLY when there is no element list, because with one the
    # preflight below sees the html and reports it itself — running both printed the
    # same undefined var twice.
    if elements is None:
        bad_vars = layout.css_var_check(html, core)
        if bad_vars:
            print(f"[{name}] ⚠ UNDEFINED CSS VARS (render invisible): {bad_vars}")
    # Also zero-false-positive: a fill that resolves to (near-)exactly the page bg is invisible,
    # full stop. Auto-run because the opt-in invisible_color_check silently never fired on
    # bespoke scripts that didn't pass color_pairs (showcase5b lemon-bubble-on-lemon-field).
    # INFER the page bg when the caller didn't pass it, straight out of the `.p` rule that page()
    # always emits. Requiring the caller to pass page_bg would leave this check opt-in — which is
    # the very flaw that let the invisible-bubble bug through in the first place.
    _bg = page_bg
    if _bg is None:
        _m = re.search(r'\.p\{[^}]*?background:\s*([^;}]+)', html or "")
        if _m:
            _bg = _m.group(1).strip()
    # same_as_bg_scan USED TO AUTO-RUN HERE and no longer does. It compares every
    # declared background against the PAGE ground, which is only the real backing
    # surface when nothing is layered — and most AQ posters layer. A cream badge on a
    # full-bleed teal panel is plainly visible and got "FILL SAME AS PAGE BG" on every
    # single render. Two independent agents reported that (session 10f, c3 and g3),
    # which makes it a spec defect and not bad luck: a static scan cannot know what is
    # behind an element, and its docstring's "zero-false-positive" claim was wrong.
    #
    # reconcile.measure_dom answers the same question EXACTLY, by asking the browser
    # what is actually painted underneath (`invisible_fill`, below). The static scan
    # remains available as a manual pre-render diagnostic, like antipattern_scan.
    if elements is not None:
        # collision_ignore/auto_nudge pass THROUGH. Without them the render-time
        # convenience gate re-reported by-design overlaps that the caller's own
        # preflight had already accepted — the two gates contradicting each other a
        # few lines apart, which teaches people to distrust both.
        # `html` USED TO BE HARDCODED None HERE, so css_var_check, img_src_check,
        # invisible_craft_scan, wash_scan and double_rotation_scan never ran through
        # the documented convenience path no matter what the caller passed — while
        # §6 claimed this one call was the whole gate. An agent found it by reading
        # this source after its own manual scans caught things `render()` had just
        # reported clean (session 10f, agent g1).
        layout.preflight(W, H, elements, html=html, color_pairs=color_pairs,
                         page_bg=page_bg, core=core, expect_hero=expect_hero,
                         collision_ignore=collision_ignore, containers=containers,
                         text_pairs=text_pairs, cascade_stacks=cascade_stacks,
                         reading_order=reading_order, contains=contains,
                         occlusion=occlusion, bleed_tags=(bleed_tags or ()),
                         auto_nudge=auto_nudge)
    # The DOM audit and the screenshot both need this html LOADED in a browser.
    # They now share one page load instead of cold-starting a browser each.
    return await _shoot(html, out_png, W, H, name, elements=elements,
                        collision_ignore=collision_ignore, bleed_tags=bleed_tags,
                        crop_tags=crop_tags)

async def _shoot(html, out_png, W, H, name, elements=None, collision_ignore=(),
                 bleed_tags=None, crop_tags=()):
    """Load once → settle → audit that same DOM → screenshot it. Uses the open
    session's page when there is one; otherwise opens a private session for this
    single call so standalone scripts behave exactly as they always did."""
    async def _work(pg):
        await pg.set_content(html, wait_until="load")
        await _settle(pg)
        issues = await audit.audit(html, name, page=pg, canvas=(W, H),
                                   ignore_pairs=collision_ignore, margin=M,
                                   bleed_tags=(bleed_tags or ()))
        # MEASURED geometry, on the page we already have. This is the only check
        # that can see what the hand-maintained (x,y,w,h) tuples structurally
        # cannot: a text block whose REAL rendered size is not what the author
        # guessed. Clipped/spilling text is unambiguous — there is no design in
        # which a word losing its last three letters is intended — so it prints
        # on every render rather than waiting to be opted into.
        # A design whose MECHANISM is bleeding off both edges printed a wall of
        # OFF-CANVAS for every element doing exactly what it was meant to, with no
        # way to quiet it (session 10f, agent g1). measure_dom always had
        # bleed_tags; render simply never exposed it.
        _md = {'crop_tags': tuple(crop_tags or ())}
        if bleed_tags is not None:
            _md['bleed_tags'] = tuple(bleed_tags)
        flaws = await reconcile.measure_dom(pg, W, H, **_md)
        # OVERSIZE fires whenever glyphs paint past their line box, which a tight
        # line-height ALWAYS causes — so it printed on every hero numeral even when the
        # author had correctly sized the bbox off measure_text()['ink_h']. If the caller
        # declared a box that already covers the real extent, they handled it; only what
        # remains is worth a line. A gate that cries wolf on every clean run is how
        # people learn to skim past the warnings that matter.
        if elements:
            flaws = reconcile.suppress_handled(flaws, elements)
        for line in reconcile.format_measure(flaws):
            print(f"[{name}] ⚠ {line}")
        # When the caller declared an element list, check it against reality. This
        # is CLAUDE.md §10's "stale bbox" row, whose guard until now was the word
        # "discipline".
        if elements:
            rec = reconcile.reconcile_boxes(flaws["boxes"], elements, canvas=(W, H))
            for line in reconcile.format_reconcile(rec):
                print(f"[{name}] ⚠ (advisory) {line}")
        if flaws["clipped"] or flaws["spilling"]:
            issues = list(issues or []) + reconcile.format_measure(
                {k: v for k, v in flaws.items() if k != "off_canvas"})
        await pg.locator(".p").screenshot(path=out_png)
        return issues
    if _SESSION is not None:
        return await _work(await _SESSION.page(W, H))
    async with session() as sess:
        return await _work(await sess.page(W, H))

async def measure_text(items, W=1080, H=1350):
    """Measure how big text ACTUALLY renders, before you lay anything out.

    THE CLASS OF BUG THIS RETIRES. Every bespoke script sizes shapes from data
    ("this bar is 120px because the count is 26") and then drops a label on top
    sized from nothing at all. When the label is wider than the shape you get
    "PLANTAT" hanging off a pill, and no static gate can see it because the two
    are unrelated siblings. The engine had no way to ask the only authority that
    knows — the font — so authors guessed. This asks.

    items: list of dicts {text, font, size, weight, style, letter_spacing, max_width}
           `font` takes the CSS family or a token name ('d','e','s','m').
           `style` is the CSS font-style — pass "italic" for anything set in
           Instrument Serif (`--s`), whose ONLY sanctioned brand use is italic (§9).
           It defaults to italic for the 's' token for exactly that reason.

    ITALIC USED TO BE UNMEASURABLE. There was no font-style parameter and the canvas
    measurer did not emit one either, so every `--s` string came back measured as
    upright — 9.9% narrow on a display-size wordmark, which bled it 71px off-canvas
    and was caught only after render by reconcile's OVERSIZE line. That is the exact
    "sized by guess" class this function exists to retire, reintroduced through a
    missing argument (session 10f, agent c3).
    Returns the same list order, each as
        {'w','h'          — the LAYOUT box: what the next element flows against,
         'text_w'         — the string's OWN width, measured unconstrained. When you
                            pass `max_width`, `w` and `ink_w` are the CONTAINER's width,
                            not the text's — a two-letter headline in a 900px box
                            reports 900. Size a collision bbox off `text_w`.
         'ink_w','ink_h'  — the content box: what the element needs to not clip,
         'glyph_w','glyph_h' — the TRUE painted bounds of the type (single-line
                            only, else None). This is the one to use for a
                            numeral or all-caps hero: `ink_h` reserves the whole
                            em box including a descender the digits never use, so
                            flowing off it opens a hole nobody asked for.
         'lines'          — line count}

    USE THE RIGHT ONE. At line-height < 1 (every AQ headline) the glyphs paint
    outside the line box: a 430px numeral at line-height .78 has h=335 but
    ink_h=443. Flow the NEXT element off `h`; size a collision bbox off `ink_h`.
    Getting this backwards is how a sticker gets cleared onto a numeral.

    Costs one page load. Batch every string you need in ONE call, then lay out.
    """
    FAM = {"d": "var(--d)", "e": "var(--e)", "s": "var(--s)", "m": "var(--m)"}
    spans = []
    for i, it in enumerate(items):
        tok = it.get("font", "d")
        fam = FAM.get(tok, it.get("font", "var(--d)"))
        # Instrument Serif is only ever used italic in this brand, so measuring it
        # upright is always wrong. Default accordingly; an explicit `style` still wins.
        sty = it.get("style") or ("italic" if tok == "s" else "normal")
        mw = it.get("max_width")
        box = f"width:{mw}px;" if mw else "white-space:nowrap;"
        # A SECOND, unconstrained copy of every string. With max_width set the block's
        # rect width is the CSS width no matter how short the text is, so `w` cannot be
        # trusted as the text's own width — that silently inflated a collision bbox by
        # ~100px for a two-letter headline. `text_w` below is measured at nowrap and IS
        # the string's real width.
        spans.append(
            f'<div id="t{i}" style="position:absolute;top:-9999px;left:0;white-space:nowrap;'
            f'font-family:{fam};font-weight:{it.get("weight", 900)};font-style:{sty};'
            f'font-size:{it.get("size", 16)}px;'
            f'letter-spacing:{it.get("letter_spacing", "0")};'
            f'text-transform:{it.get("transform", "none")};'
            f'visibility:hidden">{it["text"]}</div>')
        spans.append(
            f'<div id="m{i}" style="position:absolute;top:0;left:0;{box}'
            f'font-family:{fam};font-weight:{it.get("weight", 900)};font-style:{sty};'
            f'font-size:{it.get("size", 16)}px;'
            f'line-height:{it.get("line_height", 1)};'
            f'letter-spacing:{it.get("letter_spacing", "0")};'
            f'text-transform:{it.get("transform", "none")};'
            f'visibility:hidden">{it["text"]}</div>')
    html = page(W, H, "var(--bg)", "".join(spans), grain=False)

    async def _work(pg):
        await pg.set_content(html, wait_until="load")
        await _settle(pg)
        return await pg.evaluate(
            """n => Array.from({length:n}, (_, i) => {
                 const e = document.getElementById('m' + i);
                 const r = e.getBoundingClientRect();
                 const lh = parseFloat(getComputedStyle(e).lineHeight) || r.height;
                 // h  = the LAYOUT box (what the next element flows against)
                 // ink_h/ink_w = what the glyphs actually PAINT. At line-height
                 // below 1 these differ a lot, and the painted extent is the one
                 // a collision bbox must use — see the note in the docstring.
                 const cs = getComputedStyle(e);
                 const lines = Math.max(1, Math.round(r.height / lh));
                 // TRUE painted glyph box, for single-line text. scrollHeight
                 // reserves the whole font em box (ascender to descender); digits
                 // and caps use far less of it, so flowing off scrollHeight opens
                 // a visible hole under a numeral hero. Canvas TextMetrics gives
                 // the actual inked bounds instead of the font's reserved space.
                 let gw = null, gh = null;
                 if (lines === 1) {
                   const cx = document.createElement('canvas').getContext('2d');
                   // font shorthand ORDER MATTERS: style, then weight, then size/family.
                   // Omitting the style here measured italic as upright.
                   cx.font = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
                   const tm = cx.measureText(e.textContent);
                   if (tm.actualBoundingBoxAscent != null) {
                     gw = Math.ceil(Math.abs(tm.actualBoundingBoxLeft) + Math.abs(tm.actualBoundingBoxRight));
                     gh = Math.ceil(tm.actualBoundingBoxAscent + tm.actualBoundingBoxDescent);
                   }
                 }
                 const te = document.getElementById('t' + i);
                 const tw = te ? Math.ceil(te.getBoundingClientRect().width) : null;
                 return { w: Math.ceil(r.width), h: Math.ceil(r.height), text_w: tw,
                          ink_w: Math.max(Math.ceil(r.width), e.scrollWidth),
                          ink_h: Math.max(Math.ceil(r.height), e.scrollHeight),
                          glyph_w: gw, glyph_h: gh, lines: lines };
               })""", len(items))
    if _SESSION is not None:
        return await _work(await _SESSION.page(W, H))
    async with session() as sess:
        return await _work(await sess.page(W, H))


async def measure_free(html, W, H):
    """Return bounding boxes of .measure elements so a spec can place fillers in REAL gaps."""
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width":W,"height":H})
        await pg.set_content(html, wait_until="load"); await pg.wait_for_timeout(1000)
        boxes = await pg.eval_on_selector_all(".measure",
          "els=>els.map(e=>{const r=e.getBoundingClientRect();return{tag:e.dataset.tag,x:Math.round(r.x),y:Math.round(r.y),b:Math.round(r.bottom),rgt:Math.round(r.right)}})")
        await b.close()
    return boxes

# NOTE: individual pieces are authored as small spec functions in pieces.py.
# This module only provides the vocabulary + gate. See ENGINE.md for how to write one.
