"""Self-tests for the ranking pipeline (stdlib-only).

These tests avoid network calls.
Run:
  python scripts/selftest_model_rankings.py
"""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts import ranking_core as core  # noqa: E402
from scripts.generate_model_top3 import _render_top3_md  # noqa: E402


def _strip_generated_time(md: str) -> str:
    # Normalize timestamps to make comparisons stable.
    return re.sub(
        r"^- 生成时间（UTC）：.*$", "- 生成时间（UTC）：<normalized>", md, flags=re.M
    )


class TestCoreParsing(unittest.TestCase):
    def test_infer_param_b(self) -> None:
        self.assertEqual(core.infer_param_b("EXAONE-4.0-32B"), 32.0)
        self.assertEqual(core.infer_param_b("meta-llama/Llama-3.3-70B-Instruct"), 70.0)
        self.assertEqual(core.infer_param_b("Qwen3-235B-A22B"), 235.0)
        self.assertEqual(core.infer_param_b("Qwen3-Coder-480B-A35B-Instruct"), 480.0)
        self.assertIsNone(core.infer_param_b("gpt-5"))

    def test_is_excluded_model_keywords(self) -> None:
        self.assertTrue(core.is_excluded_model("foo-int4"))
        self.assertTrue(core.is_excluded_model("bar-mini"))
        self.assertTrue(core.is_excluded_model("some-gguf"))
        self.assertTrue(core.is_excluded_model("image-generator"))

    def test_is_excluded_model_param_threshold(self) -> None:
        self.assertTrue(core.is_excluded_model("Qwen2.5-Coder-32B-Instruct"))
        self.assertFalse(core.is_excluded_model("Llama-3.3-70B-Instruct"))
        self.assertFalse(core.is_excluded_model("Qwen3-235B-A22B"))


class TestProviderInference(unittest.TestCase):
    def test_provider_from_model_patterns(self) -> None:
        self.assertEqual(
            core.canonical_provider(
                "", "zai-org/GLM-4.6", allow_fallback_to_raw_provider=False
            ),
            "Zhipu AI",
        )
        self.assertEqual(
            core.canonical_provider(
                "",
                "Qwen/Qwen3-Coder-480B-A35B-Instruct",
                allow_fallback_to_raw_provider=False,
            ),
            "Alibaba",
        )
        self.assertEqual(
            core.canonical_provider(
                "",
                "meta-llama/Llama-3.3-70B-Instruct",
                allow_fallback_to_raw_provider=False,
            ),
            "Meta",
        )
        self.assertEqual(
            core.canonical_provider(
                "", "amazon.nova-premier-v1:0", allow_fallback_to_raw_provider=False
            ),
            "Amazon",
        )

    def test_provider_fallback_whitelist(self) -> None:
        # Unknown submitter org should not become a provider.
        self.assertEqual(
            core.canonical_provider("agentica-org", "agentica-org/DeepSWE-Preview"),
            "Unknown",
        )
        # Known providers are allowed as a last resort.
        self.assertEqual(
            core.canonical_provider("OpenAI", "some-custom-model-name"), "OpenAI"
        )


class TestAggregation(unittest.TestCase):
    def test_aggregate_scores_weighted_over_present_sources(self) -> None:
        obs = [
            core.ModelObservation(
                source="swebench", model="A", provider="OpenAI", score=10.0, meta={}
            ),
            core.ModelObservation(
                source="swebench", model="B", provider="OpenAI", score=5.0, meta={}
            ),
            core.ModelObservation(
                source="livecodebench",
                model="B",
                provider="OpenAI",
                score=99.0,
                meta={},
            ),
        ]
        total, per_source, display = core.aggregate_scores(obs)
        # A only appears in swebench => total should equal that unit score (normalized by present sources).
        a_key = (core.model_join_key("A"), "OpenAI")
        b_key = (core.model_join_key("B"), "OpenAI")
        self.assertIn(a_key, total)
        self.assertIn(b_key, total)
        self.assertIn("swebench", per_source[a_key])
        self.assertNotIn("livecodebench", per_source[a_key])
        self.assertIn("swebench", per_source[b_key])
        self.assertIn("livecodebench", per_source[b_key])
        self.assertEqual(display[a_key], "A")


class TestTop3FromJson(unittest.TestCase):
    def test_top3_renders_from_scores_json(self) -> None:
        scores_path = REPO_ROOT / "MODEL_SCORES.json"
        if not scores_path.exists():
            self.skipTest(
                "MODEL_SCORES.json not found; run update_model_rankings.py first"
            )
        payload = json.loads(scores_path.read_text(encoding="utf-8"))
        md = _render_top3_md(payload=payload)
        out_path = REPO_ROOT / "MODEL_TOP3.md"
        if out_path.exists():
            on_disk = out_path.read_text(encoding="utf-8")
            self.assertEqual(_strip_generated_time(md), _strip_generated_time(on_disk))
        # Should not contain Unknown provider section.
        self.assertNotIn("## Unknown", md)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
