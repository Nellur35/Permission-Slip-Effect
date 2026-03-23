# Project Log Enforcement Hooks

Hooks are the primary collection mechanism — they fire deterministically regardless of whether the AI follows the steering instruction. Steering is the fallback for platforms without hook support.

---

## Kiro — Agent Hook (on file save)

Create `.kiro/hooks/log-check.md`:

```markdown
---
name: log-check
trigger: on_file_save
description: Ensure log entry exists for recent changes
---

Check if project-log.md has been updated in this session. If changes were made to code, docs, or config files but no log entry was written since the last one, write the missing entry now. Follow the log entry format from the steering file.
```

This hook fires on every file save. If the AI already wrote the log entry (as the steering file instructs), the hook sees the update and does nothing. If the AI forgot, the hook catches it.

---

## Kiro — Autonomous Agent Hook

For Tier 3 (persistent agents), add to the autonomous agent's task description:

```
After completing any task, append a log entry to project-log.md following the project's log entry format. Include what you changed, why, which concern drove it, and what (if anything) was deferred.
```

The autonomous agent writes log entries as part of its task completion, keeping the log current even when the navigator isn't actively reviewing.

---

## Claude Code — Custom Hook

Claude Code supports custom hooks for tool execution events. Add to your hooks config:

```json
{
  "hooks": {
    "postToolExecution": [
      {
        "matcher": "write|edit|bash",
        "command": "echo 'Reminder: update project-log.md if this was a meaningful change'"
      }
    ]
  }
}
```

Claude Code's hook system is less deterministic than Kiro's — these are reminders, not triggers. For stronger enforcement, use the session-end hook:

```json
{
  "hooks": {
    "preCompact": [
      {
        "command": "echo 'Before compacting: verify project-log.md has entries for all changes this session'"
      }
    ]
  }
}
```

---

## Git — Pre-Commit Hook (All Platforms)

A git pre-commit hook that warns if code changed but project-log.md didn't:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Warns if code/config changed but project-log.md has no new entries

# Check if non-project-log files were modified
CODE_CHANGES=$(git diff --cached --name-only | grep -v project-log.md | grep -E '\.(ts|js|py|go|rs|md|yaml|json|toml)$' | wc -l)

# Check if project-log.md was modified
LOG_UPDATED=$(git diff --cached --name-only | grep -c project-log.md)

if [ "$CODE_CHANGES" -gt 0 ] && [ "$LOG_UPDATED" -eq 0 ]; then
    echo ""
    echo "⚠️  Code changed but project-log.md was not updated."
    echo "   Consider adding a log entry for this change."
    echo "   (This is a warning, not a block. Commit proceeds.)"
    echo ""
fi

# Always allow the commit — this is advisory, not blocking
exit 0
```

Install:
```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This works with any platform because it operates at the git level. It's advisory — warns but doesn't block. The navigator can ignore it for trivial changes.

---

## CI — Log Freshness Check (Optional)

For teams or projects that want stronger enforcement, add a CI step:

```yaml
# .github/workflows/log-check.yml
name: Log Freshness
on: pull_request

jobs:
  check-log:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check log coverage
        run: |
          # Count files changed in this PR (excluding project-log.md)
          CHANGED=$(git diff --name-only origin/main...HEAD | grep -v project-log.md | grep -E '\.(ts|js|py|go|rs)$' | wc -l)
          
          # Count new log entries in this PR
          ENTRIES=$(git diff origin/main...HEAD -- project-log.md | grep -c '^+###' || true)
          
          if [ "$CHANGED" -gt 3 ] && [ "$ENTRIES" -eq 0 ]; then
            echo "::warning::PR has $CHANGED code files changed but no log entries. Consider documenting what changed and why."
          else
            echo "✅ Log coverage looks good ($ENTRIES entries for $CHANGED files)"
          fi
```

This runs as a PR check. It warns but doesn't fail the build. The ratio of changes to entries is intentionally loose — not every file change needs an entry, but a PR with 10+ code files and zero log entries probably missed something.

---

## Summary: Defense in Depth

| Layer | Mechanism | Enforcement Level |
|---|---|---|
| Platform hook | Fires on save/compact/commit, writes entry deterministically | **Primary** — doesn't compete with coding instructions |
| Skill telemetry | Logs skill activations, outputs, overrides, reruns via PreToolUse/PostToolExecution hooks | **Observability** — feeds session retro Stage 2.5 |
| Steering file | AI instruction to write entries after each change | Secondary — works ~90% of the time but drifts in long sessions |
| Git pre-commit | Warns if code changed but project log didn't | Advisory — navigator sees the gap |
| CI check | PR-level coverage check | Team governance — optional |

**Use hooks when your platform supports them** (Kiro, Claude Code). Fall back to steering-only on platforms without hook support (Cursor, Windsurf). Add CI checks if you're running a team.

See [`telemetry.md`](telemetry.md) for skill telemetry setup — PreToolUse hooks that log which skills fire, how often, and whether the navigator overrides the output.
