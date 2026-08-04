import os, re, io

ROOT = r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE"
VAULT = os.path.join(ROOT, "AQ Design Engine")
BRAIN = os.path.join(ROOT, "brain")

def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)

def sanitize(name):
    name = name.replace("/", "-").replace("|", "-").replace(":", " -")
    name = re.sub(r'[\\\?\*"<>]', "", name)
    return name.strip()

claude = read(os.path.join(ROOT, "CLAUDE.md"))
decisions = read(os.path.join(BRAIN, "DECISIONS.md"))
recreation_audit = read(os.path.join(BRAIN, "RECREATION_AUDIT.md"))
recreation_progress = read(os.path.join(BRAIN, "RECREATION_PROGRESS.md"))

created = []  # (folder, filename) pairs for orphan check
def note(relpath, content):
    write(os.path.join(VAULT, relpath), content)
    created.append(relpath)

# ============================================================
# 1. MANUAL — split CLAUDE.md into 12 sections
# ============================================================
manual_titles = [
    (1, "The One Principle"),
    (2, "Two Workflows"),
    (3, "The Looking Gate"),
    (4, "Workflow A - Fresh Generation"),
    (5, "Workflow B - Reference Recreation"),
    (6, "The Bespoke Script"),
    (7, "The Gate Stack"),
    (8, "Encoding A Fix"),
    (9, "Brand Constants and Vocabulary"),
    (10, "The Bug Catalog"),
    (11, "Repo Map and Brain Docs"),
    (12, "Current State"),
]

# split on lines like "## 1. THE ONE PRINCIPLE ..."
pattern = re.compile(r"^## (\d+)\. (.+)$", re.M)
matches = list(pattern.finditer(claude))
sections = {}
for i, m in enumerate(matches):
    n = int(m.group(1))
    start = m.end()
    end = matches[i+1].start() if i+1 < len(matches) else len(claude)
    body = claude[start:end]
    # strip trailing "---" separators
    body = re.sub(r"\n---\s*$", "", body.strip())
    sections[n] = body.strip()

manual_filenames = {}
for n, title in manual_titles:
    fname = f"{n:02d} {title}"
    manual_filenames[n] = fname

see_also = {
    1: ["[[Taste]]"],
    2: ["[[03 The Looking Gate]]", "[[07 The Gate Stack]]"],
    3: ["[[Visual Review]]", "[[07 The Gate Stack]]"],
    4: ["[[07 The Gate Stack]]", "[[10 The Bug Catalog]]", "[[Engine State]]"],
    5: ["[[Recreations Index]]", "[[06 The Bespoke Script]]", "[[10 The Bug Catalog]]"],
    6: ["[[05 Workflow B - Reference Recreation]]", "[[07 The Gate Stack]]"],
    7: ["[[10 The Bug Catalog]]", "[[08 Encoding A Fix]]"],
    8: ["[[10 The Bug Catalog]]", "[[Decisions Index]]"],
    9: ["[[10 The Bug Catalog]]"],
    10: ["[[Bug Catalog Index]]", "[[Decisions Index]]"],
    11: ["[[Manual Index]]", "[[Decisions Index]]", "[[Recreations Index]]", "[[Bug Catalog Index]]"],
    12: ["[[Engine State]]", "[[Session Log]]"],
}

for n, title in manual_titles:
    body = sections.get(n, "*(content missing)*")
    see = "\n".join(f"- {l}" for l in see_also.get(n, []))
    content = f"# {n}. {title}\n\n{body}\n\n## See also\n{see}\n\n[[Manual Index]]\n"
    note(f"Manual/{manual_filenames[n]}.md", content)

manual_index = "# Manual Index\n\nThe 12 sections of the AQ Poster Engine operating manual (CLAUDE.md), one note per section.\n\n"
for n, title in manual_titles:
    manual_index += f"{n}. [[{manual_filenames[n]}|{title}]]\n"
manual_index += "\n[[Home]]\n"
note("Manual/Manual Index.md", manual_index)

