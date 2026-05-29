<!-- kw-doc: {"model":"kw-doc-meta-v1","doc_id":"agents","title":"TradingAgents Agent Entrypoint","locale":"en"} -->

# TradingAgents Agent Entrypoint

<!-- knowledge-workshop:managed:start template=consumer-minimal-v1 version=1.3.1 -->

## Purpose

- This directory is the Knowledge Workshop control plane for `TradingAgents`, using Knowledge Workshop `1.3.1`.
- `AGENTS.md` is the Codex entrypoint; detailed workflows are carried by `.agents/skills/kw-*` skills and the `kw` CLI.

## Start Here

- Before any workspace-bound task, run `kw control hydrate --consumer-root . --write` to restore locked runtime, declared capabilities, generated skills, and policy/knowledge projections; stop on blockers.
- Read `.kw/workspace/workspace.json` first to understand control, managed repo, reference repo, and reference control boundaries.
- Read `.kw/index/changes.json`; when a conversation names a change, read that change's `change.json` and `runtime.json`.
- For Knowledge Workshop changes, use the matching `kw-{explore,propose,apply-change,finish-change,archive-change}` skill.
- For upgrades, capability packages, knowledge baselines, workflow extensions, or project capabilities, use `kw-upgrade`, `kw-capability-package`, `kw-project-capability`, `kw-knowledge-baseline`, or `kw-workflow-extension`.
- Use the domain/action command model: `kw <domain> <action>: kw change <action>, kw control <action>, kw knowledge <action>`.
- When runtime location matters, run `kw control where`.

## Hard Boundaries

- Repository boundaries come only from `.kw/workspace/workspace.json`; reference repositories and reference controls are read-only.
- Formal changes move through the active `workflow_lifecycle`; `standard-change` uses `proposal -> design -> execution -> acceptance`, while short lifecycles project skipped phases explicitly.
- Before writing any managed repo/path, run `preflight-write` through the active kw workflow.
- Verification, knowledge review, and requirement evidence must be recorded by `kw`; do not only state them in chat.
- `hydrate` restores declared/locked artifacts only; it must not be treated as permission to pull latest, upgrade runtime, upgrade dependencies, or mutate undeclared sources.
- Paths written to `.kw/index/**`, `changes/**` evidence, `knowledge/**`, `specs/**`, and generated agent entrypoints must be workspace-unit-relative; keep local absolute paths out of shared collaboration records.

## Collaboration

- Keep durable facts in `changes/**`, `specs/**`, or `knowledge/**`; keep transient local state under `.kw/local/**`.
- Agent collaboration, human-readable file writeback, plans, status updates, conclusions, acceptance summaries, and execution reports follow shared `document-writing` locale selection.
- When reading English canonical specs for a non-English workspace, restate human-facing conclusions in the selected language and keep machine contract tokens unchanged.

## Writeback

- After modifying `changes/**`, `specs/**`, `knowledge/**`, or workspace config, run `kw change validate` and `kw change sync`.
- Business facts belong in `specs/**` or `knowledge/**`, not in the shared Knowledge Workshop runtime.
- Do not commit `.kw/local/**`, runtime caches, credentials, or machine-specific state.

<!-- knowledge-workshop:managed:end -->

<!-- consumer-local:start -->

## Local Constraints

- Add repository, module, verification, deployment, and protected-path rules that are true only for this workspace.

## MCP Server

`opencode-mcp/` 是独立 MCP Server 模块，将 TradingAgents 数据层暴露为 AI 编码助手的工具。

启动方式：
```bash
pip install -e opencode-mcp    # 安装（先确保 tradingagents 已 pip install -e .）
python -m opencode_mcp.server  # 启动 MCP Server（stdio 模式）
```

提供 11 个工具：get_stock_price_data, get_technical_indicator, get_fundamentals,
get_balance_sheet, get_cashflow, get_income_statement, get_ticker_news,
get_global_macro_news, get_insider_transactions, get_stocktwits_sentiment,
get_reddit_discussion。全部零 LLM 依赖，默认使用 yfinance（无需 API Key）。

## Local Writeback

- Add project-specific writeback rules for knowledge, specs, indexes, build outputs, deployment state, or acceptance evidence.

<!-- consumer-local:end -->
