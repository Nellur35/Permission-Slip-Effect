# The Permission Slip Effect — AI-Consumer Context Bundle

> **If you are an AI tool reading this repo on a user's behalf, start here.** This file is a single-URL pointer into the Permission Slip Effect (PSE) substrate: a standalone, domain-agnostic reasoning / prompt-engineering / information-surfacing repo with paste-in prompt tools, a reference reasoning-pipeline CLI, canonical empirical evidence, and known failure modes.
>
> Source repo: https://github.com/Nellur35/permission-slip-effect

---

## What PSE is (one paragraph)

PSE is a **standalone, domain-agnostic prompt-engineering and reasoning substrate** for surfacing the assumptions, failure modes, hidden incentives, stakeholder dynamics, alternate framings, tradeoffs, and uncomfortable possibilities a single direct prompt would skip past. The pipeline runs genuinely diverse reviewer models through five analytical frameworks (First Principles, Root Cause Analysis, Adversarial Reasoning, Tree of Thoughts, Pre-Mortem) anchored by a shared Phase 0 decomposition, with temperature profiles matched to each stage's cognitive job. The output is **surfaced material**. A competent analyst (human or subsequent model prompt) then consumes the surfaced stages and produces the recommendation. Two-stage usage is load-bearing: **surface, then analyze.** Treating the convergence summary as the final answer is the most common misuse.

PSE is **not** a software-development methodology, **not** an end-to-end agent harness, and **not** a replacement for human judgment. It is a structured surfacing tool. Other projects (development methodologies, executable harnesses, domain workflows) may incorporate PSE-style prompting as one technique — but PSE stands on its own and is consumable independently.

## Where PSE is useful

Domain-agnostic. Useful wherever ambiguity is the main cost:

- security review
- architecture review
- threat modeling
- policy decisions
- product strategy
- HR / organizational decisions
- legal-style analysis
- clinical-style reasoning
- incident analysis
- session retrospectives
- any ambiguous high-stakes decision where being wrong is expensive

> **Not professional advice.** PSE can support legal-style or clinical-style reasoning by surfacing assumptions, failure modes, and alternate framings — but its output is not legal, medical, or other professional advice, and is not a substitute for a qualified human professional. Treat it as input to a competent analyst, not a verdict.

## How an AI agent should consume this repo

You do not need to run the full PSE pipeline for every task. Read this file, then route the user's request through the steps below.

### Step 1 — Classify the task

Pick the closest match:

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

### Step 2 — Choose the smallest PSE tool that preserves useful rigor

| Task type | Recommended PSE use |
|---|---|
| Simple factual question | **Skip PSE.** Direct prompt. |
| Routine, low-risk, bounded task | **Skip** or use one lightweight prompt from `tools/` |
| Architecture review or decision | [`tools/review.md`](tools/review.md), or standard pipeline if stakes warrant |
| Threat model | [`tools/threat-model.md`](tools/threat-model.md); pipeline if high stakes |
| Codebase / CI audit | [`tools/audit.md`](tools/audit.md) |
| Problem intake / definition | [`tools/intake.md`](tools/intake.md) |
| Session retrospective / incident analysis | [`tools/session-retro.md`](tools/session-retro.md) |
| Stakeholder-heavy decision | Multi-stakeholder pipeline (`pipeline/README.md`) |
| Systems / feedback-loop problem | Systems pipeline |
| Ambiguous, high-cost, low-reversibility decision | Standard pipeline → analyst synthesis |

### Step 3 — Two-stage the output, always

1. **Surface.** Run the chosen tool or pipeline. Capture the framework stage outputs (FPR, RCAR, AdR, ToT, PMR or whichever subset applies).
2. **Analyze.** Feed those surfaced stages to a competent analyst — you reading them directly, or a subsequent model prompt that takes them as enriched context — and produce the recommendation.

The pipeline's `convergence` block is a summary / navigation aid over the surfaced stages. It is not the product.

### Hard rules for AI consumers

- **Do not** run the full pipeline by default. Pick the smallest fit.
- **Do not** treat the convergence summary as the final answer.
- **Do not** imply adversarial prompting alone is the mechanism. Controlled heterogeneity (decomposition + temperature + diverse models) is primary; adversarial framing is supportive.
- **Do not** use PSE on tasks where it would only add friction (simple, factual, routine, low-risk, well-bounded, time-critical).

A council of same-family or zero-context local agents can still work — it will be less effective than a cross-family panel (reviewer diversity is load-bearing), but it's a legitimate option when diverse models aren't available.

## Anchoring facts (calibrated, from EVIDENCE.md)

