# Situational Skills Index

어떤 규칙은 특정 작업 맥락에서만 쓰인다 (CSS, PR, Codex, 병렬화, 디버깅 교훈). 상시 떠 있는 rule 세트를 작게 유지하려고, 이런 규칙의 본문은 `ai-roots/skills/<name>/` 아래 skill로 옮겨, harness가 호출할 때 로드한다. 기본적으로는 한 줄짜리 description만 context에 남는다.

이 인덱스가 상주하는 절반이다: 본문은 lazy하게 로드되더라도 *트리거*만은 잊히지 않도록 항상 떠 있다. 어떤 행의 조건이 성립하면, 해당 작업에 손대기 **전에** 그 skill을 호출하라 — 권고가 아니라 구속력 있는 규칙으로 다뤄라. lazy 로딩은 context 최적화일 뿐, 규칙의 우선순위를 낮추지 않는다.

| When this holds | Invoke skill |
|-----------------|--------------|
| CSS나 프레임워크 스타일링(Tailwind, CSS Modules, scoped styles, inline `style`, CSS-in-JS) 편집·작성·리뷰 | `css-discipline` |
| PR 본문이나 제목 작성·수정 (`gh pr create`, `gh pr edit`, `gh api` PR 업데이트) | `github-pr-markdown` |
| 사소하지 않은 작업을 위임하기 전, executor(main vs subagent vs team)·모델(Opus/Sonnet/Haiku)·effort 결정 | `model-effort-delegation` |
| sequential vs subagent vs team, inline vs subagent, foreground vs background 선택 | `parallel-execution-modes` |
| 문제 원인이 여러 계층에 걸쳐 그럴듯한 후보가 여럿이거나, 출력이 여러 독립 판단 기준을 통과해야 할 때 | `parallel-hypothesis-investigation` |
| OpenAI Codex CLI 위임 — rescue 디버깅, cross-provider 리뷰, 최신 문서 리서치, 범위가 정해진 구현 (Codex가 `PATH`에 있을 때) | `codex-delegation` |
| 요청이 그림을 그리거나 이미지를 만들어 달라고 하거나, 아직 없는 `.png`/`.jpg`/`.webp` 자산을 지목할 때 (Codex가 `PATH`에 있을 때) | `codex-imagegen` |
| 여기서 볼 수 없는 대상을 상대로 코드를 쓸 때 — 외부 API, browser, 까다로운 shell 따옴표, 낯선 library, 데이터 pipeline | `incremental-verification` |
| 언어·프레임워크 사이로 코드를 포팅·재작성하거나, 기존 코드가 런타임에 뭘 하는지 답할 때 | `simulate-dont-just-scan` |
| 장시간 작업이 백그라운드로 돌고 사용자가 완료나 진행 상황을 봐야 할 때 — 또는 서브프로세스를 tmux split pane, sentinel 문자열, foreground tail/grep 루프로 감시하고 싶은 충동 | `background-task-monitoring` |
| 웹을 둘러보거나, 페이지 내용을 추출하거나, 데이터를 긁거나, 사이트에서 수치를 가져올 때 — agent-browser가 차단된/빈/동적 내용을 돌려줘서 다른 엔진으로 재시도하거나 형제 URL을 추측하고 싶은 충동이 들 때 포함 | `web-research` |
| memory 항목을 저장하려 하거나, 어떤 사실이 memory에 속하는지 버전 관리되는 표면(rule, `CLAUDE.md`, 프로젝트 문서)에 속하는지 판단할 때 | `memory-minimalism` |
| 요청이 같은 방식으로 처리할 항목을 셋 이상 건넬 때 — 필드, 환경변수, endpoint, 레코드, 파일, 테스트 케이스 — 또는 여러 곳에 걸친 batch 편집. 항목이 균일해 보이는지가 아니라 개수가 트리거다 | `verify-each-instance` |
| 사용자가 반복임을 말하거나 내비칠 때("또", "세 번째인데"), 또는 요청에 빠진 게 있어 되묻거나 짐작해야 했을 때 | `user-growth-coaching` |

다른 provider를 부르려고 있는 행이 둘 있다: `codex-delegation`과 `codex-imagegen`은 일을 Codex CLI로 넘긴다. Codex가 아닌 harness에서만 걸린다 — Codex 안에서는 일이 이미 거기 있으니 직접 하면 된다.

## 규칙

- 트리거가 걸리면, 매칭되는 skill을 호출하는 것은 선택이 아니라 의무다.
- lazy skill도 상주 rule과 같은 권위를 가진다 — 본문이 항상이 아니라 필요할 때 로드될 뿐이다.
- 트리거된 활동 중 하나를 skill을 로드하지 않은 채 하고 있다면, 멈추고 그 skill을 로드하라.