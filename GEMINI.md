# Global Rules — Bitz Prompt & Agent Builder Skill Suite

## 1. What This Is
The definitive Scientific Prompt Engineering and Autonomous Agent Engineering Suite for **Google Antigravity**, uniting:
- **Scientific Prompt Engineering Suite (10 Skills):** Operationalized from *The Prompt Report* (Schulhoff et al., 2025; arXiv:2406.06608) covering the full Figure 2.2 taxonomy.
- **Autonomous Agent Engineering Suite (3 Skills):** Grounded in the **Top 5 Foundational Standards** (Xi et al., CoALA, Anthropic, Oracle, Ng/Chase) and pioneering work by **Cole Medin** ([GitHub: @coleam00](https://github.com/coleam00)).

---

## 2. Architecture Map

```text
├── .git/
├── .gitignore                        # Python bytecode, OS artifacts, Antigravity scratch logs
├── README.md                         # Master guide: Cole Medin credit, Scientific Genesis, Mermaid DAG, User Guide, History
├── skills.json                       # Antigravity progressive disclosure manifest
├── GEMINI.md                         # Root global rules for Antigravity AI pairing
├── AGENTS.md                         # Root agent pointer (@GEMINI.md)
├── scripts/
│   ├── install-global.ps1            # Idempotent global installer to ~/.gemini/config/skills/ (-DryRun / -Force)
│   └── validate-skills.ps1           # Frontmatter & schema integrity validator
├── research references/              # Foundational Literature & Academic Treatises
│   ├── 00-the-prompt-report-survey.md         # The Prompt Report (Schulhoff et al. 2025, Fig 2.2 Taxonomy)
│   ├── 01-top-5-agent-specifications.md       # Comparative Survey of Top 5 Agent Specifications
│   ├── 02-cognitive-architecture-coala.md     # CoALA Memory Hierarchy & Action Space Decoupling
│   ├── 03-anthropic-workflows-vs-agents.md   # Anthropic Workflow vs Agent Boundaries & MCP Standard
│   ├── 04-oracle-agent-spec-protocol.md      # Declarative YAML Schemas & REST/SSE Agent Protocol
│   └── 05-systems-engineering-invariants.md  # Payload Armor (16KB), Memory Compaction & Git Rollback
└── skills/
    ├── 01-prompt-engineering/        # Scientific Prompt Engineering Suite (Schulhoff et al., 2025)
    │   ├── prompt-architect/
    │   ├── prompt-audit/
    │   ├── prompt-decomposition/
    │   ├── prompt-ensembling/
    │   ├── prompt-explainer/
    │   ├── prompt-few-shot/
    │   ├── prompt-generate/
    │   ├── prompt-self-criticism/
    │   ├── prompt-thought-generation/
    │   └── prompt-zero-shot/
    └── 02-agent-builder/             # Autonomous Agent Engineering Suite (Cole Medin, CoALA, Anthropic, Oracle)
        ├── opportunity-scan/         # [Cole Medin] Foundational AI-layer discovery & deployed agent retro engine
        ├── agent-opportunity-scan/   # [Benjamin Beitz] Upstream session & log mining for autonomous agentification
        └── build-agent/              # [Benjamin Beitz] Spec-driven operational agent & multi-agent compiler
```

---

## 3. Ground Rules & Non-Negotiable Invariants

1. **Skill File Structure:** Every skill must reside in its own folder containing a single `SKILL.md` with valid YAML frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: <High-signal 1-2 sentence trigger summary for progressive disclosure>
   argument-hint: "<optional: arguments description>"
   ---
   ```
2. **Format-Reasoning Decoupling Law (§2.5):** In prompt engineering, never force rigid JSON/schema output constraints directly inside reasoning token generation. Always decouple into `<thought_scratchpad>` followed by `<output_contract>`.
3. **Contrastive Curation Law (§6.2.3.3):** Every few-shot prompt must include at least one contrastive negative demonstration explaining *why* a subtle edge-case fails and *how* to correct it.
4. **Action Space Decoupling Law (CoALA §3):** In autonomous agent engineering, strictly separate *Internal Actions* (memory mutation, belief updates, self-notes) from *External Actions* (file mutations, shell execution, external APIs).
5. **Deterministic Blast Radius & Rollback:** Standalone agent harnesses must enforce non-interactive shell defaults, prohibit destructive commands (`rm -rf /`, `git push --force`), sanitize credentials, and take internal git checkpoints (`git stash create`) for automatic rollback on unrecoverable failures.
6. **Cross-Platform CLI Console Armor:** All Python helper scripts and test harnesses on Windows must enforce `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` and default to safe ASCII status indicators (`[OK]`, `[ERROR]`, `[INFO]`) to prevent `cp1252` charmap crashes.

---

## 4. Commands Agent Can Run

- **Validate Antigravity Skills Frontmatter:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/validate-skills.ps1
  ```
- **Test Global Installation (Dry-Run):**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/install-global.ps1 -DryRun
  ```
- **Install Globally Across Antigravity:**
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts/install-global.ps1 -Force
  ```
