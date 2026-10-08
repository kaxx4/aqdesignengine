"""TerraThon-look "why we throw events", FRESH layouts: every slide a different composition (no repeated slab + circle).

Kit used (brain/TERRATHON.md): black ground with white flecks, the four blue shuriken (never rotated), die-cut cream halos, the real sticker
PNGs, StretchPro for the stretched title words (EE/AA/OO ligatures), Sigmar One sparingly (tapes, chips), NeutralFace for numbers and body,
orchid #DE68F0 / green #2FD284 / blue #0396FF / cream #F3ECDE. Mechanisms: tickets with a perforated stub, a taped polaroid, a starburst
die-cut photo, a diagonal-cut photo, a sticker sheet of stat tiles, crossing marquee tapes.
Every number is from brain/AQ_FACTS.md (as of 2025-26). Copy is DRAFT. Stories reuse each composition inside the 1080x1350 safe box
with marquee tapes filling the Instagram UI zones.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_why_fresh.py [feed story]
"""
import asyncio, base64, importlib.util, io, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("tt_carousel", os.path.join(ROOT, "scratchpad", "tt_carousel.py"))
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
tt, core, B = tc.tt, tc.core, tc.B
from PIL import Image

GROUND, ORCHID, GREEN, BLUE, HALO, INK, WHITE = "#000000", "#DE68F0", "#2FD284", "#0396FF", "#F3ECDE", "#0A0A0A", "#F5F5F5"
EV = "engine/assets/img/events/"
OUT = "out/terrathon_fresh"
ST_F = tt.ST_FEAT


