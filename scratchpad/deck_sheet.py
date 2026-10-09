"""Contact sheets of a rendered deck: python scratchpad/deck_sheet.py <dir> [cols=3] [per=12]  ->  <dir>/sheet_N.png"""
import glob, os, sys
from PIL import Image, ImageDraw
d = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 3; per = int(sys.argv[3]) if len(sys.argv) > 3 else 12
fs = sorted(glob.glob(os.path.join(d, "slide_*.png")))
tw = 1920 // cols; th = tw * 9 // 16
for k in range(0, len(fs), per):
    grp = fs[k:k + per]; rows = (len(grp) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * th), "#777")
    dr = ImageDraw.Draw(sh)
    for j, f in enumerate(grp):
        im = Image.open(f).convert("RGB").resize((tw - 6, th - 6), Image.LANCZOS)
        x, y = (j % cols) * tw, (j // cols) * th
        sh.paste(im, (x + 3, y + 3)); dr.rectangle([x + 3, y + 3, x + 40, y + 24], fill="black"); dr.text((x + 8, y + 8), str(k + j + 1), fill="yellow")
    sh.save(os.path.join(d, f"sheet_{k // per + 1}.png"))
print(len(fs), "slides")
