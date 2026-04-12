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
                "plan_name": "腾讯云大模型 Coding Plan",
                "official_url": "https://cloud.tencent.com/act/pro/codingplan",
                "source_urls": [
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
            "## 腾讯云|腾讯云大模型 Coding Plan\n"
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

    def test_render_matches_catalog_template_for_minimax(self) -> None:
        vendors = [
            {
                "vendor_id": "minimax-token-plan",
                "company_name": "MiniMax",
                "plan_name": "MiniMax Token Plan",
                "official_url": "https://platform.minimaxi.com/subscribe/token-plan",
                "source_urls": [
                    "https://platform.minimaxi.com/docs/token-plan/intro",
                    "https://platform.minimaxi.com/docs/guides/pricing-token-plan",
                    "https://platform.minimaxi.com/docs/guides/text-ai-coding-tools",
                ],
                "updated_at_utc": "2026-04-12T00:00:00+00:00",
                "packages": [
                    {
                        "name": "starter套餐",
                        "price": "¥29/月",
                        "discount": "",
                        "quota": "M2.7：600次请求/5小时；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": ["M2.7", "Music-2.6"],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "plus套餐",
                        "price": "¥49/月",
                        "discount": "",
                        "quota": "M2.7：1,500次请求/5小时；Speech 2.8：4,000字符/日；image-01：50张/日；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": ["M2.7", "Speech 2.8", "image-01", "Music-2.6"],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "max套餐",
                        "price": "¥119/月",
                        "discount": "",
                        "quota": "M2.7：4,500次请求/5小时；Speech 2.8：11,000字符/日；image-01：120张/日；Hailuo-2.3-Fast 768P 6s：2个/日；Hailuo-2.3 768P 6s：2个/日；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": [
                            "M2.7",
                            "Speech 2.8",
                            "image-01",
                            "Hailuo-2.3-Fast 768P 6s",
                            "Hailuo-2.3 768P 6s",
                            "Music-2.6",
                        ],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "plus-极速版",
                        "price": "¥98/月",
                        "discount": "",
                        "quota": "M2.7-highspeed：1,500次请求/5小时；Speech 2.8：9,000字符/日；image-01：100张/日；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": [
                            "M2.7-highspeed",
                            "Speech 2.8",
                            "image-01",
                            "Music-2.6",
                        ],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "max-极速版",
                        "price": "¥199/月",
                        "discount": "",
                        "quota": "M2.7-highspeed：4,500次请求/5小时；Speech 2.8：19,000字符/日；image-01：200张/日；Hailuo-2.3-Fast 768P 6s：3个/日；Hailuo-2.3 768P 6s：3个/日；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": [
                            "M2.7-highspeed",
                            "Speech 2.8",
                            "image-01",
                            "Hailuo-2.3-Fast 768P 6s",
                            "Hailuo-2.3 768P 6s",
                            "Music-2.6",
                        ],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    },
                    {
                        "name": "ultra-极速版",
                        "price": "¥899/月",
                        "discount": "",
                        "quota": "M2.7-highspeed：30,000次请求/5小时；Speech 2.8：50,000字符/日；image-01：800张/日；Hailuo-2.3-Fast 768P 6s：5个/日；Hailuo-2.3 768P 6s：5个/日；Music-2.6：100首/天（限免）（每首<=5分钟）",
                        "models_raw": [
                            "M2.7-highspeed",
                            "Speech 2.8",
                            "image-01",
                            "Hailuo-2.3-Fast 768P 6s",
                            "Hailuo-2.3 768P 6s",
                            "Music-2.6",
                        ],
                        "models_filtered": [],
                        "tools": ["Claude Code", "Cursor", "TRAE", "OpenCode"],
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
            "## MiniMax|MiniMax Token Plan\n"
            "\n"
            "- 官方地址：https://platform.minimaxi.com/subscribe/token-plan\n"
            "- 说明文档：https://platform.minimaxi.com/docs/token-plan/intro\n"
            "- 补充来源：https://platform.minimaxi.com/docs/guides/pricing-token-plan\n"
            "- 补充来源：https://platform.minimaxi.com/docs/guides/text-ai-coding-tools\n"
            "- 最后更新时间（UTC）：<normalized>\n"
            "\n"
            "| 项目 | starter套餐 | plus套餐 | max套餐 | plus-极速版 | max-极速版 | ultra-极速版 |\n"
            "| --- | --- | --- | --- | --- | --- | --- |\n"
            "| 价格 | ¥29/月 | ¥49/月 | ¥119/月 | ¥98/月 | ¥199/月 | ¥899/月 |\n"
            "| 用量 | M2.7：600次请求/5小时；Music-2.6：100首/天（限免）（每首<=5分钟） | M2.7：1,500次请求/5小时；Speech 2.8：4,000字符/日；image-01：50张/日；Music-2.6：100首/天（限免）（每首<=5分钟） | M2.7：4,500次请求/5小时；Speech 2.8：11,000字符/日；image-01：120张/日；Hailuo-2.3-Fast 768P 6s：2个/日；Hailuo-2.3 768P 6s：2个/日；Music-2.6：100首/天（限免）（每首<=5分钟） | M2.7-highspeed：1,500次请求/5小时；Speech 2.8：9,000字符/日；image-01：100张/日；Music-2.6：100首/天（限免）（每首<=5分钟） | M2.7-highspeed：4,500次请求/5小时；Speech 2.8：19,000字符/日；image-01：200张/日；Hailuo-2.3-Fast 768P 6s：3个/日；Hailuo-2.3 768P 6s：3个/日；Music-2.6：100首/天（限免）（每首<=5分钟） | M2.7-highspeed：30,000次请求/5小时；Speech 2.8：50,000字符/日；image-01：800张/日；Hailuo-2.3-Fast 768P 6s：5个/日；Hailuo-2.3 768P 6s：5个/日；Music-2.6：100首/天（限免）（每首<=5分钟） |\n"
            "| 支持模型 | M2.7；Music-2.6 | M2.7；Speech 2.8；image-01；Music-2.6 | M2.7；Speech 2.8；image-01；Hailuo-2.3-Fast 768P 6s；Hailuo-2.3 768P 6s；Music-2.6 | M2.7-highspeed；Speech 2.8；image-01；Music-2.6 | M2.7-highspeed；Speech 2.8；image-01；Hailuo-2.3-Fast 768P 6s；Hailuo-2.3 768P 6s；Music-2.6 | M2.7-highspeed；Speech 2.8；image-01；Hailuo-2.3-Fast 768P 6s；Hailuo-2.3 768P 6s；Music-2.6 |\n"
            "| 支持工具 | Claude Code；Cursor；TRAE；OpenCode | Claude Code；Cursor；TRAE；OpenCode | Claude Code；Cursor；TRAE；OpenCode | Claude Code；Cursor；TRAE；OpenCode | Claude Code；Cursor；TRAE；OpenCode | Claude Code；Cursor；TRAE；OpenCode |\n"
            "| 使用方式 | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） | API Key + Base URL（OpenAI / Anthropic 协议） |\n"
        )

        self.assertEqual(
            _normalize_timestamp(update._render_catalog_md(vendors)), expected
        )


if __name__ == "__main__":
    raise SystemExit(unittest.main())
