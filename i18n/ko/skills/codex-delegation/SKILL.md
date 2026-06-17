---
name: codex-delegation
description: "OpenAI Codex CLI에 작업을 위임할 때 적용 — Claude가 막힌 뒤의 rescue 디버깅(three-turn 상한), cross-provider/보안 민감 리뷰, 최신 docs 웹 리서치, 또는 범위가 정해진/무인 구현. 모드와 플래그 선택, reasoning effort, rescue protocol, plan-stage review, 실행 메커니즘을 다룬다. Codex CLI가 PATH에 있을 때만 트리거할 것."
---


# Codex Delegation

> **Applicability** — 이 규칙은 OpenAI Codex CLI가 Claude Code와 함께 PATH에 있을 때 적용된다. Codex가 없으면 `/review` 스킬은 단일 평가자 리뷰(Claude subagent만)로 fallback한다 — cross-provider generator-vs-evaluator 분리는 약해지지만, 아래 rules 측 정책은 여전히 Claude 측 작업에 적용된다.

Cross-provider 위임은 세 가지 목적에 쓰인다:

1. **Bias breaking** — 단일 학습 분포가 놓치는 맹점을 잡는다(evaluation-integrity.md의 generator-vs-evaluator 분리를 모델 패밀리 너머로 확장한 것).
2. **Anchor breaking** — Claude가 어려운 문제에서 루프를 돌 때, 새 스택이 추론 앵커를 리셋한다.
3. **Ecosystem capability** — Claude Code가 자체적으로 들고 있지 않은 OpenAI 네이티브 도구(이미지 생성, OpenAI 전용 모델)에 접근한다.

앞의 둘은 reliability routing을, 셋째는 capability routing을 동기 부여한다.

## 진입점

Codex 작업은 두 갈래로 들어온다. 요청된 방식에 맞춰 진입점을 고른다.

**리뷰 → 항상 `/review` 스킬.** 리뷰 부류 작업은 모두 `/review`(`skills/review/SKILL.md`)를 쓴다: 하나의 공유 산출물을 결정한 뒤 Claude subagent와 Codex 실행을 그 산출물에 병렬로 띄우고 evaluation-integrity.md §Multi-advisor synthesis에 따라 종합한다. 리뷰의 단일 진입점이다 — `codex review`나 `/codex:review`를 직접 부르지 마라.

**그 외 → "이거 codex로 해줘" 자연어 위임.** intent에 맞춰 신뢰 가능한 호출로 매핑한다. 세 경로 모두 codex-cli 0.128에서 검증됨:

- **진단 / 막힌 디버깅** → `/codex:rescue`, 또는 Agent 도구의 `subagent_type: "codex:codex-rescue"`. read-only, companion 런타임에서 돌고 완료 신호가 하네스에 배선되어 있다.
- **쓰기 / 리서치 / 범위가 정해진 구현** → 아래 플래그·메커니즘으로 수동 `codex exec`. timeout을 하드닝하면 깨끗하게 exit한다(Codex 실행 메커니즘 참고).

**Footgun — `Skill(codex:rescue)`로 절대 부르지 마라.** 스킬로 부르면 slash 커맨드가 재진입해서 세션이 hang된다. rescue는 `/codex:rescue` 커맨드 또는 Agent 도구의 `subagent_type: "codex:codex-rescue"`로만 호출한다. "Codex 위임이 멈췄다"의 통상적 원인은 망가진 런타임이 아니라 잘못된 진입점이다.

## Reasoning effort 설정

항상 xhigh. 모든 호출에 `-c model_reasoning_effort=xhigh`를 넘긴다.

## 플래그 배치 (codex-cli ≥ 0.125)

`--search`, `-a`/`--ask-for-approval`, `--dangerously-bypass-approvals-and-sandbox`는 **top-level 플래그**이고 subcommand 앞에 온다. `--sandbox`, `--full-auto`, `-c key=value`는 **exec subcommand 플래그**이고 `exec` 뒤에 온다. 위치를 잘못 두면 `error: unexpected argument '--ask-for-approval' found`로 실패한다. `codex --help`와 `codex exec --help`로 확인하라.

```
codex [TOP-LEVEL FLAGS] exec [EXEC FLAGS] -- - < prompt
codex review [REVIEW FLAGS]    # 설계상 read-only; --sandbox / -a 를 받지 않음
```

## 모드 치트시트

`/review`(리뷰)와 `/codex:rescue`(진단)가 아래 해당 행을 대체한다. 나머지 행 — 쓰기, 리서치, 범위가 정해진/무인 구현 — 은 그 intent의 정상 수동 `codex exec` 호출이다.

