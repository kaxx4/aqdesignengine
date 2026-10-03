"""TerraThon CERTIFICATES: winner and runner_up (WHITE ground with a coloured keyline) and participant (white paper in a black flecked frame).
REVISION 3 (user, 2026-10-03): "make the background of the winner certificate and the runner-up certificate white" -> both are now on a white ground (PAPER #F9F9F9, the same
white as the participant paper) inside their coloured keyline; the black ground and flecks are gone. On white the cream wordmark/outline logic flips: ink outlines, ink text, the
rank (1ST / 2ND) sits on a gold / silver chip with ink type (gold type on white would be 1.6:1), the wordmark takes an ink stroke. Revision-2 text follows.

Model: the user's Paradox certificate set (wordmark, spaced "CERTIFICATE OF ..." line, fill-in lines,
signatory footer, faint globe watermark). One layout, three colour schemes:
  * winner      : FULL BLACK ground, solid orchid keyline, orchid wordmark, gold seal   (the sexy one)
  * runner_up   : FULL BLACK ground, blue keyline, cream wordmark, silver seal
  * participant : WHITE paper in a black flecked frame (the original white design), green seal

Revision 2 (user): "runner up" singular; rank (1ST / 2ND) set much bigger; the AQ LIVE sticker replaces the wordmark
logo; winner and runner up sit on a full black ground; the white design is for participants; TerraThon stickers used.

Adaptations (CLAUDE.md sec 2 rule 4):
  * Wordmark is StretchPro (the TerraThon title face), not Paradox's face.
  * ONE signatory (user brief): Kanishk Agarwal, Co-Founder and Trustee. Signature line left empty for a wet signature.
  * Stickers are the user's real kit files (engine/assets/terrathon), unrotated, die-cut halo intact. Never redrawn.
  * On black the ink outline / hard shadow of the craft layer cannot read, so outlines go CREAM and hard shadows take the
    variant's accent (core.outline_of logic, applied by hand).
  * Fields (name, event) are blank lines, fillable: --name "..." --event "..." on the CLI.
  * Faint globe watermark kept because the reference has one (advisory only).

Canvas: A4 landscape, 1123x794 CSS px, rendered at 3x (3369x2382, ~288 dpi). PDF is A4.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_certificate.py [--name "X" --event "Wicket Wars"] [winner|runner_up|participant ...]
"""
import asyncio, importlib.util, math, os, random, sys, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B = tt.core, tt.B
from PIL import Image

W, H = 1123, 794
F = 38                      # frame thickness (participant) / safe margin
INK, PAPER, WHITE, CREAM = "#0A0A0A", "#F9F9F9", "#F5F5F5", "#F3ECDE"
ORCHID, BLUE, GREEN, GOLD, SILVER = "#DE68F0", "#0396FF", "#2FD284", "#FFC700", "#D5D9E0"
CX = W / 2

VARIANTS = {
    "winner": dict(
        dark=True, light=True, cert="CERTIFICATE OF MERIT", verb="HAS PLACED", rank="1ST", rank_col=GOLD,
        keyline=ORCHID,
        title_fill=ORCHID, title_stroke=INK, title_shadow=GREEN, rule=ORCHID,
        seal=GOLD, seal_rim="#B98A00", ribbon=ORCHID, seal_shadow=ORCHID, seal_words=("WINNER", None)),
    "runner_up": dict(
        dark=True, light=True, cert="CERTIFICATE OF MERIT", verb="HAS PLACED", rank="2ND", rank_col=SILVER,
        keyline=BLUE,
        title_fill=BLUE, title_stroke=INK, title_shadow="#0B4F8A", rule=BLUE,
        seal=SILVER, seal_rim="#8C93A0", ribbon=BLUE, seal_shadow=BLUE, seal_words=("RUNNER", "UP")),
    "participant": dict(
        dark=False, cert="CERTIFICATE OF PARTICIPATION", verb="HAS PARTICIPATED", rank=None, rank_col=INK,
        keyline=None,
        title_fill=CREAM, title_stroke=INK, title_shadow=INK, rule=GREEN,
        seal=CREAM, seal_rim="#8C93A0", ribbon=GREEN, seal_shadow=INK, seal_words=("PARTICIPANT", None)),
}
FONT_CSS = tt.FONT_CSS


