# Phase 2.5 — Project Decomposition Map

**Input:** Phase 2 `requirements.md`

**Mode:** [Greenfield / Brownfield]

## Decomposition Verdict

[One of: "Single project" (with one-paragraph justification) or "N sub-projects" (proceed to sections below)]

**Activation trigger that fired:** [Complexity score >= 15 / 3+ distinct subsystem domains / Navigator invoked manually]

---

## Sub-project 1: [Name]

**Scope:** [One-paragraph bounded description of what it does]

**External interfaces:** [What it exposes — APIs, protocols, function signatures]

**External dependencies:** [What it consumes — other sub-projects, external services, libraries]

**Threat surface:** [What an adversary sees at its boundaries — distinct from the rest of the system]

**Recommended testing domains:**
- [ ] [Domain from Testing Domains Reference, e.g., "Correctness (unit + PBT)" — with brief rationale]
- [ ] [e.g., "Security (SAST + SCA)" — because this sub-project handles auth tokens]
- [ ] [e.g., "Reliability (timeout verification)" — because this sub-project calls external APIs]

**Methodology track:** [full | scoped | minimal viable]

**Sequencing:** [blocking / dependent on Sub-project X / parallel-safe]

**Independence evidence:** [Which of the 5 core questions this sub-project passed, briefly]

**Example:**

> **Sub-project 1: Provider — LLM Abstraction**
>
> **Scope:** Wraps LLM API calls behind a Provider protocol. Handles auth, rate limiting, retries, fallback between models.
>
> **External interfaces:** `Provider.complete(prompt) -> str`, `Provider.embed(text) -> list[float]`
>
> **External dependencies:** OpenAI API, Anthropic API, local Ollama instance
>
> **Threat surface:** External API trust (keys, rate limits, response integrity), model output injection
>
> **Recommended testing domains:**
> - [x] Correctness (unit + integration) — mock providers for unit, real API for integration
> - [x] Security (SAST + secret scanning) — API keys must never leak
> - [x] Reliability (failure injection + timeout) — API failures must degrade gracefully
> - [x] Observability (trace completeness) — every API call must emit a span
>
> **Methodology track:** full
>
> **Sequencing:** blocking — reasoning and harness depend on this
>
> **Independence evidence:** Passes team independence (different team could build this with just the protocol), threat surface (distinct: external API trust), failure mode (distinct: API timeouts vs. parser errors), consumer (reasoning + harness)

---

## Sub-project 2: [Name]

[Same structure as Sub-project 1]

---

## Sub-project N: [Name]

[Same structure as Sub-project 1]

---

## Integration Sub-project (required when N > 1)

**Scope:** The seams between sub-projects — wiring, composition, end-to-end flow. This is where integration bugs live.

**Seam inventory:**

| Sub-project A | Sub-project B | Data Crossing Seam | Trust Assumptions |
|--------------|--------------|-------------------|-------------------|
| [e.g., Provider] | [e.g., Reasoning] | [e.g., Completion requests/responses] | [e.g., Reasoning trusts Provider to return string-shaped output] |
| [e.g., Gate] | [e.g., Tools] | [e.g., ToolCall classification requests, Decisions] | [e.g., Tools trust Gate to classify before every high-risk op] |

**Seam testing domains** (from [Testing Domains Reference, Section 15](../testing-domains-reference.md)):
- [ ] Integration testing — seam-level tests for every pair in the inventory above
- [ ] Contract testing — verify each sub-project honors its declared interface
- [ ] Seam security testing — data validation at boundaries, trust assumption verification
- [ ] Failure injection — what happens when one side of a seam fails?
- [ ] Serialization round-trip — for seams that serialize/deserialize data

**Methodology track:** scoped mode, focused on integration concerns

**Seam threat model scope:** [List which seams will get explicit threat modeling in Phase 4. Every seam in the inventory should be covered.]

---

## Brownfield Extension (if applicable)

*Use this section instead of the above when applying Phase 2.5 to changes on an existing system.*

### Change Description

[What is being changed and why]

### Affected Sub-projects

| Sub-project | How Affected | Seams Crossed |
|------------|-------------|---------------|
| [e.g., Identity] | [e.g., OAuth2 replaces password auth] | [e.g., Identity ↔ Session, Identity ↔ External IdP (new)] |
| [e.g., Sessions] | [e.g., Refresh token lifecycle added] | [e.g., Session ↔ Identity] |

### Brownfield Outcome

[One of:]
1. **Change stays within one sub-project** → Run scoped methodology on that sub-project only
2. **Change crosses an existing seam** → Scoped methodology on each affected sub-project + seam threat model for crossed seam(s)
3. **Change creates a new seam** → Scoped methodology on affected sub-projects + full seam threat model for new seam

### Stale Map Detection

- [ ] Does this change touch a component not in the existing `decomposition-map.md`? If yes, update the map first.
- [ ] Does the existing seam threat model cover the seam(s) this change crosses? If no, generate one.

---

## Gate Questions

- [ ] Does the decomposition have a crisp answer to "what is the seam threat model going to cover"?
- [ ] Does every sub-project have an identifiable consumer (human, other sub-project, or external system)?
- [ ] Does the integration sub-project have explicit boundaries? (Not "wire things together" but "these specific interfaces, these specific failure modes.")
- [ ] Is the decomposition the simplest that could work? (If any two sub-projects have identical threat surfaces and consumers, they should probably be merged.)
- [ ] Does every sub-project have recommended testing domains assigned?
- [ ] [Brownfield only] Does this change touch components not in the existing decomposition map?

## Decisions & Rejected Alternatives

| Decision | Alternative Rejected | Reason |
|----------|---------------------|--------|
| [e.g., 6 sub-projects + integration] | [e.g., 3 larger sub-projects] | [e.g., Gate and Tools have distinct threat surfaces; merging them hides the permission-bypass seam bug class] |
| [e.g., Single project verdict] | [e.g., Decompose into 2] | [e.g., Both candidates share identical consumers and threat surfaces; decomposition adds coordination cost without security benefit] |

---

*This file is the sole input to Phase 3 (along with `requirements.md`). Everything not written here does not carry forward. When N > 1, Phase 3 runs N+1 times using this decomposition.*
