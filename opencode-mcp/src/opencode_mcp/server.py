"""MCP Server — exposes TradingAgents data layer as AI coding assistant tools.

Usage:
    # Install the package (from project root)
    pip install -e opencode-mcp

    # Run as stdio server (for OpenCode / Claude Code)
    python -m opencode_mcp.server
    # or via the installed command
    opencode-mcp

OpenCode/Claude Code configuration (opencode.json):
    {
        "mcp_servers": {
            "tradingagents-data": {
                "type": "python",
                "command": "python",
                "args": ["-m", "opencode_mcp.server"]
            }
        }
    }
"""

import sys

# Import tools — each is an async function that wraps route_to_vendor()
from opencode_mcp.tools import (
    get_stock_price_data,
    get_technical_indicator,
    get_fundamentals,
    get_balance_sheet,
    get_cashflow,
    get_income_statement,
    get_ticker_news,
    get_global_macro_news,
    get_insider_transactions,
    get_stocktwits_sentiment,
    get_reddit_discussion,
)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "ERROR: mcp package not installed. Run: pip install 'mcp>=1.0.0'",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Create MCP server
# ---------------------------------------------------------------------------
mcp = FastMCP(
    "tradingagents-data",
    instructions="TradingAgents 金融数据 MCP 工具 — 股票价格/技术指标/基本面/新闻/社交情绪。所有工具无需 API Key（默认使用 yfinance）。",
)


# ---------------------------------------------------------------------------
# Register tools
# ---------------------------------------------------------------------------

@mcp.tool(
    name="get_stock_price_data",
    description="获取股票 OHLCV 历史价格数据。参数: symbol=股票代码(如 AAPL), start_date=开始日期(YYYY-MM-DD), end_date=结束日期(YYYY-MM-DD)。返回 CSV 格式 OHLCV。",
)
async def tool_get_stock_price_data(
    symbol: str,
    start_date: str,
    end_date: str,
) -> str:
    """Get OHLCV stock price history."""
    return await get_stock_price_data(symbol, start_date, end_date)


@mcp.tool(
    name="get_technical_indicator",
    description="获取技术指标。支持: rsi, macd, macds, macdh, close_50_sma, close_200_sma, close_10_ema, boll, boll_ub, boll_lb, atr, vwma, mfi。参数: symbol=股票代码, indicator=指标名, curr_date=交易日(YYYY-MM-DD), look_back_days=回溯天数(默认30)。返回日期序列值+用途说明。",
)
async def tool_get_technical_indicator(
    symbol: str,
    indicator: str,
    curr_date: str,
    look_back_days: int = 30,
) -> str:
    """Get technical indicator values."""
    return await get_technical_indicator(symbol, indicator, curr_date, look_back_days)


@mcp.tool(
    name="get_fundamentals",
    description="获取公司基本面数据(29项指标)。参数: ticker=股票代码, curr_date=当前日期(可选)。返回市值/PE/EPS/Beta/股息率/营收/净利润/ROE/ROA/自由现金流等。",
)
async def tool_get_fundamentals(
    ticker: str,
    curr_date: str = None,
) -> str:
    """Get company fundamentals overview."""
    return await get_fundamentals(ticker, curr_date)


@mcp.tool(
    name="get_balance_sheet",
    description="获取资产负债表。参数: ticker=股票代码, freq=quarterly|annual(默认quarterly), curr_date=当前日期(可选)。返回 CSV。",
)
async def tool_get_balance_sheet(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str = None,
) -> str:
    """Get balance sheet data."""
    return await get_balance_sheet(ticker, freq, curr_date)


@mcp.tool(
    name="get_cashflow",
    description="获取现金流量表。参数: ticker=股票代码, freq=quarterly|annual(默认quarterly), curr_date=当前日期(可选)。返回 CSV。",
)
async def tool_get_cashflow(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str = None,
) -> str:
    """Get cash flow statement data."""
    return await get_cashflow(ticker, freq, curr_date)


@mcp.tool(
    name="get_income_statement",
    description="获取利润表。参数: ticker=股票代码, freq=quarterly|annual(默认quarterly), curr_date=当前日期(可选)。返回 CSV。",
)
async def tool_get_income_statement(
    ticker: str,
    freq: str = "quarterly",
    curr_date: str = None,
) -> str:
    """Get income statement data."""
    return await get_income_statement(ticker, freq, curr_date)


@mcp.tool(
    name="get_ticker_news",
    description="获取个股新闻。参数: ticker=股票代码, start_date=开始日期(YYYY-MM-DD), end_date=结束日期(YYYY-MM-DD)。返回新闻列表。",
)
async def tool_get_ticker_news(
    ticker: str,
    start_date: str,
    end_date: str,
) -> str:
    """Get ticker-specific news."""
    return await get_ticker_news(ticker, start_date, end_date)


@mcp.tool(
    name="get_global_macro_news",
    description="获取全球宏观新闻。覆盖: Fed/央行政策/地缘政治/S&P500/大宗商品。参数: curr_date(YYYY-MM-DD), look_back_days(回溯天数), limit(最大文章数)。",
)
async def tool_get_global_macro_news(
    curr_date: str,
    look_back_days: int = None,
    limit: int = None,
) -> str:
    """Get global macroeconomic news."""
    return await get_global_macro_news(curr_date, look_back_days, limit)


@mcp.tool(
    name="get_insider_transactions",
    description="获取内部交易数据。参数: ticker=股票代码。返回 CSV(交易人/职务/类型/股数/价格/日期)。",
)
async def tool_get_insider_transactions(
    ticker: str,
) -> str:
    """Get insider transactions data."""
    return await get_insider_transactions(ticker)


@mcp.tool(
    name="get_stocktwits_sentiment",
    description="获取 StockTwits 社交情绪(无需 API Key)。参数: ticker=股票代码, limit=最大消息数(默认30)。返回用户消息列表。",
)
async def tool_get_stocktwits_sentiment(
    ticker: str,
    limit: int = 30,
) -> str:
    """Get StockTwits social sentiment."""
    return await get_stocktwits_sentiment(ticker, limit)


@mcp.tool(
    name="get_reddit_discussion",
    description="获取 Reddit 讨论(无需 API Key)。参数: ticker=股票代码, limit=最大帖子数(默认20)。返回帖子列表。",
)
async def tool_get_reddit_discussion(
    ticker: str,
    limit: int = 20,
) -> str:
    """Get Reddit discussion posts."""
    return await get_reddit_discussion(ticker, limit)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the MCP server via stdio transport (default for coding assistants)."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
