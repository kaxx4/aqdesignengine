"""SHOWCASE 5 — recreations built on the NEW primitives (engine/shapes.py), in AQ brand language.
Each targets a different reference family so the new vocabulary gets exercised broadly:
  1 c42f94a09f  sticker pile      -> parametric die-cuts + uniform sticker() + text_on_arc
  2 091944e282  events calendar   -> two-tone capsule rows on ink
  3 25d39cb69b  giant type + blobs-> lowercase hero word + 4:1 blob size range
  4 29c6a85891  celebration pile  -> stepped slab type + connector arrow + satellites
  5 bf31ba4914  signpost stack    -> spine with rotated pills + speech-bubble stack
Run: PYTHONIOENCODING=utf-8 python scratchpad/gen_showcase5.py
"""
import asyncio, os, sys, importlib.util, math
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); dd = load("doodles")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS                    # 0 pink 1 mint 2 lemon 3 tomato 4 sky 5 grape 6 teal
INK, CREAM = "var(--ink)", "var(--bg)"

def at(x, y, w, h, inner, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{inner}</div>')

def logo(dark=False):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.45));" if dark else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:40px;z-index:30;{sh}">'

def footer(txt="@ngo.aquaterra", light=False):
    c = "#FFFFFF" if light else "var(--ink)"
    return (f'<span style="position:absolute;bottom:52px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:{c};z-index:30">{txt}</span>')

def eyebrow(txt, color="var(--ink)", y=64, right=True):
    pos = f"right:{M}px" if right else f"left:{M}px"
    return (f'<span style="position:absolute;top:{y}px;{pos};font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:{color};z-index:30">{txt}</span>')


