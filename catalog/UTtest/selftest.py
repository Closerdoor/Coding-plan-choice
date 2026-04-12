"""Self-tests for catalog generation (no network).

Run:
  python -m catalog.selftest
"""

from __future__ import annotations

import re
import unittest

from catalog import update


def _normalize_timestamp(md: str) -> str:
    normalized = re.sub(
        r"最后更新时间（UTC）：[0-9T:+-]+",
        "最后更新时间（UTC）：<normalized>",
        md,
    )
    return re.sub(
        r"最新生成时间（UTC）：[0-9T:+-]+",
        "最新生成时间（UTC）：<normalized>",
        normalized,
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

        rendered = _normalize_timestamp(
            update._render_catalog_md(vendors, [], "2026-04-11T00:00:00+00:00")
        )

        self.assertIn("# Coding Plan 套餐汇总", rendered)
        self.assertIn("## 更新状态", rendered)
        self.assertIn("- 本次更新状态：无 warnings", rendered)
        self.assertIn("## 导航", rendered)
        self.assertIn("## 总览", rendered)
        self.assertIn("## 聚合套餐", rendered)
        self.assertIn("### 腾讯云大模型 Coding Plan", rendered)
        self.assertIn("- 厂商：腾讯云", rendered)
        self.assertIn(
            "- 官方地址：https://cloud.tencent.com/act/pro/codingplan", rendered
        )
        self.assertIn("- 最后更新时间（UTC）：<normalized>", rendered)
        self.assertIn("| 项目 | lite套餐 | pro套餐 |", rendered)

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

        rendered = _normalize_timestamp(
            update._render_catalog_md(vendors, [], "2026-04-12T00:00:00+00:00")
        )

        self.assertIn("## 垂直厂商套餐", rendered)
        self.assertIn("### MiniMax Token Plan", rendered)
        self.assertIn("- 厂商：MiniMax", rendered)
        self.assertIn(
            "| 项目 | starter套餐 | plus套餐 | max套餐 | plus-极速版 | max-极速版 | ultra-极速版 |",
            rendered,
        )
        self.assertIn(
            "| 价格 | ¥29/月 | ¥49/月 | ¥119/月 | ¥98/月 | ¥199/月 | ¥899/月 |",
            rendered,
        )

    def test_render_matches_catalog_template_for_aliyun(self) -> None:
        vendors = [
            {
                "vendor_id": "aliyun-bailian-coding-plan",
                "company_name": "阿里",
                "plan_name": "阿里云百炼Coding plan",
                "official_url": "https://help.aliyun.com/zh/model-studio/coding-plan",
                "source_urls": [
                    "https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio",
                    "https://help.aliyun.com/zh/model-studio/use-chat-client-or-development-tool/",
                    "https://help.aliyun.com/zh/model-studio/models",
                ],
                "updated_at_utc": "2026-04-12T00:00:00+00:00",
                "packages": [
                    {
                        "name": "pro套餐",
                        "price": "¥200/月",
                        "discount": "",
                        "quota": "6000次请求/5小时；45000次请求/周；90000次请求/月",
                        "models_raw": [
                            "Qwen3.6-Plus",
                            "Kimi-K2.5",
                            "GLM-5",
                            "MiniMax-M2.5",
                            "Qwen3.5-Plus",
                            "Qwen3-Max-2026-01-23",
                            "Qwen3-Coder-Next",
                            "Qwen3-Coder-Plus",
                            "GLM-4.7",
                        ],
                        "models_filtered": [],
                        "tools": [
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
                        ],
                        "access_method": "API Key + Base URL（OpenAI / Anthropic 协议）",
                    }
                ],
            }
        ]

        rendered = _normalize_timestamp(
            update._render_catalog_md(vendors, [], "2026-04-12T00:00:00+00:00")
        )

        self.assertIn("### 阿里云百炼Coding plan", rendered)
        self.assertIn("- 厂商：阿里", rendered)
        self.assertIn("| 项目 | pro套餐 |", rendered)
        self.assertIn("| 价格 | ¥200/月 |", rendered)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
