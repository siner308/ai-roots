---
name: codex-tmux-monitoring
description: "장시간 도는 서브프로세스(특히 Codex)를 tmux split pane, sentinel 문자열, 또는 foreground tail/grep 루프로 감시하려는 충동이 들 때 적용하세요. 그 패턴이 왜 못 미더웠는지, 그리고 run_in_background Bash + 하네스 완료 알림을 쓰고 사용자에게 라이브로 보여줄 땐 로그에 tee 하라는 걸 설명합니다."
---


  # Codex tmux split-pane 감시는 못 미더웠다

  예전 버전의 model-effort-delegation은 Claude더러 모든 /codex:* 명령을 tmux split
  pane 안에서 === CODEX DONE === sentinel과 함께 돌리고, foreground
  tail -f "$LOG" | grep -qm1 'CODEX DONE'로 메인 세션을 깨우라고 했습니다.
  종이 위에서는 그럴듯해 보였습니다.
  하지만 실제로는 번번이 실패했습니다.

  ## 실제로 무슨 일이 있었나

  전형적인 cc tmux 하네스 아래에서 /codex:diff-review를 돌렸더니 이런 상태가 됐습니다:

  • Codex가 끝나고 자기 pane에 === CODEX DONE ===을 출력했다.
  • 나중에 grep해보니 로그 파일에 sentinel 문자열이 있었다.
  • tmux split pane은 열린 채 남아 있었다(read -p는 없었지만, 깔끔하게 종료하라는
  지시도 없었다).
  • Claude는 완료를 끝내 알아채지 못했다. 사용자가 "끝났어"라고 타이핑해야 턴이
  넘어갔다.

  그래서 약속의 두 쪽이 다 깨졌습니다: 사용자는 자동으로 닫히는 pane을 얻지 못했고
  (수동으로 닫아야 함), Claude는 sentinel이 도착했는데도 결정론적인 깨우기를
  받지 못했습니다.

  ## 깨우기가 실패한 이유

  Claude의 메인 턴은 (a) 사용자 입력, 또는 (b) run_in_background: true Bash의 완료
  이 두 경우에만 넘어갑니다. 규칙의 코드 블록은 tail -f | grep -qm1을
  run_in_background: true로 표시하지 않았습니다. 다른 곳의 산문 한 줄이 "이걸
  백그라운드로 돌려라"라고 했지만, 실제로 실행된 건 그 예시뿐이었고 그건 foreground로
  돌았습니다 — 그 순간 메인 세션은 막혀 있었고, 하네스는 기다리고 있었으며, sentinel이
  도착해도 하네스가 "Claude 턴 끝"으로 번역해줄 이벤트가 없었습니다.

  foreground/background를 고쳤다 해도, 그 설계는 서로 독립적인 두 목표를 하나의
  메커니즘으로 뭉뚱그렸습니다:

  1. codex가 종료되면 Claude를 깨운다.
  2. codex의 추론 과정을 사용자에게 라이브로 보여준다.

  목표 1은 run_in_background: true Bash가 native로 해결합니다 — 서브프로세스가
  종료되면 하네스가 완료 알림을 쏩니다. 목표 2는 로그 경로에 tee 하고 사용자가
  스스로 tail -f를 돌리게 두면 해결됩니다. 둘 다 tmux + sentinel + grep wrapper로
  밀어넣으니, 어느 목표도 더 미덥게 만들지 못한 채 새로운 실패 모드만
  추가됐습니다(tee flush와 sentinel의 경쟁 상태, foreground냐 background냐 모호함,
  수동 pane 닫기).

  ## 지금 쓰는 방식

  • run_in_background: true Bash에 2>&1 | tee /tmp/codex-*.log. 완료 알림이 Claude를
  깨운다. sentinel 없음.
  • 사용자가 라이브 추론을 보고 싶어 하면 Claude가 로그 경로를 알려준다. 사용자가
  자기 터미널에서 tail -f를 돌린다. Claude는 라이브 뷰를 스크립트로 짜지 않는다.
  • read -p 'press enter to close'와 split pane은 완전히 사라졌다. read -p를
  없애달라던 예전 사용자 피드백(프로젝트별 memory에 기록돼 있던)은 이제 더 넓은
  패턴 제거에 흡수됐다.

  ## 이 교훈이 적용되는 신호

  • 완료 시 Claude의 턴이 재개돼야 하는, 장시간 도는 서브프로세스.
  • 그 서브프로세스를 Claude 스스로 지켜보는 깨우기 sentinel로 감싸려는 충동.
  • 완료를 감지하려고 Claude에게 foreground tail, grep, 폴링 루프를 돌리게 하는
  패턴.

  세 경우 모두: run_in_background: true Bash를 쓰고 하네스의 완료 알림을
  믿으세요(lessons/background-task-monitoring.md의 Rung 1). 두 번째 감시 채널을
  발명하지 마세요.

  ## 규칙

  • Claude 쪽에서 tmux split pane을 스크립트로 짜서 서브프로세스 출력을 사용자에게
  전달하지 마세요. 사용자 본인의 터미널이 이미 tmux를 돌리고 있고, Claude가 그걸
  몰아줄 필요가 없습니다.
  • 유일한 소비자가 그걸 기다리는 Claude 쪽 grep뿐인 sentinel 문자열을 쓰지 마세요.
  백그라운드 Bash의 완료 자체가 결정론적 신호입니다.
  • 두 목표(Claude 깨우기 / 사용자에게 출력 보여주기)가 하나의 메커니즘으로
  몰아가고 싶게 만들 때, 둘을 분해하세요. 더 단순한 한 쌍이 거의 항상 통합 wrapper를
  이깁니다.
