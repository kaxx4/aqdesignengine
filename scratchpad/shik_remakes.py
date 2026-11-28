"""THREE REMAKES in the Shikshaq language, from three reference images supplied by the owner (other brands' posters).

Each reference is a MECHANISM; the remake keeps the mechanism and is rebuilt from engine/shikshaq.py with Shikshaq content
taken from the site's own copy. Nothing is copied: no photographs, no illustrations, no other brand's wording.

  1. CHAT   (square)  ref: a giant chat bubble as a dining table, a person seated at each end.
                      remake: the bubble is a student's message, a mascot at each end peeking over it; the ask is
                      "message a teacher on WhatsApp", which is the site's one conversion.
  2. TEASER (feed)    ref: "We can't show you yet." on a tabbed index-card over a photo strip, lavender graph grid.
                      remake: the site's own graph-paper ground (device I), a strip of paper covers (one real Maths cover,
                      the rest blank because the site says only "other subjects, coming soon"), a tabbed card.
  3. FLIP   (feed)    ref: an upside-down building hanging from the top, a figure on a hill below.
                      remake: upside-down paper covers hang from the top edge, a headline, a hill with the mascot.

Adaptations (recorded per the precedence ladder): the reference photographs are not reproduced (real-assets-only, and
they are other brands'); a doodle wallpaper became the site's graph paper, not a faint wash of icons; hand lettering
became Archivo/Geist; the sender and replier are mascots, not people; no number appears in the copy.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/shik_remakes.py
"""
import asyncio, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

MATHS = sk.subject_palette("Maths")
COPY = {
    "chat": dict(msg="Can you explain this chapter again?", h1="Ask a teacher.", h2="Directly.",
                 sub="On WhatsApp, free. Shikshaq never sits in the middle.", cta="Message on WhatsApp", url="shikshaq.in"),
    "teaser": dict(h=["We can’t show", "you yet."], sub="More subjects are on the way. Maths is out now.",
                   t1="Maths: out now", t2="Next up", t3="Stay tuned", url="shikshaq.in"),
    "flip": dict(h1="Flip your", h2="perspective.",
                 body="Real board papers, read as questions with marks and chapters. Free to read, before the exam reads you.",
                 url="shikshaq.in"),
}
STRINGS = [v for c in COPY.values() for v in (c.values()) for v in (v if isinstance(v, list) else [v])]


def h(text, size, w=400, extra=""):
    return f'<div style="font-family:Archivo;font-weight:{w};font-size:{size}px;line-height:1;letter-spacing:-.05em;{extra}">{text}</div>'


# ───────────────────────── 1. CHAT (square 1080) ─────────────────────────
W1, H1 = sk.SIZES["square"]
c = COPY["chat"]
tail = ('<svg width="90" height="70" viewBox="0 0 90 70" style="position:absolute;right:46px;bottom:-52px" aria-hidden="true" data-art>'
        '<path d="M0 0 H90 C70 10 52 30 40 70 C34 38 16 14 0 0 Z" fill="#E3F7EC"/></svg>')
ticks = (f'<svg width="46" height="26" viewBox="0 0 46 26" fill="none" stroke="#34B268" stroke-width="3.4" stroke-linecap="round" '
         f'stroke-linejoin="round" aria-hidden="true" data-art><path d="M3 14 L10 21 L24 4"/><path d="M17 14 L24 21 L40 4"/></svg>')
bubble = (f'<div style="position:absolute;left:110px;top:330px;width:860px;height:300px;border-radius:120px;background:var(--mint);'
          f'box-shadow:var(--ring-card);z-index:3;padding:54px 80px 0">'
          f'<div style="font-weight:500;font-size:70px;line-height:1.14;letter-spacing:-.03em;color:var(--ink)">{c["msg"]}</div>'
          f'<div style="position:absolute;right:92px;bottom:40px">{ticks}</div>{tail}</div>')