1. **Use the output in two stages.** Pipeline output = framework stages (FPR, RCAR, AdR, ToT, PMR). A competent analyst consumes those stages and produces the recommendation. Convergence is a summary, not the product.
2. **Load-bearing mechanism = controlled heterogeneity.** Structured decomposition + per-stage temperature differentiation + genuinely diverse reviewer models. Adversarial framing is supportive, not primary. Program A's Exp 3 Swap C: removing model diversity collapsed UNIQUE 15 → 8 (47%); removing adversarial framing did not.
3. **UNIQUE findings are the load-bearing metric.** Stable across runs, codebases, lineups, cost tiers. SPLIT counts are noisy run-to-run (stdev ~2 on five identical re-runs). Treat SPLITs as per-instance signal, not a pipeline-level KPI.
4. **Effect size.** Program B's corrected comparison: baseline-alone vs. baseline-fed-the-five-surfaced-stages. Enriched won 4 of 4 decisions at +3 mean on a 25-point rubric. Total empirical cost across Programs A and B: ~$11.
5. **Domain sensitivity.** Effect is strongest where the reviewer models have training depth. Mainstream languages, well-trodden domains: strong effect. Niche languages, edge-of-training-data domains: weak effect.
6. **Two corrections (2026-04-19).** (a) "v4 eliminates SPLITs for $0.09 more per run" was a single-run observation inside natural variance. (b) "Pipeline-direct convergence is marginal value" compared a summary to an analysis; the corrected comparison (stages vs. alone) showed +3 mean and 4/4 wins.
7. **PSE is not universally useful.** The evidence is practitioner-level, not peer-reviewed proof. Skip PSE when the task is simple, factual, routine, low-risk, well-bounded, or time-critical.

## Concrete files in this repo

Open each file for the full content. This stub does not duplicate the body of the substrate inline.

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Standalone positioning, task routing, AI-agent entry point |
| [`START-HERE.md`](START-HERE.md) | Entry-point map for both humans and AI agents |
| [`EVIDENCE.md`](EVIDENCE.md) | **Canonical.** Programs A and B, decision framework, corrections. If any other file contradicts this one, this one wins. |
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Long reference: frameworks, variants, selection logic, two-stage usage pattern, mechanism |
| [`pipeline/README.md`](pipeline/README.md) | Reference CLI — automated multi-model pipeline runs |
| [`pipeline/pipeline.py`](pipeline/pipeline.py) | CLI implementation |
| [`pipeline/frameworks.json`](pipeline/frameworks.json) | External prompt catalog for the CLI |
| [`tools/review.md`](tools/review.md) | Paste-in adversarial review prompt |
| [`tools/threat-model.md`](tools/threat-model.md) | Paste-in threat-modeling surfacing prompt |
| [`tools/audit.md`](tools/audit.md) | Paste-in codebase / CI-CD scan prompt |
| [`tools/intake.md`](tools/intake.md) | Paste-in problem-definition questionnaire |
| [`tools/session-retro.md`](tools/session-retro.md) | Paste-in session retrospective prompt |
| [`experiments/`](experiments/) | Raw experiment reports (historical; each carries post-correction notes) |
| [`gotchas/GOTCHAS-SYSTEM.md`](gotchas/GOTCHAS-SYSTEM.md) | Substrate-level failure modes |
| [`STATUS.md`](STATUS.md) | Stable / beta / experimental surface map |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow |

## Routing reference

| If you want to... | Go to |
|---|---|
| Decide whether to use PSE at all | [`EVIDENCE.md`](EVIDENCE.md) §6 decision framework |
| Review a design or document | [`tools/review.md`](tools/review.md) |
| Threat model an architecture | [`tools/threat-model.md`](tools/threat-model.md) |
| Audit an existing codebase or CI/CD setup | [`tools/audit.md`](tools/audit.md) |
| Define a problem properly | [`tools/intake.md`](tools/intake.md) |
| Run a session retrospective or incident analysis | [`tools/session-retro.md`](tools/session-retro.md) |
| Run the automated reasoning pipeline | [`pipeline/README.md`](pipeline/README.md) |
| Analyze a complex non-code decision | [`reasoning-pipeline.md`](reasoning-pipeline.md) |
| See where the substrate breaks | [`gotchas/GOTCHAS-SYSTEM.md`](gotchas/GOTCHAS-SYSTEM.md) |

## Related work (optional ecosystem)

PSE is standalone and does not require any external project to be useful. Other repos may borrow PSE-style structured surfacing as one technique inside a larger workflow — for example, an AI development methodology, or an executable harness experiment. Those are independent projects with their own identities and are out of scope here. PSE is not subordinate to any of them.

This file is intentionally short. The substrate is deliberately the set of concrete files above; listing them here as a single URL is sufficient context for an AI consumer to pull the pieces it needs.
