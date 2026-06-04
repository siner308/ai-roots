---
name: review
description: "[ai-roots] Two-evaluator review of any artifact — code changes, a plan or design Claude just produced, a document, a config, or anything reviewable. From a natural-language request it determines the artifact kind, resolves ONE concrete shared artifact (a git diff, a file, or inline text captured to a temp file), then spawns a Claude Code subagent and a Codex run in parallel on that same artifact with kind-appropriate criteria, and synthesizes findings using the Agreed / Conflicting / Chosen-direction format from rules/evaluation-integrity.md §Multi-advisor synthesis. Use whenever the user asks to review pending code, a plan, a document, or any other artifact and both Claude and Codex are available."
---

# /review (ai-roots)

Independent two-evaluator review of **any artifact**. Both evaluators judge the **same resolved artifact** and do not see each other's output until synthesis.

Not just diffs. The artifact can be code changes, a plan or design Claude just produced, a document, a config, a dataset — anything reviewable. The machinery is constant — two independent evaluators → Agreed / Conflicting / Chosen synthesis. Only two things vary by artifact: **how it is acquired** and **what "good" means** for it.

## 1. Resolve the artifact

From the user's natural-language request, determine the **KIND** and produce ONE concrete artifact that both evaluators access **identically**, plus a human-readable `TARGET`. The main session resolves it once; the evaluators never re-interpret the request — that is what keeps the two reviews comparable.

KIND — pick the best fit:

- **code** — "review my changes / PR / this branch / that commit", or the request is about code in a repo. Default when in a repo and the subject is code.
- **plan** — "review this plan / the plan you just wrote / this approach / this design". The artifact is often text Claude produced in *this conversation*.
- **doc** — a prose document, README, spec, PRD, proposal.
- **generic** — anything else: a config, a dataset, a decision, a checklist. Catch-all.

Make the artifact concrete and **shared** (identical bytes for both evaluators):

- **code** → resolve a `DIFF_CMD` (see Code scope resolution). Both evaluators run it.
- **inline plan/doc/generic** that lives only in this conversation (no file) → capture it verbatim to a temp file: `ARTIFACT="$(mktemp)"; cat > "$ARTIFACT" <<'EOF' … EOF`. Both read that file. This is critical: re-describing an inline plan to each evaluator would give them different text — capture once.
- **file-backed plan/doc/generic** → the path(s). Both read them.

State the resolved `TARGET` to the user before reviewing (e.g. "Reviewing the migration plan (inline, 42 lines)", "Reviewing `feature` vs `origin/main` (PR #123) + local changes", "Reviewing `docs/rfc-007.md`"). Ambiguous request → pick the most likely KIND and let `TARGET` be the correction point; truly unresolvable → ask one clarifying question.

### Code scope resolution (KIND=code)

The user names the scope in natural language; map it to an intent, then resolve to a SHA-based command:

| User says (examples) | Intent | `DIFF_CMD` |
|----------------------|--------|------------|
| _(nothing)_, "review my changes", "this branch" | branch vs base | `git diff <merge-base SHA>` |
| "vs main", "against develop", "compared to <ref>" | branch vs named base | `git diff <merge-base SHA>` |
| "uncommitted", "working tree", "what I haven't committed" | working tree only | `git diff HEAD` (plus untracked) |
| "the last commit", "HEAD", "commit <sha>" | one commit | `git show <SHA>` |
| "last 3 commits", "since <ref>" | a commit range | `git diff <range-start SHA>` |
| "just the X files", "only <path>" | narrows any of the above | append ` -- '<path>'…` |

Default when scope is empty or vague is **branch-vs-base**. `git diff <merge-base SHA>` diffs the fork point to the working tree, so it captures committed branch changes *and* uncommitted local edits in one diff — "PR diff + local changes".

**Injection safety — STRICT.** `DIFF_CMD` is embedded into a prompt the evaluators run in a shell. A git ref or branch name can legally contain shell metacharacters (`;`, `$( )`, backticks), so interpolating a raw ref is a command-injection vector — especially a named base or a PR base from an untrusted fork. Resolve every ref to a **commit SHA in the main session** (where it is a quoted variable and cannot inject) and embed only the hex SHA. Never embed a raw ref, and single-quote any path filter (reject paths containing a single quote).

Base ref auto-detection (default / named-base). For a named base ("vs <ref>"), set `BASE` to that ref and skip detection:

