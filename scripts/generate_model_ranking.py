"""Generate MODEL_RANKING.md and MODEL_SCORES.json.

This is the only step that hits external network resources.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from . import ranking_core as core
from .sources import SOURCES


REPO_ROOT = Path(__file__).resolve().parents[1]


def run() -> List[str]:
    warnings: List[str] = []
    obs: List[core.ModelObservation] = []

    for src in SOURCES:
        name = getattr(src, "SOURCE_NAME", src.__name__)
        try:
            got = src.fetch()
            got = [o for o in got if not core.is_excluded_model(o.model)]
            obs.extend(got)
            if not got and name != "helm":
                warnings.append(f"source {name}: no observations")
        except Exception as e:
            warnings.append(f"source {name}: failed: {type(e).__name__}: {e}")

    # Arena contains many non-LLM modalities; only keep Arena models that also show up
    # in at least one non-Arena source (join by a simple normalized key).
    non_arena_keys = {
        core.model_join_key(o.model)
        for o in obs
        if o.source != "arena" and core.model_join_key(o.model)
    }
    filtered: List[core.ModelObservation] = []
    for o in obs:
        if o.source == "arena" and core.model_join_key(o.model) not in non_arena_keys:
            continue
        filtered.append(o)
    obs = filtered

    total, per_source, display_by_key = core.aggregate_scores(obs)

    md = core.render_model_ranking_md(
        total=total,
        per_source=per_source,
        display_by_key=display_by_key,
        warnings=warnings,
    )
    core.write_text(REPO_ROOT / "MODEL_RANKING.md", md)
    core.write_scores_json(
        path=REPO_ROOT / "MODEL_SCORES.json",
        total=total,
        per_source=per_source,
        display_by_key=display_by_key,
        warnings=warnings,
    )
    return warnings


def main() -> int:
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
