"""WHY WE THROW EVENTS: 5-slide narrative carousel (feed 1080x1350), picture cover (user, 2026-10-05). TerraThon visual system, REAL photos only (throwback / dd_photos / core.PHOTOS). Facts printed: AQ is an NGO (DARPAN-registered, AQ_FACTS), 81 distribution drives, 30 plantation drives, 250 workshops logged June 2021 to Sept 2025 (date travels with the numbers), Rs. 10,000 TerraThon profit to welfare (user). No other numbers.
Photos include minors: confirm consent before posting.
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
H, TOTAL = (1920 if STORY else 1350), 5
OY = 200 if STORY else 0          # content drop below the top UI zone
EXTRA = 130 if STORY else 0       # extra vertical room spent on bigger frames and rows
FOOT = 270 if STORY else 0        # footer lift off the bottom edge
A = "engine/assets/terrathon/partners"


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


TB = "engine/assets/terrathon"
def ph(p): return b64(f"{TB}/{p}", "image/jpeg")
FOODP, EDUP = core.PHOTOS["food"], core.PHOTOS["edu"]


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


def body(s, tag, txt, y, size=34, color=CREAM_HALO):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:40px;top:{y}px;width:{W-80}px;text-align:center;color:{color};font-family:var(--e);font-weight:400;font-size:{size}px;line-height:1.1;white-space:nowrap;z-index:6">{txt}</div>')
    s.el(tag, 40, y, W - 80, size * .9)


def clipped(s, tag, src, x, y, w, h, deg, scale="width:128%;height:134%;left:-14%;top:0", pos="50% 0"):
    s.add(f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({deg}deg);border:12px solid {ORCHID};border-radius:44px;overflow:hidden;background:#111;z-index:4">'
          f'<img src="{src}" style="position:absolute;{scale};object-fit:cover;object-position:{pos};display:block"></div>')
    s.el(tag, *rb(x, y, w, h, deg))


async def build():
    out = []
    # 1 COVER: full-bleed photo under a scrim
    s = Slide(1, 11)
    s.add(f'<img src="{ph("dd_photos/dance.jpg")}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%;z-index:0">')
    s.add('<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.88) 0%,rgba(0,0,0,.55) 30%,rgba(0,0,0,.1) 52%,rgba(0,0,0,.55) 80%,rgba(0,0,0,.92) 100%);z-index:2"></div>')
    ty = await s.title("WHY WE THROW", "EVENTS? THE HONEST ANSWER", big_w=900, sub_w=900, top=104)
    s.star("star_l", 28, 960, 112, z=8); s.star("star_r", W - 28 - 104, 880, 104, z=8)
    s.chip("swipe", "SWIPE TO FIND OUT  \u2192", (W - 560) / 2, 1090, 560, deg=-2, size=34)
    s.footer(cta=None)
    out.append((s, ("star_l", "swipe"), ("star_r", "swipe")))
    # content slides
    async def content(idx, seed, photo, pos, deg, heads, bodies, tag="frame"):
        s = Slide(idx, seed)
        s.frame(tag, photo, 90, 90, 900, 720, deg, pos=pos)
        s.star("star", 40, 720, 120, z=8)
        y = 860
        for i, h in enumerate(heads):
            s.text(f"h{i}", h, 40, y + i * 84, W - 80, 76, 900, WHITE); 
        y = y + len(heads) * 84 + 24
        for i, b in enumerate(bodies): body(s, f"b{i}", b, y + i * 46)
        s.footer(cta=None)
        return (s, (tag, "star"))
    out.append(await content(2, 12, ph("throwback/IMG_5997.jpg"), "50% 56%", -2, ["WE ARE AN NGO.", "WE ALSO THROW", "A GREAT PARTY."], ["yes, both are true."]))
    out.append(await content(3, 13, ph("throwback_fifa/IMG-20241019-WA0023.jpg"), "50% 0%", 2, ["FUN IS OUR", "BEST FUNDRAISER."], ["tickets, stalls and games turn a good weekend", "into money for welfare."]))
    # 4: where it goes
    s = Slide(4, 14)
    clipped(s, "food", FOODP, 70, 90, 450, 600, -2)
    clipped(s, "edu", EDUP, 560, 100, 450, 600, 2)
    s.star("star", 460, 610, 120, z=8)
    for i, h in enumerate(["FUN BECOMES FOOD.", "AND CLASSES.", "AND TREES."]): s.text(f"h{i}", h, 40, 740 + i * 82, W - 80, 74, 900, WHITE)
    for i, t in enumerate(["81 FOOD DRIVES", "30 PLANTATIONS", "250 WORKSHOPS"]): s.chip(f"c{i}", t, 40 + i * 340, 1030, 320, deg=0, size=28)
    s.text("q", "LOGGED JUNE 2021 TO SEPT 2025", 40, 1148, W - 80, 28, 400, CREAM_HALO)
    s.footer(cta=None)
    out.append((s, ("food", "star"), ("edu", "star")))
    # 5: this time
    s = Slide(5, 15)
    s.frame("frame", ph("dd_photos/decor.jpg"), 90, 90, 900, 680, -2, pos="50% 40%")
    s.star("star", 900, 680, 120, z=8)
    for i, h in enumerate(["THIS TIME: RS. 10,000", "OF TERRATHON PROFIT", "GOES TO WELFARE."]): s.text(f"h{i}", h, 40, 830 + i * 84, W - 80, 72, 900, WHITE)
    body(s, "b0", "you made this happen. disco diwali is next.", 1110)
    s.footer(cta="SEE YOU 10TH NOV")
    out.append((s, ("frame", "star")))
    return out


async def main():
    slides = await build()
    os.makedirs("out/collaterals/why_events", exist_ok=True)
    async with B.session():
        for s, *ign in slides:
            out = f"out/collaterals/why_events/why_events_{s.idx:02d}.png"
            tp = [(e[0], WHITE, GROUND, 76, True) for e in s.els if e[0].startswith("h")]
            await B.render(s.html(), out, W, H, elements=s.els, text_pairs=tp, page_bg=GROUND, expect_hero=False, margin=12, collision_ignore=set(map(tuple, ign)), crop_tags=("frame", "food", "edu"))
            print("done", out)

asyncio.run(main())
