"""Tests for MCP tool functions — unit tests with mocked data layer."""

from unittest.mock import patch
import pytest

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
)


# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------
MOCK_CSV = "# Stock data for AAPL\n2026-01-02,200.0,201.0,199.0,200.5,100000\n"
MOCK_FUNDAMENTALS = "Market Cap: 3000000000000\nPE Ratio: 30.5\n"
MOCK_NEWS = "2026-01-02 | AAPL announces new product\n"


# ---------------------------------------------------------------------------
# Stock data
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_CSV)
async def test_get_stock_price_data(mock_route):
    result = await get_stock_price_data("AAPL", "2026-01-01", "2026-01-10")
    assert "AAPL" in result
    assert "200.0" in result
    mock_route.assert_called_once_with(
        "get_stock_data", "AAPL", "2026-01-01", "2026-01-10"
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_FUNDAMENTALS)
async def test_get_fundamentals(mock_route):
    result = await get_fundamentals("AAPL", "2026-05-28")
    assert "Market Cap" in result
    mock_route.assert_called_once_with(
        "get_fundamentals", "AAPL", "2026-05-28"
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value="rsi: 55.2\n")
async def test_get_technical_indicator(mock_route):
    result = await get_technical_indicator("AAPL", "rsi", "2026-05-28", 30)
    assert "rsi" in result
    mock_route.assert_called_once_with(
        "get_indicators", "AAPL", "rsi", "2026-05-28", 30
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_CSV)
async def test_get_balance_sheet(mock_route):
    result = await get_balance_sheet("AAPL", "quarterly")
    mock_route.assert_called_once_with(
        "get_balance_sheet", "AAPL", "quarterly", None
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_CSV)
async def test_get_cashflow(mock_route):
    result = await get_cashflow("AAPL", "annual")
    mock_route.assert_called_once_with(
        "get_cashflow", "AAPL", "annual", None
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_CSV)
async def test_get_income_statement(mock_route):
    result = await get_income_statement("TSM", "quarterly")
    mock_route.assert_called_once_with(
        "get_income_statement", "TSM", "quarterly", None
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_NEWS)
async def test_get_ticker_news(mock_route):
    result = await get_ticker_news("AAPL", "2026-01-01", "2026-01-10")
    assert "AAPL" in result
    mock_route.assert_called_once_with(
        "get_news", "AAPL", "2026-01-01", "2026-01-10"
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value="# Global News\nFed holds rates\n")
async def test_get_global_macro_news(mock_route):
    result = await get_global_macro_news("2026-05-28", 7, 10)
    mock_route.assert_called_once_with(
        "get_global_news", "2026-05-28", 7, 10
    )


@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", return_value=MOCK_CSV)
async def test_get_insider_transactions(mock_route):
    result = await get_insider_transactions("AAPL")
    mock_route.assert_called_once_with(
        "get_insider_transactions", "AAPL"
    )


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

@pytest.mark.unit
@pytest.mark.asyncio
@patch("opencode_mcp.tools.route_to_vendor", side_effect=ValueError("bad ticker"))
async def test_error_handling(mock_route):
    result = await get_stock_price_data("BAD", "2026-01-01", "2026-01-10")
    assert "Error" in result
    assert "BAD" in result
