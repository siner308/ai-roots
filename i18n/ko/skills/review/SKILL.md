---
name: review
description: "[ai-roots] 무엇이든 리뷰하는 두 평가자 리뷰 — 코드 변경, Claude가 방금 만든 plan·설계, 문서, config, 그 외 리뷰 가능한 무엇이든. 자연어 요청에서 산출물 종류를 판별하고, 두 평가자가 동일하게 접근할 하나의 구체적 산출물(git diff, 파일, 또는 temp 파일로 고정한 인라인 텍스트)로 결정한 뒤, 그 동일한 산출물에 대해 Claude Code subagent와 Codex를 종류별 기준으로 병렬 실행하고 rules/evaluation-integrity.md §Multi-advisor synthesis의 Agreed / Conflicting / Chosen-direction 포맷으로 종합한다. 대기 중인 코드, plan, 문서, 그 외 산출물의 리뷰를 요청하고 Claude와 Codex가 둘 다 있을 때 사용한다."
---

# /review (ai-roots)

**무엇이든** 독립적으로 리뷰하는 두 평가자 리뷰. 두 평가자는 **같은 결정된 산출물**을 보며, 종합 단계 전까지 서로의 출력을 보지 않는다.

diff에 한정되지 않는다. 산출물은 코드 변경, Claude가 방금 만든 plan·설계, 문서, config, 데이터셋 — 리뷰 가능한 무엇이든 될 수 있다. 기계 장치는 늘 같다 — 두 독립 평가자 → Agreed / Conflicting / Chosen 종합. 산출물에 따라 달라지는 건 딱 둘: **어떻게 얻느냐**와 그것에게 **무엇이 "좋음"이냐**.

## 1. 산출물 결정

사용자의 자연어 요청에서 **KIND**를 판별하고, 두 평가자가 **동일하게** 접근할 하나의 구체적 산출물과 사람이 읽을 `TARGET`을 만든다. 메인 세션이 한 번 결정하고, 평가자는 요청을 다시 해석하지 않는다 — 그래야 두 리뷰가 비교 가능하다.

KIND — 가장 잘 맞는 것을 고른다:

- **code** — "내 변경/PR/이 브랜치/그 커밋 봐줘", 또는 repo의 코드에 관한 요청. repo 안이고 대상이 코드면 기본값.
- **plan** — "이 plan / 방금 쓴 plan / 이 접근 / 이 설계 봐줘". 산출물이 *이 대화에서* Claude가 만든 텍스트인 경우가 많다.
- **doc** — 산문 문서, README, 스펙, PRD, 제안서.
- **generic** — 그 외 전부: config, 데이터셋, 결정, 체크리스트. 포괄.

산출물을 구체적이고 **공유된** 형태로 만든다(두 평가자에게 동일 바이트):

- **code** → `DIFF_CMD`를 결정한다(코드 범위 결정 참고). 두 평가자가 실행한다.
- 이 대화에만 있는 **인라인 plan/doc/generic**(파일 없음) → 그 텍스트를 그대로 temp 파일에 고정한다: `ARTIFACT="$(mktemp)"; cat > "$ARTIFACT" <<'EOF' … EOF`. 둘 다 그 파일을 읽는다. 핵심이다: 인라인 plan을 각 평가자에게 다시 설명하면 서로 다른 텍스트가 된다 — 한 번 고정한다.
- **파일로 된 plan/doc/generic** → 경로(들). 둘 다 읽는다.

리뷰 전에 결정된 `TARGET`을 사용자에게 알려준다(예: "migration plan 리뷰 (인라인, 42줄)", "`feature` vs `origin/main` (PR #123) + 로컬 변경 리뷰", "`docs/rfc-007.md` 리뷰"). 모호하면 가장 그럴듯한 KIND를 고르고 `TARGET`을 교정 지점으로 삼는다. 정말 풀 수 없으면 한 가지 확인 질문을 한다.

### 코드 범위 결정 (KIND=code)

