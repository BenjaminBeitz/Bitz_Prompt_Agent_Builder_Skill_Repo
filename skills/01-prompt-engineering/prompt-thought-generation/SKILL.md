---
name: prompt-thought-generation
description: Engineers advanced reasoning pathways into prompts using Step-Back abstraction, Thread-of-Thought, Tab-CoT, and Contrastive CoT architectures.
argument-hint: "<intent-or-prompt> [--topology <step-back|thot|tab-cot|contrastive|analogical>]"
---

# Prompt Thought Generation: Advanced Cognitive Architectures & Reasoning Scaffolding

> **"In autoregressive transformers, computation is inextricably bound to token emission. A model cannot 'think' without generating tokens; thought-generation prompting is the disciplined allocation of computational budget to state representation, concept abstraction, and invariant verification prior to answer commitment."**  
> — Grounded in *The Prompt Report: A Systematic Survey of Prompting Techniques* (Schulhoff et al., 2025, Section 2.2.2: "Thought Generation", pp. 12–13).

---

## 1. What This Skill Is

`prompt-thought-generation` is a production-grade cognitive engineering skill for Google Antigravity. It transforms raw, ambiguous, or fragile instructions into rigorously scaffolded reasoning prompts. Rather than relying on naive direct generation ("vibe coding"), this skill instills explicit intermediate thought pathways that maximize deductive depth, neutralize hallucinations, and bypass common LLM cognitive traps.

### Core Theoretical Foundation (The Prompt Report §2.2.2)
Autoregressive Large Language Models execute a fixed amount of computation per forward pass (per token). Complex logical deduction, formal verification, multi-variable constraints, and high-entropy domain decisions fail under direct generation because the model is forced to commit to output tokens before traversing the required solution space. Thought-generation techniques force the decoder to emit an intermediate trajectory $T = (t_1, t_2, \dots, t_k)$ that shifts the conditional probability distribution of the final resolution $Y$ given query $X$:

$$P(Y \mid X) \longrightarrow P(T \mid X) \cdot P(Y \mid X, T)$$

This skill operationalizes every major thought-generation topology cataloged in Figure 2.2 of *The Prompt Report* (Schulhoff et al., 2025).

---

## 2. Thought Generation Architecture Matrix (Figure 2.2 Taxonomy)

| Technique | Primary Literature | Core Cognitive Mechanism | Primary Failure Mode Mitigated | Compute / Token Overhead | Recommended Engineering Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Chain-of-Thought (CoT)** | Wei et al. (2022b) | Decomposes complex multi-step reasoning into discrete deductive links. | Premature answer commitment; calculation jumps. | Moderate ($1.5\times - 3\times$) | Multi-tier architectural decisions; algorithm design; state machine logic. |
| **Zero-Shot-CoT** | Kojima et al. (2022); Zhou et al. (2022b); Yang et al. (2023a) | Thought inducers ("Let's think step by step") elicit zero-shot deductive trails. | Direct-answer hallucination without exemplars. | Low to Moderate ($1.2\times - 2\times$) | Ad-hoc refactoring; fast code explanations; initial exploratory analysis. |
| **Step-Back Prompting** | Zheng et al. (2023c) | Two-stage abstraction: extracts fundamental domain principles before solving the instance. | Getting lost in low-level noise, red herrings, or accidental complexity. | Moderate ($2\times$) | Distributed concurrency bugs; security boundary audits; domain-model alignment. |
| **Analogical Prompting** | Yasunaga et al. (2023) | LLM self-generates relevant analogous problem-solution pairs with CoT before target task. | Cold-start domain isolation; absence of curated exemplars. | High ($3\times - 4\times$) | Greenfield system protocol design; unfamiliar library integration. |
| **Thread-of-Thought (ThoT)** | Zhou et al. (2023) | Incremental segment-by-segment analysis across chaotic, massive context windows. | "Lost in the middle"; context poisoning; attentional degradation. | High ($2.5\times - 5\times$) | Monolithic code migrations; massive trace log diagnosis; chaotic legacy repo digestion. |
| **Tabular CoT (Tab-CoT)** | Jin & Lu (2023) | Enforces intermediate reasoning steps into structured Markdown tables with strict schema. | Narrative drift; semantic drift; fuzzy state transitions; rambling prose. | Moderate ($1.5\times - 2.5\times$) | Database schema migrations; API payload mapping; state machine transitions; matrix trade-offs. |
| **Few-Shot / Golden CoT** | Wei et al. (2022b); Zhang et al. (2022b) | Curated, mathematically verified high-fidelity exemplars demonstrating optimal reasoning topology. | Out-of-distribution reasoning; structural formatting variance. | High input context ($2\times - 4\times$) | Mission-critical linting; high-assurance safety/security checks; deterministic DSL generation. |
| **Contrastive CoT** | Chia et al. (2023) | Paired exemplars of valid reasoning and invalid/flawed reasoning with explicit failure rationale. | Subtle recurring misconceptions; antipodal blind spots; shallow heuristics. | High input context ($3\times - 5\times$) | Concurrency race condition prevention; type-safety invariant enforcement; edge-case auditing. |
| **Complexity-Based Prompting** | Fu et al. (2023b) | Filters/samples candidate chains prioritizing maximum reasoning depth (steps/nodes). | Shallow shortcut reasoning; heuristic hand-waving. | High inference cost ($3\times - 8\times$) | Hard combinatorial optimization; formal grammar parsing; cryptographic protocol verification. |
| **Uncertainty-Routed CoT** | Kadavath et al. (2022); Lin et al. (2023); Google (2023) | Dynamic routing: greedy pass first; triggers multi-path CoT only when uncertainty threshold breached. | Excessive latency and token budget burn on trivial deterministic queries. | Adaptive ($1\times$ baseline, $4\times$ fallback) | High-throughput agent loops; real-time IDE completion; cost-constrained pipelines. |
| **Active Prompting & Memory-of-Thought** | Diao et al. (2023); Li & Qiu (2023b) | Dynamically pools uncertain queries for exemplar generation and indexes validated thought chains in memory. | Static exemplar staleness; repeated re-derivation of solved patterns. | Amortized / Retrieval-based | Enterprise codebase knowledge base; continuous repo maintenance; team pattern registries. |
| **Automatic CoT (Auto-CoT)** | Zhang et al. (2022b) | Clusters problem space, samples centroid questions, and auto-generates verified CoT exemplars. | Manual prompt engineering bottleneck across diverse task suites. | One-time setup compute | Automated test-suite generation; multi-module scaffolding. |

