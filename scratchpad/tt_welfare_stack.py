"""TerraThon-look WELFARE IMPACT stories, v9 (2026-10-20). History: v5's card tucked over the photo circle; the user asked for no overlap, no empty space inside the cards, NeutralFace
only (v6), "move the pills and the logos to the header and footer" (v7), less empty space top and bottom of the story (v8), then (v9, this file): add the AQ LIVE logo, logos and
ALL FOR CHARITY in the bottom footer, the slide number beside the photo like before, and SMALLER photos.
  STACK, not tuck: photo circle, then the card BELOW it with a real gap. Nothing overlaps anything (the n/7 badge sits off the circle's bbox corner, outside the circle).
  CARD SIZED FROM ITS CONTENT: every text block is measured (build.measure_text, in the real face); the card's height is content + padding, so no dead space inside it.
  SMALLER PHOTOS WITHOUT EMPTY BANDS: the circle is capped lower (Dmax) and the freed height is spent on bigger card type (K per canvas), not on dead space.
  HEADER: a caption (left), one shuriken, a SINCE 2021 pill (right).   FOOTER: AQ logo (left), AQ LIVE logo (centre), ALL FOR CHARITY pill (right). The n/7 badge sits beside the photo.
  NEUTRALFACE ONLY: headlines 900, body 400. No StretchPro, no Sigmar One, anywhere.
Content is v3's: no project counts, only the user's round directory figures (4,000+ / 3,500+ / 15,000+). Photos and copy rules are in tt_welfare_stories.py's docstring
(this file imports its photo set); photos are git-ignored, people incl. minors: confirm consent.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_welfare_stack.py [feed story]   ->  out/versions/terrathon_carousel/welfare9/<canvas>/NN_<key>.png
"""
import asyncio, importlib.util, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("ws", os.path.join(ROOT, "scratchpad", "tt_welfare_stories.py"))
ws = importlib.util.module_from_spec(spec); spec.loader.exec_module(ws)          # loads the photo set; renders nothing (its main is guarded)
tc = ws.tc; tt = tc.tt; B = tt.B; core = tt.core
GROUND, ORCHID, CREAM_HALO, SLAB, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL

CANV = {   # hy = header row top, foot_y = footer row top; R0..R1 = the band circle + card live in, clear of both rows. K = type scale (the room smaller photos free goes to bigger card type)
    "feed":  dict(W=1080, H=1350, hy=44, foot_y=1240, R0=140, R1=1188, Dmax=600, Dmin=380, K=1.12),
    "story": dict(W=1080, H=1920, hy=104, foot_y=1744, R0=232, R1=1700, Dmax=700, Dmin=420, K=1.42),   # header/footer stay at the edges (v8); Instagram's UI safe zones are given up on purpose
}
SX, SW, BORDER, PADY, PADX = 90, 900, 19, 30, 36
INNER = SW - 2 * BORDER - 2 * PADX          # 790: the width the card's text may use
G1 = 40                                     # circle->card gap (the card tilts, so it needs air)
PILL_H = 81

PH = lambda k: (ws.PHOTOS.get(k) or [(None,)])[0][0]
SLIDES = [   # kind: cover | all | pillar | close.  lines = explicit headline breaks; stats = big-number blocks; tag = one short line
    dict(kind="cover", key="cover", lines=["AQUATERRA", "IMPACT"], base=118, tag="SEVEN WAYS WE SHOW UP.", cap="SWIPE TO SEE", photo=ws.COVER),
    dict(kind="all", key="all", lines=["THE IMPACT", "SO FAR"], base=92, stats=[("4,000+", "SAPLINGS PLANTED"), ("3,500+", "KIDS REACHED"), ("15,000+", "BANANAS DISTRIBUTED")], photo=PH("all")),
    dict(kind="pillar", key="children", n=1, lines=["CHILDREN +", "EDUCATION"], base=92, stats=[("3,500+", "KIDS REACHED")], photo=PH("children")),
    dict(kind="pillar", key="health", n=2, lines=["HEALTHCARE"], base=92, tag="FREE CAMPS, CHECKUPS AND BLOOD DRIVES.", photo=PH("health")),
    dict(kind="pillar", key="women", n=3, lines=["WOMEN", "EMPOWERMENT"], base=92, tag="PADS, PERIOD TALK AND MONEY SKILLS.", photo=PH("women")),
    dict(kind="pillar", key="elderly", n=4, lines=["ELDERLY"], base=92, tag="OLD AGE HOME VISITS. SOMEONE SHOWED UP.", photo=PH("elderly")),
    dict(kind="pillar", key="community", n=5, lines=["COMMUNITY", "WELFARE"], base=92, stats=[("15,000+", "BANANAS DISTRIBUTED")], photo=PH("community")),
    dict(kind="pillar", key="environment", n=6, lines=["ENVIRONMENT"], base=92, stats=[("4,000+", "SAPLINGS PLANTED")], photo=PH("environment")),
    dict(kind="pillar", key="animals", n=7, lines=["ANIMAL", "WELFARE"], base=92, tag="DINNER FOR STRAYS. ONE DRIVE AT A TIME.", photo=PH("animals")),
    dict(kind="close", key="close", lines=["COME TO", "THE NEXT ONE"], base=92, tag="@NGO.AQUATERRA", photo=ws.CLOSE),
]


