# tradingagents/ — Core Package

## OVERVIEW

Framework core: LangGraph state machine, multi-provider LLM client abstraction, dual-vendor data acquisition layer, and all agent implementations.

## STRUCTURE

```
tradingagents/
├── agents/         # Agent definitions (analysts, researchers, managers, trader, risk)
├── graph/          # LangGraph orchestration (setup, propagation, checkpoints)
├── llm_clients/    # Provider-agnostic LLM abstraction (factory + 5+ provider clients)
├── dataflows/      # Market data acquisition (yfinance, Alpha Vantage)
├── default_config.py  # Single source of truth for all config keys
└── __init__.py     # Auto-loads .env, suppresses known deprecation warnings
```

## WHERE TO LOOK

| Task | File |
|------|------|
| Orchestrate agents | `graph/trading_graph.py` — `TradingAgentsGraph` class |
| Configure everything | `default_config.py` — `DEFAULT_CONFIG` dict |
| Add new LLM provider | `llm_clients/factory.py` + new client in `llm_clients/` |
| Add new data vendor | `dataflows/interface.py` + vendor module |
| Add new agent role | `agents/` subfolder + register in `agents/__init__.py` |

## CONVENTIONS

- Config keys are auto-overridden by `TRADINGAGENTS_*` env vars via `_apply_env_overrides()`
- New agents follow `create_<role>()` factory pattern returning a LangGraph `StateGraph` node
- Data vendor selection: category-level config in `default_config.py["data_vendors"]`, tool-level override in `["tool_vendors"]`
