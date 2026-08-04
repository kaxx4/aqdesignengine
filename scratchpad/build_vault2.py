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

recreation_audit = read(os.path.join(BRAIN, "RECREATION_AUDIT.md"))
recreation_progress = read(os.path.join(BRAIN, "RECREATION_PROGRESS.md"))

# ---- parse progress table: # | file | status | notes ----
prog = {}
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([0-9a-f]+\.jpg)\s*\|\s*([^\|]+)\|\s*(.*?)\s*\|$", recreation_progress, re.M):
    num = int(m.group(1))
    fname = m.group(2)
    status = m.group(3).strip()
    notetxt = m.group(4).strip()
    prog[num] = (fname, status, notetxt)

# ---- top summary table rows (samples 1,2,3) from the revisit tracker at top of RECREATION_AUDIT.md ----
top_table = {}
for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*([0-9a-f]+\.jpg)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|$", recreation_audit, re.M):
    num = int(m.group(1))
    if num in (1, 2, 3, 40):
        top_table[num] = {"file": m.group(2), "miss": m.group(3), "revisit": m.group(4)}

# ---- sequential "## Sample N — full composition description" sections (N=3..44) ----
sec_pattern = re.compile(r"^## Sample (\d+)( — full composition description.*)?$", re.M)
matches = list(sec_pattern.finditer(recreation_audit))
sample_sections = {}  # num -> list of (start,end) body text chunks (append, since 1 and 40 appear twice)
for i, m in enumerate(matches):
    n = int(m.group(1))
    start = m.end()
    end = matches[i+1].start() if i+1 < len(matches) else len(recreation_audit)
    body = recreation_audit[start:end].strip()
    sample_sections.setdefault(n, []).append(body)

# Sample filenames -> numbers, from progress table
sample_num_by_file = {v[0]: k for k, v in prog.items()}

recreations_index = "# Recreations Index\n\n"
recreations_index += "Every reference poster recreated during the Workflow B \"training\" pass. Full protocol: [[05 Workflow B - Reference Recreation]].\n\n"
recreations_index += "| # | Subject | Status | Note |\n|---|---|---|---|\n"

for n in range(1, 45):
    fname, status, notetxt = prog.get(n, ("(unknown)", "unknown", ""))
    bodies = sample_sections.get(n, [])
    body_txt = "\n\n---\n\n".join(bodies) if bodies else ""
    top = top_table.get(n)

    parts = []
    parts.append(f"# Sample {n:02d}\n")
    parts.append(f"**Reference file:** `{fname}`\n")
    if top:
        parts.append(f"**Original miss (revisit tracker):** {top['miss']}\n\n**Revisit status:** {top['revisit']}\n")
    if body_txt:
        parts.append("## Composition description & outcome\n\n" + body_txt + "\n")
    else:
        parts.append("*(No standalone composition-description section was written for this sample beyond the revisit-tracker summary above.)*\n")

    parts.append(f"## Status\n{status} — {notetxt}\n")

    # forward links to bug catalog notes whose "seen in" list includes this sample number
    bug_seen_map = {
        "Element clips off-canvas.md": [6, 9, 10],
        "Doodle-badge dropped over text or shape.md": [26, 27, 32],
        "Shape fill equals page bg (invisible).md": [21],
        "Text stroke approx equals bg (invisible outline).md": [24],
        "var(--typo) undefined renders transparent.md": [32],
        "Text overflows a star or burst's narrow waist.md": [19, 44],
        "Hero scaled far too small vs the reference.md": [42],
        "Wide bottom-anchored child in rotated overflow parent renders blank.md": [7],
        "Stale bbox tuple hides a real off-canvas or collision.md": [6],
        "Dead half the reference fills.md": [15, 25, 30, 31, 39],
    }
    fwd = []
    for bugfile, nums in bug_seen_map.items():
        if n in nums:
            title = bugfile[:-3]
            fwd.append(f"[[{title}]]")
    if n == 1:
        fwd.append("[[Cramming a pile into one corner starves other quadrants]]")

    see = "\n".join(f"- {l}" for l in fwd) if fwd else "- (none logged)"
    parts.append(f"## See also\n- [[Recreations Index]]\n{see}\n")

    write(os.path.join(VAULT, "Recreations", f"Sample {n:02d}.md"), "\n".join(parts))

    subject = notetxt.split(".")[0][:70] if notetxt else (top["miss"][:70] if top else "")
    recreations_index += f"| {n:02d} | {subject} | {status} | [[Sample {n:02d}]] |\n"

recreations_index += "\n[[Home]]\n"
write(os.path.join(VAULT, "Recreations", "Recreations Index.md"), recreations_index)

print("Recreations done: 44 sample notes")
