#!/usr/bin/env python3
"""Hook installer, split out from install.sh because registration is a JSON
merge bash can't do safely.

Idempotent on purpose so install.sh can call it every run: re-linking adds no
duplicate symlink and the merge skips a hook whose command is already present.
settings.json is backed up before any write because it holds live machine config.

Usage: register.py <hooks_src_dir> <home_dir>
"""
import json
import os
import shutil
import sys
import time


def relink(src, dst):
    if os.path.islink(dst):
        os.remove(dst)
    elif os.path.exists(dst):
        shutil.move(dst, f"{dst}.bak.{time.strftime('%Y%m%d%H%M%S')}")
    os.symlink(src, dst)


def main():
    hooks_src, home = sys.argv[1], sys.argv[2]
    manifest = json.load(open(os.path.join(hooks_src, "manifest.json")))

    hooks_dst = os.path.join(home, ".claude", "hooks")
    os.makedirs(hooks_dst, exist_ok=True)

    for script in {e["script"] for e in manifest}:
        src, dst = os.path.join(hooks_src, script), os.path.join(hooks_dst, script)
        relink(src, dst)
        print(f"linked hook: {src} -> {dst}")

    settings_path = os.path.join(home, ".claude", "settings.json")
    settings = json.load(open(settings_path)) if os.path.exists(settings_path) else {}
    hooks_cfg = settings.setdefault("hooks", {})

    changed = False
    for e in manifest:
        command = f"{e['run']} {os.path.join(hooks_dst, e['script'])}"
        groups = hooks_cfg.setdefault(e["event"], [])
        if any(h.get("command") == command for g in groups for h in g.get("hooks", [])):
            continue
        group = next((g for g in groups if g.get("matcher") == e["matcher"]), None)
        if group is None:
            group = {"matcher": e["matcher"], "hooks": []}
            groups.append(group)
        group["hooks"].append({"type": "command", "command": command})
        changed = True
        print(f"registered hook: {e['event']} {e['matcher']} -> {command}")

    if not changed:
        print("hooks already registered; settings.json unchanged")
        return 0

    if os.path.exists(settings_path):
        shutil.copy2(settings_path, f"{settings_path}.bak.{time.strftime('%Y%m%d%H%M%S')}")
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
