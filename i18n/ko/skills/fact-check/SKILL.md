---
name: fact-check
description: "[ai-roots] grounded-assertions Stop hook audit를 조절하거나 끄고 켠다. claim audit를 켜거나 끄거나, 문장 gate를 바꾸거나, 활성 여부를 확인해달라는 요청에 사용 — /fact-check (상태), /fact-check on, /fact-check off, /fact-check <숫자> (gate 설정)."
allowed-tools: "Bash(case *)"
---

# /fact-check (ai-roots)

`~/.claude/.ai-roots/fact-check` 파일로 `grounded-assertions` Stop hook을 제어한다. Hook이 턴이 끝날 때마다 이 파일을 읽으므로 변경은 모든 세션에서 바로 다음 턴부터 적용된다.

아래 명령은 skill 확장 시점에 이미 실행됐다 — 이 문단 다음 줄이 그 출력이고, 그게 결과다. 추가 명령을 실행하지 말고 결과를 사용자의 언어로 한 문장으로 보고하라.

!`case "$ARGUMENTS" in off) mkdir -p "$HOME/.claude/.ai-roots" && echo off > "$HOME/.claude/.ai-roots/fact-check" && echo "fact-check: off";; on) rm -f "$HOME/.claude/.ai-roots/fact-check"; echo "fact-check: on (gate 8, default)";; "") if [ -f "$HOME/.claude/.ai-roots/fact-check" ]; then v=$(cat "$HOME/.claude/.ai-roots/fact-check"); if [ "$v" = "off" ]; then echo "fact-check: off"; else echo "fact-check: on (gate $v)"; fi; else echo "fact-check: on (gate 8, default)"; fi;; *[!0-9]*) echo "unknown subcommand: $ARGUMENTS (expected on|off|<number>)";; *) mkdir -p "$HOME/.claude/.ai-roots" && echo "$ARGUMENTS" > "$HOME/.claude/.ai-roots/fact-check" && echo "fact-check: on (gate $ARGUMENTS)";; esac`

각 결과의 의미:

- `fact-check: off` — 다시 켤 때까지 모든 곳에서 Stop hook audit이 꺼진다.
- `fact-check: on (gate N)` — 마지막 메시지가 N문장 이상인 턴에 audit이 발동한다. N이 작을수록 자주, 클수록 드물게 걸린다.
- `fact-check: on (gate 8, default)` — 저장된 override 없음. Hook 내장 기본값을 쓴다.
- `unknown subcommand` — 사용법을 안내하라: 인자 없으면 상태 확인, `on`/`off`로 끄고 켜기, 숫자로 gate 설정.

## 참고

- 설정은 `~/.claude/.ai-roots/fact-check`에 산다 — 이 기기 전역(hook 자체가 전역 등록이라), 세션을 넘어 유지, commit되지 않음.
- 기본 gate(8)는 `hooks/grounded-assertions.py`의 `SENTENCE_GATE`에 정의돼 있고, `on`은 override를 지울 뿐이라 둘이 어긋날 일이 없다.
- Model 없이 하는 방법: 프롬프트에 `! echo 12 > ~/.claude/.ai-roots/fact-check`를 치면 model 턴 없이 같은 변경이 적용된다.
