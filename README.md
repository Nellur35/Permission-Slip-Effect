# Permission Slip Effect

*A domain-agnostic, model-consumable prompt-engineering and reasoning substrate for surfacing assumptions, failure modes, hidden incentives, stakeholder dynamics, alternate framings, and uncomfortable possibilities — before a decision is made.*

`Permission-Slip-Effect` (PSE) is **standalone**. It is a structured **information-surfacing tool**, not a development methodology, not an agent harness, and not a decision tool. It is useful wherever ambiguity is the main cost: security review, architecture review, threat modeling, policy decisions, product strategy, HR / organizational decisions, legal-style analysis, clinical-style reasoning, incident analysis, ambiguous high-stakes decisions of any kind.

It is meant to be consumed by **both humans and AI tools.** A model can deep-read this repo, classify the task in front of it, and pick the smallest PSE tool or pipeline that preserves useful rigor — including picking *no PSE* when the task is simple.

---

## What PSE does (30-second version)

| Aspect | What to know |
|---|---|
| **What it is** | A method for surfacing assumptions, failure modes, hidden incentives, stakeholder dynamics, alternate framings, tradeoffs, and uncomfortable possibilities before a decision |
| **What it is not** | A full development methodology, an end-to-end agent harness, a replacement for human judgment, or a finished-answer generator |
| **When to use it** | Ambiguous, high-stakes, multi-stakeholder, low-reversibility, or hidden-incentive decisions |
| **When to skip it** | Simple factual questions, routine bounded tasks, low-risk reversible work, time-critical situations where structure adds overhead |
| **How the output is used** | **Two stages.** Surface material with PSE; then a competent analyst (human or model) consumes that material and produces the recommendation |

The pipeline is **optional**. Most useful PSE work happens by picking one paste-in prompt from [`tools/`](tools/) and reading the output. Full multi-stage pipeline runs are for the highest-ambiguity, highest-stakes subset.

---

## Routing: pick the smallest tool that fits the task

| Task type | Recommended PSE use |
|---|---|
| Simple factual question | **Skip PSE.** Direct prompt. |
| Routine, low-risk, bounded task | **Skip** or use one lightweight prompt from `tools/` |
| Architecture decision or review | [`tools/review.md`](tools/review.md), or the standard pipeline if stakes warrant |
| Threat model | [`tools/threat-model.md`](tools/threat-model.md); pipeline if high stakes |
| Existing codebase / CI/CD audit | [`tools/audit.md`](tools/audit.md) |
| Problem intake / definition | [`tools/intake.md`](tools/intake.md) |
| Session retrospective / incident analysis | [`tools/session-retro.md`](tools/session-retro.md) |
| Stakeholder-heavy decision | Multi-stakeholder pipeline (`pipeline/README.md`) |
| Systems / feedback-loop problem | Systems pipeline |
| Ambiguous, high-cost, low-reversibility decision | Standard pipeline → competent analyst synthesis |

A reader new to the repo should start with **one prompt file** in `tools/`. If that immediately sharpens the analysis, try the reasoning pipeline on a real high-stakes decision. The CLI is a reference implementation for repeatable, structured runs — not a polished platform.

---

## How to use the output (two-stage pattern)

PSE is a **surfacing tool, not a decision tool.** The right usage is two-stage:

1. **Surface.** Run the prompt or pipeline. The framework outputs (FPR, RCAR, AdR, ToT, PMR) produce raw assumptions, failure modes, stakeholder dynamics, reframings, and uncomfortable truths.
2. **Analyze.** Feed the surfaced material to a competent analyst — either yourself reading it directly, or a subsequent model prompt that takes the surfaced stages as enriched context and produces the recommendation.

The convergence stage inside the pipeline is a **summary / navigation aid** over the surfaced stages. Treating convergence output as the final answer is the single most common misuse of PSE.

## For AI agents reading this repo

You are not expected to run the full PSE pipeline for every task. First classify the user's task:

- simple factual question
- routine bounded task
- ambiguous decision
- architecture review
- threat model
- codebase / CI audit
- stakeholder-heavy decision
- incident analysis
- session retrospective
- problem intake

Then choose the **lightest PSE tool that preserves useful rigor**:

- **Use PSE** when ambiguity is the main cost.
- **Skip PSE** when the task is simple, factual, routine, low-risk, or already well-bounded.
- **Prefer a single `tools/` prompt** before reaching for the pipeline.
- **Use the full pipeline** only when stakes, ambiguity, and irreversibility justify the 3–5x token cost.

Always preserve the two-stage pattern:

1. surface assumptions, risks, tradeoffs, failure modes, and reframings
2. feed that surfaced material to a competent analyst — human or model — for the actual decision

Do **not**:

- treat the convergence summary as the final answer
- imply adversarial prompting alone is the mechanism (it is supportive, not primary)
- run the full pipeline by default
- call same-family or same-context reviewers a real independent council

For a deep-read entry point optimized for AI consumers, see [`FULL-CONTEXT.md`](FULL-CONTEXT.md).

---

## Why this exists

