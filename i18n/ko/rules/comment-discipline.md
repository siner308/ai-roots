# Comment Discipline

기본은 주석을 쓰지 않는 것이다. 이름을 잘 지은 식별자, 명확한 제어 흐름, 작은 함수만으로도 코드가 WHAT(무엇을 하는지)은 이미 다 말해준다. 주석은 코드가 표현하지 못하는 단 하나, 비자명한 WHY(왜 그게 맞는지)를 위한 것이다.

이건 어디서나 적용된다 — 메인 세션 편집, subagent가 만든 코드, 리팩터링, 버그 수정 전부. 구현을 subagent에 위임할 때는 이 규칙을 브리핑에 넣어라. 약한 모델은 제약을 다시 말해주지 않으면 방어적으로 주석을 다는 습관으로 돌아간다.

## When a comment earns its place

주석은 그걸 지웠을 때 나중에 읽는 사람이 헷갈릴 경우에 쓸 가치가 있다. 구체적으로:

- **Hidden constraint**: 여기서는 안 보이지만 다른 곳에서 강제되는 불변 조건 (예: "caller holds the lock")
- **Workaround for a specific bug**: 링크나 이슈 참조를 붙여서, 업스트림 수정이 들어오면 이 주석을 떼어낼 수 있게
- **Surprising behavior**: 틀린 것처럼 보이지만 비자명한 이유로 맞는 코드
- **Subtle invariant**: 순서, idempotency, 수치 정밀도 가정처럼 읽는 사람이 무심코 깨뜨릴 수 있는 것

쓰기 전 자가 점검: "이 주석을 지우면 신중한 독자가 헷갈리거나 놀랄까?" 아니라면 — 쓰지 마라.

## Forbidden comment patterns

이런 건 신호 없이 잡음만 더하므로 절대 쓰지 마라:

- **WHAT restatements**: `// increment counter`, `// loop through users`, `// return the result`
- **Signature echoes in docstrings**: 이미 시그니처에 있는 파라미터 이름, 타입, 반환값을 다시 적는 것
- **Task-context references**: `// added for the X flow`, `// used by Y`, `// fixes issue #123`, `// as requested in review`, `// Claude suggested this`, `// per chat`. 이런 건 PR 설명과 git 로그에 들어갈 내용이지 소스에 들어갈 게 아니다.
- **Scratchpad notes**: `// 일단 이렇게`, `// for now`, `// 임시로`, `// 확실하지 않음`, `// revisit later`. 작업 중인 생각은 나중에 읽는 사람이 알 바 아니다.
- **Removal traces**: `// removed old logic`, `// no longer needed`, `// deprecated — use X instead`. 지웠으면 지운 거다 — 묘비를 남기지 마라.
- **Section dividers**: `// === Helpers ===`, `// --- Setup ---`. 파일에 이정표가 필요하다면 그건 파일이 너무 크다는 뜻이다 — 쪼개라.
- **TODO/FIXME without an owner or ticket**: 추적되지 않는 TODO는 아무도 안 지킬 약속이다. 이슈로 등록하든가 아예 쓰지 마라.

## Tension with other habits

방어적 주석은 종종 꼼꼼함인 척한다. 그쪽으로 흘러가고 있다는 신호:

- 블록이 주석 없이 "허전해서" 주석을 달고 있다
- 주석이 바로 다음 세 줄을 풀어 쓴 것이다
- 코드를 문서화하는 게 아니라 지금 작업을 가상의 리뷰어에게 설명하고 있다
- 안에서 비자명한 일이 일어나든 말든 모든 함수에 docstring이 붙어 있다

이 신호 중 하나라도 잡히면, 주석을 지우고 코드를 믿어라.

## Rules

- 주석을 안 쓰는 게 기본이다. 주석마다 정당화가 필요하고, 안 쓰는 데는 필요 없다.
- 주석이 정당할 때는 WHY부터 써라. 정확한 한 문장이 한 문단을 이긴다.
- 코드 주석에서 지금 작업, PR, 호출자를 절대 언급하지 마라 — 그 맥락은 PR 본문이나 커밋 메시지에 들어갈 내용이지 소스가 아니다.
- subagent에 구현 작업을 브리핑할 때는 이 규칙을 다시 말해라. 기본 지시는 위임을 거치면 신뢰할 만큼 보존되지 않는다.
- docstring에도 같은 규율을 적용하라 — 시그니처를 풀어 쓴 건 잡음이다. 예외: 언어 도구가 public API 문서를 강제할 때 (Go `revive`, Rust `missing_docs`, Python `pydocstyle`), exported 식별자에 한 줄짜리 계약 설명을 다는 건 괜찮다. 본문은 시그니처를 풀어 쓰는 게 아니라 계약을 설명해야 한다.
