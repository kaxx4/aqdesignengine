"""EVENTS -> IMPACT: carousel (8 slides, 1080x1350) + story set (7 frames, 1080x1920). Workflow C, bespoke.

"How a party becomes a project": 1 the party, 2 the ticket, 3 students run it, 4 what it becomes, then numbers, then CTA.
Reuses the helper block of gen_why_we_do_v1.py (exec of everything above its CAROUSEL marker).
Adaptations / honesty notes:
  * revenue split is the revenue doc's (~90% events, of which ~80% tickets / ~20% sponsors; ~10% ROOTS; 0% donations).
  * no ticket-to-outcome conversion is stated anywhere: none exists. "Sometimes a blanket, sometimes a classroom" is scoped.
  * photo captions follow file names/content: dd_photos (Disco Diwali), education-sundarban, fundraising-diwali (blanket).
  * 4 accents on black + cream; sky is the events hue by rule, so the recipe's colour count is exceeded on purpose.
"""
import os, sys, asyncio, io, base64
_HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_HERE, "gen_why_we_do_v1.py")).read().split("# ====================== CAROUSEL")[0])
from PIL import Image
OUT = "out/events_vibe"; os.makedirs(OUT, exist_ok=True)

def pimg(path, maxw=1080):
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=86)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), im.height / im.width
EV = "engine/assets/img/events/"
DANCE_DD, _ = pimg("engine/assets/terrathon/dd_photos/dance.jpg", 1500)
CROWD, CROWD_R = pimg(EV + "unsorted-2026-10-07/11_dance-green-light-portrait.jpg")
SETUP, SETUP_R = pimg(EV + "summer-aq-turns-five/07_group-portrait-pink-light.jpg")
GROUP, GROUP_R = pimg(EV + "unsorted-2026-10-07/02_IMG_7028_group-pink-balloons.jpg")
BLANKET, BLANKET_R = PH["blanket"], 1600 / 1200
EDU = PH["edu"]

def step_chip(txt, x, y):
    return (f'<div data-tag="chip" style="position:absolute;left:{x}px;top:{y}px;height:42px;padding:0 20px;border-radius:999px;background:{MINT_B};color:{BLACK};'
            f'font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.1em;display:flex;align-items:center;white-space:nowrap;z-index:12">{txt}</div>')
async def chip_w(txt):
    m = await B.measure_text([dict(text=txt, font="m", size=18, weight=700, letter_spacing=1.8)]); return int(m[0]["text_w"]) + 40

TPX = TP + [("chip", BLACK, MINT_B, 18, True), ("chip2", BLACK, CREAM, 17, True), ("bar", BLACK, A[4], 30, True), ("pill", CREAM, BLACK, 16, True)]

async def big_stats(y, size, labsize, gap=56, W=1080):
    items = [("90%", ["of what we raise comes from", "event tickets and sponsors"], A[4]), ("0%", ["comes from individual", "donations"], A[0])]
    ms = await B.measure_text([dict(text=n, font="d", size=size, weight=900) for n, _, _ in items])
    lm = await B.measure_text([dict(text=t, font="e", size=labsize, weight=400) for _, lab, _ in items for t in lab])
    html = ""; els = []; x = M
    for k, ((n, lab, col), m) in enumerate(zip(items, ms)):
        html += f'<div data-tag="num" style="position:absolute;left:{x}px;top:{y}px;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:.9;color:{core.on_dark(col, size)};white-space:nowrap;z-index:10">{n}</div>'
        els.append((f"stat_{n}", x, y, m["text_w"], int(size * .9))); lw = 0
        for i, ln in enumerate(lab):
            ly = y + int(size * .9) + 24 + i * round(labsize * 1.3); w = lm[k * 2 + i]["text_w"]; lw = max(lw, w)
            html += f'<div data-tag="lab" style="position:absolute;left:{x}px;top:{ly}px;font-family:var(--e);font-size:{labsize}px;color:{CREAM};white-space:nowrap;z-index:10">{ln}</div>'
            els.append((f"statlab_{n}{i}", x, ly, w, round(labsize * 1.3)))
        x += int(max(m["text_w"], lw)) + gap
    return html, els, y + int(size * .9) + 24 + 2 * round(labsize * 1.3)

