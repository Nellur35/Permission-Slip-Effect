# Permission Slip Effect

*Structured prompts, methodology, and a reference CLI for getting more critical, less agreeable analysis from LLMs when being wrong is expensive.*

`Permission-Slip-Effect` is **not primarily a software product**. It is a **practical operating model** for using AI more rigorously in architecture review, threat modeling, code audit, and ambiguous technical decisions.

---

## Scope

This repository currently contains two interrelated projects:

1. **The Permission Slip Effect (PSE)** — a prompt-engineering insight and reasoning pipeline that is domain-agnostic. See `tools/`, `pipeline/`, and `experiments/`. Works in any analysis-heavy discipline where ambiguity is the main cost: security review, pharmacy, UX decisions, HR, legal analysis, medical diagnosis, product strategy, policy design.

2. **A security-first AI-assisted development methodology** — an 8-phase discipline that uses PSE as a prompting substrate and adds the software-engineering scaffolding needed to build security-critical systems with AI. See `methodology/`, `integrations/`, and `case-studies/`. The methodology produced [`cicd-audit`](https://github.com/Nellur35/cicd-audit) (a 50-rule CI/CD security auditor) as its first full-cycle output. **This project is migrating to its own repository: [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology).**

These projects evolved together and currently share a repo. Contributors and readers should consume whichever layer matches their use case; each has its own evidence base and defensible claims.

---

The repository has three layers.

| Layer | What it is | Best for |
|------|------|------|
| `tools/` | Paste-in prompts for review, threat modeling, audits, gate checks, intake, and retrospectives | Immediate use in any AI chat |
| `methodology/` | A security-first AI-assisted development method (Phases 1-8 + Phase 2.5 Decomposition) with gates, templates, testing domains reference, and worked examples | Teams building real systems |
| `pipeline/` | A reference Python CLI that automates multi-stage reasoning pipelines | Advanced users who want structured runs |

## Why this exists

LLMs often stop at the first plausible, agreeable answer. That is fine for low-stakes tasks. It is dangerous for architecture, security, and decisions where the cost of being wrong is high.

This repository is built around one practical idea.

> If you force the model through structured adversarial, failure-oriented, and de-anchoring frames, it will often surface risks and contradictions that baseline prompting suppresses.

The project packages that idea as **portable prompts**, a **development methodology**, and a **reference implementation**.

## Start in 5 minutes

Choose the entry point that matches your intent.

| If you want to... | Start here |
|------|------|
| Review a design or document | [`tools/review.md`](tools/review.md) |
| Threat model an architecture | [`tools/threat-model.md`](tools/threat-model.md) |
| Decompose a complex multi-component system | [`tools/decomposition.md`](tools/decomposition.md) |
| Design test coverage for CI/CD | [`methodology/testing-domains-reference.md`](methodology/testing-domains-reference.md) |
| Audit an existing codebase or CI/CD setup | [`tools/audit.md`](tools/audit.md) |
| Start a new project with the full method | [`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md) |
| Run the automated reasoning pipeline | [`pipeline/README.md`](pipeline/README.md) |
| Load the whole system into an AI tool | [`FULL-CONTEXT.md`](FULL-CONTEXT.md) |

If you are new to the project, start with **one prompt file** in `tools/`. If that immediately improves the sharpness of your review, then adopt selected parts of the methodology. Use the CLI only if you specifically want structured, repeatable pipeline runs.

## What this repository is — and is not

| It is | It is not |
|------|------|
| A methodology for AI-assisted engineering rigor | A polished end-to-end platform |
| A prompt library you can use immediately | A replacement for engineering judgment |
| A reference implementation of a reasoning pipeline | Proof that one pipeline is optimal for every domain |
| A practitioner-tested system | A peer-reviewed scientific result |

That distinction matters. The repository’s strongest value is the **thinking model and review discipline**, not a large automation layer.

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
| [`methodology/`](methodology/) | Full development methodology + testing domains reference | Stable |
| [`pipeline/`](pipeline/) | Reference automation layer | Beta |
| [`examples/`](examples/) | Example inputs and expected outputs | Beta |
| [`experiments/`](experiments/) | Validation notes and comparisons | Experimental |
| [`integrations/`](integrations/) | Tool-specific workflows | Experimental |
| [`multi-agent/`](multi-agent/) | Multi-agent operating patterns | Experimental |
| [`gotchas/`](gotchas/) | Known failure modes and limits | Stable |
| [`STATUS.md`](STATUS.md) | Project surface-area status definitions | Stable |

Not sure where to begin? Read [`START-HERE.md`](START-HERE.md).

## What to adopt first

If you want the highest return for the least process overhead, adopt these pieces in order.

| Order | Recommended first move | Why |
|------|------|------|
| 1 | Use one prompt from `tools/` | Fastest path to value |
| 2 | Add a gate question from the methodology | Improves review rigor without major ceremony |
| 3 | Use the reasoning pipeline on one high-stakes decision | Good fit for ambiguous, expensive mistakes |
| 4 | Standardize selected artifacts in your team | Turns the method into a repeatable habit |
| 5 | Extend the CLI only if you need structured automation | The automation layer is supportive, not primary |

## Example run

The repository now includes an example review flow based on [`cicd-audit`](https://github.com/Nellur35/cicd-audit), a concrete project built with this methodology.

| Example file | Purpose |
|------|------|
| [`examples/cicd-audit-artifact.md`](examples/cicd-audit-artifact.md) | Input artifact excerpt used for review |
| [`examples/cicd-audit-review-output.json`](examples/cicd-audit-review-output.json) | Curated example of a review pipeline result |
| [`examples/cicd-audit-reasoning-problem.md`](examples/cicd-audit-reasoning-problem.md) | Example decision/problem statement |
| [`examples/cicd-audit-reasoning-output.json`](examples/cicd-audit-reasoning-output.json) | Curated example of a reasoning pipeline result |

These are **expected-output examples**, not benchmark truth. Their purpose is to show contributors what a good structured output looks like.

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
