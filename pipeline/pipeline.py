#!/usr/bin/env python3
"""
Security-First AI Dev Methodology — Reasoning Pipeline CLI

Orchestrates multi-model reasoning pipelines and adversarial reviews.
Ships as a reference implementation with an Anthropic provider included.
Additional providers can be added by implementing the Provider protocol.

Usage:
    # Adversarial review of an artifact
    python pipeline.py review architecture.md

    # Full reasoning pipeline
    python pipeline.py reason --pipeline standard "Should we migrate auth to OAuth2?"

    # Light pipeline with specific models
    python pipeline.py reason --pipeline light --architect claude --challenger gemini "Why do deploys keep failing?"

    # List available pipelines
    python pipeline.py pipelines
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, Protocol


class Provider(Protocol):
    """Minimal interface for an LLM provider."""

    name: str
    model: str

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        ...


class AnthropicProvider:
    name = "claude"

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        import urllib.error
        import urllib.request

        body = json.dumps(
            {
                "model": self.model,
                "max_tokens": 4096,
                "temperature": temperature,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }
        ).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                return "".join(block["text"] for block in data["content"] if block["type"] == "text")
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode()
            raise RuntimeError(f"Anthropic API error {exc.code}: {error_body}") from exc


class OpenAIProvider:
    """Skeleton. pip install openai, then implement complete()."""

    name = "openai"

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        raise NotImplementedError("OpenAI provider not implemented. See comments in source.")


class GoogleProvider:
    """Skeleton. pip install google-generativeai, then implement complete()."""

    name = "google"

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        raise NotImplementedError("Google provider not implemented. See comments in source.")


class BedrockProvider:
    """Skeleton. pip install boto3, then implement complete()."""

    name = "bedrock"

    def __init__(self, model: str = "anthropic.claude-sonnet-4-20250514-v1:0", region: str = "us-east-1"):
        self.model = model
        self.region = region

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        raise NotImplementedError("Bedrock provider not implemented. See comments in source.")


PROVIDERS = {
    "claude": AnthropicProvider,
    "openai": OpenAIProvider,
    "google": GoogleProvider,
    "bedrock": BedrockProvider,
}

CHEAP_MODELS = {
    "claude": "claude-haiku-4-5-20251001",
    "openai": "gpt-4o-mini",
    "google": "gemini-2.0-flash",
    "bedrock": "anthropic.claude-haiku-4-5-20251001-v1:0",
}

MODEL_COSTS = {
    "claude-sonnet-4-20250514": (0.003, 0.015),
    "claude-haiku-4-5-20251001": (0.0008, 0.004),
    "claude-opus-4-20250514": (0.015, 0.075),
    "gpt-4o": (0.0025, 0.010),
    "gpt-4o-mini": (0.00015, 0.0006),
    "o1": (0.015, 0.060),
    "gemini-2.5-flash": (0.00015, 0.0006),
    "gemini-2.5-pro": (0.00125, 0.010),
    "_default": (0.003, 0.015),
}

PIPELINES = {
    "light": {
        "name": "Light Pipeline (3 stages)",
        "stages": ["RCAR", "ToT", "PMR"],
        "use_when": "Moderate decisions where framing is clear",
    },
    "standard": {
        "name": "Standard Pipeline — FPR opener (5 stages)",
        "stages": ["FPR", "RCAR", "AdR", "ToT", "PMR"],
        "use_when": "Complex decisions with ambiguity or where the brief might be wrong",
    },
    "standard-cot": {
        "name": "Standard Pipeline — CoT opener (5 stages)",
        "stages": ["CoT", "RCAR", "AdR", "ToT", "PMR"],
        "use_when": "Complex decisions where facts need establishing first",
    },
    "stakeholder": {
        "name": "Multi-Stakeholder Pipeline (5 stages)",
        "stages": ["FPR", "SMR", "AdR", "ToT", "PMR"],
        "use_when": "Competing interests, power dynamics, multiple parties",
    },
    "systems": {
        "name": "Systems Pipeline (5 stages)",
        "stages": ["FPR", "RCAR", "GoT", "ToT", "PMR"],
        "use_when": "Feedback loops, interconnected components, emergent behavior",
    },
    "review": {
        "name": "Adversarial Review (3 stages)",
        "stages": ["AdR", "ToT", "PMR"],
        "use_when": "Reviewing an existing artifact (architecture, threat model, design)",
    },
}

FRAMEWORKS_PATH = Path(__file__).with_name("frameworks.json")


def load_frameworks(path: Path = FRAMEWORKS_PATH) -> dict:
    """Load framework prompts from JSON so prompt changes do not require code edits."""
    frameworks = json.loads(path.read_text())
    required_fields = {"name", "system", "prompt"}
    for key, value in frameworks.items():
        missing = required_fields - set(value)
        if missing:
            raise ValueError(f"Framework {key} is missing required fields: {sorted(missing)}")
    return frameworks


FRAMEWORKS = load_frameworks()


@dataclass
class StageResult:
    stage: str
    framework: str
    model: str
    raw: str
    parsed: Optional[dict] = None
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class PipelineResult:
    pipeline: str
    input_summary: str
    stages: list[StageResult] = field(default_factory=list)
    convergence: Optional[dict] = None
    total_duration_seconds: float = 0.0


def estimate_cost(pipeline_key: str, architect_model: str, challenger_model: str | None = None) -> dict:
    """Estimate token usage and cost for a pipeline run."""
    stages = PIPELINES[pipeline_key]["stages"]
    num_stages = len(stages)

    avg_input_per_stage = 800
    avg_output_per_stage = 1500
    context_growth = 1200

    total_input = 0
    total_output = 0
    for index in range(num_stages):
        stage_input = avg_input_per_stage + (context_growth * index)
        total_input += stage_input
        total_output += avg_output_per_stage

    total_input += num_stages * context_growth
    total_output += 1500

    architect_costs = MODEL_COSTS.get(architect_model, MODEL_COSTS["_default"])
    challenger_model = challenger_model or architect_model
    challenger_costs = MODEL_COSTS.get(challenger_model, MODEL_COSTS["_default"])

    has_challenger = "AdR" in stages and challenger_model != architect_model
    if has_challenger:
        architect_stages = num_stages
        challenger_stages = 1
        adversarial_index = stages.index("AdR")
        architect_input = total_input - avg_input_per_stage - (context_growth * adversarial_index)
        challenger_input = total_input - architect_input
        cost = (
            (architect_input / 1000 * architect_costs[0])
            + (total_output * (architect_stages / (num_stages + 1)) / 1000 * architect_costs[1])
            + (challenger_input / 1000 * challenger_costs[0])
            + (total_output * (challenger_stages / (num_stages + 1)) / 1000 * challenger_costs[1])
        )
    else:
        cost = (total_input / 1000 * architect_costs[0]) + (total_output / 1000 * architect_costs[1])

    return {
        "stages": num_stages + 1,
        "estimated_input_tokens": total_input,
        "estimated_output_tokens": total_output,
        "estimated_total_tokens": total_input + total_output,
        "estimated_cost_usd": round(cost, 4),
        "architect_model": architect_model,
        "challenger_model": challenger_model,
    }


def get_provider(name: str, model_override: str | None = None) -> Provider:
    if name not in PROVIDERS:
        print(f"Unknown provider: {name}. Available: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        sys.exit(1)
    provider_class = PROVIDERS[name]
    return provider_class(model=model_override) if model_override else provider_class()


def strip_fenced_code_block(text: str) -> str:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


def parse_json_response(raw: str) -> Optional[dict]:
    try:
        return json.loads(strip_fenced_code_block(raw))
    except json.JSONDecodeError:
        return None


def build_stage_input(accumulated_context: str, problem: str) -> str:
    return f"{accumulated_context}\n\n{problem}" if accumulated_context else problem


def build_stage_prompt(framework_key: str, full_input: str) -> str:
    return FRAMEWORKS[framework_key]["prompt"].replace("{input}", full_input)


def framework_temperature(framework_key: str) -> float:
    return 0.7 if framework_key == "AdR" else 0.3


def run_stage(provider: Provider, framework_key: str, accumulated_context: str, problem: str) -> StageResult:
    fw = FRAMEWORKS[framework_key]
    full_input = build_stage_input(accumulated_context, problem)
    prompt = build_stage_prompt(framework_key, full_input)

    start = time.time()
    try:
        raw = provider.complete(system=fw["system"], user=prompt, temperature=framework_temperature(framework_key))
        duration = time.time() - start
        parsed = parse_json_response(raw)
        return StageResult(
            stage=framework_key,
            framework=fw["name"],
            model=provider.name,
            raw=raw,
            parsed=parsed,
            duration_seconds=round(duration, 2),
        )
    except Exception as exc:
        return StageResult(
            stage=framework_key,
            framework=fw["name"],
            model=provider.name,
            raw="",
            duration_seconds=round(time.time() - start, 2),
            error=str(exc),
        )


def run_convergence(provider: Provider, stages: list[StageResult], problem: str) -> dict:
    findings = []
    for stage in stages:
        if stage.parsed:
            findings.append(f"## {stage.framework}\n{json.dumps(stage.parsed, indent=2)}")
        elif stage.raw:
            findings.append(f"## {stage.framework}\n{stage.raw}")

    system = (
        "You are a convergence analyst. Synthesize findings from multiple reasoning stages "
        "into a final recommendation. Focus on: genuine disagreements between stages, highest-risk items, "
        "and actionable next steps. Do not repeat analysis — synthesize it."
    )

    prompt = f"""Synthesize these findings into a final recommendation.

