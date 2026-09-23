"""DISPATCH no. 02 - this week's internal roundup.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_002.py

Outputs into out/dispatch/no02/:
  wa_poster.png     the ONE WhatsApp promotional poster (1080x1350)
  s00_cover.png     story 1: the contents page
  s01..s05_*.png    one story per item (1080x1920)
  copy.md           the WhatsApp message + the Instagram caption

Sourced from a verbal brief, 2026-09-23. Two open items, both handled by not
overstating them (VOICE.md sec. 1.5 - a claim comes from the brief or it is
omitted):
  - disco diwali is explicitly a TEASE, not a confirmed return - worded as
    such rather than stated as fact.
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
    "story_cta": "swipe for all five.",
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
            "line": ("terrathon runs october 2 to 4 this year, and a mini carnival runs "
                     "alongside it. the events team is deep into planning now."),
            "story": ("terrathon is confirmed for october 2, 3 and 4, with a mini "
                      "carnival running alongside it this year for the first time. the "
                      "events team is deep into planning both, and more details on "
                      "registration, venue and the carnival lineup will follow in the "
                      "coming weeks. if your team is helping put either one together, "
                      "that work is already underway."),
            "wa": ("terrathon is confirmed for october 2, 3 and 4, and a mini carnival "
                   "runs alongside it this year. the events team is deep into planning, "
                   "more details on registration and the carnival lineup coming soon."),
        },
        {
            "dept": "events",
            "chip": "disco diwali",
            "head": "disco diwali teaser drops",
            "line": ("disco diwali is being teased for a return this year, with ticket "
                     "giveaways in the works. watch this space for more."),
            "story": ("disco diwali looks like it's coming back this year, and the "
                      "events team is hinting at ticket giveaways before anything is "
                      "official. nothing is confirmed yet, so treat this as a tease "
                      "rather than an announcement, but if giveaways do happen they "
                      "will run through this channel first, so it is worth keeping an "
                      "eye out."),
            "wa": ("disco diwali is being teased for a return this year, and the events "
                   "team is hinting at ticket giveaways before anything is official. "
                   "nothing confirmed yet - watch this space."),
        },
        {
            "dept": "labs",
            "chip": "shikshaq",
            "head": "past papers move to review",
            "line": ("shikshaq's past papers collection is moving into internal "
                     "checking within the ngo aq community, the step before it reaches "
                     "a wider audience."),
            "story": ("shikshaq's past papers collection is entering internal checking, "
                      "run inside the ngo aq community before it goes out more widely. "
                      "the review is meant to catch errors and gaps before students "
                      "start relying on the papers, so it is a deliberate step rather "
                      "than a delay. once it clears, the collection opens up beyond the "
                      "community."),
            "wa": ("shikshaq's past papers collection is moving into internal checking "
                   "within the ngo aq community, the step before it goes out more "
                   "widely."),
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
            "chip": "magazine",
            "head": "magazine's first issue coming",
            "line": ("aq's new digital magazine is putting together its first edition, "
                     "with new blogs and designs from across the community lined up "
                     "for it."),
            "story": ("aq's new digital magazine is assembling its first edition, and "
                      "it is pulling in new blogs and designs from across the "
                      "community rather than just the usual small team. if you have "
                      "something written, drawn or designed that you want in it, this "
                      "is the edition to get it into, before the first issue goes "
                      "out."),
            "wa": ("aq's new digital magazine is putting together its first edition, "
                   "with new blogs and designs from across the community lined up for "
                   "it."),
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
    for f in ("wa_poster", "s00_cover", "s01_events", "s03_labs"):
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
