# Case Study: Decomposing pse-harness

## The Failure That Motivated Phase 2.5

pse-harness was built as a monolith over two days. Retrospective analysis surfaced 34 bugs, approximately 10 of which were seam bugs — defects at the interfaces between what should have been independent sub-projects.

The methodology at the time had no explicit decomposition step. The navigator saw the whole system and built the whole system. The result: six structurally independent sub-projects were designed together, implemented together, and coupled at every level. Bugs that would have been caught by per-sub-project threat modeling and seam-specific testing slipped through because the threat model covered the system as one unit.

## What Phase 2.5 Would Have Produced

A decomposition map listing six sub-projects plus integration:

### Sub-project 1: Provider — LLM Abstraction

**Scope:** Wraps LLM API calls behind a Provider protocol. Handles auth, rate limiting, retries, fallback between models.

**External interfaces:** `Provider.complete(prompt) -> str`, `Provider.embed(text) -> list[float]`

**External dependencies:** OpenAI API, Anthropic API, local Ollama instance, ChromaDB

**Threat surface:** External API trust (keys, rate limits, response integrity), model output injection, embedding lock consistency

**Recommended testing domains:**
- Correctness (unit + integration) — mock providers for unit, real API for integration
- Security (SAST + secret scanning) — API keys must never leak
- Reliability (failure injection + timeout) — API failures must degrade gracefully
- Observability (trace completeness) — every API call must emit a span

**Independence evidence:** Passes team independence (different team could build with just the protocol), threat surface (distinct: external API trust), failure mode (distinct: API timeouts), consumer (reasoning + harness)

### Sub-project 2: Gate — Permission Engine

**Scope:** Classifies tool calls against policy rules. Produces audit-trailed Decisions.

**External interfaces:** `classify(tool_call) -> Decision`, `record_decision(decision)`

**External dependencies:** Policy rules (config), telemetry (for audit trail)

**Threat surface:** Rule evaluation correctness, audit trail integrity, fail-open vs. fail-closed behavior

**Recommended testing domains:**
- Correctness (unit + PBT) — property: every tool call gets a Decision; every Decision is recorded
- Security (SAST) — policy bypass patterns
- Data integrity (audit trail) — decisions never lost or corrupted
- Reliability (failure injection) — what happens when telemetry is unavailable?

**Independence evidence:** Passes team independence, threat surface (distinct: policy enforcement), failure mode (distinct: misconfiguration), consumer (tools + harness)

### Sub-project 3: Parsers — CI Output Parsers

**Scope:** Parses CI tool outputs (ruff, mypy, pytest, bandit, pip-audit, gitleaks) into structured Finding objects.

**External interfaces:** `parse(report_path) -> list[Finding]`

**External dependencies:** File system (report files)

**Threat surface:** Malformed input handling, injection via tool output

**Recommended testing domains:**
- Correctness (unit + PBT) — property: parse never crashes on arbitrary input; output is always list[Finding]
- Security (fuzzing) — malicious tool output must not cause code execution

**Independence evidence:** Passes team independence, threat surface (distinct: malformed input), failure mode (distinct: parse errors), consumer (tools), release cycle (parsers version independently as CI tools update)

### Sub-project 4: Telemetry — JSONL Event Logging

**Scope:** Structured event logging with session tracking, workspace isolation, and PII filtering.

**External interfaces:** `log_event(session_id, event, workspace)`, `query_events(session_id)`

**External dependencies:** File system (JSONL files)

**Threat surface:** PII leakage in nested dicts, concurrent write corruption, log injection

**Recommended testing domains:**
- Correctness (unit + integration) — log_event produces valid JSONL
- Security (SAST) — PII patterns in logged data
- Data integrity (serialization round-trip) — events survive write/read cycle
- Reliability (concurrency) — concurrent writers don't corrupt the file

**Independence evidence:** Passes team independence, threat surface (distinct: PII leakage), failure mode (distinct: concurrent writes), consumer (gate + tools + harness)

### Sub-project 5: Tools — Workspace-Isolated Operations

**Scope:** File read, file write, run_command, git operations — all workspace-boundary-enforced.

**External interfaces:** `file_read(path, workspace)`, `file_write(path, content, workspace)`, `run_command(cmd, workspace)`, `git_commit(msg, workspace)`

