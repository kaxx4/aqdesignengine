"""DISPATCH no. 01 - the worked example of the internal-roundup series.

This file is the ONLY thing the internal community manager touches each week:
a BRIEF, and one command. Everything about how it looks lives in
engine/dispatch.py, so a bad-looking issue is an engine bug (CLAUDE.md sec. 1),
not something to hand-fix here.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_001.py

Outputs into out/dispatch/no01/:
  wa_poster.png     the ONE WhatsApp promotional poster (1080x1350)
  s00_cover.png     story 1: the contents page
  s01..s05_*.png    one story per item (1080x1920)
  copy.md           the WhatsApp message + the Instagram caption

THE FIELDS, per item:
  dept    one of events | welfare | labs | ops | content. Picks the colour BY
          RULE (core.accent_for). Not a free choice.
  chip    <= 3 words. The little label over the headline.
  head    <= 5 words. Shown UPPERCASE on the poster and the story.
  line    <= 28 words. The poster's line. Narrative, not a fragment: say what
          actually happened, not a mood.
  story   <= 70 words, OPTIONAL. The long version, used only on the story
          slide, which is the one surface with real room to explain.
  wa      <= 70 words, OPTIONAL. The WhatsApp message version. Falls back to
          `line` when absent; `story` falls back to `wa` then `line`.
  photo   OPTIONAL, one of food | edu | diwali | xmas. REAL AQ photos only.

CONTENT WARNING FOR WHOEVER READS THIS NEXT: the items below are MOCK, written
from a verbal brief on 2026-09-22 and not verified against anything. Before this
ships, check two things: the Terathon registration mechanics (is "priority
access" a real promise or an intention?), and what "AQ Labs closed off" actually
means (wrapped for the season? shut permanently?). VOICE.md sec. 1.5: a claim
comes from the brief or it is omitted. (The domain WAS an open question here -
transcribed as "ngoacqua.com" from a verbal brief, corrected to ngoaquaterra.com
on 2026-09-22. Worth remembering that a URL taken down by ear is worth reading
back before it goes on a poster.)
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

OUT = "out/dispatch/no01"


# ============================================================================
# THE BRIEF - this is the whole input surface. Nothing else gets edited.
# ============================================================================
BRIEF = {
    "issue": "01",
    "kicker": "this week at aq",
    "dateline": "22 sep 2026",
    "tagline": "what's / moving",          # "/" splits the masthead into lines
    "cover_photo": "diwali",               # a REAL AQ photo key, or omit entirely
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all five.",
    "wa_signoff": ("the detail on each one is in the poster. if your team did "
                   "something that isn't here, reply and it goes in no. 02."),
    "ig_signoff": ("the detail on each one is in the stories. not in the volunteer "
                   "group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],

    "items": [
        {
            "dept": "events",
            "chip": "events",
            "head": "new spot, new vibe",
            "line": ("diwali and terathon both move to a new venue this year with a "
                     "new look, and events is now running its own page, which is live."),
            "story": ("diwali and terathon are both moving to a new venue this year, "
                      "and the whole look is being redone with them. the events team "
                      "has also set up its own page, which is live now, and they are "
                      "putting together the group of people who will handle marketing "
                      "for both. no experience needed to join that, same as always."),
            "wa": ("diwali and terathon are both moving to a new venue this year, and "
                   "the look is being redone along with it. events has set up its own "
                   "page, which is live now, and they are looking for people to handle "
                   "the marketing for both. no experience needed."),
            "photo": "diwali",
        },
        {
            "dept": "events",
            "chip": "terathon",
            "head": "registration is open",
            "line": ("registration opened this week. if it starts filling up, aq members "
                     "get priority access, so it is worth booking a spot early."),
            "story": ("terathon registration opened this week and it is open to everyone, "
                      "not just aq. if it starts to fill up, aq members get priority "
                      "access to the remaining spots, which is the reason to book early "
                      "rather than leave it. there is no deadline pressure beyond that."),
            "wa": ("terathon registration opened this week, and it is open to everyone. "
                   "if it starts filling up, aq members get priority access to what is "
                   "left, so it is worth booking a spot at some point rather than "
                   "leaving it to the end. no hard deadline beyond that."),
        },
        {
            "dept": "content",
            "chip": "magazine",
            "head": "blogs is now bigger",
            "line": ("the blogs team is now the digital magazine team, and the new website "
                     "section will carry articles, poems, photography, art and games."),
            "story": ("the blogs team has become the digital magazine team, and they are "
                      "building a section of the website that goes well past blog posts. "
                      "it will take articles, longer pieces, poems, photography, art and "
                      "games, basically whatever anyone wants to make. they are working "
                      "on a first draft, and inductions open to everyone once that is "
                      "settled and they know how they want to run it."),
            "wa": ("the blogs team is now the digital magazine team. they are building a "
                   "new section of the website that goes well past blog posts: articles, "
                   "longer pieces, poems, photography, art and games. a first draft comes "
                   "first, then inductions open to everyone once they have worked out how "
                   "they want to run it."),
        },
        {
            "dept": "labs",
            "chip": "labs",
            "head": "labs is wrapped",
            "line": ("aq labs has closed off for now, and the podcast has moved to "
                     "linkedin, where the longer conversations will live from here."),
            "story": ("aq labs has closed off for now. the podcast is running on linkedin "
                      "instead, and that is where the longer conversations are going to "
                      "live from here on. if that is the version of what we are doing "
                      "that interests you, that is the place to follow."),
            "wa": ("aq labs has closed off for now. the podcast has moved to linkedin, "
                   "and that is where the longer conversations will live from here on. "
                   "follow us there if you want that version of what we are up to."),
        },
        {
            "dept": "ops",
            "chip": "website",
            "head": "the site is coming",
            "line": ("the website is in build. hr is training on it first, then everyone "
                     "gets an account and somewhere to post their own work."),
            "story": ("the website is finally in build. hr is learning how to use it "
                      "before the rest of us get accounts, which is why it is taking a "
                      "beat. once it opens up it becomes a live hub: you post your own "
                      "work there, aq or not, and you can see what everyone else across "
                      "the org is actually up to."),
            "wa": ("the website is finally in build. hr is training on it before the rest "
                   "of us get accounts. once it opens it becomes a live hub where you "
                   "post your own work, aq or not, and see what everyone else is up to. "
                   "that is the whole point of it."),
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
    for f in ("wa_poster", "s00_cover", "s01_events", "s03_content"):
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
