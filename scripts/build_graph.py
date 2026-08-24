#!/usr/bin/env python3
"""Validate concept references and emit Mermaid edges."""
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
data = yaml.safe_load((ROOT / "data" / "concepts.yaml").read_text(encoding="utf-8"))
concepts = data.get("concepts", [])
ids = {item["id"] for item in concepts}
edges = []
errors = []
for item in concepts:
    for neighbor in item.get("connected_to", []):
        if neighbor in ids:
            edges.append((item["id"], neighbor))
    for article in item.get("articles", []):
        if not (ROOT / article).exists():
            errors.append(f'{item["id"]}: missing article {article}')

if errors:
    print("\n".join(errors))
    sys.exit(1)

lines = ["flowchart LR"]
lines += [f"    {a} --> {b}" for a, b in sorted(set(edges))]
print("\n".join(lines))
