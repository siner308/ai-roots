# CSS Discipline

Write CSS so the cascade and box model are predictable. Most "tricky" CSS bugs — invisible spacing doublings, broken flex shrink, overlay overflow, specificity wars — happen when the codebase leaves common axes open. Close them.

This applies everywhere CSS exists: vanilla, React, Next.js, Svelte, Vue, raw HTML. Framework-specific bindings (Tailwind class names, scoped styles, CSS Modules) live in the project's supplement.

**When normative.** R1–R9 are authoring constraints when editing stylesheets, scoped styles, inline `style=""`, or CSS-adjacent JS. In tasks that do not touch styles, treat them as background knowledge — do not refactor untouched CSS just because it violates a rule.

## Core axes

- **Cascade** — keep specificity boring and override control intact.
- **Box model** — single mechanism for spacing; overflow declared only when clipping or scroll is the intent.
- **Unit discipline** — every value comes from a named set declared once.
- **Style location** — decide upfront where each kind of style belongs.

## R1 — Use a closed spacing scale

All authored spacing (padding, gap, positioned offsets, layout-sized width/height) comes from a finite set declared once in the token or utility layer. New values enter through the exception procedure below, not the call site.

Fixed-pixel chrome dimensions (icon sizes, button tap targets) are fine when they are in the set. Outside the set → declare a named token first, consume via `var()`.

*Why.* When spacing is open-ended, a child with `margin-top: 8px` next to a parent with `gap: 8px` silently produces 16px and nothing in the source signals the doubling.

## R2 — Use padding + gap for spacing; reserve margin for alignment

Spacing between siblings lives on the parent (`padding`) and on the container (`gap`). Margin exists for one job: axial auto-centering (`margin: auto`, `margin-inline: auto`, `margin-block: auto`).

Keep user-agent default margin resets in one designated base layer. Avoid every other author margin declaration. If you want `margin-top: 8px` on a child, bump the parent's `gap` instead.

*Why.* `padding + gap` localizes spacing decisions to the container. Mixed-in child margins double silently.

## R3 — Keep override control: no `!important`

When a CSS rule loses a cascade battle, fix it upstream, not in the cascade.

The most common cause is JS writing inline `element.style.*` that CSS cannot beat. Refactor JS to bind per-instance values via `element.style.setProperty('--custom-prop', value)` — the stylesheet still owns the cascade, JS only supplies the value. For `<canvas>`, JS owns the backing-store attributes (`width`/`height`); CSS owns the rendered box (`.style.width` / `.style.height`).

**Last-resort carve-out.** Third-party styles you cannot modify and cannot fork: a single narrowly-scoped `!important` is acceptable with a one-line comment naming the upstream source so the declaration can be retired when that source changes.

*Why.* `!important` wins once but surrenders override control permanently — every later layer needs `!important` too.

## R4 — Declare `overflow` only when clipping or scroll is the intent

The CSS default (`visible`) serves most layouts. Declare `overflow: clip` (preferred over `hidden` — no scroll container, no new stacking context) when clipping is the *intended* behavior. Declare `overflow: auto` for scroll.

For flex/grid children overflowing their parent, reach for R5 (`min-*: 0`) instead. Hidden-overflow hides the layout bug; the shrink contract fixes it.

*Why.* Most tricky overflow bugs come from reaching for `overflow: hidden` reflexively to cover a sizing problem.

## R5 — Enable flex/grid shrink with `min-*: 0`

A flex or grid item that must shrink below its intrinsic size needs `min-width: 0` (or `min-height: 0`). Browsers default these to `auto` on flex items, blocking shrink.

For replaced elements (`<canvas>`, `<img>`, `<video>`, `<iframe>`) with intrinsic dimensions: either size them fully via CSS (remove inline JS-set dimensions, see R3), or wrap them in an `aspect-ratio` container with `overflow: clip`. For aspect-preserving shrink, set **one axis** and let `aspect-ratio` derive the other.

*Why.* Flex-item `min-width: auto` equals min-content. A canvas with inline 768×512 size reports that as min-content, which `flex-shrink` cannot go below.

