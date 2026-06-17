# gh Markdown Style Hook

`gh`와 GitHub API 쓰기에 GitHub-flavored Markdown을 강제하는 `Bash` `PreToolUse` hook. [`github-pr-markdown`](../skills/github-pr-markdown) 스킬을 모델이 기억하기를 기대하는 대신 도구 경계에서 강제한다.

## 왜 있나

처음엔 부드러운 알림이었다(`gh pr/issue` 명령 앞에 마크다운 규칙을 출력했다). 그래도 두 가지가 계속 빠져나갔다.

1. 모델이 스킬을 부르지 않고 PR 본문을 작성했다 — 프롬프트 수준 규칙은 잊어버릴 수 있다.
2. 형식이 맞아도 `gh` CLI와 셸 heredoc이 발행 *전에* 마크다운을 조용히 망가뜨렸다(`- ` → `•`, 백틱 제거, `- [ ]` → `[ ]`). 그래서 렌더링된 페이지가 깨져 보이기 전까지는 알 수 없었다.

신뢰성 문제는 더 좋은 프롬프트가 아니라 결정론적 강제가 필요하다. 이제 이 hook은 hard gate다. 실행 직전 명령을 검사해서, 본문이 망가지는 경로로 전달되거나 본문 내용이 이미 깨져 있으면 차단한다.

## 무엇을 하나

매 `Bash` 호출마다 그 명령이 `gh` 본문을 쓰는지(`gh pr create/edit/comment/review`, `gh issue create/edit/comment`), 또는 PR/이슈용 GitHub API를 치는지(`/repos/OWNER/REPO/{pulls,issues}/N`로 가는 `curl`/`gh api`) 검사한다. 해당하면:

- **채널 규칙** — *마크다운을 담은* `gh` 본문은 **차단**된다. `gh`는 모든 본문 채널에서 마크다운을 망가뜨리고, 그 망가짐은 어떤 내용 검사보다 뒤에 `gh` 내부에서 일어난다. 그래서 유일한 해법은 채널 자체를 금지하는 것이다 — 본문을 비운 채로 만들고 API로 PATCH한다. 일반 텍스트 본문(망가질 게 없다)은 통과한다.
- **내용 규칙** — API 경로에서는 본문을 추출해서(curl `-d @file`/인라인 JSON, 또는 `gh api -f body=`) **검증**한다. 유니코드 불릿 금지, 체크박스에 `- ` 접두사, PR 리소스 본문(`/pulls/N`)에는 `## Summary` + `## Test plan`.

차단(exit 2)되면 그 이유가 모델에 피드백되고, 모델은 Write 도구로 본문을 다시 작성해서(이 셸에서는 heredoc이 마크다운을 망가뜨린다) API로 PATCH한다.

## 무엇을 건너뛰나

- **본문 없는 명령** — `gh pr review --approve`, 리뷰어만 바꾸는 edit, 본문이 없는 것: 발동 안 함.
- **일반 텍스트 본문** — 마크다운 없는 짧은 `gh pr comment -b "lgtm"`은 통과한다. 마크다운을 담은 본문만 API 경로로 밀린다.
- **위치를 못 찾는 본문** — 본문 payload를 파싱할 수 없으면 낯선 명령 형태를 막아 세우는 대신 **fail open**(허용)한다. 명확히 문제로 식별된 경우에만 차단한다.
- **검사 불가능한 본문 소스** — stdin 본문(`--body-file -`, `gh api --input -`, `curl --data @-`), 셸 변수, 명령 치환(`--body "$(cat f)"`)은 hook 시점에 펼쳐지지 않아 통과한다. 강제 대상은 모델이 실제로 쓰는 경로다 — 인라인 `--body "…"`, `--body-file <path>`, `curl -d @file`.

## 알려진 한계 (검토 후 수용)

adversarial 리뷰에서 드러났고 의식적으로 강제하지 않기로 한 것들. 여기서 상대는 공격자가 아니라 모델/사용자다 — 그래서 일부러 회피하는 형태는 실질적 위험이 없고, 흔한 경로는 커버된다. 이 게이트를 완전한 것으로 다루지 말 것.

- **stdin 본문은 검증 안 됨**(위 참고) — 검사할 수 없는 것은 fail-closed로 정당한 stdin 워크플로를 막느니 fail-open한다.
- **문자열 언급이 과잉 차단할 수 있음** — gh 본문 명령을 실행하지 않고 *이름만* 적은 명령(예: `echo gh pr create -b '- x'`)도 substring으로 매칭돼 차단될 수 있다. 걸리면 다르게 표현하면 된다.
- **URL 값을 가진 비-엔드포인트 플래그** — `curl -e <url>`처럼 플래그에 넘긴 URL이 엔드포인트로 잘못 해석돼 PR 섹션 검사를 틀어지게 할 수 있다. GitHub 쓰기에 쓰는 형태는 아니다.
- **`gh api graphql`** 본문 변경은 범위 밖(명령에 `/pulls|issues/N`이 없다).

## 설치와 등록

`install.sh`가 `hooks/register.py`를 실행한다. 이 스크립트는 `hooks/manifest.json`을 읽어 스크립트를 `~/.claude/hooks/`로 심링크하고, hook 항목을 `~/.claude/settings.json`에 병합한다. 병합은 멱등이고 `settings.json`을 먼저 백업하므로 재실행해도 안전하다. 수동 편집 불필요.
