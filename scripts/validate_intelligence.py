#!/usr/bin/env python3
"""Validate company, product, standard, interface, lineage, and freshness intelligence."""

from __future__ import annotations
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today()
CONFIG = {
    "companies": {"path": ROOT / "data" / "companies.yaml", "required": {"id", "name", "categories", "last_verified", "sources"}},
    "products": {"path": ROOT / "data" / "products.yaml", "required": {"id", "name", "company_id", "category", "product_status", "last_verified", "sources"}},
    "standards": {"path": ROOT / "data" / "standards.yaml", "required": {"id", "name", "organization", "version", "status", "last_verified", "sources"}},
    "interfaces": {"path": ROOT / "data" / "interfaces.yaml", "required": {"id", "name", "scope", "layers", "status", "last_verified", "sources"}},
}
PRODUCT_STATUSES = {"Announced", "Sampling", "Production", "Shipping", "Deployed", "Roadmap", "Rumored"}
STANDARD_STATUSES = {"Draft", "Released", "Adopted", "Superseded"}
INTERFACE_STATUSES = {"Draft", "Released", "Adopted", "Deployed", "Superseded"}
REVIEW_PRIORITIES = {"high", "medium", "low"}
REVIEW_STATUSES = {"Scheduled", "Due", "Blocked"}


def load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"{path}: schema_version must be 1")
    return payload


def load_records(kind: str) -> list[dict]:
    records = load_yaml(CONFIG[kind]["path"]).get(kind)
    if not isinstance(records, list):
        raise ValueError(f"{kind}: top-level {kind} must be a list")
    return records


def parse_date(kind: str, record_id: str, field: str, value: object, allow_future: bool = False) -> date:
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{kind}/{record_id}: invalid {field} {value!r}") from exc
    if not allow_future and parsed > TODAY:
        raise ValueError(f"{kind}/{record_id}: {field} is in the future")
    return parsed


def validate_sources(kind: str, record_id: str, sources: object) -> None:
    if not isinstance(sources, list) or not sources:
        raise ValueError(f"{kind}/{record_id}: sources must be a non-empty list")
    for source in sources:
        parsed = urlparse(str(source))
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"{kind}/{record_id}: invalid source URL {source!r}")


def validate_lineages(ids_by_kind: dict[str, set[str]]) -> int:
    lineages = load_yaml(ROOT / "data" / "product_generations.yaml").get("lineages")
    if not isinstance(lineages, list):
        raise ValueError("product_generations: lineages must be a list")
    seen: set[str] = set()
    for lineage in lineages:
        lineage_id = str(lineage.get("id", ""))
        if not lineage_id or lineage_id in seen:
            raise ValueError(f"product_generations: invalid or duplicate lineage id {lineage_id!r}")
        seen.add(lineage_id)
        if lineage.get("company_id") not in ids_by_kind["companies"]:
            raise ValueError(f"product_generations/{lineage_id}: unknown company_id")
        generations = lineage.get("generations")
        if not isinstance(generations, list) or len(generations) < 2:
            raise ValueError(f"product_generations/{lineage_id}: at least two generations required")
        prior_date: date | None = None
        for index, generation in enumerate(generations):
            required = {"name", "milestone_date", "product_status", "relation", "sources"}
            missing = required - generation.keys()
            if missing:
                raise ValueError(f"product_generations/{lineage_id}[{index}]: missing {sorted(missing)}")
            milestone = parse_date("product_generations", lineage_id, "milestone_date", generation["milestone_date"])
            if prior_date and milestone < prior_date:
                raise ValueError(f"product_generations/{lineage_id}: milestone dates must be ordered")
            prior_date = milestone
            if generation["product_status"] not in PRODUCT_STATUSES:
                raise ValueError(f"product_generations/{lineage_id}: invalid product_status")
            product_id = generation.get("product_id")
            if product_id and product_id not in ids_by_kind["products"]:
                raise ValueError(f"product_generations/{lineage_id}: unknown product_id {product_id}")
            validate_sources("product_generations", lineage_id, generation["sources"])
    return len(lineages)


