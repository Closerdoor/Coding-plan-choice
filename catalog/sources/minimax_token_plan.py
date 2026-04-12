"""MiniMax Token Plan source."""

from __future__ import annotations

import html
import re
import urllib.request
from html.parser import HTMLParser
from typing import Dict, List, Tuple


_STANDARD_PACKAGE_NAMES = {
    "Starter": "starter套餐",
    "Plus": "plus套餐",
    "Max": "max套餐",
}

_HIGHSPEED_PACKAGE_NAMES = {
    "Plus-极速版": "plus-极速版",
    "Max-极速版": "max-极速版",
    "Ultra-极速版": "ultra-极速版",
}

_TOOL_ORDER = [
    "Claude Code",
    "Cursor",
    "TRAE",
    "OpenCode",
    "Kilo Code",
    "OpenClaw",
    "Hermes Agent",
    "Cline",
    "Roo Code",
    "Grok CLI",
    "Codex CLI",
    "Droid",
    "Zed",
    "MonkeyCode",
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


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._in_table = False
        self._in_row = False
        self._in_cell = False
        self._cell_parts: List[str] = []
        self._current_row: List[str] = []
        self._current_table: List[List[str]] = []
        self.tables: List[List[List[str]]] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag in {"script", "style"}:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return
        if tag == "table":
            self._in_table = True
            self._current_table = []
        elif self._in_table and tag == "tr":
            self._in_row = True
            self._current_row = []
        elif self._in_row and tag in {"th", "td"}:
            self._in_cell = True
            self._cell_parts = []

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag in {"script", "style"} and self._skip_depth > 0:
            self._skip_depth -= 1
            return
        if self._skip_depth > 0:
            return
        if self._in_cell and tag in {"th", "td"}:
            cell_text = re.sub(
                r"\s+", " ", html.unescape(" ".join(self._cell_parts))
            ).strip()
            self._current_row.append(cell_text)
            self._in_cell = False
            self._cell_parts = []
        elif self._in_row and tag == "tr":
            if any(cell.strip() for cell in self._current_row):
                self._current_table.append(self._current_row)
            self._in_row = False
            self._current_row = []
        elif self._in_table and tag == "table":
            if self._current_table:
                self.tables.append(self._current_table)
            self._in_table = False
            self._current_table = []

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self._skip_depth == 0 and self._in_cell and data:
            self._cell_parts.append(data)


def _http_get(url: str, *, timeout_s: int = 60) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout_s) as response:
        return response.read().decode("utf-8", "replace")


def _html_to_text(raw_html: str) -> str:
    parser = _HTMLTextParser()
    parser.feed(raw_html)
    return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()


def _extract_tables(raw_html: str) -> List[List[List[str]]]:
    parser = _TableParser()
    parser.feed(raw_html)
    return parser.tables


def _normalize_package_header(value: str) -> str:
    compact = re.sub(r"\s+", "", value)
    compact = compact.replace("`", "")
    if compact.startswith("Plus-极速版"):
        return "Plus-极速版"
    if compact.startswith("Max-极速版"):
        return "Max-极速版"
    if compact.startswith("Ultra-极速版"):
        return "Ultra-极速版"
    if compact.startswith("Starter"):
        return "Starter"
    if compact.startswith("Plus"):
        return "Plus"
    if compact.startswith("Max"):
        return "Max"
    raise ValueError(f"unknown MiniMax package header: {value}")


def _normalize_price(value: str) -> str:
    match = re.search(r"¥\s*([0-9]+)\s*/\s*月", value)
    if not match:
        raise ValueError(f"failed to parse MiniMax monthly price: {value}")
    return f"¥{match.group(1)}/月"


def _normalize_quota_value(value: str) -> str:
    compact = re.sub(r"\s+", "", value)
    compact = compact.replace("（每首≤5分钟）", "（每首<=5分钟）")
    return compact


def _is_unavailable_quota(value: str) -> bool:
    compact = _normalize_quota_value(value)
    return compact in {"--", "-", "—", "––"}


def _build_quota_and_models(features: List[Tuple[str, str]]) -> Tuple[str, List[str]]:
    quota_parts: List[str] = []
    models_raw: List[str] = []
    for model_name, quota_value in features:
        if _is_unavailable_quota(quota_value):
            continue
        quota_parts.append(f"{model_name}：{_normalize_quota_value(quota_value)}")
        models_raw.append(model_name)
    if not quota_parts or not models_raw:
        raise ValueError("failed to build MiniMax quota/models data")
    return "；".join(quota_parts), models_raw


