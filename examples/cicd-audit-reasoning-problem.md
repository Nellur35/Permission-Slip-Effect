# Example Reasoning Problem: `cicd-audit`

A maintainer has built `cicd-audit`, a zero-dependency CI/CD security auditor with strong README positioning, packaging metadata, tests, and multiple report formats.

The maintainer now wants to decide the next strategic move.

## Decision question

Should the maintainer prioritize **broadening platform and rule coverage** or **hardening trust, packaging, and contributor ergonomics** over the next release cycle?

## Context

| Factor | Current situation |
|------|------|
| Public positioning | Strong, concrete, and product-oriented |
| Packaging | Conventional `pyproject.toml`, console entry point, dev extras |
| Tests | Real pytest suite with fixtures and focused unit coverage |
| Differentiation | Zero-dependency stance, explicit network behavior, CI/CD security focus |
| Risk | More features could outpace maintainability and contributor clarity |

## What the pipeline should answer

The pipeline should determine whether the highest-value next move is feature expansion, trust hardening, contributor enablement, or a staged combination of those paths.
