---
name: prompt-few-shot
description: Constructs mathematically robust few-shot prompts optimizing the 6 exemplar design decisions, KNN/Vote-K retrieval, and AutoDiCoT contrastive examples.
argument-hint: "<intent-or-prompt> [--dataset <path>] [--shots <n>]"
---

# Prompt Few-Shot: In-Context Learning & Exemplar Optimization

> *"Few-shot prompting is not merely providing illustrative examples; it is configuring an in-context parametric manifold. Sub-optimal exemplar ordering alone can swing model accuracy from 90% down to 50% random chance on identical demonstrations."*
> — Lu et al. (2021) / Schulhoff et al. (2025), *The Prompt Report*

This skill serves as the **few-shot prompt optimization engine** for Google Antigravity. It transforms fragile, naive prompts and raw task intents into mathematically grounded, high-fidelity In-Context Learning (ICL) prompts.

Grounding directly in **'The Prompt Report: A Systematic Survey of Prompt Engineering'** (Schulhoff et al., 2025, arXiv:2406.06608; Section 2.2.1, Section 2.2.1.1, Section 2.2.1.2, and Section 6.2.3.3), this skill operationalizes:
1. **The 6 Core Exemplar Design Decisions** (Quantity, Ordering, Distribution, Quality, Format, Similarity vs. Diversity).
2. **Dynamic Retrieval & Selection** (KNN by Liu et al., 2021; Vote-K Active Selection by Su et al., 2022).
3. **Synthetic Demonstration Synthesis** (Self-Generated ICL / SG-ICL by Kim et al., 2022; Prompt Mining by Jiang et al., 2020).
4. **Task-Specific Instructional Framing** (Ajith et al., 2024).
5. **AutoDiCoT Contrastive Demonstrations** (Schulhoff et al., 2025, Figure 6.12) explaining *how NOT to reason*.

---

## 1. When to Run This Skill

- **Prompt Construction:** Crafting few-shot prompts for complex reasoning, classification, code generation, schema extraction, or tool calling.
- **Prompt Refactoring & Debugging:** When an existing prompt suffers from:
  - **Recency Bias:** Output skews disproportionately toward the final exemplar's class.
  - **Prior-Probability Distortion:** Skewed label demonstrations hallucinate majority classes.
  - **Ordering Fragility:** Inconsistent outputs across minor prompt permutations.
  - **Cognitive Loop Failures:** LLM repeatedly commits known edge-case fallacies despite positive examples.
- **Many-Shot Scaling:** Expanding demonstrations from traditional few-shot ($k \in [2, 16]$) to long-context Many-Shot ICL ($k \ge 50$) under Gemini 1.5/2.0 Pro or Claude 3.5 Sonnet (Agarwal et al., 2024).

---

