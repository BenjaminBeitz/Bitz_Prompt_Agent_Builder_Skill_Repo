---
type: guide
title: "Operational Workflow Guide: Using Opportunity Scan and Build Agent Together"
description: "End-to-end practical user guide detailing how to discover workflows via /agent-opportunity-scan and construct production systems via /build-agent in strict sequence."
tags: [user-guide, workflow-guide, sequential-execution, build-agent, opportunity-scan]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "skills/02-agent-builder/agent-opportunity-scan/SKILL.md"
  - "skills/02-agent-builder/build-agent/SKILL.md"
---

# Operational Workflow Guide: Using Opportunity Scan and Build Agent Together

## 💡 Strategic Context & Rationale
*Master Index:* [index.md](../index.md)  
*Pipeline Architecture:* [Sequential Pipeline Integration](../architecture/arch-sequential-pipeline-integration.md)

This guide provides the definitive protocol for running `/agent-opportunity-scan` and `/build-agent` as a unified, two-stage engineering loop.

---

## 1. The Two-Stage Sequential Rule

> [!IMPORTANT]
> **Stage 0 discovers $N$ candidates; Stage 1 builds EXACTLY ONE candidate at a time.**  
> Do not attempt to build multiple agents simultaneously. Select the highest-priority candidate from the scan, complete its construction, verify its test harness, and then iterate.

```text
Step 1: Scan Target (Session run or log window) via /agent-opportunity-scan
                 ↓
Step 2: Review Qualified Candidates & Viability Scores (AVS)
                 ↓
Step 3: Select ONE candidate number
                 ↓
Step 4: Execute /build-agent with pre-filled candidate intake
                 ↓
Step 5: Approve Spec Sheet & fast-forward 4-station interview
                 ↓
Step 6: Live Scaffolding, --health / --mock tests, & registry activation
```

---

## 2. Step-by-Step Walkthrough

### Step 1: Execute the Opportunity Scan
Choose the mode that fits your current context:

#### Reactive Mode (Post-Run Retrospective)
You just finished a difficult task and noticed repetitive toil or test friction:
```bash
/agent-opportunity-scan "current session transcript" "find test flakiness and encoding friction"
```
Or point directly to a transcript:
```bash
/agent-opportunity-scan ".system_generated/logs/transcript.jsonl"
```

#### Proactive Mode (Mining Weeks of Logs)
You want to discover recurring toil across recent development sprints:
```bash
/agent-opportunity-scan "~/.agents/history.jsonl" "focus on git and review toil"
```

### Step 2: Review Scanner Output
The scanner evaluates candidate workflows across the **5 Critical Gates** and ranks passing candidates by their **Agent Viability Score (AVS)**. It presents the candidates:

```text
Found 3 Qualified Agent Opportunities:

1. pipeline-stage-runner (solo-tool-user) — AVS: 322.0
   - Projected Savings: ~7.0 hours/month
   - Critical Gates: 5/5 PASSED | Optional Enhancers: 1/5
   - Direct Command: /build-agent "pipeline-stage-runner: A solo tool-user..."

2. windows-compat-guard (solo-tool-user) — AVS: 276.0
   - Projected Savings: ~4.0 hours/month
   - Critical Gates: 5/5 PASSED | Optional Enhancers: 1/5
   - Direct Command: /build-agent "windows-compat-guard: A solo tool-user..."
```

### Step 3: Trigger `/build-agent`
Select your chosen candidate and run its exact command:
```bash
/build-agent "pipeline-stage-runner: A solo tool-user agent that ingests a multi-phase implementation plan, runs Phase N, verifies passing tests, and automatically transitions to Phase N+1 without requiring human prompt overhead."
```

### Step 4: The 4-Station Walkthrough & Scaffolding
Because the scanner already specified the tool requirements, Definition of Done, and Fired Conditions:
1. **Spec Sheet Approval:** The Spec Sheet is instantly generated. Reply `Approve`.
2. **Interview Fast-Forward:** `/build-agent` fast-forwards unambiguous defaults, asking only 1–2 clarifying questions about blast radius.
3. **Automated Verification:** The agent runs `--health` and `--mock` offline tests, then registers the new agent into `.agents/agents.json`.

---

## 🔗 Related Knowledge Base Links
* 🏠 [Master Index](../index.md)
* 🏗️ [Build Agent Engine Architecture](../architecture/arch-build-agent-engine.md)
* 🔍 [Agent Opportunity Scan Architecture](../architecture/arch-agent-opportunity-scan.md)
* 🛠️ [Authoring & Scaffolding Guide](guide-authoring-and-scaffolding-agents.md)
