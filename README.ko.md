# ai-roots

**한국어** | [English](README.md)

Claude Code의 사고를 확장시키는 사고 기반과 교훈 모음.

비전문가도 적당한 채팅만으로 복잡한 문제를 해결할 수 있도록, Claude가 아키텍트급 사고를 자동으로 적용합니다.

## Roots — 사고 기반

### 사고 확장
| 파일 | 설명 |
|------|------|
| `rules/roots/concept-priming.md` | 도메인 스프레드 개념 프라이밍 + 복잡도 기반 사고 확장 (Devil's Advocate, First Principles, Systems Thinking) |
| `rules/roots/progressive-deepening.md` | 피상적 답변을 자동 감지하고 한 단계 더 깊이 파고드는 내부 품질 게이트 |
| `rules/roots/capability-overhang.md` | 숨겨진 지식 활성화 — 도메인 토큰 주입, 교차 도메인 연결, 스킬 합성 |

### 품질 보증
| 파일 | 설명 |
|------|------|
| `rules/roots/evaluation-integrity.md` | 자기 평가 편향 방지 — 검증 가능성 분류, 생성/평가 분리, 드리프트 감지 |
| `rules/roots/claude-architect-principles.md` | 아키텍트급 문제 해결을 자동 적용 — enforcement 매칭, context 관리, 생성/리뷰 분리 |

### 문제 해결 전략
| 파일 | 설명 |
|------|------|
| `rules/roots/parallel-hypothesis-investigation.md` | 복잡한 문제를 계층별 가설로 분리하고 병렬 에이전트로 동시 조사 |
| `rules/roots/parallel-execution-modes.md` | 작업 독립성과 통신 필요도에 따라 순차/서브에이전트/팀 기반 병렬 실행 선택 |
| `rules/roots/model-effort-delegation.md` | 임계치 기반 모델/effort/subagent 선택 — 명세된 구현은 약한 모델에 위임, 판단은 Opus에 집중 |

### 사용자 성장
| 파일 | 설명 |
|------|------|
| `rules/roots/user-growth-coaching.md` | 문제 해결 후 사용자의 질문 방식을 교정하는 코칭 — 모호한 요청 패턴을 구체적 요청으로 유도 |

### 지식 포착
| 파일 | 설명 |
|------|------|
| `rules/roots/guardrail-maker.md` | 사용자의 교정을 암묵지로 자동 감지하고, 같은 실수를 반복하지 않도록 가드레일 생성을 제안 |

### 컨벤션
| 파일 | 설명 |
|------|------|
| `rules/roots/github-pr-markdown.md` | GitHub PR 작성 시 GFM 마크다운 컨벤션 강제 |
| `rules/roots/comment-discipline.md` | 주석은 기본적으로 쓰지 않는다 — WHY가 비자명할 때만 작성, WHAT 설명/작업 맥락 언급/제거 흔적 금지 |
| `rules/roots/css-discipline.md` | CSS에서 흔히 남용되는 4가지 축을 닫는다 — 캐스케이드(`!important`), 박스 모델(간격용 margin, 목적 없는 overflow: hidden), 단위 혼란(리터럴 픽셀/컬러), 스타일 위치(유틸리티/스코프/인라인 3계층) |

## Lessons — 시행착오 교훈

실제 실수에서 배운 구체적 패턴입니다. 피해야 할 것이 아니라, 더 나은 방법을 기록합니다.

| 파일 | 설명 |
|------|------|
| `rules/lessons/incremental-verification.md` | 불확실한 작업은 가장 작은 검증 단위로 쪼개기 — 인라인 테스트 먼저, 스크립트는 나중에, 점진적 확장 |
| `rules/lessons/background-task-monitoring.md` | 장시간 백그라운드 작업은 가장 저렴한 가시성 메커니즘 선택 — 완료 알림이 기본, 이벤트 스트림은 그 다음, 주기 폴링은 최후 fallback |
| `rules/lessons/simulate-dont-just-scan.md` | 실제로 실행했을 때 어떤 결과가 나올지 머릿속으로 시뮬레이션 — 소스를 읽은 것과 런타임 동작을 이해한 것은 다르다 |
| `rules/lessons/codex-tmux-monitoring.md` | 백그라운드 Codex 실행 모니터링용 tmux split-pane + sentinel 패턴이 실패한 이유 — wake-up과 live-output을 별개 메커니즘으로 분리하라 |

## Skill — `/review` (ai-roots)

`~/.claude/skills/review/` 아래 단일 스킬이 설치되며, 호출명은 `/review`입니다. 이 스킬은 Claude Code 플러그인으로 패키징되어 있지 않아 호출명에 `ai-roots:` 접두사가 붙지 않습니다. 다른 `review` 계열 스킬(예: Claude Code 빌트인 `/review`)과 구분할 수 있도록 스킬 설명 맨 앞에 `[ai-roots]` 태그가 붙어 있습니다.

현재 uncommitted diff에 대해 **두 평가자 코드 리뷰**를 수행합니다. Claude Code subagent (`adversarial-reviewer` 페르소나)와 `codex review`를 병렬로 띄우고, 두 결과를 `rules/roots/evaluation-integrity.md` §Multi-advisor synthesis의 Agreed / Conflicting / Chosen-direction 포맷으로 종합합니다.

| 파일 | 설명 |
|------|------|
| `skills/review/SKILL.md` | `/review` 스킬 본문. Claude subagent + `codex review`를 병렬로 띄우고 `evaluation-integrity.md`에 따라 종합 |
| `agents/adversarial-reviewer.md` | 보안 우선 어드버서리얼 리뷰어 페르소나. Claude 측 리뷰어의 `subagent_type`으로 쓰이고, 동시에 `codex review`에 stdin으로 전달됨 |
| `rules/codex/codex-delegation.md` | Cross-provider 정책 — 언제 `/review`를 호출할지, 3-턴 rescue protocol, 리뷰가 아닌 Codex 모드의 직접 호출 cheatsheet, capability routing, 실행 메커니즘, plan-stage review |

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
- `skills/<name>/` → `~/.claude/skills/<name>` — 각 스킬 서브폴더를 개별 심링크로 걸어 Claude Code 스킬 로더가 `SKILL.md`를 인식하게 합니다. 현재: `skills/review/` → `~/.claude/skills/review` (설명에 `[ai-roots]` 태그).
- `agents/<name>.md` → `~/.claude/agents/<name>.md` — 각 agent 파일을 개별 심링크로 걸어 Claude Code가 Agent 도구의 `subagent_type`으로 등록하게 합니다. 현재: `agents/adversarial-reviewer.md` → `~/.claude/agents/adversarial-reviewer.md`.

이전 버전 설치 스크립트가 만든 `~/.claude/skills/ai-roots` (전체 `skills/` 디렉터리를 단일 심링크로 건 형태)는 새 설치 스크립트가 자동으로 제거합니다 — 그 레이아웃은 Claude Code 스킬 로더가 인식하지 못했습니다.

README, HUD 스크립트, `evals/` 워크스페이스(있다면)는 심링크되지 않으므로 상시 rules로 로드되지 않습니다.

## 영감

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z 토큰 프라이밍, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — 루프를 닫아라, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator 분리, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF 한국어 스터디 노트
