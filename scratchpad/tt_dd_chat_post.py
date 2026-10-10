"""DISCO DIWALI "the chat" teaser (user, 2026-10-10): static post (1080x1350) + story (1080x1920, arg: story).
Mechanism from the user's reference: a thank-you story where comment bubbles (white, tilted, with heart-reaction pills and
avatar dots) hang on thin vertical strings under a short title, plus two small story-photo cards in the pile.
HARD RULE honoured: NO fabricated comments. The reference's bubbles were real comments from real people; invented ones would be
fake reviews presented as genuine. Here the bubbles are AQ's OWN lines (unsigned, no usernames, no photos of people as avatars;
avatars are shuriken dots), so nothing pretends to be a person talking. Tickets/date/venue/price are not mentioned (user ruling).
Photos: the user's real DD photos, small cards. Adaptation: blurred wallpaper -> TerraThon black starfield; white bubbles -> cream + orchid keyline.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_dd_chat_post.py [story]  -> out/collaterals/dd_chat[_story].png
"""
import asyncio, importlib.util, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sp = importlib.util.spec_from_file_location("fc", os.path.join(ROOT, "scratchpad", "tt_dd_folder_carousel.py"))
fc = importlib.util.module_from_spec(sp); sp.loader.exec_module(fc)
B, W, H, STORY, PH, rb = fc.B, fc.W, fc.H, fc.STORY, fc.PH, fc.rb
ORCHID, CTA_FILL, INK, WHITE, GROUND, GREEN = fc.ORCHID, fc.CTA_FILL, fc.INK, fc.WHITE, fc.GROUND, fc.GREEN
K, OFF = (1.05, 190) if STORY else (1.0, 0)
Y = lambda y: round(OFF + y * K)

STRINGS = [(60, 330), (110, 560), (340, 250), (545, 290), (975, 1050), (1030, 560)]   # (x, end y) in design space; the title column stays clear
BUBBLES = [  # x, y, w, rot, text, heart, avatar
    (70, 520, 360, -5, "outfit sorted yet?", True, True),
    (520, 505, 480, 5, "bring your people. all of them.", False, True),
    (90, 650, 400, -3, "disco balls. diyas. chaos.", False, False),
    (540, 665, 440, 3, "the dance floor is warming up...", True, False),
    (40, 800, 300, -5, "save this post.", False, True),
    (690, 800, 360, 4, "tag your plus one.", True, False),
    (60, 1015, 430, -3, "told you something was loading.", True, True),
    (560, 1020, 420, 4, "see you on the floor.", False, False),
    (300, 1135, 440, -2, "more soon. stay tuned.", True, False)]
PHOTOS = [(365, 800, 150, 200, -5, "dance", "55% 35%"), (530, 830, 150, 200, 5, "group", "40% 40%")]


async def main():
    s = fc.Slide(1, 701)
    im, src = fc.tt.crop_to_alpha("shuriken.png")
    # strings (behind everything)
    for i, (x, ye) in enumerate(STRINGS):
        s.add(f'<div style="position:absolute;left:{x}px;top:0;width:3px;height:{Y(ye)}px;background:{CTA_FILL};opacity:.9;z-index:2"></div>')
    ty = Y(300)
    yb, _ = await s.title("GET READY FOR", "DISCO DIWALI", ty, w1=520, w2=780)
    s.allow("t1", "t2")
    for i, (x, y, w, rot, txt, heart, av) in enumerate(BUBBLES):
        lines = max(1, math.ceil(len(txt) * 16.5 / (w - 56)))
        h = lines * 40 + 46
        yy = Y(y)
        s.add(f'<div class="measure" data-tag="b{i}" style="position:absolute;left:{x}px;top:{yy}px;width:{w}px;height:{h}px;box-sizing:border-box;transform:rotate({rot}deg);border:5px solid {ORCHID};border-radius:36px;background:{CTA_FILL};'
              f'display:flex;align-items:center;padding:0 26px;font-family:var(--e);font-size:32px;line-height:1.15;color:{INK};z-index:6">{txt}</div>')
        s.el(f"b{i}", *rb(x, yy, w, h, rot))
        if heart:
            hx, hy = x + 26, yy + h - 12
            s.add(f'<div class="measure" data-tag="h{i}" style="position:absolute;left:{hx}px;top:{hy}px;width:58px;height:42px;box-sizing:border-box;border:4px solid {ORCHID};border-radius:999px;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;font-size:22px;z-index:8">❤️</div>')
            s.el(f"h{i}", hx, hy, 58, 42); s.allow(f"b{i}", f"h{i}")
        if av:
            ax, ay = (x + w - 34, yy - 22) if i % 2 else (x - 20, yy + h - 40)
            s.add(f'<div class="measure" data-tag="a{i}" style="position:absolute;left:{ax}px;top:{ay}px;width:52px;height:52px;box-sizing:border-box;border:4px solid {ORCHID};border-radius:50%;background:{CTA_FILL};display:flex;align-items:center;justify-content:center;z-index:8">'
                  f'<img src="{src}" style="width:30px"></div>')
            s.el(f"a{i}", ax, ay, 52, 52); s.allow(f"b{i}", f"a{i}")
    for j, (x, y, w, h, rot, key, pos) in enumerate(PHOTOS):
        fc.photo_card(s, f"ph{j}", key, x, Y(y), w, h, rot, pos, z=5)
    s.footer(cta="STAY TUNED")
    for i in range(len(BUBBLES)):                      # overlapping tilted bubbles touch their neighbours' bounding boxes; the looking gate judges them
        for j in range(i + 1, len(BUBBLES)): s.allow(f"b{i}", f"b{j}")
    for i in range(len(BUBBLES)):
        for j in range(len(PHOTOS)): s.allow(f"b{i}", f"ph{j}")
    out = "out/collaterals/dd_chat" + ("_story" if STORY else "") + ".png"
    os.makedirs("out/collaterals", exist_ok=True)
    text_pairs = [("bubble", INK, CTA_FILL, 32, False), ("cta", INK, CTA_FILL, 30, True)]
    async with B.session():
        await B.render(s.html(), out, W, H, elements=s.els, text_pairs=text_pairs, page_bg=GROUND, expect_hero=False,
                       collision_ignore=set(map(tuple, s.ign)), margin=12, crop_tags=("ph0", "ph1"))
    print("done", out)

asyncio.run(main())
