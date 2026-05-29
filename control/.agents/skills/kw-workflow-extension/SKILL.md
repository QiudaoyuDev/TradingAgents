---
name: kw-workflow-extension
description: 规划并维护 local workflow requirements 和 gates。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-workflow-extension/SKILL.md.tmpl source-sha256=6d7c47b2e5cdd5921287c5bb710eb2297a388c67842f2b0731b50546bb88667c -->

# Workflow Extension

当项目需要 default Knowledge Workshop state machine 之外的 local workflow requirements 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 流程

1. 读取 `.kw/policies/workflow-extension.json`。
2. 判断 requirement 是 project-local，还是应进入 shared product。若可复用 lesson 适用于多个 consumer，或已有 shared rule 没能指导行为，停止本地 policy 编辑，并把候选路由到 shared product change。
3. 优先使用 declarative requirements，而不是 custom scripts。
4. 编辑后运行 `kw change validate`。
5. 用 `kw change refresh-requirements --change <change>` 刷新 active changes。

Shared default policy changes 应通过 formal change 在 Knowledge Workshop product repo 中完成。

Knowledge writing rules 属于 `kw-knowledge-writing-policy`，不要写进 workflow extension policy。
