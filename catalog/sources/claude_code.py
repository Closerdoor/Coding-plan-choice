"""Claude Code pricing source."""

from __future__ import annotations

import time
import urllib.request
from typing import Dict, List


_PACKAGE_ORDER = [
    "Pro套餐",
    "Max 5x套餐",
    "Max 20x套餐",
    "Team Standard Seat",
    "Team Premium Seat",
    "Enterprise Seat",
]

_PACKAGE_DATA = {
    "Pro套餐": {
        "price": "$20/月",
        "quota": "包含 Claude Code；比 Free 更多 usage",
    },
    "Max 5x套餐": {
        "price": "$100/月",
        "quota": "包含 Claude Code；较 Pro 提供 5x usage per session",
    },
    "Max 20x套餐": {
        "price": "$200/月",
        "quota": "包含 Claude Code；较 Pro 提供 20x usage per session",
    },
    "Team Standard Seat": {
        "price": "$20/seat/月（年付）或 $25/seat/月（月付）",
        "quota": "包含 Claude Code；All Claude features, plus more usage than Pro",
    },
    "Team Premium Seat": {
        "price": "$100/seat/月（年付）或 $125/seat/月（月付）",
        "quota": "包含 Claude Code；较 Team Standard 提供更多 usage",
    },
    "Enterprise Seat": {
        "price": "$20/seat + usage at API rates",
        "quota": "包含 Claude Code；组织可设置 user/org spend limits，使用量按模型与任务扩展",
    },
}

_MODELS = ["Opus", "Sonnet", "Haiku"]

_TOOLS = ["Terminal CLI", "VS Code", "JetBrains", "Desktop app", "Web"]


def _http_get(url: str, *, timeout_s: int = 60, retries: int = 3) -> str:
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
    raise RuntimeError(f"failed to fetch Claude source: {url}: {last_exc}")


def _validate_sources(
    pricing_text: str,
    max_text: str,
    team_text: str,
    enterprise_text: str,
    overview_text: str,
    usage_text: str,
    max_help_text: str,
) -> None:
    pricing_markers = [
        "Includes Claude Code",
        "$20",
        "From $100",
        "Max 5x",
        "Max 20x",
        "Seat price + usage at API rates",
        "usage at API rates",
    ]
    if sum(1 for fragment in pricing_markers if fragment in pricing_text) < 6:
        raise ValueError("failed to confirm Claude pricing overview")
    if any(
        fragment not in max_text for fragment in ["Max 5x", "$100", "Max 20x", "$200"]
    ):
        raise ValueError("failed to confirm Claude Max pricing")
    if any(
        fragment not in team_text
        for fragment in ["Standard seat", "$20", "Premium seat", "$100", "Claude Code"]
    ):
        raise ValueError("failed to confirm Claude Team pricing")
    enterprise_markers = ["Claude Code", "Enterprise", "subscription"]
    if any(fragment not in enterprise_text for fragment in enterprise_markers):
        raise ValueError("failed to confirm Claude Enterprise pricing")
    if any(
        fragment not in overview_text
        for fragment in [
            "Claude Code overview",
            "terminal, IDE, desktop app, and browser",
        ]
    ):
        raise ValueError("failed to confirm Claude Code overview")
    if any(
        fragment not in usage_text
        for fragment in ["Pro or Max", "shared across Claude and Claude Code"]
    ):
        raise ValueError("failed to confirm Claude Code usage doc")
    if any(
        fragment not in max_help_text
        for fragment in ["Max 5x", "$100 per month", "Max 20x", "$200 per month"]
    ):
        raise ValueError("failed to confirm Claude Max help article")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 7:
        raise ValueError("Claude Code source_urls must include pricing and help docs")

    pricing_text = _http_get(source_urls[0])
    max_text = _http_get(source_urls[1])
    team_text = _http_get(source_urls[2])
    enterprise_text = _http_get(source_urls[3])
    overview_text = _http_get(source_urls[4])
    usage_text = _http_get(source_urls[5])
    max_help_text = _http_get(source_urls[6])
    _validate_sources(
        pricing_text,
        max_text,
        team_text,
        enterprise_text,
        overview_text,
        usage_text,
        max_help_text,
    )

    packages: List[Dict[str, object]] = []
    for package_name in _PACKAGE_ORDER:
        data = _PACKAGE_DATA[package_name]
        packages.append(
            {
                "name": package_name,
                "price": data["price"],
                "discount": "",
                "quota": data["quota"],
                "models_raw": _MODELS,
                "tools": _TOOLS,
                "access_method": "账号订阅（Claude Web / Desktop / IDE / CLI）",
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