dots = "".join(f'<i style="width:22px;height:22px;border-radius:50%;background:var(--hairline-strong);display:block"></i>' for _ in range(3))
body1 = (f'<div class="grid-paper-fine" style="position:absolute;inset:0;background-color:var(--page)"></div>'
         f'<div style="position:absolute;left:64px;top:56px;right:64px;display:flex;justify-content:space-between;align-items:center">{sk.logo(False, 52)}'
         f'<span class="eyelab" style="font-size:24px">Students and teachers</span></div>'
         + sk.art(sk.blob("good", 210), "left:96px;top:194px;z-index:1")
         + sk.art(sk.mascot("orange", cls="", size=210), "right:96px;top:194px;z-index:1")
         + bubble
         + f'<div style="position:absolute;left:112px;top:676px;display:flex;gap:12px">{dots}</div>'
         + f'<div style="position:absolute;left:110px;top:752px;white-space:nowrap;display:flex;align-items:baseline;gap:22px">{h(c["h1"], 80, 400)}{h(sk.mark(c["h2"], "mint"), 80, 800)}</div>'
         + f'<p style="position:absolute;left:110px;top:866px;width:880px;font-size:32px;line-height:1.4;color:var(--prose)">{c["sub"]}</p>'
         + f'<span class="pill wa" style="position:absolute;left:110px;bottom:64px;height:84px;padding:0 44px;font-size:32px;font-weight:800">{c["cta"]}</span>')

# ───────────────────────── 2. TEASER (feed 1080x1350) ─────────────────────────
W2, H2 = sk.SIZES["feed"]
c = COPY["teaser"]


def frame(inner, dashed=False):
    st = ("border:4px dashed var(--hairline-strong);background:transparent" if dashed else "background:var(--muted)")
    return f'<div style="width:292px;height:292px;border-radius:26px;{st};display:grid;place-items:center;overflow:hidden">{inner}</div>'


m = MATHS
real = (f'<div style="width:100%;height:100%;display:flex;background:{m["tint"]}"><u style="width:22px;background:{m["solid"]}"></u>'
        f'<div style="padding:22px 20px;display:flex;flex-direction:column;gap:6px;flex:1;color:{m["text"]};font-size:22px;line-height:1.2">'
        f'<span style="font-weight:700;letter-spacing:.04em;text-transform:uppercase;font-size:20px">ICSE · 2026</span>'
        f'<span style="font-family:Archivo;font-weight:800;font-size:56px;letter-spacing:-.05em;line-height:1">Maths</span><span>Class X</span>'
        f'<span style="margin-top:auto;font-weight:700">out now</span></div></div>')
q = '<span style="font-family:Archivo;font-weight:800;font-size:110px;color:var(--text3)">?</span>'
strip = (f'<div style="position:absolute;left:70px;top:40px;width:340px;padding:24px;background:var(--card);box-shadow:var(--ring-card);'
         f'transform:rotate(7deg);transform-origin:top left;display:flex;flex-direction:column;gap:22px;border-radius:14px">'
         f'{frame(real)}{frame(q, True)}{frame("", True)}{frame("", True)}</div>')


def tab(x, hgt, text):
    return (f'<div style="position:absolute;left:{x}px;top:-{hgt}px;width:262px;height:{hgt + 30}px;border-radius:40px 40px 0 0;background:var(--card);'
            f'text-align:center;padding-top:{hgt // 2 - 14}px"><span style="display:inline-block;font-weight:700;font-size:26px;line-height:30px;color:var(--ink)">{text}</span></div>')


card = (f'<div style="position:absolute;left:240px;top:620px;width:780px;height:500px;transform:rotate(-9deg);filter:drop-shadow(0 10px 14px rgba(31,31,31,.2))">'
        f'{tab(0, 56, c["t1"])}{tab(250, 88, c["t2"])}{tab(500, 120, c["t3"])}'
        f'<div style="position:absolute;inset:0;background:var(--card);border-radius:0 0 44px 44px;padding:60px 52px">'
        f'{h(c["h"][0], 92, 800)}{h(c["h"][1], 92, 800, "margin-top:8px")}'
        f'<p style="font-weight:600;font-size:34px;line-height:1.3;color:var(--prose);margin-top:30px;max-width:560px">{c["sub"]}</p></div></div>')
