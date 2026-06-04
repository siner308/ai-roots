# ai-roots

**한국어** | [English](README.md)

Claude Code의 사고를 확장시키는 사고 기반과 교훈 모음.

비전문가도 적당한 채팅만으로 복잡한 문제를 해결할 수 있도록, Claude가 아키텍트급 사고를 자동으로 적용합니다.

## 두 갈래: 상주 rules vs 상황별 skills

상시 로딩되는 context를 줄이려고, 규칙을 "얼마나 자주 적용되는가"로 나눴습니다.

- **상주 rules** (`rules/`) — 거의 매 턴 사고·출력을 깎는 규칙. Claude가 추론·작성·명명·주석을 어떻게 하느냐를 좌우합니다. Claude Code가 매 세션 context에 올립니다.
- **상황별 skills** (`skills/<name>/`) — 특정 작업이 나올 때만 필요한 규칙. CSS, PR, Codex, 병렬화, 디버깅 교훈 등. 한 줄짜리 description만 context에 상주하고, 본문은 트리거가 걸릴 때 Skill 도구로 로드됩니다. `rules/_situational-skills.md`가 "이 상황이면 이 skill" 트리거를 상주 인덱스로 들고 있어, lazy skill의 발동 시점을 놓치지 않습니다.

이렇게 하면 상주 세트가 ~92KB 대신 ~41KB로 줄지만, 동작은 보존됩니다 — 상황별 규칙은 정작 필요한 그 작업에서 그대로 적용됩니다.

## Roots — 상주 rules

