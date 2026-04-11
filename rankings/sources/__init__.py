"""Source registry for model leaderboards."""

from __future__ import annotations

from . import arena, helm, livecodebench, opencompass, swebench


SOURCES = [
    livecodebench,
    swebench,
    arena,
    opencompass,
    helm,
]
