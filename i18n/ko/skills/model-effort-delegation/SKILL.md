---
name: model-effort-delegation
description: "executor(메인 세션 vs subagent vs team), 모델(Opus/Sonnet/Haiku), effort 레벨 중 무엇이 작업에 맞는지 정할 때 적용 — 즉 사소하지 않은 작업을 위임하거나 멀티 에이전트 workflow/fan-out을 시작하기 전에. 다운그레이드 엄격 조건(plan 정밀도 + 검증 루프), fan-out의 스테이지별 모델 고정, 에스컬레이션 트리거, blast-radius 오버라이드, subagent 브리핑 기준을 다룬다."
---

# Model, Effort, and Subagent Delegation

작업마다 **executor**(메인 세션 vs subagent), **모델**(Opus / Sonnet / Haiku), **effort 레벨**을 의식적으로 고른다. 비싼 모델은 아키텍처 판단에 몰아 쓰고, 명세가 잘 된 구현은 더 싼 모델에 위임한다.

## Principle

메인 세션은 Opus에 둔다 — 계획, 리뷰, 대화, 국소적 편집을 맡긴다. 크고 독립적인 작업은 Sonnet/Haiku subagent로 위임한다. **plan이 구체적일수록 약한 모델이 품질을 더 잘 보존한다** — 그래서 위임의 전제 조건은 정밀한 plan이다.

## Executor Selection

executor 토폴로지(메인 세션 / subagent / team)와 inline-vs-subagent 임계치는 parallel-execution-modes 스킬을 보라. 이 규칙은 고른 executor 안에서 *어떤 모델*을 돌릴지라는 직교 선택을 다룬다.

**executor마다 적용.** 규칙은 세션이 아니라 executor 단위로 적용된다. team에서는 team lead가 메인 Opus와 같은 역할(계획, 조율, 리뷰)을 하고, 각 teammate는 아래 표로 작업 유형에 따라 고른다. 다운그레이드 조건과 에스컬레이션 트리거는 teammate마다 독립적으로 적용된다.

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Architecture design, migration planning, tech selection | Opus | Trade-off judgment, ripple prediction |
| PR/code review, root-cause debugging | Opus | Hypothesis-falsification, tail cases matter |
| Plan-driven feature implementation | Sonnet | Clear spec narrows judgment space |
| Verifiable refactoring | Sonnet | Transformation rules are clear, tests catch drift |
| Test writing | Sonnet | Repetitive patterns, framework conventions |
| Bulk exploration, grep summaries | Haiku (Explore agent) | Path + summary is enough |
| Format conversion, comment adds, simple substitution | Haiku | Mechanical work |
| Log inspection, status checks | Haiku | Read-only, no judgment |

### Above Opus — 상위 티어가 열려 있을 때

Anthropic이 이따금 Opus 위 티어를 열어 준다(한정 릴리스, 리서치 프리뷰). 그럴 때도 기본값은 아니다 — 일상 아키텍처 작업의 천장은 Opus로 두고, 예외적 경우에만 의식적으로 에스컬레이션한다. "어려워 보인다", "Opus가 막힌 것 같다"는 자기 평가는 트리거가 아니다. 관찰 가능한 신호가 있을 때만:

- **수렴 실패** — 검증 루프가 있는데도 Opus가 같은 문제에서 가설이나 수정 시도를 3회 연속 실패함.
- **분석 상충** — 같은 질문에 Opus가 2회 이상 서로 모순되는 결론을 내놓음.
- **해소 안 된 되돌리기 어려운 결정** — 스키마 마이그레이션, 공개 API 계약 같은 one-way door인데 Opus가 분석을 한 바퀴 다 돌고도 트레이드오프를 해소하지 못함.
- **긴 호흡 실행에서 일관성 상실** — 한 자율 실행 안에서 Opus가 자기가 앞서 한 작업을 2회 이상 다시 도출하거나 뒤집음.

