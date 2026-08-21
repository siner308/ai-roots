---
name: hook-lang
description: "[ai-roots] hook 메시지를 전달할 언어를 설정한다. 사용자가 hook·차단 메시지를 자기 언어로 받고 싶다고 하거나 현재 설정을 물을 때 사용 — /hook-lang (상태), /hook-lang ko, /hook-lang en."
allowed-tools: "Bash(~/.claude/skills/hook-lang/scripts/hook-lang.sh *)"
---

# /hook-lang (ai-roots)

hook이 판정을 전달할 언어를 `~/.claude/.ai-roots/lang`으로 설정한다. hook 스크립트 자체는 `CLAUDE.md` 규약대로 영어로 두고, 설정이 `en`이 아니면 각 차단 메시지 끝에 그 언어로 다시 쓰라는 지시가 붙는다.

아래 명령은 skill 확장 중에 이미 실행됐다 — 이 문단 다음 줄이 그 출력이고 그게 결과다. 추가로 명령을 실행하지 말고, 결과를 사용자 언어로 한 문장으로 전달한다.

!`~/.claude/skills/hook-lang/scripts/hook-lang.sh "$ARGUMENTS"`

각 결과의 뜻:

- `hook-lang: en` — hook 메시지가 쓰인 그대로 나가고 전달 지시가 붙지 않는다.
- `hook-lang: ko` — 모든 hook 차단 메시지에 판정을 한국어로 다시 쓰라는 줄이 붙는다.
- `hook-lang: en (default)` — 저장된 설정이 없어 hook이 영어를 쓴다.
- `unsupported language` — 지원 형태를 알린다: `en`과 `ko`, 또는 인자 없이 상태 확인.

## 참고

- 설정은 `~/.claude/.ai-roots/lang`에 있다 — 이 기기 전역이고 세션이 바뀌어도 남으며 커밋되지 않는다.
- 메시지 자체가 아니라 *전달* 지시를 바꾼다. 영어 본문은 그대로 나오고 그 뒤에 다시 쓰라는 지시가 붙는다. 이미 사용자 언어로 쓰인 hook(`push-gate`, `gh-markdown-style`)은 영향받지 않는다.
- 언어를 추가하려면 `hooks/hook_lang.py`의 `RELAY`에 항목 하나, `scripts/hook-lang.sh`에 case 하나를 더한다.
- 모델 없이 하려면 프롬프트에 `! echo ko > ~/.claude/.ai-roots/lang`을 입력하면 같은 변경이 적용된다.