def pair_photos(W, x0, y0, LW, RW, h, gut=16):
    left = (f'<div data-tag="photo" style="position:absolute;left:{x0}px;top:{y0}px;width:{LW}px;height:{h}px;overflow:hidden;z-index:2">'
            f'<img src="{DANCE_DD}" style="width:100%;height:100%;object-fit:cover;object-position:42% 40%"></div>')
    right = (f'<div data-tag="photo" style="position:absolute;left:{x0 + LW + gut}px;top:{y0}px;width:{RW}px;height:{h}px;overflow:hidden;z-index:2">'
             f'<img src="{EDU}" style="position:absolute;left:-255px;top:-204px;width:918px;height:1148px"></div>')
    return left, right

def arrow_badge(cx, cy, d=112, rot=0):
    return (f'<div data-tag="badge" style="position:absolute;left:{cx - d // 2}px;top:{cy - d // 2}px;width:{d}px;height:{d}px;border-radius:50%;background:{MINT_B};'
            f'border:6px solid {BLACK};display:flex;align-items:center;justify-content:center;z-index:14;transform:rotate({rot}deg)">'
            f'<svg width="{int(d*.54)}" height="{int(d*.54)}" viewBox="0 0 60 60"><path d="M8 30 H46 M32 14 L48 30 L32 46" fill="none" stroke="{BLACK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'), (cx - d // 2, cy - d // 2, d, d)

def pill_c(txt, x, y):
    return (f'<div data-tag="chip2" style="position:absolute;left:{x}px;top:{y}px;height:40px;padding:0 18px;border-radius:999px;background:{CREAM};color:{BLACK};'
            f'font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.08em;display:flex;align-items:center;white-space:nowrap;z-index:12">{txt}</div>')

async def photo_full(name, W, H, src, pos, step, lines, sub, seed, size=92, natural_r=None, extra="", extra_els=(), sw=1.0, cta=None):
    """full-bleed (cover) photo, or natural_r=h/w to keep the photo's own aspect top-aligned with black below"""
    lp, lbox = logo_pill(y=120 if H > 1500 else 56)
    if natural_r:
        ph = round(W * natural_r)
        img = f'<img src="{src}" style="position:absolute;left:0;top:0;width:{W}px;height:auto">'
    else:
        ph = H
        img = f'<img src="{src}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos}">'
    gh = 680 if natural_r else int(H * .55)
    photo = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;overflow:hidden;z-index:2">{img}'
             f'<div style="position:absolute;left:0;right:0;top:{ph - gh}px;height:{gh}px;background:linear-gradient(transparent,{BLACK} 80%)"></div>'
             f'<div style="position:absolute;left:0;right:0;top:{ph - 3}px;bottom:0;background:{BLACK}"></div></div>')
    stp = round(size * .98); n = len(lines)
    reserve = 104 if cta else 0
    y0 = H - 150 - (len(sub) * 46 if sub else 0) - n * stp - 24 - reserve
    if natural_r: y0 = min(y0, ph - 40 - n * stp + 0) if False else y0
    h, he, yb, s = await headline(lines, size, M, y0, W - 2 * M)
    b, be, yend = await body(sub, 32, M, yb + 22) if sub else ("", [], yb)
    if cta:
        fs = 28 if H > 1500 else 26; ph_ = 74 if H > 1500 else 66
        extra = (f'<div data-tag="cta" style="position:absolute;left:{M}px;top:{yend + 30}px;background:{CREAM};color:{BLACK};font-family:var(--m);font-weight:700;font-size:{fs}px;letter-spacing:.04em;'
                 f'padding:{ph_ // 2 - 18}px 34px;border-radius:999px;z-index:12;white-space:nowrap">{cta}</div>')
        extra_els = list(extra_els) + [("cta", M, yend + 30, 340, ph_)]
    cw = await chip_w(step); chip = step_chip(step, M, y0 - 66)
    f, fe = foot(W, H, right="" if cta else ("swipe →" if H < 1500 and name.startswith("carousel") else ""), left="" if cta else "@ngo.aquaterra")
    els = [("photo", 0, 0, W, H), ("logo", *lbox), ("chip", M, y0 - 66, cw, 42)] + he + be + list(extra_els) + fe
    await shoot(name, W, H, wrap(W, H, seed, photo, lp, chip, h, b, extra, f), els, TPX)

