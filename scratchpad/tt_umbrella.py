"""TerraThon UMBRELLA card: all three sports in one (Cricket | FIFA | Pickleball), prizes totalling Rs.15,000 (7,500 + 2,500 + 5,000, all from the
user's events). Variants: closing (REGISTRATIONS CLOSE 1 OCT) for the Wed 30 story #10 and a feed post; canvas feed | story.
Built from the same parts as the event posters (tt_events.py)."""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
GROUND, ORCHID, CREAM_HALO, SLAB, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL
TOTAL = 7500 + 2500 + 5000     # must equal the sum of the events (validated below)
assert TOTAL == 15000

async def build(out, canvas="feed", line=("REGISTRATIONS", "CLOSE 1 OCT"), cta="LINK IN BIO"):
    story = canvas == "story"; Hc = 1920 if story else 1350
    dy = dict(hdr=210, hero=250, slab=280, info=300, foot=320) if story else dict(hdr=0, hero=0, slab=0, info=0, foot=0)
    els = []
    def el(label, x, y, w, h, g): els.append((label, x, y + dy[g], w, h))
    def sticker(name, label, x, y, h_px, z=3, g="hero"):
        im, src = tt.crop_to_alpha(name); w = h_px * im.width / im.height
        el(label, x, y, w, h_px, g)
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h_px}px;z-index:{z}">', w
    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, Hc):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * Hc / 1350)))
    ground = f'<div style="position:absolute;inset:0;background:{GROUND}"></div><svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{Hc}">{specks}</svg>'
    px = tt.px
    m = await B.measure_text([
        dict(text="TERRATHON", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text="CRICKET | FIFA | PICKLEBALL", font="SigmarOne", size=64, weight=400, letter_spacing=f"{tt.SG_LS}em"),
        dict(text="PRIZES TOTALLING:", font="d", size=100, weight=400), dict(text=f"RS.{TOTAL:,}", font="d", size=100, weight=900),
        dict(text=line[0], font="d", size=100, weight=400), dict(text=line[1], font="d", size=100, weight=900),
        dict(text="2ND-4TH OCTOBER, 2026", font="d", size=40, weight=400)], extra_css=tt.FONT_CSS)
    tw = [r["text_w"] for r in m]
    # header
    HB = f'position:absolute;left:{(W - 760) / 2}px;width:760px;text-align:center;color:{WHITE};z-index:6;white-space:nowrap;line-height:1;font-family:var(--d)'
    f1 = 100 * 620 / tw[2]; f2 = 100 * 600 / tw[3]
    hdr = (f'<div class="measure" data-tag="h1" style="{HB};top:70px;font-weight:400;font-size:{f1}px">PRIZES TOTALLING:</div>'
           f'<div class="measure" data-tag="h2" style="{HB};top:{70 + f1 * 1.0}px;font-weight:900;font-size:{f2 * 1.0}px">'
           f'<span style="font-family:\'Noto Color Emoji\';font-weight:400;font-size:{f2 * .72}px;margin-right:10px">💸</span>RS.{TOTAL:,}</div>')
    el("h1", (W - 620) / 2, 70, 620, f1 * .82, "hdr"); el("h2", (W - 640) / 2, 70 + f1, 640, f2 * .82, "hdr")
    # hero: three sports
    slab_top = 660
    a, aw = sticker("cricket_set.png", "hero_cricket", 58, 320, 380)
    c, cw = sticker("controller.png", "hero_fifa", (W - 420) / 2, 450, 286)
    p_, pw = sticker("pickleball_set.png", "hero_pickle", W - 58 - 361, 320, 380)
    stars = ""
    for lab, x, y, z in (("star_tl", 30, 150, 5), ("star_tr", 965, 215, 5), ("star_ml", 19, slab_top - 22, 9), ("star_br", 955, slab_top + 270 - 75, 9)):
        s_, _ = sticker("shuriken.png", lab, x, y, 100, z); stars += s_
    # slab
    SX, SW, SH = 47, 986, 270
    tpx = 100 * 700 / tw[0]; spx = 64 * min(1.0, 800 / tw[1])
    el("slab", SX - 6, slab_top - 12, SW + 12, SH + 24, "slab")
    slab = (f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{slab_top}px;width:{SW}px;height:{SH}px;transform:rotate(-1.25deg);'
            f'background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK};white-space:nowrap">'
            f'<div style="font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * tpx}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{tpx}px;line-height:1.05">TERRATHON</div>'
            f'<div style="font-family:SigmarOne;-webkit-text-stroke:{tt.SG_STROKE * spx}px {INK};letter-spacing:{tt.SG_LS}em;font-size:{spx}px;line-height:1;margin-top:26px">CRICKET | FIFA | PICKLEBALL</div></div>')
    # info + closing lines
    LB = f'position:absolute;left:{(W - 760) / 2}px;width:760px;text-align:center;color:{WHITE};white-space:nowrap;line-height:1;font-family:var(--d);z-index:6'
    r1 = min(100 * 560 / tw[4], 60); r2 = min(100 * 640 / tw[5], 88)
    info = (f'<div class="measure" data-tag="date" style="{LB};top:968px;font-weight:400;font-size:40px">2ND-4TH OCTOBER, 2026</div>'
            f'<div class="measure" data-tag="l1" style="{LB};top:1030px;font-weight:400;font-size:{r1}px">{line[0]}</div>'
            f'<div class="measure" data-tag="l2" style="{LB};top:{1030 + r1 * 1.04}px;font-weight:900;font-size:{r2}px">{line[1]}</div>')
    el("date", (W - tw[6]) / 2, 970, tw[6], 32, "info"); el("l1", (W - 560) / 2, 1032, 560, r1 * .8, "info"); el("l2", (W - 640) / 2, 1032 + r1 * 1.04, 640, r2 * .8, "info")
    fy = 1235 + (0 if not story else 0)
    foot = (f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{fy + 6}px;height:56px;z-index:9">'
            f'<div class="measure" data-tag="cta" style="position:absolute;left:720px;top:{fy}px;width:337px;height:67px;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};'
            f'display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:30px;color:{INK}">{cta}</div>')
    el("logo", 27, fy + 6, 320, 56, "foot"); el("cta", 720, fy, 337, 67, "foot")
    grp = lambda g, h_: f'<div style="position:absolute;left:0;top:{dy[g]}px;width:{W}px;height:1350px">{h_}</div>'
    html = B.page(W, Hc, GROUND, f'<style>{tt.FONT_CSS}</style>' + ground + grp("hdr", hdr) + grp("hero", a + c + p_ + stars) + grp("slab", slab) + grp("info", info) + grp("foot", foot), grain=False)
    text_pairs = [("head", WHITE, GROUND, 96, True), ("info", WHITE, GROUND, 40, False), ("title", INK, SLAB, 100, True), ("cta", INK, CTA_FILL, 30, True)]
    await B.render(html, out, W, Hc, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=True,
                   collision_ignore={("star_ml", "hero_cricket"), ("hero_cricket", "slab"), ("hero_fifa", "slab"), ("hero_pickle", "slab"), ("star_ml", "slab"), ("star_br", "slab"),
                                     ("hero_cricket", "hero_fifa"), ("hero_fifa", "hero_pickle"), ("star_tl", "hero_cricket"), ("star_tr", "hero_pickle")}, margin=12)

async def main():
    d = "out/collaterals"; os.makedirs(f"{d}/promo_stories", exist_ok=True)
    async with B.session():
        await build(f"{d}/promo_stories/umbrella_closing.png", "story")
        await build(f"{d}/umbrella_closing_feed.png", "feed")
    print("done")
if __name__ == "__main__":
    asyncio.run(main())
