---
type: index
title: "Systems Architecture Specifications: OKF Index"
description: "Master OKF v0.2 architectural index mapping deep system designs, discovery pipelines, runtime harnesses, and armor layers."
version: "1.0.0"
okf_version: "0.2"
status: active
timestamp: 2026-10-11T12:00:00Z
verified: true
verified_by: "@BenjaminBeitz"
---

# Systems Architecture Specifications: OKF Index

Welcome to the **Systems Architecture** knowledge bundle for the **Bitz Prompt & Agent Builder Skills Suite**.

This directory documents the technical architectures, pipeline state machines, runtime harnesses, and validation layers that power the suite's agent discovery and scaffolding capabilities.

---

## 🧭 Architecture Specifications Map

```text
docs/architecture/
├── index.md                                   # This Architectural Index
├── arch-build-agent-engine.md                 # Spec-driven /build-agent systems architecture
├── arch-agent-opportunity-scan.md             # /agent-opportunity-scan discovery & AVS scoring engine
├── arch-runtime-harness-and-armor.md          # Zero-dependency Python micro-harness & console armor
└── arch-sequential-pipeline-integration.md    # Two-stage autonomous pipeline (Stage 0 -> Stage 1)
```

---

## 🏛️ 1. Technical Specifications

- [arch-build-agent-engine.md](arch-build-agent-engine.md)  
  *Spec-Driven Agent Engineering Engine* — Complete system blueprint detailing the 5-phase execution pipeline (Ingestion, Interview, Synthesis, Scaffolding, Verification), artifact schemas, and safety boundaries.

- [arch-agent-opportunity-scan.md](arch-agent-opportunity-scan.md)  
  *Discovery, Archetype Classification & AVS Scoring* — Mathematical formalization of the Agent Viability Score (AVS), heuristic pattern detection across session logs, and classification into 3 core archetypes (*solo-tool-user*, *multi-agent-squad*, *autonomous-sentinel*).

- [arch-runtime-harness-and-armor.md](arch-runtime-harness-and-armor.md)  
  *Runtime Micro-Harness & Console Armor* — Design specification for the zero-dependency Python verification harness (`micro-harness-template.py`), payload size truncators, policy interceptors, and Windows cp1252 character armor.

- [arch-sequential-pipeline-integration.md](arch-sequential-pipeline-integration.md)  
  *Two-Stage Autonomous Pipeline Integration* — End-to-end integration architecture demonstrating how `agent-opportunity-scan` feeds structured candidates directly into `build-agent` without human re-entry.

---

## 🔗 Cross-Bundle Navigation

- 🏠 **Documentation Root:** [../index.md](../index.md)
- 📚 **Academic Foundations:** [../../research references/index.md](../../research%20references/index.md)
- 🛠️ **Engineering Skills Library:** [../../skills/index.md](../../skills/index.md)
- ⚙️ **Automation Scripts:** [../../scripts/index.md](../../scripts/index.md)
