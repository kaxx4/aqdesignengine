"""DISCO DIWALI TICKET STALL payment signage, single page A4 LANDSCAPE (297x210mm), TerraThon branding. PDF + 300dpi PNG.
QR: the user's own payment QR (image kept in engine/assets/terrathon/qr_dd_payment_terraroots_source.png). It decodes to a merchant payment code for TERRAROOTS, KOLKATA
(no fixed amount, so "just scan to pay" is true). The supplied image is only 742px and soft, so the build REGENERATES the code (segno, error M) from that exact decoded
string and refuses to finish unless the rendered modules match the regenerated matrix, the regenerated code decodes back to the identical string, and OpenCV decodes the
final PNG. Nothing in the payload is edited. The code sits dark-on-cream with a 4-module quiet zone (a QR on black does not scan reliably).
Copy: TERRATHON / SCAN TO PAY / DISCO DIWALI TICKET STALL / TERRAROOTS. No price (user), no UPI app claims, no date/venue.
PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; ask the printer for a bleed proof. TEST-SCAN THE PRINTED SHEET with a real payment app before the event.

CRFTD-stall variant: arg `crftd` (CRFTD logo circle instead of a sub line, same TERRAROOTS QR, files crftd_payment_qr_sign_A4_*).
Mini-Fete variant: add the arg `minifete` (sub line MINI-FETE, no TICKET STALL line, same TERRAROOTS QR, files minifete_payment_qr_sign_A4_*).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_pay_sign.py [portrait] [minifete]   ->  out/collaterals/dd_payment_qr_sign_A4_landscape.pdf + .png  (or ..._A4_portrait with the arg:
      the same pieces stacked in one centred column, smaller code (414px, ~109mm) so the stack fits)
"""
import asyncio, base64, importlib.util, io, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
import segno, cv2, numpy as np
from PIL import Image
from playwright.async_api import async_playwright

PAYLOAD = "000201010211021644038482021656080415522024082021656061661000308202165650825HDFC00000015020011163278526460010A0000005240128Vyapar.174068471103@hdfcbank27420010A0000005240124STQD295260117541249217725204829953033565802IN5910TERRAROOTS6007KOLKATA610670001562400524STQD2952601175412492177207088202165663045267"
SRC = "engine/assets/terrathon/qr_dd_payment_terraroots_source.png"
GROUND, ORCHID, CREAM_HALO, WHITE, CARD, INK = "#000000", "#DE68F0", "#F3ECDE", "#F5F5F5", "#F5EEE1", "#0A0A0A"
PORTRAIT = "portrait" in sys.argv
MINIFETE = "minifete" in sys.argv        # same verified payment QR, headline "MINI-FETE" (user, 2026-10-01: "TERRATHON MINI-FETE"; same TERRAROOTS QR)
CRFTD_ST = "crftd" in sys.argv          # CRFTD stall: the real CRFTD logo (partners/crftd.png) in an orchid-ringed circle replaces the sub line; same TERRAROOTS QR
SUB, STALL = ("MINI-FETE", None) if MINIFETE else (None, None) if CRFTD_ST else ("DISCO DIWALI", "TICKET STALL")
CRFTD_LOGO = "data:image/png;base64," + base64.b64encode(open("engine/assets/terrathon/partners/crftd.png", "rb").read()).decode() if CRFTD_ST else ""
W, H = (794, 1123) if PORTRAIT else (1123, 794)
PAGE_MM = "210mm 297mm" if PORTRAIT else "297mm 210mm"
SLUG = ("crftd_payment_qr_sign_A4_" if CRFTD_ST else "minifete_payment_qr_sign_A4_" if MINIFETE else "dd_payment_qr_sign_A4_") + ("portrait" if PORTRAIT else "landscape")
_im, STAR = tt.crop_to_alpha("shuriken.png")


def decode(img_bgr):
    return cv2.QRCodeDetector().detectAndDecode(img_bgr)[0]