LLMs often stop at the first plausible, agreeable answer. That is fine for low-stakes tasks. It is dangerous for architecture, security, policy, clinical reasoning, and any decision where the cost of being wrong is high.

The load-bearing mechanism in PSE is **controlled heterogeneity**: structured decomposition, temperature differentiation per stage, and reviewer models from genuinely different training origins. Adversarial framing is supportive but not primary — Program A's mechanism-isolation test showed that removing model diversity collapses unique findings by 47% (15 → 8), while removing adversarial framing does not. See [`EVIDENCE.md`](EVIDENCE.md).

The repo packages this as portable paste-in prompts and a reference reasoning-pipeline CLI.

## What this repository is — and is not

| It is | It is not |
|---|---|
| A standalone reasoning / prompt-engineering substrate | A full development methodology |
| Domain-agnostic — useful across security, architecture, UX, HR, legal, clinical, policy, product, incidents | A software-engineering-only tool |
| Model-consumable as well as human-readable | A polished platform or finished product |
| A surfacing tool whose product is the surfaced stages | A decision tool whose product is the convergence summary |
| Practitioner-tested with calibrated empirical evidence | Peer-reviewed proof that one pipeline is optimal for every domain |

## Evidence (calibrated)

Two experimental programs (~$11 total, 30+ runs) stress-tested PSE's claims. Both corrected earlier overconfident claims. The corrected evidence supports a narrower, sharper thesis:

| Finding | Source |
|---|---|
| Pipeline + competent analyst wins 4/4 decisions, +3 mean on a 25-point rubric | Program B |
| Mechanism is model diversity under structure, not adversarial framing | Program A |
| Effect is domain-sensitive: strongest where models have training depth | Program A |
| Cross-domain generalization confirmed by adoption outside the security/coding domain | External validation (N=1, qualitative) |
| Original v4 "zero-SPLIT" claim was within natural variance — corrected | Program A |

PSE is not universally useful. The evidence is practitioner-level, not peer-reviewed proof. UNIQUE findings — not SPLIT counts — are the load-bearing metric.

Full empirical basis, corrections, and decision framework: [`EVIDENCE.md`](EVIDENCE.md). Raw experiment data: [`experiments/`](experiments/).

## Repository map

| Path | Purpose | Status |
|---|---|---|
| [`README.md`](README.md) | Standalone positioning, routing, and AI-agent entry point | Stable |
| [`START-HERE.md`](START-HERE.md) | Entry-point map for humans and AI agents | Stable |
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | Single-file deep-read for AI consumers | Stable |
| [`EVIDENCE.md`](EVIDENCE.md) | Canonical empirical evidence, corrected claims, decision framework | Stable |
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Long reference: frameworks, variants, selection logic, mechanism | Stable |
| [`tools/`](tools/) | Paste-in prompts (review, threat model, audit, intake, session retro) | Stable |
| [`pipeline/`](pipeline/) | Reference CLI for automated multi-stage runs | Beta |
| [`experiments/`](experiments/) | Raw experiment reports (with post-correction notes) | Experimental |
| [`gotchas/`](gotchas/) | Known failure modes of the substrate | Stable |
| [`STATUS.md`](STATUS.md) | Surface-area maturity map | Stable |

## Available pipeline variants

Optionality is the point. Choose the lightest layer that fits the task.

| Variant | Stages | Use when |
|---|---|---|
| No PSE | — | Simple factual, routine, low-risk, time-critical |
| Single `tools/` prompt | 1 paste-in | Most analytical work — start here |
| Light pipeline | RCAR → ToT → PMR | Moderate decisions, framing is clear |
| Standard pipeline (FPR opener) | FPR → RCAR → AdR → ToT → PMR | Complex decisions with ambiguity |
| Standard pipeline (CoT opener) | CoT → RCAR → AdR → ToT → PMR | Complex but framing is sound; facts need establishing |
| Multi-stakeholder pipeline | FPR → SMR → AdR → ToT → PMR | Competing interests, power dynamics |
| Systems pipeline | FPR → RCAR → GoT → ToT → PMR | Feedback loops, interconnected components |

You may also use the frameworks manually without the CLI — they are just sequenced prompts.

## Development and contribution

| File | Why it matters |
|---|---|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow and expectations |
| [`STATUS.md`](STATUS.md) | What is stable, beta, and experimental |
| [`pipeline/frameworks.json`](pipeline/frameworks.json) | External prompt catalog for the CLI |
| [`tests/test_pipeline.py`](tests/test_pipeline.py) | Baseline regression coverage for the reference CLI |

## Related work (optional ecosystem)

PSE is standalone. Other projects may use PSE-style structured surfacing as one technique inside a larger workflow:

- [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) — a separate, standalone AI-development methodology that may use PSE-style prompting where structured surfacing is useful.

These are ecosystem links, not dependencies. PSE does not require any of them and is not subordinate to any of them.

## Bottom line

If the problem is ambiguous and being wrong is expensive, PSE is likely worth the overhead — usually as a single prompt, occasionally as a full pipeline, always followed by a competent analyst step.

If the problem is routine, factual, or already well-bounded, skip it.

MIT · [Asaf Yashayev](https://github.com/Nellur35) · Security hobbyist
