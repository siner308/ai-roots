# Grounded Assertions Hook

턴이 끝나려는 시점에 실행되는 `Stop` hook.
마지막 응답이 사실 주장을 담을 만큼 길면 한 번 block하고 claim 단위 audit을 요구한다. 모든 material claim은 이번 세션에서 확보한 근거를 가리키거나, 지금 도구로 검증되거나, uncertainty marker를 되찾아야 한다.

## 왜 존재하나

`grounded-assertions` rule이 이미 같은 내용을 말하지만, 이 rule이 겨냥하는 실패 — reasoning의 "아마 X"가 출력에서 "X"로 굳는 것 — 는 작성 시점에 일어나고, 상주 rule은 전체 context와 경쟁하다 밀린다.
Stop hook은 응답이 존재한 뒤에 실행되는 유일한 층이다.

설계는 self-correction 연구가 실제로 지지하는 방향을 따른다.
막연한 "확실해요?" 재질문은 맞는 답까지 뒤집고([FlipFlop 실험](https://arxiv.org/abs/2311.08596)), 외부 근거 없는 intrinsic self-correction은 답을 오히려 망가뜨리는 경향이 있다([Huang et al., ICLR'24](https://arxiv.org/abs/2310.01798)).
효과가 확인된 쪽은 출력을 claim 단위로 쪼개 모델 자신의 확신보다 단단한 것과 대조하는 방식이고([Chain-of-Verification](https://arxiv.org/abs/2309.11495)), self-correction은 신뢰할 수 있는 외부 feedback이 있을 때 성공한다([Kamoi et al., TACL 2024](https://arxiv.org/abs/2406.01297)).
여기서는 세션 transcript와 도구 출력이 그 외부 feedback이다. audit이 요구하는 건 의심이 아니라 claim과 근거의 대조다.

## 무엇을 하나

`Stop`에서 transcript로 그 턴의 마지막 assistant 메시지를 읽고, 문장 수 gate(`SENTENCE_GATE`, 기본 8, `/fact-check <숫자>`로 조절)를 넘으면 한 번 block하며 모든 material claim을 세 갈래로 나누는 audit 지시를 내린다.

1. **근거 있음** (읽은 파일, 명령 출력, 사용자 발언) — 쓴 그대로 둔다. 근거 있는 claim에 hedge를 덧붙이는 것을 명시적으로 금지하는데, 이게 FlipFlop 방어다.
2. **지금 검증 가능** — 턴이 끝나기 전에 도구로 확인하고 결과에 맞게 고친다.
3. **둘 다 아님** — uncertainty marker를 복원한다("~로 보입니다", "확인 필요").

`stop_hook_active`가 audit을 턴당 한 번으로 제한하고, 지시문이 "나머지는 다시 쓰지 마라"로 끝나서 audit 라운드가 응답을 통째로 재생성하는 것도 막는다.

## 무엇을 건너뛰나

- 마지막 메시지가 문장 gate 아래인 턴 — 짧은 대화 응답은 발동시키지 않는다.
- Fence 안 code block — gate 계산에 넣지 않는다.
- Sidechain(subagent) transcript entry.
- `/fact-check off`를 실행했거나(상태는 `~/.claude/.ai-roots/fact-check`, 매 턴 새로 읽음) `AI_ROOTS_FACT_CHECK=0`이 설정된 경우 전부 — 아무 설정 없이도 hook은 켜져 있고 조절은 gate가 한다.
- 읽거나 parse할 수 없는 transcript — hook은 fail open이라 세션을 가두는 일이 없다.

## 알려진 한계 (검토 후 수용)

Gate는 분량 heuristic이지 claim 탐지기가 아니다. 사실 주장이 하나도 없는 긴 응답도 audit을 받고(이때 비용은 "고칠 것 없음" 한 줄 라운드), 확신에 찬 추측으로 가득한 짧은 응답은 gate 아래로 빠져나간다.
Audit 라운드 자체는 재검사되지 않아서 audit 중 새로 생긴 claim은 놓친다. 1회 loop가 의도된 상한이다.
같은 context 안의 audit이라 생성자가 자신을 검토하는 구조인데, claim-근거 대조 구조가 그 편향을 좁히긴 해도 없애지는 못한다(더 무거운 교차 검토는 `/review`의 몫).
