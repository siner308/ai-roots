# English Style

This file replaces `rules/english-style.md` when the rules are installed into Codex.
The rule-based version measurably loses there: across every model tested, blind judging preferred the rewrite-directive approach below for English prose, so Codex gets that instead.
Claude keeps the rule-based version.

Apply this when the deliverable is English prose a person will read or hear — an article, a transcript, a script, a talk, a long-form answer.
It does not apply to code, comments, commit messages, PR bodies, or structured output; those keep their own conventions, and deliberate roughness in them is a defect.

## Six passes

Work through these on the draft; they overlap on purpose.

1. **Break the pattern.** You are an expert at spotting the signals that give away AI-written text. Find them and remove them one by one. Break up the structure, soften anything too rigid, and make every word look chosen in the moment rather than produced by a formula.

2. **Fail the credibility test.** Read as someone who gets suspicious the instant a text looks too polished. Go sentence by sentence and change anything that sounds too worked-over, too correct, too robotic. It has to sound like something a real person would say out loud without weighing every word.

3. **Shape a voice.** Build a voice that belongs to someone. Give the text a clear point of view instead of the tone of a neutral observer trying to please everyone. Let opinions, small contradictions, and natural shifts in tone come through.

4. **Let it be imperfect.** Perfect text has no story. Add the small imperfections only someone who actually lived the subject would write — a blunt opinion here, a hesitation there, an aside, an unfinished sentence where it earns its place. Do not tidy them away afterwards.

5. **Say it aloud.** Read the text aloud in your head. Mark every sentence where you would pause oddly or where the rhythm would break in real conversation, and rewrite those so they flow like speech rather than like a document.

6. **Find what has no soul.** Read as someone who has seen thousands of AI-generated texts. Pick the three or four sentences that sound most artificial and rewrite each one as if you were talking to a close friend.

## The one thing these passes must not do

Passes 3 and 4 buy naturalness with personality, and personality is delivery — never content.
An opinion, hesitation, or anecdote the source does not support is a fabrication, and blind judging caught exactly that: chained rewrites invented a cause for an incident report and put invented private doubt into an announcement.
`grounded-assertions` outranks everything above.

Run the six as one pass. Chaining them as six sequential rewrites measured worse on every axis — longer, less faithful, and past the register the deliverable could carry.
