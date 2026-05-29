---
name: kw-self-bootstrap
description: Review project-goal reusable cognition and meta-rule candidates for the current change or durable project assets.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-self-bootstrap/SKILL.md.tmpl source-sha256=137c4312e12eedeee6304aeaecc8f878943d64e1d67e506292dfecbf51289728 -->

# Self Bootstrap

Use this skill whenever a project-goal-relevant task exposes reusable cognition that can change future agent judgment boundaries, execution boundaries, workflow rules, shared/local ownership decisions, generated-surface source tracing, or durable writeback targets. The trigger is not limited to code changes, explicit user correction, failures, workarounds, or blockers; review, product analysis, research, operations troubleshooting, architecture judgment, process optimization, and domain modeling can all expose candidates when the insight is reusable, currently uncovered, stable, and evidence-backed.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Shared Knowledge Governance

Before choosing a durable target for a reusable cognition or meta-rule, read `specs/knowledge-governance.md` from the active Knowledge Workshop runtime or the `.kw/index/specs.json` item with `spec_id=knowledge-governance`. Use it to classify shared-base, consumer-local, contributor-artifact, and project-skill boundaries without creating a standalone one-spec skill.

## Control Objective Alignment

Inspect `.kw/index/specs.json` for `spec_id=control-objective` before classifying
`project_goal_alignment`. If absent, fall back to `knowledge/project-map.md` and include a follow-up to
create `specs/control-objective.md`. The objective spec is `mandatory-by-convention`, not a blocking gate
in this version.

## Flow

1. Stop the wrong or blocked action, then contain any current pollution such as an unwanted change, dirty file, failed command side effect, or incorrect scope expansion.
2. If there is no active change, do not write change evidence. Output a no-active-change learning candidate or follow-up change target with the same routing fields, then wait for a formal change before durable writeback.
3. Read the active change `change.json`, `runtime.json`, matched requirements, and current `knowledge_delta_review`; re-anchor only the relevant entrypoints such as `AGENTS.md`, workspace facts, the active skill, and applicable shared or local policies.
4. Write a learning candidate with: `project_goal_alignment`, `observed_knowledge_gap`, `reuse_context`, `evidence_basis`, `recommended_target`, `writeback_decision`, human merge decision, follow-up change or TODO, and conclusion. Also classify `self_growth_level`, `target.target_kind`, `evidence_refs`, `eval_cases`, `human_approval`, and `proposal_only` when the candidate may become a `kw-self-growth-proposal-v0`. When `review-knowledge` fields identify reusable project-goal knowledge, upgrade that review into this learning candidate before durable writeback.
5. Classify the candidate as one-off, reusable lesson, or meta-rule candidate. A meta-rule candidate must state which future judgment boundary or execution boundary changes; a lesson may only explain a reusable fact or tactic.
6. Keep the candidate out of the current change until a human explicitly accepts it. If accepted, update the owning scope, design, tasks, and requirements before writing to the durable surface; if rejected or deferred, record the follow-up or not-needed decision.
7. Pick the target after the learning candidate is clear: current fix, project knowledge or runbook, script, project skill, workflow requirement, knowledge writing policy, shared Knowledge Workshop product, follow-up change, or no durable writeback.
8. For an accepted meta-rule, choose an owning canonical source before editing generated output: spec, workflow policy, knowledge-writing policy, canonical skill guidance, test gate, project capability, or follow-up change.
9. Bind the meta-rule to verification. It must have a policy field, workflow requirement, generated skill trigger, test assertion, or explicit follow-up gate; do not leave it as abstract advice.
10. If the target is project-local workflow or writing policy, use `kw-workflow-extension` or `kw-knowledge-writing-policy`. If it is a project skill, produce a candidate only and route writes to `kw-project-capability`.
11. If the issue is reusable across consumers, or an existing shared rule failed to guide behavior, prefer a shared product change over consumer-local policy.
12. Record `self-bootstrap-review` and `review-knowledge` evidence with the generalized learning candidate fields plus durable routing fields; do not use root-cause depth or budget fields.

## Self-growth Level Classification

- `L0`: observation or no-op; record why no durable candidate or writeback is needed.
- `L1`: learning candidate; record candidate, evidence, and review without changing stable assets.
- `L2`: human-scoped guidance change; update knowledge, specs, docs, or skill guidance only after a formal change and human merge decision.
- `L3`: eval-gated capability behavior; require `eval_cases` and evidence before merge, without expanding execution authority.
- `L4`: approval-gated execution or control surface; require Eval/Evidence and `human_approval` before accepted or merged status.
- `L5`: autonomous or platform self-modification proposal; keep `proposal_only`, require `human_approval`, and never record it as merged.

## Self-Triggered Shared Review

- Trigger this review without waiting for user correction when reusable project-goal cognition involves generated artifacts, shared guidance, agent skills, locale overlays, runtime checkers, templates, or cross-consumer behavior.
- For generated `.agents/**`, `.claude/**`, `.kw/bin/**`, template-rendered, or locale-rendered output, trace the canonical source before choosing a repair target: `share/knowledge_workshop/templates/**`, `share/knowledge_workshop/locales/**`, generators, checkers, guides, specs, and tests.
- Treat user correction as a fallback trigger, not a prerequisite. If the agent discovers a comparable reusable cognition during its own iteration, create the same learning candidate.
- Record shared-source tracing in `evidence_basis` or `writeback_decision` when relevant: whether the review was self-triggered, which shared source was checked, the generated artifact source, any rule or skill gap, selected repair target, and scope-classification basis.
- If the selected target is a shared rule or skill, route through a shared product change and update the canonical template plus locale overlays and tests. Do not hand-edit generated skill copies as the source of truth.

## Boundary

- Do not put business rules in generated agent skills.
- Do not treat chat text as a substitute for `record-requirement`, `verify`, or `review-knowledge`.
- Do not rely on automatic language detection for feedback; use explicit evidence, failed commands, verification results, and workflow requirements.
- Do not turn every issue into a durable asset; session-only preferences and one-off clarifications can end as `not-needed`.
- Do not auto-expand the current change. Human merge decision is required before the candidate changes scope, tasks, scripts, skills, knowledge, or shared product behavior.
- Do not grow this skill as an incident log. Add or update durable knowledge, scripts, capability routing, policy fields, specs, tests, or follow-up TODOs instead.
