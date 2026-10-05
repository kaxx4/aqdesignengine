"""TerraThon IMPACT post (2026-10-05): RS. 10,000 of TerraThon profit goes to welfare, two lanes only (food distribution, plantation), per user: food and plants, a rough idea, no unit costs supplied. NO per-unit or split numbers printed. Food = real AQ photo (core.PHOTOS food); plantation = flat doodle plate (no real plantation photo in repo, acceptable adaptation).
OLD DOC: TerraThon x SHIKSHAQ static post (single feed 1080x1350): introduces Shikshaq as OUR EDUCATION PARTNER (user, 2026-10-01). Same TerraThon look as the CRFTD / Crave'lla / Artily posts.
Real asset: the user's own Shikshaq logo (black wordmark + orange sparkle on white, 1080x1080, partners/shikshaq/), masked to a circle with an orchid ring like the Artily / CRFTD / Crave'lla posts.
(v1 used a tile cropped from the partner strip; replaced when the user sent the real file.) Handle @shikshaq.in is user-supplied (2026-10-01). Facts used: Shikshaq is AquaTerra's own tutor-discovery platform (brain/AQ_FACTS.md section 10: zero-commission, connection-only, free,
Kolkata; the Shikshaq terms say it is a free platform), TerraThon runs 2nd to 4th Oct 2026 in Kolkata. This is the whole-fest partner, so the kicker is TERRATHON, not Mini-Fete, and no venue or stall
is named (none was supplied). NOT claimed: what Shikshaq does AT the event, a stall, a launch, user numbers, a link (none supplied).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_shikshaq_post.py [story]   ->  out/collaterals/shikshaq_education_partner_post.png  (story: out/collaterals/stories/shikshaq_education_partner_story.png)
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
H, TOTAL = (1920 if STORY else 1350), 1
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/partners"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


dd = tt.load("doodles")
FOOD = core.PHOTOS["food"]


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


async def build():
    s = Slide(1, 55)
    ty = await s.title("RS. 10,000", "OF OUR PROFIT GOES TO WELFARE", big_w=760, sub_w=900, top=108)
    s.star("star_tl", 28, 70 + OY); s.star("star_tr", W - 28 - 104, 86 + OY)
    y0 = ty + 36
    fh = int(min(H - FOOT - 150 - y0 - 190, 800)); fw = 450; gap = 40; x0 = (W - 2 * fw - gap) / 2
    # core.PHOTOS food has a baked-in caption along its bottom edge and a half-cut sticker at the left: crop both out by oversizing the image inside the clipped frame
    s.add(f'<div class="measure" data-tag="food" style="position:absolute;left:{x0}px;top:{y0}px;width:{fw}px;height:{fh}px;box-sizing:border-box;border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:4">'
          f'<img src="{FOOD}" style="position:absolute;left:-14%;top:0;width:128%;height:134%;object-fit:cover;object-position:50% 0;display:block"></div>')
    s.el("food", x0, y0, fw, fh)
    px = x0 + fw + gap
    tree = dd.stamp("tree", "#2FD284", rot=0); leaf = dd.stamp("leaf", "#2FD284", rot=0); spark = dd.stamp("sparkle", "#DE68F0", rot=0)
    s.add(f'<div class="measure" data-tag="plant" style="position:absolute;left:{px}px;top:{y0}px;width:{fw}px;height:{fh}px;box-sizing:border-box;border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:{CTA_FILL};z-index:4">'
          f'<div style="position:absolute;left:{(fw-24-360)/2}px;top:{(fh-24-360)/2}px;width:360px;height:360px">{tree}</div>'
          f'<div style="position:absolute;left:30px;top:{fh-24-170}px;width:130px;height:130px">{leaf}</div>'
          f'<div style="position:absolute;right:34px;top:34px;width:90px;height:90px">{spark}</div></div>')
    s.el("plant", px, y0, fw, fh)
    ly = y0 + fh + 24
    s.text("lab1", "FOOD DISTRIBUTION", x0 - 10, ly, fw + 20, 38, 900, WHITE)
    s.text("lab2", "PLANTATION", px - 10, ly, fw + 20, 38, 900, WHITE)
    s.text("kick", "FOOD ON PLATES. TREES IN THE GROUND.", 40, ly + 78, W - 80, 40, 900, ORCHID)
    s.footer(cta="YOU MADE THIS HAPPEN")
    return [(s,)]


async def main():
    slides = await build()
    os.makedirs("out/collaterals/stories" if STORY else "out/collaterals", exist_ok=True)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 50, True), ("cta", INK, CTA_FILL, 30, True), ("lab1", WHITE, GROUND, 38, True), ("lab2", WHITE, GROUND, 38, True), ("kick", ORCHID, GROUND, 40, True)]
    async with B.session():
        for s, *ign in slides:
            out = "out/collaterals/stories/impact_10k_story.png" if STORY else "out/collaterals/impact_10k_post.png"
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, page_bg=GROUND, expect_hero=False, margin=12, crop_tags=("food", "plant"))
            print("done", out)

asyncio.run(main())
