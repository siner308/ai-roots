# Codex Research

Web-backed research via Codex without write access. Use for current docs, ecosystem facts, market/product research. See `claude-rules/codex/codex-delegation.md`.

```bash
codex --search -a never exec --sandbox read-only -m gpt-5.5 -c model_reasoning_effort=xhigh -
```

Stdin brief should include: research question, required source quality (official docs, primary sources), recency requirement, the decision Claude needs to make from the result, citation requirement.

Append:

```text
Research only. Do not edit files. Use web search when needed. Prefer primary sources and official documentation. Return concise findings with links, dates where relevant, and a short recommendation. Extra user scope: $ARGUMENTS
```
