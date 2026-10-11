---
name: prompt-generate
description: Fast, direct prompt generator that skips diagnostic grilling and immediately compiles a production-grade prompt across the 6 prompt families.
argument-hint: "<intent-or-task> [--topology <zero-shot|few-shot|thought-gen|decomp|ensembling|self-criticism>] [--test]"
---

# PromptGenerate: Fast Direct Prompt Compiler
*Grounded in 'The Prompt Report' (Schulhoff et al., 2025)*

`prompt-generate` is the direct-compilation sibling of `/prompt-architect`. Use this command when you already know your requirements and want an immediate, hardened prompt specification without undergoing an interactive 2–3 question grilling session.

---

## ⚡ Direct Compilation Pipeline

1. **Topology Inference:** Instantly maps your input request to the optimal combination among the 6 core prompt skills (`prompt-zero-shot`, `prompt-few-shot`, `prompt-thought-generation`, `prompt-decomposition`, `prompt-ensembling`, `prompt-self-criticism`).
2. **Empirical Hardening:** Automatically injects:
   - **Format-Reasoning Decoupling:** Separates `<thought_scratchpad>` from `<output_contract>`.
   - **Sclar Delimiter Hygiene:** Standardizes on canonical XML boundary tags.
   - **RE2 Re-Reading Anchor:** Appends a trailing invariant repetition anchor before the query.
   - **Neutral Symmetric Phrasing:** Strips leading bias and sycophantic assumptions.
   - **Zero-Trust Tool Constraints:** Whitelists libraries if code generation or terminal commands are involved.
3. **Delivery:** Outputs the complete prompt specification card in chat.
4. **Save Prompt:** Prompts you at the end:
   ```text
   ─────────────────────────────────────────────────────────────────────────────
   💾 Would you like me to store this prompt in `.agents/prompts/<name>.md`?
   Reply with your desired prompt name (e.g. 'code_refactor_gate') or 'skip'.
   ─────────────────────────────────────────────────────────────────────────────
   ```

---

## 🛠️ Usage Examples

```bash
# Generate a zero-shot code review prompt with S2A and RE2
/prompt-generate "Review git diffs for memory leaks and race conditions in Rust"

# Generate a few-shot SQL classification prompt with AutoDiCoT
/prompt-generate "Classify user queries as read-only vs mutating SQL" --topology few-shot

# Generate and run a verification dry-run
/prompt-generate "Extract ISO 8601 dates from messy support tickets" --test
```
