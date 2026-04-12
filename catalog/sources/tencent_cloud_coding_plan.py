"""Tencent Cloud Coding Plan source.

Fetches the official product page and extracts the fields needed for the
catalog's normalized output.
"""

from __future__ import annotations

import gzip
import html
import re
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List


SOURCE_NAME = "tencent-cloud-coding-plan"

_PREFERRED_TOOL_ORDER = [
    "OpenClaw",
    "OpenCode",
    "Claude Code",
    "Codex",
    "Cursor",
]

_DOCUMENT_MODEL_ORDER = [
    "Auto",
    "Tencent HY 2.0 Instruct",
    "Tencent HY 2.0 Think",
    "MiniMax-M2.5",
    "Kimi-K2.5",
    "GLM-5",
    "Hunyuan-T1",
    "Hunyuan-TurboS",
]

_DOCUMENT_TOOL_ORDER = [
    "OpenClaw",
    "CodeBuddy Code",
    "Claude Code",
    "OpenCode",
    "Cline",
    "Cursor",
    "Codex",
    "Kilo CLI",
    "Kilo Code",
]


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


class _AnchorTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_anchor = False
        self._current: List[str] = []
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag == "a":
            self._in_anchor = True
            self._current = []

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag == "a" and self._in_anchor:
            text = " ".join(part.strip() for part in self._current if part.strip())
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                self.links.append(text)
            self._in_anchor = False
            self._current = []

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._in_anchor and data.strip():
            self._current.append(data)


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        raw = response.read()
        if response.headers.get("Content-Encoding", "").lower() == "gzip":
            raw = gzip.decompress(raw)
        return raw.decode("utf-8", "replace")


def _html_to_text(raw_html: str) -> str:
    parser = _HTMLTextParser()
    parser.feed(raw_html)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def _compact_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _extract_anchor_texts(raw_html: str) -> List[str]:
    parser = _AnchorTextParser()
    parser.feed(raw_html)
    return parser.links


def _normalize_quota(value: str) -> str:
    compact = re.sub(r"\s+", "", value)
    compact = compact.replace("；；", "；")
    return compact


def _extract_package_data(text: str) -> Dict[str, Dict[str, str]]:
    compact = _compact_text(text)
    section_start = compact.find("推荐购买")
    section_end = compact.find("4步开启AI编程之旅")
    if section_start == -1 or section_end == -1 or section_end <= section_start:
        raise ValueError("failed to locate Tencent Cloud purchase section")

    section = compact[section_start:section_end]
    quota_matches = re.findall(r"用量：([0-9次请求/小时周月；]+)", section)
    price_matches = re.findall(r"([0-9]+)元/月", section)

    unique_quotas: List[str] = []
    for quota in quota_matches:
        normalized = _normalize_quota(quota)
        if normalized not in unique_quotas:
            unique_quotas.append(normalized)

    unique_prices: List[str] = []
    for price in price_matches:
        if price not in unique_prices:
            unique_prices.append(price)

    if len(unique_quotas) < 2 or len(unique_prices) < 2:
        raise ValueError("failed to extract Tencent Cloud package price/quota data")

    return {
        "pro套餐": {"price": f"¥{unique_prices[0]}/月", "quota": unique_quotas[0]},
        "lite套餐": {"price": f"¥{unique_prices[1]}/月", "quota": unique_quotas[1]},
    }


def _extract_models(text: str) -> List[str]:
    compact = _compact_text(text)
    pattern = re.compile(
        r"TencentHY2\.0Instruct、GLM-5、kimi-k2\.5、MiniMax-M2\.5",
        re.I,
    )
    if not pattern.search(compact):
        raise ValueError("failed to extract Tencent Cloud supported models")
    return [
        "Tencent HY 2.0 Instruct",
        "GLM-5",
        "Kimi-K2.5",
        "MiniMax-M2.5",
    ]


def _extract_document_models(text: str) -> List[str]:
    models = [name for name in _DOCUMENT_MODEL_ORDER if name in text]
    if not models:
        raise ValueError("failed to extract Tencent Cloud documented models")
    return models


def _extract_tools(raw_html: str) -> List[str]:
    anchors = set(_extract_anchor_texts(raw_html))
    return [tool for tool in _PREFERRED_TOOL_ORDER if tool in anchors]


def _extract_document_tools(text: str) -> List[str]:
    tools = [name for name in _DOCUMENT_TOOL_ORDER if name in text]
    if not tools:
        raise ValueError("failed to extract Tencent Cloud documented tools")
    return tools


def _merge_unique(primary: List[str], secondary: List[str]) -> List[str]:
    merged: List[str] = []
    for value in [*primary, *secondary]:
        if value not in merged:
            merged.append(value)
    return merged


def _extract_discount_prices(text: str) -> Dict[str, str]:
    compact = _compact_text(text)
    patterns = {
        "lite套餐": r"Lite套餐特惠价首月([0-9.]+)元/月",
        "pro套餐": r"Pro套餐特惠价首月([0-9.]+)元/月",
    }
    discounts: Dict[str, str] = {}
    for package_name, pattern in patterns.items():
        match = re.search(pattern, compact)
        if not match:
            raise ValueError(
                f"failed to extract Tencent Cloud discount for {package_name}"
            )
        discounts[package_name] = f"首月¥{match.group(1)}/月"
    return discounts


def fetch(config: Dict[str, str]) -> Dict[str, object]:
    source_urls = config["source_urls"]
    if len(source_urls) < 2:
        raise ValueError(
            "Tencent Cloud source_urls must include activity page and document page"
        )

    activity_html = _http_get(source_urls[0])
    activity_text = _html_to_text(activity_html)
    document_html = _http_get(source_urls[1])
    document_text = _html_to_text(document_html)

    package_data = _extract_package_data(activity_text)
    activity_models = _extract_models(activity_text)
    document_models = _extract_document_models(document_text)
    models_raw = _merge_unique(document_models, activity_models)

    activity_tools = _extract_tools(activity_html)
    if len(activity_tools) != len(_PREFERRED_TOOL_ORDER):
        raise ValueError("failed to extract Tencent Cloud marketing tools")
    document_tools = _extract_document_tools(document_text)
    tools = _merge_unique(activity_tools, document_tools)
    discounts = _extract_discount_prices(document_text)

    packages = [
        {
            "name": "lite套餐",
            "price": package_data["lite套餐"]["price"],
            "discount": discounts["lite套餐"],
            "quota": package_data["lite套餐"]["quota"],
            "models_raw": models_raw,
            "tools": tools,
            "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
        },
        {
            "name": "pro套餐",
            "price": package_data["pro套餐"]["price"],
            "discount": discounts["pro套餐"],
            "quota": package_data["pro套餐"]["quota"],
            "models_raw": models_raw,
            "tools": tools,
            "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
        },
    ]

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "vendor_name": config["vendor_name"],
        "official_sources": source_urls,
        "packages": packages,
    }
