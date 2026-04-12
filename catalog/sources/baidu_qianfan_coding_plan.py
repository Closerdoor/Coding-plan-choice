"""Baidu Qianfan Coding Plan source."""

from __future__ import annotations

import json
import re
import time
import urllib.request
from typing import Dict, List


_MODEL_ORDER = [
    "Kimi-K2.5",
    "DeepSeek-V3.2",
    "GLM-5",
    "MiniMax-M2.5",
    "ERNIE-4.5-Turbo-20260402",
]

_TOOL_ORDER = [
    "OpenClaw",
    "Claude Code",
    "Qwen Code",
    "Cursor",
]


def _http_get(url: str, *, timeout_s: int = 120, retries: int = 4) -> str:
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
    raise RuntimeError(f"failed to fetch Baidu url: {url}: {last_exc}")


def _load_activity_payload(activity_url: str) -> Dict[str, object]:
    html = _http_get(activity_url)
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(?P<json>.*?)</script>',
        html,
        re.S,
    )
    if not match:
        raise ValueError("failed to locate Baidu activity __NEXT_DATA__")
    return json.loads(match.group("json"))


def _load_doc_html(doc_url: str) -> str:
    page_html = _http_get(doc_url)
    match = re.search(
        r'href="(?P<url>https://bce\.bdstatic\.com/p3m/bce-doc/online/qianfan/doc/qianfan/s/page-data/imlg0beiu/page-data\.json)"',
        page_html,
    )
    page_data_url = (
        match.group("url")
        if match
        else (
            "https://bce.bdstatic.com/p3m/bce-doc/online/qianfan/doc/qianfan/s/page-data/imlg0beiu/page-data.json"
        )
    )
    payload = json.loads(_http_get(page_data_url))
    html = (
        payload.get("result", {})
        .get("data", {})
        .get("markdownRemark", {})
        .get("html", "")
    )
    if not isinstance(html, str) or not html.strip():
        raise ValueError("failed to locate Baidu doc HTML payload")
    return html


def _find_activity_module(
    activity_payload: Dict[str, object], module_type: str
) -> Dict[str, object]:
    modules = activity_payload.get("props", {}).get("pageProps", {}).get("modules", [])
    if not isinstance(modules, list):
        raise ValueError("invalid Baidu activity modules payload")
    for module in modules:
        if isinstance(module, dict) and module.get("type") == module_type:
            return module
    raise ValueError(f"failed to locate Baidu activity module: {module_type}")


def _normalize_package_name(name: str) -> str:
    compact = re.sub(r"\s+", " ", name).strip().lower()
    if "lite" in compact:
        return "lite套餐"
    if "pro" in compact:
        return "pro套餐"
    raise ValueError(f"unknown Baidu package name: {name}")


def _extract_discounts(activity_payload: Dict[str, object]) -> Dict[str, str]:
    module = _find_activity_module(activity_payload, "V6G022")
    tabs = module.get("data", {}).get("render", {}).get("tabs", [])
    if not isinstance(tabs, list) or not tabs:
        raise ValueError("failed to locate Baidu discount tabs")
    items = tabs[0].get("items", []) if isinstance(tabs[0], dict) else []
    list_content = tabs[0].get("listContent", []) if isinstance(tabs[0], dict) else []
    if (
        not isinstance(items, list)
        or not isinstance(list_content, list)
        or not list_content
    ):
        raise ValueError("failed to locate Baidu discount list content")

    price_row = (
        list_content[0].get("lists", []) if isinstance(list_content[0], dict) else []
    )
    if not isinstance(price_row, list) or len(price_row) < 3:
        raise ValueError("failed to extract Baidu discount prices")

    package_names: List[str] = []
    for item in items[:2]:
        if not isinstance(item, dict):
            continue
        title = item.get("title")
        if isinstance(title, str):
            package_names.append(_normalize_package_name(title))
    if len(package_names) != 2:
        raise ValueError("failed to map Baidu discount package names")

    discounts: Dict[str, str] = {}
    for index, package_name in enumerate(package_names, start=1):
        line = str(price_row[index]).strip()
        match = re.search(r"新客\s*([0-9.]+)元/首月", line)
        if not match:
            raise ValueError(f"failed to extract Baidu discount for {package_name}")
        discounts[package_name] = f"首月¥{match.group(1)}/月"
    return discounts


