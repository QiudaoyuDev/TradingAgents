---
name: kw-knowledge-writing-policy
description: 规划并维护 Knowledge Workshop knowledge writing policies。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-knowledge-writing-policy/SKILL.md.tmpl source-sha256=814e38d853dcda43d5f7f9d1903018fa37daa39a75b0094909c2a0cce83aea68 -->

# 知识回写策略

当项目或 capability package 需要约束 `kw change review-knowledge` 如何判断长期事实、选择 shared/consumer 落点并要求 review evidence 字段时使用本 skill。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## Shared Knowledge Governance

修改 knowledge writing policy rules 前，读取 active Knowledge Workshop runtime 中的 `specs/knowledge-governance.md`，或 `.kw/index/specs.json` 里 `spec_id=knowledge-governance` 的条目。用它确保 policy targets 与 shared fact layers、candidate capture、review evidence 和 skill-vs-knowledge boundaries 对齐。

## 流程

1. 读取 `.kw/project-capabilities.json`，存在时读取 `.kw/policies/knowledge-writing.json`。
2. 对 packaged policy，检查 `capability/profile.json` 和计划发布的 `knowledge_writing_policies[]` entrypoints。
3. 保持 policy rules 声明式：selectors、docs、target hints、result guidance、required review fields、result-specific required fields 和 path fields。
4. 不在这里定义 workflow gates；`knowledge-delta-reviewed` 是 KW base requirement。
5. 用 `kw-knowledge-writing-policy-v1` 校验 payload，并验证 `kw change review-knowledge` 会报告 matched policies。

Writing policies 描述知识应该怎么写；它们不决定是否必须做 knowledge review。

对 AI-actionable knowledge，要求后续 agent 足以定位证据和行动的字段：`target_paths`、`knowledge_kind`、`source_basis`、`evidence_links`、`ai_entrypoints`、`writeback_direction` 和 `publishability`。对必须存在的 workspace-relative 路径字段使用 `path_fields`。
