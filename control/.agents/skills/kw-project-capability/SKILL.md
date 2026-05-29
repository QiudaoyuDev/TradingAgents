---
name: kw-project-capability
description: 规划、同步并安装 project-level agent capabilities。
---

<!-- knowledge-workshop:generated canonical-skill source=share/knowledge_workshop/templates/agent-skills/kw-project-capability/SKILL.md.tmpl source-sha256=9f94af53984af2962d1b201795c8a2f6e401cd537a9d7b64c789b26f381dc36a -->

# Project Capability

当项目需要 project-level skills、workflow requirements、knowledge writing policies、agent permissions 或 update-advisory 配置时使用本 skill。

Project capabilities 默认合规启用。不要新增普通 `enabled:false` 开关；用 declared sources、已安装 capability package lock，以及 `kw control project-capabilities plan` 的 `inherited`、`managed`、`not_configured`、`blocked`、`override_disabled` 状态解释行为。

本 skill 只负责 project-local activation：`.kw/project-capabilities.json`、`.kw/project-skills.json`、`.kw/policies/**`、`.kw/project-agent-permissions.json` 和 `.kw/kw-update-policy.json`。Local-only capabilities 不需要 `capability-package.json`、`capability/profile.json`、package root 下的 `skills/project-skills.json`，也不需要 package publish flow。

如果任务是创建、验证、打包、发布或安装验证 reusable capability package，改用 `kw-capability-package`。

## 任务开始 Hydration

读取或修改 KW workspace 前，先运行 `kw control hydrate --consumer-root . --write` 一次；出现 blockers 即停止。它只恢复 locked runtime、declared capabilities、generated skills 和 policy/knowledge projections；不得解析 `latest`、升级 runtime 或 dependencies，也不得新增 undeclared sources。

## 流程

1. 读取 `.kw/project-capabilities.json`。
2. 检查所选 capability 的详细 source 或已安装 capability package lock entrypoint。
3. 用 `kw control project-capabilities plan` 生成 read-only plan。
4. 用 `kw control project-capabilities sync --write` 同步 generated entries。
5. 仅在确认后用 `kw control project-capabilities install --write` 安装 native agent permissions。

对 `workflow-requirements` 和 `knowledge-writing-policies`，检查 consumer-local `sources[]` 与 `.kw/capability-lock.json` 中的已安装 capability package sources。对 `agent-permissions`，consumer 配置只声明增量：shared KW command defaults 默认继承，本地文件添加 `allow_command_ids`、`confirm_command_ids`、`deny`、`guardrail_ids` 或 `custom_prefixes`。不要把完整 knowledge documents 复制进 generated agent skills。Generated skills 应指向持久的 `knowledge/**` 或 `specs/**` sources。
