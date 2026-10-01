"""TerraThon x ARTILY stall carousel (5 slides; feed 1080x1350 and story 1080x1920), built the way the Crave'lla one was (user, 2026-10-01: "make the carousel for Artily just like
you had made for Cravella"). Slides: cover, meet the stall (slab), the FINAL menu on ONE slide, a drink feature, closer. OUR HYDRATION PARTNER (user's wording for Artily).
Real assets only: the user's three photos + logo, copied to engine/assets/terrathon/partners/artily/ (logo masked to a circle, like Crave'lla's).
Menu and prices verbatim from the user's FINAL list (2026-10-01): Classic Cold Coffee, Strawberry Matcha, Lime Bomb, Pink Panther at Rs. 250; Gondhoraj Mojito Rs. 200. The four
shared-price drinks print the price ONCE ("ALL RS. 250"). Facts: stall at the TerraThon Mini-Fete, 3rd and 4th Oct 2026, Turf XL, New Alipore. "ARTISANAL BEVERAGES" is the tagline
on Artily's own logo lockup. Handle @artilyindia is the one used on the QR poster (not independently verified). NOT claimed: ingredients, sizes, a founding year, ordering, which
menu item each non-matcha photo shows (the two other drinks are shown unlabelled; the green-white-red glass is captioned Strawberry Matcha, which is an inference from the photo).
Look: TerraThon's (black ground, shuriken, cream cards with green borders, orchid highlights, StretchPro title, Sigmar One sub).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_artily_carousel.py [story]   (story = 1080x1920, out/collaterals/stories/artily_story_NN.png)
"""
import asyncio, base64, importlib.util, os, random, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
lay = tt.load("layout")
GROUND, ORCHID, CREAM_HALO, INK, WHITE, CTA_FILL, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.CTA_FILL, tt.SLAB
GREEN = "#2FD284"
import sys
STORY = "story" in sys.argv[1:]     # 1080x1920 with Instagram UI zones clear (top ~250, bottom ~270)
H, TOTAL = (1920 if STORY else 1350), 5
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/partners/artily"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


