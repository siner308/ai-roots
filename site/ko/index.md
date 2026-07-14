---
layout: home

hero:
  name: ai-roots
  text: Claude Code를 위한 사고 기반
  tagline: 상주 rules, 상황별 skills, agents를 모아 Claude가 아키텍트급 사고를 자동으로 적용하게 합니다.
  actions:
    - theme: brand
      text: 상주 rules
      link: /ko/rules/thinking-expansion
    - theme: alt
      text: 상황별 skills
      link: /ko/skills/css-discipline
    - theme: alt
      text: GitHub
      link: https://github.com/siner308/ai-roots

features:
  - title: 상주 rules
    details: 매 세션 로드됩니다 — Claude가 추론·작성·명명·주석을 어떻게 하느냐를 좌우해요. 일부러 작게 유지합니다.
    link: /ko/rules/thinking-expansion
  - title: 상황별 skills
    details: 트리거가 걸릴 때만 로드됩니다. CSS, PR, Codex, 병렬화, 디버깅 교훈 — 본문은 그 작업이 나올 때만 context에 올라와요.
    link: /ko/skills/css-discipline
  - title: Agents
    details: adversarial reviewer 같은 전용 페르소나. 집중 리뷰가 필요할 때 불러서 씁니다.
    link: /ko/agents/adversarial-reviewer
---

## 두 갈래: 상주 rules vs 상황별 skills

상시 로딩되는 context를 줄이려고, 규칙을 "얼마나 자주 적용되는가"로 나눴습니다.

- **상주 rules** (`rules/`) — 거의 매 턴 사고·출력을 깎는 규칙. Claude가 추론·작성·명명·주석을 어떻게 하느냐를 좌우합니다. Claude Code가 매 세션 context에 올립니다.
- **상황별 skills** (`skills/<name>/`) — 특정 작업이 나올 때만 필요한 규칙. CSS, PR, Codex, 병렬화, 디버깅 교훈 등. 한 줄짜리 description만 context에 상주하고, 본문은 트리거가 걸릴 때 Skill 도구로 로드됩니다.

이렇게 하면 상시 로드되는 양이 전체의 일부로 줄지만, 동작은 보존됩니다 — 상황별 규칙은 정작 필요한 그 작업에서 그대로 적용됩니다.

> 이 사이트의 페이지는 `rules/`, `skills/`, `agents/`, `hooks/`의 영어 원본에서 생성됩니다. 영어가 정본이고, 한국어는 읽기용 미러예요. 오른쪽 위 메뉴에서 [English](/) 로 전환할 수 있습니다.
