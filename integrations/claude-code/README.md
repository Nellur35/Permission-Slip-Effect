# Claude Code Integration

## Installation

### As a persistent skill (all projects)

```bash
git clone https://github.com/Nellur35/permission-slip-effect.git \
  ~/.claude/skills/permission-slip-effect
```

### Per-project

```bash
mkdir -p .claude/skills/methodology
cp integrations/claude-code/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md
```

### As a CLAUDE.md drop-in

Copy `methodology/CLAUDE-skill.md` to your project root alongside your existing `CLAUDE.md`. Claude Code picks it up automatically.

## What's included

| Skill | Purpose |
|-------|---------|
| `methodology/SKILL.md` | Orchestrator — routes to the right skill per phase |
| `guide/SKILL.md` | Explains what's in the repo and which skill/tool fits a situation |
| `intake/SKILL.md` | `/intake` — interactive Phase 1 problem definition |
| `decomposition/SKILL.md` | `/decompose` — Phase 2.5 project decomposition (greenfield + brownfield) |
| `threat-model/SKILL.md` | `/threat-model` — Phase 4 threat modeling |
| `review/SKILL.md` | `/review` — adversarial review at any phase |
| `gate-check/SKILL.md` | `/gate-check` — verify phase exit criteria |
| `audit/SKILL.md` | `/audit` — scan existing codebase and CI/CD |
| `session-retro/SKILL.md` | Structured RCA + retrospective + lessons learned for any session |
