"""Generate artifacts/rankings/MODEL_TOP3.md from artifacts/rankings/MODEL_SCORES.json.

This step is intentionally no-network.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

from . import core


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "rankings" / "output"


def _render_top3_md(*, payload: Dict[str, Any]) -> str:
    now = core.utc_now_iso()
    models = payload.get("models") or []
    warnings = payload.get("warnings") or []

    by_provider: Dict[str, List[Tuple[str, float]]] = {}
    for m in models:
        provider = m.get("provider")
        model = m.get("model")
        score = m.get("total_score_0_1")
        if (
            not isinstance(provider, str)
            or not isinstance(model, str)
            or not isinstance(score, (int, float))
        ):
            continue
        if provider == "Unknown":
            continue
        # The ranking step already applied small-model filtering, but keep this as a guard.
        if core.is_excluded_model(model):
            continue
        by_provider.setdefault(provider, []).append((model, float(score)))

    for p in list(by_provider.keys()):
        by_provider[p].sort(key=lambda x: x[1], reverse=True)

    providers = sorted(
        by_provider.keys(),
        key=lambda p: (-(by_provider[p][0][1] if by_provider[p] else 0.0), p),
    )

    lines: List[str] = [
        "# 模型提供商 Top3（自动生成）",
        "",
        f"- 生成时间（UTC）：{now}",
        "- 说明：从全局榜单中按提供商分组，排除小模型后取 Top3。",
        "",
    ]

    for p in providers:
        top = by_provider[p][:3]
        if not top:
            continue
        lines.append(f"## {p}")
        lines.append("")
        rows: List[List[str]] = [["Rank", "Model", "Score(0..1)"]]
        for i, (model, score) in enumerate(top, start=1):
            rows.append([str(i), model, f"{score:.4f}"])
        lines.append(core.to_markdown_table(rows))
        lines.append("")

    if warnings:
        lines.append("## 抓取/解析告警")
        lines.append("")
        lines.extend([f"- {w}" for w in warnings])
        lines.append("")

    return "\n".join(lines)


def run() -> None:
    payload = core.load_scores_json(OUTPUT_DIR / "MODEL_SCORES.json")
    md = _render_top3_md(payload=payload)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    core.write_text(OUTPUT_DIR / "MODEL_TOP3.md", md)


def main() -> int:
    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
