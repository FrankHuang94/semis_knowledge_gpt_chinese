#!/usr/bin/env python3
"""Render data/glossary.csv into a Markdown reference table."""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "glossary.csv"
target = ROOT / "docs" / "31_glossary" / "generated.md"

with source.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

lines = ["# Glossary（自动生成）", "", "Glossary 是查询入口，不替代核心文章。", "",
         "| 术语 | English | 一句话直觉 | 核心文章 |", "|---|---|---|---|"]
for row in sorted(rows, key=lambda item: item["english_term"].lower()):
    article = row["primary_article"]
    rel = "../" + article.removeprefix("docs/")
    lines.append(f'| {row["term"]} | {row["english_term"]} | {row["one_sentence_intuition"]} | [深入阅读]({rel}) |')
target.write_text("\n".join(lines) + "\n", encoding="utf-8")
