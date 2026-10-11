---
name: prompt-audit
description: Audits an existing prompt or prompt file against the empirical invariants and failure modes of 'The Prompt Report' (Schulhoff et al., 2025).
argument-hint: "<prompt-text-or-file-path>"
---

# PromptAudit: Empirical Prompt Inspector & Hardener
*Grounded in 'The Prompt Report' (Schulhoff et al., 2025)*

`prompt-audit` inspects any existing prompt, system prompt, or prompt file against the empirical failure modes identified in *The Prompt Report*. It identifies structural vulnerabilities and outputs an upgraded, hardened drop-in replacement.

---

## 🔍 The 7-Point Audit Checklist

Every audited prompt is evaluated against seven empirical criteria:

1. **Format-Reasoning Collision (§2.5):** Does the prompt force strict JSON/schema output constraints in the same generation pass as reasoning? (Flags cognitive degradation).
2. **Sycophancy & Leading Presuppositions (§5.2.2 Footnote 12):** Does the prompt ask leading questions (e.g. "Identify why this is bad", "Are you sure?") that induce sycophantic false positives?
3. **Exemplar Balance & Ordering (§2.2.1.1):**
   - Are few-shot labels skewed (violating uniform distribution)?
   - Are exemplars ordered arbitrarily rather than in distance-ascending sequence?
   - Is there at least one AutoDiCoT contrastive negative exemplar showing "how NOT to reason"?
4. **Delimiter Hygiene & Tokenization Sensitivity (§5.2.1):** Does the prompt rely on fragile syntax (colons, backticks) rather than unambiguous XML boundaries (`<instructions>`, `<context>`, `<query>`)?
5. **Attention Loss in Long Contexts (§2.2.1.3 RE2):** Does the prompt lack a trailing repetition anchor before the test query?
6. **Package Hallucination Vulnerabilities (§5.1.2.2):** If code generation is involved, does the prompt lack library whitelisting?
7. **Prompt Injection Boundary Isolation (§5.1.1):** Are external user inputs directly concatenated without enclosing semantic delimiters (`<<<USER_INPUT>>>`)?

---

## 📋 Audit Report Output Format

```markdown
### 1. Audit Scorecard
- **Overall Robustness Rating:** [CRITICAL VULNERABILITIES | DEFICIENT | PRODUCTION-READY]
- **Violations Detected:**
  - ⚠️ [Violation 1: Format-Reasoning Collision]
  - ⚠️ [Violation 2: Exemplar Recency Bias]

### 2. Failure Mode Breakdown
[Detailed explanation of the empirical risk citing specific sections from The Prompt Report]

### 3. Hardened Drop-in Replacement
[Complete, corrected prompt template with XML delimiters, decoupled scratchpads, and RE2 anchors]

### 4. Diff Summary
[Key changes made and the expected gain in accuracy, determinism, and security]
```

At the end of the audit report, `prompt-audit` will prompt:
```text
─────────────────────────────────────────────────────────────────────────────
💾 Would you like me to store this hardened prompt in `.agents/prompts/<name>.md`?
Reply with your desired prompt name or 'skip'.
─────────────────────────────────────────────────────────────────────────────
```
