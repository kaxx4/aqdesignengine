"""SHOWCASE 5h — the FINAL 9, built from the batch_03/04/06 teardowns.
Rules in force: small-text density (detail), area ~0.9-1.1x, NO large flat colour blocks
(they lose detail and area at once), uniform shapes.sticker() treatment.

 36 6780506849 orbit_of_stickers -> size-ramped spiral sentence + sticker ring, paper field
 37 73c29f4cc5 net_bundle        -> echoed headline + cluster wrapped in a drawn mesh
 38 772b9a5b29 paper-strip lines -> every text line on its own torn strip over a sky field
 39 7d4fa0d720 off-frame script  -> giant script cropped by the bottom edge + pill eyebrows
 40 878f95ff7b rainbow word      -> per-letter colour + jitter, numbered pills, ghost letterforms
 41 abb2ab5d11 word-scatter      -> 3 word anchors, cut-paper shapes filling the gaps
 42 abd472f264 photo + cards     -> REAL AQ photo base, white paper cards, never type on photo
 43 b075bc30db off-frame shapes  -> blob field with key-band edge, shapes cropped at margins
 44 d2add78f90 long ribbon       -> scroll column of REAL content (no fabricated UI)
"""
import asyncio, os, sys, importlib.util, math
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes")

W, H = core.SIZES["feed"]; M = 64
A = core.ACCENTS; CREAM = "var(--bg)"; TON = core.text_on

def at(x, y, w, h, i, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{i}</div>')
def logo(d=False):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));" if d else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:52px;left:{M}px;height:38px;z-index:70;{sh}">'
def footer(l=False):
    return (f'<span style="position:absolute;bottom:50px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.06em;color:{"#FFF" if l else "var(--ink)"};z-index:70">@ngo.aquaterra</span>')
def eyebrow(t, c="var(--ink)"):
    return (f'<span style="position:absolute;top:62px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{c};z-index:70">{t}</span>')
