"""WHY WE DO WHAT WE DO: carousel (7), impact post (1), highlight story set (5). Workflow C, bespoke.

Reference: user's black-ground type carousel (gold flecks, white NeutralFace caps, marker/ring/underline marks,
one photo slide). Adaptations, per CLAUDE.md section 2 precedence ladder:
  * sponsor strip dropped: those are another event's partners, not AQ welfare partners (real-assets rule).
  * the reference's one-photo collage becomes full-bleed single photos: the repo holds only 4 real welfare
    photos, and two (food, edu) are finished posters, so the edu frame is cropped above its baked caption.
  * every number is from brain/AQ_FACTS.md with its source date. Nothing invented.
"""
import asyncio, base64, os, sys, random, importlib.util
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
A = core.ACCENTS; M = 64; BLACK = "#0A0A0A"; CREAM = "#F4EFE0"; MINT_B = "#00E5A0"
OUT = "out/why_we_do"; os.makedirs(OUT, exist_ok=True)
IMG = "engine/assets/img/"
def b64(p):
    with open(p, "rb") as f: return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()
PH = {k: b64(IMG + v) for k, v in dict(edu="education-sundarban.jpeg", xmas="christmas-khidirpur.jpeg",
                                       blanket="fundraising-diwali.jpeg").items()}

# ---------- marks ----------
def mark(t, col="#1B8A5A"):
    return (f'<span style="background:linear-gradient(transparent 10%,{col} 10%,{col} 94%,transparent 94%);'
            f'padding:0 10px;margin:0 -10px">{t}</span>')
def ring(t, col=MINT_B):
    return (f'<span style="position:relative;display:inline-block;padding:0 22px;margin:0 -22px">{t}<svg viewBox="0 0 100 100" preserveAspectRatio="none" '
            f'style="position:absolute;left:-4%;top:-14%;width:108%;height:130%;overflow:visible"><path d="M8 52 C3 20 40 5 70 9 '
            f'C99 13 105 46 91 71 C75 97 30 99 13 75 C7 66 5 57 8 49" fill="none" stroke="{col}" stroke-width="5" '
            f'stroke-linecap="round" style="vector-effect:non-scaling-stroke"/></svg></span>')
def under(t, col=A[3]):
    return f'<span style="background:linear-gradient({col},{col}) 0 100%/100% 7px no-repeat;padding-bottom:7px">{t}</span>'
def serif(t, col=CREAM):
    return f'<span style="font-family:var(--s);font-style:italic;font-weight:400;text-transform:none;color:{col}">{t}</span>'

# ---------- furniture ----------
LOGO_H = 34; LOGO_W = round(LOGO_H * 1332 / 225)
def logo_pill(x=M, y=56):
    w, h = LOGO_W + 36, LOGO_H + 16
    return (f'<div data-tag="logo" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:999px;'
            f'background:{CREAM};display:flex;align-items:center;justify-content:center;z-index:20">'
            f'<img src="{core.LOGO}" style="height:{LOGO_H}px"></div>'), (x, y, w, h)
def flecks(W, H, seed, n=70):
    r = random.Random(seed); out = ""
    for _ in range(n):
        s = r.choice([2, 3, 3, 4]); x = r.randint(10, W - 10); y = r.randint(10, H - 10)
        out += f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:#FFC700;opacity:{r.choice([.55,.8,1])};z-index:1"></div>'
    return out
def foot(W, H, right="swipe →", left="@ngo.aquaterra"):
    y = H - 74
    h = (f'<span data-tag="foot" style="position:absolute;left:{M}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:20px;'
         f'letter-spacing:.06em;color:{CREAM};z-index:20">{left}</span>')
    els = [("foot_l", M, y, 230, 26)]
    if right:
        h += (f'<span data-tag="foot" style="position:absolute;right:{M}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:20px;'
              f'letter-spacing:.06em;color:{MINT_B};z-index:20">{right}</span>'); els.append(("foot_r", W - M - 130, y, 130, 26))
    return h, els
def aq_globe(x, y, size, z=8):
    """the globe cropped out of the real wordmark (left square of core.LOGO)"""
    return (f'<div data-tag="globe" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;overflow:hidden;z-index:{z}">'
            f'<img src="{core.LOGO}" style="height:{size}px;width:auto;max-width:none;display:block"></div>'), ("globe", x, y, size, size)
