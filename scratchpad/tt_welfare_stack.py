"""TerraThon-look WELFARE IMPACT stories, v10 (2026-10-20). History: v5's card tucked over the photo circle; the user asked for no overlap, no empty space inside the cards, NeutralFace
only (v6), pills and logos in the header/footer (v7), less empty space top and bottom of the story (v8), AQ LIVE logo + smaller photos + slide number beside the photo (v9), then
(v10, this file): "dont mention numbers in any other slide other than the impact slide", "mention the different types of activities we perform in the different types of sectors",
"add the fact that we have took 8 trips to Sunderbans in the impact slide".
  NUMBERS ONLY ON THE IMPACT SLIDE: 4,000+ saplings planted, 3,500+ kids reached, 15,000+ bananas distributed, 8 trips to the Sundarbans (all the user's own figures: the directory page
    and the user's message; printed as given, never re-derived). No pillar slide carries a figure; the only digits elsewhere are the n/7 slide counter the user asked for.
  ACTIVITIES, per sector: each pillar card lists the user's own activity list for that sector (2026-10-19) as short chips. They are the user's account of what AQ does, not derived from
    the project table (which has no row for e.g. cleanup drives, blankets or water bowls); wording is shortened, nothing is added.
  STACK, not tuck: photo circle, then the card BELOW it with a real gap. CARD SIZED FROM ITS CONTENT (measured in NeutralFace; chip rows are wrapped in code so the height is known).
  HEADER: a caption (left), one shuriken, a pill (right: WHAT WE DO; SINCE 2021 only on the impact slide).  FOOTER: AQ logo, AQ LIVE logo, ALL FOR CHARITY.  The n/7 badge sits beside the photo.
  NEUTRALFACE ONLY. Photos: git-ignored, people incl. minors: confirm consent (see tt_welfare_stories.py).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_welfare_stack.py [feed story]   ->  out/versions/terrathon_carousel/welfare10/<canvas>/NN_<key>.png
"""
import asyncio, importlib.util, math, os, random, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("ws", os.path.join(ROOT, "scratchpad", "tt_welfare_stories.py"))
ws = importlib.util.module_from_spec(spec); spec.loader.exec_module(ws)          # loads the photo set; renders nothing (its main is guarded)
tc = ws.tc; tt = tc.tt; B = tt.B; core = tt.core
GROUND, ORCHID, CREAM_HALO, SLAB, INK, WHITE, CTA_FILL = tt.GROUND, tt.ORCHID, tt.CREAM_HALO, tt.SLAB, tt.INK, tt.WHITE, tt.CTA_FILL

CANV = {   # hy = header row top, foot_y = footer row top; R0..R1 = the band circle + card live in, clear of both rows. K = type scale
    "feed":  dict(W=1080, H=1350, hy=44, foot_y=1240, R0=140, R1=1188, Dmax=600, Dmin=340, K=1.0, KS=0.74),   # KS = scale of the impact slide's four figure cards (smaller on feed so the photo keeps room)
    "story": dict(W=1080, H=1920, hy=104, foot_y=1744, R0=232, R1=1700, Dmax=700, Dmin=420, K=1.3, KS=1.0),   # header/footer stay at the edges (v8); Instagram's UI safe zones are given up on purpose
}
SX, SW, BORDER, PADY, PADX = 90, 900, 19, 30, 36
INNER = SW - 2 * BORDER - 2 * PADX          # 790: the width the card's content may use
G1 = 40                                     # circle->card gap (the card tilts, so it needs air)
CARD_GAP = 30                               # headline card -> the stat cards under it (impact slide)
PILL_H = 81
CHIP_PADX, CHIP_PADY, CHIP_GAP = 20, 9, 10
OUT = "welfare10"                           # render folder under out/versions/terrathon_carousel/ (another deck, e.g. tt_why_stack.py, sets its own)
MORE_GAP = 40                              # air between the stat cards (they tilt) and the AND MANY MORE chip under them
MORE = "AND MANY MORE"                     # closes every sector's activity list (outlined chip) and the impact slide's figures

