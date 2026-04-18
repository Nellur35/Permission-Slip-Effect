# PSE Methodology — Testing Domains Reference

*A Complete Taxonomy of QA/CI Disciplines for AI-Assisted Development*

**Status:** Methodology reference document
**Integrates:** Phase 5 (CI/CD Pipeline Design)
**Purpose:** Replace ad-hoc tool selection with structured discipline taxonomy
**Evidence:** Synthesized from 2025-2026 empirical research + practitioner literature (citations throughout)
**Audience:** AI agents executing Phase 5 + navigators reviewing Phase 5 output

---

## 0. Why This Document Exists

Phase 5 of PSE requires the navigator to design CI/CD pipelines that map gates to specific failure modes identified in threat modeling. But the existing methodology treats "what gates exist" as implicit practitioner knowledge. This document makes that knowledge explicit.

The core insight from 2025 empirical research: testing discipline has fragmented into at least nine distinct domains, each catching different bug classes at different points in the development lifecycle. No single testing strategy (pyramid, trophy, honeycomb) covers all of them. Modern CI architecture requires selecting a subset of disciplines appropriate to the project's threat model and stage of maturity.

This reference document describes all nine domains with:
- What failure class each catches
- What it does not catch
- Tools and disciplines for each
- Research backing where available
- Integration with PSE phases

Use this document when:
- Designing Phase 5 gates for a new project
- Reviewing existing CI architecture for gaps
- Adding a new CI stage to a maturing codebase
- Teaching an agent what "comprehensive testing" means
- Assigning recommended testing domains per sub-project in Phase 2.5

---

## 1. The Economic Principle

Before any specific domain, understand the underlying principle: testing is a filter pipeline where each layer catches defects at a cost.

### 1.1 The Cost-of-Defect Curve

The same defect caught at different points costs different amounts:

| Stage | Approximate Cost |
|-------|-----------------|
| Editor (type error) | $0.01 |
| Pre-commit hook | $0.10 |
| PR CI gate | $1.00 |
| Main branch CI | $10.00 |
| Staging environment | $100.00 |
| Production user encounter | $10,000+ |
| Security breach / data loss | $100,000 - $10,000,000 |

Source: Industry data consistent across multiple 2024-2025 DevSecOps reports (NIST, Gartner, IBM Security). The 10x-100x-1000x cost escalation at each stage is well-established.

### 1.2 The Filter Stacking Principle

Each domain catches some defects but not others. Coverage gaps between domains are where bugs ship. The goal is not "maximum checks" but "defense in depth where each layer catches what others miss."

A codebase protected only by linting and unit tests has shallow defense. A codebase protected by linting + type checking + unit tests + integration tests + property-based tests + SAST + secret scanning + SCA has layered defense where a bug must evade multiple filters tuned to different failure classes.

### 1.3 The Reactive-Not-Speculative Rule

CI grows by reaction to real failures, not speculative completeness. When a bug ships, identify the lowest-cost layer that could have caught it. Add a test at that layer. Over time, the CI evolves to match the actual failure modes of the project.

This is the opposite of "add every tool from the vendor's checklist."

---

## 2. Testing Strategy Shapes (How Domains Combine)

The "testing pyramid" is one way to combine domains. There are others. Each shape represents a different distribution of effort across test types.

### 2.1 The Pyramid (Cohn, 2009)

**Shape:** Many unit tests, fewer integration, very few E2E
**Best for:** Monolithic codebases, pure business logic, clear interfaces
**Limitation:** Unit tests can pass while integration fails; brittle to refactoring

### 2.2 The Trophy (Dodds, 2018)

**Shape:** Static analysis foundation, moderate unit, heavy integration, light E2E
**Best for:** Modern web apps, microservices, TypeScript codebases
**Rationale:** Static analysis catches what unit tests used to; integration tests catch what matters for users; unit tests only for pure logic

### 2.3 The Honeycomb (Spotify, ~2018)

**Shape:** Thin unit layer, thick integration layer, thin E2E
**Best for:** Microservices where inter-service behavior dominates
**Rationale:** In microservices, the interesting bugs live at service boundaries, not within individual services

### 2.4 The Diamond

**Shape:** Moderate unit, heavy integration, moderate E2E
**Best for:** Domain services in microservice architectures; business-critical workflows
**Rationale:** Balance between speed and user-simulation confidence

### 2.5 WireMock Vase (2025)

**Shape:** Many integration tests through public API, fewer unit tests at edges
**Best for:** Service-oriented architectures where public API is the contract
**Rationale:** Mocking tools are now mature enough that integration tests can be fast; refactoring-resilience matters more than isolation