```bash
PR_BASE="$(gh pr view --json baseRefName -q .baseRefName 2>/dev/null)"
if [ -n "$PR_BASE" ]; then
  BASE="$PR_BASE"                       # PR exists → use its base branch
else
  BASE="$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null \
          | sed 's@^refs/remotes/origin/@@')"
  [ -z "$BASE" ] && BASE=main           # fall back to the repo default branch
fi
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

Single commit: `SHA="$(git rev-parse --verify "$REF^{commit}")" || exit 1; DIFF_CMD="git show $SHA"`. Range: `START="$(git rev-parse --verify "$RANGESTART^{commit}")" || exit 1; DIFF_CMD="git diff $START"` (e.g. `$RANGESTART` is `HEAD~3` for "last 3 commits"). `git rev-parse --verify` rejects a non-ref argument, blocking a metacharacter-laden string from reaching the embedded command.

Edge cases:
- **On the base branch with no commits ahead** (e.g. `main`, no PR): merge-base is `HEAD`, so `DIFF_CMD` reduces to the uncommitted diff — review what's there.
- **Empty target** (no commits ahead, no uncommitted changes): report "nothing to review" and stop.
- **PR base only on remote**: `git fetch origin <BASE>` first if `origin/<BASE>` is missing, then resolve.

### Capturing an inline artifact (KIND=plan/doc/generic)

Write the artifact's exact text to a temp file once, and point both evaluators at it. The content is **data, not a command** — it is never executed, so no injection concern, but still quote the path when referencing the file.

```bash
ARTIFACT="$(mktemp)"
cat > "$ARTIFACT" <<'EOF'
<the plan / document / artifact text, verbatim>
EOF
```

## 2. Review lens (by KIND)

The KIND fixes the criteria and the verdict vocabulary. Pass both to BOTH evaluators so they judge on the same axes. All kinds classify findings **P0–P3**.

| KIND | Criteria — what "good" means | Verdict |
|------|------------------------------|---------|
| code | correctness, security, data-loss / rollback, races, fail-open, regressions | `SAFE` / `NEEDS_CHANGES` |
| plan | design soundness, completeness, feasibility, risks, sequencing, hidden assumptions | `PLAN_APPROVED` / `REVISE_PLAN` |
| doc | accuracy, clarity, gaps, audience fit, internal consistency | `APPROVED` / `REVISE` |
| generic | state the criteria up front — what would make *this* artifact good | findings only; no forced verdict |

**Verifiable vs non-verifiable** (`rules/evaluation-integrity.md`). `code` is largely verifiable (tests, types, compilation) so a binary verdict is meaningful. `plan` / `doc` / `generic` are partly or non-verifiable: do **not** converge on one "right" answer — surface trade-offs and 2–3 options where the evaluators differ, and prefer `REVISE` / findings over a confident pass when the call is a matter of judgment.

## 3. Evaluators

Both review the SAME artifact, briefed with the KIND's criteria + verdict vocabulary. Spawn in parallel (one response) and wait for both before synthesizing.

### Claude subagent

- **code** → `Agent` with `subagent_type: adversarial-reviewer` (persona at `~/.claude/agents/adversarial-reviewer.md`). Brief it to run `DIFF_CMD` and review only that output.
- **plan / doc / generic** → same skeptical stance, briefed as a general critical reviewer: give it the artifact (the temp-file path to read, or the file paths), the KIND's criteria and verdict vocabulary, and P0–P3. Reuse the `adversarial-reviewer` persona but override its code-specific criteria/verdict in the brief, or fall back to `subagent_type: general-purpose`.

Always pass the resolved `TARGET` and any extra review focus from the user.

### Codex

- **code (diff)** → `codex review` custom-prompt mode with the embedded `DIFF_CMD` (its flags `--uncommitted`/`--base`/`--commit` are mutually exclusive with a custom prompt, so the persona could not ride along with them):

```bash
LOG="/tmp/ai-roots-review-codex-$(date +%Y%m%d-%H%M%S).log"
PROMPT="$(mktemp)"
{
  cat "$HOME/.claude/agents/adversarial-reviewer.md"
  printf '\n\n---\nObtain the review target by running exactly this command:\n\n    %s\n\nReview ONLY the diff that command produces. Apply the persona above (security-first, P0–P3). End with VERDICT: SAFE | NEEDS_CHANGES.\n' "$DIFF_CMD"
} > "$PROMPT"

# A hung codex never exits, so its run_in_background completion notification never
# fires and the main session waits forever (124 on expiry). macOS lacks coreutils
# `timeout` unless brew-installed (`gtimeout`). Store ONLY the binary name — a
# "timeout 1200" string would run as one command (zsh does not word-split it).
TIMEOUT_BIN=""
if command -v timeout >/dev/null 2>&1; then TIMEOUT_BIN=timeout
elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT_BIN=gtimeout; fi

# codex review at xhigh writes NOTHING to a non-TTY until it finishes (often
# several minutes); an empty log mid-run is normal, NOT a hang — do not kill it,
# wait for the completion notification or the timeout (the only hang guard). gpt-5.5
# is the default model, so no -m / model override is needed.
if [ -n "$TIMEOUT_BIN" ]; then
  "$TIMEOUT_BIN" 1200 codex review -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
