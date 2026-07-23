# Terminology Discipline

도메인 용어는 풀어써라. 작성자에게 뻔해 보이는 약어가 읽는 사람에게는 모호하고, 다른 도메인 용어와 충돌하면서 의미가 슬그머니 뒤집히기도 한다.

## 세 가지 범주

| Category | Treatment | Examples |
|----------|-----------|----------|
| **Industry-standard abbreviations** | 그대로 쓴다 | `env`, `prod`, `dev`, `repo`, `svc`, `db`, `api`, `url`, `id`, `auth`, `config`, `ctx`, `req`, `res` |
| **Established domain terms** | 약어는 유지하되 첫 등장 시 풀어쓴다 | 코드베이스나 팀 어휘에 이미 자리 잡은 프로젝트 고유 약어 |
| **Ad-hoc abbreviations** | 전부 풀어쓴다 | `usrCnt` → `userCount`, `prodInfo` → `productInfo`, `memInfo` → `memberInfo` |

약어가 industry-standard로 인정받으려면 외부 자료 — 공식 문서, 언어 명세, 널리 쓰이는 라이브러리 — 에서 같은 형태로 나타나야 한다. 사내 줄임말은 industry standard가 아니라 도메인 용어다.

## 충돌 신호

약어가 다른 도메인 개념으로 잘못 읽힐 수 있으면, 풀어쓰거나 한정어를 붙여라.

- `uid` — user id인가 unique id인가?
- `pid` — process id, player id, product id 중 무엇인가?
- `mid` — member id, message id, middleware id, 아니면 또 다른 무엇인가?

약어에 그럴듯한 해석이 둘 이상 있으면, 풀어쓰거나(`userId`, `processId`, `messageId`) 모호함을 없애는 한정어를 붙여라.

## 적용 범위

- **New identifiers** — 변수·함수·타입은 기본적으로 풀어쓴 이름을 쓴다. industry-standard 약어는 허용한다.
- **User-facing explanations** — 정착된 도메인 용어를 처음 언급할 때 풀어쓴다("X (이 도메인에서 무슨 뜻인지)"), 그 뒤로는 짧은 형태로 써도 된다.
- **Documentation and comments** — 충돌 가능한 약어는 한정어로 구분한다.
- **Editing existing code** — 정착된 약어는 있는 그대로 둔다. 풀어쓰려고 대량 rename하는 것보다 코드베이스 일관성이 우선이다.

## 규칙

- 새 identifier는 기본적으로 풀어쓴 형태로. industry-standard거나 도메인에 이미 정착된 용어일 때만 약어를 쓴다.
- 정착된 도메인 약어: 첫 등장 시 풀어쓰고, 그 뒤로는 짧은 형태로 써도 된다.
- 충돌 가능한 약어: 한정어를 붙이거나 풀어써서 모호함을 없앤다.
- 기존 코드베이스 컨벤션을 보존하라 — 정착된 약어를 어중간하게 일부만 풀어쓰지 마라.