"""AQ Instagram content, v13: welfare-first campaigns for the page (owner, 2026-11-13).

Covers the 2025-2026 window (from April 2025; the date is not stated on the posts). Carousels:
  W  "The last two years, on the ground"   welfare recap (10)
  E  "What you'd actually be doing here"    opportunities, education first (12)
  S  ShikshAQ, free learning               (6)
  T  Tails and Treats, animal welfare       (6)
  H  highlight covers                       (6)
Facts: platform project log, 2025-04-01 to now: 158 projects, 79 places, 45 workshops, ~2,000 children in workshop
sessions (sum of logged counts), Pather Sathi ~32 sessions, Tails and Treats 25 rounds, Book Basket 15, Food For All 7,
Wear and Share 7, Sharbat Seva 6, Smile Notes 6, Grow Green 4. ShikshAQ free papers and study material: owner direction.
Never: 'verified', commission, research figures, pay, member names. Copy deck: brain/RECRUITMENT_COPY_DECK_V13.md.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
from PIL import ImageEnhance
core = K.core
W = 1080; H = 1350; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/aq_content_v13"
PH = dict(K.PH)
E = "edu/"
PH.update({k: E + v for k, v in {"sund1": "sund_1.png", "sund2": "sund_2.png", "sund3": "sund_3.png", "sund4": "sund_4.png", "stem1": "stem_1.jpg",
          "stem2": "stem_2.jpg", "stem3": "stem_3.jpg", "stem4": "stem_4.jpg", "chess1": "chess_1.jpg", "chess4": "chess_4.jpg", "chessm": "chess_m.jpg",
          "plant": "plant23.jpg", "rakhi": "rakhi.jpg", "draw": "powerspeak.jpg", "magic": "magic.jpg", "onceupon": "onceupon.jpg", "artnook": "artnook.jpg", "mult": "mult.jpg"}.items()})
LINK = "ngoaquaterra.com/recruitment"

def warm(path, w, h, fy=.45, fx=.5):
    im = K.cover(path, w, h, fy=fy, fx=fx)
    im = ImageEnhance.Color(im).enhance(1.08); im = ImageEnhance.Contrast(im).enhance(1.05)
    return K.uri(im)

def kick(txt, x, y, color=INK):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.12em;color:{color};'
            f'text-transform:uppercase;z-index:60">{txt}</div>')

def headline(txt, x, y, size, color=INK, w=952, z=60):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-family:var(--s);font-size:{size}px;line-height:{round(size*1.0)}px;'
            f'letter-spacing:-.01em;color:{color};z-index:{z}">{txt}</div>')

def body(txt, x, y, color=INK, w=900, size=31):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-family:var(--e);font-size:{size}px;line-height:{round(size*1.38)}px;color:{color};z-index:60">{txt}</div>')

def pager(i, n, color=INK):
    return f'<div style="position:absolute;right:64px;top:58px;font-family:var(--m);font-weight:700;font-size:18px;letter-spacing:.08em;color:{color};z-index:80">{i:02d} / {n:02d}</div>'

def logo(dark):
    return K.logo_pill(64, 44, dark=True) if dark else K.logo(64, 48)

def linkline(x, y, txt=LINK, bg="#F6EFD8"):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:var(--m);font-weight:700;font-size:22px;letter-spacing:.03em;color:#0A0A0A;'
            f'background:{bg};padding:8px 14px;z-index:80">{txt}</div>')

def chips(items, x, y, col, size=30, maxx=W - 64):
    out = []; cx, cy = x, y
    for it in items:
        w = int(len(it) * size * .62 + 52)
        if cx + w > maxx: cx, cy = x, cy + size + 44
        out.append(f'<div style="position:absolute;left:{cx}px;top:{cy}px;padding:8px 22px;border:3px solid #0A0A0A;border-radius:999px;background:{col};'
                   f'font-family:var(--e);font-weight:600;font-size:{size}px;color:{core.text_on(col)};z-index:60">{it}</div>')
        cx += w + 14
    return "".join(out)

# ---- three slide layouts, alternated for rhythm ------------------------------------------------
def s_full(sp, i, n):
    """full-bleed photo, text bottom on a soft scrim"""
    P = [f'<img src="{warm(sp["ph"], W, H, sp.get("fy", .45))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">',
         K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(10,10,10,.35) 0%,rgba(10,10,10,0) 22%,rgba(10,10,10,0) 45%,rgba(10,10,10,.82) 100%);", z=2),
         logo(True), pager(i, n, "#F6EFD8")]
    y = H - 110 - (sp.get("body_lines", 3) * 43) - sp.get("hl_lines", 2) * sp.get("hs", 92) - 70
    if sp.get("kick"): P.append(kick(sp["kick"], 64, y - 50, "#F6EFD8"))
    P.append(headline(sp["hl"], 64, y, sp.get("hs", 92), "#F6EFD8"))
    if sp.get("body"): P.append(body(sp["body"], 64, y + sp.get("hl_lines", 2) * sp.get("hs", 92) + 26, "#F6EFD8", 880))
    if sp.get("link"): P.append(linkline(64, H - 100))
    return P, INK

def s_split(sp, i, n):
    """photo top in a bordered frame on a colour band, text below on cream"""
    col = sp.get("col", MINT)
    P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0), K.box(0, 0, W, 700, f"background:{col};", z=1), logo(False), pager(i, n)]
    P.append(f'<div style="position:absolute;left:64px;top:130px;width:952px;height:530px;border:4px solid #0A0A0A;border-radius:28px;overflow:hidden;'
             f'box-shadow:9px 10px 0 #0A0A0A;z-index:10;transform:rotate({sp.get("rot",-1)}deg)"><img src="{warm(sp["ph"], 952, 530, sp.get("fy", .45))}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    y = 740
    if sp.get("kick"): P.append(kick(sp["kick"], 64, y)); y += 46
    P.append(headline(sp["hl"], 64, y, sp.get("hs", 84))); y += sp.get("hl_lines", 1) * sp.get("hs", 84) + 26
    if sp.get("body"): P.append(body(sp["body"], 64, y)); y += sp.get("body_lines", 3) * 43 + 30
    if sp.get("list"):
        P.append(kick("you could", 64, y, "#5A5A55")); y += 40
        for k, t in enumerate(sp["list"]):
            P.append(f'<div style="position:absolute;left:64px;top:{y+k*52}px;display:flex;align-items:center;gap:16px;z-index:60"><div style="width:20px;height:20px;border-radius:50%;'
                     f'background:{col};border:3px solid #0A0A0A"></div><div style="font-family:var(--e);font-weight:600;font-size:30px">{t}</div></div>')
    if sp.get("chips"): P.append(chips(sp["chips"], 64, y, col))
    if sp.get("link"): P.append(linkline(64, H - 100))
    return P, CREAM

def s_type(sp, i, n):
    """type-led colour slide, optional small photo"""
    col = sp.get("col", LEM); fg = core.text_on(col) if col not in (INK,) else "#F6EFD8"
    P = [K.box(0, 0, W, H, f"background:{col};", z=0), logo(True), pager(i, n, fg)]
    if sp.get("ph"):
        P.append(f'<div style="position:absolute;right:64px;top:150px;width:420px;height:520px;border:4px solid #0A0A0A;border-radius:24px;overflow:hidden;'
                 f'box-shadow:9px 10px 0 #0A0A0A;transform:rotate(3deg);z-index:10"><img src="{warm(sp["ph"], 420, 520, sp.get("fy", .45))}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
    y = sp.get("y", 720 if sp.get("ph") else 380)
    if sp.get("kick"): P.append(kick(sp["kick"], 64, y - 56, fg))
    P.append(headline(sp["hl"], 64, y, sp.get("hs", 110), fg)); y += sp.get("hl_lines", 2) * sp.get("hs", 110) + 34
    if sp.get("body"): P.append(body(sp["body"], 64, y, fg, 900)); y += sp.get("body_lines", 2) * 43 + 30
    if sp.get("chips"): P.append(chips(sp["chips"], 64, y, "#F6EFD8" if col != "#F6EFD8" else LEM))
    if sp.get("link"): P.append(linkline(64, H - 100, bg="#F6EFD8" if col != "#F6EFD8" else LEM))
    return P, col

LAY = {"full": s_full, "split": s_split, "type": s_type}

# ---- the carousels ------------------------------------------------------------------------------
W_RECAP = [
    dict(L="full", ph="sund1", fy=.4, kick="AquaTerra, 2025 to 2026", hl="The last two years,<br><i>on the ground.</i>", hs=104, body="", body_lines=0),
    dict(L="type", col=MINT, hl="158 drives, workshops<br>and visits.", hs=96, kick="the short version", body="Across 79 places in and around Kolkata. Here's what was inside them.", body_lines=2),
    dict(L="split", col=TOM, ph="stem3", fy=.35, kick="teaching", hl="Teaching, mostly.", body="45 workshops: public speaking, chess, STEM, storytelling, art and digital safety. Most of them at Pather Sathi, where we were back almost every week.", body_lines=4),
    dict(L="full", ph="chess4", fy=.5, kick="in those rooms", hl="About 2,000 children.", hs=96, hl_lines=1, body="Counted session by session. Some came once. A lot of them kept coming back.", body_lines=2),
    dict(L="split", col=LEM, ph="dog_bhowanipur", fy=.5, kick="animal welfare", hl="And the dogs.", body="Tails and Treats went out 25 times in these two years. Biscuits, water, and a lot of very patient strays across the city.", body_lines=3),
    dict(L="full", ph="plant", fy=.4, kick="the rest of the calendar", hl="Books, clothes,<br>saplings, sharbat.", hs=92, body="Book Basket ran 15 times. Food For All, Wear and Share, Sharbat Seva, Smile Notes and Grow Green filled in the weeks between.", body_lines=3),
    dict(L="split", col=SKY, ph="sund3", fy=.4, kick="the sundarbans", hl="And in December, further.", hs=76, body="Sunderbans 8.0: a health camp with 120+ checkups, medicines and stationery, and a very long day.", body_lines=3),
    dict(L="full", ph="rakhi", fy=.5, kick="with partners", hl="Never on our own.", hs=96, hl_lines=1, body="A Rakhi workshop for 200 children at BSS School. A day at Science City with Vishwajagriti and Emami. STEM with AIM Foundation.", body_lines=3),
    dict(L="type", col=INK, hl="All of it run by<br><i>people your age.</i>", hs=104, kick="who did this", body="No donations, no staff. Members plan it, show up for it, and fund it with the events they throw.", body_lines=2),
    dict(L="type", col=LEM, ph="stem4", fy=.4, hl="Next year<br>starts now.", hs=120, body="Applications are open.", body_lines=1, link=True),
]

E_OPP = [
    dict(L="full", ph="sund2", fy=.4, kick="AquaTerra, Kolkata", hl="What you'd actually<br>be doing here.", hs=100, body="Department by department. Swipe.", body_lines=1),
    dict(L="type", col=MINT, ph="magic", fy=.4, kick="education", hl="Most of what<br>we do is teach.", hs=100, body="About 70% of our welfare work is a classroom. Everything else in AQ exists to keep that going.", body_lines=2),
    dict(L="split", col=TOM, ph="stem2", fy=.45, kick="teaching", hl="A different classroom every week.", hs=66, body="Public speaking and chess at Pather Sathi. STEM at AIM Foundation. Storytelling at Lamp Open Shelter. Members plan the lesson, the worksheet, and whatever keeps forty kids listening.", body_lines=4,
         list=["plan the lesson", "write the worksheet", "run the room"]),
    dict(L="split", col=LEM, ph="chess1", fy=.4, kick="shikshaq", hl="Free learning, for anyone.", hs=72, body="Our education platform for Kolkata: free study material and question papers, and a search that connects families with tutors near them.", body_lines=3,
         list=["put together papers and notes", "bring teachers on", "build the site"]),
    dict(L="split", col=MINT, ph="plant", fy=.4, kick="welfare", hl="The city, one drive at a time.", hs=66, body="Sharbat in summer. Clothes and books when they're needed. Biscuits for the strays, saplings for the parks.", body_lines=3,
         list=["plan the drive", "gather what it needs", "be there on the day"]),
    dict(L="full", ph="sund4", fy=.35, kick="the sundarbans", hl="And sometimes,<br>much further.", hs=96, body="Relief trips and health camps in the Sundarbans. Eight trips so far.", body_lines=2),
    dict(L="split", col=PINK, ph="rakhi", fy=.5, kick="collabs", hl="Nothing here happens alone.", hs=66, body="Collabs finds the school, college or NGO, and makes the plan work for both sides, from a Rakhi workshop for 200 children to a day at Science City.", body_lines=3,
         list=["find the partner", "pitch the idea", "plan it together"]),
    dict(L="split", col=GRAPE, ph="blog_city", fy=.5, kick="terranotes", hl="Our monthly magazine.", hs=72, body="Essays, art, culture and ideas, written, edited and designed by members, with no AI anywhere in it.", body_lines=3,
         list=["write a piece", "edit someone else's", "design the issue"]),
    dict(L="full", ph="dd_floor_green", fy=.4, kick="events", hl="The nights that<br>pay for the rest.", hs=92, body="AQ takes no donations. Disco Diwali, Paradox and Starry Night fund the workshops and drives.", body_lines=2),
    dict(L="type", col=GRAPE, ph=K.social_slide(9), fy=.3, kick="social media", hl="Telling all of it.", hs=96, hl_lines=1, body="Reels, design, captions, the website. How the city finds out what happened.", body_lines=2),
    dict(L="type", col=TEAL, ph="desk", fy=.4, kick="hr", hl="The people who<br>keep the people.", hs=96, body="Every new member welcomed, every team staffed.", body_lines=1),
    dict(L="type", col=LEM, hl="Start anywhere.", hs=130, hl_lines=1, y=420, body="Teaching, ShikshAQ, welfare, collabs, TerraNotes, events, social, HR, and Crftd, our streetwear label. Applications are open.", body_lines=3, link=True),
]

S_SHIK = [
    dict(L="full", ph="chess1", fy=.45, kick="shikshaq", hl="Free learning,<br><i>for anyone who needs it.</i>", hs=92, body="", body_lines=0),
    dict(L="type", col=LEM, ph="mult", fy=.4, hl="A good tutor<br>shouldn't depend<br>on who you know.", hs=84, hl_lines=3, body="ShikshAQ connects students with tutors near them, by subject, class and board.", body_lines=2),
    dict(L="split", col=SKY, ph="draw", fy=.4, kick="papers and notes", hl="Practice shouldn't cost anything.", hs=64, hl_lines=1, body="Question papers and study material, free, in one place.", body_lines=2),
    dict(L="type", col="#F6EFD8", ph="stem1", fy=.5, hl="For Kolkata.", hs=120, hl_lines=1, y=760, body="", body_lines=0, chips=["Class IV to XII", "ICSE", "ISC", "CBSE", "State board"]),
    dict(L="split", col=LEM, ph="stem2", fy=.45, kick="who builds it", hl="Built inside AQ.", hs=78, body="Members run the outreach, bring teachers on, put the papers together and build the site.", body_lines=3),
    dict(L="type", col=INK, hl="Use it. Share it.<br><i>Or help build it.</i>", hs=100, body="shikshaq.in", body_lines=1, link=True),
]

T_DOGS = [
    dict(L="full", ph="dog_bhowanipur", fy=.55, kick="animal welfare", hl="Tails and Treats.", hs=110, hl_lines=1, body="Feeding Kolkata's strays since January 2022.", body_lines=1),
    dict(L="split", col=LEM, ph="dog_biscuit", fy=.5, kick="how it works", hl="Biscuits, water, a full round.", hs=66, body="A small team, a few packets of biscuits, and every dog on the route. Then the next neighbourhood.", body_lines=3),
    dict(L="type", col=MINT, ph="cow_biscuit", fy=.5, hl="25 rounds in<br>two years.", hs=110, body="Salt Lake, Bhowanipur, Dobson Lane, Jatindas Park, Natural City, and wherever someone spots a hungry one.", body_lines=3),
    dict(L="full", ph="dog_night", fy=.5, kick="after school", hl="Some rounds<br>run after dark.", hs=96, body="", body_lines=0),
    dict(L="type", col=SKY, hl="They know the sound<br><i>of the packet.</i>", hs=100, kick="the regulars", body="Plenty of the same dogs, round after round.", body_lines=1),
    dict(L="type", col=LEM, ph="street_dog", fy=.5, hl="Come on<br>the next round.", hs=110, body="Applications are open.", body_lines=1, link=True),
]

HL = [("Welfare", MINT, "leaf"), ("Teaching", TOM, "star"), ("ShikshAQ", LEM, "speech"), ("Dogs", SKY, "heart"), ("Events", PINK, "burst"), ("Join", GRAPE, "sparkle")]

async def render_set(prefix, slides):
    n = len(slides)
    for i, sp in enumerate(slides, 1):
        sp = dict(sp)
        if "ph" in sp and sp["ph"] in PH: sp["ph"] = PH[sp["ph"]]
        P, bg = LAY[sp["L"]](sp, i, n)
        html = K.page(V6.DEFS + "".join(P) + V6.grain(.3), H, bg=bg)
        await K._render(f"{prefix}{i:02d}", html, H, None, None)
        print("rendered", f"{prefix}{i:02d}")

async def highlights():
    for name, col, icon in HL:
        Hs = 1920
        P = [K.box(0, 0, W, Hs, f"background:{CREAM};", z=0),
             f'<div style="position:absolute;left:240px;top:660px;width:600px;height:600px;border-radius:50%;background:{col};border:6px solid #0A0A0A;z-index:2;'
             f'display:flex;align-items:center;justify-content:center"><div style="width:300px;height:300px">{K.dd.stamp(icon, "#F6EFD8" if col in (TOM, GRAPE, MINT) else INK)}</div></div>',
             f'<div style="position:absolute;left:0;top:1320px;width:{W}px;text-align:center;font-family:var(--s);font-size:96px;z-index:3">{name}</div>']
        html = K.page("".join(P), Hs, bg=CREAM)
        await K._render(f"h_{name.lower()}", html, Hs, None, None)

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    only = set(sys.argv[1:])
    async with K.B.session():
        if not only or "W" in only: await render_set("W", W_RECAP)
        if not only or "E" in only: await render_set("E", E_OPP)
        if not only or "S" in only: await render_set("S", S_SHIK)
        if not only or "T" in only: await render_set("T", T_DOGS)
        if not only or "H" in only: await highlights()

if __name__ == "__main__":
    asyncio.run(main())
