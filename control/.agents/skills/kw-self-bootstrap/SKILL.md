---
name: kw-self-bootstrap
description: 将项目目标相关的可复用认知和元规则候选审查为可并入当前 change 或长期资产的学习候选。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-self-bootstrap/SKILL.md.tmpl source-sha256=137c4312e12eedeee6304aeaecc8f878943d64e1d67e506292dfecbf51289728 -->

# 自举反馈

当项目目标相关任务暴露可复用认知，并可能改变未来 agent 判断边界、执行边界、workflow rule、shared/local ownership decision、generated-surface source tracing 或 durable writeback target 时使用本 skill。触发点不再限定为改代码、用户纠错、失败、workaround 或阻塞；review、产品分析、行业研究、运营排障、架构判断、流程优化和领域建模都可能产生候选，前提是该认知可复用、当前知识未覆盖、稳定且有 evidence。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## Shared Knowledge Governance

为 reusable cognition 或 meta-rule 选择 durable target 前，读取 active Knowledge Workshop runtime 中的 `specs/knowledge-governance.md`，或 `.kw/index/specs.json` 里 `spec_id=knowledge-governance` 的条目。用它区分 shared-base、consumer-local、contributor-artifact 和 project-skill boundaries，避免创建 standalone one-spec skill。

## Control Objective Alignment

分类 `project_goal_alignment` 前，检查 `.kw/index/specs.json` 中的
`spec_id=control-objective`。若缺失，fallback 到 `knowledge/project-map.md`，并包含创建
`specs/control-objective.md` 的 follow-up。目标 spec 是 `mandatory-by-convention`，
当前版本不是 blocking gate。

## 流程

1. 停止错误或受阻动作，并隔离当前污染，例如不需要的 change、脏文件、失败命令副作用或错误 scope 扩大。
2. 如果没有 active change，不要写 change evidence。用相同 routing fields 输出 no-active-change
   learning candidate 或 follow-up change target，然后等待 formal change 再 durable writeback。
3. 读取 active change 的 `change.json`、`runtime.json`、matched requirements 和当前 `knowledge_delta_review`；只重新锚定相关入口，例如 `AGENTS.md`、workspace facts、当前 skill，以及适用的 shared/local policies。
4. 写出 learning candidate：`project_goal_alignment`、`observed_knowledge_gap`、`reuse_context`、`evidence_basis`、`recommended_target`、`writeback_decision`、human merge decision、follow-up change or TODO 和 conclusion。当候选可能成为 `kw-self-growth-proposal-v0` 时，同时分类 `self_growth_level`、`target.target_kind`、`evidence_refs`、`eval_cases`、`human_approval` 和 `proposal_only`。当 `review-knowledge` fields 判断存在 reusable project-goal knowledge 时，先把该 review 升级为 learning candidate，再进行 durable writeback。
5. 将候选分成 one-off、reusable lesson 或 meta-rule candidate。meta-rule candidate 必须说明改变哪类未来判断边界或执行边界；lesson 只解释可复用事实或做法。
6. 人类明确接受前，不要把候选并入当前 change。接受后先更新 owning scope、design、tasks 和 requirements，再写入 durable surface；拒绝或延期时记录 follow-up 或 not-needed decision。
7. 候选清楚后再选择落点：current fix、项目 knowledge/runbook、script、project skill、workflow requirement、knowledge writing policy、shared Knowledge Workshop product、follow-up change 或不沉淀。
8. 对 accepted meta-rule，先选择 owning canonical source，再改 generated output：spec、workflow policy、knowledge-writing policy、canonical skill guidance、test gate、project capability 或 follow-up change。
9. 将 meta-rule 绑定 verification surface。它必须有 policy field、workflow requirement、generated skill trigger、test assertion 或 explicit follow-up gate；不要只留下抽象建议。
10. 如果落点是 project-local workflow 或 writing policy，使用 `kw-workflow-extension` 或 `kw-knowledge-writing-policy`。如果落点是 project skill，只产出候选，写入交给 `kw-project-capability`。
11. 如果问题可跨 consumer 复用，或已有 shared rule 没能指导行为，优先使用 shared product change，而不是 consumer-local policy。
12. 用泛化后的 learning candidate 字段和 durable routing fields 记录 `self-bootstrap-review` 与 `review-knowledge` evidence；不要再使用 root-cause depth 或 budget 字段。

## Self-growth Level Classification

- `L0`: observation 或 no-op；记录为什么不需要 durable candidate 或 writeback。
- `L1`: learning candidate；只记录 candidate、evidence 和 review，不修改 stable assets。
- `L2`: human-scoped guidance change；只能在 formal change 和 human merge decision 后更新 knowledge、specs、docs 或 skill guidance。
- `L3`: eval-gated capability behavior；merge 前要求 `eval_cases` 和 evidence，且不扩大 execution authority。
- `L4`: approval-gated execution or control surface；accepted 或 merged status 前要求 Eval/Evidence 和 `human_approval`。
- `L5`: autonomous or platform self-modification proposal；保持 `proposal_only`，要求 `human_approval`，并且绝不记录为 merged。

## 主动 Shared Review

- 当可复用 project-goal cognition 涉及 generated artifacts、shared guidance、agent skills、locale overlays、runtime checkers、templates 或 cross-consumer behavior 时，不等用户纠错也要主动触发本 review。
- 对 generated `.agents/**`、`.claude/**`、`.kw/bin/**`、template-rendered 或 locale-rendered output，选择修复落点前先追溯 canonical source：`share/knowledge_workshop/templates/**`、`share/knowledge_workshop/locales/**`、generators、checkers、guides、specs 和 tests。
- 用户纠错只是 fallback trigger，不是 prerequisite。agent 在自己的迭代中发现同类可复用认知时，也要写出同样的 learning candidate。
- 相关时在 `evidence_basis` 或 `writeback_decision` 中记录 shared-source tracing：本 review 是否由 agent 主动触发、检查过哪个 shared source、generated artifact source、rule or skill gap、selected repair target 和 scope-classification basis。
- 如果 selected target 是 shared rule 或 skill，走 shared product change，并更新 canonical template、locale overlays 和 tests。不要把 generated skill copies 当成 source of truth 手写。

## 边界

- 不要把 business rules 写进 generated agent skills。
- 不要把 chat text 当成 `record-requirement`、`verify` 或 `review-knowledge` 的替代。
- 不要依赖 automatic language detection 识别反馈；使用 explicit evidence、failed commands、verification results 和 workflow requirements。
- 不要把每个问题都沉淀成 durable asset；一次性偏好和局部澄清可以以 `not-needed` 结束。
- 不要自动扩大当前 change。候选要改变 scope、tasks、scripts、skills、knowledge 或 shared product behavior 前，必须有人类 merge decision。
- 不要把本 skill 扩写成事故日志；应更新 durable knowledge、scripts、capability routing、policy fields、specs、tests 或 follow-up TODO。
