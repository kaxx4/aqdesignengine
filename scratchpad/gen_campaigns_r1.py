"""Campaigns round 1 (owner-approved copy, 2026-11-14): What is AquaTerra, One Sunday, ShikshAQ, and Impact posts.
Owner edits: no funding talk, no Pather Sathi by name, ShikshAQ papers and study material are live. Impact posts use
all-time figures (site / AQ_FACTS), each on a real photo. Each campaign has its own look.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_aq_content_v13 as C
core = K.core
W = 1080; H = 1350; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/campaigns_r1"
PH = C.PH; warm = C.warm

def mix(txt, size, color):
    ss = round(size * .78)
    txt = txt.replace("<i>", f'<i style="font-family:var(--s);font-weight:400;text-transform:none;font-size:{size}px;letter-spacing:-.01em">')
    return (f'<div style="font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:{ss}px;line-height:{size}px;letter-spacing:-.01em;color:{color}">{txt}</div>')

def line(txt, color, size=32, w=900):
    return f'<div style="font-family:var(--e);font-size:{size}px;line-height:{round(size*1.35)}px;color:{color};max-width:{w}px">{txt}</div>'

def block(parts, anchor, z=60, gap=22):
    return f'<div style="position:absolute;left:64px;{anchor};width:952px;display:flex;flex-direction:column;gap:{gap}px;z-index:{z}">' + "".join(parts) + "</div>"

def full(path, fy=.45, h=H):
    return f'<img src="{warm(path, W, h, fy)}" style="position:absolute;inset:0;width:{W}px;height:{h}px;object-fit:cover;z-index:1">'

async def out(name, P, bg, h=H):
    await K._render(name, K.page(V6.DEFS + "".join(P) + V6.grain(.28), h, bg=bg), h, None, None)

# ============================================================ 1. WHAT IS AQUATERRA  (cream, framed photo, big type)
WHAT = [
    ("sund2", .4, "We're<br><i>AquaTerra.</i>", "Here's what that means.", 0),
    ("stem3", .35, "Run by<br><i>students.</i>", "Started in 2021 by 16 school students in Kolkata. Today there are 1,400+ of us, aged 14 to 19.", 1),
    ("chess1", .4, "Mostly,<br><i>we teach.</i>", "Weekly workshops for children at shelters and community centres across the city.", 0),
    ("dog_bhowanipur", .5, "We feed, plant<br><i>and show up.</i>", "Sharbat on hot days, food on the street, biscuits for the strays, saplings for the parks.", 1),
    ("sund4", .35, "We go further<br><i>when it's needed.</i>", "Relief trips and health camps in the Sundarbans.", 0),
    ("stem2", .45, "And we<br><i>build things.</i>", "ShikshAQ, a free learning platform. TerraNotes, our monthly magazine.", 1),
    ("sund1", .4, "Every part of it is<br><i>for someone else.</i>", "That's AquaTerra.", 0),
]
async def what():
    n = len(WHAT)
    for i, (ph, fy, hl, ln, flip) in enumerate(WHAT, 1):
        P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0), K.logo(64, 48), C.pager(i, n)]
        P.append(block([mix(hl, 104, INK), line(ln, "#3A3A36", 32, 880)], "top:150px"))
        rot = -2 if flip else 2
        P.append(f'<div style="position:absolute;left:{90 if flip else 120}px;top:620px;width:870px;height:640px;transform:rotate({rot}deg);border:4px solid #0A0A0A;'
                 f'border-radius:30px;overflow:hidden;box-shadow:12px 13px 0 #0A0A0A;z-index:10"><img src="{warm(PH[ph], 870, 640, fy)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
        await out(f"A{i:02d}_what", P, CREAM)

# ============================================================ 2. ONE SUNDAY  (documentary: full-bleed photo, small caption)
SUNDAY = [
    ("onceupon", .5, None, "One Sunday."),
    ("draw", .4, "The plan gets made on Friday.", "The worksheet, the game, who's bringing chart paper."),
    ("mult", .4, "Thirty-odd kids.", "A handful of us."),
    ("chess4", .5, "Today's lesson: chess.", None),
    ("chessm", .5, "Somebody wins.", "It's rarely the teacher."),
    ("chess1", .4, "Then everyone holds up", "what they made."),
    ("magic", .4, "Same time", "next Sunday."),
]
async def sunday():
    n = len(SUNDAY)
    for i, (ph, fy, a, b) in enumerate(SUNDAY, 1):
        P = [full(PH[ph], fy), K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(0,0,0,.28) 0%,rgba(0,0,0,0) 18%,rgba(0,0,0,0) 62%,rgba(0,0,0,.7) 100%);", z=2),
             K.logo_pill(64, 44, dark=True), C.pager(i, n, "#F6EFD8")]
        if i == 1:
            P.append(block([f'<div style="font-family:var(--s);font-style:italic;font-size:150px;line-height:140px;color:#F6EFD8">{b}</div>',
                            line("a teaching session, start to finish.", "#F6EFD8", 32)], "bottom:90px"))
        else:
            txt = f'<span style="font-weight:600">{a}</span>' + (f'<br>{b}' if b else "")
            P.append(f'<div style="position:absolute;left:64px;bottom:90px;max-width:820px;background:rgba(10,10,10,.72);padding:22px 28px;font-family:var(--e);font-size:40px;'
                     f'line-height:54px;color:#F6EFD8;z-index:60">{txt}</div>')
        await out(f"B{i:02d}_sunday", P, INK)

# ============================================================ 3. SHIKSHAQ  (lemon, clean, icon-led)
SHIK = [
    ("Studying for your exams?<br><i>Start here.</i>", "ShikshAQ: free papers, study material and tutors, for students in Kolkata.", None, "chess1"),
    ("Past papers,<br><i>free.</i>", "Practise on real question papers.", None, "draw"),
    ("Study material,<br><i>free.</i>", "Notes for your class and subject, in one place.", None, "onceupon"),
    ("Need<br><i>a tutor?</i>", "Search near you, by subject, class and area.", None, "stem3"),
    ("Made for<br><i>your syllabus.</i>", None, None, "chess4"),
    ("Built by<br><i>AquaTerra.</i>", "Free, because learning shouldn't depend on what you can pay.", None, "stem4"),
    ("shikshaq.in", "Send it to someone with boards this year.", None, "magic"),
]
async def shik():
    n = len(SHIK)
    for i, (hl, ln, icon, ph) in enumerate(SHIK, 1):
        P = [K.box(0, 0, W, H, f"background:{LEM};", z=0), K.logo_pill(64, 44, dark=True), C.pager(i, n)]
        parts = [mix(hl, 120 if i != 7 else 140, INK)]
        if ln: parts.append(line(ln, INK, 34, 880))
        if i == 5:
            cs = "".join(f'<div style="padding:14px 30px;border:4px solid #0A0A0A;border-radius:999px;background:#F6EFD8;box-shadow:6px 6px 0 #0A0A0A;font-family:var(--d);font-weight:900;font-size:40px;text-transform:uppercase">{c}</div>'
                         for c in ["Class IV to XII", "ICSE", "ISC", "CBSE", "State board"])
            parts.append(f'<div style="display:flex;flex-wrap:wrap;gap:22px;margin-top:60px">{cs}</div>')
        P.append(block(parts, "top:170px"))
        if icon:
            P.append(f'<div style="position:absolute;left:600px;top:760px;width:400px;height:400px;border-radius:50%;background:#F6EFD8;border:5px solid #0A0A0A;'
                     f'box-shadow:12px 13px 0 #0A0A0A;display:flex;align-items:center;justify-content:center;z-index:10"><div style="width:230px;height:230px">{K.dd.stamp(icon, INK)}</div></div>')
        if ph:
            P.append(f'<div style="position:absolute;left:64px;top:{760 if i == 5 else 700}px;width:952px;height:{500 if i == 5 else 560}px;border:4px solid #0A0A0A;border-radius:30px;overflow:hidden;'
                     f'box-shadow:12px 13px 0 #0A0A0A;z-index:10"><img src="{warm(PH[ph], 952, 560, .4)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')
        await out(f"C{i:02d}_shikshaq", P, LEM)

# ============================================================ 4. IMPACT POSTS  (single posts, real photo, one number)
IMPACT = [
    ("chess1", .4, "3,500+", "children", "in our classrooms.", "Taught by members, one workshop at a time.", TOM),
    ("plant", .4, "4,000+", "saplings", "in the ground.", "Parks, schools and roadsides across Kolkata.", MINT),
    ("sund4", .35, "8", "trips", "to the Sundarbans.", "Supplies, relief and health camps.", SKY),
    ("dog_bhowanipur", .5, "53", "rounds", "of Tails and Treats.", "And the regulars still come running.", LEM),
    ("bananas_group", .45, "15,000+", "bananas", "handed out.", "On the street, to whoever needed one.", LEM),
    ("clothes_pile", .45, "2,500 kg", "of clothes", "and books, passed on.", "Collected, sorted and given away.", PINK),
    ("sund1", .4, "540+", "drives", "since 2021.", "Every one planned and run by students.", GRAPE),
]
async def impact():
    for i, (ph, fy, num, word, rest, ln, col) in enumerate(IMPACT, 1):
        P = [full(PH[ph], fy), K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(0,0,0,.35) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,.15) 50%,rgba(0,0,0,.82) 100%);", z=2),
             K.logo_pill(64, 44, dark=True)]
        nums = (f'<div style="display:flex;align-items:baseline;gap:22px;flex-wrap:wrap"><span style="font-family:var(--d);font-weight:900;font-size:210px;line-height:190px;color:{col};'
                f'letter-spacing:-.03em;-webkit-text-stroke:3px #0A0A0A;text-shadow:8px 8px 0 #0A0A0A">{num}</span>'
                f'<span style="font-family:var(--s);font-style:italic;font-size:110px;line-height:110px;color:#F6EFD8">{word}</span></div>')
        P.append(block([nums, mix(rest, 70, "#F6EFD8"), line(ln, "#F6EFD8", 32)], "bottom:90px", gap=14))
        await out(f"D{i:02d}_impact", P, INK)

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    async with K.B.session():
        await what(); await sunday(); await shik(); await impact()

if __name__ == "__main__":
    asyncio.run(main())