# the supplied image must itself decode to PAYLOAD (provenance), padded because its quiet zone is thin
src = cv2.imread(SRC); src = cv2.copyMakeBorder(src, 80, 80, 80, 80, cv2.BORDER_CONSTANT, value=(255, 255, 255))
assert decode(src) == PAYLOAD, "supplied QR image no longer decodes to PAYLOAD"
q = segno.make(PAYLOAD, error="m", micro=False)
buf = io.BytesIO(); q.save(buf, kind="svg", scale=1, border=0, dark=INK, light=None)
QR = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
tmp = io.BytesIO(); q.save(tmp, kind="png", scale=12, border=4)
assert decode(cv2.cvtColor(np.array(Image.open(io.BytesIO(tmp.getvalue())).convert("RGB")), cv2.COLOR_RGB2BGR)) == PAYLOAD, "regenerated QR does not decode to PAYLOAD"
MODS = q.symbol_size(border=0)[0]
QR_PX = round((414 if PORTRAIT else 480) / MODS) * MODS            # whole pixels per module
PAD = round(4 * QR_PX / MODS)               # 4-module quiet zone
BORDER = 12; PLATE = QR_PX + 2 * PAD + 2 * BORDER
PX, PY = (W - PLATE) // 2, 0 if PORTRAIT else (H - PLATE) // 2 if False else 0
if not PORTRAIT: PX, PY = 62, (H - PLATE) // 2

rnd = random.Random(31)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(420))
CX, CW = (0, 590) if PORTRAIT else (PX + PLATE + 40, W - (PX + PLATE + 40) - 52)      # text column (portrait: full-width centred stack)

