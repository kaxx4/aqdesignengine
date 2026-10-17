"""DISCO DIWALI bulk stories, set 2 (2026-10-17): ten NEW stories on the approved story_ref design, from the older event-photo library (the hall set was
set 1). Same design, only the photo changes. Note line reads 'More details to follow' (user, 2026-10-17). No date, time or location.
Photos are pre-cropped to 9:16 around each subject (story_ref centre-crops).  CONSENT: many people look like minors; no records.
Outputs out/discodiwali/bulk_library/story_NN.png and sheet.png.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories_library.py
"""
import asyncio, importlib.util, os, sys, tempfile
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details to follow")
# (library prefix, x-centre fraction, y-centre fraction)
SET = [("02", .5, .5), ("11", .5, .5), ("07", .4, .5), ("10", .5, .5), ("08", .5, .5),
       ("13", .5, .5), ("06", .5, .5), ("03", .5, .5), ("09", .45, .5), ("12", .5, .5)]
def crop916(path, fx, fy, tmp):
    im = Image.open(path).convert("RGB"); w, h = im.size
    cw, ch = (w, round(w * 16 / 9)) if w / h < 9 / 16 else (round(h * 9 / 16), h)
    x0 = min(max(round(fx * w - cw / 2), 0), w - cw); y0 = min(max(round(fy * h - ch / 2), 0), h - ch)
    out = os.path.join(tmp, os.path.basename(path)); im.crop((x0, y0, x0 + cw, y0 + ch)).save(out, quality=92); return out
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_library")
    with tempfile.TemporaryDirectory() as tmp:
        crops = [crop916(dd.photo_path(p), fx, fy, tmp) for p, fx, fy in SET]
        async with dd.B.session():
            for i, c in enumerate(crops, 1):
                await dd.render_poster("story_ref", dict(BRIEF, photo=c), "story", os.path.join(out, f"story_{i:02d}.png"))
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(SET) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("bulk library done ->", out)
asyncio.run(main())
