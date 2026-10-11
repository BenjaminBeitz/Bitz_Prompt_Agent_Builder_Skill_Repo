# Agent Specification Sheet: {{AGENT_NAME}}

> **Specification Status:** Draft / Under Review / Approved  
> **Target Runtime:** Antigravity 2.0 Subagent + Standalone Python Micro-Harness  
> **Archetype:** {{ARCHETYPE}} <!-- [Solo Tool-User | Multi-Agent Squad | Autonomous Sentinel] -->  
> **Spec Version:** 1.0.0  
> **Last Updated:** {{DATE}}

---

## 1. Mission, Mandate & Scope Envelope

### Core Objective & Mandate
{{CORE_OBJECTIVE_DESCRIPTION}}

### Triage Classification (Anthropic §2)
- **Execution Paradigm:** {{EXECUTION_PARADIGM}} <!-- [Deterministic Workflow DAG | Autonomous Agent Loop] -->
- **Triage Justification:** {{TRIAGE_JUSTIFICATION}} <!-- Why this task requires an autonomous loop or is better as a deterministic workflow -->

### In-Scope Boundaries
- [ ] {{IN_SCOPE_ITEM_1}}
- [ ] {{IN_SCOPE_ITEM_2}}
- [ ] {{IN_SCOPE_ITEM_3}}

### Hard Refusals & "The Fired Conditions" (Mohammadi et al. 2025)
*These represent explicit zero-tolerance failure modes and red lines. Violating any of these triggers immediate task abort and human escalation.*
- 🚫 **Hard Refusal 1:** {{HARD_REFUSAL_1}} <!-- e.g. "Never execute destructive commands like rm -rf, drop table, or git push --force" -->
- 🚫 **Hard Refusal 2:** {{HARD_REFUSAL_2}} <!-- e.g. "Never leak credentials, tokens, or PII into output logs or git diffs" -->
- 🚫 **Hard Refusal 3:** {{HARD_REFUSAL_3}} <!-- e.g. "Never mutate files outside designated workspace boundaries without human confirmation" -->

### Assumed Defaults (Flagged in Intake for Approval)
- ⚠️ **Assumption 1:** {{ASSUMPTION_1}}
- ⚠️ **Assumption 2:** {{ASSUMPTION_2}}

---

## 2. Team Topology & Role Slicing

### Architecture Pattern
- **Topology Model:** {{TOPOLOGY_MODEL}} <!-- [Solitary Operator | Pipeline Relay | Hub-and-Spoke Squad | Deliberative Council] -->
- **Max Worker Concurrency:** {{MAX_CONCURRENCY}} <!-- Default: 3 parallel workers -->
- **Debate / Critique Turn Ceiling:** {{MAX_DEBATE_ROUNDS}} <!-- Default: N <= 3 rounds before forced Lead arbitration -->

### Team Roster & Model Tier Allocation
| Agent Role | Model Tier | Workspace Mode | Primary Responsibility & Blast Radius |
| :--- | :--- | :--- | :--- |
| **{{LEAD_ROLE_NAME}}** | `pro` (High Reasoning) | `inherit` | Orchestration, decomposition, final evaluation, git integration |
| **{{WORKER_ROLE_NAME}}** | `flash` (High Speed) | `branch` (Worktree) | Scoped execution, tool execution, report authoring |

---

## 3. Cognitive Architecture & Domain Grounding (CoALA & Pocock)

### Domain Context Grounding Bridge
- **Ubiquitous Domain Model:** Bound to [`CONTEXT.md`](CONTEXT.md)
- **Domain Invariants & Glossary:** {{DOMAIN_INVARIANTS_SUMMARY}}

### Action Space Decoupling (CoALA §3)
- **Internal Actions (Cognitive Seam):** Scratchpad drafting, plan re-evaluation, belief updating, memory recall (Zero external side-effects).
- **External Actions (Mutation Seam):** Tool execution, file writes, bash commands, external API requests (Governed by safety interceptor).

