---
name: model-effort-delegation
description: "executor(메인 세션 vs subagent vs team), 모델(Opus/Sonnet/Haiku), effort 레벨 중 무엇이 작업에 맞는지 정할 때 적용 — 즉 사소하지 않은 작업을 위임하기 전에. 다운그레이드 엄격 조건(plan 정밀도 + 검증 루프), 에스컬레이션 트리거, blast-radius 오버라이드, subagent 브리핑 기준을 다룬다."
---


  # Model, Effort, and Subagent Delegation

  작업마다 **executor**(메인 세션 vs subagent), **모델**(Fable / Opus / Sonnet / Haiku),
  **effort 레벨**을 의식적으로 고른다. 비싼 모델은 아키텍처 판단에 몰아 쓰고,
  명세가 잘 된 구현은 더 싼 모델에 위임한다.

  ## Principle

  메인 세션은 Opus에 둔다 — 계획, 리뷰, 대화, 국소적 편집을 맡긴다. 크고 독립적인
  작업은 Sonnet/Haiku subagent로 위임한다. **plan이 구체적일수록 약한 모델이 품질을
  더 잘 보존한다** — 그래서 위임의 전제 조건은 정밀한 plan이다. Opus 한 단계 위에는 **Fable 5**가 있다 — 지금 나온 모델 중 가장 강력하지만, 평소 Opus 티어로 안 풀리는 예외적 추론에만 쓴다(아래 Top tier 참고). 일상 작업용이 아니다.

  ## Executor Selection

  executor 토폴로지(메인 세션 / subagent / team)와 inline-vs-subagent 임계치는
  parallel-execution-modes.md를 보라. 이 규칙은 고른 executor 안에서 *어떤 모델*을
  돌릴지라는 직교 선택을 다룬다.

  **executor마다 적용.** 규칙은 세션이 아니라 executor 단위로 적용된다. team에서는
  team lead가 메인 Opus와 같은 역할(계획, 조율, 리뷰)을 하고, 각 teammate는 아래 표로
  작업 유형에 따라 고른다. 다운그레이드 조건과 에스컬레이션 트리거는 teammate마다
  독립적으로 적용된다.

  ## Model Selection

  Task                              │Model │Rationale
  ──────────────────────────────────┼──────┼──────────────────────────────────────
  Architecture design, migration pl…│Opus  │Trade-off judgment, ripple prediction
  PR/code review, root-cause debugg…│Opus  │Hypothesis-falsification, tail cases …
  Plan-driven feature implementation│Sonnet│Clear spec narrows judgment space
  Verifiable refactoring            │Sonnet│Transformation rules are clear, tests…
  Test writing                      │Sonnet│Repetitive patterns, framework conven…
  Bulk exploration, grep summaries  │Haiku…│Path + summary is enough
  Format conversion, comment adds, …│Haiku │Mechanical work
  Log inspection, status checks     │Haiku │Read-only, no judgment

  ### Top tier — Fable 5 (가장 까다로운 작업)

  **Fable 5**(`claude-fable-5`; Agent 도구 selector `model: "fable"`)는 Anthropic이 널리 출시한 모델 중 가장 강력하다 — Opus 4.8 한 단계 위로, 가장 까다로운 추론과 긴 호흡의 agentic 작업용이다. adaptive thinking 상시 on, 1M 토큰 context.

  평소 Opus 티어로 정말 부족할 때만 꺼낸다:

  - **예외적으로 어려운 추론** — spec이 모호한 게 아니라 추론 자체에서 Opus가 막힌 아키텍처나 근본 원인 디버깅.
  - **긴 호흡의 agentic 작업** — 아주 큰 context를 일관되게 유지해야 하고 blast radius가 최상위 모델을 정당화하는 경우.

  **기본값이 아니다.** Fable 5는 Opus 4.8의 약 2배 비용($10 / $50 vs $5 / $25 per MTok, 입력 / 출력)이라, 일상 아키텍처 작업의 천장은 Opus로 두고 Fable 5는 예외적 경우에 의식적으로 에스컬레이션한다.

  ### Downgrade Conditions — STRICT

  Sonnet/Haiku로 다운그레이드하려면 둘 다 참이어야 한다:

  1. plan이 file path, 함수 시그니처, 검증 방법을 명시한다
  2. **검증 루프가 존재한다** — 테스트, type checker, lint, 또는 비슷한 것

  둘 중 하나라도 없으면 Opus를 유지한다. 검증 루프 없이 다운그레이드하면 조용한 품질
  저하가 생긴다(evaluation-integrity 참고).

  ## Effort Selection

  모델 선택과 직교한다. thinking budget을 작업 위험도에 맞춘다.

  Effort     │When to use
  ───────────┼────────────────────────────────────────────────────────────────────
  **high**   │Hard-to-reverse operations (DDL, production config, force-push), ar…
  **medium** │Standard feature implementation, review, multi-layer refactoring
  **low / of…│Single-file edits, mechanical transforms, tasks where verification …

  **blast radius가 effort를 덮어쓴다.** 작아 보이지만 되돌리기 어려운 작업은 high +
  Opus에 머문다.

  ## Escalation Triggers

  subagent 실행 중 다음 신호가 하나라도 나타나면 **Opus로 에스컬레이션**한다:

  • 같은 실수가 3번 이상 반복됨
  • plan에 없는 **설계 판단**이 필요한 상황
  • spec 모호함이 아니라 **코드 이해 부족**에 뿌리를 둔 실패
  • 검증 루프가 원인 불명으로 계속 실패함

  에스컬레이션은 실패가 아니라 규칙의 일부다. 약한 모델을 고집스럽게 밀어붙이면
  hysteresis로 이어진다 — 틀린 방향이 그대로 굳어 버린다. 사다리에는 Opus 위 한 칸이 있다: Opus 자체가 (spec 모호함이 아니라) 정말 어려운 추론에서 막히면 **Fable 5**로 에스컬레이션한다 — 비용 때문에 그 예외적 경우에만.

  ## Cross-Provider Delegation (Codex)

  Codex CLI가 PATH에 있으면 모드 선택, 3-턴 rescue protocol, 보안 민감 리뷰
  트리거(/review), capability routing, 실행 메커니즘, plan-stage review는
  codex-delegation 스킬을 보라. Codex 위임은 위의 모델 티어 선택과
  직교한다 — Claude 쪽 작업에는 플랫폼 내 모델 티어가 여전히 적용된다.

  ## Subagent Briefing Standard

  약한 executor에 위임할 때 브리핑에는 반드시 다음이 들어가야 한다:

  • **file path**와 편집 범위 (명시적 시작점)
  • **함수 시그니처** 또는 의사 코드
  • 따라야 할 **기존 코드 패턴** (참조 파일 + 패턴)
  • **검증 방법** — 어떤 테스트나 명령으로 성공을 판정하는지
  • **엣지 케이스**와 명시적으로 범위 밖인 항목
  • subagent에게 **판단의 근거**를 보고하도록 요청 (나중에 추적할 수 있게)

  브리핑이 빈약해질 것 같으면 실제로는 인라인 Opus가 더 싸다.

  ## Examples

  ### Threshold-based delegation

    Request: "Add avatar upload to the user profile page"
    1. Main Opus: explore existing upload patterns inline (~2 min)
    2. Main Opus: write plan — file paths, API endpoint, component structure,
  verification
    3. Sonnet subagent: implement (independent, ~15 min)
    4. Main Opus: review the result

  ### Inline handling

    Request: "Add a nil check to the function you just looked at"
    → Main Opus edits inline. Briefing cost exceeds the work.

  ### Parallel delegation

    Request: "Add the same endpoint pattern to 5 microservices"
    → Spawn 5 Sonnet subagents in parallel. Main does plan + review only.

  ### Over-delegation (bad)

    Request: "Fix a typo in README"
    Wrong: Haiku subagent — spawn overhead is 10× the work
    Right: Inline edit

  ### Under-delegation (bad)

    Request: "Audit the whole codebase for deprecated API usage"
    Wrong: Main Opus runs repeated greps — main context gets polluted
    Right: Delegate to Haiku Explore agent

  ## Rule Summary

  • 메인 세션은 Opus에 머문다 — 계획, 리뷰, 대화, 국소적 편집에 집중
  • **Fable 5**는 Opus 위 천장 — Opus로 안 풀리는 예외적 추론이나 긴 호흡의 agentic 작업에만 쓴다; Opus의 약 2배 비용이라 기본값이 아니다
  • subagent에 위임하는 조건: 5분 이상 + 독립적 + 검증 가능
  • plan 정밀도와 검증 루프가 둘 다 있을 때만 다운그레이드
  • blast radius가 클 때는 절대 모델이나 effort를 다운그레이드하지 않는다
  • 실패가 3번 쌓이거나 설계 판단이 떠오르면 Opus로 에스컬레이션; Opus 자체가 정말 어려운 추론에서 막힐 때만 Opus → Fable 5
  • 브리핑에는 file path, 시그니처, 검증, 그리고 판단 근거 보고 요청이 들어가야 한다
  • Codex CLI가 있으면 cross-provider 규칙(3-턴 상한, /review를 통한 어드버서리얼
  리뷰, capability routing, plan-stage review)은 codex-delegation 스킬을 보라.
  • **프로젝트 CLAUDE.md가 이 기본값을 더 강하게 만들 수 있다** — 예를 들어 PR당
  리뷰어 2명 규칙. 프로젝트 규칙은 더 엄격한 쪽에서 최소 기준을 덮어쓴다. 프로젝트가
  말이 없는 곳에는 최소 기준이 적용된다.
