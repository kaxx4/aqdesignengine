"""Visual proof for engine/vision.py — draws the auto-chosen placement spots onto each photo
so the looking gate can verify, by eye, that nothing lands on a face or subject.
This is the self-test for the vision module (CLAUDE.md §8 step 3): a rule you can't SEE working
isn't done."""
import os, sys, importlib.util
os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
from PIL import Image, ImageDraw


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join("engine", n + ".py"))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


v = load("vision")
W, H = 1080, 1350
SRC = "scratchpad/carousel_sunderbans8/src_images"
OUT = "scratchpad/vision_debug"
os.makedirs(OUT, exist_ok=True)

# the real carousel chrome, so vision routes around it exactly as the renderer will
EXCLUDE = [(64, 48, 340, 80), (680, 96, 360, 44), (0, 1130, 1080, 220)]

for f in ["main.png", "img1.png", "img2.png", "img3.png", "img4.png"]:
    p = os.path.join(SRC, f)
    im = v._cover(Image.open(p).convert("RGB"), W, H)
    d = ImageDraw.Draw(im, "RGBA")

    a = v.analyze(p, W, H)
    bg = v.background_grid(a, exclude=EXCLUDE)
    cell = a["cell"]
    # green wash = cells vision considers true background
    for r in range(bg.shape[0]):
        for c in range(bg.shape[1]):
            if bg[r, c]:
                d.rectangle([c * cell, r * cell, (c + 1) * cell, (r + 1) * cell],
                            fill=(0, 255, 120, 60))
    # excluded chrome in blue
    for (x, y, w, h) in EXCLUDE:
        d.rectangle([x, y, x + w, y + h], outline=(0, 160, 255, 255), width=4)
    # chosen spots in magenta
    spots = v.plan_spots(p, W, H, n=5, exclude=EXCLUDE)
    for i, s in enumerate(spots):
        d.rectangle([s["x"], s["y"], s["x"] + s["size"], s["y"] + s["size"]],
                    outline=(255, 0, 140, 255), width=6)
        d.text((s["x"] + 6, s["y"] + 6), str(i + 1), fill=(255, 255, 255, 255))
    im.save(os.path.join(OUT, f.replace(".png", "_debug.png")))
    print(f, "bg_frac=%.2f" % float(bg.mean()), "spots=", len(spots),
          [(s["x"], s["y"], s["size"]) for s in spots])
print("wrote ->", OUT)
