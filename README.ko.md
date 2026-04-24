# ai-roots

**한국어** | [English](README.md)

Claude Code의 사고를 확장시키는 사고 기반과 교훈 모음.

비전문가도 적당한 채팅만으로 복잡한 문제를 해결할 수 있도록, Claude가 아키텍트급 사고를 자동으로 적용합니다.

## Roots — 사고 기반

### 사고 확장
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/concept-priming.md` | 도메인 스프레드 개념 프라이밍 + 복잡도 기반 사고 확장 (Devil's Advocate, First Principles, Systems Thinking) |
| `claude-rules/roots/progressive-deepening.md` | 피상적 답변을 자동 감지하고 한 단계 더 깊이 파고드는 내부 품질 게이트 |
| `claude-rules/roots/capability-overhang.md` | 숨겨진 지식 활성화 — 도메인 토큰 주입, 교차 도메인 연결, 스킬 합성 |

### 품질 보증
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/evaluation-integrity.md` | 자기 평가 편향 방지 — 검증 가능성 분류, 생성/평가 분리, 드리프트 감지 |
| `claude-rules/roots/claude-architect-principles.md` | 아키텍트급 문제 해결을 자동 적용 — enforcement 매칭, context 관리, 생성/리뷰 분리 |

### 문제 해결 전략
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/parallel-hypothesis-investigation.md` | 복잡한 문제를 계층별 가설로 분리하고 병렬 에이전트로 동시 조사 |
| `claude-rules/roots/parallel-execution-modes.md` | 작업 독립성과 통신 필요도에 따라 순차/서브에이전트/팀 기반 병렬 실행 선택 |
| `claude-rules/roots/model-effort-delegation.md` | 임계치 기반 모델/effort/subagent 선택 — 명세된 구현은 약한 모델에 위임, 판단은 Opus에 집중 |

### 사용자 성장
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/user-growth-coaching.md` | 문제 해결 후 사용자의 질문 방식을 교정하는 코칭 — 모호한 요청 패턴을 구체적 요청으로 유도 |

### 지식 포착
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/guardrail-maker.md` | 사용자의 교정을 암묵지로 자동 감지하고, 같은 실수를 반복하지 않도록 가드레일 생성을 제안 |

### 컨벤션
| 파일 | 설명 |
|------|------|
| `claude-rules/roots/github-pr-markdown.md` | GitHub PR 작성 시 GFM 마크다운 컨벤션 강제 |
| `claude-rules/roots/comment-discipline.md` | 주석은 기본적으로 쓰지 않는다 — WHY가 비자명할 때만 작성, WHAT 설명/작업 맥락 언급/제거 흔적 금지 |
| `claude-rules/roots/css-discipline.md` | CSS에서 흔히 남용되는 4가지 축을 닫는다 — 캐스케이드(`!important`), 박스 모델(간격용 margin, 목적 없는 overflow: hidden), 단위 혼란(리터럴 픽셀/컬러), 스타일 위치(유틸리티/스코프/인라인 3계층) |

## Lessons — 시행착오 교훈

실제 실수에서 배운 구체적 패턴입니다. 피해야 할 것이 아니라, 더 나은 방법을 기록합니다.

| 파일 | 설명 |
|------|------|
| `claude-rules/lessons/incremental-verification.md` | 불확실한 작업은 가장 작은 검증 단위로 쪼개기 — 인라인 테스트 먼저, 스크립트는 나중에, 점진적 확장 |
| `claude-rules/lessons/background-task-monitoring.md` | 장시간 백그라운드 작업은 자동 주기 모니터링 설정 — 사용자가 "다 됐나요?" 물어보게 만들지 않기 |
| `claude-rules/lessons/simulate-dont-just-scan.md` | 실제로 실행했을 때 어떤 결과가 나올지 머릿속으로 시뮬레이션 — 소스를 읽은 것과 런타임 동작을 이해한 것은 다르다 |

## 다중 에이전트 오케스트레이션 (선택)

Claude Code와 OpenAI Codex를 함께 쓸 때 참고. Codex 연동은 **선택 사항** — 아래 중 하나라도 필요하면 사용을 권장합니다:

- (a) **Cross-family 어드버서리얼 리뷰** — 다른 학습 분포가 Claude 혼자 놓치는 사각지대를 잡아냄
- (b) **Anchoring 탈출** — 어려운 문제에서 3-턴 cap 후 fresh stack으로 anchoring 트랩 해제
- (c) **OpenAI 생태계 전용 기능** — 이미지 생성(DALL-E, `gpt-image`) 등 Claude Code가 기본으로 가지지 않는 OpenAI 전용 모달리티

위 중 해당사항이 없다면 건너뛰어도 됩니다. Claude Code 토큰이 넉넉한 것만으로도 건너뛰는 충분한 이유가 됩니다.

| 파일 | 설명 |
|------|------|
| `.claude/agents/adversarial-reviewer.md` | 보안 우선 어드버서리얼 리뷰어 페르소나. Claude Code의 Agent 도구로도 호출 가능하고, `/codex:adversarial-review` 호출 시 system prompt로 붙여쓸 수 있는 self-contained 프롬프트 |

라우팅 규칙 (어려운 문제 3-턴 cap, 보안 민감 경로 adversarial review, 이미지 생성 등 capability 라우팅)은 `claude-rules/roots/model-effort-delegation.md` §Cross-Provider Delegation (Codex)에 있습니다. 이것은 **Claude 측** 규칙 — 언제 Codex를 호출할지를 Claude에게 알려주는 것이고, Codex의 동작 방식을 규정하지 않습니다.

## 설치

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

`claude-rules/`만 `~/.claude/rules/ai-roots`로 심링크됩니다. README, HUD 스크립트, agent prompt는 상시 rules로 로드되지 않습니다. Claude Code가 `claude-rules/roots/`와 `claude-rules/lessons/` 하위의 모든 `.md` 파일을 재귀적으로 로드합니다.

## 영감

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z 토큰 프라이밍, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — 루프를 닫아라, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator 분리, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF 한국어 스터디 노트
