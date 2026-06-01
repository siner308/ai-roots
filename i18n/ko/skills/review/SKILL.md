---
name: review
description: "[ai-roots] ai-roots 스킬 세트가 제공하는 두 평가자 코드 리뷰. 리뷰 타겟을 먼저 결정하고(기본값은 현재 브랜치가 base 대비 제안하는 변경 — 즉 PR diff에 로컬 uncommitted 편집을 더한 것이지만, 명시적 base나 특정 커밋, uncommitted 전용 범위도 지정 가능), 그 동일한 diff에 대해 Claude Code subagent와 Codex 리뷰를 병렬로 띄운 뒤 rules/evaluation-integrity.md §Multi-advisor synthesis의 Agreed / Conflicting / Chosen-direction 포맷으로 결과를 종합한다. 사용자가 대기 중이거나 제안된 변경의 리뷰를 요청하고 Claude와 Codex가 둘 다 있을 때 사용한다."
---

# /review (ai-roots)

독립적인 두 평가자 리뷰. 두 평가자는 **같은 결정된 타겟**을 리뷰하며, 종합 단계 전까지 서로의 출력을 보지 않는다.

타겟은 uncommitted diff로 하드코딩되어 있지 않다. 기본값은 이 브랜치가 제안하는 변경 전체 — 커밋된 브랜치 변경에 로컬 uncommitted 편집을 더한 것 — 를 base 브랜치(PR이 있으면 PR base) 대비로 잰 것이다. 사용자가 범위를 재정의할 수 있다.

## 범위 결정

평가자를 띄우기 **전에** 메인 세션에서 타겟을 결정한다. 두 값을 만든다: `DIFF_CMD`(리뷰할 diff를 정확히 뱉는 git 명령)와 사람이 읽을 수 있는 `TARGET` 설명. 두 평가자에게 *같은* `DIFF_CMD`를 넘겨 범위를 맞춘다.

모드는 사용자 인자로 고른다. 기본은 branch-vs-base.

| 사용자 인자 | 모드 | `DIFF_CMD` |
|---------------|------|------------|
| _(없음)_ | branch vs base | `git diff <merge-base SHA>` |
| `--base <ref>` | branch vs 명시적 base | `git diff <merge-base SHA>` |
| `--uncommitted` | 워킹 트리만 | `git diff HEAD` (untracked 포함) |
| `--commit <sha>` | 커밋 하나 | `git show <commit SHA>` |
| 뒤따르는 `<paths…>` | 어떤 모드든 좁힘 | ` -- '<path>'…` 추가 (single-quote) |

`git diff <merge-base SHA>`는 fork point부터 **워킹 트리**까지를 diff하므로, 커밋된 브랜치 변경과 uncommitted 로컬 편집을 한 diff에 담는다 — 바로 "PR diff + 로컬 변경"이다. `codex review --base`가 내부적으로 하는 일이 이것이다. 우리는 merge-base를 직접 구해 그 명령을 박아 넣어, 페르소나(아래)가 명령과 함께 따라가게 한다.

**Injection 안전 — STRICT.** `DIFF_CMD`는 두 평가자 모두에게 셸에서 실행하라고 지시하는 프롬프트에 박힌다. git ref나 브랜치 이름에는 셸 메타문자(`;`, `$( )`, 백틱)가 정당하게 들어갈 수 있어서, raw ref를 명령에 그대로 끼워 넣으면 command injection 통로가 된다 — 특히 `--base <ref>`와 신뢰할 수 없는 fork에서 온 PR base 이름이 위험하다. 막는 방법: 모든 ref를 **메인 세션에서 commit SHA로 먼저 풀고**(거기서는 ref가 평범한 따옴표 친 셸 변수라 injection이 안 된다), 16진수 SHA만 박는다. SHA에는 메타문자가 없다. raw ref는 절대 박지 말고, path filter는 single-quote 한다(single quote가 든 경로는 거부).

### Base ref 자동 감지 (branch-vs-base 모드)

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

`--commit <sha>`의 경우, 먼저 풀고 검증한다: `SHA="$(git rev-parse --verify "$ARG^{commit}")" || exit 1; DIFF_CMD="git show $SHA"`. `git rev-parse --verify`는 ref가 아닌 인자를 거부하므로, 메타문자가 박힌 문자열이 박히는 명령까지 가닿는 것도 막아준다.

엣지 케이스:
- **base 브랜치 위에 있고 앞선 커밋이 없을 때** (예: `main` 위, PR 없음): merge-base가 `HEAD`라서 `DIFF_CMD`가 uncommitted diff로 줄어든다. 합리적이다 — 거기 있는 걸 리뷰한다.
- **타겟이 비었을 때** (앞선 커밋도 없고 uncommitted 변경도 없음): "nothing to review"라 보고하고 멈춘다. 빈 diff에 평가자를 띄우지 않는다.
- **PR base가 remote에만 있을 때**: `origin/<BASE>`가 없으면 먼저 `git fetch origin <BASE>` 한 뒤 푼다.

