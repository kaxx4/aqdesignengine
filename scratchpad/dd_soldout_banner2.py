"""DISCO DIWALI "SOLD OUT" v2 (user, 2026-11-06, sent the full-details poster: title, edition, 10th November 2026, 4:30 PM onwards, 60, Chowringhee Banquets).
Base = poster_ref with that logistics block (date, time, venue; supplied facts only, no price, no lineup, no status line), the Starry Night style SOLD OUT banner
across the title, set so the edition, date, time and venue lines stay clear. Feed (1080x1350, also WhatsApp) only, the size the user sent.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_soldout_banner2.py -> out/discodiwali/soldout_banner2/feed.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
import importlib
OUT = os.path.join(ROOT, "out", "discodiwali", "soldout_banner2")
BRIEF = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM onwards", venue="60, Chowringhee Banquets", link=False)
CY, DEG = float(os.environ.get("CY", .48)), float(os.environ.get("DEG", 8))

def banner_over(png, width_frac, cy_frac, deg):
    from PIL import Image, ImageFilter
    base = Image.open(png).convert("RGBA"); W, H = base.size
    b = Image.open(os.path.join(ROOT, "engine", "assets", "disco_diwali", "sold_out_banner.png")).convert("RGBA")
    bw = round(W * width_frac); b = b.resize((bw, round(bw * b.size[1] / b.size[0])), Image.LANCZOS)
    r = b.rotate(deg, expand=True, resample=Image.BICUBIC)
    x, y = round(W / 2 - r.size[0] / 2), round(H * cy_frac - r.size[1] / 2)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); a = r.split()[3].point(lambda v: int(v * .65))
    sh.paste((0, 0, 0, 255), (x, y + round(W * .012)), a); sh = sh.filter(ImageFilter.GaussianBlur(W * .012))
    base.alpha_composite(sh); base.alpha_composite(r, (x, y)); base.convert("RGB").save(png)

async def main():
    async with dd.B.session():
        await dd.render_poster("poster_ref", BRIEF, "feed", os.path.join(OUT, "feed.png"))
    banner_over(os.path.join(OUT, "feed.png"), 1.04, CY, DEG)
    print("done ->", OUT)
asyncio.run(main())
