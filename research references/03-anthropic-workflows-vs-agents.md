---
type: concept
title: "Anthropic's Workflows vs Agents & Model Context Protocol (MCP)"
description: "Analysis of Anthropic's engineering framework distinguishing deterministic workflows from autonomous loops, the 5 core production patterns, and MCP tool architecture."
tags: [anthropic, workflows-vs-agents, mcp, prompt-chaining, orchestrator-workers]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "https://www.anthropic.com/engineering/building-effective-agents"
  - "https://modelcontextprotocol.io/"
---

# Anthropic's Workflows vs. Agents & Model Context Protocol (MCP)

## ðŸ’¡ Strategic Context & Rationale
*Foundational Survey:* [Top 5 Specifications](01-top-5-agent-specifications.md)  
*Upstream Discovery:* [Agent Opportunity Scan Architecture](../docs/architecture/arch-agent-opportunity-scan.md)

Anthropicâ€™s December 2024 engineering publication (*"Building Effective Agents"*, Schluntz & Zhang) provides the definitive practical guide for modern software engineering with LLMs. Its primary thesis establishes a strict dichotomy between **Workflows** and **Agents**.

---

## 1. The Critical Boundary: Workflows vs. Autonomous Agents

```text
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      WORKFLOWS                         â”‚
â”‚  â€¢ Deterministic control code and DAGs                 â”‚
â”‚  â€¢ LLMs execute fixed, predefined transformation steps â”‚
â”‚  â€¢ Predictable latency, bounded token cost, high trust â”‚
â”‚  â€¢ Recommended for 90% of software tasks               â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                           vs
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   AUTONOMOUS AGENTS                    â”‚
â”‚  â€¢ LLMs autonomously control loop iteration and tools  â”‚
â”‚  â€¢ Dynamic branching, environment feedback, trial/errorâ”‚
â”‚  â€¢ Unbounded horizon, higher token consumption         â”‚
â”‚  â€¢ Reserved for open-ended search, debugging, repair   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### The Engineering Rule
> *"Never deploy an autonomous ReAct loop where a deterministic workflow (Prompt Chain or Router DAG) can achieve the task with lower latency and predictable cost."*

This rule forms **Critical Gate CG-1** in `/agent-opportunity-scan` and the **Triage Gate** in `/build-agent`.

---

## 2. The 5 Core Production Patterns

Anthropic formalizes 5 composable structural design patterns:

### 1. Augmented LLM (The Basic Unit)
The foundation of every system: an LLM enhanced with system prompt instructions, external retrieval (RAG / `CONTEXT.md`), and deterministic tools.

### 2. Prompt Chaining
A sequential pipeline where step $N+1$ depends on the verified output of step $N$, with deterministic gates or validators between steps. Ideal for document transformation, PRD generation, and multi-stage code reviews.

### 3. Routing
An intent classifier that directs an input to specialized prompt templates, tools, or downstream subagents. Used in our suite by `choose-skills` to route intents.

### 4. Parallelization / Orchestrator-Workers (Fan-Out / Fan-In)
A central Lead Orchestrator decomposes a complex task into independent sub-problems, spawns parallel worker subagents, and synthesizes the outputs. This is the exact blueprint for our `multi-agent-squad` archetype.

### 5. Evaluator-Optimizer (Generator-Critic Loop)
One model produces candidate solutions (code, plan, spec) while a separate model (or test runner) evaluates the candidate against explicit criteria, iterating until tests pass. This is the foundation of our Test-Driven Development (`tdd`) and ToRA execution loops.

---

## 3. The Model Context Protocol (MCP) Standard

The open standard governing how agents interact with external tools and resources:
- **Client-Host-Server Architecture:** Decouples agents from proprietary APIs.
- **Three Core Primitives:**
  1. *Tools:* Executable functions with JSON schema arguments.
  2. *Resources:* Read-only data streams (file contents, database rows, git diffs).
  3. *Prompts:* Pre-configured workflow templates exposed by servers.
- **Role in Suite:** Both `build-agent` and `agent-opportunity-scan` map external integrations (e.g. GitHub, Stripe, Notion, Chrome DevTools) into standardized MCP tool definitions.

---

## ðŸ”— Related Knowledge Base Links
* ðŸ  [Master Index](index.md)
* ðŸ“š [Top 5 Foundational Specifications](01-top-5-agent-specifications.md)
* ðŸŽ¯ [Dual-Tier Viability Rubric](../docs/guides/guide-dual-tier-viability-rubric.md)
* ðŸ—ï¸ [Build Agent Engine Architecture](../docs/architecture/arch-build-agent-engine.md)

