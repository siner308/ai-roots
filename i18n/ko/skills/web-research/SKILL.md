---
name: web-research
description: "웹을 둘러보거나, 페이지 내용을 추출하거나, 데이터를 긁거나, 사이트에서 수치를 가져올 때 적용하세요 — agent-browser(기본 lightpanda, 무겁거나 상호작용이 필요한 페이지는 chrome), 발견용 WebSearch, 차단 본문 회수용 insane-search 스킬 중에서 고릅니다. agent-browser가 차단/빈/동적 콘텐츠를 돌려줘서 다른 엔진으로 재시도하거나 형제 URL을 추측하고 싶어지는 순간에도 적용 — 브라우저 에스컬레이션을 멈추고 검색 기반 도구로 전환하세요. Codex --search는 교차검증 전용 GPT 의존 최후 수단입니다."
---

# 웹 리서치 프로토콜

**웹 브라우징의 기본 도구는 WebSearch/WebFetch가 아니라 `agent-browser`입니다.** 사이트를 방문하거나, 데이터를 추출하거나, 페이지와 상호작용하는 작업이면 agent-browser를 먼저 적극적으로 쓰세요. WebSearch가 실패할 때까지 기다리지 마세요.

**하지만 그 반대도 함정입니다.** 페이지가 봇 차단되거나 완전히 동적이면 `agent-browser`는 "더 세게 해본다"고 이길 수 없습니다. 차단 신호가 보이는 순간, 브라우저 엔진을 더 높이지 말고 검색 기반 도구로 전환하세요 — 아래 "차단 신호 → 검색 fallback" 참고. 웹 리서치가 막히는 가장 흔한 경로가 바로 이겁니다.

## 도구 우선순위

| 우선순위 | 도구 | 언제 쓰나 |
|----------|------|-----------|
| 1 (기본 렌더) | `agent-browser --engine lightpanda` | 모든 웹 브라우징. Chrome보다 10배 빠르고 메모리 10배 적게 씀. 페이지 내용 추출, 데이터 스크래핑, 기사 읽기, 구조화된 데이터 가져오기에 사용 |
| 2 (무거운 렌더) | `agent-browser` (chrome 엔진) | lightpanda가 *렌더링은 되지만 무겁고 차단은 아닌* 페이지에서 실패할 때 — 복잡한 JS 상호작용, 로그인 흐름, 동적 검증이 있는 폼 제출, 스크린샷 |
| 3 (발견) | `WebSearch` | **키워드 → URL 또는 사실.** 렌더링 없이 인덱스를 읽으므로 Cloudflare / SPA 벽도 지나갑니다. 흔히 1단계 — 아래 회수 레인에 URL을 먹이는 게 이겁니다. 내리면 안 됨. |
| 4 (차단 본문 회수) | **insane-search** 스킬 (`python3 -m engine <url>`) | **차단된 known-URL의 실제 내용이 필요할 때 — 스니펫 말고.** 자동 Phase 0→3 (공식 API → curl_cffi TLS 위장 → 내부 JSON API → 실제 브라우저), 외부 LLM 불필요. 차단 신호가 보이는 순간 chrome 위로 올리세요(아래 참고). |
| 5 (최후 — 검증) | Codex `--search` | 어려운 1차 문서에 대한 교차검증·수치추출. 유일한 GPT 의존 레인 — 첫 조회가 아니라 검증용으로 마지막에. |
| 6 (최후 — 정적) | `WebFetch` | agent-browser를 못 쓰고 페이지가 정적 HTML일 때만 |

## 차단 신호 → 검색 fallback (핵심 규칙)

`agent-browser`는 (어느 엔진이든) 살아있는 페이지를 렌더링하므로 사이트가 가진 모든 안티봇 방어를 그대로 물려받습니다. 검색은 페이지를 렌더링하지 **않습니다** — 검색 엔진이 이미 인덱싱해 둔 스니펫을 읽을 뿐입니다. 두 도구는 완전히 다른 이유로 실패하므로 **"더 세게" 사다리가 아니라 서로 다른 메커니즘**입니다. 그 차이 때문에 어떤 브라우저 엔진도 못 뚫는 차단을 검색은 우회합니다.

