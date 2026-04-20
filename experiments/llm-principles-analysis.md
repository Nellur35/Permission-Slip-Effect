# LLM Architecture Principles Applied to the Reasoning Pipeline

*Using Graph of Thoughts to map how LLMs are built onto how the pipeline works — finding gaps, validating strengths, and designing v4.*

---

> **Post-correction note (2026-04-19).** The nine principles and the P1+P3+P4 convergence (input representation + residual connection + drift constraint are the same fix from three angles) still stand. The **P8 framing is superseded**: PSE is more accurately described as a **controlled-heterogeneity mechanism** (structured decomposition + temperature differentiation + genuinely diverse reviewer models from different training origins) than as "adversarial framing exploiting a thin RLHF alignment layer." Program A's Exp 3 Swap C removed model diversity while preserving adversarial framing and the effect collapsed (UNIQUE 15 → 8). Removing adversarial framing (Exp 6) did not. Adversarial framing is supportive; model diversity is primary. See [`../EVIDENCE.md`](../EVIDENCE.md) §2.

---

## Method

Nine structural principles extracted from LLM architecture, each mapped onto the reasoning pipeline to find where the same principle validates or exposes a gap.

This is not metaphor. LLM architecture and the reasoning pipeline are both information processing systems that transform inputs through staged computation. Principles that govern one should apply to the other.

---

## The Nine Principles

| # | Principle | In LLMs | Abstract Form |
|---|-----------|---------|---------------|
| P1 | Representation Determines Processing | Tokenization defines what the model sees. Poor tokenization = poor everything downstream. | How you encode the input constrains everything downstream. |
| P2 | Parallel Multi-Perspective Extraction | Multi-head attention runs parallel projections, each extracting different signals, then combines. | Multiple simultaneous views of the same input outperform sequential single-view processing. |
| P3 | Residual Information Preservation | Residual connections keep the original signal available at every layer. | In staged processing, the original input must remain accessible at every stage. |
| P4 | Drift Constraint (KL Penalty) | RLHF uses KL divergence to prevent the policy from diverging too far from reference. | Optimization needs an anchor. Without drift constraints, staged refinement diverges from the objective. |
| P5 | Proxy Objective Gaming | Reward hacking — the model optimizes the reward model's score, not actual quality. | Components optimizing local objectives can satisfy local criteria while missing the global goal. |
| P6 | Compute-Proportional Scaling | Chinchilla scaling laws — optimal performance requires proportional data and parameters. | Processing intensity should match problem complexity. Over-processing degrades output. |
| P7 | Sampling Strategy Shapes Output | Temperature, top-k, top-p dramatically change generation behavior. | Same architecture, different parameters = different outputs. |
| P8 | Alignment Is a Thin Behavioral Layer | RLHF/DPO create a shallow coating. A few hundred fine-tuning examples can strip it. | Behavioral constraints on top of a capable system are inherently fragile. |
| P9 | Emergent Capability from Scale | Reasoning and metacognition emerge without explicit training. | Complex capabilities emerge from simple rules at scale. Premature structure prevents emergence. |

---

## Mapping Results

### P1: No Tokenizer → Add Phase 0

**Gap:** The pipeline feeds raw free-text directly to the first framework. Every downstream stage is bounded by how well that input represents the problem.

**Fix:** Phase 0 — structured decomposition before any framework runs. Observable facts, constraints, stakeholders, desired outcome, known unknowns, complexity score. This is the pipeline's tokenizer.

### P2: Sequential When It Should Be Parallel → Tiered Execution

**Gap:** Frameworks run sequentially — each sees accumulated output of all previous stages. By stage 5, the model is analyzing interpretations of interpretations, not the original problem. CoT's framing infects everything downstream.

**Fix:** Frameworks within a tier run in parallel on the same input, then merge. Different perspectives extracted independently, combined after.

### P3: No Residual Connection → Re-inject Phase 0

**Gap:** The original problem gets buried under accumulated analysis. Later stages optimize their analysis of the analysis rather than analyzing the problem.

