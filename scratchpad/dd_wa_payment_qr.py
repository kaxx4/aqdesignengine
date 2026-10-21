"""DISCO DIWALI WhatsApp PAYMENT QR poster, 1080x1350 (the WhatsApp poster size, see dd_launch_pack wa_poster).

The QR is the user's OWN supplied image, placed copy-paste (user, 2026-10-21: "use this qr, copy paste"): engine/assets/disco_diwali/qr_payment_user.png,
cropped to its content box and scaled, never redrawn. It decodes (zxing-cpp; OpenCV cannot read its rounded finders) to
upi://pay?pa=9073455396@hdfc&pn=AquaTerra&cu=INR&tn=Disco Diwali& , no amount. The build re-decodes the QR out of the RENDERED poster and refuses to
report success unless it equals PAYLOAD. TEST-SCAN with a payment app before posting.

Branding: the approved diya ground (black, navy and gold lotus corners fading to black, string lights, gold dust, film grain), the small
LIVE badge top left, off-white bold uppercase NeutralFace with a black stroke, the lockup (with its ball) as a footer mark. No pill, no link
(WhatsApp has nothing to point at). The QR sits on a paper plate with a 4-module quiet zone (a QR on black does not scan) and a gold keyline.
Hero: SCAN TO PAY. Copy is only supplied facts: EARLY BIRD RS. 450 (user, 2026-10-21; the code carries NO amount, so buyers type 450 themselves), the UPI ID (user, 2026-10-21, replaces the ALL FOR CHARITY line; the LIVE badge still says it), the date, venue and time in the user's wording (Tuesday, 10th November / 60, Chowringhee Banquets (on the rooftop) / 4:30 PM onwards; no year; drawn gold icons stand in for the emoji) and the venue (60, Chowringhee Banquets), all supplied. 
No price (unconfirmed, DISCO_DIWALI.md sec 1), no date, no venue.
Adaptation: the diya ground rather than the photo ground, so the plate is the only bright object and the code is the first thing the eye lands on.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_payment_qr.py [phase1]   ->  out/discodiwali/wa_payment_qr/poster.png
"""
import asyncio, base64, importlib.util, io, os, sys
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "wa_payment_qr")
# variant (user, 2026-10-21: "make for phase 1 Rs.550"): default is the Early Bird Rs. 450 poster; arg `phase1` makes the PHASE 1 Rs. 550 one
VARIANT = "phase1" if "phase1" in sys.argv else "earlybird"
LABEL, PRICE = ("Phase 1", "Rs. 550") if VARIANT == "phase1" else ("Early bird", "Rs. 450")
SLUG = "poster_phase1" if VARIANT == "phase1" else "poster"
UPI_ID = "9073455396@hdfc"
PAYLOAD = "upi://pay?pa=9073455396@hdfc&pn=AquaTerra&cu=INR&tn=Disco Diwali&"
QR_SRC = os.path.join(ROOT, "engine", "assets", "disco_diwali", "qr_payment_user.png")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GL = "#E8C063"
CODE = 385                                # css px of the cropped code
PLATE = 540                               # quiet zone (645-481)/2 = 82px, ~5.5 modules
PX, PY = (W - PLATE) // 2, 462


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

    def line(tag, txt, top, fsize, weight, h, w=1000, upper=True, font="--d"):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var({font});font-weight:{weight};font-size:{fsize}px;'
                     f'line-height:1;text-transform:{"uppercase" if upper else "none"};white-space:nowrap;{STROKE}z-index:20">{txt}</div>')
        els.append((tag, (W - w) // 2, top, w, h))
    # SCAN TO PAY is the hero, set across the frame; ALL FOR CHARITY sits under it
    line("head", "Scan to pay", 196, 120, 700, 120)
    # the price is the second voice (user, 2026-10-21: "450 needs to be more highlighted"): EARLY BIRD small, RS. 450 at 118px in gold with a glow
    glow = "text-shadow:0 0 34px rgba(240,198,90,.6);"
    line("price", f'{LABEL} <span style="font-size:118px;color:#F0C65A;{glow}">{PRICE}</span>', 330, 56, 700, 118, w=900)

    # the QR plate: paper, rounded, gold keyline, hard shadow; the code keeps a 4-module quiet zone
    qz = (PLATE - CODE) / 2
    g = np.array(Image.open(QR_SRC).convert("L")); ys, xs = np.where(g < 128)
    buf = io.BytesIO(); Image.open(QR_SRC).convert("RGB").crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).save(buf, "PNG")
    src = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    parts.append(f'<div data-tag="qr" style="position:absolute;left:{PX}px;top:{PY}px;width:{PLATE}px;height:{PLATE}px;background:#fff;border-radius:36px;'
                 f'box-shadow:0 0 0 8px {GL},0 22px 50px rgba(0,0,0,.7);z-index:12">'
                 f'<img src="{src}" style="position:absolute;left:{qz}px;top:{qz}px;width:{CODE}px;height:{CODE}px"></div>')
    els.append(("qr", PX - 8, PY - 8, PLATE + 16, PLATE + 16))

    # info block, small (user, 2026-10-21): the UPI ID, then the supplied date and venue (DISCO_DIWALI.md sec 1 and the location poster)
    iy = PY + PLATE + 16
    line("upi", UPI_ID, iy, 32, 700, 34, w=400, upper=False, font="--m")
    ico = lambda d: (f'<svg viewBox="0 0 24 24" width="26" height="26" style="vertical-align:-4px;margin-right:10px"><path fill="{GL}" fill-rule="evenodd" d="{d}"/></svg>')
    CAL = "M7 2h2v3H7zM15 2h2v3h-2zM4 5h16a2 2 0 012 2v13a2 2 0 01-2 2H4a2 2 0 01-2-2V7a2 2 0 012-2zm0 6v9h16v-9z"
    PIN = "M12 2a7 7 0 00-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"
    CLK = "M12 2a10 10 0 100 20 10 10 0 000-20zm1 5h-2v6l5 3 1-1.6-4-2.4z"
    # wording and order as supplied (user, 2026-10-21): date, venue (on the rooftop), time
    line("date", ico(CAL) + "Tuesday, 10th November", iy + 40, 24, 400, 26, w=470)
    line("venue", ico(PIN) + "60, Chowringhee Banquets (on the rooftop)", iy + 70, 24, 400, 26, w=760)
    line("time", ico(CLK) + "4:30 PM onwards", iy + 100, 24, 400, 26, w=340)

    # copper stickers (user, 2026-10-21: "add stickers as well"): the transparent PNGs from dd_sticker_export.py, one per free zone, none touching the code or type
    stk = os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers")
    for tag, fn, x, y, w, h in (("st_heart", "copper_heart.png", 858, 26, 182, round(182 * 1324 / 1496)),
                                ("st_diya", "copper_diya.png", 30, 1168, 262, round(262 * 1146 / 1870)),
                                ("st_star", "copper_star.png", 850, 1140, 190, 190)):
        uri = "data:image/png;base64," + base64.b64encode(open(os.path.join(stk, fn), "rb").read()).decode()
        parts.append(f'<img data-tag="{tag}" src="{uri}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:14;filter:drop-shadow(0 8px 14px rgba(0,0,0,.65))">')
        els.append((tag, x, y, w, h))

    # footer mark: the lockup with its ball, as on the date and location posters
    vw = 200; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = H - 40 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", round(vx - 265 * t + 0), round(vy - 320 * t + 0), round(2000 * t), round(1382 * t)))
    return "".join(parts), els, vy


def verify(path):
    import cv2, zxingcpp
    img = cv2.imread(path); s = img.shape[1] / W
    crop = img[int((PY - 24) * s):int((PY + PLATE + 24) * s), int((PX - 24) * s):int((PX + PLATE + 24) * s)]
    hits = []
    for f in (1.0, .75, .5, .35):
        c = crop if f == 1 else cv2.resize(crop, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        if any(r.text == PAYLOAD for r in zxingcpp.read_barcodes(c)):
            hits.append(f)
    print("PAYLOAD:", PAYLOAD, "| decoded from the poster at scales", hits)
    assert len(hits) >= 3, "QR on the poster does not decode to PAYLOAD at enough scales: DO NOT SHIP"


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, top = poster()
    print(f"footer mark starts at y={top} of {H}")
    out = os.path.join(OUT, SLUG + ".png")
    async with B.session():
        text_pairs = [("head", "#fff", "#000", 120, True), ("price", "#fff", "#000", 56, True), ("upi", "#fff", "#000", 32, True), ("date", "#fff", "#000", 24, False), ("venue", "#fff", "#000", 24, False), ("time", "#fff", "#000", 24, False)]
        await B.render(B.page(W, H, "#000", inner, grain=False), out, W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                       text_pairs=text_pairs, page_bg="#000", collision_ignore=[])
    verify(out)
    print("done ->", out)

asyncio.run(main())
