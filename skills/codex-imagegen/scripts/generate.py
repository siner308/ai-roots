#!/usr/bin/env python3
"""Generate one raster image by delegating to the Codex CLI's imagegen skill."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def build_prompt(description: str, destination: Path, style: str, extra: str) -> str:
    constraints = [f"- {line}" for line in filter(None, [style, extra])]
    body = "\n".join(constraints)
    return f"""Use the imagegen skill to produce one image.

Subject: {description}

{body}

Save the finished file to {destination}. Do nothing else."""


def resolve_target(out: Path, workspace: Path) -> tuple[Path, Path]:
    """Return (absolute target, workspace codex may write to)."""
    workspace = workspace.resolve()
    target = (out if out.is_absolute() else workspace / out).resolve()
    # workspace-write confines codex to this tree; for a target outside it codex still generates the image but leaves it in ~/.codex/generated_images/.
    inside = workspace in target.parents
    return target, workspace if inside else target.parent


def run(prompt: str, workspace: Path, model: str | None) -> subprocess.CompletedProcess:
    command = [
        "codex", "exec", "--skip-git-repo-check",
        "--sandbox", "workspace-write", "--color", "never",
        "--cd", str(workspace), "-",
    ]
    if model:
        command[-1:-1] = ["--model", model]
    return subprocess.run(command, input=prompt, text=True, capture_output=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("description", help="what the image should show")
    parser.add_argument("--out", required=True, type=Path, help="save path — absolute, or relative to the workspace")
    parser.add_argument("--workspace", type=Path, default=Path.cwd(), help="where codex runs; widened when --out falls outside it")
    parser.add_argument(
        "--style",
        default="Do not make it photorealistic. Use a painterly or diagrammatic style.",
        help="style constraint; pass an empty string to generate without one",
    )
    parser.add_argument("--extra", default="", help="one more constraint line — composition, things to exclude")
    parser.add_argument("--model", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target, workspace = resolve_target(args.out, args.workspace)
    prompt = build_prompt(args.description, target, args.style, args.extra)
    if args.dry_run:
        print(prompt)
        return 0

    workspace.mkdir(parents=True, exist_ok=True)
    result = run(prompt, workspace, args.model)
    if not target.exists():
        tail = (result.stderr or result.stdout or "")[-800:]
        print(f"generation failed: {target} was not created\n{tail}", file=sys.stderr)
        return 1

    print(f"{target} ({target.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
