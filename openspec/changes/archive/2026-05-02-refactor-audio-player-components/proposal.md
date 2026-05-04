## Why

The current audio player route contains state management, reusable UI fragments, layout markup, and section styling in one large Svelte file. Splitting the header, categories, list, reusable audio details, and fixed player into components will make the player easier to maintain without changing the existing user-facing behavior.

## What Changes

- Extract the header, categories, audio list, fixed player, and reusable audio details UI into Svelte components under the project component area.
- Move shared audio player types and constants out of the root route so page and components can import the same definitions.
- Keep route-level orchestration in `src/routes/+page.svelte`: data loading, selected category, selected audio, favorites, theme, and player messages remain owned by the page.
- Keep component props explicit and typed with Svelte 5 `$props`.
- Use Tailwind utility classes for component layout and styling instead of pure component CSS, while preserving existing CSS variables/tokens.
- Preserve existing behavior for manifest loading, category filtering, artwork fallback, favorites, theme switching, selection, and the Play control.
- Validate each new Svelte component with the Svelte 5 autofixer and the existing check/build commands.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `audio-player`: Add a component architecture requirement for the existing player UI while preserving all current behavior.

## Impact

- Affects `src/routes/+page.svelte` by reducing it to route-level state orchestration and composition.
- Adds Svelte components under `src/lib/components/` or an equivalent project component folder.
- Adds shared TypeScript module(s) for audio player types/constants if needed.
- Converts extracted component styling to Tailwind utilities, relying on existing CSS token variables through arbitrary values where needed.
- Does not change `/manifest.json`, static artwork paths, local storage keys, or external dependencies.
