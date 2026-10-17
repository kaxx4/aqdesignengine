"""DISCO DIWALI bulk stories, hall photo set (2026-10-15): ten stories on the approved story_ref design, one photo each, everything else identical.
Photos are pre-cropped to 9:16 around each subject (x-centre fraction below) because story_ref centre-crops: a 3:2 landscape would otherwise keep only the
middle 28% of the frame. No date, time or location (user, 2026-10-14). CONSENT: many people in these photos look like minors; none has a record.
Outputs out/discodiwali/bulk_hall/story_NN.png and sheet.png.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories_hall.py
"""
import asyncio, importlib.util, os, sys, tempfile
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details soon")
# (path, x-centre fraction of the crop, y-centre fraction)
SET = [(os.path.join(HALL, "08_boy-on-shoulders-stage-lights-portrait.jpg"), .5, .5),
       (os.path.join(HALL, "01_dancers-silver-pillar-purple.jpg"), .45, .5),
       (os.path.join(HALL, "09_boy-on-shoulders-star-balloon.jpg"), .5, .5),
       (os.path.join(HALL, "03_girls-dancing-yellow-top.jpg"), .62, .5),
       (os.path.join(HALL, "06_blue-room-crowd-faces.jpg"), .5, .5),
       (os.path.join(HALL, "04_pink-ceiling-chandelier-phone.jpg"), .55, .5),
       (os.path.join(HALL, "02_crowd-teal-kurta-purple.jpg"), .55, .5),
       (os.path.join(HALL, "07_pink-glare-girls-backs-phone.jpg"), .5, .5),
       (os.path.join(HALL, "05_boys-crowd-green-light.jpg"), .42, .5),
       (dd.photo_path("05"), .5, .5)]
def crop916(path, fx, fy, tmp):
    im = Image.open(path).convert("RGB"); w, h = im.size
    cw, ch = (w, round(w * 16 / 9)) if w / h < 9 / 16 else (round(h * 9 / 16), h)
    x0 = min(max(round(fx * w - cw / 2), 0), w - cw); y0 = min(max(round(fy * h - ch / 2), 0), h - ch)
    out = os.path.join(tmp, os.path.basename(path)); im.crop((x0, y0, x0 + cw, y0 + ch)).save(out, quality=92); return out
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_hall")
    with tempfile.TemporaryDirectory() as tmp:
        crops = [crop916(p, fx, fy, tmp) for p, fx, fy in SET]
        async with dd.B.session():
            for i, c in enumerate(crops, 1):
                await dd.render_poster("story_ref", dict(BRIEF, photo=c), "story", os.path.join(out, f"story_{i:02d}.png"))
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(SET) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("bulk hall done ->", out)
asyncio.run(main())
