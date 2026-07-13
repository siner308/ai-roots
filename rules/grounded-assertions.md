# Grounded Assertions — Verify Before Stating an Inference as Fact

An inference is allowed to exist only as an inference. The moment it is about to be *stated as fact* — in a summary, a recommendation, a handoff note, a "X팀에 전달해야 합니다" — it must first be grounded in evidence you actually looked up, or explicitly marked as a guess.

## The failure this prevents

Mid-task, plausible inferences accumulate: "SDK consumes this API, so the SDK team owns the spec", "this table is env-scoped, so QA rollout works", "this page is legacy, so nobody calls it". Each sounds reasonable, and autoregressive writing turns them into confident declarative sentences. The reader then acts on a guess dressed as a fact — coordinating with the wrong team, skipping a live code path, shipping the wrong rollout plan.

Real instance: "웹뷰 스펙은 SDK(데브플레이셀)가 파싱하므로 그쪽에 전달해야 한다"고 단정했지만, 웹뷰 작업의 소유는 백엔드셀이었다. 소유 조직은 조회 가능한 사실이었는데 추론으로 대체했다.

## What to do

- Before writing an inference as a declarative statement, ask: **could I verify this right now?** If yes (a file, a config, an org chart, a git log, a route table), go look — verification is usually one search away and cheaper than a wrong handoff.
- If verification is not possible in-session, keep the epistemic marker visible: "~로 보입니다", "확인 필요", "추정". Never silently drop the hedge between the thinking step and the output.
- Ownership, responsibility, and "who consumes this" claims deserve extra suspicion — they are organizational facts, not derivable from code structure alone.
- This composes with `verify-each-instance` (per-instance checks under a perceived pattern) and `evaluation-integrity` (rationale before verdict). This rule covers the general case: any single inference crossing from thought to asserted fact.

## Rules

- Never state an inference as fact without either (a) evidence you actually retrieved this session, or (b) an explicit uncertainty marker.
- Verifiable-now claims (code paths, configs, schemas, routes, docs) get verified, not hedged — hedging is the fallback only when lookup is impossible.
- Claims about people, teams, and ownership require a source (docs, CLAUDE.md, the user) — code-structure inference alone is insufficient.
- When a hedge is dropped, that is the moment of assertion — the evidence must already exist at that point, not after.
