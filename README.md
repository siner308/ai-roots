# ai-roots

[한국어](README.ko.md) | **English**

A collection of thinking foundations and lessons learned that expand Claude Code's capabilities.

Even non-experts can solve complex problems through casual conversation — Claude automatically applies architect-grade reasoning.

## Two surfaces: resident rules vs situational skills

To keep the always-loaded context small, rules are split by how often they apply:

- **Resident rules** (`rules/`) shape thinking or output on essentially every turn — how Claude reasons, writes, names, and comments. Claude Code loads them into context every session.
- **Situational skills** (`skills/<name>/`) apply only when a specific task type comes up — CSS, PRs, Codex, parallelism, a debugging lesson. Only their one-line description stays in context; the full body loads via the Skill tool when the trigger fires. `rules/_situational-skills.md` is a resident index mapping each trigger to its skill so the trigger is never forgotten.

This keeps the resident set near ~41KB instead of ~92KB while preserving effective behavior: a situational rule still applies in exactly the task where it matters.

## Roots — always-resident rules

### Thinking Expansion
| File | Description |
|------|-------------|
| `rules/thinking-expansion.md` | Prime broad retrieval, deepen past the surface answer, then classify complexity and apply Devil's Advocate / First Principles / Systems Thinking — plus domain token injection and cross-domain connection to surface hidden knowledge |

### Quality Assurance
| File | Description |
|------|-------------|
| `rules/evaluation-integrity.md` | Self-evaluation bias prevention — verifiability classification, generation/evaluation separation, drift detection |
| `rules/claude-architect-principles.md` | Auto-apply architect-grade problem solving — enforcement matching, context discipline, generation/review separation |

### User Growth
| File | Description |
|------|-------------|
| `rules/user-growth-coaching.md` | Post-solve coaching to improve user's question patterns — nudge vague requests toward specific ones |

### Knowledge Capture
| File | Description |
|------|-------------|
| `rules/guardrail-maker.md` | Auto-detect user corrections as tacit knowledge and propose persistent guardrails to prevent recurring mistakes |
| `rules/memory-minimalism.md` | Prefer version-controlled rules/docs over the device-local memory system; memory only for strictly personal, non-shareable context |

### Output Conventions
| File | Description |
|------|-------------|
| `rules/prose-style.md` | Plain spoken-rhythm language (no noun-stacks, no translationese, verbs over nominalizations) and line breaks that fall at meaning boundaries, not the column limit |
| `rules/terminology-discipline.md` | Spell out domain terms; expand established abbreviations on first use; disambiguate collision-prone ones |
| `rules/comment-discipline.md` | Default to no comments; a comment or docstring is never mandatory. Write one only when it's on a closed allowlist (non-obvious WHY). Enforced by the `comment-discipline.py` `PostToolUse` hook |

### Trigger index
| File | Description |
|------|-------------|
| `rules/_situational-skills.md` | Resident map of "when this holds → invoke this skill" for every situational skill below. Stays loaded so a lazy skill's trigger is never missed. |

## Situational Skills — lazy-loaded

Body enters context only when invoked via the Skill tool. The trigger column mirrors `_situational-skills.md`.

| Skill | Trigger | Description |
|-------|---------|-------------|
| `skills/css-discipline/` | Editing/writing/reviewing CSS or framework styling | Close four commonly abused CSS axes — cascade (`!important`), box model, unit soup, style location |
| `skills/github-pr-markdown/` | Composing or editing a PR body/title | Enforce GitHub-flavored Markdown conventions for PRs, plus the safe API-PATCH body delivery |
| `skills/model-effort-delegation/` | Deciding executor/model/effort before delegating | Threshold-based model/effort/subagent selection — delegate specified work to weaker models, keep judgment on Opus, reserve Fable 5 for exceptional reasoning |
| `skills/parallel-execution-modes/` | Choosing sequential vs subagent vs team, inline vs background | Pick the parallelism mode by task independence and communication needs |
| `skills/parallel-hypothesis-investigation/` | A problem has multiple plausible causes or criteria | Decompose into layered hypotheses or judgment criteria and investigate with parallel agents |
| `skills/codex-delegation/` | Delegating to the OpenAI Codex CLI | Cross-provider policy — `/review` triggers, three-turn rescue protocol, mode/flag cheatsheet, capability routing |
| `skills/incremental-verification/` | Task outcome uncertain (API, browser, shell, pipeline) | Break uncertain work into smallest verifiable steps — inline test first, script later, scale gradually |
| `skills/simulate-dont-just-scan/` | Porting/debugging code you read but did not run | Mentally execute code to predict actual runtime output before acting |
| `skills/codex-tmux-monitoring/` | Tempted to monitor a subprocess via tmux/sentinel/tail | Why that pattern failed — use `run_in_background` Bash + harness completion notification instead |
| `skills/background-task-monitoring/` | Long background task needs completion/progress visibility | Pick the cheapest visibility mechanism — completion notification first, event streams second, polling last |

