---
name: kw-finish-change
description: 通过记录 verification、knowledge review 和 finish evidence 完成 Knowledge Workshop acceptance。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-finish-change/SKILL.md.tmpl source-sha256=1c839249426ab516a9c4d85607949f41b4bf13f102818f4ddddcd22f75eaedbd -->

# 完成 Change

当 implementation tasks 已完成，change 需要 acceptance 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## Shared Knowledge Governance

执行 project-goal knowledge gap scan 前，读取 active Knowledge Workshop runtime 中的 `specs/knowledge-governance.md`，或 `.kw/index/specs.json` 里 `spec_id=knowledge-governance` 的条目。用它作为 fact layers、writeback routing、candidate/review evidence 和 skill-vs-knowledge boundaries 的 shared source。

## Control Objective Alignment

`review-knowledge` 前检查 `.kw/index/specs.json` 中的 `spec_id=control-objective`。
`project_goal_alignment` 字段必须引用该目标，或说明目标缺失且已使用
`knowledge/project-map.md` 作为 fallback。缺少 `specs/control-objective.md` 应产生
follow-up 建议，当前版本不是 blocking gate。

## 流程

1. 运行 `kw change validate --change <change>`。
2. 在 mutating acceptance 命令前，注意 runtime decision guard 可能按 policy 做 read-only lazy refresh，用于修复缺失、过期、无效或 `current_version` 与 lock 漂移的 advisory cache。也可以显式运行 `kw control update-advisory --consumer-root .` 查看 advisory；两种路径都不是 startup check，也不会 auto-update。
3. 进入 acceptance、runtime update 或 dogfood refresh 之后，运行 `kw control bootstrap-reconcile --consumer-root . --write`，有 blockers 时停止。普通 mutating `kw change` 命令仍有内置 bootstrap guard，不需要每次都额外手动 reconcile。
4. 如果任何 `kw` 命令返回 `runtime_update_decision_required`，停止 acceptance 工作，询问用户更新或跳过，并只在更新或 dismiss 后重试。
5. finish 前确认 `tasks.md` 没有未完成 checkbox。
6. 运行 `design.md` 中承诺的 verification commands。
7. 用 `kw change verify` 记录每个有意义的 verification。
8. `review-knowledge` 前执行 project-goal knowledge gap scan：列出本轮关键判断，检查现有 `knowledge/**`、`specs/**` 和已安装 capability package entrypoints 是否覆盖，再判断每个可复用、稳定、可验证 gap 应该 `created-new`、`updated-existing`、follow-up 或 `not-needed`。
9. 查看 matched knowledge writing policies，并用 required fields 记录 `kw change review-knowledge`。所有结果（包括 `not-needed`）都必须填写 durable routing fields（`reusable_lesson_review`、`reusable_lesson_decision`、`writeback_target`、`decision_basis`、`followup_change_or_todo`）和 project-goal fields（`project_goal_alignment`、`observed_knowledge_gap`、`reuse_context`、`evidence_basis`、`recommended_target`、`writeback_decision`）。对 `created-new` 或 `updated-existing`，还要记录 target paths、source basis、evidence links、AI entrypoints、writeback direction、publishability 和 `applicable_scenarios` 等 AI 可行动字段。对 `not-needed`，将 `not_needed_category` 设为 `already-covered`、`one-off`、`unverified`、`sensitive`、`human-deferred` 或 `out-of-project-goal`；`already-covered` 必须在 `not_needed_basis` 给出现有覆盖路径。
10. 当 active `workflow_lifecycle` 尚未到达 `acceptance` 时，用 `kw change enter-phase --change <change> --to acceptance` 进入 acceptance。
11. 检查 `runtime.json` 中所有 pending acceptance requirements；先完成所有 agent 可执行 hard gate，包括 local package dogfood 这类 `verification_requirement`，再等待人工验收。
12. 如果 `roadmap-closure-review` 仍 pending，先确认 roadmap 行已更新，并用 `kw change record-requirement --requirement-id roadmap-closure-review` 记录，再请求人工验收。
13. 向用户报告完成结果，包括实现摘要、使用的 lifecycle、验证结果、knowledge review、dogfood 或其他 acceptance gate 结果，以及剩余 blocker；报告遵循 `document-writing` locale selection，并用选定语言转述 English canonical spec 结论；然后等待新的事后验收回复。
14. 只能根据完成结果报告之后的回复记录 `human-acceptance-approval`。不要复用 design、execution、finish、archive 或 commit 的事前授权。summary 必须包含 `completed_result_summary=`、`agent_gates_completed=`、`human_response_after_result=` 和 `conclusion=`。
15. 运行 `kw change close --change <change> --archive --sync`。
16. 如果仍有 blockers，处理它们或记录无法完成的原因。
