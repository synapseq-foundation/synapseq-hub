## Why

The current player route wraps the header, categories, and audio list inside a centered card-like `<section>` with borders, rounded corners, and shadows. This creates a visual “card on a background” effect that limits how immersive and expansive the browsing experience feels. The user wants the main content area to feel like a full-page workspace, with the background and shell extending cleanly behind the content, while keeping the fixed player bar unchanged at the bottom.

## What Changes

- Remove the inner `<section>` wrapper from `+page.svelte` that currently groups the header, categories, and list.
- Move the background, padding, and layout responsibilities directly to the `<main>` element so the page feels like one continuous surface.
- Eliminate borders, rounded corners, and shadows from the main content container so it blends with the page background.
- Keep the fixed `<AudioPlayerBar>` and its positioning unchanged.
- Preserve all existing behavior: manifest loading, category filtering, artwork fallback, favorites, theme switching, selection, and Play control.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `audio-player`: Modify the layout requirement so the main content area uses a full-page container without card-like borders, while the fixed player remains unchanged.

## Impact

- Affects `src/routes/+page.svelte` by simplifying its DOM structure and moving Tailwind layout classes.
- Does not change extracted components: `PlayerHeader`, `CategoryBadges`, `AudioList`, `AudioDetails`, `StatePanel`.
- Does not change `src/routes/layout.css`, theme tokens, local storage keys, or static assets.
- Does not change the fixed player bar or its positioning.
