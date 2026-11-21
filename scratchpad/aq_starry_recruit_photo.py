"""AQ EVENTS TEAM recruitment story for STARRY NIGHT on a REAL PHOTO ground (user-supplied DJ-console photo), 1080x1920, AQ house style.

The photo is the background. The text is placed and COLOURED from what the photo actually is behind it: the photo is cover-cropped to 9:16, graded, and a navy-ink scrim is baked into the
pixels (strong at the top where the headline lives, clear through the middle where the console is the hero, strong again at the foot for the CTA). The script then MEASURES the worst-case
(90th percentile) luminance behind every text block of the baked background and asserts the WCAG contrast of the chosen colour against it; text that fails raises. Surfaces handed to
text_pairs are those measured colours, not guesses. Photo-ground conventions (CLAUDE.md sec 9): the wordmark sits in a cream pill, never white-inverted; craft is outline_of(surface), cream on dark.
Adaptations: AQ cream ground replaced by the photo (the user's request); one serif accent word ('starry'); sky is the Events hue; lemon is the star accent.
Facts: Starry Night is AQ's Christmas carnival fundraiser (Dec 2024, 2.0 in Dec 2025). NOT supplied, NOT printed: edition, date, venue, roles, deadline, link. CTA LINK IN BIO is the AQ convention.
Run: PYTHONIOENCODING=utf-8 python scratchpad/aq_starry_recruit_photo.py"""
import asyncio, base64, io, os, sys, importlib.util
import numpy as np
from PIL import Image, ImageEnhance
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine"); sys.path.insert(0, ENGINE_DIR)
def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
core = load("core"); B = load("build"); dd = load("doodles")
W, H = core.SIZES["story"]; M = 64
INK, CREAM, SKY, LEMON = core.INK, core.CREAM, core.accent_for("events"), core.ACCENTS[2]
PHOTO = "engine/assets/img/events/starry-recruit-2026-11/dj_console.jpg"
SCRIM = np.array([6, 5, 24], dtype=float)

def alpha_profile(y):                 # scrim opacity by row: heavy for the headline, clear for the console, heavy for the CTA
    pts = [(0, .74), (700, .68), (1010, .64), (1240, .56), (1360, .22), (1470, .0), (1680, .78), (1920, .86)]
    return np.interp(y, [p[0] for p in pts], [p[1] for p in pts])

def baked_background():
    im = Image.open(PHOTO).convert("RGB"); s = H / im.height                      # cover: fit height, crop width
    im = im.resize((round(im.width * s), H), Image.LANCZOS)
    left = round((im.width - W) * .62)                                            # keep the hands + console, trim the far-left blur
    im = im.crop((left, 0, left + W, H)); im = ImageEnhance.Contrast(im).enhance(1.06)
    a = np.asarray(im, dtype=float); al = alpha_profile(np.arange(H))[:, None, None]
    out = a * (1 - al) + SCRIM * al
    return Image.fromarray(out.clip(0, 255).astype("uint8"))

