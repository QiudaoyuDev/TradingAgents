---
name: kw-archive-change
description: Archive a completed Knowledge Workshop change after validation.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-archive-change/SKILL.md.tmpl source-sha256=5403cdb6c0c1e1c972cf06b8d7d602b023eb86f8e27e81487c1ed9687860c079 -->

# Archive Change

Use this skill only for a completed change.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Flow

1. Run `kw change validate --change <change>`.
2. Confirm the change status is `completed`.
3. Run `kw change archive-sync --change <change>`.
4. Report the archive path and any validation warnings.