**External dependencies:** File system, subprocess, git

**Threat surface:** Workspace boundary escape, subprocess injection, git operation safety

**Recommended testing domains:**
- Correctness (unit + integration) — operations work within workspace
- Security (SAST + PBT) — property: no operation touches files outside workspace
- Reliability (timeout + resource exhaustion) — subprocess hangs, file descriptor leaks

**Independence evidence:** Passes all 5 tests — team independence, distinct threat surface (workspace boundary), distinct failure mode (subprocess), distinct consumer (harness), independent release cycle

### Sub-project 6: Reasoning — PSE Reasoning Pipeline

**Scope:** Runs multi-stage PSE reasoning (problem → requirements → design → threats → testable plan).

**External interfaces:** `run(task, context, architect) -> StructuredPlan`

**External dependencies:** Provider (for LLM calls), vendored pipeline contract

**Threat surface:** Vendored pipeline contract stability, prompt injection via task description, unbounded prompt size

**Recommended testing domains:**
- Correctness (unit + integration) — plan structure is valid; stages execute in order
- Security (adversarial prompt testing) — task descriptions with injection attempts
- Reliability (timeout) — reasoning with large context must timeout gracefully
- Observability (trace completeness) — every stage emits telemetry

**Independence evidence:** Passes team independence, threat surface (distinct: prompt injection), failure mode (distinct: plan parsing), consumer (harness)

### Integration Sub-project: Harness — Composition + Orchestration

**Scope:** Session orchestrator, CLI, config, composition root. The ONE place where sub-projects are instantiated and wired.

**Seam inventory:**

| Sub-project A | Sub-project B | Data Crossing Seam | Trust Assumptions |
|--------------|--------------|-------------------|-------------------|
| Provider | Reasoning | Completion requests/responses | Reasoning trusts Provider to return string-shaped output |
| Gate | Tools | ToolCall classification requests, Decisions | Tools trust Gate to classify before every high-risk op |
| Tools | Harness | ToolResult values, execution status | Harness trusts Tools to honor workspace boundary |
| Harness | Telemetry | Events, metadata | Harness trusts Telemetry to not raise |

**Seam testing domains:**
- Integration testing — seam-level tests for every pair above
- Contract testing — Provider protocol, Gate classify interface, Tool result format
- Seam security testing — workspace boundary enforcement at Tools↔Harness seam
- Failure injection — what happens when Provider fails? When Gate is unavailable?

## Bugs That Would Have Been Caught

With per-sub-project Phase 3-5 plus a seam threat model:

| Bug | Sub-project | Seam | How Caught |
|-----|------------|------|-----------|
| `git_commit` bypasses permission gate | Tools | Gate ↔ Tools | Tools sub-project threat model: "why doesn't git_commit consult classify()?" |
| Provider fallback caught at construction, not call-time | Provider | Provider ↔ Reasoning | Provider sub-project contract: "Provider protocol specifies what errors occur when" |
| Orchestrator silent-success when all steps blocked | Harness | Harness ↔ Gate | Seam threat model: "what happens when gate returns BLOCK for every step?" |
| Embedding lock not enforced | Provider | — | Provider sub-project threat model: "what invariants does ChromaDB collection depend on?" |
| Concurrent telemetry writes corrupt JSONL | Telemetry | — | Telemetry sub-project: reliability domain (concurrency testing) |
| run_command accepts arbitrary cwd | Tools | Tools ↔ Harness | Seam threat model: "what if harness passes cwd from untrusted source?" |
| PII in nested dicts leaks to logs | Telemetry | Harness ↔ Telemetry | Seam threat model: "what if harness emits forbidden fields in nested dicts?" |

## The Meta-Lesson

Architectural thinkers see systems whole. The methodology must explicitly prompt decomposition because the instinct to decompose is not universal among strong architects. Phase 2.5 exists because treating a six-sub-project system as one project produces integration bugs that single-project methodology cannot see.

The testing domains reference amplified this: with per-sub-project domain assignment, each sub-project gets the testing strategy appropriate to its threat surface. The provider needs reliability testing (API failures). The gate needs PBT (every tool call must get a Decision). The tools need security testing (workspace boundary). Without decomposition, these distinct testing needs get averaged into a generic test strategy that catches less.
