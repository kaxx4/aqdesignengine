"""AQ EVENTS TEAM — registration campaign.
3 feed posters (1080x1350) + 3 stories (1080x1920).

Content is briefed from real AQ event photos (star-light installs, balloon drops, card-suit
garlands, DJ booth, pickleball setup, spray-paint tees, name-taped walkie-talkies, Rs20 cash
coupons, AQ wristbands). No imagery is fabricated — this set is illustration-led using the
engine's own vocabulary. Swap in real photos later via engine/vision.plan_spots().

Rules in force (brain/DECISIONS.md): small-text density drives detail; no large flat colour
blocks; area ~0.9-1.1x; uniform shapes.sticker() on every object.
STORY SAFE ZONE: keep key content between y=270 and y=1650 (IG chrome covers the rest).
"""
import asyncio, os, sys, importlib.util, math
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); S = load("shapes")

FW, FH = core.SIZES["feed"]; SW_, SH_ = core.SIZES["story"]; M = 64
A = core.ACCENTS; CREAM = "var(--bg)"; TON = core.text_on

def at(x, y, w, h, i, z=6, rot=0):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'z-index:{z};transform:rotate({rot}deg)">{i}</div>')
def logo(d=False, y=52):
    sh = "filter:drop-shadow(0 2px 6px rgba(0,0,0,.5));" if d else ""
    return f'<img src="{core.LOGO}" style="position:absolute;top:{y}px;left:{M}px;height:40px;z-index:80;{sh}">'
def foot(txt="@ngo.aquaterra", light=False, y=52):
    return (f'<span style="position:absolute;bottom:{y}px;left:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:14px;letter-spacing:.06em;color:{"#FFF" if light else "var(--ink)"};z-index:80">{txt}</span>')
def eyeb(t, c="var(--ink)", y=62):
    return (f'<span style="position:absolute;top:{y}px;right:{M}px;font-family:var(--m);font-weight:700;'
            f'font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:{c};z-index:80">{t}</span>')
def mono(t, s=13, c="var(--ink)", ls=".1em"):
    return (f'<span style="font-family:var(--m);font-weight:700;font-size:{s}px;letter-spacing:{ls};'
            f'text-transform:uppercase;color:{c}">{t}</span>')
def micro(t, s=18, c="#3A3A3A"):
    return f'<span style="font-family:var(--e);font-weight:600;font-size:{s}px;color:{c}">{t}</span>'
def pill(t, acc, fs=15):
    return (f'<span style="display:inline-block;background:{acc};color:{TON(acc)};border:3px solid var(--ink);'
            f'border-radius:999px;padding:8px 18px;font-family:var(--m);font-weight:700;font-size:{fs}px;'
            f'letter-spacing:.07em">{t}</span>')

# the six real crew roles, straight off the event photos
ROLES = [("DECOR + INSTALL", A[0], "star curtains, balloon drops, card-suit garlands"),
         ("PRODUCTION", A[5], "dj booth, sound, lights, stage calls"),
         ("OPS + CREW", A[4], "walkies, entry, coupons, headcounts"),
         ("MERCH + ART", A[2], "spray-paint tees, hand-painted jerseys"),
         ("SPORTS", A[1], "pickleball brackets, court setup, refs"),
         ("HOSPITALITY", A[3], "wristbands, guest desk, green room")]


# ══ POSTER 1 — hero recruitment ══════════════════════════════════════════════
async def p1_hero():
    els = []
    els.append(at(M, 150, FW - 2*M, 60,
        f'<div style="display:flex;justify-content:space-between">' + mono("AQUATERRA", 15)
        + mono("KOLKATA", 15, A[6]) + mono("2026 INTAKE", 15) + "</div>", z=30))
    els.append(at(M, 230, FW - 2*M, 330,
        f'<div style="font-family:var(--d);font-weight:900;font-size:128px;line-height:.86;'
        f'text-transform:uppercase;color:var(--ink)">events<br>team</div>'
        f'<div style="margin-top:10px;font-family:var(--s);font-style:italic;font-size:56px;'
        f'color:{A[3]}">registrations open.</div>', z=30))
    # role chips row — dense small text
    els.append(at(M, 600, FW - 2*M, 120,
        '<div style="display:flex;gap:10px;flex-wrap:wrap">'
        + "".join(pill(r[0], r[1]) for r in ROLES) + "</div>", z=30))
    # the "what you actually get" block, grounded in the photos
    facts = [("01", "a walkie with your name taped on it"),
             ("02", "a 500-person floor that you built that morning"),
             ("03", "spray paint under your fingernails for a week"),
             ("04", "a crew that texts at 2am about balloon counts")]
    y = 770
    for n, t in facts:
        els.append(at(M, y, FW - 2*M, 78,
            f'<div style="display:flex;gap:18px;align-items:baseline;'
            f'border-bottom:2px solid rgba(255,255,255,.28);padding-bottom:11px">'
            + mono(n, 16, A[2]) + micro(t, 22, '#F2EFE6') + "</div>", z=30))
        y += 88
    els.append(at(M, 1140, FW - 2*M, 84,
        f'<div style="width:100%;height:100%;background:var(--ink);border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center;border:4px solid #FFF">' + mono("DM @NGO.AQUATERRA TO REGISTER", 18, "#FFF") + "</div>", z=32))
    for x, yy, s, acc, sh, r in [(840, 200, 150, A[2], S.starburst(11), 12), (930, 380, 105, A[0], S.blob(4, 8), 0),
                                 (470, 596, 78, A[4], S.scallop(12), -9), (930, 1235, 92, A[5], S.gear(9), 6)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    field = (f'<div style="position:absolute;left:0;right:0;top:740px;bottom:0;background:{A[6]};z-index:2"></div>'
             f'<div style="position:absolute;left:0;right:0;top:560px;height:180px;background:{A[2]};z-index:2"></div>')
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>' + field
             + "".join(els) + logo() + foot(light=True) + eyeb("AQ · CREW CALL"))
    return B.page(FW, FH, CREAM, inner, grain=True), FW, FH


