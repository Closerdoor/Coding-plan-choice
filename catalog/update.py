"""Entrypoint for generating CATALOG_GENERATED.md.

Run:
  python -m catalog.update
"""

from __future__ import annotations

import copy
import importlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from .catalog_config import AUTO_UPDATE_VENDOR_IDS, MANUAL_UPDATE_VENDOR_IDS, VENDORS


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "catalog" / "output"
DATA_PATH = OUTPUT_DIR / "CATALOG_DATA.json"
GENERATED_MD_PATH = REPO_ROOT / "CATALOG_GENERATED.md"


def _selected_vendor_ids() -> set[str] | None:
    mode = os.environ.get("CATALOG_UPDATE_MODE", "all").strip().lower()
    if mode == "all":
        return None
    if mode == "auto":
        return set(AUTO_UPDATE_VENDOR_IDS)
    if mode == "manual":
        return set(MANUAL_UPDATE_VENDOR_IDS)
    raise ValueError(f"unsupported CATALOG_UPDATE_MODE: {mode}")


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).replace(microsecond=0).isoformat()


def _load_existing_payload() -> Dict[str, object]:
    if not DATA_PATH.exists():
        return {"vendors": []}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _existing_vendors_by_id(payload: Dict[str, object]) -> Dict[str, Dict[str, object]]:
    by_id: Dict[str, Dict[str, object]] = {}
    for vendor in payload.get("vendors", []):
        if not isinstance(vendor, dict):
            continue
        vendor_id = vendor.get("vendor_id")
        if isinstance(vendor_id, str):
            by_id[vendor_id] = copy.deepcopy(vendor)
    return by_id


def _normalize_vendor(vendor: Dict[str, object]) -> Dict[str, object]:
    normalized = copy.deepcopy(vendor)
    if "plan_name" not in normalized and isinstance(normalized.get("vendor_name"), str):
        normalized["plan_name"] = normalized.get("vendor_name")
    if "official_url" not in normalized:
        official_sources = normalized.get("official_sources")
        if isinstance(official_sources, list) and official_sources:
            first_source = official_sources[0]
            if isinstance(first_source, str) and first_source.strip():
                normalized["official_url"] = first_source
                normalized["source_urls"] = [
                    item
                    for item in official_sources[1:]
                    if isinstance(item, str) and item.strip()
                ]
    if "source_urls" not in normalized:
        normalized["source_urls"] = []

    packages = normalized.get("packages")
    if not isinstance(packages, list):
        normalized["packages"] = []
        return normalized

    for package in packages:
        if not isinstance(package, dict):
            continue
        raw_models = package.get("models_raw")
        raw_list = (
            [item for item in raw_models if isinstance(item, str)]
            if isinstance(raw_models, list)
            else []
        )
        package["models_raw"] = raw_list
        package["models_filtered"] = []
    return normalized


def _vendor_content(vendor: Dict[str, object]) -> Dict[str, object]:
    content = copy.deepcopy(vendor)
    content.pop("updated_at_utc", None)
    return content


def _payload_content(payload: Dict[str, object]) -> Dict[str, object]:
    content = copy.deepcopy(payload)
    content.pop("generated_at_utc", None)
    return content


def _generated_at_from_vendors(vendors: List[Dict[str, object]], fallback: str) -> str:
    timestamps = []
    for vendor in vendors:
        updated_at = vendor.get("updated_at_utc")
        if isinstance(updated_at, str) and updated_at.strip():
            timestamps.append(updated_at)
    return max(timestamps) if timestamps else fallback


def _join_values(values: List[str]) -> str:
    return "；".join(values)


def _render_price(package: Dict[str, object]) -> str:
    base_price = str(package.get("price", "")).strip()
    discount = str(package.get("discount", "")).strip()
    if not discount:
        return base_price
    normalized_base = re.sub(r"\s+", "", base_price)
    normalized_discount = re.sub(r"\s+", "", discount)
    normalized_discount = normalized_discount.removeprefix("首月")
    if normalized_base == normalized_discount:
        return base_price
    return f"{base_price}(优惠：{discount})"


