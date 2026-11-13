"""AQ recruitment v10: "we should totally...", text bubbles as a free graphic element.

Owner (2026-11-13) on v9: keep the text-bubble format, but do not copy the rest of the messaging UI. Removed: the
'AQUATERRA | the group chat' header, typing dots, 'seen', the link as a bubble ("the NGO recruitment plug is weird"),
"this one did.", and "every sunday. 2.5 years now." Blog piece renamed to the digital magazine. More variation: every
piece now has its own composition (scattered, one giant bubble, a sticker pile, a staircase, bubbles taped to covers,
an unfinished sentence).

Chat lines are SCRIPTED. The outcome bubbles are real: Tails and Treats round 53; Disco Diwali 2.0 550 registrations;
300 walk-ins at Novus; 3,500+ children reached through educational workshops (aq-master-brief); the magazine is out.
Chrome: a small logo and a small plain url line only.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_recruit_v9 as V9
core = K.core
W = 1080; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/recruit_nov2026/v10"
PH = K.PH

def bub(text, x, y, col, side="L", size=42, rot=0, maxw=640, z=60, tape=False, fg=None, pad=(20, 30)):
    fg = fg or core.text_on(col)
    r = "40px 40px 40px 10px" if side == "L" else "40px 40px 10px 40px"
    t = (f'<div style="position:absolute;left:50%;top:-20px;width:120px;height:40px;margin-left:-60px;background:#F2E4B3;opacity:.9;transform:rotate({-rot*2-4}deg)"></div>' if tape else "")
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;max-width:{maxw}px;width:max-content;transform:rotate({rot}deg);background:{col};color:{fg};'
            f'border:4px solid #0A0A0A;border-radius:{r};box-shadow:7px 8px 0 #0A0A0A;padding:{pad[0]}px {pad[1]}px {pad[0]+2}px;font-family:var(--e);font-weight:600;'
            f'font-size:{size}px;line-height:{round(size*1.2)}px;z-index:{z}">{text}{t}</div>')

def chrome(top=0, bot=0, H=1350, dark=True):
    url = (f'<div style="position:absolute;left:64px;top:{H-bot-86}px;font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.04em;color:#0A0A0A;'
           f'background:#F6EFD8;padding:6px 12px;z-index:80">{V9.LINK}</div>')
    return [K.logo_pill(64, 44 + top, dark=True), url]

async def done(name, P, H):
    html = K.page(V6.DEFS + "".join(P) + V6.grain(.4), H, bg=CREAM)
    await K._render(name, html, H, None, None)
    print("rendered", name)

geo = V9.geo

# 1. scattered around the dogs
async def dogs(story=False):
    H, top, bot = geo(story); o = 0 if not story else 160
    P = V9.bg_cast(PH["dog_bhowanipur"], H, fy=.5, wins=[(290, int(H*.53), 270, int(H*.30), MINT, "THE DOGS", "bl"), (575, int(H*.53), 330, int(H*.30), LEM, "ALSO THE DOGS", "tr")])
    P += [bub("we should totally feed<br>the dogs near school", 64, 170 + o, "#FFFFFF", "L", 44, -2.5),
          bub("i'll bring biscuits", 600, 400 + o, MINT, "R", 40, 3),
          bub("round 53.", 64, 540 + o, LEM, "L", 80, -4, pad=(16, 34), z=40)]
    P += chrome(top, bot, H)
    await done("f1_dogs" + ("_story" if story else ""), P, H)

# 2. one giant bubble across the party
async def party(story=False):
    H, top, bot = geo(story); o = 0 if not story else 200
    P = V9.bg_duo(PH["dd_blue"], H, "PARTY", GRAPE, PINK)
    P += [bub("what if we threw<br>a party for charity", 40, 360 + o, "#FFFFFF", "L", 92, -5, maxw=1000, pad=(30, 44)),
          bub("who's booking the dhol", 520, 720 + o, SKY, "R", 38, 4),
          bub("me??", 140, 820 + o, "#FFFFFF", "L", 38, -3),
          bub("550 registrations.", 420, 960 + o, LEM, "R", 58, 2)]
    P += chrome(top, bot, H)
    await done("f2_party" + ("_story" if story else ""), P, H)

# 3. sticker pile, top right
async def tees(story=False):
    H, top, bot = geo(story); o = 0 if not story else 140
    pal = ["#2a0f0a", "#7a1f12", "#c43a1e", "#ff4d2e", "#f6a07a", "#f6efd8"]
    P = V9.bg_poster(PH["tee_novus"], H, pal, fy=.3)
    P += [bub("we should make<br>our own t-shirts", 380, 140 + o, "#FFFFFF", "L", 50, 6),
          bub("and spray them at school fests", 300, 330 + o, TOM, "R", 36, -5, fg="#0A0A0A"),
          bub("300 walk-ins<br>at novus.", 520, 450 + o, LEM, "L", 72, 3),
          bub("profit funds a welfare drive", 90, int(H*.78), "#F6EFD8", "R", 32, -2)]
    P += chrome(top, bot, H)
    await done("f3_tees" + ("_story" if story else ""), P, H)

# 4. staircase down the tiles
async def teach(story=False):
    H, top, bot = geo(story); o = 0 if not story else 220
    P = V9.bg_tiles([PH["teach_abc"], PH["teach_class"], PH["art_table"], PH["holi"], PH["fable"], PH["green_talk"]], H, [MINT, SKY, LEM, PINK, TOM, GRAPE])
    P += [bub("someone should<br>teach those kids", 64, 230 + o, "#FFFFFF", "L", 58, 0),
          bub("saturday?", 420, 520 + o, MINT, "R", 46, 0),
          bub("3,500+ kids later.", 230, 700 + o, LEM, "L", 70, 0)]
    P += chrome(top, bot, H)
    await done("f4_teach" + ("_story" if story else ""), P, H)

# 5. bubbles taped onto the magazine covers
async def mag(story=False):
    H, top, bot = geo(story); o = 0 if not story else 180
    covers = [PH["blog_mirror"], PH["blog_dynamics"], PH["blog_city"], PH["blog_tea"], PH["blog_syntax"], PH["blog_pebbles"]]
    P = V9.bg_taped(covers, H)
    P += [bub("we should start<br>a magazine", 80, 250 + o, "#FFFFFF", "L", 54, -4, tape=True),
          bub("who's writing", 600, 520 + o, GRAPE, "R", 40, 5, tape=True),
          bub("everyone, apparently", 120, 760 + o, "#FFFFFF", "L", 40, -3, tape=True),
          bub("it's out.", 560, 960 + o, LEM, "R", 76, 4, tape=True)]
    P += chrome(top, bot, H)
    await done("f5_mag" + ("_story" if story else ""), P, H)

# 6. the unfinished sentence
async def closer(story=False):
    H, top, bot = geo(story)
    P = V9.bg_cast(PH["dd_group"], H, fy=.6, wins=[(40, int(H*.22), 300, int(H*.26), PINK, "", "tl"), (390, int(H*.17), 300, int(H*.28), SKY, "", "tr"), (730, int(H*.21), 320, int(H*.27), LEM, "", "tl")])
    P = [p.replace('padding:0 10px;background', 'padding:0;width:0;background') if 'line-height:26px' in p else p for p in P]
    P.append(V9.scrim(H, 0, .5))
    cur = '<span style="display:inline-block;width:8px;height:84px;background:#0A0A0A;margin-left:10px;vertical-align:-14px"></span>'
    P += [bub(f"we should totally{cur}", 64, int(H*.58), "#FFFFFF", "L", 96, -2, maxw=980, pad=(30, 44)),
          f'<div style="position:absolute;left:84px;top:{int(H*.58)+190}px;font-family:var(--s);font-style:italic;font-size:56px;color:#FFFFFF;z-index:70;text-shadow:0 2px 14px rgba(0,0,0,.6);transform:rotate(-2deg)">finish the sentence.</div>']
    P += chrome(top, bot, H)
    await done("f6_closer" + ("_story" if story else ""), P, H)

JOBS = {"dogs": dogs, "party": party, "tees": tees, "teach": teach, "mag": mag, "closer": closer}

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
