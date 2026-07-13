---
name: push-gate
description: "[ai-roots] 현재 리포지토리의 push별 확인 게이트를 토글한다. 사용자가 push 게이트를 켜거나 끄자고 할 때, 프롬프트 없이 push되게(autopilot) 해달라고 할 때, 게이트 상태를 물을 때 사용 — /push-gate (토글), /push-gate on, /push-gate off, /push-gate status."
allowed-tools: "Bash(case *), Bash(git config *)"
---

# /push-gate (ai-roots)

`push-gate` PreToolUse hook을 **현재 리포지토리**에 대해 제어한다. 리포 로컬 git config의 `ai-roots.push-gate`를 통해서이며, hook이 이를 실시간으로 읽으므로 변경은 바로 다음 push부터 적용된다.

아래 토글은 skill 확장 시점에 이미 실행되었다 — 이 문단 다음 줄이 그 출력이고, 그것이 결과다. 추가 명령을 실행하지 말고, 결과를 사용자의 언어로 한 문장으로 보고한다.

!`case "$ARGUMENTS" in off) git config ai-roots.push-gate off && echo "push-gate: off";; on) git config --unset ai-roots.push-gate; echo "push-gate: on";; "") if [ "$(git config --get ai-roots.push-gate)" = "off" ]; then git config --unset ai-roots.push-gate; echo "push-gate: on (toggled)"; else git config ai-roots.push-gate off && echo "push-gate: off (toggled)"; fi;; status) echo "push-gate: $(git config --get ai-roots.push-gate || echo on)";; *) echo "unknown subcommand: $ARGUMENTS (expected on|off|status)";; esac`

각 결과의 의미:

- `push-gate: off` — 이 리포의 push가 push별 ask를 건너뛴다: 관대한 세션 모드에서는 조용히 push되고, default 모드에서는 표준 Bash 프롬프트가 여전히 뜬다. force push는 토글과 무관하게 계속 거부된다.
- `push-gate: on` — 게이트 활성: 모든 push가 확인을 요구한다.
- "not in a git repository"류의 에러 — git 리포 안에서만 동작한다고 말한다.
- `unknown subcommand` — 기대하는 형태를 안내한다: 인자 없이는 토글, `on`/`off`는 명시적 설정, `status`는 변경 없이 조회.

## 참고

- 설정은 `.git/config`에 저장된다 — 이 클론에 로컬이고, 커밋되지 않으며, 세션이 바뀌어도 유지된다.
- 게이트를 끄는 것은 바깥을 향한 완화다: 명시적 커맨드가 아니라 지나가는 말로 요청받았을 때는, 이 리포의 push가 더 이상 개별 확인되지 않는다는 점을 한 줄로 다시 말해준다.
- 모델을 전혀 안 타는 대안: 프롬프트에 `! git config ai-roots.push-gate off`를 직접 입력하면 모델 턴 없이 같은 토글이 실행된다.
