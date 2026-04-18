# PSE Methodology — Full Lifecycle Coverage

*Phases 8-12 + Staged Evolution Roadmap for AI-Assisted Development*

**Status:** Methodology extension document
**Extends:** `methodology/METHODOLOGY.md`
**Integrates:** Phase 8 (Production Feedback) and beyond
**Audience:** AI agents executing post-implementation phases + navigators reviewing lifecycle coverage

---

## 0. Why This Document Exists

PSE has strong coverage of Phases 1-7 (problem through implementation). Phase 8 (Production Feedback) exists but is thin. Phases 9-12 (operations, observability, iteration, decommissioning) and three cross-cutting concerns (documentation lifecycle, knowledge transfer, dependency management, cost management) are unaddressed.

In AI-assisted development, the navigator is often both builder and operator. If the methodology doesn't cover ops, the navigator either improvises (producing inconsistent results) or ignores it (producing fragile production systems).

This document mirrors the structure of the rest of PSE: phases with gate questions, handoff artifacts, cross-references to other phases. It adds a staged evolution roadmap because ops artifacts at project start should be minimal and evolve as the project matures.

**The principle:** An AI agent executing PSE should produce ops artifacts appropriate to the project's stage. A week-old prototype gets a crude deployment plan and a health-check endpoint. A year-old production system gets full runbook discipline, SLI definition, and incident response procedures.

---

## 1. The Lifecycle Map

### 1.1 Updated Phase List

| Phase | Name | Status |
|-------|------|--------|
| 1 | Define the Problem | Existing |
| 2 | Product Requirements | Existing |
| 2.5 | Project Decomposition | Existing |
| 3 | Architecture & Design | Existing |
| 3.5 | Discovery Spike | Existing |
| 4 | Threat Modeling | Existing |
| 5 | CI/CD Pipeline Design | Existing |
| 6 | Task Breakdown | Existing |
| 7 | Implementation | Existing |
| | **--- build/run boundary ---** | |
| 8 | Production Feedback (expanded) | Updated |
| 9 | Operations & Incident Response | **New** |
| 10 | Observability | **New** |
| 11 | Iteration & Evolution | **New** |
| 12 | Decommissioning | **New** |

### 1.2 Cross-Cutting Concerns

Not phases. Continuous practices across the lifecycle.

| ID | Concern |
|----|---------|
| CC1 | Documentation Lifecycle |
| CC2 | Knowledge Transfer & Onboarding |
| CC3 | Dependency Management |
| CC4 | Cost Management |

### 1.3 Phase Sequencing

Phases 1-7 are sequential with re-entry allowed. Phases 8-11 run in parallel after first production deployment. Phase 12 runs when the system is being retired.

```
1 → 2 → 2.5 → 3 → 3.5 → 4 → 5 → 6 → 7 → (deploy) → 8 ←→ 9 ←→ 10 ←→ 11 → 12
                                                      ↑           ↑
                                                      └── CC1-CC4 ┘
                                                          continuous
```

### 1.4 Maturity Staging

Each ops phase has four maturity levels:

| Level | Name | When |
|-------|------|------|
| 0 | Seed | First deployment; minimum viable ops discipline |
| 1 | Running | Stable operation; basic observability |
| 2 | Growing | Real users; defined SLIs; incident response works |
| 3 | Production | Production discipline; full runbooks; SLOs enforced |

An agent executing these phases picks the level based on the project's actual maturity. A prototype gets Level 0 artifacts. A system with real users gets Level 2. Don't over-engineer for the current stage.

---

## 2. Phase 8 — Production Feedback (Expanded)

**Existing PSE coverage:** "Deploy to a live environment. Monitor for failures the pipeline did not catch. Collect logs. Feed logs back to generate new test cases."

This is correct but treats production as a test-generation source only. Production feedback is richer than that.

### 2.1 Five Feedback Streams

1. **Failure feedback** — errors, exceptions, crashes (existing coverage)
2. **Performance feedback** — latency, throughput, resource use
3. **User feedback** — complaints, feature requests, usage patterns
4. **Security feedback** — detected attacks, abuse patterns, CVE disclosures
5. **Cost feedback** — actual spend vs. projected spend

Each stream has its own handling. Failures feed back into CI as new tests. Performance feeds back into architecture as bottleneck identification. User feedback feeds back into requirements as new Phase 2 inputs.

### 2.2 Gate Questions

- [ ] Is every production failure being captured and converted into a test?
- [ ] Are performance trends being tracked against baselines?
- [ ] Is there a channel for user feedback, and is it being triaged?
- [ ] Are security events being logged and reviewed?
- [ ] Is cost being tracked against projection?

### 2.3 Handoff Artifact

`production-feedback-log.md` — ongoing document, not one-time output.

