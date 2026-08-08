---
name: codex-imagegen
description: "Generate a raster image — illustration, texture, diagram, mockup, sprite, background, thumbnail, icon — by delegating to the Codex CLI's imagegen skill. Apply when the request asks to draw, generate, or make an image, or names a missing `.png`/`.jpg`/`.webp` asset to create. Requires the codex CLI on PATH."
---

# Codex imagegen

Claude는 raster 이미지를 만들지 못하지만 Codex는 내장된 `imagegen` skill로 만들 수 있고, `codex exec`는 prompt를 stdin으로 받습니다. 그래서 사람이 대화형 Codex 세션에 앉아 있지 않아도 Claude 세션이 Codex를 몰아서 쓸 수 있어요.

## 실행

```bash
python ~/.claude/skills/codex-imagegen/scripts/generate.py "what the image should show" \
  --out ~/Desktop/hero.png
```

`--out`은 아무 경로나 받습니다 — 절대경로거나, `--workspace` 기준 상대경로입니다(`--workspace`의 기본값은 현재 디렉터리). 없는 디렉터리는 만들어 주니 새 출력 폴더를 미리 준비할 필요가 없습니다.

스크립트는 쓰인 경로와 크기를 출력하고, 파일이 안 생기면 0이 아닌 코드로 끝납니다. `--dry-run`은 호출 없이 prompt만 보여줍니다. `--style`은 기본 양식 제약을 갈아끼우고(빈 문자열이면 제약을 뺍니다), `--extra`는 제약 한 줄을 더하고, `--model`은 Codex 모델을 바꿉니다.

## codex를 직접 부르지 않고 스크립트를 두는 이유

flag 두 개가 필수인데, 둘 중 하나만 틀려도 잘못 부른 게 아니라 skill이 망가진 것처럼 보이는 방식으로 실패합니다.

- `--sandbox workspace-write` — imagegen은 파일을 쓰는데, `read-only`에서는 아무것도 안 만들면서 성공했다고 보고합니다.
- `--skip-git-repo-check` — codex는 신뢰된 디렉터리 밖에서 시작을 거부하는데, 자산 작업은 git 저장소가 아닌 임시 디렉터리에서 하는 일이 많습니다.

`--out`을 그대로 넘기지 않는 이유도 같은 sandbox입니다. workspace 밖 경로면 codex가 이미지는 만들어 놓고 거기로 옮기지 못해 `~/.codex/generated_images/`에 남기기 때문에, 스크립트가 workspace를 대상 파일의 디렉터리까지 넓힙니다.

## prompt 쓰는 법

용도가 아니라 화면에 보일 것을 적으세요. "눈보라 속 기지 건물 한 채, 창문의 희미한 불빛"이 "고립을 보여주는 이미지"보다 낫습니다.

나오면 안 되는 것을 제약으로 걸어두세요. 생성된 이미지는 따로 말하지 않으면 알아볼 수 있는 실제 장소, 실존 인물의 얼굴, 기관 로고 쪽으로 흘러갑니다. 화면비가 중요하면 명시하세요 — 기본 prompt는 화면비를 가정하지 않습니다.

## 양식 제약이 기본으로 있는 이유

기본값은 photorealistic으로 만들지 말라고 지시합니다. photorealistic한 생성 이미지는 기록 영상처럼 읽히기 때문이에요. 사실을 다루는 영상이나 뉴스 맥락에서는 무엇이 기록이고 무엇이 삽화인지 시청자를 오도하고, YouTube의 합성 콘텐츠 고지 의무도 photorealistic한 자료를 겨냥합니다.

`--style ""`로 제약을 빼는 건 photorealism 자체가 목적일 때만입니다 — 제품 mockup, texture, 게임 자산 — 그리고 이미지 주변 어디에도 그걸 기록인 것처럼 제시하지 않을 때요.

## 만든 다음

쓰기 전에 파일을 직접 보세요 — 파일 이름은 안에 뭐가 들었는지 알려주지 못합니다. 모델은 거의 어떤 prompt에도 그럴듯한 이미지를 돌려주는데, 그럴듯한 이미지가 곧 설명한 그 이미지는 아닙니다. "눈을 다지는 roller" prompt가 제설차로 돌아올 수 있어요.

프로젝트가 자산 목록을 관리한다면 그 파일을 prompt와 생성 표시와 함께 기록해 두세요. 나중에 읽는 사람이 어느 장면이 삽화인지 구분할 수 있습니다.
