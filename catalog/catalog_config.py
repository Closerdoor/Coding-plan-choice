"""Catalog configuration (mainline).

Keep this file as pure data/config. Vendor-specific parsing belongs in
catalog/sources/* modules.
"""

from __future__ import annotations


VENDORS = [
    {
        "vendor_id": "tencent-cloud-coding-plan",
        "company_name": "腾讯云",
        "vendor_name": "腾讯云大模型 Coding Plan",
        "source_urls": [
            "https://cloud.tencent.com/act/pro/codingplan",
            "https://cloud.tencent.com/document/product/1823/130092",
        ],
        "source_module": "catalog.sources.tencent_cloud_coding_plan",
    },
    {
        "vendor_id": "volcengine-coding-plan",
        "company_name": "火山方舟",
        "vendor_name": "火山方舟 Coding Plan",
        "source_urls": [
            "https://www.volcengine.com/activity/codingplan",
            "https://www.volcengine.com/docs/82379/1925114?lang=zh",
        ],
        "source_module": "catalog.sources.volcengine_coding_plan",
    },
    {
        "vendor_id": "baidu-qianfan-coding-plan",
        "company_name": "百度千帆",
        "vendor_name": "百度千帆 Coding Plan",
        "source_urls": [
            "https://cloud.baidu.com/product/codingplan.html",
            "https://cloud.baidu.com/doc/qianfan/s/imlg0beiu",
        ],
        "source_module": "catalog.sources.baidu_qianfan_coding_plan",
    },
    {
        "vendor_id": "glm-coding-plan",
        "company_name": "智谱AI",
        "vendor_name": "GLM Coding Plan",
        "source_urls": [
            "https://bigmodel.cn/glm-coding",
            "https://docs.bigmodel.cn/cn/coding-plan/overview",
            "https://docs.bigmodel.cn/cn/coding-plan/faq",
            "https://docs.bigmodel.cn/cn/coding-plan/quick-start",
        ],
        "source_module": "catalog.sources.glm_coding_plan",
    },
    {
        "vendor_id": "minimax-token-plan",
        "company_name": "MiniMax",
        "vendor_name": "MiniMax Token Plan",
        "source_urls": [
            "https://platform.minimaxi.com/subscribe/token-plan",
            "https://platform.minimaxi.com/docs/token-plan/intro",
            "https://platform.minimaxi.com/docs/guides/pricing-token-plan",
            "https://platform.minimaxi.com/docs/guides/text-ai-coding-tools",
        ],
        "source_module": "catalog.sources.minimax_token_plan",
    },
]
