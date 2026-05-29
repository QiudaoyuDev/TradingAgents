---
name: kw-knowledge-baseline
description: Plan, advise, and regenerate Knowledge Workshop project knowledge baselines.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-knowledge-baseline/SKILL.md.tmpl source-sha256=70d8a0d0e4720ba62009856e0e9a1518216d6d68e02d73e5e08520f8e8e08f1a -->

# Knowledge Baseline

Use this skill when a consumer skipped onboarding, needs to rebuild the initial knowledge map, or wants advice for evolving `knowledge/**` and `specs/**`.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Shared Knowledge Governance

When advising or regenerating durable maps, read `specs/knowledge-governance.md` from the active Knowledge Workshop runtime or the `.kw/index/specs.json` item with `spec_id=knowledge-governance`. Use it to preserve fact-layer boundaries, writeback direction, publishability, and index semantics in generated baseline knowledge.

## Read Order

1. Read `.kw/workspace/workspace.json`.
2. Read `.kw/index/knowledge.json`, `.kw/index/specs.json`, and `.kw/index/changes.json` when they exist.
3. Read existing `knowledge/project-map.md`, `knowledge/writeback-playbook.md`, `knowledge/repos/**`, and `knowledge/references/**` when present.
4. Inspect managed repositories and read-only references declared by workspace inventory.
5. Read an operator-provided `kw-onboarding-answers-v1` file when one is supplied.

## Modes

- Use `kw control knowledge-baseline plan --consumer-root .` for a read-only baseline plan.
- Use `kw control knowledge-baseline advise --consumer-root .` for evolution advice without writes.
- Use `kw control knowledge-baseline regenerate --consumer-root . --change <change> --write` only inside an active change after `preflight-write`.

## Rules

- Generate a useful map, not an empty template: purpose, audience, capability map, repo/reference map, verification entrypoints, writeback direction, publishability, and open questions.
- Make maps AI-actionable: include concrete evidence links, AI entrypoints, likely change targets, and verification entrypoints using workspace-relative paths where possible.
- Follow the consumer `artifact_locale` for human-readable generated baseline headings and prose. Keep paths, commands, JSON keys, model/schema names, source labels, and publishability enum values in their protocol form.
- Label conclusions as `confirmed-by-user`, `evidence-backed`, `inferred`, or `open-question`.
- Treat managed repositories whose `roles` include `control` or `self` as a control-plane boundary map, not as ordinary product source. Record `roles`, `boundary_class`, `summary_mode`, stable entrypoints, write boundaries, verification entrypoints, and open questions.
- Do not recursively summarize `.kw/index/**`, `.kw/local/**`, `.agents/**`, `.claude/**`, `references/knowledge/**`, `references/capabilities/**`, `changes/archive/**`, or generated `knowledge/project-map.md` as ordinary project knowledge sources.
- Treat reference repositories and reference controls as read-only; do not turn them into project facts unless the user confirms adoption.
- Keep business facts in consumer `knowledge/**` or `specs/**`; do not copy them into this skill.
- Do not patch generated `.agents/**`, `.claude/**`, or `.kw/bin/**` files as the product source. For shared baseline behavior, trace and update `share/knowledge_workshop/templates/**`, `share/knowledge_workshop/locales/**`, runtime generators/checkers, specs, guides, and tests.
- Treat capability package publishing as a separate package step handled by `kw control capability`; baseline advice may suggest `public`, `consumer-public`, `restricted`, or `secret` classifications.
