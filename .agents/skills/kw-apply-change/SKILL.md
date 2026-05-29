---
name: kw-apply-change
description: Execute tasks for an existing Knowledge Workshop change after required planning gates and write preflight.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-apply-change/SKILL.md.tmpl source-sha256=919144ec36f12019e18994e759af889871352b390d19571273b287c74898559e -->

# Apply Change

Use this skill only for a change that is in `execution` or is ready to enter `execution` according to its active `workflow_lifecycle`.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Before Writing

1. Read the change `change.json`, `runtime.json`, `proposal.md`, `design.md`, and `tasks.md`.
2. Inspect `.kw/index/specs.json` for `spec_id=control-objective` before implementation. Use that
   objective to keep the implementation path aligned; if absent, fall back to `knowledge/project-map.md`
   and preserve the follow-up to create `specs/control-objective.md`. If implementation changes the
   `project_goal_alignment`, update planning artifacts before continuing.
3. Before mutating `kw` commands, remember that the runtime decision guard may lazily refresh a missing, stale, invalid, or `current_version`-drifted advisory cache as a policy-controlled read-only check. You may still run `kw control update-advisory --consumer-root .` explicitly to inspect the advisory; neither path is a startup check or auto-update.
4. If any `kw` command returns `runtime_update_decision_required`, stop before writing, report the runtime update choice to the user, and either update or run the returned dismiss command before retrying the original command.
5. When starting execution, after a phase switch, and after runtime update or dogfood refresh, run `kw control bootstrap-reconcile --consumer-root . --write` and stop on blockers. Reconcile restores declared state only; it is not an approval to add undeclared artifacts, versions, or capabilities. Ordinary mutating `kw change` commands still have the built-in bootstrap guard and do not need a separate manual reconcile step every time.
6. Run `kw change validate --change <change>`.
7. Run `kw change refresh-requirements --change <change>`.
8. Ensure required approvals for the active lifecycle are recorded; `quick-patch` and `ops-task` do not require a design-phase approval unless policy materializes one.
9. Run `kw change preflight-write --change <change> --repo <repo> --path <path>` before writing each managed repo scope.

## Commit Timing

Use `preflight-write` before managed writes. It is a write gate, not a proposal/design commit requirement.

## Execution

- Edit only files required by the current task.
- Mark completed task checkboxes immediately.
- Record checkpoints with `kw change checkpoint`.
- Use `document-writing` locale selection for human-facing progress, status, and checkpoint summaries; translate conclusions from English canonical specs into the selected language while preserving protocol tokens.
- If scope expands or the execution plan is wrong, stop and use the rollback target allowed by the active lifecycle. `standard-change` can return to `design`; `quick-patch` and `ops-task` return to `execution` from `acceptance`.
