# ai-roots

**한국어** | [English](README.md)

Claude Code의 사고를 확장시키는 글로벌 규칙 모음.

비전문가도 적당한 채팅만으로 복잡한 문제를 해결할 수 있도록, Claude가 아키텍트급 사고를 자동으로 적용합니다.

## 규칙 목록

### 사고 확장
| 파일 | 설명 |
|------|------|
| `az-mindset.md` | A-Z 토큰 프라이밍 + 복잡도 기반 사고 확장 (Devil's Advocate, First Principles, Systems Thinking) |
| `progressive-deepening.md` | 피상적 답변을 자동 감지하고 한 단계 더 깊이 파고드는 내부 품질 게이트 |
| `capability-overhang.md` | 숨겨진 지식 활성화 — 도메인 토큰 주입, 교차 도메인 연결, 스킬 합성 |

### 품질 보증
| 파일 | 설명 |
|------|------|
| `evaluation-integrity.md` | 자기 평가 편향 방지 — 검증 가능성 분류, 생성/평가 분리, 드리프트 감지 |
| `claude-architect-principles.md` | 아키텍트급 문제 해결을 자동 적용 — enforcement 매칭, context 관리, 생성/리뷰 분리 |

### 문제 해결 전략
| 파일 | 설명 |
|------|------|
| `parallel-hypothesis-investigation.md` | 복잡한 문제를 계층별 가설로 분리하고 병렬 에이전트로 동시 조사 |

### 사용자 성장
| 파일 | 설명 |
|------|------|
| `user-growth-coaching.md` | 문제 해결 후 사용자의 질문 방식을 교정하는 코칭 — 모호한 요청 패턴을 구체적 요청으로 유도 |

### 지식 포착
| 파일 | 설명 |
|------|------|
| `guardrail-maker.md` | 사용자의 교정을 암묵지로 자동 감지하고, 같은 실수를 반복하지 않도록 가드레일 생성을 제안 |

### 컨벤션
| 파일 | 설명 |
|------|------|
| `github-pr-markdown.md` | GitHub PR 작성 시 GFM 마크다운 컨벤션 강제 |

## 설치

```bash
git clone https://github.com/siner308/ai-roots.git
cd ai-roots
chmod +x install.sh
./install.sh
```

`~/.claude/rules/`에 심볼릭 링크가 생성됩니다. 레포에서 규칙을 수정하면 바로 반영됩니다.

## 영감

- [AI Frontier EP82](https://aifrontier.kr/ko/episodes/ep82) — A-Z 토큰 프라이밍, Domain Token Injection, Skill Composition
- [AI Frontier EP87](https://aifrontier.kr/ko/episodes/ep87) — March of Nines
- [AI Frontier EP89](https://aifrontier.kr/ko/episodes/ep89) — Click vs Clunk, Problem Definition > Problem Solving
- [AI Frontier EP91](https://aifrontier.kr/ko/episodes/ep91) — Capability Overhang
- [AI Frontier EP92](https://aifrontier.kr/ko/episodes/ep92/) — 루프를 닫아라, Verifiable vs Non-verifiable
- [Anthropic Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) — Generator/Evaluator 분리, Self-evaluation Bias
- [CCAF Exam Guide](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F8lsy243ftffjjy1cx9lm3o2bw%2Fpublic%2F1773274827%2FClaude+Certified+Architect+%E2%80%93+Foundations+Certification+Exam+Guide.pdf) — Agentic Architecture, Tool Design, Context Management
- [CCAF 101 Study Notes](https://bitboom.github.io/ccaf101/) — CCAF 한국어 스터디 노트
