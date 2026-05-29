# opencode-mcp

将 TradingAgents 数据层暴露为 MCP (Model Context Protocol) 工具，供 OpenCode / Claude Code 等 AI 编码助手直接调用。

**不需要配置任何 LLM API Key。** AI 编码助手使用自己的 LLM 能力来解释数据，TradingAgents 只提供数据获取层。

## 安装

### 前置要求

- Python >= 3.10
- 项目根目录的 `tradingagents` 包已安装（`pip install -e .`）

### 安装

```bash
# 从项目根目录
pip install -e opencode-mcp

# 验证安装
python -m opencode_mcp.server --help
```

## 使用

### 直接运行（stdio 模式，供 AI 编码助手使用）

```bash
python -m opencode_mcp.server
```

### OpenCode 配置

在 `opencode.json` 中添加：

```json
{
  "mcp_servers": {
    "tradingagents-data": {
      "type": "python",
      "command": "python",
      "args": ["-m", "opencode_mcp.server"]
    }
  }
}
```

### Claude Code 配置

在 `~/.claude/settings.json` 中添加：

```json
{
  "mcpServers": {
    "tradingagents-data": {
      "command": "python",
      "args": ["-m", "opencode_mcp.server"]
    }
  }
}
```

## 可用工具

| # | 工具 | 描述 | 参数 |
|---|------|------|------|
| 1 | `get_stock_price_data` | OHLCV 股票历史价格 | symbol, start_date, end_date |
| 2 | `get_technical_indicator` | 技术指标(rsi/macd/sma/ema/boll/atr/vwma/mfi 等) | symbol, indicator, curr_date, look_back_days |
| 3 | `get_fundamentals` | 公司基本面(29 项指标) | ticker, curr_date |
| 4 | `get_balance_sheet` | 资产负债表 | ticker, freq, curr_date |
| 5 | `get_cashflow` | 现金流量表 | ticker, freq, curr_date |
| 6 | `get_income_statement` | 利润表 | ticker, freq, curr_date |
| 7 | `get_ticker_news` | 个股新闻 | ticker, start_date, end_date |
| 8 | `get_global_macro_news` | 全球宏观新闻 | curr_date, look_back_days, limit |
| 9 | `get_insider_transactions` | 内部交易数据 | ticker |
| 10 | `get_stocktwits_sentiment` | StockTwits 社交情绪(无需 API Key) | ticker, limit |
| 11 | `get_reddit_discussion` | Reddit 讨论(无需 API Key) | ticker, limit |

## 数据源

默认使用 **yfinance**（无需 API Key）。可通过环境变量 `ALPHA_VANTAGE_API_KEY` 切换到 Alpha Vantage 数据源。

## 示例（AI 编码助手的用法）

用户提问："帮我分析 AAPL 股票"

AI 编码助手内部调用链（由 AI 自动决定顺序）：
1. `get_stock_price_data("AAPL", "2026-01-01", "2026-05-28")` → 获取价格走势
2. `get_fundamentals("AAPL")` → 获取基本面
3. `get_technical_indicator("AAPL", "rsi", "2026-05-28", 30)` → RSI 指标
4. `get_technical_indicator("AAPL", "macd", "2026-05-28", 30)` → MACD 指标
5. `get_ticker_news("AAPL", "2026-05-20", "2026-05-28")` → 近期新闻
6. AI 综合以上数据生成分析报告

## 依赖

- `mcp>=1.0.0` — MCP Python SDK
- `yfinance>=0.2.63` — Yahoo Finance 数据
- `stockstats>=0.6.5` — 技术指标计算
- `pandas>=2.3.0` — 数据处理
- `requests>=2.32.4` — HTTP 请求
- `pytz>=2025.2` — 时区处理
- `tradingagents`（项目根包，数据层复用）
