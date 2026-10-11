---
name: build-agent
description: "Spec-driven agent engineering engine that transforms any natural language task into a tailored Specification Sheet, conducts a risk-weighted systems interview, and constructs production-ready agents or multi-agent teams."
argument-hint: "[explain what you want the agent or agent team to do | --from-spec <path.yaml>] [--upgrade <name>] [--preset <name>]"
---

# Build Agent: Spec-Driven Autonomous Agent Engineering Engine
*Grounded in the Top 5 Foundational Standards (Xi et al. 86pp Survey, CoALA Cognitive Architecture, Anthropic "Building Effective Agents" & MCP, Oracle agent-spec / Agent Protocol, and Andrew Ng / Harrison Chase Frameworks)*

`build-agent` is the definitive systems-engineering skill for creating autonomous agents and multi-agent teams in **Google Antigravity**. It moves past stateless prompt generation to construct **complete operational systems** complete with runtime harnesses, CoALA action decoupling, deterministic blast-radius safety interceptors, and Day-1 verification harnesses.

---

## 🧭 The 4 Invariant Architectural Laws

Every agent and multi-agent team constructed by `build-agent` strictly enforces these non-negotiable laws:

1. **Workflow-First Triage Law (Anthropic §2):** Never deploy an autonomous ReAct loop where a deterministic workflow (Prompt Chain or Router DAG) can achieve the task with lower latency and predictable cost.
2. **Action Space Decoupling Law (CoALA §3):** Strictly separate *Internal Actions* (memory mutation, belief updates, self-notes) from *External Actions* (file mutations, shell execution, external APIs). Plans must be internally verified before mutating the external world.
3. **Fail-Safe Blast Radius Invariant (Zero-Trust Security):** Prohibit destructive shell commands programmatically (`rm -rf /`, `git push --force`), enforce human confirmation barriers on high-blast-radius external mutations, and sanitize 100% of credentials (`[REDACTED_SECRET]`) in logs and traces.
4. **Deterministic Working Tree Rollback (SWE-bench & PIV Loop):** Take an internal git checkpoint (`git stash create`) upon task entry. If 3-strike reflexion fails or execution aborts, automatically rollback the working tree to guarantee zero dirty/broken state left on disk.

---

## 🔄 The 5-Stage Operational Protocol

```
[User prompt OR --from-spec draft.yaml]
         ↓
Stage 1: Intent Intake & Triage Gate (Classify Workflow vs Loop & Synthesize Spec Sheet)
         ↓
Stage 2: Mandatory Approval Gate (Hard barrier: human reviews and approves Spec Sheet)
         ↓
Stage 3: 4-Station Walkthrough Interview (Fast-forwards defaults; grills high-blast-radius seams)
         ↓
Stage 4: Multi-Substrate Scaffolding & Verification (.agents/specs/, .agents/agents/, runner.py)
         ↓
Stage 5: Master Registry Sync (.agents/agents.json)
         ↓
Stage 6: Automated Day-1 Verification & Golden Tracer Execution Gate (ARI Certification)
```

---

### Stage 1: Intent Intake & Anthropic Triage Gate

When invoked with a task description `$ARGUMENTS`:

1. **Check for Special Flags:**
   - If `--from-spec <path.yaml>` (or `--spec <path.yaml>`) is passed:
     - Ingest the candidate draft YAML authored by `/agent-opportunity-scan` (or external specification).
     - Extract `name`, `archetype`, `problem`, `tools`, `blast_radius`, `invariants`.
     - Hydrate the Spec Sheet directly from the YAML fields without manual conversational grilling.
     - Jump straight to **Stage 2: Mandatory Approval Gate** to display the pre-populated Spec Sheet for human confirmation.
   - If `--upgrade <name>` is passed, jump to **In-Place Spec Migration & Backup**.
   - If `--preset <name>` is passed, hydrate from the preset library (`solo-tool-user`, `multi-agent-squad`, `autonomous-sentinel`).