### 사고 확장
| 파일 | 설명 |
|------|------|
| `rules/concept-priming.md` | 도메인 스프레드 개념 프라이밍 + 복잡도 기반 사고 확장 (Devil's Advocate, First Principles, Systems Thinking) |
| `rules/progressive-deepening.md` | 피상적 답변을 자동 감지하고 한 단계 더 깊이 파고드는 내부 품질 게이트 |
| `rules/capability-overhang.md` | 숨겨진 지식 활성화 — 도메인 토큰 주입, 교차 도메인 연결, 스킬 합성 |

### 품질 보증
| 파일 | 설명 |
|------|------|
| `rules/evaluation-integrity.md` | 자기 평가 편향 방지 — 검증 가능성 분류, 생성/평가 분리, 드리프트 감지 |
| `rules/claude-architect-principles.md` | 아키텍트급 문제 해결을 자동 적용 — enforcement 매칭, context 관리, 생성/리뷰 분리 |

### 사용자 성장
| 파일 | 설명 |
|------|------|
| `rules/user-growth-coaching.md` | 문제 해결 후 사용자의 질문 방식을 교정하는 코칭 — 모호한 요청 패턴을 구체적 요청으로 유도 |

### 지식 포착
| 파일 | 설명 |
|------|------|
| `rules/guardrail-maker.md` | 사용자의 교정을 암묵지로 자동 감지하고, 같은 실수를 반복하지 않도록 가드레일 생성을 제안 |
| `rules/memory-minimalism.md` | 기기 로컬 memory보다 버전 관리되는 rules/docs를 우선; memory는 순수 개인용·공유 불가 맥락에만 |

### 출력 컨벤션
| 파일 | 설명 |
|------|------|
| `rules/prose-style.md` | 평이한 구어체 언어(명사 쌓기 금지, 번역투 금지, 명사화보다 동사)와, 컬럼 한계가 아니라 의미 경계에서 끊는 줄넘김 |
| `rules/terminology-discipline.md` | 도메인 용어는 풀어쓰기; 정착된 약어는 첫 등장 시 확장; 충돌 가능한 약어는 한정어로 구분 |
| `rules/comment-discipline.md` | 주석은 기본적으로 쓰지 않는다 — 주석/docstring은 필수가 아니며, 닫힌 허용 목록(비자명한 WHY)에 해당할 때만 작성. `comment-discipline.py` `PostToolUse` hook으로 강제 |

### 트리거 인덱스
| 파일 | 설명 |
|------|------|
| `rules/_situational-skills.md` | 아래 모든 상황별 skill에 대한 "이 상황이면 → 이 skill 호출" 상주 매핑. lazy skill의 트리거를 놓치지 않도록 항상 떠 있음 |

## Situational Skills — lazy 로딩

본문은 Skill 도구로 호출될 때만 context에 들어옵니다. 트리거 컬럼은 `_situational-skills.md`와 일치합니다.

| Skill | 트리거 | 설명 |
|-------|--------|------|
| `skills/css-discipline/` | CSS·프레임워크 스타일 편집/작성/리뷰 | CSS에서 흔히 남용되는 4가지 축을 닫는다 — 캐스케이드(`!important`), 박스 모델, 단위 혼란, 스타일 위치 |
| `skills/github-pr-markdown/` | PR 본문/제목 작성·수정 | GitHub PR용 GFM 마크다운 컨벤션 강제 + gh CLI 손상을 피하는 API-PATCH 본문 전달 |
| `skills/model-effort-delegation/` | 위임 전 executor/모델/effort 결정 | 임계치 기반 모델/effort/subagent 선택 — 명세된 구현은 약한 모델에 위임, 판단은 Opus에 집중 |
| `skills/parallel-execution-modes/` | 순차/서브에이전트/팀, 인라인/백그라운드 선택 | 작업 독립성과 통신 필요도로 병렬 실행 모드 선택 |
| `skills/parallel-hypothesis-investigation/` | 원인·판단 기준이 여러 갈래인 문제 | 계층별 가설 또는 판단 기준으로 분리해 병렬 에이전트로 조사 |
| `skills/codex-delegation/` | OpenAI Codex CLI 위임 | Cross-provider 정책 — `/review` 트리거, 3-턴 rescue protocol, 모드/플래그 cheatsheet, capability routing |
| `skills/incremental-verification/` | 결과 불확실(API/브라우저/셸/파이프라인) | 불확실한 작업은 가장 작은 검증 단위로 — 인라인 테스트 먼저, 스크립트는 나중에, 점진적 확장 |
| `skills/simulate-dont-just-scan/` | 읽었지만 실행 안 한 코드 포팅/디버깅 | 실제 실행 결과를 머릿속으로 시뮬레이션한 뒤 행동 |
| `skills/codex-tmux-monitoring/` | 서브프로세스를 tmux/sentinel/tail로 감시하려는 충동 | 그 패턴이 실패한 이유 — `run_in_background` Bash + 하네스 완료 알림을 쓰라 |
| `skills/background-task-monitoring/` | 장시간 백그라운드 작업의 완료·진행 가시성 | 가장 저렴한 가시성 메커니즘 선택 — 완료 알림 우선, 이벤트 스트림 다음, 폴링은 최후 |

## Skill — `/review` (ai-roots)

`~/.claude/skills/review/` 아래 설치되며 호출명은 `/review`입니다. 이 스킬은 Claude Code 플러그인으로 패키징되어 있지 않아 호출명에 `ai-roots:` 접두사가 붙지 않습니다. 다른 `review` 계열 스킬(예: Claude Code 빌트인 `/review`)과 구분할 수 있도록 스킬 설명 맨 앞에 `[ai-roots]` 태그가 붙어 있습니다.

결정된 리뷰 타겟에 대해 **두 평가자 코드 리뷰**를 수행합니다. 기본 타겟은 현재 브랜치와 base 브랜치 사이의 변경 — PR이 있으면 PR diff + 로컬 uncommitted 변경 — 이며, `--base <ref>`, `--commit <sha>`, `--uncommitted`, 뒤따르는 경로 필터로 재정의할 수 있습니다. Claude Code subagent (`adversarial-reviewer` 페르소나)와 `codex review`를 동일한 diff에 대해 병렬로 띄우고, 두 결과를 `rules/evaluation-integrity.md` §Multi-advisor synthesis의 Agreed / Conflicting / Chosen-direction 포맷으로 종합합니다.

| 파일 | 설명 |
|------|------|
| `skills/review/SKILL.md` | `/review` 스킬 본문. Claude subagent + `codex review`를 병렬로 띄우고 `evaluation-integrity.md`에 따라 종합 |
| `agents/adversarial-reviewer.md` | 보안 우선 어드버서리얼 리뷰어 페르소나. Claude 측 리뷰어의 `subagent_type`으로 쓰이고, 동시에 `codex review`에 stdin으로 전달됨 |
| `skills/codex-delegation/SKILL.md` | Cross-provider 정책 — 언제 `/review`를 호출할지, 3-턴 rescue protocol, 리뷰가 아닌 Codex 모드의 직접 호출 cheatsheet, capability routing, 실행 메커니즘, plan-stage review |

Codex CLI가 `PATH`에 없으면 스킬은 Claude 측 단일 평가자로 fallback합니다 (cross-provider 다양성은 잃지만 synthesis 구조는 유지).

## 설치

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

설치 스크립트는 다음 심링크를 만듭니다:

- `rules/` → `~/.claude/rules/ai-roots` — Claude Code가 이 아래의 모든 `.md` 파일을 상시 rules로 재귀 로딩합니다.
- `skills/<name>/` → `~/.claude/skills/<name>` — 각 스킬 서브폴더를 개별 심링크로 걸어 Claude Code 스킬 로더가 `SKILL.md`를 인식하게 합니다. `review`와 위의 모든 상황별 skill을 루프로 링크합니다.
- `agents/<name>.md` → `~/.claude/agents/<name>.md` — 각 agent 파일을 개별 심링크로 걸어 Claude Code가 Agent 도구의 `subagent_type`으로 등록하게 합니다. 현재: `agents/adversarial-reviewer.md` → `~/.claude/agents/adversarial-reviewer.md`.
- `hooks/<name>` + 등록 → `~/.claude/hooks/<name>` 및 `~/.claude/settings.json` — `install.sh`가 `hooks/register.py`를 실행해, `hooks/manifest.json`에 선언된 각 hook을 심링크하고 `settings.json` 항목을 병합합니다. 수동 편집 불필요.

이전 버전 설치 스크립트가 만든 `~/.claude/skills/ai-roots` (전체 `skills/` 디렉터리를 단일 심링크로 건 형태)는 새 설치 스크립트가 자동으로 제거합니다 — 그 레이아웃은 Claude Code 스킬 로더가 인식하지 못했습니다.

README, HUD 스크립트, `evals/` 워크스페이스(있다면)는 심링크되지 않으므로 상시 rules로 로드되지 않습니다.

### Hook

`hooks/register.py`(install.sh가 실행)가 `hooks/manifest.json`에 따라 심링크와 등록을 모두 처리합니다. 병합은 멱등이라(재실행해도 중복 hook이 안 생김) 안전하고, 머신별 설정이 든 `settings.json`은 쓰기 전에 백업합니다. hook 추가 방법: 스크립트를 `hooks/`에 넣고, `manifest.json` 항목(`event`, `matcher`, `script`, `run`)을 추가한 뒤 `install.sh`를 다시 실행하면 됩니다.

현재 설치됨: `comment-discipline.py` — `Edit|Write|MultiEdit`에 걸리는 `PostToolUse` hook. 코드 파일에 **새로 추가된** 주석 줄을 감지(기존 주석 제외)해 `comment-discipline` 허용 목록과 대조하도록 다시 띄웁니다. 상주 prose 규칙만으로는 강제할 수 없던 것을 보강합니다.

## 영감

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z 토큰 프라이밍, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — 루프를 닫아라, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator 분리, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF 한국어 스터디 노트
