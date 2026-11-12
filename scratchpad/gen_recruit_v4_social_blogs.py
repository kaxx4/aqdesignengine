"""AQ recruitment v4: SOCIAL MEDIA, BLOGS and HR pieces (five pieces, five different skeletons from the 74-style bank).

  social_1  abd472f264528c  lane social (grape)  T5  bubble-outline banner over a photo, pinboard of white cards quoting the team's real lines
  social_2  d252704dc5e5f3  lane social (grape)  T4  2x2 block collage stitched by torn tape strips naming what the department covers
  blogs_1   51010a5e1a5625  lane blogs  (grape)  T1  giant 4-line headline on grid paper, one line highlighted, real blog titles as chips
  blogs_2   10f1b8a9789261  lane blogs  (grape)  T4  stacked headline, marker rectangle + pill, a real student cover die-cut across the seam
  hr_2      114f2b19c46119  lane hr     (teal)   T3  three phones in a row, each a real AQ asset, one sticky-note prop repeated

ADAPTATIONS (CLAUDE.md section 2 ladder; every one is the brand beating a recipe, the mechanism kept):
  * Instrument Serif is <=1 accent word per piece, so the serif-led recipes (social_2 serif caps + serif body, blogs_1 giant serif
    headline) are set in NeutralFace uppercase / Eina lowercase with ONE italic serif word. The mechanism (a giant stacked headline;
    a headline block / checker block / body block) is kept; only the face changes.
  * social_2 recipe says exactly 4 colours; the department hue (grape) is fixed by rule, and the real slide panel brings its own colours.
  * hr_2's reference is a LINKEDIN landscape mockup; here three portrait phones on a 4:5 canvas. The triptych-with-a-repeated-prop
    mechanism is kept; the fake onboarding chat is replaced by REAL assets (a Social Media team slide, a blog cover, a drive photo).
  * social_1 cards stay white and ink-only as the recipe says; colour sits in doodles and the photo fragments (slide thumbnails).
  * Child photos are owner-cleared (brief section 3). Photo folders welfare-feed-2026 are local-only, so this script runs only where they exist.
"""
import os, sys, asyncio, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
from PIL import Image

INK, CREAM, PAPER = K.INK, K.CREAM, K.PAPER
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = K.PINK, K.MINT, K.LEM, K.TOM, K.SKY, K.GRAPE, K.TEAL
t, box, img, uri, cover, dd = K.t, K.box, K.img, K.uri, K.cover, K.dd
W = 1080
SH = f"box-shadow:6px 6px 0 {INK};"

def mw(items):
    return asyncio.run(K.mw(items))

def fit(text, font, weight, target, cap=400):
    w = mw([dict(text=text, font=font, size=100, weight=weight)])[0]
    return min(cap, int(100 * target / w)), w

def doodle(kind, x, y, s, col, rot=0, z=9):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;z-index:{z}">{dd.stamp(kind, col, rot=rot)}</div>'

def slide_img(n, w, h, fy=.0, fx=.5):
    return cover(K.social_slide(n), w, h, fx=fx, fy=fy)

