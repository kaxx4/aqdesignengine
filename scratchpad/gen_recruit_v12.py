"""AQ recruitment v12: the full campaign arc.

Owner (2026-11-13): the chat-bubble single poster is not weighty enough on its own. Build the whole campaign:
  A  formal carousel  (feed, 11 slides): every opportunity at AQ, one department per slide, plain and clear
  B  informal carousel (feed, 11 slides): the same opportunities as group-chat invitations
  C  "why join" stories (5): the convincing set
  D  narrative stories (6): one chat thread that unfolds one bubble per frame (the magazine, which the owner liked)
  E  standalone story posters: the v11 set, rendered as stories (out/recruit_nov2026/v11/*_story)
  F  WhatsApp posters (square, 3)
Rules: no stats-as-brag, no pay, no named open seats, no process talk, no 'student' in headlines, no member names,
no Bengali. Chat lines are SCRIPTED. Facts used only where descriptive and true (departments, what each does).
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_recruit_v9 as V9
import gen_recruit_v10 as V10
core = K.core
W = 1080; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/recruit_nov2026/v12"
PH = K.PH
cover, mono, uri, img, box = K.cover, K.mono, K.uri, K.img, K.box
bub = V10.bub
LINK = "ngoaquaterra.com/recruitment"

async def done(name, P, H, bg=CREAM, grain=.35):
    html = K.page(V6.DEFS + "".join(P) + V6.grain(grain), H, bg=bg)
    await K._render(name, html, H, None, None)
    print("rendered", name)

def t(txt, x, y, size, color=INK, font="e", weight=600, w=None, lh=None, italic=False, z=50, extra="", upper=False):
    return K.t(txt, x, y, size, color=color, font=font, weight=weight, w=w, lh=lh or round(size * 1.15), z=z, extra=(("font-style:italic;" if italic else "") + extra), upper=upper)

def url(x, y, z=80, bg="#F6EFD8"):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.04em;color:#0A0A0A;'
            f'background:{bg};padding:6px 12px;z-index:{z}">{LINK}</div>')

def pager(i, n, x=W - 64, y=58, color=INK):
    return (f'<div style="position:absolute;right:{W-x}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.08em;color:{color};z-index:80">'
            f'{i:02d} / {n:02d}</div>')

def framed(path, x, y, w, h, rot=0, z=10, fy=.45, bw=False, r=26):
    im = cover(path, w, h, fy=fy)
    if bw: im = mono(im, 1.1)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);border:4px solid #0A0A0A;border-radius:{r}px;'
            f'overflow:hidden;box-shadow:9px 10px 0 #0A0A0A;z-index:{z}"><img src="{uri(im)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')

# =========================================================================== A. FORMAL CAROUSEL
DEPTS = [
    ("Events", SKY, PH["dd_floor_green"], "Plan and run AQ's fundraising events, from Disco Diwali to TerraThon.",
     ["work with vendors and sponsors", "decor, lights, the run sheet", "be there on the night"]),
    ("Welfare", MINT, PH["dog_bhowanipur"], "Drives across Kolkata: feeding strays, food and sharbat, clothes and books, plantations.",
     ["plan a drive", "show up with the team", "keep the drive going round after round"]),
    ("Teaching", MINT, PH["teach_abc"], "Teaching internships and worksheets for children at partner centres. Part of Welfare.",
     ["run a workshop", "write the worksheet", "come back the next week"]),
    ("Crftd", TOM, PH["tee_novus"], "AQ's streetwear label. Designed, sprayed and sold by members. Profit funds welfare drives.",
     ["design the drop", "run the stall at school fests", "sell what you made"]),
    ("ShikshAQ", LEM, None, "A tutor search for Kolkata, built and run inside AQ. shikshaq.in",
     ["reach out to tutors", "help families find one", "work on the platform"]),
    ("Social Media", GRAPE, K.social_slide(9), "Reels, design, Instagram and LinkedIn. The account you are reading this on.",
     ["edit the reel", "design the post", "write the caption"]),
    ("The Magazine", GRAPE, PH["blog_city"], "AQ's digital magazine. Essays, art and stories, written and designed by members.",
     ["write a piece", "edit someone else's", "design the cover"]),
    ("Collabs", PINK, PH["emami"], "Joint projects with schools, colleges and NGOs across Kolkata.",
     ["find the partner", "write the email", "run the project together"]),
    ("HR", TEAL, PH["dd_group"], "Bring new people in and keep the community running.",
     ["welcome new members", "run the community", "know everyone"]),
]

async def formal_cover():
    P = [box(0, 0, W, 1350, f"background:{CREAM};", z=0), K.logo(64, 48), pager(1, 11)]
    P.append(framed(PH["dd_floor_green"], 560, 640, 420, 520, 4, z=10))
    P.append(framed(PH["teach_abc"], 120, 700, 380, 470, -5, z=11))
    P.append(framed(PH["tee_novus"], 420, 860, 300, 380, 2, z=12))
    P.append(t("Everything you<br>can do at <i>AquaTerra.</i>", 64, 170, 112, font="s", weight=400, w=960, lh=108))
    P.append(t("eight departments. swipe through.", 64, 440, 30, color="#5A5A55", font="e", weight=400))
    P.append(V6.tape(220, 680, 140, 44, -8, seed=2, z=20)); P.append(V6.tape(700, 620, 140, 44, 6, seed=4, z=20))
    await done("a01_formal_cover", P, 1350)

async def formal_slide(i, d):
    name, col, ph, desc, tasks = d
    fg = core.text_on(col)
    P = [box(0, 0, W, 1350, f"background:{CREAM};", z=0), K.logo(64, 48), pager(i, 11)]
    P.append(box(0, 140, W, 560, f"background:{col};", z=1))
    if ph:
        P.append(framed(ph, 64, 180, 952, 480, -1.2, z=10))
    else:
        P.append(t("shikshaq.in", 64, 330, 150, font="s", weight=400, italic=True, z=10))
    P.append(t(name, 64, 740, 96, font="s", weight=400, w=952, lh=100))
    P.append(t(desc, 64, 860, 32, color=INK, font="e", weight=400, w=900, lh=42))
    P.append(t("you could", 64, 1010, 18, color="#5A5A55", font="m", weight=700, upper=True, extra="letter-spacing:.1em;"))
    for k, task in enumerate(tasks):
        P.append(f'<div style="position:absolute;left:64px;top:{1046+k*58}px;display:flex;align-items:center;gap:16px;z-index:50">'
                 f'<div style="width:22px;height:22px;border-radius:50%;background:{col};border:3px solid #0A0A0A"></div>'
                 f'<div style="font-family:var(--e);font-weight:600;font-size:32px;color:#0A0A0A">{task}</div></div>')
    await done(f"a{i:02d}_formal_{name.split()[0].lower()}", P, 1350)

async def formal_close():
    P = [box(0, 0, W, 1350, f"background:{INK};", z=0), K.logo_pill(64, 44, dark=True), pager(11, 11, color="#F6EFD8")]
    y = 300
    for k, (name, col, *_r) in enumerate(DEPTS):
        P.append(f'<div style="position:absolute;left:{64 + (k%2)*40}px;top:{y + k*70}px;font-family:var(--s);font-size:58px;line-height:64px;color:{col};z-index:20">{name}</div>')
    P.append(t("Pick one. Or three.", 64, 980, 84, color="#F6EFD8", font="s", weight=400, italic=True))
    P.append(t("Applications are open.", 64, 1100, 32, color="#F6EFD8", font="e", weight=400))
    P.append(url(64, 1170))
    await done("a11_formal_close", P, 1350, bg=INK)

# =========================================================================== B. INFORMAL CAROUSEL
def chat_slide(photo, lines, wcol, fy=.45, H=1350, top=0, bot=0, cover_txt=None):
    """photo in B&W with one colour window; bubbles stacked with alternating sides."""
    P = V9.bg_cast(photo, H, fy=fy, wins=[(380, int(H*.12)+top, 560, int(H*.36), wcol, "", "tl")])
    P = [p for p in P if "line-height:26px" not in p]
    P.append(V9.scrim(H, .15, .55))
    y = int(H*.50) + (top if top else 0)
    cols = ["#FFFFFF", wcol, "#FFFFFF", LEM, "#FFFFFF"]
    for k, (txt, big) in enumerate(lines):
        side = "L" if k % 2 == 0 else "R"
        size = 64 if big else 42
        x = 64 if side == "L" else None
        est = min(840, int(len(txt.replace("<br>", "")) * size * .52) + 70)
        if side == "R": x = W - 64 - est
        rot = [-2, 2.5, -1.5, 2, -2.5][k % 5]
        c = LEM if big else cols[k % len(cols)]
        P.append(bub(txt, x, y, c, side, size, rot, maxw=860))
        y += int(size * 1.2 * (txt.count("<br>") + 1)) + 74
    return P

INFORMAL = [
    ("dd_group", .6, PINK, [("ok so what does everyone<br>actually do at aq", False), ("depends. what do you like?", False), ("swipe", True)]),
    ("dd_blue", .5, SKY, [("we need someone on decor", False), ("and someone to talk<br>to the dhol guy", False), ("you in?", True)]),
    ("dog_bhowanipur", .5, MINT, [("feeding the dogs on sunday", False), ("i'll bring biscuits", False), ("come. they sniff<br>new people first", True)]),
    ("teach_abc", .35, TOM, [("we need one more<br>person on saturday", False), ("i can't teach", False), ("neither could we.<br>you'll be fine.", True)]),
    ("tee_novus", .3, TOM, [("spraying t-shirts at<br>the next school fest", False), ("wear something old", False), ("want a can?", True)]),
    ("blog_city", .5, GRAPE, [("we should start<br>a magazine", False), ("who's writing", False), ("everyone, apparently.", True)]),
    ("five_group", .5, GRAPE, [("who's editing the reel", False), ("i've only ever made memes", False), ("perfect.", True)]),
    ("emami", .5, PINK, [("a school wants to do<br>a drive with us", False), ("who's emailing them", False), ("me. what do i say?", True)]),
    ("art_table", .5, LEM, [("my cousin needs a tutor", False), ("send her shikshaq.in", False), ("wait, we run that?", True)]),
    ("desk", .4, TEAL, [("new people joined today", False), ("who's saying hi", False), ("me. i was new<br>last month.", True)]),
]

async def informal(i, spec):
    key, fy, col, lines = spec
    P = chat_slide(PH[key], lines, col, fy=fy)
    P += [K.logo_pill(64, 44, dark=True), pager(i, 11, color="#F6EFD8")]
    await done(f"b{i:02d}_chat_{key}", P, 1350)

async def informal_close():
    H = 1350
    P = V9.bg_cast(PH["dd_group"], H, fy=.6, wins=[(40, int(H*.22), 300, int(H*.26), PINK, "", "tl"), (390, int(H*.17), 300, int(H*.28), SKY, "", "tr"), (730, int(H*.21), 320, int(H*.27), LEM, "", "tl")])
    P = [p for p in P if "line-height:26px" not in p] + [V9.scrim(H, 0, .5)]
    cur = '<span style="display:inline-block;width:8px;height:84px;background:#0A0A0A;margin-left:10px;vertical-align:-14px"></span>'
    P += [bub(f"we should totally{cur}", 64, int(H*.58), "#FFFFFF", "L", 96, -2, maxw=980, pad=(30, 44)),
          t("finish the sentence.", 84, int(H*.58) + 190, 56, color="#FFFFFF", font="s", weight=400, italic=True, extra="text-shadow:0 2px 14px rgba(0,0,0,.6);"),
          K.logo_pill(64, 44, dark=True), pager(11, 11, color="#F6EFD8"), url(64, H - 86)]
    await done("b11_chat_close", P, H)

# =========================================================================== C. WHY-JOIN STORIES
WHY = [
    ("No experience needed.", "most people here hadn't done any of this before.", PH["teach_abc"], MINT, .35),
    ("The real thing, not practice.", "the party happens. the dogs eat. the magazine goes out.", PH["dd_floor_green"], SKY, .4),
    ("Pick anything. Switch anytime.", "events one month, teaching the next. plenty of people do both.", PH["tee_novus"], TOM, .3),
    ("People from other schools.", "from all over kolkata. you'll know more of them than you'd expect.", PH["five_group"], PINK, .5),
    ("Come once. Decide after.", "applications are open.", PH["dd_group"], LEM, .6),
]

async def why(i, spec):
    head, sub, ph, col, fy = spec
    H = 1920
    m = mono(cover(ph, W, H, fy=fy), 1.12)
    P = [img(uri(m), 0, 0, W, H, z=1), box(0, 0, W, H, f"background:{col};mix-blend-mode:multiply;opacity:.55;", z=2),
         box(0, 0, W, H, "background:linear-gradient(180deg,rgba(10,10,10,.1) 30%,rgba(10,10,10,.7));", z=3)]
    P.append(f'<div style="position:absolute;left:64px;top:240px;font-family:var(--m);font-weight:700;font-size:22px;letter-spacing:.1em;color:#F6EFD8;z-index:40">WHY AQ · {i} / 5</div>')
    link = (f'<div style="margin-top:28px;align-self:flex-start;font-family:var(--m);font-weight:700;font-size:22px;color:#0A0A0A;background:#F6EFD8;padding:8px 14px">{LINK}</div>' if i == 5 else "")
    P.append(f'<div style="position:absolute;left:64px;bottom:300px;width:952px;display:flex;flex-direction:column;gap:30px;z-index:50">'
             f'<div style="font-family:var(--d);font-weight:900;font-size:116px;line-height:112px;color:#F6EFD8;text-transform:uppercase;text-shadow:0 4px 30px rgba(0,0,0,.5)">{head}</div>'
             f'<div style="font-family:var(--e);font-size:38px;line-height:50px;color:#F6EFD8;max-width:860px">{sub}</div>{link}</div>')
    P.append(K.logo_pill(64, 214 - 120, dark=True))
    await done(f"c{i}_why", P, H)

# =========================================================================== D. NARRATIVE STORY (one thread, unfolding)
THREAD = [("we should start a magazine", "L", "#FFFFFF", 52), ("who's writing", "R", GRAPE, 44), ("i've never written anything", "L", "#FFFFFF", 44),
          ("neither had we", "R", MINT, 44), ("it's out.", "L", LEM, 84), ("the next issue needs people", "R", "#FFFFFF", 44)]

async def narrative(k):
    H = 1920
    covers = [PH["blog_mirror"], PH["blog_dynamics"], PH["blog_city"], PH["blog_tea"], PH["blog_syntax"], PH["blog_pebbles"]]
    P = [box(0, 0, W, H, f"background:{GRAPE};", z=0)]
    spots = [(-40, 60, -8), (380, 20, 5), (720, 110, -4), (40, 640, 6), (430, 580, -6), (760, 700, 4), (-20, 1240, -5), (380, 1180, 4), (720, 1290, -3)]
    allc = covers + [PH["blog_opinions"], PH["blog_judge"], PH["blog_empathy"]]
    for j, (pth, (x, y0, r)) in enumerate(zip(allc, spots)):
        P.append(f'<div style="position:absolute;left:{x}px;top:{y0}px;width:404px;height:544px;transform:rotate({r}deg);background:#FBF8EE;padding:12px;box-shadow:8px 9px 0 rgba(10,10,10,.85);z-index:{2+j}">'
                 f'<img src="{uri(cover(pth, 380, 520))}" style="width:380px;height:520px;object-fit:cover;display:block"></div>')
        P.append(V6.tape(x + 140, y0 - 16, 120, 40, r * 2, seed=60 + j, z=20))
    P.append(box(0, 0, W, H, "background:rgba(10,10,10,.42);", z=25))
    y = 560
    for j, (txt, side, col, size) in enumerate(THREAD[:k]):
        est = min(860, int(len(txt) * size * .52) + 70)
        x = 64 if side == "L" else W - 64 - est
        P.append(bub(txt, x, y, col, side, size, [-2, 2, -1.5, 2.5, -2, 1.5][j], maxw=880))
        y += int(size * 1.2) + 100
    if k == len(THREAD): P.append(url(64, 1600))
    P.append(K.logo_pill(64, 214 - 120, dark=True))
    P.append(f'<div style="position:absolute;right:64px;top:110px;font-family:var(--m);font-weight:700;font-size:20px;color:#F6EFD8;z-index:80">{k} / {len(THREAD)}</div>')
    await done(f"d{k}_thread", P, H)

# =========================================================================== F. WHATSAPP POSTERS (square)
async def wa():
    H = 1080
    # 1 the forward
    P = V9.bg_cast(PH["dd_group"], H, fy=.6, wins=[])
    P += [V9.scrim(H, .1, .55), bub("send this to the friend<br>who'd actually show up", 64, 560, "#FFFFFF", "L", 58, -2, maxw=960),
          K.logo_pill(64, 44, dark=True), url(64, H - 86)]
    await done("f1_wa_forward", P, H)
    # 2 the decor ask
    P = V9.bg_duo(PH["dd_blue"], H, "PARTY", GRAPE, PINK)
    P += [bub("we need someone<br>on decor", 50, 300, "#FFFFFF", "L", 80, -4, maxw=960, pad=(26, 40)), bub("you in?", 600, 620, LEM, "R", 76, 3),
          K.logo_pill(64, 44, dark=True), url(64, H - 86)]
    await done("f2_wa_decor", P, H)
    # 3 finish the sentence
    P = [box(0, 0, W, H, f"background:{LEM};", z=0), V6.blob_svg(560, 520, 620, PINK, seed=6, sw=6, z=1, rot=-8)]
    cur = '<span style="display:inline-block;width:8px;height:84px;background:#0A0A0A;margin-left:10px;vertical-align:-14px"></span>'
    P += [bub(f"we should totally{cur}", 64, 360, "#FFFFFF", "L", 96, -2, maxw=980, pad=(30, 44)),
          t("finish the sentence.", 84, 560, 56, font="s", weight=400, italic=True, z=70), K.logo_pill(64, 44, dark=True), url(64, H - 86)]
    await done("f3_wa_finish", P, H)

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    async with K.B.session():
        only = set(sys.argv[1:])
        if not only or "a" in only:
            await formal_cover()
            for i, d in enumerate(DEPTS): await formal_slide(i + 2, d)
            await formal_close()
        if not only or "b" in only:
            for i, s in enumerate(INFORMAL): await informal(i + 1, s)
            await informal_close()
        if only and "c" not in only and "d" not in only and "f" not in only: return
        for i, s in enumerate(WHY): await why(i + 1, s)
        for k in range(1, len(THREAD) + 1): await narrative(k)
        await wa()

if __name__ == "__main__":
    asyncio.run(main())
