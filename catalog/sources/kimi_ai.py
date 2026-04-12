"""Kimi membership pricing source."""

from __future__ import annotations

import json
import logging
import time
import urllib.request
from typing import Dict, List


_PLAN_FEATURES = {
    "models_raw": ["Kimi"],
    "tools": ["Kimi Web", "Kimi App"],
    "access_method": "账号订阅（Kimi Web / App）",
    "quota": "会员订阅权益，具体额度以官方会员页展示为准",
}


LOGGER = logging.getLogger("catalog.update")


def _http_get(url: str, *, timeout_s: int = 15) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _http_post_json(
    url: str, payload: Dict[str, object], *, timeout_s: int = 15, retries: int = 2
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


def _normalize_price_in_cents(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return None


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


def _monthly_paid_goods(goods: List[Dict[str, object]]) -> List[Dict[str, object]]:
    paid_goods: List[Dict[str, object]] = []
    for item in goods:
        if not isinstance(item, dict) or not _has_monthly_variant(item):
            continue
        title = item.get("title")
        amounts = item.get("amounts")
        if not isinstance(title, str) or not title.strip():
            continue
        if (
            not isinstance(amounts, list)
            or not amounts
            or not isinstance(amounts[0], dict)
        ):
            continue
        amount = amounts[0]
        price_in_cents = _normalize_price_in_cents(amount.get("priceInCents"))
        currency = amount.get("currency")
        if currency != "CNY" or not price_in_cents:
            continue
        if item.get("membershipLevel") == "LEVEL_FREE" or price_in_cents == "0":
            continue
        paid_goods.append(item)
    paid_goods.sort(key=lambda item: int(item["amounts"][0]["priceInCents"]))
    return paid_goods


def _title_present_in_official_sources(
    membership_html: str, pricing_bundle: str, title: str
) -> bool:
    return title in membership_html or title in pricing_bundle


def _has_monthly_variant(item: Dict[str, object]) -> bool:
    billing_cycle = item.get("billingCycle")
    return (
        isinstance(billing_cycle, dict)
        and billing_cycle.get("timeUnit") == "TIME_UNIT_MONTH"
    )


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

    LOGGER.info(
        "Kimi diagnostics: goods=%d monthly_by_level=%s monthly_by_title=%s",
        len(goods),
        sorted(monthly_by_level.keys()),
        sorted(monthly_by_title.keys()),
    )

    filtered_goods = [
        item for item in goods if isinstance(item, dict) and _has_monthly_variant(item)
    ]
    LOGGER.info(
        "Kimi diagnostics: monthly variant sample=%s",
        [
            {
                "title": item.get("title"),
                "membershipLevel": item.get("membershipLevel"),
                "billingCycle": item.get("billingCycle"),
            }
            for item in filtered_goods[:6]
        ],
    )

    paid_goods = _monthly_paid_goods(goods)
    if not paid_goods:
        LOGGER.warning(
            "Kimi diagnostics: failed to find paid monthly goods; available levels=%s titles=%s",
            sorted(monthly_by_level.keys()),
            sorted(monthly_by_title.keys()),
        )
        raise ValueError("failed to find Kimi paid monthly goods")

    packages = []
    for goods_item in paid_goods:
        amounts = goods_item.get("amounts")
        if (
            not isinstance(amounts, list)
            or not amounts
            or not isinstance(amounts[0], dict)
        ):
            raise ValueError("failed to find Kimi amount for monthly goods")
        amount = amounts[0]
        price_in_cents = _normalize_price_in_cents(amount.get("priceInCents"))
        currency = amount.get("currency")
        if currency != "CNY" or not price_in_cents:
            raise ValueError("failed to parse Kimi monthly price for monthly goods")
        title = str(goods_item.get("title", "")).strip()
        if not title:
            raise ValueError("failed to find Kimi title for monthly goods")

        packages.append(
            {
                "name": f"{title}套餐",
                "price": _format_cny(price_in_cents),
                "discount": "",
                "quota": _PLAN_FEATURES["quota"],
                "models_raw": _PLAN_FEATURES["models_raw"],
                "tools": _PLAN_FEATURES["tools"],
                "access_method": _PLAN_FEATURES["access_method"],
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
