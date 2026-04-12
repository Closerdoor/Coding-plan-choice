"""Entrypoint for generating README.md.

Run:
  python -m catalog.update
"""

from __future__ import annotations

import copy
import importlib
import json
import logging
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Dict, List, Tuple

from .catalog_config import AUTO_UPDATE_VENDOR_IDS, MANUAL_UPDATE_VENDOR_IDS, VENDORS


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "catalog" / "output"
DATA_PATH = OUTPUT_DIR / "CATALOG_DATA.json"
README_PATH = REPO_ROOT / "README.md"
LOG_PATH = OUTPUT_DIR / "CATALOG_RUN.log"
PREFLIGHT_PATH = OUTPUT_DIR / "CATALOG_PREFLIGHT.json"


LOGGER = logging.getLogger("catalog.update")


def _duration_ms(start_time: float) -> int:
    return int((perf_counter() - start_time) * 1000)


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


def _configure_logging() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False
    LOGGER.handlers.clear()
    formatter = logging.Formatter("%(asctime)sZ %(levelname)s %(message)s")

    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8", mode="w")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(stream_handler)


def _all_urls_for_preflight(config: Dict[str, object]) -> List[str]:
    urls: List[str] = []
    official_url = config.get("official_url")
    if isinstance(official_url, str) and official_url.strip():
        urls.append(official_url.strip())
    source_urls = config.get("source_urls", [])
    if isinstance(source_urls, list):
        urls.extend(
            url.strip() for url in source_urls if isinstance(url, str) and url.strip()
        )
    return urls


def _probe_url(url: str, *, timeout_s: int = 15) -> Dict[str, object]:
    started = perf_counter()
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname
    if not host:
        return {
            "url": url,
            "ok": False,
            "error": "invalid url",
            "duration_ms": _duration_ms(started),
        }
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return {
                "url": url,
                "ok": True,
                "status": "tcp-ok",
                "duration_ms": _duration_ms(started),
            }
    except OSError as exc:
        return {
            "url": url,
            "ok": False,
            "error": str(exc),
            "duration_ms": _duration_ms(started),
        }


def _run_preflight(
    configs: List[Dict[str, object]],
) -> Tuple[Dict[str, List[Dict[str, object]]], List[str]]:
    report: Dict[str, List[Dict[str, object]]] = {}
    warnings: List[str] = []
    for config in configs:
        vendor_started = perf_counter()
        vendor_id = str(config["vendor_id"])
        checks = [_probe_url(url) for url in _all_urls_for_preflight(config)]
        report[vendor_id] = checks
        failures = [item for item in checks if not item.get("ok")]
        if failures:
            first_failure = failures[0]
            warnings.append(
                f"vendor {vendor_id}: preflight failed for {first_failure.get('url')}: {first_failure.get('error', first_failure.get('status', 'unknown'))}"
            )
            LOGGER.warning(
                "Preflight failed for %s in %dms: %s",
                vendor_id,
                _duration_ms(vendor_started),
                first_failure,
            )
        else:
            LOGGER.info(
                "Preflight ok for %s in %dms", vendor_id, _duration_ms(vendor_started)
            )

    _write_json(PREFLIGHT_PATH, report)
    return report, warnings


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


AGGREGATED_VENDOR_IDS = [
    "cursor",
    "github-copilot",
    "trae-intl",
    "tencent-cloud-coding-plan",
    "volcengine-coding-plan",
    "aliyun-bailian-coding-plan",
    "baidu-qianfan-coding-plan",
    "xfyun-xingchen-coding-plan",
    "infini-ai-coding-plan",
]

VERTICAL_VENDOR_IDS = [
    "openai-chatgpt",
    "claude-code",
    "glm-coding-plan",
    "minimax-token-plan",
    "kimi-ai",
    "xiaomi-mimo-token-plan",
]


def _vendor_anchor(vendor: Dict[str, object]) -> str:
    return str(vendor.get("plan_name", "")).strip().lower().replace(" ", "-")


