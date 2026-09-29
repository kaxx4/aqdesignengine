"""TerraThon MINI-FETE, the marketing stunt poster (Workflow B recreation).

Reference: training_samples/terrathon/mini_fete_stunt.png (1600x2000). Same visual system as the three
event posters (black ground, four shuriken, tilted white slab with orchid border, footer), but a DIFFERENT
arrangement, so it is its own builder that borrows the shared constants and helpers from tt_events.py:
  * no prize block and no TERRATHON pill; the header is a two-line ask ("CHANCE TO BUY / DISCO DIWALI PASSES")
  * the hero is the pre-composed CARNIVAL pile (palm + flower + heart + smiley) at 0.535 of native
  * slab text is CENTRED (event slabs are left-aligned) and three tiers: TERRATHON / MINI-FETE / subtitle
  * one info row, a three-line bold body, CTA "OPEN TO ALL"
  * the fourth star sits on the slab's bottom-RIGHT corner (event posters: bottom-left)

Adaptations (CLAUDE.md sec 2 rule 4): NeutralFace throughout and NO stretched glyphs (user rulings; the
reference stretches the RR of TERRATHON and the E of MINI-FETE); calendar DRAWN without a date; real
carnival sticker file; core.LOGO fitted by width. The reference writes "MINI-GAMES" in the slab and
"MINIGAMES" in the body; kept as given, flagged to the user.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_minifete.py
"""
import asyncio, importlib.util, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, px, S, W, H = tt.core, tt.B, tt.px, tt.S, tt.W, tt.H
GROUND, ORCHID, CREAM_HALO, SLAB = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB
INK, WHITE, CTA_FILL = tt.INK, tt.WHITE, tt.CTA_FILL

CAP = 0.81            # NeutralFace cap height / font size (measured on the event posters)
BOX = -0.02           # box top = band top - BOX * font, at line-height 1 (measured off v1: band top ~ box top)
CARNIVAL_K = 0.535    # carnival sticker scale vs its native pixels (palm 637px vs 1190px)

CONTENT = dict(
    ask=("CHANCE TO BUY", "DISCO DIWALI PASSES"),
    title="TERRATHON", big="MINI-FEETE", sub="MINI-GAMES | COMPETITIONS",
    date="3RD & 4TH OCTOBER, 2026", venue="TURF XL, NEW ALIPORE",
    body=["MINIGAMES TO WIN", "STALLS TO ENJOY", "DISCO DIWALI PASSES"],
    cta="OPEN TO ALL")


STORY_DY = dict(hdr=210, hero=250, slab=280, info=305, foot=320)
GROUP_OF = {"ask1": "hdr", "ask2": "hdr", "star_tl": "hdr", "hero": "hero", "star_tr": "hero", "star_ml": "hero", "slab": "slab", "star_br": "slab",
            "cal": "info", "date": "info", "venue": "info", "body0": "info", "body1": "info", "body2": "info", "logo": "foot", "cta": "foot"}


