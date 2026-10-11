# Bitz's Prompt & Agent Builder Skills

The skills I actually use to engineer prompts and construct autonomous agents with coding agents. Straight out of my `.gemini/skills/` folder.

## What this is

A skill is a folder with a `SKILL.md` in it: a name, a description of when to use it, and the procedure the agent
should follow. Your agent loads the description at startup and pulls in the full skill only when the work matches.
That's the whole idea, and it's why skills scale where a 2,000-line system prompt doesn't.

These 13 skills form two interconnected suites:
1. **Scientific Prompt Engineering:** 10 skills directly operationalizing the Figure 2.2 taxonomy and empirical findings of *The Prompt Report: A Systematic Survey of Prompt Engineering Techniques* (Schulhoff et al., 2025; arXiv:2406.06608).
2. **Autonomous Agent Engineering:** 3 skills grounded in the Top 5 Foundational Agent Standards (Xi et al. 86pp survey, CoALA Cognitive Architecture, Anthropic "Building Effective Agents" & MCP, Oracle `agent-spec` / Agent Protocol, and Andrew Ng / Harrison Chase frameworks). Full academic syntheses of these papers are available in [`research references/`](research%20references/).

They're built around two core loops:
- **The Prompt Loop:** `raw intent → architect / generate → topological reasoning → self-criticism / audit`
- **The Agent Loop:** `session mining (opportunity scan) → draft spec → build agent → verify probe → deployed retro`

Nothing here is a framework. Each skill is a plain markdown file you can read in two minutes, disagree with, and
edit. That's the point: read them, take the ones that fit how you work, rewrite the rest.

## Bring them in

### As an Antigravity global installation (recommended for Google Antigravity)

Run the included PowerShell installer to install all 13 skills globally into your Antigravity config (`~/.gemini/config/skills/`):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-global.ps1 -Force
```

To preview what would be installed first without making changes, run with `-DryRun`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-global.ps1 -DryRun
```

### As editable files, in any agent

```bash
npx skills add BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo                             # everything
npx skills add BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo --list                      # see what's here first
npx skills add BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo --skill prompt-architect build-agent agent-opportunity-scan
```

Add `-g` to install globally (`~/.gemini/skills/` or `~/.claude/skills/`) instead of into the current project. This route writes real
files into your repo, so you can edit them, which is what I'd actually recommend once you know which ones you keep
reaching for.

### Or just clone and copy

They're only markdown files:

```bash
git clone https://github.com/BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo.git
cp -r Bitz_Prompt_Agent_Builder_Skill_Repo/skills/01-prompt-engineering/prompt-architect your-project/.gemini/skills/
```

### Or ask your agent

This works fine too:

> Clone https://github.com/BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo, look at the skills in `skills/`, and copy the ones
> that fit this project into my `.gemini/skills/` (or `.claude/skills/`) folder. Tell me which ones you picked and why.

For the last two, restart your session (or run `/skills`) and they'll show up.

## The skills

**Prompt Engineering: meta & diagnostics**

| Skill | What it does |
|---|---|
| `prompt-architect` | Diagnostic architect that grills you with 2–3 questions to determine and compose the optimal prompt topology |
| `prompt-generate` | Fast direct prompt compiler that skips diagnostic grilling and outputs production-grade prompt specs |
| `prompt-explainer` | Deconstructs any prompt into a pedagogical case study explaining token dynamics and empirical science |
| `prompt-audit` | Audits an existing prompt against the 7 empirical invariants from *The Prompt Report* (sycophancy, collisions, delimiters) |

**Prompt Engineering: core reasoning topologies**

| Skill | What it does |
|---|---|
| `prompt-zero-shot` | Transforms raw prompts into high-precision zero-shot prompts using S2A, RaR, and RE2 repetition anchors |
| `prompt-few-shot` | Optimizes the 6 exemplar design decisions, distance-ascending ordering, Vote-K, and AutoDiCoT negative pairs |
| `prompt-thought-generation` | Allocates reasoning token budgets using Step-Back abstraction, Thread-of-Thought (ThoT), and Tab-CoT |
| `prompt-decomposition` | Breaks complex tasks into structured execution graphs using Least-to-Most, DECOMP, and Skeleton-of-Thought |
| `prompt-ensembling` | Designs multi-prompt consensus pipelines, Mixture of Reasoning Experts (MoRE), and Self-Consistency ($T=0.5$) |
| `prompt-self-criticism` | Embeds self-correction, Chain-of-Verification (COVE), ReverseCoT, and multi-agent critique loops |

**Agent Engineering: workflow mining & spec-driven construction**

