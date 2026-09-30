"""TerraThon x Disco Diwali: the QR / "scan to pay" poster (Workflow C, TerraThon format).

Reference (user, 2026-09-30): the TerraThon registration QR poster (logo, title, one giant QR on a white plate,
four shuriken, sport stickers along the bottom). User answers: "use the same QR as the ref" and "add price + line of copy".

The QR is a REAL asset the user supplied: a static UPI merchant QR (payee TERRAROOTS, Kolkata, no amount embedded).
It was decoded out of the screenshot, regenerated crisp at engine/assets/terrathon/qr_terrathon_upi.png, and the
regenerated image was decoded back to the IDENTICAL payload (see the check at the bottom of main()). The payload is
never edited: no amount is injected, so a buyer types 550 themselves. Nothing about the payee is printed on the poster.

Same skeleton as tt_dd_tickets.py (black ground, shuriken, slab, drawn die-cut stickers) and it borrows those builders.
Adaptations (CLAUDE.md sec 2 rule 4): the sport stickers are swapped for the DD trio (ball, diya, ticket); title is the
event ("DISCO DIWALI") instead of TERRATHON; the header carries "LIMITED TICKETS ON SALE" and a slab carries the price.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_qr.py
"""
import asyncio, base64, importlib.util, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scratchpad", fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
dd = _load("tt_dd_tickets", "tt_dd_tickets.py")
tt, core, B, px, W, H = dd.tt, dd.core, dd.B, dd.px, dd.W, dd.H
GROUND, ORCHID, HALO, SLAB, INK, WHITE = dd.GROUND, dd.ORCHID, dd.HALO, dd.SLAB, dd.INK, dd.WHITE
CAP, BOX = dd.CAP, dd.BOX
QR_PNG = "engine/assets/terrathon/qr_terrathon_upi.png"
QY, PLATE = 292, 528
MODULES = 57                      # version 10; the plate keeps a 4-module quiet zone on every side


