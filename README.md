# ai-roots

[한국어](README.ko.md) | **English**

A collection of thinking foundations and lessons learned that expand Claude Code's capabilities.

Even non-experts can solve complex problems through casual conversation — Claude automatically applies architect-grade reasoning.

## Roots — Thinking Foundations

### Thinking Expansion
| File | Description |
|------|-------------|
| `rules/roots/concept-priming.md` | Domain-spread concept priming + complexity-based thinking expansion (Devil's Advocate, First Principles, Systems Thinking) |
| `rules/roots/progressive-deepening.md` | Internal quality gate that detects shallow answers and automatically digs one level deeper |
| `rules/roots/capability-overhang.md` | Unlock hidden knowledge — domain token injection, cross-domain connections, skill composition |

### Quality Assurance
| File | Description |
|------|-------------|
| `rules/roots/evaluation-integrity.md` | Self-evaluation bias prevention — verifiability classification, generation/evaluation separation, drift detection |
| `rules/roots/claude-architect-principles.md` | Auto-apply architect-grade problem solving — enforcement matching, context discipline, generation/review separation |

### Problem-Solving Strategy
| File | Description |
|------|-------------|
| `rules/roots/parallel-hypothesis-investigation.md` | Decompose complex problems into layered hypotheses and investigate with parallel agents simultaneously |
| `rules/roots/parallel-execution-modes.md` | Choose between sequential, subagent, and team-based parallelism based on task independence and communication needs |
| `rules/roots/model-effort-delegation.md` | Threshold-based model/effort/subagent selection — delegate specified implementation to weaker models, keep judgment on Opus |

### User Growth
| File | Description |
|------|-------------|
| `rules/roots/user-growth-coaching.md` | Post-solve coaching to improve user's question patterns — nudge vague requests toward specific ones |

### Knowledge Capture
| File | Description |
|------|-------------|
| `rules/roots/guardrail-maker.md` | Auto-detect user corrections as tacit knowledge and propose persistent guardrails to prevent recurring mistakes |

### Conventions
| File | Description |
|------|-------------|
| `rules/roots/github-pr-markdown.md` | Enforce GitHub-flavored Markdown conventions for PRs |
| `rules/roots/comment-discipline.md` | Default to no comments — write only when WHY is non-obvious; forbid WHAT-restatements, task-context references, and removal traces |
| `rules/roots/css-discipline.md` | Close four commonly abused CSS axes — cascade (`!important`), box model (margin for spacing, overflow: hidden without purpose), unit soup (literal pixels/colors), style location (utility / scoped / inline trichotomy) |

## Lessons — Retrospective Learnings

Lessons are concrete patterns learned from real mistakes. They describe what works better, not what to avoid.

| File | Description |
|------|-------------|
| `rules/lessons/incremental-verification.md` | Break uncertain work into smallest verifiable steps — inline test first, script later, scale gradually |
| `rules/lessons/background-task-monitoring.md` | Pick the cheapest visibility mechanism for long background tasks — completion notification first, event streams second, interval polling only as fallback |
| `rules/lessons/simulate-dont-just-scan.md` | Mentally execute code to predict outputs before acting — reading source files is not the same as understanding runtime behavior |
| `rules/lessons/codex-tmux-monitoring.md` | Why the previous tmux split-pane + sentinel pattern for monitoring background Codex runs failed — decompose wake-up vs live-output into separate mechanisms |

## Skill — `/review` (ai-roots)

A single skill is installed under `~/.claude/skills/review/` and is invoked as `/review`. Because the skill is not packaged as a Claude Code plugin, the call name carries no `ai-roots:` prefix; the ai-roots origin is signaled by the `[ai-roots]` tag at the start of the skill description, which lets you distinguish it from other `review`-named skills (e.g., Claude Code's built-in `/review`).

It performs a **two-evaluator code review** on a resolved target. By default the target is the current branch's changes against its base branch — the PR diff (when a PR exists) plus local uncommitted edits — but `--base <ref>`, `--commit <sha>`, `--uncommitted`, and trailing path filters override it. A Claude Code subagent (`adversarial-reviewer` persona) and a `codex review` invocation run in parallel on the same diff, and their findings are synthesized using the Agreed / Conflicting / Chosen-direction format from `rules/roots/evaluation-integrity.md` §Multi-advisor synthesis.

| File | Description |
|------|-------------|
| `skills/review/SKILL.md` | The `/review` skill body. Spawns Claude subagent + `codex review` in parallel; synthesizes per `evaluation-integrity.md`. |
| `agents/adversarial-reviewer.md` | Security-first adversarial reviewer persona. Used both as the `subagent_type` for the Claude-side reviewer and piped via stdin to `codex review`. |
| `rules/codex/codex-delegation.md` | Cross-provider policy — when to invoke `/review`, three-turn rescue protocol, direct Codex invocation cheatsheet for non-review modes, capability routing, execution mechanics, plan-stage review. |

If Codex CLI is not on `PATH`, the skill falls back to a single Claude-side evaluator (the cross-provider diversity is lost but the synthesis structure still applies).

## Installation

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

The installer creates symlinks:

- `rules/` → `~/.claude/rules/ai-roots` — Claude Code recursively loads all `.md` files here as always-on rules.
- `skills/<name>/` → `~/.claude/skills/<name>` — each skill subfolder is linked individually so Claude Code's skill loader picks up its `SKILL.md`. Currently: `skills/review/` → `~/.claude/skills/review` (tagged `[ai-roots]` in its description).
- `agents/<name>.md` → `~/.claude/agents/<name>.md` — each agent file is linked individually so Claude Code registers it as an Agent tool `subagent_type`. Currently: `agents/adversarial-reviewer.md` → `~/.claude/agents/adversarial-reviewer.md`.

If a previous version of the installer created `~/.claude/skills/ai-roots` (a single symlink to the whole `skills/` directory), the new installer removes it automatically — that layout was never recognized by Claude Code's skill loader.

README files, HUD scripts, and the `evals/` workspace (if any) are not symlinked, so they are not loaded as always-on rules.

## Inspiration

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z Token Priming, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — Close the Loop, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator Separation, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF Korean Study Notes