**차단 신호 — 아래 중 하나라도 보이면, 브라우저를 더 높이지 말고 검색으로 전환:**
- `body` 텍스트가 비었거나 깨짐, 또는 "Just a moment…" / Cloudflare 챌린지 문자열
- 원하는 숫자가 `body` 텍스트에 없음 (차트 뒤나 지연 로드 JS 안에 있음)
- HTTP 4xx/5xx, 또는 타임아웃 3회 연속
- 검색 엔진 결과 페이지 자체가 깨진/인코딩된 쓰레기로 옴 (엔진이 결과 JS를 못 돌림)

**하지 마세요:** 차단에 대응한답시고 lightpanda→chrome으로 바꿔 같은 차단 URL을 다시 시도, 같은 차단 도메인의 다른 URL을 추측, 같은 fetch를 3번 이상 반복. 이건 실패를 되풀이할 뿐입니다. 차단은 *살아있는 렌더링*에 걸린 거라, 렌더링하지 않는 경로(검색)만이 우회합니다.

**가장 자주 걸리는 사이트:** 시장조사 회사, 금융 애그리게이터(Yahoo Finance, Bloomberg, MarketBeat, Morningstar), 정부 공시(SEC EDGAR, DART), 그리고 검색 엔진 자체의 결과 페이지(Google/Bing/DuckDuckGo HTML은 lightpanda에서 스니펫이 렌더링 안 되는 경우가 많음).

**가져오기 힘든 숫자에 대한 구체적 에스컬레이션 순서:**
1. 소스 페이지에 `agent-browser --engine lightpanda`.
2. 차단 신호 + 값만 필요 → 필요한 정확한 수치를 박은 키워드 쿼리로 `WebSearch` (예: `<회사> annual report <부문> revenue percent <연도>`). 스니펫을 읽으세요 — 숫자가 그대로 들어있는 경우가 많습니다.
3. 차단 신호 + 페이지 원문 전체가 필요 → **insane-search** 스킬 (차단 신호에 자동 트리거; `python3 -m engine "<url>"`). 브라우저보다 먼저 공식 API·TLS 위장·사이트 내부 JSON API를 시도합니다 — 스니펫이 아니라 실제 내용을 가져오는 무렌더링 경로.
4. 여전히 없고, 소스가 **공식 1차 문서**(SEC/DART/규제기관/발행사 IR)? → 그 *1차* URL에 chrome 엔진을 쓸 가치가 있음(데이터가 거기밖에 없으므로). 애그리게이터/2차 데이터라면 chrome 대신 다른 검색 쿼리나 다른 애그리게이터를 우선.
5. 최후, 교차 검증이 필요한 상황에서만: Codex `--search -a never exec --sandbox read-only`가 같은 web_search 도구를 돌리며 1차 공시에서 수치를 끄집어냄 — 다만 더 무겁고 유일한 GPT 의존 레인이니 첫 조회가 아니라 검증용으로.

이 프로토콜은 뉴스, 공시, 애널리스트 데이터, 시장조사 전망 등 모든 리서치 레인에 적용됩니다.

### 규칙 뒤의 교훈

이 fallback은 비싸게 배운 것입니다. 어떤 분석을 팩트체크하면서 어려운 수치 둘(한 회사의 연차 공시에 있는 지역별 매출 비중, 그리고 업계 단체의 출하량 전망)을 확인해야 했습니다:

- **실패한 접근 (살아있는 렌더링의 반복):** 소스 페이지에 lightpanda — 빈 body. chrome으로 전환 — 여전히 빈 body. Google/Bing/DuckDuckGo 결과 페이지를 *agent-browser로* 가져오기 — 깨진 쓰레기(엔진이 결과 JS를 못 돌림). 다른 기사 URL 추측 — 404. 네 번 넘게 시도하고 두 숫자 모두 "리서치 실패"로 기록. 모든 단이 여전히 *살아있는 렌더링*이었으므로, 모든 단이 같은 벽에 부딪혔습니다.
- **성공한 접근 (무렌더링 검색):** 같은 과제를 검색 도구로 돌리자, 필요한 수치를 쿼리에 박고 인덱싱된 스니펫에서 그대로 읽어냈습니다 — 심지어 1차 공시 URL까지 찾아줬습니다.

