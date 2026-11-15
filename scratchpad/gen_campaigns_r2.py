"""Campaigns round 2 (2026-11-15): the rest of the plan, plus stories, highlights and WhatsApp.

Campaigns (each its own message and look):
  E  One Round (Tails and Treats)        documentary, lemon caption tags
  F  The Sundarbans trip                 cinematic, warm, serif captions
  G  What you'll learn here              solid colour + framed photo
  H  How a collab happens                cream + pink, partner pills
  I  TerraNotes                          grape, taped covers
  J  Come in                             chat bubbles (the format the owner liked)
Stories (1080x1920): 4 frames per campaign, including round-1 campaigns. Highlights: 8 covers. WhatsApp: 3 squares.
Rules: no funding talk, no Pather Sathi by name, no pay, no member names, no stats as headline (impact posts are the
exception, built in round 1). Real photos only. ShikshAQ facts as owner-confirmed.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_recruit_v10 as V10
import gen_aq_content_v13 as C
core = K.core
W = 1080; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/campaigns_r2"
PH = C.PH; warm = C.warm
bub = V10.bub
LINK = "ngoaquaterra.com/recruitment"

def mix(txt, size, color):
    ss = round(size * .78)
    txt = txt.replace("<i>", f'<i style="font-family:var(--s);font-weight:400;text-transform:none;font-size:{size}px;letter-spacing:-.01em">')
    return f'<div style="font-family:var(--d);font-weight:900;text-transform:uppercase;font-size:{ss}px;line-height:{size}px;letter-spacing:-.01em;color:{color}">{txt}</div>'

def line(txt, color, size=32, w=900):
    return f'<div style="font-family:var(--e);font-size:{size}px;line-height:{round(size*1.35)}px;color:{color};max-width:{w}px">{txt}</div>'

def block(parts, anchor, z=60, gap=22, w=952):
    return f'<div style="position:absolute;left:64px;{anchor};width:{w}px;display:flex;flex-direction:column;gap:{gap}px;z-index:{z}">' + "".join(parts) + "</div>"

def full(path, H, fy=.45):
    return f'<img src="{warm(path, W, H, fy)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

def framed(path, x, y, w, h, rot=0, fy=.45, z=10, r=30):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);border:4px solid #0A0A0A;border-radius:{r}px;'
            f'overflow:hidden;box-shadow:12px 13px 0 #0A0A0A;z-index:{z}"><img src="{warm(path, w, h, fy)}" style="width:100%;height:100%;object-fit:cover;display:block"></div>')

def chrome(i, n, H, dark=True, col="#F6EFD8", story=False):
    top = 200 if story else 0
    P = [K.logo_pill(64, 44 + top, dark=True) if dark else K.logo(64, 48 + top)]
    if n: P.append(C.pager(i, n, col).replace("top:58px", f"top:{58+top}px"))
    return P

def linkline(y, txt=LINK, bg="#F6EFD8"):
    return C.linkline(64, y, txt, bg)

async def out(name, P, bg, H):
    await K._render(name, K.page(V6.DEFS + "".join(P) + V6.grain(.26), H, bg=bg), H, None, None)

def geo(story):
    return (1920, 200, 250) if story else (1350, 0, 0)

# ------------------------------------------------------------------ the looks (each takes story=)
def L_doc(sp, i, n, story=False, tag=LEM):
    """documentary: full-bleed photo, caption on a coloured tag bottom-left"""
    H, top, bot = geo(story)
    P = [full(PH[sp["ph"]], H, sp.get("fy", .45)), K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(0,0,0,.3) 0%,rgba(0,0,0,0) 18%,rgba(0,0,0,0) 60%,rgba(0,0,0,.65) 100%);", z=2)]
    P += chrome(i, n, H, story=story)
    if sp.get("title"):
        P.append(block([f'<div style="font-family:var(--s);font-style:italic;font-size:150px;line-height:140px;color:#F6EFD8">{sp["title"]}</div>', line(sp.get("sub", ""), "#F6EFD8", 32)], f"bottom:{90+bot}px"))
    else:
        txt = f'<span style="font-weight:600">{sp["a"]}</span>' + (f'<br>{sp["b"]}' if sp.get("b") else "")
        P.append(f'<div style="position:absolute;left:64px;bottom:{90+bot}px;max-width:820px;background:{tag};padding:20px 28px;font-family:var(--e);font-size:40px;'
                 f'line-height:54px;color:#0A0A0A;border:4px solid #0A0A0A;box-shadow:7px 8px 0 #0A0A0A;transform:rotate(-1.5deg);z-index:60">{txt}</div>')
    if sp.get("link"): P.append(linkline(H - bot - 60 - 40 - 60 if False else 160 + top))
    return P, INK, H

def L_cine(sp, i, n, story=False):
    """cinematic: warm full-bleed, letterbox bars, big serif caption"""
    H, top, bot = geo(story)
    bar = 120 if not story else 0
    P = [full(PH[sp["ph"]], H, sp.get("fy", .45)), K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(20,8,0,.25),rgba(20,8,0,0) 38%,rgba(10,4,0,.82));", z=2)]
    if bar: P += [K.box(0, 0, W, bar, "background:#0A0A0A;", z=3), K.box(0, H - bar, W, bar, "background:#0A0A0A;", z=3)]
    P += chrome(i, n, H, story=story)
    parts = [f'<div style="font-family:var(--s);font-style:italic;font-size:{sp.get("hs", 96)}px;line-height:{sp.get("hs", 96)}px;color:#FFF3E0;text-shadow:0 3px 24px rgba(0,0,0,.6)">{sp["hl"]}</div>']
    if sp.get("ln"): parts.append(line(sp["ln"], "#FFF3E0", 30))
    P.append(block(parts, f"bottom:{bar + 70 + bot}px"))
    if sp.get("link"): P.append(linkline(bar + 40 + top))
    return P, INK, H

def L_solid(sp, i, n, story=False):
    """solid colour + big mixed headline + framed photo"""
    H, top, bot = geo(story)
    col = sp.get("col", MINT); fg = "#F6EFD8" if col == INK else core.text_on(col)
    P = [K.box(0, 0, W, H, f"background:{col};", z=0)] + chrome(i, n, H, col=fg, story=story)
    parts = [mix(sp["hl"], sp.get("hs", 104), fg)]
    if sp.get("ln"): parts.append(line(sp["ln"], fg, 32))
    P.append(block(parts, f"top:{150+top}px"))
    if sp.get("ph"):
        fh = 600 if not story else 860
        P.append(framed(PH[sp["ph"]], 90, H - bot - fh - 90, 900, fh, sp.get("rot", 2), sp.get("fy", .45)))
    if sp.get("link"): P.append(linkline(H - bot - 110))
    return P, col, H

def L_cream(sp, i, n, story=False):
    """cream + headline + framed photo + optional pills (collabs look)"""
    H, top, bot = geo(story)
    P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0), K.box(0, 0, 22, H, f"background:{PINK};", z=1)] + chrome(i, n, H, dark=False, col=INK, story=story)
    parts = [mix(sp["hl"], sp.get("hs", 100), INK)]
    if sp.get("num"): parts.insert(0, f'<div style="font-family:var(--d);font-weight:900;font-size:120px;line-height:110px;color:{PINK};-webkit-text-stroke:3px #0A0A0A">{sp["num"]}</div>')
    if sp.get("ln"): parts.append(line(sp["ln"], "#3A3A36", 32))
    if sp.get("pills"):
        ps = "".join(f'<div style="padding:12px 26px;border:4px solid #0A0A0A;border-radius:999px;background:{c};box-shadow:5px 5px 0 #0A0A0A;font-family:var(--e);font-weight:600;font-size:30px">{t}</div>' for t, c in sp["pills"])
        parts.append(f'<div style="display:flex;flex-wrap:wrap;gap:16px;margin-top:10px">{ps}</div>')
    P.append(block(parts, f"top:{150+top}px"))
    if sp.get("ph"):
        fh = 560 if not story else 800
        P.append(framed(PH[sp["ph"]], 100, H - bot - fh - 100, 880, fh, sp.get("rot", -2), sp.get("fy", .45)))
    if sp.get("link"): P.append(linkline(H - bot - 110, sp.get("url", LINK)))
    return P, CREAM, H

def L_taped(sp, i, n, story=False):
    H, top, bot = geo(story)
    col = sp.get("col", GRAPE); fg = core.text_on(col)
    P = [K.box(0, 0, W, H, f"background:{col};", z=0)] + chrome(i, n, H, col=fg, story=story)
    parts = [mix(sp["hl"], sp.get("hs", 104), fg)]
    if sp.get("ln"): parts.append(line(sp["ln"], fg, 32))
    P.append(block(parts, f"top:{150+top}px"))
    phs = sp.get("phs", [])
    y0 = H - bot - (640 if not story else 900)
    spots = [(60, y0, 440, 560, -5), (540, y0 + 40, 440, 560, 4)] if len(phs) == 2 else [(40, y0, 320, 440, -6), (380, y0 + 40, 320, 440, 4), (720, y0, 320, 440, -3)]
    if story: spots = [(x, y, int(w * 1.0), int(h * 1.35), r) for (x, y, w, h, r) in spots]
    for j, (pth, (x, y, w, h, r)) in enumerate(zip(phs, spots)):
        P.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w+24}px;height:{h+24}px;transform:rotate({r}deg);background:#FBF8EE;padding:12px;'
                 f'box-shadow:9px 10px 0 rgba(10,10,10,.85);z-index:{10+j}"><img src="{warm(PH[pth], w, h, .45)}" style="width:{w}px;height:{h}px;object-fit:cover;display:block"></div>')
        P.append(V6.tape(x + w // 2 - 60, y - 18, 130, 42, r * 2, seed=40 + j, z=30))
    if sp.get("link"): P.append(linkline(H - bot - 110, sp.get("url", LINK)))
    return P, col, H

def L_chat(sp, i, n, story=False):
    H, top, bot = geo(story)
    P = [f'<img src="{K.uri(K.mono(K.cover(PH[sp["ph"]], W, H, fy=sp.get("fy", .45)), 1.1))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">',
         K.box(0, 0, W, H, f"background:{sp.get('tint', PINK)};mix-blend-mode:multiply;opacity:.5;", z=2), K.box(0, 0, W, H, "background:rgba(10,10,10,.25);", z=3)]
    P += chrome(i, n, H, story=story)
    y = 260 + top + (200 if story else 0)
    for k, (t, big) in enumerate(sp["lines"]):
        side = "L" if k % 2 == 0 else "R"; size = 66 if big else 44
        est = min(860, int(len(t.replace("<br>", "")) * size * .5) + 70)
        x = 64 if side == "L" else W - 64 - est
        P.append(bub(t, x, y, LEM if big else ("#FFFFFF" if side == "L" else sp.get("rc", SKY)), side, size, [-2, 2.5, -1.5, 2][k % 4], maxw=880))
        y += int(size * 1.22 * (t.count("<br>") + 1)) + 90
    if sp.get("link"): P.append(linkline(H - bot - 110))
    return P, INK, H

LOOK = {"doc": L_doc, "cine": L_cine, "solid": L_solid, "cream": L_cream, "taped": L_taped, "chat": L_chat}

# ------------------------------------------------------------------ copy
ROUND = [  # E One Round
    dict(L="doc", ph="dog_bhowanipur", fy=.55, title="One round.", sub="Tails and Treats: feeding Kolkata's strays."),
    dict(L="doc", ph="dog_biscuit", fy=.5, a="Biscuits in the bag.", b="Water. A route. A few of us."),
    dict(L="doc", ph="dog_saltlake", fy=.5, a="First stop.", b="They hear the packet before they see us."),
    dict(L="doc", ph="cow_biscuit", fy=.5, a="Sometimes a cow joins in.", b="Nobody objects."),
    dict(L="doc", ph="dog_night", fy=.5, a="Some rounds run late.", b="The dogs don't mind."),
    dict(L="doc", ph="street_dog", fy=.5, a="Same streets, same faces,", b="round after round."),
    dict(L="solid", col=LEM, hl="Next round's<br><i>soon.</i>", hs=140, ln="Come along. Apply at "+LINK),
]
SUND = [  # F Sundarbans
    dict(L="cine", ph="sundarbans", fy=.5, hl="The Sundarbans trip.", hs=120, ln="Weeks of planning for one long day."),
    dict(L="cine", ph="sund2", fy=.4, hl="It starts weeks before,<br>with lists.", ln="Who's going. What's needed. Who's carrying what."),
    dict(L="cine", ph="sund3", fy=.4, hl="Medicines. Stationery.<br>Packed by hand.", ln=""),
    dict(L="cine", ph="sund4", fy=.35, hl="Then a full day<br>of checkups.", ln=""),
    dict(L="solid", col=INK, hl="Eight trips.<br><i>The next one needs<br>more hands.</i>", hs=110, link=True),
]
LEARN = [  # G What you'll learn here
    dict(L="solid", col=LEM, ph="holi", fy=.4, hl="What you'll<br><i>learn here.</i>", hs=120, ln="Stuff no exam tests."),
    dict(L="solid", col=TOM, ph="stem2", fy=.45, hl="How to stand<br><i>in front of a room.</i>", ln="Teach forty kids once and presentations stop being scary."),
    dict(L="solid", col=MINT, ph="plant", fy=.4, hl="How to plan<br><i>something real.</i>", ln="A drive has a date, a place, a list and people counting on it."),
    dict(L="solid", col=PINK, ph="cookie", fy=.4, hl="How to talk to<br><i>people who aren't your friends.</i>", hs=92, ln="Principals, partners, shopkeepers."),
    dict(L="solid", col=GRAPE, ph="blog_tea", fy=.5, hl="How to write<br><i>for someone.</i>", ln="TerraNotes, captions, emails that get replies."),
    dict(L="solid", col=SKY, ph="dd_floor_green", fy=.4, hl="How to be someone<br><i>a team counts on.</i>", hs=96, ln="And what it feels like when it works."),
    dict(L="solid", col=LEM, ph="dd_group", fy=.6, hl="Come find out<br><i>what else.</i>", ln="Applications are open.", link=True),
]
COLLAB = [  # H How a collab happens
    dict(L="cream", ph="rakhi", fy=.5, hl="How a collab<br><i>happens.</i>", hs=112, ln="For schools, colleges and NGOs in Kolkata."),
    dict(L="cream", ph="emami", fy=.5, num="01", hl="It starts with<br><i>a conversation.</i>", ln="You reach out, or we do. Either way, we listen first."),
    dict(L="cream", ph="desk", fy=.45, num="02", hl="We plan it<br><i>together.</i>", ln="What it is, who it's for, when, and how many of us."),
    dict(L="cream", ph="old_age", fy=.45, num="03", hl="Then we<br><i>show up.</i>", ln="With the team, the material and everything else it needs."),
    dict(L="cream", hl="Recently,<br><i>with:</i>", hs=112, pills=[("BSS School", LEM), ("Ashok Hall", MINT), ("AIM Foundation", SKY), ("Vishwajagriti", PINK), ("Emami", TOM)], ph="plant_school", fy=.45),
    dict(L="cream", ph="green_talk", fy=.5, hl="Work<br><i>with us.</i>", hs=120, ln="Workshops, drives, events, ideas.", link=True, url="ngoaquaterra.com/collaborations"),
]
TERRA = [  # I TerraNotes
    dict(L="taped", phs=["blog_city", "blog_mirror"], hl="TerraNotes.", hs=130, ln="A monthly magazine by AquaTerra."),
    dict(L="taped", phs=["blog_dynamics", "blog_opinions", "blog_tea"], hl="Essays, art<br><i>and the city.</i>", ln="Whatever's on our minds that month."),
    dict(L="taped", phs=["blog_syntax", "blog_pebbles"], hl="Written by<br><i>people your age.</i>", ln="Edited and designed by members. No AI, ever."),
    dict(L="taped", phs=["blog_judge", "blog_empathy", "blog_nostalgia"], hl="Read it.<br><i>Or write for it.</i>", ln="ngoaquaterra.com/terranotes", link=True, url="ngoaquaterra.com/recruitment"),
]
COMEIN = [  # J Come in
    dict(L="chat", ph="five_group", fy=.5, tint=PINK, lines=[("so what do people<br>actually do at aq", False), ("teach, mostly.<br>and a lot else.", False), ("come see.", True)]),
    dict(L="chat", ph="teach_abc", fy=.35, tint=TOM, lines=[("i've never taught<br>anything", False), ("neither had we", False), ("we'll show you how.", True)]),
    dict(L="chat", ph="dog_night", fy=.5, tint=MINT, rc=MINT, lines=[("dog round on sunday", False), ("i'll bring biscuits", False), ("come. they sniff<br>new people first.", True)]),
    dict(L="chat", ph="books", fy=.45, tint=GRAPE, rc=GRAPE, lines=[("can i write for<br>terranotes?", False), ("that's what it's for", False), ("send it.", True)]),
    dict(L="chat", ph="sharbat_bananas", fy=.4, tint=LEM, lines=[("do i need experience?", False), ("nope. everyone<br>starts somewhere.", False), ("come once.<br>decide after.", True)], link=True),
]

CAMPAIGNS = {"E_round": ROUND, "F_sund": SUND, "G_learn": LEARN, "H_collab": COLLAB, "I_terra": TERRA, "J_comein": COMEIN}
STORY_PICK = {"E_round": [0, 2, 3, 6], "F_sund": [0, 2, 3, 4], "G_learn": [0, 1, 3, 6], "H_collab": [0, 2, 4, 5], "I_terra": [0, 1, 2, 3], "J_comein": [0, 1, 2, 4]}

async def render_campaign(key, slides):
    n = len(slides)
    for i, sp in enumerate(slides, 1):
        P, bg, H = LOOK[sp["L"]](sp, i, n)
        await out(f"{key}_{i:02d}", P, bg, H)
    for k, idx in enumerate(STORY_PICK[key], 1):
        sp = slides[idx]
        P, bg, H = LOOK[sp["L"]](sp, None, None, story=True)
        await out(f"{key}_story{k}", P, bg, H)

# round-1 campaigns as stories (reuse round-1 copy through these looks)
R1_STORIES = {
    "A_what": [dict(L="solid", col=LEM, ph="artnook", fy=.45, hl="We're<br><i>AquaTerra.</i>", hs=130, ln="Run by students, aged 14 to 19, in Kolkata."),
               dict(L="solid", col=TOM, ph="teach_class", fy=.5, hl="Mostly,<br><i>we teach.</i>", hs=130),
               dict(L="solid", col=MINT, ph="sharbat_stall", fy=.4, hl="We feed, plant<br><i>and show up.</i>", hs=110),
               dict(L="solid", col=SKY, ph="sharbat_cup", fy=.5, hl="Every part of it is<br><i>for someone else.</i>", hs=96, link=True)],
    "B_sunday": [dict(L="doc", ph="mult", fy=.45, title="One Sunday.", sub="what teaching with us actually looks like."),
                 dict(L="doc", ph="chess4", fy=.5, a="Today's lesson: chess."),
                 dict(L="doc", ph="chess1", fy=.4, a="Then everyone holds up", b="what they made."),
                 dict(L="doc", ph="magic", fy=.4, a="Same time", b="next Sunday.")],
    "C_shik": [dict(L="solid", col=LEM, ph="books", fy=.45, hl="Exam season?<br><i>Start with<br>the papers.</i>", hs=110),
               dict(L="solid", col=LEM, ph="fable", fy=.5, hl="Past papers.<br><i>Free.</i>", hs=130),
               dict(L="solid", col=LEM, ph="teach_board", fy=.4, hl="Need<br><i>a tutor?</i>", hs=130, ln="Search near you, by subject, class and area."),
               dict(L="solid", col=LEM, ph="stem3", fy=.35, hl="shikshaq.in", hs=150, ln="Send it to someone with boards this year.")],
}

HL = [("About", LEM, "artnook"), ("Teaching", TOM, "teach_class"), ("ShikshAQ", LEM, "books"), ("Dogs", MINT, "dog_bhowanipur"), ("Sundarbans", SKY, "sundarbans"),
      ("Collabs", PINK, "rakhi"), ("TerraNotes", GRAPE, "blog_city"), ("Join", TEAL, "five_group")]

async def highlights():
    for name, col, ph in HL:
        H = 1920
        im = K.cover(PH[ph], 560, 560, fy=.4)
        P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0),
             f'<div style="position:absolute;left:250px;top:620px;width:580px;height:580px;border-radius:50%;background:{col};border:6px solid #0A0A0A;box-shadow:12px 13px 0 #0A0A0A;z-index:2"></div>',
             f'<img src="{K.uri(im)}" style="position:absolute;left:290px;top:660px;width:500px;height:500px;border-radius:50%;object-fit:cover;border:5px solid #0A0A0A;z-index:3">',
             f'<div style="position:absolute;left:0;top:1290px;width:{W}px;text-align:center;font-family:var(--d);font-weight:900;font-size:76px;text-transform:uppercase;color:{INK};z-index:3">{name}</div>']
        await out(f"K_highlight_{name.lower()}", P, CREAM, H)

async def whatsapp():
    H = 1080
    sets = [("dd_group", .6, PINK, [("so what do people<br>actually do at aq", False), ("teach, mostly.<br>and a lot else.", False), ("come see.", True)]),
            ("teach_abc", .35, TOM, [("i've never taught<br>anything", False), ("you'll be fine.", True)]),
            ("sund1", .4, LEM, [("send this to the friend<br>who'd actually show up", False), ("come once.<br>decide after.", True)])]
    for k, (ph, fy, tint, lines) in enumerate(sets, 1):
        P = [f'<img src="{K.uri(K.mono(K.cover(PH[ph], W, H, fy=fy), 1.1))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">',
             K.box(0, 0, W, H, f"background:{tint};mix-blend-mode:multiply;opacity:.5;", z=2), K.box(0, 0, W, H, "background:rgba(10,10,10,.25);", z=3), K.logo_pill(64, 44, dark=True)]
        y = 220
        for j, (t, big) in enumerate(lines):
            side = "L" if j % 2 == 0 else "R"; size = 66 if big else 46
            est = min(860, int(len(t.replace("<br>", "")) * size * .5) + 70)
            x = 64 if side == "L" else W - 64 - est
            P.append(bub(t, x, y, LEM if big else "#FFFFFF", side, size, [-2, 2.5, -1.5][j % 3], maxw=880))
            y += int(size * 1.22 * (t.count("<br>") + 1)) + 90
        P.append(linkline(H - 100))
        await out(f"L_whatsapp_{k}", P, INK, H)

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    only = set(sys.argv[1:])
    async with K.B.session():
        for key, slides in CAMPAIGNS.items():
            if not only or key[0] in only: await render_campaign(key, slides)
        if not only or "R" in only:
            for key, frames in R1_STORIES.items():
                for k, sp in enumerate(frames, 1):
                    P, bg, H = LOOK[sp["L"]](sp, None, None, story=True)
                    await out(f"{key}_story{k}", P, bg, H)
        if not only or "K" in only: await highlights()
        if not only or "L" in only: await whatsapp()

if __name__ == "__main__":
    asyncio.run(main())