async def type_slide(name, W, H, step, lines, seed, builder, size=100, y_top=None, right_foot="swipe →"):
    lp, lbox = logo_pill(y=120 if H > 1500 else 56)
    y_top = y_top or (300 if H < 1500 else 430)
    cw = await chip_w(step); chip = step_chip(step, M, y_top - 70)
    h, he, yb, s = await headline(lines, size, M, y_top, W - 2 * M - 30)
    html, els2 = await builder(yb)
    f, fe = foot(W, H, right=right_foot)
    await shoot(name, W, H, wrap(W, H, seed, lp, chip, h, html, f), [("logo", *lbox), ("chip", M, y_top - 70, cw, 42)] + he + els2 + fe, TPX)

# ====================== CAROUSEL ======================
W, H = 1080, 1350

async def c1():
    lp, lbox = logo_pill()
    LW, RW, PHH = 628, 436, 760
    l, r = pair_photos(W, 0, 0, LW, RW, PHH)
    c1h = pill_c("THE PARTY", 24, PHH - 64); c2h = pill_c("THE PROJECT", LW + 16 + 24, PHH - 64)
    bd, bb = arrow_badge(LW + 8, 380)
    h, he, yb, s = await headline([("HOW A PARTY", "HOW A PARTY"), ("BECOMES A PROJECT.", mark("BECOMES A PROJECT."))], 98, M, 830, W - 2 * M - 30)
    b, be, yb2 = await body(["four steps. swipe."], 36, M, yb + 40)
    f, fe = foot(W, H)
    els = [("photo", 0, 0, LW, PHH), ("photo", LW + 16, 0, RW, PHH), ("logo", *lbox), ("chipL", 24, PHH - 64, 150, 40), ("chipR", LW + 40, PHH - 64, 190, 40), ("badge", *bb)] + he + be + fe
    await shoot("carousel_01", W, H, wrap(W, H, 41, l, r, lp, c1h, c2h, bd, h, b, f), els, TPX)

async def c2():
    cap = (f'<div data-tag="chip2" style="position:absolute;right:{M}px;top:62px;height:40px;padding:0 18px;border-radius:999px;background:{A[4]};color:{BLACK};font-family:var(--m);font-weight:700;'
           f'font-size:17px;letter-spacing:.08em;display:flex;align-items:center;white-space:nowrap;z-index:12">19 EVENTS LOGGED, 2021-2025</div>')
    await photo_full("carousel_02", W, H, CROWD, "50% 58%", "STEP 1 OF 4", [("WE THROW", "WE THROW"), ("THE PARTY.", mark("THE PARTY."))], ["paradox. disco diwali. starry night. terrathon."], 42,
                     size=104, extra=cap, extra_els=[("tag", W - M - 380, 62, 380, 40)])

async def c3():
    async def bld(yb):
        st, se, y2 = await big_stats(yb + 70, 200, 28)
        b, be, _ = await body(["of event money, ~80% is tickets and ~20% sponsors.", "students earn the money they deploy."], 28, M, y2 + 40, lh=1.32)
        by = y2 + 40 + 2 * 37 + 78; BW = W - 2 * M; w1 = round(BW * .9)
        lab = (f'<div style="position:absolute;left:{M}px;top:{by - 34}px;font-family:var(--m);font-weight:700;font-size:16px;letter-spacing:.14em;color:{MINT_B};z-index:10;white-space:nowrap">WHERE AQ&#39;S MONEY COMES FROM</div>')
        bar = (f'<div data-tag="bar" style="position:absolute;left:{M}px;top:{by}px;width:{BW}px;height:64px;border-radius:14px;overflow:hidden;display:flex;z-index:10">'
               f'<div style="width:{w1}px;background:{A[4]};color:{BLACK};font-family:var(--d);font-weight:900;font-size:30px;display:flex;align-items:center;padding-left:24px;white-space:nowrap">EVENTS ~90%</div>'
               f'<div style="flex:1;background:{A[5]}"></div></div>')
        rl = (f'<div style="position:absolute;right:{M}px;top:{by + 72}px;font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.08em;color:{core.on_dark(A[5], 15)};z-index:10;white-space:nowrap">ROOTS (CLOTHING BRAND) ~10%</div>')
        return st + b + lab + bar + rl, se + be + [("barlab", M, by - 34, 420, 22), ("bar", M, by, BW, 64), ("rootslab", W - M - 262, by + 72, 262, 20)]
    await type_slide("carousel_03", W, H, "STEP 2 OF 4", [("THE TICKET", "THE TICKET"), ("DOES THE WORK.", mark("DOES THE WORK."))], 43, bld, y_top=300)