---

## 3. Cognitive Topology Blueprints & Implementation Patterns

```
                                [Raw Intent / Query]
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
         [Simple / Low-Risk]                            [Complex / High-Risk]
                 │                                               │
       ┌─────────┴─────────┐                   ┌─────────────────┴─────────────────┐
       ▼                   ▼                   ▼                 ▼                 ▼
 [Zero-Shot-CoT]   [Uncertainty Route]    [Step-Back]         [ThoT]           [Tab-CoT]
 (Optimal Inducer)  (Greedy → Fallback)   (Abstraction)     (Long Context)   (State Matrix)
                                               │                 │                 │
                                               ▼                 ▼                 ▼
                                        [Domain Theory]   [Chunk Digests]   [Structured Table]
                                               │                 │                 │
                                               └────────┬────────┴─────────────────┘
                                                        ▼
                                             [Contrastive Guardrail]
                                              (Valid vs Invalid Path)
                                                        │
                                                        ▼
                                             [Decoupled Scratchpad]
                                              <thought> ──► <output>
```

### 3.1 Step-Back Prompting (Zheng et al., 2023c)
**Cognitive Mechanism:** Solves the "Abstraction Gap". When presented with a detailed, noisy problem, models often anchor on accidental surface details. Step-Back Prompting inserts an explicit Stage 1 where the agent abstracts the fundamental principles, physics, computer science axioms, or architectural invariants governing the domain, before attempting Stage 2 (concrete solution).

```markdown
<!-- Step-Back Scaffold Structure -->
## System Directives
You solve complex engineering challenges through Two-Stage Abstraction:

### Stage 1: Step-Back Abstraction
Before analyzing the specific code or scenario, answer the foundational question:
- "What are the underlying computer science principles, concurrency models, invariants, and operational physics governing this system?"
- Synthesize 2–4 immutable rules that dictate correct behavior in this domain regardless of implementation details.

### Stage 2: Grounded Instantiation
Apply the abstracted principles derived in Stage 1 directly to the target scenario:
- Map each concrete component to its theoretical counterpart.
- Deduce the solution solely through adherence to the Stage 1 principles.
```

### 3.2 Thread-of-Thought / ThoT (Zhou et al., 2023)
**Cognitive Mechanism:** Standard CoT breaks down when context windows exceed $10^4$ tokens or contain mixed conversational turns, unstructured stack traces, and large file diffs. ThoT implements an incremental divide-and-conquer strategy: it isolates context into discrete chronological or semantic blocks, performs sequential evaluation, maintains a running working-memory digest, and prevents earlier noise from corrupting downstream deductions.

