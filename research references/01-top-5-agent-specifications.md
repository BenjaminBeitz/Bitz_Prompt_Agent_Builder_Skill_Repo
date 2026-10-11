---
type: concept
title: "Top 5 Foundational Specifications and Guides for AI Agents"
description: "Comprehensive survey and comparative synthesis of the top 5 academic, open-source, production, and video specifications for engineering autonomous AI agents."
tags: [agent-specifications, literature-survey, cognitive-architectures, benchmarks]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "https://arxiv.org/abs/2309.07864"
  - "https://arxiv.org/abs/2309.02427"
  - "https://www.anthropic.com/engineering/building-effective-agents"
  - "https://github.com/oracle/agent-spec"
  - "https://github.com/AI-Engineer-Foundation/agentprotocol.ai"
---

# Top 5 Foundational Specifications and Guides for AI Agents

## 💡 Strategic Context & Rationale
*Master Index:* [index.md](index.md)  
*Architectural Implementation:* [Architecture: Build Agent Engine](../docs/architecture/arch-build-agent-engine.md)

In this repository, the Prompt Skills Suite (`skills/01-alignment-intent/`) was engineered from *The Prompt Report* (Schulhoff et al., 2025). To build an equivalent, rigorous **Autonomous Agent Engineering Suite** (`build-agent` and `agent-opportunity-scan`), we conducted a comprehensive deep-literature investigation targeting academic repositories, open specifications on GitHub, first-party frontier lab engineering guides, and canonical video masterclasses.

---

## 1. The Top 5 Foundational Standards

