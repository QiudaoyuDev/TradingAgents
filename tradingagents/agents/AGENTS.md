# tradingagents/agents/ — Agent Definitions

## OVERVIEW

All LLM-powered agent implementations organized by role. Each agent is created via a `create_*()` factory function returning a LangGraph-compatible node.

## STRUCTURE

```
agents/
├── analysts/           # 4 analyst types (market, sentiment, news, fundamentals)
├── researchers/        # Bull researcher + Bear researcher (structured debate)
├── managers/           # Research Manager + Portfolio Manager (structured output)
├── trader/             # Trader agent (translates research → transaction proposal)
├── risk_mgmt/          # 3 risk debaters (aggressive, neutral, conservative)
├── utils/              # AgentState, memory log, tool functions, schemas
└── schemas.py          # Pydantic models: ResearchPlan, TraderProposal, PortfolioDecision
```

## AGENT ROLES

| Agent | Input | Output |
|-------|-------|--------|
| Market Analyst | Stock data | Technical analysis report |
| Sentiment Analyst | News/Social | Market sentiment read |
| News Analyst | Global news | Macroeconomic impact |
| Fundamentals Analyst | Financials | Valuation + red flags |
| Bull/Bear Researcher | Analyst reports | Structured debate |
| Research Manager | Debate history | Investment plan with rating |
| Trader | Research plan | Transaction proposal |
| Risk Team | All analysis | Risk assessment debate |
| Portfolio Manager | Everything | Final decision (Buy/Overweight/Hold/Underweight/Sell) |

## CONVENTIONS

- All agents created via `create_<role>(llm)` factory functions
- Structured output via Pydantic schemas for Research Manager, Trader, Portfolio Manager
- `AgentState` (TypedDict) flows through graph — each agent reads/writes specific fields
- Utils at `utils/agent_utils.py` contain tool functions (get_stock_data, get_news, etc.)
