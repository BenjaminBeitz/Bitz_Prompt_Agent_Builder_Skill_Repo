---
type: concept
title: "Oracle Open Agent Spec and Agent Protocol Standards"
description: "Analysis of open declarative agent specifications (Oracle agent-spec) and standardized REST/SSE client-agent communication protocols (Agent Protocol)."
tags: [oracle-agent-spec, agent-protocol, declarative-specifications, rest-sse]
timestamp: 2026-10-08T16:50:00Z
status: active
generated: false
verified: true
verified_by: "@antigravity"
sources:
  - "https://github.com/oracle/agent-spec"
  - "https://github.com/AI-Engineer-Foundation/agentprotocol.ai"
---

# Oracle Open Agent Specification and Agent Protocol Standards

## ðŸ’¡ Strategic Context & Rationale
*Foundational Survey:* [Top 5 Specifications](01-top-5-agent-specifications.md)  
*Specification Output:* [Architecture: Build Agent Engine](../docs/architecture/arch-build-agent-engine.md)

Open declarative standards allow agents to be defined as portable data structures rather than opaque, framework-coupled code. This ensures agents can be inspected, version-controlled, validated, and migrated across execution runtimes.

---

## 1. Oracle `agent-spec` (Declarative Architecture Standard)

The Oracle Open Agent Specification defines agents as structured YAML/JSON data files:

### Core Declarative Schema Dimensions
1. **Metadata:** `spec_version`, `agent.name`, `display_name`, `description`, `version`.
2. **Components & Tools:**
   - Formal interface schemas and parameter types.
   - Execution permissions (read-only vs mutating).
   - Rate limits and timeout ceilings.
3. **Flows & State Machines:**
   - Explicit state transitions and decision branch points.
   - Loop termination criteria (max iterations, token ceilings).
   - Human-in-the-loop escalation barriers.
4. **Runtime Interoperability:**
   - Compiles cleanly into executable graphs (LangGraph, AutoGen) or standalone Python runners.

### Template Schema Used in Suite
Our suite generates `.agents/specs/<name>.spec.yaml` conforming to this standard:
```yaml
spec_version: "1.0"
agent:
  name: "db-migration-auditor"
  display_name: "Database Migration Auditor"
  archetype: "solo-tool-user"
  version: "1.0.0"
action_space:
  tools:
    - name: "view_file"
      permission: "read_only"
    - name: "run_command"
      permission: "scoped_execution"
verification:
  definition_of_done: "All migrations validated with zero data-loss hazards."
  fired_conditions:
    - "Executing drop table commands in production"
```

---

## 2. Agent Protocol (Universal REST/SSE Interface)

Developed by the AI Engineer Foundation, **Agent Protocol** standardizes client-agent communication across open-source agent runtimes (AutoGPT, e2b, Smolagents):

### Universal REST Endpoints
- **`POST /ap/v1/agent/tasks`**: Creates a new task session with an input payload.
- **`GET /ap/v1/agent/tasks/{task_id}`**: Retrieves task status and metadata.
- **`POST /ap/v1/agent/tasks/{task_id}/steps`**: Executes the next autonomous step; streams execution logs via Server-Sent Events (SSE).
- **`GET /ap/v1/agent/tasks/{task_id}/artifacts`**: Lists deliverables, reports, and code produced by the agent.

### Integration in our Python Micro-Harness
In our suite, every generated agent runner (`runner.py`) includes a built-in REST adapter compatible with Agent Protocol, allowing any agent created by `/build-agent` to be invoked programmatically over HTTP or integrated into CI/CD pipelines.

---

## ðŸ”— Related Knowledge Base Links
* ðŸ  [Master Index](index.md)
* ðŸ“š [Top 5 Foundational Specifications](01-top-5-agent-specifications.md)
* ðŸ›¡ï¸ [Runtime Harness Specification](../docs/architecture/arch-runtime-harness-and-armor.md)
* ðŸ—ï¸ [Build Agent Engine Architecture](../docs/architecture/arch-build-agent-engine.md)