## R6 — Use color tokens for authored design

All authored colors reference named tokens (`var(--color-*)`). Use `color-mix(in oklch, var(--color-a) N%, transparent)` for modulations — the arguments stay tokens, the percentage varies.

Avoid hex, `rgb()`, `rgba()`, `hsl()`, `oklch()`, and `color-mix(...)` with literal arguments in component source.

**Non-CSS consumers carve-out.** Render paths that cannot resolve `var()` — canvas 2D, WebGL, server-rendered SVG for email, PDF export — legitimately need literal color fallbacks. Project supplement names which paths qualify.

*Why.* Tokens localize design changes to one file.

## R7 — Place styles in the layer that owns them

Three layers, each with a narrow role.

- **Utility layer** (Tailwind, BEM globals, CSS Modules, hand-rolled atoms) — repeating layout, spacing, typography, token-based color. Default home for style that recurs.
- **Component-scoped layer** (Svelte `<style>`, CSS Modules, Vue SFC, scoped styled-components) — pseudo-classes, nested selectors, `:has()`, SVG internals, anything spanning multiple elements in the same template.
- **Inline `style=""`** — two valid uses: per-instance custom properties (`style="--row-accent: ..."` consumed by the scoped layer), or a single token reference on a single element (`style="color: var(--color-text);"`). Anything more substantial is a component waiting to be written.

**Decision tree.** (1) Existing utility class? → utility. (2) Pseudo-class / nested / structural? → scoped. (3) Per-instance value? → inline custom property + scoped consumer. (4) One-off single token reference? → inline `style`. (5) Need a literal? → stop, add the token first.

## R8 — Use named z-index tokens

```css
--z-base: 0;  --z-overlay: 10;  --z-hud: 20;  --z-modal: 30;
```

Consume via `z-index: var(--z-overlay)`. Add new levels to the token file when a genuinely new stacking layer appears. Avoid raw numeric `z-index` — `9999` becomes `99999` tomorrow.

## R9 — Scale with viewport and user font-size

The user controls two variables: device (viewport) and typography preference. Respect both.

- `rem` for typography and type-coupled values (font-size, line-height, type-driven padding/gap) — scales with user font-size preference (WCAG 1.4.4).
- Layout primitives (`%`, `fr`, `gap`, `clamp()`, media/container queries) for viewport-responsive layouts.
- `px` for chrome widgets (borders, hairlines, icon-box dimensions) where literal pixels are the intent.
- `vw`/`vh`/`svh` on the outermost shell only.

## Exception procedure — adding to a closed set

When you genuinely need a value outside an existing set:

1. Pause at the call site. Do not reach for `!important`, a bracket utility, or a literal.
2. Identify the set (spacing, color, motion, z-index).
3. Check the prior-decision log — the need may already be covered.
4. Add to the token layer. Name for intent (`--spacing-card-inset`), not value.
5. Land token + first consumer in one atomic commit.

If the token layer does not yet exist, declare it first: survey existing literals, cluster into an intentional scale, land as its own commit. Until then, treat R1–R9 as aspirations.

## Enforcement signals (review heuristics)

Starting points for investigation, not automatic rejections. Carve-outs above (R3 third-party, R6 non-CSS consumers) remain legitimate.

- `!important` anywhere in authored source without an R3 comment.
- Color literals (hex, `rgb(`, `rgba(`, `hsl(`, `oklch(`) in component source.
- Direction-specific margin outside the base reset layer or `margin: auto` family.
- Raw numeric `z-index`.
- JS writing `element.style.width` / `.style.height` (except via `setProperty('--*', value)`).
- Utility-framework arbitrary-value brackets (`-\[.*\]`) without a documented carve-out.

Framework-specific greps (Tailwind prefixes, Svelte file targeting, `.module.css` patterns) live in the project supplement.

## Project supplement

These rules describe the universal shape. Each project pins concrete bindings: which utility framework, the spacing/color/motion sets, the token-layer file, the base-reset file, the local greps. When project ergonomics conflict with these rules, project loses — framework conveniences do not override the underlying discipline.