상위 티어가 없을 때 같은 신호가 뜨면 그 뜻은: 갈아 넣기를 멈추고 전략을 바꿔라 — 다르게 분해하거나, cross-provider 평가자를 들이거나(codex-delegation 참고), 해소 안 된 트레이드오프를 사용자에게 올려라.

### Downgrade Conditions — STRICT

Sonnet/Haiku로 다운그레이드하려면 둘 다 참이어야 한다:

1. plan이 file path, 함수 시그니처, 검증 방법을 명시한다
2. **검증 루프가 존재한다** — 테스트, type checker, lint, 또는 비슷한 것

둘 중 하나라도 없으면 Opus를 유지한다. 검증 루프 없이 다운그레이드하면 조용한 품질 저하가 생긴다(evaluation-integrity 참고).

### Fan-out은 모델을 명시적으로 고정한다

Workflow 스크립트와 멀티 에이전트 fan-out은 기본적으로 세션 모델을 상속하고, fan-out은 그 모델의 비용을 에이전트 수만큼 곱한다. 최상위 세션(Opus 이상)을 상속한 30-agent 실행은 최상위 토큰을 30배로 쓴다 — 누구도 의도한 적 없는 결과다. 실제로 일어났다: Mythos급 세션에서 띄운 32-agent 개념 토너먼트를 실행 도중에 죽여야 했다.

- 3개 이상 에이전트의 workflow나 fan-out을 띄우기 전에, 스크립트나 spawn opts에서 스테이지별로 모델을 명시적으로 지정한다. worker에 대해서는 세션 모델 상속에 절대 기대지 않는다.
- 다운그레이드 조건은 스테이지 단위로 적용된다: 정밀한 rubric(체크리스트 스킬, 고정된 출력 스키마)이 plan 정밀도를 대신하고, 구조적 중복(독립 투표 N개, adversarial verify, 다수결)이 검증 루프를 대신한다. 대량의 심사/스캔 스테이지는 대개 Sonnet 자격이 되고, 창의적 생성과 항목 간 종합은 대개 안 된다 — 그런 스테이지는 Opus에 둔다.
- Opus 위 세션 티어는 오케스트레이터의 판단(계획, 브리핑, 결과 읽기)을 위한 것이지, fan-out worker를 위한 것이 결코 아니다.

예시(32-agent 개념 토너먼트): scout = Sonnet (조사 대상이 명세됨, 출처 확인 가능), ideation = Opus (창의적, 검증 루프 없음), 심사 27명 = Sonnet (각자 좁은 렌즈 하나 + gate 체크리스트 + 3표 중복), synthesis = Opus (항목 간 트레이드오프).

## Effort Selection

모델 선택과 직교한다. thinking budget을 작업 위험도에 맞춘다.

| Effort | When to use |
|--------|-------------|
| **high** | Hard-to-reverse operations (DDL, production config, force-push), architecture decisions, debugging with unclear root cause |
| **medium** | Standard feature implementation, review, multi-layer refactoring |
| **low / off** | Single-file edits, mechanical transforms, tasks where verification catches errors immediately |

**blast radius가 effort를 덮어쓴다.** 작아 보이지만 되돌리기 어려운 작업은 high + Opus에 머문다.

## Escalation Triggers

subagent 실행 중 다음 신호가 하나라도 나타나면 **Opus로 에스컬레이션**한다:

- 같은 실수가 3번 이상 반복됨
- plan에 없는 **설계 판단**이 필요한 상황
- spec 모호함이 아니라 **코드 이해 부족**에 뿌리를 둔 실패
- 검증 루프가 원인 불명으로 계속 실패함

에스컬레이션은 실패가 아니라 규칙의 일부다. 약한 모델을 고집스럽게 밀어붙이면 hysteresis로 이어진다 — 틀린 방향이 그대로 굳어 버린다. Opus 위 칸은 상위 티어가 마침 열려 있을 때만 존재한다(Above Opus 참고) — 그때도 거기 적은 관찰 가능한 신호로만 올라가고, "문제가 어렵게 느껴진다"는 결코 트리거가 아니다.

