# Verify Each Instance — Recurrence Is a Hypothesis, Not a License

When work looks repetitive — the same shape over and over, a familiar pattern, "just like the last N" — there is a pull to switch to autopilot: apply the template, stamp every item the same way, stop checking. Resist it. A perceived pattern is a hypothesis to confirm per case, not a conclusion that lets you skip the check.

The failure is silent and compounding: one assumption applied across many items is wrong in all of them at once, and because each one looked "handled," nobody notices until much later.

## Where it bites

- **Porting or replicating from a source** — copying a reference (codebase, schema, document, dataset) by reaching for a generic pattern instead of reading what the source actually is. The tell is adding, dropping, or reshaping structure to match what the template "usually" has — an extra field, a wrapper, a default, a naming convention — when the source has no such thing. Inventing structure from habit instead of mirroring the fact in front of you. A port's whole job is fidelity to the source, so each piece gets checked against the origin, not against what similar things tend to look like.
- **Batch edits / data work** — running the same transform or find-replace across many sites and assuming every match is the same case. Some aren't.
- **Repeated judgments** — triaging, classifying, or reviewing a list where the first few set an expectation and the rest get rubber-stamped.

## What to do instead

- Treat the pattern as a prior, then check each instance against its own facts before acting on it.
- When replicating from a source, design from the source's actual structure and behavior — not from a generic template you assume it follows. Go look.
- Let cost guide effort: the more instances an assumption fans out to, the more a single per-instance check is worth.
- Catch the autopilot tell — "these are all the same, I'll just…" — and slow down on the ones you never actually looked at.

## Rules

- A recurring shape is a hypothesis to verify per case, not a conclusion to apply blindly.
- When porting or replicating, build from the source's facts; never invent structure from a generic pattern you expect it to match.
- Verify each instance against its own facts even when it looks identical to the rest, and surface the ones that turn out to differ.
- This applies beyond code — any repetitive task (data, documents, triage, research) where pattern-matching tempts you to skip the per-item check.
