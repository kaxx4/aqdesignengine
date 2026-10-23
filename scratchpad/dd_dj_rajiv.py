"""DISCO DIWALI DJ LAUNCH poster, DJ RAJIV: feed 1080x1350 and story 1080x1920 from one build(H). Bespoke script on the discodiwali.py primitives (no registered kind yet).

Brief (user, 2026-10-23): "a DJ launch static poster for Disco Diwali, use Disco Diwali branding", then "make a story version too". Supplied: Rajiv's photos, his RAJIV wordmark (zip of 5 logos) and
his 2025 press kit (PDF). Photo chosen for marketing: the cream-jacket "collar hold" frame (cream and brown match the copper and gold; frontal, centred face). The studio photos are flat (no
cutout), so the name is NOT behind him: the photo is full bleed, UNGRADED (user: "remove the shadow and shade"), with a short ink fade from the chest down so the type reads.

Skeleton, back to front: ink, photo, diya plate SCREEN-blended around him (a transparent ellipse over his head), the ink fade, gold dust, film grain, LIVE badge, the DISCO DIWALI lockup (with ball),
two copper stickers as a MIRRORED PAIR either side of his head (headphones, vinyl: dd_dj_copper.py, the mask's own photographed surface, no shadow), two lowercase chips, the RAJIV wordmark (off-white)
and the type stack: "ON THE DECKS", DJ in white and RAJIV in gold foil (tilted -3 degrees), the stat, the edition line, the date and the time.

STORY (H > 1350) follows the format's story rules (brain/DISCO_DIWALI.md): nothing in Instagram's top 200px, NO link pill (a link sticker goes there), so a small LINK IN BIO cue sits above a reserved
`linkzone` (640x165 at y=1505) that nothing enters, and the bottom 250px stays empty. The photo is cropped to 9:16 around his face (object-position 62%), the type stack is scaled 1.18x (a story is read at
a third of a feed's size) and anchored so it ends above the cue, and the stickers and chips are re-placed against the new face position rather than scaled.

Adaptations (CLAUDE.md sec 2 ladder): ink ground and off-white type are the FORMAT's palette, not core.ACCENTS. The wordmark is recoloured from the artist's red to off-white (logo_red_clean.png keeps it).
The reference poster's bio paragraph, monthly-listeners stat, sponsor logos and address are NOT reproduced. The stat slot carries "500+ shows . 100+ nightclubs" from his own 2025 press kit (self-reported:
attribute it). Left off on purpose: his age, contact details, other artists' names, the kit's concert photos (Zomato branding). Facts printed: DJ Rajiv, Masquerade Sangeet Edition, 10th November 2026,
4:30 PM onwards, link in bio. No venue, price or lineup. Photo rights: confirm before posting.
Earlier experiments (navy grade, string lights, copper mask/heart/stars, a flat gold DJ sticker set, ball/bolt/notes) were dropped by the user's decisions; they live in git history and brain/DISCO_DIWALI.md.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_dj_rajiv.py   (VER=v13 names the output)"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_dj_copper as cd
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "dj_rajiv")
VER = os.environ.get("VER", "v1")
STROKE = "color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke fill;"
GOLD_LIT = "#E8C063"
FOIL = "linear-gradient(180deg,#FFF6CF 0%,#F0C65A 34%,#A8721A 60%,#F7DC86 82%,#C48A22 100%)"   # same gold as Poster.FOIL
PHOTO = os.path.join(ROOT, "engine", "assets", "disco_diwali", "dj_rajiv", "photo_collar.jpg")


def build(H):
    story = H > 1350
    P, els = [], []
    # ---- ground: photo, plate around him, fade, dust, grain (every layer tagged plate: deliberate full bleed)
    P.append(f'<img data-tag="plate" src="{dd.photo_uri(PHOTO, 1800)}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;object-position:{"62%" if story else "50%"} 0;'
             'z-index:1;filter:contrast(1.1) saturate(1.08) brightness(1.06)">')
    # the plate lives AROUND him, never on him (v1 printed lotuses across his forehead); a story's head sits lower and the box is taller, so the ellipse is in px
    face_mask = ("radial-gradient(ellipse 340px 360px at 540px 430px,transparent 0%,transparent 78%,#000 100%)" if story
                 else "radial-gradient(ellipse 36% 31% at 52% 27%,transparent 0%,transparent 78%,#000 100%)")
    P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{1350 if story else H}px;object-fit:cover;z-index:3;mix-blend-mode:screen;opacity:.8;pointer-events:none;'
             f'-webkit-mask-image:{face_mask};mask-image:{face_mask}">')
    # a story's fade is longer so the jacket does not meet the black in a hard line (v13 showed a seam across the right shoulder), but it still reaches near-solid by the stack's top (y 1040 = 54%)
    fade = ("linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 40%,rgba(0,0,0,.5) 48%,rgba(0,0,0,.9) 55%,#000 61%)" if story
            else "linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 56%,rgba(0,0,0,.78) 68%,#000 80%)")
    P.append(f'<div data-tag="plate" style="position:absolute;inset:0;z-index:4;pointer-events:none;background:{fade}"></div>')
    if story:
        # format rule 8 (brain/DISCO_DIWALI.md): a taller canvas stacks a SECOND diya plate, flipped and faded in from the bottom edge, so the lower corners carry the pattern instead of a dead black block.
        # It sits ABOVE the fade (z 5; the fade is solid black down there and would hide it) and below all type; its centre is black, so the link zone stays clear.
        flip = "-webkit-mask-image:linear-gradient(to top,transparent 0%,#000 45%);mask-image:linear-gradient(to top,transparent 0%,#000 45%);"
        P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:{H - 1350}px;width:{W}px;height:1350px;object-fit:cover;z-index:5;'
                 f'mix-blend-mode:screen;opacity:.75;pointer-events:none;transform:scaleY(-1);{flip}">')
    P.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.5;pointer-events:none">'
             f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')

    # ---- LIVE badge top left, the lockup (with ball) top right; a story keeps both clear of Instagram's top 200px
    bx, by, bw = 40, 210 if story else 40, 150
    P.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">')
    els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    vw = 250 if story else 270                              # visible outline = 1717x991 inside the 2000x1382 asset at (265, 320)
    t = vw / 1717; vh = round(991 * t); vx = 1040 - vw; vy = 226 if story else 58
    P.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:20">')
    els.append(("title", vx, vy, vw, vh))

    # ---- stickers: a mirrored pair either side of his head (user: "too many stickers randomly placed"), no shadow
    ss, sy = (230, 450) if story else (220, 330)
    for tag, fn, cxm, rot in (("headphones", cd.headphones, 540 - 385, -10), ("vinyl", cd.vinyl, 540 + 385, 10)):
        x = cxm - ss // 2
        P.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{sy}px;z-index:15">{fn(ss, rot, u=tag)}</div>'); els.append((tag, x, sy, ss, ss))
    # ---- two lowercase chips (VOICE.md: events recap, general followers, 2 chips); only supplied claims
    chip = "font-family:var(--e);font-weight:600;font-size:30px;line-height:1;white-space:nowrap;color:#0A0A0A;padding:15px 26px;border-radius:999px;z-index:16;"
    c1x, c1y, c2x, c2y = (40, 770, 730, 706) if story else (64, 722, 730, 668)
    P.append(f'<div data-tag="chip1" style="position:absolute;left:{c1x}px;top:{c1y}px;{chip}background:#F2F2F2;transform:rotate(-5deg)">the dance floor has been warned</div>'); els.append(("chip1", c1x, c1y - 22, 526, 105))
    P.append(f'<div data-tag="chip2" style="position:absolute;left:{c2x}px;top:{c2y}px;{chip}background:{FOIL};transform:rotate(5deg)">dance for a cause</div>'); els.append(("chip2", c2x, c2y - 14, 310, 90))

    # ---- RAJIV wordmark (left) and the type stack (right). A story scales the stack 1.18x and anchors it so it ENDS above the link cue.
    k = 1.18 if story else 1.0
    T = 1040 if story else 858                              # stack top
    lw, lx = (300, 40) if story else (340, 64)
    cx = 372 if story else 462
    cw = 1040 - cx if story else 556
    ly = (T + round(397 / 2) - lw // 2) if story else 902
    P.append(f'<img data-tag="logo" src="{dd.uri("dj_rajiv/logo_offwhite.png")}" style="position:absolute;left:{lx}px;top:{ly}px;width:{lw}px;height:{lw}px;z-index:20">')
    els.append(("logo", lx, ly, lw, lw))
    def line(tag, txt, off, size, weight, h, css=""):
        top = T + round(off * k); size = round(size * k); h = round(h * k)
        P.append(f'<div data-tag="{tag}" style="position:absolute;left:{cx}px;top:{top}px;width:{cw}px;white-space:nowrap;font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                 f'line-height:1;text-transform:uppercase;{STROKE}{css}z-index:20">{txt}</div>')
        els.append((tag, cx, top, cw, h))
    line("eyebrow", "On the decks", 0, 30, 600, 32, f"letter-spacing:.32em;color:{GOLD_LIT};-webkit-text-stroke:0;")
    ntop, nsize = T + round(50 * k), round(100 * k)         # DJ in white, RAJIV in gold foil, tilted up to the right about the left baseline
    P.append(f'<div data-tag="name" style="position:absolute;left:{cx}px;top:{ntop}px;width:{cw}px;white-space:nowrap;font-family:var(--d);font-weight:700;font-size:{nsize}px;line-height:1;'
             f'text-transform:uppercase;color:#fff;transform:rotate(-3deg);transform-origin:0 100%;z-index:20">DJ <span style="background:{FOIL};-webkit-background-clip:text;background-clip:text;'
             f'-webkit-text-fill-color:transparent;color:transparent">Rajiv</span></div>')
    els.append(("name", cx, ntop - round(28 * k), cw, round(128 * k)))
    line("stat", "500+ shows &middot; 100+ nightclubs", 154, 28, 600, 30, f"color:{GOLD_LIT};-webkit-text-stroke:0;")
    line("edition", "Masquerade Sangeet Edition", 202, 31, 600, 34)
    line("date", "10th November, 2026", 246, 44, 700, 46)
    line("time", "4:30 PM onwards", 298, 36, 400, 38)
    if story:
        # no pill on a story: the link sticker goes in the reserved zone, with a small cue above it (story_launch's own cue); the top 200px and bottom 250px stay clear
        P.append(f'<div data-tag="cue" style="position:absolute;left:0;width:{W}px;top:1462px;text-align:center;white-space:nowrap;font-family:var(--m);font-weight:700;font-size:24px;line-height:1;'
                 f'letter-spacing:.3em;color:{GOLD_LIT};text-shadow:none;z-index:20">&darr;&nbsp;&nbsp;LINK IN BIO&nbsp;&nbsp;&darr;</div>')
        els.append(("cue", 270, 1462, 540, 28))
        els.append(("linkzone", (W - 640) // 2, 1505, 640, 165))
        bottom = 1505 + 165
    else:
        P.append(f'<div data-tag="linkpill" style="position:absolute;left:{cx}px;top:1206px;width:300px;height:60px;border-radius:18px;border:2px solid rgba(222,180,100,.7);'
                 'background:rgba(236,200,150,.16);z-index:20;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:600;font-size:28px;'
                 'line-height:1;text-transform:uppercase;color:#fff">Link in bio</div>')
        els.append(("linkpill", cx, 1206, 300, 60))
        bottom = 1266
    text_pairs = [("name", "#FFFFFF", "#000000", nsize, True), ("date", "#FFFFFF", "#000000", round(44 * k), True), ("time", "#FFFFFF", "#000000", round(36 * k), False),
                  ("edition", "#FFFFFF", "#000000", round(31 * k), True), ("eyebrow", GOLD_LIT, "#000000", round(30 * k), True), ("stat", GOLD_LIT, "#000000", round(28 * k), True)]
    return "".join(P), els, bottom, text_pairs


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for H, suffix in ((1350, ""), (1920, "_story")):
            inner, els, bottom, text_pairs = build(H)
            print(f"[{'story' if H > 1350 else 'feed'}] last element ends at y={bottom} of {H}")
            await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{VER}{suffix}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                           page_bg="#000", collision_ignore=[], text_pairs=text_pairs)
    print("dj_rajiv done ->", OUT)
asyncio.run(main())
