"""TerraThon-look carousel + stories: WHY WE THROW EVENTS (events fund the impact). Workflow C on the TerraThon format.
Reuses tt_carousel.py (the TerraThon slide builder) with a new deck. Real AQ photos replace stickers in the circles where one fits;
the rest keep kit stickers. Every number is from brain/AQ_FACTS.md (as of 2025-26): 19 fundraisers logged 2021-2025, ~90% event money, 0% donations,
25,000+ volunteer hours, 3,500+ children, 500+ projects. Copy is DRAFT. Fest pill reads AQUATERRA (not TERRATHON): this is about all AQ events.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_why_events.py [feed story]
"""
import asyncio, base64, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
spec = importlib.util.spec_from_file_location("tt_carousel", os.path.join(ROOT, "scratchpad", "tt_carousel.py"))
tc = importlib.util.module_from_spec(spec); spec.loader.exec_module(tc)
from PIL import Image
EV = "engine/assets/img/events/"
def uri(path, w=900, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
edu = Image.open("engine/assets/img/education-sundarban.jpeg"); ew, eh = edu.size
PHOTOS = {
    "party": [(uri("engine/assets/terrathon/dd_photos/dance.jpg"), "42% 40%")],
    "students": [(uri(EV + "summer-aq-turns-five/07_group-portrait-pink-light.jpg"), "50% 40%")],
    "classroom": [(uri("engine/assets/img/education-sundarban.jpeg", crop=(0, 0, ew, int(eh * 0.72))), "50% 30%")],
    "blanket": [(uri("engine/assets/img/fundraising-diwali.jpeg"), "50% 45%")],
}
tc.photo_list = lambda key: PHOTOS.get(key, [])
tc.DATE, tc.VENUE = "2021-2025", "19 FUNDRAISING EVENTS LOGGED"
ITEMS = [
    ("party", "THE PARTY", "ONE LOUD NIGHT. EVERY TICKET COUNTS.", "basketball.png", False),
    ("ticket", "THE TICKET", "~90% OF OUR MONEY IS EVENT TICKETS AND SPONSORS.", "flower.png", False),
    ("students", "STUDENTS RUN IT", "25,000+ VOLUNTEER HOURS, LOGGED.", "smiley.png", False),
    ("zero", "0% DONATIONS", "STUDENTS EARN WHAT THEY GIVE.", "smiley.png", True),
    ("classroom", "THE CLASSROOM", "3,500+ CHILDREN REACHED THROUGH WORKSHOPS.", "flower.png", False),
    ("blanket", "THE BLANKET", "A RIBBON. A NOTE. SOMEONE SEEN.", "smiley.png", True),
    ("projects", "500+ PROJECTS", "SINCE JUNE 2021. THE PARTY KEEPS PAYING.", "carnival.png", False),
]
tc.DECKS["why"] = dict(items=ITEMS, head=("WHY WE DO", "WHAT WE DO"), swipe="SWIPE FOR THE WHY", num=True, free_sub=True, compact=True,
                       pill="AQUATERRA", cover_titles=("PAARTY", "FOR GOOD"), cover_sub="EVENTS FUND THE WORK",
                       close=("COME TO", "THE NEXT ONE", "@NGO.AQUATERRA"))
if __name__ == "__main__":
    cvs = [a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(tc.main(cvs, ("why",)))
