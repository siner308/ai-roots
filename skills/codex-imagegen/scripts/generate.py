#!/usr/bin/env python3
"""Generate one raster image through the image CLI that ships with the Codex CLI."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_STYLE = "Do not make it photorealistic. Use a painterly or diagrammatic style."


def cli_path() -> Path:
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    return home / "skills" / ".system" / "imagegen" / "scripts" / "image_gen.py"


def build_command(cli: Path, args: argparse.Namespace, target: Path, dry_run: bool) -> list[str]:
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


def parse_payload(stdout: str) -> object:
    start = stdout.find("{")
    if start < 0:
        return stdout.strip()
    try:
        return json.loads(stdout[start:])
    except json.JSONDecodeError:
        return stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description", help="what the image should show")
    parser.add_argument("--out", required=True, type=Path, help="save path; missing directories are created")
    parser.add_argument("--style", default=DEFAULT_STYLE, help="style constraint; pass an empty string to generate without one")
    parser.add_argument("--extra", default="", help="one more constraint line: composition, things to exclude")
    parser.add_argument("--model", default=None, help="image model; the CLI's default applies when omitted")
    parser.add_argument("--size", default=None, help="WIDTHxHEIGHT or auto")
    parser.add_argument("--quality", default=None, help="low for drafts, medium/high/auto for finals")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cli = cli_path()
    if not cli.exists():
        print(f"Codex's bundled image CLI is missing at {cli}; install or update the codex CLI", file=sys.stderr)
        return 1

    target = args.out.resolve()
    # The CLI assembles the final prompt itself, so a dry run is the only way to record exactly what was sent.
    preview = subprocess.run(build_command(cli, args, target, True), text=True, capture_output=True)
    if preview.returncode != 0:
        print((preview.stderr or preview.stdout)[-800:], file=sys.stderr)
        return 1
    if args.dry_run:
        print(preview.stdout.strip())
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(build_command(cli, args, target, False), text=True, capture_output=True)
    if result.returncode != 0 or not target.exists():
        tail = (result.stderr or result.stdout or "")[-800:]
        print(f"generation failed: {target} was not created\n{tail}", file=sys.stderr)
        return 1

    sidecar = target.with_suffix(target.suffix + ".gen.json")
    sidecar.write_text(
        json.dumps(
            {
                "generated": True,
                "description": args.description,
                "style": args.style,
                "extra": args.extra,
                "request": parse_payload(preview.stdout),
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