```markdown
<!-- Thread-of-Thought (ThoT) Scaffold -->
## Multi-Segment Context Processing Protocol (ThoT)
You are analyzing a high-volume, multi-source context. Do NOT generate a final verdict immediately. Execute sequential thread analysis:

1. **Segment Partitioning:** Split the provided context into chronological or architectural segments ($S_1, S_2, \dots, S_n$).
2. **Sequential Thread Processing:**
   - **For Segment $S_i$:**
     - Extract raw factual claims, state changes, and error signatures.
     - Reconcile with working memory from Segment $S_{i-1}$.
     - Flag contradictions, state overrides, or invariant violations.
     - Emit an updated **Thread State Vector**.
3. **Thread Synthesis:**
   - Review the final State Vector across all segments.
   - Formulate the terminal diagnosis and corrective action.
```

### 3.3 Tabular Chain-of-Thought / Tab-CoT (Jin & Lu, 2023)
**Cognitive Mechanism:** Eliminates prose drift and token hallucinations by forcing intermediate deductions into a two-dimensional structured Markdown table. Tabular layout activates spatial and relational inductive priors in LLMs, forcing strict row-by-row alignment between preconditions, operations, state shifts, and validation checks.

```markdown
<!-- Tab-CoT Scaffold -->
## State-Transition Tabular Deduction
For all state mutations, migrations, or algorithmic steps, maintain reasoning in the following canonical Tab-CoT format before code emission:

| Step | Current State $S_t$ | Input / Event $E$ | Invariant / Precondition | Transition Function $f(S_t, E)$ | Next State $S_{t+1}$ | Post-Verification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ORDER_CREATED` | `PaymentAuthorized` | User balance >= amount | Lock funds, emit event | `PAYMENT_HELD` | PASS (Deterministic) |
| 2 | `PAYMENT_HELD` | `InventoryReserved` | SKU stock available | Decrement stock counter | `STOCK_ALLOCATED` | PASS (Atomic) |

Execute tabular deductions row-by-row. If any row violates an invariant, halt and trigger exception handling.
```

### 3.4 Contrastive Chain-of-Thought (Chia et al., 2023)
**Cognitive Mechanism:** Prevents positive-exemplar sycophancy and common recurring bugs by providing bipartite reasoning paths: the **Canonical Valid Path** contrasted against the **Subtle Flawed Path**, complete with an explicit cognitive autopsy explaining *why* the flawed path fails.

```markdown
<!-- Contrastive CoT Scaffold -->
## Dual-Path Dialectical Analysis
For the target architecture or code modification, evaluate both paths explicitly:

### Path A: The Plausible Flawed Path (Negative Exemplar)
- **Proposed Logic:** <Common heuristic or superficial implementation>
- **The Hidden Flaw:** <Exact race condition, memory leak, edge-case failure, or invariant breach>
- **Cognitive Failure Mode:** <Why an engineer or LLM is seduced into choosing this path>

