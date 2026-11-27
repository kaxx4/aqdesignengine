"""CAROUSEL: "What if your next exam felt easy?" remade in the Shikshaq language (5 slides, 1080x1350).

Source: a five-slide carousel supplied by the owner in a different (bubbly lettering, sticker-character) style.
The COPY and FLOW are kept; the look is rebuilt from engine/shikshaq.py: bone ground, 64px-rounded panels that differ by
fill, Archivo mixed-weight headlines (400 setup, 800 payoff on a marker highlight), the site's mascots (orange eyes, the
burst, the four-lobe, the blob moods), tilted stickers, a long swipe arrow, mode and subject colour used as DATA:

  slide 1 papers mode (indigo)     slide 2 students = papers mode (lavender + dark)
  slide 3 parents = teachers mode (peach + orange)
  slide 4 a MATHS announcement, so the maths palette is the subject colour (marker, status chip, row icon)
  slide 5 trust ("Free. No hidden fees.") on mint, closing on the dark slab

Adaptations from the source, recorded as the precedence ladder asks (CLAUDE.md section 2, Shikshaq version):
  * "100% free!" became "Free to read": the site's own copy rule bans "100%" (copy_gate: unprovable superlative)
  * the pencil, star, chai cup and warning triangle are not Shikshaq characters; the site's own vocabulary stands in
    (orange mascot, burst, blob, lobe). A new character is a design decision for the owner, not for this build
  * hand-lettered equations and ticks became solid chips, because decoration is solid, never a faint wash

No number appears in the copy, so the paper-count question (asked each time) does not arise.
Run:  PYTHONIOENCODING=utf-8 python scratchpad/shik_carousel_exam_practice.py
"""
import asyncio, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

W, H = sk.SIZES["feed"]
N = 5
MATHS = sk.subject_palette("Maths")           # tint / solid / text / meta from the site's generator

COPY = {
    1: dict(h=["What if your next exam felt", "easy?"], sub="Not luck. Just the right practice.", chip="practice > panic"),
    2: dict(eb="for students", h=["Walk into every exam thoroughly", "prepared."], chip="exam mode: on"),
    3: dict(eb="for parents", h=["Know exactly what your child is", "preparing for."], chip="no more guesswork"),
    4: dict(eb="sneak peek", h=["Maths past papers,", "out now."],
            body="Shared voluntarily by students from their own schools. More subjects are on the way, and we're working hard to bring them to you.",
            r1="Maths past papers", s1="out now!", r2="Other subjects", s2="coming soon", chip="Maths papers ahead!"),
    5: dict(h1="Free.", h2="No hidden fees.", body="A learning hub built by students, for students. Maths past papers are out now.",
            sticker="Free to read", badge=("Maths", "past papers", "out now!"), foot="More subjects coming soon!", url="shikshaq.in"),
}
strings = []
for c in COPY.values():
    for v in c.values():
        strings += list(v) if isinstance(v, (list, tuple)) else [v]


def pad(inner, p="56px 64px"):
    return f'<div style="position:relative;height:100%;padding:{p}">{inner}</div>'


def h1(plain, payoff, size=118, mark="papers", top=0):
    return (f'<h1 style="font-weight:400;font-size:{size}px;line-height:1.02;letter-spacing:-.05em;margin-top:{top}px">'
            f'{plain} {sk.mark(payoff, mark)}</h1>')


def eb(text, color):
    return f'<p style="font-family:Geist;font-weight:600;font-size:32px;color:{color};margin-top:150px">{text}</p>'


# ---------- slide 1 ----------------------------------------------------------------------------
c = COPY[1]
top1 = pad(sk.slide_header(1, N)
           + f'<h1 style="font-weight:400;font-size:124px;line-height:1.02;letter-spacing:-.05em;margin-top:200px;max-width:900px">'
             f'{c["h"][0]} {sk.mark(c["h"][1], "papers")}</h1>'
           + f'<p style="font-size:38px;color:var(--prose);margin-top:44px">{c["sub"]}</p>'
           + sk.place(sk.pchip("?!", -8, "dark", 44), "right:190px;top:136px")
           + sk.place(sk.pchip("?!", 7, "dark", 44), "right:64px;top:150px"))
