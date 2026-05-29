# tradingagents/llm_clients/ — LLM Provider Abstraction

## OVERVIEW

Provider-agnostic LLM client layer. Factory pattern routes model requests to the correct provider implementation. Supports 10+ providers including OpenAI-compatible APIs and native SDKs.

## ARCHITECTURE

```
factory.py → create_llm_client(provider, model, base_url, **kwargs)
  │
  ├── openai_client.py   → Handles OpenAI, xAI, DeepSeek, Qwen, GLM, MiniMax, Ollama, OpenRouter (all OpenAI-compatible)
  ├── anthropic_client.py → Anthropic Claude SDK
  ├── google_client.py    → Google Gemini SDK
  └── azure_client.py     → Azure OpenAI
```

## PROVIDERS

| Provider | Client | API Style |
|----------|--------|-----------|
| openai, xai, deepseek, qwen, glm, minimax, ollama, openrouter | `OpenAIClient` | OpenAI chat completions |
| anthropic | `AnthropicClient` | Anthropic SDK |
| google | `GoogleClient` | Google Generative AI SDK |
| azure | `AzureOpenAIClient` | Azure OpenAI |

## CONVENTIONS

- All clients extend `BaseLLMClient` (abstract: `get_llm()`, `validate_model()`)
- `normalize_content()` handles multi-block responses (text + reasoning) across providers
- Provider-specific thinking/reasoning config passed via kwargs (google_thinking_level, openai_reasoning_effort, anthropic_effort)
- `model_catalog.py` maintains known model lists per provider; unknown models trigger a `RuntimeWarning` but continue