def dood(kind, x, y, size, col, rot=0, z=8):
    return (f'<div data-tag="doodle" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;z-index:{z}">'
            f'{dd.stamp(kind, col, rot=rot)}</div>'), (f"doodle_{kind}", x, y, size, size)

# ---------- measured text ----------
async def fit(lines, size, maxw, font="d", weight=900):
    """lines: [(plain, html)] -> (fitted size, [text_w])"""
    ms = await B.measure_text([dict(text=p, font=font, size=size, weight=weight) for p, _ in lines])
    mx = max(m["text_w"] for m in ms)
    s = size if mx <= maxw else int(size * maxw / mx)
    if s != size:
        ms = await B.measure_text([dict(text=p, font=font, size=s, weight=weight) for p, _ in lines])
    return s, [m["text_w"] for m in ms]

async def headline(lines, size, x, y, maxw, color="#fff", lh=.98, z=10, tag="hl"):
    s, ws = await fit(lines, size, maxw)
    step = round(s * lh)
    html = "".join(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + i*step}px;white-space:nowrap;font-family:var(--d);'
                   f'font-weight:900;font-size:{s}px;line-height:{lh};text-transform:uppercase;color:{color};z-index:{z}">{h}</div>'
                   for i, (_, h) in enumerate(lines))
    els = [(f"{tag}{i}", x - 10, y + i * step, ws[i] + 20, step) for i in range(len(lines))]
    return html, els, y + len(lines) * step, s

async def body(text_lines, size, x, y, color=CREAM, lh=1.34, z=10, tag="body"):
    ms = await B.measure_text([dict(text=t, font="e", size=size, weight=400) for t in text_lines])
    step = round(size * lh)
    html = "".join(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + i*step}px;white-space:nowrap;font-family:var(--e);'
                   f'font-weight:400;font-size:{size}px;line-height:{lh};color:{color};z-index:{z}">{t}</div>' for i, t in enumerate(text_lines))
    els = [(f"{tag}{i}", x, y + i * step, ms[i]["text_w"], step) for i in range(len(text_lines))]
    return html, els, y + len(text_lines) * step

TP = [("headline", "#FFFFFF", BLACK, 80, True), ("body", CREAM, BLACK, 32, False), ("foot", CREAM, BLACK, 20, True),
      ("mintfoot", MINT_B, BLACK, 20, True)]
async def shoot(name, W, H, inner, els, pairs=None):
    html = B.page(W, H, BLACK, inner, grain=False)
    await B.render(html, f"{OUT}/{name}.png", W, H, elements=els, text_pairs=pairs or TP, page_bg=BLACK,
                   containers=("photo",), crop_tags=("photo", "globe"), margin=M)
    print("rendered", name)

def wrap(W, H, seed, *parts):
    return flecks(W, H, seed) + "".join(parts)

# ====================== CAROUSEL (1080x1350) ======================
W, H = 1080, 1350

async def c1_cover():
    lp, lbox = logo_pill()
    photo = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{W}px;height:980px;overflow:hidden;z-index:2">'
             f'<img src="{PH["edu"]}" style="position:absolute;left:0;top:-190px;width:{W}px;height:1350px">'
             f'<div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(transparent,{BLACK})"></div></div>')
    eb = (f'<div style="position:absolute;left:{M}px;top:938px;font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;'
          f'color:{MINT_B};z-index:10">TEAM AQUATERRA · KOLKATA · SINCE 2021</div>')
    h, he, yb, _ = await headline([("WHY WE DO", "WHY WE DO"), ("WHAT WE DO.", mark("WHAT WE DO."))], 112, M, 980, W - 2 * M)
    f, fe = foot(W, H)
    els = [("photo", 0, 0, W, 980), ("logo", *lbox), ("eyebrow", M, 938, 620, 24)] + he + fe
    await shoot("carousel_01", W, H, wrap(W, H, 1, photo, lp, eb, h, f), els)

async def c2_origin():
    lp, lbox = logo_pill()
    lines = [("IT STARTED IN 2021.", "IT STARTED IN 2021."), ("A 12TH GRADER.", "A 12TH GRADER."),
             ("A LOCKDOWN.", "A LOCKDOWN."), ("16 STUDENTS.", ring("16") + " STUDENTS.")]
    h, he, yb, s = await headline(lines, 100, M, 380, W - 2 * M - 40)
    b, be, yb2 = await body(["by 2025, around 1,100 of us.", "same idea. just louder."], 36, M, yb + 70)
    d, de = dood("thumbsup", W - M - 280, yb2 + 20, 260, "#fff", rot=-8)
    f, fe = foot(W, H)
    els = [("logo", *lbox)] + he + be + [de] + fe
    await shoot("carousel_02", W, H, wrap(W, H, 2, lp, h, b, d, f), els)

