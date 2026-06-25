# MacBook Air 2020 Setup Plan

**Created:** 2026-06-25
**Status:** Pending — new machine not yet received

---

## Context

Caleb is transferring from an older laptop to a MacBook Air 2020 (16GB RAM). Primary goals:
- Continue AI Assistant work without interruption (repo already on GitHub)
- Install Claude Code desktop app
- Connect Claude Code to Trello
- Set up a clean, functional machine for daily work

---

## Phase 1 — Before You Touch the New Mac

- [ ] Confirm AI-Assistant repo is fully committed and pushed to GitHub
- [ ] Note Claude Code version on old machine: `claude --version`
- [ ] Have these credentials ready:
  - GitHub (email + password or SSH key)
  - Anthropic account (claude.ai)
  - Trello account
  - Google account (Gmail, Calendar, Drive — already integrated)
  - Apple ID

---

## Phase 2 — New Mac Initial Setup

- [ ] Sign into Apple ID / iCloud
- [ ] Run Software Update — get macOS fully current before installing anything
- [ ] Set up Touch ID and password
- [ ] Set system preferences (display, notifications, etc.) to your liking

---

## Phase 3 — Core Developer Tools

- [ ] Install Homebrew: go to brew.sh and follow instructions
- [ ] `brew install git`
- [ ] `brew install node`
- [ ] Configure Git identity:
  - `git config --global user.name "Caleb Nelson"`
  - `git config --global user.email "caleb.an97@gmail.com"`
- [ ] Generate SSH key and add to GitHub (so `git push` works without password):
  - `ssh-keygen -t ed25519 -C "caleb.an97@gmail.com"`
  - Add public key to GitHub → Settings → SSH Keys

---

## Phase 4 — Claude Code

- [ ] Install: `npm install -g @anthropic-ai/claude-code`
- [ ] Authenticate: run `claude` — will open browser to log in via Anthropic account
- [ ] Clone AI-Assistant repo: `git clone git@github.com:<your-repo-path>/AI-Assistant.git`
- [ ] Open the repo in Claude Code and verify CLAUDE.md and context files load correctly
- [ ] Run a quick session to confirm memory and context are intact

**Desktop App (if desired):**
- Download Claude desktop app from claude.ai/download — separate from Claude Code CLI but useful to have

---

## Phase 5 — Trello Integration (MCP)

This connects Claude Code directly to Trello so the assistant can read boards, create/move cards, update the scoreboard, etc.

Caleb's Trello structure:
- One board per active project
- A master board tracking all projects in one place
- A WIG scoreboard board
- A few other boards

Steps:
- [ ] Log into Trello → go to https://trello.com/app-key → copy your API Key
- [ ] Generate a Token on the same page
- [ ] Add MCP server config to Claude Code settings (walk through this step-by-step when ready)
- [ ] Test: ask the assistant to list your Trello boards

---

## Phase 6 — Other Applications

Download as needed:
- [ ] Google Chrome or Arc
- [ ] VS Code (if used)
- [ ] Slack (if used for team comms)
- [ ] Any other apps from old machine you use regularly

---

## Notes

- AI-Assistant repo is already on GitHub — no data loss risk for that work
- Gmail, Google Calendar, Google Drive integrations are already configured in Claude Code and will carry over once Claude Code is set up and the repo is cloned
- Trello is the main new integration to set up

---

## When Ready to Execute

Tell the assistant "let's set up the new MacBook" and we'll go one step at a time.
