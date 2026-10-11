---
name: prompt-self-criticism
description: Embeds self-correction, Chain-of-Verification (COVE), ReverseCoT, and multi-agent critique loops directly into prompts to eliminate hallucinations.
argument-hint: "<intent-or-draft-prompt> [--verification <cove|rcot|self-refine|calibration>]"
---

# Prompt Self-Criticism & Verification: Hallucination-Free Prompt Engineering

> **"Autoregressive generation without verification is an unconstrained forward drift. Once an LLM predicts an incorrect premise, sycophancy and context-conditioning force all subsequent reasoning to defend the error. True reliability requires decoupling generation from verification through structured self-criticism."**

This skill equips Google Antigravity agents and prompt engineers with state-of-the-art self-criticism, verification, and calibration architectures. Grounded directly in **The Prompt Report: A Systematic Survey of Prompting Techniques** (Schulhoff et al., 2025; Section 2.2.5 *Self-Criticism*, pages 15–16; Section 4.2 *Evaluation Methodologies*, pages 26–28), this guide provides plug-and-play verification loops, prompt templates, stopping condition formulas, two-axis quality gates, and anti-hallucination protocols.

---

## 1. Theoretical Foundation: The Self-Correction Dilemma

Empirical research in *The Prompt Report* (Schulhoff et al., 2025) and associated literature reveals critical dynamics regarding LLM self-criticism:

1. **The Intrinsic Correction Barrier:** Standard autoregressive models struggle to self-correct in an unguided, single-context conversation. When asked "Are you sure?", models frequently exhibit sycophancy, apologizing and altering correct answers or doubling down on hallucinations (Huang et al., 2023).
2. **Factored Independence is Mandatory:** Verification succeeds when the verification process is **factored** (decoupled from the baseline generation context). Inspecting a claim using independent probe prompts eliminates the confirmation bias inherent in evaluating a draft while viewing its generation trajectory.
3. **Reversibility as Ground Truth:** Forward reasoning can easily invent plausible justifications. Reconstructing original problem constraints backward from the solution (Reversing Chain-of-Thought) exposes hallucinations that forward generation conceals.
4. **Format Tax Decoupling:** Forcing a model to simultaneously compute complex reasoning and adhere to rigid syntactic formatting degrades reasoning fidelity. Verification must decouple semantic critique from schema formatting.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        Self-Criticism & Verification Taxonomy                          │
├────────────────────────────────┬───────────────────────────────┬───────────────────────┤
│ Verification Paradigm          │ Primary Academic Source       │ Primary Failure Mode  │
├────────────────────────────────┼───────────────────────────────┼───────────────────────┤
│ Chain-of-Verification (CoVe)   │ Dhuliawala et al. (2023)      │ Factual Hallucination │
│ Self-Calibration               │ Kadavath (2022), Tian (2023)  │ Overconfidence Drift  │
│ Self-Refine                    │ Madaan et al. (2023)          │ Quality / Style Flaws │
│ Reversing Chain-of-Thought     │ Xue et al. (2023)             │ Premise Fabrication   │
│ Self-Verification              │ Weng et al. (2022)            │ Constraint Violation  │
│ Cumulative Reasoning (CR)      │ Zhang et al. (2023b)          │ Complex Reasoning Loss│
│ Multi-Agent Debate (ChatEval)  │ Chan et al. (2024)            │ Evaluator Bias        │
│ G-EVAL & AutoCalibrate         │ Liu et al. (2023d, 2023h)     │ Subjective Drift      │
└────────────────────────────────┴───────────────────────────────┴───────────────────────┘
```

---

## 2. Verification Strategy Selector

Use this matrix to choose the optimal verification technique for your intent:

| Task Characteristics | Recommended Method | CLI Flag | Primary Mechanism |
| :--- | :--- | :--- | :--- |
| **Factual extraction, research synthesis, API reference** | **Chain-of-Verification (CoVe)** | `--verification cove` | Draft $\rightarrow$ Factor Probe Questions $\rightarrow$ Independent Query $\rightarrow$ Revision |
| **Algorithmic specs, boundary constraints, schema logic** | **Reversing Chain-of-Thought (RCoT)** | `--verification rcot` | Solution $\rightarrow$ Reconstruct Problem Constraints $\rightarrow$ Diff vs. Original Intent |
| **Mathematical proofs, deterministic calculations** | **Self-Verification** | `--verification self-verification` | Mask problem conditions $\rightarrow$ Predict parameters backwards from solution |
| **Code refactoring, prompt polish, document writing** | **Self-Refine** | `--verification self-refine` | Iterative Generate $\rightarrow$ Critique $\rightarrow$ Refine with quantitative stopping threshold |
| **High-stakes classification, safety screening, PR gating** | **Self-Calibration** | `--verification calibration` | Post-hoc confidence elicitation & calibrated rejection threshold $\tau$ |
| **Multi-step architectural deduction, theorem proving** | **Cumulative Reasoning** | `--verification cumulative` | Proposer $\rightarrow$ Verifier $\rightarrow$ DAG Proposition Accumulator $\rightarrow$ Reporter |
| **Contested PR reviews, design trade-offs, architecture ADRs**| **Multi-Agent Debate (ChatEval)** | `--verification debate` | Multi-persona adversarial cross-examination & synthesized consensus |
| **Automated PR/Ticket evaluation against complex rubrics** | **G-EVAL / AutoCalibrate** | `--verification geval` | Step-by-step CoT evaluation criteria + token probability weighting |

---

## 3. Deep-Dive Protocols & Operational Templates

### 3.1. Chain-of-Verification (CoVe - Dhuliawala et al., 2023)

CoVe operates across four discrete stages, explicitly separating draft generation from factual interrogation to prevent context contamination:

```
[Query X] ──> Step 1: Baseline Draft (Y0)
                     │
                     ▼
              Step 2: Verification Question Planning ({Q1, Q2, ... Qk})
                     │
                     ▼
              Step 3: Factored Verification Execution (Independent context for each Qi -> Ai)
                     │
                     ▼
              Step 4: Final Revision (Y* synthesized from X + Y0 + {Qi, Ai})
