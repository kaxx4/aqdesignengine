"""Per-drive content for build_drives.py. ALL facts come from drives.json (title, copy, location,
volunteers). Captions describe what is visible in the photo they sit on (CAROUSEL_PLAYBOOK 5), and
no caption states a number, name or date that is not in the JSON. Body copy lowercase, no em dashes.

photo spec: file, fit ("cover"|"band"), focus (cx, cy centering for cover), cap, exclude (measured boxes).
"""
HT = "#aquaterra #kolkata #studentvolunteers"

DRIVES = [
 dict(post_id=876, slug="sharbat_northern_park", seed=1, loc="Northern Park, Kolkata", volunteers=2,
      title_html="SHARBAT<br>DRIVE",
      subhead="distributing sharbat and receiving smiles. volunteers distributed sharbat to kids around them.",
      cover=dict(file="p0.jpg", focus=(0.5, 0.3)),
      slides=[dict(file="p1.jpg", focus=(0.5, 0.3), cap="two cups raised, right in the middle of the park"),
              dict(file="p2.jpg", focus=(0.5, 0.4), cap="a cup handed to a kid on a bicycle")],
      caption=f"""distributing sharbat and receiving smiles in northern park.
2 volunteers, a stack of cups, and kids from around the park.
{HT} #sharbatdrive #welfare"""),
 dict(post_id=877, slug="sharbat_momo_aunty_bangur", seed=2, loc="Momo Aunty, Bangur", volunteers=2,
      title_html="SHARBAT<br>DISTRIBUTION",
      subhead="volunteers distributed 4.5L of sharbat to people around.",
      cover=dict(file="p1.jpg", focus=(0.5, 0.4)),
      slides=[dict(file="p0.jpg", focus=(0.5, 0.5), cap="the sharbat jar, with bottles lined up beside it"),
              dict(file="p2.jpg", focus=(0.5, 0.4), cap="cups going out, one at a time"),
              dict(file="p3.jpg", focus=(0.5, 0.4), cap="everyone leaning in to pour",
                   exclude=[(560, 60, 520, 420), (0, 0, 200, 420)])],
      caption=f"""volunteers distributed 4.5L of sharbat to people around momo aunty, bangur.
2 volunteers, one big jar, a lot of cups.
{HT} #sharbatdrive #welfare"""),
 dict(post_id=878, slug="dog_drive_jatindas_park", seed=3, loc="Jatindas Park, Kolkata", volunteers=4,
      title_html="DOG DRIVE<br>JATINDAS PARK",
      subhead="4 volunteers went to jatindas and fed dogs with biscuits and had fun.",
      cover=dict(file="p2.jpg", focus=(0.5, 0.45)),
      slides=[dict(file="p0.jpg", focus=(0.5, 0.7), cap="lunch, on the pavement"),
              dict(file="p3.jpg", focus=(0.5, 0.56), cap="a hand held out, a nose lifted, a biscuit on its way")],
      caption=f"""4 volunteers went to jatindas park, fed dogs with biscuits and had fun.
nobody there was in a hurry.
{HT} #dogdrive #welfare"""),
 dict(post_id=901, slug="subject_predicate_ektara", seed=4, loc="Ektara Foundation", volunteers=7,
      title_html="SUBJECT-PREDICATE<br>WORKSHOP",
      subhead="volunteers taught children english grammar and made it fun so kids actually understand and learn easily.",
      cover=dict(file="p0.jpg", focus=(0.5, 0.7)),
      slides=[dict(file="p1.jpg", focus=(0.4, 0.5), cap="a volunteer talking the students through it")],
      caption=f"""subject-predicate workshop at ektara foundation.
7 volunteers taught english grammar and made it fun, so it actually sticks.
{HT} #grammarworkshop #welfare #education"""),
 dict(post_id=902, slug="grammar_disha", seed=5, loc="Disha Foundation", volunteers=4,
      title_html="GRAMMAR<br>WORKSHOP",
      subhead="volunteers taught children basic grammar like subject-predicate rules.",
      cover=dict(file="p0.jpg", fit="band"),
      slides=[dict(file="p1.jpg", fit="band", cap="two volunteers up front, the class settled on the floor"),
              dict(file="p2.jpg", fit="band", cap="three students, smiling for the camera")],
      caption=f"""grammar workshop at disha foundation.
4 volunteers, basic grammar, subject-predicate rules.
{HT} #grammarworkshop #welfare #education"""),
 dict(post_id=903, slug="teaching_internship_disha", seed=6, loc="Disha Foundation", volunteers=4,
      title_html="TEACHING<br>INTERNSHIP",
      subhead="volunteers taught kids various things over 4 days, including english grammar. a great learning experience for both sides.",
      cover=dict(file="p3.jpg", focus=(0.5, 0.4)),
      slides=[dict(file="p1.jpg", focus=(0.3, 0.5), cap="a volunteer mid-explanation, the whole class watching"),
              dict(file="p2.jpg", focus=(0.5, 0.6), cap="heads down over worksheets, on the floor"),
              dict(file="p0.jpg", focus=(0.4, 0.5), cap="chalk on the board, a volunteer pointing at it")],
      caption=f"""teaching internship at disha foundation, fun only.
4 volunteers taught kids various things over 4 days, english grammar included.
a great learning experience for both sides.
{HT} #teachinginternship #welfare #education"""),
 dict(post_id=904, slug="dog_feeding_natural_city", seed=7, loc="Natural City", volunteers=10,
      title_html="DOG FEEDING<br>DRIVE",
      subhead="volunteers fed dogs around the venue with biscuits.",
      cover=dict(file="p1.jpg", focus=(0.5, 0.4)),
      slides=[dict(file="p2.jpg", focus=(0.5, 0.4), cap="two dogs, both very interested in the biscuits"),
              dict(file="p0.jpg", focus=(0.5, 0.5), cap="a biscuit offered, politely accepted")],
      caption=f"""10 volunteers fed dogs around the venue at natural city with biscuits.
the dogs were thrilled. the volunteers were too.
{HT} #dogfeeding #welfare"""),
 dict(post_id=905, slug="rakhi_tangra", seed=8, loc="Tangra", volunteers=4,
      title_html="RAKHI<br>DISTRIBUTION",
      subhead="volunteers went around and distributed rakhis to several passers-by.",
      cover=dict(file="p0.jpg", focus=(0.5, 0.4)),
      slides=[dict(file="p2.jpg", focus=(0.5, 0.4), cap="a rakhi on the wrist of someone passing by"),
              dict(file="p1.jpg", focus=(0.5, 0.4), cap="after dark, one more wrist")],
      caption=f"""rakhi distribution at tangra.
4 volunteers went around and tied rakhis on several passers-by.
{HT} #rakhi #welfare"""),
 dict(post_id=906, slug="momo_aunty_sunset", seed=9, loc="Momo Aunty", volunteers=5,
      title_html="MOMO AUNTY<br>AND A SUNSET",
      subhead="volunteers went to momo aunty and came across a pretty sunset while volunteering.",
      cover=dict(file="p0.jpg", fit="band"),
      slides=[dict(file="p1.jpg", focus=(0.5, 0.5), cap="a cup handed across the counter")],
      caption=f"""5 volunteers went to momo aunty and came across a pretty sunset while volunteering.
a good evening, honestly.
{HT} #welfare #sunset"""),
]
