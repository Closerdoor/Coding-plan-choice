"""Entrypoint for generating CATALOG_GENERATED.md.

Run:
  python -m catalog.update
"""

from __future__ import annotations

import copy
import importlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from rankings import core as rankings_core

from .catalog_config import VENDORS


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "catalog" / "output"
DATA_PATH = OUTPUT_DIR / "CATALOG_DATA.json"
GENERATED_MD_PATH = REPO_ROOT / "CATALOG_GENERATED.md"
MODEL_SCORES_PATH = REPO_ROOT / "rankings" / "output" / "MODEL_SCORES.json"


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


def _load_provider_top3_keys() -> Dict[str, set[str]]:
    if not MODEL_SCORES_PATH.exists():
        return {}

    payload = json.loads(MODEL_SCORES_PATH.read_text(encoding="utf-8"))
    by_provider: Dict[str, List[Tuple[str, float]]] = {}
    for model in payload.get("models", []):
        provider = model.get("provider")
        model_name = model.get("model")
        total_score = model.get("total_score_0_1")
        if not isinstance(provider, str) or not isinstance(model_name, str):
            continue
        if not isinstance(total_score, (int, float)) or provider == "Unknown":
            continue
        by_provider.setdefault(provider, []).append((model_name, float(total_score)))

    provider_top3: Dict[str, set[str]] = {}
    for provider, rows in by_provider.items():
        ranked = sorted(rows, key=lambda item: item[1], reverse=True)[:3]
        provider_top3[provider] = {
            rankings_core.model_join_key(model_name) for model_name, _score in ranked
        }
    return provider_top3


def _filter_models(
    raw_models: List[str], provider_top3: Dict[str, set[str]]
) -> List[str]:
    filtered: List[str] = []
    for model in raw_models:
        provider = rankings_core.canonical_provider("", model)
        if provider == "Unknown":
            continue
        allowed = provider_top3.get(provider)
        if not allowed:
            continue
        if rankings_core.model_join_key(model) in allowed:
            filtered.append(model)
    return filtered


def _normalize_vendor(
    vendor: Dict[str, object], provider_top3: Dict[str, set[str]]
) -> Dict[str, object]:
    normalized = copy.deepcopy(vendor)
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
        package["models_filtered"] = _filter_models(raw_list, provider_top3)
    return normalized


def _join_values(values: List[str]) -> str:
    return "；".join(values)


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
    vendor_name = str(vendor.get("vendor_name", "")).strip()
    official_source = str(vendor.get("official_source", "")).strip()
    updated_at = str(vendor.get("updated_at_utc", "")).strip()
    packages = [
        package for package in vendor.get("packages", []) if isinstance(package, dict)
    ]
    package_names = [str(package.get("name", "")).strip() for package in packages]

    rows = [
        ["项目", *package_names],
        ["价格", *[str(package.get("price", "")).strip() for package in packages]],
        ["用量", *[str(package.get("quota", "")).strip() for package in packages]],
        [
            "支持模型",
            *[
                _join_values(
                    package.get("models_filtered") or package.get("models_raw") or []
                )
                for package in packages
            ],
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
            f"## {company_name}｜{vendor_name}",
            "",
            f"- 官方信息源：{official_source}",
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
    provider_top3 = _load_provider_top3_keys()
    warnings: List[str] = []
    vendors: List[Dict[str, object]] = []

    for config in VENDORS:
        vendor_id = config["vendor_id"]
        try:
            module = importlib.import_module(config["source_module"])
            fetched = module.fetch(config)
            normalized = _normalize_vendor(fetched, provider_top3)
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
        "generated_at_utc": utc_now_iso(),
        "warnings": warnings,
        "vendors": vendors,
    }
    _write_json(DATA_PATH, payload)
    GENERATED_MD_PATH.write_text(
        _render_catalog_md(vendors), encoding="utf-8", newline="\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