2. **Execute the Anthropic Triage Gate:**
   - *Deterministic Workflow DAG:* If the task is sequential, single-pass, or has a fixed step sequence (e.g. daily summary, label triage, format converter).
   - *Autonomous Agent Loop:* If the task requires dynamic exploration, file-tree traversal, iterative debugging, or environment feedback loops.
3. **Classify Architectural Archetype:**
   - *Solo Tool-User:* Single focused agent with bounded tools and ephemeral context.
   - *Multi-Agent Squad:* Hierarchical Lead Orchestrator with 2–3 leaf workers operating in isolated worktrees with structured artifact handoffs.
   - *Autonomous Sentinel / Daemon:* Long-running scheduled/event monitor with append-only state journals.
4. **Synthesize the Tailored Spec Sheet:**
   - Load [`resources/spec-sheet-template.md`](resources/spec-sheet-template.md).
   - Populate all 6 dimensions based on the user's explanation.
   - Explicitly highlight the top 2 unstated assumptions as **"Assumed Defaults"**.
   - Present the formatted Spec Sheet directly in the chat window.

---

### Stage 2: Mandatory Approval Barrier

> [!IMPORTANT]
> **Hard Execution Stop:** You MUST NOT proceed to interview or scaffold files until the user explicitly reviews and approves the Spec Sheet.

Present the user with three clear choices:
- **(A) Approve Spec Sheet as-is:** Proceed directly to the Stage 3 Walkthrough Interview.
- **(B) Calibrate Specific Parameters:** Tweak tool list, adjust blast radius, switch archetype, or modify Fired Conditions.
- **(C) Abort / Re-triage:** Discard draft and exit cleanly.

---

### Stage 3: Risk-Weighted Guided Walkthrough Interview

Once approved, execute the 4-station interview rubric from [`resources/interview-rubric.md`](resources/interview-rubric.md):

- **Station 1: Domain Grounding & Blast Radius:**
  - Check for workspace `CONTEXT.md`; offer to bind domain invariants into the agent's semantic context.
  - Confirm allowed write directories, prohibited shell commands, and worktree isolation modes.
- **Station 2: Team Roster & Handoff Contracts (Multi-Agent Only):**
  - Lock artifact-based handoffs in `.agents/reports/` (privacy by default).
  - Enforce debate turn ceiling ($N \le 2$ or $3$ rounds) before forced Lead arbitration.
- **Station 3: Human-in-the-Loop Interventions & `ask_human`:**
  - Define exact checkpoints requiring human confirmation (e.g. destructive migrations, external API payments).
  - Equip agent with the native `ask_human` interactive clarification primitive.
- **Station 4: Acceptance Test & Fired Conditions:**
  - Lock the Day-1 Golden Tracer Probe scenario.
  - Finalize the negative "Fired Conditions" (zero-tolerance failure modes).

*Ergonomic Rule:* Fast-forward unambiguous parameters with 1-click recommendations. Only grill on high-blast-radius decisions.

---

### Stage 4: Multi-Substrate Scaffolding & Construction

When the interview concludes, automatically author the complete system deliverables:

1. **Human Narrative Specification:**
   - Write to `.agents/specs/<agent-name>.spec.md` using the finalized Spec Sheet.
2. **Oracle Declarative YAML Specification:**
   - Write to `.agents/specs/<agent-name>.spec.yaml` conforming to [`resources/oracle-spec-template.yaml`](resources/oracle-spec-template.yaml).
3. **Antigravity Native Subagent Definition:**
   - Write to `.agents/agents/<AgentName>/agent.md` with valid YAML frontmatter (`name`, `description`, `tools`, `hidden: true`).
4. **Standalone Zero-Dependency Python Micro-Harness:**
   - Hydrate [`resources/micro-harness-template.py`](resources/micro-harness-template.py) into `.agents/agents/<AgentName>/runner.py`.
   - Embeds Universal REST client, Git working tree rollback, non-interactive shell defaults (`CI=true`, `stdin=DEVNULL`), dynamic plan tracker, CoALA action decoupling, 16KB payload armor, goal pinning (`<<<ACTIVE_MISSION_ANCHOR>>>`), 70% context compaction, 3-strike reflexion, and `--health` / `--mock` / `--verify-probe` flags.
