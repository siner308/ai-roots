---
name: codex-imagegen
description: "Generate a raster image (illustration, texture, diagram, mockup, sprite, background, thumbnail, icon) through the image CLI bundled with the Codex CLI. Apply when the request asks to draw, generate, or make an image, or names a missing `.png`/`.jpg`/`.webp` asset to create. Requires the codex CLI installed, the `openai` Python package, and `OPENAI_API_KEY`."
---

# Codex imagegen

Claude cannot generate raster images. The Codex CLI ships one that can: `~/.codex/skills/.system/imagegen/scripts/image_gen.py`, a thin client for the Images API that needs only `OPENAI_API_KEY` and the `openai` package. Calling it directly gives a Claude session image generation with no model in between.

## Run it

```bash
python ~/.claude/skills/codex-imagegen/scripts/generate.py "what the image should show" \
  --out ~/Desktop/hero.png
```

`--out` takes any path, absolute or relative to the current directory, and missing directories are created. The script prints the written path and its size, and exits non-zero when the file did not appear.

Every image gets a `<name>.gen.json` sidecar holding the description, the style constraints, and the exact request the CLI sent (model, size, quality, assembled prompt). On disk a generated image is indistinguishable from a photograph, so this is what lets you say months later which is which, and what a catalog or credit line reads from.

`--dry-run` prints the request without spending a call. `--style` replaces the default style constraint (pass `""` to drop it), `--extra` adds one constraint line, `--size` and `--quality` pass through to the CLI (`--quality low` for drafts; square sizes such as `1024x1024` come back fastest), and `--model` overrides the image model.

If the CLI reports that the `openai` SDK is missing, install it into the interpreter that runs the script: `python3 -m pip install openai`.

## Why the bundled CLI and not `codex exec`

Codex also has a built-in `image_gen` tool, and an earlier version of this skill drove it through `codex exec`. With the stock OpenAI provider that tool is only offered to sessions signed in with a paid ChatGPT plan: with API-key auth or a free plan it is silently absent, and the run ends with "The built-in image generator is unavailable in this session" and no file. The bundled CLI has no such gate, skips the language-model round trip, and puts the file exactly where `--out` says.

The script still earns its place over a raw CLI call: it resolves the CLI's install path, maps the description and constraints onto the CLI's prompt fields, passes `--force` so an existing file is replaced rather than refused, and writes the sidecar.

## Writing the prompt

Describe what should be visible, not what it is for. "one station building in a blizzard, a faint light in the window" beats "an image conveying isolation".

Constrain what must not appear. Generated images drift toward recognisable real places, real people's faces, and institutional logos unless told otherwise. State the aspect ratio when it matters, in the prompt or with `--size`.

## The style constraint exists for a reason

The default tells the model not to produce a photorealistic result, because a photorealistic generated image reads as documentary footage. In factual video and news contexts that misleads the viewer about what is a record and what is an illustration, and YouTube's synthetic-content disclosure obligation targets photorealistic material specifically.

Drop it with `--style ""` only when photorealism is the point, such as a product mockup, a texture, or a game asset, and nothing around the image presents it as a record.

## After generating

Look at the file before using it; the filename cannot tell you what is in it. The model returns a plausible image for almost any prompt, and a plausible image is not necessarily the one described: a "roller compacting snow" prompt can come back as a snowplough.

Where the project keeps an asset catalog, record the file there with its prompt and a generated flag, so a later reader can tell which frames are illustrations.
