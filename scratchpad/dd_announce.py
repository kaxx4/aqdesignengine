"""DISCO DIWALI 2026 announcement, recreation of training_samples/disco_diwali/ref_announce_2026.png (Workflow B).

Reference is 1200x1500 (4:5); built on the 1080x1350 feed canvas, every reference coordinate scaled by K=0.9.
All imagery is the user's supplied real assets in engine/assets/disco_diwali/. Nothing is fabricated.

Adaptations (CLAUDE.md sec 2 rule 4):
  * Ink ground, silver/gold/white only: a recorded FORMAT exception (brain/DISCO_DIWALI.md sec 5), not core.ACCENTS.
  * The reference grotesque is a wide geometric sans not in core.FONTS; Eina semibold uppercase stands in.
  * The clock emoji is drawn as an SVG (emoji fonts are not guaranteed in the render box).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_announce.py [vN]
"""
import asyncio, base64, os, sys, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); lay = load("layout")

W, H = core.SIZES["feed"]
K = 0.9
S = lambda v: round(v * K)
ASSETS = "engine/assets/disco_diwali/"
def uri(name):
    mime = "image/png" if name.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(open(ASSETS + name, "rb").read()).decode()

OFFWHITE, GOLD, GROUND = "#F2F2F2", "#C9971C", "#000000"
elements = []
def box(label, x, y, w, h): elements.append((label, x, y, w, h))

def img(name, x, y, w, h=None, z=1, extra="", tag=""):
    hh = f"height:{h}px;" if h else ""
    return (f'<img src="{uri(name)}" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;{hh}z-index:{z};{extra}">')

parts = [f'<div style="position:absolute;inset:0;background:{GROUND}"></div>']

# 1 ground plate (beaded corner clusters) ----------------------------------------------------------
parts.append(img("bg_beaded_portrait.jpg", 0, 0, W, H, z=1, tag="plate"))

# 2 mask, top right, bleeds off the right edge ------------------------------------------------------
MK = 0.48
mw = S(2000 * MK); mh = round(mw * 1514 / 2000)
mx, my = S(415 - 190 * MK), S(-145)
parts.append(img("mask.png", mx, my, mw, z=6, tag="mask", extra="filter:drop-shadow(0 6px 22px rgba(0,0,0,.55));"))

# 3 string lights across the top, drawn over the mask ------------------------------------------------
lw = S(1560)
parts.append(img("string_lights.png", S(105), S(-150), lw, z=7, tag="lights"))

# 4 LIVE badge, top left ----------------------------------------------------------------------------
bx, by, bw = S(45), S(48), S(293)
parts.append(img("live_badge.png", bx, by, bw, z=8, tag="badge"))
box("badge", bx, by, bw, round(bw * 1005 / 1061))

# 5 title lockup (disco ball + DISCO + दिवाली) ------------------------------------------------------
TK = 0.676
tw = S(2000 * TK)
tx, ty = S(30 - 265 * TK), S(390 - 320 * TK)
parts.append(img("title_lockup.png", tx, ty, tw, z=9, tag="title"))
box("title", S(30), S(390), S(1160), S(670))

# 6 type -------------------------------------------------------------------------------------------
def line(label, text, cx, cy, size, weight=700, extra=""):
    parts.append(f'<div data-tag="{label}" style="position:absolute;left:{cx}px;top:{cy}px;transform:translate(-50%,-50%);'
                 f'white-space:nowrap;font-family:var(--e);font-weight:{weight};font-size:{size}px;line-height:1;'
                 f'color:{OFFWHITE};text-transform:uppercase;letter-spacing:.01em;-webkit-text-stroke:{max(1,size//28)}px {OFFWHITE};z-index:12;{extra}">{text}</div>')

line("sub1", "Masquerade Sangeet", S(673), S(950), S(46))
line("sub2", "Edition", S(673), S(1000), S(44), weight=400)
line("date", "10th November, 2026", S(600), S(1090), S(76))
clock = ('<svg width="{s}" height="{s}" viewBox="0 0 40 40" style="display:inline-block;vertical-align:middle;margin-right:{m}px;-webkit-text-stroke:0">'
         '<circle cx="20" cy="20" r="18" fill="#EEE" stroke="#999" stroke-width="2"/>'
         '<path d="M20 9v11l6 5" stroke="#222" stroke-width="3" fill="none" stroke-linecap="round"/></svg>').format(s=S(60), m=S(16))
line("time", f'{clock}4:30 PM Onwards', S(600), S(1168), S(60))
line("tickets", "Ticket Sales Open Soon", S(600), S(1232), S(60))
line("more", "More Details Soon", S(600), S(1302), S(34))
for lab, cx, cy, w, h in [("sub1", 673, 950, 570, 52), ("sub2", 673, 1000, 190, 46), ("date", 600, 1090, 900, 80),
                          ("time", 640, 1168, 580, 62), ("tickets", 600, 1232, 760, 62), ("more", 600, 1302, 380, 36)]:
    box(lab, S(cx - w / 2), S(cy - h / 2), S(w), S(h))

# CTA pill
px, py, pw, ph = S(350), S(1330), S(498), S(112)
parts.append(f'<div data-tag="cta" style="position:absolute;left:{px}px;top:{py}px;width:{pw}px;height:{ph}px;border:2px solid {GOLD};'
             f'border-radius:{S(24)}px;background:#050505;z-index:12;display:flex;align-items:center;justify-content:center;'
             f'font-family:var(--e);font-weight:700;font-size:{S(58)}px;color:{OFFWHITE};text-transform:uppercase;line-height:1">Link in bio</div>')
box("cta", px, py, pw, ph)

# 7 full-frame overlays: gold sparkle dust, then film grain/scratches -------------------------------
parts.append(img("sparkles.png", 0, 0, W, H, z=14, tag="sparkles", extra="mix-blend-mode:screen;object-fit:cover;"))
parts.append(img("grain.png", 0, 0, W, H, z=15, tag="grain", extra="mix-blend-mode:screen;object-fit:cover;opacity:.9;"))

html = B.page(W, H, GROUND, "".join(parts), grain=False)

async def main():
    ver = sys.argv[1] if len(sys.argv) > 1 else "v1"
    out_dir = "out/versions/disco_diwali_announce"
    os.makedirs(out_dir, exist_ok=True)
    await B.render(html, f"{out_dir}/{ver}.png", W, H, elements=elements,
                   containers=("cta",), collision_ignore=[("title","sub1"),("title","sub2")], bleed_tags=("mask", "title", "lights", "plate", "sparkles", "grain"),
                   crop_tags=("plate", "sparkles", "grain"), page_bg=GROUND)
    print("done")
asyncio.run(main())