### Path B: The Invariant-Hardened Path (Positive Exemplar)
- **Correct Logic:** <Rigorous, boundary-checked implementation>
- **Mathematical / Architectural Guarantee:** <Why this path holds under stress, concurrency, and network partitions>
- **Validation Tripwire:** <The specific test or assert that fails in Path A but succeeds in Path B>
```

### 3.5 Analogical Prompting (Yasunaga et al., 2023)
**Cognitive Mechanism:** When an agent lacks domain-specific few-shot exemplars, instruct it to recall and generate 2–3 structurally isomorphic problems from first principles, generate full CoT solutions for those problems, and project the shared abstraction onto the new target problem.

```markdown
<!-- Analogical Prompting Scaffold -->
## Self-Generated Analogical Schema Transfer
Before solving the user's problem:
1. **Analogy Recall:** Recall 2 distinct, well-understood computer science or software engineering problems that share the exact structural topology and algorithmic constraints of the target problem.
2. **Analogical Solution Trajectory:** For each analogy, explicitly detail the core challenge, the elegant solution pattern, and the governing invariant.
3. **Target Mapping:** Map the target problem's variables, seams, and constraints to the discovered analogical pattern, then synthesize the solution.
```

### 3.6 Optimal Zero-Shot Thought Inducers (Zhou et al., 2022b; Yang et al., 2023a)
**Empirical Findings:** While Kojima et al. (2022) popularized `"Let's think step by step"`, systematic meta-optimization (OPRO - Yang et al., 2023a; APE - Zhou et al., 2022b) demonstrates that prompt inducers that prime calm, rigorous, and deliberate verification outperform naive variants by significant margins across mathematical and symbolic benchmarks:
- **Baseline:** `"Let's think step by step."` (Kojima et al., 2022)
- **Verification-Oriented:** `"Let's work this out in a step by step way to be sure we have the right answer."` (Zhou et al., 2022b)
- **OPRO SOTA Inducer:** `"Take a deep breath and work on this problem step by step."` (Yang et al., 2023a)
- **Engineering Invariant Inducer:** `"Decompose this system into explicit state invariants. Reason step-by-step from preconditions to postconditions before writing any code."`

---

## 4. Critical Anti-Patterns & Engineering Traps

### 4.1 The Format Restriction Collision (JSON / Grammar Deadlock)
> [!CAUTION]
> **THE FATAL TRAP:** Combining `"Think step by step"` with `"Respond ONLY with a valid raw JSON object matching schema X: {...}"`.
>
> In an autoregressive model, the token decoder cannot output prose reasoning tokens prior to `{` without immediately triggering a JSON schema validation error. If the model is constrained by strict grammar sampling or JSON mode, the reasoning tokens are forcefully suppressed, collapsing the model back to direct zero-shot generation and reintroducing hallucinations!

#### The Engineering Solution: Decoupled Scratchpad Architecture
Always enforce a two-envelope scratchpad or embed the thought trajectory into the structured schema:

```markdown
<!-- PATTERN A: Two-Envelope Scratchpad -->
You MUST structure your response into two distinct envelopes:

<thought_scratchpad>
Execute full Step-Back / Tab-CoT / Thread-of-Thought reasoning here.
Explore trade-offs, state transitions, and edge cases with zero formatting restrictions.
</thought_scratchpad>

<final_payload>
```json
{
  "status": "success",
  "result": "..."
}
```
</final_payload>
```

```markdown
<!-- PATTERN B: Embedded Schema Reasoning Trace -->
Generate a single JSON object where the reasoning trajectory is an explicit first-class field:
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "step_back_principles": { "type": "array", "items": { "type": "string" } },
    "deductive_trace": { "type": "array", "items": { "type": "string" } },
    "contrastive_risks_checked": { "type": "array", "items": { "type": "string" } },
    "payload": { "type": "object" }
  },
  "required": ["step_back_principles", "deductive_trace", "payload"]
}
```

### 4.2 Premature Final Answer Locking
- **The Failure:** Emitting the conclusion or return value on Line 1, then attempting to justify it in subsequent lines.
- **The Fix:** Hard prompt invariant: `"Do NOT state the final conclusion, function body, or patch until the complete deduction is validated in the thought stream."`

### 4.3 Hallucinatory Derivation Cascades in Long CoT
- **The Failure:** An error in Step 2 passes unverified into Step 3, snowballing into an absurd hallucination by Step 8.
- **The Fix:** Verification-gated stepping: `"At each reasoning step, articulate the verification condition. If the condition fails, abort the branch and document the contradiction."`

### 4.4 Context Sinking (Noise Distraction)
- **The Failure:** Dumping 50,000 tokens of raw logs or multiple documentation files into the prompt, drowning the model's self-attention heads in irrelevant tokens.
- **The Fix:** Invoke **Thread-of-Thought (ThoT)** or execute an upstream extraction pass before invoking the reasoning chain.

---

## 5. Step-by-Step Prompt Transformation Workflow

When this skill is invoked with an intent or existing prompt, follow this 5-stage transformation pipeline:

```
[Raw User Prompt / Intent]
         │
         ▼
[Phase 1: Cognitive Demands Analysis]
  - Identify problem entropy, concurrency, noise ratio, state complexity.
         │
         ▼
[Phase 2: Topology Selection]
  - Map to: Step-Back | ThoT | Tab-CoT | Contrastive | Analogical.
         │
         ▼
[Phase 3: Scratchpad & Invariant Boundary Weave]
  - Decouple thought tokens from structural outputs (JSON/code).
         │
         ▼
[Phase 4: Golden / Contrastive Exemplar Injection]
  - Supply minimal orthogonal positive/negative pairs.
         │
         ▼
[Phase 5: Self-Consistency & Validation Harness]
  - Formulate tripwires, unit checks, and falsification gates.
