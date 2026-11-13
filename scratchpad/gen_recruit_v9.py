"""AQ recruitment v9 (window tabs SAID IT / DID IT / BROUGHT A FRIEND / ALSO THE DOGS are scripted jokes): "we should totally..." The group chat where the plan actually happens.

Owner (2026-11-13): likes the texting format; recreate the chat bubbles left and right in colour as the TOPMOST layer;
the background is a Pinterest-style graphic poster (the v2 recreation look, which the owner rated closest).
Hierarchy: 1 chat thread, 2 the graphic poster behind it, 3 minimal chrome (small logo pill, the link as the last bubble).
No repeated ad chrome (lane chips, fact tapes, url pills) any more.

CHAT LINES ARE SCRIPTED by us, not quotes from real AQ chats. The outcome bubbles are real facts:
round 53 (Tails and Treats), 550 registrations (Disco Diwali 2.0), 300 walk-ins at Novus (Crftd stall), every Sunday for
2.5 years (Pather Sathi Sunday school), the blog is live. No member names, no pay, no process, no 'student' in headlines.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
from PIL import Image, ImageEnhance
core = K.core
W = 1080; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/recruit_nov2026/v9"
PH = K.PH
cover, mono, posterise, dither, uri, img = K.cover, K.mono, K.posterise, K.dither, K.uri, K.img

# ----------------------------------------------------------------- the chat layer (top of the hierarchy)
def bubble(text, side, col, fg=None, size=40, maxw=700, extra=""):
    fg = fg or core.text_on(col)
    r = "38px 38px 38px 10px" if side == "L" else "38px 38px 10px 38px"
    al = "flex-start" if side == "L" else "flex-end"
    return (f'<div style="display:flex;justify-content:{al};width:100%">'
            f'<div style="max-width:{maxw}px;background:{col};color:{fg};border:4px solid #0A0A0A;border-radius:{r};box-shadow:7px 8px 0 #0A0A0A;'
            f'padding:20px 30px 22px;font-family:var(--e);font-weight:600;font-size:{size}px;line-height:{round(size*1.22)}px;{extra}">{text}</div></div>')

def typing(col="#FFFFFF"):
    dots = "".join(f'<span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:#0A0A0A;margin:0 5px;opacity:{o}"></span>' for o in (1, .6, .3))
    return (f'<div style="display:flex;justify-content:flex-start;width:100%"><div style="background:{col};border:4px solid #0A0A0A;border-radius:38px 38px 38px 10px;'
            f'box-shadow:7px 8px 0 #0A0A0A;padding:22px 30px">{dots}</div></div>')

def seen(txt="seen"):
    return (f'<div style="display:flex;justify-content:flex-end;width:100%;margin-top:-6px"><div style="font-family:var(--m);font-weight:700;font-size:17px;'
            f'color:#0A0A0A;background:#F6EFD8;padding:3px 10px;border:2px solid #0A0A0A">{txt}</div></div>')

def thread(items, x, y, w, gap=22, z=60):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;display:flex;flex-direction:column;gap:{gap}px;z-index:{z}">'
            + "".join(items) + "</div>")

def thread_bottom(items, x, bottom, w, gap=22, z=60):
    return (f'<div style="position:absolute;left:{x}px;bottom:{bottom}px;width:{w}px;display:flex;flex-direction:column;gap:{gap}px;z-index:{z}">'
            + "".join(items) + "</div>")

def header(title, x=64, y=40, w=952, dark=False):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:92px;background:#F6EFD8;border:4px solid #0A0A0A;border-radius:26px;box-shadow:6px 7px 0 #0A0A0A;'
            f'z-index:70;display:flex;align-items:center;gap:18px;padding:0 24px">'
            f'<img src="{core.LOGO}" style="height:30px">'
            f'<div style="width:3px;height:44px;background:#0A0A0A"></div>'
            f'<div style="font-family:var(--e);font-weight:600;font-size:30px;color:#0A0A0A">{title}</div></div>')

LINK = "ngoaquaterra.com/recruitment"
def link_bubble(col=LEM):
    return bubble(f'<span style="font-family:var(--m);font-weight:700;font-size:28px;text-decoration:underline">{LINK}</span>', "R", col)

# ----------------------------------------------------------------- backgrounds (Pinterest graphic posters, v2 language)
def bg_cast(photo, H, fy=.4, wins=()):
    """B&W photo + colour windows with tabs (the cast-list reference)."""
    m = mono(cover(photo, W, H, fy=fy), contrast=1.1)
    P = [img(uri(m), 0, 0, W, H, z=1)]
    for (x, y, w, h, c, lab, side) in wins:
        P.append(V6.window(x, y, w, h, c, lab, side, z=6))
    return P

def bg_duo(photo, H, word, c1=GRAPE, c2=PINK, fy=.5):
    """duotone photo with a giant outline word bleeding off the edges."""
    g = mono(cover(photo, W, H, fy=fy), contrast=1.2)
    P = [K.box(0, 0, W, H, f"background:{c2};", z=0), img(uri(g), 0, 0, W, H, z=1, extra="mix-blend-mode:multiply;opacity:.9"),
         K.box(0, 0, W, H, f"background:{c1};mix-blend-mode:screen;opacity:.55;", z=2)]
    P.append(f'<div style="position:absolute;left:-60px;top:{int(H*.08)}px;white-space:nowrap;font-family:var(--d);font-weight:900;font-size:430px;line-height:380px;'
             f'color:transparent;-webkit-text-stroke:5px #F6EFD8;text-transform:uppercase;z-index:4;letter-spacing:-.02em">{word}</div>')
    return P

def bg_poster(photo, H, pal, fy=.35):
    pz = posterise(cover(photo, W, H, fy=fy), pal, blur=5)
    return [img(uri(pz, "PNG"), 0, 0, W, H, z=1), V6.halftone_over(W, H, 3, .1)]

def bg_tiles(photos, H, cols):
    """dithered photo tiles alternating with flat colour blocks (the website-page reference)."""
    P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0)]
    n = 3; tw = W // n; th = H // 4
    k = 0
    for r in range(4):
        for c in range(n):
            x, y = c * tw, r * th
            if (r + c) % 2 == 0:
                ph = photos[k % len(photos)]; k += 1
                im = dither(cover(ph, tw, th, fy=.4, s=1.4), cols[(r + c) % len(cols)], cell=5)
                P.append(img(uri(im, "PNG"), x, y, tw, th, z=1))
            else:
                P.append(K.box(x, y, tw, th, f"background:{cols[(r * 3 + c) % len(cols)]};", z=1))
    return P

def bg_taped(covers, H, base=GRAPE):
    P = [K.box(0, 0, W, H, f"background:{base};", z=0)]
    spots = [(-40, 60, -8), (380, 20, 5), (720, 110, -4), (40, 620, 6), (430, 560, -6), (760, 680, 4)]
    for i, (path, (x, y, r)) in enumerate(zip(covers, spots)):
        cw, ch = 380, 520
        P.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{cw+24}px;height:{ch+24}px;transform:rotate({r}deg);background:#FBF8EE;padding:12px;'
                 f'box-shadow:8px 9px 0 rgba(10,10,10,.85);z-index:{2+i}"><img src="{uri(cover(path, cw, ch))}" style="width:{cw}px;height:{ch}px;object-fit:cover;display:block"></div>')
        P.append(V6.tape(x + 130, y - 16, 120, 40, r * 2, seed=60 + i, z=20))
    return P

def scrim(H, a=.0, b=.55):
    return K.box(0, 0, W, H, f"background:linear-gradient(180deg,rgba(10,10,10,{a}) 0%,rgba(10,10,10,0) 35%,rgba(10,10,10,{b}) 100%);", z=30)

async def done(name, P, H):
    html = K.page(V6.DEFS + "".join(P) + V6.grain(.4), H, bg=CREAM)
    await K._render(name, html, H, None, None)
    print("rendered", name)

def geo(story):
    H = 1920 if story else 1350
    return H, (200 if story else 0), (250 if story else 0)

# ----------------------------------------------------------------- the pieces
async def dogs(story=False):
    H, top, bot = geo(story)
    P = bg_cast(PH["dog_bhowanipur"], H, fy=.5, wins=[(290, int(H*.53), 270, int(H*.30), MINT, "THE DOGS", "tl"), (575, int(H*.53), 330, int(H*.30), LEM, "ALSO THE DOGS", "tr")])
    P += [header("the group chat", y=40 + top)]
    P.append(thread([bubble("we should totally feed the dogs near school", "L", "#FFFFFF"),
                     bubble("i'll bring biscuits", "R", MINT),
                     bubble("round 53.", "L", LEM, size=64)], 64, 170 + top, 952))
    P.append(thread_bottom([link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e1_dogs" + ("_story" if story else ""), P, H)

async def party(story=False):
    H, top, bot = geo(story)
    P = bg_duo(PH["dd_blue"], H, "PARTY", GRAPE, PINK) + [scrim(H, 0, .45), header("the group chat", y=40 + top)]
    P.append(thread_bottom([bubble("what if we threw a party for charity", "L", "#FFFFFF"),
                            bubble("who's booking the dhol", "R", SKY),
                            bubble("me??", "L", "#FFFFFF"),
                            bubble("550 registrations.", "R", LEM, size=60),
                            link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e2_party" + ("_story" if story else ""), P, H)

async def tees(story=False):
    H, top, bot = geo(story)
    pal = ["#2a0f0a", "#7a1f12", "#c43a1e", "#ff4d2e", "#f6a07a", "#f6efd8"]
    P = bg_poster(PH["tee_novus"], H, pal, fy=.3) + [scrim(H, 0, .45), header("the group chat", y=40 + top)]
    P.append(thread_bottom([bubble("we should make our own t-shirts", "L", "#FFFFFF"),
                            bubble("and spray them at school fests", "R", TOM),
                            bubble("300 walk-ins at novus.", "L", LEM, size=60),
                            bubble("profit funds a welfare drive", "R", "#FFFFFF", size=34),
                            link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e3_tees" + ("_story" if story else ""), P, H)

async def teach(story=False):
    H, top, bot = geo(story)
    P = bg_tiles([PH["teach_abc"], PH["teach_class"], PH["art_table"], PH["holi"], PH["fable"], PH["green_talk"]], H, [MINT, SKY, LEM, PINK, TOM, GRAPE])
    P += [scrim(H, 0, .35), header("the group chat", y=40 + top)]
    P.append(thread_bottom([bubble("someone should teach those kids", "L", "#FFFFFF"),
                            bubble("sunday?", "R", MINT),
                            bubble("every sunday. 2.5 years now.", "L", LEM, size=54),
                            link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e4_teach" + ("_story" if story else ""), P, H)

async def blog(story=False):
    H, top, bot = geo(story)
    covers = [PH["blog_mirror"], PH["blog_dynamics"], PH["blog_city"], PH["blog_tea"], PH["blog_syntax"], PH["blog_pebbles"]]
    P = bg_taped(covers, H) + [scrim(H, 0, .5), header("the group chat", y=40 + top)]
    P.append(thread_bottom([bubble("we should start a blog", "L", "#FFFFFF"),
                            bubble("who's writing", "R", GRAPE),
                            bubble("everyone, apparently", "L", "#FFFFFF"),
                            bubble("it's live.", "R", LEM, size=64),
                            link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e5_blog" + ("_story" if story else ""), P, H)

async def closer(story=False):
    H, top, bot = geo(story)
    P = bg_cast(PH["dd_group"], H, fy=.6, wins=[(40, int(H*.22), 300, int(H*.26), PINK, "SAID IT", "tl"), (390, int(H*.17), 300, int(H*.28), SKY, "DID IT", "tr"), (730, int(H*.21), 320, int(H*.27), LEM, "BROUGHT A FRIEND", "tl")])
    P += [scrim(H, 0, .45), header("the group chat", y=40 + top)]
    P.append(thread_bottom([bubble("every group chat says \"we should totally\"", "L", "#FFFFFF"),
                            bubble("this one did.", "R", LEM, size=64),
                            typing(),
                            link_bubble("#F6EFD8")], 64, 64 + bot, 952))
    await done("e6_closer" + ("_story" if story else ""), P, H)

JOBS = {"dogs": dogs, "party": party, "tees": tees, "teach": teach, "blog": blog, "closer": closer}

async def main(only, stories):
    async with K.B.session():
        for k, fn in JOBS.items():
            if only and k not in only: continue
            await fn(False)
            if stories: await fn(True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    args = [a for a in sys.argv[1:] if a != "--feed"]
    asyncio.run(main(set(args) or None, "--feed" not in sys.argv))
