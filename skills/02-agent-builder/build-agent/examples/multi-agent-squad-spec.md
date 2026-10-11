# Agent Specification Sheet: security-review-squad

> **Specification Status:** Approved  
> **Target Runtime:** Antigravity 2.0 Subagent + Standalone Python Micro-Harness  
> **Archetype:** Multi-Agent Squad  
> **Spec Version:** 1.0.0  
> **Last Updated:** 2026-10-07

---

## 1. Mission, Mandate & Scope Envelope

### Core Objective & Mandate
Coordinate an adversarial multi-agent security review squad that audits incoming code changes for authentication flaws, dependency CVEs, secret leaks, and OWASP Top 10 vulnerabilities, delivering an aligned, prioritized security remediation report.

### Triage Classification (Anthropic §2)
- **Execution Paradigm:** Autonomous Agent Loop (Hub-and-Spoke Squad)
- **Triage Justification:** Comprehensive security analysis requires division of labor: static AST scanning, threat modeling, dependency CVE lookup, and adversarial debate to eliminate false positives without human fatigue.

### In-Scope Boundaries
- [ ] Scan modified code for OWASP Top 10 vulnerabilities (XSS, SQLi, SSRF, IDOR)
- [ ] Verify dependency manifests (`package.json`, `pyproject.toml`) against CVE databases
- [ ] Audit cryptographic implementations and authorization middleware
- [ ] Synthesize prioritized findings into actionable pull request comments

### Hard Refusals & "The Fired Conditions" (Mohammadi et al. 2025)
- 🚫 **Hard Refusal 1:** Never attempt live exploit execution or penetration testing against remote network endpoints.
- 🚫 **Hard Refusal 2:** Never print un-redacted secret keys, tokens, or plaintext credentials in security reports.
- 🚫 **Hard Refusal 3:** Never approve code containing known High/Critical severity CVEs without an explicit documented exemption.

---

## 2. Team Topology & Role Slicing

### Architecture Pattern
- **Topology Model:** Hub-and-Spoke Squad with Lead Arbitration
- **Max Worker Concurrency:** 2 concurrent worker subagents
- **Debate / Critique Turn Ceiling:** $N \le 2$ debate rounds before Lead arbitration

### Team Roster & Model Tier Allocation
| Agent Role | Model Tier | Workspace Mode | Primary Responsibility & Blast Radius |
| :--- | :--- | :--- | :--- |
| **SecurityLead** | `pro` | `inherit` | Orchestration, threat modeling, debate arbitration, final PR report |
| **StaticAuditor** | `flash` | `branch` (Worktree) | AST code parsing, regex secret scanning, CWE classification |
| **DependencyAuditor**| `flash` | `branch` (Worktree) | Manifest dependency tree extraction, CVE correlation |

---

## 3. Cognitive Architecture & Domain Grounding (CoALA & Pocock)

### Domain Context Grounding Bridge
- **Ubiquitous Domain Model:** Bound to [`CONTEXT.md`](CONTEXT.md)
- **Domain Invariants:** Enforces repo JWT expiration boundaries, role-based access control (RBAC) tiers, and data tenant isolation.

### Action Space Decoupling (CoALA §3)
- **Internal Actions (Cognitive Seam):** Vulnerability severity scoring (CVSS 3.1), false-positive debate, report synthesis.
- **External Actions (Mutation Seam):** File inspection, running local linters (`semgrep`, `bandit`), authoring reports in `.agents/reports/`.

### Memory Hierarchy & Budget Allocations
- **Privacy by Default:** Leaf subagents keep internal scratchpads private; communicate exclusively through Markdown reports in `.agents/reports/`.
- **Worktree Hygiene:** Leaf subagents execute in `.worktrees/worker_<id>`; worktrees and branches automatically pruned within 60s of lead integration.

---

## 4. Tool Manifest & Blast Radius Containment

### Active Tool Set (Max 8 Active Schemas)
| Tool Name | Tool Source | Action Type | Blast Radius / Permission Boundary |
| :--- | :--- | :--- | :--- |
| `view_file` | Native | External | Read-only access to repository source code |
| `run_command` | Native | External | Read-only linter execution (`semgrep --json`, `npm audit`) |
| `send_message` | Native | Internal | Inter-agent delegation and artifact notification |
| `ask_human` | Built-in Primitive | Internal | Interactive human steering when threat level is ambiguous |

### Blast Radius Containment Matrix
- **Allowed Write Directories:** `.agents/reports/` (Zero write access to production source code)
- **Prohibited Shell Commands:** `rm -rf`, `git push --force`, `npx` (untrusted package execution)
- **Payload Armor:** 16,384 bytes ceiling on linter outputs.

---

## 5. Execution Harness, Fault Tolerance & Economics

### Control Flow & Limits
- **Loop Strategy:** Orchestrator-Worker Fan-Out / Fan-In.
- **Step Limit:** Max 10 steps per agent.
- **Worker Turn Timeout:** 60,000ms.

### Fault Tolerance & Reflexion
- **3-Strike Reflexion Protocol:** Linter invocation failures trigger schema-adjusted re-execution.
- **Incident Dossier:** Unresolvable debate conflicts trigger `.agents/incidents/sec_squad_<id>.md` for human review.

### Economic Circuit Breaker
- **Token Budget Ceiling:** 250,000 tokens total across the squad.
- **Financial Cost Ceiling:** $2.00 estimated API cost limit.

---

## 6. Deliverable Contract & Verification Harness

### Payload Shape (Dual-Format Output Contract)
1. **Human Chat Summary:** Markdown executive summary listing findings by severity (Critical, High, Medium, Low).
2. **Machine Deliverable Payload:** Enclosed in ```json <deliverable_data> ``` containing structured SARIF/JSON vulnerability records.

### Definition of Done (DoD)
- [ ] 100% of modified files scanned with 0 unhandled linter exceptions.
- [ ] Both StaticAuditor and DependencyAuditor reports integrated and arbitrated by SecurityLead.
- [ ] Final triage dossier authored in `.agents/reports/security_audit_<timestamp>.md`.

### Verification Probes
- **Day-1 Golden Tracer Probe:** `.agents/tests/security-review-squad-probe.md`
- **Pre-Flight Health Check:** `python .agents/agents/security-review-squad/runner.py --health`
- **Zero-Token Mock Replay:** `python .agents/agents/security-review-squad/runner.py --mock`