def _summary_price(vendor: Dict[str, object]) -> str:
    packages = [
        package for package in vendor.get("packages", []) if isinstance(package, dict)
    ]
    if not packages:
        return ""
    return str(packages[0].get("price", "")).strip()


def _summary_models(vendor: Dict[str, object]) -> str:
    packages = [
        package for package in vendor.get("packages", []) if isinstance(package, dict)
    ]
    if not packages:
        return ""
    models = packages[0].get("models_raw") or []
    if not isinstance(models, list):
        return ""
    return _join_values(
        [str(model).strip() for model in models[:4] if str(model).strip()]
    )


def _render_vendor(vendor: Dict[str, object], *, heading_level: str = "###") -> str:
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
            f"{heading_level} {plan_name}",
            "",
            f"- 厂商：{company_name}",
            *source_lines,
            f"- 最后更新时间（UTC）：{updated_at}",
            "",
            table,
        ]
    )


def _render_vendor_nav(vendors: List[Dict[str, object]]) -> List[str]:
    return [
        f"- [{str(vendor.get('plan_name', '')).strip()}](#{_vendor_anchor(vendor)})"
        for vendor in vendors
    ]


def _render_summary_table(vendors: List[Dict[str, object]]) -> str:
    rows = [
        ["厂商", "分类", "套餐数", "起步价", "接入方式", "代表模型", "更新时间(UTC)"]
    ]
    for vendor in vendors:
        packages = [
            package
            for package in vendor.get("packages", [])
            if isinstance(package, dict)
        ]
        rows.append(
            [
                str(vendor.get("plan_name", "")).strip(),
                "聚合套餐"
                if str(vendor.get("vendor_id", "")) in AGGREGATED_VENDOR_IDS
                else "垂直厂商套餐",
                str(len(packages)),
                _summary_price(vendor),
                str(packages[0].get("access_method", "")).strip() if packages else "",
                _summary_models(vendor),
                str(vendor.get("updated_at_utc", "")).strip(),
            ]
        )
    return _to_markdown_table(rows)


def _render_warning_section(warnings: List[str]) -> List[str]:
    if not warnings:
        return ["- 本次更新状态：无 warnings"]
    lines = ["- 本次更新状态：存在 warnings"]
    lines.extend(f"- Warning：{warning}" for warning in warnings)
    return lines


def _group_vendors(
    vendors: List[Dict[str, object]],
) -> tuple[List[Dict[str, object]], List[Dict[str, object]]]:
    aggregated = [
        vendor
        for vendor in vendors
        if str(vendor.get("vendor_id", "")) in AGGREGATED_VENDOR_IDS
    ]
    vertical = [
        vendor
        for vendor in vendors
        if str(vendor.get("vendor_id", "")) in VERTICAL_VENDOR_IDS
    ]
    return aggregated, vertical


