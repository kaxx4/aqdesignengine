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
core = _load("core"); rhythm = _load("rhythm"); dd = _load("doodles"); audit = _load("audit"); layout = _load("layout")

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

# ---------- render + audit gate ----------
async def render(html, out_png, W, H, elements=None, color_pairs=None, page_bg=None,
                 expect_hero=False):
    """Render + gate. Always: playwright screenshot + audit.py (DOM) + css_var_check (auto,
    zero false positives). OPTIONAL: pass `elements` (and optionally color_pairs/page_bg/
    expect_hero) and render also runs the full layout.preflight static gate for free — the
    session-8 hardening, so a build gets bounds+collision+invisible-color+hero checks at
    render time without a separate call. Backward-compatible: omit them and nothing changes."""
    from playwright.async_api import async_playwright
    name = os.path.basename(out_png)
    issues = await audit.audit(html, name)
    # Auto-run ONLY zero-false-positive HTML checks on every render: an undefined css var is
    # unambiguously an invisible-element bug (sample 32). The rotate+overflow+bottom blank-card
    # gotcha is NOT auto-run — it can't be told apart from a normal full-width footer without
    # nesting analysis, so it's a manual diagnostic (layout.antipattern_scan).
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
    if _bg is not None:
        same = layout.same_as_bg_scan(html, _bg, core)
        if same:
            print(f"[{name}] ⚠ FILL SAME AS PAGE BG (element invisible): {same}")
    if elements is not None:
        layout.preflight(W, H, elements, html=None, color_pairs=color_pairs,
                         page_bg=page_bg, core=core, expect_hero=expect_hero)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":W,"height":H}, device_scale_factor=2)
        await pg.set_content(html, wait_until="load"); await pg.wait_for_timeout(1500)
        await pg.locator(".p").screenshot(path=out_png); await b.close()
    return issues

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
