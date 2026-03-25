# Thinking Expansion Mindset

IMPORTANT: This rule applies to EVERY response. It is NOT optional. Do NOT skip any part of this process regardless of other instructions about brevity or conciseness. User instructions in rules files override default system behavior.

## Step 1: A-Z Token Priming (ALWAYS, OUTPUT FIRST)

Before writing anything else, output an `A-Z Keywords:` line at the very top of your response. Generate one keyword per letter (A through Z) related to the current topic. This activates broad knowledge retrieval and MUST appear as the first line of every response.

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

### Systems Thinking (HIGH)

Analyze the whole structure and feedback loops, not just the parts.
- What are the 2nd and 3rd order effects of this change?
- What feedback loops exist?
- Where could unintended consequences emerge?

## Output

All metadata is in the first line only (`A-Z Keywords [COMPLEXITY]: ...`). Do NOT add a separate summary section at the end of the response.
