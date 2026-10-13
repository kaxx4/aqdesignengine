"""Cut the photos and logos for the REVER marketing deck out of the two exported PDFs (user, 2026-10-13: "extract photos and logos from these two PDFs").

WHAT THE PDFs ARE. Both are FLAT: every page is one 1920x1080 JPEG (`pdfimages -list` shows one image per page and nothing else), so there are no embedded
photos or logos to pull out. "Extracting" therefore means (1) saving each page's original JPEG losslessly with `pdfimages -j`, then (2) cropping the clean photo
regions and the Rever logo out of those pages. Crop boxes are written in the 2000x1125 coordinates I read the slides at and scaled by 0.96 to the real 1920x1080.
Every box is inset a few px so no rounded-frame edge, border or neighbouring text leaks in. Regions that carry an overlaid title or caption are NOT cropped.

PRIVATE. The output (engine/assets/rever_marketing/) holds identifiable students, a partner's logo and is git-ignored; this repo is public.

Run:  python scratchpad/rever_marketing_assets.py [cold.pdf rever.pdf]
      defaults: training_samples/sponsorship_deck/sponsors_cold.pdf and rever_disco_diwali_deck_3.pdf (git-ignored; put the two PDFs there).
Output: engine/assets/rever_marketing/{pages,photos,logos}/ and a contact sheet at engine/assets/rever_marketing/crops_sheet.png
"""
import os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "engine", "assets", "rever_marketing")
K = 1920 / 2000.0
INSET = 6

# name -> (deck, page, (x0, y0, x1, y1) in the 2000x1125 slide coordinates, what it shows)
CROPS = {
    # decor and venue set-up: no faces
    "decor_globe":      ("cold", 20, (1360, 215, 1900, 497), "Disco Diwali 2025 stage: red curtain, DIWALI blocks, balloon arch and the globe"),
    "decor_tall":       ("cold", 36, (100, 235, 642, 1037), "the same stage, tall: red drapes, black and silver balloons, DIWALI blocks, clapperboard"),
    "summer_banner":    ("cold", 14, (1314, 73, 1900, 1037), "Summer Sunset: hand-painted 'The Summer AQ turns FIVE' banner on a fishing net"),
    "hall_empty":       ("cold", 10, (100, 437, 535, 1037), "banquet hall with hanging stars, an early dancer, the DJ table"),
    # the day itself
    "stalls_live":      ("cold", 26, (1012, 296, 1445, 512), "4:00 PM stalls go live, marigold garlands (cut below the time chip)"),
    "reg_desk":         ("cold", 30, (708, 73, 1900, 545), "wide shot of the registration desk"),
    "dhol_entry":       ("cold", 27, (1060, 73, 1900, 1037), "dhol entry in blue light (cut right of the caption card)"),
    "dj_console":       ("cold", 20, (797, 638, 1337, 920), "the DJ at the console under fairy lights"),
    "stall_beadify":    ("cold", 20, (797, 215, 1337, 497), "a stall table (Beadify)"),
    "prize_sign":       ("cold", 20, (1360, 638, 1900, 920), "two volunteers holding the Disco Diwali sign and clay pots"),
    # people (older students at events)
    "volunteers_laptops": ("cold", 4, (100, 215, 680, 498), "student volunteers at laptops (cut above the icon badge)"),
    "starry_boys":      ("cold", 4, (1320, 215, 1900, 498), "boys on shoulders under fairy lights (Starry Night; cut above the icon badge)"),
    "group_banner":     ("cold", 22, (1234, 197, 1900, 643), "group at a Disco Diwali under the AQ banner"),
    # the school network
    "school_banner":    ("cold", 6, (1360, 73, 1900, 545), "students in school uniform in front of the AQ roll-up banner"),
    "school_workshop":  ("cold", 4, (710, 215, 1290, 498), "a classroom workshop (cut above the icon badge)"),
    # Rever deck
    "age_strip":        ("rever", 9, (108, 688, 1893, 900), "profile shot of four girls at Disco Diwali 2025 (cut above the caption chip)"),
}


def page(deck, n):
    d = os.path.join(A, "pages", deck)
    return os.path.join(d, [f for f in sorted(os.listdir(d)) if f.startswith(f"p-{n:03d}-")][0])


def ensure_pages(cold, rever):
    for deck, pdf in (("cold", cold), ("rever", rever)):
        d = os.path.join(A, "pages", deck)
        os.makedirs(d, exist_ok=True)
        if not os.listdir(d):
            subprocess.run(["pdfimages", "-j", "-p", pdf, os.path.join(d, "p")], check=True)


def cut(deck, n, box):
    im = Image.open(page(deck, n)).convert("RGB")
    x0, y0, x1, y1 = [round(v * K) for v in box]
    return im.crop((x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET))


def logo_rever(rever):
    """The Rever wordmark: crimson on a white circle (page 29). Un-multiply from white so it sits on any ground."""
    im = np.asarray(Image.open(page("rever", 29)).convert("RGB")).astype(float)
    x0, y0, x1, y1 = [round(v * K) for v in (1400, 250, 1760, 410)]
    c = im[y0:y1, x0:x1]
    a = 1 - c.min(axis=2) / 255.0
    a = np.clip((a - .04) / .9, 0, 1)
    rgb = np.where(a[..., None] > 0.02, (c - 255 * (1 - a[..., None])) / np.maximum(a[..., None], .02), 0).clip(0, 255)
    out = Image.fromarray(np.dstack([rgb, a * 255]).astype("uint8"), "RGBA")
    return out.crop(out.getbbox())


def main(cold, rever):
    ensure_pages(cold, rever)
    for d in ("photos", "logos"):
        os.makedirs(os.path.join(A, d), exist_ok=True)
    thumbs = []
    for name, (deck, n, box, what) in CROPS.items():
        im = cut(deck, n, box)
        im.save(os.path.join(A, "photos", name + ".jpg"), quality=93)
        print(f"{name:20s} {im.width}x{im.height}  {deck} p{n}  {what}")
        thumbs.append((name, im))
    lg = logo_rever(rever)
    lg.save(os.path.join(A, "logos", "rever_logo_from_pdf.png"))   # cross-check only: its "CAFE" line is dark-on-white and fades on black; the build uses engine/assets/rever/rever_logo.png (the user's own file)
    print("rever_logo_from_pdf", lg.size)
    # AQ wordmark pill from the cold cover (white pill, top right)
    x0, y0, x1, y1 = [round(v * K) for v in (1625, 98, 1892, 152)]
    Image.open(page("cold", 1)).convert("RGB").crop((x0, y0, x1, y1)).save(os.path.join(A, "logos", "aq_wordmark_pill_from_pdf.png"))
    # contact sheet
    tw, th, cols = 360, 250, 6
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), (20, 20, 20))
    dr = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(thumbs):
        t = im.copy(); t.thumbnail((tw - 8, th - 8))
        x, y = (i % cols) * tw + 4, (i // cols) * (th + 22) + 4
        sheet.paste(t, (x, y)); dr.text((x, y + th - 4), name, fill=(255, 255, 255))
    sheet.save(os.path.join(A, "crops_sheet.png"))


if __name__ == "__main__":
    sd = os.path.join(ROOT, "training_samples", "sponsorship_deck")
    main(*(sys.argv[1:3] or [os.path.join(sd, "sponsors_cold.pdf"), os.path.join(sd, "rever_disco_diwali_deck_3.pdf")]))
