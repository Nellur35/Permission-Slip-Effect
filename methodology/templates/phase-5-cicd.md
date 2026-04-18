# Phase 5 — CI/CD Pipeline Design

**Input:** Phase 4 `threat_model.md`

## Pipeline Overview

| Job | Purpose | Blocks Merge? | Mapped Threat | Testing Domain |
|-----|---------|--------------|---------------|----------------|
| Lint + Type Check | Code quality, catch obvious errors | Yes | — | Domain 2: Type Safety |
| Unit Tests | Verify component behavior in isolation | Yes | — | Domain 1: Correctness |
| Property-Based Tests | Correctness properties across random inputs | Yes | Logic flaws in security code | Domain 1: Correctness (PBT) |
| Security Scan (SAST) | Static analysis for vulnerabilities | Yes | Trust boundaries 1-3 | Domain 3: Security |
| Dependency Scan (SCA) | Known CVEs in dependencies | Yes | Supply chain | Domain 3: Security (SCA) |
| Secret Scan | Detect hardcoded credentials | Yes | Information leakage | Domain 3: Security |
| [IaC Scan] | [Misconfigurations in Terraform/CFN] | [Yes] | [Trust boundary 3] | Domain 3: Security (IaC) |
| [Integration Tests] | [Components working together] | [Yes] | [Trust boundary 2] | Domain 1: Correctness (Integration) |

## Job Details

### Job 1: Lint + Type Check

```yaml
# Example GitHub Actions step
- name: Lint
  run: ruff check .
- name: Type check
  run: mypy src/
```

**What a pass proves:** Code follows style conventions. No type errors in annotated code.
**What a pass does NOT prove:** Code is correct, secure, or complete.

### Job 2: Unit Tests

```yaml
- name: Unit tests
  run: pytest tests/ --cov=src --cov-fail-under=80
```

**Coverage threshold:** [X]% — set based on risk, not vanity.
**What a pass proves:** Individual components behave correctly with mocked dependencies.
**What a pass does NOT prove:** Components work together. System handles real-world inputs.

### Job 3: Security Scan (SAST)

```yaml
- name: SAST
  run: semgrep scan --config=auto src/
```

**What a pass proves:** No known vulnerability patterns in source code.
**Mapped to threat model:** [Which trust boundaries this gate protects]

### Job 4: Dependency Scan (SCA)

```yaml
- name: SCA
  run: pip-audit --strict
```

**What a pass proves:** No known CVEs in pinned dependencies.
**Waiver:** [If applicable — e.g., upstream CVEs with no available fix. Document per waiver pattern.]

### Job 5: Secret Scan

```yaml
- name: Secret scan
  run: gitleaks detect --source=. --verbose
```

**What a pass proves:** No hardcoded secrets, API keys, or credentials in the codebase.

## The Dummy Product

**What it is:** A minimal implementation that exercises every component and passes every gate.

**What it includes:**
- [e.g., A single API endpoint that calls each service component]
- [e.g., A minimal configuration file]
- [e.g., Test fixtures that cover every code path the dummy touches]

**What it proves:** The pipeline itself works end-to-end. A new contributor can clone, install, and see green on first run.

## Waivers

| What | Why | Risk Accepted | Mitigation | Owner | Expiry |
|------|-----|--------------|------------|-------|--------|
| [e.g., pip-audit continue-on-error] | [e.g., Upstream boto3 CVE has no fix] | [e.g., Known CVE, no exploit path in our usage] | [e.g., Monitor upstream, upgrade immediately on fix] | [Name] | [Date] |

## Testing Domain Coverage

**Project type:** [e.g., Python library / Web service / LLM agent / Microservice / Data pipeline]

**Applicable domains** (from [Testing Domains Reference](../testing-domains-reference.md), Section 12.2):

| Domain | Applicable? | Gate(s) Above | Gap? |
|--------|------------|---------------|------|
| 1. Correctness | [Yes/No] | [e.g., Unit Tests, Integration Tests] | [e.g., No PBT yet] |
| 2. Type Safety | [Yes/No] | [e.g., Lint + Type Check] | — |
| 3. Security | [Yes/No] | [e.g., SAST, SCA, Secret Scan] | [e.g., No DAST] |
| 4. Reliability | [Yes/No] | [e.g., —] | [e.g., No timeout verification] |
| 5. Performance | [Yes/No] | [e.g., —] | [e.g., Not applicable for library] |
| 6. Data Integrity | [Yes/No] | [e.g., —] | — |
| 7. Documentation | [Yes/No] | [e.g., —] | — |
| 8. Process | [Yes/No] | [e.g., —] | — |
| 9. Observability / AI | [Yes/No] | [e.g., —] | [e.g., Critical for agent systems] |

**Defense-in-depth assessment:** [X] domains covered out of 9. [Maturity level per Section 12.3].

**Phase 2.5 alignment:** [If decomposition assigned per-sub-project domains, verify each is covered here. List any gaps.]

## Gate Questions

- [ ] What does a passing pipeline actually prove?
- [ ] Which gate catches which failure mode?
- [ ] Does the dummy product exercise every component?
- [ ] Does every threat mitigation map to a testing domain?
- [ ] Are all applicable testing domains for this project type covered?

---

*Pipeline config + dummy product are the inputs to Phase 6. Everything not written here does not carry forward.*
