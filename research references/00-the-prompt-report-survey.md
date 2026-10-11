---
type: concept
title: "The Prompt Report: Systematic Survey of Prompt Engineering Techniques"
description: "Comprehensive synthesis of the foundational 82-page survey by Schulhoff et al. (2025), cataloging Figure 2.2 macro-taxonomy, 6 prompt families, and empirical failure modes."
tags: [prompt-engineering, survey, taxonomy, empirical-evaluation, benchmarks]
timestamp: 2026-10-11T12:00:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "https://arxiv.org/abs/2406.06608"
  - "https://learnprompting.org"
---

# The Prompt Report: Systematic Survey of Prompt Engineering

## 💡 Strategic Context & Theoretical Foundation
This treatise establishes the academic and empirical substrate for the **Scientific Prompt Engineering Suite** (`skills/01-prompt-engineering/`). It synthesizes the landmark 82-page survey:

> **"The Prompt Report: A Systematic Survey of Prompt Engineering Techniques"**  
> *Sander Schulhoff, Michael Ilie, Nishant Balepur, Konstantine Kahadze, Amanda Liu, Chenglei Si, Yinheng Li, Aayush Gupta, HyoJung Han, Sevastine Kane, Sukanya S. Sane, Joe Chen, Tongshuang Wu, Kenneth Li, & Philip Resnik (2025).*  
> **Citation:** arXiv:2406.06608v3 [cs.CL], 82 pages, 15 researchers across University of Maryland, OpenAI, Microsoft, and Carnegie Mellon.

---

## 1. The Macro-Taxonomy of Prompting (Figure 2.2)

Schulhoff et al. (2025) classify prompt engineering into six primary families that govern how autoregressive language models allocate attention, traverse solution graphs, and synthesize tokens:

```
                               ┌────────────────────────────────────────────────────────┐
                               │       THE PROMPT REPORT TAXONOMY (Figure 2.2)          │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
         ┌───────────────────┬─────────────────────┼─────────────────────┬───────────────────┐
         ▼                   ▼                     ▼                     ▼                   ▼
   1. Zero-Shot        2. Few-Shot         3. Thought Gen         4. Decomp           5. Ensembling
   • Attention (S2A)   • 6 Design Decs     • Step-Back            • Least-to-Most     • Self-Consistency
   • Expansion (RaR)   • Vote-K Medoids    • Thread-of-Thought    • DECOMP Tooling    • MoRE Experts
   • Re-Reading (RE2)  • AutoDiCoT Pairs   • Tabular-CoT          • Skeleton-of-Thgt  • Universal SC
   • Self-Ask Queries  • Distance Order    • Contrastive CoT      • Tree-of-Thoughts  • Meta-Reasoning
                                                                                             │
                                                           ┌─────────────────────────────────┘
                                                           ▼
                                                  6. Self-Criticism
                                                  • Chain-of-Verification (COVE)
                                                  • ReverseCoT Constraint Check
                                                  • Self-Calibration Scoring
                                                  • Factored Multi-Agent Debate
```

---

## 2. Core Family Deep Dives & Operational Primitives

### Family 1: Zero-Shot Prompting & Attention Steering (§2.2.1.3)
Zero-shot techniques condition the model without input-output demonstration pairs. The posterior distribution $P(Y \mid X)$ is governed entirely by instruction framing, persona priors, and attention allocation.
- **System 2 Attention (S2A; Weston et al., 2023):** Regenerates input text to remove distracting context and opinion bias prior to generating answers.
- **Re-Reading (RE2; Xu et al., 2023):** Appends a repeated invariant statement `Read the question again: <query>` immediately before execution to eliminate recency-attenuation in long contexts.
- **Rephrase and Respond (RaR; Deng et al., 2023):** Prompts the model to expand underspecified user queries before answering.
- **Self-Ask (Press et al., 2022):** Decomposes complex zero-shot questions into explicit sub-queries answered sequentially.

### Family 2: Few-Shot In-Context Learning (ICL) (§2.2.1)
Few-shot prompting conditions parametric behavior through demonstration pairs $\{(x_i, y_i)\}_{i=1}^k$.
- **The 6 Core Exemplar Decisions (§2.2.1.1):**
  1. *Exemplar Quantity:* Trade-off between context budget and in-context variance reduction ($k=2..5$).
  2. *Exemplar Ordering:* Demonstrations must be sorted in **Distance-Ascending Order** (least similar first; nearest neighbor adjacent to the test query) to prevent recency bias.
  3. *Label Distribution:* Enforce balanced, uniform distributions to avoid majority-class hallucinations.
  4. *Exemplar Quality:* Verified ground-truth labels; corrupted demonstrations degrade reasoning accuracy by up to 40%.
  5. *Format Consistency:* Consistent syntactic markers across demonstrations.
  6. *Similarity vs. Diversity:* Use Vote-K medoid active selection to maximize coverage over the input manifold.
- **AutoDiCoT Contrastive Demonstrations (§6.2.3.3):** Pair positive exemplars with explicit negative exemplars explaining *how NOT to reason*, neutralizing deceptive reasoning traps.