def _to_markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    lines = [
        "| " + " | ".join(rows[0]) + " |",
        "| " + " | ".join(["---"] * len(rows[0])) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
    return "\n".join(lines)


def _render_vendor(vendor: Dict[str, object]) -> str:
    company_name = str(vendor.get("company_name", "")).strip()
    plan_name = str(vendor.get("plan_name", "")).strip()
    official_url = str(vendor.get("official_url", "")).strip()
    source_lines: List[str] = []
    if official_url:
        source_lines.append(f"- 官方地址：{official_url}")
    updated_at = str(vendor.get("updated_at_utc", "")).strip()
    packages = [
        package for package in vendor.get("packages", []) if isinstance(package, dict)
    ]
    package_names = [str(package.get("name", "")).strip() for package in packages]

    rows = [
        ["项目", *package_names],
        ["价格", *[_render_price(package) for package in packages]],
        ["用量", *[str(package.get("quota", "")).strip() for package in packages]],
        [
            "支持模型",
            *[_join_values(package.get("models_raw") or []) for package in packages],
        ],
        [
            "支持工具",
            *[_join_values(package.get("tools") or []) for package in packages],
        ],
        [
            "使用方式",
            *[str(package.get("access_method", "")).strip() for package in packages],
        ],
    ]

    table = _to_markdown_table(rows)
    return "\n".join(
        [
            f"## {company_name}｜{plan_name}",
            "",
            *source_lines,
            f"- 最后更新时间（UTC）：{updated_at}",
            "",
            table,
        ]
    )


def _render_catalog_md(vendors: List[Dict[str, object]]) -> str:
    parts = [
        "# AI 模型与 Coding Plan 套餐汇总",
        "",
        "说明：",
        "- 本文档用于集中展示各厂商的模型/套餐信息。",
        "- 所有价格与用量信息以官方页面为准，并在条目中标注信息源链接。",
        "- 币种按厂商原始币种展示（CN=CNY，US=USD）。",
        "- 最后更新时间使用 UTC（由自动更新流程填写）。",
        "",
        "---",
        "",
    ]
    for vendor in vendors:
        parts.append(_render_vendor(vendor))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def _write_json(path: Path, payload: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    existing_payload = _load_existing_payload()
    existing_vendors = _existing_vendors_by_id(existing_payload)
    selected_vendor_ids = _selected_vendor_ids()
    warnings: List[str] = []
    vendors: List[Dict[str, object]] = []

    for config in VENDORS:
        vendor_id = config["vendor_id"]
        if selected_vendor_ids is not None and vendor_id not in selected_vendor_ids:
            if vendor_id in existing_vendors:
                vendors.append(existing_vendors[vendor_id])
            else:
                warnings.append(
                    f"vendor {vendor_id}: skipped by CATALOG_UPDATE_MODE with no previous data"
                )
            continue
        try:
            module = importlib.import_module(config["source_module"])
            fetched = module.fetch(config)
            normalized = _normalize_vendor(fetched)
            previous_vendor = existing_vendors.get(vendor_id)
            if previous_vendor and _vendor_content(previous_vendor) == _vendor_content(
                normalized
            ):
                normalized["updated_at_utc"] = previous_vendor.get(
                    "updated_at_utc", utc_now_iso()
                )
            else:
                normalized["updated_at_utc"] = utc_now_iso()
            vendors.append(normalized)
        except Exception as exc:
            if vendor_id in existing_vendors:
                vendors.append(existing_vendors[vendor_id])
                warnings.append(
                    f"vendor {vendor_id}: failed, kept previous data: {type(exc).__name__}: {exc}"
                )
            else:
                warnings.append(
                    f"vendor {vendor_id}: failed with no previous data: {type(exc).__name__}: {exc}"
                )

    payload = {
        "generated_at_utc": _generated_at_from_vendors(vendors, utc_now_iso()),
        "warnings": warnings,
        "vendors": vendors,
    }
    if _payload_content(existing_payload) == _payload_content(payload):
        payload["generated_at_utc"] = existing_payload.get(
            "generated_at_utc", payload["generated_at_utc"]
        )
    _write_json(DATA_PATH, payload)
    GENERATED_MD_PATH.write_text(
        _render_catalog_md(vendors), encoding="utf-8", newline="\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
