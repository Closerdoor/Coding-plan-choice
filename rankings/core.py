"""Shared core for model ranking aggregation.

Design goals:
- stdlib-only
- keep ranking logic deterministic and transparent
- isolate per-source scraping/parsing into scripts/sources/*

This module intentionally does not import any source modules to avoid cycles.
"""

from __future__ import annotations

import dataclasses
import datetime as _dt
import json
import re
import ssl
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


WEIGHTS: Dict[str, float] = {
    "swebench": 0.30,
    "livecodebench": 0.30,
    "arena": 0.15,
    "helm": 0.15,  # placeholder source; may be empty.
    "opencompass": 0.10,
}


EXCLUDE_NAME_PATTERNS = [
    r"\bdistill\b",
    r"\bquant\b",
    r"\bint4\b",
    r"\bint8\b",
    r"\b4bit\b",
    r"\b8bit\b",
    r"\bgguf\b",
    r"\bawq\b",
    r"\bgptq\b",
    r"\bmini\b",
    r"\bsmall\b",
    r"\blite\b",
    r"\btiny\b",
    # Exclude obviously non-LLM generative media models.
    r"\bimage\b",
    r"\bvideo\b",
    r"\bt2v\b",
    r"\bi2v\b",
    r"\bflux\b",
    r"\bsora\b",
    r"\bveo\b",
    r"\bseedance\b",
    r"\bdreamina\b",
    r"\bhunyuan-image\b",
    r"\bhunyuan-video\b",
]


# Treat models with explicit parameter size < this threshold as "small".
# Only applies when we can parse a size from the model identifier (e.g. "32B", "70B").
SMALL_PARAMS_LT_B = 70.0


# Minimal alias table (can be expanded later).
ALIASES: Dict[str, str] = {
    "google deepmind": "Google",
    "google": "Google",
    "minimax": "MiniMax",
    "meta": "Meta",
    "meta-llama": "Meta",
    "alibaba": "Alibaba",
    "tencent": "Tencent",
    "xai": "xAI",
    "z.ai": "Zhipu AI",
    "z-ai": "Zhipu AI",
    "zai": "Zhipu AI",
    "zai-org": "Zhipu AI",
    "moonshot": "Moonshot AI",
    "stepfun": "StepFun",
    "amazon nova": "Amazon",
    "byte dance": "ByteDance",
    "bytedance": "ByteDance",
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    # Common HF orgs -> company names.
    "qwen": "Alibaba",
    "mistralai": "Mistral",
    "deepseek-ai": "DeepSeek",
    "zhipuai": "Zhipu AI",
}


# Only these are treated as valid "model providers" when we have to fall back to
# a source's org/provider field. This avoids counting submitter orgs / agent teams.
KNOWN_MODEL_PROVIDERS = {
    "Alibaba",
    "Amazon",
    "Anthropic",
    "ByteDance",
    "DeepSeek",
    "EXAONE",
    "Google",
    "Meta",
    "Microsoft",
    "MiniMax",
    "Mistral",
    "Moonshot AI",
    "NVIDIA",
    "OpenAI",
    "StepFun",
    "Tencent",
    "Zhipu AI",
    "xAI",
}


# Infer provider from model name when sources provide submitter orgs (e.g. SWE-bench).
PROVIDER_FROM_MODEL_PATTERNS: List[Tuple[str, str]] = [
    # Order matters: more specific first.
    # NOTE: avoid `\b` here because many names embed digits directly (e.g. Qwen3, GLM-4.6).
    (r"^claude", "Anthropic"),
    (r"^gemini", "Google"),
    (r"^gpt", "OpenAI"),
    (r"^o[0-9]", "OpenAI"),
    (r"^codex", "OpenAI"),
    (r"^deepseek", "DeepSeek"),
    (r"^kimi", "Moonshot AI"),
    (r"^glm", "Zhipu AI"),
    (r"^qwen", "Alibaba"),
    (r"^doubao", "ByteDance"),
    (r"^minimax", "MiniMax"),
    (r"^llama", "Meta"),
    (r"^mistral", "Mistral"),
    (r"^devstral", "Mistral"),
    (r"^exaone", "EXAONE"),
    (r"^nemotron", "NVIDIA"),
    (r"^frog", "Microsoft"),
    (r"^amazon\.nova", "Amazon"),
]