body2 = (f'<div class="grid-paper-fine" style="position:absolute;inset:0;background-color:var(--indigo-tint)"></div>'
         + f'<div style="position:absolute;right:64px;top:56px">{sk.logo(False, 52)}</div>' + strip
         + sk.art(sk.mascot("orange", cls="", size=210), "left:690px;top:372px;z-index:0") + card
         + f'<span class="pill darkb" style="position:absolute;right:64px;bottom:56px;height:80px;padding:0 40px;font-size:30px;font-weight:800">{c["url"]}</span>')

# ───────────────────────── 3. FLIP (feed 1080x1350) ─────────────────────────
c = COPY["flip"]
heights = [250, 330, 280, 380, 300, 340]
cov = ""
for k, hh in enumerate(heights):
    pal = sk.palette_from_key(f"flip{k}")
    cov += (f'<div style="width:150px;height:{hh}px;border-radius:0 0 18px 18px;background:{pal["tint"]};box-shadow:var(--ring);display:flex;overflow:hidden">'
            f'<u style="width:16px;background:{pal["solid"]}"></u><div style="padding:16px 12px;flex:1;color:{pal["text"]};font-size:20px;line-height:1.2;font-weight:700;'
            f'letter-spacing:.04em;text-transform:uppercase">{["ICSE","ISC","CBSE","ICSE","ISC","CBSE"][k]}<br><span style="font-family:Archivo;font-weight:800;font-size:38px;'
            f'letter-spacing:-.04em;text-transform:none">Maths</span></div></div>')
# the flip: the whole row is rotated 180 degrees, so covers hang from the top edge and their words read upside down
hang = (f'<div data-bleed data-crop style="position:absolute;left:0;right:0;top:0;height:420px;display:flex;justify-content:center;align-items:flex-end;gap:14px;'
        f'transform:rotate(180deg);padding:0 44px">{cov}</div>')
up = ('<svg width="96" height="110" viewBox="0 0 96 110" aria-hidden="true" data-art><path d="M48 4 L92 52 H64 V106 H32 V52 H4 Z" fill="#4351FF"/></svg>')
hill = ('<div style="position:absolute;left:-160px;right:-160px;bottom:-330px;height:640px;border-radius:50%;background:var(--mint-solid)"></div>')
body3 = (f'<div style="position:absolute;inset:0;background:var(--indigo-tint)"></div>' + hang
         + sk.art(up, "right:90px;top:470px")
         + f'<div style="position:absolute;left:90px;top:520px">{h(c["h1"], 112, 800)}{h(c["h2"], 112, 800, "margin-top:2px;color:var(--indigo-deep)")}</div>'
         + f'<p style="position:absolute;left:90px;top:780px;width:620px;font-size:34px;line-height:1.42;color:var(--prose)">{c["body"]}</p>'
         + hill + sk.art(sk.mascot("orange", cls="", size=250), "left:120px;bottom:130px")
         + sk.art(sk.lobe(170, "#FFC700"), "left:420px;bottom:150px")
         + f'<span class="pill go" data-tap style="position:absolute;right:64px;bottom:64px;height:84px;padding:0 44px;font-size:32px;font-weight:800">{c["url"]}</span>'
         + f'<div style="position:absolute;left:64px;bottom:50px">{sk.logo(False, 56)}</div>')


async def main():
    errs, warns = sk.copy_gate(STRINGS)
    if errs:
        raise sk.ShikshaqError("copy gate:\n  " + "\n  ".join(errs))
    out = []
    async with sk.session() as s:
        for name, body, W, H in (("remake-chat", body1, W1, H1), ("remake-teaser", body2, W2, H2), ("remake-flip", body3, W2, H2)):
            html = sk.doc(body, kind="poster", W=W, H=H, title=name)
            out.append(await s.render(html, f"out/shikshaq/{name}.png", W, H, kind="poster", name=name))
    return out

if __name__ == "__main__":
    res = asyncio.run(main())
    print("CLEAN" if all(r.clean for r in res) else "NOT CLEAN")