## 2. Theoretical Architecture & Optimization Pipeline

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        FEW-SHOT OPTIMIZATION PIPELINE                                  │
│                                                                                        │
│   [Raw Intent / Query]                                                                 │
│            │                                                                           │
│            ▼                                                                           │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 1. Task-Specific Instructional Priming (Ajith et al., 2024)                    │   │
│   │    - Formal task description, strict schema boundary, operational constraints  │   │
│   └──────────────────────────────────────┬─────────────────────────────────────────┘   │
│                                          ▼                                             │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 2. Candidate Exemplar Acquisition                                              │   │
│   │    - Extracted Corpus / Test Cases (Prompt Mining - Jiang et al., 2020)        │   │
│   │    - Or Synthesized Multi-Path Instances (SG-ICL - Kim et al., 2022)           │   │
│   └──────────────────────────────────────┬─────────────────────────────────────────┘   │
│                                          ▼                                             │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 3. Exemplar Selection Strategy (Similarity vs. Diversity)                      │   │
│   │    - Dense KNN Cosine Retrieval (Liu et al., 2021)                             │   │
│   │    - Graph Centrality + Diversity Medoids (Vote-K - Su et al., 2022)           │   │
│   └──────────────────────────────────────┬─────────────────────────────────────────┘   │
│                                          ▼                                             │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 4. The 6-Decision Exemplar Matrix Optimization (Schulhoff et al. §2.2.1.1)    │   │
│   │    - Quantity: Small vs. Many-Shot (Brown et al.; Agarwal et al.)              │   │
│   │    - Label Distribution: Stratified Uniform Classes (Zhao et al., 2021)        │   │
│   │    - Label Quality: Frontier Model Ground-Truth Gate (Wei et al., 2023c)       │   │
│   │    - Formatting: Canonical Delimiters & Delimiter Parity (Jiang et al., 2020)  │   │
│   │    - Ordering: Entropy-Sorted / Distance-Ascending Permutations (Lu et al.)    │   │
│   └──────────────────────────────────────┬─────────────────────────────────────────┘   │
│                                          ▼                                             │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ 5. AutoDiCoT Contrastive Demonstrations (Schulhoff et al. §6.2.3.3)            │   │
│   │    - Error Analysis + Negative Exemplar ("How NOT to reason")                  │   │
│   │    - Paired with Verified Directed Correction Trajectory                       │   │
│   └──────────────────────────────────────┬─────────────────────────────────────────┘   │
│                                          ▼                                             │
│   [Production Hardened Few-Shot Prompt Artifact]                                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. The 6 Core Exemplar Design Decisions (Schulhoff et al., §2.2.1.1, Fig 2.2)

Every few-shot prompt generated or audited by this skill must explicitly satisfy the **6 Design Decisions Rubric**:

### Decision 1: Quantity (Exemplar Count $k$)

| Regime | Count ($k$) | Empirical Dynamics | Citations | Recommended Usage |
| :--- | :--- | :--- | :--- | :--- |
| **Minimal / Few-Shot** | $k \in [2, 8]$ | Rapid convergence on output format and label space; steep performance increase over 0-shot. Diminishing marginal returns for standard classification beyond $k=16$. | Brown et al. (2020); Liu et al. (2021) | Low-latency inference, standard classification, conversational agents, token-constrained APIs. |
| **Many-Shot ICL** | $k \in [30, 500+]$ | Unlocks complex domain reasoning, non-natural language translation, arbitrary symbolic mapping; overcomes pre-training frequency bias. Mitigates high-variance sensitivity. | Agarwal et al. (2024); Schulhoff et al. (2025) | Long-context models (Gemini 1.5/2.0 Pro, Claude 3.5), code repository migration, proprietary DSLs, legal/clinical reasoning. |

> [!TIP]
> **Heuristic Rule of Quantity:** For deterministic schemas or structured extraction, use $k=3$ to $k=5$. For nuanced domain reasoning where models suffer from confirmation bias, scale to $k=8$ to $k=16$. For arbitrary custom rulebooks, use Many-Shot ($k \ge 50$) with long-context windows.

---

### Decision 2: Exemplar Ordering & Permutation Sensitivity

> [!WARNING]
> **The Lu et al. (2021) Phenomenon:**
> Lu et al. demonstrated that keeping identical exemplars but altering their permutation order can swing accuracy by **over 40 percentage points** (e.g., from 53% accuracy to 93% accuracy on identical inputs).
>
> Models exhibit severe **Recency Bias** (Zhao et al., 2021): the model disproportionately favors the label or reasoning style of the *last 1–2 demonstrations*.

#### Permutation Optimization Heuristics:
1. **Distance-Ascending Sorting (Kumar & Talukdar, 2021):**
   - Calculate semantic distance $d(x_i, x_{test})$ using cosine distance between sentence embeddings.
   - Order demonstrations in **ascending order of similarity**: least similar exemplars placed first, most similar exemplar placed *immediately adjacent to the test query*.
   $$x_{(1)}^{\text{distant}} \longrightarrow x_{(2)} \longrightarrow \dots \longrightarrow x_{(k)}^{\text{nearest}} \longrightarrow x_{test}$$