**Fix:** Phase 0 output explicitly re-injected at every stage as PRIMARY INPUT, distinct from accumulated CONTEXT.

### P4: No Drift Constraint → Relevance Gates

**Gap:** No mechanism to detect that stage 6 is producing beautiful analysis disconnected from the actual question.

**Fix:** Brief relevance check between tiers. "Rate 1-10 how directly this addresses the original problem." The pipeline's KL penalty.

### P5: Proxy Objective Gaming → Marginal Value Audit

**Gap:** Each framework justifies its own existence. FPR finds first principles even when unnecessary. AdR finds adversarial dynamics even in collaborative situations.

**Fix:** At synthesis, ask which stages actually changed the recommendation. Stages that produced no unique signal get flagged. Over time this builds data for principled framework pruning.

### P6: Domain-Based Sizing → Complexity-Proportional

**Gap:** Pipeline variants selected by problem domain, not complexity. A complex interpersonal problem might need the full pipeline while a simple strategic decision needs 3 stages.

**Fix:** Complexity scoring in Phase 0 routes to appropriate pipeline depth.

### P7: Uniform Temperature → Per-Stage Profiles

**Gap:** All stages use the same inference parameters despite fundamentally different cognitive requirements.

**Fix:** Analytical stages at 0.2, diagnostic at 0.3-0.4, Permission Slip stages at 0.7, synthesis at 0.1.

### P8: Permission Slip Effect — VALIDATED, mechanism corrected

**No gap in the effect itself**; this remains the pipeline's strongest validated insight. The corrected mechanism framing is **controlled heterogeneity** rather than "adversarial framing exploiting the thin alignment layer":

- Structured decomposition (Phase 0) standardizes how every reviewer interprets the raw input.
- Per-stage temperature profiles open the output distribution where diversity matters and tighten it where determinism matters.
- Genuinely diverse reviewer models from different training origins produce different analytical trajectories — this is the load-bearing driver.

Adversarial framing (AdR, PMR) is supportive: it gives those diverse models specific failure-oriented contexts to explore. The older "RLHF alignment bypass" theory captured the role of high-temperature adversarial stages but overweighted it. Program A's mechanism-isolation tests (Exp 3 Swap C, Exp 6) confirm the re-weighting empirically: removing diversity collapses UNIQUE 47% (15 → 8); removing adversarial framing does not.

**Enhancement (unchanged):** document WHY it works at the architectural level. The updated story: staged computation across genuinely distinct reasoners, anchored by shared decomposition, with adversarial prompts providing the specific prompts where diverse reasoners produce the most actionable divergence.

### P9: Emergence Thresholds — Minor Gap

The multi-agent architecture correctly embraces emergence. Minor gap: the threshold for role identification (15-30 log entries) is heuristic rather than principled. Need observable signals: concern appearing in 25%+ of entries, recurring cross-reference patterns, navigator time concentration exceeding 30%.

---

## Key Convergence

The Graph of Thoughts structure surfaced something a linear analysis would miss: **P1 + P3 + P4 are the same fix from three angles.**

- P1 creates the structured representation (Phase 0)
- P3 ensures it persists at every stage (residual injection)
- P4 measures whether analysis is still responsive to it (drift gates)

Implement Phase 0, and the other two become trivial additions. Three "separate" gaps, one implementation sprint.

---

## What This Means for the Pipeline

The pipeline is architecturally sound but under-constrained. The sequential chaining, the Permission Slip Effect, the tiered agent model — all correct decisions. What was missing were the constraints and feedback mechanisms that prevent the architecture from degrading at scale: input representation, drift prevention, value measurement, and parameter tuning.

These are the same mechanisms that took LLMs from "technically capable" to "reliably useful." The pipeline needed the same evolution.

---

*This analysis used Graph of Thoughts to analyze the reasoning pipeline — the methodology analyzing itself. The convergence map (P1+P3+P4 being one fix) is the most valuable output and wouldn't exist from a linear review. That's GoT working as designed.*
