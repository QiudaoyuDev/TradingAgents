---
name: kw-project-capability
description: Plan, sync, and install project-level agent capabilities.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-project-capability/SKILL.md.tmpl source-sha256=9f94af53984af2962d1b201795c8a2f6e401cd537a9d7b64c789b26f381dc36a -->

# Project Capability

Use this skill for project-level skills, workflow requirements, knowledge writing policies, agent permissions, and update-advisory configuration.

Project capabilities are compliance-on by default. Do not add ordinary `enabled:false` switches. Use declared sources, installed capability package locks, and `kw control project-capabilities plan` status values (`inherited`, `managed`, `not_configured`, `blocked`, `override_disabled`) to explain behavior.

This skill owns project-local activation only: `.kw/project-capabilities.json`, `.kw/project-skills.json`, `.kw/policies/**`, `.kw/project-agent-permissions.json`, and `.kw/kw-update-policy.json`. Local-only capabilities do not need `capability-package.json`, `capability/profile.json`, `skills/project-skills.json` under a package root, or any package publish flow.

If the task is to create, validate, pack, publish, or install-check a reusable capability package, use `kw-capability-package` instead.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Flow

1. Read `.kw/project-capabilities.json`.
2. Inspect the detailed source or installed capability package lock entrypoint for the selected capability.
3. Generate a read-only plan with `kw control project-capabilities plan`.
4. Sync generated entries with `kw control project-capabilities sync --write`.
5. Install native agent permissions only after confirmation with `kw control project-capabilities install --write`.

For `workflow-requirements` and `knowledge-writing-policies`, inspect consumer-local `sources[]` and installed capability package sources from `.kw/capability-lock.json`. For `agent-permissions`, consumer config is incremental: shared KW command defaults are inherited and local files add `allow_command_ids`, `confirm_command_ids`, `deny`, `guardrail_ids`, or `custom_prefixes`. Do not copy full knowledge documents into generated agent skills. Generated skills should point to durable `knowledge/**` or `specs/**` sources.
