"""DISCO DIWALI "DJ reveal" carousel, 5 slides, feed (1080x1350) and story (1080x1920).

User brief (2026-10-20): "make a carousel for dj reveal. keep the same bg and use diff pics, use more stickers and the previous posts are becoming monotonous." Answers: the DJ's
name stays HIDDEN (a tease: nothing is printed that was not supplied, and no DJ name or handle was), event photos only, 5 slides ending on LINK IN BIO.

Same background recipe as the other carousel (dd_photo_bg.photo_ground: dark event photo, navy scrim, string lights, gold dust, grain), a DIFFERENT event photo per slide, and a
DIFFERENT layout per slide so the set stops repeating one skeleton: 1 centred headline over a big vinyl, 2 left-aligned headline with a huge speaker, 3 a glass card of question marks,
4 a tilted TURN IT UP wall of stickers, 5 the link slide. New copper stickers (vinyl, headphones, note, speaker, bolt) live in dd_copper.py; heart and star are reused sparingly.
Copy is the user's brief expressed as hype, never a claim: WHO'S ON THE DECKS? / WHO'S BEHIND THE BOOTH? / GUESS THE DJ / TURN IT UP / DJ REVEAL. No date, venue, price or lineup.
Consent caveat applies to the photos. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_dj_carousel.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_copper as cp
import dd_photo_bg as pb
B = dd.B
W = 1080
OUT = os.path.join(ROOT, "out", "discodiwali", "dj")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GOLD = "rgba(214,170,90,.85)"
PHOTOS = [("14_09", "50% 40%", .64), ("07_08", "50% 45%", .66), ("14_08", "50% 35%", .70), ("14_06", "50% 40%", .68), ("07_07", "50% 40%", .66)]
STICKER_PREFIXES = ("vinyl", "phones", "bolt", "note", "speaker", "sp", "star", "heart")


class Slide:
    def __init__(self, H, idx):
        self.H, self.dy, self.parts, self.els = H, (H - 1350) // 2, [], []
        ref, pos, dim = PHOTOS[idx]
        self.parts.append(pb.photo_ground(dd, W, H, ref, pos, dim=dim))

    def box(self, tag, x, y, w, h):
        self.els.append((tag, x, y + self.dy, w, h))

    def text(self, tag, txt, y, size, weight=700, x=0, w=W, align="center", extra="", h=None, rot=0):
        h = h or round(size * .88)                                   # a tight line-height headline's ink is ~0.88 of its font size
        rt = f";transform:rotate({rot}deg)" if rot else ""
        self.parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;width:{w}px;top:{y + self.dy}px;text-align:{align};font-family:var(--d);font-weight:{weight};font-size:{size}px;'
                          f'line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20{rt}">{txt}</div>')
        self.box(tag, x, y, w, h)

    def sticker(self, tag, svg, x, y, w, h, z=12):
        self.parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + self.dy}px;z-index:{z}">{svg}</div>')
        self.box(tag, x, y, w, h)

    def pill(self, tag, txt, x, y, w, h, size, fill="rgba(0,0,0,.4)"):
        self.parts.append(f'<div data-tag="{tag}" style="position:absolute;left:{x}px;top:{y + self.dy}px;width:{w}px;height:{h}px;border:2px solid {GOLD};border-radius:{h // 2}px;background:{fill};'
                          f'display:flex;align-items:center;justify-content:center;font-family:var(--d);font-weight:700;font-size:{size}px;white-space:nowrap;text-transform:uppercase;letter-spacing:2px;{STROKE}z-index:20">{txt}</div>')
        self.box(tag, x, y, w, h)

    def badge(self, x=40, y=40, w=150):
        self.parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{x}px;top:{y + self.dy}px;width:{w}px;z-index:20">')
        self.box("badge", x, y, w, round(w * 1005 / 1061))

    def lockup(self, vw, x, y):
        t = vw / 1717; vh = round(991 * t)
        self.parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(x - 265 * t)}px;top:{round(y + self.dy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
        self.box("title", x, y, vw, vh)
        return y + vh

    def done(self):
        return "".join(self.parts), self.els


def s1(H):
    s = Slide(H, 0); s.badge()
    s.text("h1", "Who&rsquo;s on", 215, 134); s.text("h2", "the decks?", 345, 134)
    s.pill("tag", "DJ reveal", 370, 500, 340, 70, 36)
    s.sticker("vinyl", cp.vinyl(540, 0, "v1"), 270, 620, 540, 540)
    s.sticker("phones", cp.headphones(350, -14, "hp1"), 18, 740, 350, 350, 13)
    s.sticker("bolt", cp.bolt(210, 12, "b1"), 835, 690, 210, 210)
    s.sticker("note", cp.note(170, -10, "n1"), 870, 960, 170, 170)
    s.sticker("note2", cp.note(150, 14, "n2"), 880, 70, 150, 150)
    s.pill("swipe", "Swipe &rarr;", 360, 1212, 360, 76, 38)
    return s.done()


def s2(H):
    s = Slide(H, 1); s.badge(x=40, y=40)
    s.text("h1", "Who&rsquo;s behind", 205, 118, x=64, w=950, align="left"); s.text("h2", "the booth?", 325, 118, x=64, w=950, align="left")
    s.text("sub", "Masquerade Sangeet Edition", 462, 40, 400, x=64, w=950, align="left")
    s.sticker("speaker", cp.speaker(560, 8, "sp1"), 470, 600, 560, 560)
    s.sticker("vinyl", cp.vinyl(330, -8, "v2"), 50, 880, 330, 330, 13)
    s.sticker("bolt", cp.bolt(250, -16, "b2"), 70, 590, 250, 250)
    s.sticker("note", cp.note(200, 12, "n3"), 330, 640, 200, 200, 13)
    s.sticker("star", cp.star(170, 10, "s2"), 880, 460, 170, 170)
    return s.done()


def s3(H):
    s = Slide(H, 2); s.badge(x=890, y=40)
    s.text("h1", "Guess", 150, 150, x=64, w=700, align="left"); s.text("h2", "the DJ", 285, 150, x=64, w=700, align="left")
    s.parts.append(f'<div data-tag="card" style="position:absolute;left:90px;top:{500 + s.dy}px;width:900px;height:380px;border-radius:44px;background:rgba(10,7,32,.62);border:3px solid rgba(255,255,255,.4);'
                   f'box-shadow:0 30px 70px rgba(0,0,0,.6);z-index:10"></div>'); s.box("card", 90, 500, 900, 380)
    s.pill("djtag", "DJ", 130, 535, 150, 62, 34, "rgba(0,0,0,.5)")
    s.text("q", "? ? ? ?", 620, 170, x=90, w=900)
    s.sticker("vinyl", cp.vinyl(380, 0, "v3"), -90, 930, 380, 380, 9)
    s.sticker("phones", cp.headphones(340, 12, "hp2"), 690, 330, 340, 340, 13)
    s.sticker("bolt", cp.bolt(190, 8, "b3"), 60, 420, 190, 190, 13)
    s.sticker("note", cp.note(170, -8, "n4"), 850, 1090, 170, 170, 13)
    s.text("cta", "Comment your guess", 960, 54, x=150, w=W - 150)
    return s.done()


def s4(H):
    s = Slide(H, 3); s.badge(x=40, y=40)
    s.text("h1", "Turn", 360, 215, x=60, w=700, align="left", rot=-7); s.text("h2", "it up", 560, 215, x=60, w=700, align="left", rot=-7)
    s.sticker("sp1", cp.speaker(360, 10, "sp2"), 660, 130, 360, 360)
    s.sticker("sp2", cp.speaker(300, -8, "sp3"), 30, 880, 300, 300, 13)
    s.sticker("bolt", cp.bolt(240, 10, "b4"), 690, 740, 240, 240, 13)
    s.sticker("bolt2", cp.bolt(170, -14, "b5"), 190, 200, 170, 170, 13)
    s.sticker("note", cp.note(180, -12, "n5"), 430, 940, 180, 180)
    s.sticker("note2", cp.note(150, 12, "n6"), 900, 1000, 150, 150)
    s.sticker("vinyl", cp.vinyl(250, 0, "v4"), 770, 960, 250, 250, 11)
    s.text("sub", "Masquerade Sangeet Edition", 1205, 38, 400)
    return s.done()


def s5(H):
    s = Slide(H, 4); s.badge(x=40, y=40)
    s.sticker("heart", cp.heart(200, -10, "h5"), 60, 190, 200, 180)
    s.sticker("star", cp.star(190, 12, "s5"), 840, 190, 190, 190)
    s.text("h1", "DJ", 190, 300); s.text("h2", "Reveal", 480, 170)
    s.text("sub", "Masquerade Sangeet Edition", 685, 40, 400)
    s.pill("link", "Link in bio", 260, 790, 560, 104, 48)
    s.sticker("note", cp.note(220, -10, "n7"), 20, 780, 220, 220)
    s.sticker("phones", cp.headphones(230, 12, "hp3"), 830, 770, 230, 230)
    s.lockup(330, 375, 1000)
    return s.done()


SLIDES = [s1, s2, s3, s4, s5]


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        for name, H in (("feed", 1350), ("story", 1920)):
            for i, fn in enumerate(SLIDES, 1):
                inner, els = fn(H)
                tags = [e[0] for e in els]
                stick = [t for t in tags if t.startswith(STICKER_PREFIXES)]
                ign = [(a, b) for a in stick for b in tags if a != b]   # a sticker pile overlaps on purpose; judged by eye
                await B.render(B.page(W, H, "#000", inner, grain=False), os.path.join(OUT, f"{name}_{i}.png"), W, H, elements=els, containers=("card",), bleed_tags=("plate", "vinyl"),
                               crop_tags=("plate",), page_bg="#000", collision_ignore=ign)
    print("dj carousel done ->", OUT)
asyncio.run(main())
