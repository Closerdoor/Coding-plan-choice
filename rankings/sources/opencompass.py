"""OpenCompass Rank source."""

from __future__ import annotations

from typing import List

from .. import core


SOURCE_NAME = "opencompass"
SOURCE_URL = "https://rank.opencompass.org.cn/"


def fetch() -> List[core.ModelObservation]:
    base = "https://rank.opencompass.org.cn/gw/opencompass-be"
    months_url = base + "/api/v1/rank/listRankTableAvailableMonths"
    months_resp = core.http_post_json(
        months_url,
        {"rankingType": 0, "benchmarkType": 0},
        headers={
            "Origin": "https://rank.opencompass.org.cn",
            "Referer": "https://rank.opencompass.org.cn/",
        },
    )
    months = months_resp.get("data") or []
    month = None
    for m in months:
        if isinstance(m, dict) and m.get("month") == "REALTIME":
            month = "REALTIME"
            break
    if (
        month is None
        and months
        and isinstance(months[0], dict)
        and isinstance(months[0].get("month"), str)
    ):
        month = months[0]["month"]
    if month is None:
        return []

    rankings_url = base + "/api/v1/rank/listModelRankings"
    resp = core.http_post_json(
        rankings_url,
        {"rankingType": 0, "benchmarkType": 0, "month": month},
        headers={
            "Origin": "https://rank.opencompass.org.cn",
            "Referer": "https://rank.opencompass.org.cn/",
        },
    )
    if not resp.get("success"):
        return []

    d = resp.get("data") or {}
    rankings = d.get("modelRankings") or []
    if not rankings:
        return []

    n = max(
        int(r.get("ranking")) for r in rankings if isinstance(r.get("ranking"), int)
    )
    out: List[core.ModelObservation] = []
    for r in rankings:
        model = r.get("model")
        org = r.get("org")
        rank = r.get("ranking")
        score = r.get("score")
        if not (
            isinstance(model, str) and isinstance(org, str) and isinstance(rank, int)
        ):
            continue
        provider = core.canonical_provider(org, model)
        try:
            s = float(score)
        except Exception:
            s = core.rank_to_unit_score(int(rank), n)
        out.append(
            core.ModelObservation(
                source=SOURCE_NAME,
                model=core.norm_model(model),
                provider=provider,
                score=s,
                meta={"url": SOURCE_URL, "month": month, "rank": rank, "n": n},
            )
        )
    return out
