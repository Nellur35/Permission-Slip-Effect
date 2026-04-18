---
name: decomposition
description: >
  Decompose a system into sub-projects with explicit seams and
  testing domains. Reads requirements.md (greenfield) or an existing
  decomposition-map.md plus a change description (brownfield), applies
  activation triggers, and produces decomposition-map.md or
  change-decomposition.md. Activates when the user enters Phase 2.5,
  asks to decompose a system, runs /decomposition, or when the methodology
  skill routes here because complexity thresholds fired.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Project Decomposition — Phase 2.5

Decompose a system into sub-projects with explicit seams and testing-domain assignments. Works for both greenfield (new systems) and brownfield (changes to existing systems).

Most non-trivial systems are structurally multiple sub-projects. Architectural thinkers see systems whole and build them whole — the result is projects that are structurally N sub-projects built as one system, with integration bugs proliferating at seams that were never explicitly modeled. Phase 2.5 exists to force the split before Phase 3.

## Step 1: Detect Mode

Glob for `decomposition-map.md` at project root.

**If `decomposition-map.md` exists -> Brownfield Mode.** A prior decomposition exists. This invocation is scoping a change against it. Skip to the Brownfield section below.

**If no `decomposition-map.md` but `requirements.md` exists -> Greenfield Mode.** Proceed to Step 2.

**If neither exists:** "No `requirements.md` found. Phase 2.5 needs a requirements doc to decompose from. Run Phase 2 first, or point me to your requirements doc."

## Step 2: Check Activation Triggers (Greenfield)

Phase 2.5 runs when EITHER trigger fires (union semantics):

1. **Complexity threshold.** Is the Phase 0 complexity score >= 15 / 25? If the reasoning pipeline was run, this is in the Phase 0 output. If not, ask the navigator for a quick score or infer from the requirements.

2. **Multi-domain requirements.** Does `requirements.md` span 3 or more of these subsystem domains?
   - Authentication / identity
   - Data storage / persistence
   - User interface / frontend
   - External integrations / APIs
   - Infrastructure / deployment
   - Background processing / queues
   - Security / policy enforcement
   - Observability / telemetry

**If neither trigger fires:** Write a one-paragraph "single project" verdict citing why (low complexity, single domain, contained scope) and state: "Phase 2.5 skipped. `requirements.md` passes directly to Phase 3." Done.

**If either fires:** Proceed to Step 3.

## Step 3: 60-Second Exit (Single-Project Verdict)

Before decomposing, answer one question:

> "Could this system be built by a single team treating the whole thing as one integrated codebase without coordination overhead, and still ship on budget?"

- **Yes** -> Write a one-paragraph single-project verdict in `decomposition-map.md` and proceed to Phase 3. A triggered-but-unified system (e.g., a sophisticated algorithm implementation) is the correct outcome here, not a failure path.
- **No or unsure** -> Proceed to Step 4.

## Step 4: Identify Candidate Components

List every distinct capability in `requirements.md`. Group related capabilities. Each group is a candidate sub-project.

For each candidate, draft:
- A one-sentence scope
- What it exposes (interface)
- What it consumes (dependencies)

Be generous at this stage. Over-merging later is easier than discovering missed sub-projects mid-architecture.

## Step 5: Apply the Five Independence Tests

For each candidate, answer:

1. **Team independence test.** Could a different team build and ship this component with only the defined interface as the contract? No daily coordination required?

2. **Threat surface test.** Does this component's threat model differ materially from the rest of the system? Different adversaries, different trust boundaries, different attack surfaces?

3. **Failure mode test.** When this component fails, is the failure class distinct from the rest of the system? (e.g., provider timeout vs. parser malformed-input vs. gate misconfiguration)

4. **Consumer test.** Does this component face a distinct consumer (external API, human user, another service) with its own contract?

5. **Release-cycle test.** Could this component be versioned and released independently of the others, or does it only make sense in lockstep?

**A "yes" to at least three questions = separate sub-project.** Fewer than three yeses: merge the candidate with an adjacent one.

Record the pass/fail for each candidate. The "independence evidence" field in the output artifact is this record.

