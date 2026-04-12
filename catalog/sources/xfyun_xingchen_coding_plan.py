"""XFYun Xingchen Coding Plan source.

This vendor requires an authenticated session. The source reads a single
`XFYUN_SSO_SESSION_ID` environment variable, verifies the session, then fetches
the official package list.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Dict, List


SESSION_ENV = "XFYUN_SSO_SESSION_ID"
USERINFO_URL = "https://maas.xfyun.cn/herapi/user/getUserinfo"
PACKAGE_API_URL = "https://maas.xfyun.cn/api/v1/gpt-finetune/coding-plan/package"
PACKAGE_PAGE_URL = (
    "https://maas.xfyun.cn/packageSubscription?from=packageSubscriptionOverlay"
)


class XFYunAuthError(RuntimeError):
    """Raised when the authenticated XFYun session is missing or invalid."""


def _cookie_header(session_id: str) -> str:
    return f"ssoSessionId={session_id.strip()}"


def _http_get_json(
    url: str, *, referer: str, session_id: str, timeout_s: int = 60
) -> Dict[str, object]:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Cookie": _cookie_header(session_id),
        "Referer": referer,
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as response:
            return json.loads(response.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise XFYunAuthError(f"XFYun request failed: {exc.code}: {detail}") from exc


def _require_session_id() -> str:
    session_id = os.environ.get(SESSION_ENV, "").strip()
    if not session_id:
        raise XFYunAuthError(f"missing required environment variable {SESSION_ENV}")
    return session_id


def _verify_session(session_id: str) -> None:
    payload = _http_get_json(
        USERINFO_URL,
        referer="https://maas.xfyun.cn/botIm?origin=maas",
        session_id=session_id,
    )
    if payload.get("code") != 0 or not payload.get("flag"):
        raise XFYunAuthError(f"XFYun session is invalid: {payload}")


def _price_text(amount_fen: object) -> str:
    if not isinstance(amount_fen, int):
        raise ValueError(f"unexpected XFYun price value: {amount_fen!r}")
    amount_yuan = amount_fen / 100
    if amount_yuan.is_integer():
        return f"¥{int(amount_yuan)}/月"
    return f"¥{amount_yuan:g}/月"


def _discount_text(detail: Dict[str, object]) -> str:
    activity = detail.get("activity")
    real_fee = detail.get("realFee")
    if not isinstance(activity, dict) or not isinstance(real_fee, int):
        return ""
    if real_fee >= detail.get("price", real_fee):
        return ""
    return f"首单优惠后 {_price_text(real_fee)}"


def _quota_text(package: Dict[str, object]) -> str:
    benefits = package.get("benefits")
    if not isinstance(benefits, list):
        raise ValueError("unexpected XFYun benefits payload")
    cleaned = [str(item).strip() for item in benefits if str(item).strip()]
    if not cleaned:
        raise ValueError("unexpected empty XFYun package benefits")
    return "；".join(cleaned)


def _models_text(package: Dict[str, object]) -> List[str]:
    models = package.get("supportedModels")
    if not isinstance(models, list):
        raise ValueError("unexpected XFYun model list payload")
    names = []
    for item in models:
        if not isinstance(item, dict):
            continue
        model_name = str(item.get("name", "")).strip()
        if model_name:
            names.append(model_name)
    if not names:
        raise ValueError("unexpected empty XFYun model list")
    return names


def _build_package(package: Dict[str, object]) -> Dict[str, object]:
    name = str(package.get("name", "")).strip()
    detail = package.get("detail")
    if not name or not isinstance(detail, dict):
        raise ValueError("unexpected XFYun package payload")
    return {
        "name": f"{name}套餐",
        "price": _price_text(detail.get("price")),
        "discount": _discount_text(detail),
        "quota": _quota_text(package),
        "models_raw": _models_text(package),
        "tools": ["HTTP API", "WebSocket API"],
        "access_method": "服务认证信息 + 接口地址（Http / WebSocket 协议）",
    }


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    session_id = _require_session_id()
    _verify_session(session_id)

    payload = _http_get_json(
        PACKAGE_API_URL, referer=PACKAGE_PAGE_URL, session_id=session_id
    )
    data = payload.get("data")
    if payload.get("code") != 0 or not isinstance(data, list) or not data:
        raise ValueError(f"unexpected XFYun package response: {payload}")

    packages = [_build_package(item) for item in data if isinstance(item, dict)]
    if not packages:
        raise ValueError("unexpected empty XFYun package list")

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "plan_name": config["plan_name"],
        "official_url": config["official_url"],
        "source_urls": config["source_urls"],
        "packages": packages,
    }
