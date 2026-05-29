---
name: kw-explore
description: 读取 Knowledge Workshop 上下文、检查事实并比较方案，不写 managed repositories。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-explore/SKILL.md.tmpl source-sha256=d86c13e2c80702e3f1a6dfdc4b0ee1403dbf440573d282571871cc828b489c19 -->

# 探索

当用户提出问题、要求调查，或在正式 change 前需要 design context 时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 读取顺序

1. 读取 `.kw/workspace/workspace.json`。
2. 在存在时读取 `.kw/index/changes.json` 和 `.kw/index/change-contexts.json`。
3. 如果对话指定 change，读取它的 `change.json`、`runtime.json` 和当前 phase artifacts。
4. 判断 `project_goal_alignment`、reusable knowledge gaps 或 follow-up targets 前，检查 `.kw/index/specs.json` 中的
   `spec_id=control-objective`。若缺失，fallback 到 `knowledge/project-map.md`，并建议创建
   `specs/control-objective.md` 的 follow-up change。
5. 只读取回答问题所需的最小 `specs/**`、`knowledge/**`、代码和文档。

## 规则

- explore 模式下不要写 managed repositories。
- 将 reference repositories 和 reference controls 视为只读。
- 结论必须绑定到文件路径和具体事实。
- 人读结论遵循 `document-writing` locale selection；当事实来自 English canonical specs 时，用选定语言转述结论，并保留 machine contract tokens 原文。
- 在 no-active-change 探索中，不要写 change evidence。若发现 reusable cognition，只输出 learning candidate 或 follow-up change target。
- 如果需要 implementation，在 change 状态清楚后交给 `kw-propose` 或 `kw-apply-change`。
