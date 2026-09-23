"""DISPATCH no. 02 - week of 23 sep 2026, dictated verbally by the user in-session.

Adds the "startups" department (Roots / AQ.Ventures / Shikshaq) to the engine's
department vocabulary (engine/core.py DEPT, engine/dispatch.py DEPTS) - tomato
accent, the only ACCENTS entry not already claimed by a department or reserved
as brand furniture (pink). See core.py's DEPT comment for the full note.

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_002.py
Outputs into out/dispatch/no02/.

CONTENT NOTE: sourced from a voice dictation, not a written brief. Numbers kept
are the ones stated plainly (30+ students, 2nd/3rd/4th dates); anything vague
in the dictation ("soon", "this week") was kept soft rather than firmed up
into a fake date, per VOICE.md's truth ladder. A photo was sent in-session of
a person in a CRED t-shirt in front of a tree - NOT one of core.PHOTOS's four
real AQ photos (food/edu/diwali/xmas), so it is not used here.
"""

import asyncio, os, sys, importlib.util

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

BRIEF = {
    "issue": "02",
    "kicker": "this week at aq",
    "dateline": "23 sep 2026",
    "tagline": "still / moving",
    "cover_photo": "diwali",
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
            "dept": "startups",
            "chip": "roots",
            "head": "roots goes b2b",
            "line": ("roots is going b2b, building a dedicated arm to work directly "
                     "with businesses, and hiring for the new team opens soon."),
            "story": ("roots, aq's startup arm, is launching a dedicated b2b vertical "
                      "to work directly with businesses instead of only individual "
                      "clients. the team is putting the structure in place now, and "
                      "hiring for the new vertical opens soon - no fixed date yet. if "
                      "that side of aq interests you, keep an eye out."),
        },
        {
            "dept": "startups",
            "chip": "shikshaq",
            "head": "past papers going free",
            "line": ("shikshaq's past papers section is getting a major redesign, "
                     "giving students free access to past papers from many schools, "
                     "launching this week."),
            "story": ("shikshaq's past papers section is getting a major redesign, "
                      "giving students free access to past papers from a large number "
                      "of schools across kolkata. it is set to launch this week. once "
                      "it is live, shikshaq opens hiring for a vetting team to keep "
                      "submissions accurate, and answers to the papers are planned to "
                      "follow soon after."),
        },
        {
            "dept": "events",
            "chip": "terathon",
            "head": "terathon dates locked in",
            "line": ("terathon's dates are finalised for the 2nd, 3rd and 4th, with a "
                     "mini carnival and lottery running on the 3rd and 4th."),
            "story": ("terathon's dates are finalised for the 2nd, 3rd and 4th. "
                      "running alongside it on the 3rd and 4th is a mini carnival with "
                      "games and a lottery - more on what that's for in the next card."),
        },
        {
            "dept": "events",
            "chip": "disco diwali",
            "head": "early bird tickets open",
            "line": ("the mini carnival and lottery on the 3rd and 4th let anyone grab "
                     "early bird disco diwali tickets, and it is open to spectators too."),
            "story": ("the mini carnival and lottery on the 3rd and 4th doubles as an "
                      "early sales window for disco diwali: tickets bought there are at "
                      "early bird rates, ahead of the event going live to everyone else. "
                      "you do not need to be part of terathon to come either - it is "
                      "open to anyone who wants to stop by and watch."),
        },
        {
            "dept": "welfare",
            "chip": "welfare",
            "head": "two drives, one workshop",
            "line": ("welfare ran two donation drives and a teaching workshop at "
                     "pather sathi this weekend, reaching more than 30 students with "
                     "regular lessons."),
            "photo": "edu",
        },
    ],
}


async def main():
    os.makedirs(OUT, exist_ok=True)
    D.validate_brief(BRIEF)

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

    print("\n=== PIXEL CRITIQUE ===")
    for f in ("wa_poster", "s00_cover", "s01_startups", "s03_events"):
        path = "%s/%s.png" % (OUT, f)
        if os.path.exists(path):
            c = prev.critique(path)
            print("  %-14s fill=%.2f  %s" % (f, c["fill"], [i[0] for i in c["issues"]]))

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
