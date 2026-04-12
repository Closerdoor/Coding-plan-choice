"""XFYun Xingchen Coding Plan source.

The package subscription page is a login-gated SPA. Runtime APIs for concrete
packages require authentication, so this source keeps to official facts that can
be verified anonymously from the public entry page and bundle.
"""

from __future__ import annotations

import urllib.request
from typing import Dict


_PACKAGE_DATA = {
    "name": "Coding Plan套餐",
    "price": "价格以登录后官方套餐页为准",
    "discount": "",
    "quota": "官方静态文案可确认平台赠送 500w tokens + 2QPS；启用后付费后按实际调用实时扣费",
    "models_raw": [],
    "tools": ["HTTP API", "WebSocket API"],
    "access_method": "服务认证信息 + 接口地址（Http / WebSocket 协议）",
}


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _validate_page_and_bundle(page_html: str, bundle_text: str) -> None:
    page_required = ["讯飞星辰MaaS平台-官网", "/js/index-68edb439.js"]
    bundle_markers = [
        "/packageSubscription",
        "/api/v1/gpt-finetune/coding-plan/package",
        "/api/v1/gpt-finetune/coding-plan/list",
        "500w tokens",
        "2QPS",
        "Http protocol",
        "WebSocket protocol",
        "API address",
        "Authentication information",
        "Enable post-paid",
    ]
    if any(fragment not in page_html for fragment in page_required):
        raise ValueError("failed to confirm XFYun package subscription page")
    matched = sum(1 for fragment in bundle_markers if fragment in bundle_text)
    if matched < 7:
        raise ValueError("failed to confirm XFYun coding plan bundle")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 2:
        raise ValueError("XFYun source_urls must include package page and bundle")

    page_html = _http_get(source_urls[0])
    bundle_text = _http_get(source_urls[1])
    _validate_page_and_bundle(page_html, bundle_text)

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "plan_name": config["plan_name"],
        "official_url": official_url,
        "source_urls": source_urls,
        "packages": [dict(_PACKAGE_DATA)],
    }
