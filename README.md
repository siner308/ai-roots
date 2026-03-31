# ai-roots

Claude Code의 사고를 확장시키는 글로벌 규칙 모음.

## 규칙 목록

| 파일 | 설명 |
|------|------|
| `az-mindset.md` | A-Z 토큰 프라이밍 + 복잡도 기반 사고 확장 (Devil's Advocate, First Principles, Systems Thinking) |
| `progressive-deepening.md` | 피상적 답변을 자동 감지하고 한 단계 더 깊이 파고드는 내부 품질 게이트 |
| `capability-overhang.md` | 숨겨진 지식 활성화 — 도메인 토큰 주입, 교차 도메인 연결, 스킬 합성 |
| `evaluation-integrity.md` | 자기 평가 편향 방지 — 검증 가능성 분류, 생성/평가 분리, 드리프트 감지 |


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