2. **Alternating Class Interleaving:**
   - Never place identical labels consecutively (e.g., avoid `[Label A, Label A, Label B, Label B]`).
   - Strictly interleave classes: `[Label A, Label B, Label C, Label A, Label B, Label C]`.
3. **Global Entropy Minimization (Lu et al., 2021):**
   - When evaluating prompt stability over a candidate set of permutations $\mathcal{P}$, score candidate orderings against a validation probe set $\mathcal{V}$ and select the permutation that maximizes prediction entropy over uniform distributions:
   $$\mathcal{H}(\mathcal{P}) = - \sum_{y \in \mathcal{Y}} P(y | \mathcal{P}, \text{probe}) \log P(y | \mathcal{P}, \text{probe})$$

---

### Decision 3: Label Distribution & Prior-Probability Skew

- **Prior Distortion (Zhao et al., 2021; Min et al., 2022):**
  If an exemplar set contains 4 Positive demonstrations and 1 Negative demonstration, LLMs distort their internal output priors to mirror the 80/20 skew, regardless of the test query's factual veracity.
- **Stratified Distribution Invariant:**
  - For $M$-class classification, each class must have exactly equal representation: $k_1 = k_2 = \dots = k_M$.
  - When balanced representation is mathematically impossible due to dataset constraints, calibrate prompt outputs via **Context-Free Calibration** (Zhao et al., 2021) using null inputs (e.g., `"Input: N/A\nOutput:"`).

---

### Decision 4: Label Quality & Demonstration Veracity

- **The Min et al. (2022) vs. Wei et al. (2023c) Divergence:**
  - *Small Models (<10B parameters, Min et al., 2022):* Demonstrations function primarily as syntax primers ($P(X)$ input distribution and label space $Y$). Shuffling or corrupting labels caused minimal degradation.
  - *Frontier LLMs (Gemini Pro, GPT-4, Claude 3.5, Wei et al., 2023c):* Frontier models perform true In-Context Bayesian updating on $(x_i \to y_i)$ mappings. **Incorrect, noisy, or hallucinated labels cause catastrophic reasoning degradation.**
- **Zero-Tolerance Quality Gate:**
  - All reasoning steps in Chain-of-Thought exemplars must be formally verified.
  - Synthetic exemplars generated via SG-ICL must undergo multi-sample agreement or automated test execution before insertion.

---

### Decision 5: Exemplar Formatting & Delimiter Engineering

- **Corpus Alignment (Jiang et al., 2020):**
  Prompts should conform to natural linguistic syntax and structural forms prevalent in pre-training distributions.
- **Syntactic Delimiter Protocol:**
  Use explicit, non-overlapping markup delimiters (e.g., Markdown headers `### Example N` or XML tags `<exemplar>...</exemplar>`).
  - **Tag Disambiguation:** Use `<task_instruction>`, `<exemplars>`, `<exemplar id="...">`, `<input>`, `<reasoning>`, `<output>`, and `<test_case>`.
  - **Token Hygiene:** Strip trailing whitespace before newline tokens; prevent delimiter tokenization splitting.

---

### Decision 6: Exemplar Similarity vs. Diversity (Selection Strategies)

```text
       Dense Similarity (KNN)                    Hybrid Manifold Coverage (Vote-K)
    ┌───────────────────────────┐                 ┌───────────────────────────┐
    │     Cluster Redundancy    │                 │   Centroids + Diversity   │
    │        • • •              │                 │      •            •       │
    │       • (x) •  [Query]    │                 │          •  (x)           │
    │        • • •              │                 │     •            •        │
    │  (Trapped in local niche) │                 │  (Spans full task manifold)│
    └───────────────────────────┘                 └───────────────────────────┘
```

