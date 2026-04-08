---
id: "0002"
title: "MCP Server Tools Plan"
stage: plan
date: 2026-04-07
surface: agent
model: claude-opus-4-6
feature: 001-mcp-server-tools
branch: 001-mcp-server-tools
user: hassam-rauf
command: /sp.plan
labels: ["mcp", "tools", "phase-iii", "plan", "architecture"]
links:
  spec: specs/001-mcp-server-tools/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-mcp-server-tools/plan.md
  - specs/001-mcp-server-tools/research.md
  - specs/001-mcp-server-tools/data-model.md
  - specs/001-mcp-server-tools/quickstart.md
  - specs/001-mcp-server-tools/contracts/tools-api.md
tests:
  - null
---

## Prompt

/sp.plan 001-mcp-server-tools

## Response snapshot

Created implementation plan for MCP Server + Tools. Constitution check passed all 8 principles. Designed 4 components: tools.py (5 functions), schemas.py (OpenAI format), dispatcher.py (central routing), test suite (~21 tests). Phase 0 research resolved 5 decisions (in-process vs server, dict returns, error handling, schema format, testing strategy). Phase 1 produced data-model.md (reuses existing Task, no migrations), contracts/tools-api.md (all 5 tool schemas + dispatcher contract), and quickstart.md. Pure additive change — no existing files modified.

## Outcome

- ✅ Impact: Complete plan with 4 design decisions, component specs, and dependency graph
- 🧪 Tests: ~21 tests planned across 7 test classes
- 📁 Files: 5 artifacts created (plan, research, data-model, contracts, quickstart)
- 🔁 Next prompts: /sp.adr for ADR-005 (MCP Protocol), then /sp.tasks
- 🧠 Reflection: Clean additive design — no existing files touched, reuses Task model directly

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Constitution check PASS (8/8 principles)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.adr then /sp.tasks
