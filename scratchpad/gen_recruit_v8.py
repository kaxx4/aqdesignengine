"""AQ recruitment v8: group-chat question headlines + the real detail as the answer line (owner: "1+3 looks good") (narrative A in brain/RECRUITMENT_NARRATIVES_NOV2026.md).

Owner rulings (2026-11-13): talk about ALL the possibilities at AQ, do not name which seats are open; pay is never a topic
(no 'unpaid', no 'pay: none', nothing about money for the person); and 'students' as a word was repeating, so it is dropped
from the headlines (the photos carry the age). Build it without further questions.

THE SYSTEM
  headline  a torn cream strip "SOMEBODY ..." stacked over a lane-colour strip carrying the task, in NeutralFace caps
  proof     one real fact in tape (K.FACTS), or none on breadth pieces
  chrome    logo, a lane chip, the URL pill
  materials the v6 set: real cut-outs, chalk, spray, torn paper, tape, marker, grain, halftone
THE BREADTH IDEA: one master poster lists everything somebody does at AQ; every other piece is one item from that list
shown as a real scene. Same sentence, different job, different lane colour.

Copy rules kept: dry, specific, lowercase body, no em dashes, no Bengali, no member names, no pay language, no invented numbers.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_recruit_v6 as V
from gen_recruit_v6 import *            # helpers: cover_img, strip, tape, marker_path, note, chip, fact_tape, url_pill, window, bubble, ...
import recruit_kit as K
OUT = "out/recruit_nov2026/v8"
PH = K.PH
C = {"events": K.SKY, "welfare": K.MINT, "crftd": K.TOM, "collabs": K.PINK, "blogs": K.GRAPE, "social": K.GRAPE, "shikshaq": K.LEM, "hr": K.TEAL}

async def stack(lines, x, y, size, cols, rots, z=40, step=1.0, padx=28, seeds=(3, 5, 9, 11), fg=None, h=None):
    """measure, AUTO-FIT to the canvas, and place a stack of torn strips. returns (html, bottom_y)"""
    offs = [0, 54, 12, 70]
    ws = await K.mw([dict(text=t, font="d", size=size, weight=900) for t in lines])
    room = W - 24 - x
    need = max(w + 2 * padx + offs[i % 4] for i, w in enumerate(ws))
    k = min(1.0, room / need)
    size = int(size * k); ws = [w * k for w in ws]; padx = int(padx * k)
    hh = int((h or size * 1.08) * (k if h else 1)); out = []; yy = y
    for i, (t, w) in enumerate(zip(lines, ws)):
        bg = cols[i % len(cols)]
        out.append(strip(t, x + offs[i % 4], yy, int(w + 2 * padx), hh, bg, core.text_on(bg), rots[i % len(rots)], seeds[i % len(seeds)], size, tag=f"s{i}", z=z + i, padx=padx))
        yy += int(size * step)
    return "".join(out), yy + hh - int(size * step)

# ===================================================================== 1. THE MASTER LIST (breadth)
async def master(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{CREAM};z-index:0"></div>']
    P.append(blob_svg(640, 40 + top, 560, K.LEM, seed=12, sw=6, z=1, rot=15)); P.append(blob_svg(-160, base - 640, 520, K.PINK, seed=21, sw=6, z=1, rot=-12))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("hr", y=56 + top))
    lines = ["WHO'S DOING", "ALL THIS?"]
    size, ws = await fit(lines, W - 2 * M + 40, cap=300)
    P.append(big_type(lines, M - 8, 130 + top, size, INK, 20, step=.86, extra="text-shadow:8px 8px 0 #FFC700;"))
    tasks = [("BOOKING THE DHOL", "events"), ("FEEDING THE DOGS", "welfare"), ("TEACHING THE ALPHABET", "welfare"), ("SPRAYING A T-SHIRT", "crftd"), ("EMAILING A FOUNDATION", "collabs"),
             ("WRITING TO THE CITY", "blogs"), ("RUNNING A HEALTH CAMP", "welfare"), ("BUILDING THE TUTOR SEARCH", "shikshaq"), ("WRITING THE CAPTION", "social"), ("HANDING OUT SHARBAT", "welfare")]
    if story: tasks += [("EDITING THE REEL", "social"), ("WELCOMING A WHOLE COMMUNITY", "hr")]
    y0 = 130 + top + int(size * .86) * 2 + 40
    sz = 46; step = 78 if not story else 92
    avail = base - 100 - 30 - y0
    n = min(len(tasks), avail // step); tasks = tasks[:n]
    ws = await K.mw([dict(text=t, font="d", size=sz, weight=900) for t, _ in tasks])
    rots = [-2.2, 1.6, -1.2, 2.0, -1.8, 1.2, -2.0, 1.5, -1.4, 2.2, -1.6, 1.3]
    for i, ((t, dept), w) in enumerate(zip(tasks, ws)):
        x = M + [0, 80, 20, 140, 40, 110, 10, 90, 60, 130, 30, 100][i % 12]
        bg = C[dept]
        P.append(strip(t, x, y0 + i * step, int(w + 60), 64, bg, core.text_on(bg), rots[i % len(rots)], 40 + i, sz, tag=f"t{i}", z=30 + i, padx=26))
    P.append(note("(and a lot more)", W - 380, y0 + n * step - 10, 40, INK, -4, shadow=False))
    P.append(url_pill(base - 100)); P.append(tape(W - 260, base - 98, 120, 40, 6, seed=3))
    await done("d1_master" + ("_story" if story else ""), P, H, bg=CREAM)

# ===================================================================== 2. DHOL (events)
async def dhol(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/disco-diwali-dhol/01_live-dhol-pink-turban.jpg", W, H, fy=.4)
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 8, 6, op=.22, z=2), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,0,40,.6),rgba(10,0,40,0) 42%,rgba(0,0,0,0) 70%,rgba(0,0,0,.6));z-index:3"></div>', halftone_over(W, H, 4, .08), vignette(.4)]
    html, yb = await stack(["WHO'S BOOKING", "THE DHOL?"], M - 10, 128 + top, 150, ["#F6EFD8", K.SKY], [-2.4, 1.6])
    P.append(html)
    cy = H * (.66 if not story else .64)
    P.append(marker_path(scribble_ellipse(780, cy, 330, 400, seed=7), "#FFC700", 10))
    await chrome(P, "events", top, base, "disco diwali 2.0. 550 registrations, 10+ small businesses.", fw=700)
    await done("d2_dhol" + ("_story" if story else ""), P, H)

# ===================================================================== 3. DOGS (welfare)
async def dogs(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/08_dog-drive-bhowanipur.jpg", W, H, fy=.5)
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 9, 7, op=.3, z=2), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.3),rgba(0,0,0,0) 30%,rgba(0,0,0,0) 50%,rgba(0,0,0,.6));z-index:3"></div>', halftone_over(W, H, 4, .09, 5), vignette(.4)]
    html, yb = await stack(["WHO REMEMBERS", "THE BISCUITS?"], M - 14, 128 + top, 150, ["#F6EFD8", K.MINT], [-2.5, 1.5])
    P.append(html)
    ccy = H * (.66 if not story else .63) + (0 if not story else 40)
    P.append(marker_path(scribble_ellipse(560, ccy, 400, 235, seed=4), "#FFC700", 10))
    await chrome(P, "welfare", top, base, "tails and treats. round 53, first run january 2022.", fw=700)
    await done("d3_dogs" + ("_story" if story else ""), P, H)

# ===================================================================== 4. TEACH (chalk behind the class)
async def teach(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/10_teaching-abc-board.jpg", W, H, fy=.35)
    cut = clean_alpha(cover_img("cutouts/teach.png", W, H, fy=.35, grade=False), lo=110)
    bx0, by0, bx1, by1 = alpha_bbox(cut); bw, bh = bx1 - bx0, by1 - by0
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 7, 5, op=.18, z=2), f'<div style="position:absolute;inset:0;background:rgba(8,18,12,.42);z-index:3"></div>', halftone_over(W, H, 4, .06), vignette(.5)]
    lines = ["WHO'S WRITING", "THE ALPHABET", "ON THE BOARD?"]
    size, ws = await fit(lines, W - 2 * M + 60, cap=330)
    P.append(big_type(lines, M - 20, 120 + top, size, "#F4F1E6", 10, step=.88, filt="chalk"))
    P.append(img_layer(png(cut), W, H, 20))
    P.append(window(int(bx0), int(by0 + bh * .04), int(bw * .36), int(bh * .62), K.TOM, "THE TEACHER", "tr", blend="overlay", op=1))
    P.append(window(int(bx0 + bw * .42), int(by0 + bh * .3), int(bw * .56), int(bh * .62), K.LEM, "THE CLASS", "tl", blend="overlay", op=1))
    await chrome(P, "welfare", top, base, "about 70% of our welfare work is teaching.")
    P.append(tape(M + 30, base - 206, 120, 40, -8))
    await done("d4_teach" + ("_story" if story else ""), P, H)

# ===================================================================== 5. CRFTD (serif + spray)
async def crftd(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/12_roots-stall-novus-tee.jpg", W, H, fy=.3)
    P = [img_layer(jpg(bg), W, H, 1), misreg(jpg(bg), W, H, 8, 6, op=.22, z=2), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.4),rgba(0,0,0,.05) 35%,rgba(0,0,0,.1) 55%,rgba(0,0,0,.68));z-index:3"></div>', halftone_over(W, H, 4, .06, 5), vignette(.35)]
    lines = ["who's", "spraying", "the shirt?"]
    ws = await K.mw([dict(text=l, font="s", size=220, weight=400, style="normal") for l in lines])
    size = int(220 * min(1.0, (W - 2 * M + 40) / max(ws))); stepp = int(size * .84)
    y0 = base - 260 - stepp * 3 + 40
    for i, ln in enumerate(lines):
        col = "#FFFFFF" if i != 1 else "rgba(255,255,255,0)"
        P.append(f'<div class="measure" data-tag="sf{i}" style="position:absolute;left:{M-6}px;top:{y0 + i*stepp}px;white-space:nowrap;font-family:var(--s);font-size:{size}px;line-height:{stepp}px;color:{col};z-index:30;text-shadow:0 4px 28px rgba(0,0,0,.5)">{ln}</div>')
    P.append(f'<div style="position:absolute;left:{M-6}px;top:{y0 + stepp}px;white-space:nowrap;font-family:var(--s);font-style:italic;font-size:{size}px;line-height:{stepp}px;color:{K.TOM};z-index:31;filter:url(#spray)">spraying</div>')
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("crftd", y=56 + top))
    P.append(strip("SCHOOL FESTS", M - 10, 140 + top, 420, 76, "#F6EFD8", INK, -2.5, 31, 40, tag="t1", padx=18))
    P.append(strip("300 WALK-INS AT NOVUS", M + 60, 210 + top, 620, 76, K.LEM, INK, 1.5, 33, 40, tag="t2", padx=18))
    P.append(fact_tape("crftd, formerly roots. every rupee of profit funds a welfare drive.", M, base - 190, w=640, rot=-1.5))
    P.append(url_pill(base - 100))
    await done("d5_crftd" + ("_story" if story else ""), P, H)

# ===================================================================== 6. COLLABS (taped print)
async def collabs(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{K.PINK};z-index:0"></div>']
    P.append(blob_svg(-120, 120 + top, 760, K.LEM, seed=9, sw=6, z=2, rot=20)); P.append(blob_svg(520, base - 780, 640, K.SKY, seed=4, sw=6, z=2, rot=-10))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("collabs", y=56 + top))
    pw, ph = 880, int(880 * .72); px, py = (W - pw) // 2, 150 + top
    pic = cover_img("events/welfare-feed-2026/15_emami-science-city-lineup.png", pw, ph, fy=.5, fx=.5)
    P.append(f'<div style="position:absolute;left:{px}px;top:{py}px;width:{pw+36}px;height:{ph+36+70}px;transform:rotate(-2.2deg);background:#FBF8EE;box-shadow:10px 12px 0 rgba(10,10,10,.85);z-index:10;padding:18px"><img src="{jpg(pic)}" style="width:{pw}px;height:{ph}px;object-fit:cover;display:block"></div>')
    P.append(note("science city", px + 40, py + ph + 14, 54, INK, -3.5, shadow=False, z=30))
    P.append(tape(px + 60, py - 22, 170, 52, -8, seed=2)); P.append(tape(px + pw - 150, py - 18, 170, 52, 6, seed=5))
    sy = py + ph + 130
    html, yb = await stack(["WHO'S EMAILING", "THE FOUNDATION?"], M - 14, sy, 96, ["#F6EFD8", K.LEM], [-1.8, 1.4], h=108, step=1.1)
    P.append(html)
    P.append(fact_tape("with vishwajagriti and emami, at science city. 300 stationery kits, 30 kids hosted.", M, yb + 24, w=820, rot=-1))
    P.append(url_pill(base - 100))
    await done("d6_collabs" + ("_story" if story else ""), P, H, bg=K.PINK)

# ===================================================================== 7. SUNDARBANS (cast windows)
async def sundarbans(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/welfare-feed-2026/09_sundarbans-sunset-group.png", W, H, fy=.55)
    bg = ImageEnhance.Brightness(K.mono(bg, contrast=1.15)).enhance(1.25)
    P = [img_layer(jpg(bg), W, H, 1), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,10,10,.75),rgba(10,10,10,.25) 36%,rgba(0,0,0,0) 62%,rgba(0,0,0,.55));z-index:2"></div>', vignette(.4)]
    lines = ["who's packing for", "120 checkups?"]
    ws = await K.mw([dict(text=l, font="s", size=220, weight=400, style="normal") for l in lines])
    size = int(220 * min(1.0, (W - 2 * M + 30) / max(ws))); stepp = int(size * .9)
    for i, ln in enumerate(lines):
        it = "font-style:italic;" if i == 1 else ""
        P.append(f'<div class="measure" data-tag="sg{i}" style="position:absolute;left:{M-6}px;top:{128 + top + i*stepp}px;white-space:nowrap;font-family:var(--s);{it}font-size:{size}px;line-height:{stepp}px;color:#FFF3E0;z-index:30;text-shadow:0 3px 24px rgba(0,0,0,.7)">{ln}</div>')
    off = 0 if not story else 150
    P.append(window(120, 770 + off, 330, 280, K.MINT, "120+ CHECKUPS", "tl", 40)); P.append(window(470, 560 + off, 300, 300, K.LEM, "SUNDERBANS 8.0", "br", 40)); P.append(window(730, 700 + off, 270, 280, K.PINK, "DECEMBER 2025", "tl", 40))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("welfare", y=56 + top)); P.append(url_pill(base - 100))
    await done("d7_sundarbans" + ("_story" if story else ""), P, H)

# ===================================================================== 8. BLOGS (collage of real covers)
async def blogs(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{K.GRAPE};z-index:0"></div>']
    P.append(blob_svg(520, 60 + top, 700, K.LEM, seed=14, sw=6, z=1, rot=30)); P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("blogs", y=56 + top))
    html, yb = await stack(["WHO'S WRITING", "TO THE CITY?"], M - 10, 130 + top, 150, ["#F6EFD8", K.LEM], [-2.2, 1.5])
    P.append(html)
    covers = [("events/welfare-feed-2026/blog-people-in-the-mirror.jpg", -6, 40), ("events/welfare-feed-2026/blog-dynamics.jpg", 3, 330), ("events/welfare-feed-2026/blog-letter-to-my-city.jpg", -3, 640)]
    cw = 330; chh = 500; cy0 = yb + 70
    for i, (path, rot, x) in enumerate(covers):
        pic = cover_img(path, cw, chh)
        P.append(f'<div style="position:absolute;left:{x+30}px;top:{cy0 + (i%2)*40}px;width:{cw+28}px;height:{chh+28+54}px;transform:rotate({rot}deg);background:#FBF8EE;box-shadow:9px 10px 0 rgba(10,10,10,.85);z-index:{20+i};padding:14px">'
                 f'<img src="{jpg(pic)}" style="width:{cw}px;height:{chh}px;object-fit:cover;display:block"></div>')
        P.append(tape(x + 120, cy0 + (i % 2) * 40 - 18, 110, 38, rot * 2, seed=30 + i, z=60))
    P.append(fact_tape("letter to my city, dynamics, people in the mirror. real posts on our own site.", M, base - 190, rot=-1.5)); P.append(url_pill(base - 100))
    await done("d8_blogs" + ("_story" if story else ""), P, H, bg=K.GRAPE)

# ===================================================================== 9. SOCIAL (the team's own slides)
async def social(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{K.GRAPE};z-index:0"></div>']
    P.append(blob_svg(-180, 400 + top, 620, K.PINK, seed=17, sw=6, z=1, rot=10)); P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("social", y=56 + top))
    html, yb = await stack(["WHO'S WRITING", "THE CAPTION?"], M - 10, 130 + top, 130, ["#F6EFD8", K.LEM], [-2, 1.5], h=140)
    P.append(html)
    from PIL import Image as _I
    _im = _I.open(K.IMG + K.social_slide(9)); sw_ = 400; sh_ = int(sw_ * _im.height / _im.width); cy0 = yb + 60
    for i, (n, rot, x) in enumerate([(9, -5, 90), (12, 3, 540)]):
        pic = cover_img(K.social_slide(n), sw_, sh_)
        P.append(f'<div style="position:absolute;left:{x}px;top:{cy0 + i*40}px;width:{sw_+24}px;height:{sh_+24}px;transform:rotate({rot}deg);background:#FBF8EE;box-shadow:9px 10px 0 rgba(10,10,10,.85);z-index:{20+i};padding:12px">'
                 f'<img src="{jpg(pic)}" style="width:{sw_}px;height:{sh_}px;object-fit:cover;display:block"></div>')
        P.append(tape(x + 150, cy0 + i * 40 - 16, 110, 38, rot * 2, seed=50 + i, z=60))
    P.append(fact_tape("this week at aq, by the social media team.", M, base - 190, rot=-1.5)); P.append(url_pill(base - 100))
    await done("d9_social" + ("_story" if story else ""), P, H, bg=K.GRAPE)

# ===================================================================== 10. SHIKSHAQ (cleared facts only)
async def shikshaq(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    P = [f'<div style="position:absolute;inset:0;background:{K.LEM};z-index:0"></div>']
    P.append(blob_svg(560, 520 + top, 720, K.PINK, seed=6, sw=6, z=1, rot=-8)); P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("shikshaq", y=56 + top))
    html, yb = await stack(["WHO'S FINDING", "THE MATHS", "TUTOR?"], M - 10, 128 + top, 140, ["#F6EFD8", INK, "#F6EFD8"], [-2.2, 1.6, -1])
    html = html.replace("color:#0A0A0A", "color:#0A0A0A")
    P.append(html)
    chips = ["KOLKATA", "CLASS IV TO XII", "ICSE", "ISC", "CBSE", "STATE BOARD"]
    cws = await K.mw([dict(text=c, font="d", size=34, weight=900) for c in chips]); cx, cy = M, yb + 60; rots = [-3, 2, -2, 3, -1.5, 2.5]
    for c, tw_, r in zip(chips, cws, rots):
        cw = int(tw_ + 66)
        if cx + cw > W - M: cx, cy = M + 30, cy + 100
        P.append(f'<div style="position:absolute;left:{cx}px;top:{cy}px;height:78px;padding:0 30px;border:4px solid #0A0A0A;border-radius:14px;background:#FBF8EE;box-shadow:6px 6px 0 #0A0A0A;transform:rotate({r}deg);z-index:30;font-family:var(--d);font-weight:900;font-size:34px;line-height:70px;text-transform:uppercase;color:#0A0A0A">{c}</div>')
        cx += cw + 22
    P.append(note("shikshaq.in", 560, cy + 150, 96, INK, -4, shadow=False, z=40))
    P.append(marker_path(scribble_arrow(580, cy + 250, 470, cy + 200, bend=-30), INK, 9))
    P.append(fact_tape("shikshaq.in. a tutor search for kolkata.", M, base - 190, w=760, rot=-1.5)); P.append(url_pill(base - 100))
    await done("d10_shikshaq" + ("_story" if story else ""), P, H, bg=K.LEM)

# ===================================================================== 11. CLOSER (photo, the ask)
async def closer(story=False):
    H = 1920 if story else 1350; top = safe(H, story); bot = bottom(H, story); base = H - bot
    bg = cover_img("events/unsorted-2026-10-07/01_IMG_7180_group-aquaterra-banner.jpg", W, H, fx=.5, fy=.6)
    P = [img_layer(jpg(bg), W, H, 1), f'<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55),rgba(0,0,0,0) 35%,rgba(0,0,0,0) 50%,rgba(0,0,0,.7));z-index:2"></div>', vignette(.35)]
    html, yb = await stack(["SO WHO'S", "DOING IT?"], M - 10, 120 + top, 190, ["#F6EFD8", K.TEAL], [-2.2, 1.6], h=210)
    P.append(html)
    P.append(note("(you?)", M + 10, base - 470, 110, "#FFFFFF", -4))
    P.append(K.logo_pill(M, 44 + top, dark=True)); P.append(chip("hr", y=56 + top))
    P.append(bubble("come once. decide after.", M + 10, base - 340, -3, 34))
    P.append(fact_tape("applications are open.", M, base - 190, rot=-1.5)); P.append(url_pill(base - 100))
    await done("d11_closer" + ("_story" if story else ""), P, H)

JOBS = {"master": master, "dhol": dhol, "dogs": dogs, "teach": teach, "crftd": crftd, "collabs": collabs, "sundarbans": sundarbans, "blogs": blogs, "social": social, "shikshaq": shikshaq, "closer": closer}
STORY = {"master", "dhol", "dogs", "teach", "crftd", "closer", "sundarbans"}

async def main7(only, stories=True):
    async with K.B.session():
        for k, fn in JOBS.items():
            if only and k not in only: continue
            await fn(False)
            if stories and k in STORY: await fn(True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    args = [a for a in sys.argv[1:] if a != "--feed"]
    asyncio.run(main7(set(args) or None, stories="--feed" not in sys.argv))
