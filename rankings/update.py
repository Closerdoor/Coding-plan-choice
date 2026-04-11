"""One-shot entrypoint to update ranking artifacts.

Workflow:
1) Fetch + aggregate -> artifacts/rankings/MODEL_RANKING.md + MODEL_SCORES.json
2) Generate Top3 from JSON -> artifacts/rankings/MODEL_TOP3.md
"""

from __future__ import annotations

from .generate_ranking import run as run_ranking
from .generate_top3 import run as run_top3


def main() -> int:
    run_ranking()
    run_top3()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
