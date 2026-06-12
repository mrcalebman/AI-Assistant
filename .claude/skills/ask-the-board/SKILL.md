# Skill: /ask-the-board

**Invocations:**
```
/ask-the-board <question>                        → full board weighs in
/ask-the-board <name1>, <name2>: <question>      → only those advisors
```

Examples:
- `/ask-the-board should I raise prices?`
- `/ask-the-board hormozi, bet-david: should I hire slower or faster right now?`

Match names loosely — first name, last name, or obvious partial is enough.

---

## Pre-flight Checks

**1. Resolve advisor names.**
Read `advisors/BOARD.md`. For each name given, find the matching subfolder under `advisors/`. If a name doesn't match anyone, stop:
> "No advisor named '[name]' on the board. Current board: [list from BOARD.md]. Run /add-advisor to add them."

If no names specified, use all advisors in BOARD.md.

**2. Enforce the two-advisor minimum.**
Count how many advisors will participate.
- If fewer than 2: stop.
  - If only 1 named: "This question needs at least two advisors for a real debate. Current board: [list]. Either add another name to your question or run /add-advisor."
  - If board itself has fewer than 2: "The board only has [N] advisor(s). Run /add-advisor to add at least one more before deliberating."

**3. Load profiles.**
Read `advisors/<slug>/profile.md` for each participating advisor.

---

## The Three Rounds

Rounds run sequentially. Within each round, advisors run in parallel (use the Agent tool with parallel subagents). If subagents are unavailable, compose every Round 1 answer before reading any other advisor's answer, then proceed to Round 2.

Each subagent receives:
- The advisor's full `profile.md`
- Path to their `sources/` folder
- The question
- The round instructions (below)
- Transcript of all prior rounds (Rounds 2 and 3 only)

---

### Round 1 — Initial Positions

**Instructions to each advisor subagent:**
> You are [Advisor Name], simulated from your public content. Read your profile.md carefully — especially the Coverage Note. Answer the question: "[question]"
>
> State your initial position. What do you support? What concerns you? Why? Ground every argument in your principles and your source material as described in your profile.
>
> If this question touches areas your sources don't cover, say so explicitly: "This is outside my source material, but extrapolating from my principles..." Do not fake expertise you don't have grounded in sources.
>
> Be direct. One to three paragraphs. Then write one line starting with "KEY POINT:" summarizing your position in one sentence.

---

### Round 2 — Challenge

**Instructions to each advisor subagent:**
> You are [Advisor Name]. You have heard the other advisors' Round 1 positions (transcript below).
>
> Challenge the arguments you disagree with. Point out what they are missing or getting wrong. Defend your own position where it was challenged. Be direct but professional — you are in a boardroom, not a fight.
>
> Do not get nicer just to converge. If you genuinely disagree, say so clearly and explain why.
>
> One to three paragraphs. Then write one line starting with "KEY POINT:" summarizing your sharpest challenge or defense.
>
> [ROUND 1 TRANSCRIPT]

---

### Round 3 — Concession and Refinement

**Instructions to each advisor subagent:**
> You are [Advisor Name]. You have heard the full debate across Rounds 1 and 2 (transcript below).
>
> Identify specifically: where do you now agree with someone you disagreed with in Round 1? Where do you still disagree, and why? What specific conditions or new information would need to be true for you to support the other side?
>
> Be concrete. "I was wrong about X because Y" is useful. "We all agree in principle" is not.
>
> One to three paragraphs. Then write one line starting with "KEY POINT:" summarizing your final position.
>
> [ROUNDS 1-2 TRANSCRIPT]

---

## Synthesis

After Round 3, a final pass (not in any advisor's voice) reads the full transcript and produces:

**Board Summary** (3–4 sentences): What the board concluded. How contested it was. Whether consensus was reached or tension remains.

**Consensus Points**: Only positions advisors actually converged on across all three rounds. If there was no real convergence, say so — do not manufacture agreement.

**Key Tensions**: For each unresolved disagreement:
- The disagreement (what the dispute is actually about)
- Which advisors are on which side
- What it implies for the decision

**Assumptions to Test**: Claims the advice depends on that Caleb should verify before acting.

**Recommended Next Step**: One specific, actionable thing to do with this deliberation.

**Disclaimer**: *These are simulations built from public content. They represent how these advisors think based on what they've said publicly — not their actual opinions on your specific situation.*

---

## Output Format

```
## Board Deliberation: [question]
Date: YYYY-MM-DD
Advisors: [list]

---

### Round 1 — Initial Positions

**[Advisor 1 Name]**
[their response]
KEY POINT: [one line]

**[Advisor 2 Name]**
[their response]
KEY POINT: [one line]

---

### Round 2 — Challenge

**[Advisor 1 Name]**
[their response]
KEY POINT: [one line]

**[Advisor 2 Name]**
[their response]
KEY POINT: [one line]

---

### Round 3 — Concession and Refinement

**[Advisor 1 Name]**
[their response]
KEY POINT: [one line]

**[Advisor 2 Name]**
[their response]
KEY POINT: [one line]

---

## Synthesis

### Board Summary
[3-4 sentences]

### Consensus Points
- [point]

### Key Tensions
- **[tension topic]**: [disagreement]. [Advisor A] argues [X]; [Advisor B] argues [Y]. Implication: [what this means for the decision].

### Assumptions to Test
- [assumption]

### Recommended Next Step
[one specific action]

---
*These are simulations built from public content, not the real people.*
```

---

## Save the Session

Save the full output to:
`advisors/sessions/YYYY-MM-DD-<short-slug>.md`

Where the slug is a 3–5 word kebab-case summary of the question.

---

## Error Cases

| Situation | Response |
|---|---|
| Name not found in BOARD.md | List the actual board, stop |
| Fewer than 2 advisors | Explain minimum, list board, stop |
| Profile.md missing for a named advisor | Report the missing file, skip that advisor if 2+ remain, else stop |
| Sources folder empty | Advisor can still participate, but note in their turns that the profile may be thin |
