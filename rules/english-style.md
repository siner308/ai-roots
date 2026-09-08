# English Style

Makes English output read as if a person wrote it; the English extension of `prose-style`, which carries the read-it-back-as-speech test and the cross-language rules on characters, words, and line breaks, and both apply when writing English.

## Rules

- Prefer the plainer word to the stock one, verbs to `-tion` nominalizations, and a number to a scale adjective.
- Watch the frame tells: connective padding, throat-clearing, self-answered questions, `not just X, it's Y`, tidy closers, labeled summary lines. One is fine, repetition is the tell.
- Interrupt a sentence at most once, whatever punctuation does the interrupting, and vary sentence length deliberately. The em dash glyph itself is barred by the character table in `prose-style`.
- For spoken deliverables, contract, open the way speech opens, and drop subordinate scaffolding, while keeping every claim to what the source supports.

## Word choice

- **Stock lexicon**: `delve`, `leverage`, `utilize`, `foster`, `robust`, `seamless`, `landscape`, `realm`, `testament`, `navigate` (figurative), `underscore`, `pivotal`, `myriad`, `unprecedented`, `game-changer`, and the intensifiers `genuinely` and `importantly`. ❌ `leverage the existing index` ✅ `use the index we already have`.
- **Rate tells**: the ten words that together identify LLM writing best are `across`, `additionally`, `comprehensive`, `crucial`, `enhancing`, `exhibited`, `insights`, `notably`, `particularly`, `within`. Most are ordinary words, so this is a rate tell and not a ban list: notice when a paragraph has collected three or four. The study behind it ([Science Advances](https://www.science.org/doi/10.1126/sciadv.adt3813)) found 280 style words jumped in 2024 across 15 million biomedical abstracts, two thirds of them verbs; `delves` ran 25x its pre-LLM rate, `showcasing` and `underscores` 9x, and by frequency gap `potential`, `findings`, and `crucial` moved most.
- **Nominalizations**: ❌ `the implementation of caching led to a reduction in latency` ✅ `caching made it faster`.
- **Scale adjectives with no scale**: `significant`, `substantial`, `considerable`, `massive` where a number belongs. ❌ `a significant improvement` ✅ `about 40% faster`.
- **Hedge stacking**: ❌ `this could potentially seem to indicate` ✅ `this probably means`, or drop the hedge if you actually know.

## Framing, the strongest tell

- **Interruption cadence**: ❌ `The greenhouse (rebuilt last spring) now vents automatically, no one touches it.` ✅ `The greenhouse was rebuilt last spring. It vents automatically now, so nobody touches it.`
- **The reveal frame**: `not just X, it's Y` / `not only X but also Y`. ❌ `This isn't just a new catalogue, it's a rethink of how the library lends.` ✅ `The library rethought how it lends.`
- **Connective padding**: `Moreover`, `Furthermore`, `Additionally`, `That said`, `Ultimately` opening sentences that need no connective. Cut them and check whether anything broke.
- **Throat-clearing**: ❌ `It's worth noting that the rule only applies to overnight loans.` ✅ `The rule only applies to overnight loans.`
- **Colon dumps**: ❌ `Three factors: cost, latency, and trust.` ✅ `It comes down to cost, latency, and trust.`
- **The self-answered question**: ❌ `So what changed? The vents now close at 26°C.` ✅ `The vents now close at 26°C.`
- **The tidy closer**: `In conclusion`, `Time will tell`, `One thing is clear`, and a labeled summary line (`Bottom line:`, `In short:`, `The takeaway:`) that repeats the paragraph above it. End on the last real thing you have to say.

## Rhythm

- **Monotone sentence length**: let a short sentence land after a long one.
- **Three-beat lists everywhere**: `A, B, and C` repeated paragraph after paragraph. Sometimes two items, sometimes a clause.
- **Paragraph symmetry**: every paragraph the same shape (claim, elaboration, implication). Let one be a single sentence.

## Spoken register

When the deliverable is spoken (a transcript, a script, a talk), the target is sayable, not written-correct.

- Contract everything a speaker would contract: `it's`, `they're`, `that's`, `we've`.
- Start sentences the way speech does: `And`, `But`, `So`, `Look` are fine out loud.
- Cut the subordinate scaffolding: ❌ `While the details remain unclear, what is apparent is that...` ✅ `We don't know the details yet. What we do know is...`
- Say numbers the way a speaker would read them: ❌ `1,240 m²` ✅ `about twelve hundred square metres`.
- Keep one voice; a transcript sliding between anchor formality and podcast banter reads as stitched together.
- An opinion, a hesitation, or an anecdote the source does not support is a fidelity failure, and `grounded-assertions` outranks the naturalness goal at this boundary.

`korean-style` carries a personal voice profile and this rule does not: English output keeps only the language-neutral instincts, and the spoken-register section is driven by the deliverable.
