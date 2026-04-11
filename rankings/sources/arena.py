"""LMArena (Chatbot Arena) source.

The leaderboard is served via a Next.js streaming payload.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .. import core


SOURCE_NAME = "arena"
SOURCE_URL = "https://lmarena.ai/leaderboard"


def _decode_nextjs_push_string(s: str) -> Optional[str]:
    try:
        return json.loads('"' + s + '"')
    except Exception:
        try:
            return (
                s.replace(r"\\\"", '"')
                .replace(r"\\n", "\n")
                .replace(r"\\t", "\t")
                .replace(r"\\/", "/")
                .replace(r"\\\\", r"\\")
            )
        except Exception:
            return None


def fetch() -> List[core.ModelObservation]:
    html = core.http_get(SOURCE_URL, allow_insecure_ssl=True).decode("utf-8", "replace")

    chunks = re.findall(r"self\.__next_f\.push\(\[1,\"(.*?)\"\]\)", html, re.S)
    decoded: List[str] = []
    for c in chunks:
        d = _decode_nextjs_push_string(c)
        if d:
            decoded.append(d)

    best = None
    for d in decoded:
        if "initialModels" in d and (best is None or len(d) > len(best)):
            best = d
    if not best:
        return []

    colon = best.find(":")
    if colon == -1:
        return []
    payload = best[colon + 1 :].lstrip()
    try:
        arr = json.loads(payload)
    except Exception:
        return []

    def walk(x: Any) -> Optional[List[Dict[str, Any]]]:
        if (
            isinstance(x, dict)
            and "initialModels" in x
            and isinstance(x["initialModels"], list)
        ):
            return x["initialModels"]
        if isinstance(x, list):
            for y in x:
                r = walk(y)
                if r is not None:
                    return r
        if isinstance(x, dict):
            for y in x.values():
                r = walk(y)
                if r is not None:
                    return r
        return None

    models = walk(arr)
    if not models:
        return []

    items: List[Tuple[str, str, int, str]] = []
    for m in models:
        model_name = m.get("displayName") or m.get("name")
        org = m.get("organization") or m.get("provider")
        if not isinstance(model_name, str) or not isinstance(org, str):
            continue
        rb = m.get("rankByModality")
        rank = None
        modality = "overall"
        if isinstance(rb, dict):
            if isinstance(rb.get("coding"), int):
                rank = rb["coding"]
                modality = "coding"
            elif isinstance(rb.get("overall"), int):
                rank = rb["overall"]
                modality = "overall"
        if rank is None and isinstance(m.get("rank"), int):
            rank = m["rank"]
            modality = "overall"
        if rank is None:
            continue
        provider = core.canonical_provider(org, model_name)
        items.append((core.norm_model(model_name), provider, int(rank), modality))

    if not items:
        return []

    out: List[core.ModelObservation] = []
    for modality in sorted(set(i[3] for i in items)):
        subset = [i for i in items if i[3] == modality]
        n = max(i[2] for i in subset)
        for model, provider, rank, _m in subset:
            out.append(
                core.ModelObservation(
                    source=SOURCE_NAME,
                    model=model,
                    provider=provider,
                    score=core.rank_to_unit_score(rank, n),
                    meta={
                        "url": SOURCE_URL,
                        "rank": rank,
                        "n": n,
                        "modality": modality,
                    },
                )
            )
    return out