async def build(c, out, canvas="feed"):
    story = canvas == "story"; Hc = 1920 if story else H
    DY = STORY_DY if story else {k: 0 for k in STORY_DY}
    els = []

    def el(label, x, y, w, h):
        els.append((label, x, y, w, h))

    def sticker(name, label, x0, y0, z, k=tt.NATIVE):
        im, src = tt.crop_to_alpha(name)
        w, h = px(im.width * k), px(im.height * k)
        el(label, px(x0), px(y0), w, h)
        return (f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{px(x0)}px;'
                f'top:{px(y0)}px;width:{w}px;height:{h}px;z-index:{z}">')

    # ---- measure every string once (fonts decide the sizes, not guesses) ----
    F_ASK, F_TITLE, F_BIG, F_SUB0, F_BODY0, F_INFO = 96, 96, 168, 68, 57, 47.5
    m = await B.measure_text([
        dict(text=c["ask"][0], font="d", size=px(F_ASK), weight=400),
        dict(text=c["ask"][1], font="d", size=px(F_ASK), weight=900),
        dict(text=c["title"], font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text=c["big"], font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text=c["sub"], font="SigmarOne", size=px(F_SUB0), weight=400, letter_spacing=f"{tt.SG_LS}em"),
        dict(text=c["date"], font="d", size=px(F_INFO), weight=400),
        dict(text=c["venue"], font="d", size=px(F_INFO), weight=400),
        dict(text=c["body"][2], font="d", size=px(F_BODY0), weight=900),
    ], extra_css=tt.FONT_CSS)
    tw = [r["text_w"] for r in m]
    sub_px = px(F_SUB0) * min(1.0, px(1290) / tw[4])            # subtitle clamps to the reference's 1290px
    title_px = 100 * px(760) / tw[2]      # TERRATHON (natural RR ligature) ~760 ref px wide
    big_px = 100 * px(1000) / tw[3]       # MINI-FEETE (EE ligature) ~1000 ref px wide
    ls1 = (px(850) - tw[0]) / (len(c['ask'][0]) - 1)              # ask lines: tracking solved to the reference widths
    ls2 = (px(1134) - tw[1]) / (len(c['ask'][1]) - 1)
    body_px = px(F_BODY0) * min(1.0, px(660) / tw[7])           # body clamps to the widest line, 660px

    # ---- ground ----
    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, Hc):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * Hc / H)))
    ground = (f'<div style="position:absolute;inset:0;background:{GROUND}"></div>'
              f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{Hc}">{specks}</svg>')

    # ---- header: the ask ----
    HB = f'position:absolute;left:{px(220)}px;width:{px(1160)}px;text-align:center;color:{WHITE};z-index:6;white-space:nowrap;line-height:1;font-family:var(--d)'
    hdr = (f'<div class="measure" data-tag="ask1" style="{HB};top:{px(78 - BOX * F_ASK)}px;font-weight:400;font-size:{px(F_ASK)}px;letter-spacing:{ls1}px">{c["ask"][0]}</div>'
           f'<div class="measure" data-tag="ask2" style="{HB};top:{px(173 - BOX * F_ASK)}px;font-weight:900;font-size:{px(F_ASK)}px;letter-spacing:{ls2}px">{c["ask"][1]}</div>')
    el("ask1", (W - px(850)) / 2, px(78), px(850), px(CAP * F_ASK)); el("ask2", (W - px(1134)) / 2, px(173), px(1134), px(CAP * F_ASK))

    # ---- hero (carnival pile, bottom hidden by the slab) + four stars ----
    hero = sticker("carnival.png", "hero", 420, 335, 3, k=CARNIVAL_K)
    stars = (sticker("shuriken.png", "star_tl", 62, 78, 5) + sticker("shuriken.png", "star_tr", 1402, 256, 5)
             + sticker("shuriken.png", "star_ml", 20, 988, 5) + sticker("shuriken.png", "star_br", 1458, 1438, 9, k=tt.NATIVE * 0.9))

    # ---- slab: centred three-tier title ----
    SX, SY, SW, SH = px(78), px(1114), px(1467), px(452)
    el("slab", SX - px(6), SY - px(12), SW + px(12), SH + px(24))
    LOC = 1114                                             # slab's unrotated outer top, ref px
    def tier(txt, size_px, cap_top, tag, fam='StretchPro', wt=400):
        stroke, ls = (tt.SG_STROKE, tt.SG_LS) if fam == 'SigmarOne' else (tt.ST_STROKE, tt.ST_LS)
        feat = 'normal' if fam == 'SigmarOne' else tt.ST_FEAT
        # absolute children measure from INSIDE the 28px border (the padding box), so subtract it
        top = px(cap_top - LOC - 28) - BOX * size_px
        return (f'<div style="position:absolute;left:0;width:100%;text-align:center;top:{top}px;font-family:{fam};font-weight:{wt};'
                f'color:{INK};-webkit-text-stroke:{stroke * size_px}px {INK};letter-spacing:{ls}em;font-feature-settings:{feat};font-size:{size_px}px;line-height:1;white-space:nowrap">{txt}</div>')
    slab = (f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;'
            f'transform:rotate(-1.3deg);background:{SLAB};border:{px(28)}px solid {ORCHID};border-radius:{px(70)}px;z-index:8">'
            + tier(c["title"], title_px, 1170, "t") + tier(c["big"], big_px, 1268, "b") + tier(c["sub"], sub_px, 1430, "s", "SigmarOne", 400)
            + '</div>')

    # ---- info row (calendar + date, venue) centred ----
    FS = px(F_INFO)
    cal_w, ic_gap, grp_gap = px(84), px(6), px(50)
    total = cal_w + ic_gap + tw[5] + grp_gap + tw[6]
    x = (W - total) / 2 - px(4)
    LBL = f'font-family:var(--d);font-weight:400;font-size:{FS}px;line-height:1;color:{WHITE};white-space:nowrap'
    ry = 1610 - BOX * F_INFO
    cal = (f'<svg class="measure" data-tag="cal" style="position:absolute;left:{x}px;top:{px(1601)}px;z-index:6" width="{cal_w}" height="{px(84)}" viewBox="0 0 84 84">'
           f'<rect x="6" y="14" width="72" height="64" rx="10" fill="{CREAM_HALO}"/><rect x="6" y="14" width="72" height="20" rx="8" fill="{ORCHID}"/>'
           f'<rect x="20" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/><rect x="56" y="4" width="8" height="18" rx="4" fill="{CREAM_HALO}"/>'
           f'<rect x="18" y="44" width="14" height="12" rx="3" fill="{INK}"/><rect x="38" y="44" width="14" height="12" rx="3" fill="{INK}"/>'
           f'<rect x="58" y="44" width="10" height="12" rx="3" fill="{INK}"/></svg>')
    el("cal", x, px(1601), cal_w, px(84))
    dx = x + cal_w + ic_gap
    vx = dx + tw[5] + grp_gap
    info = (cal + f'<div class="measure" data-tag="date" style="position:absolute;left:{dx}px;top:{px(ry)}px;{LBL}">{c["date"].replace("&", "&amp;")}</div>'
            f'<div class="measure" data-tag="venue" style="position:absolute;left:{vx}px;top:{px(ry)}px;{LBL}">{c["venue"]}</div>')
    el("date", dx, px(1610), tw[5], px(CAP * F_INFO)); el("venue", vx, px(1610), tw[6], px(CAP * F_INFO))

    # ---- body: three bold lines, centred, cap tops 1690 / 1749 / 1808 ----
    body = ""
    for i, line in enumerate(c["body"]):
        cap_top = 1690 + i * 59
        body += (f'<div class="measure" data-tag="body{i}" style="position:absolute;left:{px(300)}px;width:{px(1000)}px;text-align:center;'
                 f'top:{px(cap_top) - BOX * body_px}px;font-family:var(--d);font-weight:900;font-size:{body_px}px;line-height:1;color:{WHITE};'
                 f'white-space:nowrap;z-index:6">{line}</div>')
        el(f"body{i}", px(300), px(cap_top), px(1000), px(50))

    # ---- footer ----
    lh = px(83)
    logo = f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{px(40)}px;top:{px(1888)}px;height:{lh}px;z-index:9">'
    el("logo", px(40), px(1888), px(475), lh)
    cx, cy, cw, ch = px(1068), px(1880), px(500), px(100)
    el("cta", cx, cy, cw, ch)
    cta = (f'<div class="measure" data-tag="cta" style="position:absolute;left:{cx}px;top:{cy}px;width:{cw}px;height:{ch}px;'
           f'border:{px(9)}px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;'
           f'z-index:9;font-family:var(--d);font-weight:900;font-size:{px(44)}px;color:{INK}">{c["cta"]}</div>')

    grp = lambda g, h_: f'<div style="position:absolute;left:0;top:{DY[g]}px;width:{W}px;height:{H}px">{h_}</div>'
    els[:] = [(l, x, y + DY.get(GROUP_OF.get(l, ""), 0), w_, h_) for (l, x, y, w_, h_) in els]
    html = B.page(W, Hc, GROUND, f'<style>{tt.FONT_CSS}</style>' + ground + grp("hdr", hdr) + grp("hero", hero + stars) + grp("slab", slab)
                  + grp("info", info + body) + grp("foot", logo + cta), grain=False)
    text_pairs = [("ask", WHITE, GROUND, 96, True), ("body", WHITE, GROUND, 48, True), ("info", WHITE, GROUND, 40, False),
                  ("title", INK, SLAB, 100, True), ("cta", INK, CTA_FILL, 34, True)]
    await B.render(html, out, W, Hc, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND,
                   expect_hero=True, collision_ignore={("hero", "slab"), ("star_br", "slab"), ("star_ml", "slab")}, margin=12,
                   bleed_tags=("star_br",))   # the reference star sits 5px from the right edge


async def main():
    os.makedirs("out/versions/terrathon_minifete", exist_ok=True)
    out = f"out/versions/terrathon_minifete/v{os.environ.get('TT_V', '1')}.png"
    async with B.session():
        await build(CONTENT, out)
        os.makedirs("out/collaterals/stories", exist_ok=True)
        await build(CONTENT, "out/collaterals/stories/minifete_story.png", canvas="story")
    print("done", out)

if __name__ == "__main__":
    asyncio.run(main())