Respond in JSON:
{{
  "summary": "2-3 sentence executive summary",
  "key_findings": ["the 3-5 most important insights across all stages"],
  "disagreements": [
    {{"between": ["stage A", "stage B"], "about": "...", "recommendation": "..."}}
  ],
  "risks_ranked": [
    {{"risk": "...", "likelihood": "high|medium|low", "impact": "high|medium|low", "mitigation": "..."}}
  ],
  "recommended_action": "what to do next",
  "navigator_decisions_needed": ["decisions that require human judgment"]
}}

Original problem: {problem}

Stage findings:
{''.join(findings)}"""

    start = time.time()
    raw = provider.complete(system=system, user=prompt, temperature=0.3)
    duration = time.time() - start
    parsed = parse_json_response(raw)
    if parsed is not None:
        return {"result": parsed, "duration_seconds": round(duration, 2)}
    return {"raw": raw, "duration_seconds": round(duration, 2)}


def run_pipeline(
    pipeline_key: str,
    problem: str,
    architect: Provider,
    challenger: Optional[Provider] = None,
    convergence_provider: Optional[Provider] = None,
) -> PipelineResult:
    pipeline_def = PIPELINES[pipeline_key]
    result = PipelineResult(
        pipeline=pipeline_def["name"],
        input_summary=problem[:200] + "..." if len(problem) > 200 else problem,
    )

    start = time.time()
    accumulated = ""

    for index, stage_key in enumerate(pipeline_def["stages"]):
        provider = challenger if stage_key == "AdR" and challenger else architect
        print(
            f"  [{index + 1}/{len(pipeline_def['stages'])}] {FRAMEWORKS[stage_key]['name']} ({provider.name})...",
            file=sys.stderr,
        )
        stage_result = run_stage(provider, stage_key, accumulated, problem)
        result.stages.append(stage_result)

        if stage_result.error:
            print(f"  ERROR: {stage_result.error}", file=sys.stderr)
            continue

        if stage_result.parsed:
            accumulated += f"\n\n## {stage_result.framework} findings:\n{json.dumps(stage_result.parsed, indent=2)}"
        elif stage_result.raw:
            accumulated += f"\n\n## {stage_result.framework} findings:\n{stage_result.raw}"

    synth = convergence_provider or architect
    print(f"  [convergence] Synthesizing ({synth.name}: {synth.model})...", file=sys.stderr)
    result.convergence = run_convergence(synth, result.stages, problem)
    result.total_duration_seconds = round(time.time() - start, 2)
    return result


def run_review(
    artifact_path: str,
    architect: Provider,
    challenger: Optional[Provider] = None,
    convergence_provider: Optional[Provider] = None,
) -> PipelineResult:
    artifact = Path(artifact_path).read_text()
    problem = (
        "Review this artifact with an adversarial mandate. Find what is wrong, not whether it is good.\n\n"
        f"{artifact}"
    )
    return run_pipeline("review", problem, architect, challenger, convergence_provider)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Security-First Reasoning Pipeline CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    reason_parser = subparsers.add_parser("reason", help="Run a reasoning pipeline on a problem")
    reason_parser.add_argument("problem", nargs="?", help="Problem statement (or - for stdin)")
    reason_parser.add_argument("--pipeline", "-p", default="standard", choices=PIPELINES.keys())
    reason_parser.add_argument("--architect", "-a", default=os.environ.get("PIPELINE_ARCHITECT", "claude"))
    reason_parser.add_argument("--challenger", "-c", default=os.environ.get("PIPELINE_CHALLENGER", None))
    reason_parser.add_argument("--cheap", action="store_true", help="Use cheaper models for analysis, expensive only for convergence")
    reason_parser.add_argument("--yes", "-y", action="store_true", help="Skip cost confirmation")
    reason_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    review_parser = subparsers.add_parser("review", help="Adversarial review of an artifact file")
    review_parser.add_argument("file", help="Path to artifact (architecture.md, threat_model.md, etc.)")
    review_parser.add_argument("--architect", "-a", default=os.environ.get("PIPELINE_ARCHITECT", "claude"))
    review_parser.add_argument("--challenger", "-c", default=os.environ.get("PIPELINE_CHALLENGER", None))
    review_parser.add_argument("--cheap", action="store_true", help="Use cheaper models for analysis, expensive only for convergence")
    review_parser.add_argument("--yes", "-y", action="store_true", help="Skip cost confirmation")
    review_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    subparsers.add_parser("pipelines", help="List available pipeline variants")
    subparsers.add_parser("frameworks", help="List available reasoning frameworks")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "pipelines":
        for key, pipeline_def in PIPELINES.items():
            print(f"  {key:16s} {pipeline_def['name']}")
            print(f"  {'':16s} Stages: {' → '.join(pipeline_def['stages'])}")
            print(f"  {'':16s} Use when: {pipeline_def['use_when']}")
            print()
        return

    if args.command == "frameworks":
        for key, framework in FRAMEWORKS.items():
            print(f"  {key:5s} {framework['name']}")
        return

    cheap_mode = getattr(args, "cheap", False)
    skip_confirm = getattr(args, "yes", False)

    arch_model = CHEAP_MODELS.get(args.architect) if cheap_mode else None
    architect = get_provider(args.architect, model_override=arch_model)
    challenger = get_provider(args.challenger) if args.challenger else None
    convergence_provider = get_provider(args.architect) if cheap_mode else None

    if args.command == "review":
        if not Path(args.file).exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        pipeline_key = "review"
        est = estimate_cost(pipeline_key, architect.model, challenger.model if challenger else None)
        print(f"Adversarial review: {args.file}", file=sys.stderr)
        print(f"Architect: {architect.model}, Challenger: {(challenger.model if challenger else architect.model)}", file=sys.stderr)
        if cheap_mode:
            print(
                f"Cheap mode: analysis on {architect.model}, convergence on {convergence_provider.model}",
                file=sys.stderr,
            )
        print(f"Estimated: ~{est['estimated_total_tokens']:,} tokens, ~${est['estimated_cost_usd']:.4f}", file=sys.stderr)
        if not skip_confirm:
            confirm = input("Proceed? [Y/n] ").strip().lower()
            if confirm and confirm != "y":
                print("Aborted.", file=sys.stderr)
                sys.exit(0)
        result = run_review(args.file, architect, challenger, convergence_provider)
    else:
        problem = args.problem
        if problem == "-" or problem is None:
            print("Reading problem from stdin...", file=sys.stderr)
            problem = sys.stdin.read().strip()
        if not problem:
            print("No problem provided.", file=sys.stderr)
            sys.exit(1)

        pipeline_key = args.pipeline
        est = estimate_cost(pipeline_key, architect.model, challenger.model if challenger else None)
        print(f"Pipeline: {PIPELINES[pipeline_key]['name']}", file=sys.stderr)
        print(f"Architect: {architect.model}, Challenger: {(challenger.model if challenger else architect.model)}", file=sys.stderr)
        if cheap_mode:
            print(
                f"Cheap mode: analysis on {architect.model}, convergence on {convergence_provider.model}",
                file=sys.stderr,
            )
        print(f"Estimated: ~{est['estimated_total_tokens']:,} tokens, ~${est['estimated_cost_usd']:.4f}", file=sys.stderr)
        if not skip_confirm:
            confirm = input("Proceed? [Y/n] ").strip().lower()
            if confirm and confirm != "y":
                print("Aborted.", file=sys.stderr)
                sys.exit(0)
        result = run_pipeline(pipeline_key, problem, architect, challenger, convergence_provider)

    output = json.dumps(asdict(result), indent=2, default=str)
    if hasattr(args, "output") and args.output:
        Path(args.output).write_text(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
