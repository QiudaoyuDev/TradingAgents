# tradingagents/graph/ — LangGraph Workflow

## OVERVIEW

State machine orchestration: defines agent graph topology (sequential + conditional edges), checkpoint/resume, state propagation, output signal processing, and deferred return reflection.

## FILES

| File | Role |
|------|------|
| `trading_graph.py` | `TradingAgentsGraph` — main orchestrator, propagates graph for a ticker+date |
| `setup.py` | `GraphSetup` — builds `StateGraph` with all agent nodes and conditional edges |
| `propagation.py` | `Propagator` — creates initial `AgentState`, manages recursion limits |
| `conditional_logic.py` | Edge routing: should_continue_debate, should_continue_risk_analysis |
| `analyst_execution.py` | Builds sequential execution plan for the 4 analyst types |
| `signal_processing.py` | `SignalProcessor` — extracts structured decisions from raw signals |
| `reflection.py` | `Reflector` — generates post-trade reflections comparing return vs benchmark |
| `checkpointer.py` | Per-ticker SQLite checkpoint/resume via LangGraph `SqliteSaver` |

## GRAPH FLOW

```
START → Analyst(s) → Bull/Bear Researcher (debate) → Research Manager → Trader → Aggressive/Neutral/Conservative Risk → Portfolio Manager → END
```

Analysts execute sequentially (configurable concurrency). Bull/Bear researchers debate with configurable rounds. Risk team debates in fixed order: Aggressive → Conservative → Neutral (loop) → Portfolio Manager decides.