# ── 1. STICKER PILE ────────────────────────────────────────────────────────────
async def sticker_pile():
    """Reference: tight overlapping die-cut pile, generous margins, uniform halo treatment.
    compare.py on the OLD version said: detail 0.58x, spread 1.20x. Fix = real silhouettes + tight pile."""
    els = []
    # tight cluster: centre ~ (540,690), radius <= 300  (old version sprawled)
    # compare.py said: detail 0.71x (BLOCKING) + rows 5-8 under-filled -> pile sat high and loose.
    # Fix per decision table: pull toward centroid (~540,760), allow overlap, and give every
    # sticker interior linework instead of leaving blank silhouettes.
    pile = [
        # (silhouette d, fill, cx, cy, size, rot, inner)
        (S.scallop(13), A[0], 470, 560, 320, -6,
         S.label("YOU", 15, 38) + S.label("SHOWED", 15, 56) + S.label("UP!", 15, 74)),
        (S.scallop(22, 44), A[6], 285, 760, 265, 0, S.text_on_arc("GO TEAM! GO TEAM! ", 31, 10, uid=1)),
        (S.arch(), A[2], 495, 800, 250, 3,
         S.label("UPLIFT", 12, 40) + S.label("EACH", 11, 58) + S.label("OTHER", 11, 72)),
        (S.wave_banner(100, 44, 1.5, 7), A[5], 690, 610, 270, -9,
         S.label("VOLUNTEER", 11, 26, fill="#FFFFFF")),
        (S.gear(9), A[1], 745, 800, 190, 0, S.label("2021", 10, 54, fill="#FFFFFF")),
        (S.starburst(11), A[3], 700, 425, 175, 8, S.label("NEW", 13, 56, fill="#FFFFFF")),
        (S.capsule(100, 40), A[4], 300, 560, 245, -12, S.label("NO FEES", 13, 26)),
        (S.tag(100, 44), A[6], 640, 935, 225, 5, S.label("RECRUIT", 12, 27, fill="#FFFFFF")),
        (S.blob(4, 8), A[2], 385, 930, 175, 0, S.label("+1200", 12, 54)),
        (S.shield(), A[5], 845, 665, 160, -7, S.label("AQ", 14, 55, fill="#FFFFFF")),
    ]
    for d, fill, cx, cy, size, rot, inner in pile:
        svg = S.sticker(d, fill, size=size, halo=True, rot=rot, inner=inner)
        els.append(at(cx - size // 2, cy - size // 2, size, size, svg, z=8))
    # mono eyebrow: copy the reference's layout ROLE, never its literal payload
    head = (f'<div style="position:absolute;top:150px;left:0;right:0;text-align:center;'
            f'font-family:var(--m);font-weight:700;font-size:26px;letter-spacing:.08em;'
            f'color:var(--ink);z-index:20">the show-up pack</div>')
    inner = f'<div style="position:absolute;inset:0;background:{CREAM}"></div>' + head + "".join(els)
    inner += logo() + footer() + eyebrow("AQ · VOLUNTEER")
    return B.page(W, H, CREAM, inner, grain=True)


# ── 2. EVENTS CALENDAR (two-tone capsule rows on ink) ─────────────────────────
async def calendar():
    rows = [("SAT 04", "beach cleanup · diamond harbour", 6),
            ("SUN 12", "sunderbans medical camp", 4),
            ("WED 15", "school kit drive · khidirpur", 0),
            ("SAT 18", "tree plantation · rajarhat", 1),
            ("SUN 26", "food distribution · kolkata", 3),
            ("TUE 29", "volunteer orientation (online)", 5)]
    els = []
    # headline card
    els.append(at(M, 175, W - 2*M, 250,   # compare.py: row 2 under-filled -> taller headline card
        f'<div style="width:100%;height:100%;background:{A[2]};border:5px solid var(--ink);'
        f'border-radius:28px;box-shadow:10px 10px 0 rgba(0,0,0,.35);display:flex;flex-direction:column;'
        f'justify-content:center;padding:0 40px;box-sizing:border-box">'
        f'<div style="font-family:var(--d);font-weight:900;font-size:66px;line-height:.92;'
        f'text-transform:uppercase;color:var(--ink)">what\'s on</div>'
        f'<div style="font-family:var(--e);font-weight:600;font-size:24px;color:var(--ink);opacity:.75">'
        f'august 2026 · kolkata</div></div>', z=10))
    y = 470
    for i, (date, label, ai) in enumerate(rows):
        acc, acc2 = A[ai], A[(ai + 2) % 7]
        fg = core.text_on(acc); fg2 = core.text_on(acc2)
        els.append(at(M, y, W - 2*M, 108,
            f'<div style="width:100%;height:100%;border:5px solid var(--ink);border-radius:999px;'
            f'overflow:hidden;display:flex;box-shadow:7px 7px 0 rgba(0,0,0,.35)">'
            f'<div style="width:250px;background:{acc};display:flex;align-items:center;'
            f'justify-content:center;font-family:var(--m);font-weight:700;font-size:26px;'
            f'letter-spacing:.06em;color:{fg};border-right:5px solid var(--ink)">{date}</div>'
            f'<div style="flex:1;background:{acc2};display:flex;align-items:center;padding-left:34px;'
            f'font-family:var(--e);font-weight:700;font-size:26px;color:{fg2}">{label}</div></div>', z=10))
        y += 126
    # a couple of sparkles poking past the rigid grid (reference move)
    els.append(at(W - 118, 402, 74, 74, S.sticker(S.starburst(9), A[2], size=74, halo=False), z=14, rot=12))
    els.append(at(24, 560, 58, 58, S.sticker(S.starburst(7), A[0], size=58, halo=False), z=14, rot=-14))
    cta = (f'<div style="position:absolute;bottom:120px;left:{M}px;right:{M}px;height:96px;'
           f'background:{A[1]};border:5px solid var(--ink);border-radius:999px;display:flex;'
           f'align-items:center;justify-content:center;font-family:var(--d);font-weight:900;'
           f'font-size:34px;text-transform:uppercase;color:#fff;z-index:12;'
           f'box-shadow:7px 7px 0 rgba(0,0,0,.35)">dm to join any of them</div>')
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + cta + logo(dark=True) + footer(light=True) + eyebrow("AQ · CALENDAR", "#FFFFFF"))
    return B.page(W, H, "#0A0A0A", inner, grain=True)


# ── 3. GIANT TYPE + BLOB FIELD ────────────────────────────────────────────────
async def giant_blobs():
    head = (f'<div style="position:absolute;top:150px;left:{M}px;right:{M}px;display:flex;'
            f'justify-content:space-between;font-family:var(--m);font-weight:700;font-size:17px;'
            f'letter-spacing:.12em;text-transform:uppercase;color:var(--ink);z-index:20">'
            f'<span>aquaterra</span><span>est. 2021</span><span>kolkata</span></div>')
    word = (f'<div style="position:absolute;top:225px;left:{M}px;right:{M}px;font-family:var(--d);'
            f'font-weight:900;font-size:360px;line-height:.82;letter-spacing:-.05em;'
            f'text-transform:lowercase;color:var(--ink);z-index:20">roots</div>')
    # compare.py: area 0.58x (BLOCKING too small) + centroid 0.15 too high + bottom-right dead.
    # Fix: scale every blob up and push the field lower/wider, keeping the 4:1 size range.
    blobs = [(S.blob(2, 7), A[3], 70, 760, 430), (S.blob(5, 9), A[4], 450, 720, 330),
             (S.blob(8, 6), A[1], 700, 850, 250), (S.blob(11, 8), A[5], 830, 640, 140),
             (S.blob(3, 7), A[2], 250, 1010, 190), (S.blob(7, 9), A[6], 620, 1060, 150)]
    els = [at(x, y, s, s, S.sticker(d, f, size=s, halo=False, sw=7), z=10)
           for d, f, x, y, s in blobs]
    payoff = (f'<div style="position:absolute;bottom:150px;left:{M}px;width:600px;font-family:var(--e);'
              f'font-weight:600;font-size:30px;line-height:1.35;color:var(--ink);z-index:20">'
              f'a youth movement from one idea: teenagers can run real change.</div>')
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + head + word + "".join(els) + payoff + logo() + footer())
    return B.page(W, H, CREAM, inner, grain=True)


