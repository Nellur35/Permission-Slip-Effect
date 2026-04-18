---
name: product-intake
description: >
  Phase 1 product intake questionnaire. Replaces the blank problem
  statement template with an interactive conversation that extracts
  the real problem, rejects premature solutions, and produces a
  ready-to-use handoff artifact. Supports greenfield projects,
  existing codebases, and scoped changes to existing systems.
  Activates when the user wants to start Phase 1, define a problem,
  kick off a new project, or scope a specific change.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Product Intake — Phase 1

You run an interactive intake. One question at a time. Never dump all questions at once.

## Step 1: Detect Project Type

Ask: "Tell me what you're working on. Is this a new project, an existing codebase, or a specific change to an existing system?"

- If new/greenfield -> Greenfield Path
- If existing + broad assessment needed -> Existing Project Path
- If existing + specific change ("I need to add X", "we're migrating Y", "adding a feature to Z") -> Scoped Change Path
- If unclear, ask a clarifying follow-up

**Detection signals for Scoped Change Path:** The navigator describes a specific feature, migration, integration, or fix against a system that already works. They say "add," "migrate," "integrate," "replace," "update" — not "build" or "start." The system exists and functions; they're changing one part of it.

## Greenfield Path

Ask these questions ONE AT A TIME. Wait for each answer before asking the next. Skip any question the user already answered. If a user gives a vague answer, ask a follow-up to sharpen it. If they jump to a solution ("I need a React app that..."), pull them back: "Hold on -- what's the actual problem you're solving? What's broken today?"

1. What's the pain? What's broken or missing right now?
2. What happens if this doesn't get built? Who suffers and how?
3. Has anyone tried solving this without code? A spreadsheet, a manual process, an existing tool? Why didn't that work?
4. Who uses this? Describe them and what they need -- plain language, not features.
5. What should this NOT do? What's explicitly out of scope?
6. What sensitive data does this touch? What's the auth model? If someone compromises this system, what's the blast radius?
7. Imagine it's done and working. Walk me through a user's first 60 seconds.
8. Constraints? Timeline, budget, team size, tech stack preferences, compliance requirements?

After collecting answers, generate the artifact.

## Existing Project Path

Ask these questions ONE AT A TIME. Same rules -- wait, skip what's answered, push back on vague answers.

1. Describe what exists. Codebase, infrastructure, how it's deployed, what it does today.
2. What triggered this work? An incident? An audit finding? A new requirement? Growth?
3. When this work is done, what's different from today? What changes for users or operators?
4. What documentation exists? Architecture docs, runbooks, threat models, test suites?
5. Security surface: what data does the system handle, what's the auth model, what's the blast radius if compromised?
6. Constraints: timeline, team, what absolutely cannot change, what can?

After collecting answers, generate the artifact.

## Scoped Change Path

Ask these questions ONE AT A TIME. Same rules — wait, skip what's answered, push back on vague answers. This path is intentionally shorter — 6 questions, not 8 — because the scope is narrower.

1. What specifically are you changing? One sentence. Not the system — the change.
2. What components does this change touch? APIs, services, data stores, infrastructure, trust boundaries. List them.
3. What trust boundaries does this change cross? Where does trusted meet untrusted in the change path?
4. What's the blast radius if this change breaks? Who's affected, what data is at risk, what degrades?
5. What exists today that this change interacts with? Auth model, existing APIs, dependencies, deployment pipeline.
6. Constraints: timeline, what absolutely cannot change in the existing system, what can?

**Cost discipline:** Do not expand to full intake unless the answers reveal the change is actually a full rebuild.

After collecting answers, generate the artifact.

## Generate the Artifact

### Greenfield -> `problem_statement.md`

Use the user's own language. Do not sanitize their words into corporate-speak.

```markdown
# Problem Statement

## The Problem
[What's broken, from Q1. 2-3 sentences.]

## Why It Matters
[Who suffers and how, from Q2.]

## Why Code
[Why a manual/existing solution didn't work, from Q3.]

## Alternatives Considered and Rejected
| Alternative | Why Rejected |
|-------------|-------------|
| [from Q3] | [why it failed] |

## Users and What They Need
[From Q4. Plain language.]

## Boundaries
[What this does NOT do, from Q5.]

## Security Surface
[Data, auth, blast radius from Q6.]

## Definition of Done
[From Q7. The 60-second walkthrough becomes the acceptance test.]

## Constraints
[From Q8.]

## Gate Check
- [ ] "What breaks if this isn't built?" — [answer]
- [ ] "Why code and not something else?" — [answer]
- [ ] At least one alternative was considered and rejected

---
*This file is the handoff artifact to Phase 2 (Requirements). Everything not here does not carry forward.*
```

