---
name: technical-doc-precision
description: "Apply when writing or editing reference documentation, a README, a runbook, a config/CLI/env-var doc, a changelog or migration note, or when asked to proofread, tighten, or rewrite existing technical text. Covers preserving meaning while editing, explicit logic scope, distinguishing omitted/empty/null/false/0, range and time bases, placeholders vs real values, and separating commands from output."
---

# Technical Doc Precision

A technical doc is read by someone who will act on it literally, so every condition, value, and boundary has to survive the writing.

## Rules

- When editing, keep the actor, object, condition, timing, order, quantity, negation, exceptions, and obligation level exactly as they were. When the original is ambiguous, leave it as a question for the author rather than picking a reading. ❌ "check that the vent closed" rewritten as "close the vent", or "log before returning" as "log after returning" ✅ the shorter sentence still checks, and still logs first.
- State logical scope in words: "all of", "at least one of", "exactly one of". Do not compress a condition that matters into "and/or", "A/B", or "etc.". "If A, B" and "only if A, B" are different claims, so do not strengthen a sufficient condition into a necessary one.
- Say what each absent value does: omitted, empty string, empty list, null, false, and 0 are different inputs. ❌ "`MAX_LOANS` defaults to unlimited if unset" when `0` also means unlimited and an empty string raises ✅ one line per case.
- Give every range its boundaries and basis: inclusive or exclusive at each end, and in what unit or against what reference. ❌ "between 10 and 20 degrees" ✅ "10 to 20 °C inclusive, measured at the bench sensor".
- Give every time its basis: wall clock or monotonic, UTC or local, counted from what event, per what window. ❌ "retries 3 times within an hour" ✅ "retries up to 3 times in a rolling 60-minute window that starts at the first failure".
- Mark placeholders so nobody mistakes them for real values (`<catalog-id>`), and write real values literally. A plausible-looking fake value in a command gets pasted and run.
- Put a command and its output in separate code blocks, with no prompt character in the command block, so copying the command copies only the command.
