"""Entrypoint for catalog source connectivity preflight.

Run:
  python -m catalog.preflight
"""

from __future__ import annotations

from .update import preflight_only


if __name__ == "__main__":
    raise SystemExit(preflight_only())
