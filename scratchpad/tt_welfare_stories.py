"""TerraThon-look WELFARE IMPACT stories, v3 (2026-10-20, user: "dont mention such specific number / reduce the information"): cover + one overview slide + one slide
per welfare pillar + close, feed 1080x1350 AND story 1080x1920. Workflow C on the TerraThon format, reusing tt_carousel.py.
v3 is deliberately light: each pillar slab holds a headline, ONE big element and one short line, over a real user photo. No project counts, turnout counts, years or
edition numbers anywhere (v2 printed 234, 931, 558, 3,756 and the like; the user ruled those out).

The only numbers left are the user's own ROUND figures from the AquaTerra directory page (2026-10-19), printed with the page's own "+" and never re-derived:
4,000+ saplings planted, 3,500+ kids reached, 15,000+ bananas distributed. Where a pillar has no such figure its big element is a key word taken from the user's pillar
scope list (FREE camps, PADS, VISITS, DINNER), not an invented statistic. The directory's "582+ drives, blogs & openings" and "8 Sundarbans trips" are not used.
Pillars and their scope lines are the user's. Nothing is claimed for activities the project table has no row for (cleanups, blankets, water bowls, tuition).
Photos (user-supplied, git-ignored in engine/assets/terrathon/carousel_photos/, people incl. minors: confirm consent): children = repo Sundarbans classroom shot, the rest
<pillar>_welfare.jpg (health has a third-party banner's address and phone inpainted out). A slide falls back to a kit sticker if its file is absent.
Run: PYTHONIOENCODING=utf-8 python scratchpad/tt_welfare_stories.py [feed story]
"""
import asyncio, base64, importlib.util, io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
tc = _load("tt_carousel", "scratchpad/tt_carousel.py")
from PIL import Image

edu = Image.open("engine/assets/img/education-sundarban.jpeg"); ew, eh = edu.size
def uri(path, w=900, crop=None):
    im = Image.open(path).convert("RGB")
    if crop: im = im.crop(crop)
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=86); return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
PD = "engine/assets/terrathon/carousel_photos/"
PHOTOS = {"children": [(uri("engine/assets/img/education-sundarban.jpeg", crop=(0, 0, ew, int(eh * 0.72))), "50% 30%")]}
for key in ("all", "health", "women", "elderly", "community", "environment", "animals"):      # "all" = the overview slide's photo (kids at an art workshop)
    if os.path.exists(f"{PD}{key}_welfare.jpg"): PHOTOS[key] = [(uri(f"{PD}{key}_welfare.jpg", w=1200), "50% 50%")]
COVER = uri(f"{PD}cover_welfare.jpg", w=1200) if os.path.exists(f"{PD}cover_welfare.jpg") else None     # team at the Sundarbans village gate
CLOSE = uri(f"{PD}close_welfare.jpg", w=1200) if os.path.exists(f"{PD}close_welfare.jpg") else None     # banana distribution
tc.photo_list = lambda key: PHOTOS.get(key, [])

BG = {k: uri(src, w=640, crop=(0, 0, ew, int(eh * 0.72))) if k == "children" else uri(src, w=640)       # small copies for the backdrop collage (the circle keeps the 1200px one)
      for k, src in (("children", "engine/assets/img/education-sundarban.jpeg"), *((k, f"{PD}{k}_welfare.jpg") for k in ("cover", "all", "close", "health", "women", "elderly", "community", "environment", "animals")))
      if os.path.exists(src)}
tc.DATE, tc.VENUE = "SINCE 2021", "KOLKATA + THE SUNDARBANS"
ITEMS = [   # key, headline, one short line (DRAFT copy), sticker (only where no photo), recolour
    ("all", "THE IMPACT SO FAR", "SINCE 2021. STILL SHOWING UP.", "carnival.png", False),
    ("children", "CHILDREN + EDUCATION", "CLASSES, BOOKS AND ART.", "smiley.png", False),
    ("health", "HEALTHCARE", "FREE CAMPS, CHECKUPS AND BLOOD DRIVES.", "smiley.png", True),
    ("women", "WOMEN EMPOWERMENT", "PADS, PERIOD TALK AND MONEY SKILLS.", "flower.png", True),
    ("elderly", "ELDERLY", "OLD AGE HOME VISITS. SOMEONE SHOWED UP.", "flower.png", False),
    ("community", "COMMUNITY WELFARE", "FOOD, CLOTHES, BOOKS, SHARBAT AND TOYS.", "carnival.png", False),
    ("environment", "ENVIRONMENT", "PLANTATION DRIVES AND GREEN WORKSHOPS.", "flower.png", True),
    ("animals", "ANIMAL WELFARE", "DINNER FOR STRAYS. ONE DRIVE AT A TIME.", "smiley.png", False),
]
STATS = {   # ONE big element per slide: a round figure the user supplied, or a key word from the user's scope list. Never a count.
    "all": [("4,000+", "SAPLINGS PLANTED"), ("3,500+", "KIDS REACHED"), ("15,000+", "BANANAS DISTRIBUTED")],
    "children": [("3,500+", "KIDS REACHED")],
    "community": [("15,000+", "BANANAS DISTRIBUTED")],
    "environment": [("4,000+", "SAPLINGS PLANTED")],
}       # health, women, elderly, animals have no round figure from the user: headline + one line, no invented stat
LAYOUT = {   # lighter slab, bigger circle: less text, more picture
    "feed": dict(hero_max=(760, 640), slab_top=700, slab_h=440, D=620, SX=90, SW=900, strip_y=1162),
    "story": dict(hero_max=(840, 760), slab_top=980, slab_h=470, D=760, SX=90, SW=900, strip_y=1486),
}
tc.DECKS["welfare5"] = dict(items=ITEMS, stats=STATS, layout=LAYOUT, bg_photos=BG, cover_photo=COVER, close_photo=CLOSE, num_skip=1, head=("WHAT WE DO", "SEVEN WAYS WE SHOW UP"), swipe="SWIPE TO SEE", head_w=770,
                           num=True, free_sub=True, compact=True, pill="AQUATERRA", cover_titles=("AQUATERRA", "IMPAACT"),
                           cover_sub="SINCE 2021. STILL SHOWING UP.", close=("COME TO", "THE NEXT ONE", "@NGO.AQUATERRA"))
if __name__ == "__main__":
    cvs = [a for a in sys.argv[1:] if a in ("feed", "story")] or ["feed", "story"]
    asyncio.run(tc.main(cvs, ("welfare5",)))        # renders to out/versions/terrathon_carousel/welfare5/ (v5 = v4 + real photos on the cover, overview and close)
