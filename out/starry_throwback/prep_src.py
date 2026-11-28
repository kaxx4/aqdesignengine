"""Crop each chosen raw frame to the 4:5 feed aspect with an EXPLICIT window (so the
engine's vision.plan_spots, which only knows a centre crop, sees exactly what is rendered).
spec: name -> (raw file, cx, cy)  (cx/cy = crop-window centre as fraction of the raw frame)
"""
import os
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_W, OUT_H = 1620, 2025
SPEC = {
 "2024/01.jpg": ("2024_DSC_9928.jpg", .5, None, .0),    # cover DJ: (cx, cy=None, top)
 "2024/02.jpg": ("2024_IMG_6812.jpg", .40, .5, None),
 "2024/03.jpg": ("2024_IMG_6816.jpg", .5, None, .03),
 "2024/04.jpg": ("2024_IMG_0373.jpg", .5, None, .20),
 "2024/05.jpg": ("2024_DSC_9791.jpg", .5, None, .12),
 "2025/01.jpg": ("2025_IMG_20251226_171956.jpg", .5, None, .03),
 "2025/02.jpg": ("2025_IMG_9917.jpg", .465, .5, None),
 "2025/03.jpg": ("2025_IMG_9944.jpg", .50, .5, None),
 "2025/04.jpg": ("2025_IMG_2841.jpg", .5, None, .12),
}
def crop(name):
    raw, cx, cy, top = SPEC[name]
    im = ImageOps.exif_transpose(Image.open(f"{HERE}/raw/{raw}")).convert("RGB")
    w, h = im.size
    if w / h > 0.8:               # landscape-ish: full height, 4:5 width
        cw, ch = int(h * 0.8), h
        x0 = int(cx * w - cw / 2); x0 = max(0, min(w - cw, x0)); y0 = 0
    else:                         # portrait: full width, 4:5 height
        cw, ch = w, int(w * 1.25)
        x0 = 0; y0 = int(top * h); y0 = max(0, min(h - ch, y0))
    c = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((OUT_W, OUT_H), Image.LANCZOS)
    os.makedirs(os.path.dirname(f"{HERE}/src/{name}"), exist_ok=True)
    c.save(f"{HERE}/src/{name}", quality=92)
    print(name, raw, im.size, "->", (x0, y0, cw, ch))
if __name__ == "__main__":
    for n in SPEC: crop(n)
