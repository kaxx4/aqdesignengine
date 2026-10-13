"""DISCO DIWALI bulk WhatsApp posters (poster_ref + photo, pill reading LINK BELOW): ten posters, one photo each, same photos and order as the
bulk stories (scratchpad/dd_bulk_stories.py). Everything else is identical. Outputs out/discodiwali/bulk_wa/poster_NN.png and a contact sheet.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_bulk_wa_posters.py"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon", note="More details soon", link="Link below")
PHOTOS = ["05", "03", "12", "06", "09", "11", "07", "13", "08", "10"]
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "bulk_wa")
    async with dd.B.session():
        for i, ph in enumerate(PHOTOS, 1):
            await dd.render_poster("poster_ref", dict(BRIEF, photo=ph), "feed", os.path.join(out, f"poster_{i:02d}.png"))
    from PIL import Image
    ims = [Image.open(os.path.join(out, f"poster_{i:02d}.png")).convert("RGB").resize((360, 450)) for i in range(1, len(PHOTOS) + 1)]
    sh = Image.new("RGB", (360 * 5 + 40, 450 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 5) * 370, (i // 5) * 460))
    sh.save(os.path.join(out, "sheet.png")); print("bulk wa done ->", out)
asyncio.run(main())
