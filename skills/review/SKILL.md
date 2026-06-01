---
name: review
description: "[ai-roots] Two-evaluator code review provided by the ai-roots skill set. Resolves the review target (by default the current branch's changes against its base — i.e. the PR diff plus local uncommitted edits — but also an explicit base, commit, or uncommitted-only scope), then spawns a Claude Code subagent and a Codex review in parallel on that same diff and synthesizes findings using the Agreed / Conflicting / Chosen-direction format from rules/evaluation-integrity.md §Multi-advisor synthesis. Use whenever the user requests a review of pending or proposed changes and both Claude and Codex are available."
---

# /review (ai-roots)

Independent two-evaluator review. Both evaluators review the **same resolved target** and do not see each other's output until synthesis.

The target is NOT hardcoded to the uncommitted diff. By default it is the whole set of changes this branch proposes — committed branch changes plus local uncommitted edits, measured against the base branch (the PR base when a PR exists). The user can override the scope.

## Scope resolution

Resolve the target in the main session **before** spawning the evaluators. Produce two values: `DIFF_CMD` (a git command that emits exactly the diff to review) and a human-readable `TARGET` description. Pass the *same* `DIFF_CMD` to both evaluators so their scopes match.

Mode is chosen from the user's argument; default is branch-vs-base.

| User argument | Mode | `DIFF_CMD` |
|---------------|------|------------|
| _(none)_ | branch vs base | `git diff <merge-base SHA>` |
| `--base <ref>` | branch vs explicit base | `git diff <merge-base SHA>` |
| `--uncommitted` | working tree only | `git diff HEAD` (plus untracked) |
| `--commit <sha>` | one commit | `git show <commit SHA>` |
| trailing `<paths…>` | narrows any mode | append ` -- '<path>'…` (single-quoted) |

`git diff <merge-base SHA>` diffs the fork point to the **working tree**, so it captures committed branch changes *and* uncommitted local edits in one diff — exactly "PR diff + local changes". This is what `codex review --base` does internally; we resolve the merge-base ourselves and embed the resulting command so the persona (below) can travel with it.

**Injection safety — STRICT.** `DIFF_CMD` is embedded into a prompt that BOTH evaluators are instructed to run in a shell. A git ref or branch name can legally contain shell metacharacters (`;`, `$( )`, backticks), so interpolating a raw ref into the command is a command-injection vector — especially for `--base <ref>` and PR base names from untrusted forks. Defuse it by resolving every ref to a **commit SHA in the main session** (where the ref is an ordinary quoted shell variable and cannot inject), then embedding only the hex SHA. SHAs contain no metacharacters. Never embed a raw ref, and single-quote any path filter (rejecting paths that contain a single quote).

### Base ref auto-detection (branch-vs-base mode)

```bash
PR_BASE="$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null)"
if [ -n "$PR_BASE" ]; then
  BASE="$PR_BASE"                       # PR exists → use its base branch
else
  BASE="$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null \
          | sed 's@^refs/remotes/origin/@@')"
  [ -z "$BASE" ] && BASE=main           # fall back to the repo default branch
fi
# Prefer the remote-tracking ref for an accurate fork point; fall back to local.
if git rev-parse --verify --quiet "origin/$BASE^{commit}" >/dev/null; then
  BASE_REF="origin/$BASE"
else
  BASE_REF="$BASE"
fi
# Resolve to a commit SHA HERE, where BASE_REF is a quoted variable and cannot
# inject. The embedded DIFF_CMD then carries only a hex SHA — see Injection safety.
MERGE_BASE="$(git merge-base "$BASE_REF" HEAD)" || { echo "no merge-base with $BASE_REF"; exit 1; }
DIFF_CMD="git diff $MERGE_BASE"
```

For `--commit <sha>`, resolve and validate first: `SHA="$(git rev-parse --verify "$ARG^{commit}")" || exit 1; DIFF_CMD="git show $SHA"`. `git rev-parse --verify` rejects a non-ref argument, which also blocks a metacharacter-laden string from reaching the embedded command.

Edge cases:
- **On the base branch with no commits ahead** (e.g. on `main`, no PR): the merge-base is `HEAD`, so `DIFF_CMD` reduces to the uncommitted diff. Sensible — review what's there.
- **Empty target** (no commits ahead and no uncommitted changes): report "nothing to review" and stop. Do not spawn evaluators on an empty diff.
- **PR base only on remote**: `git fetch origin <BASE>` first if `origin/<BASE>` is missing, then resolve.

State the resolved `TARGET` to the user before reviewing (e.g. "Reviewing `feature` vs `origin/main` (PR #123) + local changes").

## Evaluators

### 1. Claude Code subagent

