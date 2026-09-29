"""Compare text row bands / x-extents between a reference and a render (both mapped to 1600x2000)."""
import sys
from PIL import Image
import numpy as np
def load(p):
    im = Image.open(p).convert("RGB").resize((1600, 2000)); a = np.array(im).astype(int); return a.sum(2) / 3
def bands(lum, y0, y1, x0, x1, thr, minh=12, cols=4):
    reg = (lum[y0:y1, x0:x1] > thr).sum(1) > cols; out = []; st = None
    for i, v in enumerate(reg):
        if v and st is None: st = i
        if not v and st is not None:
            if i - st >= minh: out.append((y0 + st, y0 + i))
            st = None
    return out
def xr(lum, y0, y1, x0, x1, thr, cols=4):
    m = (lum[y0:y1, x0:x1] > thr).sum(0) > cols; w = np.where(m)[0]
    return (x0 + w.min(), x0 + w.max()) if len(w) else None
if __name__ == "__main__":
    ref, ren = load(sys.argv[1]), load(sys.argv[2])
    for nm, L in (("REF", ref), ("RENDER", ren)):
        print(nm, "header bands", bands(L, 40, 300, 260, 1390, 150), " lower", bands(L, 1595, 1880, 90, 1560, 150))
        hb = bands(L, 40, 300, 260, 1390, 150)
        print("   header x", [xr(L, a, b, 236, 1400, 150) for a, b in hb])
        lb = bands(L, 1595, 1880, 90, 1560, 150)
        print("   lower x", [xr(L, a, b, 90, 1560, 150) for a, b in lb])
        dark = L < 60
        for name, (y0, y1) in {"title": (1150, 1262), "big": (1264, 1432), "sub": (1436, 1530)}.items():
            m = dark[y0:y1, 140:1440]; c = m.sum(0) > 3; r = m.sum(1) > 3; xs = np.where(c)[0]; ys = np.where(r)[0]
            print("   slab", name, "x", 140 + xs.min(), 140 + xs.max(), "y", y0 + ys.min(), y0 + ys.max()) if len(xs) else None
