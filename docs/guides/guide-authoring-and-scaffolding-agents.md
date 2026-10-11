---
type: guide
title: "Developer Guide: Authoring, Testing, and Scaffolding Agents"
description: "Practical guide on template usage, directory seams, testing with offline --health and --mock flags, and managing the .agents/ master registry."
tags: [developer-guide, testing, micro-harness, runner, verification]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "skills/02-agent-builder/build-agent/resources/micro-harness-template.py"
---

# Developer Guide: Authoring, Testing, and Scaffolding Agents

## 💡 Strategic Context & Rationale
*Master Index:* [index.md](../index.md)  
*Runtime Architecture:* [Runtime Harness & Armor](../architecture/arch-runtime-harness-and-armor.md)

This guide documents the directory seams, template assets, and testing procedures for agents built using `/build-agent`.

---

## 1. Runtime Directory Seams

Every workspace using the agent suite follows this runtime directory structure:

```text
c:\your-project\
├── .agents/
│   ├── agents.json                   # Master agent registry
│   ├── specs/                        # Narrative & Oracle declarative YAML specs
│   │   ├── <agent-name>.spec.md
│   │   └── <agent-name>.spec.yaml
│   ├── agents/                       # Live agent runtimes
│   │   └── <AgentName>/
│   │       ├── agent.md              # Native Antigravity subagent definition
│   │       ├── runner.py             # Standalone Python micro-harness
│   │       └── tools/                # Scoped custom tool scripts
│   ├── state/                        # Append-only execution logs & journals
│   └── reports/                      # Multi-agent structured artifact handoffs
```

---

## 2. Template Assets in `build-agent`

Located in [`skills/02-agent-builder/build-agent/resources/`](../../skills/02-agent-builder/build-agent/resources/):
- **`spec-sheet-template.md`:** 6-dimension specification contract with Fired Conditions and DoD.
- **`oracle-spec-template.yaml`:** Oracle `agent-spec` compliant declarative schema.
- **`micro-harness-template.py`:** Zero-dependency Python runner with REST adapter, git rollback, 16KB payload armor, and `--health` / `--mock` testing.
- **`tool-stub-template.py`:** Standardized Python tool script template.
- **`policy-interceptor-template.py`:** Pre-execution command blocklist and secret scrubber.
- **`interview-rubric.md`:** 4-station risk-weighted walkthrough interview rubric.

---

## 3. Testing & Verification Procedures

Before activating any agent in production, run its built-in CLI verification commands:

### Offline Health Check
Verifies environment variables, directory permissions, and tool schemas without consuming any LLM tokens:
```powershell
python .agents/agents/<AgentName>/runner.py --health
```
*Expected Output:* `[OK] All health checks passed. Agent is operational.`

### Offline Mock Simulation
Executes a synthetic end-to-end task using pre-canned deterministic tool outputs:
```powershell
python .agents/agents/<AgentName>/runner.py --mock
```
*Expected Output:* `[OK] Mock simulation completed successfully. 0 errors detected.`

### Live Invocation
Execute a real task with the agent:
```powershell
python .agents/agents/<AgentName>/runner.py "audit migrations in src/db/"
```

---

## 🔗 Related Knowledge Base Links
* 🏠 [Master Index](../index.md)
* 🛡️ [Runtime Harness Specification](../architecture/arch-runtime-harness-and-armor.md)
* 🧭 [Operational Workflow Guide](guide-dual-skill-operational-workflow.md)
