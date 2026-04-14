# GitHub Stacked PRs

When work decomposes naturally into a sequence of steps — where step N must land before step N+1 can be reviewed — offer GitHub's Stacked PR feature before opening any PRs.

## When to offer

Ask whether to use Stacked PRs when:
- The work spans 2+ PRs that depend on each other (e.g., schema migration → API change → frontend update)
- A single PR would exceed ~400 lines of meaningful diff
- Work is already planned as sequential phases (backend first, then frontend; infrastructure first, then application code)
- The user is about to create a PR that explicitly builds on another open PR

Do NOT offer when:
- Work is truly independent (no ordering constraint) — use subagents or teams instead
- The user has already created the PRs conventionally
- There is only one PR to open

## How to ask

After proposing the implementation plan but before creating any branches or PRs:

> "이 작업은 순서가 있는 여러 PR로 나눌 수 있습니다. GitHub Stacked PR을 사용하시겠습니까? 각 PR이 이전 PR을 기반으로 쌓여서 리뷰어가 레이어별로 집중해서 볼 수 있습니다."

Ask once. If the user declines, proceed with the conventional single-PR or sequential-PR approach without mentioning stacks again.

## Key commands

```bash
gh stack init [name]   # Start a new stack
gh stack add [name]    # Create a new layer (branch + commits)
gh stack push          # Push all branches in the stack
gh stack submit        # Open PRs for each layer
```

Requires the gh-stack extension. If not installed:
```bash
npx skills add github/gh-stack
```

## Rules

- Offer stacks as a suggestion, not a default. The user may have reasons to prefer a flat PR structure.
- Each layer should be independently reviewable: a focused diff with a clear purpose.
- Bottom PR targets `main`; each subsequent PR targets the one below it.
- GitHub handles automatic rebase of upper layers when a lower PR merges.
