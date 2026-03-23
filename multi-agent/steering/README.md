# Project Log Auto-Collection — Steering Configurations

One-line additions to your existing steering files. Add the block for your platform. That's it.

---

## Claude Code — CLAUDE.md

Add this block to your existing `CLAUDE.md`:

```markdown
## Project Log

After every meaningful change (code, docs, config, decisions — not formatting or typos), append a structured entry to `project-log.md` at project root. Use this format:

### [SESSION-ID] YYYY-MM-DD HH:MM — Brief title

- **Phase:** 1-8 or cross-phase
- **Concern:** security | architecture | correctness | performance | debt | testing | infrastructure | knowledge
- **Action:** created | modified | refactored | fixed | reviewed | deferred | reverted
- **Files:** changed files
- **What:** 1-2 sentences
- **Why:** 1-2 sentences
- **Deferred:** what was punted, or "none"

Just log what happened. Don't editorialize. Add `[RECURRING]` if you've seen this pattern before. Add `[PATTERN: S00X]` referencing specific prior entries. Add `[BOTTLENECK]` if it took disproportionate time. Write the entry immediately after the change, not at session end. Create project-log.md if it doesn't exist.
```

---

## Kiro — Steering File

Add to your steering file (`.kiro/steering/project-log.md` or append to existing):

```markdown
---
name: project-log
description: Auto-collect project log entries after every meaningful change
activation: always
---

After every meaningful change (code, docs, config, decisions — not formatting or typos), append a structured entry to `project-log.md` at project root.

Entry format:
### [SESSION-ID] YYYY-MM-DD HH:MM — Brief title
- **Phase:** 1-8 or cross-phase
- **Concern:** security | architecture | correctness | performance | debt | testing | infrastructure | knowledge
- **Action:** created | modified | refactored | fixed | reviewed | deferred | reverted
- **Files:** changed files
- **What:** 1-2 sentences
- **Why:** 1-2 sentences
- **Deferred:** what was punted, or "none"

Just log what happened. Mark `[RECURRING]` `[PATTERN: ID]` `[BOTTLENECK]` when relevant. Write immediately after the change. Create project-log.md if it doesn't exist.
```

---

## Cursor — .cursorrules

Add to your `.cursorrules`:

```
# Project Log
After every meaningful code, docs, config, or decision change, append an entry to project-log.md:
### [SESSION-ID] YYYY-MM-DD HH:MM — Title
- Phase: 1-8 | Concern: security/architecture/correctness/performance/debt/testing/infrastructure/knowledge
- Action: created/modified/refactored/fixed/reviewed/deferred/reverted | Files: changed files
- What: 1-2 sentences | Why: 1-2 sentences | Deferred: what or "none"
Just log what happened. Tag [RECURRING] [PATTERN: ID] [BOTTLENECK] when relevant. Write immediately after each change.
```

---

## Windsurf — AGENTS.md

Add to your root `AGENTS.md`:

```markdown
# Project Log Collection

After every meaningful change, append a structured entry to project-log.md. Format:

### [SESSION-ID] YYYY-MM-DD HH:MM — Title
- **Phase:** 1-8
- **Concern:** security | architecture | correctness | performance | debt | testing | infrastructure | knowledge
- **Action:** created | modified | refactored | fixed | reviewed | deferred | reverted
- **Files:** list
- **What/Why:** 1-2 sentences each
- **Deferred:** what or "none"

Just log what happened. Tag [RECURRING] [PATTERN: ID] [BOTTLENECK] when relevant.
```

---

## Codex — AGENTS.md or Project Instructions

Add to your `AGENTS.md` or project-level instructions:

```markdown
## Project Log
After every meaningful change, append to project-log.md:
### [SESSION-ID] YYYY-MM-DD HH:MM — Title
- Phase | Concern | Action | Files | What | Why | Deferred
Use the full structured format. Just log what happened. Tag [RECURRING] [PATTERN] [BOTTLENECK] when relevant.
```

---

## Notes

- **All platforms:** The project log instruction works because it's a simple, repeatable task the AI does well. It doesn't require special tooling — just a steering instruction that says "after you change something, write down what and why."

- **If the AI forgets:** Platform hooks catch the gap. On platforms with hook support (Kiro, Claude Code), hooks are the primary mechanism. On platforms without hooks (Cursor, Windsurf), steering is all you have — it works most of the time but drifts in long sessions.

- **Log location:** Default is `project-log.md` at project root. For monorepos, you might want `docs/project-log.md` or per-package logs. Adjust the path in the steering instruction.

- **Git integration:** The project log file is committed with the changes it describes. This means `git log` and `project-log.md` are complementary — git log shows what changed at the file level, the project log shows why and what concern drove it.
