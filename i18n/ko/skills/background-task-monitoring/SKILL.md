---
name: background-task-monitoring
description: "장시간 작업이 백그라운드에서 돌고 사용자가 완료나 진행 상황을 봐야 할 때 적용 — 완료 알림만(기본), Monitor를 통한 이벤트 스트림, ScheduleWakeup을 통한 인터벌 폴링 중 선택. 서브프로세스를 tmux split pane, sentinel 문자열, foreground tail/grep 루프로 감시하고 싶어질 때도 적용 — 그 패턴은 실패했고 post-mortem이 여기 있다. 결정 사다리, 안티패턴, tee 기반 사용자 가시 스트리밍을 다룬다."
---

# Background Task Monitoring

장시간 작업이 백그라운드에 앉아 있을 때, 사용자가 "다 됐나요?"라고 물어볼 일이 없어야 한다 — 다만 그 가시성을 주는 방식은 **이벤트 기반을 우선, 인터벌 기반은 fallback일 때만** 써야 한다. 이 교훈의 예전 버전은 ScheduleWakeup 폴링을 기본으로 권했는데, 그건 native 완료 신호가 없는 소수의 작업에 과적합된 것이었다.

## The Decision Ladder

작업에 실제로 맞는 것 중 가장 싼 메커니즘을 골라라. 사다리를 내려갈수록 토큰도, 지연도, 의식(ritual)도 늘어난다 — 위 단이 질문에 답하지 못할 때만 비용을 치른다.

### Rung 1 — Completion notification only (default)

사용자가 원하는 게 "결과랑 같이 다 되면 알려줘"뿐이라면, 모니터링을 아예 건너뛴다. `run_in_background: true`인 Bash가 끝나면 하네스가 이미 알려 준다. 작업을 시작하고 다른 일을 이어가다가 완료 이벤트가 뜨면 거기에 반응한다.

```
Bash(command: "...", run_in_background: true)
→ continue with unrelated work
→ completion notification arrives → Read output → report result
```

적용 대상: 단발 빌드, 테스트 스위트, 일회성 마이그레이션, 가치가 과정이 아니라 최종 결과에 있는 모든 작업.

### Rung 2 — Streamed events (when progress matters)

진행 상황을 그때그때 보는 게 사용자에게 도움이 되면 — 단계 완료, 처리된 레코드 수, 떠오르는 에러 — Monitor 도구로 stdout 줄을 구독한다. 각 줄이 알림이 되니 업데이트는 폴링이 아니라 실시간이고, 박자는 작업의 실제 속도에 맞는다.

```
Bash(run_in_background: true, command: "... 2>&1 | tee /tmp/task.log")
Monitor(path: "/tmp/task.log") → each line is an event
→ summarize meaningful phases as they arrive
→ completion event stops the subscription
```

적용 대상: codex `--json` 리뷰(`/review` 스킬 — 이벤트 스트림이 codex가 들여다보는 파일과 reasoning을 실시간으로 보여준다), 단계 경계가 있는 data pipeline, 긴 seed 스크립트, crawler, 실행 도중의 단계 경계가 사용자가 원하는 정보를 담고 있는 모든 작업.

### Rung 3 — Interval polling (fallback only)

1~2분 간격의 ScheduleWakeup(또는 /loop)는 다음이 **모두** 참일 때만 옳은 선택이다:

- 작업에 깔끔한 완료 신호가 없다(외부 시스템, 끝나지 않는 로그 파일, 폴링만 되는 API)
- 진행 상황이 사용자에게 의미가 있지만, 작업이 Monitor가 잡을 수 있는 이산 이벤트를 내보내지 않는다
- 틱마다의 브리핑 비용이 그만한 값을 할 만큼 낮다

ScheduleWakeup을 기본으로 집는다면, 하네스가 공짜로 답해 줬을 질문에 폴링 비용을 치르는 것이다. 점검하라: Rung 1이나 Rung 2가 이걸 커버하지 않나?

적용 대상: 찔러볼 수밖에 없는 외부 비동기 작업(클라우드 빌드, 원격 workflow, 서드파티 큐), 상태를 메인 대화에 끼워 넣어야 하는 subagent 작업, 사용자가 너와 함께 실시간으로 보는 progress dashboard.

## Anti-patterns

- **결과를 폴링하기.** 최종 출력만 원한다면 완료 알림을 믿어라. 다 되면 알려 줄 3분짜리 작업에 ScheduleWakeup을 쓰는 건 순수한 오버헤드다.
- **"단순하게 가려고" 긴 timeout으로 foreground 실행하기.** 그러면 대화가 막혀서 사용자가 끼어들거나 후속 질문을 할 수 없다. foreground는 결과가 다음 단계의 전부인 1분 미만 작업에는 괜찮다. 그 이상이면 Rung 1을 선호하라.
- **구조 없는 Monitor 구독.** stdout 줄을 전부 사용자에게 쏟아내면 raw 로그를 그대로 재현하는 꼴이다. Monitor는 단계 전환을 요약할 때만 값을 한다. 줄을 그대로 echo하면 소용없다.
- **스트림이 나오는 작업을 인터벌 폴링하기.** 작업이 tail할 수 있는 파일에 쓴다면 Rung 2를 써라 — tail을 2분마다 폴링하면 스트림이 이미 주는 저지연 정보를 버리는 셈이다.
- **tmux split pane, sentinel 문자열, foreground tail/grep 루프.** 이 패턴은 실제로 시도됐고 번번이 실패했다 — 아래 교훈을 보라.

