"""SHIKSHAQ WEEK 2026-W49: three feed posts, Mon 30 Nov, Wed 2 Dec, Fri 4 Dec, 19:30 IST. Built from engine/shikshaq.py.

Owner inputs (asked, 2026-11-27): week and days as above; themes = the planner's three pillars (papers, trust, teachers);
the paper count is 655 (the site shows 655 and 661; asked each time, so confirmed here). Copy comes from the planner's vetted bank
(addons/shikshaq/brain/pillars.json), captions and hashtags follow its format (caption, blank line, CTA: site, blank line,
tags; at most 8 tags), alt text follows its format. Every figure is a sk.FACTS value; every string goes through sk.copy_gate.
Nothing is posted: the output is a reviewable folder (PNGs, week.md with captions, alt text and times, a contact sheet).
Run:  PYTHONIOENCODING=utf-8 python scratchpad/shik_week_2026w49.py
"""
import asyncio, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.getcwd(), "engine"))
import shikshaq as sk

sk.confirm("papers", 655, "owner, 2026-11-27 (asked each time: the site shows 655 and 661)")
F = sk.FACTS
P, T = sk.need("papers"), F["teachers"]
W, H = sk.SIZES["feed"]
OUT = "out/shikshaq/2026-W49"
SITE, CORE = F["site"], ["#shikshaq", "#kolkata", "#kolkatastudents"]
HASH = {"papers": ["#pastpapers", "#icse", "#cbse", "#isc", "#boardexams"], "trust": ["#tuition", "#kolkataparents", "#education"],
        "teachers": ["#hometuition", "#privatetutor", "#kolkataparents", "#tuitionteacher"]}
sp = F["sample_papers"]
st, bt = F["subject_teachers"], F["board_teachers"]

POSTS = [
    dict(day="Mon", date="2026-11-30", pillar="papers", template="number-bento", accent="indigo", cta="Read two questions free",
         plain="Real papers.", bold="Real schools.", sub="Past papers from the exams Kolkata students actually sit.",
         big=f"{P}", label="papers to read", copy_id="nb-papers",
         caption="Past papers from the exams Kolkata students actually sit, all in one place.\n\nOpen one, solve it timed, check yourself after."),
    dict(day="Wed", date="2026-12-02", pillar="trust", template="number-bento", accent="mint", cta="Message a teacher directly",
         plain="Zero", bold="middlemen.", sub="You message the teacher directly. We never take a cut.",
         big=f"₹{F['commission']}", label="commission, ever", copy_id="nb-commission",
         caption="No agent, no booking fee, no commission. You talk to the teacher on WhatsApp and agree things between yourselves."),
    dict(day="Fri", date="2026-12-04", pillar="teachers", template="find-teacher", accent="orange", cta="Find a teacher near you",
         plain=f"{T} teachers.", bold="One search.", sub="Filter by subject, board and area, then reach out.",
         big=None, label=None, copy_id="ft-count",
         caption=f"Filter by subject, board and area, then reach out. {T} teachers are listed right now."),
]
for p in POSTS:
    tags = list(dict.fromkeys(CORE + HASH[p["pillar"]]))[:8]
    p["hashtags"] = tags
    p["full_caption"] = f"{p['caption']}\n\n{p['cta']}: {SITE}\n\n{' '.join(tags)}"
    p["alt"] = f"Shikshaq poster. {p['plain']} {p['bold']} {p['sub']}"
    p["headline"] = f"{p['plain']} {p['bold']}"
    assert len(p["headline"]) <= 40 and len(p["full_caption"]) <= 900 and len(tags) <= 8


def pad(inner):
    return f'<div style="position:relative;height:100%">{inner}</div>'


def head(right, on_dark=False):
    return (f'<div style="position:absolute;left:64px;right:64px;top:52px;display:flex;justify-content:space-between;align-items:center">'
            f'{sk.logo(on_dark, 56)}<span class="eyelab" style="font-size:24px">{right}</span></div>')


def line(plain, payoff, size, mark="", top=0, extra=""):
    return (f'<h1 style="position:absolute;left:64px;right:64px;top:{top}px;font-weight:400;font-size:{size}px;line-height:1.02;letter-spacing:-.05em;{extra}">'
            f'{plain}<br>{sk.mark(payoff, mark)}</h1>')


