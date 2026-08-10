"""Zip a Claude Code skill directory for distribution.

Excludes __pycache__, .pyc and any local cache dirs so the archive is exactly the skill.
Paths inside the zip are forward-slashed and rooted at the skill folder, so it unpacks
straight into .claude/skills/.
"""
import os, sys, zipfile

SKILLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "skills")
SKIP_DIRS = {"__pycache__", ".drive_cache", ".git"}
SKIP_EXT = (".pyc", ".zip")


def pack(name, dest):
    root = os.path.normpath(os.path.join(SKILLS, name))
    if not os.path.isdir(root):
        raise SystemExit(f"no such skill: {root}")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    n = 0
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in SKIP_DIRS]
            for f in sorted(fn):
                if f.endswith(SKIP_EXT):
                    continue
                full = os.path.join(dp, f)
                arc = os.path.relpath(full, os.path.dirname(root)).replace(os.sep, "/")
                z.write(full, arc)
                n += 1
    print(f"wrote {dest}\n{n} files, {os.path.getsize(dest)/1024:.1f} KB")
    with zipfile.ZipFile(dest) as z:
        for i in z.namelist():
            print("  ", i)
    return dest


if __name__ == "__main__":
    pack(sys.argv[1], sys.argv[2])