# ------------------------------------------------------------------------------------------------ social_1
def social_1():
    H = 1350
    bg = cover(K.PH["dd_group"], W, H, fx=.1, fy=.5)
    P = [img(uri(bg), 0, 0, W, H, z=1),
         box(0, 0, W, H, "background:linear-gradient(180deg,rgba(10,10,10,.30),rgba(10,10,10,.18) 40%,rgba(10,10,10,.5));", z=2)]
    P.append(K.logo_pill(64, 48))
    P.append(K.series_tab(50))
    P.append(K.lane_chip("social", y=112))
    # bubble title: white fill, thick ink outline, hard shadow (sized from a measurement, never guessed)
    s1, _ = fit("WELL, WELL,", "d", 900, 820)
    s2, _ = fit("WELL.", "d", 900, 430)
    for i, (txt, y, sz, x, rot) in enumerate([("WELL, WELL,", 168, s1, 70, -2), ("WELL.", 168 + s1 - 22, s2, 440, 1.5)]):
        P.append(t(txt, x, y, sz, color=PAPER, font="d", weight=900, lh=sz, z=14, tag=f"title{i}", upper=True,
                   extra=f"-webkit-text-stroke:14px {INK};paint-order:stroke fill;filter:drop-shadow(6px 6px 0 {INK});transform:rotate({rot}deg);letter-spacing:.01em;"))
    P.append(f'<div style="position:absolute;left:70px;top:{168+s1+28}px;width:290px;z-index:14;transform:rotate(-3deg)">'
             f'<div class="measure" data-tag="sub" style="background:{LEM};border:3px solid {INK};{SH}padding:10px 14px;font-family:var(--m);font-weight:700;font-size:15px;line-height:21px;color:{INK};letter-spacing:.04em">'
             f'THE SOCIAL MEDIA TEAM, IN ITS OWN WORDS</div></div>')

    def card(x, y, w, h, rot, inner, z=10):
        return (f'<div class="measure" data-tag="card" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;min-height:{h}px;background:{PAPER};border:3px solid {INK};border-radius:14px;{SH}'
                f'padding:16px 20px;box-sizing:border-box;transform:rotate({rot}deg);z-index:{z};color:{INK}">{inner}</div>')
    lab = lambda s: f'<div style="font-family:var(--m);font-weight:700;font-size:13px;letter-spacing:.06em;color:#555;margin-bottom:6px">{s}</div>'
    body = lambda s, sz=24: f'<div style="font-family:var(--e);font-size:{sz}px;line-height:{round(sz*1.26)}px;color:{INK}">{s}</div>'
    disp = lambda s, sz=34: f'<div style="font-family:var(--d);font-weight:900;font-size:{sz}px;line-height:{round(sz*1.0)}px;text-transform:uppercase;color:{INK}">{s}</div>'
    Y1 = 470
    P.append(card(70, Y1, 460, 190, -2.0, lab("A REAL CAPTION") + body("apparently, resting was once again not on the AQ agenda. tragic.", 29)))
    P.append(card(566, Y1 - 8, 440, 190, 2.4, lab("THIS WEEK AT AQ") + disp("Rest? Never heard of it", 34)
                  + '<div style="height:8px"></div>' + body("a break would have been nice, but the team is already planning the next one.", 19)))
    thumbs = "".join(f'<img src="{uri(slide_img(n, 112, 200, fy=.0))}" style="width:112px;height:200px;object-fit:cover;border:2px solid {INK};border-radius:6px;transform:rotate({r}deg)">'
                     for n, r in [(9, -3), (10, 2), (12, -1)])
    Y2 = 700
    P.append(card(70, Y2, 390, 250, 1.6, lab("4 ISSUES, 16 SLIDES") + f'<div style="display:flex;gap:8px;justify-content:center">{thumbs}</div>', z=11))
    P.append(card(488, Y2 - 4, 520, 128, -1.5, lab("ANOTHER REAL CAPTION") + body("Well, well, well, AQ has been <b style='font-weight:800'>BUSY</b> this week.", 30)))
    P.append(card(520, Y2 + 150, 488, 150, 2.0, lab("THIS WEEK AT AQ") + disp("No, it is not welfare", 30)
                  + '<div style="height:6px"></div>' + body("people keep assuming shikshaq is a welfare project, and we are working on fixing that.", 18), z=12))
    P.append(card(70, 980, 360, 150, -2.2, lab("CRFTD IS DROWNING IN ORDERS") + body("it is a good problem to have, but the team is working through the backlog before anything else.", 20), z=12))
    P.append(f'<div class="measure" data-tag="card" style="position:absolute;left:480px;top:1010px;width:330px;background:{PAPER};border:3px solid {INK};border-radius:46px;{SH}padding:18px 26px;box-sizing:border-box;transform:rotate(-1.5deg);z-index:13">'
             f'<div style="font-family:var(--d);font-weight:900;font-size:36px;line-height:38px;text-transform:uppercase">who writes <span style="font-family:var(--s);font-style:italic;font-weight:400;text-transform:none;font-size:46px">these?</span></div></div>')
    P.append(f'<div style="position:absolute;left:520px;top:1103px;width:36px;height:36px;background:{PAPER};border-right:3px solid {INK};border-bottom:3px solid {INK};transform:rotate(45deg) skew(8deg,8deg);z-index:12"></div>')
    P.append(f'<div class="measure" data-tag="note" style="position:absolute;left:840px;top:1030px;width:176px;z-index:13;font-family:var(--m);font-weight:700;font-size:14px;line-height:20px;color:{PAPER};letter-spacing:.04em;text-align:left">ANSWER: THE SOCIAL MEDIA TEAM. APPLICATIONS ARE OPEN.</div>')
    P.append(doodle("star", 462, 975, 64, LEM, 12, 15))
    P.append(doodle("sparkle", 20, 655, 56, PINK, -10, 15))
    P.append(doodle("heart", 960, 640, 60, PINK, 10, 15))
    P.append(doodle("burst", 930, 160, 84, GRAPE, 12, 15))
    P.append(doodle("sparkle", 960, 940, 60, LEM, 0, 15))
    P.append(K.url_pill(y=1188))
    return K.render("social_1", K.page("".join(P)), H)

