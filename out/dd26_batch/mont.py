import sys, glob, os
from PIL import Image
slug, ver, dest = sys.argv[1], sys.argv[2], sys.argv[3]
fs = sorted(glob.glob(f"out/dd26_batch/slides/{slug}/{ver}/*.png"), key=lambda p: int(os.path.basename(p).split("_")[0]))
TW = 360; TH = 450; cols = 4
rows = (len(fs) + cols - 1) // cols
out = Image.new("RGB", (cols * TW, rows * TH), (20, 20, 20))
for i, f in enumerate(fs):
    im = Image.open(f).convert("RGB").resize((TW, TH))
    out.paste(im, ((i % cols) * TW, (i // cols) * TH))
out.save(dest, quality=85); print(dest, len(fs))