def _extract_doc_section(doc_html: str, start_heading: str, end_heading: str) -> str:
    start = doc_html.find(start_heading)
    if start == -1:
        raise ValueError(f"failed to locate Baidu doc section: {start_heading}")
    end = doc_html.find(end_heading, start)
    if end == -1:
        end = len(doc_html)
    return doc_html[start:end]


def _clean_html_text(value: str) -> str:
    text = value.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _normalize_quota_line(line: str) -> str:
    compact = line.replace(",", "").replace(" ", "")
    compact = compact.replace("每5小时：最多约", "")
    compact = compact.replace("每周：最多约", "")
    compact = compact.replace("每订阅月：最多约", "")
    return compact


def _extract_packages(doc_html: str) -> Dict[str, Dict[str, str]]:
    section = _extract_doc_section(
        doc_html, '<h3 id="套餐价格与限额">', '<h3 id="套餐额度刷新规则">'
    )
    pattern = re.compile(
        r"<tr>\s*<td><strong>(?P<name>[^<]+)</strong></td>\s*<td>(?P<price>[^<]+)</td>\s*<td>(?P<quota>.*?)</td>\s*</tr>",
        re.S,
    )
    packages: Dict[str, Dict[str, str]] = {}
    for match in pattern.finditer(section):
        package_name = _normalize_package_name(match.group("name"))
        raw_price = _clean_html_text(match.group("price"))
        price_match = re.search(r"([0-9.]+)", raw_price)
        if not price_match:
            raise ValueError(f"failed to extract Baidu price for {package_name}")
        quota_lines = [
            _clean_html_text(part)
            for part in re.split(r"<br\s*/?>", match.group("quota"))
            if _clean_html_text(part)
        ]
        normalized_quota = [_normalize_quota_line(line) for line in quota_lines]
        if len(normalized_quota) != 3:
            raise ValueError(f"failed to normalize Baidu quota for {package_name}")
        packages[package_name] = {
            "price": f"¥{price_match.group(1)}/月",
            "quota": (
                f"{normalized_quota[0]}/5小时；"
                f"{normalized_quota[1]}/周；"
                f"{normalized_quota[2]}/月"
            ),
        }
    if set(packages) != {"lite套餐", "pro套餐"}:
        raise ValueError("failed to extract Baidu package table")
    return packages


def _extract_models(doc_html: str) -> List[str]:
    section = _extract_doc_section(
        doc_html, '<h3 id="支持的模型">', '<h2 id="订阅套餐">'
    )
    models = [model for model in _MODEL_ORDER if model in section]
    if not models:
        raise ValueError("failed to extract Baidu supported models")
    return models


def _extract_tools(doc_html: str) -> List[str]:
    tools = [tool for tool in _TOOL_ORDER if tool in doc_html]
    if not tools:
        raise ValueError("failed to extract Baidu supported tools")
    return tools


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 1:
        raise ValueError("Baidu source_urls must include document page")

    activity_payload = _load_activity_payload(official_url)
    doc_html = _load_doc_html(source_urls[0])
    packages = _extract_packages(doc_html)
    discounts = _extract_discounts(activity_payload)
    models_raw = _extract_models(doc_html)
    tools = _extract_tools(doc_html)

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "plan_name": config["plan_name"],
        "official_url": official_url,
        "source_urls": source_urls,
        "packages": [
            {
                "name": "lite套餐",
                "price": packages["lite套餐"]["price"],
                "discount": discounts["lite套餐"],
                "quota": packages["lite套餐"]["quota"],
                "models_raw": models_raw,
                "tools": tools,
                "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
            },
            {
                "name": "pro套餐",
                "price": packages["pro套餐"]["price"],
                "discount": discounts["pro套餐"],
                "quota": packages["pro套餐"]["quota"],
                "models_raw": models_raw,
                "tools": tools,
                "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
            },
        ],
    }
