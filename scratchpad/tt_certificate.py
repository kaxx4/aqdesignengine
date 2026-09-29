"""TerraThon CERTIFICATE template: WINNER and RUNNERS UP, one layout, two colour schemes.

Model: the user's Paradox certificate set (wordmark, spaced "CERTIFICATE OF ..." line, fill-in lines,
signatory footer, faint globe watermark, plain black frame vs a gradient frame). Same layout in both
TerraThon variants; only colour changes:
  * winner     : gradient frame (orchid > blue > green), orchid wordmark, gold seal
  * runners_up : black frame with white flecks, cream wordmark, silver seal

Adaptations (CLAUDE.md sec 2 rule 4):
  * Wordmark is StretchPro (the TerraThon title face, natural RR stretch), not Paradox's face.
  * ONE signatory (user brief): Kanishk Agarwal, Co-Founder and Trustee. The reference has two.
    The signature line is left empty for a wet signature; no signature is drawn or invented.
  * The seal sits centre-bottom; the AQ logo bottom-left. The reference has neither.
  * Fields (name, event) are blank lines, fillable: --name "..." --event "..." on the CLI.
  * Faint globe watermark kept because the reference has one (advisory wash_scan expected).

Canvas: A4 landscape, 1123x794 CSS px, rendered at 3x (3369x2382, ~288 dpi). PDF is A4.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_certificate.py [--name "X" --event "Wicket Wars"] [winner|runners_up ...]
"""
import asyncio, importlib.util, os, random, sys, base64

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B = tt.core, tt.B
dd = tt.load("doodles")
from PIL import Image

W, H = 1123, 794
F = 38                      # frame thickness
INK, PAPER = "#0A0A0A", "#F9F9F9"
CX = W / 2

VARIANTS = {
    "winner": dict(
        frame="linear-gradient(135deg,#DE68F0 0%,#0396FF 52%,#2FD284 100%)", flecks=False,
        title_fill="#DE68F0", seal="#FFC700", seal_rim="#B98A00", ribbon="#DE68F0",
        rank_word=("WINNER", None), rank="1ST", rule="#DE68F0"),
    "runners_up": dict(
        frame="#000000", flecks=True,
        title_fill="#F3ECDE", seal="#D5D9E0", seal_rim="#8C93A0", ribbon="#0396FF",
        rank_word=("RUNNERS", "UP"), rank="2ND", rule="#0396FF"),
}
FONT_CSS = tt.FONT_CSS
STAR_B64 = tt.b64_file("shuriken.png")


def seal_svg(v, size):
    """Scalloped rosette + ribbon tails. Flat fills, ink outline, hard offset shadow (house craft layer)."""
    import math
    n, R, r = 20, 58, 52
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rad = R if i % 2 == 0 else r
        pts.append(f"{60 + rad * math.sin(a):.1f},{60 - rad * math.cos(a):.1f}")
    tails = (f'<path d="M34 96 L22 140 L40 130 L52 146 L58 100 Z" fill="{v["ribbon"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M86 96 L98 140 L80 130 L68 146 L62 100 Z" fill="{v["ribbon"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    rosette = (f'<polygon points="{" ".join(pts)}" fill="{INK}" transform="translate(4 4)"/>'
               f'<polygon points="{" ".join(pts)}" fill="{v["seal"]}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
               f'<circle cx="60" cy="60" r="43" fill="none" stroke="{v["seal_rim"]}" stroke-width="2.5"/>')
    return (f'<svg width="{size}" height="{size * 150 / 120}" viewBox="0 0 120 150" style="overflow:visible">{tails}{rosette}</svg>')


