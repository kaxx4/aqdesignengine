"""Build engine/assets/disco_diwali/mask_stroked.png: the supplied mask with a red speckled die-cut stroke.

The stroke is the mask's own alpha, grown by blur-and-threshold (a rounded dilation), with the threshold jittered by
smoothed noise so the edge is rough like a hand-cut sticker, then filled with red stipple. The eye holes gain a red rim
too, because growing the opaque region shrinks the holes. The canvas is padded by PAD so the stroke is never clipped.
Run:  python scratchpad/make_mask_stroke.py
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "engine", "assets", "disco_diwali") + os.sep
PAD, GROW, SEED = 90, 62, 7
rng = np.random.default_rng(SEED)

mask = Image.open(A + "mask.png").convert("RGBA")
W, H = mask.size
canvas = Image.new("RGBA", (W + 2 * PAD, H + 2 * PAD), (0, 0, 0, 0))
canvas.paste(mask, (PAD, PAD))
alpha = np.asarray(canvas)[..., 3].astype(np.float32) / 255.0

blur = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(GROW / 2.2))).astype(np.float32) / 255.0
noise = rng.normal(0, 1, alpha.shape).astype(np.float32)
noise = np.asarray(Image.fromarray(((noise - noise.min()) / np.ptp(noise) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.3))).astype(np.float32) / 255.0
thr = 0.07 + (noise - 0.5) * 0.26                       # jittered threshold = rough edge
grown = (blur > thr) | (alpha > 0.5)

# red stipple fill: base red, with lighter pink-red and darker oxblood grains, plus a few gold flecks
h, w = grown.shape
base = np.zeros((h, w, 3), np.float32); base[:] = (176, 20, 28)
r = rng.random((h, w))
base[r < .18] = (214, 58, 78)
base[(r >= .18) & (r < .32)] = (128, 10, 16)
base[(r >= .32) & (r < .335)] = (230, 150, 40)
fill = Image.fromarray(base.astype(np.uint8), "RGB").filter(ImageFilter.GaussianBlur(0.6))

out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
stroke_a = Image.fromarray((grown * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
out.paste(fill, (0, 0), stroke_a)
out.alpha_composite(canvas)                             # the mask itself on top of its own stroke
out.save(A + "mask_stroked.png")
print("mask_stroked.png", out.size, "pad", PAD)