async def photo_slide(name, key, top, lines, sub, seed, pos="50% 25%", mark_idx=None, W=W, H=H, size=84, natural=False, hl_y=None):
    lp, lbox = logo_pill()
    if natural:   # story: photo at its own aspect, top-aligned, black below (never stretched)
        img = f'<img src="{PH[key]}" style="position:absolute;left:0;top:0;width:{W}px;height:auto">'
        fade_h = 520; fade_b = ""
    else:
        img = f'<img src="{PH[key]}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">'
    ph = int(W * 1.3333) if natural else H
    photo = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:hidden;z-index:2">{img}'
             f'<div style="position:absolute;left:0;right:0;top:{ph - 640}px;height:640px;background:linear-gradient(transparent,{BLACK} 78%)"></div>'
             f'<div style="position:absolute;left:0;right:0;top:{ph - 3}px;bottom:0;background:{BLACK}"></div></div>')
    n = len(lines)
    y0 = hl_y if hl_y is not None else H - 150 - (n * round(size * .98)) - (len(sub) * 48 if sub else 0) - 30
    h, he, yb, s = await headline(lines, size, M, y0, W - 2 * M)
    b, be, _ = await body(sub, 32, M, yb + 22) if sub else ("", [], yb)
    f, fe = foot(W, H, right="swipe →" if name.startswith("carousel") else "")
    els = [("photo", 0, 0, W, H), ("logo", *lbox)] + he + be + fe
    await shoot(name, W, H, wrap(W, H, seed, photo, lp, h, b, f), els)

async def c3():
    await photo_slide("carousel_03", "xmas", -40, [("A TREE MADE OF", "A TREE MADE OF"), ("PAPER STARS AND", "PAPER STARS AND"),
                      ("CRAYON WISHES.", mark("CRAYON WISHES."))], ["the part no spreadsheet captures."], 3, pos="50% 20%")

async def stat_slide_c4():
    lp, lbox = logo_pill()
    h, he, yb, s = await headline([("WHAT THAT", "WHAT THAT"), ("ADDS UP TO.", mark("ADDS UP TO."))], 100, M, 230, W - 2 * M)
    rows = [("500+", "projects since june 2021", A[0]), ("3,500+", "children reached through workshops", A[2]),
            ("25,000+", "hours of student volunteer time", MINT_B)]
    html = ""; els = []; y = yb + 60
    for n, lab, col in rows:
        ms = await B.measure_text([dict(text=n, font="d", size=170, weight=900)])
        html += (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{y}px;font-family:var(--d);font-weight:900;font-size:170px;'
                 f'line-height:.9;color:{col};white-space:nowrap;z-index:10">{n}</div>'
                 f'<div data-tag="lab" style="position:absolute;left:{M}px;top:{y + 158}px;font-family:var(--e);font-size:32px;'
                 f'color:{CREAM};white-space:nowrap;z-index:10">{lab}</div>')
        els += [(f"num_{n}", M, y, ms[0]["text_w"], 153), (f"lab_{n}", M, y + 158, 640, 40)]
        y += 262
    f, fe = foot(W, H)
    await shoot("carousel_04", W, H, wrap(W, H, 4, lp, h, html, f), [("logo", *lbox)] + he + els + fe)

async def c5():
    await photo_slide("carousel_05", "blanket", 0, [("A BLANKET. A RED RIBBON.", "A BLANKET. A RED RIBBON."), ("A NOTE THAT SAYS", "A NOTE THAT SAYS"),
                      ("WE SEE YOU.", "WE SEE " + ring("YOU."))], None, 5, pos="50% 30%", size=76)

