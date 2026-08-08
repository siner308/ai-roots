---
name: codex-imagegen
description: "Generate raster images — illustrations, textures, diagrams, mockups, sprites, backgrounds — by delegating to the Codex CLI's imagegen skill from a Claude session. Use whenever a task needs a bitmap asset that does not exist yet and cannot be drawn as code or vector. Requires the codex CLI on PATH."
---

# Codex imagegen

Claude cannot generate raster images, Codex can through its bundled `imagegen` skill, and `codex exec` takes a prompt on stdin — so a Claude session can drive it without a human sitting in an interactive Codex session.

## Run it

```bash
python <skill-dir>/scripts/generate.py "그릴 내용" \
  --out assets/hero.png --workspace /path/to/project
```

The script prints the written path and its size, and exits non-zero when the file did not appear. `--dry-run` prints the prompt without spending a call. `--style` replaces the default style constraint (pass `""` to drop it), `--extra` adds one constraint line, `--model` overrides the Codex model.

## Why the script and not a raw codex call

Two flags are mandatory, and getting either wrong fails in a way that looks like a broken skill rather than a misconfigured call.

- `--sandbox workspace-write` — imagegen writes a file, and under `read-only` the run reports success while producing nothing.
- `--skip-git-repo-check` — codex refuses to start outside a trusted directory, and asset work often happens in a scratch directory that is not a git repo.

## Writing the prompt

Describe what should be visible, not what it is for. "눈보라에 갇힌 기지 건물 한 채, 창문에서 희미한 불빛" beats "고립을 보여주는 이미지".

Constrain what must not appear. Generated images drift toward recognisable real places, real people's faces, and institutional logos unless told otherwise. State the aspect ratio when it matters — the default prompt does not assume one.

## The style constraint exists for a reason

The default tells the model not to produce a photorealistic result, because a photorealistic generated image reads as documentary footage. In factual video and news contexts that misleads the viewer about what is a record and what is an illustration, and YouTube's synthetic-content disclosure obligation targets photorealistic material specifically.

Drop it with `--style ""` only when photorealism is the point — a product mockup, a texture, a game asset — and nothing around the image presents it as a record.

## After generating

Look at the file before using it. The model returns a plausible image for almost any prompt, and a plausible image is not necessarily the one described: a "roller compacting snow" prompt can come back as a snowplough. Reading the file shows it; the filename does not.

Where the project keeps an asset catalog, record the file there with its prompt and a generated flag, so a later reader can tell which frames are illustrations.
