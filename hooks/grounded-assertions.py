#!/usr/bin/env python3
"""Stop hook enforcing the grounded-assertions rule: a per-claim evidence audit before a substantial turn ends.

The rule tells the model to keep uncertainty markers on unverified claims, but autoregressive writing strips them by default, and a resident rule competes with the whole context and loses — enforcement needs the one layer that runs after the response exists.
The audit is deliberately not a generic "are you sure?": challenging a whole answer flips correct claims too (FlipFlop effect), so the block demands a claim-by-claim check against session evidence and forbids touching evidenced claims.
A sentence-count gate keeps the loop off short conversational turns. Past the first round the gate no longer applies — an audit reply is short by construction — and a per-turn round counter caps the loop instead, so a round that names a defect without applying the fix gets one follow-up push.
Fails open on any parse or state error so a broken transcript or an unwritable counter can never trap the session.
"""
import json
import os
import re
import sys

from hook_lang import localize

SENTENCE_END = re.compile(r'[.!?…。！？](?=\s|$)')
SENTENCE_GATE = 8
MAX_ROUNDS = 2
KEEP_TURNS = 20
STATE_PATH = os.path.expanduser("~/.claude/.ai-roots/fact-check")
ROUNDS_PATH = os.path.expanduser("~/.claude/.ai-roots/fact-check-rounds")

AUDIT = """grounded-assertions audit:

Audit the response you just wrote, claim by claim. A material claim is a factual assertion beyond the user's input, this session's tool output, or files you actually read. For each one:

1. Backed by session evidence (a file you read, command output, the user's own words) -> leave it exactly as written. Do not add hedges to evidenced claims and do not restyle them.
2. No evidence, but verifiable right now with a tool -> verify now and correct the claim to match what you find.
3. No evidence and not verifiable in-session -> restore an uncertainty marker ("appears to", "unverified"; in Korean output: "~로 보입니다", "확인 필요").

When the check shows the work itself is wrong — the code, the file, the command, the plan, not just the sentence describing it — fix the work in this turn and then describe it correctly. Naming a defect precisely does not resolve it, and an audit that reports a problem it could have fixed is unfinished. When the fix turns on a decision only the user can make, ask that single question instead.

Close by answering the user's question again in one or two sentences — the conclusion they asked for, not a report on this audit. Your reply is the last thing on their screen, so ending on "checked, nothing to fix" buries the answer above the fold; ending on the answer itself keeps it in view. When a claim did change, state the correction and then the corrected conclusion. Change what is wrong and leave everything else — do not restyle the response."""

RESOLVE = """grounded-assertions follow-up:

Two checks on the round you just wrote, then the turn ends.

1. Did that round name anything as wrong, missing, or worth changing, and leave it unapplied? Apply it now — edit the file, run the command, correct the text — or ask the one question that blocks it. A defect described is not a defect resolved.
2. Any new material claim that round introduced gets the same sort as before: evidenced -> leave it, verifiable right now -> verify it, neither -> mark it uncertain.

If both come up clean, close in one line and stop. Do not repeat the audit or re-explain the answer."""


def gate_setting():
    # Written by the /fact-check skill.
    try:
        raw = open(STATE_PATH).read().strip().lower()
    except OSError:
        return SENTENCE_GATE
    if raw == "off":
        return None
    try:
        return max(1, int(raw))
    except ValueError:
        return SENTENCE_GATE


def round_limit():
    try:
        return max(1, int(os.environ["AI_ROOTS_FACT_CHECK_ROUNDS"]))
    except (KeyError, ValueError):
        return MAX_ROUNDS


def sentence_count(text):
    n = 0
    fence = False
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if fence or not line.strip():
            continue
        n += len(SENTENCE_END.findall(line))
    return n


def read_turn(path):
    """Return the turn's final assistant text and the uuid of the user message that opened it."""
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        return "", ""
    text = None
    for raw in reversed(lines):
        try:
            entry = json.loads(raw)
        except Exception:
            continue
        if entry.get("isSidechain"):
            continue
        kind = entry.get("type")
        content = (entry.get("message") or {}).get("content")
        if kind == "user" and not entry.get("isMeta"):
            # Tool results ride user-type entries as tool_result blocks, and a hook's own block message rides one marked isMeta.
            # Only a string body or a text block marks a real prompt bounding the turn.
            if isinstance(content, str) or (
                isinstance(content, list)
                and any(isinstance(b, dict) and b.get("type") == "text" for b in content)
            ):
                return text or "", entry.get("uuid", "")
        if kind != "assistant" or text is not None:
            continue
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            texts = [
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
            if texts:
                text = "\n".join(texts)
    return text or "", ""


def rounds_done(key):
    """Rounds already issued for this turn, or None when the count is untrackable."""
    try:
        with open(ROUNDS_PATH) as f:
            state = json.load(f)
        n = state[key]
    except Exception:
        return None
    return n if isinstance(n, int) else None


def record_round(key, n):
    state = {}
    try:
        with open(ROUNDS_PATH) as f:
            loaded = json.load(f)
        if isinstance(loaded, dict):
            state = loaded
    except Exception:
        pass
    state.pop(key, None)
    state[key] = n
    for stale in list(state)[:-KEEP_TURNS]:
        del state[stale]
    try:
        os.makedirs(os.path.dirname(ROUNDS_PATH), exist_ok=True)
        with open(ROUNDS_PATH, "w") as f:
            json.dump(state, f)
    except OSError:
        pass


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if os.environ.get("AI_ROOTS_FACT_CHECK") == "0":
        return 0
    gate = gate_setting()
    if gate is None:
        return 0
    text, turn = read_turn(data.get("transcript_path", ""))
    key = "%s:%s" % (data.get("session_id", ""), turn)
    if data.get("stop_hook_active"):
        rounds = rounds_done(key)
        # A lost count means a round already fired but cannot be attributed; stop rather than risk a loop.
        if rounds is None:
            return 0
    else:
        rounds = 0
        if sentence_count(text) < gate:
            return 0
    if rounds >= round_limit():
        return 0
    record_round(key, rounds + 1)
    print(json.dumps({"decision": "block", "reason": localize(AUDIT if rounds == 0 else RESOLVE)}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