| Skill | What it does |
|---|---|
| `opportunity-scan` | [Cole Medin] Reads how you actually work and recommends what to encode next; audits deployed agent runs |
| `agent-opportunity-scan` | [Benjamin Beitz] Mines sessions to detect high-toil patterns suitable for autonomous agentification; outputs draft specs |
| `build-agent` | [Benjamin Beitz] Spec-driven engine transforming intents into subagents, standalone Python micro-harnesses, and ARI tests |

## Using these with other agents

Skills are just markdown. There is no tool-specific lock-in here, so all of this works anywhere a coding agent
can read files (Google Antigravity, Claude Code, Cursor, Codex, Windsurf, Cline, OpenCode, and Continue).

The `npx skills` CLI installs to 75+ agents into whatever directory each one expects:

```bash
npx skills add BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo -a antigravity
npx skills add BenjaminBeitz/Bitz_Prompt_Agent_Builder_Skill_Repo -a cursor -a claude-code
```

If your agent has no skills mechanism at all, the fallback is boring and effective: keep the folder in your repo
and point at it from `AGENTS.md` (or `GEMINI.md` / `CLAUDE.md`), telling the agent to read the matching `SKILL.md` before
starting that kind of work.

Two things to adjust when you port them:

- **Slash-command syntax.** Skills that reference each other by name assume your agent's slash-invocation. Elsewhere, say "use the prompt-architect skill" instead.
- **Tool names.** Native tool references like `view_file` or `run_command` match Antigravity conventions; other agents map them to their local read/shell primitives.

## Standing on the shoulders of giants: Credit to Cole Medin

The agent engineering side of this repository is deeply indebted to **Cole Medin** ([GitHub: @coleam00](https://github.com/coleam00)).

Cole's original **`opportunity-scan`** skill pioneered the concept of analyzing developer runs and command history to surface what to encode into the AI layer next. We loved that idea so much that we repurposed and retrofitted it into **`agent-opportunity-scan`**—shifting the focus specifically from passive AI-layer configuration (rules, hooks) to **active autonomous agentification** with a 4-filter qualification gate, 3 agent archetypes (`solo-tool-user`, `multi-agent-squad`, `autonomous-sentinel`), an Agent Viability Score (AVS) formula, and direct 1-click draft specs.

We have bundled Cole Medin's original `opportunity-scan` skill right inside [`skills/02-agent-builder/opportunity-scan/`](skills/02-agent-builder/opportunity-scan/) because it closes the lifecycle loop: once an agent is built and running in production, Cole's scan inspects its runtime artifacts and feeds directly back into `/build-agent --upgrade <agent-name>`.

## The story behind the skills (A brief history)

### Act 1: Escaping the prompt "vibe-coding" wilderness
Early prompt engineering felt like alchemy: tweaking adjectives, hoping models wouldn't hallucinate, and watching minor phrasing changes break fragile code outputs. Finding *The Prompt Report* (Schulhoff et al., 2025; arXiv:2406.06608) was a revelation. Spanning 82 pages and synthesizing hundreds of empirical studies, it proved that prompt engineering is an empirical science governed by transformer attention dynamics and token budget allocation. We codified its entire Figure 2.2 taxonomy into reusable Antigravity skills, replacing ad-hoc prompts with mathematically sound primitives like Format-Reasoning Decoupling, AutoDiCoT contrastive demonstrations, Vote-K medoid selection, and RE2 repetition anchors.

### Act 2: Hitting the agent production wall
As we moved from one-shot prompts to autonomous agent loops, we ran straight into the **Agent Production Wall**: infinite tool ping-pong loops, Windows `cp1252` encoding crashes when scripts printed emojis, unmonitored blast radiuses, and dirty git states when tasks aborted. It was clear that autonomous agents cannot just be system prompt templates; they must be **engineered systems**. That led to a deep dive into the top 5 agent standards: Zhiheng Xi et al.'s 86-page survey, the CoALA Cognitive Architecture (Sumers, Yao et al.), Anthropic's "Building Effective Agents", Oracle's declarative `agent-spec`, and Andrew Ng's core design patterns.

### Act 3: Cole Medin's spark and the 2-stage agent loop
Encountering Cole Medin's `opportunity-scan` provided the missing link: instead of guessing what agent to build, scan actual session logs to find real human toil. We retrofitted that insight into `agent-opportunity-scan` to qualify candidates and author draft specs, and built `build-agent` to construct complete operational systems—standalone zero-dependency Python micro-harnesses (`runner.py`) with CoALA action decoupling, 16KB payload armor, and git working-tree rollbacks. Bundling Cole's original scan as the post-run audit completed a self-healing loop.

### Act 4: Open sourcing the suite
Having tested and proven these 13 skills across hundreds of real-world coding sessions, we adopted Cole Medin's clean skills repository structure to package and share them with the open-source community.

## License

MIT, see [LICENSE](LICENSE). Take them, fork them, rewrite them.
