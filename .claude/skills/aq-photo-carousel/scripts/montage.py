"""Tile RENDERED carousel slides — one row per carousel — for the looking gate.

Reviewing a 40-slide batch one PNG at a time is slow and, worse, makes cross-slide problems
(a duplicated cover, a palette that drifts warm, one register of doodles that reads as dirt)
effectively invisible. A montage makes those the first thing you see. Full-size Read the
individual slide afterwards for anything the montage flags.

    python montage.py <out.jpg> <slug>:<version> [<slug>:<version> ...]

Paths assume the AQ layout out/versions/<slug>_carousel/<version>/N_*.png; override with
AQ_OUT_VERSIONS if your tree differs.
"""
import os, sys, glob
from PIL import Image, ImageDraw

OUT = os.environ.get(
    "AQ_OUT_VERSIONS",
    r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE\out\versions")
TH = 380


def montage(pairs, dest, label_h=26):
    rows = []
    for slug, ver in pairs:
        fs = sorted(glob.glob(os.path.join(OUT, f"{slug}_carousel", ver, "*.png")),
                    key=lambda p: int(os.path.basename(p).split("_")[0]))
        rows.append((slug, fs))
    if not any(f for _, f in rows):
        raise SystemExit("no slides found — check slug/version and AQ_OUT_VERSIONS")
    cols = max(len(f) for _, f in rows)
    cw, ch = TH, int(TH * 1350 / 1080)
    out = Image.new("RGB", (cols * cw, len(rows) * (ch + label_h)), (24, 24, 24))
    d = ImageDraw.Draw(out)
    for r, (slug, fs) in enumerate(rows):
        for i, f in enumerate(fs):
            im = Image.open(f).convert("RGB").resize((cw, ch), Image.LANCZOS)
            out.paste(im, (i * cw, r * (ch + label_h)))
        d.text((6, r * (ch + label_h) + ch + 6), slug, fill=(255, 215, 80))
    out.save(dest, quality=84)
    print(dest)
    return dest


if __name__ == "__main__":
    montage([tuple(a.split(":")) for a in sys.argv[2:]], sys.argv[1])
