"""Cursor pricing source."""

from __future__ import annotations

import html
import re
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List


_PACKAGE_ORDER = [
    ("Pro", "Pro套餐"),
    ("Pro+", "Pro+套餐"),
    ("Ultra", "Ultra套餐"),
]

_MODEL_ORDER = [
    "Auto",
    "Composer 2",
    "Claude 4 Sonnet",
    "Claude 4 Sonnet 1M",
    "Claude 4.5 Haiku",
    "Claude 4.5 Opus",
    "Claude 4.5 Sonnet",
    "Claude 4.6 Opus",
    "Claude 4.6 Opus (Fast mode)",
    "Claude 4.6 Sonnet",
    "Composer 1",
    "Composer 1.5",
    "Gemini 2.5 Flash",
    "Gemini 3 Flash",
    "Gemini 3 Pro",
    "Gemini 3 Pro Image Preview",
    "Gemini 3.1 Pro",
    "GPT-5",
    "GPT-5 Fast",
    "GPT-5 Mini",
    "GPT-5-Codex",
    "GPT-5.1 Codex",
    "GPT-5.1 Codex Max",
    "GPT-5.1 Codex Mini",
    "GPT-5.2",
    "GPT-5.2 Codex",
    "GPT-5.3 Codex",
    "GPT-5.4",
    "GPT-5.4 Mini",
    "GPT-5.4 Nano",
    "Grok 4.20",
    "Kimi K2.5",
]

_TOOL_ORDER = [
    "Cursor Desktop",
    "Cursor Web",
    "Slack",
    "GitHub",
    "Linear",
    "API",
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


def _fetch_doc_text(url: str) -> str:
    doc_url = url
    if url.startswith("https://cursor.com/docs/") and not url.endswith(".md"):
        doc_url = url + ".md"
    return _http_get(doc_url)


def _extract_price(pricing_text: str, package_name: str) -> str:
    if package_name == "Pro":
        match = re.search(r"Pro\s*\$\s*20\s*/\s*mo", pricing_text)
        if match:
            return "$20/月"
    if package_name == "Pro+":
        match = re.search(r"Pro\+\s*Recommended\s*\$\s*60\s*/\s*mo", pricing_text)
        if match:
            return "$60/月"
    if package_name == "Ultra":
        match = re.search(r"Ultra\s*\$\s*200\s*/\s*mo", pricing_text)
        if match:
            return "$200/月"
    raise ValueError(f"failed to extract Cursor price for {package_name}")


def _extract_quota(models_text: str, package_name: str) -> str:
    quotas = {
        "Pro": "月含 $20 API usage；超出后按模型 Token 单价计费",
        "Pro+": "月含 $70 API usage；超出后按模型 Token 单价计费",
        "Ultra": "月含 $400 API usage；超出后按模型 Token 单价计费",
    }
    expected = {
        "Pro": "$20",
        "Pro+": "$70",
        "Ultra": "$400",
    }
    if expected[package_name] not in models_text:
        raise ValueError(f"failed to confirm Cursor included usage for {package_name}")
    return quotas[package_name]


def _extract_models(models_text: str) -> List[str]:
    models = [model for model in _MODEL_ORDER if model in models_text]
    if len(models) < 8:
        raise ValueError("failed to extract Cursor supported models")
    return models


def _extract_tools(*texts: str) -> List[str]:
    merged = "\n".join(texts)
    required_tokens = {
        "Cursor Desktop": "Cursor Desktop",
        "Cursor Web": "Cursor Web",
        "Slack": "Slack",
        "GitHub": "GitHub",
        "Linear": "Linear",
        "API": "API",
    }
    tools = [tool for tool in _TOOL_ORDER if required_tokens[tool] in merged]
    if len(tools) < 4:
        raise ValueError("failed to extract Cursor supported tools")
    return tools


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 3:
        raise ValueError(
            "Cursor source_urls must include model pricing, dashboard, and cloud agent docs"
        )

    pricing_text = _html_to_text(_http_get(official_url))
    models_text = _fetch_doc_text(source_urls[0])
    dashboard_text = _fetch_doc_text(source_urls[1])
    cloud_agent_text = _fetch_doc_text(source_urls[2])

    if "Pricing" not in pricing_text or "Cloud agents" not in pricing_text:
        raise ValueError("failed to confirm Cursor pricing page")
    if "Models & Pricing" not in models_text:
        raise ValueError("failed to confirm Cursor models page")

    models_raw = _extract_models(models_text)
    tools = _extract_tools(pricing_text, dashboard_text, cloud_agent_text)

    packages = []
    for package_name, normalized_name in _PACKAGE_ORDER:
        packages.append(
            {
                "name": normalized_name,
                "price": _extract_price(pricing_text, package_name),
                "discount": "",
                "quota": _extract_quota(models_text, package_name),
                "models_raw": models_raw,
                "tools": tools,
                "access_method": "账号订阅（Cursor 客户端 / Web）",
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
