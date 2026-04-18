---
name: security-first-methodology
description: >
  Orchestrator for the security-first development methodology.
  Routes to the right skill for each phase. Activates when the
  user starts a new project, asks about methodology, or needs
  to know what phase to work on next.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Security-First AI Dev Methodology

You are the engine. The user is the navigator and judge. Gate questions decide when a phase is complete. Phases 1-5 are sequential. Phase 6 onwards is iterative.

## Phase Routing

| Phase | What to Do | Skill |
|-------|-----------|-------|
| 1 — Problem | Define the real-world need | `/intake` |
| 2 — Requirements | Define what, not how. Use `templates/phase-2-requirements.md` | Direct work |
| 2.5 — Decomposition | Decompose into sub-projects + seams (if triggered). Use `templates/phase-2.5-decomposition.md` | `/decompose` |
| 3 — Architecture | Design for testability. Offer `/review` when done. Runs N+1 times if decomposition produced N > 1 sub-projects. | Direct work |
| 4 — Threat Model | Attack every trust boundary. Seam threat model mandatory when N > 1. | `/threat-model` |
| 5 — CI/CD Pipeline | Pipeline defines done. Select testing domains per project type. Offer `/review` when done | Direct work |
| 6 — Tasks | Break into pipeline-validatable units. Sub-project tags when decomposed. | Direct work |
| 7 — Implementation | Code + tests. Use `/gate-check` per task | Direct work |
| 8 — Production | Feed failures back into the pipeline | Direct work |

## Available at Any Phase

| Need | Skill |
|------|-------|
| Check exit criteria before moving on | `/gate-check` |
| Adversarial review of any artifact | `/review` |
| Scan an existing codebase or CI/CD | `/audit` |
| Decompose a system into sub-projects | `/decompose` |

## Context Handoff

| Phase | Handoff Artifact |
|-------|-----------------|
| 1 -> 2 | `problem_statement.md` or `reconstruction_assessment.md` |
| 2 -> 2.5 | `requirements.md` |
| 2.5 -> 3 | `decomposition-map.md` (or single-project verdict). If Phase 2.5 skipped, `requirements.md` passes directly to Phase 3. |
| 3 -> 4 | `architecture.md`. Runs N+1 times if decomposition produced N > 1 sub-projects. |
| 4 -> 5 | `threat_model.md`. Seam threat model is a separate artifact when N > 1. |
| 5 -> 6 | Pipeline config + dummy product + `requirements.md` + `threat_model.md` |
| 6 -> 7 | `tasks.md` |
| 7 -> 8 | Working code + test results |

If it's not in the output file, it doesn't carry forward.

## Phase Re-entry

Implementation will reveal upstream flaws. That's the process working. Identify which phase owns the flaw, re-run it with the current output + the finding, propagate changes forward.

## Brownfield Mode (Phase 2.5 for Existing Systems)

When the intake detects a scoped change to an existing system, Phase 2.5 runs in brownfield mode. This replaces the previous "scoped mode" concept with a richer decomposition-based approach.

### Brownfield Phase Routing

| Phase | Full Mode | Brownfield Mode |
|-------|----------|----------------|
| 1 — Problem | `/intake` → `problem_statement.md` | `/intake` → `change-decomposition.md` (via Phase 2.5 brownfield) |
| 2 — Requirements | Full system requirements | Requirements for the change only |
| 2.5 — Decomposition | Greenfield: produce `decomposition-map.md` | Brownfield: produce `change-decomposition.md` — which sub-projects are affected, which seams are crossed |
| 3 — Architecture | Full system architecture | Architecture of affected sub-projects + interfaces to existing system |
| 4 — Threat Model | All 14 areas + seam threat model | Only areas the change touches + seam threat model for any crossed seams |
| 5 — CI/CD | Full pipeline design | Pipeline gates for the change — testing domains per affected sub-project |
| 6 — Tasks | Full task breakdown | Tasks scoped to affected sub-projects with sub-project tags |
| 7 — Implementation | Full implementation | Implementation within scope boundary |
| 8 — Production | System-wide feedback | Feedback on the change's behavior in production |

### Brownfield Handoff Chain

| Phase | Handoff Artifact |
|-------|-----------------|
| 1 -> 2.5 | Problem description + existing `decomposition-map.md` (if available) |
| 2.5 -> 3 | `change-decomposition.md` (affected sub-projects + crossed seams) |
| 3 -> 4 | `architecture.md` (scoped — affected sub-projects + seam interfaces) |
| 4 -> 5 | `threat_model.md` (scoped — affected areas + seam threat model) |
| 5 -> 6 | Pipeline config for the change |
| 6 -> 7 | `tasks.md` (scoped, sub-project-tagged) |