bot1 = pad(sk.place(sk.pchip(c["chip"], -4, "bone", 48), "left:64px;top:110px")
           + sk.art(sk.mascot("orange", cls="", size=340), "right:-30px;bottom:-70px")
           + sk.art(sk.swipe_arrow("#fff"), "left:64px;bottom:56px"), "0")
s1 = sk.poster([("bone", top1, 800), ("indigo", bot1, None)], W, H)

# ---------- slide 2 ----------------------------------------------------------------------------
c = COPY[2]
top2 = pad(sk.slide_header(2, N)
           + eb(c["eb"], "var(--indigo-deep)").replace("margin-top:150px", "margin-top:96px")
           + f'<h1 style="font-weight:400;font-size:118px;line-height:1.02;letter-spacing:-.05em;margin-top:26px;max-width:780px">'
             f'{c["h"][0]} {sk.mark(c["h"][1], "papers")}</h1>'
           + sk.place(sk.pchip("a² + b² = c²", -6, "bone", 34), "right:64px;top:190px")
           + sk.place(sk.pchip("π", 5, "bone", 34), "right:300px;top:300px")
           + sk.place(sk.pchip("√x", -4, "bone", 34), "right:64px;top:300px")
           + sk.place(sk.pchip("x = ?", 6, "bone", 34), "right:64px;top:410px"))
bot2 = pad(sk.place(sk.pchip(c["chip"], 4, "bone", 48), "right:64px;top:90px")
           + sk.art(sk.sun(250, "#FFC700"), "left:64px;bottom:40px")
           + sk.art(sk.swipe_arrow("#F9F5F1"), "right:64px;bottom:56px"), "0")
s2 = sk.poster([("lav", top2, 860), ("dark", bot2, None)], W, H)

# ---------- slide 3 ----------------------------------------------------------------------------
c = COPY[3]
top3 = pad(sk.slide_header(3, N)
           + eb(c["eb"], "var(--orange-deep)").replace("margin-top:150px", "margin-top:96px")
           + f'<h1 style="font-weight:400;font-size:118px;line-height:1.02;letter-spacing:-.05em;margin-top:26px;max-width:800px">'
             f'{c["h"][0]} {sk.mark(c["h"][1], "")}</h1>'
           + sk.art('<div style="width:96px;height:96px;border-radius:50%;background:var(--mint-solid);display:grid;place-items:center">'
                    + sk.icon("shield", 52, "#1F1F1F", 2.6) + '</div>', "right:150px;top:200px")
           + sk.place(sk.pchip("A+", 6, "dark", 44), "right:64px;top:330px"))
bot3 = pad(sk.place(sk.pchip(c["chip"], -4, "bone", 48), "left:64px;top:90px")
           + sk.art(sk.blob("good", 270), "right:70px;bottom:50px")
           + sk.art(sk.swipe_arrow("#1F1F1F"), "left:64px;bottom:56px"), "0")
s3 = sk.poster([("peach", top3, 860), ("orange", bot3, None)], W, H)

# ---------- slide 4 (a MATHS announcement: the maths palette is the subject colour) --------------------
c = COPY[4]
row1 = (f'<div class="cardrow"><span style="display:flex;align-items:center;gap:22px">'
        f'<span style="width:54px;height:54px;border-radius:50%;background:{MATHS["solid"]};display:grid;place-items:center">{sk.icon("shield", 30, MATHS["badge"], 2.6)}</span>'
        f'<span style="font-family:Archivo;font-weight:800;font-size:46px;letter-spacing:-.04em">{c["r1"]}</span></span>'
        f'{sk.pchip(c["s1"], 0, "bone", 30, f"background:{MATHS["tint"]};color:{MATHS["text"]};box-shadow:none")}</div>')
