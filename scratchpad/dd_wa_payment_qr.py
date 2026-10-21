"""DISCO DIWALI WhatsApp PAYMENT QR poster, 1080x1350 (the WhatsApp poster size, see dd_launch_pack wa_poster).

The QR encodes the UPI ID the user supplied (2026-10-21: "9073455396@hdfc is UPI ID", "use the new qr code") as a standard UPI link,
upi://pay?pa=<id>&cu=INR (no payee name; user 2026-10-21: "remove terraroots"), with NO amount. The user's own QR image was never saved to disk, so this is regenerated from the ID, not
copied from their picture. UNVERIFIED: that "@hdfc" is a live handle (HDFC handles are usually @hdfcbank / @okhdfcbank). TEST-SCAN with a payment app.
The previous build used the old merchant QR (engine/assets/terrathon/qr_terrathon_upi.png, Vyapar.174068471103@hdfcbank). The build re-decodes the
QR out of the RENDERED poster and refuses to report success unless it equals PAYLOAD.

Branding: the approved diya ground (black, navy and gold lotus corners fading to black, string lights, gold dust, film grain), the small
LIVE badge top left, off-white bold uppercase NeutralFace with a black stroke, the lockup (with its ball) as a footer mark. No pill, no link
(WhatsApp has nothing to point at). The QR sits on a paper plate with a 4-module quiet zone (a QR on black does not scan) and a gold keyline.
Hero: SCAN TO PAY. Copy is only supplied facts: ALL FOR CHARITY and the UPI ID the user supplied.
No price (unconfirmed, DISCO_DIWALI.md sec 1), no date, no venue.
Adaptation: the diya ground rather than the photo ground, so the plate is the only bright object and the code is the first thing the eye lands on.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_wa_payment_qr.py   ->  out/discodiwali/wa_payment_qr/poster.png
"""
import asyncio, base64, importlib.util, io, os, sys
import segno
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "wa_payment_qr")
UPI_ID = "9073455396@hdfc"
PAYLOAD = f"upi://pay?pa={UPI_ID}&cu=INR"
Q = segno.make(PAYLOAD, error="m", micro=False)
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
GL = "#E8C063"
MODULES = Q.symbol_size(border=0)[0]
MOD = 13                                  # css px per module, whole pixels
PLATE = (MODULES + 8) * MOD               # a 4-module quiet zone on every side
PX, PY = (W - PLATE) // 2, 425


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
    line("head", "Scan to pay", 215, 128, 700, 128)
    line("sub", "All for charity", 365, 40, 400, 42, w=560)

    # the QR plate: paper, rounded, gold keyline, hard shadow; the code keeps a 4-module quiet zone
    qz = (PLATE - MODULES * MOD) / 2
    assert qz >= 4 * MOD, "quiet zone under 4 modules: the code will not scan reliably"
    buf = io.BytesIO(); Q.save(buf, kind="svg", scale=1, border=0, dark="#0A0A0A", light=None)
    src = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
    parts.append(f'<div data-tag="qr" style="position:absolute;left:{PX}px;top:{PY}px;width:{PLATE}px;height:{PLATE}px;background:#fff;border-radius:36px;'
                 f'box-shadow:0 0 0 8px {GL},0 22px 50px rgba(0,0,0,.7);z-index:12">'
                 f'<img src="{src}" style="position:absolute;left:{qz}px;top:{qz}px;width:{MODULES * MOD}px;height:{MODULES * MOD}px;shape-rendering:crispEdges"></div>')
    els.append(("qr", PX - 8, PY - 8, PLATE + 16, PLATE + 16))

    # UPI ID under the plate, so a buyer can type it if the scan fails
    line("upi", UPI_ID, PY + PLATE + 48, 46, 700, 48, w=480, upper=False, font="--m")

    # copper stickers (user, 2026-10-21: "add stickers as well"): the transparent PNGs from dd_sticker_export.py, one per free zone, none touching the code or type
    stk = os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers")
    for tag, fn, x, y, w, h in (("st_heart", "copper_heart.png", 836, 32, 204, round(204 * 1324 / 1496)),
                                ("st_diya", "copper_diya.png", 36, 1120, 300, round(300 * 1146 / 1870)),
                                ("st_star", "copper_star.png", 800, 1086, 236, 236)):
        uri = "data:image/png;base64," + base64.b64encode(open(os.path.join(stk, fn), "rb").read()).decode()
        parts.append(f'<img data-tag="{tag}" src="{uri}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:14;filter:drop-shadow(0 8px 14px rgba(0,0,0,.65))">')
        els.append((tag, x, y, w, h))

    # footer mark: the lockup with its ball, as on the date and location posters
    vw = 270; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = H - 40 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", round(vx - 265 * t + 0), round(vy - 320 * t + 0), round(2000 * t), round(1382 * t)))
    return "".join(parts), els, vy


def verify(path):
    import cv2
    det = cv2.QRCodeDetector()
    img = cv2.imread(path); s = img.shape[1] / W
    crop = img[int((PY - 24) * s):int((PY + PLATE + 24) * s), int((PX - 24) * s):int((PX + PLATE + 24) * s)]
    hits = []
    for f in (1.0, .75, .5, .35):
        c = crop if f == 1 else cv2.resize(crop, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
        if det.detectAndDecode(c)[0] == PAYLOAD:
            hits.append(f)
    print("PAYLOAD:", PAYLOAD, "| decoded from the poster at scales", hits)
    assert len(hits) >= 3, "QR on the poster does not decode to PAYLOAD at enough scales: DO NOT SHIP"


async def main():
    os.makedirs(OUT, exist_ok=True)
    inner, els, top = poster()
    print(f"footer mark starts at y={top} of {H}")
    out = os.path.join(OUT, "poster.png")
    async with B.session():
        text_pairs = [("head", "#fff", "#000", 128, True), ("sub", "#fff", "#000", 40, False), ("upi", "#fff", "#000", 46, True)]
        await B.render(B.page(W, H, "#000", inner, grain=False), out, W, H, elements=els, containers=(), bleed_tags=("plate",), crop_tags=("plate",),
                       text_pairs=text_pairs, page_bg="#000", collision_ignore=[])
    verify(out)
    print("done ->", out)

asyncio.run(main())
