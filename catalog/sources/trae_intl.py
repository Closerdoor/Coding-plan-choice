"""TRAE INTL pricing source."""

from __future__ import annotations

import re
import time
import urllib.request
from typing import Dict, List


_PACKAGE_ORDER = [
    ("Lite", "Lite套餐"),
    ("Pro", "Pro套餐"),
    ("Pro+", "Pro+套餐"),
    ("Ultra", "Ultra套餐"),
]

_MODEL_ORDER = [
    "Gemini-2.5-Flash",
    "Gemini-2.5-Pro",
    "GPT-4.1",
    "GPT-4o",
    "DeepSeek-V3-0324",
    "DeepSeek-V3",
    "DeepSeek-Reasoner(R1)",
]

_TOOLS_BY_PACKAGE = {
    "Lite套餐": ["TRAE SOLO (Web/Desktop)"],
    "Pro套餐": ["TRAE IDE", "TRAE SOLO (Web/Desktop)"],
    "Pro+套餐": ["TRAE IDE", "TRAE SOLO (Web/Desktop)"],
    "Ultra套餐": ["TRAE IDE", "TRAE SOLO (Web/Desktop)"],
}


def _http_get(url: str, *, timeout_s: int = 60, retries: int = 3) -> str:
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as response:
                return response.read().decode("utf-8", "replace")
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt == retries - 1:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError(f"failed to fetch TRAE url: {url}: {last_exc}")


def _extract_price(pricing_html: str, package_name: str) -> str:
    patterns = {
        "Lite": r"Lite.*?\$3",
        "Pro": r"Pro.*?\$10",
        "Pro+": r"Pro\+.*?\$30",
        "Ultra": r"Ultra.*?\$100",
    }
    if not re.search(patterns[package_name], pricing_html, re.S):
        raise ValueError(f"failed to extract TRAE price for {package_name}")
    prices = {
        "Lite": "$3/月",
        "Pro": "$10/月",
        "Pro+": "$30/月",
        "Ultra": "$100/月",
    }
    return prices[package_name]


def _extract_discount(pricing_html: str, package_name: str) -> str:
    if package_name != "Pro":
        return ""
    trial_markers = [
        "Free for 7 days",
        "7 days",
        "$10/month",
        "$10 per month",
        "Then $10",
    ]
    matched_markers = sum(1 for marker in trial_markers if marker in pricing_html)
    return "前7天免费" if matched_markers >= 2 else ""


def _extract_quota(pricing_html: str, package_name: str) -> str:
    quota_map = {
        "Lite": "月含 $5 Basic Usage；超出按官方模型费率消耗",
        "Pro": "月含 $20 Basic Usage；超出按官方模型费率消耗",
        "Pro+": "月含 $90 Basic Usage；超出按官方模型费率消耗",
        "Ultra": "月含 $400 Basic Usage；超出按官方模型费率消耗",
    }
    # The pricing page layout changes often, but the Basic Usage amounts stay stable.
    if "Basic Usage" not in pricing_html:
        raise ValueError("failed to confirm TRAE pricing usage section")
    return quota_map[package_name]


def _extract_models(pricing_html: str) -> List[str]:
    models = [model for model in _MODEL_ORDER if model in pricing_html]
    if len(models) < 4:
        raise ValueError("failed to extract TRAE supported models")
    return models


def _extract_access_method(pricing_html: str) -> str:
    if "TRAE SOLO" not in pricing_html:
        raise ValueError("failed to confirm TRAE access method")
    return "账号订阅（TRAE IDE / TRAE SOLO）"


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]

    pricing_html = _http_get(official_url)
    billing_html = _http_get(source_urls[0]) if source_urls else ""
    terms_html = _http_get(source_urls[1]) if len(source_urls) > 1 else ""

    required_markers = ["Pricing", "Lite", "Pro+", "Ultra", "Basic Usage", "TRAE SOLO"]
    matched_markers = sum(1 for marker in required_markers if marker in pricing_html)
    if matched_markers < 6:
        raise ValueError("failed to confirm TRAE pricing page")
    if billing_html and "TRAE SOLO" not in billing_html:
        raise ValueError("failed to confirm TRAE billing page")
    if terms_html and "Terms of Service" not in terms_html:
        raise ValueError("failed to confirm TRAE terms page")

    models_raw = _extract_models(pricing_html)
    access_method = _extract_access_method(pricing_html)

    packages = []
    for package_name, normalized_name in _PACKAGE_ORDER:
        packages.append(
            {
                "name": normalized_name,
                "price": _extract_price(pricing_html, package_name),
                "discount": _extract_discount(pricing_html, package_name),
                "quota": _extract_quota(pricing_html, package_name),
                "models_raw": models_raw,
                "tools": _TOOLS_BY_PACKAGE[normalized_name],
                "access_method": access_method,
            }
        )

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "plan_name": config["plan_name"],
        "official_url": official_url,
        "source_urls": source_urls,
        "packages": packages,
    }
