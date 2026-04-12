"""Aliyun Bailian Coding Plan source."""

from __future__ import annotations

import html
import re
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List


_MODEL_ORDER = [
    ("Qwen3.6-Plus", "qwen3.6-plus"),
    ("Kimi-K2.5", "kimi-k2.5"),
    ("GLM-5", "glm-5"),
    ("MiniMax-M2.5", "minimax-m2.5"),
    ("Qwen3.5-Plus", "qwen3.5-plus"),
    ("Qwen3-Max-2026-01-23", "qwen3-max-2026-01-23"),
    ("Qwen3-Coder-Next", "qwen3-coder-next"),
    ("Qwen3-Coder-Plus", "qwen3-coder-plus"),
    ("GLM-4.7", "glm-4.7"),
]

_TOOL_ORDER = [
    "OpenClaw",
    "OpenCode",
    "Claude Code",
    "Cline",
    "Cursor",
    "Qwen Code",
    "Qoder",
    "Lingma",
    "Kilo Code",
    "Kilo CLI",
    "Codex",
]


class _HTMLTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag in {"script", "style"}:
            self._skip_depth += 1

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag in {"script", "style"} and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._skip_depth == 0 and data.strip():
            self.parts.append(data.strip())


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _html_to_text(raw_html: str) -> str:
    parser = _HTMLTextParser()
    parser.feed(raw_html)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def _compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def _extract_pro_section(text: str) -> str:
    compact = _compact(text)
    start = compact.find("Pro高级套餐")
    end = compact.find("快速开始", start)
    if start == -1 or end == -1 or end <= start:
        raise ValueError("failed to locate Aliyun Coding Plan pro section")
    return compact[start:end]


def _extract_price(section: str) -> str:
    match = re.search(r"价格¥?([0-9,]+)\/月", section)
    if not match:
        raise ValueError("failed to extract Aliyun Coding Plan price")
    return f"¥{match.group(1).replace(',', '')}/月"


def _extract_quota(section: str) -> str:
    match = re.search(
        r"每5小时([0-9,]+)次请求.*?每周([0-9,]+)次请求.*?每月([0-9,]+)次请求",
        section,
    )
    if not match:
        raise ValueError("failed to extract Aliyun Coding Plan quota")
    return (
        f"{match.group(1).replace(',', '')}次请求/5小时；"
        f"{match.group(2).replace(',', '')}次请求/周；"
        f"{match.group(3).replace(',', '')}次请求/月"
    )


def _extract_models(section: str) -> List[str]:
    start = section.find("支持的模型")
    end = section.find("价格", start)
    if start == -1 or end == -1 or end <= start:
        raise ValueError("failed to locate Aliyun Coding Plan model section")
    model_section = section[start:end].lower()
    models = [label for label, token in _MODEL_ORDER if token in model_section]
    if not models:
        raise ValueError("failed to extract Aliyun Coding Plan models")
    return models


def _extract_tools(text: str) -> List[str]:
    compact = _compact(text)
    start = compact.find("步骤三：接入AI工具")
    end = compact.find("订阅前须知", start)
    if start == -1 or end == -1 or end <= start:
        raise ValueError("failed to locate Aliyun Coding Plan tool section")
    tool_section = compact[start:end]
    tools = [tool for tool in _TOOL_ORDER if tool.replace(" ", "") in tool_section]
    if not tools:
        raise ValueError("failed to extract Aliyun Coding Plan tools")
    return tools


def _validate_access_method(*texts: str) -> None:
    merged = "\n".join(texts)
    required_fragments = [
        "Coding Plan 专属 API Key",
        "OpenAI 兼容协议",
        "Anthropic 兼容协议",
        "coding.dashscope.aliyuncs.com/v1",
        "coding.dashscope.aliyuncs.com/apps/anthropic",
    ]
    if any(fragment not in merged for fragment in required_fragments):
        raise ValueError("failed to confirm Aliyun Coding Plan access method")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    official_url = config["official_url"]
    source_urls = config["source_urls"]
    if len(source_urls) < 3:
        raise ValueError(
            "Aliyun source_urls must include overview, development tools, and models pages"
        )

    coding_plan_text = _html_to_text(_http_get(official_url))
    overview_text = _html_to_text(_http_get(source_urls[0]))
    tools_text = _html_to_text(_http_get(source_urls[1]))
    models_text = _html_to_text(_http_get(source_urls[2]))

    section = _extract_pro_section(coding_plan_text)
    _validate_access_method(coding_plan_text)

    models = _extract_models(section)
    # Guard against marketing-only names that no longer exist in the public model list.
    if not all(
        model.lower() in models_text.lower()
        or model.startswith("Kimi")
        or model.startswith("GLM")
        or model.startswith("MiniMax")
        for model in models
    ):
        raise ValueError(
            "failed to validate Aliyun Coding Plan models against model list"
        )

    packages = [
        {
            "name": "pro套餐",
            "price": _extract_price(section),
            "discount": "",
            "quota": _extract_quota(section),
            "models_raw": models,
            "tools": _extract_tools(coding_plan_text),
            "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
        }
    ]

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "plan_name": config["plan_name"],
        "official_url": official_url,
        "source_urls": source_urls,
        "packages": packages,
    }
