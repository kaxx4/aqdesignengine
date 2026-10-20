"""Export every Disco Diwali red-copper sticker as a TRANSPARENT PNG (user, 2026-10-20: "give me all the stickers made in png format").

Stickers come from scratchpad/dd_copper.py (heart, star, diya, calendar, pin; surface = the mask's own copper texture). Each is rendered by Chromium on a transparent page at 3x
(no drop shadow, so the PNG drops onto any background; add your own), then trimmed to its content with a small even margin. Output: sample_outputs/disco_diwali_stickers/<name>.png and a
preview sheet on a dark ground. Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_sticker_export.py
"""
import asyncio, io, os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scratchpad"))
import dd_copper as cp
from playwright.async_api import async_playwright

OUT = os.path.join(ROOT, "sample_outputs", "disco_diwali_stickers")
STICKERS = {"heart": cp.heart(520, 0, "h", shadow=False), "star": cp.star(520, 0, "s", shadow=False), "diya": cp.diya(620, 0, "d", shadow=False),
            "calendar": cp.calendar(520, 0, "c", shadow=False), "pin": cp.pin(520, 0, "p", shadow=False)}


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        br = await pw.chromium.launch()
        pg = await br.new_page(viewport={"width": 760, "height": 760}, device_scale_factor=3)
        done = {}
        for name, svg in STICKERS.items():
            await pg.set_content(f'<html><body style="margin:0;background:transparent"><div style="padding:40px;display:inline-block">{svg}</div></body></html>')
            await pg.wait_for_timeout(250)
            png = await pg.screenshot(omit_background=True, full_page=True)
            im = Image.open(io.BytesIO(png)).convert("RGBA")
            box = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
            m = 24
            im = im.crop((max(box[0] - m, 0), max(box[1] - m, 0), min(box[2] + m, im.width), min(box[3] + m, im.height)))
            im.save(os.path.join(OUT, f"copper_{name}.png")); done[name] = im
            print(f"copper_{name}.png {im.size}")
        await br.close()
    sh = Image.new("RGBA", (2000, 520), (21, 17, 31, 255)); x = 20
    for im in done.values():
        t = im.copy(); t.thumbnail((380, 480)); sh.alpha_composite(t, (x, 20)); x += 395
    sh.convert("RGB").save("/tmp/claude-0/-home-user-aqdesignengine/a03b84c4-4ab5-5b44-a5ab-67594f254189/scratchpad/stickers_sheet.png")


asyncio.run(main())
