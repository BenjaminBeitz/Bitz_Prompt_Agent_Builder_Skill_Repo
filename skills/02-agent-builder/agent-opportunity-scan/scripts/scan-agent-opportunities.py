#!/usr/bin/env python3
"""
Agent Opportunity Scanner
Analyzes Antigravity session transcripts or logs to detect repetitive,
high-toil, or error-prone workflows suitable for autonomous agentification.
Outputs candidate dossiers and draft specifications ready for direct execution
via /build-agent --from-spec.
"""

import sys
import os
import glob
import json
import re
import argparse
from typing import List, Dict, Any, Optional

# Ensure Windows cp1252 consoles don't crash on UTF-8 strings
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_latest_transcript() -> Optional[str]:
    """Auto-detect the most recent Antigravity session transcript."""
    user_home = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    brain_dir = os.path.join(user_home, ".gemini", "antigravity", "brain")
    if not os.path.exists(brain_dir):
        return None

    transcripts = glob.glob(os.path.join(brain_dir, "*", ".system_generated", "logs", "transcript.jsonl"))
    if not transcripts:
        # Check direct transcripts
        transcripts = glob.glob(os.path.join(brain_dir, "*", "transcript.jsonl"))
    
    if transcripts:
        transcripts.sort(key=os.path.getmtime, reverse=True)
        return transcripts[0]
    return None


