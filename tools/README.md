# Tools

Standalone prompts for analysis-heavy work. Each tool works in any AI model — Claude Code, Kiro, Cursor, ChatGPT, Gemini, or anything else.

Each tool produces **surfaced material** (structured findings, questions, decomposed inputs, retrospective notes). That material is input for a navigator — a human or a subsequent analyst prompt — who decides what to do with it. None of these tools are verdicts; they are the raw analytical surface a careful reviewer would produce and then reason over. See [`../EVIDENCE.md`](../EVIDENCE.md) for the two-stage usage pattern.

## How to Use

### Option 1: Give the AI the single-file URL (easiest)

Point your AI tool at the full-context file:

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md
and use the threat-model tool on my architecture
```

One file, one fetch. The AI gets the full substrate: prompts, pipeline reference, and evidence.

### Option 2: Paste manually (for tools that can't read URLs)

1. Open any AI chat.
2. Paste the contents of the tool file as the prompt.
3. Paste your input (architecture doc, threat model, project structure, etc.) where indicated.
4. Get structured output.

Each tool is self-contained.

## Available Tools

### `intake.md`
Interactive questionnaire for problem definition. Asks one question at a time, pushes back on vague answers, redirects solution-jumping back to the problem. Supports greenfield projects and existing codebases.

**Input:** Describe your project
**Output:** Surfaced problem statement (greenfield) or reconstruction assessment (existing project) — material a navigator consumes to decide scope and next steps.

### `audit.md`
Scan an existing codebase and CI/CD pipeline. Maps architecture, test coverage, security controls, and pipeline gates. Produces a gap analysis a navigator can prioritize from.

**Input:** Project file tree, CI/CD config, existing docs
**Output:** Pipeline coverage, architecture map, priority actions — surfaced, not prescribed.

### `threat-model.md`
Generate a structured threat model from an architecture document. Examines trust boundaries, IAM blast radius, secrets lifecycle, data lifecycle, supply chain (including LLM-generated code), and related areas.

**Input:** `architecture.md` or system description
**Output:** Structured threat surface with risks, impact ratings, and mitigations the navigator then triages.

### `review.md`
Adversarial review of any artifact. Finds what is wrong, not whether it is good. Includes review lenses for architecture, threat models, CI/CD pipelines, requirements, and code.

**Input:** Any artifact (architecture, threat model, pipeline config, code, design doc)
**Output:** Structured findings with severity, impact, and recommended actions — input for the navigator's ruling step.

### `session-retro.md`
Structured feedback loop for any work session. Three stages: root cause analysis of what happened (not just what broke), retrospective on patterns and deltas, and executable lessons learned.

**Input:** Describe what happened this session — bug fix, feature, tech debt, investigation, anything
**Output:** RCA with causal chains, retrospective with pattern analysis, candidate lessons for the navigator to apply.

## Portability

Each tool works in any AI model. Point the AI at this repo and tell it which tool to use, or paste the tool contents manually if your AI can't read URLs. They are paste-in prompts, not a framework — keep whichever ones fit your workflow and ignore the rest.

## Relationship to the methodology sibling repo

These tools are the prompting layer. The software-engineering methodology that sequences them into an 8-phase workflow with gate checks, decomposition, and multi-agent orchestration lives in [`security-first-ai-dev-methodology`](https://github.com/Nellur35/security-first-ai-dev-methodology). That repo uses these tools; it is not a prerequisite for using them. Any individual tool stands alone.
