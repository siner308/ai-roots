# Grounded Assertions Hook

A `Stop` hook that runs when a turn is about to end.
When the final response is substantial enough to carry factual claims, it blocks once and asks for a claim-by-claim audit: every material assertion must either point to evidence gathered this session, get verified with a tool right now, or get its uncertainty marker restored.

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

`stop_hook_active` caps the loop at one audit round per turn, and the instruction ends with "do not rewrite the rest" so the audit round cannot regenerate the response wholesale.

## What it skips

- Turns whose final message is under the sentence gate — short conversational answers never trigger it.
- Fenced code blocks, which do not count toward the gate.
- Sidechain (subagent) transcript entries.
- Anything when `/fact-check off` was run (state in `~/.claude/.ai-roots/fact-check`, read live each turn) or `AI_ROOTS_FACT_CHECK=0` is set — with no configuration the hook is on and the gate does the tuning.
- Any transcript it cannot read or parse — the hook fails open, never trapping a session.

## Known limitations (reviewed, accepted)

The gate is a volume heuristic, not a claim detector: a long response with zero factual claims still gets audited (the audit then costs one short "nothing to fix" round), and a short response full of confident guesses slips under it.
The audit round itself is not re-audited — a claim introduced during the audit escapes; one loop is the deliberate ceiling.
Same-context audit means the generator reviews itself; the claim-by-evidence structure narrows but does not eliminate that bias (heavier cross-checking belongs to `/review`).