def seal_svg(v, size, oc):
    """Scalloped rosette + ribbon tails. Flat fills, outline colour `oc`, hard offset shadow in the variant's accent."""
    n, R, r = 20, 58, 52
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rad = R if i % 2 == 0 else r
        pts.append(f"{60 + rad * math.sin(a):.1f},{60 - rad * math.cos(a):.1f}")
    P = " ".join(pts)
    tails = (f'<path d="M34 96 L22 140 L40 130 L52 146 L58 100 Z" fill="{v["ribbon"]}" stroke="{oc}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M86 96 L98 140 L80 130 L68 146 L62 100 Z" fill="{v["ribbon"]}" stroke="{oc}" stroke-width="3" stroke-linejoin="round"/>')
    rosette = (f'<polygon points="{P}" fill="{v["seal_shadow"]}" transform="translate(4 4)"/>'
               f'<polygon points="{P}" fill="{v["seal"]}" stroke="{oc}" stroke-width="3" stroke-linejoin="round"/>'
               f'<circle cx="60" cy="60" r="43" fill="none" stroke="{v["seal_rim"]}" stroke-width="2.5"/>')
    return f'<svg width="{size}" height="{size * 150 / 120}" viewBox="0 0 120 150" style="overflow:visible">{tails}{rosette}</svg>'


