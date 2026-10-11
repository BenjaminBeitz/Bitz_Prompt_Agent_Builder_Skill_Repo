---
name: prompt-architect
description: Interactive Meta-Prompt Architect that grills you with 2-3 targeted diagnostic questions grounded in 'The Prompt Report' to determine, compose, and stress-test the optimal prompt system.
argument-hint: "<intent-or-raw-prompt> [--test]"
---

# PromptArchitect: Interactive Meta-Prompt Architect
*Grounded in 'The Prompt Report: A Systematic Survey of Prompt Engineering Techniques' (Schulhoff et al., 2025)*

`prompt-architect` is the interactive flagship prompt engineering skill for Google Antigravity (AGY). It takes any raw task, idea, or draft prompt and conducts a **disciplined, 2-3 question diagnostic grilling session** to identify the optimal prompt architecture from the 6 foundational families (Figure 2.2):
1. **`/prompt-zero-shot`**: Attention steering (S2A), perspective isolation (SimToM), question expansion (RaR), and re-reading (RE2).
2. **`/prompt-few-shot`**: 6 exemplar design decisions, Vote-K medoid selection, and AutoDiCoT contrastive negative examples.
3. **`/prompt-thought-generation`**: Cognitive pathway induction, Step-Back domain abstraction, Thread-of-Thought (ThoT), and Tabular-CoT.
4. **`/prompt-decomposition`**: Multi-stage execution graphs, Least-to-Most sequencing, Skeleton-of-Thought (SoT) parallel fan-out, and DECOMP.
5. **`/prompt-ensembling`**: Multi-persona consensus, Mixture of Reasoning Experts (MoRE), Self-Consistency (SC $T=0.5$), and Universal SC.
6. **`/prompt-self-criticism`**: Chain-of-Verification (COVE), ReverseCoT constraint reconstruction, Self-Calibration, and ChatEval debate.

---

## 🧭 The 4 Invariant Architecture Laws

1. **Format-Reasoning Decoupling Law (§2.5 & Tam/Kurt):** Never force rigid JSON/schema output constraints directly inside reasoning token generation. Always decouple into `<thought_scratchpad>` followed by `<output_contract>`.
2. **Zero-Sycophancy Invariant (§5.2.2 & Sharma et al.):** Refuse leading, biased, or opinion-confirming user premises. All classification prompts must use neutral, symmetric framing (Footnote 12).
3. **Contrastive Curation Law (§6.2.3.3 AutoDiCoT & Chia et al.):** Every few-shot prompt must include at least one contrastive negative demonstration explaining *why* a subtle edge-case fails and *how* to correct it.
4. **Zero-Trust Tool & Security Boundary (§5.1.2.2 & Lanyado et al.):** Whitelist authorized libraries to prevent package hallucination attacks; wrap external user inputs in semantic XML delimiters (`<<<USER_INPUT>>>`).

---

## 🔄 Interactive Execution Protocol

### Step 1: Contextual Diagnosis (The 2-3 Question Grill)
When invoked with an intent or raw prompt, scan the domain and immediately present **2-3 high-signal diagnostic questions** grounded in Figure 2.2:
- *Question 1 (Reasoning Topology):* Evaluate whether the problem involves multi-hop logic (triggers `prompt-thought-generation`), chaotic/long context (triggers `ThoT`), or hierarchical decomposition (triggers `prompt-decomposition`).
- *Question 2 (Exemplar Strategy):* Inquire whether real data exists or if synthetic demonstrations with AutoDiCoT contrastive pairs should be generated (`prompt-few-shot`).
- *Question 3 (Risk & Verification):* Assess whether high-stakes variance demands multi-agent consensus (`prompt-ensembling`) or independent verification queries (`prompt-self-criticism` COVE).

### Step 2: Exemplar Draft-and-Critique Probe (When Few-Shot is Selected)
If Few-Shot prompting is required:
1. Synthesize 2 positive exemplars and 1 AutoDiCoT contrastive negative pair immediately.
2. Present them to the user with a focused probe:
   - *"Does this negative exemplar accurately capture the subtle false-positive failure modes of your real-world domain?"*
   - *"Do the input attributes in demonstration #2 match the variance of your production data?"*
3. Refine exemplars based on user critique, applying **Distance-Ascending Ordering** (least similar first; nearest neighbor adjacent to query).

### Step 3: Synthesis & Verification Probe
Compile the prompt with strict XML Delimiter Hygiene (`<instructions>`, `<context>`, `<query>`, `<thought_scratchpad>`, `<output_contract>`) and trailing RE2 Re-Reading Anchors.
- If `--test` was passed, execute 1 live dry-run inference against the test probe to verify that the answer extractor parses cleanly.

### Step 4: Chat Delivery & Persistent Storage Prompt
Render the full prompt in the chat, and end with the mandatory save prompt:
```text
─────────────────────────────────────────────────────────────────────────────
💾 Would you like me to store this prompt in `.agents/prompts/<name>.md`?
Reply with your desired prompt name (e.g. 'sql_security_auditor') or 'skip'.
─────────────────────────────────────────────────────────────────────────────
```
When the user replies with a name, write the prompt to `.agents/prompts/<name>.md` using the **Full Prompt Specification Card** format.

---

## 📋 Full Prompt Specification Card Format (`.agents/prompts/<name>.md`)

```markdown
---
name: <prompt-name>
description: <One-line functional summary>
technique_topology: [e.g. Plan-and-Solve, Step-Back CoT, AutoDiCoT Few-Shot, ReverseCoT]
target_model: "gemini-2.0-pro | claude-3-5-sonnet | gpt-4o"
temperature: 0.2
answer_shape: "JSON Object | Enum | Free-form Markdown"
---

# Prompt: <prompt-name>

## Parameter Schema
- `{{INPUT}}`: [Description of user payload]
- `{{CONTEXT}}`: [Description of supplementary background]

## Production Prompt Template
<instructions>
  [Generic, task-aligned instructions per Ajith et al.]
</instructions>

<exemplars>
  [Ordered distance-ascending: broad examples first, contrastive negative penultimate, nearest neighbor last]
</exemplars>

<query_anchor>
  Re-read the core invariant before answering: [RE2 ANCHOR].
  Target Query: <<<{{INPUT}}>>>
</query_anchor>

<thought_scratchpad>
  [Deconstruct constraints and failure modes step-by-step]
</thought_scratchpad>

<output_contract>
  [Decoupled answer payload matching exact schema]
</output_contract>

## Answer Extractor & Verbalizer
- **Extractor Logic:** `regex: /<output_contract>([\s\S]*?)<\/output_contract>/`
- **Verbalizer Mapping:** `{"ACCEPTED": true, "REJECTED": false}`

## Regression Verification Test Probe
- **Test Input:** `[Deterministic test input]`
- **Expected Extracted Output:** `[Expected parsed JSON or Enum]`
- **Drift Tripwire:** If model output deviates from this expected payload on API update, re-run `/prompt-architect --test`.
```
