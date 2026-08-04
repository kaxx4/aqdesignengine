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

# ============================================================
# BRAIN — one note per remaining brain doc
# ============================================================
brain_docs = [
    ("TASTE.md", "Taste", ["[[01 The One Principle]]"]),
    ("ENGINE.md", "Engine", ["[[04 Workflow A - Fresh Generation]]", "[[07 The Gate Stack]]"]),
    ("ENGINE_STATE.md", "Engine State", ["[[12 Current State]]", "[[04 Workflow A - Fresh Generation]]"]),
    ("VISUAL_REVIEW.md", "Visual Review", ["[[03 The Looking Gate]]"]),
    ("AUDIT.md", "Audit", ["[[07 The Gate Stack]]"]),
    ("INSPIRATION.md", "Inspiration", ["[[09 Brand Constants and Vocabulary]]", "[[Recreations Index]]"]),
    ("SESSION_LOG.md", "Session Log", ["[[12 Current State]]", "[[Decisions Index]]"]),
]

for fname, title, links in brain_docs:
    body = read(os.path.join(BRAIN, fname)).strip()
    see = "\n".join(f"- {l}" for l in links)
    content = f"{body}\n\n## See also\n{see}\n\n[[Home]]\n"
    write(os.path.join(VAULT, "Brain", f"{title}.md"), content)

print("Brain docs done:", len(brain_docs))

# ============================================================
# DECISIONS — split brain/DECISIONS.md into one note per "## " entry
# ============================================================
decisions = read(os.path.join(BRAIN, "DECISIONS.md"))
pattern = re.compile(r"^## (.+)$", re.M)
matches = list(pattern.finditer(decisions))
entries = []
for i, m in enumerate(matches):
    title = m.group(1).strip()
    start = m.end()
    end = matches[i+1].start() if i+1 < len(matches) else len(decisions)
    body = decisions[start:end].strip()
    entries.append((title, body))

# simple keyword -> forward link map
keyword_links = [
    ("collision", "[[Doodle-badge dropped over text or shape]]"),
    ("flat_dominant", "[[One flat color floods the field]]"),
    ("css_var", "[[var(--typo) undefined renders transparent]]"),
    ("invisible_color", "[[Shape fill equals page bg (invisible)]]"),
    ("star_text_width", "[[Text overflows a star or burst's narrow waist]]"),
    ("dominance_check", "[[Hero scaled far too small vs the reference]]"),
    ("bounds_check", "[[Element clips off-canvas]]"),
    ("quadrant_fill_check", "[[Cramming a pile into one corner starves other quadrants]]"),
    ("bespoke", "[[06 The Bespoke Script]]"),
    ("stacked_zones", "[[04 Workflow A - Fresh Generation]]"),
    ("number_hero", "[[04 Workflow A - Fresh Generation]]"),
    ("giant_type", "[[04 Workflow A - Fresh Generation]]"),
    ("looking gate", "[[03 The Looking Gate]]"),
    ("eye candy", "[[09 Brand Constants and Vocabulary]]"),
    ("halftone", "[[09 Brand Constants and Vocabulary]]"),
    ("preflight", "[[07 The Gate Stack]]"),
]

decisions_index = "# Decisions Index\n\nStanding rulings from `brain/DECISIONS.md`, in source-file order. Read before generating.\n\n"

for title, body in entries:
    fname = sanitize(title)
    lowered = (title + " " + body).lower()
    fwd = []
    for kw, link in keyword_links:
        if kw in lowered and link not in fwd:
            fwd.append(link)
    fwd_txt = "\n".join(f"- {l}" for l in fwd) if fwd else "- (no direct cross-link identified)"
    content = f"# {title}\n\n{body}\n\n## See also\n- [[Decisions Index]]\n{fwd_txt}\n"
    write(os.path.join(VAULT, "Brain", "Decisions", f"{fname}.md"), content)
    decisions_index += f"- [[{fname}|{title}]]\n"

decisions_index += "\n[[Home]]\n"
write(os.path.join(VAULT, "Brain", "Decisions", "Decisions Index.md"), decisions_index)

print("Decisions entries done:", len(entries))
