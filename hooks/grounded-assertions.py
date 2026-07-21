#!/usr/bin/env python3
"""Stop hook enforcing the grounded-assertions rule: a per-claim evidence audit before a substantial turn ends.

The rule tells the model to keep uncertainty markers on unverified claims, but autoregressive writing strips them by default, and a resident rule competes with the whole context and loses — enforcement needs the one layer that runs after the response exists.
The audit is deliberately not a generic "are you sure?": challenging a whole answer flips correct claims too (FlipFlop effect), so the block demands a claim-by-claim check against session evidence and forbids touching evidenced claims.
A sentence-count gate keeps the loop off short conversational turns; stop_hook_active caps it at one audit round per turn.
Fails open on any parse error so a broken transcript can never trap the session.
"""
import json
import os
import re
import sys

SENTENCE_END = re.compile(r'[.!?…。！？](?=\s|$)')
SENTENCE_GATE = 8
STATE_PATH = os.path.expanduser("~/.claude/.ai-roots/fact-check")

AUDIT = """grounded-assertions audit:

Audit the response you just wrote, claim by claim. A material claim is a factual assertion beyond the user's input, this session's tool output, or files you actually read. For each one:

1. Backed by session evidence (a file you read, command output, the user's own words) -> leave it exactly as written. Do not add hedges to evidenced claims and do not restyle them.
2. No evidence, but verifiable right now with a tool -> verify now and correct the claim to match what you find.
3. No evidence and not verifiable in-session -> restore an uncertainty marker ("appears to", "unverified"; in Korean output: "~로 보입니다", "확인 필요").

If nothing needs fixing, say so in one line and finish. Do not rewrite or restyle the rest of the response."""


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


def last_assistant_text(path):
    try:
        with open(path) as f:
            lines = f.readlines()
    except OSError:
        return ""
    for raw in reversed(lines):
        try:
            entry = json.loads(raw)
        except Exception:
            continue
        if entry.get("isSidechain"):
            continue
        kind = entry.get("type")
        content = entry.get("message", {}).get("content")
        if kind == "user":
            # Tool results ride user-type entries as tool_result blocks;
            # only a string body or a text block marks a real user message bounding the turn.
            if isinstance(content, str):
                return ""
            if isinstance(content, list) and any(
                isinstance(b, dict) and b.get("type") == "text" for b in content
            ):
                return ""
        if kind != "assistant":
            continue
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = [
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
            if texts:
                return "\n".join(texts)
    return ""


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    if os.environ.get("AI_ROOTS_FACT_CHECK") == "0":
        return 0
    gate = gate_setting()
    if gate is None:
        return 0
    text = last_assistant_text(data.get("transcript_path", ""))
    if sentence_count(text) < gate:
        return 0
    print(json.dumps({"decision": "block", "reason": AUDIT}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
