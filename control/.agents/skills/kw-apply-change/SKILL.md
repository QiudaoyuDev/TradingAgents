---
name: kw-apply-change
description: 在必要 planning gates 和 write preflight 之后执行现有 Knowledge Workshop change 的任务。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-apply-change/SKILL.md.tmpl source-sha256=919144ec36f12019e18994e759af889871352b390d19571273b287c74898559e -->

# 执行 Change

仅在 change 已处于 `execution`，或按 active `workflow_lifecycle` 已准备进入 `execution` 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 写入前

1. 读取 change 的 `change.json`、`runtime.json`、`proposal.md`、`design.md` 和 `tasks.md`。
2. implementation 前检查 `.kw/index/specs.json` 中的 `spec_id=control-objective`。用该目标保持
   implementation path 对齐；若缺失，fallback 到 `knowledge/project-map.md`，并保留创建
   `specs/control-objective.md` 的 follow-up。如果 implementation 改变 `project_goal_alignment`，
   继续前先更新 planning artifacts。
3. 在 mutating `kw` 命令前，注意 runtime decision guard 可能按 policy 做 read-only lazy refresh，用于修复缺失、过期、无效或 `current_version` 与 lock 漂移的 advisory cache。也可以显式运行 `kw control update-advisory --consumer-root .` 查看 advisory；两种路径都不是 startup check，也不会 auto-update。
4. 如果任何 `kw` 命令返回 `runtime_update_decision_required`，写入前停止，向用户报告 runtime update 选择，并在更新或运行返回的 dismiss command 后重试原命令。
5. 开始 execution、phase 切换、runtime update 或 dogfood refresh 之后，运行 `kw control bootstrap-reconcile --consumer-root . --write`，有 blockers 时停止。Reconcile 只恢复已声明状态，不等于允许新增未声明 artifacts、versions 或 capabilities。普通 mutating `kw change` 命令仍有内置 bootstrap guard，不需要每次都额外手动 reconcile。
6. 运行 `kw change validate --change <change>`。
7. 运行 `kw change refresh-requirements --change <change>`。
8. 确认 active lifecycle 需要的 approvals 已记录；`quick-patch` 和 `ops-task` 默认不要求 design-phase approval，除非 policy materializes one。
9. 写入每个 managed repo scope 前运行 `kw change preflight-write --change <change> --repo <repo> --path <path>`。

## 提交时机

managed writes 前使用 `preflight-write`。它是写入门禁，不是 proposal/design 阶段的提交要求。

## 执行

- 只编辑当前任务需要的文件。
- 完成任务后立即勾选 `tasks.md`。
- 用 `kw change checkpoint` 记录 checkpoint。
- 人读进度、状态和 checkpoint summary 遵循 `document-writing` locale selection；English canonical specs 中的结论用选定语言转述，同时保留 protocol tokens 原文。
- 如果 scope 扩大或 execution plan 错误，停止并使用 active lifecycle 允许的 rollback target。`standard-change` 可回到 `design`；`quick-patch` 和 `ops-task` 从 `acceptance` 回到 `execution`。
