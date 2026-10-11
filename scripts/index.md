---
type: index
title: "Automation & Validation Scripts: OKF Index"
description: "Master OKF v0.2 index for repository automation, installation, and verification scripts."
version: "1.0.0"
okf_version: "0.2"
status: active
timestamp: 2026-10-11T12:00:00Z
verified: true
verified_by: "@BenjaminBeitz"
---

# Automation & Validation Scripts: OKF Index

Welcome to the **Scripts Directory** for the **Bitz Prompt & Agent Builder Skills Suite**.

This folder contains cross-platform automation, installation, and deterministic validation scripts.

---

## 🧭 Scripts Catalog

| Script | Runtime | Description |
| :--- | :--- | :--- |
| [`install-global.ps1`](install-global.ps1) | PowerShell | Global skills installer for Windows/Antigravity. Supports `-DryRun` and `-Force`. Deploys skills to `$HOME/.gemini/config/skills`. |
| [`validate-skills.ps1`](validate-skills.ps1) | PowerShell | Validates YAML frontmatter integrity, required `name:`, and `description:` schemas across all 13 `SKILL.md` files. |
| [`validate-okf.py`](validate-okf.py) | Python 3 | Validates OKF v0.2 frontmatter schemas (`type:`, `title:`) and asserts 100% graph link resolution across all knowledge and index cards. |

---

## 🛠️ Usage Examples

```powershell
# Validate all 13 Antigravity skills
powershell -ExecutionPolicy Bypass -File scripts/validate-skills.ps1

# Validate OKF Knowledge Graph integrity
python scripts/validate-okf.py

# Perform dry-run installation
powershell -ExecutionPolicy Bypass -File scripts/install-global.ps1 -DryRun
```

---

## 🔗 Cross-Bundle Navigation

- 🏠 **Repository Root:** [../README.md](../README.md)
- 📚 **Foundational Literature:** [../research references/index.md](../research%20references/index.md)
- 🏛️ **Systems Architecture:** [../docs/architecture/index.md](../docs/architecture/index.md)
- 🛠️ **Engineering Skills Library:** [../skills/index.md](../skills/index.md)
