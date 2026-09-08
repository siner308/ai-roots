# Char Discipline Hook

A hook on two events that flags characters a keyboard does not type: `PostToolUse` on `Edit|Write|MultiEdit` for the text an edit adds, and `Stop` for the turn's final message.
It covers the character section of the [`prose-style`](../rules/prose-style.md) rule: visible glyphs that read as a machine signature, and invisible codepoints that carry no meaning in prose.
The character tables live in `char_tables.py`, shared with [`gh-markdown-style`](gh-markdown-style), which gates the same set on PR and issue bodies. Three surfaces, one table, so they cannot disagree about what is barred.

## Why it exists

Of everything `prose-style` asks for, the character rule is the one a static check catches exactly: a codepoint is either in the text or not, with no heuristic and no language dependence.
It is also the concern a resident rule protects worst, since emitting an em dash is not a decision the model makes deliberately; the glyph arrives with the sentence.
A reader who cannot judge the prose still spots the em dash and the middle dot, and dismisses the page as machine output.
An invisible character has no reader at all: it survives a copy into code, a commit message, or a search index, and breaks things there with nothing on screen to explain why.

## What it flags

Visible glyphs, each with the ASCII form to write instead:

| Character | Write instead |
|-----------|---------------|
| em dash, en dash, horizontal bar | a period, a comma, a colon, or parentheses |
| middle dot | a comma, or `and` / `와` / `과` |
| curly double and single quotes | ASCII `"` and `'` |
| horizontal ellipsis | three periods |
| left, right, and double arrows | `->`, `<-`, `=>`, or the relation in words |
| bullet, white bullet, triangular bullet, small black square | an ASCII `-` |

Invisible codepoints, all replaced by a plain space or nothing: the no-break and narrow no-break spaces, `U+2000` to `U+200A`, the medium mathematical and ideographic spaces, the braille blank, the zero-width space, non-joiner and joiner, the word joiner, the byte-order mark, the soft hyphen, the directional marks and override, and the four invisible operators.

## Scope: every file, code included

`comment-discipline` fires on code comments and `prose-discipline` on Markdown, and they stay off each other's files so one edit never draws two blocks.
Characters admit no such split: a curly quote inside a string literal or a zero-width space inside an identifier is a bug, not a style question.
So this hook runs on whatever file the edit touched, and an edit can draw both it and the medium-specific hook. They are different concerns, and both verdicts are wanted.

## The two events

A file edit is not where the characters usually reach the user. A chat reply is, so the `Stop` surface is the one that catches the case the rule was written for: prose composed straight into the answer, never passing through a file.
It reads the turn's last assistant text from the transcript, blocks once, and asks for the affected sentences to be rewritten and the answer restated.
`stop_hook_active` caps it at one block per turn, and an unreadable transcript scans as empty, so a stubborn exempt character cannot trap the session.

## The block

The message lists each character with a count, its ASCII replacement, and a sample line for the visible ones, then asks for a verdict per occurrence with replace as the default.
The legitimate keeps cannot be detected statically, so they are named in the message and the model decides: a rule, doc, or fixture that names the character on purpose; quoted source text or upstream data copied as it is; an identifier or filename; punctuation the language requires (`。`, `、`, `「」`, `¿`); a math, unit, or currency symbol; a `❌`/`✅` comparison label.
Naming the exemption that applies is enough to continue.

## What it skips

- A tool call with no `file_path` (nothing was written).
- Everything outside the text an edit adds, so a pre-existing character elsewhere in the file stays quiet until someone touches that line.
- Fenced code blocks, on both surfaces. They hold quoted commands, diffs, and file content that has to stay byte-exact.
- A second `Stop` round in the same turn.

## Off switch

`AI_ROOTS_CHAR_CHECK=0` disables it.