PLATE_HTML = f'<div class="plate" id="plate"><img id="qr" src="{QR}"></div>'
HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:{PAGE_MM}; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:{"210mm" if PORTRAIT else "297mm"};height:{"297mm" if PORTRAIT else "210mm"};overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE};text-align:center}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:78px;z-index:1}}
.plate{{{'position:relative;margin-top:' + ('26' if CRFTD_ST else '36') + 'px;flex:none;' if PORTRAIT else f'position:absolute;left:{PX}px;top:{PY}px;'}width:{PLATE}px;height:{PLATE}px;background:{CARD};border:{BORDER}px solid {ORCHID};border-radius:44px;display:flex;align-items:center;justify-content:center;z-index:2}}
.plate img{{width:{QR_PX}px;height:{QR_PX}px;display:block}}
.col{{position:absolute;left:{CX}px;width:{CW if not PORTRAIT else W}px;top:0;height:{H}px;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:2}}
.t1{{font-weight:400;font-size:30px;letter-spacing:.22em;color:{CREAM_HALO};white-space:nowrap}}
.h{{font-family:'StretchPro';color:{WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;line-height:1.02;white-space:nowrap;display:block}}
.sub{{font-family:'SigmarOne';color:{ORCHID};-webkit-text-stroke:.8px {ORCHID};letter-spacing:-.01em;line-height:1;white-space:nowrap;margin-top:{6 if PORTRAIT else 26}px}}
.stall{{font-weight:900;font-size:27px;letter-spacing:.1em;color:{WHITE};margin-top:12px;white-space:nowrap}}
.pill{{margin-top:28px;background:{CARD};color:{INK};border:7px solid {ORCHID};border-radius:999px;font-weight:900;font-size:30px;letter-spacing:.06em;padding:12px 30px 10px;white-space:nowrap}}
.logo{{width:132px;height:132px;border-radius:50%;border:6px solid {ORCHID};display:block;margin-top:18px;overflow:hidden;background:#FFF0DC}}
.logo img{{width:100%;height:100%;display:block;object-fit:cover;transform:scale(1.04)}}
.aq{{height:46px;display:block;margin-top:34px}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 {W} {H}" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="right:{24 if PORTRAIT else 40}px;top:{22 if PORTRAIT else 34}px;{"width:56px" if PORTRAIT else ""}"><img class="star" src="{STAR}" style="left:24px;top:22px;width:56px;display:{"block" if PORTRAIT else "none"}">
{"" if PORTRAIT else PLATE_HTML}
<div class="col" id="col"><div class="t1">TERRATHON</div>
<div style="margin-top:18px"><span class="h" id="h1">SCAN TO</span><span class="h" id="h2">PAY</span></div>
{f'<div class="sub" id="sub">{SUB}</div>' if SUB else ""}{f'<div class="logo" id="logo"><img src="{CRFTD_LOGO}"></div>' if CRFTD_ST else ""}{f'<div class="stall">{STALL}</div>' if STALL else ""}{PLATE_HTML if PORTRAIT else ""}
<div class="pill" id="pill">TERRAROOTS</div><img class="aq" src="{core.LOGO}"></div>
</div></body></html>"""

FIT = f"""() => {{
  const tw = e => {{ const r = document.createRange(); r.selectNodeContents(e); return r.getBoundingClientRect().width; }};
  const fit = (ids, target, strokeEm, cap = 1e9) => {{ const els = ids.map(i => document.getElementById(i)); els.forEach(e => {{ e.style.fontSize = '100px'; }});
    const px = Math.min(100 * target / Math.max(...els.map(tw)), cap); els.forEach(e => {{ e.style.fontSize = px + 'px'; if (strokeEm) e.style.webkitTextStroke = (strokeEm * px) + 'px currentColor'; }}); return px; }};
  return [fit(['h1', 'h2'], {CW}, 0.04), document.getElementById('sub') ? fit(['sub'], {CW}, 0.03, 70) : 0]; }}"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), bad = [], boxes = {};
  ['.plate', '.t1', '#h1', '#h2', '#sub', '#logo', '.pill', '.aq'].forEach(s => { const el = document.querySelector(s); if (!el) return; const r = el.getBoundingClientRect(); boxes[s] = [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
    if (r.left < 20 || r.top < 20 || r.right > pr.right - 20 || r.bottom > pr.bottom - 20) bad.push([s, boxes[s]]); });
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]); const k = Object.keys(boxes), ov = [];
  for (let i = 0; i < k.length; i++) for (let j = i + 1; j < k.length; j++) if (hit(boxes[k[i]], boxes[k[j]])) ov.push([k[i], k[j]]);
  const stars = [...document.querySelectorAll('.star')].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; });
  stars.forEach((s, i) => k.forEach(n => { if (hit(s, boxes[n])) ov.push(['star' + i, n]); }));
  return {bad, ov, boxes, stars};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    png = f"out/collaterals/{SLUG}.png"; pdf = f"out/collaterals/{SLUG}.pdf"
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": W, "height": H}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        r = await pg.evaluate(CHECK); print("bad", r["bad"], "overlaps", r["ov"]); print(r["boxes"], r["stars"])
        qb = await pg.evaluate("(() => { const r = document.getElementById('qr').getBoundingClientRect(); return [r.left, r.top, r.width]; })()")
        await pg.locator("#page").screenshot(path=png)
        await pg.pdf(path=pdf, width=PAGE_MM.split()[0], height=PAGE_MM.split()[1], print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    img = cv2.imread(png); g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    S = 3.125; M = q.matrix; n = len(M); x0, y0, w = qb[0] * S, qb[1] * S, qb[2] * S; mod = w / n
    mism = sum((g[int(y0 + (r + .5) * mod), int(x0 + (c + .5) * mod)] < 128) != bool(M[r][c]) for r in range(n) for c in range(n))
    scales = (1.0, .75, .6, .5, .4, .35, .25)
    hits = [f for f in scales if decode(img if f == 1 else cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)) == PAYLOAD]
    print(f"RENDER CHECK: {mism} of {n * n} modules differ from the true QR | OpenCV decodes the exact payload at scales {hits}")
    assert mism == 0, "rendered QR modules differ from the generated QR"
    assert len(hits) >= 3, "rendered QR is not decoded at enough scales"
    d = open(pdf, "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
