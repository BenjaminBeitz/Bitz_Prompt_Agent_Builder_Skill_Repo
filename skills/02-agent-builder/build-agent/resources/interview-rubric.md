# 4-Station Systems Walkthrough Interview Rubric

This rubric guides the interactive walkthrough interview conducted after the user approves the initial **Agent Spec Sheet**. It fast-forwards low-risk parameters and focuses human engineering decisions strictly on high-blast-radius seams.

---

## 🧭 Interview Steering Principles

1. **Fast-Forward by Default:** If a parameter is unambiguous from the approved Spec Sheet (e.g. system name, read-only tools, standard 10-step limits), present it as a pre-assembled recommendation requiring only single-key acceptance (`Enter` or `Y`).
2. **Focus on High-Blast-Radius Seams:** Only probe deeply when actions involve file writes, shell execution, external APIs, multi-agent debate, or failure recovery.
3. **Hard Budgets:** Maximum 1–2 questions per station. Never ask open-ended vague questions; provide 2–3 concrete options with an explicit opinionated recommendation.

---

## 🏛️ Station 1: Domain Grounding & Blast Radius

**Objective:** Ground the agent in workspace-specific domain terms (`CONTEXT.md`) and establish physical execution boundaries.

### Check 1.1: Domain Context Ingestion
- *Action:* Inspect workspace for `CONTEXT.md` or domain documents.
- *Probe:*
  > "I detected the project's domain model in `CONTEXT.md`. Would you like to bind the following domain invariants into the agent's semantic context?"
  - **(A) [Recommended] Full Domain Binding:** Injects ubiquitous domain terms and business rules into the system instructions.
  - **(B) Isolated Scoped Binding:** Injects only domain entity definitions relevant to the agent's specific tools.
  - **(C) Generic / Unbound:** Operates purely on standard software engineering knowledge without repository context.

### Check 1.2: Allowed Write Paths & Shell Access
- *Action:* Review requested write permissions.
- *Probe:*
  > "This agent requires file-writing capability. Which filesystem boundary should we lock?"
  - **(A) [Recommended] Scoped Directory:** Restricts file writes exclusively to `{{TARGET_DIR}}` and creates an automatic git stash snapshot on entry.
  - **(B) Isolated Worktree (`Workspace='branch'`):** Spawns a temporary git worktree that auto-prunes upon task completion.
  - **(C) Unrestricted Workspace:** Grants write access across the current working tree.

---

## 🏛️ Station 2: Team Roster & Handoff Contracts (Multi-Agent Only)

**Objective:** Define the inter-agent communication protocol and eliminate circular debate deadlocks.

*(Skip this station if the archetype is Solo Tool-User or Autonomous Sentinel).*

### Check 2.1: Handoff Protocol & Privacy
- *Probe:*
  > "How should subagents exchange context and deliverables across the team?"
  - **(A) [Recommended] Artifact-Based Handoffs:** Subagents keep scratchpads private and communicate exclusively through structured Markdown report files in `.agents/reports/`.
  - **(B) Structured JSON Task Mailbox:** Pass typed JSON task payloads with strict input/output schemas.
  - **(C) Shared Conversation Stream:** All agents share a single conversational context.

### Check 2.2: Debate Turn Ceiling & Arbitration
- *Probe:*
  > "When specialist agents disagree on an architectural approach or implementation, how should deadlock be resolved?"
  - **(A) [Recommended] 1-Round Debate + Lead Arbitration:** Specialists submit Thesis and Antithesis; if unresolved after 1 turn, the Lead Orchestrator arbitrates.
  - **(B) Majority Voting:** Simple consensus vote among workers (ties broken by Lead).
  - **(C) Human Escalation:** Immediately halt and prompt the human when specialists disagree.

---

## 🏛️ Station 3: Human-in-the-Loop Interventions & `ask_human`

**Objective:** Establish when the agent is permitted to make autonomous decisions vs. when it MUST stop and consult the human.

### Check 3.1: Irreversible Mutation Barrier
- *Probe:*
  > "Which external actions require explicit human confirmation before execution?"
  - **(A) [Recommended] High-Blast-Radius Barrier:** Require confirmation for git commits/pushes, external API mutations, or database updates; allow read-only queries and internal scratchpads autonomously.
  - **(B) Fully Autonomous:** Execute all planned actions without human confirmation (subject only to programmatic safety blocklist).
  - **(C) Step-by-Step Approval (`--debug-step`):** Prompt before every external tool invocation.

### Check 3.2: Mid-Flight Clarification (`ask_human`) Trigger
- *Probe:*
  > "When the agent encounters ambiguous requirements or missing parameters midway through execution, how should it handle uncertainty?"
  - **(A) [Recommended] Interactive Clarification (`ask_human`):** Pause execution, serialize state to `.pending_action.json`, and prompt the user with targeted multiple-choice options.
  - **(B) Best-Effort Guessing:** Make an educated guess based on domain context and flag the assumption in the final deliverable.
  - **(C) Fail Fast:** Immediately abort task with an error report.

---

## 🏛️ Station 4: Acceptance Test & Fired Conditions

**Objective:** Lock the Day-1 Golden Probe and establish zero-tolerance failure criteria.

### Check 4.1: The Day-1 Tracer Probe
- *Action:* Synthesize a reproducible test input from the user's initial explanation.
- *Probe:*
  > "Here is the proposed Day-1 verification scenario:
  > **Input:** `{{MOCK_INPUT_TASK}}`
  > **Expected Tool Sequence:** `{{EXPECTED_TOOL_FLOW}}`
  > **Assertion Contract:** `{{EXPECTED_ASSERTION}}`
  > Does this accurately represent a successful execution?"
  - **(A) [Recommended] Approve Test Scenario:** Locks probe into `.agents/tests/{{AGENT_NAME}}-probe.md`.
  - **(B) Adjust Input / Assertions:** Calibrate test parameters.

### Check 4.2: Fired Conditions (Hard Refusals)
- *Probe:*
  > "We locked the following 'Fired Conditions' (unacceptable failure modes):
  > 1. `{{FIRED_CONDITION_1}}`
  > 2. `{{FIRED_CONDITION_2}}`
  > Would you like to add any custom refusal conditions?"
  - **(A) [Recommended] Lock Boundaries:** Finalize current refusal rules.
  - **(B) Add Custom Refusal Rule:** Specify additional unacceptable outcomes.
