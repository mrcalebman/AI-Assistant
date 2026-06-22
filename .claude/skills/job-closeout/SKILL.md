# Skill: /job-closeout

## Purpose
Structured end-of-job process to prevent callbacks and protect RHR's quality KPI.
Built from RHR's actual callback history (2025–2026 Operations Scoreboards).

## When to Run
Before the client walkthrough on any job wrapping up.

## Invocation
`/job-closeout [job address]`

---

## Workflow

### 1. Confirm RHR is Last on Site
Ask: "Has the RHR team been on site after all subcontractors?"

- If no: stop. Do not proceed with walkthrough until RHR does a final pass after every sub.
- If yes: continue.

### 2. Run the Pre-Walkthrough Punch List
Go through each item out loud or on paper before the client walks in.

#### Plumbing & Mechanical
- [ ] All faucets tested — no leaks, hot water working in every fixture
- [ ] All drains tested — no slow drains, no leaks under sinks
- [ ] GFI outlets tested (press test button, confirm reset)
- [ ] Smoke detectors present and functioning
- [ ] Any supply lines or shutoffs touched — confirm no bends, drips, or loose connections

#### Doors & Hardware
- [ ] Every door opens, closes, and latches properly
- [ ] Basement door (if applicable) shuts and seals correctly
- [ ] Cabinet doors aligned and secure
- [ ] Door jambs checked — especially around any flooring work

#### Paint & Finishes
- [ ] Walk every painted surface in good light — check for missed spots, thin coverage, uneven sheen
- [ ] Check corners, edges, and trim where tape lines were pulled
- [ ] Check caulk lines — no gaps, no cracking, no missed joints
- [ ] Flooring cuts around toilet bases, supply lines, and fixtures — confirm escutcheon covers the cut

#### Site Condition
- [ ] All trash removed — dumpster, job site, and client's property
- [ ] Client's belongings returned to original position if moved
- [ ] No materials, tools, or debris left behind
- [ ] Any surfaces used as work areas cleaned (counters, floors, etc.)

#### Scope Verification
- [ ] Walk the full scope of work — confirm every item in the contract is done
- [ ] No partial items left open without client awareness

### 3. Client Walkthrough
After the punch list is clean:
- Walk the client through each area of work
- Point out what was done — don't just ask "does everything look good?"
- Give them a chance to raise concerns before you leave
- If anything comes up: address it on the spot if possible, or set a specific return date

### 4. Log the Closeout
After the walkthrough, record:
- Date completed
- Any items the client flagged
- Any items found on punch list that needed fixing before walkthrough
- Lessons learned (anything that would have been a callback if not caught)

Update the project file in `projects/` with completion date and notes.

### 5. Set the 4-Week Follow-Up
Remind Caleb to check in with the client 4 weeks post-completion to confirm no callbacks.
Note the follow-up date in the project file.

---

## Common Callback Patterns (from RHR history)
These are the things that have actually come back — check these first:
- Missed paint spots (especially corners and edges)
- Plumbing leaks — faucets, drains, supply lines
- GFI not working
- Doors not shutting (especially basement doors)
- Trash left on site
- Caulking gaps
- Missing or non-functional smoke detectors
- Flooring cuts too big around fixtures

## Rules
- RHR must be last on site. No exceptions.
- Don't hand off to the client until the punch list is clean.
- If something can't be fixed before walkthrough, tell the client proactively — don't let them find it.
- Log every closeout. The scoreboard depends on it.