### 2.6 Selection Criteria

The right shape depends on:

- Architecture (monolith, microservices, library, agent system)
- Where bugs tend to occur (internal logic, service boundaries, UI)
- How fast tests need to run (SaaS deploy velocity vs. embedded systems)
- What refactoring patterns dominate (internal vs. interface changes)

**For LLM/agent systems specifically**, none of the traditional shapes apply directly. See Section 11.

---

## 3. Domain 1: Correctness Testing

**What it catches:** "Does the code do what it's supposed to do?"

### 3.1 Unit Testing

**Definition:** Tests for a single function or class in isolation; dependencies are mocked.

**Discipline:**
- Named by behavior, not function: `test_login_accepts_valid_credentials`
- Arrange-Act-Assert structure
- Fast (<100ms per test)
- Deterministic (no network, no time, no randomness unless seeded)

**Catches:** Component-level logic errors, simple edge cases, regression on known inputs.

**Does not catch:** Integration bugs, real-world input distributions, concurrency, environmental issues.

**Common failure modes:**
- Over-mocking (tests pass because mocks behave as designed)
- Testing implementation not behavior (refactor breaks correct tests)
- Coverage-chasing (tests hit lines without asserting meaningful behavior)

**Tools:** pytest, unittest, jest, JUnit, Go testing

### 3.2 Integration Testing

**Definition:** Multiple components working together with real dependencies (or high-fidelity doubles like testcontainers).

**Discipline:**
- One integration boundary per test
- Real DB, real Redis, real filesystem — not mocks
- Can be slower (seconds) but still deterministic

**Catches:** Seam bugs, interface drift, integration-level edge cases.

**Does not catch:** User flows, performance under load, environmental issues.

### 3.3 End-to-End (E2E) Testing

**Definition:** Full user flow through the entire system.

**Discipline:**
- Few (10-50 tests, not thousands)
- Cover 5 most important user journeys
- Slow (minutes), flake-prone
- Separate CI stage, not every PR

**Catches:** User-level regressions, top-level workflow issues.

**Does not catch:** Edge cases (E2E at scale impractical), component bugs (too noisy).

### 3.4 Property-Based Testing (PBT)

**Definition:** Define invariants the code must satisfy; framework generates random inputs to break them.

**Example:**

```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert add(a, b) == add(b, a)
```

**Catches:** Edge cases humans don't think to write, off-by-ones, Unicode weirdness, empty-collection bugs, negative-input handling.

**EMPIRICAL EVIDENCE (2025):** In a study of 40 Python projects [Goldstein et al., OOPSLA 2025], property-based tests were **52 times more likely** to catch mutations than unit tests (odds ratio 51.91, p < 0.0001). This is one of the strongest empirical findings in testing research.

**Discipline:**
- Best for pure functions and data transformations
- Define properties, not examples
- Shrinking (framework finds minimal failing input)
- Seed for reproducibility