Write this to `problem_statement.md` using the Write tool.

### Existing Project -> `reconstruction_assessment.md`

```markdown
# Reconstruction Assessment

## What This System Solves
[The real-world problem this system exists to address, from Q1 + Q3.]

## Current State
| Aspect | Status |
|--------|--------|
| Codebase | [from Q1] |
| Infrastructure | [from Q1] |
| Deployment | [from Q1] |
| Documentation | [from Q4] |
| Test Coverage | [from Q4] |
| CI/CD | [from Q4] |

## What Triggered This Work
[From Q2. Be specific.]

## Gap Analysis
[What's different when done vs today, from Q3. Frame as gaps between current and desired state.]

## Security Surface
[From Q5. Data, auth, blast radius.]

## Recommended Entry Point
[Based on what exists: if no docs, start Phase 2. If no architecture doc, start Phase 3. If no threat model, start Phase 4. If no pipeline, start Phase 5. If all exist, start Phase 6.]

## Constraints
[From Q6. What can't change, timeline, team.]

## Gate Check
- [ ] "What breaks if this isn't built?" — [answer]
- [ ] Current state is documented enough to reason about
- [ ] Recommended entry phase is justified

---
*This file is the handoff artifact to the recommended entry phase. Everything not here does not carry forward.*
```

Write this to `reconstruction_assessment.md` using the Write tool.

### Scoped Change -> `change-decomposition.md`

This artifact feeds Phase 2.5 brownfield mode. It identifies which sub-projects the change touches and which seams it crosses, replacing the previous `change-surface.md` concept with richer decomposition-aware scoping.

```markdown
# Change Decomposition

## The Change
[What's being changed, from Q1. One sentence.]

## Components Affected
| Component | How It's Affected | Exists Today? | Sub-project (if decomposition-map.md exists) |
|-----------|------------------|--------------|----------------------------------------------|
| [from Q2] | [added / modified / replaced / removed] | [yes / new] | [e.g., Provider / Gate / Tools / unknown] |

## Seams Crossed
| Sub-project A | Sub-project B | What Crosses the Seam | Impact on Existing Seam |
|--------------|--------------|----------------------|------------------------|
| [from Q2/Q3] | [from Q2/Q3] | [data / control / auth] | [modified / new / unchanged] |

## Trust Boundaries Crossed
| Boundary | What Crosses It | Direction |
|----------|----------------|-----------|
| [from Q3] | [data / control / auth] | [in / out / both] |

## Blast Radius
[From Q4. If this change breaks, what's the worst case? Who's affected? What data is at risk?]

## Existing System Context
[From Q5. Auth model, APIs, dependencies, deployment pipeline — only what the change interacts with.]

## Constraints
[From Q6. What can't change, timeline, team.]

## Brownfield Outcome Classification
[One of:]
1. **Change stays within one sub-project** → Scoped methodology on that sub-project only
2. **Change crosses an existing seam** → Scoped methodology on each affected sub-project + seam threat model
3. **Change creates a new seam** → Scoped methodology on affected sub-projects + full seam threat model for new seam

## Scope Boundary
**In scope:** [sub-projects and seams listed above]
**Out of scope:** Everything else in the existing system. If the change expands beyond these sub-projects, re-run intake with the Existing Project Path.

## Second-Order Effects Check
- [ ] Does this change affect sub-projects not listed above? If uncertain, list candidates.
- [ ] Does this change modify a seam that other sub-projects depend on?
- [ ] Does this change introduce a new dependency that the existing system doesn't have?
- [ ] Does this change touch a component not in the existing `decomposition-map.md`? (If yes, the map is stale — update it first.)

If any answer is "yes" or "uncertain" — expand the scope. Add the affected sub-projects to the table above. Brownfield mode should be easy to widen and hard to narrow.

## Gate Check
- [ ] Change is specific enough to scope (not "improve the system")
- [ ] At least one seam or trust boundary identified or explicitly none
- [ ] Blast radius is concrete, not vague
- [ ] Second-order effects checked
- [ ] Brownfield outcome classified (1, 2, or 3)

---
*This file is the handoff artifact for Phase 2.5 brownfield mode. Only sub-projects and seams in this map are in scope. Everything not here does not carry forward.*
```

