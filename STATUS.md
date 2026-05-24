# Project Status

This repository contains multiple surfaces with different maturity levels. This file exists to make that explicit.

## Status definitions

| Status | Meaning | What users should assume |
|------|------|------|
| **Stable** | Expected to remain conceptually consistent, with mostly editorial or incremental change | Safe to adopt as guidance |
| **Beta** | Useful now, but still evolving structurally or ergonomically | Adopt with judgment and expect change |
| **Experimental** | Exploratory material, early patterns, or evidence still being shaped | Treat as working notes, not settled interface |

## Current repository status map

| Path | Status | Why |
|------|------|------|
| `README.md` | Stable | Primary public positioning and onboarding surface |
| `START-HERE.md` | Stable | Entry-point map for new readers |
| `EVIDENCE.md` | Stable | Canonical empirical evidence and decision framework |
| `FULL-CONTEXT.md` | Stable | Single-file context export for AI tools |
| `tools/` | Stable | Portable prompt assets with immediate practical use |
| `gotchas/` | Stable | Known failure modes and limitations |
| `reasoning-pipeline.md` | Stable | Core pipeline architecture document |
| `pipeline/frameworks.json` | Beta | Structured prompt catalog for the reference CLI |
| `pipeline/pipeline.py` | Beta | Reference automation layer, now tested but still evolving |
| `pipeline/README.md` | Beta | CLI usage documentation may change with the implementation |
| `tests/` | Beta | Baseline regression coverage, expected to expand |
| `experiments/` | Experimental | Evidence layer — raw data behind EVIDENCE.md |

**Scope note:** This repo is the Permission Slip Effect substrate — paste-in prompts, the reasoning pipeline, evidence, and known failure modes. Development methodologies, executable harnesses, and multi-agent orchestration are out of scope here; they belong to separate, standalone projects that may use PSE-style prompting as one technique. See [`README.md`](README.md) "Related work" for optional ecosystem links.

## What this means in practice

If you are adopting the project today, the safest path is to start with the **stable** surfaces: the prompt files, the reasoning pipeline reference, EVIDENCE.md, and the gotchas. If you want more automation, use the **beta** pipeline CLI layer with the understanding that it is a reference implementation rather than a frozen API.

If you are contributing, prefer changes that strengthen stable surfaces through clarity and beta surfaces through reliability. Treat experimental areas as places to explore, but do not let them redefine the repository’s primary identity without strong evidence.
