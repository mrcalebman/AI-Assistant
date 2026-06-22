# EXPANSIONS.md

Growth roadmap for the assistant system. Reviewed and updated during `/audit`.

---

## How to Use This File
- Items move from **Backlog → In Progress → Live** as they get built
- `/audit` surfaces new candidates; `/level-up` often generates them
- Don't build speculatively — only promote to In Progress when there's a real need

---

## MCP Connections (Live Data Access)

| Connection | Status | Value |
|------------|--------|-------|
| Gmail | Backlog | Read/send emails; surface client and team threads |
| Google Calendar | Backlog | Read job deadlines, schedule awareness per session |
| Trello | Backlog | Read/update job cards without leaving Claude |
| Google Drive | Backlog | Access job photos, documents, contracts |

## Skills

| Skill | Status | Value |
|-------|--------|-------|
| `/audit` | Live | Weekly Four Cs gap report |
| `/level-up` | Live | Weekly Three Ms friction interview |
| `/add-advisor` | Live | Build advisor profiles from public content |
| `/ask-the-board` | Live | Multi-advisor deliberation framework |
| `/ingest` | Live | YouTube video → knowledge base entry |
| `/job-closeout` | Live | End-of-job checklist to prevent callbacks — pre-punch list, client walkthrough prompt, 4-week follow-up reminder |
| `/weekly-report` | Backlog | Pull job status, flag at-risk timelines, summarize week for Joel |
| `/material-order` | Backlog | Draft material list from job scope; format for Home Depot / Lowe's / Amazon |
| `/sub-brief` | Backlog | Generate subcontractor briefing from job notes before a trade shows up |

## Context & Memory

| Item | Status | Value |
|------|--------|-------|
| `MEMORY.md` | Live | Cross-session memory separate from structured context files |
| Team contact info | Backlog | Phone/email for Joel, Josh N, Josh J, and all subs |
| Remaining active jobs | Backlog | Full details on 3–4 jobs beyond 240 E Ross St |
| Subcontractor performance notes | Backlog | Track reliability, quality, and communication per sub |

## Templates

| Template | Status | Value |
|----------|--------|-------|
| Job kickoff checklist | Backlog | Scope confirmed, materials ordered, subs scheduled, client expectation set |
| Callback prevention checklist | Backlog | Pre-completion punch list tied directly to the WIG |
| Client update email | Backlog | Weekly status email template for active jobs |

## Agents / Automation

| Item | Status | Value |
|------|--------|-------|
| Sub-agent: job monitor | Backlog | Watches active job timelines and flags drift before it becomes a miss |

---

## Graveyard
Items considered and ruled out — with reason.

| Item | Ruled Out Because |
|------|-------------------|
| QuickBooks integration | Caleb has limited access; not worth the complexity |
| Houzz Pro MCP | No public API; manual data hand-off is sufficient |
