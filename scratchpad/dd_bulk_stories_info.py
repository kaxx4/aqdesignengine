"""DISCO DIWALI bulk stories, set 4 (2026-10-21): ten stories on the approved story_ref design from TEN NEW user-supplied photos
(engine/assets/img/events/disco-diwali-2026-10-21/, one story per photo). Unlike sets 1-3 these carry the event info (user, 2026-10-21):
early-bird line (price supplied by the user), date, time, venue; "More details to follow" and "Ticket sales open soon" are removed.
"Today at 6PM" makes the set valid only on the posting day. Photos are cropped to 9:16 here (story_ref centre-crops).
CONSENT: several photos show apparent minors, no consent record. Two photos carry a third-party logo (Pizza Hut sign): crops avoid it.
Outputs out/discodiwali/bulk_info/story_NN.png and sheet.png.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories_info.py
"""
import asyncio, glob, importlib.util, os, sys, tempfile
from PIL import Image, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
SOLD = os.environ.get("VARIANT") == "soldout"      # VARIANT=soldout: the "Early bird sold out" set (2026-10-22), no price line, same photos and crops
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Early bird sold out" if SOLD else "Early bird tickets open",
             date="Tue, 10 Nov 2026", time="4:30 PM onwards", venue="60, Chowringhee Banquets, Rooftop")
if not SOLD: BRIEF["note"] = "Today at 6PM @Rs450"
STAMP = os.environ.get("VARIANT") == "stamp"     # VARIANT=stamp: the sold-out set with the EARLY BIRD SOLD OUT band on top (2026-10-22)
if STAMP: BRIEF.update(status="Early bird sold out", stamp=True); BRIEF.pop("note", None)
LIB = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-2026-10-21")
# (NN prefix, x-centre fraction, top fraction, height fraction, brightness lift). hf < 1 zooms into the lower part of the frame:
# the approved design lays the DISCO lockup over y 480..1018, so a face there is cut through by the lettering. 02, 03, 06, 07 and 10
# are therefore cropped BELOW their faces (armbands, kurtas, hands); the rest have no face in that band.
SET = [("01", .2, 0, 1, 2.3), ("02", .5, .52, .46, .8), ("03", .5, .52, .46, 1.0), ("04", .45, 0, 1, 1.25), ("05", .8, 0, 1, 1.6),
       ("06", .47, .5, .5, .5), ("07", .5, .42, .58, .55), ("08", .2, 0, 1, 1.0), ("09", .5, 0, 1, 1.0), ("10", .5, .55, .45, 1.0)]
def crop916(nn, fx, y0f, hf, lift, tmp):
    path = glob.glob(os.path.join(LIB, f"{nn}_*.jpg"))[0]
    im = Image.open(path).convert("RGB"); w, h = im.size
    ch = round(h * hf); cw = round(ch * 9 / 16)
    if cw > w: cw = w; ch = round(w * 16 / 9)
    x0 = min(max(round(fx * w - cw / 2), 0), w - cw); y0 = min(max(round(y0f * h), 0), h - ch)
    im = im.crop((x0, y0, x0 + cw, y0 + ch))
    if lift != 1.0: im = ImageEnhance.Brightness(im).enhance(lift)
    out = os.path.join(tmp, f"{nn}.jpg"); im.save(out, quality=92); return out
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_stamp" if STAMP else "bulk_soldout" if SOLD else "bulk_info")
    with tempfile.TemporaryDirectory() as tmp:
        crops = [crop916(*s, tmp) for s in SET]
        async with dd.B.session():
            for i, c in enumerate(crops, 1):
                await dd.render_poster("story_ref", dict(BRIEF, photo=c), "story", os.path.join(out, f"story_{i:02d}.png"))
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(SET) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims): sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("bulk info done ->", out)
asyncio.run(main())