async def c4():
    await photo_full("carousel_04", W, H, SETUP, "50% 45%", "STEP 3 OF 4", [("STUDENTS RUN", "STUDENTS RUN"), ("ALL OF IT.", mark("ALL OF IT."))],
                     ["25,000+ volunteer hours, logged.", "around 1,100 of us, by 2025."], 44, size=104)

async def c5():
    await photo_full("carousel_05", W, H, BLANKET, "50% 30%", "STEP 4 OF 4", [("A BLANKET. A RIBBON.", "A BLANKET. A RIBBON."), ("A NOTE.", "A " + ring("NOTE."))],
                     ["one thing a party becomes."], 45, size=96)

async def c6():
    lp, lbox = logo_pill()
    photo = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{W}px;height:960px;overflow:hidden;z-index:2">'
             f'<img src="{EDU}" style="position:absolute;left:0;top:-190px;width:{W}px;height:1350px">'
             f'<div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(transparent,{BLACK})"></div></div>')
    cw = await chip_w("OR, SOMETIMES"); chip = step_chip("OR, SOMETIMES", M, 930)
    h, he, yb, s = await headline([("A CLASSROOM FULL", "A CLASSROOM FULL"), ("OF LAUGHTER.", mark("OF LAUGHTER."))], 90, M, 1000, W - 2 * M - 30)
    b, be, _ = await body(["3,500+ children reached through workshops."], 28, M, yb + 14)
    f, fe = foot(W, H)
    await shoot("carousel_06", W, H, wrap(W, H, 46, photo, lp, chip, h, b, f), [("photo", 0, 0, W, 960), ("logo", *lbox), ("chip", M, 930, cw, 42)] + he + be + fe, TPX)

