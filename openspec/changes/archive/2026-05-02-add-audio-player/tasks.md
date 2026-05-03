## 1. Data And State

- [x] 1.1 Replace the root route redirect with player state setup in `src/routes/+page.svelte` using Svelte 5 runes.
- [x] 1.2 Add TypeScript types for manifest metadata, audio entries, favorite records, and theme values.
- [x] 1.3 Fetch `/manifest.json` on the client, store entries as reassigned response data, and show safe loading/error/empty states.
- [x] 1.4 Derive categories, selected entry, filtered entries, and favorite-sorted entries from local state.

## 2. Persistence

- [x] 2.1 Implement guarded local storage read/write helpers for theme and favorites.
- [x] 2.2 Restore the saved theme and apply it through `html[data-theme]`.
- [x] 2.3 Restore saved favorites with timestamps and ignore malformed or unknown stored entries.
- [x] 2.4 Implement favorite toggling, unfavoriting, timestamp ordering, and the five-favorite limit.

## 3. Player Interface

- [x] 3.1 Add the SynapSeq light and dark CSS tokens plus atmospheric page backgrounds in `src/routes/layout.css` or route styles.
- [x] 3.2 Build the header with `/artwork/default.webp`, `Hub Player`, and a light/dark toggle using `@lucide/svelte`.
- [x] 3.3 Build the horizontal, invisibly scrollable category badge strip from manifest categories.
- [x] 3.4 Build the audio list rows with artwork, title, author, row selection, and a heart favorite button.
- [x] 3.5 Implement per-image artwork fallback from `/artwork/{id}.webp` to `/artwork/default.webp`.
- [x] 3.6 Build the fixed bottom player with selected audio details and a right-aligned Play button using `@lucide/svelte`.
- [x] 3.7 Ensure the layout works on mobile and desktop with enough bottom padding so the fixed player does not cover the list.

## 4. Verification

- [x] 4.1 Run `npx @sveltejs/mcp svelte-autofixer ./src/routes/+page.svelte --svelte-version 5` and apply any required fixes.
- [x] 4.2 Run `npm run check` and fix Svelte or TypeScript issues.
- [x] 4.3 Run `npm run build` and verify the static app builds successfully.
- [x] 4.4 Manually verify manifest loading, category filtering, artwork fallback, theme persistence, favorite ordering, favorite limit, and player selection.