# ------------------------------------------------------------------------------------------------ social_2
def tape(x, y, w, h, txt, rot, col=LEM, size=56, z=20):
    random.seed(len(txt) * 7 + x)
    n = 6; step = h / n
    pl = [f"0 0"]
    pts_r = [(w - random.choice((0, 5, 9)), i * step) for i in range(n + 1)]
    pts_l = [(random.choice((0, 5, 9)), i * step) for i in range(n + 1)]
    poly = ",".join([f"{a}px {b}px" for a, b in pts_l] + [f"{a}px {b}px" for a, b in reversed(pts_r)])
    return (f'<div class="measure" data-tag="tape" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);z-index:{z};'
            f'filter:drop-shadow(4px 5px 0 rgba(10,10,10,.55))"><div style="width:100%;height:100%;background:{col};clip-path:polygon({poly});'
            f'font-family:var(--d);font-weight:900;font-size:{size}px;line-height:{h}px;text-align:center;color:{INK};letter-spacing:.01em">{txt}</div></div>')

def checker(w, h, c1, c2, cell):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{c1}"/>'
    for r in range(0, h // cell + 1):
        for c in range(0, w // cell + 1):
            if (r + c) % 2: s += f'<rect x="{c*cell}" y="{r*cell}" width="{cell}" height="{cell}" fill="{c2}"/>'
    return s + "</svg>"

def social_2():
    H = 1350
    P = []
    VX, HY, BX = 740, 640, 400          # seams (deliberately not a uniform grid)
    P.append(box(0, 0, VX, HY, f"background:{INK};", z=2))
    ck = checker(W - VX, HY, GRAPE, "#C9BBFF", 80)
    P.append(f'<div style="position:absolute;left:{VX}px;top:0;width:{W-VX}px;height:{HY}px;z-index:2;overflow:hidden;line-height:0">{ck}</div>')
    sl = slide_img(15, BX, H - HY, fy=.0, fx=.5)
    P.append(img(uri(sl), 0, HY, BX, H - HY, z=2))
    P.append(box(BX, HY, W - BX, H - HY, f"background:{CREAM};", z=2))
    P.append(K.logo_pill(64, 48, dark=True))
    P.append(K.series_tab(58))
    P.append(K.lane_chip("social", y=116))
    P.append(t("WHO MAKES", 64, 206, 94, color=CREAM, font="d", weight=900, lh=96, z=6, tag="h1", upper=True))
    P.append(t("THE", 64, 292, 94, color=CREAM, font="d", weight=900, lh=96, z=6, tag="h2", upper=True))
    P.append(t("posts?", 290, 262, 176, color=LEM, font="s", italic=True, lh=170, z=6, tag="h3"))
    bx = 636; bw = W - bx - 64
    P.append(t("this week at aq is written, designed and posted by students aged 14 to 19.", bx, HY + 78, 30, color=INK, font="e", weight=600, w=bw, lh=40, z=6, tag="body1"))
    P.append(t("so are the reels. so are the blogs.", bx, HY + 270, 30, color=INK, font="e", weight=600, w=bw, lh=40, z=6, tag="body2"))
    P.append(t("there are 1,400+ of us. applications are open.", bx, HY + 395, 30, color=INK, font="e", weight=600, w=bw, lh=40, z=6, tag="body3"))
    P.append(f'<div style="position:absolute;left:{VX-50}px;top:{HY-70}px;width:130px;height:130px;z-index:15">{dd.stamp("burst", PINK, rot=8)}</div>')
    # tape strips across the seams, read top to bottom as one list
    P.append(tape(VX - 300, 470, 400, 78, "INSTAGRAM,", -5))
    P.append(tape(-14, 585, 440, 78, "LINKEDIN,", 3.5))
    P.append(tape(310, 700, 270, 74, "REELS,", -4, size=52))
    P.append(tape(330, 812, 250, 74, "BLOGS,", 4, size=52))
    P.append(tape(358, 928, 262, 72, "DESIGN.", -3, size=52))
    P.append(K.url_pill(x=bx, y=1188, w=W - bx - 64, size=19))
    return K.render("social_2", K.page("".join(P), bg=CREAM), H)

# ------------------------------------------------------------------------------------------------ blogs_1
def gridpaper(w, h, step=32):
    s = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
    for x in range(0, w + 1, step): s += f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#0A0A0A" stroke-opacity=".10" stroke-width="1.5"/>'
    for y in range(0, h + 1, step): s += f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#0A0A0A" stroke-opacity=".10" stroke-width="1.5"/>'
    return s + "</svg>"

def chip(x, y, label, rot=0, col=GRAPE, z=16):
    wpx = int(len(label) * 10.4 + 62)
    ic = (f'<div style="position:absolute;left:8px;top:8px;width:30px;height:30px;border-radius:50%;background:{col};border:2px solid {INK};box-sizing:border-box"></div>')
    return (f'<div class="measure" data-tag="chip" style="position:absolute;left:{x}px;top:{y}px;width:{wpx}px;height:46px;border-radius:14px;background:{PAPER};border:3px solid {INK};{"box-shadow:4px 4px 0 "+INK+";"}'
            f'box-sizing:border-box;transform:rotate({rot}deg);z-index:{z};font-family:var(--e);font-weight:600;font-size:18px;line-height:40px;color:{INK};padding-left:48px;white-space:nowrap">{ic}{label}</div>')

def blogs_1():
    H = 1350
    P = [box(0, 0, W, H, f"background:{CREAM};", z=0), f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:1">{gridpaper(W, H)}</div>']
    P.append(K.logo(64, 48)); P.append(K.series_tab(58)); P.append(K.lane_chip("blogs", y=116))
    lines = ["SOMEONE", "WROTE TO", "THEIR", "CITY."]
    sz = 200
    ws = mw([dict(text=s, font="d", size=sz, weight=900) for s in lines])
    sz = int(sz * min(1.0, 900 / max(ws)))
    ws = [w * sz / 200 for w in ws]
    step = round(sz * .93); y0 = 290
    xs = [64] * 4
    print("size", sz, "widths", [int(w) for w in ws])
    i = 3   # highlight band behind CITY.
    P.append(box(xs[i] - 14, y0 + i * step + round(sz * .10), int(ws[i]) + 28, round(sz * .80), f"background:{GRAPE};border-radius:6px;", z=3))
    for i, s in enumerate(lines):
        P.append(t(s, xs[i], y0 + i * step, sz, color=INK, font="d", weight=900, lh=step, z=6, tag=f"L{i}", upper=True, extra="letter-spacing:-.02em;"))
    L = [(xs[i], y0 + i * step, int(ws[i])) for i in range(4)]
    print("lines", L)
    titles = {"mirror": "People in the Mirror", "dyn": "Dynamics", "barks": "He Barks I Heal", "opin": "Voicing One's Opinions", "city": "Letter to My City",
              "tea": "Cup of Tea", "syn": "Syntax Error", "judge": "Before You Judge Read This", "emp": "Art of Empathy", "peb": "Pebbles and Peaks",
              "nost": "The Art of Nostalgia and Heartbreak", "x": ""}
    ybot = y0 + 4 * step
    spots = [("mirror", 64, y0 - 74, -3), ("dyn", 346, y0 - 80, 2), ("barks", 540, y0 - 70, -2), ("syn", 800, y0 - 76, 3),
             ("opin", 620, y0 + step * 2 + 34, 3), ("tea", 740, y0 + step * 2 + 100, -2),
             ("city", 530, y0 + step * 3 + 22, -3), ("emp", 700, y0 + step * 3 + 86, 2),
             ("judge", 64, ybot + 34, -1.5), ("peb", 64, ybot + 104, 2), ("nost", 330, ybot + 136, -1.5)]
    for k, x, y, r in spots:
        P.append(chip(x, y, titles[k], r))
    P.append(doodle("lightning", 915, y0 + step * 1 + 10, 90, LEM, 8, 16))
    P.append(doodle("star", 36, ybot - 20, 60, PINK, -10, 16))
    P.append(t("we published it. by students aged 14 to 19.", 64, ybot + 230, 30, color=INK, font="e", weight=600, w=900, lh=38, z=8, tag="cap1"))
    P.append(t("every title on this poster is a real post on our own site.", 64, ybot + 270, 24, color=INK, font="e", weight=400, w=900, lh=32, z=8, tag="cap2"))
    P.append(K.url_pill(y=1188))
    return K.render("blogs_1", K.page("".join(P)), H)

# ------------------------------------------------------------------------------------------------ blogs_2
def diecut(path, w, h, fx=.5, fy=.5, border=16, r=34):
    """A real cover with a thick white die-cut border (rounded-rect cut with a ragged bite taken out of one corner)."""
    from PIL import ImageDraw, ImageFilter
    S = 2
    im = cover(path, w, h, fx=fx, fy=fy, s=S).convert("RGBA")
    mask = Image.new("L", im.size, 0); d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=r * S, fill=255)
    im.putalpha(mask)
    bw, bh = im.width + 2 * border * S, im.height + 2 * border * S
    out = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d2 = ImageDraw.Draw(out)
    d2.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=(r + border) * S, fill=(10, 10, 10, 255))
    inner = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d3 = ImageDraw.Draw(inner)
    d3.rounded_rectangle([5 * S, 5 * S, bw - 1 - 5 * S, bh - 1 - 5 * S], radius=(r + border - 5) * S, fill=(255, 255, 255, 255))
    out.alpha_composite(inner); out.alpha_composite(im, (border * S, border * S))
    return out

def blogs_2():
    H = 1350
    P = [box(0, 0, W, H, f"background:{CREAM};", z=0)]
    P.append(K.logo(64, 40)); P.append(K.series_tab(50)); P.append(K.lane_chip("blogs", y=108))
    P.append(box(64, 172, 952, 3, f"background:{INK};", z=3))
    P.append(box(64, 1292, 952, 3, f"background:{INK};", z=3))
    P.append(t("04.", 64, 190, 18, color=INK, font="m", weight=700, tag="mast1"))
    P.append(t("STUDENT COVERS, STUDENT WORDS", 330, 190, 18, color=INK, font="m", weight=700, tag="mast2", ls=.04))
    sz = 140; step = 142
    y1 = 224
    ST = dict(font="d", weight=900, upper=True, z=6)
    ex = "letter-spacing:-.02em;"
    P.append(t("HOW A", 64, y1, sz, lh=step, tag="L1", extra=ex, **ST))
    # marker line
    y2 = y1 + step
    w2 = mw([dict(text="LETTER", font="d", size=sz, weight=900)])[0]
    P.append(f'<div style="position:absolute;left:40px;top:{y2+10}px;width:{int(w2)+60}px;height:{round(sz*.92)}px;background:{LEM};border:4px solid {INK};border-radius:12px;transform:rotate(-3deg);z-index:5"></div>')
    P.append(t("LETTER", 70, y2, sz, lh=step, tag="L2", extra=ex + "transform:rotate(-3deg);transform-origin:left center;", **ST))
    y3 = y2 + step + 6
    P.append(t("TO MY CITY", 64, y3, sz, lh=step, tag="L3", extra=ex, **ST))
    y4 = y3 + step
    P.append(t("BECAME A", 64, y4, sz, lh=step, tag="L4", extra=ex, **ST))
    y5 = y4 + step + 8
    wb = mw([dict(text="BLOG", font="d", size=sz, weight=900)])[0]
    ph_ = round(sz * .98); pillw = int(wb) + 32 + 108
    P.append(f'<div style="position:absolute;left:44px;top:{y5+6}px;width:{pillw}px;height:{ph_}px;background:{GRAPE};border:4px solid {INK};border-radius:999px;z-index:5"></div>')
    P.append(t("BLOG", 76, y5, sz, lh=step, tag="L5a", extra=ex, **ST))
    ax = 44 + pillw - 88
    P.append(f'<div style="position:absolute;left:{ax}px;top:{y5+6+ph_//2-36}px;width:72px;height:72px;border-radius:50%;background:{INK};z-index:6;display:flex;align-items:center;justify-content:center;color:{CREAM};font-family:var(--e);font-weight:700;font-size:42px">&#8594;</div>')
    P.append(t("POST", 44 + pillw + 12, y5, sz, lh=step, tag="L5b", extra=ex, **ST))
    print("lines y", y1, y2, y3, y4, y5, "bottom", y5 + ph_, "widths", int(w2), int(wb), pillw)
    # real student cover, die-cut, draped across the seam between line 1 and the marker line
    dc = diecut(K.PH["blog_city"], 180, 262, fx=.5, fy=.3)
    cw, ch = 180 + 32, 262 + 32
    P.append(f'<img src="{uri(dc, "PNG")}" style="position:absolute;left:790px;top:205px;width:{cw}px;height:{ch}px;transform:rotate(7deg);z-index:7;filter:drop-shadow(8px 8px 0 {INK})">')
    P.append(t("published on our own site, under the writer's name, with a cover by a student.", 64, 1060, 26, font="e", weight=500, w=700, lh=32, z=8, tag="cap"))
    P.append(doodle("squiggle", 800, 1060, 90, GRAPE, 0, 9))
    P.append(doodle("sparkle", 650, 232, 54, INK, 0, 9))
    P.append(doodle("sparkle", 880, 990, 60, INK, 0, 9))
    P.append(doodle("star", 900, 700, 56, INK, 12, 9))
    P.append(K.url_pill(y=1188))
    return K.render("blogs_2", K.page("".join(P)), H)

# ------------------------------------------------------------------------------------------------ hr_2
def phone(x, y, w, h, screen_inner, z=6):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{INK};border-radius:46px;z-index:{z};box-shadow:8px 8px 0 rgba(10,10,10,.35)">'
            f'<div style="position:absolute;left:12px;top:12px;right:12px;bottom:12px;border-radius:36px;overflow:hidden;background:#F1EEE4">{screen_inner}'
            f'<div style="position:absolute;left:0;top:0;right:0;height:42px;background:#F1EEE4;z-index:5"></div>'
            f'<div style="position:absolute;left:24px;top:11px;font-family:var(--e);font-weight:700;font-size:15px;color:{INK};z-index:6">9:41</div>'
            f'<div style="position:absolute;left:50%;top:9px;width:84px;height:24px;margin-left:-42px;border-radius:14px;background:{INK};z-index:6"></div>'
            f'<div style="position:absolute;left:50%;bottom:9px;width:100px;height:5px;margin-left:-50px;border-radius:3px;background:{INK};z-index:6"></div>'
            f'</div></div>')

