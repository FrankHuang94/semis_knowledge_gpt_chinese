#!/usr/bin/env python3
"""Generate a simple status inventory from Markdown front matter."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
items = []
for path in (ROOT / "docs").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^title:\s*(.+)$", text, re.M)
    status = re.search(r"^status:\s*(.+)$", text, re.M)
    if title:
        items.append((str(path.relative_to(ROOT / "docs")), title.group(1), status.group(1) if status else "unknown"))

out = ["# 内容状态索引", "", "| Path | Title | Status |", "|---|---|---|"]
out += [f"| `{path}` | {title} | {status} |" for path, title, status in sorted(items)]
(ROOT / "docs" / "generated_status.md").write_text("\n".join(out) + "\n", encoding="utf-8")