def validate_reviews(ids_by_kind: dict[str, set[str]]) -> int:
    payload = load_yaml(ROOT / "data" / "source_reviews.yaml")
    policies = payload.get("review_policies")
    if not isinstance(policies, dict) or set(CONFIG) - policies.keys():
        raise ValueError("source_reviews: one review policy is required for every entity type")
    for kind, policy in policies.items():
        if kind not in CONFIG or not isinstance(policy.get("review_interval_days"), int) or policy["review_interval_days"] <= 0:
            raise ValueError(f"source_reviews: invalid policy for {kind}")
    watchlist = payload.get("watchlist")
    if not isinstance(watchlist, list):
        raise ValueError("source_reviews: watchlist must be a list")
    seen: set[tuple[str, str]] = set()
    for index, review in enumerate(watchlist):
        required = {"entity_type", "entity_id", "last_reviewed", "next_review", "priority", "status", "reason"}
        missing = required - review.keys()
        if missing:
            raise ValueError(f"source_reviews[{index}]: missing {sorted(missing)}")
        kind, entity_id = review["entity_type"], review["entity_id"]
        key = (kind, entity_id)
        if kind not in ids_by_kind or entity_id not in ids_by_kind[kind]:
            raise ValueError(f"source_reviews/{kind}/{entity_id}: unknown entity")
        if key in seen:
            raise ValueError(f"source_reviews: duplicate watchlist entry {key}")
        seen.add(key)
        last_reviewed = parse_date("source_reviews", entity_id, "last_reviewed", review["last_reviewed"])
        next_review = parse_date("source_reviews", entity_id, "next_review", review["next_review"], allow_future=True)
        if next_review < last_reviewed:
            raise ValueError(f"source_reviews/{entity_id}: next_review precedes last_reviewed")
        if review["priority"] not in REVIEW_PRIORITIES or review["status"] not in REVIEW_STATUSES:
            raise ValueError(f"source_reviews/{entity_id}: invalid priority or status")
    return len(watchlist)


def validate() -> None:
    all_records = {kind: load_records(kind) for kind in CONFIG}
    ids_by_kind: dict[str, set[str]] = {}
    for kind, records in all_records.items():
        seen: set[str] = set()
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(f"{kind}[{index}]: record must be a mapping")
            missing = CONFIG[kind]["required"] - record.keys()
            if missing:
                raise ValueError(f"{kind}[{index}]: missing {sorted(missing)}")
            record_id = str(record["id"])
            if record_id in seen:
                raise ValueError(f"{kind}: duplicate id {record_id}")
            seen.add(record_id)
            parse_date(kind, record_id, "last_verified", record["last_verified"])
            validate_sources(kind, record_id, record["sources"])
        ids_by_kind[kind] = seen
    for product in all_records["products"]:
        if product["company_id"] not in ids_by_kind["companies"]:
            raise ValueError(f"products/{product['id']}: unknown company_id {product['company_id']}")
        if product["product_status"] not in PRODUCT_STATUSES:
            raise ValueError(f"products/{product['id']}: invalid product_status")
    for standard in all_records["standards"]:
        if standard["status"] not in STANDARD_STATUSES:
            raise ValueError(f"standards/{standard['id']}: invalid status")
    for interface in all_records["interfaces"]:
        if interface["status"] not in INTERFACE_STATUSES:
            raise ValueError(f"interfaces/{interface['id']}: invalid status")
    lineages = validate_lineages(ids_by_kind)
    watchlist = validate_reviews(ids_by_kind)
    counts = ", ".join(f"{kind}={len(records)}" for kind, records in all_records.items())
    print(f"intelligence validation passed: {counts}, lineages={lineages}, watchlist={watchlist}")


if __name__ == "__main__":
    validate()
