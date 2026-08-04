"""SHOWCASE 5f — five more, applying EVERY rule learned so far.

RULES IN FORCE (all measured, all in DECISIONS.md):
 - detail_ratio tracks SMALL-TEXT DENSITY -> every piece carries captions/labels/sub-copy
 - big flat masses inflate area while crushing detail -> no oversized flat blocks
 - target area ~0.9-1.1x, content pushed to all four margins, never sitting high
 - uniform shapes.sticker() treatment on every object

 26 ca484173fb  diagonal cascade -> stepped Gantt bars, x_i = x0+i*dx, y_i = y0+i*dy (the stub spec)
 27 cfec9bd415  flat-lay tableau -> nested offset rotated sheets + labelled props on a speckled ground
 28 a99a4af4ca  radial orbit     -> centre focal + ring of labelled satellites
 29 841552212f  giant type       -> huge word + dense annotation column
 30 67b12a3cd4  stacked zones    -> row list with per-row sub-copy
"""
import asyncio, os, sys, importlib.util, math
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

def eyebrow(t, c="var(--ink)"):
    return (f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{c};z-index:60">{t}</span>')

def mono(t, s=13, c="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')

def micro(t, s=17, c="#3A3A3A"):
    return f'<span style="font-family:var(--e);font-weight:600;font-size:{s}px;color:{c}">{t}</span>'


# ── 26. DIAGONAL CASCADE ──────────────────────────────────────────────────────
async def diagonal_cascade():
    """ca484173fb, the exact stub spec: N labelled bars each offset right AND down from the
    previous by a fixed delta, one dot terminator per bar — a self-explaining timeline."""
    els = []
    els.append(at(M, 250, W - 2*M, 830,
        f'<div style="width:100%;height:100%;background:{CREAM};border-radius:34px;'
        f'box-shadow:14px 14px 0 rgba(0,0,0,.55)"></div>', z=8))
    rows = [("JAN", "orientation", 0, 300, A[4]), ("MAR", "first drives", 1, 340, A[2]),
            ("MAY", "sunderbans camp", 2, 390, A[0]), ("JUL", "monsoon kits", 3, 330, A[1]),
            ("SEP", "school term starts", 4, 420, A[5]), ("NOV", "winter drive", 5, 360, A[6]),
            ("DEC", "year close", 6, 300, A[3])]
    x0, y0, dx, dy = 150, 350, 46, 92
    for lbl, name, i, bw, acc in rows:
        x, y = x0 + i * dx, y0 + i * dy
        els.append(at(x, y, bw, 62,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:999px;'
            f'display:flex;align-items:center;padding-left:22px;box-sizing:border-box;gap:14px">'
            f'{mono(lbl, 14, TON(acc))}'
            f'<span style="font-family:var(--d);font-weight:900;font-size:24px;'
            f'text-transform:uppercase;color:{TON(acc)}">{name}</span></div>', z=14))
        els.append(at(x + bw + 12, y + 19, 24, 24,
            f'<div style="width:24px;height:24px;border-radius:50%;background:#FFFFFF"></div>', z=14))
        els.append(at(x - 96, y + 18, 84, 26,
            f'<div style="text-align:right">{micro(f"{i*2+2} drives", 14, "#6A6A6A")}</div>', z=14))
    els.append(at(150, 270, 700, 70,
        f'<div style="font-family:var(--d);font-weight:900;font-size:52px;text-transform:uppercase;'
        f'color:var(--ink)">the year, in order</div>', z=14))
    els.append(at(150, 1000, 780, 60,
        f'<div>{micro("every bar is a real drive you can still join. dates shift with monsoon and exams.", 19)}</div>', z=14))
    inner = ('<div style="position:absolute;inset:0;background:#141414"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · TIMELINE", "#FFFFFF"))
    return B.page(W, H, "#141414", inner, grain=True)


# ── 27. FLAT-LAY TABLEAU ──────────────────────────────────────────────────────
async def flat_lay():
    """cfec9bd415: nest the hero inside two offset rotated sheets — a base sheet peeking out on
    two sides, then the main surface on top — instant depth and a built-in frame."""
    speck = "".join(f'<circle cx="{(i*137)%1080}" cy="{(i*271)%1350}" r="{2+(i%3)}" fill="#0A0A0A" opacity=".16"/>'
                    for i in range(320))
    ground = (f'<svg style="position:absolute;inset:0;z-index:2" width="1080" height="1350" '
              f'xmlns="http://www.w3.org/2000/svg">{speck}</svg>')
    els = []
    els.append(at(110, 250, 880, 800, f'<div style="width:100%;height:100%;background:{A[3]};'
                f'border:4px solid var(--ink)"></div>', z=6, rot=3))
    els.append(at(90, 230, 880, 800, f'<div style="width:100%;height:100%;background:{A[1]};'
                f'border:5px solid var(--ink);box-shadow:12px 12px 0 rgba(0,0,0,.3)"></div>', z=8, rot=-2))
    # the "paper" hero + labelled props
    els.append(at(180, 300, 520, 470,
        f'<div style="width:100%;height:100%;background:#FBF8F0;border:4px solid var(--ink);'
        f'padding:26px;box-sizing:border-box;display:flex;flex-direction:column;gap:12px">'
        f'{mono("DRIVE CHECKLIST", 15)}'
        f'<div style="font-family:var(--d);font-weight:900;font-size:44px;line-height:.94;'
        f'text-transform:uppercase">what to<br>bring</div>'
        + "".join(f'<div style="display:flex;gap:10px;align-items:baseline;'
                  f'border-bottom:1.5px solid rgba(10,10,10,.2);padding-bottom:7px">'
                  f'{mono(f"{i+1:02d}", 13, A[6])}{micro(t, 18)}</div>'
                  for i, t in enumerate(["water bottle", "closed shoes", "a cap", "your id", "one friend"]))
        + "</div>", z=14, rot=-2))
    props = [(S.capsule(100, 40), A[2], 740, 330, 190, 12, "PEN"),
             (S.blob(4, 8), A[4], 760, 520, 165, 0, "MUG"),
             (S.tag(100, 44), A[5], 700, 700, 210, -8, "TAG"),
             (S.gear(9), A[0], 200, 830, 150, 0, "KIT"),
             (S.scallop(12), A[6], 420, 850, 140, 7, "AQ")]
    for d, f, x, y, s, r, lab in props:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, rot=r,
                      inner=S.label(lab, 13, 55, fill=TON(f))), z=20))
    els.append(at(120, 1090, 840, 120,
        f'<div style="text-align:center;line-height:1.5">'
        + micro("show up at 7am. we bring the gloves, bags, and the rest. "
                "no experience needed, no fee, ever.", 21) + "</div>", z=24))
    inner = (f'<div style="position:absolute;inset:0;background:{A[4]}"></div>' + ground
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · KIT LIST", "#FFFFFF"))
    return B.page(W, H, A[4], inner, grain=True)


# ── 28. RADIAL ORBIT ──────────────────────────────────────────────────────────
async def radial_orbit():
    els = []
    cx, cy, R = 540, 690, 372
    els.append(f'<div style="position:absolute;left:{cx-R}px;top:{cy-R}px;width:{2*R}px;height:{2*R}px;'
               f'border-radius:50%;border:3px dashed rgba(10,10,10,.35);z-index:4"></div>')
    els.append(at(cx - 205, cy - 205, 410, 410,
        S.sticker(S.scallop(15), A[6], size=410,
                  inner=S.label("1,200", 24, 44, fill="#FFF") + S.label("VOLUNTEERS", 11, 62, fill="#FFF")), z=20))
    sats = [("FOOD", A[3], "42 drives"), ("TREES", A[1], "3,100 planted"), ("BOOKS", A[4], "9 schools"),
            ("DOGS", A[0], "weekly"), ("CLOTHES", A[5], "winter only"), ("HEALTH", A[2], "6 camps")]
    for i, (name, acc, sub) in enumerate(sats):
        ang = -math.pi / 2 + i * 2 * math.pi / len(sats)
        s = 200 if i % 2 == 0 else 172
        x, y = cx + R * math.cos(ang) - s // 2, cy + R * math.sin(ang) - s // 2
        els.append(at(int(x), int(y), s, s,
            S.sticker(S.starburst(10) if i % 2 else S.blob(i + 2, 8), acc, size=s,
                      inner=S.label(name, 13, 55, fill=TON(acc))), z=24, rot=(i * 13) % 20 - 10))
        els.append(at(int(x) - 20, int(y) + s + 4, s + 40, 24,
            f'<div style="text-align:center">{mono(sub, 12, "#4A4A4A", ".05em")}</div>', z=24))
    els.append(at(M, 160, W - 2*M, 110,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:64px;'
        f'line-height:.92;text-transform:uppercase;color:var(--ink)">six ways<br>to show up</div>', z=26))
    els.append(at(160, 1110, 760, 100,
        f'<div style="text-align:center;line-height:1.5">'
        + micro("pick any one, or all six. every number here is a real count from 2025, "
                "logged by the volunteers who did it.", 19) + "</div>", z=26))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · PROGRAMMES"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 29. GIANT TYPE + ANNOTATION COLUMN ────────────────────────────────────────
async def giant_type():
    els = []
    els.append(at(M, 200, W - 2*M, 520,
        f'<div style="font-family:var(--d);font-weight:900;font-size:330px;line-height:.78;'
        f'letter-spacing:-.05em;text-transform:lowercase;color:{CREAM}">show<br>up.</div>', z=20))
    # annotation column — the detail driver
    notes = [("WHO", "anyone 14+, no cv, no interview"),
             ("WHEN", "one saturday a month, 7am to noon"),
             ("WHERE", "kolkata + sunderbans, bus provided"),
             ("COST", "nothing, ever, in either direction"),
             ("AFTER", "stay, switch lanes, or don't come back")]
    y = 800
    for k, v in notes:
        els.append(at(M, y, W - 2*M, 80,
            f'<div style="display:flex;gap:24px;align-items:baseline;'
            f'border-top:2px solid rgba(255,255,255,.28);padding-top:12px">'
            f'<div style="min-width:120px">{mono(k, 16, A[2])}</div>'
            f'{micro(v, 22, "#EDE9DE")}</div>', z=22))
        y += 88
    for x, yy, s, acc, sh, r in [(760, 200, 165, A[3], S.starburst(11), 12),
                                 (890, 380, 110, A[0], S.blob(6, 8), 0),
                                 (700, 1150, 130, A[4], S.gear(9), -8),
                                 (890, 1100, 105, A[5], S.scallop(12), 9)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · THE WHOLE ASK", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


# ── 30. STACKED ZONES + SUB-COPY ──────────────────────────────────────────────
async def stacked_zones():
    els = []
    els.append(at(M, 160, W - 2*M, 150,
        f'<div style="width:100%;height:100%;background:{A[6]};border:5px solid var(--ink);'
        f'border-radius:22px;box-shadow:9px 9px 0 var(--ink);display:flex;flex-direction:column;'
        f'justify-content:center;padding-left:32px;box-sizing:border-box">'
        f'<div style="font-family:var(--d);font-weight:900;font-size:52px;text-transform:uppercase;'
        f'color:#FFF;line-height:1">what a drive looks like</div>'
        f'{mono("A SATURDAY, START TO FINISH", 14, "#FFF")}</div>', z=12))
    rows = [("06:40", "meet at esplanade", "look for the teal flags, we wait for stragglers", A[4]),
            ("07:15", "bus + briefing", "you get paired with someone who has done this before", A[2]),
            ("08:30", "the actual work", "sorting, carrying, teaching, feeding, planting", A[0]),
            ("11:00", "tea and a sit down", "this is where most people decide to come back", A[1]),
            ("12:00", "log the day", "two minutes on a form so the next drive is better", A[5]),
            ("12:30", "bus back", "home by two, nobody guilt-trips you into staying", A[3])]
    y = 350
    for t, title, sub, acc in rows:
        els.append(at(M, y, W - 2*M, 128,
            f'<div style="width:100%;height:100%;display:flex;gap:20px;align-items:center;'
            f'background:{CREAM};border:4px solid var(--ink);border-radius:18px;'
            f'box-shadow:6px 6px 0 rgba(10,10,10,.25);padding:0 24px;box-sizing:border-box">'
            f'<div style="min-width:110px;background:{acc};color:{TON(acc)};border:3px solid var(--ink);'
            f'border-radius:999px;padding:7px 0;text-align:center;font-family:var(--m);'
            f'font-weight:700;font-size:17px">{t}</div>'
            f'<div><div style="font-family:var(--d);font-weight:900;font-size:30px;'
            f'text-transform:uppercase;line-height:1.05">{title}</div>'
            f'{micro(sub, 18)}</div></div>', z=14))
        y += 138
    els.append(at(M, 1180, W - 2*M, 76,
        f'<div style="width:100%;height:100%;background:var(--ink);border-radius:999px;'
        f'display:flex;align-items:center;justify-content:center">'
        + mono("DM @NGO.AQUATERRA AND WE WILL SEND THE PIN", 16, "#FFF") + "</div>", z=16))
    els.append(at(905, 300, 118, 118, S.sticker(S.starburst(10), A[2], size=118), z=30, rot=13))
    inner = (f'<div style="position:absolute;inset:0;background:#EFE7D6"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · A DAY OUT"))
    return B.page(W, H, "#EFE7D6", inner, grain=True)


JOBS = [("26_diagonal_cascade", diagonal_cascade), ("27_flat_lay", flat_lay),
        ("28_radial_orbit", radial_orbit), ("29_giant_type", giant_type),
        ("30_stacked_zones", stacked_zones)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
