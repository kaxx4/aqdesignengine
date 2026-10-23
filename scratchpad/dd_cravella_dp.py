import asyncio, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, "engine"))
import discodiwali as dd
from PIL import Image, ImageDraw
out = os.path.join(ROOT, "out", "discodiwali", "stalls")
async def main():
    async with dd.B.session():
        await dd.render_poster("wa_dp", dict(edition="Masquerade Sangeet Edition", group="Crave'lla", role="Dessert stall", sticker="cupcake"), "square",
                               os.path.join(out, "cravella_dp.png"), style="plate", mask="copper")
    dp = Image.open(os.path.join(out, "cravella_dp.png")).convert("RGB")
    m = Image.new("L", dp.size, 0); ImageDraw.Draw(m).ellipse((0, 0, dp.size[0]-1, dp.size[1]-1), fill=255)
    pv = Image.new("RGB", dp.size, (30, 30, 30)); pv.paste(dp, (0, 0), m); pv.save(os.path.join(out, "cravella_dp_circle_preview.png"))
asyncio.run(main())
