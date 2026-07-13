# Push Gate Hook

`git push` 전에 사람의 push별 결정을 강제하고, force push는 아예 거부하는 `Bash` 대상 `PreToolUse` hook.

## 왜 존재하나

push는 git 워크플로우에서 바깥을 향하는 순간이다: 커밋이 동료에게(공개 리포라면 모두에게) 보이기 시작하고, 리뷰되고, 당겨지고, 그 위에 작업이 쌓인다. 한 번의 push 승인이 다음 커밋에까지 연장되지는 않는다 — 그러나 긴 세션 안에서는 앞선 "푸시하세요" 지시가 상시 허가처럼 읽히고, 넓은 Bash 허용목록이나 관대한 세션 모드는 다음 push를 조용히 실행해버린다. 이 hook을 만들게 한 사건이 정확히 그것이었다: 방금 작성된 작업물이 앞선 push 지시의 관성으로, 사용자가 검증하기 전에 공개 리포에 push되었다.

프롬프트 규칙으로는 이걸 신뢰성 있게 막을 수 없다 — 앞선 지시를 상시 허가로 오독하는 모델과 규칙을 적용할 모델이 같은 모델이기 때문이다. 그래서 이 hook은 `permissionDecision: "ask"`를 반환해, 명령이 자동 승인될 상황에서도 사람에게 권한 프롬프트를 띄운다. "공개 전 검증"이 모델의 판단이 아니라 하네스의 속성이 된다.

## 무엇을 하나

- **`git push` (모든 원격, 모든 형태 — compound 명령, `git -C dir push` 포함)** → `ask`: 이 특정 push를 사용자가 확인한다. 명시적 지시와 push 전 검증이 있었는지 상기시키는 사유가 함께 표시된다.
- **`git push --force` / `--force-with-lease` / `-f`** → `deny`: force push는 이미 리뷰된 히스토리를 다시 쓴다. 커밋을 쌓아 올리는 것이 요구되는 대안이다.
- **`git push --dry-run` / `-n`** → 통과: 아무것도 공개되지 않는다.
- **push가 아닌 명령** (`git status`, `echo push`, `git log | grep push`) → 건드리지 않는다. push 패턴은 파이프나 `;`/`&&` 경계를 넘어 다른 명령까지 매칭되지 않는다.

## 리포별 opt-out

어떤 리포는 autopilot처럼 굴러가서 push마다 뜨는 프롬프트가 목적을 해치고, 어떤 리포는 신중한 설계 작업이라 그 프롬프트가 곧 목적이다. 그래서 게이트는 git config로 리포마다 토글할 수 있다. 설정은 `.git/config`에 저장되므로 클론에 로컬이고, 커밋되지 않으며, 세션이 바뀌어도 유지된다:

```sh
git config ai-roots.push-gate off    # 이 리포: push가 ask 없이 지나간다
git config --unset ai-roots.push-gate    # 게이트 복원 (`on`으로 설정해도 됨)
```

Claude Code 세션 안에서는 `push-gate` skill이 이를 감싼다: `/push-gate`는 토글, `/push-gate on|off|status`는 명시적 설정/조회.

게이트가 꺼져 있으면 hook은 push를 강제 allow하는 대신 결정 없이 통과시킨다. 따라서 Claude Code의 일반 권한 흐름은 그대로 살아 있다: 관대한 세션 모드에서는 조용히 push되고, default 모드에서는 표준 Bash 프롬프트가 여전히 뜬다. force push `deny`는 토글과 무관하게 유지된다 — 리뷰된 히스토리 보호는 리포별 취향의 문제가 아니다.

토글은 세션의 작업 디렉토리에서 읽는다. 따라서 *다른* 리포를 향한 `git -C dir push`는 대상 리포가 아니라 세션 리포의 설정으로 판정된다.

## 알려진 한계 (검토 후 수용)

주 대상은 모델/사용자이지 공격자가 아니다. 스크립트, alias, `sh -c` 문자열 안에 감싼 push는 감지되지 않는다 — 강제되는 경로는 모델이 실제로 push하는 방식(직접적인 `git push` Bash 호출)이다. `gh pr merge`, `git remote` 조작 등 다른 외부 지향 작업은 범위 밖이며, 각각 이만큼 명확한 근거가 생길 때 별도로 다룬다.
