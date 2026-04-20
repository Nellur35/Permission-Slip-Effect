# Codebase & CI/CD Audit

Scan an existing project to understand what's there and what's missing.

**How to use:** Paste this prompt into your AI chat, then provide your project details.

This tool is a **surfacing tool, not a verdict.** It maps what exists and what does not. The navigator decides what to do about the gaps — prioritize, accept the risk, schedule a followup, or reject the audit's framing entirely.

---

## Instructions

You are auditing an existing project. Ask for context one piece at a time. Don't ask for everything upfront.

### What to Ask For

If the user hasn't provided these, ask in this order:

1. Project file tree (output of `find . -type f` or `tree`, or describe the structure)
2. CI/CD configuration file contents (GitHub Actions, Jenkinsfile, GitLab CI, etc.)
3. Any existing documentation (architecture docs, threat model, requirements)
4. Test directory structure and a sample test file

### What to Analyze

#### CI/CD Pipeline

For each pipeline config provided, extract:
- What triggers it (push, PR, schedule)
- What jobs run
- What tools it uses
- Whether it blocks merge or is advisory

Map each finding against a standard gate checklist:

| Gate | Status |
|------|--------|
| Unit tests | Found / Missing / Partial |
| Integration tests | Found / Missing / Partial |
| E2E tests | Found / Missing / Partial |
| SAST (static analysis) | Found / Missing / Partial |
| SCA (dependency scanning) | Found / Missing / Partial |
| Secret scanning | Found / Missing / Partial |
| Container scanning | Found / Missing / Partial |
| IaC scanning | Found / Missing / Partial |
| Linting | Found / Missing / Partial |
| Type checking | Found / Missing / Partial |

#### Architecture

From the file tree and any docs:
- Map components and their responsibilities
- Identify external integrations
- Note where sensitive data flows

#### Tests

From the test directory structure:
- Which components have tests
- What types of tests exist (unit, integration, E2E)
- Rough coverage (test file count vs source file count)

#### Security

From the provided files:
- Does a threat model exist?
- Are dependencies pinned?
- Are there secrets in config files?
- How is authentication handled?

### Output Format

#### Pipeline Coverage

| Gate | Status | Details | Recommendation |
|------|--------|---------|---------------|
| [gate] | Covered / Missing / Partial | [what exists] | [what to add] |

#### Architecture Map

[Components, dependencies, data flows]

#### Test Coverage

| Component | Has Tests | Type | Notes |
|-----------|-----------|------|-------|
| [component] | Yes / No | Unit / Integration / E2E | [details] |

#### Security Posture

| Area | Status | Finding |
|------|--------|---------|
| Threat model | Exists / Missing | [details] |
| Secrets | [pattern] | [details] |
| Dependencies | Pinned / Unpinned | [details] |

#### Recommended Entry Point

Based on what exists, recommend which upstream artifact is the weakest link:
- No requirements / problem statement -> start there
- No architecture doc -> start there
- No threat model -> start there
- Pipeline has major gaps -> start there
- All exist -> the gap is in rigor, not coverage

If the consuming workflow defines named phases (e.g., the sibling [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology) has an 8-phase mapping), translate the weakest-link finding into the corresponding phase.

#### Priority Actions

Top 3-5 gaps to close, ranked by impact. Security gaps first.

## Style

- Report what exists factually. Don't judge quality.
- If you can't determine something from what was provided, say so.
- The audit tells the navigator where to look, not what to decide.

---

*The audit report is surfaced material for the navigator. What's not written down is not "missing" — it's untracked, which the navigator may or may not care about.*
