"""DISPATCH no. 05 - this week's internal roundup.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_005.py

Outputs into out/dispatch/no05/:
  wa_poster.png     the ONE WhatsApp promotional poster (1080x1350)
  s00_cover.png     story 1: the contents page
  s01..s04_*.png    one story per item (1080x1920)
  copy.md           the WhatsApp message + the Instagram caption

Sourced from a verbal brief, 2026-10-22. Notes:
  - this is issue 05 (per the user, correcting an initial 04 - the gap
    since no. 03 on 2026-09-30 apparently covers two prior issues, not
    one, even though only no. 01-03 exist in this repo/session's history).
  - the design team's own recruitment (held from no. 03, tagged "will soon
    open" at the time) was not mentioned in this week's brief. Rather than
    invent a status for it, it is simply dropped from this issue - no claim
    is made about it either way. If it's still pending, the next brief
    should say so explicitly.
  - disco diwali's early bird is TIME-SENSITIVE ("going live today at 6") -
    written as going live today. Ship this one on the day it's built, or
    the tense needs revisiting before it goes out.
  - no photo/cover_photo set: none of core.PHOTOS (food/edu/diwali/xmas)
    genuinely matches this week's items.
"""

import asyncio, os, sys, importlib.util

# Repo root from THIS FILE's location - never an absolute path (CLAUDE.md sec. 6).
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE_DIR = os.path.join(os.getcwd(), "engine")
sys.path.insert(0, ENGINE_DIR)


def load(n):
    s = importlib.util.spec_from_file_location(n, os.path.join(ENGINE_DIR, n + ".py"))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


D = load("dispatch")
B = load("build")
prev = load("preview")

OUT = "out/dispatch/no05"


# ============================================================================
# THE BRIEF - this is the whole input surface. Nothing else gets edited.
# ============================================================================
BRIEF = {
    "issue": "05",
    "kicker": "this week at aq",
    "dateline": "22 oct 2026",
    "tagline": "what's / moving",
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all four.",
    "wa_signoff": ("the detail on each one is in the poster. if your team did "
                   "something that isn't here, reply and it goes in no. 06."),
    "ig_signoff": ("the detail on each one is in the stories. not in the volunteer "
                   "group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],

    "items": [
        {
            "dept": "events",
            "chip": "disco diwali",
            "head": "disco diwali early bird live",
            "line": ("disco diwali's early bird tickets go live today at 6pm, so "
                     "if you want in before the price goes up, this is the "
                     "window."),
            "story": ("disco diwali's early bird tickets go live today at 6pm. "
                      "early bird pricing never lasts long and this is usually "
                      "the best rate of the whole sale, so if you were already "
                      "planning on going, tonight is the time to lock it in "
                      "rather than wait and pay more later."),
            "wa": ("disco diwali's early bird tickets go live today at 6pm. grab "
                   "them early, the price only goes up from here."),
        },
        {
            "dept": "labs",
            "chip": "shikshaq",
            "head": "new shikshaq website live",
            "line": ("shikshaq has launched its new website, and the past papers "
                     "collection will soon be accessible to everyone through "
                     "it."),
            "story": ("shikshaq's new website is live, the redesign that has "
                      "been in the works for a few weeks now. the past papers "
                      "collection, which has been going through internal "
                      "review, will soon be accessible to everyone through the "
                      "new site rather than staying inside the ngo aq "
                      "community, so this is the version worth sharing once it "
                      "opens up."),
            "wa": ("shikshaq's new website is live. the past papers collection "
                   "will soon be accessible to everyone through it."),
        },
        {
            "dept": "content",
            "chip": "reels",
            "head": "reels team recruits editors",
            "line": ("the reels team is opening a competition to recruit video "
                     "editors, open to anyone across aq who wants to apply."),
            "story": ("the reels team is putting together a competition to "
                      "recruit video editors, and it is open to anyone across "
                      "aq, not just people already on the team. the format is "
                      "still being finalised, but the idea is to pick editors "
                      "through actual work rather than a plain application, so "
                      "if editing is something you do, this is worth watching "
                      "for."),
            "wa": ("the reels team is opening a competition to recruit video "
                   "editors, open to anyone across aq. more on the format once "
                   "it's finalised."),
        },
        {
            "dept": "content",
            "chip": "linkedin team",
            "head": "linkedin team hiring soon",
            "line": ("the linkedin team will soon open recruitment for its "
                     "research and outreach team, for anyone interested in "
                     "that side of the work."),
            "story": ("the linkedin team is about to open recruitment for its "
                      "research and outreach side, which is a different track "
                      "from the reels and design recruitment running elsewhere "
                      "right now. if digging into research or reaching out to "
                      "people and organisations is more your thing than design "
                      "or editing, this is the one to watch for."),
            "wa": ("the linkedin team will soon open recruitment for its "
                   "research and outreach team. more details when it goes "
                   "live."),
        },
    ],
}


async def main():
    os.makedirs(OUT, exist_ok=True)
    D.validate_brief(BRIEF)          # fails loudly BEFORE a browser is opened

    async with B.session():
        print("\n=== WHATSAPP POSTER ===")
        html, els, gate = await D.poster(BRIEF)
        await B.render(html, "%s/wa_poster.png" % OUT, D.W_FEED, D.H_FEED,
                       elements=els, **gate)

        print("\n=== INSTAGRAM STORIES ===")
        for name, shtml, sels, sgate in await D.stories(BRIEF):
            print("  -- %s" % name)
            await B.render(shtml, "%s/%s.png" % (OUT, name), D.W_STORY, D.H_STORY,
                           elements=sels, **sgate)

    # pixel critique - the headless proxy for the looking gate, never a substitute
    print("\n=== PIXEL CRITIQUE ===")
    for f in ("wa_poster", "s00_cover", "s01_events", "s02_labs"):
        c = prev.critique("%s/%s.png" % (OUT, f))
        print("  %-12s fill=%.2f  %s" % (f, c["fill"], [i[0] for i in c["issues"]]))

    wa = D.whatsapp_text(BRIEF)
    ig = D.ig_caption(BRIEF)
    with open("%s/copy.md" % OUT, "w", encoding="utf-8") as f:
        f.write("# AQ DISPATCH no. %s - copy\n\n## WhatsApp message\n\n```\n%s```\n\n"
                "## Instagram caption\n\n```\n%s```\n" % (BRIEF["issue"], wa, ig))

    print("\n=== WHATSAPP MESSAGE ===\n")
    print(wa)
    print("=== INSTAGRAM CAPTION ===\n")
    print(ig)
    print("written to %s/" % OUT)


asyncio.run(main())
