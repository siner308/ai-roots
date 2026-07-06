---
name: github-pr-markdown
description: "pull request 본문이나 제목을 만들거나 수정할 때(gh pr create, gh pr edit, gh api PR 업데이트), 또는 PR 설명을 작성할 때 — 다른 스킬이나 워크플로가 PR 설명을 만들어내는 경우도 포함 — 적용한다. 본문은 최대 3줄 — 기본값이 아니라 하드 캡이며, 유일한 예외는 레포의 PR 템플릿이다. GitHub-flavored Markdown을 강제한다: ASCII 대시 불릿, task-list 체크박스, 백틱 코드 참조, 그리고 gh CLI 마크다운 손상을 피하는 안전한 API-PATCH 본문 전달."
---

# GitHub PR Markdown Convention

CRITICAL: PR을 만들거나 수정할 때(gh pr create, gh pr edit, PR 본문 작성), 유효한 GitHub-flavored Markdown을 만들어야 한다. 깨진 마크다운(망가진 체크박스, 벗겨진 백틱, 맨 URL)은 제출을 막는 결함이다 — 제출 전에 고친다.

## 규칙

### 구조

- PR 제목은 70자 미만. 자세한 건 본문에
- 섹션은 `##` 사용 (PR 제목이 H1이므로 본문에서 `#`은 절대 쓰지 않음)
- 섹션 사이에는 빈 줄 하나

### 포맷 — STRICT

- 불릿: 항상 `- ` (ASCII 대시 + 공백) 사용. •, ·, * 같은 유니코드 불릿은 절대 쓰지 않음
- Task list: 항상 `- [ ]` / `- [x]` (대시 + 공백 + 대괄호) 사용. `- ` 접두사 없는 맨 `[ ]`는 체크박스로 렌더되지 않음
- 코드 참조: 항상 백틱으로 감쌈 (`componentName`, `fileName.ts`). 백틱이 셸 이스케이프를 견뎌야 함 — 최종 출력에서 확인
- Markdown으로 충분하면 raw HTML 쓰지 않음
- 표는 GFM table 문법(파이프 + 정렬) 사용

### 링크와 References — STRICT

- 이슈/PR 참조는 `owner/repo#123` 또는 `#123`
- URL: 항상 `[text](url)` 형식. 맨 URL 금지
- 이미지는 `![alt text](url)`, alt text는 설명적으로

### 본문 길이 — 하드 캡

PR 본문은 최대 **3줄**이다. 기본값이 아니라 상한이다 — diff가 크다고 본문이 길어지지 않는다. 길게 생성된 본문은 기계가 쓴 글로 읽혀 리뷰어가 건너뛰고, 무엇을 왜 바꿨는지 담은 3줄은 읽힌다.

- `## Summary`, `## Test plan`, `## References`, TL;DR 같은 형식적 섹션은 넣지 않는다. 깊은 맥락은 커밋 메시지나 리뷰 코멘트에 담는다.
- 한 줄은 문장, `- ` 불릿, 검증된 `[text](url)` 링크 중 무엇이든 될 수 있다 — 단, 합쳐서 3줄. 추측 URL은 넣지 않는다. 링크는 직접 열어 인용하려는 내용이 실제로 있는지 확인한 뒤에만 넣는다.
- 문제나 동기를 먼저, 변경 내용을 나중에. 문제를 알기 전에 해결부터 꺼내지 않는다.

**유일한 예외 — 레포의 PR 템플릿**(`.github/pull_request_template.md` 또는 `.github/PULL_REQUEST_TEMPLATE/`): 템플릿 구조가 우선하되, 캡이 그 안으로 들어간다 — 채우는 섹션마다 최대 3줄. 해당 없는 섹션은 "N/A" 채우기 대신 빼버리고, 템플릿에 없는 섹션은 추가하지 않는다. 포맷 규칙(ASCII 불릿, 백틱 코드 참조, API 전달)은 그 안에서도 그대로 적용된다.

### 본문 전달 — STRICT

gh CLI는 모든 본문 전달 방식에서 마크다운을 손상시킨다(`--body`, `--body-file`, `gh pr edit --body-file`): 대시가 •로, 백틱이 벗겨지고, `- [ ]`가 `[ ]`로 바뀐다. **PR 본문을 절대 gh CLI로 넘기지 않는다. 항상 GitHub API를 직접 쓴다.**

안전한 방법 — 빈 본문으로 PR을 만들고 API로 PATCH:

```bash
# 1. Create PR with empty body
gh pr create --title "the pr title" --body "" --draft

# 2. Write body payload with Python (preserves exact bytes)
python3 -c "
import json
body = '''Show codex token usage on API-key auth, where \x60rate_limits\x60 is null so the quota line stayed blank.

- [ ] Statusline renders token counts in apikey mode
'''
with open('/tmp/pr-payload.json', 'w', encoding='utf-8') as f:
    json.dump({'body': body}, f, ensure_ascii=False)
"

# 3. PATCH via GitHub API
curl -s -X PATCH \
  -H "Authorization: token $(gh auth token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @/tmp/pr-payload.json \
  https://api.github.com/repos/OWNER/REPO/pulls/NUMBER
```

수정할 때는 업데이트된 본문으로 2-3단계를 다시 쓴다.

Notes:

- Python 문자열에서는 셸 해석을 피하려고 백틱 대신 `\x60`을 쓴다
- **비-ASCII 문자를 바이트 이스케이프로 인코딩하지 않는다** (예: `\xec\x97\x90`). 유니코드 텍스트를 그대로 쓴다

### 제출 전 검증

PR을 만들거나 수정한 뒤, API로 raw 본문을 확인한다:

```bash
gh pr view NUMBER --json body --jq .body | head -10
```

확인 항목:

1. `- ` 불릿이 ASCII 대시인지 (•가 아닌지)
2. `- [ ]` 체크박스에 `- ` 접두사가 있는지
3. 코드 참조 둘레에 백틱 `` ` ``가 있는지

하나라도 실패하면, payload를 다시 쓰고 위처럼 API로 PATCH 한다.
