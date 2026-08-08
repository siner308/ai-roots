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
    return f"""imagegen skill로 이미지 한 장을 만들어 주세요.

내용: {description}

{body}

완성한 파일을 {destination} 경로에 저장해 주세요. 다른 작업은 하지 마세요."""


def run(prompt: str, workspace: Path, model: str | None) -> subprocess.CompletedProcess:
    # imagegen이 파일을 쓰므로 read-only 샌드박스로는 실패하고, 작업공간이 git 저장소가 아닐 수 있어 검사도 건너뛴다.
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
    parser.add_argument("description", help="그릴 내용")
    parser.add_argument("--out", required=True, type=Path, help="작업공간 기준 저장 경로")
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument(
        "--style",
        default="photorealistic으로 만들지 않는다. 회화적이거나 도해적인 양식이어야 한다.",
        help="양식 제약. 빈 문자열이면 제약 없이 생성한다",
    )
    parser.add_argument("--extra", default="", help="구도·금지 대상 등 추가 제약 한 줄")
    parser.add_argument("--model", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    prompt = build_prompt(args.description, args.out, args.style, args.extra)
    if args.dry_run:
        print(prompt)
        return 0

    result = run(prompt, workspace, args.model)
    target = workspace / args.out
    if not target.exists():
        tail = (result.stderr or result.stdout or "")[-800:]
        print(f"생성 실패: {target} 이 만들어지지 않았습니다\n{tail}", file=sys.stderr)
        return 1

    print(f"{target} ({target.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