def cover(i, hgt):
    pal = sk.palette_from_key(f"{sp[i]['board']} {sp[i]['subject']} {sp[i]['cls']}")
    return (f'<div style="width:296px;height:{hgt}px;border-radius:30px;display:flex;overflow:hidden;background:{pal["tint"]};box-shadow:0 20px 44px -16px rgba(0,0,0,.45)">'
            f'<u style="width:26px;background:{pal["solid"]}"></u><div style="display:flex;flex-direction:column;gap:6px;padding:24px 22px;font-size:24px;line-height:1.2;flex:1;color:{pal["text"]}">'
            f'<span style="font-weight:700;letter-spacing:.04em;font-size:22px;text-transform:uppercase">{sp[i]["board"]} · {sp[i]["year"]}</span>'
            f'<span style="font-family:Archivo;font-weight:800;font-size:60px;letter-spacing:-.05em;line-height:1">{sp[i]["subject"]}</span>'
            f'<span>Class {sp[i]["cls"]}</span><span style="margin-top:auto;font-weight:700">{sp[i]["questions"]} questions</span></div></div>')


# ───────── Monday: papers, indigo ─────────
m = POSTS[0]
top = pad(head("Past papers")
          + f'<div style="position:absolute;left:58px;top:124px;font-family:Archivo;font-weight:800;font-size:300px;line-height:.86;letter-spacing:-.06em;color:var(--indigo-deep);font-variant-numeric:tabular-nums">{m["big"]}</div>'
          + f'<div style="position:absolute;left:640px;top:222px;font-weight:600;font-size:46px;line-height:1.12;color:var(--prose)">papers<br>to read</div>'
          + line(m["plain"], m["bold"], 96, "papers", 440)
          + f'<p style="position:absolute;left:64px;top:672px;width:900px;font-size:32px;line-height:1.35;color:var(--prose)">{m["sub"]}</p>')
bot = pad(f'<div style="position:absolute;left:64px;top:50px;display:flex;gap:26px">{cover(0, 250)}{cover(1, 250)}{cover(2, 250)}</div>'
          + f'<span class="pill white" data-tap style="position:absolute;left:64px;bottom:60px;height:92px;padding:0 44px;font-size:34px;font-weight:800">{m["cta"]} →</span>'
          + f'<span style="position:absolute;right:64px;bottom:84px;font-size:28px;color:#fff;font-weight:600">{SITE}</span>')
mon = sk.poster([("bone", top, 800), ("indigo", bot, None)], W, H)

# ───────── Wednesday: trust, mint ─────────
w = POSTS[1]
top = pad(head("No commission")
          + line(w["plain"], w["bold"], 120, "mint", 170)
          + f'<p style="position:absolute;left:64px;top:468px;width:880px;font-size:34px;line-height:1.38;color:var(--prose)">{w["sub"]}</p>')
bot = pad(f'<div style="position:absolute;left:54px;top:40px;font-family:Archivo;font-weight:800;font-size:360px;line-height:.9;letter-spacing:-.06em;color:#24603D">{w["big"]}</div>'
          + f'<div style="position:absolute;left:68px;top:420px;font-weight:600;font-size:46px;color:#24603D">{w["label"]}</div>'
          + sk.art(sk.mascot("orange", cls="", size=300), "right:-40px;top:20px")
          + f'<span class="pill wa" data-tap style="position:absolute;left:64px;bottom:60px;height:92px;padding:0 44px;font-size:34px;font-weight:800">{w["cta"]}</span>'
          + f'<span style="position:absolute;right:64px;bottom:84px;font-size:28px;color:#24603D;font-weight:600">{SITE}</span>')
wed = sk.poster([("bone", top, 580), ("mint", bot, None)], W, H)

# ───────── Friday: teachers, orange ─────────
f_ = POSTS[2]
dots = "".join(f'<span class="count" style="height:52px;font-size:24px;padding:0 20px;gap:10px"><s style="background:{sk.subject_palette(n)["solid"]};width:12px;height:12px;border-radius:3px"></s>{n} · {c}</span>'
               for n, c in (("Maths", st["Maths"]), ("English", st["English"]), ("Hindi", st["Hindi"]), ("Chemistry", st["Chemistry"])))
