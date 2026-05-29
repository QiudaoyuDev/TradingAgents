---
name: kw-archive-change
description: 在验证完成后归档已完成的 Knowledge Workshop change。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-archive-change/SKILL.md.tmpl source-sha256=5403cdb6c0c1e1c972cf06b8d7d602b023eb86f8e27e81487c1ed9687860c079 -->

# 归档 Change

仅对已 completed 的 change 使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 流程

1. 运行 `kw change validate --change <change>`。
2. 确认 change status 是 `completed`。
3. 运行 `kw change archive-sync --change <change>`。
4. 报告 archive path 和任何 validation warnings。
