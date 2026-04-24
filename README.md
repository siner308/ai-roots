# ai-roots

[한국어](README.ko.md) | **English**

A collection of thinking foundations and lessons learned that expand Claude Code's capabilities.

Even non-experts can solve complex problems through casual conversation — Claude automatically applies architect-grade reasoning.

## Roots — Thinking Foundations

### Thinking Expansion
| File | Description |
|------|-------------|
| `claude-rules/roots/concept-priming.md` | Domain-spread concept priming + complexity-based thinking expansion (Devil's Advocate, First Principles, Systems Thinking) |
| `claude-rules/roots/progressive-deepening.md` | Internal quality gate that detects shallow answers and automatically digs one level deeper |
| `claude-rules/roots/capability-overhang.md` | Unlock hidden knowledge — domain token injection, cross-domain connections, skill composition |

### Quality Assurance
| File | Description |
|------|-------------|
| `claude-rules/roots/evaluation-integrity.md` | Self-evaluation bias prevention — verifiability classification, generation/evaluation separation, drift detection |
| `claude-rules/roots/claude-architect-principles.md` | Auto-apply architect-grade problem solving — enforcement matching, context discipline, generation/review separation |

### Problem-Solving Strategy
| File | Description |
|------|-------------|
| `claude-rules/roots/parallel-hypothesis-investigation.md` | Decompose complex problems into layered hypotheses and investigate with parallel agents simultaneously |
| `claude-rules/roots/parallel-execution-modes.md` | Choose between sequential, subagent, and team-based parallelism based on task independence and communication needs |
| `claude-rules/roots/model-effort-delegation.md` | Threshold-based model/effort/subagent selection — delegate specified implementation to weaker models, keep judgment on Opus |

### User Growth
| File | Description |
|------|-------------|
| `claude-rules/roots/user-growth-coaching.md` | Post-solve coaching to improve user's question patterns — nudge vague requests toward specific ones |

### Knowledge Capture
| File | Description |
|------|-------------|
| `claude-rules/roots/guardrail-maker.md` | Auto-detect user corrections as tacit knowledge and propose persistent guardrails to prevent recurring mistakes |

### Conventions
| File | Description |
|------|-------------|
| `claude-rules/roots/github-pr-markdown.md` | Enforce GitHub-flavored Markdown conventions for PRs |
| `claude-rules/roots/comment-discipline.md` | Default to no comments — write only when WHY is non-obvious; forbid WHAT-restatements, task-context references, and removal traces |
| `claude-rules/roots/css-discipline.md` | Close four commonly abused CSS axes — cascade (`!important`), box model (margin for spacing, overflow: hidden without purpose), unit soup (literal pixels/colors), style location (utility / scoped / inline trichotomy) |

## Lessons — Retrospective Learnings

Lessons are concrete patterns learned from real mistakes. They describe what works better, not what to avoid.

| File | Description |
|------|-------------|
| `claude-rules/lessons/incremental-verification.md` | Break uncertain work into smallest verifiable steps — inline test first, script later, scale gradually |
| `claude-rules/lessons/background-task-monitoring.md` | Auto-monitor long background tasks with periodic progress reporting — never leave the user asking "is it done?" |
| `claude-rules/lessons/simulate-dont-just-scan.md` | Mentally execute code to predict outputs before acting — reading source files is not the same as understanding runtime behavior |

## Multi-Agent Orchestration (Optional)

Claude Code and OpenAI Codex running together. Codex integration is **optional** — use it if you want any of:

- (a) **Cross-family adversarial review** — a second training distribution catches blind spots Claude alone misses
- (b) **Rescue from anchoring** on hard problems — a fresh stack breaks the 3-turn anchoring trap
- (c) **OpenAI-ecosystem capabilities** — image generation (DALL-E, `gpt-image`), and other OpenAI-exclusive modalities Claude Code does not carry natively

Skip it if none of these apply. Ample Claude Code capacity alone is a valid reason to skip.

| File | Description |
|------|-------------|
| `.claude/agents/adversarial-reviewer.md` | Security-first adversarial reviewer persona. Self-contained prompt usable via Claude Code's Agent tool, or pasted as system prompt when invoking `/codex:adversarial-review`. |
| `.claude/commands/codex/adversarial-review.md` | Slash command template that runs `codex review --uncommitted` with the adversarial reviewer prompt. |
| `.claude/commands/codex/autopilot.md` | Bounded implementation handoff using `codex exec --full-auto`; dangerous no-sandbox mode is explicitly gated. |
| `.claude/commands/codex/diff-review.md` | General read-only Codex production-review command. |
| `.claude/commands/codex/overnight.md` | Unattended workspace-sandbox implementation using `workspace-write`, approval `never`, and web search. |
| `.claude/commands/codex/research.md` | Read-only web-backed research command using `--search`. |
| `.claude/commands/codex/rescue.md` | Read-only Codex rescue handoff for stuck debugging after the three-turn cap. |
| `.claude/commands/codex/yolo-overnight.md` | Explicit no-sandbox/no-approval command for user-accepted dangerous runs. |

Routing rules (mode selection, three-turn cap for hard problems, adversarial review on security-sensitive paths, research, overnight work, and capability-based routing for image generation) live in `claude-rules/roots/model-effort-delegation.md` §Cross-Provider Delegation (Codex). These are **Claude-side** rules — they tell Claude when to invoke Codex, not how Codex should behave.

## Installation

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

Only `claude-rules/` is symlinked into `~/.claude/rules/ai-roots`, so README files, HUD scripts, and agent prompts are not loaded as always-on rules. Claude Code recursively loads all `.md` files from both `claude-rules/roots/` and `claude-rules/lessons/`.

To also install optional Codex delegation commands:

```bash
./install.sh --with-codex
```

## Inspiration

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z Token Priming, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — Close the Loop, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator Separation, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF Korean Study Notes