async def size_card(s, K):
    """Measure every text block in NeutralFace and return the card's real height and the font sizes that fit INNER (type scaled by K, then fitted to the width)."""
    lines = s["lines"]; stats = s.get("stats", []); k = len(stats)
    items = [dict(text=t, font="d", size=100, weight=900) for t in lines]
    items += [dict(text=n, font="d", size=100, weight=900) for n, _ in stats]
    m = await B.measure_text(items)
    head_px = min(s["base"] * K, 100 * INNER / max(r["text_w"] for r in m[:len(lines)]))
    mg = round(20 * K)
    out = dict(head_px=head_px, head_h=head_px * len(lines), mg=mg)
    content = out["head_h"]
    if stats:
        gap = 16; cellw = (INNER - gap * (k - 1)) / k
        num_px = min((76 if k > 1 else 96) * K, 100 * cellw * 0.94 / max(r["text_w"] for r in m[len(lines):]))
        lab_px = round((27 if k > 1 else 34) * K)
        lm = await B.measure_text([dict(text=l, font="d", size=lab_px, weight=400, line_height=1.08, max_width=cellw) for _, l in stats])
        lab_h = max(r["h"] for r in lm)
        out.update(num_px=num_px, lab_px=lab_px, cellw=cellw, gap=gap, block_h=num_px + 8 + lab_h)
        content += mg + out["block_h"]
    if s.get("tag"):
        tag_px = round(38 * K)
        tm = await B.measure_text([dict(text=s["tag"], font="d", size=tag_px, weight=400, line_height=1.15, max_width=INNER)])
        out["tag_h"] = tm[0]["h"]; out["tag_px"] = tag_px; content += (mg if s["kind"] != "close" else round(mg * 0.7)) + out["tag_h"]
    out["slab_h"] = math.ceil(content + 2 * (PADY + BORDER))
    return out


def card_html(s, c, y):
    rows = "".join(f'<div style="font-weight:900;font-size:{c["head_px"]:.1f}px;line-height:1">{t}</div>' for t in s["lines"])
    if s.get("stats"):
        cells = "".join(f'<div style="flex:1;min-width:0;text-align:center"><div style="font-weight:900;font-size:{c["num_px"]:.1f}px;line-height:1">{n}</div>'
                        f'<div style="font-weight:400;font-size:{c["lab_px"]}px;line-height:1.08;margin-top:8px;white-space:normal">{l}</div></div>' for n, l in s["stats"])
        rows += f'<div style="display:flex;gap:{c["gap"]}px;width:100%;margin-top:{c["mg"]}px">{cells}</div>'
    if s.get("tag"):
        rows += (f'<div style="font-weight:400;font-size:{c["tag_px"]}px;line-height:1.15;margin-top:{c["mg"] if s["kind"] != "close" else round(c["mg"] * 0.7)}px;white-space:normal;'
                 f'text-wrap:balance;max-width:{INNER}px">{s["tag"]}</div>')      # balance: no stranded last word
    return (f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{y:.0f}px;width:{SW}px;height:{c["slab_h"]}px;box-sizing:border-box;'
            f'transform:rotate(-1.25deg);background:{SLAB};border:{BORDER}px solid {ORCHID};border-radius:47px;z-index:8;display:flex;flex-direction:column;align-items:center;'
            f'justify-content:center;text-align:center;font-family:var(--d);color:{INK};white-space:nowrap;padding:0 {PADX}px">{rows}</div>')