def mono(t, s=13, c="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')
def micro(t, s=17, c="#3A3A3A"):
    return f'<span style="font-family:var(--e);font-weight:600;font-size:{s}px;color:{c}">{t}</span>'
def strip(txt, x, y, w, rot=-2, bg="#FFFFFF", fs=26):
    """paper_strip (772b9a5b steal): text NEVER sits directly on a busy/photo field."""
    return at(x, y, w, 62,
        f'<div style="width:100%;height:100%;background:{bg};box-shadow:5px 6px 0 rgba(0,0,0,.35);'
        f'display:flex;align-items:center;padding:0 20px;box-sizing:border-box;'
        f'font-family:var(--d);font-weight:900;font-size:{fs}px;text-transform:uppercase;'
        f'color:#0A0A0A">{txt}</div>', z=30, rot=rot)
def rainbow(word, accents, fs=86, jitter=8):
    """rainbow_word (878f95ff steal): per-letter colour + baseline jitter + rotation."""
    out = ""
    for i, ch in enumerate(word):
        out += (f'<span style="display:inline-block;color:{accents[i%len(accents)]};'
                f'transform:translateY({(jitter if i%2 else -jitter)}px) rotate({(i%3-1)*5}deg);'
                f'font-family:var(--d);font-weight:900;font-size:{fs}px">{ch}</span>')
    return out


async def orbit_stickers():
    words = [("what", 44, 250, 300, -18), ("does", 58, 400, 275, -8), ("it", 74, 545, 285, 4),
             ("take", 96, 620, 250, 12), ("to", 120, 300, 380, -6), ("show", 168, 400, 400, 2),
             ("up", 150, 690, 430, 9), ("for", 62, 300, 560, -12), ("someone", 78, 400, 570, 5),
             ("else?", 104, 640, 590, -4)]
    els = [at(x, y, 500, fs + 24,
              f'<div style="font-family:{"var(--s)" if w in ("show","up") else "var(--d)"};'
              f'{"font-style:italic;" if w in ("show","up") else ""}font-weight:900;font-size:{fs}px;'
              f'line-height:1;color:#2B2B2B;white-space:nowrap">{w}</div>', z=20, rot=r)
           for w, fs, x, y, r in words]
    for i in range(10):
        ang = -math.pi / 2 + i * 2 * math.pi / 10
        sh = [S.starburst(10), S.blob(i + 1, 8), S.scallop(12), S.gear(9), S.capsule(100, 40)][i % 5]
        s = 120 if i % 2 else 96
        x = int(540 + 410 * math.cos(ang) - s / 2); y = int(455 + 330 * math.sin(ang) - s / 2)
        els.append(at(x, y, s, s, S.sticker(sh, A[i % 7], size=s), z=26, rot=(i * 31) % 30 - 15))
    els.append(at(M, 900, W - 2*M, 120,
        f'<div style="text-align:center;line-height:1.5">'
        + micro("aquaterra runs food, climate, education, animal and health drives across kolkata "
                "every single month. no fee, no cv, no minimum.", 21) + "</div>", z=30))
    els.append(at(M, 1060, W - 2*M, 70,
        f'<div style="text-align:center;font-family:var(--d);font-weight:900;font-size:56px;'
        f'text-transform:uppercase;letter-spacing:.06em">aquaterra</div>', z=30))
    inner = ('<div style="position:absolute;inset:0;background:#F7F3E9"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · THE QUESTION"))
    return B.page(W, H, "#F7F3E9", inner, grain=True)


async def net_bundle():
    els = []
    for dx, dy, col in [(8, 55, A[2]), (0, 0, A[2])]:
        els.append(at(90 + dx, 190 + dy, 900, 130,
            f'<div style="font-family:var(--d);font-weight:900;font-size:104px;line-height:1;'
            f'text-transform:uppercase;color:{col}">saturday 04</div>', z=14 if dx else 18))
    cluster = [(S.blob(2, 8), "#B9B9B9", 250, 430, 380, 0), (S.gear(10), "#9A9A9A", 540, 520, 320, 0),
               (S.capsule(100, 40), "#CFCFCF", 280, 700, 350, -8), (S.shield(), "#AEAEAE", 600, 740, 280, 6),
               (S.starburst(11), "#C4C4C4", 130, 640, 240, 10)]
    for d, f, x, y, s, r in cluster:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=False, rot=r), z=20))
    net = '<svg style="position:absolute;inset:0;z-index:26" width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">'
    for i in range(-6, 14):
        net += (f'<line x1="{240+i*52}" y1="430" x2="{140+i*52}" y2="1010" stroke="{A[0]}" stroke-width="4" opacity=".9"/>'
                f'<line x1="240" y1="{430+i*44}" x2="880" y2="{470+i*44}" stroke="{A[0]}" stroke-width="4" opacity=".9"/>')
    net += "</svg>"
    els.append(at(200, 1030, 400, 78,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">{mono("THE LAST DRIVE OF 2026", 17, "#0A0A0A")}</div>', z=34, rot=-3))
    els.append(at(620, 1055, 300, 70,
        f'<div style="width:100%;height:100%;background:{A[4]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">{mono("07:00 · ESPLANADE", 15, "#FFF")}</div>', z=34, rot=4))
    els.append(at(M, 1180, W - 2*M, 70,
        f'<div style="display:flex;justify-content:space-between">' + mono("DIAMOND HARBOUR", 14, "#FFF")
        + mono("BUS PROVIDED", 14, "#FFF") + mono("DM TO RESERVE", 14, A[2]) + "</div>", z=34))
    inner = (f'<div style="position:absolute;inset:0;background:{A[4]}"></div>'
             + "".join(els) + net + logo(True) + footer(True) + eyebrow("AQ · YEAR END", "#FFF"))
    return B.page(W, H, A[4], inner, grain=True)


async def paper_strips():
    sky = (f'<div style="position:absolute;inset:0;background:{A[4]}"></div>'
           + "".join(f'<div style="position:absolute;left:{(i*173)%900}px;top:{(i*211)%1100+80}px;'
                     f'width:{90+(i%4)*40}px;height:{40+(i%3)*18}px;border-radius:50%;'
                     f'background:#FFFFFF;opacity:.30;z-index:2"></div>' for i in range(16)))
    scribble = '<svg style="position:absolute;inset:0;z-index:3" width="1080" height="1350" xmlns="http://www.w3.org/2000/svg">'
    for i in range(14):
        x, y = (i * 137) % 950, (i * 241) % 1150 + 60
        scribble += (f'<path d="M{x} {y} q30 -26 60 0 t60 0" fill="none" stroke="#FFFFFF" '
                     f'stroke-width="4" opacity=".34" stroke-linecap="round"/>')
    scribble += "</svg>"
    els = [strip("HELLO, VOLUNTEER", 150, 300, 620, -3, "#FFFFFF", 44),
           strip("saturday 04 · 07:00", 210, 400, 460, 2, A[2], 26),
           strip("diamond harbour beach", 170, 900, 540, -2, "#FFFFFF", 26),
           strip("bus leaves esplanade 06:40", 220, 980, 560, 3, "#FFFFFF", 24),
           strip("dm @ngo.aquaterra to come", 190, 1060, 580, -2, A[0], 24)]
    props = [(S.starburst(11), A[3], 690, 470, 280, 12), (S.gear(10), A[2], 130, 520, 250, 0),
             (S.blob(4, 8), A[1], 380, 580, 300, 0), (S.scallop(13), A[0], 640, 690, 270, -9),
             (S.tag(100, 44), A[5], 150, 730, 300, 5), (S.shield(), A[6], 780, 240, 210, 8),
             (S.capsule(100,40), A[2], 120, 250, 260, -6)]
    for d, f, x, y, s, r in props:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, rot=r), z=24))
    inner = sky + scribble + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · COME ALONG", "#FFF")
    return B.page(W, H, A[4], inner, grain=True)