사용자가 범위를 자연어로 말하면 의도로 매핑한 뒤 SHA 기반 명령으로 푼다:

| 사용자가 하는 말 (예시) | 의도 | `DIFF_CMD` |
|----------------------|--------|------------|
| _(없음)_, "내 변경 봐줘", "이 브랜치" | branch vs base | `git diff <merge-base SHA>` |
| "vs main", "develop 대비", "<ref>랑 비교" | branch vs 명시한 base | `git diff <merge-base SHA>` |
| "uncommitted", "워킹 트리", "아직 커밋 안 한 거" | 워킹 트리만 | `git diff HEAD` (untracked 포함) |
| "마지막 커밋", "HEAD", "커밋 <sha>" | 커밋 하나 | `git show <SHA>` |
| "최근 3개 커밋", "<ref> 이후" | 커밋 범위 | `git diff <범위 시작 SHA>` |
| "X 파일만", "<path>만" | 위 어떤 것이든 좁힘 | ` -- '<path>'…` 추가 |

범위가 비었거나 모호하면 기본은 **branch-vs-base**. `git diff <merge-base SHA>`는 fork point부터 워킹 트리까지를 diff하므로 커밋된 브랜치 변경과 uncommitted 로컬 편집을 한 diff에 담는다 — "PR diff + 로컬 변경".

**Injection 안전 — STRICT.** `DIFF_CMD`는 평가자가 셸에서 실행하는 프롬프트에 박힌다. git ref나 브랜치 이름에는 셸 메타문자(`;`, `$( )`, 백틱)가 정당하게 들어갈 수 있어 raw ref를 끼우면 command injection 통로다 — 특히 명시한 base나 신뢰할 수 없는 fork의 PR base. 모든 ref를 **메인 세션에서 commit SHA로 풀고**(거기서는 따옴표 친 셸 변수라 injection 불가) 16진수 SHA만 박는다. raw ref는 절대 박지 말고 path filter는 single-quote 한다(single quote 든 경로는 거부).

Base ref 자동 감지(기본 / 명시 base). 명시한 base("vs <ref>")면 `BASE`를 그 ref로 두고 감지를 건너뛴다:

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

커밋 하나: `SHA="$(git rev-parse --verify "$REF^{commit}")" || exit 1; DIFF_CMD="git show $SHA"`. 범위: `START="$(git rev-parse --verify "$RANGESTART^{commit}")" || exit 1; DIFF_CMD="git diff $START"` (예: "최근 3개 커밋"이면 `$RANGESTART`는 `HEAD~3`). `git rev-parse --verify`는 ref가 아닌 인자를 거부해 메타문자 문자열이 박히는 명령까지 가닿는 것도 막는다.

엣지 케이스:
- **base 브랜치 위에 앞선 커밋이 없을 때**(예: `main`, PR 없음): merge-base가 `HEAD`라 `DIFF_CMD`가 uncommitted diff로 줄어든다 — 거기 있는 걸 리뷰한다.
- **타겟이 비었을 때**(앞선 커밋도 uncommitted도 없음): "nothing to review"라 보고하고 멈춘다.
- **PR base가 remote에만 있을 때**: `origin/<BASE>`가 없으면 먼저 `git fetch origin <BASE>` 한 뒤 푼다.

### 인라인 산출물 고정 (KIND=plan/doc/generic)

산출물의 정확한 텍스트를 temp 파일에 한 번 쓰고, 두 평가자를 그 파일로 향하게 한다. 내용은 **명령이 아니라 데이터**라 실행되지 않으므로 injection 우려는 없지만, 파일 경로는 그래도 따옴표 친다.

```bash
ARTIFACT="$(mktemp)"
cat > "$ARTIFACT" <<'EOF'
<the plan / document / artifact text, verbatim>
EOF
```

**빈 산출물.** 고정한 파일이 비었거나(인라인 텍스트가 공백) 파일 기반 산출물이 읽을 파일로 풀리지 않으면, "nothing to review"라 보고하고 멈춘다 — 빈 code 타겟과 동일. 아무것도 없는데 평가자를 띄우지 않는다.

