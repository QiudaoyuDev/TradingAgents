---
name: kw-explore
description: Read Knowledge Workshop context, inspect facts, and compare options without writing managed repositories.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-explore/SKILL.md.tmpl source-sha256=d86c13e2c80702e3f1a6dfdc4b0ee1403dbf440573d282571871cc828b489c19 -->

# Explore

Use this skill when the user asks a question, requests investigation, or needs design context before a formal change.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Read Order

1. Read `.kw/workspace/workspace.json`.
2. Read `.kw/index/changes.json` and `.kw/index/change-contexts.json` when present.
3. If a change is named, read its `change.json`, `runtime.json`, and current phase artifacts.
4. Before judging `project_goal_alignment`, reusable knowledge gaps, or follow-up targets, inspect `.kw/index/specs.json` for
   `spec_id=control-objective`. If absent, fall back to `knowledge/project-map.md` and recommend a
   follow-up change to create `specs/control-objective.md`.
5. Read only the minimal `specs/**`, `knowledge/**`, code, and docs needed for the question.

## Rules

- Do not write managed repositories in explore mode.
- Treat reference repositories and reference controls as read-only.
- Keep findings tied to file paths and concrete facts.
- Follow `document-writing` locale selection for human-facing findings; when English canonical specs are the source, restate conclusions in the selected language and keep machine contract tokens unchanged.
- In no-active-change exploration, do not write change evidence. If reusable cognition appears, report a learning candidate or follow-up change target instead.
- If implementation is needed, hand off to `kw-propose` or `kw-apply-change` after the change state is clear.
