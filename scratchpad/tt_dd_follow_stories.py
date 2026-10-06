"""TerraThon x DISCO DIWALI TEASER, 5 follow stories (user, 2026-10-06: "5 story designs in the terrathon design language hinting at disco diwali asking people to follow aquaterra live").
Workflow C (bespoke, from tt_dd_tickets_set.py's Slide kit). 1080x1920, IG UI zones clear. Handle @aquaterra.live (the AQ live account named in the TerraThon site footer).
1 cover: disco ball + FOLLOW  2 dance-floor photo  3 the decor (DIWALI blocks) photo  4 crew photos  5 the follow ask (AQ LIVE sticker + handle).
Photos: the user's five, in git-ignored engine/assets/terrathon/follow_photos/ (people, public repo). They show a past Disco Diwali (the clapperboard reads 22/10/25); no past date is printed.
Facts printed: NO dates at all (user, 2026-10-06: "remove the dates"). No venue (never supplied), no price, no claim about what will happen on the day.
Adaptations: stories use the green-card/slab kit from the ticket stories; 'live' is read as the @aquaterra.live account.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_follow_stories.py   -> out/collaterals/stories/dd_follow_story_N.png
"""
import asyncio, base64, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = True     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = 1920, 5
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/minigames"
DDP = "engine/assets/terrathon/dd_photos"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


FP = "engine/assets/terrathon/follow_photos"
PH = {n: b64(f"{FP}/{n}.jpg", "image/jpeg") for n in ("dance", "duo", "boxes", "night", "crew")}


def rb(x, y, w, h, deg):
    b = lay.rotated_bbox(x, y, w, h, deg)
    return tuple(b) if not isinstance(b, dict) else (b["x"], b["y"], b["w"], b["h"])


