# Skill: /ingest

**Invocation:** `/ingest <youtube-url>`

Fetches a YouTube video's transcript, summarizes it, and files it in the knowledge base.

---

## Steps

### 1. Validate URL
If the URL is not a YouTube link (youtube.com or youtu.be), stop immediately:
> "This skill only handles YouTube URLs for now."

---

### 2. Fetch Metadata and Captions

Create a temp directory for this ingest run:
```bash
TMPDIR=$(mktemp -d)
```

Fetch metadata (title, channel, upload date, duration):
```bash
yt-dlp --skip-download --print "%(title)s|||%(channel)s|||%(upload_date)s|||%(duration_string)s" "<URL>" 2>/dev/null
```

Download English captions:
```bash
yt-dlp --skip-download \
  --write-subs --write-auto-subs \
  --sub-langs "en" \
  --sub-format vtt \
  --no-check-certificates \
  --output "$TMPDIR/transcript" \
  "<URL>"
```

**Key rules:**
- Use exactly `"en"` for `--sub-langs`. Never `"en.*"` — it matches dozens of machine-translated tracks.
- Pass both `--write-subs` and `--write-auto-subs` — some videos only have one type.
- If YouTube returns HTTP 429 (rate limit): wait 15 seconds, retry once. Never retry more than twice total.
- yt-dlp will print warnings about impersonation, JS runtime, and missing formats — ignore them. Judge success only by whether a `.vtt` file appeared in `$TMPDIR`.

Find the .vtt file:
```bash
VTT_FILE=$(find "$TMPDIR" -name "*.vtt" | head -1)
```

If no .vtt file exists after both attempts, stop:
> "This video has no captions — I can't ingest it."
**Never fabricate a transcript.**

---

### 3. Clean the Transcript

VTT auto-captions repeat every line 2–3 times with overlapping timestamps. Run this Python snippet:

```python
import re, sys

with open(sys.argv[1], 'r', encoding='utf-8') as f:
    raw = f.read()

# Remove WEBVTT header and NOTE blocks
lines = raw.split('\n')
cleaned = []
prev = ''
for line in lines:
    # Skip timestamps, cue numbers, WEBVTT header, NOTE lines, empty lines
    if re.match(r'^\d{2}:\d{2}', line): continue
    if re.match(r'^WEBVTT', line): continue
    if re.match(r'^NOTE', line): continue
    if re.match(r'^\d+$', line): continue
    if line.strip() == '': continue
    # Strip HTML tags
    line = re.sub(r'<[^>]+>', '', line).strip()
    if not line: continue
    # Remove consecutive duplicates
    if line == prev: continue
    cleaned.append(line)
    prev = line

print(' '.join(cleaned))
```

**Sanity check:** If the cleaned transcript is under 200 characters and the video is longer than 2 minutes, stop:
> "Transcript cleaned to under 200 characters — something went wrong. Not filing."

---

### 4. Summarize

Write four sections from the transcript:

**Summary (3–5 sentences):** What the video argues or teaches.

**Key Points (4–8 bullets):** The most important specific ideas.

**Why This Matters to Me (2–4 bullets):** Connect to Caleb's work at RHR using context from `context/work.md`, `context/current-priorities.md`, and `context/me.md`. Be specific — generic notes are useless.

**Action Items:** Concrete steps the video suggests. Label them clearly as the video's suggestions, not recommendations from this assistant.

---

### 5. File It

Target folder: `references/ingested/` (create if it doesn't exist).

Filename format: `YYYY-MM-DD-short-slug.md` where the date is today (date of ingestion) and the slug is a 3–5 word kebab-case version of the title.

File structure:
```
# [Video Title]

**Channel:** [channel name]
**URL:** [url]
**Upload date:** [YYYYMMDD → formatted as Month DD, YYYY]
**Duration:** [duration]
**Date ingested:** [today's date]

---

## Summary
[3–5 sentence summary]

## Key Points
- [bullet]
- [bullet]
...

## Why This Matters to Me
- [bullet]
...

## Action Items (video's suggestions)
- [bullet]
...

---

## Full Transcript
[full cleaned transcript]
```

---

### 6. Update the Index

Add one line to `references/INDEX.md`:
```
- [YYYY-MM-DD-short-slug.md](ingested/YYYY-MM-DD-short-slug.md) — [one sentence: what the video teaches]
```

---

### 7. Clean Up

Delete the temp directory:
```bash
rm -rf "$TMPDIR"
```

---

### 8. Report

End with a receipt:
```
Filed: references/ingested/YYYY-MM-DD-short-slug.md
Video: [title] — [channel]

[paste the summary and key points here so Caleb can read without opening the file]
```

---

## Error Handling

| Situation | Response |
|---|---|
| Not a YouTube URL | "This skill only handles YouTube URLs for now." |
| Private / region-locked video | Show the actual yt-dlp error. Tell Caleb what to do (e.g., check if video is public, try a VPN). |
| HTTP 429 rate limit | Wait 15s, retry once. If still 429, report it. |
| No captions found | "This video has no captions — I can't ingest it." |
| Transcript under 200 chars | Report the issue, don't file. |
| Any other yt-dlp failure | Show the actual error output, don't guess at the cause. |
| HTTP 403 from a cloud/server environment | YouTube blocks cloud provider IPs. This skill must be run on a personal machine or a residential IP. Show this message and stop. |