```

#### CoVe Operational Prompt Template

```markdown
You are a Chain-of-Verification (CoVe) Engine. Follow this exact 4-phase protocol.
Do NOT skip steps. Separate each phase using the designated XML tags.

<query>
{{USER_QUERY_OR_INTENT}}
</query>

<!-- PHASE 1: BASELINE GENERATION -->
<baseline_draft>
Generate an initial complete response to the query. State your assumptions clearly.
</baseline_draft>

<!-- PHASE 2: VERIFICATION PLANNING -->
<verification_plan>
Analyze the baseline draft. Identify every factual assertion, version dependency, API signature, external quote, and quantitative metric.
Generate 3 to 6 targeted, independent verification questions that directly probe the validity of these claims.
Rules for verification questions:
1. Questions must be atomic and self-contained (understandable without reading the baseline).
2. Questions must NOT leak the baseline's assumed answer (avoid leading questions).
3. Questions must focus on verifiable facts, constants, edge constraints, and invariants.
Format:
- Q1: [Specific probe]
- Q2: [Specific probe]
- Q3: [Specific probe]
</verification_plan>

<!-- PHASE 3: FACTORED VERIFICATION EXECUTION -->
<factored_verification>
For each question Q1..Qk, execute an isolated, objective verification inquiry. 
Answer each question purely based on verified knowledge, system constraints, or authoritative documentation.
Flag any discrepancy between the verified answer and the claim in the baseline draft.
Format:
- Q1: [Question]
  A1: [Verified Fact]
  Status: [CONFIRMED | CONTRADICTED | UNVERIFIABLE]
  Correction Needed: [None | Specific detail to update]
</factored_verification>

<!-- PHASE 4: FINAL REVISION -->
<final_revision>
Synthesize the final, verified response to the original query.
Incorporate every correction from Phase 3. Strip away hallucinated APIs, invalid assumptions, and unsupported claims.
Produce the clean, authoritative deliverable without internal debugging chatter.
</final_revision>
```

---

### 3.2. Reversing Chain-of-Thought (RCoT - Xue et al., 2023)

Forward generation often introduces unspoken, fabricated assumptions (e.g., assuming an API returns JSON when it returns binary, or assuming a synchronous database connection). RCoT enforces backward problem reconstruction: given the generated solution, what exact problem and constraints was this solution designed to satisfy?

```
[Original Problem P + Constraints C]
           │
           ▼
