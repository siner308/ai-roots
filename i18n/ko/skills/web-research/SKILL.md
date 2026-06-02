---
name: web-research
description: "웹을 둘러보거나, 페이지 내용을 추출하거나, 데이터를 긁거나, 사이트에서 수치를 가져올 때 적용하세요 — agent-browser(기본 lightpanda, 무겁거나 상호작용이 필요한 페이지는 chrome)와 검색 기반 도구 중에서 고릅니다. 핵심은 차단 신호 → 검색 fallback입니다. 페이지가 봇 차단되거나 완전히 동적이면, 브라우저 엔진을 더 높여가며 재시도하지 말고 WebSearch / Codex --search로 전환하세요."
---

# 웹 리서치 프로토콜

**웹 브라우징의 기본 도구는 WebSearch/WebFetch가 아니라 `agent-browser`입니다.** 사이트를 방문하거나, 데이터를 추출하거나, 페이지와 상호작용하는 작업이면 agent-browser를 먼저 적극적으로 쓰세요. WebSearch가 실패할 때까지 기다리지 마세요.

**하지만 그 반대도 함정입니다.** 페이지가 봇 차단되거나 완전히 동적이면 `agent-browser`는 "더 세게 해본다"고 이길 수 없습니다. 차단 신호가 보이는 순간, 브라우저 엔진을 더 높이지 말고 검색 기반 도구로 전환하세요 — 아래 "차단 신호 → 검색 fallback" 참고. 웹 리서치가 막히는 가장 흔한 경로가 바로 이겁니다.

## 도구 우선순위

| 우선순위 | 도구 | 언제 쓰나 |
|----------|------|-----------|
| 1 (기본) | `agent-browser --engine lightpanda` | 모든 웹 브라우징. Chrome보다 10배 빠르고 메모리 10배 적게 씀. 페이지 내용 추출, 데이터 스크래핑, 기사 읽기, 구조화된 데이터 가져오기에 사용 |
| 2 (fallback) | `agent-browser` (chrome 엔진) | lightpanda가 *렌더링은 되지만 무거운* 페이지에서 실패할 때 — 복잡한 JS 상호작용, 로그인 흐름, 동적 검증이 있는 폼 제출, 스크린샷 |
| 3 (차단 우회) | `WebSearch`, 또는 Codex `--search` 웹 리서치 모드 | **페이지가 봇 차단됐거나, 원하는 데이터가 어느 엔진도 렌더링 못 하는 동적 JS 안에 있을 때.** 검색 인덱스는 페이지를 렌더링하지 않고 스니펫을 돌려주므로 Cloudflare / SPA 벽을 그냥 지나갑니다. 차단 신호가 보이는 순간 이걸 chrome 위로 올리세요(아래 참고). |
| 4 (최후) | `WebFetch` | agent-browser를 못 쓰고 페이지가 정적 HTML일 때만 |

## 차단 신호 → 검색 fallback (핵심 규칙)

`agent-browser`는 (어느 엔진이든) 살아있는 페이지를 렌더링하므로 사이트가 가진 모든 안티봇 방어를 그대로 물려받습니다. 검색은 페이지를 렌더링하지 **않습니다** — 검색 엔진이 이미 인덱싱해 둔 스니펫을 읽을 뿐입니다. 그 차이 때문에 어떤 브라우저 엔진도 못 뚫는 차단을 검색은 우회합니다.

**차단 신호 — 아래 중 하나라도 보이면, 브라우저를 더 높이지 말고 검색으로 전환:**
- `body` 텍스트가 비었거나 깨짐, 또는 "Just a moment…" / Cloudflare 챌린지 문자열
- 원하는 숫자가 `body` 텍스트에 없음 (차트 뒤나 지연 로드 JS 안에 있음)
- HTTP 4xx/5xx, 또는 타임아웃 3회 연속
- 검색 엔진 결과 페이지 자체가 깨진/인코딩된 쓰레기로 옴 (엔진이 결과 JS를 못 돌림)

**하지 마세요:** 차단에 대응한답시고 lightpanda→chrome으로 바꿔 같은 차단 URL을 다시 시도, 같은 차단 도메인의 다른 URL을 추측, 같은 fetch를 3번 이상 반복. 이건 실패를 되풀이할 뿐입니다. 차단은 *살아있는 렌더링*에 걸린 거라, 렌더링하지 않는 경로(검색)만이 우회합니다.

**가장 자주 걸리는 사이트:** 시장조사 회사(SHD Group, Gartner류), 금융 애그리게이터(Yahoo Finance, Bloomberg, MarketBeat, Morningstar), 정부 공시(SEC EDGAR, DART), 그리고 검색 엔진 자체의 결과 페이지(Google/Bing/DuckDuckGo HTML은 lightpanda에서 스니펫이 렌더링 안 되는 경우가 많음).