## Skill — `/review` (ai-roots)

A skill installed under `~/.claude/skills/review/` and invoked as `/review`. Because the skill is not packaged as a Claude Code plugin, the call name carries no `ai-roots:` prefix; the ai-roots origin is signaled by the `[ai-roots]` tag at the start of the skill description, which lets you distinguish it from other `review`-named skills (e.g., Claude Code's built-in `/review`).

It performs a **two-evaluator code review** on a resolved target. By default the target is the current branch's changes against its base branch — the PR diff (when a PR exists) plus local uncommitted edits — but `--base <ref>`, `--commit <sha>`, `--uncommitted`, and trailing path filters override it. A Claude Code subagent (`adversarial-reviewer` persona) and a `codex review` invocation run in parallel on the same diff, and their findings are synthesized using the Agreed / Conflicting / Chosen-direction format from `rules/evaluation-integrity.md` §Multi-advisor synthesis.

| File | Description |
|------|-------------|
| `skills/review/SKILL.md` | The `/review` skill body. Spawns Claude subagent + `codex review` in parallel; synthesizes per `evaluation-integrity.md`. |
| `agents/adversarial-reviewer.md` | Security-first adversarial reviewer persona. Used both as the `subagent_type` for the Claude-side reviewer and piped via stdin to `codex review`. |
| `skills/codex-delegation/SKILL.md` | Cross-provider policy — when to invoke `/review`, three-turn rescue protocol, direct Codex invocation cheatsheet for non-review modes, capability routing, execution mechanics, plan-stage review. |

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
- `skills/<name>/` → `~/.claude/skills/<name>` — each skill subfolder is linked individually so Claude Code's skill loader picks up its `SKILL.md`. The loop links `review` plus every situational skill above.
- `agents/<name>.md` → `~/.claude/agents/<name>.md` — each agent file is linked individually so Claude Code registers it as an Agent tool `subagent_type`. Currently: `agents/adversarial-reviewer.md` → `~/.claude/agents/adversarial-reviewer.md`.
- `hooks/<name>` + registration → `~/.claude/hooks/<name>` and `~/.claude/settings.json` — `install.sh` runs `hooks/register.py`, which symlinks each hook declared in `hooks/manifest.json` and merges its `settings.json` entry. No manual editing needed.

If a previous version of the installer created `~/.claude/skills/ai-roots` (a single symlink to the whole `skills/` directory), the new installer removes it automatically — that layout was never recognized by Claude Code's skill loader.

README files, HUD scripts, and the `evals/` workspace (if any) are not symlinked, so they are not loaded as always-on rules.

### Hooks

`hooks/register.py` (run by `install.sh`) handles both symlinking and registration, driven by `hooks/manifest.json`. The merge is idempotent — re-running adds no duplicate hook — and backs up `settings.json` before writing, since that file holds live per-machine config. To add a hook: drop the script in `hooks/`, add a `manifest.json` entry (`event`, `matcher`, `script`, `run`), and re-run `install.sh`.

Currently installed: `comment-discipline.py` — a `PostToolUse` hook on `Edit|Write|MultiEdit` that detects comment lines an edit newly adds to a code file (pre-existing comments excluded) and re-surfaces the `comment-discipline` allowlist so the model re-checks each one. It hardens what a resident prose rule alone couldn't enforce.

### Staying up to date

`install.sh` adds a marker block to your shell rc (`~/.zshrc` or `~/.bashrc`, backed up first) that sources `shell/ai-roots-update.sh`. Like oh-my-zsh, a new terminal does a throttled, read-only `git fetch` (default once per 24h) and, if the clone is behind, asks before doing anything:

```
[ai-roots] 3 update(s) available. Apply now? [Y/n]
```

Answer yes and it runs `git pull --ff-only` then `install.sh`. Nothing is pulled or executed without that confirmation, and a dirty/diverged clone is left alone. Opt out with `AI_ROOTS_AUTO_UPDATE=0`; tune the cadence with `AI_ROOTS_UPDATE_INTERVAL` (seconds).

## Inspiration

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z Token Priming, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — Close the Loop, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator Separation, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF Korean Study Notes