비밀스러운 크롤링 기법은 없었습니다. 브라우저 대신 검색 도구를 쓴 것뿐입니다. 같은 우회로가 처음부터 열려 있었는데, 프로토콜이 `WebSearch`를 낮게 묻어두고 "agent-browser가 기본"만 강조한 탓에 "브라우저를 계속 써라"로 잘못 읽혔던 것입니다.

## 차단됐는데 원문 전체가 필요할 때 — insane-search에 위임

검색은 차단을 우회하지만 *인덱싱된 스니펫*만 돌려줍니다. 차단된 사이트의 **실제 페이지 내용**이 필요할 때 — Reddit 스레드 전체, X 타임라인, 상품 페이지 — 살아있는 렌더링을 하지 마세요(브라우저는 차단을 그대로 물려받습니다). Codex `--search`도 아닙니다(그게 GPT 레인이고, 그것도 스니펫만 돌려줍니다). 마켓플레이스 플러그인으로 따로 설치된 **insane-search** 스킬에 URL을 넘기세요. 외부 LLM 없이 차단 본문을 회수하며, 차단 신호(403/402/WAF, X/Reddit/YouTube/네이버/쿠팡/링크드인 등)에 자동 트리거됩니다 — 안 떴으면 직접 호출하세요.

엔트리포인트는 `python3 -m engine "<url>"`이고, Phase 0→3 에스컬레이션을 돌립니다: 공식 비인증 API 먼저(Reddit `.rss`, X syndication, HN, `yt-dlp`, arXiv …), 그다음 WAF-제품별 TLS 위장 격자(`curl_cffi`), 그다음 내부 JSON API 탐지, 마지막에 실제 브라우저 — HTTP 200을 성공으로 믿지 않고 챌린지 마커로 검증합니다. 에이전트 쪽은 자체 SKILL.md(규칙 R1~R7)가 운전하니 맡기세요. 공개 콘텐츠만 접근합니다 — auth 벽과 페이월에서 멈춥니다.

**insane-search가 설치 안 됐다면** 같은 아이디어를 손으로, 순서대로:
- **공식 공개 API**(비인증, WAF 챌린지 안 걸림): Reddit `https://www.reddit.com/r/<sub>/.rss`(`.json`은 차단), X `cdn.syndication.twimg.com/tweet-result?id=<id>&token=a`, HN `hacker-news.firebaseio.com/v0/...`, 미디어는 `yt-dlp --dump-json <url>`, 그 외 arXiv / Wikipedia REST / GitHub `gh` / Bluesky / Mastodon / Stack Overflow 공개 API.
- **TLS 위장**: `python3 -c "import curl_cffi" 2>/dev/null || pip install -q "curl_cffi>=0.15.0"` 후 `r.get('<url>', impersonate='safari')`. 챌린지에 걸리면 `chrome`/`safari_ios`/`firefox`로 지문을 바꾸고 `m.` 모바일 서브도메인을 시도 — 같은 신원을 더 세게가 아니라, 다른 신원으로.
- **내부 API**: `agent-browser`(chrome)로 한 번 열어 `/api`·`/graphql`·`.json` 호출을 찾고 그 엔드포인트를 직접 가져오기.
- **200 ≠ 성공**: ~3KB 미만이거나 `Just a moment…`·`Access Denied`·`DataDome`·`Attention Required`를 담은 본문은 거부 — 200은 검증을 *시작*하는 지점이지 멈추는 지점이 아닙니다.

> insane-search는 MIT 라이선스입니다 ([`fivetaku/insane-search`](https://github.com/fivetaku/insane-search)). 위의 수동 fallback은 플러그인이 없을 때를 위해 같은 접근을 추린 것입니다.

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
