# English Style

영어 출력이 사람이 쓴 글로 읽히게 하는 `prose-style`의 영어 확장이다. 소리 내어 읽어보는 기준과 문자, 낱말, 줄 끊기에 관한 언어 공통 규칙은 그 규칙이 갖고 있고, 영어를 쓸 때 둘 다 적용한다.

## 규칙

- 닳아버린 단어보다 평이한 단어, `-tion` 명사화보다 동사, 정도 형용사보다 숫자를 쓴다.
- 틀 표시를 살핀다: 접속어 채우기, 목 가다듬기, 스스로 묻고 답하기, `not just X, it's Y`, 깔끔한 마무리, 라벨 붙은 요약 줄. 하나는 괜찮고 반복이 티다.
- 한 문장을 끊는 건 어떤 부호로든 한 번까지, 문장 길이는 의도적으로 흔든다. em dash 글리프 자체는 `prose-style`의 문자 표가 막는다.
- 말로 나갈 산출물에서는 축약하고, 말이 여는 방식으로 열고, 종속절 받침대를 걷어내되, 모든 주장은 원 자료가 받치는 범위에 둔다.

## 낱말 선택

- **닳아버린 어휘**: `delve`, `leverage`, `utilize`, `foster`, `robust`, `seamless`, `landscape`, `realm`, `testament`, `navigate`(비유적), `underscore`, `pivotal`, `myriad`, `unprecedented`, `game-changer`, 그리고 강조어 `genuinely`와 `importantly`. ❌ `leverage the existing index` ✅ `use the index we already have`.
- **빈도 표시**: 함께 나타날 때 LLM이 쓴 글을 가장 잘 골라내는 열 개는 `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`이다. 대부분 평범한 단어라서 금지 목록이 아니라 빈도 신호다. 한 문단에 셋넷이 모였는지를 본다. 근거가 된 연구([Science Advances](https://www.science.org/doi/10.1126/sciadv.adt3813))는 생의학 논문 초록 1500만 편에서 2024년에 style word 280개가 튀어올랐고 그중 3분의 2가 동사였음을 확인했다. `delves`는 LLM 이전 대비 25배, `showcasing`과 `underscores`는 9배였고, 빈도 격차로는 `potential`, `findings`, `crucial`이 가장 많이 움직였다.
- **명사화**: ❌ `the implementation of caching led to a reduction in latency` ✅ `caching made it faster`.
- **정도 없는 정도 형용사**: 숫자가 들어갈 자리의 `significant`, `substantial`, `considerable`, `massive`. ❌ `a significant improvement` ✅ `about 40% faster`.
- **hedge 쌓기**: ❌ `this could potentially seem to indicate` ✅ `this probably means`, 아니면 실제로 안다면 hedge를 뺀다.

## 틀 짓기, 가장 강한 표시

- **끼어드는 cadence**: ❌ `The greenhouse (rebuilt last spring) now vents automatically, no one touches it.` ✅ `The greenhouse was rebuilt last spring. It vents automatically now, so nobody touches it.`
- **반전 틀**: `not just X, it's Y` / `not only X but also Y`. ❌ `This isn't just a new catalogue, it's a rethink of how the library lends.` ✅ `The library rethought how it lends.`
- **접속어 채우기**: 접속어가 필요 없는 자리를 여는 `Moreover`, `Furthermore`, `Additionally`, `That said`, `Ultimately`. 지우고 뭐가 깨지는지 본다.
- **목 가다듬기**: ❌ `It's worth noting that the rule only applies to overnight loans.` ✅ `The rule only applies to overnight loans.`
- **콜론 쏟기**: ❌ `Three factors: cost, latency, and trust.` ✅ `It comes down to cost, latency, and trust.`
- **스스로 묻고 답하기**: ❌ `So what changed? The vents now close at 26°C.` ✅ `The vents now close at 26°C.`
- **깔끔한 마무리**: `In conclusion`, `Time will tell`, `One thing is clear`, 그리고 위 문단을 되풀이하는 라벨 요약 줄(`Bottom line:`, `In short:`, `The takeaway:`). 실제로 할 말이 남은 마지막 지점에서 끝낸다.

## 리듬

- **단조로운 문장 길이**: 긴 문장 뒤에 짧은 문장을 놓는다.
- **어디서나 세 박자 나열**: 문단마다 되풀이되는 `A, B, and C`. 두 항목일 때도 한 절일 때도 있게.
- **문단 대칭**: 모든 문단이 같은 모양(주장, 부연, 함의). 하나는 한 문장으로 둔다.

## 구어 어투

산출물이 말로 나갈 때(전사, 대본, 발표) 목표는 문어적으로 맞는 문장이 아니라 말할 수 있는 문장이다.

- 말하는 사람이 축약할 건 다 축약한다: `it's`, `they're`, `that's`, `we've`.
- 말이 여는 방식으로 연다: `And`, `But`, `So`, `Look`은 입으로 하면 괜찮다.
- 종속절 받침대를 걷어낸다: ❌ `While the details remain unclear, what is apparent is that...` ✅ `We don't know the details yet. What we do know is...`
- 숫자는 말하는 사람이 읽을 방식으로: ❌ `1,240 m²` ✅ `about twelve hundred square metres`.
- 목소리를 하나로 유지한다. 앵커의 격식과 podcast 잡담을 오가는 전사는 이어 붙인 티가 난다.
- 원 자료가 받치지 않는 의견이나 망설임, 일화를 더하는 건 충실성의 실패이고, 이 경계에서는 `grounded-assertions`가 자연스러움 목표보다 우선한다.

`korean-style`에는 개인 목소리 프로파일이 있고 이 규칙에는 없다. 영어 출력은 언어 중립적 본능만 가져가고, 구어 어투 절은 산출물이 무엇인지가 결정한다.
