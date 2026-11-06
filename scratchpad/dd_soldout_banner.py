"""DISCO DIWALI "SOLD OUT" poster, Starry Night treatment (user ref, 2026-11-06: a normal event poster with ONE big diagonal red SOLD OUT banner across it, running off both
edges and covering part of the title). Base = the approved poster_ref (feed / WhatsApp) and story_ref (story) with only supplied facts: edition, 10th November, 4:30 PM onwards,
all for charity. The status line is NOT 'ticket sales open soon' (it would contradict the banner). The banner is the existing sold_out_banner.png (red grain, speckled type),
tilted ~8 degrees, scaled just past the canvas width and set high so the lower title, edition and date lines stay readable, with a soft drop shadow, composited after the base render so it sits over everything like the reference.
Which phase sold out is not supplied, so none is named.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_soldout_banner.py -> out/discodiwali/soldout_banner/{feed,story}.png"""
import asyncio, importlib.util, os, sys
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
OUT = os.path.join(ROOT, "out", "discodiwali", "soldout_banner")
BANNER = os.path.join(ROOT, "engine", "assets", "disco_diwali", "sold_out_banner.png")
BASE = dict(edition="Masquerade Sangeet Edition", status="10th November, 4:30 PM onwards", note="All for charity")


def banner_over(png, width_frac, cy_frac, deg=20):
    """Composite the tilted banner onto the rendered base at 1x of the render (render scale is 2)."""
    base = Image.open(png).convert("RGBA"); W, H = base.size
    b = Image.open(BANNER).convert("RGBA")
    bw = round(W * width_frac); b = b.resize((bw, round(bw * b.size[1] / b.size[0])), Image.LANCZOS)
    r = b.rotate(deg, expand=True, resample=Image.BICUBIC)
    x, y = round(W / 2 - r.size[0] / 2), round(H * cy_frac - r.size[1] / 2)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); a = r.split()[3].point(lambda v: int(v * .65))
    sh.paste((0, 0, 0, 255), (x, y + round(W * .012)), a); sh = sh.filter(ImageFilter.GaussianBlur(W * .012))
    base.alpha_composite(sh); base.alpha_composite(r, (x, y))
    base.convert("RGB").save(png)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with dd.B.session():
        await dd.render_poster("poster_ref", dict(BASE, link=False), "feed", os.path.join(OUT, "feed.png"))
        await dd.render_poster("story_ref", dict(BASE, photo=os.path.join(HALL, "05_boys-crowd-green-light.jpg"), dim=.2, link=False), "story", os.path.join(OUT, "story.png"))
    banner_over(os.path.join(OUT, "feed.png"), 1.04, .565, 8)
    banner_over(os.path.join(OUT, "story.png"), 1.04, .445, 6)
    print("done ->", OUT)
asyncio.run(main())
