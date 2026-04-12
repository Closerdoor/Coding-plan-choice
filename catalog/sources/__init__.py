"""Catalog source modules.

Each module should expose a `fetch(...)` function that returns normalized plan data
for one vendor/package.
"""

from __future__ import annotations

from . import baidu_qianfan_coding_plan
from . import glm_coding_plan
from . import tencent_cloud_coding_plan
from . import volcengine_coding_plan


__all__ = [
    "baidu_qianfan_coding_plan",
    "glm_coding_plan",
    "tencent_cloud_coding_plan",
    "volcengine_coding_plan",
]
