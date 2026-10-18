"""Companion art for the Disco Diwali chat carousel ("Call and Answer"). Out: out/discodiwali/carousel/chat/companion/call_and_answer.png"""
import os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "out/discodiwali/carousel/chat/companion")
S = 2; W, H = 1080 * S, 1350 * S
INK, OFF, GOLD, BLUE, DIM = (6, 6, 9), (236, 234, 226), (232, 192, 99), (10, 132, 255), (150, 148, 140)
fonts = sorted(glob.glob(os.path.join(ROOT, "engine/assets/fonts/NeutralFace*.otf")))
small = ImageFont.truetype(fonts[0], 14 * S); mid = ImageFont.truetype(fonts[-1], 24 * S)
img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
M, bh, step = 120, 44, 96
bars = [("l", 240), ("r", 560), ("l", 170), ("r", 700), ("l", 300), ("r", 420), ("l", 200), ("r", 620), ("l", 340), ("r", 480)]
y = 300
for side, L in bars:
    x0 = M if side == "l" else 1080 - M - L
    d.rounded_rectangle([x0 * S, y * S, (x0 + L) * S, (y + bh) * S], radius=(bh // 2) * S, fill=OFF if side == "l" else BLUE)
    y += step
d.line([M * S, (y + 30) * S, (1080 - M) * S, (y + 30) * S], fill=GOLD, width=2 * S)
d.text((M * S, 120 * S), "DISCO DIWALI", font=mid, fill=OFF)
d.text((M * S, 162 * S), "CALL AND ANSWER  /  TEN TURNS", font=small, fill=DIM)
img = img.resize((W // S, H // S), Image.LANCZOS)
img.save(os.path.join(OUT, "call_and_answer.png"))