5. **Custom Tool Stubs (if missing tools detected):**
   - Hydrate [`resources/tool-stub-template.py`](resources/tool-stub-template.py) into `.agents/tools/<tool_name>.py`.
6. **Day-1 Verification Probe:**
   - Author `.agents/tests/<agent-name>-probe.md` and canned fixtures in `.agents/tests/<agent-name>-fixtures.json`.

---

### Stage 5: Master Registry Sync

1. **Sync Master Registry (`.agents/agents.json`):**
   - Read or initialize `.agents/agents.json`.
   - Register the new agent entry:
     ```json
     {
       "name": "<agent-name>",
       "archetype": "<archetype>",
       "version": "1.0.0",
       "created_at": "<ISO-timestamp>",
       "spec_md": ".agents/specs/<agent-name>.spec.md",
       "spec_yaml": ".agents/specs/<agent-name>.spec.yaml",
       "subagent_md": ".agents/agents/<AgentName>/agent.md",
       "runner_py": ".agents/agents/<AgentName>/runner.py",
       "tools": ["<tool_1>", "<tool_2>"],
       "verified": false,
       "ari_score": null
     }
     ```

---

### Stage 6: Automated Day-1 Verification & Golden Tracer Execution Gate

Immediately following Stage 5 scaffolding, `build-agent` executes the integrated Day-1 verification harness without requiring manual user commands:

1. **Static Invariant Validation:**
   - Verify all generated files exist on disk.
   - Verify Python syntax via `python -m py_compile .agents/agents/<AgentName>/runner.py`.
   - Verify YAML schema via `python -c "import yaml; yaml.safe_load(open('.agents/specs/<agent-name>.spec.yaml'))"`.
   - Verify JSON registry format via `python -m json.tool .agents/agents.json`.
2. **Automated Golden Tracer Probe Execution:**
   - Execute: `python .agents/agents/<AgentName>/runner.py --verify-probe`
   - The probe automatically validates:
     - **Check 1: Directory & State Structure** (spec & test directories).
     - **Check 2: Safe Tool Dispatch** (micro-harness shell execution plumbing).
     - **Check 3: Blast-Radius Safety Interceptor** (confirms `rm -rf` and destructive actions are hard-blocked).
     - **Check 4: Secret Sanitization** (confirms credentials are automatically scrubbed).
     - **Check 5: Golden Tracer Fixtures** (validates fixture presence and schema).
3. **Agent Reliability Index (ARI) Certification:**
   - The harness generates `.agents/reports/<AgentName>/day1_verification.md` with the computed ARI score:
     $$\text{ARI} = \frac{\text{Passed Golden Invariants} \times 100}{\text{Total Assertions}}$$
   - If ARI $\ge 80\%$, the agent is certified. Update `.agents/agents.json` with `"verified": true`, `"ari_score": <score>`.
   - If ARI $< 80\%$, the agent triggers 3-strike reflexion to remediate the harness before declaring failure.
4. **Deliverable Presentation:**
   - Output the final certification results and ARI score directly to the user in chat with clickable links to all generated artifacts:
     ```text
     🎉 Agent Construction & Day-1 Verification Certified!
     
     Deliverables:
       - Human Spec: .agents/specs/<agent-name>.spec.md
       - Oracle YAML: .agents/specs/<agent-name>.spec.yaml
       - Subagent Contract: .agents/agents/<AgentName>/agent.md
       - Python Harness: .agents/agents/<AgentName>/runner.py
       - Day-1 Verification: .agents/reports/<AgentName>/day1_verification.md (ARI: 100%)
     ```

---

## 🛠️ In-Place Migration & Upgrade Protocol (`--upgrade <name>`)

When invoked with `--upgrade <name>`:
1. Verify `<name>` exists in `.agents/agents.json`.
2. Create an atomic backup snapshot in `.agents/backup/<name>_<timestamp>/`.
3. Load the existing `.agents/specs/<name>.spec.md` and present a visual Markdown diff of proposed changes.
4. Require explicit user approval before applying in-place modifications.
5. Update the version string to `1.1.0` and update `.agents/agents.json`.
