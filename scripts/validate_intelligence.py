#!/usr/bin/env python3
"""Validate structured company, product, standard, and interface intelligence."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today()

CONFIG = {
    "companies": {
        "path": ROOT / "data" / "companies.yaml",
        "required": {"id", "name", "categories", "last_verified", "sources"},
    },
    "products": {
        "path": ROOT / "data" / "products.yaml",
        "required": {"id", "name", "company_id", "category", "product_status", "last_verified", "sources"},
    },
    "standards": {
        "path": ROOT / "data" / "standards.yaml",
        "required": {"id", "name", "organization", "version", "status", "last_verified", "sources"},
    },
    "interfaces": {
        "path": ROOT / "data" / "interfaces.yaml",
        "required": {"id", "name", "scope", "layers", "status", "last_verified", "sources"},
    },
}

PRODUCT_STATUSES = {"Announced", "Sampling", "Production", "Shipping", "Deployed", "Roadmap", "Rumored"}
STANDARD_STATUSES = {"Draft", "Released", "Adopted", "Superseded"}
INTERFACE_STATUSES = {"Draft", "Released", "Adopted", "Deployed", "Superseded"}


def load_records(kind: str) -> list[dict]:
    payload = yaml.safe_load(CONFIG[kind]["path"].read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"{kind}: schema_version must be 1")
    records = payload.get(kind)
    if not isinstance(records, list):
        raise ValueError(f"{kind}: top-level {kind} must be a list")
    return records


def validate_date(kind: str, record_id: str, value: object) -> None:
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{kind}/{record_id}: invalid last_verified {value!r}") from exc
    if parsed > TODAY:
        raise ValueError(f"{kind}/{record_id}: last_verified is in the future")


def validate_sources(kind: str, record_id: str, sources: object) -> None:
    if not isinstance(sources, list) or not sources:
        raise ValueError(f"{kind}/{record_id}: sources must be a non-empty list")
    for source in sources:
        parsed = urlparse(str(source))
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"{kind}/{record_id}: invalid source URL {source!r}")


def validate() -> None:
    all_records = {kind: load_records(kind) for kind in CONFIG}
    ids_by_kind: dict[str, set[str]] = {}

    for kind, records in all_records.items():
        seen: set[str] = set()
        required = CONFIG[kind]["required"]
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError(f"{kind}[{index}]: record must be a mapping")
            missing = required - record.keys()
            if missing:
                raise ValueError(f"{kind}[{index}]: missing {sorted(missing)}")
            record_id = str(record["id"])
            if record_id in seen:
                raise ValueError(f"{kind}: duplicate id {record_id}")
            seen.add(record_id)
            validate_date(kind, record_id, record["last_verified"])
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

    counts = ", ".join(f"{kind}={len(records)}" for kind, records in all_records.items())
    print(f"intelligence validation passed: {counts}")


if __name__ == "__main__":
    validate()