def _extract_monthly_packages(pricing_html: str) -> Dict[str, Dict[str, object]]:
    tables = _extract_tables(pricing_html)
    if len(tables) < 2:
        raise ValueError("failed to extract MiniMax monthly pricing tables")

    packages: Dict[str, Dict[str, object]] = {}
    for table, package_names in [
        (tables[0], _STANDARD_PACKAGE_NAMES),
        (tables[1], _HIGHSPEED_PACKAGE_NAMES),
    ]:
        header = table[0]
        if len(header) < 4:
            raise ValueError("invalid MiniMax pricing table header")

        normalized_headers = [
            package_names[_normalize_package_header(cell)] for cell in header[1:4]
        ]
        features_by_package: Dict[str, List[Tuple[str, str]]] = {
            package_name: [] for package_name in normalized_headers
        }
        prices: Dict[str, str] = {}

        for row in table[1:]:
            if len(row) < 4:
                continue
            row_name = re.sub(r"\s+", " ", row[0]).strip()
            if not row_name:
                continue
            if row_name == "价格":
                for index, package_name in enumerate(normalized_headers, start=1):
                    prices[package_name] = _normalize_price(row[index])
                continue
            for index, package_name in enumerate(normalized_headers, start=1):
                features_by_package[package_name].append((row_name, row[index].strip()))

        for package_name in normalized_headers:
            quota, models_raw = _build_quota_and_models(
                features_by_package[package_name]
            )
            if package_name not in prices:
                raise ValueError(f"missing MiniMax price for {package_name}")
            packages[package_name] = {
                "price": prices[package_name],
                "quota": quota,
                "models_raw": models_raw,
            }

    expected_package_names = {
        "starter套餐",
        "plus套餐",
        "max套餐",
        "plus-极速版",
        "max-极速版",
        "ultra-极速版",
    }
    if set(packages) != expected_package_names:
        raise ValueError("failed to extract all MiniMax monthly packages")
    return packages


def _extract_tools(tools_doc_html: str) -> List[str]:
    text = _html_to_text(tools_doc_html)
    tools = [tool for tool in _TOOL_ORDER if tool in text]
    if not tools:
        raise ValueError("failed to extract MiniMax supported tools")
    return tools


def _validate_access_method(*texts: str) -> None:
    merged = "\n".join(texts)
    required_fragments = ["Token Plan API Key", "OpenAI", "Anthropic"]
    if any(fragment not in merged for fragment in required_fragments):
        raise ValueError("failed to confirm MiniMax access method")
    if all(fragment not in merged for fragment in ["Base URL", "baseURL", "BASE_URL"]):
        raise ValueError("failed to confirm MiniMax base URL requirement")


def fetch(config: Dict[str, object]) -> Dict[str, object]:
    source_urls = config["source_urls"]
    if len(source_urls) < 4:
        raise ValueError(
            "MiniMax source_urls must include activity, intro, pricing, and coding tools pages"
        )

    activity_html = _http_get(source_urls[0])
    intro_html = _http_get(source_urls[1])
    pricing_html = _http_get(source_urls[2])
    tools_doc_html = _http_get(source_urls[3])

    if "token-plan" not in activity_html:
        raise ValueError("failed to confirm MiniMax activity page")

    intro_text = _html_to_text(intro_html)
    tools_text = _html_to_text(tools_doc_html)
    _validate_access_method(intro_text, tools_text)
    packages_data = _extract_monthly_packages(pricing_html)
    tools = _extract_tools(tools_doc_html)

    package_order = [
        "starter套餐",
        "plus套餐",
        "max套餐",
        "plus-极速版",
        "max-极速版",
        "ultra-极速版",
    ]
    packages = []
    for package_name in package_order:
        package_data = packages_data[package_name]
        packages.append(
            {
                "name": package_name,
                "price": package_data["price"],
                "discount": "",
                "quota": package_data["quota"],
                "models_raw": package_data["models_raw"],
                "tools": tools,
                "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
            }
        )

    return {
        "vendor_id": config["vendor_id"],
        "company_name": config["company_name"],
        "vendor_name": config["vendor_name"],
        "official_sources": source_urls,
        "packages": packages,
    }
