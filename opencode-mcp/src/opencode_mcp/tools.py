"""MCP tool functions — wrap TradingAgents data layer for AI coding assistants.

Each function is a standalone, self-documenting callable that routes through
``tradingagents.dataflows.interface.route_to_vendor`` for vendor-agnostic
data fetching (yfinance default, Alpha Vantage fallback).

All functions return plain strings — no structured LLM post-processing needed.
"""

from typing import Optional

from tradingagents.dataflows.interface import route_to_vendor
from tradingagents.dataflows import stocktwits, reddit
from tradingagents.dataflows.config import set_config, get_config

# ---------------------------------------------------------------------------
# Bootstrap: ensure the dataflows layer has a usable config so
# route_to_vendor() resolves vendors correctly without a full graph init.
# ---------------------------------------------------------------------------
_cfg = get_config()
_cfg.setdefault("data_vendors", {})
_cfg["data_vendors"].setdefault("core_stock_apis", "yfinance")
_cfg["data_vendors"].setdefault("technical_indicators", "yfinance")
_cfg["data_vendors"].setdefault("fundamental_data", "yfinance")
_cfg["data_vendors"].setdefault("news_data", "yfinance")
set_config(_cfg)


# ---------------------------------------------------------------------------
# 1. Core stock data
# ---------------------------------------------------------------------------

async def get_stock_price_data(
    symbol: str,
    start_date: str,
    end_date: str,
) -> str:
    """获取股票 OHLCV 历史价格数据 / Get stock OHLCV price history.

    Args:
        symbol: 股票代码，如 AAPL / Ticker symbol, e.g. AAPL, 0700.HK
        start_date: 开始日期，YYYY-MM-DD 格式 / Start date in YYYY-MM-DD
        end_date: 结束日期，YYYY-MM-DD 格式 / End date in YYYY-MM-DD

    Returns:
        CSV 格式股票数据，含 Open/High/Low/Close/Volume / Stock data as CSV
    """
    try:
        return route_to_vendor("get_stock_data", symbol, start_date, end_date)
    except Exception as e:
        return f"Error fetching stock data for {symbol}: {e}"


# ---------------------------------------------------------------------------
# 2. Technical indicators
# ---------------------------------------------------------------------------

async def get_technical_indicator(
    symbol: str,
    indicator: str,
    curr_date: str,
    look_back_days: int = 30,
) -> str:
    """获取技术指标数据 / Get technical indicator values.

    支持以下指标 (Supported indicators):
      rsi, macd, macds, macdh, close_50_sma, close_200_sma, close_10_ema,
      boll, boll_ub, boll_lb, atr, vwma, mfi

    Args:
        symbol: 股票代码 / Ticker symbol
        indicator: 指标名称，一次一个 / Single indicator name
        curr_date: 当前交易日，YYYY-MM-DD / Trading date
        look_back_days: 回溯天数 / Lookback window in days (default 30)

    Returns:
        指标日期序列值 + 指标用途说明 / Indicator values with description
    """
    try:
        return route_to_vendor(
            "get_indicators", symbol, indicator, curr_date, look_back_days
        )
    except Exception as e:
        return f"Error fetching indicator '{indicator}' for {symbol}: {e}"


# ---------------------------------------------------------------------------
# 3. Fundamentals
# ---------------------------------------------------------------------------

async def get_fundamentals(
    ticker: str,
    curr_date: Optional[str] = None,
) -> str:
    """获取公司基本面数据 / Get company fundamentals overview.

    返回 29 项指标，包括：市值、PE、EPS、Beta、股息率、52周高低、
    营收、EBITDA、净利润、ROE、ROA、资产负债率、自由现金流等。

    Returns 29 metrics including: Market Cap, PE, EPS, Beta, Dividend Yield,
    52W High/Low, Revenue, EBITDA, Net Income, ROE, ROA, D/E, FCF, etc.

    Args:
        ticker: 股票代码 / Ticker symbol
        curr_date: 当前日期（可选）/ Current date (optional)

    Returns:
        基本面报告 / Fundamentals report (key: value format)
    """
    try:
        return route_to_vendor("get_fundamentals", ticker, curr_date)
    except Exception as e:
        return f"Error fetching fundamentals for {ticker}: {e}"


# ---------------------------------------------------------------------------
# 4-6. Financial statements
# ---------------------------------------------------------------------------

async def get_balance_sheet(
    ticker: str,
    freq: str = "quarterly",
    curr_date: Optional[str] = None,
) -> str:
    """获取资产负债表 / Get balance sheet data.

    Args:
        ticker: 股票代码 / Ticker symbol
        freq: 频率，quarterly 或 annual / Frequency (quarterly|annual)
        curr_date: 当前日期（可选）/ Current date (optional)

    Returns:
        资产负债表 CSV / Balance sheet as CSV
    """
    try:
        return route_to_vendor("get_balance_sheet", ticker, freq, curr_date)
    except Exception as e:
        return f"Error fetching balance sheet for {ticker}: {e}"


