"""
Callback root-cause analyzer agent for Redemption Home Remodeling.

Usage:
    python agent.py "Johnson Kitchen" "Grout cracking along backsplash, 2 weeks after completion"
    python agent.py --list
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

from anthropic import Anthropic

DATA_FILE = Path(__file__).parent / "data.json"
LOG_FILE = Path(__file__).parent / "findings.jsonl"

client = Anthropic()


# ── Data helpers ──────────────────────────────────────────────────────────────

def _load_data() -> dict:
    with open(DATA_FILE) as f:
        return json.load(f)


def _save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Tool implementations ──────────────────────────────────────────────────────

def get_callback_history(project_name: str) -> dict:
    data = _load_data()
    project = data["projects"].get(project_name)
    if not project:
        available = list(data["projects"].keys())
        return {"error": f"Project not found. Available: {available}"}
    return {"project": project_name, **project}


def get_trade_checklist(trade: str) -> dict:
    checklists = {
        "tile": [
            "substrate moisture content checked before install",
            "subfloor deflection within spec (L/360)",
            "expansion joints at perimeter and field breaks",
            "back-butter coverage >85%",
            "grout fully cured before water exposure (72h min)",
        ],
        "paint": [
            "surface sanded and primed",
            "humidity <50% at time of application",
            "temperature 50–85°F during and 24h after",
            "bath/kitchen areas use moisture-resistant sheen (eggshell min)",
            "two coats applied",
        ],
        "caulk": [
            "surfaces clean and dry before application",
            "100% silicone used at wet areas",
            "joint width 1/8\"–3/8\"",
            "tooled smooth and left undisturbed 24h",
            "full cure (7 days) before water exposure",
        ],
        "drywall": [
            "moisture barrier behind tile/wet areas",
            "screws countersunk, not stripped",
            "seams taped and feathered",
            "primed before paint",
        ],
        "flooring": [
            "acclimation period completed (48–72h)",
            "subfloor level within 3/16\" per 10'",
            "expansion gap maintained at perimeter",
            "transitions installed",
        ],
    }
    items = checklists.get(trade.lower())
    if not items:
        return {"trade": trade, "error": "no checklist found", "available_trades": list(checklists.keys())}
    return {"trade": trade, "checklist": items}


def log_finding(project_name: str, issue: str, root_cause: str, prevention: str) -> dict:
    entry = {
        "timestamp": datetime.now().isoformat(),
        "project": project_name,
        "issue": issue,
        "root_cause": root_cause,
        "prevention": prevention,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Mark as resolved in project data
    data = _load_data()
    project = data["projects"].get(project_name)
    if project:
        for cb in project.get("callbacks", []):
            if not cb["resolved"] and issue.lower() in cb["issue"].lower():
                cb["resolved"] = True
                cb["fix"] = root_cause
        _save_data(data)

    return {"status": "logged", "entry": entry}


def list_projects() -> dict:
    data = _load_data()
    summary = {}
    for name, proj in data["projects"].items():
        open_cbs = [c for c in proj.get("callbacks", []) if not c["resolved"]]
        summary[name] = {
            "completed": proj["completed"],
            "trades": proj["trades"],
            "open_callbacks": len(open_cbs),
            "total_callbacks": len(proj.get("callbacks", [])),
        }
    return {"projects": summary}


# ── Tool definitions ──────────────────────────────────────────────────────────

TOOLS = [
    {
        "name": "get_callback_history",
        "description": "Get full callback history for a project, including past issues and whether they were resolved.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "description": "Exact project name"}
            },
            "required": ["project_name"]
        }
    },
    {
        "name": "get_trade_checklist",
        "description": "Get the quality-control checklist for a trade. Use this to identify which checklist items were likely missed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "trade": {"type": "string", "description": "Trade name: tile, paint, caulk, drywall, flooring"}
            },
            "required": ["trade"]
        }
    },
    {
        "name": "log_finding",
        "description": "Save the root-cause analysis and prevention recommendation to the findings log. Call this once you have reached a conclusion.",
        "input_schema": {
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "issue": {"type": "string", "description": "The callback issue as reported"},
                "root_cause": {"type": "string", "description": "Most likely root cause based on history and checklist"},
                "prevention": {"type": "string", "description": "Specific action to prevent this on future jobs — be concrete"},
            },
            "required": ["project_name", "issue", "root_cause", "prevention"]
        }
    },
    {
        "name": "list_projects",
        "description": "List all projects with open callback counts.",
        "input_schema": {"type": "object", "properties": {}}
    }
]


# ── Tool dispatcher ───────────────────────────────────────────────────────────

def run_tool(name: str, inputs: dict) -> str:
    dispatch = {
        "get_callback_history": get_callback_history,
        "get_trade_checklist": get_trade_checklist,
        "log_finding": log_finding,
        "list_projects": list_projects,
    }
    fn = dispatch.get(name)
    if not fn:
        return json.dumps({"error": f"unknown tool: {name}"})
    return json.dumps(fn(**inputs))


# ── Agentic loop ──────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a construction quality analyst for Redemption Home Remodeling.
Your job is to analyze callback issues (warranty callbacks after project completion), identify root causes,
and provide concrete prevention steps.

Be direct and specific. Reference the trade checklist items when identifying what was likely missed.
Always call log_finding before your final response.
End with a plain-language summary: root cause in one sentence, prevention in one sentence."""


def analyze_callback(project_name: str, issue_description: str) -> str:
    messages = [
        {
            "role": "user",
            "content": (
                f"Project: {project_name}\n"
                f"Callback issue: {issue_description}\n\n"
                "Investigate this callback. Check the project's history and the relevant trade checklist, "
                "identify the root cause, log your finding, then give me a plain-language summary."
            )
        }
    ]

    while True:
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return "(no text response)"

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [tool] {block.name}({json.dumps(block.input)})")
                    result = run_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            messages.append({"role": "user", "content": tool_results})

        else:
            return f"Unexpected stop reason: {response.stop_reason}"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        result = list_projects()
        print("\nActive Projects\n" + "─" * 40)
        for name, info in result["projects"].items():
            open_cb = info["open_callbacks"]
            flag = " ⚠" if open_cb > 0 else ""
            print(f"{name}{flag}")
            print(f"  Completed: {info['completed']}  |  Trades: {', '.join(info['trades'])}")
            print(f"  Callbacks: {open_cb} open / {info['total_callbacks']} total")
        return

    if len(sys.argv) < 3:
        print("Usage:")
        print('  python agent.py "Project Name" "Issue description"')
        print('  python agent.py --list')
        sys.exit(1)

    project_name = sys.argv[1]
    issue = sys.argv[2]

    print(f"\nAnalyzing callback for {project_name}...")
    print(f"Issue: {issue}\n")
    print("─" * 60)

    summary = analyze_callback(project_name, issue)

    print("\n── Root Cause Analysis ─────────────────────────────────────")
    print(summary)
    print(f"\nFinding logged to: {LOG_FILE}")


if __name__ == "__main__":
    main()
