import asyncio, os
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "file://" + os.path.join(ROOT, "web/terrathon/schedule.html")
async def main():
    os.makedirs("scratchpad/tt", exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, w, h in (("desktop", 1280, 900), ("phone", 390, 844)):
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            pg = await ctx.new_page(); errs = []
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None); pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(URL); await pg.wait_for_timeout(700)
            over = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
            fonts = await pg.evaluate("document.fonts.check('900 20px NeutralFace')")
            print(name, "h-overflow px:", over, "| NeutralFace loaded:", fonts, "| errors:", errs)
            await pg.screenshot(path=f"scratchpad/tt/sched_{name}.png", full_page=True)
            await ctx.close()
        # 'today' test: freeze the clock to Sat 3 Oct 2026 10:00 IST
        ctx = await b.new_context(viewport={"width": 1280, "height": 900}); pg = await ctx.new_page()
        await pg.clock.install(time="2026-10-03T04:30:00Z"); await pg.goto(URL); await pg.wait_for_timeout(900)
        print("today-marked ids:", await pg.evaluate("[...document.querySelectorAll('.day.is-today')].map(e=>e.id)"))
        # calendar button downloads a valid ics
        async with pg.expect_download() as d: await pg.click("button.cal[data-title='TerraThon FIFA']")
        dl = await d.value; path = await dl.path(); print("ics:", open(path).read().replace("\r\n", " | ")[:330])
        await b.close()
asyncio.run(main())
