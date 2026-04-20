# Reasoning Pipeline for Complex Decisions

*When a model fills ambiguity with statistically plausible but wrong answers, structured reasoning forces it past the first plausible output.*

---

## Why This Exists

Models optimize for "plausible response" -- not "thorough response." They stop at the first reasonable answer. This is called **satisficing**. A single reasoning mode cannot cover the full problem space of a complex decision. The solution is to chain multiple reasoning frameworks into a pipeline where each stage analyzes the problem from a different angle, and the output of each stage informs the next.

## How to use the output: two-stage pattern

This is the single most important property of the pipeline.

**PSE is a surfacing tool, not a decision tool.** The product of a pipeline run is the raw material inside the five framework stages — assumptions, failure modes, stakeholder dynamics, reframings, uncomfortable truths. That material is then consumed by a competent analyst (the navigator, or a subsequent model prompt) who produces the recommendation.

```
Stage 1 — Surface:  Raw problem → Pipeline → 5 framework stages (FPR, RCAR, AdR, ToT, PMR)
Stage 2 — Analyze:  Competent analyst prompt + 5 surfaced stages → Recommendation
```

The convergence stage inside the pipeline is a **summary / navigation aid** over the five stages. It is not the product. Treating convergence output as the final answer is the single most common misuse of PSE. Program B's corrected test compared *baseline alone* to *baseline fed the five surfaced stages* — enriched won 4 of 4 decisions at +3 mean on a 25-point rubric. See [`EVIDENCE.md`](EVIDENCE.md) §3.

## The Permission Slip Effect (what the name means)

The name comes from an observation: structured stages like Pre-Mortem ("assume this failed -- why?") and Adversarial Reasoning ("what is each party secretly protecting?") give the model contexts where the expected output is analysis of failure modes and hidden incentives rather than an agreeable summary. In cross-model testing, insights like "the mandate itself is contradictory," "the VP ego is driving this decision," and "maybe this platform should not exist at all" appeared in pipeline variants with Adversarial or Pre-Mortem stages but not in the "think step by step" baseline.

That observation is real. It is also only part of the story. The load-bearing driver is **controlled heterogeneity**:

- **Structured decomposition** (Phase 0) — shared interpretation of the input before any framework runs.
- **Temperature differentiation per stage** — opens or tightens the output distribution to match the cognitive job.
- **Genuinely diverse reviewer models from different training origins** — the primary driver.

Program A's mechanism-isolation tests (Exp 3 Swap C and Exp 6) removed these one at a time. Removing adversarial framing preserved the effect. Removing model diversity collapsed UNIQUE findings from 15 to 8, a 47% drop. Adversarial framing is **supportive, not primary**.

The pipeline does not make the model smarter. It widens the set of analytical trajectories that get explored and hands the union to an analyst who decides.

---

## Available Frameworks

| Framework | Abbreviation | What It Does | Use When |
|-----------|-------------|-------------|----------|
| **First Principles** | FPR | Validates assumptions, checks if the framing is correct | The brief might be flawed; something feels off; ambiguous problem |
| **Chain of Thought** | CoT | Establishes facts, timeline, sequential logic | You need to understand what actually happened |
| **Root Cause Analysis** | RCAR / 5 Whys | Finds structural causes, not symptoms | Surface solutions keep failing; recurring problems |
| **Graph of Thoughts** | GoT | Maps systemic interconnections and feedback loops | Multiple interconnected elements; situation is stuck |
| **Stakeholder Mapping** | SMR | Maps power and interest for each player | Competing interests; multiple parties optimizing for different outcomes |
| **Adversarial Reasoning** | AdR | Models what each party is protecting and optimizing for | Conflict, resistance, hidden incentives |
| **Tree of Thoughts** | ToT | Generates and compares multiple strategic options with tradeoffs | Designing interventions; high-stakes decisions with multiple paths |
| **Pre-Mortem** | PMR | Assumes failure, works backward to identify why | Before committing to any major strategy |

### Research Basis

The individual frameworks have independent research backing:

- **Chain of Thought** -- Wei et al., Google Brain, 2022. Demonstrated significant improvements on reasoning tasks, varying widely by task type and model scale. Only effective at large scale (100B+ parameters). (arXiv:2201.11903)
- **Tree of Thoughts** -- Yao et al., Princeton, 2023. Outperforms CoT on tasks requiring deliberate planning and search. (arXiv:2305.10601)
- **Graph of Thoughts** -- Besta et al., ETH Zurich, 2023. Outperforms ToT on tasks requiring decomposition and recombination of partial results. (arXiv:2308.09687)
- **Pre-Mortem** -- Gary Klein, 2007 (HBR). Based on prospective hindsight research by Mitchell, Russo & Pennington, 1989, which found that imagining an event has already occurred increases ability to identify reasons for outcomes by 30%.
- **Root Cause Analysis / 5 Whys** -- Toyota Production System, 1950s. Established method for distinguishing symptoms from structural causes.
- **Stakeholder Mapping** -- Mendelow, 1981 (ICIS proceedings). Power-interest grid for organizational analysis.

