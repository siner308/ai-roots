# Auto-Update Hook

로컬 ai-roots 클론을 최신으로 유지하는 `SessionStart` hook. 업스트림을 pull하고,
바뀐 게 있으면 `install.sh`를 다시 실행한다.

## 존재 이유

설치 스크립트는 `rules/`, `skills/`, `agents/`, `hooks/`를 `~/.claude`로 바로
심링크하므로, 클론이 곧 살아 있는 소스다. 그래서 업데이트는 원리상 간단하다 —
`git pull`만 하면 최신이 된다. 하지만 실제로는 사람들이 잊어버리고, rules가 조용히
낡아간다. 이 hook이 그 고리를 닫는다: 모든 ai-roots 사용자가 신경 쓰지 않아도
업데이트를 받는다.

## 하는 일

세션 시작 시 `hooks/auto-update.sh`를 실행하고, 스크립트는:

1. throttle 스탬프(`~/.claude/.ai-roots/last-update`)를 확인한다. 마지막 실행이
   간격(기본 24시간) 안이면 즉시 종료 — 평범한 세션 시작의 비용은 네트워크 왕복이
   아니라 `stat` 한 번이다.
2. 때가 되면 lock을 잡고, 클론의 현재 브랜치에서 `git pull --ff-only`를 하고,
   `HEAD`가 움직였으면 `install.sh`를 다시 실행해 새 skill/agent를 다시 링크하고
   새 hook을 등록한다.
3. 실제로 업데이트가 적용됐을 때만 stderr에 한 줄 알림을 쓴다.

rule·skill **내용**은 pull이 끝나는 순간 바로 반영된다(파일이 심링크라서). 새
**skill·agent·hook**은 *다음* 세션부터 효과가 난다 — 그 심링크와 `settings.json`
항목은 시작 시점에 읽히기 때문이다.

## 건너뛰는 것 — fail-open 설계

업데이트 실패가 세션을 막거나 깨뜨려선 절대 안 되므로, 모든 에러 경로는 0으로
종료하고 surface 대신 `~/.claude/.ai-roots/update.log`에 기록한다:

- **`git pull --ff-only`** — 로컬 커밋이나 커밋 안 한 변경이 있는 클론은 건드리지
  않는다. repo를 fork했거나 직접 수정했다면, 덮어쓰는 대신 업데이트가 조용히
  멈춘다(업데이트를 기대했다면 로그를 확인하라).
- **git 없음, repo 아님, detached HEAD** — 건너뛴다.
- **throttle / lock** — 간격 안의 실행이나, 이미 업데이트 중인 동시 세션은 아무것도
  안 하고 종료한다. 죽은 실행이 남긴 lock은 1시간 뒤 정리된다.

## 끄는 법

- 환경 변수 `AI_ROOTS_AUTO_UPDATE=0` (또는 `false`/`no`/`off`), 또는
- `~/.claude/.ai-roots/disabled` 파일 생성.

주기는 `AI_ROOTS_UPDATE_INTERVAL`(초, 기본 `86400`)로 조정한다.

## 설치와 등록

`install.sh`가 `hooks/register.py`를 실행해, `hooks/manifest.json`을 읽고 스크립트를
`~/.claude/hooks/`로 심링크하고, 세 개의 `SessionStart` 항목(`startup`, `resume`,
`clear`)을 `~/.claude/settings.json`에 병합한다. lock과 throttle 덕에 중복 트리거는
무해하다 — 간격당 최대 한 번의 pull. 병합은 멱등이고 `settings.json`을 먼저
백업한다.
