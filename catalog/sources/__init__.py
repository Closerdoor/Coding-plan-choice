"""Catalog source modules.

Each module should expose a `fetch(...)` function that returns normalized plan data
for one vendor/package.
"""

from __future__ import annotations

from . import tencent_cloud_coding_plan


__all__ = ["tencent_cloud_coding_plan"]