def uri(path, w=1100, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

edu = Image.open("engine/assets/img/education-sundarban.jpeg"); ew, eh = edu.size
PH = dict(dance=uri("engine/assets/terrathon/dd_photos/dance.jpg"),
          students=uri(EV + "summer-aq-turns-five/07_group-portrait-pink-light.jpg", 900),
          classroom=uri("engine/assets/img/education-sundarban.jpeg", crop=(0, 0, ew, int(eh * 0.72))),
          blanket=uri("engine/assets/img/fundraising-diwali.jpeg"),
          group=uri(EV + "unsorted-2026-10-07/02_IMG_7028_group-pink-balloons.jpg", 900))

_cache = {}
def sticker(name, recolour=False):
    k = (name, recolour)
    if k not in _cache: _cache[k] = tc.sticker_src(name, recolour)
    return _cache[k]

async def mw(text, size, font="d", weight=900):
    """measured width of one string at `size` in its real face"""
    if font == "st":
        it = dict(text=text, font="StretchPro", size=size, weight=400, letter_spacing=f"{tt.ST_LS}em", features=ST_F)
    elif font == "sg":
        it = dict(text=text, font="SigmarOne", size=size, weight=400)
    else:
        it = dict(text=text, font=font, size=size, weight=weight)
    return (await B.measure_text([it], extra_css=tt.FONT_CSS))[0]["text_w"]

async def fit(text, target, font="d", weight=900):
    w = await mw(text, 100, font, weight); return 100 * target / w

def T(text, x, y, size, color, font="d", weight=900, rot=0, z=10, tag="t", ls=None, stroke=None, shadow=None, origin="left top", extra=""):
    fam = {"d": "var(--d)", "e": "var(--e)", "m": "var(--m)", "sg": "SigmarOne", "st": "StretchPro"}[font]
    css = f"font-family:{fam};font-size:{size}px;line-height:1;color:{color};white-space:nowrap;"
    if font == "st":
        css += f"font-weight:400;-webkit-text-stroke:{tt.ST_STROKE * size}px {stroke or color};letter-spacing:{tt.ST_LS}em;font-feature-settings:{ST_F};"
    elif font == "sg":
        css += f"font-weight:400;" + (f"-webkit-text-stroke:{stroke[0]}px {stroke[1]};paint-order:stroke fill;" if stroke else "")
    else:
        css += f"font-weight:{weight};"
    if shadow: css += f"text-shadow:{shadow};"
    if ls: css += f"letter-spacing:{ls};"
    tr = f"transform:rotate({rot}deg);transform-origin:{origin};" if rot else ""
    return (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;{css}{tr}z-index:{z};{extra}">{text}</div>')

def img(name, x, y, w, rot=0, z=6, recolour=False, tag="sticker"):
    im, src = sticker(name, recolour); h = w * im.height / im.width
    tr = f"transform:rotate({rot}deg);" if rot else ""
    return (f'<img class="measure" data-tag="{tag}" src="{src}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;{tr}z-index:{z}">', h)

def star(x, y, s=100, z=9):
    _, src = sticker("shuriken.png")
    return f'<img class="measure" data-tag="star" src="{src}" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;z-index:{z}">'

def band(y, color, text, rot, size=46, w=1500, h=108, z=8, txtcolor=INK, x=None, pad=0):
    """a marquee tape: a rotated colour strip with the text repeated across it"""
    x = -(w - 1080) / 2 if x is None else x
    rep = "&nbsp;&nbsp;✦&nbsp;&nbsp;".join([text] * 9)
    return (f'<div class="measure" data-tag="tape" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};transform:rotate({rot}deg);'
            f'z-index:{z};display:flex;align-items:center;overflow:hidden;padding-left:{pad}px;font-family:SigmarOne;font-size:{size}px;color:{txtcolor};white-space:nowrap;line-height:1">{rep}</div>')

def logo(y):
    return f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{y}px;height:56px;z-index:12">'

def ticket(w, h, fill, rot, x, y, inner, z=5, stub=0.74):
    """a perforated ticket: halo, fill, dashed stub line. `inner` is HTML in the ticket's own coordinates, so it rotates with it."""
    n = h * 0.14; pad = 22
    d = f"M0,0 H{w} V{h/2-n} A{n},{n} 0 0 0 {w},{h/2+n} V{h} H0 V{h/2+n} A{n},{n} 0 0 0 0,{h/2-n} Z"
    return (f'<div class="measure" data-tag="ticket" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z}">'
            f'<svg style="position:absolute;left:{-pad}px;top:{-pad}px;overflow:visible" width="{w+2*pad}" height="{h+2*pad}" viewBox="{-pad} {-pad} {w+2*pad} {h+2*pad}">'
            f'<path d="{d}" fill="{HALO}" stroke="{HALO}" stroke-width="{pad*1.4}" stroke-linejoin="round"/><path d="{d}" fill="{fill}"/>'
            f'<line x1="{w*stub}" y1="{n*1.4}" x2="{w*stub}" y2="{h-n*1.4}" stroke="{INK}" stroke-width="5" stroke-dasharray="4 16" stroke-linecap="round"/></svg>{inner}</div>')

def L(text, x, y, size, color=INK, font="d", weight=900, rot=0, origin="0 0"):
    fam = {"d": "var(--d)", "sg": "SigmarOne"}[font]
    tr = f"transform:rotate({rot}deg);transform-origin:{origin};" if rot else ""
    return f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:{fam};font-weight:{weight if font=="d" else 400};font-size:{size}px;line-height:1;color:{color};white-space:nowrap;{tr}">{text}</div>'

def burst_points(R, r, n):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n - math.pi / 2; rad = R if i % 2 == 0 else r
        pts.append(f"{R + rad * math.cos(a):.1f}px {R + rad * math.sin(a):.1f}px")
    return ",".join(pts)

def specks(W, H, seed=7):
    r = random.Random(seed)
    c = "".join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, H):.0f}" r="{r.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{r.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * H / 1350)))
    return f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{c}</svg>'

