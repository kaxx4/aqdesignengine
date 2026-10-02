"""AQ INSTAGRAM follow poster with a scannable QR, single page A4 PORTRAIT (210x297mm), TerraThon branding. PDF + 300dpi PNG.
QR: made with segno (error correction H) from https://www.instagram.com/ngo.aquaterra/ (the AQ account named in the TerraThon site footer; the second AQ account
there is @aquaterra.live; @crftd.lab is CRFTD's account as given by the user, 2026-10-01 and NOT independently verified to exist). It is a REAL, decoded code: the build decodes the code on its own, then checks the final rendered PNG two ways and
refuses to finish if either fails: every module is sampled and compared with the true QR matrix (must be 0 differences), and OpenCV must decode it at >=3 of 7 sizes
(its detector is flaky at some single sizes, so one scale is not a fair gate). The code sits on a cream plate with a 4-module quiet zone, dark modules on light, because
a QR on black does not scan reliably. Copy: TERRATHON / SCAN TO FOLLOW / NGO AQUATERRA ON INSTAGRAM / @NGO.AQUATERRA. No claims about content, follower counts or giveaways.
PRINT CAVEAT: full-bleed black A4, ~12mm safe margin, no bleed/crop marks; the QR itself is vector (SVG) so it prints sharp. Ask the printer for a bleed proof.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/tt_ig_qr_poster.py [ngo.aquaterra|aquaterra.live|crftd.lab|cravella_kolkata|artilyindia|shikshaq.in]   ->  out/collaterals/aq_instagram_qr_A4.pdf + .png
"""
import asyncio, base64, importlib.util, os, random, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core = tt.core
import io, segno, cv2, numpy as np
from PIL import Image
from playwright.async_api import async_playwright

ACCOUNT = sys.argv[1] if len(sys.argv) > 1 else "ngo.aquaterra"
URL = f"https://www.instagram.com/{ACCOUNT}/"
SUBS = {"ngo.aquaterra": "NGO AQUATERRA ON INSTAGRAM", "aquaterra.live": "AQUATERRA LIVE ON INSTAGRAM", "crftd.lab": "CRFTD ON INSTAGRAM", "cravella_kolkata": "CRAVE\u2019LLA ON INSTAGRAM", "artilyindia": "ARTILY ON INSTAGRAM", "shikshaq.in": "SHIKSHAQ ON INSTAGRAM"}
SUB = SUBS[ACCOUNT]                      # copy per account (user, 2026-10-01: "NGO", not "TEAM"; aquaterra.live asked for separately)
SLUG = {"ngo.aquaterra": "aq_instagram_qr_A4", "aquaterra.live": "aq_live_instagram_qr_A4", "crftd.lab": "crftd_instagram_qr_A4", "cravella_kolkata": "cravella_instagram_qr_A4", "artilyindia": "artily_instagram_qr_A4", "shikshaq.in": "shikshaq_instagram_qr_A4"}[ACCOUNT]
HANDLE_PX = {"cravella_kolkata": 34}.get(ACCOUNT, 40)
GROUND, ORCHID, GREEN, CREAM_HALO, CARD, INK, WHITE = "#000000", "#DE68F0", "#2FD284", "#F3ECDE", "#F5EEE1", "#0A0A0A", "#F5F5F5"
_im, STAR = tt.crop_to_alpha("shuriken.png")


def decode(img_bgr):
    return cv2.QRCodeDetector().detectAndDecode(img_bgr)[0]

q = segno.make(URL, error="h", micro=False)
buf = io.BytesIO(); q.save(buf, kind="svg", scale=1, border=0, dark=INK, light=None); svg = buf.getvalue().decode()
QR = "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
tmp = io.BytesIO(); q.save(tmp, kind="png", scale=12, border=4)
assert decode(cv2.cvtColor(np.array(Image.open(io.BytesIO(tmp.getvalue())).convert("RGB")), cv2.COLOR_RGB2BGR)) == URL, "QR does not decode to the URL"
MODS = q.symbol_size(border=0)[0]
QR_PX = 400                         # on-page QR width; module = QR_PX / MODS
PAD = round(4 * QR_PX / MODS)       # 4-module quiet zone

