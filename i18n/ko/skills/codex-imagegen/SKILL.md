---
name: codex-imagegen
description: "Generate a raster image (illustration, texture, diagram, mockup, sprite, background, thumbnail, icon) through the image CLI bundled with the Codex CLI. Apply when the request asks to draw, generate, or make an image, or names a missing `.png`/`.jpg`/`.webp` asset to create. Requires the codex CLI installed, the `openai` Python package, and `OPENAI_API_KEY`."
---

# Codex imagegen

Claude는 raster 이미지를 만들지 못합니다. Codex CLI에는 만들 수 있는 도구가 하나 들어 있어요. `~/.codex/skills/.system/imagegen/scripts/image_gen.py`인데, Images API를 얇게 감싼 client라 `OPENAI_API_KEY`와 `openai` 패키지만 있으면 됩니다. 이걸 직접 부르면 Claude 세션이 중간에 모델을 끼우지 않고 이미지를 만들 수 있습니다.

## 실행

```bash
python ~/.claude/skills/codex-imagegen/scripts/generate.py "what the image should show" \
  --out ~/Desktop/hero.png
```

`--out`은 절대경로든 현재 디렉터리 기준 상대경로든 아무 경로나 받고, 없는 디렉터리는 만들어 줍니다. 스크립트는 쓰인 경로와 크기를 출력하고 파일이 안 생기면 0이 아닌 코드로 끝납니다.

이미지마다 `<name>.gen.json` sidecar가 같이 생깁니다. 설명, 양식 제약, 그리고 CLI가 실제로 보낸 요청(모델, 크기, 품질, 조립된 prompt)이 들어 있어요. 디스크 위의 생성 이미지는 사진과 구분이 안 되니, 몇 달 뒤에 어느 게 어느 건지 말해 주는 근거이자 자산 목록이나 크레딧이 읽는 자료가 이 파일입니다.

`--dry-run`은 호출 없이 요청만 보여줍니다. `--style`은 기본 양식 제약을 갈아끼우고(빈 문자열이면 제약을 뺍니다), `--extra`는 제약 한 줄을 더하고, `--size`와 `--quality`는 CLI로 그대로 넘어가며(초안은 `--quality low`, `1024x1024` 같은 정사각형이 가장 빨리 나옵니다), `--model`은 이미지 모델을 바꿉니다.

CLI가 `openai` SDK가 없다고 하면 스크립트를 실행하는 인터프리터에 설치하세요: `python3 -m pip install openai`.

## `codex exec` 대신 번들 CLI를 쓰는 이유

Codex에는 내장 `image_gen` tool도 있고, 이 skill의 이전 버전은 `codex exec`로 그걸 몰아 썼습니다. 기본 OpenAI provider에서 그 tool은 유료 ChatGPT 플랜으로 로그인한 세션에만 열립니다. API 키 인증이나 무료 플랜에서는 조용히 빠지고, 실행은 "The built-in image generator is unavailable in this session"이라는 답과 함께 파일 없이 끝나요. 번들 CLI에는 그런 관문이 없고, 언어 모델 왕복도 없으며, 파일을 `--out`이 가리키는 곳에 정확히 놓습니다.

그래도 CLI를 직접 부르는 대신 스크립트를 두는 이유는 있습니다. CLI 설치 경로를 찾아 주고, 설명과 제약을 CLI의 prompt 필드에 대응시키고, 기존 파일이 있을 때 거부되지 않고 덮어쓰도록 `--force`를 넘기고, sidecar를 써 줍니다.

## prompt 쓰는 법

용도가 아니라 화면에 보일 것을 적으세요. "눈보라 속 기지 건물 한 채, 창문의 희미한 불빛"이 "고립을 보여주는 이미지"보다 낫습니다.

나오면 안 되는 것을 제약으로 걸어두세요. 생성된 이미지는 따로 말하지 않으면 알아볼 수 있는 실제 장소, 실존 인물의 얼굴, 기관 로고 쪽으로 흘러갑니다. 화면비가 중요하면 prompt나 `--size`로 명시하세요.

## 양식 제약이 기본으로 있는 이유

기본값은 photorealistic으로 만들지 말라고 지시합니다. photorealistic한 생성 이미지는 기록 영상처럼 읽히기 때문이에요. 사실을 다루는 영상이나 뉴스 맥락에서는 무엇이 기록이고 무엇이 삽화인지 시청자를 오도하고, YouTube의 합성 콘텐츠 고지 의무도 photorealistic한 자료를 겨냥합니다.

`--style ""`로 제약을 빼는 건 제품 mockup, texture, 게임 자산처럼 photorealism 자체가 목적일 때, 그리고 이미지 주변 어디에도 그걸 기록인 것처럼 제시하지 않을 때만입니다.

## 만든 다음

쓰기 전에 파일을 직접 보세요. 파일 이름은 안에 뭐가 들었는지 알려주지 못합니다. 모델은 거의 어떤 prompt에도 그럴듯한 이미지를 돌려주는데, 그럴듯한 이미지가 곧 설명한 그 이미지는 아닙니다. "눈을 다지는 roller" prompt가 제설차로 돌아올 수 있어요.

프로젝트가 자산 목록을 관리한다면 그 파일을 prompt와 생성 표시와 함께 기록해 두세요. 나중에 읽는 사람이 어느 장면이 삽화인지 구분할 수 있습니다.
