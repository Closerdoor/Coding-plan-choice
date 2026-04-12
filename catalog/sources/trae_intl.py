"""TRAE INTL pricing source."""

from __future__ import annotations

import html
import re
import urllib.request
from html.parser import HTMLParser
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


class _HTMLTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag in {"script", "style"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag in {"script", "style"} and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._skip_depth == 0 and data.strip():
            self.parts.append(data.strip())


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _html_to_text(raw_html: str) -> str:
    parser = _HTMLTextParser()
    parser.feed(raw_html)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def _extract_price(pricing_text: str, package_name: str) -> str:
    patterns = {
        "Lite": r"Lite\s*\$\s*3\s*per month, billed monthly",
        "Pro": r"Pro\s*\$\s*0\s*\$\s*10\s*Free for 7 days\. Then \$10/month",
        "Pro+": r"Pro\+\s*\$\s*30\s*per month, billed monthly",
        "Ultra": r"Ultra\s*\$\s*100\s*per month, billed monthly",
    }
    if not re.search(patterns[package_name], pricing_text):
        raise ValueError(f"failed to extract TRAE price for {package_name}")
    prices = {
        "Lite": "$3/月",
        "Pro": "$10/月",
        "Pro+": "$30/月",
        "Ultra": "$100/月",
    }
    return prices[package_name]


def _extract_discount(pricing_text: str, package_name: str) -> str:
    if package_name != "Pro":
        return ""
    if "Free for 7 days. Then $10/month." not in pricing_text:
        raise ValueError("failed to confirm TRAE Pro trial discount")
    return "前7天免费"


def _extract_quota(pricing_text: str, package_name: str) -> str:
    quota_map = {
        "Lite": "月含 $5 Basic Usage；超出按官方模型费率消耗",
        "Pro": "月含 $20 Basic Usage；超出按官方模型费率消耗",
        "Pro+": "月含 $90 Basic Usage；超出按官方模型费率消耗",
        "Ultra": "月含 $400 Basic Usage；超出按官方模型费率消耗",
    }
    required_fragments = {
        "Lite": ["$ 5 Basic usage", "Concurrent Cloud Tasks 2 2 10 15 20"],
        "Pro": ["$ 20 Basic usage", "Concurrent Cloud Tasks 2 2 10 15 20"],
        "Pro+": ["$ 90 Basic usage", "Concurrent Cloud Tasks 2 2 10 15 20"],
        "Ultra": ["$ 400 Basic usage", "Concurrent Cloud Tasks 2 2 10 15 20"],
    }
    if any(
        fragment not in pricing_text for fragment in required_fragments[package_name]
    ):
        raise ValueError(f"failed to extract TRAE quota for {package_name}")
    return quota_map[package_name]


def _extract_models(pricing_html: str) -> List[str]:
    models = [model for model in _MODEL_ORDER if model in pricing_html]
    if len(models) < 4:
        raise ValueError("failed to extract TRAE supported models")
    return models


def _extract_access_method(pricing_text: str) -> str:
    if "TRAE SOLO (Web/Desktop)" not in pricing_text:
        raise ValueError("failed to confirm TRAE access method")
    return "账号订阅（TRAE IDE / TRAE SOLO）"


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]

    pricing_html = _http_get(official_url)
    pricing_text = _html_to_text(pricing_html)
    billing_html = _http_get(source_urls[0]) if source_urls else ""
    terms_text = (
        _html_to_text(_http_get(source_urls[1])) if len(source_urls) > 1 else ""
    )

    if "Pricing" not in pricing_text or "Monthly Basic Usage" not in pricing_text:
        raise ValueError("failed to confirm TRAE pricing page")
    if billing_html and "TRAE SOLO" not in billing_html:
        raise ValueError("failed to confirm TRAE billing page")
    if terms_text and "Terms of Service" not in terms_text:
        raise ValueError("failed to confirm TRAE terms page")

    models_raw = _extract_models(pricing_html)
    access_method = _extract_access_method(pricing_text)

    packages = []
    for package_name, normalized_name in _PACKAGE_ORDER:
        packages.append(
            {
                "name": normalized_name,
                "price": _extract_price(pricing_text, package_name),
                "discount": _extract_discount(pricing_text, package_name),
                "quota": _extract_quota(pricing_text, package_name),
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