# ============================ SLIDES (content box 1080x1350, offset oy) ============================
async def s_cover(oy):
    p = []; fs1 = await fit("PAARTY", 980, "st"); fs2 = await fit("FOR GOOD", 980, "st")
    w1 = await mw("PAARTY", fs1, "st"); w2 = await mw("FOR GOOD", fs2, "st")
    p.append(T("PAARTY", (1080 - w1) / 2, oy + 70, fs1, WHITE, "st", tag="title1"))
    p.append(T("FOR GOOD", (1080 - w2) / 2, oy + 70 + fs1 * 1.0, fs2, ORCHID, "st", tag="title2"))
    pile, ph = img("carnival.png", 240, oy + 520, 600, z=4); p.append(pile)
    for x, y in ((50, oy + 520), (930, oy + 480), (900, oy + 840), (36, oy + 900)): p.append(star(x, y))
    p.append(band(oy + 1050, ORCHID, "WHY WE DO WHAT WE DO", -5, z=7, pad=240))
    p.append(T("EVENTS FUND THE WORK.", 540 - await mw("EVENTS FUND THE WORK.", 40, "d", 400) / 2, oy + 440, 40, WHITE, "d", 400, tag="sub"))
    p.append(logo(oy + 1262))
    els = [("title1", (1080 - w1) / 2, oy + 70, w1, fs1 * 0.8), ("title2", (1080 - w2) / 2, oy + 70 + fs1, w2, fs2 * 0.8)]
    return "".join(p), els

async def s_party(oy):
    p = []; fsz = await fit("THE PARTY", 900, "sg"); wz = await mw("THE PARTY", fsz, "sg")
    p.append(f'<div class="measure" data-tag="photo" style="position:absolute;left:80px;top:{oy + 80}px;width:920px;height:800px;transform:rotate(-3deg);z-index:3;'
             f'border-radius:70px 220px 70px 220px;border:20px solid {HALO};overflow:hidden;background:{HALO}"><img src="{PH["dance"]}" style="width:100%;height:100%;object-fit:cover;object-position:42% 40%"></div>')
    p.append(star(40, oy + 40)); p.append(star(930, oy + 840))
    p.append(T("THE PARTY", (1080 - wz) / 2, oy + 800, fsz, ORCHID, "sg", stroke=(14, INK), z=11, tag="title", rot=-2))
    c1 = (f'<div class="measure" data-tag="chip" style="position:absolute;left:90px;top:{oy + 1030}px;background:{GREEN};color:{INK};font-family:SigmarOne;font-size:46px;padding:22px 40px;'
          f'border-radius:999px;transform:rotate(-4deg);z-index:10;white-space:nowrap;border:6px solid {HALO}">ONE LOUD NIGHT.</div>')
    c2 = (f'<div class="measure" data-tag="chip" style="position:absolute;left:340px;top:{oy + 1135}px;background:{HALO};color:{INK};font-family:SigmarOne;font-size:46px;padding:22px 40px;'
          f'border-radius:999px;transform:rotate(3deg);z-index:10;white-space:nowrap;border:6px solid {ORCHID}">EVERY TICKET COUNTS.</div>')
    p += [c1, c2, logo(oy + 1262)]
    return "".join(p), [("title", (1080 - wz) / 2, oy + 690, wz, fsz * 0.9)]

async def s_ticket(oy):
    p = []
    t1 = (L("OF WHAT WE RAISE", 60, 44, 36, weight=400) + L("90%", 52, 86, 250) + L("COMES FROM EVENT", 60, 362, 34) + L("TICKETS + SPONSORS.", 60, 404, 34)
          + L("EVENTS", 0.74 * 940 + 98, 70, 62, font="sg", rot=90))
    t2 = (L("0%", 50, 30, 190) + L("INDIVIDUAL DONATIONS", 52, 236, 34) + L("NONE", 0.7 * 740 + 96, 70, 54, font="sg", rot=90))
    p.append(ticket(940, 500, GREEN, -5, 70, oy + 110, t1))
    p.append(ticket(740, 330, ORCHID, 4, 250, oy + 640, t2, z=7, stub=0.7))
    p.append(T("OF EVENT MONEY, ~80% IS TICKETS", 64, oy + 1040, 44, WHITE, "d", 400, tag="l1"))
    p.append(T("AND ~20% SPONSORS.", 64, oy + 1100, 44, WHITE, "d", 400, tag="l2"))
    f3 = min(52, await fit("STUDENTS EARN WHAT THEY GIVE.", 940, "sg"))
    p.append(T("STUDENTS EARN WHAT THEY GIVE.", 64, oy + 1180, f3, ORCHID, "sg", tag="l3"))
    for x, y in ((960, oy + 40), (20, oy + 560), (940, oy + 1090)): p.append(star(x, y))
    p.append(logo(oy + 1262))
    return "".join(p), []

