# Phase 10 — Observability Design

**Input:** Running production system + Phase 4 `threat_model.md`
**Maturity level:** [Level 0 / 1 / 2 / 3 — see lifecycle-phases-8-12.md]

## Logs

| Log Source | Level | Format | Destination | Retention |
|-----------|-------|--------|-------------|-----------|
| [e.g., API requests] | [e.g., INFO] | [e.g., JSON] | [e.g., CloudWatch] | [e.g., 30 days] |
| [e.g., Errors] | [e.g., ERROR] | [e.g., JSON] | [e.g., CloudWatch + Slack alert] | [e.g., 90 days] |
| [e.g., Security events] | [e.g., WARN] | [e.g., JSON] | [e.g., SIEM] | [e.g., 1 year] |

## Metrics

| Metric Name | Type | What It Measures | Dashboard? | Alert Threshold |
|------------|------|-----------------|------------|-----------------|
| [e.g., request_count] | Counter | [Total API requests] | [Yes] | [N/A — informational] |
| [e.g., request_latency_p99] | Histogram | [99th percentile response time] | [Yes] | [> 500ms] |
| [e.g., error_rate] | Gauge | [Errors per minute] | [Yes] | [> 5/min] |
| [e.g., token_cost_usd] | Counter | [LLM API spend] | [Yes] | [> $X/day] |

## Traces

| Operation | Spans Produced | Input Captured? | Output Captured? |
|-----------|---------------|-----------------|-----------------|
| [e.g., API request] | [e.g., handler → service → DB] | [Yes — sanitized] | [Yes — truncated] |
| [e.g., LLM call] | [e.g., prepare → call → parse] | [Yes — prompt hash] | [Yes — response hash] |

## SLIs (Service Level Indicators)

| SLI | Definition | Measurement |
|-----|-----------|-------------|
| [e.g., Availability] | [Percentage of successful requests / total requests] | [e.g., HTTP 2xx / total HTTP] |
| [e.g., Latency] | [Percentage of requests completing within threshold] | [e.g., P99 < 500ms] |
| [e.g., Correctness] | [Percentage of responses matching expected behavior] | [e.g., LLM output passes quality check] |

## SLOs (Service Level Objectives)

| SLI | Target | Window | Consequence of Breach |
|-----|--------|--------|----------------------|
| [Availability] | [e.g., 99.5%] | [e.g., 30 days rolling] | [e.g., Page on-call] |
| [Latency] | [e.g., 95% of requests < 500ms] | [e.g., 7 days rolling] | [e.g., Investigate bottleneck] |

## Error Taxonomy

| Error Class | Code/Exception | Meaning | Retry? | Alert? |
|------------|---------------|---------|--------|--------|
| [e.g., TransientError] | [e.g., 503, TimeoutError] | [Temporary failure, will resolve] | [Yes, with backoff] | [Only if sustained] |
| [e.g., ClientError] | [e.g., 400, ValidationError] | [Invalid input from caller] | [No] | [No — caller's problem] |
| [e.g., InternalError] | [e.g., 500, unhandled] | [Bug in our code] | [No] | [Yes — immediate] |

## Alerts

| Alert Name | Condition | Severity | Notify | Runbook Link |
|-----------|-----------|----------|--------|-------------|
| [e.g., High error rate] | [e.g., > 5 errors/min for 5 min] | [P1] | [e.g., Slack #alerts] | [e.g., runbooks/high-error-rate.md] |
| [e.g., SLO breach] | [e.g., Availability < 99.5% over 1 hour] | [P0] | [e.g., PagerDuty] | [e.g., runbooks/slo-breach.md] |

## Gate Questions

- [ ] Does every significant operation emit a trace?
- [ ] Are there dashboards showing key health metrics?
- [ ] Is there alerting on SLO breach, not just crashes?
- [ ] Is there an error taxonomy with every exception classified?
- [ ] Can a navigator reproduce a user-reported issue from traces alone?

---

*Observability is the debugging surface for production. For AI/LLM systems, this is critical — conversations cannot be re-run deterministically. This file feeds Phase 9 (operations) for incident diagnosis.*
