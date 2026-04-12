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
                "official_sources": [
                    "https://cloud.tencent.com/act/pro/codingplan",
                    "https://cloud.tencent.com/document/product/1823/130092",
                ],
                "updated_at_utc": "2026-04-11T00:00:00+00:00",
                "packages": [
                    {
                        "name": "lite套餐",
                        "price": "¥40/月",
                        "discount": "首月¥7.9/月",
                        "quota": "1200次请求/5小时；9000次请求/周；18000次请求/月",
                        "models_raw": [
                            "Auto",
                            "Tencent HY 2.0 Instruct",
                            "Tencent HY 2.0 Think",
                            "GLM-5",
                            "Kimi-K2.5",
                            "MiniMax-M2.5",
                            "Hunyuan-T1",
                            "Hunyuan-TurboS",
                        ],
                        "models_filtered": [],
                        "tools": [
                            "OpenClaw",
                            "CodeBuddy Code",
                            "Claude Code",
                            "OpenCode",
                            "Cline",
                            "Cursor",
                            "Codex",
                            "Kilo CLI",
                            "Kilo Code",
                        ],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "pro套餐",
                        "price": "¥200/月",
                        "discount": "首月¥39.9/月",
                        "quota": "6000次请求/5小时；45000次请求/周；90000次请求/月",
                        "models_raw": [
                            "Auto",
                            "Tencent HY 2.0 Instruct",
                            "Tencent HY 2.0 Think",
                            "GLM-5",
                            "Kimi-K2.5",
                            "MiniMax-M2.5",
                            "Hunyuan-T1",
                            "Hunyuan-TurboS",
                        ],
                        "models_filtered": [],
                        "tools": [
                            "OpenClaw",
                            "CodeBuddy Code",
                            "Claude Code",
                            "OpenCode",
                            "Cline",
                            "Cursor",
                            "Codex",
                            "Kilo CLI",
                            "Kilo Code",
                        ],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                ],
            }
        ]

        expected = (
            "# AI 模型与 Coding Plan 套餐汇总\n"
            "\n"
            "说明：\n"
            "- 本文档用于集中展示各厂商的模型/套餐信息。\n"
            "- 所有价格与用量信息以官方页面为准，并在条目中标注信息源链接。\n"
            "- 币种按厂商原始币种展示（CN=CNY，US=USD）。\n"
            "- 最后更新时间使用 UTC（由自动更新流程填写）。\n"
            "\n"
            "---\n"
            "\n"
            "## 腾讯云｜腾讯云大模型 Coding Plan\n"
            "\n"
            "- 官方地址：https://cloud.tencent.com/act/pro/codingplan\n"
            "- 说明文档：https://cloud.tencent.com/document/product/1823/130092\n"
            "- 最后更新时间（UTC）：<normalized>\n"
            "\n"
            "| 项目 | lite套餐 | pro套餐 |\n"
            "| --- | --- | --- |\n"
            "| 价格 | ¥40/月(优惠：首月¥7.9/月) | ¥200/月(优惠：首月¥39.9/月) |\n"
            "| 用量 | 1200次请求/5小时；9000次请求/周；18000次请求/月 | 6000次请求/5小时；45000次请求/周；90000次请求/月 |\n"
            "| 支持模型 | Auto；Tencent HY 2.0 Instruct；Tencent HY 2.0 Think；GLM-5；Kimi-K2.5；MiniMax-M2.5；Hunyuan-T1；Hunyuan-TurboS | Auto；Tencent HY 2.0 Instruct；Tencent HY 2.0 Think；GLM-5；Kimi-K2.5；MiniMax-M2.5；Hunyuan-T1；Hunyuan-TurboS |\n"
            "| 支持工具 | OpenClaw；CodeBuddy Code；Claude Code；OpenCode；Cline；Cursor；Codex；Kilo CLI；Kilo Code | OpenClaw；CodeBuddy Code；Claude Code；OpenCode；Cline；Cursor；Codex；Kilo CLI；Kilo Code |\n"
            "| 使用方式 | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） |\n"
        )

        self.assertEqual(
            _normalize_timestamp(update._render_catalog_md(vendors)), expected
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