## 교훈 — tmux sentinel wrapper는 실패했다

예전 버전의 위임 규칙은 Claude더러 모든 장시간 codex 명령을 tmux split pane 안에서 돌리고 끝에 `=== DONE ===` sentinel을 출력하고 foreground `tail -f "$LOG" | grep -qm1 'DONE'`으로 메인 세션을 깨우라고 했다. 종이 위에서는 그럴듯해 보였다. 실제로는 약속의 두 쪽이 다 깨졌다: pane은 열린 채 남았고(수동으로 닫아야 함), sentinel이 로그에 도착했는데도 Claude는 완료를 끝내 알아채지 못했다 — 사용자가 "끝났어"라고 타이핑해야 턴이 넘어갔다.

깨우기가 실패한 이유: Claude의 메인 턴은 (a) 사용자 입력, 또는 (b) `run_in_background: true` Bash의 완료, 이 두 경우에만 넘어간다. `tail -f | grep`은 foreground로 돌았다 — 그 순간 메인 세션은 막혀 있었고, sentinel이 도착해도 하네스가 "Claude 턴 끝"으로 번역해줄 이벤트가 없었다.

더 깊은 결함: 그 설계는 서로 독립적인 두 목표를 하나의 메커니즘으로 뭉뚱그렸다 — (1) 서브프로세스가 종료되면 Claude를 깨운다, (2) 서브프로세스의 출력을 사용자에게 라이브로 보여준다. 목표 1은 `run_in_background: true` Bash가 native로 해결한다(하네스가 완료 알림을 쏜다). 목표 2는 로그에 tee 하고 사용자가 스스로 `tail -f`를 돌리게 두면 해결된다. 둘 다 tmux + sentinel + grep wrapper로 밀어넣으니, 어느 목표도 더 미덥게 만들지 못한 채 새로운 실패 모드만 추가됐다(tee flush와 sentinel의 경쟁 상태, foreground냐 background냐 모호함, 수동 pane 닫기).

그 post-mortem에서 남은 상비 규칙:

- Claude 쪽에서 tmux split pane을 스크립트로 짜서 서브프로세스 출력을 사용자에게 전달하지 마라. 사용자 본인의 터미널이 이미 tmux를 돌리고 있고, Claude가 그걸 몰아줄 필요가 없다.
- 유일한 소비자가 그걸 기다리는 Claude 쪽 grep뿐인 sentinel 문자열을 쓰지 마라. 백그라운드 Bash의 완료 자체가 결정론적 신호다.
- 두 목표(Claude 깨우기 / 사용자에게 출력 보여주기)가 하나의 메커니즘으로 몰아가고 싶게 만들 때, 둘을 분해하라. 더 단순한 한 쌍이 통합 wrapper를 이긴다.

## User-visible Streaming (Separate Concern)

"출력을 실시간으로 보고 싶다"는 "다 됐는지 물어보게 만들지 마라"와는 다른 요구다. 하네스 쪽 모니터링(위 사다리)은 Claude를 계속 알게 해 주고, 사용자 쪽 스트리밍은 사용자에게 자기만의 뷰를 준다. tee로 스트림을 갈라라:

```
command ... 2>&1 | tee /tmp/task-$$.log
```

그다음 사용자가 자기 터미널에서 그 경로를 `tail -f` 하게 한다. 작동하게 만드는 건 스트림을 가르는 이 컨벤션이다. Claude는 라이브 뷰를 스크립트로 짜지 않는다.

## Why

원래의 안티패턴("사용자가 다 됐는지 계속 물어본다")은 실재하지만, 처방이 잘못 명세됐었다. 바탕 원칙은 **진행 상황을 보는 가치에 비례하는 가시성을 사용자가 가져야 한다**는 것이다. 인터벌 폴링은 가치와 무관하게 고정 비용으로 가시성을 강제한다. 이벤트 기반 메커니즘은 비용을 실제 정보가 도착하는 시점에 맞춘다.

5분짜리 Codex 리뷰는 인터벌 폴링(Rung 3) 대상이 아니다 — `--json`이 이벤트를 스트림하므로 라이브 로그 자체가 진행 상황이고, Rung 2가 그걸 폴링 비용 없이 보여준다. 12단계짜리 45분 seed 파이프라인은 단계 경계 알림에서 많은 걸 얻지만, Monitor가 그걸 폴링 비용 0으로 준다.

## When to Apply

- 한 턴을 넘겨 살아남을 것으로 예상되는 `run_in_background: true` 작업
- Codex 위임(장시간 codex exec, /review) — 보통 Rung 2(`--json` 이벤트 스트림)
- 관찰 가능한 단계가 있는 data pipeline, 마이그레이션, crawler — 보통 Rung 2
- 완료 hook이 없는 외부 비동기 작업 — Rung 3

## Rule Summary

- 기본은 Rung 1(완료 알림만). 폴링은 더 이상 기본이 아니다.
- 단계 수준 진행 상황이 사용자에게 실제 가치가 있을 때 Rung 2로 올린다.
- native 완료나 스트림 신호가 전혀 없을 때만 Rung 3로 간다.
- 사용자 가시 실시간 스트리밍은 모니터링 문제가 아니라 tee 문제다 — 둘을 따로 다룬다.
- tmux/sentinel/foreground-grep wrapper를 다시 짓지 마라. 백그라운드 Bash의 완료 알림이 곧 깨우기 신호다.
