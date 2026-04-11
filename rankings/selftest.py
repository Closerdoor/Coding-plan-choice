"""Back-compat test entrypoint.

The actual tests live under rankings/UTtest.

Run:
  python -m rankings.selftest
"""

from __future__ import annotations

import unittest

from .UTtest import selftest as _suite


if __name__ == "__main__":
    raise SystemExit(unittest.main(module=_suite))