### 2.4 Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Log errors to file; manual review weekly |
| 1 | Structured error logging + alerting on critical failures |
| 2 | Five feedback streams captured with triage process |
| 3 | Automated categorization; SLI-backed feedback targets |

---

## 3. Phase 9 — Operations & Incident Response

**Purpose:** Define how the system behaves when something goes wrong in production. Who responds, how, and what the response procedure is.

### 3.1 What Phase 9 Covers

- Incident detection — how you know something is wrong
- Incident response — what happens when you know
- Runbooks — written procedures for known incident types
- On-call practices — who responds, when, with what tools
- Escalation — when to pull in additional help
- Post-incident review — RCA applied to production incidents
- Capacity planning — making sure you have enough headroom
- Disaster recovery — what happens when infrastructure fails catastrophically
- Backup and restore — data protection with verified recovery testing

### 3.2 Gate Questions

- [ ] For each component that can fail, is there a runbook for how to respond?
- [ ] Is there a documented escalation path, even if "escalate to the navigator"?
- [ ] Has a disaster recovery procedure been tested (not just documented)?
- [ ] Are backups being tested for restore, not just existence?
- [ ] Is there a defined incident severity classification?

### 3.3 Handoff Artifacts

- `runbooks/` directory — one file per known incident type
- `incident-response.md` — escalation path, severity levels, response timelines
- `disaster-recovery.md` — what to do when infrastructure fails

### 3.4 Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | One runbook — "if it crashes, restart it" |
| 1 | Runbooks for top 3 known failure modes; manual incident response |
| 2 | Full runbook coverage; defined severity levels; escalation path |
| 3 | Automated incident detection; structured incident response; post-incident review for every P0/P1 |

### 3.5 Connection to Other Phases

- **Phase 4 (threat model):** each threat with mitigation should have a runbook for "what if the mitigation fails"
- **Phase 8 (production feedback):** incidents feed back as test cases
- **Phase 11 (iteration):** runbook gaps identified during incidents feed back as documentation work

---

## 4. Phase 10 — Observability

**Purpose:** Make the running system understandable from outside. Without this, debugging production issues is impossible, especially for LLM/agent systems.

### 4.1 Three Pillars

- **Logs** — structured, contextual, queryable records of what happened
- **Metrics** — quantitative measurements over time
- **Traces** — request/operation flow through the system

Plus supporting disciplines: dashboards, alerting, SLIs (Service Level Indicators), SLOs (Service Level Objectives), error taxonomy.

### 4.2 Why This Matters for AI Systems

An LLM conversation cannot be re-run deterministically. If something goes wrong in production, the only way to investigate is via traces and logs captured at the time. Without observability, you have no debugging surface.

A broken SQL query can be re-executed; a hallucinated response from an LLM cannot be exactly reproduced. Observability for AI systems is not optional.

### 4.3 Gate Questions

- [ ] Does every significant operation emit a trace with input/output information?
- [ ] Are there dashboards showing the key health metrics?
- [ ] Is there alerting on SLO breach, not just on crashes?
- [ ] Is there an error taxonomy, with every raised exception belonging to a documented class?
- [ ] Can a navigator reproduce a user-reported issue from the traces alone?

### 4.4 Handoff Artifacts

- `observability-design.md` — what's logged, what's traced, what's measured
- `sli-slo-definitions.md` — what "working" means, measurably
- `error-taxonomy.md` — documented exception classes

### 4.5 Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Print to stdout; no structure |
| 1 | Structured logs (JSON); basic metrics counter |
| 2 | Traces for critical paths; SLI defined; dashboards exist |
| 3 | Full three-pillar observability; SLO-based alerting; error taxonomy enforced in code |

### 4.6 Connection to Other Phases

- **Phase 4 (threat model):** every attack path should be detectable via observability
- **Phase 5 (CI/CD):** Domain 9 testing (observability assertions from [Testing Domains Reference](testing-domains-reference.md)) maps directly here
- **Phase 9 (operations):** incidents require observability to diagnose

---

## 5. Phase 11 — Iteration & Evolution

**Purpose:** PSE already has phase re-entry as a core concept. This phase makes it explicit as a lifecycle stage, not just a repair operation.

### 5.1 What Phase 11 Covers

- Feature iteration — adding new capability based on user feedback
- Technical debt reduction — addressing deferred issues
- Refactoring — structural improvement without behavior change
- Migration — changing underlying technology or patterns
- Version management — semantic versioning, deprecation, compatibility
- Change management — how changes get proposed, reviewed, deployed

### 5.2 Gate Questions

- [ ] Does every change have a clear triggering input (feedback, incident, strategic decision)?
- [ ] Does the change use Phase 2.5 brownfield decomposition to identify affected sub-projects?
- [ ] Is technical debt being tracked and addressed, not just accumulated?
- [ ] Are breaking changes communicated in advance with migration paths?
- [ ] Are version numbers meaningful (semver or documented alternative)?

