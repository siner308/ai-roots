---
layout: home

hero:
  name: ai-roots
  text: Thinking foundations for Claude Code
  tagline: A curated set of resident rules, situational skills, and agents that make Claude apply architect-grade reasoning automatically.
  actions:
    - theme: brand
      text: Resident rules
      link: /rules/thinking-expansion
    - theme: alt
      text: Situational skills
      link: /skills/css-discipline
    - theme: alt
      text: GitHub
      link: https://github.com/siner308/ai-roots

features:
  - title: Resident rules
    details: Loaded every session — they shape how Claude reasons, writes, names, and comments. Kept deliberately small.
    link: /rules/thinking-expansion
  - title: Situational skills
    details: Lazy-loaded by trigger. CSS, PRs, Codex, parallelism, debugging lessons — the body enters context only when the task comes up.
    link: /skills/css-discipline
  - title: Agents
    details: Specialized personas like the adversarial reviewer, invoked for focused review passes.
    link: /agents/adversarial-reviewer
---

## Two surfaces: resident rules vs situational skills

To keep the always-loaded context small, rules are split by how often they apply.

- **Resident rules** (`rules/`) shape thinking or output on essentially every turn — how Claude reasons, writes, names, and comments. Claude Code loads them into context every session.
- **Situational skills** (`skills/<name>/`) apply only when a specific task type comes up — CSS, PRs, Codex, parallelism, a debugging lesson. Only their one-line description stays in context; the full body loads via the Skill tool when the trigger fires.

This keeps the resident set near ~41KB instead of ~92KB while preserving effective behavior: a situational rule still applies in exactly the task where it matters.

> The pages on this site are generated from the English sources in `rules/`, `skills/`, and `agents/`. Korean translations live under [한국어](/ko/) — switch languages from the top-right menu. English is the source of truth; the Korean tree is a read-only mirror for reading.