## 2. 리뷰 렌즈 (KIND별)

KIND가 기준과 verdict 어휘를 고정한다. 둘을 두 평가자 모두에게 넘겨 같은 축에서 판단하게 한다. 모든 종류는 발견을 **P0–P3**로 분류한다.

| KIND | 기준 — "좋음"의 의미 | Verdict |
|------|------------------------------|---------|
| code | 정확성, 보안, 데이터 손실/롤백, race, fail-open, 회귀 | `SAFE` / `NEEDS_CHANGES` |
| plan | 설계 타당성, 완전성, 실현성, 리스크, 순서, 숨은 가정 | `PLAN_APPROVED` / `REVISE_PLAN` |
| doc | 정확성, 명료성, 누락, 대상 적합성, 내부 일관성 | `APPROVED` / `REVISE` |
| generic | 기준을 시작 시 명시 — *이* 산출물이 좋으려면 무엇이 필요한가 | 발견 위주; verdict 강요 안 함 |

**검증 가능 vs 검증 불가**(`rules/evaluation-integrity.md`). `code`는 대체로 검증 가능(테스트·타입·컴파일)이라 이진 verdict가 의미 있다. `plan` / `doc` / `generic`은 부분적으로 또는 전혀 검증 불가다: 하나의 "정답"으로 수렴하지 **말고** — 평가자가 갈리는 지점은 트레이드오프와 2~3개 옵션을 제시하고, 판단의 문제일 때는 자신만만한 통과보다 `REVISE` / 발견을 택한다.

## 3. 평가자

둘 다 같은 산출물을 KIND의 기준 + verdict 어휘로 브리핑받아 리뷰한다. 한 응답에서 병렬로 띄우고, 종합 전에 둘 다 끝나길 기다린다.

### Claude 서브에이전트

- **code** → `Agent`를 `subagent_type: adversarial-reviewer`로(페르소나 `~/.claude/agents/adversarial-reviewer.md`). `DIFF_CMD`를 실행해 그 출력만 리뷰하라고 브리핑한다.
- **plan / doc / generic** → 같은 회의적 자세로, 범용 critical reviewer로 브리핑: 산출물(읽을 temp 파일 경로 또는 파일 경로들), KIND의 기준과 verdict 어휘, P0–P3을 준다. `adversarial-reviewer` 페르소나를 재사용하되 코드 전용 기준/verdict를 브리핑에서 덮거나, `subagent_type: general-purpose`로 fallback.

항상 결정된 `TARGET`과 사용자가 준 추가 리뷰 초점을 넘긴다.

### Codex

- **code (diff)** → `codex review` custom-prompt 모드에 `DIFF_CMD`를 박는다(`--uncommitted`/`--base`/`--commit`은 커스텀 프롬프트와 배타적이라 페르소나를 같이 못 태운다):

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

- **plan / doc / generic** → `codex exec`(범용 비대화형 경로; `codex review`는 git-diff 전용). 산출물 내용과 KIND의 렌즈를 박는다. 실행 전에 블록이 쓰는 셸 변수를 설정한다: `KIND`, `CRITERIA`, `VERDICT_VOCAB`은 §2 표에서, 그리고 `ARTIFACT`(1단계의 인라인 temp 파일) 또는 `FILES`(파일 기반 경로들의 bash 배열):