리뷰 전에 결정된 `TARGET`을 사용자에게 알려준다 (예: "Reviewing `feature` vs `origin/main` (PR #123) + local changes").

## 평가자

### 1. Claude Code subagent

`Agent` 도구를 `subagent_type: adversarial-reviewer`로 호출한다 (페르소나는 `~/.claude/agents/adversarial-reviewer.md`). `DIFF_CMD`를 실행해 diff를 얻고 그 출력만 리뷰하라고, 페르소나의 security-first P0–P3 분류를 적용하라고 브리핑한다. 결정된 `TARGET`과 사용자가 준 범위를 프롬프트에 넘긴다.

`adversarial-reviewer` 에이전트가 등록돼 있지 않으면 `subagent_type: general-purpose`로 fallback하고 페르소나 본문을 프롬프트에 인라인한다.

### 2. Codex review

`codex review`의 `--uncommitted` / `--base` / `--commit` 플래그는 커스텀 프롬프트와 함께 못 쓴다(서로 배타적). 그래서 페르소나를 같이 태울 수 없다. 대신 **custom-prompt 모드**를 쓰고 `DIFF_CMD`를 박아, codex가 우리 페르소나로 정확히 같은 범위를 리뷰하게 한다:

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

- 모델은 `-c model=…`로 지정한다. `codex review`는 `-m`을 **받지 않는다**.
- `--uncommitted` / `--base` 플래그는 안 쓴다 — 범위는 박힌 명령 안에 있고, codex가 돌리기 전에 로컬 셸이 `$(…)`를 먼저 펼치지 않도록 single-quote 한다.
- `run_in_background: true`를 써서 Codex가 끝날 때 메인 세션이 알림을 받게 한다.
- **codex exit status를 읽는다** (`$CODEX_EXIT`). `124`는 리뷰가 타임아웃됐다는 뜻 — Codex가 없는 것처럼 취급한다: Claude 평가자만으로 진행하고, 평가자가 하나만 돌았다(그리고 codex가 타임아웃됐다)는 걸 종합에 적는다. 타임아웃을 codex가 깨끗한 판정을 낸 것처럼 조용히 버리지 않는다.
- `codex`가 `PATH`에 없으면 이 평가자를 건너뛰고, 평가자가 하나만 돌았다고 종합에 적는다.

### 병렬 실행

Agent 호출과 Bash 호출을 같은 응답에서 띄워 동시에 돌린다. 둘 다 끝나길 기다린 뒤 종합을 낸다.

## 종합

`rules/evaluation-integrity.md` §Multi-advisor synthesis를 적용한다. 출력은 세 버킷으로 반드시 나눈다:

1. **Agreed** — 두 평가자에 모두 나온 발견. 신뢰도 최고.
2. **Conflicting** — 한 평가자만 짚었거나, 심각도/원인/수정에서 평가자끼리 의견이 갈린 발견. 한 평가자만의 발견은 Agreed가 아니라 여기 들어간다. 침묵은 동의가 아니다.
3. **Chosen direction + rationale** — 충돌을 두고 내린 결정과 그 이유. 충돌이 안 풀렸으면 그렇다고 말하고 조용히 고르지 말고 사용자에게 에스컬레이션한다.

각 발견마다 원래 평가자가 매긴 심각도 분류(P0–P3)를 보존한다. 평가자끼리 일관돼 보이게 발견의 순위를 다시 매기지 않는다 — 심각도에 대한 이견 자체가 신호다.

## 범위 (사용자 재정의)

사용자가 추가로 준 범위가 있으면 두 평가자에게 그대로 넘긴다. 바꿔 말하거나 줄이지 않는다. 뒤따르는 path filter는 ` -- <paths>` suffix로 두 평가자의 `DIFF_CMD`를 함께 좁힌다.

## 안티패턴

- 사용자가 커밋된 작업이 있는 feature 브랜치에 있는데 uncommitted 전용으로 기본값을 잡는 것 — 기본 타겟은 branch-vs-base이고 둘 다 포함한다.
- 평가자 하나만 돌리고 결과를 "리뷰"라 부르는 것 — cross-provider라는 목적이 무너진다. Codex가 없으면 그렇다고 명시한다.
- 두 평가자에게 다른 범위를 넘기는 것 — 둘 다 같은 `DIFF_CMD`의 diff를 리뷰해야 한다.
- 종합에서 이견을 매끄럽게 덮는 것. Conflicting 버킷이 있는 이유가 바로 종합자가 출력을 자신만만하게 들리게 만들려는 편향을 갖기 때문이다.
- 아무도 반박하지 않았다는 이유로 한 평가자만의 발견을 "Agreed"로 올리는 것.
- 어느 평가자의 수정이든 자동으로 적용하는 것. 발견을 보고하고, 무엇을 적용할지는 메인 세션이 정한다.