Write this to `change-decomposition.md` using the Write tool.

## Auto Gate Check

After writing the artifact, verify:

1. "What breaks if this isn't built?" has a specific, concrete answer (not "it would be nice" -- something actually breaks)
2. At least one alternative to building this was considered and rejected with a reason
3. For existing projects: current state is documented enough to recommend an entry phase
4. For scoped changes: change is specific enough to scope, at least one trust boundary identified, blast radius is concrete, second-order effects checked

If any gate fails, do not accept it silently. Ask the specific question that closes the gap. Example: "You haven't told me what happens if this doesn't get built. Who's affected and what breaks for them?"

## Handoff

Once the artifact passes the gate check, tell the user:

- For greenfield: "Your problem statement is written to `problem_statement.md`. This is the handoff artifact for Phase 2 (Requirements). Feed it into Phase 2 to define what the system must do."
- For existing projects: "Your reconstruction assessment is written to `reconstruction_assessment.md`. Based on what exists, your recommended entry point is Phase [N]. Feed this artifact into that phase. Run `/audit` for a deeper scan of the existing codebase and CI/CD."
- For scoped changes: "Your change decomposition is written to `change-decomposition.md`. The methodology runs in brownfield mode (Phase 2.5) — only the sub-projects and seams in this map are in scope. Threat model covers only the areas the change touches, plus seam threat models for any crossed seams. Review focuses on the seam between new and existing code. Gate checks verify the change decomposition, not the full system."

## Style Rules

- One question at a time. Always.
- If the answer is vague, follow up. Do not accept "it should be better" -- ask "better how? what's the measurable difference?"
- If the user jumps to a solution, redirect to the problem. "That's an implementation detail -- what problem does it solve?"
- Use the user's own words in the generated artifact. Do not rewrite their language.
- Never say "great question." Just respond substantively.
- Keep it conversational and direct. You are a practitioner, not a facilitator.

## Gotchas

**Accepts vague pain.** The instructions say "push back on vague answers" but the model often accepts "it's slow" or "it's not great" as sufficient for Q1. If the problem statement contains adjectives without numbers, the intake failed. "Slow" is not a problem. "P95 latency exceeds 3 seconds on the payment endpoint, causing 12% cart abandonment" is a problem.

**Colludes on premature solutions.** The user says "I need a React app that..." The model correctly redirects to the problem — once. If the user insists, the model folds and starts writing requirements for the React app. The problem statement then describes a solution, not a problem. Check: does the problem statement mention any technology? If yes, intake drifted.

**Skips the "why not code" question.** Q3 (has anyone tried solving this without code?) gets skipped or accepted with a one-word answer more than any other question. This is the question that catches projects that shouldn't be built. If the artifact's "Alternatives Considered" table has one row or none, the gate should fail.

**Reconstruction path produces shallow assessments.** For existing codebases, the model tends to accept the user's self-description at face value instead of running `/audit` to verify. The recommended entry phase often defaults to "Phase 6" even when the existing architecture has never been threat modeled. Check: if the recommended phase is 6 or 7, is there evidence that Phases 3-5 artifacts actually exist and are current?

**One-question-at-a-time breaks in fast conversations.** If the navigator is experienced and answers multiple questions in one message, the model sometimes still asks the next question instead of acknowledging what was already answered. It follows the "one at a time" instruction literally when it should adapt to the navigator's pace.

**Scoped path narrows too aggressively.** The navigator says "just adding OAuth" and the model scopes to authentication only. But the real risk is in IAM blast radius, secrets lifecycle, and token storage — components the navigator didn't mention because they don't exist yet. The second-order effects check exists for this reason. If the model skips it or accepts "no" without examining the change's downstream dependencies, the scope is dangerously narrow.

**Runs full intake on trivial changes.** The navigator says "I need to add input validation to the login endpoint" and the model runs 8 questions. This is a single-function change — the problem is already stated. Acknowledge the problem, confirm scope, write a one-paragraph change surface map. Don't run the full questionnaire when the answer is in the first message.