```bash
LOG="/tmp/ai-roots-review-codex-$(date +%Y%m%d-%H%M%S).log"
PROMPT="$(mktemp)"
{
  cat "$HOME/.claude/agents/adversarial-reviewer.md"
  printf '\n\n---\nYou are reviewing a %s, not code. Apply the persona above (skeptical, adversarial), but judge on these criteria: %s. Classify findings P0–P3 and end with VERDICT: %s.\nReview ONLY the artifact between the markers below.\n\n===== BEGIN ARTIFACT: %s =====\n' "$KIND" "$CRITERIA" "$VERDICT_VOCAB" "$TARGET"
  cat "$ARTIFACT"   # inline; for file-backed use an array: for f in "${FILES[@]}"; do printf '\n--- %s ---\n' "$f"; cat "$f"; done
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

둘 다 공통:
- `run_in_background: true`로 Codex가 끝날 때 메인 세션이 알림을 받게 한다.
- **침묵은 hang이 아니다.** xhigh에서 codex는 끝날 때까지 non-TTY(백그라운드 로그)에 아무것도 안 쓴다 — 몇 분간 빈 로그는 정상이다. 침묵에 죽이지 말고 완료 알림이나 `timeout`을 기다린다. (실측: background `codex review`·`codex exec` 둘 다 정상 완주하며, `timeout`이 진짜 hang의 backstop이다.)
- **`$CODEX_EXIT`를 읽는다.** `124` = 타임아웃: Codex가 없는 것으로 취급하고 Claude 평가자만으로 진행하며, 평가자가 하나만 돌았다(그리고 codex가 타임아웃됐다)고 종합에 적는다. 타임아웃을 깨끗한 판정처럼 버리지 않는다.
- `codex`가 `PATH`에 없으면 건너뛰고 평가자가 하나만 돌았다고 적는다.

### 병렬 실행

Agent 호출과 Bash 호출을 같은 응답에서 띄워 동시에 돌린다. 둘 다 끝난 뒤 종합한다.

## 4. 종합

`rules/evaluation-integrity.md` §Multi-advisor synthesis를 적용한다. 출력은 세 버킷으로 반드시 나눈다:

1. **Agreed** — 두 평가자에 모두 나온 발견. 신뢰도 최고.
2. **Conflicting** — 한 평가자만 짚었거나, 심각도/원인/수정에서 갈린 발견. 한 평가자만의 발견은 Agreed가 아니라 여기. 침묵은 동의가 아니다.
3. **Chosen direction + rationale** — 충돌을 두고 내린 결정과 이유. 안 풀린 충돌은 조용히 고르지 말고 사용자에게 에스컬레이션한다.

각 평가자의 심각도(P0–P3)와 verdict를 보존하고, 일관돼 보이게 순위를 다시 매기지 않는다 — 이견 자체가 신호다. 검증 불가 종류(plan/doc/generic)는 하나의 자신만만한 verdict보다 트레이드오프와 옵션 제시를 택한다.

## 추가 지시

사용자의 *범위*는 산출물로 한 번 결정된다(1단계) — 말로 들고 다니지 않는다. 추가 *리뷰 초점*("auth 경로 주의", "롤백 안전한가?")은 같은 산출물과 함께 두 평가자에게 그대로 넘긴다. 바꿔 말하거나 줄이지 않는다.

## 안티패턴

- "리뷰" = 코드 diff라고 단정. 먼저 KIND를 판별한다 — plan·문서도 1급 대상이다.
- 인라인 plan/산출물을 각 평가자에게 따로 설명 — 그러면 서로 다른 텍스트를 리뷰한다. 먼저 하나의 공유 파일로 고정한다.
- 평가자 하나만 돌리고 "리뷰"라 부르기 — cross-provider 목적이 무너진다. Codex가 없으면 명시한다.
- 두 평가자에게 다른 산출물·다른 기준을 주기 — 둘 다 같은 산출물을 같은 축으로 봐야 한다.
- 검증 불가 산출물(plan/doc/generic)에 이진 verdict를 강요 — 트레이드오프와 옵션을 제시한다.
- 종합에서 이견 매끄럽게 덮기. Conflicting 버킷이 있는 이유가 종합자가 자신만만하게 들리려는 편향 때문이다.
- 아무도 반박 안 했다고 한 평가자 발견을 "Agreed"로 올리기.
- 어느 평가자의 수정이든 자동 적용. 발견을 보고하고 무엇을 적용할지는 메인 세션이 정한다.
