"""Self-tests for catalog generation (no network).

Run:
  python -m catalog.selftest
"""

from __future__ import annotations

import re
import unittest

from catalog import update


def _normalize_timestamp(md: str) -> str:
    return re.sub(
        r"最后更新时间（UTC）：[0-9T:+-]+",
        "最后更新时间（UTC）：<normalized>",
        md,
    )


class TestCatalogRender(unittest.TestCase):
    def test_render_matches_catalog_template_for_tencent_cloud(self) -> None:
        vendors = [
            {
                "vendor_id": "tencent-cloud-coding-plan",
                "company_name": "腾讯云",
                "vendor_name": "腾讯云大模型 Coding Plan",
                "official_source": "https://cloud.tencent.com/act/pro/codingplan",
                "updated_at_utc": "2026-04-11T00:00:00+00:00",
                "packages": [
                    {
                        "name": "lite套餐",
                        "price": "¥40/月",
                        "quota": "1200次请求/5小时；9000次请求/周；18000次请求/月",
                        "models_raw": [
                            "Tencent HY 2.0 Instruct",
                            "GLM-5",
                            "Kimi-K2.5",
                            "MiniMax-M2.5",
                        ],
                        "models_filtered": ["GLM-5", "Kimi-K2.5", "MiniMax-M2.5"],
                        "tools": [
                            "OpenClaw",
                            "OpenCode",
                            "Claude Code",
                            "Codex",
                            "Cursor",
                        ],
                        "access_method": "API Key",
                    },
                    {
                        "name": "pro套餐",
                        "price": "¥200/月",
                        "quota": "6000次请求/5小时；45000次请求/周；90000次请求/月",
                        "models_raw": [
                            "Tencent HY 2.0 Instruct",
                            "GLM-5",
                            "Kimi-K2.5",
                            "MiniMax-M2.5",
                        ],
                        "models_filtered": ["GLM-5", "Kimi-K2.5", "MiniMax-M2.5"],
                        "tools": [
                            "OpenClaw",
                            "OpenCode",
                            "Claude Code",
                            "Codex",
                            "Cursor",
                        ],
                        "access_method": "API Key",
                    },
                ],
            }
        ]

        expected = """# AI 模型与 Coding Plan 套餐汇总

说明：
- 本文档用于集中展示各厂商的模型/套餐信息。
- 所有价格与用量信息以官方页面为准，并在条目中标注信息源链接。
- 币种按厂商原始币种展示（CN=CNY，US=USD）。
- 最后更新时间使用 UTC（由自动更新流程填写）。

---

## 腾讯云｜腾讯云大模型 Coding Plan

- 官方信息源：https://cloud.tencent.com/act/pro/codingplan
- 最后更新时间（UTC）：<normalized>

| 项目 | lite套餐 | pro套餐 |
| --- | --- | --- |
| 价格 | ¥40/月 | ¥200/月 |
| 用量 | 1200次请求/5小时；9000次请求/周；18000次请求/月 | 6000次请求/5小时；45000次请求/周；90000次请求/月 |
| 支持模型 | GLM-5；Kimi-K2.5；MiniMax-M2.5 | GLM-5；Kimi-K2.5；MiniMax-M2.5 |
| 支持工具 | OpenClaw；OpenCode；Claude Code；Codex；Cursor | OpenClaw；OpenCode；Claude Code；Codex；Cursor |
| 使用方式 | API Key | API Key |
"""

        self.assertEqual(
            _normalize_timestamp(update._render_catalog_md(vendors)), expected
        )


class TestModelFiltering(unittest.TestCase):
    def test_filter_models_prefers_top3_matches(self) -> None:
        provider_top3 = {
            "Zhipu AI": {"glm5"},
            "Moonshot AI": {"kimik25"},
            "MiniMax": {"minimaxm25"},
        }

        filtered = update._filter_models(
            [
                "Tencent HY 2.0 Instruct",
                "GLM-5",
                "Kimi-K2.5",
                "MiniMax-M2.5",
            ],
            provider_top3,
        )

        self.assertEqual(filtered, ["GLM-5", "Kimi-K2.5", "MiniMax-M2.5"])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
