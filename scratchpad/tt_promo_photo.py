"""TerraThon PHOTO promotion stories, from the user's sample story templates (2026-09-29). 1080x1920.
  mode "promo": full-bleed photo under a scrim, prize block top-right, blue stars, white card with a GREEN outline holding a TERRATHON chip,
                the sport name in Sigmar One, date and venue, fee and team, then the AQ logo.  (Wed 30 Sep, sports registrations)
  mode "day":   full-bleed photo, TERRATHON chip and DAY chip, AQ logo, and clear space at the bottom for Instagram's tag/mention stickers. (Sat 3, Sun 4)
Photos are read from engine/assets/terrathon/promo_photos/<cricket|fifa|pickleball>/ and .../day_photos/ (any jpg/png/webp), one story per photo.
Run:  python scratchpad/tt_promo_photo.py            (renders every photo it finds)
      python scratchpad/tt_promo_photo.py --demo     (layout check on a synthetic placeholder, NOT a deliverable)"""
import asyncio, base64, glob, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
H = 1920
GREEN, INK, WHITE = "#2FD284", tt.INK, "#FFFFFF"
SPORTS = {"cricket": "wicket_wars", "fifa": "soccer_storm", "pickleball": "picklejam"}
NAME = {"cricket": "CRICKET", "fifa": "FIFA", "pickleball": "PICKLEBALL"}

