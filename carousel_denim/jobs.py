"""Denim upcycling workshop carousel job. Photo picks made by looking at the contact sheet.
slides = (filename, caption_or_None, sticker_or_None)
"""

JOBS = {
    "denim_workshop": dict(
        slug="denim_workshop", loc="Calcutta International School", date_label="14 AUG 2026",
        seed=20,
        title_html="DENIM<br>UPCYCLE", title_size=84,
        subhead="AquaTerra ran a denim upcycling workshop with students at Calcutta International School",
        picks=["00.jpg"],
        slides=[
            ("01.jpg", "old jeans, cut down before they became something new", "cut to reuse"),
            ("02.jpg", "the whole classroom in on it, hands up with questions", None),
            ("03.jpg", "beads and paint going onto denim scraps", "hand-decorated"),
            ("04.jpg", "a finished piece, made from what would've been thrown out", "upcycled"),
        ]),
}
