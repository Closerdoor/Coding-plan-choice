"""Xiaomi MiMo Token Plan source.

The token-plan markdown pages linked from llms.txt currently return 404 in this
environment. This source therefore validates stable official resources at runtime
and uses curated package facts already confirmed from Xiaomi's official token-plan
SPA bundle and docs.
"""

from __future__ import annotations

import re
import urllib.request
from typing import Dict


_PACKAGE_ORDER = [
    "Lite套餐",
    "Standard套餐",
    "Pro套餐",
    "Max套餐",
]

_PACKAGE_DATA = {
    "Lite套餐": {
        "price": "$6/月",
        "discount": "首购88折",
        "quota": "60M Credits；MiMo-V2-Omni <256K 按1x消耗，MiMo-V2-Pro <256K 按2x消耗，256K-1M 按4x消耗；MiMo-V2-TTS 限时免费",
    },
    "Standard套餐": {
        "price": "$16/月",
        "discount": "首购88折",
        "quota": "200M Credits；MiMo-V2-Omni <256K 按1x消耗，MiMo-V2-Pro <256K 按2x消耗，256K-1M 按4x消耗；MiMo-V2-TTS 限时免费",
    },
    "Pro套餐": {
        "price": "$50/月",
        "discount": "首购88折",
        "quota": "700M Credits；MiMo-V2-Omni <256K 按1x消耗，MiMo-V2-Pro <256K 按2x消耗，256K-1M 按4x消耗；MiMo-V2-TTS 限时免费",
    },
    "Max套餐": {
        "price": "$100/月",
        "discount": "首购88折",
        "quota": "1600M Credits；MiMo-V2-Omni <256K 按1x消耗，MiMo-V2-Pro <256K 按2x消耗，256K-1M 按4x消耗；MiMo-V2-TTS 限时免费",
    },
}

_MODELS = ["MiMo-V2-Pro", "MiMo-V2-Omni", "MiMo-V2-TTS"]

_TOOLS = [
    "OpenCode",
    "Claude Code",
    "OpenClaw",
    "Cline",
    "Kilo Code",
    "Roo Code",
    "Codex CLI",
    "Zed",
    "Cherry Studio",
    "Qwen Code",
]


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _resolve_bundle_url(official_url: str, fallback_url: str) -> str:
    page_html = _http_get(official_url)
    match = re.search(
        r'href="(?P<bundle>main\.[a-f0-9]+\.chunk\.js)"\s+as="script"', page_html
    )
    if match:
        bundle = match.group("bundle")
        return f"https://platform.xiaomimimo.com/{bundle}"
    return fallback_url


def _validate_bundle(bundle_text: str) -> None:
    required_fragments = [
        "Xiaomi MiMo Token Plan",
        "88 ",
        "Lite/Standard/Pro/Max",
        "MiMo-V2-Pro",
        "MiMo-V2-Omni",
        "MiMo-V2-TTS",
        "shared",
        "$6",
        "$16",
        "$50",
        "$100",
    ]
    if any(fragment not in bundle_text for fragment in required_fragments):
        raise ValueError("failed to confirm Xiaomi token plan bundle")


def _validate_docs(
    llms_text: str, pricing_text: str, openai_text: str, faq_text: str
) -> None:
    if "Subscription Instructions" not in llms_text or "Quick Access" not in llms_text:
        raise ValueError("failed to confirm Xiaomi token plan docs index")
    if "MiMo-V2-Pro" not in pricing_text or "MiMo-V2-Omni" not in pricing_text:
        raise ValueError("failed to confirm Xiaomi pricing doc")
    if "https://api.xiaomimimo.com/v1/chat/completions" not in openai_text:
        raise ValueError("failed to confirm Xiaomi OpenAI-compatible API doc")
    if "API Key" not in faq_text or "OpenAI and Anthropic interfaces" not in faq_text:
        raise ValueError("failed to confirm Xiaomi FAQ")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 5:
        raise ValueError(
            "Xiaomi source_urls must include llms index, bundle, pricing doc, API doc, and FAQ"
        )

    llms_text = _http_get(source_urls[0])
    bundle_url = _resolve_bundle_url(str(official_url), source_urls[1])
    bundle_text = _http_get(bundle_url)
    pricing_text = _http_get(source_urls[2])
    openai_text = _http_get(source_urls[3])
    faq_text = _http_get(source_urls[4])

    if "token-plan" not in str(official_url):
        raise ValueError("failed to confirm Xiaomi token plan official url")

    _validate_bundle(bundle_text)
    _validate_docs(llms_text, pricing_text, openai_text, faq_text)

    packages = []
    for package_name in _PACKAGE_ORDER:
        data = _PACKAGE_DATA[package_name]
        packages.append(
            {
                "name": package_name,
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
