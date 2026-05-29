---
name: kw-capability-package
description: Create, validate, package, publish, and install-check reusable capability packages.
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-capability-package/SKILL.md.tmpl source-sha256=e6ec7cdd2e6bff621488d01859abf397df014bb2c4a1b9fe2639f21c748c9570 -->

# Capability Package

Use this skill when a capability has or needs `capability-package.json` and is meant to be installed, locked, or reused by another consumer.

Do not use this skill for local-only project activation. If there is no `capability-package.json` and the task only changes `.kw/project-capabilities.json`, `.kw/project-skills.json`, `.kw/policies/**`, or `.kw/project-agent-permissions.json`, switch to `kw-project-capability`.

## Task-Start Hydration

Before reading or changing a KW workspace, run `kw control hydrate --consumer-root . --write` once and stop on blockers. It restores locked runtime, declared capabilities, generated skills, and policy/knowledge projections only; it must not resolve `latest`, upgrade runtime or dependencies, or add undeclared sources.

## Triage

1. Read the requested package root and look for `capability-package.json`.
2. If the manifest is at the KW workspace root, treat it as legacy/scattered layout: compatible, but new package source should move to `capability-packages/<package-id>/`.
3. If the package source already lives under `capability-packages/<package-id>/`, keep package-only files there and use v2 `recipe` mappings for canonical repo facts.
4. If canonical `knowledge/**`, `specs/**`, or `examples/**` should remain in the repo root, project them through `recipe.source_roots` and `recipe.mappings`; do not duplicate them under the package root.

## Authoring Root

New publishable packages use:

```text
capability-packages/<package-id>/
  capability-package.json
  capability/profile.json
  skills/project-skills.json
  policies/**
  validators/**
  evals/**
```

Root-level `capability-package.json`, `capability/`, and `skills/` remain compatibility input only. Do not create source `payload/**`; `kw control capability pack` owns generated payload staging.

## Commands

- Validate: `kw control capability validate --path capability-packages/<package-id>`
- Pack dry-run: `kw control capability pack --path capability-packages/<package-id> --dry-run`
- Pack staging: `kw control capability pack --path capability-packages/<package-id> --output-dir <dir>`
- Publish dry-run: `kw control capability publish --path capability-packages/<package-id> --dry-run --registry-url <registry>`
- Install check: `kw control capability install --package-tar <staging-dir> --package-id <package-id> --version <version> --overwrite`

Consumer scripts may wrap these commands to fix registry, output directory, or dogfood arguments, but must not reimplement payload selection, checksums, publish, or install verification.

## Verification

Before finishing a package change, record explicit evidence for file selection, redaction, publishability, i18n impact, `validate`, pack dry-run, temporary consumer install, lock contents, generated project skill output, policy/validator entrypoints, and change validation.
