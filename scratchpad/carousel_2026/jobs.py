"""Per-project carousel jobs. Photo picks made by LOOKING at each contact sheet.
All copy is sourced from the CSV's key_statistic / short_summary — no invented numbers
(CAROUSEL_PLAYBOOK rule 6). Captions describe the photo they sit on (rule 5).
slides = (filename, caption_or_None, sticker_or_None)
"""

JOBS = {
    "learners_den_art": dict(
        slug="learners_den_art", loc="Pather Saathi", date_label="APR 2026", seed=0,
        title_html="LEARNER'S<br>DEN", title_size=84,
        subhead="25+ kids took on days, weeks and months &mdash; then drew the rest of the afternoon",
        picks=["26.jpg"],
        slides=[
            ("06.jpg", "she held it up before the crayon was even back in the box", "finished, framed"),
            ("12.jpg", "a castle in six colours, drawn on a clipboard", None),
            ("04.jpg", "a volunteer showing off a portrait she was handed", "artist at work"),
            ("10.jpg", "everyone wanted their page in the photo", None),
        ]),

    "disha_grammar": dict(
        slug="disha_grammar", loc="Disha Foundation", date_label="APR 2026", seed=2,
        title_html="BUILD-A<br>SENTENCE", title_size=80,
        subhead="20 kids pulled sentences apart into subjects and predicates, then proved it on paper",
        picks=["15.jpg"],
        slides=[
            ("09.jpg", "worksheet on the floor, working through it line by line", "subject + predicate"),
            ("21.jpg", "answering out loud, in front of the whole room", None),
            ("08.jpg", "a volunteer walking the class through one more example", "four volunteers"),
            ("27.jpg", "down at floor level, where the work was actually happening", None),
        ]),

    "mothers_day": dict(
        slug="mothers_day", loc="Disha Foundation", date_label="MAY 2026", seed=4,
        title_html="16 CARDS<br>FOR MUM", title_size=82,
        subhead="students spent the session making mother's day cards, start to finish",
        picks=["09.jpg"],
        slides=[
            ("15.jpg", "crayons out, flowers going down on the front cover", "16 cards made"),
            ("16.jpg", "a heart drawn in green, finished by hand", None),
            ("05.jpg", "the finished stack &mdash; every one of them written out", "start to finish"),
            ("21.jpg", "pizza at the end, because the cards were done", None),
        ]),

    "valentines_cards": dict(
        slug="valentines_cards", loc="Pather Saathi", date_label="FEB 2026", seed=6,
        title_html="CARDS<br>BY HAND", title_size=88,
        subhead="25+ kids made valentine's day cards alongside volunteers",
        picks=["16.jpg"],
        slides=[
            ("05.jpg", "a flower drawn in five colours, held up for the camera", "made by hand"),
            ("06.jpg", "four hearts on a string, outlined in red marker", None),
            # 12.jpg pulled: its left page shows reverse-side bleed-through, so the greeting
            # reads backwards, and the 4:5 crop cut the subject down to a chin.
            ("13.jpg", "two cards, held up the moment the markers went down", "25+ kids"),
            ("15.jpg", "a paper heart, covered corner to corner", None),
        ]),

    "smile_notes_bhawanipore": dict(
        slug="smile_notes_bhawanipore", loc="Bhawanipore", date_label="MAR 2026", seed=8,
        title_html="SMILE<br>NOTES", title_size=92,
        subhead="100 handwritten affirmations and 100 toffees, handed to passers-by",
        picks=["12.jpg"],
        slides=[
            ("02.jpg", "he read his before we'd finished explaining it", "100 notes"),
            ("01.jpg", "handed one over on his shift, outside the gate", None),
            ("09.jpg", "a note and a toffee, taken with both hands", "one each"),
            ("14.jpg", "stopped at the stall and left one behind", None),
        ]),

    "smile_notes_laketown": dict(
        slug="smile_notes_laketown", loc="Lake Town Footbridge", date_label="MAY 2026", seed=10,
        title_html="SMILE<br>NOTES", title_size=92,
        subhead="six volunteers, 100 notes and 100 toffees, given out on the footbridge",
        # cover was 03.jpg (group on the restaurant steps) but 04.jpg is the same group from a
        # half-step back — cover and last slide read as the same frame. 01.jpg leads instead;
        # 03.jpg keeps the group shot as the closer and 04.jpg is dropped.
        picks=["01.jpg"],
        slides=[
            ("00.jpg", "handed across the counter, mid-shift", "100 notes"),
            ("02.jpg", "he kept his and asked what it said", None),
            ("03.jpg", "the whole group, before the notes ran out", "six volunteers"),
        ]),

    "smile_notes_mba": dict(
        slug="smile_notes_mba", loc="MBA Chaiwala, Lake Town", date_label="MAR 2026", seed=12,
        title_html="SMILE<br>NOTES", title_size=92,
        subhead="100 notes and 100 toffees, handed out around Lake Town",
        picks=["03.jpg"],
        slides=[
            ("00.jpg", "handed one over at the stall, between orders", "100 notes"),
            ("01.jpg", "she took hers and read it standing up", None),
        ],
        # the child's head sits centre-top on flat green turf; dark hair scores as background,
        # so doodles landed directly on it in v1. Box out the head and shoulders.
        # box measured off the v2 render, not estimated: the head+hair mass runs x 170-810,
        # y 30-680 in canvas space. The first guess started the box too far right and the
        # doodles landed on hair again.
        extra_exclude={"01.jpg": [(160, 20, 700, 680)]}),

    "teaching_english": dict(
        slug="teaching_english", loc="Ektara Foundation", date_label="APR 2026", seed=14,
        title_html="CONJUNCTIONS<br>&amp; VERBS", title_size=62,
        subhead="15 kids, one class on conjunctions and verbs, with five volunteers",
        picks=["00.jpg"],
        slides=[
            ("03.jpg", "the whole class, at the end of the lesson", "15 kids"),
            ("01.jpg", "packing up, still talking about it", None),
            ("02.jpg", "one more before everyone left", "five volunteers"),
        ]),
}


