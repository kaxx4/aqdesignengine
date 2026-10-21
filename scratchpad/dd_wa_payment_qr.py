"""DISCO DIWALI WhatsApp PAYMENT QR poster, 1080x1350 (the WhatsApp poster size, see dd_launch_pack wa_poster).

The QR is the user's REAL static UPI merchant code (payee TERRAROOTS, Kolkata, no amount embedded), the same asset as tt_dd_qr.py:
engine/assets/terrathon/qr_terrathon_upi.png, regenerated crisp from the decoded payload. The build re-decodes the QR out of the
RENDERED poster and refuses to report success unless it equals the asset's payload. The payload is never edited.

Branding: the approved diya ground (black, navy and gold lotus corners fading to black, string lights, gold dust, film grain), the small
LIVE badge top left, off-white bold uppercase NeutralFace with a black stroke, the lockup (with its ball) as a footer mark. No pill, no link
(WhatsApp has nothing to point at). The QR sits on a paper plate with a 4-module quiet zone (a QR on black does not scan) and a gold keyline.
Hero: SCAN TO PAY. Copy is only supplied facts: ALL FOR CHARITY and the payee name TERRAROOTS that the code itself carries.
No price (unconfirmed, DISCO_DIWALI.md sec 1), no date, no venue.
Adaptation: the diya ground rather than the photo ground, so the plate is the only bright object and the code is the first thing the eye lands on.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_payment_qr.py   ->  out/discodiwali/wa_payment_qr/poster.png
"""
import asyncio, base64, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "wa_payment_qr")
QR_PNG = os.path.join(ROOT, "engine", "assets", "terrathon", "qr_terrathon_upi.png")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GL = "#E8C063"
MODULES = 57
MOD = 8                                   # css px per module -> 456px code, whole pixels per module
PLATE = 540                               # plate leaves (540-456)/2 = 42px >= 4 modules (32px) of quiet zone
PX, PY = (W - PLATE) // 2, 430


def ground():
    return ('<div data-tag="plate" style="position:absolute;inset:0;z-index:0;background:#000"></div>'
            f'<img data-tag="plate" src="{dd.uri("bg_diya_portrait.jpg")}" style="position:absolute;left:0;top:0;width:{W}px;height:1350px;object-fit:cover;z-index:1">'
            f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">'
            f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:30;mix-blend-mode:screen;opacity:.55;pointer-events:none">'
            f'<img data-tag="plate" src="{dd.uri("grain.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:31;mix-blend-mode:screen;opacity:.35;pointer-events:none">')


def poster():
    parts, els = [ground()], []
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:40px;top:40px;width:150px;z-index:20">')
    els.append(("badge", 40, 40, 150, round(150 * 1005 / 1061)))

    def line(tag, txt, top, fsize, weight, h):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;'
                     f'line-height:1;text-transform:uppercase;white-space:nowrap;{STROKE}z-index:20">{txt}</div>')
        els.append((tag, 40, top, 1000, h))
    # SCAN TO PAY is the hero, set across the frame; ALL FOR CHARITY sits under it
    line("head", "Scan to pay", 215, 128, 700, 128)
    line("sub", "All for charity", 365, 40, 400, 42)

    # the QR plate: paper, rounded, gold keyline, hard shadow; the code keeps a 4-module quiet zone
    qz = (PLATE - MODULES * MOD) / 2
    assert qz >= 4 * MOD, "quiet zone under 4 modules: the code will not scan reliably"
    src = "data:image/png;base64," + base64.b64encode(open(QR_PNG, "rb").read()).decode()
    parts.append(f'<div data-tag="qr" style="position:absolute;left:{PX}px;top:{PY}px;width:{PLATE}px;height:{PLATE}px;background:#fff;border-radius:36px;'
                 f'box-shadow:0 0 0 8px {GL},0 22px 50px rgba(0,0,0,.7);z-index:12">'
                 f'<img src="{src}" style="position:absolute;left:{qz}px;top:{qz}px;width:{MODULES * MOD}px;height:{MODULES * MOD}px;image-rendering:pixelated"></div>')
    els.append(("qr", PX - 8, PY - 8, PLATE + 16, PLATE + 16))

    # payee line: the name the code itself carries, so a buyer can match it on their payment app
    line("payee", "Terraroots", PY + PLATE + 36, 64, 700, 64)

    # footer mark: the lockup with its ball, as on the date and location posters
    vw = 300; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = H - 40 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", round(vx - 265 * t + 0), round(vy - 320 * t + 0), round(2000 * t), round(1382 * t)))
    return "".join(parts), els, vy


def verify(path):
    import cv2
    det = cv2.QRCodeDetector()
    want = det.detectAndDecode(cv2.copyMakeBorder(cv2.imread(QR_PNG), 80, 80, 80, 80, cv2.BORDER_CONSTANT, value=(255, 255, 255)))[0]
    img = cv2.imread(path); s = img.shape[1] / W
    crop = img[int((PY - 24) * s):int((PY + PLATE + 24) * s), int((PX - 24) * s):int((PX + PLATE + 24) * s)]
    hits = []
    for f in (1.0, .75, .5, .35):
        c = crop if f == 1 else cv2.resize(crop, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        if want and det.detectAndDecode(c)[0] == want:
            hits.append(f)
    print("ASSET PAYLOAD DECODED:", bool(want), "| POSTER QR decodes to the exact payload at scales", hits)
    assert want and len(hits) >= 3, "QR on the poster does not decode to the asset payload at enough scales: DO NOT SHIP"


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, top = poster()
    print(f"footer mark starts at y={top} of {H}")
    out = os.path.join(OUT, "poster.png")
    async with B.session():
        text_pairs = [("head", "#fff", "#000", 128, True), ("sub", "#fff", "#000", 40, False), ("payee", "#fff", "#000", 64, True)]
        await B.render(B.page(W, H, "#000", inner, grain=False), out, W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                       text_pairs=text_pairs, page_bg="#000", collision_ignore=[])
    verify(out)
    print("done ->", out)

asyncio.run(main())
