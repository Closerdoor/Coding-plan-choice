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
        "source_url": "https://cloud.tencent.com/act/pro/codingplan",
        "source_module": "catalog.sources.tencent_cloud_coding_plan",
    }
]
