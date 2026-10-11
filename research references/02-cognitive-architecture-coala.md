---
type: concept
title: "CoALA Cognitive Architecture for Language Agents"
description: "Detailed analysis of the Cognitive Architectures for Language Agents (CoALA) framework, memory taxonomy, and action space decoupling seams."
tags: [coala, cognitive-architecture, memory-hierarchy, action-space]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "https://arxiv.org/abs/2309.02427"
---

# CoALA Cognitive Architecture for Language Agents

## ðŸ’¡ Strategic Context & Rationale
*Foundational Survey:* [Top 5 Specifications](01-top-5-agent-specifications.md)  
*Runtime Implementation:* [Architecture: Runtime Harness & Armor](../docs/architecture/arch-runtime-harness-and-armor.md)

CoALA (Sumers, Yao, Narasimhan, Griffiths, 2024) provides the formal computational and structural blueprint for engineering AI agents that go beyond stateless prompt calls.

---

## 1. The CoALA Memory Taxonomy

CoALA organizes agent memory into four functionally distinct substrates:

```text
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   WORKING MEMORY                       â”‚
â”‚  â€¢ Active context window buffer                        â”‚
â”‚  â€¢ Current execution goal & sub-goals                  â”‚
â”‚  â€¢ Scratchpad variables & intermediate plan states     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
          â–²                     â–²                   â–²
          â”‚ Retrieval           â”‚ Logs              â”‚ Lookups
          â–¼                     â–¼                   â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ EPISODIC MEMORY  â”‚  â”‚ SEMANTIC MEMORY  â”‚  â”‚PROCEDURAL MEMORY â”‚
â”‚ Past execution   â”‚  â”‚ Declarative domainâ”‚  â”‚ Reusable skills,â”‚
â”‚ trials, traces,  â”‚  â”‚ knowledge, facts, â”‚  â”‚ system prompts, â”‚
â”‚ & failure logs   â”‚  â”‚ CONTEXT.md rules  â”‚  â”‚ tool schemas    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

1. **Working Memory:** The fast, volatile context window holding the active goal, current observation, and immediate reasoning scratchpad. Constrained by token limits; requires periodic compaction.
2. **Episodic Memory:** Chronological database of previous executions, task outcomes, and reflection traces (`.agents/memory/*.jsonl`). Allows agents to learn from past mistakes across sessions.
3. **Semantic Memory:** Static declarative knowledge base containing domain invariants, coding conventions, architectural decisions, and `CONTEXT.md`.
4. **Procedural Memory:** The executable instructions, prompt templates, tool schemas, and runner harnesses (`runner.py`, `agent.md`) that dictate how the agent operates.

---

## 2. Action Space Decoupling: Internal vs. External Actions

The cornerstone invariant of CoALA is the strict computational separation of an agent's action space:

```mermaid
flowchart TD
    Reasoning["LLM Reasoning Core"] --> Decision{"Action Classifier"}
    Decision -->|"Internal Action"| Int["Memory Mutation / Cognitive State<br/>â€¢ Update internal belief state<br/>â€¢ Query long-term episodic memory<br/>â€¢ Generate self-reflection note<br/>â€¢ Validate plan feasibility"]
    Decision -->|"External Action"| Gate{"Blast Radius Interceptor & Safety Check"}
    Gate -->|"Approved"| Ext["Environment Mutation<br/>â€¢ Write file to disk<br/>â€¢ Execute shell command<br/>â€¢ Make network API call<br/>â€¢ Message human / user"]
    Gate -->|"Blocked"| Rollback["Safe Rejection / Rollback"]
```

### Why Decoupling is Mandatory
In naive ReAct agents, internal planning tokens and external API calls are mingled indiscriminately, causing:
- Accidental execution of half-formed plans.
- Hallucinated commands triggered before verifying schema compliance.
- Inability to roll back corrupted local state.

In our architecture, an agent must formulate and verify its internal belief state **before** triggering an external environment mutation.

---

## 3. The Generalized 3-Stage Decision Cycle

Every agent loop in the suite executes CoALA's 3-stage decision cycle:
1. **Planning & Retrieval:** The agent reads active working memory, retrieves relevant domain rules from semantic memory, and pulls past failure lessons from episodic memory.
2. **Action Selection:** The model evaluates candidate actions, chooses between an internal cognitive update or an external tool execution, and validates parameters against schema contracts.
3. **Execution & Feedback:** If an external action is selected, the runtime executes the tool, captures stdout/stderr, applies payload armor (16KB ceiling), and updates working memory with the observation.

---

## ðŸ”— Related Knowledge Base Links
* ðŸ  [Master Index](index.md)
* ðŸ“š [Top 5 Foundational Specifications](01-top-5-agent-specifications.md)
* ðŸ—ï¸ [Build Agent Engine Architecture](../docs/architecture/arch-build-agent-engine.md)
* ðŸ›¡ï¸ [Runtime Harness Specification](../docs/architecture/arch-runtime-harness-and-armor.md)

