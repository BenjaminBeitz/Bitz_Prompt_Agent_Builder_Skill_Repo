# Agent Opportunity Viability & Archetype Selection Rubric (v2.0)
*Grounded in Xi et al. (2025), CoALA (Sumers et al., 2024), Anthropic's "Building Effective Agents" (2024), Oracle agent-spec, and Andrew Ng / Harrison Chase Frameworks*

---

## 1. The Dual-Tier Qualification Taxonomy

To guarantee that autonomous agents are engineered only when justified—and to prevent over-engineering simple scripts or prompt templates into complex agent harnesses—candidates must undergo a two-tier evaluation:

```
[Candidate Workflow / Friction Pattern]
                    ↓
   Tier 1: 5 Critical Qualification Gates
         (ALL 5 MUST PASS: Binary 1/0)
                    ↓
  [Passes All 5 Gates: Qualified Candidate]
                    ↓
   Tier 2: 5 Optional Value-Add Enhancers
         (0 to 5 Boosters: +15% each)
                    ↓
   Agent Viability Score (AVS) & Archetype Mapping
                    ↓
    Direct Handoff to /build-agent Stage 1
```

---

## 2. Tier 1: The 5 Critical Qualification Gates (Non-Negotiable)

A candidate workflow **MUST satisfy ALL 5 gates** to qualify for autonomous agentification via `/build-agent`. If any single gate fails, the candidate is routed to a simpler, lower-overhead primitive.

| Critical Gate | Theoretical Anchor | Qualification Requirement | Routing if Failed |
|---|---|---|---|
| **CG-1: Dynamic State & Branching** | Anthropic §2 (Workflows vs Agents) | The task requires non-deterministic exploration, branching logic, or dynamic runtime decision trees. It cannot be resolved via a static linear script or single prompt. | **Rule or Shell Script:** If deterministic sequence, use a PowerShell/bash script or git alias. |
| **CG-2: External Tool Mutation** | CoALA §3 (Action Space Decoupling) | The task must execute *External Actions* (file I/O, terminal commands, AST queries, REST/MCP APIs) that inspect and mutate the system environment. | **Prompt or Skill:** If purely text-in/text-out without side-effects, keep as a cognitive skill or prompt. |
| **CG-3: Reflexion & Error Recovery** | Andrew Ng Pattern 1 & Xi et al. §3.3 | The execution environment exhibits runtime surprises (test failures, syntax errors, platform traps). The agent must catch exceptions, inspect logs, and iteratively self-correct. | **Pre-Commit Hook:** If failure is binary without need for autonomous repair, use a git hook. |
| **CG-4: Measurable Toil Justification** | Chip Huyen §3 (Systems Economics) | The workflow consumes $\ge 15$ minutes of active human toil per week or occurs with recurring frequency ($AVS \ge 50$), justifying the engineering cost of a micro-harness and test suite. | **Ad-hoc Execution:** If rare one-off, handle interactively without authoring an agent. |
| **CG-5: Containable Blast Radius** | Oracle `agent-spec` & SWE-bench | External mutations can be strictly bounded within an isolated directory, branch, or verified with an automated git working-tree rollback mechanism (`git stash`). | **Human-Only Task:** If actions have irreversible production risk, keep strictly manual. |

---

## 3. Tier 2: The 5 Optional Value-Add Enhancers (Architectural Multipliers)

These criteria are **not strictly required** to build an agent, but when present, they substantially increase the candidate's **Agent Viability Score (AVS)** and determine which advanced architectural capabilities are scaffolded into `/build-agent`:

### OE-1: Episodic Cross-Session Memory (CoALA §2 & Harrison Chase)
- **Signal:** The agent benefits from remembering past execution attempts, recurring codebase failure modes, or performance baselines across separate invocations.
- **Architectural Scaffolding:** Configures `.agents/memory/<agent-name>.jsonl` state journal and working memory compaction in `/build-agent`.

### OE-2: Multi-Perspective Deliberation / Adversarial Check (Xi et al. §4 & Anthropic §4)
- **Signal:** The workflow benefits from opposing or specialized personas (e.g. Creator vs. Critic, Security Auditor vs. Performance Optimizer, Standards Reviewer vs. Spec Verifier).
- **Architectural Scaffolding:** Promotes candidate to `multi-agent-squad` with Lead Orchestrator, isolated worktrees, and structured handoff contracts.

