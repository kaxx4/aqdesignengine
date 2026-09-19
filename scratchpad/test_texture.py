"""Self-tests for engine/tex.py (the texture vocabulary) and layout.wash_scan
(the faint-wash guard). Session 10.

The wash_scan assertions reconstruct the friendship_day defect: patterned
decoration at .13-.26 alpha spread across a field, which reads as dirt and
smears through body copy while every numeric gate reports CLEAN.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/test_texture.py
"""
import os, sys, re, importlib.util

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE)

def _load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

tex = _load("tex"); lay = _load("layout"); core = _load("core")
N = 0
def ok(m):
    global N; N += 1; print(f"  ok {N}: {m}")

# ── field textures are well-formed CSS and SOLID by default ─────────────────
for name, fn in tex.FIELDS.items():
    css = fn()
    assert css and ":" in css, name
    assert "None" not in css and "nan" not in css.lower(), (name, css)
ok("all 7 named field textures emit non-empty, well-formed css")

# default opacity is FULL — the house rule is decoration is solid
for name in ("stripes", "crosshatch", "dot_grid", "grid_lines", "concentric", "rays"):
    css = tex.FIELDS[name]()
    assert "00 0" not in css, name
    # a full-alpha ink colour appears as bare #0A0A0A or with an 'ff' suffix
    assert ("#0A0A0Aff" in css) or ("#0A0A0A " in css) or ("#0A0A0A" in css), (name, css)
ok("field textures default to FULL alpha, not a whisper")

assert tex._a(1.0) == "ff" and tex._a(0.0) == "00" and tex._a(0.5) == "80"
ok("_a() maps 0..1 onto a two-digit hex alpha")
assert tex._a(9.0) == "ff" and tex._a(-3) == "00"
ok("_a() clamps out-of-range alpha instead of emitting invalid css")

# field() must not guess on a typo
assert tex.field("crosshatch") != ""
assert tex.field("crosshartch") == ""
ok("field() returns '' for an unknown name — a typo degrades to a flat slab")

# ── grain is parameterised now, not one frozen string ───────────────────────
g1, g2 = tex.grain(opacity=0.06), tex.grain(opacity=0.14)
assert g1 != g2 and g1.startswith("background-image:url(")
ok("grain() is parameterised — different opacity gives different output")
assert "%3Csvg" in tex.grain() and '"' not in tex.grain()[24:-2]
ok("grain() escapes its inline svg so the url() cannot break the style attribute")

# ── photo treatments keep the <img>, never fake one ─────────────────────────
d = tex.duotone("data:image/jpeg;base64,AAAA", shadow="#0A0A0A", highlight="#FF4D8C")
assert "<img src=\"data:image/jpeg;base64,AAAA\"" in d
assert "grayscale(1)" in d and "mix-blend-mode:multiply" in d
ok("duotone() renders the real photo under two plates (no fabricated imagery)")
assert tex.duotone("x", screen=False).count("radial-gradient") == 0
ok("duotone(screen=False) drops the halftone screen cleanly")
assert "<img" in tex.photo_ink("x") and "contrast(" in tex.photo_ink("x")
ok("photo_ink() is a single-plate high-contrast treatment")

# ── physical objects are opaque ─────────────────────────────────────────────
t = tex.tape(10, 20)
assert "clip-path:polygon" in t and "opacity:0.92" in t
ok("tape() is near-opaque with torn clip-path ends (see-through tape = the wash bug)")
assert "clip-path:polygon" in tex.torn("top") and tex.torn("top") != tex.torn("bottom")
ok("torn() gives distinct top/bottom paper edges")

cp = tex.cutpaper(0, 0, 100, 100, "#FF4D8C", texture=tex.crosshatch(), outline="#0A0A0A")
assert "repeating-linear-gradient" in cp and "inset 0 0 0 3px #0A0A0A" in cp
ok("cutpaper() composes a texture INSIDE a shape that has an edge")
assert "blur" not in tex.cutpaper(0, 0, 10, 10, "#fff")
ok("cutpaper's drop is a hard offset — never a blur (no mixing the two systems)")

# legacy shims still importable for the 44 recreations
assert tex.halftone_fill("#FF4D8C") == "background-color:#FF4D8C;"
ok("legacy halftone_fill still returns a FLAT fill (house rule unchanged)")
for fn in ("halftone_gradient", "riso_photo", "riso_photo_wrap"):
    assert callable(getattr(tex, fn)), fn
ok("all legacy tex entry points survive — 44 recreations keep importing")

# ── wash_scan: THE friendship_day defect ────────────────────────────────────
WASH = ('<div style="position:absolute;inset:0;background-image:'
        'repeating-linear-gradient(45deg,#0A0A0A 0 2px,transparent 2px 9px);opacity:0.18"></div>')
hits = lay.wash_scan(WASH)
assert len(hits) == 1 and hits[0][0] == 0.18 and hits[0][1] == 1.0
ok("wash_scan catches a full-bleed hatch field at .18 alpha (the real bug)")

for a in (0.13, 0.20, 0.26, 0.33):
    assert lay.wash_scan(WASH.replace("0.18", str(a))), a
ok("caught across the whole .13-.33 'dirt' band")

# the SAME pattern at full strength is intended design, not a defect
assert lay.wash_scan(WASH.replace("opacity:0.18", "opacity:1")) == []
ok("the same pattern SOLID is not flagged — the fix is contrast, not deletion")
assert lay.wash_scan(WASH.replace("0.18", "0.02")) == []
ok("below .05 it is invisible rather than dirty — out of scope, not flagged")

# a flat low-alpha colour layer is a photo scrim: legitimate craft, left alone
SCRIM = '<div style="position:absolute;inset:0;background:#0A0A0A;opacity:0.28"></div>'
assert lay.wash_scan(SCRIM) == []
ok("a flat tinted photo scrim is NOT flagged (CAROUSEL_PLAYBOOK craft)")

# small textured objects are the supported way to use texture
CHIP = ('<div style="position:absolute;width:90px;height:90px;background-image:'
        'radial-gradient(#0A0A0A 1px,transparent 2px);opacity:0.2"></div>')
assert lay.wash_scan(CHIP) == []
ok("a small textured chip is below the area floor — not flagged")

BIG = CHIP.replace("width:90px;height:90px", "width:900px;height:700px")
assert lay.wash_scan(BIG), "a 900x700 faint pattern should trip the area floor"
ok("the same faint pattern at 900x700 DOES trip it — damage scales with area")

assert lay.wash_scan("") == [] and lay.wash_scan(None) == []
ok("wash_scan tolerates empty/None html")

# it must be ADVISORY — a known-FP check may never flip clean
r = lay.preflight(1080, 1350, [(0, 0, 100, 100)], html=WASH, page_bg="#F4EFE0", core=core)
assert r["faint_wash"], "wash_scan should be wired into preflight"
assert r["clean"] is True, "faint_wash must be advisory, not a hard fail"
ok("wired into preflight as ADVISORY — reports, never blocks")

print(f"\nALL {N} ASSERTIONS PASSED")