### Memory Hierarchy & Budget Allocations
- **Working Memory Buffer:** Capped at 30% of context window.
- **Context Compaction Trigger:** Triggers at **70% utilization** via sliding-window checkpoint summarization.
- **Recency Goal Pinning:** Injects `<<<ACTIVE_MISSION_ANCHOR>>>` at every turn to prevent long-horizon planning amnesia.
- **Cross-Session Episodic Recall:** Queries `.agents/reports/*.md` for past successful trajectories on matching task keywords.

---

## 4. Tool Manifest & Blast Radius Containment

### Active Tool Set (Max 8 Active Schemas)
| Tool Name | Tool Source | Action Type | Blast Radius / Permission Boundary |
| :--- | :--- | :--- | :--- |
| `{{TOOL_1_NAME}}` | Native / MCP / Custom | Internal / External | Read-only / Workspace-write / Mutate |
| `{{TOOL_2_NAME}}` | Native / MCP / Custom | Internal / External | Read-only / Workspace-write / Mutate |
| `ask_human` | Built-in Primitive | Internal | Interactive clarification tool when ambiguity arises |

### Blast Radius Containment Matrix
- **Allowed Write Directories:** `{{ALLOWED_WRITE_PATHS}}`
- **Prohibited Shell Commands:** `rm -rf`, `git push --force`, `drop database`, `format`, `dd`
- **Subprocess Environment Invariant:** `CI=true`, `PAGER=cat`, `DEBIAN_FRONTEND=noninteractive`, `stdin=DEVNULL`
- **Payload Armor:** Tool returns hard-capped at **16,384 bytes (~4k tokens)** with offset indicators.

---

## 5. Execution Harness, Fault Tolerance & Economics

### Control Flow & Limits
- **Loop Strategy:** ToRA Interleaved Loop (Plan $\to$ Reason $\to$ Action $\to$ Observe $\to$ Reflexion).
- **Step Limit:** Max {{MAX_STEPS}} iterations (Default: 10 steps) before mandatory human escalation.
- **Per-Turn Worker Timeout:** {{WORKER_TIMEOUT_MS}} ms (Default: 60,000ms).

### Fault Tolerance & Reflexion
- **3-Strike Reflexion Protocol:**
  - *Strike 1:* Inject stderr/schema feedback into scratchpad.
  - *Strike 2:* Force strategy shift or tool alternative.
  - *Strike 3:* Halt, generate Incident Dossier, and escalate to human.
- **Working Tree Rollback:** Takes internal git checkpoint on entry (`git stash create`); automatically rolls back on 3-strike failure.
- **Human Confirmation Resumption:** Serializes ToRA state to `.pending_action.json` (24h TTL) when awaiting human approval.

### Economic Circuit Breaker
- **Token Budget Ceiling:** 250,000 tokens per single execution run.
- **Financial Cost Ceiling:** Estimated $2.00 API cost limit; hard yields to `.budget_exceeded.json` at 100%.

---

## 6. Deliverable Contract & Verification Harness

### Payload Shape (Dual-Format Output Contract)
1. **Human Chat Summary:** Markdown summary ($< 300$ words) highlighting actions taken and validation status.
2. **Machine Deliverable Payload:** Enclosed in an isolated ```json <deliverable_data> ``` block containing structured outputs.

### Definition of Done (DoD)
- [ ] {{DOD_CRITERIA_1}}
- [ ] {{DOD_CRITERIA_2}}
- [ ] Automated validation commands pass with 0 errors: `{{VALIDATION_COMMAND}}`

### Evaluator-Optimizer Self-Critic Gate
- Before yielding to human, the agent runs an internal validation pass against the Definition of Done and Fired Conditions. If checks fail, triggers 1 internal reflex correction turn.

### Verification Probes
- **Day-1 Golden Tracer Probe:** Defined in `.agents/tests/{{AGENT_NAME}}-probe.md`
- **Pre-Flight Health Check:** `python .agents/agents/{{AGENT_NAME}}/runner.py --health`
- **Zero-Token Mock Replay:** `python .agents/agents/{{AGENT_NAME}}/runner.py --mock`
- **Cumulative Test Suite:** `python .agents/agents/{{AGENT_NAME}}/runner.py --test-suite`
