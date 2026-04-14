# Incremental Verification for Uncertain Work

When the outcome of a task is uncertain — external APIs, browser automation, shell escaping, unfamiliar libraries — break the work into the smallest verifiable steps and confirm each one before proceeding.

## Pattern

1. **Start with the smallest possible unit.** Run a single API call, extract one record, write one row to the database. Do this inline (e.g. `node -e "..."`) before writing any script or function.
2. **Verify the output explicitly.** Print the result, check the database, confirm the shape of the data. "It ran without errors" is not verification — look at the actual output.
3. **Build up one layer at a time.** Only after step N succeeds, add step N+1. If step N+1 fails, fix it and re-verify from step 1 — don't assume earlier steps still work after changes.
4. **Convert to a script last.** Once the full chain works inline, copy the verified code into a script file. Run the script on a small input (1-2 items) before scaling up.
5. **Scale gradually.** Run on 5 items, then 50, then the full dataset. Check results at each scale.

## Why

Writing a full script first and running it on thousands of items makes failures expensive to diagnose:
- Error messages scroll off screen or get buried in logs
- Multiple failure modes stack on top of each other
- Debugging requires re-running the entire slow pipeline
- "It worked on my machine" assumptions compound at scale

Small inline tests fail fast, fail cheap, and produce clear error messages.

## Example

Bad: Write a 250-line crawling script → run on 10 countries × 20 keywords → get `undefined` in the database → spend 30 minutes debugging escaping issues

Good:
```
Step 1: agent-browser eval 'single JS expression' → verify JSON output
Step 2: node -e "fetch embedding API with one title" → verify 1536 dimensions
Step 3: node -e "insert one row into supabase" → verify row in DB
Step 4: node -e "step 1 + 2 + 3 together for 1 video" → verify end-to-end
Step 5: Write script using verified code → run on 5 videos → check DB
Step 6: Run full scale
```

## When to Apply

- External system integration (APIs, databases, browser automation)
- Shell command composition (escaping, piping, subshells)
- Data pipeline construction (extract → transform → load)
- Any task where you've never run the exact code path before