PH = lambda k: (ws.PHOTOS.get(k) or [(None,)])[0][0]
SLIDES = [   # kind: cover | all | pillar | close.  lines = explicit headline breaks; stats = big-number blocks (impact slide only); chips = the sector's activities; tag = one short line
    dict(kind="cover", key="cover", lines=["AQUATERRA", "IMPACT"], base=118, tag="SEVEN WAYS WE SHOW UP.", cap="SWIPE TO SEE", photo=ws.COVER),
    dict(kind="all", key="all", lines=["THE IMPACT SO FAR"], base=92, pill="SINCE 2021", photo=PH("all"),      # one line; the four figures are 4 separate cards under it
         stats=[("4,000+", "SAPLINGS PLANTED"), ("3,500+", "KIDS REACHED"), ("15,000+", "BANANAS DISTRIBUTED"), ("8", "TRIPS TO THE SUNDARBANS")]),
    dict(kind="pillar", key="children", n=1, lines=["CHILDREN +", "EDUCATION"], base=92, photo=PH("children"),
         chips=["TEACHING", "TUITION CLASSES", "ART WORKSHOPS", "CREATIVITY WORKSHOPS", "STATIONERY + BOOKS"]),
    dict(kind="pillar", key="health", n=2, lines=["HEALTHCARE"], base=92, photo=PH("health"),
         chips=["FREE MEDICAL CAMPS", "BLOOD DONATION", "HEALTH AWARENESS", "MENSTRUAL HYGIENE", "MEDICINE DISTRIBUTION", "DENTAL CHECKUPS"]),
    dict(kind="pillar", key="women", n=3, lines=["WOMEN", "EMPOWERMENT"], base=92, photo=PH("women"),
         chips=["NAPKIN DONATION", "PERIOD WORKSHOPS", "SKILL BUILDING", "FINANCIAL LITERACY"]),
    dict(kind="pillar", key="elderly", n=4, lines=["ELDERLY"], base=92, photo=PH("elderly"),
         chips=["OLD AGE HOME VISITS", "HEALTH CHECKUPS", "FOOD + ESSENTIALS", "MEDICINE DONATION"]),
    dict(kind="pillar", key="community", n=5, lines=["COMMUNITY", "WELFARE"], base=92, photo=PH("community"),
         chips=["FOOD", "CLOTHES", "BLANKETS", "NOTEBOOKS", "BANANAS", "SHARBAT", "TOYS", "PANDEMIC RELIEF"]),
    dict(kind="pillar", key="environment", n=6, lines=["ENVIRONMENT"], base=92, photo=PH("environment"),
         chips=["PLANTATION DRIVES", "CLEANUP DRIVES", "WASTE AWARENESS", "RECYCLING + UPCYCLING", "SUSTAINABLE WORKSHOPS"]),
    dict(kind="pillar", key="animals", n=7, lines=["ANIMAL", "WELFARE"], base=92, photo=PH("animals"),
         chips=["DOG + CAT FEEDING", "WATER BOWLS"]),
    dict(kind="close", key="close", lines=["COME TO", "THE NEXT ONE"], base=92, tag="@NGO.AQUATERRA", photo=ws.CLOSE),
]


for _s in SLIDES:
    if _s.get("chips"): _s["chips"] = _s["chips"] + [MORE]


