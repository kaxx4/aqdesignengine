"""DISCO DIWALI carousel, "the group chat" (user inspo, 2026-10-18: a bright photo with iMessage-style bubbles laid over it, a short
back-and-forth that escalates: grey incoming on the left, blue outgoing on the right, the brand signing off at the foot).

MECHANISM (kept): the photograph is the scene, the bubbles are the voice. Each slide is one beat of a conversation, the grey side asks and
the blue side answers, and the answer is the information. The brand lockup signs off at the bottom the way the logo does in the inspo.

Slides (1080x1350, feed 4:5):
  01 cover   "disco diwali? / masquerade sangeet edition, / say less."   lockup large
  02         "tickets? / open soon, / how soon? / link in the bio."
  03         "what's it for? / all for charity. / okay, i'm in."
  04 cta     "how do i join? / link in the bio. / joining now."
  Every slide carries the LIVE / ALL FOR CHARITY badge top left (as on every earlier story and poster) and the SAME lockup footer, same size and place.
  The copy says "link in the bio" and never "whatsapp group" (user, 2026-10-18). The link is for joining the group; it is not a booking link.

COPY (CLAUDE.md sec 9, R12 "nothing is invented"): every fact in a blue bubble is supplied copy (edition name, ticket sales open soon, more details to
follow, all for charity, link in bio). The grey questions and the "say less / okay, i'm in / on it" beats are voice, not facts. No date, time or location
(user, 2026-10-14). No dress code, lineup or price.

ADAPTATIONS (sec 2 ladder, all recorded):
  - The inspo's "DRINK RESPONSIBLY" line and drinks imagery are for another brand and an alcohol product; this event has minors present. Dropped.
  - The bubbles are drawn UI laid over a real photo, not a fabricated screenshot. iMessage grey and blue are colours of the borrowed device, so they
    sit outside the format palette on purpose, like the LIVE badge's own blue. Body type is Eina, lowercase, as the house body face (sec 9).
  - R2 (one hero = the lockup) bends on 02-03: the photo and the conversation are the hero, the small lockup signs off.
  - CONSENT: many people in these photos look like minors and none has a consent record. Check before any public post.

Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_chat_carousel.py     -> out/discodiwali/carousel/chat/slide_NN.png (+ sheet.png)
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
B, GROUND, OFFWHITE = dd.B, dd.GROUND, dd.OFFWHITE
OUT = os.path.join(ROOT, "out", "discodiwali", "carousel", "chat")
HALL = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-hall-2026-10-14")
HALLP = lambda n: os.path.join(HALL, n)
W, H, N = 1080, 1350, 4
GREY, BLUE, M = "#E9E9EB", "#0A84FF", 64
FS, PADX, PADY, GAP = 56, 42, 26, 34                      # bubble type size, horizontal / vertical padding, gap between bubbles
BBOX = {"title_lockup_noball.png": (265, 401, 1983, 1315), "title_lockup.png": (265, 315, 1983, 1315)}
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Ticket sales open soon")

# each slide: photo, object-position, [(side, text)], lockup width, lockup name
SLIDES = [
    dict(photo=HALLP("04_pink-ceiling-chandelier-phone.jpg"), focus="50% 50%", lock=(480, "title_lockup.png"),
         chat=[("l", "disco diwali?"), ("r", "masquerade sangeet edition,"), ("l", "say less.")]),
    dict(photo=HALLP("01_dancers-silver-pillar-purple.jpg"), focus="45% 50%", lock=(480, "title_lockup.png"),
         chat=[("l", "tickets?"), ("r", "sales open soon,"), ("l", "where's the info?"), ("r", "link in the bio.")]),
    dict(photo=HALLP("09_boy-on-shoulders-star-balloon.jpg"), focus="70% 50%", lock=(480, "title_lockup.png"),
         chat=[("l", "what's it for?"), ("r", "all for charity."), ("l", "okay, i'm in.")]),
    dict(photo=HALLP("08_boy-on-shoulders-stage-lights-portrait.jpg"), focus="50% 0%", lock=(480, "title_lockup.png"),
         chat=[("l", "how do i join?"), ("r", "link in the bio."), ("l", "joining now.")]),
]

CSS = (f".bub{{position:absolute;box-sizing:border-box;border-radius:{(FS + 2 * PADY) // 2 + 6}px;font-family:var(--e);font-weight:400;font-size:{FS}px;"
       f"line-height:1;white-space:nowrap;z-index:12;display:flex;align-items:center;justify-content:center;"
       f"filter:drop-shadow(0 6px 18px rgba(0,0,0,.28))}}"
       f".bub.l{{background:{GREY};color:#000}}.bub.r{{background:{BLUE};color:#fff}}"
       f".bub svg{{position:absolute;bottom:0;width:34px;height:30px;overflow:visible}}.bub.l svg{{left:-9px}}.bub.r svg{{right:-9px;transform:scaleX(-1)}}")
TAIL = '<svg viewBox="0 0 34 30"><path d="M34 0 L34 30 C22 30 8 27 0 25 C14 19 20 11 20 0 Z" fill="{c}"/></svg>'


class Slide:
    def __init__(self, idx, spec, widths):
        self.idx, self.spec, self.widths = idx, spec, widths
        self.p = dd.Poster("poster_ref", BRIEF, "feed")
        self.p.parts.clear(); self.p.elements.clear()
        self.P = self.p.parts

    def ground(self):
        s = self.spec
        self.P.append(f'<div style="position:absolute;inset:0;background:{GROUND}"></div>')
        self.P.append(f'<img data-tag="photo" src="{dd.photo_uri(s["photo"])}" style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;'
                      f'object-position:{s["focus"]};z-index:1;filter:contrast(1.06) saturate(1.0) brightness(.95)">')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:2;background:linear-gradient(180deg,#0A1E7A,#050A33);mix-blend-mode:multiply;opacity:.22"></div>')
        self.P.append('<div data-tag="plate" style="position:absolute;inset:0;z-index:3;background:linear-gradient(180deg,rgba(0,0,0,.28) 0%,rgba(0,0,0,0) 30%,'
                      'rgba(0,0,0,0) 52%,rgba(0,0,0,.82) 100%)"></div>')

    def badge(self, w=236):
        self.p.img("live_badge.png", M, 70, w, z=8, tag="badge")
        self.p.box("badge", M, 70, w, round(w * 1005 / 1061))

    def chat(self, y0=330):
        y = y0
        for k, (side, text) in enumerate(self.spec["chat"], 1):
            tw = self.widths[text]
            w = round(tw + 2 * PADX); h = FS + 2 * PADY
            x = M if side == "l" else W - M - w
            tail = TAIL.format(c=GREY if side == "l" else BLUE)
            self.P.append(f'<div data-tag="bubble{k}" class="bub {side}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{tail}{text}</div>')
            self.p.box(f"bubble{k}", x, y, w, h)
            y += h + GAP

    def lockup(self):
        w, name = self.spec["lock"]
        x0, y0, x1, y1 = BBOX[name]
        k = w / (x1 - x0); vh = round((y1 - y0) * k)
        vx, vy = (W - w) // 2, H - 70 - vh                             # centred, 70px above the foot
        self.p.img(name, round(vx - x0 * k), round(vy - y0 * k), round(2000 * k), z=9, tag="title")
        self.p.box("title", vx, vy, w, vh)

    def finish(self):
        self.p.overlays()
        page = B.page(W, H, GROUND, "".join(self.P), grain=False)
        return page.replace("</style>", CSS + "</style>", 1)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with B.session():
        texts = sorted({t for s in SLIDES for _, t in s["chat"]})
        res = await B.measure_text([dict(text=t, font="e", size=FS, weight=400) for t in texts])
        widths = {t: r["text_w"] for t, r in zip(texts, res)}
        for i, spec in enumerate(SLIDES, 1):
            s = Slide(i, spec, widths)
            s.ground(); s.badge(); s.chat(); s.lockup()
            html = s.finish()
            labels = {e[0] for e in s.p.elements}
            text_pairs = [("bubble_grey", "#000000", GREY, FS, False), ("bubble_blue", "#FFFFFF", BLUE, FS, False)]
            await B.render(html, os.path.join(OUT, f"slide_{i:02d}.png"), W, H, elements=s.p.elements, collision_ignore=[], text_pairs=text_pairs,
                           bleed_tags=("title", "plate", "sparkles", "grain", "photo"), crop_tags=("plate", "sparkles", "grain", "photo"), page_bg=GROUND)
    from PIL import Image
    ims = [Image.open(os.path.join(OUT, f"slide_{i:02d}.png")).convert("RGB").resize((432, 540)) for i in range(1, N + 1)]
    sh = Image.new("RGB", (442 * N, 540), (40, 40, 40))
    for i, im in enumerate(ims):
        sh.paste(im, (i * 442, 0))
    sh.save(os.path.join(OUT, "sheet.png"))
    print("chat carousel done ->", OUT)

asyncio.run(main())
