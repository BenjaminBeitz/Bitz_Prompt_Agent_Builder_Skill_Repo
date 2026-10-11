# Agent Specification Sheet: db-migration-auditor

> **Specification Status:** Approved  
> **Target Runtime:** Antigravity 2.0 Subagent + Standalone Python Micro-Harness  
> **Archetype:** Solo Tool-User  
> **Spec Version:** 1.0.0  
> **Last Updated:** 2026-10-07

---

## 1. Mission, Mandate & Scope Envelope

### Core Objective & Mandate
Autonomously analyze and validate SQL database schema migrations in pull requests, verifying down-migration rollback parity, indexing strategies, and zero downtime locking risks before production merges.

### Triage Classification (Anthropic §2)
- **Execution Paradigm:** Autonomous Agent Loop
- **Triage Justification:** Analyzing multi-table SQL schema changes across various dialects and verifying destructive locking risks requires dynamic file inspection, schema dependency graph parsing, and contrastive error recovery.

### In-Scope Boundaries
- [ ] Inspect SQL migration files in `migrations/` and `schema/`
- [ ] Detect missing down-migration rollbacks or asymmetric rollback scripts
- [ ] Identify lock-heavy DDL operations (e.g. `ALTER TABLE ADD COLUMN NOT NULL` without default)
- [ ] Suggest safe concurrent indexing patterns (`CREATE INDEX CONCURRENTLY`)

### Hard Refusals & "The Fired Conditions" (Mohammadi et al. 2025)
- 🚫 **Hard Refusal 1:** Never execute live SQL statements against production or staging databases; operate strictly on static SQL files and local SQLite/Postgres test containers.
- 🚫 **Hard Refusal 2:** Never approve a migration that drops columns or tables without an explicit two-phase deprecation warning.
- 🚫 **Hard Refusal 3:** Never commit changes to git branches without passing local syntax checks.

### Assumed Defaults (Flagged in Intake)
- ⚠️ **Assumption 1:** Database dialect defaults to PostgreSQL 15+.
- ⚠️ **Assumption 2:** Local migrations directory is located at `./migrations`.

---

## 2. Team Topology & Role Slicing

### Architecture Pattern
- **Topology Model:** Solitary Operator (Single high-focus tool-user agent)
- **Max Worker Concurrency:** 1 (Single agent)
- **Debate / Critique Turn Ceiling:** N/A (Solo agent)

### Team Roster & Model Tier Allocation
| Agent Role | Model Tier | Workspace Mode | Primary Responsibility & Blast Radius |
| :--- | :--- | :--- | :--- |
| **MigrationAuditor** | `pro` (High Reasoning) | `inherit` | Static SQL parsing, lock risk assessment, review reporting |

---

## 3. Cognitive Architecture & Domain Grounding (CoALA & Pocock)

### Domain Context Grounding Bridge
- **Ubiquitous Domain Model:** Bound to [`CONTEXT.md`](CONTEXT.md)
- **Domain Invariants & Glossary:** Adheres to project table naming conventions (`snake_case`), multi-tenant account scoping (`account_id` foreign keys), and UTC timestamp constraints.

### Action Space Decoupling (CoALA §3)
- **Internal Actions (Cognitive Seam):** Scratchpad AST parsing, DDL locking matrix evaluation, review note synthesis.
- **External Actions (Mutation Seam):** Reading migration files via `view_file`, authoring review artifacts in `.agents/reports/`.

### Memory Hierarchy & Budget Allocations
- **Working Memory Buffer:** 30% active buffer.
- **Context Compaction Trigger:** 70% threshold.
- **Recency Goal Pinning:** Injects `<<<ACTIVE_MISSION_ANCHOR>>>` holding migration review checklist.
- **Cross-Session Episodic Recall:** Searches `.agents/reports/*migration*.md` for historical review patterns.

---

## 4. Tool Manifest & Blast Radius Containment

### Active Tool Set (Max 8 Active Schemas)
| Tool Name | Tool Source | Action Type | Blast Radius / Permission Boundary |
| :--- | :--- | :--- | :--- |
| `view_file` | Native | External | Read-only access to `migrations/` and `schema/` |
| `run_command` | Native | External | Read-only execution (`git diff`, `sqlfluff lint`) |
| `ask_human` | Built-in Primitive | Internal | Prompts engineer when migration intention is ambiguous |

### Blast Radius Containment Matrix
- **Allowed Write Directories:** `.agents/reports/` (Read-only on repository source code)
- **Prohibited Shell Commands:** `rm -rf`, `git push --force`, `drop database`, `psql -h prod`
- **Subprocess Environment Invariant:** `CI=true`, `PAGER=cat`, `DEBIAN_FRONTEND=noninteractive`, `stdin=DEVNULL`
- **Payload Armor:** 16,384 bytes ceiling on SQL file reads.

---

## 5. Execution Harness, Fault Tolerance & Economics

### Control Flow & Limits
- **Loop Strategy:** ToRA Interleaved Loop (max 8 steps).
- **Per-Turn Worker Timeout:** 30,000ms.

### Fault Tolerance & Reflexion
- **3-Strike Reflexion Protocol:** Strikes on parser errors trigger syntax correction and dialect retry.
- **Working Tree Rollback:** Ephemeral git checkpoint created at entry; guaranteed clean tree on exit.
- **Human Confirmation Resumption:** Awaits user input via `.pending_action.json` if ambiguous DDL detected.

### Economic Circuit Breaker
- **Token Budget Ceiling:** 150,000 tokens per review.
- **Financial Cost Ceiling:** $1.00 estimated API cost cap.

---

## 6. Deliverable Contract & Verification Harness

### Payload Shape (Dual-Format Output Contract)
1. **Human Chat Summary:** Markdown audit summary categorizing DDL operations into Green (Safe), Yellow (Caution/Locks), Red (Breaking).
2. **Machine Deliverable Payload:** Enclosed in ```json <deliverable_data> ``` containing structured lint results and risk scores.

### Definition of Done (DoD)
- [ ] 100% of SQL migration files in the active PR diff are parsed.
- [ ] Rollback parity verified for all `UP` migrations against corresponding `DOWN` files.
- [ ] Comprehensive audit report generated in `.agents/reports/migration_audit_<timestamp>.md`.

### Evaluator-Optimizer Self-Critic Gate
- Prior to finalizing report, asserts that zero DDL lock risks were omitted from the summary table.

### Verification Probes
- **Day-1 Golden Tracer Probe:** `.agents/tests/db-migration-auditor-probe.md`
- **Pre-Flight Health Check:** `python .agents/agents/db-migration-auditor/runner.py --health`
- **Zero-Token Mock Replay:** `python .agents/agents/db-migration-auditor/runner.py --mock`
