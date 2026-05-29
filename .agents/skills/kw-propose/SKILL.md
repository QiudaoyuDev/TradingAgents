---
name: kw-propose
description: Create or complete a Knowledge Workshop formal change with proposal, design, and tasks.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-propose/SKILL.md.tmpl source-sha256=d170549c86cd2c8a2a3087e08cd76c9093f6d7a76c98ad8a51de3d065e4680f4 -->

# Propose

Use this skill when work needs durable planning, cross-file coordination, workflow gates, or reviewable artifacts before implementation.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Shared Knowledge Governance

Before planning durable `knowledge/**` or `specs/**` writeback, read `specs/knowledge-governance.md` from the active Knowledge Workshop runtime or the `.kw/index/specs.json` item with `spec_id=knowledge-governance`. Use it to choose the fact layer, expected writeback target, and whether a repeated task truly needs a project skill.

## Control Objective Alignment

Before writing `proposal.md`, `design.md`, or `tasks.md`, inspect `.kw/index/specs.json` for
`spec_id=control-objective`. Use it as the `project_goal_alignment` basis. If it is absent, fall back to
`knowledge/project-map.md`, record the fallback in the planning artifacts, and recommend a follow-up
change to create `specs/control-objective.md`. The objective spec is `mandatory-by-convention`, not a
blocking gate in this version.

## Flow

1. Run `kw change sync` and inspect active changes.
2. Before mutating `kw` commands, remember that the runtime decision guard may lazily refresh a missing, stale, invalid, or `current_version`-drifted advisory cache as a policy-controlled read-only check. You may still run `kw control update-advisory --consumer-root .` explicitly to inspect the advisory; neither path is a startup check or auto-update.
3. If any `kw` command returns `runtime_update_decision_required`, stop the current operation, report the current/latest runtime and update kind to the user, and ask whether to update or skip. On skip, run the returned dismiss command and retry the original command; major updates require upgrade planning/migration before update.
4. At change start, phase switches, and after runtime update or dogfood refresh, run `kw control bootstrap-reconcile --consumer-root . --write` or inspect its blockers. Reconcile only restores declared state from locks, dependencies, and managed project capability sources; it must not choose a new version or add undeclared sources. Ordinary mutating `kw change` commands still have the built-in bootstrap guard and do not need a separate manual reconcile step every time.
5. Reuse the named active change, or create one with `kw change new --change-id <id> --title "<title>" --workflow-lifecycle <lifecycle> --workflow-profile <profile> --repo <repo> --path <path>`.
6. Read `runtime.json` and follow the active `workflow_lifecycle`; do not assume every change starts in `proposal`.
7. For `standard-change`, fill `proposal.md`, move to `design`, then fill `design.md` and `tasks.md`.
8. For `quick-patch` or `ops-task`, confirm the change starts in `execution`, keep planning artifacts concise, and use `tasks.md` as the execution checklist.
9. During design and task planning, complete the design's `Knowledge Writeback Plan`. Decide whether the change will need durable `knowledge/**`, `specs/**`, shared policy/skill/template/docs, or a follow-up change for any project-goal reusable knowledge gap. Record reusable judgment, existing coverage, planned disposition, target paths, not-needed category, and acceptance reconciliation before execution so acceptance `review-knowledge` is not a surprise.
10. Follow `document-writing` locale selection for human-facing plans and design conclusions; summarize English canonical specs in the selected language and keep machine contract tokens unchanged.
11. Run `kw change validate --change <change>` and `kw change refresh-requirements --change <change>`.

## Commit Timing

Create `proposal`, `design`, and task artifacts as owned active-change state. Follow project policy or post-acceptance closure for commits.

Do not treat `preflight-write` as a proposal/design commit requirement; it belongs before managed writes in execution.

## Human Gates

If a decision needs user approval, add the matching requirement/tag and stop before execution when the active lifecycle has a planning phase. After explicit approval, record it with `kw change record-requirement`.

## Shared Surface Check

Before finalizing scope, check whether the requested fix touches generated artifacts, shared guidance, agent skills, locale overlays, runtime checkers, templates, or cross-consumer behavior. If it does, trace the source before planning writes: `share/knowledge_workshop/templates/**`, `share/knowledge_workshop/locales/**`, generators, checkers, guides, specs, and tests. Generated `.agents/**`, `.claude/**`, and `.kw/bin/**` files are outputs, not repair sources.
