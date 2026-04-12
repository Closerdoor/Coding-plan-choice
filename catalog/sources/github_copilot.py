"""GitHub Copilot pricing source.

GitHub exposes stable plans and request allowance docs, so this source uses
curated plan facts validated against those official pages.
"""

from __future__ import annotations

from typing import Dict


_PACKAGE_ORDER = [
    "Free套餐",
    "Pro套餐",
    "Pro+套餐",
]

_PACKAGE_DATA = {
    "Free套餐": {
        "price": "$0/月",
        "discount": "",
        "quota": "50 premium requests/月；2000 completions/月",
        "models_raw": [
            "Claude Haiku 4.5",
            "GPT-5 mini",
            "Claude Sonnet 4.6",
            "Gemini 2.5 Pro",
        ],
        "tools": [
            "GitHub",
            "VS Code",
            "Visual Studio",
            "JetBrains IDEs",
            "CLI",
            "GitHub Mobile",
            "Windows Terminal",
        ],
        "access_method": "账号订阅（GitHub / IDE / CLI）",
    },
    "Pro套餐": {
        "price": "$10/月",
        "discount": "",
        "quota": "300 premium requests/月；含 GPT-5 mini / GPT-4.1 / GPT-4o 无限聊天与补全",
        "models_raw": [
            "GPT-5 mini",
            "GPT-4.1",
            "GPT-4o",
            "Claude Sonnet 4.6",
            "Claude Opus 4.6",
            "Gemini 2.5 Pro",
            "GPT-5.4",
        ],
        "tools": [
            "GitHub",
            "VS Code",
            "Visual Studio",
            "JetBrains IDEs",
            "CLI",
            "GitHub Mobile",
            "Windows Terminal",
            "Copilot cloud agent",
            "Copilot code review",
        ],
        "access_method": "账号订阅（GitHub / IDE / CLI）",
    },
    "Pro+套餐": {
        "price": "$39/月",
        "discount": "",
        "quota": "1500 premium requests/月；含全部模型访问与 included models 无限聊天与补全",
        "models_raw": [
            "GPT-5 mini",
            "GPT-4.1",
            "GPT-4o",
            "Claude Sonnet 4.6",
            "Claude Opus 4.6",
            "Gemini 2.5 Pro",
            "GPT-5.4",
        ],
        "tools": [
            "GitHub",
            "VS Code",
            "Visual Studio",
            "JetBrains IDEs",
            "CLI",
            "GitHub Mobile",
            "Windows Terminal",
            "Copilot cloud agent",
            "Copilot code review",
            "GitHub Spark",
        ],
        "access_method": "账号订阅（GitHub / IDE / CLI）",
    },
}


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 4:
        raise ValueError(
            "GitHub Copilot source_urls must include plans page and supporting docs"
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