### 1. The Encyclopedic Academic Treatise: Xi et al. (Fudan University, 2025)
- **Title:** *"The Rise and Potential of Large Language Model Based Agents: A Survey"* ([arXiv:2309.07864](https://arxiv.org/abs/2309.07864)).
- **Scale:** 86 pages, 12 figures, companion paper repository [`WooooDyy/LLM-Agent-Paper-List`](https://github.com/WooooDyy/LLM-Agent-Paper-List).
- **Core Contribution:** The direct academic twin to *The Prompt Report*. It classifies agent systems into a complete cognitive taxonomy:
  - **The Brain:** Planning (single-path, tree search, external symbolic planners), Memory hierarchy (working, episodic, semantic, perceptual), Reflexion/self-criticism loops.
  - **The Perception Module:** Textual parsing, multimodal sensory grounding, environmental feedback ingestion.
  - **The Action Module:** Tool use (APIs, calculators, web search), code execution in sandboxes, embodied actuation.
  - **Multi-Agent Topologies:** Cooperative workflows, competitive debate/adversarial validation, human-agent collaboration.
  - **Failure Modes:** Hallucination compounding, long-horizon plan degradation, context window saturation.

### 2. The Formal Cognitive Systems Specification: CoALA (Princeton, Stanford, DeepMind, 2024)
- **Title:** *"Cognitive Architectures for Language Agents"* ([TMLR / arXiv:2309.02427](https://arxiv.org/abs/2309.02427)).
- **Authors:** Theodore R. Sumers, Shunyu Yao (creator of ReAct), Karthik Narasimhan, Thomas L. Griffiths.
- **Core Contribution:** Adapts 40 years of cognitive science (Newell's Soar, Anderson's ACT-R) to LLM systems, formalizing:
  - **Memory Modularization:** Working memory (active goals & buffer), Episodic memory (historical execution logs), Semantic memory (declarative domain rules), Procedural memory (skills & tool schemas).
  - **Action Space Decoupling:** Non-negotiable boundary between *Internal Actions* (memory mutation, belief state updates, self-critique) and *External Actions* (environment mutations, API executions, shell commands).
  - **3-Stage Generalized Decision Cycle:** (1) Retrieval/Planning $\to$ (2) Action Selection $\to$ (3) Execution & Learning.

### 3. The Production Engineering Bible: Anthropic's "Building Effective Agents" & MCP (2024)
- **Authors:** Erik Schluntz and Barry Zhang (Anthropic Engineering).
- **Venues:** [Anthropic Engineering Guide](https://www.anthropic.com/engineering/building-effective-agents) and [Model Context Protocol (MCP)](https://modelcontextprotocol.io/).
- **Core Contribution:** The industry standard for separating deterministic workflows from autonomous loops:
  - **Workflows vs. Agents Boundary:** Workflows are deterministic DAGs where LLMs execute predefined steps (recommended for 90% of tasks for low latency and predictability). Agents are systems where LLMs autonomously determine control flow and tool usage.
  - **5 Core Patterns:** Augmented LLM, Prompt Chaining, Routing, Orchestrator-Workers (fan-out/fan-in), Evaluator-Optimizer.
  - **MCP Standard:** Open protocol for discovering, authenticating, and invoking tools without vendor lock-in.

### 4. Open Declarative Specifications: Oracle `agent-spec` & Agent Protocol
- **Repositories:** [`oracle/agent-spec`](https://github.com/oracle/agent-spec) and [`AI-Engineer-Foundation/agentprotocol.ai`](https://github.com/AI-Engineer-Foundation/agentprotocol.ai).
- **Core Contribution:** Framework-agnostic declarative YAML schemas defining agents as data rather than code:
  - Models tools, components, permissions, state transitions, and decision nodes declaratively.
  - Standardizes the universal REST/SSE agent lifecycle: `/tasks`, `/tasks/{id}/steps`, and `/tasks/{id}/artifacts`.

### 5. Canonical Video Masterclasses: Andrew Ng & Harrison Chase (YouTube)
- **Andrew Ng (DeepLearning.AI):** The 4 Agentic Design Patterns (Reflection, Tool Use, Planning, Multi-Agent Collaboration).
- **Harrison Chase (LangChain / Sequoia Capital):** The Tripartite Agent Architecture (1. The Model, 2. The Runtime Harness/Middleware, 3. Tripartite Long-Term Memory).

---

## 2. Comparative Matrix

| Specification | Primary Domain | Taxonomy Depth | Architectural Rigor | Production Usability | Role in Suite |
|---|---|---|---|---|---|
| **Xi et al. (Fudan)** | Academic Survey | Exhaustive (86 pp) | Very High | Moderate | Theoretical Foundation |
| **CoALA (Princeton)** | Cognitive Architecture | High (19 pp) | Highest | High | Action Space Decoupling |
| **Anthropic Guide & MCP** | Production Systems | Focused Article | High | Highest | Workflows vs Agents & Tools |
| **Oracle `agent-spec`** | Open GitHub Specs | High (Schemas) | High | Highest | Declarative YAML Format |
| **Ng & Chase Talks** | Pedagogical / Industry | High | High | Highest | Community Vocabulary |

---

## 3. The 4 Invariant Agent Architecture Laws

Derived from this research and enforced across our entire engineering suite:
1. **Workflow-First Triage Law (Anthropic Â§2):** Never deploy an autonomous ReAct loop where a deterministic workflow (Prompt Chain or Router DAG) can achieve the task with lower latency and predictable cost.
2. **Action Space Decoupling Law (CoALA Â§3):** Strictly separate *Internal Actions* (memory mutation, belief state updates, self-notes) from *External Actions* (file mutations, shell execution, external APIs).
3. **Fail-Safe Blast Radius Invariant (Zero-Trust Security):** Prohibit destructive shell commands programmatically (`rm -rf /`, `git push --force`), enforce human confirmation barriers on high-blast-radius actions, and sanitize secrets.
4. **Deterministic Working Tree Rollback (SWE-bench & PIV Loop):** Take an internal git checkpoint (`git stash create`) upon task entry. If execution aborts or 3-strike reflexion fails, automatically rollback the working tree.

---

## ðŸ”— Related Knowledge Base Links
* ðŸ  [Master Index](index.md)
* ðŸ§  [CoALA Cognitive Architecture Deep Dive](02-cognitive-architecture-coala.md)
* âš™ï¸ [Anthropic Workflows vs Agents](03-anthropic-workflows-vs-agents.md)
* ðŸ“„ [Oracle Agent Spec & Protocol](04-oracle-agent-spec-protocol.md)
* ðŸ›¡ï¸ [Systems Engineering Invariants](05-systems-engineering-invariants.md)