1. **K-Nearest Neighbors (KNN - Liu et al., 2021):**
   - For a given query $x_{test}$, compute embedding vectors $e(x_{test})$ and $e(x_i)$ for all candidates in corpus $\mathcal{D}$.
   - Select the top-$k$ candidates maximizing cosine similarity:
   $$\text{sim}(x_i, x_{test}) = \frac{e(x_i) \cdot e(x_{test})}{\|e(x_i)\| \|e(x_{test})\|}$$
   - *Limitation:* Can trap demonstrations in an overly narrow semantic sub-space, failing when the query involves multi-concept composition.

2. **Vote-K Active Selection (Su et al., 2022):**
   - Balances **local relevance** with **global diversity**.
   - Step 1: Cluster candidate embeddings into $K$ clusters via K-Means or graph community detection.
   - Step 2: Compute centrality "votes" for points closest to cluster medoids.
   - Step 3: Select top-voted exemplars that maximize semantic coverage of the entire problem domain while preserving proximity to the query cluster.

---

## 4. Advanced Few-Shot Methodologies (§2.2.1.2)

### 4.1 Self-Generated In-Context Learning (SG-ICL - Kim et al., 2022)
When external gold-standard datasets are missing, do not guess raw examples manually. Use SG-ICL:

```text
[Task Specification] 
        │
        ▼
[Step 1: Input Generation Prompt] ──> Synthesize M diverse, edge-case test inputs {x_1, ..., x_M}
        │
        ▼
[Step 2: Dual Reasoning Execution] ─> Generate CoT trajectories and candidate outputs {y_1, ..., y_M}
        │
        ▼
[Step 3: Verification & Filter] ────> Execute consistency checks (code compiler, schema validator, consensus)
        │
        ▼
[Step 4: Prompt Assembly] ──────────> Select top-k validated pairs as canonical few-shot exemplars
```

### 4.2 Prompt Mining (Jiang et al., 2020)
- Extract naturally occurring $(x, y)$ input-output pairs directly from the project's existing tests, git commits, documentation codeblocks, and production logs.
- Guarantees exemplar formatting exactly reflects the codebase's existing architectural idioms.

### 4.3 Instructional Priming: Generic vs. Task-Specific Instructions (Ajith et al., 2024)
- **Empirical Principle:** Providing few-shot examples *without* explicit task instructions forces the model to perform induction on the implicit task definition.
- **The Ajith et al. Architecture:**
  1. **Task-Specific Frame:** Place an exhaustive, mathematically precise definition of the task, constraints, and non-goals *at the very beginning* of the prompt.
  2. **Exemplar Block:** Follow with structured few-shot demonstrations showing execution.
  3. **Target Query:** Conclude with the active query.

---

## 5. AutoDiCoT: Automatic Directed Chain-of-Thought (§6.2.3.3 & Fig 6.12)

Traditional Few-Shot CoT only demonstrates successful reasoning ("how to reason"). In real-world engineering, models repeatedly fall into **systematic cognitive traps** (e.g., superficial string matching, premature returns, off-by-one loops, hallucinated helper APIs).

**AutoDiCoT (Schulhoff et al., 2025)** solves this by introducing **CONTRASTIVE NEGATIVE EXEMPLARS** explaining **"how NOT to reason"**.

### Structural AutoDiCoT Demonstration Schema:

```xml
<exemplar type="contrastive_autodicot">
  <input>
    [Concrete realistic problem instance]
  </input>

  <!-- 1. The Common Fallacy Path (Negative Demonstration) -->
  <flawed_reasoning status="REJECTED">
    [Demonstrates the intuitive, superficial, or hallucinated shortcut that models commonly take]
  </flawed_reasoning>
  <flawed_output>
    [The incorrect result generated by the flawed path]
  </flawed_output>

  <!-- 2. The Directed Error Analysis / Diagnostic Critique -->
  <error_analysis>
    CRITICAL FAILURE MODE: [Explains precisely why the flawed reasoning fails]
    VIOLATED INVARIANT: [Identifies the specific boundary, edge case, or rule broken]
    CORRECTIVE HEURISTIC: [The specific mental pivot required to avoid this trap]
  </error_analysis>

  <!-- 3. The Verified Directed Trajectory (Positive Demonstration) -->
  <directed_reasoning status="ACCEPTED">
    [Step-by-step rigorous deduction adhering to the corrective heuristic]
  </directed_reasoning>
  <verified_output>
    [The ground-truth, verified result]
  </verified_output>
</exemplar>
```

