---
type: guide
title: "Quick-Reference Guide: Dual-Tier Viability Rubric & Decision Trees"
description: "Engineer reference guide and decision trees for evaluating workflows against the 5 Critical Gates and 5 Optional Enhancers."
tags: [decision-tree, qualification-gates, viability-rubric, checklist]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "skills/02-agent-builder/agent-opportunity-scan/resources/candidate-rubric.md"
---

# Quick-Reference Guide: Dual-Tier Viability Rubric & Decision Trees

## 💡 Strategic Context & Rationale
*Master Index:* [index.md](../index.md)  
*Upstream Discovery:* [Architecture: Agent Opportunity Scan](../architecture/arch-agent-opportunity-scan.md)

Use this quick-reference checklist during planning or retro sessions to rapidly evaluate whether a task should become an **Agent**, a **Skill**, a **Hook**, or a **Script**.

---

## 1. The Decision Tree

```mermaid
flowchart TD
    Task["Candidate Task / Toil Pattern"] --> Q1{"Is execution sequence deterministic?"}
    Q1 -->|"YES"| D1["Deterministic Task:<br/>Write a PowerShell / Bash script or Git Hook"]
    Q1 -->|"NO"| Q2{"Does it mutate external files, shells, or APIs?"}
    
    Q2 -->|"NO"| D2["Cognitive / Text-Only Task:<br/>Write a Prompt Template or Skill"]
    Q2 -->|"YES"| Q3{"Does it encounter dynamic errors requiring self-repair?"}
    
    Q3 -->|"NO"| D3["Predictable Automation:<br/>Write a pre-commit hook or CI pipeline"]
    Q3 -->|"YES"| Q4{"Does it consume >= 15 min/wk of human toil?"}
    
    Q4 -->|"NO"| D4["Low ROI:<br/>Handle interactively; do not build agent"]
    Q4 -->|"YES"| Q5{"Can blast radius be bounded with git rollback?"}
    
    Q5 -->|"NO"| D5["High Irreversible Risk:<br/>Keep strictly manual human execution"]
    Q5 -->|"YES"| Agent["QUALIFIED AGENT CANDIDATE!<br/>Run /build-agent"]
```

---

## 2. The 5 Critical Gates Checklist

Before proposing or approving an agent, check all 5 boxes:
- [ ] **CG-1: Dynamic State & Branching:** Requires multi-turn planning and dynamic adaptation.
- [ ] **CG-2: External Tool Mutation:** Drives side-effects via tools (files, terminal, network).
- [ ] **CG-3: Reflexion & Error Recovery:** Catches exceptions and self-corrects without crashing.
- [ ] **CG-4: Measurable Toil Justification:** Costs $\ge 15$ mins/week or occurs frequently ($AVS \ge 50$).
- [ ] **CG-5: Containable Blast Radius:** Mutations can be rolled back via git stash.

---

## 3. Tier 2 Optional Enhancers (Bonus Scoring)

Count how many enhancers are met ($0$ to $5$):
- [ ] **OE-1: Episodic Cross-Session Memory** (+15% bonus)
- [ ] **OE-2: Multi-Perspective Deliberation** (+15% bonus $\to$ Promotes to `multi-agent-squad`)
- [ ] **OE-3: Persistent Sentinel Scheduling** (+15% bonus $\to$ Promotes to `autonomous-sentinel`)
- [ ] **OE-4: Dynamic MCP Tool Integration** (+15% bonus)
- [ ] **OE-5: Multimodal Sensory Grounding** (+15% bonus)

$$\text{AVS} = \frac{\text{Monthly Frequency} \times \text{Mean Toil (Minutes)}}{\text{Blast Radius Factor}} \times \left(1 + 0.15 \times N_{\text{optional}}\right)$$

---

## 🔗 Related Knowledge Base Links
* 🏠 [Master Index](../index.md)
* 🔍 [Agent Opportunity Scan Architecture](../architecture/arch-agent-opportunity-scan.md)
* 🧭 [Operational Workflow Guide](guide-dual-skill-operational-workflow.md)