@dataclasses.dataclass(frozen=True)
class ModelObservation:
    source: str
    model: str
    provider: str
    # Higher is better. Can be a score or a rank-derived score.
    score: float
    # Optional raw fields to keep traceability.
    meta: Dict[str, Any]


def utc_now_iso() -> str:
    return _dt.datetime.now(tz=_dt.timezone.utc).replace(microsecond=0).isoformat()


def http_get(
    url: str, *, timeout_s: int = 60, allow_insecure_ssl: bool = False
) -> bytes:
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    ctx = None
    if allow_insecure_ssl:
        ctx = ssl._create_unverified_context()  # noqa: SLF001 - pragmatic fallback for some hosts in this env.
    with urllib.request.urlopen(req, timeout=timeout_s, context=ctx) as r:
        return r.read()


def http_post_json(
    url: str,
    payload: Dict[str, Any],
    *,
    timeout_s: int = 60,
    headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    hdrs = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    if headers:
        hdrs.update(headers)
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout_s) as r:
        raw = r.read().decode("utf-8", "replace")
    return json.loads(raw)


def norm_provider(name: str) -> str:
    if not name:
        return "Unknown"
    k = re.sub(r"\s+", " ", name.strip()).lower()
    return ALIASES.get(k, name.strip())


def norm_model(name: str) -> str:
    raw = (name or "").strip()

    # Reduce common model identifiers embedded as URLs into a stable id.
    # e.g. https://huggingface.co/zai-org/GLM-4.6 -> zai-org/GLM-4.6
    if raw.lower().startswith("http://") or raw.lower().startswith("https://"):
        mm = re.search(r"huggingface\.co/([^/]+)/([^/?#]+)", raw, re.I)
        if mm:
            raw = f"{mm.group(1)}/{mm.group(2)}"

    s = re.sub(r"\s+", " ", raw)
    # Arena-style capability suffixes like "... [web-search]" make joins noisy.
    s = re.sub(r"\s*\[[^\]]+\]\s*$", "", s)
    return s


def model_join_key(model: str) -> str:
    """Normalization for cross-source joins and case-dedup."""

    s = norm_model(model).lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def prefer_display(a: str, b: str) -> str:
    """Pick a more "official looking" display string deterministically."""

    if not a:
        return b
    if not b:
        return a
    if a == b:
        return a
    # Prefer versions with more uppercase letters.
    au = sum(1 for ch in a if "A" <= ch <= "Z")
    bu = sum(1 for ch in b if "A" <= ch <= "Z")
    if au != bu:
        return a if au > bu else b
    # Prefer longer (often includes version info).
    if len(a) != len(b):
        return a if len(a) > len(b) else b
    # Stable fallback.
    return min(a, b)


def infer_provider_from_model(model: str) -> Optional[str]:
    m = (model or "").strip().lower()
    if not m:
        return None

    # If the model is a URL (common in some tool submissions), try to extract the underlying id.
    if m.startswith("http://") or m.startswith("https://"):
        mm = re.search(r"huggingface\.co/([^/]+)/([^/?#]+)", m)
        if mm:
            org = mm.group(1).strip().lower()
            repo = mm.group(2).strip().lower()
            from_repo = infer_provider_from_model(repo)
            if from_repo:
                return from_repo
            # Only treat HF org as provider if it's a known model developer org.
            if org in {
                "openai",
                "anthropic",
                "google",
                "deepseek-ai",
                "deepseek",
                "qwen",
                "zai-org",
                "zhipuai",
                "moonshot",
                "meta-llama",
                "mistralai",
            }:
                return norm_provider(org)
            return None
        return None

    if "/" in m and m.count("/") == 1:
        org, _repo = m.split("/", 1)
        if org in {
            "openai",
            "anthropic",
            "google",
            "deepseek-ai",
            "deepseek",
            "qwen",
            "zai-org",
            "zhipuai",
            "moonshot",
            "meta-llama",
            "mistralai",
        }:
            return norm_provider(org)

    for pat, provider in PROVIDER_FROM_MODEL_PATTERNS:
        if re.search(pat, m):
            return provider
    if m.startswith("xbai"):
        return "OpenAI"
    if "nemotron" in m:
        return "NVIDIA"
    return None