LOGO = b64(f"{A}/logo_circle.png", "image/png")
PH_BLUE = b64(f"{A}/drink_blue.jpg", "image/jpeg")
PH_POP = b64(f"{A}/drink_popsicle.jpg", "image/jpeg")
PH_MATCHA = b64(f"{A}/matcha.jpg", "image/jpeg")


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

    async def title(self, big, sub, big_w=780, sub_w=800, top=100, ls=None):
        ls = tt.ST_LS if ls is None else ls
        top += OY
        big = re.sub(r'([A-Z])(?=\1)', '\\1\u200c', big).replace("'", "\u2019")   # ZWNJ stops StretchPro's doubled-letter ligature (LL, EE) from stretching
        m = await B.measure_text([dict(text=big, font="StretchPro", size=100, weight=400, letter_spacing=f"{ls}em", features=tt.ST_FEAT),
                                  dict(text=sub, font="SigmarOne", size=50, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        tpx = 100 * big_w / m[0]["text_w"]; spx = 50 * min(1.0, sub_w / m[1]["text_w"])
        self.text("t1", "TERRATHON MINI-FETE", (W - 700) / 2, top - 52, 700, 38, 400, CREAM_HALO)
        self.add(f'<div class="measure" data-tag="t2" style="position:absolute;left:{(W - big_w - 20) / 2}px;width:{big_w + 20}px;top:{top}px;text-align:center;color:{WHITE};font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {WHITE};'
                 f'letter-spacing:{ls}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1;white-space:nowrap;z-index:6">{big}</div>')
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


async def build():
    slides = []
    BOT = H - FOOT - 150           # lowest content edge above the footer (feed 1200, story 1500)
    # ---- 1 COVER: name across the top, drink photo left, big logo right ----
    s = Slide(1, 41)
    ty = await s.title("ARTILY", "OUR HYDRATION PARTNER", big_w=560, sub_w=800, top=104, ls=0.02)   # looser tracking: at the house -0.045em the T and I of ARTILY fuse
    s.star("star_tl", 24, 70 + OY); s.star("star_tr", W - 24 - 104, 86 + OY)
    A = BOT - ty
    fx, fy, fw, fh = 56, ty + 30, 470, A - 90
    s.frame("frame", PH_POP, fx, fy, fw, fh, -3, "70% 50%")
    ls = 440; lx, lyy = W - 56 - ls, fy + 20
    s.logo_badge("logo_big", lx, lyy, ls, ring=14)
    s.chip("chip", "ARTISANAL BEVERAGES", lx - 20, lyy + ls + 30, ls + 40, deg=-3, size=30)
    s.text("info1", "3RD + 4TH OCT", lx - 20, lyy + ls + 150, ls + 40, 46, 900)
    s.text("info2", "TURF XL, NEW ALIPORE", lx - 20, lyy + ls + 214, ls + 40, 32, 400)
    s.star("star_br", W - 150, BOT - 70, 112)
    s.star("star_bl", fx - 30, fy + fh - 90, 112, z=10)
    s.footer(); slides.append((s, ("frame", "star_bl"), ("frame", "logo_big")))
    # ---- 2 MEET THE STALL: wide drink photo, logo badge, a tilted slab with the facts ----
    s = Slide(2, 42)
    ty = await s.title("MEET THE STALL", "ARTILY, OUR HYDRATION PARTNER", big_w=760, sub_w=860, top=96)
    A = BOT - ty
    fh = int(A * 0.54)
    s.frame("frame", PH_BLUE, 84, ty + 14, 912, fh, -1.25, "50% 55%")
    s.logo_badge("badge", 40, ty + 2, 170, ring=8)
    s.star("star_tr", W - 130, ty + 2, 104)
    sx, sy, sw = 84, ty + 14 + fh + 56, 912
    sh = min(BOT - sy + 40, 330)
    s.add(f'<div class="measure" data-tag="slab" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;box-sizing:border-box;transform:rotate(1.25deg);background:{SLAB};border:20px solid {ORCHID};border-radius:52px;z-index:8"></div>')
    s.el("slab", *rb(sx, sy, sw, sh, 1.25))
    rows = [("ARTISANAL BEVERAGES", 900, 44), ("SAT 3 + SUN 4 OCT, 2026", 900, 52), ("TURF XL, NEW ALIPORE", 900, 52)]
    tot = sum(sz for _, _, sz in rows) + 2 * 22; ty2 = sy + (sh - tot) / 2 - 6
    for i, (txt, wt, sz) in enumerate(rows):
        s.add(f'<div class="measure" data-tag="row{i}" style="position:absolute;left:{sx + 40}px;width:{sw - 80}px;top:{ty2}px;text-align:center;color:{INK};font-family:var(--d);font-weight:{wt};font-size:{sz}px;line-height:1;white-space:nowrap;z-index:9">{txt}</div>')
        s.el(f"row{i}", sx + 40, ty2, sw - 80, sz * .85); ty2 += sz + 22
    s.footer(); slides.append((s, ("frame", "badge"), ("frame", "star_tr"), ("badge", "star_tr"), ("frame", "slab")) + tuple(("slab", f"row{i}") for i in range(3)))
    # ---- 3 THE MENU: everything on one slide ----
    s = Slide(3, 43)
    ty = await s.title("THE MENU", "ARTILY STALL", big_w=620, sub_w=440, top=96)
    k = 1.12 if STORY else 1.0
    rh1 = int(112 * k); rh2 = int(120 * k)
    h1 = 36 + 56 + 14 + rh1 * 4 + 26; h2 = 36 + 56 + 14 + rh2 + 26
    gap = 24; tot = h1 + h2 + gap
    top = ty + 16 + max(0, (BOT + 30 - ty - 16 - tot) / 2)
    four = ["CLASSIC COLD COFFEE", "STRAWBERRY MATCHA", "LIME BOMB", "PINK PANTHER"]
    s.box("boxA", 56, top, 968, h1, head_row("FOUR DRINKS", "ALL RS. 250", 40) + f'<div style="margin-top:14px">{rows_html(four, rh1, 42)}</div>', pad="26px 26px 22px")
    s.box("boxB", 56, top + h1 + gap, 968, h2, head_row("THE MOJITO", "RS. 200", 40) + f'<div style="margin-top:14px">{rows_html(["GONDHORAJ MOJITO"], rh2, 42)}</div>', pad="26px 26px 22px")
    s.star("star_tl", 30, 60 + OY); s.star("star_tr", W - 30 - 104, 74 + OY)
    s.footer(); slides.append((s,))
    # ---- 4 DRINK FEATURE: the matcha photo, price stickers ----
    s = Slide(4, 44)
    ty = await s.title("STRAWBERRY MATCHA", "FROM THE ARTILY MENU", big_w=860, sub_w=640, top=96)
    A = BOT - ty
    fh = A - 230
    s.frame("frame", PH_MATCHA, 84, ty + 14, 912, fh, -1.25, "50% 50%")
    s.star("star_c", 30, ty + fh - 130, 112); s.star("star_tr", W - 130, ty - 30, 104)
    py = ty + 14 + fh + 28
    s.chip("p1", "STRAWBERRY MATCHA  RS. 250", 84, py, 700, deg=-2, size=33)
    s.chip("p2", "ALL DRINKS RS. 200 TO RS. 250", 250, py + 84, 740, deg=1.5, size=31)
    s.footer(); slides.append((s, ("frame", "star_c"), ("frame", "star_tr"), ("frame", "p1"), ("frame", "p2"), ("p1", "p2"), ("star_tr", "t3")))
    # ---- 5 CLOSER ----
    s = Slide(5, 45)
    ty = await s.title("SEE YOU THERE", "ARTILY, OUR HYDRATION PARTNER", big_w=800, sub_w=880, top=96)
    ls = 560 if STORY else 400; lx = (W - ls) / 2; lyy = ty + 26
    s.logo_badge("logo_big", lx, lyy, ls, ring=14)
    s.star("star_l", 90, lyy + 40, 112); s.star("star_r", W - 90 - 112, lyy + ls - 150, 112)
    cy = lyy + ls + 54
    s.text("d1", "3RD & 4TH OCTOBER, 2026", 40, cy, W - 80, 46, 900)
    s.text("d2", "TURF XL, NEW ALIPORE", 40, cy + 60, W - 80, 46, 900)
    s.chip("handle", "@ARTILYINDIA", (W - 700) / 2, cy + 150, 700, deg=-2, size=40)
    s.footer(); slides.append((s, ("logo_big", "star_l"), ("logo_big", "star_r"), ("logo_big", "handle")))
    return slides


async def main():
    slides = await build()
    outdir = "out/collaterals/stories" if STORY else "out/collaterals/artily_stall"; os.makedirs(outdir, exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("card", INK, CTA_FILL, 31, False), ("chip", INK, ORCHID, 30, True),
                  ("price", INK, GREEN, 40, True), ("idx", INK, CTA_FILL, 26, True), ("note", WHITE, GROUND, 24, False), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        for s, *ign in slides:
            out = f"{outdir}/artily_story_{s.idx:02d}.png" if STORY else f"{outdir}/slide_{s.idx:02d}.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, containers=("slab",) if s.idx == 2 else (), page_bg=GROUND,
                           expect_hero=False, collision_ignore=set(map(tuple, ign)), margin=12, crop_tags=("frame", "logo_big", "badge"))
            print("done", out)

asyncio.run(main())
