"""RECREATION — 091944e282ce11 (events calendar), iteration 3.

v2 STATE: score 0.328, area 0.91x, detail 0.74x, no blocking critique. Target <= 0.16.

WHAT THE SIDE-BY-SIDE (protocol step 4) FOUND IN v2 — each is a real miss, not an adaptation:
  1. FIVE rows. The reference has SIX. Element count is explicitly "not allowed to differ".
  2. The black panel had ~150px of dead black below the last row — the reference's panel is packed
     edge to edge. Straight area loss AND a dead zone.
  3. Date pill and label pill were SEPARATED by a gap. In the reference the date pill sits ON TOP
     of the label pill's left end. "Tight beats tidy" (protocol hard rule 5) — the engine's
     instinct to separate is wrong here.
  4. The title text floated in a mostly-empty yellow card; the reference's type fills its card.
  5. MISSING: the pink sparkle bleeding off the RIGHT edge of the black panel.
  6. MISSING: the white circle straddling the panel's bottom edge.
  7. Only one sparkle in the title cluster; the reference has two black ones plus the green
     left-edge bleed.

DETAIL lever (per brain/DECISIONS.md session 9): detail tracks SMALL-TEXT DENSITY. Label type is
set at a moderate size with day abbreviations rather than blown up, which raises edge-per-pixel.
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles"); lay = load("layout")

W, H = core.SIZES["feed"]                     # 1080 x 1350 — feed, never assume taller
A = core.ACCENTS                              # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
PINK, MINT, LEMON, TOMATO, SKY = A[0], A[1], A[2], A[3], A[4]
MBRIGHT = "#00E5A0"   # --mintbright, a brand token — supplies the reference's light green
INK = "#0A0A0A"; CREAM = "#F4EFE0"; PAGE = "#EDE6D0"   # --bg2, a brand token (no invented colours)
SLUG = "091944e282ce11"
els = []

def E(label, x, y, w, h):
    els.append((label, x, y, w, h)); return None

# ── outer card on the page (the reference's white card + drop shadow) ─────────
CX, CY, CW, CH = 22, 27, 1036, 1242
card = (f'<div style="position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;height:{CH}px;'
        f'background:#FFFFFF;border-radius:46px;box-shadow:0 18px 44px rgba(0,0,0,.16);z-index:1"></div>')
L, R = 108, 972                                # content column inside the card
CWID = R - L                                   # 880

def sparkle(x, y, size, color, rot=0, z=25):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;'
            f'z-index:{z}">{dd.stamp("sparkle", color, rot=rot)}</div>')

# ── 1. TITLE CARD — type now FILLS it (v2 miss #4) ───────────────────────────
TY, TH = 104, 304
title = (f'<div style="position:absolute;left:{L}px;top:{TY}px;width:{CWID}px;height:{TH}px;'
         f'background:{LEMON};border-radius:40px;z-index:6"></div>'
         f'<div style="position:absolute;left:{L+44}px;top:{TY+58}px;width:{CWID-88}px;z-index:8;'
         f'font-family:var(--d);font-weight:900;font-size:104px;line-height:.9;white-space:nowrap;letter-spacing:-.035em;'
         f'color:{INK};text-transform:uppercase">OUR DRIVES.<br>THIS MONTH.</div>')
E("title_card", L, TY, CWID, TH)
# v2 miss #7 — the reference has TWO black sparkles clustered top-right, plus a green one
# bleeding off the card's left edge.
title += (sparkle(836, TY + 24, 90, INK, rot=6)
          + sparkle(902, TY + 118, 56, INK, rot=-12)
          + sparkle(70, TY + 168, 80, MINT, rot=10))

# ── 2. NAV ROW ───────────────────────────────────────────────────────────────
NY, NH = 425, 73
nav = (f'<div style="position:absolute;left:{L}px;top:{NY}px;width:{CWID}px;height:{NH}px;'
       f'background:{INK};border-radius:999px;z-index:5"></div>'
       f'<div style="position:absolute;left:{L+7}px;top:{NY+7}px;width:600px;height:{NH-14}px;'
       f'background:#FFFFFF;border-radius:999px;z-index:6"></div>'
       f'<div style="position:absolute;left:{L+14}px;top:{NY+13}px;width:47px;height:47px;'
       f'background:{INK};border-radius:50%;z-index:8;display:flex;align-items:center;'
       f'justify-content:center;color:#FFF;font-family:var(--m);font-size:22px">&rarr;</div>'
       f'<div style="position:absolute;left:{L+76}px;top:{NY}px;height:{NH}px;z-index:8;'
       f'display:flex;align-items:center;font-family:var(--d);font-weight:900;font-size:38px;'
       f'letter-spacing:-.01em;color:{INK};text-transform:uppercase">this month</div>'
       f'<div style="position:absolute;left:{L+620}px;top:{NY+7}px;width:237px;height:{NH-14}px;'
       f'background:{PINK};border-radius:999px;z-index:6;display:flex;align-items:center;'
       f'justify-content:center;font-family:var(--d);font-weight:900;font-size:38px;'
       f'color:#FFFFFF">2026</div>')
E("nav_bar", L, NY, CWID, NH)

# ── 3. THE BLACK PANEL — SIX rows, packed (v2 misses #1, #2, #3) ─────────────
PY, PH = 512, 510
PAD, ROWH, GAP = 28, 65, 13
panel = (f'<div style="position:absolute;left:{L}px;top:{PY}px;width:{CWID}px;height:{PH}px;'
         f'background:{INK};border-radius:38px;z-index:5"></div>')
E("panel", L, PY, CWID, PH)

# real AQ drives; day names are truthful for August 2026 (Aug 1 2026 = Saturday)
ROWS = [
    ("01", "SAT", "FOOD DRIVE",        LEMON,  MINT),
    ("07", "FRI", "TREE PLANTATION",   PINK,   SKY),
    ("12", "WED", "HEALTH CHECKUP",    MINT,   LEMON),
    ("18", "TUE", "CLOTHING DRIVE",    CREAM,  TOMATO),
    ("24", "MON", "DOG FEEDING",       SKY,    MBRIGHT),
    ("31", "MON", "SUNDARBAN VISIT",   PINK,   SKY),
]
DPX, DPW = 134, 202                # date pill
LBX, LBW = 266, 706                # label pill — starts INSIDE the date pill (70px overlap)
rows_html = ""
for i, (num, day, label, dcol, lcol) in enumerate(ROWS):
    ry = PY + PAD + i * (ROWH + GAP)
    lfg, dfg = core.text_on(lcol), core.text_on(dcol)
    # label pill first (z=7), date pill ON TOP (z=9) — the reference's overlap, not a gap
    rows_html += (
        f'<div style="position:absolute;left:{LBX}px;top:{ry}px;width:{LBW}px;height:{ROWH}px;'
        f'background:{lcol};border-radius:999px;z-index:7;display:flex;align-items:center;'
        f'padding-left:118px;font-family:var(--d);font-weight:900;font-size:34px;'
        f'letter-spacing:-.01em;color:{lfg};text-transform:uppercase">{label}</div>'
        f'<div style="position:absolute;left:{DPX}px;top:{ry}px;width:{DPW}px;height:{ROWH}px;'
        f'background:{dcol};border-radius:999px;z-index:9;display:flex;align-items:center;'
        f'justify-content:center;gap:12px">'
        f'<span style="font-family:var(--d);font-weight:900;font-size:40px;color:{dfg}">{num}</span>'
        f'<span style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.06em;'
        f'color:{dfg};opacity:.85">{day}</span></div>')
    E(f"row{i}", DPX, ry, (LBX + LBW) - DPX, ROWH)

# v2 miss #5 — pink sparkle bleeding off the panel's RIGHT edge
panel_extras = sparkle(922, PY + 244, 104, PINK, rot=-8, z=12)
# v2 miss #6 — white circle straddling the panel's BOTTOM edge
panel_extras += (f'<div style="position:absolute;left:508px;top:{PY+PH-30}px;width:60px;height:60px;'
                 f'background:#FFFFFF;border-radius:50%;z-index:12"></div>')

# ── 4. MORE INFORMATION BAR (two segments + seam sparkle) ────────────────────
IY, IH, SEAM = 1070, 55, 612
info = (f'<div style="position:absolute;left:{L}px;top:{IY}px;width:{SEAM-L}px;height:{IH}px;'
        f'background:{MINT};border-radius:999px 0 0 999px;z-index:6;display:flex;align-items:center;'
        f'padding-left:46px;font-family:var(--d);font-weight:900;font-size:26px;letter-spacing:.02em;'
        f'color:#FFFFFF;text-transform:uppercase">more information</div>'
        f'<div style="position:absolute;left:{SEAM}px;top:{IY}px;width:{R-SEAM}px;height:{IH}px;'
        f'background:{TOMATO};border-radius:0 999px 999px 0;z-index:6"></div>')
E("info_bar", L, IY, CWID, IH)
info += sparkle(SEAM - 38, IY - 40, 78, LEMON, rot=4, z=20)

# ── 5. URL BAR ───────────────────────────────────────────────────────────────
UY, UH = 1137, 79
url = (f'<div style="position:absolute;left:{L}px;top:{UY}px;width:{CWID}px;height:{UH}px;'
       f'background:#FFFFFF;border:3px solid {INK};border-radius:999px;z-index:6;display:flex;'
       f'align-items:center;padding-left:44px;font-family:var(--d);font-weight:900;font-size:30px;'
       f'letter-spacing:-.01em;color:{INK}">@ngo.aquaterra</div>'
       f'<div style="position:absolute;left:{R-70}px;top:{UY+13}px;width:52px;height:52px;'
       f'background:{LEMON};border-radius:50%;z-index:9;display:flex;align-items:center;'
       f'justify-content:center;font-family:var(--m);font-size:24px;color:{INK}">&rarr;</div>')
E("url_bar", L, UY, CWID, UH)

logo = f'<img src="{core.LOGO}" style="position:absolute;top:74px;left:{L}px;height:38px;z-index:30">'
E("logo", L, 74, 240, 38)

inner = (f'<div style="position:absolute;inset:0;background:{PAGE}"></div>'
         + card + logo + title + nav + panel + rows_html + panel_extras + info + url)
html = B.page(W, H, PAGE, inner, grain=False)

# date pill deliberately overlaps its own label pill — that IS the reference. Rows are tracked as
# one merged bbox each (see E(f"row{i}") above), so no by-design pair needs whitelisting.
pf = lay.preflight(W, H, els, html=html, page_bg=PAGE, core=core)

async def main():
    os.makedirs(f"out/versions/{SLUG}", exist_ok=True)
    out = f"out/versions/{SLUG}/v6.png"
    await B.render(html, out, W, H)
    print("wrote", out, "| preflight clean =", pf.get("clean"))
asyncio.run(main())