async def get_cashflow(
    ticker: str,
    freq: str = "quarterly",
    curr_date: Optional[str] = None,
) -> str:
    """获取现金流量表 / Get cash flow statement data.

    Args:
        ticker: 股票代码 / Ticker symbol
        freq: 频率，quarterly 或 annual / Frequency (quarterly|annual)
        curr_date: 当前日期（可选）/ Current date (optional)

    Returns:
        现金流量表 CSV / Cash flow as CSV
    """
    try:
        return route_to_vendor("get_cashflow", ticker, freq, curr_date)
    except Exception as e:
        return f"Error fetching cash flow for {ticker}: {e}"


async def get_income_statement(
    ticker: str,
    freq: str = "quarterly",
    curr_date: Optional[str] = None,
) -> str:
    """获取利润表 / Get income statement data.

    Args:
        ticker: 股票代码 / Ticker symbol
        freq: 频率，quarterly 或 annual / Frequency (quarterly|annual)
        curr_date: 当前日期（可选）/ Current date (optional)

    Returns:
        利润表 CSV / Income statement as CSV
    """
    try:
        return route_to_vendor("get_income_statement", ticker, freq, curr_date)
    except Exception as e:
        return f"Error fetching income statement for {ticker}: {e}"


# ---------------------------------------------------------------------------
# 7-9. News and insider data
# ---------------------------------------------------------------------------

async def get_ticker_news(
    ticker: str,
    start_date: str,
    end_date: str,
) -> str:
    """获取个股新闻 / Get ticker-specific news.

    Args:
        ticker: 股票代码 / Ticker symbol
        start_date: 开始日期 YYYY-MM-DD / Start date
        end_date: 结束日期 YYYY-MM-DD / End date

    Returns:
        新闻列表（标题 + 时间 + 摘要）/ News headlines with timestamps
    """
    try:
        return route_to_vendor("get_news", ticker, start_date, end_date)
    except Exception as e:
        return f"Error fetching news for {ticker}: {e}"


async def get_global_macro_news(
    curr_date: str,
    look_back_days: Optional[int] = None,
    limit: Optional[int] = None,
) -> str:
    """获取全球宏观新闻 / Get global macroeconomic news.

    覆盖 (Covers): Federal Reserve, S&P 500, 地缘政治 / Geopolitics,
    央行政策 / Central bank policy, 大宗商品 / Commodities

    Args:
        curr_date: 当前日期 YYYY-MM-DD / Current date
        look_back_days: 回溯天数（默认使用配置值）/ Lookback days
        limit: 最大文章数（默认使用配置值）/ Max articles

    Returns:
        宏观新闻列表 / Macro news headlines
    """
    try:
        return route_to_vendor(
            "get_global_news", curr_date, look_back_days, limit
        )
    except Exception as e:
        return f"Error fetching global news: {e}"


async def get_insider_transactions(
    ticker: str,
) -> str:
    """获取内部交易数据 / Get insider transactions data.

    Args:
        ticker: 股票代码 / Ticker symbol

    Returns:
        内部交易 CSV（交易人、职务、类型、股数、价格、日期）
        Insider transactions CSV (transaction date, insider, type, shares, price)
    """
    try:
        return route_to_vendor("get_insider_transactions", ticker)
    except Exception as e:
        return f"Error fetching insider transactions for {ticker}: {e}"


# ---------------------------------------------------------------------------
# 10-11. Social sentiment (no API key required — public endpoints)
# ---------------------------------------------------------------------------

async def get_stocktwits_sentiment(
    ticker: str,
    limit: int = 30,
) -> str:
    """获取 StockTwits 社交情绪 / Get StockTwits social sentiment.

    无需 API Key — 使用 StockTwits 公开 API。
    No API Key required — uses StockTwits public API.

    Args:
        ticker: 股票代码 / Ticker symbol
        limit: 最大返回消息数 / Max messages to return (default 30)

    Returns:
        用户消息列表（用户 + 消息 + 时间 + 关注者数）
        User messages (user, message, time, followers)
    """
    try:
        result = stocktwits.fetch_stocktwits_messages(ticker, limit)
        return result if result else f"No StockTwits data found for {ticker}"
    except Exception as e:
        return f"Error fetching StockTwits data for {ticker}: {e}"


async def get_reddit_discussion(
    ticker: str,
    limit: int = 20,
) -> str:
    """获取 Reddit 讨论 / Get Reddit discussion posts.

    无需 API Key — 使用 Reddit 公开 JSON 接口。
    No API Key required — uses Reddit public JSON API.

    Args:
        ticker: 股票代码 / Ticker symbol
        limit: 最大返回帖子数 / Max posts to return (default 20)

    Returns:
        帖子列表（标题 + 分数 + 评论数 + 内容摘要）
        Posts (title, score, comments, content summary)
    """
    try:
        result = reddit.fetch_reddit_posts(ticker, limit_per_sub=limit)
        return result if result else f"No Reddit data found for {ticker}"
    except Exception as e:
        return f"Error fetching Reddit data for {ticker}: {e}"