row2 = (f'<div class="cardrow"><span style="display:flex;align-items:center;gap:22px">'
        f'<span style="width:54px;height:54px;display:grid;place-items:center;color:var(--text2)">{sk.icon("cap", 34, "currentColor", 2.4)}</span>'
        f'<span style="font-weight:600;font-size:40px;color:var(--prose)">{c["r2"]}</span></span>'
        f'{sk.pchip(c["s2"], 0, "dash", 30, "color:var(--text2)")}</div>')
card = (f'<div style="margin-top:34px;background:var(--muted);border-radius:40px;box-shadow:var(--ring-card);padding:34px 40px">'
        f'{row1}<div style="height:2px;background:var(--hairline-strong);margin:24px 0"></div>{row2}</div>')
top4 = pad(sk.slide_header(4, N)
           + eb(c["eb"], "var(--indigo-deep)").replace("margin-top:150px", "margin-top:50px")
           + f'<h1 style="font-weight:400;font-size:116px;line-height:1.02;letter-spacing:-.05em;margin-top:18px">'
             f'{c["h"][0]}<br>{sk.mark(c["h"][1], "")}</h1>'.replace('class="mark "', f'class="mark" style="background:{MATHS["solid"]};color:var(--ink)"')
           + f'<p style="font-size:33px;line-height:1.45;color:var(--prose);margin-top:30px;max-width:880px">{c["body"]}</p>' + card, "50px 64px")
bot4 = pad(sk.place(sk.pchip(c["chip"], -5, "dark", 40), "left:64px;top:96px")
           + sk.art(sk.lobe(230, "#FF8000"), "right:300px;bottom:-40px")
           + sk.art(sk.swipe_arrow("#fff"), "right:64px;bottom:56px"), "0")
s4 = sk.poster([("bone", top4, 1000), ("indigo", bot4, None)], W, H)

# ---------- slide 5 ----------------------------------------------------------------------------
c = COPY[5]
badge = (f'<div style="position:absolute;right:64px;bottom:60px;width:250px;height:250px;border-radius:50%;background:var(--card);'
         f'box-shadow:var(--ring-card);transform:rotate(-8deg);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">'
         f'<span style="font-family:Archivo;font-weight:800;font-size:44px;letter-spacing:-.04em;line-height:1">{c["badge"][0]}</span>'
         f'<span style="font-size:28px;color:var(--prose);margin-top:16px">{c["badge"][1]}</span>'
         f'<span style="font-family:Archivo;font-weight:800;font-size:30px;color:{MATHS["text"]};margin-top:14px">{c["badge"][2]}</span></div>')
top5 = pad(sk.slide_header(5, N)
           + f'<h1 style="font-weight:800;font-size:230px;line-height:.9;letter-spacing:-.06em;margin-top:120px">{c["h1"]}</h1>'
           + f'<h2 style="font-weight:400;font-size:104px;line-height:1.05;letter-spacing:-.05em;margin-top:34px">{sk.mark(c["h2"], "mint")}</h2>'
           + f'<p style="font-size:35px;line-height:1.45;color:var(--prose);margin-top:50px;max-width:560px">{c["body"]}</p>'
           + sk.place(sk.pchip(c["sticker"], 6, "dark", 40), "right:64px;top:150px") + badge)
bot5 = pad(f'<p style="font-family:Archivo;font-weight:800;font-size:60px;letter-spacing:-.045em;line-height:1.05;color:#fff;max-width:520px">{c["foot"]}</p>'
           f'<span class="pill go" data-tap style="position:absolute;right:64px;top:60px;height:96px;padding:0 48px;font-size:38px;font-weight:800">{c["url"]}</span>', "60px 64px")
s5 = sk.poster([("mint", top5, 900), ("dark", bot5, None)], W, H)


async def main():
    return await sk.render_carousel([s1, s2, s3, s4, s5], "out/shikshaq", "exam-practice", W, H, copy=strings)

if __name__ == "__main__":
    res = asyncio.run(main())
    print("CLEAN" if all(r.clean for r in res) else "NOT CLEAN: " + "; ".join(m for r in res for m in r.hard))
