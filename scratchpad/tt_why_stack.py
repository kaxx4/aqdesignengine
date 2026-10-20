"""TerraThon-look stories: WHY WE DO EVENTS AT AQ (2026-10-20). User brief: "you might be wondering where all the money goes... all profits to AQ that fuels our welfare campaigns,
public accounts, campaigns ka brief". Same STACK layout as the welfare deck (tt_welfare_stack.py, reused as a module): photo circle, a card sized from its measured content,
header (caption, shuriken, pill) and footer (AQ logo, AQ LIVE logo, ALL FOR CHARITY), NeutralFace only, a photo-collage backdrop.
Arc: where does the money go? -> why events (no donations, so the parties ARE the funding) -> who pays (events) -> where the profit goes (back into welfare) -> what it
funds (the campaigns, one line each) -> the books are open -> come to the next one.

FACTS, and where each comes from (nothing else is claimed):
  SITE = the user's AquaTerra website text (2026-10-20): zero donations and zero external funding since day one; Crftd sells streetwear and its profits fund the welfare drives;
         the events fund the welfare work; "open books" (public accounts) is a page on the site; DARPAN certified NGO; student run, Kolkata born, est. 2021.
  USER = "all profits to AQ that fuels our welfare campaigns" (this brief).
  TABLE = campaign names and what each is, from the project table (scratchpad/welfare_projects_2026-10-19.psv titles): Tails and Treats (feeding stray dogs), Grow Green (plantation
         drive), Food For All (food distribution drive), Sharbat Seva (sharbat distribution drive), Wear and Share (clothes collection drive), Book Basket (book collection drive),
         Respect and Reach (old age home drive), Sundarbans (relief trips).
  Deliberately NOT said: ticket revenue figures, "100% of profits" as a rule (the site says it of Paradox 2026 only), sponsor money (the site says zero external funding), any rupee amount.
Photos: the repo's real AQ event photos (faces mostly turned away or blurred; people incl. minors: confirm consent) and the user's welfare photos (git-ignored).
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_why_stack.py [feed story]   ->  out/versions/terrathon_carousel/why_events_v2/<canvas>/NN_<key>.png
"""
import asyncio, importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("tt_welfare_stack", os.path.join(ROOT, "scratchpad", "tt_welfare_stack.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ws, tc = m.ws, m.tc
from PIL import Image

E, T = "engine/assets/img/events/", "engine/assets/terrathon/"
def sq(path, fx=0.5, fy=0.5, w=1200):
    """Square crop of an event photo around a focus (fractions of the leftover), as a data URI."""
    im = Image.open(path); s = min(im.size)
    l = int((im.width - s) * fx); t = int((im.height - s) * fy)
    return ws.uri(path, w=w, crop=(l, t, l + s, t + s))

PHOTO = {
    "cover": sq(T + "dd_photos/decor.jpg"),                                                   # the Disco Diwali photo-booth set: no faces
    "why": sq(T + "dd_photos/dance.jpg", fx=0.4),                                             # dancers seen from behind
    "who": sq(E + "summer-aq-turns-five/01_registration-desk.jpg", fy=0.55),                  # the ticket / registration desk
    "profit": ws.CLOSE,                                                                       # the banana distribution
    "funds": (ws.PHOTOS.get("animals") or [(None,)])[0][0],                                   # a feeding drive
    "books": ws.COVER,                                                                        # the team
    "close": sq(E + "unsorted-2026-10-07/11_dance-green-light-portrait.jpg", fy=0.45),        # the dance floor
}
SLIDES = [
    dict(kind="cover", key="cover", lines=["WHERE DOES", "THE MONEY GO?"], base=104, tag="THE HONEST ANSWER, IN A FEW SWIPES.", cap="SWIPE TO SEE", photo=PHOTO["cover"], pill="THE WHY"),
    dict(kind="pillar", key="why", n=1, of=5, lines=["WHY WE", "THROW EVENTS"], base=92, tag="WE TAKE ZERO DONATIONS. SO THE PARTIES ARE THE FUNDING.", photo=PHOTO["why"], pill="THE WHY"),
    dict(kind="pillar", key="who", n=2, of=5, lines=["WHO PAYS", "FOR IT?"], base=92, tag="OUR EVENTS. NOT DONATIONS. NOT EXTERNAL FUNDING.", photo=PHOTO["who"], pill="THE WHY"),
    dict(kind="pillar", key="profit", n=3, of=5, lines=["WHERE THE", "PROFIT GOES"], base=92, tag="ALL OF IT BACK INTO OUR WELFARE CAMPAIGNS.", photo=PHOTO["profit"], pill="THE WHY"),
    dict(kind="pillar", key="funds", n=4, of=5, lines=["WHAT IT", "FUNDS"], base=92, photo=PHOTO["funds"], pill="THE WHY",
         chips=["CHILDREN + EDUCATION", "HEALTHCARE", "WOMEN EMPOWERMENT", "ELDERLY", "COMMUNITY WELFARE", "ENVIRONMENT", "ANIMAL WELFARE", "AND MANY MORE"]),   # the seven sectors (user's pillars) + the closing pill
    dict(kind="pillar", key="books", n=5, of=5, lines=["THE BOOKS", "ARE OPEN"], base=92, tag="OUR ACCOUNTS ARE PUBLIC. YOU CAN SEE EVERY RUPEE.", photo=PHOTO["books"], pill="THE WHY",
         chips=["DARPAN CERTIFIED NGO", "ZERO DONATIONS"]),
    dict(kind="close", key="close", lines=["COME TO", "THE NEXT ONE"], base=92, tag="EVERY EVENT FUNDS THE WORK. @NGO.AQUATERRA", photo=PHOTO["close"], pill="THE WHY"),
]
m.SLIDES = SLIDES
m.OUT = "why_events_v2"
tc.VENUE = "KOLKATA BORN + STUDENT RUN"
BGSRC = dict(cover=T + "dd_photos/decor.jpg", why=T + "dd_photos/dance.jpg", who=E + "summer-aq-turns-five/01_registration-desk.jpg",
             close=E + "unsorted-2026-10-07/11_dance-green-light-portrait.jpg", x1=E + "disco-diwali-hall-2026-10-14/02_crowd-teal-kurta-purple.jpg",
             x2=E + "disco-diwali-hall-2026-10-14/08_boy-on-shoulders-stage-lights-portrait.jpg", x3=E + "unsorted-2026-10-07/02_IMG_7028_group-pink-balloons.jpg")
BG = {k: ws.uri(p, w=640) for k, p in BGSRC.items()}
for k in ("profit", "funds", "books"): BG[k] = ws.BG.get({"profit": "community", "funds": "animals", "books": "environment"}[k]) or BG["x1"]      # welfare photos in the collage too
ws.BG = BG                                                     # the builder reads ws.BG for the backdrop collage; keys named like slides are left out of their own slide

if __name__ == "__main__":
    asyncio.run(m.main([a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]))
