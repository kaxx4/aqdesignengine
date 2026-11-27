"""Starry Night throwback: Dec 2024 + Starry Night 2.0 (Dec 2025).
slides = (file, caption, sticker, date_label). Captions describe the photo they sit on.
"""
D24, D25 = "DEC 2024", "DEC 2025"
JOB = dict(
    slug="starry_throwback", loc="Starry Night", date_label="DEC 2024 + DEC 2025", seed=21,
    eyebrow="THROWBACK &middot; DEC 2024 + DEC 2025",
    title_html="STARRY<br>NIGHT", title_size=150,
    subhead="December 2024 and Starry Night 2.0, one more time under the lights",
    picks=["2024/01.jpg"],
    slides=[
        ("2024/02.jpg", "star lights hung in daylight over an empty court, the night still to come", "starry night 2024", D24),
        ("2024/03.jpg", "the tree up, the tables dressed, the sky going gold behind the net", None, D24),
        ("2024/04.jpg", "friends on the turf in front of the tree, the AquaTerra neon glowing behind them", None, D24),
        ("2024/05.jpg", "a stall under the net after dark, with a hand-lettered sign: &ldquo;get your lip balms pierced!&rdquo;", None, D24),
        ("2025/01.jpg", "string lights overhead, stalls along the walls, people already walking the floor", "starry night 2.0", D25),
        ("2025/02.jpg", "two friends under a ceiling of fairy lights and hanging stars", None, D25),
        ("2025/03.jpg", "the DJ at the decks, with the AquaTerra globe on the banner behind him", None, D25),
        ("2025/04.jpg", "hands up under the hanging stars, the whole floor lit blue", "hands up", D25),
    ])

# Per-photo no-go boxes, MEASURED off the v1 renders (canvas px = displayed px * 0.675):
#  cover   bystanders + phone + red shirt, right half, y 236-843
#  05      the vendor: head, hair, torso (a speech-bubble doodle landed on her sweater in v1)
#  2025/02 both heads and hair fill everything below the light band
JOB["extra_exclude"] = {
    "2024/01.jpg": [(0, 160, 620, 700), (540, 330, 540, 560), (50, 800, 980, 520)],  # DJ, bystanders, title block
    "2024/05.jpg": [(410, 580, 340, 640)],
    "2025/02.jpg": [(0, 215, 1080, 1135)],
}
# vision starved on these (netted sky / faces fill the frame): spots read off the v1 render
JOB["manual_spots"] = {
    "2024/03.jpg": [(690, 190, 52), (120, 300, 44), (800, 350, 60)],
    "2025/02.jpg": [(520, 150, 46), (700, 170, 44)],
}
