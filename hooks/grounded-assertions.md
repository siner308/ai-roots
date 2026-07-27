# Grounded Assertions Hook

A `Stop` hook that runs when a turn is about to end.
When the final response is substantial enough to carry factual claims, it blocks and asks for a claim-by-claim audit: every material assertion must either point to evidence gathered this session, get verified with a tool right now, or get its uncertainty marker restored. A second round then checks that whatever the audit turned up was actually applied, not merely described.

## Why it exists

The `grounded-assertions` rule already says all of this, but the failure it targets — a "probably X" in reasoning becoming "X" in the output — happens at write time, and a resident rule competes with the whole context and loses.
A Stop hook is the only layer that runs after the response exists.

The design follows what the self-correction literature actually supports.
A generic "are you sure?" re-ask makes models flip correct answers too ([FlipFlop experiment](https://arxiv.org/abs/2311.08596)), and intrinsic self-correction without external grounding tends to degrade answers ([Huang et al., ICLR'24](https://arxiv.org/abs/2310.01798)).
What does work is decomposing the output into individual claims and checking each against something firmer than the model's own confidence ([Chain-of-Verification](https://arxiv.org/abs/2309.11495)) — and self-correction succeeds precisely when reliable external feedback exists ([Kamoi et al., TACL 2024](https://arxiv.org/abs/2406.01297)).
Here the session transcript and tool outputs are that external feedback: the audit asks for claim-by-evidence matching, not doubt.

## What it does

On `Stop` it reads the turn's final assistant message from the transcript and, past a sentence-count gate (`SENTENCE_GATE`, default 8, adjustable via `/fact-check <number>`), blocks once with an audit instruction that sorts every material claim into three buckets:

1. **Evidenced** (a file read, command output, the user's own words) — left exactly as written. The instruction explicitly forbids adding hedges to evidenced claims, which is the FlipFlop defense.
2. **Verifiable now** — verified with a tool before the turn ends, and corrected to match.
3. **Neither** — its uncertainty marker is restored ("appears to"; in Korean, "~로 보입니다").

Sorting a claim is only half of it: when the check shows the *work* is wrong — the code, the file, the command, the plan, not the sentence describing it — the audit has to fix the work in that turn, or ask the single question the fix turns on. Without that clause the audit satisfies itself by describing broken work accurately, which is the failure this hook was extended to close.

A second round enforces exactly that. Past the first block the hook stops consulting the sentence gate — an audit reply is short by construction, so the gate would silence the follow-up every time — and asks two things about the round just written: is anything it named as wrong still unapplied, and do the claims *it* introduced survive the same three-way sort. A per-turn counter caps the loop (`MAX_ROUNDS`, default 2, raise it with `AI_ROOTS_FACT_CHECK_ROUNDS`), and the instruction says to change what is wrong and leave the rest, so a round cannot regenerate the response wholesale.

The counter lives in `~/.claude/.ai-roots/fact-check-rounds`, keyed by session id plus the uuid of the user message that opened the turn — hook feedback lands in the transcript as an `isMeta` user entry, so it never counts as a new turn and never resets the count. A turn whose count cannot be read while `stop_hook_active` is set bails out instead of blocking, which pins the worst case at the old one-round behavior rather than a loop.

## What it skips

- Turns whose final message is under the sentence gate — short conversational answers never trigger it. The gate decides the first round only; once a turn is under audit the follow-up round is not length-gated.
- Fenced code blocks, which do not count toward the gate.
- Sidechain (subagent) transcript entries.
- Anything when `/fact-check off` was run (state in `~/.claude/.ai-roots/fact-check`, read live each turn) or `AI_ROOTS_FACT_CHECK=0` is set — with no configuration the hook is on and the gate does the tuning.
- Any transcript it cannot read or parse — the hook fails open, never trapping a session.

## Known limitations (reviewed, accepted)

The gate is a volume heuristic, not a claim detector: a long response with zero factual claims still gets audited, and a short response full of confident guesses slips under it. An audited turn costs two short rounds now, since the follow-up fires whether or not the audit found anything.

The audit closes by answering the user's question again rather than reporting on itself. Its reply lands at the bottom of the screen, below the response it audited, so a bare "nothing to fix" would leave the actual answer scrolled out of view — and saying nothing at all would leave the block message as the last thing visible, which reads as a failed turn.
The follow-up round re-audits the audit, but nothing re-audits the follow-up — a claim introduced there still escapes. The ceiling moved out one round; it did not go away.
Same-context audit means the generator reviews itself; the claim-by-evidence structure narrows but does not eliminate that bias (heavier cross-checking belongs to `/review`).