```

### Phase 1: Cognitive Demands Analysis
Evaluate the task along 4 dimensions:
1. **Context Entropy:** Is the input noisy, scattered, or long? $\rightarrow$ Select **ThoT**.
2. **State Complexity:** Does the task involve state machines, schemas, or relational tables? $\rightarrow$ Select **Tab-CoT**.
3. **Domain Abstraction:** Is the problem prone to deceptive low-level details or edge-case traps? $\rightarrow$ Select **Step-Back**.
4. **Subtle Flaw Vulnerability:** Are there common, seductive bad solutions? $\rightarrow$ Select **Contrastive CoT**.

### Phase 2: Topology Selection & Composition
Topologies can be unified orthogonally. For example:
- **Step-Back + Tab-CoT:** Abstract high-level distributed invariants, then build a tabular transition matrix.
- **ThoT + Contrastive CoT:** Process chaotic log chunks incrementally, contrasting normal behavior against anomalous signatures.

### Phase 3: Construct the Scaffolding
Inject the cognitive directives, thought inducers, and decoupled scratchpads into the prompt.

### Phase 4: Enforce Format & Output Integrity
Ensure the model cannot violate grammar constraints while generating reasoning tokens.

---

## 6. Concrete Before / After Case Studies

### Case Study 1: Distributed Concurrency Race Condition

#### ❌ Before (Naive Prompt)
> "Write a TypeScript function to update a user's wallet balance after a purchase. Make sure it's thread-safe and doesn't allow double spending."

*Model Behavior:* Writes a naive SQL `UPDATE users SET balance = balance - 10 WHERE id = 1` wrapped in an async function. Completely misses database isolation levels, lock contention, idempotency keys, and read-modify-write race conditions.

#### ✅ After (Engineered with Step-Back + Contrastive CoT)
```markdown
# Role & Operational Standard
You are a Staff Infrastructure & Database Reliability Engineer. Implement the wallet debit transaction in TypeScript/PostgreSQL.

## Execution Directives

### Stage 1: Step-Back Abstraction (Domain Principles)
Before touching any code, answer:
1. What fundamental distributed systems and ACID isolation principles govern financial balance mutations?
2. What are the strict mathematical conditions under which a double-spend anomaly can manifest during concurrent requests?
3. State the three invariant rules that must hold true across network timeouts, retries, and concurrent workers.

### Stage 2: Contrastive Architectural Analysis
Examine two competing implementation patterns:
- **Flawed Pattern (The Common Bug):** An application-level read-modify-write (`SELECT balance` -> check in Node.js -> `UPDATE balance`). Explain the exact interleaving where two simultaneous $50 debits against a $60 balance both succeed.
- **Hardened Pattern (Atomic / Serialized):** Provide the atomic conditional update with strict idempotency keys (`UPDATE accounts SET balance = balance - :amount WHERE id = :id AND balance >= :amount RETURNING ...`).

### Stage 3: Concrete Implementation
Inside `<code_implementation>`, write the complete, production-hardened TypeScript function utilizing PostgreSQL transactions, explicit lock semantics (or atomic single-statement balance checks), and idempotency key deduplication.
```

---

### Case Study 2: Monolithic Legacy Refactor with Chaotic Context

#### ❌ Before (Naive Prompt)
> "Here are 15 files from our old auth system and 4 error logs from production. Refactor this to support OAuth2 without breaking legacy sessions."

*Model Behavior:* Model hallucinates missing functions, skips subtle edge cases buried in file 12, ignores the error logs entirely, and produces generic boilerplate.

#### ✅ After (Engineered with Thread-of-Thought / ThoT)
```markdown
# Mission: Legacy Auth Modernization & OAuth2 Integration

## Processing Protocol: Thread-of-Thought (ThoT)
Do NOT jump to code generation. Digest the codebase and error traces through sequential thread analysis:

### Phase 1: Segment-by-Segment Ingestion
Process the provided context in 4 discrete threads:
- **Thread 1 (Core Session State):** Ingest `SessionManager.ts`, `CookieHandler.ts`. Extract current session lifecycle, token invalidation rules, and TTL mechanics.
- **Thread 2 (Legacy Data Layer):** Ingest `userRepo.ts`, `authQueries.sql`. Extract the schema assumptions, foreign keys, and nullability constraints.
- **Thread 3 (Production Failure Analysis):** Ingest the 4 production error logs. Isolate timestamps, stack traces, and root causal patterns.
- **Thread 4 (OAuth2 Interface Seam):** Ingest the new provider requirements. Identify exact overlapping boundaries with the legacy session cookies.