### OE-3: Persistent Sentinel Scheduling / Daemon Vigilance (Anthropic §5)
- **Signal:** The task requires continuous background vigilance, file watching, interval polling, or event-driven triggers (e.g. skill synchronization, test flake monitoring).
- **Architectural Scaffolding:** Classifies candidate as `autonomous-sentinel` with cron schedule, health check endpoint (`--health`), and alerting hooks.

### OE-4: Dynamic Model Context Protocol (MCP) Integration (Anthropic MCP Spec)
- **Signal:** The task requires interacting with third-party tools or SaaS platforms (GitHub issues, Linear, browser automation, PostgreSQL, Stripe).
- **Architectural Scaffolding:** Scaffolds MCP server configuration stubs and client schemas in `.agents/specs/<agent-name>.spec.yaml`.

### OE-5: Multimodal Sensory Grounding (Xi et al. §3.2)
- **Signal:** The task inspects visual artifacts, UI screenshots, rendered DOM snapshots, or PDF architecture diagrams.
- **Architectural Scaffolding:** Equips agent with `agent-browser` or vision-capable model routing in `/build-agent`.

---

## 4. Agent Viability Score (AVS) Mathematical Formulation

Rank all qualified candidates using the boosted AVS equation:

$$\text{AVS} = \frac{\text{Monthly Frequency} \times \text{Mean Human Toil (Minutes)}}{\text{Blast Radius Factor}} \times \left(1 + 0.15 \times N_{\text{optional}}\right)$$

Where:
- **Monthly Frequency:** Estimated occurrences per month.
- **Mean Human Toil:** Active minutes the developer spends manually executing or monitoring the task.
- **Blast Radius Factor:**
  - `1.0` = Read-only / Scratchpad generation (Zero mutation risk).
  - `1.5` = Scoped file modifications with git rollback (Low risk).
  - `2.5` = External API writes, database changes, or system background loops (Medium risk).
  - `4.0` = Unbounded file writes or destructive shell access (High risk).
- $N_{\text{optional}}$: Count of Tier-2 Optional Enhancers met ($0 \le N_{\text{optional}} \le 5$), granting up to a **+75% priority bonus**.

**Triage Priority Bands:**
- **AVS ≥ 100:** **Tier-1 Immediate Build Candidate** (Massive ROI; construct immediately via `/build-agent`).
- **50 ≤ AVS < 100:** **Tier-2 High-Value Candidate** (Strong candidate for sprint automation).
- **AVS < 50:** **Tier-3 Low Priority / Reject** (Better served by a script, hook, or manual execution).

---

## 5. Negative vs Positive Exemplars

### ❌ Negative Exemplars (Do NOT Agentify)
1. **Deterministic code formatting:** Fails CG-1 (Static linear execution) and CG-3 (No dynamic reflexion). *Solution: Git pre-commit hook with Prettier/Black.*
2. **Regex AST search across files:** Fails CG-2 (No mutation) and CG-1. *Solution: Direct CLI command with `ast-grep`.*
3. **One-shot prompt rewriting:** Fails CG-2 (Purely text-in/text-out). *Solution: `/prompt-generate` skill.*
4. **Git push and branch creation:** Fails CG-1 and CG-3. *Solution: `/piv-create-pr` skill or git alias.*

### ✅ Positive Exemplars (Prime Agent Candidates)
1. **`pipeline-stage-runner` (`solo-tool-user`):** Passes CG-1 (Multi-stage state), CG-2 (File I/O & command execution), CG-3 (Test validation gates), CG-4 (30+ mins toil per run), CG-5 (Git worktree rollback).
2. **`windows-compat-guard` (`solo-tool-user`):** Passes CG-1 (AST & encoding inspection), CG-2 (File modification & test execution), CG-3 (Fixes encoding & path errors), CG-4 (Recurring developer friction), CG-5 (Scoped shimming).
3. **`skill-sync-sentinel` (`autonomous-sentinel`):** Passes all 5 Critical Gates + OE-3 (Persistent Daemon Scheduling), keeping repo and global Antigravity config synchronized in real-time.
