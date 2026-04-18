# PSE Methodology — Cross-Cutting Concerns

*Continuous practices across the full lifecycle. Not phases — these run alongside Phases 1-12.*

---

## CC1 — Documentation Lifecycle

**Purpose:** Documentation is a living artifact, not a one-time output. Without lifecycle discipline, docs drift, get stale, and become untrusted.

### What This Covers

- Ownership — who is responsible for each doc
- Review cadence — how often docs are verified against reality
- Sunset discipline — when deprecated docs get retired
- Onboarding paths — how new users find what they need
- Searchability — docs are discoverable, not just existent
- Version alignment — docs match the version of code they describe

### Gate Questions (continuous)

- [ ] Does every document have a stated owner?
- [ ] Does every document have a "last verified" date?
- [ ] Are deprecated docs marked or removed, not left to mislead?
- [ ] Is there a clear onboarding path for new users?

### Handoff Artifact

`docs/README.md` — index, ownership, review cadence

### Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Docs exist somewhere |
| 1 | Docs have owners; README explains structure |
| 2 | Review cadence enforced; deprecation process exists |
| 3 | Automated doc freshness checks; onboarding paths measured |

---

## CC2 — Knowledge Transfer & Onboarding

**Purpose:** When the navigator changes — leaves, rotates, takes vacation, gets hit by a bus — the project must survive. PSE assumes the navigator has full context. Transfer planning preserves that context.

### What This Covers

- Onboarding guides — how a new navigator gets started
- Tacit knowledge capture — the things that aren't written down elsewhere
- Context handoff — what's in progress, what's blocked, what's known
- Bus-factor analysis — what happens if critical person is unavailable

### Gate Questions

- [ ] Could a new navigator take over this project with only the written artifacts? What's missing?
- [ ] Is there a documented list of tacit knowledge load-bearing for this project?
- [ ] Is there an onboarding guide tested by a real new person?

### Handoff Artifacts

- `ONBOARDING.md` — new navigator's starting point
- `TACIT-KNOWLEDGE.md` — things that aren't elsewhere
- `HANDOFF.md` — current state of in-progress work

### Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | Navigator holds all context; no transfer plan |
| 1 | ONBOARDING.md exists; points to key artifacts |
| 2 | Tacit knowledge captured; handoff works without original navigator |
| 3 | Bus-factor >= 2 for every critical component |

---

## CC3 — Dependency Management

**Purpose:** Dependencies are not a one-time Phase 4 concern. They drift, deprecate, develop CVEs, and occasionally disappear. Active management across the lifecycle prevents slow rot.

### What This Covers

- Dependency inventory — what we depend on, and why
- Freshness tracking — when dependencies were last updated
- Security monitoring — CVE disclosures affecting dependencies
- Maintainer health — is the upstream project still maintained
- Addition criteria — when to add new dependencies
- Removal discipline — when to remove obsolete dependencies

### Gate Questions

- [ ] Is the dependency inventory up to date?
- [ ] Are there dependencies that haven't been updated in N months without justification?
- [ ] Are CVE feeds being monitored for our specific dependencies?
- [ ] Is there a process for adding a new dependency?

### Handoff Artifacts

- `dependencies.md` — inventory with justifications
- `dependency-policy.md` — criteria for addition/removal

### Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | requirements.txt exists, nobody looks at it |
| 1 | Lockfile with hashes; manual CVE checks monthly |
| 2 | Automated CVE monitoring; freshness tracked per-dependency |
| 3 | Full lifecycle policy; upstream health monitored; bus-factor considered |

---

## CC4 — Cost Management

**Purpose:** Especially critical for AI systems. Token costs, compute costs, storage costs — they accumulate. Without tracking, you find out at the monthly bill.

### What This Covers

- Cost projection — what the system should cost to run
- Cost tracking — what it actually costs
- Cost allocation — which features/users/operations cost what
- Cost alerting — notification when spend exceeds projection
- Cost optimization — reducing spend without reducing value

### Gate Questions

- [ ] Is there a cost projection for the system?
- [ ] Is actual cost being tracked against projection?
- [ ] Are there alerts for unexpected spend spikes?
- [ ] Are expensive operations identified and gated (e.g., LLM calls)?

### Handoff Artifacts

- `cost-model.md` — projected and actual cost breakdown
- `cost-alerts.md` — thresholds and notification targets

### Maturity Staging

| Level | What Exists |
|-------|-------------|
| 0 | "We hope it's not too expensive" |
| 1 | Monthly cost review; rough projections |
| 2 | Per-operation cost tracking; alerts on spikes |
| 3 | Full cost allocation by feature/user; optimization ongoing |

---

*Cross-cutting concerns are not phases you pass through. They are continuous practices that the agent maintains and the navigator reviews. Match depth to project stage using the Level 0-3 matrix from [lifecycle-phases-8-12.md](lifecycle-phases-8-12.md).*
