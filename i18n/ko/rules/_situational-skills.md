# Situational Skills Index

어떤 규칙은 특정 작업 맥락에서만 쓰인다 (CSS, PR, Codex, 병렬화, 디버깅 교훈). 상시 떠 있는 rule 세트를 작게 유지하려고, 이런 규칙의 본문은 `ai-roots/skills/<name>/` 아래 skill로 옮겨 Skill 도구로 필요할 때 로드한다. 기본적으로는 한 줄짜리 description만 context에 남는다.

이 인덱스가 상주하는 절반이다: 본문은 lazy하게 로드되더라도 *트리거*만은 잊히지 않도록 항상 떠 있다. 어떤 행의 조건이 성립하면, 해당 작업에 손대기 **전에** 그 skill을 호출하라 — 권고가 아니라 구속력 있는 규칙으로 다뤄라. lazy 로딩은 context 최적화일 뿐, 규칙의 우선순위를 낮추지 않는다.

| When this holds | Invoke skill |
|-----------------|--------------|
| CSS나 프레임워크 스타일링(Tailwind, CSS Modules, scoped styles, inline `style`, CSS-in-JS) 편집·작성·리뷰 | `css-discipline` |
| PR 본문이나 제목 작성·수정 (`gh pr create`, `gh pr edit`, `gh api` PR 업데이트) | `github-pr-markdown` |
| 사소하지 않은 작업을 위임하기 전, executor(main vs subagent vs team)·모델(Opus/Sonnet/Haiku)·effort 결정 | `model-effort-delegation` |
| sequential vs subagent vs team, inline vs subagent, foreground vs background 선택 | `parallel-execution-modes` |
| 문제 원인이 여러 계층에 걸쳐 그럴듯한 후보가 여럿이거나, 출력이 여러 독립 판단 기준을 통과해야 할 때 | `parallel-hypothesis-investigation` |
| OpenAI Codex CLI 위임 — rescue 디버깅, cross-provider 리뷰, 최신 문서 리서치, 범위가 정해진 구현 (Codex가 `PATH`에 있을 때) | `codex-delegation` |
| 작업 결과가 불확실 — 외부 API, 브라우저 자동화, 셸 escaping, 낯선 라이브러리, 데이터 파이프라인 | `incremental-verification` |
| 읽었지만 실행해 보지 않은 코드를 포팅·디버깅·구현 | `simulate-dont-just-scan` |
| 장시간 도는 서브프로세스를 tmux split pane, sentinel 문자열, foreground tail/grep 루프로 감시하고 싶은 충동 | `codex-tmux-monitoring` |
| 장시간 작업이 백그라운드로 돌고 사용자가 완료나 진행 상황을 봐야 할 때 | `background-task-monitoring` |

## Rules

- 트리거가 걸리면, 매칭되는 skill을 호출하는 것은 선택이 아니라 의무다.
- lazy skill도 상주 rule과 같은 권위를 가진다 — 본문이 항상이 아니라 필요할 때 로드될 뿐이다.
- 트리거된 활동 중 하나를 skill을 로드하지 않은 채 하고 있다면, 멈추고 그 skill을 로드하라.