### Phase 2: Running State Reconciler
For each thread, output a 3-bullet **Thread Synthesis**:
- Key Invariants Discovered
- Silent Failure Risks
- Unbroken Seams Required

### Phase 3: The Unified Migration Blueprint
Synthesize the 4 thread states into an atomic implementation plan, detailing backward compatibility with legacy sessions, zero-downtime migration steps, and automated regression tests.
```

---

### Case Study 3: Complex Multi-Constraint Database Migration

#### ❌ Before (Naive Prompt)
> "Convert this MySQL relational schema for orders, order_items, and shipments into a single DynamoDB single-table design."

*Model Behavior:* Generates a random partition key / sort key scheme that works for basic fetches but breaks GSI queries, results in hot partitions, and makes shipment tracking impossible.

#### ✅ After (Engineered with Tabular Chain-of-Thought / Tab-CoT)
```markdown
# Mission: DynamoDB Single-Table Design Transformation

## Reasoning Requirement: Tabular Chain-of-Thought (Tab-CoT)
Before generating AWS CDK or table definitions, you MUST construct the complete access pattern matrix using the Tab-CoT schema below.

### 1. Access Pattern & Key Design Deduction Matrix
Fill out every row for all required access patterns (Orders by Customer, Items by Order, Shipments by Status, Range Queries by Date):

| Access Pattern ID | Business Query / Operation | Target Entity | Primary Key (PK) | Sort Key (SK) | GSI-1 PK | GSI-1 SK | Projection Type | Overloaded Entity Type Filter |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| AP-01 | Get Order by ID | Order | `ORDER#<id>` | `METADATA` | `CUST#<id>` | `DATE#<iso>` | ALL | `Type = 'ORDER'` |
| AP-02 | Get All Items in Order | OrderItem | `ORDER#<id>` | `ITEM#<id>` | N/A | N/A | ALL | `Type = 'ITEM'` |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 2. Hot Partition & Scalability Verification Table
| Key Design | Max Velocity / Sec | Partition Key Cardinality | Throttling Risk | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| `ORDER#<id>` | High | High ($10^6+$ unique) | Low | Standard hash distribution |
| ... | ... | ... | ... | ... |

### 3. Concrete Infrastructure Definition
Only after the tables above are completely filled and mathematically sound, emit the AWS CDK TypeScript stack defining the DynamoDB table and Global Secondary Indexes.
```

---

## 7. How to Invoke & Apply This Skill

When working in Antigravity, use this skill to elevate any engineering prompt:

```bash
# General invocation
/prompt-thought-generation "Refactor payment service to handle webhooks asynchronously"

# Explicit topology specification
/prompt-thought-generation "Audit our distributed locking mechanism in Redis" --topology step-back

/prompt-thought-generation "Migrate checkout state machine to support split billing" --topology tab-cot

/prompt-thought-generation "Diagnose memory leak across 20 production logs" --topology thot

/prompt-thought-generation "Verify TypeScript generic conditional type inference" --topology contrastive
```

### Automatic Execution Steps
1. **Intent Extraction:** The agent parses the target query, identifying latent assumptions, failure modes, and required cognitive depth.
2. **Topology Synthesis:** The agent selects or combines the optimal thought-generation blueprints (Step-Back, ThoT, Tab-CoT, Contrastive CoT, Analogical).
3. **Scaffold Authoring:** The agent generates the complete, ready-to-run prompt with decoupled scratchpads, verification invariants, and anti-pattern guards.
4. **Execution or Hand-off:** The agent either executes the scaffolded prompt directly or saves it to `.agents/prompts/` for team and pipeline reuse.

---

## 8. Alignment with Unified Agentic Engineering OS

- **Phase 00 (Discovery Router):** Recommended by `ask-skills` whenever a user has an ambiguous, high-risk, or analytically demanding task.
- **Phase 01 (Alignment & Intent):** Pairs directly with `grill-with-duality` and `domain-modeling` to ensure mental models are sound before specification.
- **Phase 02 (Architecture & Specs):** Integrates with `design-centroidal-adr` to ensure ADRs are derived from first-principles abstraction (Step-Back) and trade-off matrices (Tab-CoT).
- **Phase 04 (Execution & Quality):** Provides the cognitive foundation for `piv-implement` and `tdd`, preventing hallucinated test implementations and premature refactorings.
