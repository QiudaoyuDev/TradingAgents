# MCP Server: 暴露 TradingAgents 数据层为 OpenCode 工具 — 设计

## 架构

```
opencode-mcp/
├── pyproject.toml          # 依赖管理 + CLI entry point
├── README.md               # 安装与使用说明
├── src/
│   ├── __init__.py
│   ├── server.py           # MCP Server 入口，注册所有 tool
│   └── tools.py            # 工具函数实现（从 tradingagents.dataflows 调用）
└── tests/
    └── test_tools.py       # 工具函数的单元测试
```

### 数据流

```
AI 编码助手 (OpenCode/Claude Code)
       │ 调用 MCP tool (stdio)
       ▼
opencode-mcp MCP Server
       │ import / call
       ▼
tradingagents.dataflows.interface.route_to_vendor()
       │ 按 config 路由
       ├── yfinance 实现 (默认, 无需 API Key)
       └── Alpha Vantage 实现 (需 ALPHA_VANTAGE_API_KEY)
```

### MCP Server 设计

- 使用 Python `mcp` SDK 构建
- stdio 传输协议
- 每个 tool 以 `@server.tool()` 装饰器注册
- 工具函数内部调用 `route_to_vendor()`，复用 TradingAgents 数据层
- 返回格式统一为字符串
- 错误处理：网络异常/无数据/参数校验失败 → 友好错误信息

## 工具定义

### 1. get_stock_price_data
- **用途**: OHLCV 历史价格
- **参数**: symbol(str), start_date(str YYYY-MM-DD), end_date(str YYYY-MM-DD)
- **返回**: CSV 格式 OHLCV
- **实现**: `route_to_vendor("get_stock_data", ...)`

### 2. get_technical_indicator
- **用途**: 技术指标 (rsi, macd, close_50_sma, close_200_sma, close_10_ema, macds, macdh, boll, boll_ub, boll_lb, atr, vwma, mfi)
- **参数**: symbol(str), indicator(str), curr_date(str), look_back_days(int=30)
- **返回**: 指标值 + 用途说明
- **实现**: `route_to_vendor("get_indicators", ...)`

### 3. get_fundamentals
- **用途**: 公司基本面 29 项指标
- **参数**: ticker(str), curr_date(str 可选)
- **返回**: key: value 格式
- **实现**: `route_to_vendor("get_fundamentals", ...)`

### 4-6. 财务报表
- **用途**: 资产负债表 / 现金流量表 / 利润表
- **参数**: ticker(str), freq(str quarterly|annual), curr_date(str 可选)
- **返回**: CSV 格式
- **实现**: `route_to_vendor("get_balance_sheet"|"get_cashflow"|"get_income_statement", ...)`

### 7. get_ticker_news
- **用途**: 个股新闻
- **参数**: ticker(str), start_date(str), end_date(str)
- **返回**: 新闻标题列表
- **实现**: `route_to_vendor("get_news", ...)`

### 8. get_global_macro_news
- **用途**: 全球宏观新闻 (Fed, S&P500, 地缘政治, 央行, 大宗商品)
- **参数**: curr_date(str), look_back_days(int=7), limit(int=10)
- **返回**: 格式化新闻列表
- **实现**: `route_to_vendor("get_global_news", ...)`

### 9. get_insider_transactions
- **用途**: 内部交易数据
- **参数**: ticker(str)
- **返回**: CSV 格式
- **实现**: `route_to_vendor("get_insider_transactions", ...)`

### 10. get_stocktwits_sentiment
- **用途**: StockTwits 社交情绪
- **参数**: ticker(str), limit(int=30)
- **返回**: 用户消息列表
- **实现**: `stocktwits.fetch_stocktwits_messages(ticker, limit)`

### 11. get_reddit_discussion
- **用途**: Reddit 讨论
- **参数**: ticker(str), limit(int=20)
- **返回**: 帖子列表
- **实现**: `reddit.fetch_reddit_posts(ticker, limit)`

## 依赖

```toml
dependencies = [
    "mcp>=1.0.0",
    "yfinance>=0.2.63",
    "stockstats>=0.6.5",
    "pandas>=2.3.0",
    "requests>=2.32.4",
    "pytz>=2025.2",
]
```

## 决策

- 人工决策状态：等待用户确认执行计划后进入 execution
- 待确认事项：无 — 方案已在上轮分析中确认
- 已确认结论：Tier 1 数据工具先行，不含 LLM Agent 层
- 证据：上轮分析的架构拆解

## Control Objective Alignment

- `control_objective_source`: 项目分析结论 — 将数据层输出为 MCP 工具
- `project_goal_alignment`: 基础设施输出，不改变核心框架逻辑，提升框架可消费性

## Spec Impact

- `affected_specs`: 无现有 specs 受影响
- `expected_spec_delta`: 无
- `no_spec_change_reason`: 独立模块 opencode-mcp/，不修改 tradingagents/ 核心包

## 知识回写计划

- 可复用判断: TradingAgents 的 route_to_vendor 抽象可直接被 MCP 工具层复用
- 现有覆盖: 无需新增 knowledge
- 计划落点: 不落盘 — MCP 集成是一次性输出，不产生新业务知识
- 目标路径: 无
- 不回写理由: one-off — 不改核心业务逻辑
- acceptance 对账: 验收时确认工具可正常调用

## 风险

- yfinance 反爬策略变化可能导致数据获取失败（已有 yf_retry 重试机制）
- MCP Python SDK 版本兼容性（锁定 >=1.0.0）
- 内网环境可能无法直接访问 PyPI / Yahoo Finance（需要配置代理或镜像）

## 回滚

删除 `opencode-mcp/` 目录，回退 AGENTS.md 的修改。

## 验收标准

1. `cd opencode-mcp && pip install -e .` 安装成功
2. `python -m opencode_mcp.server` 启动无报错
3. 调用 get_stock_price_data("AAPL", "2026-01-01", "2026-05-28") 返回正确 CSV
4. 调用 get_fundamentals("AAPL") 返回基本面数据
5. 调用 get_technical_indicator("AAPL", "rsi", "2026-05-28", 30) 返回 RSI 值
6. 所有工具对无效参数返回友好错误而非崩溃

## 验证计划

1. 单元测试：mock route_to_vendor 验证每个工具的参数传递
2. 集成测试：实际调用 yfinance 获取 AAPL 数据
3. 手动测试：启动 MCP server 并通过 inspector 调用每个 tool
