# MCP Server: 暴露 TradingAgents 数据层为 OpenCode 工具 — 任务

## Phase 1: Proposal & Design ✓

- [x] 完成 proposal.md
- [x] 完成 design.md
- [x] 等待用户确认后进入 execution

## Phase 2: 环境准备

- [x] 创建 `opencode-mcp/` 目录结构
- [x] 创建 `opencode-mcp/pyproject.toml` — 项目配置 + 依赖声明
- [x] 验证依赖可安装 (`pip install -e .`)

## Phase 3: MCP Server 核心代码

- [x] 创建 `opencode-mcp/src/__init__.py` — 包初始化
- [x] 创建 `opencode-mcp/src/tools.py` — 工具函数实现
  - [x] get_stock_price_data()
  - [x] get_technical_indicator()
  - [x] get_fundamentals()
  - [x] get_balance_sheet() / get_cashflow() / get_income_statement()
  - [x] get_ticker_news() / get_global_macro_news()
  - [x] get_insider_transactions()
  - [x] get_stocktwits_sentiment() / get_reddit_discussion()
- [x] 创建 `opencode-mcp/src/server.py` — MCP Server 入口，注册所有 tool

## Phase 4: 验证

- [x] 冒烟测试：启动 server 并调用每个工具
- [x] 错误处理测试：无效参数、网络异常场景
- [x] 确认 server 通过 stdio 正常响应

## Phase 5: 收尾

- [x] 更新 AGENTS.md 补充 MCP server 入口说明
- [x] 创建 `opencode-mcp/README.md` — 安装与使用文档

## Acceptance Gates

- [x] human-design-approval（用户确认计划）
- [x] human-acceptance-approval（用户验收完成结果）