async def s_students(oy):
    p = []; fs = await fit("25,000+", 960, "d"); w = await mw("25,000+", fs)
    p.append(T("25,000+", (1080 - w) / 2, oy + 40, fs, WHITE, "d", tag="num"))
    fl = await fit("VOLUNTEER HOURS, LOGGED", 900, "sg"); wl = await mw("VOLUNTEER HOURS, LOGGED", fl, "sg")
    p.append(T("VOLUNTEER HOURS, LOGGED", (1080 - wl) / 2, oy + 40 + fs * 0.92, fl, GREEN, "sg", tag="lab"))
    py = oy + 470
    p.append(f'<div class="measure" data-tag="polaroid" style="position:absolute;left:50px;top:{py}px;width:580px;height:700px;background:#F9F9F9;transform:rotate(-6deg);z-index:6;'
             f'padding:30px 30px 0;box-shadow:12px 12px 0 {ORCHID}"><img src="{PH["students"]}" style="width:520px;height:520px;object-fit:cover;object-position:50% 30%;display:block">'
             f'<div style="font-family:SigmarOne;font-size:40px;color:{INK};text-align:center;margin-top:34px">STUDENTS RUN IT</div></div>')
    p.append(f'<div class="measure" data-tag="tape" style="position:absolute;left:230px;top:{py - 24}px;width:200px;height:58px;background:{ORCHID};opacity:.95;transform:rotate(-8deg);z-index:9"></div>')
    p.append(T("AROUND", 680, py + 100, 56, WHITE, "d", 900, tag="r1"))
    p.append(T("1,100 OF US,", 680, py + 164, 56, WHITE, "d", 900, tag="r2"))
    p.append(T("BY 2025.", 680, py + 228, 56, WHITE, "d", 400, tag="r3"))
    s, _ = img("smiley.png", 720, py + 380, 270, rot=10, recolour=True); p.append(s)
    p += [star(940, py - 40), star(640, py + 640), star(930, py + 700), logo(oy + 1262)]
    return "".join(p), [("num", (1080 - w) / 2, oy + 40, w, fs * 0.75)]

async def s_zero(oy):
    p = []; fs = await fit("0%", 900, "sg"); w = await mw("0%", fs, "sg"); x = (1080 - w) / 2
    p.append(T("0%", x + 22, oy + 110 + 22, fs, GREEN, "sg", tag="zshadow", z=4))
    p.append(T("0%", x, oy + 110, fs, ORCHID, "sg", stroke=(10, INK), tag="zero", z=5))
    bandy = oy + 110 + fs * 0.95
    p.append(band(bandy, HALO, "NO INDIVIDUAL DONATIONS", -3, size=54, h=118, z=8, pad=270))
    p.append(T("STUDENTS EARN", 64, bandy + 190, 92, WHITE, "d", 900, tag="l1"))
    p.append(T("WHAT THEY GIVE.", 64, bandy + 190 + 92, 92, WHITE, "d", 400, tag="l2"))
    f, _ = img("flower.png", 650, bandy + 420, 380, rot=14, recolour=True); p.append(f)
    for x_, y_ in ((40, oy + 60), (930, oy + 30), (30, bandy + 450)): p.append(star(x_, y_))
    p.append(logo(oy + 1262))
    return "".join(p), [("zero", x, oy + 110 + fs * 0.1, w, fs * 0.8)]

