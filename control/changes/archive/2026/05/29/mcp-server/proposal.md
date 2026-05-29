# MCP Server: 暴露 TradingAgents 数据层为 OpenCode 工具

## 目标

在项目根目录创建 `opencode-mcp/` 模块，通过 MCP (Model Context Protocol) Server 将 TradingAgents 的数据采集层（dataflows/）暴露为 OpenCode / Claude Code 可直接调用的工具，使 AI 编码助手无需另外接入 LLM 即可获取实时股票数据、技术指标、基本面、新闻等金融数据。

## 范围

### 受管仓库

- `TradingAgents`

### 影响路径

- `opencode-mcp/` — 新目录，MCP server 代码
- `opencode-mcp/pyproject.toml` — 依赖管理
- `opencode-mcp/README.md` — 安装与使用说明
- `AGENTS.md` — 可选：补充 MCP server 的使用入口

### 功能范围

提供以下 MCP 工具（Tier 1 — 纯数据，零 LLM 依赖）：

1. `get_stock_price_data` — OHLCV 历史价格
2. `get_technical_indicator` — 技术指标（RSI, MACD, SMA, EMA, Bollinger, ATR, VWMA, MFI 等 15 种）
3. `get_fundamentals` — 公司基本面（29 项关键指标）
4. `get_balance_sheet` — 资产负债表
5. `get_cashflow` — 现金流量表
6. `get_income_statement` — 利润表
7. `get_ticker_news` — 个股新闻
8. `get_global_macro_news` — 全球宏观新闻（Fed, 地缘政治, 大宗商品等）
9. `get_insider_transactions` — 内部交易数据
10. `get_stocktwits_sentiment` — StockTwits 社交情绪
11. `get_reddit_discussion` — Reddit 讨论

## 非目标

- 不包含 TradingAgents 的 LLM Agent 层（分析师、研究员、交易员等）
- 不修改 `tradingagents/` 核心包的现有代码
- 不要求用户配置 LLM API Key
- 不暴露 LangGraph 图编排功能
- 不包含回测（backtrader）功能

## 约束

- MCP Server 使用 stdio 传输协议（OpenCode / Claude Code 原生支持）
- 数据获取复用 `tradingagents.dataflows.interface.route_to_vendor`，不重新实现数据采集
- 最小依赖集：`yfinance`, `stockstats`, `pandas`, `requests`, `pytz`, `mcp`
- Python >= 3.10
- 所有工具函数必须包含完整的中文+英文参数描述和返回格式说明

## Control Objective Alignment

- `control_objective`: 将 TradingAgents 数据层能力输出为标准化 MCP 工具，降低 AI 编码助手获取金融数据的门槛
- `project_goal_alignment`: 本 change 属于基础设施输出层建设，不改变核心框架的业务逻辑，但显著提升框架的可消费性

## Spec Impact

- `affected_specs`: 无现有 specs 受影响；新增 `opencode-mcp/` 作为独立模块
- `expected_spec_delta`: 无
- `no_spec_change_reason`: 本次不修改 tradingagents 核心包的行为和接口
