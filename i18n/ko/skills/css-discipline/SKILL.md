---
name: css-discipline
description: "CSS를 편집·작성·리뷰할 때 적용 — 스타일시트, scoped 스타일, 인라인 style 속성, CSS-in-JS, 또는 프레임워크 스타일링(Tailwind, CSS Modules, Svelte/Vue scoped 스타일) 전반. 닫힌 spacing scale, 박스 모델, 캐스케이드/specificity, overflow, flex/grid shrink, color/z-index 토큰, 단위 규율을 다룬다. 스타일을 건드리지 않는 작업에서는 트리거하지 말 것."
---


# CSS Discipline

캐스케이드와 박스 모델이 예측 가능하도록 CSS를 작성하자. "까다로운" CSS 버그 대부분 — 눈에 안 보이게 두 배로 늘어난 spacing, 깨진 flex shrink, 오버레이 overflow, specificity 싸움 — 은 코드베이스가 흔한 축들을 열어둔 채 방치할 때 생긴다. 그 축들을 닫아라.

이건 CSS가 존재하는 모든 곳에 적용된다: vanilla, React, Next.js, Svelte, Vue, raw HTML. 프레임워크별 바인딩(Tailwind 클래스명, scoped 스타일, CSS Modules)은 프로젝트 supplement에 둔다.

**언제 규범인가.** R1–R9는 스타일시트, scoped 스타일, 인라인 `style=""`, CSS에 인접한 JS를 편집할 때 지켜야 할 작성 제약이다. 스타일을 건드리지 않는 작업에서는 배경 지식으로만 다루고 — 규칙을 어긴다는 이유만으로 손대지 않은 CSS를 리팩터링하지 마라.

## 핵심 축

- **Cascade** — specificity를 지루하게 유지하고 override 제어권을 온전히 보존한다.
- **Box model** — spacing은 단일 메커니즘으로; overflow는 clipping이나 scroll이 의도일 때만 선언한다.
- **Unit discipline** — 모든 값은 한 번 선언된 이름 있는 집합에서 나온다.
- **Style location** — 각 종류의 스타일이 어디에 속하는지 미리 정한다.

## R1 — 닫힌 spacing scale을 써라

작성하는 모든 spacing(padding, gap, positioned offset, 레이아웃 크기의 width/height)은 토큰 또는 utility 레이어에 한 번 선언된 유한한 집합에서 나온다. 새 값은 호출부가 아니라 아래의 예외 절차를 통해 들어온다.

고정 픽셀 chrome 치수(아이콘 크기, 버튼 탭 타깃)는 그 집합 안에 있으면 괜찮다. 집합 밖이면 → 이름 있는 토큰을 먼저 선언하고 `var()`로 소비한다.

*Why.* spacing이 열려 있으면, `gap: 8px`인 부모 옆의 자식에 `margin-top: 8px`가 붙으면 조용히 16px가 되고, 소스 어디에도 그 두 배를 알려주는 신호가 없다.

## R2 — spacing은 padding + gap으로; margin은 정렬용으로만 남겨둬라

형제 간 spacing은 부모(padding)와 컨테이너(gap)에 둔다. margin은 한 가지 일만 한다: 축 방향 auto 센터링(`margin: auto`, `margin-inline: auto`, `margin-block: auto`).

user-agent 기본 margin 리셋은 지정된 base 레이어 한 곳에 모아둔다. 그 외 모든 작성 margin 선언은 피한다. 자식에 `margin-top: 8px`를 주고 싶으면, 대신 부모의 gap을 키워라.

*Why.* padding + gap은 spacing 결정을 컨테이너에 국소화한다. 섞여 들어간 자식 margin은 조용히 두 배가 된다.

## R3 — override 제어권을 지켜라: `!important` 금지

CSS 규칙이 캐스케이드 싸움에서 지면, 캐스케이드에서가 아니라 상류에서 고쳐라.

