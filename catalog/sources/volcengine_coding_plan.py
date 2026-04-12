"""Volcengine Coding Plan source."""

from __future__ import annotations

import html
import re
import urllib.request
from typing import Dict, List


SOURCE_NAME = "volcengine-coding-plan"

_MODEL_ORDER = [
    "Auto",
    "Doubao-Seed-2.0-pro",
    "Doubao-Seed-2.0-lite",
    "Doubao-Seed-2.0-Code",
    "Doubao-Seed-Code",
    "MiniMax-M2.5",
    "Kimi-K2.5",
    "GLM-4.7",
    "DeepSeek-V3.2",
]

_TOOL_ORDER = [
    "OpenClaw",
    "Claude Code",
    "Cursor",
    "Cline",
    "Codex CLI",
    "Kilo Code",
    "Roo Code",
    "OpenCode",
]

_LITE_ANCHORS = [
    "configurationCode:'Coding_Plan_Lite_monthly'",
    "templateIndexKey:'ark_bd||cu3pq57og65ta2ostdvg'",
]

_PRO_ANCHORS = [
    "configurationCode:'Coding_Plan_Pro_monthly'",
    "templateIndexKey:'ark_bd||d2a7m37ditkldl312h1g'",
]


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _extract_bundle_url(activity_html: str) -> str:
    pattern = re.compile(
        r'"name":"activity/codingplan".*?"source_url":"(?P<url>[^"]+)"',
        re.S,
    )
    match = pattern.search(activity_html)
    if not match:
        raise ValueError("failed to locate Volcengine coding plan bundle URL")
    url = html.unescape(match.group("url"))
    if url.startswith("//"):
        return "https:" + url
    return url


def _extract_anchor_block(bundle_text: str, anchors: List[str]) -> str:
    anchor_pos = -1
    for anchor in anchors:
        anchor_pos = bundle_text.find(anchor)
        if anchor_pos != -1:
            break
    if anchor_pos == -1:
        raise ValueError(f"failed to locate Volcengine plan anchor: {anchors[0]}")

    start = bundle_text.rfind("name:'方舟 Coding Plan", 0, anchor_pos)
    if start == -1:
        start = max(anchor_pos - 2500, 0)

    next_name = bundle_text.find("name:'方舟 Coding Plan", anchor_pos + 1)
    next_meta = bundle_text.find("__meta__", anchor_pos + 1)
    end_candidates = [
        pos for pos in (next_name, next_meta) if pos != -1 and pos > anchor_pos
    ]
    end = (
        min(end_candidates)
        if end_candidates
        else min(len(bundle_text), anchor_pos + 6000)
    )
    return bundle_text[start:end]


def _extract_price(block: str) -> Dict[str, str]:
    price_block_match = re.search(r"priceConfig:\{(?P<body>[^}]+)\}", block)
    if not price_block_match:
        raise ValueError("failed to extract Volcengine pricing")
    price_body = price_block_match.group("body")
    original_match = re.search(r"originalAmount:'(?P<original>[^']+)'", price_body)
    discount_match = re.search(r"discountAmount:'(?P<discount>[0-9.]+)'", price_body)
    if not original_match or not discount_match:
        raise ValueError("failed to extract Volcengine pricing")
    original = original_match.group("original")
    base = original.split("/")[0].strip().replace("\u00a5", "").replace("¥", "")
    return {
        "price": f"¥{base}/月",
        "discount": f"首月¥{discount_match.group('discount')}/月",
    }


def _extract_usage(block: str) -> str:
    match = re.search(
        r"title:'用量',rightContents:\[\[\{text:'(?P<usage>[^']+)'",
        block,
    )
    if not match:
        raise ValueError("failed to extract Volcengine usage description")
    return match.group("usage").strip()


def _extract_activity_models(bundle_text: str) -> List[str]:
    match = re.search(
        r"title:'集合最新主流国产编程模型'.{0,800}?description:'(?P<description>[^']+)'",
        bundle_text,
        re.S,
    )
    model_source = match.group("description") if match else bundle_text
    normalized_source = model_source.replace("Deepseek-V3.2", "DeepSeek-V3.2")
    models = [model for model in _MODEL_ORDER if model in normalized_source]
    return models


def _extract_tools(activity_text: str, doc_text: str) -> List[str]:
    activity_match = re.search(
        r"title:'多生态兼容，无缝融入您的工具链'.{0,800}?description:'(?P<description>[^']+)'",
        activity_text,
        re.S,
    )
    merged_text = (
        (activity_match.group("description") if activity_match else activity_text)
        + "\n"
        + doc_text
    )
    tools = [tool for tool in _TOOL_ORDER if tool in merged_text]
    if not tools:
        raise ValueError("failed to extract Volcengine tools")
    return tools


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    source_urls = config["source_urls"]
    activity_html = _http_get(source_urls[0])
    doc_html = _http_get(source_urls[1])
    bundle_url = _extract_bundle_url(activity_html)
    bundle_text = _http_get(bundle_url)

    lite_block = _extract_anchor_block(bundle_text, _LITE_ANCHORS)
    pro_block = _extract_anchor_block(bundle_text, _PRO_ANCHORS)
    lite_price = _extract_price(lite_block)
    pro_price = _extract_price(pro_block)

    models_raw = _extract_activity_models(bundle_text)
    tools = _extract_tools(bundle_text, doc_html)

    packages = [
        {
            "name": "lite套餐",
            "price": lite_price["price"],
            "discount": lite_price["discount"],
            "quota": _extract_usage(lite_block),
            "models_raw": models_raw,
            "tools": tools,
            "access_method": "API Key",
        },
        {
            "name": "pro套餐",
            "price": pro_price["price"],
            "discount": pro_price["discount"],
            "quota": _extract_usage(pro_block),
            "models_raw": models_raw,
            "tools": tools,
            "access_method": "API Key",
        },
    ]

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "vendor_name": config["vendor_name"],
        "official_sources": source_urls,
        "packages": packages,
    }