# ── 4. CELEBRATION PILE (stepped slabs + connector arrow) ─────────────────────
async def celebration():
    els = []
    # stepped black slab type
    # compare.py: area 0.65x (BLOCKING) + rows 9-10 empty. Scale slabs up, add bottom mass.
    for i, (txt, x, y, fs) in enumerate([("WE", 110, 430, 250), ("SHOWED UP", 190, 700, 160)]):
        els.append(at(x, y, 760, fs + 60,
            f'<div style="display:inline-block;background:var(--ink);color:#fff;font-family:var(--d);'
            f'font-weight:900;font-size:{fs}px;line-height:1;padding:18px 30px;'
            f'box-shadow:12px 12px 0 rgba(0,0,0,.30)">{txt}</div>', z=12, rot=-3 + i * 5))
    # speech badge top-left
    els.append(at(110, 250, 300, 300,
        S.sticker(S.scallop(14), A[2], size=300, halo=True,
                  inner=S.label("1,200", 20, 44) + S.label("VOLUNTEERS", 11, 62)), z=14, rot=-9))
    # satellites
    sat = [(S.starburst(10), A[0], 810, 300, 195, 12), (S.gear(8), A[5], 840, 890, 170, 0),
           (S.capsule(100, 40), A[4], 560, 1035, 250, -8), (S.blob(6, 8), A[2], 120, 930, 180, 0),
           (S.tag(100, 44), A[3], 170, 1105, 230, 4), (S.scallop(11), A[2], 830, 1090, 165, -10)]
    for d, f, x, y, s, r in sat:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=True, rot=r), z=12))
    # hand-drawn curled connector arrow: badge -> hero slab
    arrow = ('<svg style="position:absolute;left:0;top:0;width:1080px;height:1350px;z-index:13" '
             'xmlns="http://www.w3.org/2000/svg">'
             # looking gate: at the larger slab scale the old arrow ran UNDER the "WE" block and
             # read as an artifact crossing the W. Moved into open field, badge -> headline.
             '<path d="M660 300 C760 360 720 470 600 505" fill="none" stroke="#0A0A0A" '
             'stroke-width="9" stroke-linecap="round"/>'
             '<path d="M640 470 L596 508 L646 528" fill="none" stroke="#0A0A0A" stroke-width="9" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    inner = (f'<div style="position:absolute;inset:0;background:{A[1]}"></div>'
             + "".join(els) + arrow + logo(dark=True) + footer(light=True) + eyebrow("AQ · 2026", "#FFFFFF"))
    return B.page(W, H, A[1], inner, grain=True)


