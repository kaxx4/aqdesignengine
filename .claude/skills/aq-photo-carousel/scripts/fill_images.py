"""Fill the empty image / alt / label columns of the 2026 workshop rows from the downloaded
Drive photos.

CONSTRAINT THAT SHAPES EVERYTHING: those columns hold PUBLIC SUPABASE STORAGE URLs on project
`hzowuwffjqtgszecngpe`, which this machine has no credentials for. So this script cannot upload.
What it does instead:
  1. stages the chosen photos under out/CSV_IMAGE_FILL/upload/ with their final object names,
  2. writes the CSV with the URLs those objects WILL have once uploaded,
  3. emits upload_to_supabase.py + patch.sql so the operator can run the two write steps.
Nothing is written to any remote service from here.

Only EMPTY cells are filled. An existing main_image or image_N is never overwritten.
"""
import csv, json, os, shutil

os.chdir(r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE")
SRC_CSV = r"C:\Users\kanis\Downloads\welfare_projects_rows.csv"
OUT = "out/CSV_IMAGE_FILL"
PHOTOS = "scratchpad/carousel_2026"
BUCKET = "project-images"
BASE_URL = f"https://hzowuwffjqtgszecngpe.supabase.co/storage/v1/object/public/{BUCKET}/"
PREFIX = "welfare/2026/"

# (photo_file, alt_text, label) — alt text written from actually looking at each photo.
PLAN = {
    # ── row id: (event slug used for object names, photo dir, [picks])
    "1006": ("build-a-sentence-disha", "disha_grammar", [
        ("15.jpg", "Two girls sitting together on the classroom floor during the grammar session", "in the room"),
        ("09.jpg", "A girl working through a subjects-and-predicates worksheet on the floor", "worksheet"),
        ("21.jpg", "A student answering out loud in front of the class", "answering"),
        ("08.jpg", "An AquaTerra volunteer explaining an example to the class", "volunteers"),
        ("27.jpg", "A volunteer kneeling at floor level to help a student", "one to one"),
    ]),
    "1008": ("learners-den-pather-saathi", "learners_den_art", [
        ("26.jpg", "The full group of children and volunteers at the end of the session", "the full group"),
        ("06.jpg", "A girl holding up her drawing of the earth with a flag and balloons", "held up"),
        ("12.jpg", "A girl holding a clipboard with her drawing of a castle in crayon", "a castle"),
        ("04.jpg", "A volunteer holding up a portrait a child drew of her", "portrait"),
        ("10.jpg", "Children holding their finished drawings up towards the camera", "everyone's page"),
    ]),
    "1010": ("valentines-cards-pather-saathi", "valentines_cards", [
        ("16.jpg", "Three girls holding up the Valentine's cards they made", "cards by hand"),
        ("05.jpg", "A girl holding a card with a flower drawn in five colours", "a flower"),
        ("06.jpg", "A card showing four hearts on a string, outlined in red marker", "four hearts"),
        ("13.jpg", "Two girls holding up their finished Valentine's cards", "two cards"),
        ("15.jpg", "A girl holding a paper heart covered corner to corner in drawing", "a paper heart"),
    ]),
    "1597": ("teaching-english-ektara", "teaching_english", [
        ("00.jpg", "A volunteer with a group of students after the English class", "after class"),
        ("03.jpg", "The whole class photographed at the end of the lesson", "15 kids"),
        ("01.jpg", "Students packing up their bags after the session", "packing up"),
        ("02.jpg", "A volunteer and a student at the end of the class", "one more"),
    ]),
    "1598": ("teaching-internship-ektara", "teaching_internship", [
        ("00.jpg", "A classroom of students at their desks during the teaching internship", "the classroom"),
        ("01.jpg", "Students at their desks turning towards the camera mid-session", "mid-session"),
        ("02.jpg", "Students working at their desks during the session", "at work"),
    ]),
    "1599": ("mothers-day-disha", "mothers_day", [
        ("09.jpg", "Two children colouring Mother's Day cards at a low table", "card making"),
        ("15.jpg", "Crayons out, a flower being drawn on the front of a card", "flowers"),
        ("16.jpg", "A child drawing a heart in green pen on a card", "a heart"),
        ("05.jpg", "Finished Mother's Day cards laid out with crayons", "16 cards made"),
        ("21.jpg", "Children eating pizza after finishing their cards", "afterwards"),
    ]),
    "1610": ("smile-notes-bhawanipore", "smile_notes_bhawanipore", [
        ("12.jpg", "A tray of handwritten affirmation notes with toffees", "100 notes"),
        ("02.jpg", "A man reading the note he was handed", "reading it"),
        ("01.jpg", "A security guard receiving a note and a toffee on his shift", "on shift"),
        ("09.jpg", "A man taking a note and a toffee with both hands", "one each"),
        ("14.jpg", "A stall owner with the note left with him", "at the stall"),
    ]),
    "1611": ("smile-notes-mba-chaiwala", "smile_notes_mba", [
        ("03.jpg", "A young girl holding the note she was given", "her note"),
        ("00.jpg", "A note handed over at a roadside stall between orders", "at the stall"),
        ("01.jpg", "A small child standing and reading the note she was handed", "reading it"),
        # 02.jpg deliberately omitted: it is the same child in the same pose as 01.jpg a moment
        # later. This folder only holds 4 photos and two of them are that near-duplicate, so
        # image_4 is left EMPTY rather than publishing the same frame twice.
    ]),
    "1616": ("smile-notes-lake-town-footbridge", "smile_notes_laketown", [
        ("01.jpg", "A volunteer with a man who has just been handed a note", "handed over"),
        ("00.jpg", "A note passed across a shop counter mid-shift", "mid-shift"),
        ("02.jpg", "A volunteer with a rickshaw driver holding his note", "one at a time"),
        ("03.jpg", "The six volunteers together before the notes ran out", "six volunteers"),
        ("04.jpg", "The group outside the restaurant at the end of the drive", "the group"),
    ]),
    "1005": ("sentence-secrets-ek-tara", "sentence_secrets_ektara", [
        ("00.jpg", "Two volunteers with students in the Ek Tara classroom during the grammar session",
         "the session"),
    ]),
}

# Rows deliberately NOT filled, with the reason recorded in the report.
SKIP = {
    "1004": "Menstrual Awareness 04-06 — Drive folder is shared by three CSV rows and holds at "
            "least two unrelated sessions; no photo can be honestly attributed to this row.",
    "1591": "Menstrual Awareness 04-05 — same shared/ambiguous folder as row 1004.",
    "1594": "Digital Safety 05-16 — Drive folder requires sign-in; no photos retrievable.",
    "1617": "Digital Safety 05-16 (duplicate row) — same, and a duplicate of 1594.",
    "1603": "Valentine's 02-08 (duplicate row) — same event as 1010, which is being filled. "
            "Filling both would duplicate the images; delete this row instead.",
    "1609": "Learner's Den 06-04 — already has 5 images, and its Drive link points at the shared "
            "folder, so its true source is unverified. Left untouched.",
    "1614": "Teaching English 04-25 (duplicate row) — already has 4 images; 1597 is the row with "
            "the Drive link and is being filled.",
    "1615": "Mother's Day 09-05 — already has 4 images; also the suspected day/month swap of "
            "1599, which is being filled.",
}

COLS = [("main_image", "main_image_alt", None)] + \
       [(f"image_{i}", f"image_{i}_alt", f"label_{i}") for i in (1, 2, 3, 4)]


def main():
    rows = list(csv.DictReader(open(SRC_CSV, encoding="utf-8")))
    fieldnames = list(rows[0].keys())
    os.makedirs(f"{OUT}/upload", exist_ok=True)

    staged, patches, report = [], [], []
    for r in rows:
        rid = r["id"]
        if rid not in PLAN:
            continue
        ev, photodir, picks = PLAN[rid]
        changed = {}
        for (imgc, altc, labc), (fn, alt, lab) in zip(COLS, picks):
            if (r.get(imgc) or "").strip():
                continue                       # never overwrite an existing image
            obj = f"{PREFIX}{ev}-{imgc}.jpg"
            src = f"{PHOTOS}/{photodir}/src_images/{fn}"
            if not os.path.exists(src):
                report.append(f"MISSING SOURCE {src}")
                continue
            dst = f"{OUT}/upload/{obj.replace('/', '__')}"
            shutil.copy(src, dst)
            staged.append((obj, os.path.basename(dst)))
            changed[imgc] = BASE_URL + obj
            if altc and not (r.get(altc) or "").strip():
                changed[altc] = alt
            if labc and not (r.get(labc) or "").strip():
                changed[labc] = lab
        if changed:
            r.update(changed)
            patches.append((rid, changed))
            report.append(f"row {rid} ({ev}): filled {len([k for k in changed if k.startswith(('main_image','image_')) and not k.endswith('_alt')])} image slots")

    # 1. full CSV, drop-in replacement
    with open(f"{OUT}/welfare_projects_rows_FILLED.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # 2. patch SQL.
    # Each column is written as COALESCE(NULLIF(col,''), 'new') so the statement is IDEMPOTENT
    # and physically cannot overwrite a cell that is non-empty at run time — including one
    # somebody filled in between this export and the run. Re-running it is a no-op.
    with open(f"{OUT}/patch.sql", "w", encoding="utf-8") as f:
        f.write("-- AQ 2026 workshop image backfill.\n"
                "-- Every assignment is COALESCE-guarded: it fills ONLY still-empty cells and is\n"
                "-- safe to re-run. Run AFTER upload_to_supabase.py or the URLs will 404.\n"
                "-- TABLE NAME ASSUMED from the export filename; change it if yours differs.\n\n"
                "BEGIN;\n\n")
        for rid, ch in patches:
            sets = ",\n    ".join(
                f"{k} = COALESCE(NULLIF({k}, ''), '{v.replace(chr(39), chr(39) * 2)}')"
                for k, v in ch.items())
            f.write(f"UPDATE welfare_projects SET\n    {sets}\nWHERE id = {rid};\n\n")
        f.write("COMMIT;\n")

    # 3. the uploader the operator runs with their own key
    with open(f"{OUT}/upload_to_supabase.py", "w", encoding="utf-8") as f:
        f.write(UPLOADER)
    json.dump([{"object": o, "file": fn} for o, fn in staged],
              open(f"{OUT}/manifest.json", "w"), indent=1)

    print("\n".join(report))
    print(f"\nstaged {len(staged)} files -> {OUT}/upload/")
    print(f"patched {len(patches)} rows")


UPLOADER = '''"""Upload the staged photos to Supabase Storage, then the CSV/SQL URLs resolve.

Run from this directory:
    pip install supabase
    set SUPABASE_URL=https://hzowuwffjqtgszecngpe.supabase.co
    set SUPABASE_SERVICE_KEY=<service_role key>
    python upload_to_supabase.py

Use a SERVICE ROLE key (anon usually cannot write to storage). Do not commit the key.
"""
import json, os, sys
from supabase import create_client

URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_SERVICE_KEY")
if not URL or not KEY:
    sys.exit("set SUPABASE_URL and SUPABASE_SERVICE_KEY first")

sb = create_client(URL, KEY)
manifest = json.load(open("manifest.json"))
ok = 0
for m in manifest:
    with open(os.path.join("upload", m["file"]), "rb") as fh:
        data = fh.read()
    try:
        sb.storage.from_("project-images").upload(
            m["object"], data,
            {"content-type": "image/jpeg", "upsert": "false"})   # never clobber an existing object
        print("uploaded", m["object"])
        ok += 1
    except Exception as e:
        print("SKIP", m["object"], e)
print(f"\\n{ok}/{len(manifest)} uploaded. Now run patch.sql.")
'''


if __name__ == "__main__":
    main()