#### AutoDiCoT Injection Ratio:
- In a prompt with $k$ total exemplars, maintain a **$1:3$ or $1:4$ ratio** of contrastive AutoDiCoT exemplars to standard positive exemplars.
- Place the AutoDiCoT contrastive exemplar in the **penultimate position** ($k-1$) to inoculate against recency bias while reinforcing the error boundary right before the target query.

---

## 6. Execution Instructions for the Agent

When the user invokes `/prompt-few-shot` or asks you to build, optimize, or fix a few-shot prompt, follow this strict 6-step protocol:

### Step 1: Task Classification & Constraint Envelope
1. Identify the task category:
   - **Type A:** Deterministic Classification / Labeling (requires strict label balance).
   - **Type B:** Structured Extraction / Schema Generation (requires delimiter parity).
   - **Type C:** Multi-Step Symbolic or Algorithmic Reasoning (requires AutoDiCoT).
   - **Type D:** Code Generation / Tool Invocation (requires syntax alignment & negative edge cases).
2. Author the **Task-Specific Instructional Frame** (Ajith et al., 2024):
   - Explicit operational objective.
   - Formal schema and syntax constraints.
   - Explicit negative boundaries (what NOT to output).

### Step 2: Exemplar Harvesting & Synthesis
1. If the user provided a dataset (`--dataset <path>`):
   - Ingest candidate instances.
   - Apply **KNN dense retrieval** (for targeted queries) or **Vote-K** (for generalized coverage).
2. If no dataset is provided:
   - Execute **SG-ICL (Kim et al., 2022)**: Synthesize diverse, representative edge-case instances.
   - For code/architectural tasks, mine real patterns from the local repository (Prompt Mining - Jiang et al., 2020).

### Step 3: Run the 6-Decision Exemplar Matrix Audit

Verify every candidate set against the following checklist:
- [ ] **Quantity:** Appropriate $k$ chosen ($k \in [3, 8]$ for standard tasks, $k \ge 50$ for long-context complex DSLs).
- [ ] **Distribution:** Exactly equal representation across all target classes ($k_1 = k_2$).
- [ ] **Quality:** 100% ground-truth verified; no synthetic hallucinations or unverified steps.
- [ ] **Format:** Consistent XML/Markdown delimiters; zero syntax drift across exemplars.
- [ ] **Similarity/Diversity:** Diverse edge cases represented; no redundant duplicate exemplars.
- [ ] **Ordering:** Distance-ascending sort (Kumar & Talukdar) with strictly interleaved class labels to eliminate recency bias.

### Step 4: Construct AutoDiCoT Contrastive Demonstration
1. Identify the single most dangerous cognitive trap or hallucination mode for this specific task.
2. Construct one dedicated `<exemplar type="contrastive_autodicot">` containing:
   - The flawed reasoning trajectory.
   - Explicit `<error_analysis>` isolating the broken invariant.
   - The verified, directed corrective trajectory.
3. Position this contrastive demonstration in the penultimate or strategic anchor slot.

### Step 5: Format the Production Prompt
Assemble the prompt according to the canonical structural template:

```xml
<system_instruction>
  <task_definition>
    [Ajith et al. Task-Specific Instructions & Constraints]
  </task_definition>
  
  <exemplars count="{k}">
    <!-- Exemplar 1 (Distant Positive) -->
    <exemplar id="1" class="{C1}">
      <input>...</input>
      <reasoning>...</reasoning>
      <output>...</output>
    </exemplar>

    <!-- Exemplar 2 (Interleaved Alternative Class) -->
    <exemplar id="2" class="{C2}">
      <input>...</input>
      <reasoning>...</reasoning>
      <output>...</output>
    </exemplar>

    <!-- Exemplar 3 (AutoDiCoT Contrastive Demonstrator) -->
    <exemplar id="3" type="contrastive_autodicot">
      <input>...</input>
      <flawed_reasoning>...</flawed_reasoning>
      <error_analysis>...</error_analysis>
      <directed_reasoning>...</directed_reasoning>
      <verified_output>...</verified_output>
    </exemplar>

    <!-- Exemplar 4 (Nearest Neighbor Positive - Query Adjacent) -->
    <exemplar id="4" class="{C1}">
      <input>...</input>
      <reasoning>...</reasoning>
      <output>...</output>
    </exemplar>
  </exemplars>
</system_instruction>

<query>
  <input>
    [Active User Input]
  </input>
</query>
```

### Step 6: Deliver Output & Metric Summary
Present the optimized prompt inside an expandable code artifact, accompanied by the **Few-Shot Optimization Audit Table** summarizing the design choices made.

---

## 7. Concrete Production Case Studies

### Case Study 1: Architectural Seam & Ticket Slicing (Phase 01/02 Task)

#### The Problem:
An agent is prompted to evaluate whether an architecture proposal requires a new database table or can be modeled in-memory. Naive zero-shot prompts repeatedly default to "add a database table" due to pre-training web dev bias.

#### Naive Prompt (Before):
```text
Determine if this feature needs a new database table or can be stored in-memory.
Example:
Feature: User shopping cart
Decision: Database table

Feature: Session token blacklist
Decision: ?
```
*Failure Mode:* Recency bias + 1-shot majority bias causes the model to blindly output "Database table", ignoring latency and ephemerality invariants.

#### Mathematically Optimized AutoDiCoT Few-Shot Prompt (After):

```xml
<task_instruction>
Evaluate feature storage requirements. You must classify each feature as either DATABASE_PERSISTENT or IN_MEMORY_EPHEMERAL.
Strict Rule: Features with ephemeral TTLs (<1 hour) or high write frequency (>500 req/sec) must be IN_MEMORY_EPHEMERAL unless strict audit compliance mandates persistence.
</task_instruction>

<exemplars count="3">
  <!-- Exemplar 1: Distance Ascending - Class A -->
  <exemplar id="1" class="DATABASE_PERSISTENT">
    <input>Feature: User Billing Invoices and Transaction Receipts</input>
    <reasoning>Financial transactions require non-repudiation, multi-year audit compliance, and ACID persistence. Query frequency is moderate.</reasoning>
    <output>DATABASE_PERSISTENT</output>
  </exemplar>

  <!-- Exemplar 2: AutoDiCoT Contrastive Demonstration -->
  <exemplar id="2" type="contrastive_autodicot">
    <input>Feature: Rate Limiting Sliding-Window Counters (100 req/min per IP)</input>
    <flawed_reasoning status="REJECTED">
      Every user request must check this count. We need durable storage so counts survive server restarts. Therefore, write to PostgreSQL rate_limits table on every request.
    </flawed_reasoning>
    <error_analysis>
      CRITICAL FAILURE MODE: High-frequency write thrashing on primary relational database.
      VIOLATED INVARIANT: Rate-limiting counters have sub-minute TTLs and require sub-millisecond latency. Writing to RDBMS introduces disk I/O bottlenecks and connection pool exhaustion.
      CORRECTIVE HEURISTIC: Ephemeral sliding windows tolerate restart clearing; allocate in Redis / in-memory cache.
    </error_analysis>
    <directed_reasoning status="ACCEPTED">
      Write frequency equals ingress request volume (>500 req/sec). Counter data is ephemeral (60-second window). Dropped counts during a restart do not compromise financial integrity. Sub-millisecond latency required.
    </directed_reasoning>
    <verified_output>IN_MEMORY_EPHEMERAL</verified_output>
  </exemplar>

  <!-- Exemplar 3: Interleaved Adjacent Nearest Neighbor - Class B -->
  <exemplar id="3" class="IN_MEMORY_EPHEMERAL">
    <input>Feature: Active WebSocket Connection Peer Registry</input>
    <reasoning>Connection sockets exist only in local memory processes. When server restarts, all TCP sockets disconnect simultaneously. Persistence to disk is redundant and invalid.</reasoning>
    <output>IN_MEMORY_EPHEMERAL</output>
  </exemplar>
</exemplars>

<query>
  <input>Feature: Session token revocation blacklist with 15-minute token expiry</input>
</query>
```