async def big_stats(y, size, labsize, gap=56):
    """90% / 0% pair: returns html, els, bottom y. Column 2 starts after the WIDER of column 1's numeral and labels."""
    items = [("90%", ["of what we raise comes from", "event tickets and sponsors"], A[4]),
             ("0%", ["comes from individual", "donations"], A[0])]
    ms = await B.measure_text([dict(text=n, font="d", size=size, weight=900) for n, _, _ in items])
    lm = await B.measure_text([dict(text=t, font="e", size=labsize, weight=400) for _, lab, _ in items for t in lab])
    html = ""; els = []; x = M
    for k, ((n, lab, col), m) in enumerate(zip(items, ms)):
        c = core.on_dark(col, size)
        html += f'<div data-tag="num" style="position:absolute;left:{x}px;top:{y}px;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:.9;color:{c};white-space:nowrap;z-index:10">{n}</div>'
        els.append((f"stat_{n}", x, y, m["text_w"], int(size * .9)))
        lw = 0
        for i, ln in enumerate(lab):
            ly = y + int(size * .9) + 24 + i * round(labsize * 1.3); w = lm[k * 2 + i]["text_w"]; lw = max(lw, w)
            html += f'<div data-tag="lab" style="position:absolute;left:{x}px;top:{ly}px;font-family:var(--e);font-size:{labsize}px;color:{CREAM};white-space:nowrap;z-index:10">{ln}</div>'
            els.append((f"statlab_{n}{i}", x, ly, w, round(labsize * 1.3)))
        x += int(max(m["text_w"], lw)) + gap
    return html, els, y + int(size * .9) + 24 + 2 * round(labsize * 1.3)

async def c6():
    lp, lbox = logo_pill()
    lines = [("WE THROW THE PARTY.", "WE THROW THE PARTY."), ("THE PARTY PAYS", "THE PARTY PAYS"), ("FOR THE PROJECT.", mark("FOR THE PROJECT."))]
    h, he, yb, s = await headline(lines, 100, M, 300, W - 2 * M - 30)
    st, se, yb2 = await big_stats(yb + 100, 200, 28)
    chip = (f'<div data-tag="chip" style="position:absolute;left:{M}px;top:{yb2 + 80}px;background:{A[4]};color:{BLACK};font-family:var(--m);'
            f'font-weight:700;font-size:22px;letter-spacing:.06em;padding:14px 26px;border-radius:999px;z-index:10;white-space:nowrap">'
            f'19 FUNDRAISING EVENTS LOGGED, 2021-2025</div>')
    f, fe = foot(W, H)
    els = [("logo", *lbox)] + he + se + [("chip", M, yb2 + 80, 640, 56)] + fe
    await shoot("carousel_06", W, H, wrap(W, H, 6, lp, h, st, chip, f), els, TP + [("chip", BLACK, A[4], 22, True)])

async def c7():
    lp, lbox = logo_pill()
    lines = [("STILL “JUST A BUNCH", "STILL “JUST A BUNCH"), ("OF STUDENTS.”", "OF STUDENTS.”"), ("STILL SHOWING UP.", mark("STILL SHOWING UP."))]
    h, he, yb, s = await headline(lines, 100, M, 470, W - 2 * M - 30)
    b, be, yb2 = await body(["come to the next one.", "the ticket does the rest."], 40, M, yb + 70)
    pill = (f'<div data-tag="cta" style="position:absolute;left:{M}px;top:{yb2 + 60}px;background:{CREAM};color:{BLACK};font-family:var(--m);font-weight:700;'
            f'font-size:26px;letter-spacing:.04em;padding:18px 34px;border-radius:999px;z-index:10;white-space:nowrap">@ngo.aquaterra</div>')
    d, de = dood("heart", W - M - 330, yb2 - 30, 300, A[0], rot=8)
    f, fe = foot(W, H, right="")
    els = [("logo", *lbox)] + he + be + [("cta", M, yb2 + 60, 330, 66), de] + fe
    await shoot("carousel_07", W, H, wrap(W, H, 7, lp, h, b, pill, d, f), els, TP + [("cta", BLACK, CREAM, 26, True)])

