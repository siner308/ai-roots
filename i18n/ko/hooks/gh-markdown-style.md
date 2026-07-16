# gh Markdown Style Hook

`Bash` `PreToolUse` hook. [`github-pr-markdown`](../skills/github-pr-markdown) 스킬이 혼자서는 못 막는 두 가지 본문 손상 — 발행 전에 `gh` CLI가 Markdown을 망가뜨리는 것과, aliased 렌더러(bat/glow) 출력으로 만든 본문이 어느 채널로든 깨진 줄바꿈·`•` 불릿으로 나가는 것 — 을 차단한다.

## 왜 있나

처음엔 `gh pr/issue` 명령 앞에 Markdown 규칙을 출력하는 부드러운 알림이었다. 그것만으로는 부족했지만, 게이트로 둬야 하는 진짜 이유는 "모델이 스킬을 잊는다"보다 좁다.

모델이 스킬을 완벽히 따라도 `gh` CLI는 모든 본문 채널에서 Markdown을 망가뜨린다(`- ` → `•`, 백틱 제거, `- [ ]` → `[ ]`). 그 망가짐은 모델이 다 제대로 한 *뒤에* `gh` 내부에서 일어난다. 프롬프트 뒤에서 일어나는 망가짐은 프롬프트로 못 고친다. 게이트만 고칠 수 있다.

그래서 이 hook은 딱 그것 — 채널 — 만 강제하고 나머지는 안 한다. 불릿·체크박스·섹션 형식, 본문 길이, 구조는 스킬의 몫이다. 예전엔 hook이 그것들까지 다시 검증했는데, 그게 hook과 스킬이 어긋난 원인이었다(스킬이 "기본은 짧게, repo 템플릿을 따르라"로 옮겨간 뒤에도 hook은 `## Summary` + `## Test plan`을 hard하게 요구했다). 두 곳에 적힌 규칙은 어긋난다. 이 규칙은 스킬에만 산다.

## 무엇을 하나

매 `Bash` 호출마다 그 명령이 `gh` 본문을 쓰는지 검사한다 — CLI(`gh pr create/edit/comment/review`, `gh issue create/edit/comment`)든 API(`gh api … /pulls|/issues`에 `body=` 필드)든. 두 검사를 적용한다:

- **CLI 본문의 Markdown**은 **차단**한다 — `gh` CLI가 망가뜨리므로 본문을 비운 채로 만들고 GitHub API로 PATCH해야 한다. 일반 텍스트 CLI 본문(망가뜨릴 게 없다)은 통과한다.
- **렌더러 아티팩트**(`•` 불릿, 또는 5칸 이상 후행 공백으로 패딩된 줄)는 **`gh api`를 포함한 모든 채널에서 차단**한다. 이건 본문을 aliased 렌더러(bat/glow가 텍스트를 리플로우하고 `- ` → `•`로 바꾼다)에서 캡처했을 때만 나타나며, 그 손상은 `gh`가 돌기 전에 이미 바이트에 박혀 있어 안전한 API 경로로도 새어나간다. (진짜 Markdown 하드 브레이크는 정확히 후행 공백 두 칸이라, 5칸 이상 임계값은 의도를 오탐하지 않는다.)

차단(exit 2)되면 그 이유가 모델에 피드백되고, 본문을 어떻게 작성·전달할지는 `github-pr-markdown` 스킬을 가리킨다.

## 무엇을 건너뛰나

- **본문 없는 명령** — `gh pr review --approve`, 리뷰어만 바꾸는 edit, 본문이 없는 것: 발동 안 함.
- **일반 텍스트 본문** — Markdown 없는 짧은 `gh pr comment -b "lgtm"`은 통과한다. Markdown을 담은 본문만 차단된다.
- **API 경로의 깨끗한 Markdown** — `gh api` PATCH는 이 hook이 유도하는 *해법*이라, 손으로 쓴 Markdown(불릿, 섹션, 링크)은 거기서 통과한다. 그 경로에선 렌더러 아티팩트만 게이트한다 — 그건 본문을 작성한 게 아니라 렌더러에서 캡처했다는 뜻이기 때문이다.
- **위치를 못 찾거나 검사 불가능한 본문** — 파싱할 수 없는 본문, 또는 stdin(`--body-file -`)·셸 변수·명령 치환(`--body "$(cat f)"`)에서 온 본문은 hook 시점에 펼쳐지지 않아 낯선 명령을 막느니 **fail open**(허용)한다. 강제 대상은 모델이 실제로 쓰는 경로다 — 인라인 `--body "…"` 또는 `--body-file <path>`.

## 알려진 한계 (검토 후 수용)

여기서 상대는 공격자가 아니라 모델/사용자다 — 그래서 일부러 회피하는 형태는 실질적 위험이 없고, 흔한 경로는 커버된다. 이 게이트를 완전한 것으로 다루지 말 것.

- **stdin / 변수 본문은 검사 안 됨**(위 참고) — hook 시점에 읽을 수 없는 것은 fail-closed로 정당한 워크플로를 막느니 fail-open한다.
- **문자열 언급이 과잉 차단할 수 있음** — gh 본문 명령을 실행하지 않고 *이름만* 적은 명령(예: `echo gh pr create -b '- x'`)도 substring으로 매칭돼 차단될 수 있다. 걸리면 다르게 표현하면 된다.

## 설치와 등록

`install.sh`가 `hooks/register.py`를 실행한다. 이 스크립트는 `hooks/manifest.json`을 읽어 스크립트를 `~/.claude/hooks/`로 심링크하고, hook 항목을 `~/.claude/settings.json`에 병합한다. 병합은 멱등이고 `settings.json`을 먼저 백업하므로 재실행해도 안전하다. 수동 편집 불필요.
