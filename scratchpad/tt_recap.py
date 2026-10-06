"""TerraThon RECAP (candid cut) carousel (feed 1080x1350): cover + 7 photo slides + close. Real event photos only (engine/assets/terrathon/throwback_cricket/).
Look: TerraThon black, tucked photo card + tilted slab (like the poster hero), shuriken furniture, StretchPro/Sigmar for the cover only, NeutralFace elsewhere.
FACTS: captions describe only what is visible in each frame. The event/venue/date of the photos were not stated by the user, so none is claimed; the close ties to the
UPCOMING Wicket Wars (3rd + 4th Oct, Turf XL, New Alipore, registrations closed per the site). Run: python scratchpad/tt_throwback_cricket.py"""
import asyncio, base64, importlib.util, io, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("tt_events", os.path.join(ROOT, "scratchpad", "tt_events.py"))
tt = importlib.util.module_from_spec(spec); spec.loader.exec_module(tt)
core, B, W = tt.core, tt.B, tt.W
from PIL import Image
import sys
STORY = "story" in sys.argv
H = 1920 if STORY else 1350
GROUND, ORCHID, CREAM, INK, WHITE, SLAB = "#000000", tt.ORCHID, tt.CREAM_HALO, tt.INK, tt.WHITE, tt.SLAB
PH = "engine/assets/terrathon/recap_photos"
SLIDES = [
    ("05", "WE LOVE AQ", "HOMEMADE FRAME. ZERO RESTRAINT.", "50% 58%"),
    ("03", "MAIN CHARACTER ENERGY", "MARIGOLDS, PEACE SIGNS, ONE SELF-AWARE MIRROR.", "50% 72%"),
    ("02", "SQUAD GOALS", "EIGHT PEOPLE. ARMS CROSSED. ALL IN WHITE.", "50% 45%"),
    ("06", "SHOULDER TO SHOULDER", "DIFFERENT JERSEYS. SAME GRIN.", "50% 62%"),
    ("07", "POSE PLAN: IGNORED", "EIGHT FOLLOWED IT. ONE FREESTYLED.", "50% 55%"),
    ("04", "DISCO DIWALI HQ", "MARIGOLDS, BUNTING AND ONE VERY PINK PHONE.", "50% 70%"),
]
N = len(SLIDES)

def photo_uri(n):
    im = Image.open(f"{PH}/{n}.jpg").convert("RGB")
    if im.width > 1500: im = im.resize((1500, int(im.height * 1500 / im.width)))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90); return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

_pi = Image.open("engine/assets/terrathon/partners/partner_strip.png").convert("RGBA"); _pi = _pi.resize((1600, round(1600 * _pi.height / _pi.width)))
_b = io.BytesIO(); _pi.save(_b, "PNG"); STRIP = "data:image/png;base64," + base64.b64encode(_b.getvalue()).decode()

