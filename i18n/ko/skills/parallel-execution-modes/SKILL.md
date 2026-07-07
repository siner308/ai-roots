---
name: parallel-execution-modes
description: "작업을 병렬화할 수 있을 때 적용 — sequential, subagent, team 중 선택; inline vs subagent 결정; foreground vs background 실행. 에이전트를 띄우기 전에, 또는 작업이 파일 3개 이상 또는 독립 서브태스크 2개 이상으로 퍼질 때 사용한다."
---

# Parallel Execution Modes

작업을 병렬화할 수 있을 때 전략은 셋으로 갈린다. 워커끼리 통신해야 하는지, 작업이 얼마나 독립적인지를 보고 고른다.

## The Three Modes

| Mode | 언제 쓰나 | 토큰 비용 | 워커 간 통신 |
|------|-----------|-----------|--------------|
| **Sequential** | 작업이 서로 의존하거나, 확인할 게 1~2개뿐일 때 | 최저 | 해당 없음 |
| **Subagents** | 최종 결과만 필요한 독립 작업 | 중간 | 없음 (각자 메인 세션에만 보고) |
| **Teams** | 워커끼리 조율하거나 발견을 두고 논쟁해야 하는 복잡한 작업 | 최고 | teammate 간 직접 메시징 |

## Decision Protocol

1. **애초에 병렬화가 되는 작업인가?** 각 단계가 이전 결과에 의존하면 sequential을 쓴다.
2. **워커끼리 대화해야 하나?** 그렇다면 → teams. 아니면 → subagents.
3. **조율 오버헤드를 정당화할 만큼 복잡한가?** 리서치, 리뷰, 경쟁 가설, 계층을 넘나드는 변경 → teams. 좁은 조회, 테스트 실행, 파일 분석 → subagents.

## Inline vs Subagent Threshold

워커가 하나만 필요할 때조차, 인라인(메인 세션)으로 처리할지 subagent로 위임할지의 선택은 중요하다.

**다음 중 하나라도 해당하면 subagent에 위임한다:**

- 예상 소요 시간 5분 이상 AND 결과를 짧게 요약할 수 있음
- 독립적 — 실행 중간에 사용자 입력이나 메인 context 참조가 필요 없음
- 병렬화 가능한 작업이 2개 이상 → 동시에 띄운다
- 장황한 출력(대량 grep, 긴 로그, 파일 수백 개)이 메인 context를 오염시킬 것
- 백그라운드에 맞는 장시간 작업 — 빌드, 테스트 스위트, 파이프라인

**인라인으로 유지한다:**

- 파일 1~2개의 국소적 편집
- 방금 읽은 파일에 대한 후속 편집 (재탐색 불필요)
- 사용자와 계속 대화해야 하는 상호작용 작업
- 중간 판단이 필요하거나 긴 스트리밍 출력을 내는 작업
- 브리핑 비용이 작업 자체를 넘어설 때

고른 executor 안에서의 모델 선택(Opus/Sonnet/Haiku)은 model-effort-delegation 스킬을 보라.

## Responsiveness Default

두 축이 독립적이며, 순서대로 적용한다:

1. **inline vs subagent** (위 임계치). 이걸 틀리면 비용은 context 중복 / 띄우기 오버헤드다. 짧고 국소적인 작업은 INLINE에 머문다 — foreground subagent도 context를 중복시키므로, 짧은 작업의 해법은 결코 "foreground"가 아니라 "inline"이다.
2. **foreground vs background** — 이미 subagent로 보낸 작업에 대해서만 결정한다. 이걸 틀리면 비용은 메인 세션이 막히는 것이다. `run_in_background: true`를 선호해서 subagent가 도는 동안 메인 세션이 새 사용자 요청을 받을 수 있게 자유롭게 둔다.

### Fan-out as a duration proxy

wall-clock 시간을 미리 추정하는 건 믿을 게 못 된다. 관찰 가능한 fan-out이 더 나은 트리거다. **파일 3개 이상** 또는 **독립 서브태스크 2개 이상**에 걸치는 작업은 장시간 작업 후보다 — 백그라운드(그리고 항목이 독립적이면 동시) subagent를 기본으로 한다.

개수만 보고 판단하지 않게 조심한다(Goodhart): 개수가 아니라 개수 × 항목당 비용이다. 한 줄짜리 편집 3개, 사소한 rename 3개, 답 하나를 위해 읽는 파일 3개 — 모두 인라인에 머문다. 이 proxy는 각 항목이 사소하지 않은 작업을 질 때만 발동한다.

- 백그라운드로 보낸 뒤에는 제어를 돌려받는다: 관련 없는 작업을 이어가거나 사용자를 기다린다.
- 완료 이벤트에 반응하고(background-task-monitoring 스킬의 Rung 1), 필요하면 후속 subagent를 이어 붙인다 — 메인 세션은 조율할 뿐 막히지 않는다.

## Subagents (Agent tool)

Agent 도구로 띄운다. 각 subagent는 자기만의 context window에서 돌고 호출자에게 결과 하나를 돌려준다. 워커끼리는 서로 보이지 않는다.

적합한 경우:

- 독립된 질문을 병렬로 리서치
- 격리된 구현 작업 위임
- 장황한 도구 출력으로부터 메인 context 보호

## Teams (TeamCreate tool)

settings에 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1이 필요하다. teammate들은 task list를 공유하고 서로 직접 메시지를 주고받으며, lead가 끼지 않아도 스스로 조율한다.

적합한 경우:

- 경쟁 가설로 디버깅 (teammate들이 서로의 가설을 적극적으로 반증)
- 계층을 넘나드는 작업: frontend + backend + 테스트를 각각 다른 teammate가 소유
- 서로 다른 렌즈(보안, 성능, 테스트 커버리지)로 동시에 돌리는 코드 리뷰
- 한 레인의 발견이 다른 레인에 영향을 줘야 하는 열린 리서치

현실적 한계:

- teammate 3~5명으로 시작한다. 그 이상이면 조율 오버헤드가 처리량보다 빨리 커진다
- teammate당 task 5~6개를 노린다 — 체크인할 만큼 작고, 자체 완결될 만큼 크게
- teammate마다 자기 context window가 있어 토큰 비용은 team 크기에 선형으로 비례한다
- teammate는 lead의 대화 이력을 물려받지 않는다 — task에 필요한 모든 context를 띄울 때 프롬프트에 담아라

## Rules

- 병렬화는 기본적으로 subagent를 쓴다. 단, 워커끼리 통신하거나 발견을 두고 논쟁해야 하면 예외다.
- 확인할 게 1~2개뿐이라면 기본적으로 sequential을 쓴다 — 병렬화에는 오버헤드가 있다.
- team을 띄울 때는 각 teammate에게 겹치지 않는 분명한 범위를 줘서 파일 충돌과 중복 작업을 막는다.
- team은 실험적이며, in-process teammate의 세션 재개를 지원하지 않는다.
- 명확한 작업 분해의 대체물로 team을 쓰지 마라 — 범위가 잘 잡힌 subagent가 브리핑 부실한 teammate를 이긴다.
