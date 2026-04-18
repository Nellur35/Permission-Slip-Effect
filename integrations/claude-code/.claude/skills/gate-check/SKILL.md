---
name: gate-check
description: >
  Verify exit criteria for any methodology phase. Auto-detects
  current phase from existing artifacts in the project. Activates
  when the user asks to check gates, wants to verify readiness,
  or is about to move to the next phase.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Gate Check

Verify you've met the exit criteria before moving forward.

## Step 1: Detect Current Phase

Glob for artifacts to figure out where the user is:

| Artifacts Found | Likely Finishing |
|----------------|-----------------|
| Nothing | Phase 1 |
| `problem_statement.md` or `reconstruction_assessment.md` | Phase 1 -> entering Phase 2 |
| `requirements.md` | Phase 2 -> entering Phase 2.5 (if triggered) or Phase 3 |
| `decomposition-map.md` or `change-decomposition.md` | Phase 2.5 -> entering Phase 3 |
| `architecture.md` | Phase 3 -> entering Phase 4 |
| `threat_model.md` | Phase 4 -> entering Phase 5 |
| Pipeline config (.github/workflows/, Jenkinsfile, etc.) | Phase 5 -> entering Phase 6 |
| `tasks.md` | Phase 6 -> entering Phase 7 |
| Implementation code + tests | Phase 7 (per task) |
| Deployed system | Phase 8 |

If ambiguous, ask: "Which phase are you checking?"

## Step 1.5: Detect Scope Mode

Glob for `change-decomposition.md` or `decomposition-map.md`. Also check for legacy `change-surface.md`.

If `change-decomposition.md` found → brownfield gates apply. Gate questions verify the **change decomposition**, not the full system.

If `decomposition-map.md` found → decomposition-aware gates apply. Phase 3-5 may run N+1 times.

### Brownfield Gate Additions (apply alongside phase-specific gates)

For every phase in brownfield mode, add:
- [ ] Does this artifact stay within the scope defined in `change-decomposition.md`?
- [ ] If the artifact touches sub-projects outside the change decomposition, has `change-decomposition.md` been updated?
- [ ] Are second-order effects on the existing system addressed?
- [ ] If seams are crossed, does a seam threat model exist for each crossed seam?

### Phase 2.5 Gate (Decomposition)
- [ ] Is the decomposition the simplest that could work?
- [ ] Does every sub-project pass at least 3 of 5 independence tests?
- [ ] If N > 1, does the integration sub-project have explicit seam boundaries?
- [ ] Does the seam threat model plan cover every pair of communicating sub-projects?
- [ ] Does every sub-project have recommended testing domains assigned?
- [ ] [Brownfield] Does this change touch a component not in the existing `decomposition-map.md`?

### Phase 4 Brownfield Gate (Threat Model)
- [ ] Does the threat model cover every trust boundary the change crosses?
- [ ] Does the seam threat model cover every crossed seam from `change-decomposition.md`?
- [ ] Are excluded areas explicitly marked with "not affected by this change"?
- [ ] If more than 10 of 14 areas are covered, is brownfield mode still justified?

If no decomposition artifacts exist → full gates apply as normal.

## Step 2: Read the Artifact

Read the artifact for the detected phase.

## Step 3: Evaluate Gates

### Phase 1 — Problem
- [ ] What breaks in the real world if this is not built?
- [ ] Why is code the right solution and not a process change, config, or existing tool?

**Proves:** The project has a real-world justification.
**Doesn't catch:** Whether the problem statement is too broad or solves a symptom.

### Phase 2 — Requirements
- [ ] Is every requirement testable?
- [ ] What is explicitly out of scope?
- [ ] What does done look like in reality, not on a dashboard?

**Proves:** Requirements are concrete, testable, and bounded.
**Doesn't catch:** Missing requirements you haven't thought of. Use `/review` to surface gaps.

### Phase 2.5 — Decomposition (if activated)
- [ ] Is the decomposition the simplest that could work?
- [ ] Does every sub-project pass at least 3 of 5 independence tests?
- [ ] If N > 1, does the integration sub-project have explicit seam boundaries?
- [ ] Does the seam threat model plan cover every pair of communicating sub-projects?
- [ ] Does every sub-project have recommended testing domains assigned?
- [ ] [Brownfield] Does this change touch a component not in the existing `decomposition-map.md`?

**Proves:** Decomposition is principled, not arbitrary. Seams are explicit.
**Doesn't catch:** Whether the decomposition is optimal — only whether it's defensible.

### Phase 3 — Architecture
- [ ] Can every component be tested in isolation?
- [ ] Where are external dependencies and how are they mocked?
- [ ] Does the architecture reflect the problem domain or what was easy to build?