[Forward Generation] ──> [Solution S]
                           │
                           ▼
[Backward Reconstruction Prompt] ──> [Reconstructed Problem P' + Constraints C']
                                                   │
                                                   ▼
                                       [Semantic Diff: (P, C) vs (P', C')]
                                       - Discrepancy Found? => Hallucination Detected!
                                       - Match 100%?        => Verified Solution
```

#### RCoT Reconstruction Prompt Template

```markdown
### STEP 1: Candidate Solution Generation
Generate the complete solution or technical specification for the following requirements:
{{ORIGINAL_REQUIREMENTS}}

---

### STEP 2: Reversing Chain-of-Thought (Backward Reconstruction)
Forget the original prompt requirements. Examine ONLY the candidate solution produced in Step 1.
Act as an independent reverse-engineer and reconstruct:
1. What exact problem statement was this solution built to solve?
2. What implicit constraints, preconditions, and environmental invariants does this code/spec strictly assume?
3. What edge cases does this solution handle, and what failure modes does it ignore?

Output the reconstructed specification inside <reconstructed_spec>.

---

### STEP 3: Invariant Diff & Hallucination Audit
Compare the <reconstructed_spec> against the {{ORIGINAL_REQUIREMENTS}}:

| Requirement / Constraint | Original Spec (P) | Reconstructed Spec (P') | Parity Status | Failure Analysis |
| :--- | :--- | :--- | :--- | :--- |
| Core Objective | ... | ... | MATCH / DRIFT | ... |
| Invariants / Seams | ... | ... | MATCH / VIOLATED | ... |
| Unstated Assumptions | None allowed | ... | DETECTED / CLEAN | [Hallucinated premises] |

If ANY discrepancy, drift, or phantom assumption is identified:
- Mark VERDICT: REVISE
- Pinpoint the exact hallucinated line in the candidate solution.
- Issue corrected solution resolving the discrepancy.
```

---

### 3.3. Self-Verification (Weng et al., 2022)

Self-Verification executes a bidirectional consistency check by masking core input parameters from the problem and re-deriving them using the generated output:

```markdown
<self_verification_protocol>
1. Forward Pass:
   Given input parameters {P_1, P_2, ... P_n}, solve for target outcome Y.
   Record intermediate calculation steps in <forward_scratchpad>.

2. Masking Selection:
   Select a critical initial parameter P_k (e.g., timeout value, buffer size, rate limit, tax rate).
   Mask P_k from the prompt context: P_k := [MASKED].

3. Backward Derivation:
   Given known parameters {P \ P_k} AND the calculated outcome Y, formulate the inverse equation or logical deduction to calculate P_hat_k.
   Show explicit backward derivation in <backward_scratchpad>.

4. Consistency Predicate:
   Compare P_hat_k with the original ground-truth P_k:
   Condition: | P_hat_k - P_k | <= epsilon (or exact symbolic match).
   - If TRUE: Forward reasoning is verified.
   - If FALSE: State discrepancy, reject forward solution, and re-solve.
</self_verification_protocol>
```

---

### 3.4. Self-Refine (Madaan et al., 2023) with Quantitative Stopping Conditions

Self-Refine prevents endless circular editing by anchoring iterations to explicit multi-criteria scoring rubrics and a formal convergence formula.

#### Formal Stopping Condition Formula

$$\text{TERMINATE if } \begin{cases}
t \ge T_{\max} & \text{(Budget Exhaustion)} \\
\text{CriticalDefectCount}(t) = 0 \;\land\; \text{Score}(t) \ge \tau & \text{(Quality Target Satisfied)} \\
\Delta(\text{Critique}_t, \text{Critique}_{t-1}) \le \epsilon & \text{(Diminishing Returns / Plateau)} \\
\text{Hash}(\text{Draft}_t) \in \{\text{Hash}(\text{Draft}_0), \dots, \text{Hash}(\text{Draft}_{t-1})\} & \text{(Oscillation Trap Detected)}
\end{cases}$$

Where:
- $T_{\max} = 3$ (Default maximum refinement depth to prevent degenerate hallucination loops).
- $\tau = 0.92$ (Target normalized quality threshold).
- $\epsilon = 0.03$ (Delta threshold where incremental improvements no longer justify token expenditure).

#### Self-Refine Operational Prompt

```markdown
You are a Self-Refine Engine. You will iteratively generate, critique, and refine the artifact until the formal stopping condition is satisfied.

Current Iteration: {{ITERATION_INDEX}} / {{MAX_ITERATIONS}} (Default Max: 3)
Target Threshold: tau = 0.95 | Epsilon = 0.05

<current_draft>
{{CURRENT_DRAFT}}
</current_draft>

<aspect_based_critique>
Evaluate <current_draft> across these 4 orthogonal dimensions (0.0 to 1.0):
1. Spec Fidelity (F_spec): Does it meet all hard requirements without extraneous scope?
2. Architectural Seams (F_arch): Are interfaces deep, decoupled, and cleanly separated?
3. Robustness & Edge Cases (F_robust): Are errors, timeouts, and null states handled?
4. Conciseness & Clarity (F_clarity): Is it free of boilerplate, fluff, and redundant code?

Calculate Total Score:
Composite_Score = (0.35 * F_spec) + (0.30 * F_arch) + (0.25 * F_robust) + (0.10 * F_clarity)

Identify Specific Actionable Flaws:
- Flaw 1: [Location, description, concrete remedy]
- Flaw 2: [Location, description, concrete remedy]
Critical Defect Count: [Integer count of blocking issues]
</aspect_based_critique>

<stopping_condition_evaluation>
Previous Score: {{PREVIOUS_SCORE}}
Current Score: [Composite_Score]
Delta: | Current Score - Previous Score |

Check Termination Criteria:
- Critical Defect Count == 0 AND Current Score >= 0.95? [YES/NO]
- Delta <= 0.05 (Diminishing returns)? [YES/NO]
- Current Iteration >= 3? [YES/NO]

Verdict: [TERMINATE_AND_SHIP | PROCEED_TO_REFINE]
</stopping_condition_evaluation>

<!-- IF PROCEED_TO_REFINE: Provide Refined Draft in <refined_draft> addressing Flaws -->
```

---

### 3.5. Self-Calibration & Error Bounding (Kadavath et al., 2022; Tian et al., 2023)

LLMs exhibit overconfidence bias when stating answers in prose. Self-Calibration forces the model to evaluate its own epistemic uncertainty post-hoc, mapping confidence onto calibrated rejection gates.

```markdown
<calibration_evaluation>
Analyze the candidate response provided in <candidate_output>.
Evaluate your epistemic confidence (probabilistic likelihood that the answer is completely free of factual error, unsupported assumptions, or subtle hallucinations).

Score each dimension from 0.00 (Pure Guesswork) to 1.00 (Empirically Verifiable Certainty):
1. Factual Certainty: [0.00 - 1.00]
   - Rationale: (Are all libraries, function signatures, and version numbers verifiable?)
2. Boundary & Invariant Certainty: [0.00 - 1.00]
   - Rationale: (Are concurrency, edge cases, and failure modes fully accounted for?)
3. Ambiguity Resilience: [0.00 - 1.00]
   - Rationale: (Did the prompt contain underspecified requirements that were assumed rather than clarified?)

Calibrated Confidence Vector:
Confidence_Score = Min(Factual, Boundary, Ambiguity)

Calibrated Action Decision:
- If Confidence_Score >= 0.85: STATUS: VERIFIED_PROCEED
- If 0.65 <= Confidence_Score < 0.85: STATUS: WARN_AND_FLAG (Explicitly annotate uncertain assumptions with [UNCONFIRMED: Requires Test])
- If Confidence_Score < 0.65: STATUS: REJECT_AND_ESCALATE (Refuse silent generation; trigger Socratic grilling or external doc search)
</calibration_evaluation>
```

---

### 3.6. Cumulative Reasoning (CR - Zhang et al., 2023b)

Linear reasoning fails in deep technical problems because an error in step 2 silently poisons step 5. Cumulative Reasoning organizes reasoning into a **Directed Acyclic Graph (DAG)** of propositions, maintained by three specialized subagent roles:

```
                ┌─────────────────────────────────┐
                │          Current Query          │
                └────────────────┬────────────────┘
                                 │
                                 ▼
                   ┌───────────────────────────┐
                   │    Knowledge Graph DAG    │
                   │  G_0 = {Initial Premises} │
                   └─────────────┬─────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Cumulative Reasoning Loop                    │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 1. PROPOSER SUBAGENT                                    │   │
│   │ Proposes candidate proposition p_new based on G_t       │   │
│   └────────────────────────────┬────────────────────────────┘   │
│                                │                                │
│                                ▼                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 2. VERIFIER SUBAGENT                                    │   │
│   │ Rigorously validates logical deduction: G_t |= p_new    │   │
│   │ Output: [ACCEPTED | REJECTED]                           │   │
│   └────────────────────────────┬────────────────────────────┘   │
│                                │ (If Accepted)                  │
│                                ▼                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 3. GRAPH ACCUMULATOR                                    │   │
│   │ G_{t+1} = G_t U {p_new}                                 │   │
│   └────────────────────────────┬────────────────────────────┘   │
│                                │                                │
│                                ▼                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 4. REPORTER SUBAGENT                                    │   │
│   │ Checks: Is G_{t+1} sufficient to deduce final answer?   │   │
│   │ - NO  -> Next iteration                                 │   │
│   │ - YES -> Synthesize verified final solution             │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

#### Cumulative Reasoning Prompt Specification

```markdown
### ROLE 1: PROPOSER
Input: Goal: {{TARGET_GOAL}} | Established Premises: <dag_propositions>{{CURRENT_DAG}}</dag_propositions>
Task: Propose exactly ONE atomic, logical next proposition that brings us closer to the goal.
Rules:
- Do NOT skip steps or jump to the final conclusion.
- State dependencies explicitly: "Given P1 and P3, therefore P_new..."
Format:
<candidate_proposition>
ID: P_{{NEXT_ID}}
Dependencies: [List of prerequisite P_ids]
Statement: [Atomic logical deduction]
</candidate_proposition>

### ROLE 2: VERIFIER
Input: Established Premises: {{CURRENT_DAG}} | Candidate: <candidate_proposition>{{CANDIDATE}}</candidate_proposition>
Task: Stress-test whether <candidate_proposition> strictly and necessarily follows from its dependencies.
Checks:
1. Are all listed dependencies present in the established premises?
2. Is the logical deduction mathematically and structurally sound?
3. Are any unstated assumptions or hidden variables smuggled in?
Verdict: [ACCEPT to DAG | REJECT with Counterexample]

### ROLE 3: REPORTER
Input: Goal: {{TARGET_GOAL}} | Verified DAG: {{UPDATED_DAG}}
Task: Check whether the set of verified propositions forms an unbroken path from initial premises to the final goal.
If Path is Complete: Produce final validated synthesis.
If Incomplete: Return to Proposer with target missing link.
```

---

### 3.7. Multi-Agent Evaluator Debate (ChatEval - Chan et al., 2024)

Single-evaluator LLM-as-a-Judge suffers from position bias, egocentric favoritism, and verbosity bias. ChatEval deploys a multi-agent referee panel with orthogonal archetypes to cross-examine proposals:

```markdown
<multi_agent_evaluator_panel>
Artifact Under Review: {{ARTIFACT_OR_DIFF}}
Originating Specification: {{SPEC_OR_REQUIREMENTS}}

---
### AGENT 1: The Adversarial Shadow Auditor (Red Team)
Mission: Assume the implementation has a catastrophic silent flaw. Hunt for race conditions, state desynchronization, unhandled error boundaries, and security vulnerabilities.
Critique:
- Identified Vulnerabilities: [...]
- Exploitation Scenarios: [...]
- Severity: [CRITICAL | MAJOR | MINOR]

---
### AGENT 2: The Specification Fidelity Purist (Contract Auditor)
Mission: Verify 1:1 compliance with {{SPEC_OR_REQUIREMENTS}}. Zero tolerance for scope creep, missing edge cases, or altered method signatures.
Critique:
- Unmet Requirements: [...]
- Unauthorized Scope Creep: [...]
- Contract Adherence Score: [0-100%]

---
### AGENT 3: The Deep Module Architect (Standards & Ergonomics)
Mission: Enforce Matt Pocock & John Ousterhout deep module discipline. Check for interface simplicity vs. internal implementation hiding. Flag shallow classes and leaky abstractions.
Critique:
- Leaky Abstractions: [...]
- Complexity Score: [DEEP | ACCEPTABLE | SHALLOW / LEAKY]

---
### DELIBERATION & DEBATE (Round 2 Cross-Examination)
Each agent reviews the critiques of the other two:
- Does Agent 2 agree that Agent 1's vulnerability is a real blocker, or is it premature optimization?
- Does Agent 1 agree that Agent 3's abstraction recommendation preserves performance invariants?

---
### SYNTHESIZED TRIBUNAL VERDICT
Synthesizer summarizes the final ruling:
- Consensual Blockers (Must fix before commit): [...]
- Advisory Improvements (Post-MVP tickets): [...]
- Final Gate: [APPROVED | CHANGES_REQUIRED]
</multi_agent_evaluator_panel>
```

---

### 3.8. G-EVAL & Model-Generated Guidelines (Liu et al., 2023d, 2023h)

G-EVAL formalizes evaluation using Chain-of-Thought evaluation step construction followed by token-probability scoring:

```markdown
<geval_evaluation_protocol>
## Evaluation Task
Assess candidate implementation for: {{EVALUATION_TASK_DESCRIPTION}}

## Criteria Rubric (Model-Generated Guidelines - AutoCalibrate)
- Metric 1: Spec Fidelity (Weight: 40%) - Strict satisfaction of explicit functional acceptance criteria.
- Metric 2: Interface Invariance (Weight: 30%) - Preserves existing system boundaries and type safety.
- Metric 3: Error Resilience (Weight: 20%) - Graceful degradation and zero uncaught exceptions.
- Metric 4: Idiomatic Economy (Weight: 10%) - Minimal surface area, no redundant abstractions.

## Evaluation Chain-of-Thought (Step-by-Step Scoring Guide)
1. Read the specification and candidate implementation thoroughly.
2. For Metric 1, trace every user-specified requirement to its corresponding test or code line.
3. For Metric 2, inspect all modified exported signatures and external interfaces.
4. For Metric 3, simulate unexpected inputs, network timeouts, and null values.
5. For Metric 4, verify that no new external libraries or boilerplate layers were introduced unnecessarily.

## Step-by-Step Execution
<cot_evaluation_trace>
[Detailed analysis following steps 1 through 5]
</cot_evaluation_trace>

## Final Weighted Metric Scores (1 to 5 Scale)
- Spec Fidelity: [Score 1-5] (Justification: ...)
- Interface Invariance: [Score 1-5] (Justification: ...)
- Error Resilience: [Score 1-5] (Justification: ...)
- Idiomatic Economy: [Score 1-5] (Justification: ...)

Normalized Composite Score: [ (Metric1*0.4) + (Metric2*0.3) + (Metric3*0.2) + (Metric4*0.1) ] / 5.0
Passing Gate: >= 0.85 (4.25 / 5.0)
Verdict: [PASS | FAIL]
</geval_evaluation_protocol>
```

---

### 3.9. Formatting Decoupling & XML/JSON Schemas

To prevent cognitive degradation ("format tax") during deep reasoning, always decouple verification into two phases:

1. **Phase 1: Pure Epistemic Scratchpad (Free-form / XML semantic tags)**: The model explores hypotheses, generates verification questions, and checks constraints without worrying about schema formatting.
2. **Phase 2: Structured Projection (Strict Schema)**: The model formats the verified propositions into the target JSON/XML schema.

#### Standard Antigravity Verification Schema (JSON)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AntigravityVerificationArtifact",
  "type": "object",
  "required": [
    "verification_method",
    "baseline_summary",
    "verification_probes",
    "two_axis_audit",
    "calibration_score",
    "verdict",
    "final_output"
  ],
  "properties": {
    "verification_method": {
      "type": "string",
      "enum": ["cove", "rcot", "self_refine", "calibration", "cumulative", "multi_agent_debate", "geval"]
    },
    "baseline_summary": {
      "type": "string",
      "description": "Concise summary of initial candidate draft or hypothesis"
    },
    "verification_probes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["probe_question", "factored_answer", "status"],
        "properties": {
          "probe_question": { "type": "string" },
          "factored_answer": { "type": "string" },
          "status": { "type": "string", "enum": ["CONFIRMED", "CONTRADICTED", "MODIFIED"] }
        }
      }
    },
    "two_axis_audit": {
      "type": "object",
      "required": ["spec_fidelity", "standards_fidelity"],
      "properties": {
        "spec_fidelity": {
          "type": "object",
          "properties": {
            "score": { "type": "number", "minimum": 0, "maximum": 1 },
            "hallucinations_detected": { "type": "array", "items": { "type": "string" } }
          }
        },
        "standards_fidelity": {
          "type": "object",
          "properties": {
            "score": { "type": "number", "minimum": 0, "maximum": 1 },
            "code_smells_detected": { "type": "array", "items": { "type": "string" } }
          }
        }
      }
    },
    "calibration_score": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Post-hoc calibrated confidence vector"
    },
    "verdict": {
      "type": "string",
      "enum": ["APPROVED", "REVISE_REQUIRED", "REJECTED"]
    },
    "final_output": {
      "type": "string",
      "description": "Verified, hallucination-free output artifact"
    }
  }
}
```

---

## 4. Two-Axis Quality Review Gate

Every artifact verified using this skill must pass through the **Two-Axis Quality Review Gate** (Cole Medin & Matt Pocock unified framework):

```
                       Axis 2: Spec Fidelity
                               ▲
                               │  [B] Spec Compliant,
          [A] Elegant Code,    │      Architecturally Leaky
              Wrong Problem    │      (Tech Debt / Smells)
                               │
       ────────────────────────┼────────────────────────> Axis 1: Standards Fidelity
                               │
          [C] Total Failure    │  [D] THE TARGET:
              (Reject / Rerun) │      Spec Perfect +
                               │      Deep Module Clean Seams
                               │
