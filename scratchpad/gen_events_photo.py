"""AQ EVENTS TEAM — PHOTO-LED set, using the real event photos.
2 feed posters (1080x1350) + 2 stories (1080x1920).

Photos: scratchpad/events_photos/{balloons,wristband,kithang}.jpg — real AQ event shots.
Placement of every doodle is decided by engine/vision.plan_spots(), NOT by hand: it measures
each photo, keeps to background regions that run off-frame, applies a vertically-aware clearance
floor and a pixel-level skin veto, so nothing lands on a face. This is the first real use of the
vision module in production output.

Text NEVER sits directly on the photo — always on a scrim band or a card (the abd472f264 rule).
"""
import asyncio, base64, os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes"); V = load("vision")

FW, FH = core.SIZES["feed"]; SW_, SH_ = core.SIZES["story"]; M = 64
A = core.ACCENTS; CREAM = "var(--bg)"; TON = core.text_on
PH = "scratchpad/events_photos"

def b64(f):
    with open(os.path.join(PH, f), "rb") as fh:
        return "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()

def at(x, y, w, h, i, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{i}</div>')
def photo(f, w, h):
    return (f'<img src="{b64(f)}" style="position:absolute;inset:0;width:{w}px;height:{h}px;'
            f'object-fit:cover;z-index:1">')
def scrim_b(h, w, tint=None):
    lay = 'linear-gradient(to top,rgba(0,0,0,.88),rgba(0,0,0,.45) 55%,rgba(0,0,0,0))'
    if tint: lay = f'linear-gradient(to top,{tint}55,transparent 70%), ' + lay
    return f'<div style="position:absolute;bottom:0;left:0;right:0;height:{h}px;background:{lay};z-index:8"></div>'
def scrim_t(h):
    return (f'<div style="position:absolute;top:0;left:0;right:0;height:{h}px;'
            f'background:linear-gradient(to bottom,rgba(0,0,0,.66),rgba(0,0,0,0));z-index:8"></div>')
def logo(y=52):
    return (f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{M}px;height:44px;'
            f'z-index:80;filter:drop-shadow(0 2px 8px rgba(0,0,0,.75))">')
def foot(y=52):
    return (f'<span style="position:absolute;bottom:{y}px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:#FFF;z-index:80;'
            f'text-shadow:0 2px 6px rgba(0,0,0,.7)">@ngo.aquaterra</span>')
def eyeb(t, y=62, c="#FFF"):
    return (f'<span style="position:absolute;top:{y}px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{c};z-index:80;'
            f'text-shadow:0 2px 6px rgba(0,0,0,.7)">{t}</span>')
def mono(t, s=13, c="#FFF", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')
def pill(t, acc, fs=15):
    return (f'<span style="display:inline-block;background:{acc};color:{TON(acc)};border:3px solid var(--ink);'
            f'border-radius:999px;padding:8px 18px;font-family:var(--m);font-weight:700;font-size:{fs}px;'
            f'letter-spacing:.07em">{t}</span>')

ROLES = [("DECOR + INSTALL", A[0]), ("PRODUCTION", A[5]), ("OPS + CREW", A[4]),
         ("MERCH + ART", A[2]), ("SPORTS", A[1]), ("HOSPITALITY", A[3])]

SHAPES = [S.starburst(11), S.blob(4, 8), S.scallop(12), S.gear(9), S.capsule(100, 40)]

def auto_stickers(fname, w, h, exclude, n=4, seed=0, z=30):
    """Placement by RULE — vision measures the photo and returns face-safe, edge-safe spots."""
    spots = V.plan_spots(os.path.join(PH, fname), w, h, n=n, exclude=exclude, seed=seed,
                         min_size=54, max_size=132)
    out = ""
    for i, sp in enumerate(spots):
        acc = A[(seed * 2 + i * 3) % 7]
        out += at(sp["x"], sp["y"], sp["size"], sp["size"],
                  S.sticker(SHAPES[(seed + i) % len(SHAPES)], acc, size=sp["size"]),
                  z=z, rot=((i * 37) % 30) - 15)
    return out, spots


# ══ POSTER A — balloons hero ═════════════════════════════════════════════════
async def pa():
    ex = [(0, 0, FW, 190), (0, 640, FW, FH - 640)]           # logo strip + the text block below
    st, spots = auto_stickers("balloons.jpg", FW, FH, ex, n=4, seed=1)
    els = []
    els.append(at(M, 700, FW - 2*M, 300,
        f'<div style="font-family:var(--d);font-weight:900;font-size:120px;line-height:.86;'
        f'text-transform:uppercase;color:#FFF">events<br>team</div>'
        f'<div style="margin-top:8px;font-family:var(--s);font-style:italic;font-size:54px;'
        f'color:{A[2]}">registrations open.</div>', z=30))
    els.append(at(M, 1030, FW - 2*M, 120,
        '<div style="display:flex;gap:9px;flex-wrap:wrap">'
        + "".join(pill(r[0], r[1], 14) for r in ROLES) + "</div>", z=30))
    els.append(at(M, 1180, FW - 2*M, 80,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("DM @NGO.AQUATERRA TO REGISTER", 17, "#0A0A0A") + "</div>", z=32))
    inner = (photo("balloons.jpg", FW, FH) + scrim_t(230) + scrim_b(760, FW, A[5]) + st
             + "".join(els) + logo() + foot() + eyeb("AQ · CREW CALL"))
    return B.page(FW, FH, "#0A0A0A", inner, grain=False), FW, FH, spots


# ══ POSTER B — kit hang / sports ═════════════════════════════════════════════
async def pb():
    ex = [(0, 0, FW, 190), (0, 780, FW, FH - 780)]
    st, spots = auto_stickers("kithang.jpg", FW, FH, ex, n=4, seed=3)
    els = []
    els.append(at(M, 840, FW - 2*M, 210,
        f'<div style="font-family:var(--d);font-weight:900;font-size:82px;line-height:.9;'
        f'text-transform:uppercase;color:#FFF">the setup is<br>the job</div>', z=30))
    facts = [("07:00", "ladders, nets, court lines"), ("10:00", "kit racks and brackets up"),
             ("18:30", "wristbands on, doors open")]
    y = 1070
    for t, d in facts:
        els.append(at(M, y, FW - 2*M, 62,
            f'<div style="display:flex;gap:20px;align-items:baseline;'
            f'border-top:2px solid rgba(255,255,255,.35);padding-top:9px">'
            + mono(t, 15, A[2]) + mono(d, 14, "#EDE9DE", ".04em") + "</div>", z=30))
        y += 72
    els.append(at(M, 1290, FW - 2*M, 0, "", z=30))
    inner = (photo("kithang.jpg", FW, FH) + scrim_t(220) + scrim_b(640, FW, A[6]) + st
             + "".join(els) + logo() + foot() + eyeb("AQ · SPORTS + SETUP"))
    return B.page(FW, FH, "#0A0A0A", inner, grain=False), FW, FH, spots


# ══ STORY A — wristband hero ═════════════════════════════════════════════════
async def sa():
    ex = [(0, 0, SW_, 300), (0, 1050, SW_, SH_ - 1050)]
    st, spots = auto_stickers("wristband.jpg", SW_, SH_, ex, n=4, seed=5)
    els = []
    els.append(at(M, 1120, SW_ - 2*M, 340,
        f'<div style="font-family:var(--d);font-weight:900;font-size:142px;line-height:.85;'
        f'text-transform:uppercase;color:#FFF">events<br>team</div>'
        f'<div style="margin-top:12px;font-family:var(--s);font-style:italic;font-size:60px;'
        f'color:{A[2]}">registrations open.</div>', z=30))
    els.append(at(M, 1480, SW_ - 2*M, 120,
        '<div style="display:flex;gap:9px;flex-wrap:wrap">'
        + "".join(pill(r[0], r[1], 14) for r in ROLES[:4]) + "</div>", z=30))
    els.append(at(M, 1620, SW_ - 2*M, 88,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("DM TO REGISTER", 19, "#0A0A0A") + "</div>", z=32))
    inner = (photo("wristband.jpg", SW_, SH_) + scrim_t(340) + scrim_b(1000, SW_, A[0]) + st
             + "".join(els) + logo(y=180) + foot(y=140) + eyeb("AQ · CREW CALL", y=190))
    return B.page(SW_, SH_, "#0A0A0A", inner, grain=False), SW_, SH_, spots


# ══ STORY B — balloons + deadline ════════════════════════════════════════════
async def sb():
    ex = [(0, 0, SW_, 300), (0, 1000, SW_, SH_ - 1000)]
    st, spots = auto_stickers("balloons.jpg", SW_, SH_, ex, n=4, seed=7)
    els = []
    els.append(at(M, 1060, SW_ - 2*M, 90, mono("APPLICATIONS CLOSE", 18, A[2]), z=30))
    els.append(at(M, 1120, SW_ - 2*M, 330,
        f'<div style="font-family:var(--d);font-weight:900;font-size:190px;line-height:.84;'
        f'text-transform:uppercase;color:#FFF">30 aug</div>', z=30))
    stats = [("6", "crew roles open"), ("500+", "on the floor last event"), ("0", "experience needed")]
    y = 1370
    for n, l in stats:
        els.append(at(M, y, SW_ - 2*M, 76,
            f'<div style="display:flex;gap:22px;align-items:baseline;'
            f'border-top:2px solid rgba(255,255,255,.35);padding-top:11px">'
            f'<div style="min-width:150px;font-family:var(--d);font-weight:900;font-size:46px;'
            f'line-height:1;color:{A[2]}">{n}</div>' + mono(l, 15, "#EDE9DE", ".04em") + "</div>", z=30))
        y += 86
    els.append(at(M, 1640, SW_ - 2*M, 88,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("DM @NGO.AQUATERRA", 19, "#0A0A0A") + "</div>", z=32))
    inner = (photo("balloons.jpg", SW_, SH_) + scrim_t(340) + scrim_b(1050, SW_, A[5]) + st
             + "".join(els) + logo(y=180) + foot(y=140) + eyeb("AQ · DEADLINE", y=190))
    return B.page(SW_, SH_, "#0A0A0A", inner, grain=False), SW_, SH_, spots


JOBS = [("photo_poster_1_balloons", pa), ("photo_poster_2_setup", pb),
        ("photo_story_1_wristband", sa), ("photo_story_2_deadline", sb)]

async def main():
    out = "out/events_team"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        html, w, h, spots = await fn()
        await B.render(html, f"{out}/{name}.png", w, h)
        print(f"  {name}: vision placed {len(spots)} stickers "
              f"{[(s['x'], s['y'], s['size']) for s in spots]}")
    print("done ->", out)

asyncio.run(main())
