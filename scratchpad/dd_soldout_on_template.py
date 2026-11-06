"""DISCO DIWALI "SOLD OUT" story = the user's own story template (engine/assets/img/events/disco-diwali-soldout/story_template.png, sent 2026-11-06) UNCHANGED, with only the
red SOLD OUT banner (sold_out_banner.png) laid on top, tilted, running off both edges, with a soft shadow. User directive: "use this story template just add the sold out sticker on top".
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_soldout_on_template.py -> out/discodiwali/soldout_on_template/story.png"""
import os
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out", "discodiwali", "soldout_on_template"); os.makedirs(OUT, exist_ok=True)
CY, DEG, WF = float(os.environ.get("CY", .48)), float(os.environ.get("DEG", 14)), float(os.environ.get("WF", 1.3))
base = Image.open(os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-soldout", "story_template.png")).convert("RGBA"); w, h = base.size
b = Image.open(os.path.join(ROOT, "engine", "assets", "disco_diwali", "sold_out_banner.png")).convert("RGBA")
bw = round(w * WF); b = b.resize((bw, round(bw * b.size[1] / b.size[0])), Image.LANCZOS)
r = b.rotate(DEG, expand=True, resample=Image.BICUBIC)
x, y = round(w / 2 - r.size[0] / 2), round(h * CY - r.size[1] / 2)
sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); a = r.split()[3].point(lambda v: int(v * .65))
sh.paste((0, 0, 0, 255), (x, y + round(w * .012)), a); sh = sh.filter(ImageFilter.GaussianBlur(w * .012))
base.alpha_composite(sh); base.alpha_composite(r, (x, y))
base.convert("RGB").save(os.path.join(OUT, "story.png")); print("done ->", OUT, base.size)
