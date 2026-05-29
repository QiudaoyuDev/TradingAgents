# cli/ — Terminal UI

## OVERVIEW

Rich interactive CLI built with `typer` + `questionary` + `rich`. Guides users through a step-by-step questionnaire (ticker, date, LLM provider, model selection, research depth), then streams the analysis live with agent progress tracking.

## FILES

| File | Role |
|------|------|
| `main.py` | Entry point: `app = typer.Typer()`, interactive questionnaire, live display, report saving |
| `models.py` | Enums for analyst types, asset types, research depth |
| `config.py` | Provider-specific model lists, region endpoints, thinking config options |
| `utils.py` | Selection prompts, API key validation, display helpers |
| `announcements.py` | Fetches and displays project announcements |
| `stats_handler.py` | `StatsCallbackHandler` — tracks LLM calls, tool calls, token usage |
| `static/` | ASCII art, static assets |

## CLI FLOW

```
1. Welcome banner & announcements
2. Step-by-step questionnaire (ticker, date, language, analysts, depth, provider, models, thinking config)
3. Live dashboard: agent status table, message log, report content, stats footer
4. Final report display + disk save (organized by team in subfolders)
```

## CONVENTIONS

- `MessageBuffer` manages display state: agent_status, report_sections, message log
- Reports saved to `~/.tradingagents/logs/<TICKER>/<DATE>/reports/` organized by team
- `StatsCallbackHandler` bound to both LLM and LangGraph run for full telemetry
