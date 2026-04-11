"""One-shot entrypoint to update ranking artifacts.

Output:
  rankings/output/MODEL_RANKING.md
  rankings/output/MODEL_SCORES.json
  rankings/output/MODEL_TOP3.md

Failure semantics:
- Only keep previous artifacts when the script fails (exception / non-zero exit)
  or produces an empty aggregation.
- Success always updates the artifacts.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from . import core
from .generate_ranking import run as run_ranking
from .generate_top3 import run as run_top3


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "rankings" / "output"


def main() -> int:
    # Transactional update: generate into a temp dir first, then swap into place.
    tmp_dir = OUTPUT_DIR.with_name(OUTPUT_DIR.name + ".__tmp__")
    backup_dir = OUTPUT_DIR.with_name(OUTPUT_DIR.name + ".__bak__")

    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Generate new artifacts into tmp.
    run_ranking(output_dir=tmp_dir)
    scores_path = tmp_dir / "MODEL_SCORES.json"
    payload = core.load_scores_json(scores_path)
    if not payload.get("models"):
        raise RuntimeError(
            "aggregation produced 0 models; refusing to overwrite artifacts"
        )
    run_top3(output_dir=tmp_dir)

    # Validate expected outputs exist before swapping.
    expected = [
        tmp_dir / "MODEL_RANKING.md",
        tmp_dir / "MODEL_SCORES.json",
        tmp_dir / "MODEL_TOP3.md",
    ]
    missing = [str(p) for p in expected if not p.exists()]
    if missing:
        raise RuntimeError("missing expected artifacts: " + ", ".join(missing))

    # Swap directories.
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    if OUTPUT_DIR.exists():
        OUTPUT_DIR.rename(backup_dir)
    tmp_dir.rename(OUTPUT_DIR)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