## Step 6: Define Seams

For every pair of sub-projects that communicate, answer:

1. What data crosses the seam? (Shape, volume, sensitivity)
2. What trust assumptions exist? (What does each side assume about the other?)
3. What happens when one side fails? (Graceful degradation? Cascade? Silent failure?)

The seam inventory is as important as the sub-project list. Seams that aren't written down don't get threat-modeled.

## Step 7: Assign Testing Domains

For each sub-project, consult the [Testing Domains Reference](../../../methodology/testing-domains-reference.md), Section 12.2:

1. Classify the sub-project type (library, web service, LLM agent, microservice, data pipeline, UI)
2. Look up recommended domains for that type
3. Add domains specific to the sub-project's threat surface (e.g., reliability domain for a sub-project calling external APIs; PBT for security-critical logic)

For the **integration sub-project** (required when N > 1), always include:
- Integration testing (seam-level)
- Contract testing
- Seam security testing
- Failure injection

Record recommended domains in each sub-project's entry. These assignments feed Phase 5 gate selection directly.

## Step 8: Write `decomposition-map.md`

Use the template at `methodology/templates/phase-2.5-decomposition.md`.

Required sections:

- **Decomposition Verdict** — "Single project" with paragraph, or "N sub-projects" with list
- **Activation trigger that fired** — which of the two (or manual invocation)
- **Per Sub-project** (N blocks):
  - Scope (one paragraph)
  - External interfaces
  - External dependencies
  - Threat surface
  - Recommended testing domains (with brief rationale)
  - Methodology track (full / scoped / minimal viable)
  - Sequencing (blocking / dependent / parallel-safe)
  - Independence evidence (which 3+ of 5 tests passed)
- **Integration Sub-project** (required when N > 1):
  - Scope (seams between sub-projects)
  - Seam inventory table (pair, data crossing, trust assumptions)
  - Seam testing domains
  - Seam threat model scope (which seams Phase 4 will explicitly model)
- **Decisions & Rejected Alternatives** — why this decomposition over alternatives

## Brownfield Mode

When `decomposition-map.md` already exists and the invocation is scoping a change:

### Step B1: Load Existing Decomposition

Read `decomposition-map.md`. Identify which sub-projects and seams already exist.

### Step B2: Check Brownfield Activation

Run Phase 2.5 in brownfield mode when any of these apply:

- Change crosses an existing sub-project boundary
- Change introduces a new external dependency
- Change modifies an existing seam (interface between sub-projects)
- Navigator explicitly invoked `/decomposition`

If none apply and the change is contained within a single sub-project, state: "Change stays within [sub-project name]. Brownfield Phase 2.5 not needed. Run scoped methodology on [sub-project]." Done.

### Step B3: Map Change to Sub-projects

Which sub-projects does this change touch? Does it cross any seams? Produce a table:

| Sub-project | How Affected | Seams Crossed |
|------------|-------------|---------------|
| [name] | [added / modified / replaced / removed behavior] | [list of crossed seams] |

### Step B4: Classify the Outcome

Exactly one of:

1. **Change stays within one sub-project** -> Scoped methodology on that sub-project only. Low overhead.
2. **Change crosses an existing seam** -> Scoped methodology on each affected sub-project + seam threat model for the crossed seam(s). Medium overhead.
3. **Change creates a new seam** (new integration point, new dependency) -> Scoped methodology on affected sub-projects + full seam threat model for the new seam. Higher overhead.

### Step B5: Check for Stale Map

Ask: "Does this change touch a component not listed in the existing `decomposition-map.md`?"

**If yes -> the map is stale.** Stop. Update `decomposition-map.md` first using Steps 4-8 above, then return to Step B1. A stale map produces visibly wrong output from every downstream phase — fix it at the source.

### Step B6: Write `change-decomposition.md`

Use the Brownfield Extension section of the Phase 2.5 template. Output includes:
- Change description
- Affected sub-projects (table)
- Seams crossed (table)
- Brownfield outcome (1, 2, or 3)
- Stale-map check result
- Seam threat model requirements

