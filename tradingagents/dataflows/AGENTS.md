# tradingagents/dataflows/ — Data Acquisition Layer

## OVERVIEW

Market data abstraction with dual-vendor support. Routes each data category (stock prices, technical indicators, fundamentals, news) to the configured vendor — yfinance (default) or Alpha Vantage.

## ARCHITECTURE

```
interface.py — dispatches to vendor based on config["data_vendors"] / config["tool_vendors"]
  │
  ├── y_finance.py         # OHLCV, indicators, fundamentals, balance sheet, cashflow, income
  ├── yfinance_news.py     # News via yfinance
  ├── alpha_vantage.py     # All Alpha Vantage data types
  ├── alpha_vantage_common.py  # Rate limit handling, shared helpers
  ├── alpha_vantage_*.py   # Per-category Alpha Vantage modules
  ├── reddit.py            # Reddit sentiment data
  └── stocktwits.py        # StockTwits sentiment data
```

## DATA CATEGORIES

| Category | Default Vendor | Tools |
|----------|---------------|-------|
| core_stock_apis | yfinance | get_stock_data |
| technical_indicators | yfinance | get_indicators |
| fundamental_data | yfinance | get_fundamentals, get_balance_sheet, get_cashflow, get_income_statement |
| news_data | yfinance | get_news, get_global_news |

## CONVENTIONS

- Category-level config in `DEFAULT_CONFIG["data_vendors"]`; tool-level override in `["tool_vendors"]`
- Vendor modules export functions with consistent signatures per data type
- `AlphaVantageRateLimitError` is a known exception type
- `stockstats_utils.py` wraps `stockstats` library for technical indicator calculations
