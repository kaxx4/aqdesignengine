"""SHOWCASE 5e — five more families, applying the SMALL-TEXT-DENSITY finding.

PROVEN LAST BATCH: compare.py's detail_ratio tracks small-text density, not element count,
not texture, not interior linework. 20_numbered_brief (~21 runs of 19-34px type) scored 0.83 and
was the only piece to clear the 0.72 bar; 16_contact_sheet had MORE elements but one huge word
each and scored 0.40. So every piece here carries captions, labels, sub-copy and fine rules.

 21 10f1b8a9789  annotated headline -> per-line word highlight containers + running rules
 22 e9d82bbdf04  corner arcs        -> giant quarter-circles cropped at all four corners
 23 ffc106f26f5  band-stack sign    -> full-width colour bands, one type style each, in a plate
 24 23bb507f6ec  object spine       -> labelled plates cantilevered off a vertical pole
 25 620d62f101b  photo card stack   -> fanned rotated cards on black, permitted occlusion
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

def mono(t, s=13, c="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')

def micro(t, s=17, c="#3A3A3A"):
    return f'<span style="font-family:var(--e);font-weight:600;font-size:{s}px;color:{c}">{t}</span>'


# ── 21. ANNOTATED HEADLINE ────────────────────────────────────────────────────
async def annotated_headline():
    """10f1b8a9789: editorial headline stack where exactly ONE word per line sits in a different
    container shape, plus hairline rules top and bottom and a dense sub-copy block."""
    els = []
    rule = lambda y: f'<div style="position:absolute;top:{y}px;left:{M}px;right:{M}px;height:2px;background:rgba(10,10,10,.30);z-index:20"></div>'
    lines = [("how showing up", None, None),
             ("changes", "a street", A[2]),
             ("faster than", None, None),
             ("any", "donation", A[0])]
    y = 300
    for plain, hl, acc in lines:
        seg = f'<span style="color:var(--ink)">{plain}</span>'
        if hl:
            seg += (f'<span style="display:inline-block;background:{acc};color:{TON(acc)};'
                    f'padding:2px 16px;margin-left:14px;border:4px solid var(--ink);'
                    f'transform:rotate(-2deg);box-shadow:6px 6px 0 var(--ink)">{hl}</span>')
        els.append(at(M, y, W - 2*M, 110,
            f'<div style="font-family:var(--d);font-weight:900;font-size:62px;line-height:1;'
            f'text-transform:lowercase">{seg}</div>', z=24))
        y += 120
    # dense sub-copy — the detail driver
    facts = [("01", "one saturday", "that is the entire commitment we ask for"),
             ("02", "no fee, no cv", "you are not applying, you are just coming"),
             ("03", "1,200 of us", "every one of them started with a single drive"),
             ("04", "five lanes", "welfare, climate, education, animals, health")]
    fy = 800
    for n, t, s in facts:
        els.append(at(M, fy, W - 2*M, 74,
            f'<div style="display:flex;gap:18px;align-items:baseline;border-bottom:1.5px solid rgba(10,10,10,.18);'
            f'padding-bottom:10px">{mono(n,15,A[6])}'
            f'<span style="font-family:var(--d);font-weight:900;font-size:26px;text-transform:uppercase">{t}</span>'
            f'{micro(s,17)}</div>', z=22))
        fy += 84
    for x, y2, s, acc, sh, r in [(880, 170, 120, A[4], S.starburst(10), 12),
                                 (770, 210, 78, A[3], S.blob(4, 7), 0),
                                 (930, 300, 66, A[5], S.scallop(11), -8)]:
        els.append(at(x, y2, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + rule(150) + rule(1200) + "".join(els) + logo() + footer() + eyebrow("AQ · 02 / 06"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 22. CORNER ARCS ───────────────────────────────────────────────────────────
async def corner_arcs():
    """e9d82bbdf04: giant concentric quarter-circles anchored at each canvas corner, only a
    quarter visible — kills dead quadrants with zero filler doodles."""
    arcs = ""
    for (cx, cy, cols) in [(0, 0, [A[3], A[2]]), (W, 0, [A[4], A[6]]),
                           (0, H, [A[5], A[0]]), (W, H, [A[1], A[2]])]:
        for i, col in enumerate(cols):
            r = 250 - i * 95
            arcs += (f'<div style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;'
                     f'height:{2*r}px;border-radius:50%;background:{col};z-index:{2+i}"></div>')
    els = []
    els.append(at(M, 430, W - 2*M, 260,
        f'<div style="font-family:var(--d);font-weight:900;font-size:112px;line-height:.9;'
        f'text-transform:uppercase;color:var(--ink);text-align:center">show up<br>in colour</div>', z=20))
    # dense label row + sub-copy
    tags = [("WELFARE", A[0]), ("CLIMATE", A[1]), ("EDUCATION", A[4]), ("ANIMALS", A[5]), ("HEALTH", A[6])]
    row = "".join(f'<span style="background:{a};color:{TON(a)};border:3px solid var(--ink);'
                  f'border-radius:999px;padding:8px 18px;font-family:var(--m);font-weight:700;'
                  f'font-size:15px;letter-spacing:.08em">{t}</span>' for t, a in tags)
    els.append(at(M, 730, W - 2*M, 60,
        f'<div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap">{row}</div>', z=22))
    els.append(at(210, 820, 660, 210,
        f'<div style="text-align:center;line-height:1.55">'
        + micro("aquaterra is run entirely by teenagers in kolkata. no fees, no interviews, "
                "no minimum hours. pick a lane, come once, and decide after.", 21) + "</div>", z=22))
    els.append(at(410, 1060, 260, 80,
        f'<div style="width:100%;height:100%;background:var(--ink);border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">{mono("DM TO JOIN", 18, "#FFF")}</div>', z=24))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>' + arcs
             + "".join(els) + logo() + footer() + eyebrow("AQ · FIVE LANES"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 23. BAND-STACK SIGN ───────────────────────────────────────────────────────
async def band_sign():
    """ffc106f26f5: the message as a vertical stack of full-width colour BANDS inside one
    bordered plate, each band a different type style (eyebrow bar / rule-flanked kicker /
    giant condensed / script kicker)."""
    bands = [
        (A[3], 92, "mono", "NEW AT AQUATERRA", 20, "#FFF"),
        (CREAM, 110, "rule", "THE SATURDAY", 34, "var(--ink)"),
        (A[2], 285, "giant", "CLEAN UP", 122, "#0A0A0A"),
        (CREAM, 120, "serif", "your choice of lane.", 46, "var(--ink)"),
        (A[6], 96, "mono", "DIAMOND HARBOUR · 07:00", 18, "#FFF"),
        (A[4], 92, "mono", "BUS FROM ESPLANADE · FREE", 18, "#FFF"),
    ]
    rows, y = "", 0
    for bg, h, kind, txt, fs, fg in bands:
        if kind == "mono":
            content = mono(txt, fs, fg, ".14em")
        elif kind == "rule":
            content = (f'<div style="display:flex;align-items:center;gap:16px;width:100%;padding:0 30px">'
                       f'<div style="flex:1;height:3px;background:var(--ink)"></div>'
                       f'<span style="font-family:var(--d);font-weight:900;font-size:{fs}px;'
                       f'text-transform:uppercase;color:{fg};white-space:nowrap">{txt}</span>'
                       f'<div style="flex:1;height:3px;background:var(--ink)"></div></div>')
        elif kind == "giant":
            content = (f'<span style="font-family:var(--d);font-weight:900;font-size:{fs}px;'
                       f'line-height:.9;text-transform:uppercase;color:{fg};letter-spacing:-.02em">{txt}</span>')
        else:
            content = (f'<span style="font-family:var(--s);font-style:italic;font-size:{fs}px;'
                       f'color:{fg}">{txt}</span>')
        rows += (f'<div style="height:{h}px;background:{bg};display:flex;align-items:center;'
                 f'justify-content:center;border-bottom:4px solid var(--ink)">{content}</div>')
        y += h
    plate = at(58, 165, 964, y + 8,
        f'<div style="width:100%;border:8px solid var(--ink);box-shadow:16px 16px 0 rgba(0,0,0,.5);'
        f'overflow:hidden;background:{CREAM}">{rows}</div>', z=20, rot=-1)
    els = [plate]
    for x, yy, s, acc, sh, r in [(80, 170, 130, A[0], S.starburst(11), -12),
                                 (890, 940, 120, A[5], S.scallop(12), 10),
                                 (110, 1010, 100, A[1], S.gear(8), 0)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#2C6E8F"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · NOTICE", "#FFFFFF"))
    return B.page(W, H, "#2C6E8F", inner, grain=True)


# ── 24. OBJECT SPINE ──────────────────────────────────────────────────────────
async def object_spine():
    """23bb507f6ec: a vertical pole with labelled plates cantilevered off it at alternating
    angles — a legible way to hang a list off one axis with no container boxes."""
    els = []
    sx = 470
    els.append(f'<div style="position:absolute;left:{sx-14}px;top:250px;width:28px;height:880px;'
               f'background:var(--ink);z-index:8"></div>')
    els.append(f'<div style="position:absolute;left:{sx-70}px;top:1120px;width:140px;height:26px;'
               f'background:var(--ink);border-radius:6px;z-index:8"></div>')
    plates = [("WELFARE", "food + kits", A[3], "left", 300),
              ("CLIMATE", "trees + cleanups", A[1], "right", 420),
              ("EDUCATION", "sunderbans schools", A[4], "left", 540),
              ("ANIMALS", "street feeding", A[0], "right", 660),
              ("HEALTH", "camps + checkups", A[6], "left", 780),
              ("YOU", "whichever fits", A[2], "right", 900)]
    for name, sub, acc, side, y in plates:
        w = 330
        x = sx - w - 10 if side == "left" else sx + 10
        rot = -3 if side == "left" else 3
        els.append(at(x, y, w, 96,
            f'<div style="width:100%;height:100%;background:{acc};border:5px solid var(--ink);'
            f'box-shadow:7px 7px 0 var(--ink);display:flex;flex-direction:column;'
            f'justify-content:center;padding-left:22px;box-sizing:border-box">'
            f'<span style="font-family:var(--d);font-weight:900;font-size:32px;'
            f'text-transform:uppercase;color:{TON(acc)};line-height:1">{name}</span>'
            f'{mono(sub, 13, TON(acc), ".06em")}</div>', z=14, rot=rot))
    els.append(at(M, 150, W - 2*M, 90,
        f'<div style="font-family:var(--d);font-weight:900;font-size:70px;line-height:.92;'
        f'text-transform:uppercase;text-align:center;color:var(--ink)">which way in?</div>', z=20))
    els.append(at(240, 1180, 600, 70,
        f'<div style="text-align:center">' + micro("all five run every month. you can switch lanes "
        "any time, or do all of them.", 20) + "</div>", z=20))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · SIGNPOST"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 25. PHOTO CARD STACK ──────────────────────────────────────────────────────
async def card_stack():
    """620d62f101b: a fanned stack of rotated cards on black with DELIBERATE partial occlusion —
    a later card covers ~35% of an earlier one and that is the point (collision_check would
    reject this outright; it needs an allow_occlusion intent)."""
    els = []
    cards = [
        (A[3], 120, 250, 560, 380, -6, "SATURDAY", "BEACH CLEAN", "diamond harbour · 07:00"),
        (A[2], 300, 470, 560, 360, 4, "SUNDAY", "MEDICAL CAMP", "sunderbans · 09:30"),
        (CREAM, 170, 700, 560, 350, -3, "WEDNESDAY", "SCHOOL KITS", "khidirpur · 16:00"),
        (A[4], 430, 900, 520, 320, 7, "SUNDAY", "FOOD RUN", "kolkata · 11:00"),
    ]
    for i, (bg, x, y, w, h, rot, day, title, sub) in enumerate(cards):
        fg = TON(bg) if bg != CREAM else "var(--ink)"
        els.append(at(x, y, w, h,
            f'<div style="width:100%;height:100%;background:{bg};border:5px solid var(--ink);'
            f'box-shadow:12px 12px 0 rgba(0,0,0,.6);padding:22px 26px;box-sizing:border-box;'
            f'display:flex;flex-direction:column;justify-content:space-between">'
            f'<div style="display:flex;justify-content:space-between">{mono(day,14,fg)}{mono(f"0{i+1}",14,fg)}</div>'
            f'<div style="font-family:var(--d);font-weight:900;font-size:54px;line-height:.92;'
            f'text-transform:uppercase;color:{fg}">{title}</div>'
            f'<div style="border-top:2px solid {fg};padding-top:8px">{mono(sub,13,fg,".05em")}</div>'
            f'</div>', z=10 + i * 2, rot=rot))
    els.append(at(640, 300, 300, 130,
        f'<div style="width:100%;height:100%;background:var(--ink);border:4px solid #FFF;'
        f'border-radius:999px;display:flex;align-items:center;justify-content:center;text-align:center">'
        + mono("FOUR DRIVES<br>THIS MONTH", 19, "#FFF") + "</div>", z=40, rot=9))
    for x, y, s, acc, sh, r in [(60, 640, 110, A[0], S.starburst(10), -14),
                                (900, 720, 96, A[5], S.blob(6, 8), 0),
                                (740, 1180, 88, A[1], S.scallop(11), 8)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=44, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · AUGUST", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


JOBS = [("21_annotated_headline", annotated_headline), ("22_corner_arcs", corner_arcs),
        ("23_band_sign", band_sign), ("24_object_spine", object_spine),
        ("25_card_stack", card_stack)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