def canonical_provider(
    raw_provider: str, model: str, *, allow_fallback_to_raw_provider: bool = True
) -> str:
    """Map observations to the underlying model developer/provider."""

    inferred = infer_provider_from_model(model)
    if inferred:
        return norm_provider(inferred)

    inferred2 = infer_provider_from_model(raw_provider)
    if inferred2:
        return norm_provider(inferred2)

    if not allow_fallback_to_raw_provider:
        return "Unknown"

    normalized = norm_provider(raw_provider)
    if normalized in KNOWN_MODEL_PROVIDERS:
        return normalized
    return "Unknown"


def infer_param_b(model: str) -> Optional[float]:
    """Best-effort parse parameter size in billions from a model name."""

    s = (model or "").strip()
    if not s:
        return None
    sl = s.lower()

    # Prefer MoE-style total params if present: "235B-A22B".
    m = re.search(r"\b(\d+(?:\.\d+)?)\s*b\s*-\s*a\s*(\d+(?:\.\d+)?)\s*b\b", sl)
    if m:
        try:
            return float(m.group(1))
        except Exception:
            return None

    nums: List[float] = []
    for mm in re.finditer(r"\b(\d+(?:\.\d+)?)\s*b\b", sl):
        try:
            nums.append(float(mm.group(1)))
        except Exception:
            continue
    if not nums:
        return None
    return max(nums)


def is_excluded_model(model: str) -> bool:
    s = (model or "").lower()
    if any(re.search(p, s) for p in EXCLUDE_NAME_PATTERNS):
        return True
    sz = infer_param_b(model)
    return sz is not None and sz < SMALL_PARAMS_LT_B


def rank_to_unit_score(rank: int, n: int) -> float:
    """Convert rank (1..n) to (0..1], higher better."""

    if n <= 1:
        return 1.0
    return max(0.0, min(1.0, 1.0 - (rank - 1) / (n - 1)))


def aggregate_scores(
    obs: Iterable[ModelObservation],
) -> Tuple[
    Dict[Tuple[str, str], float],
    Dict[Tuple[str, str], Dict[str, float]],
    Dict[Tuple[str, str], str],
]:
    """Return: total_score, per_source_unit, display_by_key."""

    by_source: Dict[str, List[ModelObservation]] = {}
    for o in obs:
        by_source.setdefault(o.source, []).append(o)

    display_by_key: Dict[Tuple[str, str], str] = {}
    for o in obs:
        mk = model_join_key(o.model)
        if not mk:
            continue
        k = (mk, o.provider)
        display_by_key[k] = prefer_display(display_by_key.get(k, ""), o.model)

    per_source_unit: Dict[Tuple[str, str], Dict[str, float]] = {}
    for source, rows in by_source.items():
        best: Dict[Tuple[str, str], float] = {}
        for r in rows:
            mk = model_join_key(r.model)
            if not mk:
                continue
            k = (mk, r.provider)
            best[k] = max(best.get(k, float("-inf")), float(r.score))

        ranked = sorted(best.items(), key=lambda kv: kv[1], reverse=True)
        n = len(ranked)
        for i, (k, _score) in enumerate(ranked, start=1):
            unit = rank_to_unit_score(i, n)
            per_source_unit.setdefault(k, {})[source] = unit

    total: Dict[Tuple[str, str], float] = {}
    for k, units in per_source_unit.items():
        num = 0.0
        den = 0.0
        for src, unit in units.items():
            w = WEIGHTS.get(src, 0.0)
            if w <= 0.0:
                continue
            num += w * unit
            den += w
        if den > 0.0:
            total[k] = num / den
    return total, per_source_unit, display_by_key


