"""Back-compat test entrypoint.

The actual tests live under catalog/UTtest.

Run:
  python -m catalog.selftest
"""

from __future__ import annotations

import unittest

from .UTtest import selftest as _suite


if __name__ == "__main__":
    raise SystemExit(unittest.main(module=_suite))
