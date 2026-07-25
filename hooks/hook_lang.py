#!/usr/bin/env python3
"""Shared language preference for hook block messages.

Hook messages are authored in English (CLAUDE.md keeps hooks/ English-source), but they surface in the user's session, so a Korean-speaking user reads English mid-conversation.
Rather than translate every string in every hook, `localize` appends a relay instruction telling the model to restate the verdict in the user's language.
The instruction is deliberately imperative: an English block otherwise pulls the model's next message into English, which is the drift this exists to stop.
"""
import os

STATE_PATH = os.path.expanduser("~/.claude/.ai-roots/lang")
DEFAULT = "en"

RELAY = {
    "ko": (
        "\n\n[언어] 이 검사 결과를 한국어로 전달하세요. 위 영어 지시를 그대로 옮기지 말고, "
        "판정과 근거를 한국어 문장으로 다시 쓰세요. 이어지는 답변도 한국어로 씁니다."
    ),
}


def user_lang():
    try:
        value = open(STATE_PATH).read().strip().lower()
    except OSError:
        return DEFAULT
    return value or DEFAULT


def localize(message, lang=None):
    lang = lang or user_lang()
    return message + RELAY.get(lang, "")