## Cross-Provider Delegation (Codex)

Codex CLI가 PATH에 있으면 모드 선택, 3-턴 rescue protocol, 보안 민감 리뷰 트리거(/review), capability routing, 실행 메커니즘, plan-stage review는 codex-delegation 스킬을 보라. Codex 위임은 위의 플랫폼 내 모델 티어와 직교한다 — 그 모델 티어는 Claude 쪽 작업에 여전히 적용된다.

## Subagent Briefing Standard

약한 executor에 위임할 때 브리핑에는 반드시 다음이 들어가야 한다:

- **file path**와 편집 범위 (명시적 시작점)
- **함수 시그니처** 또는 의사 코드
- 따라야 할 **기존 코드 패턴** (참조 파일 + 패턴)
- **검증 방법** — 어떤 테스트나 명령으로 성공을 판정하는지
- **엣지 케이스**와 명시적으로 범위 밖인 항목
- subagent에게 **판단의 근거**를 보고하도록 요청 (나중에 추적할 수 있게)

브리핑이 빈약해질 것 같으면 실제로는 인라인 Opus가 더 싸다.

## Examples

### Threshold-based delegation

```
Request: "Add avatar upload to the user profile page"
1. Main Opus: explore existing upload patterns inline (~2 min)
2. Main Opus: write plan — file paths, API endpoint, component structure, verification
3. Sonnet subagent: implement (independent, ~15 min)
4. Main Opus: review the result
```

### Inline handling

```
Request: "Add a nil check to the function you just looked at"
→ Main Opus edits inline. Briefing cost exceeds the work.
```

### Parallel delegation

```
Request: "Add the same endpoint pattern to 5 microservices"
→ Spawn 5 Sonnet subagents in parallel. Main does plan + review only.
```

### Over-delegation (bad)

```
Request: "Fix a typo in README"
Wrong: Haiku subagent — spawn overhead is 10× the work
Right: Inline edit
```

### Under-delegation (bad)

```
Request: "Audit the whole codebase for deprecated API usage"
Wrong: Main Opus runs repeated greps — main context gets polluted
Right: Delegate to Haiku Explore agent
```

## Rule Summary

- 메인 세션은 Opus에 머문다 — 계획, 리뷰, 대화, 국소적 편집에 집중
- Opus 위 티어는 열려 있을 때만, 에스컬레이션 전용 — 관찰 가능한 신호(시도 3회 연속 실패, 결론 상충, 해소 안 된 one-way door 결정, 일관성 상실)에서만, 결코 기본값이 아니다
- subagent에 위임하는 조건: 5분 이상 + 독립적 + 검증 가능
- plan 정밀도와 검증 루프가 둘 다 있을 때만 다운그레이드
- blast radius가 클 때는 절대 모델이나 effort를 다운그레이드하지 않는다
- Fan-out은 세션 모델을 절대 상속하지 않는다 — 3개 이상 에이전트 workflow를 띄우기 전에 스테이지별로 모델을 고정한다. 스테이지 수준 rubric과 투표 중복이 다운그레이드 조건을 충족할 수 있다
- 실패가 3번 쌓이거나 설계 판단이 떠오르면 Opus로 에스컬레이션
- 브리핑에는 file path, 시그니처, 검증, 그리고 판단 근거 보고 요청이 들어가야 한다
- Codex CLI가 있으면 cross-provider 규칙(3-턴 상한, /review를 통한 어드버서리얼 리뷰, capability routing, plan-stage review)은 codex-delegation 스킬을 보라.
- **프로젝트 CLAUDE.md가 이 기본값을 더 강하게 만들 수 있다** — 예를 들어 PR당 리뷰어 2명 규칙. 프로젝트 규칙은 더 엄격한 쪽에서 최소 기준을 덮어쓴다. 프로젝트가 말이 없는 곳에는 최소 기준이 적용된다.
