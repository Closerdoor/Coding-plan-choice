"""One-shot entrypoint to update model ranking artifacts.

Workflow:
1) Fetch + aggregate -> MODEL_RANKING.md + MODEL_SCORES.json
2) Generate Top3 from JSON -> MODEL_TOP3.md
"""

from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_imports() -> None:
    """Allow running via `python scripts/update_model_rankings.py`.

    Relative imports require a package context, so we add the repo root to sys.path
    and import via the `scripts.*` package name.
    """

    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))


_bootstrap_imports()

from scripts.generate_model_ranking import run as run_ranking  # noqa: E402
from scripts.generate_model_top3 import run as run_top3  # noqa: E402


def main() -> int:
    run_ranking()
    run_top3()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
