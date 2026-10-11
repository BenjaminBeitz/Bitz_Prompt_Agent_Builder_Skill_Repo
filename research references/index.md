---
type: index
title: "Academic Research References: OKF Master Index"
description: "Master Open Knowledge Format (OKF v0.2) index linking foundational research papers, surveys, cognitive architectures, and systems engineering invariants."
version: "1.0.0"
okf_version: "0.2"
status: active
timestamp: 2026-10-11T12:00:00Z
verified: true
verified_by: "@BenjaminBeitz"
---

# Academic Research References: OKF Master Index

Welcome to the **Open Knowledge Format (OKF v0.2)** foundational research library for the **Bitz Prompt & Agent Builder Skills Suite**.

This knowledge bundle contains the theoretical, cognitive, and systems engineering substrate underpinning both the **Scientific Prompt Engineering Suite** (`skills/01-prompt-engineering/`) and the **Autonomous Agent Engineering Suite** (`skills/02-agent-builder/`).

---

## 🧭 Foundational Research Knowledge Map

```text
research references/
├── index.md                             # This Master Research Index
├── 00-the-prompt-report-survey.md       # Schulhoff et al. (2025) 82-page survey & Figure 2.2 Macro-Taxonomy
├── 01-top-5-agent-specifications.md     # Monumental survey of Top 5 Agent Specifications (Xi et al., CoALA, etc.)
├── 02-cognitive-architecture-coala.md   # CoALA memory hierarchy & internal vs. external action spaces
├── 03-anthropic-workflows-vs-agents.md  # Anthropic workflow patterns & Model Context Protocol (MCP) standard
├── 04-oracle-agent-spec-protocol.md    # Declarative YAML schemas & universal REST/SSE Agent Protocol
└── 05-systems-engineering-invariants.md# Physical runtime invariants: payload armor, context compaction, git rollback
```

---

## 📚 1. Scientific Prompt Engineering Literature

- [00. The Prompt Report: Systematic Survey](00-the-prompt-report-survey.md)  
  *Sander Schulhoff et al. (2025)* — Synthesis of the definitive 82-page survey. Catalogs Figure 2.2 macro-taxonomy, 6 prompt families, 33 prompt techniques, and empirical failure modes. Grounds all 10 prompt engineering skills in `skills/01-prompt-engineering/`.

---

## 🤖 2. Autonomous Agent Engineering Literature

- [01. Top 5 Foundational Specifications & Guides](01-top-5-agent-specifications.md)  
  *Xi et al. (2023) & Agent Community* — Exhaustive comparative analysis across the 5 authoritative agent design standards: Xi et al. (86pp survey), Sumers et al. (CoALA), Anthropic Agent Protocol, Oracle Declarative Spec, and Andrew Ng / Harrison Chase Agentic Workflows.

- [02. CoALA Cognitive Architecture Deep Dive](02-cognitive-architecture-coala.md)  
  *Sumers, Yao, Narasimhan, Griffiths (Princeton & Berkeley, 2023)* — Formalization of Working, Episodic, Semantic, and Procedural memory structures, coupled with the fundamental separation between internal cognitive actions and external world-state actions.

- [03. Anthropic Workflows vs. Agents & MCP](03-anthropic-workflows-vs-agents.md)  
  *Anthropic Engineering (2024)* — Architectural demarcation between deterministic LLM workflows (chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer) and open-ended autonomous agent loops. Integrates the Model Context Protocol (MCP) standard.

- [04. Oracle Agent Spec & Universal Agent Protocol](04-oracle-agent-spec-protocol.md)  
  *Oracle Labs & AI Agent Protocol Working Group (2024)* — Declarative YAML schema specifications for framework-agnostic agent definitions (`agent.spec.yaml`) and universal REST/SSE streaming endpoints (`/tasks`, `/steps`).

- [05. Systems Engineering Invariants & Failure Mitigation](05-systems-engineering-invariants.md)  
  *Production Systems Engineering Standard (2025)* — Hard physical computing constraints: 16KB tool payload armor, deterministic JSON serialization, 70% memory compaction barriers, and git worktree rollback guards.

---

## 🔗 Cross-Bundle Navigation

- 🏛️ **System Architectures:** [docs/architecture/index.md](../docs/architecture/index.md)
- 🛠️ **Engineering Skills Library:** [skills/index.md](../skills/index.md)
- ⚙️ **Automation Scripts:** [scripts/index.md](../scripts/index.md)
