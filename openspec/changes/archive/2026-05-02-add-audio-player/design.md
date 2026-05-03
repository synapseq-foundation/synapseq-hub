## Context

The project is a SvelteKit static app using Svelte 5, TypeScript, Tailwind CSS, and `@lucide/svelte`. The current root route only redirects users to the main SynapSeq site. Static hub assets already exist under `static/`, including `/manifest.json`, audio package files, and `/artwork/default.webp`.

The player should replace the redirecting root route with a self-contained browsing and playback interface. The app remains static and client-friendly: metadata is fetched from `/manifest.json`, artwork is resolved from static paths, and user preferences are stored in browser `localStorage`.

## Goals / Non-Goals

**Goals:**

- Build the main route as a warm SynapSeq audio browsing experience with header, categories, list, and fixed player.
- Keep the data source simple by reading `/manifest.json` directly from the site root.
- Use Svelte 5 runes for local reactive state and `$derived` for computed category and sorted-list state.
- Persist theme and favorites locally without adding backend state.
- Preserve long-session readability with the provided SynapSeq light and dark CSS tokens.

**Non-Goals:**

- No backend API, database, authentication, or manifest schema changes.
- No audio file format conversion or `.spsq` parsing in this change.
- No synced favorites across devices.
- No advanced playback queue, waveform visualization, or media session integration.

## Decisions

### Use the root Svelte route as the player shell

Replace the current `src/routes/+page.svelte` redirect with the complete player interface. This is the smallest correct change because the requested experience is the layout principal/rota principal and there are no other routes in the app.

Alternative considered: create nested route/component architecture first. That adds structure before reuse exists. The implementation can still extract small components only where it reduces duplication, such as shared audio details markup for list rows and the fixed player.

### Fetch manifest on the client from `/manifest.json`

Use a relative root fetch exactly as requested: `fetch('/manifest.json')`. The data can be stored in `$state.raw` because manifest entries are API/static response data that are reassigned rather than deeply mutated.

Alternative considered: SvelteKit `load` fetching. Client fetch keeps the implementation direct, avoids coupling prerendered page output to manifest content, and matches the requirement that the application reads the root file at runtime.

### Keep UI state local to the page

Maintain selected category, selected audio ID, theme, and favorite timestamps in local page state. Use `$derived` for unique categories, selected entry, favorite-aware sorting, and filtered entries.

Alternative considered: shared stores or module-level state. They are unnecessary for a single route and can create SSR leakage risks. Local page state is simpler and correctly scoped.

### Persist favorites as timestamped IDs

Store favorites in `localStorage` as an object or array that preserves `id` and `favoritedAt`. Sorting can then place favorites above all other entries in descending favorite time. Enforce the five-favorite limit in the favorite button handler before writing storage.

Alternative considered: store only an array of IDs. That cannot reliably satisfy ordering by favorite date unless array order is treated as persistent timestamp semantics. Explicit timestamps are clearer and more resilient.

### Use image load fallback per artwork element

Render artwork with `/artwork/{id}.webp` and set the image `src` to `/artwork/default.webp` from the image error handler. This avoids pre-fetching each artwork path and handles missing files independently for list and player artwork.

Alternative considered: fetch artwork with `HEAD` before rendering. That increases network traffic and implementation complexity for a simple static fallback.

### Apply theme through `html[data-theme]`

Define the provided CSS tokens globally and switch dark mode by setting `document.documentElement.dataset.theme = 'dark'` or removing/changing it for light mode. Persist the chosen theme in `localStorage`.

Alternative considered: component-scoped theme class. The requested token model explicitly recommends `html[data-theme="dark"]`, and document-level theme also lets `color-scheme` apply consistently.

### Treat Play as a player control placeholder unless playable media is available

The manifest entries point to `.spsq` package files, not conventional browser audio files. The player should select and display the active audio package and provide a Play button control in the UI. If implementation discovers a directly playable audio source inside existing app conventions, the button can control an `<audio>` element; otherwise it should remain a clearly wired UI control without pretending `.spsq` is browser-playable.

Alternative considered: set an `<audio>` element directly to `download_url` or `path`. That is risky because `.spsq` is not guaranteed to be playable by the browser.

## Risks / Trade-offs

- Missing or invalid manifest data -> show an empty/error state and keep the page usable rather than crashing.
- `localStorage` is unavailable or blocked -> guard storage reads/writes and keep in-memory behavior working for the session.
- Favorite limit needs user feedback -> prevent the sixth favorite and expose a visible message or disabled affordance so the limit is understandable.
- Artwork fallback can recurse if the default image is missing -> only swap to `/artwork/default.webp` when the current source is not already the fallback.
- Static prerender plus client-only browser APIs -> initialize browser-only state from mount/effects or guarded code so `svelte-check` and prerender remain safe.
