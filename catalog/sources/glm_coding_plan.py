"""GLM Coding Plan source."""

from __future__ import annotations

import html
import re
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List


_MODEL_ORDER = [
    "GLM-5.1",
    "GLM-5-Turbo",
    "GLM-4.7",
    "GLM-4.5-Air",
]

_TOOL_ORDER = [
    "Claude Code",
    "OpenClaw",
    "OpenCode",
    "Cline",
    "Roo Code",
    "Kilo Code",
    "Cursor",
    "Crush",
    "Goose",
    "TRAE",
    "CodeBuddy",
]

_PACKAGE_ORDER = [
    ("Lite", "lite套餐"),
    ("Pro", "pro套餐"),
    ("Max", "max套餐"),
]

_RUNTIME_CHUNKS = [
    "vendors~ClaudeCode~SubscribePay~subscribe-overview",
    "ClaudeCode~subscribe-overview",
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


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _html_to_text(raw_html: str) -> str:
    parser = _HTMLTextParser()
    parser.feed(raw_html)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def _compact_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _extract_runtime_url(activity_html: str) -> str:
    match = re.search(r'<script src="(?P<url>/js/runtime\.[^"]+\.js)"', activity_html)
    if not match:
        raise ValueError("failed to locate GLM runtime script")
    return "https://bigmodel.cn" + match.group("url")


def _extract_chunk_url(runtime_js: str, chunk_name: str) -> str:
    match = re.search(rf'"{re.escape(chunk_name)}":"(?P<hash>[0-9a-f]+)"', runtime_js)
    if not match:
        raise ValueError(f"failed to locate GLM chunk hash for {chunk_name}")
    return f"https://bigmodel.cn/js/{chunk_name}.{match.group('hash')}.js"


def _load_pricing_chunk(activity_html: str) -> str:
    runtime_js = _http_get(_extract_runtime_url(activity_html))
    chunks = []
    for chunk_name in _RUNTIME_CHUNKS:
        chunks.append(_http_get(_extract_chunk_url(runtime_js, chunk_name)))
    return "\n".join(chunks)


def _extract_month_prices(chunk_text: str) -> Dict[str, Dict[str, str]]:
    object_pattern = re.compile(
        r'\{[^{}]*productName:"(?P<name>Lite|Pro|Max)"[^{}]*unit:"month"[^{}]*version:"v2"[^{}]*\}'
    )
    prices: Dict[str, Dict[str, str]] = {}
    for match in object_pattern.finditer(chunk_text):
        package_name = match.group("name")
        object_text = match.group(0)
        sale_match = re.search(r"salePrice:(?P<value>[0-9.]+)", object_text)
        renew_match = re.search(r"renewAmount:(?P<value>[0-9.]+)", object_text)
        if not sale_match or not renew_match:
            continue
        prices[package_name] = {
            "price": f"¥{renew_match.group('value')}/月",
            "discount": f"首月¥{sale_match.group('value')}/月",
        }

    if set(prices) != {"Lite", "Pro", "Max"}:
        raise ValueError("failed to extract GLM monthly prices")
    return prices


def _extract_quota(doc_text: str) -> Dict[str, str]:
    compact = _compact_text(doc_text)
    quotas: Dict[str, str] = {}
    for package_name, normalized_name in _PACKAGE_ORDER:
        match = re.search(
            rf"{package_name}套餐最多约(?P<hour>[0-9]+)次prompts最多约(?P<week>[0-9]+)次prompts",
            compact,
        )
        if not match:
            raise ValueError(f"failed to extract GLM quota for {normalized_name}")
        quotas[normalized_name] = (
            f"{match.group('hour')}次prompts/5小时；{match.group('week')}次prompts/周"
        )
    return quotas


def _extract_models(doc_text: str) -> List[str]:
    models = [model for model in _MODEL_ORDER if model in doc_text]
    if not models:
        raise ValueError("failed to extract GLM supported models")
    return models


def _extract_tools(*texts: str) -> List[str]:
    merged_text = "\n".join(texts)
    tools = [tool for tool in _TOOL_ORDER if tool in merged_text]
    if not tools:
        raise ValueError("failed to extract GLM supported tools")
    return tools


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 3:
        raise ValueError("GLM source_urls must include overview, faq, and quick start")

    activity_html = _http_get(official_url)
    overview_text = _html_to_text(_http_get(source_urls[0]))
    faq_text = _html_to_text(_http_get(source_urls[1]))
    quickstart_text = _html_to_text(_http_get(source_urls[2]))
    pricing_chunk = _load_pricing_chunk(activity_html)

    prices = _extract_month_prices(pricing_chunk)
    quotas = _extract_quota(overview_text)
    models_raw = _extract_models(overview_text)
    tools = _extract_tools(overview_text, faq_text, quickstart_text)

    packages = []
    for package_name, normalized_name in _PACKAGE_ORDER:
        packages.append(
            {
                "name": normalized_name,
                "price": prices[package_name]["price"],
                "discount": prices[package_name]["discount"],
                "quota": quotas[normalized_name],
                "models_raw": models_raw,
                "tools": tools,
                "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
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