async def render_canvas(cv, sizes):
    P = CANV[cv]; W, H = P["W"], P["H"]
    _, star = tc.sticker_src("shuriken.png")
    live_im, live = tc.sticker_src("aq_live.png"); live_h = 104; live_w = round(live_h * live_im.width / live_im.height)
    for i, s in enumerate(SLIDES):
        c = sizes[s["key"]]; els = []
        el = lambda *a: els.append(a)
        D = int(max(P["Dmin"], min(P["Dmax"], P["R1"] - P["R0"] - (G1 + c["slab_h"]))))      # capped photo; whatever is left is centred, not stretched
        top = P["R0"] + (P["R1"] - P["R0"] - (D + G1 + c["slab_h"])) / 2; cx = W / 2
        slab_y = top + D + G1
        rnd = random.Random(7)
        specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(int(520 * H / 1350)))
        parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
                 tc.bg_collage(W, H, ws.BG, exclude=s["key"]), f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']
        # ---- middle: the photo circle, its n/7 badge, and the card ----
        if s["photo"]:
            parts.append(f'<div class="measure" data-tag="hero" style="position:absolute;left:{cx - D / 2:.0f}px;top:{top:.0f}px;width:{D}px;height:{D}px;border-radius:50%;border:14px solid {CREAM_HALO};'
                         f'background:{CREAM_HALO};z-index:3;overflow:hidden;box-sizing:border-box">{tc.collage_html([(s["photo"], "50% 50%")])}</div>')
        else:
            im, src = tc.sticker_src("carnival.png"); k = min(D / im.width, D / im.height)
            parts.append(f'<img class="measure" data-tag="hero" src="{src}" style="position:absolute;left:{cx - im.width * k / 2:.0f}px;top:{top:.0f}px;width:{im.width * k:.0f}px;height:{im.height * k:.0f}px;z-index:3">')
        el("hero", cx - D / 2, top, D, D)
        if s["kind"] == "pillar":      # beside the photo, as before: parked off the circle's bbox corner (its nearest point to the centre is outside the circle)
            nb = 108; nx, ny = cx - D / 2 - 34, top - 34; el("num_badge", nx, ny, nb, nb)
            parts.append(f'<div class="measure" data-tag="num_badge" style="position:absolute;left:{nx:.0f}px;top:{ny:.0f}px;width:{nb}px;height:{nb}px;border-radius:50%;background:#fff;border:8px solid {ORCHID};'
                         f'display:flex;align-items:center;justify-content:center;z-index:10;font-family:var(--d);font-weight:900;font-size:40px;color:{INK};line-height:1;transform:rotate(-8deg);box-sizing:border-box">{s["n"]}/7</div>')
        parts.append(card_html(s, c, slab_y)); el("slab", SX - 6, slab_y - 12, SW + 12, c["slab_h"] + 24)
        # ---- header: caption | shuriken | pill ----
        hy = P["hy"]; cap = s.get("cap") or tc.VENUE; cfs = 27
        cm = await B.measure_text([dict(text=cap, font="d", size=cfs, weight=400)]); cw_ = cm[0]["text_w"]
        parts.append(f'<div class="measure" data-tag="caption" style="position:absolute;left:27px;top:{hy + (PILL_H - cfs) // 2}px;font-family:var(--d);font-weight:400;font-size:{cfs}px;line-height:1;color:{WHITE};white-space:nowrap;z-index:6">{cap}</div>')
        el("caption", 27, hy + (PILL_H - cfs) // 2 + 2, cw_, cfs * 0.81)
        pw = 250; px_ = W - 27 - pw; sx_ = (27 + cw_ + px_ - 84) / 2
        parts.append(f'<img class="measure" data-tag="star_h" src="{star}" style="position:absolute;left:{sx_:.0f}px;top:{hy - 2}px;width:84px;height:84px;z-index:5">'); el("star_h", sx_, hy - 2, 84, 84)
        parts.append(f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{px_}px;top:{hy}px;width:{pw}px;height:{PILL_H}px;border:6px solid {ORCHID};border-radius:999px;'
                     f'background:#fff;display:flex;align-items:center;justify-content:center;z-index:7;font-family:var(--d);font-weight:900;font-size:32px;color:{INK};box-sizing:border-box">SINCE 2021</div>')
        el("fest_pill", px_, hy, pw, PILL_H)
        # ---- footer: AQ logo | AQ LIVE logo | ALL FOR CHARITY pill ----
        fy = P["foot_y"]; cy = fy + 34
        parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{cy - 28}px;height:56px;z-index:9">'); el("logo", 27, cy - 28, 323, 56)
        lx = (W - live_w) / 2
        parts.append(f'<img class="measure" data-tag="aq_live" src="{live}" style="position:absolute;left:{lx:.0f}px;top:{cy - live_h // 2}px;width:{live_w}px;height:{live_h}px;z-index:9">'); el("aq_live", lx, cy - live_h // 2, live_w, live_h)
        el("cta", 720, fy, 337, 67)
        parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:720px;top:{fy}px;width:337px;height:67px;border:6px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;'
                     f'align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:26px;color:{INK};box-sizing:border-box">ALL FOR CHARITY</div>')
        html = B.page(W, H, GROUND, "".join(parts), grain=False)
        d = f"out/versions/terrathon_carousel/welfare9/{cv}"; os.makedirs(d, exist_ok=True)
        text_pairs = [("slab", INK, SLAB, 40, False), ("cta", INK, CTA_FILL, 26, True), ("pill", INK, "#FFFFFF", 32, True), ("caption", WHITE, GROUND, 27, False)]
        await B.render(html, f"{d}/{i:02d}_{s['key']}.png", W, H, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=True, margin=12,
                       crop_tags=("bgc", "bgt", "hero"), bleed_tags=("bgc", "bgt"), collision_ignore={("num_badge", "hero")})
    print("done", cv, "cards", {k: v["slab_h"] for k, v in sizes.items()})


async def main(cvs):
    async with B.session():
        for cv in cvs:
            sizes = {s["key"]: await size_card(s, CANV[cv]["K"]) for s in SLIDES}
            await render_canvas(cv, sizes)

if __name__ == "__main__":
    asyncio.run(main([a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]))
