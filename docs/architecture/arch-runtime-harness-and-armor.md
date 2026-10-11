---
type: arch
title: "Runtime Micro-Harness and Execution Armor Specification"
description: "Specification of the zero-dependency Python standalone runner (runner.py), git rollback guards, 16KB payload armor, and cross-platform console defenses."
tags: [micro-harness, runner, execution-armor, rollback, cross-platform]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "skills/02-architecture-specs/build-agent/resources/micro-harness-template.py"
  - "skills/02-architecture-specs/build-agent/resources/policy-interceptor-template.py"
---

# Runtime Micro-Harness and Execution Armor Specification

## 💡 Strategic Context & Rationale
*Master Index:* [index.md](../index.md)  
*Foundational Invariants:* [Systems Engineering Invariants](../../research%20references/05-systems-engineering-invariants.md)  
*Construction Engine:* [Build Agent Engine Architecture](arch-build-agent-engine.md)

Every agent created by `/build-agent` includes a standalone, zero-dependency Python harness (`runner.py`) located in `.agents/agents/<AgentName>/runner.py`. This ensures generated agents can run in headless CI environments, docker containers, and local terminals without requiring LangChain, CrewAI, or heavy framework dependencies.

---

## 1. Zero-Dependency Philosophy

The micro-harness relies strictly on Python's Standard Library:
- `urllib.request` & `json` (REST client and LLM API adapter).
- `subprocess` (scoped, non-interactive shell execution).
- `os`, `sys`, `pathlib`, `shutil` (file manipulation and cross-platform path handling).
- `argparse` (CLI argument parsing and testing flags).

---

## 2. Execution Armor Layers

```text
┌────────────────────────────────────────────────────────┐
│                   INCOMING TASK PROMPT                 │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 1. Git Working Tree Checkpoint (git stash create)      │
│    Takes internal snapshot before mutating any file.   │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 2. Pre-Execution Policy Interceptor                    │
│    • Blocks destructive commands (rm -rf, git reset)   │
│    • Sanitizes secrets & auth tokens from logs         │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 3. Non-Interactive Shell Runner                        │
│    • Enforces CI=true and stdin=DEVNULL                │
│    • Prevents blocking on interactive sudo/pagers      │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 4. Tool Output Payload Armor (16KB ceiling)            │
│    • Truncates outputs > 16KB to prevent context bloat │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 5. Working Memory Compaction (70% context trigger)     │
│    • Summarizes early steps; re-pins goal anchor       │
└────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│ 6. 3-Strike Reflexion & Automated Rollback             │
│    • If 3 consecutive failures occur, roll back to git │
│      checkpoint to guarantee zero dirty state on disk. │
└────────────────────────────────────────────────────────┘
```

---

## 3. Standard CLI Verification Flags

Every `runner.py` implements 3 mandatory test modes:
1. **`--health`**: Executes a zero-token offline health check, verifying tool scripts, environment variables, and directory permissions.
2. **`--mock`**: Runs an offline smoke-test using deterministic mock tool outputs without making external LLM API calls.
3. **`--test-suite`**: Runs the complete unit and integration test suite defined in the agent's spec.

---

## 🔗 Related Knowledge Base Links
* 🏠 [Master Index](../index.md)
* 📚 [Systems Engineering Invariants](../../research%20references/05-systems-engineering-invariants.md)
* 🏗️ [Build Agent Engine Architecture](arch-build-agent-engine.md)
* 🛠️ [Authoring & Scaffolding Guide](../guides/guide-authoring-and-scaffolding-agents.md)