# ══ POSTER 2 — the six roles, card grid ══════════════════════════════════════
async def p2_roles():
    els = []
    els.append(at(M, 150, FW - 2*M, 130,
        f'<div style="font-family:var(--d);font-weight:900;font-size:74px;line-height:.92;'
        f'text-transform:uppercase;color:#FFF">six ways to<br>run a night</div>', z=30))
    y = 320
    for i, (name, acc, sub) in enumerate(ROLES):
        els.append(at(M, y, FW - 2*M, 140,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:24px;display:flex;'
            f'align-items:center;gap:22px;padding:0 26px;box-sizing:border-box">'
            f'<div style="min-width:64px;height:64px;background:{TON(acc)};border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center">'
            + mono(f"{i+1:02d}", 17, acc) + "</div>"
            f'<div style="flex:1"><div style="font-family:var(--d);font-weight:900;font-size:38px;'
            f'text-transform:uppercase;color:{TON(acc)};line-height:1">{name}</div>'
            f'<div style="margin-top:3px">' + mono(sub, 12, TON(acc), ".05em") + "</div></div>"
            f'<div style="opacity:.9">' + mono("APPLY", 13, TON(acc)) + "</div></div>", z=14))
        y += 152
    els.append(at(M, 1245, FW - 2*M, 66,
        f'<div style="display:flex;justify-content:space-between;align-items:center">'
        + mono("PICK ONE OR TICK ALL SIX", 15, "#FFF") + mono("FORM IN BIO", 15, A[2]) + "</div>", z=30))
    for x, yy, s, acc, sh, r in [(900, 230, 120, A[2], S.starburst(10), 13), (30, 1150, 92, A[0], S.scallop(11), -8)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + logo(True) + foot(light=True) + eyeb("AQ · ROLES", "#FFF"))
    return B.page(FW, FH, "#0A0A0A", inner, grain=True), FW, FH


# ══ POSTER 3 — event-day timeline (diagonal cascade) ═════════════════════════
async def p3_timeline():
    els = []
    els.append(at(M, 220, FW - 2*M, 880,
        f'<div style="width:100%;height:100%;background:{CREAM};border-radius:34px;'
        f'box-shadow:14px 14px 0 rgba(0,0,0,.5)"></div>', z=8))
    els.append(at(140, 250, 760, 90,
        f'<div style="font-family:var(--d);font-weight:900;font-size:54px;text-transform:uppercase;'
        f'color:var(--ink)">one event day</div>' + mono("WHAT THE CREW ACTUALLY DOES", 14, "#5A5A5A"), z=16))
    rows = [("07:00", "ladders + star curtains", 0, 330, A[2]),
            ("10:00", "court lines, brackets, nets", 1, 370, A[1]),
            ("13:00", "merch table, tees on the rack", 2, 340, A[0]),
            ("16:00", "sound check, dj booth, lights", 3, 400, A[5]),
            ("18:30", "wristbands on, doors open", 4, 350, A[4]),
            ("23:00", "balloon drop, last track", 5, 330, A[3])]
    x0, y0, dx, dy = 150, 400, 42, 96
    for lbl, name, i, bw, acc in rows:
        x, y = x0 + i * dx, y0 + i * dy
        els.append(at(x, y, bw, 64,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:999px;display:flex;'
            f'align-items:center;padding-left:20px;box-sizing:border-box;gap:12px">'
            + mono(lbl, 14, TON(acc))
            + f'<span style="font-family:var(--d);font-weight:900;font-size:21px;'
              f'text-transform:uppercase;color:{TON(acc)}">{name}</span></div>', z=18))
        els.append(at(x + bw + 12, y + 20, 22, 22,
            '<div style="width:22px;height:22px;border-radius:50%;background:#0A0A0A"></div>', z=18))
        els.append(at(x - 92, y + 20, 80, 24,
            f'<div style="text-align:right">' + micro(f"{6+i*2} crew", 14, "#6A6A6A") + "</div>", z=18))
    els.append(at(150, 1000, 800, 70,
        f'<div>' + micro("you will be on one of these lines. we will tell you which by tuesday.", 20) + "</div>", z=18))
    els.append(at(M, 1160, FW - 2*M, 84,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("REGISTER BY 30 AUG", 19, "#0A0A0A") + "</div>", z=30))
    for x, yy, s, acc, sh, r in [(880, 170, 130, A[0], S.starburst(11), 12), (60, 1120, 88, A[6], S.gear(9), 0)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#171717"></div>'
             + "".join(els) + logo(True) + foot(light=True) + eyeb("AQ · EVENT DAY", "#FFF"))
    return B.page(FW, FH, "#171717", inner, grain=True), FW, FH


