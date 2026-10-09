"""Trace the illustrated Kolkata school map (extracted raster img_152) into clean vector geometry for the deck redesign.
Outputs scratchpad/sponsorship_private/map.json: {w,h, outline:[path d], river:[d], parks:[d], pins:[{n,name,x,y}]}.
Pins are matched from detected dark-red blobs to the hand-read label order (the labels are raster text, so the NAMES are typed here,
read off the source image; positions come from the pixels)."""
import json, os
import cv2, numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "engine/assets/sponsorship/img_152.png")
OUT = os.path.join(ROOT, "scratchpad/sponsorship_private/map.json")

# label order read off the source; (x,y) = approximate pin head in source px, used only to match the detected blobs
NAMES = [
    ("Calcutta Boys' School", 685, 145), ("St. Xavier's Collegiate School", 551, 292), ("La Martiniere for Boys", 715, 346),
    ("La Martiniere for Girls", 829, 405), ("Loreto House", 567, 482), ("St. James' School", 766, 522),
    ("Birla High School", 459, 583), ("Don Bosco School Park Circus", 699, 655), ("Modern High School for Girls", 415, 687),
    ("South Point High School", 554, 789), ("Mahadevi Birla World Academy", 757, 794), ("Garden High School", 319, 844),
    ("Army Public School Ballygunge", 516, 920), ("Delhi Public School Ruby Park", 828, 946), ("St. Lawrence High School", 584, 1030),
    ("The Heritage School", 401, 1137), ("Calcutta International School", 270, 1210), ("Cambridge Academy", 630, 1276),
]


def path_of(cnt, eps):
    c = cv2.approxPolyDP(cnt, eps, True).reshape(-1, 2)
    return "M" + " L".join(f"{x},{y}" for x, y in c) + "Z"


def main():
    im = np.asarray(Image.open(SRC).convert("RGBA"))
    h, w = im.shape[:2]
    a = im[..., 3]
    rgb = im[..., :3].astype(int)
    sil = (a > 128).astype(np.uint8) * 255
    sil = cv2.morphologyEx(sil, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max(cs, key=cv2.contourArea)
    outline = [path_of(big, 2.2)]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    river = ((b > 150) & (r < 120) & (g > 100) & (g < 190) & (a > 128)).astype(np.uint8) * 255
    river = cv2.morphologyEx(river, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    cs, _ = cv2.findContours(river, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rv = [path_of(c, 2.0) for c in cs if cv2.contourArea(c) > 20000]
    parks = ((g > r + 18) & (g > b + 18) & (r > 100) & (a > 128)).astype(np.uint8) * 255
    parks = cv2.morphologyEx(parks, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    cs, _ = cv2.findContours(parks, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    pk = [path_of(c, 1.6) for c in cs if 900 < cv2.contourArea(c) < 40000]
    red = ((r > 140) & (g < 40) & (b < 50) & (a > 200)).astype(np.uint8) * 255
    red = cv2.morphologyEx(red, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, stats, cen = cv2.connectedComponentsWithStats(red)
    blobs = [(cen[i][0], cen[i][1] - 0, stats[i][cv2.CC_STAT_AREA]) for i in range(1, n) if stats[i][cv2.CC_STAT_AREA] > 150]
    pins, used = [], set()
    for k, (nm, ex, ey) in enumerate(NAMES, 1):
        best = min((i for i in range(len(blobs)) if i not in used), key=lambda i: (blobs[i][0] - ex) ** 2 + (blobs[i][1] - ey) ** 2)
        used.add(best)
        bx, by, _ = blobs[best]
        pins.append({"n": k, "name": nm, "x": round(float(bx), 1), "y": round(float(by), 1), "err": round(((bx - ex) ** 2 + (by - ey) ** 2) ** .5, 1)})
    json.dump({"w": w, "h": h, "outline": outline, "river": rv, "parks": pk, "pins": pins}, open(OUT, "w"))
    print("blobs", len(blobs), "river", len(rv), "parks", len(pk), "max pin err", max(p["err"] for p in pins))


if __name__ == "__main__":
    main()
