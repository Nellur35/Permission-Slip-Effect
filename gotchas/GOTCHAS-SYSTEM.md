# Gotchas — System-Level

Known failure modes of the Permission Slip Effect substrate. These are where the substrate breaks — not where a single prompt produces bad output. The sibling [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) repo has its own methodology-level gotchas (multi-agent collisions, phase gate stalls, skill activation collisions, telemetry stalls); this file is scoped to the substrate itself.

---

## Treating the Convergence Summary as the Final Answer

**What happens:** The pipeline produces a `convergence` block alongside the five framework stage outputs. A user reads only the convergence summary, treats it as the recommendation, and skips the second stage of the two-stage usage pattern. The surfaced material — assumptions from FPR, failure modes from PMR, hidden incentives from AdR — never reaches the analyst who would have acted on it.

**When it hits:** Anywhere the pipeline's JSON output is summarized automatically, piped into a dashboard, or consumed by a user who expected "the answer." It is the single most common misuse of PSE.

**Why it happens:** Convergence looks like the summary of a long chain-of-thought and reads like a recommendation. It is not. It is a navigation aid over the five stages; the stages are the product.

**What to do:** For consequential decisions, always read (or feed a model) the `stages` array. If the consumer only needs a quick summary, use the pipeline-direct output fine — but do not compare it against a baseline analyst prompt and conclude "marginal value." That is the mis-specified comparison that motivated the 2026-04-19 correction. See [`../EVIDENCE.md`](../EVIDENCE.md) §3.

---

## Conflating SPLIT Count with Pipeline Quality

**What happens:** A navigator reads a single run's SPLIT count and concludes the pipeline is (or isn't) working. They retune parameters, swap models, or retire the pipeline based on one number that is largely noise.

**When it hits:** On any one-off v3-vs-v4-style comparison, on any "is my lineup any good?" check, on any CI gate that alerts on SPLIT counts.

**Why it happens:** SPLIT counts are intuitive ("the reviewers disagreed N times") and variable. Five identical re-runs of the same v4 configuration on the same artifact produced counts of 3, 6, 0, 4, 3. Mean 3.2, stdev ~2.17. A single "0" reads like success; the next run is a "6."

**What to do:** Use UNIQUE findings as the load-bearing metric. UNIQUE counts are stable across runs, codebases, lineups, and cost tiers (CV 21–42%). Treat SPLITs as per-instance signals worth investigating when they appear, not as pipeline-level KPIs. See EVIDENCE.md §2 and §5.

---

## Using the Pipeline on Domain-Unfamiliar Material

**What happens:** The pipeline is run on niche languages, unusual frameworks, or specialized technical domains the reviewer models have shallow training priors for. The reviewers converge on surface patterns, SPLITs collapse, UNIQUE findings shrink, and the pipeline's marginal value over single-model review drops.

**When it hits:** Uncommon languages, specialized scientific or regulatory domains, internal DSLs, bleeding-edge frameworks.

**Why it happens:** The effect is driven by controlled heterogeneity — diverse reviewer models exploring different analytical trajectories. Diversity needs depth to generate divergence. Where the models lack depth, they converge on what they can parse, which is surface structure.

**What to do:** Run the EVIDENCE.md §6 decision framework. If training depth is shallow, either inject domain expertise via context, skip the pipeline, or use a lighter variant. The pipeline is not a universal analytical amplifier; it is an amplifier for domains where the reviewers already know how to think.

---

## Sycophancy Under Pressure

**What happens:** When the navigator pushes back on a finding, the reviewer model softens subsequent output. This is the core problem the pipeline exists to mitigate — and it still reappears inside the pipeline's own outputs when pressure is applied hard enough.

**When it hits:** Iterative sessions where the navigator argues with reviewer findings, shared-context re-prompts that accumulate corrective pressure, convergence stages run on a model that has read the navigator's pushback.

**Why it happens:** RLHF still wins under direct pressure. Adversarial prompts and temperature profiles widen the distribution of surfacing, but they don't immunize the model against an insistent user.

**What to do:** Structural defenses beat behavioral ones. Run adversarial reviewers in a fresh context rather than inside the argument thread. Use the pipeline's multi-reviewer architecture: if three diverse reviewers surfaced the finding, the navigator's pushback on one doesn't quiet the rest. If the model starts agreeing with everything after a pushback, distrust the output, not trust it.

---

## Context Window Amnesia

**What happens:** Long sessions where early artifacts (problem statement, Phase 0 decomposition, initial constraints) fall out of the context window. Later stages optimize their analysis of accumulated analysis rather than the original problem. Drift goes undetected.

**When it hits:** Any session exceeding ~80K tokens. More common in CLI runs that pipe large inputs through all stages than in paste-in prompt use.

**Why it happens:** Models don't page — what's out of context is out of mind. The pipeline's residual injection (re-injecting Phase 0 output at every stage) is the designed mitigation, but it only works if the harness actually re-injects; many paste-in workflows don't.

**What to do:** Always re-include the Phase 0 decomposition (or the raw problem if Phase 0 wasn't run) as "PRIMARY INPUT" at every framework stage, distinct from the accumulated analysis. The pipeline CLI does this by default; manual pipelines must do it explicitly.

---

## Template Drift

**What happens:** Reviewers produce output that technically follows the framework template but fills it with generic content. A threat-model surfacing has all areas filled in, but half say "low risk — standard mitigations apply." A review has findings, but they're all Medium severity with vague impact.

**When it hits:** When the model is under context pressure, when the artifact is complex enough that genuine analysis is expensive, or when the model has already produced a similar artifact recently and is pattern-matching from its own prior output.

**Why it happens:** Filling the template is easier than surfacing the content. Models optimize for structural completion, which is easy to verify, rather than analytical depth, which isn't.

**What to do:** Run an adversarial review (`tools/review.md`) on the pipeline's output using a different model than the reviewers. A surfacing run that produced mostly "standard mitigations" on trust boundaries should fail that review. Do not let the same model that produced the artifact also validate it — the bootstrap-gap failure mode is that tools don't review themselves.
