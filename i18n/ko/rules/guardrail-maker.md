# Guardrail Maker — Tacit Knowledge Auto-Capture

사용자가 네 이해나 동작을 교정할 때, 그 교정은 암묵지가 수면 위로 떠오른 것이다. 그걸 자동으로 감지하고, 같은 교정이 두 번 필요 없도록 지속되는 가드레일을 제안하라.

## 감지

모든 사용자 메시지에서 교정 신호를 살펴라. 감지는 글자 그대로가 아니라 의미 기반이다 — 언어나 표현과 무관하게 의도를 맞춰라.

### Tier 1 — 직접 교정 (높은 확신)

사용자가 뭔가 틀렸다고 명시적으로 말하고 옳은 답을 준다. 정체성/의미 교정, 금지("하지 마 / 그만 / 절대"), 의무("항상 / 이제부터"), 대체("Y 말고 X를 써라")를 포함한다.

### Tier 2 — 반복된 교정 (높은 확신)

전에도 이걸 교정했다고 사용자가 신호한다. 그 간극이 반복적으로 낭비를 일으키고 있으니 가치가 가장 높은 후보다 — "이거 전에 말했잖아", "또 같은 실수", "몇 번을 말해야 해".

### Tier 3 — 컨벤션 선언 (중간 확신)

앞선 실수 없이, 사용자가 프로젝트·팀·도메인 규칙을 미리 밝힌다 — 명명 규칙, 아키텍처 패턴, 워크플로 규칙, 도메인 용어 정의.

### Tier 4 — 암묵적 교정 (중간 확신)

완전히 명시하지 않으면서 뭔가 어긋났다고 사용자가 신호한다 — "딱 맞진 않아", "비슷한데 정확히는 아니야", 네가 이해한 듯한 걸 말없이 다시 표현하거나, 네 출력을 조용히 고치고 계속 진행하는 것. 제안하기 전에 가치 여부를 더 신중히 확인하라.

### Tier 5 — 답답함 신호 (최고 긴급도)

반복적이거나 뻔한 실수에 대한 감정적 짜증 — 어느 언어든 한숨, 강조를 더해 다시 보낸 지시, 짧고 날 선 응답("아니.", "틀렸어.", "또?"). Tier 2의 긴급도로 다뤄라.

## 대응 절차

### Step 1: 먼저 적용하고, 제안은 그다음

교정을 즉시 받아들여라. 지금 작업부터 고치고, 가드레일은 그다음에 제안하라.

### Step 2: 가드레일로 만들 가치가 있는지 따져보기

| Capture as guardrail | Skip |
|---------------------|----------------|
| 미래 작업에 적용되는 컨벤션 | 일회성 사실 오류 (틀린 파일 경로, 오타) |
| 반복되는 교정 패턴 | 명확화로 풀린 단순 오해 |
| 코드에서 도출 안 되는 도메인 지식 | 기존 rules나 CLAUDE.md에 이미 있는 정보 |
| 행동 규칙 (always/never 패턴) | 현재 대화에만 해당하는 작업별 선호 |
| 프로젝트를 가로지르는 원칙 | 일시적 상태에 대한 교정 (브랜치 이름, 현재 PR) |

### Step 3: 가드레일 제안하기

교정을 적용한 뒤, 이 제안을 덧붙여라:

```
---
Guardrail proposal — saving this as a rule prevents the same mistake in future conversations.

Rule: [one-line rule in imperative form]
Example: [concrete good/bad pair if applicable]
Location: [placement recommendation with rationale]
```

사용자가 눈에 띄게 짜증 났으면 (Tier 5), 한 줄로 줄여라:
```
---
Guardrail proposal: "[one-line rule]" — save to [location]?
```

쓰기 전에 사용자 확인을 기다려라.

### Step 4: 확인을 받으면 쓰기

1. **Search for overlap** — 기존 rules와 CLAUDE.md에서 관련 내용을 확인하라
2. **If overlap found** — 기존 규칙을 업데이트하자고 제안하고, diff를 보여줘라
3. **If new** — 합의된 위치에 쓰되, 대상 파일의 기존 스타일에 맞춰라
4. **After writing** — 무엇을 어디에 썼는지 확인해줘라

## 배치 결정

| Signal | Location | Rationale |
|--------|----------|-----------|
| 상시 원칙 (사실상 매 턴을 깎음) | `ai-roots/rules/` | `~/.claude/rules/ai-roots/`로 심링크됨, 매 세션 상주 |
| 상황별 원칙이나 교훈 (특정 작업 맥락에서만 적용) | `ai-roots/skills/<name>/SKILL.md` + `rules/_situational-skills.md`의 트리거 행 | lazy 로딩 skill — 트리거가 걸릴 때만 본문이 context에 들어와 상주 세트를 작게 유지 |
| 프로젝트별 컨벤션 | Project `CLAUDE.md` | 프로젝트 단위로 로드됨 |
| 프로젝트별, 독립 주제 | Project `.claude/rules/` | 모듈식, CLAUDE.md가 비대해지는 걸 막음 |
| 기존 규칙을 업데이트 | 기존과 같은 파일 | 파편화를 막음 |

**Always-on rules vs situational skills:** 규칙이 `rules/`에 속하려면 사실상 매 턴 사고나 출력을 깎아야 한다 (어떻게 추론·작성·명명·주석하는지). 특정 작업 유형이 나올 때만 적용된다면 — CSS, PR, Codex, 병렬화, 또는 구체적인 디버깅 교훈 — `skills/<name>/SKILL.md` 아래 skill로 만들고 `rules/_situational-skills.md`에 트리거 행을 추가하라. "X 해봤는데 Z 때문에 Y가 더 낫더라" 류 교훈은 본질상 상황별이라, 이제는 상주 규칙이 아니라 skill이다. 상시 → rule, 상황별 → skill.

**Writing location:** `~/.claude/rules/ai-roots`는 이 저장소의 `rules/` 디렉터리로 가는 심링크다. `readlink -f ~/.claude/rules/ai-roots`로 실제 repo 경로를 풀고, 상주 규칙은 git이 추적하는 실제 트리(`rules/...`)에 써라 — 절대 `~/.claude/rules/ai-roots/...`에 직접 쓰지 마라. 심링크는 헷갈리기 쉽고 정본은 git repo이기 때문이다. 상황별 skill은 같은 repo의 `skills/<name>/SKILL.md`에 두고(각각 `name`과 트리거 중심 `description`을 담은 YAML frontmatter가 필요하다), `install.sh`를 다시 돌리면 `~/.claude/skills/`로 심링크된다.

scope가 불확실하면, 이 규칙이 다른 프로젝트에도 적용되는지 사용자에게 물어라.

## 작성 기준

잘 만든 가드레일은:
- **Imperative form** — "You should use X"보다 "Use X"
- **Concrete example** — 구분이 미묘할 때 최소 하나의 good/bad 쌍
- **Brief rationale** — WHY를 한 문장으로, 그래야 엣지 케이스를 판단할 수 있다
- **Self-contained** — 다른 규칙을 안 읽어도 이해된다
- **Positive framing preferred** — "Don't use Y"보다 "Use X". 단, 실수 자체가 핵심 신호일 때는 금지형도 괜찮다

## 경계

- 가드레일은 사용자 확인을 받은 뒤에만 쓴다
- 미래의 실수를 막는 교정만 포착하고, 나머지는 흘려보낸다
- memory 시스템을 보완한다 — memory는 맥락을 추적하고, 가드레일은 동작을 강제한다
