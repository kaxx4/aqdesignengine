"""DISPATCH no. 03 - this week's internal roundup.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_003.py

Outputs into out/dispatch/no03/:
  wa_poster.png     the ONE WhatsApp promotional poster (1080x1350)
  s00_cover.png     story 1: the contents page
  s01..s05_*.png    one story per item (1080x1920)
  copy.md           the WhatsApp message + the Instagram caption

Sourced from a verbal brief, 2026-09-30, revised same day per follow-up
direction. Notes:
  - the marketing brief had TWO recruitment threads: the design team's
    upcoming recruitment (with a competition) and a currently-open HOD
    recruitment. 7 topics came in against a 6-item cap (R2). The design
    team's recruitment - explicitly "will soon open", i.e. not live yet -
    is held for no. 04 when it actually opens, and gets a one-line forward
    mention inside the combined item instead (same technique as no. 02's
    disco diwali tease inside terrathon).
  - PER FOLLOW-UP: the digital magazine and the HOD recruitment (both
    dept=content) now share ONE item/page instead of two, and the freed
    slot goes to hr's ai-upskilling item, which an earlier pass of this
    issue had held back. Net item count is still 5 - the number already
    proven to fit the poster's card-fit solver (dispatch._plan_cards)
    comfortably. A true 6-item brief does NOT fit: even at the absolute
    text floor it only cleared the fixed card region by ~3px, too fragile
    to ship - so combining two items onto one page, rather than trying to
    squeeze 6 separate ones, is the way to cover six topics this issue.
  - "crftd" has no natural home in the 5-department vocabulary
    (events/welfare/labs/ops/content). The user had no preference; filed
    under ops (website launch, logistics/automation, internships read as
    operations work) - a genuine judgment call, flagged here for the record
    rather than silently guessed away.
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

OUT = "out/dispatch/no03"


# ============================================================================
# THE BRIEF - this is the whole input surface. Nothing else gets edited.
# ============================================================================
BRIEF = {
    "issue": "03",
    "kicker": "this week at aq",
    "dateline": "30 sep 2026",
    "tagline": "what's / moving",
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all five.",
    "wa_signoff": ("the detail on each one is in the poster. if your team did "
                   "something that isn't here, reply and it goes in no. 04."),
    "ig_signoff": ("the detail on each one is in the stories. not in the volunteer "
                   "group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],

    "items": [
        {
            "dept": "events",
            "chip": "terrathon",
            "head": "terrathon is only days away",
            "line": ("terrathon is only days away, with a mini carnival and fete "
                     "alongside it, plus disco diwali passes on sale."),
            "story": ("terrathon is only a few days away now, and there is a full "
                      "mini carnival and fete running alongside it this time, "
                      "packed with fun activities. disco diwali passes also go on "
                      "sale during the same window, so if you have been waiting to "
                      "grab one, this is when to do it."),
            "wa": ("terrathon is only a few days away, with a mini carnival and "
                   "fete running alongside it and plenty of fun activities planned. "
                   "disco diwali passes go on sale during the same window."),
        },
        {
            "dept": "content",
            "chip": "magazine & hod",
            "head": "1st edition out, hod hiring",
            "line": ("the digital magazine's first edition is out now, and "
                     "marketing's hod recruitment is open too, with the design "
                     "team's own recruitment following soon."),
            "story": ("the digital magazine's first edition is finally out, the "
                      "payoff for meet after meet of planning and chasing every "
                      "detail. right alongside that, marketing's hod recruitment "
                      "is open now, so if you've been eyeing that role, this is "
                      "your window. the design team's own recruitment, with a fun "
                      "competition built in, follows soon after."),
            "wa": ("the digital magazine's first edition is out now, and "
                   "marketing's hod recruitment is open too. the design team's "
                   "own recruitment, with a fun competition, follows soon."),
        },
        {
            "dept": "ops",
            "chip": "hr",
            "head": "hr picks up ai skills",
            "line": ("hr has started experimenting with ai, building small games "
                     "on claude and testing a personal profile website."),
            "story": ("hr has started experimenting with ai as part of learning "
                      "the tools properly, rather than just reading about them. "
                      "that has meant building small games on claude and even "
                      "trying to put together a personal profile website with it, "
                      "mostly to see what is actually possible before using any of "
                      "it for real work."),
            "wa": ("hr has started experimenting with ai, building small games on "
                   "claude and testing out a personal profile website, mostly to "
                   "learn what the tools can actually do."),
        },
        {
            "dept": "labs",
            "chip": "shikshaq",
            "head": "past papers train ai workflow",
            "line": ("shikshaq is training on past years' question papers, and "
                     "building an ai workflow to turn them into machine-readable "
                     "json."),
            "story": ("shikshaq is training on past years' question papers, and "
                      "alongside that, building an ai-orchestrator workflow that "
                      "converts question papers into machine-readable json. the "
                      "json format is the groundwork, it is what will eventually "
                      "let algorithms run on the papers directly, rather than "
                      "someone doing that work by hand. still early, but properly "
                      "underway."),
            "wa": ("shikshaq is training on past years' question papers and "
                   "building an ai-orchestrator workflow that converts them into "
                   "machine-readable json, laying the groundwork for running "
                   "algorithms on them later."),
        },
        {
            "dept": "ops",
            "chip": "crftd",
            "head": "crftd website launch is near",
            "line": ("crftd's website, for customising and ordering t-shirts, is "
                     "in the works, and internships open very soon."),
            "story": ("crftd's website is in the works, and once it's live, "
                      "people will be able to customise and order their own "
                      "t-shirts directly through it. behind the scenes, the team "
                      "is also experimenting with 24/7 ai bots to help with "
                      "marketing, logistics and automation, and internships are "
                      "opening up very soon for anyone who wants in."),
            "wa": ("crftd's website, where people can customise and order their "
                   "own t-shirts, is in the works. behind the scenes they are "
                   "experimenting with 24/7 ai bots for marketing, logistics and "
                   "automation, and internships open soon."),
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
    for f in ("wa_poster", "s00_cover", "s01_events", "s04_labs"):
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