async def build(out):
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    m = await B.measure_text([
        dict(text="DISCO DIWALI", font="d", size=104, weight=900),
        dict(text="LIMITED TICKETS ON SALE", font="d", size=40, weight=400),
        dict(text="RS. 550", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
        dict(text="SCAN TO PAY", font="SigmarOne", size=40, weight=400, letter_spacing=f"{tt.SG_LS}em"),
    ], extra_css=tt.FONT_CSS)
    tw = [r["text_w"] for r in m]

    import random
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" '
                     f'fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>',
             f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    # ---- logo + title ----
    lh = 64; lw = lh * 5.72
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{(W - lw) / 2}px;top:36px;height:{lh}px;z-index:9">')
    el("logo", (W - lw) / 2, 36, lw, lh)
    t1 = min(104, 104 * 800 / tw[0]); t1w = tw[0] * t1 / 104
    parts.append(f'<div class="measure" data-tag="title" style="position:absolute;left:{(W - t1w) / 2}px;width:{t1w + 4}px;top:{118 - BOX * t1}px;text-align:center;color:{WHITE};'
                 f'font-family:var(--d);font-weight:900;font-size:{t1}px;line-height:1;white-space:nowrap;z-index:6">DISCO DIWALI</div>')
    el("title", (W - t1w) / 2, 118, t1w, t1 * 0.95)
    t2 = 40; t2w = tw[1]
    parts.append(f'<div class="measure" data-tag="sub" style="position:absolute;left:{(W - t2w) / 2}px;width:{t2w + 4}px;top:{118 + t1 * .9 + 18 - BOX * t2}px;text-align:center;color:{ORCHID};'
                 f'font-family:var(--d);font-weight:400;font-size:{t2}px;line-height:1;white-space:nowrap;z-index:6">LIMITED TICKETS ON SALE</div>')
    el("sub", (W - t2w) / 2, 118 + t1 * .9 + 18, t2w, t2 * CAP)

    # ---- the QR plate: white, rounded, orchid keyline; 4-module quiet zone around the 57-module code ----
    qy, plate = QY, PLATE
    mod = 8                                             # css px per module: 57 * 8 = 456, plate inner leaves the quiet zone
    code = MODULES * mod; qz = (plate - code) / 2       # >= 4 modules on each side (4 * 8 = 32)
    assert qz >= 4 * mod, "quiet zone under 4 modules: the code will not scan reliably"
    qx = (W - plate) / 2
    src = "data:image/png;base64," + base64.b64encode(open(QR_PNG, "rb").read()).decode()
    parts.append(f'<div class="measure" data-tag="qr" style="position:absolute;left:{qx}px;top:{qy}px;width:{plate}px;height:{plate}px;background:#fff;border-radius:34px;'
                 f'box-shadow:0 0 0 7px {ORCHID};z-index:8"><img src="{src}" style="position:absolute;left:{qz}px;top:{qz}px;width:{code}px;height:{code}px;image-rendering:pixelated"></div>')
    el("qr", qx - 7, qy - 7, plate + 14, plate + 14)

    # ---- four shuriken, the series' furniture ----
    def shuriken(label, x, y, z=5, k=tt.NATIVE * 0.9):
        im, s = tt.crop_to_alpha("shuriken.png"); w, h = im.width * k * 0.675, im.height * k * 0.675; el(label, x, y, w, h)
        return (f'<img src="{s}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">')
    parts += [shuriken("s_tl", 46, 318), shuriken("s_tr", 908, 344), shuriken("s_mr", 924, 690), shuriken("s_bl", 34, 660)]

    # ---- slab: price + SCAN TO PAY ----
    SW, SH = 620, 190; SX, SY = (W - SW) / 2, 852
    pp = 100 * 470 / tw[2]; ppw = tw[2] * pp / 100                 # price numerals ~470 css px wide
    sp = 40 * min(1.0, 400 / tw[3])
    parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;transform:rotate(-1.3deg);background:{SLAB};'
                 f'border:19px solid {ORCHID};border-radius:48px;z-index:8">'
                 f'<div style="position:absolute;left:0;width:100%;text-align:center;top:{20 - BOX * pp}px;font-family:StretchPro;color:{INK};-webkit-text-stroke:{tt.ST_STROKE * pp}px {INK};'
                 f'letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{pp}px;line-height:1;white-space:nowrap">RS. 550</div>'
                 f'<div style="position:absolute;left:0;width:100%;text-align:center;top:{112 - BOX * sp}px;font-family:SigmarOne;color:{INK};-webkit-text-stroke:{tt.SG_STROKE * sp}px {INK};'
                 f'letter-spacing:{tt.SG_LS}em;font-size:{sp}px;line-height:1;white-space:nowrap">SCAN TO PAY</div></div>')
    el("slab", SX - 4, SY - 10, SW + 8, SH + 20)

    # ---- DD sticker trio along the bottom (ball centre, diya + ticket flanking, all IN FRONT of the slab's tail) ----
    ball_w = 280; ball, ball_h = dd.disco_ball(ball_w); bx, by = (W - ball_w) / 2, 1326 - ball_h
    dya, dya_h = dd.diya(190); dxp, dyp = 112, 1316 - dya_h
    tk, tk_h = dd.ticket(240); tx, ty = 738, 1300 - tk_h
    box = lambda x, y, svg, z, rot=0, tag="": f'<div class="measure" data-tag="{tag}" style="position:absolute;left:{x}px;top:{y}px;z-index:{z};transform:rotate({rot}deg)">{svg}</div>'
    parts += [box(bx, by, ball, 4, 0, "ball"), box(dxp, dyp, dya, 6, -8, "diya"), box(tx, ty, tk, 6, 12, "ticket")]
    el("ball", bx, by, ball_w, ball_h); el("diya", dxp - 10, dyp - 12, 214, 204); el("ticket", tx - 12, ty - 22, 264, 190)

    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    text_pairs = [("title", WHITE, GROUND, 96, True), ("sub", ORCHID, GROUND, 40, False), ("price", INK, SLAB, 100, True), ("scan", INK, SLAB, 40, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=text_pairs, containers=("slab", "qr"), page_bg=GROUND, expect_hero=True, margin=12,
                   collision_ignore={("ball", "diya"), ("ball", "ticket"), ("diya", "ticket")})


async def main():
    os.makedirs("out/versions/terrathon_dd_qr", exist_ok=True)
    out = f"out/versions/terrathon_dd_qr/v{os.environ.get('TT_V', '1')}.png"
    async with B.session():
        await build(out)
    # the QR must still decode to the user's original payload after being drawn on the poster
    try:
        import cv2
        img = cv2.imread(out); h, w = img.shape[:2]; s = w / W
        x0, y0, n = int(((W - PLATE) / 2 - 20) * s), int((QY - 20) * s), int((PLATE + 40) * s)
        got, _, _ = cv2.QRCodeDetector().detectAndDecode(img[y0:y0 + n, x0:x0 + n])
        want = cv2.QRCodeDetector().detectAndDecode(cv2.copyMakeBorder(cv2.imread(QR_PNG), 80, 80, 80, 80, cv2.BORDER_CONSTANT, value=(255, 255, 255)))[0]
        print("POSTER QR DECODES TO ORIGINAL PAYLOAD:", bool(got) and got == want)
    except ImportError:
        print("opencv missing: QR decode check SKIPPED (do not ship unverified)")
    print("done", out)

if __name__ == "__main__":
    asyncio.run(main())
