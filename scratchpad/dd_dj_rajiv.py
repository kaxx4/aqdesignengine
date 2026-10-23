"""DISCO DIWALI DJ LAUNCH poster, DJ RAJIV, feed 1080x1350. Bespoke script on the discodiwali.py primitives (no registered kind yet).

Brief (user, 2026-10-23): "a DJ launch static poster for Disco Diwali, use Disco Diwali branding". Supplied: Rajiv's photos, his RAJIV wordmark (zip of 5 logos) and his
2025 press kit (PDF). Photo chosen for marketing: the cream-jacket "collar hold" frame, because its cream and brown reads as the copper/gold of the format, the face is frontal
and centred, and the wall is dark enough to grade into the ink ground. Studio photos are flat (no cutout), so he is NOT placed in front of the logo: the photo is full bleed,
faded into ink from the chest down, and the wordmark sits in the faded zone beside the type.

Skeleton, back to front: ink, photo graded navy, diya plate SCREEN-blended (corners only), a fade to ink, gold dust, film grain, LIVE badge top left, the DISCO DIWALI
lockup (with ball) top right, the RAJIV wordmark (off-white) bottom left, the type stack bottom right.

Adaptations (CLAUDE.md sec 2 ladder): ink ground and off-white type are the FORMAT's palette, not core.ACCENTS. The wordmark is recoloured from the artist's red to the format's
off-white (his red file is kept as logo_red_clean.png). The reference poster's bio paragraph, monthly-listeners stat, sponsor logos and address are NOT reproduced. The stat slot
is filled from the press kit: "500+ shows across 100+ nightclubs" (his own kit, self-reported: attribute it as his claim, truth ladder in VOICE.md). Age (21 in the 2025 kit),
contact details, other artists' names and the concert photos (Zomato branding) are deliberately left off. "ON THE DECKS" is the eyebrow in place of KNOW YOUR ARTIST.
Facts printed: DJ Rajiv, Masquerade Sangeet Edition, 10th November 2026, 4:30 PM onwards, link in bio. No venue, price or lineup.
Photo rights: a studio portrait supplied for this launch; confirm usage rights before posting.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_dj_rajiv.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "dj_rajiv")
VER = os.environ.get("VER", "v1")
STROKE = "color:#fff;-webkit-text-stroke:3px #000;paint-order:stroke fill;"
GOLD_LIT = "#E8C063"
FUN = os.environ.get("FUN", "1") == "1"                # v4 (user, 2026-10-23: "make the poster fun and engaging"): FUN=0 reproduces v3
LIGHTS = os.environ.get("LIGHTS", "1" if FUN else "0") == "1"
FOIL = ("linear-gradient(180deg,#FFF6CF 0%,#F0C65A 34%,#A8721A 60%,#F7DC86 82%,#C48A22 100%)")   # same gold as Poster.FOIL
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PHOTO = os.path.join(ROOT, "engine", "assets", "disco_diwali", "dj_rajiv", "photo_collar.jpg")


def build():
    P, els = [], []
    P.append(f'<img data-tag="plate" src="{dd.photo_uri(PHOTO, 1800)}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;object-position:50% 0;'
             'z-index:1;filter:contrast(1.1) saturate(1.08) brightness(1.06)">')
    # v3 (user, 2026-10-23: "remove the shadow and shade"): no navy multiply, no top scrim, no logo drop shadow. The photo shows as shot.
    # the diya plate lives AROUND him, never on him: a radial mask clears his head and shoulders (v1 printed lotuses across his forehead and sunglasses)
    face_mask = "radial-gradient(ellipse 36% 31% at 52% 27%,transparent 0%,transparent 78%,#000 100%)"
    P.append(f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;object-fit:cover;z-index:3;mix-blend-mode:screen;opacity:.8;pointer-events:none;'
             f'-webkit-mask-image:{face_mask};mask-image:{face_mask}">')
    # the fade: clear over the face and shoulders, solid ink where the wordmark and type sit
    P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:4;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0) 56%,'
             'rgba(0,0,0,.78) 68%,#000 80%)"></div>')
    if LIGHTS:
        # the string sags straight across a centred head (v4 first pass put bulbs on his sunglasses), so clear a transparent ellipse over the head: lights hang either side of him
        # mask coordinates are in the LIGHTS IMAGE's own box (1045x346 at canvas 160,-53), not the canvas: head centre canvas (562,247) -> image (402,300)
        lm = "radial-gradient(ellipse 300px 215px at 402px 300px,transparent 0%,transparent 92%,#000 100%)"
        P.append(f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5;-webkit-mask-image:{lm};mask-image:{lm}">')
    P.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.5;pointer-events:none">'
             f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')

    # LIVE badge, top left (same size and place as the carousel posters)
    bx, by, bw = 40, 40, 150
    P.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">')
    els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))

    # the DISCO DIWALI lockup, with its ball, top right. Visible outline = 1717x991 inside the 2000x1382 asset at (265, 320)
    vw = 270; t = vw / 1717; vh = round(991 * t); vx = 1040 - vw; vy = 58
    P.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:20">')
    els.append(("title", vx, vy, vw, vh))

    # RAJIV wordmark, bottom left
    lw = 340; lx = 64; ly = 902
    P.append(f'<img data-tag="logo" src="{dd.uri("dj_rajiv/logo_offwhite.png")}" style="position:absolute;left:{lx}px;top:{ly}px;width:{lw}px;height:{lw}px;z-index:20">')
    els.append(("logo", lx, ly, lw, lw))

    # type stack, bottom right, left aligned on one edge
    cx, cw = 462, 556
    def line(tag, txt, top, size, weight, h, css=""):
        P.append(f'<div data-tag="{tag}" style="position:absolute;left:{cx}px;top:{top}px;width:{cw}px;white-space:nowrap;font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                 f'line-height:1;text-transform:uppercase;{STROKE}{css}z-index:20">{txt}</div>')
        els.append((tag, cx, top, cw, h))
    line("eyebrow", "On the decks", 858, 30, 600, 32, f"letter-spacing:.32em;color:{GOLD_LIT};-webkit-text-stroke:0;")
    if FUN:   # v4: DJ in white, RAJIV in gold foil, the whole name tilted up to the right (rotate about the left baseline, so only the right end lifts)
        P.append(f'<div data-tag="name" style="position:absolute;left:{cx}px;top:908px;width:{cw}px;white-space:nowrap;font-family:var(--d);font-weight:700;font-size:100px;line-height:1;'
                 f'text-transform:uppercase;color:#fff;transform:rotate(-3deg);transform-origin:0 100%;z-index:20">DJ <span style="background:{FOIL};-webkit-background-clip:text;background-clip:text;'
                 f'-webkit-text-fill-color:transparent;color:transparent">Rajiv</span></div>')
        els.append(("name", cx, 880, cw, 128))
    else:
        line("name", "DJ Rajiv", 898, 100, 700, 100)
    line("stat", "500+ shows &middot; 100+ nightclubs", 1012, 28, 600, 30, f"color:{GOLD_LIT};-webkit-text-stroke:0;")
    line("edition", "Masquerade Sangeet Edition", 1060, 31, 600, 34)
    line("date", "10th November, 2026", 1104, 44, 700, 46)
    line("time", "4:30 PM onwards", 1156, 36, 400, 38)
    pill = (f'<div data-tag="linkpill" style="position:absolute;left:{cx}px;top:1206px;width:300px;height:60px;border-radius:18px;border:2px solid rgba(222,180,100,.7);'
            'background:rgba(236,200,150,.16);z-index:20;display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:600;font-size:28px;'
            'line-height:1;text-transform:uppercase;color:#fff">Link in bio</div>')
    P.append(pill); els.append(("linkpill", cx, 1206, 300, 60))
    if FUN:
        # stickers, NO drop shadow (user, 2026-10-23: "remove the shadow and shade"), tilted, in the free wall either side of his head.
        # Default: the DJ set drawn for this poster (dd_dj_stickers.py, user: "make your own stickers and use them"). STICKERS=copper restores the earlier copper stars and heart.
        if os.environ.get("STICKERS", "own") == "copper":
            import dd_copper as cp
            spec = (("star1", cp.star, 70, 300, 170, -12, 170), ("heart", cp.heart, 836, 396, 196, 12, 176), ("star2", cp.star, 930, 770, 92, 16, 92))
            mk = lambda fn, size, rot, tag: fn(size, rot, u=tag, shadow=False)
        else:
            import dd_dj_stickers as st
            spec = (("headphones", st.headphones, 52, 292, 210, -12, 210), ("bolt", st.bolt, 262, 520, 128, 10, 128),
                    ("vinyl", st.vinyl, 826, 372, 214, 12, 214), ("notes", st.notes, 922, 750, 98, 14, 98))
            mk = lambda fn, size, rot, tag: fn(size, rot, u=tag)
        for tag, fn, x, y, size, rot, h in spec:
            P.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;z-index:15">{mk(fn, size, rot, tag)}</div>'); els.append((tag, x, y, size, h))
        # two lowercase chips (VOICE.md: events recap, general followers, loud and playful, 2 chips). Only claims already supplied: it is for charity, it is a dance floor
        chip = ("font-family:var(--e);font-weight:600;font-size:30px;line-height:1;white-space:nowrap;color:#0A0A0A;padding:15px 26px;border-radius:999px;z-index:16;")
        P.append(f'<div data-tag="chip1" style="position:absolute;left:64px;top:722px;{chip}background:#F2F2F2;transform:rotate(-5deg)">the dance floor has been warned</div>'); els.append(("chip1", 64, 700, 526, 105))
        P.append(f'<div data-tag="chip2" style="position:absolute;left:730px;top:668px;{chip}background:{FOIL};transform:rotate(5deg)">dance for a cause</div>'); els.append(("chip2", 730, 654, 310, 90))
    return "".join(P), els, 1266


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, bottom = build()
    print(f"[feed] last element ends at y={bottom} of {H}")
    text_pairs = [("name", "#FFFFFF", "#000000", 100, True), ("date", "#FFFFFF", "#000000", 44, True), ("time", "#FFFFFF", "#000000", 36, False),
                  ("edition", "#FFFFFF", "#000000", 31, True), ("eyebrow", GOLD_LIT, "#000000", 30, True), ("stat", GOLD_LIT, "#000000", 28, True)]
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{VER}.png"), W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                       page_bg="#000", collision_ignore=[], text_pairs=text_pairs)
    print("dj_rajiv done ->", OUT)
asyncio.run(main())
