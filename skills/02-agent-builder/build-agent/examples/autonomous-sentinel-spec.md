# Agent Specification Sheet: uptime-sentinel-daemon

> **Specification Status:** Approved  
> **Target Runtime:** Standalone Python Micro-Harness (Daemon Mode)  
> **Archetype:** Autonomous Sentinel / Daemon  
> **Spec Version:** 1.0.0  
> **Last Updated:** 2026-10-07

---

## 1. Mission, Mandate & Scope Envelope

### Core Objective & Mandate
Continuously monitor staging environment web endpoints and user login journeys on a scheduled interval, capturing DOM snapshots and network telemetry upon failure, and auto-filing actionable issue reports.

### Triage Classification (Anthropic §2)
- **Execution Paradigm:** Autonomous Sentinel Loop
- **Triage Justification:** Scheduled long-running monitoring requiring browser interaction, network flakiness retry heuristics, and diagnostic state journaling cannot be modeled as a single stateless prompt chain.

### In-Scope Boundaries
- [ ] Execute scheduled health checks against declared HTTP endpoints
- [ ] Drive browser login journeys using `agent-browser` or `chrome-devtools-mcp`
- [ ] Capture full DOM snapshots and failure screenshots upon HTTP 5xx or UI errors
- [ ] Maintain an append-only transaction journal in `.agents/state/sentinel_events.jsonl`

### Hard Refusals & "The Fired Conditions" (Mohammadi et al. 2025)
- 🚫 **Hard Refusal 1:** Never execute load testing, volumetric denial-of-service, or rapid multi-threaded ping floods.
- 🚫 **Hard Refusal 2:** Never log live user passwords or session cookie values in plaintext reports.
- 🚫 **Hard Refusal 3:** Never attempt automated remediation or server restarts without explicit human escalation.

---

## 2. Team Topology & Role Slicing

### Architecture Pattern
- **Topology Model:** Solitary Autonomous Daemon with Event State Journal
- **Max Worker Concurrency:** 1
- **Debate / Critique Turn Ceiling:** N/A

### Team Roster & Model Tier Allocation
| Agent Role | Model Tier | Workspace Mode | Primary Responsibility & Blast Radius |
| :--- | :--- | :--- | :--- |
| **UptimeSentinel** | `flash` (High Speed) | `inherit` | Scheduled endpoint pinging, browser journey execution, incident logging |

---

## 3. Cognitive Architecture & Domain Grounding (CoALA & Pocock)

### Domain Context Grounding Bridge
- **Ubiquitous Domain Model:** Bound to [`CONTEXT.md`](CONTEXT.md)
- **Domain Invariants:** Adheres to internal service health endpoint contracts (`/healthz`, `/readyz`) and expected response SLAs ($< 800\text{ms}$).

### Action Space Decoupling (CoALA §3)
- **Internal Actions (Cognitive Seam):** Latency percentile calculation, failure signature clustering.
- **External Actions (Mutation Seam):** HTTP requests, browser navigation via MCP, incident file writes.

### State Persistence & Crash Recovery
- **Transaction Journal:** Appends every check event to `.agents/state/sentinel_events.jsonl` with SHA-256 idempotency hashes.
- **Poison-Pill Quarantine:** Endpoints failing 3 consecutive health checks are quarantined to `.agents/dead_letter/endpoint_<id>.json` to prevent loop blocking.
- **Signal Trap:** Traps `SIGTERM` / `SIGINT` to safely flush state within a 2,000ms grace window.

---

## 4. Tool Manifest & Blast Radius Containment

### Active Tool Set (Max 8 Active Schemas)
| Tool Name | Tool Source | Action Type | Blast Radius / Permission Boundary |
| :--- | :--- | :--- | :--- |
| `run_command` | Native | External | Read-only curl / network probing (`curl -I -s`) |
| `agent-browser` | Plugin / MCP | External | Browser navigation, DOM snapshot, screenshot capture |
| `ask_human` | Built-in Primitive | Internal | Alert human when critical service outage detected |

### Blast Radius Containment Matrix
- **Allowed Write Directories:** `.agents/state/`, `.agents/artifacts/`
- **DOM Snapshot Armor:** Truncated at 50,000 characters to prevent context overflow.
- **Screenshots:** Written strictly to `.agents/artifacts/screenshots/`.

---

## 5. Execution Harness, Fault Tolerance & Economics

### Control Flow & Limits
- **Loop Strategy:** Event-Driven Sentinel Loop with Exponential Jitter Backoff.
- **Poll Interval:** Every 300 seconds (5 minutes).
- **Per-Check Timeout:** 15,000ms.

### Fault Tolerance & Reflexion
- **Network Resilience:** Full-jitter exponential backoff on transient network drops ($T = \text{random}(0, \min(30000, 1000 \times 2^{\text{attempt}}))$).
- **Dead-Letter Handling:** Quarantined endpoints trigger an immediate human escalation notification.

### Economic Circuit Breaker
- **Token Budget Ceiling:** 100,000 tokens per 24-hour monitoring window.
- **Financial Cost Ceiling:** Estimated $0.50/day API budget cap.

---

## 6. Deliverable Contract & Verification Harness

### Payload Shape (Dual-Format Output Contract)
1. **Human Chat Summary:** Live terminal status bar with colored endpoint health status and SLA percentiles.
2. **Machine Deliverable Payload:** Enclosed in ```json <deliverable_data> ``` containing structured endpoint latency metrics and error logs.

### Definition of Done (DoD)
- [ ] 100% of declared endpoints polled according to schedule.
- [ ] Incident screenshots and DOM snapshots captured on any HTTP 5xx error.
- [ ] Clean shutdown verified under `SIGINT` with 0 state corruption.

### Verification Probes
- **Pre-Flight Health Check:** `python .agents/agents/uptime-sentinel-daemon/runner.py --health`
- **Zero-Token Mock Replay:** `python .agents/agents/uptime-sentinel-daemon/runner.py --mock`
