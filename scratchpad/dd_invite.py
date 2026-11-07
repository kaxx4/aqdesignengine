"""DISCO DIWALI "SPECIAL INVITATION" poster (user, 2026-11-07: 'poster for special invitation, entry fee Rs 550'). Built on poster_ref (feed / WhatsApp) and story_ref (story) with the
full-details block: edition, 'Special invitation', the fee as the second hero line, then date, time, venue. Supplied facts only: 10th November 2026, 4:30 PM onwards, 60 Chowringhee
Banquets, Rs. 550 entry (user, 2026-11-07), all for charity. No lineup, no ticket link (nothing is said about how invitees pay or register). The story uses the brand diya-pattern ground.
Run: PYTHONIOENCODING=utf-8 python scratchpad/dd_invite.py -> out/discodiwali/invite/{feed,story}.png"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "engine"))
spec = importlib.util.spec_from_file_location("discodiwali", os.path.join(ROOT, "engine", "discodiwali.py"))
dd = importlib.util.module_from_spec(spec); spec.loader.exec_module(dd)
OUT = os.path.join(ROOT, "out", "discodiwali", "invite")
BRIEF = dict(edition="Masquerade Sangeet Edition", status="Special invitation", note=os.environ.get("FEE", "Entry Rs. 550"),
             date="10th November, 2026", time="4:30 PM onwards", venue="60, Chowringhee Banquets", link=False)
GROUND = os.path.join(ROOT, "engine", "assets", "img", "events", "disco-diwali-soldout", "diya_story_ground.jpg")

async def main():
    async with dd.B.session():
        await dd.render_poster("poster_ref", BRIEF, "feed", os.path.join(OUT, "feed.png"))
        await dd.render_poster("story_ref", dict(BRIEF, photo=GROUND), "story", os.path.join(OUT, "story.png"))
    print("done ->", OUT)
asyncio.run(main())