def _render_catalog_md(
    vendors: List[Dict[str, object]], warnings: List[str], generated_at: str
) -> str:
    aggregated_vendors, vertical_vendors = _group_vendors(vendors)
    parts = [
        "# Coding Plan 套餐汇总",
        "",
        "汇总各家 Coding Plan 套餐、价格、额度、支持模型与接入方式。自动更新公开可直接抓取的厂商，登录态厂商通过单独手动流程维护。",
        "",
        "## 更新状态",
        "",
        f"- 最新生成时间（UTC）：{generated_at}",
        f"- 自动更新厂商数：{len(AUTO_UPDATE_VENDOR_IDS)}",
        f"- 手动更新厂商数：{len(MANUAL_UPDATE_VENDOR_IDS)}",
        *_render_warning_section(warnings),
        "",
        "## 导航",
        "",
        "### 聚合套餐",
        *(_render_vendor_nav(aggregated_vendors) or ["- 暂无"]),
        "",
        "### 垂直厂商套餐",
        *(_render_vendor_nav(vertical_vendors) or ["- 暂无"]),
        "",
        "## 总览",
        "",
        _render_summary_table(vendors),
        "",
        "## 聚合套餐",
        "",
    ]
    for vendor in aggregated_vendors:
        parts.append(_render_vendor(vendor))
        parts.append("")
    parts.extend(["## 垂直厂商套餐", ""])
    for vendor in vertical_vendors:
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
    run_started = perf_counter()
    _configure_logging()
    existing_payload = _load_existing_payload()
    existing_vendors = _existing_vendors_by_id(existing_payload)
    selected_vendor_ids = _selected_vendor_ids()
    fetch_warnings: List[str] = []
    vendors: List[Dict[str, object]] = []

    selected_configs = [
        config
        for config in VENDORS
        if selected_vendor_ids is None or config["vendor_id"] in selected_vendor_ids
    ]
    LOGGER.info(
        "Starting catalog update mode=%s vendors=%s",
        os.environ.get("CATALOG_UPDATE_MODE", "all"),
        [config["vendor_id"] for config in selected_configs],
    )
    _, preflight_warnings = _run_preflight(selected_configs)
    LOGGER.info("Preflight finished with %d warnings", len(preflight_warnings))

    for config in VENDORS:
        vendor_id = config["vendor_id"]
        if selected_vendor_ids is not None and vendor_id not in selected_vendor_ids:
            if vendor_id in existing_vendors:
                vendors.append(existing_vendors[vendor_id])
            else:
                fetch_warnings.append(
                    f"vendor {vendor_id}: skipped by CATALOG_UPDATE_MODE with no previous data"
                )
            continue
        try:
            vendor_started = perf_counter()
            LOGGER.info("Fetching vendor %s", vendor_id)
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
            LOGGER.info(
                "Fetched vendor %s successfully in %dms",
                vendor_id,
                _duration_ms(vendor_started),
            )
        except Exception as exc:
            vendor_duration_ms = _duration_ms(vendor_started)
            LOGGER.exception(
                "Fetch failed for vendor %s in %dms",
                vendor_id,
                vendor_duration_ms,
            )
            if vendor_id in existing_vendors:
                vendors.append(existing_vendors[vendor_id])
                fetch_warnings.append(
                    f"vendor {vendor_id}: failed, kept previous data: {type(exc).__name__}: {exc}"
                )
            else:
                fetch_warnings.append(
                    f"vendor {vendor_id}: failed with no previous data: {type(exc).__name__}: {exc}"
                )

    payload = {
        "generated_at_utc": _generated_at_from_vendors(vendors, utc_now_iso()),
        "warnings": fetch_warnings,
        "vendors": vendors,
    }
    if _payload_content(existing_payload) == _payload_content(payload):
        payload["generated_at_utc"] = existing_payload.get(
            "generated_at_utc", payload["generated_at_utc"]
        )
    _write_json(DATA_PATH, payload)
    README_PATH.write_text(
        _render_catalog_md(vendors, fetch_warnings, payload["generated_at_utc"]),
        encoding="utf-8",
        newline="\n",
    )
    LOGGER.info("Wrote preflight report to %s", PREFLIGHT_PATH)
    LOGGER.info("Wrote catalog data to %s", DATA_PATH)
    LOGGER.info("Wrote catalog markdown to %s", README_PATH)
    LOGGER.info(
        "Finished catalog update with %d preflight warnings", len(preflight_warnings)
    )
    LOGGER.info("Finished catalog update with %d fetch warnings", len(fetch_warnings))
    LOGGER.info("Total catalog update duration: %dms", _duration_ms(run_started))
    logging.shutdown()
    return 0


def preflight_only() -> int:
    run_started = perf_counter()
    _configure_logging()
    selected_vendor_ids = _selected_vendor_ids()
    selected_configs = [
        config
        for config in VENDORS
        if selected_vendor_ids is None or config["vendor_id"] in selected_vendor_ids
    ]
    LOGGER.info(
        "Starting catalog preflight mode=%s vendors=%s",
        os.environ.get("CATALOG_UPDATE_MODE", "all"),
        [config["vendor_id"] for config in selected_configs],
    )
    _, warnings = _run_preflight(selected_configs)
    LOGGER.info("Finished catalog preflight with %d warnings", len(warnings))
    LOGGER.info("Total catalog preflight duration: %dms", _duration_ms(run_started))
    logging.shutdown()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
