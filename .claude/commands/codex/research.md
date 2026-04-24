# Codex Research

Delegate web-backed research to OpenAI Codex without granting write access.

## When To Use

Use when the task needs current information, official documentation lookup, ecosystem-specific facts, market/product research, or web search before Claude makes a decision.

## Protocol

Run Codex in read-only non-interactive mode with web search enabled:

```bash
codex exec -m gpt-5.5 -c model_reasoning_effort=xhigh --sandbox read-only --ask-for-approval never --search -
```

Paste a brief with:

- Research question
- Required source quality, such as official docs, primary sources, or reputable publications
- Recency requirement, if any
- Decision Claude needs to make from the result
- Citation requirement

## Prompt Tail

```text
Research only. Do not edit files. Use web search when needed. Prefer primary sources and official documentation. Return concise findings with links, dates where relevant, and a short recommendation. Extra user scope: $ARGUMENTS
```
