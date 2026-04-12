"""Kimi membership pricing source."""

from __future__ import annotations

import json
import time
import urllib.request
from typing import Dict, List


_PACKAGE_ORDER = [
    ("LEVEL_TRIAL", "Andante套餐"),
    ("LEVEL_BASIC", "Moderato套餐"),
    ("LEVEL_INTERMEDIATE", "Allegretto套餐"),
    ("LEVEL_ADVANCED", "Allegro套餐"),
]

_PLAN_FEATURES = {
    "Andante套餐": {
        "models_raw": ["Kimi"],
        "tools": ["Kimi Web", "Kimi App"],
        "access_method": "账号订阅（Kimi Web / App）",
        "quota": "会员订阅权益，具体额度以官方会员页展示为准",
    },
    "Moderato套餐": {
        "models_raw": ["Kimi"],
        "tools": ["Kimi Web", "Kimi App"],
        "access_method": "账号订阅（Kimi Web / App）",
        "quota": "会员订阅权益，具体额度以官方会员页展示为准",
    },
    "Allegretto套餐": {
        "models_raw": ["Kimi"],
        "tools": ["Kimi Web", "Kimi App"],
        "access_method": "账号订阅（Kimi Web / App）",
        "quota": "会员订阅权益，具体额度以官方会员页展示为准",
    },
    "Allegro套餐": {
        "models_raw": ["Kimi"],
        "tools": ["Kimi Web", "Kimi App"],
        "access_method": "账号订阅（Kimi Web / App）",
        "quota": "会员订阅权益，具体额度以官方会员页展示为准",
    },
}

_TITLE_BY_LEVEL = {
    "LEVEL_TRIAL": "Andante",
    "LEVEL_BASIC": "Moderato",
    "LEVEL_INTERMEDIATE": "Allegretto",
    "LEVEL_ADVANCED": "Allegro",
}


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _http_post_json(
    url: str, payload: Dict[str, object], *, timeout_s: int = 60, retries: int = 3
) -> Dict[str, object]:
    last_exc: Exception | None = None
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "X-Language": "zh-CN",
        "x-msh-platform": "web",
        "User-Agent": "Mozilla/5.0",
    }
    for attempt in range(retries):
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as response:
                return json.loads(response.read().decode("utf-8", "replace"))
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            if attempt == retries - 1:
                raise
            time.sleep(1 + attempt)
    raise RuntimeError(f"failed to fetch Kimi goods: {last_exc}")


def _format_cny(price_in_cents: str) -> str:
    amount = int(price_in_cents)
    yuan = amount / 100
    if yuan.is_integer():
        return f"¥{int(yuan)}/月"
    return f"¥{yuan:.2f}/月"


def _pick_monthly_goods(goods: List[Dict[str, object]]) -> Dict[str, Dict[str, object]]:
    monthly_by_level: Dict[str, Dict[str, object]] = {}
    for item in goods:
        if not isinstance(item, dict):
            continue
        billing_cycle = item.get("billingCycle")
        if not isinstance(billing_cycle, dict):
            continue
        if billing_cycle.get("timeUnit") != "TIME_UNIT_MONTH":
            continue
        level = item.get("membershipLevel")
        if isinstance(level, str):
            monthly_by_level[level] = item
    return monthly_by_level


def _pick_monthly_goods_by_title(
    goods: List[Dict[str, object]],
) -> Dict[str, Dict[str, object]]:
    monthly_by_title: Dict[str, Dict[str, object]] = {}
    for item in goods:
        if not isinstance(item, dict):
            continue
        billing_cycle = item.get("billingCycle")
        if not isinstance(billing_cycle, dict):
            continue
        if billing_cycle.get("timeUnit") != "TIME_UNIT_MONTH":
            continue
        title = item.get("title")
        if isinstance(title, str) and title.strip():
            monthly_by_title[title.strip()] = item
    return monthly_by_title


def _title_present_in_official_sources(
    membership_html: str, pricing_bundle: str, title: str
) -> bool:
    return title in membership_html or title in pricing_bundle


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 4:
        raise ValueError("Kimi membership source_urls must include goods API")

    membership_html = _http_get(official_url)
    pricing_bundle = _http_get(source_urls[2])
    goods_payload = _http_post_json(source_urls[3], {"page_size": 0, "page_token": ""})

    if "kimi-web-seo" not in membership_html:
        raise ValueError("failed to confirm Kimi membership page")
    if "subscriptionPrice" not in pricing_bundle or "plan.title" not in pricing_bundle:
        raise ValueError("failed to confirm Kimi membership pricing bundle")

    goods = goods_payload.get("goods")
    if not isinstance(goods, list) or not goods:
        raise ValueError("failed to load Kimi membership goods")

    monthly_by_level = _pick_monthly_goods(goods)
    monthly_by_title = _pick_monthly_goods_by_title(goods)

    packages = []
    for level, normalized_name in _PACKAGE_ORDER:
        goods_item = monthly_by_level.get(level)
        if not goods_item:
            title = _TITLE_BY_LEVEL[level]
            if _title_present_in_official_sources(
                membership_html, pricing_bundle, title
            ):
                goods_item = monthly_by_title.get(title)
        if not goods_item:
            raise ValueError(f"failed to find Kimi monthly goods for {level}")
        amounts = goods_item.get("amounts")
        if (
            not isinstance(amounts, list)
            or not amounts
            or not isinstance(amounts[0], dict)
        ):
            raise ValueError(f"failed to find Kimi amount for {level}")
        amount = amounts[0]
        price_in_cents = amount.get("priceInCents")
        currency = amount.get("currency")
        if currency != "CNY" or not isinstance(price_in_cents, str):
            raise ValueError(f"failed to parse Kimi monthly price for {level}")

        features = _PLAN_FEATURES[normalized_name]
        packages.append(
            {
                "name": normalized_name,
                "price": _format_cny(price_in_cents),
                "discount": "",
                "quota": features["quota"],
                "models_raw": features["models_raw"],
                "tools": features["tools"],
                "access_method": features["access_method"],
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
