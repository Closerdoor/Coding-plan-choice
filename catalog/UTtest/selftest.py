"""Self-tests for catalog generation (no network).

Run:
  python -m catalog.selftest
"""

from __future__ import annotations

import unittest


class TestPlaceholder(unittest.TestCase):
    def test_placeholder(self) -> None:
        # Real tests will be added alongside implementation.
        self.assertTrue(True)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