# ── 5. SIGNPOST STACK ─────────────────────────────────────────────────────────
async def signpost():
    els = []
    spine_x = 250
    els.append(f'<div style="position:absolute;left:{spine_x-11}px;top:330px;width:22px;height:700px;'
               f'background:var(--ink);z-index:8"></div>')
    progs = [("WELFARE", 3, -4, 470), ("EDUCATION", 4, 3, 520), ("CLIMATE", 1, -2, 440),
             ("ANIMALS", 0, 4, 450), ("HEALTH", 6, -3, 430)]
    y = 380
    for name, ai, rot, w in progs:
        acc = A[ai]; fg = core.text_on(acc)
        els.append(at(spine_x, y, w, 96,
            f'<div style="width:100%;height:100%;background:{acc};border:5px solid var(--ink);'
            f'border-radius:999px;box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;'
            f'padding-left:38px;box-sizing:border-box;font-family:var(--d);font-weight:900;'
            f'font-size:38px;letter-spacing:.02em;color:{fg}">{name}</div>', z=10, rot=rot))
        y += 128
    # ground shadow ellipse (turns the flat list into an object)
    els.append(f'<div style="position:absolute;left:{spine_x-130}px;top:1035px;width:280px;height:44px;'
               f'background:rgba(10,10,10,.16);border-radius:50%;z-index:6"></div>')
    # speech-bubble stack, right column
    # compare.py: rows 7-8 right side dead + amber missing. Extend the bubble column downward
    # and introduce the warm/amber accent the reference carries.
    bubbles = [("pick one.", A[2], 690, 400, 300), ("or pick all five.", A[4], 655, 550, 350),
               ("no fees, ever.", A[5], 700, 700, 300), ("run by teenagers.", A[3], 650, 850, 350),
               ("show up. that's it.", A[2], 690, 1000, 310)]
    for txt, acc, x, yy, w in bubbles:
        fg = core.text_on(acc)
        els.append(at(x, yy, w, 120,
            f'<div style="width:100%;height:100%;background:{acc};border:5px solid var(--ink);'
            f'border-radius:30px;box-shadow:7px 7px 0 var(--ink);display:flex;align-items:center;'
            f'justify-content:center;font-family:var(--e);font-weight:700;font-size:28px;'
            f'color:{fg};text-align:center">{txt}</div>', z=10, rot=-2))
    title = (f'<div style="position:absolute;top:170px;left:{M}px;font-family:var(--d);font-weight:900;'
             f'font-size:92px;line-height:.9;text-transform:uppercase;color:var(--ink);z-index:20">'
             f'five ways<br>to show up</div>')
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + title + "".join(els) + logo() + footer() + eyebrow("AQ · PROGRAMMES"))
    return B.page(W, H, CREAM, inner, grain=True)


JOBS = [("01_sticker_pile", sticker_pile), ("02_calendar", calendar),
        ("03_giant_blobs", giant_blobs), ("04_celebration", celebration),
        ("05_signpost", signpost)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        html = await fn()
        await B.render(html, f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