rnd = random.Random(17)
SPECKS = "".join(f'<circle cx="{rnd.uniform(0, 794):.0f}" cy="{rnd.uniform(0, 1123):.0f}" r="{rnd.choice([.5, .6, .8, 1, 1.3, 1.6]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(330))

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>
{core.FONTS}
{tt.FONT_CSS}
@page {{ size:210mm 297mm; margin:0 }}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:{GROUND}}}
.page{{position:relative;width:210mm;height:297mm;overflow:hidden;background:{GROUND};font-family:'NeutralFace',sans-serif;color:{WHITE};text-align:center}}
.specks{{position:absolute;inset:0}}
.star{{position:absolute;width:84px;z-index:1}}
.t1{{position:absolute;left:0;right:0;top:62px;font-weight:400;font-size:30px;letter-spacing:.22em;color:{CREAM_HALO};z-index:2}}
.h1{{position:absolute;left:0;right:0;font-family:'StretchPro';color:{WHITE};letter-spacing:-.045em;font-feature-settings:'liga' 1,'dlig' 1;line-height:1;white-space:nowrap;z-index:2}}
.plate{{position:absolute;left:{(794 - (QR_PX + 2 * PAD + 24)) / 2}px;top:372px;width:{QR_PX + 2 * PAD + 24}px;height:{QR_PX + 2 * PAD + 24}px;background:{CARD};border:12px solid {ORCHID};border-radius:44px;display:flex;align-items:center;justify-content:center;z-index:2}}
.plate img{{width:{QR_PX}px;height:{QR_PX}px;display:block}}
.handle{{position:absolute;left:{(794 - 560) / 2}px;width:560px;background:{CARD};color:{INK};border:7px solid {ORCHID};border-radius:999px;font-weight:900;font-size:{HANDLE_PX}px;letter-spacing:.04em;padding:14px 0 12px;z-index:2;white-space:nowrap}}
.sub{{position:absolute;left:0;right:0;font-family:'SigmarOne';color:{ORCHID};-webkit-text-stroke:.8px {ORCHID};letter-spacing:-.01em;font-size:28px;white-space:nowrap;z-index:2}}
.aq{{position:absolute;left:0;right:0;bottom:50px;display:flex;justify-content:center;z-index:2}} .aq img{{height:52px}}
</style></head><body><div class="page" id="page">
<svg class="specks" viewBox="0 0 794 1123" preserveAspectRatio="none" width="100%" height="100%">{SPECKS}</svg>
<img class="star" src="{STAR}" style="left:40px;top:40px"><img class="star" src="{STAR}" style="right:44px;top:52px">
<div class="t1">TERRATHON</div>
<div class="h1" id="h1" style="top:122px">SCAN TO</div><div class="h1" id="h2" style="top:204px">FOL&zwnj;LOW</div>
<div class="sub" id="sub" style="top:306px">{SUB}</div>
<div class="plate" id="plate"><img src="{QR}"></div>
<div class="handle" id="handle" style="top:{372 + QR_PX + 2 * PAD + 24 + 34}px">@{ACCOUNT.upper()}</div>
<div class="aq"><img src="{core.LOGO}"></div>
</div></body></html>"""

FIT = """() => {
  const fit = (ids, target, strokeEm) => { ids.forEach(id => { document.getElementById(id).style.fontSize = '100px'; document.getElementById(id).style.display = 'inline-block'; });
    const w = Math.max(...ids.map(id => document.getElementById(id).getBoundingClientRect().width)); const px = 100 * target / w;
    ids.forEach(id => { const e = document.getElementById(id); e.style.display = 'block'; e.style.fontSize = px + 'px'; if (strokeEm) e.style.webkitTextStroke = (strokeEm * px) + 'px currentColor'; }); return px; };
  const a = fit(['h1', 'h2'], 590, 0.04);
  document.getElementById('h2').style.top = (122 + a * 1.03) + 'px';
  document.getElementById('sub').style.top = (122 + a * 2.06 + 18) + 'px';
  return a;
}"""

CHECK = """() => {
  const pr = document.getElementById('page').getBoundingClientRect(), bad = [];
  const sel = ['.t1', '.h1', '.sub', '.plate', '.handle', '.aq'];
  const boxes = {}; sel.forEach(s => document.querySelectorAll(s).forEach((e, i) => { const r = e.getBoundingClientRect(); boxes[s + i] = [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)];
    if (r.left < 20 || r.right > pr.right - 20 || r.bottom > pr.bottom - 20) bad.push([s + i, boxes[s + i]]); }));
  const hit = (a, b) => !(a[2] <= b[0] || b[2] <= a[0] || a[3] <= b[1] || b[3] <= a[1]); const k = Object.keys(boxes), ov = [];
  for (let i = 0; i < k.length; i++) for (let j = i + 1; j < k.length; j++) if (hit(boxes[k[i]], boxes[k[j]])) ov.push([k[i], k[j]]);
  return {bad, ov, boxes};
}"""


async def main():
    os.makedirs("out/collaterals", exist_ok=True)
    png = f"out/collaterals/{SLUG}.png"; pdf = f"out/collaterals/{SLUG}.pdf"
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 794, "height": 1123}, device_scale_factor=3.125)
        await pg.set_content(HTML); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(400)
        print("FIT", await pg.evaluate(FIT)); await pg.wait_for_timeout(100)
        r = await pg.evaluate(CHECK); print("bad", r["bad"], "overlaps", r["ov"]); print(r["boxes"])
        qb = await pg.evaluate("(() => { const r = document.querySelector('.plate img').getBoundingClientRect(); return [r.left, r.top, r.width]; })()")
        await pg.locator("#page").screenshot(path=png)
        await pg.pdf(path=pdf, width="210mm", height="297mm", print_background=True, margin=dict(top="0", right="0", bottom="0", left="0"))
        await br.close()
    img = cv2.imread(png); g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 1) DETERMINISTIC: sample the centre of every module in the rendered PNG and compare with the QR's true matrix.
    S = 3.125; M = q.matrix; n = len(M); x0, y0, w = qb[0] * S, qb[1] * S, qb[2] * S; mod = w / n
    mism = sum((g[int(y0 + (r + .5) * mod), int(x0 + (c + .5) * mod)] < 128) != bool(M[r][c]) for r in range(n) for c in range(n))
    # 2) A real reader at several sizes (OpenCV's detector is flaky at some single scales, so require several hits, not one).
    scales = (1.0, .75, .6, .5, .4, .35, .25)
    hits = [f for f in scales if decode(img if f == 1 else cv2.resize(img, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)) == URL]
    print(f"RENDER CHECK: {mism} of {n * n} modules differ from the true QR | OpenCV decodes at scales {hits}")
    assert mism == 0, "rendered QR modules differ from the generated QR"
    assert len(hits) >= 3, "rendered QR is not decoded at enough scales"
    d = open(pdf, "rb").read(); print("pdf pages:", len(re.findall(rb"/Type\s*/Page[^s]", d)))

asyncio.run(main())