def to_markdown_table(rows: List[List[str]]) -> str:
    if not rows:
        return ""
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    out: List[str] = []
    out.append(
        "| "
        + " | ".join(rows[0][i].ljust(widths[i]) for i in range(len(widths)))
        + " |"
    )
    out.append("| " + " | ".join("-" * widths[i] for i in range(len(widths))) + " |")
    for r in rows[1:]:
        out.append(
            "| " + " | ".join(r[i].ljust(widths[i]) for i in range(len(widths))) + " |"
        )
    return "\n".join(out)


def render_model_ranking_md(
    *,
    total: Dict[Tuple[str, str], float],
    per_source: Dict[Tuple[str, str], Dict[str, float]],
    display_by_key: Dict[Tuple[str, str], str],
    warnings: List[str],
) -> str:
    now = utc_now_iso()
    ranked = sorted(total.items(), key=lambda kv: kv[1], reverse=True)

    header = [
        "# 模型能力榜单（自动生成）",
        "",
        f"- 生成时间（UTC）：{now}",
        "- 说明：按 5 个榜单（代码优先）做分位数标准化后加权平均；缺失榜单不计入分母。",
        "- 权重：SWE-bench 0.30、LiveCodeBench 0.30、Arena 0.15、HELM 0.15、OpenCompass 0.10。",
        "- 过滤规则（Top3 输出用）：排除 distill/quant/int4/int8/gguf/awq/gptq 以及 mini/small/lite/tiny 等小模型。",
        "",
        "## 全局排名",
        "",
    ]

    cols = [
        "Rank",
        "Provider",
        "Model",
        "Score(0..1)",
        "SWE",
        "LCB",
        "Arena",
        "HELM",
        "OC",
    ]
    table: List[List[str]] = [cols]
    for i, ((model_key, provider), score) in enumerate(ranked, start=1):
        units = per_source.get((model_key, provider), {})
        model = display_by_key.get((model_key, provider), model_key)
        provider = canonical_provider(provider, model)
        table.append(
            [
                str(i),
                provider,
                model,
                f"{score:.4f}",
                f"{units.get('swebench', 0.0):.3f}" if "swebench" in units else "",
                f"{units.get('livecodebench', 0.0):.3f}"
                if "livecodebench" in units
                else "",
                f"{units.get('arena', 0.0):.3f}" if "arena" in units else "",
                f"{units.get('helm', 0.0):.3f}" if "helm" in units else "",
                f"{units.get('opencompass', 0.0):.3f}"
                if "opencompass" in units
                else "",
            ]
        )

    md = "\n".join(header) + to_markdown_table(table) + "\n"
    if warnings:
        md += "\n## 抓取/解析告警\n\n" + "\n".join(f"- {w}" for w in warnings) + "\n"
    md += "\n## 数据源\n\n"
    md += "- LiveCodeBench: https://livecodebench.github.io/\n"
    md += "- SWE-bench: https://www.swebench.com/\n"
    md += "- Arena: https://lmarena.ai/leaderboard\n"
    md += "- HELM: https://crfm.stanford.edu/helm/latest/\n"
    md += "- OpenCompass Rank: https://rank.opencompass.org.cn/\n"
    return md


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_scores_json(
    *,
    path: Path,
    total: Dict[Tuple[str, str], float],
    per_source: Dict[Tuple[str, str], Dict[str, float]],
    display_by_key: Dict[Tuple[str, str], str],
    warnings: List[str],
) -> None:
    now = utc_now_iso()
    ranked = sorted(total.items(), key=lambda kv: kv[1], reverse=True)

    models: List[Dict[str, Any]] = []
    for (model_key, provider), score in ranked:
        units = per_source.get((model_key, provider), {})
        model = display_by_key.get((model_key, provider), model_key)
        provider = canonical_provider(provider, model)
        models.append(
            {
                "provider": provider,
                "model": model,
                "model_join_key": model_key,
                "total_score_0_1": float(score),
                "per_source_unit_scores": {k: float(v) for k, v in units.items()},
            }
        )

    payload = {
        "generated_at_utc": now,
        "weights": WEIGHTS,
        "filters": {
            "exclude_name_patterns": EXCLUDE_NAME_PATTERNS,
            "small_params_lt_b": SMALL_PARAMS_LT_B,
        },
        "warnings": warnings,
        "models": models,
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_scores_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
