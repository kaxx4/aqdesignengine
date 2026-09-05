import asyncio, os
from playwright.async_api import async_playwright

DIR = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 2000

async def main():
    svg_path = os.path.join(DIR, "marginalia.svg")
    with open(svg_path) as f:
        svg = f.read()
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}} body{{width:{W}px;height:{H}px}}</style></head><body>{svg}</body></html>'
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        await pg.set_content(html, wait_until="load")
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=os.path.join(DIR, "marginalia.png"))
        await pg.pdf(path=os.path.join(DIR, "marginalia.pdf"), width=f"{W}px", height=f"{H}px", print_background=True, margin={"top":"0","bottom":"0","left":"0","right":"0"})
        await b.close()
    print("done")

asyncio.run(main())
