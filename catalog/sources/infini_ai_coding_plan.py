"""Infini Coding Plan source."""

from __future__ import annotations

import urllib.request
from typing import Dict, List


_PACKAGE_ORDER = [
    "Infini Coding Lite",
    "Infini Coding Pro",
]

_PACKAGE_DATA = {
    "Infini Coding Lite": {
        "name": "Lite套餐",
        "price": "¥40/月",
        "discount": "",
        "quota": "1000次请求/5小时；6000次请求/7天；12000次请求/月",
    },
    "Infini Coding Pro": {
        "name": "Pro套餐",
        "price": "¥200/月",
        "discount": "",
        "quota": "5000次请求/5小时；30000次请求/7天；60000次请求/月",
    },
}

_MODELS = [
    "deepseek-v3.2",
    "deepseek-v3.2-thinking",
    "kimi-k2.5",
    "minimax-m2.1",
    "minimax-m2.5",
    "minimax-m2.7",
    "glm-4.7",
    "glm-5",
    "glm-5.1",
]

_TOOLS = [
    "Claude Code",
    "OpenClaw",
    "VS Code Copilot",
    "Copilot CLI",
    "Cursor",
    "Trae",
    "Cline / Roo Code",
    "OpenCode",
    "Zed",
    "Factory Droid",
]


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _validate_docs(
    overview_text: str,
    models_text: str,
    cursor_text: str,
    claude_text: str,
) -> None:
    required_overview = [
        "Infini Coding Lite",
        "Infini Coding Pro",
        "40 元/月",
        "200 元/月",
        "1,000 次",
        "6,000 次",
        "12,000 次",
        "5,000 次",
        "30,000 次",
        "60,000 次",
        "OpenAI 和 Anthropic 协议",
        "sk-cp-",
        "https://cloud.infini-ai.com/maas/coding/v1",
        "https://cloud.infini-ai.com/maas/coding",
    ]
    if any(fragment not in overview_text for fragment in required_overview):
        raise ValueError("failed to confirm Infini coding plan overview")
    if any(model not in models_text for model in _MODELS):
        raise ValueError("failed to confirm Infini supported models")
    if (
        "Cursor" not in cursor_text
        or "https://cloud.infini-ai.com/maas/coding/v1" not in cursor_text
    ):
        raise ValueError("failed to confirm Infini Cursor integration doc")
    if (
        "Claude Code" not in claude_text
        or "https://cloud.infini-ai.com/maas/coding" not in claude_text
    ):
        raise ValueError("failed to confirm Infini Claude Code integration doc")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 5:
        raise ValueError(
            "Infini source_urls must include product page, overview, models, cursor doc, and claude doc"
        )

    overview_text = _http_get(source_urls[1])
    models_text = _http_get(source_urls[2])
    cursor_text = _http_get(source_urls[3])
    claude_text = _http_get(source_urls[4])
    _validate_docs(overview_text, models_text, cursor_text, claude_text)

    packages: List[Dict[str, object]] = []
    for package_name in _PACKAGE_ORDER:
        data = _PACKAGE_DATA[package_name]
        packages.append(
            {
                "name": data["name"],
                "price": data["price"],
                "discount": data["discount"],
                "quota": data["quota"],
                "models_raw": _MODELS,
                "tools": _TOOLS,
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