```

### Axis 1: Standards Fidelity (Clean Code & Invariant Seams)
- **Fowler Code Smells:** No duplicated logic, long parameter lists, feature envy, or primitive obsession.
- **Deep Modules:** Simple interface, substantial implementation hiding behind the interface (Ousterhout discipline).
- **Type Safety & Compiler Invariants:** No bypasses (`any`, `@ts-ignore`, blind casts) without documented justification.
- **Error Boundaries:** Explicit handling of network partitions, invalid schemas, and unexpected inputs.

### Axis 2: Spec Fidelity (Contract & Intent Adherence)
- **Zero Hallucinated Features:** No phantom helper functions, unrequested options, or speculative abstractions.
- **Zero Omitted Requirements:** Every explicit requirement in the user's prompt or PRD is satisfied.
- **Contract Parity:** Method names, arguments, return signatures, and HTTP status codes match the specification exactly.

---

## 5. Before vs. After Case Studies

### Case Study 1: Architectural System Design with Hidden State Bug

#### The Flawed Before Prompt (Brittle & Open-Loop)
```markdown
Write a TypeScript Redis distributed lock utility with an automatic lease refresh loop.
```

**What Went Wrong:** The model generated an automatic renewal loop using `setInterval`, but completely hallucinated the atomicity of the release script and failed to handle lock expiration during an asynchronous execution pause (garbage collection pause / event loop stall). The code suffered from split-brain lock acquisition under concurrency.

#### The Transformed After Prompt (CoVe + RCoT Pipeline)

````markdown
You are an Antigravity Systems Engineer. Implement a TypeScript Redis distributed lock utility.
You must execute the following Chain-of-Verification (CoVe) and Reverse-CoT (RCoT) verification pipeline:

1. <baseline_draft>
   Draft the DistributedLock class implementing `acquire(ttlMs)` and `release()`.
</baseline_draft>

2. <verification_plan>
   Formulate 4 factored verification questions probing concurrency invariants:
   - Q1: What happens if the process experiences a 10-second GC pause while holding the lock?
   - Q2: Does the release operation use an atomic Lua script to verify lock ownership token identity before deletion?
   - Q3: If the lease refresh fails due to network partition, does the lock holder immediately abort execution or emit an expiry event?
   - Q4: Does the implementation use Redis redlock multi-node consensus or single-instance TTL?
</verification_plan>

3. <factored_verification>
   Independently answer Q1 through Q4 against the Redis Distributed Locks documentation and Martin Kleppmann's fencing token specifications.
   Record corrections needed in the baseline draft.
</factored_verification>

4. <rcot_audit>
   Examine the lock renewal mechanism in the baseline draft.
   Reverse-engineer: "What failure scenario does this refresh loop silently cause if an unhandled promise rejection occurs in the heartbeat?"
   Diff against safety invariants.
</rcot_audit>

5. <final_revision>
   Emit the production-grade, verified TypeScript module with atomic Lua release script, fencing tokens, and explicit heartbeat error handling.
</final_revision>
````

---

### Case Study 2: Critical Financial / Cryptographic Math Implementation

#### The Flawed Before Prompt (Brittle & Open-Loop)
```markdown
Write a Python function to calculate compound interest with monthly contributions and inflation adjustments.
```

**What Went Wrong:** The model used floating point numbers (`float`) causing IEEE-754 precision drift, incorrectly applied inflation adjustment at the beginning instead of the end of compounding periods, and produced off-by-one errors in contribution compounding.

#### The Transformed After Prompt (Self-Verification + Cumulative Reasoning)

````markdown
You are an Antigravity Financial Logic Engine. Implement compound interest calculation in Python.
You must execute the Self-Verification and Cumulative Reasoning (CR) protocol:

1. <dag_propositions>
   - P1: All currency calculations MUST use `decimal.Decimal` with explicit rounding modes (`ROUND_HALF_EVEN`). IEEE-754 floating point arithmetic is strictly prohibited.
   - P2: Monthly compounding requires effective monthly interest rate r_m = (1 + r_annual)^(1/12) - 1 for nominal vs effective conversions.
   - P3: Inflation adjustments must discount the real purchasing power at month t using discount factor D_t = (1 + r_inflation)^(-t/12).
</dag_propositions>

2. <backward_self_verification>
   Forward Pass:
   Compute total future real value for Principal = 10,000, Monthly Contribution = 500, Years = 1, Annual Rate = 12%, Inflation = 0%.
   
   Masking & Backward Derivation:
   Mask the initial Principal P. Using the computed final value, algebraically reverse the formula to solve for P_hat.
   Verify: Does P_hat == 10,000.00 to within 10^-6 precision?
   If discrepancy occurs, identify the calculation bug immediately.
</backward_self_verification>

3. <two_axis_audit>
   - Standards Fidelity: Are precision types preserved across all function arguments?
   - Spec Fidelity: Are edge cases (0% rate, negative inflation, 0 contribution) covered?
</two_axis_audit>

4. <final_deliverable>
   Output the fully verified Python module with type annotations, docstrings, and doctests.
</final_deliverable>
````

---

## 6. Antigravity Orchestration Patterns

When invoking this skill programmatically within Antigravity or dispatching to subagents, follow these integration patterns:

### Subagent Invocation with Factored Verification

To achieve true factored verification (zero context contamination), spawn a separate `research` or `self` subagent whose context does NOT include the candidate baseline draft:

```typescript
// Antigravity Subagent Invocation Pattern
// Step 1: Parent generates baseline draft
const baseline = generateDraft(prompt);

