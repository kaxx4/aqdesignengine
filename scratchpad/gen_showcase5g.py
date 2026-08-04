"""SHOWCASE 5g — five more. AREA is now the binding constraint (detail is solved), so every
piece here targets area ~0.9-1.1x: content pushed to all four margins, no dead bands, and no
oversized flat masses (which inflate area while crushing detail — the 5e tension rule).

 31 51010a5e1a  serif + annotated words -> speech-bubble tags anchored to specific glyphs
 32 fc9ff90207  grid-break contact sheet -> rigid thumbnail grid + ONE rotated/scaled hero card
 33 87525f70ad  balanced pile            -> pile spread across ALL quadrants, not dumped in one
 34 8988345ad4  word-scatter field       -> words at varied size/rotation filling the whole field
 35 684fb8df55  single-slide stack       -> banded layout with dense per-band sub-copy
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
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:38px;z-index:70;{sh}">'

def footer(light=False):
    c = "#FFFFFF" if light else "var(--ink)"
    return (f'<span style="position:absolute;bottom:50px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{c};z-index:70">@ngo.aquaterra</span>')

def eyebrow(t, c="var(--ink)"):
    return (f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{c};z-index:70">{t}</span>')

def mono(t, s=13, c="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')

def micro(t, s=17, c="#3A3A3A"):
    return f'<span style="font-family:var(--e);font-weight:600;font-size:{s}px;color:{c}">{t}</span>'

def bubble(txt, acc, x, y, w=230, rot=-3, tail="left"):
    """Speech-bubble tag with a tail — anchored beside a specific word (51010a5e steal)."""
    t = (f'<div style="position:absolute;{"left:26px" if tail=="left" else "right:26px"};bottom:-14px;'
         f'width:0;height:0;border-left:14px solid transparent;border-right:14px solid transparent;'
         f'border-top:18px solid var(--ink)"></div>')
    return at(x, y, w, 74,
        f'<div style="position:relative;width:100%;height:100%;background:{acc};border:4px solid var(--ink);'
        f'border-radius:20px;box-shadow:5px 5px 0 var(--ink);display:flex;align-items:center;'
        f'justify-content:center;text-align:center">{mono(txt,14,TON(acc),".06em")}{t}</div>', z=40, rot=rot)


# ── 31. SERIF + ANNOTATED WORDS ───────────────────────────────────────────────
async def serif_annotated():
    graph = ('<svg style="position:absolute;inset:0;z-index:1" width="1080" height="1350" '
             'xmlns="http://www.w3.org/2000/svg">'
             + "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="1350" stroke="#0A0A0A" stroke-width="1" opacity=".08"/>'
                       for x in range(0, 1081, 40))
             + "".join(f'<line x1="0" y1="{y}" x2="1080" y2="{y}" stroke="#0A0A0A" stroke-width="1" opacity=".08"/>'
                       for y in range(0, 1351, 40)) + "</svg>")
    els = []
    els.append(at(M, 210, W - 2*M, 560,
        f'<div style="font-family:var(--s);font-style:italic;font-size:92px;line-height:1.06;'
        f'color:var(--ink)">the volunteer network for '
        f'<span style="background:{A[0]};padding:0 12px;box-decoration-break:clone;'
        f'-webkit-box-decoration-break:clone">teenagers</span> who would rather '
        f'<span style="background:{A[2]};padding:0 12px;box-decoration-break:clone;'
        f'-webkit-box-decoration-break:clone">do</span> than post.</div>', z=20))
    els += [bubble("NO FEE, EVER", A[4], 600, 250, 250, -5),
            bubble("14 AND UP", A[1], 230, 740, 210, 4, "right"),
            bubble("KOLKATA + SUNDERBANS", A[5], 520, 760, 330, -3)]
    stats = [("1,200", "volunteers"), ("42", "drives in 2025"), ("5", "programmes"), ("0", "fees")]
    row = "".join(f'<div style="flex:1;border-left:3px solid var(--ink);padding-left:16px">'
                  f'<div style="font-family:var(--d);font-weight:900;font-size:52px;line-height:1">{n}</div>'
                  f'{mono(l, 13, "#4A4A4A", ".06em")}</div>' for n, l in stats)
    els.append(at(M, 920, W - 2*M, 110, f'<div style="display:flex;gap:20px">{row}</div>', z=24))
    els.append(at(M, 1075, W - 2*M, 130,
        f'<div style="line-height:1.5">' + micro("we run food, climate, education, animal and health "
        "drives every month. you pick one, come once, and decide after. nobody chases you.", 21) + "</div>", z=24))
    for x, y, s, acc, sh, r in [(842, 330, 96, A[3], S.starburst(10), 12), (862, 620, 78, A[6], S.blob(5, 8), 0)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#FBF9F2"></div>' + graph
             + "".join(els) + logo() + footer() + eyebrow("AQ · WHO WE ARE"))
    return B.page(W, H, "#FBF9F2", inner, grain=True)


# ── 32. GRID-BREAK CONTACT SHEET ──────────────────────────────────────────────
async def grid_break():
    """fc9ff90207: break the grid exactly ONCE — rotate one card ~8 deg, scale ~1.4x, hard shadow,
    overlap its neighbours. One deliberate violation manufactures the hero a rigid grid cannot."""
    els = []
    labels = ["FOOD", "TREES", "BOOKS", "DOGS", "CLOTHES", "HEALTH", "KITS", "CAMPS",
              "CLEANUP", "TUTORING", "WINTER", "MONSOON", "TOYS", "MEDS", "SHOES"]
    cw, ch, gap = 296, 176, 14
    x0, y0 = M, 300
    for i, lab in enumerate(labels):
        r, c = divmod(i, 3)
        acc = A[i % 7]
        els.append(at(x0 + c * (cw + gap), y0 + r * (ch + gap), cw, ch,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:18px;'
            f'padding:16px;box-sizing:border-box;display:flex;flex-direction:column;'
            f'justify-content:space-between">{mono(f"{i+1:02d}", 12, TON(acc))}'
            f'<div style="font-family:var(--d);font-weight:900;font-size:30px;'
            f'text-transform:uppercase;color:{TON(acc)}">{lab}</div>'
            f'<div style="border-top:1.5px solid {TON(acc)};opacity:.85;padding-top:6px">'
            f'{mono("monthly · 7am", 10, TON(acc), ".06em")}</div></div>', z=10))
    # the ONE grid-breaking hero
    els.append(at(300, 640, 460, 300,
        f'<div style="width:100%;height:100%;background:{CREAM};border:6px solid var(--ink);'
        f'border-radius:20px;box-shadow:16px 16px 0 rgba(0,0,0,.55);padding:24px;box-sizing:border-box;'
        f'display:flex;flex-direction:column;justify-content:center;gap:8px">'
        f'{mono("PICK ANY ONE", 15, A[6])}'
        f'<div style="font-family:var(--d);font-weight:900;font-size:62px;line-height:.92;'
        f'text-transform:uppercase">twelve<br>ways in</div>'
        f'{micro("all of them run every month", 18)}</div>', z=30, rot=-8))
    els.append(at(700, 600, 120, 120, S.sticker(S.starburst(11), A[2], size=120), z=36, rot=14))
    els.append(at(M, 160, W - 2*M, 110,
        f'<div style="display:flex;justify-content:space-between;align-items:baseline">'
        f'<div style="font-family:var(--d);font-weight:900;font-size:66px;text-transform:uppercase">'
        f'the whole board</div>{mono("2026", 20)}</div>', z=24))
    els.append(at(M, 1230, W - 2*M, 60,
        f'<div style="text-align:center">' + micro("dm @ngo.aquaterra with the number you want.", 19) + "</div>", z=24))
    inner = ('<div style="position:absolute;inset:0;background:#F2EEE4"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · INDEX"))
    return B.page(W, H, "#F2EEE4", inner, grain=True)


# ── 33. BALANCED PILE ─────────────────────────────────────────────────────────
async def balanced_pile():
    """87525f70 is the sample behind layout.quadrant_fill_check ('cramming a pile into one corner
    starves other quadrants'). So this pile is deliberately distributed across ALL four quadrants
    with a clear centre focal, rather than dumped."""
    els = []
    spread = [
        (S.scallop(14), A[0],  70, 210, 320, -8, "FOOD"), (S.starburst(11), A[2], 700, 175, 300, 10, "TREES"),
        (S.blob(3, 8), A[4],  80, 880, 305, 0, "BOOKS"), (S.gear(10), A[5], 720, 860, 310, 0, "DOGS"),
        (S.tag(100, 44), A[1],  60, 560, 330, 5, "KITS"), (S.shield(), A[6], 760, 540, 275, -6, "CAMPS"),
        (S.capsule(100, 40), A[3], 390, 155, 300, 4, "WINTER"), (S.arch(), A[2], 400, 940, 270, -4, "MONSOON"),
    ]
    for d, f, x, y, s, r, lab in spread:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, rot=r,
                      inner=S.label(lab, 13, 55, fill=TON(f))), z=20))
    els.append(at(320, 455, 440, 440,
        S.sticker(S.scallop(16), "#0A0A0A", size=440,
                  inner=S.label("EIGHT", 20, 42, fill="#FFF") + S.label("LANES", 20, 64, fill="#FFF")
                       + S.label("ONE ASK", 11, 80, fill=A[2])), z=30))
    els.append(at(M, 150, W - 2*M, 70,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:56px;'
        f'text-transform:uppercase;color:var(--ink)">everything we run</div>', z=34))
    els.append(at(160, 1190, 760, 80,
        f'<div style="text-align:center;line-height:1.45">'
        + micro("every sticker is a real programme with a real date this month. "
                "pick the one that fits your saturday.", 19) + "</div>", z=34))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · ALL LANES"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 34. WORD-SCATTER FIELD ────────────────────────────────────────────────────
async def word_scatter():
    """Words at varied size and rotation filling the WHOLE field — scale alone creates hierarchy,
    no headline/subhead split (the batch-3 size-ramped-sentence steal)."""
    els = []
    words = [("show", 168, 70, 210, -6, A[3]), ("up", 232, 470, 190, 5, "#0A0A0A"),
             ("for", 96, 700, 250, -3, A[5]), ("someone", 150, 90, 400, 4, A[6]),
             ("who", 112, 640, 560, -7, A[0]), ("cannot", 132, 120, 690, 3, A[4]),
             ("yet", 188, 620, 800, -5, A[2]), ("show up", 100, 110, 980, 6, A[1]),
             ("for", 62, 540, 1010, -4, "#0A0A0A"), ("themselves.", 112, 200, 1090, 3, A[5])]
    for w, fs, x, y, rot, col in words:
        els.append(at(x, y, 800, fs + 30,
            f'<div style="font-family:var(--d);font-weight:900;font-size:{fs}px;line-height:1;'
            f'text-transform:lowercase;color:{col};white-space:nowrap">{w}</div>', z=20, rot=rot))
    for x, y, s, acc, sh, r in [(860, 250, 130, A[2], S.starburst(10), 12),
                                (60, 540, 105, A[1], S.blob(4, 8), 0),
                                (900, 700, 115, A[3], S.gear(9), -8),
                                (830, 1050, 100, A[4], S.scallop(12), 9),
                                (400, 330, 88, A[0], S.capsule(100, 40), 6)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    els.append(at(M, 1230, W - 2*M, 60,
        f'<div style="display:flex;justify-content:space-between">'
        + mono("VOLUNTEER WITH AQUATERRA", 16) + mono("KOLKATA · 2026", 16, A[6]) + "</div>", z=34))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · THE POINT"))
    return B.page(W, H, CREAM, inner, grain=True)


# ── 35. SINGLE-SLIDE BAND STACK ───────────────────────────────────────────────
async def band_stack():
    els = []
    bands = [(A[6], "01", "WHO IT IS FOR", "anyone 14+ in or near kolkata. no cv, no interview, no fee.", 200),
             (A[2], "02", "WHAT YOU DO", "sort, carry, teach, feed, plant. you get paired on day one.", 400),
             (A[0], "03", "HOW LONG", "one saturday, 7am to noon. bus provided from esplanade.", 600),
             (A[4], "04", "WHAT IT COSTS", "nothing, in either direction. we do not fundraise from you.", 800),
             (A[5], "05", "WHAT COMES NEXT", "stay in the lane, switch, or stop. nobody chases you.", 1000)]
    for acc, n, title, sub, y in bands:
        fg = TON(acc)
        els.append(at(0, y, W, 190,
            f'<div style="width:100%;height:100%;background:{acc};display:flex;align-items:center;'
            f'gap:26px;padding:0 {M}px;box-sizing:border-box">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:74px;color:{fg};opacity:.55;'
            f'min-width:110px">{n}</div>'
            f'<div><div style="font-family:var(--d);font-weight:900;font-size:40px;'
            f'text-transform:uppercase;color:{fg};line-height:1.05">{title}</div>'
            f'<div style="font-family:var(--e);font-weight:600;font-size:20px;color:{fg};'
            f'opacity:.92;margin-top:4px">{sub}</div>'
            f'<div style="margin-top:6px;border-top:1.5px solid {fg};opacity:.7;padding-top:5px">'
            f'{mono("NEXT: SAT 04 · 07:00 · ESPLANADE", 11, fg, ".08em")}</div></div></div>', z=10))
        els.append(at(W - 150, y + 52, 86, 86,
            S.sticker(S.scallop(11) if n in ("01", "03", "05") else S.starburst(9),
                      "#0A0A0A", size=86, inner=S.label(n, 15, 56, fill="#FFF")), z=26, rot=(int(n) * 5) % 16 - 8))
    els.append(at(0, 130, W, 70,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:58px;'
        f'text-transform:uppercase;color:var(--ink)">five questions, answered</div>', z=20))
    els.append(at(0, 1200, W, 70,
        f'<div style="text-align:center">' + mono("DM @NGO.AQUATERRA TO PICK A SATURDAY", 17) + "</div>", z=20))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · FAQ"))
    return B.page(W, H, CREAM, inner, grain=True)


JOBS = [("31_serif_annotated", serif_annotated), ("32_grid_break", grid_break),
        ("33_balanced_pile", balanced_pile), ("34_word_scatter", word_scatter),
        ("35_band_stack", band_stack)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
