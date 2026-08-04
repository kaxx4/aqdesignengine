"""SHOWCASE 5d — five HIGH-GRANULARITY families, testing the detail hypothesis.

DETAIL HYPOTHESIS (this batch is the experiment):
compare.py's detail_ratio = edge energy per unit CONTENT pixel. Two fixes were tried and BOTH
failed to move it: shapes.interior() inner strokes (0.76->0.82) and page grain (0.82->0.82, it
averages out at analysis resolution). So detail is NOT texture — it is GRANULARITY. Edges-per-pixel
is high when a composition is subdivided into many small labelled parts and low when it is a few
large flat blocks. The references are finely subdivided; earlier AQ recreations used big blocks.
Every piece here is deliberately built from MANY SMALL LABELLED PARTS. If detail_ratio clears the
0.72 blocking threshold, the hypothesis holds and the fix is compositional, not decorative.

 16 17c7de5509  contact-sheet grid  -> 7 tiles, each a mini-composition of the same word
 17 4c6df2b479  events board        -> masonry of 6 event cards + eyebrow rail + hotline strip
 18 ce6fdd94f8  moodboard collage   -> many overlapping cards/stickers on black, diagonal read
 19 c10cb35dfa  two-panel collage   -> horizontal split, headline collage over object+giant type
 20 3bb3f9582d  numbered brief      -> white sheet on dark, 01-07 list, per-item accent rotation
"""
import asyncio, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS
CREAM = "var(--bg)"
TON = core.text_on

