"""Campaigns r3: ONE system, the v2 Pinterest-recreation look, peer voice (owner, 2026-11-15: "weird vibe": too many
styles, too polished/corporate, tone off; closest = the v2 Pinterest recreations).

System (every slide): a real photo is the ground; one of four devices from the owner's references sits on it
  cast  colour windows with tiny tabs over a b&w photo
  note  frosted card holding a photo, one highlighted phrase
  blank a sentence where photo crops stand in for words
  glass full-bleed photo, glass pills carrying the details
Type: Instrument Serif lowercase headlines, Eina lowercase body, JetBrains Mono tabs. No bold caps, no hard drop-shadow cards.
Voice: lowercase, first person plural, the way members talk.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_recruit_v3 as T3
import gen_aq_content_v13 as C
from PIL import ImageDraw
core = K.core
W = 1080; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/campaigns_r3"
PH = C.PH; LINK = "ngoaquaterra.com/recruitment"

def geo(story): return (1920, 200, 250) if story else (1350, 0, 0)
def logo(top): return K.logo_pill(64, 44 + top, dark=True)
def pager(i, n, top, col="#F6EFD8"):
    return "" if not n else f'<div style="position:absolute;right:64px;top:{58+top}px;font-family:var(--m);font-weight:700;font-size:18px;color:{col};z-index:80">{i:02d} / {n:02d}</div>'
def serif(txt, size, color, extra=""):
    return f'<div style="font-family:var(--s);font-size:{size}px;line-height:{round(size*.98)}px;letter-spacing:-.015em;color:{color};{extra}">{txt}</div>'
def body(txt, color, size=30, w=820):
    return f'<div style="font-family:var(--e);font-size:{size}px;line-height:{round(size*1.4)}px;color:{color};max-width:{w}px">{txt}</div>'
def col_block(parts, anchor, w=952, z=60, gap=18):
    return f'<div style="position:absolute;left:64px;{anchor};width:{w}px;display:flex;flex-direction:column;gap:{gap}px;z-index:{z}">' + "".join(parts) + "</div>"
def link(y, txt=LINK):
    return (f'<div style="position:absolute;left:64px;top:{y}px;font-family:var(--m);font-weight:700;font-size:24px;color:#0A0A0A;background:#F6EFD8;padding:8px 14px;z-index:90">{txt}</div>')

# ------------------------------------------------------------------ devices
def D_cast(sp, i, n, story=False):
    H, top, bot = geo(story)
    m = K.mono(K.cover(PH[sp["ph"]], W, H, fy=sp.get("fy", .45)), 1.1)
    P = [f'<img src="{K.uri(m)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">',
         K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(236,236,232,.95) 0%,rgba(236,236,232,.88) 26%,rgba(236,236,232,0) 44%);", z=2)]
    for (x, y, w, h, c, lab, side) in sp.get("wins", []):
        P.append(V6.window(x, int(y * H / 1350) + (top if story else 0), w, int(h * H / 1350), c, lab, side, z=6))
    P.append(col_block([serif(sp["hl"], sp.get("hs", 96), INK)] + ([body(sp["ln"], "#2A2A26", 28)] if sp.get("ln") else []), f"top:{140+top}px"))
    P += [logo(top), pager(i, n, top, INK)]
    if sp.get("link"): P.append(link(H - bot - 110))
    return P, H

def D_note(sp, i, n, story=False):
    H, top, bot = geo(story)
    pal = sp.get("pal", ["#0d2413", "#17391c", "#245a24", "#3f7a2a", "#7a9a35", "#b9b04a", "#e6dca0"])
    bg = K.posterise(K.cover(PH[sp["bg"]], W, H, fy=sp.get("bfy", .45)), pal, blur=5)
    P = [f'<img src="{K.uri(bg, "PNG")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:1">', V6.halftone_over(W, H, 2, .07)]
    cy = 300 + top + (120 if story else 0)
    P.append(K.box(64, cy, 600, 800, "background:rgba(244,239,224,.7);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:3px solid rgba(255,255,255,.85);", z=4))
    P.append(f'<img src="{C.warm(PH[sp["ph"]], 544, 460, sp.get("fy", .45))}" style="position:absolute;left:92px;top:{cy+28}px;width:544px;height:460px;object-fit:cover;border:3px solid #fff;z-index:5">')
    P.append(f'<div style="position:absolute;left:92px;top:{cy+512}px;font-family:var(--e);font-size:38px;color:#0A0A0A;z-index:6">{sp["pre"]}</div>')
    P.append(f'<div style="position:absolute;left:92px;top:{cy+572}px;padding:0 18px 6px;background:{sp.get("cc", SKY)};font-family:var(--e);font-weight:600;font-size:{sp.get("cs", 70)}px;'
             f'line-height:{sp.get("cs", 70)+12}px;color:#0A0A0A;z-index:6">{sp["chip"]}</div>')
    if sp.get("side"):
        P.append(f'<div style="position:absolute;left:700px;top:{cy+30}px;width:320px;text-align:right;font-family:var(--s);font-style:italic;font-size:38px;line-height:46px;color:#fff;'
                 f'text-shadow:0 2px 14px rgba(0,0,0,.6);z-index:6">{sp["side"]}</div>')
    P += [logo(top), pager(i, n, top)]
    if sp.get("link"): P.append(link(H - bot - 110))
    return P, H

def D_blank(sp, i, n, story=False):
    H, top, bot = geo(story)
    PY = int(H * .42); PHH = H - PY; S = 1.5
    base = K.cover(PH[sp["ph"]], W, PHH, fy=sp.get("fy", .45))
    punched = base.copy(); d = ImageDraw.Draw(punched)
    for (x, y, w, h) in sp["boxes"]:
        d.rectangle([x * S, y * S, (x + w) * S, (y + h) * S], fill=K.hexrgb(CREAM))
    P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0), f'<img src="{K.uri(punched)}" style="position:absolute;left:0;top:{PY}px;width:{W}px;height:{PHH}px;z-index:2">']
    thumbs = []
    for (x, y, w, h) in sp["boxes"]:
        crop = base.crop((round(x * S), round(y * S), round((x + w) * S), round((y + h) * S))); tw = round(64 * w / h)
        thumbs.append(f'<img src="{K.uri(crop)}" style="display:inline-block;vertical-align:middle;height:64px;width:{tw}px;object-fit:cover;margin:0 6px;border-radius:5px;border:2px solid #0A0A0A">')
    P.append(f'<div style="position:absolute;left:64px;top:{150+top}px;width:952px;text-align:center;font-family:var(--e);font-size:34px;line-height:86px;color:#0A0A0A;z-index:8">{sp["sentence"].format(*thumbs)}</div>')
    P += [K.logo(64, 48 + top), pager(i, n, top, INK)]
    if sp.get("link"): P.append(link(H - bot - 110))
    return P, H

def D_glass(sp, i, n, story=False):
    H, top, bot = geo(story)
    P = [f'<img src="{C.warm(PH[sp["ph"]], W, H, sp.get("fy", .45))}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">',
         K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(6,12,30,.55) 0%,rgba(6,12,30,.15) 35%,rgba(6,12,30,.1) 60%,rgba(6,12,30,.6));", z=2)]
    P.append(col_block([serif(sp["hl"], sp.get("hs", 104), "#F6EFD8", "text-shadow:0 3px 20px rgba(0,0,0,.4)")] + ([body(sp["ln"], "#F6EFD8", 28)] if sp.get("ln") else []), f"top:{150+top}px"))
    for (x, y, lab, c, rot, ic) in sp.get("pills", []):
        P.append(T3.pill(x, int(y * H / 1350), lab, c, rot, ic).replace("z-index:14", "z-index:70"))
    P += [logo(top), pager(i, n, top)]
    if sp.get("link"): P.append(link(H - bot - 110))
    return P, H

DEV = {"cast": D_cast, "note": D_note, "blank": D_blank, "glass": D_glass}

# ------------------------------------------------------------------ sample campaigns, peer voice
WHAT = [
    dict(D="cast", ph="artnook", fy=.5, hl="hi, we're <i>aquaterra.</i>", hs=104,
         ln="a few hundred kolkata students, 14 to 19, who spend weekends teaching, feeding, planting and generally showing up.",
         wins=[(150, 560, 300, 520, PINK, "THE KIDS : very loud", "tr"), (520, 520, 330, 560, LEM, "US : trying to keep up", "tl")]),
    dict(D="note", bg="teach_class", ph="teach_class", fy=.5, pre="most of what we do", chip="is teach.", side="workshops at shelters and community centres, every week."),
    dict(D="blank", ph="sharbat_stall", fy=.4, boxes=[(330, 120, 170, 200), (560, 300, 150, 260), (90, 360, 200, 220)],
         sentence="we hand out ( {0} ) sharbat on hot days, ( {1} ) biscuits to the strays and ( {2} ) saplings to the parks. mostly on weekends."),
    dict(D="glass", ph="sund1", fy=.4, hl="and sometimes we go <i>a bit further.</i>", hs=96,
         pills=[(64, 980, "the sundarbans", SKY, -3, "leaf"), (460, 1070, "health camps", MINT, 3, "heart"), (160, 1160, "medicines", LEM, -2, "plus")]),
    dict(D="cast", ph="green_talk", fy=.5, hl="we build things <i>too.</i>", hs=104,
         wins=[(60, 640, 440, 520, LEM, "SHIKSHAQ : free papers and tutors", "tr"), (560, 600, 460, 560, GRAPE, "TERRANOTES : our magazine", "tl")]),
    dict(D="note", bg="smile_notes", ph="smile_notes", fy=.45, pre="we're a registered", chip="ngo.", side="darpan-certified, if your parents ask."),
    dict(D="cast", ph="sharbat_cup", fy=.5, hl="all of it is <i>for someone else.</i>", hs=96, ln="come see what that looks like.", link=True,
         wins=[(220, 560, 640, 560, MINT, "ONE SHARBAT, ONE VERY HOT DAY", "tl")]),
]
ROUND = [
    dict(D="cast", ph="dog_bhowanipur", fy=.55, hl="one round of <i>tails and treats.</i>", hs=96, ln="we feed kolkata's strays. here's how a round goes.",
         wins=[(290, 720, 270, 400, MINT, "REGULAR", "tl"), (575, 720, 330, 400, LEM, "ALSO A REGULAR", "tr")]),
    dict(D="blank", ph="dog_biscuit", fy=.5, boxes=[(620, 300, 220, 200), (300, 280, 260, 300)],
         sentence="a bag of ( {0} ) biscuits, a bottle of water, and a route full of ( {1} ) dogs who already know the sound of the packet."),
    dict(D="glass", ph="cow_biscuit", fy=.5, hl="sometimes <i>a cow joins in.</i>", hs=104, pills=[(600, 1080, "nobody objects", LEM, -3, "heart")]),
    dict(D="note", bg="dog_night", ph="dog_night", fy=.5, pre="some rounds", chip="run late.", side="the dogs don't mind."),
    dict(D="cast", ph="street_dog", fy=.5, hl="next round's <i>soon.</i>", hs=110, ln="come along.", link=True, wins=[(560, 720, 420, 460, LEM, "THIS ONE'S WAITING", "tl")]),
]
SHIK = [
    dict(D="cast", ph="books", fy=.45, hl="exam season? <i>start with the papers.</i>", hs=92, ln="shikshaq has free past papers, study material and tutors for kolkata.",
         wins=[(260, 620, 560, 520, LEM, "FREE. ACTUALLY FREE.", "tl")]),
    dict(D="blank", ph="fable", fy=.5, boxes=[(80, 180, 240, 260), (560, 160, 220, 300)],
         sentence="free ( {0} ) past papers. free notes for your class. a tutor near you if you need one. ( {1} ) shikshaq.in"),
    dict(D="glass", ph="teach_board", fy=.4, hl="made for <i>your syllabus.</i>", hs=104,
         pills=[(64, 980, "class iv to xii", LEM, -3, "star"), (520, 1070, "icse · isc", SKY, 3, "sparkle"), (140, 1160, "cbse · state board", PINK, -2, "heart")]),
    dict(D="note", bg="stem4", ph="stem4", fy=.4, pal=["#2a1a00", "#5a3a00", "#8a6a10", "#c49a20", "#e6c450", "#f6efd8"], pre="built by aquaterra,", chip="for every student.", cc=LEM, cs=60),
    dict(D="cast", ph="stem3", fy=.35, hl="send it to someone <i>with boards this year.</i>", hs=88, link=True, wins=[(120, 640, 840, 520, LEM, "SHIKSHAQ.IN", "tl")]),
]
SETS = {"A_what": WHAT, "E_round": ROUND, "C_shik": SHIK}

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    async with K.B.session():
        for key, slides in SETS.items():
            n = len(slides)
            for i, sp in enumerate(slides, 1):
                P, H = DEV[sp["D"]](sp, i, n)
                await K._render(f"{key}_{i:02d}", K.page(V6.DEFS + "".join(P) + V6.grain(.32), H, bg=CREAM), H, None, None)
            for k, idx in enumerate([0, 1, n - 1], 1):
                P, H = DEV[slides[idx]["D"]](slides[idx], None, None, story=True)
                await K._render(f"{key}_story{k}", K.page(V6.DEFS + "".join(P) + V6.grain(.32), H, bg=CREAM), H, None, None)

if __name__ == "__main__":
    asyncio.run(main())