**What is novel here** is the integration of these frameworks into sequenced pipelines, the selection logic for choosing which to apply, and the permission slip finding. The pipeline architecture is practitioner-tested, not peer-reviewed.

---

## Pipeline Variants

### Light Pipeline (3 stages)

For moderate-complexity decisions where the framing is clear but you need structured analysis.

```
RCAR -> ToT -> PMR
```

What this gives you: Root cause identification, structured option comparison with tradeoffs, and specific failure modes to design against.

### Standard Pipeline (5 stages) -- First Principles opener

For complex decisions, especially those with ambiguity, competing stakeholders, or where the brief itself might be flawed.

```
FPR -> RCAR -> AdR -> ToT -> PMR
```

What this gives you: Everything in Light, plus assumption validation at the start and stakeholder incentive mapping before options are generated.

### Standard Pipeline (5 stages) -- CoT opener

For complex decisions where the facts need to be established before analysis. Use this when you know the framing is sound but the situation is complicated.

```
CoT -> RCAR -> AdR -> ToT -> PMR
```

### Multi-Stakeholder Pipeline (5 stages)

For decisions with competing interests, power dynamics, or multiple parties optimizing for different outcomes — organizational, commercial, cross-team, or political.

```
FPR -> SMR -> AdR -> ToT -> PMR
```

### Systems Pipeline (5 stages)

For problems with feedback loops, interconnected components, and emergent behavior.

```
FPR -> RCAR -> GoT -> ToT -> PMR
```

---

## When to Use Which

```
Simple, well-defined problem    -> No pipeline. Direct prompt.
Moderate, familiar problem      -> Light (3 stages)
Complex, multi-angle            -> Standard (5 stages)
High-stakes, multi-stakeholder    -> Multi-Stakeholder or full custom (5-7 stages)
```

### Selection Logic

Start with these questions:

1. **Is the brief itself potentially flawed?** Start with First Principles.
2. **Do you need to establish what happened?** Add Chain of Thought.
3. **Are surface solutions failing?** Add Root Cause (5 Whys).
4. **Multiple interconnected elements?** Add Graph of Thoughts.
5. **Multiple parties with competing interests?** Add Stakeholder Mapping + Adversarial.
6. **Hidden incentives or conflict?** Add Adversarial Reasoning.
7. **Multiple possible approaches?** Add Tree of Thoughts.
8. **High stakes?** Add Pre-Mortem. (Always recommended.)

---

## First Principles vs Chain of Thought as Opener

Testing showed that **First Principles is the stronger opener for ambiguous or multi-stakeholder problems** -- it catches flawed premises before you invest in detailed analysis.

However, this is not universal. CoT as opener occasionally generates unique tactical solutions that FPR misses, because establishing the full fact pattern sometimes reveals options that assumption-checking does not.

**Rule of thumb:** If the problem statement might be wrong, start with FPR. If the problem statement is solid but the situation is complex, start with CoT.

---

## How to Apply

Two modes:

**Mode 1 -- In your own thinking.** Run the pipeline yourself before prompting. Frame the problem clearly, then give the model a well-structured question instead of a raw one.

**Mode 2 -- In the prompt itself.** Ask the model to work through each stage explicitly:

```
Walk me through this problem in stages:

1. FIRST PRINCIPLES: What assumptions am I making? Are they valid?
2. ROOT CAUSE (5 Whys): What is actually causing this?
3. ADVERSARIAL: What is each party protecting? What would shift them?
4. OPTIONS (Tree of Thoughts): Generate 3-4 approaches, evaluate tradeoffs, recommend one.
5. PRE-MORTEM: Assume this failed in 6 months. Why? What should I design against?

Problem: [describe your situation with as much context as possible]
```

Mode 2 is more expensive (3-5x more tokens) but produces richer output. Use it for high-stakes decisions. Use Mode 1 for everything else.

### The Intake Pattern

For complex or unfamiliar problems, use a meta-prompt before running the pipeline:

```
I need to [brief description of challenge].

Before I ask you to analyze this, generate an intake questionnaire for me.
What do you need to know about the people, organizational context,
history, constraints, and success criteria?

Ask me the questions, I will answer, then we will proceed with analysis.
```

This surfaces blind spots in your own briefing. The pipeline is only as good as the context you feed it.

---

## What the Pipeline Produces That Baseline Misses

Based on cross-model testing (Sonnet 4.5 generation, Opus 4.6 evaluation) across problems at three complexity levels:

| What | Baseline ("think step by step") | Pipeline |
|------|--------------------------------|----------|
| Questions the framing | Rarely | Consistently (FPR stage) |
| Structured option comparison | Single recommendation | 3-5 options with tradeoffs and probability estimates |
| Stakeholder incentives mapped | No | Yes (AdR stage) |
| Specific failure modes | Generic warnings or none | Named failure modes with concrete mitigations |
| Uncomfortable truths surfaced | Suppressed by default agreeableness | Surfaced via permission slip stages |

### Where pipeline value is highest

The value scales with problem complexity:

