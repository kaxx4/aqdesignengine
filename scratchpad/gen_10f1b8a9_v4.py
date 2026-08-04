"""RECREATION — 10f1b8a9789261 (annotated headline / "HOW ILLUSTRATION ENHANCES YOUR BRAND"),
iteration 4. Prior v3 measured 0.21 vs reference, no blocking critique, and looked strong on the
side-by-side already — this is a targeted refinement, not a rebuild.

compare.py on v3:
  SCORE 0.21 | area 1.013x | detail 0.926x | spread 1.056x | bbox IoU 0.946
  - REGION UNDER-filled row 5/11 col 5-6/9 (delta 0.84-0.97) -> the hand-mascot zone (~y40-55%,
    x45-65%). Looking at both images: reference's hand is BIGGER and sits LOWER, its palm
    reaching well into the headline. v3's hand is smaller and higher, leaving that band empty.
  - REGION OVER-filled row 9/11 col 9/9 (delta 0.47) -> bottom-right sparkle next to "BRAND" is
    reference-scale ~40px; v3's is oversized and reads as a second hero mark.
  - MISSING COLOUR near-neutral rgb(128,128,128) 2% -> the reference's thin grey top/bottom rules;
    v3's rules render pure ink. Swap to a genuine mid-grey.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]
A = core.ACCENTS                      # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
PINK, MINT, LEMON, TOMATO, GRAPE = A[0], A[1], A[2], A[3], A[5]
INK = "#0A0A0A"; CREAM = "#F4EFE0"; GREY = "#8A8A82"
M = 64
els = []
def E(label, x, y, w, h): els.append((label, x, y, w, h))

def rule(y):
    return f'<div style="position:absolute;left:{M}px;top:{y}px;width:{W-2*M}px;height:2px;background:{GREY};z-index:20"></div>'

def masthead(num, center, right, y_line, y_text):
    return (rule(y_line)
            + f'<span style="position:absolute;left:{M}px;top:{y_text}px;font-family:var(--m);'
              f'font-weight:700;font-size:16px;color:{INK};z-index:20">{num}</span>'
            + f'<span style="position:absolute;left:50%;top:{y_text}px;transform:translateX(-50%);'
              f'font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.04em;color:{INK};'
              f'z-index:20;white-space:nowrap">{center}</span>'
            + f'<span style="position:absolute;right:{M}px;top:{y_text}px;font-family:var(--m);'
              f'font-weight:700;font-size:16px;color:{INK};z-index:20">{right}</span>')

top = masthead("03.", "aquaterra ngo", "@2026", 96, 66)
E("rule_top", M, 96, W - 2*M, 2)
bottom = masthead("03.", "welfare &middot; climate &middot; education", "@2026", H - 96, H - 122)
E("rule_bottom", M, H - 96, W - 2*M, 2)
E("bottom_text_row", M, H - 122, W - 2*M, 26)   # the masthead TEXT band itself — was untracked

# ── scribble double-loop + arrow, upper-left ──────────────────────────────────
scribble = (f'<svg style="position:absolute;left:{M-8}px;top:190px;z-index:8" width="420" height="260" '
            f'viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg">'
            f'<path d="M40 200 C10 160 30 120 75 130 C120 140 100 190 65 190 C30 190 20 150 60 130 '
            f'C110 105 190 110 210 60 M175 90 L212 55 L200 100" '
            f'fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="12" cy="230" r="7" fill="none" stroke="{INK}" stroke-width="5"/></svg>')
E("scribble", M - 8, 190, 420, 260)

# ── hand mascot — ENLARGED and LOWERED to fill the reference's row5 band ─────
HX, HY, HSZ = 400, 340, 400
hand = (f'<svg style="position:absolute;left:{HX}px;top:{HY}px;z-index:12;transform:rotate(-3deg)" '
        f'width="{HSZ}" height="{HSZ}" viewBox="0 0 120 130" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M40 62 C40 50 80 50 80 62 C92 74 96 96 78 106 C68 110 52 110 42 106 '
        f'C24 96 28 74 40 62 Z M46 60 L46 30 C46 24 54 24 54 30 L54 62 M58 60 L58 22 '
        f'C58 16 68 16 68 22 L68 60 M70 60 L70 28 C70 22 80 22 80 28 L80 60" '
        f'fill="{GRAPE}" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round"/>'
        f'<circle cx="52" cy="42" r="1.6" fill="{INK}"/><circle cx="56" cy="42" r="1.6" fill="{INK}"/>'
        f'<path d="M51 47 Q54 50 57 47" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="63" cy="34" r="1.6" fill="{INK}"/><circle cx="67" cy="34" r="1.6" fill="{INK}"/>'
        f'<path d="M62 39 Q65 42 68 39" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="74" cy="32" r="1.6" fill="{INK}"/><circle cx="78" cy="32" r="1.6" fill="{INK}"/>'
        f'<path d="M73 37 Q76 40 79 37" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M46 82 Q60 76 74 82 M50 92 L50 100 M62 90 L62 100" fill="none" stroke="{INK}" '
        f'stroke-width="3" stroke-linecap="round"/>'
        f'<circle cx="42" cy="100" r="6" fill="#FFFFFF" stroke="{INK}" stroke-width="3.5"/></svg>')
E("hand", HX, HY, HSZ, HSZ)

sparkle_small1 = (f'<div style="position:absolute;left:960px;top:340px;z-index:14">'
                  f'{dd.stamp("sparkle", None, rot=0)}</div>')  # outline-only, keep default stroke=none look
sparkle_small1 = (f'<svg style="position:absolute;left:1000px;top:230px;z-index:14" width="60" height="60" '
                  f'viewBox="0 0 66 66" xmlns="http://www.w3.org/2000/svg">'
                  f'<path d="M33 4 L39 28 L62 33 L39 38 L33 62 L27 38 L4 33 L27 28 Z" '
                  f'fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/></svg>')
E("sp1", 1000, 230, 60, 60)

bee = (f'<svg style="position:absolute;left:948px;top:600px;z-index:14" width="96" height="96" '
       f'viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">'
       f'<ellipse cx="36" cy="40" rx="18" ry="14" fill="{LEMON}" stroke="{INK}" stroke-width="3"/>'
       f'<path d="M22 34 L50 34 M20 40 L52 40 M22 46 L50 46" stroke="{INK}" stroke-width="3.5"/>'
       f'<ellipse cx="16" cy="30" rx="10" ry="7" fill="none" stroke="{INK}" stroke-width="2.5"/>'
       f'<ellipse cx="14" cy="20" rx="8" ry="6" fill="none" stroke="{INK}" stroke-width="2.5"/></svg>')
E("bee", 948, 600, 96, 96)

# ── headline stack ─────────────────────────────────────────────────────────
HL_Y = 700
headline = (f'<div style="position:absolute;left:{M}px;top:{HL_Y}px;z-index:16;font-family:var(--d);'
            f'font-weight:900;font-size:108px;line-height:.92;letter-spacing:-.02em;color:{INK};'
            f'text-transform:uppercase">HOW</div>')
E("how", M, HL_Y, 340, 118)

ILY = HL_Y + 116
illus = (f'<div style="position:absolute;left:{M-8}px;top:{ILY+6}px;width:900px;height:120px;'
         f'background:{LEMON};z-index:15;transform:rotate(-2.5deg);border-radius:6px"></div>'
         f'<div style="position:absolute;left:{M}px;top:{ILY}px;z-index:17;font-family:var(--d);'
         f'font-weight:900;font-size:88px;line-height:1;letter-spacing:-.02em;color:{INK};'
         f'text-transform:uppercase;transform:rotate(-2.5deg);transform-origin:left center">ILLUSTRATION</div>')
E("illustration_band", M - 8, ILY + 6, 900, 120)

EHY = ILY + 130
enhances = (f'<div style="position:absolute;left:{M}px;top:{EHY}px;z-index:16;font-family:var(--d);'
            f'font-weight:900;font-size:88px;line-height:1;letter-spacing:-.02em;color:{INK};'
            f'text-transform:uppercase">ENHANCES</div>')
E("enhances", M, EHY, 620, 100)

chevrons = (f'<svg style="position:absolute;left:700px;top:{EHY-10}px;z-index:16" width="130" height="150" '
            f'viewBox="0 0 130 150" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'
            + "".join(f'<path d="M{20+i*8} {10+i*40} L{70+i*8} {40+i*40} L{20+i*8} {70+i*40}" '
                      f'fill="none" stroke="{TOMATO}" stroke-width="7" stroke-linecap="round" '
                      f'stroke-linejoin="round"/>' for i in range(3)) + '</svg>')
E("chevrons", 700, EHY + 6, 88, 96)
sp2 = (f'<svg style="position:absolute;left:830px;top:{EHY+40}px;z-index:14" width="54" height="54" '
       f'viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg">'
       f'<path d="M27 3 L32 22 L51 27 L32 32 L27 51 L22 32 L3 27 L22 22 Z" '
       f'fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/></svg>')
E("sp2", 830, EHY + 40, 54, 54)

# ── YOUR pill + BRAND ─────────────────────────────────────────────────────
PY = EHY + 96
pill = (f'<div style="position:absolute;left:{M}px;top:{PY}px;width:520px;height:108px;'
        f'background:{MINT};border-radius:54px;z-index:16"></div>'
        f'<div style="position:absolute;left:{M+34}px;top:{PY+8}px;z-index:18;font-family:var(--d);'
        f'font-weight:900;font-size:82px;line-height:1;color:{INK};text-transform:uppercase">YOUR</div>'
        f'<div style="position:absolute;left:{M+400}px;top:{PY+14}px;width:80px;height:80px;'
        f'background:{INK};border-radius:50%;z-index:18;display:flex;align-items:center;'
        f'justify-content:center;color:#FFFFFF;font-family:var(--m);font-size:34px">&rarr;</div>'
        f'<div style="position:absolute;left:{M+560}px;top:{PY+2}px;z-index:16;font-family:var(--d);'
        f'font-weight:900;font-size:82px;line-height:1;color:{INK};text-transform:uppercase">BRAND</div>')
E("your_pill", M, PY, 520, 108)
E("brand", M + 560, PY + 2, 400, 100)

# small sparkle beside BRAND — SHRUNK from v3's oversized version (compare.py OVER-fill fix)
sp3 = (f'<svg style="position:absolute;left:960px;top:{PY-40}px;z-index:20" width="34" height="34" '
       f'viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg">'
       f'<path d="M17 2 L20 14 L32 17 L20 20 L17 32 L14 20 L2 17 L14 14 Z" '
       f'fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/></svg>')
E("sp3", 960, PY - 40, 34, 34)

SY = PY + 122
sub = (f'<div style="position:absolute;left:{M}px;top:{SY}px;width:820px;z-index:16;'
       f'font-family:var(--s);font-style:italic;font-weight:400;font-size:23px;line-height:1.3;'
       f'color:{INK}">Not just &ldquo;cute&rdquo; &mdash; illustration can elevate how people remember you.</div>')
E("sub", M, SY, 820, 70)

ast = (f'<svg style="position:absolute;left:1000px;top:{H-166}px;z-index:16" width="40" height="40" '
       f'viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">'
       f'<path d="M20 4 V36 M6 12 L34 28 M34 12 L6 28" stroke="{INK}" stroke-width="4" stroke-linecap="round"/></svg>')
E("asterisk", 1000, H - 166, 40, 40)

inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
         + top + bottom + scribble + hand + sparkle_small1 + bee
         + headline + illus + enhances + chevrons + sp2 + pill + sp3 + sub + ast)
html = B.page(W, H, CREAM, inner, grain=False)
pf = lay.preflight(W, H, els, html=html, page_bg=CREAM, core=core,
                   collision_ignore={frozenset({"hand", "illustration_band"}),
                                     frozenset({"hand", "how"}),
                                     frozenset({"hand", "scribble"})})

async def main():
    os.makedirs("out/versions/10f1b8a978926", exist_ok=True)
    out = "out/versions/10f1b8a978926/v4.png"
    await B.render(html, out, W, H)
    print("wrote", out, "| clean =", pf.get("clean"))
asyncio.run(main())
