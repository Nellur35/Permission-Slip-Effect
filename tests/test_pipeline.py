from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline import pipeline as ppl


class FakeProvider:
    def __init__(self, name: str = "fake", model: str = "fake-model", responses: list[str] | None = None):
        self.name = name
        self.model = model
        self.responses = list(responses or [])
        self.calls = []

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        self.calls.append({"system": system, "user": user, "temperature": temperature})
        if not self.responses:
            raise RuntimeError("no fake responses left")
        return self.responses.pop(0)


def test_load_frameworks_reads_external_catalog():
    frameworks = ppl.load_frameworks()
    assert "FPR" in frameworks
    assert frameworks["AdR"]["name"] == "Adversarial Reasoning"
    assert "{input}" in frameworks["RCAR"]["prompt"]


def test_strip_fenced_code_block_handles_json_fences():
    raw = "```json\n{\"summary\": \"ok\"}\n```"
    assert ppl.strip_fenced_code_block(raw) == '{"summary": "ok"}'


def test_parse_json_response_returns_none_for_non_json():
    assert ppl.parse_json_response("not json") is None


def test_parse_json_response_accepts_fenced_json():
    parsed = ppl.parse_json_response("```json\n{\"summary\": \"ok\"}\n```")
    assert parsed == {"summary": "ok"}


def test_build_stage_prompt_injects_problem_and_context():
    full_input = ppl.build_stage_input("prior findings", "new problem")
    prompt = ppl.build_stage_prompt("FPR", full_input)
    assert "prior findings" in prompt
    assert "new problem" in prompt


def test_framework_temperature_is_higher_for_adversarial_stage():
    assert ppl.framework_temperature("AdR") == 0.7
    assert ppl.framework_temperature("FPR") == 0.3


def test_estimate_cost_returns_expected_structure():
    estimate = ppl.estimate_cost("standard", "claude-sonnet-4-20250514")
    assert estimate["stages"] == 6
    assert estimate["estimated_total_tokens"] > 0
    assert estimate["estimated_cost_usd"] > 0


def test_estimate_cost_with_challenger_uses_both_models():
    estimate = ppl.estimate_cost("standard", "claude-sonnet-4-20250514", "gpt-4o")
    assert estimate["challenger_model"] == "gpt-4o"
    assert estimate["estimated_cost_usd"] > 0


def test_run_stage_parses_fenced_json():
    provider = FakeProvider(responses=['```json\n{"key_insight": "test"}\n```'])
    result = ppl.run_stage(provider, "FPR", "", "Should we ship?")
    assert result.error is None
    assert result.parsed == {"key_insight": "test"}
    assert provider.calls[0]["temperature"] == 0.3


def test_run_stage_captures_provider_errors():
    class FailingProvider(FakeProvider):
        def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
            raise RuntimeError("boom")

    result = ppl.run_stage(FailingProvider(), "RCAR", "", "Why is this failing?")
    assert result.error == "boom"
    assert result.raw == ""


def test_run_pipeline_uses_challenger_for_adversarial_stage():
    architect = FakeProvider(
        name="architect",
        model="arch-model",
        responses=[
            '{"key_insight": "framing"}',
            '{"key_insight": "root cause"}',
            '{"key_insight": "options"}',
            '{"key_insight": "premortem"}',
            '{"summary": "final", "key_findings": [], "disagreements": [], "risks_ranked": [], "recommended_action": "act", "navigator_decisions_needed": []}',
        ],
    )
    challenger = FakeProvider(
        name="challenger",
        model="chal-model",
        responses=['{"key_insight": "uncomfortable truth"}'],
    )

    result = ppl.run_pipeline("standard", "Should we adopt this?", architect, challenger)

    assert len(result.stages) == 5
    assert result.stages[2].stage == "AdR"
    assert result.stages[2].model == "challenger"
    assert architect.calls[-1]["temperature"] == 0.3
    assert challenger.calls[0]["temperature"] == 0.7
    assert result.convergence["result"]["summary"] == "final"


def test_run_review_wraps_artifact_text(tmp_path: Path):
    artifact = tmp_path / "architecture.md"
    artifact.write_text("# Architecture\n\nTrust boundary goes here.")
    architect = FakeProvider(
        responses=[
            '{"key_insight": "reviewed"}',
            '{"key_insight": "options"}',
            '{"key_insight": "premortem"}',
            '{"summary": "done", "key_findings": [], "disagreements": [], "risks_ranked": [], "recommended_action": "fix", "navigator_decisions_needed": []}',
        ]
    )

    result = ppl.run_review(str(artifact), architect)

    assert result.pipeline == ppl.PIPELINES["review"]["name"]
    assert result.stages[0].stage == "AdR"
    assert "Trust boundary goes here" in architect.calls[0]["user"]


def test_build_parser_supports_frameworks_command():
    parser = ppl.build_parser()
    args = parser.parse_args(["frameworks"])
    assert args.command == "frameworks"
