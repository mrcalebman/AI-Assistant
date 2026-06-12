# Skill: /add-advisor

**Invocation:** `/add-advisor <name> <url-or-path> [<url-or-path> ...]`

Builds (or rebuilds) an advisor profile from their real public content. The profile only contains what the sources support — never padded with general internet knowledge.

---

## Steps

### 0. Setup

Normalize the advisor name to a folder slug: lowercase, spaces to hyphens (e.g., "Alex Hormozi" → `alex-hormozi`).

Create directories if they don't exist:
```
advisors/<slug>/
advisors/<slug>/sources/
```

Install yt-dlp if missing:
```bash
yt-dlp --version 2>/dev/null || (brew install yt-dlp 2>/dev/null || python3 -m pip install --user yt-dlp)
# Verify it's on PATH — if not, find it and add to PATH or use full path
```

---

### 1. Ingest Every Source

For each URL or file path provided:

#### YouTube URLs (youtube.com or youtu.be)

**Before ingesting: verify the speaker.** Run:
```bash
yt-dlp --no-check-certificates --skip-download \
  --print "%(title)s|||%(description)s" "<URL>" 2>/dev/null
```
Check the title and description. If this is an interview or conference talk, confirm the named advisor is actually the one speaking — not just a guest or subject being discussed. If you cannot confirm, ask before ingesting.

**Download captions:**
```bash
TMPDIR=$(mktemp -d)
yt-dlp --no-check-certificates --skip-download \
  --write-subs --write-auto-subs \
  --sub-langs "en" \
  --sub-format vtt \
  --output "$TMPDIR/transcript" \
  "<URL>" 2>&1
VTT_FILE=$(find "$TMPDIR" -name "*.vtt" | head -1)
```

Rules:
- Use exactly `"en"` for `--sub-langs`. Never `"en.*"` — it matches dozens of machine-translated tracks.
- Pass both `--write-subs` and `--write-auto-subs` in the same call.
- If HTTP 429: wait 15 seconds, retry once. Never more than two total attempts.
- Ignore yt-dlp warning noise (impersonation, JS runtime, missing formats). Judge success by whether a .vtt file appeared.
- If running in a cloud/server environment and getting HTTP 403: YouTube blocks cloud IPs. Report this and continue with other sources if any.
- If no .vtt file: record this source as FAILED, continue with remaining sources.

**Clean the VTT:**
```python
import re, sys
with open(sys.argv[1], 'r', encoding='utf-8') as f:
    raw = f.read()
lines = raw.split('\n')
cleaned = []
prev = ''
for line in lines:
    if re.match(r'^\d{2}:\d{2}', line): continue
    if re.match(r'^WEBVTT', line): continue
    if re.match(r'^NOTE', line): continue
    if re.match(r'^\d+$', line): continue
    if line.strip() == '': continue
    line = re.sub(r'<[^>]+>', '', line).strip()
    if not line: continue
    if line == prev: continue
    cleaned.append(line)
    prev = line
print(' '.join(cleaned))
```

Sanity check: if cleaned transcript is under 200 characters for a video over 2 minutes, record as FAILED.

**Strip ad reads:** Before saving, scan the cleaned text for sponsor/ad segment markers ("this video is sponsored by", "use code", "check out", "go to [url]"). Flag these sections in a note at the top of the source file but leave the raw text intact. Do NOT remove them from the file — just note their approximate location so the profile-builder can down-weight them.

**Save to:** `advisors/<slug>/sources/YYYY-MM-DD-<short-slug>.md`

File format:
```
# [Video Title]
Source: <URL>
Date fetched: YYYY-MM-DD
Speaker verified: yes / could not confirm

[AD NOTE: possible sponsor segment detected near line ~X]

---

[full cleaned transcript]
```

#### Article URLs

Fetch the page text:
```python
import urllib.request
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
# Strip HTML tags
import re
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
```

If the page is paywalled or returns an error: record as FAILED, continue.

Save to `advisors/<slug>/sources/` same format as above.

#### File Paths

Read the file directly. Save a copy to `advisors/<slug>/sources/` with a note of the original path.

---

### 2. Failure Handling

- If a source fails: note it, continue with remaining sources.
- If ALL sources fail: stop. Do not create or update the profile. Report all failures clearly.
- Never create an advisor from zero successfully-ingested sources.

---

### 3. Build the Profile

Read all files in `advisors/<slug>/sources/`. Write `advisors/<slug>/profile.md`:

```markdown
# [Advisor Name]

## Who They Are
2–3 sentences. Role, domain, why they matter.

## Core Beliefs and Principles
Each belief tied to something they actually said. Format:
- **[belief statement]** — "[paraphrase or near-quote]" (source: filename)

## How They Think
Their frameworks, mental models, decision rules. Only from sources.

## How They Talk
Tone, vocabulary, sentence style, signature phrases. Be specific enough
that their voice is distinct from every other advisor on the board.

## What They Push Back On
What this person predictably challenges. Supported by sources.

## Blind Spots
Where their advice is known to be weak or biased. Be honest — a profile
that pretends there are no blind spots is useless for board deliberation.

## Coverage Note
Topics the sources actually cover. If the sources are thin on a subject,
say so explicitly. Format:
- Strong coverage: [topics]
- Thin coverage: [topics] — extrapolation required
- Not covered at all: [topics]

If the profile is built from fewer than 2 sources: add a banner:
> ⚠️ THIN PROFILE — built from [N] source(s). Add more sources for a stronger persona.
```

Rule: if the sources don't support a section, write "not enough source material to populate this section" rather than padding from general knowledge.

---

### 4. Update the Roster

Open `advisors/BOARD.md` and add or update the row for this advisor:
```
| [Full Name] | [who they are, 8 words max] | [best consulted on, 10 words max] | YYYY-MM-DD | N |
```

---

### 5. Clean Up

Delete any temp VTT directories:
```bash
rm -rf "$TMPDIR"
```

---

### 6. Report

```
Advisor: [Full Name]
Sources ingested: N
Sources failed: N (list them if any)
Profile saved: advisors/<slug>/profile.md
Best consulted on: [the line from BOARD.md]

[paste the "Who They Are" and "Core Beliefs" sections so Caleb can sanity-check]
```

---

## Rebuilding an Existing Advisor

If `advisors/<slug>/` already exists, `/add-advisor` ingests the new sources into `sources/` and rebuilds `profile.md` from the full source set (all existing + new). The roster count updates to reflect the total.
