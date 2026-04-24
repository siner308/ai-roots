# Thinking Expansion Mindset

This rule is an internal thinking aid, not an output ritual. Apply it when the user's request benefits from broader retrieval, but do not let it override brevity, natural conversation, or task-specific formatting.

## Step 1: Concept Priming

Before analysis on MEDIUM or HIGH complexity work, generate priming keywords internally as an early thinking step. This primes broad knowledge retrieval before conclusions form. Keep the keywords invisible by default.

The purpose is upstream activation: keywords must influence the thinking, not merely document it after the fact. If keywords only appear in output, the reasoning that produced the response was never primed.

### Keyword Count by Complexity

| Complexity | Count | Cross-domain minimum | Rendering |
|------------|-------|---------------------|-----------|
| LOW | 0–3 | 0 | No visible priming line |
| MEDIUM | 6–10 | 2 | No visible priming line |
| HIGH | 10–15 | 3 | Optional visible priming line only when it helps the user evaluate the framing |

LOW complexity tasks usually do not need explicit priming. If the request is a fact check, one-line edit, simple command, or routine status update, skip priming rather than manufacturing concepts.

### Diversity Axis — Domain Spread

Since there is no alphabet constraint, diversity must be enforced on a different axis: **conceptual domain**. For MEDIUM/HIGH work, use the cross-domain minimum from the table above:

| Category | Examples |
|----------|---------|
| CS/Engineering | Idempotency, Backpressure, Linearizability |
| Natural Science | Entropy, Homeostasis, Nucleation |
| Social Science | Incentive, Satisficing, Principal-agent |
| Design/Architecture | Affordance, Desire-path, Legibility |
| Mathematics/Logic | Invariant, Bijection, Ergodicity |
| Humanities/Philosophy | Hermeneutics, Parsimony, Dialectic |

This is not an exhaustive list — any real academic domain counts. The point is preventing all keywords from clustering in one conceptual neighborhood.

### Keyword Quality Rules — STRICT

Each keyword MUST be a **single standalone word or established named concept** (e.g., "Goodhart's Law", "Principal-agent") that has its own Wikipedia article, textbook chapter, or established field of study.

**Forbidden patterns:**
- Hyphenated compounds: `grpc-json`, `zero-config`, `x-envoy` — label-stuffing, not concept activation
- Domain echo: words already present in the user's question or the immediate problem context. If the user asked about gRPC, `gRPC` is not a keyword — it's an echo
- Empty generics: `unknown`, `error`, `config`, `data`, `type` — fit any context, activate nothing
- Synonym clusters: `Config` + `Setting` + `Option` is one concept occupying three slots
- Stale rotation: if a keyword appeared in your last 3 responses in this conversation, pick a different concept for the same territory

**Preferred keyword types:**
- **Principles**: Parsimony, Least-privilege, Separation-of-concerns
- **Named patterns**: Ratchet, Flywheel, Hysteresis, Circuit-breaker
- **Cross-domain analogies**: Homeostasis (biology→system stability), Arbitrage (economics→optimization gap)

### Keyword-to-Reasoning Bridge

Priming is not a ritual. At least 2 keywords should influence the actual analysis on MEDIUM/HIGH work — either by naming a pattern that frames the solution, surfacing a cross-domain insight, or identifying a tension the obvious approach misses.

Self-check: "If I remove the priming step, would the answer lose a useful frame, risk, or analogy?" If no → priming was unnecessary.

Format:
- Default: no visible priming line.
- HIGH, when useful for transparency: `Framing: Concept(short gloss), Concept(short gloss), ...`

Examples:
- Internal MEDIUM set: `Affordance`, `Backpressure`, `Goodhart's Law`, `Homeostasis`
- Optional HIGH visible line: `Framing: Goodhart's Law(metric becomes target), Backpressure(flow control), Homeostasis(self-regulating balance)`

Keyword annotations should use the user's language. The examples above are in English for language-neutrality of this rule file.

## Step 2: Classify Complexity

| Complexity | Criteria | Additional Techniques |
|------------|----------|----------------------|
| LOW | Simple questions, fact checks, one-line fixes | None |
| MEDIUM | Feature implementation, bug fixes, design choices | + Devil's Advocate |
| HIGH | Architecture decisions, complex debugging, technology selection | + Devil's Advocate + First Principles + Systems Thinking |

## Step 3: Apply Techniques (MEDIUM and HIGH only)

### Devil's Advocate (MEDIUM+)

Deliberately construct counterarguments before reaching a conclusion.
- What are the downsides of this approach?
- What benefits would the opposite choice bring?
- What trade-offs is the user missing?

### First Principles (HIGH)

Discard conventions and assumptions. Decompose to fundamental truths and rebuild from there.
- What is the essential purpose of this?
- How would this be designed from scratch, ignoring existing patterns?
- Which constraints assumed to be real are actually artificial?

### Systems Thinking (HIGH) — MUST be visible in output

For HIGH complexity responses, you MUST include a labeled `**Ripple effects:**` paragraph in the response body. This paragraph should address at least one of:
- 2nd/3rd order effects of the topic or decision
- Feedback loops or cascading consequences
- Unintended side effects on other parts of the system

This is NOT optional for HIGH. If the topic seems purely technical, consider ripple effects on: developer experience, debugging, team onboarding, API evolution, or operational burden.

## Output

Do not emit metadata by default. If HIGH complexity work benefits from showing the framing, use one short `Framing:` line near the start; otherwise keep the priming internal.
