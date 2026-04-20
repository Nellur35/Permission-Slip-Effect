# Permission Slip Effect

*Structured prompts and a reference CLI for surfacing the assumptions, failure modes, and stakeholder dynamics an LLM would otherwise skip past — then handing that enriched context to a competent analyst.*

`Permission-Slip-Effect` is **not primarily a software product**. It is a **practical operating model** for using AI more rigorously in analysis-heavy work — architecture review, threat modeling, policy design, clinical reasoning, and ambiguous decisions where being wrong is expensive.

---

## Scope

**This repository is the Permission Slip Effect (PSE)** — a domain-agnostic prompt-engineering insight, reasoning pipeline, and analytical toolkit. It works in any analysis-heavy discipline where ambiguity is the main cost: security review, pharmacy, UX decisions, HR, legal analysis, medical diagnosis, product strategy, policy design.

**Looking for the security-first AI development methodology?** That project has moved to its own repository: [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology). The methodology uses PSE as its prompting substrate.

---

The repository has two layers.

| Layer | What it is | Best for |
|------|------|------|
| `tools/` | Paste-in prompts for review, threat modeling, audits, intake, and retrospectives | Immediate use in any AI chat |
| `pipeline/` | A reference Python CLI that automates multi-stage reasoning pipelines | Advanced users who want structured runs |

## Why this exists

LLMs often stop at the first plausible, agreeable answer. That is fine for low-stakes tasks. It is dangerous for architecture, security, policy, and decisions where the cost of being wrong is high.

This repository is built around one practical idea.

> If you decompose the problem, run it past genuinely diverse models under different temperature profiles, and then hand the resulting assumptions, failure modes, and stakeholder reframings to a competent analyst, you get sharper analysis than either a single prompt or a single model could produce alone.

The load-bearing mechanism is **controlled heterogeneity** (structured decomposition + temperature differentiation + reviewer models from different training origins), not the adversarial framing on its own. Adversarial prompts help, but Program A's mechanism-isolation test showed that removing model diversity collapses unique findings by 47% (15 → 8), while removing adversarial framing does not. See [`EVIDENCE.md`](EVIDENCE.md).

The project packages that idea as **portable prompts** and a **reference implementation**.

### How to use the output (two-stage pattern)

PSE is a **surfacing tool, not a decision tool.** The right usage is two-stage:

1. **Run the pipeline to surface material.** The five framework stages (FPR, RCAR, AdR, ToT, PMR) produce raw assumptions, failure modes, stakeholder dynamics, and reframings.
2. **Feed the surfaced stages to a competent analyst** — either you reading the raw stage outputs, or a subsequent model prompt that takes the stages as enriched context and produces the recommendation.

The convergence stage is a **summary / navigation aid**, not the product. Treating convergence output as the final answer is the single most common misuse.

## Start in 5 minutes

Choose the entry point that matches your intent.

| If you want to... | Start here |
|------|------|
| Review a design or document | [`tools/review.md`](tools/review.md) |
| Threat model an architecture | [`tools/threat-model.md`](tools/threat-model.md) |
| Audit an existing codebase or CI/CD setup | [`tools/audit.md`](tools/audit.md) |
| Run the automated reasoning pipeline | [`pipeline/README.md`](pipeline/README.md) |
| Read the empirical evidence | [`EVIDENCE.md`](EVIDENCE.md) |
| Load the whole system into an AI tool | [`FULL-CONTEXT.md`](FULL-CONTEXT.md) |
| Use the full development methodology | [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) |

If you are new to the project, start with **one prompt file** in `tools/`. If that immediately improves the sharpness of your review, try the reasoning pipeline on a real decision. Use the CLI only if you specifically want structured, repeatable pipeline runs.

## What this repository is — and is not

| It is | It is not |
|------|------|
| A prompt library and reasoning pipeline you can use immediately | A polished end-to-end platform |
| A structured information-surfacing tool | A replacement for engineering judgment |
| A practitioner-tested, empirically-validated system | Proof that one pipeline is optimal for every domain |

That distinction matters. The repository’s strongest value is the **thinking model and analytical discipline**, not a large automation layer.

## When to use it

Use this repository when the problem is ambiguous, when multiple stakeholders or hidden incentives matter, when you need stronger threat modeling or adversarial review, or when being wrong is expensive.

Do **not** use the full pipeline for simple, well-defined, or speed-critical tasks. On easy work, direct prompting is usually cheaper and good enough.

## Evidence

Two experimental programs (~$11 total, 30+ runs) stress-tested PSE's claims. Both corrected earlier overconfident claims. The corrected evidence supports a narrower, sharper thesis:

| Finding | Source |
|------|------|
| Pipeline + competent analyst wins 4/4 decisions, +3 mean on 25-point rubric | Program B |
| Mechanism is model diversity under structure, not adversarial framing | Program A |
| Effect is domain-sensitive: strongest where models have training depth | Program A |
| Cross-domain generalization confirmed by independent pharmacist adoption | External validation |
| Original v4 "zero-SPLIT" claim was within natural variance — corrected | Program A |

**PSE is a structured information-surfacing tool.** Run the pipeline to surface material, then feed it to a competent analyst. Don't treat the convergence summary as the product — the raw surfaced stages are the product.

Full empirical basis, corrected claims, and decision framework: [`EVIDENCE.md`](EVIDENCE.md).

Raw experiment data: [`experiments/`](experiments/).

## Repository map

| Path | Purpose | Status |
|------|------|------|
| [`EVIDENCE.md`](EVIDENCE.md) | Canonical empirical evidence, corrected claims, and decision framework | Stable |
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | Single-file context dump for AI tools | Stable |
| [`tools/`](tools/) | Low-friction prompts | Stable |
| [`pipeline/`](pipeline/) | Reference automation layer | Beta |
| [`experiments/`](experiments/) | Validation notes and comparisons | Experimental |
| [`gotchas/`](gotchas/) | Known failure modes and limits | Stable |
| [`STATUS.md`](STATUS.md) | Project surface-area status definitions | Stable |

Not sure where to begin? Read [`START-HERE.md`](START-HERE.md).

## What to adopt first

If you want the highest return for the least process overhead, adopt these pieces in order.

| Order | Recommended first move | Why |
|------|------|------|
| 1 | Use one prompt from `tools/` | Fastest path to value |
| 2 | Use the reasoning pipeline on one high-stakes decision | Good fit for ambiguous, expensive mistakes |
| 3 | Read [`EVIDENCE.md`](EVIDENCE.md) for the decision framework | Know when PSE adds value and when to skip it |
| 4 | Adopt the full development methodology | See [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) |

## Development and contribution

If you want to contribute, read these in order.

| File | Why it matters |
|------|------|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contribution workflow and expectations |
| [`STATUS.md`](STATUS.md) | What is stable, beta, and experimental |
| [`pipeline/frameworks.json`](pipeline/frameworks.json) | External prompt catalog for the CLI |
| [`tests/test_pipeline.py`](tests/test_pipeline.py) | Baseline regression coverage for the reference CLI |

## Bottom line

This repository helps teams use AI with more friction, more skepticism, and more decision discipline.

If your work is low-stakes or routine, this is overkill.

If your work is expensive to get wrong, it may be exactly the right kind of overkill.

MIT · [Asaf Yashayev](https://github.com/Nellur35) · Security hobbyist