Invoke the `Agent` tool with `subagent_type: adversarial-reviewer` (persona at `~/.claude/agents/adversarial-reviewer.md`). Brief it to run `DIFF_CMD` to obtain the diff and review only that output, with the security-first, P0–P3 classification from its persona. Pass the resolved `TARGET` and any user scope in the prompt.

If the `adversarial-reviewer` agent is not registered, fall back to `subagent_type: general-purpose` and inline the persona body as the prompt.

### 2. Codex review

`codex review`'s `--uncommitted` / `--base` / `--commit` flags are mutually exclusive with a custom prompt, so the persona cannot ride along with them. Use **custom-prompt mode** instead and embed `DIFF_CMD` so codex reviews the exact same scope with our persona:

```bash
LOG="/tmp/ai-roots-review-codex-$(date +%Y%m%d-%H%M%S).log"
PROMPT="$(mktemp)"
{
  cat "$HOME/.claude/agents/adversarial-reviewer.md"
  printf '\n\n---\nObtain the review target by running exactly this command:\n\n    %s\n\nReview ONLY the diff that command produces. Apply the persona above (security-first, P0–P3).\n' "$DIFF_CMD"
} > "$PROMPT"

# Always wrap codex in a timeout: a hung codex never exits, so its run_in_background
# completion notification never fires and the main session waits forever. timeout
# guarantees the task ends (exit 124 on expiry). macOS lacks coreutils `timeout`
# unless brew-installed (`gtimeout`); degrade gracefully if neither exists.
# Store ONLY the binary name (a single word). zsh does not word-split unquoted
# variables, so a "timeout 900" string would be run as one command and fail with
# `command not found: timeout 900`; keeping 900 a literal arg works in bash and zsh.
TIMEOUT_BIN=""
if command -v timeout >/dev/null 2>&1; then TIMEOUT_BIN=timeout
elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT_BIN=gtimeout; fi

# Redirect (not pipe) codex output to the log so $? is codex's own exit status —
# portable across bash and zsh (no PIPESTATUS/pipestatus array). cat shows it after.
if [ -n "$TIMEOUT_BIN" ]; then
  "$TIMEOUT_BIN" 900 codex review -c model="gpt-5.5" -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
else
  codex review -c model="gpt-5.5" -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
fi
CODEX_EXIT=$?
cat "$LOG"
echo "codex exit: $CODEX_EXIT (124 = timed out)"
```

- Model is set via `-c model=…`; `codex review` does **not** accept `-m`.
- No `--uncommitted` / `--base` flag — the scope lives in the embedded command, single-quoted so the local shell does not expand `$(…)` before codex runs it.
- Use `run_in_background: true` so the main session is notified when Codex exits.
- **Read the codex exit status** (`$CODEX_EXIT`). `124` means the review timed out — treat it like Codex being unavailable: proceed with the Claude evaluator and note in the synthesis that only one reviewer ran (and that codex timed out). Do not silently drop a timeout as if codex returned a clean verdict.
- If `codex` is not on `PATH`, skip this evaluator and note in the synthesis that only one reviewer ran.

### Parallelism

Spawn the Agent call and the Bash invocation in the same response so they run concurrently. Wait for both to complete before producing the synthesis.

## Synthesis

Apply `rules/evaluation-integrity.md` §Multi-advisor synthesis. The output MUST separate three buckets:

1. **Agreed** — findings that appeared in BOTH evaluators. Highest confidence.
2. **Conflicting** — findings flagged by only one evaluator, or where evaluators disagree on severity / cause / fix. Single-evaluator findings belong here, not in Agreed. Silence is not agreement.
3. **Chosen direction + rationale** — the decision given the conflicts, and why. If a conflict is unresolved, say so and escalate to the user rather than picking silently.

For each finding, preserve the originating evaluator's severity classification (P0–P3). Do not re-rank findings to look consistent across evaluators — disagreement on severity is itself signal.

## Scope (user overrides)

Pass the user's additional scope (if any) to BOTH evaluators verbatim. Do not paraphrase or trim. A trailing path filter narrows `DIFF_CMD` for both via the ` -- <paths>` suffix.

## Anti-patterns

- Defaulting to uncommitted-only when the user is on a feature branch with committed work — the default target is branch-vs-base, which includes both.
- Running only one evaluator and labeling the result a "review" — that defeats the cross-provider purpose. If Codex is unavailable, say so explicitly.
- Passing different scopes to the two evaluators — both must review the diff from the same `DIFF_CMD`.
- Smoothing over disagreements in synthesis. The Conflicting bucket exists precisely because the synthesizer is biased toward making the output sound confident.
- Promoting a single-evaluator finding to "Agreed" because nothing contradicted it.
- Auto-applying fixes from either evaluator. Report findings; the main session decides what to apply.
