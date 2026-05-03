## Context

The current `src/routes/+page.svelte` implements the entire Hub Player in one file: manifest loading, theme/favorites persistence, derived list state, reusable audio details markup, header, categories, list, fixed player, and route styles. The app uses Svelte 5 and Tailwind, and should continue to follow runes mode, `$props`, keyed each blocks, and `onclick` event attributes.

This change is a componentization refactor. It should preserve the existing route behavior while making each major UI section independently maintainable.

## Goals / Non-Goals

**Goals:**

- Move the header, categories, list, fixed player, and reusable audio details UI into Svelte components.
- Keep shared audio player types/constants in importable TypeScript module(s), avoiding duplicate type definitions across components.
- Keep route-level state and business rules in `+page.svelte`, including manifest loading, selected category/audio, favorites, theme, and local storage persistence.
- Keep components mostly presentational, with explicit typed callback props for user actions.
- Use Tailwind utilities for extracted component styling instead of pure CSS blocks.
- Preserve the current visual design, CSS token usage, responsive layout, and behavior.

**Non-Goals:**

- No redesign of the Hub Player UI.
- No change to `/manifest.json`, artwork paths, local storage keys, favorite limit, sorting rules, or theme behavior.
- No introduction of global stores, context, backend calls, or additional dependencies.
- No implementation of actual `.spsq` audio playback beyond the existing Play control behavior.
- No replacement of existing SynapSeq CSS tokens with hardcoded Tailwind color values.

## Decisions

### Keep orchestration in the route

`src/routes/+page.svelte` remains responsible for fetching `/manifest.json`, restoring/persisting theme and favorites, computing derived state, and handling actions. Components receive data and callbacks as props.

Alternative considered: move state into a shared store or component context. That would add indirection and risk broader state lifetime than needed for a single route.

### Use a small component folder under `src/lib/components/player`

Create focused components for:

- `PlayerHeader.svelte`: logo, title, theme toggle.
- `CategoryBadges.svelte`: horizontal scrollable category badges.
- `AudioDetails.svelte`: shared artwork/title/author display used by rows and player.
- `AudioList.svelte`: list shell and favorite buttons.
- `AudioPlayerBar.svelte`: fixed bottom player with selected details and Play button.
- `StatePanel.svelte` if loading/error/empty state markup remains duplicated or benefits from extraction.

Alternative considered: place components next to the route. `src/lib/components/player` makes them easy to import and keeps route files focused.

### Move shared types/constants to a TypeScript module

Create `src/lib/player/types.ts` and optionally `src/lib/player/constants.ts` for `Theme`, `AudioEntry`, `Manifest`, `FavoriteRecord`, `defaultArtwork`, storage keys, and `maxFavorites`. This keeps component props typed without redefining structures.

Alternative considered: keep types in `+page.svelte` and export snippets. Route-local types cannot be cleanly imported by child components and would work against the goal of separation.

### Keep artwork fallback local to the reusable details component

`AudioDetails.svelte` should compute `/artwork/{id}.webp` from the entry ID and handle its own image `onerror` fallback to `/artwork/default.webp`. This removes duplicated fallback handling from list and player usages.

Alternative considered: pass precomputed artwork URLs and error handlers from the route. That spreads image concerns across callers and makes the shared component less useful.

### Use Tailwind utilities for component styling

Extracted components should express layout, spacing, borders, responsive behavior, hover states, truncation, and alignment through Tailwind utility classes. Use arbitrary values for existing SynapSeq tokens, such as `bg-[var(--panel-strong)]`, `text-[var(--muted)]`, `border-[var(--line)]`, and `shadow-[var(--shadow)]`, so the componentized UI continues to honor the light/dark token system.

Keep global body background composition, root page shell constraints, CSS variables, and any scrollbar-hiding utility that cannot be cleanly represented with existing Tailwind utilities in route/global CSS. Avoid new component-level `<style>` blocks unless there is no practical Tailwind equivalent.

Alternative considered: move scoped CSS blocks into each component. That improves locality but conflicts with the project direction to use Tailwind for component styling.

## Risks / Trade-offs

- Prop drilling can grow across components -> keep components shallow and callbacks explicit rather than introducing stores prematurely.
- CSS-to-Tailwind conversion can cause visual regressions -> preserve class intent, use token-backed arbitrary values, and validate with check/build plus manual review.
- Svelte prop typing mistakes can break reactivity -> use `$props` in every component and validate each `.svelte` file with the Svelte 5 autofixer.
- Event callbacks can be invoked from nested controls unexpectedly -> keep row selection and favorite click handlers on distinct buttons as in the current implementation.
