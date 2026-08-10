"""Tile a folder of source photos into ONE numbered contact sheet.

This exists so photo selection is made by LOOKING at all candidates at once, not by guessing from
filenames. Read the produced .jpg with the Read tool, then pick by index.

    python contact_sheet.py <src_dir> [out_path] [cols]
"""
import os, sys, math
from PIL import Image, ImageDraw

TH = 300


def sheet(src, out_path=None, cols=6, thumb=TH):
    files = sorted(f for f in os.listdir(src)
                   if f.lower().endswith(('.jpg', '.jpeg', '.png')))
    if not files:
        raise SystemExit(f"no images in {src}")
    rows = math.ceil(len(files) / cols)
    out = Image.new("RGB", (cols * thumb, rows * (thumb + 26)), (28, 28, 28))
    d = ImageDraw.Draw(out)
    for i, f in enumerate(files):
        try:
            im = Image.open(os.path.join(src, f)).convert("RGB")
        except Exception:
            continue
        im.thumbnail((thumb, thumb))
        cx, cy = (i % cols) * thumb, (i // cols) * (thumb + 26)
        out.paste(im, (cx + (thumb - im.width) // 2, cy + (thumb - im.height) // 2))
        # index + pixel dims: portrait frames crop far better to 4:5 than landscape ones,
        # so the dimensions are part of the selection decision, not decoration
        d.text((cx + 6, cy + thumb + 5), f"{i:02d}  {im.width}x{im.height}", fill=(255, 220, 90))
    out_path = out_path or os.path.join(os.path.dirname(src.rstrip("/\\")), "_contact.jpg")
    out.save(out_path, quality=82)
    print(out_path, len(files), "images")
    return out_path


if __name__ == "__main__":
    sheet(sys.argv[1],
          sys.argv[2] if len(sys.argv) > 2 else None,
          int(sys.argv[3]) if len(sys.argv) > 3 else 6)