async def s_class(oy):
    p = []; R = 430; sz = 2 * R
    pts = burst_points(R, 350, 16); cx, cy = 280, oy + 40
    p.append(f'<div class="measure" data-tag="bleed" style="position:absolute;left:{cx - 14}px;top:{cy - 14}px;width:{sz + 28}px;height:{sz + 28}px;background:{HALO};'
             f'clip-path:polygon({burst_points(R + 14, 364, 16)});z-index:3"></div>')
    p.append(f'<div class="measure" data-tag="bleed" style="position:absolute;left:{cx}px;top:{cy}px;width:{sz}px;height:{sz}px;clip-path:polygon({pts});z-index:4;overflow:hidden">'
             f'<img src="{PH["classroom"]}" style="width:100%;height:100%;object-fit:cover;object-position:35% 30%"></div>')
    fs = await fit("3,500+", 880, "d"); w = await mw("3,500+", fs)
    p.append(T("3,500+", 60, oy + 860, fs, WHITE, "d", tag="num"))
    lab = await fit("CHILDREN REACHED THROUGH WORKSHOPS", 940, "sg")
    p.append(T("CHILDREN REACHED", 64, oy + 860 + fs * 1.0, 54, GREEN, "sg", tag="lab1"))
    p.append(T("THROUGH WORKSHOPS", 64, oy + 860 + fs * 1.0 + 62, 54, GREEN, "sg", tag="lab2"))
    f, _ = img("flower.png", 20, oy + 120, 290, rot=-12, z=6, recolour=True); p.append(f)
    p += [star(20, oy + 520), star(960, oy + 900), logo(oy + 1262)]
    return "".join(p), [("num", 60, oy + 860 + fs * 0.1, w, fs * 0.7)]

async def s_blanket(oy):
    p = []; H_ = 960
    p.append(f'<div class="measure" data-tag="bleed" style="position:absolute;left:0;top:{oy + 16}px;width:1080px;height:{H_}px;background:{HALO};clip-path:polygon(0 0,100% 0,100% 62%,0 100%);z-index:3"></div>')
    p.append(f'<div class="measure" data-tag="bleed" style="position:absolute;left:0;top:{oy}px;width:1080px;height:{H_}px;clip-path:polygon(0 0,100% 0,100% 62%,0 100%);z-index:4;overflow:hidden">'
             f'<img src="{PH["blanket"]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 38%"></div>')
    p.append(f'<div class="measure" data-tag="bleed" style="position:absolute;left:0;top:{oy + 30}px;width:1080px;height:{H_}px;background:{ORCHID};clip-path:polygon(0 100%,100% 62%,100% 66%,0 105%);z-index:2"></div>')
    fs = await fit("A RIBBON. A NOTE.", 950, "d"); w1 = await mw("A RIBBON. A NOTE.", fs)
    p.append(T("A RIBBON. A NOTE.", 64, oy + 990, fs, WHITE, "d", tag="l1"))
    f2 = await fit("SOMEONE SEEN.", 950, "st");
    p.append(T("SOMEONE SEEN.", 64, oy + 990 + fs * 1.05, f2, ORCHID, "st", tag="l2"))
    s, _ = img("smiley.png", 790, oy + 700, 230, rot=-8, z=8, recolour=True); p.append(s)
    p += [star(960, oy + 560), star(900, oy + 1200), logo(oy + 1262)]
    return "".join(p), [("l1", 64, oy + 930, w1, fs * 0.8)]

async def s_wall(oy):
    p = []; fs = await fit("ALL OF THAT,", 940, "d")
    p.append(T("ALL OF THAT,", 64, oy + 50, min(fs, 110), WHITE, "d", tag="h1"))
    p.append(T("SO FAR.", 64, oy + 50 + 105, min(fs, 110), ORCHID, "d", tag="h2"))
    tiles = [(50, 330, GREEN, -4, "500+", "PROJECTS SINCE JUNE 2021"), (560, 310, ORCHID, 3, "3,500+", "CHILDREN, THROUGH WORKSHOPS"),
             (30, 610, BLUE, 3, "25,000+", "VOLUNTEER HOURS, LOGGED"), (560, 600, HALO, -3, "4,000+", "SAPLINGS AND TREES PLANTED"),
             (60, 890, ORCHID, -3, "1,600+", "MEDICAL CHECKUPS, SUNDERBANS"), (550, 880, GREEN, 4, "1,500+", "STRAY ANIMALS FED")]
    els = []
    for i, (x, y, col, rot, num, lab) in enumerate(tiles):
        nfs = await fit(num, 380, "d"); nfs = min(nfs, 120); lfs = min(26, await fit(lab, 372, "d", 400))
        p.append(f'<div class="measure" data-tag="tile" style="position:absolute;left:{x}px;top:{oy + y}px;width:470px;height:250px;background:{col};border:12px solid {HALO if col != HALO else ORCHID};'
                 f'border-radius:{[40, 90, 40, 90, 90, 40][i]}px;transform:rotate({rot}deg);z-index:6;display:flex;flex-direction:column;justify-content:center;padding:0 34px">'
                 f'<div style="font-family:var(--d);font-weight:900;font-size:{nfs}px;line-height:.95;color:{INK};white-space:nowrap">{num}</div>'
                 f'<div style="font-family:var(--d);font-weight:400;font-size:{lfs}px;line-height:1.1;color:{INK};margin-top:10px;white-space:nowrap">{lab}</div></div>')
    p.append(T("AS OF 2025-26 · FROM AQ RECORDS", 64, oy + 1190, 22, WHITE, "m", 700, tag="note", ls=".1em"))
    p += [star(940, oy + 40), star(560, oy + 1210), logo(oy + 1262)]
    return "".join(p), []

