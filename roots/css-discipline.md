# CSS Discipline

Write CSS so the cascade and box model are predictable. Most "tricky" CSS bugs — invisible spacing doublings, broken flex shrink, overlay overflow, specificity wars — happen when the codebase leaves common axes open. Close them.

This applies everywhere CSS exists: vanilla projects, React, Next.js, Svelte, Vue, raw HTML. The underlying principles — closed token sets, single-source spacing, predictable cascade — are framework-agnostic. Framework-specific bindings (Tailwind class names, Svelte scoped styles, CSS Modules) live in the project's own supplement.

**When this rule is normative.** R1–R8 are authoring constraints when editing stylesheets, component-scoped styles, inline `style=""`, or CSS-adjacent JS (`element.style.*`, class toggling, CSS-in-JS). In tasks that do not touch styles, treat them as background knowledge rather than a checklist — do not refactor untouched CSS just because it violates a rule.

## Core principles

Four axes need positive conventions:

- **Cascade** — keep specificity boring and override control intact.
- **Box model** — a single mechanism for spacing; one named purpose when hiding overflow.
- **Unit discipline** — every value comes from a named set declared once.
- **Style location** — decide upfront where each kind of style belongs.

## R1 — Use a closed spacing scale

All authored spacing (padding, gap, positioned top/right/bottom/left, layout-sized width/height) comes from a finite set declared once in the project's token or utility layer. New values enter the set through the exception procedure, not at the call site.

**Do**
- Use the project's declared spacing scale (e.g. `{0, 4, 8, 16, 32, 64}` px registered as tokens or utility classes).
- Use fixed-pixel dimensions for **chrome widgets** (icon sizes, button tap targets) when the value is in the set. If a chrome dimension is outside the set (e.g. a 24×24 SVG viewport), declare a named token first, then consume it via `var()`.
- Use percentages, `auto`, and flex/grid `gap` for fluid layout.
- Use viewport units (`vw`, `vh`) on the outermost shell only.

**Rationale.** When spacing is open-ended, later readers cannot tell which values are load-bearing and which are accidents. A child with `margin-top: 8px` next to a parent with `gap: 8px` silently produces 16px — nothing in the source signals the doubling.

## R2 — Use padding + gap for spacing; reserve margin for alignment

Spacing between siblings lives on the parent (as `padding`) and on the container (as `gap`). Margin exists for the one job flex/grid cannot do cleanly: axial auto-centering.

**Do**
- Put `padding` on parents and `gap` on flex or grid containers to space siblings.
- Use `margin: auto` (or `margin-inline: auto`, `margin-block: auto`) for alignment inside a container.
- Keep user-agent default margin resets (`h1..h6, p, figure, blockquote, dl, dd, ul, ol { margin: 0 }`) in one designated base layer.

**Avoid** — every author margin declaration outside the `margin: auto` family and the single base-layer reset. If you feel the need to add `margin-top: 8px` on a child, bump the parent's `gap` instead; if the parent doesn't have a `gap`, give it one.

**Rationale.** `padding + gap` localizes spacing decisions to the container. Mixed-in child margins double silently and are invisible in diff review.

## R3 — Keep override control: no `!important`

When a CSS rule loses a cascade battle, the fix lives upstream, not in the cascade itself.

**Do**
- Trace the overriding source. The most common cause is JS writing inline `element.style.*` that CSS then can't beat.
- Refactor the JS to bind per-instance values via `element.style.setProperty('--custom-prop', value)`. The stylesheet still owns the cascade; JS only supplies the value.
- For `<canvas>`: JS owns the **backing store** (HTML `width`/`height` attributes, DPR-scaled). CSS owns the **CSS box** (rendered size). JS writes to the attributes, not to `.style.width` / `.style.height`.
- For size-sensitive HTML elements in general: prefer data-attributes or custom properties as the JS → CSS bridge.

**Last-resort carve-out — third-party styles you cannot modify.** When the overriding rule lives in code you do not own (external widget, embedded SDK, vendor stylesheet) and forking upstream is not an option, a single narrowly-scoped `!important` declaration is acceptable. Leave one short comment naming the third-party source so the declaration can be retired when that source changes. This is the only sanctioned use in authored code.

**Rationale.** `!important` wins once but surrenders override control permanently — any later style layer needs `!important` too, and specificity debugging becomes archeology.

## R4 — Pair `overflow: hidden` with a stated purpose

Four valid purposes. The purpose must be legible alongside the declaration.

