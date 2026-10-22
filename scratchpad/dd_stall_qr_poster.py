"""DISCO DIWALI STALL ADVANCE PAYMENT poster, WhatsApp feed 1080x1350 (user, 2026-10-22: "whatsapp poster QR for stalls advance payment").
Audience (user): STALL HOLDERS booking a stall pay an advance. Copy (user: "headline + date + venue only"): STALL ADVANCE PAYMENT / SCAN TO PAY / TUE, 10 NOV 2026 /
60, CHOWRINGHEE BANQUETS, ROOFTOP. No amount (the QR has none: the payer types it), no payee name, no deadline, no app claims.
QR: the user's own static merchant payment code (payee TERRAROOTS, Kolkata; the user ruled all payment QRs are TERRAROOTS). Regenerated crisp with segno (error M) from the
EXACT payload decoded out of their supplied image; the build refuses to finish unless (1) the supplied image still decodes to the payload, (2) the regenerated code decodes to it,
(3) the rendered poster's QR plate decodes to it at three scales. Dark on cream with a 4-module quiet zone (a QR on black does not scan reliably).
Skeleton = dd_charity.py: photo ground, LIVE badge top left, headline, lockup as the footer mark, no pill (a WhatsApp poster has no link to point at).
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_stall_qr_poster.py   ->  out/discodiwali/stall_qr/feed.png.  TEST-SCAN a real phone with a payment app before sending."""
import asyncio, base64, importlib.util, io, os, sys
import cv2, numpy as np, segno
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine")); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import dd_photo_bg as _pb
B = dd.B
W, H = 1080, 1350
OUT = os.path.join(ROOT, "out", "discodiwali", "stall_qr")
STROKE = "color:#fff;-webkit-text-stroke:4px #000;paint-order:stroke fill;"
PAYLOAD = "000201010211021644038482021656080415522024082021656061661000308202165650825HDFC00000015020011163278526460010A0000005240128Vyapar.174068471103@hdfcbank27420010A0000005240124STQD295260117541249217725204829953033565802IN5910TERRAROOTS6007KOLKATA610670001562400524STQD2952601175412492177207088202165663045267"
SRC = os.path.join(ROOT, "engine/assets/terrathon/qr_dd_payment_terraroots_source.png")
INK, CREAM, GOLD = "#0A0A0A", "#F4EFE0", "rgba(222,180,100,.85)"
PHOTO, PHOTO_POS = "07_03", "50% 55%"

def decode(bgr): return cv2.QRCodeDetector().detectAndDecode(bgr)[0]
src = cv2.copyMakeBorder(cv2.imread(SRC), 80, 80, 80, 80, cv2.BORDER_CONSTANT, value=(255, 255, 255))
assert decode(src) == PAYLOAD, "supplied QR image no longer decodes to PAYLOAD"
q = segno.make(PAYLOAD, error="m", micro=False)
buf = io.BytesIO(); q.save(buf, kind="svg", scale=1, border=0, dark=INK, light=None)
QR = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
tmp = io.BytesIO(); q.save(tmp, kind="png", scale=12, border=4)
assert decode(cv2.cvtColor(np.array(Image.open(io.BytesIO(tmp.getvalue())).convert("RGB")), cv2.COLOR_RGB2BGR)) == PAYLOAD, "regenerated QR does not decode to PAYLOAD"
MODS = q.symbol_size(border=0)[0]
QR_PX = round(430 / MODS) * MODS; PAD = round(4 * QR_PX / MODS); BORDER = 10
PLATE = QR_PX + 2 * PAD + 2 * BORDER
PX, PY = (W - PLATE) // 2, 490

def poster():
    parts, els = [_pb.photo_ground(dd, W, H, PHOTO, PHOTO_POS, dim=.72)], []
    parts.append(f'<img data-tag="lights" src="{dd.uri("string_lights.png")}" style="position:absolute;left:160px;top:-53px;width:1045px;z-index:5">')
    parts.append(f'<img data-tag="plate" src="{dd.uri("sparkles.png")}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;z-index:6;mix-blend-mode:screen;opacity:.45;pointer-events:none">')
    bx, by, bw = 40, 40, 150
    parts.append(f'<img data-tag="badge" src="{dd.uri("live_badge.png")}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;z-index:20">'); els.append(("badge", bx, by, bw, round(bw * 1005 / 1061)))
    def line(tag, txt, top, fsize, weight, h, extra=""):
        parts.append(f'<div data-tag="{tag}" style="position:absolute;left:0;width:{W}px;top:{top}px;text-align:center;font-family:var(--d);font-weight:{weight};font-size:{fsize}px;line-height:1;'
                     f'text-transform:uppercase;white-space:nowrap;{STROKE}{extra}z-index:20">{txt}</div>'); els.append((tag, 40, top, 1000, h))
    line("head1", "Stall advance", 205, 112, 700, 112)
    line("head2", "payment", 205 + 104, 112, 700, 112)
    line("sub", "Scan to pay", 430, 40, 400, 44)
    parts.append(f'<div data-tag="plate" style="position:absolute;left:{PX}px;top:{PY}px;width:{PLATE}px;height:{PLATE}px;box-sizing:border-box;background:{CREAM};border:{BORDER}px solid {GOLD};'
                 f'border-radius:34px;display:flex;align-items:center;justify-content:center;z-index:12;box-shadow:0 14px 40px rgba(0,0,0,.55)">'
                 f'<img data-tag="qr" src="{QR}" style="width:{QR_PX}px;height:{QR_PX}px;display:block;image-rendering:pixelated"></div>'); els.append(("qrplate", PX, PY, PLATE, PLATE))
    line("date", "Tue, 10 Nov 2026", PY + PLATE + 34, 46, 700, 50)
    line("venue", "60, Chowringhee Banquets, Rooftop", PY + PLATE + 96, 34, 700, 38)
    vw = 240; t = vw / 1717; vh = round(991 * t); vx = (W - vw) // 2; vy = H - 48 - vh
    parts.append(f'<img data-tag="title" src="{dd.uri("title_lockup.png")}" style="position:absolute;left:{round(vx - 265 * t)}px;top:{round(vy - 320 * t)}px;width:{round(2000 * t)}px;z-index:9">')
    els.append(("title", vx, vy, vw, vh))
    return "".join(parts), els

async def main():
    os.makedirs(OUT, exist_ok=True); png = os.path.join(OUT, "feed.png")
    inner, els = poster()
    async with B.session():
        await B.render(B.page(W, H, "#000", inner, grain=False), png, W, H, elements=els, containers=("qrplate",), bleed_tags=("plate",), crop_tags=("plate",), page_bg="#000",
                       text_pairs=[("date", "#fff", "#0a0a12", 46, True), ("venue", "#fff", "#0a0a12", 34, True), ("head1", "#fff", "#0a0a12", 112, True)], collision_ignore=[])
    img = Image.open(png).convert("RGB"); k = img.width / W       # the render is 2x: scale the plate box
    crop = img.crop((round((PX - 30) * k), round((PY - 30) * k), round((PX + PLATE + 30) * k), round((PY + PLATE + 30) * k)))
    bgr = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2BGR)
    hits = [f for f in (1.0, .75, .5, .35) if decode(bgr if f == 1 else cv2.resize(bgr, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)) == PAYLOAD]
    print(f"RENDER CHECK: the QR plate in the final PNG decodes to the exact payload at scales {hits}")
    assert len(hits) >= 3, "rendered QR is not decoded at enough scales"
    print("stall qr poster ->", png, f"(plate y {PY}..{PY + PLATE}, modules {MODS}, {QR_PX // MODS}px each)")
asyncio.run(main())
