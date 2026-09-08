# Char Discipline Hook

두 event에 걸려서 키보드가 치지 않는 문자를 잡아내는 hook이다. `Edit|Write|MultiEdit`의 `PostToolUse`에서는 edit이 추가한 텍스트를, `Stop`에서는 그 턴의 마지막 메시지를 본다.
[`prose-style`](../rules/prose-style.md) 규칙의 문자 절을 담당한다. 기계 표식으로 읽히는 보이는 글리프와, 산문에서 아무 의미가 없는 보이지 않는 codepoint 둘 다다.

## 왜 있나

`prose-style`이 요구하는 것 중 정적 검사가 정확히 잡아내는 건 문자 규칙뿐이다. codepoint는 있거나 없을 뿐이라 heuristic도 언어 의존도 없다.
동시에 상주 규칙이 가장 못 지키는 항목이다. em dash를 내보내는 건 모델이 따로 결정하는 일이 아니라 문장과 함께 딸려 나오기 때문이다.
문장을 판단하지 못하는 독자도 em dash와 가운뎃점은 알아보고, 그 한 문자로 글 전체를 기계 출력으로 치워버린다.
보이지 않는 문자는 독자조차 없다. code와 commit message, 검색 index로 복사돼 살아남아서 화면에 아무 단서도 없이 그곳을 깨뜨린다.

문자 표는 `char_tables.py`에 있고, PR과 이슈 본문에 같은 집합을 거는 [`gh-markdown-style`](gh-markdown-style)과 공유한다. 표면 셋에 표 하나라서 서로 어긋날 수 없다.

## 무엇을 잡나

보이는 글리프와 대신 쓸 ASCII 형태:

| 문자 | 대신 쓸 것 |
|------|-----------|
| em dash, en dash, horizontal bar | 마침표, 쉼표, 콜론, 또는 괄호 |
| 가운뎃점 | 쉼표, 또는 `와`/`과` |
| 굽은 큰·작은 인용부호 | ASCII `"`와 `'` |
| 줄임표 글리프 | 마침표 세 개 |
| 좌·우·이중 화살표 | `->`, `<-`, `=>`, 또는 관계를 말로 |
| bullet, white bullet, triangular bullet, small black square | ASCII `-` |

보이지 않는 codepoint는 모두 평범한 공백이나 아무것도 없음으로 바꾼다: no-break과 narrow no-break 공백, `U+2000`부터 `U+200A`, medium mathematical과 ideographic 공백, braille blank, zero-width space와 non-joiner, joiner, word joiner, byte-order mark, soft hyphen, 방향 표시와 override, 보이지 않는 연산자 네 개.

## 범위: code까지 포함해 모든 파일

`comment-discipline`은 code 주석에, `prose-discipline`은 Markdown에 걸리고, 서로의 파일을 피해서 한 번의 edit이 두 block을 부르지 않는다.
문자는 그렇게 나뉘지 않는다. string literal 안의 굽은 인용부호나 식별자 안의 zero-width space는 스타일 문제가 아니라 버그다.
그래서 이 hook은 edit이 건드린 파일이 무엇이든 돌고, 한 edit이 이 hook과 매체별 hook을 함께 부를 수 있다. 서로 다른 관심사이고, 양쪽 판정 다 필요하다.

## 두 event

파일 수정은 문자가 사용자에게 닿는 자리가 아니다. 채팅 답변이 그 자리라서, `Stop` 쪽이 이 규칙이 애초에 겨냥한 경우를 잡는다. 파일을 거치지 않고 답변에 곧바로 써진 산문이다.
transcript에서 그 턴의 마지막 assistant 텍스트를 읽어 한 번 block하고, 해당 문장을 다시 쓴 뒤 답을 다시 말하라고 요구한다.
`stop_hook_active`가 턴당 한 번으로 제한하고, transcript를 못 읽으면 빈 것으로 취급하니, 예외로 남겨야 하는 문자 하나가 세션을 붙잡아둘 수는 없다.

## block 메시지

문자마다 개수와 ASCII 대체형을 나열하고, 보이는 문자에는 예시 줄을 붙인 뒤, 발생마다 판정을 요구한다. 기본값은 교체다.
정당하게 남기는 경우는 정적으로 판별할 수 없으니 메시지에 이름만 적어두고 모델이 판단한다: 그 문자를 일부러 다루는 규칙·문서·fixture, 그대로 옮긴 인용 원문이나 상위 데이터, 식별자나 파일명, 언어가 요구하는 부호(`。`, `、`, `「」`, `¿`), 수식·단위·통화 기호, `❌`/`✅` 비교 라벨.
해당하는 예외를 밝히면 계속 진행할 수 있다.

## 건너뛰는 것

- `file_path`가 없는 tool 호출(쓴 게 없다).
- edit이 추가한 텍스트 밖의 모든 것. 파일 다른 곳의 기존 문자는 누가 그 줄을 건드릴 때까지 조용하다.
- fenced code block. 양쪽 표면 다 건너뛴다. 인용한 명령과 diff, 파일 내용이 byte 그대로 남아야 하는 자리다.
- 같은 턴의 두 번째 `Stop` 라운드.

## 끄는 법

`AI_ROOTS_CHAR_CHECK=0`.