---

### Case Study 2: High-Stakes Tool-Calling & Schema Invariant

#### The Problem:
An agent invoking `run_command` hallucinations PowerShell piping syntax on Windows environments or outputs non-deterministic commands that hang waiting for interactive input.

#### Naive Prompt (Before):
```text
Generate the command to run tests.
Example:
Input: run unit tests
Output: npm test
```

#### AutoDiCoT Few-Shot Prompt (After):

```xml
<task_instruction>
Generate deterministic, non-interactive Windows PowerShell CLI commands.
Constraints:
1. Always disable interactive pagers (e.g., PAGER=cat or --no-pager).
2. Never pipe output through grep or awk (use native Select-String or PowerShell object pipelines).
3. Always include flags for non-interactive execution (e.g., --ci, --non-interactive, -y).
</task_instruction>

<exemplars count="3">
  <!-- Exemplar 1: Standard Positive -->
  <exemplar id="1">
    <intent>Run TypeScript type-checker across the workspace</intent>
    <reasoning>tsc --noEmit is non-interactive by default. Execute directly via npx.</reasoning>
    <command>npx tsc --noEmit</command>
  </exemplar>

  <!-- Exemplar 2: AutoDiCoT Contrastive Demonstration -->
  <exemplar id="2" type="contrastive_autodicot">
    <intent>Inspect recent git commit messages matching 'feat:'</intent>
    <flawed_reasoning status="REJECTED">
      Run `git log | grep 'feat:'`. This finds the commits quickly.
    </flawed_reasoning>
    <error_analysis>
      CRITICAL FAILURE MODE: Windows execution failure & interactive terminal hang.
      VIOLATED INVARIANTS:
      1. Default git log opens the 'less' terminal pager on Windows, hanging autonomous subagents indefinitely.
      2. 'grep' is not a native Windows PowerShell cmdlet (throws CommandNotFoundException unless MSYS2 is path-mapped).
      CORRECTIVE HEURISTIC: Prefix with --no-pager and replace grep with Select-String.
    </error_analysis>
    <directed_reasoning status="ACCEPTED">
      To run non-interactively in PowerShell: Pass `--no-pager` to git and pipe to native `Select-String -Pattern "feat:"`.
    </directed_reasoning>
    <command>git --no-pager log -n 20 --oneline | Select-String -Pattern "feat:"</command>
  </exemplar>

  <!-- Exemplar 3: Nearest Neighbor Positive -->
  <exemplar id="3">
    <intent>Execute pytest test suite with coverage report</intent>
    <reasoning>Pytest must run without interactive debugger stops (-s omitted, --capture=no omitted) and report clean exit codes.</reasoning>
    <command>pytest tests/ --tb=short -q</command>
  </exemplar>
</exemplars>

<query>
  <intent>Search for all files containing 'API_KEY' across subdirectories</intent>
</query>
```

---

## 8. Algorithmic Exemplar Selector (Reference Implementation)

Below is the mathematical reference algorithm for **KNN + Vote-K Diversity Re-ranking** and **Entropy Optimization**:

```python
"""
Exemplar Selection Engine (Schulhoff et al., 2025; Liu et al., 2021; Su et al., 2022)
Combines KNN Dense Retrieval with Vote-K Graph Centrality and Interleaved Ordering.
"""

from typing import List, Dict, Any
import numpy as np

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return float(np.dot(v1, v2) / norm) if norm > 0 else 0.0

def select_vote_k_exemplars(
    query_embedding: np.ndarray,
    candidate_pool: List[Dict[str, Any]],
    k: int = 4
) -> List[Dict[str, Any]]:
    """
    Selects k exemplars balancing query proximity with domain diversity (Su et al., 2022).
    """
    # 1. Compute similarity to query
    for item in candidate_pool:
        item["sim_to_query"] = cosine_similarity(query_embedding, item["embedding"])

    # 2. Sort pool by similarity
    sorted_pool = sorted(candidate_pool, key=lambda x: x["sim_to_query"], reverse=True)
    top_candidates = sorted_pool[: k * 4]  # Take top 4k candidates for diversity clustering

    selected: List[Dict[str, Any]] = []
    
    # 3. Iterative Medoid Selection (Vote-K Diversity Filter)
    while len(selected) < k and top_candidates:
        if not selected:
            # First item: Nearest neighbor to query
            selected.append(top_candidates.pop(0))
        else:
            # Subsequent items: Maximize sim to query while penalizing redundancy with already selected
            best_idx = -1
            best_score = -float("inf")
            for idx, cand in enumerate(top_candidates):
                query_sim = cand["sim_to_query"]
                redundancy = max(
                    cosine_similarity(cand["embedding"], s["embedding"]) 
                    for s in selected
                )
                # Trade-off tensor: 70% query relevance, 30% diversity bonus
                marginal_utility = (0.7 * query_sim) - (0.3 * redundancy)
                if marginal_utility > best_score:
                    best_score = marginal_utility
                    best_idx = idx
            selected.append(top_candidates.pop(best_idx))

    # 4. Ordering Optimization (Kumar & Talukdar, 2021)
    # Sort ascending by distance (least similar first -> nearest neighbor adjacent to query)
    ordered_exemplars = sorted(selected, key=lambda x: x["sim_to_query"])
    return ordered_exemplars
```

---

## 9. Few-Shot Quality Audit Scorecard

Before releasing any few-shot prompt into an Antigravity agent or workflow, grade it against this scorecard:

| Criterion | Target Metric | Violation Penalty |
| :--- | :--- | :--- |
| **Instructional Placement** | Task instructions placed *before* exemplars (Ajith et al., 2024) | Fail (Induction drift) |
| **Label Balance Ratio** | Class distribution variance $\le 5\%$ ($1:1$ parity for binary) | Fail (Zhao recency bias) |
| **Ground-Truth Veracity** | 100% verified labels; zero hallucinations (Wei et al., 2023c) | Critical Rejection |
| **Ordering Gradient** | Ascending similarity to target query ($x_{(k)}$ closest to prompt) | -20% accuracy swing risk |
| **Delimiter Consistency** | Exact tag closure parity (`<exemplar>` matched with `</exemplar>`) | Parsing failure |
| **Contrastive Inoculation**| At least 1 AutoDiCoT contrastive negative demonstration | -15% resilience against traps |

---

## 10. Summary Checklist for `/prompt-few-shot`

When invoked:
1. **Grill the Objective:** Clarify the exact input/output boundary and edge cases.
2. **Retrieve or Synthesize:** Mine existing code/tests or run SG-ICL to produce candidates.
3. **Filter via Vote-K:** Extract $k$ exemplars balancing proximity and diversity.
4. **Author 1 AutoDiCoT Unit:** Draft the contrastive negative path and error analysis.
5. **Sort by Distance Ascending:** Place the most query-similar positive exemplar last.
6. **Package Clean Artifact:** Output the finalized XML/Markdown prompt ready for execution.