**Proves:** The system is structurally testable and the design is intentional.
**Doesn't catch:** Whether the architecture handles adversarial conditions. That's Phase 4.

### Phase 3.5 — Discovery Spike (if applicable)
- [ ] Was the assumption validated or disproven?
- [ ] Is the spike code discarded?
- [ ] Is architecture.md updated with the finding?

**Proves:** Unverified assumptions were tested against reality.

### Phase 4 — Threat Model
- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the IAM execution role is compromised, what is the blast radius?
- [ ] Does the IaC have the same threat coverage as the application code?

**Proves:** Every trust boundary has been examined under adversarial conditions.
**Doesn't catch:** Novel attack vectors or zero-days. Use penetration testing and production monitoring.

### Phase 5 — CI/CD Pipeline
- [ ] What does a passing pipeline actually prove?
- [ ] Which gate catches which failure mode?
- [ ] Does the dummy product exercise every component?

**Proves:** The pipeline is designed to verify requirements and mitigate threats.
**Doesn't catch:** Whether gates are correctly implemented (verified when the pipeline runs).

### Phase 6 — Tasks
- [ ] Does every task produce a component the pipeline can validate?
- [ ] Are acceptance criteria tied to specific pipeline gates?
- [ ] Is every task independently testable?
- [ ] Is "done" defined as passing every gate, not working locally?

**Proves:** Work is structured so the pipeline validates each increment.

### Phase 7 — Implementation (per task)
- [ ] All acceptance criteria from tasks.md checked off?
- [ ] Full pipeline passes (not just locally)?
- [ ] Zero new warnings or regressions?

**Proves:** The code meets its acceptance criteria and the pipeline confirms it.
**Doesn't catch:** Production-only failure modes, performance under real load.

### Phase 8 — Production
- [ ] Are production failures being captured and converted into new tests?
- [ ] Are new tests being added to the pipeline?
- [ ] Is the pipeline becoming more comprehensive over time?

**Proves:** The system learns from production.

## Step 4: Output

### Gate Check: Phase [N] — [Name]

| Gate Question | Status | Evidence / Gap |
|--------------|--------|---------------|
| [question] | PASS / FAIL | [what satisfies it or what's missing] |

**If all pass:** "Phase [N] gates pass. Handoff artifact for Phase [N+1] is [artifact]. Consider `/review` for adversarial review before proceeding."

**If any fail:** "Phase [N] has [X] open gates. Address these before proceeding:" then list the specific gaps.

## Style

- Answer gates with specifics from the artifact, not "yes."
- If a gate can't be answered concretely, it's not met.
- A gate you can't answer is a gap you'll pay for later.

## Gotchas

**Rubber-stamps with restated evidence.** The model says "PASS" and quotes the artifact back as evidence. That's not verification — that's echo. Evidence should come from evaluating the artifact against the gate question, not restating what the artifact already says. "Requirements are testable" requires checking each requirement for testability, not noting that the artifact contains a section called "Requirements."

**Defaults to PASS under navigator pressure.** If the navigator says "I think we're ready to move on" before running the gate check, the model anchors to that expectation. Gate checks should be run without signaling the expected outcome. The skill can't fix this — it's a navigator discipline issue — but recognizing the pattern helps.

**Doesn't read upstream artifacts.** Phase 5 gate check should verify that the pipeline covers threat model risks. This requires reading both the pipeline config AND `threat_model.md`. The model often only reads the current phase's artifact and checks gates in isolation. Cross-phase verification is where gate checks are most valuable and most frequently skipped.

**"FAIL" without actionable gaps.** When gates fail, the output should say exactly what's missing and what to do. "FAIL — requirements need more detail" is not actionable. "FAIL — requirement R3 ('system handles high load') has no testable threshold. Define a specific number (requests/second, P95 latency)" is actionable.

**Skips Phase 3.5 gate entirely.** The Discovery Spike gate exists but is optional, so the model almost always skips it even when the architecture contains unverified assumptions. If architecture.md mentions "assuming the API supports X" or "pending confirmation of Y," Phase 3.5 should be triggered, not skipped.

**Runs full gate verification on minor phase transitions.** A brownfield change moving from Phase 4 to Phase 5 doesn't need full cross-phase verification of every upstream artifact. Verify the change decomposition is still accurate, the scoped threat model covers the right areas and seams, and move on. Full verification is for full-system runs.

**Skips Phase 2.5 gates entirely.** When `decomposition-map.md` or `change-decomposition.md` exists, the gate check should include Phase 2.5 gates. The model often jumps from Phase 2 gates straight to Phase 3 gates, missing the decomposition verification.