// Step 2: Parent extracts verification questions
const questions = extractVerificationProbes(baseline);

// Step 3: Spawn unprimed subagent for factored verification
const subagent = await invoke_subagent({
  TypeName: "research",
  Role: "Unbiased Fact Verifier",
  Prompt: `Answer the following verification questions objectively based on authoritative documentation. 
Do NOT assume any prior context:
${questions.join("\n")}`
});

// Step 4: Parent synthesizes final revision from baseline + subagent verified answers
```

---

## 7. Execution Checklist

When running `/prompt-self-criticism` or crafting self-verifying prompts:

- [ ] **Method Selected:** Chosen appropriate verification strategy matching the task risk profile (CoVe, RCoT, Self-Refine, etc.).
- [ ] **Factored Decoupling:** Probing questions are decoupled from the generation context to eliminate sycophantic confirmation bias.
- [ ] **Formal Stopping Condition:** Loop has explicit termination rules ($T_{\max} \le 3$, defect count = 0, delta $\le \epsilon$).
- [ ] **Format Decoupling:** Thinking/critique occurs in semantic tags before final syntactic JSON/code projection.
- [ ] **Two-Axis Gate:** Artifact evaluated across Standards Fidelity (clean seams) and Spec Fidelity (contract compliance).
- [ ] **Calibrated Confidence:** Calibrated vector score generated; rejection/escalation triggered if $\tau < 0.85$.
