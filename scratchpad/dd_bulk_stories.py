"""DISCO DIWALI bulk stories on the remake layout (kind story_ref): ten stories, one photo each, everything else identical (mask, lights, badge,
title, edition lines, status, note and the LINK IN BIO pill all sit at the positions measured from the user's reference story).
Outputs out/discodiwali/bulk/story_NN.png and a contact sheet.   Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_stories.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details soon")
PHOTOS = ["05", "03", "12", "06", "09", "11", "07", "13", "08", "10"]       # library prefixes, one story each
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk")
    async with dd.B.session():
        for i, ph in enumerate(PHOTOS, 1):
            await dd.render_poster("story_ref", dict(BRIEF, photo=ph), "story", os.path.join(out, f"story_{i:02d}.png"))
    from PIL import Image
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, len(PHOTOS) + 1)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "sheet.png")); print("bulk done ->", out)
asyncio.run(main())