## Gate Questions — Do Not Hand Off Until Answered

- [ ] Does the decomposition have a crisp answer to "what is the seam threat model going to cover"?
- [ ] Does every sub-project have an identifiable consumer (human, other sub-project, or external system)?
- [ ] Does the integration sub-project have explicit boundaries? (Not "wire things together" but "these specific interfaces, these specific failure modes.")
- [ ] Is the decomposition the simplest that could work? (Defense against over-decomposition: if any two sub-projects have identical threat surfaces and consumers, merge them.)
- [ ] Does every sub-project have recommended testing domains assigned?
- [ ] **[Brownfield]** Does this change touch a component not in the existing `decomposition-map.md`? If yes, the map was stale and has now been updated.
- [ ] **[Brownfield]** Does the existing seam threat model cover the seam(s) this change crosses? If no, the seam threat model is on Phase 4's worklist.

If any answer is missing or vague, go back and fill it in. The cost of answering now is far lower than the cost of discovering the gap in Phase 4 or Phase 7.

## Handoff

**Greenfield, N = 1 (single-project verdict):**
"Single-project verdict recorded. `requirements.md` is your handoff artifact for Phase 3."

**Greenfield, N > 1:**
"`decomposition-map.md` is written with [N] sub-projects plus an integration sub-project. Phase 3 (Architecture) will now run [N+1] times — once per sub-project and once for the integration. Phase 4 (Threat Model) is mandatory per sub-project AND for the seams. Run `/review` on the decomposition before proceeding."

**Brownfield:**
"`change-decomposition.md` is written. Outcome: [1 / 2 / 3]. Downstream phases run in scoped mode on [list of affected sub-projects][, plus seam threat model for [list of seams] if outcome is 2 or 3]. Run `/gate-check` after each affected phase to verify scope didn't expand."

## Style

- **Be specific.** "This is a separate sub-project because it's different" is not evidence. "This passes team independence (a different team could ship with just the protocol), threat surface (distinct: external API trust), and failure mode (distinct: API timeouts vs. parser errors)" is evidence.
- **Prefer merging when in doubt.** Over-decomposition is harder to undo than under-decomposition. A merged sub-project can be split later if seams emerge; split sub-projects that should have been one carry coordination cost forever.
- **Name the integration sub-project explicitly.** When N > 1, the integration sub-project is REQUIRED. It's where seam bugs live. Do not skip it.

## Gotchas

**Over-decomposition.** Splitting too aggressively creates coordination overhead. The team-independence test is the defense: if you can't imagine a different team building the sub-project, it's not a sub-project. If two candidates have identical threat surfaces and identical consumers, they should be merged.

**Missing integration sub-project.** When N > 1, integration work becomes everyone's implicit responsibility and nobody's explicit one. The integration sub-project is REQUIRED when N > 1 — not "nice to have." Seams that aren't owned are seams that get bugs.

**Decomposition drift.** Sub-projects evolve; the map becomes a lie. The defense is that `decomposition-map.md` is a handoff artifact consumed by Phase 3-7. If it drifts, downstream phases produce visibly wrong output. In brownfield mode, the stale-map check (Step B5) is the enforcement point — never skip it.

**Premature decomposition.** Forcing decomposition on work that isn't actually N projects. The 60-second exit path (Step 3) is the defense. A complex-but-unified problem (a single sophisticated algorithm, a contained library) correctly exits with a single-project verdict.

**Skipping testing-domain assignment.** The temptation is to list sub-projects and move on. But Phase 5 gate selection is downstream — if testing domains aren't assigned here, Phase 5 starts from scratch and misses the per-sub-project signal. Always complete Step 7.

**Treating the integration sub-project as documentation.** The integration sub-project is a REAL sub-project with its own architecture, threat model (the seam threat model), and testing gates. If it's treated as a summary of the others, the seam bugs proliferate. Every seam in the inventory gets its own row in the seam threat model.

**Brownfield: ignoring the stale-map check.** The easiest way to corrupt a decomposition map is to scope a change against it without checking whether the change touches unlisted components. The stale-map check in Step B5 is cheap and non-negotiable.
