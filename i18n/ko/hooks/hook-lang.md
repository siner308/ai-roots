# hook_lang

등록된 hook이 아니라 공용 helper다. `hooks/hook_lang.py`가 `~/.claude/.ai-roots/lang`을 읽고, 설정이 `en`이 아니면 차단 메시지 끝에 전달 지시를 덧붙인다.

## 왜 필요한가

hook 차단 메시지는 사용자 세션 화면에 뜨기 때문에, 한국어로 대화하던 사용자가 중간에 영어를 읽게 된다. 게다가 모델이 다음 문장을 쓰기 직전에 영어 지시가 들어오면 그 답변까지 영어로 끌려간다. 한국어 세션에서 Stop hook 감사가 발동하면 바로 보이는 현상이다.

hook마다 모든 문자열을 번역하면 텍스트가 갈라져 서로 어긋나고, `CLAUDE.md`는 `hooks/`를 영어 원본으로 둔다. 그래서 메시지는 영어로 두고, 판정을 사용자 언어로 다시 쓰라는 한 줄만 붙인다.

## 사용법

```python
from hook_lang import localize

print(json.dumps({"decision": "block", "reason": localize(msg)}))
```

상태 파일이 없거나 비었거나 모르는 언어면 `localize`는 원문을 그대로 돌려준다. 설정이 잘못돼도 편집이 막히는 일은 없다.

## 연결 구조

`hook_lang.py`는 `manifest.json`이 아니라 `hooks/register.py`의 `SUPPORT_MODULES`에 들어간다. 자신을 import하는 hook 옆에 symlink돼야 하고, 고아 링크 정리가 이 파일을 지우면 안 되기 때문이다. 다른 support 모듈을 추가할 때도 그 목록에 넣는다.

현재 `comment-discipline.py`, `prose-discipline.py`, `grounded-assertions.py`가 쓴다. `push-gate.py`와 `gh-markdown-style.py`는 메시지가 이미 한국어라 그대로 둔다.

## 언어 추가

`hooks/hook_lang.py`의 `RELAY`에 항목 하나, `skills/hook-lang/SKILL.md`(와 한국어 미러)에 case 하나를 더한다.
