# Contributing to `Permission-Slip-Effect`

Thank you for your interest in contributing.

This repository has multiple layers, but they do **not** all have the same stability level or contribution standard. Before changing anything, read [`README.md`](README.md) and [`STATUS.md`](STATUS.md) so you know which surfaces are stable, which are beta, and which are intentionally experimental.

## Contribution philosophy

The project is opinionated on purpose. The goal is not to collect every interesting idea about LLM prompting. The goal is to preserve a **coherent operating model** for adversarial review, structured reasoning, and security-conscious AI-assisted engineering.

That means good contributions usually make the repository more:

| Better in this way | What that usually looks like |
|------|------|
| Clear | Simpler onboarding, better boundaries, less ambiguity |
| Trustworthy | Tests, examples, reproducible behavior, clearer status labels |
| Useful | Better prompts, stronger examples, safer defaults |
| Durable | Refactors that reduce hidden coupling and make future changes easier |

Good contributions do **not** usually look like adding more conceptual sprawl, widening claims without evidence, or introducing new abstractions before the current ones are reliable.

## What is core vs. experimental

The repository is divided into different stability zones.

| Surface | Current expectation |
|------|------|
| `tools/` | Stable and usability-focused |
| `methodology/` | Stable and editorially curated |
| `pipeline/` | Beta reference implementation |
| `examples/` | Beta, used to show target output shape |
| `experiments/`, `integrations/`, `multi-agent/` | Experimental and more open to iteration |

If you are unsure whether a change belongs in the stable or experimental surface, prefer the experimental side first.

## What kinds of contributions are most welcome

| Type | Examples |
|------|------|
| Documentation clarity | README improvements, onboarding simplification, status labeling |
| Prompt quality | Sharper prompt wording, better output schema, lower ambiguity |
| CLI reliability | Tests, parsing hardening, provider boundaries, deterministic helpers |
| Examples | Realistic input artifacts, expected-output fixtures, worked walkthroughs |
| Evaluation discipline | Better benchmark protocol, clearer scoring rubric, reproducibility improvements |

## Evidence expectations

The repository makes practical claims. Those claims should stay calibrated.

| If you are changing... | Provide... |
|------|------|
| Prompt wording | A concrete before/after example |
| Pipeline behavior | A fixture, expected output, or regression test |
| README positioning | Clearer wording and a reason it reduces confusion |
| Performance or quality claims | A reproducible note, benchmark, or explicit limitation |
| Theoretical claims | Strong caveats unless there is broad evidence |

Please separate **observed behavior**, **working hypotheses**, and **speculation**. Mixing those together makes the project harder to trust.

## Prompt and framework changes

The reasoning prompt catalog now lives in [`pipeline/frameworks.json`](pipeline/frameworks.json). If you want to add or change a framework, keep these rules in mind.

| Rule | Why |
|------|------|
| Preserve JSON-oriented output shapes | The CLI and examples depend on structured output |
| Keep the framework purpose distinct | Overlapping stages reduce signal |
| Prefer clarity over cleverness | Contributors need to understand why the prompt exists |
| Add or update tests when behavior changes | The reference CLI should not drift silently |

## Running tests

From the repository root:

```bash
python -m pytest
```

If you do not have pytest installed yet:

```bash
pip install -e .[dev]
python -m pytest
```

The test suite currently focuses on the reference CLI: framework loading, JSON parsing, cost estimation, and orchestration behavior.

## Pull request checklist

Before opening a PR, make sure you can say yes to these questions.

| Question | Required |
|------|------|
| Does this change fit the repository’s scope? | Yes |
| Is the target surface stable, beta, or experimental, and did I treat it accordingly? | Yes |
| Did I avoid broadening claims beyond the evidence? | Yes |
| Did I add or update tests, fixtures, or examples where relevant? | Yes |
| Did I improve clarity, trust, or utility rather than just adding more material? | Yes |

## Style notes

Use clear Markdown, direct language, and explicit caveats where needed. Favor practical examples over abstract slogans. For code, prefer small deterministic helpers and simple interfaces over hidden magic.

## If you want to propose something large

For major changes, open an issue first and answer these questions:

1. What problem does the change solve?
2. Which repository surface does it affect?
3. Why does it belong in the core project rather than the experimental edge?
4. How would we know the change made the project better?

That keeps the project coherent while still allowing it to evolve.
