#!/usr/bin/env python3
"""Enforce repository-wide explanatory-content floors.

The body metric excludes navigation index pages and authoring templates so the
minimum cannot be satisfied by menus, generated lists, or scaffolding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path("docs")
MIN_BODY_HAN = 300_000
MIN_BODY_ARTICLES = 96
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def is_body_article(path: Path) -> bool:
    return (
        path.suffix == ".md"
        and path.name != "index.md"
        and "_templates" not in path.parts
    )


def count_han(text: str) -> int:
    return len(HAN_RE.findall(text))


def main() -> int:
    all_markdown = sorted(DOCS.rglob("*.md"))
    body_articles = [path for path in all_markdown if is_body_article(path)]
    body_counts = {
        path.as_posix(): count_han(path.read_text(encoding="utf-8"))
        for path in body_articles
    }
    all_han = sum(
        count_han(path.read_text(encoding="utf-8")) for path in all_markdown
    )
    body_han = sum(body_counts.values())

    print(
        f"content metrics: {len(body_articles)} body articles, "
        f"{body_han:,} body Han characters, {all_han:,} Han characters in all docs"
    )

    failures: list[str] = []
    if len(body_articles) < MIN_BODY_ARTICLES:
        failures.append(
            f"body article count {len(body_articles)} is below {MIN_BODY_ARTICLES}"
        )
    if body_han < MIN_BODY_HAN:
        failures.append(
            f"body Han count {body_han:,} is below {MIN_BODY_HAN:,}"
        )

    empty = [path for path, count in body_counts.items() if count == 0]
    if empty:
        failures.append("body articles without Han text: " + ", ".join(empty))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
