---
name: web-fetch-block-then-search
description: "agent-browser(lightpanda든 chrome이든)가 차단된/빈/동적 내용을 돌려줘서 다른 엔진으로 재시도하거나 형제 URL을 추측하고 싶어질 때 적용하세요. 살아있는 브라우저는 페이지를 렌더링하느라 모든 안티봇 방어를 물려받지만, 검색 도구는 인덱싱된 스니펫을 읽어 차단을 우회합니다. 브라우저를 더 높이지 말고 WebSearch / Codex --search로 전환하세요."
---

# agent-browser가 차단되면, 엔진을 높이지 말고 검색하라

살아있는 브라우저 fetch(`agent-browser`, lightpanda든 chrome이든)는 실제 페이지를 렌더링하므로, 사이트가 돌리는 모든 안티봇 방어를 그대로 물려받습니다 — Cloudflare 챌린지, 지연 로드 차트, 숫자를 끝내 `body` 텍스트에 넣지 않는 SPA 껍데기. 검색 도구(`WebSearch`, 또는 Codex의 `--search` web_search)는 페이지를 렌더링하지 **않습니다**. 검색 엔진이 이미 인덱싱해 둔 스니펫을 읽습니다. 그래서 검색은 어떤 브라우저 엔진도 못 깨는 차단을 그냥 지나갑니다 — 두 도구는 완전히 다른 이유로 실패하므로, "더 세게" 올라가는 사다리가 아니라 서로 다른 메커니즘입니다.

실수는 이 둘을 사다리로 취급하는 것입니다: lightpanda → chrome → 같은 도메인의 다른 URL → 포기. 그 사다리의 모든 칸은 여전히 *살아있는 렌더링*이라, 모든 칸이 같은 벽에 부딪힙니다.

## 실제로 있었던 일

ARM/RISC-V 분석을 팩트체크하면서 두 숫자를 확인해야 했습니다: ARM의 중국 매출 비중과 RISC-V 2030 칩 출하 전망.

- **실패한 접근(살아있는 렌더링, 반복):** SHD Group과 `riscv.org/exchange`에 `agent-browser --engine lightpanda`를 돌렸더니 빈 body가 옴. chrome으로 바꿔도 — 여전히 빈 body. Google, Bing, DuckDuckGo HTML 검색 페이지를 *agent-browser를 통해* 시도 — 엔진이 결과 JS를 못 돌려서 깨진/인코딩된 쓰레기가 옴. 다른 기사 URL을 추측 — 404. 4번 넘게 시도하고 두 숫자 모두 "리서치 실패"로 기록.
- **성공한 접근(렌더링 안 하는 검색):** 같은 작업을 Codex `--search -a never exec --sandbox read-only`에 넘겼더니 내장 `web_search` 도구를 씀. 로그에 `Arm Holdings annual report 2025 gross margin revenue ... 20-F`, `RISC-V chips forecasted by 2030` 같은 쿼리가 보임. 스니펫이 수치를 그대로 담고 있었음: **ARM 중국 ≈ 매출의 16% (FY2026 20-F)**, **2030년까지 RISC-V 칩 160억 개 초과 전망 (RISC-V International / SHD Group)** — 1차 SEC 공시 URL까지 드러냄.

Codex에 비밀 크롤링 기법이 있었던 게 아닙니다. 브라우저 대신 검색 도구를 썼을 뿐입니다. 같은 우회를 메인 세션도 `WebSearch`로 내내 쓸 수 있었습니다. 프로토콜이 `WebSearch`를 낮게 묻어두고 "agent-browser가 기본"을 강조하는 바람에 "계속 브라우저를 써라"로 오독된 것뿐입니다.

## 규칙

`agent-browser`가 차단 신호를 보이면 — 빈/깨진 body, Cloudflare "Just a moment", 원하는 수치가 `body` 텍스트에 없음, HTTP 4xx/5xx, 타임아웃 3회 연속, 또는 검색 결과 페이지가 쓰레기로 렌더링됨 — **브라우저 엔진을 더 높이지 말고 검색 기반 도구로 전환하세요.** 필요한 정확한 수치를 검색 쿼리에 박으면, 페이지 로드 없이 스니펫이 답하는 경우가 많습니다.

chrome 엔진은 *렌더링은 되지만 무겁고 상호작용이 필요한* 페이지(필터, 로그인, 폼)와, 데이터가 거기밖에 없어 더 힘든 fetch가 정당화되는 **공식 1차 문서**(SEC EDGAR, DART, 규제기관/발행사 IR)에만 아껴 쓰세요. 2차/애그리게이터 데이터라면 다른 검색 쿼리나 다른 애그리게이터가 chrome보다 낫습니다.

## 이 교훈이 적용되는 신호

- 시장조사·금융 애그리게이터·정부 공시·검색 엔진 페이지가 agent-browser에서 빈/차단된 내용을 돌려줌.
- 같은 차단 URL을 다른 브라우저 엔진으로 재시도하거나, 같은 도메인의 형제 URL을 추측하려는 참.
- 필요한 숫자가 "차트 뒤에" 있음 — 시각적으로는 보이지만 추출된 `body` 텍스트에는 없음.

세 경우 모두: 검색으로 전환하세요. 전체 프로토콜은 `web-research` 스킬 §"차단 신호 → 검색 fallback" 참고.
