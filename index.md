---
type: index
title: "Bitz Prompt & Agent Builder Suite: OKF Master Root Index"
description: "Master Open Knowledge Format (OKF v0.2) root index anchoring the entire repository knowledge graph, architecture specifications, research treatises, and skills catalog."
version: "1.0.0"
okf_version: "0.2"
status: active
timestamp: 2026-10-11T12:00:00Z
verified: true
verified_by: "@BenjaminBeitz"
---

# Bitz Prompt & Agent Builder Suite: OKF Master Root Index

Welcome to the **Open Knowledge Format (OKF v0.2)** root index for the **Bitz Prompt & Agent Builder Skills Suite**.

This repository is organized as a verified OKF v0.2 knowledge graph, connecting empirical NLP prompt engineering literature and autonomous agent cognitive architectures to 13 production-grade Google Antigravity skills.

---

## 🧭 Master Knowledge Graph

```text
.
├── index.md                             # Canonical OKF Root Index
├── README.md                            # GitHub Repository Home & Operational Guide
├── research references/                 # Academic Literature & Foundations
│   ├── index.md                         # Research Foundations Index
│   ├── 00-the-prompt-report-survey.md
│   ├── 01-top-5-agent-specifications.md
│   ├── 02-cognitive-architecture-coala.md
│   ├── 03-anthropic-workflows-vs-agents.md
│   ├── 04-oracle-agent-spec-protocol.md
│   └── 05-systems-engineering-invariants.md
├── docs/                                # Technical Architecture & Developer Guides
│   ├── index.md                         # Documentation Hub Index
│   ├── architecture/                    # Systems Architecture Specs
│   │   ├── index.md                     # Architecture Specs Index
│   │   ├── arch-build-agent-engine.md
│   │   ├── arch-agent-opportunity-scan.md
│   │   ├── arch-runtime-harness-and-armor.md
│   │   └── arch-sequential-pipeline-integration.md
│   └── guides/                          # Developer & Operational Walkthroughs
│       ├── index.md                     # Operational Guides Index
│       ├── guide-authoring-and-scaffolding-agents.md
│       ├── guide-dual-skill-operational-workflow.md
│       └── guide-dual-tier-viability-rubric.md
├── skills/                              # Google Antigravity Skills Library
│   ├── index.md                         # Skills Catalog Root Index
│   ├── 01-prompt-engineering/           # 10 Scientific Prompt Skills
│   │   ├── index.md                     # Prompt Engineering Category Index
│   │   └── [10 skills folders...]
│   └── 02-agent-builder/                # 3 Autonomous Agent Skills
│       ├── index.md                     # Agent Engineering Category Index
│       └── [3 skills folders...]
└── scripts/                             # Automation, Installation & Validation
    ├── index.md                         # Scripts Directory Index
    ├── install-global.ps1
    ├── validate-skills.ps1
    └── validate-okf.py
```

---

## 🗂️ Major Knowledge Bundles

1. [Academic Research References](research%20references/index.md) — Foundational NLP survey (*The Prompt Report*) and the top 5 agent specifications (Xi et al., CoALA, Anthropic, Oracle, and Systems Invariants).
2. [Systems Architecture Documentation](docs/architecture/index.md) — Concrete specifications for the agent compiler, opportunity scanner, and runtime armor layers.
3. [Developer & Operational Guides](docs/guides/index.md) — Step-by-step guides for authoring, testing, and chaining agent skills.
4. [Skills Catalog](skills/index.md) — Master index of all 13 Antigravity skills.
   - [01-prompt-engineering/](skills/01-prompt-engineering/index.md) (10 Prompt Skills)
   - [02-agent-builder/](skills/02-agent-builder/index.md) (3 Agent Skills)
5. [Automation & Validation Scripts](scripts/index.md) — Global installer and automated validation suites.

---

## 🛠️ Graph Validation

To deterministically verify all OKF YAML schemas and relative graph links across the entire repository:

```powershell
python scripts/validate-okf.py
```
