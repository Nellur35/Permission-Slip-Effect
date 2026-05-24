# Start Here

Permission Slip Effect (PSE) is a **standalone, domain-agnostic, model-consumable substrate** for surfacing the assumptions, failure modes, hidden incentives, stakeholder dynamics, and uncomfortable possibilities a single prompt would skip past — so a competent analyst (human or model) can decide on richer material.

It is not a development methodology. It is not an agent harness. It is not a finished-answer generator. Most useful PSE work is **one paste-in prompt**, not a full pipeline.

## For humans

What do you want to do?

| I want to... | Go here |
|---|---|
| **Decide whether PSE is the right tool at all** | [`README.md`](README.md) routing table, then [`EVIDENCE.md`](EVIDENCE.md) §6 decision framework |
| **Review something right now** | Paste [`tools/review.md`](tools/review.md) into any AI conversation |
| **Threat model an architecture** | Paste [`tools/threat-model.md`](tools/threat-model.md) |
| **Scan an existing codebase / CI** | Paste [`tools/audit.md`](tools/audit.md) |
| **Define a problem properly** | Paste [`tools/intake.md`](tools/intake.md) |
| **Run a session retrospective or incident analysis** | Paste [`tools/session-retro.md`](tools/session-retro.md) |
| **Analyze an ambiguous high-stakes decision** | [`reasoning-pipeline.md`](reasoning-pipeline.md) or `python pipeline/pipeline.py reason "..."` |
| **Read the empirical evidence** | [`EVIDENCE.md`](EVIDENCE.md) — what PSE proved, corrected, and when to use it |
| **See where the substrate breaks** | [`gotchas/GOTCHAS-SYSTEM.md`](gotchas/GOTCHAS-SYSTEM.md) |
| **See the raw experiments** | [`experiments/`](experiments/) |

## For AI agents

If you are an AI tool reading this repo on a user's behalf:

1. **Classify the task first** (simple factual, routine bounded, ambiguous decision, architecture review, threat model, audit, stakeholder-heavy decision, incident analysis, session retro, problem intake).
2. **Skip PSE** for simple factual, routine, low-risk, or already-well-bounded tasks. Use a direct prompt.
3. **Pick the smallest PSE tool** that fits — usually a single file in `tools/`.
4. **Reach for the full pipeline** only when ambiguity, stakes, and irreversibility justify the 3–5x token cost.
5. **Always two-stage the output.** Surface with PSE → competent analyst (you or a downstream prompt) consumes the surfaced stages → recommendation. Do not treat the convergence summary as the final answer.
6. **Do not call same-family or same-context reviewers a real independent council.** Diversity is load-bearing.

For a single-URL deep-read entry point built for AI consumers, see [`FULL-CONTEXT.md`](FULL-CONTEXT.md).
