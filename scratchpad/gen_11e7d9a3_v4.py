"""RECREATION — 11e7d9a3ff6761 (isometric OVERFLOW keycaps), iteration 4.

v3 (script since lost from scratchpad, only the PNG survives) measured 0.507 vs reference:
  CONTENT TOO SMALL (0.67x) -- BLOCKING. Scale the composition up, don't add new elements.
  MISSING COLOUR near-neutral rgb(224,224,224) 11% -- the reference's near-white card faces/grid.
  Row 8 (y~875-1105) badly under-filled across cols 3-6 -- v3 left the whole lower-middle empty
  (its bottom-left speech-bubble card and arrow sat too small/low, no isometric depth on keys).

This build: extruded isometric capsule keycaps (shapes.extrude — the SAME primitive c42f94a09f's
keycaps used, this reference's own top steal per DECISIONS.md), scaled to genuinely fill the
1080x1350 frame edge-to-edge like the reference, plus 5 near-white isometric prop cards
(envelope, code-brackets, numbered tag, pointing hand, pencil) reproducing the reference's set.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); sh = load("shapes"); lay = load("layout")

W, H = core.SIZES["feed"]
A = core.ACCENTS                      # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
INK = "#0A0A0A"; NEAR_WHITE = "#EDE9DF"; PAGE = "#F4F0E4"
M = 40
els = []
def E(label, x, y, w, h): els.append((label, x, y, w, h))

def grid():
    lines = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="#C9D6DC" stroke-width="1.2" opacity=".55"/>'
                     for x in range(0, W + 1, 54))
    lines += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#C9D6DC" stroke-width="1.2" opacity=".55"/>'
                      for y in range(0, H + 1, 54))
    return f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{lines}</svg>'

def rounded_square(w=100, h=100, r=26):
    """v4 BUG: sh.capsule(w,h) with w==h degenerates to a full CIRCLE (r=h/2). The reference's
    keycaps are ROUNDED SQUARES, not circles — this is the actual keycap silhouette."""
    return (f"M{r} 0 H{w-r} A{r} {r} 0 0 1 {w} {r} V{h-r} A{r} {r} 0 0 1 {w-r} {h} "
            f"H{r} A{r} {r} 0 0 1 0 {h-r} V{r} A{r} {r} 0 0 1 {r} 0 Z")

def keycap(letter, x, y, size, acc, rot=0, z=10):
    """Extruded isometric rounded-square keycap. v4 BUG (DETAIL TOO LOW, blocking): flat
    silhouettes with no interior linework. Fix per the decision table: add interior linework via
    shapes.interior's inset "inner" line — the die-cut bevel edge on every key's top face — rather
    than adding new objects."""
    path = rounded_square(100, 100, 22)
    art = sh.extrude(path, acc, depth=16, size=size, box=100, rot=rot)
    inset = sh.interior(path, kind="inner", box=100, color=INK)
    # LOOKING-GATE OVERRIDE: kind="both" (dots) pushed detail_ratio over the metric's 0.72
    # threshold, but the dot halftone made every key look busy/textured against the reference's
    # completely CLEAN flat-color keys with only a subtle bevel line. RECREATION_PROTOCOL.md is
    # explicit that the looking gate outranks the numeric gate — reverted to the single inset
    # line, which is what the reference actually shows.
    inset_svg = (f'<svg viewBox="0 0 100 100" width="{size}" height="{size}" '
                 f'style="position:absolute;inset:0" xmlns="http://www.w3.org/2000/svg">{inset}</svg>')
    fg = core.text_on(acc)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{art}{inset_svg}'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
            f'padding-bottom:18px;font-family:var(--d);font-weight:900;font-size:{int(size*0.42)}px;'
            f'color:{fg}">{letter}</div></div>')

def card(x, y, size, inner_svg, rot=0, z=8, badge=None):
    """Near-white extruded card — envelope/code/hand/pencil/tag props, uniform treatment."""
    path = sh.capsule(w=100, h=118) if False else "M14 0 H86 A14 14 0 0 1 100 14 V104 A14 14 0 0 1 86 118 H14 A14 14 0 0 1 0 104 V14 A14 14 0 0 1 14 0 Z"
    art = sh.extrude(path, NEAR_WHITE, depth=16, size=size, box=100, rot=0)
    bh = ""
    if badge:
        bh = (f'<div style="position:absolute;top:-4px;right:-4px;width:{size*0.24}px;height:{size*0.24}px;'
              f'border-radius:50%;background:{badge[1]};border:3px solid {INK};display:flex;'
              f'align-items:center;justify-content:center;font-family:var(--d);font-weight:900;'
              f'font-size:{size*0.13}px;color:{INK};z-index:2">{badge[0]}</div>')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{art}'
            f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;'
            f'padding-bottom:14px">{inner_svg}</div>{bh}</div>')

ICON_ENVELOPE = f'<svg width="46%" height="46%" viewBox="0 0 40 40"><rect x="4" y="9" width="32" height="22" rx="3" fill="none" stroke="{INK}" stroke-width="2.6"/><path d="M5 10 L20 22 L35 10" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/></svg>'
ICON_CODE = f'<svg width="46%" height="46%" viewBox="0 0 40 40"><path d="M14 10 L4 20 L14 30 M26 10 L36 20 L26 30" fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_HAND = f'<svg width="50%" height="50%" viewBox="0 0 40 40"><path d="M14 34 C10 34 8 30 8 24 L8 16 C8 14 10 14 10 16 L10 22 M10 22 L10 12 C10 10 12 10 12 12 L12 20 M12 20 L12 10 C12 8 14 8 14 10 L14 20 M14 20 L14 12 C14 10 16 10 16 12 L16 22 C16 22 20 20 22 24 C24 28 22 34 18 34 Z" fill="none" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/></svg>'
ICON_DOTS = f'<svg width="50%" height="26%" viewBox="0 0 60 20"><circle cx="14" cy="10" r="5" fill="{INK}"/><circle cx="30" cy="10" r="5" fill="{INK}"/><circle cx="46" cy="10" r="5" fill="{INK}"/></svg>'
ICON_PENCIL = (f'<svg width="70%" height="70%" viewBox="0 0 100 40"><path d="M4 26 L70 6 L92 12 L26 32 Z" '
               f'fill="{NEAR_WHITE}" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>'
               f'<path d="M78 9 L92 12 L82 22 Z" fill="{A[0]}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/></svg>')

# ── LETTERS — scaled to genuinely fill the frame (fixes CONTENT TOO SMALL) ────
ROW1 = [("O", A[3]), ("V", A[5]), ("E", A[5]), ("R", A[6])]
ROW2 = [("F", A[4]), ("L", A[2]), ("O", A[1]), ("W", A[5])]
KS = 300
row1_html = ""
for i, (ch, acc) in enumerate(ROW1):
    x, y = -20 + i * 232, 300 + (i % 2) * 40
    row1_html += keycap(ch, x, y, KS, acc, rot=(-4 if i % 2 else 3), z=10 + i)
    E(f"r1_{i}", x, y, KS, KS)

row2_html = ""
for i, (ch, acc) in enumerate(ROW2):
    x, y = -70 + i * 232, 660 + (i % 2) * 40
    row2_html += keycap(ch, x, y, KS, acc, rot=(3 if i % 2 else -4), z=20 + i)
    E(f"r2_{i}", x, y, KS, KS)

# ── PROP CARDS — filling the four corners + right margin, per the reference ──
props = ""
props += card(360, -60, 260, ICON_ENVELOPE, rot=-6, z=6)
E("card_envelope", 360, -60, 260, 260)
props += card(760, -70, 300, ICON_CODE, rot=8, z=5)
E("card_code", 760, -70, 300, 300)
props += card(940, 30, 240, "", rot=10, z=7, badge=("1", A[2]))
E("card_tag", 940, 30, 240, 240)
props += card(900, 560, 270, ICON_HAND, rot=-5, z=25)
E("card_hand", 900, 560, 270, 270)
props += card(-30, 1000, 300, ICON_DOTS, rot=-4, z=4)
E("card_dots", -30, 1000, 300, 300)

pencil = (f'<div style="position:absolute;left:640px;top:1140px;width:420px;height:200px;z-index:26;'
          f'transform:rotate(22deg)">{ICON_PENCIL.replace("70%25", "100%").replace("70%","100%")}</div>')
E("pencil", 640, 1140, 420, 200)

stars = ""
for sx, sy, ssz, srot in [(50, 60, 90, -8), (190, 130, 60, 10)]:
    stars += (f'<svg style="position:absolute;left:{sx}px;top:{sy}px;z-index:14" width="{ssz}" '
              f'height="{ssz}" viewBox="0 0 40 40" transform="rotate({srot})">'
              f'<path d="M20 2 L24 16 L38 20 L24 24 L20 38 L16 24 L2 20 L16 16 Z" fill="{INK}"/></svg>')
    E(f"star{sx}", sx, sy, ssz, ssz)

cursor = (f'<svg style="position:absolute;left:530px;top:560px;z-index:60" width="90" height="90" '
          f'viewBox="0 0 40 40"><path d="M6 4 L6 30 L14 24 L20 36 L26 33 L20 21 L30 21 Z" '
          f'fill="#FFFFFF" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/></svg>')
E("cursor", 530, 560, 90, 90)

arrow = (f'<svg style="position:absolute;left:700px;top:1210px;z-index:26" width="360" height="140" '
         f'viewBox="0 0 360 140"><path d="M15 125 L280 40" fill="none" stroke="{INK}" stroke-width="7" '
         f'stroke-linecap="round"/><path d="M245 15 L300 35 L278 80 Z" fill="{A[0]}" stroke="{INK}" '
         f'stroke-width="5" stroke-linejoin="round"/></svg>')
E("arrow", 700, 1210, 360, 140)

logo = f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:40px;z-index:60">'
footer = f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;font-size:14px;color:{INK};z-index:60">@ngo.aquaterra</span>'

inner = (f'<div style="position:absolute;inset:0;background:{PAGE}"></div>' + grid()
         + row1_html + row2_html + props + pencil + stars + cursor + arrow + logo + footer)
html = B.page(W, H, PAGE, inner, grain=True)

pf = lay.preflight(W, H, els, html=html, page_bg=PAGE, core=core,
                    collision_ignore={
                        frozenset({"r1_0", "r1_1"}), frozenset({"r1_1", "r1_2"}), frozenset({"r1_2", "r1_3"}),
                        frozenset({"r2_0", "r2_1"}), frozenset({"r2_1", "r2_2"}), frozenset({"r2_2", "r2_3"}),
                        frozenset({"r1_1", "r2_1"}), frozenset({"r1_1", "r2_0"}), frozenset({"r1_2", "r2_2"}),
                        frozenset({"r1_1", "cursor"}), frozenset({"r2_1", "cursor"}), frozenset({"r1_2", "cursor"}),
                        frozenset({"card_code", "card_envelope"}), frozenset({"card_code", "card_tag"}),
                        frozenset({"r1_3", "card_hand"}), frozenset({"r2_3", "card_hand"}),
                        frozenset({"r1_0", "card_envelope"}), frozenset({"pencil", "arrow"}),
                    })

async def main():
    os.makedirs("out/versions/11e7d9a3ff6761", exist_ok=True)
    out = "out/versions/11e7d9a3ff6761/v4.png"
    await B.render(html, out, W, H)
    print("wrote", out, "| clean =", pf.get("clean"))
asyncio.run(main())
