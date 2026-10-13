"""DISCO DIWALI launch pack: 10 stories (each a different photo, type treatment and layout, ALL carrying the launch information, with a clear
zone for the link sticker), one WhatsApp poster, one WhatsApp group DP (+ a circle-crop preview).
Facts are exactly the launch post's: Masquerade Sangeet Edition, 10th November 2026, 4:30 PM onwards, ticket sales open soon, more details soon,
all for charity (the LIVE badge). Nothing else is printed.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_launch_pack.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
FACTS = dict(edition="Masquerade Sangeet Edition", date="10th November, 2026", time="4:30 PM Onwards",
             status="Ticket sales open soon", note="More details soon")
#      photo, typo, layout, mask
STORIES = [
    ("03", "foil",      "classic",     "copper"),
    ("05", "outline",   "mask_hero",   "copper"),
    ("12", "editorial", "mask_behind", "copper"),
    ("06", "stack",     "classic",     "copper"),
    ("09", "foil",      "mask_hero",   "copper"),
    ("11", "outline",   "classic",     "asset"),
    ("07", "editorial", "mask_behind", "copper"),
    ("13", "stack",     "mask_hero",   "copper"),
    ("08", "foil",      "mask_behind", "copper"),
    ("10", "outline",   "classic",     "copper"),
]
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "launch")
    async with dd.B.session():
        for i, (ph, ty, lay, mk) in enumerate(STORIES, 1):
            await dd.render_poster("story_launch", dict(FACTS, photo=ph), "story", os.path.join(out, f"story_{i:02d}.png"),
                                   style="photo", mask=mk, typo=ty, layout=lay)
        await dd.render_poster("wa_poster", dict(FACTS, photo="05"), "feed", os.path.join(out, "whatsapp_poster.png"),
                               style="photo", mask="copper", typo="foil")
        await dd.render_poster("wa_dp", dict(edition=FACTS["edition"], date=FACTS["date"]), "square", os.path.join(out, "whatsapp_dp.png"),
                               style="plate", mask="copper")
    from PIL import Image, ImageDraw
    dp = Image.open(os.path.join(out, "whatsapp_dp.png")).convert("RGB")
    m = Image.new("L", dp.size, 0); ImageDraw.Draw(m).ellipse((0, 0, dp.size[0] - 1, dp.size[1] - 1), fill=255)
    prev = Image.new("RGB", dp.size, (30, 30, 30)); prev.paste(dp, (0, 0), m); prev.save(os.path.join(out, "whatsapp_dp_circle_preview.png"))
    ims = [Image.open(os.path.join(out, f"story_{i:02d}.png")).convert("RGB").resize((324, 576)) for i in range(1, 11)]
    sh = Image.new("RGB", (324 * 5 + 40, 576 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 5) * 334, (i // 5) * 586))
    sh.save(os.path.join(out, "stories_sheet.png"))
    print("launch pack done ->", out)
asyncio.run(main())
