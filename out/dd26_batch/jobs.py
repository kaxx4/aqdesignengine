"""DD 3.0 carousels (Nov 2026). Copy describes only what each photo shows; no invented numbers.
slides = (filename, caption_or_None, sticker_or_None); filenames are staged names in stage/<slug>/src_images.
"""
import os, shutil
R = "out/dd26_batch"
STAGE = {
 "dd26_stalls": {
  "gajra.jpg": "stalls/gajra_jhumka/00.jpg", "mod.jpg": "stalls/mod/02.jpg",
  "chetan.jpg": "stalls/chetan_kala/00.jpg", "unbasic.jpg": "stalls/unbasic/01.jpg",
  "meetcute.jpg": "stalls/meet_cute/01.jpg", "diyas.jpg": "stalls/bedazzling/04.jpg",
  "eloza.jpg": "stalls/eloza/01.jpg", "kulfi.jpg": "stalls/bombay_kulfi/00.jpg"},
 "dd26_groups": {
  "trio.jpg": "stalls/cravella/06.jpg", "pair.jpg": "groups/dslr/28.jpg",
  "thumbs.jpg": "stalls/eloza/00.jpg", "hug.jpg": "groups/dslr/40.jpg",
  "nandu.jpg": "stalls/nandu_jee/00.jpg", "huddle.jpg": "groups/dslr/17.jpg",
  "backs.jpg": "groups/dslr/27.jpg"},
}
def stage():
    for slug, m in STAGE.items():
        d = f"{R}/stage/{slug}/src_images"; os.makedirs(d, exist_ok=True)
        for dst, src in m.items(): shutil.copyfile(f"{R}/{src}", f"{d}/{dst}")

JOBS = {
 "dd26_stalls": dict(
    slug="dd26_stalls", loc="Disco Diwali 3.0", date_label="NOV 2026", seed=3,
    title_html="THE STALLS<br>OF DD 3.0", title_size=84,
    subhead="donuts, kulfi, jhumkas, crochet and more, all under one roof at Disco Diwali 3.0",
    picks=["gajra.jpg"],
    slides=[
        ("mod.jpg", "the Mad Over Donuts sign, glowing over a dark counter", "mad over donuts"),
        ("chetan.jpg", "crochet flowers and plush toys under a marigold garland, Chetan Kala", None),
        ("unbasic.jpg", "beaded cherries, stars and jellyfish laid out on black cloth, Unbasic", "unbasic"),
        ("meetcute.jpg", "noodles, momos and spices lined up in trays at Meet Cute", None),
        ("diyas.jpg", "rows of clay diyas beside sheets of gem stickers", "bedazzling"),
        ("eloza.jpg", "bracelets and rings laid out on pink and cream trays, Eloza", None),
        ("kulfi.jpg", "a smile behind the Bombay Kulfi counter", "bombay kulfi"),
    ],
    # vision starved on kulfi.jpg (glass door + fairy lights score as busy at every rung).
    # Spots measured off the v1 render on a 100px grid: free cream wall, left of the door,
    # below the sign (y 505-660) and above the chair (y 980). (x, y, size, local luminance)
    spots_override={"kulfi.jpg": [(56, 716, 60, 225), (150, 806, 44, 225), (66, 890, 52, 225)]}),
 "dd26_groups": dict(
    slug="dd26_groups", loc="Disco Diwali 3.0", date_label="NOV 2026", seed=9,
    title_html="THE PEOPLE<br>OF DD 3.0", title_size=80,
    subhead="pairs, trios and packs of friends, caught at Disco Diwali 3.0",
    picks=["trio.jpg"],
    slides=[
        ("pair.jpg", "two friends leaning in at the Eloza stall", "two of a kind"),
        ("thumbs.jpg", "three thumbs up under the marigold garlands at Eloza", None),
        ("hug.jpg", "a hug, mid-laugh, against the coloured wall", None),
        ("nandu.jpg", "the Nandu Jee food stall pair, peace sign up", "nandu jee"),
        ("huddle.jpg", "heads down together over the table, kurtas and stoles on", None),
        ("backs.jpg", "backs to the camera under the fairy lights, red, teal and pink kurtas", None),
    ],
    # hair boxes measured off the v1 render on a 100px grid (a doodle landed on each head)
    extra_exclude={
        "hug.jpg":    [(250, 300, 450, 660), (640, 160, 440, 840)],   # both heads + hair
        "huddle.jpg": [(0, 270, 830, 600)],                           # four heads in a row
    },
    # both exclusions leave vision with nothing (the photos are almost all heads), so spots are
    # placed by hand in the wall measured off the v2 grid: hug = pink wall left of the heads and
    # above them (y 150-290); huddle = the beige wall above the heads, clear of the ceiling lamp
    # at x 675-745 and of the dots box. (x, y, size, local luminance)
    spots_override={
        "hug.jpg":    [(60, 170, 60, 170), (170, 235, 44, 170), (40, 430, 52, 170)],
        "huddle.jpg": [(110, 175, 56, 190), (330, 160, 44, 190), (880, 215, 52, 190)],
    }),
}
