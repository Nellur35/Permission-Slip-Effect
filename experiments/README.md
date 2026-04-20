# Experiments & Evidence

Empirical validation of the reasoning pipeline and the Permission Slip Effect.

> **Note on evidence hierarchy.** [`EVIDENCE.md`](../EVIDENCE.md) is canonical. It summarizes the combined findings of Programs A and B (~$11, 30+ runs) with the post-correction framing. The files in this directory are the raw experiment reports and predate parts of the correction. Where a statement in a file below contradicts EVIDENCE.md, EVIDENCE.md wins. Per-file post-correction notes flag the specific places this happens.

## Research Synthesis

**[research-synthesis.md](research-synthesis.md)** — What the data showed across an earlier round of experiments. Retained as historical record. **Post-correction note:** the "SPLIT is where the value lives" framing is superseded. UNIQUE findings are the load-bearing de-anchoring metric (stable across runs, codebases, lineups, cost tiers). SPLIT counts are noisy run-to-run — stdev ~2 across five identical re-runs of the same artifact. Treat SPLITs as per-instance signals, not a pipeline-level KPI. See EVIDENCE.md §2 and §5.

## Model Shootout

**[model-shootout.md](model-shootout.md)** — Multi-model benchmark on Amazon Bedrock showing that role-based model assignment produces balanced insight distribution vs. single-model dominance (13/1/1 → 3/2/2). **Post-correction note:** Program A's Exp 3 Swap C later confirmed model diversity as the load-bearing mechanism at the pipeline level (removing diversity collapsed UNIQUE 15 → 8, 47%). This upgrades the shootout's conclusion from "model diversity is a factor" to "model diversity is the primary mechanism."

## v3 vs v4 Pipeline A/B Comparison

**[v3-vs-v4-comparison.md](v3-vs-v4-comparison.md)** — A/B testing of v4 improvements against v3 baseline with full mechanism isolation. The interaction effect (Phase 0 + temperature profiles are necessary counterbalances) still stands. **Post-correction note at §0 of the file:** the original "zero SPLITs for $0.09 more per run" headline was a single-run observation inside natural variance (five identical re-runs produced 3, 6, 0, 4, 3). v4 reduces SPLIT variance and stabilizes UNIQUE findings — it does not eliminate SPLITs deterministically.

## v4 Pipeline Architecture

**[v4-architecture.md](v4-architecture.md)** — The v4 pipeline design: Phase 0 (structured decomposition), tiered parallel execution, residual injection, drift gates, per-stage temperature profiles, marginal value audit. Architecture unchanged. **Post-correction note:** the claimed effect is softened from "eliminates SPLITs" to "reduces SPLIT variance and stabilizes UNIQUE findings."

## LLM Principles Analysis

**[llm-principles-analysis.md](llm-principles-analysis.md)** — Graph of Thoughts analysis mapping 9 structural principles from LLM architecture onto the reasoning pipeline. The P1+P3+P4 convergence (input representation + residual connection + drift constraint are the same fix from three angles) still stands. **Post-correction note:** PSE is more accurately characterized as a **controlled-heterogeneity mechanism** (structured decomposition + temperature differentiation + diverse reviewer models) than as "adversarial framing exploiting thin alignment." Adversarial framing is supportive, not primary.

## Pipeline Validation

Cross-model testing (Sonnet 4.5 generation, Opus 4.6 evaluation) across three complexity levels showed that pipeline variants with Adversarial and Pre-Mortem stages consistently surface insights that baseline prompting ("think step by step") suppresses entirely. See [reasoning-pipeline.md](../reasoning-pipeline.md) for detailed results. EVIDENCE.md §3 (Program B, corrected test) quantifies the effect on end-user analysis: enriched baseline wins 4 of 4 decisions at +3 mean on a 25-point rubric.

## External Validation

Gemini Deep Research independently assessed the pipeline as:
- *"A robust mechanism for extracting 'System 2' performance from 'System 1' models"*
- *"Highly useful, specifically for 'Wicked Problems'"*
- *"Moderately novel — the specific integration constitutes a novel 'Cognitive Macro'"*

A practicing pharmacist with no security or software-engineering background adopted PSE prompts for drug-interaction analysis and patient-specific risk assessment and reported measurably shorter analysis work. N=1, qualitative — an existence proof that the mechanism generalizes outside its original context, not a replacement for controlled replication. See EVIDENCE.md §4.

## Run Your Own Tests

1. Pick a problem you've already solved (so you can evaluate quality).
2. Run Prompt A (baseline alone): `Think through this step by step and recommend what to do. Problem: [your problem]`
3. Run Prompt B (enriched baseline): run the standard pipeline from [reasoning-pipeline.md](../reasoning-pipeline.md), take the five surfaced framework stages (FPR, RCAR, AdR, ToT, PMR), then feed them to a competent analyst prompt along with the problem.
4. Compare: did the enriched version surface material the baseline missed? Did the analyst's recommendation change?

The Program B comparison is baseline-alone vs. baseline fed the surfaced stages — not pipeline-convergence vs. baseline. Comparing convergence to baseline is what the original mis-specified test did.

If you run experiments, consider opening a PR with results.