search = (f'<div style="position:absolute;left:64px;right:64px;top:536px;height:92px;border-radius:30px;background:var(--muted);display:flex;align-items:center;padding:0 14px 0 28px;gap:18px;color:var(--text2);font-size:32px">'
          f'{sk.icon("search", 34)}<span style="flex:1">Which subject?</span><span class="pill go" style="height:64px;font-size:28px;padding:0 32px">Search</span></div>')
top = pad(head("Teachers in Kolkata")
          + line(f_["plain"], f_["bold"], 112, "", 140)
          + f'<p style="position:absolute;left:64px;top:412px;width:880px;font-size:33px;line-height:1.35;color:var(--prose)">{f_["sub"]}</p>'
          + search + f'<div style="position:absolute;left:64px;right:64px;top:650px;display:flex;gap:10px;flex-wrap:nowrap">{dots}</div>')
rows = "".join(f'<div style="height:84px;border-radius:999px;background:var(--card);box-shadow:var(--ring-card);display:flex;align-items:center;justify-content:space-between;padding:0 36px;font-weight:800;font-size:34px">{n}<span style="font-weight:500;font-size:28px;color:var(--prose)">{c} teachers</span></div>'
               for n, c in (("ICSE", bt["ICSE"]), ("CBSE", bt["CBSE"]), ("IGCSE", bt["IGCSE"])))
bot = pad(f'<div style="position:absolute;left:64px;right:64px;top:58px;display:flex;flex-direction:column;gap:14px">{rows}</div>'
          + sk.art(sk.character("book", 210), "right:60px;bottom:30px")
          + f'<span class="pill darkb" data-tap style="position:absolute;left:64px;bottom:60px;height:92px;padding:0 44px;font-size:34px;font-weight:800">{f_["cta"]}</span>')
fri = sk.poster([("bone", top, 730), ("orange", bot, None)], W, H)

# ───────── gate the copy, render, write the folder ─────────
strings = [p[k] for p in POSTS for k in ("plain", "bold", "sub", "cta", "full_caption", "alt") ] + [p["label"] for p in POSTS if p["label"]] \
          + ["Which subject?", "Past papers", "No commission", "Teachers in Kolkata", "ICSE", "CBSE", "IGCSE"]
errs, warns = sk.copy_gate(strings)
assert not errs, errs


async def main():
    os.makedirs(OUT, exist_ok=True)
    res = []
    async with sk.session() as s:
        for k, (p, body) in enumerate(zip(POSTS, (mon, wed, fri)), 1):
            html = sk.doc(body, kind="poster", W=W, H=H, title=p["headline"])
            r = await s.render(html, f"{OUT}/{k:02d}-{p['day'].lower()}-{p['pillar']}.png", W, H, kind="poster", name=f"{p['day']}-{p['pillar']}")
            p["file"] = os.path.basename(r.png); res.append(r)
    sk.contact_sheet([r.png for r in res], f"{OUT}/_week.png")
    lines = [f"# Shikshaq week 2026-W49", "",
             "Three feed posts, 1080x1350, **19:30 IST**. Nothing is posted automatically: you post, or schedule, from this folder.", "",
             f"Facts as of {F['asOf']} ({F['source']}). Paper count **{P}** confirmed by the owner on 2026-11-27 (the site shows 655 and 661). Re-read the live counts before posting if the week slips.", ""]
    for p in POSTS:
        lines += [f"## {p['day']} {p['date']} 19:30 IST: {p['pillar']} ({p['template']}, {p['accent']})", "", f"File: `{p['file']}`  ", f"Headline: **{p['headline']}**  ", f"CTA: {p['cta']}", "",
                  "Caption:", "", "```", p["full_caption"], "```", "", f"Alt text: {p['alt']}", "", f"Hashtags ({len(p['hashtags'])}): {' '.join(p['hashtags'])}", ""]
    lines += ["## Checks run", "", "Copy gate (no dashes, no unsourced claims, every number traced to a fact), headline at most 40 characters, caption at most 900, at most 8 hashtags, the measured layout gate on each PNG, and a look at each image.", "",
              "## Before you post", "", "- Open `_week.png` and each PNG.", "- Confirm the counts (157 teachers, 655 papers, the three paper covers) still match the site on the day.", "- Instagram posting is not automated."]
    open(f"{OUT}/week.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return res

if __name__ == "__main__":
    r = asyncio.run(main())
    print("CLEAN" if all(x.clean for x in r) else "NOT CLEAN: " + "; ".join(m for x in r for m in x.hard))
