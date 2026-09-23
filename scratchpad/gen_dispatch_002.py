"""DISPATCH no. 02 - this week's internal roundup.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_002.py

Outputs into out/dispatch/no02/:
  wa_poster.png     the ONE WhatsApp promotional poster (1080x1350)
  s00_cover.png     story 1: the contents page
  s01..s04_*.png    one story per item (1080x1920)
  copy.md           the WhatsApp message + the Instagram caption

Sourced from a verbal brief, 2026-09-23, revised same day per follow-up
direction. Open items, handled by not overstating them (VOICE.md sec. 1.5 -
a claim comes from the brief or it is omitted):
  - disco diwali does NOT get its own item/section - it is folded into the
    terrathon item as a one-line, un-emphasized tease ("maybe a ... giveaway
    or two"), per the follow-up brief.
  - shikshaq carries two facts: the past papers collection is finally under
    internal review, AND the shikshaq website itself is undergoing a full
    redesign. These are two different things under one department, not to
    be confused with the "ops" item's new NGO-wide internal website.
  - the digital magazine item is written with more weight: it is the team's
    first-ever issue, and the copy names the real effort behind it (meet
    after meet, every detail) rather than a flat announcement.
  - no real AQ photo in core.PHOTOS (food/edu/diwali/xmas) is a true match for
    any of this week's items, so no photo/cover_photo is set. The existing
    "diwali" photo is from a past fundraiser, not this year's Disco Diwali
    event, and using it here would misattribute it.
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

OUT = "out/dispatch/no02"


# ============================================================================
# THE BRIEF - this is the whole input surface. Nothing else gets edited.
# ============================================================================
BRIEF = {
    "issue": "02",
    "kicker": "this week at aq",
    "dateline": "23 sep 2026",
    "tagline": "what's / moving",
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all four.",
    "wa_signoff": ("the detail on each one is in the poster. if your team did "
                   "something that isn't here, reply and it goes in no. 03."),
    "ig_signoff": ("the detail on each one is in the stories. not in the volunteer "
                   "group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],

    "items": [
        {
            "dept": "events",
            "chip": "terrathon",
            "head": "terrathon is oct 2-4",
            "line": ("terrathon runs october 2 to 4 this year, with a mini carnival "
                     "alongside it, and maybe a disco diwali ticket giveaway or two "
                     "along the way."),
            "story": ("terrathon is confirmed for october 2, 3 and 4, with a mini "
                      "carnival running alongside it this year for the first time. the "
                      "events team is deep into planning both, and more on "
                      "registration, venue and the carnival lineup follows soon. also, "
                      "quietly: there may be a disco diwali ticket giveaway or two "
                      "along the way, so it is worth keeping half an eye on this "
                      "space."),
            "wa": ("terrathon is confirmed for october 2, 3 and 4, and a mini carnival "
                   "runs alongside it this year. more on registration and the carnival "
                   "lineup coming soon, and yes, disco diwali tickets might make an "
                   "appearance too."),
        },
        {
            "dept": "labs",
            "chip": "shikshaq",
            "head": "past papers under review",
            "line": ("shikshaq's long-awaited past papers collection is finally under "
                     "internal review, and the shikshaq website itself is now going "
                     "through a full redesign."),
            "story": ("shikshaq's past papers collection, long asked for, is finally "
                      "moving into internal review inside the ngo aq community before "
                      "it goes out more widely. alongside that, the shikshaq website "
                      "itself is going through a full redesign, so expect a different "
                      "look and feel once both land. no firm date yet, but both are "
                      "properly underway."),
            "wa": ("shikshaq's past papers collection is finally under internal "
                   "review, and the shikshaq website itself is going through a full "
                   "redesign. both are properly underway."),
        },
        {
            "dept": "ops",
            "chip": "new website",
            "head": "hr trains on the site",
            "line": ("hr is running training on the new ngo website before the wider "
                     "rollout, so the switch to using it is smooth for everyone."),
            "story": ("hr is currently training on the new ngo website ahead of the "
                      "wider rollout. the idea is to work out the kinks and get "
                      "comfortable with it before everyone else gets an account, so the "
                      "eventual switch is smooth rather than chaotic. once that "
                      "training wraps, accounts open up more broadly."),
            "wa": ("hr is running training on the new ngo website before the wider "
                   "rollout, so the switch to using it is smooth for everyone once "
                   "accounts open up."),
        },
        {
            "dept": "content",
            "chip": "digital magazine",
            "head": "digital magazine's first issue",
            "line": ("aq's first-ever digital magazine issue is almost here, built "
                     "through meet after meet of planning, execution and getting "
                     "every single detail right."),
            "story": ("aq's first-ever digital magazine issue is almost ready, and it "
                      "has taken meet after meet to get here: planning the sections, "
                      "chasing down every blog and design, and going over every "
                      "detail more than once. the team pulling this together has put "
                      "in real hours for it, and it shows in how far along it "
                      "already is."),
            "wa": ("aq's first-ever digital magazine issue is almost here, built "
                   "through meet after meet of planning, execution and getting every "
                   "detail right. the team has put in real work for this one."),
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