def sticky(x, y, text, rot=-4, z=14):
    return (f'<div class="measure" data-tag="sticky" style="position:absolute;left:{x}px;top:{y}px;width:176px;height:132px;background:{LEM};border:3px solid {INK};box-shadow:5px 5px 0 {INK};transform:rotate({rot}deg);z-index:{z};padding:22px 14px 8px;box-sizing:border-box">'
            f'<div style="position:absolute;left:50%;top:-14px;width:54px;height:24px;margin-left:-27px;background:rgba(244,239,224,.85);border:2px solid {INK};box-sizing:border-box;transform:rotate(-3deg)"></div>'
            f'<div style="font-family:var(--e);font-weight:700;font-size:22px;line-height:26px;color:{INK}">{text}</div></div>')

def hr_2():
    H = 1350
    P = [box(0, 0, W, H, f"background:{CREAM};", z=0)]
    P.append(K.logo(64, 48)); P.append(K.series_tab(58)); P.append(K.lane_chip("hr", y=116))
    P.append(t("SCREEN TIME,", 64, 190, 112, font="d", weight=900, lh=96, z=6, tag="h1", upper=True, extra="letter-spacing:-.02em;"))
    P.append(t("justified.", 74, 292, 128, font="s", italic=True, color=TEAL if False else INK, lh=120, z=6, tag="h2"))
    pw, ph = 296, 610; gap = 32; py = 420
    xs = [64 + i * (pw + gap) for i in range(3)]
    sw, sh = pw - 24, ph - 24
    # screen 1: the team's real slide
    s1 = img(uri(cover(K.social_slide(13), sw, int(sw * 1.7), fx=.5, fy=0)), 0, 44, sw, int(sw * 1.7), z=2, extra="object-fit:cover;")
    # screen 2: a real blog cover (9:16)
    s2 = img(uri(cover(K.PH["blog_dynamics"], sw, sh, fx=.5, fy=.5)), 0, 0, sw, sh, z=1)
    # screen 3: a real drive photo
    s3 = img(uri(cover(K.PH["dog_bhowanipur"], sw, sh, fx=.5, fy=.5)), 0, 0, sw, sh, z=1)
    for x, sc in zip(xs, (s1, s2, s3)): P.append(phone(x, py, pw, ph, sc))
    notes = ["a weekly roundup.", "a student's essay.", "a dog drive."]
    for x, n in zip(xs, notes): P.append(sticky(x + 40, py + ph - 70, n))
    P.append(t("what shows up for 1,400+ students aged 14 to 19 in community AQ.", 64, 1120, 28, font="e", weight=600, w=900, lh=36, z=8, tag="cap"))
    P.append(K.url_pill(y=1196, w=952))
    return K.render("hr_2", K.page("".join(P)), H)

if __name__ == "__main__":
    which = sys.argv[1:] or ["social_1", "social_2", "blogs_1", "blogs_2", "hr_2"]
    for n in which: globals()[n]()