| Need | Invocation |
|------|------------|
| 독립적 + 보안 민감 리뷰 | `/review` 스킬 |
| 세 번 실패 후 막힘 | `codex exec --sandbox read-only -m gpt-5…` |
| 최신 docs 또는 웹 리서치 | `codex --search -a never exec --sandbox …` |
| 범위가 정해진 구현(workspace edit…) | `codex exec --full-auto -m gpt-5.5 -c mo…` |
| 무인 장시간 구현(worksp…) | `codex --search -a never exec --sandbox …` |
| 명시적 no-sandbox 실행(use… 일 때만) | `codex --search --dangerously-bypass-app…` |

편의를 위해 더 넓은 모드를 고르지 마라. 리서치에는 쓰기 권한이 필요 없다. 이미지 생성에는 ecosystem capability가 필요하지, no-sandbox 접근이 필요한 게 아니다. 의존성 설치, 외부 CLI, 사설 네트워크 호출은 별개의 요구사항이고 brief에 명시해야 한다.

## 라우팅 규칙

**막힌 문제에는 three-turn 상한.** 같은 가설로 4번째 인라인 턴을 시도하지 마라. ruled-out 가설을 모두 포함해서 `/codex:rescue`(read-only)에 위임하라 — Three-Turn Rescue 프로토콜 참고.

**보안 민감 변경에는 adversarial 리뷰.** authentication, authorization, 데이터베이스 쓰기, 네트워크 경계, secret 처리, trust 경계를 건드리는 모든 동작 변경 뒤에는 `/review`를 호출한다. read-only 읽기나 순수 내부 리팩터링은 트리거하지 않는다. 리뷰어 페르소나 — 회의적, 보안 우선, 발견을 P0–P3로 분류, 높은 커버리지에서 critical 이슈가 없을 때만 `VERDICT: SAFE`를 반환 — 는 agents/adversarial-reviewer.md(`~/.claude/agents/`에 설치됨)에 있고, 스킬이 stdin으로 `codex exec --json --sandbox read-only`에 파이프한다(`--json` 이벤트 스트림 덕에 Claude가 codex 진행을 실시간으로 본다; `/review` 스킬 참조).

**Capability routing은 첫 턴에 발동한다.** 이미지 생성, TTS, 그 외 OpenAI 전용 도구 필요는 즉시 Codex로 라우팅한다. 결과물이 이미지나 오디오 산출물일 때 텍스트 기반 우회(ASCII 아트, 손으로 짠 SVG)에 턴을 낭비하지 마라.

## Three-Turn Rescue 프로토콜

1. **Turn 1** — 원래 계획.
2. **Turn 2** — 가설을 수정한다(근본 원인이 다른 계층에 있을 수 있다; parallel-hypothesis-investigation.md 참고).
3. **Turn 3** — 가설 하나 더.
4. **After Turn 3** — `/codex:rescue`(또는 Agent 도구의 `subagent_type: "codex:codex-rescue"`)에 넘긴다: 원래 작업, 시도한 각 가설과 실패 이유, 최소 재현 케이스, ruled-out 파일. companion 플러그인이 없으면 같은 내용을 stdin으로 넣어 `codex exec --sandbox read-only ...`로 fallback한다.

"turn"은 메시지 하나가 아니라 실질적 시도 하나다. 셋을 넘기면 한계 정보가 무너지고 anchoring bias가 굳어진다.

## Codex 실행 메커니즘

이 메커니즘은 수동 `codex exec` 경로(쓰기 / 리서치 / 범위가 정해진 구현, 그리고 companion 플러그인이 없을 때의 모든 실행)에 적용된다. `/codex:rescue`와 `/review`는 아래 관심사를 자체적으로 처리한다.

따로 관리할 관심사 세 가지:

1. **Claude는 codex가 언제 끝나는지 알아야 한다.** `run_in_background: true` Bash를 쓴다; 하네스의 완료 알림이 Claude를 깨운다.
2. **사용자는 codex의 추론을 실시간으로 보고 싶을 수 있다.** 로그 경로를 주고, 자기 터미널에서 `tail -f` 하게 둔다. 실시간 뷰를 Claude 쪽에서 스크립트로 짜지 마라.
3. **codex는 반드시 끝나야 한다.** 멈춘 codex는 절대 exit하지 않으므로 완료 알림이 안 뜨고 메인 세션이 영원히 기다린다. 모든 codex 호출을 timeout으로 감싼다(`timeout <secs> codex …`, 또는 coreutils 없는 macOS에서는 `gtimeout`; 둘 다 없으면 우아하게 degrade). 만료되면 codex는 124로 exit한다 — exit status를 읽고 timeout을 깨끗한 결과가 아니라 codex 사용 불가로 다룬다. 그냥 `timeout`은 직계 자식에게만 신호를 보낸다; codex(node)가 pipe를 쥔 손자 프로세스를 남기면 `| tee`가 EOF를 못 받아, codex가 죽은 뒤에도 백그라운드 작업이 hang된다. 완료 시점에 멈추면 kill-after grace(`gtimeout -k 10 <secs> …`)를 쓰고 `| tee` 대신 파일로 리다이렉트(`> "$LOG" 2>&1`)하라.

