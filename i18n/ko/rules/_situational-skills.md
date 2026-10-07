# Situational Skills Index

맥락에 따라 적용되는 규칙은 `ai-roots/skills/<name>/` 아래 skill로 있고 필요할 때 로드된다. 이 index는 그 트리거를 담아 상주시킨다.

## 규칙

- 요청받은 작업에서 어느 행의 조건이 성립하면 손대기 전에 그 skill을 invoke한다. skill 없이 그 작업을 하고 있는 자신을 발견하면 멈추고 로드한다. 로드된 skill은 상주 규칙과 똑같이 구속한다.
- skill은 요청받은 작업을 어떻게 할지를 바꿀 뿐 얼마나 할지는 바꾸지 않는다. 행은 요청과 대조하고 스스로 덧붙인 단계와는 대조하지 않아서, skill 하나가 다음 skill로 이어지지 않게 한다. ❌ 400자 설명에 출처를 달려고 `web-research`를 로드하거나, env var 표 뒤의 라이브러리 내부를 확인하려고 로드한다 ✅ 이미 눈앞에 있는 코드와 맥락으로 답한다.
- 사용자의 명시적 지시가 skill보다 우선한다. 충돌하면 사용자를 따르고 제쳐둔 skill 문장을 밝힌다.
- skill 때문에 멈추거나 확인을 요청하거나 요청받은 작업을 미완으로 두거나 방향을 바꾸게 되면, skill 파일 이름을 대고 해당 문장을 그대로 인용하고 그것이 요구하는 것과 네가 해석한 것을 나눠 말한다.
- `codex-delegation`은 작업을 Codex CLI에 넘기므로 Codex가 아닌 harness에서만 발동한다. Codex 안에서는 직접 작업한다. `codex-imagegen`은 Codex가 번들한 이미지 CLI를 부르므로 Codex가 설치된 harness라면 어디서든 적용된다.

## 트리거

| 이 조건이 성립하면 | invoke할 skill |
|---|---|
| CSS나 프레임워크 스타일링(Tailwind, CSS Modules, scoped styles, inline `style`, CSS-in-JS)을 쓰거나 고치거나 리뷰할 때 | `css-discipline` |
| PR 본문이나 제목을 쓰거나 고칠 때(`gh pr create`, `gh pr edit`, `gh api` PR 수정) | `github-pr-markdown` |
| 간단하지 않은 작업을 위임하기 전에 실행자(메인 vs subagent vs team), 모델(Opus/Sonnet/Haiku), effort를 정할 때 | `model-effort-delegation` |
| 순차 vs subagent vs team, inline vs subagent, foreground vs background를 고를 때 | `parallel-execution-modes` |
| 문제의 그럴듯한 원인이 여러 계층에 걸쳐 있거나, 출력이 독립적인 판단 기준 여러 개를 통과해야 할 때 | `parallel-hypothesis-investigation` |
| OpenAI Codex CLI에 위임할 때: 막힌 뒤의 rescue 디버깅, 교차 provider 리뷰, 최신 문서 조사, 범위가 정해진 구현 (Codex가 `PATH`에 있을 때) | `codex-delegation` |
| 이미지를 그리거나 만들어 달라는 요청, 또는 없는 `.png`/`.jpg`/`.webp` 자산을 만들라는 요청 (Codex가 설치돼 있을 때) | `codex-imagegen` |
| 여기서 볼 수 없는 것을 상대로 코드를 쓸 때: 외부 API, 브라우저, 까다로운 shell 인용, 낯선 라이브러리, 데이터 파이프라인 | `incremental-verification` |
| 언어나 프레임워크 사이로 코드를 옮기거나 다시 쓸 때, 또는 기존 코드가 런타임에 무엇을 하는지 답할 때 | `simulate-dont-just-scan` |
| 오래 걸리는 작업이 background에서 돌고 사용자가 완료나 진행 상황을 봐야 할 때, 또는 tmux 분할 창이나 sentinel 문자열, foreground tail/grep 루프로 subprocess를 지켜보고 싶어질 때 | `background-task-monitoring` |
| 웹을 훑거나 페이지 내용을 뽑거나 데이터를 긁거나 사이트에서 수치를 가져올 때, agent-browser가 차단이나 빈 응답, 동적 내용을 돌려줘서 다른 engine으로 재시도하거나 형제 URL을 추측하고 싶어질 때도 포함 | `web-research` |
| memory 항목을 저장하려 할 때, 또는 어떤 사실이 memory에 속하는지 버전 관리되는 표면(규칙, `CLAUDE.md`, 프로젝트 문서)에 속하는지 따질 때 | `memory-minimalism` |
| README, 참조 문서, 런북, 설정이나 env var 문서, 변경 이력, 마이그레이션 안내를 쓰거나 고칠 때, 또는 기존 기술 문서를 교정할 때 | `technical-doc-precision` |
| 같은 방식으로 처리할 항목 셋 이상을 받았을 때(필드, env var, endpoint, 레코드, 파일, 테스트 케이스), 또는 여러 자리에 걸친 일괄 수정. 항목이 얼마나 균일해 보이는지가 아니라 개수가 트리거다 | `verify-each-instance` |
| 사용자가 이게 반복이라고 말하거나 암시할 때("또", "세 번째인데"), 또는 요청에서 빠진 걸 네가 묻거나 추측해야 했을 때 | `user-growth-coaching` |
