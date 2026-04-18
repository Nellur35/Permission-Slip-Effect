# Project Decomposition Tool

Decompose a system into sub-projects with explicit seams and testing domains. Works for both greenfield (new systems) and brownfield (changes to existing systems).

**Input:** `requirements.md` (greenfield) or existing `decomposition-map.md` + change description (brownfield)
**Output:** `decomposition-map.md` (greenfield) or `change-decomposition.md` (brownfield)

---

## When to Use

### Greenfield Triggers (union — either fires Phase 2.5)

1. **Complexity threshold:** Phase 0 complexity score >= 15 out of 25
2. **Multi-domain requirements:** `requirements.md` spans 3+ distinct subsystem domains:
   - Authentication / identity
   - Data storage / persistence
   - User interface / frontend
   - External integrations / APIs
   - Infrastructure / deployment
   - Background processing / queues
   - Security / policy enforcement
   - Observability / telemetry

### Brownfield Triggers (any fires Phase 2.5)

- Change crosses an existing sub-project boundary
- Change introduces a new external dependency
- Change modifies an existing seam (interface between sub-projects)
- Navigator explicitly invokes this tool

### When NOT to Use

If neither greenfield trigger fires, skip. If the system is genuinely one project (a single-purpose library, a simple script), use the 60-second exit path.

---

## How to Use

### Step 1: Quick Verdict (60 seconds)

Answer one question: "Could this system be built by a single team treating the whole thing as one integrated codebase without coordination overhead, and still ship on budget?"

- **Yes** → Document the single-project verdict in one paragraph. Done. Proceed to Phase 3.
- **No or unsure** → Continue to Step 2.

### Step 2: Identify Candidate Components

List every distinct capability in `requirements.md`. Group related capabilities. Each group is a candidate sub-project.

### Step 3: Apply the 5 Core Questions

For each candidate component, answer:

1. **Team independence test.** Could a different team build and ship this component with only the defined interface as the contract?
2. **Threat surface test.** Does this component's threat model differ materially from the rest of the system?
3. **Failure mode test.** When this component fails, is the failure class distinct from the rest?
4. **Consumer test.** Does this component face a distinct consumer with its own contract?
5. **Release-cycle test.** Could this component be versioned and released independently?

A "yes" to any **three** questions = separate sub-project.

### Step 4: Define Seams

For every pair of sub-projects that communicate:
- What data crosses the seam?
- What trust assumptions exist?
- What happens when one side fails?

### Step 5: Assign Testing Domains

For each sub-project, consult the [Testing Domains Reference](../methodology/testing-domains-reference.md), Section 12.2:
1. Classify the sub-project type (library, service, agent, pipeline, UI)
2. Look up recommended domains
3. Add domains specific to the sub-project's threat surface

For the integration sub-project, always include:
- Integration testing (seam-level)
- Contract testing
- Seam security testing
- Failure injection

### Step 6: Write the Decomposition Map

Use the template at `methodology/templates/phase-2.5-decomposition.md`.

---

## Brownfield Mode

For changes to existing systems:

### Step 1: Load Existing Decomposition

Read `decomposition-map.md` if it exists. If not, reconstruct the system's implicit decomposition by identifying existing sub-project boundaries.

### Step 2: Map Change to Sub-projects

Which sub-projects does this change touch? Does it cross any seams?

### Step 3: Classify the Outcome

1. **Change stays within one sub-project** → Scoped methodology on that sub-project only. Low overhead.
2. **Change crosses an existing seam** → Scoped methodology on each affected sub-project + seam threat model for the crossed seam. Medium overhead.
3. **Change creates a new seam** → Scoped methodology on affected sub-projects + full seam threat model for the new seam. Higher overhead.

### Step 4: Check for Stale Map

Does this change touch a component not in the existing `decomposition-map.md`? If yes, the map is stale — update it first.

### Step 5: Write Change Decomposition

Output `change-decomposition.md` listing:
- Affected sub-projects
- Crossed seams
- New seams (if any)
- Seam threat model requirements
- Brownfield outcome classification (1, 2, or 3)

---

## Gate Questions — Do Not Proceed Until Answered

- [ ] Does the decomposition have a crisp answer to "what is the seam threat model going to cover"?
- [ ] Does every sub-project have an identifiable consumer?
- [ ] Does the integration sub-project have explicit boundaries?
- [ ] Is the decomposition the simplest that could work?
- [ ] Does every sub-project have recommended testing domains assigned?
- [ ] [Brownfield] Does the change touch components not in the existing decomposition map?
- [ ] [Brownfield] Does the seam threat model cover every crossed seam?

## Common Failure Modes

- **Over-decomposition.** If you can't imagine a different team building the sub-project, it's not a sub-project. Merge candidates with identical threat surfaces and consumers.
- **Missing integration sub-project.** When N > 1, the integration sub-project is REQUIRED. It's where seam bugs live.
- **Decomposition drift.** If sub-projects evolve and the map isn't updated, downstream phases produce visibly wrong output.
- **Premature decomposition.** Use the 60-second exit for genuinely single projects.
- **Brownfield: stale maps.** If the change touches unlisted components, update the map before proceeding.

---

*Output artifact feeds Phase 3 (Architecture). When N > 1, Phase 3-7 fan out per sub-project plus integration.*