### Scope Expansion

If any phase reveals the change affects more sub-projects or seams than `change-decomposition.md` lists, STOP. Update the decomposition. Re-evaluate whether brownfield mode is still appropriate. If the scope has doubled, switch to full mode with the Existing Project Path.

## Three Unbreakable Rules

1. Tests verify behavior against requirements -- not execute lines of code.
2. Pipeline gates are never weakened to make things pass.
3. Effort matches scope. A 200-line script does not get a 13-area threat model. A single-function change does not get an 8-question intake.

## Cost Discipline

AI time is a budget, not infinite. These constraints apply to every skill:

**Before running any skill, estimate scope:**
- How many components are involved?
- How many trust boundaries are crossed?
- How large is the artifact being produced or reviewed?
- Is this a full-system run or a scoped change?

**Match effort to scope:**

| Scope | Intake | Decomposition (2.5) | Threat Model | Review | Gate Check |
|-------|--------|-------------------|-------------|--------|------------|
| Single function/fix | Skip — state the problem directly | Skip | Skip — unless it touches auth/secrets | 3-5 findings max | 2-3 gates |
| Single feature (brownfield) | Scoped Change Path (6 questions) | Brownfield — affected sub-projects + crossed seams | Scoped — affected areas + seam threat model | Focus on seam + change boundary | Scoped gates + Phase 2.5 gates |
| Multi-component feature | Existing Project Path (6 questions) | Full — decompose if 3+ domains | Full — all 14 areas | Full review | Full gates |
| New system | Greenfield Path (8 questions) | Full — decompose if triggered | Full — all 14 areas + seam threat model | Full review | Full gates |

**Agent rules:**
- Max 3 sentences of instruction before code. Skip preamble.
- Never re-read a file already in context.
- Batch all independent file edits into one turn.
- Cap fix attempts at 2, then ask the navigator for direction or escalate to multi-model reasoning.
- When the navigator provides the fix approach, skip exploration — go straight to implementation.
- Before dispatching a subagent on "add X to file" tasks, grep for X first. If already present, skip the dispatch.

**Navigator habits (reminders for the human):**
- Close unused editor tabs — each open tab adds to context cost every turn.
- Summarize external content (Slack threads, emails) before pasting.
- If a change takes fewer characters to describe than to implement, do it manually.
- Front-load intent: "do task 3 using approach X, skip Y" saves exploration turns.
- Triage counterexamples yourself first — if fix is obvious, tell the agent "change X to Y."

**Escalation rule:** If a bug survives 2 fix attempts → STOP trial-and-error. Use council (multi-model reasoning via `pipeline.py`) or ask the navigator to re-analyze the approach. Never burn >2 cycles without switching approach.

**The marginal value test:** Before producing any section of output, ask: does this add signal the navigator doesn't already have? If no, skip it.

## Full Reference

See `METHODOLOGY.md` for rationale, worked examples, the reasoning pipeline, and the multi-model review system.

## Gotchas

**Tries to run multiple phases in one session.** The orchestrator routes to the right skill per phase, but it doesn't enforce "one phase per session." Under navigator pressure ("let's get through Phases 1-3 today"), the model compresses phases, skips gate checks between them, and produces artifacts that haven't been reviewed. Each phase transition should include a gate check. If the navigator wants speed, the answer is parallel sessions (Tier 2), not compressed phases.

**Routes to direct work when a skill exists.** Phases 2, 3, 5, 6, 7, 8 are listed as "Direct work" in the routing table. But `/review` should be offered at the end of every phase, and `/gate-check` should be offered at every transition. The model sometimes does Phase 3 → Phase 4 without offering either. The routing table shows what skill *runs the phase* — it doesn't show the skills that *close the phase*.

**Loses phase context in long sessions.** After 40+ turns, the model forgets which phase it's in and starts mixing phase concerns. Implementation decisions appear in Phase 2 discussions. Architecture details leak into Phase 1. The phase routing table in the orchestrator should be re-read at every phase transition, not just at session start.

**Doesn't enforce the handoff artifact.** The skill says "if it's not in the output file, it doesn't carry forward." But the model frequently carries context from the conversation that isn't in the artifact. Phase 3 discussions influence Phase 4 work even when they weren't captured in `architecture.md`. The discipline is: re-read the artifact at the start of each phase. If it's not in the file, it doesn't exist.

**Full methodology on trivial changes.** A one-function bug fix does not need 8 phases. If the navigator describes a fix, not a feature, acknowledge it and skip to the relevant phase (usually Phase 7 with a focused gate check). Running Phase 1 intake on a bug report is cost discipline failure.
