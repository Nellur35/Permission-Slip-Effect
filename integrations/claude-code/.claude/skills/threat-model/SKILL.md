---
name: threat-model
description: >
  Generate a structured threat model from an architecture document.
  Reads architecture.md from the project, examines every trust
  boundary, and produces threat_model.md. Activates when the user
  asks for threat modeling, enters Phase 4, or wants to analyze
  security risks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Threat Model — Phase 4

Generate a threat model from an architecture document.

## Step 1: Find the Architecture

Glob for:
- `architecture.md`
- `docs/architecture.md`
- `docs/architecture/*`

If nothing found: "No architecture.md found. Threat modeling needs an architecture document. Run Phase 3 first, or point me to your architecture doc."

Read the architecture document.

## Step 1.5: Detect Scope Mode

Glob for `change-decomposition.md` or `decomposition-map.md` at project root. Also check for legacy `change-surface.md`.

**If `change-decomposition.md` exists → Brownfield Mode.** Read it. The threat model covers only the areas the change touches, PLUS a seam threat model for any seams the change crosses.

From the change decomposition, identify:
- Which sub-projects are affected → run threat model scoped to those sub-projects
- Which seams are crossed → run seam threat model for each crossed seam (what data crosses, what trust assumptions exist, what happens when one side fails)
- Which of the 14 areas are relevant based on the affected sub-projects

For areas not touched by the change: one line — "Not affected by this change. Verify if scope expands." Do not fill boilerplate.

**If `decomposition-map.md` exists (greenfield with decomposition) → Per-Sub-project Mode.** The threat model runs N+1 times: once per sub-project + once for seams. Each sub-project's threat model focuses on its specific threat surface. The seam threat model covers every pair of communicating sub-projects from the seam inventory.

**If neither exists → Full Mode.** Proceed to Step 2 as normal — all 14 areas.

**Scope expansion trigger:** If examining the relevant areas reveals risks in areas you initially excluded, add them. The decomposition is the starting scope, not the final scope.

## Step 2: Examine Every Area

For every component and trust boundary, answer:
1. What does an adversary see here?
2. What can they manipulate?
3. What is the worst outcome?
4. How would this be abused at scale?

Work through every area below. Don't skip areas because they seem unlikely -- the ones you skip are the ones attackers find.

| Area | Questions |
|------|-----------|
| Trust Boundaries | Where does control pass between components? Who is trusted? |
| Data Flows | Where does sensitive data travel? Who can intercept it? |
| Authentication | How does the system know who it's talking to? |
| Authorization | How does the system decide what is allowed? |
| External Dependencies | What if a dependency is compromised or unavailable? |
| Error Handling | Do error messages leak sensitive information? |
| Infrastructure & Cloud | Are execution roles, parameter stores, KMS keys explicitly scoped or implicitly broad? |
| IAM Blast Radius | If this execution role is hijacked, what's the worst case? What does it access beyond what it needs? |
| IaC & Configuration | Can a misconfigured parameter or security group bypass all app-level controls? |
| Runtime Security | What happens after deployment? Container escape, SSRF, memory corruption? |
| Secrets Lifecycle | How are secrets provisioned, rotated, revoked? Blast radius if leaked? |
| Data Lifecycle | Where does data live, move, die? Is deletion real or soft? Who has access at each stage? |
| Supply Chain | Are dependencies, CI/CD actions, IaC modules, build plugins pinned? Could the LLM introduce compromised code? |
| LLM-Specific | Prompt injection via generated code? Hallucinated dependencies? Insecure defaults from training data? Confidence without verification? Training data leakage (keys, URLs)? |

In cloud environments, the application code is often the least interesting target. Misconfigured IAM roles, exposed parameter stores, or infrastructure that was never threat modeled -- that's where the damage happens.

## Step 3: Write threat_model.md

Write the output using these sections:

### 1. Threat Context
1-2 paragraphs: what makes this system interesting to an adversary, worst case if compromised.

### 2. Trust Boundary Diagram
ASCII diagram showing trust boundaries and data flow directions.

### 3. Threat Analysis by Trust Boundary
For each boundary:

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [specific threat] | High/Med/Low | High/Med/Low | [specific mitigation] |