class Slide:
    def __init__(self, idx, seed):
        self.idx, self.els, self.parts = idx, [], []
        rnd = random.Random(seed)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
        self.parts += [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
                       f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    def el(self, l, x, y, w, h): self.els.append((l, x, y, w, h))
    def add(self, html): self.parts.append(html)

    async def title(self, big, sub, big_w=780, sub_w=800, top=100):
        top += OY
        big = re.sub(r'([A-Z])(?=\1)', '\\1\u200c', big).replace("'", "\u2019")   # ZWNJ stops StretchPro's doubled-letter ligature (LL, EE) from stretching
        m = await B.measure_text([dict(text=big, font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                                  dict(text=sub, font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        tpx = 100 * big_w / m[0]["text_w"]; spx = 50 * min(1.0, sub_w / m[1]["text_w"])
        self.text("t1", "TERRATHON", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
        self.add(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - big_w - 20) / 2}px;width:{big_w + 20}px;top:{top}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{big}</div>')
        self.el("t2", (W - big_w) / 2, top + 4, big_w, tpx * .82)
        sy = top + tpx * 1.05
        self.add(f'<div class="measure" data-tag="t3" style="position:absolute;left:{(W - sub_w - 20) / 2}px;width:{sub_w + 20}px;top:{sy}px;text-align:center;color:{ORCHID};font-family:SigmarOne;'
                 f'-webkit-text-stroke:{tt.SG_STROKE * spx}px {ORCHID};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;white-space:nowrap;z-index:6">{sub}</div>')
        self.el("t3", (W - sub_w) / 2, sy + 2, sub_w, spx * .82)
        return sy + spx + 20

    def text(self, tag, txt, x, y, w, size, weight=400, color=WHITE, align="center", z=6):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;text-align:{align};color:{color};font-family:var(--d);font-weight:{weight};font-size:{size}px;line-height:1.05;white-space:nowrap;z-index:{z}">{txt}</div>')
        self.el(tag, x, y, w, size * .85)

    def star(self, tag, x, y, size=104, z=8):
        im, src = tt.crop_to_alpha("shuriken.png"); hh = size * im.height / im.width
        self.add(f'<img src="{src}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{hh}px;z-index:{z}">'); self.el(tag, x, y, size, hh)

    def logo_badge(self, tag, x, y, size, ring=10, z=9):
        self.add(f'<img class="measure" data-tag="{tag}" src="{LOGO}" style="position:absolute;left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;box-sizing:border-box;border:{ring}px solid {ORCHID};z-index:{z}">'); self.el(tag, x, y, size, size)

    def chip(self, tag, txt, x, y, w, deg=-3, size=40, z=9):
        h = size + 40
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:6px solid {ORCHID};border-radius:999px;'
                 f'background:{CTA_FILL};display:flex;align-items:center;justify-content:center;white-space:nowrap;font-family:var(--d);font-weight:900;font-size:{size}px;line-height:1;color:{INK};z-index:{z}">{txt}</div>')
        self.el(tag, *rb(x, y, w, h, deg))

    def frame(self, tag, src, x, y, w, h, deg, pos="50% 50%", z=4):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:{z}">'
                 f'<img src="{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>'); self.el(tag, *rb(x, y, w, h, deg))

    def box(self, tag, x, y, w, h, inner, pad="16px 22px"):
        self.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;border:6px solid {GREEN};border-radius:32px;background:{CTA_FILL};'
                 f'padding:{pad};color:{INK};font-family:var(--d);z-index:6;overflow:hidden">{inner}</div>'); self.el(tag, x, y, w, h)

    def footer(self, cta=None):
        ly = H - FOOT - 27 - 56
        self.add(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{ly}px;height:56px;z-index:9">'); self.el("logo", 27, ly, 320, 56)
        if cta:
            cw, chh = 480, 70; cx, cy = W - 27 - cw, H - FOOT - 13 - chh; self.el("cta", cx, cy, cw, chh)
            self.add(f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{chh}px;box-sizing:border-box;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:30px;color:{INK}">{cta}</div>')
        else:
            tw, th = 150, 50; tx, ty = W - 27 - tw, H - FOOT - 27 - th; self.el("idx", tx, ty, tw, th)
            self.add(f'<div class="measure" data-tag="idx" style="position:absolute;left:{tx}px;top:{ty}px;width:{tw}px;height:{th}px;box-sizing:border-box;border:5px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
                     f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:26px;color:{INK}">{self.idx:02d} / {TOTAL:02d}</div>')

    def html(self): return B.page(W, H, GROUND, "".join(self.parts), grain=False)


def head_row(chip, price=None, price_px=40):
    p = (f'<div style="background:{GREEN};color:{INK};font-weight:900;font-size:{price_px}px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{price}</div>' if price else "")
    return (f'<div style="display:flex;align-items:center;justify-content:space-between;gap:16px"><div style="background:{ORCHID};color:{INK};font-weight:900;font-size:30px;line-height:1;padding:9px 20px 8px;border-radius:999px;white-space:nowrap">{chip}</div>{p}</div>')


def rows_html(rows, rh, size, price_col=False):
    out = ""
    for i, r in enumerate(rows):
        name, price = (r if isinstance(r, tuple) else (r, None))
        sep = f"border-top:3px solid rgba(10,10,10,.22);" if i else ""
        pr = (f'<div style="font-weight:900;font-size:{size}px;white-space:nowrap">{price}</div>' if price else "")
        out += f'<div style="height:{rh}px;{sep}display:flex;align-items:center;justify-content:space-between;gap:14px;font-size:{size}px;line-height:1.08;font-weight:400"><div>{name}</div>{pr}</div>'
    return out


_s2 = importlib.util.spec_from_file_location("tt_dd_tickets", os.path.join(ROOT, "scratchpad", "tt_dd_tickets.py")); ddm = importlib.util.module_from_spec(_s2); _s2.loader.exec_module(ddm)
DK = "#0A0A0A"


def svg_sticker(s, tag, svg, x, y, w, h, deg=0, z=7):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;transform:rotate({deg}deg);z-index:{z}">{svg}</div>'); s.el(tag, x, y, w, h)


def slab(s, tag, x, y, w, h, deg=-1.25):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>'); s.el(tag, *rb(x, y, w, h, deg))


def rows_in(s, sx, sy, sw, sh, rows, tag="row"):
    tot = sum(z for _, z, _c in rows) + (len(rows) - 1) * 20; y = sy + (sh - tot) / 2 - 4
    for i, (txt, z, col) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="{tag}{i}" style="position:absolute;left:{sx + 36}px;width:{sw - 72}px;top:{y}px;text-align:center;color:{col};font-family:var(--d);font-weight:900;font-size:{z}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>'); s.el(f"{tag}{i}", sx + 36, y, sw - 72, z * .85); y += z + 20
    return [("slab", f"{tag}{i}") for i in range(len(rows))]



HANDLE = "@AQUATERRA.LIVE"
LIVE_IM, LIVE = tt.crop_to_alpha("aq_live.png")


def live_sticker(s, tag, x, y, w, deg=0, z=7):
    hh = w * LIVE_IM.height / LIVE_IM.width
    s.add(f'<img src="{LIVE}" class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hh}px;transform:rotate({deg}deg);z-index:{z}">'); s.el(tag, *rb(x, y, w, hh, deg)); return hh


async def build():
    out = []
    BOT = H - FOOT - 150
    stars = lambda s: (s.star("star_tl", 24, 70 + OY), s.star("star_tr", W - 24 - 104, 86 + OY))
    # ---- 1 COVER: disco ball, the tease ----
    s = Slide(1, 601)
    ty = await s.title("SOMETHING SHINY", "IS ON THE WAY", big_w=700, sub_w=640, top=104); stars(s)
    bw = 780; ball, bh = ddm.disco_ball(bw, "b1"); svg_sticker(s, "ball", ball, (W - bw) / 2, ty + 10, bw, bh)
    sy = ty + 10 + bh + 30; sh = BOT - sy + 20
    slab(s, "slab", 100, sy, 880, sh)
    ign = rows_in(s, 100, sy, 880, sh, [("FOLLOW " + HANDLE, 50, INK), ("TO BE THE FIRST TO KNOW", 36, "#0E7C86")])
    s.footer(cta="FOLLOW ALONG"); out.append(("1", s, ign + [("slab", "ball"), ("star_tl", "t1"), ("star_tr", "t1")]))
    # ---- 2 REMEMBER THIS? the dance floor ----
    s = Slide(2, 602)
    ty = await s.title("REMEMBER THIS?", "THE DANCE FLOOR", big_w=720, sub_w=640, top=104); stars(s)
    fh = int((BOT - ty) * 0.66); s.frame("frame", PH["dance"], 150, ty + 20, 780, fh, -2.5, "50% 55%")
    dy_ = ty + 20 + fh + 40
    dya, dyh = ddm.diya(250, "d2"); svg_sticker(s, "diya", dya, 70, dy_ - 20, 250, dyh, -8, z=9)
    s.chip("c1", "FOLLOW " + HANDLE, 250, dy_ + 30, 700, deg=-2, size=38)
    s.text("v1", "WE ARE BRINGING THE LIGHTS BACK", 340, dy_ + 150, 700, 34, 900, WHITE, align="left")
    s.footer(); out.append(("2", s, [("star_tl", "t1"), ("star_tr", "t1"), ("frame", "diya"), ("diya", "c1"), ("frame", "star_tr")]))
    # ---- 3 THE DECOR ----
    s = Slide(3, 603)
    ty = await s.title("THE DECOR", "WAS A WHOLE SCENE", big_w=560, sub_w=800, top=104); stars(s)
    fh = int((BOT - ty) * 0.5)
    s.frame("f1", PH["boxes"], 60, ty + 30, 520, int(fh * 1.12), -4, "50% 50%", z=4); s.frame("f2", PH["duo"], 500, ty + 30 + fh * 0.34, 520, int(fh * 1.1), 3.5, "50% 30%", z=5)
    py_ = ty + 30 + int(fh * 1.12) + int(fh * 0.34) + 20
    tk, tkh = ddm.ticket(300, "t3"); svg_sticker(s, "tkt", tk, 60, py_ + 10, 300, tkh, -9, z=9)
    s.text("v1", "FOLLOW " + HANDLE, 380, py_ + 20, 640, 44, 900, WHITE, align="left")
    s.text("v2", "FOR WHAT'S COMING NEXT", 380, py_ + 80, 640, 32, 400, ORCHID, align="left")
    s.footer(); out.append(("3", s, [("star_tl", "t1"), ("star_tr", "t1"), ("f1", "f2"), ("f1", "tkt"), ("f2", "tkt"), ("f2", "star_tr"), ("f2", "v1"), ("f2", "v2"), ("tkt", "v1"), ("tkt", "v2")]))
    # ---- 4 BRING YOUR CREW ----
    s = Slide(4, 604)
    ty = await s.title("BRING YOUR CREW", "OR MAKE ONE THERE", big_w=720, sub_w=640, top=104); stars(s)
    fh = int((BOT - ty) * 0.6)
    s.frame("f1", PH["crew"], 50, ty + 30, 600, int(fh * 0.72), -3, "30% 40%", z=4); s.frame("f2", PH["night"], 470, ty + 30 + fh * 0.36, 560, fh, 3, "50% 70%", z=5)
    s.chip("c1", "LIVE UPDATES: " + HANDLE, 120, ty + 30 + int(fh * 1.36) + 40, 840, deg=-2, size=36)
    s.footer(cta="FOLLOW ALONG"); out.append(("4", s, [("star_tl", "t1"), ("star_tr", "t1"), ("f1", "f2"), ("f2", "c1"), ("f2", "star_tr"), ("f1", "c1")]))
    # ---- 5 THE ASK ----
    s = Slide(5, 605)
    ty = await s.title("FOLLOW", "AQUATERRA LIVE", big_w=560, sub_w=700, top=104); stars(s)
    lw = 620; lh = live_sticker(s, "live", (W - lw) / 2, ty + 20, lw, -4)
    sy = ty + 20 + lh + 40; sh = 300
    slab(s, "slab", 84, sy, 912, sh)
    ign = rows_in(s, 84, sy, 912, sh, [(HANDLE, 84, INK), ("ON INSTAGRAM", 36, "#0E7C86")])
    ball, bh = ddm.disco_ball(200, "b5"); svg_sticker(s, "ball", ball, W - 60 - 200, sy + sh + 30, 200, bh, 8, z=9)
    s.chip("c1", "TAP FOLLOW", 140, sy + sh + 50, 560, deg=-2, size=40)
    s.footer(cta="SEE YOU THERE"); out.append(("5", s, ign + [("slab", "live"), ("slab", "ball"), ("star_tl", "t1"), ("star_tr", "t1"), ("ball", "c1"), ("slab", "c1")]))
    return out


async def stories():
    res = await build()
    outdir = "out/collaterals/stories"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("chip", INK, CTA_FILL, 40, True), ("idx", INK, CTA_FILL, 26, True), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for name, s, ign in res:
            out = f"{outdir}/dd_follow_story_{name}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=False,
                           collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "f1", "f2"))
            print("done", out)

asyncio.run(stories())
