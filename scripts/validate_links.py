#!/usr/bin/env python3
"""Check relative Markdown links without requiring network access."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for raw in pattern.findall(text):
        target = raw.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (path.parent / unquote(target)).resolve()
        if not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)} -> {target}")

if errors:
    print("Broken links:")
    print("\n".join(errors))
    sys.exit(1)
print("link validation passed")