### 4. IAM / Execution Role Blast Radius

| Role | Permissions | Blast Radius if Compromised | Mitigation |
|------|------------|---------------------------|------------|

### 5. Error Handling & Information Leakage

| Component | Risk | Mitigation |
|-----------|------|------------|

### 6. Runtime Security

| Component | Risk | Mitigation |
|-----------|------|------------|

### 7. Secrets Lifecycle

| Secret | Provisioning | Rotation | Blast Radius if Leaked |
|--------|-------------|----------|----------------------|

### 8. Data Lifecycle

| Data Type | At Rest | In Transit | Deletion | Access Control |
|-----------|---------|-----------|----------|---------------|

### 9. Supply Chain

| Dependency Type | Risk | Mitigation |
|----------------|------|------------|

### 10. Gate Verification

Before finalizing, answer explicitly:
- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the execution role is compromised, what is the blast radius?
- [ ] Does the infrastructure have the same threat coverage as the application code?

If any answer is missing or vague, go back and fill it in.

## Handoff

"threat_model.md is written. This is the handoff artifact for Phase 5 (CI/CD Pipeline Design). Run `/review` for adversarial review before proceeding."

## Style

- Be specific. "Data could be intercepted" is not a threat. "Unencrypted PII in transit between the API gateway and the Lambda can be intercepted via a compromised VPC endpoint" is a threat.
- Don't skip areas. Don't soften findings.
- Treat infrastructure with the same rigor as application code.

## Gotchas

**"Standard mitigations apply" on half the areas.** The template has 13+ areas. The model fills all 13 but treats 5-7 as boilerplate: "Low risk. Use standard encryption/authentication/input validation." If the mitigation column doesn't reference a specific component from the architecture, it's filler. Every mitigation must name what it applies to.

**Skips infrastructure for code-heavy architectures.** If the architecture doc focuses on application code and only mentions infrastructure briefly, the model mirrors that emphasis. IAM blast radius, IaC configuration, and runtime security get shallow treatment. The areas the architecture doc spends the least time on are usually the most dangerous — the model should spend more time there, not less.

**Produces threats the architecture doesn't have.** The model sometimes generates textbook threats that don't apply to the actual system. "SQL injection" for a system that doesn't use SQL. "Container escape" for a serverless architecture. Every threat must trace to a specific component in the architecture. If the architecture doesn't have containers, there's no container escape threat.

**Misses the LLM-specific area.** Area 14 (LLM-Specific) was added because AI-assisted development introduces supply chain risks the model doesn't naturally consider — hallucinated dependencies, insecure code suggestions, prompt injection via generated code. The model frequently skips this area or treats it as "N/A" even when the project is being built with AI tools. If you're using this methodology, you're using AI tools. This area is never N/A.

**Trust boundary diagram is decorative.** The ASCII diagram often doesn't match the threat analysis that follows. Components appear in the diagram but not the threat table, or vice versa. The diagram should be the source of truth — every component and boundary in the diagram gets a row in the threat analysis. If the counts don't match, something was skipped.

**Brownfield mode excludes too aggressively.** The change decomposition says "authentication" so the model only examines authentication. But adding auth introduces secrets (Secrets Lifecycle), changes IAM roles (IAM Blast Radius), and adds a token store (Data Lifecycle). Each area the model excludes is an area an attacker might find first. When in doubt, include the area with a brief analysis rather than exclude it. Phase 2.5 brownfield's seam identification helps here — crossed seams force examination of adjacent areas.

**Full 14-area treatment on brownfield changes.** The change touches authentication but the model fills all 14 areas anyway, most with "low risk — standard mitigations." This wastes tokens and dilutes the real findings. In brownfield mode, cover only the areas the change decomposition identifies. Mark excluded areas with "not affected by this change" — one line, not a paragraph.

**Misses seam threat model when decomposition exists.** When `decomposition-map.md` or `change-decomposition.md` specifies seams, the seam threat model is mandatory — not optional. The model sometimes produces per-sub-project threat models but skips the seam-specific analysis. Seam bugs are where most integration failures live.
