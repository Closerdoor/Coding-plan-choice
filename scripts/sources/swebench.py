"""SWE-bench source."""

from __future__ import annotations

import json
import re
from typing import Dict, List, Tuple

from .. import ranking_core as core


SOURCE_NAME = "swebench"
SOURCE_URL = "https://www.swebench.com/"


def fetch() -> List[core.ModelObservation]:
    html = core.http_get(SOURCE_URL).decode("utf-8", "replace")
    m = re.search(r'<script[^>]+id="leaderboard-data"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        return []
    data = json.loads(m.group(1))

    rows: List[Tuple[str, str, str, float]] = []
    for section in data:
        for r in section.get("results") or []:
            tags = r.get("tags") or []
            model = None
            org = None
            for t in tags:
                if isinstance(t, str) and t.startswith("Model:"):
                    model = t.split(":", 1)[1].strip()
                elif isinstance(t, str) and t.startswith("Org:"):
                    org = t.split(":", 1)[1].strip()
            resolved = r.get("resolved")
            if not (isinstance(model, str) and isinstance(resolved, (int, float))):
                continue

            # SWE-bench's Org is typically the submitter/team, not the underlying model provider.
            provider = core.canonical_provider(
                org or "",
                model,
                allow_fallback_to_raw_provider=False,
            )
            rows.append((core.norm_model(model), provider, org or "", float(resolved)))

    best: Dict[Tuple[str, str], Tuple[float, str]] = {}
    for model, provider, submitter_org, resolved in rows:
        k = (model, provider)
        prev = best.get(k)
        if prev is None or resolved > prev[0]:
            best[k] = (resolved, submitter_org)

    out: List[core.ModelObservation] = []
    for (model, provider), (resolved, submitter_org) in best.items():
        out.append(
            core.ModelObservation(
                source=SOURCE_NAME,
                model=model,
                provider=provider,
                score=resolved,
                meta={
                    "url": SOURCE_URL,
                    "metric": "resolved(%)",
                    "submitter_org": submitter_org,
                },
            )
        )
    return out
