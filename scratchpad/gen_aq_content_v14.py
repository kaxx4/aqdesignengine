"""AQ content v14: same four carousels, far less text, built from the owner's inspo mechanisms.

Owner (2026-11-13): "too much text, improve design looking at the inspo". Every slide now carries ONE headline (sans caps
mixed with a serif italic phrase) and the details move into the inspo devices instead of paragraphs:
  cast   colour windows with small tabs over the photo (moodboard reference)
  glass  full-bleed photo, glass pills carrying 2-3 word facts (CREATIE hero)
  note   frosted card with a framed photo and one highlighted word (the 'you are not alone' card)
  taped  taped prints on a colour ground (scrapbook)
  tiles  dithered photo tiles and colour blocks (website-page reference)
Facts as in v13 (platform log since April 2025, not stated on posts). Copy deck: brain/RECRUITMENT_COPY_DECK_V13.md.
"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recruit_kit as K
import gen_recruit_v6 as V6
import gen_recruit_v3 as T3
import gen_aq_content_v13 as C
core = K.core
W = 1080; H = 1350; INK, CREAM = K.INK, K.CREAM
PINK, MINT, LEM, TOM, SKY, GRAPE, TEAL = core.ACCENTS
OUT = "out/aq_content_v14"
PH = C.PH; LINK = C.LINK
warm = C.warm

def head(txt, size, color, anchor, w=952, z=60, align="left"):
    ss = round(size * .78)
    txt = txt.replace("<i>", f'<i style="font-family:var(--s);font-weight:400;text-transform:none;font-size:{size}px;letter-spacing:-.01em">')
    return (f'<div style="position:absolute;left:64px;{anchor};width:{w}px;text-align:{align};font-family:var(--d);font-weight:900;text-transform:uppercase;'
            f'font-size:{ss}px;line-height:{size}px;letter-spacing:-.01em;color:{color};z-index:{z}">{txt}</div>')

def kick(txt, color, anchor):
    return (f'<div style="position:absolute;left:64px;{anchor};font-family:var(--m);font-weight:700;font-size:19px;letter-spacing:.12em;color:{color};'
            f'text-transform:uppercase;z-index:60">{txt}</div>')

def chrome(i, n, dark=True, link=False, col="#F6EFD8"):
    out = [K.logo_pill(64, 44, dark=True), C.pager(i, n, col if dark else INK)]
    if link: out.append(C.linkline(64, H - 100))
    return out

def photo(path, fy=.45, mono=False):
    im = K.cover(path, W, H, fy=fy)
    if mono: im = K.mono(im, 1.1)
    return f'<img src="{K.uri(im)}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:1">'

# ---------------------------------------------------------------- the five devices
def L_cast(sp, i, n):
    P = [photo(PH[sp["ph"]], sp.get("fy", .45), mono=True)]
    for (x, y, w, h, c, lab, side) in sp["wins"]:
        P.append(V6.window(x, y, w, h, c, lab, side, z=6))
    P.append(K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(10,10,10,.85) 0%,rgba(10,10,10,.6) 28%,rgba(10,10,10,0) 46%);", z=4))
    if sp.get("kick"): P.append(kick(sp["kick"], "#F6EFD8", "top:150px"))
    P.append(head(sp["hl"], sp.get("hs", 100), "#F6EFD8", "top:190px"))
    return P + chrome(i, n, link=sp.get("link")), INK

def L_glass(sp, i, n):
    P = [photo(PH[sp["ph"]], sp.get("fy", .45)),
         K.box(0, 0, W, H, "background:linear-gradient(180deg,rgba(10,10,10,.72) 0%,rgba(10,10,10,.35) 30%,rgba(10,10,10,.05) 50%,rgba(10,10,10,.55));", z=2)]
    if sp.get("kick"): P.append(kick(sp["kick"], "#F6EFD8", "top:150px"))
    P.append(head(sp["hl"], sp.get("hs", 110), "#F6EFD8", "top:190px"))
    for (x, y, lab, col, rot, ic) in sp.get("pills", []):
        P.append(T3.pill(x, y, lab, col, rot, ic).replace("z-index:14", "z-index:70"))
    return P + chrome(i, n, link=sp.get("link")), INK

def L_note(sp, i, n):
    pal = sp.get("pal", ["#0d2413", "#17391c", "#245a24", "#3f7a2a", "#7a9a35", "#b9b04a", "#e6dca0"])
    bg = K.posterise(K.cover(PH[sp["bg"]], W, H, fy=sp.get("bfy", .45)), pal, blur=5)
    P = [f'<img src="{K.uri(bg, "PNG")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;z-index:1">', V6.halftone_over(W, H, 2, .08)]
    cx, cy, cw = 64, 300, 620
    P.append(K.box(cx, cy, cw, 820, "background:rgba(244,239,224,.66);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border:3px solid rgba(255,255,255,.85);", z=4))
    P.append(f'<img src="{warm(PH[sp["ph"]], cw-56, 470, sp.get("fy", .45))}" style="position:absolute;left:{cx+28}px;top:{cy+28}px;width:{cw-56}px;height:470px;object-fit:cover;border:3px solid #fff;z-index:5">')
    P.append(f'<div style="position:absolute;left:{cx+28}px;top:{cy+530}px;font-family:var(--e);font-size:38px;color:#0A0A0A;z-index:6">{sp["pre"]}</div>')
    P.append(f'<div style="position:absolute;left:{cx+28}px;top:{cy+590}px;padding:2px 20px 8px;background:{sp.get("chipcol", SKY)};font-family:var(--e);font-weight:600;'
             f'font-size:{sp.get("cs", 76)}px;line-height:{sp.get("cs", 76)+10}px;color:#0A0A0A;z-index:6">{sp["chip"]}</div>')
    if sp.get("side"):
        P.append(f'<div style="position:absolute;left:720px;top:330px;width:300px;text-align:right;font-family:var(--s);font-style:italic;font-size:40px;line-height:46px;color:#fff;'
                 f'text-shadow:0 2px 14px rgba(0,0,0,.6);z-index:6">{sp["side"]}</div>')
    return P + chrome(i, n, link=sp.get("link")), INK

def L_taped(sp, i, n):
    col = sp.get("col", MINT); fg = core.text_on(col) if col != INK else "#F6EFD8"
    P = [K.box(0, 0, W, H, f"background:{col};", z=0)]
    spots = sp.get("spots", [(70, 560, 470, 560, -5), (520, 600, 480, 600, 4)])
    for j, (x, y, w, h, r) in enumerate(spots):
        P.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w+28}px;height:{h+28}px;transform:rotate({r}deg);background:#FBF8EE;padding:14px;'
                 f'box-shadow:9px 10px 0 rgba(10,10,10,.85);z-index:{10+j}"><img src="{warm(PH[sp["phs"][j]], w, h, .45)}" style="width:{w}px;height:{h}px;object-fit:cover;display:block"></div>')
        P.append(V6.tape(x + w // 2 - 60, y - 18, 130, 42, r * 2, seed=40 + j, z=30))
    if sp.get("kick"): P.append(kick(sp["kick"], fg, "top:150px"))
    P.append(head(sp["hl"], sp.get("hs", 104), fg, "top:190px"))
    if sp.get("tag"):
        P.append(f'<div style="position:absolute;left:{sp.get("tx", 640)}px;top:{sp.get("ty", 1180)}px;transform:rotate(-3deg);font-family:var(--s);font-style:italic;'
                 f'font-size:52px;color:{fg};z-index:40">{sp["tag"]}</div>')
    return P + chrome(i, n, dark=True, link=sp.get("link"), col=fg), col

def L_tiles(sp, i, n):
    P = [K.box(0, 0, W, H, f"background:{CREAM};", z=0)]
    tw, th = W // 3, H // 4; k = 0; cols = sp.get("cols", [MINT, SKY, LEM, PINK, TOM, GRAPE])
    for r in range(4):
        for c in range(3):
            x, y = c * tw, r * th
            if (r + c) % 2 == 0:
                im = K.dither(K.cover(PH[sp["phs"][k % len(sp["phs"])]], tw, th, fy=.4, s=1.4), cols[(r + c) % len(cols)], cell=5); k += 1
                P.append(f'<img src="{K.uri(im, "PNG")}" style="position:absolute;left:{x}px;top:{y}px;width:{tw}px;height:{th}px;z-index:1">')
            else:
                P.append(K.box(x, y, tw, th, f"background:{cols[(r*3+c) % len(cols)]};", z=1))
    inner = head(sp["hl"], sp.get("hs", 104), INK, "top:0", w=920, z=30).replace("position:absolute;left:64px;top:0;", "position:relative;")
    P.append(f'<div style="position:absolute;left:40px;top:{sp.get("by", 480)}px;width:1000px;padding:40px 40px 48px;background:#F6EFD8;border:4px solid #0A0A0A;'
             f'box-shadow:10px 11px 0 #0A0A0A;z-index:20">{inner}</div>')
    return P + chrome(i, n, link=sp.get("link")), CREAM

LAY = {"cast": L_cast, "glass": L_glass, "note": L_note, "taped": L_taped, "tiles": L_tiles}

# ---------------------------------------------------------------- carousels (one line each)
W_RECAP = [
    dict(L="glass", ph="sund1", fy=.4, kick="2025 to 2026", hl="The last<br>two years,<br><i>on the ground.</i>", hs=118),
    dict(L="tiles", phs=["chess1", "stem3", "dog_bhowanipur", "plant", "rakhi", "sund3"], hl="158 drives,<br>workshops<br><i>and visits.</i>", hs=118, by=430),
    dict(L="cast", ph="stem3", fy=.35, kick="teaching", hl="Mostly,<br><i>we taught.</i>", hs=120,
         wins=[(80, 700, 260, 420, TOM, "PUBLIC SPEAKING", "tr"), (380, 640, 300, 420, LEM, "CHESS", "tr"), (720, 700, 290, 420, SKY, "STEM", "tl")]),
    dict(L="glass", ph="chess4", fy=.5, hl="About 2,000<br><i>children.</i>", hs=124,
         pills=[(64, 1040, "45 workshops", TOM, -3, "star"), (520, 1130, "Pather Sathi", MINT, 3, "heart")]),
    dict(L="cast", ph="dog_bhowanipur", fy=.5, kick="animal welfare", hl="And<br><i>the dogs.</i>", hs=130,
         wins=[(290, 720, 270, 400, MINT, "25 ROUNDS", "tl"), (575, 720, 330, 400, LEM, "STILL HUNGRY", "tr")]),
    dict(L="taped", col=MINT, phs=["plant", "books"], hl="Books, clothes,<br>saplings,<br><i>sharbat.</i>", hs=104, spots=[(70, 640, 440, 520, -5), (540, 690, 440, 520, 4)]),
    dict(L="note", bg="sund4", ph="sund3", fy=.4, pre="And in December,", chip="further.", side="Sunderbans 8.0. 120+ checkups."),
    dict(L="glass", ph="rakhi", fy=.5, hl="Never<br><i>on our own.</i>", hs=124,
         pills=[(64, 1020, "BSS School", PINK, -3, "heart"), (430, 1110, "AIM Foundation", SKY, 3, "star"), (120, 1190, "Science City", LEM, -2, "sparkle")]),
    dict(L="taped", col=INK, phs=["stem3", "sund2"], hl="All of it run<br>by <i>people your age.</i>", hs=96, spots=[(70, 620, 440, 540, -4), (540, 660, 440, 540, 5)]),
    dict(L="glass", ph="stem4", fy=.4, hl="Next year<br><i>starts now.</i>", hs=124, link=True),
]

E_OPP = [
    dict(L="glass", ph="sund2", fy=.4, kick="aquaterra, kolkata", hl="What you'd<br>actually<br><i>be doing here.</i>", hs=112),
    dict(L="tiles", phs=["magic", "chess1", "stem2", "onceupon", "artnook", "mult"], hl="Most of what<br>we do<br><i>is teach.</i>", hs=118, by=430),
    dict(L="cast", ph="stem2", fy=.45, kick="teaching", hl="Plan it.<br><i>Teach it.</i>", hs=124,
         wins=[(60, 680, 420, 520, TOM, "THE LESSON", "tr"), (520, 760, 480, 440, LEM, "THE ROOM", "tl")]),
    dict(L="note", bg="chess1", ph="draw", fy=.4, pal=["#2a1a00", "#5a3a00", "#8a6a10", "#c49a20", "#e6c450", "#f6efd8"], pre="ShikshAQ:", chip="free learning.", chipcol=LEM, cs=66, side="Papers, notes and tutors, for anyone in Kolkata."),
    dict(L="cast", ph="plant", fy=.4, kick="welfare", hl="The city,<br><i>one drive at a time.</i>", hs=104,
         wins=[(70, 720, 520, 520, MINT, "GROW GREEN", "tr")]),
    dict(L="glass", ph="sund4", fy=.35, kick="the sundarbans", hl="And sometimes,<br><i>much further.</i>", hs=104),
    dict(L="glass", ph="rakhi", fy=.5, kick="collabs", hl="Nothing here<br><i>happens alone.</i>", hs=108,
         pills=[(64, 1060, "Schools", PINK, -3, "heart"), (380, 1140, "Colleges", SKY, 3, "star"), (700, 1060, "NGOs", LEM, -2, "sparkle")]),
    dict(L="taped", col=GRAPE, phs=["blog_city", "blog_mirror"], kick="terranotes", hl="Our monthly<br><i>magazine.</i>", hs=110, tag="no AI. ever.", tx=600, ty=1210),
    dict(L="glass", ph="dd_floor_green", fy=.4, kick="events", hl="The nights that<br><i>pay for the rest.</i>", hs=100),
    dict(L="taped", col=TEAL, phs=["desk", "dd_group"], kick="social, hr", hl="Telling it.<br><i>Keeping it together.</i>", hs=96, spots=[(70, 650, 440, 520, -5), (540, 690, 440, 520, 4)]),
    dict(L="tiles", phs=["sund1", "stem4", "dog_bhowanipur", "plant", "chess4", "rakhi"], hl="Start<br><i>anywhere.</i>", hs=140, by=470, link=True),
]

S_SHIK = [
    dict(L="glass", ph="chess1", fy=.45, kick="shikshaq", hl="Free learning,<br><i>for anyone.</i>", hs=118),
    dict(L="note", bg="mult", ph="mult", fy=.35, pal=["#2a1a00", "#5a3a00", "#8a6a10", "#c49a20", "#e6c450", "#f6efd8"], pre="A good tutor, without", chip="knowing someone.", chipcol=LEM, cs=60),
    dict(L="taped", col=SKY, phs=["draw", "chess1"], kick="papers and notes", hl="Practice<br><i>costs nothing.</i>", hs=110),
    dict(L="glass", ph="stem1", fy=.5, hl="For<br><i>Kolkata.</i>", hs=140,
         pills=[(64, 1000, "Class IV to XII", LEM, -3, "star"), (560, 1080, "ICSE · ISC", SKY, 3, "sparkle"), (120, 1170, "CBSE · State", PINK, -2, "heart")]),
    dict(L="cast", ph="stem2", fy=.45, hl="Built<br><i>inside AQ.</i>", hs=130, wins=[(60, 700, 900, 480, LEM, "OUTREACH · TEACHERS · PAPERS · THE SITE", "tl")]),
    dict(L="taped", col=INK, phs=["stem4", "chess4"], hl="Use it. Share it.<br><i>Help build it.</i>", hs=100, link=True),
]

T_DOGS = [
    dict(L="glass", ph="dog_bhowanipur", fy=.55, kick="animal welfare", hl="Tails<br><i>and Treats.</i>", hs=130),
    dict(L="cast", ph="dog_biscuit", fy=.5, hl="Biscuits.<br><i>Water. Repeat.</i>", hs=118, wins=[(300, 700, 560, 480, LEM, "EVERY DOG ON THE ROUTE", "tl")]),
    dict(L="taped", col=MINT, phs=["cow_biscuit", "dog_saltlake"], hl="25 rounds<br><i>in two years.</i>", hs=112),
    dict(L="glass", ph="dog_night", fy=.5, hl="Some rounds<br><i>run after dark.</i>", hs=110),
    dict(L="note", bg="street_dog", ph="dog_biscuit", fy=.5, pre="They know the sound", chip="of the packet.", chipcol=LEM, cs=66),
    dict(L="taped", col=LEM, phs=["street_dog", "dog_night"], hl="Come on<br><i>the next round.</i>", hs=110, link=True),
]

async def render_set(prefix, slides):
    n = len(slides)
    for i, sp in enumerate(slides, 1):
        P, bg = LAY[sp["L"]](sp, i, n)
        html = K.page(V6.DEFS + "".join(P) + V6.grain(.3), H, bg=bg)
        await K._render(f"{prefix}{i:02d}", html, H, None, None)

async def main():
    os.makedirs(OUT, exist_ok=True); K.OUT = OUT
    only = set(sys.argv[1:])
    async with K.B.session():
        for k, s in (("W", W_RECAP), ("E", E_OPP), ("S", S_SHIK), ("T", T_DOGS)):
            if not only or k in only: await render_set(k, s)

if __name__ == "__main__":
    asyncio.run(main())
