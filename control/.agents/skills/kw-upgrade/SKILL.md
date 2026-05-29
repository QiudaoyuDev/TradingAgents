---
name: kw-upgrade
description: 规划并执行 Knowledge Workshop consumer upgrades。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-upgrade/SKILL.md.tmpl source-sha256=a2ce89d56b19375725751c00ca5cefe02d095f3f5ae1789a4f9fd55b41957aa3 -->

# Upgrade

当 consumer workspace 需要 Knowledge Workshop version update 或 entrypoint refresh 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 流程

1. 读取 `.kw/workspace/workspace.json` 和 `.kw/kw-lock.json`。
2. 运行 `kw control update-advisory --consumer-root .` 做 read-only update check。
3. 如果其他 `kw` 命令返回 `runtime_update_decision_required`，把它当作 agent-facing 用户决策：报告 current/latest/update kind，然后更新或运行返回的 dismiss command，再重试原命令。
4. 运行 `kw control upgrade-plan --consumer-root . --to <version|latest>`。
5. 对 major upgrades，写入前创建 migration change。
6. 用 `kw control update --consumer-root . --version <version> --yes` 执行。
7. 用 `kw change validate` 和 `kw change sync` 验证。