**Tools:** Hypothesis (Python), QuickCheck (Haskell), fast-check (JS), FsCheck (C#)

### 3.5 Mutation Testing

**Definition:** Deliberately break code (change < to <=, flip booleans, delete lines), run tests, measure how many mutations the tests catch.

**Metric:** Mutation score = (mutations killed / total mutations). Below 80% on critical paths means tests don't actually catch bugs.

**Catches:** Tests that pass for wrong reasons. Single highest-value metric for test quality (not code quality).

**2025 MATURITY:** Mutation testing has moved from research to practice. Meta uses it at scale (Assured LLMSE program, ICST 2025 keynote by Mark Harman). Stryker.NET, mutmut, cosmic-ray are production-ready.

**Tools:** mutmut, cosmic-ray (Python); Pitest (Java); Stryker (JS/.NET)

**Discipline:**
- Run on critical paths only (expensive)
- Set threshold per file
- Dropping score = test needs strengthening

### 3.6 Differential Testing

**Definition:** Compare old vs. new behavior on same input; fail if they differ unexpectedly.

**Catches:** Unintended behavior changes during refactoring, regression in migrations.

**Common use:** Verifying a rewrite preserves behavior of the original.

### 3.7 Snapshot / Approval Testing

**Definition:** First run produces an output; subsequent runs compare against stored snapshot.

**Catches:** Unintended output changes.

**Does not catch:** Whether the original snapshot is correct.

**Discipline:** Every snapshot change reviewed in PR (approval, not auto-accept).

---

## 4. Domain 2: Type Safety and Static Analysis

**What it catches:** "Is this code internally consistent, before running?"

### 4.1 Static Type Checking

**Python:** mypy, pyright, pytype
**TypeScript:** tsc, strict mode
**Other:** Sorbet (Ruby), Flow (JS)

**Discipline levels:**
- Loose: any-types allowed, optional annotations
- Strict: every function annotated, no implicit Any

**Catches:** Wrong argument types, None handling errors, return type mismatches, refactoring errors (renamed fields, forgot call sites).

**Does not catch:** Logic errors within well-typed code, runtime conditions.

**Discipline:**
- Every `# type: ignore` has a reason comment
- `Any` count baselined, no growth allowed
- New code must pass strict mode even if legacy is exempted

### 4.2 Runtime Type Checking

**Definition:** Types verified at function-call time, not compile time.

**Tools:** pydantic, typeguard, beartype (Python); io-ts (TypeScript)

**When to use:**
- At API boundaries (HTTP request/response)
- At deserialization points
- Anywhere untrusted input enters

**Difference from static:** Static catches before running; runtime catches when it happens. Both useful for different reasons.

### 4.3 Linting

**Definition:** Pattern-based code inspection for "code that looks like bugs I've seen before."

**Tools:** ruff (Python), ESLint (JS), golangci-lint (Go)

**Disciplines:**
- Style rules (formatting, naming)
- Bug-pattern rules (bare except, mutable defaults)
- Security rules (often overlap with SAST)

**Discipline:** Start strict, disable with reason comments. Rule config as negotiation is a failure mode.

### 4.4 Complexity Analysis

**Metrics:**
- Cyclomatic complexity (branches per function)
- Cognitive complexity (readability-weighted)
- Halstead metrics (vocabulary, length, difficulty)

**Ceiling:** Typically 10 for cyclomatic. Functions above get split or reviewed.

**Catches:** Architectural drift, functions growing beyond purpose.

**Tools:** radon, ruff C901 (Python); ESLint complexity rules

### 4.5 Dead Code Detection

**Tools:** vulture, unimport (Python); ts-prune (TS)

**Catches:** Functions/imports defined but never used.

**Does not catch:** Code used only in tests, dynamic dispatch (eval, getattr).

### 4.6 Dataflow Analysis

**Tools:** semgrep, CodeQL

**Catches:**
- Taint: user input reaching SQL without sanitization
- Secret flow: API keys reaching logs
- Null propagation: None reaching non-checking code

**Used at:** Mature security-focused CI pipelines.

---

## 5. Domain 3: Security Testing

**What it catches:** "Can an adversary exploit this?"

This is the most-fragmented domain in testing; the SAST/DAST/IAST/SCA taxonomy is 2025-standard practice for enterprise security.

### 5.1 SAST — Static Application Security Testing

**Definition:** Pattern-matching analysis of source code for known vulnerability patterns. Does not execute code.

**Tools:** bandit (Python), semgrep, CodeQL, SonarQube, Checkmarx

**Catches:**
- Hardcoded credentials
- Unsafe deserialization (pickle, yaml.load)
- SQL injection patterns
- Command injection patterns
- Weak cryptographic choices

**Does not catch:** Logic vulnerabilities, authentication bypass, authorization flaws, context-dependent issues.

**2026 UPDATE:** Anthropic's Claude Code Security and OpenAI's Codex Security released early 2026 use LLM reasoning to find bugs traditional SAST literally cannot see. Claude found heap buffer overflows fuzzing missed at 100% coverage. Not replacing traditional SAST; running alongside.

### 5.2 DAST — Dynamic Application Security Testing

**Definition:** Run the application, send malicious input, observe responses.

**Tools:** OWASP ZAP, Burp Suite, Acunetix

**Catches:** Runtime vulnerabilities, auth flaws, session handling bugs, XSS in rendered output.

**Does not catch:** Code-level issues not triggered by external input.

**When applicable:** HTTP services, APIs. Not applicable to pure libraries or batch processes.

### 5.3 IAST — Interactive Application Security Testing

**Definition:** Run the application with instrumentation; catch security issues while functional tests run.

**Tools:** Contrast Security, Seeker, Checkmarx CxIAST

**Catches:** Combines SAST's code-level visibility with DAST's runtime observation. Fewer false positives than either alone.

**Maturity:** Specialized tooling, enterprise-adopted, less common in open source.

### 5.4 RASP — Runtime Application Self-Protection

**Definition:** Security controls embedded in the application at runtime that detect and block attacks.

**Where it lives:** Production, not CI. Blocks attacks in real-time.

**Catches:** Exploitation attempts against known vulnerability classes.

**Tools:** Imperva, Contrast Protect, Signal Sciences

### 5.5 SCA — Software Composition Analysis

**Definition:** Check dependencies against known-vulnerability databases.

**Tools:** pip-audit, safety, Snyk, Dependabot, Renovate

**Catches:** CVEs in libraries you depend on.

**Discipline:**
- Pin dependencies with hashes (not just versions)
- Audit transitive deps, not just direct
- When CVE flagged: upgrade or document waiver

### 5.6 Secret Scanning

**Definition:** Find API keys, tokens, passwords in source or git history.

**Tools:** gitleaks, truffleHog, detect-secrets

**Discipline:**
- Run on every commit, not just main
- Run on full git history when introducing the tool
- Have a revocation runbook

### 5.7 Fuzzing

**Definition:** Generate random or mutated inputs; observe for crashes, hangs, or unexpected behavior.

**Types:**
- **Coverage-guided fuzzing:** AFL, libFuzzer, atheris — bit-level mutation, finds memory bugs
- **Property-based fuzzing:** Hypothesis — structured input generation for APIs
- **Grammar-based fuzzing:** For parsers, protocols, language implementations

**Catches:** Parser bugs, memory corruption, unhandled exceptions, DoS conditions.

**2025 research:** Fuzzing + mutation testing are increasingly combined; LLM-assisted fuzzing finds bugs pure-random fuzzing misses.

### 5.8 Container and IaC Scanning

**Tools:**
- Containers: trivy, grype, Clair, Snyk Container
- IaC: checkov, tfsec, Terrascan, Snyk IaC

**Catches:**
- Container: known CVEs in base images, misconfigured Dockerfiles
- IaC: overpermissive IAM, exposed storage, missing encryption

### 5.9 Threat-Modeling-as-a-Check

**Definition:** Automated verification that implementation matches threat model.

**Discipline:**
- Every mitigation in threat_model.md maps to a specific test or CI gate
- When a mitigation isn't covered, the threat model is docs without enforcement
- New threats produce new tests

**This is where PSE is ahead of standard practice.** Phase 4 (threat model) directly feeds Phase 5 (CI gates). Each threat's mitigation must have a corresponding automated check.

---

## 6. Domain 4: Reliability and Operational Readiness

**What it catches:** "Does it still work when something breaks?"

### 6.1 Failure Injection Testing

**Definition:** Deliberately fail dependencies and verify graceful degradation.

**Catches:** Error handling that looks good but doesn't work. Retry loops that don't terminate. Timeouts that don't fire.

**Not to be confused with chaos engineering:** Failure injection is targeted; chaos is random.

### 6.2 Chaos Engineering

**Definition:** Failure injection in production (or production-like) on live traffic.

**Tools:** Chaos Monkey, Gremlin, Litmus

**When applicable:** Mature distributed systems at scale. Not useful for single-machine work.

### 6.3 Resource Exhaustion Testing

**Catches:** Resource leaks (file descriptors, processes, memory). Memory bloat. Subprocess orphans.

**Discipline:**
- Run operations N times (100-1000); assert resource counts return to baseline
- Run under constrained resources (ulimit); assert graceful behavior

### 6.4 Timeout Verification

**Definition:** Test that timeouts actually fire.

**Example:**

```python
def test_subprocess_timeout_fires():
    start = time.time()
    with pytest.raises(subprocess.TimeoutExpired):
        run_command(["sleep", "60"], timeout=2)
    assert time.time() - start < 3
```

**Catches:** Timeouts configured but ignored; timeout values not propagated; hung operations.

### 6.5 Idempotency Testing

**Definition:** Verify that running an operation twice produces the same result as once.

**Catches:** Double-charge bugs, duplicate record creation, migration failures on retry.

**Critical for:** Anything that retries. Payment systems. Data ingestion. Deployment automation.

### 6.6 Retry Semantics Testing

**Verify:**
- Retries happen N times, not N+1
- Backoff applied
- Non-retryable errors (4xx) don't retry
- Retry storm prevention (jitter, circuit breaker)

---

## 7. Domain 5: Performance Testing

**What it catches:** "Is it fast enough, and does it stay fast enough?"

### 7.1 Benchmark Regression Testing

**Definition:** Measure time/memory cost of specific operations; verify no regression vs. baseline.

**Tools:** pytest-benchmark, asv (Python); Criterion (Rust); JMH (Java)

**Discipline:**
- Benchmark hot paths only, not every function
- Baselines in git
- Fail PR if regression >N% (typical: 20%)

### 7.2 Load Testing

**Definition:** Simulate expected user load; measure throughput, latency, resource usage.

**Tools:** k6, Locust, JMeter, Gatling

**Catches:** Throughput limits, connection pool exhaustion, query plan issues under load.

### 7.3 Stress Testing

**Definition:** Push beyond expected load until something breaks; find failure point.

**Catches:** Graceful degradation vs. cliff failure. Queueing behavior under overload.

### 7.4 Profiling

**Definition:** Measure where time/memory is actually being spent.

**Tools:** py-spy, scalene, cProfile (Python); perf (Linux); Chrome DevTools (JS)

**Discipline:**
- Profile before optimizing
- Profile real workloads, not synthetic benchmarks

### 7.5 Memory Leak Detection

**Tools:** memray, tracemalloc (Python); Valgrind (C/C++)

**Catches:** Caches growing unbounded, references preventing GC, C-extension leaks.

---

## 8. Domain 6: Data and State Integrity

**What it catches:** "Does data survive operations correctly?"

### 8.1 Migration Testing

**Disciplines:**
- Every migration has up and down
- Migration tests run on production-like data snapshots
- Data migrations separate from schema migrations

### 8.2 Schema Evolution Testing

**Verify:**
- Forward compat: old code handles new data (ignores new fields)
- Backward compat: new code handles old data (defaults for missing)
- Both tested during every schema change

### 8.3 Serialization Round-Trip Testing

**Definition:** `deserialize(serialize(x)) == x` for every serializable type.

**Catches:** Silent data corruption across serialization boundary.

**Critical for:** Any system with persistent state.

### 8.4 Runtime Invariant Checking

**Definition:** Assert system invariants during execution.

**Examples:**
- Audit trail always monotonically grows
- Account balance never negative
- Foreign keys always valid

**Tools:** Assertion libraries, custom contract decorators (icontract)

**Discipline:** Invariants in dev/staging, optional in production hot paths.

---

## 9. Domain 7: Documentation and Knowledge Integrity

**What it catches:** "Does documentation match code?"

### 9.1 Docstring Contract Verification

**Definition:** For docstrings claiming specific behavior, verify a test exists that exercises that behavior.

**Catches:** Doc/code drift. The "docstring says X, code does Y" bug class.

### 9.2 Example Validation

**Definition:** Code examples in documentation actually run.

**Tools:** doctest (Python), mdBook (Rust), custom extraction scripts

**Catches:** Documentation rot, API changes breaking tutorials.

### 9.3 API Documentation Completeness

**Discipline:** Every public function has a docstring; every public class documents invariants.

**Tools:** pydocstyle, interrogate

**Discipline:** Public API requires full documentation; internal exempt.

### 9.4 Link Validation

**Tools:** markdown-link-check, lychee

**Catches:** Refactoring that moved files without updating references; external docs that 404'd.

---

## 10. Domain 8: Process and Meta

**What it catches:** "Is the team following its own rules?"

### 10.1 Commit Message Validation

**Tools:** commitlint, commitizen

**Enables:** Automated changelog, semantic versioning, code archaeology.

### 10.2 PR Metadata Validation

**Requires:** PR description, linked issue, review checklist.

### 10.3 Code Review Coverage

**Tools:** CODEOWNERS, branch protection rules

**Enforces:** N reviewers, domain experts for touched areas.

### 10.4 Branch Hygiene

**Discipline:**
- Branches older than 30 days auto-closed
- PRs idle 14 days prompted for resolution

### 10.5 CI Health Metrics

**Track weekly:**
- PR gate duration (target: <5 min)
- PR failure rate (target: <30%)
- Main failure rate (target: <5%)
- Flaky test count (target: 0)
- Suppression counts (trending down)
- Baseline age (oldest entry)

---

## 11. Domain 9: Observability and AI-System Testing

**What it catches:** "When it breaks, can we figure out why?" PLUS "Does the AI/LLM system produce quality output?"

This is the newest domain and the most relevant to PSE's target use case. 2025-2026 research has established that LLM-based systems require fundamentally different testing than deterministic software.

### 11.1 Why Traditional Testing Fails on LLM Systems

**The core issue:** Conventional tests assume `f(X) == Y` for all X. LLMs produce probabilistic outputs — same X yields different Y across runs.

**Research consensus (2025-2026):** [Braintrust, DeepEval, Confident AI, Deepchecks]

- Exact-match assertions break against probabilistic output
- Coverage is meaningless when behavior is stochastic
- Reliability requires multiple runs to measure variance
- LLM-as-judge needed for open-ended output quality

### 11.2 The Three-Layer Model for Agent Systems

From Braintrust 2026 framework + academic survey (arXiv:2507.21504):

**Layer 1: Deterministic logic**
- Tool call routing (which tool selected)
- Argument parsing
- Response formatting
- State machine transitions
- Authentication/authorization

These use traditional unit/integration tests. Standard domains 1-8 apply.

**Layer 2: Semi-deterministic behavior**
- Prompt templates (format validity)
- Schema compliance (JSON validity, required fields)
- Cost/latency bounds
- Rate limit adherence

These use structural assertions — test for required shape without specifying exact content.

**Layer 3: Non-deterministic output**
- Response quality
- Goal achievement
- Hallucination detection
- Faithfulness to source

These use LLM-as-judge or quality-threshold evaluation.

### 11.3 LLM Evaluation Frameworks

**Tools (2025-2026):**
- promptfoo — prompt regression testing
- DeepEval — pytest-style evaluation
- Ragas — RAG-specific metrics
- Giskard — LLM safety testing
- Braintrust — unified evaluation platform
- Langfuse — observability-first
- Deepchecks LLM — comprehensive
- Arize Phoenix — tracing + evaluation
- Confident AI — evaluation + monitoring

**Evaluation dimensions (standard taxonomy):**
- **Faithfulness:** Is response grounded in provided context?
- **Relevance:** Does it address the query?
- **Coherence:** Is it logically structured?
- **Correctness:** Factually accurate?
- **Hallucination rate:** Does it fabricate?

### 11.4 Reliability Under Non-Determinism

**Critical discipline:** Run each test N times (typically 3-5); measure pass rate AND variance.

Pass criteria:
- Mean score above threshold
- Variance below limit (consistency)
- No catastrophic failures (zero-scored runs)

**From Confident AI / Braintrust 2026:** Tests that pass 4/5 runs but fail 1/5 are LESS trustworthy than tests that pass 5/5 at slightly lower mean. Variance matters as much as mean.

### 11.5 Trace Completeness Testing

**Definition:** Verify that every LLM call, tool execution, and state transition produces a trace span.

**Why critical for LLM systems:** Production debugging is impossible without complete traces. You cannot re-run an LLM conversation deterministically.

**What to verify:**
- Every stage of pipeline emits expected telemetry event
- Every provider call logged with input/output hashes
- Every gate decision traced
- Every tool invocation has a span

### 11.6 Prompt Regression Testing

**Definition:** When prompts change, verify behavior hasn't regressed on a fixed set of example inputs.

**Discipline:**
- Maintain a fixture set of inputs with expected output properties
- Run on every prompt change
- LLM-as-judge for quality scores
- Threshold gates for regression

### 11.7 Cost and Token Regression

**Definition:** Track average token cost per operation; fail if regression >N%.

**Catches:** Prompt changes that inflate cost without improving quality.

**From 2026 production guide:** A 30% token increase is a cost regression that should fail CI before hitting the API bill.

### 11.8 Adversarial Prompt Testing

**Definition:** Test against prompt injection, jailbreak attempts, policy bypass.

**Disciplines:**
- Static fixture set of known attack prompts
- Dynamic generation (red-teaming)
- Continuous update as new attacks emerge

**Tools:** Giskard, PyRIT (Microsoft), Garak

### 11.9 Authentication and Permission Testing for Agents

**From IntellAgent (Levi and Kadar, 2025):** Evaluate that agents enforce permission-sensitive behavior. Agent with DB access should not return data from another user's records even when asked plausibly.

**Discipline:** Permission boundaries enforced in test fixtures; assertions check that policy layer (not model alignment) prevents leakage.

---

## 12. PSE Integration — Which Domains Apply When

### 12.1 Phase 5 Generation Rule

When generating Phase 5 gates for a project:

1. Load the threat model (Phase 4 output)
2. For each threat, identify which domain's tests catch it
3. Require at least one gate per threat
4. Select domains based on project type (Section 12.2)
5. Skip domains that don't apply (e.g., DAST for a library)

### 12.2 Domain Selection by Project Type

**Python library / CLI tool:**
- Must: 1 (correctness), 2 (type safety), 3.1/3.5/3.6 (SAST/SCA/secrets)
- Should: 4 (reliability — timeouts, retries)
- Skip: DAST, IAST, container scanning, load testing

**Web application / API service:**
- Must: All of above + DAST, IAST, container scanning
- Should: 5 (performance), 6 (data integrity)
- Skip: Chaos engineering (unless mature)

**LLM agent / AI system:**
- Must: All library domains + 9 (observability + LLM eval)
- Should: Adversarial prompt testing, cost regression
- Critical: Trace completeness (production debugging depends on it)

**Microservice:**
- Must: 1 (heavy integration), 2, 3, 4 (chaos-lite)
- Should: 6 (contract testing), 10 (process)

**Data pipeline / ETL:**
- Must: 1, 2, 6 (heavy migration + schema evolution), 8 (process)
- Should: 4 (failure injection), 7 (data quality)

### 12.3 The "Defense in Depth" Heuristic

A mature CI has coverage across at least 5 domains. Projects with coverage in only 2-3 domains have shallow defense regardless of how thoroughly each domain is tested.

Rough maturity indicator:

| Domain Count | Maturity Level |
|-------------|---------------|
| 1-2 domains | Early / prototype |
| 3-4 domains | Functional but incomplete |
| 5-6 domains | Production-ready |
| 7-8 domains | Mature |
| 9 domains | Research-grade |

For most projects, 6-7 domains is the sweet spot. 9 is overkill except for safety-critical or regulated systems.

### 12.4 Adding a New Domain to an Existing CI

Use the staged-addition discipline:

1. Identify a specific bug class motivating the addition
2. Write a seeded-bug fixture that proves the check works
3. Baseline existing violations (if retrofitting)
4. Confirm time cost matches phase budget
5. Define suppression strategy with reason comments
6. Ship as single PR
7. Monitor false-positive rate for 2 weeks

If steps 1-2 cannot be completed, the check is not well-defined enough to add.

---

## 13. The Testing Strategy Decision Tree

Use this when designing or reviewing a Phase 5 CI architecture:

```
Is this a pure library?
├── Yes → Domain 1-3 required; Domain 4-8 as needed
│
└── No → Is it an HTTP service?
         ├── Yes → Domain 1-5 required; add Domain 3 (DAST), Domain 3 (Container and IaC Scanning)
         │
         └── No → Is it an LLM/agent system?
                  ├── Yes → Domain 1-4, 6, 9 required; Domain 9 is critical
                  │
                  └── No → Is it a data pipeline?
                           ├── Yes → Domain 1, 2, 6, 8 required
                           │
                           └── No → Classify more narrowly; consult Section 12.2
```

### 13.2 Phase 5 Gate-Selection Rubric

For each identified threat in threat_model.md:

1. What domain catches this threat?
2. What specific tool in that domain?
3. What gate configuration enforces it?
4. What's the seeded-bug fixture proving the gate works?
5. What's the time cost (floor/invariants/tests/slow-gates)?

If any question cannot be answered, the gate is not ready to add.

---

## 14. Common Pitfalls

### 14.1 Coverage Theater

**Symptom:** "We have 95% coverage."

**Problem:** Coverage measures execution, not verification. Tests can execute code without asserting meaningful behavior.

**Fix:** Mutation score as the real metric. Coverage is a floor (below which something is clearly untested), not a ceiling.

### 14.2 The Test-Pyramid Religion

**Symptom:** "We need more unit tests and fewer integration tests."

**Problem:** Pyramid is one strategy; trophy/honeycomb/vase may fit better depending on architecture.

**Fix:** Select shape based on where bugs actually occur.

### 14.3 Tool-Driven CI Growth

**Symptom:** "We added Tool X because it's industry standard."

**Problem:** Tools added without a failure class to catch become noise.

**Fix:** Reactive addition — bug class first, tool second.

### 14.4 Suppression Proliferation

**Symptom:** Baseline files growing; `# noqa` comments without reasons.

**Problem:** Checks become theater when suppressions are cheaper than fixes.

**Fix:** Every suppression requires a reason comment; baselines have expiration dates.

### 14.5 Flaky Test Tolerance

**Symptom:** "Just re-run it, it usually passes."

**Problem:** Flaky tests destroy CI trust. Once developers route around CI, it stops working regardless of check count.

**Fix:** Flaky tests quarantined immediately, fixed within 7 days, or deleted.

### 14.6 Slow-Gate Ignorance

**Symptom:** Slow-gate failures on main ignored because they don't block PRs.

**Problem:** Silent rot. Bugs accumulate.

**Fix:** Slow-gate failures notify owners. Main failing is higher severity than PR failing, not lower.

### 14.7 LLM Eval as Vibes-Check

**Symptom:** "The output looked good in manual testing."

**Problem:** Manual eval doesn't scale; doesn't catch regressions; doesn't produce gate-able metrics.

**Fix:** LLM-as-judge with threshold gates; N-run averaging for variance; fixture sets for regression.

---

## 15. Phase 2.5 Integration — Testing Domains per Sub-Project

When Phase 2.5 produces a decomposition map, each sub-project should be assigned recommended testing domains. This assignment happens during Phase 2.5 and feeds directly into Phase 5 gate selection.

### 15.1 How to Assign Testing Domains in Decomposition

For each sub-project in `decomposition-map.md`:

1. Classify the sub-project type (library, service, agent, pipeline, UI)
2. Look up the recommended domains in Section 12.2
3. Add the sub-project's specific threat surface (from the decomposition) to refine domain selection
4. Record the recommended domains in the sub-project's entry

### 15.2 Integration Sub-Project Testing Domains

The integration sub-project (required when N > 1) always includes:

- **Integration testing (Domain 1 — Integration Testing):** Seam-level tests for every pair of communicating sub-projects
- **Contract testing:** Verify each sub-project honors its declared interface
- **Seam security testing (Domain 3):** Security tests focused specifically on data crossing seam boundaries — trust assumptions, input validation at boundaries, authentication between components
- **Failure injection (Domain 4 — Failure Injection Testing):** What happens when one sub-project fails? Does the other degrade gracefully or cascade?

### 15.3 Seam-Specific Testing Guidance

For each seam in the seam inventory:

| Question | Testing Domain |
|----------|---------------|
| What data crosses this seam? | Domain 6 — Serialization Round-Trip Testing |
| What trust assumptions exist? | Domain 3 — Seam Security Testing |
| What happens when one side fails? | Domain 4 — Failure Injection Testing |
| Is the interface versioned? | Domain 6 — Schema Evolution Testing |
| Can the seam be fuzzed? | Domain 3 — Fuzzing |

---

## 16. Empirical Evidence Summary

Key research findings backing this reference:

### 16.1 Property-Based Testing Effectiveness

Goldstein et al., OOPSLA 2025 — Empirical study of 40 Python projects. Property-based tests caught mutations **52x more often** than unit tests (odds ratio 51.91, chi-square p<0.0001). Strongest empirical finding in 2025 testing research.

### 16.2 Mutation Testing at Scale

Meta's Assured LLMSE program (ICST 2025 keynote, Mark Harman): mutation testing combined with LLM-generated tests achieved 73% acceptance rate from human engineers, with 36% judged as relevant to real fault classes. At-scale proof that mutation testing produces actionable signal.

### 16.3 Shift-Left Economics

Multiple 2024-2025 industry studies (GitLab, Wiz, IBM Security, NIST): catching vulnerabilities at PR gate costs ~$100; at production costs $10,000+. 100x cost reduction for shifting left. Consistent across programming languages and deployment models.

### 16.4 LLM Agent Reliability

arXiv:2507.21504 (Evaluation and Benchmarking of LLM Agents, 2025): reliability requires multiple-run variance measurement. Agents showing high mean quality with high variance are less production-ready than agents with slightly lower mean and consistent output.

### 16.5 Testing Strategy Evolution

WireMock 2025 report + industry adoption data: traditional pyramid increasingly replaced by trophy/vase/honeycomb shapes as mocking infrastructure matures. Integration tests can now be as fast as unit tests were in 2010, changing the cost calculus.

### 16.6 LLM-Powered SAST

Anthropic Claude Code Security (2026), OpenAI Codex Security (2026): LLM-based SAST finding bugs traditional pattern-matching misses. Example: heap buffer overflow found by Claude that fuzzing missed at 100% coverage. Complementary to, not replacing, traditional SAST.

---

## 17. Why This Belongs in PSE

PSE's existing methodology generates Phase 5 gates from threats, which is ahead of standard practice. But it treats "what gates exist" as implicit practitioner knowledge. For AI-assisted development — where agents execute the methodology — the knowledge must be explicit.

This reference document:

1. Makes the full landscape explicit for agent consumption
2. Establishes domain-selection discipline tied to project type
3. Grounds recommendations in 2025-2026 empirical research
4. Specifically addresses LLM/agent systems (PSE's primary use case)
5. Preserves the reactive-addition principle (don't add speculatively)
6. Maps directly to the existing Phase 5 → CI gate flow
7. Provides the vocabulary for navigator ↔ agent communication about testing strategy
8. Integrates with Phase 2.5 decomposition via per-sub-project domain assignment

The result: Phase 5 moves from "design a CI pipeline" to "select testing domains covering the identified threats, then implement gates in each selected domain." This is a stronger, more defensible, more teachable process.

---

*Testing fragments into nine domains, each catching a specific bug class; Phase 5 gates must be selected by domain based on project type and threat model, with empirical research (especially the 52x finding on property-based testing) grounding the disciplines that produce the highest-quality test suites.*