async def off_frame_script():
    els = []
    cols = [("LANES", ["welfare", "climate", "education"]), ("WHEN", ["one saturday", "7am to noon", "monthly"]),
            ("COST", ["no fee", "bus provided", "no cv needed"])]
    for i, (lab, items) in enumerate(cols):
        x = M + i * 320
        els.append(at(x, 220, 280, 46,
            f'<div style="display:inline-block;background:{CREAM};border-radius:999px;padding:8px 20px">'
            + mono(lab, 13) + "</div>", z=24))
        for j, it in enumerate(items):
            els.append(at(x, 290 + j * 52, 300, 46,
                f'<div style="font-family:var(--d);font-weight:900;font-size:30px;'
                f'text-transform:lowercase;color:#FFFFFF">{it}</div>', z=24))
    els.append(at(-40, 560, 1200, 520,
        f'<div style="font-family:var(--s);font-style:italic;font-size:400px;line-height:.9;'
        f'color:{CREAM};white-space:nowrap">aquaterra</div>', z=14))
    for x, y, s, acc, sh, r in [(200, 690, 190, A[3], S.starburst(10), 12), (540, 660, 165, A[2], S.blob(4, 8), 0),
                                (820, 730, 180, A[0], S.scallop(12), -8), (370, 880, 155, A[1], S.gear(9), 6),
                                (60, 300, 150, A[2], S.tag(100,44), -5), (900, 300, 140, A[6], S.shield(), 9)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    els.append(at(M, 1170, W - 2*M, 80,
        f'<div style="display:flex;justify-content:space-between;border-top:3px solid {CREAM};padding-top:14px">'
        + mono("KOLKATA + SUNDERBANS", 14, CREAM) + mono("SINCE 2021", 14, CREAM)
        + mono("1,200 VOLUNTEERS", 14, A[2]) + "</div>", z=30))
    inner = (f'<div style="position:absolute;inset:0;background:{A[5]}"></div>'
             + "".join(els) + logo(True) + footer(True) + eyebrow("AQ · CONTACT", CREAM))
    return B.page(W, H, A[5], inner, grain=True)


async def rainbow_word():
    ghost = (f'<div style="position:absolute;top:300px;left:-260px;font-family:var(--d);font-weight:900;'
             f'font-size:520px;line-height:.8;color:transparent;-webkit-text-stroke:5px rgba(10,10,10,.10);'
             f'white-space:nowrap;z-index:1">AQAQ</div>')
    els = [at(M, 180, W - 2*M, 160, f'<div style="line-height:1">{rainbow("PROGRAMMES", A, 78)}</div>', z=20)]
    rows = [("01", "food + welfare", "hot meals, kits, winter clothing"),
            ("02", "climate", "tree drives, beach and canal cleanups"),
            ("03", "education", "sunderbans schools, tutoring, books"),
            ("04", "animals", "street feeding, vet camps, shelters"),
            ("05", "health", "checkup camps, medicine, awareness"),
            ("06", "you", "whichever of the five actually fits")]
    y = 360
    for n, t, s in rows:
        acc = A[int(n) % 7]
        els.append(at(M, y, W - 2*M, 138,
            f'<div style="width:100%;height:100%;display:flex;align-items:center;gap:20px;'
            f'border-bottom:2px solid rgba(10,10,10,.16)">'
            f'<div style="min-width:78px;height:56px;background:{acc};border:3px solid var(--ink);'
            f'border-radius:999px;display:flex;align-items:center;justify-content:center">'
            + mono(n, 17, TON(acc)) + "</div>"
            f'<div><div style="font-family:var(--d);font-weight:900;font-size:34px;'
            f'text-transform:uppercase;line-height:1.05">{t}</div>{micro(s, 18)}</div></div>', z=22))
        y += 146
    els.append(at(M, 1150, W - 2*M, 76,
        f'<div style="width:100%;height:100%;background:var(--ink);border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("DM TO PICK ONE", 17, "#FFF") + "</div>", z=24))
    for x, y2, s, acc, sh, r in [(900, 250, 110, A[2], S.starburst(10), 12), (60, 1230, 84, A[0], S.scallop(11), -9)]:
        els.append(at(x, y2, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>' + ghost
             + "".join(els) + logo() + footer() + eyebrow("AQ · ALL FIVE"))
    return B.page(W, H, CREAM, inner, grain=True)


async def word_scatter_field():
    els = []
    anchors = [("show", 90, 230, 150, -6), ("up", 700, 480, 170, 8), ("kolkata", 120, 880, 120, -4)]
    for w, x, y, fs, r in anchors:
        out = ""
        for i, ch in enumerate(w):
            out += (f'<span style="display:inline-block;font-family:var(--d);font-weight:900;'
                    f'font-size:{fs}px;transform:translateY({int(14*math.sin(i))}px) rotate({(i%3-1)*9}deg);'
                    f'color:#141414">{ch}</span>')
        els.append(at(x, y, 760, fs + 50, f'<div style="line-height:1;white-space:nowrap">{out}</div>', z=24, rot=r))
    shapes = [(S.blob(3, 9), A[3], 600, 170, 340, 0), (S.starburst(12), A[4], 160, 450, 280, 12),
              (S.gear(10), A[1], 440, 600, 260, 0), (S.scallop(13), A[5], 780, 730, 270, -8),
              (S.capsule(100, 40), A[2], 100, 620, 300, 6), (S.tag(100, 44), A[0], 590, 940, 320, -5),
              (S.shield(), A[6], 860, 280, 220, 9)]
    for d, f, x, y, s, r in shapes:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, rot=r), z=18))
    els.append(at(M, 1130, W - 2*M, 130,
        f'<div style="display:flex;justify-content:space-between;align-items:flex-end">'
        f'<div>{mono("VOLUNTEER DRIVES", 15)}<br>{micro("every saturday, five lanes, no fee", 19)}</div>'
        f'<div style="text-align:right">{mono("2026", 15, A[6])}<br>{micro("kolkata + sunderbans", 19)}</div></div>', z=30))
    inner = (f'<div style="position:absolute;inset:0;background:#F6F2E7"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · FESTIVAL OF WORK"))
    return B.page(W, H, "#F6F2E7", inner, grain=True)


async def photo_cards():
    """abd472f264: text NEVER sits directly on the photo — every block is on a white card."""
    img = core.PHOTOS.get("edu", "")
    els = [f'<img src="{img}" style="position:absolute;inset:0;width:{W}px;height:{H}px;'
           f'object-fit:cover;filter:saturate(.55) brightness(.82);z-index:1">',
           f'<div style="position:absolute;inset:0;background:rgba(10,10,10,.28);z-index:2"></div>']
    els.append(at(120, 180, 840, 190,
        f'<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;'
        f'font-family:var(--d);font-weight:900;font-size:104px;text-transform:uppercase;color:#FFF;'
        f'-webkit-text-stroke:11px #0A0A0A;paint-order:stroke fill">field notes</div>', z=20, rot=-2))
    cards = [("06:40", "everyone is late. we wait anyway.", 90, 430, 470, -4),
             ("08:15", "the kits get sorted twice. always.", 480, 560, 500, 3),
             ("10:30", "someone's mother sends tea.", 120, 700, 480, -3),
             ("12:00", "nobody wants to leave yet.", 460, 850, 510, 4)]
    for t, txt, x, y, w, r in cards:
        els.append(at(x, y, w, 112,
            f'<div style="width:100%;height:100%;background:#FAF8F2;box-shadow:8px 9px 0 rgba(0,0,0,.45);'
            f'padding:16px 22px;box-sizing:border-box">{mono(t, 14, A[3])}'
            f'<div style="font-family:var(--d);font-weight:900;font-size:26px;text-transform:uppercase;'
            f'line-height:1.1;margin-top:4px">{txt}</div>'
            f'<div style="border-top:1.5px solid rgba(10,10,10,.25);margin-top:7px;padding-top:5px">'
            f'{mono("SUNDERBANS · DEC 2025", 10, "#6A6A6A", ".06em")}</div></div>', z=24, rot=r))
    for x, y, s, acc, sh, r in [(830, 420, 120, A[2], S.starburst(10), 12), (70, 600, 96, A[0], S.blob(5, 8), 0),
                                (860, 900, 105, A[1], S.scallop(12), -8)]:
        els.append(at(x, y, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    els.append(at(120, 1030, 840, 96,
        f'<div style="width:100%;height:100%;background:#FAF8F2;box-shadow:8px 9px 0 rgba(0,0,0,.45);'
        f'display:flex;align-items:center;justify-content:center">'
        + mono("SUNDERBANS SCHOOL DRIVE · DEC 2025 · 34 VOLUNTEERS", 16) + "</div>", z=24, rot=-1))
    inner = "".join(els) + logo(True) + footer(True) + eyebrow("AQ · FIELD NOTES", "#FFF")
    return B.page(W, H, "#0A0A0A", inner, grain=True)


async def off_frame_shapes():
    els = [f'<div style="position:absolute;left:-160px;top:330px;width:1400px;height:700px;'
           f'border-radius:52% 48% 46% 54%/58% 44% 56% 42%;background:{A[1]};z-index:4"></div>']
    keys = "".join(f'<div style="position:absolute;left:{60+i*66}px;bottom:0;width:44px;height:74px;'
                   f'background:#0A0A0A;z-index:6"></div>' for i in range(15))
    els.append(f'<div style="position:absolute;left:0;right:0;top:960px;height:74px;z-index:6">{keys}</div>')
    # shapes cropped by the canvas edges (intentional bleed)
    bleed = [(S.blob(2, 8), A[4], -110, 520, 440, 0), (S.gear(11), A[3], 830, 420, 400, 0),
             (S.capsule(100, 40), A[2], 300, 1080, 520, -8), (S.starburst(12), A[5], -80, 980, 300, 10)]
    for d, f, x, y, s, r in bleed:
        els.append(at(x, y, s, s, S.sticker(d, f, size=s, halo=False, rot=r), z=10))
    els.append(at(M, 380, W - 2*M, 200,
        f'<div style="font-family:var(--d);font-weight:900;font-size:112px;line-height:.9;'
        f'text-transform:uppercase;color:#0A0A0A;text-align:center">all that<br>'
        f'<span style="font-family:var(--s);font-style:italic;text-transform:none">work</span></div>', z=20))
    els.append(at(M, 620, W - 2*M, 70,
        f'<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">'
        + "".join(f'<span style="background:{CREAM};border:3px solid #0A0A0A;border-radius:999px;'
                  f'padding:7px 16px;font-family:var(--m);font-weight:700;font-size:14px">{t}</span>'
                  for t in ["FOOD", "TREES", "BOOKS", "DOGS", "HEALTH"]) + "</div>", z=22))
    els.append(at(200, 720, 680, 120,
        f'<div style="text-align:center;line-height:1.5">'
        + micro("five programmes, one saturday a month, run entirely by teenagers in kolkata.", 21, "#123") + "</div>", z=22))
    els.append(at(M, 860, W - 2*M, 90,
        f'<div style="display:flex;justify-content:space-between">'
        + ''.join(f'<div style="flex:1;border-left:2px solid #0A0A0A;padding-left:12px">'
                  f'<div style="font-family:var(--d);font-weight:900;font-size:34px;line-height:1">{n}</div>'
                  + mono(l, 11, '#2A2A2A', '.05em') + '</div>' for n, l in
                  [('1,200','volunteers'),('42','drives'),('5','lanes'),('0','fees')]) + '</div>', z=22))
    els.append(at(620, 1160, 400, 76,
        f'<div style="width:100%;height:100%;background:#0A0A0A;border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("4/30 · JOIN A LANE", 16, "#FFF") + "</div>", z=26, rot=-3))
    inner = ('<div style="position:absolute;inset:0;background:#FFFFFF"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · SERIES"))
    return B.page(W, H, "#FFFFFF", inner, grain=True)


async def long_ribbon():
    """d2add78f90 adapted: the reference is a UI mockup, which the real-assets rule bars. Same
    long-scroll RIBBON composition, filled with real AQ content instead of fabricated screens."""
    els = []
    els.append(at(180, 140, 720, 1100,
        f'<div style="width:100%;height:100%;background:{CREAM};border:6px solid var(--ink);'
        f'border-radius:26px;box-shadow:16px 16px 0 rgba(0,0,0,.35)"></div>', z=8))
    y = 180
    sections = [(A[6], "AQUATERRA", "a volunteer network run by teenagers", 120),
                (A[2], "FIVE LANES", "welfare · climate · education · animals · health", 150),
                (CREAM, "1,200", "people who showed up at least once", 170),
                (A[0], "42 DRIVES", "logged across kolkata in 2025", 150),
                (A[4], "NO FEE", "in either direction, ever", 140),
                (A[5], "ONE SATURDAY", "7am to noon, bus provided", 150)]
    for acc, t, sub, hh in sections:
        fg = TON(acc) if acc != CREAM else "var(--ink)"
        els.append(at(208, y, 664, hh - 10,
            f'<div style="width:100%;height:100%;background:{acc};display:flex;flex-direction:column;'
            f'justify-content:center;padding:0 28px;box-sizing:border-box;gap:4px">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:{46 if len(t)<9 else 38}px;'
            f'text-transform:uppercase;color:{fg};line-height:1">{t}</div>'
            f'<div style="font-family:var(--e);font-weight:600;font-size:18px;color:{fg};opacity:.9">{sub}</div>'
            f'</div>', z=14))
        y += hh
    for x, yy, s, acc, sh, r in [(120, 260, 130, A[3], S.starburst(11), 12), (860, 380, 115, A[2], S.blob(4, 8), 0),
                                 (110, 700, 120, A[1], S.gear(9), 0), (870, 820, 125, A[0], S.scallop(12), -9),
                                 (140, 1020, 100, A[5], S.tag(100, 44), 6)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=30, rot=r))
    els.append(at(M, 1260, W - 2*M, 50,
        f'<div style="display:flex;justify-content:space-between">' + mono("SCROLL THE WHOLE YEAR", 14)
        + mono("03 / 06", 14, A[6]) + "</div>", z=34))
    inner = ('<div style="position:absolute;inset:0;background:#F6DDE4"></div>'
             + "".join(els) + logo() + footer() + eyebrow("AQ · THE LONG VERSION"))
    return B.page(W, H, "#F6DDE4", inner, grain=True)


JOBS = [("36_orbit_stickers", orbit_stickers), ("37_net_bundle", net_bundle),
        ("38_paper_strips", paper_strips), ("39_off_frame_script", off_frame_script),
        ("40_rainbow_word", rainbow_word), ("41_word_scatter_field", word_scatter_field),
        ("42_photo_cards", photo_cards), ("43_off_frame_shapes", off_frame_shapes),
        ("44_long_ribbon", long_ribbon)]

async def main():
    out = "out/showcase5"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        await B.render(await fn(), f"{out}/{name}.png", W, H)
    print("done ->", out)

asyncio.run(main())
