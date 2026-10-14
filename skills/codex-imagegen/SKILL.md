---
name: codex-imagegen
description: "Generate a raster image (illustration, texture, diagram, mockup, sprite, background, thumbnail, icon) through the Codex CLI. Apply when the request asks to draw, generate, or make an image, or names a missing `.png`/`.jpg`/`.webp` asset to create. Needs either the codex CLI signed in with a paid ChatGPT plan, or `OPENAI_API_KEY` with the `openai` Python package; the default `--route auto` picks whichever is available."
---

# Codex imagegen

Claude cannot generate raster images. The Codex CLI can, by two routes, and `scripts/generate.py` drives either one:

- `--route subscription` runs `codex exec` on the ChatGPT login and has the agent call Codex's built-in image tool once. It uses the ChatGPT login instead of API credits; its exact effect on the plan's billing or usage limits is unconfirmed.
- `--route api` calls `~/.codex/skills/.system/imagegen/scripts/image_gen.py`, a thin Images API client that needs `OPENAI_API_KEY` and the `openai` package, with no language model in between. It behaves exactly as this script did before the subscription route existed: same flags, same defaults, same output.
- `--route auto` (default) picks subscription when `codex` is on `PATH` and `codex login status` reports a ChatGPT login, otherwise api when `OPENAI_API_KEY` is set, otherwise exits with a message naming both options. It prints the choice and the reason on stderr.

When auto picked subscription and that run fails (codex error, timeout, no image) while `OPENAI_API_KEY` is set, the script retries once on the api route and records `"fallback_from": "subscription"` in the sidecar. An explicit `--route subscription` or `--route api` never falls back, so it never spends on a route the caller did not ask for.

## Run it

```bash
python ~/.claude/skills/codex-imagegen/scripts/generate.py "what the image should show" \
  --out ~/Desktop/hero.png
```

`--out` takes any path, absolute or relative to the current directory, and missing directories are created. The script prints the written path and its size, and exits non-zero when the file did not appear.

Every image gets a `<name>.gen.json` sidecar holding the route used (`route`, plus `route_requested`, `route_reason` and any `fallback_from`), the description, the style constraints, the pixel size, and the request that produced it. On disk a generated image is indistinguishable from a photograph, so this is what lets you say months later which is which, and what a catalog or credit line reads from.

`--dry-run` prints the request without spending a call: the `codex exec` command on the subscription route, the CLI's assembled request on the api route. With `--route auto` it also prints on stderr which route auto would pick and why. `--style` replaces the default style constraint (pass `""` to drop it) and `--extra` adds one constraint line on both routes.

`--size`, `--quality` and `--model` are exact only on the api route (`--quality low` for drafts; square sizes such as `1024x1024` come back fastest). On the subscription route `--size` becomes a line in the prompt, which the tool treats as a hint (a `1024x1024` request came back 1254x1254), and `--quality` and `--model` are ignored with a note.

## How the subscription route works

The script removes `OPENAI_API_KEY` from the child environment so codex runs on its ChatGPT login; API-key auth does not get the built-in tool. It runs `codex exec --json --sandbox read-only` with stdin closed, so the agent cannot write anywhere and the run cannot wait on input. The tool is only offered to a paid ChatGPT plan; with a free plan the run ends with "The built-in image generator is unavailable in this session" and no file.

Codex saves the image to `~/.codex/generated_images/<thread_id>/exec-*.png`. The script reads the thread id from the `thread.started` event, copies that file to `--out` itself, and fails when the folder holds no image. The model and tool names come from the session rollout under `~/.codex/sessions`, since the JSON stream does not carry them.

One test took about 31 seconds and two model calls (about 70k input tokens, half of them cached). The prompt tells the agent not to read files: an earlier run without that line opened Codex's imagegen skill first and took four model calls and about 206k input tokens.

If the api route reports that the `openai` SDK is missing, install it into the interpreter that runs the script: `python3 -m pip install openai`.

## Writing the prompt

Describe what should be visible, not what it is for. "one station building in a blizzard, a faint light in the window" beats "an image conveying isolation".

Constrain what must not appear. Generated images drift toward recognisable real places, real people's faces, and institutional logos unless told otherwise. State the aspect ratio when it matters, in the prompt or with `--size`.

## The style constraint exists for a reason

The default tells the model not to produce a photorealistic result, because a photorealistic generated image reads as documentary footage. In factual video and news contexts that misleads the viewer about what is a record and what is an illustration, and YouTube's synthetic-content disclosure obligation targets photorealistic material specifically.

Drop it with `--style ""` only when photorealism is the point, such as a product mockup, a texture, or a game asset, and nothing around the image presents it as a record.

## After generating

Look at the file before using it; the filename cannot tell you what is in it. The model returns a plausible image for almost any prompt, and a plausible image is not necessarily the one described: a "roller compacting snow" prompt can come back as a snowplough.

Where the project keeps an asset catalog, record the file there with its prompt and a generated flag, so a later reader can tell which frames are illustrations.