async def grid_cells(y, W, rh=122, size=64):
    cells = [("500+", "projects since june 2021", A[0]), ("3,500+", "children, through workshops", A[2]), ("1,600+", "medical checkups, sunderbans camps", A[4]),
             ("4,000+", "saplings and trees planted", MINT_B), ("1,500+", "stray animals fed", A[3]), ("2.5 tons", "clothes and books donated", A[5])]
    cw = (W - 2 * M - 30) // 2; html = ""; els = []
    for i, (n, lab, col) in enumerate(cells):
        cx = M + (i % 2) * (cw + 30); cy = y + (i // 2) * rh
        mm = await B.measure_text([dict(text=n, font="d", size=size, weight=900)])
        html += (f'<div data-tag="num" style="position:absolute;left:{cx}px;top:{cy}px;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;color:{col};white-space:nowrap;z-index:10">{n}</div>'
                 f'<div data-tag="lab" style="position:absolute;left:{cx}px;top:{cy + 68}px;font-family:var(--e);font-size:24px;color:{CREAM};white-space:nowrap;z-index:10">{lab}</div>'
                 f'<div style="position:absolute;left:{cx}px;top:{cy - 14}px;width:{cw}px;height:2px;background:{col};z-index:9"></div>')
        els += [(f"cell{i}_n", cx, cy, mm[0]["text_w"], size), (f"cell{i}_l", cx, cy + 68, cw - 20, 30)]
    return html, els, y + 3 * rh

async def c7():
    lp, lbox = logo_pill()
    h, he, yb, s = await headline([("ALL OF THAT,", "ALL OF THAT,"), ("SO FAR.", mark("SO FAR."))], 100, M, 200, W - 2 * M - 30)
    hm = await B.measure_text([dict(text="25,000+", font="d", size=200, weight=900)])
    hero = (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{yb + 30}px;font-family:var(--d);font-weight:900;font-size:200px;line-height:.9;color:{MINT_B};white-space:nowrap;z-index:10">25,000+</div>'
            f'<div data-tag="lab" style="position:absolute;left:{M}px;top:{yb + 218}px;font-family:var(--e);font-size:32px;color:{CREAM};z-index:10;white-space:nowrap">hours of student volunteer time, logged</div>')
    gh, ge, gy2 = await grid_cells(yb + 30 + 188 + 40 + 56, W)
    note = (f'<div style="position:absolute;left:{M}px;top:{gy2 + 12}px;font-family:var(--m);font-weight:700;font-size:15px;letter-spacing:.1em;color:{MINT_B};z-index:10;white-space:nowrap">'
            f'AS OF 2025-26 · FROM AQ RECORDS</div>')
    f, fe = foot(W, H)
    els = [("logo", *lbox)] + he + [("hero", M, yb + 30, hm[0]["text_w"], 180), ("hero_lab", M, yb + 218, 640, 40)] + ge + [("note", M, gy2 + 12, 460, 20)] + fe
    await shoot("carousel_07", W, H, wrap(W, H, 47, lp, h, hero, gh, note, f), els, TPX)

async def c8():
    await photo_full("carousel_08", W, H, GROUP, "50% 40%", "NEXT TIME", [("COME TO THE", "COME TO THE"), ("NEXT ONE.", mark("NEXT ONE."))], ["the ticket does the rest."], 48,
                     size=104, cta="@ngo.aquaterra")

# ====================== STORIES ======================
SW, SH = 1080, 1920

async def s0():
    lp, lbox = logo_pill(y=120)
    g, ge = aq_globe(290, 520, 500)
    t, te, yb, s = await headline([("EVENTS", "EVENTS")], 220, 0, 1100, SW)
    t = t.replace("left:0px", f"left:0px;width:{SW}px;text-align:center")
    ws = await B.measure_text([dict(text="EVENTS", font="d", size=s, weight=900)])
    sub = (f'<div style="position:absolute;left:0;width:{SW}px;text-align:center;top:1420px;font-family:var(--m);font-weight:700;font-size:30px;letter-spacing:.14em;color:{MINT_B};z-index:10">WHAT THEY MAKE POSSIBLE</div>')
    await shoot("story_00_cover", SW, SH, wrap(SW, SH, 50, lp, g, t, sub), [("logo", *lbox), ge, ("events", (SW - ws[0]["text_w"]) / 2, 1100, ws[0]["text_w"], int(s * .98)), ("sub", 200, 1420, 680, 36)], TPX)

async def s1():
    lp, lbox = logo_pill(y=120)
    PH_H = 700
    left = (f'<div data-tag="photo" style="position:absolute;left:0;top:0;width:{SW}px;height:{PH_H}px;overflow:hidden;z-index:2"><img src="{DANCE_DD}" style="width:100%;height:100%;object-fit:cover;object-position:42% 40%"></div>')
    right = (f'<div data-tag="photo" style="position:absolute;left:0;top:{PH_H + 16}px;width:{SW}px;height:{PH_H}px;overflow:hidden;z-index:2">'
             f'<img src="{EDU}" style="position:absolute;left:0;top:-250px;width:{SW}px;height:1350px"></div>')
    c1h = pill_c("THE PARTY", M, PH_H - 66); c2h = pill_c("THE PROJECT", M, 2 * PH_H + 16 - 66)
    bd, bb = arrow_badge(SW // 2, PH_H + 8, 124, rot=90)
    h, he, yb, s = await headline([("THE PARTY FUNDS", "THE PARTY FUNDS"), ("THE PROJECT.", mark("THE PROJECT."))], 96, M, 1470 + 52, SW - 2 * M - 30)
    f, fe = foot(SW, SH, right="")
    els = [("photo", 0, 0, SW, PH_H), ("photo", 0, PH_H + 16, SW, PH_H), ("logo", *lbox), ("chipL", M, PH_H - 66, 150, 40), ("chipR", M, 2 * PH_H - 50, 190, 40), ("badge", *bb)] + he + fe
    await shoot("story_01_pair", SW, SH, wrap(SW, SH, 51, left, right, lp, c1h, c2h, bd, h, f), els, TPX)

async def s2():
    async def bld(yb):
        by = yb + 90; BW = SW - 2 * M; w1 = round(BW * .9)
        bar = (f'<div data-tag="bar" style="position:absolute;left:{M}px;top:{by}px;width:{BW}px;height:92px;border-radius:18px;overflow:hidden;display:flex;z-index:10">'
               f'<div style="width:{w1}px;background:{A[4]};color:{BLACK};font-family:var(--d);font-weight:900;font-size:44px;display:flex;align-items:center;padding-left:30px;white-space:nowrap">EVENTS ~90%</div>'
               f'<div style="flex:1;background:{A[5]}"></div></div>')
        rl = (f'<div style="position:absolute;right:{M}px;top:{by + 104}px;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.08em;color:{core.on_dark(A[5], 20)};z-index:10;white-space:nowrap">ROOTS (CLOTHING BRAND) ~10%</div>')
        cap, cape, cy = await body(["of event money, ~80% is tickets", "and ~20% sponsors."], 34, M, by + 150, lh=1.3)
        z = await B.measure_text([dict(text="0%", font="d", size=300, weight=900)])
        zy = cy + 70
        zero = (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{zy}px;font-family:var(--d);font-weight:900;font-size:300px;line-height:.9;color:{core.on_dark(A[0], 300)};white-space:nowrap;z-index:10">0%</div>'
                f'<div data-tag="lab" style="position:absolute;left:{M + int(z[0]["text_w"]) + 36}px;top:{zy + 90}px;font-family:var(--e);font-size:34px;line-height:1.3;color:{CREAM};white-space:nowrap;z-index:10">from individual<br>donations. students<br>earn what they give.</div>')
        zl = await B.measure_text([dict(text="earn what they give.", font="e", size=34, weight=400)])
        els = [("bar", M, by, BW, 92), ("rootslab", SW - M - 420, by + 104, 420, 26)] + cape + [("zero", M, zy, z[0]["text_w"], 270), ("zerolab", M + int(z[0]["text_w"]) + 36, zy + 90, zl[0]["text_w"], 135)]
        return bar + rl + cap + zero, els
    await type_slide("story_02_money", SW, SH, "WHERE THE MONEY COMES FROM", [("THE TICKET", "THE TICKET"), ("DOES THE WORK.", mark("DOES THE WORK."))], 52, bld, size=108, y_top=560, right_foot="")

async def s3():
    await photo_full("story_03_students", SW, SH, SETUP, "50% 40%", "STEP 3 OF 4", [("STUDENTS RUN", "STUDENTS RUN"), ("ALL OF IT.", mark("ALL OF IT."))],
                     ["25,000+ volunteer hours, logged.", "around 1,100 of us, by 2025."], 53, size=104, natural_r=SETUP_R)

async def s4():
    await photo_full("story_04_blanket", SW, SH, BLANKET, "50% 30%", "WHAT IT BECOMES", [("A BLANKET.", "A BLANKET."), ("A CLASSROOM.", "A CLASSROOM."), ("A MEAL.", "A " + ring("MEAL."))],
                     ["not a promise of a number. a promise to show up."], 54, size=104, natural_r=BLANKET_R)

async def s5():
    lp, lbox = logo_pill(y=120)
    h, he, yb, s = await headline([("ALL OF THAT,", "ALL OF THAT,"), ("SO FAR.", mark("SO FAR."))], 112, M, 360, SW - 2 * M - 30)
    rows = [("500+", "projects since june 2021", A[0]), ("3,500+", "children, through workshops", A[2]), ("25,000+", "hours of student volunteer time", MINT_B), ("4,000+", "saplings and trees planted", A[4])]
    html = ""; els = []; y = yb + 80
    for n, lab, col in rows:
        ms = await B.measure_text([dict(text=n, font="d", size=150, weight=900)])
        html += (f'<div data-tag="num" style="position:absolute;left:{M}px;top:{y}px;font-family:var(--d);font-weight:900;font-size:150px;line-height:.9;color:{col};white-space:nowrap;z-index:10">{n}</div>'
                 f'<div data-tag="lab" style="position:absolute;left:{M}px;top:{y + 140}px;font-family:var(--e);font-size:30px;color:{CREAM};white-space:nowrap;z-index:10">{lab}</div>')
        els += [(f"n_{n}", M, y, ms[0]["text_w"], 135), (f"l_{n}", M, y + 140, 620, 40)]; y += 235
    note = (f'<div style="position:absolute;left:{M}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.1em;color:{MINT_B};z-index:10;white-space:nowrap">AS OF 2025-26 · FROM AQ RECORDS</div>')
    f, fe = foot(SW, SH, right="")
    await shoot("story_05_numbers", SW, SH, wrap(SW, SH, 55, lp, h, html, note, f), [("logo", *lbox)] + he + els + [("note", M, y, 560, 26)] + fe, TPX)

async def s6():
    await photo_full("story_06_close", SW, SH, GROUP, "50% 40%", "NEXT TIME", [("COME TO THE", "COME TO THE"), ("NEXT ONE.", mark("NEXT ONE."))], ["the ticket does the rest."], 56,
                     size=108, natural_r=GROUP_R, cta="@ngo.aquaterra")

async def main():
    async with B.session():
        for fn in (c1, c2, c3, c4, c5, c6, c7, c8, s0, s1, s2, s3, s4, s5, s6):
            await fn()
    print("done")
asyncio.run(main())