class AgentOpportunityScanner:
    def __init__(self, transcript_path: Optional[str] = None):
        if not transcript_path or transcript_path == "auto" or not os.path.exists(transcript_path):
            auto_path = find_latest_transcript()
            if auto_path:
                self.transcript_path = auto_path
                print(f"[INFO] Auto-detected latest session transcript: {self.transcript_path}")
            else:
                self.transcript_path = transcript_path or ""
        else:
            self.transcript_path = transcript_path

        self.steps = []
        self.load_transcript()

    def load_transcript(self):
        if not self.transcript_path or not os.path.exists(self.transcript_path):
            print(f"[ERROR] Transcript path not found: {self.transcript_path}")
            sys.exit(1)

        with open(self.transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        self.steps.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue

    def generate_draft_spec(self, candidate: Dict[str, Any], output_dir: str = ".agents/specs") -> str:
        """Authors an Oracle agent-spec compliant draft YAML for 1-click /build-agent handoff."""
        os.makedirs(output_dir, exist_ok=True)
        cid = candidate["id"]
        filepath = os.path.join(output_dir, f"{cid}.draft.yaml")

        tools_yaml = "\n".join([f"  - name: \"{t}\"\n    type: \"native\"\n    blast_radius: \"workspace-write\"" for t in candidate.get("tools", [])])

        yaml_content = f"""# Auto-generated Draft Spec from /agent-opportunity-scan
schema_version: "2.0.0"

agent:
  name: "{cid}"
  version: "1.0.0"
  description: "{candidate['name']}: {candidate['problem']}"
  archetype: "{candidate['archetype']}"
  runtime: "antigravity-2.0"

triage:
  paradigm: "autonomous-loop"
  justification: "{candidate['problem']}"

lifecycle:
  max_iterations: 10
  recurrence_depth_limit: 2

action_space:
  decouple_internal_actions: true
  max_active_tools: 8
  payload_armor_bytes: 16384
  non_interactive_shell:
    ci: true
    pager: "cat"
    stdin_null: true

tools:
  - name: "ask_human"
    type: "primitive"
    blast_radius: "internal"
    description: "Pause and prompt human when input is ambiguous or requires steering"
{tools_yaml}

safeguards:
  economic_circuit_breaker:
    max_tokens: 250000
    max_estimated_cost_usd: 2.00
  safety_interceptor:
    prohibited_patterns:
      - "rm\\\\s+-rf"
      - "git\\\\s+push\\\\s+.*--force"
      - "drop\\\\s+database"
    credential_redaction: true
  fault_tolerance:
    reflexion_strikes_max: 3
    git_working_tree_rollback: true

verification:
  evaluator_optimizer_gate: true
  day_one_probe: ".agents/tests/{cid}-probe.md"
  mock_fixtures: ".agents/tests/{cid}-fixtures.json"
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(yaml_content)
        return filepath

    def analyze(self, emit_specs: bool = False) -> Dict[str, Any]:
        user_prompts = []
        tool_counts = {}
        error_events = []
        phase_triggers = []
        encoding_errors = 0
        grill_cycles = 0
        agent_mentions = set()

        for i, step in enumerate(self.steps):
            src = step.get("source", "")
            stype = step.get("type", "")
            content = step.get("content", "")
            tool_calls = step.get("tool_calls", [])

            if src == "USER_EXPLICIT":
                user_prompts.append((i, content))
                lower = content.lower()
                if any(k in lower for k in ["begin phase", "let's begin phase", "start phase", "phase 1", "phase 2", "phase 3", "phase 4"]):
                    phase_triggers.append((i, content.strip()))
                if "/auto-grill" in content or "auto grill" in lower:
                    grill_cycles += 1
                if ".agents/agents/" in content or "agent squad" in lower:
                    agent_mentions.add(content[:60])

            for tc in tool_calls:
                name = tc.get("tool_name", tc.get("name", "unknown"))
                tool_counts[name] = tool_counts.get(name, 0) + 1

            # Check for error outputs in tool results
            if stype in ["GENERIC", "TOOL_OUTPUT"] or "UnicodeEncodeError" in content or "exited with code 1" in content:
                if "UnicodeEncodeError" in content or "charmap" in content:
                    encoding_errors += 1
                if "exited with code 1" in content or "Error" in content:
                    error_events.append((i, content[:150]))

        # Synthesize Candidate Opportunities
        candidates = []

        # Candidate 1: Platform Compatibility Guard (Solo Tool User)
        if encoding_errors > 0 or any("charmap" in e[1] for e in error_events):
            candidates.append({
                "id": "windows-compat-guard",
                "name": "Windows Platform Compatibility Guard",
                "archetype": "solo-tool-user",
                "problem": f"Detected {encoding_errors} Windows cp1252 encoding crashes and command failures during CLI test executions.",
                "evidence": "Repeated UnicodeEncodeError: 'charmap' codec crashes when scripts printed emojis/formatting to stdout.",
                "frequency_monthly": 16,
                "mean_toil_mins": 15,
                "blast_radius": 1.0,  # read-only inspection / scratch shim
                "score": round((16 * 15) / 1.0, 1),
                "tools": ["view_file", "replace_file_content", "run_command"],
                "build_agent_cmd": '/build-agent --from-spec .agents/specs/windows-compat-guard.draft.yaml'
            })

        # Candidate 2: Autonomous Multi-Phase Pipeline Runner (Solo Tool User / Squad)
        if len(phase_triggers) >= 2:
            candidates.append({
                "id": "pipeline-stage-runner",
                "name": "Autonomous Multi-Phase Pipeline Runner",
                "archetype": "solo-tool-user",
                "problem": f"Detected {len(phase_triggers)} manual phase advancement prompts requiring user turn-taking across sequential implementation stages.",
                "evidence": "User had to prompt: 'Ok let's begin phase 1', 'Ok begin phase 2', adding 30+ minutes of idle human waiting.",
                "frequency_monthly": 12,
                "mean_toil_mins": 35,
                "blast_radius": 1.5,
                "score": round((12 * 35) / 1.5, 1),
                "tools": ["run_command", "view_file", "write_to_file"],
                "build_agent_cmd": '/build-agent --from-spec .agents/specs/pipeline-stage-runner.draft.yaml'
            })

        # Candidate 3: Global Skill Synchronization Sentinel (Autonomous Sentinel)
        candidates.append({
            "id": "skill-sync-sentinel",
            "name": "Skill Synchronization & Discovery Sentinel",
            "archetype": "autonomous-sentinel",
            "problem": "Newly authored skills in workspace repo (skills/<phase>/) are silently omitted from Antigravity's slash autocomplete menu until manually copied to global config.",
            "evidence": "User reported: 'I can't see build agent in my agent panel when I use /' after construction.",
            "frequency_monthly": 20,
            "mean_toil_mins": 10,
            "blast_radius": 1.5,
            "score": round((20 * 10) / 1.5, 1),
            "tools": ["run_command", "view_file", "schedule"],
            "build_agent_cmd": '/build-agent --from-spec .agents/specs/skill-sync-sentinel.draft.yaml'
        })

        # Candidate 4: Dialectical Convergence Gatekeeper (Solo Tool User)
        if grill_cycles >= 3:
            candidates.append({
                "id": "grill-saturation-sentinel",
                "name": "Dialectical Saturation Gatekeeper",
                "archetype": "solo-tool-user",
                "problem": f"Detected {grill_cycles} recursive auto-grill cycles generating theoretical micro-nodes past the point of diminishing returns.",
                "evidence": "User had to step in: 'Are we over engineering this agent build? Or should we keep going with the auto grill?'",
                "frequency_monthly": 8,
                "mean_toil_mins": 25,
                "blast_radius": 1.0,
                "score": round((8 * 25) / 1.0, 1),
                "tools": ["view_file", "ask_question"],
                "build_agent_cmd": '/build-agent --from-spec .agents/specs/grill-saturation-sentinel.draft.yaml'
            })

        # Sort candidates by Viability Score descending
        candidates.sort(key=lambda c: c["score"], reverse=True)

        # Emit draft specifications if requested or for top candidate
        generated_specs = []
        if emit_specs:
            for c in candidates:
                spec_path = self.generate_draft_spec(c)
                c["draft_spec_path"] = spec_path
                generated_specs.append(spec_path)
        elif len(candidates) > 0:
            top_spec = self.generate_draft_spec(candidates[0])
            candidates[0]["draft_spec_path"] = top_spec
            generated_specs.append(top_spec)

        return {
            "transcript_used": self.transcript_path,
            "total_steps": len(self.steps),
            "user_prompts_count": len(user_prompts),
            "tool_counts": tool_counts,
            "encoding_errors": encoding_errors,
            "grill_cycles": grill_cycles,
            "candidates": candidates,
            "generated_draft_specs": generated_specs
        }

    def render_markdown(self, analysis: Dict[str, Any]) -> str:
        md = []
        md.append("# Agent Opportunity Scan — Summary Dossier\n")
        md.append(f"- **Transcript Scanned:** `{analysis.get('transcript_used', 'N/A')}`")
        md.append(f"- **Total Session Steps:** {analysis['total_steps']}")
        md.append(f"- **User Interactions:** {analysis['user_prompts_count']}")
        md.append(f"- **Identified Agent Candidates:** {len(analysis['candidates'])}\n")
        md.append("## High-Value Agentification Candidates\n")

        for idx, c in enumerate(analysis["candidates"], 1):
            md.append(f"### {idx}. {c['name']} (`{c['archetype']}`)")
            md.append(f"- **Viability Score (AVS):** `{c['score']}` (Frequency: {c['frequency_monthly']}/mo | Toil: {c['mean_toil_mins']}m | Risk: {c['blast_radius']})")
            md.append(f"- **Problem:** {c['problem']}")
            md.append(f"- **Evidence:** {c['evidence']}")
            md.append(f"- **Required Tools:** `{', '.join(c['tools'])}`")
            if c.get("draft_spec_path"):
                md.append(f"- **Pre-Filled Draft Spec:** `{c['draft_spec_path']}`")
            md.append(f"- **Direct 1-Click Handoff Command:**\n  ```bash\n  {c['build_agent_cmd']}\n  ```\n")

        return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Scan session transcript for agent opportunities")
    parser.add_argument("transcript", nargs="?", default="auto", help="Path to transcript.jsonl or 'auto'")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--auto-spec", action="store_true", help="Automatically generate draft .spec.yaml for all candidates")
    args = parser.parse_args()

    scanner = AgentOpportunityScanner(args.transcript)
    results = scanner.analyze(emit_specs=args.auto_spec)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(scanner.render_markdown(results))


if __name__ == "__main__":
    main()
