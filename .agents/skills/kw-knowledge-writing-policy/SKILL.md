---
name: kw-knowledge-writing-policy
description: Plan and maintain Knowledge Workshop knowledge writing policies.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-knowledge-writing-policy/SKILL.md.tmpl source-sha256=814e38d853dcda43d5f7f9d1903018fa37daa39a75b0094909c2a0cce83aea68 -->

# Knowledge Writing Policy

Use this skill when a project or capability package needs rules for how `kw change review-knowledge` should classify durable facts, choose shared or consumer targets, and require review evidence fields.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Shared Knowledge Governance

Before changing knowledge writing policy rules, read `specs/knowledge-governance.md` from the active Knowledge Workshop runtime or the `.kw/index/specs.json` item with `spec_id=knowledge-governance`. Use it to keep policy targets aligned with shared fact layers, candidate capture, review evidence, and skill-vs-knowledge boundaries.

## Flow

1. Read `.kw/project-capabilities.json` and existing `.kw/policies/knowledge-writing.json` when present.
2. For packaged policies, inspect `capability/profile.json` and planned `knowledge_writing_policies[]` entrypoints.
3. Keep policy rules declarative: selectors, docs, target hints, result guidance, required review fields, result-specific required fields, and path fields.
4. Do not define workflow gates here; `knowledge-delta-reviewed` is a KW base requirement.
5. Validate policy payloads with `kw-knowledge-writing-policy-v1` and verify `kw change review-knowledge` reports matched policies.

Writing policies describe how knowledge should be written. They do not decide whether knowledge review is required.

For AI-actionable knowledge, require enough fields for future agents to locate evidence and act: `target_paths`, `knowledge_kind`, `source_basis`, `evidence_links`, `ai_entrypoints`, `writeback_direction`, and `publishability`. Use `path_fields` for fields whose values must be existing workspace-relative paths.