def at(x, y, w, h, inner, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def logo(dark=False):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:38px;z-index:60;{sh}">'

def footer(light=False):
    c = "#FFFFFF" if light else "var(--ink)"
    return (f'<span style="position:absolute;bottom:50px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:60">@ngo.aquaterra</span>')

def eyebrow(txt, color="var(--ink)"):
    return (f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:60">{txt}</span>')

def mono(txt, size=13, color="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{size}px;'
            f'letter-spacing:{ls};text-transform:uppercase;color:{color}">{txt}</span>')


# ── 16. CONTACT-SHEET GRID ────────────────────────────────────────────────────
async def contact_sheet():
    """17c7de5509: the SAME word rendered 7 ways in a gutterless tile grid, unified by one
    full-width caption strip. Granularity comes from 7 independent mini-compositions."""
    els = []
    tiles = [
        (0, 150, 360, 300, A[0], "SHOW UP", "d", 54, "#FFF"),
        (360, 150, 360, 300, "#0A0A0A", "show up", "s", 62, A[2]),
        (720, 150, 360, 300, A[4], "SHOW<br>UP", "d", 48, "#0A0A0A"),
        (0, 450, 540, 280, A[2], "show up", "e", 56, "#0A0A0A"),
        (540, 450, 540, 280, A[5], "SHOW UP", "m", 34, "#FFF"),
        (0, 730, 360, 300, A[6], "SHOW<br>UP", "d", 50, "#FFF"),
        (360, 730, 720, 300, A[3], "show up.", "s", 74, "#FFF"),
    ]
    fam = {"d": "var(--d)", "s": "var(--s)", "e": "var(--e)", "m": "var(--m)"}
    for i, (x, y, w, h, bg, txt, f, fs, fg) in enumerate(tiles):
        ital = "font-style:italic;" if f == "s" else ""
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:{bg};display:flex;align-items:center;'
            f'justify-content:center;border:2px solid rgba(10,10,10,.35);box-sizing:border-box">'
            f'<div style="font-family:{fam[f]};{ital}font-weight:900;font-size:{fs}px;line-height:.92;'
            f'color:{fg};text-align:center;letter-spacing:{".08em" if f=="m" else "0"}">{txt}</div></div>', z=10))
        # per-tile index chip — granularity: 7 more small labelled parts
        els.append(at(x + 12, y + 12, 46, 30,
            f'<div style="width:100%;height:100%;background:{CREAM};border:2px solid #0A0A0A;'
            f'display:flex;align-items:center;justify-content:center">{mono(f"{i+1:02d}", 12)}</div>', z=20))
    strip = (f'<div style="position:absolute;top:1030px;left:0;right:0;height:120px;background:#0A0A0A;'
             f'display:flex;align-items:center;justify-content:space-between;padding:0 {M}px;z-index:22">'
             + mono("SEVEN WAYS", 20, "#FFF") + mono("ONE ASK", 20, A[2])
             + mono("AQUATERRA", 20, "#FFF") + "</div>")
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + strip + logo() + footer() + eyebrow("AQ · TYPE STUDY"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 17. EVENTS BOARD (masonry + rails) ────────────────────────────────────────
async def events_board():
    """4c6df2b479: masonry of event cards on black with a mono eyebrow rail and a footer strip.
    Granularity: 6 cards, each with 4 labelled sub-parts (day / title / place / time)."""
    els = []
    rail = (f'<div style="position:absolute;top:130px;left:{M}px;right:{M}px;display:flex;'
            f'justify-content:space-between;z-index:30">' + mono("AQUATERRA", 15, "#FFF")
            + mono("KOLKATA", 15, A[2]) + mono("PRESENTS", 15, "#FFF") + "</div>")
    cards = [
        (M, 190, 460, 300, A[4], "SAT", "beach cleanup", "diamond harbour", "07:00"),
        (M + 480, 190, 472, 300, A[2], "SUN", "medical camp", "sunderbans", "09:30"),
        (M, 510, 300, 290, A[0], "WED", "school kits", "khidirpur", "16:00"),
        (M + 320, 510, 300, 290, A[1], "SAT", "tree drive", "rajarhat", "08:00"),
        (M + 640, 510, 312, 290, A[5], "SUN", "food run", "kolkata", "11:00"),
        (M, 820, 952, 240, A[6], "TUE", "volunteer orientation", "online · zoom", "19:00"),
    ]
    for x, y, w, h, acc, day, title, place, time in cards:
        fg = TON(acc)
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:26px;padding:20px 24px;'
            f'box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">'
            f'{mono(day,14,fg)}{mono(time,14,fg)}</div>'
            f'<div style="font-family:var(--d);font-weight:900;font-size:{40 if w>400 else 32}px;'
            f'line-height:.94;text-transform:uppercase;color:{fg}">{title}</div>'
            f'<div style="border-top:2px solid {fg};opacity:.75;padding-top:8px">{mono(place,12,fg)}</div>'
            f'</div>', z=10))
    els.append(at(520, 470, 92, 92, S.sticker(S.starburst(9), A[3], size=92), z=30, rot=-10))
    els.append(at(330, 780, 76, 76, S.sticker(S.scallop(11), A[2], size=76), z=30, rot=8))
    strip = (f'<div style="position:absolute;bottom:110px;left:{M}px;right:{M}px;height:78px;'
             f'border:3px solid #FFF;border-radius:999px;display:flex;align-items:center;'
             f'justify-content:center;z-index:24">' + mono("DM @NGO.AQUATERRA TO JOIN ANY OF THEM", 17, "#FFF") + "</div>")
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>' + rail
             + "".join(els) + strip + logo(True) + footer(True) + eyebrow("AQ · AUGUST", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


# ── 18. MOODBOARD COLLAGE ─────────────────────────────────────────────────────
async def moodboard():
    """ce6fdd94f8: overlapping promo cards + photo cards + stickers on black, arranged on a loose
    top-left -> bottom-right diagonal, with blob stickers STRADDLING card edges to bind the pile."""
    els = []
    cards = [
        (70, 170, 430, 250, A[4], "AN EVENING WITH", "AQUATERRA", -4),
        (520, 260, 400, 210, A[3], "VOLUNTEER", "INTAKE 2026", 5),
        (110, 460, 360, 230, A[2], "SINCE", "2021", -6),
        (470, 520, 470, 250, "#FFFFFF", "1,200", "PEOPLE", 3),
        (90, 730, 420, 240, A[5], "FIVE", "PROGRAMMES", 4),
        (540, 800, 400, 220, A[1], "NO FEES", "EVER", -5),
    ]
    for x, y, w, h, bg, l1, l2 in [(c[0], c[1], c[2], c[3], c[4], c[5], c[6]) for c in cards]:
        pass
    for x, y, w, h, bg, l1, l2, rot in cards:
        fg = TON(bg) if bg != "#FFFFFF" else "#0A0A0A"
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:{bg};border:4px solid #0A0A0A;'
            f'box-shadow:9px 9px 0 rgba(0,0,0,.55);padding:18px 22px;box-sizing:border-box;'
            f'display:flex;flex-direction:column;justify-content:center;gap:4px">'
            f'{mono(l1,15,fg)}'
            f'<div style="font-family:var(--d);font-weight:900;font-size:46px;line-height:.94;'
            f'text-transform:uppercase;color:{fg}">{l2}</div></div>', z=10, rot=rot))
    # stickers straddling card seams (the binding move)
    for x, y, s, acc, sh, r in [(470, 400, 110, A[0], S.blob(3, 8), -10), (430, 700, 96, A[6], S.scallop(12), 8),
                                (880, 470, 90, A[2], S.starburst(9), 14), (60, 660, 84, A[3], S.gear(8), 0)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    band = (f'<div style="position:absolute;bottom:120px;left:{M}px;right:{M}px;height:86px;'
            f'background:{A[2]};display:flex;align-items:center;justify-content:center;z-index:34;'
            f'border:4px solid #0A0A0A">' + mono("SHOW UP · ANY LANE · ANY SATURDAY", 19, "#0A0A0A") + "</div>")
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + band + logo(True) + footer(True) + eyebrow("AQ · BOARD", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


# ── 19. TWO-PANEL COLLAGE ─────────────────────────────────────────────────────
async def two_panel():
    """c10cb35dfa: two saturated fields split horizontally; a light 'torn paper' headline card
    over the top panel, and an object overlapping giant type in the bottom panel."""
    els = []
    els.append(f'<div style="position:absolute;top:0;left:0;right:0;height:660px;background:{A[4]};z-index:1"></div>')
    els.append(f'<div style="position:absolute;top:660px;left:0;right:0;bottom:0;background:{A[3]};z-index:1"></div>')
    # headline card + small labelled parts
    els.append(at(90, 200, 620, 330,
        f'<div style="width:100%;height:100%;background:{CREAM};border:5px solid #0A0A0A;'
        f'box-shadow:12px 12px 0 rgba(0,0,0,.45);padding:26px 30px;box-sizing:border-box;'
        f'display:flex;flex-direction:column;justify-content:space-between">'
        f'{mono("VOLUNTEER PROGRAMME · 2026", 14)}'
        f'<div style="font-family:var(--d);font-weight:900;font-size:76px;line-height:.9;'
        f'text-transform:uppercase;color:#0A0A0A">we leave<br>a mark</div>'
        f'<div style="display:flex;gap:8px">'
        + "".join(f'<span style="background:{a};border:2px solid #0A0A0A;padding:5px 12px;'
                  f'font-family:var(--m);font-weight:700;font-size:12px;color:{TON(a)}">{t}</span>'
                  for a, t in [(A[0], "WELFARE"), (A[1], "CLIMATE"), (A[2], "EDU"), (A[5], "HEALTH")])
        + f'</div></div>', z=14, rot=-2))
    for x, y, s, acc, sh, r in [(740, 180, 130, A[2], S.starburst(10), 12), (800, 400, 105, A[0], S.blob(5, 8), 0),
                                (690, 540, 92, A[5], S.gear(9), -8)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=20, rot=r))
    # bottom panel: giant type with an object overlapping it (permitted occlusion)
    els.append(f'<div style="position:absolute;top:720px;left:{M}px;font-family:var(--d);font-weight:900;'
               f'font-size:230px;line-height:.82;text-transform:uppercase;color:{CREAM};z-index:10">WE</div>')
    els.append(at(300, 760, 330, 330, S.sticker(S.scallop(15), A[2], size=330,
                inner=S.label("1,200", 19, 46) + S.label("VOLUNTEERS", 10, 64)), z=18, rot=-6))
    els.append(f'<div style="position:absolute;bottom:150px;left:{M}px;right:{M}px;'
               f'font-family:var(--e);font-weight:700;font-size:30px;color:#FFF;z-index:20">'
               f'one saturday a month. that is the whole ask.</div>')
    inner = "".join(els) + logo(True) + footer(True) + eyebrow("AQ · CAMPAIGN", "#FFFFFF")
    return B.page(W, H, A[4], inner, grain=True)


# ── 20. NUMBERED BRIEF ────────────────────────────────────────────────────────
async def numbered_brief():
    """3bb3f9582d: a white sheet on a dark surface carrying a numbered list where each 'NN / label'
    pair takes the next accent in sequence — a mono list reading as a rainbow index.
    Granularity: 7 rows x 3 labelled parts each."""
    els = []
    els.append(at(70, 150, 940, 1010,
        f'<div style="width:100%;height:100%;background:#FFFFFF;box-shadow:16px 16px 0 rgba(0,0,0,.5)"></div>',
        z=8, rot=-1.5))
    rows = [("01", "pick a lane", "welfare · climate · edu · animals · health"),
            ("02", "show up once", "no interview, no cv, no fee"),
            ("03", "get paired", "you shadow someone on your first drive"),
            ("04", "do the work", "sorting, teaching, planting, feeding"),
            ("05", "log the day", "so the next drive is better planned"),
            ("06", "bring one friend", "that is how all 1,200 of us got here"),
            ("07", "keep going", "or don't. no guilt either way")]
    y = 300
    for i, (num, title, sub) in enumerate(rows):
        acc = A[i % 7]
        els.append(at(120, y, 850, 108,
            f'<div style="width:100%;height:100%;display:flex;align-items:center;gap:22px;'
            f'border-bottom:2px solid rgba(10,10,10,.18)">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:46px;color:{acc};'
            f'min-width:82px">{num}</div>'
            f'<div style="flex:1">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:34px;text-transform:uppercase;'
            f'color:{acc};line-height:1">{title}</div>'
            f'<div style="font-family:var(--e);font-weight:600;font-size:19px;color:#3A3A3A;'
            f'margin-top:3px">{sub}</div></div></div>', z=14, rot=-1.5))
        y += 112
    head = at(120, 190, 850, 100,
        f'<div style="font-family:var(--d);font-weight:900;font-size:64px;line-height:.9;'
        f'text-transform:uppercase;color:#0A0A0A">how to<br></div>', z=14, rot=-1.5)
    els.append(head)
    # sticky-note overlay + a couple of stickers = more small parts
    els.append(at(700, 130, 220, 170,
        f'<div style="width:100%;height:100%;background:{A[2]};box-shadow:7px 7px 0 rgba(0,0,0,.4);'
        f'display:flex;align-items:center;justify-content:center;font-family:var(--d);'
        f'font-weight:900;font-size:34px;color:#0A0A0A;text-align:center">START<br>HERE</div>', z=24, rot=7))
    els.append(at(60, 1080, 130, 130, S.sticker(S.scallop(12), A[0], size=130), z=26, rot=-9))
    inner = ('<div style="position:absolute;inset:0;background:#171717"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · ONBOARDING", "#FFFFFF"))
    return B.page(W, H, "#171717", inner, grain=True)


JOBS = [("16_contact_sheet", contact_sheet), ("17_events_board", events_board),
        ("18_moodboard", moodboard), ("19_two_panel", two_panel),
        ("20_numbered_brief", numbered_brief)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
