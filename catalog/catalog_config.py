"""Catalog configuration (mainline).

Keep this file as pure data/config. Vendor-specific parsing belongs in
catalog/sources/* modules.
"""

from __future__ import annotations


VENDORS = [
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
        "vendor_id": "github-copilot",
        "company_name": "Microsoft",
        "plan_name": "GitHub Copilot",
        "official_url": "https://github.com/features/copilot/plans",
        "source_urls": [
            "https://github.com/features/copilot/plans",
            "https://docs.github.com/en/copilot/about-github-copilot/plans-for-github-copilot",
            "https://docs.github.com/en/copilot/about-github-copilot/what-is-github-copilot",
            "https://docs.github.com/en/copilot/concepts/billing/copilot-requests",
        ],
        "source_module": "catalog.sources.github_copilot",
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
        "vendor_id": "xfyun-xingchen-coding-plan",
        "company_name": "科大讯飞",
        "plan_name": "讯飞星辰Coding Plan",
        "official_url": "https://maas.xfyun.cn/packageSubscription?from=packageSubscriptionOverlay",
        "source_urls": [
            "https://maas.xfyun.cn/packageSubscription?from=packageSubscriptionOverlay",
            "https://maas.xfyun.cn/js/index-68edb439.js",
        ],
        "source_module": "catalog.sources.xfyun_xingchen_coding_plan",
    },
    {
        "vendor_id": "infini-ai-coding-plan",
        "company_name": "无问芯穹",
        "plan_name": "无问芯穹Coding Plan",
        "official_url": "https://docs.infini-ai.com/gen-studio-coding-plan/",
        "source_urls": [
            "https://cloud.infini-ai.com/platform/ai",
            "https://docs.infini-ai.com/gen-studio-coding-plan/",
            "https://docs.infini-ai.com/gen-studio-coding-plan/supported-models.html",
            "https://docs.infini-ai.com/shared/gen-studio/coding-tools/cp-use-cursor.html",
            "https://docs.infini-ai.com/shared/gen-studio/coding-tools/cp-use-claude-code.html",
        ],
        "source_module": "catalog.sources.infini_ai_coding_plan",
    },
    {
        "vendor_id": "openai-chatgpt",
        "company_name": "OpenAI",
        "plan_name": "ChatGPT",
        "official_url": "https://help.openai.com/en/collections/3742473-chatgpt",
        "source_urls": [
            "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus",
            "https://help.openai.com/en/articles/9275245-chatgpt-free-tier-faq",
            "https://help.openai.com/en/articles/11989085-what-is-chatgpt-go",
            "https://help.openai.com/en/articles/9793128-about-chatgpt-pro-plans",
            "https://help.openai.com/en/articles/12642688-using-credits-for-flexible-usage-in-chatgpt-freegopluspro-sora",
        ],
        "source_module": "catalog.sources.openai_chatgpt",
    },
    {
        "vendor_id": "claude-code",
        "company_name": "Anthropic",
        "plan_name": "Claude Code",
        "official_url": "https://claude.com/pricing",
        "source_urls": [
            "https://claude.com/pricing",
            "https://claude.com/pricing/max",
            "https://claude.com/pricing/team",
            "https://claude.com/pricing/enterprise",
            "https://docs.anthropic.com/en/docs/claude-code/overview",
            "https://support.claude.com/en/articles/11145838-using-claude-code-with-your-pro-or-max-plan",
            "https://support.claude.com/en/articles/11049741-what-is-the-max-plan",
        ],
        "source_module": "catalog.sources.claude_code",
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
    {
        "vendor_id": "xiaomi-mimo-token-plan",
        "company_name": "小米",
        "plan_name": "Xiaomi MiMo Token Plan",
        "official_url": "https://platform.xiaomimimo.com/#/token-plan",
        "source_urls": [
            "https://platform.xiaomimimo.com/llms.txt",
            "https://platform.xiaomimimo.com/main.3b886aad.chunk.js",
            "https://platform.xiaomimimo.com/docs/pricing.md",
            "https://platform.xiaomimimo.com/docs/api/chat/openai-api.md",
            "https://platform.xiaomimimo.com/docs/faq.md",
        ],
        "source_module": "catalog.sources.xiaomi_mimo_token_plan",
    },
]


AUTO_UPDATE_VENDOR_IDS = [
    "cursor",
    "github-copilot",
    "trae-intl",
    "tencent-cloud-coding-plan",
    "volcengine-coding-plan",
    "aliyun-bailian-coding-plan",
    "baidu-qianfan-coding-plan",
    "infini-ai-coding-plan",
    "openai-chatgpt",
    "claude-code",
    "glm-coding-plan",
    "minimax-token-plan",
    "kimi-ai",
    "xiaomi-mimo-token-plan",
]

MANUAL_UPDATE_VENDOR_IDS = [
    "xfyun-xingchen-coding-plan",
]
