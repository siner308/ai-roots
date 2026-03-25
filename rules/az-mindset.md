# Thinking Expansion Mindset

Apply thinking expansion techniques progressively based on task complexity.

## Complexity Routing

| Complexity | Criteria | Techniques |
|------------|----------|------------|
| LOW | Simple questions, fact checks, one-line fixes | A-Z Priming only |
| MEDIUM | Feature implementation, bug fixes, design choices | A-Z Priming + Devil's Advocate |
| HIGH | Architecture decisions, complex debugging, technology selection | A-Z Priming + Devil's Advocate + First Principles + Systems Thinking |

## Techniques

### A-Z Token Priming (always, FIRST)

Generate A-Z keywords related to the current topic BEFORE composing the response. This primes knowledge activation and must be the first step, not an afterthought.
Surface non-obvious concepts, risks, and alternatives that the user may not have considered.

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

### Systems Thinking (HIGH)

Analyze the whole structure and feedback loops, not just the parts.
- What are the 2nd and 3rd order effects of this change?
- What feedback loops exist?
- Where could unintended consequences emerge?

## Rules

- **Execution order**: A-Z Priming MUST be performed and displayed FIRST (at the top of the response), before any reasoning or answer. This ensures knowledge activation influences the entire response, not just decorates it.
- Show your work: display the complexity classification and applied techniques in a `### Thinking Expansion` section at the end of the response.
- Pursue depth and breadth while staying concise.