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
]