가장 흔한 원인은 JS가 인라인으로 `element.style.*`를 써서 CSS가 이길 수 없게 만드는 것이다. JS를 리팩터링해서 인스턴스별 값을 `element.style.setProperty('--custom-prop', value)`로 바인딩하라 — 스타일시트가 여전히 캐스케이드를 소유하고, JS는 값만 공급한다. `<canvas>`의 경우 JS는 backing-store 속성(width/height)을 소유하고, CSS는 렌더링되는 박스(`.style.width` / `.style.height`)를 소유한다.

**최후 수단 예외.** 수정도 fork도 할 수 없는 서드파티 스타일: 좁게 한정된 `!important` 하나는 허용된다. 단, 상류 소스를 명시하는 한 줄 주석을 달아 그 소스가 바뀔 때 선언을 폐기할 수 있게 한다.

*Why.* `!important`는 한 번 이기지만 override 제어권을 영구히 내준다 — 이후 모든 레이어도 `!important`가 필요해진다.

## R4 — overflow는 clipping이나 scroll이 의도일 때만 선언하라

CSS 기본값(`visible`)이 대부분의 레이아웃에 맞는다. clipping이 *의도된* 동작일 때 `overflow: clip`을 선언하라(`hidden`보다 선호 — scroll 컨테이너도, 새 stacking context도 안 생긴다). scroll에는 `overflow: auto`를 선언한다.

부모를 넘쳐나는 flex/grid 자식에는 R5(`min-*: 0`)로 가라. hidden-overflow는 레이아웃 버그를 숨기지만, shrink 계약은 그걸 고친다.

*Why.* 까다로운 overflow 버그 대부분은 크기 문제를 덮으려고 반사적으로 `overflow: hidden`을 잡는 데서 온다.

## R5 — flex/grid shrink는 `min-*: 0`으로 풀어줘라

본래 크기 아래로 줄어들어야 하는 flex나 grid 아이템에는 `min-width: 0`(또는 `min-height: 0`)이 필요하다. 브라우저는 flex 아이템에서 이걸 `auto`로 기본 설정해 shrink를 막는다.

본래 치수가 있는 replaced 요소(`<canvas>`, `<img>`, `<video>`, `<iframe>`)는: CSS로 완전히 크기를 정하거나(JS가 인라인으로 세팅한 치수를 제거, R3 참고), aspect-ratio 컨테이너에 `overflow: clip`으로 감싼다. 비율을 유지하며 줄이려면 **한 축만** 설정하고 aspect-ratio가 나머지를 유도하게 둔다.

*Why.* flex 아이템의 `min-width: auto`는 `min-content`와 같다. 인라인 768×512 크기가 붙은 canvas는 그걸 `min-content`로 보고하고, flex-shrink는 그 아래로 못 내려간다.

## R6 — 작성하는 디자인에는 color 토큰을 써라

작성하는 모든 색은 이름 있는 토큰(`var(--color-*)`)을 참조한다. 모듈레이션에는 `color-mix(in oklch, var(--color-a) N%, transparent)`를 써라 — 인자는 토큰으로 두고 퍼센트만 바꾼다.

컴포넌트 소스에서 hex, `rgb()`, `rgba()`, `hsl()`, `oklch()`, 그리고 리터럴 인자를 쓴 `color-mix(...)`는 피한다.

**Non-CSS consumer 예외.** `var()`를 해석할 수 없는 렌더 경로 — canvas 2D, WebGL, 이메일용 서버 렌더링 SVG, PDF export — 는 리터럴 color fallback이 정당하게 필요하다. 어떤 경로가 해당되는지는 프로젝트 supplement가 명시한다.

*Why.* 토큰은 디자인 변경을 한 파일에 국소화한다.

## R7 — 스타일을 그걸 소유하는 레이어에 둬라

세 레이어, 각자 좁은 역할.

- **Utility 레이어** (Tailwind, BEM global, CSS Modules, 직접 만든 atom) — 반복되는 레이아웃, spacing, 타이포그래피, 토큰 기반 color. 반복되는 스타일의 기본 집.
- **Component-scoped 레이어** (Svelte `<style>`, CSS Modules, Vue SFC, scoped styled-components) — pseudo-class, 중첩 셀렉터, `:has()`, SVG 내부, 같은 템플릿 안 여러 요소에 걸치는 것.
- **인라인 `style=""`** — 유효한 용도 두 가지: 인스턴스별 커스텀 프로퍼티(scoped 레이어가 소비하는 `style="--row-accent: ..."`), 또는 단일 요소에 단일 토큰 참조 하나(`style="color: var(--color-text);"`). 그보다 큰 건 아직 안 쓴 컴포넌트다.