**Do — pair `overflow: hidden` with one of:**
- **Letterbox / aspect-ratio container**: the same element declares `aspect-ratio: <ratio>`. `overflow: hidden` clips over-wide content rather than letting it push siblings.
- **Scroll container on the other axis**: the same element declares `overflow-y: auto` or `overflow-x: auto` on the complementary axis. A container with `overflow: hidden` on both axes that scrolls nothing is rarely what was intended.
- **Text ellipsis**: the same element declares `text-overflow: ellipsis` and `white-space: nowrap`.
- **Rounded clipping**: the same element declares a non-zero `border-radius` and needs children (images, backgrounds, inner elements) to respect the rounded shape. Without `overflow: hidden` (or `overflow: clip`), children escape the corners. Prefer `overflow: clip` when available — it does not create a scroll container or a new stacking context.

**When a flex or grid child overflows the parent**, reach for R5 (shrink contract), not `overflow: hidden`. The hidden-overflow pattern hides a layout bug; the shrink contract fixes it.

**Grep signal.** Any `overflow: hidden` without a companion `aspect-ratio`, `overflow-*: auto`, `text-overflow: ellipsis`, or non-zero `border-radius` on the same element is a review flag.

## R5 — Enable flex/grid shrink with `min-*: 0`

A flex or grid item that must shrink below its intrinsic size needs `min-width: 0` and/or `min-height: 0` on itself or its container. Browsers default these to `auto` on flex items, which prevents shrinking.

**Do**
- Add `min-width: 0` (or `min-height: 0`) on flex children that contain long text or replaced elements and need to shrink.
- For replaced elements (`<canvas>`, `<img>`, `<video>`, `<iframe>`) with intrinsic dimensions:
  - Either size them fully by CSS (remove inline `style.width` / `style.height` set by JS — see R3).
  - Or wrap them in an R4-approved `aspect-ratio` + `overflow: hidden` container.
- For aspect-preserving shrink of a replaced element inside flex/grid, pick **one axis** (width or height) and let `aspect-ratio` derive the other. Explicit values on both axes at once leaves `aspect-ratio` no computation axis and distorts the box.

**Rationale.** Flex-item `min-width: auto` equals the child's intrinsic min-content size. A canvas with inline 768×512 size reports 768×512 as min-content, which `flex-shrink` cannot go below — the parent silently grows past the viewport.

## R6 — Use color tokens for authored design

All authored colors reference named tokens declared once in the project's token layer.

**Do**
- Use `var(--color-*)` references in component source, scoped styles, and inline styles.
- Use `color-mix(in oklch, var(--color-a) N%, transparent)` when you need a modulation — the arguments are tokens, the percentage is the variation.

**Non-CSS consumers.** Some render paths cannot resolve `var()` at consumption time — canvas 2D, WebGL, server-rendered SVG baked into email, PDF export. These layers legitimately need literal color fallbacks as defensive defaults. The concrete carve-out (which render paths, which fallback file) belongs in the project supplement, not here. Literal colors in those specific render-layer consumers are not authored design and are out of scope for R6.

**Avoid** — hex, `rgb()`, `rgba()`, `hsl()`, `oklch()`, and `color-mix(...)` with literal arguments in component source. When you need a new color, add a token first.

**Rationale.** Tokens localize design changes to the token file. Literal colors require a global hunt on every change.

## R7 — Place styles in the layer that owns them

Three layers, each with a narrow role. When unsure, follow the decision tree at the bottom.

### Utility layer — repeating, composable atoms

Layout, spacing, typography, token-based color. The default home for style that recurs across components. Concrete mechanism (Tailwind, BEM global classes, CSS Modules, hand-written utility sheet) belongs in the project supplement; the principle ("repeating layout lives here") is universal.

### Component-scoped layer — structure the template needs

The component's own stylesheet (Svelte `<style>`, CSS Modules, Vue SFC `<style>`, scoped styled-components). Use for:

- Nested selectors (`:has()`, `::before`, `::after`, `[data-state='open']`).
- Pseudo-classes (`:hover`, `:focus-visible`, `:disabled`).
- SVG internals (`<g>`, `<path>` styling inside an inline SVG).
- Rules that span multiple elements inside the same template.
- Anything the utility layer cannot express in one class.

### Inline per-instance layer — varying values per element

The element's `style=""` attribute. Two valid purposes:

