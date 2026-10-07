"""DISPATCH no. 04 (week 4). Three items: events, shikshaq, hr.

Content comes from the community manager's verbal brief of 2026-10-07. Nothing is
invented: no Disco Diwali date (asked to leave it out), no paper counts, no URLs.
Shikshaq is a new department (lime, core.DEPT) on purpose: it must not read as
welfare/mint. Photos are real team photos supplied for this issue, kept in the
git-ignored scratchpad/dispatch04_photos/ (identifiable people, public repo).

Run:  PYTHONIOENCODING=utf-8 python scratchpad/gen_dispatch_004.py
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

OUT = "out/dispatch/no04"


# ============================================================================
# THE BRIEF - this is the whole input surface. Nothing else gets edited.
# ============================================================================
BRIEF = {
    "issue": "04",
    "kicker": "this week at aq",
    "dateline": "7 oct 2026",
    "tagline": "what's / moving",
    "cover_photo": "scratchpad/dispatch04_photos/events_team.jpg",
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all three.",
    "wa_signoff": ("the detail on each one is in the poster. if your team did "
                   "something that isn't here, reply and it goes in no. 05."),
    "ig_signoff": ("the detail on each one is in the stories. not in the volunteer "
                   "group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],
    "items": [
        {
            "dept": "events", "chip": "disco diwali",
            "head": "rest? never heard of it",
            "line": ("terathon was a success and the events team has already started on "
                     "disco diwali. a break would have been nice, but it is a busy season."),
            "story": ("terathon went well, and the events team has not stopped since. "
                      "preparation for disco diwali has already started, so it is going to "
                      "be a busy season for them. a break would have been nice, but the "
                      "team is already planning the next one."),
            "photo": "scratchpad/dispatch04_photos/events_team.jpg",
        },
        {
            "dept": "shikshaq", "chip": "shikshaq",
            "head": "no, it is not welfare",
            "line": ("shikshaq keeps getting mistaken for welfare, and we are fixing that. "
                     "past papers are the proof: processed automatically, verified by "
                     "students, and slowly going live on the website."),
            "story": ("people keep assuming shikshaq is a welfare project, and we are "
                      "working on fixing that. the proof is past papers. an automated flow "
                      "now processes them, students verify each one, and the verified "
                      "papers are slowly going live on the website. it is built for "
                      "students preparing for exams."),
        },
        {
            "dept": "ops", "chip": "hr",
            "head": "the robots teach hr now",
            "line": ("hr is still working through its ai lessons. the latest ones covered "
                     "agents and projects, so the team is now officially more automated than us."),
            "story": ("hr continues with its ai lessons, and the most recent sessions "
                      "were about agents and projects. the team is learning how to hand "
                      "work to ai properly, which is more than most of us can say."),
            "photo": "scratchpad/dispatch04_photos/hr_meet.jpg",
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
    for f in ("wa_poster", "s00_cover", "s01_events", "s02_shikshaq", "s03_ops"):
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