async def s_close(oy):
    p = []; fs = await fit("THE NEXT", 800, "d")
    for i, (t, c) in enumerate((("COME TO", WHITE), ("THE NEXT", WHITE), ("ONE.", ORCHID))):
        p.append(T(t, 64, oy + 70 + i * (fs * 0.92), fs, c, "d", tag=f"h{i}"))
    p.append(f'<div class="measure" data-tag="photo" style="position:absolute;left:560px;top:{oy + 640}px;width:470px;height:380px;transform:rotate(5deg);z-index:6;border-radius:200px;'
             f'border:16px solid {HALO};overflow:hidden;background:{HALO}"><img src="{PH["group"]}" style="width:100%;height:100%;object-fit:cover;object-position:50% 45%"></div>')
    p.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:64px;top:{oy + 650}px;background:{HALO};border:7px solid {ORCHID};border-radius:999px;color:{INK};font-family:var(--d);'
             f'font-weight:900;font-size:44px;padding:20px 42px;z-index:9;white-space:nowrap">@NGO.AQUATERRA</div>')
    p.append(T("THE TICKET", 64, oy + 790, 46, WHITE, "d", 400, tag="sub1"))
    p.append(T("DOES THE REST.", 64, oy + 850, 46, WHITE, "d", 400, tag="sub2"))
    p.append(band(oy + 1070, ORCHID, "SEE YOU AT THE NEXT ONE", -8, size=44, h=100, z=7, pad=240))
    p.append(band(oy + 1070, GREEN, "ALL FOR CHARITY", 8, size=44, h=100, z=8, pad=240))
    p += [star(960, oy + 40), star(480, oy + 560), logo(oy + 1262)]
    return "".join(p), []

SLIDES = [("00_cover", s_cover), ("01_party", s_party), ("02_ticket", s_ticket), ("03_students", s_students), ("04_zero", s_zero),
          ("05_classroom", s_class), ("06_blanket", s_blanket), ("07_numbers", s_wall), ("08_close", s_close)]

async def render(name, fn, canvas):
    W, H = (1080, 1350) if canvas == "feed" else (1080, 1920)
    oy = 0 if canvas == "feed" else 285
    body, els = await fn(oy)
    extra = ""
    if canvas == "story":
        extra = band(70, ORCHID, "ALL FOR CHARITY", -2, size=40, h=90, z=7) + band(1745, GREEN, "ALL FOR CHARITY", 2, size=40, h=90, z=7)
    html = B.page(W, H, GROUND, f'<style>{tt.FONT_CSS}</style>' + specks(W, H) + body + extra, grain=False)
    d = f"{OUT}/{canvas}"; os.makedirs(d, exist_ok=True)
    await B.render(html, f"{d}/{name}.png", W, H, elements=els or None, page_bg=GROUND, bleed_tags=("bleed", "tape"), crop_tags=("bleed", "tape", "photo", "tile", "polaroid"), margin=12)
    print("rendered", canvas, name)

async def main(canvases):
    async with B.session():
        for c in canvases:
            for name, fn in SLIDES: await render(name, fn, c)

if __name__ == "__main__":
    cv = [a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(main(cv))
