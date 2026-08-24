#!/usr/bin/env python3
"""Validate required freshness and source labels in Markdown front matter."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PRODUCT_MARKERS = ("product_status:", "last_verified:", "source_date:")
LABELS = ("[Primary Source]", "[Independent]", "[Vendor Claim]", "[Estimate]", "[Inference]")

errors = []
for path in DOCS.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if "product_status:" in text:
        for marker in PRODUCT_MARKERS:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing {marker}")
    for match in re.finditer(r"\b\d+(?:\.\d+)?\s*(?:TB/s|GB/s|Gbps|Tbps|W|kW|MW|PFLOPS|TFLOPS)\b", text):
        paragraph = text[max(0, match.start()-400):match.end()+400]
        if not any(label in paragraph for label in LABELS):
            errors.append(f"{path.relative_to(ROOT)}: unlabeled quantitative claim near '{match.group(0)}'")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("source validation passed")
