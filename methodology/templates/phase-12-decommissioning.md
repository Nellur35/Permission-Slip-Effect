# Phase 12 — Decommissioning Plan

**Input:** Decision to retire the system
**Maturity level:** [Level 0 / 1 / 2 / 3 — see lifecycle-phases-8-12.md]

## Why Decommissioning

[Business or technical reason for retiring this system]

## Timeline

| Milestone | Date | Action |
|-----------|------|--------|
| Announcement | [Date] | [Notify all users and consumers] |
| Migration deadline | [Date] | [All users migrated to alternative] |
| Shutdown | [Date] | [System stops accepting requests] |
| Final removal | [Date] | [Infrastructure torn down, code archived] |

## Dependencies to Address

| Dependent System | Contact | Migration Plan | Status |
|-----------------|---------|---------------|--------|
| [e.g., Service X] | [e.g., Team Y] | [e.g., Switch to API Z] | [ ] Migrated |
| [e.g., User group] | [e.g., via email] | [e.g., Use alternative tool] | [ ] Notified |

## Data Disposition

| Data Class | Current Location | Disposition | Regulatory Requirement | Status |
|-----------|-----------------|------------|----------------------|--------|
| [e.g., User data] | [e.g., PostgreSQL] | [e.g., Delete after 90 days] | [e.g., GDPR Art. 17] | [ ] Completed |
| [e.g., Audit logs] | [e.g., S3] | [e.g., Archive for 7 years] | [e.g., SOX compliance] | [ ] Archived |
| [e.g., Config/secrets] | [e.g., Vault] | [e.g., Revoke immediately] | [e.g., Security policy] | [ ] Revoked |

## Credentials to Revoke

| Credential | Type | Where Used | Status |
|-----------|------|-----------|--------|
| [e.g., API key for Service X] | [e.g., API key] | [e.g., Production env vars] | [ ] Revoked |
| [e.g., Service account] | [e.g., IAM role] | [e.g., AWS] | [ ] Deleted |
| [e.g., OAuth client] | [e.g., Client ID/secret] | [e.g., Auth0] | [ ] Removed |

## Infrastructure to Tear Down

| Resource | Provider | Order | Dependencies | Status |
|----------|---------|-------|-------------|--------|
| [e.g., Lambda functions] | [e.g., AWS] | [1] | [None] | [ ] Removed |
| [e.g., Database] | [e.g., AWS RDS] | [2] | [After data export] | [ ] Removed |
| [e.g., DNS records] | [e.g., Route53] | [3] | [After shutdown] | [ ] Removed |

## Knowledge to Preserve

- [ ] Architecture decisions and rationale (archive `architecture.md`)
- [ ] Threat model lessons learned (archive `threat_model.md`)
- [ ] Operational lessons (archive runbooks and incident history)
- [ ] Why this system was decommissioned (this document)

## Post-Decommission Verification

- [ ] No DNS records point to decommissioned infrastructure
- [ ] No active credentials remain
- [ ] No other systems still call this one (check logs for 30 days post-shutdown)
- [ ] Data disposition is complete per regulatory requirements
- [ ] Archive is accessible if needed for historical reference

## Gate Questions

- [ ] Has every user/consumer been notified?
- [ ] Has every dependency been identified and rerouted?
- [ ] Is data preserved as required?
- [ ] Are credentials revoked?
- [ ] Is post-decommission audit planned?

---

*Decommissioning is the final phase of a system's lifecycle. A clean removal prevents zombie infrastructure, credential sprawl, and regulatory violations.*
