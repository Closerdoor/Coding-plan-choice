"""HELM source (placeholder).

We keep the module to preserve a stable interface, but return empty for now.
"""

from __future__ import annotations

from typing import List

from .. import ranking_core as core


SOURCE_NAME = "helm"
SOURCE_URL = "https://crfm.stanford.edu/helm/latest/"


def fetch() -> List[core.ModelObservation]:
    return []