async def build(name, out, fill_name="", fill_event=""):
    v = VARIANTS[name]
    light = v.get("light", False)          # white ground + coloured keyline (winner / runner up, revision 3)
    dark = v["dark"] and not light         # black ground (no variant uses it any more)
    TXT = WHITE if dark else INK
    SURF = "#000000" if dark else PAPER
    OC = CREAM if dark else INK           # outline colour: ink cannot read on black
    els = []

    def el(label, x, y, w, h): els.append((label, x, y, w, h))

    def sticker(fname, label, x, y, w, z=8):
        im, src = tt.crop_to_alpha(fname)
        h = w * im.height / im.width
        el(label, x, y, w, h)
        return (f'<img class="measure" data-tag="{label}" src="{src}" style="position:absolute;left:{x}px;top:{y}px;'
                f'width:{w}px;height:{h}px;z-index:{z}">')

    # ---- ground ---------------------------------------------------------------------------
    rnd = random.Random(11)
    if light:
        pts = []                           # white flecks would be invisible on white
    elif dark:
        pts = [(rnd.uniform(0, W), rnd.uniform(0, H)) for _ in range(26)]
    else:
        pts = [(rnd.uniform(0, W), rnd.uniform(0, H)) for _ in range(900)]
        pts = [(x, y) for x, y in pts if not (F < x < W - F and F < y < H - F)][:45]
    specks = (f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">'
              + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([.7, 1, 1.4, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for x, y in pts)
              + '</svg>')
    ground = ('' if (dark or light) else '<div style="position:absolute;inset:0;background:#000"></div>') + specks   # dark / light: the page itself is the ground
    if dark or light:
        K, KW = 20, 4          # keyline: ONE solid-border div (user: no gradient border)
        ground += (f'<div style="position:absolute;left:{K}px;top:{K}px;width:{W - 2 * K}px;height:{H - 2 * K}px;border:{KW}px solid {v["keyline"]};z-index:2"></div>')
    else:
        ground += (f'<div style="position:absolute;left:{F}px;top:{F}px;width:{W - 2 * F}px;height:{H - 2 * F}px;'
                   f'background:{PAPER};border:3px solid {INK};z-index:2"></div>')

    # watermark: light globe, no ink outline, centred behind the copy
    gs = 500
    wm = (f'<svg style="position:absolute;left:{CX - gs / 2}px;top:{H / 2 - gs / 2 + 34}px;z-index:3" width="{gs}" height="{gs}" viewBox="0 0 120 120" '
          f'fill="none" stroke="{v["rule"]}" stroke-width="1.6" opacity="{.16 if dark else .11}"><circle cx="60" cy="60" r="56"/><ellipse cx="60" cy="60" rx="24" ry="56"/>'
          f'<ellipse cx="60" cy="60" rx="46" ry="56"/><path d="M4 60H116M12 34H108M12 86H108"/></svg>')

    # ---- wordmark --------------------------------------------------------------------------
    TITLE_W = 520
    TLS = 0.012          # looser than the posters' -0.045: the thick outline fuses E and the stretched R at poster tracking
    m = await B.measure_text([dict(text="TERRATHON", font="StretchPro", size=100, weight=400,
                                   letter_spacing=f"{TLS}em", features=tt.ST_FEAT)], extra_css=FONT_CSS)
    tpx = 100 * TITLE_W / m[0]["text_w"]
    th = 0.72 * tpx
    ty = 70
    title = (f'<div class="measure" data-tag="title" style="position:absolute;left:{CX - TITLE_W / 2}px;top:{ty}px;width:{TITLE_W}px;height:{th}px;'
             f'text-align:center;z-index:6;font-family:StretchPro;font-size:{tpx}px;line-height:{th}px;white-space:nowrap;color:{v["title_fill"]};'
             f'-webkit-text-stroke:{tpx * 0.055}px {v["title_stroke"]};paint-order:stroke fill;letter-spacing:{TLS}em;font-feature-settings:{tt.ST_FEAT};'
             f'filter:drop-shadow(3px 4px 0 {v["title_shadow"]})">TERRATHON</div>')
    el("title", CX - TITLE_W / 2, ty, TITLE_W, th)
    shur = tt.b64_file("shuriken.png")
    for side, sx_ in (("l", CX - TITLE_W / 2 - 74), ("r", CX + TITLE_W / 2 + 16)):
        title += (f'<img class="measure" data-tag="tstar_{side}" src="{shur}" style="position:absolute;left:{sx_}px;top:{ty + th / 2 - 29}px;'
                  f'width:58px;height:58px;z-index:6">')
        el(f"tstar_{side}", sx_, ty + th / 2 - 29, 58, 58)

    sy = ty + th + 30
    sub = (f'<div class="measure" data-tag="sub" style="position:absolute;left:{CX - 250}px;width:500px;top:{sy}px;text-align:center;z-index:6;'
           f'font-family:var(--d);font-weight:900;font-size:17px;letter-spacing:.42em;text-indent:.42em;color:{TXT};line-height:1;white-space:nowrap">{v["cert"]}</div>')
    el("sub", CX - 250, sy, 500, 20)
    rules = "".join(f'<div style="position:absolute;left:{x}px;top:{sy + 9}px;width:70px;height:3px;background:{v["rule"]};z-index:6"></div>'
                    for x in (CX - 250 - 70 - 14, CX + 250 + 14))

    # ---- the fill-in lines -----------------------------------------------------------------
    LBL = f"font-family:var(--d);font-weight:400;font-size:22px;letter-spacing:.05em;color:{TXT};line-height:1;white-space:nowrap"
    FLD = (f"border-bottom:2px solid {TXT};height:34px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:3px;"
           f"font-family:var(--d);font-weight:900;font-size:23px;letter-spacing:.05em;color:{TXT};line-height:1")
    RW = 780; RX = CX - RW / 2
    r1y, r2y, r3y = 262, 330, 410
    row = lambda tag, y, h, inner: (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{RX}px;top:{y}px;width:{RW}px;height:{h}px;'
                                    f'display:flex;align-items:flex-end;gap:14px;z-index:6">{inner}</div>')
    rows = row("row1", r1y, 36, f'<span style="{LBL};padding-bottom:6px">THIS IS TO CERTIFY THAT</span><span style="{FLD};flex:1">{fill_name}</span>')
    RANK = (f"border-bottom:2px solid {TXT};height:58px;width:150px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:2px;"
            f"font-family:var(--d);font-weight:900;font-size:46px;letter-spacing:.03em;color:{v['rank_col']};line-height:1"
            + (f";background:{v['rank_col']};color:{INK};border-bottom:none;border-radius:12px" if light else ""))
    if v["rank"]:
        rows += row("row2", r2y - 22, 58, f'<span style="{LBL};padding-bottom:6px">{v["verb"]}</span><span style="{RANK}">{v["rank"]}</span>'
                                          f'<span style="{LBL};padding-bottom:6px">IN</span><span style="{FLD};flex:1">{fill_event}</span>'
                                          f'<span style="{LBL};padding-bottom:6px">AT</span>')
        el("row2", RX, r2y - 22, RW, 58)
    else:
        rows += row("row2", r2y, 36, f'<span style="{LBL};padding-bottom:6px">{v["verb"]} IN</span><span style="{FLD};flex:1">{fill_event}</span>'
                                     f'<span style="{LBL};padding-bottom:6px">AT</span>')
        el("row2", RX, r2y, RW, 36)
    rows += (f'<div class="measure" data-tag="row3" style="position:absolute;left:{RX}px;top:{r3y}px;width:{RW}px;text-align:center;z-index:6;{LBL}">'
             f'<b style="font-weight:900">TERRATHON 2026</b>, ORGANISED BY <b style="font-weight:900">AQUATERRA</b></div>')
    el("row1", RX, r1y, RW, 36); el("row3", RX, r3y, RW, 24)

    # ---- footer: AQ LIVE sticker | seal | signatory ---------------------------------------
    live = sticker("aq_live.png", "aq_live", 34, 592, 200, z=8)

    sz = 150
    sh = sz * 150 / 120
    seal_y = 488
    w1, w2 = v["seal_words"]
    fs = (sz / 132) * (13 if w2 else (15.5 if len(w1) <= 6 else 10.5))
    words = (f'<div style="position:absolute;left:0;top:{sz * 0.5 - fs * (1.0 if w2 else 0.6)}px;width:{sz}px;text-align:center;font-family:var(--d);font-weight:900;'
             f'font-size:{fs}px;line-height:1.05;letter-spacing:.03em;color:{INK}">{w1}{("<br>" + w2) if w2 else ""}</div>')
    seal = (f'<div class="measure" data-tag="seal" style="position:absolute;left:{CX - sz / 2}px;top:{seal_y}px;width:{sz}px;height:{sh}px;z-index:7">'
            f'{seal_svg(v, sz, OC)}{words}</div>')
    el("seal", CX - sz / 2, seal_y, sz, sh)

    sw = 290
    sx = W - F - 44 - sw
    sig_y = H - F - 108
    sig = (f'<div class="measure" data-tag="sig" style="position:absolute;left:{sx}px;top:{sig_y}px;width:{sw}px;z-index:6;text-align:center">'
           f'<div style="border-top:2px solid {TXT};margin-bottom:9px"></div>'
           f'<div style="font-family:var(--d);font-weight:900;font-size:17px;letter-spacing:.06em;color:{TXT};line-height:1">KANISHK AGARWAL</div>'
           f'<div style="font-family:var(--d);font-weight:400;font-size:13.5px;letter-spacing:.08em;color:{TXT};line-height:1;margin-top:7px">CO-FOUNDER AND TRUSTEE</div>'
           f'<div style="font-family:var(--d);font-weight:900;font-size:13.5px;letter-spacing:.08em;color:{TXT};line-height:1;margin-top:5px">NGO AQUATERRA</div></div>')
    el("sig", sx, sig_y, sw, 78)

    # ---- stickers: 3 green sport stickers + stars, on two aligned side columns (centres x=96 and x=W-96) ----
    LC, RC = 96, W - 96
    stk = (sticker("cricket_set.png", "stk_cricket", LC - 66, 30, 132)
           + sticker("pickleball_set.png", "stk_pickle", RC - 71, 30, 142)
           + sticker("controller.png", "stk_ctrl", LC - 64, 322, 128))
    for label, cxc, cyc, d in (("stk_star_r", RC, 366, 100),):
        stk += (f'<img class="measure" data-tag="{label}" src="{shur}" style="position:absolute;left:{cxc - d / 2}px;top:{cyc - d / 2}px;'
                f'width:{d}px;height:{d}px;z-index:8">')
        el(label, cxc - d / 2, cyc - d / 2, d, d)

    html = B.page(W, H, SURF, f'<style>{FONT_CSS}</style>' + ground + wm + title + sub + rules + rows + live + seal + sig + stk, grain=False)
    text_pairs = [("body", TXT, SURF, 22, False), ("sub", TXT, SURF, 17, True), ("sig", TXT, SURF, 13.5, False),
                  ("rank", INK if light else v["rank_col"], v["rank_col"] if light else SURF, 46, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, page_bg=SURF,
                   collision_ignore={("seal", "row3")}, margin=F,
                   bleed_tags=tuple(l for l, *_ in els if l.startswith("stk_") or l == "aq_live"))


def to_pdf(png, pdf):
    im = Image.open(png).convert("RGB")
    im.save(pdf, "PDF", resolution=im.width / (297 / 25.4))     # A4 landscape: 297mm wide


async def main(names, fill_name="", fill_event=""):
    d = "out/certificates"; os.makedirs(d, exist_ok=True)
    async with B.session(scale=3):
        for n in names:
            out = f"{d}/terrathon_certificate_{n}.png"
            await build(n, out, fill_name, fill_event)
            to_pdf(out, out.replace(".png", ".pdf"))
            print("done", out)


if __name__ == "__main__":
    a = sys.argv[1:]; kw = {}
    for flag, key in (("--name", "fill_name"), ("--event", "fill_event")):
        if flag in a:
            i = a.index(flag); kw[key] = a[i + 1]; del a[i:i + 2]
    asyncio.run(main(a or list(VARIANTS), **kw))