- **Per-instance CSS custom properties** — `style="--row-accent: {computed};"`. The stylesheet consumes the variable via the component-scoped layer. This is how you vary one property across instances without inventing a class per instance.
- **A single token reference on a single element** — `style="color: var(--color-text);"` or `style="background: var(--color-surface);"`. One declaration, one token reference.

**Avoid in inline style** — literal colors, literal dimensions, multiple unrelated declarations, and any value not resolving through a token or the project's declared scale. If inline style starts doing real work (three declarations, conditional composition, shared values), it's a component waiting to be written.

### Decision tree

1. Can an existing utility class express it? → Utility layer.
2. Does it need a pseudo-class, nested selector, or structural relationship? → Component-scoped layer.
3. Does the value vary per instance? → Declare a `--name` custom property inline on the instance; consume it in the scoped layer.
4. Is it a one-off single-property token reference? → Inline `style="<prop>: var(--color-*)"` is fine.
5. Still needed a literal value? → Stop. Add the token first (R1, R6), then consume it.

## R8 — Use named z-index tokens

Stacking contexts get a small named scale declared once:

```css
--z-base:     0;
--z-overlay:  10;
--z-hud:      20;
--z-modal:    30;
```

**Do**
- Consume via `z-index: var(--z-overlay)` etc.
- Add new levels to the token file when a genuinely new stacking layer appears.

**Avoid** — raw numeric `z-index` in authored source. `z-index: 9999` becomes `z-index: 99999` tomorrow and the scale loses meaning.

**Rationale.** A named scale encodes intent ("this is an overlay, above base, below modal") and survives reviews. Raw numbers become a specificity war.

## Adding to a closed set — exception procedure

**When the set doesn't exist yet.** On a new project or a codebase that never declared a token layer, the procedure below cannot run — there is nothing to add to. The first task is to declare the layer itself: survey the literals already in use, cluster them into an intentional scale (spacing, color, z-index), and land the token file as its own commit with a few initial consumers. Once the set exists, all subsequent work flows through the steps below. Until then, treat R1–R8 as aspirations, not gates.

When you genuinely need a value outside an existing closed set:

1. **Pause at the call site.** Do not reach for `!important`, a bracket utility, or a literal value.
2. **Identify the set** — spacing, color, motion, z-index, etc.
3. **Check the prior-decision log** (project rationale file, design history). The need is often already covered by an existing token.
4. **Add to the token layer.** Name the token for intent (`--spacing-card-inset`, `--color-accent-hover`), not the value.
5. **Land as one atomic commit** — token declaration + first consumer together. Never land a token without a consumer or a consumer without the token.

The general shape is universal. The concrete routing (which token file, which upstream review process) belongs to the project supplement.

## Enforcement signals for review

R1–R8 above are **authoring guidance** — what to do while writing code. The signals below are **review heuristics** — what should fail a review (human or linter). Both trace back to the same principles, but the review list is deliberately narrower so false positives stay low. Signals are starting points for investigation, not automatic rejections; the documented carve-outs above (R3 third-party override, R4 border-radius clipping, R6 non-CSS consumers) remain legitimate.

- `!important` anywhere in authored source (without the R3 third-party-source comment).
- Hex, `rgb(`, `rgba(`, `hsl(`, `oklch(` literals in component source or scoped styles (R6 non-CSS-consumer carve-out excepted).
- A direction-specific margin utility or property outside the single designated base layer or outside the `margin: auto` alignment family.
- `z-index:` with a raw number instead of a token reference.
- `overflow: hidden` with no companion `aspect-ratio`, `overflow-*: auto`, `text-overflow: ellipsis`, or non-zero `border-radius` on the same element.
- JS writing `element.style.width` or `element.style.height` (except `element.style.setProperty('--*', value)` for custom properties).
- Utility-framework arbitrary-value bracket syntax (`-\[.*\]`) without a documented project carve-out.

Framework-specific greps (Tailwind prefixes, Svelte file targeting, `.module.css` patterns) live in the project supplement.

## Tension with framework conventions

These rules describe the universal shape. Every project layers on:

- Which utility CSS framework is in use (Tailwind, UnoCSS, hand-rolled BEM) and which utilities are on or off.
- The concrete spacing set values, color palette, motion catalog.
- Which file is "the token layer" (CSS file, theme object, design tokens JSON).
- Which file is "the base layer" where margin resets live.
- Which grep patterns catch local anti-patterns.

Those bindings belong in the project's own CSS rule file. When the project's supplement and these rules disagree on ergonomics, the project's supplement loses on principle — framework conveniences do not override the underlying discipline.
