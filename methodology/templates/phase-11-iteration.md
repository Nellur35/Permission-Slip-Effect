# Phase 11 — Iteration & Evolution

**Input:** Phase 8 production feedback + ongoing development
**Maturity level:** [Level 0 / 1 / 2 / 3 — see lifecycle-phases-8-12.md]

## Iteration Log

### Iteration N: [Change Name]

**Date:** [When started]
**Trigger:** [feedback | incident | strategic decision | tech debt | dependency update]
**Source:** [e.g., Phase 8 finding #3 / user request / CVE-2025-XXXX]
**Scope:** [Which sub-projects affected — from Phase 2.5 brownfield decomposition]
**Brownfield outcome:** [1: within sub-project / 2: crosses seam / 3: creates new seam]
**Status:** [planned | in-progress | completed | abandoned]

**What changed:**
[Brief description]

**What broke (if anything):**
[Regressions, unexpected side effects]

---

## Technical Debt Register

### Debt Item 1: [Name]

**What:** [The shortcut that was taken]
**Why:** [What pressure caused it]
**Impact:** [What it costs now — time, risk, complexity]
**Cost to fix:** [Estimated effort]
**Priority:** [P0 - blocking / P1 - painful / P2 - annoying / P3 - nice-to-have]
**Deadline:** [When this must be addressed]
**Owner:** [Navigator or agent responsible]
**Status:** [ ] Resolved

---

### Debt Item 2: [Name]

[Same structure]

---

## Version History (CHANGELOG)

### [Version] — [Date]

**Added:**
- [New feature or capability]

**Changed:**
- [Modified behavior]

**Fixed:**
- [Bug fix]

**Breaking:**
- [Breaking change — link to migration guide]

---

## Migration Guides

### Migration: [From version] → [To version]

**What changed:** [Specific breaking change]
**Who is affected:** [Which users/consumers]
**Migration steps:**
1. [Step]
2. [Step]

**Deadline:** [When old behavior is removed]

---

## Gate Questions

- [ ] Does every change have a clear triggering input?
- [ ] Does the change use Phase 2.5 brownfield decomposition?
- [ ] Is technical debt being tracked and addressed?
- [ ] Are breaking changes communicated with migration paths?
- [ ] Are version numbers meaningful?

---

*Iteration is the primary operating mode after first deployment. Every change runs through Phase 2.5 brownfield decomposition. This file is the record of how the system evolves.*
