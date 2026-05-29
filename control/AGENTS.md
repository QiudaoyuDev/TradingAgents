<!-- kw-doc: {"model":"kw-doc-meta-v1","doc_id":"agents","title":"TradingAgents Agent 入口","locale":"zh-CN","canonical_path":"AGENTS.md"} -->

# TradingAgents Agent 入口

<!-- knowledge-workshop:managed:start template=consumer-minimal-v1 version=1.3.1 -->

## 用途

- 本目录是 `TradingAgents` 的 Knowledge Workshop 控制面，使用 Knowledge Workshop `1.3.1`。
- `AGENTS.md` 是 Codex 入口；详细工作流由 `.agents/skills/kw-*` skills 和 `kw` CLI 承载。

## 先读这里

- 任何 workspace-bound task 前，运行 `kw control hydrate --consumer-root . --write`，恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；有 blockers 即停止。
- 先读 `.kw/workspace/workspace.json`，理解 control、managed repo、reference repo 和 reference control 边界。
- 再读 `.kw/index/changes.json`；当对话点名某个 change 时，读取该 change 的 `change.json` 和 `runtime.json`。
- Knowledge Workshop changes 使用匹配的 `kw-{explore,propose,apply-change,finish-change,archive-change}` skill。
- 升级、capability packages、knowledge baselines、workflow extensions 或 project capabilities 使用 `kw-upgrade`、`kw-capability-package`、`kw-knowledge-baseline`、`kw-workflow-extension` 或 `kw-project-capability`。
- 使用 domain/action command model：`kw <domain> <action>`；当前 agent runtime domains 包括 `change` 和 `control`。
- 需要确认 runtime 位置时，运行 `kw control where`。

## 硬边界

- 仓库边界只来自 `.kw/workspace/workspace.json`；reference repositories 和 reference controls 只读。
- Formal changes 按 active `workflow_lifecycle` 流转；`standard-change` 使用 `proposal -> design -> execution -> acceptance`，短 lifecycle 必须显式投影 skipped phases。
- 写入任何 managed repo/path 前，通过 active kw workflow 执行 `preflight-write`。
- Verification、knowledge review 和 requirement evidence 必须由 `kw` 记录；不要只在聊天里说明。
- `hydrate` 只恢复 declared/locked artifacts；不得把它当作 pull latest、升级 runtime、升级 dependencies 或修改 undeclared sources 的许可。
- 写入 `.kw/index/**`、`changes/**` evidence、`knowledge/**`、`specs/**` 和 generated agent entrypoints 的路径必须是 workspace-unit-relative；不要把本机绝对路径写入共享协作记录。

## 协作

- 持久事实放在 `changes/**`、`specs/**` 或 `knowledge/**`；临时本地状态放在 `.kw/local/**`。
- Agent 协作、人读文件回写、计划、状态更新、结论、验收说明和执行汇报语言遵循 shared `document-writing` 的 locale selection。
- 读取 English canonical specs 后，面向中文 workspace 的人读结论用中文转述；paths、commands、JSON keys、schema/model names、enum values 和 API names 保持协议原文。

## 回写

- 修改 `changes/**`、`specs/**`、`knowledge/**` 或 workspace config 后，运行 `kw change validate` 和 `kw change sync`。
- 业务事实属于 `specs/**` 或 `knowledge/**`，不要写入 shared Knowledge Workshop runtime。
- 不要提交 `.kw/local/**`、runtime caches、credentials 或机器相关状态。

<!-- knowledge-workshop:managed:end -->

<!-- consumer-local:start -->

## 本地约束

- 在这里补充只适用于本 workspace 的仓库、模块、验证、部署和受保护路径规则。

## 本地回写

- 在这里补充项目特定的 knowledge、specs、indexes、build outputs、deployment state 或 acceptance evidence 回写规则。

<!-- consumer-local:end -->
