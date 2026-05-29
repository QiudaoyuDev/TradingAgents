---
name: kw-finish-change
description: Complete Knowledge Workshop acceptance by recording verification, knowledge review, and finish evidence.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-finish-change/SKILL.md.tmpl source-sha256=1c839249426ab516a9c4d85607949f41b4bf13f102818f4ddddcd22f75eaedbd -->

# Finish Change

Use this skill when implementation tasks are complete and the change needs acceptance.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Shared Knowledge Governance

Before the project-goal knowledge gap scan, read `specs/knowledge-governance.md` from the active Knowledge Workshop runtime or the `.kw/index/specs.json` item with `spec_id=knowledge-governance`. Use it as the shared source for fact layers, writeback routing, candidate/review evidence, and skill-vs-knowledge boundaries.

## Control Objective Alignment

Before `review-knowledge`, inspect `.kw/index/specs.json` for `spec_id=control-objective`. The
`project_goal_alignment` field must cite that objective, or state that the objective is absent and that
`knowledge/project-map.md` was used as the fallback. Missing `specs/control-objective.md` should produce
a follow-up recommendation, not a blocking gate in this version.

## Flow

1. Run `kw change validate --change <change>`.
2. Before mutating acceptance commands, remember that the runtime decision guard may lazily refresh a missing, stale, invalid, or `current_version`-drifted advisory cache as a policy-controlled read-only check. You may still run `kw control update-advisory --consumer-root .` explicitly to inspect the advisory; neither path is a startup check or auto-update.
3. Run `kw control bootstrap-reconcile --consumer-root . --write` after entering acceptance, after runtime update, or after dogfood refresh, and stop on blockers. Ordinary mutating `kw change` commands still have the built-in bootstrap guard and do not need a separate manual reconcile step every time.
4. If any `kw` command returns `runtime_update_decision_required`, stop acceptance work, ask the user whether to update or skip, and retry only after update or dismissal.
5. Confirm `tasks.md` has no incomplete checkboxes before finish.
6. Run the verification commands promised in `design.md`.
7. Record each meaningful verification with `kw change verify`.
8. Run a project-goal knowledge gap scan before `review-knowledge`: list the task's key judgments, check existing `knowledge/**`, `specs/**`, and installed capability package entrypoints for coverage, then decide whether each reusable, stable, evidence-backed gap needs `created-new`, `updated-existing`, follow-up, or `not-needed`.
9. Record `kw change review-knowledge` with matched knowledge writing policy fields. Every result, including `not-needed`, must fill durable routing fields (`reusable_lesson_review`, `reusable_lesson_decision`, `writeback_target`, `decision_basis`, `followup_change_or_todo`) and project-goal fields (`project_goal_alignment`, `observed_knowledge_gap`, `reuse_context`, `evidence_basis`, `recommended_target`, `writeback_decision`). For `created-new` or `updated-existing`, also include AI-actionable fields such as target paths, source basis, evidence links, AI entrypoints, writeback direction, publishability, and `applicable_scenarios`. For `not-needed`, set `not_needed_category` to `already-covered`, `one-off`, `unverified`, `sensitive`, `human-deferred`, or `out-of-project-goal`; `already-covered` must name the existing coverage path in `not_needed_basis`.
10. Move to acceptance with `kw change enter-phase --change <change> --to acceptance` when the active `workflow_lifecycle` has not already reached `acceptance`.
11. Inspect all pending acceptance requirements in `runtime.json`; complete every agent-actionable hard gate, including `verification_requirement` entries such as local package dogfood, before waiting for human acceptance.
12. If `roadmap-closure-review` is pending, confirm the roadmap row was updated and record `kw change record-requirement --requirement-id roadmap-closure-review` before asking for human acceptance.
13. Report the completed result to the operator, including implementation summary, lifecycle used, verification results, knowledge review, dogfood or other acceptance gate results, and any remaining blockers; this report follows `document-writing` locale selection and restates English canonical spec conclusions in the selected language. Then wait for a new post-completion acceptance response.
14. Record `human-acceptance-approval` only from a response after that completed-result report. Do not reuse design, execution, finish, archive, or commit pre-approval. The summary must include `completed_result_summary=`, `agent_gates_completed=`, `human_response_after_result=`, and `conclusion=`.
15. Run `kw change close --change <change> --archive --sync`.
16. If blockers remain, address them or record why they cannot be completed.