**가져오기 힘든 숫자에 대한 구체적 에스컬레이션 순서:**
1. 소스 페이지에 `agent-browser --engine lightpanda`.
2. 차단 신호? → 필요한 정확한 수치를 박은 키워드 쿼리로 `WebSearch` (예: `Arm Holdings 20-F China revenue percent 2026`). 스니펫을 읽으세요 — 숫자가 그대로 들어있는 경우가 많습니다.
3. 여전히 없고, 소스가 **공식 1차 문서**(SEC/DART/규제기관/발행사 IR)? → 그 *1차* URL에 chrome 엔진을 쓸 가치가 있음(데이터가 거기밖에 없으므로). 애그리게이터/2차 데이터라면 chrome 대신 다른 검색 쿼리나 다른 애그리게이터를 우선.
4. 교차 검증이 이미 필요한 상황이면, Codex `--search -a never exec --sandbox read-only`가 같은 web_search 도구를 돌리며 1차 공시에서 수치를 끄집어내는 데 탁월함 — 다만 더 무거우니 첫 조회가 아니라 검증 패스에 쓰세요.

이 프로토콜은 뉴스, 공시, 애널리스트 데이터, 시장조사 전망 등 모든 리서치 레인에 적용됩니다. 그 배경 교훈: `web-fetch-block-then-search`.

## Lightpanda 먼저

항상 lightpanda를 먼저 시도하세요. 대부분의 정적·반동적 페이지를 완벽하게 처리합니다:

```bash
# 기본 패턴 — 빠른 내용 추출을 위한 lightpanda
agent-browser --engine lightpanda open <url> && agent-browser --engine lightpanda wait --load networkidle && agent-browser --engine lightpanda get text body

# --engine 플래그 반복을 피하려면 환경변수 설정
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser open <url> && agent-browser wait --load networkidle && agent-browser get text body
```

**chrome 엔진으로 전환할 때**는 페이지가 렌더링은 되지만 무거운 경우입니다 (봇 차단일 때가 아님 — 그건 위의 검색 fallback):
- 여전히 *상호작용*해야 하는 무거운 SPA 때문에 lightpanda가 빈/깨진 내용을 돌려줌
- 폼, 드롭다운, 동적 UI와 상호작용해야 함
- 스크린샷이나 시각적 확인이 필요함
- --extension, --profile, --state, --allow-file-access를 써야 함

## 흔한 패턴

### 데이터 추출 (기사, 리뷰, 문서)
```bash
agent-browser --engine lightpanda open <url>
agent-browser --engine lightpanda wait --load networkidle
agent-browser --engine lightpanda get text body
```

### 상호작용 리서치 (필터링, 페이지네이션, 로그인)
```bash
agent-browser open <url> && agent-browser wait --load networkidle
agent-browser snapshot -i
agent-browser fill @ref "value"
agent-browser click @ref
agent-browser snapshot -i  # 상호작용 후 다시 스냅샷
```

### 대량 데이터 수집 (여러 페이지)
```bash
# 여러 URL을 긁을 때는 속도를 위해 lightpanda 사용
export AGENT_BROWSER_ENGINE=lightpanda
for url in url1 url2 url3; do
  agent-browser open "$url" && agent-browser wait --load networkidle && agent-browser get text body > "output_$i.txt"
done
```

### 가져오기 힘든 숫자 (차단된 애그리게이터, 공시)
```bash
# 1) 페이지 시도; 2) 차단 신호가 뜨면 수치를 쿼리에 박아 검색으로 전환
WebSearch: "<entity> <metric> <unit/year>"   # 스니펫에 숫자가 들어있는 경우가 많음
# 1차 공시(SEC/DART)는 그 1차 URL에 chrome을 쓰는 게 정당한 에스컬레이션
```

### 부동산 리서치 (네이버 부동산, 호갱노노, KB부동산)
이들은 상호작용해야 하는 JS 무거운 SPA입니다 — chrome 엔진 사용:
1. `agent-browser open <url>` (chrome 엔진)
2. snapshot + fill/click으로 필터 적용
3. snapshot으로 데이터 추출
4. 스크롤 후 페이지네이션을 위해 다시 snapshot

## Chrome DevTools MCP

agent-browser가 복잡한 JS 무거운 페이지에서 문제를 겪을 때, 또는 고급 디버깅(네트워크 검사, 성능 프로파일링)에 보조 옵션으로 사용하세요.
