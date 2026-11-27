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

OUT = "out/dispatch/no07"

# USER-SUPPLIED PHOTOS (adaptation, recorded): the two screenshots were handed over
# by the issue's author, so they are real, not fabricated. dispatch only accepts keys
# in core.PHOTOS, so they are registered here under their own keys.
import base64
IMG = os.path.join(os.getcwd(), "scratchpad", "dispatch_002_src") + os.sep
import io
from PIL import Image
# Pre-cropped so the story band (about 3:1) cuts BETWEEN lines of text, never through one.
for key, fn, box in (("mag", "1.jpg", (0, 0, 977, 325)), ("chat", "2.jpg", (0, 12, 1206, 405))):
    buf = io.BytesIO(); Image.open(IMG + fn).convert("RGB").crop(box).save(buf, "JPEG", quality=92)
    D.core.PHOTOS[key] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
# the masthead card is near-square, so it gets the UNCROPPED screenshot (a 3:1 band crop shows fragments)
D.core.PHOTOS["mag_full"] = "data:image/jpeg;base64," + base64.b64encode(open(IMG + "1.jpg", "rb").read()).decode()

BRIEF = {
    "issue": "07",
    "kicker": "this week at aq",
    "dateline": "27 nov 2026",
    "tagline": "what's / moving",
    "cover_photo": "mag_full",
    "handle": "@ngo.aquaterra",
    "site": "ngoaquaterra.com",
    "story_cta": "swipe for all three.",
    "wa_signoff": ("if your team did something that isn't here, reply and it goes in no. 08."),
    "ig_signoff": ("not in the volunteer group yet? dm us."),
    "tags": ["#aquaterra", "#kolkata", "#studentrun"],
    "items": [
        {
            "dept": "content",
            "chip": "magazine",
            "head": "third launch loading",
            "line": ("the digital magazine team is working on its third launch, so hard that "
                     "their sessions keep hitting the weekly usage limit."),
            "photo": "mag",
        },
        {
            "dept": "events",
            "chip": "starry nights",
            "head": "is starry nights happening? \U0001F440",
            "line": ("the dms are flooded with people asking about the dates, and even we want "
                     "to know! stay tuned and follow @aq.lives for updates."),
            "photo": "chat",
        },
        {
            "dept": "welfare",
            "chip": "dog drives",
            "head": "time for dog drives",
            "line": ("winter is the perfect time for dog drives. spend time with the dogs, give "
                     "them the care they need, then get a treat at sharma or kona dukaan."),
            "story": ("now that winter is here, it is the perfect time to organise dog drives. "
                      "spend some time with the dogs, help give them the care they need, and "
                      "make a difference in their day. and of course, no dog drive is complete "
                      "without a post-drive treat stop at sharma or kona dukaan."),
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
    for f in ("wa_poster", "s00_cover"):
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