async def build(name, out, fill_name="", fill_event=""):
    v = VARIANTS[name]
    els = []

    def el(label, x, y, w, h): els.append((label, x, y, w, h))

    # ---- frame + paper -------------------------------------------------------------------
    rnd = random.Random(11)
    specks = ""
    if v["flecks"]:
        pts = [(rnd.uniform(0, W), rnd.uniform(0, H)) for _ in range(900)]
        pts = [(x, y) for x, y in pts if not (F < x < W - F and F < y < H - F)][:120]
        specks = (f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">'
                  + "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.choice([.7, 1, 1.4, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.3, .85):.2f}"/>' for x, y in pts)
                  + '</svg>')
    ground = f'<div style="position:absolute;inset:0;background:{v["frame"]}"></div>' + specks
    paper = (f'<div style="position:absolute;left:{F}px;top:{F}px;width:{W - 2 * F}px;height:{H - 2 * F}px;'
             f'background:{PAPER};border:3px solid {INK};z-index:2"></div>')

    # watermark: the AQ globe, big and faint, centred behind the copy
    gs = 500
    wc = v["rule"]
    wm = (f'<svg style="position:absolute;left:{CX - gs / 2}px;top:{H / 2 - gs / 2 + 34}px;z-index:3" width="{gs}" height="{gs}" viewBox="0 0 120 120" '
          f'fill="none" stroke="{wc}" stroke-width="1.6" opacity=".11"><circle cx="60" cy="60" r="56"/><ellipse cx="60" cy="60" rx="24" ry="56"/>'
          f'<ellipse cx="60" cy="60" rx="46" ry="56"/><path d="M4 60H116M12 34H108M12 86H108"/></svg>')

    # ---- wordmark ------------------------------------------------------------------------
    TITLE_W = 600
    TLS = 0.012          # looser than the posters' -0.045: the thick outline fuses E and the stretched R at poster tracking
    m = await B.measure_text([dict(text="TERRATHON", font="StretchPro", size=100, weight=400,
                                   letter_spacing=f"{TLS}em", features=tt.ST_FEAT)], extra_css=FONT_CSS)
    tpx = 100 * TITLE_W / m[0]["text_w"]
    th = 0.72 * tpx
    ty = 74
    title = (f'<div class="measure" data-tag="title" style="position:absolute;left:{CX - TITLE_W / 2}px;top:{ty}px;width:{TITLE_W}px;height:{th}px;'
             f'text-align:center;z-index:6;font-family:StretchPro;font-size:{tpx}px;line-height:{th}px;white-space:nowrap;color:{v["title_fill"]};'
             f'-webkit-text-stroke:{tpx * 0.055}px {INK};paint-order:stroke fill;letter-spacing:{TLS}em;font-feature-settings:{tt.ST_FEAT};'
             f'filter:drop-shadow(3px 4px 0 {INK})">TERRATHON</div>')
    el("title", CX - TITLE_W / 2, ty, TITLE_W, th)
    star = lambda side: (f'<img class="measure" data-tag="tstar_{side}" src="{STAR_B64}" style="position:absolute;'
                         f'left:{(CX - TITLE_W / 2 - 96) if side == "l" else (CX + TITLE_W / 2 + 26)}px;top:{ty + th / 2 - 35}px;width:70px;height:70px;z-index:6">')
    title += star("l") + star("r")
    el("tstar_l", CX - TITLE_W / 2 - 96, ty + th / 2 - 35, 70, 70); el("tstar_r", CX + TITLE_W / 2 + 26, ty + th / 2 - 35, 70, 70)

    # spaced certificate line, with two rules either side
    sy = ty + th + 30
    sub = (f'<div class="measure" data-tag="sub" style="position:absolute;left:{CX - 190}px;width:380px;top:{sy}px;text-align:center;z-index:6;'
           f'font-family:var(--d);font-weight:900;font-size:17px;letter-spacing:.42em;text-indent:.42em;color:{INK};line-height:1;white-space:nowrap">CERTIFICATE OF MERIT</div>')
    el("sub", CX - 190, sy, 380, 20)
    rules = "".join(f'<div style="position:absolute;left:{x}px;top:{sy + 9}px;width:150px;height:3px;background:{v["rule"]};z-index:6"></div>'
                    for x in (CX - 190 - 150 - 22, CX + 190 + 22))

    # ---- the fill-in lines ---------------------------------------------------------------
    LBL = f"font-family:var(--d);font-weight:400;font-size:22px;letter-spacing:.05em;color:{INK};line-height:1;white-space:nowrap"
    FLD = (f"border-bottom:2px solid {INK};height:34px;display:flex;align-items:flex-end;justify-content:center;padding-bottom:3px;"
           f"font-family:var(--d);font-weight:900;font-size:23px;letter-spacing:.05em;color:{INK};line-height:1")
    RW, RX = 840, CX - 420
    r1y, r2y, r3y = 262, 336, 410
    row = lambda tag, y, inner: (f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{RX}px;top:{y}px;width:{RW}px;height:36px;'
                                 f'display:flex;align-items:flex-end;gap:14px;z-index:6">{inner}</div>')
    rows = row("row1", r1y, f'<span style="{LBL};padding-bottom:6px">THIS IS TO CERTIFY THAT</span><span style="{FLD};flex:1">{fill_name}</span>')
    rows += row("row2", r2y, f'<span style="{LBL};padding-bottom:6px">HAS PLACED</span><span style="{FLD};width:110px">{v["rank"]}</span>'
                             f'<span style="{LBL};padding-bottom:6px">IN</span><span style="{FLD};flex:1">{fill_event}</span>'
                             f'<span style="{LBL};padding-bottom:6px">AT</span>')
    rows += (f'<div class="measure" data-tag="row3" style="position:absolute;left:{RX}px;top:{r3y}px;width:{RW}px;text-align:center;z-index:6;{LBL}">'
             f'<b style="font-weight:900">TERRATHON 2026</b>, ORGANISED BY <b style="font-weight:900">AQUATERRA</b></div>')
    for t, y in (("row1", r1y), ("row2", r2y), ("row3", r3y)):
        el(t, RX, y, RW, 36)

    # ---- footer: logo | seal | signatory -------------------------------------------------
    lh = 46
    logo = (f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{F + 44}px;top:{H - F - 40 - lh}px;height:{lh}px;z-index:6">')
    el("logo", F + 44, H - F - 40 - lh, 250, lh)

    sz = 132
    sh = sz * 150 / 120
    seal_y = 492
    w1, w2 = v["rank_word"]
    words = (f'<div style="position:absolute;left:0;top:{sz * 0.5 - (12 if w2 else 8)}px;width:{sz}px;text-align:center;font-family:var(--d);font-weight:900;'
             f'font-size:{13 if w2 else 15.5}px;line-height:1.05;letter-spacing:.03em;color:{INK}">{w1}{("<br>" + w2) if w2 else ""}</div>')
    seal = (f'<div class="measure" data-tag="seal" style="position:absolute;left:{CX - sz / 2}px;top:{seal_y}px;width:{sz}px;height:{sh}px;z-index:7">'
            f'{seal_svg(v, sz)}{words}</div>')
    el("seal", CX - sz / 2, seal_y, sz, sh)

    sw = 290
    sx = W - F - 44 - sw
    sig_y = H - F - 108
    sig = (f'<div class="measure" data-tag="sig" style="position:absolute;left:{sx}px;top:{sig_y}px;width:{sw}px;z-index:6;text-align:center">'
           f'<div style="border-top:2px solid {INK};margin-bottom:9px"></div>'
           f'<div style="font-family:var(--d);font-weight:900;font-size:17px;letter-spacing:.06em;color:{INK};line-height:1">KANISHK AGARWAL</div>'
           f'<div style="font-family:var(--d);font-weight:400;font-size:13.5px;letter-spacing:.08em;color:{INK};line-height:1;margin-top:7px">CO-FOUNDER AND TRUSTEE</div>'
           f'<div style="font-family:var(--d);font-weight:900;font-size:13.5px;letter-spacing:.08em;color:{INK};line-height:1;margin-top:5px">NGO AQUATERRA</div></div>')
    el("sig", sx, sig_y, sw, 78)

    # ---- corner shuriken on the frame (the series trait: a star sits ON the edge) --------
    cs = 74
    corners = "".join(
        f'<img class="measure" data-tag="corner{i}" src="{STAR_B64}" style="position:absolute;left:{x}px;top:{y}px;width:{cs}px;height:{cs}px;z-index:9">'
        for i, (x, y) in enumerate([(-8, -8), (W - cs + 8, -8), (-8, H - cs + 8), (W - cs + 8, H - cs + 8)]))
    for i, (x, y) in enumerate([(-8, -8), (W - cs + 8, -8), (-8, H - cs + 8), (W - cs + 8, H - cs + 8)]):
        el(f"corner{i}", x, y, cs, cs)

    html = B.page(W, H, PAPER, f'<style>{FONT_CSS}</style>' + ground + paper + wm + title + sub + rules + rows + logo + seal + sig + corners, grain=False)
    text_pairs = [("body", INK, PAPER, 20, False), ("sub", INK, PAPER, 17, True), ("sig", INK, PAPER, 13.5, False)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, page_bg=PAPER,
                   bleed_tags=("corner0", "corner1", "corner2", "corner3"),
                   collision_ignore={("seal", "row3")}, margin=F)


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