async def size_card(s, K, KS=1.0):
    """Measure every block in NeutralFace; return the card's real height and the sizes that fit INNER (type scaled by K, then fitted to the width)."""
    lines = s["lines"]; stats = s.get("stats", []); chips = s.get("chips", [])
    items = [dict(text=t, font="d", size=100, weight=900) for t in lines] + [dict(text=n, font="d", size=100, weight=900) for n, _ in stats]
    m = await B.measure_text(items)
    head_px = min(s["base"] * K, 100 * INNER / max(r["text_w"] for r in m[:len(lines)]))
    mg = round(20 * K)
    out = dict(head_px=head_px, head_h=head_px * len(lines), mg=mg)
    content = out["head_h"]
    if stats and s["kind"] == "all":                 # the impact slide: each figure is its OWN card (2x2), measured here, drawn by render_canvas
        gapx, gapy, sb, py2, px2 = 24, round(26 * KS), 14, round(22 * KS), 18
        cardw = (SW - gapx) / 2; inner = cardw - 2 * sb - 2 * px2
        num_px = min(80 * KS, 100 * inner * 0.94 / max(r["text_w"] for r in m[len(lines):])); lab_px = round(27 * KS)
        lm = await B.measure_text([dict(text=l, font="d", size=lab_px, weight=400, line_height=1.08, max_width=inner) for _, l in stats])
        card_h = math.ceil(num_px + 8 + max(r["h"] for r in lm) + 2 * (py2 + sb))
        stats_h = 2 * card_h + gapy                  # (no AND MANY MORE chip on the impact slide: the user removed it; it stays on the sector slides)
        out.update(sc=dict(gapx=gapx, gapy=gapy, sb=sb, cardw=cardw, card_h=card_h, num_px=num_px, lab_px=lab_px), stats_h=stats_h)
        stats = []                                   # nothing of it goes inside the headline card
    if stats:                                        # 4 stats go in a 2x2 grid so the numbers stay big; 1-3 stay in one row
        k = len(stats); cols = 2 if k == 4 else k; rows = math.ceil(k / cols); gap = 16
        cellw = (INNER - gap * (cols - 1)) / cols
        num_px = min((76 if k > 1 else 96) * K, 100 * cellw * 0.94 / max(r["text_w"] for r in m[len(lines):]))
        lab_px = round((27 if k > 1 else 34) * K)
        lm = await B.measure_text([dict(text=l, font="d", size=lab_px, weight=400, line_height=1.08, max_width=cellw) for _, l in stats])
        cell_h = num_px + 8 + max(r["h"] for r in lm); rgap = round(16 * K)
        out.update(num_px=num_px, lab_px=lab_px, cols=cols, gap=gap, cell_h=cell_h, rgap=rgap, block_h=rows * cell_h + (rows - 1) * rgap)
        content += mg + out["block_h"]
    if chips:                                        # wrap the chips into rows ourselves, so the card height is known, not guessed
        chip_px = round(27 * K); cm = await B.measure_text([dict(text=t, font="d", size=chip_px, weight=900) for t in chips])
        widths = [r["text_w"] + 2 * CHIP_PADX for r in cm]; chip_h = chip_px + 2 * CHIP_PADY
        rows_, cur, curw = [], [], 0
        for t, w in zip(chips, widths):
            if cur and curw + CHIP_GAP + w > INNER: rows_.append(cur); cur, curw = [], 0
            curw += (CHIP_GAP if cur else 0) + w; cur.append((t, w))
        rows_.append(cur)
        out.update(chip_px=chip_px, chip_h=chip_h, chip_rows=rows_, chips_h=len(rows_) * chip_h + (len(rows_) - 1) * CHIP_GAP)
        content += mg + out["chips_h"]
    if s.get("rows"):                                # a brief: one "NAME + what it is" line per row, all one size, fitted to the card width
        mi = []
        for a, b in s["rows"]: mi += [dict(text=a, font="d", size=100, weight=900), dict(text=b, font="d", size=100, weight=400)]
        mr = await B.measure_text(mi)
        names_w = max(mr[2 * i]["text_w"] for i in range(len(s["rows"]))); descs_w = max(mr[2 * i + 1]["text_w"] for i in range(len(s["rows"])))
        row_px = min(34 * K, 100 * INNER / (names_w + descs_w + 110)); rgap_r = round(row_px * 0.42)      # 110 = the dot column and its two gaps at 100px (a 3-column grid)
        out.update(row_px=row_px, rgap_r=rgap_r, rows_h=len(s["rows"]) * row_px + (len(s["rows"]) - 1) * rgap_r); content += mg + out["rows_h"]
    if s.get("tag"):
        tag_px = round(38 * K)
        tm = await B.measure_text([dict(text=s["tag"], font="d", size=tag_px, weight=400, line_height=1.15, max_width=INNER)])
        out["tag_h"] = tm[0]["h"]; out["tag_px"] = tag_px; content += (mg if s["kind"] != "close" else round(mg * 0.7)) + out["tag_h"]
    out["slab_h"] = math.ceil(content + 2 * (PADY + BORDER))
    out["total_h"] = out["slab_h"] + ((CARD_GAP + out["stats_h"]) if "stats_h" in out else 0)     # headline card + (impact slide) the stat cards under it
    return out