def lum(rgb):
    c = [(v / 255) / 12.92 if v / 255 <= .03928 else (((v / 255) + .055) / 1.055) ** 2.4 for v in rgb]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def hex_rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def contrast(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
def behind(bg, x, y, w, h):           # worst-case (lightest 10%) colour behind a box
    r = np.asarray(bg.crop((round(x), round(y), round(x + w), round(y + h))), dtype=float).reshape(-1, 3)
    L = np.array([lum(p) for p in r[::7]]); idx = np.argsort(L)[int(len(L) * .9)]; return tuple(r[::7][idx])

els = []; checks = []
def box(label, x, y, w, h, html, z=10):
    els.append((label, round(x), round(y), round(w), round(h)))
    return f'<div data-tag="{label}" style="position:absolute;left:{round(x)}px;top:{round(y)}px;width:{round(w)}px;height:{round(h)}px;z-index:{z}">{html}</div>'

async def main():
    bg = baked_background(); buf = io.BytesIO(); bg.save(buf, "JPEG", quality=93)
    bg_uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    async with B.session():
        pr = await B.measure_text([{"text": "EVENTS", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                   {"text": "TEAM", "font": "d", "size": 100, "weight": 900, "transform": "uppercase"},
                                   {"text": "starry night", "font": "s", "size": 100, "weight": 400}], W, H)
        ev_size = 100 * (W - 2 * M) / pr[0]["text_w"]; sn_size = 100 * 700 / pr[2]["text_w"]
        sz = await B.measure_text([{"text": "JOIN THE", "font": "d", "size": 92, "weight": 900, "transform": "uppercase", "line_height": .9},
                                   {"text": "EVENTS", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "TEAM", "font": "d", "size": ev_size, "weight": 900, "transform": "uppercase", "line_height": .86},
                                   {"text": "starry night", "font": "s", "size": sn_size, "weight": 400, "line_height": .9}], W, H)
        join_h, ev_h, team_h, sn_h = (s["ink_h"] for s in sz); team_w = sz[2]["text_w"]; join_w = sz[0]["text_w"]; sn_w = sz[3]["text_w"]
        parts = [f'<img data-tag="plate" src="{bg_uri}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;z-index:0">']
        ring = f"0 0 0 4px {CREAM}"
        # wordmark in a cream pill (photo ground), safe below Instagram's top bar
        lx, ly = M, 210
        parts.append(box("logo", lx, ly, 214, 62, f'<div style="width:100%;height:100%;background:{CREAM};border:4px solid {INK};border-radius:999px;box-shadow:{ring};box-sizing:border-box;display:flex;align-items:center;justify-content:center">'
                         f'<img src="{core.LOGO}" style="height:30px"></div>', z=20))
        # eyebrow chip, ink on sky (own surface)
        parts.append(box("eyebrow", M + 214 + 24, ly + 3, 300, 56, f'<div style="width:100%;height:100%;background:{SKY};border:4px solid {INK};border-radius:999px;box-shadow:{ring};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.14em;color:{INK}">NOW RECRUITING</div>', z=20))
        checks.append(("eyebrow chip", hex_rgb(INK), hex_rgb(SKY), 20, True))
        y = ly + 62 + 58
        # headline lines: white, measured against the baked background behind each line
        def line(label, txt, y0, size, ink_h, w, lh, font="d", extra=""):
            x = M - 4 if label == "events" else M
            surf = behind(bg, x, y0, w, ink_h); col = "#FFFFFF" if contrast((255, 255, 255), surf) >= 4.5 else None
            assert col, f"{label}: white fails on its photo ground (contrast {contrast((255,255,255), surf):.2f}); raise the scrim"
            checks.append((label, (255, 255, 255), surf, size, True))
            return box(label, x, y0, w, ink_h, f'<div style="font-family:var(--{font});font-weight:900;font-size:{size:.0f}px;line-height:{lh};text-transform:uppercase;color:{col};white-space:nowrap;{extra}">{txt}</div>')
        parts.append(line("join", "JOIN THE", y, 92, join_h, join_w + 20, .9)); y += join_h + 14
        parts.append(line("events", "EVENTS", y, ev_size, ev_h, W - 2 * M + 8, .86)); y += ev_h + 28
        pad_x, pad_y = 40, 22; bw, bh = team_w + 2 * pad_x, team_h + 2 * pad_y
        parts.append(box("team", M, y, bw, bh, f'<div style="width:100%;height:100%;background:{SKY};border:5px solid {INK};border-radius:{core.RADII["outer"]}px;box-shadow:{ring},12px 12px 0 4px {INK};box-sizing:border-box;'
                         f'display:flex;align-items:center;justify-content:center"><span style="font-family:var(--d);font-weight:900;font-size:{ev_size:.0f}px;line-height:.86;text-transform:uppercase;color:{INK}">TEAM</span></div>', z=11))
        checks.append(("team plate", hex_rgb(INK), hex_rgb(SKY), ev_size, True))
        sx = M + bw + 40; surf = behind(bg, sx, y + bh / 2 - 60, W - M - sx, 120)
        assert contrast((255, 255, 255), surf) >= 4.5
        parts.append(box("sub", sx, y + bh / 2 - 60, W - M - sx, 120, f'<div style="font-family:var(--e);font-weight:600;font-size:34px;line-height:1.18;color:#fff">come run<br>the night<br>with us</div>'))
        checks.append(("sub", (255, 255, 255), surf, 34, False)); y += bh + 54
        # starry night lockup: serif lemon on the measured ground, lemon only if it clears 4.5
        surf = behind(bg, M, y, sn_w + 20, sn_h)
        lemon_ok = contrast(hex_rgb(LEMON), surf) >= 4.5
        sn_col = LEMON if lemon_ok else "#FFFFFF"
        parts.append(box("starry", M, y, sn_w + 30, sn_h, f'<div style="font-family:var(--s);font-style:italic;font-size:{sn_size:.0f}px;line-height:.9;color:{sn_col};white-space:nowrap">starry night</div>'))
        checks.append(("starry night", hex_rgb(sn_col), surf, sn_size, True)); y += sn_h + 22
        surf = behind(bg, M, y, 560, 24)
        parts.append(box("label", M, y, 560, 24, f'<div style="font-family:var(--m);font-weight:700;font-size:17px;letter-spacing:.12em;color:#fff;white-space:nowrap">THE CHRISTMAS CARNIVAL FUNDRAISER</div>'))
        checks.append(("label", (255, 255, 255), surf, 17, False))
        # CTA row on the bottom scrim
        cy = 1640 - 78
        parts.append(box("cta", M, cy, 360, 78, f'<div style="width:100%;height:100%;background:{SKY};border:4px solid {INK};border-radius:999px;box-shadow:{ring};box-sizing:border-box;display:flex;align-items:center;justify-content:center;'
                         f'font-family:var(--m);font-weight:700;font-size:24px;letter-spacing:.1em;color:{INK}">LINK IN BIO</div>', z=12))
        checks.append(("cta", hex_rgb(INK), hex_rgb(SKY), 24, True))
        surf = behind(bg, M + 400, cy + 24, 400, 30)
        parts.append(box("handle", M + 400, cy + 24, 400, 30, f'<div style="font-family:var(--m);font-weight:700;font-size:20px;letter-spacing:.05em;color:#fff">@ngo.aquaterra</div>'))
        checks.append(("handle", (255, 255, 255), surf, 20, False))
        for name, fg, surf, size, bold in checks:
            need = 3.0 if (size >= 24 and bold) or size >= 36 else 4.5
            c = contrast(fg, surf); print(f"  contrast {name:14s} {c:5.2f} (need {need})"); assert c >= need, f"{name} fails: {c:.2f} < {need}"
        tp = [(n, "#%02x%02x%02x" % tuple(int(v) for v in fg), "#%02x%02x%02x" % tuple(int(v) for v in surf), s, b) for n, fg, surf, s, b in checks]
        os.makedirs("out/aq_events", exist_ok=True)
        await B.render(B.page(W, H, "#000", "".join(parts), grain=False), "out/aq_events/starry_recruit_photo_story.png", W, H, elements=els, text_pairs=tp, page_bg="#000",
                       bleed_tags=("plate",), crop_tags=("plate",), collision_ignore=[("team", "events"), ("team", "sub")], expect_hero=True)
        print("CTA row ends at", cy + 78, "of", H)
asyncio.run(main())