- **Simple, well-defined problems:** Pipeline produces the same answer as baseline but costs 3x more. Not worth it.
- **Medium problems:** Pipeline adds structured options and failure analysis. The jump from baseline to Light (3-stage) is the biggest value gain.
- **Complex, multi-stakeholder problems:** Pipeline is transformative. Adversarial and Pre-Mortem stages surface dynamics that baseline suppresses entirely.

### Where pipeline value is lowest

- Simple factual questions
- Low-stakes routine work
- Problems where the path forward is already clear
- Time-sensitive situations where speed matters more than depth

---

## Limitations

- Pipeline costs 3-5x more tokens and time than simple prompts
- The testing behind these findings is practitioner-level (cross-model, varied complexity) but not peer-reviewed
- AI outputs are working notes, not ground truth -- verify critical points independently
- Works best with rich context; thin briefings produce thin analysis regardless of pipeline
- "More thorough analysis" does not automatically mean "better decisions" -- that depends on what you do with the analysis
- The specific framework sequences have not been validated as optimal across all domains

---

## Why the pipeline works (mechanism, post-correction)

The original framing here was that adversarial and Pre-Mortem prompts exploit a thin RLHF alignment layer and that framing is what surfaces uncomfortable truths. That framing is **not wrong, but it is not the load-bearing driver.** Program A's mechanism-isolation experiments corrected it.

The corrected mechanism is **controlled heterogeneity**:

1. **Structured decomposition (Phase 0)** standardizes how every reviewer interprets the raw input. Without it, disagreements happen at the parsing level and look like analytical disagreement.
2. **Per-stage temperature profiles** open the output distribution at the stages where diverse completions matter (AdR 0.7, PMR 0.7, ToT 0.6) and tighten it where determinism matters (Phase 0 0.1, Synthesis 0.1).
3. **Genuinely diverse reviewer models from different training origins** produce genuinely different analytical trajectories. This is the primary driver. A panel of four models from Anthropic, Moonshot, Qwen, and a fourth distinct origin does not behave like four copies of one model — even at identical temperatures.

Program A's mechanism-isolation results:

| Configuration | What was removed | Result |
|---|---|---|
| Exp 6: Adversarial off | adversarial framing | effect preserved |
| Exp 3 Swap C: Duplicate model | model diversity | UNIQUE collapsed 15 → 8 (47%) |

Adversarial framing is **supportive**. Model diversity is **load-bearing**. Both are real. Only one is primary.

The older RLHF-alignment-bypass framing is preserved in the literature, and higher temperature on AdR/PMR does expand the completion space, but the effect is not a jailbreak-style trick. It is a pipeline that runs genuinely different reasoners over a shared decomposition of the problem and returns their union for an analyst to read.

---

## v4 Pipeline Architecture

The v3 pipeline (documented above) chains frameworks sequentially with uniform parameters. Analysis through LLM architectural principles revealed six gaps — the most important being that the pipeline has no "tokenizer" (structured input decomposition), no residual connection (original problem gets buried), and no drift constraint (analysis can diverge undetected).

v4 adds: Phase 0 (structured decomposition before any framework runs), tiered parallel execution, residual injection of the original problem at every stage, drift gates between tiers, per-stage temperature profiles, and a marginal value audit at synthesis.

A/B testing on real production code showed that Phase 0 and temperature profiles are **necessary counterbalances** — temperature alone is actively harmful (increases disagreement), Phase 0 alone does not reduce SPLITs (though it doubles MAJOR findings and increases CONSENSUS), but together they reduce SPLIT variance and stabilize UNIQUE findings. The interaction is non-obvious and would not be predicted from either mechanism alone.

**Correction (2026-04-19):** an earlier write-up claimed v4 eliminated SPLITs for $0.09 more per run. Five identical re-runs of the same artifact produced SPLIT counts of 3, 6, 0, 4, 3 (mean 3.2, stdev ~2). The original zero-SPLIT outcome was a single-run observation inside natural variance, not a repeatable elimination. Treat SPLITs as per-instance signal, not a pipeline-level KPI. UNIQUE findings — the stable de-anchoring signal — are the load-bearing metric. See [`EVIDENCE.md`](EVIDENCE.md) §2 and §5.

**[Full v4 architecture →](experiments/v4-architecture.md)** · **[A/B comparison data →](experiments/v3-vs-v4-comparison.md)** · **[LLM principles analysis →](experiments/llm-principles-analysis.md)**

---

*The pipeline does not make the model smarter. It changes what the model is willing to say.*

---

## See also

- **[Model Shootout](experiments/model-shootout.md)** — Multi-model benchmark testing which Bedrock models perform best in chained reasoning pipelines, and empirical proof that role-based model assignment (Challenger / Architect / Debugger) produces balanced insight distribution vs. single-model dominance.
- **[v4 Architecture](experiments/v4-architecture.md)** — Phase 0, parallel tiers, residual injection, drift gates, temperature profiles, marginal value audit.
- **[LLM Principles Analysis](experiments/llm-principles-analysis.md)** — Graph of Thoughts mapping of 9 LLM architectural principles onto the pipeline.
