import os, re, io

VAULT = r"C:\Users\kanis\Desktop\AquaTerra\AQ_POSTER_ENGINE\AQ_CODEBASE\AQ Design Engine"

files = {}
for root, dirs, fs in os.walk(VAULT):
    for f in fs:
        if f.endswith(".md"):
            name = f[:-3]
            files[name] = os.path.join(root, f)

all_text = ""
for name, path in files.items():
    with io.open(path, encoding="utf-8") as fh:
        all_text += fh.read() + "\n"

link_pattern = re.compile(r"\[\[([^\]|]+)(\|[^\]]+)?\]\]")
linked = set()
for m in link_pattern.finditer(all_text):
    linked.add(m.group(1).strip())

orphans = []
for name in files:
    if name == "Home":
        continue
    # count occurrences of this note being linked FROM any file OTHER than itself
    count_elsewhere = 0
    for other_name, other_path in files.items():
        if other_name == name:
            continue
        with io.open(other_path, encoding="utf-8") as fh:
            txt = fh.read()
        if f"[[{name}]]" in txt or f"[[{name}|" in txt:
            count_elsewhere += 1
    if count_elsewhere == 0:
        orphans.append(name)

print("Total notes:", len(files))
print("Orphans:", len(orphans))
for o in orphans:
    print(" -", o, "=>", files[o])
