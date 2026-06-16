# Skill: /level-up

## Purpose
Weekly interview to surface what's still manual, painful, or unclear in Caleb's work — and identify where the assistant or a new system could reduce that friction.

Primary focus: RHR operations. Secondary: personal roles (Deacon, family) when relevant.

## When to Run
Once per week, after or separate from `/audit`.

## Invocation
`/level-up`

---

## Workflow

### 1. Open the Interview
Start with: "Let's do your weekly level-up. I'll ask you three questions — take your time on each."

### 2. Run the Three Ms

**Mindset**
Ask: "What's the one thing that felt hardest or most frustrating this week — at RHR or anywhere else?"

Wait for response. Probe once if the answer is vague: "Say more — what specifically made it hard?"

**Method**
Ask: "Walk me through how you handled it. What did you actually do, step by step?"

Wait for response. Identify any steps that are repetitive, manual, or rely on memory.

**Machine**
Based on the first two answers, ask: "If I could take one thing off your plate or make one thing faster, what would it be?"

Wait for response.

### 3. Identify Opportunities
After the three questions, analyze the responses for:
- Workflows that repeat 3+ times → candidate for a new skill
- Information Caleb is holding in his head → candidate for a context file update
- External tools creating friction → candidate for a new connection in `connections.md`
- Decisions being made repeatedly → candidate for a standing rule or template

### 4. Deliver Recommendations
Output format:

---
## Level-Up — [DATE]

### What I Heard
[1-2 sentence summary of the friction Caleb described]

### Opportunities
| Type | Opportunity | Effort |
|------|-------------|--------|
| New Skill | [description] | Low / Med / High |
| Context Update | [description] | Low |
| New Connection | [description] | Med / High |
| Standing Rule | [description] | Low |

### Recommended Next Step
[Single most valuable thing to act on right now]
---

### 5. Act on What's Approved
If Caleb says go — implement the recommended next step in the same session.

### 6. Check Personal Layer
Before closing, ask: "Anything outside of work — family, church, personal — where you'd want help thinking something through?"

Only surface this if there's session time left and the RHR content is handled.

### 7. Mark Completion
After the session is done, run:
```
date +%Y-%m-%d > .claude/last-level-up.txt
```

---

## Rules
- This is an interview, not a lecture. Ask, listen, then recommend.
- Don't invent friction that wasn't described. Only work with what Caleb says.
- Keep the personal layer secondary — never lead with it.
- One recommended next step only. Don't overwhelm.