```
LOG="/tmp/codex-$(date +%Y%m%d-%H%M%S).log"
Bash(
  run_in_background: true,
  command: "<codex invocation> 2>&1 | tee '$LOG'"
)
# 백그라운드 작업이 끝나면 "$LOG"를 Read 한다.
```

sentinel 없이, Claude 쪽 `tail -f` 없이, split pane 없이. 이전 래퍼가 왜 실패했는지는 lessons/codex-tmux-monitoring.md 참고.

**Stdin-piping 호출**(`exec`, `review`)은 프롬프트를 stdin으로 받는다. 먼저 temp 파일에 쓰고 리다이렉트하라:

```
PROMPT="$(mktemp)"
command cat > "$PROMPT" <<'EOF'
<reviewer prompt or task brief>
EOF
Bash(run_in_background: true, command: "codex exec ... -- - < '$PROMPT' 2>&1 | tee '$LOG'")
```

## Plan 단계 리뷰

두 리뷰어 리뷰는 코드를 쓰기 *전에도* 가치 있다. 산출물이 diff가 아니라 **plan**일 때다. 구현이 시작되면 되돌리기 비싼 설계 결정을 잡아낸다.

**효과를 보는 경우:** plan이 여러 파일 / 새 모듈 / 새 추상화를 건드릴 때; planner가 직접 검증하지 않은 프레임워크나 라이브러리 API에 의존할 때; 구현이 충분히 커서 중간에 버리는 비용이 클 때(≥ 1 PR 또는 ≥ 수백 줄).

**건너뛸 경우:** 모양이 뻔한 한두 파일 편집, 또는 탐색적("X 해보고 어떻게 되나 보자")인 경우.

**포맷:** `VERDICT: PLAN_APPROVED | REVISE_PLAN` (`SAFE | NEEDS_CHANGES`가 아님 — 그건 diff 리뷰 verdict다). 발견은 P0–P3로 분류한다.

**Plan 리뷰는 권고이지 차단이 아니다.** PR 단계 리뷰는 여전히 필수다. 수정할지 진행할지는 사용자가 정한다.

**Anti-patterns:** stale-revision 리뷰(아래 Cross-Provider Rules 참고); ~3을 넘는 라운드 부풀리기(plan 주인이 수렴 못한 것 — 대신 사용자와 목표를 명확히 하라); 권고를 차단으로 다루기.

## Cross-Provider 규칙

- three-turn 상한은 forcing function이지 단단한 천장이 아니다. Turn 3에서 확실한 돌파가 나오면 끝내고, 아니면 escalate한다.
- 토큰 아끼려고 보안 민감 경로에서 `/review`를 건너뛰지 마라.
- Codex rescue를 호출할 때 ruled-out 가설을 포함해서 Codex가 같은 작업을 다시 하지 않게 하라.
- Codex 발견을 **독립적 증거**로 다뤄라: Claude 결론과의 불일치는 조사하고, Claude 혼자에게 재고하라고 물어 해소하지 마라.
- Codex 위임은 model-effort-delegation.md의 플랫폼 내 모델 티어와 직교한다 — 그 티어는 Claude 측 작업에 여전히 적용된다.
- **매 Codex 라운드마다 stale-revision 검증.** Codex는 같은 파일로 반복 호출되면 이전 호출의 분석을 출력할 때가 있다. 매 round-N 프롬프트에서 Codex가 먼저 현재 revision 식별자(`file head -1`, `git HEAD` short SHA, 또는 고유한 헤더 줄)를 echo하게 하라. 이미 바뀐 파일의 stale 줄 번호를 재현하는 verdict는 신뢰하지 않는다; fresh 세션으로 재시도하라(`codex resume` 아님).
- **프로젝트 CLAUDE.md가 이 기본값을 강화할 수 있다** — 예: PR당 두 리뷰어 규칙. 프로젝트별 강화가 최소치를 덮어쓴다; 최소치는 프로젝트가 침묵하는 곳에 적용된다.
