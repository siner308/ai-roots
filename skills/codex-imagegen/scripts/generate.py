#!/usr/bin/env python3
"""Generate one raster image through Codex: its built-in image tool on the ChatGPT plan, or its bundled Images API CLI."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_STYLE = "Do not make it photorealistic. Use a painterly or diagrammatic style."
SUBSCRIPTION_TIMEOUT = 600
LOGIN_STATUS_TIMEOUT = 30


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def cli_path() -> Path:
    return codex_home() / "skills" / ".system" / "imagegen" / "scripts" / "image_gen.py"


def build_api_command(cli: Path, args: argparse.Namespace, target: Path, dry_run: bool) -> list[str]:
    command = [sys.executable, str(cli), "generate", "--prompt", args.description, "--out", str(target), "--force"]
    for flag, value in (
        ("--style", args.style),
        ("--constraints", args.extra),
        ("--model", args.model),
        ("--size", args.size),
        ("--quality", args.quality),
    ):
        if value:
            command += [flag, value]
    if dry_run:
        command.append("--dry-run")
    return command


def build_subscription_prompt(args: argparse.Namespace) -> str:
    lines = [f"Image: {args.description}"]
    if args.style:
        lines.append(f"Style: {args.style}")
    if args.extra:
        lines.append(f"Constraint: {args.extra}")
    if args.size:
        lines.append(f"Aspect and size: {args.size}")
    lines.append("Call the built-in image generation tool once with this description. Do not read any files or run commands. Reply only with done.")
    return "\n".join(lines)


def build_subscription_command(codex: str, workdir: Path, prompt: str) -> list[str]:
    return [codex, "exec", "--json", "--skip-git-repo-check", "--sandbox", "read-only", "-C", str(workdir), prompt]


def parse_payload(stdout: str) -> object:
    start = stdout.find("{")
    if start < 0:
        return stdout.strip()
    try:
        return json.loads(stdout[start:])
    except json.JSONDecodeError:
        return stdout.strip()


def parse_events(stdout: str) -> tuple[str | None, dict | None, list[str]]:
    thread_id, usage, errors = None, None, []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = event.get("type")
        if kind == "thread.started":
            thread_id = event.get("thread_id")
        elif kind == "turn.completed":
            usage = event.get("usage")
        elif kind in ("turn.failed", "error"):
            errors.append(json.dumps(event, ensure_ascii=False)[:400])
    return thread_id, usage, errors


def rollout_details(thread_id: str) -> dict:
    # The JSONL stream names neither the model nor the tool, so read them from the session rollout.
    details: dict = {}
    for rollout in (codex_home() / "sessions").glob(f"*/*/*/rollout-*-{thread_id}.jsonl"):
        for line in rollout.read_text(errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict):
                continue
            if event.get("type") == "turn_context" and payload.get("model"):
                details["model"] = payload["model"]
            tool_input = str(payload.get("input") or payload.get("name") or "")
            if payload.get("type") in ("custom_tool_call", "function_call") and "image_gen" in tool_input:
                details["image_tool"] = tool_input.split("(", 1)[0].split("tools.")[-1].strip()
    return details


def png_size(path: Path) -> list[int] | None:
    header = path.read_bytes()[:24]
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return list(struct.unpack(">II", header[16:24]))


def run_api(args: argparse.Namespace, target: Path) -> tuple[int, dict]:
    cli = cli_path()
    if not cli.exists():
        print(f"Codex's bundled image CLI is missing at {cli}; install or update the codex CLI", file=sys.stderr)
        return 1, {}
    # The CLI assembles the final prompt itself, so a dry run is the only way to record exactly what was sent.
    preview = subprocess.run(build_api_command(cli, args, target, True), text=True, capture_output=True)
    if preview.returncode != 0:
        print((preview.stderr or preview.stdout)[-800:], file=sys.stderr)
        return 1, {}
    if args.dry_run:
        print(preview.stdout.strip())
        return 0, {}

    target.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(build_api_command(cli, args, target, False), text=True, capture_output=True)
    if result.returncode != 0 or not target.exists():
        tail = (result.stderr or result.stdout or "")[-800:]
        print(f"generation failed: {target} was not created\n{tail}", file=sys.stderr)
        return 1, {}
    return 0, {"request": parse_payload(preview.stdout)}


def without_api_key() -> dict[str, str]:
    return {key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"}


def chatgpt_login(codex: str) -> bool:
    # Checked without the key, the way the subscription run itself starts codex.
    try:
        status = subprocess.run(
            [codex, "login", "status"],
            env=without_api_key(),
            stdin=subprocess.DEVNULL,
            text=True,
            capture_output=True,
            timeout=LOGIN_STATUS_TIMEOUT,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return status.returncode == 0 and "chatgpt" in (status.stdout + status.stderr).lower()


def resolve_route(requested: str) -> tuple[str | None, str]:
    if requested != "auto":
        return requested, "requested with --route"
    has_key = bool(os.environ.get("OPENAI_API_KEY"))
    codex = shutil.which("codex")
    if codex and chatgpt_login(codex):
        return "subscription", "codex reports a ChatGPT login"
    why = "codex reports no ChatGPT login" if codex else "codex is not on PATH"
    if has_key:
        return "api", f"{why}, and OPENAI_API_KEY is set"
    return None, (
        f"no route available: {why}, and OPENAI_API_KEY is not set. "
        "Either sign codex in with a paid ChatGPT plan (codex login) for --route subscription, "
        "or export OPENAI_API_KEY for --route api."
    )


def run_subscription(args: argparse.Namespace, target: Path) -> tuple[int, dict]:
    codex = shutil.which("codex")
    if not codex:
        print("codex CLI not found on PATH", file=sys.stderr)
        return 1, {}
    ignored = [flag for flag, value in (("--model", args.model), ("--quality", args.quality)) if value]
    if ignored:
        print(f"note: ignoring {', '.join(ignored)}, which only --route api uses", file=sys.stderr)

    prompt = build_subscription_prompt(args)
    command = build_subscription_command(codex, target.parent, prompt)
    if args.dry_run:
        print("env -u OPENAI_API_KEY " + shlex.join(command) + " < /dev/null")
        return 0, {}

    target.parent.mkdir(parents=True, exist_ok=True)
    # Without the key in the environment codex uses its ChatGPT login, which is what offers the built-in image tool.
    env = without_api_key()
    started = time.monotonic()
    try:
        result = subprocess.run(
            command, env=env, stdin=subprocess.DEVNULL, text=True, capture_output=True, timeout=SUBSCRIPTION_TIMEOUT
        )
    except subprocess.TimeoutExpired:
        print(f"generation failed: codex exec ran past {SUBSCRIPTION_TIMEOUT}s", file=sys.stderr)
        return 1, {}
    seconds = round(time.monotonic() - started, 1)

    thread_id, usage, errors = parse_events(result.stdout)
    folder = codex_home() / "generated_images" / thread_id if thread_id else None
    images = sorted(folder.glob("*.png"), key=lambda p: p.stat().st_mtime) if folder else []
    if result.returncode != 0 or not images:
        tail = "\n".join(errors) or (result.stderr or result.stdout or "")[-800:]
        print(f"generation failed: codex produced no image (thread {thread_id})\n{tail}", file=sys.stderr)
        print("The built-in tool needs a paid ChatGPT login; --route api uses OPENAI_API_KEY instead.", file=sys.stderr)
        return 1, {}

    shutil.copyfile(images[-1], target)
    return 0, {
        "request": {
            "command": shlex.join(command[:-1]) + " <prompt>",
            "prompt": prompt,
            "thread_id": thread_id,
            "source": str(images[-1]),
            "images_in_thread": len(images),
            "seconds": seconds,
            "usage": usage,
            **rollout_details(thread_id),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description", help="what the image should show")
    parser.add_argument("--out", required=True, type=Path, help="save path; missing directories are created")
    parser.add_argument(
        "--route",
        choices=("auto", "subscription", "api"),
        default="auto",
        help="auto (default): subscription when codex has a ChatGPT login, else api when OPENAI_API_KEY is set; "
        "subscription: codex exec on the ChatGPT login; api: the Images API with OPENAI_API_KEY",
    )
    parser.add_argument("--style", default=DEFAULT_STYLE, help="style constraint; pass an empty string to generate without one")
    parser.add_argument("--extra", default="", help="one more constraint line: composition, things to exclude")
    parser.add_argument("--model", default=None, help="image model (api route); the CLI's default applies when omitted")
    parser.add_argument("--size", default=None, help="WIDTHxHEIGHT or auto; exact on the api route, a prompt hint on subscription")
    parser.add_argument("--quality", default=None, help="api route only: low for drafts, medium/high/auto for finals")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = args.out.resolve()
    route, reason = resolve_route(args.route)
    if route is None:
        print(reason, file=sys.stderr)
        return 1
    if args.route == "auto":
        print(f"route: auto -> {route} ({reason})", file=sys.stderr)

    runners = {"subscription": run_subscription, "api": run_api}
    code, record = runners[route](args, target)
    fallback_from = None
    # Only auto falls back, so an explicit --route never spends on a route the caller did not ask for.
    if code != 0 and not args.dry_run and args.route == "auto" and route == "subscription" and os.environ.get("OPENAI_API_KEY"):
        print("route: subscription failed, retrying once with --route api (OPENAI_API_KEY is set)", file=sys.stderr)
        fallback_from, route, reason = "subscription", "api", "subscription produced no image, and OPENAI_API_KEY is set"
        code, record = run_api(args, target)
    if code != 0 or args.dry_run:
        return code

    sidecar = target.with_suffix(target.suffix + ".gen.json")
    sidecar.write_text(
        json.dumps(
            {
                "generated": True,
                "route": route,
                "route_requested": args.route,
                "route_reason": reason,
                **({"fallback_from": fallback_from} if fallback_from else {}),
                "description": args.description,
                "style": args.style,
                "extra": args.extra,
                "pixels": png_size(target),
                **record,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    )

    print(f"{target} ({target.stat().st_size:,} bytes), prompt at {sidecar.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
