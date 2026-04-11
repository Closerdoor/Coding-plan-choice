"""LiveCodeBench source."""

from __future__ import annotations

import json
from typing import Dict, List

from .. import ranking_core as core


SOURCE_NAME = "livecodebench"
SOURCE_URL = "https://livecodebench.github.io/performances_generation.json"


def fetch() -> List[core.ModelObservation]:
    """Use latest date in the dataset, average across platforms/difficulty."""

    data = json.loads(core.http_get(SOURCE_URL).decode("utf-8"))

    perfs = data.get("performances") or []
    if not perfs:
        return []

    latest_date = max(p.get("date") for p in perfs if isinstance(p.get("date"), int))

    by_model: Dict[str, List[float]] = {}
    for p in perfs:
        if p.get("date") != latest_date:
            continue
        model = p.get("model")
        score = p.get("pass@1")
        if not isinstance(model, str) or not isinstance(score, (int, float)):
            continue
        by_model.setdefault(model, []).append(float(score))

    display_by_model: Dict[str, str] = {}
    for m in data.get("models") or []:
        if not isinstance(m, dict):
            continue
        name = m.get("model_name")
        disp = m.get("model_repr")
        if isinstance(name, str) and isinstance(disp, str):
            display_by_model[name] = disp

    out: List[core.ModelObservation] = []
    for model, vals in by_model.items():
        avg = sum(vals) / max(1, len(vals))
        display = core.norm_model(display_by_model.get(model, model))
        provider = (
            core.infer_provider_from_model(display)
            or core.infer_provider_from_model(model)
            or "Unknown"
        )
        out.append(
            core.ModelObservation(
                source=SOURCE_NAME,
                model=display,
                provider=core.canonical_provider(provider, display),
                score=avg,
                meta={"latest_date_ms": latest_date, "n": len(vals), "url": SOURCE_URL},
            )
        )
    return out