### Family 3: Thought Generation & Reasoning Allocation (§2.2.2)
Autoregressive transformers compute a fixed budget per emitted token. Direct answer generation forces commitment before traversing the latent solution space.
- **Computation Allocation Formula:**  
  $$P(Y \mid X) \longrightarrow P(T \mid X) \cdot P(Y \mid X, T)$$  
  Emitting intermediate trajectory $T = (t_1, t_2, \dots, t_k)$ shifts the conditional probability of final answer $Y$.
- **Step-Back Abstraction (Zheng et al., 2023):** Steps back from concrete instance variables to deduce high-level domain physics or principles first.
- **Thread-of-Thought (ThoT; Zhou et al., 2023):** Maintains structured, bounded conversational threads across noisy contexts.
- **Tabular Chain-of-Thought (Tab-CoT; Zhai et al., 2023):** Enforces tabular two-dimensional state transitions for multi-entity logic.

### Family 4: Decomposition Execution Graphs (§2.2.3)
Breaks high-entropy tasks into structured directed acyclic graphs (DAGs):
- **Least-to-Most Prompting (Zhou et al., 2022):** Bottom-up sub-problem sequencing where outputs of sub-task $i$ feed sub-task $i+1$.
- **Decomposed Prompting (DECOMP; Khot et al., 2022):** Hierarchical sub-task routing to specialized external tools, prompts, or subagents.
- **Skeleton-of-Thought (SoT; Ning et al., 2023):** Emits an answer outline first, then fans out parallel workers to write sub-sections simultaneously.

### Family 5: Ensembling & Multi-Path Consensus (§2.2.4 & §6.1.3)
Single-turn greedy decoding ($T=0$) suffers from local optima traps:
- **Self-Consistency (Wang et al., 2022):** Samples $k$ distinct reasoning trajectories at temperature $T=0.5$ and aggregates via majority vote or semantic clustering.
- **Mixture of Reasoning Experts (MoRE; Cabello et al., 2023):** Dispatches the same query to specialized reasoning personas (e.g. Architect, Security Auditor, Systems Engineer).
- **Universal Self-Consistency:** Synthesizes multi-path distributions into a unified, highest-likelihood consensus.

### Family 6: Self-Criticism & Verification Loops (§2.2.5)
Overcoming the intrinsic failure of models to self-correct within a single conversational turn:
- **The Intrinsic Correction Barrier (Huang et al., 2023):** Asking "Are you sure?" in-context induces sycophancy or apologies. True verification requires **factored independence**.
- **Chain-of-Verification (COVE; Dhuliawala et al., 2023):** Drafts baseline $\to$ plans independent verification queries $\to$ executes verification queries without seeing draft $\to$ synthesizes final verified output.
- **ReverseCoT:** Reconstructs the original problem constraints backward from the proposed answer to detect hallucinated premises.

---

## 3. The 4 Invariant Architecture Laws

1. **Format-Reasoning Decoupling Law (§2.5):** Never force JSON/schema output constraints in the same token generation pass as reasoning. Always decouple into `<thought_scratchpad>` followed by `<output_contract>`.
2. **Zero-Sycophancy Invariant (§5.2.2):** Prohibit leading or biased user prompts. Enforce neutral, symmetric framing across classification boundaries.
3. **Contrastive Curation Law (§6.2.3.3):** Every few-shot prompt must include at least one negative demonstration explaining *why* subtle edge-cases fail and *how* to correct them.
4. **Zero-Trust Tool & Boundary Hygiene (§5.1.1 & §5.1.2):** Wrap external user inputs in semantic XML delimiters (`<<<USER_INPUT>>>`) and whitelist allowed modules to prevent package hallucination.

---

## 4. The 7-Point Empirical Audit Checklist

| Checklist Item | Theoretical Section | Vulnerability Detected | Remediation |
|---|---|---|---|
| **1. Format-Reasoning Collision** | §2.5 | Reasoning degradation caused by simultaneous JSON syntax constraints. | Decouple scratchpad reasoning from final schema emission. |
| **2. Sycophancy & Presupposition** | §5.2.2 Footnote 12 | Agent confirms user's biased premise or leading question. | Rephrase to neutral symmetric framing. |
| **3. Exemplar Imbalance & Ordering** | §2.2.1.1 | Skewed labels or recency bias distorting predictions. | Enforce uniform class distribution and distance-ascending ordering. |
| **4. Delimiter Hygiene** | §5.2.1 | Fragile markdown or punctuation parsing ambiguity. | Wrap input, context, and instructions in strict XML tags (`<instructions>`, `<context>`). |
| **5. Context Attention Loss** | §2.2.1.3 RE2 | Degradation across long multi-turn contexts. | Inject trailing RE2 re-reading repetition anchor. |
| **6. Package Hallucination** | §5.1.2.2 | Generating imports for non-existent packages. | Explicitly whitelist authorized packages and libraries. |
| **7. Injection Boundary Leakage** | §5.1.1 | Direct string interpolation allowing prompt injection. | Isolate user inputs in semantic boundaries (`<<<USER_INPUT>>>`). |