async def slide(kind, out, idx=None):
    els = []
    def el(l, x, y, w, h): els.append((l, x, y, w, h))
    def sticker(name, label, x, y, w, z=5):
        im, src = tt.crop_to_alpha(name); h = w * im.height / im.width; el(label, x, y, w, h)
        return f'<img src="{src}" class="measure" data-tag="{label}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;z-index:{z}">'
    rnd = random.Random(7)
    specks = "".join(f'<circle cx="{rnd.uniform(0, W):.0f}" cy="{rnd.uniform(0, H):.0f}" r="{rnd.choice([.6, .8, 1, 1.3, 1.9]):.1f}" fill="#fff" opacity="{rnd.uniform(.25, .8):.2f}"/>' for _ in range(520))
    parts = [f'<style>{tt.FONT_CSS}</style>', f'<div style="position:absolute;inset:0;background:{GROUND}"></div>', f'<svg style="position:absolute;inset:0;z-index:1" width="{W}" height="{H}">{specks}</svg>']

    CX, CY, CW, CH = (60, 270, 960, 962) if STORY else (60, 122, 960, 730)          # photo card
    SX, SY, SW, SH = 47, (1190 if STORY else 810), 986, 250          # slab (overlaps the card's lower edge: the photo is tucked, as on the posters)
    if kind == "close":
        CH = 0
    # chip + counter
    parts.append(f'<div class="measure" data-tag="chip" style="position:absolute;left:40px;top:{150 if STORY else 44}px;padding:9px 22px;border:5px solid {ORCHID};border-radius:999px;background:{tt.CTA_FILL};color:{INK};font-family:var(--d);font-weight:900;font-size:26px;line-height:1;z-index:10">RECAP</div>'); el("chip", 40, 150 if STORY else 44, 220, 56)
    if kind == "photo":
        parts.append(f'<div class="measure" data-tag="count" style="position:absolute;right:40px;top:{160 if STORY else 54}px;font-family:var(--d);font-weight:900;font-size:26px;color:{WHITE};line-height:1;z-index:10">{idx + 1:02d} / {N:02d}</div>'); el("count", 880, 162 if STORY else 56, 160, 26)

    if kind == "photo":
        f, head, cap, pos = SLIDES[idx]
        el("card", CX, CY, CW, CH)
        parts.append(f'<div class="measure" data-tag="card" style="position:absolute;left:{CX}px;top:{CY}px;width:{CW}px;height:{CH}px;transform:rotate(.8deg);border:14px solid {CREAM};border-radius:44px;overflow:hidden;background:#111;z-index:3">'
                     f'<img src="{photo_uri(f)}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block"></div>')
        m = await B.measure_text([dict(text=head, font="d", size=100, weight=900)])
        hp = min(70, 100 * 880 / m[0]["text_w"])
        body = (f'<div style="font-weight:900;font-size:{hp}px;line-height:1">{head.replace("&", "&amp;")}</div>'
                f'<div style="font-family:Eina,var(--e),sans-serif;font-weight:400;font-size:28px;line-height:1.2;margin-top:14px;max-width:860px;text-transform:uppercase;letter-spacing:.02em">{cap}</div>')
    elif kind == "cover":
        f = "01"; CH = 902 if STORY else 690
        el("card", CX, CY + (60 if not STORY else 60), CW, CH)
        parts.append(f'<div class="measure" data-tag="card" style="position:absolute;left:{CX}px;top:{CY + (60 if not STORY else 60)}px;width:{CW}px;height:{CH}px;transform:rotate(.8deg);border:14px solid {CREAM};border-radius:44px;overflow:hidden;background:#111;z-index:3">'
                     f'<img src="{photo_uri(f)}" style="width:100%;height:100%;object-fit:cover;object-position:50% 40%;display:block"></div>')
        m = await B.measure_text([dict(text="TERRATHON", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT),
                                  dict(text="THE CANDID CUT", font="SigmarOne", size=100, weight=400, letter_spacing=f"{tt.SG_LS}em")], extra_css=tt.FONT_CSS)
        t1 = 100 * 760 / m[0]["text_w"]; t2 = 100 * min(0.8, 760 / m[1]["text_w"])
        body = (f'<div style="font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * t1}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{t1}px;line-height:1.05">TERRATHON</div>'
                f'<div style="font-family:SigmarOne;-webkit-text-stroke:{tt.SG_STROKE * t2}px {INK};letter-spacing:{tt.SG_LS}em;font-size:{t2}px;line-height:1;margin-top:14px;color:{ORCHID}">RECAP</div>')
    else:  # close
        parts.append(sticker("aq_live.png", "hero", 170, 300 if STORY else 100, 740, 3))
        SY = 1190 if STORY else 810; SH = 280
        m = await B.measure_text([dict(text="THANK YOU", font="StretchPro", size=100, weight=400, letter_spacing=f"{tt.ST_LS}em", features=tt.ST_FEAT)], extra_css=tt.FONT_CSS)
        t1 = 100 * 700 / m[0]["text_w"]
        st = f'font-family:StretchPro;-webkit-text-stroke:{tt.ST_STROKE * t1}px {INK};letter-spacing:{tt.ST_LS}em;font-feature-settings:{tt.ST_FEAT};font-size:{t1}px;line-height:1.02'
        body = (f'<div style="{st}">THANK YOU</div>'
                f'<div style="font-weight:400;font-size:30px;line-height:1.2;margin-top:16px">THANKS FOR SHOWING UP  |  NEXT: DISCO DIWALI</div>')
        cf = None
    el("slab", SX - 6, SY - 12, SW + 12, SH + 24)
    parts.append(f'<div class="measure" data-tag="slab" style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;transform:rotate(-1.25deg);background:{SLAB};border:19px solid {ORCHID};border-radius:47px;z-index:8;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;font-family:var(--d);color:{INK};white-space:nowrap;padding:0 18px">{body}</div>')
    # stars on the card corners (constant furniture)
    parts.append(sticker("shuriken.png", "star_a", 20, (450 if STORY else 300) if kind != "close" else (500 if STORY else 250), 92, 9))
    parts.append(sticker("shuriken.png", "star_b", 968, (1290 if STORY else 910) if kind != "close" else (1090 if STORY else 710), 92, 9))
    # footer
    fy = 1650 if STORY else 1250
    sw = 800 if STORY else 720; sh = round(sw * 322 / 2000); sy = SY + SH + (36 if STORY else 40); sx = (W - sw) // 2
    parts.append(f'<img class="measure" data-tag="sponsors" src="{STRIP}" style="position:absolute;left:{sx}px;top:{sy}px;width:{sw}px;height:{sh}px;z-index:9">'); el("sponsors", sx, sy, sw, sh)
    parts.append(f'<img class="measure" data-tag="logo" src="{core.LOGO}" style="position:absolute;left:27px;top:{fy}px;height:56px;z-index:9">'); el("logo", 27, fy, 320, 56)
    ft = "DISCO DIWALI: 10TH NOV" if kind == "close" else ("SWIPE FOR THE CHAOS" if kind == "cover" else "TERRATHON 2026")
    fm = await B.measure_text([dict(text=ft, font="d", size=100, weight=900)]); ff = min(26, 100 * 560 / fm[0]["text_w"]); fw = fm[0]["text_w"] * ff / 100 + 64
    parts.append(f'<div class="measure" data-tag="cta" style="position:absolute;left:{W - 27 - fw}px;top:{fy - 4}px;width:{fw}px;height:64px;border:6px solid {ORCHID};border-radius:999px;background:{tt.CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:9;font-family:var(--d);font-weight:900;font-size:{ff}px;white-space:nowrap;color:{INK}">{ft}</div>'); el("cta", W - 27 - fw, fy - 4, fw, 64)
    html = B.page(W, H, GROUND, "".join(parts), grain=False)
    ign = {("card", "slab"), ("star_a", "card"), ("star_b", "card"), ("star_b", "slab"), ("star_a", "slab"), ("hero", "slab"), ("chip", "card"), ("count", "card"), ("chip", "hero"), ("sponsors", "slab"), ("sponsors", "logo"), ("sponsors", "cta")}
    tp = [("head", INK, SLAB, 60, True), ("cta", INK, tt.CTA_FILL, 24, True), ("chip", INK, tt.CTA_FILL, 26, True), ("count", WHITE, GROUND, 26, True)]
    await B.render(html, out, W, H, elements=els, text_pairs=tp, containers=("slab",), page_bg=GROUND, expect_hero=True, margin=12, collision_ignore=ign, crop_tags=("card",))

async def main():
    d = "out/collaterals/terrathon_recap" + ("_story" if STORY else ""); os.makedirs(d, exist_ok=True)
    async with B.session():
        await slide("cover", f"{d}/00_cover.png")
        for i, s in enumerate(SLIDES): await slide("photo", f"{d}/{i + 1:02d}_{s[0]}.png", idx=i)
        await slide("close", f"{d}/{N + 1:02d}_close.png")
    print("done")
asyncio.run(main())
