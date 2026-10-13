"""DISCO DIWALI unique variations: twelve announce posters that differ on several axes at once (photo, direction, type treatment, mask
colourway, mask tilt and scale). Facts are identical everywhere (nothing invented); only the design varies.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/dd_variations.py
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
BASE = dd.DEMO[0][1]
# name, style, mask, typo, photo, tilt, scale
V = [
    ("01_foil_redcurtain",     "photo",  "copper", "foil",      "03", -4, 1.00),
    ("02_outline_cardhall",    "photo",  "copper", "outline",   "05",  5, 0.92),
    ("03_minimal_friends",     "photo",  "copper", "minimal",   "06", -8, 1.08),
    ("04_whisper_photobooth",  "photo",  "asset",  "whisper",   "10",  3, 1.00),
    ("05_stack_pinklight",     "photo",  "copper", "stack",     "13", -6, 0.95),
    ("06_editorial_greendance","photo",  "asset",  "editorial", "11",  6, 1.05),
    ("07_diya_classic",        "diya",   "copper", "editorial", None, -3, 1.00),
    ("08_blue_beams",          "blue",   "copper", "editorial", None,  4, 0.96),
    ("09_stroke_redmask",      "stroke", "red",    "editorial", None,  0, 1.00),
    ("10_foil_banner",         "photo",  "asset",  "foil",      "01",  5, 0.9),
    ("11_outline_courtyard",   "photo",  "copper", "outline",   "09", -5, 1.04),
    ("12_minimal_blur",        "photo",  "asset",  "minimal",   "07", -3, 1.0),
]
async def main():
    out = os.path.join(ROOT, "out", "discodiwali", "variations")
    async with dd.B.session():
        for name, st, mk, ty, ph, tilt, sc in V:
            content = dict(BASE, photo=ph) if ph else dict(BASE)
            await dd.render_poster("announce", content, "feed", os.path.join(out, name + ".png"), style=st, mask=mk, typo=ty,
                                   mask_tilt=tilt, mask_scale=sc)
    from PIL import Image
    ims = [Image.open(os.path.join(out, n + ".png")).convert("RGB").resize((480, 600)) for n, *_ in V]
    sh = Image.new("RGB", (480 * 4 + 30, 600 * 3 + 20), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, ((i % 4) * 490, (i // 4) * 610))
    sh.save(os.path.join(out, "sheet.png"))
    print("variations done ->", out)
asyncio.run(main())