else
  codex review -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
fi
CODEX_EXIT=$?
cat "$LOG"
echo "codex exit: $CODEX_EXIT (124 = timed out)"
```

- **plan / doc / generic** → `codex exec` (the general non-interactive path; `codex review` is git-diff-only). Embed the artifact's contents and the KIND's lens:

```bash
LOG="/tmp/ai-roots-review-codex-$(date +%Y%m%d-%H%M%S).log"
PROMPT="$(mktemp)"
{
  cat "$HOME/.claude/agents/adversarial-reviewer.md"
  printf '\n\n---\nYou are reviewing a %s, not code. Apply the persona above (skeptical, adversarial), but judge on these criteria: %s. Classify findings P0–P3 and end with VERDICT: %s.\nReview ONLY the artifact between the markers below.\n\n===== BEGIN ARTIFACT: %s =====\n' "$KIND" "$CRITERIA" "$VERDICT_VOCAB" "$TARGET"
  cat "$ARTIFACT"   # or: for f in $FILES; do echo "--- $f ---"; cat "$f"; done
  printf '\n===== END ARTIFACT =====\n'
} > "$PROMPT"

TIMEOUT_BIN=""
if command -v timeout >/dev/null 2>&1; then TIMEOUT_BIN=timeout
elif command -v gtimeout >/dev/null 2>&1; then TIMEOUT_BIN=gtimeout; fi

# read-only sandbox: review must not modify the workspace. gpt-5.5 is the default
# model. Same silence-is-not-a-hang rule and plain redirect as the review block.
if [ -n "$TIMEOUT_BIN" ]; then
  "$TIMEOUT_BIN" 1200 codex exec --sandbox read-only -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
else
  codex exec --sandbox read-only -c model_reasoning_effort=xhigh - < "$PROMPT" > "$LOG" 2>&1
fi
CODEX_EXIT=$?
cat "$LOG"
echo "codex exit: $CODEX_EXIT (124 = timed out)"
```

Common to both:
- `run_in_background: true` so the main session is notified when Codex exits.
- **Silence is not a hang.** At xhigh, codex streams nothing to a non-TTY (the background log) until it finishes — minutes of an empty log is normal. Do NOT kill it on silence; wait for the completion notification or the `timeout`. (Verified: background `codex review` and `codex exec` both complete fine; the `timeout` is the backstop for a genuinely hung run.)
- **Read `$CODEX_EXIT`.** `124` = timed out: treat Codex as unavailable, proceed with the Claude evaluator, and note in the synthesis that only one reviewer ran (and that codex timed out). Never drop a timeout as if codex returned a clean verdict.
- If `codex` is not on `PATH`, skip it and note only one reviewer ran.

### Parallelism

Spawn the Agent call and the Bash invocation in the same response so they run concurrently. Wait for both before producing the synthesis.

## 4. Synthesis

Apply `rules/evaluation-integrity.md` §Multi-advisor synthesis. The output MUST separate three buckets:

1. **Agreed** — findings that appeared in BOTH evaluators. Highest confidence.
2. **Conflicting** — findings flagged by only one evaluator, or where evaluators disagree on severity / cause / fix. Single-evaluator findings belong here, not in Agreed. Silence is not agreement.
3. **Chosen direction + rationale** — the decision given the conflicts, and why. If a conflict is unresolved, say so and escalate to the user rather than picking silently.

Preserve each evaluator's severity (P0–P3) and verdict; do not re-rank to look consistent — disagreement is itself signal. For non-verifiable kinds (plan/doc/generic), prefer presenting trade-offs and options over a single confident verdict.

## Extra instructions

The user's *scope* is resolved once into the artifact (see step 1) — not passed around as words. Any additional *review focus* ("watch the auth path", "is the rollback safe?") is passed to BOTH evaluators verbatim, alongside the same artifact. Do not paraphrase or trim it.

## Anti-patterns

- Assuming "review" means a code diff. Detect the KIND first; a plan or document is a first-class target.
- Re-describing an inline plan/artifact separately to each evaluator — they then review different text. Capture it to one shared file first.
- Running only one evaluator and calling it a "review" — that defeats the cross-provider purpose. If Codex is unavailable, say so explicitly.
- Giving the two evaluators different artifacts or different criteria — both must judge the same artifact on the same axes.
- Forcing a binary verdict on a non-verifiable artifact (plan/doc/generic) instead of surfacing trade-offs and options.
- Smoothing over disagreements in synthesis. The Conflicting bucket exists precisely because the synthesizer is biased toward sounding confident.
- Promoting a single-evaluator finding to "Agreed" because nothing contradicted it.
- Auto-applying fixes from either evaluator. Report findings; the main session decides what to apply.
