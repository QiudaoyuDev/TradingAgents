---
name: kw-upgrade
description: Plan and execute Knowledge Workshop consumer upgrades.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-upgrade/SKILL.md.tmpl source-sha256=a2ce89d56b19375725751c00ca5cefe02d095f3f5ae1789a4f9fd55b41957aa3 -->

# Upgrade

Use this skill when a consumer workspace needs a Knowledge Workshop version update or entrypoint refresh.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Flow

1. Read `.kw/workspace/workspace.json` and `.kw/kw-lock.json`.
2. Run `kw control update-advisory --consumer-root .` for a read-only update check.
3. If another `kw` command returns `runtime_update_decision_required`, treat it as an agent-facing user decision: report current/latest/update kind, then update or run the returned dismiss command before retrying the original command.
4. Run `kw control upgrade-plan --consumer-root . --to <version|latest>`.
5. For major upgrades, create a migration change before writing.
6. Execute with `kw control update --consumer-root . --version <version> --yes`.
7. Validate with `kw change validate` and `kw change sync`.
