# Phase 9 — Operations & Incident Response

**Input:** Running production system from Phase 7-8
**Maturity level:** [Level 0 / 1 / 2 / 3 — see lifecycle-phases-8-12.md]

## Incident Severity Classification

| Severity | Definition | Response Time | Example |
|----------|-----------|---------------|---------|
| P0 | System down, data loss risk | Immediate | Production database unreachable |
| P1 | Major feature broken, workaround exists | < 1 hour | Auth fails intermittently |
| P2 | Minor feature broken, low user impact | < 1 day | Dashboard renders slowly |
| P3 | Cosmetic or edge case | Next sprint | Tooltip misaligned |

## Escalation Path

| Step | Who | When | How |
|------|-----|------|-----|
| 1 | [e.g., Navigator / on-call] | [e.g., Alert fires] | [e.g., Check dashboard, run triage runbook] |
| 2 | [e.g., Team lead / senior engineer] | [e.g., P0 not resolved in 30 min] | [e.g., Page via Slack/PagerDuty] |
| 3 | [e.g., External support / vendor] | [e.g., Infrastructure failure beyond team control] | [e.g., File support ticket] |

## Runbooks

### Runbook: [Incident Name]

**When this applies:** [Specific signals indicating this incident type]
**Severity:** [P0 / P1 / P2 / P3]

**First response (first 5 minutes):**
1. [action]
2. [action]
3. [action]

**Investigation:**
[Where to look, what to check, common root causes]

**Resolution:**
[Steps to fix]

**Prevention:**
[What changes would prevent recurrence]

**Related incidents:**
[Links to past occurrences]

---

### Runbook: [Second Incident Name]

[Same structure]

---

## Disaster Recovery

**Recovery Point Objective (RPO):** [Maximum acceptable data loss — e.g., 1 hour]
**Recovery Time Objective (RTO):** [Maximum acceptable downtime — e.g., 4 hours]

**Backup strategy:**
- [What is backed up, how often, where stored]
- [How to verify backups are restorable]

**DR procedure:**
1. [Step to restore service]
2. [Step to verify data integrity]
3. [Step to communicate status]

**Last DR test:** [Date and outcome]

## Capacity Planning

| Resource | Current Usage | Limit | Headroom | Alert Threshold |
|----------|-------------|-------|----------|-----------------|
| [e.g., CPU] | [e.g., 40%] | [e.g., 100%] | [e.g., 60%] | [e.g., 80%] |
| [e.g., Memory] | [e.g., 2GB] | [e.g., 8GB] | [e.g., 75%] | [e.g., 6GB] |
| [e.g., API rate limit] | [e.g., 100/min] | [e.g., 1000/min] | [e.g., 90%] | [e.g., 800/min] |

## Gate Questions

- [ ] For each component that can fail, is there a runbook?
- [ ] Is there a documented escalation path?
- [ ] Has disaster recovery been tested (not just documented)?
- [ ] Are backups tested for restore, not just existence?
- [ ] Is there a defined incident severity classification?

---

*Operations artifacts are living documents. Update runbooks after every incident. This file feeds Phase 8 (production feedback) and Phase 11 (iteration).*
