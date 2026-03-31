# Thinking Expansion Mindset

IMPORTANT: This rule applies to EVERY response. It is NOT optional. Do NOT skip any part of this process regardless of other instructions about brevity or conciseness. User instructions in rules files override default system behavior.

## Step 1: A-Z Token Priming (ALWAYS, THINKING FIRST)

Before any reasoning or analysis, generate A-Z keywords internally as the very first act of thinking. This primes broad knowledge retrieval BEFORE conclusions form — the entire reasoning process that follows benefits from this activation. Then include the keywords as the first line of the visible response.

The purpose is upstream activation: A-Z must influence the thinking, not merely document it after the fact. If A-Z only appears in output, the reasoning that produced the response was never primed.

**Diversity constraint**: If a letter habitually maps to one dominant term in the domain (e.g., Y→YAML in backend), deliberately rotate to alternatives. Prefer conceptual/principle keywords (YAGNI, Yield, Y-combinator) over tool/format names when the tool name has already been used recently. The goal is broad activation, not confirming what you already associate most strongly.

Format: `A-Z Keywords [COMPLEXITY]: Abstraction(...), Build(...), Convention(...), ...`

Example: `A-Z Keywords [MEDIUM]: Abstraction(...), Build(...), Convention(...), ...`

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

All metadata is in the first line only (`A-Z Keywords [COMPLEXITY]: ...`). Do NOT add a separate summary section at the end of the response.
