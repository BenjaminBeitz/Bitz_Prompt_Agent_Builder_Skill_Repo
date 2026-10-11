---
name: prompt-zero-shot
description: Transforms raw prompts into high-precision zero-shot prompts using S2A, RaR, RE2, Self-Ask, Role/Style conditioning, and Question Clarification.
argument-hint: "<raw-prompt-or-intent> [--technique <s2a|rar|re2|self-ask|role>]"
---

# Zero-Shot Prompt Engineering: Precision Intent Alignment Engine

> **Theoretical Foundation:** Grounded in *The Prompt Report: A Systematic Survey of Prompt Engineering* (Schulhoff et al., 2025; Section 2.2.1.3 "Zero-Shot Prompting", Section 5.2.1 "Prompt Sensitivity", and Section 5.2.4 "Ambiguity").

This skill transforms raw, ambiguous, noisy, or underspecified human prompts into mathematically hardened, bias-resistant, and high-precision zero-shot prompts. It equips Google Antigravity agents to eliminate hallucinations, neutralize sycophancy, resolve semantic ambiguities, and anchor transformer attention without relying on few-shot in-context exemplars.

---

## 1. Theoretical Foundations & Ground Rules

### 1.1 Zero-Shot Conditioning vs In-Context Learning
In zero-shot prompting, the model is presented with task instructions and context $X$ without input-output demonstration pairs $\{(x_i, y_i)\}_{i=1}^k$. The posterior distribution $P(Y \mid X)$ is governed entirely by:
1. **Instruction Framing:** Activating specific latent representations through semantic clarity.
2. **Prior Conditioning:** Inducing domain heuristics via persona, role, and style constraints.
3. **Attention Steering:** Eliminating distracting context tokens to prevent attention dispersion.

### 1.2 The Triad of Failure Modes (The Prompt Report §5.2)

1. **Prompt Sensitivity (§5.2.1):** LLMs exhibit high variance under minor perturbations (word order, punctuation, token casing). A naive zero-shot prompt often triggers brittle, sub-optimal generation paths.
2. **Prompt Ambiguity (§5.2.4):** Human prompts frequently omit critical invariants (runtime constraints, thread-safety, failure domains). When prompts are underspecified, models either hallucinate hidden premises or generate generic "vibe-coding" boilerplate.
3. **The Sycophancy Trap:** When prompts include opinions, leading questions, or conversational noise (e.g., *"I think the bug is in Redis cache, right?"*), models suffer from strong confirmation bias, agreeing with erroneous human hypotheses rather than analyzing objective ground truth.

---

## 2. Taxonomy of Zero-Shot Techniques (The Prompt Report Fig. 2.2 & §2.2.1.3)

| Technique | Primary Paper Reference | Core Mechanism | Best Used For |
| :--- | :--- | :--- | :--- |
| **System 2 Attention (S2A)** | Weston & Sukhbaatar (2023) | Rewrites input to purge extraneous noise, bias, and leading opinions before generation | Debugging logs, noisy context, biased user queries |
| **SimToM (Simulated Theory of Mind)** | Wilf et al. (2023) | Explicitly isolates multi-entity knowledge states and perspectives to prevent belief leakage | Multi-agent coordination, permissions, game theory |
| **Rephrase and Respond (RaR)** | Deng et al. (2023) | Rephrases and expands the query into an unambiguous technical problem before answering | High-level, underspecified, or colloquial human requests |
| **Re-reading (RE2)** | Xu et al. (2023) | Repeats instructions/context strategically to re-energize deep-layer attention weights | Long context windows, complex logic with strict constraints |
| **Self-Ask** | Press et al. (2022) | Compositionally decomposes queries by deciding and answering sub-questions first | Multi-hop reasoning, architectural dependency analysis |
| **Role / Persona Prompting** | Wang et al. (2023j); Schmidt et al. (2023); Zheng et al. (2023d) | Conditions latent space on expert domain heuristics and rigor | Code reviews, security audits, distributed systems |
| **Style Prompting** | Lu et al. (2023a) | Enforces deterministic output syntax, schema, tone, and verbosity bounds | Machine-consumable diffs, RFC 2119 specs, structured PRDs |
| **Emotion Prompting** | Li et al. (2023a) | Injects psychological importance/urgency to increase calibration and attention | High-stakes security validations, mission-critical migrations |
| **Question Clarification** | Rao & Daume (2019); Zhang & Choi (2023) | Identifies underspecified axes and poses targeted clarifying questions before execution | Ambiguous feature requests, vague error descriptions |

---

## 3. Algorithmic Blueprints for Zero-Shot Primitives

### 3.1 System 2 Attention (S2A) (Weston & Sukhbaatar, 2023)
*Operational Protocol:* When an incoming prompt contains opinionated commentary, emotional rants, or huge dumps of irrelevant console logs, S2A executes an attention-purging step:

```markdown
[SYSTEM 2 ATTENTION PROTOCOL]
Given the raw input below, perform a strict two-stage extraction:
1. De-noised Context Reconstruction:
   Extract ONLY the objective technical facts, reproduction steps, code snippets, and system constraints.
   Completely discard user conjectures, emotional bias, unverified assumptions, and extraneous logs.
2. Isolated Reasoning:
   Solve the problem using EXCLUSIVELY the de-noised context extracted in Step 1.
```

### 3.2 SimToM: Simulated Theory of Mind (Wilf et al., 2023)
*Operational Protocol:* For workflows involving multiple actors (e.g. Client vs Server, User A vs Tenant B, Subagent Alpha vs Subagent Beta), SimToM enforces belief isolation:

```markdown
[SIMULATED THEORY OF MIND (SimToM) PROTOCOL]
Identify all distinct entities/actors in the system.
Before answering, explicitly delineate the epistemic boundary for each entity:
- Entity [A] observes: {list verified facts known to A}
- Entity [A] DOES NOT observe: {hidden state unknown to A}
- Entity [B] observes: {list verified facts known to B}
Answer the objective query by strictly respecting these perspective barriers. Never leak entity B's privileged state into entity A's decision space.
```

### 3.3 Rephrase and Respond (RaR) (Deng et al., 2023)
*Operational Protocol:* Unpacks conversational prompts into formal technical problem statements:

```markdown
[REPHRASE AND RESPOND (RaR) PROTOCOL]
Step 1 - Semantic Expansion & Rephrasing:
Rephrase the user's intent into a precise, self-contained, domain-specific engineering specification. Resolve any vague pronouns, clarify technical boundaries, and state implicit assumptions explicitly.
Step 2 - Execution:
Respond to and execute the rephrased specification from Step 1.
```

### 3.4 Re-Reading (RE2) (Xu et al., 2023)
*Operational Protocol:* Overcomes the "Lost in the Middle" transformer attention decay on long contexts:

```markdown
<TASK_SPECIFICATION>
[Insert detailed architectural requirements, API boundaries, and invariants]
</TASK_SPECIFICATION>

<INPUT_CONTEXT>
[Insert complex codebase file or long diff]
</INPUT_CONTEXT>

Read the task specification again:
<TASK_SPECIFICATION>
[Exact duplicate of task specification]
</TASK_SPECIFICATION>

Now generate the implementation strictly complying with every invariant above.
```

### 3.5 Self-Ask (Press et al., 2022)
*Operational Protocol:* Decomposes multi-hop dependencies into explicit sequential questions:

```markdown
[SELF-ASK DECOMPOSITION PROTOCOL]
Query: <Compositional Problem>
Are follow-up questions needed here? Yes.
Follow-up 1: <Sub-question 1>
Intermediate Answer 1: <Derived factual answer 1>
Follow-up 2: <Sub-question 2 depending on Answer 1>
Intermediate Answer 2: <Derived factual answer 2>
Therefore, the final synthesized response is: <Final Answer>
```

### 3.6 Role & Style Conditioning (Wang et al., 2023j; Lu et al., 2023a)
*Operational Protocol:* Moves beyond theatrical roleplay by embedding concrete verification heuristics:

```markdown
[ROLE & STYLE SPECIFICATION]
- Persona: Principal Systems Architect & Distributed Database Specialist.
- Evaluation Heuristics: Zero tolerance for data races, silent error swallowing, or unindexed queries.
- Output Style: ASD-STE100 Simplified Technical English, concise markdown tables for trade-offs, bulleted invariant rules, RFC 2119 keywords (MUST, SHALL, SHOULD NOT). Zero conversational pleasantries.
```

### 3.7 Question Clarification & Ambiguity Resolution (Rao & Daume, 2019; Zhang & Choi, 2023)
*Operational Protocol:* Blocks premature execution when degrees of freedom exceed tolerance:

```markdown
[AMBIGUITY RESOLUTION PROTOCOL]
Analyze the user's request across 4 axes:
1. Scope & Invariants (What are the non-negotiables?)
2. Environment & Tooling (Language versions, OS, target runtimes)
3. Performance & Scale (Latency bounds, concurrency, memory constraints)
4. Failure Semantics (How should errors be recovered or surfaced?)

If any axis contains unresolved ambiguity that creates divergent implementation forks:
HALT execution. Formulate maximum 3 targeted, multiple-choice clarifying questions before writing code.
```

---

## 4. The 5-Stage Zero-Shot Hardening Pipeline

When you invoke `/prompt-zero-shot`, the agent executes this unified pipeline:

```
[Raw Human Prompt / Intent]
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 1: Noise & Bias Triage (S2A)    │ ──> Strip sycophantic cues & irrelevant noise
└───────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 2: Ambiguity & Scope Detection  │ ──> Detect under-specified axes; clarify or branch
└───────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 3: Semantic Expansion (RaR/Self)│ ──> Expand intent & generate sub-questions
└───────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 4: Structural Reinforcement     │ ──> Anchor attention via RE2, Role & Style bounds
└───────────────────────────────────────┘
            │
            ▼
┌───────────────────────────────────────┐
│ Stage 5: Calibrated Zero-Shot Prompt  │ ──> High-fidelity, deterministic prompt output
└───────────────────────────────────────┘
```

