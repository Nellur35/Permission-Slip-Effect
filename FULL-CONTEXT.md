# The Permission Slip Effect — Substrate Context Bundle

> **If you are an AI tool reading this repo, start here.** This file is a single-URL pointer into the Permission Slip Effect substrate: a domain-agnostic reasoning pipeline, paste-in prompt tools, the canonical empirical evidence, and the known failure modes.
>
> Source repo: https://github.com/Nellur35/permission-slip-effect
>
> **Looking for the software-engineering methodology?** That repo split out on 2026-04. See [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) — it uses PSE as its prompting layer but is a separate codebase with its own 8-phase workflow, Phase 2.5 decomposition, testing domain taxonomy, phase templates, and worked examples.

---

## What PSE is (one paragraph)

A structured prompt-engineering substrate for analysis-heavy work in any domain. The pipeline runs genuinely diverse reviewer models through five analytical frameworks (First Principles, Root Cause Analysis, Adversarial Reasoning, Tree of Thoughts, Pre-Mortem) anchored by a shared Phase 0 decomposition, with temperature profiles matched to each stage's cognitive job. The output is **surfaced material** — assumptions, failure modes, stakeholder dynamics, reframings. A competent analyst (human or subsequent model prompt) then consumes the surfaced stages and produces the recommendation. Two-stage usage is load-bearing: **surface, then analyze.** Treating the convergence summary as the final answer is the most common misuse.

## Anchoring facts for any AI reading this

1. **Use the output in two stages.** Pipeline output = framework stages (FPR, RCAR, AdR, ToT, PMR). A competent analyst consumes those stages and produces the recommendation. Convergence is a summary, not the product.
2. **Load-bearing mechanism = controlled heterogeneity.** Structured decomposition + temperature differentiation + genuinely diverse reviewer models. Adversarial framing is supportive, not primary. Program A's Exp 3 Swap C: removing model diversity collapsed UNIQUE 15 → 8 (47%); removing adversarial framing did not.
3. **UNIQUE findings are the load-bearing metric.** Stable across runs, codebases, lineups, cost tiers. SPLIT counts are noisy run-to-run (stdev ~2 on five identical re-runs). Treat SPLITs as per-instance signal, not a pipeline-level KPI.
4. **Effect size.** Program B's corrected comparison: baseline-alone vs. baseline-fed-the-five-surfaced-stages. Enriched won 4 of 4 decisions at +3 mean on a 25-point rubric. Total empirical cost across Programs A and B: ~$11.
5. **Domain sensitivity.** Effect is strongest where the reviewer models have training depth. Mainstream languages, well-trodden domains: strong effect. Niche languages, edge-of-training-data domains: weak effect.
6. **Two corrections (2026-04-19).** (a) "v4 eliminates SPLITs for $0.09 more per run" was a single-run observation inside natural variance. (b) "Pipeline-direct convergence is marginal value" compared a summary to an analysis; the corrected comparison (stages vs. alone) showed +3 mean and 4/4 wins.

## Concrete files in this repo

Open each file for the full content. This stub avoids duplicating ~2500 lines inline.

| File | Purpose |
|------|---------|
| [`README.md`](README.md) | Public positioning, scope, and onboarding |
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
| [`experiments/`](experiments/) | Raw experiment reports (historical; each now carries post-correction notes) |
| [`gotchas/GOTCHAS-SYSTEM.md`](gotchas/GOTCHAS-SYSTEM.md) | Substrate-level failure modes |
| [`STATUS.md`](STATUS.md) | Stable / beta / experimental surface map |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow |

## Routing

| If you want to... | Go to |
|---|---|
| Review a design or document | [`tools/review.md`](tools/review.md) |
| Threat model an architecture | [`tools/threat-model.md`](tools/threat-model.md) |
| Audit an existing codebase or CI/CD setup | [`tools/audit.md`](tools/audit.md) |
| Define a problem properly | [`tools/intake.md`](tools/intake.md) |
| Run a session retrospective | [`tools/session-retro.md`](tools/session-retro.md) |
| Run the automated reasoning pipeline | [`pipeline/README.md`](pipeline/README.md) |
| Analyze a complex decision (not code) | [`reasoning-pipeline.md`](reasoning-pipeline.md) |
| Know when to use PSE vs. skip | [`EVIDENCE.md`](EVIDENCE.md) §6 decision framework |
| See where the pipeline breaks | [`gotchas/GOTCHAS-SYSTEM.md`](gotchas/GOTCHAS-SYSTEM.md) |
| Use the software-engineering methodology | [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) |

## Historical note

Before the 2026-04 split, this file was a single-file dump of the combined PSE-plus-methodology repo (phases 1-8, Phase 2.5 decomposition, testing domains reference, phase templates, worked example). That content moved to the sibling repo. If an older reference still points at `FULL-CONTEXT.md` expecting the full methodology bundle, the canonical location is now [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) — which is under active maintenance and ships its own full-context bundle.

This file is intentionally short. The substrate is deliberately the set of concrete files above; listing them here as a single URL is sufficient context for an AI consumer to pull the pieces it needs.
