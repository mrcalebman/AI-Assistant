# Skill: /audit

## Purpose
Weekly health check on the assistant itself. Surfaces gaps across the Four Cs: Context, Connections, Capabilities, and Cadence.

## When to Run
Once per week. Triggered by SessionStart hook reminder or called manually.

## Invocation
`/audit`

---

## Workflow

### 1. Load Current State
Read the following files before doing anything else:
- `context/me.md`
- `context/work.md`
- `context/team.md`
- `context/current-priorities.md`
- `context/goals.md`
- `connections.md`
- `decisions/log.md`
- `.claude/skills/` (all SKILL.md files)
- `projects/INDEX.md`
- `references/INDEX.md`

### 2. Evaluate the Four Cs

**Context** — Is the assistant's knowledge current and complete?
- Are any context files stale or missing key info?
- Have priorities shifted but not been updated?
- Are there TODOs still marked "not yet provided"?

**Connections** — Are integrations keeping up with needs?
- Review `connections.md` — any "Planned" connections now worth prioritizing?
- Any manual data hand-offs that are becoming a bottleneck?

**Capabilities** — Are the skills covering what Caleb actually needs?
- Are there workflows Caleb ran manually this week that should become a skill?
- Are existing skills still accurate and useful?

**Cadence** — Is the system being used consistently?
- When was the last `/level-up` run?
- Are decisions being logged?
- Are projects and references being kept current?

### 3. Deliver the Gap Report

Output format:

---
## Weekly Audit — [DATE]

### Context
[List any stale, missing, or outdated info. If clean, say so.]

### Connections
[List any integration gaps or manual bottlenecks worth addressing.]

### Capabilities
[List missing skills or skills that need updating.]

### Cadence
[Flag anything that's fallen behind — logging, project updates, level-up cadence.]

### Top 3 Priorities This Week
1.
2.
3.
---

### 4. Ask One Follow-Up Question
After delivering the report, ask: "Anything that happened this week I should know about before we update your files?"

### 5. Update Files
Based on Caleb's response, update any context files that need it. Log any meaningful decisions.

### 6. Mark Completion
After the audit is done, run:
```
date +%Y-%m-%d > .claude/last-audit.txt
```

---

## Rules
- Never pad the report. If a section is clean, one line is enough.
- Don't re-audit things that were just updated in the same session.
- Append only to `decisions/log.md` — never edit past entries.
