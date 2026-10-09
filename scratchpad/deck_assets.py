"""Extract the embedded rasters from the Figma export of the Disco Diwali sponsorship deck into engine/assets/sponsorship/.

Source: training_samples/sponsorship_deck/source_export.pdf (one tall page, real text layer, 57 masked images).
pdfimages writes every image and its soft-mask (smask) as SEPARATE files, which is why the logos look black on a naive extract.
This merges each image with its mask, drops duplicates (Figma repeats every image twice), caps the long side at 1800px
(photos -> jpg q86, anything with alpha -> png) and writes manifest.json.

Run:  python scratchpad/deck_assets.py [--logos-only]   (needs poppler: pdfimages + pdftoppm)
"""
import hashlib, json, os, re, subprocess, sys, tempfile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "training_samples", "sponsorship_deck", "source_export.pdf")
OUT = os.path.join(ROOT, "engine", "assets", "sponsorship")
MAXSIDE = 1800


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="deckimg_")
    lst = subprocess.run(["pdfimages", "-list", PDF], capture_output=True, text=True).stdout.splitlines()[2:]
    rows = []
    for ln in lst:
        p = ln.split()
        rows.append({"num": int(p[1]), "type": p[2], "w": int(p[3]), "h": int(p[4])})
    subprocess.run(["pdfimages", "-png", PDF, os.path.join(tmp, "i")], check=True)
    f = lambda n: os.path.join(tmp, f"i-{n:03d}.png")
    seen, manifest = {}, []
    for r in rows:
        if r["type"] != "image":
            continue
        n = r["num"]
        nxt = next((x for x in rows if x["num"] == n + 1), None)
        mask = f(n + 1) if nxt and nxt["type"] == "smask" else None
        im = Image.open(f(n)).convert("RGB")
        if mask:
            m = Image.open(mask).convert("L")
            if m.size != im.size:
                m = m.resize(im.size, Image.LANCZOS)
            im = im.convert("RGBA"); im.putalpha(m)
        key = hashlib.md5(im.resize((32, 32)).tobytes()).hexdigest() + f"{r['w']}x{r['h']}"
        if key in seen:
            continue
        seen[key] = n
        has_alpha = bool(mask) and im.getchannel("A").getextrema()[0] < 250
        if max(im.size) > MAXSIDE:
            im.thumbnail((MAXSIDE, MAXSIDE), Image.LANCZOS)
        name = f"img_{n:03d}"
        if has_alpha:
            im.save(os.path.join(OUT, name + ".png"), optimize=True); ext = "png"
        else:
            im.convert("RGB").save(os.path.join(OUT, name + ".jpg"), quality=86, optimize=True); ext = "jpg"
        manifest.append({"id": n, "file": f"{name}.{ext}", "w": im.size[0], "h": im.size[1], "alpha": has_alpha})
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    print(len(manifest), "assets ->", OUT)



# ---- vector logos: the Figma export keeps ~8 sponsor logos as vector paths, so pdfimages never sees them. Re-render each at 200dpi.
# rects are (x0, y0, x1, y1) in PDF points on the one tall page.
VECTOR_LOGOS = {
    "yrs": (255, 7700 + 172, 503, 7700 + 270), "cross": (458, 7700 + 267, 648, 7700 + 357),
    "police": (1238, 7700 + 207, 1490, 7700 + 252), "heritage": (735, 7700 + 762, 1017, 7700 + 894),
    "dillilane": (1058, 7700 + 747, 1358, 7700 + 894), "kanxshkag": (1365, 7700 + 900, 1550, 7700 + 1122),
    "cacophony": (1242, 7700 + 525, 1449, 7700 + 728),
}


def vector_logos(dpi=200):
    k = dpi / 72.0
    for name, (x0, y0, x1, y1) in VECTOR_LOGOS.items():
        pad = 6
        out = os.path.join(OUT, f"logo_{name}")
        subprocess.run(["pdftoppm", "-r", str(dpi), "-x", str(int((x0 - pad) * k)), "-y", str(int((y0 - pad) * k)),
                        "-W", str(int((x1 - x0 + 2 * pad) * k)), "-H", str(int((y1 - y0 + 2 * pad) * k)),
                        "-png", "-singlefile", PDF, out], check=True)
    print(len(VECTOR_LOGOS), "vector logos")


if __name__ == "__main__":
    if "--logos-only" not in sys.argv:
        main()
    vector_logos()