**결정 트리.** (1) 기존 utility 클래스? → utility. (2) pseudo-class / 중첩 / 구조적? → scoped. (3) 인스턴스별 값? → 인라인 커스텀 프로퍼티 + scoped 소비자. (4) 일회성 단일 토큰 참조? → 인라인 style. (5) 리터럴이 필요? → 멈추고 토큰을 먼저 추가.

## R8 — 이름 있는 z-index 토큰을 써라

```
--z-base: 0;  --z-overlay: 10;  --z-hud: 20;  --z-modal: 30;
```

`z-index: var(--z-overlay)`로 소비한다. 정말로 새로운 stacking 레이어가 생기면 토큰 파일에 새 레벨을 추가한다. raw 숫자 z-index는 피한다 — 9999는 내일 99999가 된다.

## R9 — 뷰포트와 사용자 font-size에 맞춰 스케일하라

사용자는 변수 둘을 통제한다: 기기(뷰포트)와 타이포그래피 선호. 둘 다 존중하라.

- 타이포그래피와 타입에 묶인 값(font-size, line-height, 타입에 따른 padding/gap)에는 `rem` — 사용자 font-size 선호에 맞춰 스케일된다(WCAG 1.4.4).
- 뷰포트 반응형 레이아웃에는 레이아웃 프리미티브(`%`, `fr`, gap, `clamp()`, media/container 쿼리).
- 리터럴 픽셀이 의도인 chrome 위젯(border, hairline, 아이콘 박스 치수)에는 `px`.
- `vw`/`vh`/`svh`는 가장 바깥 shell에만.

## 예외 절차 — 닫힌 집합에 추가하기

기존 집합 밖의 값이 정말로 필요할 때:

1. 호출부에서 멈춰라. `!important`, bracket utility, 리터럴로 손 뻗지 마라.
2. 집합을 식별한다(spacing, color, motion, z-index).
3. prior-decision 로그를 확인한다 — 이미 다뤄진 필요일 수 있다.
4. 토큰 레이어에 추가한다. 값이 아니라 의도로 이름 짓는다(`--spacing-card-inset`).
5. 토큰 + 첫 소비자를 하나의 atomic commit으로 올린다.

토큰 레이어가 아직 없으면 먼저 선언하라: 기존 리터럴을 조사하고, 의도된 scale로 묶고, 별도 commit으로 올린다. 그때까지 R1–R9는 지향점으로 다룬다.

## 강제 신호 (리뷰 휴리스틱)

조사의 출발점이지 자동 거부가 아니다. 위의 예외(R3 서드파티, R6 non-CSS consumer)는 여전히 정당하다.

- R3 주석 없이 작성 소스 어디든 있는 `!important`.
- 컴포넌트 소스의 color 리터럴(hex, `rgb(`, `rgba(`, `hsl(`, `oklch()`).
- base 리셋 레이어 밖의 방향별 margin 또는 `margin: auto` 계열.
- raw 숫자 z-index.
- JS가 쓰는 `element.style.width` / `.style.height` (`setProperty('--*', value)` 경유 제외).
- 문서화된 예외 없는 utility 프레임워크 arbitrary-value 대괄호(`-\[.*\]`).

프레임워크별 grep(Tailwind 접두사, Svelte 파일 타기팅, `.module.css` 패턴)은 프로젝트 supplement에 둔다.

## 프로젝트 supplement

이 규칙들은 보편적 형태를 기술한다. 각 프로젝트는 구체적 바인딩을 고정한다: 어떤 utility 프레임워크인지, spacing/color/motion 집합, 토큰 레이어 파일, base 리셋 파일, 로컬 grep. 프로젝트 편의가 이 규칙과 충돌하면 프로젝트가 진다 — 프레임워크 편의가 근본 규율을 덮어쓰지 못한다.