def data_uri(path, maxw=1500):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    if im.width > maxw: im = im.resize((maxw, int(im.height * maxw / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

async def story(photo_uri, sport, mode, out, day=None):
    ev = tt.EVENTS[SPORTS[sport]] if sport else None
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    def img(name, label, x, y, w, z=5):
        im, src = tt.crop_to_alpha(name); h = w * im.height / im.width; el(label, x, y, w, h)
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<img src="{photo_uri}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover">',
             f'<div style="position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,.50),rgba(0,0,0,.22) 42%,rgba(0,0,0,.62));z-index:1"></div>']
    # TERRATHON chip
    if mode == "promo":
        pv = ev["pool"]
        parts.append(f'<div class="measure" data-tag="prize" style="position:absolute;right:60px;top:300px;text-align:right;color:{WHITE};font-family:var(--d);white-space:nowrap;line-height:1;z-index:6;text-shadow:0 2px 12px rgba(0,0,0,.5)">'
                     f'<div style="font-weight:400;font-size:44px">PRIZE POOL:</div>'
                     f'<div style="font-weight:900;font-size:78px;margin-top:6px"><span style="font-family:\'Noto Color Emoji\';font-weight:400;font-size:56px;margin-right:8px">💸</span>{pv}</div>'
                     f'<div style="font-weight:400;font-size:30px;margin-top:10px">WINNER<span style="font-family:\'Noto Color Emoji\';font-size:24px">🥇</span>: <b style="font-weight:900">{ev["winner"]}</b></div>'
                     f'<div style="font-weight:400;font-size:30px;margin-top:4px">RUNNERS UP<span style="font-family:\'Noto Color Emoji\';font-size:24px">🥈</span>: <b style="font-weight:900">{ev["runners"]}</b></div></div>')
        el("prize", 560, 300, 460, 210)
        top = 1235; ch = 330
        parts.append(img("shuriken.png", "star_a", 28, 330, 100) + img("shuriken.png", "star_b", 950, 760, 100) + img("shuriken.png", "star_c", 14, top - 48, 100, 9) + img("shuriken.png", "star_d", 962, top + ch - 58, 100, 9))
        m = await B.measure_text([dict(text=NAME[sport], font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        nf = 100 * min(1.6, 800 / m[0]["text_w"])
        fee = " ".join(f'{a}<b style="font-weight:900">{b}</b>' for a, b in ev["fee"])
        el("card", 41, top - 6, 998, ch + 12)
        parts.append(f'<div class="measure" data-tag="card" style="position:absolute;left:47px;top:{top}px;width:986px;height:{ch}px;transform:rotate(-1.25deg);background:{tt.SLAB};border:9px solid {GREEN};border-radius:38px;z-index:8;'
                     f'display:flex;flex-direction:column;align-items:center;justify-content:center;color:{INK};white-space:nowrap;text-align:center">'
                     f'<div style="font-family:SigmarOne;-webkit-text-stroke:{tt.SG_STROKE * nf}px {INK};letter-spacing:{tt.SG_LS}em;font-size:{nf}px;line-height:1">{NAME[sport]}</div>'
                     f'<div style="font-family:var(--d);font-weight:400;font-size:30px;line-height:1.1;margin-top:18px">{ev["date"].replace("&", "&amp;")}  |  {ev["venue"]}</div>'
                     f'<div style="font-family:var(--d);font-weight:400;font-size:28px;line-height:1.15;margin-top:8px">{fee}</div></div>')
        parts.append(f'<div class="measure" data-tag="chip" style="position:absolute;left:78px;top:{top - 30}px;padding:8px 22px;border:5px solid {GREEN};border-radius:999px;background:#fff;color:{INK};'
                     f'font-family:var(--d);font-weight:900;font-size:26px;line-height:1;z-index:10;transform:rotate(-1.25deg)">TERRATHON</div>'); el("chip", 78, top - 30, 200, 52)
        ly = top + ch + 40
    else:
        parts.append(f'<div class="measure" data-tag="chip" style="position:absolute;left:60px;top:290px;padding:10px 26px;border:6px solid {tt.ORCHID};border-radius:999px;background:#fff;color:{INK};'
                     f'font-family:var(--d);font-weight:900;font-size:34px;line-height:1;z-index:10">TERRATHON</div>'); el("chip", 60, 290, 240, 60)
        if day: parts.append(f'<div class="measure" data-tag="day" style="position:absolute;right:60px;top:290px;padding:10px 26px;border-radius:999px;background:{tt.ORCHID};color:{INK};'
                             f'font-family:var(--d);font-weight:900;font-size:34px;line-height:1;z-index:10">{day}</div>'); el("day", 780, 290, 240, 60)
        parts.append(img("shuriken.png", "star_a", 30, 380, 100) + img("shuriken.png", "star_b", 950, 1050, 100))
        ly = 1500
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:{(W - 320) / 2}px;top:{ly}px;height:56px;z-index:9">'); el("logo", (W - 320) / 2, ly, 320, 56)
    html = B.page(W, H, "#000", "".join(parts), grain=False)
    await B.render(html, out, W, H, elements=els, text_pairs=[("prize", WHITE, "#333", 44, False), ("card", INK, tt.SLAB, 30, False)], containers=("card",),
                   page_bg="#000", margin=12, collision_ignore={("star_c", "card"), ("star_d", "card"), ("chip", "card")})

async def main(demo):
    os.makedirs("out/collaterals/photo_stories", exist_ok=True)
    async with B.session():
        if demo:
            from PIL import Image
            import numpy as np
            rng = np.random.default_rng(3); g = np.linspace(60, 130, 1920)[:, None, None] * np.ones((1, 1080, 3)); g[..., 1] += 25
            demo_p = "scratchpad/tt/placeholder_photo.jpg"; os.makedirs("scratchpad/tt", exist_ok=True)
            Image.fromarray(np.clip(g + rng.normal(0, 6, g.shape), 0, 255).astype("uint8")).save(demo_p)
            uri = data_uri(demo_p)
            for sp in SPORTS: await story(uri, sp, "promo", f"out/collaterals/photo_stories/_DEMO_{sp}.png")
            await story(uri, None, "day", "out/collaterals/photo_stories/_DEMO_day.png", day="DAY 1"); print("demo done"); return
        n = 0
        for sp in SPORTS:
            for f in sorted(glob.glob(f"engine/assets/terrathon/promo_photos/{sp}/*.*")):
                if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    n += 1; await story(data_uri(f), sp, "promo", f"out/collaterals/photo_stories/{sp}_{os.path.splitext(os.path.basename(f))[0]}.png")
        for i, f in enumerate(sorted(glob.glob("engine/assets/terrathon/day_photos/*.*"))):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                n += 1; await story(data_uri(f), None, "day", f"out/collaterals/photo_stories/day_{i + 1:02d}.png", day=os.environ.get("TT_DAY", "DAY 1"))
        print("rendered", n, "stories" if n else "(no photos found: add files under engine/assets/terrathon/promo_photos/<sport>/ and day_photos/)")
if __name__ == "__main__":
    asyncio.run(main("--demo" in sys.argv))
