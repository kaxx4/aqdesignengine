"""Render ONE copper sticker from dd_copper as a trimmed transparent PNG: python scratchpad/dd_sticker_one.py <name>"""
import sys, io, asyncio, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
import dd_copper as cp
from PIL import Image
from playwright.async_api import async_playwright
name = sys.argv[1]
async def main():
    svg = getattr(cp, name)(620, 0, "z", shadow=False)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(); pg = await br.new_page(viewport={"width": 760, "height": 760}, device_scale_factor=3)
        await pg.set_content(f'<html><body style="margin:0;background:transparent"><div style="padding:40px;display:inline-block">{svg}</div></body></html>')
        await pg.wait_for_timeout(300); png = await pg.screenshot(omit_background=True, full_page=True); await br.close()
    im = Image.open(io.BytesIO(png)).convert("RGBA"); b = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox(); m = 24
    im = im.crop((max(b[0] - m, 0), max(b[1] - m, 0), b[2] + m, b[3] + m))
    im.save(os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers", f"copper_{name}.png"))
    t = im.copy(); t.thumbnail((1000, 1000)); t.save(os.path.join(ROOT, "engine", "assets", "disco_diwali", f"sticker_{name}.png"), optimize=True)
    bg = Image.new("RGBA", (900, 900), (10, 10, 10, 255)); t.thumbnail((800, 800)); bg.alpha_composite(t, (50, 50)); bg.convert("RGB").save(os.path.join(ROOT, "out", "discodiwali", "stalls", f"{name}_preview.png"))
asyncio.run(main())