def card_html(s, c, y):
    rows = "".join(f'<div style="font-weight:900;font-size:{c["head_px"]:.1f}px;line-height:1">{t}</div>' for t in s["lines"])
    if s.get("stats") and "sc" not in c:             # (the impact slide's figures are drawn as separate cards by render_canvas)
        st = s["stats"]; cols = c["cols"]; grid = ""
        for r0 in range(0, len(st), cols):
            cells = "".join(f'<div style="flex:1;min-width:0;text-align:center"><div style="font-weight:900;font-size:{c["num_px"]:.1f}px;line-height:1">{n}</div>'
                            f'<div style="font-weight:400;font-size:{c["lab_px"]}px;line-height:1.08;margin-top:8px;white-space:normal">{l}</div></div>' for n, l in st[r0:r0 + cols])
            grid += f'<div style="display:flex;gap:{c["gap"]}px;width:100%;margin-top:{c["mg"] if r0 == 0 else c["rgap"]}px">{cells}</div>'
        rows += grid
    if s.get("chips"):
        rows += f'<div style="margin-top:{c["mg"]}px;display:flex;flex-direction:column;align-items:center;gap:{CHIP_GAP}px">'
        for row in c["chip_rows"]:
            rows += f'<div style="display:flex;gap:{CHIP_GAP}px;justify-content:center">' + "".join(
                f'<div style="height:{c["chip_h"]}px;width:{w:.0f}px;box-sizing:border-box;border-radius:999px;background:{"#fff" if t == MORE else ORCHID};{"border:4px solid " + ORCHID + ";" if t == MORE else ""}color:{INK};display:flex;align-items:center;justify-content:center;'
                f'font-weight:900;font-size:{c["chip_px"]}px;line-height:1;white-space:nowrap">{t}</div>' for t, w in row) + '</div>'
        rows += '</div>'
    if s.get("rows"):
        rows += (f'<div style="margin-top:{c["mg"]}px;display:grid;grid-template-columns:auto auto auto;justify-content:center;align-items:baseline;column-gap:0.4em;row-gap:{c["rgap_r"]}px;'
                 f'font-size:{c["row_px"]:.1f}px;line-height:1;white-space:nowrap">' + "".join(
            f'<div style="font-weight:900;text-align:right">{a}</div><div style="font-weight:400">·</div><div style="font-weight:400;text-align:left">{b}</div>' for a, b in s["rows"]) + '</div>')
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
        D = int(max(P["Dmin"], min(P["Dmax"], P["R1"] - P["R0"] - (G1 + c["total_h"]))))      # capped photo; whatever is left is centred, not stretched
        top = P["R0"] + (P["R1"] - P["R0"] - (D + G1 + c["total_h"])) / 2; cx = W / 2
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
        if s["kind"] == "pillar":      # beside the photo: parked off the circle's bbox corner (its nearest point to the centre is outside the circle)
            nb = 108; nx, ny = cx - D / 2 - 34, top - 34; el("num_badge", nx, ny, nb, nb)
            parts.append(f'<div class="measure" data-tag="num_badge" style="position:absolute;left:{nx:.0f}px;top:{ny:.0f}px;width:{nb}px;height:{nb}px;border-radius:50%;background:#fff;border:8px solid {ORCHID};'
                         f'display:flex;align-items:center;justify-content:center;z-index:10;font-family:var(--d);font-weight:900;font-size:40px;color:{INK};line-height:1;transform:rotate(-8deg);box-sizing:border-box">{s["n"]}/{s.get("of", 7)}</div>')
        parts.append(card_html(s, c, slab_y)); el("slab", SX - 6, slab_y - 12, SW + 12, c["slab_h"] + 24)
        if "sc" in c:                  # impact slide: the four figures, each in its own card (2x2), tilted a touch the way the headline card is
            sc = c["sc"]; y0 = slab_y + c["slab_h"] + CARD_GAP
            for j, (n, lab) in enumerate(s["stats"]):
                col, row = j % 2, j // 2; x = SX + col * (sc["cardw"] + sc["gapx"]); y = y0 + row * (sc["card_h"] + sc["gapy"]); tilt = -1.25 if col == 0 else 1.0
                parts.append(f'<div class="measure" data-tag="stat{j}" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;width:{sc["cardw"]:.0f}px;height:{sc["card_h"]}px;box-sizing:border-box;transform:rotate({tilt}deg);'
                             f'background:{SLAB};border:{sc["sb"]}px solid {ORCHID};border-radius:36px;z-index:8;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;'
                             f'font-family:var(--d);color:{INK};padding:0 18px"><div style="font-weight:900;font-size:{sc["num_px"]:.1f}px;line-height:1;white-space:nowrap">{n}</div>'
                             f'<div style="font-weight:400;font-size:{sc["lab_px"]}px;line-height:1.08;margin-top:8px;text-wrap:balance">{lab}</div></div>')
                el(f"stat{j}", x - 6, y - 8, sc["cardw"] + 12, sc["card_h"] + 16)
        # ---- more sparkle stickers: shuriken in the free gaps either side of the photo (never on a card, never on the badge; unrotated, as the kit rule says) ----
        gl = cx - D / 2
        for tag, side, fy_, sz in (("star_a", "L", 0.58, 96), ("star_b", "R", 0.14, 104), ("star_c", "R", 0.70, 74)):
            if gl < sz + 24: continue
            sx2 = (gl - sz) / 2 if side == "L" else cx + D / 2 + (gl - sz) / 2; sy2 = top + fy_ * D
            parts.append(f'<img class="measure" data-tag="{tag}" src="{star}" style="position:absolute;left:{sx2:.0f}px;top:{sy2:.0f}px;width:{sz}px;height:{sz}px;z-index:5">'); el(tag, sx2, sy2, sz, sz)
        # ---- header: caption | shuriken | pill ----
        hy = P["hy"]; cap = s.get("cap") or tc.VENUE; cfs = 27
        cm = await B.measure_text([dict(text=cap, font="d", size=cfs, weight=400)]); cw_ = cm[0]["text_w"]
        parts.append(f'<div class="measure" data-tag="caption" style="position:absolute;left:27px;top:{hy + (PILL_H - cfs) // 2}px;font-family:var(--d);font-weight:400;font-size:{cfs}px;line-height:1;color:{WHITE};white-space:nowrap;z-index:6">{cap}</div>')
        el("caption", 27, hy + (PILL_H - cfs) // 2 + 2, cw_, cfs * 0.81)
        pw = 250; px_ = W - 27 - pw; sx_ = (27 + cw_ + px_ - 84) / 2
        parts.append(f'<img class="measure" data-tag="star_h" src="{star}" style="position:absolute;left:{sx_:.0f}px;top:{hy - 2}px;width:84px;height:84px;z-index:5">'); el("star_h", sx_, hy - 2, 84, 84)
        parts.append(f'<div class="measure" data-tag="fest_pill" style="position:absolute;left:{px_}px;top:{hy}px;width:{pw}px;height:{PILL_H}px;border:6px solid {ORCHID};border-radius:999px;'
                     f'background:#fff;display:flex;align-items:center;justify-content:center;z-index:7;font-family:var(--d);font-weight:900;font-size:32px;color:{INK};box-sizing:border-box">{s.get("pill", "WHAT WE DO")}</div>')
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
        d = f"out/versions/terrathon_carousel/{OUT}/{cv}"; os.makedirs(d, exist_ok=True)
        text_pairs = [("slab", INK, SLAB, 40, False), ("cta", INK, CTA_FILL, 26, True), ("pill", INK, "#FFFFFF", 32, True), ("caption", WHITE, GROUND, 27, False), ("chip", INK, ORCHID, 24, True)]
        await B.render(html, f"{d}/{i:02d}_{s['key']}.png", W, H, elements=els, text_pairs=text_pairs, containers=("slab",), page_bg=GROUND, expect_hero=True, margin=12,
                       crop_tags=("bgc", "bgt", "hero"), bleed_tags=("bgc", "bgt"), collision_ignore={("num_badge", "hero")})
    print("done", cv, "cards", {k: v["slab_h"] for k, v in sizes.items()})


async def main(cvs):
    async with B.session():
        for cv in cvs:
            sizes = {s["key"]: await size_card(s, CANV[cv]["K"], CANV[cv]["KS"]) for s in SLIDES}
            await render_canvas(cv, sizes)

if __name__ == "__main__":
    asyncio.run(main([a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]))
