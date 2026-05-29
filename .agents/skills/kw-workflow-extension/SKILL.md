---
name: kw-workflow-extension
description: Plan and maintain local workflow requirements and gates.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-workflow-extension/SKILL.md.tmpl source-sha256=6d7c47b2e5cdd5921287c5bb710eb2297a388c67842f2b0731b50546bb88667c -->

# Workflow Extension

Use this skill when a project needs local workflow requirements beyond the default Knowledge Workshop state machine.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Flow

1. Read `.kw/policies/workflow-extension.json`.
2. Decide whether the requirement is project-local or belongs in the shared product. If a reusable lesson applies across consumers, or an existing shared rule failed to guide behavior, stop local policy edits and route the candidate to a shared product change.
3. Prefer declarative requirements over custom scripts.
4. Run `kw change validate` after edits.
5. Refresh active changes with `kw change refresh-requirements --change <change>`.

Shared default policy changes should be made in the Knowledge Workshop product repo through a formal change.

Knowledge writing rules belong to `kw-knowledge-writing-policy`, not workflow extension policy.