# ============================================================
# 2. BUG CATALOG — split CLAUDE.md section 10 table into atomic notes
# ============================================================
bug_rows = [
    ("Element clips off-canvas", "6, 9, 10", "`layout.bounds_check`"),
    ("Doodle-badge dropped over text or shape", "26, 27, 32", "`layout.collision_check`"),
    ("Shape fill equals page bg (invisible)", "21", "`layout.invisible_color_check`"),
    ("Text stroke approx equals bg (invisible outline)", "24", "`layout.invisible_color_check`"),
    ("var(--typo) undefined renders transparent", "32", "`layout.css_var_check` (auto in `render`)"),
    ("Text overflows a star or burst's narrow waist", "19, 44", "`layout.star_text_width`"),
    ("Hero scaled far too small vs the reference", "42", "`layout.dominance_check` (opt-in)"),
    ("Wide bottom-anchored child in rotated overflow parent renders blank", "7", "`layout.antipattern_scan` (manual) + rule: anchor wide content with `top:`"),
    ("Stale bbox tuple hides a real off-canvas or collision", "6", "discipline: update `elements.append` whenever you move CSS"),
    ("Dead half the reference fills", "15, 25, 30, 31, 39", "`preview.critique` dead_quadrant/sparse + \"scale up before filler\""),
    ("One flat color floods the field", "(batch)", "`preview.critique` flat_dominant (>52%)"),
    ("Cramming a pile into one corner starves other quadrants", "87525f70", "`layout.quadrant_fill_check` (overlap LOCAL, fill GLOBAL)"),
]

# slug -> sample number, from RECREATION_PROGRESS.md
prog_rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([0-9a-f]+)\.jpg", recreation_progress, re.M)
slug_to_num = {slug[:8]: int(num) for num, slug in prog_rows}

def sample_link(numstr):
    numstr = numstr.strip()
    if numstr.isdigit():
        n = int(numstr)
        return f"[[Sample {n:02d}]]"
    # slug form
    for slug, n in slug_to_num.items():
        if numstr.startswith(slug) or slug.startswith(numstr[:8]):
            return f"[[Sample {n:02d}]]"
    return None

bug_filenames = []
for title, seen_in, guard in bug_rows:
    fname = sanitize(title)
    bug_filenames.append((fname, title, seen_in, guard))

for fname, title, seen_in, guard in bug_filenames:
    links = []
    for part in seen_in.replace("(batch)", "").split(","):
        part = part.strip()
        if not part:
            continue
        l = sample_link(part)
        if l:
            links.append(l)
    links_txt = ", ".join(links) if links else "(no individual samples logged — a cross-batch finding)"
    content = f"""# {title}

**Seen in:** {seen_in}

**Encoded guard:** {guard}

This failure class was caught by eye during the 44-sample Workflow B recreation pass and is now
guarded by an automated rule in `engine/layout.py` (or `engine/preview.py` / `engine/build.py` as
noted), per the "encode the fix" loop in [[08 Encoding A Fix]].

## Samples where this was seen
{links_txt}

## See also
- [[10 The Bug Catalog]]
- [[Bug Catalog Index]]
"""
    note(f"Bug Catalog/{fname}.md", content)

# fold in the collision auto-nudge paragraph (not a table row, but directly related) into the
# "Doodle-badge dropped over text or shape" note
nudge_para = """

## Update — collision auto-nudge (session 9)
Collision AUTO-nudge is now encoded: `layout.collision_nudge` repositions the later-placed
element of a colliding pair away from the earlier (anchor) one, opt-in via
`preflight(..., auto_nudge=True)`. Self-test: `scratchpad/test_collision_nudge.py`. See
[[Collision auto-nudge (session 9)]] in the Decisions log for the full story.
"""
p = os.path.join(VAULT, "Bug Catalog", "Doodle-badge dropped over text or shape.md")
write(p, read(p) + nudge_para)

bug_index = "# Bug Catalog Index\n\nEvery recurring visual failure class caught during the 44-sample Workflow B pass, now guarded by an encoded rule. See [[10 The Bug Catalog]] for the source table.\n\n"
for fname, title, seen_in, guard in bug_filenames:
    bug_index += f"- [[{fname}|{title}]] — seen in {seen_in}\n"
bug_index += "\n[[Home]]\n"
note("Bug Catalog/Bug Catalog Index.md", bug_index)

print("Manual + Bug Catalog done:", len(manual_titles), len(bug_filenames))
