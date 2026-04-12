"""ChatGPT subscription pricing source.

OpenAI Help Center pages are protected by Cloudflare in this environment, so this
source uses curated values confirmed from the configured official help articles.
"""

from __future__ import annotations

from typing import Dict


_PACKAGE_ORDER = [
    "Free套餐",
    "Go套餐",
    "Plus套餐",
    "Pro $100套餐",
    "Pro $200套餐",
]

_PACKAGE_DATA = {
    "Free套餐": {
        "price": "$0/月",
        "discount": "",
        "quota": "GPT-5.2 五小时窗口内限量使用；工具使用有单独限额",
        "models_raw": ["GPT-5.2"],
        "tools": [
            "Web Search",
            "File Uploads",
            "Image Generation",
            "GPTs",
        ],
        "access_method": "账号订阅（ChatGPT Web / App）",
    },
    "Go套餐": {
        "price": "价格以官方 pricing 页为准",
        "discount": "",
        "quota": "比 Free 更高的使用上限；包含 GPT-5.3 Instant 无限聊天访问（受滥用防护限制）",
        "models_raw": ["GPT-5.3 Instant", "Thinking"],
        "tools": [
            "Image Generation",
            "File Uploads",
            "Advanced Data Analysis",
            "Projects",
            "Tasks",
            "Custom GPTs",
            "Memory",
        ],
        "access_method": "账号订阅（ChatGPT Web / App）",
    },
    "Plus套餐": {
        "price": "$20/月",
        "discount": "",
        "quota": "更高 GPT-5.3 使用上限；高级功能按套餐内 included usage 提供",
        "models_raw": ["GPT-5.3", "Advanced reasoning models"],
        "tools": [
            "Voice",
            "Image Generation",
            "File Uploads",
            "Deep Research",
            "Custom GPTs",
            "Codex",
            "Sora",
        ],
        "access_method": "账号订阅（ChatGPT Web / App）",
    },
    "Pro $100套餐": {
        "price": "$100/月",
        "discount": "",
        "quota": "比 Plus 高 5x 使用上限；Codex 限额限时为 Plus 的 10x",
        "models_raw": ["GPT-5", "Pro models"],
        "tools": [
            "Codex",
            "Deep Research",
            "Image Creation",
            "Memory",
            "File Uploads",
        ],
        "access_method": "账号订阅（ChatGPT Web / App）",
    },
    "Pro $200套餐": {
        "price": "$200/月",
        "discount": "",
        "quota": "比 Plus 高 20x 使用上限；GPT-5 与 legacy models 为 unlimited access（受使用政策与防护限制）",
        "models_raw": ["GPT-5", "Legacy models", "Pro models"],
        "tools": [
            "Codex",
            "Deep Research",
            "Image Creation",
            "Memory",
            "File Uploads",
        ],
        "access_method": "账号订阅（ChatGPT Web / App）",
    },
}


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 5:
        raise ValueError(
            "ChatGPT source_urls must include plus/free/go/pro/credits articles"
        )

    packages = []
    for package_name in _PACKAGE_ORDER:
        data = _PACKAGE_DATA[package_name]
        packages.append(
            {
                "name": package_name,
                "price": data["price"],
                "discount": data["discount"],
                "quota": data["quota"],
                "models_raw": data["models_raw"],
                "tools": data["tools"],
                "access_method": data["access_method"],
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
