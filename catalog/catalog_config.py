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
]