### 5.3 Handoff Artifacts

- `iteration-log.md` — record of significant changes and their motivation
- `technical-debt.md` — tracked debt items with priority
- `migration-guides/` directory — when breaking changes happen
- `CHANGELOG.md` — user-facing version history

### 5.4 Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Changes happen; maybe there's a changelog |
| 1 | Breaking changes announced; semver followed loosely |
| 2 | Debt register exists; iterations use brownfield decomposition |
| 3 | Full change management; debt is budgeted and retired systematically |

### 5.5 Connection to Other Phases

- **Phase 2.5 (decomposition):** every iteration runs through brownfield decomposition
- **Phase 8 (production feedback):** feedback drives iteration priorities
- **CC3 (dependency management):** dependency updates are iteration work

---

## 6. Phase 12 — Decommissioning

**Purpose:** Remove the system safely when it's no longer needed. Most systems outlive their usefulness and become zombie infrastructure. Decommissioning is a real phase, not an afterthought.

### 6.1 What Phase 12 Covers

- Decommission planning — when and why to retire
- Dependency analysis — what else depends on this
- User migration — where do current users go
- Data disposition — what happens to the data
- Archive and audit — regulatory requirements for deleted data
- Knowledge preservation — what should be documented before shutdown
- Clean removal — code deleted, infrastructure torn down, accounts closed

### 6.2 Gate Questions

- [ ] Has every user/consumer of this system been notified?
- [ ] Has every dependency on this system been identified and rerouted?
- [ ] Is data being preserved as required (regulatory, historical)?
- [ ] Are credentials being revoked?
- [ ] Is there a post-decommission audit to verify nothing was missed?

### 6.3 Handoff Artifacts

- `decommission-plan.md` — what, when, how
- `data-disposition.md` — what happens to the data
- `dependency-map.md` — what depends on this, and what the migration is
- `post-decommission-audit.md` — verification that removal was clean

### 6.4 Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Delete the code, hope nothing breaks |
| 1 | Announce deprecation; provide basic migration info |
| 2 | Full decommission plan; dependency analysis; data disposition |
| 3 | Regulatory compliance; audit trail; post-decommission review |

---

## 7. The Staged Evolution Roadmap

At project start, the agent builds crude versions of each artifact. As the project matures, the agent evolves them. No phase gets skipped, but the depth matches the stage.

### 7.1 Stage Assessment Matrix

At each Phase 8+ invocation, the agent determines the project's current stage:

| Criterion | Level 0 | Level 1 | Level 2 | Level 3 |
|-----------|---------|---------|---------|---------|
| Deployment count | <5 | 5-50 | 50-500 | 500+ |
| Real users | 0-1 | 2-10 | 10-100 | 100+ |
| Known incidents | 0 | 1-3 | 4-20 | 20+ |
| Time since first deploy | <1 week | <1 month | <6 months | 6+ months |
| SLI-measurable components | 0 | 1-2 | 3-5 | 5+ |

Pick the level that best matches. If criteria conflict, pick the higher level (err toward more discipline).

### 7.2 Level 0 — Seed (first deployment, prototype)

**Time budget:** 30 minutes for all artifacts.

| Phase | What to produce |
|-------|----------------|
| 8 | Single `production-feedback-log.md` with space for failures only |
| 9 | One runbook: "if it crashes, here's how to restart it" |
| 10 | Structured logging (JSON format); no metrics or traces yet |
| 11 | `CHANGELOG.md` exists |
| 12 | Not applicable yet |
| CC1 | README with project description and how to run it |
| CC2 | If solo navigator, skip. Otherwise 3-sentence ONBOARDING.md |
| CC3 | Lockfile with pinned versions and hashes |
| CC4 | One-line cost estimate if applicable |

**Exit criteria:** First deployment is running. A navigator can restart it if it crashes.

### 7.3 Level 1 — Running (stable, some users)

**Time budget:** 4-8 hours to level up from Level 0, spread across weeks.

| Phase | What to produce |
|-------|----------------|
| 8 | All five feedback streams captured; review is manual and weekly |
| 9 | Runbooks for top 3 known failure modes; navigator as on-call |
| 10 | Basic metrics counter; dashboard is a text report |
| 11 | `technical-debt.md` exists; iterations use brownfield decomposition |
| 12 | Still not applicable |
| CC1 | Every doc has a stated owner and last-verified date |
| CC2 | ONBOARDING.md that a new person could actually follow |
| CC3 | Monthly CVE check; automated in CI |
| CC4 | Monthly cost review against projection |

