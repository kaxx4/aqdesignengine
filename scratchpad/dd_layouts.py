"""DISCO DIWALI layout variations: the photo direction under four composition presets x type treatments x photos.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_layouts.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BASE = dd.DEMO[0][1]
V = [  # name, layout, typo, photo, mask
    ("L01_maskhero_foil",     "mask_hero",   "foil",      "03", "copper"),
    ("L02_maskhero_minimal",  "mask_hero",   "minimal",   "05", "copper"),
    ("L03_titlehero_outline", "title_hero",  "outline",   "06", "copper"),
    ("L04_titlehero_whisper", "title_hero",  "whisper",   "13", "copper"),
    ("L05_behind_editorial",  "mask_behind", "editorial", "05", "copper"),
    ("L06_behind_minimal",    "mask_behind", "minimal",   "03", "copper"),
    ("L07_maskhero_stack",    "mask_hero",   "stack",     "11", "asset"),
    ("L08_titlehero_foil",    "title_hero",  "foil",      "09", "copper"),
]
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "layouts")
    async with dd.B.session():
        for name, lay, ty, ph, mk in V:
            await dd.render_poster("announce", dict(BASE, photo=ph), "feed", os.path.join(out, name + ".png"),
                                   style="photo", mask=mk, typo=ty, layout=lay)
    from PIL import Image
    ims = [Image.open(os.path.join(out, n + ".png")).convert("RGB").resize((480, 600)) for n, *_ in V]
    sh = Image.new("RGB", (480 * 4 + 30, 600 * 2 + 10), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 4) * 490, (i // 4) * 610))
    sh.save(os.path.join(out, "sheet.png"))
    print("layouts done ->", out)
asyncio.run(main())
