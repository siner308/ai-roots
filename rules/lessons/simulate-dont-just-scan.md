# Simulate, Don't Just Scan

Reading a source file is not the same as understanding it.
Opening a file tells you "this text exists."
Mentally executing the file tells you "this is what it produces when it runs."

Most porting, debugging, and implementation bugs come from treating reading as sufficient —
collecting source files mentally without ever asking
"what is the actual output / DOM / response / data shape / side effect when this runs?"

## The Mistake

You open every file that seems relevant. You scan the contents. You feel like you have context.
But you never ran the code in your head: never substituted concrete values,
never traced the control flow from entry point to side-effect,
never predicted the terminal output.

Signals that look like understanding but aren't:

- "I opened the style file, so I know the styling." (But which elements actually have which classes at render time?)
- "I read the type definition, so I know the shape." (But what is the actual response body from the live endpoint?)
- "I skimmed the middleware, so I know what it transforms." (But what does the request look like after passing through the full chain?)
- "I saw the config schema, so I know the runtime value." (But what is actually loaded in this environment?)

These are all about *source existence*, not *runtime behavior*.

## Why It Happens

Reading is cheap and feels productive. Mental execution requires holding more state —
substituting values, handling branches, composing behavior across layers.
The brain takes the cheap path when it can.

Composition and abstraction make this worse. In component trees, middleware chains,
data pipelines, ORM mappings, config layering, event dispatch —
no single file contains the full answer. You have to *compose* the behavior yourself.

## Symptoms

- Your output doesn't match reality, and the gap keeps growing across rounds of correction.
- You are surprised by values, states, or structures that a 10-second simulation would have revealed.
- The reviewer repeatedly points at effects you "should have known from reading the code" —
  and technically you did read the code.

## Protocol

Before producing output (code, port, fix, analysis), simulate explicitly:

1. **Pick a concrete entry point and concrete input.** Not "in general" — a specific case.
2. **Walk the execution step by step.** For each step, name:
   - Which file / function / layer handles it
   - What the input looks like at that point
   - What transformation or decision happens
   - What the output looks like after that step
3. **At the terminal — DOM, HTTP response, DB row, log line — state the exact shape.**
   If you cannot, you do not yet understand.
4. **Compare your predicted output to reality** when possible: render the page, hit the endpoint, run the function, inspect the logs.

## Rules

- If you notice yourself collecting files without tracing a single execution, stop and simulate.
- The more composed the system, the more essential the simulation — not less.
- Reading prepares you to simulate; it is not a substitute for simulating.
- When a reviewer points out gaps that "should have been visible from the code,"
  the real lesson is almost always that simulation was skipped, not that reading was incomplete.