# ── the two photo-poor events ────────────────────────────────────────────────────────
# Neither has enough usable frames for a photo-only carousel (3 and 1). Rather than pad with
# near-duplicates or fabricate imagery (§9 real-assets-only), each closes on a type slide built
# from the row's OWN key_statistic.
JOBS["teaching_internship"] = dict(
    slug="teaching_internship", loc="Ektara Foundation", date_label="APR 2026", seed=16,
    title_html="TEACHING<br>INTERNSHIP", title_size=68,
    subhead="15 kids taught nouns, pronouns and verbs, with four volunteers",
    picks=["00.jpg"],
    slides=[
        ("01.jpg", "working through it at their desks, by the window", "15 kids"),
        ("02.jpg", "questions from the back row, halfway through", None),
    ],
    type_slides=[
        ("EKTARA FOUNDATION · APR 2026", "15 KIDS.<br>NOUNS,<br>PRONOUNS,<br>VERBS.",
         "four AquaTerra volunteers ran the session end to end."),
    ])

JOBS["sentence_secrets"] = dict(
    slug="sentence_secrets", photodir="sentence_secrets_ektara", loc="Ek Tara", date_label="APR 2026", seed=18,
    title_html="SENTENCE<br>SECRETS", title_size=76,
    subhead="15 kids took apart subjects and predicates, then proved it on worksheets",
    picks=["00.jpg"],
    slides=[],
    type_slides=[
        ("EK TARA · APR 2026", "15 KIDS.<br>SUBJECTS<br>AND<br>PREDICATES.",
         "broken down with examples and back-and-forth questioning until it clicked."),
        ("THE PART THAT STUCK", "WORKSHEETS<br>FOLLOWED.",
         "seven volunteers, one grammar lesson the room actually looked forward to."),
    ])
