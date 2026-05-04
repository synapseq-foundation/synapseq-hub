## Why

The hub currently exposes audio packages through a manifest, but the main experience does not give users a focused way to browse, prioritize, and play available audio entries. Adding a dedicated audio player turns the hub into a usable listening interface while preserving the lightweight static manifest model.

## What Changes

- Add a main-route audio player layout with header, horizontal category filters, audio list, and fixed bottom player.
- Load audio metadata from `/manifest.json` without a base URL and render available entries from its `entries` array.
- Resolve artwork from `/artwork/{id}.webp`, falling back to `/artwork/default.webp` when an entry image cannot load.
- Allow users to select an audio entry with one tap, making it the active item in the bottom player.
- Add local theme switching between light and dark using the SynapSeq warm color tokens.
- Add local favorites with heart icons, persisted in device local storage, limited to five favorites.
- Sort favorites to the top of the list by the time they were favorited, while keeping non-favorites available below.
- Use `@lucide/svelte` icons for theme, favorite, and play controls.

## Capabilities

### New Capabilities

- `audio-player`: Covers manifest-driven audio browsing, category filtering, artwork fallback, item selection, fixed player controls, theme switching, and persisted favorites.

### Modified Capabilities

None.

## Impact

- Affects the Svelte main route and related UI component structure.
- Reads the existing static `/manifest.json` endpoint and artwork assets under `/artwork/`.
- Uses browser `localStorage` for theme and favorites persistence.
- Uses the already-installed `@lucide/svelte` package for UI icons.
- Does not require backend API changes or changes to the manifest schema.