---

## 5. Anti-Patterns & Sycophancy Traps in Zero-Shot Prompting

### ❌ Anti-Pattern 1: The Sycophantic Validation Trap
- *Flawed Prompt:* "I wrote this caching logic in Node.js, and I'm pretty sure using an in-memory global map is safe because Node is single-threaded. Can you confirm?"
- *Why it fails:* The model is heavily incentivized to agree with the user's single-threaded premise, overlooking async event-loop interleaving, memory leaks, and multi-process cluster topologies.
- *Zero-Shot Remedy (S2A):* Strip the leading conjecture: "Analyze the concurrency, memory lifecycle, and safety boundaries of using an in-memory global map in Node.js under multi-process clustering and async I/O."

### ❌ Anti-Pattern 2: The Shallow Persona Trap
- *Flawed Prompt:* "Act as a world-class senior developer and review my code."
- *Why it fails:* "World-class senior developer" is empty semantic theater. It provides zero domain invariants or operational heuristics.
- *Zero-Shot Remedy:* Define explicit persona heuristics: "Act as a Senior Database Reliability Engineer. Evaluate the following queries specifically against index cardinality, write amplification under B-Tree page splits, and transaction isolation deadlocks."

### ❌ Anti-Pattern 3: The Context Drowning Trap
- *Flawed Prompt:* [Pastes 500 lines of random bash output, git logs, and stack traces] "Why is my test failing?"
- *Why it fails:* Irrelevant tokens dilute self-attention across the transformer context.
- *Zero-Shot Remedy (S2A + RE2):* Isolate the exact failing assertion, repeat the test contract directly prior to the generation target, and purge irrelevant execution logs.

---

## 6. Concrete Before-and-After Transformations

### Case A: Concurrency & Architectural Deadlock
- **Raw User Input:**
  > "I have a deadlock when users transfer funds between accounts. I think it's because my Postgres connection pool is too small. How do I increase it in Prisma?"
- **Zero-Shot Hardened Prompt (S2A + RaR + Self-Ask):**
  ```markdown
  [CONTEXT & OBJECTIVE]
  System: Financial ledger running on PostgreSQL with Prisma ORM.
  Observed Symptom: Transaction deadlocks during concurrent bilateral fund transfers between accounts.

  [DE-NOISED ATTENTION (S2A)]
  Disregard user hypothesis regarding connection pool size (connection exhaustion produces timeout errors, not database deadlocks).

  [SELF-ASK DECOMPOSITION]
  1. What is the fundamental root cause of deadlocks in concurrent bilateral account transfers? (e.g. inconsistent resource lock ordering between Account A->B and Account B->A).
  2. How must the transfer query be rephrased and structured to guarantee deterministic lock acquisition order?
  3. Provide the idiomatic Prisma interactive transaction implementation enforcing this lock order.

  [STYLE CONSTRAINTS]
  - Explain the mechanism in <= 3 sentences.
  - Provide complete, compilable TypeScript code.
  - Include zero conversational filler.
  ```

### Case B: Multi-Tenant RBAC & Security Boundary
- **Raw User Input:**
  > "Make sure tenant users can't see other tenant's projects in our multi-tenant SaaS."
- **Zero-Shot Hardened Prompt (SimToM + Question Clarification + Style):**
  ```markdown
  [SIMULATED THEORY OF MIND (SimToM)]
  Model two distinct tenants in a shared database schema:
  - Tenant Alpha (User ID: `u_alpha`, Org ID: `org_1`)
  - Tenant Bravo (User ID: `u_bravo`, Org ID: `org_2`)
  Epistemic Rule: `u_alpha` must possess zero queryable knowledge or projection of records where `org_id == org_2`.

  [AMBIGUITY CHECK & SELECTION]
  Clarify which architectural tenancy isolation model is implemented:
  - Option A: PostgreSQL Row Level Security (RLS) with session claims (`app.current_tenant`).
  - Option B: ORM-level query filtering middleware (e.g., Prisma Client Extensions).
  - Option C: Schema-per-tenant physical database separation.

  [SPECIFICATION & STYLE]
  Deliver:
  1. The minimal configuration to enforce Option A (RLS) or Option B (Middleware).
  2. A negative security integration test proving an unauthorized tenant query fails closed with 403 Forbidden.
  ```

---

## 7. Execution Protocol for Agents

When a user invokes `/prompt-zero-shot <prompt-or-topic>`:

1. **Parse Options:**
   - `--technique <s2a|rar|re2|self-ask|role|simtom>`: Focus on a specific zero-shot primitive.
   - If no technique flag is supplied, execute the complete **5-Stage Zero-Shot Hardening Pipeline**.
2. **Deconstruct & Triage:**
   - Detect and flag any Sycophancy Traps or leading premises in the user's input.
   - Separate verified facts from unverified conjectures.
3. **Generate Output:**
   - Present the **Hardened Zero-Shot Prompt** in a copy-pasteable fenced markdown block.
   - Annotate the transformation rationale: highlight which Prompt Report techniques were deployed and why.
   - Provide the execution command or direct continuation prompt.
