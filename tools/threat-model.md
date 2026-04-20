# Threat Model Tool

Generate a structured threat model from an architecture document.

**Input:** Paste your `architecture.md` (or describe your system's components, boundaries, and data flows).
**Output:** A complete `threat_model.md` ready for use.

This tool is a **surfacing tool, not a verdict.** It enumerates a threat surface — risks, impacts, candidate mitigations. A navigator (or a subsequent analysis prompt) then decides which mitigations to implement, which risks to accept, and which trust boundaries need deeper review.

---

## Instructions

Read the architecture input. For every component and trust boundary, answer these four questions:

1. What does an adversary see here?
2. What can they manipulate?
3. What is the worst possible outcome?
4. How would this be abused at scale?

Work through every area in the table below. Do not skip areas because they seem unlikely. The areas you skip are the ones attackers find.

## Areas to Examine

| Area | Questions to Ask |
|------|-----------------|
| Trust Boundaries | Where does control pass between components? Who is trusted? |
| Data Flows | Where does sensitive data travel? Who can intercept it? |
| Authentication | How does the system know who it is talking to? |
| Authorization | How does the system decide what is allowed? |
| External Dependencies | What happens if a dependency is compromised or unavailable? |
| Error Handling | Do error messages leak sensitive information? |
| Infrastructure & Cloud Boundaries | Are execution roles, parameter stores, and KMS keys explicitly scoped or implicitly broad? |
| IAM Blast Radius | If this execution role is hijacked, what is the worst case? What does it have access to beyond what it needs? |
| IaC & Configuration | Are infrastructure definitions version-controlled and scanned? Can a misconfigured SSM parameter or overly permissive security group bypass all application-level controls? |
| Runtime Security | What happens after deployment? Container escape, SSRF, memory corruption, side-channel attacks? |
| Secrets Lifecycle | How are secrets provisioned, rotated, and revoked? What is the blast radius if a secret leaks? |
| Data Lifecycle | Where does data live, move, and die? Is deletion real or soft? Who has access at each stage? |
| Supply Chain | Are dependencies, CI/CD actions, IaC modules, build plugins, and dev tooling pinned? Could the LLM itself introduce compromised code? |
| LLM-Specific Risks | Prompt injection via generated code? Hallucinated (non-existent) dependencies? Insecure defaults copied from training data? Model-introduced logic flaws that pass basic tests? Leaked API keys or internal URLs from training data? |

**Cloud reality check:** In modern cloud environments, the application code is often the least interesting target. Catastrophic failures happen in misconfigured IAM roles, exposed parameter stores, or infrastructure that was never threat modeled. Treat infrastructure with the same adversarial rigor as the application.

## Output Format

Structure the output as follows:

### 1. Threat Context
1-2 paragraphs: What makes this system interesting to an adversary? What is the worst thing that can happen if the system is compromised?

### 2. Trust Boundary Diagram
ASCII diagram showing all trust boundaries and data flow directions.

### 3. Threat Analysis by Trust Boundary
For each trust boundary, a table:

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [specific threat] | High/Medium/Low | High/Medium/Low | [specific mitigation] |

### 4. IAM / Execution Role Blast Radius

| Role | Permissions | Blast Radius if Compromised | Mitigation |
|------|------------|---------------------------|------------|
| [role] | [permissions] | [worst case] | [scope reduction] |

### 5. Error Handling & Information Leakage

| Component | Risk | Mitigation |
|-----------|------|------------|
| [component] | [what leaks] | [how to prevent it] |

### 6. Runtime Security

| Component | Risk | Mitigation |
|-----------|------|------------|
| [component] | [post-deploy risk] | [control] |

### 7. Secrets Lifecycle

| Secret | Provisioning | Rotation | Blast Radius if Leaked |
|--------|-------------|----------|----------------------|
| [secret] | [how created] | [how rotated] | [worst case + scope reduction] |

### 8. Data Lifecycle

| Data Type | At Rest | In Transit | Deletion | Access Control |
|-----------|---------|-----------|----------|---------------|
| [type] | [encryption] | [transport security] | [hard/soft delete] | [who can access] |

### 9. Supply Chain

| Dependency Type | Risk | Mitigation |
|----------------|------|------------|
| [packages/images/actions/IaC modules/LLM code] | [specific risk] | [pinning, scanning, review] |

### 10. Mitigation-to-Testing Mapping (optional)

For each mitigation, identify the testing domain that would catch its failure. A mitigation without a way to test whether it still holds is documentation, not a control. If the consuming workflow defines a specific testing taxonomy (e.g., the sibling [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) has one), use that. Otherwise, a simple pairing is enough:

| Mitigation | Testing Domain | Specific Gate/Tool |
|-----------|---------------|-------------------|
| [e.g., Input validation on all API endpoints] | [e.g., Security (SAST) + Correctness (PBT)] | [e.g., semgrep rules + Hypothesis property tests] |
| [e.g., Token expiry enforced at 15 min] | [e.g., Correctness (integration) + Security] | [e.g., Integration test: expired token rejected] |

### 11. Gate Verification

Before finalizing, answer these questions explicitly:

- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the execution role is compromised, what is the blast radius?
- [ ] Does the infrastructure have the same threat coverage as the application code?
- [ ] Does every mitigation map to a testing domain and a specific gate?

If any answer is missing or vague, go back and fill it in. These are the exit criteria.

---

## What This Catches and What It Does Not

**Catches:** Architectural security gaps, missing controls at trust boundaries, over-permissioned roles, unencrypted data flows, supply chain risks, secrets management gaps.

**Does not catch:** Implementation bugs, logic errors in code, zero-day vulnerabilities in dependencies, social engineering vectors, physical security. Those require code review, penetration testing, and operational security practices.

---

*End of output: the resulting `threat_model.md` is surfaced material for the navigator. Whatever the navigator accepts from it carries forward; what they reject, reframe, or defer also carries forward as explicit decisions. The artifact's purpose is to make those decisions conscious, not to make them for you.*
