# English Style

This rule makes English output read as if a person wrote it, not as if a model assembled it.
It is the English-specific counterpart of `korean-style`, and the same extension of `prose-style`: that rule governs rhythm and line breaks in any language, this one names the tells that mark English as machine-made.

## The test comes first

There is one test, and it is judgment, not pattern-matching: read the sentence back as speech, and ask whether a person would actually say it that way.
If it sounds assembled — padded, hedged, reaching for a bigger word than the thought needs — rewrite it as something you'd say out loud.

Everything below just trains your ear for that test.
The patterns are smells to recognize, never a token list to grep: you can trip none of them and still sound machine-made, and you can use any one of them naturally — so fix a flagged sentence by re-saying the whole thing, not by swapping the token.
Some tells are damning on a single appearance (a "not just X, it's Y" reveal); most are about frequency (one `moreover` is fine, three in a page is the tell).

## Word choice

- **Stock lexicon.** A small set of words has been worn smooth by machine prose: `delve`, `leverage`, `utilize`, `robust`, `seamless`, `landscape`, `realm`, `testament`, `navigate` (figurative), `underscore`, `pivotal`, `myriad`, `unprecedented`, `game-changer`. ❌ `leverage the existing index` → ✅ `use the index we already have`.
- **Nominalizations.** `-tion`/`-ment`/`-ity` chains where a verb would do the work. ❌ `the implementation of caching led to a reduction in latency` → ✅ `caching made it faster`.
- **Scale adjectives with no scale.** `significant`, `substantial`, `considerable`, `massive` used where a number belongs. ❌ `a significant improvement` → ✅ `about 40% faster`.
- **Hedge stacking.** ❌ `this could potentially seem to indicate` → ✅ `this probably means` — or drop the hedge if you actually know.

## Punctuation and framing — the strongest tells

Word choice gives a sentence away one word at a time; these give away the whole paragraph, and they survive a synonym pass untouched.

- **Em-dash pileups.** More than one em dash per paragraph reads as machine cadence. ❌ `The greenhouse — rebuilt last spring — now vents automatically — no one touches it.` → ✅ `The greenhouse was rebuilt last spring. It vents automatically now, so nobody touches it.`
- **The reveal frame.** `not just X, it's Y` / `isn't just X — it's Y` / `not only X but also Y`. It promises a twist and delivers a synonym. ❌ `This isn't just a new catalogue, it's a rethink of how the library lends.` → ✅ `The library rethought how it lends.`
- **Connective padding.** `Moreover`, `Furthermore`, `Additionally`, `That said`, `Ultimately` opening sentences that need no connective. Cut them and check whether anything broke; usually nothing does.
- **Throat-clearing.** `It's important to note that`, `It's worth mentioning`, `Here's the thing`, `The big question is`. ❌ `It's worth noting that the rule only applies to overnight loans.` → ✅ `The rule only applies to overnight loans.`
- **Colon dumps.** ❌ `Three factors: cost, latency, and trust.` → ✅ `It comes down to cost, latency, and trust.`

## Rhythm and structure

- **Monotone sentence length.** Machine prose writes sentences of near-identical length. Vary them; let a short one land after a long one.
- **Three-beat lists everywhere.** `A, B, and C` repeated paragraph after paragraph. Break the pattern — sometimes two items, sometimes a clause.
- **Paragraph symmetry.** Every paragraph the same shape (claim, elaboration, implication) is a tell. Let one be a single sentence.
- **The tidy closer.** `In conclusion`, `Time will tell`, `One thing is clear`, `The future of X remains to be seen`. End on the last real thing you have to say.

## Spoken register

When the deliverable is spoken — a transcript, a script, a talk — the bar moves. Written-correct is not the target; sayable is.

- **Contract everything a speaker would contract.** `it's`, `they're`, `that's`, `we've`.
- **Start sentences the way speech does.** `And`, `But`, `So`, `Look` are fine openers out loud.
- **Cut the subordinate scaffolding.** ❌ `While the details remain unclear, what is apparent is that...` → ✅ `We don't know the details yet. What we do know is...`
- **Say numbers the way you'd read them.** ❌ `1,240 m²` → ✅ `about twelve hundred square metres` where a speaker would say it.
- **Keep one voice.** A transcript that slides between anchor formality and podcast banter reads as stitched together.

Spoken register does not license invention. Adding an opinion, a hesitation, or an anecdote the source does not support is a fidelity failure, not a naturalness win — the sentence has to become sayable, not become someone else's. This is where "make it sound human" advice most often goes wrong: personality gets added as content rather than as delivery, and the claim that comes out the other side is one the source never made.

## Relationship to other rules

- `prose-style` carries the cross-language half — plain language, noun-stacks, line breaks. When writing English, apply both.
- `korean-style` is the same rule for Korean, and it alone carries the user's personal voice profile (first-person retrospective, motivation-first). This rule deliberately has no equivalent: English output keeps only the language-neutral instincts, and the spoken-register section above is driven by the deliverable, not by a personal voice.
- `grounded-assertions` outranks the naturalness goal, and governs the boundary the spoken-register section names.

## Rules

- The test is judgment by ear (read it back as speech), not token-matching; the patterns are smells, not a grep list. Re-say the whole sentence rather than swapping the flagged word.
- Prefer the plainer word to the stock one, verbs to `-tion` nominalizations, and a number to a scale adjective.
- Watch the frame tells: `not just X, it's Y`, connective padding, throat-clearing, tidy closers. One is fine, repetition is the tell.
- Hold em dashes to at most one per paragraph, and vary sentence length deliberately.
- For spoken deliverables, contract, open the way speech opens, and drop subordinate scaffolding — and keep every claim to what the source supports.
- This rule composes with `prose-style` (rhythm, line breaks); when writing English, both apply.
