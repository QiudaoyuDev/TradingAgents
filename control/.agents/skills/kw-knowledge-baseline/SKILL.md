---
name: kw-knowledge-baseline
description: 规划、建议并重建 Knowledge Workshop 项目知识基线。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-knowledge-baseline/SKILL.md.tmpl source-sha256=70d8a0d0e4720ba62009856e0e9a1518216d6d68e02d73e5e08520f8e8e08f1a -->

# 知识基线

当 consumer 跳过 onboarding、需要重建初始知识地图，或需要获得 `knowledge/**` 与 `specs/**` 演进建议时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## Shared Knowledge Governance

建议或重建 durable maps 时，读取 active Knowledge Workshop runtime 中的 `specs/knowledge-governance.md`，或 `.kw/index/specs.json` 里 `spec_id=knowledge-governance` 的条目。用它在生成的 baseline knowledge 中保持 fact-layer boundaries、writeback direction、publishability 和 index semantics。

## 读取顺序

1. 读取 `.kw/workspace/workspace.json`。
2. 存在时读取 `.kw/index/knowledge.json`、`.kw/index/specs.json` 和 `.kw/index/changes.json`。
3. 存在时读取 `knowledge/project-map.md`、`knowledge/writeback-playbook.md`、`knowledge/repos/**` 和 `knowledge/references/**`。
4. 检查 workspace inventory 声明的 managed repositories 和 read-only references。
5. 当 operator 提供 `kw-onboarding-answers-v1` 文件时读取它。

## 模式

- 使用 `kw control knowledge-baseline plan --consumer-root .` 生成只读 baseline plan。
- 使用 `kw control knowledge-baseline advise --consumer-root .` 生成不写文件的 evolution advice。
- 只有在 active change 内且已经完成 `preflight-write` 后，才使用 `kw control knowledge-baseline regenerate --consumer-root . --change <change> --write`。

## 规则

- 生成有用的地图，而不是空模板：purpose、audience、capability map、repo/reference map、verification entrypoints、writeback direction、publishability 和 open questions。
- 让地图对 AI 可行动：尽量用 workspace-relative 路径写出 concrete evidence links、AI entrypoints、likely change targets 和 verification entrypoints。
- 生成的 baseline 标题和正文遵循 consumer `artifact_locale`。路径、命令、JSON keys、model/schema names、source labels 和 publishability enum values 保持协议原文。
- 将结论标记为 `confirmed-by-user`、`evidence-backed`、`inferred` 或 `open-question`。
- 当 managed repository 的 `roles` 包含 `control` 或 `self` 时，将其作为 control-plane boundary map，而不是普通 product source。记录 `roles`、`boundary_class`、`summary_mode`、stable entrypoints、write boundaries、verification entrypoints 和 open questions。
- 不要把 `.kw/index/**`、`.kw/local/**`、`.agents/**`、`.claude/**`、`references/knowledge/**`、`references/capabilities/**`、`changes/archive/**` 或 generated `knowledge/project-map.md` 当作普通 project knowledge sources 递归总结。
- reference repositories 和 reference controls 只读；除非用户确认采纳，不要把它们变成本项目事实。
- 业务事实保存在 consumer `knowledge/**` 或 `specs/**`；不要复制进本 skill。
- 不要把 generated `.agents/**`、`.claude/**` 或 `.kw/bin/**` 文件当作产品源手写补丁。修 shared baseline 行为时，追溯并更新 `share/knowledge_workshop/templates/**`、`share/knowledge_workshop/locales/**`、runtime generators/checkers、specs、guides 和 tests。
- capability package 发布是独立 package 步骤，由 `kw control capability` 处理；baseline advice 可以建议 `public`、`consumer-public`、`restricted` 或 `secret` 分类。
