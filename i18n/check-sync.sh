#!/bin/bash
# Reports English source files that have no Korean mirror, and Korean mirrors
# that no longer have an English source. The Korean tree under i18n/ko/ is a
# read-only mirror for humans — it is never symlinked into ~/.claude.

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KO="$ROOT/i18n/ko"

missing=0
orphan=0

# English source -> expected Korean mirror
for f in "$ROOT"/rules/*.md "$ROOT"/skills/*/SKILL.md "$ROOT"/agents/*.md "$ROOT"/hooks/*.md; do
  [ -e "$f" ] || continue
  rel="${f#"$ROOT"/}"
  if [ ! -f "$KO/$rel" ]; then
    echo "missing mirror: i18n/ko/$rel"
    missing=$((missing + 1))
  fi
done

# Korean mirror -> must have an English source
while IFS= read -r kf; do
  rel="${kf#"$KO"/}"
  if [ ! -f "$ROOT/$rel" ]; then
    echo "orphan mirror (no English source): i18n/ko/$rel"
    orphan=$((orphan + 1))
  fi
done < <(find "$KO" -name '*.md' -type f)

if [ "$missing" -eq 0 ] && [ "$orphan" -eq 0 ]; then
  echo "in sync: every English file has a Korean mirror and vice versa."
else
  echo "out of sync: $missing missing, $orphan orphan."
  exit 1
fi