# ══ STORY 1 — hero ═══════════════════════════════════════════════════════════
async def s1_hero():
    els = []
    els.append(at(M, 300, SW_ - 2*M, 70,
        f'<div style="display:flex;justify-content:space-between">' + mono("AQUATERRA EVENTS", 15)
        + mono("2026", 15, A[6]) + "</div>", z=30))
    els.append(at(M, 400, SW_ - 2*M, 460,
        f'<div style="font-family:var(--d);font-weight:900;font-size:150px;line-height:.84;'
        f'text-transform:uppercase;color:var(--ink)">events<br>team</div>'
        f'<div style="margin-top:16px;font-family:var(--s);font-style:italic;font-size:64px;'
        f'color:{A[3]}">registrations open.</div>', z=30))
    els.append(at(M, 900, SW_ - 2*M, 190,
        '<div style="display:flex;gap:11px;flex-wrap:wrap">'
        + "".join(pill(r[0], r[1], 16) for r in ROLES) + "</div>", z=30))
    facts = [("01", "a walkie with your name on tape"),
             ("02", "a floor you built that morning"),
             ("03", "spray paint under your nails"),
             ("04", "a crew that texts at 2am")]
    y = 1215
    for n, t in facts:
        els.append(at(M, y, SW_ - 2*M, 84,
            f'<div style="display:flex;gap:20px;align-items:baseline;'
            f'border-bottom:2px solid rgba(255,255,255,.28);padding-bottom:12px">'
            + mono(n, 17, A[2]) + micro(t, 25, '#F2EFE6') + "</div>", z=30))
        y += 94
    els.append(at(M, 1560, SW_ - 2*M, 92,
        f'<div style="width:100%;height:100%;background:var(--ink);border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center;border:4px solid #FFF">' + mono("DM TO REGISTER", 20, "#FFF") + "</div>", z=32))
    for x, yy, s, acc, sh, r in [(830, 350, 160, A[2], S.starburst(11), 12), (640, 790, 118, A[0], S.blob(4, 8), 0),
                                 (890, 1035, 116, A[4], S.scallop(12), -9), (700, 1055, 96, A[5], S.gear(9), 6)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    field = (f'<div style="position:absolute;left:0;right:0;top:1160px;bottom:0;background:{A[6]};z-index:2"></div>'
             f'<div style="position:absolute;left:0;right:0;top:880px;height:290px;background:{A[2]};z-index:2"></div>'
             f'<div style="position:absolute;right:-120px;top:250px;width:420px;height:420px;'
             f'border-radius:50%;background:{A[0]};opacity:.30;z-index:2"></div>')
    inner = (f'<div style="position:absolute;inset:0;background:{CREAM}"></div>' + field
             + "".join(els) + logo(y=180) + foot(light=True, y=140) + eyeb("AQ · CREW CALL", y=190))
    return B.page(SW_, SH_, CREAM, inner, grain=True), SW_, SH_


# ══ STORY 2 — the roles ══════════════════════════════════════════════════════
async def s2_roles():
    els = []
    els.append(at(M, 300, SW_ - 2*M, 170,
        f'<div style="font-family:var(--d);font-weight:900;font-size:86px;line-height:.9;'
        f'text-transform:uppercase;color:#FFF">six ways to<br>run a night</div>', z=30))
    y = 520
    for i, (name, acc, sub) in enumerate(ROLES):
        els.append(at(M, y, SW_ - 2*M, 160,
            f'<div style="width:100%;height:100%;background:{acc};border-radius:26px;display:flex;'
            f'align-items:center;gap:22px;padding:0 26px;box-sizing:border-box">'
            f'<div style="min-width:70px;height:70px;background:{TON(acc)};border-radius:50%;'
            f'display:flex;align-items:center;justify-content:center">'
            + mono(f"{i+1:02d}", 19, acc) + "</div>"
            f'<div style="flex:1"><div style="font-family:var(--d);font-weight:900;font-size:42px;'
            f'text-transform:uppercase;color:{TON(acc)};line-height:1">{name}</div>'
            f'<div style="margin-top:4px">' + mono(sub, 13, TON(acc), ".05em") + "</div></div></div>", z=14))
        y += 172
    els.append(at(M, 1560, SW_ - 2*M, 92,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("TICK ONE. OR ALL SIX.", 19, "#0A0A0A") + "</div>", z=30))
    for x, yy, s, acc, sh, r in [(900, 330, 130, A[2], S.starburst(10), 13), (50, 1700, 100, A[0], S.scallop(11), -8)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    inner = ('<div style="position:absolute;inset:0;background:#0A0A0A"></div>'
             + "".join(els) + logo(True, y=180) + foot(light=True, y=140) + eyeb("AQ · ROLES", "#FFF", y=190))
    return B.page(SW_, SH_, "#0A0A0A", inner, grain=True), SW_, SH_


# ══ STORY 3 — deadline / proof ═══════════════════════════════════════════════
async def s3_deadline():
    els = []
    els.append(at(M, 300, SW_ - 2*M, 70, mono("APPLICATIONS CLOSE", 17, A[2]), z=30))
    els.append(at(M, 370, SW_ - 2*M, 300,
        f'<div style="font-family:var(--d);font-weight:900;font-size:210px;line-height:.82;'
        f'text-transform:uppercase;color:#FFF">30<br>aug</div>', z=30))
    stats = [("1,200", "volunteers on the roster"), ("6", "crew roles open right now"),
             ("500+", "people on the floor last event"), ("0", "experience required")]
    y = 840
    for n, l in stats:
        els.append(at(M, y, SW_ - 2*M, 130,
            f'<div style="display:flex;align-items:baseline;gap:24px;'
            f'border-top:2px solid rgba(255,255,255,.25);padding-top:16px">'
            f'<div style="min-width:230px;font-family:var(--d);font-weight:900;font-size:76px;'
            f'line-height:1;color:{A[2]}">{n}</div>' + micro(l, 26, "#EDE9DE") + "</div>", z=30))
        y += 148
    els.append(at(M, 1480, SW_ - 2*M, 130,
        f'<div style="line-height:1.45">'
        + micro("no cv, no interview, no fee. you tell us which lane you want and we put you on a crew.", 25, "#EDE9DE")
        + "</div>", z=30))
    els.append(at(M, 1580, SW_ - 2*M, 96,
        f'<div style="width:100%;height:100%;background:{A[2]};border-radius:999px;display:flex;'
        f'align-items:center;justify-content:center">' + mono("DM @NGO.AQUATERRA", 20, "#0A0A0A") + "</div>", z=32))
    for x, yy, s, acc, sh, r in [(820, 330, 170, A[0], S.starburst(11), 12), (900, 1315, 118, A[4], S.blob(5, 8), 0),
                                 (905, 1690, 105, A[5], S.gear(9), 6)]:
        els.append(at(x, yy, s, s, S.sticker(sh, acc, size=s), z=40, rot=r))
    field = (f'<div style="position:absolute;left:0;right:0;top:780px;height:670px;background:#0A0A0A;z-index:2"></div>'
             f'<div style="position:absolute;right:-140px;top:180px;width:460px;height:460px;'
             f'border-radius:50%;background:{A[2]};opacity:.85;z-index:2"></div>'
             f'<div style="position:absolute;left:-100px;bottom:120px;width:340px;height:340px;'
             f'border-radius:50%;background:{A[0]};opacity:.75;z-index:2"></div>')
    inner = (f'<div style="position:absolute;inset:0;background:{A[5]}"></div>' + field
             + "".join(els) + logo(True, y=180) + foot(light=True, y=140) + eyeb("AQ · DEADLINE", "#FFF", y=190))
    return B.page(SW_, SH_, A[5], inner, grain=True), SW_, SH_


JOBS = [("poster_1_hero", p1_hero), ("poster_2_roles", p2_roles), ("poster_3_timeline", p3_timeline),
        ("story_1_hero", s1_hero), ("story_2_roles", s2_roles), ("story_3_deadline", s3_deadline)]

async def main():
    out = "out/events_team"; os.makedirs(out, exist_ok=True)
    for name, fn in JOBS:
        html, w, h = await fn()
        await B.render(html, f"{out}/{name}.png", w, h)
    print("done ->", out)

asyncio.run(main())