# ====================== IMPACT POST (1080x1350) ======================
async def impact():
    lp, lbox = logo_pill()
    eb = (f'<div style="position:absolute;left:{M}px;top:140px;font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.14em;'
          f'color:{MINT_B};z-index:10">THE NUMBERS · AS OF 2025-26 · FROM AQ RECORDS</div>')
    h, he, yb, s = await headline([("WHAT THE PARTIES", "WHAT THE PARTIES"), ("ACTUALLY BUILT.", mark("ACTUALLY BUILT."))], 96, M, 190, W - 2 * M - 30)
    hm = await B.measure_text([dict(text="25,000+", font="d", size=200, weight=900)])
    hero = (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{yb + 30}px;font-family:var(--d);font-weight:900;font-size:200px;line-height:.9;'
            f'color:{MINT_B};white-space:nowrap;z-index:10">25,000+</div>'
            f'<div data-tag="lab" style="position:absolute;left:{M}px;top:{yb + 30 + 188}px;font-family:var(--e);font-size:32px;color:{CREAM};z-index:10;white-space:nowrap">'
            f'hours of student volunteer time, logged</div>')
    els = [("logo", *lbox), ("eyebrow", M, 140, 880, 24)] + he + [("hero", M, yb + 30, hm[0]["text_w"], 180), ("hero_lab", M, yb + 218, 640, 40)]
    cells = [("500+", "projects since june 2021", A[0]), ("3,500+", "children reached through workshops", A[2]),
             ("1,600+", "medical checkups, sunderbans camps", A[4]), ("4,000+", "saplings and trees planted", MINT_B),
             ("1,500+", "stray animals fed", A[3]), ("2.5 tons", "clothes and books donated", A[5])]
    gy = yb + 30 + 188 + 40 + 56; cw = (W - 2 * M - 30) // 2; rh = 118; html = ""
    for i, (n, lab, col) in enumerate(cells):
        cx = M + (i % 2) * (cw + 30); cy = gy + (i // 2) * rh
        c = col
        mm = await B.measure_text([dict(text=n, font="d", size=64, weight=900)])
        html += (f'<div data-tag="num" style="position:absolute;left:{cx}px;top:{cy}px;font-family:var(--d);font-weight:900;font-size:64px;line-height:1;'
                 f'color:{c};white-space:nowrap;z-index:10">{n}</div>'
                 f'<div data-tag="lab" style="position:absolute;left:{cx}px;top:{cy + 68}px;font-family:var(--e);font-size:24px;color:{CREAM};white-space:nowrap;z-index:10">{lab}</div>'
                 f'<div style="position:absolute;left:{cx}px;top:{cy - 14}px;width:{cw}px;height:2px;background:{col};z-index:9"></div>')
        els += [(f"cell{i}_n", cx, cy, mm[0]["text_w"], 64), (f"cell{i}_l", cx, cy + 68, cw - 20, 30)]
    by = gy + 3 * rh + 20
    band = (f'<div data-tag="band" style="position:absolute;left:{M}px;top:{by}px;width:{W - 2*M}px;height:104px;background:{A[4]};border-radius:22px;'
            f'z-index:10;display:flex;align-items:center;padding:0 30px;gap:22px">'
            f'<div style="font-family:var(--d);font-weight:900;font-size:50px;color:{BLACK};line-height:1;white-space:nowrap">19 EVENTS</div>'
            f'<div style="font-family:var(--e);font-size:25px;color:{BLACK};line-height:1.2">paid for it. about 90% of our revenue is event tickets and sponsors. 0% is donations.</div></div>')
    els.append(("band", M, by, W - 2 * M, 104))
    f, fe = foot(W, H, right="")
    await shoot("impact_numbers", W, H, wrap(W, H, 11, lp, eb, h, hero, html, band, f), els + fe,
                TP + [("bandtxt", BLACK, A[4], 25, False)])

# ====================== HIGHLIGHT STORY SET (1080x1920) ======================
SW, SH = 1080, 1920
async def s_cover():
    lp, lbox = logo_pill(y=120)
    g, ge = aq_globe(290, 560, 500)
    t, te, yb, s = await headline([("WHY", "WHY")], 300, 0, 1120, SW)
    t = t.replace("left:0px", f"left:0px;width:{SW}px;text-align:center")
    ws = await B.measure_text([dict(text="WHY", font="d", size=300, weight=900)])
    sub = (f'<div style="position:absolute;left:0;width:{SW}px;text-align:center;top:1480px;font-family:var(--m);font-weight:700;font-size:34px;'
           f'letter-spacing:.14em;color:{MINT_B};z-index:10">WE DO WHAT WE DO</div>')
    els = [("logo", *lbox), ge, ("why", (SW - ws[0]["text_w"]) / 2, 1120, ws[0]["text_w"], 290), ("sub", 250, 1480, 580, 40)]
    await shoot("story_00_cover", SW, SH, wrap(SW, SH, 20, lp, g, t, sub), els)

async def s_origin():
    lp, lbox = logo_pill(y=120)
    lines = [("IT STARTED", "IT STARTED"), ("IN 2021.", "IN 2021."), ("A 12TH GRADER.", "A 12TH GRADER."), ("A LOCKDOWN.", "A LOCKDOWN."),
             ("16 STUDENTS.", ring("16") + " STUDENTS.")]
    h, he, yb, s = await headline(lines, 112, M, 580, SW - 2 * M - 40)
    b, be, yb2 = await body(["by 2025, around 1,100 of us.", "same idea. just louder."], 40, M, yb + 70)
    d, de = dood("thumbsup", SW - M - 380, yb2 + 50, 340, "#fff", rot=-8)
    f, fe = foot(SW, SH, right="")
    await shoot("story_01_origin", SW, SH, wrap(SW, SH, 21, lp, h, b, d, f), [("logo", *lbox)] + he + be + [de] + fe)

async def s_stats():
    lp, lbox = logo_pill(y=120)
    h, he, yb, s = await headline([("WHAT THAT", "WHAT THAT"), ("ADDS UP TO.", mark("ADDS UP TO."))], 112, M, 400, SW - 2 * M - 30)
    rows = [("500+", "projects since june 2021", A[0]), ("3,500+", "children reached through workshops", A[2]),
            ("25,000+", "hours of student volunteer time", MINT_B), ("4,000+", "saplings and trees planted", A[4])]
    html = ""; els = []; y = yb + 80
    for n, lab, col in rows:
        c = col
        ms = await B.measure_text([dict(text=n, font="d", size=150, weight=900)])
        html += (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{y}px;font-family:var(--d);font-weight:900;font-size:150px;line-height:.9;'
                 f'color:{c};white-space:nowrap;z-index:10">{n}</div>'
                 f'<div data-tag="lab" style="position:absolute;left:{M}px;top:{y + 140}px;font-family:var(--e);font-size:30px;color:{CREAM};white-space:nowrap;z-index:10">{lab}</div>')
        els += [(f"n_{n}", M, y, ms[0]["text_w"], 135), (f"l_{n}", M, y + 140, 600, 40)]
        y += 235
    f, fe = foot(SW, SH, right="")
    await shoot("story_02_stats", SW, SH, wrap(SW, SH, 22, lp, h, html, f), [("logo", *lbox)] + he + els + fe)

async def s_photo():
    await photo_slide("story_03_photo", "xmas", 0, [("A TREE MADE OF", "A TREE MADE OF"), ("PAPER STARS AND", "PAPER STARS AND"),
                      ("CRAYON WISHES.", mark("CRAYON WISHES."))], ["the part no spreadsheet captures."], 23,
                      W=SW, H=SH, size=92, natural=True, hl_y=1330)

async def s_close():
    lp, lbox = logo_pill(y=120)
    lines = [("WE THROW", "WE THROW"), ("THE PARTY.", "THE PARTY."), ("THE PARTY PAYS", "THE PARTY PAYS"), ("FOR THE PROJECT.", mark("FOR THE PROJECT."))]
    h, he, yb, s = await headline(lines, 112, M, 480, SW - 2 * M - 30)
    st, se, yb2 = await big_stats(yb + 90, 196, 28)
    b, be, yb3 = await body(["come to the next one.", "the ticket does the rest."], 42, M, yb2 + 70)
    pill = (f'<div data-tag="cta" style="position:absolute;left:{M}px;top:{yb3 + 50}px;background:{CREAM};color:{BLACK};font-family:var(--m);font-weight:700;'
            f'font-size:28px;letter-spacing:.04em;padding:20px 38px;border-radius:999px;z-index:10;white-space:nowrap">@ngo.aquaterra</div>')
    f, fe = foot(SW, SH, right="")
    await shoot("story_04_close", SW, SH, wrap(SW, SH, 24, lp, h, st, b, pill, f),
                [("logo", *lbox)] + he + se + be + [("cta", M, yb3 + 50, 360, 74)] + fe, TP + [("cta", BLACK, CREAM, 28, True)])

async def main():
    async with B.session():
        for fn in (c1_cover, c2_origin, c3, stat_slide_c4, c5, c6, c7, impact, s_cover, s_origin, s_stats, s_photo, s_close):
            await fn()
    print("done")
asyncio.run(main())
