"""Catalog configuration (mainline).

Keep this file as pure data/config. Vendor-specific parsing belongs in
catalog/sources/* modules.
"""

from __future__ import annotations


VENDORS = [
    {
        "vendor_id": "tencent-cloud-coding-plan",
        "company_name": "腾讯",
        "plan_name": "腾讯云大模型 Coding Plan",
        "official_url": "https://cloud.tencent.com/act/pro/codingplan",
        "source_urls": [
            "https://cloud.tencent.com/document/product/1823/130092",
        ],
        "source_module": "catalog.sources.tencent_cloud_coding_plan",
    },
    {
        "vendor_id": "volcengine-coding-plan",
        "company_name": "字节跳动",
        "plan_name": "火山方舟 Coding Plan",
        "official_url": "https://www.volcengine.com/activity/codingplan",
        "source_urls": [
            "https://www.volcengine.com/docs/82379/1925114?lang=zh",
        ],
        "source_module": "catalog.sources.volcengine_coding_plan",
    },
    {
        "vendor_id": "baidu-qianfan-coding-plan",
        "company_name": "百度",
        "plan_name": "百度千帆 Coding Plan",
        "official_url": "https://cloud.baidu.com/product/codingplan.html",
        "source_urls": [
            "https://cloud.baidu.com/doc/qianfan/s/imlg0beiu",
        ],
        "source_module": "catalog.sources.baidu_qianfan_coding_plan",
    },
    {
        "vendor_id": "glm-coding-plan",
        "company_name": "智谱AI",
        "plan_name": "GLM Coding Plan",
        "official_url": "https://bigmodel.cn/glm-coding",
        "source_urls": [
            "https://docs.bigmodel.cn/cn/coding-plan/overview",
            "https://docs.bigmodel.cn/cn/coding-plan/faq",
            "https://docs.bigmodel.cn/cn/coding-plan/quick-start",
        ],
        "source_module": "catalog.sources.glm_coding_plan",
    },
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
        "source_module": "catalog.sources.minimax_token_plan",
    },
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
        "source_module": "catalog.sources.aliyun_bailian_coding_plan",
    },
    {
        "vendor_id": "xiaomi-mimo-token-plan",
        "company_name": "小米",
        "plan_name": "Xiaomi MiMo Token Plan",
        "official_url": "https://platform.xiaomimimo.com/docs/pricing.md",
        "source_urls": [
            "https://platform.xiaomimimo.com/#/token-plan",
            "https://platform.xiaomimimo.com/llms.txt",
            "https://platform.xiaomimimo.com/docs/api/chat/openai-api.md",
            "https://platform.xiaomimimo.com/docs/faq.md",
        ],
        "source_module": "catalog.sources.xiaomi_mimo_token_plan",
    },
    {
        "vendor_id": "trae-intl",
        "company_name": "字节跳动",
        "plan_name": "TRAE国际版",
        "official_url": "https://trae.ai/pricing",
        "source_urls": [
            "https://docs.trae.ai/ide/billing",
            "https://trae.ai/terms-of-service",
        ],
        "source_module": "catalog.sources.trae_intl",
    },
    {
        "vendor_id": "openai-chatgpt",
        "company_name": "OpenAI",
        "plan_name": "ChatGPT",
        "official_url": "https://chatgpt.com/",
        "source_urls": [
            "https://chatgpt.com/zh-Hans-CN/pricing/",
            "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus",
            "https://help.openai.com/en/articles/9793128-what-is-chatgpt-pro",
            "https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq",
        ],
        "source_module": "catalog.sources.openai_chatgpt",
    },
    {
        "vendor_id": "cursor",
        "company_name": "Anysphere",
        "plan_name": "Cursor",
        "official_url": "https://cursor.com/pricing",
        "source_urls": [
            "https://cursor.com/docs/models-and-pricing",
            "https://cursor.com/docs/account/teams/dashboard",
            "https://cursor.com/docs/cloud-agent",
        ],
        "source_module": "catalog.sources.cursor",
    },
    {
        "vendor_id": "kimi-ai",
        "company_name": "月之暗面",
        "plan_name": "Kimi AI",
        "official_url": "https://www.kimi.com/membership/pricing",
        "source_urls": [
            "https://www.kimi.com/membership/pricing",
            "https://www.kimi.com/robots.txt",
            "https://statics.moonshot.cn/kimi-web-seo/assets/Pricing-1vnxNQVp.js",
            "https://www.kimi.com/apiv2/kimi.gateway.order.v1.GoodsService/ListGoods",
        ],
        "source_module": "catalog.sources.kimi_ai",
    },
]
