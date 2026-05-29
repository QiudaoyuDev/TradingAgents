---
name: kw-propose
description: 创建或完善 Knowledge Workshop formal change 的 proposal、design 和 tasks。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-propose/SKILL.md.tmpl source-sha256=d170549c86cd2c8a2a3087e08cd76c9093f6d7a76c98ad8a51de3d065e4680f4 -->

# 提案

当工作需要持久计划、跨文件协调、workflow gates 或可审查 artifacts 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## Shared Knowledge Governance

规划长期 `knowledge/**` 或 `specs/**` 回写前，读取 active Knowledge Workshop runtime 中的 `specs/knowledge-governance.md`，或 `.kw/index/specs.json` 里 `spec_id=knowledge-governance` 的条目。用它判断 fact layer、预期 writeback target，以及重复任务是否真的需要 project skill。

## Control Objective Alignment

写入 `proposal.md`、`design.md` 或 `tasks.md` 前，检查 `.kw/index/specs.json` 中的
`spec_id=control-objective`，并用它作为 `project_goal_alignment` 依据。若缺失，fallback 到
`knowledge/project-map.md`，在 planning artifacts 中记录 fallback，并建议创建
`specs/control-objective.md` 的 follow-up change。目标 spec 是 `mandatory-by-convention`，
当前版本不是 blocking gate。

## 流程

1. 运行 `kw change sync` 并检查 active changes。
2. 在 mutating `kw` 命令前，注意 runtime decision guard 可能按 policy 做 read-only lazy refresh，用于修复缺失、过期、无效或 `current_version` 与 lock 漂移的 advisory cache。也可以显式运行 `kw control update-advisory --consumer-root .` 查看 advisory；两种路径都不是 startup check，也不会 auto-update。
3. 如果任何 `kw` 命令返回 `runtime_update_decision_required`，停止当前操作，向用户报告 current/latest runtime 和 update kind，并询问更新或跳过。跳过时先运行返回的 dismiss command，再重试原命令；major update 必须先做 upgrade planning/migration。
4. 在 change 开始、phase 切换、runtime update 或 dogfood refresh 之后，运行 `kw control bootstrap-reconcile --consumer-root . --write`，或先检查它的 blockers。Reconcile 只从 locks、dependencies 和 managed project capability sources 恢复已声明状态；不得选择新版本或新增未声明 source。普通 mutating `kw change` 命令仍有内置 bootstrap guard，不需要每次都额外手动 reconcile。
5. 复用已命名的 active change，或用 `kw change new --change-id <id> --title "<title>" --workflow-lifecycle <lifecycle> --workflow-profile <profile> --repo <repo> --path <path>` 创建一个。
6. 读取 `runtime.json`，按 active `workflow_lifecycle` 执行；不要假设每个 change 都从 `proposal` 开始。
7. 对 `standard-change`，填写 `proposal.md`，进入 `design`，再填写 `design.md` 和 `tasks.md`。
8. 对 `quick-patch` 或 `ops-task`，确认 change 从 `execution` 开始，保持 planning artifacts 简洁，并把 `tasks.md` 作为 execution checklist。
9. 在 design 和 task planning 阶段填写 design 的 `Knowledge Writeback Plan` / `知识回写计划`。判断是否存在 project-goal reusable knowledge gap 需要长期 `knowledge/**`、`specs/**`、shared policy/skill/template/docs 或 follow-up change 回写。执行前记录可复用判断、现有覆盖、计划落点、目标路径、not-needed category 和 acceptance 对账，避免 acceptance 的 `review-knowledge` 临时补判断。
10. 人读计划和 design 结论遵循 `document-writing` locale selection；读取 English canonical specs 后用选定语言转述结论，并保留 machine contract tokens 原文。
11. 运行 `kw change validate --change <change>` 和 `kw change refresh-requirements --change <change>`。

## 提交时机

把 `proposal`、`design` 和 task artifacts 作为当前 active change 的自有状态维护。提交时机遵循项目约定或 acceptance 后收束。

不要把 `preflight-write` 理解为 proposal/design 阶段的提交要求；它属于 execution 中 managed writes 前的写入门禁。

## Human Gates

如果 decision 需要用户确认，添加匹配的 requirement/tag；当 active lifecycle 有 planning phase 时，在 execution 前停止。用户明确确认后，用 `kw change record-requirement` 记录。

## Shared Surface Check

最终确认 scope 前，检查请求是否触及 generated artifacts、shared guidance、agent skills、locale overlays、runtime checkers、templates 或 cross-consumer behavior。若触及，先追溯 source 再规划写入：`share/knowledge_workshop/templates/**`、`share/knowledge_workshop/locales/**`、generators、checkers、guides、specs 和 tests。Generated `.agents/**`、`.claude/**` 和 `.kw/bin/**` 文件是 outputs，不是 repair sources。
