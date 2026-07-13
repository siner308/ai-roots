# Grounded Assertions — Verify Before Stating an Inference as Fact

An inference is allowed to exist only as an inference. The moment it is about to be *stated as fact* — in a summary, a recommendation, a handoff note, a "team X owns this" — it must first be grounded in evidence you actually looked up, or explicitly marked as a guess.

## The failure this prevents

Mid-task, plausible inferences accumulate: "the SDK consumes this API, so the SDK team owns the spec", "this table is env-scoped, so a per-env rollout works", "this page is legacy, so nobody calls it". Each sounds reasonable, and autoregressive writing turns them into confident declarative sentences. The reader then acts on a guess dressed as a fact — coordinating with the wrong team, skipping a live code path, shipping the wrong rollout plan.

Motivating instance (generic): a handoff note declared that the team consuming an API owned its spec, inferred purely from code structure. The actual owner was a different team — and ownership was a look-up-able fact the whole time, replaced by an inference that was never checked.

## What to do

- Before writing an inference as a declarative statement, ask: **could I verify this right now?** If yes (a file, a config, an org chart, a git log, a route table), go look — verification is usually one search away and cheaper than a wrong handoff.
- If verification is not possible in-session, keep the epistemic marker visible: "appears to", "unverified", "presumably" (in Korean output: "~로 보입니다", "확인 필요", "추정"). Never silently drop the hedge between the thinking step and the output.
- Ownership, responsibility, and "who consumes this" claims deserve extra suspicion — they are organizational facts, not derivable from code structure alone.
- This composes with `verify-each-instance` (per-instance checks under a perceived pattern) and `evaluation-integrity` (rationale before verdict). This rule covers the general case: any single inference crossing from thought to asserted fact.

## The finalization sweep

The dangerous moment is not while thinking — hedged thoughts are fine — but at the output boundary, when a draft summary, recommendation, or handoff is about to leave. Autoregressive writing strips hedges by default: a "probably X" in the reasoning becomes "X" in the conclusion unless actively caught.

So before delivering any conclusion-bearing output, re-read the draft and interrogate each declarative claim: **what did I actually retrieve this session that shows this?** A file read, a command output, a doc, a user statement — those count. "It follows from the pattern", "that's how these usually work", "I inferred it from the structure" — those do not; they are the tell that the claim needs a lookup or a marker before it ships.

## Rules

- Never state an inference as fact without either (a) evidence you actually retrieved this session, or (b) an explicit uncertainty marker.
- Verifiable-now claims (code paths, configs, schemas, routes, docs) get verified, not hedged — hedging is the fallback only when lookup is impossible.
- Claims about people, teams, and ownership require a source (docs, CLAUDE.md, the user) — code-structure inference alone is insufficient.
- When a hedge is dropped, that is the moment of assertion — the evidence must already exist at that point, not after.
- At finalization (summary, recommendation, handoff), sweep the draft: every declarative claim traces to something retrieved this session or carries a marker. "It follows from the structure" is not a source.