**Exit criteria:** System has run 2+ weeks without constant intervention. Users exist.

### 7.4 Level 2 — Growing (real users, real stakes)

**Time budget:** 10-20% of ongoing development time.

| Phase | What to produce |
|-------|----------------|
| 8 | Feedback streams with triage process; findings routed to phases |
| 9 | Full runbook coverage; severity levels; escalation path |
| 10 | Traces for critical paths; SLIs defined; real dashboards; SLO alerting |
| 11 | Debt register budgeted; semver strict; breaking changes announced |
| 12 | Decommission plan template exists for future use |
| CC1 | Quarterly review cadence; deprecation process documented |
| CC2 | Tacit knowledge captured; handoff tested (vacation coverage) |
| CC3 | Automated CVE monitoring; freshness tracked |
| CC4 | Per-operation cost tracking; spike alerts; expensive ops gated |

**Exit criteria:** System running 6+ months. Known incidents have runbooks. SLIs measured.

### 7.5 Level 3 — Production (mature, dependable)

**Time budget:** 20-30% of ongoing development time.

| Phase | What to produce |
|-------|----------------|
| 8 | Automated feedback categorization; SLI-backed targets |
| 9 | Automated incident detection; structured response; P0/P1 post-incident review; DR tested |
| 10 | Full three-pillar observability; SLO alerting; error taxonomy in code |
| 11 | Full change management; debt budgeted and retired; migration guides standard |
| 12 | Decommission plans for planned retirements; regulatory audit trail |
| CC1 | Automated doc freshness checks; onboarding paths measured |
| CC2 | Bus-factor >= 2 for every critical component |
| CC3 | Full lifecycle policy; upstream health monitored |
| CC4 | Full cost allocation by feature/user; optimization ongoing |

**Exit criteria:** None — this is steady state. Phase 12 is the eventual transition.

### 7.6 The Leveling-Up Decision

- **0 → 1:** When the navigator has investigated a real production issue, or when a second user exists.
- **1 → 2:** When the navigator spends significant time on operations instead of development.
- **2 → 3:** When downtime has business consequence, or when a team (not just navigator) operates the system.

The agent should prompt when advancement seems warranted. Don't advance speculatively.

---

## 8. Agent Execution Protocol

### 8.1 Trigger Conditions

The agent invokes Phase 8+ when:

1. The navigator requests deployment planning, runbook creation, observability design
2. Phase 7 completes and the project is about to be deployed
3. The navigator reports a production incident
4. The navigator asks "what am I missing for production?"
5. A scheduled review is due

### 8.2 Execution Sequence

1. **Assess stage** — use the matrix in 7.1 to determine current level
2. **Identify phase** — determine which phase (8/9/10/11/12) or CC the request targets
3. **Look up level guidance** — find what's appropriate at this level
4. **Produce artifact** — generate the appropriate template at the appropriate depth
5. **Log stage** — record the stage assessment in the artifact's header
6. **Surface level-up candidates** — if criteria suggest advancement, mention it

### 8.3 Do Not Over-Engineer

The most common failure mode: producing Level 3 artifacts for Level 0 projects. A prototype doesn't need full runbook coverage, complete observability, SLOs, disaster recovery plans. It needs a restart script and structured logs.

### 8.4 Do Not Skip

The complementary failure: skipping phases entirely. A Level 0 project still needs Phase 8 (a crude feedback log), Phase 9 (a restart runbook), Phase 10 (structured logs). Minimal but present.

### 8.5 Connection to Decomposition (Phase 2.5)

When Phase 2.5 produces multiple sub-projects, each sub-project gets its own stage assessment for Phase 8+. A provider abstraction might be at Level 1 while the harness integration is at Level 0. Ops discipline matches each sub-project's actual maturity.

---

## 9. Why This Isn't Bureaucracy

A 200-person software company has distinct people for product management, engineering, QA, SRE, security, DevOps, technical writing, IT, legal, finance. Each specializes in one slice of the lifecycle.

A solo navigator with AI agents has the same lifecycle concerns and zero specialist headcount. The agents substitute for the specialists. But the agents need to know what the specialists would do. This document tells them.

**The staging compensates for scope.** A Level 0 project spends 30 minutes on all artifacts. A Level 3 system spends 20-30% of ongoing time. The commitment matches the stakes.

**AI agents make it tractable.** Before agents, following this full lifecycle required a team. With agents, the coordination cost collapses. The agent writes the docs, the runbooks, the dependency inventory. The navigator reviews. Not by cutting corners, but by changing who does the work.

---

*PSE covers build (Phases 1-7). Real systems also need deploy, operate, observe, iterate, retire (Phases 8-12) plus continuous concerns (documentation, knowledge, dependencies, cost). Match artifact depth to project stage using the Level 0-3 matrix.*
